import datetime as dt
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]


def tool_json(*arguments: str) -> dict:
  completed = subprocess.run(
    [str(ROOT / "tools/tpt"), *arguments, "--format", "json"],
    cwd=ROOT,
    check=True,
    capture_output=True,
    text=True,
  )
  return json.loads(completed.stdout)


def nominal_resumed_slots(pentecost_sundays: int) -> dict[int, str]:
  """Return the fixed RG 18 map; occurrence is deliberately out of scope."""
  if pentecost_sundays == 23:
    raise ValueError("RG 18 does not legislate the P=23 shortfall")
  starts = {24: None, 25: 6, 26: 5, 27: 4, 28: 3}
  first = starts.get(pentecost_sundays)
  if first is None:
    return {}
  return {
    slot: f"Epiphany {first + slot - 24}"
    for slot in range(24, pentecost_sundays)
  }


def apply_occurrence(
    nominal: dict[dt.date, str], winners: dict[dt.date, str]
) -> dict[dt.date, tuple[str, str, bool]]:
  """Overlay winners without shifting any later nominal assignment."""
  return {
    date: (formulary, winners.get(date, formulary), date in winners)
    for date, formulary in nominal.items()
  }


class CalendarComputationGuidanceTest(unittest.TestCase):
  def test_rg18_branches_are_fixed_slots(self):
    self.assertEqual(nominal_resumed_slots(24), {})
    self.assertEqual(nominal_resumed_slots(25), {24: "Epiphany 6"})
    self.assertEqual(
      nominal_resumed_slots(28),
      {
        24: "Epiphany 3",
        25: "Epiphany 4",
        26: "Epiphany 5",
        27: "Epiphany 6",
      },
    )

  def test_2008_collisions_do_not_compress(self):
    dates = [dt.date(2008, 10, 26) + dt.timedelta(weeks=n) for n in range(4)]
    nominal = dict(zip(dates, nominal_resumed_slots(28).values()))
    result = apply_occurrence(
      nominal,
      {
        dt.date(2008, 10, 26): "Christ the King",
        dt.date(2008, 11, 9): "Lateran dedication",
      },
    )
    self.assertEqual(result[dt.date(2008, 10, 26)], ("Epiphany 3", "Christ the King", True))
    self.assertEqual(result[dt.date(2008, 11, 2)], ("Epiphany 4", "Epiphany 4", False))
    self.assertEqual(result[dt.date(2008, 11, 9)], ("Epiphany 5", "Lateran dedication", True))
    self.assertEqual(result[dt.date(2008, 11, 16)], ("Epiphany 6", "Epiphany 6", False))

  def test_p23_fails_closed(self):
    with self.assertRaisesRegex(ValueError, "P=23"):
      nominal_resumed_slots(23)

  def test_1962_reader_calendar_has_68_parents(self):
    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    parent_ids = re.findall(r"^\| (\d{2}) \| \*\*", landing, re.MULTILINE)
    self.assertEqual(parent_ids, [f"{n:02d}" for n in range(1, 69)])
    self.assertIn("| 27 | **Mass of the Lord's Supper** | Planned | Planned |", landing)
    self.assertIn(
      "| 28 | **Solemn Liturgical Action of the Passion and Death of the Lord** "
      "| Planned | Planned |",
      landing,
    )
    self.assertIn("| 29 | **Easter Vigil** | Planned | Planned |", landing)

  def test_postconciliar_registry_and_reader_calendar_arithmetic(self):
    registry = (
      ROOT / "guidance/liturgy/postconciliar-propers-registry.md"
    ).read_text()
    landing = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    parents = re.findall(
      r"^\| (PC-S\d{2}) \| `[^`]+` \| [^|]+ \|$", registry, re.MULTILINE
    )
    rows = re.findall(
      r"^\| \*\*(.+?)\*\* \|.*\|.*\|.*\|$",
      landing.split("## Sunday Propers Calendar")[1].split("### Sunday replacements")[0],
      re.MULTILINE,
    )
    counts = [
      int(value)
      for value in re.findall(
        r"^\| PC-S\d{2} \| `[^`]+`(?:, `[^`]+`)* \| [^|]+ \| (\d+) \|$",
        registry,
        re.MULTILINE,
      )
    ]
    self.assertEqual(parents, [f"PC-S{n:02d}" for n in range(1, 61)])
    self.assertEqual(len(rows), 63)
    self.assertEqual(sum(counts), 184)
    self.assertIn(
      "| PC-T01 | `pc-t01-evening-mass-of-the-lords-supper` | "
      "Evening Mass of the Lord's Supper | `PC-T01-ABC` |",
      registry,
    )
    self.assertIn(
      "| PC-T02 | `pc-t02-celebration-of-the-lords-passion` | "
      "Celebration of the Lord's Passion | `PC-T02-ABC` |",
      registry,
    )
    self.assertIn(
      "| PC-T03 | `pc-t03-easter-vigil` | Easter Vigil | "
      "Alias of `PC-S17-A-VIGIL`, `PC-S17-B-VIGIL`, and "
      "`PC-S17-C-VIGIL` |",
      registry,
    )
    # The Triduum entries are now inline in the Sunday Propers Calendar,
    # ordered between Palm Sunday and Easter Sunday.
    calendar = landing.split("## Sunday Propers Calendar", 1)[1].split(
      "### Sunday replacements", 1
    )[0]
    self.assertIn(
      "| **Evening Mass of the Lord's Supper** | Planned | Planned | Planned |",
      calendar,
    )
    self.assertIn(
      "| **Celebration of the Lord's Passion** | Planned | Planned | Planned |",
      calendar,
    )
    self.assertIn(
      "| **Easter Vigil** | Planned with Easter Sunday | "
      "Planned with Easter Sunday | Planned with Easter Sunday |",
      calendar,
    )
    # Verify Triduum ordering: Palm Sunday < Supper < Passion < Vigil < Easter
    palm = calendar.index("**Palm Sunday of the Passion of the Lord**")
    supper = calendar.index("**Evening Mass of the Lord's Supper**")
    passion = calendar.index("**Celebration of the Lord's Passion**")
    vigil = calendar.index("**Easter Vigil**")
    easter = calendar.index("**Easter Sunday of the Resurrection of the Lord**")
    self.assertLess(palm, supper)
    self.assertLess(supper, passion)
    self.assertLess(passion, vigil)
    self.assertLess(vigil, easter)
    self.assertNotRegex(calendar, r"\bPC-[A-Z0-9-]+\b")
    # The production plan no longer restates the registry's counts, so there
    # is no totals table to assert on; the registry above is the one source.
    self.assertIn(
      "| **Nativity of the Lord** | Planned | Planned | Planned |",
      landing,
    )
    self.assertNotRegex(landing, r"\b\d+ planned\b")
    self.assertIn(
      "| PC-R08 | **Commemoration of All the Faithful Departed** | "
      "Unresolved | Unresolved | Unresolved |",
      landing,
    )

  def test_sunday_catalog_links_only_installed_publications(self):
    permitted_full_guides = {
      *(f"{number:02d}-{slug}.pdf" for number, slug in (
        (39, "trinity-sunday"),
        (41, "second-after-pentecost"),
        (43, "third-after-pentecost"),
        (44, "fourth-after-pentecost"),
        (45, "fifth-after-pentecost"),
        (46, "sixth-after-pentecost"),
        (47, "seventh-after-pentecost"),
        (48, "eighth-after-pentecost"),
        (50, "tenth-after-pentecost"),
        (54, "fourteenth-after-pentecost"),
      )),
      *(f"pc-s{number}-{slug}-year-a.pdf" for number, slug in (
        (37, "eleventh-sunday-in-ordinary-time"),
        (38, "twelfth-sunday-in-ordinary-time"),
        (39, "thirteenth-sunday-in-ordinary-time"),
        (40, "fourteenth-sunday-in-ordinary-time"),
        (41, "fifteenth-sunday-in-ordinary-time"),
        (42, "sixteenth-sunday-in-ordinary-time"),
        (26, "most-holy-trinity"),
        (27, "most-holy-body-and-blood-of-christ"),
      )),
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf",
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf",
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf",
    }
    for name in ("traditional-latin-mass.md", "novus-ordo-liturgy.md"):
      text = (ROOT / "library" / name).read_text()
      calendar = text.split("## Sunday Propers Calendar", 1)[1]
      for target in re.findall(r"\]\((\.\./pdf/[^)]+\.pdf)\)", calendar):
        if "m01-nuptial-mass.pdf" not in target:
          self.assertTrue(
            target.endswith("-synthesis.pdf")
            or target.rsplit("/", 1)[-1] in permitted_full_guides,
            target,
          )
        self.assertTrue((ROOT / "library" / target).resolve().exists(), target)

  def test_approved_alpha_propers_do_not_regress_to_planned(self):
    traditional = (ROOT / "library/traditional-latin-mass.md").read_text()
    for proper_id in (39, 41, 43, 44, 45, 46, 47, 48):
      row = re.search(rf"^\| {proper_id:02d} \|.*$", traditional, re.MULTILINE)
      self.assertIsNotNone(row)
      self.assertIn("../pdf/gpt/", row.group())
      if proper_id == 48:
        self.assertIn("../pdf/claude/", row.group())
        self.assertIn("../web/claude/", row.group())
      else:
        self.assertTrue(row.group().endswith("| Planned |"))
    self.assertIn("| 38 | **Pentecost Sunday** | Planned | Planned |", traditional)

    postconciliar = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    for name in (
      "Most Holy Trinity",
      "Eleventh Sunday in Ordinary Time",
      "Twelfth Sunday in Ordinary Time",
      "Thirteenth Sunday in Ordinary Time",
      "Fourteenth Sunday in Ordinary Time",
      "Fifteenth Sunday in Ordinary Time",
      "Sixteenth Sunday in Ordinary Time",
      "Most Holy Body and Blood of Christ",
    ):
      row = re.search(
        rf"^\| \*\*{re.escape(name)}\*\* \|.*$", postconciliar, re.MULTILINE
      )
      self.assertIsNotNone(row, f"Row not found for: {name}")
      self.assertIn("../pdf/gpt/", row.group())
      if name == "Sixteenth Sunday in Ordinary Time":
        self.assertIn("../pdf/claude/", row.group())


