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


---

## Senior Patterns (Deep Dive) — Update 12

The senior macro analyst playbook for crypto. Crypto cycles are ultimately liquidity cycles dressed in technology — getting macro wrong gets the cycle wrong even if every chart looks right.

### 1. Liquidity-First Mental Model

```
GLOBAL LIQUIDITY EXPANDING       =  risk-on regime; crypto cycle accelerates
GLOBAL LIQUIDITY CONTRACTING     =  risk-off regime; crypto cycle stalls or reverses

Liquidity proxies (in order of crypto-correlation strength):
  1. Global M2 (USD + EUR + JPY + CNY combined, USD-equivalent)
  2. US M2 (narrower but timely)
  3. Central bank balance sheet sum
  4. DXY (inverse correlation; weak DXY = global $ liquidity higher)
  5. Real yields (10Y TIPS — rising = liquidity headwind)
```

Crypto correlates with global liquidity at ~12-week lag historically. Liquidity expanding now = crypto tailwind in ~3 months. This lag is the **single most useful macro insight** for cycle timing.

Reference: `knowledge/crypto/global-liquidity.md`.

### 2. The Five Macro Drivers (In Priority Order)

| Driver | What to watch | Crypto sensitivity |
|---|---|---|
| Fed funds rate path | FOMC + dot plot + market pricing | Highest at inflection |
| Real yields (10Y TIPS) | TIPS, breakevens | High continuous |
| US M2 / global M2 | FRED, central bank releases | Highest mid-cycle |
| DXY | Trade-weighted dollar index | High during regime shifts |
| Equities (NDX) correlation | Mag 7, NDX, SPX | Variable; strongest during de-risking |

Tier 6+: commodity prices (gold, copper, oil) — secondary unless commodity shock.

### 3. The Fed Watch Discipline

Senior analysts read **what the Fed actually says**, not what Twitter says they said.

```
Tier 1 — Primary
  FOMC statement (post-meeting)
  Press conference Q&A
  Dot plot (quarterly)
  SEP (Summary of Economic Projections)

Tier 2 — Secondary
  FOMC minutes (3 weeks after meeting)
  Fed governor speeches (Powell, Williams, Brainard, Waller)

Tier 3 — Inference layer
  Fed funds futures (CME FedWatch)
  Eurodollar curve
  Treasury auction results

Tier 4 — Noise (don't trade off)
  Fed-leak Twitter
  WSJ "Nick Timiraos" trial balloons (sometimes signal, often noise)
```

Senior pattern: **never** quote "Fed pivot incoming" without citing primary or secondary tier source verbatim with date.

### 4. Macro Calendar Discipline

Track the calendar two weeks ahead:

```
[NEXT 2 WEEKS — MACRO CALENDAR]
| Date       | Event              | Importance | Pricing | Crypto implication |
| 2026-05-19 | Powell speech      | Medium     | Hawkish | Risk-off if hawk    |
| 2026-05-21 | Fed minutes        | High       | -       | Volatility window   |
| 2026-05-24 | Core PCE           | High       | 0.3%    | Risk-on if soft     |
| 2026-05-28 | NFP                | High       | 200k    | Strong = risk-off   |
| 2026-06-04 | ECB decision       | Medium     | Hold    | DXY mover           |
```

Crypto trades the **delta vs expectation**, not the absolute number.

### 5. Cross-Asset Correlation Regime

Crypto's correlation with equities shifts:

```
RISK-ON regime          BTC tracks NDX with beta ~1.5
RISK-OFF regime         BTC tracks NDX with beta ~2.0+ (worse than equities)
DECOUPLED regime        BTC moves on idiosyncratic narrative
                        (ETF flows, halving, DeFi event)
```

Detect regime shift by 30-day rolling correlation. When correlation collapses, crypto-native catalysts dominate. When it surges, macro dominates and crypto-native TA loses signal.

### 6. The DXY Cheat Sheet

| DXY trend | Mechanism | Crypto implication |
|---|---|---|
| DXY rising | $ strength; foreign capital flees risk | Crypto headwind |
| DXY falling | $ weakness; global liquidity easier | Crypto tailwind |
| DXY range-bound | No liquidity regime change | Crypto trades on internals |

Caveat: DXY is trade-weighted (heavy EUR, JPY, GBP). It's a **dollar vs developed peers** index. Doesn't capture USD vs EM currencies. For full liquidity read, combine with broad-trade-weighted dollar (DTWEXBGS on FRED).

### 7. Senior Macro Output Template

```
[MACRO READ — Crypto Implication]
Issued:             YYYY-MM-DD HH:MM TZ
Decay window:       30 days (or post-event)

[REGIME CALL]
  Liquidity:        expanding / neutral / contracting
  Risk:             risk-on / mixed / risk-off
  Correlation:      crypto~equities / decoupled / inverse

[FACTS]
  DXY:              <value, 30d change>
  Fed funds:        <rate>, last move <date>
  Next FOMC:        <date>
  10Y nominal:      <value>
  10Y real:         <value>
  M2 YoY:           <change>
  NDX 30d:          <change>
  BTC/NDX 30d corr: <value>

[SOURCE]
  Each fact tagged with FRED / Fed.gov / TradingView / etc + timestamp.

[INTERPRET]
  What this regime typically means for crypto cycle.
  Caveats and historical analogs.

[SCENARIO]
  Bear: <macro shock conditions + crypto impact>
  Sideways: <muddle-through conditions>
  Bull: <liquidity expansion conditions>

[CALENDAR — NEXT 2 WEEKS]
  <macro events table>

[RISK NOTE]
  What macro shock would invalidate this regime call.
  Policy uncertainty, election risk, geopolitical risk.
```

### 8. Anti-Patterns Senior Macro Avoids

- **Predicting central bank decisions with certainty.** They have information you don't; market pricing is best estimate, not guarantee.
- **Single-data-point trends.** One CPI print isn't a trend. Three consecutive surprises is.
- **Ignoring lag.** Liquidity → crypto has ~12 week lag; ignore this and you fade real moves.
- **Quoting Twitter macro.** Use primary sources.
- **Cherry-picking the indicator that agrees.** State all five drivers; if they diverge, the divergence is the read.
- **Treating equity correlation as constant.** It shifts; track 30d rolling.
- **Conflating "Fed pivot" with "rate cut".** Pivot = end of hike cycle; cut = active easing. Different signals.
- **Ignoring fiscal alongside monetary.** Fed tightening + Treasury issuance flooding = different from tightening alone.

### Reference

- `knowledge/crypto/global-liquidity.md` (Update 12).
- `knowledge/crypto/news-source-rubric.md` (Update 12 — for tier 1 source citation).
- `companies/crypto-consultant/skills/macro/global-liquidity.md` (Update 12 — agent-specific deep skill).
