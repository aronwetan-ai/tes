# Hermes Config Reference — config.yaml Schema

Versi: 1.0
Created: 2026-05-18
Owner: Operator + NexusAI
Source: Adapted from Hermes SOUL Guide Section 08
Location: ~/.hermes/config.yaml

---

## Purpose

Quick-reference untuk semua config sections yang tersedia di Hermes.
JANGAN commit config.yaml ke repo publik — bisa berisi API keys.

---

## Section Map

| Section | Purpose | Key Settings |
|---------|---------|--------------|
| model | LLM provider & model | default, provider, base_url |
| custom_providers | OpenAI-compatible providers | name, base_url, api_key, models[].context_length |
| fallback_model | Auto-failover | provider, model (trigger: 429/503/529) |
| agent | Behavior tuning | max_turns, reasoning_effort, tool_use_enforcement |
| agent.personalities | Personality presets | key: system_prompt pairs |
| approvals | Autonomy mode | mode (yolo/smart/always), timeout, cron_mode |
| terminal | Shell execution | backend (local/docker), timeout, persistent_shell |
| code_execution | Code runner | mode (project), timeout, max_tool_calls |
| browser | Web automation | engine (auto/camofox/playwright/cdp), cdp_url |
| memory | Persistent memory | memory_enabled, provider (holographic), char_limit |
| delegation | Sub-agent control | max_concurrent_children, orchestrator_enabled |
| compression | Context management | threshold, target_ratio, protect_last_n |
| auxiliary | Task-specific models | vision, web_extract, compression, session_search |
| skills | Skill system | external_dirs, disabled[], template_vars |
| display | UI/UX | personality, streaming, language, compact |
| security | Safety | redact_secrets, tirith_enabled, allow_private_urls |
| privacy | Data protection | redact_pii |
| tts/stt | Voice | provider (edge/elevenlabs/openai), voice model |
| cron | Scheduling | wrap_response, max_parallel_jobs |
| kanban | Task board | dispatch_interval_seconds, failure_limit |
| sessions | History | auto_prune, retention_days |
| logging | Logs | level (INFO/DEBUG), max_size_mb |

---

## Critical Settings untuk AI Holding

### Approval Mode

```yaml
approvals:
  mode: yolo          # Agent langsung eksekusi (sesuai autonomy-tiers.md)
  cron_mode: deny     # Scheduled tasks perlu explicit approval
```

Catatan: "yolo" mode HANYA aman kalau SOUL.md + autonomy-tiers.md sudah lengkap.
Agent tetap harus respect Boundary #4 dan Tier 3 konfirmasi meski mode yolo.

### Memory (Recommended)

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  provider: holographic    # Deep structured memory
  memory_char_limit: 1000000
  nudge_interval: 10
  flush_min_turns: 6
```

### Delegation (Sub-agent)

```yaml
delegation:
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true
  subagent_auto_approve: true
  inherit_mcp_toolsets: true
  child_timeout_seconds: 600
```

### Context Compression

```yaml
compression:
  enabled: true
  threshold: 0.2           # Mulai compress saat 80% penuh
  target_ratio: 0.2        # Compress sampai 20% terpakai
  protect_last_n: 20       # 20 pesan terakhir dilindungi
```

### Browser (Anti-detect)

```yaml
browser:
  engine: auto             # Prefer camofox kalau tersedia
  allow_private_urls: true
  record_sessions: true
  camofox:
    managed_persistence: true
```

---

## Contoh Config Minimal (Production-Ready)

```yaml
model:
  default: "your-model-name"
  provider: "custom"
  base_url: "https://api.example.com/v1"

agent:
  max_turns: 300
  tool_use_enforcement: auto
  reasoning_effort: medium

approvals:
  mode: yolo
  cron_mode: deny

terminal:
  backend: local
  timeout: 180
  persistent_shell: true

browser:
  engine: auto

memory:
  memory_enabled: true
  user_profile_enabled: true

delegation:
  max_concurrent_children: 3
  orchestrator_enabled: true
  subagent_auto_approve: true

compression:
  enabled: true

telegram:
  reactions: false
```

---

## Platform Messaging Quick-Ref

| Platform | Token Env Var | Key Config |
|----------|--------------|-----------|
| Telegram | TELEGRAM_BOT_TOKEN | reactions, allowed_chats |
| Discord | DISCORD_TOKEN | require_mention, auto_thread |
| Slack | SLACK_BOT_TOKEN | require_mention, allowed_channels |
| WhatsApp | (varies) | minimal config |
| Matrix | (varies) | require_mention |

---

## Security Checklist

- [ ] `redact_secrets: true` — auto-hide API keys di output
- [ ] `redact_pii: true` — hide personal data
- [ ] Config.yaml TIDAK di-commit ke repo publik
- [ ] API keys di .env file, bukan di config.yaml langsung
- [ ] `allow_private_urls: true` hanya kalau di environment yang aman

---

## Reference

- Source: Hermes SOUL Guide Section 08 (https://guide.mahiru.my.id/id/config/)
- Complementary: `knowledge/ml/llm-providers.md` (multi-provider selection)
- Complementary: `knowledge/sop/credential-management.md` (secrets handling)
