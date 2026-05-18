#!/usr/bin/env bash
#
# rei.sh — One-shot installer & switcher untuk persona Drayco/Rei
#
# Wraps:
#   - Provider switch (~/.hermes/config.yaml)
#   - Persona injection via install-rei-persona.sh
#   - Service restart
#   - Verification test
#
# Usage:
#   bash bin/rei.sh setup                    # interactive provider chooser
#   bash bin/rei.sh setup openrouter         # langsung pakai OpenRouter
#   bash bin/rei.sh setup anthropic          # langsung Anthropic Direct
#   bash bin/rei.sh setup local-qwen         # local Qwen di port 8080
#   bash bin/rei.sh setup kiro               # stay di Kiro proxy
#   bash bin/rei.sh status                   # cek persona aktif + provider
#   bash bin/rei.sh verify                   # full verification
#   bash bin/rei.sh restart                  # restart Hermes gateway only
#   bash bin/rei.sh rollback                 # restore last backup
#
# Setelah ganti provider, jalanin: bash bin/rei.sh setup <provider>

set -euo pipefail

HERMES_CONFIG="${HOME}/.hermes/config.yaml"
HOLDING_ROOT="${HOME}/ai-holding"
INSTALLER="${HOLDING_ROOT}/bin/install-rei-persona.sh"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# ─── Banner ───
banner() {
  echo "════════════════════════════════════════════════════════════"
  echo "  rei.sh — Persona Drayco/Rei Setup & Switcher"
  echo "════════════════════════════════════════════════════════════"
}

# ─── Helpers ───
require_config() {
  if [[ ! -f "$HERMES_CONFIG" ]]; then
    echo -e "${RED}ERROR:${NC} Hermes config nggak ada: $HERMES_CONFIG"
    echo "Install Hermes dulu."
    exit 1
  fi
}

require_installer() {
  if [[ ! -x "$INSTALLER" ]]; then
    echo -e "${RED}ERROR:${NC} install-rei-persona.sh nggak ada / nggak executable."
    echo "Run: chmod +x $INSTALLER"
    exit 1
  fi
}

