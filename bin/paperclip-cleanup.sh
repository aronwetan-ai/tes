#!/usr/bin/env bash
#
# paperclip-cleanup.sh — Hapus semua sisa Paperclip + adapter sebelum fresh install
#
# WHAT IT DOES:
#   1. Stop PM2 processes (paperclip, paperclip-rebuilt, etc.)
#   2. Kill running paperclip / pnpm dev processes
#   3. Backup ~/.paperclip/ (data dir) sebelum hapus
#   4. Backup ~/paperclip-src/ (cloned source) sebelum hapus
#   5. Uninstall global npm packages (paperclipai, hermes-paperclip-adapter)
#   6. Clear localStorage / pnpm cache yang relate ke Paperclip
#   7. Disable paperclip section di ~/.hermes/config.yaml (kalau ada)
#
# WHAT IT DOES NOT TOUCH:
#   - ~/.hermes/ (Hermes runtime — separate concern, identity Drayco/Rei live here)
#   - ~/ai-holding/ (repo workspace)
#   - ~/.agent/credentials/ (credentials)
#   - System Node.js / pnpm / pm2 binaries
#
# Usage:
#   bash bin/paperclip-cleanup.sh              # interactive (default)
#   bash bin/paperclip-cleanup.sh --dry-run    # preview only
#   bash bin/paperclip-cleanup.sh --apply      # auto-confirm
#   bash bin/paperclip-cleanup.sh --no-backup  # skip backup (faster, riskier)
#
# After running: ready untuk fresh install per knowledge/sop/paperclip-setup.md

set -euo pipefail

# ─── Config ───
PAPERCLIP_DATA="${HOME}/.paperclip"
PAPERCLIP_SRC="${HOME}/paperclip-src"
HERMES_CONFIG="${HOME}/.hermes/config.yaml"
BACKUP_BASE="${HOME}/.paperclip-cleanup-backup-$(date +%Y%m%d-%H%M%S)"

# ANSI colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# ─── Flags ───
DRY_RUN=false
AUTO_APPLY=false
DO_BACKUP=true

for arg in "$@"; do
  case "$arg" in
    --dry-run)    DRY_RUN=true ;;
    --apply)      AUTO_APPLY=true ;;
    --no-backup)  DO_BACKUP=false ;;
    -h|--help)
      sed -n '3,20p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
  esac
done

# ─── Helpers ───
heading() {
  echo ""
  echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
  echo -e "${BLUE}  $1${NC}"
  echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
}

step() { echo -e "${YELLOW}[*]${NC} $1"; }
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
err()  { echo -e "  ${RED}✗${NC} $1"; }
info() { echo -e "  ${BLUE}ℹ${NC} $1"; }

run_or_skip() {
  if [[ "$DRY_RUN" == true ]]; then
    echo -e "  ${YELLOW}[DRY-RUN]${NC} $*"
  else
    eval "$*"
  fi
}

# ─── Step 1: Discover what's running ───
heading "Paperclip Cleanup — Discovery Phase"

step "Scanning for Paperclip-related state..."
echo ""

# PM2 processes
PM2_PROCS=""
if command -v pm2 >/dev/null 2>&1; then
  PM2_PROCS=$(pm2 jlist 2>/dev/null | grep -oE '"name":"[^"]*paperclip[^"]*"' | sed 's/"name":"//;s/"$//' || true)
  if [[ -n "$PM2_PROCS" ]]; then
    echo "  PM2 processes found:"
    echo "$PM2_PROCS" | sed 's/^/    - /'
  else
    info "No PM2 paperclip processes"
  fi
else
  info "pm2 not installed — skip PM2 check"
fi

# Running processes
RUNNING_PIDS=$(pgrep -f "paperclipai\|paperclip-src\|hermes-paperclip-adapter" 2>/dev/null || true)
if [[ -n "$RUNNING_PIDS" ]]; then
  echo "  Running processes (raw):"
  ps -fp $RUNNING_PIDS 2>/dev/null | tail -n +2 | awk '{print "    PID " $2 ": " substr($0, index($0,$8))}' | head -10
