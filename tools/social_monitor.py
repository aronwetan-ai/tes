#!/usr/bin/env python3
"""
social_monitor.py — Sentiment + cluster + spread scan for BrandFlow's community manager.

Operates on a JSONL stream of mention/comment events (from native API exports
or scraped/copied input). Runs:

  - Naive keyword-based sentiment classification (positive/neutral/negative)
  - Volume aggregation per period
  - Cluster detection (similar phrases / repeated themes)
  - Spread velocity (volume change vs prior periods)
  - Crisis-tier suggestion (T1 / T2 / T3 / T4) with rationale

Sentiment heuristic is **directional only** — not a substitute for human review
(see knowledge/marketing/crisis-comms-playbook.md).

Tier:    Update 11 (BrandFlow deepening)
Risk:    Low (read-only stdin/file)
Status:  Active

Input format (JSONL, one event per line):

    {
      "id": "...",
      "platform": "instagram",
      "type": "mention | comment | dm | reply",
      "from_handle": "@user",
      "from_followers": 1234,
      "content": "...",
      "received_at": "2026-05-17T10:14:22Z",
      "thread_id": "...",        (optional)
      "url": "..."               (optional)
    }

Usage:
    python3 social_monitor.py --input mentions.jsonl
    python3 social_monitor.py --input mentions.jsonl --client acme --json
    python3 social_monitor.py --stdin --period-hours 24 --json

Exit codes:
    0   no crisis signal
    1   crisis signal present (T2+)
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Sentiment lexicon (Indonesian + English; keyword heuristic; directional only)
# ---------------------------------------------------------------------------

POSITIVE_WORDS = {
    # English
    "great", "amazing", "love", "loved", "loving", "awesome", "fantastic",
    "best", "helpful", "useful", "thank", "thanks", "thx", "appreciate",
    "good", "excellent", "brilliant", "perfect", "happy", "cool",
    "saved", "shared", "recommend",
    # Indonesian
    "bagus", "keren", "mantap", "mantul", "suka", "love banget", "thanks",
    "makasih", "terimakasih", "terima kasih", "membantu", "berguna",
    "rekomen", "rekomendasi", "best", "puas", "setuju", "ngena",
    "relate", "wow", "kepake", "manfaat",
}

NEGATIVE_WORDS = {
    # English
    "bad", "worst", "terrible", "awful", "horrible", "hate", "scam",
    "fraud", "fake", "lie", "lied", "broken", "doesn't work", "doesnt work",
    "useless", "waste", "refund", "complaint", "complain", "angry", "upset",
    "disappointed", "ripoff", "rip off", "overpriced",
    # Indonesian
    "jelek", "buruk", "sampah", "rugi", "scam", "penipu", "penipuan", "bohong",
    "kecewa", "marah", "kesal", "kesel", "ga guna", "gak guna", "ga jelas",
    "gak jelas", "ribet", "lambat", "telat", "complaint", "komplain",
    "refund", "balikin", "tipu", "menyesal", "menyesatkan", "halu",
}

CRITICAL_INDICATORS = {
    "lawsuit", "legal", "lawyer", "court", "police", "report",
    "tuntut", "lapor polisi", "pengacara", "hukum", "tindak hukum",
    "boycott", "boikot", "fraud", "penipuan",
    "exposed", "thread berbahaya", "viral",
}

INFLUENCER_FOLLOWER_THRESHOLD = 10_000
JOURNALIST_KEYWORDS = {
    "journalist", "wartawan", "reporter", "redaksi", "editor",
    "press", "pers", "@kumparan", "@detikcom", "@cnbcindonesia",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WORD_SPLIT = re.compile(r"\b[\w']+\b", re.UNICODE)


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _parse_iso(s: str) -> datetime:
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return _now()


def _classify_sentiment(text: str) -> tuple[str, list[str]]:
    """Returns ('positive' | 'neutral' | 'negative' | 'critical', triggers)."""
    lower = text.lower()
    pos_hits = [w for w in POSITIVE_WORDS if w in lower]
    neg_hits = [w for w in NEGATIVE_WORDS if w in lower]
    crit_hits = [w for w in CRITICAL_INDICATORS if w in lower]

    if crit_hits:
        return "critical", crit_hits
    if neg_hits and (len(neg_hits) > len(pos_hits)):
        return "negative", neg_hits
    if pos_hits and (len(pos_hits) > len(neg_hits)):
        return "positive", pos_hits
    return "neutral", []


def _normalize_phrase(text: str) -> str:
    """For cluster detection — reduce to bag-of-words signature."""
    words = [w.lower() for w in WORD_SPLIT.findall(text)]
    # Drop very short / very common stopwords (Indonesian + English)
    stop = {
        "a", "an", "the", "to", "of", "is", "are", "and", "or", "but",
        "in", "on", "at", "for", "with", "yang", "ini", "itu", "dan",
        "atau", "tapi", "di", "ke", "dari", "sama", "saya", "aku", "kami",
    }
    sig = [w for w in words if w not in stop and len(w) >= 3]
    return " ".join(sorted(sig[:8]))


# ---------------------------------------------------------------------------
# Tier suggestion logic
# ---------------------------------------------------------------------------

def suggest_tier(stats: dict) -> tuple[str, list[str]]:
    """
    Returns (tier_label, reasoning_list).
    Tier vocabulary matches knowledge/marketing/crisis-comms-playbook.md.
    """
    reasons: list[str] = []
    tier = "T1"

    total = stats["total"]
    sentiment_neg_pct = stats["sentiment_pct"].get("negative", 0)
    sentiment_crit_pct = stats["sentiment_pct"].get("critical", 0)
    cluster_size = stats["largest_cluster_size"]
    has_journalist = stats["has_journalist_signal"]
    has_influencer = stats["has_influencer_signal"]
    has_critical = stats["sentiment_count"].get("critical", 0) > 0

    # Crisis (T4) overrides
    if has_journalist:
        reasons.append("journalist / press keyword detected in incoming")
        tier = "T4"
    if has_critical:
        reasons.append(
            "critical-language indicator present "
            "(legal / lawsuit / boycott / fraud)"
        )
        if tier != "T4":
            tier = "T4"

    # Alert (T3)
    if tier in ("T1", "T2"):
        if has_influencer and sentiment_neg_pct > 30:
            reasons.append(
                f"influencer signal + negative sentiment {sentiment_neg_pct:.0f}%"
            )
            tier = "T3"
        elif sentiment_neg_pct > 50 and total >= 10:
            reasons.append(
                f"sentiment majority negative {sentiment_neg_pct:.0f}% "
                f"with volume {total}"
            )
            tier = "T3"

    # Concern (T2)
    if tier == "T1":
        if cluster_size >= 3:
            reasons.append(f"cluster of {cluster_size}+ similar complaints forming")
            tier = "T2"
        elif sentiment_neg_pct > 30 and total >= 5:
            reasons.append(
                f"sentiment shifting: {sentiment_neg_pct:.0f}% negative on {total} mentions"
            )
            tier = "T2"

    if not reasons:
        reasons.append("baseline; monitor")

    return tier, reasons


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate(events: list[dict], period_hours: int) -> dict:
    cutoff = _now() - timedelta(hours=period_hours)

    in_window = []
    for e in events:
        ts = _parse_iso(e.get("received_at", ""))
        if ts >= cutoff:
            in_window.append(e)

    sentiment_count: Counter = Counter()
    cluster_signatures: Counter = Counter()
    has_journalist_signal = False
    has_influencer_signal = False
    examples: dict[str, list[dict]] = {}

    for e in in_window:
        content = e.get("content", "") or ""
        sent, triggers = _classify_sentiment(content)
        sentiment_count[sent] += 1
        examples.setdefault(sent, []).append({
            "id": e.get("id"),
            "from": e.get("from_handle"),
            "platform": e.get("platform"),
            "preview": content[:120],
            "triggers": triggers[:5],
        })

        sig = _normalize_phrase(content)
        if sig:
            cluster_signatures[sig] += 1

        followers = int(e.get("from_followers") or 0)
        if followers >= INFLUENCER_FOLLOWER_THRESHOLD:
            has_influencer_signal = True

        handle = (e.get("from_handle") or "").lower()
        if any(j in content.lower() or j in handle for j in JOURNALIST_KEYWORDS):
            has_journalist_signal = True

    total = sum(sentiment_count.values())
    sentiment_pct = {
        k: round(100 * v / total, 1) if total else 0.0
        for k, v in sentiment_count.items()
    }
    largest_cluster = cluster_signatures.most_common(1)
    largest_cluster_size = largest_cluster[0][1] if largest_cluster else 0
    largest_cluster_phrase = largest_cluster[0][0] if largest_cluster else ""

    stats = {
        "period_hours": period_hours,
        "total": total,
        "sentiment_count": dict(sentiment_count),
        "sentiment_pct": sentiment_pct,
        "largest_cluster_size": largest_cluster_size,
        "largest_cluster_phrase": largest_cluster_phrase,
        "top_clusters": cluster_signatures.most_common(5),
        "has_influencer_signal": has_influencer_signal,
        "has_journalist_signal": has_journalist_signal,
        "examples": {
            k: v[:5] for k, v in examples.items()  # cap examples per bucket
        },
    }

    tier, reasons = suggest_tier(stats)
    stats["tier"] = tier
    stats["tier_reasons"] = reasons
    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_human(stats: dict, client: str | None) -> str:
    lines: list[str] = []
    label = f" client={client}" if client else ""
    lines.append(f"== social-monitor scan{label} ==")
    lines.append(
        f"period={stats['period_hours']}h  total_events={stats['total']}"
    )
    if stats["total"]:
        sc = stats["sentiment_count"]
        sp = stats["sentiment_pct"]
        lines.append(
            f"sentiment: pos={sc.get('positive',0)} ({sp.get('positive',0)}%)  "
            f"neu={sc.get('neutral',0)} ({sp.get('neutral',0)}%)  "
            f"neg={sc.get('negative',0)} ({sp.get('negative',0)}%)  "
            f"crit={sc.get('critical',0)} ({sp.get('critical',0)}%)"
        )
    lines.append(
        f"clusters: largest={stats['largest_cluster_size']} "
        f"phrase={stats['largest_cluster_phrase']!r}"
    )
    if stats["top_clusters"]:
        lines.append("top clusters:")
        for phrase, n in stats["top_clusters"]:
            lines.append(f"  {n:3d}  {phrase!r}")
    lines.append(
        f"signals: influencer={stats['has_influencer_signal']}  "
        f"journalist={stats['has_journalist_signal']}"
    )
    lines.append(f"crisis-tier: {stats['tier']}")
    for r in stats["tier_reasons"]:
        lines.append(f"  · {r}")
    if stats["tier"] in ("T2", "T3", "T4"):
        lines.append("")
        lines.append(
            "→ See knowledge/marketing/crisis-comms-playbook.md for tier response."
        )
        lines.append(
            "→ Operational steps: companies/brandflow/skills/community/crisis-playbook.md"
        )
    lines.append("")
    lines.append(
        "note: sentiment classification is directional keyword heuristic, "
        "not authoritative. Always pair with human review."
    )
    return "\n".join(lines)


def _read_events(path_or_none: str | None, use_stdin: bool) -> list[dict]:
    if use_stdin:
        text = sys.stdin.read()
    elif path_or_none:
        text = Path(path_or_none).read_text(encoding="utf-8")
    else:
        raise ValueError("provide --input FILE or --stdin")
    events: list[dict] = []
    for line_num, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"line {line_num}: invalid JSON: {e}") from e
    return events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Sentiment + cluster + spread scan with crisis-tier suggestion. "
            "See knowledge/marketing/crisis-comms-playbook.md."
        )
    )
    parser.add_argument(
        "--input", default=None,
        help="Path to JSONL file with mention events.",
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="Read JSONL events from stdin.",
    )
    parser.add_argument(
        "--period-hours",
        type=int,
        default=24,
        help="Window in hours for the scan (default: 24).",
    )
    parser.add_argument(
        "--client", default=None,
        help="Client label for report (informational only).",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output JSON instead of human-readable.",
    )
    args = parser.parse_args(argv)

    try:
        events = _read_events(args.input, args.stdin)
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    stats = aggregate(events, args.period_hours)

    if args.json:
        out = dict(stats)
        if args.client:
            out["client"] = args.client
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(_format_human(stats, args.client))

    return 1 if stats["tier"] in ("T2", "T3", "T4") else 0


if __name__ == "__main__":
    raise SystemExit(main())
