# La Maison de Stefanie — new site + Studio

A rebuild of lamaisondestefanie.com with a proper back office, so Stefanie can
add products, write descriptions and upload photos herself, and every photo she
adds is put through one house treatment so the whole catalogue looks like a
single collection.

Same stack you already work in: static files, GitHub web UI, Netlify,
Firestore. No terminal, no build step, nothing to install.

---

## 1. Her icon — do this before anything else

The favicon is her logo and must not change. The new site references the same
filenames the current site uses, so copying her existing `assets` folder across
keeps it identical.

Full instructions, including how to find the exact filenames she is using now:
**`assets/PUT-HER-FILES-HERE.txt`**.

Nothing else in this project needs her old code. Only the asset files.

> Right now `assets/` holds nothing of hers — only labelled placeholders, one
> per photograph the layout is waiting for. Each placeholder says on its face
> what belongs there. The page works with them in; it only looks like her shop
> once they are replaced.

---

## 2. Put it online (15 minutes)

1. Create a new repository on github.com.
2. **Add file → Upload files**, drag in everything from this zip, commit.
3. Copy her `assets` files in (step 1 above) and commit again.
4. netlify.com → **Add new site → Import an existing project** → pick the repo.
   Build command: leave empty. Publish directory: `.` (already set in
   `netlify.toml`).
5. Point the domain at Netlify when you are ready to cut over. Until then the
   `*.netlify.app` preview URL is a safe place to show her.

At this point the site is live and reads its content from `content.json`.

---

## 3. Give her the Studio (Firebase)

Without this the Studio still works, but it saves to her browser and she has to
download a backup and upload it. With it, she edits and presses Publish and the
site changes. Worth the 20 minutes.

1. console.firebase.google.com → **Add project**.
2. **Build → Firestore Database → Create database** → production mode, region
   `eur3` or `europe-west`.
3. **Build → Authentication → Get started → Email/Password → Enable.**
   Then **Users → Add user** with her email and a password you give her.
4. **Firestore → Rules** → paste the contents of `firestore.rules`, replacing
   the email with hers, then **Publish**.
5. **Project settings → Your apps → Web (`</>`)** → register the app → copy the
   `firebaseConfig` values into `config.js`, and put her email in
   `adminEmails`. Commit `config.js`.

She then goes to `yourdomain.com/studio.html`, signs in, and edits the live
site. Publishing takes about a second.

> The first time she presses Publish, the whole of `content.json` is copied into
> Firestore and becomes the live source. `content.json` stays in the repo as the
> fallback if Firebase is ever unreachable.

---

## 4. Writing help (optional)

The Studio has small green buttons that draft a description in the house voice,
suggest a note pyramid, and translate the English into Greek. They only appear
if an API key is present.

Netlify → **Site configuration → Environment variables → Add**:

```
ANTHROPIC_API_KEY = sk-ant-...
```

Optionally `ANTHROPIC_MODEL` to pin a specific model. Redeploy. The house voice
and the list of words it must never use live in `netlify/functions/ai.js` — edit
that file to change how it writes.

---

## 5. What she can change, and where

Everything below is in the Studio. Nothing here needs you.

| Studio section | What it controls |
|---|---|
| **The shelf** | Every product: name, line, description, notes, price, size, photo, payment link, whether it shows |
| **Categories** | The tabs above the shelf. Add any category — she is not limited to perfume |
| **House look** | The single treatment applied to every photo, and a button to re-make the older ones to match |
| **The bench** | The memories people can pick on the front page, and the notes each one carries |
| **Words** | Every line of copy on the page, in English and Greek |
| **Reviews** | The three quotes in the guest book |
| **Questions** | The FAQ, which also feeds Google's rich results |
| **Shop details** | Address, hours, phone, WhatsApp, Instagram, map, rating |

**Download backup** produces a zip with `content.json` and every photo as a real
`.jpg`. Drag those into GitHub and the site updates without Firebase at all —
which is also the disaster recovery route if Firebase ever goes wrong.

