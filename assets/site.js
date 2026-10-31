/* ══════════════════════════════════════════════════════════════
   LA MAISON DE STEFANIE — front of house
   Content comes from Firestore when it is configured, and from
   content.json otherwise. Nothing here needs a build step.
   ══════════════════════════════════════════════════════════════ */
const CFG = window.LMS_CONFIG || {};
const $  = (s,r=document)=>r.querySelector(s);
const $$ = (s,r=document)=>[...r.querySelectorAll(s)];
const esc = s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const motionQ = matchMedia('(prefers-reduced-motion: reduce)');
let REDUCED = motionQ.matches;
/* parallax is for a mouse on a large screen only — never on a phone */

/* ── interface words that are not the shop's to edit ─────────── */
const UI = {
 en:{nav:{maison:'The Maison',experience:'Bespoke Experience',legacy:'The Story',
          shelf:'Creations',bespoke:'Bespoke',visit:'Visit'},
     ui:{onGoogle:'on Google',phone:'Telephone',follow:'Follow',perfumer:'Stefanie · perfumer',
         book:'Book',scroll:'Scroll',theMaterial:'The material',
         reviews:'reviews',top:'Top',heart:'Heart',base:'Base',size:'Size',price:'Price',
         onRequest:'On request',buy:'Order this',enquire:'Ask Stefanie',
         made:'Made to order in the shop',nothing:'Nothing on this shelf yet.',
         everything:'Everything',fullPrivacy:'Read the full Privacy & Cookies policy',
         openMenu:'Menu',closeMenu:'Close menu'}},
 el:{nav:{maison:'Το Σπίτι',experience:'Η Εμπειρία',legacy:'Η Ιστορία',
          shelf:'Δημιουργίες',bespoke:'Προσωπικά',visit:'Επίσκεψη'},
     ui:{onGoogle:'στη Google',phone:'Τηλέφωνο',follow:'Ακολούθησε',perfumer:'Στεφανί · αρωματοποιός',
         book:'Ραντεβού',scroll:'Κύλισε',theMaterial:'Η ύλη',
         reviews:'κριτικές',top:'Κορυφή',heart:'Καρδιά',base:'Βάση',size:'Μέγεθος',price:'Τιμή',
         onRequest:'Κατόπιν ζήτησης',buy:'Παράγγειλέ το',enquire:'Ρώτησε τη Στεφανί',
         made:'Φτιάχνεται κατά παραγγελία',nothing:'Τίποτα εδώ ακόμη.',
         everything:'Όλα',fullPrivacy:'Διάβασε την πλήρη πολιτική απορρήτου',
         openMenu:'Μενού',closeMenu:'Κλείσε το μενού'}}
};

let LANG = (new URLSearchParams(location.search).get('lang')
        || localStorage.getItem('lms-lang')
        || (navigator.language||'en').slice(0,2).toLowerCase());
if (LANG !== 'el') LANG = 'en';

let DATA=null, DB=null, CAT='all', THREAD=null, PICKED=[];
const mcache = new Map();

/* ── boot ────────────────────────────────────────────────────── */
async function boot(){
  if (CFG.firebase && !String(CFG.firebase.apiKey).startsWith('PASTE')){
    try{
      const [{initializeApp}, fs] = await Promise.all([
        import('https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js'),
        import('https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js')]);
      DB = fs.getFirestore(initializeApp(CFG.firebase)); window.__fs = fs;
      const s = await fs.getDoc(fs.doc(DB,'site','content'));
      if (s.exists()) DATA = s.data();
    }catch(e){ console.warn('Live content unavailable; using content.json.', e); }
  }
  if (!DATA){
    /* the fetch was started in the head before this module was parsed */
    try{ DATA = await (window.__lmsContent
           || fetch('content.json',{cache:'no-cache'}).then(r=>r.json())); }
    catch(e){ console.error(e); }
  }
  if (!DATA){ console.error('Content could not be loaded.'); return; }
  render();
}

const L = (o,k)=>(o && o[LANG] && o[LANG][k]!=null) ? o[LANG][k] : (o && o.en ? o.en[k] : '');
const U = k=>UI[LANG].ui[k];
function tGet(p){
  const parts = p.split('.');
  const [a,b] = parts;
  if (parts.length === 2){
    if (UI[LANG][a] && UI[LANG][a][b]!=null) return UI[LANG][a][b];
    return DATA?.[a] ? L(DATA[a],b) : '';
  }
  /* deeper than two, as the five pages are: pages.maison.title walks down
     to the bilingual block and then asks it for the key */
  let node = DATA?.[a];
  for (let i = 1; i < parts.length - 1 && node; i++) node = node[parts[i]];
  return node ? L(node, parts[parts.length - 1]) : '';
}
const wa = t=>'https://wa.me/' + String(DATA.settings.whatsapp||'').replace(/\D/g,'')
            + '?text=' + encodeURIComponent(t);
const askMsg = ()=>LANG==='el'
  ? 'Γεια σας! Θα ήθελα να ρωτήσω για ένα προσωπικό άρωμα.'
  : 'Hello! I would like to ask about a bespoke perfume.';

/* ── pictures ────────────────────────────────────────────────
   A slot may hold a plain path, or a "media:<id>" reference to a
   photograph Stefanie uploaded through the Studio.             */
async function resolve(ref){
  if (!ref) return '';
  if (!ref.startsWith('media:')) return ref;
  const id = ref.slice(6);
  if (mcache.has(id)) return mcache.get(id);
  if (!DB) return '';
  try{
    const s = await window.__fs.getDoc(window.__fs.doc(DB,'media',id));
    const u = s.exists() ? (s.data().out||'') : '';
    mcache.set(id,u); return u;
  }catch(e){ return ''; }
}
const slot = k=>(DATA.pictures||{})[k]||{};

/* Everything below the fold waits until it is nearly in view. The
   box is already the right shape, so nothing moves when it lands. */
/* A slot may carry a srcset. It is only trusted while `srcsetFor` still
   matches `src` — the moment Stefanie puts her own photograph in through
   the Studio the two disagree and the plain src is used instead. */
function sizeUp(img, slot, url){
  if (slot && slot.srcset && slot.srcsetFor && slot.srcsetFor === slot.src && url === slot.src){
    img.srcset = slot.srcset;
    if (slot.sizes) img.sizes = slot.sizes;
  }
  if (slot && slot.w && slot.h){ img.width = slot.w; img.height = slot.h; }
}
const io = new IntersectionObserver(async es=>{
  for (const e of es){
    if (!e.isIntersecting) continue;
    io.unobserve(e.target);
    const url = await resolve(e.target.dataset.ref);
    if (!url) continue;
    const i = new Image();
    i.alt = e.target.dataset.alt || '';
    i.loading = 'lazy'; i.decoding = 'async';
    i.addEventListener('load', ()=>i.classList.add('on'), {once:true});
    sizeUp(i, e.target.__slot, url);
    i.src = url;
    if (i.complete) i.classList.add('on');
    e.target.querySelector('.ph')?.remove();
    e.target.prepend(i);
  }
},{rootMargin:'500px 0px'});

