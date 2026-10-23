"""Catena reads canonical chapters through the published edition projection.

The regression is real: canonical Psalm 50 previously fetched KJV Psalm 50
and showed a different psalm beside its commentary. These tests run the same
loader used by the browser and Lectern, with the shared citation picker.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
sys.path.insert(0, str(ROOT / "scripts"))
from lectern import bridge  # noqa: E402


@unittest.skipUnless(NODE, "node is required to run the Catena model")
class CatenaScriptureTests(unittest.TestCase):
    PROBE = r"""
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const root = process.argv[1];
globalThis.window = globalThis;
globalThis.document = require(path.join(root, 'scripts/lectern/dom.js')).document;
globalThis.location = {search: '', hash: ''};
globalThis.addEventListener = () => {};
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/shared/browser-core.js'), 'utf8'));
const T = globalThis.Triptych;
const M = require(path.join(root, 'src/web/browser/catena/catena-model.js'));
const index = {
  scripture: 'structure/catena/scripture/',
  canon: [
    {token: 'Ps', name: 'Psalms', chapters: 150, path: '21-ps', testament: 'old'},
    {token: 'Dan', name: 'Daniel', chapters: 14, path: '32-dan', testament: 'old'}
  ]
};
const bible = M.bibleRecord({id: 'king-james-version', label: 'King James',
  numbering: 'hebrew', loci: 'hebrew-unnumbered-titles', language: 'en'});
const citation = (token, chapter, loci) => ({token, numbering: 'vulgate',
  ref: token + ' ' + chapter, loci: {vulgate: [{chapter, first: null, last: null}]},
  edition_loci: {[bible.id]: loci}, refused: {}, unresolved: null});
