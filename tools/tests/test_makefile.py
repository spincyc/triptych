#!/usr/bin/env python3
"""Focused regression tests for the PDF build and validation graph."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class MakefileBuildGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copy2(REPOSITORY_ROOT / "Makefile", self.root / "Makefile")
        shutil.copy2(
            REPOSITORY_ROOT / "requirements-public-alpha.txt",
            self.root / "requirements-public-alpha.txt",
        )

        (self.root / "src/gpt/common").mkdir(parents=True)
        (self.root / "src/gpt/common/preamble.tex").write_text(
            "% shared render dependency\n", encoding="utf-8"
        )
        curriculum_shared = (
            self.root / "src/gpt/curriculums/ecclesiastical-latin/shared"
        )
        curriculum_shared.mkdir(parents=True)
        (curriculum_shared / "course-format.sty").write_text(
            "% curriculum-wide render dependency\n", encoding="utf-8"
        )
        curriculum_research = (
            self.root / "src/gpt/curriculums/ecclesiastical-latin/research"
        )
        curriculum_research.mkdir()
        (curriculum_research / "curriculum-map.md").write_text(
            "# Fake curriculum map\n", encoding="utf-8"
        )
        for document in ("demo-a", "demo-b"):
            leaf = self.root / "src/gpt" / document
            (leaf / "research").mkdir(parents=True)
            (leaf / "main.tex").write_text("\\input{body}\n", encoding="utf-8")
            (leaf / "body.tex").write_text(f"{document}\n", encoding="utf-8")
            (leaf / "generation-metadata.tex").write_text(
                "metadata\n", encoding="utf-8"
            )
            (leaf / "research/notes.md").write_text("notes\n", encoding="utf-8")

        scripts = self.root / "scripts"
        scripts.mkdir()
        library = self.root / "tools"
        library.mkdir(parents=True)
        (self.root / "tools" / "tests").mkdir()
        (self.root / "tools/tests/test_curriculum_liturgical_rights.py").write_text(
            """import os
import unittest


class CurriculumLiturgicalRightsTests(unittest.TestCase):
    def test_gate_was_invoked(self):
        with open(os.environ["MAKE_TEST_CURRICULUM_RIGHTS_LOG"], "a", encoding="utf-8") as log:
            log.write("check\\n")
""",
            encoding="utf-8",
        )
        launcher = self.root / "tools" / "tpt"
        launcher.write_text(
            """#!/usr/bin/env python3
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target = os.path.join(root, "tools", sys.argv[1])
if not os.path.exists(target):
    sys.stderr.write("stub tpt: no fake tool for %s\\n" % sys.argv[1])
    raise SystemExit(127)
os.execv(target, [target] + sys.argv[2:])
""",
            encoding="utf-8",
        )
        launcher.chmod(0o755)
        self.checker = library / "check-generation-metadata"
        self.checker.write_text(
            """#!/bin/sh
printf '%s\\n' "$*" >> "$MAKE_TEST_CHECK_LOG"
last=
for argument do
    last=$argument
done
if [ "$3" = --pdf ] && [ ! -f "$last" ]; then
    exit 1
fi
""",
            encoding="utf-8",
        )
        self.checker.chmod(0o755)

        self.structure_checker = library / "check-curriculum-structure"
        self.structure_checker.write_text(
            """#!/usr/bin/env python3
import os
import sys
from pathlib import Path

