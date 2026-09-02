#!/usr/bin/env python3
"""Regression checks for the Ordinary layer, and for the page that shows it.

The interesting failures here are not crashes. They are a prayer served under
the wrong name and a surface-limited text escaping its source-study quarantine,
and neither would raise anything.

Two of the checks below exist because of specific, recorded near-misses. The
1861 Canon and the postconciliar Eucharistic Prayer I differ at eleven places,
among them both consecratory forms, so serving the one as the other would put a
wrong text at the most consequential locus in the rite; `test_prayer_one_is_not
_the_1861_canon` holds that boundary. Surface-specific permissions are retained
only in source-study records, while the assembled Ordinary exposes a typed,
provider-neutral absence and no recoverable text or attribution.

The browser half runs the real `day.js` and `ordinary-seating.js` under node
against the real generated files, for the reason `calendar-rubrics check` runs
`assembly-model.js` that way: a Python re-implementation would drift from the
page.
"""

from collections import Counter

import hashlib
import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "web" / "data" / "structure" / "ordinary"
PROPERS = ROOT / "src" / "web" / "data" / "structure" / "propers"
DAY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "day.js"
DAY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "day.html"
FORMULARY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "liturgy.js"
FORMULARY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "index.html"
FORMULARY_READER_JS = (
    ROOT / "src" / "web" / "browser" / "liturgy" / "propers-reader.js"
)
READING_CONTENTS_JS = (
    ROOT / "src" / "web" / "browser" / "liturgy" / "reading-contents.js"
)
PLACEMENT_NOTES_JS = (
    ROOT / "src" / "web" / "browser" / "liturgy" / "proper-placement-notes.js"
)
DAY_MISSAL_CSS = ROOT / "src" / "web" / "browser" / "liturgy" / "day-missal.css"
TOOL = ROOT / "tools" / "mass-ordinary"
POST_INVENTORY = (
    ROOT / "src" / "sources" / "inventories" / "postconciliar-ordo-missae-v1.toml"
)
ROMAN_1962_INVENTORY = (
    ROOT / "src" / "sources" / "inventories" / "roman-1962-ordo-missae-v1.toml"
)

ICEL_SOURCE_ID = (
    "edition.international-commission-on-english-in-the-liturgy."
    "music-for-the-roman-missal.2010-chants-web-2026-08-21"
)
ICEL_ACKNOWLEDGEMENT = (
    "Excerpts from the English translation of The Roman Missal © 2010, "
    "International Commission on English in the Liturgy Corporation. "
    "All rights reserved."
)
ICEL_ARTIFACT_SUFFIXES = (
    "greeting", "penitential-act", "kyrie", "gloria", "liturgy-word", "credo-1",
    "orate-fratres", "preface-dialogue", "sanctus", "memorial-acclamation",
    "doxology", "lords-prayer", "sign-of-peace", "agnus-dei", "communion",
    "blessing", "dismissal",
)
ELLC_SOURCE_ID = (
    "edition.english-language-liturgical-consultation.praying-together.1998"
)

PUBLISHABLE = {"public-domain", "project-created"}


def load(name: str) -> dict:
    return json.loads((DATA / (name + ".json")).read_text(encoding="utf-8"))


def elements(file: dict):
    for section in file["sections"]:
        for element in section["elements"]:
            yield element


