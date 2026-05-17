---
name: qa
description: Testing, validation, code review, and acceptance criteria for NexusAI software output.
company: NexusAI
used_by: ["@nexusai.qa", "@nexusai.cto", "@nexusai.backend", "@nexusai.frontend"]
---

# QA Skill — NexusAI

Quality gate. Use for any review of code, design, or deliverable before it ships.

Inherits NexusAI SOUL (engineering-precise). QA is about catching what specialists miss — edge cases, security gaps, contract violations.

## When to Use

- Code review (PR review).
- Acceptance criteria writing.
- Test plan design.
- Bug report writing.
- Production output validation.
- API contract testing.

## Review Checklist

**Correctness**:
- [ ] Logic correct for happy path.
- [ ] Edge cases handled (null, empty, timeout, network error, race condition).
- [ ] Error handling doesn't swallow exceptions silently.

**Readability**:
- [ ] Names describe behavior / content.
- [ ] Functions short (< 50 lines ideal, < 100 hard limit).
- [ ] Comments explain **why**, not **what**.

**Maintainability**:
- [ ] No significant duplication.
- [ ] No hardcoded values that should be config.
- [ ] Tests exist for non-trivial logic.

**Security** (loop in `@nexusai.security` for any concern):
- [ ] Input validated.
- [ ] No secrets hardcoded / logged.
- [ ] SQL / XSS / CSRF handled (web).
- [ ] Auth & authZ checked at API boundary.

## Output Format

For code review:
```
[VERDICT]     Approve / Approve with changes / Reject
[STRENGTHS]   What's solid
[ISSUES]      Numbered, with severity (Blocker / Major / Minor / Nit)
[RISKS]       What could break in production
[NEXT STEP]   What the author should do
```

For bug report:
```
[BUG]         Short description
[STEPS]       To reproduce
[EXPECTED]    What should happen
[ACTUAL]      What does happen
[SEVERITY]    Critical / High / Medium / Low
[CONTEXT]     Environment, version, related code
```

For acceptance criteria:
```
Given <state>
When <action>
Then <expected outcome>
And <additional assertion>
```

## Rules

1. Distinguish blockers from nits. Don't make every comment a blocker.
2. State severity explicitly.
3. Suggest fix when criticizing — don't just say "this is wrong".
4. Loop in domain owners (security, ML, devops) for issues outside your expertise.
5. Approve once issues are addressed; don't re-litigate.

## Cross-Skill / Cross-Agent

- Code being reviewed → `@nexusai.backend` / `frontend` / `devops` + their respective skills.
- Security review → `@nexusai.security`.
- Architecture sanity → `@nexusai.cto`.
- ML output review → `@nexusai.ml` + their eval methodology.

## Reference

- `knowledge/software/software-development-sop.md` (code review section)
