#!/usr/bin/env python3
"""A patterned work's registered holdings must each have a locus it admits.

`source-library validate` holds passage and binding loci to their work's
`locus_pattern`, and never holds the pattern to what the library registers
under the work. Two patterns drifted that way. `work.cassiodorus.expositio-
psalmorum` admitted Pss 16, 24, 64 and 88 while the library held its
expositions of Pss 39, 70, 85, 95, 97, 101 and 121 and Adriaen's CCSL 98 for
Pss 71-150; `work.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-
epistolas` admitted two named loci over a volume running from the proemium to
Galatians 6. No valid locus could be written for most of either holding, so
bindings named their sections in free text, and widening a pattern moved every
fingerprint under the work. The maintainer's sweep of 2026-09-23 widened both.

Each artifact and segment registered under a work named here is mapped to the
loci it carries -- read off its own record or tracked bytes where that is
mechanical, declared in `DECLARED` against a phrase of its record where it is
not -- and each must match the work's pattern. A holding that maps to no locus
fails: state its extent here in the change that registers it, and widen the
pattern if it does not fit. The rejected loci are the other half of the
decision, that a pattern admits what the holdings carry and nothing unrelated.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VULGATE = ROOT / "src/sources/bibles/clementine-vulgate/chapters"


def load_source_library():
    path = ROOT / "tools/source-library"
    loader = importlib.machinery.SourceFileLoader(
        "_source_locus_patterns_source_library", str(path)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SOURCE_LIBRARY = load_source_library()


def vulgate_chapters(book: str) -> int:
    return len(list((VULGATE / book).glob("*.json")))


CASSIODORUS = "work.cassiodorus.expositio-psalmorum"
LAPIDE = "work.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-epistolas"

# A psalm's exposition opens with its title as sectio 1 in every registered
# delivery, so `<psalm>.1` is the locus that names a psalm a holding carries.
PSALTER = [f"{psalm}.1" for psalm in range(1, vulgate_chapters("Ps") + 1)]

# Lapide's 1614 volume: the general proemium, each epistle's argumentum, then
# the exposition chapter by chapter. The epistles are those whose running heads
# stand in the tracked optical layer (`RUNNING_HEADS` below), in the Vulgate's
# chapter count; the scan stops in Galatians 6.
LAPIDE_EPISTLES = {
    "Rom": "epistola-ad-romanos-argumentum",
    "1Cor": "epistola-i-ad-corinthios-argumentum",
    "2Cor": "epistola-ii-ad-corinthios-argumentum",
    "Gal": "epistola-ad-galatas-argumentum",
}
LAPIDE_1614 = ["prooemium", *LAPIDE_EPISTLES.values()] + [
    f"{book}.{chapter}"
    for book in LAPIDE_EPISTLES
    for chapter in range(1, vulgate_chapters(book) + 1)
]
LAPIDE_1614_PREFIX = (
    "artifact.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-epistolas."
    "antwerp-1614."
)

# Holdings whose extent is not mechanical from their bytes, each with a phrase
# its own record or edition must still carry, so the declaration cannot outlive
# the record it restates.
DECLARED = {
    "artifact.cassiodorus.expositio-psalmorum.latin-adriaen-ccsl98-turnhout-1958."
    "azbyka-google-scan-pdf-c72410b0": (
        "edition title",
        "Expositio Psalmorum LXXI-CL",
        PSALTER[70:],
    ),
    "artifact.cassiodorus.expositio-psalmorum.latin-migne-wikisource-web-2026-09-05."
    "wikisource-index-c531d00e": (
        "notes",
        "a table of contents naming all 150 psalms",
        PSALTER,
    ),
    LAPIDE_1614_PREFIX + "internet-archive-google-facsimile-pdf-6a83dd45": (
        "provenance",
        "p. 514 for the Galatians Argumentum",
        LAPIDE_1614,
    ),
    LAPIDE_1614_PREFIX + "ia-djvu-text-197365b2": (
        "notes",
        "this volume stops at Galatians",
        LAPIDE_1614,
    ),
    LAPIDE_1614_PREFIX + "ia-item-metadata-f6b3f465": (
        "notes",
        "Commentaria in omnes D. Pauli Epistolas",
        LAPIDE_1614,
    ),
}

RUMPFID = re.compile(
    r"rumpfid=Cassiodorus%2C\+Expositio\+in\+Psalterium%2C\+[1-3]%2C\++"
    r"([1-9][0-9]{0,2})(?:&|$)"
)
WIKISOURCE_PSALM = re.compile(
    r"^https://la\.wikisource\.org/wiki/Expositio_in_Psalterium/([1-9][0-9]{0,2})$"
)
LISTED_PSALM = re.compile(r"^Expositio in Psalterium/([1-9][0-9]{0,2})$")

RUNNING_HEAD = r"EP[I1lL]S[T7].{{0,6}}A[DBd][ .,]{{0,3}}{}"
RUNNING_HEADS = {
    "held": {"Rom": "R[Oo][MmWw]", "Cor": "C[Oo][NnRrGg]", "Gal": "G[Aa][LlRr][Aa]"},
    "absent": {
        "Eph": "E[Pp][Hh]",
        "Phil": "P[Hh][Ii1l][Ll]",
        "Col": "C[Oo][Ll]",
        "Thess": "T[Hh][Ee][Ss]",
        "Tim": "T[Ii1][Mm]",
        "Tit": "T[Ii1][Tt]",
        "Heb": "H[Ee][Bb]",
    },
}

REJECTED = {
    CASSIODORUS: [
        "0.1", "151.1", "016.1", "16", "16.0", "16.1000", "16.1,2,3",
        "16.1-2-3", "praefatio", "Ps.16.1",
    ],
    LAPIDE: [
        "Eph.1.1", "Heb.1.1", "Phil.1", "Rom.17", "1Cor.17.1", "2Cor.14",
        "Gal.7.1", "Gal.6.0", "Gen.1.1", "1 Cor 1:4",
        "epistola-ad-ephesios-argumentum", "epistola-dedicatoria",
    ],
}


class SourceLocusPatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = SOURCE_LIBRARY.load_library(ROOT)
        cls.records = cls.library.records

    def work_of(self, record) -> str | None:
        edition = self.records.get(record.data.get("edition_id", ""))
        return edition.data.get("work_id") if edition else None

    def holdings(self, work_id: str) -> list:
        found = [
            record
            for record in self.records.values()
            if record.record_type in {"artifact", "segment"}
            and self.work_of(record) == work_id
        ]
        self.assertTrue(found, f"{work_id} registers no artifact or segment")
        return sorted(found, key=lambda record: record.record_id)

    def pattern(self, work_id: str) -> re.Pattern[str]:
        return re.compile(self.records[work_id].data["locus_pattern"])

    def tracked_bytes(self, record) -> bytes | None:
        if record.data.get("storage") != "tracked":
            return None
        return (ROOT / record.data["path"]).read_bytes()

    def psalm_of(self, record) -> str | None:
        url = record.data.get("source_url", "")
        match = RUMPFID.search(url) or WIKISOURCE_PSALM.match(url)
        if match:
            return match.group(1)
        parent = self.records.get(record.data.get("derived_from", ""))
        return self.psalm_of(parent) if parent else None

    def mechanical_loci(self, record) -> list[str]:
        loci = []
        psalm = self.psalm_of(record)
        if psalm:
            loci.append(f"{psalm}.1")
        payload = self.tracked_bytes(record)
        media = record.data.get("media_type", "")
        if payload is not None and psalm and media.startswith("text/plain"):
            for line in payload.decode("utf-8").splitlines():
                loci.append(f"{psalm}.{line.split(chr(9), 1)[0]}")
        if payload is not None and media == "application/json":
            for page in json.loads(payload)["query"]["allpages"]:
                listed = LISTED_PSALM.match(page["title"])
                if listed:
                    loci.append(f"{listed.group(1)}.1")
        return loci

    def declared_loci(self, record) -> list[str]:
        if record.record_id not in DECLARED:
            return []
        field, phrase, loci = DECLARED[record.record_id]
        owner = record.data
        if field == "edition title":
            owner, field = self.records[record.data["edition_id"]].data, "title"
        self.assertIn(
            phrase,
            owner.get(field, ""),
            f"{record.record_id}: its record no longer says what DECLARED restates",
        )
        return loci

    def test_every_registered_holding_has_an_admitted_locus(self) -> None:
        for work_id in (CASSIODORUS, LAPIDE):
            pattern = self.pattern(work_id)
            for record in self.holdings(work_id):
                loci = self.mechanical_loci(record) + self.declared_loci(record)
                with self.subTest(holding=record.record_id):
                    self.assertTrue(
                        loci,
                        "no locus is known for this holding: state its extent in "
                        "tools/tests/test_source_locus_patterns.py",
                    )
                    refused = sorted({locus for locus in loci if not pattern.fullmatch(locus)})
                    self.assertEqual(
                        refused, [], f"{work_id} locus_pattern refuses these loci"
                    )

    def test_patterns_admit_nothing_unrelated(self) -> None:
        for work_id, loci in REJECTED.items():
            pattern = self.pattern(work_id)
            for locus in loci:
                with self.subTest(work=work_id, locus=locus):
                    self.assertIsNone(pattern.fullmatch(locus))

    def test_lapide_epistles_are_the_running_heads_of_the_volume(self) -> None:
        text = (
            ROOT
            / self.records[LAPIDE_1614_PREFIX + "ia-djvu-text-197365b2"].data["path"]
        ).read_text(encoding="utf-8")
        for state, heads in RUNNING_HEADS.items():
            for epistle, spelling in heads.items():
                count = len(re.findall(RUNNING_HEAD.format(spelling), text))
                with self.subTest(epistle=epistle):
                    if state == "held":
                        self.assertGreater(count, 0)
                    else:
                        self.assertEqual(count, 0)
        pattern = self.pattern(LAPIDE)
        for book in LAPIDE_EPISTLES:
            with self.subTest(book=book):
                last = vulgate_chapters(book)
                self.assertTrue(pattern.fullmatch(f"{book}.{last}"))
                self.assertIsNone(pattern.fullmatch(f"{book}.{last + 1}"))


if __name__ == "__main__":
    unittest.main()
