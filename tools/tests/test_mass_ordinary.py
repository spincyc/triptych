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

from argparse import Namespace
from collections import Counter
from copy import deepcopy

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
            # 2026-10-19 (C2 G5): the appointed Pentecost Preface and paschal
            # dismissal stand-ins add two English rights absences and two
            # Latin publication-unresolved absences.
            "appointed-text-printed-with-formulary": (
                2, "unresolved", "rights-unresolved"
            ),
            "approved-english-publication-restriction": (
                27, "rights-restricted", "rights-withheld"
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
            self.assertEqual(set(absence), {"key", "label", "count", "state", "kind"})
            self.assertTrue(absence["label"].strip())
            self.assertEqual(
                absence["state"],
                {
                    "rights-withheld": "rights-restricted",
                    "rights-unresolved": "unresolved",
                }.get(absence["kind"], "unavailable"),
            )
        affected = [
            element for element in elements(file)
            if element["absent"]["english"]
            == "approved-english-publication-restriction"
        ]
        # 27 since 2026-10-19 (C2 G5): the appointed Pentecost Preface and
        # paschal dismissal stand-ins carry the same English restriction.
        self.assertEqual(len(affected), 27)
        for element in affected:
            self.assertFalse(
                any(row["lang"] == "en" for row in (element["translations"] or [])),
                element["key"],
            )

        languages = {one["lang"]: one for one in file["languages"]}
        # 61 elements since 2026-10-19 (C2 G5: two appointed stand-ins).
        self.assertEqual((languages["en"]["held"], languages["en"]["elements"]),
                         (0, 61))
        self.assertEqual((languages["la"]["held"], languages["la"]["elements"]),
                         (20, 61))
        self.assertEqual(languages["en"]["elements"] - languages["en"]["held"], 61)
        self.assertEqual(languages["la"]["elements"] - languages["la"]["held"], 41)
        held_elements = [one for one in elements(file) if one["translations"]]
        wholly_absent = [one for one in elements(file) if not one["translations"]]
        self.assertEqual((len(held_elements), len(wholly_absent)), (20, 41))

        self.assertEqual(len(source["witnesses"]), 1)
        self.assertEqual(source["witnesses"][0]["lang"], "la")
        self.assertEqual(
            {absence["kind"] for absence in source["absences"]},
            {
                "model-gap", "no-exemplar", "not-applicable", "outside-layer",
                "rights-withheld", "witness-gap",
                # 2026-10-19 (C2 G5): a formulary's appointed Preface and
                # dismissal, whose publication basis is not established.
                "rights-unresolved",
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
                            {"key", "speaker", "dialogue_role", "action",
                             "printed_marker", "text"} | ({"gloss"} if turn.get("gloss") is True else set()),
                        )
                        # The reviewed marker is the row's own head letter,
                        # one space, then spoken matter; the row text itself
                        # is never shortened in the generated data.
                        self.assertIn(turn["printed_marker"], (None, "P.", "R."))
                        if turn["printed_marker"] is not None:
                            self.assertTrue(
                                turn["text"].startswith(turn["printed_marker"] + " "),
                                (calendar, element["key"], turn["key"]),
                            )
                        else:
                            self.assertNotRegex(turn["text"], r"^(?:[PRVS]\.|[℣℟])")
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
        } | {("postconciliar", "praeparatio-donorum/orate-fratres", "la")} | {
            # 2026-10-19 (C3): the Canon's proper forms carry the inline rubric
            # for the joining of the hands as an action turn.
            ("roman-1962", "canon/communicantes-continuatio", "la"),
            ("roman-1962", "canon/hanc-igitur-pascha-pentecoste", "la"),
        } | {
            # 2026-10-19 (C4 step 2): the reviewed child rows of ten printed
            # dialogue blocks, in both 1861-derived frames and both columns,
            # and the postconciliar Latin antecedent Preface dialogue and Pax.
            (calendar, key, lang)
            for calendar in ("roman-1962", "roman-pre-1955")
            for key in (
                "praeparatio/introibo-ad-altare-dei",
                "praeparatio/judica-me-deus",
                "praeparatio/emitte-lucem-tuam",
                "praeparatio/confitebor-tibi-in-cithara",
                "praeparatio/gloria-patri",
                "praeparatio/introibo-ad-altare-dei-repetitio",
                "oblatio/per-omnia-saecula",
                "oblatio/sursum-corda",
                "communio/pax-domini",
                "conclusio/dominus-vobiscum-ite-missa-est",
            )
            for lang in ("en", "la")
        } | {
            ("postconciliar", "prex-eucharistica/praefationis-dialogus", "la"),
            ("postconciliar", "ritus-communionis/pax-domini", "la"),
            ("postconciliar", "prex-eucharistica/doxologia", "la"),
        } | {
            # The 1962 n. 1016 Adjutorium has its own two source-backed turns;
            # the pre-1955 frame still uses the unchanged block artifact.
            ("roman-1962", key, lang)
            for key in ['praeparatio/adjutorium-nostrum', 'praeparatio/deus-tu-conversus', 'praeparatio/ostende-nobis', 'praeparatio/domine-exaudi', 'praeparatio/dominus-vobiscum', 'praeparatio/misereatur-tui', 'praeparatio/misereatur-vestri', 'praeparatio/indulgentiam', 'praeparatio/kyrie-eleison', 'praeparatio/christe-eleison', 'praeparatio/kyrie-eleison-repetitio', 'praeparatio/dominus-vobiscum-post-gloriam', 'oblatio/dominus-vobiscum-ante-evangelium', 'oblatio/dominus-vobiscum-ante-offertorium', 'conclusio/dominus-vobiscum-ante-postcommunionem', 'canon/per-omnia-saecula', 'communio/pater-noster', 'communio/per-omnia-saecula-post-libera-nos', 'conclusio/requiescant-in-pace', 'conclusio/initium-sancti-evangelii']
            for lang in ("en", "la")
        }
        # C26 joins are independently checked single-actor Latin bodies;
        # Cummiskey's source-owned English has no new turn partition here.
        expected |= {
            ("roman-1962", "oblatio/" + key, "la")
            for key in ("munda-cor-meum", "dominus-sit-in-corde-meo", "per-evangelica-dicta", "accendat-in-nobis")
        }
        # C26 optional source presentation: English has one source-grounded
        # priest-with-assistants turn; the separate Latin remains priest only.
        expected.add(("roman-1962", "oblatio/per-evangelica-dicta", "en"))
        # Each checked Lasance replacement has its own exact, language-local
        # source partition, including single-actor prayers.
        inventory = tomllib.loads(ROMAN_1962_INVENTORY.read_text())
        replacements = [
            (section["key"], row)
            for section in inventory["sections"]
            for row in section.get("english_replacements", [])
        ]
        self.assertEqual(len(replacements), 101)
        replacement_keys = {("roman-1962", section + "/" + row["element"], "en")
                            for section, row in replacements}
        expected |= replacement_keys
        self.assertEqual(reached, expected)
        # Postconciliar: speakers priest/all; roles only where the 2002
        # Praefationes print versicle and response marks, none for the Pax.
        by_reach = {(calendar, key, lang): turns for calendar, key, lang, turns in found}
        self.assertEqual(
            [(turn["speaker"], turn["dialogue_role"], turn["printed_marker"])
             for turn in by_reach[("postconciliar", "prex-eucharistica/praefationis-dialogus", "la")]],
            [("priest", "versicle", "P."), ("all", "response", "R.")] * 3,
        )
        self.assertEqual(
            [(turn["speaker"], turn["dialogue_role"], turn["printed_marker"])
             for turn in by_reach[("postconciliar", "ritus-communionis/pax-domini", "la")]],
            [("priest", None, "P."), ("all", None, "R.")],
        )
        doxology = by_reach[("postconciliar", "prex-eucharistica/doxologia", "la")]
        # Three source fragments retain the two contiguous target speaker spans;
        # they remain one doxology event. The 2002 target has no V./R. marks.
        self.assertEqual(
            [(turn["speaker"], turn["dialogue_role"], turn["printed_marker"])
             for turn in doxology],
            [("priest", None, None), ("priest", None, "P."), ("all", None, "R.")],
        )
        self.assertEqual(
            [turn["key"] for turn in doxology],
            ["priest-doxology", "priest-conclusion", "people-amen"],
        )
        post_turns = next(
            turns for calendar, key, lang, turns in found
            if (calendar, key, lang)
            == ("postconciliar", "praeparatio-donorum/orate-fratres", "la")
        )
        self.assertEqual(
            [(turn["key"], turn["speaker"], turn["dialogue_role"], turn["action"])
             for turn in post_turns],
            # 2026-10-19 (C4): speakers only. The 2002 Ordo n. 29 (artifact
            # p. 310) prints rubrics naming the priest and the people and no
            # versicle or response mark, so the roles once declared here, which
            # had no stated basis, were withdrawn; turns_basis records the page.
            [("priest-summons", "priest", None, None),
             ("people-response", "all", None, None)],
        )
        self.assertTrue(post_turns[1]["text"].startswith("R. Suscipiat"))
        self.assertEqual([turn["printed_marker"] for turn in post_turns], [None, "R."])
        for calendar, key, lang, turns in found:
            if key.startswith("canon/") and any(turn["action"] is True for turn in turns):
                self.assertEqual(
                    [(turn["key"], turn["speaker"], turn["action"]) for turn in turns],
                    [("oratio", "priest", None), ("iungit-manus", None, True),
                     ("conclusio", None, None)],
                    (calendar, key, lang),
                )
                continue
            # The divided dialogue blocks are held to their partitions by
            # tests/tools/mass-ordinary.test; these are the single-row turns.
            if (calendar.startswith("roman-") and key in roman_elements
                    and (calendar, key, lang) not in replacement_keys):
                self.assertEqual(len(turns), 1, (calendar, key, lang))
                self.assertEqual(turns[0]["speaker"], roman_elements[key])
                self.assertEqual(
                    turns[0]["dialogue_role"],
                    "response" if (calendar, key)
                    == ("roman-1962", "conclusio/deo-gratias") else None,
                )
                # The book's P. marks the priest's row and R. the server's;
                # declaring either never supplies a dialogue role.
                self.assertEqual(
                    turns[0]["printed_marker"],
                    "P." if roman_elements[key] == "priest" else "R.",
                    (calendar, key, lang),
                )

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
        for calendar in ("roman-pre-1955",):
            opaque = next(
                element for element in elements(self.files[calendar])
                # The 1962 frame now has reviewed Adjutorium child rows; the
                # pre-1955 witness still holds this as one opaque block.
                if element["key"] == "praeparatio/adjutorium-nostrum"
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
                "appointment-not-established": 6,
                # Reviewed proper Canon heads now fill their own source gaps.
                # The separate Joseph continuation remains unavailable.
                "communicantes-continuation-english-lacks-1962-clause": 1,
                "no-facing-latin": 4,
                "not-in-the-1962-ordo": 0,
                "preface-not-in-witness": 2,
                "proper-canon-form-not-held": 0,
                "proper-communicantes-english-variant": 0,
                "witness-own-english": 63,
            },
        )
        self.assertEqual(sum(row["count"] for row in roman["absences"]), 76)
        by_key = {element["key"]: element for element in elements(roman)}
        self.assertEqual(
            by_key["oblatio/accendat-in-nobis"]["absent"]["latin"],
            None,
        )
        # 2026-10-19 (C2 G6): both not-in-the-1962-ordo orations are excluded,
        # so the class now accounts only for source rows, not emitted elements.
        self.assertNotIn("conclusio/postcommunio-mundet", by_key)
        self.assertNotIn("conclusio/et-famulos", by_key)
        self.assertEqual(
            by_key["praefatio/rubrica-nota-asterisci"]["absent"]["latin"],
            "witness-own-english",
        )

        pre = self.files["roman-pre-1955"]
        self.assertEqual(
            {row["key"]: row["count"] for row in pre["absences"]},
            # 2026-10-19 (C2 G5): the recension's own appointment stand-ins.
            {
                "appointment-not-established": 6,
                "no-facing-latin": 83,
                "preface-not-in-witness": 2,
                "proper-canon-form-not-held": 12,
            },
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

        This checks the slot vocabulary. A partial recension is checked
        against the canonical corpus-wide vocabulary because an unrepresented
        formulary cannot supply names of its own. A complete recension must
        supply every slot name from its own corpus.
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
            if proper_coverage in {"none", "partial", "structural-only", "inherited-uncollated"}:
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

    def matthias_seating_case(self):
        ordinary = load("roman-1962")
        payload = json.loads((PROPERS / "roman-1962.json").read_text(encoding="utf-8"))
        mass = next(row for row in payload["masses"]
                    if row["key"] == "s-matthiae-apostoli")
        # Keep the real published candidates and source facts; scope only the
        # calendar input to the single Mass whose cross-layer join regressed.
        calendar = {**payload, "masses": [mass]}
        form = {"mass": mass["key"], "form_id": "main",
                "where": "roman-1962/s-matthiae-apostoli/main",
                "full": True, "propers": mass["propers"]}
        return ordinary, calendar, form

    def test_matthias_normal_paschal_candidates_have_exact_ordinary_seats(self) -> None:
        tool = self.tool_module
        ordinary, calendar, form = self.matthias_seating_case()
        facts = calendar["proper_appointment_facts"]
        summary = {"mass": "s-matthiae-apostoli", "form_id": "main",
                   "candidates": 14, "conditional_rows": 1,
                   "choice_groups": 4, "diagnostics": []}
        self.assertEqual(tool.check_appointment_seating(ordinary, [form], facts), [summary])
        self.assertEqual(tool.check_calendar_seating(ordinary, calendar), {
            "calendar": "roman-1962", "full_forms": 1, "nonfull_forms": 0,
            "failures": 0, "source_appointments": [summary]})
        rows = form["propers"]
        self.assertEqual([row["name"] for row in rows], [
            "Introit", "Introit", "Collect", "Epistle", "Gradual", "Tract",
            "Alleluia (Tempore paschali)", "Gospel", "Offertory", "Offertory",
            "Secret", "Communion", "Communion", "Postcommunion"])
        regime = "roman-1962-common-chant-regime"
        outside = {"fact": regime, "in": ["advent", "regular", "tract"]}
        paschal = {"fact": regime, "in": ["paschal"]}
        common = "commune-martyrum-tempore-paschali-1"
        for role in ["Introit", "Offertory", "Communion"]:
            with self.subTest(role=role):
                own, borrowed = [row for row in rows if row["name"] == role]
                anchor = {"mass": form["mass"], "form_id": "main",
                          "proper": role, "occurrence": 1}
                self.assertEqual(own["appointment_identity"], anchor)
                self.assertEqual(borrowed["appointment_identity"],
                                 {**anchor, "occurrence": 2})
                self.assertIsNone(own["taken_from"])
                # AP562/p481/L, after2225, explicitly appoints these normal
                # Paschal chants from Protexisti, Common Martyrs I[15]. The
                # preceding2225 paragraph is a separate votive-only direction.
                self.assertEqual(borrowed["taken_from"], {
                    "mass": common, "form": "", "proper": role,
                    "citation": "Missale Romanum1962 artifact562/printed481 left, "
                    "after2225: tempore paschali, ex Missa Protexisti de Communi "
                    "Martyrum I loco[15]"})
                basis = own["ordinary_disposition"]["basis"]
                for row, option, when in [(own, "outside-paschal", outside),
                                          (borrowed, "paschal", paschal)]:
                    self.assertEqual(row["ordinary_disposition"], {
                        "kind": "alternative", "group": "seasonal-" + role.lower(),
                        "option": option, "basis": basis, "anchor": anchor,
                        "when": when})
        groups = {}
        for row in rows:
            disposition = row.get("ordinary_disposition") or {}
            if disposition.get("kind") == "alternative":
                groups.setdefault(disposition["group"], set()).add(disposition["option"])
        self.assertEqual(groups, {"seasonal-" + role: {"outside-paschal", "paschal"}
                                  for role in ["introit", "acclamation", "offertory", "communion"]})
        conditional = [row for row in rows
                       if (row.get("ordinary_disposition") or {}).get("kind") == "conditional"]
        self.assertEqual([row["name"] for row in conditional], ["Gradual"])
        self.assertEqual(conditional[0]["ordinary_disposition"]["when"], outside)
        alleluia = next(row for row in rows if row["name"] == "Alleluia (Tempore paschali)")
        self.assertEqual(alleluia["taken_from"]["mass"], common)
        self.assertEqual(alleluia["taken_from"]["proper"], "Alleluia")
        self.assertEqual(alleluia["ordinary_disposition"]["when"], paschal)

    def test_matthias_inactive_or_unknown_options_cannot_evade_exact_seat_guards(self) -> None:
        tool = self.tool_module
        ordinary, calendar, form = self.matthias_seating_case()
        original_facts = calendar["proper_appointment_facts"]
        regime = "roman-1962-common-chant-regime"
        false_facts = deepcopy(original_facts)
        held = false_facts[regime]
        # Synthetic negative-control fact: the Paschal options are known false.
        # The unmodified publisher facts leave season explicitly unknown here.
        held.pop("season_values")
        held["mass_values"] = {form["mass"]: {
            "value": "regular", "basis": "Synthetic known non-Paschal guard control."}}
        for state, facts in [("unknown", original_facts), ("false", false_facts)]:
            for role in ["Introit", "Offertory", "Communion", "mixed-seat"]:
                with self.subTest(applicability=state, corruption=role):
                    bad = deepcopy(form)
                    group = "seasonal-" + ("introit" if role == "mixed-seat" else role.lower())
                    row = next(one for one in bad["propers"]
                               if (one.get("ordinary_disposition") or {}).get("group") == group
                               and one["ordinary_disposition"]["option"] == "paschal")
                    row["name"] = ("Communion" if role == "mixed-seat"
                                   else role + " (Tempore paschali)")
                    message = ("anchored Proper group must share one established semantic seat"
                               if role == "mixed-seat" else
                               "alternative Proper group must share one usable semantic Ordinary seat")
                    with self.assertRaisesRegex(tool.SourceError, message):
                        tool.check_appointment_seating(ordinary, [bad], facts)

    def test_john_damascene_paschal_offertory_has_an_exact_declared_seat(self) -> None:
        tool = self.tool_module
        ordinary = tool.build(Namespace(root=str(ROOT / "src/sources"),
                                        calendar="roman-1962"))[0]
        payload = json.loads((PROPERS / "roman-1962.json").read_text(encoding="utf-8"))
        mass = next(row for row in payload["masses"]
                    if row["key"] == "s-ioannis-damasceni-confessoris-ecclesiae-doctoris")
        form = {"mass": mass["key"], "form_id": "main",
                "where": "roman-1962/" + mass["key"] + "/main",
                "full": True, "propers": mass["propers"]}
        slot = next(row for row in ordinary["slots"] if row["key"] == "offertorium")
        self.assertEqual(slot["propers"], ["Offertory"])
        self.assertFalse(slot["qualified"], "the native seat must not admit arbitrary qualifiers")
        summary = {"mass": mass["key"], "form_id": "main", "candidates": 12,
                   "conditional_rows": 1, "choice_groups": 2, "diagnostics": []}
        self.assertEqual(tool.check_appointment_seating(
            ordinary, [form], payload["proper_appointment_facts"]), [summary])
        branches = [row for row in mass["propers"]
                    if (row.get("ordinary_disposition") or {}).get("group")
                    == "john-damascene-offertory"]
        self.assertEqual([row["name"] for row in branches], ["Offertory", "Offertory"])
        self.assertEqual([row["appointment_identity"]["occurrence"] for row in branches], [1, 2])
        self.assertEqual([row["ordinary_disposition"]["option"] for row in branches],
                         ["non-paschal-base", "paschal-body-gap"])
        self.assertEqual(branches[1]["text_status"]["state"], "unavailable")
        self.assertIsNone(branches[1]["text"], "the seat does not supply a missing body")
        self.assertEqual([row["ordinary_disposition"]["when"]["in"] for row in branches],
                         [["tract"], ["paschal"]])

    def test_john_damascene_foreign_offertory_seat_does_not_authorize_execution(self) -> None:
        tool = self.tool_module
        ordinary = tool.build(Namespace(root=str(ROOT / "src/sources"),
                                        calendar="roman-pre-1955"))[0]
        payload = json.loads((PROPERS / "roman-pre-1955.json").read_text(encoding="utf-8"))
        mass = next(row for row in payload["masses"]
                    if row["key"] == "s-ioannis-damasceni-confessoris-ecclesiae-doctoris")
        form = {"mass": mass["key"], "form_id": "main",
                "where": "roman-pre-1955/" + mass["key"] + "/main",
                "full": True, "propers": mass["propers"]}
        before = deepcopy(mass)
        summary = tool.check_appointment_seating(
            ordinary, [form], payload.get("proper_appointment_facts", {}))[0]
        self.assertEqual((summary["candidates"], summary["choice_groups"]), (12, 2))
        notices = {row["sourceIndex"]: row for row in summary["diagnostics"]}
        for index in [7, 8]:
            self.assertEqual(notices[index], {
                "kind": "unsupported-foreign-source-applicability", "sourceIndex": index,
                "source_edition": "roman-1962", "target_edition": "roman-pre-1955"})
        self.assertEqual(mass, before)
        harness = r"""
const assert = require('node:assert/strict');
const S = require(process.argv[1]);
let text = '';
process.stdin.on('data', chunk => { text += chunk; });
process.stdin.on('end', () => {
  const p = JSON.parse(text);
  const shown = p.ordinary.sections.flatMap(section =>
    section.elements.map(element => ({section, element})));
  const seating = S.seats(p.ordinary, shown);
  for (const row of p.rows) {
    assert.equal(row.appointment_applicability.state, 'unresolved');
    assert(S.usableSlotOf(seating, row.name) >= 0);
    assert.throws(() => S.prepareProperAppointments([row], {
      calendar: 'roman-pre-1955', entrance: 'propers'}), /foreign-source/);
    assert.throws(() => S.unframedEvents([row]), /foreign-source/);
    assert.throws(() => S.properUnits([row], seating), /foreign-source/);
  }
});
"""
        checked = subprocess.run(["node", "-e", harness, str(tool.SEATING_MODEL)],
                                 input=json.dumps({"ordinary": ordinary,
                                                   "rows": mass["propers"][7:9]}),
                                 text=True, capture_output=True, timeout=20, check=False)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
    def damascene_seating_case(self):
        ordinary = load("roman-1962")
        payload = json.loads((PROPERS / "roman-1962.json").read_text(encoding="utf-8"))
        mass = next(row for row in payload["masses"]
                    if row["key"] == "s-ioannis-damasceni-confessoris-ecclesiae-doctoris")
        return ordinary, payload, {
            "mass": mass["key"], "form_id": "main",
            "where": "roman-1962/" + mass["key"] + "/main",
            "full": True, "propers": mass["propers"],
        }

    def test_damascene_offertory_keeps_exact_seats_and_distinct_body_owners(self) -> None:
        tool = self.tool_module
        ordinary, payload, form = self.damascene_seating_case()
        expected = {"mass": form["mass"], "form_id": "main", "candidates": 12,
                    "conditional_rows": 1, "choice_groups": 2, "diagnostics": []}
        self.assertEqual(tool.check_appointment_seating(
            ordinary, [form], payload["proper_appointment_facts"]), [expected])
        rows = [row for row in form["propers"] if
                (row.get("ordinary_disposition") or {}).get("group") == "john-damascene-offertory"]
        self.assertEqual([row["name"] for row in rows], ["Offertory", "Offertory"])
        anchor = {"mass": form["mass"], "form_id": "main", "proper": "Offertory", "occurrence": 1}
        self.assertEqual([row["appointment_identity"] for row in rows],
                         [anchor, {**anchor, "occurrence": 2}])
        for row, option, regime in zip(rows, ["non-paschal-base", "paschal-body-gap"],
                                       ["tract", "paschal"]):
            disposition = row["ordinary_disposition"]
            self.assertEqual(disposition["anchor"], anchor)
            self.assertEqual(disposition["option"], option)
            self.assertEqual(disposition["when"],
                             {"fact": "roman-1962-common-chant-regime", "in": [regime]})
        base, paschal = rows
        self.assertEqual(hashlib.sha256(base["text"].encode()).hexdigest(),
                         "b06720237c7314a55174aecedcabdbac4dbbbbd6fa43b11c160c689b703340b4")
        self.assertIsNone(paschal["text"])
        self.assertEqual(paschal["text_status"], {"state": "unavailable", "scope": "proper-body"})
        self.assertEqual(paschal["untranslated"], [{
            "lang": "en", "state": "unavailable",
            "target": {**anchor, "occurrence": 2, "cycle": "all", "extent": "body"},
        }])

    def test_damascene_inactive_and_unknown_paschal_option_keeps_seat_guards(self) -> None:
        tool = self.tool_module
        ordinary, payload, form = self.damascene_seating_case()
        unknown = payload["proper_appointment_facts"]
        inactive = deepcopy(unknown)
        fact = inactive["roman-1962-common-chant-regime"]
        fact.pop("season_values")
        fact["mass_values"] = {form["mass"]: {
            "value": "tract", "basis": "Synthetic known non-Paschal guard control."}}
        for state, facts in [("unknown", unknown), ("inactive", inactive)]:
            self.assertEqual(tool.check_appointment_seating(
                ordinary, [form], facts)[0]["candidates"], len(form["propers"]))
            for name, message in [
                ("Offertory (Tempore paschali)", "share one usable semantic Ordinary seat"),
                ("Communion", "share one established semantic seat"),
            ]:
                with self.subTest(applicability=state, corruption=name):
                    bad = deepcopy(form)
                    row = next(row for row in bad["propers"] if
                               (row.get("ordinary_disposition") or {}).get("option") == "paschal-body-gap")
                    row["name"] = name
                    with self.assertRaisesRegex(tool.SourceError, message):
                        tool.check_appointment_seating(ordinary, [bad], facts)

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
            "typed_coverage",
        }
        for calendar, row in rows.items():
            self.assertEqual(set(row), required, calendar)
            self.assertEqual(row["typed_coverage"]["counts"]["occurrences"], row["elements"])
            for language in row["typed_coverage"]["languages"]:
                original = next(item for item in row["language_coverage"]
                                if item["lang"] == language["lang"])
                self.assertEqual(language["available"], original["held"])
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
                    set(absence), {"key", "label", "lang", "count", "state", "kind"}
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
            # Reviewed proper Canon heads and the separately witnessed
            # Accendat fill their individual sides without adding frame rows.
            [("en", 191, 5), ("la", 125, 71)],
        )
        self.assertEqual(
            [one["key"] for one in roman["exclusions"]],
            [
                # 2026-10-19 (C2 G6): the second-Postcommunion regime and the
                # added prayer Et famulos, on the verified 1962 Ordo passages.
                "conclusio/et-famulos",
                "conclusio/oratio-et-famulos-heading",
                "conclusio/postcommunio-mundet",
                "conclusio/rubrica-oratio-addita",
                "conclusio/rubrica-postcommunio-paschalis",
                "conclusio/rubrica-postcommunio-secunda",
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

    def test_junctions_projections_and_conditional_words_are_closed(self) -> None:
        """C3, 2026-10-19: a cut is an exact prefix; a projection must be word-exact."""
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        projection_id = "edition.synthetic.projection"
        english_id = "artifact.synthetic.junction-en"
        latin_id = "artifact.synthetic.junction-la"
        projected_id = "artifact.synthetic.projected-la"
        appointments = {"canon_form": {
            "variable": "canon_form", "options": [{"id": "proper"}, {"id": "common"}],
            "default": "common", "spans": [],
        }}
        appointed = [{"kind": "appointed", "variable": "canon_form", "options": ["proper"],
                      "basis": "Synthetic heading."}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "english.tsv").write_text(
                "element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\tnotes\n"
                "whole\t10\tprayer\tAlpha beta. * Gamma [delta] epsilon.\tAlpha\t1\tpriest\t\n",
                encoding="utf-8",
            )
            (root / "latin.tsv").write_text(
                "element_key\tseq\tlatin\nwhole\t10\tUnus duo. * Tres [quattuor] quinque.\n",
                encoding="utf-8",
            )
            (root / "projected.tsv").write_text(
                "element_key\tseq\tlatin\ncontinued\t1\tSex septem.\ncontinued\t2\tIungit manus.\n",
                encoding="utf-8",
            )
            library = {
                english_id: {"id": english_id, "path": "english.tsv", "_source_root": root},
                latin_id: {"id": latin_id, "path": "latin.tsv", "_source_root": root},
                projected_id: {"id": projected_id, "path": "projected.tsv", "_source_root": root},
            }
            witnesses = {
                (witness_id, "en"): {"lang": "en", "rights": "public-domain", "artifacts": [english_id]},
                (witness_id, "la"): {"lang": "la", "rights": "public-domain", "artifacts": [latin_id]},
                (projection_id, "la"): {"lang": "la", "rights": "project-created",
                                        "artifacts": [projected_id]},
            }
            absences = {"gap": {"key": "gap", "kind": "witness-gap", "what": "Synthetic."}}
            collated = {"relation": "antecedent", "collation": "collated",
                        "collation_finding": "passage.synthetic", "note": "Synthetic note.",
                        "target_wording": "word-exact"}
            continued = {
                "key": "continued", "after": "whole", "kind": "prayer", "speaker": "priest",
                "absent_english": "gap", "conditions": appointed,
                "latin": {"witness": projection_id, "artifact": projected_id,
                          "elements": ["continued"], "column": "latin"} | collated,
                "latin_turns": [{"key": "oratio", "seq": [1], "speaker": "priest"},
                                {"key": "rubrica", "seq": [2], "action": True}],
            }
            section = {
                "key": "synthetic", "artifact": english_id, "witness": witness_id,
                "artifact_latin": latin_id,
                "english": {"relation": "own"}, "latin": {"relation": "own"},
                "junctions": [{"element": "whole", "through": {"en": "beta.", "la": "duo."},
                               "basis": "Target locus."}],
                "element_provenance": [{"element": "whole", "lang": "la"} | collated],
                "inserted": [continued, {
                    "key": "opening", "before": "whole", "kind": "prayer", "name": "Opening",
                    "text_of": "whole", "through": {"en": "Alpha", "la": "Unus"},
                    "conditions": appointed,
                }],
            }
            built, _ = tool.from_artifact(section, witnesses, {}, absences, library,
                                          "synthetic.toml", {}, appointments)
            by_key = {one["key"]: one for one in built}
            self.assertEqual(list(by_key), ["synthetic/opening", "synthetic/whole",
                                            "synthetic/continued"])
            whole = {row["lang"]: row for row in by_key["synthetic/whole"]["translations"]}
            self.assertEqual(whole["la"]["text"], "Unus duo.")
            self.assertEqual(whole["la"]["coverage_relationship"], "exact-target")
            self.assertEqual(whole["en"]["relation"], "own")
            opening = {row["lang"]: row["text"] for row in by_key["synthetic/opening"]["translations"]}
            self.assertEqual(opening, {"en": "Alpha", "la": "Unus"})
            cont = by_key["synthetic/continued"]
            self.assertIsNone(cont["name"])
            self.assertEqual(cont["absent"], {"english": "gap", "latin": None})

            spans = {"conditional_spans": [{
                "element": "whole", "lang": "la", "text": "[quattuor]",
                "said": {"anchor": "pentecost", "from": -1, "to": 6},
                "rubric": "Said in the window.", "locus": "Target locus."}]}
            plain = {key: value for key, value in section.items() if key != "junctions"}
            built, _ = tool.from_artifact(plain | spans, witnesses, {}, absences, library,
                                          "synthetic.toml", {}, appointments)
            latin = next(row for row in built[1]["translations"] if row["lang"] == "la")
            self.assertEqual(latin["conditional_spans"][0]["said"]["from"], -1)

            def without_wording(block: dict) -> dict:
                return {key: value for key, value in block.items() if key != "target_wording"}

            invalid = (
                ({"junctions": [{"element": "whole", "through": {"en": "a", "la": "duo."},
                                 "basis": "B."}]}, "occurs 2 times|exactly once"),
                ({"junctions": [{"element": "whole", "through": {"la": "duo."},
                                 "basis": "B."}]}, "would pair unlike texts"),
                ({"junctions": [{"element": "whole", "through": {"en": "epsilon.", "la": "quinque."},
                                 "basis": "B."}]}, "cuts nothing"),
                ({"element_provenance": [{"element": "whole", "lang": "la",
                                          "relation": "antecedent", "collation": "uncollated",
                                          "note": "N.", "target_wording": "word-exact"}]},
                 "without a collation"),
                ({"inserted": [continued | {"latin": without_wording(continued["latin"])}]},
                 "without a collated word-exact"),
                ({"inserted": [{key: value for key, value in continued.items()
                                if key != "absent_english"}]}, "names no absence"),
                (spans | {"conditional_spans": [spans["conditional_spans"][0] | {"text": "absent"}]},
                 "exactly once"),
                (spans | {"conditional_spans": [spans["conditional_spans"][0]
                                                | {"said": {"anchor": "nowhere", "from": 0, "to": 1}}]},
                 "declared anchor"),
            )
            for change, message in invalid:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(tool.SourceError, message):
                        tool.from_artifact(section | change, witnesses, {}, absences, library,
                                           "synthetic.toml", {}, appointments)

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
                    {"element": "dialogue", "lang": "en", "parts": parts,
                     "basis": "Synthetic book prints versicle and response marks."},
                    {"element": "dialogue", "lang": "la", "parts": parts,
                     "basis": "Synthetic book prints versicle and response marks."},
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

            # A dialogue role is a reading of the controlling book's marks; a
            # partition that declares one without saying where is refused,
            # and an empty basis is no basis.
            for basis, message in ((None, "dialogue role without a basis"),
                                   ("  ", "empty basis")):
                unbased = dict(section)
                unbased["turn_partitions"] = [
                    {key: value for key, value in partition.items() if key != "basis"}
                    | ({} if basis is None else {"basis": basis})
                    for partition in section["turn_partitions"]
                ]
                with self.subTest(basis=basis), self.assertRaisesRegex(tool.SourceError, message):
                    tool.from_artifact(unbased, witnesses, {}, {}, library, "synthetic.toml")
            # Speakers alone need no basis.
            speakers_only = dict(section)
            speakers_only["turn_partitions"] = [
                {"element": "dialogue", "lang": lang, "parts": [
                    {key: value for key, value in part.items() if key != "dialogue_role"}
                    for part in parts
                ]}
                for lang in ("en", "la")
            ]
            built, _ = tool.from_artifact(
                speakers_only, witnesses, {}, {}, library, "synthetic.toml"
            )
            self.assertTrue(all(
                turn["dialogue_role"] is None
                for translation in built[0]["translations"]
                for turn in translation["turns"]
            ))

    def test_child_rows_split_turns_and_headings_lose_only_reviewed_cues(self) -> None:
        """C4 step 2: reviewed child rows, labels that are not cues, headings."""
        tool = self.tool_module
        witness_id = "edition.synthetic.witness"
        english_id = "artifact.synthetic.child-en"
        latin_id = "artifact.synthetic.child-la"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "english.tsv").write_text(
                "element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\n"
                "antiphon\t401\tdialogue\tAnth. Priest sings.\tAntiphona prima\t1\tpriest\n"
                "antiphon\t402\tdialogue\tR. Server sings.\t\t1\t\n"
                "headed\t5\tdialogue\tR. Server alone.\tR. Responsum solum\t1\tserver\n",
                encoding="utf-8",
            )
            (root / "latin.tsv").write_text(
                "element_key\tseq\tlatin\n"
                "antiphon\t401\tAnt. Sacerdos canit.\n"
                "antiphon\t402\tR. Minister canit.\n"
                "headed\t5\tR. Responsum solum.\n",
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
                {"key": "priest-1", "seq": [401], "speaker": "priest"},
                {"key": "server-1", "seq": [402], "speaker": "server", "printed_marker": "R."},
            ]
            section = {
                "key": "synthetic", "artifact": english_id, "witness": witness_id,
                "artifact_latin": latin_id,
                "english": {"relation": "own"}, "latin": {"relation": "own"},
                "turn_partitions": [
                    {"element": "antiphon", "lang": "en", "parts": parts},
                    {"element": "antiphon", "lang": "la", "parts": parts},
                ],
                "incipit_markers": [{"element": "headed", "printed_marker": "R."}],
            }
            built, _ = tool.from_artifact(section, witnesses, {}, {}, library, "synthetic.toml")
            antiphon, headed = built
            # Several first-child-only element cells still give one element.
            self.assertEqual(antiphon["speaker"], "priest")
            self.assertEqual(antiphon["name"], "Antiphona prima")
            self.assertNotIn("incipit_printed_marker", antiphon)
            for translation in antiphon["translations"]:
                first, second = translation["turns"]
                # The antiphon label is printed matter, not a cue: no marker,
                # kept in the text, and not refused as an undeclared cue.
                self.assertIsNone(first["printed_marker"])
                self.assertTrue(first["text"].startswith(("Ant. ", "Anth. ")))
                self.assertEqual(second["printed_marker"], "R.")
                self.assertEqual(translation["text"], first["text"] + "\n" + second["text"])
            # The heading is set without the reviewed cue; the record keeps it.
            self.assertEqual(headed["name"], "Responsum solum")
            self.assertEqual(headed["latin_incipit"], "Responsum solum")
            self.assertEqual(headed["incipit_printed_marker"], "R.")

            undeclared = dict(section)
            del undeclared["incipit_markers"]
            with self.assertRaisesRegex(tool.SourceError, "undeclared printed cue"):
                tool.from_artifact(undeclared, witnesses, {}, {}, library, "synthetic.toml")
            for markers, message in (
                ([{"element": "headed", "printed_marker": "P."}], "does not open with that marker"),
                ([{"element": "headed", "printed_marker": "V."}], "one of P., R."),
                ([{"element": "absent", "printed_marker": "R."}], "does not hold"),
                ([{"element": "headed"}], "must carry exactly"),
            ):
                wrong = dict(section)
                wrong["incipit_markers"] = markers
                with self.subTest(markers=markers), self.assertRaisesRegex(tool.SourceError, message):
                    tool.from_artifact(wrong, witnesses, {}, {}, library, "synthetic.toml")

    def test_inline_turns_basis_is_a_stated_reading_or_nothing(self) -> None:
        tool = self.tool_module
        base = {"key": "dialogue", "kind": "dialogue", "speaker": "all",
                "absent_english": "gap", "absent_latin": "gap"}
        absences = {"gap": {"key": "gap", "kind": "witness-gap", "what": "Synthetic."}}
        for extra, message in (
            ({"turns_basis": " "}, "empty turns_basis"),
            ({"turns_basis": "Synthetic page."}, "declares no turns"),
        ):
            section = {"key": "synthetic", "elements": [base | extra]}
            with self.subTest(extra=extra), self.assertRaisesRegex(tool.SourceError, message):
                tool.from_inventory(section, {}, {}, absences, {}, {}, "synthetic.toml")

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
                            "label": "Publication basis is unresolved",
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
            "label": "The witness has no facing text",
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
                    ],
                    # A role states where the book prints its mark (C4,
                    # 2026-10-19); without this the turns are refused below.
                    "turns_basis": "Synthetic page, printing both marks.",
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
                            "printed_marker": None, "text": "Server call.",
                        },
                        {
                            "key": "priest-response", "speaker": "priest",
                            "dialogue_role": "response", "action": None,
                            "printed_marker": None, "text": "Priest response.",
                        },
                        {
                            "key": "bow", "speaker": None,
                            "dialogue_role": None, "action": True,
                            "printed_marker": None, "text": "Bow.",
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
                    ({"english_turns": [
                        {"key": "bad-marker", "seq": [10, 20, 30],
                         "speaker": "server", "printed_marker": "V."},
                    ]}, "has printed_marker"),
                    ({"english_turns": [
                        {"key": "marked-action", "seq": [10, 20, 30],
                         "action": True, "printed_marker": "R."},
                    ]}, "is an action and cannot carry"),
                    ({"english_turns": [
                        {"key": "absent-marker", "seq": [10, 20, 30],
                         "speaker": "server", "printed_marker": "R."},
                    ]}, "does not open with that marker"),
                    # 2026-10-19 (C4): a dialogue role with no stated basis,
                    # the shape the withdrawn Orate fratres roles had.
                    ({"english_turns": entry["english_turns"]},
                     "dialogue role in english_turns without a turns_basis"),
                )
                for bad_entry, message in invalid:
                    with self.subTest(message=message):
                        with self.assertRaisesRegex(tool.SourceError, message):
                            tool.structured_turns(
                                bad_entry, "english", library, artifact_id,
                                ["dialogue"], "text", "synthetic/dialogue",
                                "synthetic", parent,
                            )

                # A printed head letter is separated only by a reviewed
                # declaration, never inferred from the string, and a row that
                # opens with one undeclared is refused rather than rendered
                # under two cues.
                (fixture / "marked.tsv").write_text(
                    "element_key\tseq\ttext\n"
                    "marked\t10\tP. Priest summons.\n"
                    "marked\t20\tR. Server answer.\n",
                    encoding="utf-8",
                )
                marked_id = "artifact.synthetic.marked"
                library[marked_id] = {
                    "id": marked_id, "path": "marked.tsv", "_source_root": fixture,
                }
                marked_parent = "P. Priest summons.\nR. Server answer."
                marked = tool.structured_turns(
                    {"english_turns": [
                        {"key": "summons", "seq": [10], "speaker": "priest",
                         "printed_marker": "P."},
                        {"key": "answer", "seq": [20], "speaker": "server",
                         "printed_marker": "R."},
                    ]},
                    "english", library, marked_id, ["marked"], "text",
                    "synthetic/marked", "synthetic", marked_parent,
                )
                self.assertEqual(
                    [(row["printed_marker"], row["dialogue_role"], row["text"])
                     for row in marked],
                    [("P.", None, "P. Priest summons."),
                     ("R.", None, "R. Server answer.")],
                )
                with self.assertRaisesRegex(tool.SourceError, "undeclared printed cue"):
                    tool.structured_turns(
                        {"english_turns": [
                            {"key": "summons", "seq": [10], "speaker": "priest",
                             "printed_marker": "P."},
                            {"key": "answer", "seq": [20], "speaker": "server",
                             "dialogue_role": "response"},
                        ], "turns_basis": "Synthetic page, printing the mark."},
                        "english", library, marked_id, ["marked"], "text",
                        "synthetic/marked", "synthetic", marked_parent,
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
        self.assertNotIn('<script src="day.js"></script>', page)
        self.assertLess(
            page.index('<script src="ordinary-seating.js"></script>'),
            page.index('<script src="reader-optional-runtime.js"></script>'),
        )
        loader = (DAY_HTML.parent / "reader-optional-runtime.js").read_text(encoding="utf-8")
        self.assertIn("new URL('day.js', doc.currentScript.src)", loader)
        self.assertIn("return state.options.ordinary ? loadOrdinary() : Promise.resolve(null);", loader)
        self.assertIn("if (root.TriptychOrdinaryRenderer) resolve(root.TriptychOrdinaryRenderer);", loader)
        self.assertLess(loader.index("script.onload = function ()"),
                        loader.index("doc.head.appendChild(script)"))
        controller = (DAY_HTML.parent / "day-reader.js").read_text(encoding="utf-8")
        ready = controller.index("await window.TriptychReaderOptionalRuntime?.forState(normalized.state);")
        self.assertLess(controller.index("const validation = Contract.validateReaderState(normalized.state);"), ready)
        self.assertLess(ready, controller.index("OrdinaryRenderer = window.TriptychOrdinaryRenderer;", ready))

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
        self.assertEqual(page.count('data-reader-action="'), 5)
        # Study is a direct mode action; the four dialog actions keep their
        # existing aria-controls/expanded contract below.
        self.assertIn('data-reader-action="study" aria-current="false"', page)
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
            '<script src="reader-optional-runtime.js"></script>',
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
        # Re-pinned 2026-10-19 (C2 gaps G5 and G6), diffed against the HEAD
        # ec0816c59 harness: exactly 30 events left Pentecost X and one entered.
        # The 25 Preface rows the 1861 witness prints (eleven Prefaces with
        # their headings and notes) give way to the one typed stand-in
        # praefatio/praefatio-diei, since no formulary, span or default yet
        # appoints that Sunday's Preface; the Sanctus stays. The six conclusio
        # rows of the second-Postcommunion regime and Et famulos are excluded.
        # Every other event, and the common Communicantes and Hanc igitur, is
        # unchanged and in the same order.
        # Re-pinned 2026-10-19 (C2 Preface directions), diffed against the HEAD
        # 799988766 harness, whose digest was the one above: exactly two events
        # left and four entered, all in the Preface. The stand-in
        # praefatio/praefatio-diei and the Sanctus at the common Preface's seat
        # gave way to the 1861 witness's asterisk note, the Trinity Preface
        # heading and Preface, and the Sanctus after a proper Preface, because
        # the Sunday's formulary prints "Praefatio de Ssma Trinitate" (physical
        # PDF p. 471, printed p. 390; RGMR 494 b). Every other event is
        # unchanged and in the same order.
        # Re-pinned 2026-10-19 (C3 Ordinary variables), diffed against the HEAD
        # 839c4b6cd harness: exactly one event entered and none left. The
        # 1962 Canon continues every Communicantes with one shared
        # continuation carrying the clause naming Saint Joseph, so
        # canon/communicantes-continuatio now follows the common form, which
        # is carried as far as its printed junction. Every other event is
        # unchanged and in the same order.
        self.assertEqual(len(sequence), 178)
        self.assertEqual(
            digest,
            "6946cf74b2cbf867cb89304e47784ba7fff0bbed3611c81d799e4567b9f2348f",
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

        The harness freezes the complete DOM-text projection, omitting nodes
        marked presentation-only. Opaque source signs keep their semantic glyph
        and hidden English name in this projection. Separate cue, source-row
        reconstruction and shared copy-owner checks hold those distinct layers.
        """
        report = self.run_harness()
        # Compared with the pinned 7285e3ec9 payloads on 2026-10-01: only
        # c2b1a271b's explicit Psalm numbering/title-unnumbered loci and the
        # collated ot-18 Communion group basis changed. Received prayer text,
        # translations, event order and counts are unchanged.
        # Re-pinned against d3c36e8ea on 2026-10-19 (C4 cue step). Sequences
        # are unchanged; received text changed in exactly three ways: a turn's
        # reviewed printed marker (the 1962 Confiteor, Laus tibi, Suscipiat and
        # Deo gratias rows; the postconciliar Suscipiat response) moved out of
        # the spoken words beside its one structured cue; the `all` Preface
        # dialogue and Pax regained their opening "Priest"; and a final word
        # label is no longer glued to its words ("ResponseAmen." became
        # "Response Amen."), matching every interior label.
        # Re-pinned 2026-10-19 (C2 gap G3): only the Collect, Secret and
        # Postcommunion English absences of Pentecost X changed state, from
        # rights-restricted to unavailable; count and order are unchanged.
        # Re-pinned 2026-10-19 (C2 gaps G5 and G6): the same 30 removals and
        # one typed stand-in as the sequence pin above, diffed against HEAD
        # ec0816c59; every retained event's received text is byte-identical.
        # Re-pinned 2026-10-19 (C2 Preface directions): the same two removals
        # and four additions as the sequence pin above, diffed against HEAD
        # 799988766; every retained event's received text is byte-identical.
        # Re-pinned 2026-10-19 (C3 Ordinary variables), diffed against HEAD
        # 839c4b6cd: the common Communicantes' received text now ends at its
        # printed junction, and one event entered after it, the continuation,
        # whose English is the typed absence
        # communicantes-continuation-english-lacks-1962-clause. Every other
        # event's received text is byte-identical.
        # Re-pinned 2026-10-19 (C4 step 2), diffed against HEAD 1107fdc1a: the
        # sequence is unchanged and exactly 15 events' received text changed,
        # each identical once cue labels, printed P./R. and whitespace are set
        # aside: the ten divided dialogue blocks (their word labels and printed
        # letters became one presentation-only cue per turn row) and five
        # headings that lost a reviewed printed cue (Dominus vobiscum before
        # the Gospel and the Offertory, Laus tibi, Suscipiat, and Per omnia
        # before the Pax).
        # Re-pinned 2026-10-20 (C4 G15): both streams keep their
        # liturgical words and order; typed absence prose now uses the
        # source-owned reader labels instead of storage keys.
        # Re-pinned 2026-10-20 (C4 Adjutorium): one 1962 element's received
        # cue words become the two structured turns established by n. 1016;
        # its 1861 spoken words and semantic event position are unchanged.
        # Re-pinned 2026-10-20 (C4 complete source-turn batch): source-owned
        # child rows replace interior speaker labels with presentation-only
        # cues. Kyrie translation glosses remain exact, named nonspoken notes.
        # Every source word and semantic event position is unchanged.
        # Replayed 2026-10-25: clean 6a1fe6e33 and the current frozen reader
        # produce identical complete 178/67 arrays. These pins include the
        # existing source-qualified R./V. presentation; its hidden role label
        # also enters this DOM-text projection. Copy is checked independently.
        expected = {
            # The 1962 Missal p. 389 (artifact p. 470, n. 1532) specifies
            # Psalm 54:17-18, 20, 23 and 54:2 for this Introit. The held
            # 4b0d33fb baseline reproduces the old pin; only event 26's
            # citation bounds change. All 178 event positions, body words,
            # translation fields and the postconciliar stream stay identical.
            "pentecost_10_text": (
                178,
                "1edc606286d8f909b86af9fa6f2de2c54ade781f731dcf0fed1044d657b19384",
            ),
            # Re-pinned 2026-10-19 (C4 step 2), diffed against HEAD 1107fdc1a:
            # the sequence is unchanged and only the Preface dialogue and the
            # Pax changed, by losing their "Priest"/"Response" word labels now
            # that each turn row carries one presentation-only cue.
            # Re-pinned 2026-10-20 (C4 doxology): only the doxology's
            # stored P./R. letters become independently checked speaker cues.
            # Three source fragments remain two target speaker spans inside
            # one unchanged event; all source words and event order survive.
            # Re-pinned 2026-10-21 against 1498adefe: exactly two of 67
            # events change, only in citation apparatus. The Entrance Antiphon
            # now carries source-checked Vulgate Psalm 69 / Hebrew Psalm 70;
            # the Communion alternative honors John 6's existing unrecorded
            # Hebrew-addressing stance through the shared citation owner.
            # All event positions and every non-citation field are unchanged.
            "ot_18_text": (
                67,
                "f59b35a245b8078c33787bd79148c88d260e27a84a8decc9487842f016bf0b15",
            ),
        }
        for key, (count, wanted_digest) in expected.items():
            rows = report[key]
            digest = hashlib.sha256(
                json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(rows), count, key)
            self.assertEqual(digest, wanted_digest, key)

    def test_explicit_source_paths_are_prepared_before_ordinary_seating(self) -> None:
        report = self.run_harness()["source_path_controls"]
        self.assertEqual(report["principal"], {
            "main/easter-day-second-reading": {"state": "selected", "option": "colossians-3"},
            "main/easter-day-gospel": {"state": "selected", "option": "john-20"},
        })
        self.assertEqual(report["primary_names"].count("Second Reading"), 1)
        self.assertEqual(report["primary_names"].count("Gospel"), 1)
        self.assertEqual(report["vigil_material"], {"family": "cycles", "cycle": "A"})
        for key, reason in {
            "raw": "source path membership must be prepared",
            "missing": "fixture requires explicit resolved source appointments",
            "mixed": "mix incompatible correlated source paths",
            "unknown_evening": "source-condition-unresolved",
            "wrong_cycle": "source-path-inapplicable",
        }.items():
            self.assertIn(reason, report["refused"][key], key)

    def test_the_page_states_what_it_withholds(self) -> None:
        report = self.run_harness()
        self.assertNotIn("Lord, have mercy.", report["kyrie"])
        self.assertIn("Not shown: its English.", report["kyrie"])
        self.assertIn("Approved English text is not published here", report["kyrie"])
        self.assertNotIn(ICEL_SOURCE_ID, report["kyrie"])
        self.assertNotIn(ICEL_ACKNOWLEDGEMENT, report["kyrie"])
        self.assertIn("Wherefore, we humbly pray and beseech Thee", report["te_igitur_1962"])
        self.assertNotIn("used by permission", report["te_igitur_1962"])

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
            # Easter Sunday's formulary prints the Paschal Preface (2026-10-19),
            # so the Sanctus is seated after that proper Preface
            # (praefatio/sanctus-post-praefationem, not a mark this list
            # tracks) and not at the common Preface's place.
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

        The postconciliar English is unavailable. The Roman frame has checked
        historical English and Latin bodies, including separately witnessed
        proper Canon heads and the Mame Accendat. Its remaining gaps keep their
        source-specific reasons; a reader must never receive another language
        silently in place of the requested side.
        """
        report = self.run_harness()
        self.assertEqual(
            [one["lang"] for one in report["languages"]["postconciliar"]], ["en", "la"])
        self.assertEqual(
            [one["held"] for one in report["languages"]["postconciliar"]], [0, 20])
        self.assertEqual(
            [one["held"] for one in report["languages"]["roman-1962"]], [191, 125])
        # The reviewed five new English heads and four new Latin heads plus
        # Accendat add five held sides in each language without adding elements.
        # The remaining Latin sides match the preamble's typed partition.
        elements = report["languages"]["roman-1962"][1]["elements"]
        self.assertEqual(elements - 125, 71)

        pater = report["kyrie_in_each"]
        self.assertNotIn("Our Father, who art in heaven", pater["en"])
        self.assertIn("Not shown: its English.", pater["en"])
        self.assertIn("Approved English text is not published here", pater["en"])
        self.assertIn("Pater noster, qui es in cœlis", pater["la"])
        self.assertNotIn("Not shown: its Latin.", pater["la"])

        greeting = report["greeting_in_each"]
        self.assertNotIn("The grace of our Lord Jesus Christ", greeting["en"])
        self.assertIn("Not shown: its English.", greeting["en"])
        self.assertIn("Approved English text is not published here", greeting["en"])
        self.assertIn("Not shown: its Latin.", greeting["la"])
        self.assertIn("This element mixes inherited and changed wording", greeting["la"])

        # Held: the facing column was read, so the Latin stands in its own right
        # and no reason is offered for a silence there is not.
        canon = report["te_igitur_in_each"]
        self.assertIn("Wherefore, we humbly pray and beseech Thee", canon["en"])
        self.assertNotIn("Wherefore, we humbly pray and beseech Thee", canon["la"])
        self.assertIn("TE igitur, clementissime Pater", canon["la"])
        self.assertNotIn("Not shown: its Latin.", canon["la"])
        self.assertNotIn("The 1861 witness prints this block only in English", canon["la"])

        # Accendat's independently checked Mame Latin is now held. This does
        # not turn the old Cummiskey column into a witness for those words.
        accendat = report["accendat_in_each"]
        self.assertIn("May the Lord enkindle", accendat["en"])
        self.assertNotIn("May the Lord enkindle", accendat["la"])
        self.assertNotIn("Not shown: its Latin.", accendat["la"])
        self.assertIn("Accéndat in nobis", accendat["la"])
        self.assertNotIn("The 1861 witness prints this block only in English", accendat["la"])
        self.assertNotIn("editio-typica", accendat["la"])

    def test_the_reason_is_stated_once_and_referred_to_after_that(self) -> None:
        """State every absence reason once and refer to it from affected rows.

        New checked witnesses fill individual gaps without changing the older
        witness's own findings. Four source-only English blocks, the separate
        Joseph continuation, two Prefaces and sixty-three English apparatus
        rows remain typed; six appointment stand-ins are model gaps. A held
        Latin prayer must not continue to claim a facing-column absence.
        """
        report = self.run_harness()
        preamble = report["preamble_1962"]
        self.assertIn("The 1861 witness prints this block only in English", preamble)
        self.assertIn("4 of 196 elements", preamble)
        self.assertIn("This older oration is outside the 1962 Ordinary", preamble)
        self.assertIn("0 of 196 elements", preamble)
        self.assertIn("The 1861 lay witness supplies its own English heading or rubric", preamble)
        self.assertIn("63 of 196 elements", preamble)
        self.assertIn("This day’s Ordinary appointment is not established — 6 of 196 elements", preamble)
        self.assertIn("The appointed proper Canon form is not held here — 0 of 196 elements", preamble)
        self.assertIn("Held English differs from this proper Communicantes — 0 of 196 elements", preamble)
        self.assertIn(
            "Held English lacks the 1962 Saint Joseph clause — 1 of 196 elements", preamble)
        self.assertIn("The appointed Preface is absent from the 1861 witness — 2 of 196 elements", preamble)
        self.assertNotIn("undefined", preamble)
        self.assertNotIn("The 1861 witness prints this block only in English", report["accendat_in_each"]["la"])
        self.assertNotIn("The 1861 witness prints this block only in English", report["te_igitur_in_each"]["la"])

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
        self.assertEqual(raw["source"], "V. Literal call. R. Literal response.")
        self.assertEqual(raw["received"],
                         "℣Versicle. Literal call. ℟Response. Literal response.",
                         "the raw Ordinary rendering retains every literal word")
        self.assertEqual(raw["turns"], [], "opaque text is never split into turns")
        self.assertEqual(raw["role_marks"], [
            {"glyphs": ["℣"], "hidden": ["true"], "labels": ["Versicle."], "languages": ["en"]},
            {"glyphs": ["℟"], "hidden": ["true"], "labels": ["Response."], "languages": ["en"]},
        ])
        self.assertEqual(raw["vr_marks"], 2, "literal V./R. retain their own signs")
        self.assertEqual(raw["cues"], ["P"], "priest is a speaker, not a versicle")
        self.assertEqual(report["role_copy"], {
            "prevented": True, "writes": [["text/plain", "℣ Literal call.\n℟ Literal response."]],
        }, "the shared copy owner keeps glyphs and words, without hidden labels")

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
                    "action": None, "printed_marker": None,
                    "id": None, "semantic_id": None,
                    "labels": ["Versicle — Server"], "cue_langs": ["en"],
                    "cues": [{"mark": "℣", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Server call."}],
                    "received": "Server call.",
                },
                {
                    "speaker": "priest", "dialogue_role": "response",
                    "action": None, "printed_marker": None,
                    "id": None, "semantic_id": None,
                    "labels": ["Response — Priest"], "cue_langs": ["en"],
                    "cues": [{"mark": "℟", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Priest response."}],
                    "received": "Priest response.",
                },
                {
                    "speaker": "priest", "dialogue_role": None,
                    "action": None, "printed_marker": None,
                    "id": None, "semantic_id": None,
                    "labels": ["Priest"], "cue_langs": ["en"],
                    "cues": [{"mark": "P", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Priest part."}],
                    "received": "Priest part.",
                },
                {
                    "speaker": "server", "dialogue_role": None,
                    "action": None, "printed_marker": None,
                    "id": None, "semantic_id": None,
                    "labels": ["Server"], "cue_langs": ["en"],
                    "cues": [{"mark": "S", "aria_hidden": "true"}],
                    "texts": [{"lang": "en", "text": "Server part."}],
                    "received": "Server part.",
                },
                {
                    "speaker": None, "dialogue_role": None,
                    "action": "true", "printed_marker": None,
                    "id": None, "semantic_id": None,
                    "labels": [], "cue_langs": [], "cues": [],
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
        # The generated row keeps the printed `R.`; the reader sets the
        # speaker's one cue and the spoken words, and records the separated
        # marker. Speakers only since 2026-10-19 (C4): the 2002 Ordo n. 29
        # prints no versicle or response mark, so no target role is inferred.
        # The antecedent's separately checked printed R. retains its sign.
        self.assertEqual(
            [
                (row["printed_marker"] or "") + (" " if row["printed_marker"] else "")
                + row["texts"][0]["text"]
                for row in real["rendered_turns"]
            ],
            [row["text"] for row in real["source_turns"]],
        )
        self.assertEqual(
            [row["printed_marker"] for row in real["rendered_turns"]], [None, "R."]
        )
        self.assertEqual(
            [
                (row["speaker"], row["dialogue_role"], row["labels"], row["cues"])
                for row in real["rendered_turns"]
            ],
            [
                (
                    "priest", None, ["Priest"],
                    [{"mark": "P", "aria_hidden": "true"}],
                ),
                (
                    "all", None, ["Response — All"],
                    [{"mark": "℟", "aria_hidden": "true"}],
                ),
            ],
        )
        self.assertTrue(real["rendered_turns"][1]["received"].startswith("Suscipiat"))
        self.assertTrue(all(
            row["id"] is None and row["semantic_id"] is None
            for row in real["rendered_turns"]
        ))

        # A declared marker steps aside only for a structured cue that fits it.
        marked = report["marked_synthetic"]
        self.assertEqual(
            [
                (row["printed_marker"], [cue["mark"] for cue in row["cues"]],
                 row["texts"][0]["text"])
                for row in marked["turns"]
            ],
            [
                ("R.", ["℟"], "Cued answer."),
                ("R.", ["℟"], "Uncued answer."),
                (None, ["P"], "P. Misdeclared row."),
            ],
        )
        self.assertEqual([row["labels"] for row in marked["turns"]],
                         [["Response — Server"], ["Response"], ["Priest"]])
        self.assertEqual([row["dialogue_role"] for row in marked["turns"]], [None] * 3,
                         "a printed sign never assigns a target dialogue role")
        self.assertEqual(english["copy"], {"prevented": False, "writes": []},
                         "the shared copy owner leaves Ordinary rows to native selection")

    def test_each_verified_turn_sets_exactly_one_visible_cue(self) -> None:
        """Confiteor, Suscipiat and Orate fratres: one cue, one label per turn.

        Before 2026-10-19 the 1962 Confiteor set a gutter P beside the printed
        "P.", the server's rows S beside "R.", and Orate fratres needed an
        event-specific stylesheet rule to hide its generated response glyph.
        The reviewed `printed_marker` now separates the book's letter, so the
        common representation alone yields one visible cue per turn. Its one
        accessible label is English; the spoken words keep the row's language.
        """
        report = self.run_harness()
        dialogues = report["real_dialogues"]
        self.assertEqual(len(dialogues), 72)
        priest_server = [("P", "Priest", "P."), ("℟", "Response — Server", "R.")]
        versicle_response = [("℣", "Versicle — Priest", "P."), ("℟", "Response — Server", "R.")]
        expected_cues = {
            "praeparatio/confiteor-sacerdotis": [("P", "Priest", "P.")],
            "praeparatio/confiteor-ministrorum": [("℟", "Response — Server", "R.")],
            "oblatio/suscipiat-dominus": [("℟", "Response — Server", "R.")],
            # Speakers only since 2026-10-19 (C4): n. 29 of the 2002 Ordo
            # prints no versicle or response mark; the antecedent's printed
            # R. retains its sign without assigning a target dialogue role.
            "praeparatio-donorum/orate-fratres": [
                ("P", "Priest", None),
                ("℟", "Response — All", "R."),
            ],
            # C4 step 2 (2026-10-19). The antiphon's Ant./Anth. is a label and
            # stays in the words; the Judica verses carry speakers only, as the
            # 1962 prints S./M. there; ℣/℟ only where the 1962 prints them.
            "praeparatio/introibo-ad-altare-dei": [("P", "Priest", None), ("℟", "Response — Server", "R.")],
            "praeparatio/judica-me-deus": [("P", "Priest", None), ("℟", "Response — Server", "R.")],
            "praeparatio/emitte-lucem-tuam": priest_server,
            "praeparatio/confitebor-tibi-in-cithara": priest_server,
            "praeparatio/gloria-patri": priest_server,
            "praeparatio/introibo-ad-altare-dei-repetitio": [
                ("P", "Priest", "P."), ("℟", "Response — Server", "R."),
            ],
            "praeparatio/adjutorium-nostrum": versicle_response,
            'praeparatio/deus-tu-conversus': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/ostende-nobis': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/domine-exaudi': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/dominus-vobiscum': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/misereatur-tui': [('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.')],
            'praeparatio/misereatur-vestri': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/indulgentiam': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/kyrie-eleison': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.')],
            'praeparatio/christe-eleison': [('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'praeparatio/kyrie-eleison-repetitio': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.')],
            'praeparatio/dominus-vobiscum-post-gloriam': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'oblatio/dominus-vobiscum-ante-evangelium': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'oblatio/dominus-vobiscum-ante-offertorium': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'conclusio/dominus-vobiscum-ante-postcommunionem': [('P', 'Priest', None), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', None)],
            'canon/per-omnia-saecula': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'communio/pater-noster': [('P', 'Priest', None), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.')],
            'communio/per-omnia-saecula-post-libera-nos': [('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'conclusio/requiescant-in-pace': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            'conclusio/initium-sancti-evangelii': [('℣', 'Versicle — Priest', 'P.'), ('℟', 'Response — Server', 'R.'), ('P', 'Priest', 'P.'), ('℟', 'Response — Server', 'R.')],
            "oblatio/per-omnia-saecula": versicle_response,
            "oblatio/sursum-corda": versicle_response * 3,
            "communio/pax-domini": [("P", "Priest", "P."), ("℟", "Response — Server", "R.")],
            "conclusio/dominus-vobiscum-ite-missa-est": [
                ("℣", "Versicle — Priest", None), ("℟", "Response — Server", "R."),
                ("P", "Priest", None), ("℟", "Response — Server", "R."),
            ],
            "conclusio/deo-gratias": [("℟", "Response — Server", "R.")],
            "prex-eucharistica/praefationis-dialogus": [
                ("℣", "Versicle — Priest", "P."), ("℟", "Response — All", "R."),
            ] * 3,
            "ritus-communionis/pax-domini": [("P", "Priest", "P."), ("℟", "Response — All", "R.")],
            "prex-eucharistica/doxologia": [
                ("P", "Priest", None), ("P", "Priest", "P."), ("℟", "Response — All", "R."),
            ],
        }
        antiphon = dialogues["roman-1962 praeparatio/introibo-ad-altare-dei la"]
        self.assertTrue(antiphon["rendered_turns"][0]["texts"][0]["text"].startswith("Ant. "))
        antiphon = dialogues["roman-1962 praeparatio/introibo-ad-altare-dei en"]
        self.assertTrue(antiphon["rendered_turns"][0]["texts"][0]["text"].startswith("I will go in"))
        for name, dialogue in dialogues.items():
            calendar, key, lang = name.split(" ")
            rows = [row for row in dialogue["rendered_turns"] if row.get("gloss") != "true"]
            spoken_source = [turn for turn in dialogue["source_turns"] if turn.get("gloss") is not True]
            wanted = expected_cues[key]
            if calendar == "roman-1962" and lang == "en":
                # The new witness supplies its own actors and roles. An
                # unassigned printed R. keeps its sign without inheriting
                # the old Server or manufacturing a target dialogue role.
                speakers = {"priest": ("P", "Priest"), "server": ("S", "Server"),
                            "all": ("All", "All")}
                roles = {"versicle": ("℣", "Versicle"), "response": ("℟", "Response")}
                wanted = []
                for source in spoken_source:
                    speaker = speakers.get(source["speaker"])
                    marker = source.get("printed_marker")
                    checked_sign = marker in {"V.", "R."} and source["text"].startswith(marker + " ")
                    role = roles.get(source["dialogue_role"]) or (
                        roles["versicle" if marker == "V." else "response"] if checked_sign else None)
                    mark = role[0] if role else speaker[0] if speaker else None
                    label = (role[1] + (" — " + speaker[1] if speaker else "")
                             if role else speaker[1] if speaker else None)
                    wanted.append((mark, label, source["printed_marker"] if mark else None))
            with self.subTest(dialogue=name):
                self.assertEqual(
                    [
                        (
                            row["cues"][0]["mark"] if row["cues"] else None,
                            row["labels"][0] if row["labels"] else None,
                            row["printed_marker"],
                        )
                        for row in rows
                    ],
                    wanted,
                )
                self.assertEqual(len(rows), len(spoken_source))
                for row, source in zip(rows, spoken_source):
                    marker = source.get("printed_marker")
                    checked_sign = marker in {"V.", "R."} and source["text"].startswith(marker + " ")
                    cued = bool(source["speaker"] or source["dialogue_role"] or checked_sign)
                    self.assertEqual(len(row["cues"]), int(cued),
                                     "one cue for a known actor, role or checked printed sign")
                    self.assertEqual(row["speaker"], source["speaker"])
                    self.assertEqual(row["dialogue_role"], source["dialogue_role"],
                                     "a source sign adds no target role or actor")
                    if cued:
                        self.assertEqual(row["cues"][0]["aria_hidden"], "true")
                    self.assertEqual(len(row["labels"]), int(cued), "one accessible label per cue")
                    self.assertEqual(row["cue_langs"], ["en"] if cued else [],
                                     "cue names retain their own English language")
                    self.assertEqual(row["texts"][0]["lang"], lang)
                    body = row["texts"][0]["text"]
                    # No printed cue letter survives in the spoken words, and
                    # the source row is recovered exactly from marker + body.
                    if cued:
                        self.assertNotRegex(body, r"^(?:[PRVS]\.|[℣℟])")
                    marker = row["printed_marker"]
                    self.assertEqual(
                        (marker + " " if marker and cued else "") + body, source["text"]
                    )
                    self.assertEqual(row["received"], body)

    def test_opaque_all_dialogue_keeps_its_opening_attribution(self) -> None:
        """An `all` element announces no opening speaker, so its P. survives.

        Regression for the recovery probe of 2026-10-19: the postconciliar
        Preface dialogue and Pax Domini suppressed the `all` opening cue and
        also removed the leading source P., so their first line had no
        attribution at all. The last word label is also kept apart from its
        words, as every interior label already was.
        """
        report = self.run_harness()
        opaque = report["opaque_all"]
        preface = opaque["preface"]
        self.assertEqual(preface["speaker"], "all")
        self.assertTrue(preface["source"].startswith("P. Dominus vobiscum."))
        self.assertEqual(preface["opening_cues"], 0)
        self.assertEqual(
            preface["received"],
            "Priest Dominus vobiscum. ℟Response. Et cum spiritu tuo. "
            "Priest Sursum corda. ℟Response. Habemus ad Dominum. "
            "Priest Gratias agamus Domino Deo nostro. ℟Response. Dignum et justum est.",
        )
        self.assertEqual(preface["tags"], ["Priest"] * 3)
        self.assertEqual(preface["role_marks"], [
            {"glyphs": ["℟"], "hidden": ["true"], "labels": ["Response."], "languages": ["en"]},
        ] * 3)
        # English word labels inside Latin words carry their own language.
        self.assertEqual(preface["body_lang"], "la")
        self.assertEqual(preface["tag_langs"], ["en"] * 3)

        pax = opaque["pax"]
        self.assertEqual(pax["speaker"], "all")
        self.assertEqual(pax["opening_cues"], 0)
        self.assertEqual(
            pax["received"], "Priest Pax Domini sit semper vobiscum. ℟Response. Et cum spiritu tuo."
        )
        self.assertEqual(pax["role_marks"], [
            {"glyphs": ["℟"], "hidden": ["true"], "labels": ["Response."], "languages": ["en"]},
        ])

        # Where the speaker IS announced, the redundant leading mark still goes.
        priest = opaque["priest_dominus_vobiscum"]
        self.assertEqual(priest["speaker"], "priest")
        self.assertEqual(priest["opening_cues"], 1)
        self.assertTrue(priest["source"].startswith("P. "))
        self.assertFalse(priest["received"].startswith("Priest Priest"))
        self.assertNotIn("P. ", priest["received"])

    def test_source_gloss_is_a_note_after_three_spoken_acclamations(self) -> None:
        report = self.run_harness()
        for key in ("kyrie-eleison", "christe-eleison", "kyrie-eleison-repetitio"):
            lasance = report["real_dialogues"]["roman-1962 praeparatio/" + key + " en"]
            self.assertEqual(len(lasance["rendered_turns"]), 3)
            self.assertTrue(all(not row.get("gloss") for row in lasance["source_turns"]))
            latin = report["real_dialogues"]["roman-1962 praeparatio/" + key + " la"]
            self.assertEqual(len(latin["rendered_turns"]), 3)
            self.assertTrue(all(row["dialogue_role"] is None for row in lasance["rendered_turns"] + latin["rendered_turns"]))
        # Lasance now prints the acclamations in English without a gloss.
        # Keep the nonspoken-gloss renderer contract with a technical fixture;
        # test_ordinary_source_gloss independently checks the old source rows.
        english = report["synthetic_gloss"]
        self.assertEqual(len(english["rendered_turns"]), 4)
        gloss = english["rendered_turns"][-1]
        source = english["source_turns"][-1]
        self.assertTrue(source["gloss"])
        self.assertEqual((gloss["gloss"], gloss["note_role"], gloss["note_label"]),
                         ("true", "note", "Source translation"))
        self.assertEqual((gloss["speaker"], gloss["dialogue_role"], gloss["printed_marker"], gloss["action"]),
                         (None, None, None, None))
        self.assertEqual(gloss["cues"], [])
        self.assertEqual(gloss["labels"], [])
        self.assertEqual(gloss["texts"], [{"lang": "en", "text": source["text"]}])
        self.assertEqual(gloss["received"], source["text"])
        self.assertIsNone(gloss["id"])
        self.assertIsNone(gloss["semantic_id"])

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
        self.assertEqual(page.count('data-reader-action="'), 5)
        # Study is a direct mode action; the four dialog actions keep their
        # existing aria-controls/expanded contract below.
        self.assertIn('data-reader-action="study" aria-current="false"', page)
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
        # The 2026-10-01 comparison against 7285e3ec9 found only c2b1a271b's
        # citation numbering and hebrew-unnumbered-titles loci additions:
        # 16 fields in Advent I and six in ot-18, with no prayer text or
        # translation/provenance change and the same ten/eleven Proper rows.
        # Re-pinned 2026-10-19 (C2 gap G3): Advent I's Collect, Secret and
        # Postcommunion English absences changed state from rights-restricted
        # to unavailable; nothing else in these rows changed.
        # Re-pinned 2026-10-21 against 1498adefe: Advent I changes only
        # Epistle.text and its explicit English absence, from d43007dd0's
        # independently collated 57-word Mame reading (exact-primary fixture).
        # OT-18 changes only its source-checked Psalm 69 numbering and the
        # shared owner's existing John 6 Hebrew-addressing refusal, covered by
        # the antiphon-numbering and Proper-citation-divergence regressions.
        # Every other field in this projection and all ten/eleven rows remain.
        expected = {
            "roman-1962": (
                "advent-1",
                10,
                "79c653c1a959ef53d7ce772bd6cf38ebee7296b1069dc26780ef723512de572c",
            ),
            "postconciliar": (
                "ot-18",
                11,
                "e3f087b4bf34a32bff82ae866299efc0b920f686efc76cd0dd7b4e02f2f6fc70",
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
        self.assertNotIn('<script src="day.js"></script>', day)
        self.assertLess(
            day.index('<script src="reader-optional-runtime.js"></script>'),
            day.index('<script src="day-reader.js"></script>'),
        )
        # Placement reasoning remains owned by the Day controller and comes
        # only from actual seated Proper events and their source loci.
        day_controller = (DAY_HTML.parent / "day-reader.js").read_text(encoding="utf-8")
        start = day_controller.index("function appendOrdinaryReasoning(")
        reasoning = day_controller[start:day_controller.index("\n  function ", start + 1)]
        self.assertIn("event.kind === 'proper' && event.seat && event.seat.locus", reasoning)
        self.assertIn("'Seated here by ' + event.seat.locus", reasoning)

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
const documentListeners = {};
function node(tag) {
  return { nodeType: 1, tagName: tag.toUpperCase(), className: '', textContent: '', lang: null, hidden: false,
    children: [], attrs: {}, style: {},
    appendChild(c) { this.children.push(c); c.parentElement = this; return c; },
    get childNodes() {
      // A real textContent value is a text child, which the copy owner walks.
      return this.textContent ? [{nodeType: 3, nodeValue: this.textContent,
        parentElement: this}].concat(this.children) : this.children;
    },
    matches(selectors) {
      return selectors.split(',').some((selector) => {
        selector = selector.trim();
        if (selector.startsWith('.')) return hasClass(this, selector.slice(1));
        if (selector === '[data-copy="skip"]') return this.attrs['data-copy'] === 'skip';
        return this.tagName.toLowerCase() === selector;
      });
    },
    closest(selectors) { return this.matches(selectors) ? this
      : this.parentElement && this.parentElement.closest(selectors); },
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
    nodeType: 3, nodeValue: t, data: t, text: () => t, receivedText: () => t }),
  createDocumentFragment: () => node('#fragment'),
  getElementById: (id) => (ids[id] = ids[id] || node('div')),
  body: { classList: { toggle() {} }, appendChild() {} },
  addEventListener(type, listener) { documentListeners[type] = listener; } };
global.getComputedStyle = (one) => ({
  display: ['P', 'DIV', 'BR'].includes(one.tagName) ? 'block' : 'inline', visibility: 'visible'
});
global.window = { location: { search: '' }, addEventListener() {},
  MassAssembly: { derive: () => ({}) }, matchMedia: null };
global.window.OrdinarySeating = require(
  './src/web/browser/liturgy/ordinary-seating.js');
global.window.LiturgyReaderStateAdapters = require(
  './src/web/browser/liturgy/reader-state-adapters.js');

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
function roleMarks(root) {
  return descendants(root, 'vr-mark').map((one) => ({
    glyphs: descendants(one, 'vr-glyph').map((mark) => mark.text()),
    hidden: descendants(one, 'vr-glyph').map((mark) => mark.attrs['aria-hidden']),
    labels: descendants(one, 'visually-hidden').map((label) => label.text()),
    languages: descendants(one, 'visually-hidden').map((label) => label.lang)
  }));
}
// Invoke the shared copy listener. This proves its serialization/deferral
// decision; real native selection and AX are covered by test_reader_dialogue.
function ownerCopy(body) {
  const wrapper = node('div'); wrapper.className = 'reader-document';
  if (body.tagName === '#FRAGMENT') body.children.forEach((child) => wrapper.appendChild(child));
  else wrapper.appendChild(body);
  const range = {commonAncestorContainer: wrapper, intersectsNode: () => true,
    startContainer: wrapper, endContainer: wrapper, startOffset: 0, endOffset: wrapper.children.length};
  document.getSelection = () => ({isCollapsed: false, rangeCount: 1, getRangeAt: () => range});
  const result = {prevented: false, writes: []};
  documentListeners.copy({
    clipboardData: {setData(type, value) { result.writes.push([type, value]); }},
    preventDefault() { result.prevented = true; }
  });
  return result;
}
function dialogueReport(rendered) {
  return descendants(rendered, 'ordinary-turn').map((row) => ({
    speaker: row.attrs['data-speaker'] || null,
    dialogue_role: row.attrs['data-dialogue-role'] || null,
    action: row.attrs['data-action'] || null,
    printed_marker: row.attrs['data-printed-marker'] || null,
    ...(row.attrs['data-gloss'] === 'true' ? {gloss: 'true', note_role: row.attrs.role, note_label: row.attrs['aria-label']} : {}),
    id: row.attrs.id || null,
    semantic_id: row.attrs['data-semantic-id'] || null,
    labels: descendants(row, 'visually-hidden').map((one) => one.text()),
    cue_langs: descendants(row, 'ordinary-turn-cue').map((one) => one.lang),
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
/* The Day's appointment context for one formulary on one civil date, built
   exactly as reader-state-adapters builds it: the formulary's own printed
   Ordinary appointments (the form's replacing the Mass's), the date and the
   owning liturgical year's anchors from the tracked calendar layer. */
function liturgicalYear(calendar, date) {
  const year = read('src/web/data/structure/calendar/' + calendar + '/' +
    date.slice(0, 4) + '.json');
  return year.liturgical_years.find((one) => one.begins <= date && date <= one.ends);
}
function dayPredicates(calendar, mass, form, date) {
  const owner = liturgicalYear(calendar, date);
  const appointments = {};
  [mass.ordinary_appointments, form && form.ordinary_appointments].forEach((rows) => {
    Object.keys(rows || {}).forEach((variable) => { appointments[variable] = rows[variable].option; });
  });
  return global.window.OrdinarySeating.predicateFacts({
    date: date, anchors: owner && owner.anchors || null, appointments: appointments
  });
}
/* The production reader prepares source-owned appointments before framing.
   These renderer probes must cross that same shared boundary, with explicit
   fixture choices rather than a default for a source relation. */
function prepare(file, calendar, mass, form, date, choices) {
  const owner = date && liturgicalYear(calendar, date);
  const lectionary = owner && owner.lectionary || {};
  const prepared = window.OrdinarySeating.prepareProperAppointments(
    (form ? form.propers : mass.propers) || [], {
      calendar: calendar, entrance: 'day', mass: mass.key,
      formId: form ? form.id : 'main', sourcePaths: mass.proper_source_paths || [],
      calendarCycles: {sunday: lectionary.sunday || null, weekday: lectionary.weekday || null},
      date: date, season: owner && (owner.seasons || []).find(
        (one) => one.from <= date && date <= one.to)?.season || null,
      facts: file.proper_appointment_facts || {}, choices: choices || {}
    });
  if (prepared.unresolved.length || prepared.sourcePathUnresolved.length) {
    throw new Error('renderer fixture requires explicit resolved source appointments');
  }
  return prepared;
}
function pour(file, calendar, key, formId, date, choices) {
  const structure = read('src/web/data/structure/propers/' + calendar + '.json');
  const mass = structure.masses.find((m) => m.key === key);
  const form = formId && (mass.forms || []).find((one) => one.id === formId);
  if (formId && !form) throw new Error('missing stable form ' + key + '/' + formId);
  const prepared = prepare(structure, calendar, mass, form, date, choices);
  const frame = date
    ? global.window.OrdinarySeating.resolveElements(
      file, {}, dayPredicates(calendar, mass, form, date)).shown
    : P.shownElements(file);
  const placed = window.OrdinarySeating.seatPropers(
    prepared.rows, P.seats(file, frame), window.Triptych.isPlaceholder, prepared.selections);
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
const easter = pour(tlm, 'roman-1962', 'easter-sunday', null, '2026-04-05');
const pentecost10 = pour(tlm, 'roman-1962', 'pentecost-10', null, '2026-08-02');
const ot18 = pour(pc, 'postconciliar', 'ot-18', null, '2026-08-02');
const nativity = ['vigil', 'night', 'dawn', 'day'].map((id) => ({
  id: id, result: pour(pc, 'postconciliar', 'nativity', id, '2026-12-25')
}));
const easterChoices = {
  'main/easter-day-second-reading': 'colossians-3',
  'main/easter-day-gospel': 'john-20'
};
const collect = pour(pc, 'postconciliar', 'easter-sunday', null, '2026-04-05', easterChoices).order;
const easterStructure = read('src/web/data/structure/propers/postconciliar.json');
const easterMass = easterStructure.masses.find((one) => one.key === 'easter-sunday');
const principal = prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05', easterChoices);
const vigil = prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05', {
  ...easterChoices, 'main/easter-day-gospel': 'easter-vigil-a'
});
function refuses(action) {
  try { action(); return ''; } catch (error) { return error.message; }
}
const sourcePathControls = {
  principal: principal.sourcePathSelections,
  primary_names: principal.rows.map((row) => row.proper.name),
  vigil_material: vigil.rows.find((row) => row.proper.name === 'Gospel').materialCycle,
  refused: {
    raw: refuses(() => P.seatPropers(easterMass.propers, P.seats(pc, P.shownElements(pc)))),
    missing: refuses(() => prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05')),
    mixed: refuses(() => prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05', {
      ...easterChoices, 'main/gospel': 'easter-vigil'
    })),
    unknown_evening: refuses(() => prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05', {
      ...easterChoices, 'main/easter-day-gospel': 'evening-emmaus'
    })),
    wrong_cycle: refuses(() => prepare(easterStructure, 'postconciliar', easterMass, null, '2026-04-05', {
      ...easterChoices, 'main/easter-day-gospel': 'easter-vigil-b'
    }))
  }
};
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
/* A declared printed marker is separated only where a structured cue stands
   in its place, and only when the declaration fits the row; otherwise the row
   is shown exactly as printed and keeps its one printed cue. */
const marked = {
  key: 'synthetic/marked', kind: 'dialogue', speaker: null,
  name: null, latin_incipit: null, locus: null, note: null, variant: null,
  absent: {english: null, latin: null},
  translations: [{lang: 'en', source_id: 'synthetic-en', rights: 'project-created',
    text: 'R. Cued answer.\nR. Uncued answer.\nP. Misdeclared row.',
    turns: [
      {key: 'cued', speaker: 'server', dialogue_role: null, action: null,
        printed_marker: 'R.', text: 'R. Cued answer.'},
      {key: 'uncued', speaker: null, dialogue_role: null, action: null,
        printed_marker: 'R.', text: 'R. Uncued answer.'},
      {key: 'misdeclared', speaker: 'priest', dialogue_role: null, action: null,
        printed_marker: 'R.', text: 'P. Misdeclared row.'}
    ]}]
};
P.state.ordinaryLang = 'en';
const markedRendered = P.renderElement(marked, syntheticFile);
P.state.ordinaryLang = null;

/* The three verified dialogues C4 names, rendered from the generated data. */
function realTurns(file, key, lang) {
  const element = all(file).find((e) => e.key === key);
  const held = (element.translations || []).find((one) => one.lang === lang);
  P.state.ordinaryLang = lang;
  const rendered = P.renderElement(element, file);
  P.state.ordinaryLang = null;
  return { source_turns: held.turns, rendered_turns: dialogueReport(rendered) };
}
const realDialogues = {};
const glossTurns = ['priest', 'server', 'priest'].map((speaker, index) => ({
  key: 'invocation-' + index, speaker: speaker, dialogue_role: null,
  action: null, printed_marker: null, text: 'Technical invocation.'
}));
glossTurns.push({key: 'source-gloss', speaker: null, dialogue_role: null,
  action: null, printed_marker: null, gloss: true, text: 'Technical translation.'});
const glossFile = {...syntheticFile, sections: [{elements: [{
  ...structured, key: 'synthetic/gloss',
  translations: [{lang: 'en', source_id: 'synthetic-en', rights: 'project-created',
    text: glossTurns.map((row) => row.text).join('\n'), turns: glossTurns}]
}]}]};
const syntheticGloss = realTurns(glossFile, 'synthetic/gloss', 'en');
for (const lang of ['en', 'la']) {
  for (const key of ['praeparatio/confiteor-sacerdotis',
    'praeparatio/confiteor-ministrorum', 'oblatio/suscipiat-dominus',
    // C4 step 2 (2026-10-19): the reviewed child rows of the dialogues.
    'praeparatio/introibo-ad-altare-dei', 'praeparatio/judica-me-deus',
    'praeparatio/emitte-lucem-tuam', 'praeparatio/confitebor-tibi-in-cithara',
    'praeparatio/gloria-patri', 'praeparatio/introibo-ad-altare-dei-repetitio',
    'praeparatio/adjutorium-nostrum',
    'praeparatio/deus-tu-conversus', 'praeparatio/ostende-nobis', 'praeparatio/domine-exaudi', 'praeparatio/dominus-vobiscum', 'praeparatio/misereatur-tui', 'praeparatio/misereatur-vestri', 'praeparatio/indulgentiam', 'praeparatio/kyrie-eleison', 'praeparatio/christe-eleison', 'praeparatio/kyrie-eleison-repetitio', 'praeparatio/dominus-vobiscum-post-gloriam', 'oblatio/dominus-vobiscum-ante-evangelium', 'oblatio/dominus-vobiscum-ante-offertorium', 'conclusio/dominus-vobiscum-ante-postcommunionem', 'canon/per-omnia-saecula', 'communio/pater-noster', 'communio/per-omnia-saecula-post-libera-nos', 'conclusio/requiescant-in-pace', 'conclusio/initium-sancti-evangelii',
    'oblatio/per-omnia-saecula', 'oblatio/sursum-corda', 'communio/pax-domini',
    'conclusio/dominus-vobiscum-ite-missa-est', 'conclusio/deo-gratias']) {
    realDialogues['roman-1962 ' + key + ' ' + lang] = realTurns(tlm, key, lang);
  }
}
for (const key of ['praeparatio-donorum/orate-fratres',
  'prex-eucharistica/praefationis-dialogus', 'ritus-communionis/pax-domini',
  'prex-eucharistica/doxologia']) {
  realDialogues['postconciliar ' + key + ' la'] = realTurns(pc, key, 'la');
}

/* Opaque `all` dialogues: no opening cue is set, so the leading P. is the
   first line's only attribution and must survive as its word label. */
function opaqueCues(file, key, lang) {
  const found = all(file).find((e) => e.key === key);
  // Since C4 step 2 no real `all` dialogue is opaque: the regression runs on
  // the same element as its source block stood before the child-row division,
  // the turns rejoined by the single spaces the division removed.
  const element = Object.assign({}, found, {
    translations: (found.translations || []).map((one) => one.turns
      ? Object.assign({}, one, { text: one.turns.map((t) => t.text).join(' '), turns: undefined })
      : one)
  });
  P.state.ordinaryLang = lang;
  const rendered = P.renderElement(element, file);
  P.state.ordinaryLang = null;
  const body = descendants(rendered, 'composed')[0];
  return {
    speaker: element.speaker,
    source: (element.translations || []).find((one) => one.lang === lang).text,
    received: body.receivedText(),
    opening_cues: descendants(rendered, 'is-opening-cue').length,
    tags: descendants(body, 'speaker-tag').map((one) => one.text()),
    tag_langs: descendants(body, 'speaker-tag').map((one) => one.lang),
    role_marks: roleMarks(body),
    body_lang: body.lang
  };
}
const opaqueAll = {
  preface: opaqueCues(pc, 'prex-eucharistica/praefationis-dialogus', 'la'),
  pax: opaqueCues(pc, 'ritus-communionis/pax-domini', 'la'),
  // A priest-announced element still drops its redundant leading mark.
  priest_dominus_vobiscum: opaqueCues(tlm, 'praeparatio/dominus-vobiscum', 'en')
};

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
  te_igitur_1962: P.renderElement(all(tlm).find((e) => e.key === 'canon/te-igitur'), tlm).text(),
  easter_1962: easter.order.filter((one) => MARKS.has(one) || one.indexOf('/') < 0),
  nativity_forms: nativity.map((one) => ({
    id: one.id, broke: one.result.broke,
    seated: one.result.seated, before: one.result.before,
    after: one.result.after,
    total: one.result.seated + one.result.before + one.result.after
  })),
  postconciliar_collect: collect.slice(seat, seat + 2),
  source_path_controls: sourcePathControls,
  event_kinds: easter.kinds,
  pentecost_10_sequence: pentecost10.sequence,
  pentecost_10_text: pentecost10.text,
  ot_18_sequence: ot18.sequence,
  ot_18_text: ot18.text,
  structured_english: {
    turns: dialogueReport(structuredEnglish),
    received: structuredEnglish.receivedText(),
    dialogue_count: descendants(structuredEnglish, 'ordinary-dialogue').length,
    copy: ownerCopy(structuredEnglish)
  },
  structured_latin: {
    turns: dialogueReport(structuredLatin),
    received: structuredLatin.receivedText(),
    dialogue_count: descendants(structuredLatin, 'ordinary-dialogue').length
  },
  raw_vr: {
    source: raw.translations[0].text,
    received: rawRendered.receivedText(),
    turns: dialogueReport(rawRendered),
    vr_marks: descendants(rawRendered, 'vr-mark').length,
    role_marks: roleMarks(rawRendered),
    cues: descendants(rawRendered, 'cue-mark').map((one) => one.attrs['data-cue'])
  },
  role_copy: ownerCopy(window.Triptych.versicled(raw.translations[0].text)),
  marked_synthetic: {
    turns: dialogueReport(markedRendered),
    received: markedRendered.receivedText()
  },
  real_dialogues: realDialogues,
  synthetic_gloss: syntheticGloss,
  opaque_all: opaqueAll,
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
