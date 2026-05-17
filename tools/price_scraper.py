#!/usr/bin/env python3
"""
price_scraper.py — Multi-asset OHLCV history scraper from CoinGecko public API.

Fetches historical price + volume data for one or more crypto assets.
Output: per-asset CSV-style table or JSON; aggregated across assets in --json mode.

Tier:    Update 12 (Crypto Consultant deepening)
Risk:    Low (read-only HTTP GET to public API)
Status:  Active

Usage:
    python3 price_scraper.py --coin bitcoin
    python3 price_scraper.py --coin bitcoin --days 365 --vs usd
    python3 price_scraper.py --coin bitcoin,ethereum,solana --days 90 --json
    python3 price_scraper.py --coin bitcoin --days 30 --interval daily --output btc.csv

Notes:
- Free CoinGecko public API; no key required.
- Rate-limited: ~10-30 calls/min per IP. Sleeps between multi-coin calls.
- Days values >90 default to daily granularity (CoinGecko free tier limit).
- Output is timestamped at the time of scrape; treat as snapshot.
- Used as input for pattern_detector.py and other downstream analytics.

Exit codes:
    0   success
    1   API error (network, parse, etc.)
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.coingecko.com/api/v3"
DEFAULT_DAYS = 365
DEFAULT_VS = "usd"
DEFAULT_INTERVAL = "daily"
USER_AGENT = "ai-holding-price-scraper/1.0"
INTER_CALL_SLEEP = 1.5  # seconds between multi-coin calls (rate limit politeness)


def _http_get(url: str, timeout: float = 20.0) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} from {url}")
        body = resp.read().decode("utf-8")
    return json.loads(body)


def fetch_ohlcv(coin: str, vs: str, days: int, interval: str | None = None) -> list[dict]:
    """
    Fetch OHLCV-like data from CoinGecko market_chart endpoint.

    CoinGecko free tier returns:
      - prices: [[timestamp, price], ...]
      - market_caps: [[timestamp, market_cap], ...]
      - total_volumes: [[timestamp, volume], ...]

    We zip them by timestamp to produce a per-bar record.
    Daily granularity for days >= 90; hourly for days < 90 (auto by API).
    """
    url = f"{API_BASE}/coins/{coin}/market_chart?vs_currency={vs}&days={days}"
    if interval:
        url += f"&interval={interval}"
    raw = _http_get(url)

    prices = raw.get("prices") or []
    caps = raw.get("market_caps") or []
    vols = raw.get("total_volumes") or []

    # Index caps & vols by timestamp for join
    cap_map = {ts: v for ts, v in caps}
    vol_map = {ts: v for ts, v in vols}

    out: list[dict] = []
    for ts, price in prices:
        out.append({
            "timestamp_ms": int(ts),
            "iso_utc": datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "price": round(float(price), 4),
            "market_cap": round(float(cap_map.get(ts, 0.0)), 2),
            "volume": round(float(vol_map.get(ts, 0.0)), 2),
        })
    return out


def fetch_ohlc_candles(coin: str, vs: str, days: int) -> list[dict]:
    """
    Optional richer data via CoinGecko OHLC endpoint (returns true OHLC candles).
    Free tier limited to specific day windows: 1 / 7 / 14 / 30 / 90 / 180 / 365 / max.
    Only call when --ohlc flag set.
    """
    url = f"{API_BASE}/coins/{coin}/ohlc?vs_currency={vs}&days={days}"
    raw = _http_get(url)
    if not isinstance(raw, list):
        raise RuntimeError(f"unexpected OHLC response shape for {coin}")
    out: list[dict] = []
    for ts, o, h, l, c in raw:
        out.append({
            "timestamp_ms": int(ts),
            "iso_utc": datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "open": round(float(o), 4),
            "high": round(float(h), 4),
            "low": round(float(l), 4),
            "close": round(float(c), 4),
        })
    return out


def _to_csv(rows: list[dict], coin: str) -> str:
    if not rows:
        return ""
    # Header: union of keys, stable order
    keys = list(rows[0].keys())
    out = [",".join(keys)]
    for r in rows:
        out.append(",".join(str(r.get(k, "")) for k in keys))
    return "\n".join(out)


def _summary_stats(rows: list[dict]) -> dict:
    if not rows:
        return {}
    prices = [r.get("price") for r in rows if r.get("price") is not None]
    if not prices:
        prices = [r.get("close") for r in rows if r.get("close") is not None]
    if not prices:
        return {"bars": len(rows)}
    return {
        "bars": len(rows),
        "first_iso": rows[0].get("iso_utc"),
        "last_iso": rows[-1].get("iso_utc"),
        "first_price": prices[0],
        "last_price": prices[-1],
        "high": max(prices),
        "low": min(prices),
        "change_pct": round((prices[-1] - prices[0]) / prices[0] * 100, 2)
            if prices[0] else 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Multi-asset OHLCV history scraper from CoinGecko. "
            "See knowledge/crypto/cycle-indicators.md for downstream uses."
        )
    )
    parser.add_argument(
        "--coin", required=True,
        help="Coin id(s) per CoinGecko: bitcoin, ethereum, solana, etc. "
             "Comma-separated for multi-coin (e.g. bitcoin,ethereum).",
    )
    parser.add_argument(
        "--vs", default=DEFAULT_VS,
        help=f"Quote currency (default: {DEFAULT_VS}). Common: usd, idr, eur.",
    )
    parser.add_argument(
        "--days", type=int, default=DEFAULT_DAYS,
        help=f"Days of history (default: {DEFAULT_DAYS}; max ~365 free tier).",
    )
    parser.add_argument(
        "--interval", default=None,
        choices=[None, "daily"],
        help="Optional explicit interval; default is API-determined.",
    )
    parser.add_argument(
        "--ohlc", action="store_true",
        help="Use OHLC candle endpoint (limited day windows).",
    )
    parser.add_argument(
        "--output", default=None,
        help="Optional output file path. Format inferred from extension "
             "(.json / .csv); else CSV to stdout.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-coin status messages.")
    args = parser.parse_args(argv)

    coins = [c.strip() for c in args.coin.split(",") if c.strip()]
    if not coins:
        print("error: --coin requires at least one coin id", file=sys.stderr)
        return 2

    if args.days <= 0 or args.days > 730:
        print(f"warning: days={args.days} may exceed free tier; clamping to 365", file=sys.stderr)
        args.days = min(max(1, args.days), 365)

    results: dict[str, list[dict]] = {}
    summaries: dict[str, dict] = {}

    for i, coin in enumerate(coins):
        if not args.quiet:
            print(f"[{i+1}/{len(coins)}] fetching {coin} {args.days}d vs {args.vs}...",
                  file=sys.stderr)
        try:
            if args.ohlc:
                # Snap days to allowed values for OHLC endpoint
                allowed = [1, 7, 14, 30, 90, 180, 365]
                d = min(allowed, key=lambda x: abs(x - args.days))
                rows = fetch_ohlc_candles(coin, args.vs, d)
            else:
                rows = fetch_ohlcv(coin, args.vs, args.days, args.interval)
            results[coin] = rows
            summaries[coin] = _summary_stats(rows)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError) as e:
            print(f"error: {coin}: {e}", file=sys.stderr)
            return 1
        if i < len(coins) - 1:
            time.sleep(INTER_CALL_SLEEP)

    # Output
    if args.output:
        outpath = Path(args.output)
        if outpath.suffix == ".json":
            payload = {
                "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "vs": args.vs,
                "days": args.days,
                "coins": results,
                "summary": summaries,
            }
            outpath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        else:  # csv (default)
            chunks: list[str] = []
            for coin, rows in results.items():
                chunks.append(f"# coin={coin} vs={args.vs} days={args.days}")
                chunks.append(_to_csv(rows, coin))
                chunks.append("")
            outpath.write_text("\n".join(chunks), encoding="utf-8")
        if not args.quiet:
            print(f"wrote {outpath}", file=sys.stderr)
        return 0

    if args.json:
        payload = {
            "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "vs": args.vs,
            "days": args.days,
            "coins": results,
            "summary": summaries,
        }
        print(json.dumps(payload, indent=2))
    else:
        # Human-readable summary
        print(f"== price_scraper: {len(coins)} coin(s), {args.days}d vs {args.vs} ==")
        for coin, summary in summaries.items():
            print(f"\n[{coin}]")
            for k, v in summary.items():
                print(f"  {k}: {v}")
        print()
        if not args.quiet:
            print("(use --json or --output for full data)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
