# -*- coding: utf-8 -*-
"""Cut the loose petals out of the storyboard so the ones that move on the
page are the same objects the storyboard drew.

The petals in keyframes 03 and 04 are pink and lit against a near-black
ground, so they separate cleanly on hue and brightness. Each one is
lifted with a soft alpha taken from its own luminance, which keeps the
edge it was photographed with rather than a cut-out's hard line.

    python3 tools/petals.py <folder-of-keyframes>

Writes assets/hero/petal-N.webp.
"""
from PIL import Image, ImageFilter
import numpy as np
import os
import sys

OUT = '/home/user/Maisondestefanie/assets/hero'
SOURCES = ['keyframe-03.jpg', 'keyframe-04.jpg']
MIN_AREA = 900          # anything smaller is grain, not a petal
MAX_AREA = 60000        # anything larger is the rose itself


def blobs(mask):
    """Connected components, breadth first, without scipy."""
    h, w = mask.shape
    seen = np.zeros((h, w), bool)
    out = []
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys, xs):
        if seen[sy, sx]:
            continue
        stack = [(sy, sx)]
        seen[sy, sx] = True
        pts = []
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        out.append(pts)
    return out


def main(folder):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name in SOURCES:
        im = Image.open(os.path.join(folder, name)).convert('RGB')
        a = np.asarray(im).astype(float)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        lum = a.max(axis=2)
        # pink: red clearly ahead of blue, and well clear of the ground
        mask = (lum > 95) & (r - b > 26) & (r > g + 8)
        for pts in blobs(mask):
            if not (MIN_AREA <= len(pts) <= MAX_AREA):
                continue
            ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
            t, bm = min(ys), max(ys); l, rt = min(xs), max(xs)
            pad = 8
            t = max(0, t - pad); l = max(0, l - pad)
            bm = min(a.shape[0], bm + pad); rt = min(a.shape[1], rt + pad)
            if (rt - l) < 24 or (bm - t) < 24:
                continue
            crop = im.crop((l, t, rt, bm))
            ca = np.asarray(crop).astype(float)
            # alpha from the petal's own light, so its edge stays soft
            al = np.clip((ca.max(axis=2) - 62) / 120, 0, 1)
            sub = np.zeros(((bm - t), (rt - l)), bool)
            for y, x in pts:
                sub[y - t, x - l] = True
            keep = Image.fromarray((sub * 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(3))
            al = al * (np.asarray(keep).astype(float) / 255.0)
            out = np.dstack([ca, np.clip(al, 0, 1) * 255]).astype(np.uint8)
            n += 1
            p = os.path.join(OUT, f'petal-{n}.webp')
            Image.fromarray(out, 'RGBA').save(p, 'WEBP', quality=86, method=6)
            print(f'  {os.path.basename(p):16} {rt-l}x{bm-t}  '
                  f'{os.path.getsize(p)//1024} KB  <- {name}')
    print(f'{n} petals')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
