#!/usr/bin/env python3
"""Regression checks for the Ordinary layer, and for the page that shows it.

The interesting failures here are not crashes. They are a prayer served under
the wrong name and a licensed text served without the condition that makes it
lawful, and neither would raise anything.

Two of the checks below exist because of specific, recorded near-misses. The
1861 Canon and the postconciliar Eucharistic Prayer I differ at eleven places,
among them both consecratory forms, so serving the one as the other would put a
wrong text at the most consequential locus in the rite; `test_prayer_one_is_not
_the_1861_canon` holds that boundary. And the ELLC common texts are free only on
a stated condition, so `test_a_licensed_text_carries_its_acknowledgement` holds
the acknowledgement beside the words rather than in a footer.

The browser half runs the real `day.js` and `ordinary-seating.js` under node
against the real generated files, for the reason `calendar-rubrics check` runs
`assembly-model.js` that way: a Python re-implementation would drift from the
page.
"""

import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "web" / "data" / "structure" / "ordinary"
PROPERS = ROOT / "src" / "web" / "data" / "structure" / "propers"
DAY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "day.js"
DAY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "day.html"
FORMULARY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "liturgy.js"
FORMULARY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "index.html"
READING_CONTENTS_JS = (
    ROOT / "src" / "web" / "browser" / "liturgy" / "reading-contents.js"
)
PLACEMENT_NOTES_JS = (
    ROOT / "src" / "web" / "browser" / "liturgy" / "proper-placement-notes.js"
)
DAY_MISSAL_CSS = ROOT / "src" / "web" / "browser" / "liturgy" / "day-missal.css"
TOOL = ROOT / "tools" / "mass-ordinary"

