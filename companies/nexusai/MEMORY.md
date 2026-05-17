# NexusAI Memory

Inherits: Root SOUL → NexusAI SOUL (Tier 2)
Versi: 2.0
Update terakhir: 2026-05-17 (post Update 6)

This file is **company-scoped**. Holding-wide memory lives at `MEMORY.md` (strategic) and `memory/global.md` (operational tagged log).

---

## Company Identity

```
Name   : NexusAI
Type   : IT Software Company
Focus  : cloud, DevOps, AI agents, SaaS
SOUL   : companies/nexusai/SOUL.md (Tier 2 — engineering-precise, pragmatic, zero fluff)
Roster : 10 agents (CEO, CTO, PM, Backend, Frontend, DevOps, Security, ML, QA, Writer)
Tier 3 : 6 agent SOULs in agents/ (ceo, cto, backend, devops, security, ml)
Skills : 7 specialized (coding, devops, security, ml-agent, automation, qa, uiux) — see SKILLS.md
```

---

## Active Decisions

[DECISION] 2026-05-17 — NexusAI menambahkan role `@nexusai.security` dan `@nexusai.ml` (Update 5). Security handle defensive + OPSEC offensive enablement. ML handle agent design + prompt engineering + evals.
[DECISION] 2026-05-17 — Skill `business`, `content`, `research` dihapus dari NexusAI karena tidak fit fokus engineering. Marketing-related → BrandFlow. Crypto research → Crypto Consultant.
[DECISION] 2026-05-17 — Default tech stack philosophy ditetapkan: boring tech > newest framework. Working code beats perfect code. Documented di Tier 2 SOUL.

---

## Active Projects

None yet.

---

## Active Tasks

None yet.

---

## Architecture Notes

[ARCH] 2026-05-17 — `companies/nexusai/agents/` dibuat untuk Tier 3 SOULs.
[ARCH] 2026-05-17 — Skill folder dirombak: `business`, `content`, `research` dihapus; `security`, `ml-agent` ditambah. Total 7 specialized skills.
[ARCH] 2026-05-17 — `SKILLS.md` index dibuat di company root.

---

## Tools (NexusAI-relevant)

[TOOL] create-company.sh — Active (used by Main Assistant, but built / maintained by NexusAI patterns).
[TOOL] fear_greed.py — Active (built per NexusAI standards, used by Crypto Consultant).

Future tools yang akan dibangun NexusAI:
- btc_price.py (PLANNED)
- news_sentiment.py (PLANNED)
- Task logger writer (PLANNED — schema sudah di `skills/automation/SKILL.md`).

---

## Cross-Company Collaboration Protocol

[ARCH] 2026-05-17 — Cross-company integration infrastructure deployed. SOPs:
- `knowledge/sop/cross-company-handoff.md` — handoff block format + type-specific templates
- `knowledge/sop/cross-company-qa-routing.md` — auto QA triggers when other companies feed us
- `knowledge/sop/approval-workflow.md` — Fathur approval gate (Tier 3 decisions only)
- `knowledge/sop/autonomous-boundaries.md` — what runs without Fathur (most things)
- `knowledge/sop/weekly-cadence.md` — autonomous weekly rhythm (Mon-Fri)

**NexusAI's role in cross-company:**
- **Receives:** Data spec handoffs from Crypto Consultant (Type 2: Research → Data Spec)
- **Receives:** Design direction from BrandFlow (Type 3: Design Direction)
- **Produces:** Tools, APIs, dashboards. Sends [HANDOFF → ALL] for tool status changes (Type 4).
- **QA duty:** @nexusai.qa reviews technical implementation. Also validates data accuracy post-integration.
- **Builds tools FOR other companies:** All Python tools (fear_greed, price_scraper, etc.) built by NexusAI, used by Crypto Consultant.
- **Weekly cadence:** Dashboard data refresh daily (automated). Schema changes on-demand. Tool status notifications immediate.

**Active handoff relationships:**
- Crypto → NexusAI: Dashboard data spec (7 API endpoints: fear-greed, btc-price, funding, lth-supply, etf-flow, cycle-phase, scenarios)
- BrandFlow → NexusAI: Visual design direction (dark theme, Inter font, green/red/yellow accents)
- NexusAI → Crypto + BrandFlow: Tool status notifications (when tools change/break/upgrade)

**Pending/Blocked:**
- ETF flow tool (TOOL-033) — needed for dashboard, not yet built
- Backend OpenAPI spec — needed for frontend implementation
- Auth/access decision — waiting Fathur (public vs private dashboard)

### Collaboration Log

_Entries written here when cross-company work happens:_

---

## Memory Rules (Company-Scoped)

Tulis ke file ini saat:
- **[DECISION]** keputusan yang affect NexusAI specifically.
- **[ARCH]** perubahan internal NexusAI (role, skill, struktur).
- **[TOOL]** tool yang built oleh / dipakai khusus NexusAI.
- **[TASK]** task NexusAI yang sedang berjalan.
- **[DONE]** task NexusAI yang selesai.
- **[INSIGHT]** insight teknis yang reusable di NexusAI.

Jangan tulis di sini:
- Keputusan holding-wide → `MEMORY.md` atau `memory/global.md`.
- Keputusan BrandFlow / Crypto → company mereka masing-masing.
- Basa-basi, klarifikasi ringan.

Detail rules: `knowledge/agent-design/memory-rules.md`.
