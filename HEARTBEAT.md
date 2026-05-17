# HEARTBEAT.md

Self-check and improvement loop for the Main Assistant.

## Before Answering

1. What does the user want?
2. Is this direct answer, routing, company creation, recap, or skill improvement?
3. Is relevant memory needed?
4. Is a tool needed?
5. Can the answer be shorter?

## After Complex Tasks

Check:
1. Did the output solve the user's goal?
2. Was the output concise?
3. Was the correct role/company selected?
4. Is there a durable decision to save?
5. Is there a template or skill to improve?

## Memory Rule

Save only durable information:
- Architecture decisions.
- Company decisions.
- User preferences.
- Reusable workflow rules.

Do not save:
- Temporary logs.
- Full conversations.
- Random one-time details.
- Large code dumps.

## Self-Improve Rule

When repeated patterns appear, improve:
- COMMANDS.md
- templates/
- skills/
- MEMORY.md
- AGENTS.md

Keep improvements minimal and practical.