class OrdinaryStructure(unittest.TestCase):
    """What the generated files must say, whatever the page does with them."""

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written; run `tools/tpt mass-ordinary structure`")
        calendars = [row["calendar"] for row in load("index")["calendars"]]
        self.files = {calendar: load(calendar) for calendar in calendars}

    def test_every_element_has_text_or_a_stated_reason(self) -> None:
        """The one thing this layer must never emit is a silent gap."""
        for name, file in self.files.items():
            for element in elements(file):
                if not element["translations"]:
                    self.assertTrue(
                        element["absent"]["english"],
                        f"{name}: {element['key']} has no English and names no reason",
                    )

    def test_no_witness_reaches_the_page_without_publishable_rights(self) -> None:
        for name, file in self.files.items():
            for witness in file["translations"]:
                self.assertIn(witness["rights"], PUBLISHABLE, name)
            for element in elements(file):
                for translation in element["translations"] or []:
                    self.assertIn(translation["rights"], PUBLISHABLE,
                                  f"{name}: {element['key']}")

    def test_surface_limited_rights_never_reach_the_assembled_ordinary(self) -> None:
        """A permission for another surface is not an assembled-data right."""
        for name, file in self.files.items():
            for witness in file["translations"]:
                self.assertNotEqual(witness["rights"], "licensed-free", name)
            for element in elements(file):
                for translation in element["translations"] or []:
                    self.assertNotEqual(
                        translation["rights"], "licensed-free",
                        f"{name}: {element['key']}",
                    )

    def test_restricted_provenance_never_enters_the_public_payload(self) -> None:
        """Restricted provenance stays source-only; public absence is text-free."""
        with POST_INVENTORY.open("rb") as handle:
            source = tomllib.load(handle)
        restricted = source["restricted_witnesses"]
        self.assertEqual(len(restricted), 1)
        icel = restricted[0]
        self.assertEqual(icel["id"], ICEL_SOURCE_ID)
        self.assertEqual(icel["lang"], "en")
        self.assertEqual(icel["state"], "rights-restricted")
        self.assertEqual(icel["acknowledgement"], ICEL_ACKNOWLEDGEMENT)
        prefix = "artifact." + ICEL_SOURCE_ID.removeprefix("edition.") + "."
        self.assertEqual(icel["artifacts"], [prefix + one for one in ICEL_ARTIFACT_SUFFIXES])

        file = self.files["postconciliar"]
        serialized = json.dumps(file, ensure_ascii=False, sort_keys=True)
        self.assertNotIn(ICEL_SOURCE_ID, serialized)
        self.assertNotIn(ICEL_ACKNOWLEDGEMENT, serialized)
        self.assertNotIn(icel["label"], serialized)
        self.assertNotIn(ELLC_SOURCE_ID, serialized)
        self.assertNotIn("English Language Liturgical Consultation", serialized)
        self.assertNotIn("International Commission on English", serialized)
        self.assertNotIn("licensed-free", serialized)
        self.assertEqual(
            [(one["source_id"], one["held"]) for one in file["translations"]],
            [
                (
                    "edition.eugene-cummiskey.roman-missal-english-laity."
                    "philadelphia-1861",
                    20,
                ),
            ],
        )
        expected_absences = {
            "antecedent-diverges-at-named-words": (
                3, "rights-restricted", "rights-withheld"
            ),
            "antecedent-held-not-carried": (1, "unavailable", "witness-gap"),
            "approved-english-publication-restriction": (
                25, "rights-restricted", "rights-withheld"
            ),
            "editio-typica-new-matter": (
                13, "rights-restricted", "rights-withheld"
            ),
            "element-spans-mixed-availability": (3, "unavailable", "model-gap"),
            "element-spans-mixed-matter": (7, "unavailable", "model-gap"),
            "no-antecedent-witness": (3, "unavailable", "witness-gap"),
            "no-fixed-text": (3, "unavailable", "not-applicable"),
            "not-a-text": (12, "unavailable", "not-applicable"),
            "official-exemplar-not-carried": (16, "unavailable", "witness-gap"),
            "priest-prayer-said-quietly": (6, "unavailable", "no-exemplar"),
            "proper-text-outside-ordinary": (6, "unavailable", "outside-layer"),
        }
        self.assertEqual(
            {
                row["key"]: (row["count"], row["state"], row["kind"])
                for row in file["absences"]
            },
            expected_absences,
        )
        for absence in file["absences"]:
            self.assertEqual(set(absence), {"key", "count", "state", "kind"})
            self.assertEqual(
                absence["state"],
                "rights-restricted"
                if absence["kind"] == "rights-withheld"
                else "unavailable",
            )
        affected = [
            element for element in elements(file)
            if element["absent"]["english"]
            == "approved-english-publication-restriction"
        ]
        self.assertEqual(len(affected), 25)
        for element in affected:
            self.assertFalse(
                any(row["lang"] == "en" for row in (element["translations"] or [])),
                element["key"],
            )

        languages = {one["lang"]: one for one in file["languages"]}
        self.assertEqual((languages["en"]["held"], languages["en"]["elements"]),
                         (0, 59))
        self.assertEqual((languages["la"]["held"], languages["la"]["elements"]),
                         (20, 59))
        self.assertEqual(languages["en"]["elements"] - languages["en"]["held"], 59)
        self.assertEqual(languages["la"]["elements"] - languages["la"]["held"], 39)
        held_elements = [one for one in elements(file) if one["translations"]]
        wholly_absent = [one for one in elements(file) if not one["translations"]]
        self.assertEqual((len(held_elements), len(wholly_absent)), (20, 39))

        self.assertEqual(len(source["witnesses"]), 1)
        self.assertEqual(source["witnesses"][0]["lang"], "la")
        self.assertEqual(
            {absence["kind"] for absence in source["absences"]},
            {
                "model-gap", "no-exemplar", "not-applicable", "outside-layer",
                "rights-withheld", "witness-gap",
            },
        )
        self.assertFalse(any("english" in element
                             for section in source["sections"]
                             for element in section.get("elements", [])))

    def test_structured_turns_are_lossless_translation_local_metadata(self) -> None:
        """The generator preserves source rows; it never invents turn text."""
        found = []
        allowed_speakers = {None, "all", "priest", "server"}
        allowed_roles = {None, "versicle", "response"}
        for calendar, file in self.files.items():
            for element in elements(file):
                self.assertNotIn("turns", element, f"{calendar}: {element['key']}")
                for translation in element["translations"] or []:
                    turns = translation.get("turns")
                    if turns is None:
                        continue
                    found.append((calendar, element["key"], translation["lang"], turns))
                    self.assertTrue(turns)
                    keys = [turn["key"] for turn in turns]
                    self.assertEqual(len(keys), len(set(keys)))
                    self.assertEqual(
                        "\n".join(turn["text"] for turn in turns),
                        translation["text"],
                        f"{calendar}: {element['key']}: {translation['lang']}",
                    )
                    for turn in turns:
                        self.assertEqual(
                            set(turn),
                            {"key", "speaker", "dialogue_role", "action", "text"},
                        )
                        self.assertRegex(turn["key"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                        self.assertIn(turn["speaker"], allowed_speakers)
                        self.assertIn(turn["dialogue_role"], allowed_roles)
                        self.assertIn(turn["action"], (None, True))
                        self.assertIsInstance(turn["text"], str)
                        self.assertTrue(turn["text"])
                        if turn["action"] is True:
                            self.assertIsNone(turn["speaker"])
                            self.assertIsNone(turn["dialogue_role"])

        reached = {(calendar, key, lang) for calendar, key, lang, _turns in found}
        roman_elements = {
            "praeparatio/confiteor-sacerdotis": "priest",
            "praeparatio/confiteor-ministrorum": "server",
            "oblatio/laus-tibi-christe": "server",
            "oblatio/suscipiat-dominus": "server",
            "conclusio/deo-gratias": "server",
        }
        expected = {
            (calendar, key, lang)
            for calendar in ("roman-1962", "roman-pre-1955")
            for key in roman_elements
            for lang in ("en", "la")
        } | {("postconciliar", "praeparatio-donorum/orate-fratres", "la")}
        self.assertEqual(reached, expected)
        post_turns = next(
            turns for calendar, key, lang, turns in found
            if (calendar, key, lang)
            == ("postconciliar", "praeparatio-donorum/orate-fratres", "la")
        )
        self.assertEqual(
            [(turn["key"], turn["speaker"], turn["dialogue_role"], turn["action"])
             for turn in post_turns],
            [("priest-summons", "priest", "versicle", None),
             ("people-response", "all", "response", None)],
        )
        self.assertTrue(post_turns[1]["text"].startswith("R. Suscipiat"))
        for calendar, key, lang, turns in found:
            if calendar.startswith("roman-"):
                self.assertEqual(len(turns), 1, (calendar, key, lang))
                self.assertEqual(turns[0]["speaker"], roman_elements[key])
                self.assertIsNone(turns[0]["dialogue_role"])

        # Quarantined English has neither text nor turns. Metadata on Latin
        # never leaks across to English, and no Roman source is heuristically
        # split.
        post = self.files["postconciliar"]
        post_by_key = {element["key"]: element for element in elements(post)}
        key = "symbolum/symbolum-apostolicum"
        self.assertFalse(any(
            row["lang"] == "en"
            for row in (post_by_key[key]["translations"] or [])
        ), key)
        for calendar in ("roman-1962", "roman-pre-1955"):
            opaque = next(
                element for element in elements(self.files[calendar])
                if element["key"] == "praeparatio/introibo-ad-altare-dei"
            )
            for translation in opaque["translations"] or []:
                self.assertNotIn("turns", translation, f"{calendar}: opaque {translation['lang']}")

    def test_postconciliar_n_130_is_the_single_received_agnus_dei(self) -> None:
        """One received text at n. 130 must not acquire an invented alternative."""
        post = list(elements(self.files["postconciliar"]))
        self.assertEqual(
            [one["key"] for one in post if one["locus"] == "n. 130"],
            ["ritus-communionis/agnus-dei"],
        )
        self.assertNotIn(
            "ritus-communionis/agnus-dei-forma-altera",
            {one["key"] for one in post},
        )

    def test_element_keys_are_unique_across_sections(self) -> None:
        """The 1861 book says `Gloria Patri` twice; the keys must still differ."""
        for name, file in self.files.items():
            keys = [element["key"] for element in elements(file)]
            self.assertEqual(len(keys), len(set(keys)), name)

    def test_roman_1962_absence_split_is_target_local_and_exhaustive(self) -> None:
        """One witness's 1962 classifications do not rewrite its older frame."""
        roman = self.files["roman-1962"]
        self.assertEqual(
            {row["key"]: row["count"] for row in roman["absences"]},
            {
                "no-facing-latin": 8,
                "not-in-the-1962-ordo": 2,
                "witness-own-english": 67,
            },
        )
        self.assertEqual(sum(row["count"] for row in roman["absences"]), 77)
        by_key = {element["key"]: element for element in elements(roman)}
        self.assertEqual(
            by_key["oblatio/accendat-in-nobis"]["absent"]["latin"],
            "no-facing-latin",
        )
        self.assertEqual(
            by_key["conclusio/postcommunio-mundet"]["absent"]["latin"],
            "not-in-the-1962-ordo",
        )
        self.assertEqual(
            by_key["praefatio/rubrica-nota-asterisci"]["absent"]["latin"],
            "witness-own-english",
        )

        pre = self.files["roman-pre-1955"]
        self.assertEqual(
            {row["key"]: row["count"] for row in pre["absences"]},
            {"no-facing-latin": 83},
        )

    def test_only_the_postconciliar_missal_offers_bounded_choices(self) -> None:
        """The 1962 Missal has one Canon, so it must offer nothing to choose."""
        self.assertEqual(self.files["roman-1962"]["variants"], [])
        groups = self.files["postconciliar"]["variants"]
        self.assertEqual(
            [one["group"] for one in groups],
            ["penitential-act", "creed", "eucharistic-prayer"],
        )
        self.assertTrue(all(one["mode"] == "one-of" for one in groups))
        defaults = {
            one["group"]: [option["id"] for option in one["options"] if option["default"]]
            for one in groups
        }
        self.assertEqual(
            defaults,
            {
                "penitential-act": ["pa-i"],
                "creed": ["creed-nicene"],
                "eucharistic-prayer": ["ep-i"],
            },
        )

    def test_choice_memberships_and_conditions_are_structural(self) -> None:
        post = {one["key"]: one for one in elements(self.files["postconciliar"])}
        expected = {
            "ritus-initiales/actus-paenitentialis-i":
                [{"group": "penitential-act", "option": "pa-i"}],
            "ritus-initiales/actus-paenitentialis-ii":
                [{"group": "penitential-act", "option": "pa-ii"}],
            "ritus-initiales/actus-paenitentialis-iii":
                [{"group": "penitential-act", "option": "pa-iii"}],
            "symbolum/symbolum-nicaenum":
                [{"group": "creed", "option": "creed-nicene"}],
            "symbolum/symbolum-apostolicum":
                [{"group": "creed", "option": "creed-apostles"}],
        }
        for key, alternatives in expected.items():
            self.assertEqual(post[key]["alternatives"], alternatives, key)
        conditioned = {
            key: condition
            for key, element in post.items()
            for condition in element["conditions"]
        }
        self.assertEqual(
            conditioned["ritus-initiales/kyrie"]["kind"], "omit-when-option"
        )
        self.assertEqual(
            conditioned["liturgia-verbi/lectio-secunda"]["predicates"],
            ["second-reading-appointed"],
        )
        self.assertEqual(
            conditioned["prex-eucharistica/prex-eucharistica-iv"]["predicates"],
            ["mass-has-no-proper-preface"],
        )
        self.assertTrue(
            all(condition["unknown"] == "unresolved" for condition in conditioned.values())
        )

    def test_prayer_one_is_not_the_1861_canon(self) -> None:
        """The divergence that makes this the worst possible substitution.

        Prayer I is split only at bounded source children. Its nine safe
        antecedents remain language-local and plainly antecedent; three unsafe
        children carry no Latin, and no child carries quarantined English.
        """
        found = [
            one for one in elements(self.files["postconciliar"])
            if {"group": "eucharistic-prayer", "option": "ep-i"}
            in one["alternatives"]
        ]
        self.assertEqual(len(found), 12)
        for prayer in found:
            self.assertFalse(
                any(row["lang"] == "en" for row in (prayer["translations"] or [])),
                prayer["key"],
            )
            self.assertEqual(
                prayer["absent"]["english"], "official-exemplar-not-carried"
            )
        latin = {
            prayer["key"]: next(
                (row for row in (prayer["translations"] or []) if row["lang"] == "la"),
                None,
            )
            for prayer in found
        }
        self.assertEqual(sum(row is not None for row in latin.values()), 9)
        self.assertEqual(
            [key for key, row in latin.items()
             if row is not None and row["collation"] == "collated"],
            ["prex-eucharistica/quam-oblationem"],
        )
        self.assertEqual(
            {
                prayer["key"]: prayer["absent"]["latin"]
                for prayer in found if latin[prayer["key"]] is None
            },
            {
                "prex-eucharistica/communicantes": "element-spans-mixed-matter",
                "prex-eucharistica/qui-pridie": "editio-typica-new-matter",
                "prex-eucharistica/supplices": "element-spans-mixed-matter",
            },
        )

    def test_every_language_names_the_side_that_records_its_absence(self) -> None:
        """A language on offer must be able to say why it is empty.

        The page offers the reader every language declared here, including ones
        no word of which is held, because choosing an empty language is how the
        reason for the emptiness becomes visible. That only works if the join
        holds: each language names one side of `absent`, every element carries
        exactly those sides, and a language holding nothing carries a reason on
        every element rather than on most of them.
        """
        for name, file in self.files.items():
            langs = [one["lang"] for one in file["languages"]]
            self.assertEqual(len(langs), len(set(langs)), name)
            sides = {one["absent"] for one in file["languages"]}
            self.assertEqual(len(sides), len(langs), f"{name}: two languages share a side")
            for element in elements(file):
                self.assertEqual(set(element["absent"]), sides, f"{name}: {element['key']}")
            for one in file["languages"]:
                held = sum(1 for element in elements(file)
                           for translation in (element["translations"] or [])
                           if translation["lang"] == one["lang"])
                self.assertEqual(one["held"], held, f"{name}: {one['lang']} miscounted")
                for element in elements(file):
                    if any(row["lang"] == one["lang"]
                           for row in (element["translations"] or [])):
                        continue
                    self.assertTrue(
                        element["absent"][one["absent"]],
                        f"{name}: {element['key']} is silent in {one['lang']} "
                        "and names no reason",
                    )

    def test_the_index_names_every_calendar(self) -> None:
        listed = {row["calendar"] for row in load("index")["calendars"]}
        self.assertEqual(listed, set(self.files))


class OrdinarySlots(unittest.TestCase):
    """Where a proper of the day sits in the frame.

    These hold the declaration, not the page. A seat that resolves to nothing,
    a proper claimed by two seats, or seats that run backwards would each put a
    prayer somewhere plausible and wrong without anything failing.
    """

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written; run `tools/tpt mass-ordinary structure`")
        calendars = [row["calendar"] for row in load("index")["calendars"]]
        self.files = {calendar: load(calendar) for calendar in calendars}

    def test_every_seat_names_an_element_the_frame_shows(self) -> None:
        for name, file in self.files.items():
            keys = {element["key"]: element for element in elements(file)}
            for slot in file["slots"]:
                self.assertIn(slot["anchor"], keys, f"{name}: seat {slot['key']}")
                self.assertFalse(
                    keys[slot["anchor"]]["alternatives"],
                    f"{name}: seat {slot['key']} would vanish with a choice of prayer",
                )
                self.assertIn(slot["where"], ("before", "after"), f"{name}: {slot['key']}")

    def test_a_proper_has_one_seat(self) -> None:
        for name, file in self.files.items():
            claimed = [proper for slot in file["slots"] for proper in slot["propers"]]
            self.assertEqual(len(claimed), len(set(claimed)), name)

    def test_the_seats_run_forward_through_the_frame(self) -> None:
        """The file's order is the order of the rite, and is checked to be."""
        for name, file in self.files.items():
            order = {element["key"]: index for index, element in enumerate(elements(file))}
            reached = -1
            for slot in file["slots"]:
                at = order[slot["anchor"]] + (1 if slot["where"] == "after" else 0)
                self.assertGreaterEqual(at, reached, f"{name}: seat {slot['key']} runs backwards")
                reached = at

    def test_a_seat_says_which_rubric_puts_it_there(self) -> None:
        for name, file in self.files.items():
            if not file["slots"]:
                continue
            self.assertTrue(file["slots_derived_from"],
                            f"{name}: seats are declared and no book is named for them")
            for slot in file["slots"]:
                self.assertTrue(slot["locus"], f"{name}: seat {slot['key']} cites nothing")

    def test_the_seats_name_propers_the_corpus_actually_carries(self) -> None:
        """A seat for a proper name no mass uses is a seat that never fills.

        Not a rights or a truth question — a spelling one, and exactly the kind
        that resolves successfully and does nothing. A structural-only
        recension with no independently represented Propers is checked against
        the canonical corpus-wide vocabulary: its typed missing formularies
        cannot supply names of their own.
        """
        corpus_names = set()
        for path in PROPERS.glob("*.json"):
            if path.name == "index.json":
                continue
            corpus = json.loads(path.read_text(encoding="utf-8"))
            corpus_names.update(
                proper.get("name")
                for mass in corpus.get("masses", [])
                for proper in mass.get("propers", [])
            )
        for name, file in self.files.items():
            path = PROPERS / (name + ".json")
            if not path.is_file():
                self.skipTest("no propers layer written")
            corpus = json.loads(path.read_text(encoding="utf-8"))
            used = {proper.get("name")
                    for mass in corpus.get("masses", [])
                    for proper in mass.get("propers", [])}
            proper_coverage = (
                (corpus.get("recension_coverage") or {})
                .get("domains", {})
                .get("propers", {})
                .get("state")
            )
            if proper_coverage == "none":
                used = corpus_names
            for slot in file["slots"]:
                for proper in slot["propers"]:
                    self.assertIn(proper, used, f"{name}: seat {slot['key']} awaits {proper!r}")


class OrdinaryTool(unittest.TestCase):
    """The generator refuses what it must refuse."""

    @classmethod
    def setUpClass(cls) -> None:
        loader = importlib.machinery.SourceFileLoader("mass_ordinary_test", str(TOOL))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool_module = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool_module)

    def test_written_files_are_current(self) -> None:
        run = subprocess.run(
            ["python3", str(TOOL), "check", "--json"],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        payload = json.loads(run.stdout)
        self.assertEqual(payload["stale"], [],
                         "regenerate with `tools/tpt mass-ordinary structure`")
        self.assertEqual(payload["seating"]["failures"], 0)
        self.assertGreater(payload["seating"]["full_forms"], 0)
        self.assertGreater(payload["seating"]["nonfull_forms"], 0)
        self.assertEqual(
            payload["seating"]["full_forms"],
            sum(row["full_forms"] for row in payload["seating"]["calendars"]),
        )
        self.assertEqual(
            payload["seating"]["nonfull_forms"],
            sum(row["nonfull_forms"] for row in payload["seating"]["calendars"]),
        )

    def test_cross_layer_seating_refuses_unknown_backward_and_stale_rows(self) -> None:
        tool = self.tool_module
        ordinary = {
            "calendar": "synthetic",
            "slots": [
                {"key": "first", "propers": ["First"], "qualified": False},
                {"key": "second", "propers": ["Second"], "qualified": False},
            ],
        }
        with self.assertRaisesRegex(tool.SourceError, "has no Ordinary seat"):
            tool.check_form_seating(
                ordinary, [{"name": "Unknown"}], "synthetic/mass/main", full=True
            )
        with self.assertRaisesRegex(tool.SourceError, "runs backward"):
            tool.check_form_seating(
                ordinary,
                [{"name": "Second"}, {"name": "First"}],
                "synthetic/mass/main",
                full=True,
            )
        with self.assertRaisesRegex(tool.SourceError, "stale because"):
            tool.check_form_seating(
                ordinary,
                [{
                    "name": "First",
                    "ordinary_disposition": {
                        "kind": "unplaced", "group": "outside-rite",
                        "region": "before-frame", "basis": "Synthetic locus.",
                    },
                }],
                "synthetic/mass/main",
                full=True,
            )

    def test_cross_layer_seating_refuses_singleton_and_mixed_seat_choices(self) -> None:
        tool = self.tool_module
        ordinary = {
            "calendar": "synthetic",
            "slots": [
                {"key": "first", "propers": ["First"], "qualified": False},
                {"key": "second", "propers": ["Second"], "qualified": False},
            ],
        }

        def choice(name: str, option: str) -> dict:
            return {
                "name": name,
                "ordinary_disposition": {
                    "kind": "alternative", "group": "reading-choice",
                    "option": option, "basis": "Synthetic source choice.",
                },
            }

        with self.assertRaisesRegex(tool.SourceError, "at least two distinct options"):
            tool.check_form_seating(
                ordinary, [choice("First", "long")],
                "synthetic/mass/main", full=True,
            )
        with self.assertRaisesRegex(tool.SourceError, "spans Ordinary slots"):
            tool.check_form_seating(
                ordinary, [choice("First", "long"), choice("Second", "short")],
                "synthetic/mass/main", full=True,
            )

    def test_cross_layer_seating_refuses_stale_generated_propers_shape(self) -> None:
        tool = self.tool_module
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            target = out / "structure" / "propers" / "synthetic.json"
            target.parent.mkdir(parents=True)
            target.write_text(
                json.dumps({
                    "schema": "triptych-propers-structure/retired",
                    "calendar": "synthetic", "masses": [],
                }),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(tool.SourceError, "stale generated Propers"):
                tool.read_propers_structure(out, "synthetic")

    def test_roman_1962_source_absences_partition_all_english_only_rows(self) -> None:
        """The six target exclusions do not erase their source classifications."""
        tool = self.tool_module
        source = tool.read_toml(ROMAN_1962_INVENTORY)
        library = tool.artifact_records(ROOT / "src" / "sources")
        counts = Counter()
        for section in source["sections"]:
            english = {
                row["element_key"] for row in tool.payload_rows(library[section["artifact"]])
            }
            latin = {
                row["element_key"]
                for row in tool.payload_rows(library[section["artifact_latin"]])
            }
            missing = english - latin
            overrides = section.get("absent_latin_by_element", {})
            self.assertLessEqual(set(overrides), missing, section["key"])
            counts.update(overrides.get(key, section["absent_latin"]) for key in missing)
        self.assertEqual(
            counts,
            Counter({
                "no-facing-latin": 8,
                "not-in-the-1962-ordo": 4,
                "witness-own-english": 71,
            }),
        )

    def test_artifact_latin_absence_overrides_are_closed(self) -> None:
        tool = self.tool_module
        section = {
            "key": "synthetic",
            "absent_latin_by_element": {"english-only": "specific-gap"},
        }
        absences = {"default-gap": {}, "specific-gap": {}}
        self.assertEqual(
            tool.artifact_latin_absence_overrides(
                section, {"english-only", "held"}, {"held"}, absences,
                "synthetic.toml",
            ),
            {"english-only": "specific-gap"},
        )
        invalid = (
            ({}, "empty or malformed"),
            ([], "empty or malformed"),
            ({"missing": "specific-gap"}, "does not hold"),
            ({"held": "specific-gap"}, "already holds text"),
            ({"english-only": "undeclared"}, "does not state"),
            ({"english-only": "   "}, "has no reason"),
        )
        for declared, message in invalid:
            with self.subTest(declared=declared):
                with self.assertRaisesRegex(tool.SourceError, message):
                    tool.artifact_latin_absence_overrides(
                        section | {"absent_latin_by_element": declared},
                        {"english-only", "held"}, {"held"}, absences,
                        "synthetic.toml",
                    )

    def test_coverage_is_language_relation_absence_and_exclusion_aware(self) -> None:
        run = subprocess.run(
            ["python3", str(TOOL), "coverage", "--json"],
            capture_output=True, text=True, cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        rows = {row["calendar"]: row for row in json.loads(run.stdout)["coverage"]}
        required = {
            "calendar", "elements", "witnesses", "language_coverage",
            "relation_coverage", "absent", "language_absences", "exclusions",
        }
        for calendar, row in rows.items():
            self.assertEqual(set(row), required, calendar)
            for language in row["language_coverage"]:
                self.assertEqual(
                    language["held"] + language["missing"], row["elements"], calendar
                )
                self.assertEqual(language["absent"], language["missing"], calendar)
                self.assertEqual(
                    sum(
                        relation["count"] for relation in row["relation_coverage"]
                        if relation["lang"] == language["lang"]
                    ),
                    language["held"],
                    calendar,
                )
                self.assertEqual(
                    sum(
                        absence["count"] for absence in row["language_absences"]
                        if absence["lang"] == language["lang"]
                    ),
                    language["missing"],
                    calendar,
                )
            for absence in row["language_absences"]:
                self.assertGreater(absence["count"], 0, calendar)
                self.assertEqual(
                    set(absence), {"key", "lang", "count", "state", "kind"}
                )
            for absence in row["absent"]:
                self.assertEqual(
                    absence["count"],
                    sum(
                        part["count"] for part in row["language_absences"]
                        if part["key"] == absence["key"]
                    ),
                    f"{calendar}: {absence['key']}",
                )

        roman = rows["roman-1962"]
        self.assertEqual(
            [(one["lang"], one["held"], one["missing"])
             for one in roman["language_coverage"]],
            [("en", 189, 0), ("la", 112, 77)],
        )
        self.assertEqual(
            [one["key"] for one in roman["exclusions"]],
            [
                "oblatio/a-cunctis",
                "oblatio/nota-incarnationis",
                "oblatio/rubrica-collecta-concede",
                "oblatio/rubrica-secreta",
                "oblatio/rubrica-secreta-concede",
                "oblatio/secreta-ii",
            ],
        )
        for exclusion in roman["exclusions"]:
            self.assertEqual(exclusion["state"], "not-in-target-recension")
            self.assertFalse(
                any("text" in evidence for evidence in exclusion["evidence"]),
                exclusion["key"],
            )
            self.assertEqual(exclusion["sources"], sorted(set(exclusion["sources"])))

    def test_show_selects_one_option_and_surfaces_unknown_applicability(self) -> None:
        def show(*options: str) -> subprocess.CompletedProcess:
            command = [
                "python3", str(TOOL), "show", "--calendar", "postconciliar",
                "--no-rubrics",
            ]
            for option in options:
                command.extend(("--variant", option))
            return subprocess.run(
                command, capture_output=True, text=True, cwd=ROOT, check=False,
            )

        default = show()
        self.assertEqual(default.returncode, 0, default.stdout + default.stderr)
        self.assertIn("\n  Penitential Act, form I (all)\n", default.stdout)
        self.assertNotIn("\n  Penitential Act, form II (all)\n", default.stdout)
        self.assertNotIn("\n  Penitential Act, form III (all)\n", default.stdout)
        self.assertIn("Eucharistic Prayer I — Te igitur", default.stdout)
        self.assertNotIn("Eucharistic Prayer IV (priest)", default.stdout)
        self.assertIn("applicability unresolved: second-reading-appointed", default.stdout)

        selected = show("pa-iii", "ep-iv")
        self.assertEqual(selected.returncode, 0, selected.stdout + selected.stderr)
        self.assertIn("\n  Penitential Act, form III (all)\n", selected.stdout)
        self.assertNotIn("\n  Penitential Act, form I (all)\n", selected.stdout)
        self.assertNotIn("Kyrie eleison", selected.stdout)
        self.assertNotIn("\n  Eucharistic Prayer IV (priest)\n", selected.stdout)
        self.assertNotIn("Eucharistic Prayer I —", selected.stdout)
        self.assertIn(
            "Eucharistic Prayer IV: applicability unresolved: "
            "mass-has-no-proper-preface",
            selected.stdout,
        )

        unknown = show("not-an-option")
        self.assertEqual(unknown.returncode, 2, unknown.stdout + unknown.stderr)
        self.assertIn("no variant option", unknown.stderr)

    def test_check_distinguishes_stale_and_current_output_in_both_tiers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            shutil.copytree(PROPERS, out / "structure" / "propers")
            stale = subprocess.run(
                ["python3", str(TOOL), "check", "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(stale.returncode, 1, stale.stdout + stale.stderr)
            self.assertTrue(json.loads(stale.stdout)["stale"])

            written = subprocess.run(
                ["python3", str(TOOL), "structure", "--out", str(out)],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
            for json_tier in (False, True):
                command = ["python3", str(TOOL), "check", "--out", str(out)]
                if json_tier:
                    command.append("--json")
                current = subprocess.run(
                    command, capture_output=True, text=True, cwd=ROOT, check=False,
                )
                self.assertEqual(current.returncode, 0, current.stdout + current.stderr)
                if json_tier:
                    self.assertEqual(json.loads(current.stdout)["stale"], [])
                else:
                    self.assertIn("the written files are current", current.stdout)

    def test_unscoped_writer_prunes_only_owned_orphan_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            shutil.copytree(PROPERS, out / "structure" / "propers")
            written = subprocess.run(
                ["python3", str(TOOL), "structure", "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
            ordinary = out / "structure" / "ordinary"
            orphan = ordinary / "retired-calendar.json"
            unrelated = ordinary / "keep-me.txt"
            orphan.write_text("{}\n", encoding="utf-8")
            unrelated.write_text("not owned by mass-ordinary\n", encoding="utf-8")

            scoped = subprocess.run(
                ["python3", str(TOOL), "check", "--calendar", "postconciliar",
                 "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(scoped.returncode, 0, scoped.stdout + scoped.stderr)
            self.assertEqual(json.loads(scoped.stdout)["stale"], [])
            subprocess.run(
                ["python3", str(TOOL), "structure", "--calendar", "postconciliar",
                 "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=True,
            )
            self.assertTrue(orphan.is_file(), "scoped structure must not prune")

            stale = subprocess.run(
                ["python3", str(TOOL), "check", "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(stale.returncode, 1, stale.stdout + stale.stderr)
            self.assertEqual(
                json.loads(stale.stdout)["stale"],
                ["structure/ordinary/retired-calendar.json"],
            )

            refreshed = subprocess.run(
                ["python3", str(TOOL), "structure", "--out", str(out), "--json"],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            self.assertEqual(refreshed.returncode, 0, refreshed.stdout + refreshed.stderr)
            self.assertEqual(
                json.loads(refreshed.stdout)["removed"], [str(orphan)]
            )
            self.assertFalse(orphan.exists())
            self.assertTrue(unrelated.is_file(), "unowned files must survive pruning")

    def test_artifact_payloads_resolve_against_the_passed_source_root(self) -> None:
        tool = self.tool_module
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "alternate-sources"
            artifact_dir = source_root / "works" / "synthetic"
            artifact_dir.mkdir(parents=True)
            (artifact_dir / "rows.tsv").write_text(
                "element_key\tseq\ttext\nmarker\t1\talternate root\n",
                encoding="utf-8",
            )
            (artifact_dir / "artifact.toml").write_text(
                'id = "artifact.synthetic.alternate-root"\n'
                'path = "src/sources/works/synthetic/rows.tsv"\n',
                encoding="utf-8",
            )

            records = tool.artifact_records(source_root)
            record = records["artifact.synthetic.alternate-root"]
            self.assertEqual(record["_source_root"], source_root.resolve())
            self.assertEqual(tool.payload_rows(record)[0]["text"], "alternate root")

    def test_artifact_sections_require_explicit_language_provenance(self) -> None:
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        english_id = "artifact.synthetic.english"
        latin_id = "artifact.synthetic.latin"
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory)
            (source_root / "english.tsv").write_text(
                "element_key\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\tnotes\n"
                "oratio\tprayer\tEnglish words.\tOratio\t1\tpriest\t\n",
                encoding="utf-8",
            )
            (source_root / "latin.tsv").write_text(
                "element_key\tlatin\n"
                "oratio\tOratio Latina.\n",
                encoding="utf-8",
            )
            library = {
                english_id: {
                    "id": english_id, "path": "english.tsv",
                    "_source_root": source_root,
                },
                latin_id: {
                    "id": latin_id, "path": "latin.tsv",
                    "_source_root": source_root,
                },
            }
            witnesses = {
                (witness_id, "en"): {
                    "lang": "en", "rights": "public-domain",
                    "artifacts": [english_id],
                },
                (witness_id, "la"): {
                    "lang": "la", "rights": "public-domain",
                    "artifacts": [latin_id],
                },
            }
            section = {
                "key": "synthetic",
                "artifact": english_id,
                "witness": witness_id,
                "artifact_latin": latin_id,
                "english": {
                    "relation": "antecedent",
                    "collation": "uncollated",
                    "note": "An identified antecedent; this comparison is uncollated.",
                },
                "latin": {
                    "relation": "antecedent",
                    "collation": "collated",
                    "collation_finding": "research/finding.md:1",
                    "note": "An identified antecedent with a cited collation.",
                },
            }

            built, exclusions = tool.from_artifact(
                section, witnesses, {}, {}, library, "synthetic.toml"
            )
            self.assertEqual(exclusions, [])
            translations = {
                row["lang"]: row for row in built[0]["translations"]
            }
            self.assertEqual(
                {
                    key: translations["en"][key]
                    for key in ("relation", "collation", "note")
                },
                section["english"],
            )
            self.assertEqual(
                {
                    key: translations["la"][key]
                    for key in (
                        "relation", "collation", "collation_finding", "note",
                    )
                },
                section["latin"],
            )

            for side in ("english", "latin"):
                missing = dict(section)
                missing.pop(side)
                with self.subTest(missing=side):
                    with self.assertRaisesRegex(
                        tool.SourceError, rf"no \[{side}\] provenance block"
                    ):
                        tool.from_artifact(
                            missing, witnesses, {}, {}, library, "synthetic.toml"
                        )

            invalid = dict(section)
            invalid["english"] = section["english"] | {"grade": "uncollated"}
            with self.assertRaisesRegex(tool.SourceError, "unknown fields grade"):
                tool.from_artifact(
                    invalid, witnesses, {}, {}, library, "synthetic.toml"
                )

            contradictory = dict(section)
            contradictory["english"] = {
                "relation": "own", "collation": "uncollated",
            }
            with self.assertRaisesRegex(tool.SourceError, "relation is own"):
                tool.from_artifact(
                    contradictory, witnesses, {}, {}, library, "synthetic.toml"
                )

    def test_artifact_sections_refuse_an_unreasoned_latin_gap(self) -> None:
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        artifact_id = "artifact.synthetic.english-only"
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory)
            (source_root / "english.tsv").write_text(
                "element_key\tkind\tenglish\n"
                "oratio\tprayer\tEnglish words.\n",
                encoding="utf-8",
            )
            library = {
                artifact_id: {
                    "id": artifact_id, "path": "english.tsv",
                    "_source_root": source_root,
                },
            }
            witnesses = {
                (witness_id, "en"): {
                    "lang": "en", "rights": "project-created",
                    "artifacts": [artifact_id],
                },
            }
            section = {
                "key": "synthetic", "artifact": artifact_id,
                "witness": witness_id, "english": {"relation": "own"},
            }
            with self.assertRaisesRegex(tool.SourceError, "has no Latin"):
                tool.from_artifact(
                    section, witnesses, {}, {}, library, "synthetic.toml"
                )

            section["absent_latin"] = "no-facing-latin"
            built, exclusions = tool.from_artifact(
                section, witnesses, {},
                {"no-facing-latin": {"kind": "witness-gap"}},
                library, "synthetic.toml",
            )
            self.assertEqual(exclusions, [])
            self.assertEqual(built[0]["absent"]["latin"], "no-facing-latin")
            self.assertEqual(built[0]["translations"][0]["relation"], "own")

    def test_artifact_exclusions_consume_rows_without_publishing_text(self) -> None:
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        english_id = "artifact.synthetic.exclusion-en"
        latin_id = "artifact.synthetic.exclusion-la"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "english.tsv").write_text(
                "element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\tnotes\n"
                "kept\t10\tprayer\tKept English.\tServata\t1\tpriest\t\n"
                "removed\t20\tprayer\tSecret excluded words.\tRemota\t2\tpriest\t\n",
                encoding="utf-8",
            )
            (root / "latin.tsv").write_text(
                "element_key\tseq\tlatin\n"
                "kept\t10\tServata Latina.\n"
                "removed\t20\tVerba remota secreta.\n",
                encoding="utf-8",
            )
            library = {
                english_id: {"id": english_id, "path": "english.tsv", "_source_root": root},
                latin_id: {"id": latin_id, "path": "latin.tsv", "_source_root": root},
            }
            witnesses = {
                (witness_id, "en"): {
                    "lang": "en", "rights": "public-domain", "artifacts": [english_id],
                },
                (witness_id, "la"): {
                    "lang": "la", "rights": "public-domain", "artifacts": [latin_id],
                },
            }
            section = {
                "key": "synthetic", "artifact": english_id, "witness": witness_id,
                "artifact_latin": latin_id,
                "english": {"relation": "own"}, "latin": {"relation": "own"},
                "exclusions": [{"element": "removed", "basis": "Target edition, locus 1."}],
            }
            built, exclusions = tool.from_artifact(
                section, witnesses, {}, {}, library, "synthetic.toml"
            )
            self.assertEqual([one["key"] for one in built], ["synthetic/kept"])
            self.assertEqual([one["key"] for one in exclusions], ["synthetic/removed"])
            self.assertEqual(exclusions[0]["state"], "not-in-target-recension")
            self.assertEqual(exclusions[0]["sources"], [witness_id])
            self.assertEqual(
                [one["lang"] for one in exclusions[0]["evidence"]], ["en", "la"]
            )
            serialized = json.dumps(exclusions, ensure_ascii=False)
            self.assertNotIn("Secret excluded words", serialized)
            self.assertNotIn("Verba remota secreta", serialized)

            invalid = (
                ([{"element": "missing", "basis": "Citation."}], "does not hold"),
                ([{"element": "removed", "basis": ""}], "has no basis"),
                ([{"element": "removed", "basis": "A."},
                  {"element": "removed", "basis": "B."}], "excludes removed twice"),
                ([{"element": "removed", "basis": "A.", "note": "free prose"}],
                 "unknown fields note"),
            )
            for declarations, message in invalid:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(tool.SourceError, message):
                        tool.from_artifact(
                            section | {"exclusions": declarations}, witnesses, {}, {},
                            library, "synthetic.toml",
                        )

    def test_artifact_section_turns_partition_source_rows_not_prose(self) -> None:
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        english_id = "artifact.synthetic.turn-en"
        latin_id = "artifact.synthetic.turn-la"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "english.tsv").write_text(
                "element_key\tseq\tkind\tenglish\tprinted_page\tspeaker\n"
                "dialogue\t10\tdialogue\tPriest calls.\t1\tpriest\n"
                "dialogue\t20\tdialogue\tPeople answer.\t1\tall\n"
                "opaque\t30\tdialogue\tP. Embedded call. R. Embedded answer.\t2\tall\n",
                encoding="utf-8",
            )
            (root / "latin.tsv").write_text(
                "element_key\tseq\tlatin\n"
                "dialogue\t10\tSacerdos vocat.\n"
                "dialogue\t20\tPopulus respondet.\n"
                "opaque\t30\tP. Vocatio inclusa. R. Responsum inclusum.\n",
                encoding="utf-8",
            )
            library = {
                english_id: {"id": english_id, "path": "english.tsv", "_source_root": root},
                latin_id: {"id": latin_id, "path": "latin.tsv", "_source_root": root},
            }
            witnesses = {
                (witness_id, "en"): {
                    "lang": "en", "rights": "project-created", "artifacts": [english_id],
                },
                (witness_id, "la"): {
                    "lang": "la", "rights": "project-created", "artifacts": [latin_id],
                },
            }
            parts = [
                {"key": "priest-call", "seq": [10], "speaker": "priest",
                 "dialogue_role": "versicle"},
                {"key": "people-answer", "seq": [20], "speaker": "all",
                 "dialogue_role": "response"},
            ]
            section = {
                "key": "synthetic", "artifact": english_id, "witness": witness_id,
                "artifact_latin": latin_id,
                "english": {"relation": "own"}, "latin": {"relation": "own"},
                "turn_partitions": [
                    {"element": "dialogue", "lang": "en", "parts": parts},
                    {"element": "dialogue", "lang": "la", "parts": parts},
                ],
            }
            built, exclusions = tool.from_artifact(
                section, witnesses, {}, {}, library, "synthetic.toml"
            )
            self.assertEqual(exclusions, [])
            self.assertEqual(len(built), 2)
            for translation in built[0]["translations"]:
                self.assertEqual(
                    "\n".join(turn["text"] for turn in translation["turns"]),
                    translation["text"],
                )
            for translation in built[1]["translations"]:
                self.assertNotIn("turns", translation)
            bad = dict(section)
            bad["turn_partitions"] = [
                {"element": "dialogue", "lang": "en", "parts": [
                    {"key": "invented-first", "seq": [10]},
                    {"key": "invented-second", "seq": [10]},
                ]},
                section["turn_partitions"][1],
            ]
            with self.assertRaisesRegex(tool.SourceError, "does not exactly partition"):
                tool.from_artifact(bad, witnesses, {}, {}, library, "synthetic.toml")

    def test_alternatives_conditions_and_unresolved_rights_are_closed(self) -> None:
        tool = self.tool_module
        source = {
            "variants": [{
                "group": "forms", "name": "Forms", "what": "One received form.",
                "options": [
                    {"id": "form-a", "name": "A", "default": True},
                    {"id": "form-b", "name": "B", "default": False},
                ],
            }]
        }
        groups, options = tool.variant_table(source, "synthetic")
        self.assertEqual(groups[0]["mode"], "one-of")
        legacy, alternatives = tool.element_alternatives(
            {"alternatives": [{"group": "forms", "option": "form-b"}]},
            options, "element", "synthetic",
        )
        self.assertIsNone(legacy)
        self.assertEqual(alternatives, [{"group": "forms", "option": "form-b"}])
        conditions = tool.element_conditions(
            {"conditions": [
                {"kind": "include-when-any", "predicates": ["second-reading-appointed"],
                 "basis": "Rubric 1."},
                {"kind": "omit-when-option", "group": "forms", "options": ["form-b"],
                 "basis": "Rubric 2."},
            ]},
            options, "element", "synthetic",
        )
        self.assertTrue(all(one["unknown"] == "unresolved" for one in conditions))
        with self.assertRaisesRegex(tool.SourceError, "more than once"):
            tool.element_alternatives(
                {"alternatives": [
                    {"group": "forms", "option": "form-a"},
                    {"group": "forms", "option": "form-b"},
                ]}, options, "element", "synthetic",
            )
        with self.assertRaisesRegex(tool.SourceError, "closed predicate table"):
            tool.element_conditions(
                {"conditions": [{"kind": "include-when-any",
                                  "predicates": ["prose-is-true"], "basis": "X"}]},
                options, "element", "synthetic",
            )
        unresolved = tool.absence_table(
            {"absences": [{"key": "rights-open", "kind": "rights-unresolved",
                            "what": "Authorization has not been established."}]},
            "synthetic",
        )
        self.assertEqual(unresolved["rights-open"]["kind"], "rights-unresolved")
        self.assertEqual(tool.absence_state("rights-unresolved"), "unresolved")
        self.assertEqual(tool.absence_state("rights-withheld"), "rights-restricted")
        self.assertEqual(tool.absence_state("witness-gap"), "unavailable")

    def test_duplicate_absence_keys_fail_closed_before_public_projection(self) -> None:
        tool = self.tool_module
        row = {
            "key": "provider-neutral-gap",
            "kind": "witness-gap",
            "what": "The held witness carries no facing text.",
        }
        with self.assertRaisesRegex(
            tool.SourceError, "absence provider-neutral-gap is declared twice"
        ):
            tool.absence_table({"absences": [row, dict(row)]}, "synthetic")

    def test_structured_turns_are_exact_closed_and_source_row_owned(self) -> None:
        tool = self.tool_module
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            (fixture / "rows.tsv").write_text(
                "element_key\tseq\ttext\n"
                "dialogue\t10\tServer call.\n"
                "dialogue\t20\tPriest response.\n"
                "dialogue\t30\tBow.\n",
                encoding="utf-8",
            )
            artifact_id = "artifact.synthetic.turns"
            library = {
                artifact_id: {
                    "id": artifact_id,
                    "path": "rows.tsv",
                    "_source_root": fixture,
                }
            }
            with self.subTest(source_root=fixture):
                entry = {
                    "english_turns": [
                        {
                            "key": "server-call", "seq": [10],
                            "speaker": "server", "dialogue_role": "versicle",
                        },
                        {
                            "key": "priest-response", "seq": [20],
                            "speaker": "priest", "dialogue_role": "response",
                        },
                        {"key": "bow", "seq": [30], "action": True},
                    ]
                }
                parent = "Server call.\nPriest response.\nBow."
                turns = tool.structured_turns(
                    entry, "english", library, artifact_id, ["dialogue"],
                    "text", "synthetic/dialogue", "synthetic", parent,
                )
                self.assertEqual(
                    turns,
                    [
                        {
                            "key": "server-call", "speaker": "server",
                            "dialogue_role": "versicle", "action": None,
                            "text": "Server call.",
                        },
                        {
                            "key": "priest-response", "speaker": "priest",
                            "dialogue_role": "response", "action": None,
                            "text": "Priest response.",
                        },
                        {
                            "key": "bow", "speaker": None,
                            "dialogue_role": None, "action": True, "text": "Bow.",
                        },
                    ],
                )
                self.assertEqual("\n".join(row["text"] for row in turns), parent)
                self.assertIsNone(
                    tool.structured_turns(
                        entry, "latin", library, artifact_id, ["dialogue"],
                        "text", "synthetic/dialogue", "synthetic", parent,
                    ),
                    "English turn metadata must not create Latin turns",
                )

                invalid = (
                    ({"english_turns": []}, "empty or malformed"),
                    ({"english_turns": [
                        {"key": "second", "seq": [20]},
                        {"key": "first", "seq": [10]},
                        {"key": "bow", "seq": [30]},
                    ]}, "does not exactly partition"),
                    ({"english_turns": [
                        {"key": "first", "seq": [10, 20]},
                        {"key": "again", "seq": [20, 30]},
                    ]}, "does not exactly partition"),
                    ({"english_turns": [
                        {"key": "same", "seq": [10]},
                        {"key": "same", "seq": [20, 30]},
                    ]}, "repeats turn key"),
                    ({"english_turns": [
                        {"key": "Not Kebab", "seq": [10, 20, 30]},
                    ]}, "kebab"),
                    ({"english_turns": [
                        {"key": "bad-speaker", "seq": [10, 20, 30],
                         "speaker": "deacon"},
                    ]}, "has speaker"),
                    ({"english_turns": [
                        {"key": "bad-role", "seq": [10, 20, 30],
                         "dialogue_role": "reply"},
                    ]}, "has dialogue_role"),
                    ({"english_turns": [
                        {"key": "false-action", "seq": [10, 20, 30],
                         "action": False},
                    ]}, "action must be true or omitted"),
                    ({"english_turns": [
                        {"key": "mixed-action", "seq": [10, 20, 30],
                         "action": True, "speaker": "priest"},
                    ]}, "both an action and a spoken turn"),
                    ({"english_turns": [
                        {"key": "unknown-field", "seq": [10, 20, 30],
                         "offset": 0},
                    ]}, "unknown fields"),
                )
                for bad_entry, message in invalid:
                    with self.subTest(message=message):
                        with self.assertRaisesRegex(tool.SourceError, message):
                            tool.structured_turns(
                                bad_entry, "english", library, artifact_id,
                                ["dialogue"], "text", "synthetic/dialogue",
                                "synthetic", parent,
                            )

                with self.assertRaisesRegex(tool.SourceError, "without a english text block"):
                    tool.side_text(
                        {"english_turns": entry["english_turns"]}, "en",
                        {}, {}, {}, "synthetic/dialogue", "synthetic",
                    )

    def test_restricted_witness_validation_is_fail_closed(self) -> None:
        tool = self.tool_module
        witness_id = "edition.synthetic.restricted"
        artifact_id = "artifact.synthetic.restricted"
        entry = {
            "id": witness_id,
            "lang": "en",
            "state": tool.RESTRICTED_WITNESS_STATE,
            "label": "Restricted provenance",
            "acknowledgement": tool.ICEL_EXCERPT_ACKNOWLEDGEMENT,
            "caution": "Not a publication basis.",
            "artifacts": [artifact_id],
        }
        record = {
            "id": artifact_id,
            "rights_status": "restricted",
            "storage": tool.RESTRICTED_ARTIFACT_STORAGE,
            "indexable": False,
        }
        for rights_status in tool.RESTRICTED_ARTIFACT_RIGHTS:
            with self.subTest(rights_status=rights_status):
                restricted = tool.restricted_witness_table(
                    {"restricted_witnesses": [entry]},
                    {artifact_id: record | {"rights_status": rights_status}},
                    "synthetic",
                )
                self.assertEqual(set(restricted), {(witness_id, "en")})

        cases = (
            (entry | {"state": "licensed"}, record, "state = 'rights-restricted'"),
            (entry | {"acknowledgement": "Almost the prescribed notice."}, record,
             "exact prescribed excerpt acknowledgement"),
            (entry, record | {"rights_status": "public-domain"}, "rights_status"),
            (entry, record | {"storage": "tracked"}, "text-free restricted storage"),
            (entry, record | {"path": "payload.tsv"}, "text-free restricted storage"),
            (entry, record | {"indexable": True}, "text-free restricted storage"),
        )
        for bad_entry, bad_record, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(tool.SourceError, message):
                    tool.restricted_witness_table(
                        {"restricted_witnesses": [bad_entry]},
                        {artifact_id: bad_record},
                        "synthetic",
                    )

        with self.assertRaisesRegex(tool.SourceError, "rights-restricted witness"):
            tool.side_text(
                {
                    "english": {
                        "witness": witness_id,
                        "artifact": artifact_id,
                        "element": "dialogue",
                    }
                },
                "en", {}, restricted, {artifact_id: record},
                "synthetic/dialogue", "synthetic",
            )


class OrdinaryPage(unittest.TestCase):
    """The real day.js, over the real files, under node.

    A stub DOM rather than a browser: what is being held is the join and the
    filtering, which are the parts that can be wrong without failing.
    """

    def setUp(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not installed")
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written")

    def test_the_page_loads_the_shared_seating_before_its_renderer(self) -> None:
        page = DAY_HTML.read_text(encoding="utf-8")
        self.assertLess(
            page.index('<script src="ordinary-seating.js"></script>'),
            page.index('<script src="day.js"></script>'),
        )

    def test_definite_omission_dominates_unknown_conditions(self) -> None:
        script = r"""
const S = require('./src/web/browser/liturgy/ordinary-seating.js');
const file = {
  variants: [{group: 'choice', options: [
    {id: 'a', default: true}, {id: 'b', default: false}
  ]}],
  sections: [{key: 'section', elements: [{
    key: 'element', alternatives: [], conditions: [
      {kind: 'include-when-any', predicates: ['unknown-fact']},
      {kind: 'omit-when-option', group: 'choice', options: ['b']}
    ]
  }]}]
};
const definite = S.resolveElements(file, {choice: 'b'}, {});
const unresolved = S.resolveElements(file, {choice: 'a'}, {});
file.sections[0].elements[0].conditions.push(
  {kind: 'include-when-any', predicates: ['known-false']});
const laterFalse = S.resolveElements(
  file, {choice: 'a'}, {'known-false': false});
let conflict = null;
try { S.selectionMap(file, ['a', 'b']); }
catch (error) { conflict = String(error && error.message || error); }
process.stdout.write(JSON.stringify({
  definite, unresolved, laterFalse, conflict,
  adventSunday: S.predicateFacts({
    settled: true, weekday: 'sunday', season: 'advent',
    nature: 'solemnity-or-sunday'
  }),
  feast: S.predicateFacts({
    settled: true, weekday: 'thursday', season: 'ordinary-time', nature: 'feast'
  }),
  unsettled: S.predicateFacts({
    settled: false, weekday: 'sunday', season: 'ordinary-time', nature: 'sunday'
  })
}));
"""
        run = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True,
            cwd=ROOT, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report["definite"]["shown"], [])
        self.assertEqual(report["definite"]["unresolved"], [])
        self.assertEqual(report["unresolved"]["shown"], [])
        self.assertEqual(len(report["unresolved"]["unresolved"]), 1)
        self.assertEqual(report["laterFalse"]["shown"], [])
        self.assertEqual(report["laterFalse"]["unresolved"], [])
        self.assertIn("conflicting Ordinary options", report["conflict"])
        self.assertEqual(
            report["adventSunday"],
            {
                "sunday-outside-advent-and-lent": False,
                "sunday-or-solemnity": True,
            },
        )
        self.assertEqual(
            report["feast"],
            {
                "sunday-outside-advent-and-lent": False,
                "solemnity-or-feast": True,
                "sunday-or-solemnity": False,
            },
        )
        self.assertEqual(report["unsettled"], {})

    def test_reading_first_hierarchy_and_event_sequence(self) -> None:
        """The Instrument keeps identity, reading, and actions in authored order."""
        page = DAY_HTML.read_text(encoding="utf-8")
        identity = page.index('<header class="reader-identity"')
        title = page.index('id="celebration-title"')
        notice = page.index('<p id="coverage-notice"')
        mass = page.index('<main id="reader-document"')
        actions = page.index('<nav class="reader-actions"')
        date_surface = page.index('<dialog id="date-surface"')
        self.assertLess(identity, title)
        self.assertLess(title, notice)
        self.assertLess(notice, mass)
        self.assertLess(mass, actions)
        self.assertLess(actions, date_surface)
        main_opening = page[mass:page.index(">", mass) + 1]
        self.assertIn('tabindex="-1"', main_opening)
        self.assertIn('aria-busy="true"', main_opening)
        notice_opening = page[notice:page.index(">", notice) + 1]
        self.assertIn('role="note"', notice_opening)
        self.assertIn(" hidden", notice_opening)
        self.assertEqual(page.count('data-reader-action="'), 4)
        for action, surface in (
            ("date", "date"),
            ("contents", "contents"),
            ("mode", "mode"),
            ("details", "details"),
        ):
            button = page.index(f'data-reader-action="{action}"')
            button_opening = page[
                page.rfind("<button", 0, button):page.index(">", button) + 1
            ]
            self.assertIn(f'aria-controls="{surface}-surface"', button_opening)
            self.assertIn('aria-expanded="false"', button_opening)
        scripts = [
            '<script src="assembly-model.js"></script>',
            '<script src="ordinary-seating.js"></script>',
            '<script src="day.js"></script>',
            '<script src="reader-state.js"></script>',
            '<script src="reader-state-adapters.js"></script>',
            '<script src="reader-shell.js"></script>',
            '<script src="day-reader.js"></script>',
        ]
        positions = [page.index(script) for script in scripts]
        self.assertEqual(positions, sorted(positions))

        report = self.run_harness()
        sequence = report["pentecost_10_sequence"]
        digest = hashlib.sha256(
            json.dumps(sequence, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(len(sequence), 205)
        self.assertEqual(
            digest,
            "e43b1727e55428383661223497fcdc5e492026df58c00be90f16df023411cf8d",
        )

        sequence = report["ot_18_sequence"]
        digest = hashlib.sha256(
            json.dumps(sequence, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(len(sequence), 67)
        self.assertEqual(
            digest,
            "ea501e6d426d345d30e217f61395d54801d69f339f2fa1c24927cf6ef1325abd",
        )

    def test_ordered_mass_text_contract_for_both_missals(self) -> None:
        """Navigation must not alter the text-bearing event stream.

        The harness hashes received text, explicitly omitting nodes marked
        presentation-only. Speaker and role cues therefore cannot change this
        digest; the postconciliar movement records the ICEL quarantine and the
        current Proper corpus, while the separate cue test holds accessibility.
        """
        report = self.run_harness()
        expected = {
            "pentecost_10_text": (
                205,
                "37053a4e0de66568700c5320d433217ccfb65c601f3bd0d1f1b4c9106e4802dc",
            ),
            "ot_18_text": (
                67,
                "b49c8f64f4bf81dbb01f373d9d90ea9ba55bf60ec3f0f0faffd188a127161368",
            ),
        }
        for key, (count, wanted_digest) in expected.items():
            rows = report[key]
            digest = hashlib.sha256(
                json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(rows), count, key)
            self.assertEqual(digest, wanted_digest, key)

    def test_the_page_states_what_it_withholds(self) -> None:
        report = self.run_harness()
        self.assertNotIn("Lord, have mercy.", report["kyrie"])
        self.assertIn("Not shown: its English.", report["kyrie"])
        self.assertIn("approved-english-publication-restriction", report["kyrie"])
        self.assertNotIn(ICEL_SOURCE_ID, report["kyrie"])
        self.assertNotIn(ICEL_ACKNOWLEDGEMENT, report["kyrie"])
        self.assertIn("WE therefore, humbly pray", report["te_igitur_1861"])
        self.assertNotIn("used by permission", report["te_igitur_1861"])

    def test_the_propers_are_read_in_the_order_the_mass_is_said(self) -> None:
        """The whole point of the frame, over the real Easter Sunday formulary.

        Not a spot check of two placements: the full reading order, so that a
        seat moved to a plausible neighbour fails here rather than serving a
        Mass whose parts are all present and in the wrong order.
        """
        report = self.run_harness()
        self.assertEqual(report["easter_1962"], [
            "Introit",
            "praeparatio/kyrie-eleison",
            "praeparatio/gloria-in-excelsis",
            "Collect",
            "Epistle",
            "Gradual", "Alleluia", "Sequence",
            "Gospel",
            "oblatio/credo-in-unum-deum",
            "Offertory",
            "Secret",
            "praefatio/praefatio-communis",
            "praefatio/sanctus",
            "canon/te-igitur",
            "canon/forma-corporis",
            "canon/forma-sanguinis",
            "communio/pater-noster",
            "communio/agnus-dei",
            "Communion",
            "Postcommunion",
            "conclusio/dominus-vobiscum-ite-missa-est",
        ])
        self.assertEqual(
            report["event_kinds"], ["begin_section", "ordinary_element", "proper"]
        )

    def test_stable_forms_are_seated_without_combining_their_propers(self) -> None:
        """Christmas's four authored forms remain four distinct Masses.

        Form identity supersedes the historical flattened projection: the
        seating engine receives exactly one form and must neither manufacture
        a composite frame nor discard a source row from that form.
        """
        report = self.run_harness()
        self.assertEqual(
            report["nativity_forms"],
            [
                {"id": "vigil", "broke": False, "seated": 11,
                 "before": 0, "after": 0, "total": 11},
                {"id": "night", "broke": False, "seated": 11,
                 "before": 0, "after": 0, "total": 11},
                {"id": "dawn", "broke": False, "seated": 10,
                 "before": 0, "after": 0, "total": 10},
                {"id": "day", "broke": False, "seated": 11,
                 "before": 0, "after": 0, "total": 11},
            ],
        )

    def test_an_outside_layer_element_still_holds_the_place_of_its_proper(self) -> None:
        """Absence does not forfeit a seat.

        The invariant Ordinary has a seat for the postconciliar Collect, but the
        variable prayer itself belongs to the Propers layer. The day's Collect
        is still set down immediately after that seat, so a reader sees the
        boundary between layers at the moment the prayer falls due.
        """
        report = self.run_harness()
        self.assertEqual(report["postconciliar_collect"],
                         ["ritus-initiales/collecta", "Collect"])

    def test_a_language_nobody_holds_is_offered_and_says_why(self) -> None:
        """Partial language coverage stays visible and never becomes fallback.

        A language is offered whether or not a given element holds it, and a
        reader who asks for it must be told, at every element that is silent,
        under which recorded reason — never handed a page that has quietly gone
        blank. The reasons are different reasons and must not be
        interchangeable.

        SUPERSEDES the reading of 2026-08-01, which held that NEITHER missal's
        Latin was here and that the 1962's whole absence was
        `latin-not-transcribed`, work nobody had done. The 1861 witness's facing
        Latin column has since been transcribed and is carried, so 112 of that
        file's 195 elements now hold their Latin and the Te igitur — the example
        this test used for the absent case — is one of them. What remains absent
        there is absent for one of three source-specific reasons: eight blocks
        contain a 1962 prayer or form without facing Latin, four belong to the
        abolished second-oration regime, and seventy-one are the witness's own
        English apparatus. So the absent case is now taken on an element that
        really is absent, and the held case is asserted beside it, because a
        control that offers a language must be tested on both.

        The postconciliar file now carries partial English and partial
        antecedent Latin. It must neither describe the Latin as wholly absent
        nor silently fall back to English where an element has no Latin.
        """
        report = self.run_harness()
        self.assertEqual(
            [one["lang"] for one in report["languages"]["postconciliar"]], ["en", "la"])
        self.assertEqual(
            [one["held"] for one in report["languages"]["postconciliar"]], [0, 20])
        self.assertEqual(
            [one["held"] for one in report["languages"]["roman-1962"]], [189, 112])
        # The Latin the 1962 file does not hold is exactly the elements the
        # preamble's three reasons partition; the next test asserts those counts
        # from the other side.
        elements = report["languages"]["roman-1962"][1]["elements"]
        self.assertEqual(elements - 112, 77)

        pater = report["kyrie_in_each"]
        self.assertNotIn("Our Father, who art in heaven", pater["en"])
        self.assertIn("Not shown: its English.", pater["en"])
        self.assertIn("approved-english-publication-restriction", pater["en"])
        self.assertIn("Pater noster, qui es in cœlis", pater["la"])
        self.assertNotIn("Not shown: its Latin.", pater["la"])

        greeting = report["greeting_in_each"]
        self.assertNotIn("The grace of our Lord Jesus Christ", greeting["en"])
        self.assertIn("Not shown: its English.", greeting["en"])
        self.assertIn("approved-english-publication-restriction", greeting["en"])
        self.assertIn("Not shown: its Latin.", greeting["la"])
        self.assertIn("element-spans-mixed-matter", greeting["la"])

        # Held: the facing column was read, so the Latin stands in its own right
        # and no reason is offered for a silence there is not.
        canon = report["te_igitur_in_each"]
        self.assertIn("WE therefore, humbly pray", canon["en"])
        self.assertNotIn("WE therefore, humbly pray", canon["la"])
        self.assertIn("TE igitur, clementissime Pater", canon["la"])
        self.assertNotIn("Not shown: its Latin.", canon["la"])
        self.assertNotIn("no-facing-latin", canon["la"])

        # Absent: this offertory prayer is one of the eight 1962 prayers/forms
        # the book sets to the full measure in English, so the Latin side names
        # its narrow reason and only that reason.
        accendat = report["accendat_in_each"]
        self.assertIn("May the Lord enkindle", accendat["en"])
        self.assertNotIn("May the Lord enkindle", accendat["la"])
        self.assertIn("Not shown: its Latin.", accendat["la"])
        self.assertIn("no-facing-latin", accendat["la"])
        self.assertNotIn("editio-typica", accendat["la"])

    def test_the_reason_is_stated_once_and_referred_to_after_that(self) -> None:
        """Two copies of a reason are two reasons waiting to disagree.

        Printed in full at every element it covers, the 1861 Latin reason ran to
        one copy of the same 400 characters per element the moment a reader
        asked for the Latin. It is stated in the preamble, with how far it
        reaches, and the elements name it.

        The reach is what moved, not the rule: one blanket reason is now three
        exact source classifications. In the 1962 target frame their emitted
        counts are 8, 2, and 67 after six explicit exclusions; source-wide they
        account for 8, 4, and 71 rows. The preamble must state every emitted
        reason once and say how far it goes, covered elements must refer to it
        without repeating it, and an element that holds Latin must not carry a
        reason at all.
        """
        report = self.run_harness()
        preamble = report["preamble_1962"]
        self.assertIn("no-facing-latin", preamble)
        self.assertIn("8 of 189 elements", preamble)
        self.assertIn("not-in-the-1962-ordo", preamble)
        self.assertIn("2 of 189 elements", preamble)
        self.assertIn("witness-own-english", preamble)
        self.assertIn("67 of 189 elements", preamble)
        self.assertNotIn("undefined", preamble)
        self.assertIn("no-facing-latin", report["accendat_in_each"]["la"])
        self.assertNotIn("no-facing-latin", report["te_igitur_in_each"]["la"])

    def test_the_speaker_is_named_and_a_name_is_not_a_mark(self) -> None:
        """Who is speaking, in words, and never a ℣ standing over a response.

        SUPERSEDES a ruling of this same test, 2026-08-01. It formerly held that
        the Ordinary set ℟ for the book's "R.". The maintainer's complaint was
        that the priest's and the server's parts could not be told apart and
        that the ℣/℟ letters were doing that job badly; the proposed fix, to set
        the book's "P." as ℣, would have introduced an error, and the evidence
        is in the book's own rows:

            priest   P. I confess to Almighty God, &c.
            server   R. May Almighty God be merciful to thee…
            server   R. I confess to Almighty God…
            priest   P. May Almighty God be merciful unto you…

        "P." marks the PRIEST and "R." marks a RESPONSE — two axes, printed in
        one column. In the fourth row the priest's line IS the response, so a ℣
        there would say "versicle" over a response. And in two rubric elements
        "P." is not a speaker mark at all but an abbreviation inside running
        text. So each is now set as the word it abbreviates.

        The marks are not merely dropped, which is the part that is easy to get
        wrong: 28 of the 39 marked elements hold a two-party dialogue inside ONE
        element, whose `speaker` field names the first line only. A leading mark
        is redundant with the speaker and goes; an INTERIOR mark is the only
        record that the speaker changed, and stays.

        Both halves of the original ruling that still hold are kept: the initial
        that is not a mark, and ℣/℟ outside the Ordinary, where `versicled` is
        untouched and the propers still use them.
        """
        report = self.run_harness()
        held = report["versicles_1861"]
        self.assertIn("Priest", held, "the speaker is named, not lettered")
        self.assertIn("Response", held)
        self.assertNotIn("R. And with thy spirit", held,
                         "the raw mark is never left in the reading face")
        self.assertNotIn("℣", held, "a versicle mark must never stand over a response")
        # The leading mark repeats the element's own speaker and is dropped;
        # what follows it is the words, not another tag.
        self.assertNotIn("Priest Priest", held)

        raw = report["raw_vr"]
        self.assertEqual(raw["received"], "V. Literal call. R. Literal response.")
        self.assertEqual(raw["turns"], [], "opaque text is never split into turns")
        self.assertEqual(raw["vr_marks"], 0)
        self.assertEqual(raw["cues"], ["P"], "priest is a speaker, not a versicle")

    def test_explicit_turns_keep_role_speaker_accessibility_and_language_apart(self) -> None:
        """Structured turns are lossless presentation inside one element.

        The crossed server-versicle and priest-response rows prove the visible
        glyph comes only from the explicit dialogue role. Speaker-only rows
        prove a priest does not imply a versicle. Presentation cues have one
        accessible English name, are absent from the received text, and turn
        rows acquire neither event IDs nor semantic destinations.
        """
        report = self.run_harness()
        english = report["structured_english"]
        self.assertEqual(english["dialogue_count"], 1)
        self.assertEqual(
            english["received"],
            "Server call.Priest response.Priest part.Server part.Bow.",
        )
        self.assertEqual(
            english["turns"],
            [
                {
                    "speaker": "server", "dialogue_role": "versicle",
                    "action": None, "id": None, "semantic_id": None,
                    "labels": ["Versicle — Server"],
                    "cues": [{"mark": "℣", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Server call."}],
                    "received": "Server call.",
                },
                {
                    "speaker": "priest", "dialogue_role": "response",
                    "action": None, "id": None, "semantic_id": None,
                    "labels": ["Response — Priest"],
                    "cues": [{"mark": "℟", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Priest response."}],
                    "received": "Priest response.",
                },
                {
                    "speaker": "priest", "dialogue_role": None,
                    "action": None, "id": None, "semantic_id": None,
                    "labels": ["Priest"],
                    "cues": [{"mark": "P", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Priest part."}],
                    "received": "Priest part.",
                },
                {
                    "speaker": "server", "dialogue_role": None,
                    "action": None, "id": None, "semantic_id": None,
                    "labels": ["Server"],
                    "cues": [{"mark": "S", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Server part."}],
                    "received": "Server part.",
                },
                {
                    "speaker": None, "dialogue_role": None,
                    "action": "true", "id": None, "semantic_id": None,
                    "labels": [], "cues": [],
                    "texts": [{"lang": "en", "text": "Bow."}],
                    "received": "Bow.",
                },
            ],
        )

        latin = report["structured_latin"]
        self.assertEqual(latin["dialogue_count"], 1)
        self.assertEqual(latin["received"], "Versus.Responsum.")
        self.assertEqual(
            [row["texts"] for row in latin["turns"]],
            [
                [{"lang": "la", "text": "Versus."}],
                [{"lang": "la", "text": "Responsum."}],
            ],
        )
        self.assertEqual([row["received"] for row in latin["turns"]],
                         ["Versus.", "Responsum."])
        self.assertNotEqual(len(english["turns"]), len(latin["turns"]),
                            "one language's turns must not leak into the other")

        real = report["real_orate_latin"]
        self.assertEqual(real["dialogue_count"], 1)
        self.assertEqual(
            [row["text"] for row in real["source_turns"]],
            real["source_text"].split("\n"),
        )
        self.assertEqual(
            [row["texts"][0]["text"] for row in real["rendered_turns"]],
            [row["text"] for row in real["source_turns"]],
        )
        self.assertEqual(
            [
                (row["speaker"], row["dialogue_role"], row["labels"], row["cues"])
                for row in real["rendered_turns"]
            ],
            [
                (
                    "priest", "versicle", ["Versicle — Priest"],
                    [{"mark": "℣", "aria_hidden": "true"}],
                ),
                (
                    "all", "response", ["Response — All"],
                    [{"mark": "℟", "aria_hidden": "true"}],
                ),
            ],
        )
        self.assertTrue(real["rendered_turns"][1]["received"].startswith("R. Suscipiat"))
        self.assertTrue(all(
            row["id"] is None and row["semantic_id"] is None
            for row in real["rendered_turns"]
        ))

    def run_harness(self) -> dict:
        run = subprocess.run(
            ["node", "-e", HARNESS],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)


class FormularyPage(unittest.TestCase):
    """The direct-formulary entrance shares the reading-first page hierarchy."""

    def test_title_first_hierarchy_and_closed_reader_surfaces(self) -> None:
        page = FORMULARY_HTML.read_text(encoding="utf-8")
        identity = page.index('<header class="reader-identity"')
        title = page.index('id="formulary-title"')
        notice = page.index('<p id="coverage-notice"')
        proper = page.index('<main id="reader-document"')
        actions = page.index('<nav class="reader-actions"')
        browse = page.index('<dialog id="browse-surface"')
        self.assertLess(identity, title)
        self.assertLess(title, notice)
        self.assertLess(notice, proper)
        self.assertLess(proper, actions)
        self.assertLess(actions, browse)
        self.assertEqual(page.count('data-reader-action="'), 4)
        for action, surface in (
            ("browse", "browse"),
            ("contents", "contents"),
            ("mode", "mode"),
            ("details", "details"),
        ):
            button = page.index(f'data-reader-action="{action}"')
            button_opening = page[
                page.rfind("<button", 0, button):page.index(">", button) + 1
            ]
            self.assertIn(f'aria-controls="{surface}-surface"', button_opening)
            self.assertIn('aria-expanded="false"', button_opening)
            dialog = page.index(f'<dialog id="{surface}-surface"')
            dialog_opening = page[dialog:page.index(">", dialog) + 1]
            self.assertNotIn(" open", dialog_opening)
            self.assertLess(dialog, page.index("</dialog>", dialog))
        browse_end = page.index("</dialog>", browse)
        self.assertLess(browse, page.index('id="browse-form"'))
        self.assertLess(page.index('id="browse-form"'), browse_end)
        styles = [
            '<link rel="stylesheet" href="liturgy.css">',
            '<link rel="stylesheet" href="reader-shell.css">',
            '<link rel="stylesheet" href="propers-reader.css">',
            '<link rel="stylesheet" href="reader-instrument.css">',
        ]
        positions = [page.index(style) for style in styles]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('<link rel="stylesheet" href="day-missal.css">', page)
        scripts = [
            '<script src="ordinary-seating.js"></script>',
            '<script src="reader-state.js"></script>',
            '<script src="reader-state-adapters.js"></script>',
            '<script src="reader-shell.js"></script>',
            '<script src="propers-reader.js"></script>',
        ]
        positions = [page.index(script) for script in scripts]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('<script src="liturgy.js"></script>', page)

    def test_renderer_keeps_each_missals_propers_in_source_order(self) -> None:
        expected = {
            "roman-1962": (
                "advent-1",
                10,
                "9b8a7c8c853d9363ebeb2c5aa9c19292f3af0dc3e240c209c49a892c06941ee6",
            ),
            "postconciliar": (
                "ot-18",
                11,
                "3747fa005cf696dca44389aae29904967e4960187a866ac72928b8963846b4fd",
            ),
        }
        for missal, (key, count, wanted_digest) in expected.items():
            file = json.loads((PROPERS / f"{missal}.json").read_text(encoding="utf-8"))
            mass = next(one for one in file["masses"] if one["key"] == key)
            names = [proper["name"] for proper in mass["propers"]]
            digest = hashlib.sha256(
                json.dumps(names, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(names), count, missal)
            self.assertEqual(digest, wanted_digest, missal)

        source = FORMULARY_JS.read_text(encoding="utf-8")
        traversal = source.index("for (const proper of propers)")
        self.assertLess(source.index("formularyTitle.textContent"), traversal)
        self.assertLess(source.index("formularyMeta.textContent"), traversal)
        self.assertIn("reading.appendChild(T.renderProper(proper", source[traversal:])

    def test_text_bearing_proper_structures_remain_fixed(self) -> None:
        """The full Proper records, including current FDLC oration provenance."""
        expected = {
            "roman-1962": (
                "advent-1",
                10,
                "a5fdf977ad1519d1b16242d0536026b3d267a8e9434db3b4c95c8ee911d92911",
            ),
            "postconciliar": (
                "ot-18",
                11,
                "1a9a860550b7d969c3838fe256bc7af10a61904b6feecc964f780c3a1bdb7cbc",
            ),
        }
        keys = (
            "name", "form", "incipit", "text", "translations", "untranslated", "citations"
        )
        for missal, (key, count, wanted_digest) in expected.items():
            file = json.loads((PROPERS / f"{missal}.json").read_text(encoding="utf-8"))
            mass = next(one for one in file["masses"] if one["key"] == key)
            rows = [{field: proper.get(field) for field in keys} for proper in mass["propers"]]
            digest = hashlib.sha256(
                json.dumps(
                    rows,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(rows), count, missal)
            self.assertEqual(digest, wanted_digest, missal)

    def test_day_reading_missal_hierarchy_and_event_contract_remain_fixed(self) -> None:
        page = DAY_HTML.read_text(encoding="utf-8")
        self.assertLess(page.index('id="celebration-title"'), page.index('id="reader-document"'))
        self.assertIn('data-reader-mode="read"', page)
        self.assertIn('data-reader-surface="contents"', page)
        self.assertIn('data-reader-surface="mode"', page)
        self.assertNotIn("annotation-control", page)
        self.assertNotIn("Annotation placeholder.", page)
        self.assertNotIn("annotation-control", DAY_JS.read_text(encoding="utf-8"))


class ReadingContentsPage(unittest.TestCase):
    """Generated navigation stays a DOM-only view of the rendered Mass."""

    def setUp(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not installed")

    def test_both_pages_load_a_closed_empty_semantic_contents_dialog(self) -> None:
        cases = (
            (DAY_HTML, '<script src="day-reader.js"></script>', "Mass contents"),
            (
                FORMULARY_HTML,
                '<script src="propers-reader.js"></script>',
                "Formulary contents",
            ),
        )
        for path, page_script, accessible_name in cases:
            page = path.read_text(encoding="utf-8")
            reading = page.index('<main id="reader-document"')
            action = page.index('data-reader-action="contents"')
            contents = page.index('<dialog id="contents-surface"')
            script = page.index(page_script)
            self.assertLess(reading, action, path.name)
            self.assertLess(action, contents, path.name)
            self.assertLess(reading, contents, path.name)
            self.assertLess(contents, script, path.name)
            action_opening = page[
                page.rfind("<button", 0, action):page.index(">", action) + 1
            ]
            self.assertIn('aria-controls="contents-surface"', action_opening, path.name)
            self.assertIn('aria-expanded="false"', action_opening, path.name)
            dialog_opening = page[contents:page.index(">", contents) + 1]
            self.assertIn('data-reader-surface="contents"', dialog_opening, path.name)
            self.assertIn(
                'aria-labelledby="contents-surface-title"', dialog_opening, path.name
            )
            self.assertNotIn(" open", dialog_opening, path.name)
            end = page.index("</dialog>", contents)
            heading = page.index('id="contents-surface-title"', contents)
            nav = page.index("<nav", heading)
            nav_open_end = page.index(">", nav)
            nav_close = page.index("</nav>", nav_open_end)
            self.assertLess(contents, heading, path.name)
            self.assertLess(heading, nav, path.name)
            self.assertLess(nav_close, end, path.name)
            nav_opening = page[nav:nav_open_end + 1]
            self.assertIn("data-reader-contents", nav_opening, path.name)
            self.assertIn(f'aria-label="{accessible_name}"', nav_opening, path.name)
            self.assertEqual(page[nav_open_end + 1:nav_close].strip(), "", path.name)
            self.assertNotIn(
                '<script src="reading-contents.js"></script>', page, path.name
            )

    def test_each_page_supplies_only_its_rendered_semantic_landmarks(self) -> None:
        day = DAY_JS.read_text(encoding="utf-8")
        self.assertIn("ReadingContents.rebuild({", day)
        self.assertIn(".ordinary-division", day)
        call = self._contents_call(day)
        self.assertIn(
            ".ordinary-frame > .annotated > .annotated-text > .proper > .proper-name",
            call,
        )
        self.assertNotIn(".ordinary-head", call)

        formulary = FORMULARY_JS.read_text(encoding="utf-8")
        call = self._contents_call(formulary)
        self.assertIn(".proper > .proper-name", call)
        self.assertNotIn(".ordinary-division", call)
        rendered = formulary.index("renderMass(mass, bible")
        self.assertLess(rendered, formulary.index("rebuildContents();", rendered))

    def test_rebuild_follows_dom_order_and_is_idempotent_without_hash_links(self) -> None:
        run = subprocess.run(
            ["node", "-e", CONTENTS_HARNESS],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report["first_labels"], ["Beginning", "The Canon", "Gospel"])
        self.assertEqual(
            report["first_ids"],
            ["celebration-title", "reading-destination-02", "reading-destination-03"],
        )
        self.assertEqual(report["first_tabindexes"], ["-1", "-1", "-1"])
        self.assertEqual(report["hash_before"], report["hash_after"])
        self.assertTrue(report["scrolled"])
        self.assertTrue(report["focused"])

        self.assertEqual(report["second_labels"], ["Beginning", "Collect"])
        self.assertEqual(report["second_count"], 2)
        self.assertEqual(report["second_ids"], ["celebration-title", "reading-destination-02"])
        self.assertEqual(report["obsolete_id"], "")
        self.assertIsNone(report["obsolete_tabindex"])
        self.assertFalse(report["hidden_after_rebuild"])
        self.assertTrue(report["hidden_after_clear"])
        self.assertEqual(report["count_after_clear"], 0)

        source = READING_CONTENTS_JS.read_text(encoding="utf-8")
        self.assertNotIn("location.hash", source)
        self.assertNotIn("href", source)

    @staticmethod
    def _contents_call(source: str) -> str:
        start = source.index("ReadingContents.rebuild({")
        return source[start:source.index("});", start) + 3]


class ProperPlacementNotesPage(unittest.TestCase):
    """Placement notes report only facts carried by seated Proper events."""

    def setUp(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not installed")

    def test_day_alone_loads_placement_notes_before_its_renderer(self) -> None:
        day = DAY_HTML.read_text(encoding="utf-8")
        self.assertNotIn('proper-placement-notes.js', day)
        self.assertLess(
            day.index('<script src="day.js"></script>'),
            day.index('<script src="day-reader.js"></script>'),
        )

        formulary = FORMULARY_HTML.read_text(encoding="utf-8")
        self.assertNotIn("proper-placement-notes", formulary)
        scripts = [
            '<script src="../shared/browser-core.js"></script>',
            '<script src="ordinary-seating.js"></script>',
            '<script src="reader-state.js"></script>',
            '<script src="reader-state-adapters.js"></script>',
            '<script src="reader-shell.js"></script>',
            '<script src="propers-reader.js"></script>',
        ]
        positions = [formulary.index(script) for script in scripts]
        self.assertEqual(positions, sorted(positions))
        for script in scripts:
            self.assertEqual(formulary.count(script), 1, script)
        self.assertNotIn('<script src="liturgy.js"></script>', formulary)

        # Bind the page to the controller it actually loads. This guards the
        # dependency contract and load order without pinning unrelated bytes in
        # either the HTML or a retired controller.
        controller = FORMULARY_READER_JS.read_text(encoding="utf-8")
        bindings = [
            "const T = window.Triptych;",
            "const Contract = window.LiturgyReaderState;",
            "const Adapters = window.LiturgyReaderStateAdapters;",
            "const Shell = window.TriptychReaderShell;",
        ]
        binding_positions = [controller.index(binding) for binding in bindings]
        self.assertEqual(binding_positions, sorted(binding_positions))

    def test_real_seats_supply_exact_factual_notes_and_no_placeholder(self) -> None:
        run = subprocess.run(
            ["node", "-e", PLACEMENT_NOTES_HARNESS],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)

        self.assertEqual(
            report["roman_note"],
            "Within the Ordinary, this Proper is seated after its declared anchor. "
            "Seat citation: Ritus servandus IV, 2.",
        )
        self.assertEqual(
            report["postconciliar_note"],
            "Within the Ordinary, this Proper is seated after its declared anchor. "
            "Seat citation: Ordo Missae nn. 14-16.",
        )
        self.assertIsNone(report["unseated"])
        self.assertIsNone(report["missing_locus"])
        self.assertTrue(report["events_unchanged"])
        self.assertNotIn("Annotation placeholder.", report["all_text"])

    def test_controls_are_idempotent_independent_and_keyboard_accessible(self) -> None:
        run = subprocess.run(
            ["node", "-e", PLACEMENT_NOTES_DOM_HARNESS],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)

        self.assertEqual(report["control_count"], 2)
        self.assertEqual(report["note_ids"], [
            "proper-placement-note-01", "proper-placement-note-02"
        ])
        self.assertEqual(report["controls"], report["note_ids"])
        self.assertTrue(report["both_open"])
        self.assertFalse(report["first_open_after_escape"])
        self.assertTrue(report["second_still_open"])
        self.assertTrue(report["focus_restored"])
        self.assertEqual(report["hash_before"], report["hash_after"])
        self.assertEqual(report["heading_text"], "Introit")
        self.assertTrue(report["notes_are_siblings"])
        self.assertEqual(report["first_role"], "note")
        self.assertEqual(report["first_label"], "Show placement note for Introit")

    def test_notes_are_url_free_and_hidden_in_print(self) -> None:
        source = PLACEMENT_NOTES_JS.read_text(encoding="utf-8")
        self.assertNotIn("location", source)
        self.assertNotIn("history", source)
        self.assertNotIn("Annotation placeholder.", source)

        css = DAY_MISSAL_CSS.read_text(encoding="utf-8")
        self.assertIn('content: "Why here?"', css)
        print_at = css.index("@media print")
        print_css = css[print_at:]
        self.assertIn(".proper-placement-toggle", print_css)
        self.assertIn(".proper-placement-note", print_css)
        self.assertIn("display: none !important", print_css)

        self.assertEqual(
            hashlib.sha256(READING_CONTENTS_JS.read_bytes()).hexdigest(),
            "01067b1208dc6468aecd278328043acc83d3c2de31bd149b66f1ac0383340f3d",
        )


# A DOM small enough to write here and faithful enough to prove the join.
#
# The shared machinery is the REAL browser-core.js and not a second stub of it.
# What is being held is the join, the filtering and the setting, and every one
# of those runs partly in code both pages share: a stub of `notice` or of
# `versicled` would pass while the page they actually load did something else.
# Only the things that reach the network or the URL are replaced.
HARNESS = r"""
const fs = require('fs');
function node(tag) {
  return { tagName: tag, className: '', textContent: '', lang: null, hidden: false,
    children: [], attrs: {}, style: {},
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelectorAll() { return []; }, addEventListener() {},
    text() { let o = this.textContent || '';
      for (const c of this.children) o += (c.text ? c.text() : String(c.data || '')); return o; },
    receivedText() {
      if (this.attrs['data-presentation-only']) return '';
      let o = this.textContent || '';
      for (const c of this.children) {
        o += c.receivedText ? c.receivedText() : String(c.data || '');
      }
      return o;
    } };
}
const ids = {};
global.document = { createElement: node, createTextNode: (t) => ({
    data: t, text: () => t, receivedText: () => t }),
  createDocumentFragment: () => node('#fragment'),
  getElementById: (id) => (ids[id] = ids[id] || node('div')),
  body: { classList: { toggle() {} }, appendChild() {} }, addEventListener() {} };
global.window = { location: { search: '' }, addEventListener() {},
  MassAssembly: { derive: () => ({}) }, matchMedia: null };
global.window.OrdinarySeating = require(
  './src/web/browser/liturgy/ordinary-seating.js');

eval(fs.readFileSync('src/web/browser/shared/browser-core.js', 'utf8'));
global.window.Triptych = Object.assign({}, global.window.Triptych, {
  fillSelect(s, i) { s.filled = i; }, loadJSON: async () => ({}),
  readHash: () => new Map(), writeHash() {}, onHashChange() {}, onArrowStep() {},
  loadBibles: async () => ({ ok: false, message: 'stub' }), fillBibleSelect() {},
  setInlineNotice() {}, fail() {}, statusLine() {} });

let src = fs.readFileSync('src/web/browser/liturgy/day.js', 'utf8');
src = src.replace('  start();',
  '  global.__probe = { renderElement, elementShows, state, ordinaryPreamble, ' +
  'seats, seatPropers, shownElements, massEvents };');
eval(src);
const P = global.__probe;
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const pc = read('src/web/data/structure/ordinary/postconciliar.json');
const tlm = read('src/web/data/structure/ordinary/roman-1962.json');
const all = (f) => f.sections.flatMap((s) => s.elements);
const hasClass = (n, wanted) => String(n.className || '').split(/\s+/).includes(wanted);
function descendants(root, wanted) {
  const out = [];
  function visit(one) {
    if (hasClass(one, wanted)) out.push(one);
    for (const child of one.children || []) visit(child);
  }
  visit(root);
  return out;
}
function dialogueReport(rendered) {
  return descendants(rendered, 'ordinary-turn').map((row) => ({
    speaker: row.attrs['data-speaker'] || null,
    dialogue_role: row.attrs['data-dialogue-role'] || null,
    action: row.attrs['data-action'] || null,
    id: row.attrs.id || null,
    semantic_id: row.attrs['data-semantic-id'] || null,
    labels: descendants(row, 'visually-hidden').map((one) => one.text()),
    cues: descendants(row, 'cue-mark').map((one) => ({
      mark: one.attrs['data-cue'] || null,
      aria_hidden: one.attrs['aria-hidden'] || null
    })),
    texts: descendants(row, 'ordinary-turn-text').map((one) => ({
      lang: one.lang, text: one.text()
    })),
    received: row.receivedText()
  }));
}
/* The frame with a real formulary poured into it, as one flat sequence: a
   proper by its name, an element by its key. This is what the page renders, in
   the order it renders it. */
function pour(file, calendar, key, formId) {
  const mass = read('src/web/data/structure/propers/' + calendar + '.json')
    .masses.find((m) => m.key === key);
  const form = formId && (mass.forms || []).find((one) => one.id === formId);
  if (formId && !form) throw new Error('missing stable form ' + key + '/' + formId);
  const propers = form ? form.propers : mass.propers;
  const frame = P.shownElements(file);
  const placed = P.seatPropers(propers || [], P.seats(file, frame));
  const events = P.massEvents(frame, placed);
  const out = [];
  for (const event of events) {
    if (event.kind === 'proper') out.push(event.proper.name);
    if (event.kind === 'proper_choice') {
      out.push('Choice: ' + event.group);
    }
    if (event.kind === 'ordinary_element') out.push(event.element.key);
  }
  const properCount = (event) => event.kind === 'proper_choice'
    ? event.options.reduce((total, option) => total + option.rows.length, 0)
    : event.kind === 'proper' ? 1 : 0;
  const count = (placement) => events.reduce((total, event) =>
    total + (event.placement === placement ? properCount(event) : 0), 0);
  const sequence = events.map((event) => {
    if (event.kind === 'begin_section') {
      return 'begin_section:' + event.section.key;
    }
    if (event.kind === 'ordinary_element') {
      return 'ordinary_element:' + event.element.key;
    }
    if (event.kind === 'proper_choice') {
      return 'proper_choice:' + event.placement + ':' + event.group + ':' +
        event.options.map((option) => option.id + '=' + option.rows.map(
          (row) => row.proper.name).join('+')).join('|');
    }
    return 'proper:' + event.placement + ':' + event.proper.name;
  });
  const text = events.map((event) => {
    if (event.kind === 'begin_section') return event.section.name;
    if (event.kind === 'ordinary_element') {
      return P.renderElement(event.element, file).receivedText();
    }
    if (event.kind === 'proper_choice') {
      return JSON.stringify({
        group: event.group, basis: event.basis,
        options: event.options.map((option) => ({
          id: option.id,
          propers: option.rows.map((row) => ({
            name: row.proper.name, form: row.proper.form,
            incipit: row.proper.incipit, text: row.proper.text,
            translations: row.proper.translations,
            untranslated: row.proper.untranslated,
            citations: row.proper.citations
          }))
        }))
      });
    }
    const proper = event.proper;
    return JSON.stringify({
      name: proper.name, form: proper.form, incipit: proper.incipit,
      text: proper.text, translations: proper.translations,
      untranslated: proper.untranslated, citations: proper.citations
    });
  });
  return { order: out, broke: placed.broke, seated: count('seated'),
    before: count('before'), after: count('after'),
    kinds: Array.from(new Set(events.map((event) => event.kind))).sort(),
    sequence: sequence, text: text };
}

// Landmarks of the frame, one per position the reading order names. Anything
// not a landmark and not a proper is dropped, so the assertion is about order.
const MARKS = new Set(['praeparatio/kyrie-eleison', 'praeparatio/gloria-in-excelsis',
  'oblatio/credo-in-unum-deum', 'praefatio/praefatio-communis', 'praefatio/sanctus',
  'canon/te-igitur', 'canon/forma-corporis', 'canon/forma-sanguinis',
  'communio/pater-noster', 'communio/agnus-dei',
  'conclusio/dominus-vobiscum-ite-missa-est']);
const easter = pour(tlm, 'roman-1962', 'easter-sunday');
const pentecost10 = pour(tlm, 'roman-1962', 'pentecost-10');
const ot18 = pour(pc, 'postconciliar', 'ot-18');
const nativity = ['vigil', 'night', 'dawn', 'day'].map((id) => ({
  id: id, result: pour(pc, 'postconciliar', 'nativity', id)
}));
const collect = pour(pc, 'postconciliar', 'easter-sunday').order;
const seat = collect.indexOf('ritus-initiales/collecta');

/* The same element read in each language the file declares, which is what the
   language control offers. Nothing is re-derived here: the languages come from
   the file, and the page is asked for each of them in turn. */
function inEach(file, key) {
  const element = all(file).find((e) => e.key === key);
  const out = {};
  for (const one of file.languages) {
    P.state.ordinaryLang = one.lang;
    out[one.lang] = P.renderElement(element, file).text();
  }
  P.state.ordinaryLang = null;
  return out;
}

/* Synthetic rows hold renderer semantics that must not depend on an artifact's
   current coverage. Each language owns an explicit, complete set of turns; a
   speaker and a dialogue role deliberately cross so neither can imply the
   other. */
const syntheticFile = {
  languages: [
    {lang: 'en', held: 1, elements: 1, absent: 'english'},
    {lang: 'la', held: 1, elements: 1, absent: 'latin'}
  ],
  translations: [], absences: []
};
const structured = {
  key: 'synthetic/structured', kind: 'dialogue', speaker: null,
  name: null, latin_incipit: null, locus: null, note: null, variant: null,
  absent: {english: null, latin: null},
  translations: [
    {lang: 'en', source_id: 'synthetic-en', rights: 'project-created',
      text: 'Server call.\nPriest response.\nPriest part.\nServer part.\nBow.',
      turns: [
        {key: 'server-call', speaker: 'server', dialogue_role: 'versicle',
          action: null, text: 'Server call.'},
        {key: 'priest-response', speaker: 'priest', dialogue_role: 'response',
          action: null, text: 'Priest response.'},
        {key: 'priest-part', speaker: 'priest', dialogue_role: null,
          action: null, text: 'Priest part.'},
        {key: 'server-part', speaker: 'server', dialogue_role: null,
          action: null, text: 'Server part.'},
        {key: 'bow', speaker: null, dialogue_role: null,
          action: true, text: 'Bow.'}
      ]},
    {lang: 'la', source_id: 'synthetic-la', rights: 'project-created',
      text: 'Versus.\nResponsum.',
      turns: [
        {key: 'versus', speaker: 'priest', dialogue_role: 'versicle',
          action: null, text: 'Versus.'},
        {key: 'responsum', speaker: 'all', dialogue_role: 'response',
          action: null, text: 'Responsum.'}
      ]}
  ]
};
P.state.ordinaryLang = 'en';
const structuredEnglish = P.renderElement(structured, syntheticFile);
P.state.ordinaryLang = 'la';
const structuredLatin = P.renderElement(structured, syntheticFile);
P.state.ordinaryLang = null;

/* Raw V./R. is intentionally opaque. The priest field may provide P as visual
   furniture, but it must not manufacture a versicle or split the source. */
const raw = {
  key: 'synthetic/raw', kind: 'dialogue', speaker: 'priest',
  name: null, latin_incipit: null, locus: null, note: null, variant: null,
  absent: {english: null, latin: 'synthetic'},
  translations: [{lang: 'en', source_id: 'synthetic-en',
    rights: 'project-created', text: 'V. Literal call. R. Literal response.'}]
};
P.state.ordinaryLang = 'en';
const rawRendered = P.renderElement(raw, syntheticFile);
P.state.ordinaryLang = null;
const orateElement = all(pc).find(
  (e) => e.key === 'praeparatio-donorum/orate-fratres');
const orateLatin = (orateElement.translations || []).find((one) => one.lang === 'la');
P.state.ordinaryLang = 'la';
const orateRendered = P.renderElement(orateElement, pc);
P.state.ordinaryLang = null;

process.stdout.write(JSON.stringify({
  languages: { postconciliar: pc.languages, 'roman-1962': tlm.languages },
  kyrie_in_each: inEach(pc, 'ritus-communionis/pater-noster'),
  te_igitur_in_each: inEach(tlm, 'canon/te-igitur'),
  accendat_in_each: inEach(tlm, 'oblatio/accendat-in-nobis'),
  greeting_in_each: inEach(pc, 'ritus-initiales/salutatio'),
  preamble_1962: P.ordinaryPreamble(tlm).text(),
  versicles_1861: P.renderElement(
    all(tlm).find((e) => e.key === 'praeparatio/dominus-vobiscum'), tlm).text(),
  kyrie: P.renderElement(all(pc).find((e) => e.key.endsWith('/kyrie')), pc).text(),
  te_igitur_1861: P.renderElement(all(tlm).find((e) => e.key === 'canon/te-igitur'), tlm).text(),
  easter_1962: easter.order.filter((one) => MARKS.has(one) || one.indexOf('/') < 0),
  nativity_forms: nativity.map((one) => ({
    id: one.id, broke: one.result.broke,
    seated: one.result.seated, before: one.result.before,
    after: one.result.after,
    total: one.result.seated + one.result.before + one.result.after
  })),
  postconciliar_collect: collect.slice(seat, seat + 2),
  event_kinds: easter.kinds,
  pentecost_10_sequence: pentecost10.sequence,
  pentecost_10_text: pentecost10.text,
  ot_18_sequence: ot18.sequence,
  ot_18_text: ot18.text,
  structured_english: {
    turns: dialogueReport(structuredEnglish),
    received: structuredEnglish.receivedText(),
    dialogue_count: descendants(structuredEnglish, 'ordinary-dialogue').length
  },
  structured_latin: {
    turns: dialogueReport(structuredLatin),
    received: structuredLatin.receivedText(),
    dialogue_count: descendants(structuredLatin, 'ordinary-dialogue').length
  },
  raw_vr: {
    received: rawRendered.receivedText(),
    turns: dialogueReport(rawRendered),
    vr_marks: descendants(rawRendered, 'vr-mark').length,
    cues: descendants(rawRendered, 'cue-mark').map((one) => one.attrs['data-cue'])
  },
  real_orate_latin: {
    source_text: orateLatin && orateLatin.text,
    source_turns: orateLatin && orateLatin.turns,
    rendered_turns: dialogueReport(orateRendered),
    dialogue_count: descendants(orateRendered, 'ordinary-dialogue').length
  }
}));
"""


CONTENTS_HARNESS = r"""
const fs = require('fs');

class Element {
  constructor(tag, text) {
    this.tagName = tag;
    this._text = text || '';
    this.children = [];
    this.attrs = {};
    this.listeners = {};
    this.hidden = false;
    this.ownerDocument = null;
    this.parent = null;
    this.removed = false;
    this.candidates = [];
  }
  get id() { return this.attrs.id || ''; }
  set id(value) { if (value) this.attrs.id = value; else delete this.attrs.id; }
  get textContent() {
    return this._text + this.children.filter((one) => !one.removed)
      .map((one) => one.textContent).join('');
  }
  set textContent(value) { this._text = value; this.children = []; }
  appendChild(child) {
    child.parent = this;
    child.ownerDocument = this.ownerDocument;
    this.children.push(child);
    return child;
  }
  replaceChildren(...children) {
    this.children = [];
    for (const child of children) this.appendChild(child);
  }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return Object.hasOwn(this.attrs, name) ? this.attrs[name] : null; }
  hasAttribute(name) { return Object.hasOwn(this.attrs, name); }
  removeAttribute(name) { delete this.attrs[name]; }
  addEventListener(kind, listener) { this.listeners[kind] = listener; }
  click() { this.listeners.click(); }
  scrollIntoView() { this.scrolled = true; }
  focus() { this.focused = true; }
  remove() { this.removed = true; }
  querySelectorAll(selector) {
    if (selector === '.proper-ref') {
      return this.children.filter((one) => one.attrs.class === 'proper-ref' && !one.removed);
    }
    return this.candidates;
  }
  cloneNode(deep) {
    const copy = new Element(this.tagName, this._text);
    copy.attrs = Object.assign({}, this.attrs);
    if (deep) for (const child of this.children) copy.appendChild(child.cloneNode(true));
    return copy;
  }
}

const all = [];
const doc = {
  createElement(tag) { return register(new Element(tag)); },
  querySelectorAll(selector) {
    if (selector === '[id]') return all.filter((one) => one.id);
    const match = selector.match(/^\[([^\]]+)\]$/);
    return match ? all.filter((one) => one.hasAttribute(match[1])) : [];
  }
};
function register(node) { node.ownerDocument = doc; all.push(node); return node; }
function heading(label, reference) {
  const node = register(new Element('h2', label));
  if (reference) {
    const ref = register(new Element('span', reference));
    ref.setAttribute('class', 'proper-ref');
    node.appendChild(ref);
  }
  return node;
}

global.document = doc;
global.window = { location: { hash: '#date=2026-08-02&missal=roman-1962' } };
eval(fs.readFileSync('src/web/browser/liturgy/reading-contents.js', 'utf8'));

const beginning = heading('Tenth Sunday after Pentecost');
beginning.id = 'celebration-title';
const division = heading('The Canon');
const gospel = heading('Gospel', 'Matthew 1:1');
const collect = heading('Collect');
const reading = register(new Element('main'));
reading.candidates = [division, gospel];
const disclosure = register(new Element('details'));
disclosure.hidden = true;
const nav = register(new Element('nav'));
const options = { beginning, reading, disclosure, nav, selector: '.semantic-landmark' };

const first = window.ReadingContents.rebuild(options);
const hashBefore = window.location.hash;
nav.children[2].click();
const hashAfter = window.location.hash;
const report = {
  first_labels: nav.children.map((one) => one.textContent),
  first_ids: first.map((one) => one.id),
  first_tabindexes: first.map((one) => one.getAttribute('tabindex')),
  hash_before: hashBefore,
  hash_after: hashAfter,
  scrolled: gospel.scrolled === true,
  focused: gospel.focused === true
};

reading.candidates = [collect];
const second = window.ReadingContents.rebuild(options);
Object.assign(report, {
  second_labels: nav.children.map((one) => one.textContent),
  second_count: nav.children.length,
  second_ids: second.map((one) => one.id),
  obsolete_id: gospel.id,
  obsolete_tabindex: gospel.getAttribute('tabindex'),
  hidden_after_rebuild: disclosure.hidden
});
window.ReadingContents.clear(options);
report.hidden_after_clear = disclosure.hidden;
report.count_after_clear = nav.children.length;
process.stdout.write(JSON.stringify(report));
"""


PLACEMENT_NOTES_HARNESS = r"""
const fs = require('fs');
const Seating = require('./src/web/browser/liturgy/ordinary-seating.js');
global.window = {};
eval(fs.readFileSync(
  'src/web/browser/liturgy/proper-placement-notes.js', 'utf8'));

function events(calendar, massKey) {
  const ordinary = JSON.parse(fs.readFileSync(
    'src/web/data/structure/ordinary/' + calendar + '.json', 'utf8'));
  const structure = JSON.parse(fs.readFileSync(
    'src/web/data/structure/propers/' + calendar + '.json', 'utf8'));
  const mass = structure.masses.find((one) => one.key === massKey);
  const shown = Seating.shownElements(ordinary);
  const placed = Seating.seatPropers(mass.propers, Seating.seats(ordinary, shown));
  return Seating.massEvents(shown, placed);
}

const roman = events('roman-1962', 'pentecost-10');
const postconciliar = events('postconciliar', 'ot-18');
const romanIntroit = roman.find(
  (event) => event.kind === 'proper' && event.proper.name === 'Introit');
const postconciliarGospel = postconciliar.find(
  (event) => event.kind === 'proper' && event.proper.name === 'Gospel');
const before = JSON.stringify({romanIntroit, postconciliarGospel});

const romanFacts = window.ProperPlacementNotes.facts(romanIntroit);
const postconciliarFacts = window.ProperPlacementNotes.facts(postconciliarGospel);
const unseated = window.ProperPlacementNotes.facts({
  kind: 'proper', proper: {name: 'Unseated'}, placement: 'before', seat: null
});
const missingLocus = window.ProperPlacementNotes.facts({
  kind: 'proper', proper: {name: 'Uncited'}, placement: 'seated',
  seat: {where: 'after', locus: ''}
});

process.stdout.write(JSON.stringify({
  roman_note: romanFacts && romanFacts.text,
  postconciliar_note: postconciliarFacts && postconciliarFacts.text,
  unseated,
  missing_locus: missingLocus,
  events_unchanged: before === JSON.stringify({romanIntroit, postconciliarGospel}),
  all_text: [romanFacts && romanFacts.text, postconciliarFacts && postconciliarFacts.text]
    .filter(Boolean).join('\n')
}));
"""


PLACEMENT_NOTES_DOM_HARNESS = r"""
const fs = require('fs');

class Element {
  constructor(tag, text) {
    this.tagName = tag.toUpperCase();
    this._text = text || '';
    this.children = [];
    this.attrs = {};
    this.listeners = {};
    this.className = '';
    this.hidden = false;
    this.ownerDocument = null;
    this.parentElement = null;
  }
  get textContent() {
    return this._text + this.children.map((child) => child.textContent || '').join('');
  }
  set textContent(value) { this._text = String(value); this.children = []; }
  get id() { return this.getAttribute('id') || ''; }
  set id(value) { this.setAttribute('id', value); }
  get nextSibling() {
    if (!this.parentElement) return null;
    const at = this.parentElement.children.indexOf(this);
    return this.parentElement.children[at + 1] || null;
  }
  appendChild(child) {
    child.parentElement = this;
    child.ownerDocument = this.ownerDocument;
    this.children.push(child);
    return child;
  }
  insertBefore(child, before) {
    child.parentElement = this;
    child.ownerDocument = this.ownerDocument;
    const at = before ? this.children.indexOf(before) : -1;
    if (at < 0) this.children.push(child); else this.children.splice(at, 0, child);
    return child;
  }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) {
    return Object.hasOwn(this.attrs, name) ? this.attrs[name] : null;
  }
  hasAttribute(name) { return Object.hasOwn(this.attrs, name); }
  addEventListener(kind, listener) { this.listeners[kind] = listener; }
  click() { this.listeners.click({currentTarget: this}); }
  keydown(key) {
    let prevented = false;
    this.listeners.keydown({
      key,
      currentTarget: this,
      preventDefault() { prevented = true; }
    });
    return prevented;
  }
  focus() { this.focused = true; this.ownerDocument.activeElement = this; }
  matches(selector) {
    const classMatch = selector.match(/^\.([a-z0-9-]+)$/);
    return Boolean(classMatch && this.className.split(/\s+/).includes(classMatch[1]));
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  querySelectorAll(selector) {
    const selectors = selector.split(',').map((one) => one.trim());
    const found = [];
    function visit(node) {
      for (const child of node.children) {
        if (selectors.some((one) => child.matches && child.matches(one))) found.push(child);
        visit(child);
      }
    }
    visit(this);
    return found;
  }
}

const all = [];
const document = {
  activeElement: null,
  createElement(tag) {
    const node = new Element(tag);
    node.ownerDocument = document;
    all.push(node);
    return node;
  }
};
global.document = document;
global.window = {location: {hash: '#date=2026-08-02&missal=roman-1962'}};
eval(fs.readFileSync(
  'src/web/browser/liturgy/proper-placement-notes.js', 'utf8'));

function proper(name) {
  const body = document.createElement('section');
  body.className = 'proper';
  const heading = document.createElement('h5');
  heading.className = 'proper-name';
  heading.textContent = name;
  body.appendChild(heading);
  return {body, heading};
}

const introit = proper('Introit');
const gospel = proper('Gospel');
const introitEvent = {
  kind: 'proper', proper: {name: 'Introit'}, placement: 'seated',
  seat: {where: 'after', locus: 'Ritus servandus IV, 2'}
};
const gospelEvent = {
  kind: 'proper', proper: {name: 'Gospel'}, placement: 'seated',
  seat: {where: 'after', locus: 'Ritus servandus VI, 2'}
};

window.ProperPlacementNotes.add({
  body: introit.body, event: introitEvent, noteId: 'proper-placement-note-01'
});
window.ProperPlacementNotes.add({
  body: introit.body, event: introitEvent, noteId: 'proper-placement-note-01'
});
window.ProperPlacementNotes.add({
  body: gospel.body, event: gospelEvent, noteId: 'proper-placement-note-02'
});

const controls = all.filter((node) => node.className === 'proper-placement-toggle');
const notes = all.filter((node) => node.className === 'proper-placement-note');
const hashBefore = window.location.hash;
controls[0].click();
controls[1].click();
const bothOpen = controls.every((one) => one.getAttribute('aria-expanded') === 'true');
controls[0].keydown('Escape');

process.stdout.write(JSON.stringify({
  control_count: controls.length,
  note_ids: notes.map((one) => one.id),
  controls: controls.map((one) => one.getAttribute('aria-controls')),
  both_open: bothOpen,
  first_open_after_escape: controls[0].getAttribute('aria-expanded') === 'true',
  second_still_open: controls[1].getAttribute('aria-expanded') === 'true',
  focus_restored: controls[0].focused === true && document.activeElement === controls[0],
  hash_before: hashBefore,
  hash_after: window.location.hash,
  heading_text: introit.heading.textContent,
  notes_are_siblings: notes[0].parentElement === introit.body &&
    notes[1].parentElement === gospel.body,
  first_role: notes[0].getAttribute('role'),
  first_label: controls[0].getAttribute('aria-label')
}));
"""


if __name__ == "__main__":
    unittest.main()
