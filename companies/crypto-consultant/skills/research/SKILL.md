---
name: research
description: Synthesis-layer research using 6-layer format. Pulls market / on-chain / macro / risk into one coherent read.
company: Crypto Consultant
used_by: ["@crypto.research", "@crypto.ceo", "@crypto.report"]
---

# Research Skill — Crypto Consultant

Synthesis layer. Take inputs from market, on-chain, macro, risk specialists and produce one coherent read.

Inherits Crypto Consultant SOUL (analyst-cautious, data-first, skeptical, separates fact from interpretation). Output discipline = 6-layer format, mandatory.

## When to Use

- "What's crypto saying right now?" type questions.
- Multi-signal synthesis (technicals + on-chain + macro + risk).
- Cycle phase reading.
- Pre-decision research brief for Fathur.
- Research sanity check before report assembly.

## Default Process

1. **Pull active tools first.** `fear_greed.py` always runs for sentiment baseline.
2. **Identify what's needed.** Sentiment? Technicals? Flows? Macro? Risk? All?
3. **Pull specialists** as needed:
   - `@crypto.market` → technicals, structure, cycle.
   - `@crypto.onchain` → wallet flows, supply.
   - `@crypto.macro` → DXY, Fed, equities.
   - `@crypto.risk` → drawdown, position sizing, tail.
4. **Cross-check signals**: convergence (agree) vs divergence (conflict). State both.
5. **Apply 6-layer format**.
6. **Self-review**: bear case represented? sources cited? timestamps? disclaimer note for Report?
7. **Hand to `@crypto.report`** if formal deliverable.

## Rules

1. **6-layer format mandatory** for full research output.
2. **Source every fact.** No "I read somewhere".
3. **Time-stamp every datapoint.** Crypto moves; stale data is wrong data.
4. **Probabilistic, never deterministic.** Scenarios + likelihood, not predictions.
5. **Bear case before bull case.** Always.
6. **Cite which specialist provided which input.** Transparency over false confidence.
7. **"Mixed signal" is a valid conclusion.** Don't force a thesis.
8. **No buy/sell calls.** We give scenarios + risks; Fathur decides.

## Output Format — 6 Layers (Per `knowledge/crypto/crypto-research-framework.md`)

```
[FACT]
- Specific data points, with numbers.
- Multiple sources combined here, kept distinct.

[SOURCE]
- Each fact tagged to source + timestamp.
- Tool name + version if internal tool.

[TREND]
- Pattern across 7-day / 30-day / 90-day window as relevant.
- Convergence / divergence noted.

[INTERPRET]
- What the pattern typically means.
- Where signals agree / diverge.
- Caveats explicit.

[SCENARIO]
- Bull / sideways / bear with relative likelihood.
- Bear case stated FIRST.

[RISK NOTE]
- What invalidates the read.
- What we don't know.
- Macro / event risk.
```

## Quick Read Format (For Fast Questions)

```
[QUICK READ]    1-2 sentence summary
[FACT]          Key 3-5 datapoints (with timestamps + sources)
[INTERPRET]     What it means
[RISK NOTE]     What could break it
```

## Tools (Per `knowledge/tools/tool-registry.md`)

**Active**:
- `fear_greed.py` — always run for sentiment context.

