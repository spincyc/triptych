from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "tools" / "check-web-edition"
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_web_edition_checker", str(CHECKER_PATH)
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {CHECKER_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

DRIVER_PATH = ROOT / "tools" / "web-edition"
DRIVER_LOADER = importlib.machinery.SourceFileLoader(
    "triptych_web_edition_driver", str(DRIVER_PATH)
)
DRIVER_SPEC = importlib.util.spec_from_loader(DRIVER_LOADER.name, DRIVER_LOADER)
if DRIVER_SPEC is None or DRIVER_SPEC.loader is None:
    raise RuntimeError(f"cannot load {DRIVER_PATH}")
DRIVER = importlib.util.module_from_spec(DRIVER_SPEC)
sys.modules[DRIVER_SPEC.name] = DRIVER
DRIVER_SPEC.loader.exec_module(DRIVER)

REVIEWED = "2026-07-25"


def record(leaf: str, **overrides: str) -> str:
    fields: dict[str, str] = {
        "schema": "1",
        "record_type": '"web-edition"',
        "document": f'"{leaf}"',
        "eligibility": '"eligible"',
        "blocking_constructs": "[]",
        "reviewed": f'"{REVIEWED}"',
    }
    fields.update(overrides)
    return "".join(
        f"{key} = {value}\n" for key, value in fields.items() if value is not None
    )


class WebEditionTreeTests(unittest.TestCase):
    """Each test builds a synthetic provider tree in a temporary directory."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "src" / "common").mkdir(parents=True)
        (self.root / "src" / "common" / "preamble.tex").write_text(
            "\\newcommand{\\Nothing}{}\n", encoding="utf-8"
        )
        self.patch = mock.patch.object(CHECKER, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def leaf(self, document: str, provider: str = "gpt") -> Path:
        path = self.root / "src" / provider / document
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_leaf(
        self,
        document: str,
        main: str = "\\input{common/preamble}\n",
        declaration: str | None = None,
        provider: str = "gpt",
        files: dict[str, str] | None = None,
    ) -> Path:
        path = self.leaf(document, provider)
        (path / "main.tex").write_text(main, encoding="utf-8")
        if declaration is not None:
            (path / "web-edition.toml").write_text(declaration, encoding="utf-8")
        for name, text in (files or {}).items():
            target = path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        return path

    def audit(self, document: str, provider: str = "gpt") -> CHECKER.Record:
        return CHECKER.audit_document(self.root / "src" / provider, document)

    def run_main(self, *arguments: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["check-web-edition", *arguments]),
            redirect_stdout(out),
            redirect_stderr(err),
        ):
            status = CHECKER.main()
        return status, out.getvalue(), err.getvalue()

    def test_accepts_eligible_conditional_and_ineligible_records(self) -> None:
        self.write_leaf("articles/faith/plain", declaration=record("articles/faith/plain"))
        self.write_leaf(
            "theology/matrix",
            main="\\begin{landscape}\\end{landscape}\n",
            declaration=record(
                "theology/matrix",
                eligibility='"conditional"',
                basis='"wide-matrix"',
                blocking_constructs='["landscape"]',
                rationale='"A landscape comparative matrix needs a linearized equivalent."',
            ),
        )
        self.write_leaf(
            "liturgy/cards",
            main="\\geometry{letterpaper,margin=0in}\n",
            declaration=record(
                "liturgy/cards",
                eligibility='"ineligible"',
                basis='"duplex-cards"',
                blocking_constructs='["zero-margin-geometry"]',
                rationale='"The card sheet layout is the content."',
            ),
        )
        status, output, errors = self.run_main("--provider", "gpt")
        self.assertEqual(status, 0, errors)
        self.assertIn("1 eligible, 1 conditional, 1 ineligible", output)

    def test_missing_declaration_is_an_error(self) -> None:
        self.write_leaf("articles/faith/undeclared")
        status, _, errors = self.run_main("--provider", "gpt")
        self.assertEqual(status, 1)
        self.assertIn("missing web-edition declaration", errors)

    def test_no_documents_is_an_error(self) -> None:
        status, _, errors = self.run_main("--provider", "absent")
        self.assertEqual(status, 1)
        self.assertIn("no documents found", errors)

    def test_blocking_constructs_are_empty_exactly_when_eligible(self) -> None:
        self.write_leaf(
            "articles/faith/mismatch",
            declaration=record(
                "articles/faith/mismatch", blocking_constructs='["landscape"]'
            ),
        )
        with self.assertRaisesRegex(ValueError, "no blocking construct"):
            self.audit("articles/faith/mismatch")

        self.write_leaf(
            "articles/faith/bare",
            declaration=record(
                "articles/faith/bare",
                eligibility='"conditional"',
                basis='"wide-matrix"',
                rationale='"Needs a linearized matrix."',
            ),
        )
        with self.assertRaisesRegex(ValueError, "must name the blocking construct"):
            self.audit("articles/faith/bare")

    def test_basis_and_rationale_are_required_only_when_not_eligible(self) -> None:
        self.write_leaf(
            "articles/faith/nobasis",
            declaration=record(
                "articles/faith/nobasis",
                eligibility='"conditional"',
                blocking_constructs='["landscape"]',
                rationale='"Needs a linearized matrix."',
            ),
        )
        with self.assertRaisesRegex(ValueError, "requires a basis"):
            self.audit("articles/faith/nobasis")

        self.write_leaf(
            "articles/faith/norationale",
            declaration=record(
                "articles/faith/norationale",
                eligibility='"ineligible"',
                basis='"print-artifact"',
                blocking_constructs='["clearpage-sheet"]',
            ),
        )
        with self.assertRaisesRegex(ValueError, "requires a rationale"):
            self.audit("articles/faith/norationale")

        self.write_leaf(
            "articles/faith/overdeclared",
            declaration=record("articles/faith/overdeclared", basis='"wide-matrix"'),
        )
        with self.assertRaisesRegex(ValueError, "must not declare a basis"):
            self.audit("articles/faith/overdeclared")

    def test_rejects_malformed_schema_type_document_and_date(self) -> None:
        cases = {
            "schema": ({"schema": "2"}, "must declare schema = 1"),
            "record_type": ({"record_type": '"bindings"'}, "record_type"),
            "eligibility": ({"eligibility": '"maybe"'}, "eligibility must be one of"),
            "document": ({"document": '"articles/faith/other"'}, "must match the leaf"),
            "reviewed": ({"reviewed": '"25 July 2026"'}, "must be an ISO date"),
            "calendar": ({"reviewed": '"2026-02-30"'}, "must be an ISO date|invalid"),
            "basis-case": (
                {
                    "eligibility": '"conditional"',
                    "basis": '"Wide Matrix"',
                    "blocking_constructs": '["landscape"]',
                    "rationale": '"Needs a linearized matrix."',
                },
                "kebab-case",
            ),
        }
        for label, (overrides, message) in cases.items():
            with self.subTest(label=label):
                document = f"articles/faith/{label}"
                self.write_leaf(
                    document, declaration=record(document, **overrides)
                )
                with self.assertRaisesRegex(ValueError, message):
                    self.audit(document)

    def test_rejects_unknown_field_and_invalid_toml(self) -> None:
        self.write_leaf(
            "articles/faith/extra",
            declaration=record("articles/faith/extra") + 'converter = "pandoc"\n',
        )
        with self.assertRaisesRegex(ValueError, "unknown field"):
            self.audit("articles/faith/extra")

        self.write_leaf("articles/faith/broken", declaration="schema = \n")
        with self.assertRaisesRegex(ValueError, "not valid TOML"):
            self.audit("articles/faith/broken")

    def test_eligible_leaf_may_not_use_a_blocking_construct(self) -> None:
        constructs = {
            "landscape": "\\begin{landscape}\\end{landscape}",
            "tikzpicture": "\\begin{tikzpicture}\\end{tikzpicture}",
            "multicols": "\\begin{multicols}{2}\\end{multicols}",
            "overlay-picture": "\\begin{tikzpicture}[remember picture,overlay]",
            "zero-margin-geometry": "\\geometry{letterpaper,margin=0in}",
            "rule-line": "\\hrulefill",
            "solutions-enabled": "\\solutionstrue",
        }
        for construct, body in constructs.items():
            with self.subTest(construct=construct):
                document = f"articles/faith/{construct}"
                self.write_leaf(
                    document,
                    main=f"\\input{{common/preamble}}\n{body}\n",
                    declaration=record(document),
                )
                with self.assertRaisesRegex(
                    ValueError, f"declared eligible.*{construct} in "
                ):
                    self.audit(document)

    def test_scan_follows_sections_shared_trees_and_path_macros(self) -> None:
        shared = self.root / "src" / "gpt" / "shared"
        shared.mkdir(parents=True)
        (shared / "matrix.tex").write_text(
            "\\begin{landscape}\\end{landscape}\n", encoding="utf-8"
        )
        self.write_leaf(
            "articles/faith/composed",
            main=(
                "\\input{common/preamble}\n"
                "\\newcommand{\\SharedRoot}{shared}\n"
                "\\input{\\SharedRoot/matrix}\n"
                "\\input{articles/faith/composed/sections/10-body}\n"
            ),
            declaration=record("articles/faith/composed"),
            files={"sections/10-body.tex": "\\begin{tikzpicture}\\end{tikzpicture}\n"},
        )
        with self.assertRaises(ValueError) as raised:
            self.audit("articles/faith/composed")
        message = str(raised.exception)
        self.assertIn("landscape in src/gpt/shared/matrix.tex", message)
        self.assertIn("tikzpicture in src/gpt/articles/faith/composed/sections", message)

    def test_commented_construct_does_not_fail_the_gate(self) -> None:
        self.write_leaf(
            "articles/faith/commented",
            main="\\input{common/preamble}\n% \\begin{landscape}\n",
            declaration=record("articles/faith/commented"),
        )
        self.assertEqual(
            self.audit("articles/faith/commented").eligibility, "eligible"
        )

    def test_provider_defaults_to_the_environment_then_gpt(self) -> None:
        self.write_leaf("articles/faith/plain", declaration=record("articles/faith/plain"))
        self.write_leaf(
            "articles/faith/peer",
            declaration=record("articles/faith/peer"),
            provider="claude",
        )
        with mock.patch.dict("os.environ", {}, clear=True):
            status, output, errors = self.run_main()
        self.assertEqual(status, 0, errors)
        self.assertIn("1 eligible", output)
        with mock.patch.dict("os.environ", {"PROVIDER": "claude"}, clear=True):
            status, output, errors = self.run_main()
        self.assertEqual(status, 0, errors)
        self.assertIn("1 eligible", output)

    def test_single_document_audit(self) -> None:
        self.write_leaf("articles/faith/plain", declaration=record("articles/faith/plain"))
        self.write_leaf("articles/faith/undeclared")
        status, output, _ = self.run_main("--document", "articles/faith/plain")
        self.assertEqual(status, 0)
        self.assertIn("1 eligible", output)

    def test_input_may_not_escape_the_source_root(self) -> None:
        self.assertIsNone(
            CHECKER.resolve_input("../outside", self.root / "src" / "gpt")
        )
        self.assertIsNone(
            CHECKER.resolve_input("/etc/passwd", self.root / "src" / "gpt")
        )


class DriverConversionTests(unittest.TestCase):
    """The converter's silent-loss guards, which no declaration can express."""

    def test_definition_survives_a_comment_between_its_groups(self) -> None:
        preamble = (
            "\\newenvironment{dossiertable}\n"
            "{\\begin{longtable}{ll}\\endhead}\n"
            "% The closing rule is supplied by the final note.\n"
            "{\\end{longtable}}\n"
        )
        self.assertIn("dossiertable", DRIVER.defined_names(
            DRIVER.local_definitions(preamble)
        ))

    def test_a_row_of_empty_cells_fails_the_audit(self) -> None:
        markdown = (
            "Reuse and rights. Last revised (UTC): now\n\n"
            "| A | B |\n|:--|:--|\n| one | two |\n|  |  |\n"
        )
        self.assertIn(
            "1 table row(s) written with every cell empty",
            DRIVER.audit_output("", markdown),
        )

    def test_a_ragged_column_keeps_a_cell_leading_digit(self) -> None:
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")
        document = (
            "\\input{common/preamble}\n"
            "\\hypersetup{pdftitle={T}}\n"
            "\\begin{document}\n"
            "\\begin{longtable}"
            "{>{\\raggedright\\arraybackslash}p{0.4\\linewidth}"
            ">{\\raggedright\\arraybackslash}p{0.4\\linewidth}}\n"
            "\\textbf{A} & \\textbf{B}\\\\\n\\midrule\n\\endhead\n"
            "Epistle & 1~Pet. 5:6--11\\\\\n"
            "\\end{longtable}\n"
            "\\AIDocumentRevisionTimestamp{2026-07-25T00:00:00Z}\n"
            "\\AIModelContribution{m}{q}{r}\n"
            "\\end{document}\n"
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            leaf = root / "src" / "provider" / "doc"
            leaf.mkdir(parents=True)
            (leaf / "main.tex").write_text(document, encoding="utf-8")
            with mock.patch.object(DRIVER, "SRC", root / "src"):
                written = DRIVER.convert("provider", "doc", out=root / "out")
            self.assertIn("| 1", written.read_text(encoding="utf-8"))

    def test_a_headerless_table_keeps_its_empty_header_row(self) -> None:
        markdown = (
            "Reuse and rights. Last revised (UTC): now\n\n"
            "|  |  |\n|:--|:--|\n| one | two |\n"
        )
        self.assertEqual([], DRIVER.audit_output("", markdown))


class TrackedWebEditionRecordTests(unittest.TestCase):
    """The tracked declarations must satisfy the gate they are governed by."""

    def test_every_tracked_gpt_leaf_declares_a_valid_web_edition(self) -> None:
        source_root = ROOT / "src" / "gpt"
        for main in sorted(source_root.rglob("main.tex")):
            document = main.parent.relative_to(source_root).as_posix()
            with self.subTest(document=document):
                CHECKER.audit_document(source_root, document)


if __name__ == "__main__":
    unittest.main()
