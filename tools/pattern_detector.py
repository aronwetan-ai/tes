#!/usr/bin/env python3
"""
pattern_detector.py — Cycle / structural pattern detection over OHLCV time series.

Patterns supported:
  pi_top          Pi cycle top: 111-DMA crosses above 350-DMA × 2
  btc_bottom      Price within X% of 200W moving average (cycle bottom zone)
  mayer_low       Mayer Multiple <0.7 (deep accumulation)
  mayer_high      Mayer Multiple >2.4 (distribution / cycle top zone)
  golden_cross    50DMA crosses above 200DMA (mid-cycle bull confirmation)
  death_cross     50DMA crosses below 200DMA (bear regime confirmation)
  mvrv_zone       Approximate MVRV-Z zone (proxy: price/200D MA z-score)
  cycle_phase     Aggregate read of cycle phase (1-5) from multiple signals
  all             Run all patterns; report which are firing

Tier:    Update 12 (Crypto Consultant deepening)
Risk:    Low (read-only; consumes price_scraper.py output)
Status:  Active

Input format: JSON from price_scraper.py --json, OR CSV with columns
              "timestamp_ms,iso_utc,price,..." or
              "timestamp_ms,iso_utc,open,high,low,close".

Usage:
    python3 price_scraper.py --coin bitcoin --days 365 --json --output btc.json --quiet
    python3 pattern_detector.py --input btc.json --pattern pi_top
    python3 pattern_detector.py --input btc.json --pattern all --json
    python3 pattern_detector.py --input btc.json --pattern cycle_phase

Output: per-pattern read with current state, threshold, firing/not, base rate.

CRITICAL DISCIPLINE (per knowledge/crypto/cycle-indicators.md):
- Patterns are PROBABILISTIC, not deterministic.
- Sample sizes for crypto patterns are small (N=3-4 cycles); base rates are descriptive.
- This tool DETECTS patterns; interpretation requires senior analyst (`@crypto.market`,
  `@crypto.research`, `skills/pattern-recognition`).
- No buy/sell calls. Pattern firing = signal to investigate, not directive to act.

Exit codes:
    0   success (any state)
    1   pattern critical zone reached AND --fail-on-fire set
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PATTERNS_AVAILABLE = (
    "pi_top",
    "btc_bottom",
    "mayer_low",
    "mayer_high",
    "golden_cross",
    "death_cross",
    "mvrv_zone",
    "cycle_phase",
    "all",
)


# --------------------------------------------------------------------------
# Input parsing
# --------------------------------------------------------------------------

def load_series(path: str) -> tuple[list[float], list[str], dict]:
    """Returns (prices, iso_dates, metadata)."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"input file not found: {path}")
    text = p.read_text(encoding="utf-8")
    if path.endswith(".json"):
        return _load_json(text)
    return _load_csv(text)


def _load_json(text: str) -> tuple[list[float], list[str], dict]:
    raw = json.loads(text)
    # Format from price_scraper.py: { coins: { coin: [rows] } } OR direct list
    if isinstance(raw, list):
        rows = raw
        coin = "unknown"
    elif "coins" in raw:
        # Pick first coin if multi-coin file
        coins = raw["coins"]
        coin = next(iter(coins))
        rows = coins[coin]
    else:
        raise ValueError("JSON does not match expected price_scraper.py output schema")

    prices: list[float] = []
    dates: list[str] = []
    for r in rows:
        # price_scraper market_chart format
        if "price" in r:
            prices.append(float(r["price"]))
        # OHLC format
        elif "close" in r:
            prices.append(float(r["close"]))
        else:
            continue
        dates.append(r.get("iso_utc", ""))

    metadata = {"coin": coin, "input_format": "json", "bars": len(prices)}
    return prices, dates, metadata


def _load_csv(text: str) -> tuple[list[float], list[str], dict]:
    reader = csv.DictReader(text.splitlines())
    prices: list[float] = []
    dates: list[str] = []
    for row in reader:
        if row.get("price"):
            prices.append(float(row["price"]))
        elif row.get("close"):
            prices.append(float(row["close"]))
        else:
            continue
        dates.append(row.get("iso_utc", ""))
    return prices, dates, {"coin": "unknown", "input_format": "csv", "bars": len(prices)}


