#!/usr/bin/env python3
"""
readability_check.py — Readability + structure scan for BrandFlow drafts.

Reports:
  - Flesch Reading Ease score (English approximation; for Indonesian text
    treats it as a directional metric, not authoritative)
  - Average sentence length, sentence-length distribution
  - Average word length
  - Paragraph length stats
  - Adverb density, passive-voice signals (English-only heuristics)
  - Filler word density ("really", "very", "just", "actually", "basically")
  - Per-channel length compliance check (IG / LinkedIn / X / email subject / blog title)
  - Hook-zone read (first 1-2 sentences) length & strength signals

For long-form (blog/article), runs SEO structure checks too:
  - H1/H2/H3 hierarchy
  - Image alt-text presence (in markdown)
  - Internal/external link counts

Tier:    Update 11 (BrandFlow deepening)
Risk:    Low (read-only stdin/file)
Status:  Active

Usage:
    python3 readability_check.py FILE [FILE...] [--channel ig|linkedin|x|email-subj|blog]
    python3 readability_check.py --stdin --channel linkedin
    python3 readability_check.py --stdin --json

Exit codes:
    0   no issues
    1   issues found (e.g. exceeds channel cap, missing structure)
    2   argument or IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHANNEL_LIMITS = {
    # value: (soft_max_chars, hard_max_chars, label)
    "ig":         (140, 2200, "Instagram caption (140 char hook visible; 2200 hard cap)"),
    "linkedin":   (210, 3000, "LinkedIn post (210 char before 'see more'; 3000 hard cap)"),
    "x":          (260, 280,  "X / Twitter (single tweet)"),
    "email-subj": (50,  78,   "Email subject (50 char mobile preview; 78 hard ceiling)"),
    "email-pre":  (90,  120,  "Email preheader (90 char ideal)"),
    "blog-title": (60,  70,   "Blog title (60 char SERP cap)"),
    "blog":       (1500, 5000, "Blog body word range — soft 1500 words; hard 5000 word ceiling"),
}

FILLER_WORDS = {
    "really", "very", "just", "actually", "basically", "literally",
    "totally", "definitely", "kind of", "sort of",
    "in order to", "as a matter of fact",
}

# English passive-voice indicator patterns
PASSIVE_INDICATORS = re.compile(
    r"\b(am|is|are|was|were|be|being|been)\s+\w+(ed|en)\b",
    re.IGNORECASE,
)

# English adverb signal (-ly suffix). Indonesian: limited utility.
ADVERB_LY = re.compile(r"\b\w+ly\b", re.IGNORECASE)

# Sentence boundary heuristic
SENT_SPLIT = re.compile(r"(?<=[\.\!\?])\s+|\n{2,}")

# Word splitter
WORD_SPLIT = re.compile(r"\b[\w']+\b", re.UNICODE)

# Markdown patterns
MD_H1 = re.compile(r"^#\s+", re.MULTILINE)
MD_H2 = re.compile(r"^##\s+", re.MULTILINE)
MD_H3 = re.compile(r"^###\s+", re.MULTILINE)
MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MD_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)")


# ---------------------------------------------------------------------------
# Syllable counter (English heuristic; directional only for ID)
# ---------------------------------------------------------------------------

def _count_syllables(word: str) -> int:
    word = word.lower().strip("'")
    if not word:
        return 0
    vowels = "aeiouy"
    count = 0
    prev = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev:
            count += 1
        prev = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def flesch_reading_ease(text: str) -> float:
    sents = [s for s in SENT_SPLIT.split(text) if s.strip()]
    words = WORD_SPLIT.findall(text)
    if not sents or not words:
        return 0.0
    syllables = sum(_count_syllables(w) for w in words)
    asl = len(words) / len(sents)
    asw = syllables / len(words)
    return round(206.835 - 1.015 * asl - 84.6 * asw, 2)


def flesch_label(score: float) -> str:
    if score >= 90:
        return "very easy (5th grade)"
    if score >= 80:
        return "easy (6th grade)"
    if score >= 70:
        return "fairly easy (7th grade)"
    if score >= 60:
        return "plain (8-9th grade)"
    if score >= 50:
        return "fairly difficult (10-12th grade)"
    if score >= 30:
        return "difficult (college)"
    return "very difficult (college graduate+)"


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(text: str, *, channel: str | None = None, is_markdown: bool = False) -> dict:
    issues: list[dict] = []

    sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    words = WORD_SPLIT.findall(text)
    paragraphs = [p for p in re.split(r"\n{2,}", text) if p.strip()]
    chars = len(text)

    # Basic stats
    n_sents = len(sents)
    n_words = len(words)
    n_paras = len(paragraphs)
    avg_sent_len = round(n_words / n_sents, 2) if n_sents else 0
    avg_word_len = (
        round(sum(len(w) for w in words) / n_words, 2) if n_words else 0
    )

    # Sentence-length distribution buckets
    sent_lens = [len(WORD_SPLIT.findall(s)) for s in sents]
    short = sum(1 for n in sent_lens if n <= 8)
    medium = sum(1 for n in sent_lens if 9 <= n <= 20)
    long_ = sum(1 for n in sent_lens if n > 20)

    # Readability score (English-leaning; directional only for ID)
    flesch = flesch_reading_ease(text)

    # Filler / adverb / passive scans (English-leaning)
    filler_count = 0
    for fw in FILLER_WORDS:
        # word-boundary match for single-word fillers; substring for multi-word
        if " " in fw:
            filler_count += text.lower().count(fw)
        else:
            filler_count += len(re.findall(rf"\b{re.escape(fw)}\b", text, re.I))
    adverb_count = len(ADVERB_LY.findall(text))
    passive_count = len(PASSIVE_INDICATORS.findall(text))

    # Hook zone analysis (first 1-2 sentences or first 250 chars)
    hook = " ".join(sents[:2]) if sents else text[:250]
    hook_chars = len(hook)
    hook_words = len(WORD_SPLIT.findall(hook))

    # Channel-compliance
    channel_check = None
    if channel and channel in CHANNEL_LIMITS:
        soft, hard, label = CHANNEL_LIMITS[channel]
        if channel == "blog":
            # blog uses word count
            metric = n_words
            metric_name = "words"
        else:
            metric = chars
            metric_name = "chars"
        channel_check = {
            "channel": channel,
            "label": label,
            "metric": metric,
            "metric_name": metric_name,
            "soft_limit": soft,
            "hard_limit": hard,
            "status": (
                "OK"
                if metric <= soft
                else "WARN"
                if metric <= hard
                else "FAIL"
            ),
        }
        if metric > hard:
            issues.append({
                "severity": "blocker",
                "msg": f"{label}: {metric} {metric_name} exceeds hard cap {hard}",
            })
        elif metric > soft:
            issues.append({
                "severity": "warn",
                "msg": f"{label}: {metric} {metric_name} exceeds soft cap {soft}",
            })

    # Sentence rhythm advisory
    if n_sents >= 5 and short < n_sents * 0.2:
        issues.append({
            "severity": "minor",
            "msg": (
                f"Few short sentences (<= 8 words): {short} / {n_sents}. "
                "Consider mixing in shorter punches for rhythm."
            ),
        })
    if avg_sent_len > 25:
        issues.append({
            "severity": "warn",
            "msg": f"Avg sentence length {avg_sent_len} words > 25; reads dense.",
        })

    # Filler advisory
    if n_words and filler_count / n_words > 0.02:
        issues.append({
            "severity": "minor",
            "msg": (
                f"Filler density {filler_count}/{n_words} "
                f"({round(100 * filler_count / n_words, 1)}%). "
                "Cut filler in revision."
            ),
        })

    # Markdown / blog structure checks
    structure = None
    if is_markdown:
        h1 = len(MD_H1.findall(text))
        h2 = len(MD_H2.findall(text))
        h3 = len(MD_H3.findall(text))
        images = MD_IMG.findall(text)
        links = MD_LINK.findall(text)
        images_without_alt = [src for alt, src in images if not alt.strip()]
        structure = {
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "images": len(images),
            "images_without_alt": len(images_without_alt),
            "links": len(links),
        }
        if h1 != 1:
            issues.append({
                "severity": "warn" if h1 == 0 else "minor",
                "msg": f"Markdown should have exactly 1 H1 (found {h1}).",
            })
        if h2 < 2 and channel == "blog":
            issues.append({
                "severity": "warn",
                "msg": f"Blog body has only {h2} H2 sections; consider more skim-anchors.",
            })
        if images_without_alt:
            issues.append({
                "severity": "minor",
                "msg": f"{len(images_without_alt)} image(s) without alt text.",
            })

    return {
        "stats": {
            "chars": chars,
            "words": n_words,
            "sentences": n_sents,
            "paragraphs": n_paras,
            "avg_sentence_words": avg_sent_len,
            "avg_word_chars": avg_word_len,
            "sentence_dist": {
                "short_<=8": short,
                "medium_9-20": medium,
                "long_>20": long_,
            },
        },
        "flesch": {
            "score": flesch,
            "label": flesch_label(flesch),
            "note": "English-leaning heuristic; directional only for non-English text.",
        },
        "rhythm": {
            "filler_count": filler_count,
            "adverb_ly_count": adverb_count,
            "passive_indicator_count": passive_count,
        },
        "hook_zone": {
            "chars": hook_chars,
            "words": hook_words,
            "preview": hook[:160] + ("..." if len(hook) > 160 else ""),
        },
        "channel_check": channel_check,
        "structure": structure,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_human(path: str, result: dict) -> str:
    lines: list[str] = []
    lines.append(f"== readability: {path} ==")
    s = result["stats"]
    lines.append(
        f"chars={s['chars']}  words={s['words']}  sents={s['sentences']}  "
        f"paras={s['paragraphs']}  avg_sent_words={s['avg_sentence_words']}  "
        f"avg_word_chars={s['avg_word_chars']}"
    )
    sd = s["sentence_dist"]
    lines.append(
        f"sentence-dist: short={sd['short_<=8']} "
        f"medium={sd['medium_9-20']} long={sd['long_>20']}"
    )
    f = result["flesch"]
    lines.append(f"flesch={f['score']} ({f['label']})")
    r = result["rhythm"]
    lines.append(
        f"rhythm: filler={r['filler_count']} adverb_ly={r['adverb_ly_count']} "
        f"passive={r['passive_indicator_count']}"
    )
    h = result["hook_zone"]
    lines.append(f"hook-zone: {h['chars']}c / {h['words']}w  preview: {h['preview']}")
    if result["channel_check"]:
        cc = result["channel_check"]
        lines.append(
            f"channel: {cc['label']}  metric={cc['metric']} {cc['metric_name']}  "
            f"soft={cc['soft_limit']} hard={cc['hard_limit']}  status={cc['status']}"
        )
    if result["structure"]:
        st = result["structure"]
        lines.append(
            f"structure: h1={st['h1']} h2={st['h2']} h3={st['h3']} "
            f"img={st['images']} (no-alt={st['images_without_alt']}) "
            f"links={st['links']}"
        )
    if result["issues"]:
        lines.append("issues:")
        for i in result["issues"]:
            lines.append(f"  [{i['severity']}] {i['msg']}")
    else:
        lines.append("issues: none")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Readability + structure scan for BrandFlow drafts. "
            "See knowledge/marketing/social-platform-specs.md for channel limits."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files to analyze (markdown / plain text). Empty + --stdin reads stdin.",
    )
    parser.add_argument(
        "--channel",
        choices=sorted(CHANNEL_LIMITS.keys()),
        default=None,
        help="Channel for length-cap compliance check.",
    )
    parser.add_argument(
        "--stdin", action="store_true", help="Read text from stdin."
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON instead of text."
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Treat input as markdown (run structure checks).",
    )
    args = parser.parse_args(argv)

    inputs: list[tuple[str, str]] = []  # (label, content)

    if args.stdin or not args.paths:
        try:
            text = sys.stdin.read()
        except KeyboardInterrupt:
            return 2
        if not text:
            print("error: no input (use FILE or --stdin)", file=sys.stderr)
            return 2
        inputs.append(("<stdin>", text))
    else:
        for p in args.paths:
            try:
                content = Path(p).read_text(encoding="utf-8")
            except OSError as e:
                print(f"error: cannot read {p}: {e}", file=sys.stderr)
                return 2
            inputs.append((p, content))

    is_md = args.markdown or any(
        label.endswith((".md", ".markdown")) for label, _ in inputs
    )

    overall_exit = 0
    results: list[dict] = []
    for label, content in inputs:
        result = analyze(content, channel=args.channel, is_markdown=is_md)
        results.append({"path": label, **result})
        for issue in result["issues"]:
            if issue["severity"] in ("blocker", "warn"):
                overall_exit = 1

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(_format_human(r["path"], r))
            print()

    return overall_exit


if __name__ == "__main__":
    raise SystemExit(main())
