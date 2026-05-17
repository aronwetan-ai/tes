# NexusAI Skill Index

Versi: 1.1
Last updated: 2026-05-17 (post Update 10 — NexusAI deepening)

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → NexusAI SOUL.

---

## Active Skills (7 parent + 3 agent-specific deep skills = 10 total)

### Parent skills (used by multiple agents)

| Skill | Path | Primary Users |
|---|---|---|
| coding | `skills/coding/SKILL.md` | @nexusai.backend, @nexusai.frontend, @nexusai.cto |
| devops | `skills/devops/SKILL.md` | @nexusai.devops, @nexusai.cto, @nexusai.security |
| security | `skills/security/SKILL.md` | @nexusai.security, @nexusai.cto |
| ml-agent | `skills/ml-agent/SKILL.md` | @nexusai.ml, @nexusai.cto |
| automation | `skills/automation/SKILL.md` | @nexusai.devops, @nexusai.backend, @nexusai.ml |
| qa | `skills/qa/SKILL.md` | @nexusai.qa, @nexusai.cto, @nexusai.backend, @nexusai.frontend |
| uiux | `skills/uiux/SKILL.md` | @nexusai.frontend, @nexusai.cto |

### Agent-specific deep skills (Update 10)

These extend a parent skill with depth that's primarily owned by one agent. They're loaded in addition to (not instead of) the parent skill.

| Skill | Path | Owner | Parent |
|---|---|---|---|
| threat-modeling | `skills/security/threat-modeling.md` | @nexusai.security | security |
| acceptance-criteria-templates | `skills/qa/acceptance-criteria-templates.md` | @nexusai.qa | qa |
| prompt-eval | `skills/ml-agent/prompt-eval.md` | @nexusai.ml | ml-agent |

---

## What Was Deepened in Update 10

Each parent skill now has a **Senior Patterns (Deep Dive)** section appended. Highlights:

- **coding** — Architecture decision tree (stateless vs stateful, sync vs async, when to split bounded contexts), multi-tenant patterns (row-level + RLS), error categorization (programmer vs operational vs business), API contract patterns, boring-tech baseline table.
- **devops** — Deploy strategy decision tree (rolling/blue-green/canary/expand-and-contract), 12-factor compliance defaults, multi-tenant infra, CI/CD pattern trade-offs, observability triage, secrets handling, cost optimization, disaster recovery checklist.
- **security** — STRIDE applied to typical agency feature (worked example), OWASP Top 10 cheatsheet, auth pattern decision matrix, OPSEC playbook for multi-account/scraping work, credential vault discipline, incident response compressed.
- **ml-agent** — Agent design pattern, prompt-as-code discipline, eval methodology (Tier 1/2/3), prompt injection defenses, cost control patterns, tool-calling design, memory strategy, agency-context AI tooling map.
- **automation** — Multi-account orchestration template, cold outreach pipeline architecture, scraping pipeline patterns, pipeline reliability (idempotency/checkpoint/DLQ/backoff/circuit breaker), cron discipline, inter-process communication picker.
- **qa** — Senior code review priority order, agency-scale AC dimensions (tenant isolation, permission, failure, rate limit, empty state, concurrent, audit), test strategy by code type, bug severity calibration, deepened review output template.
- **uiux** — SaaS dashboard archetype, client switcher pattern (multi-tenant UX), form patterns by complexity, empty/loading/error state hierarchies, accessibility baseline, frontend state decision tree, design tokens.

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because they don't fit NexusAI's IT / SaaS / cloud / AI agents focus:

- `content` — marketing copy → use BrandFlow (`@brandflow.copywriter`).
- `research` — market research → use BrandFlow (`@brandflow.cmo`) or Crypto Consultant for crypto-specific.
- `business` — business / SOP design → that's the CEO's role + companies/<co>/identity.

---

## Tools Available to NexusAI Agents (post Update 10)

All entries in `knowledge/tools/tool-registry.md`.

**Local utility (Risk=Low, whitelistable):**
- `tools/json_schema_check.py` — validate JSON output against schema.
- `tools/markdown_lint.py` — doc quality check.
- `tools/dep_audit.py` — outdated/vulnerable dep scan.
- `tools/api_health.py` — single-URL health probe + latency.
- `tools/prompt_eval.py` — local eval runner for AI agents.

