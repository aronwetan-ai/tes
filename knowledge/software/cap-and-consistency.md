# CAP & Consistency — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.backend`, `@nexusai.cto`

For any agent designing a distributed system. Not relevant for monolith + single DB.

---

## CAP — The Theorem in 3 Lines

In a distributed system, you can have **at most 2 of**:

- **C** — Consistency: every read sees the latest write.
- **A** — Availability: every request gets a response (no error).
- **P** — Partition tolerance: system works when network splits between nodes.

Network partitions happen. So in practice, the choice is **CP** or **AP** — you pick C or A during a partition.

| Pick | Behavior during partition |
|---|---|
| **CP** (Consistency + Partition) | Reject writes/reads on the minority side. Stay consistent. |
| **AP** (Availability + Partition) | Accept writes on both sides. Reconcile later. |

NexusAI default for agency: single-region Postgres = **CA-flavored** (no partitions while the DB is up). When you replicate or shard, you pick CP or AP.

---

## PACELC — The Refinement

Even WITHOUT partitions, you trade Latency for Consistency.

| When | Trade |
|---|---|
| Partition (P): pick A or C. | (Same as CAP.) |
| Else (E): pick L or C. | Strong consistency = synchronous replication = higher latency. |

**Postgres synchronous replica**: PC/EC — strong consistency, higher latency.
**Postgres async replica**: PA/EL — fast, eventual consistency.
**Cassandra (default)**: PA/EL.
**DynamoDB strong-read**: PC/EC for that read.

---

## Consistency Models — Spectrum

From strongest to weakest:

| Model | Guarantee | Cost |
|---|---|---|
| **Linearizable** | Reads see most recent write, total global order. | High latency. Synchronous coordination. |
| **Sequential** | All clients see same order, but order may not be real-time. | Cheaper than linearizable. |
| **Causal** | If A causes B, all observers see A before B. Concurrent ops may differ. | Reasonable cost. |
| **Read-Your-Writes** | A client sees its own writes immediately. | Easy with sticky session. |
| **Monotonic Reads** | Once you've seen value V, you don't see older. | Easy with sticky session. |
| **Eventual** | Replicas converge, eventually. | Cheapest. |

**For agency context**:
- User-facing flows (campaign create, contact edit) → at minimum read-your-writes.
- Reporting dashboards → eventual is fine (data <30s stale acceptable).
- Payments / billing → linearizable (contention-aware).

---

## When Eventual Consistency Bites

Common bugs:

```
1. User edits campaign → read returns old version → "my change didn't save".
   Fix: read-your-writes via sticky session OR write-then-read from primary.

2. List view shows new item, detail page 404s.
   Fix: read-your-writes guarantee for the user who just created.

3. Aggregate counter is off (sum of children ≠ parent total).
   Fix: aggregate on read, or update transactionally.

4. Cross-region replica delay → user sees stale data after roaming.
   Fix: pin to primary region for the session, or accept staleness with UI hint.
```

---

## Distributed Transaction Patterns

Avoid distributed (two-phase commit) transactions. Instead:

### Saga
A sequence of local transactions, each emitting an event. If any step fails, run compensating transactions to undo prior steps.

```
[Create Order] → emit OrderCreated
                   ↓
[Reserve Stock] → emit StockReserved
                   ↓
[Charge Card]  → emit CardCharged
                   ↓
[Ship Order]   → emit OrderShipped

If [Charge Card] fails:
  [Reserve Stock] compensating: ReleaseStock
  [Create Order] compensating: CancelOrder
```

### Outbox Pattern
To reliably emit events alongside DB writes:

```sql
BEGIN;
  INSERT INTO orders (...);
  INSERT INTO outbox (event_type, payload) VALUES ('OrderCreated', '{...}');
COMMIT;

-- Separate poller reads outbox → publishes to Redis/Kafka → marks sent.
```

Why: same DB transaction = atomic. Without outbox, you risk "DB write succeeded but event publish failed" or vice versa.

NexusAI agency default: outbox in Postgres + LISTEN/NOTIFY for publishing.

---

## Idempotency — The Lifesaver

In any distributed system, retries happen. Make every operation safe to retry:

- **Idempotency key per request** (`Idempotency-Key` header).
- **Server stores** `(client_id, key) → response` for 24h.
- **Same key + same body** = return stored response, no duplicate effect.
- **Same key + different body** = 422 conflict.

Mandatory for: payment, send, post, message. Skip for: read-only ops.

---

## Replication Patterns

### Single primary + read replicas
- **Writes** → primary.
- **Reads** → replicas (eventual consistency lag — typically <1s for healthy setups).
- **Read-your-writes**: route reads from same user to primary for short window after write, OR store last-write-time and check.

### Multi-primary (avoid for agency-scale)
- Both nodes accept writes. Conflict resolution required (last-write-wins, CRDT).
- Operationally complex. Don't pick this without serious need.

### Postgres logical replication
- Selectively replicate tables. Useful for cross-region read replicas, or moving to a new DB.

---

## Quorum Patterns

For systems with N replicas, R reads + W writes:

- `R + W > N` → strong consistency for those reads.
- `R = 1, W = N` → fast reads, slow writes.
- `R = N, W = 1` → fast writes, slow reads.

Cassandra/DynamoDB tunable per-query. Postgres replicas typically `W=1, R=1` (eventual) by default.

---

## Anti-Patterns

- **Distributed transactions across services.** Cross-service 2PC = brittle. Use saga.
- **"Strong consistency everywhere."** Latency cost. Most reads can tolerate slight staleness.
- **Multi-primary without conflict strategy.** Random data corruption.
- **Cache without invalidation strategy.** Stale data served forever.
- **Reading from replica + writing to primary, with no read-your-writes guarantee.** Common UX bug.
- **No outbox for cross-service events.** Lost events on crash.
- **Tight coupling between services + sync HTTP cascade.** A → B → C → D in one call = latency multiplier + cascade failure.

---

## When This Doesn't Matter (Most Agency Work)

Single Postgres instance + single app cluster = no distributed system. Skip CAP entirely. Don't over-engineer.

CAP becomes relevant when:
- Adding read replicas.
- Multi-region deploy.
- Splitting into microservices that share state.
- Integrating with external services (each external API = a remote node, partition possible).

For agency context: most NexusAI services start in the simple bucket. CAP becomes relevant around year 2 + 20+ active clients + multi-region.

---

## Reference

- *Designing Data-Intensive Applications* — Martin Kleppmann (canonical book).
- `knowledge/software/postgres-prod.md` (replication detail).
- `knowledge/software/api-design.md` (idempotency).
- `companies/nexusai/skills/coding/SKILL.md`
