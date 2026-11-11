/* ------------------------------------------------------------------
   Her rating on Google, fetched once a week.

   The number of reviews is on three parts of the site — the sentence
   that opens the guest book, the figure under the stars, and the
   structured data Google itself reads — and all three take it from one
   field. That field was typed by hand and had gone stale by 119.

   This runs on a schedule (netlify.toml, [functions."reviews-refresh"])
   and writes what Google says into a blob. reviews.js serves it. The
   page asks for it after it has already drawn itself, so nothing waits
   on Google and a failure here leaves the number in content.json
   showing, which is the behaviour the site had before.

   Set GOOGLE_PLACES_KEY in Netlify → Site configuration → Environment
   variables. Nothing works without it and nothing breaks either.
   Optionally set GOOGLE_PLACE_ID to skip the one lookup that finds it.

   Billing: rating and userRatingCount are Places API "Enterprise"
   fields, $20 per 1,000 requests with the first 1,000 a month free.
   Once a week is 4.3 a month. Put a quota cap on the key in Google
   Cloud so a mistake here can never cost anything.
   ------------------------------------------------------------------ */

const { getStore } = require('@netlify/blobs');

const PLACE = 'La Maison de Stefanie, Mnisikleous 10, Plaka, Athens 105 56, Greece';
const STORE = 'reviews';
const KEY = 'google';

/* The place id is stable, so it is looked up once and kept. */
async function placeId(key, store) {
  if (process.env.GOOGLE_PLACE_ID) return process.env.GOOGLE_PLACE_ID;
  const held = await store.get(KEY, { type: 'json' }).catch(() => null);
  if (held && held.placeId) return held.placeId;

  const r = await fetch('https://places.googleapis.com/v1/places:searchText', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': key,
      'X-Goog-FieldMask': 'places.id'
    },
    body: JSON.stringify({ textQuery: PLACE, maxResultCount: 1 })
  });
  if (!r.ok) throw new Error('search ' + r.status + ' ' + (await r.text()).slice(0, 200));
  const j = await r.json();
  const id = j.places && j.places[0] && j.places[0].id;
  if (!id) throw new Error('no place matched ' + PLACE);
  return id;
}

exports.handler = async () => {
  const key = process.env.GOOGLE_PLACES_KEY;
  if (!key) {
    console.log('reviews-refresh: no GOOGLE_PLACES_KEY set, nothing to do');
    return { statusCode: 200, body: 'no key' };
  }

  try {
    /* getStore can throw on its own, and when it did the whole function
       fell over with a 502 instead of the quiet 200 everything else here
       is built to return. It belongs inside the net, not outside it. */
    const store = getStore(STORE);
    const id = await placeId(key, store);
    const r = await fetch(
      'https://places.googleapis.com/v1/places/' + encodeURIComponent(id)
        + '?fields=rating,userRatingCount,reviews&key=' + encodeURIComponent(key));
    if (!r.ok) throw new Error('details ' + r.status + ' ' + (await r.text()).slice(0, 200));
    const j = await r.json();

    const count = Number(j.userRatingCount);
    const rating = Number(j.rating);
    /* A place with no reviews, or a response missing them, is not a
       reason to publish a zero over a real number. */
    if (!Number.isFinite(count) || count < 1 || !Number.isFinite(rating)) {
      throw new Error('no usable rating in ' + JSON.stringify(j).slice(0, 200));
    }

    /* Google hands back up to five and does not say in what order.
       Only the five-star ones are kept — the guest book's own line is
       that every guest who writes leaves five stars, and a four beside
       it would make a liar of her — and of those, the three most
       recently written. Her guests' words are stored exactly as they
       came, never trimmed or tidied, with the name, the score and when
       it was written, which is what Google asks of anyone showing
       them. */
    const newest = (Array.isArray(j.reviews) ? j.reviews : [])
      .filter(v => v && v.text && v.text.text && v.authorAttribution)
      .filter(v => Number(v.rating) === 5)
      .sort((a, b) => String(b.publishTime || '').localeCompare(String(a.publishTime || '')))
      .slice(0, 3)
      .map(v => ({
        name: v.authorAttribution.displayName || '',
        profile: v.authorAttribution.uri || '',
        stars: Number(v.rating) || 5,
        text: v.text.text,
        lang: v.text.languageCode || '',
        when: v.relativePublishTimeDescription || '',
        at: v.publishTime || '',
        href: v.googleMapsUri || ''
      }));

    const was = await store.get(KEY, { type: 'json' }).catch(() => null);
    await store.setJSON(KEY, {
      placeId: id,
      rating: Math.round(rating * 10) / 10,
      count,
      /* if a run comes back without them, the ones already stored stay */
      reviews: newest.length ? newest : (was && was.reviews) || [],
      checkedAt: new Date().toISOString()
    });
    console.log('reviews-refresh: ' + (was ? was.count + ' → ' : '') + count
      + ' reviews, ' + rating + ', kept ' + newest.length + ' five-star of '
      + ((j.reviews || []).length) + ' returned');
    return { statusCode: 200, body: JSON.stringify({ rating, count }) };
  } catch (e) {
    /* Leave whatever is stored alone: a stale real number beats none. */
    console.error('reviews-refresh failed, keeping what is stored:', e.message);
    return { statusCode: 200, body: 'kept: ' + e.message };
  }
};
