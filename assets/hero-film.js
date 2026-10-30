/* ══════════════════════════════════════════════════════════════
   THE FIRST SCREEN, AS A FILM

   The storyboard is sixteen keyframes, and between any two of them the
   camera and the subject have moved. Playing them would jump. So one
   frame per act is held as a fixed plate — locked camera, locked
   subject — and everything that is supposed to move is built here and
   animated over it as its own layer:

     1  the rose      petals let go, turn, and fall away down-left
     2  the bowl      a petal lands, and the ring it makes opens and goes
     3  the still     vapour lifts and curls, a drop gathers and falls
     4  the bottle    a drop goes in, petals cross the foreground

   The camera is the plate's own slow move, different in each act —
   a drift across, a breath of a dolly — so it never reads as the page
   scrolling. Scenes cross-fade; nothing cuts.

   Nothing here runs under prefers-reduced-motion: the act you arrive on
   is held still and that is the whole of it.
   ══════════════════════════════════════════════════════════════ */

const STILL = matchMedia('(prefers-reduced-motion: reduce)');
const WIDE  = matchMedia('(min-aspect-ratio: 1/1)');

const PETALS = [1, 2, 3, 4, 5, 6].map(n => `assets/hero/petal-${n}.webp`);

/* Where each act's plate comes from, per shape of screen.
   A 16:9 screen takes the motion pack's frame, which is 1280 x 720 and
   the best wide source there is.
   An upright screen used to take a 9:16 window of that same frame — 405
   by 720, a third of a megapixel, stretched across a phone that wants
   three. The house's own four photographs are upright already, within a
   thousandth of 9:16, and carry 1.4 to 1.6 megapixels each: five times
   the detail, no crop at all, and they are the same rose, the same bowl,
   the same still and the same flacon. They are used as they are, not
   re-encoded, so nothing is lost a second time. */
const PLATES = [
  { wide: 'assets/hero/plate-1-wide.webp', tall: 'assets/img/scene-rose-941.webp' },
  { wide: 'assets/hero/plate-2-wide.webp', tall: 'assets/img/scene-essence-941.webp' },
  { wide: 'assets/hero/plate-3-wide.webp', tall: 'assets/img/scene-still-940.webp' },
  { wide: 'assets/hero/plate-4-wide.webp', tall: 'assets/img/frame-00-880.webp' },
];

/* Where things are in each plate, as a fraction of it. Measured off the
   keyframes, not guessed: the rose's heart, the line of the liquid, the
   lip of the spout, the mouth of the bottle. */
const ACTS = [
  { n: 1, rose:  [0.72, 0.33] },
  { n: 2, water: 0.71, land: [[0.61, 0.71], [0.44, 0.74]] },
  { n: 3, spout: [0.13, 0.83], steam: [[0.30, 0.55], [0.46, 0.44], [0.17, 0.62]] },
  { n: 4, neck:  [0.54, 0.26] },
];

const HOLD  = 3600;   /* each act */
const FADE  = 1400;   /* and the dissolve between two of them */

let at = 0, timer = 0, host = null, held = false;

const el = (cls, tag = 'div') => {
  const e = document.createElement(tag);
  e.className = cls;
  return e;
};

/* ── the plate ─────────────────────────────────────────────────── */
function plate(act) {
  const img = el('fh-plate', 'img');
  img.alt = '';
  img.decoding = 'async';
  img.src = PLATES[act.n - 1][WIDE.matches ? 'wide' : 'tall'];
  if (act.n === 1) img.fetchPriority = 'high';
  else img.loading = 'lazy';
  return img;
}

/* ── petals: they let go, turn as they go, and are gone ─────────── */
function petal(from, to, opts = {}) {
  const p = el('fh-petal', 'img');
  p.alt = '';
  p.decoding = 'async';
  p.src = PETALS[opts.sprite ?? Math.floor(Math.random() * PETALS.length)];
  p.style.setProperty('--x0', from[0] * 100 + '%');
  p.style.setProperty('--y0', from[1] * 100 + '%');
  p.style.setProperty('--dx', (to[0] - from[0]) * 100 + 'vw');
  p.style.setProperty('--dy', (to[1] - from[1]) * 100 + 'vh');
  p.style.setProperty('--r0', (opts.r0 ?? 0) + 'deg');
  p.style.setProperty('--r1', (opts.r1 ?? 200) + 'deg');
  p.style.setProperty('--sz', (opts.size ?? 15) + 'vmin');
  p.style.setProperty('--d', (opts.delay ?? 0) + 'ms');
  p.style.setProperty('--t', (opts.dur ?? 5200) + 'ms');
  p.style.setProperty('--op', opts.opacity ?? 0.92);
  /* depth: the ones further back are smaller, dimmer and a little out
     of focus, which is what puts them behind the subject rather than
     in front of it */
  if (opts.blur) p.style.setProperty('--bl', opts.blur + 'px');
  return p;
}

/* ── a ring on the water, opening and going ────────────────────── */
function ripple(at, delay, size = 16) {
  const r = el('fh-ring');
  r.style.setProperty('--x', at[0] * 100 + '%');
  r.style.setProperty('--y', at[1] * 100 + '%');
  r.style.setProperty('--sz', size + 'vmin');
  r.style.setProperty('--d', delay + 'ms');
  return r;
}

/* ── vapour: soft, slow, and never the same twice ──────────────── */
function steam(at, delay, scale) {
  const s = el('fh-steam');
  s.style.setProperty('--x', at[0] * 100 + '%');
  s.style.setProperty('--y', at[1] * 100 + '%');
  s.style.setProperty('--sz', scale + 'vmin');
  s.style.setProperty('--d', delay + 'ms');
  return s;
}

