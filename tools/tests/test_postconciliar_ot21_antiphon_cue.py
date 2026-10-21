"""Preserve the source-corrected OT21 cue without changing its Vulgate words.

Notitiae2008 AP53/p371 changes MR p471 second Communion cue 55 to54,
with a literal Is abbreviation typo; ICEL2010 AP85/p77 independently gives
John6:54. MR2002 AP285 and the existing locus owner establish Vulgate6:55.
These are appointment/address facts, never a liturgical-body text claim.
"""
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / "src/sources/calendars/postconciliar/propers.yaml"


def tool(name):
    loader = SourceFileLoader("_ot21_cue_test_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class OrdinaryTime21AntiphonCue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(PROPERS.read_text())
        cls.mp, cls.canon = tool("mass-propers"), tool("citations")
        cls.masses = {m["key"]: m for _, m in cls.mp.masses_of(cls.document)}
        entries = [e for _, m in cls.mp.masses_of(cls.document)
            for e, _ in cls.mp.numbered_entries(m, cls.document["psalm_numbering"])]
        cls.divergences = {target: cls.mp.Divergences("postconciliar", cls.document, entries, cls.canon, target,
            numberings=tuple(s for s in cls.mp.SYSTEMS if s != cls.mp.RESOLVED_IN)) for target in cls.mp.SYSTEMS}

    def test_2008_corrected_cue_preserves_vulgate_reading_and_refusal(self):
        proper = next(p for p in self.masses["ot-21"]["propers"] if p["name"] == "Communion Antiphon (alternative)")
        self.assertEqual(proper["verses"], [{"book": "John", "ranges": [
            {"begin": {"chapter": 6, "verse": 54}, "end": {"chapter": 6, "verse": 54}}], "ref": "John 6:54"}])
        self.assertEqual(proper["ordinary_disposition"]["kind"], "alternative")
        self.assertEqual(proper["ordinary_disposition"]["group"], "communion-antiphon")
        # The historical option identity is technical and remains stable.
        self.assertEqual(proper["ordinary_disposition"]["option"], "john-6-55")
        entry, numbering = next(self.mp.numbered_proper_entries(proper, self.document["psalm_numbering"]))
        citation = self.mp.citation_structure(entry, numbering, self.mp.book_tokens(), self.divergences)
        self.assertEqual(citation["ref"], "John 6:54")
        self.assertEqual(citation["loci"]["vulgate"], [{"chapter": 6, "first": 55, "last": 55}])
        self.assertNotIn("hebrew", citation["loci"])
        self.assertIn("unrecorded", citation["refused"]["hebrew"])

    def test_old_unrecorded_55_is_not_inherited_as_a_future_default(self):
        # A later source row with raw55 needs its own exact proof. Renaming
        # OT21's declaration must not silently authorize that different cue.
        entry = self.canon.parse_citation("John 6:55")
        citation = self.mp.citation_structure(entry, self.document["psalm_numbering"], self.mp.book_tokens(), self.divergences)
        self.assertNotIn("vulgate", citation["loci"])
        self.assertIn("no resolution for this citation", citation["refused"]["vulgate"])
        self.assertNotIn("hebrew", citation["loci"])
        self.assertIn("unrecorded", citation["refused"]["hebrew"])


if __name__ == "__main__":
    unittest.main()
