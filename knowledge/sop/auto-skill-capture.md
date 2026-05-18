# Auto-Skill Capture Policy — Learning from Successful Workflows

Versi: 1.0
Created: 2026-05-18
Owner: All agents
Source: Adapted from Hermes SOUL Guide Section 09 (Waguri — Skills)

---

## Purpose

Setiap workflow yang berhasil adalah pengetahuan yang bisa di-reuse.
Policy ini mengatur kapan agent menyimpan skill, format-nya, dan cara maintain.

Skill = procedural memory. Bukan fakta, tapi "cara melakukan sesuatu."

---

## Trigger: Kapan Simpan Skill?

Agent HARUS menawarkan skill capture ketika:

1. **Workflow berhasil dengan 5+ tool calls** — complexity worth saving.
2. **Error yang berhasil diatasi** — recovery path valuable.
3. **User explicitly minta** — "simpan cara ini sebagai skill."
4. **Pattern yang berulang** — kalau sudah lakukan hal yang sama 2x, bikin skill.

Agent TIDAK perlu simpan skill untuk:
- Aksi trivial (1-2 step, obvious)
- One-off task yang tidak akan diulang
- Task yang sudah ada skill-nya (update saja kalau ada perubahan)

---

## Format Skill

```markdown
# Skill: [Nama Skill]

Versi: [1.0]
Created: [YYYY-MM-DD]
Owner: [@company.agent]
Trigger: [kapan skill ini dipakai]

---

## Steps

1. [Step 1 — aksi spesifik]
2. [Step 2 — aksi spesifik]
3. ...

## Prerequisites

- [Tool/akses yang dibutuhkan]
- [Credential yang perlu ada]

## Common Errors & Recovery

- [Error X] → [Recovery Y]

## Verify

- [Cara verify skill berhasil dijalankan]

## Notes

- [Hal yang perlu diperhatikan]
```

---

## Lokasi Penyimpanan

```
companies/[company]/skills/[domain]/[skill-name].md
```

Contoh:
- `companies/nexusai/skills/devops/deploy-vps.md`
- `companies/brandflow/skills/content/thread-creation.md`
- `companies/crypto-consultant/skills/onchain/whale-tracking.md`

Cross-company skills (applicable untuk semua):
```
knowledge/sop/[skill-name].md
```

---

## Skill Lifecycle

### Creation
Agent selesaikan task kompleks → menawarkan: "Mau aku simpan workflow ini sebagai skill?"
Atau agent detect pattern berulang → langsung simpan (Tier 2: autonomous + log).

### Usage
Saat task baru mirip dengan skill yang ada → agent load skill → ikuti steps.
Tidak perlu belajar ulang.

### Patching
Saat skill dipakai dan ditemukan step yang outdated atau error:
- Agent fix step yang bermasalah
- Update versi
- Log patch: "Step 3 updated karena API endpoint berubah"

### Retirement
Saat skill tidak relevan lagi (tool deprecated, workflow berubah total):
- Move ke `archive/` atau hapus
- Log retirement reason

---

## Integration dengan Existing System

- Skills complement memory (memory = fakta, skills = prosedur)
- Skills complement SOUL (SOUL = rules, skills = how-to)
- Skills directory per company sudah ada → format ini standardisasi isi-nya
- QA agents bisa review skills saat System Audit (Friday)

---

## Anti-Patterns

❌ Simpan semua workflow sebagai skill — hanya yang complex + reusable.
❌ Skill tanpa verify step — bagaimana tahu skill berhasil?
❌ Skill outdated yang tidak di-patch — worse than no skill (misleading).
❌ Skill di memory — skill adalah file terpisah, bukan entry di memory.
❌ Skip offering skill capture — pengetahuan yang hilang tidak bisa di-recall.

---

## Reference

- Source: Hermes SOUL Guide Section 09 (https://guide.mahiru.my.id/id/waguri/)
- Existing: `companies/*/skills/` (per-company skill directories)
- Complementary: `knowledge/sop/testing-iteration.md` (validate skill works)
