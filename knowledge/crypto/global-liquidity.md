# Global Liquidity — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.macro`, `@crypto.research`, `@crypto.risk`

---

## Why This File

Crypto cycles are liquidity cycles dressed in technology. Understanding **global liquidity mechanics** is the prerequisite for any cycle-position read that lasts more than a week. This cheatsheet is the operational reference for liquidity sources, lag mechanics, central bank dynamics, and how to **measure** liquidity rather than feel it.

---

## What Is "Global Liquidity"?

Global liquidity = the pool of capital seeking yield across asset classes, **measured** rather than felt.

Three layers:

```
LAYER 1 — MONETARY BASE
  Total money supply (M2) across major economies
  Central bank balance sheets

LAYER 2 — TRANSMISSION
  Real yields (cost of capital)
  DXY (dollar strength relative to peers)
  Bank lending conditions

LAYER 3 — RISK ASSET FLOWS
  Equity inflows / outflows
  Crypto inflows / outflows (ETF + on-chain)
  EM flows
```

Layer 1 generates liquidity; Layer 2 transmits it; Layer 3 absorbs it.

---

## The 12-Week Lag

**Empirical observation**: Global liquidity changes correlate with crypto cycle behavior at approximately a **12-week (3-month) lag**.

**Mechanism**:
- Central bank action → bank lending → capital reallocation → risk-asset bid
- Each step takes weeks
- Smaller institutions react faster; pension/sovereign funds slower
- Average lag ≈ 12 weeks

**Examples**:

| Liquidity inflection | Crypto response |
|---|---|
| Mar 2020 emergency Fed cut + QE | BTC bottom Mar 2020; parabolic Oct 2020 (~6mo) |
| Late 2021 hawkish pivot | Crypto top Nov 2021; bear Dec 2021- |
| Late 2022 reflation hint (TGA / SVB intervention) | Crypto bottom Nov 2022 |
| 2023 Fed rate peak signal | Crypto recovery accelerating Q4 2023 |
| 2024 spot ETF approval | Crypto markup Q1 2024 |

**Operational use**:
- Liquidity expanding NOW = crypto tailwind in ~3 months
- Liquidity contracting NOW = crypto headwind in ~3 months
- This lag is the **single most useful macro insight** for cycle-position timing

**Caveats**:
- Lag varies (6-16 weeks); 12 is approximate
- Lag compresses in crisis (everything correlates to 1)
- Lag extends during crypto-native catalysts (halving, ETF, narrative cycles)
- Sample size for "12 weeks" is small (3-4 cycles); treat as directional, not exact

---

## Global M2 — The Master Liquidity Indicator

### Definition
M2 = currency in circulation + checking deposits + savings deposits + money market funds + small time deposits + (varies by jurisdiction).

### Global M2 Construction
Sum of major economy M2s, USD-equivalent:
- US M2 (FRED `M2SL`)
- EUR M2 (ECB releases)
- JPY M2 (BoJ releases)
- CNY M2 (PBoC releases)
- + smaller: GBP, KRW, INR, BRL

### Reading
| Global M2 YoY | Regime |
|---|---|
| >+15% | Aggressive expansion (rare; crisis response) |
| +5% to +15% | Healthy expansion |
| 0% to +5% | Slow expansion |
| -3% to 0% | Stagnation |
| <-3% | Contraction (rare; significant) |

### Crypto Correlation
- BTC has historically correlated with global M2 at ~0.7-0.8 over multi-year windows
- Strongest correlation at multi-month horizons
- Short-term correlation often poor (crypto-native catalysts dominate)

---

## US M2 — Most Timely Driver

### Why US M2
- Fed policy is global liquidity anchor
- Most timely data (weekly H.6 release)
- Cleanest mechanism

### Dynamics
- QE expands US M2 directly (Fed buys bonds, deposits credited)
- QT contracts US M2 (Fed lets bonds roll off)
- Fiscal expansion (Treasury spending) expands M2 via TGA draw-down
- Fiscal contraction (Treasury issuance > spending) contracts M2 via TGA build-up

### Source
FRED — `M2SL` series (weekly), `M2REAL` for real (inflation-adjusted).

---

## DXY — The Currency Lens

### Definition
USD index trade-weighted against major peers (EUR ~58%, JPY ~14%, GBP ~12%, CAD ~9%, SEK ~4%, CHF ~4%).

### Mechanism
- DXY rising = USD strength = foreign capital flees risk = crypto headwind
- DXY falling = USD weakness = global $-funded liquidity expansion = crypto tailwind

### Reference
| DXY | State | Crypto implication |
|---|---|---|
| <90 | Weak USD | Strong tailwind |
| 90-100 | Neutral | Mixed |
| 100-110 | Strong USD | Headwind |
| >110 | Very strong | Severe headwind |

### Caveats
- DXY is **trade-weighted** — heavy EUR/JPY/GBP
- Doesn't capture USD vs EM currencies
- For full liquidity read, combine with broad-trade-weighted dollar (FRED `DTWEXBGS`)

### Source
ICE / Bloomberg DXY index; `pattern_detector.py --pattern dxy_breakdown` (proxy).

---

## Real Yields — The Cost-of-Capital Lens

### Definition
10-year Treasury Inflation-Protected Securities (TIPS) yield.

### Mechanism
- Real yields rising = real cost of capital rising = liquidity headwind for risk assets
- Real yields falling = liquidity tailwind

### Reference
| 10Y TIPS | State |
|---|---|
| <0% | Very expansionary (post-COVID era) |
| 0-1% | Expansionary |
| 1-2% | Neutral |
| 2-3% | Restrictive |
| >3% | Very restrictive |

