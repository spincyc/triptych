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

  def test_postconciliar_registry_and_reader_calendar_arithmetic(self):
    registry = (
      ROOT / "guidance/liturgy/postconciliar-propers-registry.md"
    ).read_text()
    landing = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    parents = re.findall(
      r"^\| (PC-S\d{2}) \| `[^`]+` \| [^|]+ \|$", registry, re.MULTILINE
    )
    rows = re.findall(r"^\| \*\*(PC-S\d{2}) ·", landing, re.MULTILINE)
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
      "| **PC-S05 · Nativity of the Lord** | 4 planned | 4 planned | 4 planned |",
      landing,
    )
    self.assertIn(
      "| PC-R08 | **Commemoration of All the Faithful Departed** | "
      "Unresolved | Unresolved | Unresolved |",
      landing,
    )

  def test_sunday_catalog_links_only_installed_syntheses(self):
    for name in ("traditional-latin-mass.md", "novus-ordo-liturgy.md"):
      text = (ROOT / "library" / name).read_text()
      calendar = text.split("## Sunday Propers Calendar", 1)[1]
      for target in re.findall(r"\]\((\.\./doc/[^)]+\.pdf)\)", calendar):
        if "m01-nuptial-mass.pdf" not in target:
          self.assertTrue(target.endswith("-synthesis.pdf"), target)
        self.assertTrue((ROOT / "library" / target).resolve().exists(), target)


if __name__ == "__main__":
  unittest.main()
