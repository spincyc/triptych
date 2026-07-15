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
        (self.control / "scripts").mkdir()
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
