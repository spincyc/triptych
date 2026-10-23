"""Explicitly undated commentary stays outside the dated chronological chain."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import PropertyMock, patch

ROOT = Path(__file__).resolve().parents[2]
if __package__:
    from . import test_catena_production as production
else:
    import test_catena_production as production

LABEL = "Composition date not established"
REASON_A = "Checked witness does not establish a usable composition year for this text."
REASON_Z = "Reviewed introduction leaves this individual homily's date unresolved."


def source(author, date, voice="original", reason=None, **extra):
    row = {"author": author, "work": author + " commentary", "date": date,
           "language": "la" if voice == "original" else "en", "voice": voice,
           "edition": "Explicit synthetic test witness", "translators": [] if voice == "original" else ["Fixture translator"],
           "rights": "public-domain"}
    if reason is not None:
        row.update(composition_date_status="unestablished", composition_date_basis=reason)
    row.update(extra)
    return row


def fragment(identifier, key):
    return {"id": identifier, "source": key, "locator": identifier, "text_words": 5,
            "review": "verified", "extent": {"token": "Gen", "first_chapter": 1,
            "last_chapter": 1, "first_verse": 1, "last_verse": 1}}


SPINE = {"_adversarial": "EXPLICIT SYNTHETIC UNDATED FIXTURE — NOT CORPUS EVIDENCE",
         "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
         "sources": {
             "known-a": source("Known A", 300), "known-b": source("Known B", 500),
             "unknown-a": source("Unknown A", None, reason=REASON_A),
             "unknown-z": source("Unknown Z", None, "translation", REASON_Z)},
         # Unknowns are deliberately scattered; only their section may reorder.
         "fragments": [fragment("fixture.unknown-z", "unknown-z"),
                       fragment("fixture.known-a", "known-a"),
                       fragment("fixture.unknown-a", "unknown-a"),
                       fragment("fixture.known-b", "known-b")],
         "leads": [], "blocked": [], "refusals": {}}


def fixture_files(spine):
    files = {"structure/catena/01-gen/001.json": spine}
    for row in spine["fragments"]:
        owner = spine["sources"][row["source"]]
        files[f"structure/catena/text/{row['id']}.json"] = {
            "id": row["id"], "text": "Explicit synthetic test text for " + row["id"],
            "basis": "Synthetic test extent", "date_basis": owner.get("composition_date_basis", "Known fixture date")}
    return files


def run(root, scenarios, extra_inspection=False):
    harness = production.REPLAY
    if extra_inspection:
        marker = "    chapterNames: withClass('chapter-name').map(text),"
        assert marker in harness
        harness = harness.replace(marker, marker + """
    compositionLabels: withClass('fragment-date').map(text),
    dateReasons: withClass('fragment-basis').map(text),
    datedIds: withClass('chain').filter((node) =>
      node.parentNode && new ClassList(node.parentNode).contains('chain-column'))
      .flatMap((node) => node.descendants().filter((one) =>
        new ClassList(one).contains('fragment-whole')).map((one) => one.href.split('=')[1])),
    undatedIds: withClass('aside').filter((node) =>
      node.getAttribute('data-date-state') === 'unestablished')
      .flatMap((node) => node.descendants().filter((one) =>
        new ClassList(one).contains('fragment-whole')).map((one) => one.href.split('=')[1])),
""")
    scratch = ROOT / ".scratch"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="catena-undated-", dir=scratch) as folder:
        script, plan = Path(folder) / "replay.cjs", Path(folder) / "plan.json"
        script.write_text(harness)
        plan.write_text(json.dumps(scenarios))
        done = subprocess.run(["node", str(script), str(root), str(plan)], capture_output=True, text=True, timeout=60)
        if done.returncode:
            raise AssertionError(done.stderr)
        return json.loads(done.stdout)



@unittest.skipUnless(production.NODE, "node is required for the Catena consumer model")
class UndatedConsumerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scenarios = [
            {"name": "mixed", "hash": production.GEN1, "files": fixture_files(SPINE),
             "steps": [{"do": "openEveryFragment", "label": "opened"}]},
            {"name": "original", "hash": production.GEN1 + "&voice=original", "files": fixture_files(SPINE)},
            {"name": "english", "hash": production.GEN1 + "&voice=translation:en", "files": fixture_files(SPINE)},
        ]
        only = dict(SPINE, fragments=[row for row in SPINE["fragments"] if "unknown" in row["id"]])
        scenarios.append({"name": "only", "hash": production.GEN1, "files": fixture_files(only)})
        cls.pages = run(ROOT, scenarios, True)

    def test_the_chronological_chain_and_undated_section_are_separate(self):
        page = self.pages["mixed"]
        self.assertNotIn("error", page, page.get("error"))
        self.assertEqual(page["datedIds"], ["fixture.known-a", "fixture.known-b"])
        self.assertEqual(page["undatedIds"], ["fixture.unknown-a", "fixture.unknown-z"])
        self.assertIn(LABEL, page["sectionHeadings"])
        self.assertEqual(page["fragmentCount"], 4)
        self.assertEqual(page["tallyText"], "4 fragments held")

    def test_undated_rows_show_a_label_and_one_reason_even_after_loading(self):
        page = self.pages["mixed"]["snapshots"]["opened"]
        self.assertEqual(page["compositionLabels"], ["300", "500", LABEL, LABEL])
        for reason in (REASON_A, REASON_Z):
            self.assertEqual(page["dateReasons"].count("Date — " + reason), 1)
        self.assertEqual(len(page["fragmentTexts"]), 4)
        self.assertTrue(all("Explicit synthetic test text" in text for text in page["fragmentTexts"]))
        self.assertTrue(all(href in page["undatedIds"] for href in ("fixture.unknown-a", "fixture.unknown-z")))

    def test_voices_include_both_date_classes_without_substitution(self):
        original, english = self.pages["original"], self.pages["english"]
        self.assertEqual(original["datedIds"], ["fixture.known-a", "fixture.known-b"])
        self.assertEqual(original["undatedIds"], ["fixture.unknown-a"])
        self.assertEqual(english["datedIds"], [])
        self.assertEqual(english["undatedIds"], ["fixture.unknown-z"])
        self.assertIn("4 fragments held", english["tallyText"])

    def test_an_undated_only_chapter_has_no_pretend_dated_chain(self):
        page = self.pages["only"]
        self.assertEqual(page["datedIds"], [])
        self.assertEqual(page["undatedIds"], ["fixture.unknown-a", "fixture.unknown-z"])
        self.assertEqual(page["tallyText"], "2 fragments held")
        self.assertEqual(page["busy"], "false")

    def test_exact_explicit_metadata_is_required(self):
        probe = r"""