current_provider() {
  python3 -c "
import yaml
with open('$HERMES_CONFIG') as f:
    cfg = yaml.safe_load(f) or {}
m = cfg.get('model', {})
print(f\"{m.get('provider','?')} | {m.get('default','?')} | {m.get('base_url','?')}\")
" 2>/dev/null || echo "unknown"
}

current_persona() {
  python3 -c "
import yaml
with open('$HERMES_CONFIG') as f:
    cfg = yaml.safe_load(f) or {}
print(cfg.get('display', {}).get('personality', 'none'))
" 2>/dev/null || echo "unknown"
}

# ─── Provider switchers ───
switch_to_openrouter() {
  local key="${1:-}"
  if [[ -z "$key" ]]; then
    echo -e "${YELLOW}Setup OpenRouter${NC}"
    echo "Get API key: https://openrouter.ai/keys"
    read -p "OpenRouter API key (sk-or-v1-...): " key
    if [[ -z "$key" ]]; then
      echo "Cancelled."
      exit 1
    fi
  fi

  python3 <<PYEOF
import yaml
from pathlib import Path

config = yaml.safe_load(open("$HERMES_CONFIG")) or {}
config["model"] = {
    "default": "anthropic/claude-haiku-4.5",
    "provider": "openrouter",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": "$key",
}
with open("$HERMES_CONFIG", "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)
print("  Provider switched: openrouter (claude-haiku-4.5)")
PYEOF
}

switch_to_anthropic() {
  local key="${1:-}"
  if [[ -z "$key" ]]; then
    echo -e "${YELLOW}Setup Anthropic Direct${NC}"
    echo "Get API key: https://console.anthropic.com/settings/keys"
    read -p "Anthropic API key (sk-ant-...): " key
    if [[ -z "$key" ]]; then
      echo "Cancelled."
      exit 1
    fi
  fi

  python3 <<PYEOF
import yaml

config = yaml.safe_load(open("$HERMES_CONFIG")) or {}
config["model"] = {
    "default": "claude-haiku-4-5-20241022",
    "provider": "anthropic",
    "api_key": "$key",
}
with open("$HERMES_CONFIG", "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)
print("  Provider switched: anthropic-direct (claude-haiku-4.5)")
PYEOF
}

switch_to_local_qwen() {
  python3 <<PYEOF
import yaml

config = yaml.safe_load(open("$HERMES_CONFIG")) or {}
config["model"] = {
    "default": "qwen35-4b-claude.gguf",
    "provider": "custom",
    "base_url": "http://localhost:8080/v1",
}
with open("$HERMES_CONFIG", "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=200)
print("  Provider switched: local-qwen (port 8080)")
PYEOF
  echo -e "  ${YELLOW}NOTE:${NC} Pastikan local Qwen server jalan di port 8080"
}

switch_to_kiro() {
  echo -e "${YELLOW}Stay di Kiro proxy${NC}"
  echo "Note: Kiro proxy punya enforced 'I'm Kiro' system prompt — persona Drayco"
  echo "akan ke-override di identity layer (tone tetep work, nama tetep 'Kiro')."
  read -p "Lanjut? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
  fi
  echo "  No config change. Stay di provider sekarang."
}

# ─── Commands ───
cmd_setup() {
  banner
  require_config
  require_installer

  local provider="${1:-}"

  if [[ -z "$provider" ]]; then
    echo ""
    echo "Pilih provider:"
    echo "  1) openrouter   — Recommended (Drayco persona aktif penuh)"
    echo "  2) anthropic    — Direct ke Anthropic"
    echo "  3) local-qwen   — Free, local LLM (port 8080)"
    echo "  4) kiro         — Stay di Kiro proxy (identity override)"
    echo "  5) cancel"
    echo ""
    read -p "Pilihan [1-5]: " choice
    case "$choice" in
      1) provider="openrouter" ;;
      2) provider="anthropic" ;;
      3) provider="local-qwen" ;;
      4) provider="kiro" ;;
      *) echo "Cancelled."; exit 0 ;;
    esac
  fi

  echo ""
  echo "[1/4] Provider switch..."
  case "$provider" in
    openrouter)
      switch_to_openrouter "${2:-}"
      ;;
    anthropic)
      switch_to_anthropic "${2:-}"
      ;;
    local-qwen)
      switch_to_local_qwen
      ;;
    kiro)
      switch_to_kiro
      ;;
    *)
      echo -e "${RED}ERROR:${NC} Unknown provider: $provider"
      echo "Valid: openrouter, anthropic, local-qwen, kiro"
      exit 1
      ;;
  esac

  echo ""
  echo "[2/4] Inject persona Drayco/Rei..."
  bash "$INSTALLER" --apply

  echo ""
  echo "[3/4] Restart Hermes gateway..."
  if systemctl --user is-enabled hermes-gateway &>/dev/null; then
    systemctl --user restart hermes-gateway
    echo -e "  ${GREEN}✓${NC} Restarted via systemctl"
  else
    echo -e "  ${YELLOW}⚠${NC} systemctl unit nggak ditemukan."
    echo "     Restart manual: pkill -f 'hermes gateway' && hermes gateway &"
  fi

  echo ""
  echo "[4/4] Verify..."
  sleep 2
  cmd_verify

  echo ""
  echo "════════════════════════════════════════════════════════════"
  echo -e "  ${GREEN}DONE.${NC} Test di Telegram: kirim 'siapa lo?'"
  if [[ "$provider" == "kiro" ]]; then
    echo -e "  Expected: ${YELLOW}'Kiro' (identity override) + tone Gen Z${NC}"
  else
    echo -e "  Expected: ${GREEN}'gue Drayco — bisa lo panggil Rei...'${NC}"
  fi
  echo "════════════════════════════════════════════════════════════"
}

cmd_status() {
  banner
  require_config
  echo ""
  echo "Provider:    $(current_provider)"
  echo "Persona:     $(current_persona)"
  echo "Config path: $HERMES_CONFIG"
  echo ""
  echo "Sessions:    $(ls ~/.hermes/sessions/ 2>/dev/null | wc -l) files"
  echo "Memory:      $(ls -d ~/.hermes/memory/ 2>/dev/null | wc -l) dir"
  echo ""
  if systemctl --user is-active hermes-gateway &>/dev/null; then
    echo -e "Service:     ${GREEN}active${NC}"
  else
    echo -e "Service:     ${RED}inactive${NC}"
  fi
}

