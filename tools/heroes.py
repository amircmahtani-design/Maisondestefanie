# -*- coding: utf-8 -*-
"""Bring the per-page hero artwork into the site.

Stefanie's artwork arrives as PNG, three compositions of one scene per
page — 16:9 for a wide screen, 4:3 for a tablet, 9:16 for a phone. PNG is
the wrong thing to serve a photograph over a phone connection, so each
one is written out as WebP beside it. Drop a replacement PNG in and run
this again; the names on the page never change.

The artwork is 1672 x 941 and that is the ceiling — the WebP is written
at the PNG's own size, never enlarged. Quality is 86: at 74 the encoder
was smoothing away the grain and the specular edges that make these read
as photographs, for about 60 KB a page.

    python3 tools/heroes.py <folder-of-pages> [<folder-of-pages> ...]

Each folder holds one directory per page (home, maison, bespoke, story,
creations, visit), each with desktop.png, ipad.png and iphone.png.
"""
from PIL import Image
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'heroes')
PAGES = ('home', 'maison', 'bespoke', 'story', 'creations', 'visit')
DEVICES = ('desktop', 'ipad', 'iphone')
QUALITY = 86


def main(folders):
    found = 0
    for folder in folders:
        for page in PAGES:
            src_dir = os.path.join(folder, page)
            if not os.path.isdir(src_dir):
                continue
            os.makedirs(os.path.join(OUT, page), exist_ok=True)
            for device in DEVICES:
                src = os.path.join(src_dir, device + '.png')
                if not os.path.exists(src):
                    print(f'  missing: {page}/{device}.png')
                    continue
                im = Image.open(src).convert('RGB')
                dst = os.path.join(OUT, page, device + '.webp')
                im.save(dst, 'WEBP', quality=QUALITY, method=6)
                before = os.path.getsize(src) // 1024
                after = os.path.getsize(dst) // 1024
                print(f'  {page}/{device}.webp  {im.size[0]}x{im.size[1]}  '
                      f'{before} KB PNG -> {after} KB WebP')
                found += 1
    print(f'{found} files')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