---

## 6. How the photo treatment works

She photographs a candle on the counter with her phone. The Studio then:

1. reads the border of the frame to find the background colour;
2. flood-fills inwards and lifts the product off it, with a feathered edge;
3. stands it on the house backdrop at a fixed size and height, so every product
   in the catalogue is framed identically;
4. drops a soft contact shadow underneath;
5. applies one tone curve — same warmth, contrast, colour depth, grain and
   vignette for every image;
6. compresses it to about 350KB and keeps a copy of her original, so the whole
   catalogue can be re-made if she changes the look later.

If the background is too busy to remove cleanly it says so and falls back to a
square crop with the same grade, rather than producing a bad cutout. Tell her:
plain surface, even light, product filling the middle of the frame. A white
tabletop and a window is enough.

All of it runs in her browser. No image service, no cost, no upload wait.

---

## 7. What is new, and why

The old site was beautiful and told people to visit. It gave them no way to buy
anything, no reason to come back, and no idea she sells anything but perfume.
This one keeps the tone and adds the parts that make money.

- **The bench.** The front page now asks people to pick memories and shows them
  the perfume that would result, then hands them a WhatsApp message with their
  own accord already written in it. It converts a browse into a conversation,
  which is the only step that matters for her.
- **A shelf that exists at all.** Candles, oils, soaps, diffusers, vouchers,
  wedding favours. All editable, all category-driven.
- **Repeat orders.** Her real asset is the formula file. "Made Again" and the
  FAQ say plainly that anyone can reorder from anywhere in the world — that is
  revenue from customers who already left Athens.
- **Vouchers, weddings, hotels.** Highest-margin work, currently invisible.
- **Greek and English throughout**, including the products.
- **Structured data** for the shop, its rating and the FAQ, so Google can show
  the stars and the answers directly.
- **Payment links.** She pastes a Stripe or Revolut link into a product and an
  Order button appears. No checkout to build or maintain.

### Worth doing next

- Swap the sample products for her real ones and photograph them (an afternoon).
- Ask three recent guests for a Google review each; the rating block is the
  strongest thing on the page.
- Print a small card with a QR to the site and drop it in every bag — that is
  what drives the reorders.
- Talk to two or three Plaka hotel concierges about the voucher.

---

## Files

```
index.html            the site
studio.html           the back office
config.js             the only file needing edits (Firebase + house look defaults)
content.json          all content — the fallback source, and the export format
privacy.html          privacy page
firestore.rules       paste into Firebase
netlify.toml          headers and function config
netlify/functions/ai.js   writing help (needs ANTHROPIC_API_KEY)
robots.txt · sitemap.xml · site.webmanifest
assets/               her logo, photos and video go here
```

## The front page, and how it is put together

The homepage is one story told in six chapters, and the chapter rail down the
right-hand side is the reader's place in it:

| # | Section | What it does |
|---|---|---|
| 01 | Hero | *Your Story. Your Scent.* — the offer, and the two ways in |
| 02 | A memory, distilled | the three steps, stated plainly |
| 03 | The bench | she picks memories, sees the accord, sends it on WhatsApp |
| 04 | Composed by hand | the essences chosen, the formula written out |
| 05 | Bottled and sealed | filled and sealed at the counter, kept on file |
| 06 | Visit | address, hours, telephone, and the map behind a button |

Everything after that — her story, the session, the shelf, the guest book and
the questions — supports those six. The one thing the page is for is getting
someone to message or walk in.

All of it is driven from `content.json` (or Firestore once it is connected),
so every word, price and photograph is hers to change from the Studio. There
is still no build step: the page is one file, the styles and the script are
inside it, and nothing is compiled.

Motion is small on purpose — the layers drift, headings arrive, the formula is
written out — and all of it is switched off for anyone whose device asks for
reduced motion. The page reads correctly before any of it runs.
