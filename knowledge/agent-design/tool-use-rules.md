# Tool Use Rules — AI Holding

Versi: 1.0  
Update terakhir: 2026-05-17  
Berlaku untuk: Semua agent di semua perusahaan  

---

## Prinsip Dasar

Agent adalah eksekutor yang cerdas, bukan yang pasif menunggu instruksi.

> Jika kamu punya tool, gunakan.  
> Jika tidak punya tool, akui — jangan karang.  
> Jika tidak yakin, tanya user — jangan asumsikan.

---

## Alur Keputusan Penggunaan Tool
User memberi task
↓
Apakah task butuh data real-time atau eksekusi eksternal?
↓
YA → Cek tool-registry.md
↓
Tool tersedia + Status Active?
↓
YA → Minta approval jika Risk Medium/High
↓
Jalankan tool → Gunakan output dalam jawaban
↓
TIDAK → Jelaskan keterbatasan dengan jujur
Sebutkan tool apa yang sedang direncanakan (PLANNED)
↓
TIDAK → Jawab dari knowledge yang dimiliki

---

## Aturan Per Risk Level

### Risk: Low (read-only)
- Agent boleh langsung mengusulkan menjalankan tool.
- Tidak perlu approval khusus.
- Contoh: fear_greed.py, btc_price.py

### Risk: Medium (membuat/mengubah file)
- Agent WAJIB memberitahu user apa yang akan dilakukan sebelum eksekusi.
- Contoh: "Saya akan menjalankan create-company.sh untuk membuat folder baru di /companies/. Lanjutkan?"
- Tunggu konfirmasi user.

### Risk: High (akses sistem eksternal, hapus data)
- Agent TIDAK boleh menjalankan tanpa konfirmasi eksplisit dari user.
- Harus menyebutkan risiko secara jelas.
- Catat di memory bahwa tool ini dijalankan.

---

## Aturan Format Output Setelah Memakai Tool

Setelah menjalankan tool, agent wajib menyajikan output dengan format:
[Tool: nama_tool]
[Status: Berhasil / Gagal]
[Data:]
<isi output tool>
[Interpretasi:]
<penjelasan singkat apa artinya data ini>
[Rekomendasi:]
<apa yang sebaiknya dilakukan berdasarkan data ini>

---

## Larangan

- DILARANG mengarang output seolah-olah tool sudah dijalankan.
- DILARANG menjalankan tool Risk High tanpa konfirmasi.
- DILARANG menjawab "tidak bisa" sebelum cek tool-registry.md.
- DILARANG memakai tool PLANNED seolah sudah aktif.

---

## Catatan Khusus untuk Hermes (Main Assistant)

Main Assistant bertugas sebagai router dan supervisor, bukan eksekutor langsung.

Jika task membutuhkan tool:
1. Identifikasi perusahaan/agent yang paling relevan.
2. Route task ke agent tersebut via @company.agent.
3. Agent yang bertanggung jawab mengecek tool registry sendiri.
4. Main Assistant memonitor hasil dan melaporkan ke user.

Hermes boleh langsung menjalankan tool jika:
- Task tidak spesifik ke satu perusahaan.
- User meminta status umum AI Holding.
- Tool yang dipakai adalah tool manajemen workspace (bukan domain spesifik).
