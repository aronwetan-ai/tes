# Crypto Consultant Skill Index

Last updated: 2026-05-17

Skills are reusable behavior modules. Each Tier 3 agent uses one or more skills depending on the task. Skills inherit Root SOUL → Crypto Consultant SOUL.

---

## Active Skills (7)

| Skill | Path | Primary Users |
|---|---|---|
| research | `skills/research/SKILL.md` | @crypto.research, @crypto.ceo, @crypto.report |
| market-analysis | `skills/market-analysis/SKILL.md` | @crypto.market, @crypto.research |
| onchain | `skills/onchain/SKILL.md` | @crypto.onchain, @crypto.research |
| macro | `skills/macro/SKILL.md` | @crypto.macro, @crypto.research |
| risk | `skills/risk/SKILL.md` | @crypto.risk, @crypto.research |
| reporting | `skills/reporting/SKILL.md` | @crypto.report, @crypto.writer, @crypto.ceo |
| qa | `skills/qa/SKILL.md` | @crypto.qa, @crypto.report, @crypto.ceo |

---

## Removed Skills (Not Relevant for This Company)

These were boilerplate from the original template; removed because Crypto Consultant doesn't ship code, design, or content — it produces research:

- `coding` — engineering → NexusAI.
- `devops` — infrastructure → NexusAI.
- `content` — marketing copy → BrandFlow.
- `automation` — pipelines → NexusAI handles infra; tools used by Crypto Consultant come from `tools/`.
- `uiux` — product UI → NexusAI.
- `business` — business / SOP → CEO + identity files.

---

## Boundary #4 — Maximum Strength for Crypto

Crypto research has **financial consequences**. Every skill here treats output that could leave the holding as gated:

- **research, market-analysis, onchain, macro, risk** — produce internal analysis with 6-layer format.
- **reporting** — final assembly + mandatory disclaimer.
- **qa** — checks disclaimer presence + risk-language compliance before ship.

Public-facing output requires explicit Fathur per-piece approval (via `@crypto.ceo`). Internal use ships after `@crypto.qa` review.

---

## 6-Layer Format (Cross-Skill Standard)

All analytical skills produce output in 6 layers:

```
[FACT]       — measurable data with timestamp
[SOURCE]     — where data came from + when
[TREND]      — pattern in the data
[INTERPRET]  — what the pattern typically means
[SCENARIO]   — bull / sideways / bear (BEAR FIRST) with relative likelihood
[RISK NOTE]  — what could invalidate the read
```

Mandated by `knowledge/crypto/crypto-research-framework.md`.

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
   company: Crypto Consultant
   used_by: ["@crypto.role1", "@crypto.role2"]
   ---
   ```
4. Update this index.
5. Update relevant Tier 3 SOULs to reference the skill.

---

## Reference

- `companies/crypto-consultant/SOUL.md` (Tier 2 — company personality)
- `companies/crypto-consultant/AGENTS.md` (role roster)
- `knowledge/crypto/crypto-research-framework.md` (domain SOP)
- `knowledge/tools/tool-registry.md` (active + planned tools)