# --------------------------------------------------------------------------
# Statistical helpers
# --------------------------------------------------------------------------

def sma(values: list[float], window: int) -> list[float | None]:
    """Simple moving average; returns None for indices < window-1."""
    n = len(values)
    out: list[float | None] = [None] * n
    if window <= 0 or window > n:
        return out
    cumsum = 0.0
    for i in range(n):
        cumsum += values[i]
        if i >= window:
            cumsum -= values[i - window]
        if i >= window - 1:
            out[i] = cumsum / window
    return out


def stdev_window(values: list[float], window: int) -> list[float | None]:
    n = len(values)
    out: list[float | None] = [None] * n
    if window <= 0 or window > n:
        return out
    for i in range(window - 1, n):
        slice_ = values[i - window + 1: i + 1]
        mean = sum(slice_) / window
        var = sum((x - mean) ** 2 for x in slice_) / window
        out[i] = math.sqrt(var)
    return out


# --------------------------------------------------------------------------
# Pattern detectors
# --------------------------------------------------------------------------

def detect_pi_top(prices: list[float], dates: list[str]) -> dict:
    """Pi cycle top: 111-DMA crosses ABOVE 350-DMA × 2."""
    if len(prices) < 350:
        return _insufficient("pi_top", 350, len(prices))
    ma111 = sma(prices, 111)
    ma350 = sma(prices, 350)
    last_idx = len(prices) - 1
    ma111_now = ma111[last_idx]
    ma350_now = ma350[last_idx]
    if ma111_now is None or ma350_now is None:
        return _insufficient("pi_top", 350, len(prices))
    threshold = 2 * ma350_now
    distance_pct = (threshold - ma111_now) / threshold * 100 if threshold else 0
    fired_now = ma111_now >= threshold

    # Check for crossover in last 30 bars (recently fired)
    recent_fire_idx: int | None = None
    for i in range(max(350, last_idx - 30), last_idx + 1):
        if (
            ma111[i] is not None and ma350[i] is not None
            and ma111[i - 1] is not None and ma350[i - 1] is not None
        ):
            if ma111[i] >= 2 * ma350[i] and ma111[i - 1] < 2 * ma350[i - 1]:
                recent_fire_idx = i
                break

    return {
        "pattern": "pi_top",
        "name": "Pi Cycle Top Indicator",
        "current_value": {
            "ma111": round(ma111_now, 2),
            "ma350x2": round(threshold, 2),
            "distance_pct": round(distance_pct, 2),
        },
        "firing_now": fired_now,
        "recent_fire": {
            "fired_in_last_30_bars": recent_fire_idx is not None,
            "fire_date": dates[recent_fire_idx] if recent_fire_idx is not None else None,
        },
        "current_date": dates[last_idx] if last_idx < len(dates) else None,
        "base_rate": {
            "sample_size": 3,
            "historical_fires": [
                {"date": "2013-04-09", "btc_price": 230, "cycle_top_within_days": 1},
                {"date": "2017-12-17", "btc_price": 19300, "cycle_top_within_days": 0},
                {"date": "2021-04-12", "btc_price": 63300, "cycle_top_within_days": 2},
            ],
            "hit_rate_within_3_days": 1.00,
            "note": "Statistically NOT significant. Directional only.",
        },
        "invalidation": "Pi cycle has fired AND price continues markup for >30 days.",
        "tier": "B (moderate, small sample)",
        "reference": "knowledge/crypto/cycle-indicators.md",
    }


