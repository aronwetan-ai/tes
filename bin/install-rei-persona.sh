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
# Patch is needed when:
#   (a) file masih punya legacy line "You are Fathur's Main Assistant" tanpa identity block, OR
#   (b) file udah punya marker AUTO-GENERATED tapi content beda dengan MAIN_SOUL.md (re-sync)
SOUL_NEEDS_PATCH=0
if [[ -f "$HERMES_SOUL" ]]; then
  if ! grep -q "BEGIN: AUTO-GENERATED IDENTITY" "$HERMES_SOUL" 2>/dev/null; then
    # First time install — needs patch
    SOUL_NEEDS_PATCH=1
  fi
  # Note: kalau marker ada, Python script di Step 5d akan deteksi
  # apakah perlu re-sync dengan MAIN_SOUL.md atau skip.
fi

echo "  Current display.personality: ${CURRENT_PERSONA}"
echo "  Has 'rei' persona block: $([ "$HAS_REI_PERSONA" -gt 0 ] && echo "YES" || echo "NO")"
echo "  Sessions with 'Kiro' residue: ${KIRO_SESSIONS}"
echo "  Config has typo 'Aku Kir': $([ "$HAS_TYPO" -gt 0 ] && echo "YES (will fix)" || echo "NO")"
echo "  ~/.hermes/SOUL.md identity: $([ "$SOUL_NEEDS_PATCH" -gt 0 ] && echo "needs initial patch" || echo "auto-managed (will re-sync from MAIN_SOUL.md)")"
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
echo -e "  ${YELLOW}G.${NC} Auto-sync ~/.hermes/SOUL.md identity dari MAIN_SOUL.md (THE real fix)"
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

# 5d. Patch ~/.hermes/SOUL.md identity (THE real fix untuk nama persona)
# Tanpa ini, LLM jawab "Gue Main Assistant" walau persona block tone aktif —
# karena ~/.hermes/SOUL.md di-load Hermes sebagai base identity prompt yang
# overrule personality overlay.
#
# AUTO-SYNC: Identity (name + nicknames + role) di-extract otomatis dari
# MAIN_SOUL.md. Jadi kalau lo edit nama persona di MAIN_SOUL.md, tinggal
# rerun installer ini — nggak perlu sentuh skrip ini.
#
# Format MAIN_SOUL.md yang di-parse (kontrak):
#   Header line:     `Role: <Role Name> — ...`
#   Identity section: `## Identity\n\nNama gue **<Name>** — ... manggil gue **<Nick1>** atau **<Nick2>** ...`
if [[ -f "$HERMES_SOUL" ]]; then
  python3 <<PYEOF
import re
import sys
from pathlib import Path

soul_path = Path("$HERMES_SOUL")
main_soul_path = Path("${HOLDING_ROOT}/MAIN_SOUL.md")

if not main_soul_path.exists():
    print("  ⚠ MAIN_SOUL.md nggak ada — skip identity patch")
    sys.exit(0)

main_soul = main_soul_path.read_text()

# ─── Extract role from header (line: "Role: Main Assistant — ...") ───
role_match = re.search(r'^Role:\s*([^\n—-]+?)(?:\s*[—-]|\n|$)', main_soul, re.MULTILINE)
role = role_match.group(1).strip() if role_match else "Main Assistant"

# ─── Extract name + nicknames from "## Identity" section ───
id_match = re.search(
    r'^##\s+Identity\s*\n(.+?)(?=\n##\s+|\Z)',
    main_soul,
    re.MULTILINE | re.DOTALL,
)

primary_name = None
nicknames = []

if id_match:
    id_section = id_match.group(1)
    # Take first paragraph only (avoid grabbing bolded words deeper down)
    first_paragraph = id_section.split("\n\n", 1)[0]
    bolds = re.findall(r'\*\*([^*\n]+?)\*\*', first_paragraph)
    bolds = [b.strip() for b in bolds if b.strip()]
    if bolds:
        primary_name = bolds[0]
        # Take up to 2 nicknames after primary name
        nicknames = bolds[1:3]

# ─── Validation: extracted values must be sane ───
def looks_like_name(s):
    if not s or len(s) < 2 or len(s) > 30:
        return False
    # Reject if contains punctuation/special chars beyond hyphen/apostrophe
    return bool(re.match(r"^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\-' ]*$", s))

