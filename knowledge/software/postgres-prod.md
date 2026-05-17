# Postgres in Production — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.backend`, `@nexusai.devops`

NexusAI default DB. This is what every backend agent should know.

---

## Version Pin

Default to **Postgres 15+**. Postgres 16 has good agency-relevant wins (logical replication, perf). Avoid Postgres 11/12 — EOL or near-EOL.

---

## Connection Pooling

App connections are not free. One web server = many workers = many connections × N replicas × M pods. Postgres struggles past ~200 connections.

| Pool | When |
|---|---|
| **PgBouncer** (transaction mode) | Default for high-concurrency apps. Use transaction-mode unless app needs session features (advisory locks, prepared statements across requests). |
| **App-side pool** (SQLAlchemy) | Always present, sized to ~10 per worker. |
| **PgCat** | Newer alternative, good if you need sharding-aware routing. |

Layout: app → app-side pool (~10) → PgBouncer (~50) → Postgres (~100 max). Layered.

---

## Indexing — Practical Rules

1. **Index every foreign key.** Postgres doesn't auto-index FK; queries with JOIN suffer.
2. **Index columns in WHERE clauses with high selectivity.** `WHERE status = 'active'` on 95%-active table = no value.
3. **Composite index order matters.** `(client_id, created_at)` serves `WHERE client_id = ?` and `WHERE client_id = ? AND created_at > ?`. Doesn't serve `WHERE created_at > ?` alone.
4. **Partial indexes for sparse data.** `CREATE INDEX ... WHERE deleted_at IS NULL` — smaller, faster, only covers active rows.
5. **GIN for jsonb / array / full-text.** B-tree for everything else.
6. **Drop unused indexes.** They slow writes. `pg_stat_user_indexes` shows usage.

```sql
-- Example: per-tenant query pattern
CREATE INDEX idx_campaigns_client_active
  ON campaigns (client_id, status, created_at DESC)
  WHERE deleted_at IS NULL;
```

---

## Query Patterns

### Pagination
- ❌ Offset for deep pages: `LIMIT 50 OFFSET 100000` reads 100050 rows.
- ✅ Keyset: `WHERE created_at < ? ORDER BY created_at DESC LIMIT 50` — O(log n).

### Counting
- `SELECT COUNT(*) FROM campaigns` on 10M rows is slow.
- For estimates: `SELECT reltuples::bigint FROM pg_class WHERE relname = 'campaigns';`
- For exact + filtered: ensure filter has index, accept the cost, or maintain a counter table.

### Soft delete
- Add `deleted_at TIMESTAMP NULL`. Default queries filter `WHERE deleted_at IS NULL`.
- Combine with partial index for performance.
- Hard-delete after retention window (90+ days) for GDPR / data minimization.

### Idempotency
- `INSERT ... ON CONFLICT (idempotency_key) DO NOTHING RETURNING *` — atomic.
- Or use unique partial index for (client_id, idempotency_key) when key has scope.

---

## Transactions — Discipline

```python
# Bad — lock held across HTTP call
with db.begin():
    user = db.query(User).filter_by(id=uid).with_for_update().one()
    response = external_api.send(user.email)  # ← seconds, lock held
    user.last_sent_at = now
```

```python
# Good — split
with db.begin():
    user = db.query(User).filter_by(id=uid).one()
external_api.send(user.email)
with db.begin():
    db.query(User).filter_by(id=uid).update({"last_sent_at": now})
```

Rules:
1. Never hold a transaction across external I/O.
2. Keep transactions short — milliseconds, not seconds.
3. Use `SELECT FOR UPDATE` only when truly contended; prefer optimistic concurrency (version column).
4. Avoid `SERIALIZABLE` isolation by default; use `READ COMMITTED` (PG default), upgrade only when business requires.

---

## Schema Migrations — Safe Patterns

NexusAI rule: **expand-and-contract**, never inline drop.

### Adding a column
- Default: NULLABLE first (instant).
- Set NOT NULL only after backfill complete.
- Adding NOT NULL with DEFAULT in PG11+ is instant; PG10- locks.

### Renaming a column
1. Add new column.
2. Backfill: `UPDATE table SET new = old`.
3. Deploy code that writes to BOTH.
4. Deploy code that reads from new only.
5. Deploy code that stops writing to old.
6. Drop old (1+ week later).

