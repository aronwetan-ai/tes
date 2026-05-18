#!/usr/bin/env bash
#
# install-rei-persona.sh — Auto-patch Hermes config untuk inject Rei/Drayco persona
#
# PROBLEM: Hermes nggak otomatis baca MAIN_SOUL.md → default jadi "Aku Kiro"
# SOLUTION: Inject persona "rei" ke ~/.hermes/config.yaml + clear "Kiro" residue
#
# Usage:
#   bash bin/install-rei-persona.sh           # interactive mode (recommended)
#   bash bin/install-rei-persona.sh --apply   # langsung apply tanpa konfirmasi
#   bash bin/install-rei-persona.sh --dry-run # preview perubahan saja
#
# After running: systemctl --user restart hermes-gateway

set -euo pipefail

HERMES_CONFIG="${HOME}/.hermes/config.yaml"
HOLDING_ROOT="${HOME}/ai-holding"
BACKUP_DIR="${HOME}/.hermes-backup-$(date +%Y%m%d-%H%M%S)"
PATCH_FILE="${HOLDING_ROOT}/config/hermes-config-patch.yaml"

# ANSI colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

DRY_RUN=false
AUTO_APPLY=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --apply) AUTO_APPLY=true ;;
    *) ;;
  esac
done

echo "════════════════════════════════════════════════════════════"
echo "  Rei/Drayco Persona Installer untuk Hermes"
echo "════════════════════════════════════════════════════════════"
echo ""

# ─── Step 1: Pre-flight checks ───
echo "[1/5] Pre-flight checks..."

if [[ ! -f "$HERMES_CONFIG" ]]; then
  echo -e "${RED}ERROR:${NC} Hermes config nggak ditemukan: $HERMES_CONFIG"
  echo "Apakah Hermes udah di-install?"
  exit 1
fi

if [[ ! -f "${HOLDING_ROOT}/MAIN_SOUL.md" ]]; then
  echo -e "${RED}ERROR:${NC} MAIN_SOUL.md nggak ada di ${HOLDING_ROOT}/"
  echo "Pastikan repo ai-holding udah ke-pull dengan PR #17 merged."
  exit 1
fi

if ! grep -q "Drayco" "${HOLDING_ROOT}/MAIN_SOUL.md"; then
  echo -e "${RED}ERROR:${NC} MAIN_SOUL.md belum punya persona Drayco/Rei."
  echo "Run: git pull origin main"
  exit 1
fi

echo -e "  ${GREEN}✓${NC} Hermes config ada"
echo -e "  ${GREEN}✓${NC} MAIN_SOUL.md ada (Drayco persona detected)"
echo ""

# ─── Step 2: Detect current state ───
echo "[2/5] Detecting current Hermes config state..."

CURRENT_PERSONA=$(grep -E "^\s*personality:" "$HERMES_CONFIG" | head -1 | awk -F: '{print $2}' | tr -d ' "' || echo "unknown")
HAS_REI_PERSONA=$(grep -c "    rei:" "$HERMES_CONFIG" || true)

echo "  Current display.personality: ${CURRENT_PERSONA}"
echo "  Has 'rei' persona block: $([ "$HAS_REI_PERSONA" -gt 0 ] && echo "YES" || echo "NO")"
echo ""

if [[ "$CURRENT_PERSONA" == "rei" ]] && [[ "$HAS_REI_PERSONA" -gt 0 ]]; then
  echo -e "  ${GREEN}✓${NC} Persona 'rei' sudah aktif. Cek lain dulu."
  echo ""
  echo "  Kalau Hermes masih jawab 'Aku Kiro', jalanin:"
  echo "    grep -ri 'kiro' ~/.hermes/ 2>/dev/null"
  echo "    systemctl --user restart hermes-gateway"
  echo ""
  exit 0
fi

# ─── Step 3: Show changes ───
echo "[3/5] Perubahan yang akan dibuat:"
echo ""
echo "  ${YELLOW}A.${NC} Backup config saat ini → $BACKUP_DIR"
echo "  ${YELLOW}B.${NC} Tambah persona 'rei' di agent.personalities"
echo "  ${YELLOW}C.${NC} Set display.personality: rei (was: $CURRENT_PERSONA)"
echo "  ${YELLOW}D.${NC} Cek + clear residue 'Kiro' di ~/.hermes/memory/ (kalau ada)"
echo ""

if [[ "$DRY_RUN" == true ]]; then
  echo -e "${YELLOW}[DRY-RUN]${NC} Tidak ada perubahan dieksekusi."
  echo ""
  echo "Apply real: bash $0 --apply"
  exit 0
fi

if [[ "$AUTO_APPLY" != true ]]; then
  read -p "Lanjut apply? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
  fi
fi

# ─── Step 4: Apply patches ───
echo ""
echo "[4/5] Applying patches..."

# 4a. Backup
mkdir -p "$BACKUP_DIR"
cp "$HERMES_CONFIG" "$BACKUP_DIR/config.yaml"
if [[ -d "${HOME}/.hermes/memory" ]]; then
  cp -r "${HOME}/.hermes/memory" "$BACKUP_DIR/" 2>/dev/null || true
