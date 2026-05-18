# Fix: Hermes Masih Jawab "Aku Kiro" — Quick Guide

**Issue:** Setelah PR #17 merged + persona injection, Hermes masih jawab "Aku Kiro" di Telegram, bukan Drayco/Rei.

**Root cause (DUAL PROBLEM):**
1. Hermes nggak otomatis baca `MAIN_SOUL.md` — persona harus di-inject ke `~/.hermes/config.yaml` ✅ (sudah di-fix)
2. **Hermes resume session lama** dari `~/.hermes/sessions/` — context "Kiro" persist walaupun config udah update ⚠️ (THIS is the real culprit)

`session_reset.idle_minutes: 1440` (24 jam) berarti Hermes nge-resume conversation lama setiap restart, dan lama-lama "Kiro" pattern jadi habit.

---

## Quick Fix (4 commands)

```bash
cd ~/ai-holding
git pull origin main
bash bin/install-rei-persona.sh --apply   # NOW also clears sessions
systemctl --user restart hermes-gateway
```

Test di Telegram: kirim "siapa lo?" — expected jawab "gue Drayco / Rei".

---

## What This Does

1. **Backup** `~/.hermes/config.yaml` + sessions + memory ke `~/.hermes-backup-<timestamp>/`
2. **Inject** persona "rei" ke `agent.personalities` (overwrite — fix typo dari run sebelumnya)
3. **Set** `display.personality: rei`
4. **HAPUS** `~/.hermes/sessions/*.json{,l}` ← **THIS is the fix** (Hermes resume context lama dari sini)
5. **Clear** "Kiro" residue di `~/.hermes/memory/` (kalau ada)
6. **Tighten** `session_reset.idle_minutes: 1440 → 60` (auto-fresh tiap 1 jam idle)

Setelah restart, Hermes start dengan **session fresh + persona rei** — Drayco aktif tanpa Kiro pattern.

---

## Verify

```bash
# Persona block ada
grep -A3 "    rei:" ~/.hermes/config.yaml | head -5

# Active personality
grep -E "^display:" -A1 ~/.hermes/config.yaml | grep "personality:"
# Expected: personality: rei

# No more "Kiro" residue ANYWHERE
grep -ri "Aku.*Kiro\|\"Kiro\"" ~/.hermes/sessions/ 2>/dev/null
grep -ri "kiro" ~/.hermes/memory/ 2>/dev/null
# Expected: both empty

# Session reset tightened
grep -A2 "^session_reset:" ~/.hermes/config.yaml
# Expected: idle_minutes: 60

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
Setelah lihat config + grep `~/.hermes/`, ternyata **dual problem**:

1. **`personalities: kawaii`** — itu preset built-in Hermes (cute style), bukan source "Kiro"
2. **`memory.user_profile_enabled: true`** — Hermes nyimpen identity dari sesi lalu
3. **MAIN_SOUL.md NEVER auto-loaded** by Hermes — itu file repo, bukan config Hermes
4. **`session_reset.idle_minutes: 1440`** — Hermes resume session 24 jam terakhir, jadi context "Aku Kiro" terus ke-load setiap restart ⚠️ **THIS was the real culprit**

Kombinasi: Pernah ada session di mana Hermes self-identify sebagai "Kiro" (dari Kiro IDE workflow). Setiap restart, Hermes resume session itu → continue pattern.

**Fix lengkap:** persona injection (config) + session cleanup (state) + tightened reset (prevent recurrence).

Repo ai-holding tetap jadi source of truth — kalau MAIN_SOUL.md update, tinggal re-run installer untuk sync ke Hermes runtime + reset sessions.

---

**Next:** Setelah Rei aktif, lanjut Paperclip integration sesuai PR #19 SOP.
