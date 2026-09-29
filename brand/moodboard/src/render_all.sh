#!/usr/bin/env bash
# Re-render the moodboard: 3D stills and materials into ../img/, then both boards to PNG.
# Needs: `npm install` in this folder (three, playwright), a Playwright Chromium, Python 3 with Pillow.
set -euo pipefail
cd "$(dirname "$0")/../.."   # brand/: the boards reference ../fonts and ../assets
PORT="${PORT:-8765}"
export PORT
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER' EXIT
sleep 1

SRC=moodboard/src
mkdir -p "$SRC/raw"
node "$SRC/shoot.js" \
  "$SRC/scene.html" "s=capsule&w=2256&h=2058&face=6&vsm=1&map=512&rad=18" "$SRC/raw/capsule.png" \
  "$SRC/scene.html" "s=chess&w=1104&h=2058" "$SRC/raw/chess.png" \
  "$SRC/scene.html" "s=towers&w=1104&h=2058&key=3.2&fill=0.3&cy=0.9&ly=10&fog=0.03" "$SRC/raw/towers.png" \
  "$SRC/scene.html" "s=paper&w=1104&h=2058&cx=0.1&cy=3.5&cz=2.4&lx=0.1&lz=0.05&fov=32" "$SRC/raw/paper.png" \
  "$SRC/textures.html" "t=twill&w=736&h=670" "$SRC/raw/twill.png" \
  "$SRC/textures.html" "t=brass&w=736&h=670" "$SRC/raw/brass.png" \
  "$SRC/textures.html" "t=marble&w=736&h=670" "$SRC/raw/marble.png" \
  "$SRC/textures.html" "t=emboss&w=736&h=670" "$SRC/raw/emboss.png"

# The stills render at 1.5x and come down with Lanczos for clean edges; everything ships as JPEG.
python3 - <<'EOF'
from PIL import Image
size = {"capsule": (1504, 1372), "chess": (736, 1372), "towers": (736, 1372), "paper": (736, 1372)}
for n in ["capsule", "chess", "towers", "paper", "twill", "brass", "marble", "emboss"]:
    im = Image.open(f"moodboard/src/raw/{n}.png").convert("RGB")
    if n in size:
        im = im.resize(size[n], Image.LANCZOS)
    im.save(f"moodboard/img/{n}.jpg", quality=90, optimize=True, progressive=True)
EOF

node "$SRC/snap.js" moodboard/moodboard.html moodboard/moodboard.png
node "$SRC/snap.js" moodboard/direction.html moodboard/direction.png
