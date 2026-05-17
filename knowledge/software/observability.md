# Observability — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.devops`, `@nexusai.backend`

---

## Three Pillars

| Pillar | What | When to query |
|---|---|---|
| **Logs** | Discrete events, free-text or structured. | "What exactly happened at 14:32?" |
| **Metrics** | Numeric time-series, aggregable. | "Is error rate up over the last hour?" |
| **Traces** | Request path across services with timing. | "Where did this slow request spend its time?" |

NexusAI default tooling: OpenTelemetry SDK → OTLP → either (a) Grafana stack (Loki + Prometheus + Tempo) self-hosted, or (b) Datadog if budget allows. Don't pick the third option; pick one and standardize.

---

## Logs — Structured, Always

Format: JSON one-line per event.

```json
{"ts":"2026-05-17T14:32:01.234Z","level":"error","logger":"campaigns.create",
 "request_id":"abc123","client_id":"client_42","user_id":"u_9",
 "msg":"failed to create campaign","error":"budget_negative","budget_cents":-100}
```

Mandatory fields:
- `ts` — ISO 8601 UTC.
- `level` — debug / info / warn / error.
- `request_id` — links log to trace + downstream services.
- `client_id` — agency-critical for tenant filtering.
- `msg` — short, English, no PII.

**Never log**:
- Passwords / API tokens / session cookies / OTP codes.
- Full request body (often contains PII / secrets).
- Stack trace at INFO level (only at ERROR).

**Field-level redaction**: structured logger configured to scrub known sensitive keys (`password`, `token`, `cookie`, `authorization`, `secret`).

---

## Log Levels (use sparingly)

| Level | When |
|---|---|
| `debug` | Off in prod. Local + ephemeral. |
| `info` | Notable normal events: request received, job started, deploy applied. |
| `warn` | Unexpected but handled: retry kicked in, fallback used, deprecated path hit. |
| `error` | Failed to perform requested operation. Page-worthy threshold. |
| `critical` | Reserved for "service down" / "data corruption". Always pages. |

Anti: every line at `info`. Logs become noise. Logs become bills.

---

## Metrics — RED + USE

### RED (per service)
- **R**ate: requests/sec.
- **E**rrors: errors/sec.
- **D**uration: latency distribution (p50, p95, p99).

### USE (per resource: CPU, RAM, disk, queue, conn pool)
- **U**tilization: % busy.
- **S**aturation: queue depth / wait time.
- **E**rrors: hardware/OS errors.

Common counters/gauges to expose:
- `http_requests_total{method, route, status}`
- `http_request_duration_seconds{method, route}`
- `db_pool_in_use / db_pool_size`
- `external_call_total{target, status}`
- `external_call_duration_seconds{target}`
- `queue_depth{queue}`
- `cost_usd_total{model, feature}` — for AI workload cost tracking

**Per-tenant labels**: add `client_id` label to relevant metrics. Cardinality discipline — keep total label combinations <100k or your TSDB will hate you.

---

## Tracing

OpenTelemetry instruments:
- HTTP server / client (auto).
- DB queries (auto via SQLAlchemy / pg driver).
- Redis (auto).
- External API calls (auto via `requests` / `httpx`).
- Custom spans for important business operations:

```python
with tracer.start_as_current_span("campaign.create",
        attributes={"client_id": ctx.client_id, "campaign_name": req.name}):
    # ... business logic
```

Sampling:
- 100% for low-traffic services.
- Tail-based sampling for high-traffic: keep all errors + slow requests + 1% of normal.
- Always keep traces for any 5xx / 4xx-of-interest.

---

## SLOs (Service Level Objectives)

For every user-facing service, define:

| SLI (indicator) | SLO (target) | Window |
|---|---|---|
| Availability (% successful HTTP responses) | 99.9% | 30 days |
| Latency p95 | <300ms | 30 days |
| Error rate | <0.1% | 30 days |

Error budget = (1 − SLO) × time. Spend it on shipping; conserve when budget low.

---

## Alert Discipline

Every alert MUST:
1. Wake (or notify) someone — no "informational" alerts to a muted channel.
2. Be actionable — runbook URL in the alert body.
3. Be accurate — false-positive rate <5%. Else fatigue.
4. Be tied to user impact — alert on symptoms (errors, latency), not causes (CPU 80%).

Anti-pattern: alert on every WARN log. Alert on **change in pattern**: error rate spiked, latency p95 jumped, queue depth growing unbounded.

---

## Dashboards

For each service:
1. **Service overview** (1 page) — RED metrics, error log tail, recent deploys timeline.
2. **Per-tenant slice** (agency-critical) — same metrics filterable by `client_id`.
3. **Per-feature** — track new feature post-launch.
4. **Cost dashboard** — daily / monthly spend by feature, alerting on threshold.

Discipline: kill dashboards no one looks at after 30 days.

---

## Triage Workflow (When Things Break)

```
1. Confirm        — is the alert real? Look at user-facing surface, not just metric.
2. Triage scope   — broad (multi-service) or narrow (one endpoint, one client)?
3. Recent changes — last deploy / config / DB migration in past 60 min? (rollback candidate)
4. Dependency    — DB up? Cache up? External API up?
5. Resource      — CPU/mem/disk/conn pool saturated?
6. Logs at fault — what's actually erroring? Look at last 100 ERROR lines.
7. Trace          — where in the call graph does latency spike?
8. Hypothesis    — form one. Test cheap (read-only) before mutating.
9. Mitigate      — feature flag off, scale up, restart, rollback. Whichever cheapest.
10. Postmortem    — within 5 days. Blameless. Action items tracked.
```

Don't skip to "restart the server" — restart hides root cause.

Reference: `knowledge/security/incident-runbook.md`.

---

## Cost Observability (Often Skipped)

Modern apps leak money quietly:
- LLM token spend per feature / per client.
- Cloud egress per region.
- DB IOPS for unindexed reports.
- Logging bill (Datadog dollar-per-GB-ingested).

Track these as metrics. Alert on monthly trend.

---

## Anti-Patterns

- **`print()` in production code.** Use the structured logger.
- **Logging full request/response bodies "for debugging"**. PII / secrets in logs = breach.
- **Alerting on every WARN.** Pager fatigue, alerts ignored.
- **Dashboards no one reads.** Kill them.
- **Metrics without tenant tag (agency context).** Can't slice "this client's pipeline broke".
- **No request_id propagation.** Logs across services unjoinable.
- **Tracing turned off because "expensive".** Sample, don't disable.
- **Logs as the only observability.** Logs are expensive to query at scale; use metrics for dashboards, logs for forensics.

---

## Reference

- `companies/nexusai/skills/devops/SKILL.md`
- `knowledge/software/twelve-factor.md` (factor 11 — logs).
- `knowledge/security/incident-runbook.md` (triage detail).
- OpenTelemetry docs (canonical instrumentation reference).
- Google SRE book (chapter on monitoring).
