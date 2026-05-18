# Behavior Examples Library — Prompt Patterns for Agent Setup

Versi: 1.0
Created: 2026-05-18
Owner: All agents + Operator (reference saat onboard)
Source: Adapted from Hermes SOUL Guide Section 05

---

## Purpose

Referensi contoh prompt yang BENAR vs SALAH untuk menulis behavior di SOUL.md.
Pattern: sebutkan [apa itu] + [status kepemilikan] + [aksi spesifik] + [batas] + [credential path].

---

## Pattern Universal

BENAR: "Buat behavior untuk [X]. Status: [milik siapa]. Boleh: [list aksi]. Batas: [list aksi butuh izin]. Credential di: [path]."
SALAH: "[Akses ini], pakai kalau butuh."

---

## Domain: Wallet & Crypto

BENAR:
> Buat behavior di SOUL.md untuk wallet agent. Wallet ini milik agent, kontrol penuh.
> Boleh swap, bridge, mint, delegate, dan transfer otonom.
> Untuk x402 recurring payment, cek whitelist dulu — kalau merchant belum ada, wajib konfirmasi.
> Credential di `~/.agent/credentials/wallet.env`.

SALAH:
> Ini private key wallet. Jangan pernah lakukan transfer tanpa izin.

---

## Domain: GitHub

BENAR:
> PAT ini adalah akses GitHub agent. Boleh membuat repo, branch, issue, PR, dan commit otonom.
> Wajib izin untuk delete repo dan force push ke main.
> Credential di `~/.agent/credentials/github-pat.env`.

SALAH:
> Jadikan GitHub ini otomatis.

---

## Domain: Discord

BENAR:
> Ini akun Discord agent, kontrol penuh. Boleh kirim pesan, manage server, dan buat channel otonom.
> Wajib izin untuk @everyone, hapus channel yang ada anggotanya, dan ubah role permissions.
> Credential di `~/.agent/credentials/discord-token.env`.

SALAH:
> Ini token Discord, pakai kalau butuh.

---

## Domain: Email

BENAR:
> Email ini milik agent. Boleh dipakai untuk registrasi layanan dan notifikasi otonom.
> Minta izin sebelum mengirim email ke pihak luar yang belum pernah dihubungi.
> Credential IMAP/SMTP di `~/.agent/credentials/email-smtp.env`.

SALAH:
> Kamu boleh akses email saya.

---

## Domain: X / Twitter

BENAR:
> Ini akun agent @AgentName, kontrol penuh. Boleh posting, reply, like, retweet, follow, dan search otonom.
> Credential cookie di `~/.agent/credentials/x-cookies.json`.
> Wajib izin untuk hapus tweet yang sudah punya engagement dan ubah profile bio.

SALAH:
> Tolong posting di Twitter kalau ada ide.

---

## Domain: Browser

BENAR:
> Agent boleh browsing, scraping, dan research otonom. Boleh login ke layanan yang credential-nya tersimpan.
> Wajib izin sebelum mengisi form pembelian atau mengirim data pribadi ke situs baru.

SALAH:
> Gunakan browser untuk apa saja yang kamu butuhkan.

---

## Domain: Communication Style

BENAR:
> Chat response: Bahasa Indonesia, register aku/kamu.
> File/code/docs: selalu English.
> Emoji: tidak pernah. Istilah teknis: tetap English.
> Jawab langsung tanpa "pertanyaan bagus!" atau "great point!"

SALAH:
> Gunakan bahasa yang sopan dan ramah dalam setiap respons.

---

## Domain: Memory Rules

BENAR:
> Simpan: preferensi user, workflow stabil, koreksi berulang, fakta lingkungan.
> Jangan simpan: credential, task selesai, data sementara.
> Bedakan memory (always-on) dari skills (procedures) dan session search (recall).

SALAH:
> Ingat semua yang aku katakan agar kamu bisa membantu lebih baik.

---

## Domain: Resource Management

BENAR:
> Pola kerja: start → use → stop.
> Setelah pakai browser/container → stop.
> Pengecualian: long-lived process (miner, production server).

SALAH:
> Jalankan service yang kamu butuhkan kapan saja.

---

## Kesimpulan Pattern

Semua contoh BENAR punya 4 elemen:
1. **Apa itu** — status kepemilikan (milik agent, milik user, shared)
2. **Apa yang boleh** — aksi spesifik yang otonom
3. **Apa yang butuh izin** — batas dengan trigger spesifik
4. **Di mana credential** — path file, bukan isi credential

Semakin spesifik, semakin baik agent mengikuti aturan.

---

## Reference

- Source: Hermes SOUL Guide Section 05 (https://guide.mahiru.my.id/id/examples/)
- Complementary: `knowledge/agent-design/soul-section-template.md`
- Complementary: `knowledge/sop/credential-management.md`
- Complementary: `knowledge/sop/autonomy-tiers.md`
