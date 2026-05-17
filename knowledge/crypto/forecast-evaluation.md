# Forecast Evaluation — Crypto Knowledge Cheatsheet

Versi: 1.0 (Update 12)
Last updated: 2026-05-17
Audience: Crypto Consultant — `@crypto.research`, `@crypto.qa`, `@crypto.ceo`, all forecasting agents

---

## Why This File

The single biggest separator between honest research and selective memory is **calibration tracking**: do our forecasts perform as confidently stated? Without honest evaluation, the team's pattern faith is just survivorship bias.

This file is the canonical reference for evaluating predictions, scoring calibration, and updating reliability ratings on indicators.

---

## The Forecast Ledger Discipline

Every multi-week-horizon view goes into `companies/crypto-consultant/MEMORY.md` under `[FORECAST LEDGER]`:

```
[FORECAST LEDGER ENTRY]
ID:               FL-2026-05-17-001
Issued:           2026-05-17 09:00 UTC
Issuer:           @crypto.research
Horizon:          90 days
Decay:            2026-08-15

Cycle phase:      Phase 3 — Markup post-halving (confidence: high)
Lens convergence: PARTIAL — price+derivatives bullish, on-chain mixed

Stated scenarios:
  Bear:     20%, range $40K-$55K
  Sideways: 35%, range $58K-$72K
  Bull:     45%, range $76K-$110K

Key levels:       BTC bull >$76K confirms; bear <$58K invalidates
Key catalysts:    Fed June meeting; ETF flow re-acceleration
Invalidation:     Sustained <$58K with on-chain net inflow >50k BTC
                  to exchanges over 14d

Tracked:          Yes — full report at <path>
Reviewed:         [post-horizon evaluation field — filled at 2026-08-15]
```

Six months of ledger entries reveal:
- Which agents call cycles well
- Which patterns the team over-trusts
- Where the team's calibration is honest vs hopeful

---

## Brier-Style Scoring

After horizon expires, each forecast scored:

```
For each scenario (Bear / Sideways / Bull):
  Stated probability:    P_i (e.g. 0.20, 0.35, 0.45)
  Actual outcome:        O_i (1 if happened, 0 if not)
  Score per scenario:    (P_i - O_i)²
  
Brier score = mean of scores across all scenarios
            = sum((P_i - O_i)²) / N

Lower Brier = better calibrated.
Perfect calibration = 0.
Random guessing = ~0.25.
```

**Example**:
- Stated: Bear 20% / Sideways 35% / Bull 45%
- Actual: Bull happened (Bull = 1, others = 0)
- Bear score: (0.20 - 0)² = 0.04
- Sideways score: (0.35 - 0)² = 0.1225
- Bull score: (0.45 - 1)² = 0.3025
- Brier = (0.04 + 0.1225 + 0.3025) / 3 = 0.155

Interpretation: moderate-good calibration. The 45% bull stated was less than the realized outcome (bull happened); ledger shows under-confidence in the bull case. Adjust priors next time.

---

## Calibration Curves

Plot stated probability vs actual frequency over many forecasts:

```
If team is well-calibrated:
   Stated 20% → ~20% actually happen
   Stated 50% → ~50% actually happen
   Stated 80% → ~80% actually happen

Common biases:
   Over-confident bull: stated 60%+ bull happens 40%
   Under-confident bear: stated 30% bear happens 50%
   Anchoring on midcase: stated 40-50% sideways always
```

After 6+ months of ledger entries, calculate:
- Per-agent calibration curve
- Per-pattern calibration (does Pi cycle calling actually correlate?)
- Per-cycle-phase calibration (are we worse at Phase 4 calls?)

---

## Track Record Discipline

`companies/crypto-consultant/MEMORY.md` maintains a permanent `[FORECAST LEDGER]` section:

```
[FORECAST LEDGER]

Active Forecasts:
  FL-2026-05-17-001  @crypto.research  90d  decay 2026-08-15  STATUS: tracking
  FL-2026-05-12-002  @crypto.market    14d  decay 2026-05-26  STATUS: tracking
  ...

Decayed Forecasts (post-horizon, scored):
  FL-2026-02-10-005  @crypto.research  90d  Brier 0.18  Bull 50% (under)  
                     Lessons: Underweighted ETF flow impact; pattern recognition
                              missed institutional inflow regime change
  ...

Quarterly Aggregate:
  Q1 2026:  10 forecasts, mean Brier 0.21, top performer @crypto.market (0.15)
  Q2 2026:  ...
```

This is non-negotiable for senior research. Reports without ledger entries = unauditable.

---

## Pattern-Specific Calibration

For each cycle indicator (Pi cycle, Mayer, MVRV-Z, etc.), maintain:

```
[PATTERN CALIBRATION RECORD]

Indicator: Pi Cycle Top
Sample size: 4 (after current cycle resolves)
Hits: TBD (3 of 3 prior cycles)
Misses: TBD
Reliability tier: B → A or A → B (adjust based on cycle 4 outcome)

Indicator: MVRV-Z >7
Sample size: 3 cycle tops
Hits: 2 (within 30 days), 1 (close)
Reliability tier: A

Indicator: Stock-to-Flow
Sample size: 4
Hits: 2 (cycle 1, 2)
Misses: 2 (cycle 3 broke down badly)
Reliability tier: D — deprecated as predictive
```

