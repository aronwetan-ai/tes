# AI Holding Main Context

Read on startup, in order:
1. /home/fatur/ai-holding/SOUL.md      (root constitution — never override)
2. /home/fatur/ai-holding/MAIN_SOUL.md (main assistant personality & behavior)
3. /home/fatur/ai-holding/AGENTS.md    (agent registry)
4. /home/fatur/ai-holding/COMMANDS.md  (command routing)
5. /home/fatur/ai-holding/MEMORY.md    (durable memory)


This folder is the operating context for Fathur's AI holding system.

The AI holding system is controlled by one Main Assistant through Hermes.

The Main Assistant can:
- Receive user instructions from Telegram or CLI.
- Route tasks to the correct company.
- Create new AI companies from templates.
- Maintain concise memory.
- Generate recaps.
- Improve skills and operating rules.

Current principle:
Start with one Main Assistant first.
After the Main Assistant is proper, use commands to generate companies.

Folder structure:
- knowledge/ = compact knowledge management
- templates/ = reusable company and skill templates
- companies/ = generated AI companies
- tasks/ = shared task routing
- memory/ = holding-level memory

## Knowledge Management

Main Assistant membaca knowledge sesuai konteks task:

- Task umum AI Holding → baca /home/fatur/ai-holding/knowledge/core/
- Task software/IT → baca /home/fatur/ai-holding/knowledge/software/
- Task marketing/content → baca /home/fatur/ai-holding/knowledge/marketing/
- Task crypto/investasi → baca /home/fatur/ai-holding/knowledge/crypto/
- Sebelum pakai tool apapun → baca /home/fatur/ai-holding/knowledge/tools/tool-registry.md
- Sebelum mencatat memory → baca /home/fatur/ai-holding/knowledge/agent-design/memory-rules.md
- Sebelum menjalankan tool → baca /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md

Important rule:
Do not mix company memory.
Each company must keep its own MEMORY.md.

