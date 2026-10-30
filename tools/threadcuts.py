# -*- coding: utf-8 -*-
"""Purpose-made 3:4 crops for the five cards on the perfumer's bench.

The cards were showing whole photographs squeezed into a portrait box — the
candle shelf lost 58% of its width, the rose 25% of its height. Each card
gets its own crop of the subject instead, at the shape the card actually is.
"""
from PIL import Image
import os
SRC = '/home/user/Maisondestefanie/assets/img'
OUT = SRC
AR  = 3/4                       # the card at its widest

CUTS = [
    # name,          source,              centre x, centre y  (0–1 of the frame)
    ('thread-places', 'plaka-900.webp',      .56, .58),   # the steps and the lantern
    ('thread-sea',    'scene-essence-941.webp', .50, .47), # light moving on the water
    ('thread-someone','scene-rose-941.webp',  .52, .26),   # the rose, alone
    ('thread-moment', 'shopfront-900.webp',   .66, .42),   # the door still lit
    ('thread-lost',   'cut-bottle-900.webp',  .62, .44),   # the bottle, sealed
]

for name, src, cx, cy in CUTS:
    im = Image.open(os.path.join(SRC, src)).convert('RGB')
    W, H = im.size
    # the largest 3:4 box that fits, placed on the subject
    w = min(W, int(H * AR)); h = int(w / AR)
    if h > H: h = H; w = int(h * AR)
    l = int(cx * W - w / 2); t = int(cy * H - h / 2)
    l = max(0, min(W - w, l)); t = max(0, min(H - h, t))
    cut = im.crop((l, t, l + w, t + h))
    for width in (560, 900):
        r = cut.resize((width, int(width / AR)), Image.LANCZOS)
        p = os.path.join(OUT, f'{name}-{width}.webp')
        r.save(p, 'WEBP', quality=72, method=6)
        print(f'{os.path.basename(p):26} {r.size[0]}x{r.size[1]}  {os.path.getsize(p)//1024} KB   <- {src} {w}x{h} @ {l},{t}')