fi

# Data directory
if [[ -d "$PAPERCLIP_DATA" ]]; then
  PAPERCLIP_DATA_SIZE=$(du -sh "$PAPERCLIP_DATA" 2>/dev/null | cut -f1)
  echo "  Data dir: $PAPERCLIP_DATA ($PAPERCLIP_DATA_SIZE)"
else
  info "No data dir at $PAPERCLIP_DATA"
fi

# Source clone
if [[ -d "$PAPERCLIP_SRC" ]]; then
  PAPERCLIP_SRC_SIZE=$(du -sh "$PAPERCLIP_SRC" 2>/dev/null | cut -f1)
  echo "  Source clone: $PAPERCLIP_SRC ($PAPERCLIP_SRC_SIZE)"
else
  info "No source clone at $PAPERCLIP_SRC"
fi

# Global npm packages
GLOBAL_NPM=""
if command -v npm >/dev/null 2>&1; then
  GLOBAL_NPM=$(npm ls -g --depth=0 2>/dev/null | grep -E "paperclipai|hermes-paperclip-adapter" || true)
  if [[ -n "$GLOBAL_NPM" ]]; then
    echo "  Global npm packages:"
    echo "$GLOBAL_NPM" | sed 's/^/    /'
  else
    info "No global npm paperclip packages"
  fi
fi

# Port 3100 in use?
PORT_USAGE=""
if command -v lsof >/dev/null 2>&1; then
  PORT_USAGE=$(lsof -ti:3100 2>/dev/null || true)
  if [[ -n "$PORT_USAGE" ]]; then
    echo "  Port 3100 used by PID(s): $PORT_USAGE"
  fi
fi

# Hermes config paperclip section
HERMES_HAS_PAPERCLIP=0
if [[ -f "$HERMES_CONFIG" ]] && grep -q "^paperclip:" "$HERMES_CONFIG" 2>/dev/null; then
  HERMES_HAS_PAPERCLIP=1
  echo "  Hermes config has 'paperclip:' section (will be commented out)"
fi

# Old data warning if huge
if [[ -d "$PAPERCLIP_DATA" ]]; then
  SIZE_BYTES=$(du -sb "$PAPERCLIP_DATA" 2>/dev/null | cut -f1)
  if [[ "$SIZE_BYTES" -gt 524288000 ]]; then  # 500 MB
    warn "Paperclip data dir > 500 MB — backup akan lama (atau pakai --no-backup)"
  fi
fi

# ─── Step 2: Confirm ───
echo ""
heading "Action Plan"

cat <<EOF
  1. Stop PM2 paperclip processes
  2. Kill running paperclip / pnpm dev processes
  3. ${DO_BACKUP:+Backup}${DO_BACKUP:-Skip backup of} ${PAPERCLIP_DATA} → ${BACKUP_BASE}/data/
  4. ${DO_BACKUP:+Backup}${DO_BACKUP:-Skip backup of} ${PAPERCLIP_SRC} → ${BACKUP_BASE}/src/  (lalu DELETE)
  5. Uninstall global npm: paperclipai + hermes-paperclip-adapter
  6. Clear pnpm cache untuk paperclip packages
  7. Comment out 'paperclip:' section di ${HERMES_CONFIG}
EOF

if [[ "$DRY_RUN" == true ]]; then
  echo ""
  echo -e "${YELLOW}[DRY-RUN]${NC} No changes will be applied."
  echo "Apply real: bash $0 --apply"
  exit 0
fi

if [[ "$AUTO_APPLY" != true ]]; then
  echo ""
  read -p "Lanjut cleanup? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
  fi
fi

