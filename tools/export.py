# -*- coding: utf-8 -*-
"""Write the finished set into the repository at the sizes the page
actually asks for, and hand back the srcset strings to put in
content.json."""
import json, os, shutil
from PIL import Image

OUT = '/home/user/Maisondestefanie/assets/img'
SRC = '/tmp/claude-0/-home-user-Maisondestefanie/f8d3ecfc-ee3c-5319-ae1c-05127152a947/scratchpad/graded'

#  name            widths                  quality  png fallback
PLAN = [
    ('hero-still', [1100, 1600, 2200], 70, False),
    ('workshop',   [ 900, 1500, 2000], 70, False),
    ('atwork',     [ 900, 1500, 2000], 70, False),
    ('counter',    [ 560,  900, 1200], 76, False),
    ('botanical',  [ 560,  900, 1200], 76, False),
    ('bench',      [ 560,  900, 1200], 76, False),
    ('sealing',    [ 560,  900, 1200], 76, False),
    ('shopfront',  [ 560,  900, 1200], 76, False),
    ('plaka',      [ 560,  900, 1200], 76, False),
    ('bottle',     [ 420,  700, 1000], 68, False),
    ('vessel',     [ 480,  800, 1100], 68, False),
    ('rose',       [ 520,  860, 1200], 68, False),
]
PLAN += [(f'prod-p{i}', [420, 700], 78, False) for i in range(1, 13)]


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    total = 0
    for name, widths, q, png in PLAN:
        im = Image.open(os.path.join(SRC, f'{name}.png'))
        has_alpha = im.mode in ('RGBA', 'LA')
        entries = []
        # a width larger than the source is pointless, and a repeated
        # descriptor makes the srcset invalid
        widths = sorted({min(w, im.width) for w in widths})
        for w in widths:
            h = round(im.height * w / im.width)
            r = im.resize((w, h), Image.LANCZOS)
            fn = f'{name}-{w}.webp'
            path = os.path.join(OUT, fn)
            if has_alpha:
                r.save(path, 'WEBP', quality=q, method=6)
            else:
                r.convert('RGB').save(path, 'WEBP', quality=q, method=6)
            total += os.path.getsize(path)
            entries.append((f'assets/img/{fn}', w))
        if png:
            w = widths[1]
            h = round(im.height * w / im.width)
            fb = f'{name}-{w}.png'
            im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, fb), optimize=True)
            total += os.path.getsize(os.path.join(OUT, fb))
        mid = entries[len(entries) // 2]
        manifest[name] = {
            'src': mid[0],
            'srcset': ', '.join(f'{p} {w}w' for p, w in entries),
            'w': im.width, 'h': im.height,
        }
    print(f'{len(os.listdir(OUT))} files, {total/1024/1024:.2f} MB total')
    json.dump(manifest, open(os.path.join(
        '/tmp/claude-0/-home-user-Maisondestefanie/f8d3ecfc-ee3c-5319-ae1c-05127152a947/scratchpad',
        'manifest.json'), 'w'), indent=1)
    for k, v in manifest.items():
        print(f"  {k:14s} {v['w']}x{v['h']}  -> {v['src']}")


if __name__ == '__main__':
    main()
