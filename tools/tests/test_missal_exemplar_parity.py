"""Cross-surface event and absence checks for the Pentecost exemplars.

The ten Proper names and three variable appointments are an independent,
source-reviewed oracle recorded in guidance/liturgy-browser-roadmap.md C2.
The full frame is compared by event ID between the expanded CLI stream and
real rendered browser DOMs; the CLI's human reading view supplies independent
source-reviewed landmarks.
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROPER_NAMES = (
    "Introit", "Collect", "Lesson", "Alleluia", "Sequence", "Gospel",
    "Offertory", "Secret", "Communion", "Postcommunion",
)
APPOINTMENTS = {
    "preface": "spiritu-sancto",
    "communicantes": "pentecoste",
    "hanc_igitur": "pascha-pentecoste",
}
LANDMARKS = (
    ("Introit", "proper/roman-1962/pentecost/001"),
    ("Collect", "proper/roman-1962/pentecost/002"),
    ("Lesson", "proper/roman-1962/pentecost/003"),
    ("Alleluia", "proper/roman-1962/pentecost/004"),
    ("Sequence", "proper/roman-1962/pentecost/005"),
    ("Gospel", "proper/roman-1962/pentecost/006"),
    ("Offertory", "proper/roman-1962/pentecost/007"),
    ("Secret", "proper/roman-1962/pentecost/008"),
    ("Per Christum Dominum nostrum. Qui ascendens",
     "ordinary-element/praefatio/praefatio-de-spiritu-sancto"),
    ("Communicantes -- the proper form of Pentecost",
     "ordinary-element/canon/communicantes-pentecoste"),
    ("Hanc igitur -- the proper form of Easter and Pentecost",
     "ordinary-element/canon/hanc-igitur-pascha-pentecoste"),
    ("Communion", "proper/roman-1962/pentecost/009"),
    ("Postcommunion", "proper/roman-1962/pentecost/010"),
)


def run(*arguments: str, input_text: str | None = None) -> str:
    completed = subprocess.run(
        arguments, cwd=ROOT, input=input_text, capture_output=True,
        text=True, check=False, timeout=90,
    )
    if completed.returncode:
        raise AssertionError(
            f"{' '.join(arguments)} exited {completed.returncode}: "
            f"{completed.stderr[-1600:]}"
        )
    return completed.stdout


def structure_events(ordinary: dict, mass: dict, context: dict) -> dict:
    script = r"""
const fs = require('fs');
const model = require(process.argv[1]);
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const facts = model.predicateFacts(input.context);
const resolution = model.resolveElements(input.ordinary, {}, facts);
const placed = model.seatPropers(
  input.mass.propers, model.seats(input.ordinary, resolution.shown));
