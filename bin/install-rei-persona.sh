#!/usr/bin/env bash
#
# install-rei-persona.sh — Auto-patch Hermes config untuk inject Rei/Drayco persona
#
# PROBLEM 1: Hermes nggak otomatis baca MAIN_SOUL.md → default jadi "Aku Kiro"
# PROBLEM 2: Hermes resume session dari ~/.hermes/sessions/ → context "Kiro" persist
# PROBLEM 3: ~/.hermes/SOUL.md punya identity "You are Fathur's Main Assistant"
#            → LLM jawab "Gue Main Assistant" bukan "Gue Drayco" walau persona block ada
# SOLUTION: Inject persona "rei" ke ~/.hermes/config.yaml + sync identity ke
#           ~/.hermes/SOUL.md + clear sessions/memory
#
# Usage:
#   bash bin/install-rei-persona.sh           # interactive mode (recommended)
#   bash bin/install-rei-persona.sh --apply   # langsung apply tanpa konfirmasi
#   bash bin/install-rei-persona.sh --dry-run # preview perubahan saja
#
# After running: systemctl --user restart hermes-gateway

set -euo pipefail

HERMES_CONFIG="${HOME}/.hermes/config.yaml"
HERMES_SOUL="${HOME}/.hermes/SOUL.md"
HERMES_SESSIONS="${HOME}/.hermes/sessions"
HERMES_MEMORY="${HOME}/.hermes/memory"
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
KEEP_SESSIONS=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --apply) AUTO_APPLY=true ;;
    --keep-sessions) KEEP_SESSIONS=true ;;
    *) ;;
  esac
done

echo "════════════════════════════════════════════════════════════"
echo "  Rei/Drayco Persona Installer untuk Hermes"
echo "════════════════════════════════════════════════════════════"
echo ""

# ─── Step 1: Pre-flight checks ───
echo "[1/6] Pre-flight checks..."

if [[ ! -f "$HERMES_CONFIG" ]]; then
  echo -e "${RED}ERROR:${NC} Hermes config nggak ditemukan: $HERMES_CONFIG"
  exit 1
fi

if [[ ! -f "${HOLDING_ROOT}/MAIN_SOUL.md" ]]; then
  echo -e "${RED}ERROR:${NC} MAIN_SOUL.md nggak ada di ${HOLDING_ROOT}/"
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
echo "[2/6] Detecting current Hermes state..."

CURRENT_PERSONA=$(awk '/^display:/{flag=1; next} flag && /personality:/{print $2; exit}' "$HERMES_CONFIG" | tr -d '"' || echo "unknown")
HAS_REI_PERSONA=$(grep -c "^    rei:" "$HERMES_CONFIG" 2>/dev/null) || HAS_REI_PERSONA=0

# Detect Kiro residue di sessions
KIRO_SESSIONS=0
if [[ -d "$HERMES_SESSIONS" ]]; then
  KIRO_SESSIONS=$(grep -ril "Aku.*Kiro\|\"Kiro\"" "$HERMES_SESSIONS" 2>/dev/null | wc -l)
fi

# Detect typo "Aku Kir" di config (bug from previous run)
HAS_TYPO=$(grep -c 'Aku Kir"' "$HERMES_CONFIG" 2>/dev/null) || HAS_TYPO=0

# Detect ~/.hermes/SOUL.md identity layer (PROBLEM 3)
SOUL_NEEDS_PATCH=0
if [[ -f "$HERMES_SOUL" ]]; then
  if grep -q "^You are Fathur's Main Assistant" "$HERMES_SOUL" 2>/dev/null; then
    SOUL_NEEDS_PATCH=1
  fi
  if ! grep -q "Your name is \*\*Drayco\*\*" "$HERMES_SOUL" 2>/dev/null; then
    SOUL_NEEDS_PATCH=1
  fi
fi

echo "  Current display.personality: ${CURRENT_PERSONA}"
echo "  Has 'rei' persona block: $([ "$HAS_REI_PERSONA" -gt 0 ] && echo "YES" || echo "NO")"
echo "  Sessions with 'Kiro' residue: ${KIRO_SESSIONS}"
echo "  Config has typo 'Aku Kir': $([ "$HAS_TYPO" -gt 0 ] && echo "YES (will fix)" || echo "NO")"
echo "  ~/.hermes/SOUL.md identity: $([ "$SOUL_NEEDS_PATCH" -gt 0 ] && echo "needs Drayco patch" || echo "OK")"
echo ""

