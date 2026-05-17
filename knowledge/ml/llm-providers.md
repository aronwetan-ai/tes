# LLM Provider Selection Guide

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.ml`) + Operator
Source: Adapted from SUPERAGENT v2 m7.md
Tool: `tools/llm_client.py` (TOOL-033)

---

## Purpose

Guide untuk memilih LLM provider berdasarkan use case di AI Holding.

---

## Provider Comparison Matrix

| Provider | Best For | Speed | Cost | Context | Quality |
|----------|----------|-------|------|---------|---------|
| **Anthropic (Claude)** | Reasoning, long-form, complex tasks | Medium | High | 200k | Excellent |
| **OpenAI (GPT-4o)** | General purpose, coding, vision | Medium | High | 128k | Excellent |
| **Groq (Llama)** | Speed-critical, real-time | Ultra-fast | Low | 8k | Good |
| **DeepSeek** | Coding, cost-effective | Fast | Very Low | 4k | Good |
| **Kimi (Moonshot)** | Long documents, research | Medium | Medium | 128k | Good |
| **OpenRouter** | Multi-model access, flexibility | Variable | Variable | Variable | Variable |

---

## Use Cases Per Company

### NexusAI (@nexusai.*)

**Default:** Anthropic (Claude) untuk architecture + strategic decisions
**Fallback:** OpenRouter untuk cost optimization
**Speed-critical:** Groq untuk real-time API responses

```
@nexusai.cto → Anthropic (reasoning)
@nexusai.backend → Groq (fast) or Anthropic (complex)
@nexusai.devops → DeepSeek (coding) or Groq (speed)
```

### BrandFlow (@brandflow.*)

**Default:** Anthropic (Claude) untuk creative + nuanced copy
**Fallback:** OpenAI (GPT-4o) untuk consistency
**Budget:** DeepSeek untuk bulk content generation

```
@brandflow.copywriter → Anthropic (quality)
@brandflow.social → Groq (speed) or DeepSeek (bulk)
@brandflow.cmo → Anthropic (strategy)
```

### Crypto Consultant (@crypto.*)

**Default:** Anthropic (Claude) untuk analysis + reasoning
**Research:** Kimi (long context untuk whitepaper analysis)
**Real-time:** Groq (fast market updates)

```
@crypto.research → Anthropic (analysis) or Kimi (long docs)
@crypto.risk → Anthropic (reasoning)
@crypto.market → Groq (speed) or DeepSeek (cost)
```

---

## Selection Decision Tree

```
START
  ↓
Is this speed-critical (< 2s response)?
  YES → Groq
  NO ↓
Is this reasoning-heavy (strategy, architecture, analysis)?
  YES → Anthropic
  NO ↓
Is this long-context (> 50k tokens)?
  YES → Kimi or Anthropic
  NO ↓
Is this cost-sensitive (bulk generation)?
  YES → DeepSeek
  NO ↓
Is this multi-model needed (flexibility)?
  YES → OpenRouter
  NO ↓
DEFAULT → Anthropic
```

---

## Cost Estimation (per 1M tokens)

| Provider | Input | Output | Notes |
|----------|-------|--------|-------|
| Anthropic | $3 | $15 | Premium quality |
| OpenAI | $2.50 | $10 | GPT-4o pricing |
| Groq | $0.05 | $0.10 | Ultra-cheap |
| DeepSeek | $0.14 | $0.28 | Very cheap |
| Kimi | $1 | $3 | Long context premium |
| OpenRouter | Variable | Variable | Depends on model |

---

## Environment Setup

Create `.env` file in workspace root:

```bash
# Pick provider(s) you use — not all required
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
OPENAI_API_KEY=sk-...
KIMI_API_KEY=your-moonshot-key
GROQ_API_KEY=gsk_...
DEEPSEEK_API_KEY=your-deepseek-key
```

Load via:
```bash
export $(cat .env | xargs)
```

---

## CLI Usage

```bash
# Basic call
python tools/llm_client.py --provider anthropic --message "Halo"

# With system prompt
python tools/llm_client.py --provider groq --system "Anda asisten Indonesia" --message "Apa kabar?"

# Custom model
python tools/llm_client.py --provider openrouter --model "openai/gpt-4o" --message "..."

# JSON output
python tools/llm_client.py --provider deepseek --message "..." --json
```

---

## Python Import Usage

```python
from tools.llm_client import call_llm

# Simple call
result = call_llm("Halo", provider="anthropic")
print(result)

# With system prompt
result = call_llm(
    "Analisis risiko BTC",
    system="Anda expert crypto analyst",
    provider="anthropic"
)

# Custom model
result = call_llm(
    "Buat caption Instagram",
    provider="openrouter",
    model="anthropic/claude-sonnet-4-20250514"
)
```

---

## Fallback Strategy

If primary provider fails:

```python
providers_fallback = ["anthropic", "openrouter", "groq"]

for provider in providers_fallback:
    try:
        result = call_llm(message, provider=provider)
        return result
    except RuntimeError:
        continue

raise RuntimeError("All providers failed")
```

---

## Monitoring & Logging

Track provider usage in `memory/global.md`:

```
[TOOL_USAGE — 2026-05-17]
- @crypto.research: Anthropic (1 call, 2.5k tokens)
- @nexusai.backend: Groq (3 calls, 1.2k tokens)
- @brandflow.copywriter: DeepSeek (5 calls, 8.3k tokens)
```

---

## Reference

- Source: `update/v2/openclaw/skills/m7.md`
- Tool: `tools/llm_client.py` (TOOL-033)
- Tool registry: `knowledge/tools/tool-registry.md`
