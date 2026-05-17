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
