# BrandFlow Skill Index

Versi: 1.1
Last updated: 2026-05-17 (post Update 11 — BrandFlow deepening)

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → BrandFlow SOUL.

---

## Active Skills (7 parent + 3 agent-specific deep skills = 10 total)

### Parent skills (used by multiple agents)

| Skill | Path | Primary Users |
|---|---|---|
| content | `skills/content/SKILL.md` | @brandflow.copywriter, @brandflow.cmo, @brandflow.writer |
| design | `skills/design/SKILL.md` | @brandflow.designer, @brandflow.cmo |
| community | `skills/community/SKILL.md` | @brandflow.community, @brandflow.cmo |
| seo | `skills/seo/SKILL.md` | @brandflow.seo, @brandflow.copywriter, @brandflow.writer |
| research | `skills/research/SKILL.md` | @brandflow.cmo, @brandflow.copywriter, @brandflow.analytics |
| automation | `skills/automation/SKILL.md` | @brandflow.pm, @brandflow.social, @brandflow.analytics |
| qa | `skills/qa/SKILL.md` | @brandflow.qa, @brandflow.cmo, @brandflow.community |

### Agent-specific deep skills (Update 11)

These extend a parent skill with depth that's primarily owned by one agent. They're loaded in addition to (not instead of) the parent skill.

| Skill | Path | Owner | Parent |
|---|---|---|---|
| hook-library | `skills/content/hook-library.md` | @brandflow.copywriter | content |
| crisis-playbook | `skills/community/crisis-playbook.md` | @brandflow.community | community |
| format-adaptation | `skills/design/format-adaptation.md` | @brandflow.designer | design |

---

## What Was Deepened in Update 11

Each parent skill now has a **Senior Patterns (Deep Dive)** section appended. Highlights:

