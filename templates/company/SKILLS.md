# {{COMPANY_NAME}} Skill Index

Last updated: (set on company create)

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → {{COMPANY_NAME}} SOUL.

---

## Default Skills (Generic — Customize After Create-Company)

The generator copies a default set of skill folders. **NOT all are relevant for every company.** After `create-company.sh`:

1. **Review** the `skills/` folder.
2. **Delete** skill folders that don't fit your company's domain.
3. **Specialize** the SKILL.md files that remain (rewrite for your company's voice and process).
4. **Add** new skill folders for capabilities specific to your company.
5. **Update this index** to list active skills and removed skills.

### Default Skill Set (May Not All Be Relevant)

| Skill | When Relevant |
|---|---|
| coding | Software / SaaS / engineering companies |
| content | Marketing / content / writing companies |
| design | Marketing / brand / visual companies (NEW NAME — not in default template; add for marketing) |
| devops | Software / infra / cloud companies |
| qa | All companies (quality gate) |
| research | Marketing, crypto, knowledge companies |
| business | Companies needing internal SOP work |
| automation | All companies (workflow + pipeline) |
| uiux | Software companies (product UI) |
| seo | Marketing companies (search optimization) — add manually |
| security | Software / SaaS companies — add manually |
| ml-agent | AI / agent companies — add manually |
| community | Marketing / brand companies — add manually |

---

## Skill File Format

Every SKILL.md uses front-matter:

```yaml
---
name: skill-name
description: One-line description.
company: {{COMPANY_NAME}}
used_by: ["@{{COMPANY_SLUG}}.role1", "@{{COMPANY_SLUG}}.role2"]
---
```

Then content includes:
- When to use
- Process (numbered steps)
- Rules (numbered)
- Output Format (concrete templates)
- Cross-Skill / Cross-Agent Routing
- What This Skill Does NOT Cover
- Reference

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
3. Use the standard front-matter (see above).
4. Update this index.
5. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference Examples

For specialized skill examples, see:
- `companies/nexusai/skills/` — NexusAI's specialized set (coding, devops, security, ml-agent, automation, qa, uiux).
- `companies/brandflow/skills/` — BrandFlow's specialized set (content, design, community, seo, research, automation, qa).
- `companies/crypto-consultant/skills/` — Crypto Consultant's specialized set (research, market-analysis, onchain, macro, risk, reporting, qa).

---

## Reference

- `companies/{{COMPANY_SLUG}}/SOUL.md` (Tier 2 — company personality)
- `companies/{{COMPANY_SLUG}}/AGENTS.md` (role roster)
- Domain SOP at `knowledge/<domain>/<file>.md`
