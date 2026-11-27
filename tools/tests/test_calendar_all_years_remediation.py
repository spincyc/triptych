"""Comprehensive regression tests for all-years calendar & rubrics remediation
(Roman 1962 TLM & Postconciliar).

Exercises tools/calendar-days, tools/calendar-rubrics, and
src/web/browser/liturgy/assembly-model.js directly in memory across historical
and future edge years (1818, 1940, 1962, 2008, 2011, 2022, 2024, 2025, 2027,
2028, 2029, 2033, 2035, 2038, 2044, 2046, 2057, 2062, 2095) without depending
on the sealed cache's year bounds.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALENDARS_ROOT = ROOT / "src" / "sources" / "calendars"
MODEL_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "assembly-model.js"
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))


def _load_tool(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    loader.exec_module(mod)
    return mod


NODE_BATCH_SCRIPT = r"""
const model = require(process.argv[1]);
const fs = require('fs');
const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = {};
for (const q of payload.queries) {
  const rubrics = payload.rubrics[q.calendar];
  const year = payload.years[q.calendar][String(q.year)];
  out[q.id] = model.derive({ date: q.date, year, rubrics });
}
process.stdout.write(JSON.stringify(out));
"""


class AllYearsRemediationTests(unittest.TestCase):
    """End-to-end verification of all 8 remediated calendar & rubrics defects."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.cd = _load_tool("calendar_days_remediation_test", ROOT / "tools" / "calendar-days")
        cls.cr = _load_tool("calendar_rubrics_remediation_test", ROOT / "tools" / "calendar-rubrics")

        cls.rubrics: dict[str, dict] = {}
        cls.indices: dict[str, dict] = {}
        cls.year_cache: dict[str, dict[int, dict]] = {}
        for cal in ("roman-1962", "postconciliar", "roman-pre-1955"):
            built_rubrics, problems, _ = cls.cr.build(CALENDARS_ROOT, cal)
            if problems:
                raise AssertionError(f"{cal} rubrics build failed: {problems}")
            cls.rubrics[cal] = built_rubrics[0]
            cls.indices[cal] = cls.cd.load_calendar(CALENDARS_ROOT, cal)
            cls.year_cache[cal] = {}

    @classmethod
    def _ensure_years(cls, calendar: str, years: set[int]) -> None:
        missing = sorted(years - set(cls.year_cache[calendar]))
        if not missing:
            return
        index = dict(cls.indices[calendar])
        index["fixed"] = {y: cls.cd.fixed_dates(index, y) for y in missing}
        needed_endings = sorted({y for y in missing} | {y + 1 for y in missing})
        built = cls.cd.build_years(index, needed_endings)
        for y in missing:
            cls.year_cache[calendar][y] = cls.cd.year_document(index, y, built)

    @classmethod
    def derive_batch(cls, queries: list[tuple[str, str, str]]) -> dict[str, dict]:
        """Run [(id, calendar, iso_date), ...] in a single Node process."""
        by_cal_years: dict[str, set[int]] = {}
        payload_queries = []
        for qid, cal, iso_date in queries:
            y = int(iso_date[:4])
            by_cal_years.setdefault(cal, set()).add(y)
            payload_queries.append({"id": qid, "calendar": cal, "date": iso_date, "year": y})
        for cal, ys in by_cal_years.items():
            cls._ensure_years(cal, ys)
        payload = {
            "rubrics": {cal: cls.rubrics[cal] for cal in by_cal_years},
            "years": {
                cal: {str(y): cls.year_cache[cal][y] for y in ys}
                for cal, ys in by_cal_years.items()
            },
            "queries": payload_queries,
        }
        proc = subprocess.run(
            ["node", "-e", NODE_BATCH_SCRIPT, str(MODEL_JS)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(proc.stdout)

    @staticmethod
    def _branch(derived: dict, option: str | None = None) -> dict:
        for b in derived["options"]:
            if b["option"] == option:
                return b
        raise AssertionError(f"branch {option!r} not found in {[b['option'] for b in derived['options']]}")

    # ------------------------------------------------------------------ Roman 1962

    def test_1962_bissextile_shift_leap_and_common_years(self) -> None:
        res = self.derive_batch([
            ("2028-24", "roman-1962", "2028-02-24"),
            ("2028-25", "roman-1962", "2028-02-25"),
            ("2028-27", "roman-1962", "2028-02-27"),
            ("2028-28", "roman-1962", "2028-02-28"),
            ("2024-24", "roman-1962", "2024-02-24"),
            ("2024-25", "roman-1962", "2024-02-25"),
            ("2027-24", "roman-1962", "2027-02-24"),
            ("2027-25", "roman-1962", "2027-02-25"),
            ("2027-27", "roman-1962", "2027-02-27"),
            ("2027-28", "roman-1962", "2027-02-28"),
        ])
        # Leap year 2028: Matthias 02-24 -> 02-25; Gabriel 02-27 -> 02-28
        b28_24 = self._branch(res["2028-24"])
        self.assertEqual(b28_24["winner"]["id"], "implied:septuagesima-feria")
        self.assertNotIn("s-matthiae-apostoli", [c["key"] for c in b28_24["candidates"]])
        b28_25 = self._branch(res["2028-25"])
        self.assertEqual(b28_25["winner"]["id"], "s-matthiae-apostoli")
        b28_27 = self._branch(res["2028-27"])
        self.assertNotIn("s-gabrielis-a-virgine-perdolente-confessoris", [c["key"] for c in b28_27["candidates"]])
        b28_28 = self._branch(res["2028-28"])
        self.assertEqual(b28_28["winner"]["id"], "s-gabrielis-a-virgine-perdolente-confessoris")

        # Leap year 2024 (Lent): Feb 24 is Ember Saturday without Matthias; Feb 25 is Lent 2 Sunday with Matthias omitted
        b24_24 = self._branch(res["2024-24"])
        self.assertEqual(b24_24["winner"]["id"], "lent-1-ember-saturday")
        self.assertNotIn("s-matthiae-apostoli", [c["key"] for c in b24_24["candidates"]])
        b24_25 = self._branch(res["2024-25"])
        self.assertEqual(b24_25["winner"]["id"], "lent-2")
        self.assertIn("s-matthiae-apostoli", [c["key"] for c in b24_25["candidates"]])

        # Common year 2027: Matthias stays on 02-24; Gabriel stays on 02-27
        self.assertIn("s-matthiae-apostoli", [c["key"] for c in self._branch(res["2027-24"])["candidates"]])
        self.assertNotIn("s-matthiae-apostoli", [c["key"] for c in self._branch(res["2027-25"])["candidates"]])
        self.assertIn("s-gabrielis-a-virgine-perdolente-confessoris", [c["key"] for c in self._branch(res["2027-27"])["candidates"]])
        self.assertNotIn("s-gabrielis-a-virgine-perdolente-confessoris", [c["key"] for c in self._branch(res["2027-28"])["candidates"]])

    def test_1962_precious_blood_and_vigil_of_nativity_and_christmas_octave_on_sunday(self) -> None:
        res = self.derive_batch([
            ("pb-2029", "roman-1962", "2029-07-01"),
            ("vn-2028", "roman-1962", "2028-12-24"),
            ("oct-2024", "roman-1962", "2024-12-29"),
            ("oct-2029", "roman-1962", "2029-12-30"),
            ("oct-2028", "roman-1962", "2028-12-31"),
        ])
        # RG 112 b: Precious Blood (Class I Feast of the Lord) omits Sunday commemoration
        pb = self._branch(res["pb-2029"])
        self.assertTrue(pb["settled"])
        self.assertEqual(pb["winner"]["id"], "pretiosissimi-sanguinis-domini-nostri-iesu-christi")
        self.assertEqual(len(pb["orations"]["low_mass"]), 1)
        self.assertEqual(len(pb["orations"]["sung_non_conventual"]), 1)
        self.assertEqual([l["disposition"] for l in pb["losers"] if l["id"] == "pentecost-6"], ["omitted"])

        # RG 112 c + Missal p. 15: Vigil of Nativity on Sunday omits Advent 4
        vn = self._branch(res["vn-2028"])
        self.assertTrue(vn["settled"])
        self.assertEqual(vn["winner"]["id"], "vigil-nativity-lord")
        self.assertEqual(len(vn["orations"]["low_mass"]), 1)
        self.assertEqual(len(vn["orations"]["sung_non_conventual"]), 1)
        adv4 = [l for l in vn["losers"] if l["id"] == "advent-4"]
        self.assertEqual(len(adv4), 1)
        self.assertEqual(adv4[0]["disposition"], "omitted")
        self.assertEqual(adv4[0]["locus"], "RG 112 c")

        # RG 112 c + Missal p. 22 ("non vero octavae"): Sunday within Christmas Octave omits Octave day
        for qid, oct_key in (("oct-2024", "fifth-day-within-octave"), ("oct-2029", "sixth-day-within-octave"), ("oct-2028", "seventh-day-within-octave")):
            b = self._branch(res[qid])
            self.assertTrue(b["settled"])
            self.assertEqual(b["winner"]["id"], "sunday-within-octave-of-nativity")
            oct_loser = [l for l in b["losers"] if l["id"] == oct_key]
            self.assertEqual(len(oct_loser), 1)
            self.assertEqual(oct_loser[0]["disposition"], "omitted")
            self.assertEqual(oct_loser[0]["locus"], "RG 112 c")

    def test_1962_rg33_vigil_omitted_when_feast_transferred_or_commemorated(self) -> None:
        res = self.derive_batch([
            ("jb-2038", "roman-1962", "2038-06-23"),
            ("jb-2033", "roman-1962", "2033-06-23"),
            ("pp-1962", "roman-1962", "1962-06-28"),
            ("pp-2057", "roman-1962", "2057-06-28"),
            ("law-2025", "roman-1962", "2025-08-09"),
            ("law-2027", "roman-1962", "2027-08-09"),
        ])
        for qid, vigil_key in (
            ("jb-2038", "vigil-nativity-saint-john-baptist"),
            ("jb-2033", "vigil-nativity-saint-john-baptist"),
            ("pp-1962", "vigil-saints-peter-paul"),
            ("pp-2057", "vigil-saints-peter-paul"),
        ):
            b = self._branch(res[qid])
            self.assertTrue(b["settled"], qid)
            self.assertEqual(b["winner"]["id"], "implied:after-pentecost-feria", qid)
            self.assertEqual(b["winner"]["row"], 28, qid)
            v = [l for l in b["losers"] if l["id"] == vigil_key]
            self.assertEqual(len(v), 1, qid)
            self.assertEqual(v[0]["disposition"], "omitted", qid)
            self.assertEqual(v[0]["locus"], "RG 33", qid)

        # 2025-08-09: St Lawrence reduced to comm. on Sun Aug 10 -> Vigil omitted -> Our Lady on Saturday + comm St Romanus
        law25 = self._branch(res["law-2025"])
        self.assertTrue(law25["settled"])
        self.assertEqual(law25["winner"]["row"], 27)
        self.assertEqual(law25["winner"]["formulary"]["key"], "missa-de-s-maria-in-sabbato-5")
        self.assertEqual([l["id"] for l in law25["losers"] if l["disposition"] == "commemorated"], ["comm-s-romani-martyris"])
        self.assertEqual([l["disposition"] for l in law25["losers"] if l["id"] == "vigil-saint-lawrence"], ["omitted"])

        # Control: 2027-08-09 (Mon; Aug 10 is Tue, St Lawrence celebrated) -> Vigil of St Lawrence IS celebrated!
        law27 = self._branch(res["law-2027"])
        self.assertEqual(law27["winner"]["id"], "vigil-saint-lawrence")

    def test_1962_rg96_general_transfer_arrivals(self) -> None:
        res = self.derive_batch([
            # St Joseph on Lent 3 Sunday -> Mon Mar 20
            ("sj-2028-src", "roman-1962", "2028-03-19"),
            ("sj-2028-dst", "roman-1962", "2028-03-20"),
            # Easter Mar 25 (2035): Annunciation -> Mon Apr 2 (RG 96 a); St Joseph -> Tue Apr 3 (RG 96)
            ("sj-2035-src", "roman-1962", "2035-03-19"),
            ("an-2035-dst", "roman-1962", "2035-04-02"),
            ("sj-2035-dst", "roman-1962", "2035-04-03"),
            # Annunciation on Lent 3 Sunday (2029: Easter Apr 1 -> Mar 25 Palm Sunday; 2057: Easter Apr 22 -> Mar 25 Lent 3 Sun)
            ("an-2057-src", "roman-1962", "2057-03-25"),
            ("an-2057-dst", "roman-1962", "2057-03-26"),
            # St Joseph the Worker on Ascension Thu (2008-05-01) -> Fri 2008-05-02
            ("sjw-2008-src", "roman-1962", "2008-05-01"),
            ("sjw-2008-dst", "roman-1962", "2008-05-02"),
            # St Joseph the Worker on Low Sunday (2095-05-01) -> Mon 2095-05-02
            ("sjw-2095-src", "roman-1962", "2095-05-01"),
            ("sjw-2095-dst", "roman-1962", "2095-05-02"),
            # St John Baptist on Corpus Christi (2038-06-24) -> Fri 2038-06-25
            ("jb-2038-src", "roman-1962", "2038-06-24"),
            ("jb-2038-dst", "roman-1962", "2038-06-25"),
            # Ss Peter & Paul on Sacred Heart (1962-06-29, 2057-06-29) -> Sat Jun 30
            ("pp-1962-src", "roman-1962", "1962-06-29"),
            ("pp-1962-dst", "roman-1962", "1962-06-30"),
            ("pp-2057-src", "roman-1962", "2057-06-29"),
            ("pp-2057-dst", "roman-1962", "2057-06-30"),
            # Precious Blood on Sacred Heart (2011-07-01, 2095-07-01) -> skips Jul 2 (Visitation II) & Jul 3 (Sun II) -> Mon Jul 4
            ("pb-2011-src", "roman-1962", "2011-07-01"),
            ("pb-2011-dst", "roman-1962", "2011-07-04"),
            ("pb-2095-src", "roman-1962", "2095-07-01"),
            ("pb-2095-dst", "roman-1962", "2095-07-04"),
        ])

        pairs = [
            ("sj-2028-src", "sj-2028-dst", "s-ioseph-sponsi-beatae-mariae-virginis", "2028-03-20"),
            ("sj-2035-src", "sj-2035-dst", "s-ioseph-sponsi-beatae-mariae-virginis", "2035-04-03"),
            ("an-2057-src", "an-2057-dst", "annuntiatio-beatae-mariae-virginis", "2057-03-26"),
            ("sjw-2008-src", "sjw-2008-dst", "s-ioseph-opificis-sponsi-beatae-mariae", "2008-05-02"),
            ("sjw-2095-src", "sjw-2095-dst", "s-ioseph-opificis-sponsi-beatae-mariae", "2095-05-02"),
            ("jb-2038-src", "jb-2038-dst", "nativitate-s-ioannis-baptistae", "2038-06-25"),
            ("pp-1962-src", "pp-1962-dst", "ss-petri-pauli-apostolorum", "1962-06-30"),
            ("pp-2057-src", "pp-2057-dst", "ss-petri-pauli-apostolorum", "2057-06-30"),
            ("pb-2011-src", "pb-2011-dst", "pretiosissimi-sanguinis-domini-nostri-iesu-christi", "2011-07-04"),
            ("pb-2095-src", "pb-2095-dst", "pretiosissimi-sanguinis-domini-nostri-iesu-christi", "2095-07-04"),
        ]
        for src_id, dst_id, feast_key, expected_dest in pairs:
            sb = self._branch(res[src_id])
            db = self._branch(res[dst_id])
            self.assertTrue(sb["settled"], src_id)
            self.assertTrue(db["settled"], dst_id)
            tr = [l for l in sb["losers"] if l["id"] == feast_key]
            self.assertEqual(len(tr), 1, src_id)
            self.assertEqual(tr[0]["disposition"], "transferred", src_id)
            self.assertEqual(tr[0]["destination"], expected_dest, src_id)
            self.assertIsNone(tr[0]["destinationNotComputed"], src_id)
            self.assertEqual(db["winner"]["id"], feast_key, dst_id)
            self.assertEqual(db["winner"]["source"], "arrived", dst_id)

        # Also check Annunciation kept its RG 96 a proper seat in 2035
        an35 = self._branch(res["an-2035-dst"])
        self.assertEqual(an35["winner"]["id"], "annuntiatio-beatae-mariae-virginis")
        self.assertEqual(an35["winner"]["source"], "arrived")

    # ------------------------------------------------------------------ Postconciliar

    def test_postconciliar_annunciation_on_easter_sunday_and_octave(self) -> None:
        cases = [
            (1818, "1818-03-30"),  # Easter Mar 22 -> Mar 25 Easter Wed -> Mon Mar 30
            (1940, "1940-04-01"),  # Easter Mar 24 -> Mar 25 Easter Mon -> Mon Apr 1
            (2008, "2008-03-31"),  # Easter Mar 23 -> Mar 25 Easter Tue -> Mon Mar 31
            (2035, "2035-04-02"),  # Easter Mar 25 -> Mar 25 Easter Sun -> Mon Apr 2
            (2046, "2046-04-02"),  # Easter Mar 25 -> Mar 25 Easter Sun -> Mon Apr 2
        ]
        queries = []
        for y, seat in cases:
            queries.append((f"src-{y}", "postconciliar", f"{y}-03-25"))
            queries.append((f"dst-{y}", "postconciliar", seat))
        res = self.derive_batch(queries)

        for y, seat in cases:
            sb = self._branch(res[f"src-{y}"])
            db = self._branch(res[f"dst-{y}"])
            self.assertTrue(sb["settled"], y)
            tr = [l for l in sb["losers"] if l["id"] == "annunciation-lord"]
            self.assertEqual(len(tr), 1, y)
            self.assertEqual(tr[0]["disposition"], "transferred", y)
            self.assertEqual(tr[0]["destination"], seat, y)
            self.assertTrue(db["settled"], y)
            self.assertEqual(db["winner"]["id"], "annunciation-lord", y)
            self.assertEqual(db["winner"]["source"], "arrived", y)

    def test_postconciliar_st_joseph_in_holy_week_anticipated(self) -> None:
        cases = [
            (1818, "1818-03-14"),  # Easter Mar 22 -> Easter - 8 = Sat Mar 14
            (1940, "1940-03-16"),  # Easter Mar 24 -> Easter - 8 = Sat Mar 16
            (2008, "2008-03-15"),  # Easter Mar 23 -> Easter - 8 = Sat Mar 15
            (2035, "2035-03-17"),  # Easter Mar 25 -> Easter - 8 = Sat Mar 17
            (2046, "2046-03-17"),  # Easter Mar 25 -> Easter - 8 = Sat Mar 17
            (2062, "2062-03-18"),  # Easter Mar 26 (Mar 19 = Palm Sun) -> Easter - 8 = Sat Mar 18
        ]
        queries = []
        for y, seat in cases:
            queries.append((f"src-{y}", "postconciliar", f"{y}-03-19"))
            queries.append((f"dst-{y}", "postconciliar", seat))
        res = self.derive_batch(queries)

        for y, seat in cases:
            sb = self._branch(res[f"src-{y}"])
            db = self._branch(res[f"dst-{y}"])
            self.assertTrue(sb["settled"], y)
            tr = [l for l in sb["losers"] if l["id"] == "saint-joseph-spouse-blessed-virgin-mary"]
            self.assertEqual(len(tr), 1, y)
            self.assertEqual(tr[0]["disposition"], "transferred", y)
            self.assertEqual(tr[0]["destination"], seat, y)
            self.assertIn("anticipated", tr[0]["why"], y)
            self.assertTrue(db["settled"], y)
            self.assertEqual(db["winner"]["id"], "saint-joseph-spouse-blessed-virgin-mary", y)
            self.assertEqual(db["winner"]["source"], "arrived", y)

    def test_postconciliar_row3_solemnity_ties_resolved_and_territorial_isolated(self) -> None:
        res = self.derive_batch([
            # Sacred Heart vs St John Baptist (Fri Jun 24 -> anticipated Thu Jun 23)
            ("sh-jb-2022-src", "postconciliar", "2022-06-24"),
            ("sh-jb-2022-dst", "postconciliar", "2022-06-23"),
            ("sh-jb-2033-src", "postconciliar", "2033-06-24"),
            ("sh-jb-2033-dst", "postconciliar", "2033-06-23"),
            ("sh-jb-2044-src", "postconciliar", "2044-06-24"),
            ("sh-jb-2044-dst", "postconciliar", "2044-06-23"),
            # Corpus Christi (Thu) vs St John Baptist (2038-06-24 -> Fri Jun 25 ONLY under Thu branch!)
            ("cc-jb-2038-src", "postconciliar", "2038-06-24"),
            ("cc-jb-2038-dst", "postconciliar", "2038-06-25"),
            # Corpus Christi (Sun) vs St John Baptist (2057-06-24 -> Mon Jun 25 ONLY under Sun branch!)
            ("cc-jb-2057-src", "postconciliar", "2057-06-24"),
            ("cc-jb-2057-dst", "postconciliar", "2057-06-25"),
            # Sacred Heart vs Ss Peter & Paul (2057-06-29 -> Sat Jun 30 unconditionally!)
            ("sh-pp-2057-src", "postconciliar", "2057-06-29"),
            ("sh-pp-2057-dst", "postconciliar", "2057-06-30"),
        ])

        # 1. Sacred Heart vs John Baptist (2022, 2033, 2044)
        for y in (2022, 2033, 2044):
            sb = self._branch(res[f"sh-jb-{y}-src"])
            db = self._branch(res[f"sh-jb-{y}-dst"])
            self.assertTrue(sb["settled"], y)
            self.assertEqual(sb["winner"]["id"], "most-sacred-heart-jesus", y)
            tr = [l for l in sb["losers"] if l["id"] == "nativity-saint-john-baptist"]
            self.assertEqual(len(tr), 1, y)
            self.assertEqual(tr[0]["disposition"], "transferred", y)
            self.assertEqual(tr[0]["destination"], f"{y}-06-23", y)
            self.assertTrue(db["settled"], y)
            self.assertEqual(db["winner"]["id"], "nativity-saint-john-baptist", y)
            self.assertEqual(db["winner"]["source"], "arrived", y)

        # 2. Corpus Christi Thu vs John Baptist (2038) — territorial isolation!
        s38_thu = self._branch(res["cc-jb-2038-src"], "corpus-christi-thursday")
        s38_sun = self._branch(res["cc-jb-2038-src"], "corpus-christi-transferred-to-sunday")
        self.assertEqual(s38_thu["winner"]["id"], "corpus-christi")
        self.assertEqual([l["destination"] for l in s38_thu["losers"] if l["id"] == "nativity-saint-john-baptist"], ["2038-06-25"])
        self.assertEqual(s38_sun["winner"]["id"], "nativity-saint-john-baptist")

        d38_thu = self._branch(res["cc-jb-2038-dst"], "corpus-christi-thursday")
        d38_sun = self._branch(res["cc-jb-2038-dst"], "corpus-christi-transferred-to-sunday")
        self.assertEqual(d38_thu["winner"]["id"], "nativity-saint-john-baptist")
        self.assertEqual(d38_thu["winner"]["source"], "arrived")
        self.assertNotIn("nativity-saint-john-baptist", [c["key"] for c in d38_sun["candidates"]])

        # 3. Corpus Christi Sun vs John Baptist (2057) — territorial isolation!
        s57_thu = self._branch(res["cc-jb-2057-src"], "corpus-christi-thursday")
        s57_sun = self._branch(res["cc-jb-2057-src"], "corpus-christi-transferred-to-sunday")
        self.assertEqual(s57_thu["winner"]["id"], "nativity-saint-john-baptist")
        self.assertEqual(s57_sun["winner"]["id"], "corpus-christi")
        self.assertEqual([l["destination"] for l in s57_sun["losers"] if l["id"] == "nativity-saint-john-baptist"], ["2057-06-25"])

        d57_thu = self._branch(res["cc-jb-2057-dst"], "corpus-christi-thursday")
        d57_sun = self._branch(res["cc-jb-2057-dst"], "corpus-christi-transferred-to-sunday")
        self.assertNotIn("nativity-saint-john-baptist", [c["key"] for c in d57_thu["candidates"]])
        self.assertEqual(d57_sun["winner"]["id"], "nativity-saint-john-baptist")
        self.assertEqual(d57_sun["winner"]["source"], "arrived")

        # 4. Sacred Heart vs Peter & Paul (2057-06-29 -> 2057-06-30 unconditionally, no spurious territorial split!)
        self.assertEqual(len(res["sh-pp-2057-src"]["options"]), 1)
        self.assertEqual(len(res["sh-pp-2057-dst"]["options"]), 1)
        s57_pp = self._branch(res["sh-pp-2057-src"])
        d57_pp = self._branch(res["sh-pp-2057-dst"])
        self.assertEqual(s57_pp["winner"]["id"], "most-sacred-heart-jesus")
        self.assertEqual([l["destination"] for l in s57_pp["losers"] if l["id"] == "saints-peter-paul-apostles"], ["2057-06-30"])
        self.assertEqual(d57_pp["winner"]["id"], "saints-peter-paul-apostles")
        self.assertEqual(d57_pp["winner"]["source"], "arrived")

    # ------------------------------------------------------------------ Non-regression

    def test_roman_pre_1955_unchanged_by_bissextile_or_general_transfers(self) -> None:
        res = self.derive_batch([
            ("pre55-2028-24", "roman-pre-1955", "2028-02-24"),
            ("pre55-2036-1102", "roman-pre-1955", "2036-11-02"),
            ("pre55-2036-1103", "roman-pre-1955", "2036-11-03"),
        ])
        # roman-pre-1955 stays untouched by 1962 bissextile rule
        self.assertIn("s-matthiae-apostoli", [c["key"] for c in self._branch(res["pre55-2028-24"])["candidates"]])
        # All Souls proper seat still works in roman-pre-1955
        self.assertEqual(self._branch(res["pre55-2036-1102"])["winner"]["id"], "pentecost-22")
        self.assertEqual(self._branch(res["pre55-2036-1103"])["winner"]["id"], "commemoratione-omnium-fidelium-defunctorum")
        self.assertEqual(self._branch(res["pre55-2036-1103"])["winner"]["source"], "arrived")


if __name__ == "__main__":
    unittest.main()
