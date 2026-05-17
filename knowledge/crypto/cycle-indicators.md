# Cycle Indicators — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.market`, `@crypto.research`, `@crypto.onchain`

---

## Why This File

Cycle-position indicators are the operational vocabulary of crypto research. This file catalogs the major ones with **base rates**, **historical fires**, **invalidation conditions**, and **honest limitations**. Used jointly with `four-year-cycle.md` (frame) and `pattern-recognition/cycle-models.md` (deep skill).

---

## Indicator Reliability Tiering

| Tier | Reliability | Example |
|---|---|---|
| **A — Strong** | Multi-cycle convergent + clear mechanism | 200W MA bottom touch, MVRV-Z extremes, Mayer extremes |
| **B — Moderate** | Multi-cycle directional + plausible mechanism | Pi cycle top, RHODL, NUPL zones |
| **C — Weak** | Limited evidence or analyst-subjective | Log regression bands, Elliott waves, fractals |
| **D — Deprecated** | Failed in recent cycles | Stock-to-Flow as predictive model |

Use Tier A for high-confidence reads; Tier B as confirming; Tier C as illustrative; Tier D not at all.

---

## Tier A Indicators

### 200-Week Moving Average (BTC Bottom Zone)

**Definition**: Price relative to 200W (50-month) moving average.

**Historical fires** (BTC):
| Cycle bottom | Bottom price | 200W MA at time | Distance |
|---|---|---|---|
| Jan 2015 | ~$200 | ~$200 | 0% |
| Dec 2018 | ~$3,200 | ~$3,400 | within 6% |
| Nov 2022 | ~$15,500 | ~$22,500 | within 30% |

**Reliability**: **A — strong**. Every BTC cycle bottom has touched or come within 30% of 200W MA.

**Invalidation**: cycle bottom forms without 200W MA proximity → pattern broken (has not happened).

**Caveat**: 2022 cycle showed 200W MA can be approached without exact touch; structural changes possible.

**Tool**: `pattern_detector.py --pattern btc_bottom`.

---

### Mayer Multiple

**Definition**: Price ÷ 200-day moving average.

**Reference levels**:
| Multiple | Zone |
|---|---|
| <0.7 | Deep accumulation (cycle bottom zone) |
| 0.7-1.0 | Accumulation |
| 1.0-1.5 | Fair value |
| 1.5-2.0 | Premium |
| 2.0-2.4 | Elevated |
| >2.4 | Distribution / cycle top zone |

**Historical**:
- Mayer <0.7 occurred at every major BTC cycle bottom.
- Mayer >2.4 has coincided with every major BTC cycle top.

**Reliability**: **A — strong as zones**, weak as exact triggers.

**Tool**: `pattern_detector.py --pattern mayer_low / mayer_high`.

---

### MVRV-Z Score

**Definition**: (Market Cap - Realized Cap) ÷ stdev(Market Cap).

**Reference levels**:
| MVRV-Z | Zone |
|---|---|
| <0 | Capitulation (cycle bottoms) |
| 0-2 | Recovery |
| 2-5 | Healthy bull |
| 5-7 | Elevated |
| >7 | Euphoria (cycle tops historically) |

**Historical fires (cycle tops)**:
- 2013-12: peaked ~10
- 2017-12: peaked ~12
- 2021-04: peaked ~7

**Reliability**: **A — strong as zones**. Note: 2021 fired at lower MVRV-Z than prior cycles — possible structural shift due to ETF / institutional flow changing cost basis dynamics.

**Caveat**: full MVRV-Z requires paid Glassnode data; our `pattern_detector.py --pattern mvrv_zone` uses simplified proxy. State this in output.

---

## Tier B Indicators

### Pi Cycle Top Indicator

**Source**: Philip Swift, 2019.

**Definition**: 111-DMA crosses ABOVE 350-DMA × 2.

**Historical fires**:
| Date | BTC | Cycle top within |
|---|---|---|
| 2013-04-09 | $230 | 1 day |
| 2017-12-17 | $19,300 | 0 days |
| 2021-04-12 | $63,300 | 2 days |

**Sample size**: N=3. Hit rate: 100% within ±3 days. **Statistically not significant.**

**Reliability**: **B — moderate** (small sample, but striking convergence).

**Invalidation**: pattern fires AND price continues markup for >30 days = pattern broken.

**Tool**: `pattern_detector.py --pattern pi_top`.

---

### NUPL (Net Unrealized Profit/Loss)

**Definition**: (Market Cap - Realized Cap) ÷ Market Cap. Range -1 to +1.

