# Voice Command Setup — Local Whisper STT

Versi: 1.0
Created: 2026-05-18
Owner: Main Assistant (Drayco/Rei)
Provider: Local Whisper (offline, free, privacy-first)

---

## Overview

Fathur bisa kirim **voice note ke Telegram** → Hermes auto-transcribe → proses seperti text command.

```
Voice note (Telegram)
    ↓
Hermes download audio file
    ↓
Local Whisper transcribe → teks Indonesia
    ↓
Drayco/Rei process command
    ↓
Reply teks ke Telegram
```

**100% offline** — audio tidak keluar dari mesin WSL.

---

## Install Whisper

### Option A: faster-whisper (Recommended — lebih cepat dari openai-whisper)

```bash
pip install faster-whisper
```

### Option B: openai-whisper (original)

```bash
pip install openai-whisper
# Dependencies
sudo apt install ffmpeg
```

---

## Download Model

| Model | Size | Speed | Akurasi Indonesian |
|-------|------|-------|--------------------|
| `tiny` | 75MB | Ultra fast | Cukup (testing) |
| `base` | 145MB | Fast | OK untuk slang ringan |
| `small` | 465MB | Medium | **Recommended** |
| `medium` | 1.5GB | Slower | Bagus untuk slang Gen-Z |
| `large-v3` | 3GB | Slowest | Best accuracy |

**Rekomendasi untuk Fathur:** `small` — balance antara speed dan akurasi Indonesian + slang.

```bash
# faster-whisper auto-download saat pertama kali run
# Atau manual:
python3 -c "from faster_whisper import WhisperModel; WhisperModel('small')"
# Model disimpan di ~/.cache/huggingface/hub/
```

---

## Script Transcriber

Buat file `bin/stt.py`:

```python
#!/usr/bin/env python3
"""
Voice note transcriber — Local Whisper STT
Usage: python3 bin/stt.py audio.ogg
Output: teks transkripsi ke stdout
"""

import sys
import os
import subprocess
import tempfile

MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
LANGUAGE = os.getenv("WHISPER_LANG", "id")  # Indonesian


def transcribe(audio_path: str) -> str:
    """Transcribe audio file to text using faster-whisper."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language=LANGUAGE)
        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()
    except ImportError:
        # Fallback ke openai-whisper
        import whisper
        model = whisper.load_model(MODEL_SIZE)
        result = model.transcribe(audio_path, language=LANGUAGE)
        return result["text"].strip()


def convert_to_wav(input_path: str) -> str:
    """Convert audio to WAV format (Whisper prefers WAV)."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
    subprocess.run(
        ["ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", wav_path, "-y", "-loglevel", "quiet"],
        check=True
    )
    return wav_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 stt.py <audio_file>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]

    # Convert kalau bukan WAV (Telegram kirim .ogg)
    if not audio_path.endswith(".wav"):
        wav_path = convert_to_wav(audio_path)
        text = transcribe(wav_path)
        os.unlink(wav_path)  # cleanup temp file
    else:
        text = transcribe(audio_path)

    print(text)
```

```bash
chmod +x bin/stt.py
```

---

## Konfigurasi Hermes

### config.yaml

```yaml
stt:
  enabled: true
  provider: local
  local:
    model: small           # tiny/base/small/medium/large-v3
    language: id           # Indonesian
    script: bin/stt.py     # Custom script path (opsional)

# Kalau pakai Hermes STT bawaan:
stt:
  enabled: true
  provider: local
  local:
    model: base            # Hermes default
```

---

## Hermes Native STT vs Custom Script

| | Hermes Native | Custom bin/stt.py |
|--|--------------|-------------------|
| Setup | Cukup config.yaml | Perlu install + script |
| Model control | Terbatas | Full control |
| Language hint | Auto-detect | Explicit `id` |
| Indonesian slang | Varies | Lebih baik dengan `small`+ |
| **Recommended** | ✓ untuk mulai cepat | ✓ kalau akurasi kurang |

**Start dengan Hermes native** dulu. Kalau hasilnya kurang accurate untuk Indonesian → switch ke custom script.

---

## Cara Kirim Voice Command

```
1. Buka chat Telegram dengan bot Hermes (Drayco/Rei)
2. Tekan dan tahan ikon mikrofon
3. Rekam command kamu
4. Lepas → kirim
5. Hermes auto-transcribe + proses + reply
```

**Tips untuk akurasi:**
- Bicara clear, jangan terlalu cepat
- Istilah teknis (deploy, commit, push) biasanya ke-capture dengan baik
- Kalau ada noise, cari tempat yang lebih sepi
- Mulai dengan kata yang jelas: "@brandflow buat content..." bukan langsung "...content..."

---

## Handling Transcription Error

Kalau Rei nggak yakin dengan transcription:

```
Rei: "gue tangkap: '[hasil transcribe]' — bener nggak? kalau salah koreksi ya"
```

Kalau transcription terlalu noise/tidak jelas:

```
Rei: "voice note-nya kurang jelas, bisa kirim ulang atau ketik commandnya?"
```

---

## Install ffmpeg (Required)

```bash
# Ubuntu/WSL
sudo apt update && sudo apt install -y ffmpeg

# Verify
ffmpeg -version
```

---

## Verify Setup

```bash
# Test dengan file audio sample
wget -O /tmp/test.ogg "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# Run transcriber
python3 bin/stt.py /tmp/test.ogg
# Harusnya output teks (mungkin noise tapi tidak error)

# Atau test Hermes STT langsung:
hermes --stt-test  # kalau ada flag ini
```

---

## Privacy Note

Semua audio diproses **lokal di WSL** — tidak dikirim ke server manapun.
Model Whisper berjalan sepenuhnya offline setelah download awal.

---

## Reference

- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- openai-whisper: https://github.com/openai/whisper
- Hermes STT config: `~/.hermes/config.yaml` (stt section)
- Model storage: `~/.cache/huggingface/hub/`
