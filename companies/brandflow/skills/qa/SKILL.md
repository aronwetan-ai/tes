---
name: qa
description: Content review for brand voice, accuracy, KPI fit, channel appropriateness — before publish.
company: BrandFlow
used_by: ["@brandflow.qa", "@brandflow.cmo", "@brandflow.community"]
---

# QA Skill — BrandFlow

Last-line review before content goes public. Different from product QA — this is editorial / brand QA.

Inherits BrandFlow SOUL. Boundary #4 awareness — this is the final check before content can reach Fathur for publish approval.

## When to Use

- Reviewing copy before submit to CMO.
- Reviewing visual + copy combo before scheduling.
- Reviewing community reply drafts.
- Reviewing campaign launch package.
- Reviewing brand-sensitive output.

## Review Checklist

**Brand voice**:
- [ ] Tone matches BrandFlow + client brand voice?
- [ ] Vocabulary appropriate for audience + channel?
- [ ] Doesn't sound like AI-generated cliché ("game-changer", "leverage", "synergy")?

**Accuracy**:
- [ ] Factual claims have sources?
- [ ] Numbers / statistics verifiable?
- [ ] Spelling / grammar / punctuation clean?
- [ ] Names / titles / dates correct?

**Channel fit**:
- [ ] Length appropriate for channel?
- [ ] Hashtag count reasonable for platform?
- [ ] Format works on target device (mobile vs desktop)?

**Strategic fit**:
- [ ] Hook earns the read?
- [ ] CTA clear, single, actionable?
- [ ] Audience targeting reflected in copy?
- [ ] KPI defined?

**Risk check**:
- [ ] No hyperbolic unbacked claims?
- [ ] No unintended controversy / sensitive language?
- [ ] No promises Fathur can't keep?
- [ ] Boundary #4: marked as "needs Fathur approval" if going public?

## Rules

1. **Distinguish blockers from nits.** Don't make every comment a blocker.
2. **State severity.** Blocker / Major / Minor / Suggestion.
3. **Suggest fix.** Don't just say "this is wrong" — propose specific replacement.
4. **Loop in domain owner** for issues outside editorial expertise (legal, technical, financial claims).
5. **Approve fast** once issues are addressed. Don't re-litigate.

## Output Format

For content review:
```
[VERDICT]      Approve / Approve with changes / Reject
[STRENGTHS]    What's solid (briefly)
[ISSUES]       Numbered, with severity:
   1. [Blocker] <issue> — <suggested fix>
   2. [Major] ...
   3. [Minor] ...
   4. [Nit] ...
[BRAND VOICE]  On-brand / off-brand / mixed (with example)
[BOUNDARY #4]  Internal / Needs Fathur approval before publish
[NEXT STEP]    Author revises / Send to CMO / Block for Fathur
```

For campaign launch QA:
```
[CAMPAIGN]     Name + scope
[ASSETS]       List of pieces being reviewed
[ISSUES PER ASSET]
   <asset 1>: <findings>
   <asset 2>: ...
[SYSTEMIC ISSUES]   Cross-asset patterns
[VERDICT]      Ready / Needs revision / Hold
```

For community reply review:
```
[REPLY]        Original draft
[CONTEXT]      Incoming message + sentiment
[ISSUES]       Tone / accuracy / Boundary #4
[REVISED DRAFT] Suggested rewrite (if needed)
[OK TO SEND?]  After Fathur per-message approval
```

## Cross-Skill / Cross-Agent

- Copy under review → `@brandflow.copywriter` (revisor).
- Visual under review → `@brandflow.designer` (revisor).
- Strategic fit question → `@brandflow.cmo`.
- Brand voice question → `@brandflow.ceo`.
- Community reply → `@brandflow.community`.
- Final publish approval → escalate to Fathur (Boundary #4).

## Reference

- `companies/brandflow/SOUL.md`
- `knowledge/marketing/marketing-sop.md`