def detect_btc_bottom(prices: list[float], dates: list[str], pct_threshold: float = 30.0) -> dict:
    """200W (~1400 day) moving average bottom proximity."""
    needed = 1400
    if len(prices) < needed:
        return _insufficient("btc_bottom", needed, len(prices),
                             note="200W MA pattern needs ~3.8 years of daily data; "
                                  "scrape with --days 365 won't suffice")
    ma200w = sma(prices, needed)
    last = len(prices) - 1
    ma_now = ma200w[last]
    price_now = prices[last]
    if ma_now is None:
        return _insufficient("btc_bottom", needed, len(prices))
    distance_pct = (price_now - ma_now) / ma_now * 100
    in_zone = abs(distance_pct) < pct_threshold
    return {
        "pattern": "btc_bottom",
        "name": "200-Week MA Bottom Zone",
        "current_value": {
            "price": round(price_now, 2),
            "ma200w": round(ma_now, 2),
            "distance_pct": round(distance_pct, 2),
            "threshold_pct": pct_threshold,
        },
        "in_bottom_zone": in_zone and distance_pct < 0,  # below 200W
        "current_date": dates[last] if last < len(dates) else None,
        "base_rate": {
            "sample_size": 3,
            "note": "Every BTC cycle bottom touched or came within ~30% of 200W MA.",
        },
        "tier": "A (strong)",
        "reference": "knowledge/crypto/cycle-indicators.md",
    }


def detect_mayer(prices: list[float], dates: list[str]) -> dict:
    """Mayer Multiple = price / 200D MA."""
    if len(prices) < 200:
        return _insufficient("mayer", 200, len(prices))
    ma200 = sma(prices, 200)
    last = len(prices) - 1
    ma_now = ma200[last]
    price_now = prices[last]
    if ma_now is None or ma_now == 0:
        return _insufficient("mayer", 200, len(prices))
    multiple = price_now / ma_now

    if multiple < 0.7:
        zone = "deep_accumulation"
    elif multiple < 1.0:
        zone = "accumulation"
    elif multiple < 1.5:
        zone = "fair_value"
    elif multiple < 2.0:
        zone = "premium"
    elif multiple < 2.4:
        zone = "elevated"
    else:
        zone = "distribution_top"

    return {
        "pattern": "mayer",
        "name": "Mayer Multiple",
        "current_value": {
            "price": round(price_now, 2),
            "ma200": round(ma_now, 2),
            "mayer_multiple": round(multiple, 3),
        },
        "zone": zone,
        "low_zone": multiple < 0.7,    # cycle bottom zone
        "high_zone": multiple > 2.4,   # cycle top zone
        "current_date": dates[last] if last < len(dates) else None,
        "base_rate": {
            "note": "Mayer <0.7 has occurred at every BTC cycle bottom (N=3).",
            "note_high": "Mayer >2.4 has coincided with every BTC cycle top (N=3).",
        },
        "tier": "A (strong as zones)",
        "reference": "knowledge/crypto/cycle-indicators.md",
    }


def detect_cross(prices: list[float], dates: list[str]) -> dict:
    """Golden cross / death cross: 50DMA vs 200DMA."""
    if len(prices) < 200:
        return _insufficient("cross", 200, len(prices))
    ma50 = sma(prices, 50)
    ma200 = sma(prices, 200)
    last = len(prices) - 1
    if ma50[last] is None or ma200[last] is None:
        return _insufficient("cross", 200, len(prices))
    above = ma50[last] > ma200[last]
    # Look back 30 bars for cross event
    cross_event = None
    cross_date = None
    for i in range(max(200, last - 30), last + 1):
        if (
            ma50[i] is not None and ma200[i] is not None
            and ma50[i - 1] is not None and ma200[i - 1] is not None
        ):
            if ma50[i] > ma200[i] and ma50[i - 1] <= ma200[i - 1]:
                cross_event = "golden_cross"
                cross_date = dates[i]
            elif ma50[i] < ma200[i] and ma50[i - 1] >= ma200[i - 1]:
                cross_event = "death_cross"
                cross_date = dates[i]
    return {
        "pattern": "cross",
        "name": "50/200 DMA Cross",
        "current_value": {
            "ma50": round(ma50[last], 2),
            "ma200": round(ma200[last], 2),
            "ma50_above_ma200": above,
        },
        "regime": "bullish" if above else "bearish",
        "recent_cross_event": cross_event,
        "recent_cross_date": cross_date,
        "current_date": dates[last] if last < len(dates) else None,
        "tier": "B (moderate)",
        "reference": "knowledge/crypto/cycle-indicators.md",
    }


