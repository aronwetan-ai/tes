# Memory Rules — AI Holding

Versi: 2.0
Update terakhir: 2026-05-17 (post Update 6 — memory reference clarification)
Berlaku untuk: Main Assistant + semua agent

---

## Prinsip Dasar

Memory adalah aset jangka panjang. Jangan isi dengan noise.

> Catat yang penting, buang yang basa-basi.
> Memory yang penuh sampah lebih berbahaya dari memory yang kosong.

---

## Struktur Memory di Holding (Authoritative)

Memory dibagi berdasarkan **scope** dan **format**. Setiap file punya peran berbeda — jangan dicampur.

### Holding-level (2 files, dipakai oleh Main Assistant + cross-company concerns)

| File | Sifat | Format | Read at | Write when |
|---|---|---|---|---|
| `MEMORY.md` (root) | Strategic / narrative | Paragraphs, tabel struktural | Session start | Strategic decision, architecture restructure, migration milestone |
| `memory/global.md` | Operational / tagged log | Tagged entries | Session start, before related task | Day-to-day durable decisions, task state, tool changes, insights |

### Company-level (1 file per company)

| File | Sifat | Format | Read at | Write when |
|---|---|---|---|---|
| `companies/<co>/MEMORY.md` | Company-scoped narrative + tagged log | Mixed (identity section narrative, decisions/projects/tasks tagged) | Agent gets task in this company | Company-scoped decision, project state change, learning |

### Agent-level

Tidak ada file memory terpisah per agent. Agent tulis ke company MEMORY.md dengan tagging yang menyebut role-nya jika relevan.

---

## Kapan Pakai File Mana

```
Decision is...                          Write to...
─────────────────────────────────────   ─────────────────────────────────
Strategic / arsitektur holding-wide  →  MEMORY.md (root)
Day-to-day operational, holding-wide →  memory/global.md
Company-scoped (NexusAI / BrandFlow / Crypto) → companies/<co>/MEMORY.md
Cross-company impact                  →  memory/global.md AND each affected company MEMORY.md
```

A single decision **boleh** ditulis di lebih dari satu file kalau memang bersifat strategic + operational + per-company.

---

## Apa yang WAJIB Dicatat

### Kategori 1 — Keputusan Strategis
- Arah produk / bisnis.
- Perubahan fokus perusahaan.
- Approval / rejection user terhadap proposal besar.
- Pivot atau migration.

Contoh: `[DECISION] 2026-05-17 — Fathur memutuskan tidak pakai Google Trends dulu karena API berbayar.`

### Kategori 2 — Task Penting yang Sedang Berjalan
- Task priority HIGH atau MEDIUM.
- Task multi-agent.
- Task dengan output yang akan reusable.

Format: `[TASK] ID: XX-001 | Company: nexusai | Agent: ceo | Task: <deskripsi> | Status: IN_PROGRESS | Date: 2026-05-17`

### Kategori 3 — Perubahan Arsitektur
- Penambahan / penghapusan perusahaan.
- Penambahan / penghapusan agent.
- Perubahan struktur folder workspace.
- Update file konfigurasi utama (MAIN.md, SOUL.md, AGENTS.md, COMMANDS.md).
- Perubahan SOUL hierarchy (Tier 2/3 SOULs).

### Kategori 4 — Tool Baru atau Update Tool
- Tool baru ditambahkan ke registry.
- Tool dinonaktifkan atau status berubah (Active ↔ PLANNED ↔ Deprecated).
- Perubahan path / command tool.

### Kategori 5 — Insight Penting dari Riset / Kerja
- Insight crypto yang punya dampak keputusan nyata.
- Temuan teknis yang mempengaruhi arsitektur.
- Perubahan kondisi market yang signifikan.
- Pattern yang berulang dan perlu di-codify jadi skill.

---

## Apa yang TIDAK Perlu Dicatat

- Ucapan terima kasih ("makasih", "oke", "siap").
- Konfirmasi ringan ("ya", "lanjutkan", "betul").
- Pertanyaan klarifikasi tanpa keputusan.
- Chat santai / basa-basi.
- Jawaban yang tidak menghasilkan keputusan / perubahan.
- Pertanyaan yang sudah dijawab dan tidak akan ditanya lagi.

---

## Format Memory Entry

### Format Pendek (untuk kebanyakan entry di `memory/global.md` + company MEMORY.md)

```
[TAG] YYYY-MM-DD — Deskripsi singkat (max 1 baris)
```

Tag yang dipakai:

| Tag | Untuk |
|---|---|
| `[DECISION]` | Keputusan yang sudah final |
| `[TASK]` | Task sedang berjalan atau baru dibuat |
| `[DONE]` | Task yang selesai |
| `[TOOL]` | Perubahan tool atau registry |
| `[ARCH]` | Perubahan arsitektur |
| `[INSIGHT]` | Temuan / insight penting |
| `[NOTE]` | Catatan operasional yang tidak fit kategori atas |

### Format Panjang (untuk keputusan kompleks; bisa di `MEMORY.md` atau company MEMORY.md)

```
[DECISION] YYYY-MM-DD
Context: <kenapa keputusan ini diambil>
Decision: <apa yang diputuskan>
Impact: <efek ke sistem atau workflow>
Decided by: Fathur
```

### Format Narrative (khusus `MEMORY.md` root + company MEMORY.md identity section)

Paragraph atau tabel struktural. Bukan tagged log. Lihat current `MEMORY.md` untuk contoh.

---

## Kapan Memory Dibaca

Setiap agent membaca memory yang relevan:

| Saat | Baca |
|---|---|
| Session start (Main Assistant) | `MEMORY.md` + `memory/global.md` |
| Agent dapat task company-scoped | `companies/<co>/MEMORY.md` |
| Topic terkait keputusan lama | Memory yang relevan |
| Konflik instruksi baru vs lama | Memory yang relevan untuk verifikasi |

Agent **tidak** perlu membaca semua memory setiap saat. Read what's relevant.

---

## Aturan Maintenance Memory

- **Memory tidak dihapus tanpa konfirmasi user**, kecuali pemindahan ke arsip.
- Memory yang panjang (>200 baris di `memory/global.md` atau company MEMORY.md): buat ringkasan, arsipkan yang lama ke `memory/archive/<YYYY-MM>.md`.
- Task `[TASK]` yang selesai → ubah jadi `[DONE]` lalu pindah ke section archive bulanan kalau sudah lebih dari 30 hari.
- Konflik antar entries: latest wins, tapi catat sebagai `[DECISION] superseding [<old date>]`.

---

## Anti-Pattern

- ❌ Menulis basa-basi sebagai `[NOTE]`.
- ❌ Menulis `[TASK]` tanpa ID, owner, atau status.
- ❌ Menulis `[DECISION]` tanpa konteks atau impact.
- ❌ Mencampur company memory di `memory/global.md`. Pakai company MEMORY.md.
- ❌ Mencampur strategic dan operational di `MEMORY.md` (root). Operational pakai `memory/global.md`.
- ❌ Memory yang panjang tanpa di-arsipkan — bikin context window agent meledak.

---

## Reference

- `MEMORY.md` (root) — strategic narrative.
- `memory/global.md` — operational tagged log.
- `companies/<co>/MEMORY.md` — company-scoped.
- `MAIN.md` — startup read order.
- `AGENTS.md` — Memory Reference Rules section.
