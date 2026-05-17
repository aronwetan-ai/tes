# TOOLS.md

Tool policy for Crypto Consultant.

Allowed by default:
- Planning
- Writing
- Code generation
- Documentation
- Analysis
- File creation inside company folder

Confirmation required:
- Delete files
- Overwrite important config
- Run destructive commands
- Access secrets
- Send external messages
- Deploy to production
- Make financial actions

Token rule:
- Read only relevant files.
- Summarize long context.
- Do not load all skills at once.

## Official Tools

### fear_greed.py

Name: fear_greed.py
Path: /home/fatur/ai-holding/tools/fear_greed.py
Purpose: Fetch latest Crypto Fear & Greed Index from Alternative.me API.
Used by: @crypto.research, @crypto.market, @crypto.risk
Command: python3 /home/fatur/ai-holding/tools/fear_greed.py

When to use:
- User asks about Fear & Greed Index
- User asks about crypto sentiment
- User asks about market fear or market greed
- User asks about short-term sentiment outlook
- User asks for 1-week sentiment forecast

Rules:
- Use this tool when relevant — do not say there is no real-time access before checking.
- Always separate fact, interpretation, and risk note in output.
- Never provide guaranteed profit or guaranteed signal.
- Include data source and timestamp in response.
- Output format: current value, comparison, trend, forecast, risk note.