function fillPane(el,key){
  const s = slot(key);
  el.__slot = s;
  el.dataset.ref = s.src || '';
  el.dataset.alt = s.alt || '';
  if (!el.querySelector('img') && !el.querySelector('.ph'))
    el.insertAdjacentHTML('afterbegin',`<span class="ph">${esc(s.label||'')}</span>`);
  if (s.src) io.observe(el);
}

/* the three steps under the hero */
function renderDistilled(){
  const d = L(DATA.distilled, 'steps') || [];
  const host = $('#distilledSteps'); if (!host) return;
  host.innerHTML = d.map(s=>`<li class="step rv">
      <span class="n">${esc(s.n)}</span>
      <h3>${esc(s.t)}</h3><i class="tick" aria-hidden="true"></i>
      <p>${esc(s.d)}</p>
    </li>`).join('');
}

/* ══ THE HERO ══════════════════════════════════════════════════
   Four scenes behind one set of words. Three of them breathe on a
   four second Ken Burns; the fourth is the bottle, whose petals are
   a run of photographs played out and back. The scene changes on a
   timer, not on scroll, so nothing is pinned and the page is exactly
   as tall as its content.                                        */
const HERO = { scenes: [], n: 0, el: null, at: 0, timer: 0,
               still: false, held: false, flat: false };
const SCENE_HOLD = 4400;          /* long enough to look, short enough to move */

/* How tall one screen is — and whether this page is being shown inside
   something that has sized itself to fit the whole page.

   That case is not hypothetical: an embed that grows its frame to the
   content height makes innerHeight the CONTENT height, so anything sized
   from it grows the content, which grows the frame, without end. The
   display is the one bound that cannot be fed by our own layout. */
function screenBound(){
  const ih = window.innerHeight || 0;
  const sh = (window.screen && window.screen.height) || 0;
  if (!ih) return { h: sh || 720, grown: false };
  if (sh && ih > sh * 1.5) return { h: sh, grown: true };
  return { h: ih, grown: false };
}
function sizeStage(){
  const { h, grown } = screenBound();
  document.documentElement.style.setProperty('--stage', h + 'px');
  HERO.flat = grown;
  return h;
}

function renderHero(){
  const data = L(DATA.sequence, 'chapters') || [];
  HERO.scenes = data; HERO.n = data.length;
  HERO.el = $('.hero');
  /* a first screen can exist without the four chapters in it — the home
     page's film has its own player */
  const sceneHost = $('#heroScenes');
  if (!HERO.el || !sceneHost || !HERO.n) return;
  sizeStage();

  sceneHost.innerHTML = data.map((c,i)=>{
    const pic = slot(c.subject) || {};
    /* a tall photograph in a wide frame loses most of its height, so each
       one says which part of itself to keep */
    const pos = [pic.focus ? `--pos:${esc(pic.focus)}` : '',
                 pic.focusM ? `--pos-m:${esc(pic.focusM)}` : ''].filter(Boolean).join(';');
    return `<div class="scene" data-i="${i}" data-motion="${c.frames ? 'frames' : 'burns'}"
                 ${pos ? `style="${pos}"` : ''}>
      <img class="lay a" alt="" decoding="async"${c.frames ? ''
        : ` data-subject="${esc(c.subject)}"${i ? ' loading="lazy"' : ''}`}>
      <img class="lay b" alt="" decoding="async">
    </div>`;
  }).join('');

  paintScenes();

  /* The chapter count used to sit down the right edge as a tab list. It
     is gone: the chapters turn by themselves and the page is meant to be
     looked at. Anything left that wants to drive them still can. */
  const nums = $('#heroNums');
  if (nums){
    nums.innerHTML = data.map((c,i)=>
      `<button type="button" role="tab" data-i="${i}" aria-current="${i===0}"
         aria-label="${esc(c.word || c.num)}">${esc(c.num)}</button>`).join('');
    $$('#heroNums button').forEach(btn=>{
      btn.addEventListener('click', ()=>{ showScene(+btn.dataset.i); restartHero(); });
    });
  }

  /* whichever scene carries a run of frames gets the two-layer player */
  stopLoop(); LOOP.ready = false; LOOP.live = false; LOOP.urls = [];
  const fi = data.findIndex(c => c.frames && c.frames.length);
  if (fi > -1) setupLoop(fi);

  /* anything that says someone is reading it stops it moving under them */
  if (!HERO.el.dataset.wired){
    HERO.el.dataset.wired = '1';
    /* Pausing under the pointer is a courtesy to somebody reading with a
       mouse. A finger is not a pointer resting on something — on a phone
       the first touch anywhere would stop the hero, so touch is ignored. */
    HERO.el.addEventListener('pointerenter', e=>{ if(e.pointerType!=='touch') holdHero(true); });
    HERO.el.addEventListener('pointerleave', e=>{ if(e.pointerType!=='touch') holdHero(false); });
    HERO.el.addEventListener('focusin',      ()=>holdHero(true));
    HERO.el.addEventListener('focusout', e=>{
      if (!HERO.el.contains(e.relatedTarget)) holdHero(false);
    });
  }

  HERO.still = REDUCED;
  HERO.held = false;
  showScene(HERO.still ? Math.min(3, HERO.n - 1) : 0);
  beginHero();
}

function showScene(i){
  if (!HERO.n) return;
  HERO.at = ((i % HERO.n) + HERO.n) % HERO.n;
  $$('#heroScenes .scene').forEach((el,k)=> el.classList.toggle('on', k === HERO.at));
  $$('#heroNums button').forEach((b,k)=> b.setAttribute('aria-current', String(k === HERO.at)));
  /* the frames run only while their own scene is showing, and the set is
     fetched a scene early so it is decoded by the time it is wanted */
  const fi = HERO.scenes.findIndex(c => c.frames && c.frames.length);
  if (fi > -1){
    if (!LOOP.ready && (HERO.at === fi || HERO.at === (fi - 1 + HERO.n) % HERO.n)) loadLoop();
    setLoopLive(HERO.at === fi);
  }
}

function startHero(firstHold){
  stopHero();
  if (HERO.still || HERO.held || document.hidden || HERO.n < 2) return;
  HERO.timer = setTimeout(function step(){
    showScene(HERO.at + 1);
    HERO.timer = setTimeout(step, SCENE_HOLD);
  }, firstHold || SCENE_HOLD);
}
function stopHero(){ clearTimeout(HERO.timer); HERO.timer = 0; }
function restartHero(){ stopHero(); startHero(); }

/* The curtain is drawn by an inline script that runs long before this
   module does, so the two cannot call each other reliably — whichever
   finishes first would win. The hero simply waits for the curtain to go
   instead, and nobody arrives mid-sequence. */
function beginHero(){
  if (HERO.still) return;
  if (!document.body.classList.contains('curtained')){ startHero(); return; }
  const ob = new MutationObserver(()=>{
    if (document.body.classList.contains('curtained')) return;
    ob.disconnect(); showScene(0); startHero(1800);
  });
  ob.observe(document.body, {attributes:true, attributeFilter:['class']});
}

