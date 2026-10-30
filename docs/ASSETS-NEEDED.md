# What to send, and exactly how big

Every soft picture on this site is soft for one reason: the file behind
it has fewer pixels than the screen asks for. Nothing in code recovers
that. This is the whole list, measured against the real viewports, with
the size each one has to be.

**Rule of thumb for all of it:** PNG or JPEG at maximum quality, sRGB, no
sharpening applied, no watermark, no text burnt in. Send them larger than
asked rather than smaller — every script here downscales cleanly and
nothing enlarges.

---

## 1. The home page's first screen — the film · THE BIGGEST WIN

What is there now: sixteen storyboard frames at **1280 × 720**. On a 1440
laptop at 2× the plate renders into 3144 device pixels with 1280 of real
detail behind it. That is the softness; it is not recoverable.

| | aspect | send at least | ideal |
|---|---|---|---|
| wide, one per scene | 16:9 | 2560 × 1440 | **3840 × 2160** |
| upright, one per scene | 9:16 | 1170 × 2080 | **1620 × 2880** |

Four scenes, in this order, which is the story and does not change:

1. **The rose** — the bloom, petals about to let go
2. **The essence** — the glass bowl, petals on the liquid
3. **The still** — copper, the gooseneck, vapour
4. **The flacon** — the finished bottle among roses

So **8 files** minimum. Name them anything; drop them in `tools/supplied/`
and say which is which.

Composition, for both shapes:
- Near-black ground, one warm copper source from the side, everything
  else falling into shadow. No white, no daylight.
- **Wide:** subject on the right, the left 40% dark and empty — the
  headline is read there.
- **Upright:** subject in the top two thirds, the bottom third dark and
  empty — the words sit under it.
- Camera and subject **locked** within a scene. The motion is built in
  code over the top of a still plate; a scene that moves fights it.

If you can also send **more scenes** — a hand at the bench, the shelf of
essences, the stopper going in — the sequence gets longer and varies
more. Each extra scene is one wide and one upright file and plugs
straight in.

---

## 2. The five page openings

What is there now: **1672 × 941** artwork. Good on a phone (1.24× up),
good on an iPad (1.13×), soft on a desktop (**1.72×**).

| | aspect | send at | used for |
|---|---|---|---|
| `desktop` | 16:9 | **3840 × 2160** | laptops, tablets on their side |
| `ipad` | 4:3 | **2800 × 2100** | tablets held upright |
| `iphone` | 9:16 | **1800 × 3200** | phones |

Five pages — **maison, bespoke, story, creations, visit** — so **15
files**, in folders of those names, each holding `desktop.png`,
`ipad.png`, `iphone.png`. Then:

    python3 tools/heroes.py <that folder>

Same composition rule as above: subject right and left dark on the wide
ones, subject top and bottom dark on the upright ones.

---

## 3. Stefanie's photograph

What is there now: **1400 × 939**, cropped to 751 × 939 for the site. It
carries the home page and the Story page and it renders at about 1.5× on
a retina screen — the softest thing on either page after the heroes.

Send the **original camera file** — whatever came off the card, uncropped
and unresized. Anything above 2400px on the long edge fixes it outright.
`tools/portrait.py` re-cuts the window.

---

## 4. The twelve products

What is there now: generated concept artwork, not photographs of her
actual products. They are marked as concepts in the asset guide and
should not go to print as if they were real.

Send **1600 × 2000** each (upright 4:5), all twelve shot together on the
same dark surface under one warm side light, so the shelf reads as one
set:

    p1  The Bespoke Session      p7   Body Oil
    p2  Made Again               p8   Cold-Pressed Soap
    p3  Mnisikleous              p9   House Candle
    p4  Chios                    p10  Reed Diffuser
    p5  Kyria                    p11  Bespoke Voucher
    p6  The Perfume You Lost     p12  Weddings & Events

A single wide shot of the whole shelf, **3000 px on the long edge**, would
also replace a generated location image.

---

## 5. The shop itself

Three generated concept images stand in for real places:

- the room from the doorway, **3000 × 1280** or wider
- the shopfront at Mnisikleous 10 at dusk, **2000 × 2500**
- the Plaka steps, **2000 × 2500**

---

## 6. Footage

`lamaisondestefanie.com/assets/house.mp4` is real footage of Stefanie at
her bench — her products on the counter, the stock bottles behind her. It
is daylight and documentary rather than dark and cinematic, so it wants
grading before it can sit in these pages, but it is the only real moving
picture of her that exists. The original file at full resolution, rather
than the 2.4 MB web copy, would be the thing to send.

---

## What I do when each one lands

| you send | I run | what changes |
|---|---|---|
| film scenes | `tools/filmplates.py` | the first screen, every shape |
| page artwork | `tools/heroes.py` | that page's opening |
| her portrait | `tools/portrait.py` | home page and Story |
| product shots | existing slots | the shelf |
| location shots | existing slots | Visit, Maison |

Nothing else has to change. Every one of these scripts is sized from its
own master, so a bigger master is the entire upgrade.
