---
name: devops
description: Deployment / infrastructure / observability skill for NexusAI. Specialized for cloud / SaaS / Linux / WSL context.
company: NexusAI
used_by: ["@nexusai.devops", "@nexusai.cto", "@nexusai.security"]
---

# DevOps Skill — NexusAI

Operational reliability. Use for anything that touches infrastructure, deployment, or production behavior.

Inherits NexusAI SOUL (engineering-precise, pragmatic). Reliability-first thinking — what breaks, why, how to detect, how to roll back.

## When to Use

- CI/CD pipeline design.
- Container / orchestration config (Docker, K8s).
- Infrastructure as code (Terraform, Ansible, Pulumi).
- Monitoring / logging / alerting setup.
- Production incident response + post-mortem.
- Cost optimization (right-sizing, idle cleanup).
- Disaster recovery plan.
- Cloudflare Tunnel / Nginx / reverse proxy.

## Process — Standard Deploy

Per `knowledge/software/software-development-sop.md`:

**Before deploy**:
1. Code reviewed (`@nexusai.cto` or peer).
2. Tests pass.
3. Migration script ready (DB change).
4. Rollback plan documented.

**During deploy**:
1. Staging first. Smoke test there.
2. Production deploy.
3. Monitor logs ≥ 15 minutes.

**After deploy**:
1. Notify stakeholder.
2. Log to `companies/nexusai/MEMORY.md`: date, version, what changed, observed impact.

## Rules

1. Prefer safe / dry-run flags before destructive ops.
2. Explain destructive commands before running. Get explicit confirmation.
3. Separate local / staging / production rigorously.
4. Never expose secrets in logs / commits / config files.
5. Every alert needs a runbook. No silenced unexplained alerts.
6. Rollback plan exists BEFORE deploy, not after.

## Output Format

For deployment plan:
```
[CONTEXT]       What's deploying + why now
[STEPS]         Numbered, executable
[PRE-CHECKS]    Things to verify before starting
[ROLLBACK]      Exact undo command
[MONITORING]    Metrics + thresholds to watch
[OWNER]         Who's on call
[POST-DEPLOY]   Verification checklist
```

For infra design:
```
[GOAL]          What this serves
[COMPONENTS]    Services + relationships
[CAPACITY]      Expected load + headroom
[FAILURE MODES] What breaks when X is down
[COST]          Estimated $/mo
[NEXT STEP]     Provision / migrate / monitor
```

For incident:
```
[INCIDENT]     What, severity, scope
[TIMELINE]     Time-stamped events
[ROOT CAUSE]   Confirmed or hypothesized
[FIX]          What was done
[FOLLOW-UP]    Action items to prevent recurrence
```

## Cross-Skill / Cross-Agent

- Code being deployed → `@nexusai.backend` + `skills/coding`.
- Security hardening → `@nexusai.security`.
- ML model deployment → `@nexusai.ml`.
- Test the pipeline → `@nexusai.qa` + `skills/qa`.
- Architecture-level decisions → `@nexusai.cto`.

## Senior Patterns (Deep Dive)

### Deploy strategy decision tree

```
What's the blast radius of a bad deploy?
├─ Single non-revenue client          → rolling deploy, monitor 15 min.
├─ Multiple paying clients            → blue/green, 10% canary first.
├─ Foundational shared service        → blue/green + 1% canary + 24h soak.
└─ Database migration                 → expand-and-contract, never drop columns inline.
```

### Twelve-factor compliance defaults

NexusAI services must hit all twelve. Cheatsheet:

| Factor | NexusAI default |
|---|---|
| Codebase | Single repo per service, `main` branch deployable. |
| Dependencies | `requirements.txt` / `package.json` pinned, `pip-tools` / `pnpm` lockfile committed. |
| Config | `.env` for dev, vault / secret manager for prod. Never in repo. |
| Backing services | Connection string from env. Easy swap dev → staging → prod. |
| Build / release / run | Docker image = artifact. Tag = git SHA. Run config = env vars. |
| Processes | Stateless. State in DB / cache / S3. |
| Port binding | App self-binds, reverse proxy in front. |
| Concurrency | Horizontal scale via process count, not threads. |
| Disposability | SIGTERM handled; drain in <30s. |
| Dev/prod parity | Docker Compose mirrors prod topology. |
| Logs | stdout JSON. Aggregator handles routing. |
| Admin processes | Migrations as one-shot containers, not in-app. |

Reference: `knowledge/software/twelve-factor.md`.

### Multi-tenant infra pattern (agency context)

Per-client compute usually wasteful at agency scale (20–50 clients, mostly idle). Default pattern:

