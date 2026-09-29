"""Paint the mist studio ground for each post: one continuous image per carousel, so the light runs across the swipe.

It matches the studio the 3D objects are rendered in (brand/moodboard/src/scene.html): wall a little darker at the top,
brightest where wall meets floor, and soft window-blind light falling across the upper half. Patches straddle the slide
seams, so each slide hands its light to the next one.

    python3 paint_studio.py     # writes studio/<post>.png (n x 1080 wide, 1350 high)
"""
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
SW, SH = 1080, 1350

# wall-to-floor gradient sampled from the registered-mark render (y as a fraction of the height)
STOPS = [(0.0, '#e0e9f0'), (0.22, '#e5eef5'), (0.5, '#e7f0f7'), (0.74, '#e6eff6'), (1.0, '#e3ecf3')]
LIGHT = np.array([0xf6, 0xf9, 0xfc], dtype=np.float32)  # blind light: near-white, a touch warmer than the wall


def hex3(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32)


def ground(width):
    ys = np.linspace(0, 1, SH)
    col = np.zeros((SH, 3), np.float32)
    for c in range(3):
        col[:, c] = np.interp(ys, [s for s, _ in STOPS], [hex3(h)[c] for _, h in STOPS])
    return np.repeat(col[:, None, :], width, axis=1)


def blinds(width, centres, rng):
    """Soft diagonal slats of light inside a feathered window shape, one patch per centre."""
    yy, xx = np.mgrid[0:SH, 0:width].astype(np.float32)
    total = np.zeros((SH, width), np.float32)
    for cx, cy in centres:
        w, h = rng.uniform(820, 1000), rng.uniform(520, 640)
        ang = np.deg2rad(rng.uniform(-30, -22))
        # rotate into the slat frame
        u = (xx - cx) * np.cos(ang) + (yy - cy) * np.sin(ang)
        v = -(xx - cx) * np.sin(ang) + (yy - cy) * np.cos(ang)
        window = np.exp(-(np.maximum(np.abs(u) - w / 2, 0) / 90) ** 2) * np.exp(-(np.maximum(np.abs(v) - h / 2, 0) / 70) ** 2)
        window *= (np.abs(u) < w / 2 + 300) & (np.abs(v) < h / 2 + 240)
        period, open_ = 62, 0.55
        slats = ((v % period) / period) < open_
        total = np.maximum(total, window * slats * rng.uniform(0.55, 0.75))
    return gaussian_filter(total, 5)


def paint(post_id, n, daylight, seed):
    width = n * SW
    rng = np.random.default_rng(seed)
    img = ground(width)
    # a patch across every seam between two daylight slides, plus one on a daylight slide with no daylight neighbour
    centres = []
    for i in range(n):
        if not daylight[i]:
            continue
        if i + 1 < n and daylight[i + 1]:
            centres.append(((i + 1) * SW - rng.uniform(40, 160), rng.uniform(300, 420)))
        elif i == 0 or not daylight[i - 1]:
            centres.append((i * SW + rng.uniform(760, 880), rng.uniform(320, 420)))
    a = blinds(width, centres, rng)[..., None] * 0.62
    img = img * (1 - a) + LIGHT * a
    out = np.clip(np.round(img), 0, 255).astype(np.uint8)
    os.makedirs(os.path.join(HERE, 'studio'), exist_ok=True)
    Image.fromarray(out, 'RGB').save(os.path.join(HERE, 'studio', f'{post_id}.png'), optimize=True)
    return width


if __name__ == '__main__':
    posts = json.load(open(os.path.join(HERE, 'posts.json')))['posts']
    for k, p in enumerate(posts):
        daylight = [s == 'daylight' for s in p['themes']]
        if any(daylight):
            print(p['id'], paint(p['id'], len(p['slides']), daylight, seed=101 + k))
