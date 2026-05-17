#!/usr/bin/env python3
"""
osint_lookup.py — Identifier-pivot OSINT: phone / email / username → public surfaces.

Given an identifier (phone number, email, username), generate URLs to
public OSINT sources where that identifier might appear. NO automated
scraping — generates URLs the user opens in their browser.

For username, also probes a small set of platforms via HEAD requests
(public, unauthenticated) to see if the handle is taken — same approach
as Sherlock/WhatsMyName, narrower scope.

Categories:
- Phone:    OSINT lookup pages, carrier identification, breach lookup.
- Email:    Breach lookup (HaveIBeenPwned), Gravatar, public profile pages.
- Username: Sherlock-style platform availability check.

Substitute for face recognition (per `knowledge/scope/declined-tools.md`)
in investigation workflows.

Usage:
    tools/osint_lookup.py --phone +6281234567890
    tools/osint_lookup.py --email someone@example.com
    tools/osint_lookup.py --username johndoe
    tools/osint_lookup.py --username johndoe --probe   # check 30 platforms
    tools/osint_lookup.py --username johndoe --json

Risk: Low (URL generation + HEAD requests to public profile URLs).

Used by: `@nexusai.security`, investigations, agency due-diligence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any
from urllib import error, request
from urllib.parse import quote_plus


# ---------------------------------------------------------------------------
# Phone number lookup URL builders
# ---------------------------------------------------------------------------

def phone_lookup_urls(phone: str) -> dict[str, str]:
    p = phone.strip().replace(" ", "").replace("-", "")
    qs = quote_plus(p)
    return {
        "truecaller":     f"https://www.truecaller.com/search/id/{qs}",
        "google_search":  f"https://www.google.com/search?q={qs}",
        "duck_search":    f"https://duckduckgo.com/?q={qs}",
        "numverify_form": "https://numverify.com/  # paste manually for free tier",
        "carrier_lookup": f"https://freecarrierlookup.com/?phonenum={qs}",
    }


# ---------------------------------------------------------------------------
# Email lookup URL builders
# ---------------------------------------------------------------------------

def email_lookup_urls(email: str) -> dict[str, str]:
    qs = quote_plus(email)
    md5 = hashlib.md5(email.lower().strip().encode()).hexdigest()
    sha256 = hashlib.sha256(email.lower().strip().encode()).hexdigest()
    return {
        "haveibeenpwned":  f"https://haveibeenpwned.com/account/{qs}",
        "gravatar":        f"https://www.gravatar.com/avatar/{md5}?d=404",
        "gravatar_profile": f"https://www.gravatar.com/{md5}.json",
        "google_search":   f"https://www.google.com/search?q=%22{qs}%22",
        "duck_search":     f"https://duckduckgo.com/?q=%22{qs}%22",
        "github_search":   f"https://github.com/search?q={qs}&type=users",
        "intelx_search":   f"https://intelx.io/?s={qs}",
        "dehashed":        f"https://www.dehashed.com/search?query={qs}",
        "_hashes": {"md5": md5, "sha256": sha256},
    }


# ---------------------------------------------------------------------------
# Username platforms (Sherlock-style)
# ---------------------------------------------------------------------------

# Each entry: name → (URL template, "exists if" detector)
# For HEAD probe: we just look at status code by default.
USERNAME_PLATFORMS: dict[str, dict[str, Any]] = {
    "github":      {"url": "https://github.com/{u}",                       "exists_status": 200},
    "gitlab":      {"url": "https://gitlab.com/{u}",                       "exists_status": 200},
    "twitter":     {"url": "https://twitter.com/{u}",                      "exists_status": 200},
    "x":           {"url": "https://x.com/{u}",                            "exists_status": 200},
    "instagram":   {"url": "https://www.instagram.com/{u}/",               "exists_status": 200},
    "tiktok":      {"url": "https://www.tiktok.com/@{u}",                  "exists_status": 200},
    "linkedin":    {"url": "https://www.linkedin.com/in/{u}/",             "exists_status": 200},
    "youtube":     {"url": "https://www.youtube.com/@{u}",                 "exists_status": 200},
    "reddit":      {"url": "https://www.reddit.com/user/{u}/",             "exists_status": 200},
    "medium":      {"url": "https://medium.com/@{u}",                      "exists_status": 200},
    "devto":       {"url": "https://dev.to/{u}",                           "exists_status": 200},
    "stackoverflow":{"url": "https://stackoverflow.com/users/{u}",         "exists_status": 200},
    "hackernews":  {"url": "https://news.ycombinator.com/user?id={u}",     "exists_status": 200},
    "producthunt": {"url": "https://www.producthunt.com/@{u}",             "exists_status": 200},
    "behance":     {"url": "https://www.behance.net/{u}",                  "exists_status": 200},
    "dribbble":    {"url": "https://dribbble.com/{u}",                     "exists_status": 200},
    "vimeo":       {"url": "https://vimeo.com/{u}",                        "exists_status": 200},
    "twitch":      {"url": "https://www.twitch.tv/{u}",                    "exists_status": 200},
    "soundcloud":  {"url": "https://soundcloud.com/{u}",                   "exists_status": 200},
    "spotify":     {"url": "https://open.spotify.com/user/{u}",            "exists_status": 200},
    "pinterest":   {"url": "https://www.pinterest.com/{u}/",               "exists_status": 200},
    "facebook":    {"url": "https://www.facebook.com/{u}",                 "exists_status": 200},
    "telegram":    {"url": "https://t.me/{u}",                             "exists_status": 200},
    "kaggle":      {"url": "https://www.kaggle.com/{u}",                   "exists_status": 200},
    "huggingface": {"url": "https://huggingface.co/{u}",                   "exists_status": 200},
    "npm":         {"url": "https://www.npmjs.com/~{u}",                   "exists_status": 200},
    "pypi":        {"url": "https://pypi.org/user/{u}/",                   "exists_status": 200},
    "keybase":     {"url": "https://keybase.io/{u}",                       "exists_status": 200},
    "bitbucket":   {"url": "https://bitbucket.org/{u}/",                   "exists_status": 200},
    "lichess":     {"url": "https://lichess.org/@/{u}",                    "exists_status": 200},
}


def username_search_urls(username: str) -> dict[str, str]:
    qs = quote_plus(username)
    return {
        "google_search":  f"https://www.google.com/search?q=%22{qs}%22",
        "duck_search":    f"https://duckduckgo.com/?q=%22{qs}%22",
        "github_search":  f"https://github.com/search?q={qs}&type=users",
        "twitter_search": f"https://twitter.com/search?q={qs}",
        "intelx_search":  f"https://intelx.io/?s={qs}",
    }


# ---------------------------------------------------------------------------
# HEAD probe (for --probe)
# ---------------------------------------------------------------------------

def _probe_one(name: str, url: str, expected_status: int,
               timeout: float) -> dict[str, Any]:
    req = request.Request(url, method="HEAD")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; osint-lookup/1.0)")
    t0 = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
    except error.HTTPError as e:
        status = e.code
    except (error.URLError, TimeoutError, OSError) as e:
        return {
            "name":   name,
            "url":    url,
            "status": None,
            "exists": None,
            "error":  str(e),
            "ms":     round((time.perf_counter() - t0) * 1000, 1),
        }

    return {
        "name":   name,
        "url":    url,
        "status": status,
        "exists": status == expected_status,
        "ms":     round((time.perf_counter() - t0) * 1000, 1),
    }


def probe_username(username: str, timeout: float, max_workers: int) -> list[dict[str, Any]]:
    if not re.match(r"^[A-Za-z0-9_\.\-]{1,40}$", username):
        return []
    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for name, info in USERNAME_PLATFORMS.items():
            url = info["url"].format(u=username)
            tasks.append(ex.submit(_probe_one, name, url, info["exists_status"], timeout))
        results = []
        for f in as_completed(tasks):
            results.append(f.result())
    results.sort(key=lambda r: r["name"])
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="OSINT identifier pivot: phone / email / username → public sources.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--phone")
    g.add_argument("--email")
    g.add_argument("--username")

    p.add_argument("--probe", action="store_true",
                   help="(--username only) HEAD-probe ~30 platforms to check existence.")
    p.add_argument("--probe-timeout", type=float, default=8.0)
    p.add_argument("--probe-workers", type=int, default=8)
    p.add_argument("--json", action="store_true", help="JSON output.")
    args = p.parse_args()

    out: dict[str, Any] = {}

    if args.phone:
        if not re.match(r"^\+?[0-9 \-]{7,20}$", args.phone):
            print("ERROR: phone format invalid", file=sys.stderr)
            return 2
        out = {"identifier": "phone", "value": args.phone,
               "lookup_urls": phone_lookup_urls(args.phone)}
    elif args.email:
        if "@" not in args.email or len(args.email) > 254:
            print("ERROR: email invalid", file=sys.stderr)
            return 2
        out = {"identifier": "email", "value": args.email,
               "lookup_urls": email_lookup_urls(args.email)}
    elif args.username:
        if not re.match(r"^[A-Za-z0-9_\.\-]{1,40}$", args.username):
            print("ERROR: username chars/length invalid", file=sys.stderr)
            return 2
        out = {"identifier": "username", "value": args.username,
               "lookup_urls": username_search_urls(args.username)}
        if args.probe:
            out["probes"] = probe_username(args.username, args.probe_timeout,
                                            args.probe_workers)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(f"=== OSINT lookup: {out['identifier']} = {out['value']} ===\n")
    print("Search URLs (open in browser):")
    for k, v in out["lookup_urls"].items():
        if k.startswith("_"):
            continue
        print(f"  {k:<22}{v}")
    if out["lookup_urls"].get("_hashes"):
        h = out["lookup_urls"]["_hashes"]
        print(f"\n  email hashes:")
        print(f"    md5    {h['md5']}")
        print(f"    sha256 {h['sha256']}")

    if "probes" in out:
        found = [r for r in out["probes"] if r.get("exists")]
        unsure = [r for r in out["probes"]
                  if r.get("exists") is None and r.get("error")]
        print(f"\nProbed {len(out['probes'])} platforms.  "
              f"Found: {len(found)}.  Errors: {len(unsure)}.")
        if found:
            print("\nFound on:")
            for r in found:
                print(f"  {r['name']:<14} {r['url']}")
        if unsure:
            print("\nUnreachable / error:")
            for r in unsure[:10]:
                print(f"  {r['name']:<14} {r['error']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
