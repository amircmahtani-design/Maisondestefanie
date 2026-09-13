# -*- coding: utf-8 -*-
"""Matte the four supplied photographs onto true black.

Each was shot on a lit studio backdrop, so the frame carries a broad warm
wash right out to its own corners. Screened onto the stage that wash reads
as a lighter rectangle sitting on the page. Here the wash is deepened with
a tonal curve and then multiplied by a soft ellipse centred on the subject,
so the crop runs to a genuine zero and has no edge left to see.

Radii are per-direction because the light pool under each object is worth
keeping and reaches much further down than the glow reaches up.
"""
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(HERE, 'supplied')   # the photographs as they were sent
OUT = os.path.join(HERE, '..', 'assets', 'img')

SHOTS = {
    #          source file            cx   cy   rx   up  down  gamma top-fade
    'rose':    ('rose.png', 476, 330, 480, 400, 610, 1.16, 0),
    'vessel':  ('vessel.png', 471, 381, 495, 380, 560, 1.34, 0),
    'compose': ('compose.png', 471, 320, 300, 430, 660, 1.38, 150),
    'bottle':  ('bottle.png', 468, 372, 340, 420, 650, 1.34, 0),
}
# full brightness inside this fraction of each radius, zero at the radius
INNER = 0.46
WIDTHS = [440, 720, 980]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def matte(name):
    f, cx, cy, rx, up, down, gamma, topfade = SHOTS[name]
    a = np.asarray(Image.open(os.path.join(UP, f)).convert('RGB')).astype(np.float32) / 255.0
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    a = a ** gamma                       # the dim field loses far more than the subject

    ny = np.where(yy < cy, (yy - cy) / up, (yy - cy) / down)
    d = np.sqrt(((xx - cx) / rx) ** 2 + ny ** 2)
    m = 1.0 - smoothstep(INNER, 1.0, d)
    if topfade:                          # the pipette leaves the frame; let it recede
        m *= smoothstep(0, topfade, yy)
    a *= m[..., None]

    keep = a.max(2) > 0.0035
    ys, xs = np.where(keep)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return Image.fromarray((np.clip(a[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8))


def main():
    man, total = {}, 0
    for name in SHOTS:
        im = matte(name)
        widths = sorted({min(x, im.width) for x in WIDTHS})
        entries = []
        for wdt in widths:
            hgt = round(im.height * wdt / im.width)
            fn = f'shot-{name}-{wdt}.webp'
            p = os.path.join(OUT, fn)
            im.resize((wdt, hgt), Image.LANCZOS).save(p, 'WEBP', quality=80, method=6)
            total += os.path.getsize(p)
            entries.append((f'assets/img/{fn}', wdt))
        man[name] = {'src': entries[-1][0],
                     'srcset': ', '.join(f'{p} {x}w' for p, x in entries),
                     'w': im.width, 'h': im.height}
        e = np.asarray(im.convert('RGB')).astype(int).max(2)
        print(f'{name:8s} {im.width}x{im.height}  edge max '
              f'{e[:2].max()}/{e[-2:].max()}/{e[:,:2].max()}/{e[:,-2:].max()}  peak {e.max()}')
    json.dump(man, open(os.path.join(HERE, 'shots-manifest.json'), 'w'), indent=1)
    print(f'{total/1024:.0f} KB total')


if __name__ == '__main__':
    main()
