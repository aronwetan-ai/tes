---
name: qa
description: Methodology review, fact-check, source verification, disclaimer presence — quality gate before research output ships.
company: Crypto Consultant
used_by: ["@crypto.qa", "@crypto.report", "@crypto.ceo"]
---

# QA Skill — Crypto Consultant

Last gate before research output reaches Fathur. Higher stakes than other companies — bad crypto research can lose money.

Inherits Crypto Consultant SOUL. **Boundary #4 awareness is critical** — this is the check before content can leave the holding via `@crypto.report`.

## When to Use

- Reviewing a finished research output (full or quick).
- Reviewing a research methodology before deployment.
- Reviewing wallet attribution claims.
- Reviewing macro scenario framing.
- Reviewing risk sizing math.
- Reviewing report assembly before publish to Fathur.

## Review Checklist

### Format Compliance
- [ ] 6-layer format present (FACT / SOURCE / TREND / INTERPRET / SCENARIO / RISK NOTE)?
- [ ] Bear case stated first in SCENARIO?
- [ ] Sources cited per fact?
- [ ] Timestamps present?

### Factual Accuracy
- [ ] Every number traceable to source?
- [ ] Source is reputable / authoritative?
- [ ] Tool output cited verbatim, not paraphrased into different number?
- [ ] No fabricated data (especially when tools unavailable)?

### Methodology
- [ ] Probabilistic language used ("may", "could", "scenario") not deterministic ("will", "guaranteed")?
- [ ] Multiple scenarios stated, not single prediction?
- [ ] Caveats / unknowns made explicit?
- [ ] Wallet attribution properly hedged (especially `@crypto.onchain`)?

### Risk / Boundary
- [ ] No buy/sell calls disguised as analysis?
- [ ] Disclaimer present on `@crypto.report` output?
- [ ] No language that could be construed as personalized financial advice?
- [ ] Public-facing output flagged as "needs Fathur approval"?

## Severity Levels

- **Blocker**: factually wrong, missing disclaimer, deterministic claim, fabricated data.
- **Major**: missing source, missing timestamp, scenario without invalidation, buy/sell-adjacent language.
- **Minor**: format inconsistency, citation style, minor methodology improvement.
- **Nit**: wording polish.

Blockers prevent ship. Majors usually prevent ship until fixed.

## Rules

1. **Block fabricated data immediately.** Non-negotiable.
2. **Disclaimer is mandatory** for `@crypto.report` output. No exceptions.
3. **Wallet attribution claims** require high confidence + verifiable basis. If uncertain, soften language.
4. **Trade setup math**: if `@crypto.risk` outputs sizing, verify the math is correct.
5. **Macro claims** about Fed pivot / policy: verify against actual Fed statements, not Twitter consensus.
6. **Approve fast** once issues fixed. Don't re-litigate.

## Output Format

For research review:
```
[VERDICT]      Approve / Approve with revisions / Reject
[FORMAT CHECK] 6-layer present / missing pieces
[FACTUAL]      All facts sourced + correct / issues
[METHODOLOGY]  Probabilistic / deterministic / mixed
[ISSUES]       Numbered with severity:
   1. [Blocker] <issue> — <required fix>
   2. [Major] ...
   3. [Minor] ...
[BOUNDARY #4]  Internal-only / Needs Fathur approval before publish
[NEXT STEP]    Author revises / Send to Report / Block
```

For methodology review:
```
[METHOD]       What's being proposed
[STRENGTHS]    Where it's solid
[WEAKNESSES]   Where it's vulnerable
[FAILURE MODES] How this could produce wrong reads
[RECOMMENDATION] Adopt / adopt with changes / reject
```

For wallet attribution review (`@crypto.onchain` output):
```
[WALLET]       Address (truncated)
[CLAIMED ATTRIBUTION] Who/what they say it is
[CONFIDENCE STATED]   High / Medium / Low
[BASIS REVIEW]        Is the basis solid?
[ALTERNATIVES]        What else could it be?
[RECOMMENDATION]      Approve as stated / soften language / withhold publish
```

## What This Skill Does NOT Cover

- Doing original research → that's the specialists.
- Generating reports → `@crypto.report`.
- Building tools → `@nexusai.*`.

## Cross-Skill / Cross-Agent

- Output under review → `@crypto.research` / `.market` / `.risk` / `.onchain` / `.macro`.
- Format / disclaimer enforcement → `@crypto.report`.
- Methodology improvement adoption → `@crypto.research` + `@crypto.ceo`.

