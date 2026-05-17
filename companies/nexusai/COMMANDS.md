# COMMANDS.md
Commands for NexusAI.

## Knowledge Loading Rules

Setiap kali agent @nexusai.* dipanggil, wajib baca file berikut secara urutan:
1. /home/fatur/ai-holding/memory/global.md
2. /home/fatur/ai-holding/companies/nexusai/MEMORY.md
3. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/software/software-development-sop.md

## Development Commands

Format: @nexusai <keyword>

@nexusai idea        — Generate ide produk atau fitur baru
@nexusai api         — Desain API endpoint
@nexusai architecture — Buat arsitektur teknis sistem
@nexusai deploy      — Buat deployment plan
@nexusai review      — Review code atau desain
@nexusai docs        — Buat dokumentasi teknis
@nexusai status      — Tampilkan task aktif perusahaan
@nexusai recap       — Rangkum progress perusahaan

## Task Commands

Format: @nexusai <keyword>

@nexusai new-task      — Buat task baru
@nexusai save-decision — Simpan keputusan penting ke memory
@nexusai new-project   — Buat folder project baru
@nexusai improve-skill — Tingkatkan skill perusahaan

## Routing

Tasks should be routed based on:
- Strategy → CEO / CTO
- Planning → Project Manager
- Backend → Backend Engineer
- Frontend → Frontend Engineer
- Infrastructure → DevOps Engineer
- Testing → QA Engineer
- Documentation → Technical Writer
