# Hermes Persona Binding — How SOUL.md Reaches Hermes

Versi: 1.0
Created: 2026-05-18
Owner: Operator + NexusAI DevOps
Trigger: Kalau Hermes jawab dengan persona yang salah (mis. "Aku Kiro" padahal MAIN_SOUL.md sudah Drayco/Rei)

---

## Problem Statement

Repo `~/ai-holding/` punya hierarchy SOUL:
```
SOUL.md (Tier 0)         — Root constitution
MAIN_SOUL.md (Tier 1)    — Drayco/Rei persona + behavior
companies/*/SOUL.md      — Company persona (Tier 2)
companies/*/agents/*.md  — Agent persona (Tier 3)
```

**Tapi Hermes TIDAK otomatis baca file-file ini.** Hermes hanya baca:

1. `~/.hermes/config.yaml` — primary config
2. `~/.hermes/memory/` — persistent memory (kalau enabled)
3. `~/.hermes/skills/` — skill files
4. System prompt yang di-set via `agent.personalities` di config.yaml

**Akibat:** Walaupun MAIN_SOUL.md sudah berisi persona "Drayco/Rei", Hermes tetap pakai default identity (sering muncul sebagai "Aku Kiro" — name dari Kiro IDE/CLI).

---

## Root Cause

Hermes adalah **agent runtime** — dia eksekusi instruksi yang masuk ke context-nya. Hermes nggak punya konsep "load semua markdown di workspace" secara default.

Repo `ai-holding` adalah **knowledge base + state**, bukan **system prompt source**. SOUL.md dibaca **on-demand** kalau ada tool call yang explicit baca file itu — bukan sebagai default behavior.

---

## Solution: Inject Persona via Hermes Personalities

Hermes punya feature `agent.personalities` di config.yaml — ini adalah cara resmi untuk set system prompt.

**Strategy:** Buat persona "rei" yang:
1. Berisi summary persona (Identity, Personality, Hard rules)
2. Reference path absolut ke MAIN_SOUL.md + rei-voice.md sebagai source of truth (untuk detail-detail yang mungkin perlu Hermes baca on-demand)
3. Set sebagai `display.personality: rei`

---

## Step-by-Step

### Step 1: Verify Repo Up-to-Date

```bash
cd ~/ai-holding
git pull origin main
grep -l "Drayco" MAIN_SOUL.md  # harus return MAIN_SOUL.md
```

### Step 2: Run Auto-Installer

```bash
# Dry-run dulu (preview perubahan)
bash bin/install-rei-persona.sh --dry-run

# Apply
bash bin/install-rei-persona.sh --apply
```

Script ini:
- Backup `~/.hermes/config.yaml` ke `~/.hermes-backup-<timestamp>/`
- Inject persona "rei" ke `agent.personalities` (via Python YAML — aman, nggak rusak struktur)
- Set `display.personality: rei`
- Cek + clear residue "Kiro" di `~/.hermes/memory/` (kalau ada)

### Step 3: Restart Hermes

```bash
systemctl --user restart hermes-gateway
```

### Step 4: Verify

Kirim ke Telegram:
```
"siapa lo?"
```

Expected:
```
gue Drayco — bisa lo panggil Rei. personal assistant lo buat AI Holding...
(gue/lo register, no preamble, minimal emoji)
```

NOT:
```
Aku Kiro — AI assistant Fathur...
```

---

## Manual Patching (kalau script gagal)

Edit `~/.hermes/config.yaml`:

### A. Tambah persona "rei" di `agent.personalities`

```yaml
agent:
  personalities:
    helpful: ...    # biarin existing
    concise: ...    # biarin existing
    # ... (preset lain biarin)
    rei: |
      Lo Drayco — dipanggil Rei atau Rey. Personal assistant Fathur untuk AI Holding.
      [paste full persona dari config/hermes-config-patch.yaml]
```

### B. Set active persona

```yaml
display:
  personality: rei   # was: kawaii
```

### C. (Optional) Clear memory residue

```bash
ls ~/.hermes/memory/
grep -ri "kiro" ~/.hermes/memory/

# Kalau ada:
cp -r ~/.hermes/memory ~/.hermes-backup/
rm -f ~/.hermes/memory/user_profile.*
```

---

## Why Memory Residue Matters

Hermes punya `memory.user_profile_enabled: true` (default). Profile ini terbentuk dari interaksi sebelumnya — termasuk pas Hermes masih self-identify sebagai "Kiro".

Saat persona di-update, **memory tetap nyimpen identity lama**. Inilah kenapa:
- `display.personality: kawaii` muncul bareng "Aku Kiro" (bukan kawaii style) — karena memory override personality dengan identity lama.

**Solusi:** Hapus profile yang nyimpen identity "Kiro", biar Hermes rebuild dengan persona baru.

---

## Why This Workaround Exists

Ideally, Hermes punya feature `--system-prompt-file MAIN_SOUL.md` atau auto-load workspace SOUL files. Tapi current Hermes **belum** punya itu.

**Workaround:** `agent.personalities` adalah satu-satunya supported way untuk inject custom system prompt. Persona "rei" jadi pointer ke MAIN_SOUL.md.

**Future:** Kalau Hermes ada feature `workspace_soul_path`, kita bisa migrate ke approach yang lebih clean. Untuk sekarang, persona injection via config = solusi resmi.

---

## Verification Checklist

Setelah apply patch:

```bash
# 1. Persona block ada
grep -A5 "    rei:" ~/.hermes/config.yaml | head -10

# 2. Active personality "rei"
grep -A1 "^display:" ~/.hermes/config.yaml | grep "personality:"

# 3. No more "Kiro" di memory
grep -ri "kiro" ~/.hermes/memory/ 2>/dev/null

# 4. Service running
systemctl --user status hermes-gateway

# 5. Test in Telegram
# → "siapa lo?" → harus jawab Drayco/Rei
```

---

## Rollback

```bash
# Restore config dari backup
ls ~/.hermes-backup-*/
LATEST_BACKUP=$(ls -dt ~/.hermes-backup-* | head -1)
cp "$LATEST_BACKUP/config.yaml" ~/.hermes/config.yaml

# Restart
systemctl --user restart hermes-gateway
```

---

## Maintenance

Kalau MAIN_SOUL.md di-update major (perubahan persona, new behavior rules):

1. Update `config/hermes-config-patch.yaml` di repo
2. Re-run `bash bin/install-rei-persona.sh --apply` di mesin
3. Restart Hermes gateway

Atau lebih ringan: edit langsung `~/.hermes/config.yaml` bagian `agent.personalities.rei` lalu restart.

---

## Related Files

- `MAIN_SOUL.md` — full identity Drayco/Rei (source of truth)
- `knowledge/persona/rei-voice.md` — voice guide detail (slang, sarcasm calibration)
- `config/hermes-config-patch.yaml` — config patch reference
- `bin/install-rei-persona.sh` — auto-installer script
- `knowledge/reference/hermes-config.md` — full Hermes config reference
