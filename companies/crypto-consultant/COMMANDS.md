# COMMANDS.md
Commands for Crypto Consultant.

## Knowledge Loading Rules

Setiap kali agent @crypto.* dipanggil, wajib baca file berikut secara urutan:
1. /home/fatur/ai-holding/memory/global.md
2. /home/fatur/ai-holding/companies/crypto-consultant/MEMORY.md
3. /home/fatur/ai-holding/knowledge/tools/tool-registry.md
4. /home/fatur/ai-holding/knowledge/agent-design/tool-use-rules.md
5. /home/fatur/ai-holding/knowledge/crypto/crypto-research-framework.md

## Research Commands

Format: @crypto <keyword>

@crypto research   — Riset lengkap: sentiment + market + risk + report
@crypto sentiment  — Cek Fear & Greed Index via fear_greed.py
@crypto market     — Analisis teknikal dan siklus market
@crypto risk       — Risk assessment kondisi market saat ini
@crypto report     — Susun dan simpan laporan final ke tasks/
@crypto status     — Tampilkan task aktif perusahaan
@crypto recap      — Rangkum progress perusahaan

## Task Commands

Format: @crypto <keyword>

@crypto new-task      — Buat task baru
@crypto save-decision — Simpan keputusan penting ke memory
@crypto new-project   — Buat folder project baru
@crypto improve-skill — Tingkatkan skill perusahaan

## Routing

Tasks should be routed based on:
- Strategy → CEO / Research Lead
- Planning → Project Manager
- Execution → Market Analyst, Risk Analyst, Data Analyst
- Review → QA Agent
- Documentation → Writer
