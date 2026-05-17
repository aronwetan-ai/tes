#!/usr/bin/env python3
"""
task_logger.py — Shared library for AI Holding Task Logger.

Provides core functions used by:
  - log_task.py     (create new task)
  - update_task.py  (transition task status)
  - list_tasks.py   (filter & list)
  - log_message.py  (agent-to-agent message)

Schema (single source of truth, mirrors companies/<co>/skills/automation/SKILL.md):
{
  "id":          "T001",
  "company":     "nexusai" | "brandflow" | "crypto-consultant" | "holding",
  "from":        "USER" | "@<company>.<agent>" | "MAIN",
  "to":          "@<company>" | "@<company>.<agent>" | "MAIN",
  "task":        "<one-line description>",
  "priority":    "LOW" | "MEDIUM" | "HIGH" | "URGENT",
  "status":      "NEW" | "IN_PROGRESS" | "DONE" | "FAILED" | "CANCELLED" | "RETRY",
  "created_at":  "<ISO-8601 UTC>",
  "updated_at":  "<ISO-8601 UTC>",
  "context":     {<arbitrary JSON object, optional>}
}

Files:
  inbox.jsonl     — single source of truth for tasks (status field differentiates)
  logs.jsonl      — append-only audit log of every state transition
  messages.jsonl  — agent-to-agent durable messages
  recap.jsonl     — periodic summaries (untouched by this module; reserved)

Filter rules: see knowledge/agent-design/task-logger-rules.md.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_STATUSES = {"NEW", "IN_PROGRESS", "DONE", "FAILED", "CANCELLED", "RETRY"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH", "URGENT"}
TERMINAL_STATUSES = {"DONE", "FAILED", "CANCELLED"}

# Allowed status transitions (state machine)
ALLOWED_TRANSITIONS: Dict[str, set] = {
    "NEW":         {"IN_PROGRESS", "CANCELLED"},
    "IN_PROGRESS": {"DONE", "FAILED", "CANCELLED"},
    "FAILED":      {"RETRY", "CANCELLED"},
    "RETRY":       {"IN_PROGRESS", "CANCELLED"},
    "DONE":        set(),       # terminal
    "CANCELLED":   set(),       # terminal
}

REQUIRED_FIELDS = ("id", "company", "from", "to", "task", "priority",
                   "status", "created_at", "updated_at")


# ---------------------------------------------------------------------------
# Workspace + path resolution
# ---------------------------------------------------------------------------

def workspace_root() -> Path:
    """
    Resolve the AI Holding workspace root.

    Resolution order:
      1. AI_HOLDING_HOME env var (explicit override).
      2. Walk upward from this file until we find a directory containing
         BOTH 'companies/' and 'tasks/' (heuristic for the repo root).
      3. Fallback to two levels up from this file (bin/ → repo root).
    """
    env = os.environ.get("AI_HOLDING_HOME")
    if env:
        return Path(env).expanduser().resolve()

    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if (parent / "companies").is_dir() and (parent / "tasks").is_dir():
            return parent
    return here.parent.parent  # fallback: bin/ -> repo root


def company_tasks_dir(company: str) -> Path:
    """Return path to a company's tasks/ folder. 'holding' → root tasks/."""
    root = workspace_root()
    if company == "holding":
        return root / "tasks"
    return root / "companies" / company / "tasks"


def file_path(company: str, name: str) -> Path:
    """Resolve a task file path for a given company.

    name in {"inbox", "logs", "messages", "recap"}.
    """
    if name not in {"inbox", "logs", "messages", "recap"}:
        raise ValueError(f"unknown task file: {name}")
    return company_tasks_dir(company) / f"{name}.jsonl"


# ---------------------------------------------------------------------------
# Time + ID helpers
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    """Return current UTC time as ISO-8601 with 'Z' suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_task_id(company: str) -> str:
    """
    Compute next task ID by scanning inbox.jsonl for the highest existing
    T### number. Returns 'T001' if no tasks yet. ID space is per-company.
    """
    inbox = file_path(company, "inbox")
    max_n = 0
    if inbox.is_file():
        for entry in iter_jsonl(inbox):
            tid = entry.get("id", "")
            if isinstance(tid, str) and tid.startswith("T") and tid[1:].isdigit():
                n = int(tid[1:])
                if n > max_n:
                    max_n = n
    return f"T{max_n + 1:03d}"


# ---------------------------------------------------------------------------
# JSONL I/O (atomic append, line-by-line iter, in-place update)
# ---------------------------------------------------------------------------

def ensure_file(path: Path) -> None:
    """Make sure the parent directory and the file itself exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def append_jsonl(path: Path, entry: Dict[str, Any]) -> None:
    """Append one JSON object as a single line. Creates file if missing."""
    ensure_file(path)
    line = json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    """Yield each JSON object in a JSONL file. Skips blank lines."""
    if not path.is_file():
        return
    with path.open("r", encoding="utf-8") as fh:
        for ln, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                # Surface but don't crash a list/filter op on a single bad line.
                print(f"[task_logger] WARN: {path}:{ln} invalid JSON: {e}",
                      file=sys.stderr)


def read_all(path: Path) -> List[Dict[str, Any]]:
    return list(iter_jsonl(path))


