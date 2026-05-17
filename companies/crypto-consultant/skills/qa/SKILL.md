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
