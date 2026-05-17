# Incident Runbook — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.security`, `@nexusai.devops`, on-call

When something is broken in production, follow this. Don't improvise.

---

## Severity Levels

| Sev | Definition | Response |
|---|---|---|
| **P0** | Customer impact, data loss, security breach, payment broken, full outage. | Drop everything. Page Fathur. Postmortem mandatory. |
| **P1** | Single-tenant outage, primary feature broken, severe degradation. | Same-day fix. Postmortem if recurring. |
| **P2** | Workaround exists, secondary feature broken, performance regression. | This-week fix. |
| **P3** | Cosmetic / edge case / internal-only. | Backlog. |

If unsure: **start at P1, downgrade if proven less severe**. Never start at P3 and discover it was P0.

---

## Phase 1 — Confirm (5 min max)

Before pager:
- [ ] Reproducible? Can I see the symptom myself, or is it monitoring noise?
- [ ] Real or synthetic? Did a real user / client notice, or is it only an internal alert?
- [ ] Scope? Single tenant, multi-tenant, full?
- [ ] Recent change? Last deploy / config / migration in past 60 min?

Output: **5-line incident summary** + severity.

```
[INCIDENT-2026-05-17-01]
What:    Campaign create endpoint returning 5xx for client_42.
Scope:   1 client confirmed; checking others.
Started: ~14:32 UTC, ~10 min ago.
Severity: P1.
Recent:  Deploy 14:25, includes campaign-validation refactor.
```

---

## Phase 2 — Contain (next 5–15 min)

Stop the bleeding before fixing.

Decision: **rollback or roll-forward?**

| Situation | Action |
|---|---|
| Recent deploy, error rate up | **Rollback to last known good.** ~1 min via `kubectl rollout undo` / re-deploy prev tag. |
| No deploy, external dep down | Wait + circuit break. |
| Bad config | Revert config; reload. |
| Compromised credential / token | **Revoke the credential immediately.** Rotate. Investigate after. |
| Data being corrupted | **Disable the writer path** (feature flag off). Triage data afterward. |
| Suspected breach | Disconnect affected systems from network. **Preserve evidence before remediating.** |

Output: incident moves from "still degrading" to "stable, root cause TBD".

---

## Phase 3 — Preserve (BEFORE remediation, if forensic-relevant)

If incident is **security-suspected** or **data-loss-suspected**:

- [ ] Snapshot DB state (pg_dump / cloud snapshot).
- [ ] Capture relevant log windows (write to S3 outside affected system).
- [ ] Capture process memory dump if RCE suspected (`gcore <pid>`).
- [ ] Note current time + actor of every action.
- [ ] Don't `rm` anything. Move to a quarantine path.

For ops incidents (not security): skip this phase. Move to remediation.

---

## Phase 4 — Notify

Internal:
- [ ] Fathur — always for P0/P1.
- [ ] Team chat — incident channel with rolling timeline.

External (Fathur's call):
- [ ] Affected clients — when impact >30 min and visible to them.
- [ ] Status page — when broad impact.
- [ ] Regulator — if breach involves regulated data + jurisdiction requires.

Communication template (for affected client):
```
We're investigating an issue affecting [feature] starting at [time].
We've contained it as of [time]. [Optional: customer impact summary.]
We'll send an update by [time]. Sorry for the disruption.
— Fathur
```

Do NOT speculate on cause in customer comms until confirmed.

---

## Phase 5 — Eradicate (root cause)

After containment, find the actual cause:

```
Hypothesis 1: <specific cause>
Test:         <cheap read-only check>
Result:       <yes/no>

If no, Hypothesis 2: ...
```

Test cheaply (logs, traces, replicate locally) before invasive (restart prod, hot patch).

Common patterns:
- Recent deploy → rollback proves cause if symptom resolves.
- DB connection storm → exhausted pool; missing pooler or connection leak.
- External API down → check their status page.
- Data corruption → query path bypassing tenant filter.
- Credential breach → unusual login pattern, audit log review.

Once root cause confirmed: **patch or rollback**. Don't ship the fix without verifying.

---

## Phase 6 — Recover

- [ ] Service restored (verified via the same probe that detected).
- [ ] Backlog drained (queued work processed).
- [ ] Affected data corrected if needed (replay events, restore from backup).
- [ ] Monitoring confirms stable for ≥30 min before declaring resolved.
- [ ] Affected clients notified resolution.

---

## Phase 7 — Postmortem (within 5 days)

Mandatory for P0/P1. Format:

```
[POSTMORTEM] <incident-id>
Severity:   <P0/P1>
Duration:   start → contained → resolved
Impact:     <users / clients / data affected>

[TIMELINE]
14:32 — first error in logs
14:34 — alert fired
14:35 — engineer ack'd
14:38 — confirmed real
14:42 — rollback initiated
14:45 — service restored
15:30 — root cause identified
17:00 — long-term fix deployed

[ROOT CAUSE]
<single sentence + supporting paragraph>

[CONTRIBUTING FACTORS]
- Why didn't tests catch?
- Why didn't review catch?
- Why didn't earlier monitoring catch?

[ACTION ITEMS]
[ ] Add test for edge case X.       (owner: <agent>, due: <date>)
[ ] Add monitoring on signal Y.     (owner: <agent>, due: <date>)
[ ] Update runbook for class Z.     (owner: <agent>, due: <date>)

[LESSONS]
What we'd tell our past selves.
```

Discipline:
- **Blameless.** "The system allowed X to happen" not "Alice caused X".
- **Action items tracked to closure** — don't write the postmortem and forget the fixes.
- **Shared.** Read by the whole team, even if not on call.

---

## Common Incident Patterns + First Move

| Symptom | First check |
|---|---|
| All endpoints 5xx | DB up? Network up? Recent deploy? |
| Slow everything | DB connection pool full? Long-running query? GC pause? |
| Spike in 401/403 | Auth provider issue? Token rotation gone wrong? |
| One tenant's pipeline broken | Their credential expired? Their external API down? Their data shape changed? |
| Disk full | Logs rotation broken? Temp files leaking? Backup not cleaning up? |
| Cost spike | LLM in retry loop? Egress regression? Forgotten cron multiplied? |
| Account flagged on platform | Pacing exceeded? IP burned? Fingerprint cluster detected? See `opsec-multi-account.md`. |
| Unauthorized access alert | Don't restart yet. Preserve logs first. Then revoke + rotate. |
| Data appears wrong | Hold writes. Diff against backup. Identify scope before remediation. |

---

## Anti-Patterns

- **"Restart it" before knowing why.** Hides the cause; recurs.
- **Skip postmortem for "small" P1.** Patterns in small incidents predict the big one.
- **Investigate from production.** Reproduce in staging if possible; protect prod.
- **Speculate to clients before confirmed.** Damage compounds when retraction needed.
- **Solo war room.** Bus factor. Bring at least one second pair of eyes.
- **No timeline notes.** Postmortem is impossible without rolling timestamp.
- **Action items without owner + date.** They never close.
- **Blame the engineer.** Look at the system that allowed it. Engineers leave; systems stay.

---

## Reference

- `companies/nexusai/skills/security/SKILL.md`
- `companies/nexusai/skills/devops/SKILL.md`
- `knowledge/software/observability.md`
- `knowledge/security/threat-modeling-stride.md`
- Google SRE book — incident management chapter.