if not primary_name or not looks_like_name(primary_name):
    print(f"  ⚠ Bisa nggak extract nama valid dari MAIN_SOUL.md (got: {primary_name!r})")
    print("    Pastikan section ## Identity punya: Nama gue **<Name>**")
    sys.exit(0)

nicknames = [n for n in nicknames if looks_like_name(n)]

# ─── Build expected SOUL.md content ───
if nicknames:
    nicks_str = " or ".join(f"**{n}**" for n in nicknames)
    nick_phrase = f"Fathur calls you {nicks_str}"
    nick_answer = " atau ".join(nicknames)
    answer = f'"Gue {primary_name} — bisa lo panggil {nick_answer}. Personal assistant lo untuk AI Holding."'
    nick_role_warn = f"NEVER identify yourself as just \"{role}\" when asked your name — that is your ROLE, not your NAME."
else:
    nick_phrase = f"You are also Fathur's personal AI assistant"
    answer = f'"Gue {primary_name}. Personal assistant lo untuk AI Holding."'
    nick_role_warn = f"NEVER identify yourself as just \"{role}\" when asked your name — that is your ROLE, not your NAME."

new_block = (
    f"Your name is **{primary_name}** — {nick_phrase}.\n"
    f"Your role is **{role}** for the AI Holding system.\n"
    f"\n"
    f'When asked "siapa lo / siapa kamu / siapa nama lo / what\'s your name":\n'
    f"Answer: {answer}\n"
    f"\n"
    f"NEVER answer with \"Belum ada nama\" — your name is {primary_name}.\n"
    f"{nick_role_warn}\n"
    f"NEVER identify as \"Kiro\" or generic \"AI assistant\".\n"
    f"\n"
    f"You are Fathur's {role} for the AI Holding system."
)

# Marker comments delimit the auto-generated block (idempotent re-runs)
BEGIN = "<!-- BEGIN: AUTO-GENERATED IDENTITY (from MAIN_SOUL.md, do not edit) -->"
END   = "<!-- END: AUTO-GENERATED IDENTITY -->"
wrapped = f"{BEGIN}\n{new_block}\n{END}"

text = soul_path.read_text()
old_legacy_line = "You are Fathur's Main Assistant for the AI Holding system."

if BEGIN in text and END in text:
    # Already auto-managed — replace block in place
    new_text = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        wrapped,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new_text == text:
        print("  ✓ ~/.hermes/SOUL.md identity sudah up-to-date (skip)")
    else:
        soul_path.write_text(new_text)
        print(f"  ✓ ~/.hermes/SOUL.md identity re-synced from MAIN_SOUL.md")
        print(f"    Name: {primary_name} | Nicknames: {', '.join(nicknames) or '(none)'} | Role: {role}")
elif old_legacy_line in text:
    # First-time install — replace legacy line with auto-managed block
    new_text = text.replace(old_legacy_line, wrapped, 1)
    soul_path.write_text(new_text)
    print(f"  ✓ ~/.hermes/SOUL.md identity patched from MAIN_SOUL.md")
    print(f"    Name: {primary_name} | Nicknames: {', '.join(nicknames) or '(none)'} | Role: {role}")
else:
    # File ada tapi format nggak terduga — prepend block setelah header H1
    h1_match = re.search(r'^(#\s+SOUL\.md.*?\n)', text, re.MULTILINE)
    if h1_match:
        insert_at = h1_match.end()
        new_text = text[:insert_at] + "\n" + wrapped + "\n" + text[insert_at:]
        soul_path.write_text(new_text)
        print(f"  ✓ ~/.hermes/SOUL.md identity prepended from MAIN_SOUL.md")
        print(f"    Name: {primary_name} | Nicknames: {', '.join(nicknames) or '(none)'} | Role: {role}")
    else:
        print("  ⚠ ~/.hermes/SOUL.md format tak terduga — skip patch")
        print("     Manual fix: tambahin identity di top file")
PYEOF
else
  echo -e "  ${YELLOW}⚠${NC} ~/.hermes/SOUL.md belum ada — skip identity patch"
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
