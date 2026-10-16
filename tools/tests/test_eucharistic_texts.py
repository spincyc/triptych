"""Publication and witness boundaries of the original-language adapters."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _eucharistic_texts as texts


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class AdapterBoundaryTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/text-reuse-expansion"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records = {}
        self.library = SimpleNamespace(records=self.records, errors=[])

    def record(self, identity, kind, **data):
        path = self.root / "records" / (identity + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = {"id": identity, "record_type": kind, **data}
        path.write_text(json.dumps(fields), encoding="utf-8")
        self.records[identity] = SimpleNamespace(path=path, record_type=kind, data=fields)
        return fields

    def artifact(self, identity, body, **metadata):
        path = self.root / "payloads" / (identity + ".txt")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return self.record(identity, "artifact", storage="tracked", path=path.relative_to(self.root).as_posix(),
                           sha256=sha(body), byte_size=len(body.encode("utf-8")), **metadata)

    def proper_fixture(self):
        self.path = self.root / "src/sources/calendars/roman-1962/propers.yaml"
        self.path.parent.mkdir(parents=True)
        self.path.write_text('''schema: triptych-calendar-masses/v1
calendar: roman-1962
sections:
  seasonal:
    kind: seasonal
    masses:
      - key: synthetic
        name: Synthetic test only
        registry: '01'
        propers:
          - name: Collect
            source: composed
            text: "Idem textus."
          - name: Collect
            source: composed
            text: "Idem textus."
''')
        self.record("edition.projection", "edition", date="2026-09-03")
        target_edition = "edition.catholic-church.missale-romanum.vatican-typica-1962"
        self.record(target_edition, "edition", date="1962")
        projection = self.artifact("artifact.projection", "Idem textus.\nIdem textus.\n",
                                   edition_id="edition.projection", rights_status="project-created")
        self.artifact("artifact.public-domain", "Historical fixture.\n", rights_status="public-domain")
        self.record("artifact.target", "artifact", storage="remote", rights_status="unresolved", sha256="a" * 64)
        self.record("passage.target", "passage", edition_id=target_edition, artifact_id="artifact.target")
        self.entries = []
        for occurrence in (1, 2):
            passage = f"passage.projection.{occurrence}"
            self.record(passage, "passage", edition_id="edition.projection", artifact_id="artifact.projection",
                        artifact_sha256=projection["sha256"], physical_line_ranges=[[occurrence, occurrence]])
            self.entries.append({
                "mass": "synthetic", "form": "", "proper": "Collect", "course": "", "cycle": "", "occurrence": occurrence,
                "text_sha256": sha("Idem textus."), "provenance_status": "collated", "source_id": passage,
                "source_date": "2026-09-03", "locator": "fixture line", "relationship": "editorial-projection-exact-to-target",
                "verification_source_id": "passage.target", "verification_locator": "fixture target page",
                "transformations": [], "provenance_evidence": "Synthetic test evidence", "provenance_authority": "test",
                "provenance_confidence": "high", "publication_status": "permitted", "publication_basis": "public-domain",
                "surfaces": ["public-git", "corpus-data"], "publication_source_ids": ["artifact.public-domain"],
                "publication_locator": "fixture", "publication_evidence": "Synthetic test basis",
            })
        self.ledger = self.root / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
        self.ledger.parent.mkdir(parents=True)
        self.write_ledger()

    def write_ledger(self):
        lines = ['schema = "triptych-proper-latin-provenance/v1"', 'calendar = "roman-1962"', 'language = "la"',
                 'policy = "guidance/liturgical-text-publication-policy.md"', '[defaults]',
                 'provenance_status = "unresolved"', 'publication_status = "unresolved"',
                 'publication_basis = "unresolved"', 'surfaces = []']
        for entry in self.entries:
            lines.append('[[entries]]')
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in entry.items())
        self.ledger.write_text("\n".join(lines) + "\n")

    def load(self, adapter="roman-1962-propers"):
        with patch.object(texts, "_load_library", return_value=self.library):
            return texts.load_adapter(adapter, self.root)

    def test_occurrences_keep_distinct_identity_and_order_even_when_words_match(self):
        self.proper_fixture()
        first = self.load()
        self.assertEqual(first, self.load())
        units = first["units"]
        self.assertEqual([1, 2], [u["identity"]["occurrence"] for u in units])
        self.assertNotEqual(units[0]["unit_id"], units[1]["unit_id"])
        self.assertEqual(units[0]["content_id"], units[1]["content_id"])
        self.assertNotEqual(units[0]["text_edition_id"], units[0]["target_edition_id"])
        self.assertFalse(first["scope"]["whole_book_complete"])
        self.assertEqual([], first["historical_comparisons"])

    def test_changed_calendar_text_fails_even_with_plausible_words(self):
        self.proper_fixture()
        self.path.write_text(self.path.read_text().replace("Idem textus.", "Mutatus textus.", 1))
        with self.assertRaisesRegex(texts.AdapterError, "stale text hash"):
            self.load()

    def test_rehashed_calendar_cannot_drift_from_owning_projection(self):
        self.proper_fixture()
        self.path.write_text(self.path.read_text().replace("Idem textus.", "Mutatus textus.", 1))
        self.entries[0]["text_sha256"] = sha("Mutatus textus.")
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "differs from owning projection"):
            self.load()

    def test_web_permission_does_not_authorize_git_export(self):
        self.proper_fixture()
        self.entries[0]["surfaces"] = ["web"]
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "must cover corpus-data and public-git"):
            self.load()

    def test_changed_projection_payload_fails_hash_check(self):
        self.proper_fixture()
        artifact = self.records["artifact.projection"].data
        (self.root / artifact["path"]).write_text("Mutatus textus.\nIdem textus.\n")
        with self.assertRaisesRegex(texts.AdapterError, "Artifact hash mismatch"):
            self.load()

    def test_registered_other_edition_cannot_verify_a_1962_target(self):
        self.proper_fixture()
        self.record("edition.other-target", "edition", date="1861")
        self.record("passage.other-target", "passage", edition_id="edition.other-target",
                    artifact_id="artifact.target")
        self.entries[0]["verification_source_id"] = "passage.other-target"
        self.write_ledger()
        with self.assertRaisesRegex(texts.AdapterError, "Verification target edition mismatch"):
            self.load()

    def test_alternate_data_root_cannot_supply_or_hide_executed_tool_provenance(self):
        self.proper_fixture()
        # A sparse data root still pins every trusted implementation input.
        first = self.load()
        actual = {row["path"]: row for row in first["tool_inputs"]}
        self.assertEqual(set(texts.TOOL_INPUT_PATHS), set(actual))
        for path, record in actual.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), record["sha256"])
        fake = self.root / "scripts/_eucharistic_texts.py"
        fake.parent.mkdir(parents=True)
        fake.write_text("raise RuntimeError('untrusted data-root code')\n")
        second = self.load()
        self.assertEqual(first["tool_inputs"], second["tool_inputs"])
        self.assertNotIn("scripts/_eucharistic_texts.py", {row["path"] for row in second["inputs"]})

    def test_missing_trusted_tool_input_fails_closed(self):
        self.proper_fixture()
        with patch.object(texts, "TOOL_INPUT_PATHS", ("scripts/absent-eucharistic-tool.py",)):
            with self.assertRaisesRegex(texts.AdapterError, "Cannot export.*absent-eucharistic-tool"):
                self.load()

    def ordinary_fixture(self):
        self.record(texts.ORDINARY_EDITION, "edition", date="1861")
        stem = "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.canon-missae"
        self.artifact(stem + "-la", "seq\telement_key\tpart\tprinted_page\tia_leaf\tlatin\tnotes\n"
                      "2\tte-igitur\tcanon\txxxiii\t43\tTest fixture Latin.\tUnchanged wording\n",
                      rights_status="public-domain", rights_basis="Synthetic test basis", edition_id=texts.ORDINARY_EDITION)
        self.artifact(stem + "-en", "seq\telement_key\tpart\tkind\tspeaker\tprinted_page\tenglish\n"
                      "1\theading\tcanon\theading\t\txxxiii\tDo not export this\n"
                      "2\tte-igitur\tcanon\tprayer\tpriest\txxxiii\tDo not export this either\n"
                      "3\trubric\tcanon\trubric\t\txxxiii\tNor this\n",
                      rights_status="public-domain", rights_basis="Synthetic test basis", edition_id=texts.ORDINARY_EDITION)

    def test_ordinary_preserves_edition_and_explicit_non_latin_omissions(self):
        self.ordinary_fixture()
        with patch.object(texts, "ORDINARY_DIVISIONS", ("canon-missae",)):
            result = self.load("cummiskey-1861-latin-ordinary")
        self.assertEqual("Test fixture Latin.", result["units"][0]["text"])
        self.assertEqual(texts.ORDINARY_EDITION, result["units"][0]["target_edition_id"])
        self.assertEqual(["heading", "rubric"], [r["kind"] for r in result["divisions"][0]["omitted_non_latin_blocks"]])
        self.assertNotIn("Do not export", json.dumps(result))

    def test_ordinary_refuses_a_changed_rights_disposition(self):
        self.ordinary_fixture()
        key = "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.canon-missae-la"
        self.records[key].data["rights_status"] = "unresolved"
        with patch.object(texts, "ORDINARY_DIVISIONS", ("canon-missae",)):
            with self.assertRaisesRegex(texts.AdapterError, "lacks publication basis"):
                self.load("cummiskey-1861-latin-ordinary")

    def wilson_fixture(self):
        self.wilson_text = "Synthetic source. Exact fixture wording."
        self.record(texts.WILSON_EDITION, "edition", date="1915")
        artifact = self.artifact(texts.WILSON_MEMENTO_ARTIFACT, self.wilson_text + "\n",
                                 artifact_type="normalized-text", edition_id=texts.WILSON_EDITION,
                                 rights_status="public-domain", rights_basis="Synthetic test basis",
                                 rights_jurisdiction="United States", transformation="Synthetic test transformation")
        self.record(texts.WILSON_MEMENTO_PASSAGE, "passage", edition_id=texts.WILSON_EDITION,
                    artifact_id=texts.WILSON_MEMENTO_ARTIFACT, artifact_sha256=artifact["sha256"],
                    physical_line_ranges=[[1, 1]], states=["verified"], verified_on="2026-10-16", locus="Fixture page")

    def load_wilson(self):
        with patch.object(texts, "WILSON_MEMENTO_TEXT_SHA256", sha(self.wilson_text)):
            return self.load("wilson-1915-gregorian-canon-memento")

    def test_wilson_uses_only_the_checked_body_and_preserves_edition_scope(self):
        self.wilson_fixture()
        result = self.load_wilson()
        self.assertEqual(self.wilson_text, result["units"][0]["text"])
        self.assertEqual("1915", result["target_date"])
        self.assertEqual("2026-10-16", result["reviewed_on"])
        self.assertIn("ninth century", result["witness_date"])
        self.assertTrue(result["scope"]["not_direct_manuscript_transcription"])
        self.assertFalse(result["scope"]["whole_book_complete"])
        self.assertIn("critical apparatus, including the O variant", result["scope"]["omitted_book_divisions"])

    def test_wilson_rehashed_wording_cannot_override_the_reviewed_body(self):
        self.wilson_fixture()
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        changed = "Unreviewed replacement.\n"
        (self.root / artifact["path"]).write_text(changed)
        artifact["sha256"] = sha(changed)
        self.records[texts.WILSON_MEMENTO_PASSAGE].data["artifact_sha256"] = sha(changed)
        with self.assertRaisesRegex(texts.AdapterError, "differs from its reviewed wording"):
            self.load_wilson()

    def test_wilson_requires_review_publication_and_exact_identity(self):
        self.wilson_fixture()
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        for record, field, replacement, message in (
            (passage, "states", ["inspected"], "lacks a verified bounded transcription"),
            (artifact, "rights_status", "unresolved", "lacks its public-domain publication basis"),
            (artifact, "rights_jurisdiction", "unspecified", "lacks its public-domain publication basis"),
            (passage, "edition_id", texts.ORDINARY_EDITION, "identity mismatch"),
            (passage, "physical_line_ranges", [[1, 2]], "extent/hash mismatch"),
        ):
            with self.subTest(field=field):
                original = record[field]
                record[field] = replacement
                # An alternative registered edition must still be refused.
                self.record(texts.ORDINARY_EDITION, "edition", date="1861")
                try:
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load_wilson()
                finally:
                    record[field] = original

    def checked_selection(self):
        self.wilson_fixture()
        return {"title": "Synthetic selected prayer", "edition_id": texts.WILSON_EDITION,
                "scope": {"status": "one-complete-prayer", "omitted_book_divisions": ["all other text"]},
                "units": [{"unit_id": "unit.synthetic.prayer", "passage_id": texts.WILSON_MEMENTO_PASSAGE,
                           "artifact_id": texts.WILSON_MEMENTO_ARTIFACT, "text_sha256": sha(self.wilson_text),
                           "language": "la", "division": "canon", "element_key": "synthetic", "source_order": 1}]}

    def test_generic_checked_selection_keeps_native_text_and_deterministic_provenance(self):
        selection = self.checked_selection()
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            first = self.load("synthetic-checked-prayer")
            self.assertEqual(first, self.load("synthetic-checked-prayer"))
        self.assertEqual(self.wilson_text, first["units"][0]["text"])
        self.assertEqual("1915", first["target_date"])
        self.assertIsNone(first["witness_date"])
        self.assertEqual(["all other text"], first["scope"]["omitted_book_divisions"])
        self.assertEqual("Synthetic test transformation", first["units"][0]["provenance"]["normalization"])

    def test_generic_checked_selection_rejects_unreviewed_rehashed_text(self):
        selection = self.checked_selection()
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        changed = "Different but well-formed text.\n"
        (self.root / artifact["path"]).write_text(changed)
        artifact["sha256"] = sha(changed)
        self.records[texts.WILSON_MEMENTO_PASSAGE].data["artifact_sha256"] = sha(changed)
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            with self.assertRaisesRegex(texts.AdapterError, "differs from reviewed wording"):
                self.load("synthetic-checked-prayer")

    def test_generic_checked_selection_preserves_greek_codepoints_and_speech_boundaries(self):
        selection = self.checked_selection()
        # Deliberately decomposed accent, lunate sigma and final sigma: neither
        # Unicode composition nor comparison-oriented letter folding is an export.
        body = "Α\u0301 Ϲ ϲ ς"
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        (self.root / artifact["path"]).write_text(body + "\n", encoding="utf-8")
        artifact.update(sha256=sha(body + "\n"), byte_size=len((body + "\n").encode("utf-8")))
        passage.update(artifact_sha256=artifact["sha256"],
                       notes="Synthetic speech blocks [0, 4) and [5, 8); intervening response omitted.")
        selection["units"][0].update(language="grc", text_sha256=sha(body))
        with patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
            result = self.load("synthetic-checked-prayer")
        unit = result["units"][0]
        self.assertEqual(body.encode("utf-8"), unit["text"].encode("utf-8"))
        self.assertEqual(sha(body), unit["text_sha256"])
        self.assertEqual(passage["notes"], unit["provenance"]["review_limits"])
        self.assertEqual({"grc": 1}, result["counts"]["languages"])

    def test_generic_checked_selection_requires_exact_controller_review_and_rights(self):
        selection = self.checked_selection()
        passage = self.records[texts.WILSON_MEMENTO_PASSAGE].data
        artifact = self.records[texts.WILSON_MEMENTO_ARTIFACT].data
        self.record(texts.ORDINARY_EDITION, "edition", date="1861")
        for record, field, replacement, message in (
            (passage, "edition_id", texts.ORDINARY_EDITION, "identity mismatch"),
            (passage, "artifact_id", "artifact.other", "identity mismatch"),
            (passage, "states", ["inspected"], "is not verified"),
            (artifact, "rights_status", "unresolved", "publication basis"),
            (passage, "physical_line_ranges", [[1, 2]], "extent/hash mismatch"),
        ):
            with self.subTest(field=field), patch.dict(texts.CHECKED_PASSAGE_SETS, {"synthetic-checked-prayer": selection}):
                self.artifact("artifact.other", self.wilson_text + "\n", edition_id=texts.WILSON_EDITION)
                original = record[field]
                record[field] = replacement
                try:
                    with self.assertRaisesRegex(texts.AdapterError, message):
                        self.load("synthetic-checked-prayer")
                finally:
                    record[field] = original


if __name__ == "__main__":
    unittest.main()
