#!/usr/bin/env python3
"""Black-box tests for scripts/triptych-codex."""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAKEFILE = SCRIPTS_ROOT.parent / "Makefile"
SOURCE_LAUNCHER = SCRIPTS_ROOT / "triptych-codex"
SOURCE_FAKE = Path(__file__).resolve().with_name("fake-codex")


class TriptychCodexTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="triptych-codex-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.control = self.root / "control"
        self.control.mkdir()
        self.state = self.root / "state"
        self.home = self.root / "home"
        self.home.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.fake = self.bin / "codex"

        self.git(self.control, "init", "-b", "main")
        self.git(self.control, "config", "user.name", "Triptych Test")
        self.git(self.control, "config", "user.email", "triptych-test@example.invalid")
        self.git(self.control, "config", "commit.gpgSign", "false")
        (self.control / ".gitignore").write_text("/build/\n", encoding="utf-8")
        (self.control / "baseline.txt").write_text("baseline\n", encoding="utf-8")
        (self.control / "subdir").mkdir()
        (self.control / "subdir/placeholder.txt").write_text("context\n", encoding="utf-8")
        (self.control / "src/gpt/common").mkdir(parents=True)
        (self.control / "scripts").mkdir()
        shutil.copy2(SOURCE_MAKEFILE, self.control / "Makefile")
        self.launcher = self.control / "scripts/triptych-codex"
        shutil.copy2(SOURCE_LAUNCHER, self.launcher)
        self.launcher.chmod(0o755)
        shutil.copy2(SOURCE_FAKE, self.fake)
        self.fake.chmod(0o755)
        self.git(self.control, "add", ".")
        self.git(self.control, "commit", "-m", "Synthetic baseline")
        self.base_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

    def git(
        self,
        cwd: Path,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            env=self.base_environment() if hasattr(self, "home") else None,
        )

    def base_environment(self) -> dict[str, str]:
        environment = os.environ.copy()
        for name in list(environment):
            if name.startswith("TRIPTYCH_CODEX_") or name in {
                "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_COMMON_DIR",
                "GIT_DIR",
                "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY",
                "GIT_PREFIX",
                "GIT_WORK_TREE",
            }:
                environment.pop(name, None)
        environment.update(
            {
                "HOME": str(self.home),
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "TRIPTYCH_CODEX_REAL": str(self.fake),
                "TRIPTYCH_CODEX_STATE_DIR": str(self.state),
            }
        )
        return environment

    def run_launcher(
        self,
        arguments: list[str] | None = None,
        *,
        cwd: Path | None = None,
        stdin: bytes = b"",
        environment: dict[str, str] | None = None,
        timeout: float = 20,
    ) -> subprocess.CompletedProcess:
        merged = self.base_environment()
        if environment:
            merged.update(environment)
        return subprocess.run(
            [str(self.launcher), *(arguments or [])],
            cwd=cwd or self.control,
            env=merged,
            input=stdin,
            capture_output=True,
            check=False,
            timeout=timeout,
        )

    def run_make(
        self,
        arguments: list[str],
        *,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess:
        merged = self.base_environment()
        if environment:
            merged.update(environment)
        return subprocess.run(
            ["make", "--no-print-directory", *arguments],
            cwd=self.control,
            env=merged,
            capture_output=True,
            check=False,
            timeout=20,
        )

    def repo_state(self) -> Path:
        matches = [path for path in self.state.iterdir() if path.is_dir()]
        self.assertEqual(len(matches), 1, matches)
        return matches[0]

    def manifests(self) -> list[dict]:
        if not self.state.exists():
            return []
        state_directories = [path for path in self.state.iterdir() if path.is_dir()]
        if not state_directories:
            return []
        self.assertEqual(len(state_directories), 1)
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((state_directories[0] / "runs").glob("*.json"))
        ]

    def worktree_output(self) -> str:
        return self.git(self.control, "worktree", "list", "--porcelain").stdout

    def worktree_paths(self) -> list[Path]:
        return [
            Path(line.removeprefix("worktree ")).resolve()
            for line in self.worktree_output().splitlines()
            if line.startswith("worktree ")
        ]

    def worker_branches(self) -> list[str]:
        output = self.git(
            self.control,
            "branch",
            "--list",
            "codex/isolated/*",
            "--format=%(refname:short)",
        ).stdout
        return [line for line in output.splitlines() if line]

    def records(self, log: Path) -> list[dict]:
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def rebase_race_environment(
        self,
        worker: Path,
        marker: Path,
        *,
        detach_at: str | None = None,
        independent_advance: bool = False,
    ) -> dict[str, str]:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        wrapper_directory = self.root / "race-bin"
        wrapper_directory.mkdir()
        wrapper = wrapper_directory / "git"
        wrapper.write_text(
            "#!/bin/sh\n"
            '"$TRIPTYCH_TEST_REAL_GIT" "$@"\n'
            "status=$?\n"
            "case \" $* \" in\n"
            '  *" rebase "*)\n'
            '    if [ "$status" -eq 0 ] && '
            '[ "$PWD" = "$TRIPTYCH_TEST_RACE_WORKER" ] && '
            '[ ! -e "$TRIPTYCH_TEST_RACE_MARKER" ]; then\n'
            '      : > "$TRIPTYCH_TEST_RACE_MARKER"\n'
            '      if [ -n "${TRIPTYCH_TEST_RACE_INDEPENDENT:-}" ]; then\n'
            '        printf "%s\\n" "independent target result" > '
            '"$TRIPTYCH_TEST_RACE_CONTROL/target-race-result.txt"\n'
            '        "$TRIPTYCH_TEST_REAL_GIT" -C "$TRIPTYCH_TEST_RACE_CONTROL" '
            'add target-race-result.txt || exit $?\n'
            '        "$TRIPTYCH_TEST_REAL_GIT" -C "$TRIPTYCH_TEST_RACE_CONTROL" '
            'commit -m "Advance target during integration rebase" || exit $?\n'
            "      else\n"
            '        candidate=$("$TRIPTYCH_TEST_REAL_GIT" rev-parse HEAD)\n'
            '        "$TRIPTYCH_TEST_REAL_GIT" -C "$TRIPTYCH_TEST_RACE_CONTROL" '
            'merge --ff-only "$candidate" || exit $?\n'
            "      fi\n"
            '      if [ -n "${TRIPTYCH_TEST_RACE_DETACH_AT:-}" ]; then\n'
            '        "$TRIPTYCH_TEST_REAL_GIT" -C "$TRIPTYCH_TEST_RACE_CONTROL" '
            'switch --detach "$TRIPTYCH_TEST_RACE_DETACH_AT" || exit $?\n'
            "      fi\n"
            "    fi\n"
            "    ;;\n"
            "esac\n"
            "exit \"$status\"\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        environment = {
            "PATH": f"{wrapper_directory}{os.pathsep}{os.environ['PATH']}",
            "TRIPTYCH_TEST_REAL_GIT": real_git or "git",
            "TRIPTYCH_TEST_RACE_WORKER": str(worker),
            "TRIPTYCH_TEST_RACE_CONTROL": str(self.control),
            "TRIPTYCH_TEST_RACE_MARKER": str(marker),
        }
        if detach_at is not None:
            environment["TRIPTYCH_TEST_RACE_DETACH_AT"] = detach_at
        if independent_advance:
            environment["TRIPTYCH_TEST_RACE_INDEPENDENT"] = "1"
        return environment

    def assert_control_unchanged(self) -> None:
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), self.base_head)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            "",
        )

    def test_forwards_arguments_stdin_streams_and_exit_status(self) -> None:
        log = self.root / "forward.jsonl"
        payload = b"plain\x00stdin\nwith bytes\xff"
        prompt = "prompt with spaces; $(not-a-shell) * ?"
        forwarded = ["exec", "--json", prompt]
        result = self.run_launcher(
            forwarded,
            stdin=payload,
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_EXIT": "7",
                "FAKE_CODEX_STDOUT": "child stdout\n",
                "FAKE_CODEX_STDERR": "child stderr\n",
            },
        )
        self.assertEqual(result.returncode, 7)
        self.assertEqual(result.stdout, b"child stdout\n")
        self.assertIn(b"child stderr\n", result.stderr)
        record = self.records(log)[0]
        self.assertEqual(record["argv"][-4:], ["exec", "--json", "--", prompt])
        self.assertEqual(base64.b64decode(record["stdin"]), payload)
        self.assertEqual(record["process_cwd"], record["workdir"])
        self.assertEqual(record["role"], "worker")
        self.assertNotEqual(Path(record["workdir"]), self.control)
        self.assert_control_unchanged()

    def test_clean_success_removes_ephemeral_worker(self) -> None:
        log = self.root / "clean.jsonl"
        result = self.run_launcher(environment={"FAKE_CODEX_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "cleaned")
        self.assert_control_unchanged()

    def test_ignored_build_output_does_not_retain_an_unchanged_worker(self) -> None:
        log = self.root / "ignored.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "ignored"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assert_control_unchanged()

    def test_dirty_and_committed_results_are_preserved(self) -> None:
        for action in ("dirty", "commit"):
            with self.subTest(action=action):
                log = self.root / f"{action}.jsonl"
                result = self.run_launcher(
                    environment={
                        "FAKE_CODEX_LOG": str(log),
                        "FAKE_CODEX_ACTION": action,
                    }
                )
                self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifests = self.manifests()
        self.assertEqual(len(manifests), 2)
        self.assertEqual({manifest["state"] for manifest in manifests}, {"preserved"})
        self.assertEqual(len(self.worktree_paths()), 3)
        self.assertEqual(len(self.worker_branches()), 2)
        for manifest in manifests:
            self.assertIn("locked triptych-codex", self.worktree_output())
            self.assertTrue(Path(manifest["worktree"]).exists())
        committed = next(manifest for manifest in manifests if manifest["dirty"] is False)
        self.assertNotEqual(committed["final_head"], committed["base_sha"])
        clean = self.run_launcher(["--triptych-clean", committed["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"not integrated", clean.stderr)
        self.assert_control_unchanged()

    def test_nonzero_clean_run_is_preserved_and_can_be_cleaned(self) -> None:
        log = self.root / "failed.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_EXIT": "9"}
        )
        self.assertEqual(result.returncode, 9)
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "failed-preserved")
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_clean_refuses_uncommitted_result(self) -> None:
        log = self.root / "dirty-clean.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "dirty"}
        )
        self.assertEqual(result.returncode, 0)
        manifest = self.manifests()[0]
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"uncommitted changes", clean.stderr)
        self.assertTrue(Path(manifest["worktree"]).exists())

    def test_dirty_control_checkout_fails_before_allocation(self) -> None:
        log = self.root / "must-not-run.jsonl"
        (self.control / "untracked.txt").write_text("local work\n", encoding="utf-8")
        result = self.run_launcher(environment={"FAKE_CODEX_LOG": str(log)})
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"control checkout is not clean", result.stderr)
        self.assertFalse(log.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_tracked_or_staged_control_changes_fail_before_allocation(self) -> None:
        for staged in (False, True):
            with self.subTest(staged=staged):
                (self.control / "baseline.txt").write_text("local change\n", encoding="utf-8")
                if staged:
                    self.git(self.control, "add", "baseline.txt")
                log = self.root / f"dirty-tracked-{staged}.jsonl"
                result = self.run_launcher(environment={"FAKE_CODEX_LOG": str(log)})
                self.assertEqual(result.returncode, 2)
                self.assertIn(b"control checkout is not clean", result.stderr)
                self.assertFalse(log.exists())
                self.git(self.control, "restore", "--staged", "baseline.txt", check=False)
                self.git(self.control, "restore", "baseline.txt")
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_ignored_control_build_output_does_not_block_allocation(self) -> None:
        (self.control / "build").mkdir()
        (self.control / "build/local.tmp").write_text("ignored\n", encoding="utf-8")
        log = self.root / "ignored-control.jsonl"
        result = self.run_launcher(environment={"FAKE_CODEX_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_rejects_workspace_escape_options_before_allocation(self) -> None:
        unsafe_arguments = (
            ["-C", "/tmp"],
            ["--cd=/tmp"],
            ["--add-dir", "/tmp"],
            ["--remote", "ws://example.invalid"],
            ["--dangerously-bypass-approvals-and-sandbox"],
            ["--yolo"],
            ["--sandbox", "danger-full-access"],
            ["-sdanger-full-access"],
            ["--enable", "multi_agent"],
            ["exec", "--ignore-rules", "prompt"],
            ["exec", "-o", "/tmp/result.txt", "prompt"],
            ["exec", "-o/tmp/result.txt", "prompt"],
            ["-c", "sandbox_workspace_write.writable_roots=['/tmp']"],
            ["-csandbox_mode='danger-full-access'"],
            ["-c", "'sandbox_permissions'=['disk-full-read-access']"],
            ["-c", '"sandbox_workspace_write"."writable_roots"=["/tmp"]'],
            ["-c", 'sandbox_workspace_write={writable_roots=["/tmp"]}'],
            ["-c", "features={multi_agent=true}"],
            ["-c", r'"\u0073andbox_mode"="danger-full-access"'],
            ["--profile", "unsafe-profile"],
            ["--disable", "multi_agent"],
            ["--future-write-root", "/tmp"],
        )
        for index, arguments in enumerate(unsafe_arguments):
            with self.subTest(arguments=arguments):
                log = self.root / f"unsafe-{index}.jsonl"
                result = self.run_launcher(
                    list(arguments),
                    environment={"FAKE_CODEX_LOG": str(log)},
                )
                self.assertEqual(result.returncode, 2)
                self.assertFalse(log.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_allows_only_scoped_agent_options_and_normalizes_prompts(self) -> None:
        log = self.root / "safe-options.jsonl"
        result = self.run_launcher(
            [
                "--model",
                "test-model",
                "--sandbox",
                "read-only",
                "exec",
                "--json",
                "safe prompt",
            ],
            environment={"FAKE_CODEX_LOG": str(log)},
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        argv = self.records(log)[0]["argv"]
        self.assertEqual(
            argv[-8:],
            [
                "--model",
                "test-model",
                "--sandbox",
                "read-only",
                "exec",
                "--json",
                "--",
                "safe prompt",
            ],
        )
        self.assertNotIn("workspace-write", argv)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_separated_image_value_is_bounded_before_an_agent_subcommand(self) -> None:
        log = self.root / "image-boundary.jsonl"
        result = self.run_launcher(
            ["--image", "reference.png", "exec", "--version"],
            environment={"FAKE_CODEX_LOG": str(log)},
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(
            self.records(log)[0]["argv"][-3:],
            ["--image=reference.png", "exec", "--version"],
        )

    def test_exec_review_is_an_allowed_nested_agent_surface(self) -> None:
        log = self.root / "exec-review.jsonl"
        result = self.run_launcher(
            ["exec", "review", "--uncommitted", "review prompt"],
            environment={"FAKE_CODEX_LOG": str(log)},
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(
            self.records(log)[0]["argv"][-5:],
            ["exec", "review", "--uncommitted", "--", "review prompt"],
        )

    def test_native_exec_resume_is_rejected_before_allocation(self) -> None:
        log = self.root / "native-resume.jsonl"
        result = self.run_launcher(
            ["exec", "resume", "--last"],
            environment={"FAKE_CODEX_LOG": str(log)},
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"outside the isolated agent launcher", result.stderr)
        self.assertFalse(log.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_rejects_non_agent_codex_subcommands_before_allocation(self) -> None:
        blocked = (
            "app-server",
            "apply",
            "cloud",
            "debug",
            "exec-server",
            "login",
            "mcp-server",
            "plugin",
            "remote-control",
            "sandbox",
            "update",
        )
        for index, subcommand in enumerate(blocked):
            with self.subTest(subcommand=subcommand):
                log = self.root / f"subcommand-{index}.jsonl"
                result = self.run_launcher(
                    ["--model", "test-model", subcommand],
                    environment={"FAKE_CODEX_LOG": str(log)},
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn(b"outside the isolated agent launcher", result.stderr)
                self.assertFalse(log.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_double_dash_can_force_a_command_name_to_be_an_interactive_prompt(self) -> None:
        log = self.root / "forced-prompt.jsonl"
        result = self.run_launcher(
            ["--", "sandbox"],
            environment={"FAKE_CODEX_LOG": str(log)},
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(self.records(log)[0]["argv"][-2:], ["--", "sandbox"])
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_preserves_starting_subdirectory(self) -> None:
        log = self.root / "subdir.jsonl"
        result = self.run_launcher(
            cwd=self.control / "subdir",
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_EXIT": "3"},
        )
        self.assertEqual(result.returncode, 3)
        record = self.records(log)[0]
        self.assertEqual(Path(record["workdir"]).name, "subdir")
        self.assertNotEqual(Path(record["root"]), self.control)

    def test_recursive_launcher_is_rejected_without_a_second_writer(self) -> None:
        log = self.root / "recursive.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "recursive",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        records = self.records(log)
        self.assertEqual(len(records), 1)
        self.assertIn(b"nested Codex launch refused", result.stderr)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(len(self.manifests()), 1)

    def test_managed_worktree_lock_rejects_marker_free_detached_recursion(self) -> None:
        log = self.root / "recursive-detached.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "recursive-detached",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(len(self.records(log)), 1)
        self.assertIn(b"nested Codex launch refused", result.stderr)
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "quarantined")
        self.assertTrue(Path(manifest["worktree"]).exists())
        self.assertEqual(len(self.worktree_paths()), 2)

    def test_forged_worker_marker_does_not_run_in_control_checkout(self) -> None:
        log = self.root / "forged.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "TRIPTYCH_CODEX_ROLE": "worker",
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse(log.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        status = self.run_launcher(
            ["--triptych-status"],
            environment={"TRIPTYCH_CODEX_ROLE": "worker"},
        )
        self.assertEqual(status.returncode, 2)
        self.assertIn(b"worker marker is invalid", status.stderr)

    def test_real_binary_cannot_be_the_launcher(self) -> None:
        result = self.run_launcher(
            environment={"TRIPTYCH_CODEX_REAL": str(self.launcher)}
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"non-launcher executable", result.stderr)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_runtime_state_cannot_be_placed_inside_the_control_worktree(self) -> None:
        log = self.root / "inside-state.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "TRIPTYCH_CODEX_STATE_DIR": str(self.control / ".runtime-state"),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"outside the worktree", result.stderr)
        self.assertFalse(log.exists())
        self.assertFalse((self.control / ".runtime-state").exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_reopen_reuses_a_retained_worker(self) -> None:
        first_log = self.root / "resume-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(first.returncode, 0)
        manifest = self.manifests()[0]
        second_log = self.root / "resume-second.jsonl"
        second = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"], "--", "follow-up"],
            environment={"FAKE_CODEX_LOG": str(second_log)},
        )
        self.assertEqual(second.returncode, 0)
        self.assertEqual(
            self.records(first_log)[0]["root"],
            self.records(second_log)[0]["root"],
        )
        self.assertEqual(len(self.manifests()), 1)
        self.assertEqual(len(self.worktree_paths()), 2)

    def test_reopen_quarantines_history_rewritten_before_automatic_cleanup(self) -> None:
        first_log = self.root / "reopen-reset-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        manifest = self.manifests()[0]
        reviewed_head = manifest["final_head"]

        second_log = self.root / "reopen-reset-second.jsonl"
        second = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(second_log),
                "FAKE_CODEX_ACTION": "reset-parent",
            },
        )
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        self.assertIn(b"was quarantined", second.stderr)
        quarantined = self.manifests()[0]
        self.assertEqual(quarantined["state"], "quarantined")
        self.assertEqual(quarantined["final_head"], reviewed_head)
        self.assertEqual(quarantined["observed_head"], self.base_head)
        self.assertTrue(Path(quarantined["worktree"]).exists())
        self.assertEqual(self.worker_branches(), [quarantined["branch"]])

        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"changed since its last launcher audit", clean.stderr)

    def test_reopen_records_a_clean_result_before_explicit_cleanup(self) -> None:
        first_log = self.root / "reopen-clean-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        manifest = self.manifests()[0]
        self.assertTrue(manifest["dirty"])

        second_log = self.root / "reopen-clean-second.jsonl"
        second = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(second_log),
                "FAKE_CODEX_ACTION": "remove-dirty-result",
            },
        )
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        refreshed = self.manifests()[0]
        self.assertEqual(refreshed["state"], "preserved")
        self.assertFalse(refreshed["dirty"])
        self.assertEqual(refreshed["final_head"], self.base_head)
        self.assertTrue(Path(refreshed["worktree"]).exists())

        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_worker_keeps_run_lock_if_launcher_is_killed(self) -> None:
        log = self.root / "orphan.jsonl"
        ready = self.root / "orphan.ready"
        release = self.root / "orphan.release"
        environment = self.base_environment()
        environment.update(
            {
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_READY": str(ready),
                "FAKE_CODEX_RELEASE": str(release),
            }
        )
        process = subprocess.Popen(
            [str(self.launcher), "long-running task"],
            cwd=self.control,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.addCleanup(lambda: release.touch(exist_ok=True))
        deadline = time.monotonic() + 10
        while not ready.exists():
            if process.poll() is not None:
                self.fail(f"launcher exited before worker became ready: {process.returncode}")
            if time.monotonic() >= deadline:
                process.kill()
                self.fail("worker did not become ready")
            time.sleep(0.02)

        manifest = self.manifests()[0]
        process.kill()
        process.wait(timeout=5)
        active = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertEqual(active.returncode, 0, active.stderr.decode())
        self.assertIn(b"running", active.stdout)
        self.assertIn(b"yes", active.stdout)
        reopen = self.run_launcher(["--triptych-reopen", manifest["run_id"]])
        self.assertEqual(reopen.returncode, 2)
        self.assertIn(b"already active", reopen.stderr)
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"already active", clean.stderr)

        release.touch()
        deadline = time.monotonic() + 10
        while True:
            status = self.run_launcher(["--triptych-status", manifest["run_id"]])
            if b"interrupted" in status.stdout and b"no" in status.stdout:
                break
            if time.monotonic() >= deadline:
                self.fail(f"orphaned worker did not settle: {status.stdout!r}")
            time.sleep(0.05)
        self.assertTrue(Path(manifest["worktree"]).exists())

    def test_signal_exit_is_normalized_for_the_shell(self) -> None:
        log = self.root / "signal.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "signal"}
        )
        self.assertEqual(result.returncode, 128 + 15)
        self.assertEqual(self.manifests()[0]["child_exit_code"], 128 + 15)

    def test_background_descendant_keeps_run_exclusive_until_it_exits(self) -> None:
        log = self.root / "background.jsonl"
        ready = self.root / "background.ready"
        release = self.root / "background.release"
        self.addCleanup(lambda: release.touch(exist_ok=True))
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "background",
                "FAKE_CODEX_BACKGROUND_READY": str(ready),
                "FAKE_CODEX_BACKGROUND_RELEASE": str(release),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        deadline = time.monotonic() + 5
        while not ready.exists():
            if time.monotonic() >= deadline:
                self.fail("background worker did not become ready")
            time.sleep(0.02)

        manifest = self.manifests()[0]
        self.assertTrue(manifest["background_process_active"])
        status = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertIn(b"yes", status.stdout)
        reopen = self.run_launcher(["--triptych-reopen", manifest["run_id"]])
        self.assertEqual(reopen.returncode, 2)
        self.assertIn(b"already active", reopen.stderr)
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"already active", integrate.stderr)

        release.touch()
        deadline = time.monotonic() + 5
        while True:
            status = self.run_launcher(["--triptych-status", manifest["run_id"]])
            if b"no" in status.stdout:
                break
            if time.monotonic() >= deadline:
                self.fail(f"background worker did not release its lock: {status.stdout!r}")
            time.sleep(0.05)
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_clean_removes_a_fully_integrated_committed_result(self) -> None:
        log = self.root / "integrated.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        self.git(self.control, "merge", "--ff-only", manifest["branch"])

        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )

    def test_integrate_fast_forwards_target_and_cleans_worker(self) -> None:
        log = self.root / "integrate.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker_head = manifest["final_head"]
        temporary = Path(manifest["tmpdir"])

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        self.assertIn(b"integrated and cleaned", integrate.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            worker_head,
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "1",
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertFalse(temporary.exists())
        integrated_manifest = self.manifests()[0]
        self.assertEqual(integrated_manifest["state"], "cleaned")
        self.assertEqual(integrated_manifest["integrated_head"], worker_head)
        self.assertIn("integrated_at", integrated_manifest)
        self.assertIn("cleaned_at", integrated_manifest)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            "",
        )
        repeated = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(repeated.returncode, 0, repeated.stderr.decode())
        self.assertIn(b"already integrated and cleaned", repeated.stderr)

    def test_make_integrate_forwards_one_run_id_without_masking_unknown_targets(self) -> None:
        log = self.root / "make-integrate.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]

        missing = self.run_make(["integrate"])
        self.assertEqual(missing.returncode, 2)
        self.assertIn(b"Usage: make integrate <run-id>", missing.stderr)
        self.assert_control_unchanged()
        self.assertTrue(Path(manifest["worktree"]).exists())

        unknown = self.run_make(["definitely-unknown"])
        self.assertEqual(unknown.returncode, 2)
        self.assertIn(b"No rule to make target", unknown.stderr)

        integrate = self.run_make(["integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            manifest["final_head"],
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_integrate_does_not_claim_an_auto_cleaned_run_was_integrated(self) -> None:
        log = self.root / "auto-cleaned-integrate.jsonl"
        result = self.run_launcher(environment={"FAKE_CODEX_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "cleaned")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"no retained result to integrate", integrate.stderr)

    def test_integrate_rechecks_a_cleaned_result_reachability(self) -> None:
        log = self.root / "cleaned-reachability.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        self.git(self.control, "reset", "--hard", self.base_head)

        repeated = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(repeated.returncode, 2)
        self.assertIn(b"no longer contains the integrated commit", repeated.stderr)

    def test_integrate_recognizes_an_already_reachable_result_and_cleans(self) -> None:
        log = self.root / "already-integrated.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        self.git(self.control, "merge", "--ff-only", manifest["branch"])

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        integrated_manifest = self.manifests()[0]
        self.assertEqual(integrated_manifest["state"], "cleaned")
        self.assertIn("integration_confirmed_at", integrated_manifest)

    def test_integrate_refuses_uncommitted_worker_changes(self) -> None:
        log = self.root / "integrate-dirty-worker.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "dirty"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"uncommitted changes", integrate.stderr)
        self.assert_control_unchanged()
        self.assertTrue(Path(manifest["worktree"]).exists())
        self.assertEqual(self.worker_branches(), [manifest["branch"]])

    def test_integrate_refuses_a_commit_after_the_terminal_audit(self) -> None:
        log = self.root / "integrate-late-commit.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        (worker / "late-result.txt").write_text("not audited\n", encoding="utf-8")
        self.git(worker, "add", "late-result.txt")
        self.git(worker, "commit", "-m", "Add unaudited result")
        late_head = self.git(worker, "rev-parse", "HEAD").stdout.strip()

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"changed since its last launcher audit", integrate.stderr)
        self.assert_control_unchanged()
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), late_head)
        self.assertTrue(worker.exists())

    def test_integrate_refuses_a_reset_after_the_terminal_audit(self) -> None:
        log = self.root / "integrate-reset-worker.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        self.git(worker, "reset", "--hard", self.base_head)

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"changed since its last launcher audit", integrate.stderr)
        self.assert_control_unchanged()
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD").stdout.strip(),
            self.base_head,
        )
        self.assertTrue(worker.exists())
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"changed since its last launcher audit", clean.stderr)
        self.assertTrue(worker.exists())

    def test_integrate_rolls_back_rebase_and_preserves_ignored_primary_collision(
        self,
    ) -> None:
        log = self.root / "integrate-ignored-collision.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "commit-ignored",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        original_worker_head = manifest["final_head"]
        (self.control / "primary-result.txt").write_text(
            "primary result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        advanced_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        (self.control / "build").mkdir(exist_ok=True)
        collision = self.control / "build/collision.txt"
        collision.write_text("local ignored output\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"fast-forward integration failed after rebase", integrate.stderr)
        self.assertEqual(collision.read_text(encoding="utf-8"), "local ignored output\n")
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            advanced_head,
        )
        self.assertTrue(worker.exists())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), original_worker_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        rolled_back = self.manifests()[0]
        self.assertEqual(rolled_back["final_head"], original_worker_head)
        self.assertNotIn("integration_candidate_head", rolled_back)
        self.assertNotIn("integrated_head", rolled_back)

        collision.unlink()
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(
            (self.control / "build/collision.txt").read_text(encoding="utf-8"),
            "tracked worker result\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_integrate_direct_fast_forward_preserves_ignored_primary_collision(
        self,
    ) -> None:
        log = self.root / "integrate-direct-ignored-collision.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "commit-ignored",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        (self.control / "build").mkdir(exist_ok=True)
        collision = self.control / "build/collision.txt"
        collision.write_text("local ignored output\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"fast-forward integration failed", integrate.stderr)
        self.assertEqual(collision.read_text(encoding="utf-8"), "local ignored output\n")
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            self.base_head,
        )
        self.assertTrue(Path(manifest["worktree"]).exists())
        self.assertEqual(
            self.git(Path(manifest["worktree"]), "rev-parse", "HEAD").stdout.strip(),
            manifest["final_head"],
        )

    def test_integrate_refuses_a_dirty_primary_checkout(self) -> None:
        log = self.root / "integrate-dirty-primary.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        (self.control / "local-review.txt").write_text("keep me\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"control checkout is not clean", integrate.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            self.base_head,
        )
        self.assertTrue(Path(manifest["worktree"]).exists())
        self.assertEqual(self.worker_branches(), [manifest["branch"]])

    def test_integrate_requires_the_recorded_target_branch(self) -> None:
        log = self.root / "integrate-wrong-target.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        self.git(self.control, "switch", "-c", "alternate")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"recorded target branch 'main'", integrate.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            self.base_head,
        )
        self.assertTrue(Path(manifest["worktree"]).exists())
        self.assertEqual(self.worker_branches(), [manifest["branch"]])

    def test_integrate_rebases_diverged_result_and_fast_forwards_flat_history(self) -> None:
        log = self.root / "integrate-diverged.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        original_worker_head = manifest["final_head"]
        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        advanced_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, original_worker_head)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), advanced_head)
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "2",
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--merges", f"{self.base_head}..HEAD").stdout,
            "",
        )
        self.assertEqual(
            self.git(
                self.control,
                "merge-base",
                "--is-ancestor",
                original_worker_head,
                landed_head,
                check=False,
            ).returncode,
            1,
        )
        self.assertEqual(
            (self.control / "primary-result.txt").read_text(encoding="utf-8"),
            "primary result\n",
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )
        merge_head = self.git(self.control, "rev-parse", "--verify", "MERGE_HEAD", check=False)
        self.assertNotEqual(merge_head.returncode, 0)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            "",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        integrated = self.manifests()[0]
        self.assertEqual(integrated["state"], "cleaned")
        self.assertEqual(integrated["final_head"], original_worker_head)
        self.assertEqual(integrated["integration_source_head"], original_worker_head)
        self.assertEqual(integrated["integration_target_head"], advanced_head)
        self.assertEqual(integrated["integration_candidate_head"], landed_head)
        self.assertEqual(integrated["integrated_head"], landed_head)

    def test_integrate_accepts_target_that_reaches_candidate_during_rebase(self) -> None:
        log = self.root / "integrate-target-advance-during-rebase.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        original_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        captured_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        marker = self.root / "target-advanced-during-rebase"

        integrate = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.rebase_race_environment(worker, marker),
        )
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        self.assertTrue(marker.exists())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, original_head)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), captured_target)
        self.assertEqual(
            self.git(self.control, "rev-list", "--merges", f"{self.base_head}..HEAD").stdout,
            "",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        integrated = self.manifests()[0]
        self.assertEqual(integrated["state"], "cleaned")
        self.assertEqual(integrated["final_head"], original_head)
        self.assertEqual(integrated["integration_candidate_head"], landed_head)
        self.assertEqual(integrated["integrated_head"], landed_head)

    def test_integrate_does_not_rollback_landed_candidate_after_checkout_switch(
        self,
    ) -> None:
        log = self.root / "integrate-target-landed-before-checkout-switch.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        original_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        captured_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        marker = self.root / "target-landed-before-checkout-switch"

        integrate = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.rebase_race_environment(
                worker,
                marker,
                detach_at=captured_target,
            ),
        )
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"was not rolled back", integrate.stderr)
        self.assertTrue(marker.exists())
        landed_head = self.git(self.control, "rev-parse", "main").stdout.strip()
        self.assertNotEqual(landed_head, original_head)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), landed_head)
        self.assertEqual(
            self.git(self.control, "symbolic-ref", "--quiet", "HEAD", check=False).returncode,
            1,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-verification-failed")
        self.assertEqual(retained["integration_candidate_head"], landed_head)
        self.assertEqual(retained["integrated_head"], landed_head)

        self.git(self.control, "switch", "main")
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integrated_head"], landed_head)

    def test_integrate_restores_worker_if_target_advances_elsewhere_during_rebase(
        self,
    ) -> None:
        log = self.root / "integrate-independent-target-race.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        original_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        marker = self.root / "independent-target-race"

        integrate = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.rebase_race_environment(
                worker,
                marker,
                independent_advance=True,
            ),
        )
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"restored and was not merged", integrate.stderr)
        self.assertTrue(marker.exists())
        raced_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(
            (self.control / "target-race-result.txt").read_text(encoding="utf-8"),
            "independent target result\n",
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), original_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "preserved")
        self.assertNotIn("integration_candidate_head", retained)
        self.assertNotIn("integrated_head", retained)

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), raced_target)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["integrated_head"], landed_head)

    def test_integrate_retains_conflict_until_abort_restores_audited_worker(self) -> None:
        log = self.root / "integrate-rebase-conflict.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        audited_head = manifest["final_head"]

        (self.control / "agent-result.txt").write_text(
            "conflicting primary result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Add conflicting primary result")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"stopped at a conflict and remains active", integrate.stderr)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertIn("AA agent-result.txt", self.git(worker, "status", "--short").stdout)
        self.assertEqual(
            self.git(worker, "rev-parse", "--verify", "REBASE_HEAD").returncode,
            0,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-pending")
        self.assertEqual(retained["integration_source_head"], audited_head)
        self.assertEqual(retained["integration_target_head"], target_head)

        abort = self.run_make(["abort", manifest["run_id"]])
        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), audited_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(
            self.git(worker, "symbolic-ref", "--short", "HEAD").stdout.strip(),
            manifest["branch"],
        )
        self.assertNotEqual(
            self.git(worker, "rev-parse", "--verify", "REBASE_HEAD", check=False).returncode,
            0,
        )
        restored = self.manifests()[0]
        self.assertEqual(restored["state"], "preserved")
        self.assertEqual(restored["final_head"], audited_head)
        self.assertNotIn("integration_source_head", restored)
        self.assertNotIn("integration_candidate_head", restored)
        self.assertNotIn("integrated_head", restored)

    def test_fixed_resolver_and_continue_complete_existing_integration_path(self) -> None:
        log = self.root / "resolver-source.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])

        (self.control / "agent-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Add conflicting primary result")
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)

        resolver_log = self.root / "fixed-resolver.jsonl"
        resolve = self.run_make(
            ["resolve", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(resolver_log)},
        )
        self.assertEqual(resolve.returncode, 0, resolve.stderr.decode())
        resolver_argv = self.records(resolver_log)[0]["argv"]
        self.assertEqual(resolver_argv[-2], "--")
        self.assertIn("stage the complete resolution with git add", resolver_argv[-1])
        self.assertIn("Do not run git rebase --continue", resolver_argv[-1])
        self.assertEqual(self.manifests()[0]["state"], "integration-rebase-pending")

        (worker / "agent-result.txt").write_text("reconciled result\n", encoding="utf-8")
        self.git(worker, "add", "agent-result.txt")
        self.git(worker, "config", "core.editor", "false")
        continued = self.run_make(["continue", manifest["run_id"]])
        self.assertEqual(continued.returncode, 0, continued.stderr.decode())
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "reconciled result\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        completed = self.manifests()[0]
        self.assertEqual(completed["state"], "cleaned")
        self.assertEqual(completed["integration_source_head"], manifest["final_head"])
        self.assertEqual(completed["integrated_head"], completed["integration_candidate_head"])

    def test_continue_retains_the_next_rebase_conflict(self) -> None:
        log = self.root / "multi-conflict-source.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        (worker / "second-result.txt").write_text("worker second result\n", encoding="utf-8")
        self.git(worker, "add", "second-result.txt")
        self.git(worker, "commit", "-m", "Add second worker result")
        refresh_log = self.root / "multi-conflict-refresh.jsonl"
        refresh = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(refresh_log)},
        )
        self.assertEqual(refresh.returncode, 0, refresh.stderr.decode())
        audited_head = self.manifests()[0]["final_head"]

        (self.control / "agent-result.txt").write_text("primary first result\n", encoding="utf-8")
        (self.control / "second-result.txt").write_text(
            "primary second result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "agent-result.txt", "second-result.txt")
        self.git(self.control, "commit", "-m", "Add conflicting primary results")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)

        (worker / "agent-result.txt").write_text("resolved first result\n", encoding="utf-8")
        self.git(worker, "add", "agent-result.txt")
        continued = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continued.returncode, 2)
        self.assertIn(b"current or next conflict", continued.stderr)
        self.assertIn("AA second-result.txt", self.git(worker, "status", "--short").stdout)
        self.assertEqual(
            self.git(worker, "rev-parse", "--verify", "REBASE_HEAD").returncode,
            0,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-pending")
        self.assertEqual(retained["integration_source_head"], audited_head)
        self.assertEqual(retained["integration_target_head"], target_head)

    def test_integrate_refuses_worker_merge_that_could_hide_merge_only_content(
        self,
    ) -> None:
        first_log = self.root / "integrate-worker-merge-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])

        self.git(worker, "switch", "-c", "test-side")
        (worker / "side-result.txt").write_text("side result\n", encoding="utf-8")
        self.git(worker, "add", "side-result.txt")
        self.git(worker, "commit", "-m", "Add side result")
        self.git(worker, "switch", manifest["branch"])
        (worker / "mainline-result.txt").write_text("mainline result\n", encoding="utf-8")
        self.git(worker, "add", "mainline-result.txt")
        self.git(worker, "commit", "-m", "Add mainline result")
        self.git(worker, "merge", "--no-ff", "--no-commit", "test-side")
        (worker / "merge-only.txt").write_text("merge-only result\n", encoding="utf-8")
        self.git(worker, "add", "merge-only.txt")
        self.git(worker, "commit", "-m", "Merge side result with reviewed resolution")

        second_log = self.root / "integrate-worker-merge-second.jsonl"
        audited = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(second_log)},
        )
        self.assertEqual(audited.returncode, 0, audited.stderr.decode())
        refreshed = self.manifests()[0]
        merge_head = refreshed["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"worker-side merge commit", integrate.stderr)
        self.assertIn(b"linear audited worker history", integrate.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), merge_head)
        self.assertEqual(
            (worker / "merge-only.txt").read_text(encoding="utf-8"),
            "merge-only result\n",
        )
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertTrue(worker.exists())

    def test_integrate_drops_duplicate_patch_for_flattest_history(self) -> None:
        first_log = self.root / "duplicate-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "commit",
                "GIT_AUTHOR_DATE": "2001-01-01T00:00:00+0000",
                "GIT_COMMITTER_DATE": "2001-01-01T00:00:00+0000",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        first_manifest = self.manifests()[0]

        second_log = self.root / "duplicate-second.jsonl"
        second = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(second_log),
                "FAKE_CODEX_ACTION": "commit",
                "GIT_AUTHOR_DATE": "2002-02-02T00:00:00+0000",
                "GIT_COMMITTER_DATE": "2002-02-02T00:00:00+0000",
            }
        )
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        second_manifest = next(
            manifest
            for manifest in self.manifests()
            if manifest["run_id"] != first_manifest["run_id"]
        )
        self.assertNotEqual(first_manifest["final_head"], second_manifest["final_head"])

        integrate_first = self.run_launcher(
            ["--triptych-integrate", first_manifest["run_id"]]
        )
        self.assertEqual(integrate_first.returncode, 0, integrate_first.stderr.decode())
        first_landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        integrate_second = self.run_launcher(
            ["--triptych-integrate", second_manifest["run_id"]]
        )
        self.assertEqual(integrate_second.returncode, 0, integrate_second.stderr.decode())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            first_landed_head,
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "1",
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--merges", f"{self.base_head}..HEAD").stdout,
            "",
        )
        second_integrated = next(
            manifest
            for manifest in self.manifests()
            if manifest["run_id"] == second_manifest["run_id"]
        )
        self.assertEqual(second_integrated["state"], "cleaned")
        self.assertEqual(second_integrated["final_head"], second_manifest["final_head"])
        self.assertEqual(second_integrated["integrated_head"], first_landed_head)
        self.assertEqual(second_integrated["integration_candidate_head"], first_landed_head)

    def test_integrate_reapplies_worker_patch_reverted_on_target(self) -> None:
        log = self.root / "integrate-reverted-upstream-patch.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]

        (self.control / "agent-result.txt").write_text(
            "committed result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Apply worker patch independently")
        self.git(self.control, "revert", "--no-edit", "HEAD")
        reverted_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertFalse((self.control / "agent-result.txt").exists())

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), reverted_target)
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "3",
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--merges", f"{self.base_head}..HEAD").stdout,
            "",
        )
        integrated = self.manifests()[0]
        self.assertEqual(integrated["state"], "cleaned")
        self.assertEqual(integrated["integrated_head"], landed_head)

    def test_serial_integration_rebases_a_second_run_from_the_same_base(self) -> None:
        first_log = self.root / "serial-first.jsonl"
        first = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(first_log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        first_manifest = self.manifests()[0]

        second_log = self.root / "serial-second.jsonl"
        second = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(second_log),
                "FAKE_CODEX_ACTION": "commit-ignored",
            }
        )
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        second_manifest = next(
            manifest
            for manifest in self.manifests()
            if manifest["run_id"] != first_manifest["run_id"]
        )

        integrate_first = self.run_launcher(
            ["--triptych-integrate", first_manifest["run_id"]]
        )
        self.assertEqual(integrate_first.returncode, 0, integrate_first.stderr.decode())
        first_landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        integrate_second = self.run_launcher(
            ["--triptych-integrate", second_manifest["run_id"]]
        )
        self.assertEqual(integrate_second.returncode, 0, integrate_second.stderr.decode())
        final_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD^").stdout.strip(),
            first_landed_head,
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "2",
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--merges", f"{self.base_head}..HEAD").stdout,
            "",
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )
        self.assertEqual(
            (self.control / "build/collision.txt").read_text(encoding="utf-8"),
            "tracked worker result\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        second_integrated = next(
            manifest
            for manifest in self.manifests()
            if manifest["run_id"] == second_manifest["run_id"]
        )
        self.assertEqual(second_integrated["state"], "cleaned")
        self.assertEqual(second_integrated["integrated_head"], final_head)
        self.assertNotEqual(second_integrated["integrated_head"], second_manifest["final_head"])

    def test_internal_rebase_disables_hooks_that_could_mutate_candidate(self) -> None:
        log = self.root / "integrate-post-rewrite-disabled.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        original_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        hook = self.control / ".git/hooks/post-rewrite"
        hook.write_text(
            "#!/bin/sh\n"
            'printf "%s\\n" "hook result" > post-rewrite-result.txt\n'
            "git add post-rewrite-result.txt\n"
            'git commit -m "Hook-created commit"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, original_head)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertFalse((self.control / "post-rewrite-result.txt").exists())
        self.assertNotIn(
            "Hook-created commit",
            self.git(
                self.control,
                "log",
                "--format=%s",
                f"{self.base_head}..HEAD",
            ).stdout,
        )
        self.assertEqual(
            self.git(self.control, "rev-list", "--count", f"{self.base_head}..HEAD").stdout.strip(),
            "2",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        integrated = self.manifests()[0]
        self.assertEqual(integrated["state"], "cleaned")
        self.assertEqual(integrated["final_head"], original_head)
        self.assertEqual(integrated["integration_target_head"], target_head)
        self.assertEqual(integrated["integration_candidate_head"], landed_head)
        self.assertEqual(integrated["integrated_head"], landed_head)

    def test_interrupted_rebase_recovery_does_not_reset_dirty_worker(self) -> None:
        log = self.root / "integrate-interrupted-rebase.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.git(worker, "rebase", "--onto", target_head, self.base_head)
        candidate_head = self.git(worker, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(candidate_head, source_head)

        manifest.update(
            {
                "state": "integration-rebase-pending",
                "integration_previous_state": "preserved",
                "integration_source_head": source_head,
                "integration_target_head": target_head,
                "integration_started_at": "2000-01-01T00:00:00+00:00",
            }
        )
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        recovery_note = worker / "recovery-note.txt"
        recovery_note.write_text("do not discard\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"retained without abort or reset", integrate.stderr)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate_head)
        self.assertEqual(recovery_note.read_text(encoding="utf-8"), "do not discard\n")
        self.assertIn("?? recovery-note.txt", self.git(worker, "status", "--porcelain=v1").stdout)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-recovery-failed")
        self.assertEqual(recovered["integration_source_head"], source_head)

    def test_interrupted_rebase_recovery_does_not_reset_unknown_clean_commit(
        self,
    ) -> None:
        log = self.root / "integrate-interrupted-clean-commit.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.git(worker, "rebase", "--onto", target_head, self.base_head)
        (worker / "manual-recovery.txt").write_text("preserve this commit\n", encoding="utf-8")
        self.git(worker, "add", "manual-recovery.txt")
        self.git(worker, "commit", "-m", "Manual recovery commit")
        unknown_head = self.git(worker, "rev-parse", "HEAD").stdout.strip()

        manifest.update(
            {
                "state": "integration-rebase-pending",
                "integration_previous_state": "preserved",
                "integration_source_head": source_head,
                "integration_target_head": target_head,
                "integration_started_at": "2000-01-01T00:00:00+00:00",
            }
        )
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"retained without abort or reset", integrate.stderr)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), unknown_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(
            (worker / "manual-recovery.txt").read_text(encoding="utf-8"),
            "preserve this commit\n",
        )
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-recovery-failed")
        self.assertEqual(recovered["integration_observed_head"], unknown_head)

    def test_interrupted_rebase_recovery_leaves_active_rebase_untouched(self) -> None:
        log = self.root / "integrate-interrupted-active-rebase.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]

        (self.control / "agent-result.txt").write_text("primary conflict\n", encoding="utf-8")
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary with conflict")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        conflict = self.git(
            worker,
            "rebase",
            "--onto",
            target_head,
            self.base_head,
            check=False,
        )
        self.assertNotEqual(conflict.returncode, 0)
        (worker / "agent-result.txt").write_text("manual resolution\n", encoding="utf-8")
        self.git(worker, "add", "agent-result.txt")
        status_before = self.git(worker, "status", "--porcelain=v1").stdout
        rebase_marker = Path(
            self.git(worker, "rev-parse", "--git-path", "rebase-merge").stdout.strip()
        )
        if not rebase_marker.is_absolute():
            rebase_marker = worker / rebase_marker
        self.assertTrue(rebase_marker.exists())

        manifest.update(
            {
                "state": "integration-rebase-pending",
                "integration_previous_state": "preserved",
                "integration_source_head": source_head,
                "integration_target_head": target_head,
                "integration_started_at": "2000-01-01T00:00:00+00:00",
            }
        )
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"integration rebase conflict remains active", integrate.stderr)
        for action in ("resolve", "continue", "abort"):
            self.assertIn(
                f"--triptych-{action} {manifest['run_id']}".encode(),
                integrate.stderr,
            )
        self.assertTrue(rebase_marker.exists())
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, status_before)
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "manual resolution\n",
        )
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-pending")
        self.assertNotIn("integration_recovery_error", recovered)

    def test_interrupted_rebase_marker_is_retained_at_clean_source_head(self) -> None:
        log = self.root / "integrate-interrupted-source-marker.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]
        marker = Path(
            self.git(worker, "rev-parse", "--git-path", "rebase-merge").stdout.strip()
        )
        if not marker.is_absolute():
            marker = worker / marker
        marker.mkdir()

        manifest.update(
            {
                "state": "integration-rebase-pending",
                "integration_previous_state": "preserved",
                "integration_source_head": source_head,
                "integration_target_head": self.base_head,
                "integration_started_at": "2000-01-01T00:00:00+00:00",
            }
        )
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"integration rebase conflict remains active", integrate.stderr)
        for action in ("resolve", "continue", "abort"):
            self.assertIn(
                f"--triptych-{action} {manifest['run_id']}".encode(),
                integrate.stderr,
            )
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-pending")
        self.assertNotIn("integration_recovery_error", recovered)

    def test_integrate_reports_post_rebase_cleanup_failure_and_allows_retry(self) -> None:
        log = self.root / "integrate-post-merge.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        advanced_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        late_file = worker / "post-merge-result.txt"
        hook = self.control / ".git/hooks/post-merge"
        hook.write_text(
            f'#!/bin/sh\nprintf "%s\\n" "hook result" > "{late_file}"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"integrated, but cleanup failed", integrate.stderr)
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, manifest["final_head"])
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), advanced_head)
        failed_manifest = self.manifests()[0]
        self.assertEqual(failed_manifest["state"], "integration-cleanup-failed")
        self.assertEqual(failed_manifest["final_head"], manifest["final_head"])
        self.assertEqual(failed_manifest["integrated_head"], landed_head)
        self.assertEqual(failed_manifest["integration_candidate_head"], landed_head)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), landed_head)
        self.assertTrue(worker.exists())
        self.assertTrue(late_file.exists())

        late_file.unlink()
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_integrate_refuses_to_reland_commit_removed_from_target_history(self) -> None:
        log = self.root / "integrate-target-rewritten-after-landing.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])

        (self.control / "primary-result.txt").write_text("primary result\n", encoding="utf-8")
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary independently")
        pre_landing_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        late_file = worker / "post-merge-result.txt"
        hook = self.control / ".git/hooks/post-merge"
        hook.write_text(
            f'#!/bin/sh\nprintf "%s\\n" "hook result" > "{late_file}"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, manifest["final_head"])
        self.assertEqual(self.manifests()[0]["integrated_head"], landed_head)
        hook.unlink()
        late_file.unlink()

        self.git(self.control, "reset", "--hard", pre_landing_target)
        (self.control / "agent-result.txt").write_text("replacement target result\n", encoding="utf-8")
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Rewrite target without landed result")
        rewritten_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        refusal = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(refusal.returncode, 2)
        self.assertIn(b"no longer contains", refusal.stderr)
        self.assertIn(b"previously integrated commit", refusal.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            rewritten_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), landed_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-cleanup-failed")
        self.assertEqual(retained["integration_candidate_head"], landed_head)
        self.assertEqual(retained["integrated_head"], landed_head)

        self.git(self.control, "reset", "--hard", landed_head)
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_clean_retries_a_retained_worker_branch_deletion(self) -> None:
        log = self.root / "integrate-branch-retry.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        competing = self.root / "competing-worker"
        self.git(
            self.control,
            "worktree",
            "add",
            "--force",
            str(competing),
            manifest["branch"],
        )

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 1, integrate.stderr.decode())
        self.assertIn(b"worker branch remains", integrate.stderr)
        self.assertEqual(self.manifests()[0]["state"], "cleaned-branch-retained")
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            manifest["final_head"],
        )
        self.assertFalse(Path(manifest["worktree"]).exists())
        self.assertIn(manifest["branch"], self.worker_branches())

        self.git(self.control, "worktree", "remove", str(competing))
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        cleaned_manifest = self.manifests()[0]
        self.assertEqual(cleaned_manifest["state"], "cleaned")
        self.assertIn("branch_cleaned_at", cleaned_manifest)

    def test_clean_refuses_a_symbolic_retained_worker_branch(self) -> None:
        log = self.root / "integrate-symbolic-branch.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        competing = self.root / "symbolic-worker"
        self.git(
            self.control,
            "worktree",
            "add",
            "--force",
            str(competing),
            manifest["branch"],
        )
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 1, integrate.stderr.decode())
        self.git(self.control, "worktree", "remove", str(competing))

        branch_ref = f"refs/heads/{manifest['branch']}"
        self.git(self.control, "symbolic-ref", branch_ref, "refs/heads/main")
        target_head = self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip()
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2)
        self.assertIn(b"replaced by a symbolic ref", clean.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            target_head,
        )
        self.assertEqual(
            self.git(self.control, "symbolic-ref", branch_ref).stdout.strip(),
            "refs/heads/main",
        )

    def test_concurrent_allocations_are_unique_locked_and_isolated(self) -> None:
        processes: list[tuple[subprocess.Popen, Path]] = []
        for index in range(4):
            log = self.root / f"parallel-{index}.jsonl"
            environment = self.base_environment()
            environment.update(
                {
                    "FAKE_CODEX_LOG": str(log),
                    "FAKE_CODEX_ACTION": "dirty",
                    "FAKE_CODEX_CONTENT": f"worker {index}\n",
                    "FAKE_CODEX_SLEEP": "0.3",
                }
            )
            process = subprocess.Popen(
                [str(self.launcher), f"parallel task {index}"],
                cwd=self.control,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            processes.append((process, log))

        for process, _ in processes:
            stdout, stderr = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, (stdout, stderr))

        records = [self.records(log)[0] for _, log in processes]
        roots = {record["root"] for record in records}
        run_ids = {record["run_id"] for record in records}
        self.assertEqual(len(roots), 4)
        self.assertEqual(len(run_ids), 4)
        self.assertEqual(len(self.worktree_paths()), 5)
        self.assertEqual(len(self.worker_branches()), 4)
        output = self.worktree_output()
        self.assertEqual(output.count("locked triptych-codex"), 4)
        for index, record in enumerate(records):
            self.assertEqual(
                (Path(record["root"]) / "agent-result.txt").read_text(encoding="utf-8"),
                f"worker {index}\n",
            )
            self.assertEqual(record["head"], self.base_head)
        self.assert_control_unchanged()

    def test_status_uses_opaque_ids_without_worktree_paths(self) -> None:
        log = self.root / "status.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0)
        manifest = self.manifests()[0]
        status = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertEqual(status.returncode, 0)
        rendered = status.stdout.decode()
        self.assertIn(manifest["run_id"], rendered)
        self.assertIn("preserved", rendered)
        self.assertNotIn(manifest["worktree"], rendered)


if __name__ == "__main__":
    unittest.main()
