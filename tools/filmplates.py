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

    python3 tools/filmplates.py <folder-of-keyframes>
"""
from PIL import Image
import os
import sys

OUT = '/home/user/Maisondestefanie/assets/hero'
WIDE = (1920, 1080)
TALL = (1080, 1920)

# act, the wide frame, the phone's frame, and where the phone's window
# sits across it — the rose at 0.68, the bottle at 0.54, and for the bowl
# and the still a frame that has no edge to lose
PLATES = [
    (1, 'keyframe-02.jpg', 'keyframe-02.jpg', 0.68, 0.46),
    (2, 'keyframe-06.jpg', 'keyframe-08.jpg', 0.50, 0.50),
    (3, 'keyframe-09.jpg', 'keyframe-10.jpg', 0.42, 0.50),
    (4, 'keyframe-16.jpg', 'keyframe-16.jpg', 0.54, 0.52),
]


def crop_to(im, size, cx, cy):
    """The largest window of `size`'s shape that fits, placed on the
    subject. Nothing is invented and nothing is feathered."""
    W, H = size
    ar = W / H
    if im.width / im.height > ar:
        h = im.height; w = round(h * ar)
    else:
        w = im.width; h = round(w / ar)
    l = max(0, min(im.width - w, round(cx * im.width - w / 2)))
    t = max(0, min(im.height - h, round(cy * im.height - h / 2)))
    return im.crop((l, t, l + w, t + h)).resize(size, Image.LANCZOS)


def main(folder):
    os.makedirs(OUT, exist_ok=True)
    for act, wide_src, tall_src, cx, cy in PLATES:
        wide = Image.open(os.path.join(folder, wide_src)).convert('RGB')
        tall = Image.open(os.path.join(folder, tall_src)).convert('RGB')
        for suffix, img, src in (
                ('wide', wide.resize(WIDE, Image.LANCZOS), wide_src),
                ('tall', crop_to(tall, TALL, cx, cy), tall_src)):
            p = os.path.join(OUT, f'plate-{act}-{suffix}.webp')
            img.save(p, 'WEBP', quality=78, method=6)
            print(f'  {os.path.basename(p):22} {img.size[0]}x{img.size[1]}  '
                  f'{os.path.getsize(p)//1024} KB   <- {src}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
