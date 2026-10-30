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
  img.src = `assets/hero/plate-${act.n}-${WIDE.matches ? 'wide' : 'tall'}.webp`;
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
  p.style.setProperty('--sz', (opts.size ?? 8) + 'vmin');
  p.style.setProperty('--d', (opts.delay ?? 0) + 'ms');
  p.style.setProperty('--t', (opts.dur ?? 5200) + 'ms');
  p.style.setProperty('--op', opts.opacity ?? 0.92);
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
    [[0, 6.4, -14, 150], [700, 5.2, 8, -170], [1500, 7.0, -4, 210],
     [2300, 4.6, 16, -140], [3100, 5.8, -20, 190]
    ].forEach(([delay, size, r0, r1], i) => {
      fx.append(petal(
        [rx - 0.02 + i * 0.012, ry + 0.04 + i * 0.02],
        [rx - 0.30 - i * 0.05, 1.12],
        { delay, size, r0, r1, dur: 5600 + i * 420, sprite: i % PETALS.length }
      ));
    });
  }

  if (act.n === 2) {
    act.land.forEach(([lx, ly], i) => {
      const t = 300 + i * 1500;
      fx.append(petal([lx + 0.05, -0.12], [lx, ly - 0.01], {
        delay: t, size: 6.2, r0: -18, r1: 26, dur: 1500, sprite: i + 2
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
    fx.append(petal([1.06, 0.18], [-0.10, 0.62], {
      delay: 400, size: 5.4, r0: 10, r1: -160, dur: 7200, sprite: 0, opacity: 0.6
    }));
    fx.append(petal([-0.08, 0.74], [1.05, 0.42], {
      delay: 2200, size: 4.2, r0: -30, r1: 120, dur: 7600, sprite: 3, opacity: 0.45
    }));
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

  root.addEventListener('pointerenter', () => hold(true));
  root.addEventListener('pointerleave', () => hold(false));
  root.addEventListener('focusin', () => hold(true));
  root.addEventListener('focusout', e => {
    if (!root.contains(e.relatedTarget)) hold(false);
  });
  document.addEventListener('visibilitychange', () =>
    document.hidden ? stop() : start());
  WIDE.addEventListener?.('change', () => { build(); show(at); start(); });
  STILL.addEventListener?.('change', () => STILL.matches ? stop() : start());
}
