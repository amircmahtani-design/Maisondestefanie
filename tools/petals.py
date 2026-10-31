# -*- coding: utf-8 -*-
"""The petal cut-outs the first screen drops through its scenes.

They arrive with the scene plates, in tools/supplied/motion-masks/, cut
from the same artwork and already carrying their own alpha — so there is
nothing to mask here. This only writes them out as WebP, at twice the
size they are ever drawn so a retina screen has something to work with.

    python3 tools/petals.py
"""
from PIL import Image
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'supplied', 'motion-masks')
OUT = os.path.join(ROOT, 'assets', 'hero')
LONG_EDGE = 320          # a petal is drawn at up to ~160px
QUALITY = 88


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(SRC, 'petal-*.png'))):
        im = Image.open(f).convert('RGBA')
        s = LONG_EDGE / max(im.size)
        if s > 1:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        n += 1
        p = os.path.join(OUT, f'petal-{n}.webp')
        im.save(p, 'WEBP', quality=QUALITY, method=6)
        print(f'  petal-{n}.webp  {im.size[0]}x{im.size[1]}  '
              f'{os.path.getsize(p)//1024} KB   <- {os.path.basename(f)}')
    # anything left from the previous set is no longer referenced
    for extra in range(n + 1, 12):
        p = os.path.join(OUT, f'petal-{extra}.webp')
        if os.path.exists(p):
            os.remove(p)
            print(f'  removed petal-{extra}.webp')


if __name__ == '__main__':
    main()
