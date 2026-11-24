#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty news-image-20261123 (v2 final).

Takes the finished front page that ships beside this file and places
a copy at /output/entry.png. The program touches no network and uses
no randomness, so repeated runs write the same bytes every time. It
refuses to write anything unless the bundled file starts with the
PNG magic bytes and stays inside the competition's 1 MiB limit.
"""
from hashlib import sha256
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parent / "entry.png"
TARGET = Path("/output/entry.png")
MAGIC = b"\x89PNG\r\n\x1a\n"
LIMIT = 1024 * 1024


def run() -> int:
    if not SOURCE.is_file():
        print(f"cannot find the bundled page: {SOURCE}", file=sys.stderr)
        return 1
    blob = SOURCE.read_bytes()
    if blob[:8] != MAGIC:
        print("the bundled page is not a PNG file", file=sys.stderr)
        return 1
    if len(blob) > LIMIT:
        print(f"the bundled page is {len(blob)} bytes, past the 1 MiB cap",
              file=sys.stderr)
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(blob)
    print(f"wrote {TARGET} ({len(blob)} bytes, sha256 {sha256(blob).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
