---
name: cycle-models
description: 4-year halving cycle models — Pi cycle top, Mayer Multiple, MVRV-Z, log regression, Wyckoff phases, halving-anchored timing. Senior cycle-position playbook.
company: Crypto Consultant
agent_specific: "@crypto.market"
parent_skill: pattern-recognition
used_by: ["@crypto.market", "@crypto.research", "@crypto.onchain"]
---

# Cycle Models — Crypto Consultant Deep Skill

Agent-specific extension of `skills/pattern-recognition/SKILL.md`. Used by `@crypto.market` (and `@crypto.research` for synthesis) when cycle position is the question.

Inherits Crypto Consultant SOUL. **The 3-Guard discipline applies absolutely** — every model statement requires name+source, base rate, invalidation.

Core principle: **cycles rhyme, they don't repeat.** Models are frames for thinking about probability distributions, not crystal balls. Anyone selling certainty around 4Y cycle predictions is selling a story.

---

## When to Use

- "Where are we in the 4Y cycle?"
- Cycle top / bottom probability assessment.
- Pre-halving / post-halving positioning analysis.
- Long-term portfolio framing (12+ month horizon).
- Calibration check on prior cycle reads.
- Multi-model convergence audit.

---

## The 4-Year Halving Cycle (Reference Frame)

```
PHASE 1 — ACCUMULATION              (~12-18 months)
  After cycle bear bottom.
  Quiet sideways action; on-chain accumulation by LTH; sentiment dead.
  Mayer Multiple <1; MVRV-Z negative or near zero; F&G frequently <30.

PHASE 2 — PRE-HALVING MARKUP        (~6-9 months pre-halving)
  Anticipation of supply shock; price slowly rises.
  Mayer Multiple 1-1.5; MVRV-Z rising from negative; F&G rising to 50-70.

   [HALVING EVENT]                  Block-reward cut by 50%

PHASE 3 — POST-HALVING MARKUP       (~12-18 months post-halving)
  Supply shock realized; demand catches up; price parabolic.
  Mayer Multiple 1.5-2.4; MVRV-Z rising to 5-7; F&G frequently >70.

PHASE 4 — DISTRIBUTION / TOP        (~3-6 months)
  Euphoria; smart money distributing; new retail entering.
  Mayer Multiple >2.4; MVRV-Z >7; F&G frequently >80; Pi cycle fires.

PHASE 5 — MARKDOWN / BEAR           (~12-18 months back to Phase 1)
  Distribution complete; price collapses ~80-90% from top.
  Mayer Multiple back to <1; MVRV-Z back to <0; F&G crashes to <20.
```

Total cycle: ~4 years, anchored to ~210,000 block halving events (every ~4 years).

Halvings to date:
- 2012-11-28 — Block 210,000 — reward 50→25 BTC
- 2016-07-09 — Block 420,000 — reward 25→12.5 BTC
- 2020-05-11 — Block 630,000 — reward 12.5→6.25 BTC
- 2024-04-19 — Block 840,000 — reward 6.25→3.125 BTC
- 2028-04 (estimated) — Block 1,050,000 — reward 3.125→1.5625 BTC

Reference: `knowledge/crypto/four-year-cycle.md`.

---

## Model 1 — Pi Cycle Top Indicator

**Source**: Philip Swift, 2019.

**Definition**: 111-day moving average crosses ABOVE 350-day moving average × 2.

**Mechanism**: When short-term price acceleration meets a multiple of long-term, the cycle is overheating.

**Historical fires**:
| Date | BTC price | Cycle top within | Days |
|---|---|---|---|
| 2013-04-09 | $230 | $260 (top: 2013-04-10) | 1 day |
| 2017-12-17 | $19,300 | $19,800 (top: 2017-12-17) | 0 days |
| 2021-04-12 | $63,300 | $64,800 (top: 2021-04-14) | 2 days |

**Sample size**: N=3. Hit rate: 100% within ±3 days. **Statistically not significant**.

**Invalidation**: Pi cycle has fired and price continued markup for >30 days = pattern broken (has not happened historically, but theoretical possibility).

**Tool**: `pattern_detector.py --pattern pi_top`.

**Limitations**:
- Does not predict drawdown depth or duration.
- Does not signal bottom.
- May fail in altered market structure (post-ETF, institutional, microstructure changes).
- N=3 is descriptive, not statistical.

**Senior usage**: when Pi cycle approaches firing, increase risk scrutiny + check convergence with other top indicators. Pi alone is suggestive; Pi + MVRV-Z>7 + Mayer>2.4 + euphoria funding is high-confidence top zone.

---

## Model 2 — Mayer Multiple