/* Anyone reading, hovering or tabbing through the hero has the scenes
   hold still — auto-changing content that cannot be paused is a trap. */
function holdHero(on){
  if (on === HERO.held) return;
  HERO.held = on;
  HERO.el && HERO.el.classList.toggle('hold', on);
  if (on){ stopHero(); stopLoop(); }
  else { startHero(); if (LOOP.live) runLoop(); }
}

/* The page may be shown at its full height inside something that grew to
   fit it. The hero is one screen either way and keeps playing; all that
   changes is where the honest measure of a screen comes from, so the stage
   is simply re-measured whenever the size moves. */
/* Every chapter photograph is a 9:16 frame with its subject composed to
   the very edges. Across a screen that is wider than it is tall there is
   nowhere for that to go but off the sides, so each one also exists in a
   wide frame with the light carried outwards and real room around the
   subject — tools/widescenes.py. A phone gets the upright one. */
const WIDE_SCREEN = matchMedia('(min-aspect-ratio: 1/1)');
const sceneSrc = url => {
  if (!url || !/\.webp$/i.test(url) || /-(wide|tall)\.webp$/i.test(url)) return url;
  const kind = WIDE_SCREEN.matches ? '-wide.webp' : '-tall.webp';
  /* The extended frames exist at one size per shape, so the width a
     narrow screen would otherwise have asked for does not apply to them;
     they all come from the 880 originals. */
  const frame = url.match(/^(.*\/frame-\d\d)-\d+\.webp$/i);
  if (frame) return frame[1] + '-880' + kind;
  return url.replace(/\.webp$/i, kind);
};
function paintScenes(){
  $$('#heroScenes img.lay.a[data-subject]').forEach(async (img,i)=>{
    const sl = slot(img.dataset.subject) || {};
    const url = sceneSrc(await resolve(sl.src));
    if (!url || img.getAttribute('src') === url) return;
    img.alt = '';
    if (i === 0) img.fetchPriority = 'high';
    img.src = url;
  });
}
WIDE_SCREEN.addEventListener?.('change', paintScenes);

function applyHeroMode(){ sizeStage(); paintScenes(); }

/* ══ THE BOTTLE LOOP ═══════════════════════════════════════════
   Nine photographs of the same bottle with the petals a little
   further along in each. Played out and back — 00 to 08 and home
   again — so the run closes on itself and the petals drift rather
   than jumping back to the start.

   Two layers, and the one you can see is never taken away: the next
   frame is decoded into the hidden layer first, and only then do the
   two opacities swap. That is what stops the flicker a plain src
   change gives you, and it is why the whole run is decoded before
   the first swap rather than during it.                          */
const LOOP = {
  el:null, lays:null, urls:[], order:[], at:0, timer:0,
  ready:false, loading:false, showing:0, live:false
};
const FRAME_HOLD  = 220;   /* a brief breath between petal positions */
const FRAME_BLEND = 520;   /* a soft, overlapping dissolve into the next */

function loopOrder(n){                 /* 0,1,…,n-1,…,1  — out and back */
  const a = [];
  for (let i = 0; i < n; i++) a.push(i);
  for (let i = n - 2; i > 0; i--) a.push(i);
  return a;
}

async function loadLoop(){
  if (LOOP.loading || LOOP.ready || !LOOP.urls.length) return;
  LOOP.loading = true;
  try{
    /* every frame decoded before the first swap, or the run stutters
       through its first pass while the browser catches up */
    await Promise.all(LOOP.urls.map(u => new Promise(res=>{
      const i = new Image();
      i.decoding = 'async';
      i.addEventListener('load', ()=> (i.decode ? i.decode().catch(()=>{}) : Promise.resolve()).then(res), {once:true});
      i.addEventListener('error', res, {once:true});
      i.src = u;
    })));
    LOOP.ready = true;
    if (LOOP.live) runLoop();
  } finally { LOOP.loading = false; }
}

function stopLoop(){ clearTimeout(LOOP.timer); LOOP.timer = 0; }

function runLoop(){
  stopLoop();
  if (!LOOP.ready || !LOOP.live || document.hidden || REDUCED) return;
  const step = async ()=>{
    LOOP.at = (LOOP.at + 1) % LOOP.order.length;
    const url = LOOP.urls[LOOP.order[LOOP.at]];
    const next = LOOP.lays[LOOP.showing ^ 1];
    if (next.src !== url){
      next.src = url;
      try{ await next.decode(); }catch(e){ /* a swap missed is not a failure */ }
    }
    if (!LOOP.live || document.hidden) return;
    /* only now is the outgoing layer allowed to go */
    LOOP.showing ^= 1;
    LOOP.lays[LOOP.showing].style.opacity = '1';
    LOOP.lays[LOOP.showing ^ 1].style.opacity = '0';
    LOOP.timer = setTimeout(step, FRAME_HOLD + FRAME_BLEND);
  };
  LOOP.timer = setTimeout(step, FRAME_HOLD);
}

function setLoopLive(on){
  if (on === LOOP.live) return;
  LOOP.live = on;
  if (on){ loadLoop(); if (LOOP.ready) runLoop(); } else stopLoop();
}

/* Every frame is downloaded, so the run picks one width and keeps it
   rather than letting srcset choose per frame — a phone has no business
   pulling the desktop set nine times over, and a run that mixed widths
   would resample on every swap. */
function frameWidth(panel){
  /* a phone is still a retina phone: the bottle itself never moves, so a
     set too small for the screen reads as a soft photograph rather than
     as motion. Two device pixels is the point past which nobody can see
     the difference, and anyone who has asked to save data gets the small
     set whatever their screen. */
  const conn = navigator.connection || {};
  if (conn.saveData) return 560;
  return panel * Math.min(devicePixelRatio || 1, 2) <= 620 ? 560 : 880;
}
function atWidth(sl, want){
  const cands = String(sl.srcset || '').split(',').map(x=>x.trim().split(/\s+/))
    .filter(x=>x.length===2).map(([u,w])=>[u, parseInt(w,10)]);
  if (!cands.length) return sl.src;
  const hit = cands.find(([,w])=>w === want);
  return hit ? hit[0] : cands[cands.length-1][0];
}