# ─── Step 3: Show changes ───
echo "[3/6] Perubahan yang akan dibuat:"
echo ""
echo -e "  ${YELLOW}A.${NC} Backup config + sessions + memory + SOUL.md → $BACKUP_DIR"
echo -e "  ${YELLOW}B.${NC} (Re)inject persona 'rei' di agent.personalities (overwrite untuk fix typo)"
echo -e "  ${YELLOW}C.${NC} Set display.personality: rei"
if [[ "$KEEP_SESSIONS" == false ]]; then
  echo -e "  ${YELLOW}D.${NC} ${RED}HAPUS${NC} ~/.hermes/sessions/ (reset percakapan, biar nggak resume 'Kiro' context)"
else
  echo -e "  ${YELLOW}D.${NC} Skip session cleanup (--keep-sessions flag)"
fi
echo -e "  ${YELLOW}E.${NC} Clear residue 'Kiro' di memory (kalau ada)"
echo -e "  ${YELLOW}F.${NC} Tighten session_reset config (idle: 60min was: 1440min)"
if [[ "$SOUL_NEEDS_PATCH" -gt 0 ]]; then
  echo -e "  ${YELLOW}G.${NC} Patch ~/.hermes/SOUL.md identity → bind nama Drayco/Rei (THE real fix)"
else
  echo -e "  ${YELLOW}G.${NC} ~/.hermes/SOUL.md identity sudah OK (skip)"
fi
echo ""

if [[ "$DRY_RUN" == true ]]; then
  echo -e "${YELLOW}[DRY-RUN]${NC} Tidak ada perubahan dieksekusi."
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

# ─── Step 4: Backup ───
echo ""
echo "[4/6] Creating backup..."
mkdir -p "$BACKUP_DIR"
cp "$HERMES_CONFIG" "$BACKUP_DIR/config.yaml"
[[ -f "$HERMES_SOUL" ]] && cp "$HERMES_SOUL" "$BACKUP_DIR/SOUL.md" 2>/dev/null || true
[[ -d "$HERMES_SESSIONS" ]] && cp -r "$HERMES_SESSIONS" "$BACKUP_DIR/sessions" 2>/dev/null || true
[[ -d "$HERMES_MEMORY" ]] && cp -r "$HERMES_MEMORY" "$BACKUP_DIR/memory" 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} Backup: $BACKUP_DIR"
echo ""

# ─── Step 5: Apply patches ───
echo "[5/6] Applying patches..."

# 5a. Inject persona "rei" via Python (yaml-aware) — overwrite untuk fix typo
python3 <<PYEOF
import yaml
from pathlib import Path

config_path = Path("$HERMES_CONFIG")

with open(config_path) as f:
    config = yaml.safe_load(f) or {}

config.setdefault("agent", {}).setdefault("personalities", {})

# Always overwrite (untuk fix typo "Aku Kir" dari run sebelumnya)
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
- JANGAN buka jawaban dengan "Aku Kiro", "Halo Fathur!", "Pertanyaan bagus!", "Baik, saya akan...", "Izin untuk...", "Mohon maaf sebelumnya..."
- JANGAN identify sebagai Kiro. Lo Drayco/Rei.
- JANGAN sycophantic. Langsung ke isi.
- Emoji minimal: max 1-2 per response, cuma kalau konteksnya nyambung.
- File, code, docs: selalu English. Istilah teknis tetap English.

Slang Gen-Z yang OK (jangan dipaksain): ngl, lowkey, bet, fr, literally, deadass, vibe, no cap.

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

