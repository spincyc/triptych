#!/usr/bin/env python3
"""Focused exact-identity and dual-publication tests for translation sidecars."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import tomllib
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


def load_propers():
    path = ROOT / "tools/mass-propers"
    loader = SourceFileLoader("calendar_translation_overlay_propers", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
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
                                            "takes_from": {
                                                "mass": "source",
                                                "proper": "Collect",
                                            },
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
        # Scripture owns occurrence 1, while a reference wrapper owns no body
        # and therefore does not move the composed body's occurrence 2.
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
            ({"surprise": "schema drift"}, "untranslated row has unknown fields"),
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

    def test_unavailable_antecedent_relation_is_complete_and_revised(self) -> None:
        relation = {
            "antecedent_calendar": "roman-1962",
            "antecedent_mass": "pentecost-18",
            "antecedent_proper": "Postcommunion",
            "relation": "revised",
        }
        self.assertEqual(self.problems([self.row(**relation)]), [])
        for field in relation:
            partial = dict(relation)
            del partial[field]
            joined = "\n".join(self.problems([self.row(**partial)]))
            self.assertIn("all-or-none bundle", joined, field)
        joined = "\n".join(
            self.problems([self.row(**{**relation, "relation": "novel"})])
        )
        self.assertIn("must be 'revised'", joined)

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
            ({"incipit": False}, "incipit must be a nonempty string"),
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

        joined = "\n".join(self.problems([], positive={"form": False}))
        self.assertIn("legacy form must be a string", joined)

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


class RuntimePositiveIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.propers = load_propers()
        self.temporary = tempfile.TemporaryDirectory()
        self.sources = Path(self.temporary.name) / "sources"
        self.calendars = self.sources / "calendars"
        self.inventory = self.sources / "inventories"
        self.calendar = self.calendars / "test" / "propers.yaml"
        self.calendar.parent.mkdir(parents=True)
        self.inventory.mkdir(parents=True)
        self.document = {
            "schema": "triptych-calendar-masses/v1",
            "calendar": "test",
            "sections": {
                "seasonal": {
                    "kind": "seasonal",
                    "masses": [
                        {
                            "key": "fixture",
                            "propers": [
                                {
                                    "name": "Cyclic",
                                    "cycles": {
                                        "A": {
                                            "source": "composed",
                                            "incipit": "Cycle A",
                                            "text": "Latin A.",
                                        },
                                        "B": {
                                            "source": "composed",
                                            "incipit": "Cycle B",
                                            "text": "Latin B.",
                                        },
                                    },
                                },
                                {
                                    "name": "Repeat",
                                    "source": "composed",
                                    "text": "Latin first.",
                                },
                                {
                                    "name": "Repeat",
                                    "source": "composed",
                                    "text": "Latin second.",
                                },
                                {
                                    "name": "Legacy",
                                    "source": "composed",
                                    "incipit": "Legacy incipit",
                                    "text": "Latin legacy.",
                                },
                            ],
                        },
                        {
                            "key": "multi",
                            "forms": [
                                {
                                    "id": "stable-form",
                                    "name": "Current label",
                                    "propers": [
                                        {
                                            "name": "Collect",
                                            "source": "composed",
                                            "text": "Latin form.",
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                }
            },
        }
        self.calendar.write_text(
            yaml.safe_dump(self.document, sort_keys=False), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_entries(self, entries: list[dict]) -> None:
        lines = ['schema = "triptych-proper-translations/v1"', 'calendar = "test"']
        for source in entries:
            entry = dict(source)
            english = entry.pop("english")
            rights = entry.pop("translation_rights", "project-created")
            source_id = entry.pop("translation_source_id", None)
            lines.append("[[entries]]")
            for key, value in entry.items():
                if isinstance(value, str):
                    lines.append(f"{key} = {json.dumps(value)}")
                else:
                    lines.append(f"{key} = {value}")
            lines.extend(
                [
                    "[[entries.translations]]",
                    'lang = "en"',
                    f"rights = {json.dumps(rights)}",
                    *(
                        [f"source_id = {json.dumps(source_id)}"]
                        if source_id is not None
                        else []
                    ),
                    f"text = {json.dumps(english)}",
                ]
            )
        (self.inventory / "test-proper-translations-v1.toml").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def test_distinct_cycles_and_occurrences_load_and_merge_exactly(self) -> None:
        self.write_entries(
            [
                {
                    "mass": "fixture", "form_id": "main", "proper": "Cyclic",
                    "cycle": "A", "occurrence": 1, "incipit": "Cycle A",
                    "english": "English A.",
                },
                {
                    "mass": "fixture", "form_id": "main", "proper": "Cyclic",
                    "cycle": "B", "occurrence": 1, "incipit": "Cycle B",
                    "english": "English B.",
                },
                {
                    "mass": "fixture", "form_id": "main", "proper": "Repeat",
                    "cycle": "all", "occurrence": 1, "english": "English first.",
                },
                {
                    "mass": "fixture", "form_id": "main", "proper": "Repeat",
                    "cycle": "all", "occurrence": 2, "english": "English second.",
                },
            ]
        )
        overlay, _, _, _ = self.propers.translation_overlay("test", self.calendars)
        self.assertEqual(
            set(overlay),
            {
                ("fixture", "main", "Cyclic", "A", 1),
                ("fixture", "main", "Cyclic", "B", 1),
                ("fixture", "main", "Repeat", "all", 1),
                ("fixture", "main", "Repeat", "all", 2),
            },
        )
        masses = self.propers._calendars.mass_index(self.document)
        cyclic = masses["fixture"]["propers"][0]
        carried = self.propers.carry_translations(
            "test",
            ("fixture", "", "Cyclic"),
            cyclic,
            overlay,
            [],
            ("fixture", "main", "Cyclic", 1),
        )
        self.assertEqual(
            carried["cycles"]["A"]["translations"][0]["text"], "English A."
        )
        self.assertEqual(
            carried["cycles"]["B"]["translations"][0]["text"], "English B."
        )
        manifest = self.propers.translation_manifest(
            [{"propers": [carried]}], {}
        )
        self.assertEqual(
            [(row["lang"], row["held"], row["composed"]) for row in manifest],
            [("en", 2, 2)],
        )
        for occurrence, expected in ((1, "English first."), (2, "English second.")):
            proper = masses["fixture"]["propers"][occurrence]
            found = self.propers.carry_translations(
                "test",
                ("fixture", "", "Repeat"),
                proper,
                overlay,
                [],
                ("fixture", "main", "Repeat", occurrence),
            )
            self.assertEqual(found["translations"][0]["text"], expected)

    def test_exact_form_id_does_not_need_a_label_but_rejects_a_stale_one(self) -> None:
        exact = {
            "mass": "multi", "form_id": "stable-form", "proper": "Collect",
            "cycle": "all", "occurrence": 1, "english": "English form.",
        }
        self.write_entries([exact])
        overlay, _, _, _ = self.propers.translation_overlay("test", self.calendars)
        self.assertIn(("multi", "stable-form", "Collect", "all", 1), overlay)
        self.assertIsNotNone(
            self.propers.translation_entry_for(
                overlay,
                ("multi", "Current label", "Collect"),
                ("multi", "stable-form", "Collect", 1),
            )
        )

        self.write_entries([{**exact, "form": "Former label"}])
        with self.assertRaisesRegex(ValueError, "has no form labelled"):
            self.propers.translation_overlay("test", self.calendars)

        self.write_entries([{**exact, "form": "Current label"}])
        overlay, _, _, _ = self.propers.translation_overlay("test", self.calendars)
        self.assertIn(("multi", "stable-form", "Collect", "all", 1), overlay)

    def test_legacy_positive_row_is_normalized_to_canonical_identity(self) -> None:
        self.write_entries(
            [
                {
                    "mass": "fixture", "form": "", "proper": "Legacy",
                    "incipit": "Legacy incipit", "english": "Legacy English.",
                }
            ]
        )
        overlay, _, _, _ = self.propers.translation_overlay("test", self.calendars)
        identity = ("fixture", "main", "Legacy", "all", 1)
        self.assertEqual(set(overlay), {identity})
        self.assertIs(
            self.propers.translation_entry_for(
                overlay, ("fixture", "", "Legacy"), identity
            ),
            overlay[identity],
        )

    def test_reference_wrapper_does_not_consume_an_owned_occurrence(self) -> None:
        remote = {
            "key": "remote",
            "propers": [
                {"name": "Collect", "source": "composed", "text": "Remote."}
            ],
        }
        borrowed = {
            "name": "Collect",
            "takes_from": {"mass": "remote", "proper": "Collect"},
        }
        direct = {"name": "Collect", "source": "composed", "text": "Local."}
        local = {"key": "local", "propers": [borrowed, direct]}
        document = {"sections": {"seasonal": {"masses": [remote, local]}}}
        self.assertEqual(
            self.propers.source_slot_identity(document, local, "", direct, None),
            ("local", "main", "Collect", 1),
        )

    def test_runtime_closes_typed_absence_rows_and_reasons(self) -> None:
        row = {
            "mass": "fixture",
            "form_id": "main",
            "proper": "Legacy",
            "cycle": "all",
            "occurrence": 1,
            "extent": "body",
            "lang": "en",
            "availability": "unavailable",
            "reason": {"kind": "no-exemplar"},
            "note": "No exact exemplar is held.",
        }
        self.assertEqual(
            self.propers.untranslated_record_identity(row),
            ("fixture", "main", "Legacy", "all", 1),
        )
        witnessed = {
            **row,
            "witness_artifact_id": "artifact.example.official",
            "witness_passage_id": "passage.example.official.exact-slot",
        }
        self.assertEqual(
            self.propers.untranslated_record_identity(witnessed),
            ("fixture", "main", "Legacy", "all", 1),
        )
        with self.assertRaisesRegex(ValueError, "exact untranslated witness lacks"):
            self.propers.untranslated_record_identity(
                {**row, "witness_passage_id": "passage.example.partial"}
            )
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            self.propers.untranslated_record_identity({**row, "surprise": True})
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            self.propers.untranslated_record_identity(
                {**row, "reason": {"kind": "no-exemplar", "surprise": True}}
            )
        relation = {
            "antecedent_calendar": "roman-1962",
            "antecedent_mass": "pentecost-18",
            "antecedent_proper": "Postcommunion",
            "relation": "revised",
        }
        related = {**row, **relation}
        self.assertEqual(
            self.propers.untranslated_record_identity(related),
            ("fixture", "main", "Legacy", "all", 1),
        )
        self.assertEqual(
            set(self.propers.public_untranslated_record(related)),
            {"target", "lang", "state"},
        )
        with self.assertRaisesRegex(ValueError, "all-or-none bundle"):
            self.propers.untranslated_record_identity(
                {**row, "antecedent_calendar": "roman-1962"}
            )
        with self.assertRaisesRegex(ValueError, "must be 'revised'"):
            self.propers.untranslated_record_identity(
                {**related, "relation": "novel"}
            )
        with self.assertRaisesRegex(ValueError, "legacy translation target form"):
            self.propers.translation_record_identity(
                {"mass": "fixture", "proper": "Legacy", "form": False},
                self.document,
            )

    def test_runtime_rejects_malformed_translation_tables_and_aggregates(self) -> None:
        path = self.inventory / "test-proper-translations-v1.toml"
        for translation, expected in (
            (
                {"lang": "en", "rights": "project-created", "text": False},
                "text must be a nonempty string",
            ),
            (
                {
                    "lang": "en",
                    "rights": "project-created",
                    "text": "English.",
                    "surprise": True,
                },
                "unknown fields",
            ),
            (
                {"lang": "en", "rights": "public-domain", "text": "English."},
                "requires source_id",
            ),
        ):
            with self.subTest(translation=translation):
                with self.assertRaisesRegex(ValueError, expected):
                    self.propers.validate_translation_payload(
                        {"translations": [translation]}, path
                    )

        path.write_text(
            'calendar = "test"\nentries = "not an array"\n', encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "entries must be an array"):
            self.propers.translation_overlay("test", self.calendars)

    def test_exact_artifact_source_alias_carries_witness_rights_and_label(self) -> None:
        artifact_id = "artifact.example.exact-expression"
        edition_id = "edition.example.work"
        entry = {
            "mass": "fixture",
            "form_id": "main",
            "proper": "Legacy",
            "cycle": "all",
            "occurrence": 1,
            "translation_rights": "public-domain",
            "translation_source_id": artifact_id,
            "english": "Exact expression English.",
        }
        self.write_entries([entry])
        sidecar = self.inventory / "test-proper-translations-v1.toml"
        sidecar.write_text(
            sidecar.read_text(encoding="utf-8")
            + "\n".join(
                [
                    "[[sources]]",
                    'id = "example"',
                    f"source_id = {json.dumps(edition_id)}",
                    f"artifact_id = {json.dumps(artifact_id)}",
                    'label = "Exact expression witness"',
                    'rights = "public-domain"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        overlay, _, _, witnesses = self.propers.translation_overlay(
            "test", self.calendars
        )
        self.assertIs(witnesses[edition_id], witnesses[artifact_id])
        manifest = self.propers.translation_manifest(
            [
                {
                    "propers": [
                        {
                            "name": "Legacy",
                            "text": "Latin legacy.",
                            "translations": next(iter(overlay.values()))["translations"],
                        }
                    ]
                }
            ],
            witnesses,
        )
        self.assertEqual(manifest[0]["label"], "Exact expression witness")

        bad = sidecar.read_text(encoding="utf-8").replace(
            'rights = "public-domain"',
            'rights = "permission"\nnotice = "Granted."',
            1,
        )
        sidecar.write_text(bad, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "do not match translation source"):
            self.propers.translation_overlay("test", self.calendars)

        self.write_entries([{**entry, "translation_source_id": "artifact.missing"}])
        with self.assertRaisesRegex(ValueError, "has no translation source row"):
            self.propers.translation_overlay("test", self.calendars)


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

    def test_positive_public_domain_antecedent_body_cannot_omit_binding(self) -> None:
        unbound = copy.deepcopy(self.entry)
        unbound["witness_relation"] = "antecedent"
        for field in self.checker.OVERLAY_PUBLICATION_FIELDS:
            del unbound[field]
        joined = "\n".join(
            self.checker.overlay_entry_publication_problems("entry", unbound)
        )
        self.assertIn(
            "positive public-domain antecedent body requires an exact publication binding",
            joined,
        )

        unbound["translations"][0]["rights"] = "permission"
        self.assertEqual(
            self.checker.overlay_entry_publication_problems("entry", unbound), []
        )

    def test_json_encoded_multiline_capable_body_is_exactly_decoded(self) -> None:
        self.payload.write_text(
            'id\tenglish_json\nfixture\t"""Exact body."""\n',
            encoding="utf-8",
        )
        digest = hashlib.sha256(self.payload.read_bytes()).hexdigest()
        self.entry["publication_artifact_sha256"] = digest
        self.records[self.publication_artifact_id].data["sha256"] = digest
        self.records[self.publication_passage_id].data["artifact_sha256"] = digest
        self.assertEqual(
            self.checker.overlay_entry_publication_problems("entry", self.entry), []
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


class RecoveredCummiskeyAntecedentProductionTests(unittest.TestCase):
    INVENTORY = (
        ROOT / "src/sources/inventories/postconciliar-proper-translations-v1.toml"
    )
    PUBLICATION_ARTIFACT = (
        "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861."
        "postconciliar-antecedent-orations-en"
    )
    BOUND = {
        ("ot-5", "Collect"),
        ("ot-3", "Prayer after Communion"),
        ("ot-2", "Prayer over the Offerings"),
        ("ot-6", "Prayer after Communion"),
        ("most-holy-name-jesus", "Collect"),
        ("most-holy-name-jesus", "Prayer over the Offerings"),
        ("most-holy-name-jesus", "Prayer after Communion"),
        ("saints-sixtus-ii-pope-companions-martyrs", "Prayer over the Offerings"),
        ("saint-wenceslaus-martyr", "Collect"),
        ("saint-hedwig-religious", "Collect"),
        ("saint-margaret-scotland", "Collect"),
        ("epiphany-lord", "Collect"),
        ("epiphany-lord", "Prayer over the Offerings"),
        ("epiphany-lord", "Prayer after Communion"),
        ("saint-george-martyr", "Collect"),
        ("saint-george-martyr", "Prayer over the Offerings"),
        ("saint-george-martyr", "Prayer after Communion"),
        ("saint-jerome-emiliani", "Collect"),
        ("saint-jerome-emiliani", "Prayer over the Offerings"),
        ("saint-jerome-emiliani", "Prayer after Communion"),
        ("saint-apollinaris-bishop-martyr", "Collect"),
        ("saint-apollinaris-bishop-martyr", "Prayer over the Offerings"),
        ("saint-apollinaris-bishop-martyr", "Prayer after Communion"),
        ("saint-louis", "Collect"),
        ("saint-louis", "Prayer over the Offerings"),
        ("saint-louis", "Prayer after Communion"),
        ("most-holy-name-mary", "Collect"),
    }
    QUARANTINED = {
        ("advent-4", "Collect"),
        ("mary-mother-of-god", "Collect"),
        ("ot-25", "Entrance Antiphon"),
        ("ot-31", "Prayer after Communion"),
        ("mary-holy-mother-god", "Collect"),
        ("saint-raymond-penyafort-priest", "Collect"),
        ("saint-anthony-abbot", "Collect"),
        ("saint-anthony-abbot", "Prayer over the Offerings"),
        ("saint-anthony-abbot", "Prayer after Communion"),
        ("saint-paulinus-nola-bishop", "Collect"),
        ("saint-paulinus-nola-bishop", "Prayer over the Offerings"),
        ("saint-paulinus-nola-bishop", "Prayer after Communion"),
        ("saints-sixtus-ii-pope-companions-martyrs", "Collect"),
        ("saints-sixtus-ii-pope-companions-martyrs", "Prayer after Communion"),
        ("most-holy-name-mary", "Prayer over the Offerings"),
        ("most-holy-name-mary", "Prayer after Communion"),
    }

    def setUp(self) -> None:
        with self.INVENTORY.open("rb") as handle:
            self.data = tomllib.load(handle)

    @staticmethod
    def key(row: dict) -> tuple[str, str]:
        return row["mass"], row["proper"]

    def test_all_43_recovered_candidates_are_bound_or_text_free(self) -> None:
        positives = {self.key(row): row for row in self.data["entries"]}
        gaps = {self.key(row): row for row in self.data["untranslated"]}
        self.assertEqual(len(self.BOUND), 27)
        self.assertEqual(len(self.QUARANTINED), 16)
        for key in self.BOUND:
            self.assertIn(key, positives)
            self.assertNotIn(key, gaps)
            row = positives[key]
            self.assertEqual(row["publication_artifact_id"], self.PUBLICATION_ARTIFACT)
            self.assertEqual(len(row["translations"]), 1)
            self.assertEqual(row["translations"][0]["rights"], "public-domain")
            for field in (
                "artifact_id",
                "passage_id",
                "ia_leaf_range",
                "publication_artifact_sha256",
                "publication_passage_id",
            ):
                self.assertTrue(row.get(field), (key, field))
        for key in self.QUARANTINED:
            self.assertNotIn(key, positives)
            self.assertIn(key, gaps)
            self.assertEqual(gaps[key]["availability"], "unavailable")
            self.assertEqual(gaps[key]["reason"]["kind"], "no-exemplar")
            self.assertNotIn("text", gaps[key])

    def test_overbroad_ot25_page_proof_survives_without_a_body(self) -> None:
        proof = (
            ROOT
            / "src/sources/works/eugene-cummiskey/roman-missal-english-laity/"
            "editions/philadelphia-1861/passages/"
            "verify--post-pentecosten-19--introit.toml"
        )
        with proof.open("rb") as handle:
            record = tomllib.load(handle)
        self.assertEqual(record["artifact_page_ranges"], [[454, 455]])
        self.assertIn("printed pp. 445-446", record["context"])
        self.assertEqual(record["states"][-2:], ["inspected", "verified"])


if __name__ == "__main__":
    unittest.main()
