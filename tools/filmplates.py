# -*- coding: utf-8 -*-
"""The four scene plates for the home page's first screen.

The storyboard is sixteen keyframes in which the camera and the subject
move between one and the next, so playing them would jump. One frame per
act is taken as a fixed plate instead — locked camera, locked subject —
and everything that moves is animated over it as its own layer.

Nothing is extended and nothing is composited. A keyframe is already
16:9, so on a wide screen it fills the viewport edge to edge: real
photograph everywhere, including under the headline, with no seam for a
feathered panel to leave behind.

A phone is 9:16, which a 16:9 frame cannot cover without losing two
thirds of its width — so each act names its own frame and its own crop
for a phone, chosen so the subject survives the window rather than being
cut by it.

This writes the 16:9 plates only. An upright screen does not take a 9:16
window of these frames any more: that window is 405 x 720, a third of a
megapixel behind a phone that wants three, and the house already owns
four upright photographs of the same four subjects at 1.4 to 1.6
megapixels. assets/hero-film.js names those directly.

ON SHARPNESS. Every frame in the motion pack is 1280 x 720. That is the
ceiling: no detail can be recovered that was not in the file. What CAN be
thrown away is most of it, and the first pass did — it enlarged to
1920 x 1080 and then wrote WebP at quality 78, so the quantiser spent its
bytes on interpolated gradient and smeared the copper. The pass now
resizes once with LANCZOS, puts a real unsharp mask over the result, and
writes at quality 90.

If the full-resolution originals turn up, drop them in and run this
again; nothing else needs to change.

    python3 tools/filmplates.py <folder-of-keyframes>
"""
from PIL import Image, ImageFilter
import os
import sys

OUT = '/home/user/Maisondestefanie/assets/hero'
WIDE = (1920, 1080)
QUALITY = 90

# act, and the frame it is held on
PLATES = [
    (1, 'keyframe-02.jpg'),
    (2, 'keyframe-06.jpg'),
    (3, 'keyframe-09.jpg'),
    (4, 'keyframe-16.jpg'),
]


def deframe(im, limit=6):
    """A few of the frames carry two or three rows of pure black along an
    edge. Enlarged they become a hairline across the screen."""
    import numpy as np
    a = np.asarray(im.convert('L')).astype(int)
    col, row = a.mean(axis=0), a.mean(axis=1)

    def run(v, forward):
        n = 0
        for i in (range(len(v)) if forward else range(len(v) - 1, -1, -1)):
            if v[i] < limit:
                n += 1
            else:
                break
        return n

    l, r = run(col, True), run(col, False)
    t, b = run(row, True), run(row, False)
    if l or r or t or b:
        im = im.crop((l, t, im.width - r, im.height - b))
    return im


def sharpen(im):
    """Enlarging is interpolation, and interpolation is a low-pass filter.
    This puts the edge back — enough to read as the photograph it came
    from, not so much that the copper picks up a halo."""
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=118, threshold=3))


def main(folder):
    os.makedirs(OUT, exist_ok=True)
    for act, wide_src in PLATES:
        wide = deframe(Image.open(os.path.join(folder, wide_src)).convert('RGB'))
        img = sharpen(wide.resize(WIDE, Image.LANCZOS))
        p = os.path.join(OUT, f'plate-{act}-wide.webp')
        img.save(p, 'WEBP', quality=QUALITY, method=6)
        print(f'  {os.path.basename(p):22} {img.size[0]}x{img.size[1]}  '
              f'{os.path.getsize(p)//1024} KB   <- {wide_src}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