@unittest.skipUnless(shutil.which("node"), "node is required by calendar-rubrics")
class CalendarSelectionSemanticsTest(unittest.TestCase):
  def rubric_day(self, date: str) -> dict:
    payload = tool_json(
      "calendar-rubrics", "day", "--date", date, "--calendar", "postconciliar"
    )
    self.assertEqual(payload["status"], "ok")
    self.assertEqual(payload["problems"], [])
    self.assertEqual(len(payload["days"]), 1)
    return payload["days"][0]

  def proper_forms(self, key: str) -> list[str | None]:
    payload = tool_json(
      "mass-propers", "show", "--calendar", "postconciliar", "--mass", key
    )
    forms = []
    for row in payload["appointed"]:
      form = row.get("form")
      if form not in forms:
        forms.append(form)
    return forms

  def test_territorial_alternatives_remain_separate_tagged_branches(self):
    branches = self.rubric_day("2026-01-04")["options"]
    self.assertEqual(
      [branch["option"] for branch in branches],
      ["epiphany-january-6", "epiphany-transferred-to-sunday"],
    )
    self.assertEqual(
      [branch["winner"]["key"] for branch in branches],
      ["second-sunday-after-nativity", "epiphany"],
    )
    self.assertTrue(all(branch["settled"] for branch in branches))
    self.assertTrue(all(not branch["choiceRequired"] for branch in branches))

  def test_optional_memorial_is_a_settled_choice_not_an_unresolved_day(self):
    branch = self.rubric_day("2026-09-12")["options"][0]
    self.assertTrue(branch["settled"])
    self.assertEqual(branch["unsettled"], [])
    self.assertIsNone(branch["winner"])
    self.assertTrue(branch["choiceRequired"])
    self.assertEqual(branch["choice"]["id"], "calendar-formulary")
    self.assertEqual(
      [row["key"] for row in branch["choice"]["among"]],
      ["most-holy-name-mary", "ot-23-saturday"],
    )
    self.assertEqual(
      [(row["key"], row["state"], row["choice"]) for row in branch["readable"]],
      [
        ("most-holy-name-mary", "option", "calendar-formulary"),
        ("ot-23-saturday", "option", "calendar-formulary"),
      ],
    )

  def test_calendar_selection_does_not_invent_one_nativity_form(self):
    branch = self.rubric_day("2026-12-25")["options"][0]
    self.assertEqual(branch["winner"]["key"], "nativity")
    self.assertIsNone(branch["winner"]["formulary"])
    self.assertEqual(
      self.proper_forms("nativity"),
      ["Vigil Mass", "Mass during the Night", "Mass at Dawn", "Mass during the Day"],
    )

  def test_plural_optional_memorials_keep_distinct_mass_identities(self):
    branch = self.rubric_day("2026-01-20")["options"][0]
    self.assertEqual(
      [row["key"] for row in branch["choice"]["among"]],
      ["saint-fabian-pope-martyr", "saint-sebastian-martyr", "ot-2-tuesday"],
    )
    self.assertEqual(self.proper_forms("saint-fabian-pope-martyr"), [None])
    self.assertEqual(self.proper_forms("saint-sebastian-martyr"), [None])


if __name__ == "__main__":
  unittest.main()
