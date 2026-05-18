# Credentials — Template & Index

## Arsitektur (Option C)

```
REPO (aman di-commit):
  credentials/
  ├── README.md              ← ini
  ├── .gitignore             ← block semua *.env *.json *.key
  └── templates/             ← schema reference, tidak ada secret
      ├── twitter.env.example
      ├── discord.env.example
      ├── telegram.env.example
      ├── openai.env.example
      ├── github-pat.env.example
      └── wallet.env.example

WSL ONLY (tidak pernah ke Git):
  ~/.agent/credentials/
  ├── twitter.env            ← real values
  ├── discord.env            ← real values
  ├── telegram.env           ← real values
  ├── openai.env             ← real values (kalau pakai OpenAI)
  ├── github-pat.env         ← real values
  └── wallet.env             ← real values (kalau ada crypto)
```

## Setup Awal (setelah git pull di WSL)

```bash
# 1. Buat direktori credential di luar repo
mkdir -p ~/.agent/credentials
chmod 700 ~/.agent/credentials

# 2. Copy template → fill dengan real values
cd ~/ai-holding
cp credentials/templates/twitter.env.example ~/.agent/credentials/twitter.env
cp credentials/templates/discord.env.example ~/.agent/credentials/discord.env
cp credentials/templates/telegram.env.example ~/.agent/credentials/telegram.env
cp credentials/templates/openai.env.example ~/.agent/credentials/openai.env
cp credentials/templates/github-pat.env.example ~/.agent/credentials/github-pat.env

# 3. Edit masing-masing file
nano ~/.agent/credentials/twitter.env
nano ~/.agent/credentials/discord.env
# dst...

# 4. Set permission ketat
chmod 600 ~/.agent/credentials/*.env
```

## Credential Index

| File | Platform | Siapa yang pakai | Rotation |
|------|----------|-----------------|----------|
| `twitter.env` | X/Twitter | @brandflow.social, @brandflow.community, @crypto.research | On expiry / 90 hari |
| `discord.env` | Discord | Main Assistant (Rei) | On expiry / 90 hari |
| `telegram.env` | Telegram | Main Assistant (Rei) | On expire |
| `openai.env` | OpenAI API | STT / LLM fallback | 90 hari |
| `github-pat.env` | GitHub | NexusAI agents | 60 hari |
| `wallet.env` | Crypto wallet | Future (kalau ada crypto ops) | Never rotate — cold backup |

## Rules

1. **NEVER** tulis credential asli di file yang masuk ke repo
2. **ALWAYS** reference by path di SOUL.md — bukan isi tokennya
3. **ALWAYS** chmod 600 setiap credential file
4. **NEVER** `echo $VAR` credential di terminal session yang direkam
5. Kalau credential expired / compromised → rotate immediately + update index di sini

## Load di Hermes/agent

```bash
# Di script atau SOUL context:
source ~/.agent/credentials/twitter.env
# Atau via Python:
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.agent/credentials/twitter.env"))
```
