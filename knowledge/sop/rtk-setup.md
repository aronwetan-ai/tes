# RTK Setup — Rust Token Killer

Versi: 1.0
Created: 2026-05-18
Owner: Main Assistant (Drayco/Rei) + NexusAI
Source: https://github.com/rtk-ai/rtk | https://rtk-ai.app/

---

## Apa itu RTK?

CLI proxy yang compress output terminal sebelum masuk ke AI context window.
Hemat **60–90% token** dari setiap command execution.

4 strategi kompresi:
1. **Smart filtering** — buang comments, whitespace berlebihan, boilerplate
2. **Grouping** — aggregate items serupa (file by dir, errors by type)
3. **Truncation** — potong output panjang yang redundant
4. **Deduplication** — hapus baris duplikat

Token savings di-track di SQLite lokal. Lihat stats: `rtk gain`

---

## Install

### Option A: Cargo (Rust toolchain)
```bash
cargo install rtk
```

### Option B: Download binary (zero deps, fastest)
```bash
# Linux x86_64
curl -fsSL https://github.com/rtk-ai/rtk/releases/latest/download/rtk-linux-x86_64 \
  -o /usr/local/bin/rtk && chmod +x /usr/local/bin/rtk

# Verify
rtk --version
```

---

## Integrasi ke Hermes

### config.yaml

```yaml
terminal:
  backend: local
  timeout: 180
  persistent_shell: true
  # Semua CLI command di-proxy lewat rtk
  command_prefix: "rtk"
```

### Manual usage (kalau nggak pakai config prefix)

```bash
# Pakai langsung sebagai prefix
rtk git status
rtk npm install
rtk docker ps
rtk ls -la

# Atau pipe output ke rtk
git log --oneline -20 | rtk
docker compose logs | rtk
```

---

## Konfigurasi RTK

File config: `~/.config/rtk/config.toml`

```toml
[filters]
# Aggressiveness: low, medium, high
level = "medium"

# Commands yang di-skip RTK filtering (kalau butuh raw output)
passthrough = ["cat", "less", "diff"]

[output]
# Tampilkan berapa token yang dihemat per command
show_savings = true

[retention]
# SQLite stats retention (hari)
days = 90
```

---

## Lihat Token Savings

```bash
# Total savings
rtk gain

# Savings per command type
rtk gain --breakdown

# Export CSV
rtk gain --export savings.csv
```

---

## Commands yang Paling Untung dari RTK

| Command | Typical savings |
|---------|----------------|
| `git log` | ~85% |
| `npm install` | ~90% |
| `docker compose logs` | ~88% |
| `ls -la` (large dir) | ~70% |
| `cat large_file.json` | ~75% |
| `pip install` | ~82% |
| `cargo build` | ~78% |

---

## Fail-safe

RTK dirancang fail-safe — kalau filtering gagal, fallback ke raw output.
Exit code dari original command tetap preserved (penting untuk CI/CD).

---

## Verify Setup

```bash
# Test basic
rtk echo "hello world"
# Output: hello world (passthrough, no noise to remove)

# Test dengan command yang punya noise
rtk git log --oneline -10
# Harusnya lebih compact dari git log --oneline -10 langsung

# Cek stats
rtk gain
```

---

## Reference

- GitHub: https://github.com/rtk-ai/rtk
- Token savings tracked di: `~/.local/share/rtk/savings.db`
- Hermes config: `~/.hermes/config.yaml` (terminal.command_prefix)
