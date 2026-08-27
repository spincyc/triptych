"""Keep the 2011 en-US finding aid honest without copying protected text."""

from __future__ import annotations

import json
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COVERAGE = (
    ROOT
    / "src"
    / "sources"
    / "inventories"
    / "postconciliar-english-2011-recension-coverage-v1.toml"
)
RECENSIONS = ROOT / "src" / "sources" / "calendars" / "recensions.json"


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


propers = load_tool("mass-propers")


def live_slot_sets() -> tuple[
    set[tuple[str, str, str, str, int]],
    set[tuple],
]:
    """Derive exact problem identities through the frozen production helpers."""
    overlay, untranslated, _, _ = propers.translation_overlay(
        "postconciliar", propers.DEFAULT_ROOT
    )
    document = propers.load_calendar(propers.DEFAULT_ROOT, "postconciliar")
    families = {propers.slot_family(key[2]) for key in overlay} | {
        propers.slot_family(key[2]) for key in untranslated
    }
    slots: dict[
        tuple[str, str, str, str, int],
        tuple[dict, dict, tuple[str, str, str]],
    ] = {}
    legacy_slots: set[tuple[str, str, str]] = set()
    for _, mass in propers.masses_of(document):
        for form, proper, taken_from in propers.appointed_propers(document, mass):
            if proper.get("name") == propers.PLACEHOLDER:
                continue
            key = propers.overlay_key(mass, form, proper, taken_from)
            source_identity = propers.source_slot_identity(
                document, mass, form, proper, taken_from
            )
            units = propers.coverage_slot_units(proper, source_identity)
            if units:
                legacy_slots.add(key)
            for identity, owner in units:
                if propers.slot_family(proper.get("name")) in families:
                    slots[identity] = (proper, owner, key)
    covered = {
        identity
        for identity, (_, owner, key) in slots.items()
        if propers.translation_answers(
            propers.translation_entry_for(overlay, key, identity) or {},
            owner,
            "en",
        )
    }
    matched = {
        identity: propers.matching_untranslated_records(
            proper,
            untranslated.get(propers.untranslated_key(identity)) or [],
            identity[4],
            cycle=identity[3],
            extent="body",
        )
        for identity, (proper, _, _) in slots.items()
    }
    ledgered = {identity for identity, records in matched.items() if records}
    matched_absences = {
        (
            identity[0],
            identity[1],
            identity[2],
            identity[3],
            identity[4],
            propers.public_untranslated_record(record)["target"]["extent"],
        )
        for identity, records in matched.items()
        for record in records
    }
    all_absences = {
        (
            public["target"]["mass"],
            public["target"]["form_id"],
            public["target"]["proper"],
            public["target"]["cycle"],
            public["target"]["occurrence"],
            public["target"]["extent"],
        )
        for records in untranslated.values()
        for record in records
        for public in [propers.public_untranslated_record(record)]
    }
    unmatched_positive = {("positive", *key) for key in set(overlay) - legacy_slots}
    unmatched_absence = {
        ("unavailable", *identity) for identity in all_absences - matched_absences
    }
    return set(slots) - covered - ledgered, unmatched_positive | unmatched_absence


