# Skill: Approval Request Formatter & Response Parser

**Version:** 1.0  
**Created:** 2026-05-18  
**Owner:** @operator, @main-assistant  
**Trigger:** Tier 3 decision ready for Fathur approval  
**Frequency:** 5x/week (every Monday + ad-hoc)  
**Risk Level:** Low

---

## Purpose

Format structured approval requests for Fathur via Telegram, parse his responses, and route to appropriate handlers. Ensures consistent approval workflow across all Tier 3 decisions.

---

## Prerequisites

- Telegram bot token (TELEGRAM_BOT_TOKEN env var)
- Telegram chat_id for Fathur (TELEGRAM_CHAT_ID env var)
- Decision data ready (type, priority, summary, preview, risk, deadline)
- Access to memory/approvals.jsonl for logging

---

## Steps

### Step 1: Gather Decision Data

Collect all required fields in one pass:

```
{
  "type": "publish | new-client | budget | deploy | strategic | other",
  "priority": "routine | time-sensitive | urgent",
  "summary": "2-3 sentences: what is being requested and why",
  "preview": "3-5 lines of content or options with recommendation",
  "risk": "What happens if approved — what's the downside",
  "deadline": "YYYY-MM-DD or 'no deadline'",
  "from": "@company.agent",
  "ref": "unique reference ID (e.g., FL-2026-05-19-001)"
}
```

**Rule:** Don't send approval request until all fields are populated. Fathur reviews finished work, not plans.

---

### Step 2: Format Structured Message

Build Telegram message per template:

```
🔒 APPROVAL REQUEST

Type:       <type>
From:       <from>
Priority:   <priority>
Deadline:   <deadline>

SUMMARY:
<summary>

PREVIEW:
<preview>

RISK:
<risk>

ATTACHED:
<Full draft available at: <path> or "see next message">

---
Reply with:
✅ "yes" — approve as-is
✏️ "revise: <feedback>" — approve with changes
❌ "no" — reject (with optional reason)
⏸️ "hold" — not now, ask again later
```

**For batch approvals (routine only):**

```
🔒 WEEKLY APPROVAL BATCH (Week of YYYY-MM-DD)

Items requiring approval:

1. [CONTENT] <item 1>
   Preview: <preview>
   Risk: <risk>
   
2. [CONTENT] <item 2>
   ...

---
Reply options:
✅ "all yes" — approve all items
✅ "1,2 yes, 3 no" — selective approval
✏️ "revise 1: <feedback>" — approve others, revise specified
❌ "all no" — reject batch
```

---

### Step 3: Send via Telegram

```python
import requests

def send_approval_request(message_text, ref_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        log_entry = {
            "ref": ref_id,
            "status": "SENT",
            "timestamp": datetime.utcnow().isoformat(),
            "message_id": response.json()["result"]["message_id"]
        }
        append_to_approvals_jsonl(log_entry)
        return True
    else:
        log_entry = {
            "ref": ref_id,
            "status": "SEND_FAILED",
            "error": response.text,
            "timestamp": datetime.utcnow().isoformat()
        }
        append_to_approvals_jsonl(log_entry)
        return False
```

---

### Step 4: Wait for Response (with Timeout Handling)

```
T+0h:     Request sent → log SENT
T+24h:    No response → send gentle reminder (routine only)
T+48h:    No response → send second reminder
T+72h:    No response → log TIMED_OUT, hold indefinitely
          Exception: if Priority=urgent, escalate with 🚨 alert
```

**Timeout reminder template:**

```
⏰ Reminder: approval pending for <summary>

Original request: <timestamp>
Priority: <priority>
Deadline: <deadline>

Please reply with: yes / no / revise: <feedback> / hold
```

---

### Step 5: Parse Response

Listen for Fathur's reply and classify:

```python
def parse_approval_response(message_text, ref_id):
    text = message_text.lower().strip()
    
    if text in ["yes", "ok", "lanjut", "go", "approved", "✅"]:
        return {"status": "APPROVED", "feedback": None}
    
    elif text.startswith("revise:") or text.startswith("ubah:"):
        feedback = text.split(":", 1)[1].strip()
        return {"status": "REVISE", "feedback": feedback}
    
    elif text in ["no", "jangan", "cancel", "❌"]:
        reason = text.split(":", 1)[1].strip() if ":" in text else None
        return {"status": "REJECTED", "reason": reason}
    
    elif text in ["hold", "nanti", "later", "⏸️"]:
        return {"status": "HELD", "feedback": None}
    
    else:
        return {"status": "UNCLEAR", "raw": message_text}
```

