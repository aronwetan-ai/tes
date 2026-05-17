#!/usr/bin/env python3
"""
funding_rates.py — Perpetual futures funding rate + open interest from public exchange APIs.

Pulls from public endpoints (no key required):
  - Binance Futures        https://fapi.binance.com
  - Bybit                  https://api.bybit.com

Returns current funding rate, open interest, and recent funding history
for a given symbol pair (default BTCUSDT).

Tier:    Update 12 (Crypto Consultant deepening)
Risk:    Low (read-only HTTP GET to public APIs; no positions, no orders)
Status:  Active

Usage:
    python3 funding_rates.py
    python3 funding_rates.py --symbol BTCUSDT
    python3 funding_rates.py --symbol ETHUSDT --limit 30 --json
    python3 funding_rates.py --symbol BTCUSDT --include-oi --json
    python3 funding_rates.py --exchanges binance,bybit --symbol BTCUSDT

Notes:
- Binance / Bybit perp funding paid every 8 hours typically.
- Default symbol: BTCUSDT. Use --symbol for ETHUSDT, SOLUSDT, etc.
- --limit controls history depth (default 30 funding intervals = ~10 days).
- Funding rate interpretation per knowledge/crypto/derivatives-glossary.md.
- Used by `@crypto.market` for derivatives lens; `@crypto.research` for
  3-lens convergence reads.

Exit codes:
    0   success
    1   API error
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

USER_AGENT = "ai-holding-funding-rates/1.0"
TIMEOUT = 15.0


def _http_get_json(url: str, timeout: float = TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} from {url}")
        body = resp.read().decode("utf-8")
    return json.loads(body)


# --------------------------------------------------------------------------
# Binance
# --------------------------------------------------------------------------

def fetch_binance_funding(symbol: str, limit: int = 30) -> dict:
    """
    Binance USD-M futures premium history.
    Endpoint: /fapi/v1/fundingRate?symbol=...&limit=...
    """
    url = ("https://fapi.binance.com/fapi/v1/fundingRate"
           f"?symbol={urllib.parse.quote(symbol)}&limit={limit}")
    rows = _http_get_json(url)

    if not isinstance(rows, list):
        raise RuntimeError(f"unexpected Binance response: {rows}")

    history = []
    rates_pct = []
    for r in rows:
        rate = float(r.get("fundingRate", 0))
        rates_pct.append(rate * 100)
        history.append({
            "fundingTime_iso": datetime.fromtimestamp(
                r["fundingTime"] / 1000, tz=timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fundingRate": rate,
            "fundingRate_pct": round(rate * 100, 5),
        })

    # Latest premium index (current expected funding)
    try:
        prem = _http_get_json(
            f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={urllib.parse.quote(symbol)}"
        )
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError):
        prem = None

    summary = {
        "exchange": "binance",
        "symbol": symbol,
        "history_count": len(history),
        "latest_funding_rate_pct": history[-1]["fundingRate_pct"] if history else None,
        "latest_funding_time": history[-1]["fundingTime_iso"] if history else None,
        "mean_funding_rate_pct": round(statistics.mean(rates_pct), 5) if rates_pct else None,
        "max_funding_rate_pct": round(max(rates_pct), 5) if rates_pct else None,
        "min_funding_rate_pct": round(min(rates_pct), 5) if rates_pct else None,
    }
    if prem and isinstance(prem, dict):
        summary["live_mark_price"] = float(prem.get("markPrice", 0))
        summary["live_index_price"] = float(prem.get("indexPrice", 0))
        summary["live_last_funding_rate_pct"] = round(float(prem.get("lastFundingRate", 0)) * 100, 5)
        summary["next_funding_time_iso"] = (
            datetime.fromtimestamp(prem["nextFundingTime"] / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ") if prem.get("nextFundingTime") else None
        )

    return {
        "summary": summary,
        "history": history,
    }


def fetch_binance_oi(symbol: str) -> dict:
    """
    Binance open interest snapshot.
    Endpoint: /fapi/v1/openInterest
    """
    url = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={urllib.parse.quote(symbol)}"
    data = _http_get_json(url)
    return {
        "exchange": "binance",
        "symbol": symbol,
        "open_interest_contracts": float(data.get("openInterest", 0)),
        "snapshot_time_iso": datetime.fromtimestamp(
            data["time"] / 1000, tz=timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ") if data.get("time") else None,
    }


# --------------------------------------------------------------------------
# Bybit
# --------------------------------------------------------------------------

def fetch_bybit_funding(symbol: str, limit: int = 30) -> dict:
    """
    Bybit linear perp funding history.
    Endpoint: /v5/market/funding/history?category=linear&symbol=...
    """
    url = ("https://api.bybit.com/v5/market/funding/history"
           f"?category=linear&symbol={urllib.parse.quote(symbol)}&limit={limit}")
    raw = _http_get_json(url)

    rows = []
    if isinstance(raw, dict) and raw.get("retCode") == 0:
        rows = raw.get("result", {}).get("list", []) or []

    history = []
    rates_pct = []
    for r in rows:
        rate = float(r.get("fundingRate", 0))
        rates_pct.append(rate * 100)
        ts_ms = int(r.get("fundingRateTimestamp", 0))
        history.append({
            "fundingTime_iso": datetime.fromtimestamp(
                ts_ms / 1000, tz=timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ") if ts_ms else None,
            "fundingRate": rate,
            "fundingRate_pct": round(rate * 100, 5),
        })

    # Bybit returns most-recent first; reverse for chronological
    history.reverse()
    rates_pct.reverse()

    summary = {
        "exchange": "bybit",
        "symbol": symbol,
        "history_count": len(history),
        "latest_funding_rate_pct": history[-1]["fundingRate_pct"] if history else None,
        "latest_funding_time": history[-1]["fundingTime_iso"] if history else None,
        "mean_funding_rate_pct": round(statistics.mean(rates_pct), 5) if rates_pct else None,
        "max_funding_rate_pct": round(max(rates_pct), 5) if rates_pct else None,
        "min_funding_rate_pct": round(min(rates_pct), 5) if rates_pct else None,
    }

    return {
        "summary": summary,
        "history": history,
    }


def fetch_bybit_oi(symbol: str, interval: str = "1h") -> dict:
    """
    Bybit open interest history (latest snapshot from history endpoint).
    Endpoint: /v5/market/open-interest?category=linear&symbol=...&intervalTime=1h&limit=1
    """
    url = ("https://api.bybit.com/v5/market/open-interest"
           f"?category=linear&symbol={urllib.parse.quote(symbol)}"
           f"&intervalTime={interval}&limit=1")
    raw = _http_get_json(url)
    rows = []
    if isinstance(raw, dict) and raw.get("retCode") == 0:
        rows = raw.get("result", {}).get("list", []) or []
    if not rows:
        return {"exchange": "bybit", "symbol": symbol, "open_interest_contracts": None}
    r = rows[0]
    return {
        "exchange": "bybit",
        "symbol": symbol,
        "open_interest_contracts": float(r.get("openInterest", 0)),
        "snapshot_time_iso": datetime.fromtimestamp(
            int(r.get("timestamp", 0)) / 1000, tz=timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ") if r.get("timestamp") else None,
    }


# --------------------------------------------------------------------------
# Interpretation helper
# --------------------------------------------------------------------------

def funding_zone_label(rate_pct_8h: float | None) -> str:
    """
    Maps Binance-style 8h funding to the zones in
    knowledge/crypto/derivatives-glossary.md.
    """
    if rate_pct_8h is None:
        return "unknown"
    if rate_pct_8h < -0.05:
        return "extreme_negative_short_squeeze_risk"
    if rate_pct_8h < 0:
        return "mild_bear_positioning"
    if rate_pct_8h < 0.01:
        return "neutral"
    if rate_pct_8h < 0.05:
        return "mild_bull_positioning"
    if rate_pct_8h < 0.1:
        return "bull_leaning"
    return "extreme_positive_long_flush_risk"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Perp funding rate + OI from Binance/Bybit. "
            "See knowledge/crypto/derivatives-glossary.md for interpretation."
        )
    )
    parser.add_argument(
        "--symbol", default="BTCUSDT",
        help="Perp symbol (default: BTCUSDT). Common: ETHUSDT, SOLUSDT.",
    )
    parser.add_argument(
        "--exchanges", default="binance,bybit",
        help="Comma-separated exchanges (default: binance,bybit).",
    )
    parser.add_argument(
        "--limit", type=int, default=30,
        help="History depth in funding intervals (default 30 ≈ 10 days).",
    )
    parser.add_argument(
        "--include-oi", action="store_true",
        help="Also fetch open interest snapshot from each exchange.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--quiet", action="store_true", help="Suppress narrative.")
    args = parser.parse_args(argv)

    exchanges = [e.strip().lower() for e in args.exchanges.split(",") if e.strip()]
    bad = [e for e in exchanges if e not in {"binance", "bybit"}]
    if bad:
        print(f"error: unknown exchange(s) {bad}. Available: binance, bybit",
              file=sys.stderr)
        return 2

    results: dict = {
        "scanned_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbol": args.symbol,
        "exchanges": {},
    }

    overall_error = False
    for exch in exchanges:
        if not args.quiet:
            print(f"fetching {exch} funding for {args.symbol}...", file=sys.stderr)
        try:
            if exch == "binance":
                f = fetch_binance_funding(args.symbol, args.limit)
                if args.include_oi:
                    try:
                        f["open_interest"] = fetch_binance_oi(args.symbol)
                    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
                        f["open_interest_error"] = str(e)
            else:  # bybit
                f = fetch_bybit_funding(args.symbol, args.limit)
                if args.include_oi:
                    try:
                        f["open_interest"] = fetch_bybit_oi(args.symbol)
                    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
                        f["open_interest_error"] = str(e)

            # Annotate zone label
            latest = f.get("summary", {}).get("latest_funding_rate_pct")
            f["summary"]["zone"] = funding_zone_label(latest)
            results["exchanges"][exch] = f
        except (urllib.error.URLError, urllib.error.HTTPError,
                RuntimeError, ValueError) as e:
            print(f"warning: {exch}: {e}", file=sys.stderr)
            results["exchanges"][exch] = {"status": "ERROR", "error": str(e)}
            overall_error = True

    results["disclaimer"] = (
        "Funding rate interpretation per knowledge/crypto/derivatives-glossary.md. "
        "Single-exchange reads are partial; senior reads aggregate or note exchange. "
        "Sustained extremes ≠ immediate reversal — combine with other lenses."
    )

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"== funding_rates: {args.symbol} on {len(exchanges)} exchange(s) ==")
        for exch, r in results["exchanges"].items():
            print(f"\n[{exch}]")
            if r.get("status") == "ERROR":
                print(f"  ERROR: {r.get('error')}")
                continue
            s = r.get("summary", {})
            print(f"  symbol:                    {s.get('symbol')}")
            print(f"  latest_funding_rate_pct:   {s.get('latest_funding_rate_pct')}  "
                  f"(zone: {s.get('zone')})")
            print(f"  latest_funding_time:       {s.get('latest_funding_time')}")
            print(f"  history_count:             {s.get('history_count')}")
            print(f"  mean_funding_rate_pct:     {s.get('mean_funding_rate_pct')}")
            print(f"  max_funding_rate_pct:      {s.get('max_funding_rate_pct')}")
            print(f"  min_funding_rate_pct:      {s.get('min_funding_rate_pct')}")
            if s.get("live_mark_price"):
                print(f"  live_mark_price:           {s.get('live_mark_price')}")
            if s.get("live_index_price"):
                print(f"  live_index_price:          {s.get('live_index_price')}")
            if s.get("next_funding_time_iso"):
                print(f"  next_funding_time:         {s.get('next_funding_time_iso')}")
            if r.get("open_interest"):
                oi = r["open_interest"]
                print(f"  open_interest_contracts:   {oi.get('open_interest_contracts')}")
        print()
        if not args.quiet:
            print(f"NOTE: {results['disclaimer']}")

    return 1 if overall_error and not results["exchanges"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