class PostconciliarEnglish2011CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = tomllib.loads(COVERAGE.read_text(encoding="utf-8"))
        cls.overlay_path = ROOT / cls.record["overlay_ref"]
        cls.overlay = tomllib.loads(cls.overlay_path.read_text(encoding="utf-8"))

    def test_record_is_an_incomplete_nonpublishing_finding_aid(self) -> None:
        self.assertEqual(
            self.record["schema"], "triptych-recension-language-coverage/v1"
        )
        self.assertEqual(self.record["recension_id"], "roman-missal-en-us-2011")
        self.assertEqual(self.record["calendar"], "postconciliar")
        self.assertEqual(self.record["language"], "en-US")
        self.assertEqual(self.record["status"], "incomplete")
        self.assertEqual(self.record["record_kind"], "finding-aid")
        capability = self.record["capability"]
        self.assertEqual(capability["data_availability"], "partial")
        self.assertEqual(
            capability["website_display"], "blocked-pending-delivery-gate"
        )
        self.assertEqual(
            capability["repository_corpus"], "unavailable-pending-permission"
        )
        self.assertEqual(
            {capability[surface] for surface in ("api", "pdf", "download")},
            {"not-authorized"},
        )
        for ref in (
            "overlay_ref",
            "rights_ref",
            "rights_matrix_ref",
            "publication_policy_ref",
        ):
            self.assertTrue((ROOT / self.record[ref]).is_file(), self.record[ref])

    def test_central_expression_points_back_to_this_finding_aid(self) -> None:
        catalog = json.loads(RECENSIONS.read_text(encoding="utf-8"))
        expression = next(
            row
            for row in catalog["expressions"]
            if row["id"] == self.record["recension_id"]
        )
        self.assertEqual(expression["language"], self.record["language"])
        self.assertEqual(
            expression["coverage_ref"], str(COVERAGE.relative_to(ROOT))
        )
        proper = expression["capabilities"]["propers"]
        self.assertEqual(proper["data_availability"], "partial")
        self.assertEqual(proper["publication_availability"], "unavailable")
        self.assertEqual(proper["collation"], "mixed")

    def test_finding_aid_contains_no_liturgical_text_fields(self) -> None:
        forbidden = {"text", "translation", "translations", "incipit", "words"}

        def visit(value, path: tuple[str, ...] = ()) -> None:
            if isinstance(value, dict):
                self.assertFalse(
                    forbidden & set(value),
                    f"protected-content field at {'.'.join(path) or '<root>'}",
                )
                for key, child in value.items():
                    visit(child, (*path, str(key)))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    visit(child, (*path, str(index)))

        visit(self.record)

    def test_every_overlay_witness_and_translation_source_is_classified(self) -> None:
        classes = self.record["source_classes"]
        by_witness = {row["entry_witness"]: row for row in classes}
        self.assertEqual(len(by_witness), len(classes), "duplicate witness class")
        actual_witnesses = {
            str(entry.get("witness") or "") for entry in self.overlay["entries"]
        }
        active_witnesses = {
            row["entry_witness"] for row in classes if row["active_entries"]
        }
        self.assertEqual(active_witnesses, actual_witnesses)

        source_rows = {row["id"]: row for row in self.overlay["sources"]}
        for row in classes:
            if row["source_record_id"]:
                declared = source_rows[row["source_record_id"]]
                self.assertEqual(
                    row["source_id"], str(declared.get("source_id") or "")
                )
            actual_translation_sources = {
                str(translation.get("source_id") or "")
                for entry in self.overlay["entries"]
                if str(entry.get("witness") or "") == row["entry_witness"]
                for translation in entry.get("translations") or []
            }
            if row["active_entries"]:
                self.assertEqual(
                    set(row["translation_source_ids"]), actual_translation_sources
                )
            else:
                self.assertFalse(actual_translation_sources)
                quarantined_sources = {
                    str(record.get("source_id") or "")
                    for record in self.overlay.get("untranslated") or []
                    if str(record.get("witness") or "") == row["entry_witness"]
                    and record.get("source_id") is not None
                }
                self.assertEqual(
                    set(row["translation_source_ids"]), quarantined_sources
                )

    def test_only_collated_approved_sources_claim_2011_identity(self) -> None:
        approved = {
            "icel-antiphonary-2010",
            "icel-music-2010",
            "fdlc-mystagogy-2016",
            "fdlc-mystagogy-2012",
        }
        classes = self.record["source_classes"]
        verified = {row["entry_witness"] for row in classes if row["verified_identity"]}
        self.assertEqual(verified, approved)
        source_rows = {row["id"]: row for row in self.overlay["sources"]}
        for row in classes:
            if row["entry_witness"] in approved:
                self.assertEqual(row["identity_relation"], "approved-icel-2011")
                self.assertEqual(
                    row["corpus_disposition"], "quarantined-metadata-only"
                )
                self.assertFalse(row["active_entries"])
                self.assertFalse(row["text_held"])
                self.assertFalse(row["currently_servable"])
                source = source_rows[row["source_record_id"]]
                self.assertEqual(source["rights"], "permission")
                self.assertTrue(source.get("acknowledgement"))
            else:
                self.assertNotEqual(row["identity_relation"], "approved-icel-2011")
        historical_or_project = {"", "cummiskey-1861", "caswall-1849"}
        by_witness = {row["entry_witness"]: row for row in classes}
        for witness in historical_or_project:
            self.assertTrue(by_witness[witness]["currently_servable"])
            self.assertEqual(
                by_witness[witness]["corpus_disposition"], "not-2011-recension"
            )

    def test_unofficial_web_rows_are_not_miscounted_as_verified_2011(self) -> None:
        web = next(
            row
            for row in self.record["source_classes"]
            if row["entry_witness"] == "icel-web-2010"
        )
        self.assertFalse(web["verified_identity"])
        self.assertEqual(web["exemplar_tier"], "unofficial")
        self.assertEqual(web["corpus_disposition"], "removed-hash-only")
        self.assertFalse(web["active_entries"])
        self.assertFalse(web["text_held"])
        self.assertFalse(web["currently_servable"])
        self.assertIn("liturgies.net", web["provenance_issue"])
        self.assertIn("Music for the Roman Missal", web["provenance_issue"])
        rejected = [
            row
            for row in self.overlay.get("untranslated") or []
            if "liturgies-net-2026-08-22" in (row.get("rejected_detectors") or [])
        ]
        self.assertTrue(rejected)
        for row in rejected:
            self.assertNotIn("text", row)
            self.assertTrue(row.get("quarantined_text_sha256"))

    def test_unavailable_ledger_is_typed_unique_and_text_free(self) -> None:
        ledger = self.record["unavailable_ledger"]
        self.assertEqual(
            ledger["record_ref"], f"{self.record['overlay_ref']}#untranslated"
        )
        records = self.overlay.get("untranslated") or []
        identities = []
        reason_kinds = set()
        for row in records:
            self.assertEqual(row["lang"], ledger["language"])
            self.assertEqual(row["availability"], ledger["availability"])
            self.assertNotIn("text", row)
            reason = row.get("reason")
            self.assertIsInstance(reason, dict)
            reason_kinds.add(reason["kind"])
            public = propers.public_untranslated_record(row)
            self.assertEqual(set(public), {"target", "lang", "state"})
            self.assertEqual(
                set(public["target"]), set(ledger["public_target_fields"])
            )
            expected_state = (
                "rights-restricted"
                if reason["kind"] == "rights-withheld"
                else "unavailable"
            )
            self.assertEqual(public["state"], expected_state)
            self.assertEqual(public["lang"], ledger["language"])
            target = public["target"]
            identities.append(
                (
                    target["mass"],
                    target["form_id"],
                    target["proper"],
                    target["cycle"],
                    target["occurrence"],
                    target["extent"],
                )
            )
        self.assertEqual(reason_kinds, set(ledger["reason_kinds"]))
        self.assertEqual(len(identities), len(set(identities)))

    def test_exact_missing_and_unmatched_ledgers_equal_the_live_inventory(self) -> None:
        missing, unmatched = live_slot_sets()
        self.assertEqual(self.record["missing_slots"], [])
        self.assertEqual(self.record["unmatched_records"], [])
        self.assertEqual(missing, set())
        self.assertEqual(unmatched, set())
        summary = propers.english_coverage(propers.DEFAULT_ROOT, "postconciliar")
        self.assertEqual(summary["unaccounted"], len(missing))
        self.assertEqual(summary["unmatched_records"], len(unmatched))
        self.assertEqual(summary["outside_the_ledger"], 0)
        self.assertEqual(summary["stale_translation_records"], 0)

    def test_every_problem_row_has_a_typed_reason_and_known_dependencies(self) -> None:
        dependencies = {row["id"] for row in self.record["dependencies"]}
        self.assertEqual(len(dependencies), len(self.record["dependencies"]))
        ledger = self.record["unavailable_ledger"]
        linked = (
            ledger["no_exemplar_dependencies"]
            + ledger["no_exemplar_special_cases"]
            + ledger["rights_withheld_dependencies"]
        )
        self.assertLessEqual(set(linked), dependencies)
        for row in self.record["missing_slots"]:
            self.assertEqual(row["reason"], "no-current-overlay-record")
            self.assertTrue(row["source_dependencies"])
            self.assertLessEqual(set(row["source_dependencies"]), dependencies)
        for row in self.record["unmatched_records"]:
            self.assertEqual(row["reason"], "form-key-missing")
            self.assertTrue(row["source_dependencies"])
            self.assertLessEqual(set(row["source_dependencies"]), dependencies)


if __name__ == "__main__":
    unittest.main()
