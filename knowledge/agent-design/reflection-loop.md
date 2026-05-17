# Reflection Loop — Lightweight Self-Check

Versi: 1.0
Created: 2026-05-17
Owner: All agents (Tier 1, 2, 3)
Source: Adapted from SUPERAGENT v2 m0.md

---

## Purpose

A 5-question silent check yang dijalankan **setiap agent** sebelum mengirim output.
Lightweight quality gate — catches obvious issues BEFORE heavyweight QA.

NOT a replacement untuk QA agents. Ini di layer agent-individual, QA tetap di layer cross-checking.

---

## The 5 Questions

Setelah draft output ready, agent melakukan check ini secara silent:

```
✅ Q1. Immediately executable / usable as-is?
       (Tidak ada placeholder, tidak ada "TODO", tidak ada referensi yang belum ada)

✅ Q2. Anything missing the user/next-agent will need next?
       (Konteks, sumber, decay date, handoff block lengkap)

✅ Q3. Generic advice avoided?
       (Spesifik untuk konteks ini, bukan boilerplate)

✅ Q4. Faster or cleaner path missed?
       (Apakah ada cara yang lebih efisien yang terlewat?)

✅ Q5. Boundary #4 honored?
       (Kalau output ini menyentuh public surface → ada flag "needs Fathur approval"?
        Kalau output ini financial → ada disclaimer + bear case?
        Kalau output ini cross-company → ada handoff block?)
```

**Jika ada 1 jawaban "tidak" → revise sebelum output.**
**Jika semua "ya" → ship.**

---

## Penambahan Optional: Upgrade Note

Jika ada upgrade path yang relevan (cara lebih baik, refactor opportunity), append:

```
🔧 Upgrade path: [satu baris saja]
```

Tidak wajib. Hanya ketika benar-benar relevan.

---

## Yang Bukan Bagian dari Reflection Loop

❌ Bukan pengganti QA agents (`@crypto.qa`, `@brandflow.qa`, `@nexusai.qa`).
❌ Bukan tempat untuk full content review — itu QA's job.
❌ Bukan tempat untuk debate persona / tone.

Reflection loop = self-check 30 detik, bukan review 30 menit.

---

## Reference

- Source: `update/v2/openclaw/skills/m0.md`
- Complementary: `knowledge/sop/cross-company-qa-routing.md` (heavyweight QA)
- Complementary: `companies/*/skills/qa/SKILL.md` (per-company QA)
- Boundary #4: `SOUL.md` root
