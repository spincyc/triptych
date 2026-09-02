from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
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


class ScannedProductionFieldsTests(unittest.TestCase):
    """Which production fields a rendered page can honestly be scanned for.

    Scanning is a substring search over extracted text. It is evidence only
    where a match cannot happen by accident, and two of the six fields are an
    ordinary lowercase word and a small integer. The propers workflow's id is
    `proper`; the word appears on nearly every page of a document about the
    Propers, and scanning for it failed every propers document in the corpus
    while proving nothing. These tests hold the gate to the four fields that
    are evidence and to the two that are not.
    """

    def rendered(self, text: str, record) -> None:
        with (
            mock.patch.object(CHECKER, "validate_pdf_info"),
            mock.patch.object(CHECKER, "pdf_text", return_value=CHECKER.normalize(text)),
        ):
            CHECKER.validate_rendered_record(Path("unused.pdf"), record)

    def test_the_scanned_fields_are_the_high_entropy_ones_and_only_those(self) -> None:
        self.assertEqual(
            CHECKER.SCANNED_PRODUCTION_FIELDS,
            ("workflow_digest", "run_id", "seed_commit", "install_commit"),
        )
        for field in CHECKER.SCANNED_PRODUCTION_FIELDS:
            self.assertIn(field, CHECKER.PRODUCTION_FIELDS)
        for field in ("workflow_id", "workflow_version"):
            self.assertNotIn(field, CHECKER.SCANNED_PRODUCTION_FIELDS)

    def test_an_ordinary_word_workflow_id_on_the_page_is_not_a_leak(self) -> None:
        """`proper` is the workflow's id and also the subject of the document.

        This is the shape of the defect exactly: every value in the record was
        substring-matched against the extracted text, so a document about the
        Propers, produced by the `proper` workflow at version 11, failed its
        own publication gate on the word "proper" and on the number 11.
        """
        record = CHECKER.Record(
            TIMESTAMP,
            (CHECKER.Contribution("test-model", "effort=high", CLAUDE_RUNTIME),),
            None,
            CHECKER.Production("proper", "11", "a" * 64, "b" * 16, "c" * 40, "d" * 40),
        )
        self.rendered(
            f"Last revised (UTC): {TIMESTAMP} The proper of the Mass, in its "
            f"proper order, at Psalm 11 and page 11.",
            record,
        )

    def test_every_scanned_field_is_still_refused_when_it_reaches_the_page(self) -> None:
        values = {
            "workflow_digest": "a" * 64,
            "run_id": "b" * 16,
            "seed_commit": "c" * 40,
            "install_commit": "d" * 40,
        }
        record = CHECKER.Record(
            TIMESTAMP,
            (CHECKER.Contribution("test-model", "effort=high", CLAUDE_RUNTIME),),
            None,
            CHECKER.Production("proper", "11", *values.values()),
        )
        for field, leaked in values.items():
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(ValueError, f"generation-provenance {field}"),
            ):
                self.rendered(f"Last revised (UTC): {TIMESTAMP} Run {leaked}", record)


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("pdfinfo", "pdftotext")),
    "Poppler tools are required",
)
class TheGateOnRealDocumentsTests(unittest.TestCase):
    """Run the gate the pipeline runs, on the documents it runs it against.

    Nothing did this. Every rendered-record test in this file was built from a
    fabricated `Record` and a fabricated page, and each of them passed while
    the real command failed on all thirty-four installed propers documents. A
    gate whose only evidence is a fixture is a gate nobody has run.
    """

    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import _corpus  # noqa: PLC0415

        cls.propers = [
            (document.provider, document.leaf, issue.pdf)
            for document in _corpus.documents(extents=False)
            for issue in document.issues
            if "/propers/" in document.leaf
            and issue.kind == _corpus.FULL
            and issue.pdf
        ]

    def test_the_pdf_gate_passes_on_every_installed_propers_document(self) -> None:
        self.assertTrue(self.propers, "no propers document has an installed PDF")
        for provider, leaf, pdf in self.propers:
            with self.subTest(document=f"{provider}/{leaf}"):
                CHECKER.audit_document(ROOT / "src" / provider, leaf, ROOT / pdf)

    def test_the_command_the_pipeline_runs_exits_zero(self) -> None:
        """The gate as `workflows/pipelines/proper.json` and the Makefile spell it."""
        seen = set()
        for provider, leaf, pdf in self.propers:
            if provider in seen:
                continue
            seen.add(provider)
            with self.subTest(provider=provider):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(CHECKER_PATH),
                        "--provider",
                        provider,
                        "--pdf",
                        leaf,
                        pdf,
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Generation metadata valid", result.stdout)
        self.assertTrue(seen)


