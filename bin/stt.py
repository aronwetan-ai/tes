#!/usr/bin/env python3
"""
TOOL-037 — Local Whisper STT (Speech-to-Text)
==============================================

Transcribe audio files to text using local Whisper model.
Designed for voice note → text command pipeline via Telegram.

Usage:
    python3 bin/stt.py <audio_file>
    python3 bin/stt.py voice_note.ogg
    python3 bin/stt.py recording.wav --model medium

Environment:
    WHISPER_MODEL  — Model size (default: small)
    WHISPER_LANG   — Language hint (default: id = Indonesian)

Output: Plain text transcription to stdout.
Exit codes: 0 = success, 1 = transcription error, 2 = arg/dep error.

Dependencies:
    - faster-whisper (pip install faster-whisper)  [preferred]
    - OR: openai-whisper (pip install openai-whisper)  [fallback]
    - ffmpeg (sudo apt install ffmpeg)

Privacy: 100% offline — no audio leaves the machine.
"""

import sys
import os
import subprocess
import tempfile
import argparse


def convert_to_wav(input_path: str) -> str:
    """Convert any audio format to 16kHz mono WAV (Whisper preferred input)."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name

    try:
        subprocess.run(
            [
                "ffmpeg", "-i", input_path,
                "-ar", "16000",
                "-ac", "1",
                "-f", "wav",
                wav_path,
                "-y",
                "-loglevel", "quiet"
            ],
            check=True
        )
    except FileNotFoundError:
        print("ERROR: ffmpeg not found. Install: sudo apt install ffmpeg", file=sys.stderr)
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: ffmpeg conversion failed: {e}", file=sys.stderr)
        sys.exit(1)

    return wav_path


def transcribe_faster_whisper(audio_path: str, model_size: str, language: str) -> str:
    """Transcribe using faster-whisper (SYSTRAN — recommended, faster than original)."""
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, language=language)
    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()


def transcribe_openai_whisper(audio_path: str, model_size: str, language: str) -> str:
    """Transcribe using openai-whisper (original — fallback)."""
    import whisper

    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=language)
    return result["text"].strip()


def transcribe(audio_path: str, model_size: str = "small", language: str = "id") -> str:
    """
    Transcribe audio file to text.
    Tries faster-whisper first, falls back to openai-whisper.
    """
    # Try faster-whisper first (faster, less memory)
    try:
        return transcribe_faster_whisper(audio_path, model_size, language)
    except ImportError:
        pass

    # Fallback to openai-whisper
    try:
        return transcribe_openai_whisper(audio_path, model_size, language)
    except ImportError:
        print(
            "ERROR: No Whisper library found.\n"
            "Install one of:\n"
            "  pip install faster-whisper   (recommended)\n"
            "  pip install openai-whisper   (fallback)\n",
            file=sys.stderr
        )
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio to text using local Whisper (offline)"
    )
    parser.add_argument("audio_file", help="Path to audio file (.ogg, .wav, .mp3, .m4a, etc)")
    parser.add_argument(
        "--model", "-m",
        default=os.getenv("WHISPER_MODEL", "small"),
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size (default: small)"
    )
    parser.add_argument(
        "--language", "-l",
        default=os.getenv("WHISPER_LANG", "id"),
        help="Language hint (default: id = Indonesian)"
    )
    args = parser.parse_args()

    # Validate input file
    if not os.path.isfile(args.audio_file):
        print(f"ERROR: File not found: {args.audio_file}", file=sys.stderr)
        sys.exit(2)

    # Convert to WAV if not already
    wav_path = None
    if not args.audio_file.lower().endswith(".wav"):
        wav_path = convert_to_wav(args.audio_file)
        audio_to_process = wav_path
    else:
        audio_to_process = args.audio_file

    try:
        text = transcribe(audio_to_process, args.model, args.language)
        if text:
            print(text)
        else:
            print("(empty transcription — audio mungkin terlalu pendek atau noise)", file=sys.stderr)
            sys.exit(1)
    finally:
        # Cleanup temp WAV
        if wav_path and os.path.exists(wav_path):
            os.unlink(wav_path)


if __name__ == "__main__":
    main()
