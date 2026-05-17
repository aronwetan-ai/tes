---
name: macro
description: Macro context for crypto — DXY, Fed, M2, yields, equities. Liquidity-first cycle analysis.
company: Crypto Consultant
used_by: ["@crypto.macro", "@crypto.research"]
---

# Macro Skill — Crypto Consultant

Crypto cycles don't happen in a vacuum. Liquidity expands → risk-on → crypto rallies. Liquidity contracts → risk-off → crypto bleeds. Understanding what's happening in TradFi is half the job.

Inherits Crypto Consultant SOUL. 6-layer format. Probabilistic. Cite specific numbers and dates.

## When to Use

- DXY (US dollar index) read for crypto implications.
- Fed policy analysis (rate decisions, FOMC minutes, dot plot).
- Money supply tracking (M2, global liquidity proxies).
- Treasury yield analysis (2Y, 10Y, real yields, curve shape).
- Equity correlation (SPX / NDX / Mag 7 vs BTC).
- Commodities (gold = digital gold narrative; oil; copper).
- Macro event calendar (CPI, NFP, FOMC dates).
- Cross-asset correlation regime shifts.

## Default Macro Frame

For any "what's macro saying for crypto?" question:

1. **Liquidity proxy** — DXY direction, M2 trend, global liquidity index. Tightening or loosening?
2. **Real yields** — 10Y TIPS. Up = bad for risk. Down = good.
3. **Fed posture** — Hawkish / dovish based on most recent statements + market pricing of next move.
4. **Equity correlation** — Is BTC moving with NDX or independently?
5. **Narrative** — Dominant macro story this month (inflation / recession / soft landing / debt ceiling / etc).

Synthesize into a **macro regime call**: risk-on / risk-off / mixed / pivot incoming.

## Rules

1. **No central bank prediction with certainty.** Describe what they've done and said. Pricing of next move ≠ guarantee.
2. **Single data point ≠ trend.** One CPI print is a data point, not disinflation.
3. **Don't invent macro data.** If FRED / source unavailable, say so.
4. **Cross-asset checks required.** Crypto-only macro is half-blind.
5. **Specific numbers + dates.** Vague "market conditions" is non-content.
6. **Liquidity > sentiment** as primary driver of risk-asset cycles.

## Output Format — 6 Layers

```
[FACT]
- DXY: <value>, <change %, period>
- Fed funds: <rate>
- 10Y yield: <value>, <change>
- Real 10Y (TIPS): <value>
- M2: <YoY change>
- Recent macro events: <CPI, FOMC dates with values>

[SOURCE]
- FRED / Fed.gov / Treasury / Trading Economics / FOMC statements with dates.

[TREND]
- DXY trend (last 30 / 90 days).
- Yield curve shape.
- Equity / crypto correlation regime.

[INTERPRET]
- What this macro setup typically means for risk assets.
- Caveats and historical analogs.

[SCENARIO]
- 2-3 macro paths with crypto implications.
- Bear case first.

[RISK NOTE]
- What macro shock could break this thesis.
- What we don't know (upcoming data, policy uncertainty).
```

For macro calendar:
```
[NEXT WEEK]
| Date       | Event       | Importance | What to watch | Crypto implication |
| YYYY-MM-DD | CPI print   | High       | Above/below %  | Risk-on if soft   |
...
```

## Default Sources

**Free / Public**:
- FRED (Federal Reserve Economic Data).
- Treasury.gov releases.
- Fed.gov (FOMC statements, minutes, dot plot).
- BLS for CPI / NFP.
- Trading Economics, Investing.com for charts.

**Freemium**:
- TradingView for cross-asset charts.
- Reuters / Bloomberg headlines.

**Paid (escalate to `@crypto.ceo`)**:
- Bloomberg Terminal.
- Steno Research.
- 22V Research.
- MacroBond.

If a macro read needs paid data we don't have, say so. No fabrication.

## Cross-Skill / Cross-Agent

- Crypto-specific technical / chart → `@crypto.market`.
- On-chain confirmation of macro thesis → `@crypto.onchain`.
- Risk overlay on macro scenario → `@crypto.risk`.
- Generic data work → `@crypto.data`.
- Final synthesis → `@crypto.research`.
- Final report → `@crypto.report`.

## What This Skill Does NOT Cover

- Crypto-specific technicals → `@crypto.market`.
- On-chain forensics → `@crypto.onchain`.
- Position sizing math → `@crypto.risk`.

## Reference

- `companies/crypto-consultant/SOUL.md`
- `companies/crypto-consultant/agents/macro.md`
- `knowledge/crypto/crypto-research-framework.md`
