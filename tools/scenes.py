# -*- coding: utf-8 -*-
"""The cinematic set: three scenes and the nine bottle frames.

These are whole photographs, so nothing is cut out. The script sets a true
black point, grades the four scenes so they read as one shoot, and writes
the widths the page asks for.

The bottle frames are a different job. They are a loop, so they are graded
identically — one shared black point and curve for all nine, or the petals
would appear to flicker as the exposure moved under them — and written at
two widths only, because every frame in whichever set the browser picks
has to be decoded before the loop can start.
"""
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'supplied')
OUT = os.path.join(HERE, '..', 'assets', 'img')

#            source file                black gamma  warmth
SCENES = {
    'rose':    ('01-rose-hero.png',         5, 1.02, (1.000, 0.985, 0.965)),
    'essence': ('02-essence-hero.png',      5, 1.04, (1.000, 0.982, 0.958)),
    'still':   ('03-distillation-hero.png', 6, 1.06, (1.000, 0.975, 0.940)),
}
SCENE_WIDTHS = [470, 700, 941]

FRAMES = [f'04-bottle-frame-0{i}.png' for i in range(9)]
FRAME_BLACK, FRAME_GAMMA, FRAME_WARM = 5, 1.05, (1.000, 0.980, 0.955)
# the loop is dense bokeh, so quality is dominated by content rather than
# the quantiser: q58 and q76 measure within a decibel of each other, and
# every frame here has to be decoded before the loop can start
FRAME_WIDTHS = [560, 880]
FRAME_Q = 58


def grade(path, black, gamma, warm):
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32) / 255.0
    a = np.clip((a - black / 255.0) / (1.0 - black / 255.0), 0, 1)
    a = (a ** gamma) * np.asarray(warm, np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def write(im, name, widths, q):
    entries = []
    for w in sorted({min(x, im.width) for x in widths}):
        h = round(im.height * w / im.width)
        fn = f'{name}-{w}.webp'
        im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, fn), 'WEBP',
                                              quality=q, method=6)
        entries.append((f'assets/img/{fn}', w))
    return {'src': entries[-1][0],
            'srcset': ', '.join(f'{p} {w}w' for p, w in entries),
            'w': im.width, 'h': im.height}


def main():
    man, total = {}, 0
    for name, (f, black, gamma, warm) in SCENES.items():
        man[name] = write(grade(os.path.join(SRC, f), black, gamma, warm),
                          f'scene-{name}', SCENE_WIDTHS, 76)
        print(f"{name:8s} {man[name]['w']}x{man[name]['h']}")

    frames = []
    for i, f in enumerate(FRAMES):
        im = grade(os.path.join(SRC, f), FRAME_BLACK, FRAME_GAMMA, FRAME_WARM)
        frames.append(write(im, f'frame-{i:02d}', FRAME_WIDTHS, FRAME_Q))
    man['frames'] = frames
    print(f'{len(frames)} bottle frames  {frames[0]["w"]}x{frames[0]["h"]}')

    for w in FRAME_WIDTHS:
        kb = sum(os.path.getsize(os.path.join(OUT, f'frame-{i:02d}-{w}.webp'))
                 for i in range(9)) / 1024
        print(f'  the {w}w loop costs {kb:.0f} KB in total')
    total = sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT)
                if x.startswith(('scene-', 'frame-')))
    json.dump(man, open(os.path.join(HERE, 'scenes-manifest.json'), 'w'), indent=1)
    print(f'{total/1024:.0f} KB written')


if __name__ == '__main__':
    main()
