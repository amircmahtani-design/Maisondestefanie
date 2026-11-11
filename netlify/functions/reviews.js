/* ------------------------------------------------------------------
   What reviews-refresh last heard from Google, as plain JSON.

   No key, no Google call: this only reads the blob the weekly job
   wrote, so the cost of serving it to every visitor is nothing. If the
   job has never run, or ran and failed before it ever stored anything,
   this says so with 204 and the page keeps the number in content.json.
   ------------------------------------------------------------------ */

const { getStore } = require('@netlify/blobs');

exports.handler = async () => {
  const headers = {
    'Content-Type': 'application/json',
    /* an hour at the edge: the number behind it only moves once a week */
    'Cache-Control': 'public, max-age=300, s-maxage=3600',
    'Netlify-CDN-Cache-Control': 'public, durable, s-maxage=3600'
  };
  try {
    const held = await getStore('reviews').get('google', { type: 'json' });
    if (!held || !held.count) return { statusCode: 204, headers };
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        rating: held.rating, count: held.count,
        reviews: held.reviews || [], checkedAt: held.checkedAt
      })
    };
  } catch (e) {
    console.error('reviews: ' + e.message);
    return { statusCode: 204, headers };
  }
};
