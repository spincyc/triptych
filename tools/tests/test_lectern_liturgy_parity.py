"""Terminal controls retain the production reader's semantic selections."""
from __future__ import annotations

import importlib.util
import asyncio
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge  # noqa: E402
from lectern.repo import Refused  # noqa: E402


def words(blocks: list[dict]) -> str:
    return " ".join(run["text"] for block in blocks for run in block["runs"])


@unittest.skipUnless(shutil.which("node"), "the browser models require node")
class LiturgyParityTests(unittest.TestCase):
    def test_the_ordinary_language_default_matches_both_page_owners(self) -> None:
        default = bridge.call("liturgy", "opening")["defaultOrdinaryLanguage"]
        for name in ("day-reader.js", "propers-reader.js"):
            source = (ROOT / "src/web/browser/liturgy" / name).read_text()
            found = re.search(r"\{\s*'ordinary-lang':\s*'([^']+)'\s*\}", source)
            self.assertIsNotNone(found, name)
            self.assertEqual(default, found.group(1), name)

    def test_ordinary_choice_and_language_are_independent_of_orations(self) -> None:
        options = {"orations": "la", "ordinary": True, "ordinaryLang": "en",
                   "variants": {"eucharistic-prayer": "ep-ii"}, "cycle": "A"}
        direct = bridge.call("liturgy", "propers", "postconciliar", "advent-1", options)
        self.assertEqual(direct["ordinary"]["selection"]["eucharistic-prayer"], "ep-ii")
        ordinary = [row for row in direct["events"] if row["kind"] == "ordinary-element"]
        self.assertTrue(ordinary)
        self.assertTrue(all(row["text"]["language"] == "en" for row in ordinary))
        self.assertTrue(any(row["id"].endswith("/prex-eucharistica-ii") for row in ordinary))
        self.assertFalse(any(row["id"].endswith(("/prex-eucharistica-i", "/prex-eucharistica-iii", "/prex-eucharistica-iv"))
                             for row in ordinary))
        day = bridge.call("liturgy", "day", "postconciliar", "2026-11-29", options)
        self.assertEqual(day["ordinary"]["selection"]["eucharistic-prayer"], "ep-ii")
        self.assertTrue(all(row["text"]["language"] == "en" for row in day["rows"][0]["events"]
                            if row["kind"] == "ordinary-element"))

    def test_an_unsupported_ordinary_option_is_refused(self) -> None:
        with self.assertRaisesRegex(Refused, "explicit Ordinary option"):
            bridge.call("liturgy", "propers", "roman-1962", "advent-1",
                        {"ordinary": True, "variants": {"eucharistic-prayer": "ep-ii"}})

    def test_bilingual_keeps_both_languages_in_the_production_rendering(self) -> None:
        view = bridge.call("liturgy", "propers", "roman-1962", "pentecost",
                           {"orations": "en", "ordinary": True, "ordinaryLang": "en",
                            "textDisplay": "latin-and-selected"})
        proper = next(row for row in view["events"] if row.get("slot") == "Collect")
        self.assertIn("Latin", words(proper["blocks"]))
        self.assertIn("English", words(proper["blocks"]))
        ordinary = next(row for row in view["events"] if row["kind"] == "ordinary-element"
                        and "text-side-label" in str(row.get("blocks")))
        self.assertIn("Latin", words(ordinary["blocks"]))
        self.assertIn("English", words(ordinary["blocks"]))

    def test_witnesses_belong_to_the_selected_mass_and_have_selectable_ids(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "advent-2", {"orations": "en", "cycle": "A"})
        witnesses = view["mass"]["witnesses"]
        self.assertTrue(witnesses)
        self.assertTrue(all(one["id"] and one["available"] > 0 for one in witnesses))
        self.assertTrue(any(one["id"] == "project-created" for one in witnesses))
        picked = bridge.call("liturgy", "propers", "postconciliar", "advent-2",
                             {"orations": "en", "cycle": "A", "witness": "project-created"})
        self.assertEqual(picked["state"]["witness"], "project-created")

    def test_study_uses_the_production_source_and_seating_apparatus(self) -> None:
        blocks = bridge.call("liturgy", "studyPropers", "roman-1962", "pentecost", {})
        said = words(blocks)
        for label in ("Study this selection", "Propers is date-independent", "Functional slot", "Source record"):
            self.assertIn(label, said)
        self.assertIn("proper-structure", said)
        branches = bridge.call("liturgy", "studyDay", "roman-1962", "2026-05-24", {})
        self.assertIn("Calendar result", words(branches[0]["blocks"]))
        self.assertIn("2026-05-24", words(branches[0]["blocks"]))

    def test_propers_comparisons_stay_date_independent_and_keep_their_peers(self) -> None:
        cases = [
            ("advent-1", {"cycle": "A"}, "oration-language", "la", "en"),
            ("transfiguration-lord", {}, "lectionary-cycle", "A", "B"),
            ("advent-1", {"cycle": "A"}, "bible-edition", "douay-rheims", "clementine-vulgate"),
        ]
        view = bridge.call("liturgy", "propers", "postconciliar", "ot-12-thursday", {"cycle": "I"})
        offer = next(one for one in view["comparisonOffers"] if one["dimension"] == "reading-alternative")
        cases.append(("ot-12-thursday", {"cycle": "I"}, "reading-alternative",
                      offer["options"][0]["id"], offer["options"][1]["id"]))
        for key, options, dimension, primary, peer in cases:
            with self.subTest(dimension=dimension):
                compared = bridge.call("liturgy", "comparePropers", "postconciliar", key, options,
                                       {"dimension": dimension, "primary": primary, "peer": peer})
                self.assertIsNone(compared["calendarResult"])
                self.assertEqual(compared["semantic"]["dimension"], dimension)
                self.assertEqual(compared["semantic"]["anchor"]["correspondingFormulary"], key)
                self.assertTrue(compared["blocks"])
                self.assertEqual(compared["selection"]["peer"], peer)

    def test_compare_does_not_choose_a_missing_peer_or_resolve_an_open_choice(self) -> None:
        with self.assertRaisesRegex(Refused, "two distinct held peers"):
            bridge.call("liturgy", "comparePropers", "postconciliar", "advent-1", {},
                        {"dimension": "oration-language", "primary": "la", "peer": "la"})
        with self.assertRaisesRegex(Refused, "choices that remain unresolved"):
            bridge.call("liturgy", "comparePropers", "postconciliar", "ot-12-thursday", {"cycle": "I"},
                        {"dimension": "oration-language", "primary": "la", "peer": "en"})

    def test_reader_urls_round_trip_languages_options_location_and_legacy_pairs(self) -> None:
        options = {"orations": "en", "ordinary": True, "ordinaryLang": "la", "cycle": "A",
                   "textDisplay": "latin-and-selected", "companion": "clementine-vulgate",
                   "variants": {"eucharistic-prayer": "ep-ii"},
                   "location": "proper/postconciliar/transfiguration-lord/001",
                   "urlLegacy": {"unknown": [{"key": "retained-note", "value": "a & b"}], "inert": []}}
        route = bridge.call("liturgy", "readerUrl", "propers", "postconciliar", "transfiguration-lord", options, None)
        self.assertIn("type=christological", route)
        self.assertIn("retained-note=a%20%26%20b", route)
        target = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/" + route.replace("index.html", "propers-reader.html"), "day")
        self.assertEqual(target["entrance"], "propers")
        intent = target["intent"]
        for key in ("orations", "ordinary", "ordinaryLang", "cycle", "textDisplay", "companion", "variants", "location", "urlLegacy"):
            self.assertEqual(intent[key], options[key], key)
        reshared = bridge.call("liturgy", "readerUrl", "propers", intent["calendar"], intent["mass"], intent, None)
        self.assertEqual(reshared, route)

    def test_compare_urls_round_trip_both_entrances(self) -> None:
        cases = [("propers", "postconciliar", "transfiguration-lord",
                  {"dimension": "lectionary-cycle", "primary": "A", "peer": "B"}),
                 ("day", "roman-1962", "2026-10-25", {"peer": "roman-pre-1955"})]
        for entrance, calendar, anchor, selection in cases:
            with self.subTest(entrance=entrance):
                route = bridge.call("liturgy", "readerUrl", entrance, calendar, anchor, {}, selection)
                result = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/" + route, entrance)
                self.assertEqual(result["entrance"], entrance)
                if entrance == "propers":
                    self.assertEqual(result["intent"]["comparison"], selection)
                else:
                    self.assertTrue(result["intent"]["comparing"])
                    self.assertEqual(result["intent"]["peer"], selection["peer"])

    def test_url_import_does_not_discard_invalid_locations_or_custom_data(self) -> None:
        for value, reason in [("#date=2026-05-24&missal=roman-1962&location=proper/no-such-event", "semantic location"),
                              ("?data=https://example.test/other#date=2026-05-24", "custom browser data root")]:
            with self.subTest(value=value), self.assertRaisesRegex(Refused, reason):
                bridge.call("liturgy", "openReaderLink", value, "day")
        browse = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/liturgy/", "day")
        self.assertEqual(browse["entrance"], "propers")
        self.assertTrue(browse["intent"]["browse"])
        self.assertNotIn("mass", browse["intent"])

    def test_the_latin_bible_companion_uses_its_own_numbering_and_rendering(self) -> None:
        view = bridge.call("liturgy", "propers", "roman-1962", "pentecost", {"companion": "clementine-vulgate"})
        self.assertEqual(view["state"]["scriptureCompanion"], {"id": "clementine-vulgate", "numbering": "vulgate"})
        self.assertTrue(any("scripture-pair" in str(row.get("blocks")) for row in view["events"]))
        with self.assertRaisesRegex(Refused, "must be a held Latin Bible"):
            bridge.call("liturgy", "propers", "roman-1962", "pentecost", {"companion": "douay-rheims"})

    def test_native_source_paths_supply_exact_admitted_choice_requests(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "baptism-of-the-lord", {"cycle": "B"})
        (path,) = view["sourcePaths"]
        alternate = next(one for one in path["options"] if one["id"] == "year-b-optional")
        forbidden = next(one for one in path["options"] if one["id"] == "year-c-optional")
        self.assertFalse(alternate["unavailable"])
        self.assertTrue(forbidden["unavailable"])
        self.assertIsNone(forbidden["properChoices"])
        chosen = bridge.call("liturgy", "propers", "postconciliar", "baptism-of-the-lord",
                             {"cycle": "B", "properChoices": alternate["properChoices"]})
        self.assertEqual(chosen["sourcePaths"][0]["selection"]["option"], "year-b-optional")
        self.assertIn("Source reading path", words(chosen["sourcePaths"][0]["blocks"]))
        self.assertTrue(chosen["events"])

    def test_source_path_request_keeps_independent_choices(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "advent-1-monday", {})
        first = next(one for one in view["sourcePaths"][0]["options"] if not one["unavailable"])
        chosen = bridge.call("liturgy", "propers", "postconciliar", "advent-1-monday",
                             {"properChoices": first["properChoices"]})
        second = next(one for one in chosen["sourcePaths"][1]["options"] if not one["unavailable"])
        self.assertTrue(all(second["properChoices"][key] == value for key, value in first["properChoices"].items()))


