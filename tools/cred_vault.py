#!/usr/bin/env python3
"""
cred_vault.py — Encrypted per-client credential vault.

Stores credentials in a single encrypted file using a master key. Audit-logs
every read with timestamp + reason. Designed for the agency's multi-client
use case: each client's API tokens / session cookies / OAuth tokens isolated.

Storage layout:
    vault/
        vault.enc           # AES-256-GCM ciphertext, single source of truth
        vault.audit.jsonl   # append-only audit log

Master key:
    Read from env var $AI_VAULT_KEY (base64-encoded 32 bytes), or
    from $AI_VAULT_KEY_FILE (file containing the base64 key).
    Generate one with: tools/cred_vault.py keygen

Usage:
    tools/cred_vault.py keygen
    tools/cred_vault.py init
    tools/cred_vault.py set    --client client_42 --key ig.session_cookie --value '<sealed>'
    tools/cred_vault.py set    --client client_42 --key meta.access_token --stdin
    tools/cred_vault.py get    --client client_42 --key ig.session_cookie --reason "dm_run"
    tools/cred_vault.py list   [--client client_42]
    tools/cred_vault.py delete --client client_42 --key ig.session_cookie
    tools/cred_vault.py rotate --client client_42 --key meta.access_token --value '<new>'
    tools/cred_vault.py audit  [--limit 50] [--client client_42]
    tools/cred_vault.py export --client client_42  # encrypted export, for backup

Risk: Medium (writes encrypted file + audit log; never logs plaintext).

Used by: `@nexusai.security`, all automation that needs client credentials.
Reference: knowledge/security/opsec-multi-account.md.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Try `cryptography` first (preferred). Fall back to PBKDF2+stdlib if missing.
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # type: ignore[import-untyped]
    HAVE_CRYPTOGRAPHY = True
except ImportError:
    HAVE_CRYPTOGRAPHY = False


VAULT_DIR_DEFAULT = Path(
    os.environ.get("AI_VAULT_DIR", str(Path.home() / ".ai-holding" / "vault"))
)
VAULT_FILE = "vault.enc"
AUDIT_FILE = "vault.audit.jsonl"


# ---------------------------------------------------------------------------
# Master key handling
# ---------------------------------------------------------------------------

def load_master_key() -> bytes:
    raw = os.environ.get("AI_VAULT_KEY")
    if raw:
        try:
            key = base64.b64decode(raw)
        except (ValueError, TypeError) as e:
            raise SystemExit(f"AI_VAULT_KEY not valid base64: {e}")
        if len(key) != 32:
            raise SystemExit(f"AI_VAULT_KEY must decode to 32 bytes, got {len(key)}")
        return key

    fpath = os.environ.get("AI_VAULT_KEY_FILE")
    if fpath:
        try:
            raw = Path(fpath).read_text(encoding="utf-8").strip()
            key = base64.b64decode(raw)
            if len(key) != 32:
                raise SystemExit(
                    f"AI_VAULT_KEY_FILE must contain base64 of 32 bytes, got {len(key)}"
                )
            return key
        except OSError as e:
            raise SystemExit(f"cannot read AI_VAULT_KEY_FILE: {e}")

    raise SystemExit(
        "no master key. Set $AI_VAULT_KEY or $AI_VAULT_KEY_FILE. "
        "Run `tools/cred_vault.py keygen` to make one."
    )


# ---------------------------------------------------------------------------
# Crypto primitives (AES-GCM via cryptography lib)
# ---------------------------------------------------------------------------

def _require_cryptography() -> None:
    if not HAVE_CRYPTOGRAPHY:
        raise SystemExit(
            "cred_vault requires the `cryptography` package: "
            "pip install cryptography"
        )


def encrypt_blob(plaintext: bytes, master_key: bytes) -> bytes:
    """AES-256-GCM. Output: nonce(12) || ciphertext+tag."""
    _require_cryptography()
    nonce = os.urandom(12)
    aead = AESGCM(master_key)
    ct = aead.encrypt(nonce, plaintext, None)
    return nonce + ct


def decrypt_blob(blob: bytes, master_key: bytes) -> bytes:
    _require_cryptography()
    if len(blob) < 28:  # 12 nonce + at least 16 tag
        raise ValueError("ciphertext too short")
    nonce, ct = blob[:12], blob[12:]
    aead = AESGCM(master_key)
    return aead.decrypt(nonce, ct, None)


# ---------------------------------------------------------------------------
# Vault I/O
# ---------------------------------------------------------------------------

def vault_paths(vault_dir: Path) -> tuple[Path, Path]:
    return vault_dir / VAULT_FILE, vault_dir / AUDIT_FILE


def load_vault(vault_dir: Path, master_key: bytes) -> dict[str, dict[str, str]]:
    vfile, _ = vault_paths(vault_dir)
    if not vfile.exists():
        return {}
    try:
        blob = vfile.read_bytes()
        plaintext = decrypt_blob(blob, master_key)
        data = json.loads(plaintext.decode("utf-8"))
    except OSError as e:
        raise SystemExit(f"cannot read vault: {e}")
    except (ValueError, json.JSONDecodeError) as e:
        raise SystemExit(
            f"vault decryption / parse failed (wrong master key?): {e}"
        )
    if not isinstance(data, dict):
        raise SystemExit("corrupted vault: top-level not an object")
    return data


def save_vault(vault_dir: Path, master_key: bytes,
               data: dict[str, dict[str, str]]) -> None:
    vault_dir.mkdir(parents=True, exist_ok=True)
    vfile, _ = vault_paths(vault_dir)
    plaintext = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    blob = encrypt_blob(plaintext, master_key)
    tmp = vfile.with_suffix(vfile.suffix + ".tmp")
    tmp.write_bytes(blob)
    os.chmod(tmp, 0o600)
    os.replace(tmp, vfile)


def append_audit(vault_dir: Path, event: str, **fields: Any) -> None:
    vault_dir.mkdir(parents=True, exist_ok=True)
    _, afile = vault_paths(vault_dir)
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event": event,
        "actor": os.environ.get("USER") or os.environ.get("USERNAME") or "?",
        **fields,
    }
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    with afile.open("a", encoding="utf-8") as fh:
        fh.write(line)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_keygen(_args: argparse.Namespace) -> int:
    """Print a fresh 32-byte master key (base64). User stores it themselves."""
    key = os.urandom(32)
    print(base64.b64encode(key).decode("ascii"))
    print(
        "\n# Store this in $AI_VAULT_KEY or write to a file you point\n"
        "# $AI_VAULT_KEY_FILE at. Do NOT commit it. Lose it = lose vault.",
        file=sys.stderr,
    )
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    vault_dir: Path = args.vault_dir
    if (vault_dir / VAULT_FILE).exists():
        print(f"vault already exists at {vault_dir}", file=sys.stderr)
        return 2
    master = load_master_key()
    save_vault(vault_dir, master, {})
    append_audit(vault_dir, "INIT")
    print(f"initialized vault at {vault_dir}")
    return 0


def _read_value(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read().rstrip("\n")
    if args.value is not None:
        return args.value
    return getpass.getpass(prompt="value: ")


def cmd_set(args: argparse.Namespace) -> int:
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    value = _read_value(args)
    if not value:
        print("ERROR: empty value", file=sys.stderr)
        return 2
    data.setdefault(args.client, {})[args.key] = value
    save_vault(args.vault_dir, master, data)
    append_audit(args.vault_dir, "SET", client=args.client, key=args.key)
    print(f"OK SET {args.client}/{args.key}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    if not args.reason:
        print("ERROR: --reason required for get", file=sys.stderr)
        return 2
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    client_data = data.get(args.client, {})
    if args.key not in client_data:
        append_audit(args.vault_dir, "GET_MISS",
                     client=args.client, key=args.key, reason=args.reason)
        print(f"ERROR: {args.client}/{args.key} not found", file=sys.stderr)
        return 2
    append_audit(args.vault_dir, "GET",
                 client=args.client, key=args.key, reason=args.reason)
    sys.stdout.write(client_data[args.key])
    if not args.no_newline:
        sys.stdout.write("\n")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    if args.client:
        keys = sorted(data.get(args.client, {}).keys())
        if not keys:
            print(f"(no entries for {args.client})")
            return 0
        for k in keys:
            print(f"{args.client}/{k}")
    else:
        for client in sorted(data.keys()):
            for k in sorted(data[client].keys()):
                print(f"{client}/{k}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    client_data = data.get(args.client, {})
    if args.key not in client_data:
        print(f"ERROR: {args.client}/{args.key} not found", file=sys.stderr)
        return 2
    del client_data[args.key]
    if not client_data:
        del data[args.client]
    save_vault(args.vault_dir, master, data)
    append_audit(args.vault_dir, "DELETE", client=args.client, key=args.key)
    print(f"OK DELETE {args.client}/{args.key}")
    return 0


def cmd_rotate(args: argparse.Namespace) -> int:
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    if args.client not in data or args.key not in data[args.client]:
        print(f"ERROR: {args.client}/{args.key} not found, use 'set' first",
              file=sys.stderr)
        return 2
    new = _read_value(args)
    if not new:
        print("ERROR: empty value", file=sys.stderr)
        return 2
    data[args.client][args.key] = new
    save_vault(args.vault_dir, master, data)
    append_audit(args.vault_dir, "ROTATE", client=args.client, key=args.key)
    print(f"OK ROTATE {args.client}/{args.key}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    _, afile = vault_paths(args.vault_dir)
    if not afile.exists():
        print("(no audit log)")
        return 0
    lines = afile.read_text(encoding="utf-8").splitlines()
    if args.client:
        lines = [
            ln for ln in lines
            if json.loads(ln).get("client") == args.client
        ]
    for ln in lines[-args.limit:]:
        print(ln)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export a single client's entries as ENCRYPTED blob (base64)."""
    master = load_master_key()
    data = load_vault(args.vault_dir, master)
    client_data = data.get(args.client, {})
    if not client_data:
        print(f"ERROR: no entries for {args.client}", file=sys.stderr)
        return 2
    plaintext = json.dumps(
        {"client": args.client, "data": client_data},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    blob = encrypt_blob(plaintext, master)
    print(base64.b64encode(blob).decode("ascii"))
    append_audit(args.vault_dir, "EXPORT", client=args.client)
    return 0


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Encrypted per-client credential vault for the AI Holding.")
    p.add_argument("--vault-dir", type=Path, default=VAULT_DIR_DEFAULT,
                   help=f"Vault directory (default: {VAULT_DIR_DEFAULT}).")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("keygen", help="Print a new master key (base64).")
    sub.add_parser("init", help="Initialize an empty vault.")

    s_set = sub.add_parser("set", help="Add or overwrite an entry.")
    s_set.add_argument("--client", required=True)
    s_set.add_argument("--key", required=True)
    s_set.add_argument("--value")
    s_set.add_argument("--stdin", action="store_true")

    s_get = sub.add_parser("get", help="Read an entry to stdout.")
    s_get.add_argument("--client", required=True)
    s_get.add_argument("--key", required=True)
    s_get.add_argument("--reason", required=True,
                       help="Why this read; appended to audit log.")
    s_get.add_argument("--no-newline", action="store_true")

    s_list = sub.add_parser("list", help="List entries.")
    s_list.add_argument("--client", default=None)

    s_del = sub.add_parser("delete", help="Delete an entry.")
    s_del.add_argument("--client", required=True)
    s_del.add_argument("--key", required=True)

    s_rot = sub.add_parser("rotate", help="Rotate an existing entry's value.")
    s_rot.add_argument("--client", required=True)
    s_rot.add_argument("--key", required=True)
    s_rot.add_argument("--value")
    s_rot.add_argument("--stdin", action="store_true")

    s_aud = sub.add_parser("audit", help="Tail the audit log.")
    s_aud.add_argument("--limit", type=int, default=50)
    s_aud.add_argument("--client", default=None)

    s_exp = sub.add_parser("export", help="Encrypted export of one client.")
    s_exp.add_argument("--client", required=True)

    return p


def main() -> int:
    args = make_parser().parse_args()
    handlers = {
        "keygen": cmd_keygen,
        "init":   cmd_init,
        "set":    cmd_set,
        "get":    cmd_get,
        "list":   cmd_list,
        "delete": cmd_delete,
        "rotate": cmd_rotate,
        "audit":  cmd_audit,
        "export": cmd_export,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
