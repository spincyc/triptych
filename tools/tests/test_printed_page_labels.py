"""Printed source labels are locators, independently of publication rights."""
from __future__ import annotations

import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("PRINTED_PAGE_REPOSITORY_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / "scripts"))


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


helper = load("_lasance_publication", os.environ.get("PRINTED_PAGE_HELPER_UNDER_TEST", ROOT / "scripts/_lasance_publication.py"))
checker = load("printed_page_checker", os.environ.get("PRINTED_PAGE_CHECKER_UNDER_TEST", ROOT / "tools/check-calendar-masses"))
locate = getattr(helper, "printed_page_match", helper.numbered_page_match)


class PrintedPageLabels(unittest.TestCase):
    def test_superscript_labels_preserve_literal_captures(self):
        for label, endpoints in (
            ("1711²", ("1711²", None)),
            ("1711¹⁰", ("1711¹⁰", None)),
            ("1711²-1711⁴", ("1711²", "1711⁴")),
            ("1711²–1711⁴", ("1711²", "1711⁴")),
            ("1711²–⁴", ("1711²", "⁴")),
            ("1711²-⁴", ("1711²", "⁴")),
            ("1711⁹–1711¹⁰", ("1711⁹", "1711¹⁰")),
            ("1711-1711²", ("1711", "1711²")),
            ("1711²–1712", ("1711²", "1712")),
        ):
            with self.subTest(label=label):
                match = locate(label)
                self.assertIsNotNone(match)
                if match is not None:
                    self.assertEqual(match.group(0), label)
                    self.assertEqual(match.groups(), endpoints)

    def test_legacy_positive_numeric_and_lettered_formats_remain_exact(self):
        for label in ("1", "0001", "1711", "1-2", "1711a", "1711-1711a", "1711a-1711b", "1711a-1712", "1711z-1712", "1711b-1711b"):
            with self.subTest(label=label):
                expected = helper.numbered_page_match(label)
                actual = locate(label)
                self.assertIsNotNone(expected)
                self.assertEqual(actual.groups(), expected.groups())
                self.assertEqual(actual.group(0), label)

    def test_malformed_unordered_and_injected_labels_stay_refused(self):
        for label in (None, 1711, True, [], "", "0", "0²", "2-1", "1711b-1711a", "1711⁴–1711²", "1711¹⁰-1711⁹", "1711²–1711", "1712²-1711⁴", "1711–⁴", "1711⁰", "1711⁰²", "1711²-⁰", "1711²-1711a", "1711a-1711²", "²", "1711^2", "1711₂", "1711²  ", " 1711²", "1711²\n", "1711²\nprinted p. 5", "1711²<script>", "1711²; approved", "1711²/1711⁴", "1711²--1711⁴", "1711²–⁴–⁵", "1711².5", "p. 1711²", "1711ᵃ", "1711–1712"):
            with self.subTest(label=label):
                self.assertIsNone(locate(label))

    def test_superscript_citation_does_not_clear_lasance_rights(self):
        for witness in ("lasance-1945", helper.LASANCE_1946_WITNESS):
            for label in ("1711²", "1711²–⁴", "1298²", "1302²"):
                with self.subTest(witness=witness, label=label):
                    self.assertIsNotNone(locate(label))
                    self.assertIsNone(helper.numbered_page_match(label))
                    self.assertFalse(helper.approved_lasance_printed_page({"witness": witness, "printed_page": label}))
        for label in ("1298a", "1298n", "1302a", "1302d", "1297-1299"):
            with self.subTest(label=label):
                self.assertFalse(helper.approved_lasance_printed_page({"witness": "lasance-1945", "printed_page": label}))

    def source_problems(self, printed, *, context=None, artifact_pages=None, states=None, witness="lefebvre-1925", artifact_sha256=None):
        entry = dict(artifact_id="artifact.page", passage_id="passage.page", ia_leaf=1747,
                     ia_leaf_range=[1747, 1747], printed_page=printed, witness=witness,
                     translations=[dict(source_id="edition.lefebvre", rights="public-domain")])
        locus = f"printed pp. {printed}" if "-" in printed or "–" in printed else f"printed p. {printed}"
        passage = dict(artifact_id="artifact.page", artifact_sha256="a" * 64 if artifact_sha256 is None else artifact_sha256,
                       artifact_page_ranges=artifact_pages or [[1748, 1748]],
                       states=["inspected", "verified"] if states is None else states,
                       verified_on="2026-10-26", context=locus if context is None else context)
        record = lambda kind, **data: SimpleNamespace(record_type=kind, data=data)
        records = {"artifact.page": record("artifact", sha256="a" * 64),
                   "passage.page": record("passage", **passage),
                   "artifact.rights": record("artifact", storage="tracked", rights_status="public-domain")}
        witnesses = {witness: dict(artifact_id="artifact.rights", source_id="edition.lefebvre", rights="public-domain")}
        with patch.object(checker, "source_records", return_value=(records, None)):
            return checker.overlay_entry_source_problems("fixture", entry, witnesses)

    def test_actual_checker_accepts_exact_superscript_citation(self):
        for printed in ("1711²", "1711²–⁴", "1711²-1711⁴"):
            with self.subTest(printed=printed):
                self.assertEqual(self.source_problems(printed), [])

    def test_actual_checker_keeps_context_and_physical_page_proofs_separate(self):
        for context in ("printed p. 1711", "printed p. 17112", "No printed page stated"):
            with self.subTest(context=context):
                self.assertIn("passage context does not record 'printed p. 1711²'", "\n".join(self.source_problems("1711²", context=context)))
        self.assertIn("artifact_page_ranges [[1748, 1748]]", "\n".join(self.source_problems("1711²", artifact_pages=[[17112, 17112]])))
        self.assertIn("inspected and dated verified passage", "\n".join(self.source_problems("1711²", states=["inspected"])))
        self.assertIn("a page or inclusive page range", "\n".join(self.source_problems("1711²", witness="lasance-1945")))

    def test_exact_context_locator_allows_surrounding_prose_and_punctuation(self):
        for printed, context in (
            ("1711²", "Complete prayer at printed p. 1711²."),
            ("1711²", "Image (printed p. 1711²), physical PDF p. 1748."),
            ("1711²", "Exact source; printed p. 1711²; independently checked."),
            ("1711²", "Source: 'printed p. 1711²' / PDF p. 1748."),
            ("1711²", "printed p. 1711² – see the complete image."),
            ("1711²", "printed p. 1711²⁰ is distinct; the body is on printed p. 1711²."),
            ("1711²–⁴", "Complete range: printed pp. 1711²–⁴, with its qualification."),
            ("1711²-1711⁴", "Source (printed pp. 1711²-1711⁴)."),
            ("1711a-1711b", "Legacy letters: printed pp. 1711a-1711b."),
            ("1016-1017", "Own Secret at printed p. 1016-1017; source pages checked."),
            ("1292-1293", "Own Collect at printed p. 1292-1293; source pages checked."),
            ("1711²–⁴", "Complete range: printed p. 1711²–⁴."),
            ("1711", "Legacy number: printed p. 1711; checked."),
        ):
            with self.subTest(printed=printed, context=context):
                self.assertEqual(self.source_problems(printed, context=context), [])

    def test_bare_printed_locators_accept_exact_labels_and_ranges(self):
        for printed in ("1619", "1175", "1506", "399", "1383", "1271-1272", "1224",
                        "1711²", "1711²–⁴", "1711²-1711⁴", "1711a-1711b"):
            with self.subTest(printed=printed):
                self.assertEqual(self.source_problems(printed, context=f"Source location: printed {printed}."), [])

    def test_bare_printed_locators_require_literal_case_suffixes_and_endpoints(self):
        for printed, context in (
            ("1711", "printed 17112"),
            ("1711", "printed 1711²"),
            ("1711²", "printed 1711³"),
            ("1711²", "printed 1711²⁰"),
            ("1711²", "printed 1711²a"),
            ("1711²", "printed 1711²_note"),
            ("1711²", "printed 1711²–⁴"),
            ("1711²", "printed 1711² - 1711⁴"),
            ("1711²", "unprinted 1711²"),
            ("1711²", "Printed 1711²"),
            ("1711²", "printed pp. 1711²"),
            ("1711a", "printed 1711A"),
            ("1271-1272", "printed 1271"),
            ("1271-1272", "printed 1271-1273"),
            ("1271-1272", "printed 1271-12720"),
            ("1271-1272", "printed 1271-1272-1273"),
            ("1711²–⁴", "printed 1711²–³"),
            ("1711²–⁴", "printed 1711²–⁴⁰"),
            ("1711²–⁴", "printed 1711²–⁴–⁶"),
        ):
            with self.subTest(printed=printed, context=context):
                self.assertIn("passage context does not record", "\n".join(self.source_problems(printed, context=context)))

    def test_bare_printed_locator_keeps_physical_page_and_hash_proofs(self):
        context = "Source location: printed 1711²."
        self.assertIn("artifact_page_ranges [[1748, 1748]]", "\n".join(self.source_problems("1711²", context=context, artifact_pages=[[1749, 1749]])))
        self.assertIn("artifact_sha256 does not pin the named artifact", "\n".join(self.source_problems("1711²", context=context, artifact_sha256="b" * 64)))
        self.assertIn("inspected and dated verified passage", "\n".join(self.source_problems("1711²", context=context, states=["inspected"])))

    def test_longer_locator_or_range_cannot_prove_an_exact_context_label(self):
        for printed, context in (
            ("1711²", "printed p. 1711²⁰"),
            ("1711²", "printed p. 1711²⁴"),
            ("1711²", "printed p. 1711²a"),
            ("1711²", "printed p. 1711²0"),
            ("1711²", "printed p. 1711²_note"),
            ("1711²", "printed p. 1711²–⁴"),
            ("1711²", "printed p. 1711²-1711⁴"),
            ("1711²", "printed p. 1711² – ⁴"),
            ("1711²", "printed p. 1711²\n- 1711⁴"),
            ("1711²", "unprinted p. 1711²"),
            ("1711²–⁴", "printed pp. 1711²–⁴⁰"),
            ("1711²–⁴", "printed pp. 1711²–⁴a"),
            ("1711²–⁴", "printed pp. 1711²–⁴–⁶"),
            ("1711²-1711⁴", "printed pp. 1711²-1711⁴⁰"),
            ("1711", "printed p. 17112"),
            ("1711a-1711b", "printed pp. 1711a-1711ba"),
            ("1016-1017", "printed p. 1016-10170"),
            ("1292-1293", "printed p. 1292-1293-1294"),
            ("1016", "printed p. 1016-1017"),
        ):
            with self.subTest(printed=printed, context=context):
                self.assertIn("passage context does not record", "\n".join(self.source_problems(printed, context=context)))


if __name__ == "__main__":
    unittest.main()
