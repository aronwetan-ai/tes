# COMMANDS.md
Commands for NexusAI.

## Knowledge Loading Rules

Setiap kali agent @nexusai.* dipanggil, wajib baca file berikut secara urutan:
1. /home/fatur/ai-holding/SOUL.md
2. /home/fatur/ai-holding/knowledge/core/principles.md
3. /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
6. /home/fatur/ai-holding/companies/nexusai/SOUL.md
7. /home/fatur/ai-holding/companies/nexusai/MEMORY.md
8. /home/fatur/ai-holding/knowledge/software/software-development-sop.md
9. (jika ada) /home/fatur/ai-holding/companies/nexusai/agents/<agent>.md

## Development Commands

Format: @nexusai <keyword>

@nexusai idea         — Generate ide produk atau fitur baru
@nexusai api          — Desain API endpoint
@nexusai architecture — Buat arsitektur teknis sistem
@nexusai deploy       — Buat deployment plan
@nexusai review       — Review code atau desain
@nexusai security     — Threat modeling / security review                  (NEW)
@nexusai opsec        — Operational security plan untuk automation work    (NEW)
@nexusai agent        — Design AI agent / prompt engineering               (NEW)
@nexusai eval         — Build evals untuk AI agent                         (NEW)
@nexusai docs         — Buat dokumentasi teknis
@nexusai status       — Tampilkan task aktif perusahaan
@nexusai recap        — Rangkum progress perusahaan

## Task Commands

Format: @nexusai <keyword>

@nexusai new-task      — Buat task baru
@nexusai save-decision — Simpan keputusan penting ke memory
@nexusai new-project   — Buat folder project baru
@nexusai improve-skill — Tingkatkan skill perusahaan

## Direct Agent Routing

Format: @nexusai.<agent> <task>

```
@nexusai.ceo        — Direction, priority, business decision
@nexusai.cto        — Architecture, technical strategy
@nexusai.pm         — Task breakdown, timeline, backlog
@nexusai.backend    — API design, database, server logic
@nexusai.frontend   — UI flow, component design
@nexusai.devops     — Deployment, infrastructure, CI/CD
@nexusai.security   — Security review, threat modeling, OPSEC          (NEW)
@nexusai.ml         — AI agent design, prompts, tool integration       (NEW)
@nexusai.qa         — Testing, validation, acceptance criteria
@nexusai.writer     — Documentation, README, SOP
```

## Routing

Tasks should be routed based on:
- Strategy → CEO / CTO
- Planning → Project Manager
- Backend / API / DB → Backend Engineer
- Frontend / UI → Frontend Engineer
- Infrastructure / Deploy → DevOps Engineer
- Security / Auth / OPSEC → Security Engineer (NEW)
- AI / Agent / Prompt → ML Engineer (NEW)
- Testing → QA Engineer
- Documentation → Technical Writer
