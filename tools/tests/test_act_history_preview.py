"""A printable preview cannot silently lose isolated stations or invent joins."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET

from scripts import _act_history_preview as preview
from tools.tests import test_act_history_reception as reception


ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/stages-print"
BROWSER = ROOT / "src/web/browser/history/history.js"
NS = {"s": preview.NS}


def stage_fixture():
    """Constructed claims exercise presentation without pretending to be history."""
    evidence = [{"source_id": "fixture-source", "locus": "constructed pages 1–2",
                 "claim": "This fixture supports no historical claim."}]
    stages = []
    for identifier, label, start, end, status in (
        ("state-a", "First constructed book state", 1500, 1500, "documented"),
        ("state-b", "A bounded constructed revision", 1550, 1550, "documented"),
        ("state-c", "An uncertain attestation date", 1590, 1610, "documented"),
        ("state-undated", "An unpositioned state", None, None, "documented"),
        ("state-lead", "A provisional state remains a lead", 1650, 1650, "provisional"),
    ):
        stages.append({"id": identifier, "tradition_id": "fixture-tradition", "label": label,
                       "date_label": "unknown" if start is None else str(start) if start == end else f"{start}–{end}",
                       "start_year": start, "end_year": end, "date_kind": "attestation", "status": status,
                       "scope": "Only one constructed rubric.", "components": ["rubrics"],
                       "witness_ids": [], "witness_label": "Constructed witness; not a real book",
                       "summary": "A short rubric in a constructed state.", "text_coverage": "not-transcribed",
                       "evidence": evidence, "limitations": "This is test data, not evidence.",
                       "reception": "No community reception asserted."})
    return {"schema": "triptych-eucharistic-stages/v1", "traditions": [
        {"id": "fixture-tradition", "label": "Constructed tradition", "family": "fixture",
         "scope": "One test tradition.", "coverage_note": "Deliberately incomplete."}],
        "sources": [{"id": "fixture-source", "title": "Constructed primary description",
                     "url": "https://example.org/constructed", "kind": "primary-act", "status": "inspected",
                     "inspection": "A synthetic source used only in tests.", "checked_on": "2026-10-16",
                     "limitations": "No real source was inspected."}], "stages": stages,
        "transitions": [{"id": "change-ab", "from_stage": "state-a", "to_stage": "state-b",
                         "kind": "revision", "status": "documented", "evidence_level": "primary-description",
                         "summary": "The rubric adds a second bow after the prayer.", "components": ["rubrics"],
                         "changes": [{"component": "rubrics", "before": "One bow before the prayer.",
                                      "after": "A second bow after the prayer.", "locus_before": "first rubric",
                                      "locus_after": "revised rubric", "evidence": evidence}], "evidence": evidence,
                         "limitations": "Source-described, not text-collated.", "comparison_ids": [],
                         "historical_parentage": "established", "git_ancestry": False, "text_inheritance": False}],
        "gaps": [{"id": "fixture-gap", "tradition_id": "fixture-tradition", "period": "1550–1590",
                  "missing": "No established link to the uncertain witness.", "next_source": "A missing constructed folio.",
                  "consequence": "No connector is drawn across this gap."}], "limitations": []}


class ActHistoryPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in ("node", "rsvg-convert", "pdfunite"):
            try:
                preview.executable(name)
            except preview.PreviewError as error:
                raise unittest.SkipTest(str(error)) from error
        SCRATCH.mkdir(parents=True, exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.tool = reception.load_tool()
        data = cls.tool.load(reception.MISSAL)
        cls.plate = Path(cls.tool.plate(data, cls.root / "plate")["written"])
        cls.spine = json.loads(Path(cls.tool.structure(data, cls.root / "data")["written"]).read_text())
        cls.output = cls.root / "preview"
        cls.audit = preview.render_preview(plate_path=cls.plate, spine=cls.spine,
                                          out_dir=cls.output, browser_source=BROWSER,
                                          catalogue={"records": [{"id": "unaccepted-candidate"}]})
        cls.svg = ET.parse(cls.output / "latin-missal-preview.svg").getroot()

    def test_every_station_parent_and_isolated_root_survives(self):
        expected_ids = {s["id"] for s in self.spine["stations"]}
        expected_edges = {(p, s["id"]) for s in self.spine["stations"] for p in s["parents"]}
        marks = self.svg.findall('.//s:g[@data-station]', NS)
        paths = self.svg.findall('.//s:path[@data-from]', NS)
        self.assertEqual({m.get("data-station") for m in marks}, expected_ids)
        self.assertEqual(len(marks), len(expected_ids))
        self.assertEqual({(p.get("data-from"), p.get("data-to")) for p in paths}, expected_edges)
        self.assertEqual(len(paths), len(expected_edges))
        isolated = expected_ids - {s for pair in expected_edges for s in pair}
        self.assertEqual(len(isolated), 4, "the fixture must continue exercising the observed LOOM loss")
        self.assertEqual(self.audit["isolated_count"], len(isolated))
        self.assertNotIn("unaccepted-candidate", ET.tostring(self.svg, encoding="unicode"))
        self.assertEqual(self.audit["status"], "review-preview")
        self.assertEqual(self.audit["renderer"], "existing-browser-geometry")

    def test_printed_stations_and_partial_coverage_remain_explicit(self):
        marks = {m.get("data-station"): m for m in self.svg.findall('.//s:g[@data-station]', NS)}
        for station in self.spine["stations"]:
            circle = marks[station["id"]].find('s:circle', NS)
            self.assertEqual(circle.get("fill") == "white", station["station_kind"] == "printed")
        words = " ".join(self.svg.itertext())
        for phrase in ("recorded lines", "graph steps, not years", "parent-link evidence", "Text coverage is partial"):
            self.assertIn(phrase, words)
        self.assertNotIn("17 traditions", words)
        self.assertEqual(self.audit["reception_count"], 0)

    def test_catalogue_pdf_has_every_station_identifier(self):
        try:
            extractor = preview.executable("pdftotext")
        except preview.PreviewError as error:
            self.skipTest(str(error))
        result = preview.run([extractor, "-layout", str(self.output / "latin-missal-catalogue.pdf"), "-"])
        for station in self.spine["stations"]:
            self.assertIn(station["id"], result.stdout)
        self.assertTrue((self.output / "latin-missal-preview.pdf").read_bytes().startswith(b"%PDF"))

    def test_full_titles_and_single_named_panel_replace_numeric_only_lanes(self):
        visible = self.svg.findall('.//s:text[@data-label-for]', NS)
        for station in self.spine["stations"]:
            label = " ".join(node.text for node in visible if node.get("data-label-for") == station["id"])
            self.assertEqual(" ".join(station["title"].split()), " ".join(label.split()))
        geometry = json.loads((self.output / "latin-missal-preview-parts/browser-geometry.json").read_text())
        panels = geometry["panels"]
        self.assertEqual(len(panels), len({s["line"] for s in self.spine["stations"]}))
        roman = [p for p in panels if p["line"] == "typica"]
        self.assertEqual(len(roman), 1)
        self.assertGreater(roman[0]["tracks"], 1, "the fixture must retain the Holy Week branch inside its line")
        self.assertGreater(self.audit["detail_pages"], 1)
        self.assertEqual(set(self.audit["station_sheets"]), {s["id"] for s in self.spine["stations"]})

    def test_research_relationship_is_visible_without_becoming_an_act_parent(self):
        evidence = {"source_id": "constructed-source", "locus": "fixture p. 1", "source": {
            "title": "Constructed research citation", "inspection_status": "inspected",
            "inspection": "A test fixture, not historical evidence.", "url": "https://example.org/fixture"}}
        group = {"id": "test-group", "label": "Constructed group", "status": "declared"}
        catalogue = {
            "presentation_groups": [group],
            "entries": [{"id": "candidate-book", "title": "A candidate book", "family": "fixture",
                         "date_label": "1500", "chronology": {"start": 1500, "end": 1500},
                         "presentation_group": group}],
            "relationship_entities": [{"id": "undated-donor", "label": "An undated textual tradition",
                                       "kind": "textual-tradition", "family": "fixture", "presentation_group": group,
                                       "scope": "Only the donor tradition named by the source.",
                                       "basis": "A qualified conceptual donor, not an identified edition.",
                                       "limitations": "The exact donor witness remains unidentified.", "evidence": [evidence]}],
            "relationships": [{"id": "constructed-relationship", "kind": "borrowing", "label": "A bounded borrowing claim",
                               "from": "undated-donor", "to": "candidate-book", "directed": True, "certainty": "sourced",
                               "scope": "A single named prayer.", "basis": "A constructed basis.",
                               "limitations": "Does not establish an edition, date or act.", "evidence": [evidence]}],
        }
        output = self.root / "research-preview"
        audit = preview.render_preview(plate_path=self.plate, spine=self.spine, out_dir=output,
                                       browser_source=BROWSER, catalogue=catalogue)
        svg = ET.parse(output / "latin-missal-preview.svg").getroot()
        links = svg.findall('.//s:path[@data-relationship]', NS)
        self.assertEqual([link.get("data-relationship") for link in links], ["constructed-relationship"])
        marks = {m.get("data-station") for m in svg.findall('.//s:g[@data-station]', NS)}
        self.assertNotIn("undated-donor", marks)
        self.assertNotIn("candidate-book", marks)
        words = " ".join(svg.itertext())
        self.assertIn("Context entity; no dated witness plotted", words)
        self.assertIn("A candidate book", words)
        self.assertIn("Source record; text not assessed", words)
        self.assertIn("not the lifespan", words.lower())
        self.assertIn("#family=group%3Atest-group", words)
        self.assertEqual(audit["station_count"], self.audit["station_count"])
        self.assertEqual(audit["edge_count"], self.audit["edge_count"])
        self.assertEqual(audit["research_relationship_count"], 1)
        self.assertGreater(audit["network_pages"], 0)
        network_ids = [identifier for node in svg.findall('.//s:g[@data-network-group]', NS)
                       for identifier in node.get("data-within-relationships", "").split()]
        network_ids += [identifier for edge in svg.findall('.//s:path[@data-network-bundle]', NS)
                        for identifier in edge.get("data-relationship-ids").split()]
        self.assertEqual(network_ids, ["constructed-relationship"])
        self.assertIn("Constructed group · within-group assertion", words)
        appendix = " ".join(" ".join(ET.parse(p).getroot().itertext())
                            for p in (output / "latin-missal-preview-parts").glob("relationships-*.svg"))
        self.assertIn("Constructed research citation", appendix)
        self.assertIn("Does not establish an edition, date or act.", appendix)
        self.assertIn("The exact donor witness remains unidentified.", appendix)
        self.assertIn("E01", appendix)

    def test_branch_route_does_not_pass_through_an_unrelated_station(self):
        geometry = preview.browser_geometry(self.spine, BROWSER)
        for panel in geometry["panels"]:
            for edge in panel["edges"]:
                points = [(float(x), float(y)) for x, y in re.findall(r"[ML] ([\d.]+) ([\d.]+)", edge["path"])]
                for node in panel["nodes"]:
                    if node["id"] in (edge["from"], edge["to"]):
                        continue
                    for (ax, ay), (bx, by) in zip(points, points[1:]):
                        nx, ny = node["x"], node["y"]
                        on_segment = (min(ax, bx) <= nx <= max(ax, bx) and min(ay, by) <= ny <= max(ay, by)
                                      and abs((nx - ax) * (by - ay) - (ny - ay) * (bx - ax)) < .001)
                        self.assertFalse(on_segment, f"{edge['from']} → {edge['to']} falsely touches {node['id']}")

    def test_missing_isolated_station_is_a_refusal_not_a_smaller_map(self):
        changed = copy.deepcopy(self.spine)
        changed["stations"] = [s for s in changed["stations"] if s["id"] != "lugdunense-1503"]
        with self.assertRaisesRegex(preview.PreviewError, "same stations and parent links"):
            preview.render_preview(plate_path=self.plate, spine=changed,
                                   out_dir=self.root / "bad", browser_source=BROWSER)
        self.assertFalse((self.root / "bad").exists())

    def test_browser_extraction_contract_change_refuses(self):
        changed = self.root / "changed-browser.js"
        changed.write_text(BROWSER.read_text().replace("  function connector(from, to) {",
                                                      "  function connectorRenamed(from, to) {"))
        with self.assertRaisesRegex(preview.PreviewError, "extraction contract changed"):
            preview.browser_geometry(self.spine, changed)

    def test_stale_station_metadata_is_refused(self):
        changed = copy.deepcopy(self.spine)
        changed["stations"][0]["date"] = "1490"
        with self.assertRaisesRegex(preview.PreviewError, "station metadata disagree"):
            preview.render_preview(plate_path=self.plate, spine=changed,
                                   out_dir=self.root / "stale", browser_source=BROWSER)

    def test_same_inputs_repeat_the_same_svg(self):
        output = self.root / "repeat"
        preview.render_preview(plate_path=self.plate, spine=self.spine,
                               out_dir=output, browser_source=BROWSER)
        self.assertEqual((output / "latin-missal-preview.svg").read_bytes(),
                         (self.output / "latin-missal-preview.svg").read_bytes())

    def test_declared_reception_gets_band_ring_and_evidence(self):
        source = self.root / "constructed.toml"
        source.write_text(reception.HOLY_WEEK.read_text() + reception.FIXTURE.format(
            receiving=reception.RECEIVING, parents=json.dumps(["vernacular-first-1965", reception.RECEIVED]),
            act_citation="cited-externally", extra="", receptions=reception.RECEPTION.format(
                source=reception.RECEIVED, kind="translates-typical-edition")))
        data = self.tool.load(source)
        plate = Path(self.tool.plate(data, self.root / "fixture-plate")["written"])
        spine = json.loads(Path(self.tool.structure(data, self.root / "fixture-data")["written"]).read_text())
        output = self.root / "reception-preview"
        audit = preview.render_preview(plate_path=plate, spine=spine, out_dir=output, browser_source=BROWSER)
        svg = ET.parse(output / "roman-holy-week-preview.svg").getroot()
        received = svg.findall('.//s:path[@data-reception="true"]', NS)
        self.assertEqual([(p.get("data-from"), p.get("data-to")) for p in received],
                         [(reception.RECEIVED, reception.RECEIVING)])
        self.assertEqual(len(svg.findall('.//s:circle[@data-interchange="true"]', NS)), 1)
        ordinary = svg.find('.//s:path[@data-from="vernacular-first-1965"]', NS)
        self.assertEqual(ordinary.get("data-reception"), "false")
        self.assertNotEqual(ordinary.get("stroke-width"), received[0].get("stroke-width"))
        pages = output / "roman-holy-week-preview-parts"
        evidence = " ".join(" ".join(ET.parse(p).getroot().itertext()) for p in pages.glob("catalogue-*.svg"))
        self.assertIn("A constructed decree of the receiving conference", evidence)
        self.assertIn("which is not a source", evidence)
        self.assertEqual(audit["reception_count"], 1)

    def test_stage_appendix_preserves_change_evidence_and_unpositioned_limits(self):
        history = stage_fixture()
        parts = self.root / "stage-evidence"
        parts.mkdir()
        paths = preview._stage_evidence(history, parts, "fixture", {"state-a": ["H001"]},
                                        "https://example.org/history?view=catalogue")
        words = " ".join(" ".join(ET.parse(path).getroot().itertext()) for path in paths)
        for phrase in ("One bow before the prayer.", "A second bow after the prayer.",
                       "constructed pages 1–2", "primary-description", "Source-described, not text-collated.",
                       "Historical parentage: established", "No Git ancestry or automatic text inheritance.",
                       "No dated position is asserted.", "Status: provisional", "Text coverage: not-transcribed",
                       "1590–1610 (not a duration of use)", "No connector is drawn across this gap.",
                       "S001", "T001", "C001", "G001", "https://example.org/constructed"):
            self.assertIn(phrase, words)
        self.assertNotIn("text-collated revision", words)

    def test_stage_evidence_missing_source_is_refused(self):
        history = stage_fixture()
        history["sources"] = []
        with self.assertRaisesRegex(preview.PreviewError, "missing source"):
            preview._stage_evidence(history, self.root, "fixture", {}, "")

    def test_stage_keys_stay_in_source_order_and_dates_do_not_become_durations(self):
        history = stage_fixture()
        history["stages"].reverse()
        keys = preview._stage_keys(history)
        self.assertEqual(keys["stages"]["state-lead"], "S001")
        self.assertEqual(keys["stages"]["state-a"], "S005")
        options = preview._stage_requests(history)[0]
        self.assertEqual(options["tradition"], "fixture-tradition")
        self.assertLess(options["start"], 1500)
        self.assertGreater(options["end"], 1650)

    def test_chronology_is_default_and_draws_only_recorded_transitions(self):
        history = stage_fixture()
        output = self.root / "chronology-preview"
        audit = preview.render_preview(plate_path=self.plate, spine=self.spine, out_dir=output,
                                       browser_source=BROWSER, catalogue={"stage_history": history})
        svg = ET.parse(output / "latin-missal-preview.svg").getroot()
        self.assertEqual(audit["presentation"], "chronological-book-stages")
        self.assertFalse(svg.findall('.//s:g[@data-network-group]', NS))
        self.assertFalse(svg.findall('.//s:g[@data-station]', NS))
        marks = svg.findall('.//s:g[@data-stage]', NS)
        self.assertEqual({mark.get("data-stage") for mark in marks},
                         {row["id"] for row in history["stages"] if row["start_year"] is not None})
        for mark in marks:
            circle = mark.find('s:circle', NS)
            key_label = next(node for node in mark.findall('s:text', NS)
                             if node.text == mark.get("data-stage-key"))
            self.assertGreaterEqual(abs(float(key_label.get("x")) - float(circle.get("cx"))), 14)
        unpositioned = svg.findall('.//s:g[@data-unpositioned-stage]', NS)
        self.assertEqual([mark.get("data-unpositioned-stage") for mark in unpositioned], ["state-undated"])
        transitions = svg.findall('.//s:path[@data-transition]', NS)
        self.assertEqual([edge.get("data-transition") for edge in transitions], ["change-ab"])
        self.assertEqual(len(svg.findall('.//s:path[@data-date-bounds="uncertainty-not-duration"]', NS)), 1)
        words = " ".join(svg.itertext())
        for phrase in ("years increase left to right", "The rubric adds a second bow after", "Provisional lead",
                       "not duration of use", "not-transcribed", "primary description"):
            self.assertIn(phrase, words)
        details = svg.findall('.//s:g[@data-change-detail="change-ab"]', NS)
        self.assertEqual(len(details), 1)
        local_change = " ".join(details[0].itertext())
        for phrase in ("Before: One bow before the prayer.", "After: A second bow after the prayer.",
                       "C001", "first rubric"):
            self.assertIn(phrase, local_change)
        self.assertEqual(len(svg.findall('.//s:g[@data-stage-scope]', NS)), len(marks))
        geometry = json.loads((output / "latin-missal-preview-parts/browser-geometry.json").read_text())
        first_sheet = ET.parse(output / "latin-missal-preview-parts/chronology-001.svg").getroot()
        self.assertIn("Traditions and dated sheets", " ".join(first_sheet.itertext()))
        for path in (output / "latin-missal-preview-parts").glob("chronology-*.svg"):
            page = ET.parse(path).getroot()
            if page.findall('.//s:g[@data-stage]', NS):
                self.assertEqual(page.get("width"), "420mm")
                self.assertIn(page.get("height"), ("297mm", "594mm"))
        model = geometry["chronology"][0]
        by_id = {node["id"]: node for lane in model["lanes"] for node in lane["nodes"]}
        self.assertEqual(by_id["state-b"]["changeLines"], [])
        self.assertTrue(by_id["state-b"]["fullChangeLines"])
        unit = (model["axis"]["x1"] - model["axis"]["x0"]) / (model["end"] - model["start"])
        self.assertAlmostEqual(by_id["state-b"]["x"] - by_id["state-a"]["x"], 50 * unit)
        self.assertAlmostEqual(by_id["state-c"]["xEnd"] - by_id["state-c"]["xStart"], 20 * unit)
        self.assertEqual(audit["stage_count"], 5)
        self.assertEqual(audit["documented_stages"], 4)
        self.assertEqual(audit["provisional_stages"], 1)

    def test_arabic_citations_keep_adjacent_latin_dates_and_numeric_ranges(self):
        value = "C055 · عنوان عربي 2014–2020 / English title (27 August 2025)"
        node = preview.text(ET.Element("g"), 0, 0, value)
        self.assertIn("\u2069 / English title (27 August 2025)", node.text)
        self.assertIn("\u20662014–2020\u2069", node.text)
        self.assertEqual(node.text.translate(dict.fromkeys(map(ord, "\u2066\u2067\u2069"))), value)

    def test_print_keeps_default_family_in_authored_recension_order(self):
        history = stage_fixture()
        history["traditions"] = [
            {"id": "other", "family": "Other"},
            {"id": "early", "family": "Primary"},
            {"id": "fixture-tradition", "family": "Primary"},
            {"id": "later", "family": "Primary"},
        ]
        history["default_tradition_id"] = "fixture-tradition"
        self.assertEqual([row["tradition"] for row in preview._stage_requests(history)],
                         ["early", "fixture-tradition", "later", "other"])

    def test_long_chronology_uses_windows_without_duplicating_uncertain_states(self):
        history = stage_fixture()
        early = copy.deepcopy(history["stages"][0])
        early.update(id="early", label="A genuinely early attestation", date_label="700–750",
                     start_year=700, end_year=750)
        history["stages"].insert(0, early)
        windows = preview._stage_requests(history, {"fixture-tradition"})
        self.assertGreater(len(windows), 1)
        geometry = preview.browser_geometry(self.spine, BROWSER, {"stage_history": history}, windows)
        nodes = [node for model in geometry["chronology"] for lane in model["lanes"] for node in lane["nodes"]]
        self.assertEqual(len(nodes), len({node["id"] for node in nodes}))
        uncertain = next(node for node in nodes if node["id"] == "state-c")
        self.assertFalse(uncertain["clippedStart"])
        self.assertFalse(uncertain["clippedEnd"])
        self.assertLess(windows[0]["end"], windows[1]["start"])


if __name__ == "__main__":
    unittest.main()
