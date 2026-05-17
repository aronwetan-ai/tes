# Architecture Decision Records (ADR) — Format Reference

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.cto`, `@nexusai.writer`, `@nexusai.backend`

---

## Why ADRs

Code shows **what**. Comments show **how**. ADRs explain **why**.

When future-you (or future-agent) asks "why did we pick Postgres over MySQL?" — the answer should be a 2-minute read in `docs/adr/0007-postgres-as-primary-db.md`, not a 2-hour archaeology session through Slack history.

---

## When to Write an ADR

For any decision that:
- Has alternatives that were considered.
- Has tradeoffs (not "obviously right").
- Will be hard to reverse later.
- Affects multiple components / services.
- New team members will eventually wonder about.

**Skip** for:
- Trivial style decisions (let formatter handle).
- Pure code refactors with no architectural impact.
- Dependency version bumps (changelog suffices).

---

## Standard Format (Michael Nygard's, lightly adapted)

```markdown
# ADR-{NNNN} — {Title in noun phrase, not question}

Status:    Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
Date:      YYYY-MM-DD
Deciders:  @nexusai.cto, @nexusai.security
Tags:      database, multi-tenant, agency

---

## Context

What's the situation? What forced this decision? Be concrete.
Don't pad — 1-3 paragraphs is plenty.

## Decision

What we chose. State it clearly in one sentence at the top.
Then 2-4 paragraphs of detail.

## Consequences

### Positive
- Specific gain 1
- Specific gain 2

### Negative
- Specific cost 1
- Specific cost 2

### Neutral
- Things that change but aren't obviously good/bad

## Alternatives Considered

### Alternative 1: <name>
- Why we considered it
- Why we didn't pick it

### Alternative 2: <name>
- ...

## References

- Links to issues, PRs, docs, papers, prior art.
```

---

## Worked Example

```markdown
# ADR-0007 — Postgres as Primary Database

Status:   Accepted
Date:     2026-05-12
Deciders: @nexusai.cto, @nexusai.backend
Tags:     database, foundation, agency

---

## Context

NexusAI is starting client-data services for the agency (campaigns, contacts,
report cache, OAuth tokens for client integrations). We need a primary store.
Expected scale: 20–50 clients, ~1M rows/client/year, transactional reads
dominant, occasional analytical queries.

Constraints:
- Multi-tenant: row-level isolation required.
- Strong consistency on auth/billing paths.
- Operational simplicity (solo founder + freelancers).
- Cloud-portable (avoid vendor lock).

## Decision

Postgres 15+ as primary OLTP database for all NexusAI services. Single instance
per environment to start, with read replica added when query load justifies it.

Use SQLAlchemy (Python) / Prisma (Node) at the ORM layer with explicit raw SQL
for hot reports.

Use Postgres native features for tenant isolation:
- `client_id` column on every multi-tenant table (FK indexed).
- Row-level security (RLS) policies as defense-in-depth.

## Consequences

### Positive
- Mature, audited tooling — well-known operational risks.
- Strong consistency by default; can opt into async via replica.
- JSONB for occasional dynamic shape, full-text search built-in, extension ecosystem.
- RLS provides "belt-and-suspenders" tenant safety beyond app-layer filters.
- Backup tooling (pg_dump, WAL-G) battle-tested.

### Negative
- Vertical scaling has limits — we'll need read replicas + sharding considerations
  if a client passes 100M rows.
- Connection management requires PgBouncer in front at scale (not a default).
- ANALYZE / VACUUM tuning becomes important past 100GB.

### Neutral
- ORM abstraction means devs may not learn Postgres deeply — curated training
  required for senior engineers.

## Alternatives Considered

### MySQL / MariaDB
- Familiar to many; reasonable. Rejected because we'd lose Postgres-specific
  wins: RLS, JSONB query capability, GIN indexes for our use cases.

### MongoDB
- Document model is a poor fit — agency data is highly relational
  (clients ↔ campaigns ↔ contacts ↔ events). JOIN performance matters.

### Firebase / Firestore
- Too cloud-locked; tenant isolation harder; query model limited.

### CockroachDB / Yugabyte
- Distributed SQL — overkill for current scale, ops complexity now to solve
  problems 2 years away.

## References

- `knowledge/software/postgres-prod.md`
- `knowledge/software/cap-and-consistency.md`
- Discussion: PR #142 `chore/decide-primary-db`
```

---

## Status Lifecycle

```
Proposed
   ↓
   ├──→ Accepted ────→ (later) Deprecated by reality → Superseded by ADR-NNNN
   │                          ↓
   ↓                       Deprecated
Rejected (kept as record of "why not this path")
```

Don't delete deprecated/superseded ADRs — they're history. Mark status, link to replacement.

---

## File Layout

```
docs/
  adr/
    README.md                    # index of all ADRs, status, summary line each
    0001-record-architecture-decisions.md   # the meta-ADR ("we use ADRs")
    0002-python-as-primary-language.md
    0003-fastapi-for-http-services.md
    ...
    template.md                  # blank template for new ADRs
```

Numbering is sequential and **never reused** even after deletion.

---

## Index README Format

```markdown
# ADR Index

| ID | Title | Status | Date |
|---|---|---|---|
| 0001 | Record Architecture Decisions | Accepted | 2026-04-01 |
| 0002 | Python as Primary Language | Accepted | 2026-04-02 |
| 0007 | Postgres as Primary Database | Accepted | 2026-05-12 |
| 0011 | Drop Kafka in Favor of Redis Streams | Accepted | 2026-05-15 |
| 0011-supersede-0009 | (note: this supersedes ADR-0009 Kafka Adoption) | | |
```

---

## Discipline

- **One decision, one ADR.** Don't bundle 3 unrelated decisions.
- **Write at the time of decision**, not 6 months later from memory.
- **Stakeholders sign off in the ADR file** (commit by them, or named).
- **Link from code/comments where helpful**: `# see ADR-0007 for tenant isolation rationale`.
- **Review during quarterly architecture audits** — any ADR no longer reflective of reality gets deprecated.

---

## When ADRs Are Overkill

- Solo project, no other readers ever.
- Decision is genuinely obvious (no real alternatives).
- Decision is reversible in <1 day.

For 95% of NexusAI architectural decisions: write the ADR.

---

## Reference

- Michael Nygard's original "Documenting Architecture Decisions" (2011) — canonical.
- adr.github.io
- *Building Evolutionary Architectures* — Ford, Parsons, Kua.
- `knowledge/software/clean-architecture.md`
- `companies/nexusai/agents/cto.md`
- `companies/nexusai/agents/writer.md`
