# -*- coding: utf-8 -*-
"""Grade, lift and trim the three hero objects."""
import numpy as np
from PIL import Image
from grade import grade_rgba

GAIN = {'bottle': 1.30, 'vessel': 1.18, 'rose': 1.72}
FLOOR = 14          # alpha below this is halo, not object

for i, n in enumerate(['bottle', 'vessel', 'rose']):
    im = grade_rgba(Image.open(f'render/{n}.png'), bloom=0.24, vignette=0.0,
                    desat=0.08, grain=0.0, seed=50 + i)
    a = np.asarray(im).astype(np.float32)          # float, not int16 —
    a[..., :3] = np.clip(a[..., :3] * GAIN[n], 0, 255)
    if n == 'rose':
        # lifting every channel equally turns a burgundy rose pink; take
        # the saturation back out and hold the red down
        lum = (a[..., :3] @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
        a[..., :3] = a[..., :3] * 0.74 + lum * 0.26
        a[..., 0] *= 0.95
        a[..., 2] *= 1.02
        a[..., :3] = np.clip(a[..., :3], 0, 255)
    al = a[..., 3]
    al = np.where(al < FLOOR, 0.0, (al - FLOOR) * (255.0 / (255 - FLOOR)))
    a[..., 3] = np.clip(al, 0, 255)
    out = Image.fromarray(a.astype(np.uint8), 'RGBA')
    bb = out.getchannel('A').point(lambda v: 255 if v > 2 else 0).getbbox()
    if bb:
        pad = 6
        out = out.crop((max(0, bb[0]-pad), max(0, bb[1]-pad),
                        min(out.width, bb[2]+pad), min(out.height, bb[3]+pad)))
    out.save(f'graded/{n}.png')
    arr = np.asarray(out).astype(np.float32)
    vis = arr[..., 3] > 90
    lum = (arr[..., :3][vis] @ [0.2126, 0.7152, 0.0722]) if vis.sum() else np.array([0])
    print(f'{n}: {out.size}  opaque={vis.mean()*100:.0f}%  lum mean={lum.mean():.0f}')