**Agency-context (mixed risk):**
- `tools/cred_vault.py` — encrypted per-client credential vault (Medium for writes).
- `tools/secret_scanner.py` — Risk=Low; pre-commit / CI scan for leaked secrets.
- `tools/exif_extract.py` — Risk=Low; metadata extraction from images.
- `tools/reverse_image_lookup.py` — Risk=Low; URL builders for image search engines.
- `tools/osint_lookup.py` — Risk=Low; identifier-pivot OSINT (phone/email/username).

**Existing (foundational):**
- `tools/fear_greed.py`, `tools/btc_price.py`, `tools/news_sentiment.py` — for `@crypto.*` mostly, but available cross-company.
- `bin/log_task.py` / `update_task.py` / `list_tasks.py` / `log_message.py` / `archive_*.py` / `recap_manager.py` — task logger system.

What NexusAI does NOT build: see `knowledge/scope/declined-tools.md`. Two specific items declined; substitutes provided.

---

## Knowledge References (post Update 10)

Domain knowledge files relevant to NexusAI agents. See `companies/nexusai/SOUL.md` for the per-task loading guidance.

**Software patterns (12 files):**
- `knowledge/software/clean-architecture.md`
- `knowledge/software/api-design.md`
- `knowledge/software/twelve-factor.md`
- `knowledge/software/ddd-cheatsheet.md`
- `knowledge/software/cicd-patterns.md`
- `knowledge/software/code-review-checklist.md`
- `knowledge/software/cap-and-consistency.md`
- `knowledge/software/observability.md`
- `knowledge/software/postgres-prod.md`
- `knowledge/software/auth-patterns.md`
- `knowledge/software/frontend-state.md`
- `knowledge/software/tech-writing.md`
- `knowledge/software/adr-format.md`
- `knowledge/software/software-development-sop.md` (existing, foundational)

**Security (4 files):**
- `knowledge/security/owasp-top10.md`
- `knowledge/security/threat-modeling-stride.md`
- `knowledge/security/incident-runbook.md`
- `knowledge/security/opsec-multi-account.md`

**Agile / process (2 files):**
- `knowledge/agile/scrum-kanban.md`
- `knowledge/agile/agile-manifesto.md`

**ML / AI agent (2 files):**
- `knowledge/ml/prompt-engineering.md`
- `knowledge/ml/eval-methodology.md`

**Scope (1 file):**
- `knowledge/scope/declined-tools.md` — boundaries on what is NOT built.

---

## How To Use

Agents call skills by reference, not duplication. When a task arrives:

1. Identify which skill(s) apply (parent skill + agent-specific deep skill if you own one).
2. Read the skill file for process + output format.
3. Apply the skill's rules to the task.
4. Use the skill's output template.
5. Load relevant `knowledge/` cheatsheets per the skill's References section.

If a skill conflicts with the agent's Tier 3 SOUL, the SOUL wins (it's more specific). If a skill conflicts with the company's Tier 2 SOUL, the SOUL wins. Root SOUL always wins above all.

---

## Adding New Skills

When a behavior pattern emerges that's used by 2+ agents and isn't covered:

1. Decide if it should be **company-specific** (here) or **cross-company** (`knowledge/sop/`).
2. Decide if it's a **parent skill** (multi-agent, broad) or an **agent-specific deep skill** (extends a parent, owned by one agent).
3. Create file:
   - Parent: `skills/<skill-name>/SKILL.md`
   - Deep: `skills/<parent-skill-name>/<deep-skill-name>.md`
4. Use the standard front-matter:
   ```yaml
   ---
   name: skill-name
   description: One-line description.
   company: NexusAI
   used_by: ["@nexusai.role1", "@nexusai.role2"]
   # for deep skills also include:
   # agent_specific: "@nexusai.<role>"
   # parent_skill: <parent-skill-name>
   ---
   ```
5. Update this index.
6. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/nexusai/SOUL.md` (Tier 2 — company personality, agency context, knowledge loading order).
- `companies/nexusai/AGENTS.md` (role roster).
- `knowledge/software/software-development-sop.md` (foundational SOP).
- `knowledge/scope/declined-tools.md` (scope boundaries).
- `knowledge/tools/tool-registry.md` (full tool registry, 22 entries post Update 10).