/* ── a drop gathering at a lip, then falling ───────────────────── */
function drop(from, fall, delay) {
  const d = el('fh-drop');
  d.style.setProperty('--x', from[0] * 100 + '%');
  d.style.setProperty('--y', from[1] * 100 + '%');
  d.style.setProperty('--fall', fall + 'vh');
  d.style.setProperty('--d', delay + 'ms');
  return d;
}

/* ── what moves in each act ────────────────────────────────────── */
function populate(fx, act) {
  if (act.n === 1) {
    const [rx, ry] = act.rose;
    /* The rose fills most of the frame, so a petal off it is a hand's
       width on screen, not a confetto. delay, size, start angle, end
       angle, and where on the bloom it lets go. */
    [[0,    18.5, -14,  150, -0.06,  0.02],
     [900,  14.0,   8, -170,  0.06,  0.10],
     [1900, 21.0,  -4,  210, -0.14,  0.14],
     [2800, 12.5,  16, -140,  0.13,  0.04],
     [3700, 16.0, -20,  190, -0.01,  0.18]
    ].forEach(([delay, size, r0, r1, ox, oy], i) => {
      fx.append(petal(
        [rx + ox, ry + oy],
        [rx + ox - 0.26 - i * 0.06, 1.18],
        { delay, size, r0, r1, dur: 5600 + i * 420, sprite: i % PETALS.length }
      ));
    });
  }

  if (act.n === 2) {
    act.land.forEach(([lx, ly], i) => {
      const t = 300 + i * 1500;
      fx.append(petal([lx + 0.05, -0.16], [lx, ly - 0.01], {
        delay: t, size: 13.5, r0: -18, r1: 26, dur: 1500, sprite: i + 2
      }));
      fx.append(ripple([lx, ly], t + 1450, 14));
      fx.append(ripple([lx, ly], t + 1850, 22));
      fx.append(ripple([lx, ly], t + 2300, 30));
    });
  }

  if (act.n === 3) {
    act.steam.forEach(([sx, sy], i) =>
      fx.append(steam([sx, sy], i * 1300, 26 + i * 8)));
    fx.append(drop(act.spout, 14, 1400));
    fx.append(drop(act.spout, 14, 3900));
  }

  if (act.n === 4) {
    fx.append(drop([act.neck[0], act.neck[1] - 0.16], 13, 600));
    /* x, delay, size, start angle, end angle, how far it drifts, opacity,
       blur. The small, dim, soft ones read as falling behind the bottle;
       the large, bright, sharp ones as falling in front of it, which is
       what makes a flat layer look like a room with depth in it. */
    [[0.14,  200,  19.0, -16,  170, -0.10, 0.95, 0  ],
     [0.33, 1500,  10.0,  22, -130,  0.07, 0.52, 1.6],
     [0.52,  800,  13.0,  -8,  150, -0.06, 0.66, 1.0],
     [0.71, 2400,  21.0,  12, -180,  0.09, 0.92, 0  ],
     [0.88, 1100,   9.0, -24,  120, -0.05, 0.46, 2.0],
     [0.62, 3300,  15.5,   4,  200,  0.12, 0.74, 0.6]
    ].forEach(([x, delay, size, r0, r1, dx, opacity, blur], i) => {
      fx.append(petal([x, -0.22], [x + dx, 1.22], {
        delay, size, r0, r1, opacity, blur,
        dur: 7600 - size * 90, sprite: i % PETALS.length
      }));
    });
  }
}

/* ── building and running ──────────────────────────────────────── */
function build() {
  host.innerHTML = '';
  ACTS.forEach((act, i) => {
    const s = el('fh-scene');
    s.dataset.act = act.n;
    s.style.setProperty('--fade', FADE + 'ms');
    s.append(plate(act));
    const fx = el('fh-fx');
    populate(fx, act);
    s.append(fx);
    if (i === 0) s.classList.add('on');
    host.append(s);
  });
}

function show(i) {
  const scenes = [...host.children];
  if (!scenes.length) return;
  at = ((i % scenes.length) + scenes.length) % scenes.length;
  scenes.forEach((s, k) => {
    const on = k === at;
    s.classList.toggle('on', on);
    /* the layers are restarted with their scene, so a petal never
       arrives half way down */
    if (on) {
      s.querySelectorAll('.fh-fx > *').forEach(n => {
        n.style.animation = 'none';
        void n.offsetWidth;
        n.style.animation = '';
      });
    }
  });
}

function start() {
  stop();
  if (STILL.matches || held) return;
  timer = setTimeout(function step() {
    show(at + 1);
    timer = setTimeout(step, HOLD + FADE);
  }, HOLD + FADE);
}
function stop() { clearTimeout(timer); timer = 0; }

/* anything that says somebody is reading it stops it moving under them */
function hold(on) {
  held = on;
  host.closest('.filmhero')?.classList.toggle('hold', on);
  on ? stop() : start();
}

export function mountFilmHero(root) {
  host = root.querySelector('.fh-scenes');
  if (!host) return;
  build();
  show(0);
  start();

  /* a finger is not a pointer resting on something: on a phone the first
     touch anywhere on the first screen would otherwise stop the film */
  root.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch') hold(true); });
  root.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch') hold(false); });
  root.addEventListener('focusin', () => hold(true));
  root.addEventListener('focusout', e => {
    if (!root.contains(e.relatedTarget)) hold(false);
  });
  document.addEventListener('visibilitychange', () =>
    document.hidden ? stop() : start());
  WIDE.addEventListener?.('change', () => { build(); show(at); start(); });
  STILL.addEventListener?.('change', () => STILL.matches ? stop() : start());
}
