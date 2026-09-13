# -*- coding: utf-8 -*-
"""The four chapter scenes.

These are whole photographs, not objects cut out on black, so they are used
the way the reference film uses them: a full-bleed frame behind the words,
clipped by the panel and darkened by the stage scrim rather than matted.

Nothing here removes a background. All this does is grade them so the four
read as one shoot, and write the widths the page asks for. The scene sits
under a heavy scrim on its copy side, so the grade lifts a little contrast
back and keeps the deep end genuinely deep.
"""
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'supplied')
OUT = os.path.join(HERE, '..', 'assets', 'img')

#            file          black  gamma  warmth (r, g, b gain)
SCENES = {
    'rose':    ('rose.png',    5, 1.00, (1.000, 0.985, 0.965)),
    'vessel':  ('vessel.png',  6, 1.06, (1.000, 0.975, 0.940)),
    'compose': ('compose.png', 5, 1.06, (1.000, 0.980, 0.955)),
    'bottle':  ('bottle.png',  6, 1.08, (1.000, 0.982, 0.958)),
}
WIDTHS = [470, 700, 941]


def grade(name):
    f, black, gamma, warm = SCENES[name]
    a = np.asarray(Image.open(os.path.join(SRC, f)).convert('RGB')).astype(np.float32) / 255.0
    a = np.clip((a - black / 255.0) / (1.0 - black / 255.0), 0, 1)   # a true black point
    a = a ** gamma
    a *= np.asarray(warm, np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def main():
    man, total = {}, 0
    for name in SCENES:
        im = grade(name)
        entries = []
        for w in sorted({min(x, im.width) for x in WIDTHS}):
            h = round(im.height * w / im.width)
            fn = f'scene-{name}-{w}.webp'
            p = os.path.join(OUT, fn)
            im.resize((w, h), Image.LANCZOS).save(p, 'WEBP', quality=76, method=6)
            total += os.path.getsize(p)
            entries.append((f'assets/img/{fn}', w))
        man[name] = {'src': entries[-1][0],
                     'srcset': ', '.join(f'{p} {w}w' for p, w in entries),
                     'w': im.width, 'h': im.height}
        print(f'{name:8s} {im.width}x{im.height}  {len(entries)} widths')
    json.dump(man, open(os.path.join(HERE, 'scenes-manifest.json'), 'w'), indent=1)
    print(f'{total/1024:.0f} KB total')


if __name__ == '__main__':
    main()
