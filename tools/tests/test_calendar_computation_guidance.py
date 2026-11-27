import datetime as dt
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _product_data import browser_data_root

ROOT = Path(__file__).resolve().parents[2]

LAST_THINGS_READERS = [
  (subject, provider, f"articles/faith/four-last-things-{number:02d}-{subject.lower()}")
  for provider in ("gpt", "claude", "gemini")
  for number, subject in enumerate(("Death", "Judgment", "Hell", "Heaven"), 1)
]


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
  starts = {23: None, 24: None, 25: 6, 26: 5, 27: 4, 28: 3}
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

  def test_p23_has_no_resumed_epiphany_slot(self):
    self.assertEqual(nominal_resumed_slots(23), {})

  def test_1962_reader_calendar_has_68_parents(self):
    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    parent_ids = re.findall(r"^\| (\d{2}) \| \*\*", landing, re.MULTILINE)
    self.assertEqual(sorted(parent_ids), [f"{n:02d}" for n in range(1, 69)])
    # Reader list presentation (roman-1962-propers.md, 2026-11-16 and
    # 2026-11-17): the after-Pentecost run ends at 68, and the resumed Sundays
    # follow in their own section, in numeric order.
    self.assertEqual(parent_ids, [f"{n:02d}" for n in range(1, 64)] + ["68", "64", "65", "66", "67"])
    self.assertIn("| 27 | **Mass of the Lord's Supper** | Planned | Planned |", landing)
    self.assertIn(
      "| 28 | **Solemn Liturgical Action of the Passion and Death of the Lord** "
      "| Planned | Planned |",
      landing,
    )
    self.assertIn("| 29 | **Easter Vigil** | Planned | Planned |", landing)

  def test_1962_list_presentation_has_one_owner(self):
    """The catalog, and the producer every reader list reads, agree."""
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader("list_presentation_producer", str(ROOT / "tools/mass-propers"))
    producer = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(producer)
    document = producer.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
    held = {mass["key"]: mass for _, mass in producer.masses_of(document)}
    registry = {key: mass.get("registry") for key, mass in held.items()}

    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    calendar = landing.split("## Sunday Propers Calendar", 1)[1].split("### Feasts Replacing a Sunday", 1)[0]
    main, resumed = calendar.split("### Resumed Sundays after the Epiphany\n", 1)
    marked = re.findall(r"^\| (\d{2}) \| \*\*[^*]+\*\* † \|", main, re.MULTILINE)
    self.assertEqual(sorted(marked),
                     sorted(registry[key] for key in producer.EASTER_DEPENDENT_SUNDAYS))
    self.assertEqual(re.findall(r"^\| (\d{2}) \| \*\*[^*]+\*\* ‡ \|", resumed, re.MULTILINE),
                     [registry[key] for key in producer.RESUMED_SUNDAYS])
    self.assertEqual(re.findall(r"^\| (\d{2}) \| ", resumed, re.MULTILINE),
                     [registry[key] for key in producer.RESUMED_SUNDAYS])
    self.assertEqual(landing.count("\n† "), 1)
    self.assertEqual(landing.count("\n‡ "), 1)
    self.assertIn("\n† " + producer.EASTER_DEPENDENCE_NOTE + "\n", main)
    self.assertTrue(resumed.rstrip().endswith("\n‡ " + producer.RESUMED_NOTE))

    # Presentation never rewrites the calendar: the resumed Masses keep their
    # season and are only displayed in their own list group.
    listings = producer.list_presentation(document)
    for key in producer.RESUMED_SUNDAYS:
      self.assertEqual(held[key]["season"], "after-pentecost")
      self.assertEqual(listings[key], {"note": producer.RESUMED_NOTE,
                                       "season": producer.RESUMED_LIST_SEASON})
    for key in producer.EASTER_DEPENDENT_SUNDAYS:
      self.assertEqual(listings[key], {"note": producer.EASTER_DEPENDENCE_NOTE})
    self.assertEqual(set(listings),
                     set(producer.EASTER_DEPENDENT_SUNDAYS) | set(producer.RESUMED_SUNDAYS))
    seasonal = [{"key": mass["key"]} for kind, mass in producer.masses_of(document)
                if kind == "seasonal"]
    ordered = [mass["key"] for mass in producer.list_order(seasonal)]
    self.assertEqual(ordered[ordered.index("epiphany-2"):ordered.index("septuagesima")], [
      "epiphany-2", "epiphany-3", "epiphany-4", "epiphany-5", "epiphany-6",
    ])
    self.assertEqual(ordered[-7:], [
      "pentecost-23", "christ-the-king", "last-sunday-after-pentecost",
      "resumed-epiphany-3", "resumed-epiphany-4", "resumed-epiphany-5", "resumed-epiphany-6",
    ])
    # A selection without the Last Sunday leaves the resumed Sundays in place.
    self.assertEqual([mass["key"] for mass in producer.list_order(
      [{"key": "resumed-epiphany-3"}, {"key": "pentecost-23"}])],
      ["resumed-epiphany-3", "pentecost-23"])

    # The resumed note describes the record; a record that stops matching it
    # is refused rather than described by guess.
    import copy
    changed = copy.deepcopy(document)
    for _, mass in producer.masses_of(changed):
      if mass["key"] == "resumed-epiphany-4":
        mass["propers"] = mass["propers"][:-1]
    with self.assertRaisesRegex(ValueError, "resumed-epiphany-4 no longer takes what RESUMED_NOTE says"):
      producer.list_presentation(changed)

  def test_1962_last_things_block_closes_the_after_pentecost_run(self):
    """The Four Last Things block (roman-1962-propers.md, Reader list
    presentation, 2026-11-17): beneath the Proper of Time table, not a row,
    marked § with its own note after the † note, linking each provider's four
    essays by subject. It owns none of them; library/faith.md does."""
    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    calendar = landing.split("## Sunday Propers Calendar", 1)[1].split("### Feasts Replacing a Sunday", 1)[0]
    main = calendar.split("### Resumed Sundays after the Epiphany\n", 1)[0]
    last_row = re.findall(r"^\| \d{2} \|.*$", main, re.MULTILINE)[-1]
    self.assertTrue(last_row.startswith("| 68 | "))
    block, dagger, note = main.split(last_row + "\n", 1)[1].strip().split("\n\n")
    self.assertTrue(dagger.startswith("† "))
    self.assertTrue(note.startswith("§ "))
    self.assertEqual(landing.count("§"), 2)
    self.assertEqual(landing.count("\n§ "), 1)
    self.assertNotIn("](../pdf/", block)
    # The series names its home and takes the mark; each provider's four
    # essays stand on a line of their own.
    lead, chatgpt, claude, gemini = block.split("<br>\n")
    self.assertTrue(lead.endswith("\n[The Four Last Things](faith.md#the-four-last-things) §"), lead)
    self.assertTrue(chatgpt.startswith("ChatGPT: ") and "/claude/" not in chatgpt and "/gemini/" not in chatgpt)
    self.assertTrue(claude.startswith("Claude: ") and "/gpt/" not in claude and "/gemini/" not in claude)
    self.assertTrue(gemini.startswith("Gemini: ") and "/gpt/" not in gemini and "/claude/" not in gemini)

    linked = re.findall(r"\[([^\]]+)\]\(\.\./web/([a-z]+)/([^)]+)\.html\)", block)
    self.assertEqual(linked, LAST_THINGS_READERS)

    # The essays keep exactly one catalog home. The ownership check counts the
    # owner's legacy print links before reader links, so this block is not
    # counted as a home; were faith.md to keep only reader links for them, the
    # check would find two homes. This test fails first and names the rule.
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader("last_things_catalog", str(ROOT / "tools/public-alpha"))
    tool = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(tool)
    manifest = tool.load_manifest()
    primary, providers = tool.declared_providers(manifest)
    publications = tool.publication_map(manifest)
    occurrences = tool.catalog_occurrences(primary, providers, publications)[0]
    faith = (ROOT / "library/faith.md").read_text()
    for _, provider, leaf in LAST_THINGS_READERS:
      self.assertEqual(publications[(provider, leaf)]["catalog"], "library/faith.md")
      self.assertEqual(occurrences[(provider, leaf)], ["library/faith.md"],
                       f"{provider}:{leaf} must keep one catalog home; guidance/repository.md "
                       "§ Public navigation and catalog states when the 1962 block may link it")
      self.assertIn(f"](../web/{provider}/{leaf}.html)", faith)

  def test_1962_advent_handbook_cue_above_the_table(self):
    """The Sunday cue references each edition; the seasonal table owns it."""
    landing = (ROOT / "library/traditional-latin-mass.md").read_text()
    leaf = "liturgy/roman-rite/1962/seasons/advent"

    calendar = landing.split("## Sunday Propers Calendar", 1)[1].split("### Feasts Replacing a Sunday", 1)[0]
    main = calendar.split("### Resumed Sundays after the Epiphany\n", 1)[0]
    before_table, table_and_after = main.split("\n| ID | Sunday |", 1)
    cue = before_table.rstrip("\n").rsplit("\n", 1)[-1]
    self.assertTrue(cue.startswith("*Advent handbook*"))
    for provider, label, prefix in (("gpt", "ChatGPT", ""), ("claude", "Claude", "claude:")):
      self.assertIn(f"[{label}](../web/{provider}/{leaf}.html)", cue)
      marker = f"<!-- triptych-publication-reference: {prefix}{leaf} -->"
      self.assertIn(marker, cue)
      self.assertEqual(landing.count(marker), 1)
    self.assertTrue(table_and_after.split("\n", 3)[2].startswith("| 01 | **First Sunday of Advent**"))
    # The row that owns the handbook: Seasonal Handbooks, after the core works
    # and before the Sunday table, with no two-digit ID cell.
    self.assertIn('<a id="seasonal-primers"></a>', landing)
    handbooks = landing.split("## Seasonal Handbooks", 1)[1].split("\n## ", 1)[0]
    self.assertLess(landing.index("## Core and Reference Works"), landing.index("## Seasonal Handbooks"))
    self.assertLess(landing.index("## Seasonal Handbooks"), landing.index("## Sunday Propers Calendar"))
    self.assertNotRegex(handbooks, r"\b20\d\d\b")
    rows = [line for line in handbooks.splitlines() if line.startswith("| **")]
    self.assertEqual([row.split("**")[1] for row in rows], [
      "Advent", "Christmas", "Epiphany", "Time after Epiphany", "Septuagesima",
      "Lent", "Passiontide", "Easter", "Ascensiontide", "Octave of Pentecost",
      "Time after Pentecost",
    ])
    for provider in ("gpt", "claude"):
      self.assertIn(f"](../web/{provider}/{leaf}.html)", rows[0])
    self.assertIn("[Seasonal handbooks](#seasonal-handbooks)", landing.split("## Core and Reference Works", 1)[0])

    # One owner: the Seasonal Handbooks row, not the cue line.
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader("advent_handbook_catalog", str(ROOT / "tools/public-alpha"))
    tool = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(tool)
    manifest = tool.load_manifest()
    primary, providers = tool.declared_providers(manifest)
    publications = tool.publication_map(manifest)
    occurrences = tool.catalog_occurrences(primary, providers, publications)[0]
    for provider in ("gpt", "claude"):
      self.assertEqual(publications[(provider, leaf)]["catalog"], "library/traditional-latin-mass.md")
      self.assertEqual(occurrences[(provider, leaf)], ["library/traditional-latin-mass.md"])

  def test_postconciliar_seasonal_handbooks(self):
    landing = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    section = landing.split("## Seasonal Handbooks", 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| **")]
    self.assertEqual([row.split("**")[1] for row in rows], [
      "Advent", "Christmas Time", "Ordinary Time", "Lent", "Sacred Paschal Triduum", "Easter Time",
    ])
    self.assertIn("after Pentecost", rows[2])
    self.assertNotRegex(re.sub(r"\]\([^)]+\)", "]", section), r"\b20\d\d\b")
    leaf = "liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/seasons/advent"
    self.assertIn(f"](../web/gpt/{leaf}.html)", rows[0])
    self.assertIn("[Seasonal handbooks](#seasonal-handbooks)", landing.split("## Core", 1)[0])

  def test_postconciliar_registry_and_reader_calendar_arithmetic(self):
    registry = (
      ROOT / "guidance/liturgy/postconciliar-propers-registry.md"
    ).read_text()
    landing = (ROOT / "library/novus-ordo-liturgy.md").read_text()
    parents = re.findall(
      r"^\| (PC-S\d{2}) \| `[^`]+` \| [^|]+ \|$", registry, re.MULTILINE
    )
    rows = re.findall(
      r"^\| \*\*(.+?)\*\* \| ([ABC](?:, [ABC])*) \|.*\|.*\|$",
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
    # 59fe23257 separated provider columns and split published cycles into
    # their own rows; the 60 parents plus three Triduum entries are unchanged.
    cycles_by_title = {}
    for title, cycles in rows:
      cycles_by_title.setdefault(title, []).extend(cycles.split(", "))
    self.assertEqual(len(cycles_by_title), 63)
    for title, cycles in cycles_by_title.items():
      self.assertCountEqual(cycles, ["A", "B", "C"], title)
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
      "| **Evening Mass of the Lord's Supper** | A, B, C | Planned | Planned |",
      calendar,
    )
    self.assertIn(
      "| **Celebration of the Lord's Passion** | A, B, C | Planned | Planned |",
      calendar,
    )
    self.assertIn(
      "| **Easter Vigil** | A, B, C | Planned with Easter Sunday | "
      "Planned with Easter Sunday |",
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
      "| **Nativity of the Lord** | A, B, C | Planned | Planned |",
      landing,
    )
    self.assertNotRegex(landing, r"\b\d+ planned\b")
    self.assertIn(
      "| PC-R08 | **Commemoration of All the Faithful Departed** | "
      "A, B, C | Unresolved | Unresolved |",
      landing,
    )

  def test_sunday_catalog_links_only_installed_publications(self):
    # Keep the installed full-guide families aligned with the publication source
    # inventories and accepted catalogue installations. The inventories own the
    # source records; generated PDFs are not publication inputs.
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
        (49, "ninth-after-pentecost"),
        (50, "tenth-after-pentecost"),
        (51, "eleventh-after-pentecost"),
        (52, "twelfth-after-pentecost"),
        (53, "thirteenth-after-pentecost"),
        (54, "fourteenth-after-pentecost"),
        (55, "fifteenth-after-pentecost"),
        (56, "sixteenth-after-pentecost"),
        (57, "seventeenth-after-pentecost"),
        (58, "eighteenth-after-pentecost"),
        (59, "nineteenth-after-pentecost"),
        (60, "twentieth-after-pentecost"),
        (61, "twenty-first-after-pentecost"),
      )),
      "57-seventeenth-after-pentecost-homily.pdf",
      "58-eighteenth-after-pentecost-homily.pdf",
      "59-nineteenth-after-pentecost-homily.pdf",
      "60-twentieth-after-pentecost-homily.pdf",
      "61-twenty-first-after-pentecost-homily.pdf",
      "f01-christ-the-king.pdf",
      "f01-christ-the-king-homily.pdf",
      # This exact source owner and its installed three-edition catalogue are
      # checked below; a Planned peer column is not a missing GPT publication.
      "f02-all-saints.pdf",
      "f02-all-saints-homily.pdf",
      "pc-r07-all-saints-abc.pdf",
      "pc-r07-all-saints-abc-homily.pdf",
      *(f"pc-s{number}-{slug}-year-a.pdf" for number, slug in (
        (37, "eleventh-sunday-in-ordinary-time"),
        (38, "twelfth-sunday-in-ordinary-time"),
        (39, "thirteenth-sunday-in-ordinary-time"),
        (40, "fourteenth-sunday-in-ordinary-time"),
        (41, "fifteenth-sunday-in-ordinary-time"),
        (42, "sixteenth-sunday-in-ordinary-time"),
        (43, "seventeenth-sunday-in-ordinary-time"),
        (26, "most-holy-trinity"),
        (27, "most-holy-body-and-blood-of-christ"),
        (51, "twenty-fifth-sunday-in-ordinary-time"),
        (52, "twenty-sixth-sunday-in-ordinary-time"),
        (53, "twenty-seventh-sunday-in-ordinary-time"),
        (54, "twenty-eighth-sunday-in-ordinary-time"),
        (55, "twenty-ninth-sunday-in-ordinary-time"),
      )),
      "pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a-homily.pdf",
      "pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a-homily.pdf",
      "pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a-homily.pdf",
      "pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a-homily.pdf",
      "pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a-homily.pdf",
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf",
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf",
      "pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf",
    }
    corpus = json.loads((browser_data_root(ROOT) / 'structure/documents/corpus.json').read_text())
    installed_readers = {}
    for work in corpus["works"]:
      for edition in work["editions"]:
        source = ROOT / edition["title_source"]
        for issue in (edition, *edition.get("also", [])):
          if issue["available"]["reader"]:
            kind = issue.get("kind")
            entrypoint = source.with_name(kind + ".tex") if kind in (
              "synthesis", "homily") else source
            installed_readers[issue["targets"]["reader"]] = (entrypoint, work["catalog"])
    for owner, catalog in (
        ("liturgy/roman-rite/1962/propers/temporal/f02-all-saints", "library/traditional-latin-mass.md"),
        ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
         "propers/general-calendar/pc-r07-all-saints-abc", "library/novus-ordo-liturgy.md"),
    ):
      works = [work for work in corpus["works"] if work["leaf"] == owner]
      self.assertEqual(len(works), 1)
      self.assertEqual(works[0]["catalog"], catalog)
      editions = [edition for edition in works[0]["editions"] if edition["provider"] == "gpt"]
      self.assertEqual(len(editions), 1)
      edition = editions[0]
      self.assertEqual(edition["title_source"], "src/gpt/" + owner + "/main.tex")
      self.assertTrue((ROOT / edition["title_source"]).is_file())
      self.assertEqual(edition["status"], "alpha")
      issues = (edition, *edition["also"])
      paths = {issue["targets"]["reader"] for issue in issues}
      self.assertEqual(paths, {"web/gpt/" + owner + suffix + ".html"
                               for suffix in ("", "-synthesis", "-homily")})
      for issue in issues:
        self.assertTrue(issue["available"]["reader"])
        self.assertTrue(issue["available"]["print"])
        source, _ = installed_readers[issue["targets"]["reader"]]
        self.assertTrue(source.is_file())
    related_readers = {f"../web/{provider}/{leaf}.html"
                       for _, provider, leaf in LAST_THINGS_READERS}
    for name in ("traditional-latin-mass.md", "novus-ordo-liturgy.md"):
      text = (ROOT / "library" / name).read_text()
      calendar = text.split("## Sunday Propers Calendar", 1)[1]
      for target in re.findall(
          r"\]\((\.\./(?:pdf|web)/[^)]+\.(?:pdf|html))\)", calendar):
        if target.startswith("../pdf/") and "m01-nuptial-mass.pdf" not in target:
          self.assertTrue(
            target.endswith("-synthesis.pdf")
            or target.rsplit("/", 1)[-1] in permitted_full_guides,
            target,
          )
        reader = target.removeprefix("../")
        if reader.startswith("pdf/"):
          reader = "web/" + reader.removeprefix("pdf/").removesuffix(".pdf") + ".html"
        self.assertIn(reader, installed_readers, target)
        source, owner = installed_readers[reader]
        expected_owner = f"library/{name}"
        if name == "traditional-latin-mass.md" and target in related_readers:
          expected_owner = "library/faith.md"
        self.assertEqual(owner, expected_owner, target)
        self.assertTrue(source.is_file(), target)

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
