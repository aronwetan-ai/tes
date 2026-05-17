# Clean Architecture — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.*` engineers

Source: Robert C. Martin (Uncle Bob) — paraphrased for NexusAI agency context.

---

## TL;DR

Layers point inward. Inner layers know nothing about outer layers. Business rules don't import frameworks.

```
                ┌─────────────────────────┐
                │  Frameworks & Drivers   │  ← Web, DB, External APIs
                │  ┌───────────────────┐  │
                │  │ Interface Adapters│  │  ← Controllers, Presenters, Repos
                │  │  ┌─────────────┐  │  │
                │  │  │  Use Cases  │  │  │  ← Application logic
                │  │  │  ┌───────┐  │  │  │
                │  │  │  │Entities│ │  │  │  ← Enterprise rules
                │  │  │  └───────┘  │  │  │
                │  │  └─────────────┘  │  │
                │  └───────────────────┘  │
                └─────────────────────────┘
                  Dependencies point in →
```

---

## Layer Responsibilities

| Layer | Owns | Imports |
|---|---|---|
| **Entities** | Pure business rules. Pure data + invariants. | Nothing external. |
| **Use Cases** | Application-specific orchestration ("createCampaign", "syncIGMetrics"). | Entities + repository **interfaces**. |
| **Interface Adapters** | Map use case I/O to outside world. Controllers, repos, presenters. | Use case interfaces + outer-world libs. |
| **Frameworks & Drivers** | FastAPI / Next.js / Postgres driver / Meta SDK. | Anything. |

The **Dependency Rule**: source code dependencies point only inward. Outer can depend on inner; never reverse.

---

## When to Use vs Skip

**Use when**:
- Service expected to live >12 months.
- Business rules complex enough to test independently.
- Likely to swap a framework / database / external API.
- Multi-tenant / agency context: business rule must work whether called from cron, web, or queue.

**Skip when**:
- One-off script.
- Tiny CRUD with no real business logic.
- Prototype to be thrown away in 2 weeks.

For the agency: **always use for client-facing services**, skip for internal cron-glue.

---

## Practical Folder Layout (Python / FastAPI)

```
src/
  domain/           ← Entities + value objects. No imports outside stdlib.
    campaign.py
    client.py
  application/      ← Use cases. Imports from domain.
    create_campaign.py
    sync_ig_metrics.py
    ports/          ← Interfaces (Protocol classes).
      campaign_repo.py
  adapters/         ← Implementations of ports + I/O mapping.
    persistence/
      sqlalchemy_campaign_repo.py
    external/
      meta_ads_client.py
    web/
      campaign_controller.py
  infrastructure/   ← FastAPI app, DB session, config.
    main.py
    db.py
    config.py
```

Test pyramid maps:
- `domain/` and `application/` = unit tests, no I/O.
- `adapters/` = integration tests against real DB / mocked external.
- `infrastructure/` = E2E only.

---

## Concrete Example (agency context)

Bad (typical FastAPI tutorial):
```python
@router.post("/campaigns")
def create_campaign(req: CampaignReq, db: Session = Depends(get_db)):
    c = Campaign(client_id=req.client_id, name=req.name, ...)
    db.add(c)
    db.commit()
    return c
```
Problems: `client_id` from request body (tenant bypass), DB session bleeds into controller, no business validation, can't unit-test without DB.

Better:
```python
# domain/campaign.py — pure
@dataclass
class Campaign:
    id: UUID; client_id: UUID; name: str; budget_cents: int
    def __post_init__(self):
        if self.budget_cents < 0: raise ValueError("budget cannot be negative")

# application/ports/campaign_repo.py
class CampaignRepo(Protocol):
    def save(self, c: Campaign) -> Campaign: ...

# application/create_campaign.py
def create_campaign(req: CreateCampaignInput, ctx: AuthCtx, repo: CampaignRepo) -> Campaign:
    c = Campaign(id=uuid4(), client_id=ctx.client_id, name=req.name, budget_cents=req.budget_cents)
    return repo.save(c)

# adapters/web/campaign_controller.py
@router.post("/campaigns")
def post_campaign(req: CampaignReq, ctx=Depends(auth), repo=Depends(get_campaign_repo)):
    c = create_campaign(req.to_input(), ctx, repo)
    return CampaignResponse.from_domain(c)
```
Now `client_id` comes from auth context, business rule lives in `domain`, use case is unit-testable without DB.

---

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Domain imports SQLAlchemy `Model` | Can't unit test without DB. Migration coupling. | Plain dataclass / Pydantic in domain; ORM model in adapter. |
| Use case calls `requests.get(...)` directly | Can't test offline. Coupled to HTTP lib. | Define `MetaApiClient` port; inject impl. |
| Controller does business logic | Logic duplicated across HTTP/cron/queue entry points. | Move to use case. |
| Repo returns ORM model | API response shape = DB schema. Breaks on migration. | Map ORM → domain at repo boundary. |
| One giant `services.py` | God file. | Split per use case. |
| Anemic domain | All logic in services, entities are just bags-of-fields. | Push invariants & calculations into entities. |

---

## Anti-Patterns

- **"Just one quick query in the controller."** That's how it starts. Now business logic is in your HTTP handler.
- **Skipping the domain layer for "simple" services.** Simple grows complex. Add the layer when it's still small.
- **Following the layer split religiously for trivial CRUD.** Pragmatism wins. Tiny services skip use case layer.
- **Defining ports for things you'll never swap.** YAGNI. Define a port when you have ≥2 likely implementations.

---

## Multi-Tenant Note

Tenant isolation belongs in the **adapter** layer (repo enforces `client_id` filter), with the use case receiving an `AuthCtx` that already proved the tenant. Domain entities carry `client_id` but don't enforce isolation themselves — that's the repo's job. Defense in depth: also add Postgres RLS policy.

---

## Reference

- *Clean Architecture* — Robert C. Martin (book).
- `companies/nexusai/skills/coding/SKILL.md`
- `knowledge/software/ddd-cheatsheet.md` — bounded context maps to use case package.
- `knowledge/software/api-design.md` — adapter/web layer conventions.
