#!/usr/bin/env python3
"""Focused exact-identity and dual-publication tests for translation sidecars."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from types import SimpleNamespace

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_checker():
    path = ROOT / "tools/check-calendar-masses"
    loader = SourceFileLoader("calendar_translation_overlay_checker", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


def record(record_type: str, **data):
    return SimpleNamespace(record_type=record_type, data=data)


class ExactUntranslatedSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_checker()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.inventory = self.root / "inventories"
        self.inventory.mkdir()
        self.calendar = self.root / "test" / "propers.yaml"
        self.calendar.parent.mkdir()
        self.calendar.write_text(
            yaml.safe_dump(
                {
                    "sections": {
                        "seasonal": {
                            "kind": "seasonal",
                            "masses": [
                                {
                                    "key": "fixture",
                                    "propers": [
                                        {
                                            "name": "Collect",
                                            "source": "scripture",
                                            "incipit": "First incipit",
                                            "verses": ["Ps 1:1"],
                                        },
                                        {
                                            "name": "Collect",
                                            "source": "composed",
                                            "incipit": "Second incipit",
                                            "text": "Second body.",
                                        },
                                        {
                                            "name": "Placeholder",
                                            "source": "composed",
                                            "text": "Not liturgical text.",
                                        },
                                        {
                                            "name": "Cyclic",
                                            "cycles": {
                                                "A": {
                                                    "source": "composed",
                                                    "incipit": "Cycle A",
                                                    "text": "A body.",
                                                },
                                                "B": {
                                                    "source": "composed",
                                                    "incipit": "Cycle B",
                                                    "text": "B body.",
                                                },
                                            },
                                        },
                                        {
                                            "name": "Held",
                                            "source": "composed",
                                            "incipit": "Held incipit",
                                            "text_status": {
                                                "state": "unavailable",
                                                "scope": "proper-body",
                                            },
                                        },
                                        {
                                            "name": "No Incipit",
                                            "source": "composed",
                                            "text": "A body without an indexed incipit.",
                                        },
                                    ],
                                }
                            ],
                        }
                    }
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        self.checker.OVERLAY_DIR = self.inventory
        self.checker.act_history = lambda: ()
        self.checker._SOURCE_RECORDS = ({}, None)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def row(**changes):
        row = {
            "mass": "fixture",
            "form_id": "main",
            "proper": "Collect",
            "cycle": "all",
            "occurrence": 2,
            "extent": "body",
            "lang": "en",
            "availability": "unavailable",
            "reason": {"kind": "no-exemplar"},
            "note": "The exact source exemplar has not been acquired.",
        }
        row.update(changes)
        return row

    def write_sidecar(self, rows, *, positive: bool | dict = False) -> None:
        lines = ['schema = "triptych-proper-translations/v1"', 'calendar = "test"']
        if positive:
            entry = {"mass": "fixture", "form": "", "proper": "Held"}
            if isinstance(positive, dict):
                entry.update(positive)
            lines.append("[[entries]]")
            for key, value in entry.items():
                if isinstance(value, str):
                    lines.append(f"{key} = {json.dumps(value)}")
                elif isinstance(value, bool):
                    lines.append(f"{key} = {'true' if value else 'false'}")
                else:
                    lines.append(f"{key} = {value}")
            lines.extend(
                [
                    "[[entries.translations]]",
                    'lang = "en"',
                    'rights = "project-created"',
                    'text = "Second body."',
                ]
            )
        for row in rows:
            reason = row.get("reason")
            lines.append("[[untranslated]]")
            for key, value in row.items():
                if key == "reason":
                    continue
                if isinstance(value, str):
                    lines.append(f"{key} = {json.dumps(value)}")
                elif isinstance(value, bool):
                    lines.append(f"{key} = {'true' if value else 'false'}")
                else:
                    lines.append(f"{key} = {value}")
            if isinstance(reason, dict):
                lines.append("[untranslated.reason]")
                for key, value in reason.items():
                    if isinstance(value, list):
                        lines.append(
                            f"{key} = [{', '.join(json.dumps(one) for one in value)}]"
                        )
                    else:
                        lines.append(f"{key} = {json.dumps(value)}")
            elif reason is not None:
                lines.append(f"reason = {json.dumps(reason)}")
        (self.inventory / "test-proper-translations-v1.toml").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def problems(self, rows, *, positive: bool | dict = False):
        self.write_sidecar(rows, positive=positive)
        return self.checker.overlay_problems([self.calendar])[0]

    def test_required_exact_fields_have_no_legacy_defaults(self) -> None:
        self.assertEqual(self.problems([self.row()]), [])
        for field in (
            "mass",
            "form_id",
            "proper",
            "cycle",
            "occurrence",
            "extent",
            "lang",
            "availability",
            "reason",
            "note",
        ):
            row = self.row()
            del row[field]
            joined = "\n".join(self.problems([row]))
            self.assertIn("legacy defaults are not accepted", joined, field)

        joined = "\n".join(self.problems([self.row(form="Main")]))
        self.assertIn("legacy form labels are forbidden", joined)

    def test_raw_occurrence_cycle_surface_and_placeholder_identity(self) -> None:
        # Scripture still consumes occurrence 1, so the composed body is 2.
        self.assertEqual(self.problems([self.row(occurrence=2)]), [])
        joined = "\n".join(self.problems([self.row(occurrence=1)]))
        self.assertIn("target owns no body", joined)

        self.assertEqual(
            self.problems(
                [self.row(proper="Cyclic", cycle="A", occurrence=1)]
            ),
            [],
        )
        joined = "\n".join(
            self.problems([self.row(proper="Cyclic", cycle="all", occurrence=1)])
        )
        self.assertIn("no source-owned proper", joined)

        joined = "\n".join(
            self.problems([self.row(proper="Placeholder", occurrence=1)])
        )
        self.assertIn("Placeholder is not a translatable", joined)

        self.assertEqual(
            self.problems([self.row(proper="Held", occurrence=1)]), []
        )

    def test_extent_duplicate_and_positive_collision_use_full_claim(self) -> None:
        incipit = self.row(
            extent="incipit", incipit="Second incipit", occurrence=2
        )
        self.assertEqual(self.problems([incipit]), [])
        # Body and incipit are separate claims; an identical claim is not.
        self.assertEqual(self.problems([self.row(), incipit]), [])
        joined = "\n".join(self.problems([self.row(), self.row()]))
        self.assertIn("duplicate exact untranslated claims", joined)

        joined = "\n".join(
            self.problems(
                [self.row(proper="Held", occurrence=1)], positive=True
            )
        )
        self.assertIn("both translated and unavailable", joined)
        self.assertEqual(self.problems([incipit], positive=True), [])

    def test_tokens_and_typed_reason_are_closed(self) -> None:
        for changes, expected in (
            ({"occurrence": True}, "positive one-based integer"),
            ({"cycle": "Z"}, "cycle must be one of"),
            ({"extent": "summary"}, "extent must be one of"),
            ({"lang": "la"}, "requires lang = 'en'"),
            ({"availability": "unknown"}, "availability must be one of"),
            ({"reason": "unavailable"}, "reason must be a table"),
            (
                {"reason": {"kind": "no-exemplar", "source_id": "edition.x"}},
                "cannot name source_id",
            ),
            (
                {"reason": {"kind": "witness-gap"}},
                "requires source_id",
            ),
            (
                {"reason": {"kind": "no-exemplar", "surfaces": ["download"]}},
                "applies only to rights-withheld",
            ),
        ):
            with self.subTest(changes=changes):
                joined = "\n".join(self.problems([self.row(**changes)]))
                self.assertIn(expected, joined)

    def test_positive_entries_join_exact_live_body_identity(self) -> None:
        exact = {
            "form_id": "main",
            "proper": "Collect",
            "cycle": "all",
            "occurrence": 2,
        }
        self.assertEqual(self.problems([], positive=exact), [])

        for changes, expected in (
            ({"occurrence": True}, "positive one-based integer"),
            ({"occurrence": 0}, "positive one-based integer"),
            ({"occurrence": 1}, "owns no composed body"),
            ({"mass": "missing"}, "translation target"),
        ):
            with self.subTest(changes=changes):
                joined = "\n".join(
                    self.problems([], positive={**exact, **changes})
                )
                self.assertIn(expected, joined)

        joined = "\n".join(
            self.problems(
                [],
                positive={"mass": "missing", "form": "", "proper": "Held"},
            )
        )
        self.assertIn("does not exist on source mass", joined)

    def test_repeated_legacy_target_is_ambiguous(self) -> None:
        joined = "\n".join(
            self.problems([], positive={"proper": "Collect"})
        )
        self.assertIn("legacy translation target", joined)
        self.assertIn("is ambiguous", joined)

    def test_legacy_incipit_can_supply_an_absent_target_value_but_exact_is_strict(self) -> None:
        legacy = {
            "proper": "No Incipit",
            "incipit": "Recorded only by the translation witness",
        }
        self.assertEqual(self.problems([], positive=legacy), [])
        exact = {
            **legacy,
            "form_id": "main",
            "cycle": "all",
            "occurrence": 1,
        }
        self.assertTrue(
            any("does not match exact target" in one for one in self.problems([], positive=exact))
        )

    def test_malformed_cycle_does_not_crash_overlay_join(self) -> None:
        document = yaml.safe_load(self.calendar.read_text(encoding="utf-8"))
        propers = document["sections"]["seasonal"]["masses"][0]["propers"]
        cyclic = next(proper for proper in propers if proper["name"] == "Cyclic")
        cyclic["cycles"] = ["not-a-mapping"]
        self.calendar.write_text(
            yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
        )
        owned: list[str] = []
        self.checker.check_file(self.calendar, owned)
        self.assertTrue(any("cycles must be a nonempty mapping" in one for one in owned))
        self.assertEqual(self.problems([]), [])


class PublicationBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_checker()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.payload = self.root / "publish.tsv"
        self.payload.write_text("id\tenglish\nfixture\tExact body.\n", encoding="utf-8")
        self.edition_id = "edition.cummiskey.1861"
        self.page_artifact_id = "artifact.cummiskey.scan"
        self.page_passage_id = "passage.cummiskey.verify"
        self.publication_artifact_id = "artifact.cummiskey.publish"
        self.publication_passage_id = "passage.cummiskey.publish"
        self.digest = hashlib.sha256(self.payload.read_bytes()).hexdigest()
        self.records = {
            self.edition_id: record("edition", date="1861"),
            self.page_artifact_id: record(
                "artifact", edition_id=self.edition_id, sha256="b" * 64,
                storage="remote", rights_status="unresolved"
            ),
            self.page_passage_id: record(
                "passage", edition_id=self.edition_id,
                artifact_id=self.page_artifact_id, artifact_sha256="b" * 64,
                artifact_page_ranges=[[6, 6]], states=["inspected", "verified"],
                verified_on="2026-08-26", context="Exact body, printed p. 505."
            ),
            self.publication_artifact_id: record(
                "artifact", edition_id=self.edition_id, sha256=self.digest,
                storage="tracked", indexable=True, encoding="utf-8",
                media_type="text/tab-separated-values; charset=utf-8",
                rights_status="public-domain", rights_jurisdiction="United States",
                path=str(self.payload),
            ),
            self.publication_passage_id: record(
                "passage", edition_id=self.edition_id,
                artifact_id=self.publication_artifact_id,
                artifact_sha256=self.digest, physical_line_ranges=[[2, 2]],
                states=["inspected", "verified"], verified_on="2026-08-26",
            ),
        }
        self.checker._SOURCE_RECORDS = (self.records, None)
        self.entry = {
            "artifact_id": self.page_artifact_id,
            "passage_id": self.page_passage_id,
            "ia_leaf": 5,
            "ia_leaf_range": [5, 5],
            "printed_page": "505",
            "witness": "cummiskey-1861",
            "publication_artifact_id": self.publication_artifact_id,
            "publication_artifact_sha256": self.digest,
            "publication_passage_id": self.publication_passage_id,
            "translations": [
                {
                    "lang": "en",
                    "rights": "public-domain",
                    "source_id": self.edition_id,
                    "text": "Exact body.",
                }
            ],
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_dual_binding_keeps_remote_page_proof_separate(self) -> None:
        self.assertEqual(
            self.checker.overlay_entry_publication_problems("entry", self.entry), []
        )
        witnesses = {
            "cummiskey-1861": {
                "source_id": self.edition_id,
                "rights": "public-domain",
                "artifact_id": self.page_artifact_id,
                "caution": "The remote scan verifies the reading; it is not published.",
            }
        }
        self.assertEqual(
            self.checker.overlay_entry_source_problems(
                "entry", self.entry, witnesses
            ),
            [],
        )

    def test_collated_claim_requires_exact_page_image_binding(self) -> None:
        witnesses = {
            "cummiskey-1861": {
                "source_id": self.edition_id,
                "rights": "public-domain",
                "artifact_id": self.page_artifact_id,
            }
        }
        unbound = {
            "collated": "page-image, 2026-08-26",
            "witness": "cummiskey-1861",
        }
        joined = "\n".join(
            self.checker.overlay_entry_source_problems("entry", unbound, witnesses)
        )
        for field in (
            self.checker.OVERLAY_ARTIFACT,
            self.checker.OVERLAY_PASSAGE,
            self.checker.OVERLAY_IA_LEAF_RANGE,
        ):
            self.assertIn(f"collated page-image claim also requires {field}", joined)

        self.assertEqual(
            self.checker.overlay_entry_source_problems(
                "entry",
                {"witness": "cummiskey-1861"},
                witnesses,
            ),
            [],
        )

    def test_atomic_triple_hash_line_and_exact_body_mutations_fail(self) -> None:
        for field in self.checker.OVERLAY_PUBLICATION_FIELDS:
            changed = copy.deepcopy(self.entry)
            del changed[field]
            joined = "\n".join(
                self.checker.overlay_entry_publication_problems("entry", changed)
            )
            self.assertIn("publication binding also requires", joined, field)

            changed = copy.deepcopy(self.entry)
            changed[field] = ""
            joined = "\n".join(
                self.checker.overlay_entry_publication_problems("entry", changed)
            )
            self.assertTrue(
                "must be a nonempty" in joined
                or "64 lowercase hexadecimal" in joined,
                (field, joined),
            )

        changed = copy.deepcopy(self.entry)
        changed["publication_artifact_sha256"] = "c" * 64
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", changed)
        )
        self.assertIn("does not match the named publication artifact", joined)

        self.records[self.publication_artifact_id].data["storage"] = "remote"
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", self.entry)
        )
        self.assertIn("publication artifact must be tracked", joined)
        self.records[self.publication_artifact_id].data["storage"] = "tracked"

        self.records[self.publication_passage_id].data["states"] = ["verified"]
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", self.entry)
        )
        self.assertIn("inspected and dated verified", joined)
        self.records[self.publication_passage_id].data["states"] = [
            "inspected",
            "verified",
        ]

        self.records[self.publication_passage_id].data["physical_line_ranges"] = [[1, 1]]
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", self.entry)
        )
        self.assertIn("exactly one TSV data line", joined)
        self.records[self.publication_passage_id].data["physical_line_ranges"] = [[2, 2]]

        changed = copy.deepcopy(self.entry)
        changed["translations"][0]["text"] = "Exact body!"
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", changed)
        )
        self.assertIn("does not exactly equal", joined)


if __name__ == "__main__":
    unittest.main()
