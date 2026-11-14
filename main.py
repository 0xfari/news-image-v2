#!/usr/bin/env python3
"""news-image-01 entry v2: a dense broadsheet summing up 13 November 2026.

The artwork lives in this repository as a base64 text file
(``entry.png.b64``) so the whole entry stays plain UTF-8, which is what
the submission tooling can push. At run time this program decodes that
file and writes the image out as ``entry.png`` inside the output
directory the grader points at (``$MAKEFUN_OUTPUT_DIR``, falling back
to ``/output``).

There is no network access, no randomness, and no dependency beyond
the standard library, so two runs of this program always produce
exactly the same bytes. Before writing, the decoded data is checked
for the PNG signature and the IHDR dimensions, so a corrupted payload
fails loudly instead of silently producing a broken file.

The picture itself: a newspaper front page for Friday 13 November
2026, "THE WORLD TODAY". The lead story is the FAA's nationwide
ground stop — every US departure held for four hours after an
air-traffic communications failure, 10,000 flights delayed and 2,500
cancelled, the second nationwide stop since 9/11. Below it a numbered
world map carries ten stories (Kyiv, Baltic, Gaza, Hormuz, Taiwan,
Jakarta, London, Lisbon, Assam, Nairobi), two sidebars cover Nvidia's
chief resigning and bitcoin sinking to $68,000, and the grid below
lists the rest of the day — 26 verified stories across five
continents, plus a markets strip (BTC, ETH, S&P, Nasdaq, NVDA, gold,
Brent). The image was drawn programmatically (render.py, Pillow) so
every word is perfectly legible.
"""

import base64
import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png.b64"
OUTPUT_NAME = "entry.png"
# A PNG starts with this 8-byte signature, then the IHDR chunk whose
# payload carries width and height (4 bytes each, big-endian).
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_DIMENSION = 1024
MAX_BYTES = 1_048_576


def output_directory() -> Path:
    """Where the grader wants the image (env var, else /output)."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def check_png_complete(data: bytes) -> None:
    """Walk the PNG chunk list and confirm the file ends at IEND.

    Each chunk is length (4 bytes) + type (4) + payload + CRC (4).
    A truncated payload stops mid-chunk or never reaches IEND, so
    this catches a cut-off file that the header checks alone miss.
    """
    pos = 8  # past the PNG signature
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError(f"truncated PNG: {chunk_type!r} chunk runs past the end")
        if chunk_type == b"IEND":
            if end != len(data):
                raise ValueError("trailing bytes after the PNG IEND chunk")
            return
        pos = end
    raise ValueError("no PNG IEND chunk found (file is truncated)")


def load_image_bytes() -> bytes:
    """Decode the stored artwork and sanity-check it is a PNG."""
    source = Path(__file__).resolve().parent / SOURCE_NAME
    text = source.read_text(encoding="ascii").strip()
    data = base64.b64decode(text, validate=True)
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("decoded payload is not a PNG (bad signature)")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("decoded payload is not a PNG (missing IHDR chunk)")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(f"image is {width}x{height}, over the 1024x1024 limit")
    check_png_complete(data)
    print(f"decoded PNG {width}x{height} ({len(data)} bytes)")
    return data


def write_entry(data: bytes) -> Path:
    """Write the image and report where it went and how big it is."""
    out_dir = output_directory()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes)")
    return target


def main() -> int:
    write_entry(load_image_bytes())
    return 0


if __name__ == "__main__":
    sys.exit(main())
