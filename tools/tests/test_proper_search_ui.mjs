#!/usr/bin/env node
/* Form-qualified discovery behavior against generated public indexes. */
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const require = createRequire(import.meta.url);
const search = require(resolve(root, 'src/web/browser/liturgy/proper-search.js'));
const load = async (id) => JSON.parse(await readFile(resolve(root,
  `src/web/data/structure/propers/search/${id}.json`), 'utf8'));
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
console.log('proper search UI assertions passed');
