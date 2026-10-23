"""Seven exact maps, nine raw/resolved Gospel owners; chapter remains closed."""
from __future__ import annotations
import copy
import hashlib
import unittest
if __package__:
    from .test_postconciliar_easter_ferials import context, ROOT, KEYS
else:
    from test_postconciliar_easter_ferials import context, ROOT, KEYS

MAPS = {f"John 6:{source}": f"John 6:{target}" for source, target in (
    ("1-15", "1-15"), ("16-21", "16-21"), ("22-29", "22-29"), ("30-35", "30-35"),
    ("35-40", "35-40"), ("52-59", "53-60"), ("60-69", "61-70"))}
EXPECTED = {
    ("easter-2-friday", "main", "Gospel", 1, "", "all", "John 6:1-15"),
    ("easter-2-saturday", "main", "Gospel", 1, "", "all", "John 6:16-21"),
    ("easter-3-monday", "main", "Gospel", 1, "", "all", "John 6:22-29"),
    ("easter-3-tuesday", "main", "Gospel", 1, "", "all", "John 6:30-35"),
    ("easter-3-wednesday", "main", "Gospel", 1, "", "all", "John 6:35-40"),
    ("easter-3-friday", "main", "Gospel", 1, "", "all", "John 6:52-59"),
    ("easter-3-saturday", "main", "Gospel", 1, "", "all", "John 6:60-69"),
    ("ot-17", "main", "Gospel", 1, "cycles", "B", "John 6:1-15"),
    ("ot-21", "main", "Gospel", 1, "cycles", "B", "John 6:60-69"),
}


class EasterExactNumberingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc, cls.masses, cls.mp, cls.index, cls.canon, cls.tables, cls.public = context()

    def test_exact_seven_maps_leave_vulgate_and_chapter_stance(self):
        row = next(r for r in self.doc["citation_divergences"] if r["book"] == "John")
        self.assertEqual(row["numbering"], {"hebrew": "unrecorded"})
        for ref, vulgate in MAPS.items():
            self.assertEqual(row["citations"][ref], {"vulgate": vulgate, "hebrew": ref})
            parsed = self.canon.parse_citation(ref)
            for system, target in (("vulgate", vulgate), ("hebrew", ref)):
                ranges, error = self.tables[system].apply(parsed, parsed["ranges"])
                self.assertFalse(error)
                self.assertEqual(ranges, self.canon.parse_citation(target)["ranges"])
        self.assertEqual(row["citations"]["John 6:44-51"], "John 6:44-52")
        for target in row["citations"].values():
            if isinstance(target, dict):
                self.assertNotIn("hebrew-unnumbered-titles", target)

    def test_all_raw_and_resolved_consumers_are_the_exact_nine(self):
        for resolved in (False, True):
            found = set()
            for _, mass in self.mp.masses_of(self.doc):
                entries = (self.mp.appointed_propers(self.doc, mass) if resolved else
                           [(form, p, None) for form, p in self.mp.propers_of(mass)])
                for form, proper, taken in entries:
                    if proper["name"] != "Gospel":
                        continue
                    for family, cycle, owner in [("", "all", proper), *self.mp.cycle_owners(proper)]:
                        for entry in owner.get("verses", []):
                            if entry["ref"] in MAPS:
                                identity = self.mp.source_slot_identity(self.doc, mass, form, proper, taken)
                                found.add((*identity, family, cycle, entry["ref"]))
            self.assertEqual(found, EXPECTED)
        found = set()
        for mass in self.public["masses"]:
            for proper in mass["propers"]:
                for cycle, owner in [("all", proper), *((c, p) for c, p in proper.get("cycles", {}).items())]:
                    for entry in owner.get("citations", []):
                        if entry["ref"] not in MAPS:
                            continue
                        self.assertEqual(proper["name"], "Gospel")
                        found.add((mass["key"], cycle, entry["ref"]))
                        for system, ref in (("vulgate", MAPS[entry["ref"]]), ("hebrew", entry["ref"]),
                                            ("hebrew-unnumbered-titles", entry["ref"])):
                            parsed = self.canon.parse_citation(ref)
                            self.assertEqual(entry["loci"][system], [l for span in parsed["ranges"]
                                for l in self.mp.range_to_loci(span["begin"], span["end"])])
        self.assertEqual(found, {(r[0], r[5], r[6]) for r in EXPECTED})

    def test_all_seven_bibles_resolve_each_of_the_nine_exact_addresses(self):
        for edition, config in self.index.EDITIONS.items():
            if edition not in {"douay-rheims", "douay-rheims-american-1899", "clementine-vulgate",
                              "king-james-version", "world-english-bible-catholic",
                              "revised-version-1895", "catholic-public-domain-version"}:
                continue
            bible = self.index.Bible(ROOT / "src/sources/works" / config["artifacts"])
            for owner in EXPECTED:
                ref = owner[-1]; parsed = self.canon.parse_citation(ref)
                ranges, error = self.tables[config["numbering"]].apply(parsed, parsed["ranges"])
                self.assertFalse(error, (edition, owner))
                body, error = bible.passage("John", ranges)
                self.assertFalse(error, (edition, owner))
                self.assertTrue(body)
                target = MAPS[ref] if config["numbering"] == "vulgate" else ref
                self.assertEqual(ranges, self.canon.parse_citation(target)["ranges"])

    def test_n276_and_three_psalm_and_cpdv_and_acts837_refusals_remain(self):
        for ref in ("John 6:44-51", "John 6:51", "John 6:51-52", "John 6:57",
                    "John 6:58", "John 6:61", "John 6:63c, 68c"):
            entry = self.canon.parse_citation(ref)
            ranges, error = self.tables["hebrew"].apply(entry, entry["ranges"])
            self.assertEqual(ranges, [])
            self.assertIn("unrecorded", error)
        projected = {m["key"]: m for m in self.public["masses"]}
        refusals = []
        for key in KEYS:
            for proper in projected[key]["propers"]:
                if proper["name"] in ("First Reading", "Responsorial Psalm", "Gospel"):
                    for entry in proper["citations"]:
                        if entry.get("refused", {}).get("hebrew-unnumbered-titles"):
                            refusals.append((key, proper["name"]))
        self.assertEqual(set(refusals), {("easter-2-monday", "Responsorial Psalm"),
            ("easter-3-thursday", "Gospel"), ("easter-4-monday", "Responsorial Psalm"),
            ("easter-4-friday", "Responsorial Psalm")})
        for edition in ("world-english-bible-catholic", "revised-version-1895"):
            config = self.index.EDITIONS[edition]
            bible = self.index.Bible(ROOT / "src/sources/works" / config["artifacts"])
            body, problem = bible.passage(bible.token("Acts"), self.canon.parse_citation("Acts 8:26-40")["ranges"])
            self.assertFalse(body)
            self.assertIn("37", problem)
        config = self.index.EDITIONS["catholic-public-domain-version"]
        bible = self.index.Bible(ROOT / "src/sources/works" / config["artifacts"])
        body, problem = bible.passage(bible.token("Psalms"), self.canon.parse_citation("Psalm 92:1-2, 5")["ranges"])
        self.assertFalse(body)
        self.assertTrue(problem)

    def test_source_primaries_and_old_map_source_fail_control(self):
        files = {
            "catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts/verse-text-50-john-1542486b/50-john.tsv":
                "1542486b92076807c978539845d189be3a28cd8f288eaad0f90a3da4ec1e8016",
            "robinson-pierpont/greek-new-testament-byzantine-textform/editions/rp2018-byztxt-unicode-csv/artifacts/ccat-csv-joh-1e4f4305/JOH.csv":
                "1e4f430576b7e14daeda93e8c53c551358048cb5587f06e6807ab164b95728ee",
        }
        for path, digest in files.items():
            self.assertEqual(hashlib.sha256((ROOT / "src/sources/works" / path).read_bytes()).hexdigest(), digest)
        old = copy.deepcopy(self.doc)
        for row in old["citation_divergences"]:
            if row["book"] == "John":
                for ref, target in MAPS.items():
                    row["citations"][ref] = target
        entries = [e for _, mass in self.mp.masses_of(old)
                   for e, _ in self.mp.numbered_entries(mass, old["psalm_numbering"])]
        table = self.mp.Divergences("postconciliar", old, entries, self.canon, "hebrew",
            numberings=tuple(n for n in self.mp.SYSTEMS if n != self.mp.RESOLVED_IN))
        for ref in MAPS:
            entry = self.canon.parse_citation(ref)
            self.assertIn("unrecorded", table.apply(entry, entry["ranges"])[1])


if __name__ == "__main__":
    unittest.main()
