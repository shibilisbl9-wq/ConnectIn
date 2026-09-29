#!/usr/bin/env bash
# Render the cover objects into objects/<post>.png: transparent 2160 x 2700 frames holding the object and its floor
# shadow, from the same studio and camera as the brand moodboard and the registered-mark post.
# Needs `npm install` in brand/moodboard/src (three, playwright) and a Playwright Chromium.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../../brand"
PORT="${PORT:-8765}"
export PORT
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER' EXIT
sleep 1

mkdir -p "$HERE/objects"
C="s=cover&alpha=1&vsm=1&w=2160&h=2700&nk=0.3&nc=062a45&ox=0.39&mw=0.85&mh=1.1&ly=0.85"
node moodboard/src/shoot.js \
  moodboard/src/scene.html "$C&o=hourglass&face=3" "$HERE/objects/P01.png" \
  moodboard/src/scene.html "$C&o=signpost&face=1.5" "$HERE/objects/P03.png" \
  moodboard/src/scene.html "$C&o=card&face=1.5" "$HERE/objects/P05.png" \
  moodboard/src/scene.html "$C&o=scale&face=3" "$HERE/objects/P07.png" \
  moodboard/src/scene.html "$C&o=tower&face=3" "$HERE/objects/P10.png" \
  moodboard/src/scene.html "$C&o=question&face=6" "$HERE/objects/P12.png"
