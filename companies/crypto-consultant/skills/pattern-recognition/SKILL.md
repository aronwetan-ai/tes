---
name: pattern-recognition
description: Identify recurring patterns in price, on-chain, derivatives, macro data — 4Y halving cycle, Pi top, Wyckoff, MVRV bands, divergences. Distinguish recognition from force-fitting.
company: Crypto Consultant
used_by: ["@crypto.market", "@crypto.onchain", "@crypto.macro", "@crypto.research", "@crypto.risk"]
---

# Pattern Recognition Skill — Crypto Consultant

The skill that turns the 4-year cycle, on-chain bands, and recurring formations from "story" into operational pattern detection backed by base rates and invalidation conditions.

Inherits Crypto Consultant SOUL. **Hardest discipline in this domain** — the line between recognition (pattern is in the data) and force-fitting (pattern is in the analyst's head) is where most crypto research fails.

## When to Use

- "Where are we in the cycle?"
- "Has this pattern fired historically?"
- "What does the [Pi cycle / MVRV / Wyckoff / etc.] say?"
- Any setup that names a pattern.
- Any cycle-position read.
- Convergence checks across multiple patterns.
- Audit of pattern claims by other agents.

## Core Discipline (Three Guards)

Every pattern claim must pass **all three** guards:

### Guard 1 — Pattern Has a Name and a Source

Not "I see a head-and-shoulders" — but "Wyckoff distribution Schematic 1, per Wyckoff (1931), with PSY → BC → AR → ST → SOW → LPSY → UTAD → SOW2".

Patterns without literature reference, without explicit named structure, without source = not patterns; they are vibes. Reject.

### Guard 2 — Base Rate Stated

Every pattern claim states:
- **Sample size** — how many historical occurrences.
- **Hit rate** — % of times pattern resolved as expected.
- **Failure rate** — % of times pattern invalidated.
- **Time to resolution** — typical window for confirmation.

Example: "Pi cycle top has fired 3 times historically (2013, 2017, 2021). Each time it called the cycle top within ±3 days. Sample size N=3 across 3 cycles. NOT statistically significant — directional only, not predictive."

Stating low base rate is honest. Hiding it is not.

### Guard 3 — Invalidation Stated Before Confirmation

Before stating "pattern X is firing," state "pattern X invalidates if Y."

- Pi cycle invalidation: 111-DMA fails to cross 350-DMA × 2.
- Wyckoff accumulation invalidation: price breaks below the spring low on volume.
- Mayer Multiple low invalidation: price moves above 1.0 without confirming structure.

Without invalidation, "pattern X is firing" is a hope, not a read.

## When Patterns Are Force-Fit

Common signs:

| Sign | Why it's force-fitting |
|---|---|
| Multiple patterns "all" point one way | Reality usually has divergent signals |
| Pattern definition stretched to fit current data | "Sort of like a head-and-shoulders" = no head-and-shoulders |
| Invalidation conditions vague | "It's still valid because [excuse]" |
| No sample size mentioned | Can't be evaluated |
| Pattern fires on every chart in your portfolio | You're seeing what you want to see |
| Pattern conveniently confirms your prior | Always check: would you call this if you held the opposite position? |

**Senior antidote**: when a pattern jumps out, write down the bear case for the pattern. If you can't construct a coherent counter-read, you're force-fitting.

## The Pattern Library (Cycle-Tier)

| Pattern | Domain | Tool flag | Reliability |
|---|---|---|---|
| 4-year halving cycle phase | Cycle | `pattern_detector.py --pattern cycle_phase` | Strong (3 cycles) |
| Pi cycle top | Price | `--pattern pi_top` | High but N=3 |
| 200W MA bottom touch | Price | `--pattern btc_bottom` | Strong (every cycle) |
| Mayer Multiple <1 / >2.4 | Price | `--pattern mayer_low/high` | Strong as zones |
| Golden cross / death cross | Price | `--pattern golden_cross / death_cross` | Moderate |
| MVRV-Z extremes | On-chain | `--pattern mvrv_zone` | Strong as zones |
| Realized HODL / RHODL | On-chain | `--pattern rhodl` | Strong as zones |
| NUPL extremes | On-chain | `--pattern nupl` | Strong as zones |
| Difficulty ribbon compression | On-chain | manual or paid data | Moderate |
| Funding rate extreme | Derivatives | `funding_rates.py` | Short-horizon |

Reference: `knowledge/crypto/cycle-indicators.md` for the full library + base rates.

## The Pattern Library (Structural / TA)

| Pattern | Domain | Reliability | Notes |
|---|---|---|---|
| Wyckoff accumulation (Schematic 1, 2) | Structure | Moderate-high | Slow; requires patience to read |
| Wyckoff distribution | Structure | Moderate-high | Mirror of accumulation |
| Range top / range bottom test | Structure | High at zone | Volume confirmation required |
| Bull flag / bear flag | Continuation | Moderate | Volume + RSI confirms |
| Head and shoulders | Reversal | Moderate | Often force-fit; high standard required |
| Cup and handle | Continuation | Low-moderate | Often force-fit |
| Falling wedge | Reversal | Moderate | Requires breakout volume |
| Symmetrical triangle | Continuation | Low | Often resolves opposite to "obvious" direction |
| Diverging RSI / MACD | Momentum | Moderate | Higher signal at multi-timeframe alignment |
| Volume profile node test | Structure | High at HVN | Heavy-volume node = real S/R |

Reference: `knowledge/crypto/wyckoff-method.md`.

## The Pattern Library (On-Chain Specific)

| Pattern | Description | Mechanism |
|---|---|---|
| LTH supply rising | Long-term holder supply increasing | Smart money accumulating |
| Exchange supply falling | Coins leaving exchanges | Shift to self-custody = bullish |
| Stablecoin issuance surge | New stable mints | Buy-side dry powder |
| Hashrate ATH | Network hash power peaks | Miner confidence |
| Difficulty ribbon compression | Miner cost convergence | Pre-recovery signal |
| Whale accumulation (>1k BTC wallets growing) | Top cohort buying | Cycle-bottom signal |
| Realized profit/loss extremes | Cohort PnL state | Capitulation or euphoria |

## The Pattern Library (Macro Specific)

| Pattern | Description | Crypto implication |
|---|---|---|
| Yield curve un-inverting | 2s10s normalizing after inversion | Recession risk window |
| DXY breakdown | $ index breaking trend | Liquidity tailwind |
| M2 reflation | Global M2 expanding YoY | Cycle accelerator (12wk lag) |
| Fed pivot signal | First explicit dovish shift | Risk-on regime change |
| Real yield rollover | TIPS yield falling from peak | Risk asset bid |
| Equity correlation collapse | BTC/NDX rolling correlation drops | Crypto-native catalyst dominant |

Reference: `knowledge/crypto/global-liquidity.md`.

## Convergence Logic

Single-pattern reads are weak. Senior pattern recognition checks **convergence**:

```
LEVEL 1 — Single pattern fires           = note, low confidence
LEVEL 2 — 2 patterns same domain agree   = moderate confidence
LEVEL 3 — 2+ patterns across domains agree = high confidence
LEVEL 4 — All 3 lenses (price+on-chain+derivatives) align = highest

PLUS macro regime check:
   Pattern firing aligned with macro regime = stronger
   Pattern firing against macro regime     = weaker, often early
```

Cycle bottoms historically converge: BTC near 200W MA + MVRV-Z<0 + capitulation funding + LTH accumulating + Mayer<1 + on-chain capitulation = high confidence cycle floor zone.

Cycle tops historically converge: Pi cycle fires + MVRV-Z>7 + euphoria funding + LTH distributing + Mayer>2.4 + on-chain euphoria = high confidence cycle top zone.

When 5/6 indicators agree but 1 disagrees, the disagreement is the alpha — it tells you what could be different this time.

## Output Format

For pattern call:

```
[PATTERN NAME]      Specific named pattern
[SOURCE/LITERATURE] Where the pattern is defined (book / paper / convention)
[DOMAIN]            Cycle / Structure / On-chain / Macro / Derivatives

[BASE RATE]
  Sample size:      N occurrences historically
  Hit rate:         X% resolved as expected
  Failure rate:     Y% invalidated
  Resolution time:  typical window in days/weeks

[CURRENT STATE]
  Tool firing:      pattern_detector.py output OR manual basis
  Current value:    specific datapoint
  Threshold:        what triggers the pattern
  Triggered at:     YYYY-MM-DD timestamp

[INVALIDATION]
  Specific level / condition.
  Observable. Not "if it doesn't work."

[CONFIRMATION]
  What additional data confirms the pattern is playing out as expected.

[ALTERNATIVES]
  What else this data could be (other valid reads).
  If only one read fits, you're force-fitting.

[CONVERGENCE]
  Other patterns currently agreeing (cite each).
  Other patterns currently disagreeing (cite each).
  Net confidence: low / moderate / high.

[VERDICT]
  Pattern firing as recognized: YES / NO / DEVELOPING
  Confidence: low / moderate / high
  Action implication: <not advice; what changes about the read>

[BOUNDARY #4]
  Pattern claim publishable as-is: YES / NO / Needs Fathur approval
```

For convergence audit:

```
[CONVERGENCE AUDIT — Cycle Position Read]
Issued:           YYYY-MM-DD
Cycle phase claim: <phase>

[PATTERNS IN AGREEMENT]
  1. Pi cycle status:        <state>
  2. MVRV-Z zone:            <zone>
  3. Mayer Multiple zone:    <zone>
  4. LTH supply trend:       <state>
  5. Funding regime:         <state>
  6. Macro liquidity:        <state>

[PATTERNS DISAGREEING]
  1. <pattern>:              <state, why disagrees>

[NET READ]
  Convergence level:         L1 / L2 / L3 / L4
  Confidence:                low / moderate / high
  Phase confidence:          high / moderate / low

[WHAT WOULD CHANGE THE READ]
  Specific observable conditions.
```

## Cross-Skill / Cross-Agent

- Price-side pattern firing → `@crypto.market`.
- On-chain pattern firing → `@crypto.onchain`.
- Macro pattern firing → `@crypto.macro`.
- Combined cycle synthesis → `@crypto.research`.
- Risk implication of patterns → `@crypto.risk`.
- Pattern claim audit (force-fit detection) → `@crypto.qa`.
- Tool execution → `pattern_detector.py`.

## What This Skill Does NOT Cover

- Position sizing → `@crypto.risk` + `skills/risk`.
- News-pattern recognition → `@crypto.research` + news_scraper output.
- Final report assembly → `@crypto.report` + `skills/reporting`.

## Reference

- `knowledge/crypto/four-year-cycle.md` (Update 12).
- `knowledge/crypto/cycle-indicators.md` (Update 12).
- `knowledge/crypto/wyckoff-method.md` (Update 12).
- `knowledge/crypto/onchain-metrics-glossary.md` (Update 12).
- `knowledge/crypto/derivatives-glossary.md` (Update 12).
- `knowledge/crypto/global-liquidity.md` (Update 12).
- `knowledge/crypto/forecast-evaluation.md` (Update 12 — calibration tracking for pattern reliability).
- `tools/pattern_detector.py` (Update 12).
- `companies/crypto-consultant/skills/market-analysis/SKILL.md` Senior Patterns.
- `companies/crypto-consultant/skills/onchain/SKILL.md` Senior Patterns.

---

## Senior Patterns (Deep Dive) — Update 12

This skill is itself the deep-dive pattern; the section below is the senior-level "how to operate this skill" rather than another extension.

### 1. The Pattern-Recognition Workflow

```
STEP 1: Define the question
        What pattern are we looking for? Why now?

STEP 2: Pull data
        price_scraper.py for OHLCV
        onchain_metrics.py for on-chain
        funding_rates.py for derivatives
        Manual macro data if needed

STEP 3: Run pattern_detector.py with relevant flags
        Get current state of all in-library patterns

STEP 4: Apply three guards (name + source / base rate / invalidation)
        Reject any pattern that fails any guard

STEP 5: Convergence audit
        Which patterns agree? Which disagree?
        Disagreement matters — surface it

STEP 6: Output in structured format above

STEP 7: File ledger entry if multi-week prediction
        (forecast ledger in MEMORY.md)
```

### 2. Calibration as the Long Game

After each cycle, audit which patterns held up and which didn't:

```
[POST-CYCLE PATTERN AUDIT]
Cycle:                   2024-2026 cycle
Cycle bottom date:       <verified post-fact>
Cycle top date:          <verified post-fact>

[PATTERNS THAT WORKED]
  1. Pi cycle top fired at $XXX, top at $YYY (within Z days)
  2. ...

[PATTERNS THAT MISSED]
  1. ...

[PATTERNS WITHOUT CLEAR SIGNAL]
  1. ...

[TAKEAWAYS]
  - Adjust reliability ratings in cycle-indicators.md
  - Update knowledge/crypto/forecast-evaluation.md
```

This post-cycle review is the **only honest basis** for trusting next cycle's patterns. Without it, the team's pattern faith is just survivorship bias.

### 3. The Anti-Force-Fit Self Check

Before publishing a pattern claim, run the self check:

```
[ ] Could I write a coherent bear-case for this same data?
[ ] If I held the opposite position, would I still see this pattern?
[ ] Have I stated invalidation specifically?
[ ] Have I stated alternatives explicitly?
[ ] Is base rate disclosed honestly (even if low)?
[ ] Is convergence stated, including disagreement?
[ ] Am I citing tool output OR explicit manual basis?
```

If any answer is no, the read is not yet senior-grade.

### 4. Anti-Patterns

- **Naming patterns nobody else recognizes.** Pattern recognition is shared vocabulary; if you invented the pattern, that's fine but state it as your construction.
- **Hiding low base rates.** N=3 is N=3; say so.
- **Promoting Pi cycle (or any pattern) past its evidence.** "Has fired 3 times" ≠ "will fire again."
- **Treating fractals/Elliott as predictive.** They're descriptive; subjective; calibration is poor.
- **Dismissing disagreement.** When patterns conflict, the conflict is the read.
- **Publishing pattern claims as advice.** Pattern recognition feeds analysis; analysis feeds Fathur decisions; Fathur decides. Boundary #4.