**Source**: Trace Mayer.

**Definition**: BTC price ÷ 200-day moving average.

**Reference levels**:
| Multiple | State |
|---|---|
| <1.0 | Discount zone (historical accumulation territory) |
| 1.0-1.5 | Fair value range |
| 1.5-2.0 | Premium |
| 2.0-2.4 | Elevated |
| >2.4 | Historical "sell zone" — coincides with cycle tops |

**Historical context**: Mayer Multiple <0.7 has occurred at every cycle bottom; >2.4 has coincided with every cycle top.

**Tool**: `pattern_detector.py --pattern mayer_low / mayer_high`.

**Senior usage**: zones, not triggers. "Mayer at 0.65 = deep accumulation zone" is honest; "Mayer at 0.65 = bottom is in" is overconfident.

---

## Model 3 — MVRV / MVRV-Z Score

**Source**: Murad Mahmudov, David Puell, 2018.

**Definition**:
- MVRV = Market Cap ÷ Realized Cap
- MVRV-Z = (Market Cap - Realized Cap) ÷ stdev(Market Cap)

**Mechanism**: When market value runs far above realized (cost-basis aggregate), holders are sitting on large unrealized profit → distribution risk.

**Reference levels** (BTC historical):
| MVRV-Z | State | Historical context |
|---|---|---|
| <0 | Capitulation | Cycle bottoms |
| 0-2 | Recovery | Phase 1-2 transition |
| 2-5 | Healthy bull | Mid-cycle |
| 5-7 | Elevated | Late cycle |
| >7 | Euphoria zone | Cycle tops |

**Historical fires (cycle tops)**:
- 2013-12: MVRV-Z peaked ~10
- 2017-12: MVRV-Z peaked ~12
- 2021-04: MVRV-Z peaked ~7

Note: 2021 cycle top fired at lower MVRV-Z than prior — possible structural shift due to institutional / ETF inflows changing cost basis dynamics.

**Tool**: `pattern_detector.py --pattern mvrv_zone` (approximation; full MVRV-Z requires paid Glassnode data).

**Caveat**: realized cap calculation depends on UTXO data; without paid Glassnode access, our tool uses simplified proxy (200D price avg as cost-basis approximation). State this in output.

---

## Model 4 — NUPL (Net Unrealized Profit/Loss)

**Source**: Tuur Demeester / Adamant Capital framework.

**Definition**: (Market Cap - Realized Cap) ÷ Market Cap. Range -1 to +1.

**Reference zones**:
| NUPL | Color zone | Cycle phase |
|---|---|---|
| <0 | Capitulation (red) | Cycle bottoms |
| 0-0.25 | Hope/Fear (orange) | Recovery |
| 0.25-0.5 | Optimism (yellow) | Early bull |
| 0.5-0.75 | Belief (green) | Mid bull |
| >0.75 | Euphoria (blue) | Cycle tops |

**Senior usage**: NUPL color transitions are slow; useful for confirming cycle phase changes after-the-fact, less for real-time prediction.

---

## Model 5 — Realized HODL (RHODL)

**Source**: Philip Swift, 2020.

**Definition**: Ratio of realized cap held in 1-week vs 1-2 year cohorts (with multiplier).

**Reference**: extreme highs historically coincide with cycle tops (short-term holders dominating realized cap = retail FOMO peak).

**Tool**: `pattern_detector.py --pattern rhodl` (approximation).

**Status**: requires paid data for precision; our tool is directional only.

---

## Model 6 — 200-Week Moving Average (BTC Bottom)

**Definition**: BTC price approaching or touching the 200-week (50-month) MA.

**Historical**: BTC has touched the 200W MA at every cycle bottom:
- 2015-01: bottom ~$200, 200W MA ~$200
- 2018-12: bottom ~$3,200, 200W MA ~$3,400
- 2022-11: bottom ~$15,500, 200W MA ~$22,500 (closest touch within 30%)

**Senior usage**: 200W MA is bottom **zone**, not trigger. "Within 20% of 200W MA + macro capitulation" = high probability bottom zone.

**Tool**: `pattern_detector.py --pattern btc_bottom`.

---

## Model 7 — Logarithmic Regression Bands (Bitcoin Power Law)

**Source**: TrololoBubble (anonymous, 2014); refined by various analysts.

**Definition**: Log-log regression fit to BTC's price-vs-time data, producing rainbow bands of fair value.

**Reference**:
- "Maximum bubble territory" (top band) = sell zone historically.
- "Basically a fire sale" (bottom band) = bottom zone historically.

**Caveats**:
- Log regression assumes BTC's growth pattern continues; structural breaks possible.
- Subjective — different analysts fit different curves.
- Useful as a rough framing, not an exact level.

