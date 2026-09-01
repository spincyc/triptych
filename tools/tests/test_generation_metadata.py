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
CHECKER_PATH = ROOT / "tools" / "check-generation-metadata"
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
SECOND_CONTRIBUTION = (
    r"\AIModelContribution{test-model}{effort=high}"
    r"{OpenAI Codex CLI 1.2.4; API workspace; review role}"
)
CLAUDE_RUNTIME = (
    "Anthropic Claude Code agent; Claude Code CLI 2.1.219; "
    "unexposed: server revision"
)
PROVENANCE = (
    r"\AIGenerationProvenance"
    r"{unknown}{unknown}{unknown}{unknown}{unknown}{unknown}"
)
RECORDED_PROVENANCE = (
    r"\AIGenerationProvenance{proper}{11}"
    r"{" + "a" * 64 + r"}{" + "b" * 16 + r"}{" + "c" * 40 + r"}{" + "d" * 40 + r"}"
)
# What every record in this file states about its production unless the test is
# about production: nothing was recoverable.
NOTHING_RECOVERABLE = None


class GenerationMetadataParserTests(unittest.TestCase):
    def parse(self, text: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "generation-metadata.tex"
            path.write_text(text, encoding="utf-8")
            return CHECKER.parse_record(path)

    def test_accepts_canonical_and_inherited_records(self) -> None:
        canonical = self.parse(
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE + "\n" + CONTRIBUTION + "\n"
        )
        self.assertEqual(canonical.revision_timestamp, TIMESTAMP)
        self.assertEqual(len(canonical.contributions), 1)
        self.assertIsNone(canonical.inheritance)

        inherited = self.parse(
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE + "\n"
            + r"\AIInheritedGenerationMetadata{theology/sacraments}"
            + "\n"
        )
        self.assertEqual(inherited.revision_timestamp, TIMESTAMP)
        self.assertEqual(inherited.inheritance, "theology/sacraments")
        self.assertFalse(inherited.contributions)

    def test_rejects_missing_duplicate_and_noninitial_timestamp(self) -> None:
        cases = {
            "missing": PROVENANCE + "\n" + CONTRIBUTION + "\n",
            "duplicate": (
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
                rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
                + PROVENANCE
                + "\n"
                + CONTRIBUTION
                + "\n"
            ),
            "noninitial": (
                CONTRIBUTION
                + "\n"
                + rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
                + "\n"
                + PROVENANCE
                + "\n"
            ),
        }
        for label, text in cases.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                self.parse(text)

    def test_rejects_inheritance_mixed_with_contribution_and_stray_text(self) -> None:
        mixed = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE + "\n"
            + r"\AIInheritedGenerationMetadata{theology/sacraments}"
            + "\n"
            + CONTRIBUTION
            + "\n"
        )
        stray = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE + "\n"
            + CONTRIBUTION
            + "\nnot structured\n"
        )
        for text in (mixed, stray):
            with self.assertRaises(ValueError):
                self.parse(text)

    def test_rejects_exact_duplicate_contribution(self) -> None:
        text = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE
            + "\n"
            + CONTRIBUTION
            + "\n"
            + CONTRIBUTION
            + "\n"
        )
        with self.assertRaisesRegex(ValueError, "exact duplicate model contribution"):
            self.parse(text)

    def test_rejects_noncontiguous_model_group(self) -> None:
        other = (
            r"\AIModelContribution{other-model}{effort=medium}"
            r"{OpenAI Codex CLI 1.2.3; API workspace; other role}"
        )
        text = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n"
            + PROVENANCE
            + "\n"
            + CONTRIBUTION
            + "\n"
            + other
            + "\n"
            + SECOND_CONTRIBUTION
            + "\n"
        )
        with self.assertRaisesRegex(ValueError, "noncontiguous model and qualifier"):
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

    def test_accepts_claude_contribution_with_conforming_runtime(self) -> None:
        CHECKER.validate_contribution(
            CHECKER.Contribution(
                "claude-fable-5", "unexposed: numeric qualifiers", CLAUDE_RUNTIME
            )
        )

    def test_rejects_claude_runtime_missing_cli_version(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires runtime component"):
            CHECKER.validate_contribution(
                CHECKER.Contribution(
                    "claude-fable-5",
                    "unexposed: numeric qualifiers",
                    "Anthropic Claude Code agent; unexposed: server revision",
                )
            )

    def test_rejects_generic_claude_family_labels(self) -> None:
        generic = (
            "claude",
            "Claude",
            "claude 4",
            "claude-4.5",
            "claude-fable",
            "claude opus",
            "Claude Mythos",
        )
        for model in generic:
            with self.subTest(model=model), self.assertRaisesRegex(
                ValueError, "generic or unavailable"
            ):
                CHECKER.validate_contribution(
                    CHECKER.Contribution(
                        model, "unexposed: numeric qualifiers", CLAUDE_RUNTIME
                    )
                )
        self.assertIsNone(CHECKER.GENERIC_MODEL_RE.search("claude-fable-5"))

    def test_handwritten_revision_label_is_rejected_as_legacy(self) -> None:
        self.assertRegex(r"\textbf{Last revised (UTC):}", CHECKER.LEGACY_LABEL_RE)

    def test_rejects_standalone_generation_metadata_wrapper_headings(self) -> None:
        headings = (
            r"\section{Generation Metadata}",
            r"\section*{AI Generation Metadata}",
            r"\chapter{Generation Metadata}",
            r"\addcontentsline{toc}{section}{Generation Metadata}",
            r"\noindent{\small\bfseries Generation Metadata\par}",
            r"\noindent\textbf{Generation Metadata}\par",
        )
        for heading in headings:
            with (
                self.subTest(heading=heading),
                self.assertRaisesRegex(ValueError, "wrapper heading"),
            ):
                CHECKER.validate_source_metadata_display(heading)

    def test_allows_metadata_input_without_a_wrapper_heading(self) -> None:
        CHECKER.validate_source_metadata_display(
            r"\input{articles/faith/example/generation-metadata}"
        )

    def test_rendered_record_keeps_contributions_audit_only(self) -> None:
        first = CHECKER.Contribution(
            "same-model", "effort=high", "OpenAI Codex CLI 1.2.3; first role"
        )
        second = CHECKER.Contribution(
            "same-model", "effort=high", "OpenAI Codex CLI 1.2.4; second role"
        )
        record = CHECKER.Record(TIMESTAMP, (first, second), None, NOTHING_RECOVERABLE)
        rendered = CHECKER.normalize(
            f"Last revised (UTC): {TIMESTAMP}\n"
        )
        with (
            mock.patch.object(CHECKER, "validate_pdf_info"),
            mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
        ):
            CHECKER.validate_rendered_record(Path("unused.pdf"), record)

        exposed = CHECKER.normalize(
            f"Last revised (UTC): {TIMESTAMP}\n"
            "Model: same-model; effort=high\n"
        )
        with (
            mock.patch.object(CHECKER, "validate_pdf_info"),
            mock.patch.object(CHECKER, "pdf_text", return_value=exposed),
            self.assertRaisesRegex(ValueError, "tracked model"),
        ):
            CHECKER.validate_rendered_record(Path("unused.pdf"), record)

    def test_rendered_record_rejects_runtime_and_process_ledger_fields(self) -> None:
        contribution = CHECKER.Contribution(
            "test-model", "effort=high", "OpenAI Codex CLI 1.2.3; first role"
        )
        record = CHECKER.Record(TIMESTAMP, (contribution,), None, NOTHING_RECOVERABLE)
        cases = (
            f"Agent/runtime: {contribution.runtime}",
            f"Client/runtime: {contribution.runtime}",
            "Agent instance: reviewer",
            "Contribution count: 1",
            "Process ledger: drafting and review",
            contribution.runtime,
        )
        for ledger in cases:
            rendered = CHECKER.normalize(
                f"Last revised (UTC): {TIMESTAMP}\n"
                f"{ledger}\n"
            )
            with (
                self.subTest(ledger=ledger),
                mock.patch.object(CHECKER, "validate_pdf_info"),
                mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
                self.assertRaisesRegex(
                    ValueError, "production-ledger|agent/runtime record"
                ),
            ):
                CHECKER.validate_rendered_record(Path("unused.pdf"), record)

    def test_rendered_record_rejects_model_identity_and_effort(self) -> None:
        first = CHECKER.Contribution(
            "first-model", "effort=high", "OpenAI Codex CLI 1.2.3; first role"
        )
        second = CHECKER.Contribution(
            "second-model", "effort=low", "OpenAI Codex CLI 1.2.4; second role"
        )
        record = CHECKER.Record(TIMESTAMP, (first, second), None, NOTHING_RECOVERABLE)
        for exposed in ("first-model", "effort=high"):
            rendered = CHECKER.normalize(
                f"Last revised (UTC): {TIMESTAMP}\n{exposed}\n"
            )
            with (
                self.subTest(exposed=exposed),
                mock.patch.object(CHECKER, "validate_pdf_info"),
                mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
                self.assertRaisesRegex(ValueError, "tracked model|model effort"),
            ):
                CHECKER.validate_rendered_record(Path("unused.pdf"), record)

    def test_inherited_render_rejects_duplicated_model_or_ledger(self) -> None:
        record = CHECKER.Record(TIMESTAMP, (), "theology/sacraments", NOTHING_RECOVERABLE)
        inherited = CHECKER.Record(
            TIMESTAMP,
            (
                CHECKER.Contribution(
                    "test-model",
                    "effort=high",
                    "OpenAI Codex CLI 1.2.3; inherited role",
                ),
            ),
            None,
            NOTHING_RECOVERABLE,
        )
        for field in ("Model: test-model; effort=high", "Agent/runtime: hidden"):
            rendered = CHECKER.normalize(
                f"Last revised (UTC): {TIMESTAMP}\n{field}\n"
            )
            with (
                self.subTest(field=field),
                mock.patch.object(CHECKER, "validate_pdf_info"),
                mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
                self.assertRaises(ValueError),
            ):
                CHECKER.validate_rendered_record(
                    Path("unused.pdf"), record, inherited
                )

    def test_rendered_record_allows_ordinary_pedagogical_model_heading(self) -> None:
        record = CHECKER.Record(TIMESTAMP, (), "theology/sacraments", NOTHING_RECOVERABLE)
        inherited = CHECKER.Record(
            TIMESTAMP,
            (
                CHECKER.Contribution(
                    "test-model",
                    "effort=high",
                    "OpenAI Codex CLI 1.2.3; inherited role",
                ),
            ),
            None,
            NOTHING_RECOVERABLE,
        )
        rendered = CHECKER.normalize(
            f"Last revised (UTC): {TIMESTAMP}\n"
            "Model: practice the first sentence before continuing.\n"
        )
        with (
            mock.patch.object(CHECKER, "validate_pdf_info"),
            mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
        ):
            CHECKER.validate_rendered_record(
                Path("unused.pdf"), record, inherited
            )


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
            preamble = next(
                path
                for path in (
                    ROOT / "src/common/preamble.tex",
                    ROOT / "src/gpt/common/preamble.tex",
                )
                if path.is_file()
            )
            source.write_text(
                rf"\input{{{preamble.as_posix()}}}"
                "\n"
                r"\hypersetup{pdftitle={Reproducibility test},pdfsubject={Metadata test}}"
                "\n"
                r"\begin{document}"
                "\nTest\n"
                + rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
                + "\n"
                + RECORDED_PROVENANCE
                + "\n"
                + CONTRIBUTION
                + "\n"
                + SECOND_CONTRIBUTION
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
            CHECKER.validate_rendered_record(
                first,
                CHECKER.Record(
                    TIMESTAMP,
                    (
                        CHECKER.Contribution(
                            "test-model",
                            "effort=high",
                            "OpenAI Codex CLI 1.2.3; API workspace",
                        ),
                        CHECKER.Contribution(
                            "test-model",
                            "effort=high",
                            "OpenAI Codex CLI 1.2.4; API workspace; review role",
                        ),
                    ),
                    None,
                    NOTHING_RECOVERABLE,
                ),
            )
            rendered = CHECKER.pdf_text(first)
            self.assertEqual(rendered.count(f"Last revised (UTC): {TIMESTAMP}"), 1)
            self.assertNotIn("Model:", rendered)
            self.assertNotIn("test-model", rendered)
            self.assertNotIn("effort=high", rendered)
            self.assertNotIn("Agent/runtime:", rendered)
            self.assertNotIn("OpenAI Codex CLI 1.2.3; API workspace", rendered)
            self.assertNotIn(
                "OpenAI Codex CLI 1.2.4; API workspace; review role", rendered
            )
            # The production record is tracked and never printed.
            self.assertNotIn("proper", rendered)
            for value in ("a" * 64, "b" * 16, "c" * 40, "d" * 40):
                self.assertNotIn(value, rendered)
            self.assertIsNone(re.search(rb"/ID\s*\[", first_bytes))



class ProductionRecordTests(unittest.TestCase):
    """What produced a document, and the ways that record could lie."""

    def parse(self, text: str):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "generation-metadata.tex"
            path.write_text(text, encoding="utf-8")
            return CHECKER.parse_record(path)

    def record(self, provenance: str) -> str:
        return (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
            + "\n"
            + provenance
            + "\n"
            + CONTRIBUTION
            + "\n"
        )

    def test_unknown_reads_back_as_absence_and_a_value_as_itself(self) -> None:
        nothing = self.parse(self.record(PROVENANCE)).production
        self.assertEqual(
            (
                nothing.workflow_id,
                nothing.workflow_version,
                nothing.workflow_digest,
                nothing.run_id,
                nothing.seed_commit,
                nothing.install_commit,
            ),
            (None,) * 6,
        )
        self.assertFalse(nothing.recorded)

        stated = self.parse(self.record(RECORDED_PROVENANCE)).production
        self.assertEqual(stated.workflow_id, "proper")
        self.assertEqual(stated.workflow_version, "11")
        self.assertEqual(stated.workflow_digest, "a" * 64)
        self.assertEqual(stated.run_id, "b" * 16)
        self.assertEqual(stated.seed_commit, "c" * 40)
        self.assertEqual(stated.install_commit, "d" * 40)
        self.assertTrue(stated.recorded)

    def test_the_record_is_required_and_stands_second(self) -> None:
        missing = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
            + "\n"
            + CONTRIBUTION
            + "\n"
        )
        with self.assertRaisesRegex(ValueError, "exactly one generation-provenance"):
            self.parse(missing)

        twice = self.record(PROVENANCE).replace(
            PROVENANCE + "\n", PROVENANCE + "\n" + PROVENANCE + "\n"
        )
        with self.assertRaisesRegex(ValueError, "exactly one generation-provenance"):
            self.parse(twice)

        after = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
            + "\n"
            + CONTRIBUTION
            + "\n"
            + PROVENANCE
            + "\n"
        )
        with self.assertRaisesRegex(ValueError, "must follow the document revision"):
            self.parse(after)

    def test_every_field_is_held_to_its_own_shape(self) -> None:
        cases = {
            "workflow_id": "Proper",
            "workflow_version": "v11",
            "workflow_digest": "a" * 63,
            "run_id": "b" * 40,
            "seed_commit": "c" * 16,
            "install_commit": "not-a-commit",
        }
        for field, value in cases.items():
            fields = {name: None for name, _ in CHECKER.PRODUCTION_FIELD_PATTERNS}
            fields["workflow_id"] = "proper"
            fields[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, f"generation provenance {field}"
            ):
                CHECKER.validate_production(CHECKER.Production(**fields))

    def test_a_run_fact_may_not_be_carried_without_its_workflow(self) -> None:
        """A digest or a run id with no workflow names a provenance nobody can check."""
        for field, value in (
            ("workflow_version", "11"),
            ("workflow_digest", "a" * 64),
            ("run_id", "b" * 16),
            ("seed_commit", "c" * 40),
        ):
            fields = {name: None for name, _ in CHECKER.PRODUCTION_FIELD_PATTERNS}
            fields[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "no workflow it belongs to"
            ):
                CHECKER.validate_production(CHECKER.Production(**fields))
        # An install commit is a fact about this repository and not about a run,
        # so it stands on its own. Every backfilled document in the corpus is
        # exactly this shape.
        alone = {name: None for name, _ in CHECKER.PRODUCTION_FIELD_PATTERNS}
        alone["install_commit"] = "d" * 40
        CHECKER.validate_production(CHECKER.Production(**alone))

    def test_a_production_value_reaching_the_page_is_refused(self) -> None:
        production = CHECKER.Production(
            "proper", "11", "a" * 64, "b" * 16, "c" * 40, "d" * 40
        )
        record = CHECKER.Record(TIMESTAMP, (), "theology/sacraments", production)
        inherited = CHECKER.Record(
            TIMESTAMP,
            (CHECKER.Contribution("test-model", "effort=high", CLAUDE_RUNTIME),),
            None,
            NOTHING_RECOVERABLE,
        )
        for leaked in ("a" * 64, "b" * 16, "c" * 40, "d" * 40):
            rendered = CHECKER.normalize(
                f"Last revised (UTC): {TIMESTAMP}\nRun {leaked}\n"
            )
            with (
                self.subTest(leaked=leaked[:8]),
                mock.patch.object(CHECKER, "validate_pdf_info"),
                mock.patch.object(CHECKER, "pdf_text", return_value=rendered),
                self.assertRaisesRegex(ValueError, "generation-provenance"),
            ):
                CHECKER.validate_rendered_record(
                    Path("unused.pdf"), record, inherited
                )

    def test_the_whole_corpus_records_what_produced_it(self) -> None:
        """Every leaf answers the question, even when the answer is `unknown`."""
        sys.path.insert(0, str(ROOT / "scripts"))
        import _corpus  # noqa: PLC0415

        for document in _corpus.documents(extents=False):
            with self.subTest(document=f"{document.provider}/{document.leaf}"):
                self.assertIsNotNone(document.provenance.produced)


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("pdflatex", "pdfinfo", "pdftotext")),
    "TeX and Poppler tools are required",
)
class ProductionRecordIsInertTests(unittest.TestCase):
    """Backfilling provenance had to leave every accepted PDF byte-identical.

    134 leaves were already reviewed, installed and hash-pinned when this record
    was added, and `installed-pdf-matches-accepted` byte-compares each installed
    PDF against the artifact its review accepted. A record that printed even one
    space would have invalidated all of them at once. So the macro renders
    nothing, and this compiles the same document with and without the record to
    show that nothing is exactly what it renders.
    """

    def compile(self, body: str, where: Path) -> bytes:
        where.mkdir()
        source = where / "main.tex"
        preamble = ROOT / "src/common/preamble.tex"
        source.write_text(
            rf"\input{{{preamble.as_posix()}}}"
            "\n"
            r"\hypersetup{pdftitle={Inertness test},pdfsubject={Inertness test}}"
            "\n"
            r"\begin{document}"
            "\nSome body text, so the page has something to typeset and a rebuild\n"
            "has something to move if anything moves at all.\n"
            "\n" + r"\clearpage" + "\n\n" + body + r"\end{document}" + "\n",
            encoding="utf-8",
        )
        environment = os.environ.copy()
        environment.update(
            TZ="UTC", SOURCE_DATE_EPOCH="1000000000", FORCE_SOURCE_DATE="1"
        )
        for _ in range(2):
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-jobname=document",
                    f"-output-directory={where}",
                    str(source),
                ],
                cwd=where,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return (where / "document.pdf").read_bytes()

    def test_adding_the_record_moves_no_byte_of_the_rendered_pdf(self) -> None:
        without = (
            rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
            + "\n"
            + CONTRIBUTION
            + "\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            before = self.compile(without, root / "before")
            after = self.compile(
                without.replace(
                    rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}" + "\n",
                    rf"\AIDocumentRevisionTimestamp{{{TIMESTAMP}}}"
                    + "\n"
                    + RECORDED_PROVENANCE
                    + "\n",
                ),
                root / "after",
            )
        self.assertEqual(
            hashlib.sha256(before).hexdigest(), hashlib.sha256(after).hexdigest()
        )

    def test_the_macro_that_carries_the_record_typesets_nothing(self) -> None:
        """The mechanism, stated where a reader of the preamble will find it."""
        preamble = (ROOT / "src/common/preamble.tex").read_text(encoding="utf-8")
        self.assertIn(
            r"\newcommand{\AIGenerationProvenance}[6]{\ignorespaces}", preamble
        )


if __name__ == "__main__":
    unittest.main()
