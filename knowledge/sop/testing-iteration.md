# Testing & Iteration SOP — Behavior Validation Loop

Versi: 1.0
Created: 2026-05-18
Owner: All agents + Operator
Source: Adapted from Hermes SOUL Guide Section 06

---

## Purpose

Testing adalah BAGIAN DARI setup, bukan afterthought.
Setiap behavior baru harus divalidasi melalui iterasi: task kecil → nilai → koreksi → simpan.

Agent yang baik tidak lahir dari satu prompt — ia terbentuk dari koreksi berulang.

---

## The 3-Step Loop

### Step 1: Task Kecil Dulu

Mulai dari aksi read-only atau low-risk:
- Cek balance / cek channel / baca repo
- Rangkum email / rangkum diskusi
- Research tanpa aksi (scrape, summarize)

**JANGAN** langsung kasih task yang melibatkan uang, aksi publik, atau irreversible.
Bangun kepercayaan lewat aksi yang aman dulu.

### Step 2: Nilai Hasilnya

Perhatikan 5 dimensi:

| Dimensi | Yang Dicek |
|---------|-----------|
| Bahasa & tone | Register benar? Emoji? Terlalu formal/kasual? |
| Level otonomi | Langsung jalan vs minta izin — sesuai ekspektasi? |
| Tool selection | Pilih tool yang tepat? (wallet tool, bukan web search) |
| Verifikasi | Agent cek hasilnya? (tx hash, build status, endpoint test) |
| Error handling | Retry? Menyerah? Lapor informatif atau cuma bilang "gagal"? |

### Step 3: Koreksi Permanen

Setiap koreksi HARUS disimpan:
- Aturan umum (berlaku di semua konteks) → simpan ke **SOUL.md**
- Preferensi spesifik (konteks tertentu) → simpan ke **memory**
- Workflow yang berhasil (5+ tool calls) → simpan sebagai **skill**

**Koreksi yang tidak disimpan akan terulang di session berikutnya.**

---

## Behavior Pathology — Tanda Perlu Diperbaiki

### Terlalu Pasif

**Gejala:** Agent selalu minta izin bahkan untuk aksi yang seharusnya otonom.
**Root cause:** SOUL.md terlalu banyak "wajib izin" tanpa menjelaskan kapan boleh langsung.
**Fix:** Tambahkan section "Fully autonomous" yang eksplisit dengan contoh aksi.

### Terlalu Agresif

**Gejala:** Agent langsung eksekusi tanpa konfirmasi untuk aksi berisiko.
**Root cause:** SOUL.md tidak jelaskan batas, atau agent salah baca level risiko.
**Fix:** Tambahkan section "Wajib konfirmasi" dengan contoh aksi spesifik.

### Terlalu Verbose

**Gejala:** Penjelasan panjang untuk pertanyaan sederhana.
**Root cause:** Tidak ada aturan tentang panjang jawaban.
**Fix:** Tambahkan: "jawab singkat dan langsung, jangan bertele-tele, no preamble."

### Salah Konteks

**Gejala:** Agent bawa konteks dari project/company lain.
**Root cause:** SOUL.md terlalu umum, tidak ada domain boundary.
**Fix:** Tambahkan domain-specific rules atau memory per project.

### Over-Cautious (Refuse/Lecture)

**Gejala:** Agent menolak request atau memberikan paragraf warning.
**Root cause:** Tidak ada Default Disposition di SOUL.md.
**Fix:** Tambahkan: "Asumsi user tahu apa yang dilakukan. Tanya konteks, jangan refuse."

---

## Iteration Cadence

| Phase | Duration | Focus |
|-------|----------|-------|
| Onboard (baru) | 3-5 hari | Task kecil, koreksi intensif, simpan banyak |
| Stabilize | 1-2 minggu | Task normal, koreksi berkurang, behavior menetap |
| Mature | Ongoing | Koreksi jarang, mostly upgrade/expand capabilities |

---

## When To Run Testing

- Setelah SOUL.md baru ditulis atau di-update major
- Setelah credential/akses baru diberikan
- Setelah behavior baru ditulis (dari template)
- Setelah upgrade (UPGRADE.md / UPGRADE2.md)
- Setelah bug yang terkait agent behavior

---

## Reference

- Source: Hermes SOUL Guide Section 06 (https://guide.mahiru.my.id/id/testing/)
- Complementary: `knowledge/agent-design/soul-section-template.md`
- Complementary: `knowledge/sop/autonomy-tiers.md`
- Complementary: `knowledge/agent-design/reflection-loop.md`
