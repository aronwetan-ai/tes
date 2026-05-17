# System Audit Protocol — Periodic Health Check

Versi: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Schedule: Weekly (Friday, after weekly recap) + ad-hoc when triggered
Source: Adapted from SUPERAGENT v2 x1.md

---

## Purpose

Periodic 4-layer audit untuk health check seluruh AI Holding system.
Catches drift, redundancy, dan gaps yang reflection loop / per-company QA miss.

Tier 2 dari `autonomous-boundaries.md` — autonomous tapi log decision + propose fix.

---

## When To Run

- **Scheduled:** Setiap Jumat sebagai bagian dari weekly recap (`weekly-cadence.md` Step 4)
- **Triggered:** Setelah major update (PR merge yang affect SOP / structure)
- **Ad-hoc:** Operator request "run system audit"

---

## The 4 Layers

### Layer 1 — Output Quality

```
Pertanyaan:
- Were last week's outputs immediately executable?
- Did any cause unnecessary follow-up rounds?
- Did reflection loop catch all issues?
- Did QA agents catch issues reflection loop missed?

Data source:
- tasks/logs.jsonl (last 7 days, all companies)
- memory/global.md (last week's [APPROVAL] / [QA_HEALTH] entries)
- tests/integration/cross-company-smoke-test.md (Friday run results)
```

### Layer 2 — Module / Skill Coverage

```
Pertanyaan:
- Did correct skills/agents activate per task?
- Any gaps (task needed skill yang belum ada)?
- Any redundancy between skills (BrandFlow design vs NexusAI uiux, dll)?
- Any deprecated skill yang masih ke-load?

Data source:
- companies/*/SKILLS.md
- knowledge/sop/* (cross-cutting SOPs)
- Recent task routing decisions
```

### Layer 3 — Routing Precision

```
Pertanyaan:
- Any false positives in pseudo-mention routing (@x.y dispatched ke wrong agent)?
- Any handoff blocks malformed?
- Any cross-company QA missed (skipped routing)?
- Approval workflow respected (no Tier 3 bypassed)?

Data source:
- tasks/inbox.jsonl (handoff entries)
- tasks/messages.jsonl (cross-agent routing)
- memory/global.md (approval log)
```

### Layer 4 — Token / Context Efficiency

```
Pertanyaan:
- Any always-on content yang bisa dijadikan conditional?
- Which skills load more than needed?
- What can be compressed without losing function?
- Any MEMORY bloat (entries yang seharusnya pindah ke archive)?

Data source:
- File size of always-loaded files (SOUL.md, MAIN.md, MEMORY.md, COMMANDS.md)
- Skill file sizes
- memory/global.md growth rate
```

---

## Output Format

```
[AUDIT — YYYY-MM-DD]

[FINDINGS]
Layer 1 (Output Quality):
  - <issue> → <fix>
  - <issue> → <fix>

Layer 2 (Skill Coverage):
  - <issue> → <fix>

Layer 3 (Routing Precision):
  - <issue> → <fix>

Layer 4 (Token Efficiency):
  - <issue> → <fix>

[PRIORITY]
1. <highest impact item>
2. <second>
3. <third>

[PROPOSED EDITS]
File: <path>
Change: <specific edit>
Rationale: <why>

[STATUS]
[ ] Applied immediately (Tier 1 — config-only, no impact on running ops)
[ ] Awaiting Operator review (Tier 2 — affects multiple agents)
[ ] Awaiting Fathur approval (Tier 3 — affects Boundary #4 / strategic)
```

---

## Critical Rule

**Never auto-apply system changes.** Audit produces findings + proposed edits.
Operator (or Fathur untuk Tier 3) decides apply or revise.

After audit always close with:
> "Apply now or review first?"

---

## Reference

- Source: `update/v2/openclaw/skills/x1.md`
- Schedule: `knowledge/sop/weekly-cadence.md` (Friday slot)
- Complementary: `tests/integration/cross-company-smoke-test.md`
- Boundaries: `knowledge/sop/autonomous-boundaries.md`
