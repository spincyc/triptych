#!/usr/bin/env python3
"""Keep unresolved curriculum translations out of source and PDF surfaces."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "src/gpt/curriculums/ecclesiastical-latin/shared/content/volume1/all.tex"
)
PASSAGE_INVENTORY = (
    ROOT
    / "src/gpt/curriculums/ecclesiastical-latin/research/passage-inventory.md"
)
PDF_ROOT = ROOT / "pdf/gpt/curriculums/ecclesiastical-latin"
TEXT_SUFFIXES = frozenset(
    {
        ".css",
        ".html",
        ".js",
        ".json",
        ".md",
        ".py",
        ".tex",
        ".toml",
        ".tsv",
        ".txt",
        ".yaml",
        ".yml",
    }
)
PROTECTED_FINGERPRINTS = frozenset(
    {
        (4, "dd68e34004e9dafc378b50e89ac1b1bb720de65dc3b378d9f64f857f90c3ea93"),
        (7, "04af286f323881b1f533a4e216354ce9231252ff6393c1ca3122af23f22a95a8"),
        (8, "9194d3c85e8af790e049b5d128eeff8aebe24a1d35cd9da16adca9904b525a0d"),
        (11, "890f276da1000218103969f1bd9295256cb6eb68817b01123af056f7349ed88a"),
        (34, "b52bcbb6bbfc9a01828f1e18e1e47f7e50e361d44cbe7217621597f2b11723fe"),
    }
)
STATUS_REASON = "authorship-and-redistribution-basis-unestablished"


def contains_protected_fingerprint(text: str) -> bool:
    words = re.findall(r"[a-z]+", text.casefold())
    for word_count, fingerprint in PROTECTED_FINGERPRINTS:
        for start in range(len(words) - word_count + 1):
            window = " ".join(words[start : start + word_count])
            if hashlib.sha256(window.encode("utf-8")).hexdigest() == fingerprint:
                return True
    return False


class CurriculumLiturgicalRightsTests(unittest.TestCase):
    def test_current_text_tree_excludes_unresolved_english(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "src/gpt/curriculums/ecclesiastical-latin"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
        findings: list[str] = []
        for raw_path in tracked:
            if not raw_path:
                continue
            path = ROOT / raw_path.decode("utf-8")
            if path.suffix.casefold() not in TEXT_SUFFIXES or not path.is_file():
                continue
            if contains_protected_fingerprint(path.read_text(encoding="utf-8")):
                findings.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(findings, [])

        source = SOURCE.read_text(encoding="utf-8")
        inventory = PASSAGE_INVENTORY.read_text(encoding="utf-8")
        self.assertIn("English rendering status: unavailable", source)
        self.assertIn(STATUS_REASON, inventory)
        for stable_id in ("W.I.20", "W.I.21", "W.I.27", "W.I.53", "W.II.61"):
            self.assertIn(f"| {stable_id} | English | unavailable |", inventory)

    def test_installed_pdfs_exclude_unresolved_english(self) -> None:
        pdftotext = shutil.which("pdftotext")
        self.assertIsNotNone(pdftotext, "pdftotext is required for the PDF rights gate")
        pdfs = sorted(PDF_ROOT.rglob("*.pdf"))
        self.assertTrue(pdfs, f"no installed curriculum PDFs found below {PDF_ROOT}")
        findings: list[str] = []
        for pdf in pdfs:
            extracted = subprocess.run(
                [pdftotext, str(pdf), "-"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            if contains_protected_fingerprint(extracted):
                findings.append(pdf.relative_to(ROOT).as_posix())
        self.assertEqual(findings, [])

        module_pdf = PDF_ROOT / "01-foundations/06-pronouns-prepositions-and-reading.pdf"
        extracted = subprocess.run(
            [pdftotext, str(module_pdf), "-"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertIn("English rendering status: unavailable", extracted)


if __name__ == "__main__":
    unittest.main()
