/* ------------------------------------------------------------
   Writing help for the Studio.
   Set ANTHROPIC_API_KEY in Netlify → Site settings → Environment
   variables. Without it the Studio simply hides the AI buttons.
   ------------------------------------------------------------ */

const MODEL = process.env.ANTHROPIC_MODEL || "claude-sonnet-4-6";

const VOICE = `You write for La Maison de Stefanie, a family perfume house on Mnisikleous Street in Plaka, Athens.
Stefanie blends bespoke extrait de parfum by hand, in front of the customer, from the memory they describe.
The house also makes candles, diffusers, body oils, soaps, gift vouchers and wedding favours.

Voice: plain, warm, unhurried, quietly confident. Short sentences. British spelling.
Concrete over poetic — name a material, a place, a time of day, a thing that happened.
Never use: luxurious, exquisite, indulge, elevate, journey, olfactory experience, sensorial,
unleash, timeless elegance, captivating, symphony, notes that dance. No exclamation marks.
Do not oversell. Do not invent prices, ingredients that were not given, or claims about awards.`;

exports.handler = async (event) => {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS"
  };
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers };
  if (event.httpMethod !== "POST") return { statusCode: 405, headers, body: '{"error":"POST only"}' };

  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) return { statusCode: 503, headers, body: '{"error":"No API key set"}' };

  let body = {};
  try { body = JSON.parse(event.body || "{}"); } catch (e) {}
  const { task } = body;

  if (task === "ping") return { statusCode: 200, headers, body: '{"ok":true}' };

  let prompt;
  if (task === "write") {
    const { field, name, tagline, story, notes } = body;
    const known = [
      name && `Name: ${name}`,
      tagline && `Existing line: ${tagline}`,
      story && `Existing description: ${story}`,
      notes && [notes.top, notes.heart, notes.base].some(a => a && a.length) &&
        `Notes — top: ${(notes.top || []).join(", ")}; heart: ${(notes.heart || []).join(", ")}; base: ${(notes.base || []).join(", ")}`
    ].filter(Boolean).join("\n") || "Nothing yet.";

    const ask = {
      name: "Suggest one product name. Two or three words at most, in the spirit of the house — a place, a person, a moment. Reply with the name only.",
      tagline: "Write one line to sit under the name. Under twelve words. It should say something true and specific, not a slogan. Reply with the line only.",
      story: "Write the product description. Two or three short sentences, about 45 words. Say what it is, what it smells of or does, and one honest detail about how it is made. Reply with the description only."
    }[field] || "Write a short product description. Reply with the text only.";

    prompt = `${VOICE}\n\nWhat is known about this item:\n${known}\n\n${ask}`;
  } else if (task === "notes") {
    const { name, tagline, story } = body;
    prompt = `${VOICE}\n\nItem: ${name}\n${tagline || ""}\n${story || ""}\n\n` +
      `Suggest a plausible note pyramid for this perfume, using real perfumery materials. ` +
      `Two or three per tier. Prefer materials a Greek perfumer would actually reach for.\n` +
      `Reply with JSON only, no markdown fences: {"top":[],"heart":[],"base":[]}`;
  } else if (task === "translate") {
    prompt = `Translate this shop copy from English into natural Modern Greek as a Greek perfumer would write it — ` +
      `not word for word, and not formal katharevousa. Keep perfumery terms that Greek customers use in French or English ` +
      `(extrait de parfum, eau de parfum) as they are. Keep any arrays as arrays.\n\n` +
      `Reply with JSON only, no markdown fences, using exactly the same keys as the input.\n\n` +
      `Input:\n${JSON.stringify(body.source, null, 2)}`;
  } else {
    return { statusCode: 400, headers, body: '{"error":"Unknown task"}' };
  }

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 1200,
        messages: [{ role: "user", content: prompt }]
      })
    });
    if (!r.ok) {
      const detail = await r.text();
      return { statusCode: 502, headers, body: JSON.stringify({ error: "Upstream error", detail: detail.slice(0, 400) }) };
    }
    const data = await r.json();
    let text = (data.content || []).filter(b => b.type === "text").map(b => b.text).join("\n").trim();
    text = text.replace(/^```(?:json)?\s*/i, "").replace(/```$/, "").trim();
    return { statusCode: 200, headers, body: JSON.stringify({ text }) };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: String(e) }) };
  }
};
