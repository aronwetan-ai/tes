# Technical Writing — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.writer`, all engineers writing docs.

Different from `@brandflow.writer` (long-form brand voice). This is for engineers writing for engineers — README, API docs, runbooks, ADRs, internal SOPs.

---

## Reader-First Principles

1. **Identify the reader.** "New backend hire" vs "external API consumer" vs "on-call engineer in 3am crisis". Different docs.
2. **Optimize for skim.** Headings + tables + code blocks > walls of prose. 80% of readers scan first.
3. **Example first, explanation second.** Reader copy-pastes the example, then reads if it didn't work.
4. **One thing per doc.** README ≠ tutorial ≠ API reference ≠ ADR.
5. **Date + owner stamp.** Future-reader needs to know if it's stale.

---

## Doc Type Picker

| Doc | Audience | Format |
|---|---|---|
| README | Anyone landing on the repo | What it does + quickstart + links to deeper docs |
| Quickstart / Tutorial | New user, learning | Step-by-step, runnable, single happy path |
| Reference (API / CLI) | User looking up specifics | Exhaustive, no narrative |
| Architecture overview | New contributor, system understanding | Diagrams + component descriptions + linked ADRs |
| ADR | Future-self / future-team | Context + decision + alternatives + consequences |
| Runbook | On-call engineer in incident | Symptoms → first-response commands → escalation |
| SOP | Recurring process operator | Step-by-step, owner-tagged, verified-checklist |
| Postmortem | Team learning from incident | Timeline + root cause + action items |
| Changelog | User tracking changes | Per-release, by category, semver-aware |

---

## README Standard

```markdown
# project-name

One-line tagline.

## What it does
2-3 sentences max.

## Quick start
\`\`\`bash
# verified copy-paste commands
git clone ...
cd ...
make setup
make run
\`\`\`

## Configuration
Required env vars + defaults + where to set them.

## Usage
Most common scenarios with examples.

## Architecture
Linked diagram or ADR. Don't duplicate here.

## Limitations
What it doesn't do. Known issues.

## Contributing
How to develop / test / submit.

## Support
Where to ask. Who owns this.
```

Verifiable: every command in Quick Start MUST run as written. Verify on a clean machine before merging.

---

## API Reference Standard

For each endpoint:

```markdown
### `POST /v1/campaigns`

Create a new campaign for the authenticated client.

**Auth**: required. Role: `member` or `admin`.

**Request**
\`\`\`json
{
  "name": "Q3 Launch",
  "budget_cents": 1500000,
  "starts_at": "2026-07-01T00:00:00Z"
}
\`\`\`

**Response (201)**
\`\`\`json
{
  "success": true,
  "data": {
    "id": "camp_abc123",
    "client_id": "client_42",
    "name": "Q3 Launch",
    "budget_cents": 1500000,
    "starts_at": "2026-07-01T00:00:00Z",
    "created_at": "2026-05-17T14:32:00Z"
  },
  "error": null
}
\`\`\`

**Errors**
- `400` with `error.code = "VALIDATION"` if body invalid
- `401` if not authenticated
- `403` if role insufficient
- `409` if duplicate within idempotency window

**Notes**
- Pass `Idempotency-Key` header to safely retry
- Rate limited at 60/min per client
```

Generate from OpenAPI spec when possible. Hand-written drift between code and doc is a permanent problem.

---

## Runbook Standard (for on-call)

