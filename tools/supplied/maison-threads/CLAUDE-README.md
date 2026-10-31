# Claude — Replace the five Maison "Choose a Thread" images ONLY

Repository: `amircmahtani-design/Maisondestefanie`
Target page: `maison.html` / five thread cards in `content.json` (`organ.threads`).

The correct five mappings are:

| Card in site | Source JPEG, 1400 × 1800 | Drop-in assets (WebP) |
|---|---|---|
| Places you remember | 01-places-you-remember.jpg | assets/img/thread-places-560.webp and thread-places-900.webp |
| The sea | 02-the-sea.jpg | assets/img/thread-sea-560.webp and thread-sea-900.webp |
| Someone in particular | 03-someone-in-particular.jpg | assets/img/thread-someone-560.webp and thread-someone-900.webp |
| A moment that stayed | 04-a-moment-that-stayed.jpg | assets/img/thread-moment-560.webp and thread-moment-900.webp |
| Something you lost | 05-something-you-lost.jpg | assets/img/thread-lost-560.webp and thread-lost-900.webp |

## Implementation

1. Copy the ten included `.webp` files into `assets/img/`, replacing the original ten WebP files in the repository. Keep filenames unchanged so existing src/srcset references work automatically.
2. No HTML, JavaScript, CSS, `content.json`, navigation, page hero, homepage film, or other pages should change.
3. Check each card visually at desktop and mobile width, ensuring that the photo shown matches the subject. Do not swap the images.
4. Provide a staging preview before publishing if any layout changes seem necessary. None should be necessary.
5. Keep the five master JPEGs as originals in `tools/supplied/maison-threads/` if storing source photos for future exports; don't link to them in the live page.
6. These are AI-generated photographic **concept visuals**, not authentic documentary photographs of Stefanie's actual shop or identifiable people. Do not represent the anonymous model or fictional location image as a factual photo.

## Quality notes

- Each JPEG is encoded at 1400×1800, sRGB, quality 96, no added sharpening, no text.
- The original image-generation resolution is smaller than the master JPEG exports: the person and night shopfront are extended from narrow portrait crops, with soft ambient sides. These files are for relatively small cards, not full-screen 4K hero uses.
- Never upscale browser assets on-device when smaller responsive WebPs are supplied.

Only this Maison card section is in scope.