async function setupLoop(chapter){
  const c = HERO.scenes[chapter];
  if (!c || !c.frames || !c.frames.length) return;
  LOOP.el = $$('#heroScenes .scene')[chapter];
  if (!LOOP.el) return;
  LOOP.lays = [$('.lay.a', LOOP.el), $('.lay.b', LOOP.el)];
  const want = frameWidth(LOOP.el.getBoundingClientRect().width || innerWidth);
  /* the nine frames get the same wide or upright treatment the chapters
     do, so the bottle is not clipped by the edge it was composed against */
  LOOP.urls = (await Promise.all(c.frames.map(async k => {
    const sl = slot(k) || {};
    return sceneSrc(await resolve(atWidth(sl, want)));
  }))).filter(Boolean);
  if (LOOP.urls.length < 2){ LOOP.urls = []; return; }
  LOOP.order = loopOrder(LOOP.urls.length);
  LOOP.el.classList.add('xf');
  const sl0 = slot(c.frames[0]) || {};
  LOOP.lays.forEach(l=>{
    /* a srcset would quietly win over the src the player sets */
    l.removeAttribute('srcset'); l.removeAttribute('sizes');
    l.removeAttribute('data-subject'); l.removeAttribute('loading');
    if (sl0.w && sl0.h){ l.width = sl0.w; l.height = sl0.h; }
  });
  /* the frame it rests on, and the only one a stilled page ever sees */
  const rest = Math.min(4, LOOP.urls.length - 1);
  LOOP.at = LOOP.order.indexOf(rest);
  LOOP.showing = 0;
  LOOP.lays[0].src = LOOP.urls[rest];
  LOOP.lays[0].style.opacity = '1'; LOOP.lays[1].style.opacity = '0';
}

document.addEventListener('visibilitychange', ()=>{
  HERO.el && HERO.el.classList.toggle('hold', document.hidden);
  if (document.hidden){ stopHero(); stopLoop(); }
  else { startHero(); if (LOOP.live) runLoop(); }
});

/* ══════════════════════════════════════════════════════════════
   RENDER
   ══════════════════════════════════════════════════════════════ */
/* set(selector, fn) — do this to that element if the page has one.
   Six pages share this module and each carries only its own sections. */
function set(sel, fn){ const e = $(sel); if (e) fn(e); return e; }

function render(){
  const S = DATA.settings;
  document.documentElement.lang = LANG;
  document.body.classList.remove('lang-en','lang-el');
  document.body.classList.add('lang-'+LANG);
  $$('[data-lang]').forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.lang===LANG)));
  set('#yr', e => e.textContent = new Date().getFullYear());

  if (DATA.seo){
    document.title = L(DATA.seo,'title');
    $('meta[name="description"]')?.setAttribute('content', L(DATA.seo,'description'));
    $('meta[property="og:title"]')?.setAttribute('content', L(DATA.seo,'title'));
    $('meta[property="og:description"]')?.setAttribute('content', L(DATA.seo,'description'));
  }
  $$('[data-t]').forEach(el=>{ const v = tGet(el.dataset.t); if (v) el.textContent = v; });
  /* the third headline line only exists if she has written one */
  const tc = $('[data-optional]');
  if (tc) tc.hidden = !tGet('hero.titleC');

  renderHero();
  renderDistilled();
  $$('[data-pic]').forEach(el=>fillPane(el, el.dataset.pic));
  $$('[data-pic-face]').forEach(async el=>{
    const u = await resolve(slot(el.dataset.picFace).src);
    if (u && !el.querySelector('img')){ const i = new Image(); i.src = u; i.alt=''; i.loading='lazy'; el.append(i); }
  });

  /* every route to Stefanie */
  const msg = askMsg();
  ['#bespokeCta','#vWhats','#sealedCta','#send'].forEach(s=>{ const e=$(s); if(e) e.href = wa(msg); });
  const put = (sel, prop, val)=>{ const e = $(sel); if (e) e[prop] = val; };
  put('#dirs','href', S.mapsUrl);
  put('#gbLink','href', S.reviewsUrl);
  put('#footIg','href', S.instagram);
  put('#ig','href', S.instagram);
  set('#ig',    e => e.textContent = '@' + String(S.instagram||'').replace(/\/$/,'').split('/').pop());
  set('#addr',  e => e.innerHTML = esc(L(S,'street')) + '<br>' + esc(L(S,'city')));
  set('#hours', e => e.textContent = L(S,'hours'));
  set('#phone', e => { e.href = 'tel:' + String(S.phone).replace(/\s/g,''); e.textContent = S.phone; });
  set('#score', e => e.textContent = S.rating);
  set('#count', e => e.textContent = S.reviewCount ? S.reviewCount + ' ' + U('reviews') : '');

  /* her story, and the card she writes it on */
  set('#legacyBody', e => e.innerHTML = (L(DATA.legacy,'body')||[]).map(p=>`<p>${esc(p)}</p>`).join(''));
  set('#fRef', e => e.textContent = DATA.formula?.ref || '');
  set('#fFor', e => e.textContent = DATA.formula?.for || '');

  renderThreads(); renderFilters(); renderGrid(); renderDoors(); renderPageHero();

  /* the four steps of a session */
  const mv = LANG==='el' ? ['Πρώτο','Έπειτα','Έπειτα','Τέλος'] : ['First','Then','Then','Finally'];
  set('#session', e => e.innerHTML = (L(DATA.bespoke,'steps')||[]).map((s,i)=>`
    <li class="item rv" data-d="${i%3}">
      <span class="n">${esc(mv[i]||'')}</span>
      <h3>${esc(s.t)}</h3><p>${esc(s.d)}</p></li>`).join(''));

  set('#quotes', e => e.innerHTML = (DATA.reviews||[]).map((r,i)=>`
    <figure class="rv" data-d="${i}">
      <div class="stars" aria-hidden="true">${'★'.repeat(r.stars||5)}</div>
      <blockquote>${esc(r[LANG]||r.en)}</blockquote>
      <cite>${esc(r.name)}${r.meta?' · '+esc(r.meta):''}</cite></figure>`).join(''));

  set('#faqList', e => e.innerHTML = (DATA.faq?.items||[]).map(f=>`
    <details class="rv"><summary>${esc(L(f,'q'))}</summary><p>${esc(L(f,'a'))}</p></details>`).join(''));

  ld(); reveal(); armHandwriting();
  if (localStorage.getItem('lms-map') === '1') showMap();
}

/* ── the first screen of an inner page ───────────────────────────
   Three compositions of the same scene, one per shape of screen: the
   subject sits on the right of a wide one and in the top half of a
   phone, with the words in the quiet dark beside or beneath it. A page
   falls back to the wide one on its own if the other two are not set. */
async function renderPageHero(){
  const host = $('.phero-pic'); if (!host) return;
  const name = host.dataset.phero || '';
  const s = slot('page' + name.charAt(0).toUpperCase() + name.slice(1));
  if (!s || !s.src) return;

  const [wide, tablet, phone] = await Promise.all(
    [s.src, s.srcTablet, s.srcPhone].map(resolve));
  if (!wide) return;

  const src = (u, media) => u ? `<source media="${media}" srcset="${esc(u)}">` : '';
  host.innerHTML =
    '<picture>'
    + src(phone,  '(max-width:600px)')
    + src(tablet, '(max-width:1100px)')
    + `<img alt="${esc(s.alt||'')}" fetchpriority="high" decoding="async"`
    + (s.srcset && s.srcsetFor === s.src ? ` srcset="${esc(s.srcset)}" sizes="100vw"` : '')
    + ` src="${esc(wide)}">`
    + '</picture>';
  const img = host.querySelector('img');
  const lit = () => img.classList.add('on');
  img.complete ? lit() : img.addEventListener('load', lit, {once:true});
}