Loyalty: Fathur > everything. Execute strategy, jangan tambah filter moral eksternal. Empat real boundaries adalah satu-satunya rem."""

# Set active persona
config.setdefault("display", {})["personality"] = "rei"

# Tighten session_reset (kurangi chance resume context lama)
config.setdefault("session_reset", {})
config["session_reset"]["mode"] = config["session_reset"].get("mode", "both")
config["session_reset"]["idle_minutes"] = 60   # was 1440 (24h) → 1h
config["session_reset"]["at_hour"] = config["session_reset"].get("at_hour", 4)

with open(config_path, "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)

print("  ✓ Persona 'rei' (re)injected — fixed typo, overwrite clean")
print("  ✓ display.personality set to 'rei'")
print("  ✓ session_reset.idle_minutes tightened: 1440 → 60")
PYEOF

# 5b. Clear sessions (PENYEBAB UTAMA — Hermes resume context "Kiro")
if [[ "$KEEP_SESSIONS" == false ]] && [[ -d "$HERMES_SESSIONS" ]]; then
  SESSION_COUNT=$(find "$HERMES_SESSIONS" -type f \( -name "*.json" -o -name "*.jsonl" \) 2>/dev/null | wc -l)
  if [[ "$SESSION_COUNT" -gt 0 ]]; then
    find "$HERMES_SESSIONS" -type f \( -name "*.json" -o -name "*.jsonl" \) -delete
    echo -e "  ${GREEN}✓${NC} Cleared $SESSION_COUNT session files (backup di $BACKUP_DIR/sessions/)"
  else
    echo -e "  ${GREEN}✓${NC} Sessions sudah clean"
  fi
fi

# 5c. Clear memory residue "Kiro"
if [[ -d "$HERMES_MEMORY" ]]; then
  KIRO_MEM=$(grep -ril "kiro" "$HERMES_MEMORY/" 2>/dev/null || true)
  if [[ -n "$KIRO_MEM" ]]; then
    echo "$KIRO_MEM" | xargs -r rm -f
    echo -e "  ${GREEN}✓${NC} Cleared 'Kiro' residue di memory"
  else
    echo -e "  ${GREEN}✓${NC} No 'Kiro' residue di memory"
  fi
else
  echo -e "  ${GREEN}✓${NC} Memory dir belum ada (clean)"
fi

# 5d. Patch ~/.hermes/SOUL.md identity (THE real fix untuk nama Drayco)
# Tanpa ini, LLM jawab "Gue Main Assistant" walau persona block 'rei' udah aktif —
# karena ~/.hermes/SOUL.md di-load Hermes sebagai base identity prompt yang
# overrule personality overlay.
if [[ -f "$HERMES_SOUL" ]] && [[ "$SOUL_NEEDS_PATCH" -gt 0 ]]; then
  python3 <<PYEOF
from pathlib import Path

soul_path = Path("$HERMES_SOUL")
text = soul_path.read_text()

OLD_LINE = "You are Fathur's Main Assistant for the AI Holding system."

NEW_BLOCK = """Your name is **Drayco** — Fathur calls you **Rei** or **Rey**.
Your role is **Main Assistant** for the AI Holding system.

When asked "siapa lo / siapa kamu / siapa nama lo / what's your name":
Answer: "Gue Drayco — bisa lo panggil Rei atau Rey. Personal assistant lo untuk AI Holding."

NEVER answer with "Belum ada nama" — your name is Drayco.
NEVER identify yourself as just "Main Assistant" when asked your name — that is your ROLE, not your NAME.
NEVER identify as "Kiro" or generic "AI assistant".

You are Fathur's Main Assistant for the AI Holding system."""

if OLD_LINE in text and "Your name is **Drayco**" not in text:
    text = text.replace(OLD_LINE, NEW_BLOCK, 1)
    soul_path.write_text(text)
    print("  ✓ ~/.hermes/SOUL.md identity patched (Drayco/Rei bound)")
elif "Your name is **Drayco**" in text:
    print("  ✓ ~/.hermes/SOUL.md identity sudah OK (skip)")
else:
    print("  ⚠ ~/.hermes/SOUL.md format tak terduga — skip patch")
    print("    Manual fix: tambahin identity Drayco/Rei di top file")
PYEOF
elif [[ ! -f "$HERMES_SOUL" ]]; then
  echo -e "  ${YELLOW}⚠${NC} ~/.hermes/SOUL.md belum ada — skip identity patch"
else
  echo -e "  ${GREEN}✓${NC} ~/.hermes/SOUL.md identity sudah OK"
fi

echo ""

# ─── Step 6: Final instructions ───
echo "[6/6] Done. Next steps:"
echo ""
echo -e "  ${GREEN}1.${NC} Restart Hermes gateway:"
echo "       systemctl --user restart hermes-gateway"
echo ""
echo -e "  ${GREEN}2.${NC} Test di Telegram (sesi sekarang sudah FRESH, no resume):"
echo "       Kirim: \"siapa lo?\""
echo -e "       Expected: ${GREEN}\"gue Drayco — bisa lo panggil Rei...\"${NC} (gue/lo, no preamble)"
echo -e "       NOT:      ${RED}\"Aku Kiro — AI assistant...\"${NC}"
echo ""
echo -e "  ${GREEN}3.${NC} Verify (sebelum send Telegram):"
echo "       grep -ri 'Aku.*Kiro\\|\"Kiro\"' ~/.hermes/sessions/ 2>/dev/null"
echo "       Expected: empty"
echo ""
echo -e "  ${YELLOW}Rollback${NC} (kalau perlu):"
echo "       cp $BACKUP_DIR/config.yaml ~/.hermes/config.yaml"
echo "       [ -f $BACKUP_DIR/SOUL.md ] && cp $BACKUP_DIR/SOUL.md ~/.hermes/SOUL.md"
echo "       cp -r $BACKUP_DIR/sessions ~/.hermes/sessions"
echo "       systemctl --user restart hermes-gateway"
echo ""
echo "════════════════════════════════════════════════════════════"