class RecordedOriginAgainstRunEvidenceTests(unittest.TestCase):
    """A recorded origin may not be contradicted by the run that produced it.

    `build/tpt-runs/<run-id>/manifest.json` is what the engine wrote when the
    run was seeded: the workflow, its version, its source digest, the seed
    commit, and the arguments naming the document. It is untracked and
    therefore not always present, so this skips rather than fails when it is
    gone — but where it is present it is the primary evidence, and a document's
    own record may not disagree with it.

    This is the check that was missing. One leaf recorded `proper v10` with
    every other field `unknown` while a manifest in the tree named the run that
    produced it at v11, and the version was promoted into a structured fact out
    of prose an earlier pass had written.
    """

    RUNS = ROOT / "build" / "tpt-runs"

    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import _corpus  # noqa: PLC0415

        cls.corpus = _corpus
        cls.manifests = []
        if cls.RUNS.is_dir():
            for path in sorted(cls.RUNS.glob("*/manifest.json")):
                try:
                    cls.manifests.append(json.loads(path.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    continue

    def setUp(self) -> None:
        if not self.manifests:
            self.skipTest("no run manifests are present under build/tpt-runs")

    def test_a_recorded_run_agrees_with_its_manifest_in_every_field(self) -> None:
        by_run = {row["run_id"]: row for row in self.manifests}
        compared = 0
        for document in self.corpus.documents(extents=False):
            produced = document.provenance.produced
            if produced is None or not produced.run_id:
                continue
            manifest = by_run.get(produced.run_id)
            if manifest is None:
                continue
            compared += 1
            with self.subTest(document=f"{document.provider}/{document.leaf}"):
                self.assertEqual(produced.workflow_id, manifest["workflow_id"])
                self.assertEqual(
                    produced.workflow_version, str(manifest["workflow_version"])
                )
                if produced.workflow_digest:
                    self.assertEqual(
                        produced.workflow_digest, manifest["workflow_digest"]
                    )
                if produced.seed_commit:
                    self.assertEqual(produced.seed_commit, manifest["repo_commit"])
                args = manifest.get("normalized_args", {})
                self.assertEqual(args.get("provider"), document.provider)
                self.assertIn(document.leaf, args.values())
        if not compared:
            self.skipTest("no document records a run this tree still holds")

    def test_a_stated_workflow_is_grounded_where_the_run_evidence_exists(self) -> None:
        """Naming a workflow while the tree holds the runs is half an answer.

        A record that states which workflow produced a document, in a tree that
        holds manifests for runs of that workflow against that very document,
        must say which of them it was. Otherwise the version is an assertion
        with evidence sitting beside it that nobody checked it against — which
        is exactly how `v10` came to be recorded for a document a v11 run wrote.
        """
        for document in self.corpus.documents(extents=False):
            produced = document.provenance.produced
            if produced is None or not produced.workflow_id:
                continue
            candidates = [
                row
                for row in self.manifests
                if row.get("workflow_id") == produced.workflow_id
                and row.get("normalized_args", {}).get("provider") == document.provider
                and document.leaf in row.get("normalized_args", {}).values()
            ]
            if not candidates:
                continue
            with self.subTest(document=f"{document.provider}/{document.leaf}"):
                self.assertTrue(
                    produced.run_id,
                    "this tree holds run manifests for this document, so the "
                    "record must name which run produced it rather than "
                    "stating a bare workflow version",
                )
                self.assertIn(
                    produced.run_id,
                    [row["run_id"] for row in candidates],
                    "the recorded run is not one of the runs this tree holds "
                    "for this document",
                )


@unittest.skipUnless(shutil.which("git"), "git is required")
class InstallCommitDerivationTests(unittest.TestCase):
    """The backfilled install commits, and the rule that produced them.

    187 of them were derived from history rather than recorded by the run that
    installed the artifact, and a derivation nobody can rerun is a derivation
    nobody can check. The rule is written out in `scripts/_corpus.py` beside
    the field it produces:

        git log --follow --diff-filter=AM --format=%H -1 -- pdf/<...>.pdf

    which this replays in a single pass over the history of `pdf/` and `doc/`,
    resolving renames itself, so that holding 187 records to it costs one `git
    log` rather than 187 of them.
    """

    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import _corpus  # noqa: PLC0415

        cls.corpus = _corpus
        cls.installs = cls._installs()

    @classmethod
    def _installs(cls) -> dict[str, list[str]]:
        """Every commit that added or modified each installed PDF, latest first.

        `--diff-filter=AMR` keeps renames in the stream so the walk can follow
        a path back through them, and only `A` and `M` entries are recorded as
        installs: a pure rename moves a path without installing anything, which
        is exactly the distinction that decides this derivation. Three commits
        in this history are pure renames of the whole tree — `doc/` to `pdf/`,
        and two renumberings of the propers registries — and without it every
        document in the corpus would name one of them.
        """
        result = subprocess.run(
            ["git", "log", "--format=C %H", "--name-status",
             "--diff-filter=AMR", "-M", "--", "pdf/", "doc/"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if result.returncode:
            raise unittest.SkipTest(f"git log failed: {result.stderr.strip()}")
        # Walked newest first, so `alias` maps the name a path had at this
        # point in history to the name it has today.
        alias: dict[str, str] = {}
        installs: dict[str, list[str]] = {}
        commit = None
        for line in result.stdout.splitlines():
            if line.startswith("C "):
                commit = line[2:].strip()
                continue
            if not line.strip():
                continue
            parts = line.split("\t")
            if parts[0].startswith("R"):
                old, new = parts[1], parts[2]
                alias[old] = alias.pop(new, new)
            else:
                path = parts[1]
                installs.setdefault(alias.get(path, path), []).append(commit)
        return installs

    def test_the_rule_is_written_where_the_field_is_defined(self) -> None:
        rule = (ROOT / "scripts" / "_corpus.py").read_text(encoding="utf-8")
        self.assertIn("--diff-filter=AM", rule)
        self.assertIn("--follow", rule)

    def test_every_recorded_install_commit_is_that_pdf_s_latest_install(self) -> None:
        checked = 0
        for document in self.corpus.documents(extents=False):
            produced = document.provenance.produced
            if produced is None or not produced.install_commit:
                continue
            pdf = next(
                (issue.pdf for issue in document.issues
                 if issue.kind == self.corpus.FULL and issue.pdf),
                None,
            )
            with self.subTest(document=f"{document.provider}/{document.leaf}"):
                self.assertIsNotNone(
                    pdf,
                    "an install commit states where an installed artifact "
                    "entered the tree, so there must be one",
                )
                history = self.installs.get(pdf, [])
                self.assertTrue(history, f"no install of {pdf} is in history")
                self.assertEqual(produced.install_commit, history[0])
            checked += 1
        self.assertEqual(checked, 187)


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
