"""Book-stage evidence stays scoped, reviewable and separate from text ancestry."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _eucharistic_history as history
import _eucharistic_stages as stages


def fixture():
    citation = {"source_id": "fixture.book", "locus": "p. 2", "claim": "The source identifies the two scoped states."}
    first = {"id": "fixture.first", "tradition_id": "fixture-tradition", "label": "Earlier bounded state",
             "date_label": "1200–1220 attestation", "start_year": 1200, "end_year": 1220,
             "date_kind": "attestation", "status": "documented", "scope": "The Ordinary rubric only.",
             "components": ["rubrics"], "witness_ids": ["research:first"], "witness_label": "First identified witness",
             "summary": "The earlier rubric in the identified witness.", "text_coverage": "not-transcribed",
             "evidence": [citation], "limitations": "No whole-book reconstruction.",
             "reception": "Community reception is not established by this fixture."}
    second = {**copy.deepcopy(first), "id": "fixture.second", "label": "Later bounded state",
              "start_year": 1210, "end_year": 1230, "date_label": "1210–1230 attestation",
              "witness_ids": ["research:second"], "witness_label": "Second identified witness"}
    change = {"component": "rubrics", "before": "Earlier prescribed action", "after": "Revised prescribed action",
              "locus_before": "first witness p. 1", "locus_after": "second witness p. 2", "evidence": [citation]}
    return {"schema_version": 1, "record_type": "eucharistic-book-stages", "dossier_id": "fixture",
            "title": "Constructed test dossier, not historical evidence",
            "traditions": [{"id": "fixture-tradition", "label": "Fixture tradition", "family": "fixture",
                            "scope": "One identified recension", "coverage_note": "Incomplete evidence."}],
            "sources": [{"id": "fixture.book", "title": "Fixture book", "url": "https://example.org/book",
                         "kind": "primary-book", "inspection": "Both named witness pages were inspected.",
                         "checked_on": "2026-10-16", "status": "inspected", "limitations": "Bounded excerpt only."}],
            "stages": [first, second],
            "transitions": [{"id": "fixture.revision", "from_stage": "fixture.first", "to_stage": "fixture.second",
                             "kind": "revision", "status": "documented", "evidence_level": "primary-description",
                             "summary": "The source describes a change in prescribed action.", "components": ["rubrics"],
                             "changes": [change], "evidence": [citation], "limitations": "No before/after transcription held.",
                             "comparison_ids": [], "historical_parentage": "attributed"}],
            "gaps": [{"id": "fixture-gap", "tradition_id": "fixture-tradition", "period": "After the later witness",
                      "missing": "Evidence of subsequent revision", "next_source": "The identified successor book",
                      "consequence": "No later stage is inferred."}]}


class EucharisticStagesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.directory = self.root / stages.DIRECTORY
        self.directory.mkdir(parents=True)
        self.path = self.directory / "fixture.json"
        self.data = fixture()

    def write(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

    def project(self, **kwargs):
        self.write()
        return stages.load(self.root, catalogue_ids={"research:first", "research:second"},
                           comparisons={"fixture-comparison": {"left": {"record_id": "research:first"},
                                                               "right": {"record_id": "research:second"}}},
                           fingerprint=history.fingerprint, **kwargs)

    def reject(self, pattern):
        with self.assertRaisesRegex(stages.StageError, pattern):
            self.project()

    def test_missing_directory_is_explicit_empty_research(self):
        self.directory.rmdir()
        result = stages.load(self.root, catalogue_ids=set(), comparisons={}, fingerprint=history.fingerprint)
        self.assertEqual(0, result["counts"]["stages"])
        self.assertEqual([], result["inputs"])
        self.assertIn("research gaps", " ".join(result["limitations"]))

    def test_source_description_preserves_bounds_order_and_no_inheritance(self):
        result = self.project()
        self.assertEqual(["fixture.first", "fixture.second"], [row["id"] for row in result["stages"]])
        self.assertEqual([1200, 1210], [row["start_year"] for row in result["stages"]])
        transition = result["transitions"][0]
        self.assertEqual("primary-description", transition["evidence_level"])
        self.assertEqual("attributed", transition["historical_parentage"])
        self.assertIs(False, transition["git_ancestry"])
        self.assertIs(False, transition["text_inheritance"])
        self.assertEqual(2, result["counts"]["documented_stages"])
        self.assertEqual(1, result["counts"]["documented_revisions"])
        self.assertEqual(0, result["counts"]["documented_witness_successions"])
        self.assertEqual("not-transcribed", result["stages"][0]["text_coverage"])
        self.assertEqual(history.fingerprint(self.root, self.path), result["inputs"][0])

    def test_null_bounds_remain_unpositioned(self):
        self.data["stages"][0].update(start_year=None, end_year=None)
        self.assertIsNone(self.project()["stages"][0]["start_year"])

    def test_invalid_dates_and_precision_are_refused(self):
        for start, end in ((None, 1200), (1220, 1200), (True, 1200), ("1200", 1200)):
            with self.subTest(start=start, end=end):
                self.data = fixture()
                self.data["stages"][0].update(start_year=start, end_year=end)
                self.reject("date bounds")
        self.data = fixture()
        self.data["sources"][0]["checked_on"] = "2026-02-30"
        self.reject("ISO date")

    def test_documented_does_not_accept_lead_only_sources(self):
        self.data["sources"][0]["status"] = "lead"
        self.reject("inspected sources")
        for row in self.data["stages"] + self.data["transitions"]:
            row["status"] = "provisional"
        result = self.project()
        self.assertEqual(0, result["counts"]["documented_stages"])
        self.assertEqual(2, result["counts"]["provisional_stages"])

    def test_documented_transition_cannot_promote_provisional_endpoint(self):
        self.data["stages"][0]["status"] = "provisional"
        self.reject("documented endpoints")

    def test_documented_progression_rejects_disjoint_reverse_dates(self):
        for kind in ("revision", "recension-branch", "reception", "witness-succession"):
            with self.subTest(kind=kind):
                self.data = fixture()
                self.data["stages"][0].update(start_year=1500, end_year=1500)
                self.data["transitions"][0]["kind"] = kind
                self.reject("fixture.revision.*reverses disjoint attestation date bounds")

    def test_progression_does_not_invent_order_from_uncertain_or_different_dates(self):
        for start, end, role in ((1225, 1250, "attestation"), (1230, 1230, "attestation"),
                                 (1500, 1500, "publication"), (None, None, "attestation")):
            with self.subTest(start=start, end=end, role=role):
                self.data = fixture()
                self.data["stages"][0].update(start_year=start, end_year=end, date_kind=role)
                self.assertEqual(1, self.project()["counts"]["documented_transitions"])
        self.data = fixture()
        self.data["stages"][0].update(start_year=1500, end_year=1500)
        self.data["transitions"][0]["status"] = "provisional"
        self.assertEqual(1, self.project()["counts"]["provisional_transitions"])

    def test_documented_progression_rejects_cycles_with_overlapping_dates(self):
        for kind in ("revision", "recension-branch", "reception", "witness-succession"):
            with self.subTest(kind=kind):
                self.data = fixture()
                reverse = copy.deepcopy(self.data["transitions"][0])
                reverse.update(id="fixture.reverse", from_stage="fixture.second",
                               to_stage="fixture.first", kind=kind)
                self.data["transitions"].append(reverse)
                self.reject("documented transition cycle")
                reverse["status"] = "provisional"
                self.assertEqual(1, self.project()["counts"]["documented_transitions"])

    def test_progression_requires_feasible_dates_across_overlapping_chain(self):
        self.data["stages"][0].update(start_year=1400, end_year=1500)
        self.data["stages"][1].update(start_year=1000, end_year=1450)
        third = copy.deepcopy(self.data["stages"][1])
        third.update(id="fixture.third", start_year=1100, end_year=1200)
        self.data["stages"].append(third)
        onward = copy.deepcopy(self.data["transitions"][0])
        onward.update(id="fixture.onward", from_stage="fixture.second", to_stage="fixture.third")
        self.data["transitions"].append(onward)

        # Each adjacent pair overlaps, but no dates satisfy first <= second <= third.
        self.reject("transition path.*attestation.*fixture.first.*fixture.third")
        third["end_year"] = 1400
        self.assertEqual(2, self.project()["counts"]["documented_transitions"])
        third["end_year"] = 1200
        self.data["stages"][1].update(start_year=None, end_year=None)
        self.reject("transition path.*attestation.*fixture.first.*fixture.third")
        self.data["stages"][1]["date_kind"] = "publication"
        self.assertEqual(2, self.project()["counts"]["documented_transitions"])
        self.data["stages"][1]["date_kind"] = "attestation"
        onward["status"] = "provisional"
        self.assertEqual(1, self.project()["counts"]["documented_transitions"])

    def test_parallel_claims_and_converging_sequences_are_not_cycles(self):
        third = copy.deepcopy(self.data["stages"][1])
        third.update(id="fixture.third", start_year=1230, end_year=1230)
        self.data["stages"].append(third)
        for identifier, origin, target in (("parallel", "first", "second"),
                                            ("direct", "first", "third"),
                                            ("onward", "second", "third")):
            edge = copy.deepcopy(self.data["transitions"][0])
            edge.update(id="fixture." + identifier, from_stage="fixture." + origin,
                        to_stage="fixture." + target)
            self.data["transitions"].append(edge)
        self.assertEqual(4, self.project()["counts"]["documented_transitions"])

    def test_complete_requires_separate_binding_contract(self):
        self.data["stages"][0]["text_coverage"] = "complete"
        self.reject("full-text binding and scope denominator")

    def test_duplicate_and_unprefixed_ids_are_refused(self):
        self.data["stages"][1]["id"] = self.data["stages"][0]["id"]
        self.reject("duplicate")
        self.data = fixture()
        self.data["sources"][0]["id"] = "unprefixed"
        self.reject("prefixed")

    def test_duplicate_json_keys_are_refused(self):
        self.path.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaisesRegex(stages.StageError, "duplicate JSON key"):
            stages.load(self.root, catalogue_ids=set(), comparisons={}, fingerprint=history.fingerprint)

    def test_references_must_resolve_exactly(self):
        mutations = [("stages", "tradition_id", "missing", "tradition_id"),
                     ("stages", "witness_ids", ["missing"], "witness_id"),
                     ("transitions", "to_stage", "missing", "to_stage"),
                     ("transitions", "comparison_ids", ["missing"], "comparison_id")]
        for table, field, value, pattern in mutations:
            with self.subTest(field=field):
                self.data = fixture()
                self.data[table][0][field] = value
                self.reject(pattern)
        self.data = fixture()
        self.data["stages"][0]["evidence"][0]["source_id"] = "missing"
        self.reject("unresolved evidence")

    def test_comparison_requires_exact_witnesses_in_either_orientation(self):
        self.data["transitions"][0]["comparison_ids"] = ["fixture-comparison"]
        self.assertEqual(["fixture-comparison"], self.project()["transitions"][0]["comparison_ids"])
        self.data["stages"][0]["witness_ids"] = ["research:second"]
        self.data["stages"][1]["witness_ids"] = ["research:first"]
        self.project()
        self.data["stages"][1]["witness_ids"] = []
        self.reject("exact stage witnesses")

    def test_default_tradition_is_source_owned_and_resolved(self):
        self.assertEqual("fixture-tradition", self.project()["default_tradition_id"])
        self.assertEqual("fixture-tradition", self.project(default_tradition_id="fixture-tradition")["default_tradition_id"])
        with self.assertRaisesRegex(stages.StageError, "default tradition"):
            self.project(default_tradition_id="nonexistent")

    def test_text_collated_requires_every_change_locus_and_book_evidence(self):
        transition = self.data["transitions"][0]
        transition["evidence_level"] = "text-collated"
        transition["changes"].append(copy.deepcopy(transition["changes"][0]))
        transition["changes"][1]["locus_after"] = ""
        self.reject("locus_after")
        transition["changes"][1]["locus_after"] = "p. 3"
        self.data["sources"].append({**self.data["sources"][0], "id": "fixture.scholar", "kind": "scholarship"})
        transition["changes"][1]["evidence"] = [{"source_id": "fixture.scholar", "locus": "p. 3", "claim": "A scholarly description only."}]
        self.reject("book or critical-edition")
        transition["evidence_level"] = "scholarly-description"
        self.assertEqual("scholarly-description", self.project()["transitions"][0]["evidence_level"])

    def test_bibliography_is_not_substantive_revision(self):
        transition = self.data["transitions"][0]
        transition["evidence_level"] = "bibliographic-only"
        self.reject("bibliography alone")
        transition.update(kind="witness-succession", changes=[])
        result = self.project()
        self.assertEqual(1, result["counts"]["documented_witness_successions"])
        self.assertEqual(0, result["counts"]["documented_revisions"])

    def test_catalogue_description_cannot_be_labelled_primary_evidence(self):
        self.data["sources"][0]["kind"] = "institutional-catalogue"
        self.reject("primary-description requires primary source evidence")
        self.data["transitions"][0]["evidence_level"] = "scholarly-description"
        self.assertEqual(1, self.project()["counts"]["documented_revisions"])
        self.data["transitions"][0]["evidence_level"] = "text-collated"
        self.reject("book or critical-edition")

    def test_each_primary_description_change_needs_primary_evidence(self):
        self.data["sources"].append({**self.data["sources"][0], "id": "fixture.catalogue",
                                     "kind": "institutional-catalogue"})
        self.data["transitions"][0]["changes"].append(copy.deepcopy(self.data["transitions"][0]["changes"][0]))
        self.data["transitions"][0]["changes"][1]["evidence"][0]["source_id"] = "fixture.catalogue"
        self.reject("primary-description change requires primary source evidence")

    def test_no_inheritance_permissions_or_undeclared_parents(self):
        for flag in ("git_ancestry", "text_inheritance"):
            with self.subTest(flag=flag):
                self.data = fixture()
                self.data["transitions"][0][flag] = True
                self.reject("cannot grant")
        self.data = fixture()
        self.data["transitions"][0]["parents"] = ["fixture.first"]
        self.reject("unsupported fields")

    def test_scoped_changes_cannot_escape_components(self):
        self.data["transitions"][0]["changes"][0]["component"] = "anaphoras"
        self.reject("outside declared scope")

    def test_documented_change_requires_both_endpoint_component_scopes(self):
        for index, endpoint in ((0, "from_stage"), (1, "to_stage")):
            with self.subTest(endpoint=endpoint):
                self.data = fixture()
                self.data["stages"][index]["components"] = ["ordinary"]
                self.reject("outside " + endpoint + " component scope")
        self.data["transitions"][0]["status"] = "provisional"
        self.assertEqual(0, self.project()["counts"]["documented_transitions"])
        self.data = fixture()
        self.data["transitions"][0]["changes"][0]["before"] = "Explicitly attested absence within the examined rubric scope"
        self.assertEqual(1, self.project()["counts"]["documented_transitions"])

    def test_sources_need_inspection_and_safe_urls(self):
        self.data["sources"][0]["inspection"] = ""
        self.reject("inspection")
        self.data = fixture()
        self.data["sources"][0]["url"] = "javascript:alert(1)"
        self.reject("HTTP")

    def test_cross_dossier_refs_resolve_after_all_files(self):
        other = copy.deepcopy(self.data)
        other.update(dossier_id="other", title="A source owner")
        source = other["sources"][0]
        source["id"] = "other.book"
        for table in ("traditions", "stages", "transitions", "gaps"):
            other[table] = []
        self.data["sources"] = []
        for row in self.data["stages"] + self.data["transitions"]:
            for item in row["evidence"]:
                item["source_id"] = "other.book"
        for change in self.data["transitions"][0]["changes"]:
            for item in change["evidence"]:
                item["source_id"] = "other.book"
        (self.directory / "zzz-other.json").write_text(json.dumps(other))
        self.assertEqual(2, self.project()["counts"]["dossiers"])

    def test_changed_input_during_load_is_refused(self):
        self.write()
        calls = 0
        def changing_fingerprint(root, path):
            nonlocal calls
            calls += 1
            if calls == 2:
                path.write_text(path.read_text() + "\n")
            return history.fingerprint(root, path)
        with self.assertRaisesRegex(stages.StageError, "stage input changed"):
            stages.load(self.root, catalogue_ids={"research:first", "research:second"},
                        comparisons={}, fingerprint=changing_fingerprint)

    def test_symlink_dossier_cannot_extend_input_ownership(self):
        self.write()
        (self.directory / "alias.json").symlink_to(self.path)
        with self.assertRaisesRegex(stages.StageError, "regular repository files"):
            stages.load(self.root, catalogue_ids=set(), comparisons={}, fingerprint=history.fingerprint)

    def test_catalogue_input_closure_and_staleness_include_dossiers(self):
        self.write()
        source = self.root / "routing.toml"
        source.write_text('schema_version=1\nrecord_type="catholic-eucharistic-history"\nscope_ref="scope"\n'
                          '[[catalogues]]\nid="research"\npath="research.toml"\ntable="records"\n')
        (self.root / "research.toml").write_text('[[records]]\nid="first"\n[[records]]\nid="second"\n')
        result = history.catalogue(source, self.root, act_loader=lambda path: {})
        self.assertIn(history.fingerprint(self.root, self.path), result["inputs"])
        self.assertEqual(2, result["stage_history"]["counts"]["stages"])
        target = self.root / "catalogue.json"
        history.write_catalogue(result, target)
        self.data["gaps"][0]["next_source"] = "A more precise source locator"
        self.write()
        current = history.catalogue(source, self.root, act_loader=lambda path: {})
        with self.assertRaisesRegex(history.HistoryError, "projection differs"):
            history.write_catalogue(current, target, check=True)

    def test_linked_comparison_fingerprints_and_rechecks_stage_evidence(self):
        self.data["transitions"][0]["comparison_ids"] = ["fixture-comparison"]
        self.write()
        source = self.root / "routing.toml"
        source.write_text('''schema_version=1
record_type="catholic-eucharistic-history"
scope_ref="scope"
[[catalogues]]
id="research"
path="research.toml"
table="records"
[[text_sets]]
id="fixture-text"
adapter="fixture"
[[comparisons]]
id="fixture-comparison"
kind="same-prayer-witness-comparison"
membership_status="established"
basis="Constructed test alignment"
apparatus_caveat="No historical inference from this test fixture"
source_refs=["fixture.book"]
[comparisons.left]
text_set="fixture-text"
unit_ids=["unit.fixture"]
record_id="research:first"
[comparisons.right]
text_set="fixture-text"
unit_ids=["unit.fixture"]
record_id="research:second"
''')
        (self.root / "research.toml").write_text('[[records]]\nid="first"\n[[records]]\nid="second"\n')
        witness = self.root / "body.txt"
        witness.write_text("Oratio.\n")
        payload = {"adapter_id": "fixture", "sources": [{"id": "fixture.book"}],
                   "inputs": [history.fingerprint(self.root, witness)],
                   "units": [{"unit_id": "unit.fixture", "text": "Oratio.\n", "text_sha256": history.digest(b"Oratio.\n"),
                              "source_order": 1, "division": "ordinary", "element_key": "oratio",
                              "publication": {"status": "permitted", "surfaces": ["public-git"]}}]}
        def compare(loader):
            return history.compare(source, self.root, "fixture-comparison", ventilator=lambda text: [text.strip()],
                                   adapter_loader=loader, supported_adapters=("fixture",), act_loader=lambda path: {})
        result = compare(lambda adapter, root: copy.deepcopy(payload))
        self.assertIn(history.fingerprint(self.root, self.path), result["inputs"])
        self.assertIn("scripts/_eucharistic_stages.py", [row["path"] for row in result["tool_inputs"]])
        self.assertFalse(result["historical_ancestry_claimed"])
        def changed(adapter, root):
            self.path.write_text(self.path.read_text() + "\n")
            return copy.deepcopy(payload)
        with self.assertRaisesRegex(history.HistoryError, "comparison input changed.*fixture.json"):
            compare(changed)
        self.write()
        def added(adapter, root):
            (self.directory / "new-dossier.json").write_text(json.dumps(fixture()))
            return copy.deepcopy(payload)
        with self.assertRaisesRegex(history.HistoryError, "stage dossier membership changed"):
            compare(added)


if __name__ == "__main__":
    unittest.main()