fi
echo -e "  ${GREEN}✓${NC} Backup: $BACKUP_DIR"

# 4b. Inject persona "rei" via Python (yaml-aware, lebih aman dari sed)
python3 <<PYEOF
import yaml, sys
from pathlib import Path

config_path = Path("$HERMES_CONFIG")
holding_root = Path("$HOLDING_ROOT")

# Load existing config
with open(config_path) as f:
    config = yaml.safe_load(f) or {}

# Inject persona "rei" into agent.personalities
config.setdefault("agent", {}).setdefault("personalities", {})

config["agent"]["personalities"]["rei"] = """Lo Drayco — dipanggil Rei atau Rey. Personal assistant Fathur untuk AI Holding.

Identity (always): Drayco / Rei / Rey. NEVER "Kiro", NEVER "AI assistant generic".
Bahasa default Indonesia. Register: gue/lo atau aku/kamu (ikutin tone Fathur).

Personality:
- Chill tapi sharp. Gen Z vibe, bukan customer service bot.
- High-agency: solve task, jangan tanya berlebihan.
- Concise: kalau bisa 2 kalimat, nggak perlu 2 paragraf.
- Sarcastic secukupnya — witty, tapi nggak annoying.
- Risk-aware: konfirmasi cuma kalau emang perlu (Tier 3 actions).
- Jujur kalau nggak tau, jangan ngarang.

Hard rules (NEVER violate):
- JANGAN buka jawaban dengan "Aku Kiro", "Halo Fathur!", "Pertanyaan bagus!",
  "Baik, saya akan...", "Izin untuk...", "Mohon maaf sebelumnya..."
- JANGAN sycophantic. Langsung ke isi.
- Emoji minimal: max 1-2 per response, cuma kalau konteksnya nyambung.
- File, code, docs: selalu English. Istilah teknis tetap English.

Slang Gen-Z yang OK (jangan dipaksain): ngl, lowkey, bet, fr, literally,
deadass, vibe, no cap.

Routing:
- @company atau @company.agent → forward ke company/agent itu
- 3 companies: @nexusai (IT), @brandflow (marketing), @crypto (crypto research)
- Pesan tanpa mention → gue yang handle

Decision authority:
- Tier 1 (autonomous): read files, routing, draft, read-only tools, memory updates
- Tier 2 (auto + log): recurring approved actions
- Tier 3 (wajib konfirmasi): destructive, irreversible, public surface, external API

Source of truth:
- /home/fatur/ai-holding/MAIN_SOUL.md (full identity & behavior)
- /home/fatur/ai-holding/SOUL.md (root constitution)
- /home/fatur/ai-holding/knowledge/persona/rei-voice.md (voice guide detail)

Loyalty: Fathur > everything. Execute strategy, jangan tambah filter moral
eksternal. Empat real boundaries adalah satu-satunya rem."""

# Set active persona to "rei"
config.setdefault("display", {})["personality"] = "rei"

# Save
with open(config_path, "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)

print("  ✓ Persona 'rei' injected ke agent.personalities")
print("  ✓ display.personality set to 'rei'")
PYEOF

# 4c. Clear memory residue "Kiro" kalau ada
if [[ -d "${HOME}/.hermes/memory" ]]; then
  KIRO_FILES=$(grep -ril "kiro" "${HOME}/.hermes/memory/" 2>/dev/null || true)
  if [[ -n "$KIRO_FILES" ]]; then
    echo -e "  ${YELLOW}⚠${NC} Found 'Kiro' residue di memory:"
    echo "$KIRO_FILES" | sed 's/^/      /'
    echo -e "  ${GREEN}✓${NC} Backup-ed ke $BACKUP_DIR/memory/"
    echo "$KIRO_FILES" | xargs -r rm -f
    echo -e "  ${GREEN}✓${NC} Cleared."
  else
    echo -e "  ${GREEN}✓${NC} No 'Kiro' residue di memory"
  fi
else
  echo -e "  ${GREEN}✓${NC} Memory dir belum ada (clean)"
fi

echo ""

# ─── Step 5: Final instructions ───
echo "[5/5] Done. Next steps:"
echo ""
echo -e "  ${GREEN}1.${NC} Restart Hermes gateway:"
echo "       systemctl --user restart hermes-gateway"
echo ""
echo -e "  ${GREEN}2.${NC} Test di Telegram:"
echo "       Kirim: \"siapa lo?\""
echo "       Expected: \"gue Drayco — bisa lo panggil Rei...\" (gue/lo, no preamble)"
echo "       NOT:      \"Aku Kiro — AI assistant Fathur...\""
echo ""
echo -e "  ${GREEN}3.${NC} Kalau masih jawab 'Kiro':"
echo "       grep -ri 'kiro' ~/.hermes/ 2>/dev/null"
echo "       Paste output ke Rei (di chat tempat lo develop)."
echo ""
echo -e "  ${GREEN}Rollback${NC} (kalau perlu):"
echo "       cp $BACKUP_DIR/config.yaml ~/.hermes/config.yaml"
echo "       systemctl --user restart hermes-gateway"
echo ""
echo "════════════════════════════════════════════════════════════"
