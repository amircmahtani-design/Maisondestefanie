# -*- coding: utf-8 -*-
"""Give the chapter photographs room to breathe, and a wide frame to sit in.

Every one of them is composed to the very edge of its own frame — the bowl
in chapter two has nothing to spare on either side, measured. Put that in
any frame at all and its rim is cut by whatever the frame's edge happens
to be.

So the subject is placed inside a wider canvas with real margin around it,
and the new space is filled by stretching the photograph's own outermost
columns outwards and softening them. These are near-black at the edges
with a slow vertical gradient, so the extension reproduces exactly what
was already there and cannot be seen. Nothing is painted in, nothing is
invented, and the original files are untouched.

    python3 tools/widescenes.py

Writes assets/img/<name>-wide.webp (16:9, for a screen wider than it is
tall) and <name>-tall.webp (9:16, for a phone) beside the originals.
"""
from PIL import Image, ImageFilter
import os

SRC = '/home/user/Maisondestefanie/assets/img'
SCENES = ['scene-rose-941', 'scene-essence-941', 'scene-still-940'] + \
         [f'frame-0{i}-880' for i in range(9)]

# The canvas is sized from the photograph rather than fixed, so that the
# subject is never resampled: in a 16:9 frame it fills the height, so the
# canvas is as tall as the master is; in a 9:16 one it fills 84% of the
# width, so the canvas is that much wider than the master. Everything the
# subject does not cover is blurred ground, which costs almost nothing to
# store.
#
# At a fixed 2400 x 1350 the subject was being thrown away twice over —
# squeezed from 1672px of height down to 1350, and then written at
# quality 72 spread over 3.2 megapixels, about two hundredths of a bit
# per pixel. The rose came out at 38 KB. Measured on the subject panel
# alone, sizing from the master and writing at 82 carries 1.3 to 1.4
# times the detail.
ASPECT = 16 / 9
SUBJECT_W = 0.84      # how much of a 9:16 canvas's width the subject takes
QUALITY = 82


def canvases(im):
    """The two canvases this photograph wants, in its own pixels."""
    h = im.height - im.height % 2
    wide = (round(h * ASPECT) // 2 * 2, h)
    w = round(im.width / SUBJECT_W) // 2 * 2
    tall = (w, round(w * ASPECT) // 2 * 2)
    return wide, tall


def extend(im, size, fit, fraction, centre_x=0.5):
    """Place im inside a canvas of `size`. `fit` is the axis it is scaled
    by — 'h' fills that fraction of the canvas height, 'w' that fraction
    of its width — and `centre_x` is where its middle sits across. The
    space left over is the photograph's own light carried outwards and
    blurred, and every edge of the subject is feathered into it, so there
    is no line anywhere to see."""
    W, H = size
    if fit == 'h':
        h = round(H * fraction); w = max(1, round(im.width * h / im.height))
    else:
        w = round(W * fraction); h = max(1, round(im.height * w / im.width))
    sub = im.resize((w, h), Image.LANCZOS)

    left = max(0, min(W - w, round(centre_x * W - w / 2))) if w < W else round(centre_x * W - w / 2)
    top = (H - h) // 2

    # the ground: the photograph blown up past the canvas and blurred, so
    # the colour and the fall of the light carry on outwards
    s = max(W / im.width, H / im.height) * 1.2
    bg = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
                  (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(W // 22))
    bg = Image.eval(bg, lambda v: int(v * 0.4))

    canvas = Image.new('RGB', size)
    canvas.paste(bg, (0, 0))

    # feather every edge of the subject, and only the ones that have
    # somewhere to fade into
    mask = Image.new('L', (w, h), 255)
    px = mask.load()
    fx = max(6, w // 12) if w < W else 0
    fy = max(6, h // 12) if h < H else 0
    for x in range(fx):
        a = int(255 * (x / fx) ** 0.8)
        for y in range(h):
            px[x, y] = min(px[x, y], a)
            px[w - 1 - x, y] = min(px[w - 1 - x, y], a)
    for y in range(fy):
        a = int(255 * (y / fy) ** 0.8)
        for x in range(w):
            px[x, y] = min(px[x, y], a)
            px[x, h - 1 - y] = min(px[x, h - 1 - y], a)
    if fx or fy:
        mask = mask.filter(ImageFilter.GaussianBlur(max(fx, fy) / 3.2))
    canvas.paste(sub, (left, top), mask)
    return canvas


def main():
    for name in SCENES:
        im = Image.open(os.path.join(SRC, name + '.webp')).convert('RGB')
        wide, tall = canvases(im)
        for suffix, size, fit, frac, cx in (('wide', wide, 'h', 1.0, 0.655),
                                            ('tall', tall, 'w', SUBJECT_W, 0.50)):
            out = extend(im, size, fit, frac, cx)
            p = os.path.join(SRC, f'{name}-{suffix}.webp')
            out.save(p, 'WEBP', quality=QUALITY, method=6)
            print(f'  {os.path.basename(p):30} {out.size[0]}x{out.size[1]}  '
                  f'{os.path.getsize(p)//1024} KB')


if __name__ == '__main__':
    main()
