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


---

## Senior Patterns (Deep Dive) — Update 12

The senior market-analyst playbook. TA in crypto fails most often when the analyst stares at one timeframe, ignores cycle position, or treats indicators as oracles instead of statistical patterns.

### 1. The Top-Down Workflow (Mandatory Before Any Trade Idea)

```
1. CYCLE PHASE      Where are we in the 4Y? (knowledge/crypto/four-year-cycle.md)
                    Confidence on phase identification.

2. MACRO REGIME     Liquidity expanding or contracting?
                    Risk-on or risk-off cross-asset?

3. MONTHLY (1M)     Long-term trend. HH+HL = bull regime; LH+LL = bear.

4. WEEKLY (1W)      Mid-term structure. Which side of 200W MA?
                    Range or trend?

5. DAILY (1D)       Current state. Recent breakouts/breakdowns.

6. 4-HOUR (4H)      Tactical. Only relevant after 1-5 align.

NEVER START FROM 4H. Daily trader's bull setup is a swing trader's
bear retracement is a cycle trader's accumulation buy.
```

### 2. Cycle-Anchored Pattern Library

| Pattern | Fires | Historical reliability | Tool |
|---|---|---|---|
| Pi cycle top | 111-DMA crosses 350-DMA × 2 | 100% within ±3 days for prior 4 cycle tops | `pattern_detector.py --pattern pi_top` |
| Bitcoin bottom (200W MA touch) | Price within 5% of 200W MA | Hit at every prior cycle bottom | `pattern_detector.py --pattern btc_bottom` |
| Mayer Multiple <1 | Price/200D MA <1 | Coincides with accumulation phases | `pattern_detector.py --pattern mayer_low` |
| Mayer Multiple >2.4 | Price/200D MA >2.4 | Coincides with euphoria tops | `pattern_detector.py --pattern mayer_high` |
| Golden cross (50/200 D) | 50DMA crosses above 200DMA | Mid-cycle bull confirmation | `pattern_detector.py --pattern golden_cross` |
| Death cross (50/200 D) | 50DMA crosses below 200DMA | Bear regime confirmation | `pattern_detector.py --pattern death_cross` |
| Wyckoff phases | Pattern of accumulation/distribution structure | Manual recognition | `knowledge/crypto/wyckoff-method.md` |

For each pattern in your read, state:
- **Base rate**: how often it fired correctly historically.
- **Sample size**: across how many cycles.
- **Invalidation**: what disconfirms.

A pattern call without these three is junior work. Reference: `knowledge/crypto/cycle-indicators.md`.

### 3. Volume-Confirmed Structure (Don't Trust Price Alone)

Modern crypto has manipulated levels. Volume tells the truth:

| Move | Volume rising | Volume falling | Volume flat |
|---|---|---|---|
| Breakout | Confirmed | Suspect (likely fakeout) | Wait |
| Breakdown | Confirmed | Possible bear trap | Wait |
| Range high test | Resistance solid | Watch for break | Range continues |
| Range low test | Support solid | Watch for break | Range continues |

Plus on-chain volume (real transfer volume from `onchain_metrics.py`) cross-check — exchange volume can be wash-traded, on-chain transfer volume is harder to fake.

### 4. Dominance + Rotation Reading

Bitcoin Dominance (BTC.D) drives altcoin behavior:

```
BTC.D rising + BTC up      = "BTC season" — alts bleed
BTC.D rising + BTC down    = panic; alts bleed harder
BTC.D falling + BTC up     = "alt season" — capital rotates out of BTC
BTC.D falling + BTC down   = mid-bear; alts often capitulate first
```

Combine with ETH/BTC ratio:
- ETH/BTC rising = appetite for risk within crypto
- ETH/BTC falling = flight to quality (BTC) or capital exit

Rotation timing within cycle is more predictable than absolute price.

### 5. Derivatives Overlay

Funding rate + open interest read (from `funding_rates.py`):

| Funding | OI rising | OI falling | Implication |
|---|---|---|---|
| High positive (>0.05% 8h) | New longs piling in | Longs closing | Top risk if sustained |
| Low/negative | New shorts piling in | Shorts closing | Squeeze potential if low |
| Neutral (~0) | Healthy market | Position flush | Continuation likely |

Senior interpretation:
- **Sustained high funding** at cycle highs = topping signal.
- **Negative funding** at cycle lows = capitulation, often near-bottom.
- **Funding flips** during ranges = volatility incoming.

### 6. Multi-Timeframe Conflict Resolution

When timeframes disagree:

```
Monthly bull + weekly bear     = correction in bull market
                                 (don't fight the higher timeframe)

Monthly bear + weekly bull     = bear-market rally
                                 (sell the rally is base case)

Weekly bull + daily bear       = pullback in uptrend
                                 (look for higher-low entry)

All timeframes bear           = real trend; don't catch falling knife

All timeframes bull           = rare; don't fight the tape
```

The lower timeframe always serves the higher. Saying "weekly bullish but monthly is in markdown phase" is a complete read; "weekly bullish" alone is half-blind.

### 7. Setup Spec (Complete or Don't Ship)

Every setup brought to `@crypto.risk` must include:

```
[SETUP NAME]         Wyckoff Spring / Cup-and-handle / Range high test / etc
[CYCLE FIT]          Does this fit current cycle phase? Why?
[REGIME FIT]         Does macro support? Why?
[TIMEFRAME]          Where it lives (1H / 4H / 1D / 1W)
[ENTRY ZONE]         Range, not single price
[INVALIDATION]       Specific observable level
[CONFIRMATION]       What confirms the move
[NEGATION]           What kills the setup short of stop
[BASE RATE]          How this pattern has performed historically (sample, accuracy)
[POSITION TIME]      Expected hold duration
[ALTERNATIVES]       What else this could be doing
```

Without these fields, `@crypto.risk` rejects sizing.

### 8. Anti-Patterns Senior TA Avoids

- **Single-timeframe reads.** Junior pattern. Always go top-down.
- **Indicator soup.** RSI + MACD + Stoch + Bollinger + Ichimoku stacked = noise. Pick 2-3 with rationale.
- **Force-fitting patterns.** "I see a head-and-shoulders" on every chart = bias. State invalidation; if data fits multiple patterns equally, you have no pattern.
- **Ignoring cycle phase.** "Bullish setup" in late distribution phase has different odds than in mid-markup.
- **Counter-trend trading without explicit framing.** Fading the trend is a pattern itself, not a default.
- **No invalidation level.** Without it, "the trade went against me but I'm still in" becomes excuse.
- **Trading the chart, ignoring the news.** A clean technical setup gets steamrolled by a Fed surprise.

### Reference

- `knowledge/crypto/four-year-cycle.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12).
- `knowledge/crypto/wyckoff-method.md` (Update 12).
- `knowledge/crypto/derivatives-glossary.md` (Update 12).
- `tools/pattern_detector.py`, `tools/price_scraper.py`, `tools/funding_rates.py` (Update 12).
- `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` (Update 12 — pattern parent skill).
