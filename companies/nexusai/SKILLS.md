# NexusAI Skill Index

Last updated: 2026-05-17

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → NexusAI SOUL.

---

## Active Skills (7)

| Skill | Path | Primary Users |
|---|---|---|
| coding | `skills/coding/SKILL.md` | @nexusai.backend, @nexusai.frontend, @nexusai.cto |
| devops | `skills/devops/SKILL.md` | @nexusai.devops, @nexusai.cto, @nexusai.security |
| security | `skills/security/SKILL.md` | @nexusai.security, @nexusai.cto |
| ml-agent | `skills/ml-agent/SKILL.md` | @nexusai.ml, @nexusai.cto |
| automation | `skills/automation/SKILL.md` | @nexusai.devops, @nexusai.backend, @nexusai.ml |
| qa | `skills/qa/SKILL.md` | @nexusai.qa, @nexusai.cto, @nexusai.backend, @nexusai.frontend |
| uiux | `skills/uiux/SKILL.md` | @nexusai.frontend, @nexusai.cto |

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because they don't fit NexusAI's IT / SaaS / cloud / AI agents focus:

- `content` — marketing copy → use BrandFlow (`@brandflow.copywriter`).
- `research` — market research → use BrandFlow (`@brandflow.cmo`) or Crypto Consultant for crypto-specific.
- `business` — business / SOP design → that's the CEO's role + companies/<co>/identity.

---

## How To Use

Agents call skills by reference, not duplication. When a task arrives:

1. Identify which skill(s) apply.
2. Read the skill file for process + output format.
3. Apply the skill's rules to the task.
4. Use the skill's output template.

If a skill conflicts with the agent's Tier 3 SOUL, the SOUL wins (it's more specific). If a skill conflicts with the company's Tier 2 SOUL, the SOUL wins. Root SOUL always wins above all.

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
   company: NexusAI
   used_by: ["@nexusai.role1", "@nexusai.role2"]
   ---
   ```
4. Update this index.
5. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/nexusai/SOUL.md` (Tier 2 — company personality)
- `companies/nexusai/AGENTS.md` (role roster)
- `knowledge/software/software-development-sop.md` (domain SOP)
