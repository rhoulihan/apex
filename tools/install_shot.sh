#!/bin/bash
# Install a captured screenshot into the workshop tree.
#   tools/install_shot.sh <lab-dir> <image-name.png> [source.jpg]
# With no source, uses the newest file in the Chrome extension's screenshot dir.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$1"; NAME="$2"
SRC="${3:-$(ls -t /var/folders/*/*/T/claude-chrome-screenshots-*/*.jpg 2>/dev/null | head -1)}"
[ -n "$SRC" ] && [ -f "$SRC" ] || { echo "no source screenshot found" >&2; exit 1; }
DEST="$REPO/ai-helpdesk-agent/$LAB/images/$NAME"
[ -d "$(dirname "$DEST")" ] || { echo "no such lab images dir: $(dirname "$DEST")" >&2; exit 1; }
sips -s format png "$SRC" --out "$DEST" >/dev/null
python3 - "$DEST" <<'PY'
import sys,os
p=sys.argv[1]; b=open(p,'rb').read()
assert b[:8]==b'\x89PNG\r\n\x1a\n', "not a PNG"
assert b'PLACEHOLDER-SCREENSHOT' not in b, "still a placeholder"
print(f"  installed {os.path.relpath(p)}  ({len(b)//1024} KB)")
PY
