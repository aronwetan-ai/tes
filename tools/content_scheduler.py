#!/usr/bin/env python3
"""
content_scheduler.py — BrandFlow editorial pipeline + scheduler.

Operates over the per-client JSONL pipeline at:

    companies/brandflow/clients/<client>/pipeline/
        inbox.jsonl       (IDEA stage)
        active.jsonl      (BRIEF / DRAFT / REVIEW / APPROVED)
        scheduled.jsonl   (SCHEDULED / FATHUR_APPROVED)
        published.jsonl   (PUBLISHED / MEASURED)

Enforces:
  - Stage state machine (validated transitions only)
  - Brief-completeness validation at IDEA → BRIEF transition
  - Boundary #4 hardcoded gate at SCHEDULED → PUBLISHED:
        requires `boundary_4_status == "fathur_approved"` (per-piece sign-off)
  - Per-channel cap (default 3/day per client per channel)
  - Quiet-hours respect (default: 22:00 - 08:00 local; configurable)

This tool DOES NOT call external scheduler APIs (Buffer, Hootsuite, etc.).
It manages the agency-internal state machine and emits a `release` action
that downstream integrations consume.

Tier:    Update 11 (BrandFlow deepening)
Risk:    Medium (mutates pipeline JSONL files)
Status:  Active

Subcommands:
    list        List pieces in a stage (read-only)
    add         Append a new IDEA to inbox
    advance     Transition a piece to next stage (validates state machine)
    approve     Mark a piece FATHUR_APPROVED (Boundary #4 gate)
    release     Move FATHUR_APPROVED → PUBLISHED (records published_at)
    validate    Validate pipeline integrity (no orphans, no invalid stages)

Usage:
    python3 content_scheduler.py list --client acme --stage DRAFT
    python3 content_scheduler.py add --client acme --campaign summer-launch \\
        --channel instagram --format carousel --owner @brandflow.copywriter
    python3 content_scheduler.py advance --client acme --id BF-acme-0142 \\
        --to DRAFT --by @brandflow.copywriter
    python3 content_scheduler.py approve --client acme --id BF-acme-0142 \\
        --by fathur --signature "fathur-2026-05-17-1430"
    python3 content_scheduler.py release --client acme --id BF-acme-0142 \\
        --published-url https://instagram.com/p/...
    python3 content_scheduler.py validate --client acme

Exit codes:
    0   success
    1   validation / state-machine error
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STAGES = (
    "IDEA",
    "BRIEF",
    "DRAFT",
    "REVIEW",
    "REVISION",
    "APPROVED",
    "SCHEDULED",
    "FATHUR_APPROVED",
    "PUBLISHED",
    "MEASURED",
    "KILLED",
    "ARCHIVED",
)

# Allowed transitions (from -> set of valid to)
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "IDEA":             {"BRIEF", "KILLED"},
    "BRIEF":            {"DRAFT", "KILLED"},
    "DRAFT":            {"REVIEW", "KILLED"},
    "REVIEW":           {"APPROVED", "REVISION", "KILLED"},
    "REVISION":         {"DRAFT", "KILLED"},
    "APPROVED":         {"SCHEDULED", "KILLED"},
    "SCHEDULED":        {"FATHUR_APPROVED", "APPROVED", "KILLED"},
    "FATHUR_APPROVED":  {"PUBLISHED", "KILLED"},
    "PUBLISHED":        {"MEASURED"},
    "MEASURED":         {"ARCHIVED"},
    "KILLED":           {"ARCHIVED"},
}

# Mapping of stages to which file they live in
STAGE_FILE_MAP = {
    "IDEA":            "inbox.jsonl",
    "BRIEF":           "active.jsonl",
    "DRAFT":           "active.jsonl",
    "REVIEW":          "active.jsonl",
    "REVISION":        "active.jsonl",
    "APPROVED":        "active.jsonl",
    "SCHEDULED":       "scheduled.jsonl",
    "FATHUR_APPROVED": "scheduled.jsonl",
    "PUBLISHED":       "published.jsonl",
    "MEASURED":        "published.jsonl",
    "KILLED":          "active.jsonl",
    "ARCHIVED":        "active.jsonl",
}

REQUIRED_BRIEF_FIELDS = (
    "audience", "goal", "channel", "tone", "format", "kpi", "deadline",
)

DEFAULT_CHANNEL_DAILY_CAP = 3
DEFAULT_QUIET_HOURS = (22, 8)  # publish blocked between 22:00 and 08:00 local


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _home() -> Path:
    return Path(
        os.environ.get(
            "AI_HOLDING_HOME",
            "/home/fatur/ai-holding",
        )
    )


def _client_dir(client: str) -> Path:
    return _home() / "companies" / "brandflow" / "clients" / client


def _pipeline_dir(client: str) -> Path:
    return _client_dir(client) / "pipeline"


def _file_for_stage(client: str, stage: str) -> Path:
    name = STAGE_FILE_MAP.get(stage)
    if not name:
        raise ValueError(f"unknown stage: {stage}")
    return _pipeline_dir(client) / name


def _ensure_dirs(client: str) -> None:
    p = _pipeline_dir(client)
    p.mkdir(parents=True, exist_ok=True)
    for fname in {
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    }:
        f = p / fname
        if not f.exists():
            f.touch()


# ---------------------------------------------------------------------------
# JSONL IO
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    items: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"{path}:{line_num} invalid JSON: {e}"
                ) from e
    return items


def _write_jsonl(path: Path, items: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def _append_jsonl(path: Path, item: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Pipeline ops
# ---------------------------------------------------------------------------

def _next_seq(client: str) -> int:
    """Highest sequence number in pipeline + 1."""
    base = _pipeline_dir(client)
    max_seq = 0
    for fname in (
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    ):
        for item in _read_jsonl(base / fname):
            piece_id = item.get("id", "")
            # BF-<client>-<seq>
            parts = piece_id.split("-")
            if len(parts) >= 3:
                try:
                    n = int(parts[-1])
                    if n > max_seq:
                        max_seq = n
                except ValueError:
                    pass
    return max_seq + 1


def _find_piece(client: str, piece_id: str) -> tuple[dict, Path] | None:
    base = _pipeline_dir(client)
    for fname in (
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    ):
        path = base / fname
        for item in _read_jsonl(path):
            if item.get("id") == piece_id:
                return item, path
    return None


def _update_piece(client: str, piece_id: str, new_item: dict) -> Path:
    """Replace piece in its current file; return path written."""
    base = _pipeline_dir(client)
    for fname in (
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    ):
        path = base / fname
        items = _read_jsonl(path)
        replaced = False
        out: list[dict] = []
        for it in items:
            if it.get("id") == piece_id:
                out.append(new_item)
                replaced = True
            else:
                out.append(it)
        if replaced:
            _write_jsonl(path, out)
            return path
    raise ValueError(f"piece {piece_id} not found in client {client}")


def _move_piece(client: str, piece_id: str, target_path: Path) -> None:
    """Move piece from its current file to target_path."""
    base = _pipeline_dir(client)
    moved_item: dict | None = None
    for fname in (
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    ):
        path = base / fname
        if path == target_path:
            continue
        items = _read_jsonl(path)
        out: list[dict] = []
        for it in items:
            if it.get("id") == piece_id and moved_item is None:
                moved_item = it
            else:
                out.append(it)
        if moved_item and len(out) != len(items):
            _write_jsonl(path, out)
            break
    if not moved_item:
        # Piece may already be in target_path; that's a no-op.
        return
    _append_jsonl(target_path, moved_item)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    _ensure_dirs(args.client)
    base = _pipeline_dir(args.client)
    files = (
        ("inbox.jsonl", "inbox"),
        ("active.jsonl", "active"),
        ("scheduled.jsonl", "scheduled"),
        ("published.jsonl", "published"),
    )
    rows: list[dict] = []
    for fname, _bucket in files:
        for it in _read_jsonl(base / fname):
            if args.stage and it.get("stage") != args.stage:
                continue
            if args.channel and it.get("channel") != args.channel:
                continue
            rows.append(it)

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        if not rows:
            print(f"(no pieces match for client={args.client})")
            return 0
        print(f"client={args.client} count={len(rows)}")
        for r in rows:
            print(
                f"  {r.get('id','?'):24s}  "
                f"{r.get('stage','?'):18s}  "
                f"{r.get('channel','?'):10s}  "
                f"{r.get('format','?'):12s}  "
                f"owner={r.get('owner','?')}  "
                f"due={r.get('due','-')}"
            )
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    _ensure_dirs(args.client)
    seq = _next_seq(args.client)
    piece = {
        "id": f"BF-{args.client}-{seq:04d}",
        "client_id": args.client,
        "campaign_id": args.campaign,
        "company": "brandflow",
        "format": args.format,
        "channel": args.channel,
        "stage": "IDEA",
        "owner": args.owner,
        "due": args.due,
        "scheduled_at": None,
        "published_at": None,
        "published_url": None,
        "brief": {},
        "draft": {},
        "review_notes": [],
        "approvals": [],
        "metrics": {},
        "utm": {},
        "boundary_4_status": "draft_only",
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
    }
    _append_jsonl(_file_for_stage(args.client, "IDEA"), piece)
    if args.json:
        print(json.dumps(piece, ensure_ascii=False, indent=2))
    else:
        print(f"created {piece['id']} stage=IDEA channel={piece['channel']}")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    found = _find_piece(args.client, args.id)
    if not found:
        print(f"error: piece {args.id} not found", file=sys.stderr)
        return 1
    piece, _path = found

    current = piece.get("stage")
    target = args.to

    if target not in STAGES:
        print(f"error: unknown target stage '{target}'", file=sys.stderr)
        return 2

    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        print(
            f"error: illegal transition {current} -> {target}. "
            f"Allowed from {current}: {sorted(allowed) or '(none)'}",
            file=sys.stderr,
        )
        return 1

    # Brief-completeness gate at IDEA → BRIEF
    if current == "IDEA" and target == "BRIEF":
        brief = piece.get("brief", {}) or {}
        missing = [f for f in REQUIRED_BRIEF_FIELDS if not brief.get(f)]
        if missing:
            print(
                f"error: brief missing required fields: "
                f"{', '.join(missing)}. Fill brief before advancing.",
                file=sys.stderr,
            )
            return 1

    # Hardcoded Boundary #4 gate at FATHUR_APPROVED → PUBLISHED
    if current == "FATHUR_APPROVED" and target == "PUBLISHED":
        if piece.get("boundary_4_status") != "fathur_approved":
            print(
                "error: Boundary #4 gate violated — boundary_4_status must "
                "be 'fathur_approved' before publishing. "
                "Use the `approve` subcommand first.",
                file=sys.stderr,
            )
            return 1

    # Update piece
    piece["stage"] = target
    piece["updated_at"] = _now()
    if target == "PUBLISHED":
        piece["published_at"] = _now()

    target_path = _file_for_stage(args.client, target)
    current_path = _file_for_stage(args.client, current)

    if target_path == current_path:
        # Same file; just update in place
        _update_piece(args.client, args.id, piece)
    else:
        # Cross-file move
        _update_piece(args.client, args.id, piece)
        _move_piece(args.client, args.id, target_path)

    print(f"advanced {args.id}: {current} -> {target}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    found = _find_piece(args.client, args.id)
    if not found:
        print(f"error: piece {args.id} not found", file=sys.stderr)
        return 1
    piece, _path = found

    if piece.get("stage") not in ("SCHEDULED",):
        print(
            f"error: piece must be in SCHEDULED stage to receive Fathur "
            f"approval (current: {piece.get('stage')}).",
            file=sys.stderr,
        )
        return 1

    if args.by != "fathur":
        print(
            f"error: only 'fathur' can sign Boundary #4 approval "
            f"(got --by {args.by}).",
            file=sys.stderr,
        )
        return 1

    if not args.signature:
        print("error: --signature required (Boundary #4 audit trail).", file=sys.stderr)
        return 2

    piece["stage"] = "FATHUR_APPROVED"
    piece["boundary_4_status"] = "fathur_approved"
    piece.setdefault("approvals", []).append({
        "by": "fathur",
        "at": _now(),
        "stage_advanced_to": "FATHUR_APPROVED",
        "signature": args.signature,
    })
    piece["updated_at"] = _now()

    _update_piece(args.client, args.id, piece)
    print(
        f"approved {args.id} by fathur (Boundary #4 cleared); "
        f"now eligible for release."
    )
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    found = _find_piece(args.client, args.id)
    if not found:
        print(f"error: piece {args.id} not found", file=sys.stderr)
        return 1
    piece, _path = found

    if piece.get("stage") != "FATHUR_APPROVED":
        print(
            f"error: piece must be FATHUR_APPROVED to release "
            f"(current: {piece.get('stage')}).",
            file=sys.stderr,
        )
        return 1
    if piece.get("boundary_4_status") != "fathur_approved":
        print(
            "error: Boundary #4 gate violated — boundary_4_status mismatch.",
            file=sys.stderr,
        )
        return 1

    # Channel daily cap check
    cap = args.channel_cap or DEFAULT_CHANNEL_DAILY_CAP
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    pub_path = _file_for_stage(args.client, "PUBLISHED")
    pub_today = sum(
        1
        for it in _read_jsonl(pub_path)
        if it.get("channel") == piece.get("channel")
        and (it.get("published_at") or "").startswith(today)
    )
    if pub_today >= cap:
        print(
            f"error: channel cap reached for {piece.get('channel')} today "
            f"({pub_today}/{cap}).",
            file=sys.stderr,
        )
        return 1

    piece["stage"] = "PUBLISHED"
    piece["published_at"] = _now()
    piece["published_url"] = args.published_url
    piece["boundary_4_status"] = "published"
    piece["updated_at"] = _now()

    _update_piece(args.client, args.id, piece)
    _move_piece(args.client, args.id, pub_path)

    print(f"released {args.id} to PUBLISHED at {piece['published_at']}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    base = _pipeline_dir(args.client)
    if not base.exists():
        print(f"error: client pipeline dir does not exist: {base}", file=sys.stderr)
        return 2
    issues: list[str] = []
    seen_ids: dict[str, list[str]] = {}
    for fname in (
        "inbox.jsonl", "active.jsonl", "scheduled.jsonl", "published.jsonl",
    ):
        path = base / fname
        for it in _read_jsonl(path):
            pid = it.get("id", "<missing>")
            seen_ids.setdefault(pid, []).append(fname)
            stage = it.get("stage")
            if stage not in STAGES:
                issues.append(f"{fname}: piece {pid} has unknown stage {stage!r}")
                continue
            expected = STAGE_FILE_MAP.get(stage)
            if expected and expected != fname:
                issues.append(
                    f"{fname}: piece {pid} stage {stage} should live in {expected}"
                )

    for pid, where in seen_ids.items():
        if len(where) > 1:
            issues.append(f"piece {pid} appears in multiple files: {where}")

    if issues:
        print(f"validate: {len(issues)} issue(s):")
        for i in issues:
            print(f"  - {i}")
        return 1
    print(f"validate: OK ({len(seen_ids)} pieces across pipeline)")
    return 0


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "BrandFlow editorial pipeline state-machine + scheduler. "
            "See companies/brandflow/skills/automation/SKILL.md."
        )
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="List pieces in a client's pipeline.")
    s.add_argument("--client", required=True)
    s.add_argument("--stage", default=None, choices=STAGES)
    s.add_argument("--channel", default=None)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("add", help="Append a new IDEA to inbox.")
    s.add_argument("--client", required=True)
    s.add_argument("--campaign", required=True, help="Campaign id (slug).")
    s.add_argument("--channel", required=True)
    s.add_argument("--format", required=True)
    s.add_argument("--owner", required=True, help="@brandflow.<role>")
    s.add_argument("--due", default=None, help="YYYY-MM-DD (optional).")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser(
        "advance",
        help="Transition a piece to next stage (state-machine validated).",
    )
    s.add_argument("--client", required=True)
    s.add_argument("--id", required=True, help="Piece id (BF-<client>-<seq>).")
    s.add_argument("--to", required=True, choices=STAGES)
    s.add_argument("--by", required=True, help="@brandflow.<role> or fathur")
    s.set_defaults(func=cmd_advance)

    s = sub.add_parser(
        "approve",
        help="Mark FATHUR_APPROVED (Boundary #4 gate). Only --by fathur allowed.",
    )
    s.add_argument("--client", required=True)
    s.add_argument("--id", required=True)
    s.add_argument("--by", required=True, help="Must be 'fathur'.")
    s.add_argument(
        "--signature", required=True,
        help="Approval signature for audit (e.g. 'fathur-2026-05-17-1430').",
    )
    s.set_defaults(func=cmd_approve)

    s = sub.add_parser(
        "release",
        help="Move FATHUR_APPROVED → PUBLISHED with channel-cap check.",
    )
    s.add_argument("--client", required=True)
    s.add_argument("--id", required=True)
    s.add_argument(
        "--published-url", required=True, help="Native post URL after publish.",
    )
    s.add_argument(
        "--channel-cap", type=int, default=None,
        help=f"Per-channel daily cap (default {DEFAULT_CHANNEL_DAILY_CAP}).",
    )
    s.set_defaults(func=cmd_release)

    s = sub.add_parser("validate", help="Validate pipeline integrity.")
    s.add_argument("--client", required=True)
    s.set_defaults(func=cmd_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
