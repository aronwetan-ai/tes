# COMMANDS.md

Use pseudo-mentions only for company-specific routing.

## Company Routing

@nexusai <task>
Route task to NexusAI.

@brandflow <task>
Route task to BrandFlow.

@crypto <task>
Route task to Crypto Consultant.

## Direct Agent Routing

Format:
@company.agent <task>

Examples:
@nexusai.ceo buatkan arah strategis produk
@nexusai.cto buatkan arsitektur teknis
@nexusai.pm buatkan backlog MVP
@nexusai.backend buatkan desain API
@nexusai.frontend buatkan UI flow
@nexusai.devops buatkan deployment plan
@nexusai.qa buatkan test case
@nexusai.writer buatkan dokumentasi

@brandflow.cmo buatkan strategi campaign
@brandflow.copywriter buatkan caption Instagram
@brandflow.social buatkan kalender konten
@brandflow.seo buatkan keyword plan
@brandflow.analytics buatkan KPI campaign

@crypto.research buatkan riset narasi market
@crypto.market analisis trend BTC
@crypto.risk buatkan risk assessment
@crypto.data buatkan struktur data analisis
@crypto.report buatkan laporan market

## Cross-Company Commands

weekly brief
Start the full weekly cadence: run tools → research → handoff → BrandFlow draft → QA → approval request. See `knowledge/sop/weekly-cadence.md`.

handoff crypto ke brandflow
Trigger Crypto Consultant → BrandFlow handoff for latest research. Generates handoff block per `knowledge/sop/cross-company-handoff.md`.

handoff crypto ke nexusai
Trigger Crypto Consultant → NexusAI data spec handoff for dashboard refresh.

cross-qa status
Show all pending cross-company QA requests and their SLA status.

approval status
Show all pending Fathur approval requests and their age/timeout status.

weekly recap
Generate cross-company weekly summary for Fathur. Includes: research produced, content published, QA health, tool status, Forecast Ledger entries.

cek handoff aktif
List all active (non-expired) handoff blocks across companies.

kirim approval ke fathur: <summary>
Package and send approval request to Fathur per `knowledge/sop/approval-workflow.md`. Supports batch ("batch approval minggu ini").

cadence status
Show where we are in the weekly cadence (Monday=production, Tuesday=publish, etc.) and what's on track / delayed.

forecast ledger status
Show active Forecast Ledger entries, their decay dates, and any expired entries pending review.

crisis brief
Trigger ad-hoc crisis research workflow: run tools → quick synthesis → alert Fathur. Used when extreme market event detected.

---

## Main Assistant Natural Commands

status semua perusahaan
Show all company status.

recap semua perusahaan
Summarize all companies.

cek task aktif <company>
Show active tasks for one company. Backed by `bin/list_tasks.py --company <company> --active-only`.

cek task <company> status <STATUS>
Filter tasks by status (NEW / IN_PROGRESS / DONE / FAILED / CANCELLED / RETRY).

log task untuk @company.agent: <task description> [priority HIGH]
Create a new task. Backed by `bin/log_task.py` (or `bin/log-task.sh` wrapper).
Filter rules apply — basa-basi tidak boleh dilog. Lihat `knowledge/agent-design/task-logger-rules.md`.

mulai task <ID>
Transition task `NEW` → `IN_PROGRESS`. Backed by `bin/update_task.py`.

tutup task <ID> sebagai DONE [note: ...]
Transition task `IN_PROGRESS` → `DONE`. Backed by `bin/update_task.py`.

batalkan task <ID> [note: ...]
Transition task non-terminal → `CANCELLED`.

kirim pesan dari @x ke @y: <message> [ref T001]
Append agent-to-agent durable message to `messages.jsonl`. Backed by `bin/log_message.py`.

buat perusahaan baru bernama <name>, fokus <focus>
Create a new AI company from template.

list perusahaan
List existing companies.

buat skill baru <name>
Create a reusable skill.

improve skill <name>
Improve an existing skill.

simpan keputusan untuk <company>: <decision>
Save durable company decision.