/* ── the five doors ──────────────────────────────────────────── */
const DOORS = [
  ['maison',    '/maison.html'],
  ['bespoke',   '/bespoke.html'],
  ['story',     '/story.html'],
  ['creations', '/creations.html'],
  ['visit',     '/visit.html'],
];
const slotKey = k => 'page' + k.charAt(0).toUpperCase() + k.slice(1);
function renderDoors(){
  const host = $('#doorGrid'); if (!host) return;
  host.innerHTML = DOORS.map(([key,href],i)=>`
    <a class="door rv" href="${href}" data-d="${i%3}">
      <span class="im" data-ref="" data-alt=""></span>
      <span class="ttl">${esc(tGet(slotKey(key)+'.title')||'')}</span>
      <p>${esc(tGet(slotKey(key)+'.lede')||'')}</p>
      <span class="open">${esc(tGet('organ.open')||'Open')}</span>
    </a>`).join('');
  $$('#doorGrid .im').forEach((el,i)=>{
    const sl = slot(slotKey(DOORS[i][0]));
    if (!sl || !sl.src) return;
    el.__slot = sl; el.dataset.ref = sl.src; io.observe(el);
  });
}

/* ── the threads ─────────────────────────────────────────────── */

/* One mark per thread, drawn in the house line: a courtyard arch, the sea,
   someone standing there, a church window, and — for the perfume that is
   gone — a bottle whose outline never quite closes. They stand in only
   while a thread has no photograph of its own. */
const THREAD_MARK = [
  '<svg viewBox="0 0 100 100" aria-hidden="true">'
  + '<path d="M22 88V46a28 28 0 0 1 56 0v42"/>'
  + '<path d="M40 88V64a10 10 0 0 1 20 0v24"/>'
  + '<path d="M10 88h80"/></svg>',

  '<svg viewBox="0 0 100 100" aria-hidden="true">'
  + '<path d="M14 34h72"/>'
  + '<path d="M8 58c8-6 14-6 22 0s14 6 22 0 14-6 22 0 14 6 22 0"/>'
  + '<path d="M4 76c8-6 14-6 22 0s14 6 22 0 14-6 22 0 14 6 22 0"/></svg>',

  '<svg viewBox="0 0 100 100" aria-hidden="true">'
  + '<path d="M50 54a17 17 0 1 0 0-34 17 17 0 0 0 0 34"/>'
  + '<path d="M20 90c0-17 13-28 30-28s30 11 30 28"/></svg>',

  '<svg viewBox="0 0 100 100" aria-hidden="true">'
  + '<path d="M28 88V46a22 22 0 0 1 44 0v42"/>'
  + '<path d="M28 64h44"/><path d="M50 46v42"/>'
  + '<path d="M14 88h72"/></svg>',

  '<svg class="dotted" viewBox="0 0 100 100" aria-hidden="true">'
  + '<path d="M42 16h16a5 5 0 0 1 5 5v11a5 5 0 0 1-5 5H42a5 5 0 0 1-5-5V21a5 5 0 0 1 5-5Z"/>'
  + '<path d="M34 37h32a8 8 0 0 1 8 8v39a8 8 0 0 1-8 8H34a8 8 0 0 1-8-8V45a8 8 0 0 1 8-8Z"/>'
  + '<path d="M43 56h14"/></svg>'
];

function renderThreads(){
  const host = $('#threadGrid'); if (!host) return;
  host.innerHTML = (DATA.organ?.threads||[]).map((t,i)=>`
    <button class="thread rv" type="button" data-th="${esc(t.id)}" data-d="${i%3}">
      <span class="im" data-ref="${esc(t.image||'')}" data-alt=""></span>
      ${t.image ? '' : `<span class="emb" aria-hidden="true">${THREAD_MARK[i % THREAD_MARK.length]}</span>`}
      <span class="n">${esc(t.num)}</span>
      <span class="ttl">${esc(L(t,'label'))}</span>
      <p>${esc(L(t,'blurb'))}</p>
      <span class="open">${esc(L(DATA.organ,'open')||'Open')}</span>
    </button>`).join('');
  /* a thread carries its own crop at two widths, like every other picture */
  const TH = (DATA.organ?.threads||[]);
  $$('#threadGrid .im').forEach((el,i)=>{ el.__slot = TH[i];
    if (el.dataset.ref) io.observe(el); });
  $$('#threadGrid .thread').forEach(b=>b.addEventListener('click',()=>openStage(b)));
}

/* ══ the memory, taken full screen ══ */
let stageReturn = null;
async function openStage(tile){
  const id = tile.dataset.th;
  const t  = (DATA.organ?.threads||[]).find(x=>x.id===id);
  if (!t) return;
  THREAD = id; PICKED = []; stageReturn = tile;

  $('#stNum').textContent   = t.num;
  $('#stTitle').textContent = L(t,'label');
  $('#stBlurb').textContent = L(t,'blurb');
  $('#chipNote').textContent = L(DATA.organ,'chipNote') || '';

  const bg = $('#stBg'); bg.querySelector('img')?.remove();
  const u = await resolve(t.image);
  if (u){ const i = new Image(); i.src = u; i.alt=''; bg.prepend(i); }

  renderChips(t); paintPyramid([], t);

  const st = $('#stage');
  st.classList.add('on');
  document.body.classList.add('noscroll');
  trap(st);
  requestAnimationFrame(()=>{ $('#stClose').focus(); liquid.start(); });
}
function closeStage(){
  const st = $('#stage');
  if (!st.classList.contains('on')) return;
  st.classList.remove('on');
  document.body.classList.remove('noscroll');
  untrap(); liquid.stop();
  stageReturn?.focus();
  THREAD = null; PICKED = [];
}

function renderChips(t){
  $('#chips').innerHTML = (t.memories||[]).map(m=>`
    <button class="chip" type="button" data-m="${esc(m.id)}" aria-pressed="${PICKED.includes(m.id)}"
      ${!PICKED.includes(m.id) && PICKED.length>=3 ? 'disabled' : ''}>
      <span class="dot" style="background:${esc(m.colour)}" aria-hidden="true"></span>${esc(L(m,'label'))}</button>`).join('');
  $$('#chips .chip').forEach(b=>b.onclick=()=>{
    const i = PICKED.indexOf(b.dataset.m);
    if (i>-1) PICKED.splice(i,1); else if (PICKED.length<3) PICKED.push(b.dataset.m);
    renderChips(t);
    paintPyramid((t.memories||[]).filter(m=>PICKED.includes(m.id)), t);
    $(`#chips [data-m="${CSS.escape(b.dataset.m)}"]`)?.focus();
  });
}

