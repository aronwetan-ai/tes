# SOP — Reusable Skills Library

Versi: 1.0
Update terakhir: 2026-05-17
Scope: Skill kecil yang bisa dipakai lintas perusahaan.

---

## Tujuan Folder Ini

Folder ini berisi **skill reusable** — pola kerja kecil yang dipakai oleh banyak agent di perusahaan berbeda.

Beda dengan `knowledge/<domain>/`:
- `knowledge/software/` → SOP khusus NexusAI.
- `knowledge/marketing/` → SOP khusus BrandFlow.
- `knowledge/sop/` → skill umum yang **tidak terikat satu perusahaan**.

Contoh:
- "Cara meringkas teks panjang" → bisa dipakai @nexusai.writer, @brandflow.copywriter, @crypto.report.
- "Cara format JSONL task" → dipakai semua perusahaan untuk task logger.
- "Cara nulis disclaimer" → terutama @crypto.*, tapi bisa dipakai lain.

---

## Struktur Skill File

Setiap skill file pakai format ini:

```
# Skill: <nama skill>

Tujuan: <satu kalimat>
Used by: <list agent yang biasa pakai>
Risk level: Low / Medium / High

## Input
<apa yang dibutuhkan>

## Steps
1. ...
2. ...
3. ...

## Output Format
<seperti apa hasil akhirnya>

## Contoh
<contoh konkret minimal 1>

## Catatan
<edge case, limitations, atau tips>
```

---

## Skill yang Direncanakan

Status: **PLANNED — belum dibuat satu per satu**

| Filename                  | Tujuan                                   | Priority |
|---------------------------|------------------------------------------|----------|
| summarize-long-text.md    | Meringkas teks > 500 kata jadi 3-5 poin  | HIGH     |
| extract-key-points.md     | Ekstrak fakta/keputusan dari diskusi     | HIGH     |
| format-jsonl-task.md      | Format task ke schema JSONL standar      | HIGH     |
| write-disclaimer.md       | Tulis disclaimer crypto / financial      | MEDIUM   |
| compare-options.md        | Bandingkan 2-3 opsi dengan trade-off     | MEDIUM   |
| draft-followup-message.md | Tulis follow-up message setelah meeting  | LOW      |
| extract-action-items.md   | Pull action items dari teks              | LOW      |

Skill di-create on-demand ketika polanya muncul lebih dari sekali.

---

## Aturan Maintenance

- Setiap skill file maksimal 1 layar (< 80 baris).
- Update versi setiap kali ada revisi major.
- Jika skill mulai khusus untuk satu perusahaan, **pindahkan** ke folder perusahaan tersebut.
- Jika dua perusahaan butuh variasi yang sama tapi beda, buat 1 skill base + spesifik per perusahaan di folder mereka.

---

## Cara Agent Pakai Skill

Saat agent dapat task yang match dengan skill yang ada:

1. Baca file skill di folder ini.
2. Ikuti steps-nya.
3. Output sesuai format yang ditentukan.
4. Jika hasil tidak match expectation, jangan modify ad-hoc — usulkan **improve skill** ke Fathur.

---

## Referensi

- Core principles: `knowledge/core/principles.md`
- Memory rules: `knowledge/agent-design/memory-rules.md`
- Tool use rules: `knowledge/agent-design/tool-use-rules.md`