### Crypto Sensitivity
- High continuous correlation (negative)
- TIPS rollover from peak often coincides with crypto bottom

### Source
FRED — `DFII10` (10-year TIPS).

---

## Fed Watch — The Policy Lens

### Tier 1 Sources (Cite Verbatim)
- FOMC statement (post-meeting)
- Press conference Q&A
- Dot plot (quarterly)
- SEP (Summary of Economic Projections)

### Tier 2 Sources
- FOMC minutes (3 weeks after)
- Fed governor speeches

### Tier 3 — Inference Layer
- CME FedWatch (Fed funds futures pricing)
- SOFR futures
- Treasury auction results

### Tier 4 — NOT Citable as Fact
- Twitter Fed-watcher accounts
- WSJ "Nick Timiraos" trial balloons (sometimes signal, often noise)

### Pivot vs Cut
- **Pivot** = end of hike cycle / hawkish-to-neutral shift (signal)
- **Cut** = active easing (reality)
- Don't conflate; different signals

### Source
Fed.gov, CME FedWatch tool, FRED.

---

## Treasury Issuance — The Often-Missed Driver

Fed policy is half the story. Treasury issuance is the other half:

### Mechanism
- Large Treasury issuance during QT = liquidity vacuum (capital absorbed)
- Low Treasury issuance = relative liquidity expansion
- TGA balance draw-down = liquidity injection (Treasury spending money)
- TGA balance build-up = liquidity withdrawal
- Debt ceiling resolution = catch-up issuance (can rapidly drain liquidity)

### Source
- Treasury.gov refunding announcements (quarterly)
- FRED — `WTREGEN` (TGA balance), `WLODL` (Treasury issuance pace)

### Operational
Senior macro analysts watch fiscal flow alongside monetary stance. This is the real-world version of "Fed pivot doesn't matter as much as people think" — fiscal flow can offset monetary stance.

---

## Currency Cross Reads (Beyond DXY)

```
USD/CNY                      China capital flow
   PBoC defending yuan / letting it slip
   Stronger CNY = capital staying in China; weaker = capital fleeing

USD/JPY                      Carry trade indicator
   JPY weakness (USD/JPY rising) = global risk-on (carry active)
   JPY strength (USD/JPY falling) = carry unwind, risk-off

EUR/USD                      ECB vs Fed differential
   Mostly secondary for crypto; matters at extremes

USD/EM (broad)               Emerging market stress
   EM crisis = risk-off contagion
```

Senior pattern: BTC has been correlated with USD/JPY at points (carry trade thesis), uncorrelated at others. Track 30-day rolling.

---

## Cross-Asset Correlation Regime

Crypto's correlation with equities shifts:

```
RISK-ON regime          BTC tracks NDX with beta ~1.5
RISK-OFF regime         BTC tracks NDX with beta ~2.0+ (worse than equities)
DECOUPLED regime        BTC moves on idiosyncratic narrative
                        (ETF flows, halving, DeFi event)
```

Detect regime shift by 30-day rolling correlation.

When correlation collapses, crypto-native catalysts dominate. When it surges, macro dominates and crypto-native TA loses signal.

---

## Senior Macro Output Quick-Reference

```
[GLOBAL LIQUIDITY READ]
Issued:              YYYY-MM-DD HH:MM TZ
Decay window:        30 days (or post-event)

[REGIME CALL]
Liquidity:           expanding / neutral / contracting / pivot
Confidence:          high / moderate / low

[FIVE-DRIVER STATE]
Fed funds:           <rate>, last move <date>, next pricing: <%>
Real 10Y (TIPS):     <value>, 30d trend: <state>
US M2 YoY:           <change>, 12mo direction: <state>
DXY:                 <value>, 30d change: <%>, regime: <ranging/trend>
BTC/NDX 30d corr:    <value>, regime: <coupled/decoupled>

[12-WEEK LAG IMPLICATION]
Crypto regime in ~3mo if liquidity continues current path.

[FISCAL OVERLAY]
TGA, issuance, debt ceiling status.

[CALENDAR — NEXT 2 WEEKS]
[macro events table]

[INTERPRET]
[SCENARIO]
[RISK NOTE]
```

---

## Anti-Patterns

- **Predicting central bank decisions with certainty**: Market pricing is best estimate, not guarantee.
- **Single-data-point trends**: One CPI is a print; three consecutive surprises is a trend.
- **Ignoring the 12-week lag**: Real-time liquidity ≠ real-time crypto impact.
- **Fed-only focus**: Treasury fiscal flow is half the story.
- **Quoting Twitter macro as fact**: Use primary sources.
- **Cherry-picking the indicator that agrees**: State all 5 drivers; divergence is the read.
- **Treating equity correlation as constant**: It shifts; track 30d rolling.
- **Conflating "Fed pivot" with "rate cut"**: Pivot ≠ cut.
- **Ignoring Japan / China**: PBoC and BoJ are major players; ignoring them = US-centric blind spot.

---

## Reference

- `companies/crypto-consultant/skills/macro/SKILL.md` (parent skill).
- `companies/crypto-consultant/skills/macro/global-liquidity.md` (Update 12 — deep skill).
- `knowledge/crypto/four-year-cycle.md` (Update 12 — cycle × macro interaction).
- `knowledge/crypto/news-source-rubric.md` (Update 12 — for tier 1 source citation discipline).
- This file paraphrases established global liquidity frameworks (Howell, Macrobond, Steno tradition); content rephrased for licensing compliance.
