#!/usr/bin/env python3
"""The Ordinary variables a day appoints, seated over the real generated data.

C2 gaps G5-G8 (2026-10-19). Missal mode seats exactly the appointed Preface,
Communicantes and Hanc igitur, a typed stand-in where the appointed text is not
held or the appointment is not established, and never the common form in a
proper seat; the 1962 frame excludes the second-Postcommunion regime and Et
famulos; the postconciliar frame seats the Sequence; and on Pentecost Sunday
the postconciliar Day takes the Day form, the Vigil being appointed for the
evening before.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NODE = r"""
const fs = require('fs');
const root = process.cwd() + '/src/web/browser/liturgy/';
const C = require(root + 'reader-state.js');
const A = require(root + 'reader-state-adapters.js');
const M = require(root + 'assembly-model.js');
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
function request(entrance, calendar, date, form) {
  const held = {
    schema: C.STATE_SCHEMA, entrance: entrance, civilDate: date,
    edition: { id: calendar }, calendar: { id: calendar },
    bible: { id: 'douay-rheims', numbering: 'vulgate' },
    languages: { orations: 'la', ordinary: 'en' }, requestedMode: 'missal',
    options: { ordinary: true, legitimate: {} },
    coverage: [], unresolvedChoices: [], sourceHooks: []
  };
  if (form) {
    held.form = form;
    held.selectedReadableFormulary = { id: 'pentecost' };
  }
  return held;
}
function project(result) {
  return {
    resolved: result.resolved || null,
    choices: (result.unresolvedChoices || []).map((one) => one.id),
    ordinary: (result.events || []).filter((one) => one.kind === 'ordinary-element')
      .map((one) => one.id.replace('ordinary-element/', '')),
    propers: (result.events || []).filter((one) => one.kind === 'proper')
      .map((one) => [one.editionSlotLabel, one.seat && one.seat.id]),
    unresolved: (result.ordinaryUnresolved || []).map((one) => one.element)
  };
}
const out = {};
for (const row of input.days) {
  const year = read('src/web/data/structure/calendar/' + row.calendar + '/' +
    row.date.slice(0, 4) + '.json');
  const rubrics = read('src/web/data/structure/rubrics/' + row.calendar + '.json');
  out[row.id] = project(A.adaptDay({
    request: request('day', row.calendar, row.date, row.form),
    derived: M.derive({ year: year, rubrics: rubrics, date: row.date }),
    structure: read('src/web/data/structure/propers/' + row.calendar + '.json'),
    ordinary: read('src/web/data/structure/ordinary/' + row.calendar + '.json')
  }));
}
const propersRequest = {
  schema: C.STATE_SCHEMA, entrance: 'propers', civilDate: null,
  edition: { id: 'postconciliar' }, formulary: { id: 'pentecost' },
  bible: { id: 'douay-rheims', numbering: 'vulgate' },
  languages: { orations: 'la' }, requestedMode: 'read',
  options: { ordinary: false, legitimate: {} },
  coverage: [], unresolvedChoices: [], sourceHooks: []
};
out.propersPentecost = project(A.adaptPropers({
  request: propersRequest,
  structure: read('src/web/data/structure/propers/postconciliar.json')
}));
process.stdout.write(JSON.stringify(out));
"""

DAYS = [
    {"id": "pentecost1962", "calendar": "roman-1962", "date": "2026-05-24"},
    {"id": "pentecostPre1955", "calendar": "roman-pre-1955", "date": "2026-05-24"},
    {"id": "pentecostX1962", "calendar": "roman-1962", "date": "2026-08-02"},
    {"id": "epiphanyFeria1962", "calendar": "roman-1962", "date": "2026-01-08"},
    {"id": "epiphany1962", "calendar": "roman-1962", "date": "2026-01-06"},
    {"id": "holyFamilyPre1955", "calendar": "roman-pre-1955", "date": "2026-01-11"},
    {"id": "pentecostPost", "calendar": "postconciliar", "date": "2026-05-24"},
    {"id": "pentecostPostVigil", "calendar": "postconciliar", "date": "2026-05-24",
     "form": "vigil"},
    {"id": "easterPost", "calendar": "postconciliar", "date": "2026-04-05"},
    {"id": "adventPost", "calendar": "postconciliar", "date": "2026-11-29"},
]


def run() -> dict:
    finished = subprocess.run(
        ["node", "-e", NODE], input=json.dumps({"days": DAYS}), cwd=ROOT,
        capture_output=True, text=True, check=False,
    )
    if finished.returncode:
        raise AssertionError(finished.stderr[-4000:])
    return json.loads(finished.stdout)


PREFACE_ROWS = (
    "praefatio/praefatio-communis", "praefatio/praefatio-communis-heading",
)


class OrdinaryAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run()

    def prefaces(self, key: str) -> list[str]:
        return [
            one for one in self.report[key]["ordinary"]
            if one.startswith("praefatio/praefatio")
        ]

    def test_1962_pentecost_seats_one_preface_and_no_common_canon_form(self) -> None:
        for key in ("pentecost1962", "pentecostPre1955"):
            day = self.report[key]
            self.assertEqual(
                self.prefaces(key),
                [
                    "praefatio/praefatio-de-spiritu-sancto-heading",
                    "praefatio/praefatio-de-spiritu-sancto",
                ],
                key,
            )
            ordinary = day["ordinary"]
            # The Sanctus follows the proper Preface, never before it.
            self.assertLess(
                ordinary.index("praefatio/praefatio-de-spiritu-sancto"),
                ordinary.index("praefatio/sanctus-post-praefationem"), key,
            )
            self.assertNotIn("praefatio/sanctus", ordinary, key)
            # Proper Canon forms: typed absences in the appointed place, and
            # never the common Communicantes or Hanc igitur.
            self.assertIn("canon/communicantes-pentecoste", ordinary, key)
            self.assertIn("canon/hanc-igitur-pascha-pentecoste", ordinary, key)
            self.assertNotIn("canon/communicantes", ordinary, key)
            self.assertNotIn("canon/hanc-igitur", ordinary, key)
            self.assertLess(
                ordinary.index("canon/et-omnium-circumstantium"),
                ordinary.index("canon/communicantes-pentecoste"), key,
            )
            self.assertLess(
                ordinary.index("canon/communicantes-pentecoste"),
                ordinary.index("canon/quam-oblationem"), key,
            )
            self.assertEqual(day["unresolved"], [], key)

    def test_ordinary_green_sunday_keeps_the_common_canon_forms(self) -> None:
        ordinary = self.report["pentecostX1962"]["ordinary"]
        self.assertIn("canon/communicantes", ordinary)
        self.assertIn("canon/hanc-igitur", ordinary)
        self.assertNotIn("canon/communicantes-pentecoste", ordinary)
        # Its Preface is not appointed yet: one typed stand-in, not eleven.
        self.assertEqual(self.prefaces("pentecostX1962"), ["praefatio/praefatio-diei"])
        self.assertIn("praefatio/sanctus", ordinary)

    def test_feast_only_canon_forms_do_not_follow_a_borrowed_formulary(self) -> None:
        feast = self.report["epiphany1962"]
        feria = self.report["epiphanyFeria1962"]
        self.assertEqual(feast["resolved"]["formulary"], "epiphania-domini")
        self.assertEqual(feria["resolved"]["formulary"], "epiphania-domini")
        self.assertIn("canon/communicantes-epiphania", feast["ordinary"])
        self.assertIn("canon/communicantes", feria["ordinary"])
        self.assertNotIn("canon/communicantes-epiphania", feria["ordinary"])
        # The pre-1955 witness says the Epiphany form through its octave.
        self.assertIn(
            "canon/communicantes-epiphania", self.report["holyFamilyPre1955"]["ordinary"]
        )

    def test_1962_frame_excludes_second_postcommunion_regime_and_et_famulos(self) -> None:
        ordinary = self.report["pentecost1962"]["ordinary"]
        for key in (
            "conclusio/rubrica-postcommunio-secunda", "conclusio/postcommunio-mundet",
            "conclusio/rubrica-postcommunio-paschalis", "conclusio/rubrica-oratio-addita",
            "conclusio/oratio-et-famulos-heading", "conclusio/et-famulos",
        ):
            self.assertNotIn(key, ordinary)
        self.assertIn(["Postcommunion", "postcommunio"], self.report["pentecost1962"]["propers"])

    def test_pre_1955_seasonal_orations_are_not_said_on_pentecost(self) -> None:
        ordinary = self.report["pentecostPre1955"]["ordinary"]
        for key in (
            "oblatio/a-cunctis", "oblatio/secreta-ii", "conclusio/postcommunio-mundet",
            "oblatio/rubrica-secreta", "conclusio/rubrica-postcommunio-secunda",
            "oblatio/rubrica-collecta-concede", "oblatio/rubrica-secreta-concede",
            "conclusio/rubrica-postcommunio-paschalis",
        ):
            self.assertNotIn(key, ordinary)
        propers = self.report["pentecostPre1955"]["propers"]
        self.assertIn(["Secret", "secreta"], propers)
        self.assertIn(["Postcommunion", "postcommunio"], propers)

    def test_postconciliar_sequence_is_seated_and_frame_is_full(self) -> None:
        for key in ("pentecostPost", "easterPost"):
            day = self.report[key]
            self.assertIn(["Sequence", "sequentia"], day["propers"], key)
            ordinary = day["ordinary"]
            self.assertIn("liturgia-verbi/acclamatio-ante-evangelium", ordinary, key)
            labels = [one[0] for one in day["propers"]]
            self.assertLess(labels.index("Second Reading"), labels.index("Sequence"), key)
            self.assertLess(labels.index("Sequence"), labels.index("Gospel Acclamation"), key)

    def test_postconciliar_pentecost_appoints_its_preface_and_dismissal(self) -> None:
        ordinary = self.report["pentecostPost"]["ordinary"]
        self.assertIn("prex-eucharistica/praefatio-appointed", ordinary)
        self.assertNotIn("prex-eucharistica/praefatio", ordinary)
        self.assertIn("ritus-conclusionis/dimissio-appointed", ordinary)
        self.assertNotIn("ritus-conclusionis/dimissio", ordinary)
        advent = self.report["adventPost"]["ordinary"]
        self.assertIn("prex-eucharistica/praefatio", advent)
        self.assertIn("ritus-conclusionis/dimissio", advent)
        self.assertNotIn("prex-eucharistica/praefatio-appointed", advent)

    def test_pentecost_day_takes_the_day_form_and_vigil_stays_explicit(self) -> None:
        day = self.report["pentecostPost"]
        self.assertEqual(day["resolved"]["form"], "day")
        self.assertNotIn("proper-form:postconciliar/pentecost", day["choices"])
        vigil = self.report["pentecostPostVigil"]
        self.assertEqual(vigil["resolved"]["form"], "vigil")
        # The date-independent Propers entrance still offers both forms.
        self.assertIn(
            "proper-form:postconciliar/pentecost", self.report["propersPentecost"]["choices"]
        )

    def test_cli_selects_the_day_form_and_seats_the_same_appointments(self) -> None:
        finished = subprocess.run(
            ["python3", "tools/mass-today", "--date", "2026-05-24", "--calendar",
             "postconciliar", "--expanded", "--plain"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(finished.returncode, 0, finished.stderr[-2000:])
        self.assertIn("The Preface of the Mystery of Pentecost", finished.stdout)
        self.assertIn("The paschal Dismissal, with a double Alleluia", finished.stdout)
        self.assertNotIn("choose one with --form", finished.stdout)
        finished = subprocess.run(
            ["python3", "tools/mass-today", "--date", "2026-05-24", "--calendar",
             "roman-1962", "--expanded", "--plain"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(finished.returncode, 0, finished.stderr[-2000:])
        self.assertIn("Communicantes -- the proper form of Pentecost", finished.stdout)
        self.assertNotIn("Communicantes, et memoriam venerantes", finished.stdout)
        self.assertNotIn("The PREFACE on Festivals", finished.stdout)


if __name__ == "__main__":
    unittest.main()
