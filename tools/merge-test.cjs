/* Exercise the merge rules against the cases that actually matter. */
const fs = require('fs');
const root = {};
new Function('window', fs.readFileSync('/home/user/Maisondestefanie/assets/content-merge.js', 'utf8'))(root);
const M = root.LMSContent;

let pass = 0, fail = 0;
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function t(name, got, want) {
  if (eq(got, want)) { pass++; console.log('  ok   ' + name); }
  else { fail++; console.log('  FAIL ' + name + '\n    got  ' + JSON.stringify(got) + '\n    want ' + JSON.stringify(want)); }
}

/* ---- 1. the round trip: her content survives diff then merge ---- */
const base1 = { a: 1, b: { c: 'x', d: 'y' }, list: [{ id: 'p1', n: 'one' }, { id: 'p2', n: 'two' }] };
const hers1 = JSON.parse(JSON.stringify(base1));
hers1.b.c = 'SHE CHANGED THIS';
hers1.list[1].n = 'TWO, HERS';
const p1 = M.diff(base1, hers1);
t('round trip reproduces her content', M.merge(base1, p1), hers1);
t('patch holds only what she changed', p1, { b: { c: 'SHE CHANGED THIS' }, list: { _list: true, _items: { p2: { n: 'TWO, HERS' } } } });

/* ---- 2. my later change flows through where she never touched ---- */
const newBase1 = JSON.parse(JSON.stringify(base1));
newBase1.b.d = 'I CHANGED THIS';
newBase1.a = 99;
const merged1 = M.merge(newBase1, p1);
t('my change to an untouched field appears', merged1.b.d, 'I CHANGED THIS');
t('my change to another untouched field appears', merged1.a, 99);
t('her change still wins on the field she edited', merged1.b.c, 'SHE CHANGED THIS');

/* ---- 3. I change a field she HAS edited: hers wins ---- */
const newBase2 = JSON.parse(JSON.stringify(base1));
newBase2.b.c = 'I ALSO CHANGED THIS';
t('she wins on a field we both changed', M.merge(newBase2, p1).b.c, 'SHE CHANGED THIS');

/* ---- 4. I add a list item; she had edited a different one ---- */
const newBase3 = JSON.parse(JSON.stringify(base1));
newBase3.list.push({ id: 'p3', n: 'three, new from me' });
const m3 = M.merge(newBase3, p1);
t('my new list item appears', m3.list.map(x => x.id), ['p1', 'p2', 'p3']);
t('her edit to p2 survives my addition', m3.list[1].n, 'TWO, HERS');

/* ---- 5. she deletes an item: it stays deleted ---- */
const hers2 = JSON.parse(JSON.stringify(base1));
hers2.list = hers2.list.filter(x => x.id !== 'p1');
const p2 = M.diff(base1, hers2);
t('deletion is written down', p2.list._removed, ['p1']);
t('deleted item stays gone', M.merge(base1, p2).list.map(x => x.id), ['p2']);
const newBase4 = JSON.parse(JSON.stringify(base1));
newBase4.list.push({ id: 'p9', n: 'added later by me' });
t('deletion holds even after I add elsewhere', M.merge(newBase4, p2).list.map(x => x.id), ['p2', 'p9']);

/* ---- 6. she adds an item of her own ---- */
const hers3 = JSON.parse(JSON.stringify(base1));
hers3.list.push({ id: 'own1', n: 'hers alone' });
const p3 = M.diff(base1, hers3);
t('her own item round trips', M.merge(base1, p3).list.map(x => x.id), ['p1', 'p2', 'own1']);
t('her own item survives my additions', M.merge(newBase4, p3).list.map(x => x.id), ['p1', 'p2', 'p9', 'own1']);

/* ---- 7. she reorders ---- */
const hers4 = JSON.parse(JSON.stringify(base1));
hers4.list.reverse();
const p4 = M.diff(base1, hers4);
t('order is recorded', p4.list._order, ['p2', 'p1']);
t('her order is kept', M.merge(base1, p4).list.map(x => x.id), ['p2', 'p1']);
t('my later addition lands at the end of her order', M.merge(newBase4, p4).list.map(x => x.id), ['p2', 'p1', 'p9']);

/* ---- 8. no edits at all means an empty patch ---- */
t('no edits produces no patch', M.diff(base1, JSON.parse(JSON.stringify(base1))), undefined);
t('an empty patch is just the build', M.merge(newBase4, undefined), newBase4);

/* ---- 9. lists of plain strings are taken whole ---- */
const base5 = { steps: ['one', 'two', 'three'] };
const hers5 = { steps: ['one', 'TWO HERS', 'three'] };
t('a plain list is stored whole', M.diff(base5, hers5), { steps: ['one', 'TWO HERS', 'three'] });
t('a plain list merges whole', M.merge({ steps: ['a', 'b'] }, M.diff(base5, hers5)).steps, ['one', 'TWO HERS', 'three']);

/* ---- 10. what the Studio shows her ---- */
const ch = M.changedFields(base1, newBase1, p1);
const bd = ch.find(c => c.path === 'b.d');
const bc = ch.find(c => c.path === 'b.c');
t('a build change on an untouched field is listed as not hers', bd && bd.hers, false);
t('a build change she has overridden is flagged as hers', bc === undefined || bc.hers, true);

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
