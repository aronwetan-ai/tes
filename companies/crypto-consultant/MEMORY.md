# Crypto Consultant Memory

Inherits: Root SOUL → Crypto Consultant SOUL (Tier 2)
Versi: 2.0
Update terakhir: 2026-05-17 (post Update 6)

This file is **company-scoped**. Holding-wide memory lives at `MEMORY.md` (strategic) and `memory/global.md` (operational tagged log).

---

## Company Identity

```
Name   : Crypto Consultant
Type   : Crypto Research Company
Focus  : market research, cycle analysis, risk management, reporting
SOUL   : companies/crypto-consultant/SOUL.md (Tier 2 — analyst-cautious, data-first, skeptical)
Roster : 11 agents (CEO, Research Lead, PM, Market, Risk, On-chain, Macro, Data, QA, Report, Writer)
Tier 3 : 6 agent SOULs in agents/ (ceo, research, market, risk, onchain, macro)
Skills : 7 specialized (research, market-analysis, onchain, macro, risk, reporting, qa) — see SKILLS.md
```

---

## Active Decisions

[DECISION] 2026-05-17 — Crypto Consultant menambahkan role `@crypto.onchain` dan `@crypto.macro` (Update 5). On-chain handle wallet flows + smart money tracking; Macro handle DXY / Fed / M2 / equity correlation.
[DECISION] 2026-05-17 — 6-layer output format wajib untuk semua riset: FACT → SOURCE → TREND → INTERPRET → SCENARIO → RISK NOTE. Bear case stated FIRST in SCENARIO.
[DECISION] 2026-05-17 — Disclaimer mandatory di setiap output yang melalui `@crypto.report`. Boundary #4 enforcement.
[DECISION] 2026-05-17 — No buy/sell calls — ever. Crypto Consultant gives scenarios + risk-sized positioning examples; Fathur decides execution.
[DECISION] 2026-05-17 — Wallet attribution policy: confidence stated explicitly (High/Medium/Low). Public attribution of wallets ke real entities butuh approval Fathur per-piece.
[DECISION] 2026-05-17 — Skill `coding`, `devops`, `content`, `automation`, `uiux`, `business` dihapus karena Crypto Consultant tidak ship code/copy/UI. Engineering → NexusAI; marketing → BrandFlow.

---

## Active Projects

None yet.

---

## Active Tasks

None yet.

---

## Architecture Notes

[ARCH] 2026-05-17 — `companies/crypto-consultant/agents/` dibuat untuk Tier 3 SOULs.
[ARCH] 2026-05-17 — Skill folder dirombak total: 6 skill dihapus, 5 skill baru (`market-analysis`, `onchain`, `macro`, `risk`, `reporting`). Total 7 specialized skills.
[ARCH] 2026-05-17 — `SKILLS.md` index dibuat di company root.
[ARCH] 2026-05-17 — `crypto-research-framework.md` di `knowledge/crypto/` jadi single source of truth untuk methodology + 6-layer format.

---

## Cycle / Market State Log

Belum ada cycle phase call yang aktif.

Format saat ada:
```
[CYCLE] YYYY-MM-DD — Phase: <accumulation/markup/distribution/markdown>
Confidence: <high/medium/low>
Basis: <signals supporting>
Invalidation: <what would change this read>
Reviewed by: @crypto.research / @crypto.market / @crypto.macro
```

---

## Tool Notes (Crypto-Specific)

[TOOL] fear_greed.py — Active. Always run for sentiment baseline before research output.
[TOOL] btc_price.py — PLANNED. Will integrate with `@crypto.market` workflow.
[TOOL] news_sentiment.py — PLANNED. Will integrate with `@crypto.research` for narrative reads.
[TOOL] No paid sources approved yet (Glassnode, Nansen, Bloomberg). Escalate to `@crypto.ceo` if research needs them.

---

## Cross-Company Collaboration Log

Belum ada catatan kolaborasi cross-company yang durable. Akan ditulis di sini saat Crypto Consultant bekerja sama dengan NexusAI (mis. on-chain dashboard) atau BrandFlow (mis. translate research jadi market commentary content).

---

## Boundary #4 — Maximum Strength

Crypto research has financial consequences. Public-facing output is **always** gated.

- Internal use → ship after `@crypto.qa` review.
- External publish → wait for Fathur per-piece approval.
- Default assumption: every report is **internal** unless Fathur explicitly says otherwise.

Detail: Tier 2 SOUL + `agents/ceo.md` + `skills/reporting/SKILL.md`.

---

## Memory Rules (Company-Scoped)

Tulis ke file ini saat:
- **[DECISION]** keputusan research methodology / focus.
- **[ARCH]** perubahan internal Crypto Consultant (role, skill, framework).
- **[CYCLE]** cycle phase identification update.
- **[TOOL]** tool crypto baru / status berubah.
- **[TASK]** task riset yang sedang berjalan.
- **[DONE]** task riset yang selesai.
- **[INSIGHT]** insight cycle / market / on-chain / macro yang reusable.
- **[RISK]** risk threshold breach (mis. F&G > 90 atau < 10).

Jangan tulis di sini:
- Daily F&G readings → `tasks/` JSONL atau report file.
- Single-line market commentary tanpa decision.
- Routine "BTC at $X today" updates.
- Speculation tanpa decision impact.
- Keputusan holding-wide → `MEMORY.md` atau `memory/global.md`.

Detail rules: `knowledge/agent-design/memory-rules.md`.
