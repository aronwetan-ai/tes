# BrandFlow Skill Index

Last updated: 2026-05-17

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → BrandFlow SOUL.

---

## Active Skills (7)

| Skill | Path | Primary Users |
|---|---|---|
| content | `skills/content/SKILL.md` | @brandflow.copywriter, @brandflow.cmo, @brandflow.writer |
| design | `skills/design/SKILL.md` | @brandflow.designer, @brandflow.cmo |
| community | `skills/community/SKILL.md` | @brandflow.community, @brandflow.cmo |
| seo | `skills/seo/SKILL.md` | @brandflow.seo, @brandflow.copywriter, @brandflow.writer |
| research | `skills/research/SKILL.md` | @brandflow.cmo, @brandflow.copywriter, @brandflow.analytics |
| automation | `skills/automation/SKILL.md` | @brandflow.pm, @brandflow.social, @brandflow.analytics |
| qa | `skills/qa/SKILL.md` | @brandflow.qa, @brandflow.cmo, @brandflow.community |

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because they don't fit BrandFlow's marketing / content / branding focus:

- `coding` — engineering work → use NexusAI (`@nexusai.backend`).
- `devops` — infrastructure → use NexusAI (`@nexusai.devops`).
- `business` — business / SOP design → CEO + identity files.
- `uiux` — product UI → use NexusAI (`@nexusai.frontend` + `skills/uiux`). BrandFlow's `design` skill covers marketing visuals, NOT product UI.

---

## How To Use

Agents call skills by reference, not duplication. When a task arrives:

1. Identify which skill(s) apply.
2. Read the skill file for process + output format.
3. Apply the skill's rules to the task.
4. Use the skill's output template.

If a skill conflicts with the agent's Tier 3 SOUL, the SOUL wins (it's more specific). If a skill conflicts with the company's Tier 2 SOUL, the SOUL wins. Root SOUL always wins above all.

---

## Boundary #4 Across Skills

Every BrandFlow skill that touches public-facing content (content, design, community, seo) is gated by Boundary #4 from Root SOUL: **draft, never publish on Fathur's behalf without explicit approval.**

Community skill is the front line for this — incoming public messages get drafted replies, never auto-sent.

---

## Adding New Skills

When a behavior pattern emerges that's used by 2+ agents and isn't covered:

1. Decide if it should be **company-specific** (here) or **cross-company** (`knowledge/sop/`).
2. Create `skills/<skill-name>/SKILL.md`.
3. Use the standard front-matter:
   ```yaml
   ---
   name: skill-name
   description: One-line description.
   company: BrandFlow
   used_by: ["@brandflow.role1", "@brandflow.role2"]
   ---
   ```
4. Update this index.
5. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/brandflow/SOUL.md` (Tier 2 — company personality)
- `companies/brandflow/AGENTS.md` (role roster)
- `knowledge/marketing/marketing-sop.md` (domain SOP)
