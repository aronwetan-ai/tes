---
name: global-liquidity
description: Senior macro liquidity analysis — global M2, central bank balance sheets, real yields, DXY, liquidity-cycle lag, regime detection.
company: Crypto Consultant
agent_specific: "@crypto.macro"
parent_skill: macro
used_by: ["@crypto.macro", "@crypto.research", "@crypto.risk"]
---

# Global Liquidity — Crypto Consultant Deep Skill

Agent-specific extension of `skills/macro/SKILL.md`. Used by `@crypto.macro` for any task that requires reading the macro liquidity regime that crypto cycles ride underneath.

Inherits Crypto Consultant SOUL. Probabilistic. Tier-1 sources only for the citations in this domain.

Core principle: **crypto cycles are liquidity cycles dressed in technology.** Get the liquidity regime wrong and the cycle read collapses, even if every chart looks textbook.

---

## When to Use

- "What is global liquidity doing?"
- Liquidity-regime classification (expanding / neutral / contracting).
- Long-horizon cycle positioning that requires macro overlay.
- Pre-FOMC / pre-CPI positioning brief.
- Cross-asset correlation regime check.
- Risk-on / risk-off transitions.
- Central bank balance sheet tracking.

---

## The Liquidity Hierarchy (Read Top-Down)

```
LEVEL 1 — GLOBAL TOTAL LIQUIDITY (broadest)
  Global M2 (USD-equivalent: US M2 + EUR M2 + JPY M2 + CNY M2)
  Central bank balance sheet sum (Fed + ECB + BoJ + PBoC, USD-eq)
  
LEVEL 2 — MAJOR ECONOMY LIQUIDITY
  US M2 (most timely, most relevant for crypto)
  China total social financing
  EUR M2
  Japan QT/QE state

LEVEL 3 — CURRENCY-RELATIVE LIQUIDITY
  DXY (broad-trade-weighted USD)
  EUR/USD, USD/JPY, USD/CNY
  
LEVEL 4 — REAL YIELD (cost of capital)
  US 10Y TIPS (real yield)
  10Y nominal - 10Y breakeven inflation = real
  Inverted: rising real yields = liquidity headwind
  
LEVEL 5 — POLICY POSTURE
  Fed funds rate + market pricing of next move
  ECB rate
  BoJ posture (still anchored at zero?)
  PBoC RRR + LPR cuts
  
LEVEL 6 — FISCAL OVERLAY
  US Treasury issuance pace (TGA balance, debt ceiling, refunding announcements)
  US deficit trajectory
```

Senior reads work top-down: Level 1 frames the regime; Levels 2-6 explain why.

---

## The 12-Week Lag (Most Useful Macro Insight for Crypto Timing)

**Empirical observation**: Global liquidity changes correlate with crypto cycle accelerations / decelerations at approximately a 12-week lag.

**Mechanism**:
- Liquidity expanding = capital seeking yield → flows into risk assets → crypto inflows accelerate.
- Lag exists because capital reallocation through institutional channels takes weeks to months.
- 2020-2021 cycle: massive QE in March-April 2020 → BTC parabolic Oct 2020-Apr 2021 (6-12 month lag).
- 2022 cycle bottom: liquidity inflection in late 2022 → crypto bottom Nov 2022 (concurrent in this case due to severity).

**Operational use**:
- Liquidity expanding NOW = crypto tailwind in ~3 months.
- Liquidity contracting NOW = crypto headwind in ~3 months.
- This lag is the **single most useful macro insight** for cycle-position timing.

**Caveats**:
- Lag varies (6-16 weeks); 12 weeks is approximate.
- Lag can compress in crisis (everything correlates to 1).
- Lag can extend during crypto-native catalysts (halving, ETF, narrative cycles).

Reference: `knowledge/crypto/global-liquidity.md`.

---

## Liquidity Regime Classification

```
EXPANDING REGIME
  Triggers: Fed cutting OR balance sheet growing OR M2 YoY rising OR DXY weakening
  State: Risk-on across assets; crypto receives tailwind ~12wk later
  Cycle implication: Phase 1-3 acceleration; risk posture aggressive

NEUTRAL REGIME
  Triggers: Fed pause; M2 flat; DXY range-bound
  State: Markets trade on idiosyncratic catalysts
  Cycle implication: Crypto-native dynamics dominate (halving, ETF, etc.)

CONTRACTING REGIME
  Triggers: Fed hiking OR QT active OR M2 contracting OR DXY breaking out
  State: Risk-off; correlations rise; crypto receives headwind
  Cycle implication: Phase 4-5 risk; capital preservation posture

PIVOT REGIME (regime transition)
  Triggers: Fed dot plot shift; first cut after hike cycle; QT taper
  State: High volatility; markets re-price aggressively
  Cycle implication: Often cycle-inflection coincident
```