```markdown
## Incident: Database connection pool exhausted

### Symptoms
- `db_pool_in_use` metric pegged at `db_pool_size`
- Error log: `TimeoutError: QueuePool limit ... reached`
- User-facing: 5xx on heavy endpoints

### First Response (5 min, no investigation)
1. Check recent deploys: `kubectl rollout history deployment/api`
2. If deploy in last hour: rollback. `kubectl rollout undo`
3. Else: scale workers down by half, then back up (clears stuck connections)

### Diagnosis (next 15 min)
1. Check `pg_stat_activity` for long-running queries:
   \`\`\`sql
   SELECT pid, state, query_start, query
   FROM pg_stat_activity
   WHERE state != 'idle' AND query_start < now() - interval '5 min';
   \`\`\`
2. Check app log for connection leak patterns: search `acquired` without matching `released`
3. ...

### Fix
- Identify leaking code path → patch.
- Increase pool size if legitimately under-sized.
- Add PgBouncer if not already in front.

### Verification
- `db_pool_in_use` returns to baseline (~30%)
- Error rate drops to baseline
- No 5xx for 15 min sustained

### Postmortem
Mandatory if ≥P2. File at `docs/postmortems/YYYY-MM-DD-pool-exhausted.md`.

### Escalation
If not resolved in 30 min: page Fathur.

Owner: @nexusai.devops    Last reviewed: 2026-05-15
```

---

## Writing Discipline

### Voice
- Active. "We deploy" > "Deployment is performed".
- Present tense. "The function returns X" > "The function will return X".
- Direct. Drop hedging ("might be", "could possibly", "in some cases").

### Length
- One idea per paragraph.
- Max ~5 sentences per paragraph.
- Cut 20% on second pass.

### Structure
- Headings answer "what is in this section?", not "let's discuss X".
- Lists for ≥3 parallel items.
- Tables for comparison or specs.
- Code blocks for any command/code/config.

### Specificity
- "Database" → "Postgres 15".
- "Recently" → "in the last 24h".
- "Some endpoints" → "POST /v1/campaigns and PATCH /v1/campaigns/:id".

---

## Comments in Code (Bonus)

Different from docs but related:

| Comment type | Use |
|---|---|
| `# WHY` | Why this non-obvious approach? Future-reader needs context. |
| `# TODO(name, date, ticket)` | Owner + due + tracking. No anonymous TODOs. |
| `# HACK` | Acknowledge tech debt with link to fix-it ticket. |
| `# NOTE` | Useful aside. Use sparingly. |

Never: comments that restate the code. (`x = x + 1  # increment x`)

---

## Diagrams (When Useful)

- **Sequence diagram** for request flow across services.
- **Component diagram** for service map.
- **State machine** for finite-state logic.
- **Data model** for DB schema relationships.

Tooling:
- **Mermaid** for in-repo (renders in GitHub MD).
- **PlantUML** for more control.
- **Excalidraw** for whiteboard-style.
- **draw.io** for polished diagrams (export to SVG, commit).

Skip diagrams for trivial flows. A 4-step linear flow doesn't need a picture.

---

## Anti-Patterns

- **README that doesn't describe what the project does.** Common.
- **Commands that don't actually work.** Verify. Or auto-test in CI.
- **Doc that ignores edge cases entirely.** Reader hits one immediately, loses trust.
- **"Just read the code."** Reader wants WHY, not WHAT — code shows what.
- **Long preambles.** "In today's fast-paced world of cloud computing..." — cut.
- **Unowned doc.** No name, no date, no context for staleness check.
- **Documentation for documentation's sake.** Every doc has a reader. If you can't name them, don't write it.
- **Inconsistent terminology across docs.** Once you pick a term, use it everywhere.

---

## Doc Quality Checklist (Pre-Merge)

```
[ ] Reader identified explicitly.
[ ] First example actually runs as written.
[ ] All claims either cited or labeled as opinion.
[ ] No broken links (verify on PR build).
[ ] Date stamp + owner present.
[ ] Skim test passes: TOC + headings convey the argument.
[ ] No filler sentences (each paragraph earns its place).
[ ] Cross-links to related docs.
```

---

## Reference

- `companies/nexusai/agents/writer.md`
- `companies/nexusai/skills/qa/SKILL.md` (quality dimension).
- `knowledge/software/adr-format.md` (specific doc type).
- *Docs for Developers* — Bhumika Mukherjee et al. (book, modern technical writing).
- Diátaxis framework (diataxis.fr) — canonical doc-type taxonomy.
