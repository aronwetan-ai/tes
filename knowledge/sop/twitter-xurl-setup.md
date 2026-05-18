# Twitter / X Setup — xurl CLI

Versi: 1.0
Created: 2026-05-18
Owner: @brandflow.social, @brandflow.community, @crypto.research
Source: Hermes bundled skill social-media/xurl (xdevplatform/xurl)

---

## Overview

**xurl** adalah official X Developer Platform CLI untuk API v2.
Sudah bundled di Hermes — Hermes auto-load skill ini saat task terkait X/Twitter.

**Akun:** Shared (satu akun untuk semua agents)
**Credentials:** `~/.agent/credentials/twitter.env`
**Status:** Otonom penuh (sesuai UPGRADE2 Section 3)
**Boundary #4:** Public posting yang berdampak reputasi → konfirmasi Fathur dulu

---

## Install xurl

```bash
# Via npm (official)
npm install -g @xdevplatform/xurl

# Verify
xurl --version
```

---

## Authentication

### Method 1: Cookie-based (Primary — paling stabil)

Login manual 1x di browser, export cookies:

```bash
# Di browser yang sudah login ke X:
# Developer Tools → Application → Cookies → twitter.com
# Export sebagai JSON atau Netscape format

# Simpan ke:
cp exported-cookies.json ~/.agent/credentials/x-cookies.json
chmod 600 ~/.agent/credentials/x-cookies.json

# Set di environment:
export X_COOKIES_PATH=~/.agent/credentials/x-cookies.json
```

### Method 2: OAuth via xurl (Fallback)

```bash
# Interactive login (jalankan sekali)
xurl auth login

# Credentials tersimpan di ~/.xurl/config.json
# Atau set manual via env vars dari credentials file:
source ~/.agent/credentials/twitter.env
xurl config set bearer-token $X_BEARER_TOKEN
```

---

## Cara Pakai — Common Operations

### Posting

```bash
# Post tweet biasa
xurl tweet create --text "konten tweet di sini"

# Post dengan media
xurl tweet create --text "caption" --media-ids $(xurl media upload image.png | jq -r '.media_id_string')

# Reply ke tweet
xurl tweet create --text "reply" --reply-to TWEET_ID

# Quote tweet
xurl tweet create --text "komentar" --quote-tweet-id TWEET_ID
```

### Searching & Research

```bash
# Search recent tweets
xurl tweet search recent --query "bitcoin" --max-results 10

# Search dengan filter
xurl tweet search recent --query "BTC -is:retweet lang:id" --max-results 20

# Get user timeline
xurl tweet timelines home --max-results 10
```

### Engagement

```bash
# Like tweet
xurl tweet like --tweet-id TWEET_ID

# Retweet
xurl tweet retweet --tweet-id TWEET_ID

# Follow user
xurl user follow --target-user-id USER_ID

# Unfollow
xurl user unfollow --target-user-id USER_ID
```

### DM

```bash
# Kirim DM
xurl dm create --participant-id USER_ID --text "pesan"

# Lihat DM conversations
xurl dm events list
```

---

## Per-Agent Access Control

| Agent | Access Level | Otonom | Butuh Konfirmasi |
|-------|-------------|--------|-----------------|
| `@brandflow.social` | Full | Post rutin, like, RT, follow | Post viral/kontroversial, ubah bio |
| `@brandflow.community` | Full | Reply, engage, DM | Mass unfollow, hapus tweet engagement tinggi |
| `@crypto.research` | Read-only | Search, scrape sentiment | Apapun yang write |
| `Drayco/Rei` | Read-only | Research, monitoring | — |

---

## Behavior di SOUL (Template)

Sesuai UPGRADE2 credential-management, tambahkan ini ke SOUL agent yang butuh Twitter:

```
Twitter / X:
  Status akun:   shared (milik agent kolektif)
  Credential:    ~/.agent/credentials/twitter.env
  Kemampuan:     posting, reply, like, retweet, follow, search, DM, media upload
  Batas:         hapus tweet dengan engagement tinggi (wajib konfirmasi)
                 ubah profile bio/photo (wajib konfirmasi Fathur)
                 posting finansial claim / kontroversi (wajib konfirmasi Fathur)
```

---

## Rate Limits (API v2 Free Tier)

| Endpoint | Limit |
|----------|-------|
| Tweet (POST) | 17/24h per app + 100/24h per user |
| Search (GET) | 500k tweets/month |
| DM | 1000/24h |
| Media upload | 5/min |

**Mitigasi:** Jangan burst posting. Spread over time. Monitor `x-rate-limit-remaining` header.

---

## Verify Setup

```bash
# Cek auth
xurl user lookup me

# Test tweet (draft, bukan kirim)
xurl tweet create --text "test" --dry-run  # kalau ada flag ini

# Atau test dengan search (read-only, aman)
xurl tweet search recent --query "hello" --max-results 1
```

---

## Reference

- xurl GitHub: https://github.com/xdevplatform/xurl
- Hermes bundled skill: `skills/social-media/xurl`
- X API v2 docs: https://developer.x.com/en/docs/x-api
- Credentials: `~/.agent/credentials/twitter.env`
- Template: `credentials/templates/twitter.env.example`
