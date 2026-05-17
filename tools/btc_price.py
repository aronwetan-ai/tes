#!/usr/bin/env python3
"""
btc_price.py — Fetch current BTC price + 24h change from CoinGecko.

Usage:
    python3 tools/btc_price.py
    python3 tools/btc_price.py --currency idr
    python3 tools/btc_price.py --json

Sources:
    - CoinGecko Public API (free, no key required).
    - Endpoint: https://api.coingecko.com/api/v3/simple/price

Output (default):
    Compact human-readable summary.

Output (--json):
    Structured JSON for downstream tools / agents.

Risk: Low (read-only, public API).

Used by: @crypto.market, @crypto.risk, @crypto.report.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_ID = "bitcoin"
DEFAULT_VS = "usd"
TIMEOUT_S = 10


def fetch_price(vs_currency: str = DEFAULT_VS) -> dict:
    """Fetch BTC price from CoinGecko.

    Returns a parsed dict with keys: price, change_24h_pct, market_cap_usd,
    volume_24h_usd, last_updated_at, currency, status, source.
    On failure returns {"status":"error", "message": "..."}.
    """
    params = {
        "ids":                       COIN_ID,
        "vs_currencies":             vs_currency,
        "include_24hr_change":       "true",
        "include_24hr_vol":          "true",
        "include_market_cap":        "true",
        "include_last_updated_at":   "true",
    }
    try:
        r = requests.get(API_URL, params=params, timeout=TIMEOUT_S)
        r.raise_for_status()
        data = r.json().get(COIN_ID)
        if not data:
            return {"status": "error", "message": "no data for bitcoin"}

        price          = data.get(vs_currency)
        change_24h     = data.get(f"{vs_currency}_24h_change")
        market_cap     = data.get(f"{vs_currency}_market_cap")
        volume_24h     = data.get(f"{vs_currency}_24h_vol")
        last_updated   = data.get("last_updated_at")

        return {
            "status":            "success",
            "currency":          vs_currency.upper(),
            "price":             price,
            "change_24h_pct":    round(change_24h, 2) if change_24h is not None else None,
            "market_cap":        market_cap,
            "volume_24h":        volume_24h,
            "last_updated_at":   datetime.fromtimestamp(last_updated, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if last_updated else None,
            "fetched_at":        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source":            "CoinGecko",
        }
    except requests.RequestException as e:
        return {"status": "error", "message": f"request failed: {e}"}
    except (KeyError, ValueError) as e:
        return {"status": "error", "message": f"parse failed: {e}"}


def render_human(result: dict) -> str:
    if result["status"] != "success":
        return f"ERROR: {result.get('message', 'unknown')}"
    price = result["price"]
    chg   = result["change_24h_pct"]
    cur   = result["currency"]
    arrow = "↑" if (chg or 0) >= 0 else "↓"
    sign  = "+" if (chg or 0) >= 0 else ""
    lines = [
        f"BTC price: {price:,.2f} {cur}  {arrow} {sign}{chg}% (24h)" if chg is not None
        else f"BTC price: {price:,.2f} {cur}",
        f"Market cap: {result['market_cap']:,.0f} {cur}" if result.get("market_cap") else "",
        f"Volume 24h: {result['volume_24h']:,.0f} {cur}" if result.get("volume_24h") else "",
        f"Last updated: {result.get('last_updated_at', '?')} (source: CoinGecko)",
    ]
    return "\n".join(line for line in lines if line)


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch current BTC price from CoinGecko.")
    p.add_argument("--currency", default=DEFAULT_VS,
                   help="vs_currency (e.g. usd, idr, eur). Default: usd.")
    p.add_argument("--json", action="store_true",
                   help="Output structured JSON.")
    args = p.parse_args()

    result = fetch_price(args.currency.lower())

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_human(result))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