Senior identification: regime change is detected when **3 of 5 indicators** flip direction simultaneously across a 30-90 day window.

---

## The Five Macro Drivers (Crypto-Sensitivity Ranked)

### Driver 1 — Fed Funds Rate Path
**Tier 1 source**: FOMC statement + dot plot + SEP.
**Tier 1 source**: Fed funds futures (CME FedWatch) for market pricing.
**Crypto sensitivity**: HIGHEST at inflection. First cut after hike cycle = regime change.

### Driver 2 — Real Yields (10Y TIPS)
**Tier 1 source**: FRED — `DFII10` series.
**Mechanism**: Real yields are cost of capital for risk assets. Rising real yields = liquidity headwind regardless of nominal Fed posture.
**Crypto sensitivity**: HIGH continuous. Real-yield rollover from peak often coincides with crypto bottoms.

### Driver 3 — US M2 / Global M2
**Tier 1 source**: FRED — `M2SL` for US; central bank releases for others.
**Mechanism**: M2 expansion = excess liquidity seeking yield.
**Crypto sensitivity**: HIGH mid-cycle (Phase 2-3); LATE-CYCLE concern when M2 stalls.

### Driver 4 — DXY
**Tier 1 source**: ICE / Bloomberg DXY index.
**Mechanism**: Strong USD = foreign capital flees risk; weak USD = global $-funded liquidity expansion.
**Crypto sensitivity**: HIGH during regime shifts.

### Driver 5 — Equity Correlation
**Tier 1 source**: Calculate from price data (BTC vs NDX 30-day rolling correlation).
**Mechanism**: When correlation collapses, crypto-native catalysts dominate; when correlation surges, macro dominates.
**Crypto sensitivity**: VARIABLE; strongest during de-risking.

---

## Fed Watch Discipline — Tier Layered

```
TIER 1 — Primary (cite verbatim)
  FOMC statement (post-meeting, posted to Fed.gov)
  Press conference Q&A (transcript)
  Dot plot (quarterly)
  SEP (Summary of Economic Projections)

TIER 2 — Secondary (citable)
  FOMC minutes (3 weeks after meeting)
  Fed governor speeches (Powell, Williams, Brainard, Waller)

TIER 3 — Inference layer
  Fed funds futures (CME FedWatch)
  Eurodollar curve / SOFR futures
  Treasury auction results

TIER 4 — Noise (NOT for citation)
  Twitter Fed-watcher accounts
  WSJ "Nick Timiraos" trial balloons (sometimes signal, often noise)
  Crypto Twitter macro takes
```

**Senior rule**: never quote "Fed pivot incoming" without citing primary or secondary tier verbatim with date. T4 is suggestive at best; never citable as fact.

---

## Treasury Issuance Overlay (Often Missed)

Fed monetary policy is half the story. Treasury issuance is the other half:

```
LARGE TREASURY ISSUANCE                  = liquidity vacuum
  (especially during QT)                   capital absorbed by Treasuries
  Effect: tighter liquidity than Fed alone

LOW TREASURY ISSUANCE                    = relative liquidity expansion
  Effect: easier conditions even with rates high

TGA BALANCE DRAW-DOWN                    = liquidity injection
  (Treasury General Account spending)      money entering economy
  
TGA BALANCE BUILD-UP                     = liquidity withdrawal
  (Treasury issuance > spending)           money leaving economy

DEBT CEILING RESOLUTION                  = catch-up issuance
  (post-debt-ceiling)                      can rapidly drain liquidity
```

Source: Treasury.gov, FRED.

This is the **real-world version** of "Fed pivot doesn't matter as much as people think" — fiscal flow can offset monetary stance.

---

## Currency Cross Reads

Beyond DXY, watch:

```
USD/CNY                                   = China capital flow
  PBoC defending yuan / letting it slip
  Stronger CNY = capital staying in China; weaker = capital fleeing
  
USD/JPY                                   = carry trade indicator
  JPY weakness (USD/JPY rising) = global risk-on (carry trade active)
  JPY strength (USD/JPY falling) = carry unwind, risk-off

EUR/USD                                   = ECB vs Fed differential
  Mostly secondary for crypto; matters at extremes
  
USD/EM (broad)                            = emerging market stress
  EM crisis = risk-off contagion
```

Senior pattern: BTC has been correlated with USD/JPY at points (carry trade thesis), uncorrelated at others. Track 30-day rolling.

---

## Crypto-Specific Macro Sensitivities

Different crypto assets respond differently to macro:

```
BTC                                       Most macro-sensitive
  Closest to "digital gold" + "risk asset" hybrid
  Real yields = key
  Halving anchor moderates macro sensitivity for ~6mo windows

ETH                                       Hybrid macro + tech
  Tracks BTC at ~0.85 corr
  Tech-sector overlay (NDX correlation higher than BTC)
  
Stablecoins                               Macro-neutral by design
  Issuance = leading liquidity indicator (USDT, USDC mint pace)
  
Memecoins                                 Liquidity-driven extremity
  Late-cycle phenomenon
  Capitulate first, recover last
  
DeFi tokens                               High beta to crypto + DeFi rates
  Spread vs Treasuries matters (yield arb)
```

---

## Output Format — Senior Liquidity Read

```
[GLOBAL LIQUIDITY READ]
Issued:                YYYY-MM-DD HH:MM TZ
Decay window:          30 days OR post-event refresh

[REGIME CALL]
  Liquidity:           expanding / neutral / contracting / pivot
  Confidence:          high / moderate / low
  Stage in regime:     early / mid / late

[FIVE-DRIVER STATE]
  Fed funds:           <rate>, last move <date>, market pricing next: <%>
  Real 10Y (TIPS):     <value>, 30d trend: <state>
  US M2 YoY:           <change>, 12mo direction: <state>
  DXY:                 <value>, 30d change: <%>, regime: <ranging/trend>
  BTC/NDX 30d corr:    <value>, regime: <coupled/decoupled>

[FACTS — ALL TIER 1]
  Cite each fact with FRED / Fed.gov / Treasury.gov + timestamp.

[12-WEEK LAG IMPLICATION]
  If liquidity continues current path, crypto regime in ~3mo: <state>
  Caveats: lag variability; possible cycle-acceleration or compression

[FISCAL OVERLAY]
  TGA balance:         <state>
  Issuance pace:       <state>
  Debt ceiling status: <state>
  Net fiscal effect:   <reinforcing or offsetting monetary>

[INTERPRET]
  What this combined regime typically means.
  Historical analogs (with caveats — different structural era).

[SCENARIO]
  Bear macro: <conditions, crypto impact via 12wk lag>
  Sideways: <muddle-through>
  Bull macro: <liquidity expansion conditions>

[CALENDAR — NEXT 2 WEEKS]
  | Date       | Event       | Tier (1/2/3) | Pricing | Implication |
  | ...        | ...         | ...          | ...     | ...         |

[RISK NOTE]
  Macro shocks that would invalidate this read.
  Policy uncertainty, geopolitical risk, structural breaks.
  What we don't know.

[BOUNDARY #4 STATUS]
  Internal / external publish requires Fathur approval (per `@crypto.ceo`)
```

---

## Anti-Patterns Senior Liquidity Analysts Avoid

- **Predicting central bank decisions with certainty.** They have information you don't; market pricing is best estimate, not guarantee.
- **Single-data-point trends.** One CPI is a print, not a trend. Three consecutive surprises is.
- **Ignoring the 12-week lag.** Real-time liquidity ≠ real-time crypto impact.
- **Fed-only focus.** Treasury fiscal flow is half the story.
- **Quoting T4 sources as fact.** Twitter is suggestive; not citable.
- **Cherry-picking the indicator that agrees.** State all 5 drivers; if they diverge, the divergence IS the read.
- **Treating equity correlation as constant.** It shifts; track 30d rolling.
- **Conflating "Fed pivot" with "rate cut".** Pivot = end of hike cycle; cut = active easing. Different signals.
- **Ignoring Japan / China.** PBoC and BoJ are major players; ignoring them = US-centric blind spot.
- **Promoting one model.** Liquidity is multi-driver; single-driver views fail at regime transitions.

---

## Cross-Skill / Cross-Agent

- Crypto-specific patterns triggered by macro → `@crypto.market` + `skills/pattern-recognition`.
- On-chain confirmation of macro thesis → `@crypto.onchain`.
- Risk overlay on macro scenario → `@crypto.risk`.
- Final synthesis → `@crypto.research`.
- Final report → `@crypto.report` + `skills/reporting`.
- News-driven macro events → `news_scraper.py` + `@crypto.research`.

---

## Reference

- `companies/crypto-consultant/skills/macro/SKILL.md` (parent skill).
- `knowledge/crypto/global-liquidity.md` (Update 12 — full mechanics + sources).
- `knowledge/crypto/news-source-rubric.md` (Update 12 — for tier 1 citation discipline).
- `knowledge/crypto/forecast-evaluation.md` (Update 12 — calibration of macro calls).
- Root SOUL — Boundary #4.
