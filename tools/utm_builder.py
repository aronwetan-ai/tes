#!/usr/bin/env python3
"""
utm_builder.py — Convention-validated UTM URL builder for BrandFlow.

Enforces the agency-wide convention from
`knowledge/marketing/utm-conventions.md`:

  - utm_source from a fixed allowed-list
  - utm_medium from a fixed allowed-list
  - utm_campaign in `<client-slug>__<campaign-slug>__<YYYY-MM>` format
  - utm_content as `<piece-id>` or `<piece-id>__<variant>`
  - utm_term lowercase slug (paid only)

Rejects custom formats so analytics can be aggregated joinably across clients.

Tier:    Update 11 (BrandFlow deepening)
Risk:    Low (read-only stdin/args; constructs URL string)
Status:  Active

Usage:
    python3 utm_builder.py --url https://acme.com/landing \\
        --source instagram --medium organic-post \\
        --client acme --campaign-slug summer-launch --month 2026-05 \\
        --content BF-acme-0142

    python3 utm_builder.py --url https://acme.com/landing \\
        --source instagram --medium paid-feed \\
        --client acme --campaign-slug summer-launch --month 2026-05 \\
        --content BF-acme-0142 --variant hookA \\
        --term b2b-founders-id

Exit codes:
    0   built successfully
    1   validation error (printed to stderr)
    2   argument error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import quote, urlencode, urlparse

# ---------------------------------------------------------------------------
# Allowed values per the convention file
# ---------------------------------------------------------------------------

ALLOWED_SOURCES = {
    "instagram",
    "linkedin",
    "tiktok",
    "twitter",
    "youtube",
    "pinterest",
    "facebook",
    "whatsapp",
    "telegram",
    "email",
    "newsletter",
    "direct",
    "qr",
}

# Source prefixes allowed (for partner-/podcast-/influencer-specific tracking)
ALLOWED_SOURCE_PREFIXES = (
    "referral-",
    "podcast-",
)

ALLOWED_MEDIA = {
    "organic-post",
    "organic-reel",
    "organic-story",
    "organic-thread",
    "bio-link",
    "dm",
    "paid-feed",
    "paid-story",
    "paid-reel",
    "paid-search",
    "paid-display",
    "paid-influencer",
    "email-body",
    "email-cta",
    "email-footer",
    "referral",
    "event",
    "print",
    "organic",  # generic organic fallback for influencer/event
}

PAID_MEDIA = {m for m in ALLOWED_MEDIA if m.startswith("paid-")}

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
PIECE_ID_RE = re.compile(r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$")
VARIANT_RE = re.compile(r"^[a-zA-Z0-9]+([\-][a-zA-Z0-9]+)*$")
MAX_VALUE_LEN = 100


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    pass


def _validate_source(source: str) -> None:
    if source in ALLOWED_SOURCES:
        return
    for prefix in ALLOWED_SOURCE_PREFIXES:
        if source.startswith(prefix):
            tail = source[len(prefix):]
            if SLUG_RE.match(tail):
                return
            raise ValidationError(
                f"source '{source}': part after '{prefix}' must be a slug "
                f"(lowercase, hyphens, alnum)."
            )
    raise ValidationError(
        f"source '{source}' not in allowed list. "
        f"Allowed: {sorted(ALLOWED_SOURCES)} or prefixes "
        f"{list(ALLOWED_SOURCE_PREFIXES)}<slug>"
    )


def _validate_medium(medium: str) -> None:
    if medium not in ALLOWED_MEDIA:
        raise ValidationError(
            f"medium '{medium}' not in allowed list. "
            f"Allowed: {sorted(ALLOWED_MEDIA)}"
        )


def _validate_slug(value: str, field: str) -> None:
    if not SLUG_RE.match(value):
        raise ValidationError(
            f"{field} '{value}' must be lowercase, alphanumeric, "
            f"hyphenated (no underscores, no spaces)."
        )


def _validate_month(month: str) -> None:
    if not MONTH_RE.match(month):
        raise ValidationError(
            f"month '{month}' must be YYYY-MM (e.g. 2026-05)."
        )


def _validate_piece_id(piece_id: str) -> None:
    if not PIECE_ID_RE.match(piece_id):
        raise ValidationError(
            f"piece-id '{piece_id}' must be alphanumeric / hyphenated "
            f"(e.g. BF-acme-0142)."
        )


def _validate_variant(variant: str) -> None:
    if not VARIANT_RE.match(variant):
        raise ValidationError(
            f"variant '{variant}' must be alphanumeric / hyphenated "
            f"(e.g. hookA, copy-v2)."
        )


def _validate_term(term: str) -> None:
    if not SLUG_RE.match(term):
        raise ValidationError(
            f"term '{term}' must be a slug "
            f"(lowercase, alphanumeric, hyphenated)."
        )


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError(
            f"url '{url}' must start with http:// or https:// "
            f"(got scheme '{parsed.scheme}')."
        )
    if not parsed.netloc:
        raise ValidationError(f"url '{url}' missing host.")


def _validate_length(name: str, value: str) -> None:
    if len(value) > MAX_VALUE_LEN:
        raise ValidationError(
            f"{name} '{value[:30]}...' exceeds {MAX_VALUE_LEN} chars "
            f"(actual {len(value)})."
        )


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_campaign(client_slug: str, campaign_slug: str, month: str) -> str:
    _validate_slug(client_slug, "client-slug")
    _validate_slug(campaign_slug, "campaign-slug")
    _validate_month(month)
    return f"{client_slug}__{campaign_slug}__{month}"


def build_content(piece_id: str, variant: str | None = None) -> str:
    _validate_piece_id(piece_id)
    if variant is None or variant == "":
        return piece_id
    _validate_variant(variant)
    return f"{piece_id}__{variant}"


def build_url(
    *,
    url: str,
    source: str,
    medium: str,
    client_slug: str,
    campaign_slug: str,
    month: str,
    piece_id: str,
    variant: str | None = None,
    term: str | None = None,
) -> str:
    _validate_url(url)
    _validate_source(source)
    _validate_medium(medium)

    campaign = build_campaign(client_slug, campaign_slug, month)
    content = build_content(piece_id, variant)

    if medium in PAID_MEDIA and not term:
        # Soft warning; not error. Allow but note via stderr.
        print(
            "warning: paid medium without utm_term loses targeting attribution.",
            file=sys.stderr,
        )

    if term and medium not in PAID_MEDIA:
        # Allow but warn — convention says term is paid-only.
        print(
            f"warning: utm_term set on non-paid medium '{medium}'; "
            f"convention reserves term for paid.",
            file=sys.stderr,
        )

    if term:
        _validate_term(term)

    for n, v in [
        ("source", source),
        ("medium", medium),
        ("campaign", campaign),
        ("content", content),
    ]:
        _validate_length(n, v)
    if term:
        _validate_length("term", term)

    params = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
        "utm_content": content,
    }
    if term:
        params["utm_term"] = term

    # Use quote_via=quote so '__' is preserved (urlencode default would not encode underscore).
    suffix = urlencode(params, quote_via=quote, safe="_-")
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}{suffix}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a UTM-tagged URL using the BrandFlow agency-wide "
            "convention. See knowledge/marketing/utm-conventions.md."
        )
    )
    parser.add_argument("--url", required=True, help="Destination URL.")
    parser.add_argument("--source", required=True, help="utm_source (allowed list).")
    parser.add_argument("--medium", required=True, help="utm_medium (allowed list).")
    parser.add_argument("--client", required=True, help="Client slug (lowercase).")
    parser.add_argument(
        "--campaign-slug",
        required=True,
        help="Campaign slug (lowercase, hyphenated).",
    )
    parser.add_argument(
        "--month",
        required=True,
        help="Campaign start month YYYY-MM (e.g. 2026-05).",
    )
    parser.add_argument(
        "--content",
        required=True,
        help="Piece id (e.g. BF-acme-0142).",
    )
    parser.add_argument(
        "--variant",
        default=None,
        help="Optional variant suffix for A/B (e.g. hookA).",
    )
    parser.add_argument(
        "--term",
        default=None,
        help="utm_term (paid only; audience or keyword slug).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON {url, params} instead of plain URL.",
    )
    parser.add_argument(
        "--list-allowed",
        action="store_true",
        help="Print allowed sources and media, then exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if "--list-allowed" in argv:
        print("allowed sources:")
        for s in sorted(ALLOWED_SOURCES):
            print(f"  {s}")
        print("allowed source prefixes:")
        for p in ALLOWED_SOURCE_PREFIXES:
            print(f"  {p}<slug>")
        print("allowed media:")
        for m in sorted(ALLOWED_MEDIA):
            tag = "  (paid)" if m in PAID_MEDIA else ""
            print(f"  {m}{tag}")
        return 0

    try:
        args = _parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    try:
        url = build_url(
            url=args.url,
            source=args.source,
            medium=args.medium,
            client_slug=args.client,
            campaign_slug=args.campaign_slug,
            month=args.month,
            piece_id=args.content,
            variant=args.variant,
            term=args.term,
        )
    except ValidationError as e:
        print(f"validation-error: {e}", file=sys.stderr)
        return 1

    if args.json:
        # Re-derive params for the JSON view.
        out = {
            "url": url,
            "params": {
                "utm_source": args.source,
                "utm_medium": args.medium,
                "utm_campaign": build_campaign(
                    args.client, args.campaign_slug, args.month
                ),
                "utm_content": build_content(args.content, args.variant),
            },
        }
        if args.term:
            out["params"]["utm_term"] = args.term
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
