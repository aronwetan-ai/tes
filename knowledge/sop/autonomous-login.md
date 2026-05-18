# Autonomous Login SOP — Google & X/Twitter

Versi: 1.0
Created: 2026-05-18
Owner: All agents yang punya akses web login
Source: Adapted from Hermes SOUL Guide Section 07

---

## Purpose

Agent yang bisa login sendiri tanpa bantuan user = agent yang benar-benar mandiri.
SOP ini cover: credential setup, 2FA handling, session persistence, dan recovery.

---

## Prinsip Umum

1. **Simpan credential dengan aman** — di `~/.agent/credentials/`, bukan di SOUL/code/env yang bocor ke log.
2. **Handle semua jalur autentikasi** — password + 2FA (TOTP/backup codes) + CAPTCHA (anti-detect browser).
3. **Deteksi & recovery** — detect session expired → re-login otomatis → fallback ke manual sebagai last resort.
4. **Jangan minta bantuan untuk hal yang bisa diotomasi** — TOTP bisa di-generate lokal, cookies bisa di-load.

---

## Google Login

### Credential Setup

Simpan di `~/.agent/credentials/google-auth.txt`:
```
email: agent@example.com
password: [password]
totp_secret: [TOTP secret key dari 2FA setup — 16+ karakter base32]
backup_codes:
  - [code1]
  - [code2]
  - ... (generate 10 dari Google settings)
```

### TOTP Generation (Otonom)

Agent generate 6-digit code lokal tanpa Google Authenticator:

```python
import pyotp

secret = "[TOTP_SECRET dari credential file]"
totp = pyotp.TOTP(secret)
code = totp.now()  # Valid 30 detik
```

### Login Flow

```
1. Buka browser anti-detect → accounts.google.com
2. Input email → Next
3. Input password → Next
4. Jika 2FA diminta:
   a. Generate TOTP dari secret key
   b. Input 6-digit code → Next
   c. Jika TOTP fail → pakai backup code (sekali pakai)
5. Verify login berhasil (cek cookies / redirect ke inbox)
6. Simpan session cookies untuk reuse
```

### Session Persistence

- Google cookies bertahan berminggu-minggu sampai bulan.
- Agent detect expired: HTTP 401 / redirect ke login page → trigger re-login.
- Simpan cookies di `~/.agent/credentials/google-cookies.json`.

---

## X / Twitter Login

### Metode 1: Cookie-Based (Primary — Paling Stabil)

Login manual 1x → export cookies → agent pakai untuk semua operasi.

**Credential:** `~/.agent/credentials/x-cookies.json`

**Kelebihan:**
- Tidak kena anti-bot (Cloudflare)
- Tidak perlu handle 2FA
- Session bertahan berminggu-minggu
- Cover semua operasi: post, delete, reply, like, RT, follow, DM, media upload

**Kekurangan:**
- Perlu login manual 1x untuk export
- Kalau expired → perlu re-login manual ATAU fallback ke Metode 2

### Metode 2: Username + Password + Backup Code (Fallback)

Agent login langsung. Cocok untuk fresh start atau re-login otomatis.

**Credential:** `~/.agent/credentials/x-auth.env`
```
X_USERNAME=[username]
X_PASSWORD=[password]
X_BACKUP_CODES=[code1,code2,code3,...]
```

**Kelebihan:**
- Full autonomous — tidak perlu manual sama sekali
- Backup code handle 2FA otomatis
- Cocok saat cookies expired

**Kekurangan:**
- Rentan anti-bot (Cloudflare 403) — butuh browser anti-detect
- Backup codes limited quantity

### Decision: Kapan Pakai Metode Mana?

```
Default operasi harian → Metode 1 (cookies)
Cookies expired        → Coba Metode 2 (username + backup code)
Metode 2 gagal (anti-bot) → Request re-login manual (last resort)
```

---

## Browser Anti-Detect Requirements

Untuk login ke Google dan X, agent butuh browser yang:
- Support humanize mode (random delays, natural mouse movement)
- Fingerprint randomization (canvas, WebGL, timezone, language)
- Persistent session (cookies survive restart)
- Tidak kena anti-bot detection (Cloudflare, reCAPTCHA)

Recommended: Camofox atau browser anti-detect yang support CDP.

---

## Recovery Hierarchy

```
1. Load saved cookies → cek masih valid
2. Kalau expired → re-login otomatis (TOTP / backup code)
3. Kalau re-login gagal → coba fallback credentials
4. Kalau semua gagal → log error + notify operator "butuh re-login manual"
```

JANGAN langsung minta user. Exhaust semua opsi otonom dulu.

---

## Anti-Patterns

❌ Minta user masukkan 2FA code — kalau TOTP secret ada, generate sendiri.
❌ Minta user login manual — kalau ada backup code, pakai dulu.
❌ Tidak detect session expired — agent fail tanpa tahu kenapa.
❌ Credential di SOUL.md — bocor ke context/log.
❌ Hanya punya 1 metode tanpa fallback — single point of failure.

---

## Reference

- Source: Hermes SOUL Guide Section 07 (https://guide.mahiru.my.id/id/login/)
- Credential storage: `knowledge/sop/credential-management.md`
- Browser config: Hermes `config.yaml` browser section
