#!/usr/bin/env python3
"""Copy the rendered broadsheet to the grader output.

Stdlib only: the grader runs python3 -P -s in a bare image with no
Pillow and no network, so this file imports nothing beyond the
standard library. It reads the pre-rendered image shipped in the
repository, checks it is a whole PNG of the size the contest allows,
and writes the same bytes to /output/entry.png.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def fail(msg):
    sys.stderr.write("entry: %s\n" % msg)
    raise SystemExit(1)


def read_asset():
    try:
        with open(SRC, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (SRC, exc))
    if len(data) > MAX_BYTES:
        fail("image is %d bytes, over the 1048576 limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("image is not a PNG (bad magic bytes)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("image has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("image is %dx%d, over the 1024x1024 limit" % (width, height))
    if width < 1 or height < 1:
        fail("image has a zero dimension")
    if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
        fail("image has no IEND chunk (truncated PNG)")
    return data


def main():
    data = read_asset()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    os.chmod(dest, 0o644)
    print("wrote %s (%d bytes)" % (dest, len(data)))


if __name__ == "__main__":
    main()