const events = model.massEvents(resolution.shown, placed);
process.stdout.write(JSON.stringify({
  appointments: resolution.appointed,
  unresolved: resolution.unresolved,
  events: events.map(event => event.kind === 'proper'
    ? {id: 'proper/roman-1962/pentecost/' + String(event.sourceIndex + 1).padStart(3, '0'),
       name: event.proper.name, placement: event.placement}
    : event.kind === 'ordinary_element'
      ? {id: 'ordinary-element/' + event.element.key}
      : {id: 'ordinary-section/' + event.section.key})
}));
"""
    return json.loads(run(
        "node", "-e", script,
        str(ROOT / "src/web/browser/liturgy/ordinary-seating.js"),
        input_text=json.dumps({"ordinary": ordinary, "mass": mass, "context": context}),
    ))


class MissalExemplarParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        base = (
            "tools/mass-today", "show", "--date", "2026-05-24",
            "--calendar", "roman-1962", "--expanded", "--bible", "douay-rheims",
        )
        cls.cli_json = json.loads(run(*base, "--format", "json"))
        cls.post_cli_json = json.loads(run(
            "tools/mass-today", "show", "--date", "2026-05-24",
            "--calendar", "postconciliar", "--form", "day", "--expanded",
            "--bible", "douay-rheims", "--format", "json",
        ))
        cls.pre_cli_json = json.loads(run(
            "tools/mass-today", "show", "--date", "2026-05-24",
            "--calendar", "roman-pre-1955", "--expanded",
            "--bible", "douay-rheims", "--format", "json",
        ))
        cls.cli_latin = run(*base, "--lang", "la", "--plain")
        cls.cli_english = run(*base, "--lang", "en", "--plain")
        cls.browser = json.loads(run(
            "node", "tools/tests/missal_exemplar_parity_browser.mjs",
        ))
        cls.propers = json.loads((ROOT / "src/web/data/structure/propers/roman-1962.json").read_text())
        cls.ordinary = json.loads((ROOT / "src/web/data/structure/ordinary/roman-1962.json").read_text())
        cls.mass = next(row for row in cls.propers["masses"] if row["key"] == "pentecost")
        cls.day = next(day for day in cls.cli_json["days"] if day["calendar"] == "roman-1962")
        cls.cli_mass = next(row for row in cls.day["masses"] if row["key"] == "pentecost")
        branch = next(row for row in cls.day["branches"] if row["selected"])
        context = {
            "settled": branch["settled"], "weekday": cls.day["weekday"],
            "season": cls.day["season"], "nature": branch["winner"]["nature"],
            "date": cls.cli_json["date"], "anchors": cls.day["anchors"],
            "appointments": {key: value["option"] for key, value
                             in cls.mass["ordinary_appointments"].items()},
        }
        cls.structural = structure_events(cls.ordinary, cls.mass, context)

    @staticmethod
    def expanded_mass(payload: dict) -> dict:
        day = payload["days"][0]
        return next(row for row in day["masses"] if row["key"] == "pentecost")

    def assert_full_event_parity(self, cli_mass: dict, browser_name: str) -> list[str]:
        cli_events = cli_mass["expanded_events"]
        browser = self.browser[browser_name]
        ids = [event["id"] for event in cli_events]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            [(event["id"], event["kind"]) for event in cli_events],
            [(event["id"], event["kind"]) for event in browser["events"]],
        )
        self.assertEqual(browser["domIds"], ids)
        self.assertNotIn("_proper_source_indices", cli_mass)
        for event in cli_events:
            if event["kind"] == "proper":
                self.assertEqual(
                    event["id"].rsplit("/", 1)[-1],
                    f"{event['source_index'] + 1:03d}",
                )
                self.assertEqual(event["form_id"], cli_mass["selected_form"])
            elif event["kind"] == "proper-choice":
                self.assertEqual(event["form_id"], cli_mass["selected_form"])
                self.assertTrue(event["options"])
        return ids

    def test_identity_propers_and_appointed_variables(self) -> None:
        self.assertEqual(self.browser["problems"], [])
        self.assertEqual(self.cli_json["date"], "2026-05-24")
        self.assertEqual(self.day["selected_mass"], "pentecost")
        self.assertEqual(self.cli_mass["selected"], True)
        self.assertEqual(self.cli_mass["ordinary_appointments"], APPOINTMENTS)
        self.assertEqual(
            {key: value["option"] for key, value
             in self.mass["ordinary_appointments"].items()}, APPOINTMENTS,
        )
        self.assertEqual([row["name"] for row in self.mass["propers"]], list(PROPER_NAMES))
        self.assertEqual([row["name"] for row in self.cli_mass["propers"]], list(PROPER_NAMES))
        for name in ("dayRead", "dayMissal", "propersRead", "dayEnglish"):
            with self.subTest(name=name):
                self.assertEqual(self.browser[name]["outcome"], "ready")
                self.assertEqual(self.browser[name]["resolved"]["edition"], "roman-1962")
                self.assertEqual(self.browser[name]["resolved"]["formulary"], "pentecost")
                self.assertEqual(self.browser[name]["literalLeaks"], [])
                self.assertEqual(self.browser[name]["pageLeaks"], [])
                self.assertNotRegex(
                    self.browser[name]["coverageNotice"],
                    r"\b(?:undefined|null|NaN)\b|\[object Object\]",
                )

    def test_generated_full_frame_matches_browser_semantics_and_dom(self) -> None:
        expected = [event["id"] for event in self.structural["events"]]
        browser = self.browser["dayMissal"]
        self.assertEqual(self.structural["unresolved"], [])
        self.assertEqual(self.structural["appointments"], APPOINTMENTS)
        self.assertEqual(len(expected), 179)
        self.assertEqual(self.assert_full_event_parity(self.cli_mass, "dayMissal"), expected)
        self.assertEqual(self.assert_full_event_parity(self.cli_mass, "propersMissal"), expected)
        self.assertEqual(
            [event["name"] for event in self.structural["events"] if "name" in event],
            list(PROPER_NAMES),
        )
        self.assertTrue(all(event["placement"] == "seated" for event
                            in self.structural["events"] if "name" in event))
        for required in (
            "ordinary-element/praefatio/praefatio-de-spiritu-sancto-initium",
            "ordinary-element/praefatio/praefatio-de-spiritu-sancto",
            "ordinary-element/canon/communicantes-pentecoste",
            "ordinary-element/canon/hanc-igitur-pascha-pentecoste",
        ):
            self.assertIn(required, expected)
        for forbidden in (
            "ordinary-element/canon/communicantes",
            "ordinary-element/canon/hanc-igitur",
            "ordinary-element/praefatio/praefatio-communis",
        ):
            self.assertNotIn(forbidden, expected)
        shown = {row["id"]: row["text"] for row in browser["variableNodes"]}
        self.assertIn("VERE dignum et justum est", shown[
            "ordinary-element/praefatio/praefatio-de-spiritu-sancto-initium"])
        self.assertIn("promissum Spiritum sanctum", shown[
            "ordinary-element/praefatio/praefatio-de-spiritu-sancto"])
        self.assertIn("diem sacratissimum Pentecostes", shown[
            "ordinary-element/canon/communicantes-pentecoste"])
        self.assertIn("quos regenerare dignatus es", shown[
            "ordinary-element/canon/hanc-igitur-pascha-pentecoste"])

    def test_postconciliar_day_and_pre_1955_full_event_parity(self) -> None:
        post = self.expanded_mass(self.post_cli_json)
        post_ids = self.assert_full_event_parity(post, "postDayMissal")
        self.assertEqual(len(post_ids), 71)
        self.assertEqual(post["selected_form"], "day")
        self.assertEqual(post["ordinary_appointments"], {
            "dismissal": "paschal-double-alleluia", "preface": "pentecost",
        })
        choices = [event for event in post["expanded_events"]
                   if event["kind"] == "proper-choice"]
        self.assertEqual(choices, [{
            "id": "proper-choice/postconciliar/pentecost/day/entrance-antiphon",
            "kind": "proper-choice", "source_index": 14, "form_id": "day",
            "options": [
                {"id": "spiritus-domini", "events": ["proper/postconciliar/pentecost/015"]},
                {"id": "caritas-dei", "events": ["proper/postconciliar/pentecost/016"]},
            ],
        }])
        self.assertEqual(
            [(row["id"], [option["id"] for option in row["options"]])
             for row in self.browser["postDayMissal"]["events"]
             if row["kind"] == "proper-choice"],
            [(choices[0]["id"], ["spiritus-domini", "caritas-dei"])],
        )
        # Propers has no civil date.  Its two date-conditioned Ordinary rows
        # therefore remain unresolved instead of inheriting Day's predicate.
        post_propers = self.browser["postPropersMissal"]
        self.assertEqual(post_propers["calendarResult"], None)
        self.assertEqual(
            {row["element"] for row in post_propers["ordinaryUnresolved"]},
            {"ritus-initiales/gloria-in-excelsis", "symbolum/symbolum-nicaenum"},
        )
        self.assertEqual(
            set(post_ids) - set(event["id"] for event in post_propers["events"]),
            {"ordinary-element/ritus-initiales/gloria-in-excelsis",
             "ordinary-element/symbolum/symbolum-nicaenum"},
        )
        self.assertEqual(
            [event["id"] for event in post_propers["events"]],
            [event_id for event_id in post_ids if event_id not in {
                "ordinary-element/ritus-initiales/gloria-in-excelsis",
                "ordinary-element/symbolum/symbolum-nicaenum",
            }],
        )
        self.assertEqual(post_propers["domIds"],
                         [event["id"] for event in post_propers["events"]])

        pre = self.expanded_mass(self.pre_cli_json)
        pre_ids = self.assert_full_event_parity(pre, "preDayMissal")
        self.assertEqual(len(pre_ids), 181)
        self.assertEqual(self.assert_full_event_parity(pre, "prePropersMissal"), pre_ids)
        self.assertEqual(pre["ordinary_appointments"], APPOINTMENTS)
        self.assertEqual(pre["recension_coverage"]["status"], "structural-only")
        self.assertIn("inherited", self.browser["preDayMissal"]["coverageNotice"].lower())

    def test_cli_printed_landmarks_follow_browser_event_order(self) -> None:
        browser_ids = [event["id"] for event in self.browser["dayMissal"]["events"]]
        for output in (self.cli_latin, self.cli_english):
            positions = []
            for heading, event_id in LANDMARKS:
                match = re.search(r"^      " + re.escape(heading) +
                                  r"(?: --[^\n]*)?(?: \([^\n]*\))?$",
                                  output, re.MULTILINE)
                self.assertIsNotNone(match, heading)
                positions.append(match.start())
                self.assertIn(event_id, browser_ids)
            self.assertEqual(positions, sorted(positions))
        self.assertEqual(
            [browser_ids.index(event_id) for _, event_id in LANDMARKS],
            sorted(browser_ids.index(event_id) for _, event_id in LANDMARKS),
        )
        proper_ids = [event["id"] for event in self.browser["dayRead"]["events"]]
        self.assertEqual(self.browser["dayRead"]["domIds"], proper_ids)
        self.assertEqual(self.browser["propersRead"]["domIds"], proper_ids)
        self.assertEqual(self.browser["dayEnglish"]["domIds"], proper_ids)

    def test_lesson_english_absence_keeps_latin_and_types_bible_text(self) -> None:
        lesson = self.mass["propers"][2]
        english = next(row for row in lesson["coverage"]["languages"] if row["lang"] == "en")
        self.assertEqual(english["availability"], "unresolved")
        self.assertEqual(english["relationship"], "unresolved")
        self.assertEqual(english["witnesses"], [])
        self.assertIn("(no en translation recorded; showing Latin)", self.cli_english)
        rendered = self.browser["dayEnglish"]["lesson"]
        self.assertIn("English translation unavailable: not resolved", rendered)
        self.assertIn("The Latin original is shown", rendered)
        self.assertIn("Lectio Actuum Apostolorum", rendered)
        self.assertIn("not the Missal’s wording", rendered)


if __name__ == "__main__":
    unittest.main()
