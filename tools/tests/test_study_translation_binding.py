"""Study English stays bound to the exact, publishable Latin it translates."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_tool(name):
    loader = SourceFileLoader("study_binding_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


class StudyTranslationBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool("mass-propers")

    def setUp(self):
        self.text = "Da nobis, quaesumus, Domine, pacem. Per Dominum.\n"
        self.passage = "passage.fixture.missal.historical.collect"
        self.rights_source = "artifact.fixture.missal.historical.text"
        # English occurrence two is Latin occurrence one: the preceding
        # Scripture-owned slot has no direct Latin body or provenance row.
        self.document = {
            "schema": "triptych-calendar-masses/v1", "calendar": "test",
            "edition": "Test edition", "psalm_numbering": "vulgate",
            "sections": {"seasonal": {"kind": "seasonal", "masses": [{
                "key": "day", "name": "Test day", "registry": "test",
                "propers": [
                    {"name": "Collect", "source": "scripture", "verses": []},
                    {"name": "Collect", "source": "composed", "text": self.text},
                ],
            }]}},
        }
        self.records = {self.tool.LatinKey("day", "", "Collect", occurrence=1): {
            "text_sha256": self.digest(self.text), "provenance_status": "collated",
            "publication_status": "permitted", "publication_basis": "public-domain",
            "surfaces": sorted(self.tool.SURFACES), "source_id": self.passage,
            "publication_source_ids": [self.rights_source],
        }}
        self.sources = {
            self.passage: {"record_type": "passage"},
            self.rights_source: {"record_type": "artifact", "rights_status": "public-domain"},
            "passage.fixture.missal.historical.other": {"record_type": "passage"},
            "artifact.fixture.missal.historical.other": {"record_type": "artifact"},
        }
        self.entry = {
            "mass": "day", "form_id": "main", "proper": "Collect",
            "cycle": "all", "occurrence": 2,
            "source_latin_sha256": self.digest(self.text),
            "source_latin_passage_id": self.passage,
            "source_latin_publication_source_ids": [self.rights_source],
            "translations": [{"lang": "en", "rights": "project-created",
                              "text": "Grant us peace, we pray, O Lord. Through the Lord."}],
        }

    @staticmethod
    def digest(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @property
    def context(self):
        return self.document, self.records, self.sources

    def validate(self, entry=None):
        self.tool.validate_study_translation_binding(
            self.entry if entry is None else entry, "test", Path("unused"),
            Path("test-sidecar.toml"), context=self.context,
        )

    def test_exact_source_and_distinct_english_latin_ordinals_pass_without_mutation(self):
        before = copy.deepcopy((self.entry, self.context))
        self.validate()
        self.assertEqual((self.entry, self.context), before)

    def test_legacy_unbound_study_does_not_acquire_a_new_source_claim(self):
        entry = {key: value for key, value in self.entry.items()
                 if key not in self.tool.STUDY_TRANSLATION_SOURCE_FIELDS}
        with mock.patch.object(self.tool, "study_translation_source_context", side_effect=AssertionError("unbound legacy")):
            self.tool.validate_study_translation_binding(entry, "test", Path("unused"), Path("test"))

    def test_partial_binding_is_rejected_for_each_missing_field(self):
        for field in self.tool.STUDY_TRANSLATION_SOURCE_FIELDS:
            with self.subTest(field=field):
                entry = copy.deepcopy(self.entry)
                entry.pop(field)
                with self.assertRaisesRegex(ValueError, "partial study translation source binding"):
                    self.validate(entry)

    def test_invalid_hash_is_rejected(self):
        for value in ("A" * 64, "abc", None, 7):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "source_latin_sha256"):
                    self.validate(dict(self.entry, source_latin_sha256=value))

    def test_changed_latin_is_rejected_even_when_its_provenance_was_updated(self):
        changed = self.text.replace("pacem", "gratiam")
        self.document["sections"]["seasonal"]["masses"][0]["propers"][1]["text"] = changed
        next(iter(self.records.values()))["text_sha256"] = self.digest(changed)
        with self.assertRaisesRegex(ValueError, "source Latin hash is stale"):
            self.validate()

    def test_stale_latin_provenance_cannot_be_used_as_translation_authority(self):
        self.document["sections"]["seasonal"]["masses"][0]["propers"][1]["text"] += "Amen."
        with self.assertRaisesRegex(ValueError, "complete publishable Latin source body"):
            self.validate()

    def test_wrong_registered_passage_is_rejected(self):
        self.entry["source_latin_passage_id"] = "passage.fixture.missal.historical.other"
        with self.assertRaisesRegex(ValueError, "passage differs"):
            self.validate()

    def test_nonpassage_and_missing_passage_are_rejected(self):
        for record in ({"record_type": "artifact"}, None):
            with self.subTest(record=record):
                if record is None:
                    self.sources.pop(self.passage, None)
                else:
                    self.sources[self.passage] = record
                with self.assertRaisesRegex(ValueError, "passage differs"):
                    self.validate()

    def test_wrong_registered_publication_source_is_rejected(self):
        self.entry["source_latin_publication_source_ids"] = ["artifact.fixture.missal.historical.other"]
        with self.assertRaisesRegex(ValueError, "publication sources differ"):
            self.validate()

    def test_invalid_source_lists_are_rejected(self):
        for value in ([], [self.rights_source, self.rights_source], [None], [""], self.rights_source):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "nonempty unique source ids"):
                    self.validate(dict(self.entry, source_latin_publication_source_ids=value))

    def test_unregistered_publication_source_is_rejected(self):
        self.sources.pop(self.rights_source)
        with self.assertRaisesRegex(ValueError, "publication sources differ"):
            self.validate()

    def test_latin_must_be_permitted_for_all_translation_surfaces(self):
        for missing in self.tool.SURFACES:
            with self.subTest(surface=missing):
                next(iter(self.records.values()))["surfaces"] = sorted(self.tool.SURFACES - {missing})
                with self.assertRaisesRegex(ValueError, "complete publishable Latin source body"):
                    self.validate()

    def test_withheld_latin_body_cannot_be_translated_through_the_study_route(self):
        next(iter(self.records.values()))["publication_status"] = "withheld"
        with self.assertRaisesRegex(ValueError, "complete publishable Latin source body"):
            self.validate()

    def test_missing_latin_body_cannot_be_reconstructed_from_a_binding(self):
        self.document["sections"]["seasonal"]["masses"][0]["propers"][1].pop("text")
        with self.assertRaisesRegex(ValueError, "complete publishable Latin source body"):
            self.validate()

    def test_permission_to_display_modern_latin_does_not_authorize_a_new_translation(self):
        for basis in ("permission", "licensed", "project-created", "unreviewed-method"):
            with self.subTest(basis=basis):
                next(iter(self.records.values()))["publication_basis"] = basis
                with self.assertRaises(ValueError):
                    self.validate()

    def test_arbitrary_qualified_basis_cannot_invent_an_adopted_method(self):
        next(iter(self.records.values()))["publication_basis"] = "qualified-nonoriginal-adaptation"
        with self.assertRaisesRegex(ValueError, "qualified Latin authority"):
            self.validate()

    def test_qualified_authority_is_selected_by_the_exact_source_row(self):
        source = next(iter(self.records.values()))
        source["publication_basis"] = "qualified-nonoriginal-adaptation"
        qualified = self.tool._proper_qualified_latin
        with mock.patch.object(qualified, "source_problems", return_value=[]), \
                mock.patch.object(qualified, "authority_problems", return_value=["successor adoption missing"]) as authority:
            with self.assertRaisesRegex(ValueError, "successor adoption missing"):
                self.validate()
        self.assertIs(authority.call_args.kwargs["row"], source)

    def test_public_qualified_metadata_uses_only_its_exact_scope_and_notice(self):
        qualified = self.tool._proper_qualified_latin
        for scope in qualified.SCOPES:
            latin = {
                "text_sha256": scope["body_sha256"],
                "provenance": {"source_id": scope["source_id"], "status": "collated"},
                "publication": {"basis": qualified.BASIS, "status": "permitted",
                                "surfaces": sorted(self.tool.SURFACES)},
                "withheld": False,
            }
            projected = self.tool.public_latin_state(latin, "Collect")
            owned = qualified.public_scope(latin)
            self.assertEqual(projected["publication"]["source_ids"], [owned["artifact_id"]])
            self.assertEqual(projected["publication"]["notice"], owned["notice"])
            changed = copy.deepcopy(latin)
            changed["text_sha256"] = "0" * 64
            self.assertTrue(self.tool.public_latin_state(changed, "Collect")["withheld"])

    def test_uncollated_latin_is_not_a_bound_study_source(self):
        next(iter(self.records.values()))["provenance_status"] = "identified"
        with self.assertRaisesRegex(ValueError, "collated public-domain"):
            self.validate()

    def test_inherited_english_refuses_changed_child_latin_with_the_same_incipit(self):
        source = self.document["sections"]["seasonal"]["masses"][0]["propers"][1]
        source["incipit"] = "Da nobis"
        entry = dict(self.entry, incipit="Da nobis")
        identity = ("day", "main", "Collect", 2)
        overlay = {("day", "main", "Collect", "all", 2): entry}
        stale = []
        same = self.tool.carry_translations("child", ("day", "", "Collect"), source, overlay, stale, identity)
        self.assertEqual(same["translations"], entry["translations"])
        self.assertEqual(stale, [])
        self.assertTrue(self.tool.translation_answers(entry, source, "en"))
        changed = dict(source, text=self.text.replace("pacem", "gratiam"))
        carried = self.tool.carry_translations("child", ("day", "", "Collect"), changed, overlay, stale, identity)
        self.assertNotIn("translations", carried)
        self.assertFalse(self.tool.translation_answers(entry, changed, "en"))
        self.assertEqual(len(stale), 1)
        self.assertIn("effective Proper body", stale[0])

    def test_project_study_label_is_carried_without_a_false_human_source_id(self):
        source = self.document["sections"]["seasonal"]["masses"][0]["propers"][1]
        overlay = {("day", "main", "Collect", "all", 2): self.entry}
        carried = self.tool.carry_translations(
            "test", ("day", "", "Collect"), source, overlay, [],
            ("day", "main", "Collect", 2),
            {"": {"label": "Triptych study English", "caution": "Original study translation."}},
        )
        translation = carried["translations"][0]
        self.assertEqual(translation["source_label"], "Triptych study English")
        self.assertEqual(translation["caution"], "Original study translation.")
        self.assertNotIn("source_id", translation)
        chosen = self.tool.select_texts(carried, "en", None)
        self.assertEqual(chosen[0][1], "Triptych study English")
        self.assertEqual(chosen[0][0], self.entry["translations"][0]["text"])

    def test_cannot_relabel_a_human_translation_as_bound_project_work(self):
        for change in ({"rights": "public-domain"}, {"source_id": self.passage}, {"source_id": None}):
            with self.subTest(change=change):
                entry = copy.deepcopy(self.entry)
                entry["translations"][0].update(change)
                with self.assertRaisesRegex(ValueError, "project-created translation without source_id"):
                    self.validate(entry)

    def test_no_same_word_guess_for_a_missing_occurrence_or_form(self):
        for change in ({"occurrence": 3}, {"form_id": "missing"}, {"cycle": "A"}, {"mass": "missing"}):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    self.validate(dict(self.entry, **change))

    def test_stable_form_and_cycle_select_their_exact_body(self):
        mass = self.document["sections"]["seasonal"]["masses"][0]
        mass.pop("propers")
        mass["forms"] = [{"id": "first", "name": "First Mass", "propers": [{
            "name": "Collect", "cycles": {
                "A": {"source": "composed", "text": self.text},
                "B": {"source": "composed", "text": "Another prayer."},
            },
        }]}]
        source = next(iter(self.records.values()))
        self.records = {self.tool.LatinKey("day", "First Mass", "Collect", "cycles", "A", 1): source}
        entry = dict(self.entry, form_id="first", cycle="A", occurrence=1)
        self.validate(entry)
        with self.assertRaisesRegex(ValueError, "complete publishable Latin source body"):
            self.validate(dict(entry, cycle="B"))

    def write_fixture(self, base):
        calendar_root = base / "calendars"
        calendar = calendar_root / "test" / "propers.yaml"
        calendar.parent.mkdir(parents=True)
        calendar.write_text(yaml.safe_dump(self.document, sort_keys=False))
        inventory = base / "inventories"
        inventory.mkdir()
        fields = {key: value for key, value in self.entry.items() if key != "translations"}
        content = ['calendar = "test"', '[[entries]]']
        content.extend(f"{key} = {json.dumps(value)}" for key, value in fields.items())
        content.append("[[entries.translations]]")
        content.extend(f"{key} = {json.dumps(value)}" for key, value in self.entry["translations"][0].items())
        (inventory / "test-proper-translations-v1.toml").write_text("\n".join(content) + "\n")
        return calendar_root, calendar, inventory

    def test_overlay_and_cli_refuse_stale_binding_before_emitting_english(self):
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            calendar_root, _, _ = self.write_fixture(Path(directory))
            with mock.patch.object(self.tool, "study_translation_source_context", return_value=self.context):
                overlay, _, _, _ = self.tool.translation_overlay("test", calendar_root)
                self.assertEqual(overlay[tuple(self.entry[key] for key in ("mass", "form_id", "proper", "cycle", "occurrence"))], self.entry)
                changed = self.text.replace("pacem", "gratiam")
                self.document["sections"]["seasonal"]["masses"][0]["propers"][1]["text"] = changed
                next(iter(self.records.values()))["text_sha256"] = self.digest(changed)
                with self.assertRaisesRegex(ValueError, "source Latin hash is stale"):
                    self.tool.translation_overlay("test", calendar_root)
                out, error = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(error):
                    status = self.tool.main(["--root", str(calendar_root), "--calendar", "test",
                                             "--mass", "day", "--lang", "en", "--format", "json", "show"])
                self.assertEqual(status, 2)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("source Latin hash is stale", error.getvalue())

    def test_checker_delegates_to_the_same_source_binding_validator(self):
        checker = load_tool("check-calendar-masses")
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            _, calendar, inventory = self.write_fixture(Path(directory))
            checker.OVERLAY_DIR = inventory
            checker.act_history = lambda: ()
            checker._SOURCE_RECORDS = ({}, None)
            original = checker.sibling
            checker.sibling = lambda name: self.tool if name == "mass-propers" else original(name)
            with mock.patch.object(self.tool, "study_translation_source_context", return_value=self.context), \
                    mock.patch.object(self.tool, "validate_study_translation_binding", side_effect=ValueError("source binding rejected")) as validate:
                problems, _ = checker.overlay_problems([calendar])
            self.assertTrue(validate.called)
            self.assertIn("source binding rejected", problems)


if __name__ == "__main__":
    unittest.main()
