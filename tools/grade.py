# -*- coding: utf-8 -*-
"""One grade over the whole set, so twelve separately built frames read
as a single afternoon's shoot: crushed blacks, warm mids, a little
bloom off the highlights, and film grain."""
import numpy as np
from PIL import Image, ImageFilter


def _curve(x, toe=0.16, shoulder=0.96, gamma=1.18):
    """Pull the shadows down and hold the highlights, the way a print does."""
    x = np.clip((x - toe * 0.32) / (shoulder - toe * 0.32), 0, 1)
    return np.clip(x ** gamma, 0, 1)


def grade(img, warmth=0.09, desat=0.14, bloom=0.30, bloom_r=26,
          grain=0.016, vignette=0.30, lift=0.008, seed=0):
    rgb = img.convert('RGB')
    a = np.asarray(rgb).astype(np.float32) / 255.0

    # tone
    a = _curve(a)

    # warm the mid-tones, cool the deepest shadows a touch so the black
    # does not go muddy brown
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    mid = np.clip(1.0 - np.abs(lum - 0.42) / 0.46, 0, 1)[..., None]
    a[..., 0] += warmth * 1.00 * mid[..., 0]
    a[..., 1] += warmth * 0.42 * mid[..., 0]
    a[..., 2] -= warmth * 0.34 * mid[..., 0]
    shadow = np.clip(1.0 - lum / 0.16, 0, 1)[..., None]
    a[..., 2] += 0.012 * shadow[..., 0]

    # take a little colour out so it stops looking like a screen
    lum2 = (a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    a = a * (1 - desat) + lum2 * desat

    a = np.clip(a, 0, 1)

    # bloom: the highlights spill, which is most of what makes a lit
    # photograph feel lit
    if bloom > 0:
        hi = np.clip((a - 0.62) / 0.38, 0, 1)
        him = Image.fromarray((hi * 255).astype(np.uint8))
        him = him.filter(ImageFilter.GaussianBlur(bloom_r))
        hb = np.asarray(him).astype(np.float32) / 255.0
        a = 1 - (1 - a) * (1 - hb * bloom)

    # a last vignette, on top of the one drawn in the scene
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx / w) - 0.55) ** 2 + ((yy / h) - 0.44) ** 2) / 0.78
    v = np.clip(1 - vignette * np.clip(d - 0.42, 0, None) ** 1.5 * 3.2, 0, 1)
    a *= v[..., None]

    # grain
    if grain > 0:
        rs = np.random.RandomState(seed)
        n = rs.normal(0, grain, (h, w, 1)).astype(np.float32)
        a = np.clip(a + n * (0.35 + 0.65 * np.clip(a, 0, 1)), 0, 1)

    a = np.clip(a + lift, 0, 1)
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def grade_rgba(img, **kw):
    """Same, but keep the cut-out's transparency."""
    rgba = img.convert('RGBA')
    alpha = rgba.getchannel('A')
    out = grade(rgba, **kw)
    out = out.convert('RGBA')
    out.putalpha(alpha)
    return out