---

### Step 6: Route to Handler

Based on response status:

```
APPROVED:
  → Execute immediately
  → Log: [APPROVED] YYYY-MM-DD by Fathur
  → Trigger downstream action (publish, deploy, etc.)

REVISE:
  → Route feedback to owning agent
  → Agent revises work
  → Re-submit for approval (new ref_id)

REJECTED:
  → Cancel execution
  → Log: [REJECTED] YYYY-MM-DD by Fathur. Reason: <reason>
  → Notify owning agent

HELD:
  → Park in queue
  → Re-ask after 48h
  → Log: [HELD] YYYY-MM-DD, re-ask scheduled

TIMED_OUT:
  → Log: [TIMED_OUT] YYYY-MM-DD
  → Hold indefinitely (do NOT proceed)
  → Alert Operator for manual follow-up
```

---

### Step 7: Log to memory/approvals.jsonl

```jsonl
{"ref": "FL-2026-05-19-001", "type": "content-publish", "from": "@brandflow.copywriter", "priority": "routine", "status": "APPROVED", "submitted": "2026-05-19T10:00:00Z", "approved": "2026-05-19T12:30:00Z", "published": "2026-05-21T08:00:00Z"}
```

---

## Input Format

```json
{
  "type": "publish",
  "priority": "routine",
  "summary": "Weekly crypto brief for social media",
  "preview": "BTC +3.8% this week. Fear & Greed at 65.",
  "risk": "Standard — public financial content with disclaimer",
  "deadline": "2026-05-21",
  "from": "@brandflow.copywriter",
  "ref": "FL-2026-05-19-001"
}
```

---

## Output Format

**On Send:**
```
✅ Approval request sent
Ref: FL-2026-05-19-001
Type: content-publish
Priority: routine
Deadline: 2026-05-21
Waiting for Fathur's response...
```

**On Response:**
```
[APPROVED] 2026-05-19 12:30 UTC
Ref: FL-2026-05-19-001
Action: Execute immediately
Next: Publish to social media
```

---

## Common Errors & Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| Telegram message fails to send | Invalid token or chat_id | Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars. Test with `curl` to Telegram API. |
| Response not received after 72h | Fathur offline or didn't see message | Send escalation alert. If urgent, escalate to Operator. |
| Response is unclear (not yes/no/revise/hold) | Fathur replied with unexpected text | Log as UNCLEAR. Ask Operator to clarify. |
| Batch approval with selective response | Fathur approves some items, rejects others | Parse "1,2 yes, 3 no" format. Route each item separately. |
| Revise feedback is vague | Fathur says "revise: make it better" | Ask Operator to clarify with Fathur. Don't guess. |

---

## Verification

- [ ] Approval request formatted per template
- [ ] All required fields populated (type, priority, summary, preview, risk, deadline)
- [ ] Message sent successfully to Telegram (check API response)
- [ ] Response received and parsed correctly
- [ ] Status logged to memory/approvals.jsonl
- [ ] Downstream action triggered (or held/rejected as appropriate)
- [ ] No approval proceeds without explicit "yes" from Fathur

---

## Notes

- **Batch approvals:** Only for routine priority. Time-sensitive and urgent must be individual.
- **Silence ≠ consent:** If Fathur doesn't respond in 72h, hold indefinitely. Never assume approval.
- **Revise loop:** Can repeat revise→resubmit multiple times. No limit, but log each iteration.
- **Timezone:** All times in WIB (UTC+7) for Fathur's convenience.
- **Fallback:** If Telegram is down, system holds all Tier 3 decisions until channel restored.

---

## Related Skills

- Skill: Cross-Company Handoff Block Generator (generates content for approval)
- Skill: System Audit (reviews approval SLA compliance)
- SOP: approval-workflow.md (full specification)
- SOP: weekly-cadence.md (approval timing)
