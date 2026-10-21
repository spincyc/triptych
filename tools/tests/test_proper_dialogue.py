"""Explicit Proper dialogue markers start lines and retain accessible glyphs."""
from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
CORE = Path(os.environ.get("TRIPTYCH_CORE_PATH", ROOT / "src/web/browser/shared/browser-core.js"))

HARNESS = r"""
const fs = require('node:fs');
function node(tag) {
  return {nodeType:1,tagName:tag.toUpperCase(),className:'',textContent:'',lang:null,
    get lastChild(){return this.children.at(-1);},
    children:[],attrs:{},appendChild(child){this.children.push(child);return child;},
    setAttribute(key,value){this.attrs[key]=value;},addEventListener(){}};
}
global.document = {createElement:node,
  createTextNode:text=>({nodeType:3,nodeValue:text,get data(){return this.nodeValue;}}),createDocumentFragment:()=>node('#fragment'),
  addEventListener(){}};
global.window = {location:{search:''},addEventListener(){}};
eval(fs.readFileSync(process.env.TRIPTYCH_CORE_PATH,'utf8'));
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
function hasClass(node,wanted){return String(node.className||'').split(/\s+/).includes(wanted);}
function report(root){
  const marks=[],breaks=[],rubrics=[],stanzas=[];
  function text(node){
    if ('data' in node) return node.data;
    if (hasClass(node,'visually-hidden')) return '';
    return node.tagName==='BR' ? '\n' : (node.textContent||'')+(node.children||[]).map(text).join('');
  }
  function visit(node){
    if (hasClass(node,'vr-mark')) {
      const glyph=node.children.find(child=>hasClass(child,'vr-glyph'));
      const label=node.children.find(child=>hasClass(child,'visually-hidden'));
      marks.push({glyph:glyph.textContent,hidden:glyph.attrs['aria-hidden'],label:label.textContent,lang:label.lang});
    }
    if (node.tagName==='BR') breaks.push(true);
    if (hasClass(node,'inline-rubric')) rubrics.push(text(node));
    if (hasClass(node,'stanza')) stanzas.push(text(node));
    for (const child of node.children||[]) visit(child);
  }
  visit(root);
  return {text:text(root),marks,breaks:breaks.length,rubrics,stanzas};
}
process.stdout.write(JSON.stringify(cases.map(row=>report(window.Triptych.composedBody(row.text,row.structure||null,null)))));
"""


def render(*cases: dict) -> list[dict]:
    result = subprocess.run(
        ["node", "-e", HARNESS], cwd=ROOT,
        env={**os.environ, "TRIPTYCH_CORE_PATH": str(CORE)},
        input=json.dumps(cases), text=True, capture_output=True, check=True, timeout=15,
    )
    return json.loads(result.stdout)


def proper(key: str, name: str) -> dict:
    payload = json.loads((ROOT / f"src/web/data/structure/propers/mass/roman-1962/{key}.json").read_text())
    return next(row for row in payload["mass"]["propers"] if row["name"] == name)


class ProperDialogueTests(unittest.TestCase):
    def assert_mark(self, actual: dict, letter: str) -> None:
        self.assertEqual(actual, {
            "glyph": {"V": "℣", "R": "℟"}[letter], "hidden": "true",
            "label": {"V": "Versicle.", "R": "Response."}[letter], "lang": "en",
        })

    def test_palm_sunday_explicit_exchange_uses_two_lines_in_both_languages(self) -> None:
        latin = proper("palm-sunday", "Versicle at the Beginning of the Procession")
        english = next(row for row in latin["translations"] if row["lang"] == "en")
        la, en = render(latin, english)
        self.assertEqual(la["breaks"], 1)
        self.assertEqual(en["breaks"], 1)
        self.assertEqual(la["text"], latin["text"].replace("V.", "℣").replace("R.", "\n℟"))
        self.assertEqual(en["text"], english["text"].replace("R.", "\n℟"))
        self.assertEqual(len(la["marks"]), 2)
        self.assert_mark(la["marks"][0], "V")
        self.assert_mark(la["marks"][1], "R")
        self.assertEqual(len(en["marks"]), 1)
        self.assert_mark(en["marks"][0], "R")

    def test_source_printed_response_glyph_uses_the_same_accessible_mark(self) -> None:
        source = proper("seventh-day-within-octave", "Collect")
        found, = render(source)
        self.assertEqual(found["breaks"], 1)
        self.assertEqual(found["text"], source["text"].replace("℟.", "\n℟"))
        self.assertEqual(len(found["marks"]), 1)
        self.assert_mark(found["marks"][0], "R")

    def test_ascii_and_glyph_markers_share_the_same_presentation(self) -> None:
        ascii_source = "V. First call. R. First answer. V. Second call. R. Second answer."
        glyph_source = ascii_source.replace("V.", "℣.").replace("R.", "℟")
        ascii_body, glyph_body = render({"text": ascii_source}, {"text": glyph_source})
        self.assertEqual(ascii_body, glyph_body)
        self.assertEqual(ascii_body["breaks"], 3)
        self.assertEqual([row["glyph"] for row in ascii_body["marks"]], ["℣", "℟", "℣", "℟"])

    def test_abbreviations_and_speaker_letters_create_no_dialogue_roles(self) -> None:
        source = "Of the B. V. M. and the P. Com. P. Priest words. R.S.V. A name V. inside prose.\nA source hard wrap."
        found, = render({"text": source})
        self.assertEqual(found["text"], source)
        self.assertEqual(found["marks"], [])
        self.assertEqual(found["breaks"], 0)

    def test_marker_at_a_checked_stanza_boundary_needs_no_extra_empty_line(self) -> None:
        source = "V. First call.\nR. First answer."
        boundary = source.index("R.")
        found, = render({"text": source, "structure": {"stanzas": [0, boundary]}})
        self.assertEqual(found["breaks"], 0)
        self.assertEqual(found["stanzas"], ["℣ First call.", "℟ First answer."])

    def test_checked_inline_action_keeps_its_exact_words_and_offsets(self) -> None:
        source = "V. First call (bow). R. First answer."
        start = source.index("(bow)")
        found, = render({"text": source, "structure": {
            "actions": [{"kind": "rubric", "start": start, "end": start + len("(bow)")}]}})
        self.assertEqual(found["rubrics"], ["(bow)"])
        self.assertEqual(found["breaks"], 1)
        self.assertEqual(found["text"], "℣ First call (bow). \n℟ First answer.")


    def test_response_after_a_checked_action_still_starts_a_line(self) -> None:
        source = "V. First call. (bow) R. First answer."
        start = source.index("(bow)")
        found, = render({"text": source, "structure": {
            "actions": [{"kind": "rubric", "start": start, "end": start + len("(bow)")}]}})
        self.assertEqual(found["rubrics"], ["(bow)"])
        self.assertEqual(found["breaks"], 1)
        self.assertEqual(found["text"], "℣ First call. (bow) \n℟ First answer.")

if __name__ == "__main__":
    unittest.main()
