#!/usr/bin/env python3
"""Keep restricted liturgical English out of curriculum publication surfaces."""

from __future__ import annotations

import collections
import hashlib
import re
import shutil
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CURRICULUM_ROOT = ROOT / "src/gpt/curriculums/ecclesiastical-latin"
PDF_ROOT = ROOT / "pdf/gpt/curriculums/ecclesiastical-latin"
REGISTRY = ROOT / "src/sources/inventories/icel-2010-chant-fingerprints-v1.toml"
ALLOWLIST = CURRICULUM_ROOT / "research/liturgical-rights-allowlist-v1.toml"
PASSAGE_INVENTORY = CURRICULUM_ROOT / "research/passage-inventory.md"
ICEL_ARTIFACT_ROOT = (
    ROOT
    / "src/sources/works/international-commission-on-english-in-the-liturgy/"
    "music-for-the-roman-missal/editions/2010-chants-web-2026-08-21/artifacts"
)
WORD_RE = re.compile(r"[a-z]+")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
STATUS_REASON = "authorship-and-redistribution-basis-unestablished"
DISPOSITIONS = frozenset(
    {"independently-retainable", "non-liturgical-incidental-collision"}
)
BASIS_KINDS = frozenset(
    {
        "non-rights-disposition",
        "project-created-independent",
        "public-domain-exact-witness",
    }
)


def digest(words: list[str]) -> str:
    return hashlib.sha256(" ".join(words).encode()).hexdigest()


def marked_words(text: str, *, pdf: bool) -> list[tuple[str, int]]:
    units = text.split("\f") if pdf else text.splitlines()
    return [
        (word, number)
        for number, unit in enumerate(units, 1)
        for word in WORD_RE.findall(unit.casefold())
    ]


def de_tex(text: str) -> str:
    text = re.sub(r"\\[A-Za-z@]+\*?", " ", text)
    return text.replace("{", " ").replace("}", " ")


def load_registry() -> tuple[dict[str, object], dict[str, tuple[str, ...]]]:
    data = tomllib.loads(REGISTRY.read_text(encoding="utf-8"))
    window_artifacts: dict[str, set[str]] = collections.defaultdict(set)
    for artifact in data["artifact"]:
        for value in artifact["four_word_sha256"]:
            window_artifacts[value].add(artifact["artifact_id"])
    return data, {
        value: tuple(sorted(artifact_ids))
        for value, artifact_ids in window_artifacts.items()
    }


def source_findings(
    window_artifacts: dict[str, tuple[str, ...]],
) -> tuple[list[tuple[object, ...]], list[str]]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", CURRICULUM_ROOT.relative_to(ROOT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    findings: list[tuple[object, ...]] = []
    undecodable: list[str] = []
    for raw_path in tracked:
        if not raw_path:
            continue
        relative = raw_path.decode()
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            undecodable.append(relative)
            continue
        matches: set[tuple[str, int, int]] = set()
        for projection in (text, de_tex(text)):
            marked = marked_words(projection, pdf=False)
            for start in range(len(marked) - 3):
                value = digest([word for word, _ in marked[start : start + 4]])
                if value in window_artifacts:
                    matches.add((value, marked[start][1], marked[start + 3][1]))
        findings.extend(
            (
                "tracked-source",
                relative,
                line_start,
                line_end,
                1,
                value,
                window_artifacts[value],
            )
            for value, line_start, line_end in sorted(matches)
        )
    return findings, undecodable


