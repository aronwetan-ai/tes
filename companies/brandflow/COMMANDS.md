# COMMANDS.md
Commands for BrandFlow.

## Knowledge Loading Rules

Setiap kali agent @brandflow.* dipanggil, wajib baca file berikut secara urutan:
1. /home/fatur/ai-holding/SOUL.md
2. /home/fatur/ai-holding/knowledge/core/principles.md
3. /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
6. /home/fatur/ai-holding/companies/brandflow/SOUL.md
7. /home/fatur/ai-holding/companies/brandflow/MEMORY.md
8. /home/fatur/ai-holding/knowledge/marketing/marketing-sop.md
9. (jika ada) /home/fatur/ai-holding/companies/brandflow/agents/<agent>.md

## Marketing Commands

Format: @brandflow <keyword>

@brandflow caption      — Buat caption media sosial
@brandflow artikel      — Buat artikel atau blog post
@brandflow campaign     — Rancang strategi campaign
@brandflow calendar     — Buat content calendar
@brandflow design       — Buat visual concept / layout / type spec     (NEW)
@brandflow reply        — Draft reply DM / comment / mention           (NEW)
@brandflow community    — Sentiment / community report                 (NEW)
@brandflow seo          — Analisis atau optimasi SEO
@brandflow kpi          — Buat KPI dan metrics campaign
@brandflow branding     — Kerjakan identitas atau arah brand
@brandflow status       — Tampilkan task aktif perusahaan
@brandflow recap        — Rangkum progress perusahaan

## Task Commands

Format: @brandflow <keyword>

@brandflow new-task      — Buat task baru
@brandflow save-decision — Simpan keputusan penting ke memory
@brandflow new-project   — Buat folder project baru
@brandflow improve-skill — Tingkatkan skill perusahaan

## Direct Agent Routing

Format: @brandflow.<agent> <task>

```
@brandflow.ceo          — Direction, brand identity, strategic positioning
@brandflow.cmo          — Marketing strategy, campaigns, briefs
@brandflow.pm           — Calendar, timeline, asset requests
@brandflow.copywriter   — Captions, headlines, hooks, CTAs
@brandflow.social       — Calendar, cadence, format strategy
@brandflow.community    — Real-time engagement, DM/comment drafts          (NEW)
@brandflow.designer     — Visual concept, layout, type, color spec         (NEW)
@brandflow.seo          — Keyword research, content optimization
@brandflow.analytics    — KPI tracking, metrics, dashboards
@brandflow.qa           — Content review, brand consistency
@brandflow.writer       — Long-form, brand book, SOP
```

## Routing

Tasks should be routed based on:
- Brand strategy → CEO
- Campaign strategy → CMO
- Planning → Project Manager
- Copy production → Copywriter
- Calendar / channel format → Social
- DMs / comments / live engagement → Community (NEW)
- Visual / layout / design spec → Designer (NEW)
- SEO → SEO Specialist
- Data / KPI → Analytics Specialist
- Review → QA Agent
- Long-form / brand book → Writer

## Boundary #4 Reminder

BrandFlow's whole job involves public output. We DRAFT; we never PUBLISH on Fathur's behalf without explicit approval. Community manager especially never auto-sends public replies.
