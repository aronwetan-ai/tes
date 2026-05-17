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

## Senior Patterns (Deep Dive)

### Code review depth — what a senior actually checks

Beyond the basic checklist, senior review looks at:

1. **Tenant isolation** (agency-critical): does this code path correctly scope by `client_id`? Could one client see another's data?
2. **Idempotency**: if this endpoint is called twice (network retry, browser double-click), is the result consistent?
3. **N+1 queries**: any `for x in items: db.query(...)` pattern? Use bulk fetch.
4. **Lock contention**: any DB lock held across external I/O?
5. **Error visibility**: when this fails in prod, will we know what failed and why?
6. **Backward compatibility**: does this break existing callers? If yes, is it documented + versioned?
7. **Deletion handling**: does this code do the right thing when input refers to a deleted entity?
8. **Time zone**: any naive datetime? UTC at the boundary, render in user TZ at display.
9. **Money / counts**: integers (cents) for money, never float. Decimal lib for tax/fee math.
10. **Strings from users**: validated for length, encoding, control chars before storing.

### Agency-scale acceptance criteria patterns

For every feature in NexusAI's output, AC must explicitly cover:

| Dimension | Question to answer |
|---|---|
| Single-tenant | Works for one client. (Necessary, not sufficient.) |
| Multi-tenant | Works correctly when client A and client B share the system. |
| Permission | Freelancer with limited scope can't access full vault / other clients. |
| Failure | When external API (IG / Meta / Google) is down, app degrades gracefully. |
| Rate limit | When client hits external API quota, error message is actionable. |
| Empty state | First-time client (no data yet) sees useful onboarding, not crash. |
| Concurrent | Two team members editing same client simultaneously — last-write or merge? |
| Audit | Action is logged with who/when/what for compliance + dispute resolution. |

Reference: `companies/nexusai/skills/qa/acceptance-criteria-templates.md` (agent-specific deep skill, in tasks/#5).

### Test strategy by code type

| Code type | Test approach |
|---|---|
| Pure logic (calculator, parser, formatter) | Unit tests, high coverage, fast. |
| DB-backed service | Integration tests against real DB (testcontainers). Fixtures for tenants. |
| External API integration | Mocked at network layer (responses lib / nock). Contract tests against sandbox if available. |
| AI agent | Eval suite (per `skills/ml-agent`). Not "unit tests". |
| UI component | Storybook + visual regression for visual states. Behavior in component tests. |
| End-to-end flow | Playwright / Cypress for critical paths only. Slow + flaky = use sparingly. |
| Operational scripts | Smoke test on dry-run + execute on disposable env. |

### Bug severity calibration (NexusAI)

| Severity | Examples | SLA |
|---|---|---|
| Critical | Data leak across clients. Auth bypass. Payment failure. Production down. | Drop everything. Hotfix. Postmortem. |
| High | Single client's pipeline broken. Data corruption (recoverable). | Fix this sprint. |
| Medium | Workaround exists. Cosmetic but visible. Performance regression <2x. | Fix next sprint. |
| Low | Edge-case logging. Internal-only. Minor copy. | Backlog. |

### Code review output template (deepened)

```
[VERDICT]     Approve / Approve with changes / Reject

[STRENGTHS]   2-3 specific things done well (training signal, not flattery).

[ISSUES]
  Blocker (must fix before merge):
    - <file:line> — issue + suggested fix.
  Major (should fix this PR):
    - ...
  Minor (consider fixing):
    - ...
  Nit (preference, take or leave):
    - ...

[RISKS]       What could break in production. Be specific.

[TENANT CHECK] (agency-required)
  Does this respect client_id isolation? <yes/no/N-A>

[NEXT STEP]   What the author should do.
```

### Anti-patterns in QA

- **Rubber-stamp approval.** "LGTM" with no comments = no review. Either there are no issues (rare) or you didn't read it.
- **Bikeshedding small things while missing big ones.** Style nits are fine if architecture is solid; criticize architecture first if it's not.
- **Re-litigating after approval.** Once approved with changes, the changes are made — don't add new objections after.
- **No test required for "trivial" changes.** "Trivial" change in tenant-isolation code = potential cross-tenant leak.
- **Reviewing only the diff.** Sometimes the bug is what's NOT in the diff (missing edge case, missing test, missing docs).

## Reference

- `knowledge/software/software-development-sop.md` (code review section)
- `knowledge/software/code-review-checklist.md`
- `companies/nexusai/skills/qa/acceptance-criteria-templates.md` (agent-specific deep skill)
