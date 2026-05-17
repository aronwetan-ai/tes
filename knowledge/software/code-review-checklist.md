# Code Review Checklist — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.qa`, `@nexusai.cto`, `@nexusai.backend`, `@nexusai.frontend`

Used by reviewer at PR time. Pair with `companies/nexusai/skills/qa/acceptance-criteria-templates.md` for AC dimension.

---

## What a Senior Actually Reads

Don't review top-to-bottom. Read in priority:

1. **PR description + linked AC**. What's it claiming to do?
2. **Test diff** (if no test diff for a non-trivial change → red flag, ask).
3. **Critical files** (auth, payment, tenant boundary, data migration).
4. **Logic diff** (the actual change).
5. **Style** (last; auto-formatter handles most).

---

## Tier 1 — Correctness (Blockers)

| Check | What to look for |
|---|---|
| **Tenant isolation** | Every query filters by `client_id`. Or RLS protects. (Agency-critical — most-frequent bug source.) |
| **Auth at boundary** | Endpoint has `Depends(auth)` or equivalent. AuthZ check before action. |
| **Idempotency** | Mutating endpoint accepts and respects `Idempotency-Key`. |
| **Input validation** | All user input validated (Pydantic / zod / explicit). No raw `str` flowing to SQL/exec. |
| **Output structured** | Returns expected schema. Errors have `code` + `message`. |
| **Edge cases** | Empty / null / very large / very small / unicode / negative. At least 2 covered. |
| **Race conditions** | Concurrent edit handled (version check / lock / transaction). |
| **Error handling** | Realistic errors caught and surfaced. No bare `except`. |
| **No regression** | Existing tests still pass. New code has tests where non-trivial. |

---

## Tier 2 — Maintainability (Should Fix)

| Check | What to look for |
|---|---|
| **Naming** | Names describe behavior / content, not implementation detail. |
| **Function size** | <50 lines ideal, <100 hard. Split if complex. |
| **Duplication** | Same logic in 2+ places? Extract. |
| **Magic numbers** | Hardcoded values that should be config / constant. |
| **Comments** | Explain *why*, not *what*. Code shows what. |
| **Docs updated** | README / API spec / changelog matches new behavior. |
| **Dependencies** | New dep justified? Pinned? Audit-clean (`tools/dep_audit.py`)? |
| **Tests sensible** | Cover behavior, not implementation. Don't test mocks. |

---

## Tier 3 — Performance / Cost (Major)

| Check | What to look for |
|---|---|
| **N+1 queries** | `for x in items: db.query(...)` patterns. Use bulk fetch. |
| **Heavy queries** | New endpoint that does table scan? Add index. |
| **External calls in hot path** | Caching opportunity? Batch? |
| **Memory** | Loading whole result set into memory? Stream / paginate. |
| **Cost** | New LLM call without budget cap? Add. |

---

## Tier 4 — Security (Always Looking)

| Check | What to look for |
|---|---|
| **Secrets** | No hardcoded tokens / passwords. Loading from vault / env. |
| **SQL injection** | Parameterized queries everywhere. No string concat into SQL. |
| **XSS** | User-supplied content escaped before rendering. |
| **SSRF** | User-supplied URLs validated against allowlist. Private IPs blocked. |
| **CSV injection** | Cells starting with `=+@-` prefixed with `'`. |
| **Logging** | No PII / no secrets / no full request body in logs. |
| **Auth scope** | New endpoint matches expected role / permission. |

Reference: `knowledge/security/owasp-top10.md`, `knowledge/security/threat-modeling-stride.md`.

---

## Multi-Tenant-Specific (Agency Context)

For any change touching shared code paths:

```
[ ] Does this path filter by client_id at the right layer?
[ ] If a query is cross-tenant (legitimate, e.g. internal admin), is it explicitly tagged?
[ ] Does cache key include client_id (not just resource_id)?
[ ] Does observability (logs/metrics/traces) include client_id label?
[ ] Could a malicious client_A spoof client_id in any input → action on client_B's data?
[ ] Does test cover the negative case (client_A trying to access client_B)?
```

---

## Severity Calibration (Comment Tags)

| Tag | Meaning | When |
|---|---|---|
| **BLOCKER** | Must fix before merge. | Tier 1 issue, tenant leak, security flaw, broken main flow. |
| **MAJOR** | Should fix this PR. | Tier 2 issue, missing test for non-trivial logic. |
| **MINOR** | Consider fixing. | Tier 2/3 nice-to-have. |
| **NIT** | Preference, take or leave. | Style, naming opinion, micro-optimization. |
| **QUESTION** | Need understanding before approval. | "Why this approach?" |
| **PRAISE** | Good work worth flagging. | Notable improvement, smart pattern. |

Disciplines:
- **Don't make every comment a blocker.** Inflation defeats the system.
- **One BLOCKER = block merge.** Author addresses, re-requests review.
- **Approve once issues are addressed.** Don't re-litigate after.

---

## Output Format

```
[VERDICT]     Approve / Approve with changes / Reject

[STRENGTHS]
  - <specific thing done well>
  - <another>

[BLOCKER]     (must fix before merge)
  - <file>:<line> — <issue>. Suggested fix: <fix>.

[MAJOR]
  - ...

[MINOR]
  - ...

[NIT]
  - ...

[QUESTION]
  - ...

[TENANT-CHECK] (agency-required for shared paths)
  Verified: <yes / no / N-A> — <why>

[NEXT STEP]   What the author should do.
```

---

## Reviewer Anti-Patterns

- **Rubber-stamp ("LGTM")** with no comments on a 500-line diff. Either you didn't read or there are issues you missed.
- **Bikeshedding** small style/naming while missing architectural problems.
- **Re-litigating** after approval. Once approved with changes, the changes are made; don't pile on new objections.
- **No-test approval** for non-trivial logic.
- **Reviewing only the diff** — sometimes the bug is what's NOT in the diff (missing edge case, missing docs).
- **Approving your own buddy's PR without scrutiny.** Friendship ≠ free pass.
- **Holding PR > 24h** without comment. Either review or hand off.

---

## Author Anti-Patterns

- **Megafucking-PR.** 2000+ line change touching 30 files. Split.
- **PR title "WIP — fix stuff"**. Title is a release note. Be specific.
- **No PR description.** Future archeology nightmare. State context + change + risk.
- **Tests skipped via `skip_ci`.** Find the fix, not the bypass.
- **Re-formatting unrelated files.** Adds noise. Separate PR.
- **Force-push after review started.** Lose review history. Add commits, squash on merge.

---

## Cross-PR Patterns Worth Noticing

- Same bug recurring? Update knowledge / template / SOP, don't just fix locally.
- New dep added every PR? Audit total deps; consolidate.
- Reviews always blocked on same person? Bus factor risk.
- Reviews always green? Either team is excellent or reviews are theater. Sample-check.

---

## Reference

- `companies/nexusai/skills/qa/SKILL.md`
- `companies/nexusai/skills/qa/acceptance-criteria-templates.md`
- `knowledge/security/owasp-top10.md`
- `knowledge/security/threat-modeling-stride.md`
- `knowledge/software/api-design.md`
