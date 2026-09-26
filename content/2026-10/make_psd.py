"""Assemble layers/<slide>/ into psd/<post>/<slide>.psd with named layers in groups.

Text is rasterised: each headline, body line, tag and chip is its own positioned layer, but not live type.
"""
import json
import os
import sys

from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import Group, PixelLayer
from psd_tools.constants import Compression

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['Background', 'Photo', 'Brand', 'Text', 'Footer']  # bottom to top


def build(slide):
    src = os.path.join(HERE, 'layers', slide)
    layers = json.load(open(os.path.join(src, 'layers.json')))
    psd = PSDImage.new('RGBA', (1080, 1350), color=(255, 255, 255, 0))
    for group in ORDER:
        members = []
        for l in layers:
            if l['group'] != group:
                continue
            im = Image.open(os.path.join(src, l['file'])).convert('RGBA')
            px = PixelLayer.frompil(im, psd, l['name'][:250], l['top'], l['left'])
            psd.append(px)
            members.append(px)
        if members and group != 'Background':
            Group.group_layers(psd, members, name=group)
    post, nn = slide.split('-')
    # Flattened preview = the rendered slide, RLE-compressed (keeps files small, shows in Finder/Bridge).
    flat = Image.open(os.path.join(HERE, 'posts', post, nn + '.png')).convert('RGBA')
    psd._record.image_data.compression = Compression.RLE
    psd._record.image_data.set_data([c.tobytes() for c in flat.split()], psd._record.header)
    os.makedirs(os.path.join(HERE, 'psd', post), exist_ok=True)
    out = os.path.join(HERE, 'psd', post, slide + '.psd')
    psd.save(out)
    return out


if __name__ == '__main__':
    slides = sorted(d for d in os.listdir(os.path.join(HERE, 'layers')) if not sys.argv[1:] or d.startswith(sys.argv[1]))
    for s in slides:
        build(s)
    print('wrote', len(slides), 'PSDs')
