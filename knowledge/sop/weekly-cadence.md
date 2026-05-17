# Weekly Cadence — Autonomous Rhythm

Version: 1.0
Created: 2026-05-17
Owner: Operator (Main Assistant)
Scope: All 3 companies — defines what happens when, automatically, every week

---

## Design Principle

> **The system runs on a clock, not on prompts.**

Every Monday the machine starts. By Friday it's produced, reviewed, approved (or held), and recapped. Fathur's only action is responding to approval requests — the rest is autonomous.

---

## Weekly Timeline

All times in **WIB (UTC+7)** — Fathur's timezone.

### MONDAY — Production Day

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| 07:00 | Run all crypto tools (fear_greed, price_scraper, funding_rates, onchain_metrics, pattern_detector, news_scraper) | Crypto Consultant | @crypto.data | ✅ Tier 1 |
| 07:30 | Pull specialist inputs (market, onchain, macro, risk) | Crypto Consultant | @crypto.research | ✅ Tier 1 |
| 08:30 | Produce weekly synthesis (3-Lens + 6-layer) | Crypto Consultant | @crypto.research | ✅ Tier 1 |
| 09:00 | Produce Forecast Ledger entry | Crypto Consultant | @crypto.research | ✅ Tier 2 (logged) |
| 09:30 | QA review of research report | Crypto Consultant | @crypto.qa | ✅ Tier 1 |
| 10:00 | **HANDOFF** → BrandFlow (handoff block generated) | Cross-company | Operator | ✅ Tier 1 |
| 10:30 | BrandFlow produces content drafts (thread + carousel) | BrandFlow | @brandflow.copywriter + .designer | ✅ Tier 1 |
| 12:00 | BrandFlow internal QA | BrandFlow | @brandflow.qa | ✅ Tier 1 |
| 12:30 | Cross-company QA (@crypto.qa reviews BrandFlow draft) | Cross-company | @crypto.qa | ✅ Tier 1 |
| 13:00 | **APPROVAL REQUEST** sent to Fathur (batch) | System | Operator | ⏸️ Tier 3 — WAIT |
| 13:00+ | Fathur reviews and approves/revises/rejects | — | Fathur | Human action |

### TUESDAY — Publish Day (Post-Approval)

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| On approval | Schedule content per calendar | BrandFlow | @brandflow.social | ✅ Tier 1 |
| 08:00 | X/Twitter thread goes live | BrandFlow | @brandflow.social | ✅ (post-approval) |
| 12:00 | IG carousel goes live | BrandFlow | @brandflow.social | ✅ (post-approval) |
| Ongoing | Community engagement on live posts | BrandFlow | @brandflow.community | ✅ Tier 1 |

### WEDNESDAY — Mid-Week Check

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| 07:00 | Run crypto tools (daily refresh) | Crypto Consultant | @crypto.data | ✅ Tier 1 |
| 08:00 | Check: has anything materially changed since Monday? | Crypto Consultant | @crypto.research | ✅ Tier 1 |
| 08:30 | If material change (>5% move, major news) → produce update brief | Crypto Consultant | @crypto.research | ✅ Tier 2 |
| 09:00 | If update brief produced → route for approval (crisis update SOP) | Cross-company | Operator | ⏸️ Tier 3 if public |
| 10:00 | NexusAI dashboard data refresh verification | NexusAI | @nexusai.qa | ✅ Tier 1 |
| 10:00 | BrandFlow engagement metrics check (Mon/Tue posts) | BrandFlow | @brandflow.analytics | ✅ Tier 1 |

### THURSDAY — Preparation Day

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| 07:00 | Run crypto tools (daily refresh) | Crypto Consultant | @crypto.data | ✅ Tier 1 |
| 09:00 | Review: any Forecast Ledger entries hitting decay this week? | Crypto Consultant | @crypto.research | ✅ Tier 2 |
| 10:00 | Check: any QA failures unresolved from Monday? | All | QA agents | ✅ Tier 1 |
| 11:00 | Pre-plan next Monday: any special topics/events coming? | BrandFlow | @brandflow.social | ✅ Tier 1 |
| 14:00 | NexusAI: any tool issues to flag before next cycle? | NexusAI | @nexusai.devops | ✅ Tier 1 |

### FRIDAY — Recap Day

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| 07:00 | Run crypto tools (daily refresh) | Crypto Consultant | @crypto.data | ✅ Tier 1 |
| 09:00 | Produce weekly recap for each company | All | Company CEOs | ✅ Tier 2 |
| 10:00 | Cross-company summary (single report) | System | Operator | ✅ Tier 2 |
| 10:30 | QA health check (all cross-QA resolved? SLAs met?) | System | Operator | ✅ Tier 1 |
| 11:00 | Send weekly recap to Fathur (Telegram) | System | Operator | ✅ Tier 1 (informational) |
| 11:00 | Log week to `memory/global.md` | System | Operator | ✅ Tier 2 |