async function read(token, chapter, cite, change, verses) {
  const calls = [];
  let file = {schema: 'triptych-catena-scripture/v1', token,
    chapters: {[chapter]: cite}};
  if (change) file = change(file);
  const result = await M.readScripture(index, token, chapter, bible, {
    file: async (where) => { calls.push(['projection', where]); return file; },
    chapter: async (book, number) => {
      calls.push(['chapter', book, number]);
      return {ok: true, verses: verses || {'1': book + ' ' + number + ' first',
        '2': book + ' ' + number + ' second', '3': 'outside extent'}};
    },
    paragraphs: async (book, number) => {
      calls.push(['paragraphs', book, number]); return {breaks: {'2': 'printed'}};
    },
    pick: (one) => T.editionLoci(one, bible),
    recast: (one, picked) => T.recastLoci(one, bible, 'vulgate', picked),
    format: T.formatLoci
  });
  return {result, calls};
}
(async () => {
  const ps = citation('Ps', 50, [{book: 'Ps', chapter: 51, first: 1, last: 2}]);
  const refused = structuredClone(ps);
  refused.refused[bible.id] = 'The verse boundary is not established.';
  const split = citation('Dan', 13, [
    {book: 'Sus', chapter: 1, first: 1, last: 2},
    {book: 'Bel', chapter: 1, first: 1, last: 1}
  ]);
  const missing = structuredClone(ps);
  missing.edition_loci[bible.id][0].last = 9;
  const out = {
    psalm: await read('Ps', 50, ps),
    split: await read('Dan', 13, split),
    refused: await read('Ps', 50, refused),
    wrongOwner: await read('Ps', 50, ps, (file) => ({...file, token: 'Dan'})),
    missingChapter: await read('Ps', 50, ps, (file) => ({...file, chapters: {}})),
    staleBounds: await read('Ps', 50, missing),
    interiorGap: await read('Ps', 50,
      citation('Ps', 50, [{book: 'Ps', chapter: 51, first: 1, last: 3}]),
      undefined, {'1': 'first', '3': 'third'}),
    unsafePath: M.scripturePath({...index, scripture: '../other/'}, 'Ps'),
    addressing: bible.loci,
  };
  process.stdout.write(JSON.stringify(out));
})().catch((error) => { process.stderr.write(error.stack); process.exitCode = 1; });
"""

    @classmethod
    def setUpClass(cls) -> None:
        done = subprocess.run(
            [NODE, "-e", cls.PROBE, str(ROOT)], cwd=ROOT,
            capture_output=True, text=True, timeout=30,
        )
        if done.returncode:
            raise RuntimeError(done.stderr)
        cls.results = json.loads(done.stdout)

    def test_psalm_50_fetches_51_and_only_its_projected_extent(self) -> None:
        row = self.results["psalm"]
        self.assertTrue(row["result"]["ok"])
        self.assertIn(["chapter", "Ps", 51], row["calls"])
        self.assertNotIn(["chapter", "Ps", 50], row["calls"])
        part, = row["result"]["parts"]
        self.assertEqual(part["label"], "Psalms 51:1-2")
        self.assertEqual(list(part["verses"]), ["1", "2"])
        self.assertIn("51:1-2", row["result"]["note"])
        self.assertIn(["paragraphs", "Ps", 51], row["calls"])

    def test_a_canonical_chapter_can_reach_two_native_books(self) -> None:
        parts = self.results["split"]["result"]["parts"]
        self.assertEqual([(p["book"], p["chapter"]) for p in parts], [("Sus", 1), ("Bel", 1)])
        self.assertEqual([len(p["verses"]) for p in parts], [2, 1])

    def test_refusal_or_missing_projection_never_fetches_a_same_number(self) -> None:
        for key in ("refused", "wrongOwner", "missingChapter"):
            with self.subTest(key=key):
                row = self.results[key]
                self.assertFalse(row["result"]["ok"])
                self.assertFalse([call for call in row["calls"] if call[0] == "chapter"])
        self.assertIn("boundary is not established", self.results["refused"]["result"]["problem"])
        self.assertIsNone(self.results["unsafePath"])

    def test_a_stale_extent_is_refused_without_clamping(self) -> None:
        row = self.results["staleBounds"]
        self.assertFalse(row["result"]["ok"])
        self.assertIn("extent is not present", row["result"]["problem"])

    def test_the_manifest_addressing_survives_the_catena_boundary(self) -> None:
        self.assertEqual(self.results["addressing"], "hebrew-unnumbered-titles")

    def test_a_missing_middle_verse_refuses_the_whole_extent(self) -> None:
        row = self.results["interiorGap"]
        self.assertFalse(row["result"]["ok"])
        self.assertIn("extent is not present", row["result"]["problem"])
        self.assertNotIn("parts", row["result"])


@unittest.skipUnless(NODE, "node is required to run the Catena adapter")
class PublishedCatenaScriptureTests(unittest.TestCase):
    def view(self, token: str, chapter: int) -> dict:
        return bridge.call("catena", "view", token, chapter, "king-james-version", "")

    def test_miserere_reads_native_psalm_51_beside_canonical_50(self) -> None:
        view = self.view("Ps", 50)
        self.assertEqual(view["reference"], "Psalms 50")
        scripture = view["scripture"]
        self.assertTrue(scripture["ok"], scripture)
        section, = scripture["sections"]
        self.assertEqual(section["label"], "Psalms 51")
        self.assertEqual(scripture["verseCount"], 19)
        self.assertTrue(section["paragraphs"][0]["verses"][0]["text"].startswith("Have mercy upon me"))
        self.assertIn("51", scripture["note"])

    def test_joined_and_split_psalms_keep_the_native_ranges(self) -> None:
        for canonical, labels, counts in (
            (9, ["Psalms 9", "Psalms 10"], [20, 18]),
            (113, ["Psalms 114", "Psalms 115"], [8, 18]),
            (147, ["Psalms 147:12ff."], [9]),
        ):
            with self.subTest(chapter=canonical):
                scripture = self.view("Ps", canonical)["scripture"]
                self.assertTrue(scripture["ok"], scripture)
                self.assertEqual([s["label"] for s in scripture["sections"]], labels)
                self.assertEqual([s["verseCount"] for s in scripture["sections"]], counts)

    def test_daniel_13_reaches_susanna_and_bel_in_order(self) -> None:
        scripture = self.view("Dan", 13)["scripture"]
        self.assertTrue(scripture["ok"], scripture)
        self.assertEqual([s["label"] for s in scripture["sections"]], ["Sus 1:1-64", "Bel 1:1"])
        self.assertEqual(scripture["verseCount"], 65)

    def test_unmapped_or_absent_text_is_a_refusal(self) -> None:
        for token, chapter, reason in (("Dan", 14, "no counterpart"), ("Ecclus", 3, "not mapped")):
            with self.subTest(token=token):
                scripture = self.view(token, chapter)["scripture"]
                self.assertFalse(scripture["ok"])
                self.assertIn(reason, scripture["problem"])


if __name__ == "__main__":
    unittest.main()