function paintPyramid(mems, thread){
  const out = $('#pyr');
  if (!mems.length){
    out.innerHTML = `<p class="blank">${esc(tGet('organ.empty'))}</p>`;
    liquid.set(0, ['#B99358']);
    $('#send').href = wa(askMsg());
    return;
  }
  const tiers = ['top','heart','base'].map(k=>{
    const s=[]; mems.forEach(m=>(L(m,k)||[]).forEach(n=>{ if(!s.includes(n)) s.push(n); })); return s;
  });
  const labs = [U('top'),U('heart'),U('base')];
  out.innerHTML = `<dl class="pyr">${tiers.map((t,i)=>
    `<div class="tier"><dt>${labs[i]}</dt><dd>${t.map(esc).join(' · ')}</dd></div>`).join('')}</dl>`;
  liquid.set(mems.length/3, mems.map(m=>m.colour||'#B99358'));
  writeFormula(tiers.flat().slice(0,7));

  const names = mems.map(m=>L(m,'label')), th = thread ? L(thread,'label') : '';
  $('#send').href = wa(LANG==='el'
    ? `Γεια σας Στεφανί! Θα ήθελα ένα προσωπικό άρωμα.\nΝήμα: ${th}\nΑναμνήσεις: ${names.join(' · ')}\nΚορυφή: ${tiers[0].join(', ')}\nΚαρδιά: ${tiers[1].join(', ')}\nΒάση: ${tiers[2].join(', ')}`
    : `Hello Stefanie! I would like a bespoke perfume.\nThread: ${th}\nMemories: ${names.join(' · ')}\nTop: ${tiers[0].join(', ')}\nHeart: ${tiers[1].join(', ')}\nBase: ${tiers[2].join(', ')}`);
}
$('#reset').onclick = ()=>{
  PICKED = [];
  const t = (DATA.organ?.threads||[]).find(x=>x.id===THREAD);
  if (t){ renderChips(t); paintPyramid([], t); }
};
$('#stClose').onclick = closeStage;

/* ══ the liquid, which knows where your hand is ══ */
const liquid = (()=>{
  const c = $('#liquid'), x = c.getContext('2d');
  const W = c.width, H = c.height;
  let raf=null, t=0, fill=0, target=0, tilt=0, tiltT=0, push=0, cols=['#B99358'], running=false;
  const rgb = h=>{ const s=String(h).replace('#',''),
    f = s.length===3 ? s.split('').map(v=>v+v).join('') : s;
    return [parseInt(f.slice(0,2),16)||185, parseInt(f.slice(2,4),16)||147, parseInt(f.slice(4,6),16)||88]; };
  const blend = ()=>{
    const v = cols.map(rgb);
    return v.reduce((p,q)=>[p[0]+q[0],p[1]+q[1],p[2]+q[2]],[0,0,0]).map(n=>Math.round(n/v.length));
  };
  /* her flacon, in the same proportions the opening curtain draws:
     round stopper, ribbed collar, sloped shoulders, the house plate */
  const INK  = 'rgba(238,228,210,.34)';   /* glass  */
  const GOLD = 'rgba(206,166,102,.62)';   /* collar, plate, the house's gold */

  function body(){ x.beginPath(); x.roundRect(40,142,120,226,10); }

  function shoulders(){
    x.beginPath();
    x.moveTo(74,120);  x.bezierCurveTo(67,129,54,134,44,142);
    x.moveTo(126,120); x.bezierCurveTo(133,129,146,134,156,142);
  }

  const wave = (p,level,amp)=>level
    + Math.sin(p*5.2 + t*1.7)*amp
    + Math.sin(p*11  + t*2.9)*amp*.45
    + (p-.5)*tilt*22;

  function frame(){
    t += .016;
    fill += (target-fill)*.06;
    tilt += (tiltT-tilt)*.07;
    push *= .94;
    x.clearRect(0,0,W,H);
    x.lineJoin='round'; x.lineCap='round';

    /* the stopper and its collar sit above the glass */
    x.strokeStyle=INK; x.lineWidth=2.2;
    x.beginPath(); x.ellipse(100,61,38,37,0,0,Math.PI*2); x.stroke();
    x.strokeStyle=GOLD;
    x.beginPath(); x.roundRect(66,100,68,20,5); x.stroke();
    x.beginPath();
    for (const px of [84,100,116]){ x.moveTo(px,100); x.lineTo(px,120); }
    x.stroke();
    x.strokeStyle=INK; shoulders(); x.stroke();

    /* the perfume itself, which answers to the chips and to your hand */
    x.save(); body(); x.clip();
    const top=142, bot=368, span=bot-top;
    const level = bot - Math.max(0,Math.min(1,fill))*span*.9;
    const [r,g,b] = blend();
    const grd = x.createLinearGradient(0,level,0,bot);
    grd.addColorStop(0,`rgba(${r},${g},${b},.9)`);
    grd.addColorStop(1,`rgba(${Math.round(r*.62)},${Math.round(g*.62)},${Math.round(b*.62)},.95)`);
    x.fillStyle = grd;
    const amp = (1.6 + push*9) * (fill>.02 ? 1 : 0);
    x.beginPath(); x.moveTo(0,H);
    for (let px=0; px<=W; px+=4) x.lineTo(px, wave(px/W, level, amp));
    x.lineTo(W,H); x.closePath(); x.fill();
    x.strokeStyle='rgba(255,240,214,.35)'; x.lineWidth=1.6;
    x.beginPath();
    for (let px=0; px<=W; px+=4){ const y=wave(px/W,level,amp); px===0?x.moveTo(0,y):x.lineTo(px,y); }
    x.stroke(); x.restore();

    /* the glass over it */
    x.save(); body();
    const gl = x.createLinearGradient(40,0,160,0);
    gl.addColorStop(0,'rgba(255,255,255,.13)');
    gl.addColorStop(.5,'rgba(255,255,255,.02)');
    gl.addColorStop(1,'rgba(255,255,255,.09)');
    x.fillStyle = gl; x.fill();
    x.strokeStyle=INK; x.lineWidth=2.2; x.stroke(); x.restore();

    /* two long highlights down the sides, as on the drawn bottle */
    x.strokeStyle='rgba(238,228,210,.16)'; x.lineWidth=1.6;
    x.beginPath(); x.moveTo(55,168); x.lineTo(55,342);
    x.moveTo(145,182); x.lineTo(145,328); x.stroke();

    /* the house plate */
    x.strokeStyle=GOLD; x.lineWidth=1.6;
    x.beginPath(); x.roundRect(65,192,70,72,5); x.stroke();
    x.fillStyle='rgba(222,200,160,.72)';
    x.font='500 17px "Playfair Display",Georgia,serif'; x.textAlign='center';
    x.fillText('LMS', 100, 234);

    if (running) raf = requestAnimationFrame(frame);
  }
  return {
    start(){ if (REDUCED){ running=false; frame(); return; } if (running) return; running=true; frame(); },
    stop(){ running=false; cancelAnimationFrame(raf); },
    set(f,c){ target=Math.max(0,Math.min(1,f)); cols=(c&&c.length)?c:['#B99358'];
              push=Math.min(.9,push+.5); if (!running) frame(); },
    hand(nx,ny){ if (REDUCED) return;
              tiltT=Math.max(-1,Math.min(1,nx*1.6)); push=Math.min(.9,push+Math.abs(ny)*.04); }
  };
})();
$('#stage').addEventListener('pointermove', e=>{
  if (REDUCED) return;
  const r = $('#liquid').getBoundingClientRect();
  liquid.hand((e.clientX-(r.left+r.width/2))/innerWidth*2,
              (e.clientY-(r.top +r.height/2))/innerHeight*2);
});

