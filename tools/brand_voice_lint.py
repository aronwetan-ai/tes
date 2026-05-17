#!/usr/bin/env python3
"""
brand_voice_lint.py — Voice-drift scoring against a locked brand voice profile.

Loads a voice profile YAML/JSON (per `knowledge/marketing/brand-voice-rubric.md`)
and scores a draft for drift on:

  - Vocabulary "do use" coverage (does the draft reach for in-profile words?)
  - Vocabulary "don't use" violations (does the draft contain banned words?)
  - Sentence-length pattern match
  - POV match (first-person plural / singular / brand voice)
  - Emoji policy compliance
  - Punctuation quirks compliance (em-dash, ALL CAPS, exclamation count)
  - Off-limits topics scan (substring match)

Outputs:
  - Drift score (0-100; lower = more on-brand)
  - Per-dimension issues
  - Suggested fixes per violation

Tier:    Update 11 (BrandFlow deepening)
Risk:    Low (read-only)
Status:  Active

Profile format (YAML or JSON; JSON is default if `yaml` is unavailable):

    {
      "client": "acme",
      "vocab_do":  ["teman", "founder", "framework"],
      "vocab_dont": ["guys", "literally", "hustle"],
      "pov":       "first_person_plural",
      "sentence_length_pattern": "mixed_short_medium",
      "emoji_policy": "sparingly",
      "max_emoji_per_post": 1,
      "punctuation": {
        "em_dash": "preferred",
        "all_caps": "single_word_only",
        "max_exclamation": 1
      },
      "off_limits_topics": ["politics", "religion"]
    }

Usage:
    python3 brand_voice_lint.py --profile voice.json --draft draft.txt
    python3 brand_voice_lint.py --profile voice.json --stdin
    python3 brand_voice_lint.py --profile voice.json --draft draft.txt --json

Exit codes:
    0   no major drift (score < 30)
    1   drift detected (score >= 30)
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000027BF"
    "]+",
    flags=re.UNICODE,
)

ALL_CAPS_RUN = re.compile(r"\b[A-Z]{2,}(?:\s+[A-Z]{2,}){1,}\b")
ALL_CAPS_SINGLE = re.compile(r"\b[A-Z]{2,}\b")
EXCL_COUNT = re.compile(r"!")
EM_DASH = re.compile(r"—")
SENT_SPLIT = re.compile(r"(?<=[\.\!\?])\s+|\n{2,}")
WORD_SPLIT = re.compile(r"\b[\w']+\b", re.UNICODE)


# ---------------------------------------------------------------------------
# Profile loading (JSON or YAML if available)
# ---------------------------------------------------------------------------

def load_profile(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    # Try JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try YAML if present
    try:
        import yaml  # type: ignore
        loaded = yaml.safe_load(text)
        if isinstance(loaded, dict):
            return loaded
    except ImportError:
        pass
    raise ValueError(
        f"profile {path}: not valid JSON; install pyyaml to use YAML profiles."
    )


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def _lint_vocab(text: str, profile: dict) -> list[dict]:
    issues: list[dict] = []
    lower = text.lower()
    do_words = [w.lower() for w in profile.get("vocab_do", [])]
    dont_words = [w.lower() for w in profile.get("vocab_dont", [])]

    do_hits = sum(1 for w in do_words if re.search(rf"\b{re.escape(w)}\b", lower))
    do_target = max(1, len(do_words) // 5)  # expect ~20% reach
    if do_words and do_hits == 0:
        issues.append({
            "severity": "warn",
            "dim": "vocab_do",
            "msg": (
                f"draft uses 0 of {len(do_words)} 'do-use' words; "
                f"voice may be drifting away from profile."
            ),
            "suggestion": (
                f"Reach for some of: {', '.join(do_words[:8])}..."
            ),
        })
    elif do_words and do_hits < do_target:
        issues.append({
            "severity": "minor",
            "dim": "vocab_do",
            "msg": (
                f"draft uses only {do_hits}/{len(do_words)} 'do-use' words "
                f"(target: ~{do_target}+)."
            ),
        })

    for w in dont_words:
        for m in re.finditer(rf"\b{re.escape(w)}\b", lower):
            issues.append({
                "severity": "blocker",
                "dim": "vocab_dont",
                "msg": f"banned word in profile: '{w}' at offset {m.start()}.",
                "suggestion": "remove or replace per voice profile.",
            })
            break  # one report per banned word
    return issues


def _lint_pov(text: str, profile: dict) -> list[dict]:
    pov = profile.get("pov")
    if not pov:
        return []
    fp_plural = len(re.findall(r"\b(we|our|us|kami|kita)\b", text, re.I))
    fp_singular = len(re.findall(r"\b(i|i'm|my|me|saya|aku)\b", text, re.I))
    issues: list[dict] = []

    if pov == "first_person_plural" and fp_singular > fp_plural:
        issues.append({
            "severity": "warn",
            "dim": "pov",
            "msg": (
                f"profile POV is plural ('we / kami') but draft skews singular "
                f"({fp_singular} vs {fp_plural}). Adjust."
            ),
        })
    if pov == "first_person_singular" and fp_plural > fp_singular:
        issues.append({
            "severity": "warn",
            "dim": "pov",
            "msg": (
                f"profile POV is singular ('I / saya') but draft skews plural "
                f"({fp_plural} vs {fp_singular}). Adjust."
            ),
        })
    if pov == "brand_voice" and (fp_plural + fp_singular) > 0:
        issues.append({
            "severity": "minor",
            "dim": "pov",
            "msg": (
                f"profile POV is brand voice but draft uses first-person "
                f"({fp_plural + fp_singular} occurrences)."
            ),
        })
    return issues


def _lint_emoji(text: str, profile: dict) -> list[dict]:
    policy = profile.get("emoji_policy", "any")
    max_per_post = int(profile.get("max_emoji_per_post", 0) or 0)
    n_emoji = sum(len(m.group(0)) for m in EMOJI_RE.finditer(text))
    issues: list[dict] = []
    if policy == "none" and n_emoji > 0:
        issues.append({
            "severity": "blocker",
            "dim": "emoji",
            "msg": f"profile bans emoji; draft contains {n_emoji}.",
        })
    elif policy == "sparingly" and max_per_post and n_emoji > max_per_post:
        issues.append({
            "severity": "warn",
            "dim": "emoji",
            "msg": (
                f"profile allows up to {max_per_post} emoji 'sparingly'; "
                f"draft contains {n_emoji}."
            ),
        })
    return issues


def _lint_punctuation(text: str, profile: dict) -> list[dict]:
    issues: list[dict] = []
    p = profile.get("punctuation", {}) or {}

    # ALL CAPS
    all_caps_setting = p.get("all_caps", "any")
    runs = ALL_CAPS_RUN.findall(text)
    if all_caps_setting == "no" and (runs or ALL_CAPS_SINGLE.findall(text)):
        issues.append({
            "severity": "warn",
            "dim": "punctuation",
            "msg": "profile bans ALL CAPS; found ALL CAPS in draft.",
        })
    elif all_caps_setting == "single_word_only" and runs:
        issues.append({
            "severity": "warn",
            "dim": "punctuation",
            "msg": (
                f"profile permits single-word ALL CAPS only; "
                f"draft has multi-word ALL CAPS run(s): {runs[:3]}."
            ),
        })

    # Exclamation count
    max_excl = p.get("max_exclamation")
    if isinstance(max_excl, int):
        n_excl = len(EXCL_COUNT.findall(text))
        if n_excl > max_excl:
            issues.append({
                "severity": "minor",
                "dim": "punctuation",
                "msg": (
                    f"profile caps exclamation at {max_excl} per post; "
                    f"draft has {n_excl}."
                ),
            })

    # Em-dash
    em_setting = p.get("em_dash", "any")
    n_em = len(EM_DASH.findall(text))
    if em_setting == "no" and n_em > 0:
        issues.append({
            "severity": "minor",
            "dim": "punctuation",
            "msg": f"profile bans em-dash (—); draft contains {n_em}.",
        })

    return issues


def _lint_off_limits(text: str, profile: dict) -> list[dict]:
    issues: list[dict] = []
    topics = [t.lower() for t in (profile.get("off_limits_topics") or [])]
    lower = text.lower()
    for t in topics:
        if t in lower:
            issues.append({
                "severity": "blocker",
                "dim": "off_limits",
                "msg": f"off-limits topic in draft: '{t}'.",
            })
    return issues


def _lint_sentence_length(text: str, profile: dict) -> list[dict]:
    pattern = profile.get("sentence_length_pattern")
    if not pattern:
        return []
    sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    if not sents:
        return []
    sent_lens = [len(WORD_SPLIT.findall(s)) for s in sents]
    avg = sum(sent_lens) / len(sent_lens)
    short_ratio = sum(1 for n in sent_lens if n <= 8) / len(sent_lens)
    issues: list[dict] = []
    if pattern == "mostly_short" and avg > 12:
        issues.append({
            "severity": "minor",
            "dim": "sentence_length",
            "msg": (
                f"profile expects mostly-short sentences; draft avg "
                f"sentence length {avg:.1f} words."
            ),
        })
    if pattern == "mixed_short_medium" and short_ratio < 0.2:
        issues.append({
            "severity": "minor",
            "dim": "sentence_length",
            "msg": (
                f"profile expects mixed rhythm with short sentences; draft "
                f"has only {short_ratio*100:.0f}% short sentences."
            ),
        })
    if pattern == "long" and avg < 15:
        issues.append({
            "severity": "minor",
            "dim": "sentence_length",
            "msg": (
                f"profile expects long sentences; draft avg "
                f"{avg:.1f} words."
            ),
        })
    return issues


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------

SEVERITY_WEIGHT = {
    "blocker": 25,
    "warn": 8,
    "minor": 3,
}


def compute_score(issues: list[dict]) -> int:
    """0 = perfect, 100 = severely off-brand."""
    score = 0
    for i in issues:
        score += SEVERITY_WEIGHT.get(i.get("severity"), 0)
    return min(100, score)


# ---------------------------------------------------------------------------
# Lint orchestration
# ---------------------------------------------------------------------------

def lint(text: str, profile: dict) -> dict:
    issues: list[dict] = []
    issues.extend(_lint_vocab(text, profile))
    issues.extend(_lint_pov(text, profile))
    issues.extend(_lint_emoji(text, profile))
    issues.extend(_lint_punctuation(text, profile))
    issues.extend(_lint_off_limits(text, profile))
    issues.extend(_lint_sentence_length(text, profile))

    score = compute_score(issues)
    return {
        "client": profile.get("client", "<unknown>"),
        "score": score,
        "verdict": (
            "on-brand" if score < 15
            else "minor-drift" if score < 30
            else "drifted" if score < 60
            else "severe-drift"
        ),
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_human(result: dict, draft_label: str = "draft") -> str:
    lines = [f"== brand-voice-lint: {draft_label} ==",
             f"client: {result['client']}",
             f"score: {result['score']} ({result['verdict']})"]
    if not result["issues"]:
        lines.append("issues: none — voice on-brand")
    else:
        lines.append("issues:")
        for i in result["issues"]:
            sug = f"  → {i['suggestion']}" if i.get("suggestion") else ""
            lines.append(f"  [{i['severity']}] {i['dim']}: {i['msg']}{sug}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint a draft against a locked brand voice profile. "
            "See knowledge/marketing/brand-voice-rubric.md for profile schema."
        )
    )
    parser.add_argument(
        "--profile", required=True,
        help="Path to brand voice profile (.json or .yaml/.yml).",
    )
    parser.add_argument(
        "--draft", default=None,
        help="Path to draft file. Use --stdin instead to read stdin.",
    )
    parser.add_argument("--stdin", action="store_true", help="Read draft from stdin.")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument(
        "--threshold",
        type=int,
        default=30,
        help="Score threshold for non-zero exit (default: 30).",
    )
    args = parser.parse_args(argv)

    try:
        profile = load_profile(args.profile)
    except (OSError, ValueError) as e:
        print(f"error: profile load failed: {e}", file=sys.stderr)
        return 2

    if args.stdin:
        text = sys.stdin.read()
        draft_label = "<stdin>"
    elif args.draft:
        try:
            text = Path(args.draft).read_text(encoding="utf-8")
        except OSError as e:
            print(f"error: cannot read draft {args.draft}: {e}", file=sys.stderr)
            return 2
        draft_label = args.draft
    else:
        print("error: provide --draft FILE or --stdin", file=sys.stderr)
        return 2

    result = lint(text, profile)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_human(result, draft_label))

    return 1 if result["score"] >= args.threshold else 0


if __name__ == "__main__":
    raise SystemExit(main())
