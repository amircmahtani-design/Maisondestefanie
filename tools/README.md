# How the temporary pictures were made

Everything in `assets/img` is original artwork rendered by these scripts.
It is not photography and it is not stock. It exists so the layout could
be judged with real pictures in it, and it is meant to be replaced by
Stefanie's own photographs through Studio → Pictures.

Nothing here runs on the site. It is kept only so the set can be
regenerated or adjusted before the real photographs arrive. Delete the
whole folder once they do.

## What is where

    kit.py          the house light: palette, blooms, falloff, a bottle,
                    a petal — the parts every scene is built from
    s_bottle.py     the flacon, close up, on transparency
    s_objects.py    the blending bowl and the rose, on transparency
    s_rooms.py      the nine wider frames
    s_products.py   the twelve shelf items, on the house backdrop
    grade.py        one film grade over all of it, so separately built
                    frames read as a single shoot
    cutouts.py      grades, lifts and trims the three hero objects
    build.py        writes the scenes out as SVG
    render.mjs      renders each SVG in Chromium (SVG filters do the
                    lighting, blurs and texture)
    export.py       resizes to the widths the page asks for, writes WebP,
                    and prints the srcset strings for content.json
    scenes.py       the four chapter photographs. These are whole frames,
                    not objects cut out on black, so nothing is removed:
                    the script only sets a true black point and grades
                    them so the four read as one shoot, then writes the
                    widths the page asks for. Reads
                    tools/supplied/{rose,vessel,compose,bottle}.png, which
                    are not committed — drop the originals there first.
    heroloop.py     the hero film: takes the rendered still and moves it
                    — a slow push, candlelight that gutters, a flame that
                    leans, haze drifting — and encodes VP9 WebM plus
                    H.264 MP4 at desktop and phone sizes. Every motion
                    runs a whole number of cycles over the loop, so the
                    last frame meets the first without a seam.

## Regenerating

    pip install Pillow numpy
    python3 build.py && node render.mjs jobs.json
    python3 cutouts.py
    python3 export.py        # writes into ../assets/img
    pip install imageio-ffmpeg && python3 heroloop.py   # the hero film

The ffmpeg that ships with Playwright carries VP8 and WebM only, which
is why heroloop.py pulls a full build from PyPI instead.

`export.py` also writes `manifest.json`, whose `srcset` strings are what
`content.json` carries for each picture slot.

## Why the srcset survives Stefanie replacing a picture

Each slot stores `srcsetFor` alongside `srcset`. The page only uses the
srcset while `srcsetFor` still equals `src`. The moment she uploads her
own photograph through the Studio, `src` changes, the two disagree, and
the page quietly falls back to the single image she uploaded.