PUBLISHABLE = {"public-domain", "project-created", "licensed-free"}
NEEDS_ACKNOWLEDGEMENT = {"licensed-free"}


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
        self.files = {row: load(row) for row in ("roman-1962", "postconciliar")}

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

    def test_a_licensed_text_carries_its_acknowledgement(self) -> None:
        """Free use granted on a condition is not free use without the condition."""
        for name, file in self.files.items():
            for witness in file["translations"]:
                if witness["rights"] in NEEDS_ACKNOWLEDGEMENT:
                    self.assertTrue(witness["acknowledgement"],
                                    f"{name}: {witness['source_id']} states no acknowledgement")

    def test_element_keys_are_unique_across_sections(self) -> None:
        """The 1861 book says `Gloria Patri` twice; the keys must still differ."""
        for name, file in self.files.items():
            keys = [element["key"] for element in elements(file)]
            self.assertEqual(len(keys), len(set(keys)), name)

    def test_only_the_postconciliar_missal_offers_a_choice_of_prayer(self) -> None:
        """The 1962 Missal has one Canon, so it must offer nothing to choose."""
        self.assertEqual(self.files["roman-1962"]["variants"], [])
        groups = self.files["postconciliar"]["variants"]
        self.assertEqual([one["group"] for one in groups], ["eucharistic-prayer"])
        options = groups[0]["options"]
        self.assertEqual([one["id"] for one in options if one["default"]], ["ep-i"],
                         "the default is the first prayer the Missal itself prints")

    def test_prayer_one_is_not_the_1861_canon(self) -> None:
        """The divergence that makes this the worst possible substitution.

        The postconciliar Prayer I must carry no text at all, and must say in
        terms that the Canon this site serves under the 1962 Missal is a
        different prayer. Reproducing the 1861 English here would be silent,
        plausible, and wrong at both consecratory forms.
        """
        found = [one for one in elements(self.files["postconciliar"])
                 if one["variant"] == "ep-i"]
        self.assertEqual(len(found), 1)
        prayer = found[0]
        self.assertIsNone(prayer["translations"], "Prayer I must carry no English")
        self.assertTrue(prayer["absent"]["english"])
        self.assertIn("NOT THE CANON OF THE 1962 MISSAL", (prayer["note"] or "").upper())

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
        self.files = {row: load(row) for row in ("roman-1962", "postconciliar")}

    def test_every_seat_names_an_element_the_frame_shows(self) -> None:
        for name, file in self.files.items():
            keys = {element["key"]: element for element in elements(file)}
            for slot in file["slots"]:
                self.assertIn(slot["anchor"], keys, f"{name}: seat {slot['key']}")
                self.assertIsNone(
                    keys[slot["anchor"]]["variant"],
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
        that resolves successfully and does nothing.
        """
        for name, file in self.files.items():
            path = PROPERS / (name + ".json")
            if not path.is_file():
                self.skipTest("no propers layer written")
            corpus = json.loads(path.read_text(encoding="utf-8"))
            used = {proper.get("name")
                    for mass in corpus.get("masses", [])
                    for proper in mass.get("propers", [])}
            for slot in file["slots"]:
                for proper in slot["propers"]:
                    self.assertIn(proper, used, f"{name}: seat {slot['key']} awaits {proper!r}")


class OrdinaryTool(unittest.TestCase):
    """The generator refuses what it must refuse."""

    def test_written_files_are_current(self) -> None:
        run = subprocess.run(
            ["python3", str(TOOL), "check", "--json"],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)["stale"], [],
                         "regenerate with `tools/tpt mass-ordinary structure`")


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
        self.assertEqual(len(sequence), 211)
        self.assertEqual(
            digest,
            "c1fe93220057c722c753d3af29c9fb111c162a2572304780c018a6fed2591c08",
        )

        sequence = report["ot_18_sequence"]
        digest = hashlib.sha256(
            json.dumps(sequence, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(len(sequence), 63)
        self.assertEqual(
            digest,
            "0aa4fc7139443a2bd9a53df16a737485d64cc8bf686fbde8e8e976981f158f2e",
        )

    def test_ordered_mass_text_contract_for_both_missals(self) -> None:
        """Navigation must not alter the text-bearing event stream."""
        report = self.run_harness()
        expected = {
            "pentecost_10_text": (
                211,
                "b18b9e4c33019380fa11baeb7ed8e386848fdb530b8bd1a396afff601c6d2666",
            ),
            "ot_18_text": (
                63,
                "da08c368ba61ce86467892eaa4833b7659ae8939c4bd73cc1eb4fcec726d1988",
            ),
        }
        for key, (count, wanted_digest) in expected.items():
            rows = report[key]
            digest = hashlib.sha256(
                json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(rows), count, key)
            self.assertEqual(digest, wanted_digest, key)

    def test_the_page_shows_one_prayer_and_states_what_it_withholds(self) -> None:
        report = self.run_harness()
        self.assertEqual(report["shown_by_default"], ["ep-i"])
        self.assertEqual(report["shown_when_third_chosen"], ["ep-iii"])
        self.assertIn("Lord, have mercy.", report["kyrie"])
        self.assertIn("English Language Liturgical Consultation (ELLC), and used by permission",
                      report["kyrie"])
        self.assertIn("Not shown: its English.", report["prayer_one"])
        self.assertIn("Not shown: its Latin.", report["prayer_one"])
        self.assertIn("Te igitur, clementissime Pater", report["prayer_one"])
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

    def test_a_day_the_frame_does_not_fit_is_said_so_and_not_rearranged(self) -> None:
        """Christmas carries four Masses; one Ordinary cannot hold them.

        The failure this guards is the attractive one: pouring all four into the
        frame would put four Collects under one Collect and read as a Mass that
        was never said. What must happen instead is that the frame takes the
        first, the rest follow it whole, and the page says why.
        """
        report = self.run_harness()
        self.assertTrue(report["nativity_broke"])
        self.assertEqual(report["nativity_seated"], 10)
        self.assertEqual(report["nativity_after"], 31)
        self.assertEqual(report["nativity_total"], 41, "nothing is dropped")

    def test_a_withheld_element_still_holds_the_place_of_its_proper(self) -> None:
        """Absence does not forfeit a seat.

        The postconciliar Collect is withheld under ICEL's licence. The day's
        Collect is still set down immediately after it, so a reader sees both
        what is withheld and what is not, at the moment each falls due.
        """
        report = self.run_harness()
        self.assertEqual(report["postconciliar_collect"],
                         ["ritus-initiales/collecta", "Collect"])

    def test_a_language_nobody_holds_is_offered_and_says_why(self) -> None:
        """The control's whole purpose, and the failure it must not have.

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
        there is absent for a different reason, `no-facing-latin`: the book sets
        those blocks across the full measure in English and prints no Latin at
        all, which is the witness's own silence and not a gap in anyone's work.
        So the absent case is now taken on an element that really is absent, and
        the held case is asserted beside it, because a control that offers a
        language must be tested on both.

        The two reasons still in play remain incomparable and are asserted not
        to leak into each other: `no-facing-latin` is a fact about one
        printing's pages, and `editio-typica` is a rights question nobody has
        settled about the postconciliar Missal, whose Latin is held nowhere.
        """
        report = self.run_harness()
        self.assertEqual(
            [one["lang"] for one in report["languages"]["postconciliar"]], ["en", "la"])
        self.assertEqual(
            [one["held"] for one in report["languages"]["postconciliar"]], [9, 0])
        self.assertEqual(
            [one["held"] for one in report["languages"]["roman-1962"]], [195, 112])
        # The Latin the 1962 file does not hold is exactly the elements the
        # preamble's one reason covers; the next test asserts that count from
        # the other side.
        elements = report["languages"]["roman-1962"][1]["elements"]
        self.assertEqual(elements - 112, 83)

        pater = report["kyrie_in_each"]
        self.assertIn("Our Father in heaven", pater["en"])
        self.assertNotIn("Our Father in heaven", pater["la"])
        self.assertIn("Not shown: its Latin.", pater["la"])
        self.assertIn("editio-typica", pater["la"])

        # Held: the facing column was read, so the Latin stands in its own right
        # and no reason is offered for a silence there is not.
        canon = report["te_igitur_in_each"]
        self.assertIn("WE therefore, humbly pray", canon["en"])
        self.assertNotIn("WE therefore, humbly pray", canon["la"])
        self.assertIn("TE igitur, clementissime Pater", canon["la"])
        self.assertNotIn("Not shown: its Latin.", canon["la"])
        self.assertNotIn("no-facing-latin", canon["la"])

        # Absent: this offertory prayer is one of the 83 the book sets to the
        # full measure in English, so the Latin side names its reason and only
        # its reason.
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

        The reach is what moved on 2026-08-20, not the rule: the reason used to
        be `latin-not-transcribed` over all 195 elements, and now the facing
        column is carried, so it is `no-facing-latin` over the 83 blocks the
        book prints in English alone. The preamble must still state it once and
        say how far it goes, the covered elements must still refer to it without
        repeating it, and — new with the transcription — an element that holds
        its Latin must not carry the reason at all.
        """
        report = self.run_harness()
        preamble = report["preamble_1962"]
        self.assertIn("no-facing-latin", preamble)
        self.assertIn("83 of 195 elements", preamble)
        self.assertIn("prints no Latin text for it", preamble)
        self.assertNotIn("prints no Latin text for it",
                         report["accendat_in_each"]["la"])
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
        self.assertIn("B. V. M.", report["virgin_1861"])
        self.assertNotIn("℣", report["virgin_1861"])

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
        expected = {
            "roman-1962": (
                "advent-1",
                10,
                "c7e2c7432efc8383a6aa253a25cb27b57f583d7ce2bbc3fba9011bb0df97220c",
            ),
            "postconciliar": (
                "ot-18",
                11,
                "0e177a7008ef4b3ba4863724848b185257164cacd383d334378b03d55c2b81e2",
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
        # The two pins are a tripwire, not the assertion: they say the formulary
        # page and its script have not moved without someone re-reading the line
        # above, which is the thing actually guarded. Re-pinned once, on
        # 2026-08-20. The page's bytes had moved and the pin had not, so the
        # tripwire was reporting a change nobody had looked at. It was then
        # looked at: `git diff` over the whole interval since the pin was set
        # shows one hunk, the six lines that wrap the existing reader-place
        # breadcrumb around a hidden `data-reader-locus` span. It adds no
        # script tag, names no placement-notes module, and changes no load
        # order, so the guarded proposition is untouched and the pin is moved
        # rather than the assertion weakened. `liturgy.js` had not moved at all
        # and its pin is the original.
        self.assertEqual(
            hashlib.sha256(FORMULARY_HTML.read_bytes()).hexdigest(),
            "61593982117969b8673a936117ae8c331aca91c20283f613bd9c289424c83164",
        )
        self.assertEqual(
            hashlib.sha256(FORMULARY_JS.read_bytes()).hexdigest(),
            "7e1def40d8ed150d181926e312b2faa24aa4bf85f24bfe14dd9edf832150f73d",
        )

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
      for (const c of this.children) o += (c.text ? c.text() : String(c.data || '')); return o; } };
}
const ids = {};
global.document = { createElement: node, createTextNode: (t) => ({ data: t, text: () => t }),
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
const eps = all(pc).filter((e) => e.variant);
const shown = () => eps.filter((e) => P.elementShows(e, pc)).map((e) => e.variant);
const byDefault = shown();
P.state.variants['eucharistic-prayer'] = 'ep-iii';
const whenThird = shown();
P.state.variants = {};

/* The frame with a real formulary poured into it, as one flat sequence: a
   proper by its name, an element by its key. This is what the page renders, in
   the order it renders it. */
function pour(file, calendar, key) {
  const mass = read('src/web/data/structure/propers/' + calendar + '.json')
    .masses.find((m) => m.key === key);
  const frame = P.shownElements(file);
  const placed = P.seatPropers(mass.propers || [], P.seats(file, frame));
  const events = P.massEvents(frame, placed);
  const out = [];
  for (const event of events) {
    if (event.kind === 'proper') out.push(event.proper.name);
    if (event.kind === 'ordinary_element') out.push(event.element.key);
  }
  const count = (placement) => events.filter(
    (event) => event.kind === 'proper' && event.placement === placement).length;
  const sequence = events.map((event) => {
    if (event.kind === 'begin_section') {
      return 'begin_section:' + event.section.key;
    }
    if (event.kind === 'ordinary_element') {
      return 'ordinary_element:' + event.element.key;
    }
    return 'proper:' + event.placement + ':' + event.proper.name;
  });
  const text = events.map((event) => {
    if (event.kind === 'begin_section') return event.section.name;
    if (event.kind === 'ordinary_element') return P.renderElement(event.element, file).text();
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
const nativity = pour(pc, 'postconciliar', 'nativity');
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

process.stdout.write(JSON.stringify({
  shown_by_default: byDefault,
  shown_when_third_chosen: whenThird,
  languages: { postconciliar: pc.languages, 'roman-1962': tlm.languages },
  kyrie_in_each: inEach(pc, 'ritus-communionis/pater-noster'),
  te_igitur_in_each: inEach(tlm, 'canon/te-igitur'),
  accendat_in_each: inEach(tlm, 'oblatio/accendat-in-nobis'),
  preamble_1962: P.ordinaryPreamble(tlm).text(),
  versicles_1861: P.renderElement(
    all(tlm).find((e) => e.key === 'praeparatio/dominus-vobiscum'), tlm).text(),
  virgin_1861: P.renderElement(
    all(tlm).find((e) => e.key === 'oblatio/rubrica-collecta-concede'), tlm).text(),
  kyrie: P.renderElement(all(pc).find((e) => e.key.endsWith('/kyrie')), pc).text(),
  prayer_one: P.renderElement(eps.find((e) => e.variant === 'ep-i'), pc).text(),
  te_igitur_1861: P.renderElement(all(tlm).find((e) => e.key === 'canon/te-igitur'), tlm).text(),
  easter_1962: easter.order.filter((one) => MARKS.has(one) || one.indexOf('/') < 0),
  nativity_broke: nativity.broke,
  nativity_seated: nativity.seated,
  nativity_after: nativity.after,
  nativity_total: nativity.seated + nativity.before + nativity.after,
  postconciliar_collect: collect.slice(seat, seat + 2),
  event_kinds: easter.kinds,
  pentecost_10_sequence: pentecost10.sequence,
  pentecost_10_text: pentecost10.text,
  ot_18_sequence: ot18.sequence,
  ot_18_text: ot18.text
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
