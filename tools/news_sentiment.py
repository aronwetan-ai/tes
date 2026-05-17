#!/usr/bin/env python3
"""
news_sentiment.py — Fetch latest crypto news + simple sentiment classification.

Usage:
    python3 tools/news_sentiment.py
    python3 tools/news_sentiment.py --limit 20
    python3 tools/news_sentiment.py --json
    python3 tools/news_sentiment.py --kind=hot

Source:
    CryptoPanic Public API (free tier; no key required for public posts).
    Endpoint: https://cryptopanic.com/api/v1/posts/

Sentiment:
    Heuristic classifier — keyword + (hot/important) flags. Not a full NLP
    sentiment model. Honest about that: classification has noise; agents
    should treat output as "headline scan", not analytical truth.

Risk: Low (read-only, public API).

Used by: @crypto.research, @crypto.market, @brandflow.analytics (audience trends).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from typing import Iterable

import requests

API_URL = "https://cryptopanic.com/api/v1/posts/"
TIMEOUT_S = 12

POSITIVE_KW = {
    "surge", "rally", "soar", "bull", "breakout", "approval", "approved",
    "adoption", "partnership", "launch", "upgrade", "bullish", "rebound",
    "all-time high", "ath", "milestone", "expansion", "inflow", "buyback",
}
NEGATIVE_KW = {
    "crash", "plunge", "dump", "bear", "sell-off", "selloff", "hack",
    "exploit", "rugpull", "rug pull", "lawsuit", "ban", "fraud", "investigation",
    "bearish", "outflow", "default", "liquidat", "delist", "halt",
    "warning", "scam",
}


def classify(title: str) -> str:
    """Naive keyword-based sentiment classifier. Returns positive | negative | neutral."""
    t = title.lower()
    pos = any(kw in t for kw in POSITIVE_KW)
    neg = any(kw in t for kw in NEGATIVE_KW)
    if pos and not neg:
        return "positive"
    if neg and not pos:
        return "negative"
    return "neutral"


def fetch_news(limit: int = 10, kind: str | None = None) -> dict:
    """Fetch latest posts from CryptoPanic public feed.

    kind: optional filter — "news" / "media" / None (all).
    Returns parsed dict with status, fetched_at, summary, items.
    """
    params: dict = {"public": "true"}
    if kind:
        params["kind"] = kind
    try:
        r = requests.get(API_URL, params=params, timeout=TIMEOUT_S)
        r.raise_for_status()
        payload = r.json()
        results = payload.get("results", [])[:limit]
    except requests.RequestException as e:
        return {"status": "error", "message": f"request failed: {e}"}
    except (KeyError, ValueError) as e:
        return {"status": "error", "message": f"parse failed: {e}"}

    items = []
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for post in results:
        title = (post.get("title") or "").strip()
        if not title:
            continue
        sentiment = classify(title)
        counts[sentiment] += 1
        votes = post.get("votes") or {}
        items.append({
            "title":       title,
            "sentiment":   sentiment,
            "url":         post.get("url"),
            "published":   post.get("published_at"),
            "source":      (post.get("source") or {}).get("title"),
            "domain":      (post.get("source") or {}).get("domain"),
            "kind":        post.get("kind"),
            "votes":       {
                "important": votes.get("important", 0),
                "positive":  votes.get("positive", 0),
                "negative":  votes.get("negative", 0),
            },
        })

    total = sum(counts.values()) or 1
    summary = {
        "total":             total,
        "positive_pct":      round(counts["positive"] / total * 100, 1),
        "negative_pct":      round(counts["negative"] / total * 100, 1),
        "neutral_pct":       round(counts["neutral"]  / total * 100, 1),
        "skew":              "positive" if counts["positive"] > counts["negative"]
                             else ("negative" if counts["negative"] > counts["positive"]
                                   else "balanced"),
    }
    return {
        "status":     "success",
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source":     "CryptoPanic (public feed, free tier)",
        "summary":    summary,
        "items":      items,
        "disclaimer": "Sentiment is keyword-based, not full NLP. Treat as headline scan.",
    }


def render_human(result: dict) -> str:
    if result["status"] != "success":
        return f"ERROR: {result.get('message', 'unknown')}"
    s = result["summary"]
    out = [
        f"News sentiment scan — {result['fetched_at']}",
        f"Source: {result['source']}",
        f"Items: {s['total']}  |  +{s['positive_pct']}%  -{s['negative_pct']}%  ={s['neutral_pct']}%  →  skew: {s['skew']}",
        "",
    ]
    for it in result["items"]:
        marker = {"positive": "+", "negative": "-", "neutral": "·"}[it["sentiment"]]
        out.append(f"  {marker} [{it['source'] or '?'}] {it['title']}")
    out.append("")
    out.append(f"Note: {result['disclaimer']}")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch latest crypto news + sentiment classification.")
    p.add_argument("--limit", type=int, default=10,
                   help="Number of headlines to fetch (default 10).")
    p.add_argument("--kind", default=None, choices=("news", "media"),
                   help="Filter by post kind (CryptoPanic).")
    p.add_argument("--json", action="store_true",
                   help="Output structured JSON.")
    args = p.parse_args()

    if args.limit < 1 or args.limit > 100:
        print("ERROR: --limit must be 1..100", file=sys.stderr)
        return 2

    result = fetch_news(limit=args.limit, kind=args.kind)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_human(result))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
