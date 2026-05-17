# AI Holding Memory

## Current Setup

Fathur is building an AI Holding system using Hermes on WSL2.

Current mode:
- Option A portable.
- One Telegram bot.
- One Main Assistant.
- AI holding workspace at ~/ai-holding.
- Designed to migrate later to Option C with Telegram topics.

## Important Decisions

1. Start with Main Assistant first.
2. Main Assistant acts as personal assistant, router, company generator, and recap manager.
3. Companies must be generated from templates.
4. Each company must have isolated memory.
5. Knowledge should be compact, not full article dumps.
6. Use Markdown for knowledge and memory.
7. Use JSONL for task routing.
8. Use high-agency but risk-aware behavior.

## Knowledge References

- knowledge/karpathy.md stores compact principles inspired by Karpathy:
  - Prompt is program.
  - Context is source code.
  - Memory is persistent state.
  - Skills are reusable modules.
  - Evals are tests.
  - Human remains the supervisor.

## Migration Plan

Current:
Telegram Bot → Main Assistant → command routing.

Future:
Telegram Group Topics → topic-based company routing.
