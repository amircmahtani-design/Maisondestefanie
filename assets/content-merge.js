/* ------------------------------------------------------------------
   Two hands on the same content, without either rubbing out the other.

   content.json is built with the site and is mine. The Studio writes to
   Firestore and is Stefanie's. Until now the Studio saved a complete
   copy of everything, so from her first Publish every one of the several
   hundred fields counted as hers, including the ones she had never
   opened, and anything I changed afterwards never reached the page.

   So the Studio now saves only what she has actually changed, and the
   page is content.json with her changes laid over it. A sentence she has
   rewritten stays rewritten. A section she has never touched follows the
   build. Neither of us has to ask the other first.

   Deleting is the one thing a patch cannot say by omission, because an
   item missing from her side is indistinguishable from an item I have
   just added. So a deletion is written down: _removed carries the ids
   she has taken away, and they stay away.

   Both the site and the Studio read this file. There is one definition
   of how the two sides combine and it lives here.
   ------------------------------------------------------------------ */
(function (root) {
  'use strict';

  var SCHEMA = 2;

  function isObj(v) {
    return v !== null && typeof v === 'object' && !Array.isArray(v);
  }
  /* An array the two sides can be reasoned about item by item: every
     entry an object carrying an id. Products, categories, reviews and
     the questions in Good to know are all of this shape. Anything else
     — a list of bullets, a list of notes — is taken whole or not at all,
     because there is no honest way to line up two lists of strings. */
  function keyed(a) {
    return Array.isArray(a) && a.length > 0 && a.every(function (x) {
      return isObj(x) && typeof x.id === 'string' && x.id;
    });
  }
  function byId(a) {
    var m = {};
    (a || []).forEach(function (x) { if (isObj(x) && x.id) m[x.id] = x; });
    return m;
  }
  function same(a, b) {
    if (a === b) return true;
    if (typeof a !== typeof b) return false;
    if (a === null || b === null) return a === b;
    if (typeof a !== 'object') return a === b;
    return JSON.stringify(a) === JSON.stringify(b);
  }
  function clone(v) {
    return v === undefined ? v : JSON.parse(JSON.stringify(v));
  }

  /* ---- what she changed, against what was built ------------------ */
  function diff(base, cur) {
    if (!isObj(base) || !isObj(cur)) {
      return same(base, cur) ? undefined : clone(cur);
    }
    var out = {}, had = false;

    Object.keys(cur).forEach(function (k) {
      var b = base[k], c = cur[k];

      if (keyed(b) || (keyed(c) && Array.isArray(b))) {
        var d = diffList(b || [], c || []);
        if (d) { out[k] = d; had = true; }
        return;
      }
      if (isObj(b) && isObj(c)) {
        var sub = diff(b, c);
        if (sub !== undefined && Object.keys(sub).length) { out[k] = sub; had = true; }
        return;
      }
      if (!same(b, c)) { out[k] = clone(c); had = true; }
    });

    /* a key she has emptied that the build still carries */
    Object.keys(base).forEach(function (k) {
      if (!(k in cur)) { out[k] = null; had = true; }
    });

    return had ? out : undefined;
  }

  function diffList(base, cur) {
    var B = byId(base), C = byId(cur);
    var items = {}, had = false;

    Object.keys(C).forEach(function (id) {
      if (!B[id]) { items[id] = clone(C[id]); had = true; return; }  /* hers alone */
      var d = diff(B[id], C[id]);
      if (d !== undefined && Object.keys(d).length) { items[id] = d; had = true; }
    });

    var removed = Object.keys(B).filter(function (id) { return !C[id]; });
    if (removed.length) had = true;

    /* order is only worth writing down when she has moved something */
    var curOrder = cur.map(function (x) { return x.id; });
    var baseOrder = base.map(function (x) { return x.id; })
                        .filter(function (id) { return removed.indexOf(id) < 0; });
    var addedAtEnd = baseOrder.concat(curOrder.filter(function (id) { return !B[id]; }));
    var moved = JSON.stringify(curOrder) !== JSON.stringify(addedAtEnd);
    if (moved) had = true;

    if (!had) return undefined;
    var out = { _list: true };
    if (Object.keys(items).length) out._items = items;
    if (removed.length) out._removed = removed;
    if (moved) out._order = curOrder;
    return out;
  }

  /* ---- the build, with her changes laid over it ------------------ */
  function merge(base, patch) {
    if (patch === undefined) return clone(base);
    if (patch === null) return undefined;
    if (!isObj(base) || !isObj(patch)) return clone(patch);
    if (patch._list) return mergeList(Array.isArray(base) ? base : [], patch);

    var out = clone(base) || {};
    Object.keys(patch).forEach(function (k) {
      var p = patch[k];
      if (p === null) { delete out[k]; return; }
      if (isObj(p) && p._list) { out[k] = mergeList(out[k] || [], p); return; }
      if (isObj(p) && isObj(out[k])) { out[k] = merge(out[k], p); return; }
      out[k] = clone(p);
    });
    return out;
  }

  function mergeList(base, patch) {
    var removed = patch._removed || [];
    var items = patch._items || {};
    var out = [];
    var seen = {};

    /* what was built, minus what she has deleted, plus her changes to it */
    base.forEach(function (x) {
      if (!isObj(x) || !x.id) { out.push(clone(x)); return; }
      if (removed.indexOf(x.id) >= 0) return;
      seen[x.id] = true;
      out.push(items[x.id] ? merge(x, items[x.id]) : clone(x));
    });
    /* and anything she has added that the build knows nothing about */
    Object.keys(items).forEach(function (id) {
      if (!seen[id] && removed.indexOf(id) < 0) out.push(clone(items[id]));
    });

    if (patch._order && patch._order.length) {
      var pos = {};
      patch._order.forEach(function (id, i) { pos[id] = i; });
      out.sort(function (a, b) {
        var ai = pos[a && a.id], bi = pos[b && b.id];
        if (ai == null && bi == null) return 0;
        if (ai == null) return 1;   /* added since she last ordered: to the end */
        if (bi == null) return -1;
        return ai - bi;
      });
    }
    return out;
  }

  /* ---- plain English, for the Studio to show --------------------- */
  /* Every field the build has changed since she published, so she can
     see what is coming rather than find out by looking at the page. */
  function changedFields(oldBase, newBase, patch, limit) {
    var out = [];
    var cap = limit || 200;
    (function walk(a, b, path) {
      if (out.length >= cap) return;
      if (!isObj(a) || !isObj(b)) return;
      Object.keys(b).forEach(function (k) {
        if (out.length >= cap) return;
        var p = path ? path + '.' + k : k;
        if (Array.isArray(a[k]) || Array.isArray(b[k])) {
          if (!same(a[k], b[k])) out.push({ path: p, kind: 'list' });
          return;
        }
        if (isObj(a[k]) && isObj(b[k])) { walk(a[k], b[k], p); return; }
        if (!same(a[k], b[k])) {
          out.push({
            path: p,
            was: a[k] === undefined ? null : a[k],
            now: b[k],
            hers: overridden(patch, p)
          });
        }
      });
    })(oldBase || {}, newBase || {}, '');
    return out;
  }

  function overridden(patch, path) {
    var node = patch;
    var parts = path.split('.');
    for (var i = 0; i < parts.length; i++) {
      if (!isObj(node)) return false;
      if (!(parts[i] in node)) return false;
      node = node[parts[i]];
    }
    return true;
  }

  root.LMSContent = {
    SCHEMA: SCHEMA,
    diff: diff,
    merge: merge,
    changedFields: changedFields,
    isPatchDoc: function (d) { return !!(d && d._schema >= 2); }
  };
})(window);