def detect_mvrv_zone(prices: list[float], dates: list[str]) -> dict:
    """
    Approximate MVRV-Z proxy: z-score of price vs 200D price (cost-basis proxy).
    NOTE: real MVRV-Z requires Glassnode UTXO data; this is a simplification.
    """
    window = 200
    if len(prices) < window:
        return _insufficient("mvrv_zone", window, len(prices))
    ma200 = sma(prices, window)
    sd200 = stdev_window(prices, window)
    last = len(prices) - 1
    if ma200[last] is None or sd200[last] is None or sd200[last] == 0:
        return _insufficient("mvrv_zone", window, len(prices))
    z = (prices[last] - ma200[last]) / sd200[last]

    if z < 0:
        zone = "capitulation"
    elif z < 2:
        zone = "recovery"
    elif z < 5:
        zone = "healthy_bull"
    elif z < 7:
        zone = "elevated"
    else:
        zone = "euphoria"

    return {
        "pattern": "mvrv_zone",
        "name": "MVRV-Z Proxy (price vs 200D MA z-score)",
        "current_value": {
            "price": round(prices[last], 2),
            "ma200": round(ma200[last], 2),
            "stdev200": round(sd200[last], 2),
            "z_proxy": round(z, 3),
        },
        "zone": zone,
        "current_date": dates[last] if last < len(dates) else None,
        "caveat": "PROXY ONLY. True MVRV-Z requires Glassnode realized-cap data. "
                  "This is price/200D-MA z-score as approximation. "
                  "Use directionally; confirm with paid data for ship-grade output.",
        "tier": "B-as-proxy (A if real MVRV-Z available)",
        "reference": "knowledge/crypto/cycle-indicators.md",
    }


def detect_cycle_phase(prices: list[float], dates: list[str]) -> dict:
    """
    Aggregate cycle-phase read from multiple signals.
    Combines Mayer + cross + MVRV-Z proxy + price-vs-200W (if available).
    """
    if len(prices) < 200:
        return _insufficient("cycle_phase", 200, len(prices))

    mayer_r = detect_mayer(prices, dates)
    cross_r = detect_cross(prices, dates)
    mvrv_r = detect_mvrv_zone(prices, dates)
    btc_bot_r = (detect_btc_bottom(prices, dates)
                 if len(prices) >= 1400 else None)

    # Score signals
    signals = []

    if mayer_r.get("zone") in ("deep_accumulation", "accumulation"):
        signals.append("phase1_or_5")
    elif mayer_r.get("zone") == "fair_value":
        signals.append("phase2")
    elif mayer_r.get("zone") in ("premium", "elevated"):
        signals.append("phase3")
    elif mayer_r.get("zone") == "distribution_top":
        signals.append("phase4")

    if cross_r.get("regime") == "bullish":
        signals.append("phase2_3")
    else:
        signals.append("phase4_5")

    if mvrv_r.get("zone") == "capitulation":
        signals.append("phase5_or_phase1_low")
    elif mvrv_r.get("zone") == "recovery":
        signals.append("phase1_2")
    elif mvrv_r.get("zone") == "healthy_bull":
        signals.append("phase3")
    elif mvrv_r.get("zone") == "elevated":
        signals.append("phase3_4")
    elif mvrv_r.get("zone") == "euphoria":
        signals.append("phase4")

    # Naive vote: majority signal type wins
    phase_votes = {"phase1": 0, "phase2": 0, "phase3": 0, "phase4": 0, "phase5": 0}
    for s in signals:
        if "1" in s:
            phase_votes["phase1"] += 1
        if "2" in s:
            phase_votes["phase2"] += 1
        if "3" in s:
            phase_votes["phase3"] += 1
        if "4" in s:
            phase_votes["phase4"] += 1
        if "5" in s:
            phase_votes["phase5"] += 1

    likely = max(phase_votes, key=phase_votes.get)
    confidence = "low"
    if phase_votes[likely] >= 3:
        confidence = "high"
    elif phase_votes[likely] >= 2:
        confidence = "moderate"

    return {
        "pattern": "cycle_phase",
        "name": "Aggregate Cycle Phase Read",
        "likely_phase": likely,
        "confidence": confidence,
        "phase_votes": phase_votes,
        "underlying_signals": {
            "mayer": mayer_r.get("zone"),
            "cross_regime": cross_r.get("regime"),
            "mvrv_z_zone": mvrv_r.get("zone"),
            "btc_bottom_zone": btc_bot_r.get("in_bottom_zone") if btc_bot_r else "n/a",
        },
        "current_date": dates[-1] if dates else None,
        "caveat": "Aggregate read is heuristic. Senior analysts should run "
                  "convergence audit per skills/pattern-recognition/cycle-models.md.",
        "tier": "Aggregate (combines A and B-proxy)",
        "reference": "knowledge/crypto/four-year-cycle.md",
    }