**Senior usage**: as one input to cycle position, never as a single signal.

---

## Model 8 — Wyckoff Cycle Phases (Structural)

**Source**: Richard Wyckoff, 1931 (applied to crypto by various analysts).

**Phases**:
- Accumulation Schematics 1, 2 — sideways structure with PSY → BC → AR → ST → SC → spring → SOS → LPS → markup.
- Distribution Schematics 1, 2 — mirror structure: PSY → BC → AR → ST → UTAD → SOW → LPSY → markdown.

**Senior usage**: Wyckoff is structural rather than time-based. Recognizing a Wyckoff pattern requires:
- Multi-month observation
- Volume confirmation at key zones
- Cycle context (Wyckoff accumulation in Phase 1 = bullish; Wyckoff distribution in Phase 4 = bearish)

Reference: `knowledge/crypto/wyckoff-method.md`.

---

## Model 9 — Halving-Anchored Timing

**Empirical observation** (3 cycles only):
- Cycle bottom typically ~12-18 months **before** halving.
- Cycle top typically ~12-18 months **after** halving.

**Cycle 4 (2024 halving) timing reference**:
- Halving: 2024-04-19
- Predicted top window (if pattern repeats): 2025-04 to 2025-10
- Predicted bottom window for cycle 5 (if pattern repeats): 2026-04 to 2026-10

**Caveats**:
- N=3, descriptive not statistical.
- Each cycle's structure has shortened (timing-wise vs prior). Cycle 5 may compress further.
- Macro liquidity overlay can extend or compress.
- Spot ETF (since 2024) may have changed institutional flow dynamics.

**Senior usage**: halving-anchored timing is a frame for "where might we be?", never a calendar prediction.

---

## Model 10 — Stock-to-Flow (Deprecated as Predictive)

**Source**: PlanB, 2019.

**Status**: **failed as a predictive model post-2021.** Initially correlated; broke down significantly in 2022 cycle.

**Senior usage**: cite as historical analytical curiosity, **not** as forward predictor. Pattern-recognition discipline requires honesty about model failures.

---

## Convergence Audit (The Senior Read)

Cycle position reads are most defensible when **multiple models agree**:

```
[CYCLE POSITION CONVERGENCE AUDIT]
Issued:                     YYYY-MM-DD

Model 1 — Pi cycle status:        <not yet fired / firing / post-fire>
Model 2 — Mayer Multiple:         <value, zone>
Model 3 — MVRV-Z:                 <value, zone>
Model 4 — NUPL color:             <zone>
Model 5 — RHODL:                  <zone, approximation note>
Model 6 — 200W MA distance:       <% above/below>
Model 7 — Log regression band:    <which band>
Model 8 — Wyckoff structure:      <phase, schematic if applicable>
Model 9 — Halving timing window:  <where in window>
Model 10 — Stock-to-Flow:         not used (deprecated)

[CONVERGENCE LEVEL]
  L1 (single model)         = note
  L2 (2 models same domain) = moderate confidence
  L3 (2+ models different)  = high confidence
  L4 (5+ models agree)      = highest confidence

[PHASE READ]
  Most likely phase: <phase>
  Confidence:        <high / moderate / low>

[PHASE READS BY MODEL]
  <list each model's implied phase>

[DISAGREEMENT NOTES]
  <models that point different direction; what would resolve>
```

---

## Anti-Patterns Senior Cycle Modelers Avoid

- **Single-model confidence.** Pi cycle alone, MVRV alone, Mayer alone — each has failed in some context. Convergence is the senior read.
- **Stock-to-flow worship post-2022.** It broke. Acknowledge.
- **Treating N=3 as predictive.** Three cycles = descriptive sample. Each cycle may be different.
- **Calendar-based cycle predictions.** "Top in April 2025" without convergence check is calendar astrology.
- **Ignoring structural changes.** ETF, institutional, regulatory shifts may alter cycle dynamics — flag as uncertainty.
- **Burying low confidence.** "Cycle top is in" with N=3 base = overconfident. Honest version: "high probability we're in distribution zone."
- **Promoting models past their evidence.** Especially common with rainbow charts and S2F.

---

## Reference

- `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` (parent skill).
- `knowledge/crypto/four-year-cycle.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — full library + reliability ratings).
- `knowledge/crypto/wyckoff-method.md` (Update 12).
- `knowledge/crypto/forecast-evaluation.md` (Update 12 — calibration tracking).
- `tools/pattern_detector.py` (Update 12).
- `tools/price_scraper.py` (Update 12 — historical OHLCV input).
