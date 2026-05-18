# Resource Management Policy — Start → Use → Stop

Versi: 1.0
Created: 2026-05-18
Owner: All agents (terutama NexusAI engineering + Operator)
Source: Adapted from Hermes SOUL Guide Section 05

---

## Purpose

Mencegah resource waste: service idle, container yang lupa di-stop, browser session yang menggantung.
Pola universal: **start → use → stop**. Tidak ada resource yang dibiarkan running tanpa alasan.

---

## The Pattern

```
1. START   — spin up resource (container, browser, dev server, build process)
2. USE     — lakukan task yang membutuhkan resource tersebut
3. STOP    — matikan resource segera setelah task selesai
```

## Exceptions (Long-Lived Processes)

Resource yang BOLEH tetap running tanpa stop:
- Production server / API endpoint yang melayani traffic
- Mining process yang memang scheduled 24/7
- Monitoring agent / health check daemon
- Cron scheduler (Hermes gateway)

Semua yang lain → WAJIB stop setelah selesai.

---

## Per-Resource Rules

### Browser / Container

```
- Setelah pakai browser untuk scrape/research → close browser session
- Setelah pakai Docker container untuk build/test → stop container
- Session timeout: 5 menit idle = auto-close (kalau supported)
```

### Dev Server / Build Process

```
- Setelah test selesai → stop dev server
- Setelah build artifact generated → stop build watcher
- Jangan biarkan `npm run dev` atau `python manage.py runserver` idle
```

### SSH / Remote Connection

```
- Setelah deploy atau maintenance selesai → disconnect SSH
- Jangan biarkan SSH tunnel open tanpa aktif dipakai
```

### LLM API Calls

```
- Set timeout per call (default: 60s)
- Jangan retry infinite — max 3 retries dengan exponential backoff
- Kalau provider down → fallback ke provider lain, bukan infinite wait
```

---

## Verification

Setelah stop, verify resource benar-benar mati:

```bash
# Container
docker ps | grep [nama] && echo "MASIH RUNNING — stop!" || echo "clean"

# Process
pgrep -f [pattern] && echo "MASIH RUNNING" || echo "clean"

# Port
lsof -i :[port] && echo "PORT MASIH OCCUPIED" || echo "clean"
```

---

## Anti-Patterns

❌ Start browser, lalu lupa close di akhir task.
❌ Spawn container untuk 1 test, lalu biarkan running berhari-hari.
❌ Open SSH session, deploy, lalu pindah task tanpa disconnect.
❌ LLM call tanpa timeout — bisa hang indefinitely.
❌ "Nanti aja di-stop" — nanti tidak pernah datang.

---

## Reference

- Source: Hermes SOUL Guide Section 05 (https://guide.mahiru.my.id/id/examples/)
- Complementary: `companies/nexusai/skills/devops/SKILL.md`
- Complementary: `knowledge/software/devops-cookbook.md`
