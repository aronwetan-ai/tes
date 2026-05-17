# Wyckoff Method — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.market`, `@crypto.research`, `@crypto.onchain`

---

## Why This File

The Wyckoff Method (Richard Wyckoff, 1931) is one of the few **structural** frameworks that holds up well in crypto — accumulation and distribution patterns recur across cycles because they reflect underlying market mechanics (smart money positioning vs retail).

This cheatsheet is the operational reference for recognizing Wyckoff phases in crypto charts. Content paraphrased from the original Wyckoff literature for licensing compliance.

---

## The Wyckoff Three Laws

```
1. SUPPLY AND DEMAND
   Determines price direction.
   Demand > supply → price rises.
   Supply > demand → price falls.

2. CAUSE AND EFFECT
   Time spent in accumulation or distribution = "cause".
   Subsequent move = "effect".
   Larger cause → larger effect (longer ranges → bigger moves).

3. EFFORT VS RESULT
   Volume = effort. Price movement = result.
   Effort/result divergence = warning of trend exhaustion.
```

These three laws underpin every Wyckoff structural read.

---

## The Five-Step Approach

```
1. Determine the present position and probable future trend
   of the market (or the asset).

2. Determine the asset most likely to outperform/underperform
   the market.

3. Select assets aligned with the market trend.

4. Determine assets ready to make a move.

5. Time entry/exit per market analysis.
```

In crypto, this collapses to:
- Read BTC's position in macro cycle.
- Read individual asset's position (often correlated to BTC).
- Wait for setup confirmation.

---

## Wyckoff Accumulation Schematics

### Schematic 1 — Standard Accumulation

```
   Phase A — Stopping the prior downtrend
     PSY  Preliminary Support
     SC   Selling Climax
     AR   Automatic Rally
     ST   Secondary Test

   Phase B — Building the cause (sideways action)
     Multiple ST tests; volume gradually decreasing on tests

   Phase C — Spring (testing strength)
     Spring (or shakeout) — false breakdown below SC low
     followed by rejection on volume

   Phase D — Up-thrust within range
     SOS  Sign of Strength (breakout from range)
     LPS  Last Point of Support (retest of breakout)

   Phase E — Markup (range break above)
     Sustained advance out of range
```

### Schematic 2 — Accumulation Without Spring

Same phases A-E but Phase C lacks the spring; instead, range tightens and breaks higher directly. Less common in crypto but seen.

---

## Wyckoff Distribution Schematics

### Schematic 1 — Standard Distribution (Mirror of Accumulation)

```
   Phase A — Stopping the prior uptrend
     PSY  Preliminary Supply
     BC   Buying Climax
     AR   Automatic Reaction
     ST   Secondary Test

   Phase B — Building the cause (sideways)
     Multiple tests of high; volume signals weakness

   Phase C — Up-thrust (UTAD = Up-Thrust After Distribution)
     False breakout above BC high, followed by rejection

   Phase D — Down-thrust
     SOW  Sign of Weakness (breakdown from range)
     LPSY Last Point of Supply (retest of breakdown)

   Phase E — Markdown (range break below)
     Sustained decline out of range
```

### Schematic 2 — Distribution Without UTAD

Range tightens and breaks lower without final upward shakeout.

---

## Recognizing Wyckoff in Crypto

### Time Scale

Crypto Wyckoff plays out faster than traditional markets:

| Timeframe | Cycle accumulation duration |
|---|---|
| Equities | 6-24 months |
| BTC | 6-12 months |
| Mid-cap alts | 3-9 months |
| Small-cap alts | 1-6 months |

Don't impose equity timescales; crypto compresses.

### Volume Confirmation

Volume is essential for Wyckoff reads. In crypto:

- **Use spot exchange volume**, not derivatives.
- **Cross-check with on-chain transfer volume** (`onchain_metrics.py`) — exchange volume can be wash-traded.
- **Rising volume on rallies, falling on reactions** = bullish Phase D-E.
- **Falling volume on rallies, rising on reactions** = bearish Phase D-E (markdown).

### Phase Identification Order

```
1. Has there been a prior trend? (Wyckoff requires one to reverse from)
2. Has volume signaled a climax (SC or BC)?
3. Has the AR happened?
4. Are we in Phase B (range-building)?
5. Has Phase C (spring or UTAD) occurred?
6. What does Phase D structure look like?
7. Has the range broken?
```

Don't skip phases; partial Wyckoff reads = force-fitting.

---

## Common Crypto Wyckoff Cycles (Historical Examples)

### BTC Cycle 3 Bottom (2018-2019)

- SC: Dec 2018 ~$3,200
- AR: Apr 2019 to ~$5,400
- Phase B: Apr-Aug 2019
- Phase C/D played out
- Markup began late 2019

### BTC Cycle 3 Top (2021)

- BC: Apr 2021 ~$64,800
- AR: May 2021 to ~$30,000
- Phase B: May-Oct 2021
- UTAD: Nov 2021 ~$69,000 (false breakout above April high)
- Markdown: Nov 2021 onward

### BTC Cycle 4 Bottom (2022)

- SC: June 2022 ~$17,500 (initial cap)
- Second SC: Nov 2022 ~$15,500 (FTX collapse)
- AR: Jan 2023 to ~$25,000
- Phase B: Q2-Q4 2023
- Spring + markup: late 2023 - 2024

These are illustrative; real-time identification is harder than retrospective.

---

## Wyckoff vs Other Pattern Frameworks

| Framework | Uses Wyckoff? | When to use |
|---|---|---|
| Wyckoff | Native | Multi-month structural reads |
| Elliott Wave | Different framework | Subjective, harder to falsify |
| Classical TA (H&S, flags) | Compatible | Short-term within Wyckoff context |
| Cycle indicators (Pi, MVRV) | Compatible | Quantitative confirmation |
| On-chain (LTH, exchange flow) | Strong complement | Confirms Phase B accumulation/distribution |

Senior usage: Wyckoff is structural frame; cycle indicators + on-chain confirm the phase identification.

---

## Anti-Patterns

- **Force-fitting Wyckoff on every chart**: Wyckoff requires a prior trend + climax. Random ranges don't qualify.
- **Calling Phase E too early**: range break needs volume confirmation; many false breaks in crypto.
- **Ignoring volume**: Wyckoff without volume is just lines. Volume is the test.
- **Skipping the spring**: Phase C (spring/UTAD) is high-probability identification point. Without it, the read is weaker.
- **Trading Wyckoff on 1-hour chart**: Wyckoff is structural; 1H is noise. Use weekly + daily.
- **Treating Wyckoff predictions as deterministic**: it's a probability frame, not a guarantee.
- **Wyckoff without macro context**: even textbook accumulation can be steamrolled by macro shock.

---

## Reference

- `companies/crypto-consultant/skills/market-analysis/SKILL.md` (parent skill).
- `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` (Update 12).
- `knowledge/crypto/four-year-cycle.md` (Update 12 — Wyckoff phases align with cycle phases).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — quantitative confirmations).
- This file paraphrases the Wyckoff Method (R. Wyckoff, 1931) as applied to crypto. Content rephrased for licensing compliance.
