# COMMANDS.md
Commands for Crypto Consultant.

## Knowledge Loading Rules

Setiap kali agent @crypto.* dipanggil, wajib baca file berikut secara urutan:
1. /home/fatur/ai-holding/SOUL.md
2. /home/fatur/ai-holding/knowledge/core/principles.md
3. /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
6. /home/fatur/ai-holding/companies/crypto-consultant/SOUL.md
7. /home/fatur/ai-holding/companies/crypto-consultant/MEMORY.md
8. /home/fatur/ai-holding/knowledge/crypto/crypto-research-framework.md
9. (jika ada) /home/fatur/ai-holding/companies/crypto-consultant/agents/<agent>.md

## Research Commands

Format: @crypto <keyword>

@crypto research   — Riset lengkap: sentiment + market + risk + report
@crypto sentiment  — Cek Fear & Greed Index via fear_greed.py
@crypto market     — Analisis teknikal, market structure, cycle phase
@crypto risk       — Risk assessment + position sizing
@crypto onchain    — Wallet flows, exchange flows, smart money tracking    (NEW)
@crypto macro      — DXY, Fed, M2, equity correlation, macro events       (NEW)
@crypto report     — Susun dan simpan laporan final ke tasks/
@crypto status     — Tampilkan task aktif perusahaan
@crypto recap      — Rangkum progress perusahaan

## Task Commands

Format: @crypto <keyword>

@crypto new-task      — Buat task baru
@crypto save-decision — Simpan keputusan penting ke memory
@crypto new-project   — Buat folder project baru
@crypto improve-skill — Tingkatkan skill perusahaan

## Direct Agent Routing

Format: @crypto.<agent> <task>

```
@crypto.ceo         — Research focus, quality gate, public-facing approval
@crypto.research    — Synthesis, 6-layer research output
@crypto.pm          — Task breakdown, deadline, planning
@crypto.market      — Technicals, market structure, cycle phase
@crypto.risk        — Drawdown, position sizing, tail scenarios
@crypto.onchain     — Wallet flows, exchange flows, smart money            (NEW)
@crypto.macro       — DXY, Fed, M2, equity correlation                     (NEW)
@crypto.data        — Generic data structure, dashboards, metrics
@crypto.qa          — Methodology review, fact-check
@crypto.report      — Final report assembly, disclaimer
@crypto.writer      — Long-form documentation
```

## Routing

Tasks should be routed based on:
- Research direction / focus → CEO
- Coherent multi-signal read → Research Lead
- Planning / breakdown → PM
- Charts, levels, cycle phase → Market
- Risk sizing, scenarios → Risk
- Wallet flows, on-chain forensics → On-chain (NEW)
- DXY, Fed, macro context → Macro (NEW)
- Generic data / dashboards → Data
- Validation / fact-check → QA
- Final formatted report → Report
- Long-form / documentation → Writer

## Boundary #4 Reminder

Crypto research has financial consequences. We never publish without Fathur's explicit approval. Disclaimer mandatory on @crypto.report output. We give analysis, not financial advice.