def _insufficient(pattern: str, needed: int, have: int, note: str = "") -> dict:
    return {
        "pattern": pattern,
        "status": "INSUFFICIENT_DATA",
        "needed_bars": needed,
        "have_bars": have,
        "note": note or f"Need at least {needed} bars; have {have}.",
    }


# --------------------------------------------------------------------------
# CLI orchestration
# --------------------------------------------------------------------------

PATTERN_DISPATCH = {
    "pi_top":       lambda p, d: detect_pi_top(p, d),
    "btc_bottom":   lambda p, d: detect_btc_bottom(p, d),
    "mayer_low":    lambda p, d: detect_mayer(p, d),
    "mayer_high":   lambda p, d: detect_mayer(p, d),
    "golden_cross": lambda p, d: detect_cross(p, d),
    "death_cross":  lambda p, d: detect_cross(p, d),
    "mvrv_zone":    lambda p, d: detect_mvrv_zone(p, d),
    "cycle_phase":  lambda p, d: detect_cycle_phase(p, d),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Detect cycle / structural patterns over OHLCV. "
            "See companies/crypto-consultant/skills/pattern-recognition/SKILL.md "
            "for senior interpretation discipline."
        )
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to JSON (from price_scraper.py) or CSV with price/close column.",
    )
    parser.add_argument(
        "--pattern", default="cycle_phase",
        choices=list(PATTERNS_AVAILABLE),
        help="Pattern to detect (default: cycle_phase). 'all' runs every pattern.",
    )
    parser.add_argument(
        "--fail-on-fire", action="store_true",
        help="Exit code 1 if pattern is firing (for CI/automation).",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--quiet", action="store_true", help="Suppress narrative.")
    args = parser.parse_args(argv)

    try:
        prices, dates, meta = load_series(args.input)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not prices:
        print("error: no price data found in input", file=sys.stderr)
        return 2

    results: dict[str, Any] = {
        "scanned_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input_metadata": meta,
        "patterns": {},
    }

    if args.pattern == "all":
        targets = ["pi_top", "btc_bottom", "mayer_low", "golden_cross", "mvrv_zone", "cycle_phase"]
    else:
        targets = [args.pattern]

    fired = False
    for pat in targets:
        fn = PATTERN_DISPATCH.get(pat)
        if not fn:
            continue
        r = fn(prices, dates)
        results["patterns"][pat] = r
        if r.get("firing_now") or r.get("low_zone") or r.get("high_zone") \
                or r.get("in_bottom_zone"):
            fired = True

    results["disclaimer"] = (
        "Patterns are PROBABILISTIC, sample sizes small (N=3-4 cycles for crypto). "
        "Pattern firing = signal to investigate, not directive to act. "
        "Senior interpretation per skills/pattern-recognition/SKILL.md required. "
        "Boundary #4: no buy/sell calls."
    )

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        meta_in = results["input_metadata"]
        print(f"== pattern_detector: {meta_in.get('coin', '?')} "
              f"({meta_in.get('bars', 0)} bars, {meta_in.get('input_format')}) ==")
        for pat_name, r in results["patterns"].items():
            print(f"\n[{pat_name}] — {r.get('name', '')}")
            if r.get("status") == "INSUFFICIENT_DATA":
                print(f"  status: insufficient data ({r.get('have_bars')}/{r.get('needed_bars')})")
                if r.get("note"):
                    print(f"  note: {r['note']}")
                continue
            for k, v in r.items():
                if k in ("pattern", "name"):
                    continue
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        print()
        if not args.quiet:
            print(f"NOTE: {results['disclaimer']}")

    if args.fail_on_fire and fired:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
