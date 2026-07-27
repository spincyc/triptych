import datetime as dt
import unittest


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


if __name__ == "__main__":
  unittest.main()
