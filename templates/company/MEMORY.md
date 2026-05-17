# {{COMPANY_NAME}} Memory

Inherits: Root SOUL → {{COMPANY_NAME}} SOUL (Tier 2)
Versi: 2.0
Update terakhir: (set on company create)

This file is **company-scoped**. Holding-wide memory lives at `MEMORY.md` (strategic) and `memory/global.md` (operational tagged log).

---

## Company Identity

```
Name   : {{COMPANY_NAME}}
Type   : {{COMPANY_TYPE}}
Focus  : {{COMPANY_FOCUS}}
SOUL   : companies/{{COMPANY_SLUG}}/SOUL.md (Tier 2 — customize after create-company)
Roster : (list active roles after customizing AGENTS.md)
Tier 3 : (list Tier 3 SOULs in agents/ as you create them)
Skills : (list active skills after customizing skills/ — see SKILLS.md)
```

---

## Active Decisions

None yet. Tulis di sini saat keputusan strategi {{COMPANY_NAME}}-spesifik diambil.

Format pendek:
```
[DECISION] YYYY-MM-DD — Deskripsi singkat
```

Format panjang (untuk keputusan kompleks):
```
[DECISION] YYYY-MM-DD
Context  : <kenapa>
Decision : <apa yang diputuskan>
Impact   : <efek ke sistem / workflow>
Decided by: Fathur
```

---

## Active Projects

None yet.

Format saat ada:
```
[PROJECT] <nama> | Started: YYYY-MM-DD
Goal     : <tujuan>
Owner    : @{{COMPANY_SLUG}}.<role>
Status   : <ACTIVE/PAUSED/DONE>
```

---

## Active Tasks

None yet.

Format:
```
[TASK] ID: XX-001 | Owner: @{{COMPANY_SLUG}}.<role> | Status: NEW/IN_PROGRESS/DONE
Task: <deskripsi>
Date: YYYY-MM-DD
```

---

## Architecture Notes

Tulis di sini saat ada perubahan internal {{COMPANY_NAME}} (role baru, skill baru, struktur change).

```
[ARCH] YYYY-MM-DD — <perubahan>
```

---

## Cross-Company Collaboration Log

Tulis saat {{COMPANY_NAME}} bekerja sama dengan perusahaan lain di holding.

---

## Memory Rules (Company-Scoped)

Tulis ke file ini saat:
- **[DECISION]** keputusan yang affect {{COMPANY_NAME}} specifically.
- **[ARCH]** perubahan internal {{COMPANY_NAME}}.
- **[PROJECT]** project lifecycle change.
- **[TASK]** task aktif.
- **[DONE]** task selesai.
- **[INSIGHT]** insight reusable di domain {{COMPANY_NAME}}.

Jangan tulis di sini:
- Keputusan holding-wide → `MEMORY.md` atau `memory/global.md`.
- Keputusan perusahaan lain → company mereka masing-masing.
- Basa-basi, klarifikasi ringan.

Detail rules: `knowledge/agent-design/memory-rules.md`.
