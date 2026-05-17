# Scenario Modeling — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.research`, `@crypto.market`, `@crypto.risk`, `@crypto.report`

---

## Why This File

Scenarios are the structural alternative to single-point predictions. Senior crypto research produces **multiple scenarios with relative likelihood** rather than "BTC will go to $X." This file is the canonical reference for scenario construction, weighting, and rendering.

---

## The Scenario Frame

Every multi-week-horizon view ships with **3 scenarios** at minimum:

```
BEAR CASE         (always stated FIRST)
SIDEWAYS CASE
BULL CASE
```

Plus optional:
```
TAIL BEAR         (extreme downside; <10% probability)
TAIL BULL         (extreme upside; <10% probability)
```

Senior reads sometimes use 5 scenarios when distributions warrant it.

---

## The Construction Workflow

```
STEP 1: Identify cycle phase (frame)
        Phase 1-5 per four-year-cycle.md

STEP 2: Identify macro regime (modulator)
        Expanding / neutral / contracting per global-liquidity.md

STEP 3: Identify dominant catalysts (next 30-90 days)
        Macro events (FOMC, CPI), crypto events (halving, ETF approvals),
        geopolitical, regulatory

STEP 4: For each scenario (Bear / Sideways / Bull):
        - State conditions that produce this outcome
        - State key levels (support/resistance/breakouts)
        - State price range (NOT single number)
        - State time horizon
        - State probability (as %, summing to 100%)
        - State invalidation (what would force re-evaluation)

STEP 5: Verify probabilities sum to 100% across all scenarios

STEP 6: Bear case must be stated FIRST in output
```

---

## Probability Weighting Heuristics

Senior reads avoid common biases:

```
COMMON MISTAKES:
- Overweighting recency (last week's price action dominates)
- Anchor bias (starting from current price as baseline)
- Confirmation bias (favoring scenarios that match prior view)
- Bullish bias (industry-wide tendency)
- Recency-of-event bias (last big event over-weights)

SENIOR DEFAULTS:
- Distribute probabilities reflecting cycle phase
- Phase 1: bull-tilted (50/30/20 or similar)
- Phase 3: bull-tilted but with rising bear weight
- Phase 4: balanced (30/35/35) — top zone uncertainty high
- Phase 5: bear-tilted (40/40/20)

CHECK:
- If probabilities feel uncomfortable, you're probably more honest
- "I'm 80% confident in bull" is rarely justifiable in crypto
```

---

## Scenario Construction Template

### BEAR CASE (Stated First)

```
[BEAR CASE]
Probability:           X% (state explicit)
Time horizon:          N days
Conditions to develop:
  - Specific observable conditions
  - e.g. "BTC closes below $58K weekly with on-chain net inflow >50k BTC over 14d"
Price range:           $A - $B (range, not single number)
Key levels:
  - First support breach: $X
  - Second support: $Y
  - Capitulation zone: $Z
Catalysts that could trigger:
  - Specific named events
Invalidation:
  - What would mean this scenario is wrong
  - e.g. "Sustained close >$72K with positive on-chain"
```

### SIDEWAYS CASE

```
[SIDEWAYS CASE]
Probability:           Y%
Time horizon:          N days
Conditions:            Range-bound
Range:                 $A - $B
Catalysts:             What sustains range
Break direction triggers:
  - Up: <conditions>
  - Down: <conditions>
```

### BULL CASE

```
[BULL CASE]
Probability:           Z%
Time horizon:          N days
Conditions to develop:
  - Specific observable
Price range:           $A - $B
Key levels:
  - First resistance: $X
  - Target zone: $Y
  - Extreme bull (rare): $Z
Catalysts:
Invalidation:
```

### Verification

```
Bear% + Sideways% + Bull% = 100%

If using tail cases:
Bear% + Tail-Bear% + Sideways% + Bull% + Tail-Bull% = 100%
```

---

## Range Discipline (Not Single Numbers)

**Forbidden**: "BTC will reach $100,000."
**Required**: "Bull scenario points to $90,000-$110,000 over the next 90 days, with conditions: ..."

Why ranges:
- Crypto volatility makes single numbers misleading
- Ranges reflect actual uncertainty
- Forces honest communication of confidence
- Aligns with probability framing

**Range width heuristics**:
- Short horizon (<30 days): narrower range OK (5-10%)
- Medium horizon (30-90 days): 15-25% range typical
- Long horizon (90+ days): 30%+ range, often wider
- Cycle horizon: very wide ranges (50%+)

---

## Tail Scenario Discipline

For tail scenarios (extreme outcomes), state:

```
[TAIL BEAR]
Probability:           <10%
Trigger:               Specific tail event (e.g. major exchange insolvency)
Impact:                Severe (-50% to -70% from current)
Mitigation:            Already-existing position sizing should survive
Watch indicators:      What signals tail brewing
```

