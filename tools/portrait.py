# -*- coding: utf-8 -*-
"""Her photograph, the one the site uses wherever Stefanie herself appears.

The original is tools/supplied/stefanie-portrait.jpg, 1400 x 939. The
site wants it upright, so it takes a 751 x 939 window of it — the full
height, placed on her — and serves that at two widths.

751 x 939 is the whole of the original's height, so this is the largest
the picture can be. The only thing worth changing is the quality it is
written at: the first pass wrote it small enough that her hair and the
stone of the flacon went to mush.

    python3 tools/portrait.py
"""
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'supplied', 'stefanie-portrait.jpg')
OUT = os.path.join(ROOT, 'assets', 'img')

# In the original she is at x 230-620 and the flacon she is holding runs
# from 740 to 880, with her fingers round it to about 900. The window the
# site inherited was 98-849, which cut the flacon — a quarter of it and
# two of her fingertips were outside the frame. 175-926 is the same 751
# wide, moved along so the bottle and her hand are whole; it loses a
# little hair on the left, which runs off frame the way hair does.
BOX = (175, 0, 926, 939)
WIDTHS = (560, 751)
QUALITY = 90


def main():
    im = Image.open(SRC).convert('RGB').crop(BOX)
    for w in WIDTHS:
        h = round(im.height * w / im.width)
        out = im if w == im.width else im.resize((w, h), Image.LANCZOS)
        p = os.path.join(OUT, f'stefanie-{w}.webp')
        out.save(p, 'WEBP', quality=QUALITY, method=6)
        print(f'  stefanie-{w}.webp  {out.size[0]}x{out.size[1]}  '
              f'{os.path.getsize(p)//1024} KB')


if __name__ == '__main__':
    main()
