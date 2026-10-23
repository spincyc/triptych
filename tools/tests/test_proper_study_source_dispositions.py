"""New research cannot lose checked witnesses between L2 holdings and L3 text.

The source library and Catena validators run over synthetic, hash-pinned source
records. No production research, admission, or review is performed here.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _catena
import _proper_study as study
from tools.tests import test_source_library as source_fixture
from tools.tests.test_catena import BOOK_INDEX

DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
SOURCE_LIBRARY = source_fixture.SOURCE_LIBRARY
WORK_ID, EDITION_ID = source_fixture.WORK_ID, source_fixture.EDITION_ID
ARTIFACT_ID, PASSAGE_ID = source_fixture.ARTIFACT_ID, source_fixture.PASSAGE_ID
EXTENT = {"token": "Gen", "first_chapter": 1, "first_verse": 3,
          "last_chapter": 1, "last_verse": 5}


class SourceDispositionTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/resume-weekly-workflow-fix/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="source-dispositions-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.addCleanup(_catena._SOURCES_CACHE.pop, self.root, None)
        self.environment = patch.dict(os.environ, {"TRIPTYCH_LIBRARY_CACHE": "0"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        fixture = source_fixture.SourceLibraryTests()
        fixture.root = self.root
        fixture.add_valid_vertical_fixture()
        self.write = fixture.write
        # The source fixture's original consumer is unrelated to this proper.
        (self.root / "src/gpt/theology/demo/research/source-bindings.toml").unlink()
        self.leaf = self.root / "src/gpt" / DOCUMENT
        self.write(f"src/gpt/{DOCUMENT}/main.tex", "% Synthetic source owner.\n")
        for name in ("context.md", "scope.md", "interpretations.md", "chronology.toml",
                     "chronology-annotations.tex"):
            self.write(f"src/gpt/{DOCUMENT}/research/{name}", "Synthetic checked research.\n")
        self.write(f"src/gpt/{DOCUMENT}/research/review-dependencies.toml", "paths = []\n")
        self.binding_path = self.leaf / "research/source-bindings.toml"
        self.work = next(self.root.glob("src/sources/works/augustine/*/work.toml"))
        self.edition = next(self.root.glob("src/sources/works/augustine/*/editions/*/edition.toml"))
        self.artifact = next(self.root.glob("src/sources/works/augustine/*/editions/*/artifacts/*/artifact.toml"))
        self.passage = next(self.root.glob("src/sources/works/augustine/*/editions/*/passages/*.toml"))
        self.canonical_fixture()
        self.bindings = [{"source_id": ARTIFACT_ID, "role": "reception",
                          "states": ["inspected"], "loci": ["book-10.chapter-6"],
                          "context": "The complete synthetic chapter was inspected."}]
        self.pin_bindings()
        self.rows = [{"id": "augustine-sacrifice", "binding_index": 1,
                      "binding_sha256": study.binding_digest(self.bindings[0]),
                      "source_id": ARTIFACT_ID,
                      "source_fingerprint": self.bindings[0]["source_fingerprint"],
                      "locus": "book-10.chapter-6; chapter and adjacent context read",
                      "relationship": "direct-exegesis", "disposition": "deferred",
                      "reason": "The source is held; its natural excerpt boundary still needs checking.",
                      "missing_criteria": ["natural-excerpt-boundary"],
                      "scripture_extents": [copy.deepcopy(EXTENT)]}]
        self.save_rows()
        self.assertEqual(SOURCE_LIBRARY.load_library(self.root).errors, [])

    def canonical_fixture(self):
        """An actual registered index plus one synthetic canonical chapter."""
        prefix = "src/sources/works/catholic-church/vulgata-clementina"
        self.write(f"{prefix}/work.toml", '''schema=1
record_type="work"
id="work.catholic-church.vulgata-clementina"
title="Synthetic canonical index"
responsible="Synthetic fixture"
work_type="bible"
languages=["la"]
''')
        self.write(f"{prefix}/editions/fixture/edition.toml", '''schema=1
record_type="edition"
id="edition.catholic-church.vulgata-clementina.fixture"
work_id="work.catholic-church.vulgata-clementina"
title="Synthetic canonical index"
language="la"
publication="Synthetic test only"
''')
        target = f"{prefix}/editions/fixture/artifacts/book-index-fixture/book-index.tsv"
        self.write(target, BOOK_INDEX)
        self.write(f"{prefix}/editions/fixture/artifacts/book-index-fixture/artifact.toml", f'''schema=1
record_type="artifact"
id="artifact.catholic-church.vulgata-clementina.fixture.book-index"
edition_id="edition.catholic-church.vulgata-clementina.fixture"
artifact_type="book-index"
media_type="text/tab-separated-values"
storage="tracked"
rights_status="project-created"
rights_basis="Synthetic test data."
sha256="{hashlib.sha256(BOOK_INDEX.encode()).hexdigest()}"
byte_size={len(BOOK_INDEX.encode())}
retrieved="2026-07-22"
provenance="Synthetic test fixture."
path="{target}"
''')
        self.write("src/sources/bibles/clementine-vulgate/chapters/Gen/1.json",
                   json.dumps({"book": "Gen", "chapter": 1,
                               "verses": {str(n): "Synthetic verse" for n in range(1, 32)}}))
        self.write("src/sources/commentary/work-aliases.yaml", yaml.safe_dump({
            "schema": "triptych-commentary-work-aliases/v1",
            "groups": [{"author": "Augustine of Hippo", "work": "De civitate Dei",
                        "titles": ["de civitate dei", "the city of god"]}]}))

    def save_rows(self):
        data = {"schema": 1, "contract": study.SOURCE_DISPOSITIONS_SCHEMA,
                "document": DOCUMENT, "numbering": "vulgate", "sources": self.rows}
        self.write_toml(self.leaf / study.SOURCE_DISPOSITIONS, data, "sources")

    @staticmethod
    def write_toml(path, data, array):
        # JSON strings and inline dictionaries use the same scalar syntax here.
        def value(item):
            if isinstance(item, dict):
                return "{ " + ", ".join(key + " = " + value(val) for key, val in item.items()) + " }"
            if isinstance(item, list):
                return "[" + ", ".join(value(val) for val in item) + "]"
            return json.dumps(item)
        rows = data[array]
        text = "\n".join(f"{key} = {value(val)}" for key, val in data.items() if key != array)
        if not rows:
            text += f"\n{array} = []\n"
        for row in rows:
            text += f"\n\n[[{array}]]\n" + "\n".join(f"{key} = {value(val)}" for key, val in row.items())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")

    def pin_bindings(self):
        library = SOURCE_LIBRARY.load_library(self.root, check_binding_fingerprints=False)
        for binding in self.bindings:
            if set(binding["states"]) & {"acquired", "searched", "inspected", "verified"}:
                binding["source_fingerprint"] = SOURCE_LIBRARY.source_fingerprint(library, binding["source_id"])
            else:
                binding.pop("source_fingerprint", None)
        self.write_toml(self.binding_path, {"schema": 1, "record_type": "bindings",
                                          "document": DOCUMENT, "bindings": self.bindings}, "bindings")
        if hasattr(self, "rows"):
            for row in self.rows:
                binding = self.bindings[row["binding_index"] - 1]
                row["binding_sha256"] = study.binding_digest(binding)
                pin = binding.get("source_fingerprint")
                if pin:
                    row["source_fingerprint"] = pin
                else:
                    row.pop("source_fingerprint", None)

    def check(self):
        self.save_rows()
        return study.source_dispositions(self.root, "gpt", DOCUMENT)

    def admit(self):
        self.rows[0].update(disposition="admitted", passage_ids=[PASSAGE_ID],
                            reason="The exact passage and its natural Scripture edge were checked.")
        for name in ("scripture_extents", "missing_criteria"):
            self.rows[0].pop(name)

    def map_passage(self, **overrides):
        fragment = {"passage_id": PASSAGE_ID, "work_id": WORK_ID,
                    "work_alias": {"author": "Augustine of Hippo", "work": "De civitate Dei"},
                    "text_date": 417, "text_date_basis": "Synthetic fixture date only.",
                    "numbering": "vulgate", "extent": copy.deepcopy(EXTENT),
                    "basis": "The synthetic checked paragraph explains these verses."}
        fragment.update(overrides)
        return self.write("src/sources/commentary/fragment-loci.yaml", yaml.safe_dump({
            "schema": _catena.SCHEMA, "updated": "2026-07-22", "numbering": "vulgate",
            "fragments": [fragment]}))

    def test_missing_handoff_fails_even_with_valid_checked_bindings(self):
        (self.leaf / study.SOURCE_DISPOSITIONS).unlink()
        with self.assertRaisesRegex(ValueError, "missing reusable-source handoff"):
            study.source_dispositions(self.root, "gpt", DOCUMENT)

    def test_checked_witness_cannot_disappear_from_handoff(self):
        self.rows = []
        with self.assertRaisesRegex(ValueError, "omits source bindings.*1"):
            self.check()

    def test_used_catalog_only_witness_is_refused(self):
        for source_id in (WORK_ID, EDITION_ID):
            with self.subTest(source_id=source_id):
                self.bindings[0].update(source_id=source_id, states=["cataloged"])
                self.rows[0]["source_id"] = source_id
                self.pin_bindings()
                with self.assertRaisesRegex(ValueError, "used evidence requires an exact hashed"):
                    self.check()

    def test_catalog_only_bibliography_is_allowed_as_an_explicit_uninspected_lead(self):
        self.bindings[0].update(source_id=WORK_ID, role="lead", states=["cataloged"])
        self.rows[0].update(source_id=WORK_ID, disposition="lead", relationship="lead",
                            reason="Uninspected bibliography; no publication claim uses this lead.")
        for name in ("scripture_extents", "missing_criteria"):
            self.rows[0].pop(name)
        self.pin_bindings()
        self.check()
        self.bindings[0]["role"] = "direct-witness"
        self.pin_bindings()
        with self.assertRaisesRegex(ValueError, "catalog-only lead binding"):
            self.check()

    def test_a_checked_holding_may_be_deferred_without_creating_any_fragment(self):
        self.rows[0]["relationship"] = "analogue"
        paths = self.check()
        self.assertIn(self.artifact, paths)
        self.assertFalse((self.root / "src/sources/commentary/fragment-loci.yaml").exists())
        self.assertEqual(self.rows[0]["scripture_extents"], [EXTENT])

    def test_deferral_requires_specific_remaining_criteria_and_source_extent(self):
        self.rows[0]["missing_criteria"] = []
        with self.assertRaisesRegex(ValueError, "concrete missing_criteria"):
            self.check()
        self.rows[0]["missing_criteria"] = ["natural-excerpt-boundary"]
        self.rows[0]["scripture_extents"] = []
        with self.assertRaisesRegex(ValueError, "scripture-extent explicitly unresolved"):
            self.check()
        self.rows[0]["missing_criteria"].append("scripture-extent")
        self.check()

    def test_deferred_extent_uses_owning_canonical_bounds_check(self):
        self.rows[0]["scripture_extents"][0]["last_verse"] = 99
        with self.assertRaisesRegex(ValueError, "past the canonical last verse"):
            self.check()

    def test_stable_row_identity_and_original_binding_pin_are_required(self):
        self.rows.append(copy.deepcopy(self.rows[0]))
        with self.assertRaisesRegex(ValueError, "unique stable"):
            self.check()
        self.rows.pop()
        self.rows[0]["source_fingerprint"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "reviewed binding source_fingerprint"):
            self.check()

    def test_row_cannot_follow_a_reordered_or_replaced_binding_silently(self):
        self.rows[0]["source_id"] = PASSAGE_ID
        with self.assertRaisesRegex(ValueError, "source_id disagrees"):
            self.check()

    def test_same_artifact_bindings_at_different_loci_cannot_be_interchanged(self):
        other = copy.deepcopy(self.bindings[0])
        other["loci"] = ["book-10.chapter-7"]
        self.bindings.append(other)
        row = copy.deepcopy(self.rows[0])
        row.update(id="augustine-next-chapter", binding_index=2, locus="book-10.chapter-7")
        self.rows.append(row)
        self.pin_bindings()
        self.check()
        unchanged = copy.deepcopy(self.rows)
        self.bindings.reverse()
        self.write_toml(self.binding_path, {"schema": 1, "record_type": "bindings",
                                          "document": DOCUMENT, "bindings": self.bindings}, "bindings")
        self.assertEqual(self.rows, unchanged)
        with self.assertRaisesRegex(ValueError, "binding_sha256 disagrees"):
            self.check()

    def test_used_witness_requires_a_registered_artifact(self):
        self.artifact.unlink()
        with self.assertRaisesRegex(ValueError, "unregistered source"):
            self.check()

    def test_research_preflight_rejects_a_missing_disposition_over_valid_bindings(self):
        self.assertEqual(SOURCE_LIBRARY.load_library(self.root).errors, [])
        self.rows = []
        self.save_rows()
        with patch.object(study, "scope"), patch.object(study, "run"):
            with self.assertRaisesRegex(ValueError, "omits source bindings"):
                study.check(self.root, "gpt", DOCUMENT, "research", None,
                            require_source_dispositions=True)
            # Historical callers retain their original non-admission contract.
            study.check(self.root, "gpt", DOCUMENT, "research", None)

    def test_admitted_requires_a_passage_instead_of_an_artifact_or_missing_id(self):
        self.admit()
        for source_id in (ARTIFACT_ID, "passage.not-registered"):
            with self.subTest(source_id=source_id):
                self.rows[0]["passage_ids"] = [source_id]
                with self.assertRaisesRegex(ValueError, "admission requires an existing passage"):
                    self.check()

    def test_admitted_passage_requires_its_canonical_scripture_edge(self):
        self.admit()
        self.map_passage(passage_id="passage.some-other-fragment")
        with self.assertRaisesRegex(ValueError, "lack a canonical Scripture edge"):
            self.check()

    def test_admitted_passage_and_edge_validate_and_are_sealed_as_evidence(self):
        self.admit()
        edge = self.map_passage()
        paths = self.check()
        self.assertIn(self.passage, paths)
        self.assertIn(edge, paths)
        self.assertIn(self.root / _catena.ALIASES_RELATIVE, paths)
        self.assertIn(self.root / "src/sources/bibles/clementine-vulgate/chapters/Gen/1.json", paths)

    def test_anthology_admission_seals_the_constituent_work_outside_controller_ancestry(self):
        self.work.write_text(self.work.read_text().replace(
            'work_type = "patristic-treatise"', 'work_type = "anthology"'))
        constituent = self.write("src/sources/works/augustine/constituent/work.toml", '''schema=1
record_type="work"
id="work.augustine.constituent"
title="De civitate Dei"
responsible="Augustine of Hippo"
work_type="patristic-commentary"
languages=["la"]
composed="417"
composed_basis="Synthetic fixture date only."
''')
        self.pin_bindings()
        self.admit()
        self.map_passage(work_id="work.augustine.constituent", constituent_of=EDITION_ID,
                         text_date=None, text_date_basis="")
        self.assertNotIn(constituent, study.bound_evidence(self.root, self.binding_path))
        self.assertIn(constituent, self.check())

    def test_binding_digest_recipe_reports_the_actual_full_local_use(self):
        output = io.StringIO()
        args = ["_proper_study.py", "binding-digests", "--root", str(self.root),
                "--provider", "gpt", "--document", DOCUMENT]
        with patch.object(sys, "argv", args), patch("sys.stdout", output):
            self.assertEqual(study.main(), 0)
        reported = json.loads(output.getvalue())["bindings"]
        self.assertEqual(reported, [{"binding_index": 1, "source_id": ARTIFACT_ID,
                                     "binding_sha256": study.binding_digest(self.bindings[0])}])

    def test_admission_uses_catena_text_date_voice_and_rights_requirements(self):
        self.admit()
        original_passage = self.passage.read_text()
        self.map_passage()
        self.passage.write_text("\n".join(line for line in original_passage.splitlines()
                                         if not line.lstrip().startswith(("text =", "transcription_segments ="))))
        with self.assertRaisesRegex(ValueError, "has no text"):
            self.check()
        self.passage.write_text(original_passage)
        self.map_passage(text_date=None)
        with self.assertRaisesRegex(ValueError, "dated by nothing"):
            self.check()
        self.map_passage()
        self.edition.write_text("\n".join(line for line in self.edition.read_text().splitlines()
                                         if not line.lstrip().startswith("translators =")))
        self.pin_bindings()
        with self.assertRaisesRegex(ValueError, "no translator"):
            self.check()

    def test_corrupt_retained_bytes_cannot_be_handed_off(self):
        payload = self.artifact.parent / "city-of-god.txt"
        payload.write_text("Different bytes, same false metadata.\n")
        with self.assertRaisesRegex(ValueError, "invalid reusable-source evidence"):
            self.check()

    def test_restricted_text_cannot_be_admitted_even_with_refreshed_identity_pins(self):
        self.admit()
        self.map_passage()
        self.artifact.write_text(self.artifact.read_text().replace(
            'rights_status = "public-domain"', 'rights_status = "restricted"'))
        self.pin_bindings()
        with self.assertRaisesRegex(ValueError, "may not be published|affirmative distribution"):
            self.check()

    def test_a_passage_is_not_admitted_merely_because_it_was_inspected(self):
        self.admit()
        self.map_passage()
        self.passage.write_text(self.passage.read_text().replace(
            'states = ["inspected", "verified"]', 'states = ["inspected"]'))
        with self.assertRaisesRegex(ValueError, "has not been verified"):
            self.check()

    def test_restricted_exact_witness_can_be_deferred_with_no_retained_bytes(self):
        text = self.artifact.read_text()
        text = text.replace('storage = "tracked"', 'storage = "restricted"')
        text = text.replace('rights_status = "public-domain"', 'rights_status = "restricted"')
        text = "\n".join(line for line in text.splitlines()
                         if not line.lstrip().startswith(("path =", "indexable =", "encoding =")))
        self.artifact.write_text(text)
        (self.artifact.parent / "city-of-god.txt").unlink()
        self.passage.unlink()
        self.pin_bindings()
        self.rows[0].update(reason="Metadata-only exact witness; redistribution is restricted.",
                            missing_criteria=["publishable-rights"])
        self.check()
        self.assertEqual(list(self.artifact.parent.iterdir()), [self.artifact])

    def test_explicit_noncommentary_use_needs_no_fragment(self):
        self.rows[0].update(disposition="not-commentary", relationship="not-commentary",
                            reason="This exact source supplies an edition fact only.")
        self.rows[0].pop("scripture_extents")
        self.rows[0].pop("missing_criteria")
        self.check()

    def test_historical_research_seals_do_not_require_the_new_handoff(self):
        (self.leaf / study.SOURCE_DISPOSITIONS).unlink()
        with patch.object(study, "chronology_computation_inputs", return_value={}), \
                patch.object(study, "source_admission_computation_inputs", return_value={}), \
                patch.object(study, "chronology_reads", return_value=(set(), {}, [])):
            for contract in (None, study.RESEARCH_REVIEW_CONTRACT, study.CHRONOLOGY_READS_CONTRACT):
                study.review_inputs(self.root, "gpt", DOCUMENT, "research", review_contract=contract)
            with self.assertRaisesRegex(ValueError, "missing reusable-source handoff"):
                study.review_inputs(self.root, "gpt", DOCUMENT, "research",
                                    review_contract=study.SOURCE_DISPOSITIONS_CONTRACT)

    def test_v5_seal_includes_the_admitted_passage_and_canonical_map(self):
        self.admit()
        edge = self.map_passage()
        self.save_rows()
        with patch.object(study, "chronology_computation_inputs", return_value={}), \
                patch.object(study, "source_admission_computation_inputs", return_value={}), \
                patch.object(study, "chronology_reads", return_value=(set(), {}, [])):
            legacy = study.review_inputs(self.root, "gpt", DOCUMENT, "research",
                                         review_contract=study.CHRONOLOGY_READS_CONTRACT)
            current = study.review_inputs(self.root, "gpt", DOCUMENT, "research",
                                          review_contract=study.SOURCE_DISPOSITIONS_CONTRACT)
            self.assertNotIn(str(self.passage.relative_to(self.root)), legacy["files"])
            self.assertIn(str(self.passage.relative_to(self.root)), current["files"])
            self.assertIn(str(edge.relative_to(self.root)), current["files"])
            edge.write_text(edge.read_text() + "\n# Independently reviewed edge metadata changed.\n")
            self.assertNotEqual(current, study.review_inputs(
                self.root, "gpt", DOCUMENT, "research", review_contract=study.SOURCE_DISPOSITIONS_CONTRACT))


class WorkflowHandoffTests(unittest.TestCase):
    def test_new_runs_must_register_sources_then_pass_the_engine_gate_and_v5_seal(self):
        pipeline = json.loads((ROOT / "workflows/pipelines/proper-study.json").read_text())
        stages = {stage["id"]: stage for stage in pipeline["stages"]}
        self.assertGreaterEqual(pipeline["version"], 15)
        self.assertEqual(stages["research"]["next"], "source-registration")
        self.assertEqual(stages["source-registration"]["next"], "research-preflight")
        checks = stages["research-preflight"]["checks"]
        self.assertIn("--require-source-dispositions", checks[0]["command"])
        self.assertTrue(any("source-reader structure --check" in check["command"] for check in checks))
        self.assertIn("--review-contract proper-study-v5", stages["research-review"]["review_input_command"])

    def test_research_check_enforces_dispositions_when_the_pipeline_requests_it(self):
        with patch.object(study, "scope"), patch.object(study, "reference_only_contract"), \
                patch.object(study, "run"), patch.object(study, "review_inputs"), \
                patch.object(study, "source_dispositions", side_effect=ValueError("missing handoff")) as guard, \
                patch.object(study, "leaf_path", return_value=ROOT / "workflows/fragments/proper-study"):
            # Supply ordinary research records without depending on a publication.
            with patch.object(Path, "is_file", return_value=True), \
                    patch.object(Path, "read_text", return_value="synthetic record"):
                with self.assertRaisesRegex(ValueError, "missing handoff"):
                    study.check(ROOT, "gpt", DOCUMENT, "research", None, require_source_dispositions=True)
            guard.assert_called_once_with(ROOT, "gpt", DOCUMENT)


if __name__ == "__main__":
    unittest.main()