arguments = sys.argv[1:]
with open(os.environ["MAKE_TEST_STRUCTURE_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(arguments) + "\\n")
if "--sources-only" not in arguments:
    for option in ("--toc", "--out", "--pdf"):
        value = Path(arguments[arguments.index(option) + 1])
        if not value.is_file():
            raise SystemExit(f"missing {option}: {value}")
""",
            encoding="utf-8",
        )
        self.structure_checker.chmod(0o755)

        self.pdf_review = library / "pdf-review"
        self.pdf_review.write_text(
            """#!/usr/bin/env python3
import os
import sys

with open(os.environ["MAKE_TEST_REVIEW_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
""",
            encoding="utf-8",
        )
        self.pdf_review.chmod(0o755)

        self.source_library = library / "source-library"
        self.source_library.write_text(
            """#!/usr/bin/env python3
import os
import sys

with open(os.environ["MAKE_TEST_SOURCE_LIBRARY_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
with open(os.environ["MAKE_TEST_SOURCE_GATE_ORDER_LOG"], "a", encoding="utf-8") as log:
    log.write("library\\n")
""",
            encoding="utf-8",
        )
        self.source_library.chmod(0o755)

        self.source_reader = library / "source-reader"
        self.source_reader.write_text(
            """#!/usr/bin/env python3
import os
import sys

with open(os.environ["MAKE_TEST_SOURCE_READER_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
""",
            encoding="utf-8",
        )
        self.source_reader.chmod(0o755)

        # The deployment-source gate composes these read-only validators.  This
        # build-graph test exercises their ordering and arguments, not their
        # domain implementations, so deterministic no-op stubs are sufficient.
        for tool_name in (
            "document-library",
            "calendar-days",
            "check-calendar-masses",
            "mass-propers",
            "calendar-rubrics",
            "mass-ordinary",
        ):
            fake = library / tool_name
            fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            fake.chmod(0o755)

        self.source_inventory = library / "source-inventory"
        self.source_inventory.write_text(
            """#!/usr/bin/env python3
import os
import sys

with open(os.environ["MAKE_TEST_SOURCE_INVENTORY_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
with open(os.environ["MAKE_TEST_SOURCE_GATE_ORDER_LOG"], "a", encoding="utf-8") as log:
    log.write("inventory\\n")
""",
            encoding="utf-8",
        )
        self.source_inventory.chmod(0o755)

        self.source_family_migration = library / "source-family-migration"
        self.source_family_migration.write_text(
            """#!/usr/bin/env python3
import os
import sys

with open(os.environ["MAKE_TEST_SOURCE_FAMILY_MIGRATION_LOG"], "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
with open(os.environ["MAKE_TEST_SOURCE_GATE_ORDER_LOG"], "a", encoding="utf-8") as log:
    log.write("family\\n")
""",
            encoding="utf-8",
        )
        self.source_family_migration.chmod(0o755)

        self.pdflatex = scripts / "fake-pdflatex"
        self.pdflatex.write_text(
            """#!/bin/sh
printf '%s\\n' "$*" >> "$MAKE_TEST_LATEX_LOG"
printf '%s\\n' "$MAKEFLAGS" >> "$MAKE_TEST_FLAGS_LOG"
output_directory=
job_name=
for argument do
    case "$argument" in
        -output-directory=*) output_directory=${argument#*=} ;;
        -jobname=*) job_name=${argument#*=} ;;
    esac
done
mkdir -p "$output_directory"
printf 'test PDF for %s\\n' "$job_name" > "$output_directory/$job_name.pdf"
: > "$output_directory/$job_name.toc"
: > "$output_directory/$job_name.out"
""",
            encoding="utf-8",
        )
        self.pdflatex.chmod(0o755)

        self.check_log = self.root / "checker.log"
        self.structure_log = self.root / "structure.log"
        self.latex_log = self.root / "latex.log"
        self.flags_log = self.root / "flags.log"
        self.review_log = self.root / "review.log"
        self.source_library_log = self.root / "source-library.log"
        self.source_reader_log = self.root / "source-reader.log"
        self.source_inventory_log = self.root / "source-inventory.log"
        self.source_family_migration_log = self.root / "source-family-migration.log"
        self.source_gate_order_log = self.root / "source-gate-order.log"
        self.curriculum_rights_log = self.root / "curriculum-rights.log"
        self.pacman_log = self.root / "pacman.log"
        self.codex_log = self.root / "codex.log"
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "MAKE_TEST_CHECK_LOG": str(self.check_log),
                "MAKE_TEST_STRUCTURE_LOG": str(self.structure_log),
                "MAKE_TEST_LATEX_LOG": str(self.latex_log),
                "MAKE_TEST_FLAGS_LOG": str(self.flags_log),
                "MAKE_TEST_REVIEW_LOG": str(self.review_log),
                "MAKE_TEST_SOURCE_LIBRARY_LOG": str(self.source_library_log),
                "MAKE_TEST_SOURCE_READER_LOG": str(self.source_reader_log),
                "MAKE_TEST_SOURCE_INVENTORY_LOG": str(self.source_inventory_log),
                "MAKE_TEST_SOURCE_FAMILY_MIGRATION_LOG": str(
                    self.source_family_migration_log
                ),
                "MAKE_TEST_SOURCE_GATE_ORDER_LOG": str(self.source_gate_order_log),
                "MAKE_TEST_CURRICULUM_RIGHTS_LOG": str(
                    self.curriculum_rights_log
                ),
                "MAKE_TEST_PACMAN_LOG": str(self.pacman_log),
                "MAKE_TEST_CODEX_LOG": str(self.codex_log),
                "PATH": f"{scripts}:{self.environment['PATH']}",
                "PDFLATEX": str(self.pdflatex),
            }
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_make(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["make", "--no-print-directory", *arguments],
            cwd=self.root,
            env=self.environment,
            text=True,
            capture_output=True,
            check=False,
        )
        if check and result.returncode:
            self.fail(
                f"make {' '.join(arguments)} failed ({result.returncode})\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    @staticmethod
    def lines(path: Path) -> list[str]:
        if not path.exists():
            return []
        return path.read_text(encoding="utf-8").splitlines()

    def clear_logs(self) -> None:
        self.check_log.write_text("", encoding="utf-8")
        self.structure_log.write_text("", encoding="utf-8")
        self.latex_log.write_text("", encoding="utf-8")
        self.flags_log.write_text("", encoding="utf-8")
        self.review_log.write_text("", encoding="utf-8")
        self.source_library_log.write_text("", encoding="utf-8")
        self.source_reader_log.write_text("", encoding="utf-8")
        self.source_inventory_log.write_text("", encoding="utf-8")
        self.source_family_migration_log.write_text("", encoding="utf-8")
        self.source_gate_order_log.write_text("", encoding="utf-8")
        self.curriculum_rights_log.write_text("", encoding="utf-8")

    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def stamp_fields(path: Path) -> dict[str, str]:
        return dict(line.split("=", 1) for line in path.read_text(encoding="utf-8").splitlines())

    def test_direct_and_default_build_each_validate_a_new_pdf_once(self) -> None:
        self.run_make("build/gpt/demo-a.pdf")
        self.assertEqual(len(self.lines(self.latex_log)), 2)
        self.assertEqual(len(self.lines(self.check_log)), 2)  # global source + local PDF
        build_pdf = self.root / "build/gpt/demo-a.pdf"
        stamp = self.root / "build/gpt/.metadata/demo-a.ok"
        self.assertEqual(
            self.stamp_fields(stamp),
            {
                "schema": "1",
                "provider": "gpt",
                "document": "demo-a",
                "pdf_sha256": self.sha256(build_pdf),
                "validator_sha256": self.sha256(self.checker),
            },
        )

        shutil.rmtree(self.root / "build")
        self.clear_logs()
        result = self.run_make("PDF_JOBS=2")
        self.assertEqual(len(self.lines(self.latex_log)), 4)
        self.assertEqual(len(self.lines(self.check_log)), 3)  # one global + two local
        self.assertTrue(all("-j2" in flags for flags in self.lines(self.flags_log)))
        self.assertNotIn("resetting jobserver", result.stderr)
        self.assertNotIn("jobserver unavailable", result.stderr)
        for document in ("demo-a", "demo-b"):
            self.assertTrue((self.root / f"build/gpt/{document}.pdf").is_file())
            document_pdf = self.root / f"build/gpt/{document}.pdf"
            document_stamp = self.root / f"build/gpt/.metadata/{document}.ok"
            self.assertEqual(
                self.stamp_fields(document_stamp)["pdf_sha256"],
                self.sha256(document_pdf),
            )

        self.clear_logs()
        self.run_make("-j4", "all", "pdf")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 1)

    def test_check_sources_invokes_validation_without_building(self) -> None:
        inventory = self.root / "src/sources/inventories/publications-v1.toml"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text("")
        self.run_make("check-sources")
        self.assertEqual(self.lines(self.curriculum_rights_log), ["check"])
        self.assertEqual(self.lines(self.source_library_log), ["validate"])
        self.assertEqual(self.lines(self.source_reader_log), ["check", "structure --check"])
        self.assertEqual(
            self.lines(self.source_inventory_log),
            [
                "check --review "
                "src/sources/inventories/classification-review-v1.toml "
                "src/sources/inventories/publications-v1.toml"
            ],
        )
        self.assertEqual(self.lines(self.source_family_migration_log), ["check"])
        self.assertEqual(
            self.lines(self.source_gate_order_log),
            ["library", "inventory", "family"],
        )
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(self.lines(self.check_log), [])

    def test_individual_source_gates_keep_completion_screening_explicit(self) -> None:
        self.run_make("check-source-inventory")
        self.run_make("check-source-family-migration")
        self.run_make("check-source-family-screening")
        self.assertEqual(self.lines(self.source_library_log), [])
        self.assertEqual(self.lines(self.source_inventory_log), ["check"])
        self.assertEqual(
            self.lines(self.source_family_migration_log),
            ["check", "check --require-family-screened"],
        )
        self.assertEqual(self.lines(self.latex_log), [])

    def test_clean_review_bootstraps_bounded_jobs_and_reuses_a_jobserver(self) -> None:
        result = self.run_make("review-pdfs", "PDF_JOBS=2")
        self.assertEqual(len(self.lines(self.latex_log)), 4)
        self.assertEqual(len(self.lines(self.check_log)), 3)
        self.assertEqual(len(self.lines(self.review_log)), 1)
        self.assertTrue(all("-j2" in flags for flags in self.lines(self.flags_log)))
        self.assertNotIn("resetting jobserver", result.stderr)
        self.assertNotIn("jobserver unavailable", result.stderr)

        time.sleep(0.02)
        for document in ("demo-a", "demo-b"):
            (self.root / f"src/gpt/{document}/body.tex").write_text(
                f"changed {document}\n", encoding="utf-8"
            )
        self.clear_logs()
        result = self.run_make("-j2", "review-all-pdfs")
        self.assertEqual(len(self.lines(self.latex_log)), 4)
        self.assertEqual(len(self.lines(self.review_log)), 1)
        self.assertTrue(all("-j2" in flags for flags in self.lines(self.flags_log)))
        self.assertNotIn("resetting jobserver", result.stderr)
        self.assertNotIn("jobserver unavailable", result.stderr)

    def test_parallel_all_and_install_share_one_build_graph(self) -> None:
        result = self.run_make("-j4", "all", "install")
        self.assertEqual(len(self.lines(self.latex_log)), 4)
        self.assertEqual(len(self.lines(self.check_log)), 3)
        self.assertNotIn("resetting jobserver", result.stderr)
        self.assertNotIn("jobserver unavailable", result.stderr)
        for document in ("demo-a", "demo-b"):
            self.assertEqual(
                (self.root / f"pdf/gpt/{document}.pdf").read_bytes(),
                (self.root / f"build/gpt/{document}.pdf").read_bytes(),
            )

    def test_research_edits_do_not_build_but_tex_edits_do(self) -> None:
        self.run_make("pdf")
        self.clear_logs()

        notes = self.root / "src/gpt/demo-a/research/notes.md"
        notes.write_text("changed notes\n", encoding="utf-8")
        self.run_make("pdf")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 1)

        self.clear_logs()
        time.sleep(0.02)
        self.checker.write_text(
            self.checker.read_text(encoding="utf-8") + "# validator revision\n",
            encoding="utf-8",
        )
        self.run_make("pdf")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 3)  # global + two PDFs

        self.clear_logs()
        time.sleep(0.02)
        body = self.root / "src/gpt/demo-a/body.tex"
        body.write_text("changed publication\n", encoding="utf-8")
        self.run_make("pdf")
        self.assertEqual(len(self.lines(self.latex_log)), 2)
        self.assertEqual(len(self.lines(self.check_log)), 2)

    def test_curriculum_shared_source_rebuilds_each_dependent_packet(self) -> None:
        for module in ("01-first", "02-second"):
            leaf = (
                self.root
                / "src/gpt/curriculums/ecclesiastical-latin/01-foundations"
                / module
            )
            leaf.mkdir(parents=True)
            (leaf / "main.tex").write_text("\\input{module-data}\n", encoding="utf-8")
            (leaf / "module-data.tex").write_text(f"{module}\n", encoding="utf-8")
            (leaf / "generation-metadata.tex").write_text("metadata\n", encoding="utf-8")

        self.run_make("pdf")
        self.clear_logs()
        time.sleep(0.02)
        shared = (
            self.root
            / "src/gpt/curriculums/ecclesiastical-latin/shared/course-format.sty"
        )
        shared.write_text("% changed curriculum source\n", encoding="utf-8")

        self.run_make("pdf")

        curriculum_jobs = [
            line
            for line in self.lines(self.latex_log)
            if "curriculums/ecclesiastical-latin" in line
        ]
        self.assertEqual(len(curriculum_jobs), 4)
        self.assertEqual(len(self.lines(self.structure_log)), 3)
        self.assertFalse(any("demo-a" in line or "demo-b" in line for line in self.lines(self.latex_log)))

        self.clear_logs()
        self.run_make("check-curriculum-structure")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.structure_log)), 3)
        self.assertTrue(
            all(
                "--toc" in line and "--out" in line and "--pdf" in line
                for line in self.lines(self.structure_log)
                if "--sources-only" not in line
            )
        )

    def test_install_uses_only_validated_builds_and_refreshes_changed_pdf(self) -> None:
        self.run_make("-j4", "install")
        build_pdf = self.root / "build/gpt/demo-a.pdf"
        installed_pdf = self.root / "pdf/gpt/demo-a.pdf"
        self.assertEqual(installed_pdf.read_bytes(), build_pdf.read_bytes())

        time.sleep(0.02)
        build_pdf.write_bytes(b"externally replaced PDF\n")
        self.clear_logs()
        self.run_make("install")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 2)  # global + changed PDF
        self.assertEqual(installed_pdf.read_bytes(), build_pdf.read_bytes())

    def test_altar_server_single_install_routes_through_complete_series_gate(self) -> None:
        owner = (
            self.root
            / "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides"
        )
        shared = owner / "shared"
        shared.mkdir(parents=True)
        (shared / "series-format.tex").write_text(
            "% shared altar-server render source\n", encoding="utf-8"
        )
        documents = (
            "01-low-mass",
            "01-low-mass-trainer-manual",
            "01-low-mass-flash-cards",
            "02-missa-cantata",
            "02-missa-cantata-cue-cards",
            "03-solemn-mass",
            "03-solemn-mass-cue-cards",
        )
        for document in documents:
            leaf = owner / document
            leaf.mkdir()
            (leaf / "main.tex").write_text(
                "\\input{series-format}\n", encoding="utf-8"
            )
            (leaf / "generation-metadata.tex").write_text(
                "metadata\n", encoding="utf-8"
            )

        requested = (
            "liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass"
        )
        self.run_make("install-doc", f"DOC={requested}")

        altar_jobs = [
            line
            for line in self.lines(self.latex_log)
            if "altar-server-guides" in line
        ]
        self.assertEqual(len(altar_jobs), 14)
        self.assertEqual(len(self.lines(self.review_log)), 1)
        reviewed = self.lines(self.review_log)[0]
        for document in documents:
            relative = (
                "liturgy/roman-rite/1962/reference/altar-server-guides/"
                f"{document}.pdf"
            )
            self.assertIn(f"build/gpt/{relative}", reviewed)
            self.assertEqual(
                (self.root / f"pdf/gpt/{relative}").read_bytes(),
                (self.root / f"build/gpt/{relative}").read_bytes(),
            )

        self.clear_logs()
        time.sleep(0.02)
        (shared / "series-format.tex").write_text(
            "% revised shared altar-server render source\n", encoding="utf-8"
        )
        self.run_make("altar-server-guides")
        altar_jobs = [
            line
            for line in self.lines(self.latex_log)
            if "altar-server-guides" in line
        ]
        self.assertEqual(len(altar_jobs), 14)

    def test_checker_refresh_does_not_reinstall_identical_pdf_bytes(self) -> None:
        self.run_make("-j4", "install")
        installed_pdfs = [
            self.root / f"pdf/gpt/{document}.pdf"
            for document in ("demo-a", "demo-b")
        ]
        installed_mtimes = [pdf.stat().st_mtime_ns for pdf in installed_pdfs]

        time.sleep(0.02)
        self.checker.write_text(
            self.checker.read_text(encoding="utf-8") + "# validator revision\n",
            encoding="utf-8",
        )
        self.clear_logs()
        self.run_make("install")

        self.assertEqual(len(self.lines(self.check_log)), 3)  # global + two PDFs
        self.assertEqual(
            [pdf.stat().st_mtime_ns for pdf in installed_pdfs], installed_mtimes
        )

    def test_old_mtime_pdf_replacement_cannot_bypass_validation(self) -> None:
        self.run_make("pdf")
        build_pdf = self.root / "build/gpt/demo-a.pdf"
        stamp = self.root / "build/gpt/.metadata/demo-a.ok"
        original_stat = build_pdf.stat()
        self.assertLess(original_stat.st_mtime_ns, stamp.stat().st_mtime_ns)

        build_pdf.write_bytes(b"unvalidated replacement with restored timestamp\n")
        os.utime(
            build_pdf,
            ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns),
        )
        self.clear_logs()
        result = self.run_make("install", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Validation stamp does not match current PDF/checker", result.stderr)
        self.assertFalse((self.root / "pdf/gpt/demo-a.pdf").exists())
        self.assertEqual(len(self.lines(self.check_log)), 1)  # global source only

    def test_legacy_empty_stamp_is_revalidated_and_migrated(self) -> None:
        self.run_make("pdf")
        build_pdf = self.root / "build/gpt/demo-a.pdf"
        stamp = self.root / "build/gpt/.metadata/demo-a.ok"
        stamp.write_bytes(b"")
        self.clear_logs()

        self.run_make("pdf")

        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 2)  # global + migrated PDF
        self.assertEqual(
            self.stamp_fields(stamp),
            {
                "schema": "1",
                "provider": "gpt",
                "document": "demo-a",
                "pdf_sha256": self.sha256(build_pdf),
                "validator_sha256": self.sha256(self.checker),
            },
        )

    def test_pdf_replaced_during_copy_is_not_installed(self) -> None:
        self.run_make("pdf")
        mutating_install = self.root / "tools/tests/mutating-install"
        mutating_install.write_text(
            """#!/bin/sh
printf 'replacement during copy\\n' > "$3"
cp "$3" "$4"
chmod 0644 "$4"
""",
            encoding="utf-8",
        )
        mutating_install.chmod(0o755)
        self.clear_logs()

        result = self.run_make(
            "pdf/gpt/demo-a.pdf",
            f"INSTALL={mutating_install}",
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PDF or metadata checker changed during install", result.stderr)
        self.assertFalse((self.root / "pdf/gpt/demo-a.pdf").exists())
        self.assertEqual(
            list((self.root / "pdf/gpt").glob("demo-a.pdf.tmp.*")), []
        )

    def test_empty_parallel_limit_fails_closed(self) -> None:
        for arguments in (
            ("PDF_JOBS=",),
            ("PDF_JOBS=bad",),
            ("PDF_JOBS=bad", "_triptych_make_strip_decimal="),
            ("PDF_JOBS=bad", "_TRIPTYCH_PDF_JOBS_INVALID="),
            ("PDF_JOBS=bad", "_TRIPTYCH_MAKE_PARALLEL_FLAGS=-j"),
        ):
            with self.subTest(arguments=arguments):
                result = self.run_make(*arguments, check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("requires a positive integer", result.stderr)

    def test_arch_dependency_target_uses_one_canonical_pacman_transaction(self) -> None:
        os_release = self.root / "arch-os-release"
        os_release.write_text('ID=arch\nNAME="Arch Linux"\n', encoding="utf-8")
        pacman = self.root / "fake-pacman"
        pacman.write_text(
            """#!/bin/sh
printf '%s\\n' "$@" > "$MAKE_TEST_PACMAN_LOG"
""",
            encoding="utf-8",
        )
        pacman.chmod(0o755)
        sudo = self.root / "fake-sudo"
        sudo.write_text(
            """#!/bin/sh
if [ "$1" = -- ]; then
    shift
fi
exec "$@"
""",
            encoding="utf-8",
        )
        sudo.chmod(0o755)
        shadow_bin = self.root / "shadow-bin"
        shadow_bin.mkdir()
        for name in ("codex", "gh", "rg"):
            executable = shadow_bin / name
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            executable.chmod(0o755)
        fake_id = shadow_bin / "id"
        fake_id.write_text(
            """#!/bin/sh
if [ "$1" = -u ]; then
    printf '1000\\n'
    exit 0
fi
exec /usr/bin/id "$@"
""",
            encoding="utf-8",
        )
        fake_id.chmod(0o755)
        self.environment["PATH"] = f"{shadow_bin}:{self.environment['PATH']}"

        listed = self.run_make("dependencies-arch").stdout.splitlines()
        install_arguments = (
            "install-dependencies-arch",
            f"ARCH_OS_RELEASE={os_release}",
            f"ARCH_PACMAN={pacman}",
            f"ARCH_SUDO={sudo}",
            f"ARCH_ID={fake_id}",
        )
        dry_run = self.run_make("-n", *install_arguments)
        self.assertIn(str(pacman), dry_run.stdout)
        self.assertIn(str(sudo), dry_run.stdout)
        self.assertIn(str(fake_id), dry_run.stdout)
        self.assertNotIn("/usr/bin/pacman", dry_run.stdout)
        self.assertNotIn("/usr/bin/sudo", dry_run.stdout)
        result = self.run_make(*install_arguments)
        arguments = self.lines(self.pacman_log)
        expected_packages = [
            "make",
            "bash",
            "findutils",
            "coreutils",
            "diffutils",
            "python",
            "tzdata",
            "python-markdown",
            "python-yaml",
            "texlive-bin",
            "texlive-basic",
            "texlive-latex",
            "texlive-latexrecommended",
            "texlive-latexextra",
            "texlive-pictures",
            "texlive-fontsrecommended",
            "texlive-fontsextra",
            "poppler",
            "imagemagick",
            "pandoc",
            "nodejs",
            "git",
            "github-cli",
            "openai-codex",
            "ripgrep",
        ]

        self.assertEqual(arguments[:2], ["-Syu", "--needed"])
        self.assertEqual(arguments[2:], listed)
        self.assertEqual(listed, expected_packages)
        # `nodejs` was on this list until 2026-08-08 and should not have been:
        # tools/calendar-rubrics spawns `node -e` and tells the operator to
        # install it when absent, so the installer was documented as excluding
        # a package two checks fail without. npm stays excluded because nothing
        # here resolves a package from a registry.
        for excluded in (
            "base-devel",
            "texlive-meta",
            "npm",
            "ghostscript",
            "qpdf",
            # A browser is wanted only by the *_browser.mjs harnesses and is
            # declared by `dependencies-arch-browser`, never installed here.
            "chromium",
            "google-chrome-stable",
        ):
            self.assertNotIn(excluded, listed)
        self.assertNotIn("--noconfirm", arguments)
        self.assertNotIn(".local", " ".join(arguments))
        self.assertIn("shadows canonical /usr/bin/codex", result.stderr)
        self.assertIn("shadows canonical /usr/bin/gh", result.stderr)
        self.assertIn("shadows canonical /usr/bin/rg", result.stderr)

    def test_arch_dependency_install_rejects_other_operating_systems(self) -> None:
        os_release = self.root / "other-os-release"
        os_release.write_text("ID=ubuntu\n", encoding="utf-8")
        pacman = self.root / "must-not-run-pacman"
        pacman.write_text(
            """#!/bin/sh
printf 'unexpected invocation\\n' > "$MAKE_TEST_PACMAN_LOG"
exit 99
""",
            encoding="utf-8",
        )
        pacman.chmod(0o755)

        result = self.run_make(
            "install-dependencies-arch",
            f"ARCH_OS_RELEASE={os_release}",
            f"ARCH_PACMAN={pacman}",
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported host OS: ubuntu", result.stderr)
        self.assertFalse(self.pacman_log.exists())

if __name__ == "__main__":
    unittest.main()
