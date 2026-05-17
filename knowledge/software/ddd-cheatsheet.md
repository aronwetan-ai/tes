# Domain-Driven Design — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.backend`, `@nexusai.cto`, `@nexusai.ml`

Source: Eric Evans' DDD (2003), distilled for agency-scale services.

---

## TL;DR

DDD is about **mapping software structure to business meaning**, not picking patterns. Use it when the business model is non-trivial.

For the agency: each major capability (clients, campaigns, content, outreach, reporting) is a **bounded context**. Strict boundary, well-defined contract, separate evolution.

---

## Core Concepts (Fastest Read)

| Term | One-line definition |
|---|---|
| **Ubiquitous Language** | Every term in code matches what stakeholders say. No translation. |
| **Bounded Context** | A part of the system where one model is consistent. Outside it, same word can mean something else. |
| **Entity** | Has identity that persists across change (a User, a Campaign). Equality by ID. |
| **Value Object** | Defined by its values; interchangeable if equal (Money, Email, DateRange). Immutable. |
| **Aggregate** | Cluster of entities + value objects with one entity as root, treated as one transactional unit. |
| **Aggregate Root** | The only entity in an aggregate that outsiders reference. Enforces invariants for the whole. |
| **Domain Service** | Business logic that doesn't naturally fit on an entity (cross-aggregate). |
| **Repository** | Returns aggregates by identity. Hides persistence. |
| **Domain Event** | Something the business cares about happened (`CampaignLaunched`, `ClientChurned`). |

---

## Bounded Context Map for the Agency

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Client Mgmt  │ ←──→│  Campaigns   │ ←──→│   Content    │
│ (CRM)        │     │              │     │ (production) │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ↓                    ↓                    ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Outreach    │     │   Ads Ops    │     │  Reporting   │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

Each box is its own bounded context — own data model, own service, own deploy cadence (eventually). They communicate via events or REST; they don't share a database.

**Why this matters**: a "Client" in CRM has 50 fields, but in Reporting it's just `{client_id, name}`. Don't force one universal Client model.

---

## Ubiquitous Language — Glossary as Code

For each bounded context, maintain a glossary file (`docs/glossary.md`):

```
### Campaign
A time-bounded marketing initiative for one client, tracked across one or
more channels. NOT to be confused with "Ad Set" (a Meta-specific subdivision
of a campaign).

### Channel
A delivery surface (Instagram organic, Meta paid, email). NOT a "platform"
(which we use for software platforms like Meta, Google).
```

Code uses these names exactly. `class Campaign:` matches "Campaign" in client conversations. Renaming requires glossary update + stakeholder confirmation.

---

## Aggregate Design

Rules:
1. **One repo, one aggregate.** Don't load 5 entities to update one.
2. **Reference other aggregates by ID, not object reference.** A `Campaign` holds `client_id: ClientId`, not `client: Client`.
3. **Modify one aggregate per transaction.** If you need to change two, use a domain event + eventual consistency.
4. **Aggregate root enforces invariants.** Inner entities can't be mutated except through the root.
5. **Smallest aggregate that maintains its invariants.** Don't bloat; don't make it a "GodAggregate".

Example sizing:
- ✅ `Campaign` aggregate = Campaign (root) + AdSet[] + DailyBudget. Invariant: sum of AdSet budgets ≤ Campaign budget.
- ❌ `Client` aggregate including all Campaigns and Contacts and Reports. Too big — every save touches everything.

---

## Value Objects (Underused, High ROI)

Replace primitive obsession:

```python
# Bad
def send_email(to: str, body: str): ...

# Better
@dataclass(frozen=True)
class EmailAddress:
    value: str
    def __post_init__(self):
        if "@" not in self.value: raise ValueError("invalid email")

def send_email(to: EmailAddress, body: str): ...
```

Wins:
- Validation in one place.
- Type signature self-documenting.
- Can't accidentally pass `phone_number` where `email` expected.

Common value objects in the agency: `EmailAddress`, `Username`, `Money`, `Percentage`, `DateRange`, `IGAccountId`, `MetaAdAccountId`, `ApiToken`.

---

## Domain Events

Events are facts about the past, named in past tense:

```python
@dataclass(frozen=True)
class CampaignLaunched:
    campaign_id: CampaignId
    client_id: ClientId
    launched_at: datetime
    initial_budget_cents: int
```

Use cases:
- **Decouple side effects**: `CampaignLaunched` → notify Slack, log audit, kick off ads sync. Each handler independent.
- **Cross-context communication**: Reporting context subscribes to `CampaignLaunched` from Campaigns context.
- **Audit trail**: persisted events become history.

NexusAI default for inter-context: events via Postgres `LISTEN/NOTIFY` or Redis Streams. Kafka only when justified.

---

## Strategic Patterns (Context Map)

When mapping interactions between bounded contexts:

| Pattern | When |
|---|---|
| **Shared Kernel** | Two contexts genuinely share a small core (e.g. `ClientId`, `Money`). Tightly coordinated change. |
| **Customer-Supplier** | One context's output is the other's input. Supplier has the upstream relationship. |
| **Conformist** | Downstream conforms to upstream's model (e.g. our model conforms to Meta's API model where forced). |
| **Anti-Corruption Layer** | Between us and an external system whose model we refuse to import. (Always use ACL when integrating external APIs.) |
| **Open Host Service** | We publish a clean public API (other teams' consumers conform to us). |
| **Published Language** | Two contexts agree on a shared schema (events, contract). |

For agency: **always wrap external APIs (Meta, Google, IG) in ACL.** Their model is theirs; ours is ours.

---

## When DDD Is Overkill

- Solo founder building MVP.
- Pure CRUD with no real invariants.
- Throwaway prototype.
- Service with one entity and 4 endpoints.

Go full DDD when: business model is the differentiator, multiple developers contributing, expected lifespan >12 months, regulated domain.

---

## Anti-Patterns

- **Anemic domain.** Entities with only getters/setters; logic in `*Service` classes. Defeats DDD entirely.
- **Large aggregates.** "Client" loads with 100 campaigns — every save = transaction storm.
- **Cross-aggregate transactions.** Use events + eventual consistency.
- **Persistence model = domain model.** SQLAlchemy ORM models with business methods. Mapping at the boundary; don't conflate.
- **One bounded context for everything.** Defeats the purpose; tangled deps everywhere.
- **DDD without stakeholder conversations.** You're inventing a "Ubiquitous Language" no one uses.

---

## Quick Decision Tree

```
Does this codebase need DDD?

Has business logic richer than CRUD?  → No → Skip DDD, use simple layered.
                                       ↓ Yes
Will multiple devs contribute?         → No → Light DDD: entities + repos.
                                       ↓ Yes
Multiple cohesive concept clusters?    → No → One bounded context, full DDD.
                                       ↓ Yes
Each cluster has independent change rate? → Yes → Multiple bounded contexts, full DDD + context map.
                                            ↓ No → One context still, but watch coupling.
```

---

## Reference

- *Domain-Driven Design* — Eric Evans (book, the original).
- *Implementing Domain-Driven Design* — Vaughn Vernon (more practical).
- `knowledge/software/clean-architecture.md` (use case = aggregate operation).
- `companies/nexusai/skills/coding/SKILL.md`.
