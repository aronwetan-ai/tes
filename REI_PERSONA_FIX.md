# Fix: Hermes Masih Jawab "Aku Kiro" — Quick Guide

**Issue:** Setelah PR #17 merged, Hermes masih jawab "Aku Kiro" di Telegram, bukan Drayco/Rei.

**Root cause:** Hermes nggak otomatis baca `MAIN_SOUL.md`. Persona harus di-inject ke `~/.hermes/config.yaml`.

---

## Quick Fix (3 commands)

```bash
cd ~/ai-holding
git pull origin main
bash bin/install-rei-persona.sh --apply
systemctl --user restart hermes-gateway
```

Test di Telegram: kirim "siapa lo?" — expected jawab "gue Drayco / Rei".

---

## What This Does

1. **Backup** `~/.hermes/config.yaml` ke `~/.hermes-backup-<timestamp>/`
2. **Inject** persona "rei" ke `agent.personalities` (Drayco identity + behavior rules)
3. **Set** `display.personality: rei` (was: kawaii)
4. **Clear** "Kiro" residue di `~/.hermes/memory/` (kalau ada)

Setelah restart, Hermes load persona "rei" sebagai system prompt — Drayco aktif.

---

## Verify

```bash
# Persona block ada
grep -A3 "    rei:" ~/.hermes/config.yaml | head -5

# Active personality
grep -E "^display:" -A1 ~/.hermes/config.yaml | grep "personality:"
# Expected: personality: rei

# No more "Kiro" residue
grep -ri "kiro" ~/.hermes/memory/ 2>/dev/null
# Expected: empty

# Service running
systemctl --user status hermes-gateway --no-pager | head -5
```

---

## If Still Broken

```bash
# Cek "Kiro" residue di seluruh ~/.hermes
grep -ri "kiro" ~/.hermes/ 2>/dev/null | grep -v "config.yaml.bak" | head -20

# Cek skills custom yang mungkin override
ls -la ~/.hermes/skills/ 2>/dev/null
ls -la ~/.hermes/sessions/ 2>/dev/null

# Paste output ke chat tempat lo develop
```

---

## Rollback

```bash
LATEST=$(ls -dt ~/.hermes-backup-* 2>/dev/null | head -1)
[ -n "$LATEST" ] && cp "$LATEST/config.yaml" ~/.hermes/config.yaml
systemctl --user restart hermes-gateway
```

---

## Detail Lengkap

- **SOP:** `knowledge/sop/hermes-persona-binding.md`
- **Config patch:** `config/hermes-config-patch.yaml`
- **Installer:** `bin/install-rei-persona.sh`
- **Persona source:** `MAIN_SOUL.md`, `knowledge/persona/rei-voice.md`

---

## Why This Happened

Awalnya gue asumsi `display.personality: kawaii` di Hermes config jadi penyebab.
Setelah lihat config lengkap lo, ternyata:

1. **`personalities: kawaii`** — itu preset built-in Hermes (cute style), bukan source "Kiro"
2. **`memory.user_profile_enabled: true`** — Hermes nyimpen identity dari sesi lalu
3. **MAIN_SOUL.md NEVER auto-loaded** by Hermes — itu file repo, bukan config Hermes

Hermes butuh persona di-inject lewat `agent.personalities` (built-in feature), lalu
`display.personality` set ke nama persona itu. Itu cara resmi inject custom system prompt.

Repo ai-holding tetap jadi source of truth — kalau MAIN_SOUL.md update, tinggal re-run
installer untuk sync ke Hermes runtime.

---

**Next:** Setelah Rei aktif, lanjut Paperclip integration sesuai PR #19 SOP.
