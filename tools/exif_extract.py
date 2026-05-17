#!/usr/bin/env python3
"""
exif_extract.py — Extract EXIF metadata from image files (local, no network).

Reads JPEG/TIFF EXIF tags using stdlib + minimal manual parser. Returns
structured fields including GPS, timestamps, device info.

Useful for OSINT / investigation workflows where a photo's metadata reveals
the source (per `knowledge/scope/declined-tools.md` — substitute for face
recognition tooling).

Usage:
    tools/exif_extract.py photo.jpg
    tools/exif_extract.py photo.jpg --json
    tools/exif_extract.py *.jpg

Risk: Low (read-only local FS, no network).

Used by: `@nexusai.security`, `@nexusai.automation`, OSINT investigations.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any

# Try Pillow for full EXIF; otherwise minimal manual parser.
try:
    from PIL import Image, ExifTags  # type: ignore[import-untyped]
    HAVE_PILLOW = True
except ImportError:
    HAVE_PILLOW = False


# ---------------------------------------------------------------------------
# Pillow path (preferred)
# ---------------------------------------------------------------------------

def _pillow_extract(path: Path) -> dict[str, Any]:
    img = Image.open(path)
    out: dict[str, Any] = {
        "format":   img.format,
        "mode":     img.mode,
        "size":     {"width": img.width, "height": img.height},
        "exif":     {},
        "gps":      None,
    }
    raw = img.getexif()
    if not raw:
        return out

    name_for_tag = ExifTags.TAGS
    name_for_gps = ExifTags.GPSTAGS

    for tag_id, val in raw.items():
        name = name_for_tag.get(tag_id, f"tag_{tag_id}")
        out["exif"][name] = _scrub(val)

    gps_info = raw.get_ifd(0x8825) if hasattr(raw, "get_ifd") else None
    if gps_info:
        gps: dict[str, Any] = {}
        for k, v in gps_info.items():
            gps[name_for_gps.get(k, f"gps_{k}")] = _scrub(v)
        out["gps"] = _gps_to_decimal(gps)
        out["gps_raw"] = gps

    return out


def _scrub(v: Any) -> Any:
    """Make values JSON-serializable."""
    if isinstance(v, bytes):
        try:
            return v.decode("utf-8", errors="replace").rstrip("\x00").strip()
        except Exception:
            return v.hex()
    if isinstance(v, (list, tuple)):
        return [_scrub(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _scrub(x) for k, x in v.items()}
    if hasattr(v, "numerator") and hasattr(v, "denominator"):
        try:
            return float(v) if v.denominator else None
        except Exception:
            return str(v)
    return v


def _gps_to_decimal(gps: dict[str, Any]) -> dict[str, Any] | None:
    """Convert GPS DMS to decimal lat/lon, with hemisphere applied."""
    try:
        lat_dms = gps.get("GPSLatitude")
        lat_ref = gps.get("GPSLatitudeRef", "N")
        lon_dms = gps.get("GPSLongitude")
        lon_ref = gps.get("GPSLongitudeRef", "E")
        if not (lat_dms and lon_dms):
            return None

        def to_dec(dms: list, ref: str) -> float:
            d, m, s = dms[0], dms[1], dms[2]
            d = float(d) if not hasattr(d, "numerator") else float(d)
            m = float(m) if not hasattr(m, "numerator") else float(m)
            s = float(s) if not hasattr(s, "numerator") else float(s)
            dec = d + m / 60.0 + s / 3600.0
            if ref in ("S", "W"):
                dec = -dec
            return dec

        return {
            "latitude":  to_dec(lat_dms, lat_ref),
            "longitude": to_dec(lon_dms, lon_ref),
            "altitude":  float(gps["GPSAltitude"]) if "GPSAltitude" in gps else None,
            "timestamp": gps.get("GPSTimeStamp"),
            "datestamp": gps.get("GPSDateStamp"),
        }
    except (TypeError, ValueError, IndexError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Stdlib fallback (JPEG / TIFF only, common tags)
# ---------------------------------------------------------------------------

# Minimal subset for the fallback. Pillow path covers more.
_FALLBACK_TAGS = {
    0x010F: "Make",
    0x0110: "Model",
    0x0112: "Orientation",
    0x011A: "XResolution",
    0x011B: "YResolution",
    0x0128: "ResolutionUnit",
    0x0131: "Software",
    0x0132: "DateTime",
    0x013B: "Artist",
    0x013E: "WhitePoint",
    0x8769: "ExifIFDPointer",
    0x8825: "GPSIFDPointer",
    0x9003: "DateTimeOriginal",
    0x9004: "DateTimeDigitized",
}


def _fallback_extract(path: Path) -> dict[str, Any]:
    """Parse JPEG APP1 EXIF segment manually. Returns top-level tags only.

    Limitations: no GPS decoding; only the first IFD; only common tag IDs.
    Use Pillow for full support.
    """
    out: dict[str, Any] = {
        "format":            None,
        "size":              None,
        "exif":              {},
        "fallback_warning":  "Pillow not installed; only basic top-level EXIF tags read.",
    }
    try:
        with path.open("rb") as fh:
            data = fh.read()
    except OSError as e:
        return {"error": f"cannot read: {e}"}

    if not data.startswith(b"\xFF\xD8"):
        out["error"] = "not a JPEG (fallback supports JPEG only)"
        return out
    out["format"] = "JPEG"

    # Find APP1 segment with "Exif\x00\x00" header
    i = 2
    while i < len(data) - 4:
        if data[i] != 0xFF:
            break
        marker = data[i+1]
        if marker == 0xD9:
            break
        seg_len = struct.unpack(">H", data[i+2:i+4])[0]
        if marker == 0xE1 and data[i+4:i+10] == b"Exif\x00\x00":
            return _parse_tiff_block(data, i+10, seg_len-8, out)
        i += 2 + seg_len

    out["exif"] = {}
    return out


def _parse_tiff_block(data: bytes, start: int, length: int,
                      out: dict[str, Any]) -> dict[str, Any]:
    block = data[start : start+length]
    if len(block) < 8:
        return out
    endian = block[0:2]
    if endian == b"II":
        fmt = "<"
    elif endian == b"MM":
        fmt = ">"
    else:
        return out
    magic, ifd0_off = struct.unpack(fmt + "HI", block[2:8])
    if magic != 0x002A:
        return out
    if ifd0_off >= len(block):
        return out

    n = struct.unpack(fmt + "H", block[ifd0_off : ifd0_off+2])[0]
    pos = ifd0_off + 2
    for _ in range(n):
        if pos + 12 > len(block):
            break
        tag, ttype, count, value_off = struct.unpack(
            fmt + "HHII", block[pos : pos+12])
        pos += 12
        name = _FALLBACK_TAGS.get(tag)
        if not name:
            continue
        if ttype == 2:  # ASCII
            try:
                if count <= 4:
                    raw = struct.pack(fmt + "I", value_off)[:count]
                else:
                    raw = block[value_off : value_off+count]
                out["exif"][name] = raw.rstrip(b"\x00").decode(
                    "utf-8", errors="replace").strip()
            except Exception:
                out["exif"][name] = "<unreadable>"
        elif ttype == 3 and count == 1:  # SHORT
            out["exif"][name] = value_off & 0xFFFF
        elif ttype == 4 and count == 1:  # LONG
            out["exif"][name] = value_off
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def extract(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"error": f"not a file: {path}"}
    if HAVE_PILLOW:
        try:
            return _pillow_extract(path)
        except Exception as e:  # PIL throws many exception types
            return {"error": f"pillow extract failed: {e}"}
    return _fallback_extract(path)


def render_human(path: Path, data: dict[str, Any]) -> str:
    lines = [f"=== {path} ==="]
    if "error" in data:
        lines.append(f"  ERROR: {data['error']}")
        return "\n".join(lines)
    if data.get("fallback_warning"):
        lines.append(f"  note: {data['fallback_warning']}")
    if data.get("size"):
        s = data["size"]
        lines.append(f"  format: {data.get('format')}  size: {s['width']}×{s['height']}")
    if data.get("gps"):
        g = data["gps"]
        lines.append(f"  GPS:    {g.get('latitude'):.6f}, {g.get('longitude'):.6f}"
                     f"  alt={g.get('altitude')}  ts={g.get('timestamp')}")
    if data.get("exif"):
        keys_of_interest = (
            "Make", "Model", "Software", "DateTimeOriginal", "DateTime",
            "DateTimeDigitized", "Artist", "ImageDescription", "GPSDateStamp",
        )
        for k in keys_of_interest:
            if k in data["exif"]:
                lines.append(f"  {k:<22}{data['exif'][k]}")
        # Show count of all tags
        lines.append(f"  ({len(data['exif'])} EXIF tags total)")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Extract EXIF metadata from image files.")
    p.add_argument("paths", nargs="+", help="Image file(s).")
    p.add_argument("--json", action="store_true",
                   help="JSON output.")
    args = p.parse_args()

    results: list[tuple[Path, dict[str, Any]]] = []
    for arg in args.paths:
        path = Path(arg)
        results.append((path, extract(path)))

    if args.json:
        print(json.dumps(
            [{"path": str(p), "data": d} for p, d in results],
            ensure_ascii=False, indent=2,
        ))
    else:
        for path, data in results:
            print(render_human(path, data))
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
