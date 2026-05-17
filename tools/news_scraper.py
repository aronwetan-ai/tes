#!/usr/bin/env python3
"""
news_scraper.py — Multi-source crypto news aggregator with keyword filter + sentiment.

Pulls public RSS feeds from major crypto news outlets, normalizes them,
applies optional keyword filter, runs naive keyword-based sentiment classifier.

Sources covered (default set):
  - CoinDesk           https://www.coindesk.com/arc/outboundfeeds/rss
  - CoinTelegraph      https://cointelegraph.com/rss
  - Decrypt            https://decrypt.co/feed
  - The Block          https://www.theblock.co/rss.xml
  - Bitcoin Magazine   https://bitcoinmagazine.com/.rss/full

Tier:    Update 12 (Crypto Consultant deepening)
Risk:    Low (read-only HTTP GET to public RSS)
Status:  Active

Usage:
    python3 news_scraper.py
    python3 news_scraper.py --limit 30
    python3 news_scraper.py --keyword "bitcoin,etf,sec" --since 2026-05-15
    python3 news_scraper.py --json --quiet

Notes:
- Sentiment is **keyword-based heuristic, directional only**, not full NLP.
- Output explicitly disclaims this. Treat as headline scan, not analytical truth.
- News tier rating per knowledge/crypto/news-source-rubric.md: outputs are T4
  (crypto media) — citable for news, NOT for analysis.
- Used by `@crypto.research` for narrative scan; never as primary fact source.

Exit codes:
    0   success
    1   network / parse error
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

USER_AGENT = "ai-holding-news-scraper/1.0"
TIMEOUT = 15.0

DEFAULT_FEEDS: dict[str, str] = {
    "coindesk":         "https://www.coindesk.com/arc/outboundfeeds/rss",
    "cointelegraph":    "https://cointelegraph.com/rss",
    "decrypt":          "https://decrypt.co/feed",
    "theblock":         "https://www.theblock.co/rss.xml",
    "bitcoinmagazine":  "https://bitcoinmagazine.com/.rss/full",
}

POSITIVE_WORDS = {
    "rally", "surge", "soar", "breakout", "uptrend", "all-time high", "ath",
    "bullish", "buy", "accumulation", "adoption", "approve", "approval",
    "launch", "milestone", "growth", "expand", "partnership", "integration",
    "naik", "tembus", "rally", "bullish", "tertinggi",
}

NEGATIVE_WORDS = {
    "crash", "plunge", "tumble", "collapse", "bearish", "sell-off", "selloff",
    "liquidation", "hack", "exploit", "stolen", "lawsuit", "ban", "fraud",
    "scam", "rug", "rug pull", "drop", "decline", "warning", "risk", "fear",
    "panic", "fud", "regulation crackdown", "indicted", "charged",
    "anjlok", "longsor", "jatuh", "panik", "scam", "tipu", "bobol", "diretas",
    "diserang",
}

CRITICAL_INDICATORS = {
    "lawsuit", "indicted", "charged", "fraud", "ponzi", "exploit",
    "stolen", "sec enforcement", "doj indictment",
    "lapor polisi", "tindak hukum", "tuntut", "boikot",
}


def _http_get_text(url: str, timeout: float = TIMEOUT) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} from {url}")
        return resp.read().decode("utf-8", errors="replace")


# Simple regex-based RSS / Atom parser (stdlib only, avoids xml.etree pitfalls
# with mixed namespaces). Sufficient for headline + summary + date extraction.
RSS_ITEM_RE = re.compile(r"<item\b[^>]*>(.*?)</item>", re.DOTALL | re.IGNORECASE)
ATOM_ENTRY_RE = re.compile(r"<entry\b[^>]*>(.*?)</entry>", re.DOTALL | re.IGNORECASE)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.DOTALL | re.IGNORECASE)
LINK_RSS_RE = re.compile(r"<link\b[^>]*>(.*?)</link>", re.DOTALL | re.IGNORECASE)
LINK_ATOM_RE = re.compile(r"<link\b[^>]*href=[\"']([^\"']+)[\"']", re.IGNORECASE)
DESC_RE = re.compile(
    r"<(?:description|summary|content)\b[^>]*>(.*?)</(?:description|summary|content)>",
    re.DOTALL | re.IGNORECASE,
)
PUBDATE_RE = re.compile(
    r"<(?:pubDate|published|updated|dc:date)\b[^>]*>(.*?)</(?:pubDate|published|updated|dc:date)>",
    re.DOTALL | re.IGNORECASE,
)
TAG_STRIP_RE = re.compile(r"<[^>]+>")
CDATA_RE = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.DOTALL)


def _clean(text: str) -> str:
    if not text:
        return ""
    # Pull out CDATA contents
    m = CDATA_RE.search(text)
    if m:
        text = m.group(1)
    text = TAG_STRIP_RE.sub("", text)
    text = html.unescape(text)
    return text.strip()


def _parse_date(s: str) -> datetime | None:
    s = s.strip()
    if not s:
        return None
    # Try RFC 2822 (RSS standard)
    try:
        d = parsedate_to_datetime(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except (TypeError, ValueError):
        pass
    # Try ISO 8601 (Atom)
    try:
        # Strip trailing Z, replace with +00:00
        t = s.replace("Z", "+00:00")
        d = datetime.fromisoformat(t)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except ValueError:
        return None


def parse_feed(source: str, xml_text: str) -> list[dict]:
    items: list[dict] = []

    # Try RSS items first; if none, try Atom entries
    item_blocks = RSS_ITEM_RE.findall(xml_text)
    is_atom = False
    if not item_blocks:
        item_blocks = ATOM_ENTRY_RE.findall(xml_text)
        is_atom = True

    for block in item_blocks:
        title_m = TITLE_RE.search(block)
        title = _clean(title_m.group(1)) if title_m else ""

        if is_atom:
            link_m = LINK_ATOM_RE.search(block)
            link = link_m.group(1).strip() if link_m else ""
        else:
            link_m = LINK_RSS_RE.search(block)
            link = _clean(link_m.group(1)) if link_m else ""

        desc_m = DESC_RE.search(block)
        desc = _clean(desc_m.group(1)) if desc_m else ""

        pubdate_m = PUBDATE_RE.search(block)
        pubdate_raw = _clean(pubdate_m.group(1)) if pubdate_m else ""
        pubdate = _parse_date(pubdate_raw)

        if not title:
            continue

        items.append({
            "source": source,
            "title": title,
            "link": link,
            "summary": desc[:500],  # cap summary
            "published_iso": pubdate.strftime("%Y-%m-%dT%H:%M:%SZ") if pubdate else None,
            "published_raw": pubdate_raw,
        })
    return items


def classify_sentiment(text: str) -> tuple[str, list[str]]:
    """Returns (sentiment, triggers). Heuristic, directional only."""
    lower = text.lower()
    crit_hits = [w for w in CRITICAL_INDICATORS if w in lower]
    pos_hits = [w for w in POSITIVE_WORDS if w in lower]
    neg_hits = [w for w in NEGATIVE_WORDS if w in lower]

    if crit_hits:
        return "critical", crit_hits[:3]
    if neg_hits and (len(neg_hits) > len(pos_hits)):
        return "negative", neg_hits[:3]
    if pos_hits and (len(pos_hits) > len(neg_hits)):
        return "positive", pos_hits[:3]
    return "neutral", []


def filter_by_keywords(items: list[dict], keywords: list[str]) -> list[dict]:
    if not keywords:
        return items
    lower_kws = [k.lower().strip() for k in keywords if k.strip()]
    out: list[dict] = []
    for it in items:
        haystack = (it.get("title", "") + " " + it.get("summary", "")).lower()
        if any(k in haystack for k in lower_kws):
            out.append(it)
    return out


def filter_by_since(items: list[dict], since_iso: str | None) -> list[dict]:
    if not since_iso:
        return items
    try:
        cutoff = datetime.fromisoformat(since_iso).replace(tzinfo=timezone.utc) \
            if "T" not in since_iso \
            else datetime.fromisoformat(since_iso.replace("Z", "+00:00"))
        if cutoff.tzinfo is None:
            cutoff = cutoff.replace(tzinfo=timezone.utc)
    except ValueError:
        print(f"warning: cannot parse --since '{since_iso}', skipping filter", file=sys.stderr)
        return items
    out: list[dict] = []
    for it in items:
        if not it.get("published_iso"):
            continue
        d = datetime.fromisoformat(it["published_iso"].replace("Z", "+00:00"))
        if d >= cutoff:
            out.append(it)
    return out


def aggregate_sentiment(items: list[dict]) -> dict:
    counts: dict[str, int] = {"positive": 0, "neutral": 0, "negative": 0, "critical": 0}
    for it in items:
        s = it.get("sentiment", "neutral")
        counts[s] = counts.get(s, 0) + 1
    total = sum(counts.values())
    pct = {k: round(100 * v / total, 1) if total else 0.0 for k, v in counts.items()}
    return {"counts": counts, "pct": pct, "total": total}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Crypto news multi-source aggregator with keyword filter + sentiment. "
            "See knowledge/crypto/news-source-rubric.md for citation tier guidance."
        )
    )
    parser.add_argument(
        "--source", default=None,
        help="Comma-separated source slugs (default: all). "
             f"Available: {','.join(DEFAULT_FEEDS.keys())}",
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Max items per source (default: 20). 0 = all available.",
    )
    parser.add_argument(
        "--keyword", default=None,
        help="Comma-separated keywords; OR-match in title or summary.",
    )
    parser.add_argument(
        "--since", default=None,
        help="ISO date or datetime cutoff (e.g. 2026-05-15 or 2026-05-15T00:00:00Z).",
    )
    parser.add_argument(
        "--sentiment-only", default=None,
        choices=["positive", "neutral", "negative", "critical"],
        help="Filter to one sentiment class only.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-source status.")
    args = parser.parse_args(argv)

    sources = (
        [s.strip() for s in args.source.split(",") if s.strip()]
        if args.source else list(DEFAULT_FEEDS.keys())
    )
    bad = [s for s in sources if s not in DEFAULT_FEEDS]
    if bad:
        print(f"error: unknown source(s) {bad}. Available: {list(DEFAULT_FEEDS.keys())}",
              file=sys.stderr)
        return 2

    keywords = [k.strip() for k in (args.keyword or "").split(",") if k.strip()]

    all_items: list[dict] = []

    for src in sources:
        url = DEFAULT_FEEDS[src]
        if not args.quiet:
            print(f"fetching {src}...", file=sys.stderr)
        try:
            xml_text = _http_get_text(url)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
            print(f"warning: {src}: {e}", file=sys.stderr)
            continue
        try:
            items = parse_feed(src, xml_text)
        except (ValueError, RuntimeError) as e:
            print(f"warning: {src} parse error: {e}", file=sys.stderr)
            continue

        if args.limit and args.limit > 0:
            items = items[: args.limit]
        all_items.extend(items)

    # Apply filters
    all_items = filter_by_since(all_items, args.since)
    all_items = filter_by_keywords(all_items, keywords)

    # Sentiment classification
    for it in all_items:
        text = (it.get("title", "") + " " + it.get("summary", ""))
        sent, triggers = classify_sentiment(text)
        it["sentiment"] = sent
        it["sentiment_triggers"] = triggers

    if args.sentiment_only:
        all_items = [it for it in all_items if it.get("sentiment") == args.sentiment_only]

    # Sort by published descending where available, else preserve order
    def _sort_key(it: dict) -> str:
        return it.get("published_iso") or ""
    all_items.sort(key=_sort_key, reverse=True)

    summary = aggregate_sentiment(all_items)
    summary["sources_used"] = sources
    summary["scraped_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary["disclaimer"] = (
        "Sentiment is keyword-based heuristic, directional only. "
        "Treat as headline scan, not analytical truth. "
        "News sources are tier T4 (crypto media) per "
        "knowledge/crypto/news-source-rubric.md — citable for news, "
        "not for primary analytical claims."
    )

    if args.json:
        print(json.dumps({"summary": summary, "items": all_items},
                         ensure_ascii=False, indent=2))
        return 0

    # Human-readable
    print(f"== news_scraper: {summary['total']} items from "
          f"{len(sources)} source(s) ==")
    print(f"sources: {', '.join(sources)}")
    print(f"sentiment: pos={summary['counts']['positive']} ({summary['pct']['positive']}%) "
          f"neu={summary['counts']['neutral']} ({summary['pct']['neutral']}%) "
          f"neg={summary['counts']['negative']} ({summary['pct']['negative']}%) "
          f"crit={summary['counts']['critical']} ({summary['pct']['critical']}%)")
    print()
    for it in all_items[:50]:  # cap human-readable display
        marker = {"positive": "+", "neutral": " ", "negative": "-",
                  "critical": "!"}.get(it.get("sentiment", "neutral"), " ")
        date = it.get("published_iso") or it.get("published_raw") or "—"
        print(f"  [{marker}] {date}  [{it['source']}]  {it['title'][:90]}")
    if len(all_items) > 50:
        print(f"\n  ... and {len(all_items) - 50} more (use --json for full)")
    print()
    print(f"NOTE: {summary['disclaimer']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
