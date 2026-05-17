#!/usr/bin/env python3
"""
reverse_image_lookup.py — Open or build reverse-image-search URLs across
                          public engines (Google Lens, Yandex, TinEye, Bing).

Most reverse-image engines don't have free public APIs. This tool generates
shareable URLs you can open in a browser, or — when given a publicly-hosted
image URL — uses each engine's known query string format.

For a LOCAL image:
- Generates an SHA-256 fingerprint and prints upload-URL templates.
- Optionally opens the upload page in your default browser.

For a REMOTE (publicly accessible) image URL:
- Builds direct query URLs that work without upload.

Substitute for generic face recognition (per `knowledge/scope/declined-tools.md`).

Usage:
    tools/reverse_image_lookup.py --url https://example.com/photo.jpg
    tools/reverse_image_lookup.py --file photo.jpg
    tools/reverse_image_lookup.py --url ... --open      # open in browser
    tools/reverse_image_lookup.py --url ... --json

Risk: Low (only generates URLs and optionally opens browser; no upload
without explicit user action; no automated scraping of results).

Used by: `@nexusai.security`, OSINT investigations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus


def url_for_remote_image(image_url: str) -> dict[str, str]:
    """Build query URLs for engines that accept image-URL parameter."""
    qs = quote_plus(image_url)
    return {
        "google_images":  f"https://www.google.com/searchbyimage?image_url={qs}",
        "google_lens":    f"https://lens.google.com/uploadbyurl?url={qs}",
        "yandex":         f"https://yandex.com/images/search?rpt=imageview&url={qs}",
        "tineye":         f"https://tineye.com/search?url={qs}",
        "bing":           f"https://www.bing.com/images/searchbyimage?cbir=sbi&imgurl={qs}",
        "saucenao":       f"https://saucenao.com/search.php?url={qs}",
    }


def upload_pages_for_local() -> dict[str, str]:
    """Engines that require manual upload — open these and drop the file in."""
    return {
        "google_lens":    "https://lens.google.com/",
        "yandex":         "https://yandex.com/images/",
        "tineye":         "https://tineye.com/",
        "bing":           "https://www.bing.com/visualsearch",
        "saucenao":       "https://saucenao.com/",
    }


def fingerprint(path: Path) -> dict[str, str]:
    h_sha256 = hashlib.sha256()
    h_md5    = hashlib.md5()
    h_sha1   = hashlib.sha1()
    with path.open("rb") as fh:
        while chunk := fh.read(65536):
            h_sha256.update(chunk)
            h_md5.update(chunk)
            h_sha1.update(chunk)
    return {
        "sha256": h_sha256.hexdigest(),
        "sha1":   h_sha1.hexdigest(),
        "md5":    h_md5.hexdigest(),
        "size_bytes": str(path.stat().st_size),
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build reverse-image-search URLs for OSINT workflows.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--url",  help="Public URL of the image to search.")
    src.add_argument("--file", help="Local image file (prints upload URLs + fingerprint).")
    p.add_argument("--open", action="store_true",
                   help="Open URLs in your default browser.")
    p.add_argument("--engines", default="google_lens,yandex,tineye,bing,saucenao",
                   help="Comma-separated engine list (default: all).")
    p.add_argument("--json", action="store_true", help="JSON output.")
    args = p.parse_args()

    requested = [e.strip() for e in args.engines.split(",") if e.strip()]

    if args.url:
        if not (args.url.startswith("http://") or args.url.startswith("https://")):
            print("ERROR: --url must start with http:// or https://", file=sys.stderr)
            return 2
        all_urls = url_for_remote_image(args.url)
        urls = {k: v for k, v in all_urls.items() if k in requested or k == "google_images"}
        result: dict[str, object] = {
            "mode": "remote",
            "image_url": args.url,
            "search_urls": urls,
        }
    else:
        path = Path(args.file)
        if not path.is_file():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2
        all_uploads = upload_pages_for_local()
        uploads = {k: v for k, v in all_uploads.items() if k in requested}
        result = {
            "mode":         "local",
            "file":         str(path),
            "fingerprint":  fingerprint(path),
            "upload_pages": uploads,
            "note":         (
                "Engines below don't accept local files via API; open each, "
                "drag the file in. Fingerprint included so you can verify "
                "later that you searched on the same image."
            ),
        }

    if args.open:
        # Only open the engines we actually returned URLs/pages for.
        if args.url:
            target_map = result["search_urls"]
        else:
            target_map = result["upload_pages"]
        for engine, target in target_map.items():
            try:
                webbrowser.open_new_tab(target)
            except Exception as e:
                print(f"WARN: could not open {engine}: {e}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["mode"] == "remote":
            print(f"=== Reverse image search for: {args.url} ===\n")
            for engine, url in result["search_urls"].items():
                print(f"  {engine:<14} {url}")
        else:
            print(f"=== Local image: {result['file']} ===")
            fp = result["fingerprint"]
            print(f"  sha256: {fp['sha256']}")
            print(f"  size:   {fp['size_bytes']} bytes")
            print(f"\n  {result['note']}\n")
            print("  Upload pages:")
            for engine, page in result["upload_pages"].items():
                print(f"    {engine:<14} {page}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
