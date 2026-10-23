"""Liturgical marks and line boundaries survive the browser-to-terminal bridge."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge  # noqa: E402

NODE = shutil.which("node")
TEXTUAL = importlib.util.find_spec("textual") is not None


def plain(blocks: list[dict]) -> str:
    return "\n".join("".join(run["text"] for run in block["runs"]) for block in blocks)


@unittest.skipUnless(NODE, "node runs the shared browser renderers")
class SharedTypesettingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        done = subprocess.run([NODE, "-e", r"""
const fs=require('fs'), vm=require('vm'), dom=require('./scripts/lectern/dom.js');
globalThis.window=globalThis;
globalThis.document=dom.document;
globalThis.location={search:''};
vm.runInThisContext(fs.readFileSync('src/web/browser/shared/browser-core.js','utf8'));
const T=Triptych;
const marked=text=>dom.read(T.versicled(text));
const turn=(speaker,text,printed_marker=null,dialogue_role=null,extra={})=>
  ({speaker,text,printed_marker,dialogue_role,...extra});
const element={kind:'dialogue',speaker:'priest'};
const turns=[
  turn('priest','P. Opening.','P.'),
  turn('server','R. Answer.','R.'),
  turn('priest','P. A priest answers.','P.','response'),
  turn('server','An unclassified server line.'),
  turn('server','A marker declaration that does not match.','R.'),
  turn(null,'A source action.',null,null,{action:true}),
  turn(null,'A source gloss.',null,null,{gloss:true}),
];
const body=T.ordinaryText(element,{lang:'en',text:turns.map(t=>t.text).join('\n'),turns});
const post=JSON.parse(fs.readFileSync('src/web/data/structure/ordinary/postconciliar.json','utf8'));
const pater=post.sections.flatMap(s=>s.elements).find(e=>e.key==='ritus-communionis/pater-noster');
const latin=pater.translations.find(t=>t.lang==='la');
const properFile=JSON.parse(fs.readFileSync('src/web/data/structure/propers/roman-1962.json','utf8'));
const introit=properFile.masses.find(m=>m.key==='pentecost').propers[0];
const translation=T.orationFor(introit,'en');
translation.notice='Required acknowledgement, retained verbatim.';
const passage=dom.read(T.renderLocus({book:'Gen',chapter:1,first:1,last:2},
  {ok:true,verses:{1:'First verse.',2:'Second verse.'}},'en',{}));