### WEEKEND — Monitoring Only

| Time | Action | Company | Agent | Autonomous? |
|------|--------|---------|-------|-------------|
| Daily 07:00 | Run fear_greed.py + btc_price.py (minimal) | Crypto Consultant | @crypto.data | ✅ Tier 1 |
| On alert trigger | If F&G <10 or >90, or BTC ±10% in 24h → crisis brief | Crypto Consultant | @crypto.research | ✅ Tier 2 + alert Fathur |

---

## Daily Tool Execution (Underlying All Days)

These run every day regardless of weekly phase:

| Tool | Frequency | Time | Purpose |
|------|-----------|------|---------|
| fear_greed.py | Every 4h | 07, 11, 15, 19, 23 | Sentiment baseline |
| btc_price.py (price_scraper.py) | Hourly | :00 | Price tracking |
| funding_rates.py | Every 8h | 07, 15, 23 | Derivatives check |
| onchain_metrics.py | Daily | 07:00 | On-chain snapshot |
| news_scraper.py | Every 6h | 07, 13, 19, 01 | Narrative tracking |
| pattern_detector.py | Daily | 07:30 | Pattern/cycle check |

NexusAI dashboard endpoints refresh based on these tool outputs (pull from cached tool results, not re-run).

---

## Trigger Conditions (Override Normal Cadence)

| Event | Trigger | Action | Who |
|-------|---------|--------|-----|
| BTC ±10% in 24h | price_scraper.py detects | Crisis brief immediately | @crypto.research |
| F&G extreme (<10 or >90) | fear_greed.py detects | Alert + sentiment brief | @crypto.research |
| Major news (T1 source) | news_scraper.py flags sentiment spike | Ad-hoc research request | @crypto.research |
| Tool failure >4h | API health check | Alert to @nexusai.devops + Fathur | NexusAI |
| QA FAIL (Critical/Sev-1) | QA agent flags | Hold delivery + alert Fathur | QA agent |
| Fathur direct request | Telegram message | Priority response, override queue | Operator |

---

## Week-Over-Week Continuity

### What Carries Over
- Forecast Ledger entries (until decay)
- Unresolved QA issues
- Content performance data (for next week's planning)
- Standing approvals (if Phase 2 pilot active)

### What Resets
- Weekly research (fresh data each Monday)
- Content calendar (new week, new plan)
- QA queue (clear pending items by Friday)

### Monthly Additions (First Monday of Month)
- Forecast Ledger review: score expired forecasts (Brier)
- Calibration discussion: are we systematically biased?
- Tool health review: any tools degraded/deprecated?
- Cross-company friction log review: any recurring handoff issues?

---

## Late/Missed Handling

| What's Late | Impact | Recovery |
|-------------|--------|----------|
| Monday tools don't run | Research delayed | @nexusai.devops investigates. If not resolved by 09:00, research uses last known data with STALE flag. |
| Research not ready by 10:00 | BrandFlow delayed | BrandFlow waits (does not produce from stale data). If not ready by 12:00, skip this week's content. |
| BrandFlow draft not ready by 12:00 | QA delayed | QA still reviews same-day. If not ready by 15:00, push publish to Wednesday. |
| Fathur doesn't approve Monday | Publish delayed | Content queued. Reminder per approval-workflow.md. Publish when approved (adjust schedule). |
| Mid-week crisis overrides normal flow | Thursday/Friday disrupted | Crisis takes priority. Weekly recap notes the disruption. Normal cadence resumes next Monday. |

---

## Fathur's Minimum Commitment

For the system to run autonomously, Fathur needs to:

1. **Check Telegram once on Monday afternoon** — approve/revise the weekly batch (~5 min)
2. **Read Friday recap** — optional but recommended (~3 min)
3. **Respond to alerts** — only when triggered (crisis, extreme market, tool failure)

**Total Fathur time per normal week: ~10 minutes.**

Everything else runs without him.

---

## Starting The Cadence (Bootstrap)

First week:
1. Operator sends Fathur: "Weekly cadence starting next Monday. You'll get approval request ~13:00 WIB. Reply 'yes'/'no'/'revise'."
2. Monday: run full pipeline, send first batch.
3. Log results. Fix any issues.
4. Week 2: smoother. Week 3: routine.

---

## Reference

- `knowledge/sop/autonomous-boundaries.md` — what's autonomous
- `knowledge/sop/approval-workflow.md` — how approval works
- `knowledge/sop/cross-company-handoff.md` — handoff protocol
- `knowledge/sop/cross-company-qa-routing.md` — QA triggers
- `knowledge/agent-design/task-logger-rules.md` — logging format
- `COMMANDS.md` — commands that trigger individual steps
