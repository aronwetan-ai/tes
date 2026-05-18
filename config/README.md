# config/ — Hermes & Tooling Configuration

Folder ini berisi config patches yang harus di-apply ke runtime tools (Hermes, dll).
File-file di sini **bukan** auto-loaded — harus di-apply manual atau via installer script.

## Files

### `hermes-config-patch.yaml`

Patch untuk `~/.hermes/config.yaml` — inject persona "rei" (Drayco) + clear "Kiro" residue.

**Why:** Hermes nggak otomatis baca `MAIN_SOUL.md`. Tanpa patch ini, Hermes default ke identity generic (sering muncul sebagai "Aku Kiro").

**How to apply:**

```bash
# Option A: Auto-installer (recommended)
bash bin/install-rei-persona.sh --apply

# Option B: Manual edit
nano ~/.hermes/config.yaml
# Copy content dari hermes-config-patch.yaml ke spot yang sesuai

# Then restart:
systemctl --user restart hermes-gateway
```

**Verify:**
- Test di Telegram: "siapa lo?" → harus jawab "gue Drayco / Rei", bukan "Aku Kiro"

**Detail SOP:** `knowledge/sop/hermes-persona-binding.md`

---

## Why Config Patches Exist

Repo `~/ai-holding/` adalah **knowledge base**, bukan **runtime config**. Hermes
runtime hidup di `~/.hermes/` dan punya config sendiri.

Untuk menjembatani: kalau ada perubahan di MAIN_SOUL.md yang harus tercermin di
runtime Hermes, kita siapkan patch di `config/` yang bisa di-apply ke Hermes.

Pattern ini berlaku juga untuk tooling lain di masa depan (Paperclip, dll).