Tail scenarios are NOT bear scenarios. They have separate probability, separate triggers, separate management.

---

## Catalysts vs Conditions

Senior scenario modeling distinguishes:

- **Catalysts** = events that could trigger the scenario (FOMC decision, ETF flow event, regulatory ruling)
- **Conditions** = market state required for scenario to develop (key levels, on-chain confirmation, sentiment)

Both stated; one without the other is half-formed.

---

## Forecast Decay

All scenarios have a **decay window**:

```
Short-horizon (<30 days):    decay 7 days
Medium-horizon (30-90 days): decay 14-30 days
Long-horizon (>90 days):     decay 30 days
Cycle-horizon:               decay 30 days for confidence; 90+ for direction
```

After decay, scenario must be **refreshed** before reuse. Stale scenarios poison synthesis.

Reference: `companies/crypto-consultant/SOUL.md` Prediction Discipline.

---

## Multi-Asset Scenario Construction

When scenarios cover multiple assets, structure separately:

```
[BTC SCENARIOS]
  Bear / Sideways / Bull (with probabilities for BTC specifically)

[ETH SCENARIOS]
  May differ from BTC due to relative dynamics
  Reference ETH/BTC ratio scenarios

[ALT BROAD SCENARIOS]
  Often inherit from BTC + relative beta

[CROSS-ASSET CORRELATION ASSUMPTIONS]
  State explicitly (e.g. "Assumes BTC/ETH correlation remains >0.85")
```

Senior reads acknowledge: "BTC scenarios drive most alt scenarios, but with leverage / correlation caveats."

---

## Scenario Conflict Detection (Check Before Ship)

Before shipping, audit for internal contradictions:

```
[ ] If macro regime is contracting, is bull case probability appropriate?
    (Should be lower than expanding regime)

[ ] If cycle phase is Phase 4 (top), is bull case % too high?
    (Should be lower than Phase 1-2)

[ ] If on-chain shows distribution, does bull case mention this contradiction?

[ ] Are price ranges consistent with stated time horizons?
    (3-day target $20K higher than current = unrealistic)

[ ] Does invalidation for one scenario align with conditions for another?

[ ] Are catalysts realistic for the time horizon?
    (Asking "Fed pivot in 3 days" is unrealistic if no FOMC scheduled)
```

QA gate: scenarios that fail self-consistency check = block.

---

## Output Render — Senior Scenario Section

```
[SCENARIOS]

BEAR CASE (X% likelihood, 90-day horizon)
   Conditions: <observable triggers>
   Price range: $A - $B
   Key levels: support breach $X; capitulation $Y
   Catalysts: <events>
   Invalidation: <observable>

SIDEWAYS CASE (Y% likelihood, 90-day horizon)
   Conditions: range-bound between $A - $B
   Catalysts to break up: <conditions>
   Catalysts to break down: <conditions>

BULL CASE (Z% likelihood, 90-day horizon)
   Conditions: <observable triggers>
   Price range: $A - $B
   Key levels: resistance $X; target $Y
   Catalysts: <events>
   Invalidation: <observable>

VERIFICATION:    X + Y + Z = 100%

[OPTIONAL — TAIL CASES]
TAIL BEAR (<10%): trigger, impact, mitigation
TAIL BULL (<10%): trigger, impact, capture mechanism
```

---

## Anti-Patterns

- **Single-number price targets**: "BTC to $100K" — replace with range.
- **Probabilities not summing to 100%**: math error or hidden tail.
- **Bull case stated first**: bias indicator; bear-first rule.
- **Probabilities feel comfortable**: probably overconfident; honest probabilities feel uncomfortable.
- **"I'm 80% confident in bull"**: rarely justifiable in crypto's uncertainty.
- **Internal contradictions**: macro contracting + bull case 60% = inconsistent.
- **No catalysts named**: scenarios without triggers are vague.
- **No invalidation**: without it, scenario can't be falsified.
- **Same scenario across all timeframes**: short / medium / long horizon scenarios should differ.
- **Forgotten decay**: stale scenarios reused = false confidence.

---

## Reference

- `companies/crypto-consultant/skills/research/SKILL.md` (Update 12 — synthesis output).
- `companies/crypto-consultant/skills/reporting/SKILL.md` (Update 12 — bear-first rendering).
- `knowledge/crypto/four-year-cycle.md` (Update 12 — phase context).
- `knowledge/crypto/risk-sizing-methods.md` (Update 12 — tail scenario library).
- `knowledge/crypto/forecast-evaluation.md` (Update 12 — calibration).
- This file establishes scenario-modeling discipline for the company; based on standard probability and forecasting practice from finance and intelligence community methodology.