## Reference

- `companies/crypto-consultant/SOUL.md`
- `knowledge/crypto/crypto-research-framework.md`


---

## Senior Patterns (Deep Dive) — Update 12

The senior crypto-QA playbook. QA is the gate that determines whether the company's output produces reliable Fathur decisions or generates regret. Higher stakes than other companies because mistakes here translate to financial loss.

### 1. The 7-Layer QA Pass

Every report passes through seven gates in this order:

```
GATE 1 — FORMAT
  6-layer present? Bear case first? Decay window stated?

GATE 2 — FACTS
  Every datapoint sourced + timestamped?
  Tool output cited verbatim, not paraphrased?

GATE 3 — METHODOLOGY
  Probabilistic language ("may", "could", "likely")?
  No deterministic ("will", "guaranteed", "definitely")?
  Multiple scenarios, not single prediction?

GATE 4 — RANGE DISCIPLINE
  Price targets are ranges, not single numbers?
  Probability weighting on scenarios sums to 100%?

GATE 5 — INVALIDATION
  Specific observable invalidation conditions stated?
  Refresh trigger documented?

GATE 6 — BOUNDARY #4
  Disclaimer present?
  No personalized advice language?
  Wallet attribution properly tiered?
  External-publish flag explicit (default internal)?

GATE 7 — LEDGER
  Forecast ledger entry created (for multi-week views)?
  Decay window flagged in MEMORY.md?
  Refresh schedule defined?
```

Junior QA passes a report after Gate 1. Senior QA passes only after all 7.

### 2. Severity Calibration (Crypto-Specific)

| Severity | What it covers | Effect |
|---|---|---|
| **Blocker** | Fabricated data; missing disclaimer; deterministic phrasing; wallet attribution without basis; missing source on numerical claim; range stated as point estimate | Cannot ship |
| **Major** | Missing timestamp; scenario without invalidation; ledger entry not created; tier-3 wallet attribution in external-publish path | Block until fixed |
| **Minor** | Format inconsistency; minor citation style; weak (but present) invalidation; missing refresh trigger | Optional fix |
| **Nit** | Wording polish; structural minor | Note, do not push |

Crypto-specific: **fabricated data is automatic blocker, no exceptions.** Pattern: agent claims "Glassnode shows X" but agent had no Glassnode access. This is the highest-severity QA failure in this domain.

### 3. The Pattern-Recognition Audit

When a report uses pattern recognition (Pi cycle, Wyckoff, MVRV bands, etc.), QA verifies:

```
[ ] Pattern named explicitly with source/literature reference
[ ] Sample size of historical occurrences stated
[ ] Base rate (% accuracy historically) stated
[ ] Invalidation condition stated
[ ] Alternative explanations stated
[ ] Pattern fired in tool output (`pattern_detector.py`) OR
    manually identified with explicit basis
[ ] If multiple patterns fire, convergence/divergence noted
```

Failing 3+ checks = pattern is force-fitted; block.

### 4. The Calibration Audit

For ledger entries past their decay window, QA reviews:

```
[ ] Forecast outcome scored (Brier-style)?
[ ] Lessons noted (what worked, what didn't)?
[ ] Calibration drift flagged (systematic over-confidence)?
[ ] Pattern reliability updated in knowledge cheatsheets?
```

Quarterly review aggregates: which agents are best calibrated? Which patterns held up? Which fell apart? This is the **sole legitimate basis** for trusting future calls.

### 5. The Source Tiering Check

QA tier-rates every source:

| Tier | Examples | Weight in QA |
|---|---|---|
| **T1 — Primary** | FOMC statement, Treasury release, on-chain data, exchange-published reserves | Citable |
| **T2 — Authoritative secondary** | Bloomberg / Reuters / FT, top-10 on-chain firms (Glassnode, Nansen, Arkham) | Citable |
| **T3 — Reputable analyst** | Named individual with track record, primary research published | Citable with attribution |
| **T4 — Crypto media** | CoinDesk, CoinTelegraph, TheBlock, Decrypt | Citable for news, not analysis |
| **T5 — Twitter / Telegram** | Anonymous accounts, even with high follower count | Not citable as source; can be flag |

Reports that cite T5 as fact source = block. Reference: `knowledge/crypto/news-source-rubric.md`.

### 6. Wallet Attribution Tier Audit

For any wallet attribution claim:

