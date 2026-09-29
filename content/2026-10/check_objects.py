"""Check that no text on a cover sits on its object: tests each text box (from render.js) against the object's alpha.

    python3 check_objects.py     # prints any clash; exit code 1 if there is one
"""
import glob
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAD = 16  # breathing room around text, in canvas px


def main():
    clashes = 0
    for f in sorted(glob.glob(os.path.join(HERE, 'objects', 'boxes', '*.json'))):
        post = os.path.basename(f)[:-5]
        alpha = np.asarray(Image.open(os.path.join(HERE, 'objects', post + '.png')).convert('RGBA').resize((1080, 1350)))[..., 3]
        solid = alpha > 96  # the object itself; its soft floor shadow may run under text
        for b in json.load(open(f)):
            x0, y0 = max(0, int(b['x']) - PAD), max(0, int(b['y']) - PAD)
            x1, y1 = min(1080, int(b['x'] + b['w']) + PAD), min(1350, int(b['y'] + b['h']) + PAD)
            n = int(solid[y0:y1, x0:x1].sum())
            if n:
                clashes += 1
                print(f'{post}: "{b["text"]}" overlaps the object ({n} px)')
        ys, xs = np.nonzero(solid)
        print(f'{post}: object spans x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}')
    return 1 if clashes else 0


if __name__ == '__main__':
    sys.exit(main())
