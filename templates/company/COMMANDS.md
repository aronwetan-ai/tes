# COMMANDS.md

Commands for {{COMPANY_NAME}}.

---

## Knowledge Loading Rules

Setiap kali agent @{{COMPANY_SLUG}}.* dipanggil, wajib baca file berikut secara urutan:

1. /home/fatur/ai-holding/SOUL.md
2. /home/fatur/ai-holding/knowledge/core/principles.md
3. /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
6. /home/fatur/ai-holding/companies/{{COMPANY_SLUG}}/SOUL.md
7. /home/fatur/ai-holding/companies/{{COMPANY_SLUG}}/MEMORY.md
8. Knowledge domain perusahaan (edit setelah create-company)

---

## Company Routing

Format company-level (PM yang internal routing):
```
@{{COMPANY_SLUG}} <task>
```

---

## Direct Agent Routing

Format:
```
@{{COMPANY_SLUG}}.<agent> <task>
```

Default agents (rename / hapus yang tidak relevan):
```
@{{COMPANY_SLUG}}.ceo         buatkan arah strategis
@{{COMPANY_SLUG}}.strategy    buatkan plan jangka panjang
@{{COMPANY_SLUG}}.pm          buatkan breakdown task
@{{COMPANY_SLUG}}.specialist  eksekusi task domain spesifik
@{{COMPANY_SLUG}}.qa          review output / acceptance check
@{{COMPANY_SLUG}}.writer      buatkan dokumentasi
```

---

## Domain Commands

Format: `@{{COMPANY_SLUG}} <keyword>`

Edit daftar berikut setelah create-company agar match dengan fokus perusahaan.

```
@{{COMPANY_SLUG}} idea       — Generate ide baru di domain perusahaan
@{{COMPANY_SLUG}} plan       — Buat rencana / strategi
@{{COMPANY_SLUG}} review     — Review output internal
@{{COMPANY_SLUG}} report     — Susun laporan akhir
@{{COMPANY_SLUG}} status     — Tampilkan task aktif perusahaan
@{{COMPANY_SLUG}} recap      — Rangkum progress perusahaan
```

---

## Task Commands

Format: `@{{COMPANY_SLUG}} <keyword>`

```
@{{COMPANY_SLUG}} new-task      — Buat task baru
@{{COMPANY_SLUG}} save-decision — Simpan keputusan penting ke MEMORY.md perusahaan
@{{COMPANY_SLUG}} new-project   — Buat folder project baru
@{{COMPANY_SLUG}} improve-skill — Tingkatkan skill perusahaan
```

---

## Routing Internal

Strategic        → CEO / Strategy Lead
Planning         → Project Manager
Domain execution → Specialist Agent yang relevan
Validation       → QA Agent
Documentation    → Technical Writer

Detail role: /home/fatur/ai-holding/companies/{{COMPANY_SLUG}}/AGENTS.md
