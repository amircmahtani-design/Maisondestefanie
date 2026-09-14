# -*- coding: utf-8 -*-
"""The hero film.

Takes the rendered still and actually moves it: a slow push across the
counter, candlelight that gutters, a flame that will not sit still, and
warm haze drifting through the room. Every motion is driven by whole
numbers of cycles over the loop, so the last frame runs back into the
first with no seam.
"""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SRC = ('/tmp/claude-0/-home-user-Maisondestefanie/'
       'f8d3ecfc-ee3c-5319-ae1c-05127152a947/scratchpad/graded/hero-still.png')

FPS = 24
SECONDS = 12
N = FPS * SECONDS

# where the candle sits in the source frame, as a fraction
FLAME_X, FLAME_Y = 0.752, 0.252


def sprite(w, h, inner=0.0):
    """A soft round falloff, used for every light in the scene."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    g = np.clip(1.0 - d, 0, 1) ** 2.6
    if inner:
        g = np.clip(g + inner * np.clip(1.0 - d / 0.35, 0, 1) ** 2, 0, 1)
    return g


def add_light(buf, spr, cx, cy, colour, gain):
    """Screen-blend a light sprite into the frame at (cx, cy)."""
    if gain <= 0:
        return
    h, w = spr.shape
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    x1, y1 = x0 + w, y0 + h
    bx0, by0 = max(0, x0), max(0, y0)
    bx1, by1 = min(buf.shape[1], x1), min(buf.shape[0], y1)
    if bx1 <= bx0 or by1 <= by0:
        return
    s = spr[by0 - y0:by1 - y0, bx0 - x0:bx1 - x0][..., None]
    region = buf[by0:by1, bx0:bx1]
    light = s * gain * np.asarray(colour, np.float32)
    buf[by0:by1, bx0:bx1] = 1.0 - (1.0 - region) * (1.0 - np.clip(light, 0, 1))


def build(out_w, out_h, path, codec, seed=7):
    src = Image.open(SRC).convert('RGB')
    SW, SH = src.size
    rs = np.random.RandomState(seed)

    glow = sprite(int(out_w * 0.50), int(out_w * 0.50), inner=0.30)
    flame = sprite(int(out_w * 0.045), int(out_w * 0.085), inner=0.9)
    haze1 = sprite(int(out_w * 0.95), int(out_w * 0.72))
    haze2 = sprite(int(out_w * 0.70), int(out_w * 0.55))

    proc = subprocess.Popen(
        [FFMPEG, '-y', '-loglevel', 'error',
         '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{out_w}x{out_h}', '-r', str(FPS), '-i', '-',
         *codec, '-pix_fmt', 'yuv420p', '-an', path],
        stdin=subprocess.PIPE)

    for i in range(N):
        t = i / N                      # 0..1 across the loop
        a = 2 * math.pi * t

        # ── the push: one full breath over the loop, so it never jumps
        zoom = 1.045 + 0.035 * math.sin(a - math.pi / 2)
        panx = 0.010 * math.sin(a)
        pany = 0.007 * math.cos(a)

        cw, ch = SW / zoom, SH / zoom
        cx = SW * (0.5 + panx) - cw / 2
        cy = SH * (0.5 + pany) - ch / 2
        cx = min(max(cx, 0), SW - cw)
        cy = min(max(cy, 0), SH - ch)
        frame = src.resize((out_w, out_h), Image.LANCZOS,
                           box=(cx, cy, cx + cw, cy + ch))
        buf = np.asarray(frame).astype(np.float32) / 255.0

        # where the candle ended up after the crop
        fx = (FLAME_X * SW - cx) / cw * out_w
        fy = (FLAME_Y * SH - cy) / ch * out_h

        # ── the gutter: harmonics that all close over the loop
        flick = (0.55 * math.sin(7 * a + 0.7) + 0.28 * math.sin(13 * a + 2.1)
                 + 0.17 * math.sin(23 * a + 4.3) + 0.10 * math.sin(37 * a))
        flick = 0.5 + 0.5 * flick                      # 0..1
        add_light(buf, glow, fx, fy, (1.0, 0.68, 0.32), 0.085 + 0.075 * flick)

        # the flame itself, leaning as it burns
        lean = 0.010 * out_w * math.sin(11 * a + 1.2)
        rise = 0.004 * out_h * math.sin(17 * a)
        add_light(buf, flame, fx + lean, fy + rise, (1.0, 0.90, 0.68),
                  0.34 + 0.30 * flick)

        # ── the air, going round a closed path so it loops
        add_light(buf, haze1,
                  out_w * (0.34 + 0.06 * math.cos(a)),
                  out_h * (0.55 + 0.05 * math.sin(a)),
                  (1.0, 0.66, 0.30), 0.032)
        add_light(buf, haze2,
                  out_w * (0.70 + 0.05 * math.cos(a + 2.2)),
                  out_h * (0.36 + 0.06 * math.sin(a + 2.2)),
                  (0.85, 0.35, 0.42), 0.022)

        # ── film grain, which should not loop
        buf += rs.normal(0, 0.011, (out_h, out_w, 1)).astype(np.float32)
        proc.stdin.write((np.clip(buf, 0, 1) * 255).astype(np.uint8).tobytes())

        if i % 48 == 0:
            print(f'  {path.split("/")[-1]}: frame {i}/{N}', flush=True)

    proc.stdin.close()
    proc.wait()
    return proc.returncode


if __name__ == '__main__':
    import os
    out = '/home/user/Maisondestefanie/assets/img'
    os.makedirs(out, exist_ok=True)
    VP9 = lambda crf: ['-c:v','libvpx-vp9','-crf',str(crf),'-b:v','0',
                       '-row-mt','1','-deadline','good','-cpu-used','2']
    # H.264 as well, because Safari on older iOS will not take WebM
    H264 = lambda crf: ['-c:v','libx264','-crf',str(crf),'-preset','slow',
                        '-profile:v','main','-movflags','+faststart']
    jobs = [(1600, 900, 'hero-loop.webm',        VP9(36)),
            (1600, 900, 'hero-loop.mp4',         H264(28)),
            ( 800, 450, 'hero-loop-mobile.webm', VP9(38)),
            ( 800, 450, 'hero-loop-mobile.mp4',  H264(30))]
    for w, h, name, codec in jobs:
        rc = build(w, h, f'{out}/{name}', codec)
        size = os.path.getsize(f'{out}/{name}') / 1024
        print(f'{name}: rc={rc}  {size:.0f} KB')
