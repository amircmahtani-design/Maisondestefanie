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

const PETALS = [1, 2, 3, 4, 5].map(n => `assets/hero/petal-${n}.webp`);

/* Where each act's plate comes from, per shape of screen. Both shapes
   are now the four scenes delivered for this film; tools/filmplates.py
   writes them at the size their detail actually lives at, which is
   smaller than the export says — see the note at the top of that file. */
const PLATES = [
  { wide: 'assets/hero/plate-1-wide.webp', tall: 'assets/hero/plate-1-upright.webp' },
  { wide: 'assets/hero/plate-2-wide.webp', tall: 'assets/hero/plate-2-upright.webp' },
  { wide: 'assets/hero/plate-3-wide.webp', tall: 'assets/hero/plate-3-upright.webp' },
  { wide: 'assets/hero/plate-4-wide.webp', tall: 'assets/hero/plate-4-upright.webp' },
];
/* Where things are in each plate, as a fraction of it, measured off the
   delivered scenes with a grid laid over them. A 16:9 screen and an
   upright one are different photographs of the same table, so each act
   carries both sets and the player takes the one in use.

     rose   the head of the bloom, where a petal lets go
     water  the surface of the essence, where a petal lands and rings
     steam  the mouths the vapour leaves by
     drip   the lip a drop gathers on, and how far it falls
     neck   the mouth of the flacon
*/
const ACTS = [
  { n: 1,
    wide: { rose: [0.73, 0.14] },
    tall: { rose: [0.46, 0.21] } },

  { n: 2,
    /* The bowl is wide and low in a 16:9 frame and sits left in an
       upright one, so the three places a petal can land differ. On a
       wide screen they also keep right of x=0.52, because the headline
       is read to the left of that and a petal landing under it is a
       petal nobody sees. */
    wide: { water: [[0.560, 0.585], [0.630, 0.600], [0.685, 0.590]] },
    tall: { water: [[0.160, 0.400], [0.300, 0.385], [0.440, 0.402]] } },

  { n: 3,
    wide: { steam: [[0.475, 0.30], [0.50, 0.24], [0.45, 0.35]],
            drip:  [0.845, 0.575], fall: 11 },
    tall: { steam: [[0.405, 0.125], [0.43, 0.075], [0.385, 0.175]],
            drip:  [0.615, 0.335], fall: 9 } },

  { n: 4,
    wide: { neck: [0.635, 0.525] },
    tall: { neck: [0.385, 0.205] } },
];

const shape = () => (WIDE.matches ? 'wide' : 'tall');

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

/* ── petals ──────────────────────────────────────────────────────
   `to` is where it ends up. A petal given `land` decelerates into that
   point and stays there, once, which is what settling on water looks
   like; every other petal passes through and leaves. `sway` is how far
   it swings either side of its path on the way down. */
