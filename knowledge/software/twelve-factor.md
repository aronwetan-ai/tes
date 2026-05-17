# Twelve-Factor App — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.backend`, `@nexusai.devops`

Source: Heroku's 12-Factor methodology (~2011), still the baseline for cloud-native apps.

---

## TL;DR

| # | Factor | Question |
|---|---|---|
| 1 | Codebase | One repo per service, deployable from `main`? |
| 2 | Dependencies | Pinned + locked + isolated? |
| 3 | Config | In env vars, not code? |
| 4 | Backing services | Swappable via connection string? |
| 5 | Build / release / run | Three distinct stages? |
| 6 | Processes | Stateless? |
| 7 | Port binding | Self-contained server? |
| 8 | Concurrency | Horizontal via process model? |
| 9 | Disposability | Fast start, graceful shutdown? |
| 10 | Dev / prod parity | Tools + topology + data shape match? |
| 11 | Logs | stdout JSON event stream? |
| 12 | Admin processes | One-shot, not embedded in app? |

Pass = ready for cloud / containers / horizontal scale. Fail = legacy pain at scale.

---

## NexusAI Defaults Per Factor

### 1 — Codebase
- One repo per service. Mono-repo OK if tooling supports per-service deploys.
- Branch convention: `main` is always deployable. PRs from feature branches.
- **Anti**: shared codebase across multiple deployed apps without clear boundary.

### 2 — Dependencies
- Python: `pip-tools` → `requirements.txt` + `requirements-dev.txt`, both pinned.
- Node: `pnpm` lockfile committed.
- System deps in `Dockerfile`, also pinned (tag, not `latest`).
- **Anti**: relying on system Python / global npm. Always virtual env / container.

### 3 — Config
- All deployment-varying values in env: `DATABASE_URL`, `STRIPE_KEY`, `LOG_LEVEL`.
- `.env.example` checked in. Real `.env` never.
- Production secrets: vault (HashiCorp / Bitwarden / `tools/cred_vault.py`).
- **Anti**: `if env == "prod": ...` branches in code. Config drives behavior, not branches.

### 4 — Backing services
- DB / cache / queue / S3 / external API — all reachable via URL/credential from env.
- Replacing prod DB with test DB = change one env var.
- **Anti**: hardcoded `localhost:5432` anywhere.

### 5 — Build / release / run
| Stage | Output | Triggered by |
|---|---|---|
| Build | Docker image (immutable) tagged with git SHA. | Push to `main`. |
| Release | Image + config bundle. | Promotion (manual or auto). |
| Run | Container running with env vars injected. | Deploy command. |

- **Anti**: building inside the production container.

### 6 — Processes
- Stateless. State lives in DB / cache / S3.
- Local filesystem ephemeral. No "user uploads stored on disk" — that's S3.
- **Anti**: in-process session storage, in-memory caches that aren't easy to drop.

### 7 — Port binding
- App self-binds (e.g. `uvicorn ... --host 0.0.0.0 --port 8000`).
- Reverse proxy (Cloudflare / Nginx) in front, but app must run standalone for dev.
- **Anti**: depending on Apache module / external runtime.

### 8 — Concurrency
- Scale by process count, not threads inside one process.
- Queue / batch worker = a separate process type, scaled independently.
- **Anti**: cramming web + worker + scheduler into one container "for simplicity".

### 9 — Disposability
- Start fast (<10s ideal, <30s acceptable).
- SIGTERM → drain in-flight requests → exit clean within 30s.
- Crash-only design: random kill survives. No "graceful shutdown" depended on.
- **Anti**: in-memory queues that lose on shutdown, long-running transactions held open.

### 10 — Dev/prod parity
- Local Docker Compose mirrors prod topology (Postgres + Redis + app).
- No SQLite-in-dev, Postgres-in-prod (different SQL dialects, different bugs).
- Same OS family base image dev → prod.
- **Anti**: "works on my Mac, breaks on Linux container".

### 11 — Logs
- stdout / stderr only. JSON if structured.
- Aggregator (Loki / CloudWatch / Datadog) collects from there.
- Never write logs to disk inside the container.
- **Anti**: app rotates its own log files, mails reports, calls home.

### 12 — Admin processes
- Migrations: `alembic upgrade head` — one-shot container, not in-app.
- Backfills: same pattern.
- Console / REPL: same image, one-shot exec.
- **Anti**: admin endpoints inside the running web app (`/admin/migrate`).

---

## Multi-Tenant Add-Ons (Beyond 12-Factor)

NexusAI's agency context demands extras the original 12 don't cover:

13. **Per-tenant config**: per-client API keys, rate-limit budget, feature flags. Loaded from DB at request time, not env.
14. **Per-tenant observability**: every log line tagged `client_id`. Metrics filterable by tenant.
15. **Per-tenant rate isolation**: token bucket per tenant on hot endpoints; one client's spike doesn't block others.
16. **Per-tenant secret isolation**: client A's IG token never leaves a process handling client B's request.

---

## Compliance Audit (run quarterly)

```
[ ] git log shows main always deploys (no local hacks)
[ ] requirements/lockfile pinned to specific versions
[ ] .env.example exists, .env never committed
[ ] App starts from env vars only (no hardcoded URLs)
[ ] Single Docker image promotes through staging → prod
[ ] grep filesystem writes outside /tmp → none in app code
[ ] App self-binds, runs `python main.py` standalone
[ ] Workers / scheduler are separate processes
[ ] App SIGTERM drains in <30s
[ ] docker-compose up locally = prod topology
[ ] All logs to stdout, JSON if structured
[ ] Migrations run as one-shot job, not at app startup
```

Failing items get tickets, prioritized by blast radius.

---

## Anti-Patterns

- **"It works without env vars in dev."** Dev convenience leaks into prod debugging.
- **Reading config from a file at startup.** That's config-as-code; doesn't compose with secret managers.
- **Sticky sessions.** Couples client to specific instance — kills horizontal scaling and graceful redeploy.
- **Long-running migrations on app start.** Slow boot. New container can't replace old fast enough.
- **In-app cron threads.** Use a real scheduler / cron container.
- **Singleton state in app memory.** Doesn't scale to N processes.

---

## Reference

- 12factor.net (canonical).
- `companies/nexusai/skills/devops/SKILL.md`
- `knowledge/software/observability.md` (factor 11).
- `knowledge/software/cicd-patterns.md` (factor 5).
- `tools/cred_vault.py` (factor 3, agency context).