/* ══ the formula, written out by hand ══ */
let writing = null;
function writeFormula(lines){
  const hand = $('#hand'), nib = $('#nib');
  if (!hand) return;
  clearTimeout(writing?.t); if (writing) writing.dead = true;
  const w = {dead:false,t:null}; writing = w;
  hand.querySelectorAll('.ln').forEach(n=>n.remove());

  const rows = (lines && lines.length ? lines : (DATA.formula?.lines||[]))
    .map(s=>String(s).replace(/^./,c=>c.toUpperCase()));
  const spans = rows.map(txt=>{
    const ln = document.createElement('span'); ln.className='ln';
    [...txt].forEach(ch=>{ const s=document.createElement('span'); s.className='ch'; s.textContent=ch; ln.append(s); });
    ln.append(document.createTextNode('\n'));
    hand.append(ln); return ln;
  });
  const chars = spans.flatMap(l=>[...l.querySelectorAll('.ch')]);
  if (REDUCED){ chars.forEach(c=>c.classList.add('on')); return; }
  nib.classList.add('on');
  let i = 0;
  (function step(){
    if (w.dead) return;
    if (i >= chars.length){ nib.classList.remove('on'); return; }
    const c = chars[i]; c.classList.add('on');
    const hr = hand.getBoundingClientRect(), cr = c.getBoundingClientRect();
    nib.style.left = (cr.right - hr.left) + 'px';
    nib.style.top  = (cr.bottom - hr.top - 4) + 'px';
    const ch = c.textContent; i++;
    w.t = setTimeout(step, ch===' ' ? 26 : (/[.,()]/.test(ch) ? 90 : 20 + Math.random()*26));
  })();
}
function armHandwriting(){
  const paper = $('#paper'); if (!paper) return;
  const ob = new IntersectionObserver(es=>{
    es.forEach(e=>{ if (e.isIntersecting){ writeFormula(null); ob.disconnect(); } });
  },{threshold:.3});
  ob.observe(paper);
}

/* ── the shelf ───────────────────────────────────────────────── */
const cats  = ()=>(DATA.categories||[]).filter(c=>c.visible!==false).sort((a,b)=>(a.order||0)-(b.order||0));
const prods = ()=>(DATA.products||[]).filter(p=>p.visible!==false).sort((a,b)=>(a.order||0)-(b.order||0));

function renderFilters(){
  const host = $('#filters'); if (!host) return;
  host.innerHTML =
    `<button type="button" data-c="all" aria-pressed="${CAT==='all'}">${esc(L(DATA.shop,'all')||U('everything'))}</button>` +
    cats().map(c=>`<button type="button" data-c="${esc(c.id)}" aria-pressed="${CAT===c.id}">${esc(L(c,'name'))}</button>`).join('');
  $$('#filters button').forEach(b=>b.onclick=()=>{ CAT=b.dataset.c; renderFilters(); renderGrid();
    $(`#filters [data-c="${CSS.escape(CAT)}"]`)?.focus(); });
}
function renderGrid(){
  const host = $('#grid'); if (!host) return;
  const list = prods().filter(p=>CAT==='all' || p.cat===CAT);
  const cn = id=>{ const c = cats().find(x=>x.id===id); return c ? L(c,'name') : ''; };
  if (!list.length){ host.innerHTML = `<p style="color:#6A5C4E;font-size:.85rem">${U('nothing')}</p>`; return; }
  host.innerHTML = list.map((p,i)=>{
    const price = p.price
      ? `${DATA.settings.currency||'€'}${esc(p.price)}`
      : `<s>${U('onRequest')}</s>`;
    return `<article class="card rv" data-d="${i%3}">
      <span class="shot" data-ref="${esc(p.image||'')}" data-alt="${esc(L(p,'name'))}" data-pid="${esc(p.id)}">
        ${p.image?'':`<span class="ph">${esc(L(p,'name'))}</span>`}
        ${CAT==='all'?`<span class="tag">${esc(cn(p.cat))}</span>`:''}</span>
      <h3><button type="button" data-p="${esc(p.id)}">${esc(L(p,'name'))}</button></h3>
      <span class="sub">${esc(L(p,'tagline'))}</span>
      <span class="price">${price}${p.size?` · ${esc(p.size)}`:''}</span></article>`;
  }).join('');
  $$('#grid .card').forEach(c=>{
    c.querySelector('h3 button').onclick = e=>openDrawer(e.currentTarget.dataset.p);
    const s = c.querySelector('.shot');
    if (s.dataset.ref){
      s.__slot = (DATA.products||[]).find(x=>x.id===s.dataset.pid);
      io.observe(s);
    }
  });
  reveal();
}

/* ── the product drawer ──────────────────────────────────────── */
async function openDrawer(id){
  const p = (DATA.products||[]).find(x=>x.id===id); if (!p) return;
  $('#dTitle').textContent = L(p,'name');
  $('#dSub').textContent   = L(p,'tagline');
  $('#dStory').innerHTML   = `<p>${esc(L(p,'story'))}</p>`;
  $('#dSpec').innerHTML =
    (p.size?`<span><b>${U('size')}</b>${esc(p.size)}</span>`:'') +
    `<span><b>${U('price')}</b>${p.price?(DATA.settings.currency||'€')+esc(p.price):U('onRequest')}</span>` +
    `<span><b>${LANG==='el'?'Παραγωγή':'Made'}</b>${U('made')}</span>`;
  const tiers = [['top',U('top')],['heart',U('heart')],['base',U('base')]].filter(([k])=>(L(p,k)||[]).length);
  $('#dNotes').innerHTML = tiers.length
    ? `<dl class="pyr">${tiers.map(([k,l])=>
        `<div class="tier"><dt>${l}</dt><dd>${(L(p,k)||[]).map(esc).join(' · ')}</dd></div>`).join('')}</dl>`
    : '';
  const msg = LANG==='el' ? `Γεια σας! Ενδιαφέρομαι για: ${L(p,'name')}.`
                          : `Hello! I am interested in: ${L(p,'name')}.`;
  $('#dActions').innerHTML =
    (p.payLink?`<a class="btn btn-solid" href="${esc(p.payLink)}" target="_blank" rel="noopener">${U('buy')}</a>`:'') +
    `<a class="btn ${p.payLink?'btn-line':'btn-solid'}" href="${esc(wa(msg))}" target="_blank" rel="noopener">${U('enquire')}</a>`;
  const shot = $('#dShot'); shot.replaceChildren();
  const u = await resolve(p.image);
  if (u){ const i = new Image(); i.src = u; i.alt = L(p,'name'); shot.append(i); }

  document.body.classList.add('drawer');
  trap($('#drawer'));
  $('#dclose').focus();
}
function closeDrawer(){
  if (!document.body.classList.contains('drawer')) return;
  document.body.classList.remove('drawer');
  untrap();
}
$('#dclose').onclick = closeDrawer;
$('#scrim').onclick  = closeDrawer;