@unittest.skipUnless(importlib.util.find_spec("textual") and shutil.which("node"), "Textual and node are required")
class SurfaceParityTests(unittest.IsolatedAsyncioTestCase):
    async def test_day_can_reselect_source_mass_and_forms_with_cli_event_parity(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        cases = [
            ("postconciliar", "2026-10-19", "calendar-formulary",
             "saint-paul-cross-priest", "ot-29-monday", None, "pentecost"),
            ("roman-1962", "2026-12-25", "proper-form",
             "night", "day", "nativitate-domini-octave", "first"),
            ("roman-1962", "2026-11-02", "proper-form",
             "first", "third", "commemoratione-omnium-fidelium-defunctorum", "night"),
        ]
        for calendar, date, kind, first, second, mass, foreign in cases:
            with self.subTest(calendar=calendar, date=date):
                app = TriptychApp(start="day", intent={"calendar": calendar, "date": date,
                                      "ordinary": True, "ordinaryLang": "la", "orations": "la"})
                async with app.run_test(size=(120, 40)) as pilot:
                    await _settle(app, pilot)
                    day = app.query_one(Day)
                    for target in (first, second):
                        await pilot.press("s")
                        await _settle(app, pilot)
                        self.assertIsInstance(app.screen, Pick)
                        offered = [(index, value) for index, (value, _) in enumerate(app.screen.options)
                                   if value[2].startswith(kind)]
                        self.assertNotIn(foreign, [value[3] for _, value in offered])
                        matches = [index for index, value in offered if value[3] == target]
                        self.assertEqual(len(matches), 1, (target, offered))
                        app.screen.query_one(OptionList).highlighted = matches[0]
                        await pilot.press("enter")
                        await _settle(app, pilot)
                        row = day.views[calendar]["rows"][0]
                        self.assertNotIn("failed", row)
                        wanted_mass = mass or target
                        wanted_form = target if mass else "main"
                        self.assertEqual(Day.resolved_key(row), wanted_mass)
                        self.assertEqual(row["resolved"].get("form") or "main", wanted_form)
                        direct = bridge.call("liturgy", "day", calendar, date, day.options_for(calendar))
                        events = [(event["id"], event["kind"]) for event in row["events"]]
                        self.assertEqual(events, [(event["id"], event["kind"])
                                                  for event in direct["rows"][0]["events"]])
                        arguments = [sys.executable, str(ROOT / "tools/mass-today"), "show",
                                     "--calendar", calendar, "--date", date,
                                     "--expanded", "--lang", "la", "--format", "json"]
                        if mass:
                            arguments.extend(["--form", target])
                        else:
                            arguments.extend(["--mass", target])
                        done = await asyncio.to_thread(subprocess.run, arguments, cwd=ROOT,
                                                       capture_output=True, text=True, timeout=90)
                        self.assertEqual(done.returncode, 0, done.stderr)
                        selected = next(item for item in json.loads(done.stdout)["days"][0]["masses"]
                                        if item["key"] == wanted_mass)
                        self.assertEqual(selected["selected_form"], wanted_form)
                        self.assertEqual(events, [(event["id"], event["kind"])
                                                  for event in selected["expanded_events"]])
                    invalid = dict(day.options_for(calendar))
                    invalid["form" if mass else "mass"] = foreign
                    rejected = bridge.call("liturgy", "day", calendar, date, invalid)["rows"][0]
                    self.assertIn("failed", rejected)
                    self.assertNotIn("events", rejected)

    async def test_day_compare_waits_for_layout_and_keeps_the_corresponding_unit(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-10-25"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            await pilot.press("i", "down", "down", "enter", "m")
            await _settle(app, pilot)
            await pilot.press("o", "v")
            await _settle(app, pilot)
            self.assertFalse((day.compared or {}).get("refused"))
            self.assertEqual(day.compare_current(), "compare/proper/collect")
            await pilot.press("i", "end", "enter")
            await _settle(app, pilot)
            self.assertEqual(day.compare_current(), day.compare_locations[-1][0])

    async def test_contents_preserves_its_unit_across_bilingual_reflow_and_share(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers
        from lectern.surface import shown
        from textual.widgets import Input

        app = TriptychApp(start="propers", intent={"calendar": "roman-1962", "mass": "pentecost"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            self.assertEqual(propers.ordinary_language, "en")
            chosen = propers.navigation.entries[3][0]
            await pilot.press("i", "down", "down", "down", "down", "enter")
            await _settle(app, pilot)
            box, text = propers.query_one("#propers-reading"), propers.query_one("#propers-text")
            self.assertEqual(propers.navigation.current(box, text), chosen)
            await pilot.press("B")
            await _settle(app, pilot)
            self.assertEqual(propers.navigation.current(box, text), chosen)
            await pilot.press("u")
            await _settle(app, pilot)
            self.assertIn("location=proper%2Froman-1962%2Fpentecost%2F004", app.clipboard)
            await pilot.press("escape", "slash")
            await _settle(app, pilot)
            self.assertTrue(propers.query_one("#propers-query", Input).has_focus)
            self.assertTrue(shown(app.focused))

    async def test_last_contents_target_survives_the_scroll_boundary(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers

        app = TriptychApp(start="propers", intent={"calendar": "postconciliar", "mass": "transfiguration-lord"})
        async with app.run_test(size=(120, 40)) as pilot:
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            propers.comparison = {"dimension": "lectionary-cycle", "primary": "A", "peer": "B"}
            propers.again()
            await _settle(app, pilot)
            wanted = propers.navigation.entries[-1][0]
            await pilot.press("i", "end", "enter")
            await _settle(app, pilot)
            self.assertEqual(propers.navigation.current(propers.query_one("#propers-reading"),
                                                       propers.query_one("#propers-text")), wanted)
            await pilot.press("u")
            await _settle(app, pilot)
            self.assertIn("location=" + wanted.replace("/", "%2F"), app.clipboard)

    async def test_a_day_link_preserves_its_semantic_reading_in_propers(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-05-24"})
        async with app.run_test(size=(120, 40)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            day.orations = "en"
            day.bible = "clementine-vulgate"
            day.text_display = "latin-and-selected"
            day.ordinary = True
            day.ordinary_language = "la"
            day.selection()["witness"] = "edition.edward-caswall.lyra-catholica.london-1849"
            day.load()
            await _settle(app, pilot)
            day.action_propers()
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            self.assertEqual(propers.reading[:2], ("roman-1962", "pentecost"))
            state = propers.view["state"]
            self.assertEqual((state["orations"], state["bible"], state["ordinaryLang"], state["textDisplay"]),
                             ("en", "clementine-vulgate", "la", "latin-and-selected"))
            self.assertEqual(state["witness"], day.selection()["witness"])
            self.assertTrue(state["ordinary"])


if __name__ == "__main__":
    unittest.main()
