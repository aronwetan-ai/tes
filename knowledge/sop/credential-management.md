# Credential Management Policy

Versi: 1.0
Created: 2026-05-18
Owner: All agents + Operator
Source: Adapted from Hermes SOUL Guide Section 03

---

## Purpose

Standardisasi cara simpan, reference, dan rotate credential di seluruh AI Holding.
Mencegah credential bocor ke context, log, chat, atau repo publik.

---

## Golden Rules

1. **NEVER tulis credential di SOUL.md, MEMORY.md, atau file yang masuk context.**
2. **NEVER paste credential verbatim di chat output.**
3. **ALWAYS reference by file path** — `~/.agent/credentials/[nama].env`
4. **ALWAYS mask di output** — `sk-ant-***rg3`, bukan full key.
5. **ALWAYS tulis behavior SEGERA setelah mendapat credential baru.**

---

## Directory Structure

```
~/.agent/credentials/
├── wallet.env           # Private keys, mnemonics
├── github-pat.env       # GitHub Personal Access Token
├── discord-token.env    # Discord user/bot token
├── x-cookies.json       # X/Twitter session cookies
├── x-auth.env           # X/Twitter username + password + backup codes
├── google-auth.txt      # Google email + password + TOTP secret + backup codes
├── email-smtp.env       # IMAP/SMTP credentials
├── openrouter-key.env   # LLM provider API keys
├── server-ssh.env       # SSH keys / connection strings
└── README.md            # Index: file apa, untuk apa, kapan last rotated
```

---

## Per-Credential Checklist (4 Fields)

Setiap credential yang masuk HARUS segera ditulis behavior-nya:

```
[Nama Akses]:
  Status akun:   [milik agent / milik user / shared / company-owned]
  Credential:    [~/.agent/credentials/nama-file.env]
  Kemampuan:     [read, write, send, deploy, transfer, dll — SPESIFIK]
  Batas:         [aksi yang wajib konfirmasi sebelum eksekusi]
```

### Contoh: Wallet

```
Wallet (Primary):
  Status akun:   milik agent (agent generate, agent manage)
  Credential:    ~/.agent/credentials/wallet.env
  Kemampuan:     swap, bridge, mint, delegate, transfer, cek balance
  Batas:         x402 payment ke merchant baru (belum di whitelist)
```

### Contoh: GitHub

```
GitHub:
  Status akun:   milik agent (@agent-name)
  Credential:    ~/.agent/credentials/github-pat.env
  Kemampuan:     create repo, branch, issue, PR, commit, push, manage packages
  Batas:         delete repo, force push ke main/master
```

### Contoh: X/Twitter

```
X/Twitter:
  Status akun:   milik agent (@AgentName)
  Credential:    ~/.agent/credentials/x-cookies.json (primary)
                 ~/.agent/credentials/x-auth.env (fallback)
  Kemampuan:     posting, reply, like, retweet, follow, search, DM
  Batas:         hapus tweet dengan engagement tinggi, ubah profile bio
```

---

## Rotation Policy

| Credential Type | Rotation Frequency | Trigger |
|---|---|---|
| API keys (LLM, services) | 90 hari | Atau saat compromise suspected |
| PAT (GitHub, etc) | 60 hari | Atau saat scope berubah |
| Cookies (X, Google) | On expiry | Agent deteksi expired → re-login |
| Wallet keys | Never rotate | Tapi backup di cold storage |
| Passwords | 90 hari | Atau saat compromise suspected |

---

## Anti-Patterns

❌ Credential di SOUL.md — bocor ke context compression, log, platform lain.
❌ Credential di chat — bocor ke session history, bisa ke-recall.
❌ "Full access" tanpa spesifikasi — agent tidak tahu batasnya.
❌ Credential tanpa behavior — agent bingung, bisa salah pakai.
❌ Shared credential tanpa ownership clarity — siapa yang rotate? siapa yang monitor?

---

## Reference

- Source: Hermes SOUL Guide Section 03 (https://guide.mahiru.my.id/id/access/)
- Complementary: `knowledge/sop/autonomous-login.md` (login flows)
- Complementary: `knowledge/agent-design/soul-section-template.md` (Section 3: Capabilities)
