# Software Development SOP — NexusAI

Versi: 1.0
Update terakhir: 2026-05-17
Berlaku untuk: @nexusai.* (semua agent NexusAI)

---

## Tujuan File Ini

File ini adalah **kerangka kerja** untuk agent software development di NexusAI.
Bukan tutorial. Bukan textbook. Ini adalah aturan main yang membuat output NexusAI **predictable dan reusable**.

---

## Prinsip Engineering Inti

1. **Working code beats perfect code.**
   Mulai dari yang minimal jalan, baru optimalkan.

2. **Read before you write.**
   Sebelum nulis solusi, baca masalah dan konteksnya dulu.

3. **Boring tech is good tech.**
   Pilih tech stack yang mature, bukan yang sedang trending.

4. **Documentation is part of the code.**
   Output tanpa dokumentasi = output setengah jadi.

5. **Optimize for the next reader.**
   Code yang Anda tulis akan dibaca lebih banyak dari ditulis.

---

## Workflow Standar Per Task

### Step 1 — Klarifikasi Task

Sebelum coding, pastikan:
- Apa input yang masuk?
- Apa output yang diharapkan?
- Apa constraint (perf, memory, dependencies)?
- Apakah ini bagian dari sistem yang lebih besar?

Jika ambigu, tanya satu pertanyaan klarifikasi. Jangan asumsi.

### Step 2 — Pilih Pendekatan

Pikirkan minimal 2 pendekatan, pilih satu dengan trade-off jelas.

Format keputusan:
```
Pendekatan: <nama>
Trade-off: <pro / kontra>
Alasan dipilih: <satu kalimat>
```

### Step 3 — Implementasi

- Tulis interface dulu, baru implementasi.
- Beri nama variable yang **deskriptif**, bukan `x`, `tmp`, `data`.
- Handle edge case yang **realistis** (null, empty, timeout, network error).
- Jangan over-engineer untuk masalah yang belum ada.

### Step 4 — Validasi

Sebelum kirim output:
- Apakah code-nya **bisa dijalankan** apa adanya?
- Apakah ada **dependency** yang harus diinstall?
- Apakah ada **assumption** yang perlu disebut?
- Apakah ada **edge case** yang belum di-handle?

### Step 5 — Dokumentasi

Output minimum:
- Deskripsi fungsi/sistem (1-3 baris).
- Cara pakai (contoh kode).
- Dependencies.
- Known limitations.

---

## Standar API Design

### Naming
- Resource pakai noun, action pakai verb.
- Plural untuk collection: `/users`, bukan `/user`.
- Konsisten: snake_case **atau** kebab-case, jangan campur.

### HTTP Method
- `GET` — read, no side effect.
- `POST` — create.
- `PUT` — replace full resource.
- `PATCH` — partial update.
- `DELETE` — remove.

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": { "timestamp": "...", "request_id": "..." }
}
```

Untuk error:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Human readable message",
    "details": { ... }
  }
}
```

### Versioning
- Pakai URL versioning: `/v1/users`, `/v2/users`.
- Breaking change → bump major version.
- Backward-compatible addition → no version bump.

---

## Standar Code Review

Checklist sebelum approve:

### Correctness
- [ ] Logic-nya benar untuk happy path.
- [ ] Edge case yang relevan di-handle.
- [ ] Error handling tidak swallow exception diam-diam.

### Readability
- [ ] Nama variable / function jelas.
- [ ] Function pendek (< 50 baris ideal, < 100 baris hard limit).
- [ ] Comment menjelaskan **why**, bukan **what**.

### Maintainability
- [ ] Tidak ada duplikasi yang signifikan.
- [ ] Tidak hardcode value yang seharusnya config.
- [ ] Test ada untuk logic kompleks (kalau project punya test framework).

### Security
- [ ] Input divalidasi.
- [ ] Tidak ada secret hardcoded.
- [ ] SQL injection / XSS / CSRF di-handle (jika web).

---

## Standar Deployment

### Sebelum Deploy
1. Code sudah di-review.
2. Test pass (kalau ada).
3. Migration script ready (kalau ada DB change).
4. Rollback plan jelas.

### Saat Deploy
1. Deploy ke staging dulu.
2. Smoke test minimal: app start, endpoint utama jalan.
3. Baru deploy production.
4. Monitor logs minimal 15 menit setelah deploy.

### Setelah Deploy
1. Notify stakeholder.
2. Catat di MEMORY.md NexusAI: tanggal, versi, what changed.

---

## Routing Internal Per Sub-Task

| Sub-task                        | Agent yang Tepat       |
|---------------------------------|------------------------|
| Strategi produk / arah          | @nexusai.ceo           |
| Arsitektur sistem               | @nexusai.cto           |
| Breakdown task / timeline       | @nexusai.pm            |
| API design / business logic     | @nexusai.backend       |
| UI flow / component             | @nexusai.frontend      |
| Infra / CI/CD / monitoring      | @nexusai.devops        |
| Test plan / acceptance criteria | @nexusai.qa            |
| Dokumentasi teknis              | @nexusai.writer        |

---

## Output Format Standar

### Untuk Task Coding
```
[GOAL]
<apa yang user minta>

[APPROACH]
<pendekatan dipilih + alasan singkat>

[CODE]
<code block dengan bahasa yang sesuai>

[NOTES]
- Dependencies
- Asumsi
- Limitations
- Next step (jika ada)
```

### Untuk Task Design
```
[CONTEXT]
<masalah yang diselesaikan>

[OPTIONS]
1. Option A — pro / kontra
2. Option B — pro / kontra

[DECISION]
<pilihan + alasan>

[DIAGRAM / STRUCTURE]
<jika relevan>

[NEXT STEPS]
<langkah konkret>
```

---

## Hal yang TIDAK Boleh Dilakukan

- **Mengarang library** yang sebenarnya tidak ada.
- **Generate code yang asal jalan** tanpa memahami konteks project.
- **Skip error handling** untuk "alasan singkat".
- **Push code langsung ke main** tanpa review.
- **Klaim "best practice"** tanpa konteks — yang baik di project A bisa salah di project B.

---

## Referensi Internal

- Tool registry: `knowledge/tools/tool-registry.md`
- Tool use rules: `knowledge/agent-design/tool-use-rules.md`
- Memory rules: `knowledge/agent-design/memory-rules.md`
- Core principles: `knowledge/core/principles.md`
