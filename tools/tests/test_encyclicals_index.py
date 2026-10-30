"""The encyclicals index, the catalogue it generates, and the page's model.

`scripts/_encyclicals.py` is the gate between the tracked index and the file
the `/encyclicals/` page reads; `src/web/browser/encyclicals/encyclicals-model.js`
is what that page sorts and narrows with. Both are exercised here against a
small synthetic release record, and the model again under node against the
tracked catalogue whenever one is present.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
MODEL = REPOSITORY / "src/web/browser/encyclicals/encyclicals-model.js"
TRACKED_CATALOGUE = REPOSITORY / "src/web/data/encyclicals/index.json"
NODE = shutil.which("node")


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "test_encyclicals_generator", REPOSITORY / "scripts/_encyclicals.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_browser_driver():
    spec = importlib.util.spec_from_file_location(
        "encyclicals_browser_driver", REPOSITORY / "tools/tests/test_browser_truthfulness.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class EncyclicalsIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.generator = load_generator()
        self.documents = []
        for identity, language, pages in (
            ("papal.leo-xiii.rerum-novarum", "la", 12),
            ("papal.leo-xiii.rerum-novarum", "en", 14),
            ("acta.ass.010.act-007", "la", 3),
        ):
            data = f"%PDF-1.7 {identity} {language}\n".encode()
            pdf = f"pdf/papal-documents/1891-05-15--{identity}--{language}--0123456789abcdef.pdf"
            self.documents.append({
                "id": identity, "language": language, "pdf": pdf,
                "pdf_sha256": digest(data), "pages": pages, "bytes": len(data),
                "review": {"status": "PASS"},
                "source": {"rights_status": "public-domain"},
            })
        self.release = {"schema": "triptych-papal-release/v1", "documents": self.documents}
        self.index = {
            "schema": "triptych-encyclicals-index/v2",
            "revision": "2026-10-28T12:00:00Z",
            "scope": "Synthetic test index.",
            "description_provenance": {
                "author": "Claude (Anthropic), AI-written project apparatus",
                "method": "Written from each act's text.",
                "written_on": "2026-10-28",
            },
            "encyclicals": [
                self.row("papal.gregory-xvi.mirari-vos", "Gregory XVI", "gregorius-xvi", 8,
                         "1832-08-15", "Mirari vos", readers=[self.reader(2, "fragment")]),
                self.row("papal.leo-xiii.rerum-novarum", "Leo XIII", "leo-xiii", 10,
                         "1891-05-15", "Rerum novarum", subject="On capital and labor",
                         readers=[self.reader(0), self.reader(1, "damaged")]),
                self.row("papal.pius-xii.humani-generis", "Pius XII", "pius-xii", 14,
                         "1950-08-12", "Humani generis", readers=[]),
                self.row("encyclical.pius-ix.undated.example", "Pius IX", "pius-ix", 9,
                         None, "Exemplum", readers=[]),
            ],
        }

    def reader(self, position: int, extent: str = "complete") -> dict:
        document = self.documents[position]
        return {
            "language": document["language"], "release_id": document["id"],
            "pdf": document["pdf"], "pdf_sha256": document["pdf_sha256"],
            "pages": document["pages"], "witness": "Acta Sanctae Sedis 23 (1890-91)",
            "extent": extent,
        }

    def row(self, identity, pope, pope_id, pontificate, date, title, *, readers, subject=None):
        return {
            "id": identity, "pope": pope, "pope_id": pope_id,
            "pontificate_index": pontificate, "date": date,
            "year": int(date[:4]) if date else None, "title": title, "subject": subject,
            "description": f"A one-line summary of {title}.",
            "description_basis": (
                f"local-reader:{readers[0]['release_id']}" if readers
                else "vatican-page:https://www.vatican.va/content/example.html"
            ),
            "readers": readers,
            "english_routes": [],
            "links": {"vatican": "https://www.vatican.va/content/example.html"},
            "no_local_text_reason": None if readers else "No qualifying historical printing acquired yet",
        }

    def write(self, name: str, value: object) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=1) + "\n", encoding="utf-8")
        return path

    def render(self) -> dict:
        index = self.write("index.json", self.index)
        release = self.write("release.json", self.release)
        return json.loads(self.generator.render(index, release, self.root))

    def refused(self, expected: str) -> str:
        with self.assertRaises(self.generator.EncyclicalsError) as failure:
            self.render()
        self.assertIn(expected, str(failure.exception))
        return str(failure.exception)

    def test_a_valid_index_becomes_the_browser_catalogue(self) -> None:
        catalogue = self.render()
        self.assertEqual("triptych-encyclicals-browser/v2", catalogue["schema"])
        self.assertEqual(self.index["encyclicals"], catalogue["encyclicals"])
        self.assertEqual(
            ["gregorius-xvi", "pius-ix", "leo-xiii", "pius-xii"],
            [pope["id"] for pope in catalogue["popes"]],
        )
        self.assertEqual(["la", "en"], [language["code"] for language in catalogue["languages"]])
        self.assertEqual(
            {"encyclicals": 4, "with_local_text": 2, "without_local_text": 2,
             "readers": 3, "pages": 29,
             "english": {"complete": 0, "source_complete": 0,
                         "external_complete": 0, "incomplete_only": 1, "unavailable": 3,
                         "source_readers": 1, "external_routes": 0}},
            catalogue["counts"],
        )
        index_bytes = (self.root / "index.json").read_bytes()
        self.assertEqual(digest(index_bytes), catalogue["index"]["sha256"])
        self.assertEqual(self.index["description_provenance"], catalogue["description_provenance"])

    def test_structure_writes_reads_an_alternative_index_and_checks_drift(self) -> None:
        index = self.write("elsewhere/trial-index.json", self.index)
        release = self.write("release.json", self.release)
        out = self.root / "data"
        arguments = ["--root", str(self.root), "structure", "--index", str(index),
                     "--release", str(release), "--out", str(out)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, self.generator.main(arguments))
        target = out / "encyclicals/index.json"
        first = target.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, self.generator.main(arguments + ["--check"]))
            self.assertEqual(0, self.generator.main(arguments))
        self.assertEqual(first, target.read_bytes(), "the output must be deterministic")
        self.index["encyclicals"][0]["description"] = "A changed summary."
        self.write("elsewhere/trial-index.json", self.index)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(1, self.generator.main(arguments + ["--check"]))
        self.assertEqual(first, target.read_bytes(), "--check must write nothing")
        default = self.generator._paths(self.root, None, None, None)
        self.assertEqual(self.root / "src/sources/papal-documents/encyclicals-index.json", default[0])

    def test_a_reader_whose_hash_differs_from_the_release_record_is_refused(self) -> None:
        self.index["encyclicals"][1]["readers"][0]["pdf_sha256"] = "0" * 64
        self.refused("pdf_sha256")

    def test_a_reader_the_release_record_does_not_install_is_refused(self) -> None:
        reader = dict(self.reader(0), release_id="papal.leo-xiii.unrecorded",
                      pdf="pdf/papal-documents/1891-unrecorded--la--0000000000000000.pdf")
        self.index["encyclicals"][1]["readers"].append(reader)
        self.refused("is not a document of release/papal-documents.json")

    def test_a_reader_must_agree_with_its_release_row_in_every_field(self) -> None:
        for field, value, expected in (
            ("pages", 13, "pages 13 does not match"),
            ("pdf", "pdf/papal-documents/other--la--0123456789abcdef.pdf", "does not match"),
            ("language", "it", "in 'it' is not a document"),
            ("extent", "partial", "extent must be one of"),
            ("pdf", "pdf/gpt/work.pdf", "must name a file under pdf/papal-documents/"),
        ):
            with self.subTest(field=field, value=value):
                self.setUp()
                self.index["encyclicals"][1]["readers"][0][field] = value
                self.refused(expected)

    def test_a_reader_needs_a_reviewed_public_domain_release_row(self) -> None:
        self.documents[0]["review"]["status"] = "FAIL"
        self.refused("no PASS review")
        self.setUp()
        self.documents[0]["source"]["rights_status"] = "licensed"
        self.refused("no public-domain distribution basis")

    def test_availability_is_always_stated_one_way_or_the_other(self) -> None:
        self.index["encyclicals"][2]["no_local_text_reason"] = None
        self.refused("must say why no local text is offered")
        self.setUp()
        self.index["encyclicals"][1]["no_local_text_reason"] = "Published after 1930"
        self.refused("must not carry no_local_text_reason")

    def test_descriptions_are_short_single_lines_with_a_stated_basis(self) -> None:
        self.index["encyclicals"][0]["description"] = "x" * 161
        self.refused("the limit is 160")
        self.setUp()
        self.index["encyclicals"][0]["description"] = "Two\nlines."
        self.refused("one line of plain English or null")
        self.setUp()
        self.index["encyclicals"][0]["description_basis"] = "local-reader:papal.leo-xiii.rerum-novarum"
        self.refused("not one of this row's readers")
        self.setUp()
        self.index["encyclicals"][2]["description_basis"] = "memory:somewhere"
        self.refused("description_basis must be")
        self.setUp()
        del self.index["description_provenance"]["author"]
        self.refused("description_provenance must hold exactly author, method and written_on")

    def test_a_description_not_yet_written_is_null_with_a_null_basis(self) -> None:
        self.index["encyclicals"][2]["description"] = None
        self.index["encyclicals"][2]["description_basis"] = None
        self.assertIsNone(self.render()["encyclicals"][2]["description"])
        self.index["encyclicals"][2]["description_basis"] = "vatican-page:https://www.vatican.va/x.html"
        self.refused("names a basis for a description that is null")

    def test_rows_run_by_date_then_undated_and_popes_never_go_backwards(self) -> None:
        rows = self.index["encyclicals"]
        rows[0], rows[1] = rows[1], rows[0]
        self.refused("out of order")
        self.setUp()
        self.index["encyclicals"][1]["pontificate_index"] = 7
        self.refused("after encyclicals[0]")
        self.setUp()
        self.index["encyclicals"][2]["pope"] = "Pius XI"
        self.index["encyclicals"][2]["pope_id"] = "leo-xiii"
        self.refused("is 'Leo XIII' at pontificate 10 elsewhere")

    def test_identity_schema_links_and_languages_are_strict(self) -> None:
        cases = (
            (lambda: self.index["encyclicals"].append(dict(self.index["encyclicals"][3])),
             "is listed twice"),
            (lambda: self.index["encyclicals"][0].update({"notes": "extra"}),
             "fields differ from the schema"),
            (lambda: self.index["encyclicals"][0]["links"].update(
                {"vatican": "https://example.org/mirari"}), "www.vatican.va"),
            (lambda: self.index["encyclicals"][0].update({"year": 1833}),
             "does not match date"),
            (lambda: self.index.update({"schema": "triptych-encyclicals-index/v3"}),
             "schema must be"),
            (lambda: self.index["encyclicals"][0].update({"subject": ""}),
             "subject must be text or null"),
        )
        for change, expected in cases:
            with self.subTest(expected=expected):
                self.setUp()
                change()
                self.refused(expected)
        self.setUp()
        self.documents[2]["language"] = "xx"
        self.index["encyclicals"][0]["readers"][0]["language"] = "xx"
        self.refused("has no reader-facing label")

    def route(self, extent="complete", **changes) -> dict:
        return dict({"url": "https://www.vatican.va/content/example-en.html",
                     "label": "Holy See English text", "language": "en", "extent": extent,
                     "authority": "official", "checked_on": "2026-10-29",
                     "source_index_url": "https://www.vatican.va/content/index.html",
                     "verification_note": "English body and closing checked."}, **changes)

    def test_external_english_does_not_claim_a_local_reader_or_complete_a_fragment(self) -> None:
        self.index["encyclicals"][0]["english_routes"] = [self.route("fragment")]
        self.index["encyclicals"][2]["english_routes"] = [self.route()]
        catalogue = self.render()
        self.assertEqual(2, catalogue["counts"]["with_local_text"])
        self.assertEqual(3, catalogue["counts"]["readers"])
        self.assertEqual({"complete": 1, "source_complete": 0,
                          "external_complete": 1, "incomplete_only": 2, "unavailable": 1,
                          "source_readers": 1, "external_routes": 2},
                         catalogue["counts"]["english"])
        self.assertIsNotNone(catalogue["encyclicals"][2]["no_local_text_reason"])

    def test_external_route_identity_extent_and_check_are_explicit(self) -> None:
        for changes, expected in (
            ({"url": "javascript:alert(1)"}, "https URL"),
            ({"url": "https://user:secret@www.vatican.va/a"}, "without credentials"),
            ({"url": "https://example.org/a"}, "official route must be"),
            ({"language": "la"}, "language 'en'"),
            ({"checked_on": "2026-02-30"}, "checked_on"),
            ({"extent": "excerpt"}, "extent must be"),
            ({"verification_note": ""}, "verification_note"),
        ):
            with self.subTest(changes=changes):
                self.index["encyclicals"][2]["english_routes"] = [self.route(**changes)]
                self.refused(expected)
        self.index["encyclicals"][2]["english_routes"] = [self.route(), self.route()]
        self.refused("duplicate english_routes identity")

    def test_partial_damaged_and_unreviewed_external_english_never_count_as_complete(self) -> None:
        for extent in ("fragment", "damaged", "unreviewed"):
            with self.subTest(extent=extent):
                self.index["encyclicals"][2]["english_routes"] = [self.route(extent)]
                english = self.render()["counts"]["english"]
                self.assertEqual(0, english["complete"])
                self.assertEqual(2, english["incomplete_only"])

    def test_strict_json_refuses_duplicate_keys(self) -> None:
        path = self.root / "index.json"
        path.write_text('{"schema": "a", "schema": "b"}\n', encoding="utf-8")
        release = self.write("release.json", self.release)
        with self.assertRaisesRegex(self.generator.EncyclicalsError, "duplicate JSON key"):
            self.generator.render(path, release, self.root)


MODEL_REPLAY = r"""
const M = require(process.argv[1]);
const catalogue = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
const ids = (rows) => rows.map((row) => row.id);
const all = catalogue.encyclicals;
const report = {};
for (const sort of M.SORTS.map((one) => one.value)) report['order:' + sort] = ids(M.order(all, sort));
for (const filter of M.TEXT_FILTERS.map((one) => one.value)) {
  report['text:' + filter] = ids(M.narrow(catalogue, { pope: '', text: filter, find: '' }));
}
report.pope = ids(M.narrow(catalogue, { pope: catalogue.popes[0].id, text: '', find: '' }));
report.find = ids(M.narrow(catalogue, { pope: '', text: '', find: process.argv[3] }));
report.findNothing = ids(M.narrow(catalogue, { pope: '', text: '', find: 'zzzz-no-such-word' }));
const params = (text) => new URLSearchParams(text);
report.invalid = M.stateFrom(params('pope=nobody&text=greek&sort=colour'), catalogue).invalid;
report.valid = M.stateFrom(params('pope=' + catalogue.popes[0].id + '&sort=-title'), catalogue);
report.hash = M.hashPairs({ pope: '', text: 'la', sort: 'date', find: ' x ' });
report.toggle = [M.toggled('date', 'date'), M.toggled('-date', 'date'), M.toggled('-date', 'pope')];
report.columns = M.languageColumns(catalogue).map((one) => one.code);
report.longDate = M.longDate('1891-05-15');
report.tally = M.tally(all);
process.stdout.write(JSON.stringify(report));
"""


@unittest.skipIf(NODE is None, "node is not installed; the page's model cannot be replayed")
class EncyclicalsModelTest(unittest.TestCase):
    """The page's sorting and filtering, replayed from the file the page loads."""

    def replay(self, catalogue_path: Path, find: str) -> dict:
        result = subprocess.run(
            [NODE, "-e", MODEL_REPLAY, str(MODEL), str(catalogue_path), find],
            capture_output=True, text=True, cwd=REPOSITORY,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def synthetic_catalogue(self) -> Path:
        fixture = EncyclicalsIndexTest("test_a_valid_index_becomes_the_browser_catalogue")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        catalogue = fixture.render()
        path = fixture.root / "catalogue.json"
        path.write_text(json.dumps(catalogue), encoding="utf-8")
        return path

    def test_sorting_filtering_and_addresses_on_a_known_catalogue(self) -> None:
        report = self.replay(self.synthetic_catalogue(), "capital labor")
        gregory, leo, pius_xii, undated = (
            "papal.gregory-xvi.mirari-vos", "papal.leo-xiii.rerum-novarum",
            "papal.pius-xii.humani-generis", "encyclical.pius-ix.undated.example",
        )
        self.assertEqual([gregory, leo, pius_xii, undated], report["order:date"])
        # Undated stays last whichever way the dates run.
        self.assertEqual([pius_xii, leo, gregory, undated], report["order:-date"])
        # Pontificate order, not name order: Pius IX (9) before Leo XIII (10).
        self.assertEqual([gregory, undated, leo, pius_xii], report["order:pope"])
        self.assertEqual([pius_xii, leo, undated, gregory], report["order:-pope"])
        self.assertEqual([undated, pius_xii, gregory, leo], report["order:title"])
        self.assertEqual([leo, gregory, pius_xii, undated], report["order:-title"])
        self.assertEqual([gregory, leo], report["text:la"])
        self.assertEqual([leo], report["text:en"])
        self.assertEqual([gregory, leo], report["text:la-or-en"])
        self.assertEqual([pius_xii, undated], report["text:none"])
        self.assertEqual(4, len(report["text:"]))
        self.assertEqual([gregory], report["pope"])
        self.assertEqual([leo], report["find"])
        self.assertEqual([], report["findNothing"])
        self.assertEqual(
            [{"key": "pope", "value": "nobody"}, {"key": "text", "value": "greek"},
             {"key": "sort", "value": "colour"}],
            report["invalid"],
        )
        self.assertEqual([], report["valid"]["invalid"])
        self.assertEqual("-title", report["valid"]["state"]["sort"])
        self.assertEqual([["pope", ""], ["text", "la"], ["sort", ""], ["find", "x"]], report["hash"])
        self.assertEqual(["-date", "date", "pope"], report["toggle"])
        self.assertEqual(["la", "en"], report["columns"])
        self.assertEqual("15 May 1891", report["longDate"])
        self.assertEqual(2, report["tally"]["withText"])
        self.assertEqual(1, report["tally"]["undated"])

    @unittest.skipUnless(TRACKED_CATALOGUE.is_file(), "no tracked encyclicals catalogue yet")
    def test_the_tracked_catalogue_sorts_and_narrows_consistently(self) -> None:
        catalogue = json.loads(TRACKED_CATALOGUE.read_text(encoding="utf-8"))
        report = self.replay(TRACKED_CATALOGUE, "")
        rows = {row["id"]: row for row in catalogue["encyclicals"]}
        total = len(rows)
        for sort in ("date", "-date", "pope", "-pope", "title", "-title"):
            with self.subTest(sort=sort):
                self.assertEqual(total, len(report["order:" + sort]))
                self.assertEqual(set(rows), set(report["order:" + sort]))
        indices = [rows[key]["pontificate_index"] for key in report["order:pope"]]
        self.assertEqual(sorted(indices), indices)
        dated = [rows[key]["date"] for key in report["order:date"] if rows[key]["date"]]
        self.assertEqual(sorted(dated), dated)
        self.assertEqual(total, len(report["text:"]))
        with_text = {key for key, row in rows.items() if row["readers"]}
        self.assertEqual(set(report["text:none"]), set(rows) - with_text)
        self.assertLessEqual(set(report["text:la-or-en"]), with_text)
        self.assertEqual(catalogue["counts"]["with_local_text"], report["tally"]["withText"])
        self.assertEqual(catalogue["counts"]["english"], report["tally"]["english"])

    def test_complete_english_excludes_fragments_and_counts_overlapping_routes_once(self) -> None:
        fixture = EncyclicalsIndexTest("test_a_valid_index_becomes_the_browser_catalogue")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        rows = fixture.index["encyclicals"]
        rows[0]["english_routes"] = [fixture.route("fragment")]
        rows[1]["english_routes"] = [fixture.route()]
        rows[1]["readers"][1]["extent"] = "complete"
        rows[2]["english_routes"] = [fixture.route()]
        catalogue = fixture.render()
        path = fixture.write("mixed-catalogue.json", catalogue)
        report = self.replay(path, "English external")
        self.assertEqual([rows[1]["id"], rows[2]["id"]], report["text:en-complete"])
        self.assertEqual([rows[1]["id"]], report["text:en"])
        self.assertEqual([row["id"] for row in rows[:3]], report["text:en-external"])
        self.assertEqual([rows[0]["id"], rows[3]["id"]], report["text:en-missing"])
        self.assertEqual(catalogue["counts"]["english"], report["tally"]["english"])
        self.assertEqual(2, report["tally"]["english"]["complete"])
        self.assertEqual(1, report["tally"]["english"]["incomplete_only"])


@unittest.skipIf(NODE is None, "node is not installed")
class EncyclicalsBrowserTest(unittest.TestCase):
    def test_external_source_and_missing_english_are_distinct_in_the_page(self) -> None:
        fixture = EncyclicalsIndexTest("test_a_valid_index_becomes_the_browser_catalogue")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        rows = fixture.index["encyclicals"]
        rows[0]["english_routes"] = [fixture.route("fragment")]
        rows[2]["english_routes"] = [fixture.route()]
        rows[1]["readers"][1]["extent"] = "complete"
        catalogue = fixture.render()
        # Reuse the repository's real Chromium runner; response replacement
        # leaves the production page/controller/model unchanged.
        driver = load_browser_driver()
        report = driver.drive({
            "responses": {"src/web/data/encyclicals/index.json": json.dumps(catalogue)},
            "acts": [
                {"do": "navigate", "url": driver.page("encyclicals")},
                {"do": "wait", "until": "document.querySelectorAll('tr.enc-row').length === 4"},
                {"do": "eval", "name": "initial", "expression": """(() => ({
                  rows: Array.from(document.querySelectorAll('tr.enc-row')).map(row => ({
                    id: row.dataset.id, text: row.textContent,
                    pdfs: Array.from(row.querySelectorAll('a[type="application/pdf"]')).map(a => a.getAttribute('href')),
                    online: Array.from(row.querySelectorAll('a.enc-online')).map(a => a.href)
                  })), english: document.getElementById('enc-english-tally').textContent,
                  viewport: innerWidth, document: document.documentElement.scrollWidth
                }))()"""},
                {"do": "eval", "expression": """(() => {
                  const select = document.getElementById('text-select');
                  select.value = 'en-complete'; select.dispatchEvent(new Event('change'));
                })()"""},
                {"do": "eval", "name": "complete", "expression":
                 "Array.from(document.querySelectorAll('tr.enc-row')).map(row => row.dataset.id)"},
                {"do": "eval", "name": "hash", "expression": "location.hash"},
            ],
        })
        by_id = {row["id"]: row for row in report["initial"]["rows"]}
        self.assertIn("Fragment", by_id[rows[0]["id"]]["text"])
        self.assertIn("Complete English not recorded", by_id[rows[0]["id"]]["text"])
        self.assertIn("Source PDF", by_id[rows[1]["id"]]["text"])
        self.assertTrue(all(path.startswith("../pdf/papal-documents/") for path in by_id[rows[1]["id"]]["pdfs"]))
        self.assertEqual([], by_id[rows[2]["id"]]["pdfs"])
        self.assertEqual([fixture.route()["url"]], by_id[rows[2]["id"]]["online"])
        self.assertIn("No source PDF here", by_id[rows[2]["id"]]["text"])
        self.assertIn("No English text recorded", by_id[rows[3]["id"]]["text"])
        self.assertIn("2 of 4 have complete English", report["initial"]["english"])
        self.assertLessEqual(report["initial"]["document"], report["initial"]["viewport"])
        self.assertEqual([rows[1]["id"], rows[2]["id"]], report["complete"])
        self.assertEqual("#text=en-complete", report["hash"])

    def test_narrow_pdf_labels_and_pope_names_reflow_at_200_percent_text(self) -> None:
        fixture = EncyclicalsIndexTest("test_a_valid_index_becomes_the_browser_catalogue")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        driver = load_browser_driver()
        seam = "await cdp.send('Runtime.enable');"
        self.assertIn(seam, driver.HARNESS)
        driver.HARNESS = driver.HARNESS.replace(seam, seam + """
          await cdp.send('Emulation.setDeviceMetricsOverride', {
            width: 320, height: 852, deviceScaleFactor: 1, mobile: false
          });
        """)
        report = driver.drive({
            "responses": {"src/web/data/encyclicals/index.json": json.dumps(fixture.render())},
            "acts": [
                {"do": "navigate", "url": driver.page("encyclicals")},
                {"do": "wait", "until": "document.querySelectorAll('tr.enc-row').length === 4"},
                {"do": "eval", "expression": "document.documentElement.style.fontSize = '200%'"},
                {"do": "eval", "name": "layout", "expression": """({
                  viewport: innerWidth, document: document.documentElement.scrollWidth,
                  popeLines: Array.from(document.querySelectorAll('.enc-pope')).map(e =>
                    e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight))
                })"""},
            ],
        })["layout"]
        self.assertEqual(320, report["viewport"])
        self.assertLessEqual(report["document"], report["viewport"])
        self.assertTrue(all(lines <= 3 for lines in report["popeLines"]), report)


if __name__ == "__main__":
    unittest.main()
