#!/usr/bin/env python3
"""
api_health.py — Single-endpoint health check + latency report.

Hits one HTTP endpoint, reports status code, latency, and basic checks.
Useful for quick "is my service up?" or pre-deploy smoke tests.

Usage:
    tools/api_health.py https://api.example.com/health
    tools/api_health.py https://api.example.com/v1/ping --expect-status 200
    tools/api_health.py https://api.example.com/me --header 'Authorization: Bearer X'
    tools/api_health.py https://api.example.com/v1 --runs 5 --json

Risk: Low (single GET against a single URL passed in by user; no write).

Used by: `@nexusai.devops`, `@nexusai.qa`, smoke tests after deploy.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib import error, request


def fetch_once(url: str,
               headers: dict[str, str],
               timeout: float) -> dict[str, Any]:
    req = request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)

    t0 = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return {
                "ok": True,
                "status": resp.status,
                "latency_ms": round(latency_ms, 2),
                "headers": dict(resp.headers),
                "body_bytes": len(body),
                "body_preview": body[:200].decode("utf-8", errors="replace"),
            }
    except error.HTTPError as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        body = e.read() if hasattr(e, "read") else b""
        return {
            "ok": False,
            "status": e.code,
            "latency_ms": round(latency_ms, 2),
            "headers": dict(e.headers) if e.headers else {},
            "body_bytes": len(body),
            "body_preview": body[:200].decode("utf-8", errors="replace"),
            "error": "http_error",
        }
    except error.URLError as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "ok":         False,
            "status":     None,
            "latency_ms": round(latency_ms, 2),
            "error":      "url_error",
            "reason":     str(e.reason),
        }
    except (TimeoutError, OSError) as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "ok":         False,
            "status":     None,
            "latency_ms": round(latency_ms, 2),
            "error":      "timeout_or_io",
            "reason":     str(e),
        }


def parse_headers(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if ":" not in item:
            raise ValueError(f"--header must be 'Name: Value', got: {item!r}")
        k, v = item.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    p = argparse.ArgumentParser(
        description="Single-endpoint health check + latency report.")
    p.add_argument("url", help="URL to GET.")
    p.add_argument("--expect-status", type=int, default=None,
                   help="Required status code; nonzero exit if mismatched.")
    p.add_argument("--expect-substring", default=None,
                   help="Required substring in response body.")
    p.add_argument("--max-latency-ms", type=float, default=None,
                   help="Latency threshold; nonzero exit if exceeded "
                        "(p95 if --runs > 1).")
    p.add_argument("--header", action="append", default=[],
                   help="Header line. Repeat for multiple. Format: 'Name: Value'.")
    p.add_argument("--runs", type=int, default=1,
                   help="Number of fetches; reports min/p50/p95/max latency "
                        "(default 1).")
    p.add_argument("--timeout", type=float, default=10.0,
                   help="Per-request timeout seconds (default 10).")
    p.add_argument("--json", action="store_true",
                   help="JSON output instead of human report.")
    args = p.parse_args()

    if not (args.url.startswith("http://") or args.url.startswith("https://")):
        print("ERROR: URL must start with http:// or https://", file=sys.stderr)
        return 2

    if args.runs < 1 or args.runs > 100:
        print("ERROR: --runs must be 1..100", file=sys.stderr)
        return 2

    try:
        headers = parse_headers(args.header)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    results = [fetch_once(args.url, headers, args.timeout) for _ in range(args.runs)]

    latencies = [r["latency_ms"] for r in results]
    latencies_sorted = sorted(latencies)
    n = len(latencies_sorted)

    summary = {
        "url":           args.url,
        "runs":          args.runs,
        "ok_count":      sum(1 for r in results if r.get("ok")),
        "fail_count":    sum(1 for r in results if not r.get("ok")),
        "latency_min":   min(latencies),
        "latency_p50":   latencies_sorted[n // 2],
        "latency_p95":   latencies_sorted[min(n - 1, int(n * 0.95))],
        "latency_max":   max(latencies),
        "first_status":  results[0].get("status"),
        "first_body_preview": results[0].get("body_preview"),
    }

    issues: list[str] = []
    if args.expect_status is not None and summary["first_status"] != args.expect_status:
        issues.append(
            f"expected status {args.expect_status}, "
            f"got {summary['first_status']}"
        )
    if args.expect_substring is not None and (
        not results[0].get("body_preview")
        or args.expect_substring not in results[0].get("body_preview", "")
    ):
        issues.append(
            f"expected substring {args.expect_substring!r} not in body preview"
        )
    if args.max_latency_ms is not None and summary["latency_p95"] > args.max_latency_ms:
        issues.append(
            f"p95 latency {summary['latency_p95']}ms > {args.max_latency_ms}ms"
        )

    summary["issues"] = issues

    if args.json:
        print(json.dumps({"summary": summary, "results": results},
                         ensure_ascii=False, indent=2))
    else:
        print(f"=== {args.url} ===")
        print(
            f"runs:     {summary['runs']}  "
            f"ok={summary['ok_count']} fail={summary['fail_count']}"
        )
        print(f"status:   {summary['first_status']}")
        print(
            f"latency:  min={summary['latency_min']}ms  "
            f"p50={summary['latency_p50']}ms  "
            f"p95={summary['latency_p95']}ms  "
            f"max={summary['latency_max']}ms"
        )
        if results[0].get("body_preview"):
            print(f"body:     {summary['first_body_preview']!r}")
        if issues:
            print("\nISSUES:")
            for it in issues:
                print(f"  - {it}")
        else:
            print("\nOK")

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
