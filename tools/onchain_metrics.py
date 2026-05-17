#!/usr/bin/env python3
"""
onchain_metrics.py — Public on-chain metric aggregator (free APIs only).

Pulls from public endpoints:
  - blockchain.info / blockchain.com (BTC hashrate, difficulty, blockchain stats)
  - mempool.space (BTC mempool, fees, recent blocks)
  - DefiLlama (TVL across protocols and chains)

Tier:    Update 12 (Crypto Consultant deepening)
Risk:    Low (read-only HTTP GET to public APIs)
Status:  Active

Usage:
    python3 onchain_metrics.py --metric hashrate
    python3 onchain_metrics.py --metric mempool
    python3 onchain_metrics.py --metric tvl --protocol aave
    python3 onchain_metrics.py --metric tvl --chain ethereum
    python3 onchain_metrics.py --metric all --json

Metrics supported:
    hashrate      BTC network hashrate + difficulty (blockchain.info)
    mempool       BTC mempool size, fee rates (mempool.space)
    blockchain    BTC blockchain summary (blockchain.info /stats)
    tvl           DeFi TVL (DefiLlama; --protocol or --chain optional)
    stablecoin    Stablecoin total supply (DefiLlama)
    all           Run all metrics

Notes:
- Free APIs only. Paid sources (Glassnode, Nansen) NOT covered here — they
  require subscriptions and are out of scope for this tool.
- Whale-level / cohort-level metrics are NOT available without paid data.
  See knowledge/crypto/onchain-metrics-glossary.md for what's possible
  with free vs paid sources.
- Used by `@crypto.onchain` for network-health and DeFi reads.

Exit codes:
    0   success
    1   network / parse error
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER_AGENT = "ai-holding-onchain-metrics/1.0"
TIMEOUT = 15.0


def _http_get_json(url: str, timeout: float = TIMEOUT) -> dict | list:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} from {url}")
        body = resp.read().decode("utf-8")
    return json.loads(body)


# --------------------------------------------------------------------------
# Bitcoin network metrics
# --------------------------------------------------------------------------

def fetch_btc_hashrate() -> dict:
    """
    BTC hashrate + difficulty from blockchain.info.

    Endpoints:
      https://blockchain.info/q/hashrate           hashrate in GH/s
      https://blockchain.info/q/getdifficulty      current difficulty
      https://blockchain.info/q/totalbc            circulating supply (sat * 1e8)
    """
    base = "https://blockchain.info"
    try:
        hr_ghs_text = _http_get_text_raw(f"{base}/q/hashrate")
        diff_text = _http_get_text_raw(f"{base}/q/getdifficulty")
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
        raise RuntimeError(f"blockchain.info fetch failed: {e}")

    hr_ghs = float(hr_ghs_text.strip())
    difficulty = float(diff_text.strip())
    hr_ehs = hr_ghs / 1e9  # GH/s → EH/s

    return {
        "metric": "hashrate",
        "source": "blockchain.info",
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": {
            "hashrate_GHs": round(hr_ghs, 2),
            "hashrate_EHs": round(hr_ehs, 2),
            "difficulty": round(difficulty, 2),
        },
        "interpretation_hint": (
            "Rising hashrate + difficulty = miner confidence. "
            "ATH = healthy network. Significant drops (>15% / 30d) = "
            "miner capitulation (often near cycle bottoms)."
        ),
    }


def fetch_btc_mempool() -> dict:
    """
    BTC mempool from mempool.space.

    Endpoints:
      https://mempool.space/api/mempool                summary stats
      https://mempool.space/api/v1/fees/recommended    recommended fee rates
    """
    try:
        summary = _http_get_json("https://mempool.space/api/mempool")
        fees = _http_get_json("https://mempool.space/api/v1/fees/recommended")
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
        raise RuntimeError(f"mempool.space fetch failed: {e}")

    return {
        "metric": "mempool",
        "source": "mempool.space",
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": {
            "mempool_count": summary.get("count"),
            "mempool_vsize": summary.get("vsize"),
            "mempool_total_fee_BTC": (summary.get("total_fee", 0) / 1e8) if summary.get("total_fee") else None,
            "fees_satoshi_per_vbyte": {
                "fastest": fees.get("fastestFee"),
                "halfHour": fees.get("halfHourFee"),
                "hour": fees.get("hourFee"),
                "economy": fees.get("economyFee"),
                "minimum": fees.get("minimumFee"),
            },
        },
        "interpretation_hint": (
            "High mempool + high fees = network demand strong (bullish for "
            "fee revenue post-halving). Low mempool sustained = waning demand."
        ),
    }


def fetch_btc_blockchain_stats() -> dict:
    """Bitcoin blockchain.info /stats endpoint."""
    try:
        stats = _http_get_json("https://blockchain.info/stats")
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
        raise RuntimeError(f"blockchain.info stats fetch failed: {e}")
    return {
        "metric": "blockchain",
        "source": "blockchain.info /stats",
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": {
            "n_blocks_total": stats.get("n_blocks_total"),
            "n_btc_mined": stats.get("n_btc_mined"),
            "totalbc": (stats.get("totalbc") / 1e8) if stats.get("totalbc") else None,
            "market_price_usd": stats.get("market_price_usd"),
            "hash_rate_GHs": stats.get("hash_rate"),
            "difficulty": stats.get("difficulty"),
            "minutes_between_blocks": stats.get("minutes_between_blocks"),
            "mempool_size": stats.get("mempool_size"),
            "n_btc_mined_24h": stats.get("n_btc_mined"),
            "trade_volume_btc_24h": stats.get("trade_volume_btc"),
        },
    }


# --------------------------------------------------------------------------
# DeFi TVL (DefiLlama)
# --------------------------------------------------------------------------

def fetch_tvl(protocol: str | None = None, chain: str | None = None) -> dict:
    """
    DeFi TVL from DefiLlama.

    No args: total cross-chain TVL (https://api.llama.fi/v2/historicalChainTvl)
    --protocol <slug>: per-protocol TVL (https://api.llama.fi/protocol/<slug>)
    --chain <name>: per-chain TVL (https://api.llama.fi/v2/historicalChainTvl/<chain>)
    """
    base = "https://api.llama.fi"

    if protocol:
        url = f"{base}/protocol/{protocol}"
        try:
            data = _http_get_json(url)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
            raise RuntimeError(f"DefiLlama protocol fetch failed: {e}")
        latest_tvl = None
        if "tvl" in data and isinstance(data["tvl"], list) and data["tvl"]:
            latest_tvl = data["tvl"][-1].get("totalLiquidityUSD")
        return {
            "metric": "tvl",
            "scope": "protocol",
            "protocol": protocol,
            "source": "DefiLlama",
            "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "value": {
                "name": data.get("name"),
                "symbol": data.get("symbol"),
                "category": data.get("category"),
                "chains": data.get("chains"),
                "tvl_usd": latest_tvl,
            },
        }

    if chain:
        url = f"{base}/v2/historicalChainTvl/{chain}"
        try:
            data = _http_get_json(url)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
            raise RuntimeError(f"DefiLlama chain fetch failed: {e}")
        latest_tvl = data[-1].get("tvl") if data else None
        latest_date = data[-1].get("date") if data else None
        return {
            "metric": "tvl",
            "scope": "chain",
            "chain": chain,
            "source": "DefiLlama",
            "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "value": {
                "tvl_usd_latest": latest_tvl,
                "as_of_unix": latest_date,
                "history_points": len(data) if isinstance(data, list) else 0,
            },
        }

    # Total cross-chain TVL
    url = f"{base}/v2/historicalChainTvl"
    try:
        data = _http_get_json(url)
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
        raise RuntimeError(f"DefiLlama total TVL fetch failed: {e}")
    latest_tvl = data[-1].get("tvl") if data else None
    latest_date = data[-1].get("date") if data else None
    return {
        "metric": "tvl",
        "scope": "total",
        "source": "DefiLlama",
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": {
            "tvl_usd_total": latest_tvl,
            "as_of_unix": latest_date,
            "history_points": len(data) if isinstance(data, list) else 0,
        },
    }


def fetch_stablecoins() -> dict:
    """Stablecoin total market cap from DefiLlama."""
    url = "https://stablecoins.llama.fi/stablecoins?includePrices=false"
    try:
        data = _http_get_json(url)
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
        raise RuntimeError(f"DefiLlama stablecoins fetch failed: {e}")

    coins = data.get("peggedAssets", []) if isinstance(data, dict) else []
    summary: list[dict] = []
    total_circulating = 0.0
    for c in coins[:10]:  # top 10 by listing order
        name = c.get("name")
        circ = c.get("circulating", {})
        # Sum across pegs (typically USD)
        circ_usd = sum(v for v in circ.values() if isinstance(v, (int, float)))
        summary.append({
            "name": name,
            "symbol": c.get("symbol"),
            "circulating_usd": round(circ_usd, 2),
            "chains": c.get("chains", [])[:5],
        })
        total_circulating += circ_usd

    return {
        "metric": "stablecoin",
        "source": "DefiLlama stablecoins",
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": {
            "top_10": summary,
            "top_10_total_circulating_usd": round(total_circulating, 2),
        },
        "interpretation_hint": (
            "Stablecoin growth = dry powder accumulating. "
            "Stablecoin contraction = capital exiting crypto via redemption. "
            "Sustained 7-14d trend matters; daily noise is noise."
        ),
    }


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _http_get_text_raw(url: str, timeout: float = TIMEOUT) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} from {url}")
        return resp.read().decode("utf-8", errors="replace")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

METRIC_DISPATCH = {
    "hashrate":   lambda args: fetch_btc_hashrate(),
    "mempool":    lambda args: fetch_btc_mempool(),
    "blockchain": lambda args: fetch_btc_blockchain_stats(),
    "tvl":        lambda args: fetch_tvl(args.protocol, args.chain),
    "stablecoin": lambda args: fetch_stablecoins(),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Public on-chain metric aggregator (BTC network + DeFi TVL). "
            "See knowledge/crypto/onchain-metrics-glossary.md for usage."
        )
    )
    parser.add_argument(
        "--metric", required=True,
        choices=list(METRIC_DISPATCH.keys()) + ["all"],
        help="Metric to fetch (or 'all').",
    )
    parser.add_argument("--protocol", default=None,
                        help="DefiLlama protocol slug (for --metric tvl).")
    parser.add_argument("--chain", default=None,
                        help="DefiLlama chain name (for --metric tvl).")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--quiet", action="store_true", help="Suppress narrative.")
    args = parser.parse_args(argv)

    metrics_to_run = (
        list(METRIC_DISPATCH.keys()) if args.metric == "all" else [args.metric]
    )

    results: dict = {
        "scanned_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metrics": {},
    }

    for m in metrics_to_run:
        if not args.quiet:
            print(f"fetching {m}...", file=sys.stderr)
        try:
            r = METRIC_DISPATCH[m](args)
            results["metrics"][m] = r
        except RuntimeError as e:
            print(f"warning: {m}: {e}", file=sys.stderr)
            results["metrics"][m] = {"metric": m, "status": "ERROR", "error": str(e)}

    results["disclaimer"] = (
        "Free public APIs only. Whale-level / cohort metrics require paid data "
        "(Glassnode, Nansen) — see skills/onchain/whale-tracking-playbook.md "
        "and knowledge/crypto/onchain-metrics-glossary.md."
    )

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"== onchain_metrics: {len(metrics_to_run)} metric(s) ==")
        for m, r in results["metrics"].items():
            print(f"\n[{m}] source: {r.get('source', 'n/a')}")
            if r.get("status") == "ERROR":
                print(f"  ERROR: {r.get('error')}")
                continue
            val = r.get("value", {})
            if isinstance(val, dict):
                for k, v in val.items():
                    if isinstance(v, dict):
                        print(f"  {k}:")
                        for kk, vv in v.items():
                            print(f"    {kk}: {vv}")
                    elif isinstance(v, list):
                        print(f"  {k}: [{len(v)} items]")
                    else:
                        print(f"  {k}: {v}")
            if r.get("interpretation_hint"):
                print(f"  hint: {r['interpretation_hint']}")
        print()
        if not args.quiet:
            print(f"NOTE: {results['disclaimer']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
