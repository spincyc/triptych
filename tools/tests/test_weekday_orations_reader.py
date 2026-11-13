"""Explicit weekday prayers keep their source owners in each reader."""
from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import unittest
from pathlib import Path
from datetime import date
from unittest.mock import Mock, PropertyMock, patch

from tools.tests._product_data import browser_data_root

ROOT = Path(__file__).resolve().parents[2]
PROBE = Path(__file__).with_name("weekday_orations_chromium.mjs")


class WeekdayOrationReaderTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required for the terminal surface")
    def test_terminal_source_named_mass_choice_is_actionable(self):
        from lectern.surfaces.day import Day
        day = Day()
        day.calendar = "roman-1962"
        day.date = date(2026, 3, 27)
        day.calendars = []
        choice = "seven-sorrows-where-devotions-are-held"
        day.views = {day.calendar: {"rows": [{"primaryDayChoice": choice, "unresolvedChoices": [{
            "id": choice, "reason": "The source authorizes these formularies without a default.",
            "options": [{"id": "passion-friday"}, {"id": "comm-septem-dolorum-beatae-mariae-virginis"}]}],
            "events": []}]}}
        offers = day.offers(day.calendar)
        self.assertEqual([one[0][3] for one in offers], [
            "passion-friday", "comm-septem-dolorum-beatae-mariae-virginis"])
        app = Mock()
        with patch.object(Day, "app", new_callable=PropertyMock, return_value=app), patch.object(day, "load") as reload:
            day.action_choose()
            picked = app.push_screen.call_args.args[1]
            picked(offers[0][0])
            self.assertEqual(day.selection()["mass"], "passion-friday")
            reload.assert_called_once()

    @unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required for the terminal surface")
    def test_terminal_location_requires_confirmation_and_is_not_imported(self):
        from lectern.surfaces.day import Day
        day = Day()
        attestation = {"schema": "triptych-dedication-location/v1", "calendar": "roman-1962",
            "civilDate": "2026-11-09", "mass": "dedicatione-archibasilicae-mi-salvatoris",
            "formId": "main", "territory": None, "relation": "in-dedicated-church"}
        day.follow(date=attestation["civilDate"], calendar=attestation["calendar"],
                   dedicationAttestation=attestation, replace=True)
        day.adopt_pending()
        self.assertNotIn("dedicationAttestation", day.options_for("roman-1962"))
        day.selection()["dedicationAttestation"] = attestation
        self.assertEqual(day.options_for("roman-1962")["dedicationAttestation"], attestation)
        day.date = date(2026, 11, 18)
        self.assertNotIn("dedicationAttestation", day.options_for("roman-1962"))
        self.assertNotIn("dedicationAttestation", day.options_for("postconciliar"))

    @unittest.skipUnless(importlib.util.find_spec("textual"), "Textual is required for the terminal surface")
    def test_terminal_chooser_and_import_are_scoped_to_date_and_calendar(self):
        from lectern.surfaces.day import Day
        day = Day()
        day.follow(date="2026-01-12", calendar="postconciliar", orationMass="ot-2", replace=True)
        day.adopt_pending()
        self.assertEqual(day.options_for("postconciliar")["orationMass"], "ot-2")
        day.views = {"postconciliar": {"rows": [{"orationChoices": {
            "locus": "IGMR 363", "options": [{"id": "ot-2", "label": "Second Sunday in Ordinary Time"}]},
            "orationSelection": {"owner": "ot-2"}, "events": []}]}}
        self.assertEqual(day.offers("postconciliar")[0][0][2:4], ("weekday-orations", "ot-2"))
        day.date = date(2026, 1, 13)
        self.assertNotIn("orationMass", day.options_for("postconciliar"))
        self.assertNotIn("orationMass", day.options_for("roman-1962"))

    def test_probe_parses(self):
        subprocess.run(["node", "--check", str(PROBE)], check=True,
                       capture_output=True, text=True, timeout=15)

    def test_terminal_selection_preserves_sources_and_round_trips(self):
        options = {"orations": "en", "orationMass": "ot-2"}
        requests = [
            {"id": 1, "adapter": "liturgy", "fn": "day", "args": ["postconciliar", "2026-01-12", options]},
            {"id": 2, "adapter": "liturgy", "fn": "readerUrl", "args": ["day", "postconciliar", "2026-01-12", options, None]},
            {"id": 3, "adapter": "liturgy", "fn": "openReaderLink", "args": [
                "liturgy/day.html#date=2026-01-12&missal=postconciliar&bible=douay-rheims&orations=en&oration-mass=ot-2", "day"]},
        ]
        process = subprocess.run(["node", str(ROOT / "scripts/lectern/bridge.js"), str(browser_data_root(ROOT))],
            input="".join(json.dumps(row) + "\n" for row in requests), text=True, capture_output=True, timeout=60)
        self.assertEqual(process.returncode, 0, process.stderr)
        replies = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual(len(replies), 3, process.stdout)
        self.assertTrue(all(row["ok"] for row in replies), process.stdout)
        events = replies[0]["value"]["rows"][0]["events"]
        prayers = [row for row in events if "/ot-2/" in row["id"]]
        self.assertEqual(len(prayers), 3)
        self.assertEqual(len([row for row in events if "/ot-1-monday/" in row["id"]]), 4)
        self.assertTrue(all(row.get("blocks") and not row.get("problem") for row in prayers))
        self.assertIn("oration-mass=ot-2", replies[1]["value"])
        self.assertEqual(replies[2]["value"]["intent"]["orationMass"], "ot-2")

    @unittest.skipUnless(os.environ.get("TRIPTYCH_WEEKDAY_CHROMIUM") == "1",
                         "set TRIPTYCH_WEEKDAY_CHROMIUM=1 for source-served Chromium")
    def test_native_selection_reload_scope_and_source_qualification(self):
        process = subprocess.run(["node", str(PROBE)], cwd=ROOT, capture_output=True, text=True, timeout=180)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        report = json.loads(process.stdout.strip().splitlines()[-1])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["checks"], 22)
        for key in ("consoleProblems", "failedRequests", "httpProblems"):
            self.assertEqual(report[key], [])