function petal(from, to, opts = {}) {
  const p = el('fh-petal', 'img');
  p.alt = '';
  p.decoding = 'async';
  p.src = PETALS[opts.sprite ?? Math.floor(Math.random() * PETALS.length)];
  p.style.setProperty('--x0', from[0] * 100 + '%');
  p.style.setProperty('--y0', from[1] * 100 + '%');
  p.style.setProperty('--dx', (to[0] - from[0]) * 100 + 'vw');
  p.style.setProperty('--dy', (to[1] - from[1]) * 100 + 'vh');
  p.style.setProperty('--sw', (opts.sway ?? 2.2) + 'vmin');
  p.style.setProperty('--r0', (opts.r0 ?? 0) + 'deg');
  p.style.setProperty('--r1', (opts.r1 ?? 200) + 'deg');
  p.style.setProperty('--ra', ((opts.r0 ?? 0) + ((opts.r1 ?? 200) - (opts.r0 ?? 0)) * 0.26) + 'deg');
  p.style.setProperty('--rb', ((opts.r0 ?? 0) + ((opts.r1 ?? 200) - (opts.r0 ?? 0)) * 0.53) + 'deg');
  p.style.setProperty('--rc', ((opts.r0 ?? 0) + ((opts.r1 ?? 200) - (opts.r0 ?? 0)) * 0.78) + 'deg');
  p.style.setProperty('--sz', (opts.size ?? 15) + 'vmin');
  p.style.setProperty('--d', (opts.delay ?? 0) + 'ms');
  p.style.setProperty('--t', (opts.dur ?? 5200) + 'ms');
  p.style.setProperty('--op', opts.opacity ?? 0.92);
  /* depth: the ones further back are smaller, dimmer and a little out
     of focus, which is what puts them behind the subject rather than
     in front of it */
  if (opts.blur) p.style.setProperty('--bl', opts.blur + 'px');
  if (opts.land) p.classList.add('lands');
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

/* ── vapour: a plume and the wisp shearing inside it ───────────── */
function steam(at, delay, scale, dur) {
  const s = el('fh-steam');
  s.style.setProperty('--x', at[0] * 100 + '%');
  s.style.setProperty('--y', at[1] * 100 + '%');
  s.style.setProperty('--sz', scale + 'vmin');
  s.style.setProperty('--d', delay + 'ms');
  s.style.setProperty('--t', dur + 'ms');
  return s;
}
function wisp(at, delay, scale, dur) {
  const w = el('fh-wisp');
  w.style.setProperty('--x', at[0] * 100 + '%');
  w.style.setProperty('--y', at[1] * 100 + '%');
  w.style.setProperty('--sz', scale + 'vmin');
  w.style.setProperty('--d', delay + 'ms');
  w.style.setProperty('--t', dur + 'ms');
  return w;
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
  const A = act[shape()];

  if (act.n === 1) {
    const [rx, ry] = A.rose;
    /* Petals let go from different places on the bloom and fall away
       across the table. delay, size, start angle, end angle, where on
       the head it parts, how far it drifts sideways, how wide it swings
       on the way down. */
    [[0,    17.0, -12,  164, -0.045, -0.26, 2.6],
     [1100, 12.5,  14, -148,  0.050,  0.14, 1.9],
     [2200, 19.5,  -6,  196, -0.015,  0.30, 3.1],
     [3300, 10.5,  20, -126,  0.065, -0.10, 1.6],
     [4400, 14.5, -18,  178,  0.010,  0.22, 2.3]
    ].forEach(([delay, size, r0, r1, ox, dx, sway], i) => {
      fx.append(petal(
        [rx + ox, ry + 0.03],
        [rx + ox + dx, 1.16],
        { delay, size, r0, r1, sway, dur: 6400 + i * 360, sprite: i % PETALS.length }
      ));
    });
  }

  if (act.n === 2) {
    /* Each petal falls from above the frame and settles on the essence,
       and the rings open from where it touched — three of them, a beat
       apart, widening and going as the surface takes it. */
    A.water.forEach(([lx, ly], i) => {
      const t = 200 + i * 1500;
      const dur = 2400;
      fx.append(petal([lx + 0.055, -0.14], [lx, ly], {
        delay: t, dur, land: true, sway: 2.4,
        /* the size of the petals already lying in that bowl, not the
           size of the ones falling past the rose */
        size: [7.6, 6.4, 5.6][i] ?? 6, r0: -22 + i * 14, r1: 18 + i * 10,
        sprite: (i + 1) % PETALS.length
      }));
      const hit = t + dur;
      fx.append(ripple([lx, ly], hit +   0,  7));
      fx.append(ripple([lx, ly], hit + 420, 12));
      fx.append(ripple([lx, ly], hit + 900, 18));
    });
  }

  if (act.n === 3) {
    /* Three plumes, each on its own clock so they never pulse together,
       and a faster wisp inside each one shearing the other way. */
    A.steam.forEach(([sx, sy], i) => {
      fx.append(steam([sx, sy], i * 1150,        20 + i * 7, 8200 + i * 900));
      fx.append(wisp ([sx, sy], i * 1150 + 600,  20 + i * 7, 5900 + i * 700));
    });
    fx.append(drop(A.drip, A.fall, 1400));
    fx.append(drop(A.drip, A.fall, 4200));
  }

  if (act.n === 4) {
    fx.append(drop([A.neck[0], A.neck[1] - 0.14], 11, 700));
    /* x, delay, size, start angle, end angle, how far it drifts,
       opacity, blur. The small, dim, soft ones read as falling behind
       the flacon; the large, bright, sharp ones as falling in front of
       it, which is what makes a flat layer look like a room with depth
       in it. */
    [[0.12,  200,  17.0, -16,  170, -0.09, 0.95, 0  ],
     [0.31, 1500,   9.5,  22, -130,  0.07, 0.52, 1.6],
     [0.50,  800,  12.5,  -8,  150, -0.06, 0.66, 1.0],
     [0.73, 2400,  19.0,  12, -180,  0.08, 0.92, 0  ],
     [0.89, 1100,   8.5, -24,  120, -0.05, 0.46, 2.0]
    ].forEach(([x, delay, size, r0, r1, dx, opacity, blur], i) => {
      fx.append(petal([x, -0.20], [x + dx, 1.20], {
        delay, size, r0, r1, opacity, blur, sway: 2.0 + i * 0.3,
        dur: 8200 - size * 90, sprite: i % PETALS.length
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