const fragment=document.createDocumentFragment();
fragment.appendChild(body);
body.dataset.semanticEventId='ordinary-element/example';
body.setAttribute('data-text-language','en');
const hidden=document.createElement('p');
hidden.textContent='Hidden browser material';
hidden.hidden=true;
fragment.appendChild(hidden);
const cueRows=body.querySelectorAll('.ordinary-turn').map(row=>({
  role:row.getAttribute('data-dialogue-role'),
  cue:row.querySelector('.cue-mark')?.getAttribute('data-cue')||null,
  mark:row.querySelector('.cue-mark')?.getAttribute('data-dialogue-mark')||null,
}));
process.stdout.write(JSON.stringify({
 marks:marked('V. Gloria Patri. R. Amen.'),
 slash:marked('V/. Opening. R/. Answer. ℣ Again. ℟ Amen.'),
 initials:marked('The B. V. M. and the P. COMMUNION.'),
 prose:marked('A source hard wrap\ndoes not create a turn.'),
 turns:dom.read(body),cueRows,
 unicodeTurn:dom.read(T.ordinaryText(element,{lang:'en',turns:[turn('server','℣. Opening.','℣.')]})),
 pater:dom.read(T.ordinaryText(pater,latin)),passage,
 locus:dom.read(T.ordinaryText({kind:'heading'},{lang:'en',text:'THE ORDINARY.'},'xv')),
 compactCredits:dom.read(T.translationCredits(translation)),
 expandedCredits:dom.read(T.translationCredits(translation,{expanded:true})),
 fullCaution:translation.caution,fullLabel:translation.sourceLabel,
 unknownCredits:dom.read(T.translationCredits({source:'unclassified',caution:'A material qualification.'})),
 fragment:{contains:fragment.contains(body),rows:fragment.querySelectorAll('.ordinary-turn').length},
 reflection:{id:body.getAttribute('data-semantic-event-id'),language:body.dataset.textLanguage,
   hosts:fragment.querySelectorAll('[data-semantic-event-id]').length,hidden:dom.read(hidden)},
}));
"""], cwd=ROOT, capture_output=True, text=True, check=True, timeout=30)
        cls.result = json.loads(done.stdout)

    def test_explicit_marks_use_real_glyphs_and_own_lines(self) -> None:
        self.assertEqual(plain(self.result["marks"]), "℣ Gloria Patri. \n℟ Amen.")
        self.assertEqual(plain(self.result["slash"]), "℣ Opening. \n℟ Answer. \n℣ Again. \n℟ Amen.")

    def test_initials_and_file_hard_wraps_create_no_dialogue(self) -> None:
        self.assertEqual(plain(self.result["initials"]), "The B. V. M. and the P. COMMUNION.")
        self.assertNotIn("br", [tag for block in self.result["prose"]
                                for run in block["runs"] for tag in run["tags"]])

    def test_printed_source_mark_and_speaker_remain_independent(self) -> None:
        rows = self.result["cueRows"]
        self.assertEqual([row["cue"] for row in rows], ["P", "℟", "℟", "S", "S", None, None])
        self.assertEqual(rows[1]["role"], None)  # source typography adds no target role
        self.assertEqual(rows[2]["role"], "response")  # a priest can respond
        self.assertEqual(rows[1]["mark"], "true")
        self.assertIsNone(rows[3]["mark"])
        self.assertEqual(plain(self.result["unicodeTurn"]), "℣ Opening.")
        self.assertEqual(plain(self.result["turns"]).splitlines()[:5], [
            "P Opening.", "℟ Answer.", "℟ A priest answers.",
            "S An unclassified server line.", "S A marker declaration that does not match.",
        ])

    def test_opaque_pater_noster_keeps_its_explicit_response_on_a_new_line(self) -> None:
        said = plain(self.result["pater"])
        self.assertIn("\n℟ Sed libera nos a malo.", said)
        self.assertNotIn("R.", said)
        self.assertNotIn("Versicle.", said)

    def test_css_verse_gap_survives_without_creating_an_extra_verse(self) -> None:
        self.assertEqual(plain(self.result["passage"]), "1 First verse. 2 Second verse. ")
        runs = self.result["passage"][0]["runs"]
        self.assertEqual(sum("verse-num" in run["classes"] for run in runs), 2)
        self.assertEqual(sum("verse-gap" in run["classes"] for run in runs), 2)
        self.assertEqual(plain(self.result["locus"]), "xv  THE ORDINARY.")

    def test_fragment_supports_the_same_study_traversal_as_an_element(self) -> None:
        self.assertEqual(self.result["fragment"], {"contains": True, "rows": 7})
        self.assertEqual(self.result["reflection"], {"id": "ordinary-element/example", "language": "en",
                                                    "hosts": 1, "hidden": []})

    def test_reading_closes_research_and_study_preserves_every_source_word(self) -> None:
        compact = plain(self.result["compactCredits"])
        expanded = plain(self.result["expandedCredits"])
        self.assertIn("Historical lay translation; not approved for liturgical use.", compact)
        self.assertNotIn(self.result["fullCaution"], compact)
        self.assertIn(self.result["fullCaution"], expanded)
        self.assertIn(self.result["fullLabel"], expanded)
        self.assertIn("Required acknowledgement, retained verbatim.", compact)
        self.assertIn("A material qualification.", plain(self.result["unknownCredits"]))

    def test_terminal_study_expands_the_selected_propers_exact_source_notes(self) -> None:
        notes = bridge.call("liturgy", "studyPropers", "roman-1962", "pentecost", {"orations": "en"})
        self.assertIn(self.result["fullCaution"], plain(notes))

    def test_real_ordinary_returns_the_browser_presenters_blocks(self) -> None:
        view = bridge.call("liturgy", "day", "roman-1962", "2026-10-22",
                           {"orations": "la", "ordinary": True})
        events = view["rows"][0]["events"]
        introibo = next(event for event in events if event["id"] ==
                        "ordinary-element/praeparatio/introibo-ad-altare-dei")
        said = plain(introibo["blocks"])
        self.assertIn("P Ant. Introibo ad altare Dei.", said)
        self.assertIn("\n℟ Ad Deum, qui lætificat juventutem meam.", said)
        self.assertNotIn("Server", said)

    @unittest.skipUnless(TEXTUAL, "Textual is required to set terminal text")
    def test_terminal_retains_turns_rubrics_glosses_and_verse_spacing(self) -> None:
        from lectern.missal import blocks, ordinary_element
        from lectern.widgets import Ink

        ink = blocks(Ink(), self.result["turns"])
        said = "".join(part[0] if isinstance(part, tuple) else part for part in ink.parts)
        self.assertIn("P Opening.\n℟ Answer.\n℟ A priest answers.\n", said)
        self.assertIn("[ A source action. ]", said)
        self.assertIn("[ Source translation: A source gloss. ]", said)
        ink = blocks(Ink(), self.result["passage"])
        said = "".join(part[0] if isinstance(part, tuple) else part for part in ink.parts)
        self.assertEqual(said, "¹ First verse. ² Second verse. \n")
        ink = blocks(Ink(), self.result["compactCredits"])
        said = "".join(part[0] if isinstance(part, tuple) else part for part in ink.parts)
        self.assertIn("Translation source, differences and qualifications  (d Study)", said)
        with self.assertRaisesRegex(ValueError, "shared browser renderer"):
            ordinary_element(Ink(), {"element": {"kind": "dialogue"},
                                      "text": {"text": "Opaque text without browser blocks."}}, None)


if __name__ == "__main__":
    unittest.main()