# ─── Step 3: Stop PM2 ───
heading "Step 1/7 — Stop PM2 processes"
if [[ -n "$PM2_PROCS" ]]; then
  while IFS= read -r proc; do
    [[ -z "$proc" ]] && continue
    step "Stopping PM2 process: $proc"
    run_or_skip "pm2 stop \"$proc\" 2>/dev/null || true"
    run_or_skip "pm2 delete \"$proc\" 2>/dev/null || true"
    ok "Removed: $proc"
  done <<< "$PM2_PROCS"
  run_or_skip "pm2 save 2>/dev/null || true"
else
  ok "No PM2 processes to clean"
fi

# ─── Step 4: Kill running ───
heading "Step 2/7 — Kill running processes"
RUNNING_PIDS_NOW=$(pgrep -f "paperclipai\|paperclip-src\|hermes-paperclip-adapter" 2>/dev/null || true)
if [[ -n "$RUNNING_PIDS_NOW" ]]; then
  step "Killing PIDs: $RUNNING_PIDS_NOW"
  run_or_skip "kill $RUNNING_PIDS_NOW 2>/dev/null || true"
  sleep 2
  # Force kill if still alive
  STILL_ALIVE=$(pgrep -f "paperclipai\|paperclip-src" 2>/dev/null || true)
  if [[ -n "$STILL_ALIVE" ]]; then
    warn "Some processes survived SIGTERM, sending SIGKILL: $STILL_ALIVE"
    run_or_skip "kill -9 $STILL_ALIVE 2>/dev/null || true"
  fi
  ok "Processes terminated"
else
  ok "No running processes to kill"
fi

# Free port 3100 if still occupied
if command -v lsof >/dev/null 2>&1; then
  PORT_USAGE_NOW=$(lsof -ti:3100 2>/dev/null || true)
  if [[ -n "$PORT_USAGE_NOW" ]]; then
    warn "Port 3100 still occupied by PID(s): $PORT_USAGE_NOW — killing"
    run_or_skip "kill -9 $PORT_USAGE_NOW 2>/dev/null || true"
  fi
fi

# ─── Step 5: Backup ───
heading "Step 3-4/7 — Backup + Delete data + source"
if [[ "$DO_BACKUP" == true ]]; then
  run_or_skip "mkdir -p \"$BACKUP_BASE\""

  if [[ -d "$PAPERCLIP_DATA" ]]; then
    step "Backing up data dir → $BACKUP_BASE/data/"
    run_or_skip "cp -r \"$PAPERCLIP_DATA\" \"$BACKUP_BASE/data\""
    ok "Backed up: $PAPERCLIP_DATA"
  fi

  if [[ -d "$PAPERCLIP_SRC" ]]; then
    step "Backing up source clone → $BACKUP_BASE/src/ (excluding node_modules + .git)"
    # Backup tanpa node_modules + .git supaya cepat dan ringan
    run_or_skip "rsync -a --exclude='node_modules' --exclude='.git' --exclude='dist' --exclude='.next' \"$PAPERCLIP_SRC/\" \"$BACKUP_BASE/src/\" 2>/dev/null || cp -r \"$PAPERCLIP_SRC\" \"$BACKUP_BASE/src\""
    ok "Backed up: $PAPERCLIP_SRC (lean, no node_modules)"
  fi

  if [[ "$DRY_RUN" != true ]]; then
    info "Backups saved at: $BACKUP_BASE"
  fi
else
  warn "--no-backup specified — skipping backup phase"
fi

# Delete data dir
if [[ -d "$PAPERCLIP_DATA" ]]; then
  step "Deleting data dir: $PAPERCLIP_DATA"
  run_or_skip "rm -rf \"$PAPERCLIP_DATA\""
  ok "Deleted: $PAPERCLIP_DATA"
fi

# Delete source
if [[ -d "$PAPERCLIP_SRC" ]]; then
  step "Deleting source clone: $PAPERCLIP_SRC"
  run_or_skip "rm -rf \"$PAPERCLIP_SRC\""
  ok "Deleted: $PAPERCLIP_SRC"
fi

