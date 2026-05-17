#!/usr/bin/env python3
"""
TOOL-033 — LLM Multi-Provider Client
====================================

Unified client untuk 6 LLM providers: Anthropic, OpenAI, Groq, Kimi, DeepSeek, OpenRouter.
Adapted from SUPERAGENT v2 m7.md.

Usage (CLI):
    python tools/llm_client.py --provider anthropic --message "Halo"
    python tools/llm_client.py --provider groq --system "Anda asisten Indonesia" --message "Apa kabar?"

Usage (import):
    from tools.llm_client import call_llm
    result = call_llm("Halo", provider="anthropic")
    print(result)

Env vars (set yang dipakai saja):
    ANTHROPIC_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, KIMI_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY

Risk: Medium (network call to external API, requires API key)
"""

import os
import sys
import json
import argparse
import time
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library missing. Install: pip install requests", file=sys.stderr)
    sys.exit(1)


# Provider config registry
PROVIDERS = {
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-sonnet-4-20250514",
        "auth_style": "anthropic",  # x-api-key + anthropic-version
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "default_model": "anthropic/claude-sonnet-4-20250514",
        "auth_style": "bearer",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o",
        "auth_style": "bearer",
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key_env": "GROQ_API_KEY",
        "default_model": "llama-3.1-70b-versatile",
        "auth_style": "bearer",
    },
    "kimi": {
        "url": "https://api.moonshot.cn/v1/chat/completions",
        "key_env": "KIMI_API_KEY",
        "default_model": "moonshot-v1-128k",
        "auth_style": "bearer",
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key_env": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
        "auth_style": "bearer",
    },
}


def call_llm(
    message: str,
    system: str = "You are a helpful assistant.",
    provider: str = "anthropic",
    model: Optional[str] = None,
    max_tokens: int = 1024,
    timeout: int = 60,
    max_retries: int = 2,
) -> str:
    """
    Call an LLM provider with unified interface.

    Returns: response text (string).
    Raises: RuntimeError on failure after retries.
    """
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(PROVIDERS.keys())}")

    cfg = PROVIDERS[provider]
    api_key = os.getenv(cfg["key_env"])
    if not api_key:
        raise RuntimeError(f"Missing env var: {cfg['key_env']}")

    use_model = model or cfg["default_model"]

    # Build headers + body per auth style
    if cfg["auth_style"] == "anthropic":
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": use_model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": message}],
        }
    else:  # bearer (OpenAI-compatible)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body = {
            "model": use_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            "max_tokens": max_tokens,
        }

    # Retry loop
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(cfg["url"], json=body, headers=headers, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            # Parse per provider response shape
            if cfg["auth_style"] == "anthropic":
                return data["content"][0]["text"]
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            raise RuntimeError(f"LLM call failed after {max_retries + 1} attempts: {e}") from e

    raise RuntimeError(f"Unreachable: {last_error}")


def main():
    parser = argparse.ArgumentParser(description="LLM Multi-Provider Client")
    parser.add_argument("--provider", default="anthropic",
                        choices=list(PROVIDERS.keys()),
                        help="LLM provider to use")
    parser.add_argument("--model", help="Model name (override default)")
    parser.add_argument("--system", default="You are a helpful assistant.",
                        help="System prompt")
    parser.add_argument("--message", required=True, help="User message")
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of plain text")
    args = parser.parse_args()

    try:
        result = call_llm(
            message=args.message,
            system=args.system,
            provider=args.provider,
            model=args.model,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        if args.json:
            print(json.dumps({"provider": args.provider, "ok": True, "output": result}))
        else:
            print(result)
    except Exception as e:
        if args.json:
            print(json.dumps({"provider": args.provider, "ok": False, "error": str(e)}))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