**PLANNED** (mention if needed, don't fabricate):
- `btc_price.py`
- `news_sentiment.py`

## Cross-Skill / Cross-Agent

- Charts / structure → `@crypto.market`.
- Wallet flows / on-chain → `@crypto.onchain`.
- Macro overlay → `@crypto.macro`.
- Risk sizing / scenarios → `@crypto.risk`.
- Final formatted report + disclaimer → `@crypto.report`.
- Methodology / fact-check review → `@crypto.qa`.
- Long-form documentation → `@crypto.writer`.

## What This Skill Does NOT Cover

- Doing every analysis myself — synthesis pulls from specialists.
- Buy / sell signals — never.
- Public-facing publish — that's gated by `@crypto.ceo` + Fathur (Boundary #4).

## Reference

- `companies/crypto-consultant/SOUL.md`
- `companies/crypto-consultant/agents/research.md`
- `knowledge/crypto/crypto-research-framework.md`


---

## Senior Patterns (Deep Dive) — Update 12

The senior research-synthesis playbook. Synthesis is where individual lens reads (price, on-chain, derivatives, macro) become a coherent view — and where most amateur research falls apart by stitching signals that disagree into a forced conclusion.

### 1. The 3-Lens Convergence Test

Before shipping any multi-week view, run the convergence test:

```
Lens 1 — PRICE / TA          (skills/market-analysis + pattern_detector.py)
Lens 2 — ON-CHAIN            (skills/onchain + onchain_metrics.py)
Lens 3 — DERIVATIVES         (funding_rates.py + market-analysis)

For each lens, what does it say? bull / sideways / bear?

CONVERGENCE (3/3 agree)         → high-confidence single thesis
PARTIAL (2/3 agree)             → moderate-confidence with named caveat
DIVERGENCE (1/1/1 each different) → "mixed signal" IS the read
```

Senior synthesis explicitly **labels** the convergence state. Junior synthesis hides divergence by leaning on the lens that agrees with the analyst's prior.

Plus the two ambient layers:
- **Macro liquidity** — the regime under which all three lenses operate.
- **News / narrative** — what's actually moving sentiment this week.

### 2. The Forecast Ledger

Every multi-week view goes into `companies/crypto-consultant/MEMORY.md` under `[FORECAST LEDGER]`:

```
[FORECAST LEDGER ENTRY]
ID:               FL-2026-05-17-001
Issued:           2026-05-17 09:00 UTC
Issuer:           @crypto.research
Horizon:          90 days (decay 2026-08-15)
Cycle phase:      Phase 3 — Markup post-halving (confidence: high)
Lens convergence: PARTIAL — price+derivatives bullish, on-chain mixed
View summary:    Bull 45 / Sideways 35 / Bear 20
Key levels:       BTC bull >$76K confirms; bear <$58K invalidates
Key catalysts:    Fed June meeting; ETF flow re-acceleration
Invalidation:     Sustained <$58K with on-chain net inflow >50k BTC
                  to exchanges over 14d
Reviewed at:      Post-event refresh required
```

Six months of ledger entries reveal:
- Which agents call cycles well.
- Which patterns the team over-trusts.
- Where the team's calibration is honest vs hopeful.

This is the **single biggest separator** between honest research and selective memory.

### 3. Calibration Discipline (Brier-Style Scoring)

For each forecast in the ledger, score after horizon expires:

```
Stated probability of outcome that occurred:
  Bull called at 45% → bull happened     → score: 0.45 (low Brier loss)
  Bull called at 90% → bull didn't happen → score: 0.10 (high Brier loss)
```

Lower Brier = better calibrated. Track quarterly. Discuss in monthly research review:
- "Are we systematically over-confident on bull calls?" (Common bias.)
- "Are bear calls under-weighted because they're unpopular?" (Also common.)

Reference: `knowledge/crypto/forecast-evaluation.md`.

### 4. Synthesis Output Template (Senior)

```
[SYNTHESIS — Crypto Consultant Research]
Forecast ID:        FL-YYYY-MM-DD-NNN
Issued:             YYYY-MM-DD HH:MM TZ
Decay window:       N days
Cycle phase read:   <phase> — confidence <H/M/L>

[LENS READS]
  Price/TA:         <bull/sideways/bear> — basis: ...
  On-chain:         <bull/sideways/bear> — basis: ...
  Derivatives:      <bull/sideways/bear> — basis: ...
  Macro liquidity:  <expanding/neutral/contracting> — basis: ...
  Narrative:        <dominant story> — strength: ...

[CONVERGENCE STATE]   3/3 agree | 2/1 split | full divergence

[6-LAYER OUTPUT]
[FACT]
[SOURCE]
[TREND]
[INTERPRET]
[SCENARIO] (bear first; ranges + probabilities)
[RISK NOTE]

[INVALIDATION]      Specific observable conditions
[REFRESH TRIGGER]   What would force early review before decay
```

### 5. Anti-Patterns Senior Synthesis Avoids

- **Stitching disagreeing lenses into a forced thesis.** Mixed signal is a real conclusion.
- **Using single-number price targets.** Range required. "$100K" ≠ "$90K-$110K with 35% likelihood".
- **Quoting prior cycles as guarantees.** Cycles rhyme; don't repeat. Always state "if pattern repeats" caveat.
- **Forecast without invalidation.** Without it, it's not a forecast — it's hope.
- **Forgetting decay.** Stale views poison new synthesis if not flagged.
- **Skipping the ledger.** Untracked forecasts produce dishonest self-assessment.
- **Confirmation bias by source selection.** "I read 3 bullish takes; consensus is bullish" — but 3 bears were filtered out unconsciously.

### Reference

- `knowledge/crypto/scenario-modeling.md` (Update 12).
- `knowledge/crypto/forecast-evaluation.md` (Update 12).
- `knowledge/crypto/four-year-cycle.md` (Update 12).
- `companies/crypto-consultant/skills/pattern-recognition/SKILL.md` (Update 12).
- `tools/pattern_detector.py` (Update 12).