# ─── Step 6: Uninstall global npm ───
heading "Step 5/7 — Uninstall global npm packages"
if command -v npm >/dev/null 2>&1; then
  for pkg in paperclipai hermes-paperclip-adapter; do
    if npm ls -g --depth=0 2>/dev/null | grep -q "$pkg"; then
      step "Uninstalling: $pkg"
      run_or_skip "npm uninstall -g \"$pkg\" 2>/dev/null || true"
      ok "Uninstalled: $pkg"
    fi
  done
else
  info "npm not available, skip"
fi

# ─── Step 7: Clear pnpm cache ───
heading "Step 6/7 — Clear pnpm cache for paperclip packages"
if command -v pnpm >/dev/null 2>&1; then
  step "Pruning pnpm store"
  run_or_skip "pnpm store prune 2>/dev/null || true"
  ok "pnpm store pruned"
else
  info "pnpm not installed, skip"
fi

# ─── Step 8: Comment out paperclip section di Hermes config ───
heading "Step 7/7 — Disable Paperclip in Hermes config"
if [[ "$HERMES_HAS_PAPERCLIP" -eq 1 ]]; then
  step "Commenting out 'paperclip:' section di $HERMES_CONFIG"

  # Backup config dulu
  CONFIG_BACKUP="${HERMES_CONFIG}.pre-paperclip-cleanup-$(date +%Y%m%d-%H%M%S)"
  run_or_skip "cp \"$HERMES_CONFIG\" \"$CONFIG_BACKUP\""
  info "Hermes config backup: $CONFIG_BACKUP"

  # Use Python (we already verified it works) to comment out the section
  if [[ "$DRY_RUN" != true ]]; then
    python3 <<'PYEOF'
import re
import os

config_path = os.path.expanduser("~/.hermes/config.yaml")
with open(config_path) as f:
    text = f.read()

# Find paperclip: section (top-level YAML key)
# Match from 'paperclip:' to the next top-level key or EOF
pattern = re.compile(
    r'^paperclip:\s*\n'                    # 'paperclip:' line
    r'(?:[ \t]+.*\n|^\s*\n)*',             # indented lines + blank lines
    re.MULTILINE,
)

def comment_block(match):
    block = match.group(0)
    # Comment out each line
    return '\n'.join(
        ('# ' + line) if line.strip() else line
        for line in block.splitlines()
    ) + '\n'

new_text, count = pattern.subn(comment_block, text, count=1)
if count > 0:
    with open(config_path, 'w') as f:
        f.write(new_text)
    print(f"  ✓ Commented out paperclip: section ({count} block)")
else:
    print("  ⚠ paperclip: section not found (already clean?)")
PYEOF
  else
    echo -e "  ${YELLOW}[DRY-RUN]${NC} Would comment out paperclip: section via Python"
  fi
  ok "Hermes config updated"
else
  ok "Hermes config has no paperclip section (already clean)"
fi

# ─── Done ───
heading "Cleanup Complete"

cat <<EOF

State sekarang:
  ✓ All Paperclip processes stopped
  ✓ ~/.paperclip/ deleted ${DO_BACKUP:+(backup at $BACKUP_BASE)}
  ✓ ~/paperclip-src/ deleted ${DO_BACKUP:+(backup at $BACKUP_BASE)}
  ✓ Global npm packages uninstalled
  ✓ Hermes config paperclip section disabled

Next steps:
  1. Restart Hermes: systemctl --user restart hermes-gateway
  2. Verify Hermes still works: kirim "siapa lo?" ke Telegram
  3. Fresh install Paperclip: ikutin knowledge/sop/paperclip-setup.md

Restore backup (kalau perlu):
EOF

if [[ "$DO_BACKUP" == true ]]; then
  cat <<EOF
  cp -r "$BACKUP_BASE/data" "$PAPERCLIP_DATA"
  cp -r "$BACKUP_BASE/src" "$PAPERCLIP_SRC"
  cp "$CONFIG_BACKUP" "$HERMES_CONFIG"
EOF
else
  echo "  (--no-backup was used, no restore available)"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