const M = require(process.argv[1]);
const rows = [
 {date:null,composition_date_status:'unestablished',composition_date_basis:' checked '},
 {date:null},
 {date:null,composition_date_status:'unestablished'},
 {date:null,composition_date_status:'unestablished',composition_date_basis:' '},
 {date:null,composition_date_status:'other',composition_date_basis:'checked'},
 {date:400,composition_date_status:'unestablished',composition_date_basis:'checked'}
];
process.stdout.write(JSON.stringify(rows.map((row) => ({metadata:M.compositionDateMetadata(row),label:M.compositionDateLabel(row)}))));
"""
        done = subprocess.run(["node", "-e", probe, str(ROOT / "src/web/browser/catena/catena-model.js")],
                              capture_output=True, text=True, check=True)
        rows = json.loads(done.stdout)
        self.assertEqual(rows[0], {"metadata": {"composition_date_status": "unestablished", "composition_date_basis": "checked"}, "label": LABEL})
        self.assertEqual(rows[1:], [{"metadata": {}, "label": ""}] * 5)

    def test_dated_rows_keep_their_order_without_unknown_metadata(self):
        probe = r"""
const M = require(process.argv[1]);
const rows = [
 {id:'known-a',author:'Author A',work:'First',date:'300'},
 {id:'known-b',author:'Author B',work:'Second',date:'400'},
 {id:'known-c',author:'Author A',work:'Third',date:'500'}
];
process.stdout.write(JSON.stringify({
 ids:M.commentaryGroups(rows).flatMap((group) => group.fragments.map((row) => row.id)),
 metadata:rows.map(M.compositionDateMetadata)
}));
"""
        done = subprocess.run(["node", "-e", probe, str(ROOT / "src/web/browser/catena/catena-model.js")],
                              capture_output=True, text=True, check=True)
        result = json.loads(done.stdout)
        self.assertEqual(result["ids"], ["known-a", "known-b", "known-c"])
        self.assertEqual(result["metadata"], [{}, {}, {}])


@unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required for the terminal reader")
class UndatedTerminalTest(unittest.TestCase):
    def test_date_label_and_reason_survive_a_missing_text_without_duplication(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from lectern.surfaces.catena import Catena
        row = {"id": "fixture.unknown", "author": "Test author", "work": "Test work", "date": None,
               "composition_date_status": "unestablished", "composition_date_basis": REASON_A,
               "locator": "Test location", "extent": "Genesis 1:1", "spans": False,
               "chip": "Latin — the author’s own", "text_words": 5, "edition": "Test witness",
               "edition_published": "", "translators": [], "rights": "public-domain",
               "attribution": "", "rights_basis": "", "reviewNote": ""}
        owner = Catena()
        owner.current = {"chain": {"fragments": [row]}}
        screens = []
        from types import SimpleNamespace
        app = SimpleNamespace(push_screen=lambda screen, callback: screens.append(screen))
        with patch.object(Catena, "app", new_callable=PropertyMock, return_value=app):
            owner.open_reading(0, row, {"missing": True, "date_basis": REASON_A})
        text = screens[0].body.plain
        self.assertIn(LABEL, text)
        self.assertEqual(text.count(REASON_A), 1)
        self.assertIn("The text of this fragment could not be loaded.", text)
        self.assertIn("source library: fixture.unknown", text)



if __name__ == "__main__":
    unittest.main()
