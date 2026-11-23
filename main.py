#!/usr/bin/env python3
"""Entry point for the make.fun bounty news-image-20261123.

Copies the bundled front page (entry.png, 1024x1024 PNG, under 1 MiB)
to /output/entry.png. No network access, no randomness: every run
writes identical bytes. Validates the PNG signature and the size cap
before writing, and fails loudly if either check does not pass.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def main() -> int:
    if not os.path.isfile(SRC):
        print(f"entry.png not found next to main.py ({SRC})", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_SIGNATURE:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"wrote {DST} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
