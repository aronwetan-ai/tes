# Memory Rules — AI Holding

Versi: 1.0  
Update terakhir: 2026-05-17  
Berlaku untuk: Main Assistant + semua agent  

---

## Prinsip Dasar

Memory adalah aset jangka panjang. Jangan isi dengan noise.

> Catat yang penting, buang yang basa-basi.  
> Memory yang penuh sampah lebih berbahaya dari memory yang kosong.

---

## Apa yang WAJIB Dicatat

### Kategori 1 — Keputusan Strategis
- Keputusan arah produk atau bisnis.
- Perubahan fokus perusahaan.
- Approval atau rejection dari user terhadap proposal besar.

Contoh:
[DECISION] 2026-05-17 — Fathur memutuskan tidak pakai Google Trends dulu karena API berbayar.

### Kategori 2 — Task Penting yang Sedang Berjalan
- Task dengan prioritas HIGH atau MEDIUM.
- Task yang melibatkan lebih dari satu agent.
- Task yang hasilnya akan dipakai lagi di masa depan.

Format:
[TASK] ID: XX-001 | Company: nexusai | Agent: ceo | Task: <deskripsi> | Status: IN_PROGRESS | Date: 2026-05-17

### Kategori 3 — Perubahan Arsitektur
- Penambahan perusahaan baru.
- Penambahan atau penghapusan agent.
- Perubahan struktur folder workspace.
- Update file konfigurasi utama (MAIN.md, SOUL.md, AGENTS.md).

### Kategori 4 — Tool Baru atau Update Tool
- Tool baru yang ditambahkan ke registry.
- Tool yang dinonaktifkan.
- Perubahan path atau command tool.

### Kategori 5 — Temuan Penting dari Riset
- Insight crypto yang punya dampak keputusan nyata.
- Temuan teknis yang mempengaruhi arsitektur.
- Perubahan kondisi market yang signifikan.

---

## Apa yang TIDAK Perlu Dicatat

- Ucapan terima kasih ("makasih", "oke", "siap").
- Konfirmasi ringan ("ya", "lanjutkan", "betul").
- Pertanyaan klarifikasi tanpa keputusan.
- Chat santai atau basa-basi.
- Jawaban yang tidak menghasilkan keputusan atau perubahan.
- Pertanyaan yang sudah dijawab dan tidak akan ditanya lagi.

---

## Format Memory Entry

### Format Pendek (untuk kebanyakan entry)
[TAG] YYYY-MM-DD — Deskripsi singkat (max 1 baris)

Tag yang dipakai:
- [DECISION] — Keputusan yang sudah final
- [TASK] — Task yang sedang berjalan atau baru dibuat
- [DONE] — Task yang selesai
- [TOOL] — Perubahan tool atau registry
- [ARCH] — Perubahan arsitektur
- [INSIGHT] — Temuan atau insight penting
- [NOTE] — Catatan yang tidak masuk kategori lain

### Format Panjang (untuk keputusan kompleks)
[DECISION] YYYY-MM-DD
Context: <kenapa keputusan ini diambil>
Decision: <apa yang diputuskan>
Impact: <efek ke sistem atau workflow>
Decided by: Fathur

---

## Kapan Memory Dibaca

Agent membaca memory yang relevan:
- Saat memulai task baru di domain yang sama.
- Saat user menyebut project atau task lama.
- Saat ada konflik antara instruksi baru dan keputusan lama.

Agent TIDAK perlu membaca semua memory setiap saat.
Baca hanya memory yang relevan dengan konteks saat ini.

---

## Lokasi File Memory
/home/fatur/ai-holding/memory/
├── global.md          ← Memory utama AI Holding
├── companies/
│   ├── nexusai.md
│   ├── brandflow.md
│   └── crypto.md
└── tasks/
└── active.md

---

## Aturan Maintenance Memory

- Memory global dibaca oleh Main Assistant setiap sesi baru.
- Memory perusahaan dibaca oleh agent saat routing masuk.
- Task yang sudah DONE dipindahkan dari active.md ke arsip bulanan.
- Memory tidak boleh dihapus tanpa konfirmasi user.
- Jika memory sudah panjang (>200 baris), buat ringkasan dan arsipkan yang lama.