cmd_verify() {
  echo "Verification:"

  local persona=$(current_persona)
  if [[ "$persona" == "rei" ]]; then
    echo -e "  ${GREEN}✓${NC} Active persona: rei"
  else
    echo -e "  ${RED}✗${NC} Active persona: $persona (expected: rei)"
  fi

  local has_rei=$(grep -c "^    rei:" "$HERMES_CONFIG" 2>/dev/null || echo "0")
  if [[ "$has_rei" -gt 0 ]]; then
    echo -e "  ${GREEN}✓${NC} Persona block 'rei' exists"
  else
    echo -e "  ${RED}✗${NC} Persona block 'rei' missing"
  fi

  if [[ -d ~/.hermes/sessions ]]; then
    local kiro_sessions=$(grep -ril "Aku.*Kiro" ~/.hermes/sessions/ 2>/dev/null | wc -l)
    if [[ "$kiro_sessions" -eq 0 ]]; then
      echo -e "  ${GREEN}✓${NC} No 'Kiro' residue in sessions"
    else
      echo -e "  ${YELLOW}⚠${NC} Found 'Kiro' in $kiro_sessions session files"
    fi
  fi

  if systemctl --user is-active hermes-gateway &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Hermes gateway active"
  else
    echo -e "  ${RED}✗${NC} Hermes gateway inactive"
  fi

  echo ""
  echo "Provider info:"
  echo "  $(current_provider)"
}

cmd_restart() {
  banner
  echo ""
  if systemctl --user is-enabled hermes-gateway &>/dev/null; then
    systemctl --user restart hermes-gateway
    echo -e "${GREEN}✓${NC} Restarted hermes-gateway"
  else
    echo -e "${YELLOW}⚠${NC} systemctl unit nggak ditemukan."
    echo "Restart manual:"
    echo "  pkill -f 'hermes gateway'"
    echo "  hermes gateway &"
  fi
}

cmd_rollback() {
  banner
  echo ""
  local latest=$(ls -dt ~/.hermes-backup-* 2>/dev/null | head -1)
  if [[ -z "$latest" ]]; then
    echo -e "${RED}ERROR:${NC} No backup found di ~/.hermes-backup-*"
    exit 1
  fi

  echo "Latest backup: $latest"
  read -p "Restore? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
  fi

  cp "$latest/config.yaml" "$HERMES_CONFIG"
  echo -e "  ${GREEN}✓${NC} Config restored"

  if [[ -d "$latest/sessions" ]]; then
    cp -r "$latest/sessions" ~/.hermes/ 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Sessions restored"
  fi

  systemctl --user restart hermes-gateway 2>/dev/null || true
  echo -e "  ${GREEN}✓${NC} Hermes restarted"
  echo ""
  echo "Rollback done."
}

cmd_help() {
  banner
  cat <<EOF

Usage: bash bin/rei.sh <command> [args]

Commands:
  setup [provider] [api_key]   Switch provider + inject persona + restart
                               Providers: openrouter | anthropic | local-qwen | kiro
                               Tanpa args = interactive mode

  status                       Cek persona aktif + provider + service status

  verify                       Run all verification checks

  restart                      Restart Hermes gateway only

  rollback                     Restore latest backup (~/.hermes-backup-*)

  help                         Show this help

Examples:
  bash bin/rei.sh setup                              # interactive
  bash bin/rei.sh setup openrouter sk-or-v1-XXX     # langsung
  bash bin/rei.sh setup local-qwen                  # no key needed
  bash bin/rei.sh status
  bash bin/rei.sh verify
  bash bin/rei.sh rollback

After ganti provider, persona Drayco/Rei akan otomatis aktif.
EOF
}

# ─── Main ───
case "${1:-help}" in
  setup) shift; cmd_setup "$@" ;;
  status) cmd_status ;;
  verify) cmd_verify ;;
  restart) cmd_restart ;;
  rollback) cmd_rollback ;;
  help|-h|--help) cmd_help ;;
  *)
    echo -e "${RED}ERROR:${NC} Unknown command: $1"
    echo ""
    cmd_help
    exit 1
    ;;
esac