- **Shared compute, isolated data**: one app cluster, row-level tenant isolation in DB, per-client Redis namespace.
- **Per-client secrets**: every external integration token (Meta Ads, Google Analytics, IG Graph API, etc.) lives in `cred_vault` keyed by `client_id`. Service fetches token by client_id at request time, never caches across clients.
- **Per-client rate limit budget**: each external API has a budget per client to avoid one client burning the others' quota.
- **Per-client observability tag**: every log line and metric has `client_id` label so you can slice "Client X's pipeline failed" without scanning all logs.

### CI/CD patterns (trade-off)

| Pattern | Use when | Avoid when |
|---|---|---|
| Trunk-based + feature flag | Small team, fast delivery, feature gating in app | No flag system, regulated env requiring segregated promotion |
| GitFlow (`develop`/`release` branches) | Versioned product, scheduled releases | Solo / small team — branch overhead exceeds benefit |
| Release branches per client | Clients on different versions (legacy) | Default — usually a smell, fix the cause |

NexusAI default for agency work: **trunk-based + Docker tag = git SHA + manual promote staging → prod**. No `develop` branch overhead.

Reference: `knowledge/software/cicd-patterns.md`.

### Observability triage

When something's wrong, look in this order:

1. **External signal** — user / monitor reported what?
2. **SLO / error rate** — is it broad or one endpoint?
3. **Recent changes** — last deploy / config change / schema migration in last hour?
4. **Dependency health** — DB / Redis / external API up?
5. **Resource saturation** — CPU / mem / disk / connections / goroutines?
6. **Logs at the failure path** — what's the actual error trace?
7. **Distributed trace** — where in the call graph?

Don't open the IDE before step 3. Don't restart prod before step 4 (restart hides root cause).

Reference: `knowledge/software/observability.md`, `knowledge/security/incident-runbook.md`.

### Secrets handling (agency reality)

- **Sources of truth**: vault (Bitwarden / 1Password / HashiCorp Vault / `tools/cred_vault.py` for AI Holding-internal).
- **Distribution**: env-injected at runtime, never committed, never in container layers.
- **Rotation**: rotate per-client tokens on freelancer offboarding, every 90 days otherwise. Calendar reminder, not "we'll get to it".
- **Audit**: every read of a credential gets logged with timestamp + actor + reason. Your log is your alibi.
- **Pre-commit**: `tools/secret_scanner.py` runs in pre-commit hook + CI. Block on detection, not just warn.

### Cost optimization patterns

| Smell | Likely fix |
|---|---|
| EC2/VPS at 5% avg CPU 24/7 | Right-size or move to serverless. |
| K8s cluster running 1 service | Switch to single VM + systemd. |
| Datadog bill > infra bill | Drop to Grafana stack + selective external for incident-only. |
| 50 RDS instances (one per client) | Consolidate to 1 instance + tenant isolation; only split for compliance reasons. |
| LLM bill dominated by retry | Cache successful responses keyed by (model, prompt hash). |
| Egress bills | Move heavy traffic to provider with free egress (Cloudflare R2, Bunny). |

### Disaster recovery checklist

For every production system NexusAI runs:

- [ ] DB backed up daily, encrypted at rest, retention ≥ 30d.
- [ ] Restore tested ≥ once per quarter (untested backup = no backup).
- [ ] Runbook exists for `database lost`, `region lost`, `auth provider lost`, `payment provider lost`.
- [ ] Critical secrets escrowed (someone other than Fathur knows where the recovery seed is, encrypted).
- [ ] Status page or comms plan for clients during outage.

### Anti-patterns NexusAI rejects

- **"It works on my machine" prod debugging**. If it's broken in prod, fix in prod *artifacts* (logs, traces, replay), not by re-running locally.
- **Deploy on Friday afternoon**. Unless hotfix.
- **Manual prod commands without trail**. Every prod command goes through a logged channel (CI, runbook, audit-logged jumphost).
- **Snowflake servers**. Configured by hand, no IaC, no one knows how they got that way. Burn and rebuild.
- **Alerts that nobody reads**. Either it pages someone or it doesn't exist. No "informational" alerts that get muted.

## Reference

- `knowledge/software/software-development-sop.md`
- `knowledge/software/twelve-factor.md`
- `knowledge/software/cicd-patterns.md`
- `knowledge/software/observability.md`
- `knowledge/software/postgres-prod.md`
- `knowledge/security/incident-runbook.md`
- `knowledge/security/opsec-multi-account.md`
- `companies/nexusai/agents/devops.md`
