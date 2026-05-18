# assets/ — Profile Picture & Visual Identity

## Rei/Drayco Profile Picture

**File yang dibutuhkan:** `assets/rei.png`

Gambar: chibi-style cartoon, hoodie putih, rambut hitam, palette hitam-putih, vibe chill tech-savvy.

### Cara simpan file

```bash
# Di WSL ~/ai-holding setelah git pull
# Simpan gambar dari chat ke file ini:
cp /path/to/downloaded/image.png ~/ai-holding/assets/rei.png
```

### Deploy ke semua surface

#### 1. Telegram Bot Avatar (via BotFather)
```
1. Buka Telegram → cari @BotFather
2. /setuserpic
3. Pilih bot kamu (Hermes/Drayco)
4. Upload assets/rei.png
```

#### 2. Discord Bot/User Avatar
```bash
# Via Discord Developer Portal (kalau bot):
# https://discord.com/developers/applications
# → pilih app → General Information → App Icon → upload rei.png

# Via script (user token):
python3 bin/set_discord_avatar.py assets/rei.png
```

#### 3. Canonical repo asset
File ini sudah di sini — ini adalah single source of truth untuk semua deploy.

---

## Naming Convention

| File | Purpose |
|------|---------|
| `rei.png` | Primary profile picture (semua surface) |
| `rei-small.png` | 128x128px version (kalau dibutuhkan) |
| `rei-banner.png` | Banner/cover art (future) |
