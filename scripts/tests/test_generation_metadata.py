from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "scripts" / "check-generation-metadata"
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_generation_metadata_checker", str(CHECKER_PATH)
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {CHECKER_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

TIMESTAMP = "2026-07-17T13:48:28Z"
CONTRIBUTION = (
    r"\AIModelContribution{test-model}{effort=high}"
    r"{OpenAI Codex CLI 1.2.3; API workspace}"
)


class GenerationMetadataParserTests(unittest.TestCase):
    def parse(self, text: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "generation-metadata.tex"
            path.write_text(text, encoding="utf-8")
            return CHECKER.parse_record(path)

    def test_accepts_canonical_and_inherited_records(self) -> None:
        canonical = self.parse(
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n" + CONTRIBUTION + "\n"
        )
        self.assertEqual(canonical.revision_timestamp, TIMESTAMP)
        self.assertEqual(len(canonical.contributions), 1)
        self.assertIsNone(canonical.inheritance)

        inherited = self.parse(
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            r"\AIInheritedGenerationMetadata{theology/sacraments}"
            + "\n"
        )
        self.assertEqual(inherited.revision_timestamp, TIMESTAMP)
        self.assertEqual(inherited.inheritance, "theology/sacraments")
        self.assertFalse(inherited.contributions)

    def test_rejects_missing_duplicate_and_noninitial_timestamp(self) -> None:
        cases = {
            "missing": CONTRIBUTION + "\n",
            "duplicate": (
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
                + CONTRIBUTION
                + "\n"
            ),
            "noninitial": (
                CONTRIBUTION
                + "\n"
                + rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
                + "\n"
            ),
        }
        for label, text in cases.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                self.parse(text)

    def test_rejects_inheritance_mixed_with_contribution_and_stray_text(self) -> None:
        mixed = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            r"\AIInheritedGenerationMetadata{theology/sacraments}"
            + "\n"
            + CONTRIBUTION
            + "\n"
        )
        stray = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + CONTRIBUTION
            + "\nnot structured\n"
        )
        for text in (mixed, stray):
            with self.assertRaises(ValueError):
                self.parse(text)

    def test_revision_timestamp_requires_strict_possible_utc_whole_seconds(self) -> None:
        invalid = (
            "2026-07-17",
            "2026-07-17T13:48:28+00:00",
            "2026-07-17T13:48:28.1Z",
            "2026-02-30T13:48:28Z",
            "2026-07-17T24:00:00Z",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                CHECKER.validate_revision_timestamp(value)
        self.assertEqual(
            CHECKER.validate_revision_timestamp(TIMESTAMP).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            TIMESTAMP,
        )

    def test_handwritten_revision_label_is_rejected_as_legacy(self) -> None:
        self.assertRegex(r"\textbf{Last revised (UTC):}", CHECKER.LEGACY_LABEL_RE)

    def test_rendered_record_accepts_repeated_model_for_distinct_runtimes(self) -> None:
        first = CHECKER.Contribution(
            "same-model", "effort=high", "OpenAI Codex CLI 1.2.3; first role"
        )
        second = CHECKER.Contribution(
            "same-model", "effort=high", "OpenAI Codex CLI 1.2.4; second role"
        )
        record = CHECKER.Record(TIMESTAMP, (first, second), None)
        rendered = CHECKER.normalize(
            f"Last revised (UTC): {TIMESTAMP}\n"
            "Model: same-model; effort=high\n"
            f"Agent/runtime: {first.runtime}\n"
            "Model: same-model; effort=high\n"
            f"Agent/runtime: {second.runtime}\n"
        )
        with (
            mock.patch.object(CHECKER, "validate_pdf_info"),
            mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
        ):
            CHECKER.validate_rendered_record(Path("unused.pdf"), record)


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("pdflatex", "pdfinfo", "pdftotext")),
    "TeX and Poppler tools are required",
)
class ReproduciblePdfMetadataTests(unittest.TestCase):
    def compile(self, source: Path, output: Path, environment: dict[str, str]) -> Path:
        output.mkdir()
        command = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-jobname=document",
            f"-output-directory={output}",
            str(source),
        ]
        for _ in range(2):
            result = subprocess.run(
                command,
                cwd=source.parent,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return output / "document.pdf"

    def test_tracked_moddate_has_no_clock_fields_and_rebuild_is_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            source = temporary_path / "main.tex"
            source.write_text(
                rf"\input{{{(ROOT / 'src/gpt/common/preamble.tex').as_posix()}}}"
                "\n"
                r"\hypersetup{pdftitle={Reproducibility test},pdfsubject={Metadata test}}"
                "\n"
                r"\begin{document}"
                "\nTest\n"
                + rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
                + "\n"
                + CONTRIBUTION
                + "\n"
                + r"\end{document}"
                + "\n",
                encoding="utf-8",
            )

            first_environment = os.environ.copy()
            first_environment.update(
                TZ="Pacific/Honolulu",
                SOURCE_DATE_EPOCH="123456789",
                FORCE_SOURCE_DATE="1",
            )
            second_environment = os.environ.copy()
            second_environment.update(
                TZ="Europe/Warsaw",
                SOURCE_DATE_EPOCH="1893456000",
                FORCE_SOURCE_DATE="1",
            )
            first = self.compile(source, temporary_path / "first", first_environment)
            second = self.compile(source, temporary_path / "second", second_environment)

            first_bytes = first.read_bytes()
            self.assertEqual(
                hashlib.sha256(first_bytes).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )
            CHECKER.validate_pdf_info(first, TIMESTAMP)
            rendered = CHECKER.pdf_text(first)
            self.assertEqual(rendered.count(f"Last revised (UTC): {TIMESTAMP}"), 1)
            self.assertIsNone(re.search(rb"/ID\s*\[", first_bytes))


if __name__ == "__main__":
    unittest.main()
