# CI/CD Patterns — Senior Cheatsheet

Versi: 1.0  ·  Update: 2026-05-17  ·  Audience: `@nexusai.devops`, `@nexusai.backend`, `@nexusai.cto`

---

## Branching Strategies — Trade-offs

| Strategy | Use when | Avoid when |
|---|---|---|
| **Trunk-based** | Small team (<10 devs), fast delivery, feature flags available, automated tests trustworthy. | Regulated env requiring segregated promotion, no flag system. |
| **GitFlow** (`develop` + `release` branches) | Versioned product (e.g. mobile app), scheduled releases, multiple parallel versions in support. | Solo / small team — overhead exceeds benefit. |
| **Release branches per client** | Different clients on different versions (legacy reality). | Default — usually a smell, fix the cause. |

**NexusAI default**: trunk-based + Docker tag = git SHA + manual promote staging → prod. No `develop` branch.

---

## CI Pipeline Stages (NexusAI default)

```
git push
  ↓
[1] Lint + format check         (10s)   block on fail
  ↓
[2] Type check                  (30s)   block on fail
  ↓
[3] Unit tests                  (1m)    block on fail
  ↓
[4] Integration tests           (3m)    block on fail
  ↓
[5] Security scan + dep audit   (1m)    warn-only initially, block-on-critical eventually
  ↓
[6] Build container             (2m)    tag = git SHA
  ↓
[7] Push to registry            (30s)
  ↓
[8] Deploy to staging           (1m)    auto on main branch
  ↓
[9] Smoke test                  (1m)    block prod promotion on fail
  ↓
[10] Manual approve → prod      (human gate)
```

Total target: <10 minutes wall-clock for happy path.

---

## Test Pyramid Allocation

| Layer | Share | Speed | Example |
|---|---|---|---|
| Unit | 70% | <1ms each | Pure logic, value objects, domain rules. |
| Integration | 25% | 10–500ms each | Repo against real DB (testcontainers), external client against mock. |
| E2E | 5% | 1–10s each | Critical user journey only. Login + 1 happy path. |

**Anti**: bottom-heavy E2E suite (slow + flaky + high false-fail rate).

---

## Deployment Strategies — Decision Tree

```
What's the blast radius of a bad deploy?
├─ Single non-revenue client          → rolling, monitor 15 min.
├─ Multiple paying clients            → blue/green, 10% canary first.
├─ Foundational shared service        → blue/green + 1% canary + 24h soak.
└─ Database migration                 → expand-and-contract pattern (no inline drops).
```

### Rolling deploy
- Replace pods/instances one-by-one.
- Cheap. Default for most services.
- Risk: brief mixed-version state during deploy. App must tolerate (backward-compatible API + DB).

### Blue/green
- Two identical environments. Switch traffic at the load balancer.
- Instant rollback. Higher infra cost (2x during cutover).
- Default for paying-client services.

### Canary
- Send N% of traffic to new version. Compare error rate / latency. Promote on green.
- Best for risky changes, high-traffic services.
- Needs reliable per-version metric tagging.

### Expand-and-contract (DB migrations)
```
1. Add new column / table (backward compatible).
2. Deploy code that writes to BOTH old + new.
3. Backfill data: old → new.
4. Deploy code that reads from new only.
5. Deploy code that stops writing to old.
6. Drop old (only after window proves safe — typically 1 week).
```
Never drop columns inline with code that reads them — that's how "deploy at 5pm Friday" goes wrong.

---

## Feature Flags

When trunk-based, decouple deploy from release:

```python
if flag("new-reporting-pipeline", client_id):
    return new_reporting(client_id)
return legacy_reporting(client_id)
```

Flag types:
- **Release**: gate incomplete features in main.
- **Experiment**: A/B test a new path.
- **Ops**: kill switch for problematic features.
- **Permission**: feature gated to certain clients/roles.

Discipline:
- Every flag has an owner + creation date + removal date.
- Quarterly review: kill flags older than 6 months that are 100%-on or 100%-off.
- Don't ship a flag without a rollback plan.

---

## Rollback Patterns

| Failure detected | Fix |
|---|---|
| Bad code, no DB migration | Re-deploy previous Docker tag. ~1 min. |
| Bad code + benign migration | Re-deploy previous tag; migration stays applied (was additive per expand-and-contract). |
| Bad code + breaking migration | This shouldn't exist (you didn't expand-and-contract). Forward fix or restore from backup. |
| Bad config | Revert config; redeploy. |
| Bad data after batch job | Restore affected rows from backup or reverse-transform. |

**Always have a one-line rollback command** documented in the deploy ticket. If you can't articulate it before deploy, don't deploy.

---

## Secrets in CI

- CI never logs secret values. Mask them in CI tool config.
- Per-environment secrets injected at deploy, not build.
- No secrets in built artifacts (no baked-in API keys in images).
- CI service account has minimum permissions (deploy this service, push to this registry, nothing else).

---

## NexusAI Concrete Toolchain (defaults)

- **CI host**: GitHub Actions (default), GitLab CI as fallback. Self-hosted runners only if cost > $50/mo.
- **Container registry**: GHCR for code in GitHub. Otherwise self-hosted or AWS ECR.
- **Image base**: `python:3.12-slim` / `node:20-slim` / `alpine` only when cold-start matters.
- **Tag scheme**: `<service>:<git-sha-7>` plus `<service>:<branch>` for staging.
- **Deploy target**: single VPS + systemd + Cloudflare Tunnel for small services. K8s only when fleet >10 services.
- **Secret manager**: SOPS + age (in-repo encrypted), or HashiCorp Vault for medium scale, or `tools/cred_vault.py` for AI Holding internal.

---

## Branch Protection Rules (NexusAI required)

On `main`:
- [ ] Require PR (no direct push).
- [ ] Require ≥1 approving review.
- [ ] Require all CI checks pass.
- [ ] Dismiss stale approvals when new commit pushed.
- [ ] Require linear history (rebase or squash).
- [ ] No force-push.
- [ ] Branch up-to-date before merge.

---

## Commit Message Convention (Conventional Commits)

```
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

Types: `feat` `fix` `chore` `docs` `style` `refactor` `test` `perf` `build` `ci` `revert`

```
feat(campaigns): support time-windowed launch
fix(auth): handle expired refresh token
docs(api): document idempotency-key header
chore(deps): bump fastapi 0.110 → 0.112
```

Why: enables auto-changelog generation, semver bumps, signal-quality grep.

---

## Anti-Patterns

- **Manual deploys.** No audit trail, no consistency, key person bus risk.
- **Tests skipped via `skip_ci` to ship fast.** Find a way to fix the test, not bypass.
- **CI that takes 30+ minutes.** Devs work around it. Optimize.
- **No staging environment.** "We test in prod." Eventually a major incident.
- **Deploy on Friday.** Unless hotfix, wait until Monday.
- **One giant pipeline that builds 20 services.** Build only what changed.
- **Secrets in CI logs.** Audit logs. If found, rotate immediately.
- **`latest` tag in production.** Pin to SHA. Reproducibility.

---

## Reference

- `companies/nexusai/skills/devops/SKILL.md`
- `knowledge/software/twelve-factor.md` (factor 5).
- `knowledge/software/observability.md` (deploy monitoring).
- `knowledge/security/incident-runbook.md` (rollback in incident).