These ratings update post-cycle and feed into `cycle-indicators.md`.

---

## Honest Failure Documentation

When a forecast fails badly:

```
[POST-MORTEM ENTRY]

Forecast ID:        FL-XXXX
Issuer:             @crypto.X
Stated:             [probabilities, levels, conditions]
Actual:             [what happened]
Brier:              <score>

What went wrong:
  - Specific analytical errors
  - Pattern misread
  - Macro overlay missed
  - Data source error
  - Timing error
  - Bias-driven (confirmation, recency, anchoring)

Lessons:
  - Specific changes to method
  - Updates to indicator reliability ratings
  - Updates to source tier weights

Action items:
  - [ ] Update knowledge file X
  - [ ] Adjust QA checklist
  - [ ] Update agent SOUL if behavioral change needed
```

These post-mortems are the company's institutional memory. Skipping them = repeating mistakes.

---

## Common Calibration Failures

### Over-Confidence in Bull Cases
**Pattern**: Industry-wide bull bias. Average Brier on bull-leaning forecasts often 0.25-0.35 (poor).

**Mitigation**:
- Cap any bull-case probability at 60% unless multi-lens convergence + macro alignment
- Bear-first rendering forces honest weighing
- Quarterly bull-bias audit per agent

### Under-Confidence in Capitulation
**Pattern**: At cycle bottoms, team often under-weights the bear case continuing despite indicators flashing.

**Mitigation**:
- During Phase 5, calibration audit explicitly checks bear weighting
- Reference 200W MA + MVRV-Z bottom signals as ANCHORS, not GUARANTEES

### Recency Bias
**Pattern**: Last week's action dominates next-week forecast.

**Mitigation**:
- Forecasts must explicitly address conditions across multiple timeframes
- "Last 7 days" and "Last 30 days" as separate inputs

### Cycle-Position Confusion
**Pattern**: Team identifies wrong cycle phase, all subsequent forecasts inherit error.

**Mitigation**:
- Cycle phase confidence stated explicitly (high/moderate/low)
- Convergence audit uses multiple indicators
- Disagreement among indicators flagged

### Survivorship Bias on Patterns
**Pattern**: Team remembers patterns that worked; forgets ones that failed.

**Mitigation**:
- Pattern calibration record (Section above)
- Deprecated patterns (S2F) explicitly listed
- Any new pattern must establish base rate before being used

---

## Quarterly Research Review

Every quarter:

```
[QUARTERLY REVIEW — Q[N] YYYY]
Date:                 YYYY-MM-DD

[FORECAST LEDGER STATS]
  Total forecasts:    N
  Decayed:            X (scored)
  Active:             Y
  Mean Brier:         <score>
  Best performer:     @crypto.X (Brier <score>)
  Worst performer:    @crypto.Y (Brier <score>)

[CALIBRATION DRIFT]
  Bull-bias check:    <state>
  Bear-bias check:    <state>
  Cycle-phase confusion incidents: <count>

[PATTERN PERFORMANCE]
  Tier A indicators: did they hold up?
  Tier B indicators: any move to A or C?
  Deprecated additions: any new failures?

[LESSONS APPLIED]
  Knowledge files updated:
  Agent SOULs adjusted:
  QA checklist additions:

[NEXT QUARTER FOCUS]
  Areas to improve.
```

This review is owned by `@crypto.ceo` and `@crypto.qa`.

---

## The "What Would Falsify This" Check

For every forecast, before shipping:

```
What observable conditions, if they occurred, would falsify this view?
If you cannot answer specifically, the view is unfalsifiable = vibe.

Examples of unfalsifiable views:
  - "BTC will eventually reach $X" (no time horizon = unfalsifiable)
  - "Crypto adoption will continue" (no specifics = vacuous)
  - "Pattern X is bullish" (no metric = unauditable)

Senior versions:
  - "BTC reaches $90K-$110K within 90 days at 45% probability;
     falsified if BTC closes <$58K weekly with on-chain net inflow >50k BTC"
```

QA enforces this check.

---

## Anti-Patterns

- **No ledger entry**: forecast cannot be evaluated post-hoc.
- **Vague invalidation**: "if conditions change" — not observable.
- **Probability without horizon**: "70% bullish" without time = unfalsifiable.
- **Selective memory**: "I called the top!" without showing all the misses.
- **Ignoring failed patterns**: Stock-to-Flow worship post-2022 = bad faith.
- **No quarterly review**: institutional memory atrophies.
- **No post-mortem on big misses**: repeated mistakes likely.
- **Adjusting probabilities mid-horizon "to be right"**: cheating; original entry stays.
- **Bull-bias unchecked**: industry-wide tendency must be actively countered.

---

## Reference

- `companies/crypto-consultant/SOUL.md` Prediction Discipline (Update 12).
- `companies/crypto-consultant/skills/research/SKILL.md` Senior Patterns (Forecast Ledger).
- `companies/crypto-consultant/skills/qa/SKILL.md` Senior Patterns (calibration audit).
- `knowledge/crypto/scenario-modeling.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12 — pattern reliability ratings).
- This file establishes calibration discipline based on Tetlock's "Superforecasting" tradition + standard Brier scoring; content paraphrased for licensing compliance.
