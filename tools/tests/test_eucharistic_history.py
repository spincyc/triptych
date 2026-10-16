"""History discovery cannot admit text; text commits require exact owner evidence."""
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _eucharistic_history as history


def owning_ventilator():
    loader = importlib.machinery.SourceFileLoader("act_history_corpus_serialization_test", str(ROOT / "tools/act-history"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module.ventilate


class EucharisticHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ventilator = staticmethod(owning_ventilator())

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "routing.toml"
        self.source.write_text('''schema_version=1
record_type="catholic-eucharistic-history"
scope_ref="guidance/scope"
[[catalogues]]
id="research"
path="research.toml"
table="records"
[[text_sets]]
id="first-witness"
adapter="fixture"
[[text_sets]]
id="second-witness"
adapter="fixture"
''')
        (self.root / "research.toml").write_text('''[[sources]]
id="library"
url="https://example.org/catalogue"
inspection="catalogue metadata only"
[[records]]
id="manuscript"
family="test-family"
book_label="A manuscript witness"
date="circa 1200, perhaps later"
kind="manuscript-witness"
source_ids=["library"]
''')
        body = "Oratio prima.\n"
        (self.root / "witness.txt").write_text(body)
        self.payload = {"adapter_id": "fixture", "title": "Constructed fixture, not historical evidence",
                        "target_date": "1861", "witness_date": "1861", "reviewed_on": None,
                        "scope": {"whole_book_complete": False, "status": "partial"},
                        "counts": {"units": 1}, "sources": [],
                        "inputs": [history.fingerprint(self.root, self.root / "witness.txt")],
                        "units": [{"unit_id": "unit.fixture.collect", "text": body,
                                   "text_sha256": hashlib.sha256(body.encode()).hexdigest(),
                                   "division": "ordinary", "element_key": "collect", "source_order": 1,
                                   "publication": {"status": "permitted", "surfaces": ["public-git"]}}]}

    def emit(self, output="corpus"):
        return history.corpus(self.source, self.root, self.root / output,
                              ventilator=self.ventilator,
                              adapter_loader=lambda adapter, root: copy.deepcopy(self.payload),
                              supported_adapters=("fixture",))

    def catalogue(self):
        return history.catalogue(self.source, self.root, act_loader=lambda path: {})

    def test_candidate_has_no_invented_date_or_normative_acceptance(self):
        result = self.catalogue()
        entry = result["entries"][0]
        self.assertIsNone(entry["chronology"])
        self.assertEqual("circa 1200, perhaps later", entry["date_label"])
        self.assertEqual("candidate", entry["evidence_status"])
        self.assertEqual("unestablished", entry["substantive_status"])
        self.assertIsNone(entry["act_ref"])
        self.assertEqual("unestablished", entry["acquisition_status"])
        self.assertEqual("not-acquired", entry["text_status"])
        self.assertIn("Unknown acquisition", " ".join(result["limitations"]))

    def test_acquired_scan_is_not_transcribed_text(self):
        with (self.root / "research.toml").open("a") as output:
            output.write('acquisition_status="scan-acquired"\ntranscription_status="not-transcribed"\n')
        entry = self.catalogue()["entries"][0]
        self.assertEqual("scan-acquired", entry["acquisition_status"])
        self.assertEqual("not-transcribed", entry["text_status"])

    def test_explicit_bounds_survive_without_changing_date_claim(self):
        with (self.root / "research.toml").open("a") as output:
            output.write('[records.chronology]\nstart=1180\nend=1240\nkind="range"\ncertainty="estimated"\n')
        entry = self.catalogue()["entries"][0]
        self.assertEqual(1180, entry["chronology"]["start"])
        self.assertEqual("circa 1200, perhaps later", entry["date_label"])

    def test_broken_source_reference_is_refused(self):
        path = self.root / "research.toml"
        path.write_text(path.read_text().replace('source_ids=["library"]', 'source_ids=["missing"]'))
        with self.assertRaisesRegex(history.HistoryError, "unresolved source"):
            self.catalogue()

    def test_flat_research_bounds_are_explicit_not_parsed_dates(self):
        with (self.root / "research.toml").open("a") as output:
            output.write('chronology_start=1180\nchronology_end=1240\nchronology_kind="range"\nchronology_certainty="estimated"\n')
        self.assertEqual({"start": 1180, "end": 1240, "kind": "range", "certainty": "estimated"}, self.catalogue()["entries"][0]["chronology"])

    def test_catalogue_check_detects_drift_without_writing(self):
        target = self.root / "catalogue.json"
        history.write_catalogue(self.catalogue(), target)
        history.write_catalogue(self.catalogue(), target, check=True)
        target.write_text("stale")
        with self.assertRaisesRegex(history.HistoryError, "differs"):
            history.write_catalogue(self.catalogue(), target, check=True)
        self.assertEqual("stale", target.read_text())

    def test_exact_source_hash_mutation_denies_emission(self):
        (self.root / "witness.txt").write_text("different source")
        with self.assertRaisesRegex(history.HistoryError, "source hash mismatch"):
            self.emit()
        self.assertFalse((self.root / "corpus").exists())

    def test_publication_surface_denial_preserves_previous_output(self):
        before = self.emit()["branches"]
        self.payload["units"][0]["publication"]["surfaces"] = ["print"]
        with self.assertRaisesRegex(history.HistoryError, "not permitted"):
            self.emit()
        self.assertEqual(before["first-witness"], history.git(self.root / "corpus", "rev-parse", "refs/heads/reconstruction/first-witness").decode().strip())

    def test_unknown_adapter_is_not_executable_configuration(self):
        self.source.write_text(self.source.read_text().replace('adapter="fixture"', 'adapter="shell:curl"'))
        with self.assertRaisesRegex(history.HistoryError, "unknown text adapter"):
            self.emit()

    def test_roots_are_isolated_and_dates_truthfully_typed(self):
        result = self.emit()
        repo = self.root / "corpus"
        self.assertEqual(2, result["commits"])
        for commit in result["branches"].values():
            self.assertEqual("", history.git(repo, "show", "-s", "--format=%P", commit).decode().strip())
            message = history.git(repo, "show", "-s", "--format=%B", commit).decode()
            self.assertIn("Target-date: 1861", message)
            self.assertIn("Reconstruction-review-date: unestablished", message)
            self.assertIn("Git-date-role: synthetic-serialization", message)
            self.assertIn("Historical-act-claimed: no", message)
            self.assertEqual(b"946684800\n", history.git(repo, "show", "-s", "--format=%at", commit))
        history.git(repo, "fsck", "--strict")

    def test_deterministic_replay_and_owned_replacement(self):
        first = self.emit()
        second = self.emit("fresh")
        replaced = self.emit()
        self.assertEqual(first["branches"], second["branches"])
        self.assertEqual(first["branches"], replaced["branches"])

    def test_git_template_cannot_introduce_unconfigured_refs_or_hooks(self):
        first = self.emit("template")
        template = self.root / "template"
        history.git(template, "update-ref", "refs/heads/unconfigured", first["branches"]["first-witness"])
        (template / "hooks").mkdir()
        (template / "hooks" / "post-update").write_text("unconfigured hook")
        with mock.patch.dict(os.environ, {"GIT_TEMPLATE_DIR": str(template)}):
            result = self.emit()
        actual = history.git(self.root / "corpus", "for-each-ref", "--format=%(refname)").decode().splitlines()
        self.assertEqual(["refs/heads/reconstruction/first-witness", "refs/heads/reconstruction/second-witness"], actual)
        self.assertFalse((self.root / "corpus/hooks/post-update").exists())
        self.assertEqual(first["branches"], result["branches"])

    def test_unowned_directory_is_never_deleted(self):
        out = self.root / "corpus"
        out.mkdir()
        (out / "precious.txt").write_text("keep")
        with self.assertRaisesRegex(history.HistoryError, "ownership marker"):
            self.emit()
        self.assertEqual("keep", (out / "precious.txt").read_text())

    def test_configured_remote_blocks_replacement(self):
        self.emit()
        history.git(self.root / "corpus", "remote", "add", "origin", "https://example.org/repo.git")
        with self.assertRaisesRegex(history.HistoryError, "remote"):
            self.emit()

    def test_single_unit_edit_changes_only_its_text_and_evidence(self):
        unit = self.payload["units"][0]
        unit["text"] = "Prima oratio, integra; media oratio mutanda: ultima oratio integra. Amen."
        unit["text_sha256"] = history.digest(unit["text"].encode())
        first = self.emit()
        repo = self.root / "corpus"
        original = first["branches"]["first-witness"]
        # Keep both snapshots in one object store only for this synthetic diff;
        # no ancestry is inferred from the fixture's two recorded states.
        unit["text"] = unit["text"].replace("media oratio mutanda:", "media oratio emendata:")
        unit["text_sha256"] = history.digest(unit["text"].encode())
        second = self.emit("edited")
        history.git(repo, "fetch", str(self.root / "edited"), "refs/heads/reconstruction/first-witness")
        changed = history.git(repo, "diff", "--name-only", original, second["branches"]["first-witness"]).decode().splitlines()
        self.assertEqual(["provenance/ordinary/ordinary/collect.json", "text/ordinary/ordinary/collect.txt"], changed)
        text_path = "text/ordinary/ordinary/collect.txt"
        emitted = history.git(repo, "show", second["branches"]["first-witness"] + ":" + text_path)
        self.assertEqual(b"Prima oratio, integra;\nmedia oratio emendata:\nultima oratio integra.\nAmen.\n", emitted)
        self.assertEqual("1\t1\t" + text_path, history.git(repo, "diff", "--numstat", original, second["branches"]["first-witness"], "--", text_path).decode().strip())

    def test_whitespace_rewrap_preserves_serialized_text_and_source_hash_evidence(self):
        unit = self.payload["units"][0]
        unit["text"] = "Prima oratio, integra; media oratio: ultima oratio. Amen."
        unit["text_sha256"] = history.digest(unit["text"].encode())
        original_hash = unit["text_sha256"]
        first = self.emit()
        unit["text"] = "\n Prima\t oratio,  integra;\nmedia  oratio:\tultima\n oratio.\u00a0Amen. \n"
        unit["text_sha256"] = history.digest(unit["text"].encode())
        second = self.emit("rewrapped")
        repo = self.root / "corpus"
        history.git(repo, "fetch", str(self.root / "rewrapped"), "refs/heads/reconstruction/first-witness")
        before, after = first["branches"]["first-witness"], second["branches"]["first-witness"]
        self.assertEqual(b"", history.git(repo, "diff", "--name-only", before, after, "--", "text/"))
        path = "provenance/ordinary/ordinary/collect.json"
        previous = json.loads(history.git(repo, "show", before + ":" + path))
        current = json.loads(history.git(repo, "show", after + ":" + path))
        self.assertEqual(original_hash, previous["text_sha256"])
        self.assertEqual(unit["text_sha256"], current["text_sha256"])
        self.assertNotEqual(previous["text_sha256"], current["text_sha256"])
        self.assertEqual(previous["serialized_text_sha256"], current["serialized_text_sha256"])
        self.assertEqual(history.TEXT_SERIALIZATION, current["text_serialization"])
        body = history.git(repo, "show", after + ":text/ordinary/ordinary/collect.txt")
        self.assertEqual(history.digest(body), current["serialized_text_sha256"])

    def test_serialization_cannot_edit_punctuation_or_words(self):
        with self.assertRaisesRegex(history.HistoryError, "non-whitespace content"):
            history.corpus(self.source, self.root, self.root / "corpus",
                           ventilator=lambda text: [text.replace(".", ";")],
                           adapter_loader=lambda adapter, root: copy.deepcopy(self.payload),
                           supported_adapters=("fixture",))
        self.assertFalse((self.root / "corpus").exists())

    def test_repeated_proper_occurrences_have_distinct_readable_paths(self):
        unit = {"unit_id": "a", "identity": {"mass": "test-mass", "form": "", "course": "", "cycle": "", "proper": "Collect", "occurrence": 1}}
        first = history.text_path(unit)
        unit["identity"]["occurrence"] = 2
        self.assertNotEqual(first, history.text_path(unit))
        self.assertIn("test-mass", first)
        self.assertIn("Collect--1", first)
        unit["identity"]["occurrence"] = 1
        unit["identity"]["form"] = "@none"
        self.assertNotEqual(first, history.text_path(unit))
        self.assertIn("form-%40none", history.text_path(unit))

    def test_reserved_git_segments_are_escaped_without_identity_collisions(self):
        base = self.payload["units"][0]
        units = []
        expected = []
        for kind in ("ordinary", "proper"):
            for raw, encoded in ((".", "%2E"), ("..", "%2E%2E"),
                                 (".git", "%2Egit"), (".GiT", "%2EGiT"),
                                 ("%2E", "%252E"), ("%2Egit", "%252Egit")):
                unit = copy.deepcopy(base)
                unit["unit_id"] = f"unit.fixture.reserved-{len(units)}"
                if kind == "ordinary":
                    unit["division"] = raw
                    path = f"text/ordinary/{encoded}/collect.txt"
                else:
                    unit["identity"] = {"mass": raw, "form": "", "course": "", "cycle": "",
                                        "proper": "Collect", "occurrence": 1}
                    path = f"text/propers/{encoded}/form-@none/course-@none/cycle-@none/Collect--1.txt"
                self.assertEqual(path, history.text_path(unit))
                expected.append(path)
                units.append(unit)
        self.assertEqual(len(expected), len(set(expected)))
        self.payload["units"] = units
        self.payload["counts"]["units"] = len(units)
        result = self.emit()
        repo = self.root / "corpus"
        commit = result["branches"]["first-witness"]
        for path in expected:
            self.assertEqual(b"Oratio prima.\n", history.git(repo, "show", commit + ":" + path))
        history.git(repo, "fsck", "--strict")


class WitnessComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ventilator = staticmethod(owning_ventilator())

    def setUp(self):
        EucharisticHistoryTests.setUp(self)
        self.payload["sources"] = [{"id": "fixture.source", "title": "Constructed fixture source"}]
        second = copy.deepcopy(self.payload["units"][0])
        second.update({"unit_id": "unit.fixture.second", "element_key": "second", "source_order": 3,
                       "text": "Oratio secunda; tertia.\n"})
        second["text_sha256"] = history.digest(second["text"].encode())
        self.payload["units"].append(second)
        self.payload["counts"]["units"] = 2
        with self.source.open("a") as output:
            output.write('''
[[comparisons]]
id="constructed-pair"
kind="same-prayer-witness-comparison"
membership_status="established"
basis="Synthetic test alignment, not historical evidence."
apparatus_caveat="Do not infer an introduction date from this synthetic difference."
source_refs=["fixture.source"]
[comparisons.left]
text_set="first-witness"
unit_ids=["unit.fixture.collect"]
[comparisons.right]
text_set="second-witness"
unit_ids=["unit.fixture.collect","unit.fixture.second"]
''')

    def compare(self):
        return history.compare(self.source, self.root, "constructed-pair", ventilator=self.ventilator,
                               adapter_loader=lambda adapter, root: copy.deepcopy(self.payload),
                               supported_adapters=("fixture",))

    def test_ordered_group_preserves_members_hashes_paths_and_explicit_gap(self):
        original = copy.deepcopy(self.payload)
        result = self.compare()
        self.assertEqual(original, self.payload)
        members = result["right"]["members"]
        self.assertEqual([1, 3], [row["source_order"] for row in members])
        self.assertEqual([1, 2], [row["comparison_order"] for row in members])
        self.assertEqual(["unit.fixture.collect", "unit.fixture.second"], [row["unit_id"] for row in members])
        self.assertEqual(["text/ordinary/ordinary/collect.txt", "text/ordinary/ordinary/second.txt"], [row["text_path"] for row in members])
        for row in members:
            self.assertEqual(history.digest(row["source_text"].encode()), row["text_sha256"])
            self.assertEqual(history.digest(row["serialized_text"].encode()), row["serialized_text_sha256"])
        joined = "Oratio prima.\n Oratio secunda; tertia.\n"
        self.assertEqual(joined, result["right"]["joined_source_text"])
        self.assertEqual(history.digest(joined.encode()), result["right"]["joined_source_text_sha256"])
        self.assertEqual("Oratio prima.\nOratio secunda;\ntertia.\n", result["right"]["serialized_text"])
        self.assertIn("+Oratio secunda;\n+tertia.\n", result["unified_diff"])
        self.assertFalse(result["historical_ancestry_claimed"])
        self.assertFalse(result["historical_act_claimed"])
        self.assertFalse(result["introduction_date_inferred"])
        self.assertIn("introduction date", result["apparatus_caveat"])

    def test_comparison_json_is_deterministic(self):
        catalogue = history.catalogue(self.source, self.root, act_loader=lambda path: {})
        declaration = catalogue["comparisons"][0]
        self.assertEqual("comparisons/constructed-pair.json", declaration["projection_path"])
        self.assertEqual("configured-not-generated", declaration["status"])
        first = self.compare()
        self.assertEqual(history.json_bytes(first), history.json_bytes(self.compare()))
        out = self.root / "comparison.json"
        history.write_comparison(first, out)
        self.assertEqual(history.json_bytes(first), out.read_bytes())

    def test_missing_duplicate_or_reversed_membership_is_refused(self):
        original = self.source.read_text()
        for replacement, reason in [
            ('["unit.fixture.missing"]', "missing unit IDs"),
            ('["unit.fixture.collect","unit.fixture.collect"]', "distinct ordered"),
            ('["unit.fixture.second","unit.fixture.collect"]', "uncertain source order"),
        ]:
            with self.subTest(replacement=replacement):
                self.source.write_text(original.replace('["unit.fixture.collect","unit.fixture.second"]', replacement))
                with self.assertRaisesRegex(history.HistoryError, reason):
                    self.compare()

    def test_uncertain_membership_and_unsupported_kind_are_refused(self):
        original = self.source.read_text()
        for old, new, reason in [("membership_status=\"established\"", "membership_status=\"uncertain\"", "explicitly established"),
                                 ("kind=\"same-prayer-witness-comparison\"", "kind=\"historical-revision\"", "unsupported comparison kind")]:
            with self.subTest(new=new):
                self.source.write_text(original.replace(old, new))
                with self.assertRaisesRegex(history.HistoryError, reason):
                    self.compare()

    def test_cross_container_group_is_refused(self):
        self.payload["units"][1]["division"] = "another-prayer"
        with self.assertRaisesRegex(history.HistoryError, "uncertain source order or container"):
            self.compare()

    def test_source_or_text_hash_mutation_prevents_comparison(self):
        self.payload["units"][0]["text"] = "Changed without an updated source decision."
        with self.assertRaisesRegex(history.HistoryError, "text hash mismatch"):
            self.compare()
        self.payload["units"][0]["text"] = "Oratio prima.\n"
        (self.root / "witness.txt").write_text("Mutated source artifact")
        with self.assertRaisesRegex(history.HistoryError, "source hash mismatch"):
            self.compare()

    def test_unresolved_apparatus_source_and_denied_publication_are_refused(self):
        original = self.source.read_text()
        self.source.write_text(original.replace('source_refs=["fixture.source"]', 'source_refs=["not-checked"]'))
        with self.assertRaisesRegex(history.HistoryError, "not in its checked source owners"):
            self.compare()
        self.source.write_text(original)
        self.payload["units"][0]["publication"]["surfaces"] = []
        with self.assertRaisesRegex(history.HistoryError, "not permitted"):
            self.compare()


if __name__ == "__main__":
    unittest.main()