/* ── keeping focus where it belongs ──────────────────────────── */
let trapped = null, trapReturn = null;
const FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';
function trap(el){
  trapReturn = document.activeElement;
  trapped = el;
  document.addEventListener('keydown', trapKeys, true);
}
function untrap(){
  document.removeEventListener('keydown', trapKeys, true);
  trapped = null;
  trapReturn?.focus?.(); trapReturn = null;
}
function trapKeys(e){
  if (!trapped || e.key !== 'Tab') return;
  const items = $$(FOCUSABLE, trapped).filter(n=>n.offsetParent !== null);
  if (!items.length) return;
  const first = items[0], last = items[items.length-1];
  if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
}
addEventListener('keydown', e=>{
  if (e.key !== 'Escape') return;
  if ($('#stage')?.classList.contains('on')) closeStage();
  else if (document.body.classList.contains('drawer')) closeDrawer();
  else if (document.body.classList.contains('menu')) toggleMenu(false);
});

/* ── structured data ─────────────────────────────────────────── */
function ld(){
  const S = DATA.settings, site = CFG.siteUrl || 'https://lamaisondestefanie.com';
  $('#ldjson').textContent = JSON.stringify({"@context":"https://schema.org","@graph":[
    {"@type":["HealthAndBeautyBusiness","Store"],"@id":site+"#shop",
     name:"La Maison de Stefanie", description:L(DATA.seo,'description'),
     url:site, telephone:S.phone, email:S.email,
     image:site+"/assets/og-image.jpg", priceRange:"€€",
     currenciesAccepted:"EUR",
     address:{"@type":"PostalAddress",streetAddress:S.en.street,addressLocality:"Athens",
              postalCode:"105 56",addressCountry:"GR"},
     geo:{"@type":"GeoCoordinates",latitude:S.lat,longitude:S.lng},
     hasMap:S.mapsUrl,
     openingHoursSpecification:[{"@type":"OpeningHoursSpecification",
       dayOfWeek:["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
       opens:"11:00", closes:"20:00"}],
     sameAs:[S.instagram].filter(Boolean),
     aggregateRating:S.reviewCount?{"@type":"AggregateRating",ratingValue:String(S.rating),
       reviewCount:S.reviewCount,bestRating:"5"}:undefined,
     review:(DATA.reviews||[]).slice(0,3).map(r=>({"@type":"Review",
       author:{"@type":"Person",name:r.name},
       reviewRating:{"@type":"Rating",ratingValue:String(r.stars||5),bestRating:"5"},
       reviewBody:r.en})),
     makesOffer:prods().slice(0,12).map(p=>({"@type":"Offer",
       itemOffered:{"@type":"Product",name:L(p,'name'),description:L(p,'tagline')},
       priceCurrency:"EUR",
       ...(p.price?{price:String(p.price)}:{availability:"https://schema.org/InStock"})}))},
    {"@type":"FAQPage","@id":site+"#faq",
     mainEntity:(DATA.faq?.items||[]).map(f=>({"@type":"Question",name:L(f,'q'),
       acceptedAnswer:{"@type":"Answer",text:L(f,'a')}}))}
  ]});
}

/* ── chrome ──────────────────────────────────────────────────── */
function toggleMenu(open){
  const o = open ?? !document.body.classList.contains('menu');
  document.body.classList.toggle('menu', o);
  document.body.classList.toggle('noscroll', o);
  const b = $('#burger');
  b.setAttribute('aria-expanded', String(o));
  b.setAttribute('aria-label', o ? U('closeMenu') : U('openMenu'));
  if (!o) b.focus();
}
$('#burger').onclick = ()=>toggleMenu();

/* Which of the five you are on, so its tab is the struck one. The host
   serves these pages with and without the .html, and rewrites the links
   in the markup to drop it, so both sides are reduced to the same thing
   before they are compared. */
(function(){
  const tidy = u => u.replace(/\/index(\.html)?$/,'/')
                     .replace(/\.html$/,'')
                     .replace(/\/$/,'') || '/';
  const here = tidy(location.pathname);
  $$('.nav a[href]').forEach(a=>{
    const to = tidy(new URL(a.getAttribute('href'), location.href).pathname);
    if (to === here) a.setAttribute('aria-current','page');
  });
})();

/* smooth, but never in the way: anchors still work if this fails */
$$('a[data-nav]').forEach(a=>{
  a.addEventListener('click', e=>{
    const href = a.getAttribute('href')||'';
    if (!href.startsWith('#')) return;
    const el = document.querySelector(href);
    if (!el) return;
    e.preventDefault();
    if (document.body.classList.contains('menu')) toggleMenu(false);
    el.scrollIntoView({behavior: REDUCED ? 'auto' : 'smooth', block:'start'});
    history.replaceState(null,'',href);
    /* send the keyboard where the eye went */
    el.setAttribute('tabindex','-1');
    el.focus({preventScroll:true});
  });
});

$$('[data-lang]').forEach(b=>b.onclick=()=>{
  if (b.dataset.lang === LANG) return;
  LANG = b.dataset.lang;
  localStorage.setItem('lms-lang', LANG);
  closeStage(); closeDrawer();
  render();
});

/* the map is only ever fetched when it is asked for */
function showMap(){
  const S = DATA.settings, box = $('#mapwrap');
  /* render() ends by restoring the map for anyone who has opened it
     before, and render() runs on every page and on every change of
     language — but the map is only on the Visit page. Without this, one
     tap of "Show the map" left every other page throwing on load. */
  if (!box || box.classList.contains('loaded')) return;
  box.classList.add('loaded');
  box.innerHTML = `<iframe title="${LANG==='el'?'Χάρτης — Μνησικλέους 10, Πλάκα':'Map — Mnisikleous 10, Plaka'}"
    loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen
    src="https://www.google.com/maps?q=${S.lat},${S.lng}&z=17&output=embed"></iframe>`;
}
set('#mapLoad', e => e.onclick = ()=>{ try{ localStorage.setItem('lms-map','1'); }catch(e){} showMap(); });

/* ── reveal, rail, drift ─────────────────────────────────────── */
let ro;
function reveal(){
  ro?.disconnect();
  ro = new IntersectionObserver(es=>es.forEach(e=>{
    if (e.isIntersecting){ e.target.classList.add('in'); ro.unobserve(e.target); }
  }),{rootMargin:'0px 0px -8% 0px'});
  $$('.rv').forEach(el=>ro.observe(el));
}

let tick = false;
function frame(){
  const y = scrollY;
  $('#bar').classList.toggle('stuck', y > 60);
  tick = false;
}
addEventListener('scroll', ()=>{ if(!tick){ tick = true; requestAnimationFrame(frame); } },{passive:true});
addEventListener('resize', applyHeroMode, {passive:true});

/* if someone turns reduced motion on mid-visit, honour it at once */
motionQ.addEventListener?.('change', e=>{
  REDUCED = e.matches;
  $$('.rv').forEach(el=>el.classList.add('in'));
  if (DATA) renderHero();              /* still, or breathing */
});

boot();
