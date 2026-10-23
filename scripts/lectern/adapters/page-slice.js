'use strict';
/*
 * The pages' own logic where it is not exported: read out of the page's source.
 *
 * `history/history.js` keeps its model `M` (and the validators that gate every
 * literal text it shows) inside the page IIFE, `law/law.js` keeps a few
 * glossaries and count sentences there too, and the liturgy readers keep their
 * "Why this Mass", their coverage notices and their titles inside theirs. Neither is reachable from outside
 * a browser except by slicing the source text, and the repository already
 * does exactly that: `scripts/_act_history_preview.py` (BROWSER_GEOMETRY,
 * lines 31-44) slices `  const M = (function () {` .. `  }());` out of
 * history.js and runs it. This does the same, in the bridge's own realm (so
 * the JSON the bridge parses has the prototypes the model expects), with the
 * REAL `Triptych.stationKind` from browser-core.js rather than a stub.
 *
 * Every slice must occur exactly once in its page. A marker that moved throws,
 * and that is the signal to re-read the page, never to fall back to a copy.
 *
 * Nothing here is callable over the bridge: the adapter this file would be
 * loaded as exports no functions.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function section(source, start, end, file) {
  const at = source.indexOf(start);
  if (at < 0 || source.indexOf(start, at + start.length) >= 0) {
    throw new Error('the extraction contract changed in ' + file + ': ' + JSON.stringify(start) +
      ' no longer occurs exactly once; re-read the page');
  }
  const stop = source.indexOf(end, at + start.length);
  if (stop < 0) throw new Error('the extraction has no end in ' + file + ': ' + JSON.stringify(start));
  return source.slice(at, stop + end.length);
}

/* Run the named slices of one page inside a function whose parameters stand
 * for the page's own closure (`T`, `C`), declaring first whatever page state
 * the slices read (`let kindsStated`), and return what `returns` names. */
function slicePage(realm, relative, parts, options) {
  const browser = path.join(realm.ROOT, 'src', 'web', 'browser');
  const file = path.resolve(browser, relative);
  if (path.relative(browser, file).startsWith('..')) throw new Error('outside src/web/browser: ' + relative);
  const source = fs.readFileSync(file, 'utf8');
  const body = parts.map(([start, end]) => section(source, start, end, relative)).join('\n');
  const factory = vm.runInThisContext(
    '(function (' + options.params.join(', ') + ') {\n' + (options.prelude || '') + '\n' + body +
    '\nreturn {' + options.returns.join(', ') + '};\n})',
    { filename: file });
  return factory(...options.args);
}

const FN = '\n  }';
const TABLE = '\n  };';
const LINE = ';\n';

/* history.js: the model, the page's validators, its glossaries, and the
 * few count sentences the map and the station panel speak. */
function history(realm) {
  realm.script('shared/browser-core.js');
  return slicePage(realm, 'history/history.js', [
    ['  const M = (function () {', '  }());'],
    ['  function receptionsOf(station) {', FN],
    ['  const RECEPTION_WORDS = {', TABLE],
    ['  const DEFAULT_WORDS = ', LINE],
    ['  const GENERIC_WORDS = ', LINE],
    ['  let words = ', LINE],
    ['  function declaredWord(value) {', FN],
    ['  function readVocabulary(data) {', FN],
    ['  function unitWord() {', FN],
    ['  function groupWord() {', FN],
    ['  function followWord() {', FN],
    ['  function plural(word) {', FN],
    ['  function tallyOf(count, word) {', FN],
    ['  function groupsIn(payload) {', FN],
    ['  function groupsTouched(changed) {', FN],
    ['  function magnitude(station) {', FN],
    ['  function changeSummary(station) {', FN],
    ['  const CITATION_WORDS = {', TABLE],
    ['  const FIELD_NAMES = {', TABLE],
    ['  const STATE_WORDS = {', TABLE],
    ['  function whatHappened(row) {', FN],
    ['  const EDGE_WORDS = {', TABLE],
    ['  function catalogueValid(data) {', FN],
    ['  function catalogueText(value) {', FN],
    ['  function catalogueURL(value) {', FN],
    ['  const RELATION_WORDS = {', TABLE],
    ['  function comparisonValid(payload, declared) {', FN],
    ['  function nativeTextBindings(stage) {', FN],
    ['  function nativeTextValid(payload, stage, binding) {', FN],
    ['  function stageHistoryValid(history) {', FN],
  ], {
    params: ['T'],
    args: [globalThis.Triptych],
    // The page's own closure state, which `changeSummary` reads.
    prelude: 'let kindsStated = false;',
    returns: [
      'M', 'receptionsOf', 'RECEPTION_WORDS', 'readVocabulary', 'unitWord', 'groupWord', 'followWord',
      'plural', 'tallyOf', 'groupsIn', 'groupsTouched', 'magnitude', 'changeSummary', 'CITATION_WORDS',
      'FIELD_NAMES', 'STATE_WORDS', 'whatHappened', 'EDGE_WORDS', 'catalogueValid', 'catalogueText',
      'catalogueURL', 'RELATION_WORDS', 'comparisonValid', 'nativeTextBindings', 'nativeTextValid',
      'stageHistoryValid',
      'setKindsStated: function (value) { kindsStated = value; }',
    ],
  });
}

/* law.js: the glossaries and the extent sentence, over code-model.js, which
 * loads on its own as the law page loads it. */
function law(realm) {
  realm.script('shared/browser-core.js');
  realm.script('law/code-model.js');
  return slicePage(realm, 'law/law.js', [
    ['  function kindOf(station) {', FN],
    ['  function many(count, word) {', FN],
    ['  const CITATION_WORDS = {', TABLE],
    ['  const STATE_WORDS = {', TABLE],
    ['  function whatHappened(stop) {', FN],
    ['  function inLine(entry, line) {', FN],
    ['  function extentWords(station) {', FN],
    ['  const EDGE_WORDS = {', TABLE],
  ], {
    params: ['C'],
    args: [globalThis.TriptychCode],
    prelude: 'let kindsStated = false;',
    returns: [
      'C', 'kindOf', 'many', 'CITATION_WORDS', 'STATE_WORDS', 'whatHappened', 'inLine', 'extentWords',
      'EDGE_WORDS', 'setKindsStated: function (value) { kindsStated = value; }',
    ],
  });
}

module.exports = function () { return {}; };
module.exports.history = history;
module.exports.law = law;
module.exports.slicePage = slicePage;
module.exports.FN = FN;
module.exports.LINE = LINE;