**Reference**:
| NUPL | Color | Zone |
|---|---|---|
| <0 | Red | Capitulation |
| 0-0.25 | Orange | Hope/Fear |
| 0.25-0.5 | Yellow | Optimism |
| 0.5-0.75 | Green | Belief |
| >0.75 | Blue | Euphoria |

**Reliability**: **B — moderate**. Color transitions confirm cycle phase changes after-the-fact.

**Tool**: `pattern_detector.py --pattern nupl` (proxy approximation).

---

### Realized HODL (RHODL)

**Source**: Philip Swift, 2020.

**Definition**: Ratio of realized cap held in 1-week vs 1-2 year cohorts (multiplier-adjusted).

**Reference**: extreme highs historically coincide with cycle tops (short-term holders dominating realized cap = retail FOMO peak).

**Reliability**: **B — moderate**, requires paid data for precision.

**Tool**: `pattern_detector.py --pattern rhodl` (directional only).

---

### Difficulty Ribbon Compression

**Source**: Willy Woo.

**Definition**: 9 moving averages of mining difficulty (9-200 day); compression of bands signals miner equilibrium.

**Historical**: ribbon compression has preceded every BTC cycle bottom by ~30-90 days.

**Reliability**: **B — moderate** (mechanism: weak miners capitulate, leaves stronger miners, equilibrium).

**Tool**: requires hashrate / difficulty data; manual or paid.

---

### Hashrate ATH

**Definition**: New all-time-high in network hashrate.

**Mechanism**: Miners commit hashpower when economically rational; ATH = bullish on miner economics.

**Caveat**: hashrate can lag price (miners deploy after profitable price); ATH alone insufficient signal.

**Reliability**: **B — moderate**, useful as confirmation.

**Tool**: `onchain_metrics.py --metric hashrate`.

---

## Tier C Indicators (Use Cautiously)

### Logarithmic Regression Bands

**Source**: TrololoBubble (anon, 2014); various refinements.

**Definition**: Log-log regression fit to BTC's price vs time, producing rainbow bands.

**Use**: rough framing of "extreme overvalued" vs "extreme undervalued".

**Reliability**: **C — weak**. Subjective fit; structural breaks possible. Not predictive.

---

### Elliott Wave Theory

**Status**: Highly subjective. Different analysts produce different counts on the same data.

**Reliability**: **C — weak as predictor**, useful as descriptive frame for cycle structure.

**Senior usage**: cite as one analytical lens; never as sole basis.

---

### Fibonacci Retracements

**Use**: identifying potential support/resistance zones in retracement.

**Reliability**: **C — weak as standalone**, can confirm structure-based reads.

**Senior usage**: combine with structural levels (HH/HL, range bounds), never alone.

---

## Tier D — Deprecated

### Stock-to-Flow (S2F)

**Source**: PlanB, 2019.

**Status**: **failed as predictive model post-2021**. Initially correlated; broke down significantly in 2022 cycle.

**Senior usage**: cite as historical analytical curiosity, **not** as forward predictor. Pattern-recognition discipline requires honesty about model failures.

---

## Convergence Logic Reference

Senior reads require multi-indicator agreement:

| Convergence | Confidence |
|---|---|
| 1 Tier A indicator | Note (low confidence) |
| 2 Tier A indicators agree | Moderate confidence |
| 3+ Tier A indicators agree | High confidence |
| Tier A + Tier B convergence | Confirming |
| Tier A + macro liquidity agree | High confidence (cycle + macro) |
| Tier C alone | Not a basis for shipping |

When indicators **disagree**, the disagreement is the read. Don't bury divergence.

---

## Cycle-Indicator Calibration (Track Over Time)

Each cycle's indicators should be evaluated post-cycle:

```
[POST-CYCLE INDICATOR AUDIT]
Cycle:                   <e.g. 2024-2026>
Cycle bottom verified:   <date, price>
Cycle top verified:      <date, price>

Indicator               Triggered? Within window? Lessons
Pi cycle top            Y/N        Y/N            ...
Mayer >2.4              Y/N        Y/N            ...
MVRV-Z >7               Y/N        Y/N            ...
200W MA bottom          Y/N        Y/N            ...
...
```

This audit feeds the next cycle's reliability ratings. Reference: `knowledge/crypto/forecast-evaluation.md`.

---

## Reference

- `knowledge/crypto/four-year-cycle.md` (Update 12 — frame).
- `companies/crypto-consultant/skills/pattern-recognition/cycle-models.md` (Update 12 — deep skill).
- `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` (Update 12 — parent skill).
- `tools/pattern_detector.py` (Update 12).
- `tools/price_scraper.py` (Update 12 — historical data input).
- This file paraphrases established crypto cycle indicator literature (Swift, Mayer, Mahmudov, Demeester, Woo); content rephrased for licensing compliance.