def rewrite_jsonl(path: Path, entries: List[Dict[str, Any]]) -> None:
    """Atomically rewrite the file with the given entries."""
    ensure_file(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(json.dumps(entry, ensure_ascii=False,
                                separators=(",", ":")) + "\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TaskLoggerError(Exception):
    """Raised on schema, transition, or filter violations."""


def validate_task(entry: Dict[str, Any]) -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if missing:
        raise TaskLoggerError(f"missing required fields: {missing}")

    if entry["status"] not in VALID_STATUSES:
        raise TaskLoggerError(
            f"invalid status '{entry['status']}'. "
            f"valid: {sorted(VALID_STATUSES)}")
    if entry["priority"] not in VALID_PRIORITIES:
        raise TaskLoggerError(
            f"invalid priority '{entry['priority']}'. "
            f"valid: {sorted(VALID_PRIORITIES)}")

    task_text = (entry.get("task") or "").strip()
    if len(task_text) < 8:
        raise TaskLoggerError(
            "task description is too short (min 8 chars). "
            "filter rules: don't log basa-basi.")


def assert_transition_allowed(old: str, new: str) -> None:
    if old not in VALID_STATUSES:
        raise TaskLoggerError(f"unknown current status: {old}")
    if new not in VALID_STATUSES:
        raise TaskLoggerError(f"unknown target status: {new}")
    if old == new:
        raise TaskLoggerError(f"no-op transition: {old} -> {new}")
    if new not in ALLOWED_TRANSITIONS[old]:
        raise TaskLoggerError(
            f"illegal transition {old} -> {new}. "
            f"allowed from {old}: {sorted(ALLOWED_TRANSITIONS[old]) or 'none (terminal)'}")


# ---------------------------------------------------------------------------
# High-level operations
# ---------------------------------------------------------------------------

def create_task(*,
                company: str,
                from_: str,
                to: str,
                task: str,
                priority: str = "MEDIUM",
                context: Optional[Dict[str, Any]] = None,
                task_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task: append to inbox.jsonl + audit to logs.jsonl.
    Returns the created entry.
    """
    now = utc_now_iso()
    entry = {
        "id":         task_id or next_task_id(company),
        "company":    company,
        "from":       from_,
        "to":         to,
        "task":       task.strip(),
        "priority":   priority.upper(),
        "status":     "NEW",
        "created_at": now,
        "updated_at": now,
        "context":    context or {},
    }
    validate_task(entry)
    append_jsonl(file_path(company, "inbox"), entry)
    audit("CREATE", entry, prev_status=None, new_status="NEW")
    return entry


def update_task_status(*,
                       company: str,
                       task_id: str,
                       new_status: str,
                       note: Optional[str] = None,
                       actor: str = "MAIN") -> Dict[str, Any]:
    """
    Transition an existing task's status. Validates state machine.
    Rewrites inbox.jsonl with the updated entry; appends to logs.jsonl.
    """
    new_status = new_status.upper()
    inbox = file_path(company, "inbox")
    entries = read_all(inbox)

    target_idx = None
    for i, e in enumerate(entries):
        if e.get("id") == task_id:
            target_idx = i
            break
    if target_idx is None:
        raise TaskLoggerError(f"task {task_id} not found in {inbox}")

    target = entries[target_idx]
    old_status = target.get("status", "NEW")
    assert_transition_allowed(old_status, new_status)

    target["status"] = new_status
    target["updated_at"] = utc_now_iso()
    if note:
        ctx = target.setdefault("context", {})
        history = ctx.setdefault("history", [])
        history.append({"at": target["updated_at"],
                        "by": actor,
                        "from": old_status,
                        "to": new_status,
                        "note": note})

    entries[target_idx] = target
    rewrite_jsonl(inbox, entries)
    audit("UPDATE", target, prev_status=old_status,
          new_status=new_status, actor=actor, note=note)
    return target


def list_tasks(*,
               company: str,
               status: Optional[str] = None,
               agent: Optional[str] = None,
               priority: Optional[str] = None,
               include_terminal: bool = True) -> List[Dict[str, Any]]:
    """
    Read inbox.jsonl and apply filters. All filters are AND-combined.
    If include_terminal is False, hides DONE/CANCELLED/FAILED.
    """
    entries = read_all(file_path(company, "inbox"))

    def keep(e: Dict[str, Any]) -> bool:
        if status and e.get("status") != status.upper():
            return False
        if priority and e.get("priority") != priority.upper():
            return False
        if agent and e.get("to") != agent and e.get("from") != agent:
            return False
        if not include_terminal and e.get("status") in TERMINAL_STATUSES:
            return False
        return True

    return [e for e in entries if keep(e)]


def log_message(*,
                company: str,
                from_: str,
                to: str,
                message: str,
                ref_task: Optional[str] = None) -> Dict[str, Any]:
    """
    Append an agent-to-agent durable message to messages.jsonl.
    `ref_task` optionally links the message to a task ID.
    """
    msg_text = message.strip()
    if len(msg_text) < 4:
        raise TaskLoggerError(
            "message too short (min 4 chars). filter rules: don't log basa-basi.")
    entry = {
        "company":    company,
        "from":       from_,
        "to":         to,
        "message":    msg_text,
        "ref_task":   ref_task,
        "created_at": utc_now_iso(),
    }
    append_jsonl(file_path(company, "messages"), entry)
    return entry


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

def audit(event: str,
          task_entry: Dict[str, Any],
          *,
          prev_status: Optional[str],
          new_status: str,
          actor: str = "MAIN",
          note: Optional[str] = None) -> None:
    """Append a structured audit record to the company's logs.jsonl."""
    record = {
        "event":       event,           # CREATE | UPDATE
        "task_id":     task_entry["id"],
        "company":     task_entry["company"],
        "to":          task_entry["to"],
        "from":        task_entry["from"],
        "prev_status": prev_status,
        "new_status":  new_status,
        "actor":       actor,
        "at":          utc_now_iso(),
    }
    if note:
        record["note"] = note
    append_jsonl(file_path(task_entry["company"], "logs"), record)
