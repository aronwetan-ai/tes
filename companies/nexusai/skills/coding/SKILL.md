---
name: coding
description: Backend / frontend / API implementation skill for NexusAI. Specialized for cloud / SaaS / DevOps / AI agent context.
company: NexusAI
used_by: ["@nexusai.backend", "@nexusai.frontend", "@nexusai.cto"]
---

# Coding Skill — NexusAI

NexusAI's craft. Use this for any task that produces code or technical design.

This skill inherits NexusAI SOUL (engineering-precise, pragmatic, zero fluff). It is NOT generic — it assumes SaaS / cloud / API context.

## When to Use

- API design (REST / GraphQL / gRPC).
- Database schema and queries.
- Backend business logic.
- Frontend UI implementation.
- Refactoring existing code.
- Debugging production issues.
- Code review.

## Process

1. **Read context first.** Existing code, existing patterns. No drive-by refactors.
2. **Clarify spec.** Input / output / contract / constraint.
3. **Pick approach.** State minimum 2 options + trade-off, choose with reasoning.
4. **Implement.** Working code beats perfect code.
5. **Validate.** Runs as written? Edge cases? Dependencies clear?
6. **Document inline + at handoff.**

## Rules

1. Identify root cause before fix. No symptom-patching.
2. Prefer boring tech (Postgres > new NoSQL, React > newest framework).
3. No hardcoded secrets. Ever. Loop in `@nexusai.security` for crypto / auth.
4. Handle errors that are realistic. Don't swallow exceptions.
5. Function names describe behavior; variable names describe content.
6. Tests are mandatory for shared code, optional for one-offs.

## Output Format

For implementation:
```
[GOAL]         What we're building
[APPROACH]     Chosen approach + why (1-2 lines)
[CODE]         Code block, language-tagged, with comments on tricky parts
[DEPENDENCIES] What needs to be installed / configured
[EDGE CASES]   What's handled, what's NOT (and why)
[NEXT STEP]    Test, deploy, integrate
```

For debugging:
```
[PROBLEM]      Observed behavior
[CAUSE]        Root cause (verified, not guessed)
[FIX]          Specific change
[VERIFICATION] How to confirm fix works
```

For API design:
```
[ENDPOINT]    METHOD /path
[PURPOSE]     One line
[INPUT]       Schema + example
[OUTPUT]      Schema + example (uses NexusAI standard envelope)
[ERRORS]      Possible codes + when fired
[AUTH]        Required level
[NOTES]       Edge cases, perf, deps
```

## API Standard (NexusAI)

Per `knowledge/software/software-development-sop.md`:

```json
// success
{ "success": true, "data": { ... }, "error": null, "meta": {...} }

// error
{ "success": false, "data": null, "error": { "code": "...", "message": "..." } }
```

## Cross-Skill / Cross-Agent

- Infra / deploy concerns → `@nexusai.devops` + `skills/devops`.
- Security review for auth / crypto → `@nexusai.security`.
- AI agent / prompt design → `@nexusai.ml`.
- Test plans → `@nexusai.qa` + `skills/qa`.
- UI components → `skills/uiux`.

## What This Skill Does NOT Cover

- Marketing copy. Use `@brandflow.copywriter`.
- Crypto research. Use `@crypto.*`.
- Pure infrastructure work. Use `skills/devops`.

## Reference

- `knowledge/software/software-development-sop.md`
- `companies/nexusai/SOUL.md`
- `companies/nexusai/agents/backend.md`, `agents/cto.md`
