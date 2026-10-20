#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import test from 'node:test';

const require = createRequire(import.meta.url);
const preference = require('../../src/web/browser/liturgy/reader-text-size.js');

test('only supported exact enlargement preferences are accepted', () => {
  for (const size of [100, 125, 150, 175, 200]) {
    assert.equal(preference.validSize(size), size);
    assert.equal(preference.validSize(String(size)), size);
  }
  for (const invalid of [null, undefined, '', ' 150 ', '200%', '150.0', '1e2',
    0, 99, 101, 201, NaN, Infinity, {}, [150]]) {
    assert.equal(preference.validSize(invalid), null);
  }
});

test('storage failure and malformed memory leave a usable default', () => {
  for (const raw of [null, '', '200%', '999', '{}']) {
    assert.equal(preference.readPreference({ localStorage: { getItem: () => raw } }), 100);
  }
  assert.equal(preference.readPreference({ get localStorage() { throw new Error('denied'); } }), 100);
  assert.equal(preference.readPreference({ localStorage: { getItem: () => '175' } }), 175);
});

test('only valid explicit settings are persisted in the independent display preference', () => {
  const calls = [];
  const win = { localStorage: { setItem: (...args) => calls.push(args) } };
  assert.equal(preference.writePreference(win, 200), true);
  assert.deepEqual(calls, [['triptych:liturgy:text-size:v1', '200']]);
  assert.equal(preference.writePreference(win, '200%'), false);
  assert.equal(calls.length, 1);
  assert.equal(preference.writePreference({ get localStorage() { throw new Error('denied'); } }, 150), false);
});