### Adding an index
- `CREATE INDEX CONCURRENTLY` — doesn't lock writes.
- Watch for failures; partial index may exist after error. Drop and retry.

### Changing a type
- Add new column with new type.
- Backfill with cast/transform.
- Switch reads + writes (above).
- Drop old.

---

## Multi-Tenant Patterns (Agency)

Three isolation levels:

| Pattern | When |
|---|---|
| **Row-level (`client_id` column + filter)** | Default for agency. Cheap. Index FK. |
| **Schema per tenant** | Sensitive client data, regulated workloads. Migration overhead × N. |
| **DB per tenant** | SLA / compliance differentiation. Operational overhead high. |

Defense-in-depth for row-level: **Postgres RLS**.

```sql
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

CREATE POLICY campaign_tenant_iso ON campaigns
  USING (client_id = current_setting('app.client_id')::uuid);

-- App sets at session start:
SET app.client_id = '...uuid...';
```

If app code forgets the WHERE, RLS denies. Belt-and-suspenders.

---

## Backup + Restore

| Backup type | Cadence | Test cadence |
|---|---|---|
| Logical (pg_dump) | Daily, 30-day retention. | Monthly restore drill. |
| Physical (WAL archiving) | Continuous. | Quarterly PITR drill. |
| Snapshot (cloud provider) | Daily. | Quarterly restore. |

**Rule**: an untested backup is no backup. Schedule a quarterly restore-from-backup exercise.

Store backups in a different region / account / provider from primary. Ransomware that encrypts your prod can encrypt your backups too if same auth.

---

## Performance Tuning Checklist

When a query is slow:

1. `EXPLAIN ANALYZE` — actual plan + actual time.
2. Look for `Seq Scan` on big tables (missing index?).
3. Look for `Sort` of huge intermediate (need `WORK_MEM` increase or rewrite).
4. Look for `Nested Loop` over large outer (consider `HASH JOIN`).
5. Check stats are fresh: `ANALYZE table_name;`.
6. Bloat? `VACUUM ANALYZE table_name;` regularly. `pg_stat_user_tables` shows `n_dead_tup`.
7. Index that should match — check column types align (int vs bigint mismatch defeats index).

Common config knobs:
- `shared_buffers = 25% of RAM` (start point).
- `effective_cache_size = 50–75% of RAM`.
- `work_mem = 32–64MB` per connection (multiplied by N!).
- `max_connections = 100–200`. More = use a pooler instead.

---

## Disaster Patterns to Know

| Symptom | Likely cause |
|---|---|
| Sudden slowdown of all queries | Long-running transaction blocking VACUUM → bloat → bad plans. |
| Connection storms | App leak — connection not released. Or no pooler in front of PG. |
| Replica lagging | Long-running query on replica blocking apply. Or write spike on primary. |
| OOM on Postgres process | `work_mem × N connections × parallel workers` math. |
| Mystery data corruption | Underlying disk / cosmic ray. Verify with `pg_amcheck`. Restore from backup. |

---

## Anti-Patterns

- **Storing JSON when relational fits.** `jsonb` is great when shape is dynamic; bad when shape is fixed (lose constraints, lose query optimization).
- **No connection pooler.** Direct app-to-PG at scale = connection storm.
- **Indexing everything.** Index = slower writes + larger storage. Audit `pg_stat_user_indexes` quarterly.
- **`SELECT *` in production code.** Tight coupling to schema.
- **String IDs.** Use UUID (uuid type) or bigint with sequence. Strings break ordering, indexing, foreign keys.
- **Storing money as float.** Use `numeric(15, 2)` or integer cents. Float math = lost cents.
- **Long-running transactions during external I/O.** See above.
- **Skipping migrations / running on prod manually.** Lost reproducibility, lost rollback.

---

## Reference

- PostgreSQL official docs (canonical).
- *PostgreSQL Up & Running* (Regina Obe, Leo Hsu).
- `companies/nexusai/skills/coding/SKILL.md`
- `knowledge/software/api-design.md` (idempotency, pagination patterns).
- `knowledge/software/cicd-patterns.md` (migrations in deploy).
