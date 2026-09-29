"""Assemble layers/<slide>/ into one PSD per post: psd/<post>.psd.

A carousel is one wide canvas (slides side by side, 1080 px apart), like a seamless-carousel file: the studio ground is
a single continuous layer at the bottom, then one group per slide holding its Navy ground, Object, Brand, Text and
Footer groups. A static post is the same with one slide. The file's flattened preview is the rendered PNGs side by side.

Text is rasterised: each headline, body line, tag and chip is its own positioned layer, but not live type.

    python3 make_psd.py          # all posts
    python3 make_psd.py P03      # one post
"""
import json
import os
import sys

from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import Group, PixelLayer
from psd_tools.constants import Compression

HERE = os.path.dirname(os.path.abspath(__file__))
SW, SH = 1080, 1350
ORDER = ['Background', 'Object', 'Brand', 'Text', 'Footer']  # bottom to top within a slide


def pixel_layer(psd, path, name, top, left):
    """Load a layer image and trim it to its visible pixels so the PSD stays small."""
    im = Image.open(path).convert('RGBA')
    box = im.getchannel('A').getbbox()
    if not box:
        return None
    im = im.crop(box)
    return PixelLayer.frompil(im, psd, name[:250], top + box[1], left + box[0], compression=Compression.RLE)


def build(post):
    pid, slides, themes = post['id'], post['slides'], post['themes']
    n = len(slides)
    psd = PSDImage.new('RGBA', (n * SW, SH), color=(255, 255, 255, 0))
    studio = os.path.join(HERE, 'studio', pid + '.png')
    if os.path.exists(studio):
        ground = PixelLayer.frompil(Image.open(studio).convert('RGBA'), psd, 'Studio ground (continuous across the carousel)', 0, 0,
                                    compression=Compression.RLE)
        psd.append(ground)
    for i, (html, theme) in enumerate(zip(slides, themes)):
        name = html[:-5]
        src = os.path.join(HERE, 'layers', name)
        layers = json.load(open(os.path.join(src, 'layers.json')))
        subgroups = []
        for group in ORDER:
            members = []
            for l in layers:
                if l['group'] != group:
                    continue
                if group == 'Background' and theme != 'navy':
                    continue  # daylight slides show the continuous studio layer instead
                label = 'Navy ground' if group == 'Background' else l['name']
                px = pixel_layer(psd, os.path.join(src, l['file']), label, l['top'], l['left'] + i * SW)
                if px is not None:
                    psd.append(px)
                    members.append(px)
            if not members:
                continue
            subgroups.append(members[0] if group == 'Background' else Group.group_layers(psd, members, name=group))
        kind = 'Cover' if i == 0 else ('Call to action' if i == n - 1 and n > 1 else f'Slide {i + 1}')
        Group.group_layers(psd, subgroups, name=f'{i + 1:02d} · {kind}' if n > 1 else f'{pid} · {post["topic"]}')
    # flattened preview: the rendered slides side by side
    flat = Image.new('RGBA', (n * SW, SH))
    for i, html in enumerate(slides):
        flat.paste(Image.open(os.path.join(HERE, 'posts', pid, html.split('-')[1][:-5] + '.png')).convert('RGBA'), (i * SW, 0))
    psd._record.image_data.compression = Compression.RLE
    psd._record.image_data.set_data([c.tobytes() for c in flat.split()], psd._record.header)
    os.makedirs(os.path.join(HERE, 'psd'), exist_ok=True)
    out = os.path.join(HERE, 'psd', pid + '.psd')
    psd.save(out)
    return out


if __name__ == '__main__':
    posts = json.load(open(os.path.join(HERE, 'posts.json')))['posts']
    only = sys.argv[1:]
    for p in posts:
        if not only or p['id'] in only:
            out = build(p)
            print(p['id'], f'{os.path.getsize(out) / 1e6:.1f} MB', f'{len(p["slides"])} slide(s)')
