#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import test from 'node:test';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const ROOT = resolve(import.meta.dirname, '../..');
const Payload = require(resolve(ROOT, 'src/web/browser/liturgy/reader-proper-payload.js'));
globalThis.LiturgyReaderProperPayload = Payload;
const Day = require(resolve(ROOT, 'src/web/browser/liturgy/day-read-payload.js'));
const calendar = 'roman-1962';
const key = 'last-sunday-after-pentecost';
const indexPath = 'structure/propers/index.json';
const catalogPath = 'structure/propers/catalog/roman-1962.json';
const massPath = 'structure/propers/mass/roman-1962/' + key + '.json';
const monolithPath = 'structure/propers/roman-1962.json';
const data = async (path) => JSON.parse(await readFile(resolve(ROOT, 'src/web/data', path)));
const clone = (value) => structuredClone(value);
const chosen = (index) => index.missals.find((row) => row.id === calendar);

async function fixture() {
  const index = await data(indexPath);
  const catalog = await data(catalogPath);
  const envelope = await data(massPath);
  return { index, catalog, envelope };
}

function loadFor(parts, requests) {
  return async (path) => {
    requests.push(path);
    if (path === catalogPath) return parts.catalog;
    if (path === massPath) return parts.envelope;
    if (path === monolithPath) return { fallback: true };
    throw new Error('unexpected request ' + path);
  };
}

function dayInput(parts, requests) {
  return {
    load: loadFor(parts, requests), index: parts.index, missal: calendar,
    parsed: { recognized: {}, present: [] }, mode: 'read', needsOrdinary: false,
    derived: { options: [{ settled: true, winner: { key, formulary: null },
      readable: [{ key, state: 'said' }] }] }
  };
}

test('generated 1962 payload retains the selected exact Mass and every catalog identity', async () => {
  const { index } = await fixture();
  const paths = [];
  const partial = await Payload.load({ load: async (path) => {
    paths.push(path); return data(path);
  }, indexRow: chosen(index), calendar, massKey: key });
  const full = await data(monolithPath);
  assert.deepEqual(paths, [catalogPath, massPath]);
  assert.equal(partial.masses.length, full.masses.length);
  assert.deepEqual(partial.masses.find((row) => row.key === key),
    full.masses.find((row) => row.key === key));
  assert.deepEqual(partial.coverage, full.coverage);
  assert.ok(partial.masses.filter((row) => row.key !== key)
    .every((row) => !Object.hasOwn(row, 'propers')));
});

test('catalog and selected Mass start together, then validate before rendering', async () => {
  const parts = await fixture();
  const requests = [];
  const pending = new Map();
  const loaded = Payload.load({
    indexRow: chosen(parts.index), calendar, massKey: key,
    load: (path) => {
      requests.push(path);
      return new Promise((resolve) => { pending.set(path, resolve); });
    }
  });
  assert.deepEqual(requests, [catalogPath, massPath]);
  pending.get(massPath)(parts.envelope);
  pending.get(catalogPath)(parts.catalog);
  const structure = await loaded;
  assert.equal(structure.masses.find((row) => row.key === key).name,
    parts.envelope.mass.name);
});

test('speculative catalog requests stay inside eligible Read state and reuse cache', async () => {
  const parts = await fixture();
  const requests = [];
  const cache = new Map();
  const load = (path) => {
    if (!cache.has(path)) cache.set(path, loadFor(parts, requests)(path));
    return cache.get(path);
  };
  const input = dayInput(parts, requests);
  input.load = load;
  await Payload.warmDay(input);
  await Day.loadStructure(input);
  assert.deepEqual(requests, [catalogPath, massPath]);

  for (const change of [
    (row) => { row.mode = 'missal'; },
    (row) => { row.parsed.recognized.why = '1'; },
    (row) => { row.parsed.present.push('mass'); },
    (row) => { row.index.missals.find((one) => one.id === calendar).read_payload = null; }
  ]) {
    const candidate = dayInput(clone(parts), []);
    change(candidate);
    assert.equal(Payload.warmDay(candidate), null);
  }

  const good = '#missal=roman-1962&type=sanctoral&mass=' + key + '&mode=read';
  const propersRequests = [];
  await Payload.warmPropers((path) => {
    propersRequests.push(path); return Promise.resolve(parts.catalog);
  }, good);
  assert.deepEqual(propersRequests, [catalogPath]);
  for (const invalid of [
    good + '&mode=read', good + '&unexpected=1',
    good.replace('mode=read', 'mode=study'),
    good.replace(key, '../escape'), good.replace('type=sanctoral', 'type=unknown')
  ]) {
    assert.equal(Payload.warmPropers((path) => {
      propersRequests.push(path); return Promise.resolve(parts.catalog);
    }, invalid), null);
  }
  assert.deepEqual(propersRequests, [catalogPath]);
});

test('untrusted paths, generation, and descriptor identity reject before rendering', async () => {
  const parts = await fixture();
  const requests = [];
  const load = loadFor(parts, requests);
  const normal = { load, indexRow: chosen(parts.index), calendar, massKey: key };
  await assert.rejects(Payload.load({ ...normal, massKey: '../escape' }), /calendar, Mass key/);
  const wrongPath = clone(normal.indexRow);
  wrongPath.read_payload.catalog = '../outside.json';
  await assert.rejects(Payload.load({ ...normal, indexRow: wrongPath }), /bounded payload paths/);
  const broken = clone(parts);
  broken.envelope.generation = '0'.repeat(64);
  await assert.rejects(Payload.load({ ...normal, load: loadFor(broken, []) }), /Mass envelope/);
  broken.envelope.generation = parts.envelope.generation;
  broken.envelope.mass.name = 'Substituted Mass';
  await assert.rejects(Payload.load({ ...normal, load: loadFor(broken, []) }), /Mass envelope/);
});

test('Day uses only one settled said Read Mass and falls back for unresolved or cross-Mass text', async () => {
  const parts = await fixture();
  const requests = [];
  const input = dayInput(parts, requests);
  assert.equal(Day.eligibleKey(input), key);
  assert.notEqual((await Day.loadStructure(input)).fallback, true);
  assert.deepEqual(requests, [catalogPath, massPath]);
  for (const change of [
    (row) => { row.mode = 'study'; },
    (row) => { row.parsed.recognized.why = '1'; },
    (row) => { row.parsed.present.push('mass'); },
    (row) => { row.derived.options[0].settled = false; },
    (row) => { row.derived.options[0].readable.push({ key: 'other', state: 'said' }); }
  ]) {
    const candidate = dayInput(parts, []); change(candidate);
    assert.equal(Day.eligibleKey(candidate), null);
  }
  const cross = clone(parts);
  cross.envelope.mass.takes_from = { mass: 'commune-virginum' };
  // The shared loader first validates descriptor identity; takes_from is outside
  // the descriptor, so Day itself must reject this cross-Mass dependency.
  const fallbackRequests = [];
  const fallback = await Day.loadStructure(dayInput(cross, fallbackRequests));
  assert.deepEqual(fallback, { fallback: true });
  assert.deepEqual(fallbackRequests, [catalogPath, massPath, monolithPath]);
});