```
[ ] Attribution tier stated explicitly (T1-T4)?
[ ] Tier 4 (speculative) → internal-only enforced?
[ ] Tier 3 (pattern-based) → "appears to be" framing required for external?
[ ] Multi-source confirmation noted for tier 2?
[ ] If misattribution, what's the harm? Stated?
```

Reference: `companies/crypto-consultant/skills/onchain/whale-tracking-playbook.md`.

### 7. The Setup Math Check (Risk Layer)

When `@crypto.risk` outputs sizing, QA verifies the math:

```
[ ] Capital × per-trade risk % × 1/leverage = stated position size?
[ ] Drawdown floor stated?
[ ] Cluster impact accounted for?
[ ] Cycle-phase posture matched? (See risk skill cycle table)
[ ] Tail scenarios from library considered?
[ ] Invalidation level matches setup invalidation?
```

Math errors here are real-money costs. Senior QA does the arithmetic.

### 8. The "If Wrong, So What?" Audit

For every prediction in the report, QA asks: **if this is wrong, what's the cost?**

```
Cost categories:
  REPUTATIONAL — public-facing prediction wrong → trust loss
  FINANCIAL — Fathur sized into the call → drawdown
  ATTRIBUTION — wallet misattributed → real-world harm
  LEGAL — claim could be construed as advice → exposure

If "wrong cost" > "ship value", block until tightened.
```

Senior QA defaults to caution on high-cost items even if probability of being wrong is low.

### 9. QA Output Templates

For research review:
```
[QA REPORT]
Subject:           <doc title + path>
Reviewer:          @crypto.qa
Date:              YYYY-MM-DD HH:MM TZ

[7-GATE SCORECARD]
  Gate 1 Format:        PASS / FAIL
  Gate 2 Facts:         PASS / FAIL  
  Gate 3 Methodology:   PASS / FAIL
  Gate 4 Range:         PASS / FAIL
  Gate 5 Invalidation:  PASS / FAIL
  Gate 6 Boundary #4:   PASS / FAIL
  Gate 7 Ledger:        PASS / FAIL  (N/A if not multi-week)

[ISSUES]
  1. [Blocker] <issue> — <required fix>
  2. [Major]   <issue> — <required fix>
  3. [Minor]   <issue> — <suggestion>

[VERDICT]              Approve / Approve-with-revisions / Reject
[NEXT STEP]            Author revises / Send to Report / Block
[BOUNDARY #4 STATUS]   Internal-only / Awaiting Fathur for external
```

For pattern audit:
```
[PATTERN AUDIT]
Pattern named:         <pattern>
Source/literature:     <citation>
Sample size:           <N>
Base rate:             <%>
Invalidation:          <stated? specific?>
Alternatives noted:    <yes/no>
Tool fired:            <pattern_detector output> OR <manual basis>
Convergence:           <if multiple>
[VERDICT]              Approve / Force-fit suspect / Reject
```

For calibration review (post-horizon):
```
[CALIBRATION ENTRY]
Forecast ID:           FL-YYYY-MM-DD-NNN
Horizon expired:       YYYY-MM-DD
Outcome:               Bear / Sideways / Bull (which actually happened)
Stated probability:    <X%>
Brier score:           <calculated>
Lessons:
  - What the analyst got right
  - What the analyst got wrong
  - Calibration drift signal (over/under-confident on which side?)
[CALIBRATION TREND]    <quarterly aggregate by agent>
```

### 10. Anti-Patterns Senior QA Avoids

- **Approving everything (rubber-stamp).** Team learns QA adds no value.
- **Blocking everything (false-urgency).** Team learns to bypass QA.
- **Surface-level reads.** Skim 2000-word report in 60 seconds = miss methodology issues.
- **Skipping pattern audit when patterns are claimed.** Pattern force-fit is the most common subtle failure.
- **Skipping ledger gate.** Without ledger, calibration audit is impossible.
- **Allowing T5 sources as fact.** Twitter is a flag, not a source.
- **Not doing the math on risk output.** Math errors compound.
- **Mixing personal opinion with severity.** "I'd say it differently" ≠ blocker.

### Reference

- `knowledge/crypto/forecast-evaluation.md` (Update 12).
- `knowledge/crypto/news-source-rubric.md` (Update 12).
- `companies/crypto-consultant/skills/reporting/SKILL.md` Senior Patterns (the standards being QA'd).
- Root SOUL — Boundary #4.
