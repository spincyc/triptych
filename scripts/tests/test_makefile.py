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
        self.checker = scripts / "check-generation-metadata"
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

        self.pdf_review = scripts / "pdf-review"
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
""",
            encoding="utf-8",
        )
        self.pdflatex.chmod(0o755)

        self.check_log = self.root / "checker.log"
        self.latex_log = self.root / "latex.log"
        self.flags_log = self.root / "flags.log"
        self.review_log = self.root / "review.log"
        self.pacman_log = self.root / "pacman.log"
        self.codex_log = self.root / "codex.log"
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "MAKE_TEST_CHECK_LOG": str(self.check_log),
                "MAKE_TEST_LATEX_LOG": str(self.latex_log),
                "MAKE_TEST_FLAGS_LOG": str(self.flags_log),
                "MAKE_TEST_REVIEW_LOG": str(self.review_log),
                "MAKE_TEST_PACMAN_LOG": str(self.pacman_log),
                "MAKE_TEST_CODEX_LOG": str(self.codex_log),
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
        self.latex_log.write_text("", encoding="utf-8")
        self.flags_log.write_text("", encoding="utf-8")
        self.review_log.write_text("", encoding="utf-8")

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
                (self.root / f"doc/gpt/{document}.pdf").read_bytes(),
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

    def test_install_uses_only_validated_builds_and_refreshes_changed_pdf(self) -> None:
        self.run_make("-j4", "install")
        build_pdf = self.root / "build/gpt/demo-a.pdf"
        installed_pdf = self.root / "doc/gpt/demo-a.pdf"
        self.assertEqual(installed_pdf.read_bytes(), build_pdf.read_bytes())

        time.sleep(0.02)
        build_pdf.write_bytes(b"externally replaced PDF\n")
        self.clear_logs()
        self.run_make("install")
        self.assertEqual(self.lines(self.latex_log), [])
        self.assertEqual(len(self.lines(self.check_log)), 2)  # global + changed PDF
        self.assertEqual(installed_pdf.read_bytes(), build_pdf.read_bytes())

    def test_checker_refresh_does_not_reinstall_identical_pdf_bytes(self) -> None:
        self.run_make("-j4", "install")
        installed_pdfs = [
            self.root / f"doc/gpt/{document}.pdf"
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
        self.assertFalse((self.root / "doc/gpt/demo-a.pdf").exists())
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
        mutating_install = self.root / "scripts/mutating-install"
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
            "doc/gpt/demo-a.pdf",
            f"INSTALL={mutating_install}",
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PDF or metadata checker changed during install", result.stderr)
        self.assertFalse((self.root / "doc/gpt/demo-a.pdf").exists())
        self.assertEqual(
            list((self.root / "doc/gpt").glob("demo-a.pdf.tmp.*")), []
        )

    def test_empty_parallel_limit_fails_closed(self) -> None:
        result = self.run_make("PDF_JOBS=", check=False)
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
        for name in ("codex", "rg"):
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
            "texlive-bin",
            "texlive-basic",
            "texlive-latex",
            "texlive-latexrecommended",
            "texlive-latexextra",
            "texlive-pictures",
            "texlive-fontsrecommended",
            "poppler",
            "imagemagick",
            "git",
            "openai-codex",
            "ripgrep",
        ]

        self.assertEqual(arguments[:2], ["-Syu", "--needed"])
        self.assertEqual(arguments[2:], listed)
        self.assertEqual(listed, expected_packages)
        for excluded in (
            "base-devel",
            "texlive-meta",
            "nodejs",
            "npm",
            "github-cli",
            "ghostscript",
            "qpdf",
        ):
            self.assertNotIn(excluded, listed)
        self.assertNotIn("--noconfirm", arguments)
        self.assertNotIn(".local", " ".join(arguments))
        self.assertIn("shadows canonical /usr/bin/codex", result.stderr)
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

    def test_codex_target_pins_the_configured_system_binary(self) -> None:
        launcher = self.root / "scripts/triptych-codex"
        launcher.write_text(
            """#!/bin/sh
printf '%s\\n' "$TRIPTYCH_CODEX_REAL" > "$MAKE_TEST_CODEX_LOG"
""",
            encoding="utf-8",
        )
        launcher.chmod(0o755)
        self.environment.pop("CODEX", None)
        self.environment["TRIPTYCH_CODEX_REAL"] = "/home/test/.local/bin/codex"

        self.run_make("codex")

        self.assertEqual(self.lines(self.codex_log), ["/usr/bin/codex"])


if __name__ == "__main__":
    unittest.main()
