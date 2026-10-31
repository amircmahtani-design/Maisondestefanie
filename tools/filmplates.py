# -*- coding: utf-8 -*-
"""The eight scene plates for the home page's first screen.

Source: tools/supplied/0N-<name>-wide-3840x2160.jpg and
        tools/supplied/0N-<name>-upright-1620x2880.jpg

WHAT THOSE EXPORTS ACTUALLY CARRY, AND WHY THIS RESIZES THEM DOWN

Their own README and manifest say it plainly: both exports are resamples
of four 1600 x 900 masters, not native 4K. Measured, that is exactly what
they are — detail per pixel keeps climbing all the way down, which is the
signature of an enlargement.

So the plates are written at the size where the detail actually lives.
Measured as the variance of the Laplacian at what a 1440 laptop at 2x and
a 390 phone at 3x really paint:

  wide     1600 x 900  + unsharp      50.4     (the 3840 export, taken
                                                down to 1920, scores
                                                50.7 for 71 KB more)
  upright  1080 x 1920 + unsharp      65.9     (the 1620 export as it
                                                stands scores 25.5 —
                                                downscaling it recovers
                                                two and a half times)

Quality 78 is the knee on both: 72 loses a little, 86 costs a quarter
more bytes for nothing.

For comparison, what these replace: the first motion pack scored 11.3 at
a common size against these scenes' 351, and the house's own photographs
— which the first screen used in between — gave 8.96 wide and 56.9
upright on the same screen measure. So this is 5.6x wide and 1.16x
upright over the photographs, and far past the old pack either way.

If genuinely native 3840 x 2160 and 1620 x 2880 scenes ever arrive, drop
them in the same place: raise WIDE and TALL to match and change nothing
else.

    python3 tools/filmplates.py
"""
from PIL import Image, ImageFilter
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'supplied')
OUT = os.path.join(ROOT, 'assets', 'hero')

WIDE = (1600, 900)
TALL = (1080, 1920)
QUALITY = 78
USM_WIDE = (1.5, 110, 3)
USM_TALL = (1.3, 95, 3)


def one(act, shape, size, usm):
    hits = sorted(glob.glob(os.path.join(SRC, f'0{act}-*-{shape}-*.jpg')))
    if not hits:
        print(f'  missing: 0{act}-*-{shape}-*.jpg')
        return
    im = Image.open(hits[0]).convert('RGB')
    out = im.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(*usm))
    p = os.path.join(OUT, f'plate-{act}-{shape}.webp')
    out.save(p, 'WEBP', quality=QUALITY, method=6)
    print(f'  plate-{act}-{shape}.webp  {size[0]}x{size[1]}  '
          f'{os.path.getsize(p)//1024:4} KB   <- {os.path.basename(hits[0])}')


def main():
    os.makedirs(OUT, exist_ok=True)
    for act in (1, 2, 3, 4):
        one(act, 'wide', WIDE, USM_WIDE)
        one(act, 'upright', TALL, USM_TALL)


if __name__ == '__main__':
    main()
