#!/usr/bin/env node
import { browserDataRoot } from './_product_data.cjs';
/* Form-qualified discovery behavior against generated public indexes. */
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const require = createRequire(import.meta.url);
const search = require(resolve(root, 'src/web/browser/liturgy/proper-search.js'));
const load = async (id) => JSON.parse(await readFile(resolve(browserDataRoot(root),
  `structure/propers/search/${id}.json`), 'utf8'));
const roman = await load('roman-1962');
const post = await load('postconciliar');
const earlier = await load('roman-pre-1955');
const keys = (rows) => rows.map((item) => [item.row.key, item.row.form_id]);

assert.ok(keys(search.find(roman, 'First Sunday of Advent')).some(([key]) => key === 'advent-1'));
assert.ok(keys(search.find(roman, 'Spiritus Domini')).some(([key]) => key === 'pentecost'));
assert.ok(keys(search.find(roman, 'Wisdom 1:7')).some(([key]) => key === 'pentecost'));
assert.ok(keys(search.find(roman, 'Caswall')).some(([key]) => key === 'pentecost'));
assert.equal(search.normalized('Ætérna Œconomia'), 'aeterna oeconomia');
assert.deepEqual(keys(search.find(roman, '11-02 Requiem')).filter(([key]) =>
  key === 'commemoratione-omnium-fidelium-defunctorum'), [
  ['commemoratione-omnium-fidelium-defunctorum', 'first'],
  ['commemoratione-omnium-fidelium-defunctorum', 'second'],
  ['commemoratione-omnium-fidelium-defunctorum', 'third'],
]);
assert.deepEqual(search.find(roman, '2026-11-02'), []);
assert.equal(search.find(roman, '').length, 0);
assert.ok(keys(search.find(post, 'Transfiguration')).some(([key]) => key === 'transfiguration-lord'));
assert.ok(keys(search.find(earlier, 'First Sunday of Advent')).some(([key]) => key === 'advent-1'));
assert.notEqual(roman.calendar, earlier.calendar);

const pentecost = search.find(roman, 'Spiritus Domini')[0].row;
const extent = search.coverage(pentecost);
assert.match(extent, /Represented non-Scripture Proper units only/);
assert.match(extent, /exact target/);
assert.match(extent, /Bible text is separate from exact Missal wording/);
assert.doesNotMatch(extent, /complete Missal/i);
// Formulary-list presentation arrives with the data (roman-1962-propers.md
// § Reader list presentation): each resumed Sunday follows its Epiphanytide
// counterpart in that group, the after-Pentecost run ends at the Last Sunday,
// and the Easter-dependent Sundays share one marked note.
for (const index of [roman, earlier]) {
  const seasonal = index.rows.filter((row) => row.kind === 'seasonal');
  const order = seasonal.map((row) => row.key);
  assert.deepEqual(order.slice(order.indexOf('epiphany-3'), order.indexOf('septuagesima')), [
    'epiphany-3', 'resumed-epiphany-3', 'epiphany-4', 'resumed-epiphany-4',
    'epiphany-5', 'resumed-epiphany-5', 'epiphany-6', 'resumed-epiphany-6',
  ]);
  const afterPentecost = seasonal.filter((row) => search.listSeason(row) === 'after-pentecost');
  assert.equal(afterPentecost.at(-1).key, 'last-sunday-after-pentecost');
  assert.ok(!afterPentecost.some((row) => row.key.startsWith('resumed-')));
  for (const key of ['resumed-epiphany-3', 'resumed-epiphany-6']) {
    const row = seasonal.find((one) => one.key === key);
    assert.equal(row.season, 'after-pentecost');
    assert.equal(search.listSeason(row), 'epiphanytide');
  }
  const notes = search.listNotes(seasonal);
  assert.equal(notes.length, 1);
  assert.equal(notes[0].mark, '†');
  assert.match(notes[0].text, /^These Sundays move with the date of Easter each year\./);
  assert.deepEqual(seasonal.filter((row) => search.listMark(row, notes)).map((row) => row.key), [
    'epiphany-2', 'epiphany-3', 'resumed-epiphany-3', 'epiphany-4', 'resumed-epiphany-4',
    'epiphany-5', 'resumed-epiphany-5', 'epiphany-6', 'resumed-epiphany-6',
    'last-sunday-after-pentecost',
  ]);
}
assert.deepEqual(search.listNotes(post.rows), []);
assert.ok(post.rows.every((row) => row.listing === null));
console.log('proper search UI assertions passed');
