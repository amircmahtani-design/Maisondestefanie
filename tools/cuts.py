# -*- coding: utf-8 -*-
"""Editorial crops of the supplied photographs for the sections below the
hero.

The hero shows each photograph whole; the sections want particular shapes —
a 4:5 beside her words, a 21:9 band across the page. Rather than let the
browser cover-crop a 9:16 frame into a 21:9 slot and lose nine tenths of it,
the crop is taken here, from the part of the picture that is worth keeping.
"""
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'supplied')
OUT  = os.path.join(HERE, '..', 'assets', 'img')

#  name          source                    ratio   the band of the frame to keep
CUTS = {
    'cut-essence': ('02-essence-hero.png',  4/5,   (0.26, 0.86), 1.04, [560, 900]),
    'cut-still':   ('03-distillation-hero.png', 21/9, (0.30, 0.62), 1.06, [900, 1500, 2000]),
    'cut-bottle':  ('04-bottle-frame-04.png', 3/4,  (0.14, 0.86), 1.04, [560, 900]),
    'cut-rose':    ('01-rose-hero.png',     21/9,   (0.06, 0.34), 1.00, [900, 1500, 2000]),
    'cut-petals':  ('04-bottle-frame-07.png', 21/9, (0.02, 0.34), 1.04, [900, 1500, 2000]),
}


def cut(name):
    f, ratio, (a, b), gamma, widths = CUTS[name]
    im = Image.open(os.path.join(SRC, f)).convert('RGB')
    W, H = im.size
    top, bot = int(H * a), int(H * b)
    want_h = bot - top
    want_w = int(round(want_h * ratio))
    if want_w > W:                       # the band is wider than the frame
        want_w = W
        want_h = int(round(W / ratio))
        top = min(max(top + (bot - top - want_h) // 2, 0), H - want_h)
    x = (W - want_w) // 2
    box = im.crop((x, top, x + want_w, top + want_h))
    if gamma != 1.0:
        arr = (np.asarray(box).astype(np.float32) / 255.0) ** gamma
        box = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    return box, widths


def main():
    man = {}
    for name in CUTS:
        im, widths = cut(name)
        entries = []
        for w in sorted({min(x, im.width) for x in widths}):
            h = round(im.height * w / im.width)
            fn = f'{name}-{w}.webp'
            im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, fn), 'WEBP',
                                                  quality=76, method=6)
            entries.append((f'assets/img/{fn}', w))
        man[name] = {'src': entries[-1][0],
                     'srcset': ', '.join(f'{p} {w}w' for p, w in entries),
                     'w': im.width, 'h': im.height}
        print(f'{name:12s} {im.width}x{im.height}  ({im.width/im.height:.2f})')
    json.dump(man, open(os.path.join(HERE, 'cuts-manifest.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
