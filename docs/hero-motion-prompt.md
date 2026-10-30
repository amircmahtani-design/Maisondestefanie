# Hero motion prompt and asset map

## Creative prompt

Create a restrained, cinematic 8-second perfume-making hero loop for La
Maison de Stefanie in Plaka, Athens. Preserve the existing visual idea:
rose petals being extracted into perfume through the copper still. Keep
the narrative and objects recognizable in this order:

1. A single rose in darkness.
2. Petals loosen and drift down toward a glass essence bowl.
3. The copper still begins to work: warm light catches the copper, a
   fine thread of steam rises, and the essence/petals feel as if they
   are being drawn through the distillation.
4. Resolve to the finished perfume bottle among roses while a few petals
   continue moving gently past it.

One fixed camera, intimate close framing, low-key chiaroscuro, nearly
black surroundings, one warm amber source from the side, rich copper,
rose and glass detail, deep shadows, no flat fill light. Motion is slow,
continuous and physically plausible: petals fall under gravity, steam
curls softly, highlights breathe with the flame. Use overlapping
dissolves between the four scenes and a seamless return to the opening
rose. Hold the bottle steady while petals move. Keep the pace quiet,
luxurious and tactile.

Match the existing photographs and artwork as visual references. Do not
change the story into a generic perfume advertisement; do not add new
props, text, logos, people, hands, labels, floating particles, camera
moves, fast cuts, bright backgrounds or extra bottles. Keep packaging
and bottle shape consistent with the supplied reference frames. If using
real video, retain the same low-key grade and avoid generated faces or
hands. Prefer the existing chapter images as the visual anchors and
animate only the transition, steam and petals.

## Suggested timing

- 0.0–1.4 s: rose in warm side light; a petal begins to release.
- 1.4–3.0 s: petal travels toward the essence bowl; dissolve into the bowl.
- 3.0–5.2 s: copper still, gentle steam and warm reflected flame; essence
  extraction is the visual center.
- 5.2–7.4 s: bottle among roses, petals crossing the foreground.
- 7.4–8.0 s: petal motion and light align with the opening composition
  for a clean loop.

Use a locked camera and matching exposure, white balance, lens, grain and
black level across all shots. Keep the subject and petal motion inside
the existing crop-safe area for desktop and mobile. Export a 6–10 second
loop, ideally 24 fps, with desktop and mobile crops. Keep the desktop
WebM under about 4 MB and mobile under about 1.5 MB when practical.
Provide a poster still. Respect reduced-motion and data-saver settings.

## Existing hero assets

These are the committed chapter anchors; keep them in sequence:

- Rose: `assets/img/scene-rose-470.webp`,
  `assets/img/scene-rose-700.webp`, `assets/img/scene-rose-941.webp`
- Essence bowl: `assets/img/scene-essence-470.webp`,
  `assets/img/scene-essence-700.webp`, `assets/img/scene-essence-941.webp`
- Copper still: `assets/img/scene-still-470.webp`,
  `assets/img/scene-still-700.webp`, `assets/img/scene-still-940.webp`
- Bottle among roses: `assets/img/frame-00-560.webp` through
  `frame-08-560.webp`, and matching `frame-00-880.webp` through
  `frame-08-880.webp`. The current player advances and reverses the
  frames to keep the movement continuous. `frame-04` is the resting
  image for a still page and reduced-motion users.

The site now uses a 1250 ms chapter dissolve, with each bottle/petal frame
held for 220 ms and crossfaded over 520 ms. This preserves the original
art and slows the movement enough to read as a film-like loop.

## Optional real bench footage

For the optional Stefanie-at-work hero film, record 6–10 seconds of her
actually working at the bench. Keep the camera still, include the copper
still and the petal/essence extraction in frame, and use the same single
warm side light and dark grade. Export as:

- `assets/stefanie_hero_loop.webm` (desktop)
- `assets/stefanie_hero_loop_mobile.webm` (mobile)

The footage should be authentic to Stefanie and her shop. Generated
motion is not a substitute for a real clip of her.

## Generated shelf and place concepts

The product and location concept sources and all responsive exports are
kept in `assets/source/generated-products/`,
`assets/source/generated-places/`, and `assets/img/`. They share the
same dark surface and warm side light. They are clearly marked as
generated concept artwork in `assets/GENERATED-CONCEPTS.md`.

## The six pages, and their first screens

The site is no longer one scrolling page. index.html keeps the four
chapters; maison, bespoke, story, creations and visit each open on a
still of their own, under `assets/heroes/<page>/`, in three
compositions — 16:9 for a wide screen, 4:3 for a tablet, 9:16 for a
phone. The browser chooses between them with `<picture>` media queries,
so each shape of screen gets a photograph composed for it rather than a
crop of one composed for something else.

The composition rule is the same on every page: subject on the right,
the left half dark and quiet for the headline; on a phone the subject
moves to the top half and the words sit in the dark beneath it.

The home artwork is wired to `heroPoster` — the still the first screen
falls back to when the chapters cannot play (reduced motion, data
saver, or before the first chapter lands).
