---
name: market-analysis
description: Technical analysis — chart, structure, cycle phase, dominance, derivatives positioning.
company: Crypto Consultant
used_by: ["@crypto.market", "@crypto.research"]
---

# Market Analysis Skill — Crypto Consultant

Read the chart, the structure, the cycle. Different from on-chain (which reads the ledger) and macro (which reads outside crypto).

Inherits Crypto Consultant SOUL. 6-layer output mandatory. Probabilistic. Bear case first.

## When to Use

- Price action read.
- Market structure (HH / HL / range / breakout / breakdown).
- Cycle phase identification (accumulation / markup / distribution / markdown).
- Dominance analysis (BTC.D, ETH.D).
- Volume confirmation.
- Funding rate / open interest read (derivatives positioning).
- Historical analog identification.

## Default Approach

1. **Multi-timeframe**: monthly cycle → weekly regime → daily state. Always start wide.
2. **Structure first, indicators second.** Levels and trend, then RSI / MACD as confirmation.
3. **Volume confirmation.** Move on rising volume = legitimate; falling volume = suspect.
4. **Dominance context.** BTC.D / ETH.D matters even for individual assets.
5. **Derivatives context.** Funding / OI tells you if positioning is crowded.
6. **Cycle position.** State which part of the cycle the read sits in.

## Rules

1. **No price predictions** with deterministic certainty.
2. **No buy/sell calls.** Describe structure + scenarios; risk sizes from `@crypto.risk`; Fathur decides.
3. **No indicator soup.** Clean structure beats stacking 8 indicators.
4. **Multi-timeframe required.** Daily-only reads are half-blind.
5. **State confidence on cycle phase.** "Looks like late accumulation" ≠ "we are in accumulation".
6. **Historical analogs are illustrative**, not predictive. History rhymes; doesn't repeat.

## Output Format — 6 Layers

```
[FACT]
- Current price + timestamp.
- Key levels: support, resistance, range bounds.
- Volume context.
- Dominance (BTC.D, ETH.D).
- Funding rate, OI trend.

[SOURCE]
- TradingView / CoinGecko / Coinglass with timestamp.
- Tool name if internal tool used.

[TREND]
- Multi-timeframe summary: monthly cycle / weekly regime / daily state.
- Recent structural events (breakouts, breakdowns, range tests).

[INTERPRET]
- Cycle phase read with confidence.
- Historical analog (with caveat).
- Where price + dominance + funding agree / disagree.

[SCENARIO]
- Bull / sideways / bear with key levels confirming each.
- Bear case stated FIRST.

[RISK NOTE]
- What invalidates the structural read.
- Macro / event catalysts that override technicals.
```

For setup analysis (when asked "what's a possible setup?"):
```
[SETUP]            Description
[INVALIDATION]     Where structure breaks
[KEY LEVELS]       Specific support / resistance to watch
[CONFIRMATION]     What confirms the move
[NEGATION]         What kills the setup
[REGIME FIT]       Does this fit current cycle phase?
```

Always hand setup work to `@crypto.risk` before it becomes a recommendation.

## Default Sources / Tools

**Free**:
- TradingView (charts, multi-timeframe, alerts).
- CoinGecko / CoinMarketCap (prices, dominance).
- Coinglass (funding, OI, liquidations).

**Internal tools**:
- `fear_greed.py` (Active) — sentiment overlay.
- `btc_price.py` (PLANNED) — price reference.

## Cross-Skill / Cross-Agent

- Macro overlay on this read → `@crypto.macro`.
- On-chain confirmation → `@crypto.onchain`.
- Risk sizing for any setup → `@crypto.risk`.
- Final synthesis → `@crypto.research`.
- Methodology check → `@crypto.qa`.

## What This Skill Does NOT Cover

- DXY / Fed / macro → `@crypto.macro`.
- Wallet flows → `@crypto.onchain`.
- Position sizing math → `@crypto.risk`.
- Generic data dashboard work → `@crypto.data`.

## Reference

- `companies/crypto-consultant/SOUL.md`
- `companies/crypto-consultant/agents/market.md`
- `knowledge/crypto/crypto-research-framework.md`