- **content** — Voice capture before writing (multi-brand discipline), hook selection decision tree, cold/warm/hot audience calibration, "one idea" discipline, specificity ladder, CTA hierarchy by funnel stage, senior self-edit pass, repurposing discipline (one brief → 3 formats), senior brief-to-draft template.
- **design** — Visual voice profile per client, 3-level hierarchy rule, composition patterns by format, carousel design pattern, color roles (not "color choices"), typography discipline (sizes / line length / pairing), accessibility as constraint, asset pipeline (source → derivative), the "strip" pass, layout-spec-as-renderer-contract, cross-brand senior workflow.
- **community** — Multi-brand reply voice discipline, expanded triage matrix v2, 3-beat reply pattern, reply timing rules, drop-the-rope pattern, crisis early warning signals, Boundary #4 operationalization, reply-approval queue JSONL schema, sentiment reporting cadence.
- **seo** — Search intent classification, topical authority over single article, keyword tier system, SERP reverse-engineering before writing, on-page structure for modern SEO, E-E-A-T, refresh/re-optimize pattern, AI overviews / SGE optimization, technical SEO coordination points, KPI stack by client tier.
- **research** — 3 research modes (discovery/validation/reporting), 3-layer persona, persona source hierarchy, voice-of-customer mining method, competitive audit (direct + adjacent), trend triage, channel benchmark research, hashtag/community research.
- **automation** — Multi-tenant editorial pipeline (per-client compartmentalization), full state machine, canonical pipeline JSONL schema, Boundary #4 hardcoded gate, brief validation (refuse incomplete briefs), cron/scheduler layer, performance pipeline (publish→report), UTM convention, A/B test discipline.
- **qa** — Review layers (don't skip), severity calibration, voice drift detection method, fact-checking hierarchy, cluster drift detection (cross-piece patterns), approval-path discipline (Boundary #4), senior QA output templates, common editorial failures, approval speed discipline, brand-aware approval tier per client.

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because they don't fit BrandFlow's marketing / content / branding focus:

- `coding` — engineering work → use NexusAI (`@nexusai.backend`).
- `devops` — infrastructure → use NexusAI (`@nexusai.devops`).
- `business` — business / SOP design → CEO + identity files.
- `uiux` — product UI → use NexusAI (`@nexusai.frontend` + `skills/uiux`). BrandFlow's `design` skill covers marketing visuals, NOT product UI.

---

## Tools Available to BrandFlow Agents (post Update 11)

All entries in `knowledge/tools/tool-registry.md`.

**Marketing tools (Update 11, mostly Risk=Low):**
- `tools/utm_builder.py` — convention-validating UTM URL builder.
- `tools/readability_check.py` — Flesch + sentence rhythm + per-channel length compliance + markdown structure.
- `tools/brand_voice_lint.py` — voice-drift scoring against locked client voice profile.
- `tools/content_scheduler.py` — editorial pipeline state machine + Boundary #4 gate enforcement (Risk=Medium for mutating sub-commands).
- `tools/social_monitor.py` — sentiment + cluster + crisis-tier suggestion.

**Existing cross-company tools (relevant subset):**
- `tools/news_sentiment.py` — for trend / audience-sentiment scans.
- `tools/markdown_lint.py` — doc quality on long-form output.
- `bin/log_task.py` / `update_task.py` / `list_tasks.py` / `log_message.py` / `archive_*.py` / `recap_manager.py` — task logger system shared across companies.

What BrandFlow does NOT build: see `knowledge/scope/declined-tools.md`. Two agency-specific items declined; substitutes provided (Items 3 and 4 of that file).

---

## Knowledge References (post Update 11)

Domain knowledge files relevant to BrandFlow agents. See `companies/brandflow/SOUL.md` for the per-task loading guidance.

**Marketing cheatsheets (10 files):**
- `knowledge/marketing/marketing-sop.md` (foundational SOP — pre-existing)
- `knowledge/marketing/copywriting-frameworks.md` (AIDA / PAS / BAB / 4U / FAB / StoryBrand / P3)
- `knowledge/marketing/hook-patterns.md` (7-mechanism hook taxonomy)
- `knowledge/marketing/social-platform-specs.md` (canonical platform specs)
- `knowledge/marketing/search-intent.md` (4 intent types + page structure)
- `knowledge/marketing/persona-template.md` (3-layer persona)
- `knowledge/marketing/brand-voice-rubric.md` (8-dimension voice profile)
- `knowledge/marketing/crisis-comms-playbook.md` (strategic crisis comms)
- `knowledge/marketing/utm-conventions.md` (UTM convention)
- `knowledge/marketing/content-calendar-patterns.md` (cadence + 60/30/10 mix + pillars)
- `knowledge/marketing/kpi-cheatsheet.md` (metric definitions + per-goal anchors)

**Cross-cutting (relevant to BrandFlow):**
- `knowledge/scope/declined-tools.md` — boundaries on what is NOT built (Items 3 and 4 are BrandFlow-specific in Update 11).
- `knowledge/security/opsec-multi-account.md` — when client account hygiene is in question.
- `knowledge/agent-design/memory-rules.md`, `tool-use-rules.md`, `task-logger-rules.md`.

---

## How To Use

Agents call skills by reference, not duplication. When a task arrives:

1. Identify which skill(s) apply (parent skill + agent-specific deep skill if you own one).
2. Read the skill file for process + output format.
3. Apply the skill's rules to the task.
4. Use the skill's output template.
5. Load relevant `knowledge/marketing/*` cheatsheets per the skill's References section.

If a skill conflicts with the agent's Tier 3 SOUL, the SOUL wins (it's more specific). If a skill conflicts with the company's Tier 2 SOUL, the SOUL wins. Root SOUL always wins above all.

---

## Boundary #4 Across Skills

Every BrandFlow skill that touches public-facing content (content, design, community, seo, automation, qa) is gated by Boundary #4 from Root SOUL: **draft, never publish on Fathur's behalf without explicit approval.**

In Update 11 this is **hard-coded into `tools/content_scheduler.py`**: the SCHEDULED → PUBLISHED transition refuses to release any piece unless `boundary_4_status == "fathur_approved"` (per-piece signature required).

Community skill is the front line for this — incoming public messages get drafted replies, never auto-sent. Crisis playbook escalates approval to Fathur for any T3+ public statement.

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
   company: BrandFlow
   used_by: ["@brandflow.role1", "@brandflow.role2"]
   # for deep skills also include:
   # agent_specific: "@brandflow.<role>"
   # parent_skill: <parent-skill-name>
   ---
   ```
5. Update this index.
6. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/brandflow/SOUL.md` (Tier 2 — company personality, agency context, knowledge loading order).
- `companies/brandflow/AGENTS.md` (role roster).
- `knowledge/marketing/marketing-sop.md` (foundational SOP).
- `knowledge/scope/declined-tools.md` (scope boundaries).
- `knowledge/tools/tool-registry.md` (full tool registry, 27 entries post Update 11).