def pdf_findings(
    window_artifacts: dict[str, tuple[str, ...]],
) -> list[tuple[object, ...]]:
    pdftotext = shutil.which("pdftotext")
    if pdftotext is None:
        raise RuntimeError("pdftotext is required for the PDF rights gate")
    findings: list[tuple[object, ...]] = []
    for path in sorted(PDF_ROOT.rglob("*.pdf")):
        extracted = subprocess.run(
            [pdftotext, str(path), "-"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        marked = marked_words(extracted, pdf=True)
        counts: collections.Counter[tuple[str, int, int]] = collections.Counter()
        for start in range(len(marked) - 3):
            value = digest([word for word, _ in marked[start : start + 4]])
            if value not in window_artifacts:
                continue
            page_start, page_end = marked[start][1], marked[start + 3][1]
            key = value, page_start, page_end
            counts[key] += 1
            findings.append(
                (
                    "installed-pdf",
                    path.relative_to(ROOT).as_posix(),
                    page_start,
                    page_end,
                    counts[key],
                    value,
                    window_artifacts[value],
                )
            )
    return findings


def allowance_key(item: dict[str, object]) -> tuple[object, ...]:
    if item["surface"] == "tracked-source":
        start, end = item["line_start"], item["line_end"]
    else:
        start, end = item["page_start"], item["page_end"]
    return (
        item["surface"],
        item["path"],
        start,
        end,
        item["occurrence"],
        item["normalized_sha256"],
        tuple(item["expected_artifact_ids"]),
    )


class CurriculumLiturgicalRightsTests(unittest.TestCase):
    def test_hash_only_registry_is_complete_and_well_formed(self) -> None:
        data, window_artifacts = load_registry()
        self.assertEqual(data["schema"], "triptych-icel-2010-chant-fingerprints-v1")
        self.assertEqual(data["normalizer"], "casefold-ascii-a-z")
        self.assertEqual(data["minimum_word_count"], 4)
        self.assertIs(data["contains_protected_wording"], False)
        self.assertEqual(len(data["artifact"]), 17)
        self.assertEqual(len(window_artifacts), 1410)
        artifact_ids: set[str] = set()
        for artifact in data["artifact"]:
            artifact_id = artifact["artifact_id"]
            self.assertNotIn(artifact_id, artifact_ids)
            artifact_ids.add(artifact_id)
            self.assertRegex(artifact["artifact_sha256"], HASH_RE)
            self.assertRegex(artifact["normalized_stream_sha256"], HASH_RE)
            windows = artifact["four_word_sha256"]
            self.assertEqual(len(windows), artifact["normalized_word_count"] - 3)
            for value in windows:
                self.assertRegex(value, HASH_RE)
            historical_path = Path(artifact["path"])
            self.assertEqual(historical_path.name, f"{artifact_id}.tsv")
            self.assertEqual(historical_path.parent.name, artifact_id)
            self.assertFalse((ROOT / historical_path).exists())
            manifest_path = ICEL_ARTIFACT_ROOT / artifact_id / "artifact.toml"
            manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["artifact_type"], "normalized-text")
            self.assertEqual(manifest["storage"], "restricted")
            self.assertEqual(manifest["rights_status"], "restricted")
            self.assertEqual(manifest["sha256"], artifact["artifact_sha256"])

    def test_allowlist_exactly_matches_current_public_surfaces(self) -> None:
        _, window_artifacts = load_registry()
        allowlist = tomllib.loads(ALLOWLIST.read_text(encoding="utf-8"))
        self.assertEqual(
            allowlist["schema"],
            "triptych-curriculum-liturgical-rights-allowlist-v1",
        )
        self.assertIs(allowlist["contains_protected_wording"], False)
        expected: list[tuple[object, ...]] = []
        ids: set[str] = set()
        for item in allowlist["allowance"]:
            self.assertNotIn(item["id"], ids)
            ids.add(item["id"])
            self.assertIn(item["disposition"], DISPOSITIONS)
            self.assertIn(item["basis_kind"], BASIS_KINDS)
            self.assertEqual(item["word_count"], 4)
            self.assertRegex(item["normalized_sha256"], HASH_RE)
            self.assertEqual(
                tuple(item["expected_artifact_ids"]),
                window_artifacts[item["normalized_sha256"]],
            )
            self.assertEqual(item["reviewed_on"], "2026-08-27")
            self.assertTrue(item["basis_record"])
            self.assertTrue(item["authority_scope"])
            self.assertTrue(item["review_record"])
            self.assertNotIn("..", Path(item["path"]).parts)
            if item["surface"] == "tracked-source":
                self.assertTrue(
                    item["path"].startswith("src/gpt/curriculums/ecclesiastical-latin/")
                )
                self.assertNotIn("page_start", item)
            else:
                self.assertEqual(item["surface"], "installed-pdf")
                self.assertTrue(
                    item["path"].startswith("pdf/gpt/curriculums/ecclesiastical-latin/")
                )
                self.assertNotIn("line_start", item)
            expected.append(allowance_key(item))
        self.assertEqual(len(expected), len(set(expected)), "duplicate allowance")

        source, undecodable = source_findings(window_artifacts)
        self.assertEqual(undecodable, [], "tracked curriculum file is not UTF-8")
        pdfs = sorted(PDF_ROOT.rglob("*.pdf"))
        self.assertEqual(len(pdfs), 37, "installed curriculum PDF census changed")
        actual = source + pdf_findings(window_artifacts)
        self.assertEqual(
            sorted(actual),
            sorted(expected),
            "hash-only rights finding differs from the exact location-scoped allowlist",
        )

    def test_unavailable_dispositions_cover_affected_stable_ids(self) -> None:
        inventory = PASSAGE_INVENTORY.read_text(encoding="utf-8")
        self.assertIn(STATUS_REASON, inventory)
        for stable_id in (
            "W.I.2",
            "W.I.55",
            "W.II.1",
            "W.II.57",
            "I.2.1",
            "I.48.1",
            "II.1.1",
            "II.51.1",
            "R/ordinary-dialogue",
        ):
            self.assertIn(stable_id, inventory)

    def test_scanner_is_location_and_surface_sensitive(self) -> None:
        synthetic = "alpha beta gamma delta"
        value = digest(synthetic.split())
        registry = {value: ("synthetic-artifact",)}
        marked = marked_words(synthetic, pdf=False)
        self.assertEqual(digest([word for word, _ in marked]), value)
        live = ("tracked-source", "safe.tex", 1, 1, 1, value, registry[value])
        moved = ("tracked-source", "moved.tex", 1, 1, 1, value, registry[value])
        pdf = ("installed-pdf", "safe.pdf", 1, 1, 1, value, registry[value])
        self.assertNotEqual(live, moved)
        self.assertNotEqual(live, pdf)

    def test_tex_control_words_cannot_hide_a_window(self) -> None:
        projected = de_tex(r"alpha \Textbf{beta gamma} delta")
        self.assertEqual(
            [word for word, _ in marked_words(projected, pdf=False)],
            ["alpha", "beta", "gamma", "delta"],
        )


if __name__ == "__main__":
    unittest.main()
