# Discord Setup — User Token (Selfbot via Hermes Gateway)

Versi: 1.0
Created: 2026-05-18
Owner: Main Assistant (Drayco/Rei)
Note: User token method — akun disposable, bukan akun pribadi Fathur

---

## Overview

Hermes punya native Discord support via gateway.
Mode: **user token (selfbot)** — akun Discord disposable yang dipakai sebagai presence Rei di Discord.

**Akun:** Disposable (bukan akun pribadi Fathur)
**Credentials:** `~/.agent/credentials/discord.env`
**Risk:** Discord ToS — mitigasi dengan rate limiting + human-like timing

---

## Setup Akun Discord Disposable

```
1. Buat akun Discord baru (email disposable OK)
   - Username: DraycoxRei atau nama yang kamu mau
   - Avatar: upload assets/rei.png

2. Join server yang diperlukan dengan akun ini

3. Aktifkan 2FA di akun ini (backup code untuk recovery)
```

---

## Dapat User Token

```
1. Buka Discord di browser (bukan app)
2. Login dengan akun disposable tadi
3. Buka Developer Tools (F12)
4. Tab Network → Filter: "api"
5. Kirim pesan atau reload page
6. Cari request ke discord.com/api/v*/users/@me
7. Header "authorization" = user token kamu

Atau via Console (lebih cepat):
  (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m)
  .find(m=>m?.exports?.default?.getToken!==void 0)
  .exports.default.getToken()
```

```bash
# Simpan token
echo 'DISCORD_TOKEN=your_token_here' > ~/.agent/credentials/discord.env
chmod 600 ~/.agent/credentials/discord.env
```

---

## Konfigurasi Hermes

### config.yaml

```yaml
discord:
  require_mention: false      # Rei aktif di semua pesan (bukan cuma saat di-mention)
  auto_thread: true           # Auto buat thread untuk percakapan panjang
  reactions: true             # Boleh react ke pesan
  channel_prompts: {}         # System prompt per channel (isi kalau perlu)
  allowed_channels: ""        # Kosong = semua channel yang bot join
```

### Environment variable

```bash
# Load credentials sebelum jalankan Hermes gateway
source ~/.agent/credentials/discord.env
export DISCORD_TOKEN

# Jalankan Hermes gateway
hermes gateway
```

---

## Jalankan

```bash
# Single run
source ~/.agent/credentials/discord.env && hermes gateway

# Dengan PM2 (agar tetap jalan di background)
pm2 start "hermes gateway" --name rei-gateway
pm2 save
pm2 startup

# Cek status
pm2 status
pm2 logs rei-gateway
```

---

## Operasi yang Tersedia

### Messaging
```
- Receive & respond pesan di channel
- Kirim pesan ke channel / DM
- Edit pesan sendiri
- Delete pesan sendiri
- React dengan emoji
```

### Channel Management
```
- Baca channel history
- Create thread
- Join/leave voice channel (listen only)
```

### Server Operations
```
- Lihat member list
- Search message history
- Baca server info
```

---

## Behavior di SOUL

```
Discord:
  Status akun:   milik agent (Drayco/Rei) — disposable
  Credential:    ~/.agent/credentials/discord.env
  Kemampuan:     receive/send pesan, react, buat thread, baca history, search
  Batas:         @everyone / @here (wajib konfirmasi)
                 mass DM ke banyak user (wajib konfirmasi)
                 kick/ban member (wajib konfirmasi Fathur)
                 posting ke channel publik yang berdampak reputasi (wajib konfirmasi)
```

---

## Rate Limiting & Anti-Detection

Untuk mengurangi risk ban pada selfbot:

```python
# Pattern yang aman
import time, random

def safe_send(channel, message):
    # Random delay 1-3 detik antar pesan
    time.sleep(random.uniform(1, 3))
    channel.send(message)

# Jangan:
# - Kirim pesan berturut-turut tanpa delay
# - Join/leave server terlalu cepat
# - Flood channel dengan banyak pesan dalam waktu singkat
```

Hermes sudah punya rate limiting bawaan — tapi tetap perlu dikonfigurasikan wajar.

---

## Recovery kalau Akun Ter-ban

```
1. Buat akun Discord baru (email baru)
2. Dapatkan token baru (ikuti langkah di atas)
3. Update ~/.agent/credentials/discord.env
4. Restart hermes gateway
5. Update avatar dengan assets/rei.png
```

---

## Verify Setup

```bash
# Cek token valid
curl -H "Authorization: your_token" https://discord.com/api/v10/users/@me

# Harusnya return JSON dengan info user
# {"id":"...","username":"DraycoxRei",...}

# Cek Hermes gateway connect
hermes gateway --verbose
# Harusnya ada log: "Discord connected as DraycoxRei#XXXX"
```

---

## Reference

- Hermes Discord config: `~/.hermes/config.yaml` (discord section)
- Credentials: `~/.agent/credentials/discord.env`
- Template: `credentials/templates/discord.env.example`
- Profile picture: `assets/rei.png`
