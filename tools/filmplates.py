# -*- coding: utf-8 -*-
"""The four landscape plates for the home page's first screen.

WHY THESE COME FROM THE HOUSE'S OWN PHOTOGRAPHS AND NOT THE MOTION PACK

The pack was never a resolution problem. Measured as the variance of the
Laplacian with every file resampled to the same 1280 x 720 — so the
number is about the picture and not its size — the sixteen keyframes
score 3.7 to 24.0, mean 11.3. The house's four scene photographs score
228 to 706, mean 397. Forty times the detail at the same pixel count.
The pack is not a small version of a sharp picture; it is a soft
picture, which is also why an unsharp mask over it bought only 1.39x:
there was almost no edge in it to find.

So a 16:9 band cut out of a 941 x 1672 photograph — 941 pixels wide,
twenty-six per cent fewer than the pack's 1280 — lands on screen with
2.2x the detail. Fewer pixels, sharper result. The pack remains the
storyboard: it is what the four acts and their movement were designed
from. It is no longer what the page paints.

Enlarging the band to 1600 x 900 and sharpening it beats both leaving it
native and going to 1920: measured on a 1440 laptop at 2x, 8.96 against
2.87 native and 8.63 at 1920, for 57 KB.

An upright screen takes the master itself, uncut and unencoded a second
time; assets/hero-film.js names those directly.

    python3 tools/filmplates.py
"""
from PIL import Image, ImageFilter
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'img')
OUT = os.path.join(ROOT, 'assets', 'hero')

WIDE = (1600, 900)
QUALITY = 86

# act, the master, and where down it the 16:9 band is taken — chosen so
# the subject keeps to the right of the frame and the left stays dark,
# which is where the headline is read
PLATES = [
    (1, 'scene-rose-941', 0.30),
    (2, 'scene-essence-941', 0.34),
    (3, 'scene-still-940', 0.26),
    (4, 'frame-00-880', 0.30),
]


def band(im, ty):
    """The widest 16:9 window the photograph holds, placed down it by
    `ty`. Nothing is extended, nothing is feathered, and the picture runs
    edge to edge."""
    w = im.width
    h = round(w * 9 / 16)
    top = max(0, min(im.height - h, round((im.height - h) * ty)))
    return im.crop((0, top, w, top + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    for act, master, ty in PLATES:
        im = Image.open(os.path.join(SRC, master + '.webp')).convert('RGB')
        out = band(im, ty).resize(WIDE, Image.LANCZOS) \
                          .filter(ImageFilter.UnsharpMask(1.5, 110, 3))
        p = os.path.join(OUT, f'plate-{act}-wide.webp')
        out.save(p, 'WEBP', quality=QUALITY, method=6)
        print(f'  plate-{act}-wide.webp  {out.size[0]}x{out.size[1]}  '
              f'{os.path.getsize(p)//1024} KB   <- {master}')


if __name__ == '__main__':
    main()
