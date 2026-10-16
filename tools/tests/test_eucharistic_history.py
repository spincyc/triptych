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


class RelationshipTests(unittest.TestCase):
    catalogue = EucharisticHistoryTests.catalogue
    emit = EucharisticHistoryTests.emit

    @classmethod
    def setUpClass(cls):
        cls.ventilator = staticmethod(owning_ventilator())

    def setUp(self):
        EucharisticHistoryTests.setUp(self)
        with (self.root / "research.toml").open("a") as output:
            output.write('''
[[records]]
id="later"
family="test-alias"
book_label="Later constructed witness"
date="1300"
chronology_start=1300
chronology_end=1300
chronology_kind="printed-witness"
chronology_certainty="stated"
''')
        with self.source.open("a") as output:
            output.write('''
[[relationship_sets]]
id="links"
path="relationships.toml"
''')
        self.relations = self.root / "relationships.toml"
        self.relations.write_text('''schema_version=1
record_type="eucharistic-history-relationships"
[[sources]]
id="inspected"
title="Constructed source, not historical evidence"
url="https://example.org/source"
inspection_status="inspected"
inspection="The bounded fixture paragraph was inspected."
[[relationships]]
id="bounded-claim"
kind="shared-text"
from="research:manuscript"
to="research:later"
certainty="sourced"
scope="One bounded fixture prayer."
basis="The constructed source identifies this shared prayer."
limitations="No direct borrowing or introduction date is established."
evidence=[{source_id="inspected",locus="Page 2, paragraph 3"}]
''')

    def test_typed_links_preserve_exact_endpoints_and_never_grant_inheritance(self):
        baseline = self.relations.read_text()
        for kind, directed in history.RELATIONSHIP_KINDS.items():
            with self.subTest(kind=kind):
                self.relations.write_text(baseline.replace('kind="shared-text"', f'kind="{kind}"'))
                payload = self.catalogue()
                relation = payload["relationships"][0]
                self.assertEqual(directed, relation["directed"])
                self.assertEqual("research:manuscript", relation["from"])
                self.assertEqual("research:later", relation["to"])
                self.assertFalse(relation["git_ancestry"])
                self.assertFalse(relation["text_inheritance"])
                self.assertEqual("Page 2, paragraph 3", relation["evidence"][0]["locus"])
                self.assertEqual("inspected", relation["evidence"][0]["source"]["inspection_status"])
                self.assertEqual(2, payload["counts"]["entries"])
                self.assertTrue(all(e["relationship_ids"] == ["links:bounded-claim"] for e in payload["entries"]))
        emitted = self.emit()
        for commit in emitted["branches"].values():
            self.assertEqual(b"\n", history.git(self.root / "corpus", "show", "-s", "--format=%P", commit))

    def test_relationship_date_is_not_inferred_from_witness_dates(self):
        relation = self.catalogue()["relationships"][0]
        self.assertIsNone(relation["chronology"])
        self.assertIsNone(relation["date_label"])
        with self.relations.open("a") as output:
            output.write('date_label="Uncertain interval, independently sourced"\nchronology={start=1200,end=1250,kind="relationship-bound",certainty="approximate"}\n')
        relation = self.catalogue()["relationships"][0]
        self.assertEqual(1250, relation["chronology"]["end"])
        self.assertEqual("Uncertain interval, independently sourced", relation["date_label"])

    def test_unresolved_records_and_unsupported_claims_fail_closed(self):
        baseline = self.relations.read_text()
        changes = [
            ('from="research:manuscript"', 'from="research:missing"'),
            ('to="research:later"', 'to="research:manuscript"'),
            ('kind="shared-text"', 'kind="similar-title"'),
            ('certainty="sourced"', 'certainty="certain-from-dates"'),
            ('source_id="inspected"', 'source_id="missing"'),
            ('locus="Page 2, paragraph 3"', 'locus=" "'),
            ('scope="One bounded fixture prayer."', 'scope=""'),
        ]
        for before, after in changes:
            with self.subTest(after=after):
                self.relations.write_text(baseline.replace(before, after))
                with self.assertRaises(history.HistoryError):
                    self.catalogue()
        for extra in ('git_ancestry=true', 'text_inheritance=true', 'parents=["research:manuscript"]',
                      'comparison_ids=["missing"]', 'chronology={start=1250,end=1200,kind="bound",certainty="approximate"}'):
            with self.subTest(extra=extra):
                self.relations.write_text(baseline + extra + "\n")
                with self.assertRaises(history.HistoryError):
                    self.catalogue()

    def test_url_is_not_source_inspection_and_uncertainty_is_retained(self):
        baseline = self.relations.read_text()
        self.relations.write_text(baseline.replace('inspection_status="inspected"', 'inspection_status="not-inspected"'))
        with self.assertRaisesRegex(history.HistoryError, "requires inspected evidence"):
            self.catalogue()
        self.relations.write_text(self.relations.read_text().replace('certainty="sourced"', 'certainty="unresolved"'))
        self.assertEqual("unresolved", self.catalogue()["relationships"][0]["certainty"])
        self.relations.write_text(baseline.replace('inspection="The bounded fixture paragraph was inspected."', 'inspection=" "'))
        with self.assertRaisesRegex(history.HistoryError, "inspection"):
            self.catalogue()

    def test_evidence_mutation_changes_projection_and_is_fingerprinted(self):
        before = self.catalogue()
        out = self.root / "catalogue.json"
        history.write_catalogue(before, out)
        self.relations.write_text(self.relations.read_text().replace("Page 2, paragraph 3", "Page 3, paragraph 1"))
        after = self.catalogue()
        self.assertNotEqual(before["inputs"], after["inputs"])
        with self.assertRaisesRegex(history.HistoryError, "differs"):
            history.write_catalogue(after, out, check=True)

    def test_alias_groups_preserve_family_and_expose_unmapped_groups(self):
        before = self.catalogue()
        self.assertEqual(2, before["counts"]["unmapped_families"])
        with self.source.open("a") as output:
            output.write('''
[[presentation_groups]]
id="named-tradition"
label="Named tradition"
families=["test-family","test-alias"]
''')
        after = self.catalogue()
        self.assertEqual(1, after["counts"]["presentation_groups"])
        self.assertEqual(0, after["counts"]["unmapped_families"])
        self.assertEqual(2, after["presentation_groups"][0]["count"])
        self.assertEqual({"test-family", "test-alias"}, {entry["family"] for entry in after["entries"]})
        self.assertTrue(all(entry["presentation_group"]["label"] == "Named tradition" for entry in after["entries"]))
        with self.source.open("a") as output:
            output.write('''
[[presentation_groups]]
id="overlapping"
label="Overlapping group"
families=["test-alias"]
''')
        with self.assertRaisesRegex(history.HistoryError, "two presentation groups"):
            self.catalogue()

    def test_contextual_donor_is_cited_undated_and_excluded_from_version_counts(self):
        self.relations.write_text(self.relations.read_text().replace('from="research:manuscript"', 'from="links:entity:donor"') + '''
[[entities]]
id="donor"
label="Named donor textual tradition"
kind="textual-tradition"
family="test-family"
scope="The prayer tradition only."
basis="The source names a tradition but no exact donor edition."
limitations="Exact exemplar unresolved."
evidence=[{source_id="inspected",locus="Page 2, paragraph 3"}]
''')
        payload = self.catalogue()
        self.assertEqual(2, payload["counts"]["entries"])
        self.assertEqual(1, payload["counts"]["relationship_entities"])
        entity = payload["relationship_entities"][0]
        self.assertIsNone(entity["chronology"])
        self.assertEqual(["links:bounded-claim"], entity["relationship_ids"])
        self.assertEqual(2, sum(group["count"] for group in payload["presentation_groups"]))
        self.assertEqual(1, sum(group["entity_count"] for group in payload["presentation_groups"]))
        with self.relations.open("a") as output:
            output.write('chronology={start=1000,end=1000,kind="invented",certainty="invented"}\n')
        with self.assertRaisesRegex(history.HistoryError, "undated textual-tradition"):
            self.catalogue()

    def test_duplicate_relationships_sources_and_aliases_are_refused(self):
        baseline = self.relations.read_text()
        relation = baseline[baseline.index("[[relationships]]"):]
        source = baseline[baseline.index("[[sources]]"):baseline.index("[[relationships]]")]
        for duplicate in (relation, source):
            self.relations.write_text(baseline + duplicate)
            with self.assertRaisesRegex(history.HistoryError, "duplicate"):
                self.catalogue()
        self.relations.write_text(baseline)
        with self.source.open("a") as output:
            output.write('\n[[presentation_groups]]\nid="group"\nlabel="Group"\nfamilies=["test-family","test-family"]\n')
        with self.assertRaisesRegex(history.HistoryError, "distinct nonempty aliases"):
            self.catalogue()

    def test_common_ancestry_reference_requires_separate_existing_record(self):
        with (self.root / "research.toml").open("a") as output:
            output.write('\n[[records]]\nid="earlier"\nbook_label="Earlier identified witness"\n')
        baseline = self.relations.read_text().replace('kind="shared-text"', 'kind="common-ancestry"')
        self.relations.write_text(baseline + 'ancestor_ref="research:earlier"\n')
        relation = self.catalogue()["relationships"][0]
        self.assertEqual("research:earlier", relation["ancestor_ref"])
        self.assertFalse(relation["directed"])
        self.assertFalse(relation["git_ancestry"])
        for ancestor in ("research:missing", "research:later"):
            self.relations.write_text(baseline + f'ancestor_ref="{ancestor}"\n')
            with self.assertRaisesRegex(history.HistoryError, "separate recorded common ancestor"):
                self.catalogue()
        self.relations.write_text(baseline.replace('kind="common-ancestry"', 'kind="borrowing"') + 'ancestor_ref="research:earlier"\n')
        with self.assertRaisesRegex(history.HistoryError, "separate recorded common ancestor"):
            self.catalogue()


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

    def test_comparison_record_binding_checks_actual_source_edition_not_target(self):
        research = self.root / "research.toml"
        research.write_text(research.read_text() + '\nsource_library_edition_id="edition.claimed"\n')
        self.source.write_text(self.source.read_text().replace(
            '[comparisons.left]\n', '[comparisons.left]\nrecord_id="research:manuscript"\n'))
        unit = self.payload["units"][0]
        unit.update(text_edition_id="edition.unrelated", target_edition_id="edition.claimed")
        with self.assertRaisesRegex(history.HistoryError, "text edition does not match"):
            self.compare()
        unit["text_edition_id"] = "edition.claimed"
        binding = self.compare()["left"]["record_binding"]
        self.assertEqual("checked-declared-identities", binding["status"])
        self.assertEqual(["source_library_edition_id"], binding["checked_fields"])
        del unit["text_edition_id"]
        with self.assertRaisesRegex(history.HistoryError, "text edition does not match"):
            self.compare()

    def test_same_edition_cannot_substitute_another_explicitly_bound_passage(self):
        research = self.root / "research.toml"
        research.write_text(research.read_text() + '''
source_library_edition_id="edition.anthology"
source_library_passage_ids=["passage.selected"]
source_library_checked_text_artifact_ids=["artifact.selected"]
''')
        self.source.write_text(self.source.read_text().replace(
            '[comparisons.right]\n', '[comparisons.right]\nrecord_id="research:manuscript"\n'))
        for unit in self.payload["units"]:
            unit.update(text_edition_id="edition.anthology", source_id="passage.selected",
                        source_artifact_id="artifact.selected")
        self.assertEqual(3, len(self.compare()["right"]["record_binding"]["checked_fields"]))
        self.payload["units"][1]["source_id"] = "passage.another-liturgy"
        with self.assertRaisesRegex(history.HistoryError, "member source_id does not match"):
            self.compare()
        self.payload["units"][1]["source_id"] = "passage.selected"
        self.payload["units"][1]["source_artifact_id"] = "artifact.another-liturgy"
        with self.assertRaisesRegex(history.HistoryError, "member source_artifact_id does not match"):
            self.compare()

    def test_unmapped_record_does_not_claim_canonical_witness_binding(self):
        self.source.write_text(self.source.read_text().replace(
            '[comparisons.left]\n', '[comparisons.left]\nrecord_id="research:manuscript"\n'))
        result = self.compare()
        self.assertEqual("unestablished-no-canonical-binding", result["left"]["record_binding"]["status"])
        self.assertEqual([], result["left"]["record_binding"]["checked_fields"])
        self.assertEqual("no-catalogue-record", result["right"]["record_binding"]["status"])

    def test_parallel_function_comparison_does_not_claim_same_composition(self):
        same = self.compare()
        self.assertEqual("same-prayer-witnesses", same["identity_claim"])
        self.source.write_text(self.source.read_text().replace(
            'kind="same-prayer-witness-comparison"', 'kind="parallel-liturgical-unit-comparison"'))
        parallel = self.compare()
        self.assertEqual("parallel-function-not-same-composition", parallel["identity_claim"])
        self.assertEqual(same["left"], parallel["left"])
        self.assertEqual(same["right"], parallel["right"])
        self.assertFalse(parallel["historical_ancestry_claimed"])
        catalogue = history.catalogue(self.source, self.root, act_loader=lambda path: {})
        self.assertEqual(parallel["identity_claim"], catalogue["comparisons"][0]["identity_claim"])
        self.payload["units"][0]["text_sha256"] = "0" * 64
        with self.assertRaisesRegex(history.HistoryError, "hash mismatch"):
            self.compare()

    def test_comparison_relationship_requires_matching_catalogue_members(self):
        with (self.root / "research.toml").open("a") as output:
            output.write('\n[[records]]\nid="second"\nbook_label="Second witness"\n')
        self.source.write_text(self.source.read_text().replace(
            '[comparisons.left]\n', '[comparisons.left]\nrecord_id="research:manuscript"\n').replace(
            '[comparisons.right]\n', '[comparisons.right]\nrecord_id="research:second"\n') + '''
[[relationship_sets]]
id="links"
path="relationships.toml"
''')
        relation_path = self.root / "relationships.toml"
        relation_path.write_text('''schema_version=1
record_type="eucharistic-history-relationships"
[[sources]]
id="source"
title="Constructed source"
inspection_status="inspected"
inspection="The exact fixture comparison was inspected."
[[relationships]]
id="sharing"
kind="shared-text"
from="research:manuscript"
to="research:second"
certainty="sourced"
scope="A bounded prayer."
basis="Constructed test alignment."
limitations="No ancestry or introduction date."
evidence=[{source_id="source",locus="Fixture paragraph"}]
comparison_ids=["constructed-pair"]
''')
        payload = self.compare()
        self.assertEqual(["links:sharing"], payload["relationship_ids"])
        self.assertEqual("research:manuscript", payload["left"]["record_id"])
        self.assertFalse(payload["relationships"][0]["directed"])
        self.assertIn("relationships.toml", {row["path"] for row in payload["inputs"]})
        catalogue = history.catalogue(self.source, self.root, act_loader=lambda path: {})
        self.assertEqual(["links:sharing"], catalogue["comparisons"][0]["relationship_ids"])
        self.assertEqual("comparisons/constructed-pair.json", catalogue["relationships"][0]["comparison_links"][0]["projection_path"])
        self.source.write_text(self.source.read_text().replace('record_id="research:second"', 'record_id="research:manuscript"'))
        with self.assertRaisesRegex(history.HistoryError, "endpoints do not match"):
            self.compare()
        self.source.write_text(self.source.read_text().replace('record_id="research:manuscript"', 'record_id="research:absent"'))
        with self.assertRaisesRegex(history.HistoryError, "unresolved .* record_id"):
            self.compare()

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
