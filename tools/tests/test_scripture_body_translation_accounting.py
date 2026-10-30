"""A proved whole English antiphon survives its negative-to-positive transition."""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage
import yaml


def load_tool(name):
    loader = SourceFileLoader("scripture_body_accounting_" + name.replace("-", "_"),
                              str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


class ScriptureBodyAccountingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool("mass-propers")

    def setUp(self):
        # Repeated names, sibling forms, Sunday cycles and a borrower all carry
        # the same citation. That citation must establish none of their bodies.
        scripture = {"name": "Communion Antiphon", "source": "scripture",
                     "verses": [{"ref": "Psalm 1:1"}]}
        cyclic = {"name": "Communion Antiphon", "source": "scripture",
                  "cycles": {key: {"verses": [{"ref": "Psalm 1:1"}]}
                             for key in ("A", "B")}}
        self.document = {
            "calendar": "test", "psalm_numbering": "vulgate",
            "sections": {"seasonal": {"kind": "seasonal", "masses": [
                {"key": "owner", "forms": [
                    {"id": "vigil", "name": "Vigil", "propers": [scripture, cyclic]},
                    {"id": "day", "name": "Day", "propers": [copy.deepcopy(scripture)]},
                ]},
                {"key": "borrower", "takes_from": {"mass": "owner", "form": "Vigil"}},
            ]}},
        }
        self.identity = ("owner", "vigil", "Communion Antiphon", "A", 2)
        self.absence = dict(zip(("mass", "form_id", "proper", "cycle", "occurrence"),
                                self.identity), extent="body", lang="en",
                            availability="unavailable",
                            reason={"kind": "rights-withheld", "source_id": "artifact.fixture",
                                    "surfaces": sorted(self.tool.TRANSLATION_ABSENCE_SURFACES)},
                            note="Synthetic exact whole-body witness for accounting tests.")
        self.positive = {
            **dict(zip(("mass", "form_id", "proper", "cycle", "occurrence"), self.identity)),
            "extent": "body",
            "translations": [{"lang": "en", "rights": "project-created",
                              "text": "Technical complete body."}],
        }

    def report(self, overlay, untranslated):
        # Source admission has its own tests. Here a validated producer result
        # crosses the real appointment resolver and both census partitions.
        with mock.patch.object(self.tool, "translation_overlay", return_value=(overlay, untranslated, [], {})), \
                mock.patch.object(self.tool, "load_calendar", return_value=self.document), \
                mock.patch.object(self.tool, "translation_ledger_calendars", return_value=["base", "test"]), \
                mock.patch.object(self.tool, "inherited_inapplicable_count", return_value=0):
            return self.tool.english_coverage(Path("unused"), "test")

    def test_positive_and_negative_share_denominator_and_exact_owner(self):
        before = self.report({}, {self.identity[:3]: [self.absence]})
        after = self.report({self.identity: self.positive}, {})
        for report in (before, after):
            self.assertEqual(report["slots"], 1)
            self.assertEqual(report["unaccounted"], 0)
            self.assertEqual(report["unmatched_records"], 0)
            self.assertTrue(report["translation_ledger_inherited"])
        self.assertEqual((before["with_english"], before["ledgered_untranslated"]), (0, 1))
        self.assertEqual((after["with_english"], after["ledgered_untranslated"]), (1, 0))
        expected = {self.identity}
        self.assertEqual(self.tool.english_body_targets({}, {self.identity[:3]: [self.absence]}), expected)
        self.assertEqual(self.tool.english_body_targets({self.identity: self.positive}, {}), expected)

    def test_scope_does_not_spread_to_same_citation_form_cycle_or_occurrence(self):
        body_targets = self.tool.english_body_targets({self.identity: self.positive}, {})
        appointed = []
        for _, mass in self.tool.masses_of(self.document):
            for form, proper, taken_from in self.tool.appointed_propers(self.document, mass):
                identity = self.tool.source_slot_identity(self.document, mass, form, proper, taken_from)
                appointed.extend(key for key, _ in self.tool.coverage_slot_units(proper, identity, body_targets))
        # Two appointments of one source owner are still one census target.
        self.assertEqual(appointed, [self.identity, self.identity])

    def test_unscoped_and_nonenglish_positive_rows_do_not_invent_bodies(self):
        for changes in ({"extent": "incipit"}, {"extent": None},
                        {"translations": [{"lang": "fr", "rights": "project-created", "text": "Technical."}]}):
            with self.subTest(changes=changes):
                entry = dict(self.positive, **changes)
                report = self.report({self.identity: entry}, {})
                self.assertEqual(report["slots"], 0)
                self.assertEqual(report["with_english"], 0)
                self.assertEqual(report["unmatched_records"], 1)

    def test_unappointed_positive_body_remains_unmatched(self):
        for offset, value in ((0, "unrelated"), (1, "unknown-form"), (3, "C"), (4, 3)):
            with self.subTest(offset=offset):
                target = list(self.identity)
                target[offset] = value
                report = self.report({tuple(target): self.positive}, {})
                self.assertEqual(report["slots"], 0)
                self.assertEqual(report["unmatched_records"], 1)

    def test_generated_coverage_keeps_body_coordinate_and_latin_carrier(self):
        source = coverage.identity("test", "proper", *self.identity[:3], self.identity[4])
        target = coverage.identity(source, "cycles", self.identity[3])
        owner = {"source": "scripture", "citations": [{"ref": "Psalm 1:1"}]}
        negative = dict(owner, untranslated=[self.tool.public_untranslated_record(self.absence)])
        before = coverage.unit(negative, target_id=target, occurrence_id="appointed",
                               cycle_family="cycles", cycle="A",
                               absence_kinds={"en": ["rights-withheld"]})
        positive = dict(owner, translations=self.positive["translations"])
        after = coverage.unit(positive, target_id=target, occurrence_id="appointed",
                              cycle_family="cycles", cycle="A", translation_body_languages=["en"])
        for field in ("target_id", "occurrence_id", "component", "body_languages", "scripture_component"):
            self.assertEqual(before[field], after[field], field)
        la_before, en_before = before["languages"]
        la_after, en_after = after["languages"]
        self.assertEqual(la_before, la_after)
        self.assertEqual(la_after["relationship"], "bible-reconstruction")
        self.assertEqual(en_before["availability"], "not-publishable")
        self.assertEqual(en_after["availability"], "available")
        self.assertEqual(en_after["relationship"], "study-translation")
        for unit in (before, after):
            summary = coverage.summarize([unit], "selection")
            coverage.validate_summary(summary)
            self.assertEqual([row["targets"] for row in summary["languages"]], [0, 1])
        unscoped = coverage.unit(positive, target_id=target, occurrence_id="appointed")
        self.assertEqual(unscoped["component"], "scripture")
        self.assertNotIn("body_languages", unscoped)

    def test_explicit_scope_accepts_only_the_closed_english_body_shape(self):
        for value in ([], ["la"], ["en", "la"], ["en", "en"], "en"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "explicit translation body scope"):
                coverage.unit({"source": "scripture"}, target_id="target", occurrence_id="use",
                              translation_body_languages=value)


class ScriptureBodyAdmissionTests(unittest.TestCase):
    """Only an explicitly pinned source packet crosses both production gates."""

    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool("mass-propers")
        cls.checker = load_tool("check-calendar-masses")

    @staticmethod
    def digest(value):
        if isinstance(value, dict):
            value = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
        elif isinstance(value, str):
            value = value.encode()
        return hashlib.sha256(value).hexdigest()

    def setUp(self):
        scratch = ROOT / ".scratch" / "scripture-antiphon-accounting-20261029"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.repository = Path(self.temporary.name)
        self.root = self.repository / "src/sources/calendars"
        (self.root / "test").mkdir(parents=True)
        self.inventory = self.root.parent / "inventories"
        self.inventory.mkdir()
        self.calendar = self.root / "test/propers.yaml"
        self.document = {"calendar": "test", "sections": {"seasonal": {"masses": [{
            "key": "fixture", "propers": [{"name": "Communion Antiphon", "source": "scripture",
                                           "verses": [{"ref": "Psalm 1:1"}]}],
        }]}}}
        self.calendar.write_text(yaml.safe_dump(self.document))
        self.payload = self.repository / "source/old-latin.txt"
        self.payload.parent.mkdir()
        self.payload.write_text("Technical independently held Latin body.\n")
        source_sha = self.digest(self.payload.read_bytes())
        self.records = {
            "work.old": {"record_type": "work"},
            "edition.old": {"record_type": "edition", "work_id": "work.old", "language": "la"},
            "artifact.old": {"record_type": "artifact", "edition_id": "edition.old", "storage": "tracked",
                             "path": "source/old-latin.txt", "sha256": source_sha, "rights_status": "public-domain"},
            "passage.old": {"record_type": "passage", "edition_id": "edition.old", "artifact_id": "artifact.old",
                            "artifact_sha256": source_sha, "states": ["inspected", "verified"]},
            "work.target": {"record_type": "work"},
            "edition.target": {"record_type": "edition", "work_id": "work.target", "language": "en"},
            "artifact.target": {"record_type": "artifact", "edition_id": "edition.target", "storage": "restricted",
                                "sha256": "a" * 64, "rights_status": "unresolved"},
            "passage.target": {"record_type": "passage", "edition_id": "edition.target", "artifact_id": "artifact.target",
                               "artifact_sha256": "a" * 64,
                               "locus": "proper-body:test:fixture:main:Communion%20Antiphon:all:1:en",
                               "states": ["inspected", "verified"], "artifact_page_ranges": [[12, 12]],
                               "verified_on": "2026-10-29"},
        }
        self.target = {"mass": "fixture", "form_id": "main", "proper": "Communion Antiphon",
                       "cycle": "all", "occurrence": 1, "extent": "body", "lang": "en"}
        self.absence = dict(self.target, availability="unavailable",
                            reason={"kind": "rights-withheld", "source_id": "artifact.target",
                                    "surfaces": ["public-git"]}, note="Synthetic exact target witness.",
                            witness_artifact_id="artifact.target", witness_passage_id="passage.target",
                            verified_artifact_page=12, verified_on_page="2026-10-29")
        self.entry = {key: value for key, value in self.target.items() if key != "lang"}
        self.entry.update(scripture_body_source={"admission_id": "fixture-reviewed"},
                          translations=[{"lang": "en", "rights": "project-created", "text": "Technical complete study body."}])
        self.packet = {
            "schema": "triptych-scripture-body-translation-admission/v1", "id": "fixture-reviewed",
            "calendar": "test", "target": self.target,
            "english_sha256": self.digest(self.entry["translations"][0]["text"]),
            "target_witness": self.absence, "source_passage_ids": ["passage.old"],
            "source_record_sha256": {key: self.digest(value) for key, value in self.records.items()},
            "source_payload_sha256": {"source/old-latin.txt": source_sha},
            "assessment": {"scope": "Synthetic test only; no liturgical admission.",
                           "ancient_reading": self.payload.read_text(), "arrangement": "complete",
                           "variants": [], "omissions": []},
        }
        self.packet_path = self.repository / "reviews/admission.json"
        self.packet_path.parent.mkdir()
        self.admissions = {}
        self.recension_admissions = {}
        self.pin_packet()
        self.patches = [mock.patch.object(self.tool, "SCRIPTURE_BODY_TRANSLATION_ADMISSIONS", self.admissions),
                        mock.patch.object(self.tool, "SCRIPTURE_BODY_TRANSLATION_RECENSION_ADMISSIONS", self.recension_admissions),
                        mock.patch.object(self.tool, "_source_library_records", return_value=(self.records, [])),
                        mock.patch.object(self.checker, "OVERLAY_DIR", self.inventory),
                        mock.patch.object(self.checker, "_SOURCE_RECORDS", (self.records, None)),
                        mock.patch.object(self.checker, "act_history", return_value=()),
                        mock.patch.object(self.checker, "sibling", return_value=self.tool)]
        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)
        self.addCleanup(self.temporary.cleanup)

    def pin_packet(self):
        self.packet_path.write_text(json.dumps(self.packet, sort_keys=True))
        self.admissions["fixture-reviewed"] = ("reviews/admission.json", self.digest(self.packet_path.read_bytes()))

    def validate(self, entry=None):
        return self.tool.scripture_body_translation_problems(
            self.entry if entry is None else entry, "test", self.root, records=self.records)

    def write_entry(self, entry):
        lines = ['schema = "triptych-proper-translations/v1"', 'calendar = "test"', '[[entries]]']
        for key, value in entry.items():
            if key not in {"translations", "scripture_body_source"}:
                lines.append(f"{key} = {json.dumps(value)}")
        binding = entry.get("scripture_body_source")
        if binding is not None:
            lines.append("[entries.scripture_body_source]")
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in binding.items())
        for translation in entry["translations"]:
            lines.append("[[entries.translations]]")
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in translation.items())
        (self.inventory / "test-proper-translations-v1.toml").write_text("\n".join(lines) + "\n")

    def test_exact_synthetic_packet_passes_both_producer_and_checker(self):
        self.assertEqual(self.validate(), [])
        self.write_entry(self.entry)
        overlay, untranslated, _, _ = self.tool.translation_overlay("test", self.root)
        self.assertEqual(set(overlay), {("fixture", "main", "Communion Antiphon", "all", 1)})
        self.assertEqual(untranslated, {})
        self.assertEqual(self.checker.overlay_problems([self.calendar])[0], [])

    def test_empty_production_dispatcher_and_unknown_methods_refuse(self):
        self.admissions.clear()
        self.assertIn("exact reviewed finite admission", " ".join(self.validate()))
        self.write_entry(self.entry)
        with self.assertRaisesRegex(ValueError, "exact reviewed finite admission"):
            self.tool.translation_overlay("test", self.root)
        self.assertIn("exact reviewed finite admission", " ".join(self.checker.overlay_problems([self.calendar])[0]))

    def test_citation_only_or_self_asserted_body_cannot_pass_either_gate(self):
        for key in ("extent", "scripture_body_source", "form_id", "cycle", "occurrence"):
            with self.subTest(key=key):
                entry = copy.deepcopy(self.entry)
                entry.pop(key)
                self.assertTrue(self.validate(entry))
                self.write_entry(entry)
                with self.assertRaises(ValueError):
                    self.tool.translation_overlay("test", self.root)
                self.assertTrue(self.checker.overlay_problems([self.calendar])[0])

    def test_body_or_coordinate_tampering_refuses(self):
        for field, value in (("mass", "other"), ("form_id", "day"), ("cycle", "A"), ("occurrence", 2)):
            with self.subTest(field=field):
                self.assertTrue(self.validate(dict(self.entry, **{field: value})))
        entry = copy.deepcopy(self.entry)
        entry["translations"][0]["text"] += " Altered."
        self.assertIn("English body", " ".join(self.validate(entry)))

    def test_source_record_payload_or_packet_tampering_refuses(self):
        self.records["passage.old"]["states"] = ["cataloged"]
        self.assertIn("source record is missing or changed", " ".join(self.validate()))
        self.records["passage.old"]["states"] = ["inspected", "verified"]
        self.payload.write_text("Altered Latin.")
        self.assertIn("payload is missing or changed", " ".join(self.validate()))
        self.payload.write_text("Technical independently held Latin body.\n")
        self.packet_path.write_text(self.packet_path.read_text() + "\n")
        self.assertIn("packet or payload is missing or changed", " ".join(self.validate()))

    def test_complete_scalar_and_list_derivation_ancestry_is_required(self):
        # The retained Clementine verse artifact uses one scalar derived_from
        # ID. Follow its entire source graph without treating that ID as chars.
        self.records["artifact.raw"] = {
            "record_type": "artifact", "edition_id": "edition.old",
            "storage": "remote", "sha256": "b" * 64,
            "rights_status": "public-domain",
        }
        self.records["artifact.projected"] = {
            "record_type": "artifact", "edition_id": "edition.old",
            "storage": "remote", "sha256": "c" * 64,
            "rights_status": "public-domain", "projected_from": "artifact.raw",
        }
        self.records["artifact.old"].update(
            derived_from="artifact.projected", projected_from=["artifact.raw"])
        complete_pins = {key: self.digest(value) for key, value in self.records.items()}
        self.packet["source_record_sha256"] = complete_pins.copy()
        self.pin_packet()
        self.assertEqual(self.validate(), [])
        self.write_entry(self.entry)
        self.assertEqual(self.tool.translation_overlay("test", self.root)[1], {})
        self.assertEqual(self.checker.overlay_problems([self.calendar])[0], [])
        for missing in ("artifact.raw", "artifact.projected"):
            with self.subTest(missing=missing):
                self.packet["source_record_sha256"] = complete_pins.copy()
                self.packet["source_record_sha256"].pop(missing)
                self.pin_packet()
                self.assertIn("source ancestor", " ".join(self.validate()))

    def test_malformed_derivation_ancestry_types_are_refused(self):
        original = copy.deepcopy(self.records["artifact.old"])
        for field in ("derived_from", "projected_from"):
            for malformed in (None, {}, 1, True, ("artifact.raw",), [None], [""], "", " "):
                with self.subTest(field=field, malformed=malformed):
                    self.records["artifact.old"] = dict(original, **{field: malformed})
                    self.packet["source_record_sha256"]["artifact.old"] = self.digest(
                        self.records["artifact.old"])
                    self.pin_packet()
                    self.assertIn("malformed source ancestry", " ".join(self.validate()))
        self.records["artifact.old"] = original

    def test_even_pinned_packet_requires_full_target_witness_and_independent_pd_source(self):
        for mutation in ("wrong-witness", "no-source", "unheld-source", "unresolved-rights", "missing-ancestor"):
            with self.subTest(mutation=mutation):
                before_packet, before_records = copy.deepcopy(self.packet), copy.deepcopy(self.records)
                if mutation == "wrong-witness":
                    self.packet["target_witness"]["verified_artifact_page"] = 13
                elif mutation == "no-source":
                    self.packet["source_passage_ids"] = []
                elif mutation == "unheld-source":
                    self.records["artifact.old"]["storage"] = "remote"
                elif mutation == "unresolved-rights":
                    self.records["artifact.old"]["rights_status"] = "unresolved"
                else:
                    self.packet["source_record_sha256"].pop("work.old")
                if mutation in {"unheld-source", "unresolved-rights"}:
                    self.packet["source_record_sha256"]["artifact.old"] = self.digest(self.records["artifact.old"])
                self.pin_packet()
                self.assertTrue(self.validate())
                self.packet = before_packet
                self.records.clear()
                self.records.update(before_records)
                self.pin_packet()

    def test_body_binding_cannot_attach_to_composed_or_unappointed_target(self):
        for mutation in ("composed", "unappointed"):
            with self.subTest(mutation=mutation):
                document = copy.deepcopy(self.document)
                if mutation == "composed":
                    proper = document["sections"]["seasonal"]["masses"][0]["propers"][0]
                    proper.update(source="composed", text="Technical Latin.")
                    proper.pop("verses")
                else:
                    document["sections"]["seasonal"]["masses"][0]["key"] = "other"
                self.calendar.write_text(yaml.safe_dump(document))
                self.write_entry(self.entry)
                with self.assertRaises(ValueError):
                    self.tool.translation_overlay("test", self.root)
                self.assertTrue(self.checker.overlay_problems([self.calendar])[0])

    def child_calendar(self, *, masked=False):
        child = self.root / "child/propers.yaml"
        child.parent.mkdir()
        departures = [{"key": "fixture", "departure": "absent", "basis": "Synthetic source departure."}] if masked else []
        child.write_text(yaml.safe_dump({"schema": "triptych-calendar-masses/v1", "calendar": "child",
                                        "text_from": "test", "sections": {"seasonal": {"kind": "seasonal",
                                                                                     "masses": departures}}}))
        lines = ['calendar = "child"']
        if masked:
            lines += ['[[inherited_inapplicable]]', 'record = "entry"', 'mass = "fixture"',
                      'form_id = "main"', 'proper = "Communion Antiphon"', 'cycle = "all"',
                      'occurrence = 1', 'reason = "recension-absent"', 'basis = "calendar-departure"']
        (self.inventory / "child-proper-translations-v1.toml").write_text("\n".join(lines) + "\n")
        self.write_entry(self.entry)
        return child

    def test_exact_child_exclusion_removes_parent_before_child_admission(self):
        child = self.child_calendar(masked=True)
        overlay, unavailable, _, _ = self.tool.translation_overlay("child", self.root)
        self.assertEqual((overlay, unavailable), ({}, {}))
        self.assertEqual(self.checker.overlay_problems([child])[0], [])

    def test_same_citation_child_refuses_without_its_own_closed_admission(self):
        child = self.child_calendar()
        with self.assertRaisesRegex(ValueError, "requested recension 'child'"):
            self.tool.translation_overlay("child", self.root)
        self.assertIn("requested recension 'child'", " ".join(self.checker.overlay_problems([child])[0]))
        # A child without a local sidecar must obey the same inherited gate.
        (self.inventory / "child-proper-translations-v1.toml").unlink()
        self.assertIn("requested recension 'child'", " ".join(self.checker.overlay_problems([child])[0]))

    def test_scoped_child_checker_rejects_parent_with_missing_body_claim_fields(self):
        child = self.child_calendar()
        sidecar = self.inventory / "child-proper-translations-v1.toml"
        for fields in (("scripture_body_source",), ("scripture_body_source", "extent")):
            for local_sidecar in (True, False):
                with self.subTest(fields=fields, local_sidecar=local_sidecar):
                    entry = copy.deepcopy(self.entry)
                    for field in fields:
                        entry.pop(field)
                    self.write_entry(entry)
                    if local_sidecar:
                        sidecar.write_text('calendar = "child"\n')
                    else:
                        sidecar.unlink(missing_ok=True)
                    with self.assertRaises(ValueError):
                        self.tool.translation_overlay("child", self.root)
                    self.assertTrue(self.checker.overlay_problems([child])[0])

    def test_independent_closed_child_packet_is_required_and_rechecked(self):
        child = self.child_calendar()
        child_packet = copy.deepcopy(self.packet)
        child_packet.update(id="fixture-child-reviewed", calendar="child")
        child_witness = copy.deepcopy(self.records["passage.target"])
        child_witness["locus"] = child_witness["locus"].replace("proper-body:test:", "proper-body:child:")
        self.records["passage.target-child"] = child_witness
        child_packet["target_witness"]["witness_passage_id"] = "passage.target-child"
        child_packet["source_record_sha256"] = {key: self.digest(value) for key, value in self.records.items()}
        packet_path = self.repository / "reviews/child-admission.json"
        packet_path.write_text(json.dumps(child_packet, sort_keys=True))
        self.admissions["fixture-child-reviewed"] = ("reviews/child-admission.json", self.digest(packet_path.read_bytes()))
        self.recension_admissions[("fixture-reviewed", "child")] = "fixture-child-reviewed"
        overlay, _, _, _ = self.tool.translation_overlay("child", self.root)
        entry = next(iter(overlay.values()))
        self.assertEqual(entry["scripture_body_source"], {"admission_id": "fixture-child-reviewed"})
        self.assertEqual(entry["translations"], self.entry["translations"])
        self.assertEqual(self.checker.overlay_problems([child])[0], [])
        self.records["passage.target-child"]["verified_on"] = "2026-10-30"
        with self.assertRaisesRegex(ValueError, "source record is missing or changed"):
            self.tool.translation_overlay("child", self.root)
        self.assertIn("source record is missing or changed", " ".join(self.checker.overlay_problems([child])[0]))


if __name__ == "__main__":
    unittest.main()
