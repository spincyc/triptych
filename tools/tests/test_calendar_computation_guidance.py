import datetime as dt
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


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

  def test_1962_reader_calendar_has_52_parents_and_four_resumed_variants(self):
    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    parent_ids = re.findall(r"^\| (\d{2}) \| \*\*", landing, re.MULTILINE)
    resumed_ids = re.findall(r"^\| (4[6-9]R) \| \*\*", landing, re.MULTILINE)
    self.assertEqual(parent_ids, [f"{n:02d}" for n in range(1, 53)])
    self.assertEqual(resumed_ids, ["46R", "47R", "48R", "49R"])
    self.assertIn("| **Mass of the Lord's Supper** | Planned | Planned |", landing)
    self.assertIn(
      "| **Solemn Liturgical Action of the Passion and Death of the Lord** "
      "| Planned | Planned |",
      landing,
    )
    self.assertIn("| **Easter Vigil** | Planned | Planned |", landing)

  def test_postconciliar_registry_and_reader_calendar_arithmetic(self):
    registry = (
      ROOT / "guidance/liturgy/postconciliar-propers-registry.md"
    ).read_text()
    landing = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    parents = re.findall(
      r"^\| (PC-S\d{2}) \| `[^`]+` \| [^|]+ \|$", registry, re.MULTILINE
    )
    rows = re.findall(r"^\| \*\*(PC-S\d{2}) ·", landing, re.MULTILINE)
    s42_reader_row = re.findall(
      r"^\| \*\*Eighteenth Sunday in Ordinary Time\*\* \|.*$",
      landing,
      re.MULTILINE,
    )
    self.assertEqual(len(s42_reader_row), 1)
    rows.append("PC-S42")
    rows.sort(key=lambda value: int(value.removeprefix("PC-S")))
    counts = [
      int(value)
      for value in re.findall(
        r"^\| PC-S\d{2} \| `[^`]+`(?:, `[^`]+`)* \| [^|]+ \| (\d+) \|$",
        registry,
        re.MULTILINE,
      )
    ]
    self.assertEqual(parents, [f"PC-S{n:02d}" for n in range(1, 61)])
    self.assertEqual(rows, parents)
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
    triduum = landing.split("### Sacred Triduum", 1)[1].split(
      "### Sunday replacements", 1
    )[0]
    self.assertIn("| Celebration | Status |", triduum)
    self.assertIn(
      "| **Evening Mass of the Lord's Supper** | Planned |", triduum
    )
    self.assertIn(
      "| **Celebration of the Lord's Passion** | Planned |", triduum
    )
    self.assertIn(
      "| **Easter Vigil** | Planned with Easter Sunday |", triduum
    )
    self.assertIn("one cycle-invariant plan", triduum)
    self.assertIn("rather than counted as another planned work", triduum)
    self.assertNotRegex(triduum, r"\|\s*A\s*\|\s*B\s*\|\s*C\s*\|")
    self.assertNotRegex(triduum, r"\bPC-[A-Z0-9-]+\b")
    # The production plan no longer restates the registry's counts, so there
    # is no totals table to assert on; the registry above is the one source.
    self.assertIn(
      "| **PC-S05 · Nativity of the Lord** | Planned | Planned | Planned |",
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
        (15, "trinity-sunday"),
        (16, "second-after-pentecost"),
        (17, "third-after-pentecost"),
        (18, "fourth-after-pentecost"),
        (19, "fifth-after-pentecost"),
        (20, "sixth-after-pentecost"),
        (21, "seventh-after-pentecost"),
        (22, "eighth-after-pentecost"),
        (24, "tenth-after-pentecost"),
      )),
      *(f"pc-s{number}-{slug}-year-a.pdf" for number, slug in (
        (35, "eleventh-sunday-in-ordinary-time"),
        (36, "twelfth-sunday-in-ordinary-time"),
        (37, "thirteenth-sunday-in-ordinary-time"),
        (38, "fourteenth-sunday-in-ordinary-time"),
        (39, "fifteenth-sunday-in-ordinary-time"),
        (40, "sixteenth-sunday-in-ordinary-time"),
        (58, "most-holy-trinity"),
        (59, "most-holy-body-and-blood-of-christ"),
      )),
      "pc-s42-eighteenth-sunday-in-ordinary-time-year-a.pdf",
      "pc-s42-eighteenth-sunday-in-ordinary-time-year-b.pdf",
      "pc-s42-eighteenth-sunday-in-ordinary-time-year-c.pdf",
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
    for proper_id in range(15, 23):
      row = re.search(rf"^\| {proper_id} \|.*$", traditional, re.MULTILINE)
      self.assertIsNotNone(row)
      self.assertIn("../pdf/gpt/", row.group())
      if proper_id == 22:
        self.assertIn("../pdf/claude/", row.group())
        self.assertIn("../web/claude/", row.group())
      else:
        self.assertTrue(row.group().endswith("| Planned |"))
    self.assertIn("| 14 | **Pentecost Sunday** | Planned | Planned |", traditional)

    postconciliar = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    for proper_id in (35, 36, 37, 38, 39, 40, 58, 59):
      row = re.search(
        rf"^\| \*\*PC-S{proper_id} ·.*$", postconciliar, re.MULTILINE
      )
      self.assertIsNotNone(row)
      self.assertIn("../pdf/gpt/", row.group())
      if proper_id == 40:
        self.assertIn("../pdf/claude/", row.group())


if __name__ == "__main__":
  unittest.main()
