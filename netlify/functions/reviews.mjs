/* ------------------------------------------------------------------
   What reviews-refresh last heard from Google, as plain JSON.

   No key, no Google call: this only reads what the weekly job wrote,
   so serving it to every visitor costs nothing. If the job has never
   run, or ran and failed before it stored anything, this says so with
   204 and the page keeps the number in content.json.

   Written in Netlify's second function format. It has to be: the
   storage credentials are only handed to functions in this format,
   and the older style failed on every call with "the environment has
   not been configured to use Netlify Blobs".
   ------------------------------------------------------------------ */

import { getStore } from '@netlify/blobs';

export default async () => {
  const headers = {
    'Content-Type': 'application/json',
    /* an hour at the edge: the number behind it only moves once a week */
    'Cache-Control': 'public, max-age=300, s-maxage=3600',
    'Netlify-CDN-Cache-Control': 'public, durable, s-maxage=3600'
  };
  try {
    const held = await getStore('reviews').get('google', { type: 'json' });
    if (!held || !held.count) return new Response(null, { status: 204, headers });
    return new Response(JSON.stringify({
      rating: held.rating,
      count: held.count,
      reviews: held.reviews || [],
      checkedAt: held.checkedAt
    }), { status: 200, headers });
  } catch (e) {
    console.error('reviews: ' + e.message);
    headers['X-Store-Note'] = String(e.message || e).slice(0, 180).replace(/[^\x20-\x7e]/g, ' ');
    return new Response(null, { status: 204, headers });
  }
};
