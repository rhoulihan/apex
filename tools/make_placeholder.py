"""Write a gray placeholder PNG (with marker bytes) + caption text file.

Usage: python3 tools/make_placeholder.py <lab>/images/<name>.png "caption of the real screenshot"
The marker bytes PLACEHOLDER-SCREENSHOT make `validate_workshop.py --final` fail
until the real screenshot replaces the file.
"""
import struct
import sys
import zlib
from pathlib import Path


def png(w=400, h=250, rgb=(220, 222, 226)):
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"tEXt", b"Comment\x00PLACEHOLDER-SCREENSHOT")
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b""))


if __name__ == "__main__":
    out, caption = Path(sys.argv[1]), sys.argv[2]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png())
    out.with_suffix(".caption.txt").write_text(caption + "\n")
    print("placeholder:", out)
