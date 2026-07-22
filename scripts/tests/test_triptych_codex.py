#!/usr/bin/env python3
"""Black-box tests for scripts/triptych-codex."""

from __future__ import annotations

import base64
import fcntl
import json
import os
import runpy
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAKEFILE = SCRIPTS_ROOT.parent / "Makefile"
SOURCE_MAKE_FRAGMENT = (
    SCRIPTS_ROOT.parent
    / "tools/worktree-marshal/src/worktree_marshal/resources/worktree-marshal.mk"
)
SOURCE_LAUNCHER = SCRIPTS_ROOT / "triptych-codex"
SOURCE_FAKE = Path(__file__).resolve().with_name("fake-codex")
COMMAND_TIMEOUT_SECONDS = 60
LOCK_CHECKPOINT_TIMEOUT_SECONDS = 30


class RunTemporaryRemovalTests(unittest.TestCase):
    def test_leaf_replacement_is_not_recursively_deleted(self) -> None:
        launcher = runpy.run_path(str(SOURCE_LAUNCHER), run_name="triptych_codex_unit")
        run_id = "20260722t000000z-000000000000"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_root = root / "state"
            temporary_root = state_root / "tmp"
            run_temporary = temporary_root / run_id
            replacement = temporary_root / "replacement"
            displaced = temporary_root / "displaced"
            run_temporary.mkdir(parents=True)
            replacement.mkdir()
            (run_temporary / "owned.txt").write_text("owned\n", encoding="utf-8")
            (replacement / "preserved.txt").write_text(
                "preserved\n",
                encoding="utf-8",
            )
            repository = launcher["Repository"](
                root=root,
                git_dir=root / ".git",
                common_git_dir=root / ".git",
                relative_cwd=Path("."),
                linked_worktree=False,
                state_root=state_root,
            )
            manifest = {"run_id": run_id, "tmpdir": str(run_temporary)}
            real_open = os.open
            swapped = False

            def racing_open(path, flags, mode=0o777, *, dir_fd=None):
                nonlocal swapped
                if path == run_id and dir_fd is not None and not swapped:
                    swapped = True
                    os.rename(run_id, displaced.name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
                    os.rename(
                        replacement.name,
                        run_id,
                        src_dir_fd=dir_fd,
                        dst_dir_fd=dir_fd,
                    )
                return real_open(path, flags, mode, dir_fd=dir_fd)

            with mock.patch.object(launcher["os"], "open", side_effect=racing_open):
                with self.assertRaisesRegex(
                    launcher["LauncherError"],
                    "changed before removal",
                ):
                    launcher["remove_run_tmpdir"](repository, manifest)

            self.assertTrue(swapped)
            self.assertEqual(
                (run_temporary / "preserved.txt").read_text(encoding="utf-8"),
                "preserved\n",
            )
            self.assertEqual(
                (displaced / "owned.txt").read_text(encoding="utf-8"),
                "owned\n",
            )


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
        make_fragment = (
            self.control
            / "tools/worktree-marshal/src/worktree_marshal/resources/worktree-marshal.mk"
        )
        make_fragment.parent.mkdir(parents=True)
        shutil.copy2(SOURCE_MAKE_FRAGMENT, make_fragment)
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
        timeout: float = COMMAND_TIMEOUT_SECONDS,
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
        merged["CODEX"] = str(self.fake)
        if environment:
            merged.update(environment)
        return subprocess.run(
            ["make", "--no-print-directory", *arguments],
            cwd=self.control,
            env=merged,
            capture_output=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
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

    def source_anchor_ref(self, run_id: str) -> str:
        return f"refs/triptych-codex/runs/{run_id}/integration-source"

    def retirement_anchor_ref(self, run_id: str) -> str:
        return f"refs/triptych-codex/runs/{run_id}/retirement-discard"

    def retirement_receipt_ref(self, run_id: str) -> str:
        return f"refs/triptych-codex/runs/{run_id}/retirement-receipt"

    def direct_ref_commit(self, ref: str) -> str | None:
        symbolic = self.git(
            self.control,
            "symbolic-ref",
            "--quiet",
            ref,
            check=False,
        )
        self.assertIn(symbolic.returncode, (0, 1), symbolic.stderr)
        if symbolic.returncode == 0:
            return None
        resolved = self.git(
            self.control,
            "rev-parse",
            "--verify",
            f"{ref}^{{commit}}",
            check=False,
        )
        self.assertIn(resolved.returncode, (0, 128), resolved.stderr)
        return resolved.stdout.strip() if resolved.returncode == 0 else None

    def retirement_ref_tuple(
        self,
        manifest: dict,
    ) -> tuple[str | None, str | None, str | None]:
        return (
            self.direct_ref_commit(f"refs/heads/{manifest['branch']}"),
            self.direct_ref_commit(self.retirement_anchor_ref(manifest["run_id"])),
            self.direct_ref_commit(self.retirement_receipt_ref(manifest["run_id"])),
        )

    def expire_reflogs_and_prune(self) -> None:
        self.git(
            self.control,
            "reflog",
            "expire",
            "--expire=now",
            "--expire-unreachable=now",
            "--all",
        )
        self.git(self.control, "gc", "--prune=now")

    def commit_exists(self, commit: str) -> bool:
        return (
            self.git(
                self.control,
                "cat-file",
                "-e",
                f"{commit}^{{commit}}",
                check=False,
            ).returncode
            == 0
        )

    def manifest_file(self, manifest: dict) -> Path:
        return self.repo_state() / "runs" / f"{manifest['run_id']}.json"

    def write_test_manifest(self, manifest: dict) -> None:
        self.manifest_file(manifest).write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def retire_arguments(
        self,
        manifest: dict,
        *,
        discard_head: str | None = None,
        target_contains: str | None = None,
    ) -> list[str]:
        return [
            "--triptych-retire",
            manifest["run_id"],
            "--discard-head",
            discard_head or manifest["observed_head"],
            "--target-contains",
            target_contains or self.git(
                self.control,
                "rev-parse",
                "--verify",
                f"{manifest['target_ref']}^{{commit}}",
            ).stdout.strip(),
        ]

    def create_rewritten_quarantine(self) -> tuple[dict, Path, str, str, str]:
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "retirement-first.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        final_head = manifest["final_head"]

        second = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(self.root / "retirement-rewrite.jsonl"),
                "FAKE_CODEX_ACTION": "rewrite-sibling",
            },
        )
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        quarantined = self.manifests()[0]
        discard_head = quarantined["observed_head"]
        target_head = self.git(
            self.control,
            "rev-parse",
            "--verify",
            f"{quarantined['target_ref']}^{{commit}}",
        ).stdout.strip()
        self.assertEqual(quarantined["state"], "quarantined")
        self.assertFalse(quarantined["observed_dirty"])
        self.assertNotEqual(final_head, discard_head)
        self.assertNotEqual(target_head, discard_head)
        self.assertEqual(
            self.git(worker, "rev-parse", f"{final_head}^").stdout.strip(),
            self.base_head,
        )
        self.assertEqual(
            self.git(worker, "rev-parse", f"{discard_head}^").stdout.strip(),
            self.base_head,
        )
        self.assertEqual(
            self.git(
                self.control,
                "merge-base",
                "--is-ancestor",
                discard_head,
                target_head,
                check=False,
            ).returncode,
            1,
        )
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD").stdout.strip(),
            discard_head,
        )
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        return quarantined, worker, final_head, discard_head, target_head

    def post_git_action_environment(
        self,
        *,
        cwd: Path,
        tokens: list[str],
        marker: Path,
        action: str = "kill-parent",
        dirty_path: Path | None = None,
        dangling_link: tuple[Path, Path] | None = None,
        move_ref: tuple[str, str, str] | None = None,
    ) -> dict[str, str]:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        wrapper_directory = self.root / f"git-action-{marker.name}"
        wrapper_directory.mkdir()
        wrapper = wrapper_directory / "git"
        wrapper.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, signal, subprocess, sys, time\n"
            "args = sys.argv[1:]\n"
            "tokens = json.loads(os.environ['TRIPTYCH_TEST_GIT_TOKENS'])\n"
            "matched = (pathlib.Path.cwd().resolve() == "
            "pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_CWD']).resolve() and "
            "all(token in args for token in tokens) and "
            "not pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_MARKER']).exists())\n"
            "action = os.environ['TRIPTYCH_TEST_GIT_ACTION']\n"
            "marker = pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_MARKER'])\n"
            "if matched and action == 'kill-parent-before':\n"
            "    marker.write_text('matched-before\\n', encoding='utf-8')\n"
            "    os.kill(os.getppid(), signal.SIGKILL)\n"
            "    time.sleep(0.05)\n"
            "    raise SystemExit(94)\n"
            "if matched and action == 'refuse':\n"
            "    marker.write_text('refused\\n', encoding='utf-8')\n"
            "    raise SystemExit(93)\n"
            "if matched and action == 'move-ref':\n"
            "    marker.write_text('moved\\n', encoding='utf-8')\n"
            "    subprocess.run([os.environ['TRIPTYCH_TEST_REAL_GIT'], "
            "'update-ref', os.environ['TRIPTYCH_TEST_MOVE_REF'], "
            "os.environ['TRIPTYCH_TEST_MOVE_NEW'], "
            "os.environ['TRIPTYCH_TEST_MOVE_OLD']], check=True)\n"
            "payload = sys.stdin.buffer.read()\n"
            "result = subprocess.run([os.environ['TRIPTYCH_TEST_REAL_GIT'], *args], "
            "input=payload)\n"
            "if matched:\n"
            "    marker.write_text('matched\\n', encoding='utf-8')\n"
            "    if action == 'kill-parent':\n"
            "        os.kill(os.getppid(), signal.SIGKILL)\n"
            "        time.sleep(0.05)\n"
            "    elif action == 'dirty':\n"
            "        pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_DIRTY']).write_text("
            "'post-Git dirt\\n', encoding='utf-8')\n"
            "    elif action == 'dangling-symlink':\n"
            "        pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_LINK']).symlink_to("
            "pathlib.Path(os.environ['TRIPTYCH_TEST_GIT_LINK_TARGET']), "
            "target_is_directory=True)\n"
            "raise SystemExit(result.returncode)\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        environment = {
            "PATH": f"{wrapper_directory}{os.pathsep}{os.environ['PATH']}",
            "TRIPTYCH_TEST_REAL_GIT": real_git or "git",
            "TRIPTYCH_TEST_GIT_CWD": str(cwd),
            "TRIPTYCH_TEST_GIT_TOKENS": json.dumps(tokens),
            "TRIPTYCH_TEST_GIT_MARKER": str(marker),
            "TRIPTYCH_TEST_GIT_ACTION": action,
        }
        if dirty_path is not None:
            environment["TRIPTYCH_TEST_GIT_DIRTY"] = str(dirty_path)
        if dangling_link is not None:
            link, target = dangling_link
            environment["TRIPTYCH_TEST_GIT_LINK"] = str(link)
            environment["TRIPTYCH_TEST_GIT_LINK_TARGET"] = str(target)
        if move_ref is not None:
            ref, new, old = move_ref
            environment["TRIPTYCH_TEST_MOVE_REF"] = ref
            environment["TRIPTYCH_TEST_MOVE_NEW"] = new
            environment["TRIPTYCH_TEST_MOVE_OLD"] = old
        return environment

    def landing_race_environment(
        self,
        *,
        marker: Path,
        action: str,
    ) -> dict[str, str]:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        wrapper_directory = self.root / f"landing-race-{action}"
        wrapper_directory.mkdir()
        wrapper = wrapper_directory / "git"
        wrapper.write_text(
            "#!/usr/bin/env python3\n"
            "import os, pathlib, subprocess, sys\n"
            "args = sys.argv[1:]\n"
            "marker = pathlib.Path(os.environ['TRIPTYCH_TEST_LANDING_MARKER'])\n"
            "control = pathlib.Path(os.environ['TRIPTYCH_TEST_LANDING_CONTROL'])\n"
            "real_git = os.environ['TRIPTYCH_TEST_REAL_GIT']\n"
            "matched = (pathlib.Path.cwd().resolve() == control.resolve() and "
            "'update-ref' in args and '--no-deref' in args and "
            "'refs/heads/main' in args and not marker.exists())\n"
            "if matched:\n"
            "    marker.write_text('raced\\n', encoding='utf-8')\n"
            "    action = os.environ['TRIPTYCH_TEST_LANDING_ACTION']\n"
            "    if action == 'checkout':\n"
            "        subprocess.run([real_git, '-C', str(control), 'switch', "
            "'side'], check=True)\n"
            "    elif action == 'symref':\n"
            "        subprocess.run([real_git, '-C', str(control), "
            "'symbolic-ref', 'HEAD', 'refs/heads/side'], check=True)\n"
            "    elif action == 'ref':\n"
            "        old = subprocess.run([real_git, '-C', str(control), "
            "'rev-parse', 'refs/heads/main^{commit}'], check=True, "
            "capture_output=True, text=True).stdout.strip()\n"
            "        tree = subprocess.run([real_git, '-C', str(control), "
            "'rev-parse', old + '^{tree}'], check=True, capture_output=True, "
            "text=True).stdout.strip()\n"
            "        raced = subprocess.run([real_git, '-C', str(control), "
            "'commit-tree', tree, '-p', old, '-m', 'Race target CAS'], "
            "check=True, capture_output=True, text=True).stdout.strip()\n"
            "        subprocess.run([real_git, '-C', str(control), 'update-ref', "
            "'refs/heads/main', raced, old], check=True)\n"
            "        pathlib.Path(os.environ['TRIPTYCH_TEST_LANDING_RACED_HEAD']).write_text("
            "raced + '\\n', encoding='utf-8')\n"
            "    else:\n"
            "        raise SystemExit('unknown landing race action')\n"
            "payload = sys.stdin.buffer.read()\n"
            "result = subprocess.run([real_git, *args], input=payload)\n"
            "raise SystemExit(result.returncode)\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        return {
            "PATH": f"{wrapper_directory}{os.pathsep}{os.environ['PATH']}",
            "TRIPTYCH_TEST_REAL_GIT": real_git or "git",
            "TRIPTYCH_TEST_LANDING_CONTROL": str(self.control),
            "TRIPTYCH_TEST_LANDING_MARKER": str(marker),
            "TRIPTYCH_TEST_LANDING_ACTION": action,
            "TRIPTYCH_TEST_LANDING_RACED_HEAD": str(
                self.root / f"landing-raced-head-{action}"
            ),
        }

    def slow_landing_git_environment(
        self,
        *,
        marker: Path,
        release: Path,
    ) -> dict[str, str]:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        wrapper_directory = self.root / "slow-landing-git"
        wrapper_directory.mkdir()
        wrapper = wrapper_directory / "git"
        wrapper.write_text(
            "#!/usr/bin/env python3\n"
            "import os, pathlib, signal, sys, time\n"
            "args = sys.argv[1:]\n"
            "marker = pathlib.Path(os.environ['TRIPTYCH_TEST_SLOW_MARKER'])\n"
            "matched = ('update-ref' in args and '--no-deref' in args and "
            "'refs/heads/main' in args and not marker.exists())\n"
            "if matched:\n"
            "    marker.write_text('orphan owns locks\\n', encoding='utf-8')\n"
            "    os.kill(os.getppid(), signal.SIGKILL)\n"
            "    release = pathlib.Path(os.environ['TRIPTYCH_TEST_SLOW_RELEASE'])\n"
            "    while not release.exists():\n"
            "        time.sleep(0.01)\n"
            "os.execv(os.environ['TRIPTYCH_TEST_REAL_GIT'], "
            "[os.environ['TRIPTYCH_TEST_REAL_GIT'], *args])\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        return {
            "PATH": f"{wrapper_directory}{os.pathsep}{os.environ['PATH']}",
            "TRIPTYCH_TEST_REAL_GIT": real_git or "git",
            "TRIPTYCH_TEST_SLOW_MARKER": str(marker),
            "TRIPTYCH_TEST_SLOW_RELEASE": str(release),
        }

    def retained_admin_directory(self, worker: Path) -> Path:
        pointer = (worker / ".git").read_text(encoding="utf-8")
        self.assertTrue(pointer.startswith("gitdir: "), pointer)
        return Path(pointer.removeprefix("gitdir: ").strip())

    def assert_retained_admin_tamper_rejected(self, component: str) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / f"admin-{component}-worker.jsonl"),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        admin = self.retained_admin_directory(worker)
        if component == ".git":
            (worker / ".git").write_text(
                f"gitdir: {self.control / '.git'}\n",
                encoding="utf-8",
            )
        elif component == "commondir":
            (admin / "commondir").write_text(
                f"{self.control / '.git/worktrees'}\n",
                encoding="utf-8",
            )
        else:
            self.assertEqual(component, "gitdir")
            (admin / "gitdir").write_text(
                f"{self.control / '.git/HEAD'}\n",
                encoding="utf-8",
            )
        reopen_log = self.root / f"admin-{component}-reopen.jsonl"

        reopen = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(reopen_log)},
        )

        self.assertEqual(reopen.returncode, 2)
        diagnostic = reopen.stderr.lower()
        self.assertIn(b"worktree", diagnostic)
        self.assertFalse(reopen_log.exists())

    def prepare_successful_rebase(self) -> tuple[dict, Path, str, str]:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "successful-rebase-worker.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]
        (self.control / "primary-result.txt").write_text(
            "independent primary result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "primary-result.txt")
        self.git(self.control, "commit", "-m", "Advance primary for rebase")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        return manifest, worker, source_head, target_head

    def assert_landing_race(self, *, manual: bool, action: str) -> None:
        if manual:
            manifest, worker, _, target_head = self.create_review_pending_candidate()
        else:
            manifest, worker, _, target_head = self.prepare_successful_rebase()
        self.git(self.control, "branch", "side", target_head)
        marker = self.root / f"{'manual' if manual else 'ordinary'}-{action}-race"

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.landing_race_environment(marker=marker, action=action),
        )

        self.assertTrue(marker.exists())
        if action in {"checkout", "symref"}:
            self.assertEqual(landing.returncode, 0, landing.stderr.decode())
            cleaned = self.manifests()[0]
            candidate = cleaned["integrated_head"]
            self.assertEqual(cleaned["state"], "cleaned")
            self.assertEqual(
                self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
                candidate,
            )
            self.assertEqual(
                self.git(self.control, "symbolic-ref", "HEAD").stdout.strip(),
                "refs/heads/side",
            )
            self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
            self.assertEqual(
                self.git(self.control, "write-tree").stdout.strip(),
                self.git(self.control, "rev-parse", "HEAD^{tree}").stdout.strip(),
            )
            self.assertEqual(
                self.git(
                    self.control,
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                ).stdout,
                "",
            )
            self.assertFalse(worker.exists())
            return

        self.assertEqual(action, "ref")
        self.assertEqual(landing.returncode, 2)
        raced_path = self.root / "landing-raced-head-ref"
        raced_head = raced_path.read_text(encoding="utf-8").strip()
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            raced_head,
        )
        self.assertNotEqual(raced_head, target_head)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), raced_head)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            "",
        )
        retained = self.manifests()[0]
        if manual:
            self.assertEqual(retained["integration_landing_expected_head"], target_head)
            self.assertEqual(
                self.git(worker, "rev-parse", "HEAD").stdout.strip(),
                retained["integration_landing_candidate_head"],
            )
        else:
            self.assertEqual(retained["state"], "preserved")
            self.assertEqual(
                self.git(worker, "rev-parse", "HEAD").stdout.strip(),
                retained["final_head"],
            )
            self.assertNotIn("integration_landing_candidate_head", retained)

        self.git(
            self.control,
            "update-ref",
            "refs/heads/main",
            target_head,
            raced_head,
        )
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def assert_abort_ignores_target_change(self, change: str) -> None:
        manifest, worker, _, target_head = self.create_review_pending_candidate()
        source_head = self.manifests()[0]["integration_source_head"]
        self.git(self.control, "branch", "side", target_head)
        self.git(self.control, "switch", "side")
        primary_ref = self.git(self.control, "symbolic-ref", "HEAD").stdout.strip()
        primary_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        primary_tree = self.git(self.control, "write-tree").stdout.strip()

        if change == "deleted":
            self.git(self.control, "update-ref", "-d", "refs/heads/main", target_head)
            expected_target = None
        elif change == "rewound":
            self.git(
                self.control,
                "update-ref",
                "refs/heads/main",
                self.base_head,
                target_head,
            )
            expected_target = self.base_head
        else:
            self.assertEqual(change, "unrelated")
            tree = self.git(self.control, "rev-parse", f"{self.base_head}^{{tree}}").stdout.strip()
            unrelated = subprocess.run(
                [
                    "git",
                    "commit-tree",
                    tree,
                    "-p",
                    self.base_head,
                    "-m",
                    "Unrelated target rewrite",
                ],
                cwd=self.control,
                env=self.base_environment(),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.git(
                self.control,
                "update-ref",
                "refs/heads/main",
                unrelated,
                target_head,
            )
            expected_target = unrelated

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        target = self.git(
            self.control,
            "rev-parse",
            "--verify",
            "refs/heads/main^{commit}",
            check=False,
        )
        if expected_target is None:
            self.assertNotEqual(target.returncode, 0)
        else:
            self.assertEqual(target.returncode, 0)
            self.assertEqual(target.stdout.strip(), expected_target)
        self.assertEqual(self.git(self.control, "symbolic-ref", "HEAD").stdout.strip(), primary_ref)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), primary_head)
        self.assertEqual(self.git(self.control, "write-tree").stdout.strip(), primary_tree)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            "",
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.manifests()[0]["state"], "preserved")

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

    def active_rebase_paths(self, worker: Path) -> list[Path]:
        paths = []
        for name in ("rebase-merge", "rebase-apply"):
            path = Path(self.git(worker, "rev-parse", "--git-path", name).stdout.strip())
            if not path.is_absolute():
                path = worker / path
            if path.exists():
                paths.append(path)
        return paths

    def prepare_integration_conflict(self) -> tuple[dict, Path, str, str]:
        log = self.root / "integration-conflict-worker.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]

        (self.control / "agent-result.txt").write_text(
            "conflicting primary result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Add conflicting primary result")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        return manifest, worker, source_head, target_head

    def create_integration_conflict(
        self,
    ) -> tuple[dict, Path, str, str, subprocess.CompletedProcess]:
        manifest, worker, source_head, target_head = self.prepare_integration_conflict()
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        return manifest, worker, source_head, target_head, integrate

    def resolve_integration_conflict(
        self,
        manifest: dict,
        *,
        log_name: str = "integration-conflict-resolver.jsonl",
        content: str = "manually resolved result\n",
        conflict_path: str = "agent-result.txt",
    ) -> tuple[subprocess.CompletedProcess, Path]:
        log = self.root / log_name
        result = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_CONTENT": content,
                "FAKE_CODEX_CONFLICT_PATH": conflict_path,
            },
        )
        return result, log

    def create_interrupted_manual_verification(
        self,
        *,
        advance_target: bool,
    ) -> tuple[dict, Path, str, str]:
        manifest, worker, _, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        pending = self.manifests()[0]
        candidate = pending["integration_candidate_head"]

        self.git(self.control, "merge", "--ff-only", candidate)
        pending["state"] = "integration-verification-pending"
        pending["integrated_head"] = candidate
        pending["integrated_at"] = "2000-01-01T00:00:00+00:00"
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(pending, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        target_head = candidate
        if advance_target:
            (self.control / "target-after-pending-verification.txt").write_text(
                "target advanced after interrupted verification\n",
                encoding="utf-8",
            )
            self.git(self.control, "add", "target-after-pending-verification.txt")
            self.git(
                self.control,
                "commit",
                "-m",
                "Advance target after interrupted manual verification",
            )
            target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        return pending, worker, candidate, target_head

    def create_review_pending_candidate(self) -> tuple[dict, Path, str, str]:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        review = self.manifests()[0]
        return manifest, worker, review["integration_candidate_head"], target_head

    def create_pre_landing_manual_verification_failure(
        self,
    ) -> tuple[dict, Path, str, str, str]:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        review = self.manifests()[0]
        source_head = review["integration_source_head"]
        (self.control / "target-before-manual-landing.txt").write_text(
            "target advanced before manual landing\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "target-before-manual-landing.txt")
        self.git(self.control, "commit", "-m", "Advance target before manual landing")
        advanced_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        landing = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(landing.returncode, 2)
        failed = self.manifests()[0]
        self.assertEqual(failed["state"], "integration-verification-failed")
        self.assertTrue(failed["integration_manual_resolution"])
        self.assertEqual(failed["integration_candidate_head"], candidate)
        self.assertNotIn("integrated_head", failed)
        for field in (
            "integration_manual_landing_started_at",
            "integration_landing_expected_head",
            "integration_landing_candidate_head",
            "integration_landing_started_at",
        ):
            self.assertNotIn(field, failed)
        return failed, worker, source_head, candidate, advanced_target

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
        manifest = self.manifests()[0]
        self.assertEqual(
            record["temporary_environment"],
            {name: manifest["tmpdir"] for name in ("TMPDIR", "TMP", "TEMP")},
        )
        self.assert_control_unchanged()

    def test_post_git_ordinary_branch_cleanup_crash_is_idempotent(self) -> None:
        marker = self.root / "post-ordinary-branch-cleanup-kill"
        environment = self.post_git_action_environment(
            cwd=self.control,
            tokens=["update-ref", "--stdin"],
            marker=marker,
        )
        environment["FAKE_CODEX_LOG"] = str(self.root / "ordinary-cleanup-worker.jsonl")

        crashed = self.run_launcher(environment=environment)

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "cleaned-branch-retained")
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertFalse(Path(manifest["tmpdir"]).exists())

        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

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

    def test_rejects_command_bearing_git_configuration_before_allocation(self) -> None:
        marker = self.root / "unsafe-git-config-called"
        command = self.root / "unsafe-git-config"
        command.write_text(
            "#!/bin/sh\n"
            f'printf "%s\\n" called >> "{marker}"\n'
            "exit 0\n",
            encoding="utf-8",
        )
        command.chmod(0o755)
        for index, key in enumerate(
            (
                "core.fsmonitor",
                "filter.triptych.process",
                "merge.triptych.driver",
                "diff.triptych.textconv",
            )
        ):
            with self.subTest(key=key):
                self.git(self.control, "config", key, str(command))
                log = self.root / f"unsafe-git-config-{index}.jsonl"
                result = self.run_launcher(
                    environment={"FAKE_CODEX_LOG": str(log)}
                )
                self.git(self.control, "config", "--unset-all", key)
                self.assertEqual(result.returncode, 2)
                self.assertIn(b"unsafe command-bearing Git configuration", result.stderr)
                self.assertFalse(log.exists())
                self.assertFalse(marker.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

    def test_worker_environment_removes_git_redirection_and_config_injection(self) -> None:
        log = self.root / "sanitized-git-environment.jsonl"
        trace = self.root / "unsafe-git-trace"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "CDPATH": "/tmp",
                "EDITOR": "unsafe-editor",
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.fsmonitor",
                "GIT_CONFIG_VALUE_0": "/unsafe/fsmonitor",
                "GIT_DIR": "/unsafe/git-dir",
                "GIT_EDITOR": "unsafe-git-editor",
                "GIT_EXEC_PATH": "/unsafe/git-exec-path",
                "GIT_EXTERNAL_DIFF": "/unsafe/external-diff",
                "GIT_TRACE": str(trace),
                "GIT_WORK_TREE": "/unsafe/worktree",
                "SSH_ASKPASS": "/unsafe/askpass",
                "VISUAL": "unsafe-visual",
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode())
        recorded = self.records(log)[0]["git_environment"]
        for name in (
            "CDPATH",
            "GIT_CONFIG_COUNT",
            "GIT_CONFIG_KEY_0",
            "GIT_CONFIG_VALUE_0",
            "GIT_DIR",
            "GIT_EXEC_PATH",
            "GIT_EXTERNAL_DIFF",
            "GIT_TRACE",
            "GIT_WORK_TREE",
            "SSH_ASKPASS",
        ):
            self.assertNotIn(name, recorded)
        self.assertEqual(recorded["EDITOR"], ":")
        self.assertEqual(recorded["GIT_EDITOR"], ":")
        self.assertEqual(recorded["VISUAL"], ":")
        self.assertEqual(recorded["GIT_CONFIG_GLOBAL"], os.devnull)
        self.assertEqual(recorded["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(recorded["GIT_ATTR_GLOBAL"], os.devnull)
        self.assertEqual(recorded["GIT_ATTR_NOSYSTEM"], "1")
        self.assertEqual(recorded["GIT_NO_REPLACE_OBJECTS"], "1")
        self.assertEqual(recorded["GIT_OPTIONAL_LOCKS"], "1")
        self.assertFalse(trace.exists())

    def test_launcher_pins_resolved_git_before_the_worker_changes_path_entry(self) -> None:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        git_directory = self.root / "mutable-git-path"
        git_directory.mkdir()
        git_link = git_directory / "git"
        git_link.symlink_to(real_git or "git")
        marker = self.root / "replacement-git-called"
        replacement = self.root / "replacement-git"
        replacement.write_text(
            "#!/bin/sh\n"
            f'printf "%s\\n" called >> "{marker}"\n'
            "exit 97\n",
            encoding="utf-8",
        )
        replacement.chmod(0o755)
        log = self.root / "pinned-git-worker.jsonl"

        result = self.run_launcher(
            environment={
                "PATH": f"{git_directory}{os.pathsep}{os.environ['PATH']}",
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "retarget-git",
                "FAKE_CODEX_GIT_LINK": str(git_link),
                "FAKE_CODEX_GIT_REPLACEMENT": str(replacement),
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(git_link.resolve(), replacement.resolve())
        self.assertFalse(marker.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])

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

        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 2, clean.stderr.decode())
        self.assertIn(b"quarantined run", clean.stderr)
        self.assertIn(b"no retirement checkpoint", clean.stderr)
        self.assertNotIn(b"rewritten quarantine", clean.stderr)
        self.assertEqual(self.manifests()[0]["state"], "quarantined")
        self.assertTrue(Path(manifest["worktree"]).exists())

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

    def test_reopen_rejects_unsafe_manifest_relative_cwd(self) -> None:
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(self.root / "relative-cwd-worker.jsonl")}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"

        for index, unsafe in enumerate(("../outside", "/tmp/outside")):
            with self.subTest(relative_cwd=unsafe):
                tampered = dict(manifest)
                tampered["relative_cwd"] = unsafe
                manifest_file.write_text(
                    json.dumps(tampered, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                log = self.root / f"unsafe-relative-{index}.jsonl"
                reopen = self.run_launcher(
                    ["--triptych-reopen", manifest["run_id"]],
                    environment={"FAKE_CODEX_LOG": str(log)},
                )
                self.assertEqual(reopen.returncode, 2)
                self.assertIn(b"unsafe relative working directory", reopen.stderr)
                self.assertNotIn(os.fsencode(manifest["worktree"]), reopen.stderr)
                self.assertFalse(log.exists())

    def test_reopen_rejects_symlinked_worktree_and_tmpdir_leaves(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "symlink-worker.jsonl"),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]

        worker = Path(manifest["worktree"])
        moved_worker = self.root / "moved-managed-worker"
        worker.rename(moved_worker)
        outside_worker = self.root / "outside-worker"
        outside_worker.mkdir()
        worker.symlink_to(outside_worker, target_is_directory=True)
        worktree_reopen = self.run_launcher(["--triptych-reopen", manifest["run_id"]])
        self.assertEqual(worktree_reopen.returncode, 2)
        self.assertIn(b"unsafe worktree path", worktree_reopen.stderr)
        self.assertNotIn(os.fsencode(manifest["worktree"]), worktree_reopen.stderr)

        worker.unlink()
        moved_worker.rename(worker)
        temporary = Path(manifest["tmpdir"])
        shutil.rmtree(temporary)
        outside_tmp = self.root / "outside-tmp"
        outside_tmp.mkdir()
        temporary.symlink_to(outside_tmp, target_is_directory=True)
        tmp_reopen = self.run_launcher(["--triptych-reopen", manifest["run_id"]])
        self.assertEqual(tmp_reopen.returncode, 2)
        self.assertIn(b"unsafe temporary path", tmp_reopen.stderr)
        self.assertNotIn(os.fsencode(manifest["tmpdir"]), tmp_reopen.stderr)

    def test_reopen_rejects_a_symlinked_tmp_root_before_launch(self) -> None:
        log = self.root / "symlinked-tmp-root-worker.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        temporary_root = self.repo_state() / "tmp"
        moved_root = self.root / "moved-tmp-root"
        outside_root = self.root / "outside-tmp-root"
        temporary_root.rename(moved_root)
        outside_root.mkdir()
        (outside_root / "preserved.txt").write_text("outside\n", encoding="utf-8")
        temporary_root.symlink_to(outside_root, target_is_directory=True)
        reopen_log = self.root / "symlinked-tmp-root-reopen.jsonl"
        try:
            reopen = self.run_launcher(
                ["--triptych-reopen", manifest["run_id"]],
                environment={"FAKE_CODEX_LOG": str(reopen_log)},
            )
            self.assertEqual(reopen.returncode, 2)
            self.assertIn(b"not a real directory", reopen.stderr)
            self.assertFalse(reopen_log.exists())
            self.assertEqual(
                (outside_root / "preserved.txt").read_text(encoding="utf-8"),
                "outside\n",
            )
        finally:
            temporary_root.unlink()
            moved_root.rename(temporary_root)

    def test_reopen_rejects_a_non_directory_tmpdir_before_launch(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "regular-tmp-worker.jsonl"),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        temporary = Path(manifest["tmpdir"])
        shutil.rmtree(temporary)
        temporary.write_text("preserve this obstruction\n", encoding="utf-8")
        reopen_log = self.root / "regular-tmp-reopen.jsonl"

        reopen = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(reopen_log)},
        )

        self.assertEqual(reopen.returncode, 2)
        self.assertIn(b"not an exact real directory", reopen.stderr)
        self.assertFalse(reopen_log.exists())
        self.assertEqual(
            temporary.read_text(encoding="utf-8"),
            "preserve this obstruction\n",
        )

    def test_reopen_rejects_noncanonical_equivalent_tmpdir(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "noncanonical-tmp-worker.jsonl"),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        canonical = Path(manifest["tmpdir"])
        detour = canonical.parent / "detour"
        detour.mkdir()
        manifest["tmpdir"] = str(detour / ".." / manifest["run_id"])
        self.write_test_manifest(manifest)
        before = self.manifest_file(manifest).read_bytes()

        reopen = self.run_launcher(["--triptych-reopen", manifest["run_id"]])

        self.assertEqual(reopen.returncode, 2)
        self.assertIn(b"exact launcher path", reopen.stderr)
        self.assertEqual(self.manifest_file(manifest).read_bytes(), before)
        self.assertTrue(Path(manifest["worktree"]).is_dir())
        self.assertTrue(canonical.is_dir())

    def test_reopen_authenticates_retained_worktree_git_file(self) -> None:
        self.assert_retained_admin_tamper_rejected(".git")

    def test_reopen_authenticates_retained_worktree_commondir(self) -> None:
        self.assert_retained_admin_tamper_rejected("commondir")

    def test_reopen_authenticates_retained_worktree_gitdir_backlink(self) -> None:
        self.assert_retained_admin_tamper_rejected("gitdir")

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
        self.assertIn(b"quarantined run", clean.stderr)
        self.assertIn(b"no retirement checkpoint", clean.stderr)
        self.assertNotIn(b"rewritten quarantine", clean.stderr)

    def test_retire_cli_is_direct_only_and_requires_exact_full_commit_ids(self) -> None:
        manifest, worker, final_head, discard_head, target_head = (
            self.create_rewritten_quarantine()
        )
        before = self.manifest_file(manifest).read_bytes()
        tree_id = self.git(
            self.control,
            "rev-parse",
            f"{target_head}^{{tree}}",
        ).stdout.strip()
        malformed = (
            ["--triptych-retire"],
            ["--triptych-retire", manifest["run_id"]],
            [
                "--triptych-retire",
                manifest["run_id"],
                "--discard-head",
                discard_head,
            ],
            [
                "--triptych-retire",
                manifest["run_id"],
                "--discard-head",
                discard_head,
                "--target-contains",
            ],
            [
                *self.retire_arguments(manifest),
                "unexpected-extra-argument",
            ],
            [
                "--triptych-retire",
                manifest["run_id"],
                "--discard-head",
                discard_head,
                "--discard-head",
                discard_head,
                "--target-contains",
                target_head,
            ],
            self.retire_arguments(
                manifest,
                discard_head=discard_head[:12],
            ),
            self.retire_arguments(
                manifest,
                target_contains=target_head[:12],
            ),
            self.retire_arguments(
                manifest,
                discard_head="g" * len(discard_head),
            ),
            self.retire_arguments(
                manifest,
                target_contains=target_head.upper(),
            ),
            self.retire_arguments(manifest, discard_head=tree_id),
            self.retire_arguments(manifest, target_contains=tree_id),
        )

        for arguments in malformed:
            with self.subTest(arguments=arguments):
                refusal = self.run_launcher(arguments)
                self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
                self.assertEqual(self.manifest_file(manifest).read_bytes(), before)
                self.assertTrue(worker.exists())
                self.assertIn(manifest["branch"], self.worker_branches())
                self.assertEqual(
                    self.git(
                        self.control,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        self.retirement_anchor_ref(manifest["run_id"]),
                        check=False,
                    ).returncode,
                    1,
                )

        launcher_help = self.run_launcher(["--triptych-help"])
        self.assertEqual(launcher_help.returncode, 0, launcher_help.stderr.decode())
        self.assertIn(
            b"--triptych-retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID",
            launcher_help.stdout,
        )
        help_text = launcher_help.stdout.lower()
        self.assertIn(b"direct", help_text)
        self.assertIn(b"no make wrapper", help_text)
        self.assertIn(b"operator-selected", help_text)
        self.assertIn(b"reachability checkpoint", help_text)
        self.assertIn(b"semantic equivalence", help_text)

        make_help = self.run_make(["help"])
        self.assertEqual(make_help.returncode, 0, make_help.stderr.decode())
        self.assertNotIn(b"make retire", make_help.stdout)
        plain_make_retire = self.run_make(["retire"])
        self.assertEqual(plain_make_retire.returncode, 2)
        self.assertIn(b"No rule to make target", plain_make_retire.stderr)
        make_retire = self.run_make(["retire", manifest["run_id"]])
        self.assertEqual(make_retire.returncode, 2)
        self.assertIn(b"No rule to make target", make_retire.stderr)

    def test_retire_requires_primary_checkout_invocation(self) -> None:
        manifest, worker, _, _, _ = self.create_rewritten_quarantine()
        before = self.manifest_file(manifest).read_bytes()

        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            cwd=worker,
        )

        self.assertEqual(refusal.returncode, 2)
        self.assertIn(b"primary checkout", refusal.stderr)
        self.assertEqual(self.manifest_file(manifest).read_bytes(), before)
        self.assertTrue(worker.exists())

    def test_retire_refuses_noncanonical_equivalent_tmpdir_before_checkpoint(
        self,
    ) -> None:
        manifest, worker, _, discard_head, target_head = (
            self.create_rewritten_quarantine()
        )
        canonical_tmpdir = Path(manifest["tmpdir"])
        detour = canonical_tmpdir.parent / "sub"
        detour.mkdir()
        manifest["tmpdir"] = str(detour / ".." / manifest["run_id"])
        self.assertNotEqual(manifest["tmpdir"], str(canonical_tmpdir))
        self.assertEqual(Path(manifest["tmpdir"]).resolve(), canonical_tmpdir.resolve())
        self.write_test_manifest(manifest)

        manifest_before = self.manifest_file(manifest).read_bytes()
        worktrees_before = self.worktree_output()
        worktree_paths_before = self.worktree_paths()
        worker_metadata = worker.stat()
        refs_before = self.retirement_ref_tuple(manifest)
        target_before = self.direct_ref_commit(manifest["target_ref"])
        self.assertEqual(refs_before, (discard_head, None, None))
        self.assertEqual(target_before, target_head)
        self.assertTrue(canonical_tmpdir.is_dir())

        refusal = self.run_launcher(self.retire_arguments(manifest))

        self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
        self.assertIn(b"exact launcher path", refusal.stderr)
        self.assertEqual(self.manifest_file(manifest).read_bytes(), manifest_before)
        self.assertEqual(self.manifests()[0]["state"], "quarantined")
        self.assertEqual(self.worktree_output(), worktrees_before)
        self.assertEqual(self.worktree_paths(), worktree_paths_before)
        self.assertTrue(worker.is_dir())
        retained_metadata = worker.stat()
        self.assertEqual(
            (retained_metadata.st_dev, retained_metadata.st_ino),
            (worker_metadata.st_dev, worker_metadata.st_ino),
        )
        self.assertEqual(self.retirement_ref_tuple(manifest), refs_before)
        self.assertEqual(self.direct_ref_commit(manifest["target_ref"]), target_before)
        self.assertTrue(canonical_tmpdir.is_dir())

    def test_retire_exact_rewritten_quarantine_is_audited_and_idempotent(self) -> None:
        manifest, worker, final_head, discard_head, target_head = (
            self.create_rewritten_quarantine()
        )
        arguments = self.retire_arguments(manifest)
        branch_ref = f"refs/heads/{manifest['branch']}"
        anchor_ref = self.retirement_anchor_ref(manifest["run_id"])
        receipt_ref = self.retirement_receipt_ref(manifest["run_id"])
        control_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        control_tree = self.git(self.control, "write-tree").stdout.strip()
        control_status = self.git(
            self.control,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout

        retirement = self.run_launcher(arguments)

        self.assertEqual(retirement.returncode, 0, retirement.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["retirement_discard_head"], discard_head)
        self.assertEqual(cleaned["retirement_target_contains"], target_head)
        self.assertEqual(cleaned["retirement_initial_target_head"], target_head)
        self.assertEqual(cleaned["retirement_cleanup_target_head"], target_head)
        self.assertIs(cleaned["retirement_anchor_created"], True)
        for field in (
            "retirement_started_at",
            "retirement_worktree_removed_at",
            "retirement_ref_cleanup_started_at",
            "retirement_ref_transaction_committed_at",
            "retirement_receipt_removed_at",
            "retirement_completed_at",
        ):
            self.assertIn(field, cleaned)
        self.assertNotIn("retirement_cleanup_warning", cleaned)
        self.assertEqual(cleaned["final_head"], final_head)
        self.assertEqual(cleaned["observed_head"], discard_head)
        self.assertFalse(cleaned["observed_dirty"])
        self.assertFalse(worker.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        for ref in (branch_ref, anchor_ref, receipt_ref):
            self.assertEqual(
                self.git(
                    self.control,
                    "show-ref",
                    "--verify",
                    "--quiet",
                    ref,
                    check=False,
                ).returncode,
                1,
            )
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            control_head,
        )
        self.assertEqual(self.git(self.control, "write-tree").stdout.strip(), control_tree)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            control_status,
        )

        repeated = self.run_launcher(arguments)
        self.assertEqual(repeated.returncode, 0, repeated.stderr.decode())
        self.assertEqual(self.manifests()[0], cleaned)

        temporary = Path(cleaned["tmpdir"])
        temporary.mkdir()
        cleaned_checkpoint = self.manifest_file(cleaned).read_bytes()
        retained_temporary = self.run_launcher(
            ["--triptych-clean", manifest["run_id"]]
        )
        self.assertEqual(
            retained_temporary.returncode,
            2,
            retained_temporary.stderr.decode(),
        )
        self.assertIn(b"retains a temporary path", retained_temporary.stderr)
        self.assertTrue(temporary.is_dir())
        self.assertEqual(self.manifest_file(cleaned).read_bytes(), cleaned_checkpoint)

        temporary.rmdir()
        cleared_temporary = self.run_launcher(
            ["--triptych-clean", manifest["run_id"]]
        )
        self.assertEqual(
            cleared_temporary.returncode,
            0,
            cleared_temporary.stderr.decode(),
        )
        self.assertEqual(self.manifests()[0], cleaned)

        (self.control / "retirement-target-descendant.txt").write_text(
            "target may advance after retirement\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "retirement-target-descendant.txt")
        self.git(self.control, "commit", "-m", "Advance target after retirement")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        descendant_retry = self.run_launcher(arguments)
        self.assertEqual(
            descendant_retry.returncode,
            0,
            descendant_retry.stderr.decode(),
        )
        changed_target = self.run_launcher(
            self.retire_arguments(manifest, target_contains=descendant)
        )
        self.assertEqual(changed_target.returncode, 2)
        changed_discard = self.run_launcher(
            self.retire_arguments(manifest, discard_head=final_head)
        )
        self.assertEqual(changed_discard.returncode, 2)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), descendant)

        overview = self.run_launcher(["--triptych-status"])
        self.assertEqual(overview.returncode, 0, overview.stderr.decode())
        self.assertEqual(overview.stdout, b"No Triptych Codex runs.\n")
        exact = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertEqual(exact.returncode, 0, exact.stderr.decode())
        self.assertIn(os.fsencode(manifest["run_id"]), exact.stdout)
        self.assertIn(b"cleaned", exact.stdout)

    def test_retire_rejects_nonquarantine_and_nonrewritten_history(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "retirement-ineligible.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        final_head = manifest["final_head"]
        target_head = self.git(
            self.control,
            "rev-parse",
            f"{manifest['target_ref']}^{{commit}}",
        ).stdout.strip()
        arguments = self.retire_arguments(
            manifest,
            discard_head=final_head,
            target_contains=target_head,
        )

        ordinary = self.run_launcher(arguments)
        self.assertEqual(ordinary.returncode, 2)
        self.assertTrue(worker.exists())

        manifest.update(
            {
                "state": "quarantined",
                "observed_head": final_head,
                "observed_dirty": False,
                "quarantine_reason": (
                    "the retained worker history no longer descends from its last "
                    "terminal audit"
                ),
            }
        )
        self.write_test_manifest(manifest)
        continuous = self.run_launcher(arguments)
        self.assertEqual(continuous.returncode, 2)
        self.assertIn(b"still descends", continuous.stderr)
        self.assertTrue(worker.exists())

    def test_retire_requires_exact_resolvable_terminal_and_observed_heads(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        original = json.loads(json.dumps(manifest))
        cases = (
            ("missing-final", {"final_head": "0" * len(final_head)}, None),
            ("missing-observed", {"observed_head": "0" * len(discard_head)}, None),
            ("recorded-dirty", {"observed_dirty": True}, None),
            ("unknown-dirty", {"observed_dirty": None}, None),
            ("wrong-discard", {}, final_head),
        )
        for label, changes, argument_head in cases:
            with self.subTest(case=label):
                candidate = json.loads(json.dumps(original))
                candidate.update(changes)
                self.write_test_manifest(candidate)
                refusal = self.run_launcher(
                    self.retire_arguments(
                        candidate,
                        discard_head=argument_head or candidate["observed_head"],
                    )
                )
                self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
                self.assertTrue(worker.exists())
                self.assertEqual(
                    self.git(
                        self.control,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        self.retirement_anchor_ref(manifest["run_id"]),
                        check=False,
                    ).returncode,
                    1,
                )
        self.write_test_manifest(original)

    def test_retire_enforces_base_and_terminal_ancestry_before_mutation(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        original = json.loads(json.dumps(manifest))
        cases = (
            ("base-not-ancestor", {"base_sha": final_head}),
            ("terminal-is-ancestor", {"final_head": discard_head}),
        )
        for label, changes in cases:
            with self.subTest(case=label):
                candidate = json.loads(json.dumps(original))
                candidate.update(changes)
                self.write_test_manifest(candidate)
                refusal = self.run_launcher(self.retire_arguments(candidate))
                self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
                self.assertTrue(worker.exists())
                self.assertEqual(
                    self.git(
                        self.control,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        self.retirement_anchor_ref(manifest["run_id"]),
                        check=False,
                    ).returncode,
                    1,
                )
        self.write_test_manifest(original)

    def test_retire_refuses_fresh_dirty_or_changed_worker_state(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        arguments = self.retire_arguments(manifest)
        late_change = worker / "late-retirement-change.txt"
        late_change.write_text("unreviewed dirt\n", encoding="utf-8")

        dirty = self.run_launcher(arguments)
        self.assertEqual(dirty.returncode, 2)
        self.assertTrue(worker.exists())
        self.assertIn("?? late-retirement-change.txt", self.git(
            worker,
            "status",
            "--porcelain=v1",
        ).stdout)
        late_change.unlink()

        (worker / "rewritten-after-audit.txt").write_text(
            "new clean commit after the quarantine audit\n",
            encoding="utf-8",
        )
        self.git(worker, "add", "rewritten-after-audit.txt")
        self.git(worker, "commit", "-m", "Change rewritten worker after audit")
        changed_head = self.git(worker, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(changed_head, discard_head)

        changed = self.run_launcher(arguments)
        self.assertEqual(changed.returncode, 2)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), changed_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                self.retirement_anchor_ref(manifest["run_id"]),
                check=False,
            ).returncode,
            1,
        )

    def test_retire_refuses_changed_worker_branch_ref_and_lock_state(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        arguments = self.retire_arguments(manifest)

        self.git(worker, "switch", "-c", "retirement-wrong-branch")
        wrong_branch = self.run_launcher(arguments)
        self.assertEqual(wrong_branch.returncode, 2)
        self.assertTrue(worker.exists())
        self.git(worker, "switch", manifest["branch"])

        self.git(self.control, "worktree", "unlock", str(worker))
        unlocked = self.run_launcher(arguments)
        self.assertEqual(unlocked.returncode, 2)
        self.assertTrue(worker.exists())
        self.git(
            self.control,
            "worktree",
            "lock",
            "--reason",
            f"triptych-codex {manifest['run_id']}",
            str(worker),
        )

        branch_ref = f"refs/heads/{manifest['branch']}"
        self.git(
            self.control,
            "update-ref",
            branch_ref,
            final_head,
            discard_head,
        )
        changed_ref = self.run_launcher(arguments)
        self.assertEqual(changed_ref.returncode, 2)
        self.assertEqual(
            self.git(self.control, "rev-parse", branch_ref).stdout.strip(),
            final_head,
        )
        self.assertTrue(worker.exists())

    def test_retire_refuses_unregistered_or_unauthenticated_worktree(self) -> None:
        manifest, worker, _, _, _ = self.create_rewritten_quarantine()
        arguments = self.retire_arguments(manifest)
        admin = self.retained_admin_directory(worker)
        original_pointer = (worker / ".git").read_bytes()
        (worker / ".git").write_text(
            f"gitdir: {self.control / '.git'}\n",
            encoding="utf-8",
        )

        unauthenticated = self.run_launcher(arguments)
        self.assertEqual(unauthenticated.returncode, 2)
        self.assertTrue(worker.exists())
        (worker / ".git").write_bytes(original_pointer)

        gitdir_backlink = admin / "gitdir"
        original_backlink = gitdir_backlink.read_bytes()
        gitdir_backlink.write_text(
            f"{self.control / '.git/HEAD'}\n",
            encoding="utf-8",
        )
        unregistered = self.run_launcher(arguments)
        self.assertEqual(unregistered.returncode, 2)
        self.assertTrue(worker.exists())
        gitdir_backlink.write_bytes(original_backlink)

        self.git(self.control, "worktree", "unlock", str(worker))
        self.git(self.control, "worktree", "remove", str(worker))
        missing_registration = self.run_launcher(arguments)
        self.assertEqual(missing_registration.returncode, 2)
        self.assertFalse(worker.exists())
        self.assertIn(manifest["branch"], self.worker_branches())
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                self.retirement_anchor_ref(manifest["run_id"]),
                check=False,
            ).returncode,
            1,
        )

    def test_retire_requires_recorded_target_to_contain_exact_selected_commit(self) -> None:
        manifest, worker, final_head, _, target_head = (
            self.create_rewritten_quarantine()
        )
        original = json.loads(json.dumps(manifest))

        not_contained = self.run_launcher(
            self.retire_arguments(manifest, target_contains=final_head)
        )
        self.assertEqual(not_contained.returncode, 2)
        self.assertTrue(worker.exists())

        missing = json.loads(json.dumps(original))
        missing["target_ref"] = "refs/heads/missing-retirement-target"
        self.write_test_manifest(missing)
        missing_target = self.run_launcher(
            self.retire_arguments(
                missing,
                target_contains=target_head,
            )
        )
        self.assertEqual(missing_target.returncode, 2)
        self.assertTrue(worker.exists())

        alias_ref = "refs/heads/retirement-target-alias"
        self.git(self.control, "symbolic-ref", alias_ref, original["target_ref"])
        symbolic = json.loads(json.dumps(original))
        symbolic["target_ref"] = alias_ref
        self.write_test_manifest(symbolic)
        symbolic_target = self.run_launcher(
            self.retire_arguments(
                symbolic,
                target_contains=target_head,
            )
        )
        self.assertEqual(symbolic_target.returncode, 2)
        self.assertTrue(worker.exists())
        self.write_test_manifest(original)

    def test_retire_refuses_active_worker_and_background_lock(self) -> None:
        manifest, worker, _, _, _ = self.create_rewritten_quarantine()
        manifest["background_process_active"] = True
        self.write_test_manifest(manifest)
        lock_path = self.repo_state() / "runs" / f"{manifest['run_id']}.lock"

        with lock_path.open("a+", encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            refusal = self.run_launcher(self.retire_arguments(manifest))
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

        self.assertEqual(refusal.returncode, 2)
        self.assertIn(b"already active", refusal.stderr)
        self.assertTrue(worker.exists())
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "quarantined")
        self.assertTrue(retained["background_process_active"])

        inactive_background = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(inactive_background.returncode, 2)
        self.assertIn(b"background worker", inactive_background.stderr)
        self.assertTrue(worker.exists())
        self.assertTrue(self.manifests()[0]["background_process_active"])

        background = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(background.returncode, 2)
        self.assertIn(b"background worker", background.stderr)
        self.assertTrue(worker.exists())

    def test_retire_refuses_transactions_rebase_and_conflicting_private_refs(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        original = json.loads(json.dumps(manifest))
        transactions = (
            ("integration", {"integration_started_at": "2000-01-01T00:00:00+00:00"}),
            (
                "landing",
                {"integration_landing_expected_head": self.base_head},
            ),
            ("landing-timestamp", {"integrated_at": "2000-01-01T00:00:00+00:00"}),
            (
                "cleanup",
                {"cleanup_expected_head": discard_head},
            ),
            ("integrated", {"integrated_head": final_head}),
        )
        for label, fields in transactions:
            with self.subTest(transaction=label):
                candidate = json.loads(json.dumps(original))
                candidate.update(fields)
                self.write_test_manifest(candidate)
                refusal = self.run_launcher(self.retire_arguments(candidate))
                self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
                self.assertTrue(worker.exists())
                self.assertEqual(
                    self.git(
                        self.control,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        self.retirement_anchor_ref(manifest["run_id"]),
                        check=False,
                    ).returncode,
                    1,
                )
        self.write_test_manifest(original)

        rebase_marker = Path(
            self.git(worker, "rev-parse", "--git-path", "rebase-merge").stdout.strip()
        )
        if not rebase_marker.is_absolute():
            rebase_marker = worker / rebase_marker
        rebase_marker.mkdir()
        active_rebase = self.run_launcher(self.retire_arguments(original))
        self.assertEqual(active_rebase.returncode, 2)
        self.assertTrue(rebase_marker.exists())
        rebase_marker.rmdir()

        integration_anchor = self.source_anchor_ref(manifest["run_id"])
        self.git(self.control, "update-ref", integration_anchor, final_head)
        conflicting_integration_ref = self.run_launcher(self.retire_arguments(original))
        self.assertEqual(conflicting_integration_ref.returncode, 2)
        self.assertEqual(
            self.git(self.control, "rev-parse", integration_anchor).stdout.strip(),
            final_head,
        )
        self.git(self.control, "update-ref", "-d", integration_anchor, final_head)

        retirement_receipt = self.retirement_receipt_ref(manifest["run_id"])
        self.git(self.control, "update-ref", retirement_receipt, discard_head)
        uncheckpointed_retirement_receipt = self.run_launcher(
            self.retire_arguments(original)
        )
        self.assertEqual(uncheckpointed_retirement_receipt.returncode, 2)
        self.assertEqual(
            self.git(self.control, "rev-parse", retirement_receipt).stdout.strip(),
            discard_head,
        )
        self.git(
            self.control,
            "update-ref",
            "-d",
            retirement_receipt,
            discard_head,
        )

        retirement_anchor = self.retirement_anchor_ref(manifest["run_id"])
        self.git(self.control, "update-ref", retirement_anchor, discard_head)
        uncheckpointed_retirement_ref = self.run_launcher(
            self.retire_arguments(original)
        )
        self.assertEqual(uncheckpointed_retirement_ref.returncode, 2)
        self.assertEqual(
            self.git(self.control, "rev-parse", retirement_anchor).stdout.strip(),
            discard_head,
        )

    def test_retire_anchor_creation_crash_is_retryable_with_exact_arguments(self) -> None:
        manifest, worker, _, discard_head, target_head = (
            self.create_rewritten_quarantine()
        )
        arguments = self.retire_arguments(manifest)
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        marker = self.root / "post-retirement-anchor-create-kill"

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", anchor, discard_head],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        self.assertEqual(pending["retirement_discard_head"], discard_head)
        self.assertEqual(pending["retirement_target_contains"], target_head)
        self.assertEqual(pending["retirement_initial_target_head"], target_head)
        self.assertNotIn("retirement_anchor_created", pending)
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), discard_head)
        self.assertTrue(worker.exists())

        changed = self.run_launcher(
            self.retire_arguments(pending, target_contains=pending["final_head"])
        )
        self.assertEqual(changed.returncode, 2)
        self.assertTrue(worker.exists())
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), discard_head)

        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertFalse(worker.exists())

    def test_retire_retry_with_worktree_requires_restored_target_containment(
        self,
    ) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        (self.control / "worktree-retirement-checkpoint.txt").write_text(
            "operator-selected checkpoint before worktree retirement\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "worktree-retirement-checkpoint.txt")
        self.git(self.control, "commit", "-m", "Select worktree retirement checkpoint")
        selected = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        arguments = self.retire_arguments(manifest, target_contains=selected)
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        marker = self.root / "post-worktree-retirement-anchor-create-kill"

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", anchor, discard_head],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.assertTrue(worker.exists())
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        self.git(self.control, "reset", "--hard", self.base_head)
        lost = self.run_launcher(arguments)
        self.assertEqual(lost.returncode, 2, lost.stderr.decode())
        self.assertIn(b"no longer contains", lost.stderr)
        self.assertTrue(worker.exists())
        self.assertIn("locked triptych-codex", self.worktree_output())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        self.assertNotIn("retirement_worktree_removed_at", pending)
        self.assertNotIn("retirement_cleanup_target_head", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        self.git(self.control, "reset", "--hard", selected)
        (self.control / "restored-worktree-retirement-descendant.txt").write_text(
            "restored containing descendant\n",
            encoding="utf-8",
        )
        self.git(
            self.control,
            "add",
            "restored-worktree-retirement-descendant.txt",
        )
        self.git(
            self.control,
            "commit",
            "-m",
            "Restore worktree retirement containment",
        )
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["retirement_initial_target_head"], selected)
        self.assertEqual(cleaned["retirement_cleanup_target_head"], descendant)
        self.assertFalse(worker.exists())

    def test_clean_refuses_untouched_quarantine_but_resumes_retirement_checkpoint(
        self,
    ) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        untouched = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(untouched.returncode, 2)
        self.assertIn(b"quarantined run", untouched.stderr)
        self.assertIn(b"no retirement checkpoint", untouched.stderr)
        self.assertNotIn(b"rewritten quarantine", untouched.stderr)
        self.assertEqual(self.manifests()[0]["state"], "quarantined")

        anchor = self.retirement_anchor_ref(manifest["run_id"])
        marker = self.root / "clean-resumes-retirement-anchor-checkpoint"
        crashed = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", anchor, discard_head],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.assertTrue(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        checkpoint = self.manifest_file(pending).read_bytes()
        expected_direction = os.fsencode(
            f"scripts/triptych-codex --triptych-clean {manifest['run_id']}"
        )

        for option in ("--triptych-reopen", "--triptych-integrate"):
            with self.subTest(option=option):
                refused = self.run_launcher([option, manifest["run_id"]])
                self.assertEqual(refused.returncode, 2, refused.stderr.decode())
                self.assertIn(b"checkpointed retirement", refused.stderr)
                self.assertIn(expected_direction, refused.stderr)
                self.assertEqual(self.manifest_file(pending).read_bytes(), checkpoint)
                self.assertTrue(worker.exists())
                self.assertEqual(
                    self.retirement_ref_tuple(manifest),
                    (discard_head, discard_head, None),
                )

        resumed = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(resumed.returncode, 0, resumed.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertFalse(worker.exists())

    def test_retire_unlock_crash_relocks_and_retries_exact_worker(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        marker = self.root / "post-retirement-unlock-kill"

        crashed = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "unlock", str(worker)],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertTrue(worker.exists())
        self.assertNotIn("locked\n", self.worktree_output())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        self.assertIs(pending["retirement_anchor_created"], True)
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), discard_head)

        retry = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertFalse(worker.exists())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_retire_revalidates_after_unlock_and_relocks_changed_worker(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        marker = self.root / "dirty-after-retirement-unlock"
        late_change = worker / "post-retirement-unlock-dirt.txt"

        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "unlock", str(worker)],
                marker=marker,
                action="dirty",
                dirty_path=late_change,
            ),
        )

        self.assertEqual(refusal.returncode, 2)
        self.assertTrue(marker.exists())
        self.assertTrue(worker.exists())
        self.assertIn("locked triptych-codex", self.worktree_output())
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), discard_head)
        self.assertEqual(self.manifests()[0]["state"], "retirement-pending")
        self.assertIn(
            "?? post-retirement-unlock-dirt.txt",
            self.git(worker, "status", "--porcelain=v1").stdout,
        )

        late_change.unlink()
        retry = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_retire_ref_cleanup_rejects_partial_ref_deletion(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        branch_ref = f"refs/heads/{manifest['branch']}"
        marker = self.root / "retain-retirement-refs-for-partial-test"
        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )
        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertFalse(worker.exists())
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        self.git(self.control, "update-ref", "-d", anchor, discard_head)
        missing_anchor = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(missing_anchor.returncode, 2)
        self.assertIn(b"partial", missing_anchor.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", branch_ref).stdout.strip(),
            discard_head,
        )

        self.git(self.control, "update-ref", anchor, discard_head)
        self.git(self.control, "update-ref", "-d", branch_ref, discard_head)
        missing_branch = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(missing_branch.returncode, 2)
        self.assertIn(b"partial", missing_branch.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            discard_head,
        )
        self.assertEqual(
            self.manifests()[0]["state"],
            "retirement-ref-cleanup-pending",
        )

        self.git(self.control, "update-ref", "-d", anchor, discard_head)
        both_deletion_refs_missing = self.run_launcher(
            self.retire_arguments(manifest)
        )
        self.assertEqual(
            both_deletion_refs_missing.returncode,
            2,
            both_deletion_refs_missing.stderr.decode(),
        )
        self.assertIn(b"partial", both_deletion_refs_missing.stderr)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertNotIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)

    def test_retire_ref_cleanup_rejects_anchor_and_branch_tampering(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        anchor = self.retirement_anchor_ref(manifest["run_id"])
        branch_ref = f"refs/heads/{manifest['branch']}"
        marker = self.root / "retain-retirement-refs-for-tamper-test"
        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )
        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertFalse(worker.exists())

        self.git(self.control, "update-ref", anchor, final_head, discard_head)
        changed_anchor = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(changed_anchor.returncode, 2)
        self.assertIn(b"ref changed", changed_anchor.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", branch_ref).stdout.strip(),
            discard_head,
        )
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            final_head,
        )

        self.git(self.control, "update-ref", anchor, discard_head, final_head)
        self.git(self.control, "update-ref", branch_ref, final_head, discard_head)
        changed_branch = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(changed_branch.returncode, 2)
        self.assertIn(b"ref changed", changed_branch.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", branch_ref).stdout.strip(),
            final_head,
        )
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            discard_head,
        )

    def test_retire_target_ref_race_accepts_containing_descendant_on_retry(self) -> None:
        manifest, worker, _, discard_head, target_head = (
            self.create_rewritten_quarantine()
        )
        (self.control / "retirement-race-descendant.txt").write_text(
            "descendant target raced into place\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "retirement-race-descendant.txt")
        self.git(self.control, "commit", "-m", "Prepare retirement target race")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.git(self.control, "reset", "--hard", target_head)
        arguments = self.retire_arguments(manifest)
        marker = self.root / "retirement-target-ref-race"

        raced = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="move-ref",
                move_ref=(manifest["target_ref"], descendant, target_head),
            ),
        )

        self.assertEqual(raced.returncode, 1, raced.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        self.assertEqual(
            self.git(self.control, "rev-parse", manifest["target_ref"]).stdout.strip(),
            descendant,
        )
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertEqual(pending["retirement_initial_target_head"], target_head)
        self.assertEqual(pending["retirement_cleanup_target_head"], target_head)

        self.git(self.control, "reset", "--hard", descendant)
        descendant_marker = self.root / "retain-descendant-retirement-checkpoint"
        checkpointed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=descendant_marker,
                action="refuse",
            ),
        )
        self.assertEqual(checkpointed.returncode, 1, checkpointed.stderr.decode())
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )
        pending = self.manifests()[0]
        self.assertEqual(pending["retirement_initial_target_head"], target_head)
        self.assertEqual(pending["retirement_cleanup_target_head"], descendant)
        status = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertEqual(status.returncode, 0, status.stderr.decode())

        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["retirement_initial_target_head"], target_head)
        self.assertEqual(cleaned["retirement_cleanup_target_head"], descendant)
        self.assertEqual(
            self.git(self.control, "rev-parse", manifest["target_ref"]).stdout.strip(),
            descendant,
        )
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

    def test_retire_retry_fails_closed_until_target_containment_is_restored(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        (self.control / "selected-retirement-checkpoint.txt").write_text(
            "operator-selected target checkpoint\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "selected-retirement-checkpoint.txt")
        self.git(self.control, "commit", "-m", "Create selected retirement checkpoint")
        selected = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        arguments = self.retire_arguments(manifest, target_contains=selected)
        marker = self.root / "retain-retirement-refs-before-target-rewind"
        refusal = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )
        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertFalse(worker.exists())

        self.git(self.control, "reset", "--hard", self.base_head)
        lost = self.run_launcher(arguments)
        self.assertNotEqual(lost.returncode, 0)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        self.git(self.control, "reset", "--hard", selected)
        (self.control / "selected-retirement-descendant.txt").write_text(
            "descendant still contains the selected checkpoint\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "selected-retirement-descendant.txt")
        self.git(self.control, "commit", "-m", "Advance selected retirement checkpoint")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        descendant_retry = self.run_launcher(arguments)
        self.assertEqual(
            descendant_retry.returncode,
            0,
            descendant_retry.stderr.decode(),
        )
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["retirement_target_contains"], selected)
        self.assertEqual(cleaned["retirement_initial_target_head"], selected)
        self.assertEqual(cleaned["retirement_cleanup_target_head"], descendant)

    def test_retirement_object_fields_and_observed_head_are_manifest_validated(
        self,
    ) -> None:
        manifest, _, _, _, _ = self.create_rewritten_quarantine()
        retirement = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(retirement.returncode, 0, retirement.stderr.decode())
        cleaned = self.manifests()[0]
        original = json.loads(json.dumps(cleaned))
        fields = (
            "observed_head",
            "retirement_discard_head",
            "retirement_target_contains",
            "retirement_initial_target_head",
            "retirement_cleanup_target_head",
        )

        for field in fields:
            with self.subTest(field=field):
                tampered = json.loads(json.dumps(original))
                tampered.setdefault(field, self.base_head)
                tampered[field] = tampered[field][:12]
                self.write_test_manifest(tampered)
                status = self.run_launcher(
                    ["--triptych-status", manifest["run_id"]]
                )
                self.assertEqual(status.returncode, 2)
                self.assertIn(
                    f"invalid {field.replace('_', ' ')}".encode(),
                    status.stderr,
                )
        self.write_test_manifest(original)

    def test_retirement_pending_manifest_validates_receipt_marker_order(
        self,
    ) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        marker = self.root / "retain-retirement-checkpoint-for-validation"
        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )
        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        valid_status = self.run_launcher(
            ["--triptych-status", manifest["run_id"]]
        )
        self.assertEqual(valid_status.returncode, 0, valid_status.stderr.decode())

        transaction_marked = json.loads(json.dumps(pending))
        transaction_marked["retirement_ref_transaction_committed_at"] = (
            "2000-01-01T00:00:00+00:00"
        )
        self.write_test_manifest(transaction_marked)
        transaction_status = self.run_launcher(
            ["--triptych-status", manifest["run_id"]]
        )
        self.assertEqual(
            transaction_status.returncode,
            0,
            transaction_status.stderr.decode(),
        )

        receipt_removed = json.loads(json.dumps(transaction_marked))
        receipt_removed["retirement_receipt_removed_at"] = (
            "2000-01-01T00:00:01+00:00"
        )
        self.write_test_manifest(receipt_removed)
        receipt_status = self.run_launcher(
            ["--triptych-status", manifest["run_id"]]
        )
        self.assertEqual(receipt_status.returncode, 0, receipt_status.stderr.decode())

        invalid_cases = []
        receipt_without_transaction = json.loads(json.dumps(pending))
        receipt_without_transaction["retirement_receipt_removed_at"] = (
            "2000-01-01T00:00:01+00:00"
        )
        invalid_cases.append(("receipt-without-transaction", receipt_without_transaction))

        for field in (
            "retirement_cleanup_target_head",
            "retirement_ref_cleanup_started_at",
            "retirement_worktree_removed_at",
            "retirement_anchor_created",
        ):
            missing = json.loads(json.dumps(transaction_marked))
            missing.pop(field)
            invalid_cases.append((f"transaction-missing-{field}", missing))

        invalid_timestamp = json.loads(json.dumps(transaction_marked))
        invalid_timestamp["retirement_ref_transaction_committed_at"] = ""
        invalid_cases.append(("empty-transaction-timestamp", invalid_timestamp))
        invalid_receipt_timestamp = json.loads(json.dumps(receipt_removed))
        invalid_receipt_timestamp["retirement_receipt_removed_at"] = False
        invalid_cases.append(("invalid-receipt-timestamp", invalid_receipt_timestamp))

        for label, candidate in invalid_cases:
            with self.subTest(case=label):
                self.write_test_manifest(candidate)
                status = self.run_launcher(
                    ["--triptych-status", manifest["run_id"]]
                )
                self.assertEqual(status.returncode, 2, status.stderr.decode())

        self.write_test_manifest(pending)

    def test_cleaned_retirement_manifest_requires_complete_receipt_audit(
        self,
    ) -> None:
        manifest, _, _, _, _ = self.create_rewritten_quarantine()
        retirement = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(retirement.returncode, 0, retirement.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        valid_status = self.run_launcher(
            ["--triptych-status", manifest["run_id"]]
        )
        self.assertEqual(valid_status.returncode, 0, valid_status.stderr.decode())

        required = (
            "retirement_discard_head",
            "retirement_target_contains",
            "retirement_initial_target_head",
            "retirement_cleanup_target_head",
            "retirement_started_at",
            "retirement_anchor_created",
            "retirement_worktree_removed_at",
            "retirement_ref_cleanup_started_at",
            "retirement_ref_transaction_committed_at",
            "retirement_receipt_removed_at",
            "retirement_completed_at",
        )
        for field in required:
            with self.subTest(missing=field):
                missing = json.loads(json.dumps(cleaned))
                missing.pop(field)
                self.write_test_manifest(missing)
                status = self.run_launcher(
                    ["--triptych-status", manifest["run_id"]]
                )
                self.assertEqual(status.returncode, 2, status.stderr.decode())

        for field in (
            "retirement_ref_transaction_committed_at",
            "retirement_receipt_removed_at",
        ):
            with self.subTest(invalid_timestamp=field):
                invalid = json.loads(json.dumps(cleaned))
                invalid[field] = ""
                self.write_test_manifest(invalid)
                status = self.run_launcher(
                    ["--triptych-status", manifest["run_id"]]
                )
                self.assertEqual(status.returncode, 2, status.stderr.decode())

        self.write_test_manifest(cleaned)

    def test_retire_worktree_removal_crash_is_adopted(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        marker = self.root / "post-retirement-worktree-removal-kill"

        crashed = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "remove", str(worker)],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        self.assertNotIn("retirement_worktree_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        retry = self.run_launcher(self.retire_arguments(manifest))
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_worktree_removed_at", cleaned)

    def test_retire_worktree_removal_dangling_symlink_race_fails_closed(
        self,
    ) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        arguments = self.retire_arguments(manifest)
        marker = self.root / "post-retirement-worktree-removal-symlink"
        nonexistent_target = self.root / "nonexistent-retirement-worktree-target"

        raced = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "remove", str(worker)],
                marker=marker,
                action="dangling-symlink",
                dangling_link=(worker, nonexistent_target),
            ),
        )

        self.assertEqual(raced.returncode, 2, raced.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertTrue(worker.is_symlink())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-pending")
        self.assertNotIn("retirement_worktree_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        unsafe_retry = self.run_launcher(arguments)
        self.assertEqual(unsafe_retry.returncode, 2, unsafe_retry.stderr.decode())
        self.assertEqual(self.manifests()[0], pending)
        self.assertTrue(worker.is_symlink())

        worker.unlink()
        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

    def test_retire_ref_transaction_refusal_is_clean_run_retryable(self) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        marker = self.root / "refuse-retirement-ref-transaction"

        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )

        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertEqual(pending["retirement_cleanup_target_head"], self.base_head)
        self.assertIn("retirement_ref_cleanup_started_at", pending)
        self.assertIn("retirement_cleanup_warning", pending)
        self.assertNotIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (discard_head, discard_head, None),
        )

        resumed = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(resumed.returncode, 0, resumed.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_ref_transaction_committed_at", cleaned)
        self.assertIn("retirement_receipt_removed_at", cleaned)
        self.assertIn("retirement_completed_at", cleaned)
        self.assertNotIn("retirement_cleanup_warning", cleaned)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

    def test_retire_receipt_deletion_refusal_keeps_exact_receipt_and_retries(
        self,
    ) -> None:
        manifest, worker, _, discard_head, _ = self.create_rewritten_quarantine()
        marker = self.root / "refuse-retirement-receipt-deletion"
        receipt = self.retirement_receipt_ref(manifest["run_id"])

        refusal = self.run_launcher(
            self.retire_arguments(manifest),
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "-d", receipt, discard_head],
                marker=marker,
                action="refuse",
            ),
        )

        self.assertEqual(refusal.returncode, 1, refusal.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertNotIn("retirement_completed_at", pending)
        self.assertIn("retirement_cleanup_warning", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, discard_head),
        )

        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_receipt_removed_at", cleaned)
        self.assertIn("retirement_completed_at", cleaned)
        self.assertNotIn("retirement_cleanup_warning", cleaned)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

    def test_retire_post_ref_transaction_crash_uses_receipt_after_gc(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        (self.control / "one-use-retirement-target.txt").write_text(
            "operator-selected checkpoint may later be pruned\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "one-use-retirement-target.txt")
        self.git(self.control, "commit", "-m", "Create one-use retirement target")
        selected_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        arguments = self.retire_arguments(
            manifest,
            target_contains=selected_target,
        )
        marker = self.root / "post-retirement-ref-transaction-kill"

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "--stdin"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertNotIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, discard_head),
        )

        self.git(self.control, "reset", "--hard", self.base_head)
        self.expire_reflogs_and_prune()
        self.assertFalse(self.commit_exists(final_head))
        self.assertFalse(self.commit_exists(selected_target))
        self.assertTrue(self.commit_exists(discard_head))

        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_ref_transaction_committed_at", cleaned)
        self.assertIn("retirement_receipt_removed_at", cleaned)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

        self.expire_reflogs_and_prune()
        self.assertFalse(self.commit_exists(discard_head))
        repeated = self.run_launcher(arguments)
        self.assertEqual(repeated.returncode, 0, repeated.stderr.decode())
        self.assertEqual(self.manifests()[0], cleaned)

    def test_retire_post_transaction_receipt_tampering_prevents_marker(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        arguments = self.retire_arguments(manifest)
        marker = self.root / "post-retirement-ref-transaction-tamper"
        receipt = self.retirement_receipt_ref(manifest["run_id"])

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "--stdin"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.assertFalse(worker.exists())
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, discard_head),
        )

        self.git(self.control, "update-ref", receipt, final_head, discard_head)
        tampered = self.run_launcher(arguments)
        self.assertEqual(tampered.returncode, 2, tampered.stderr.decode())
        self.assertIn(b"receipt", tampered.stderr)
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertNotIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, final_head),
        )

    def test_retire_crash_after_transaction_marker_keeps_exact_receipt(self) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        arguments = self.retire_arguments(manifest)
        marker = self.root / "before-retirement-receipt-delete-kill"
        receipt = self.retirement_receipt_ref(manifest["run_id"])

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "-d", receipt, discard_head],
                marker=marker,
                action="kill-parent-before",
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, discard_head),
        )

        self.git(self.control, "update-ref", receipt, final_head, discard_head)
        tampered = self.run_launcher(arguments)
        self.assertEqual(tampered.returncode, 2, tampered.stderr.decode())
        self.assertIn(b"receipt", tampered.stderr)
        self.assertEqual(
            self.retirement_ref_tuple(manifest),
            (None, None, final_head),
        )
        self.git(self.control, "update-ref", receipt, discard_head, final_head)

        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_receipt_removed_at", cleaned)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

    def test_retire_crash_after_receipt_deletion_recovers_with_pruned_objects(
        self,
    ) -> None:
        manifest, worker, final_head, discard_head, _ = (
            self.create_rewritten_quarantine()
        )
        (self.control / "prunable-retirement-target.txt").write_text(
            "temporary selected target\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "prunable-retirement-target.txt")
        self.git(self.control, "commit", "-m", "Create prunable retirement target")
        selected_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        arguments = self.retire_arguments(
            manifest,
            target_contains=selected_target,
        )
        receipt = self.retirement_receipt_ref(manifest["run_id"])
        marker = self.root / "after-retirement-receipt-delete-kill"

        crashed = self.run_launcher(
            arguments,
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "-d", receipt, discard_head],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertFalse(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "retirement-ref-cleanup-pending")
        self.assertIn("retirement_ref_transaction_committed_at", pending)
        self.assertNotIn("retirement_receipt_removed_at", pending)
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

        temporary = Path(manifest["tmpdir"])
        shutil.rmtree(temporary)
        temporary.write_text("obstruct retirement finalization\n", encoding="utf-8")
        self.git(self.control, "reset", "--hard", self.base_head)
        self.expire_reflogs_and_prune()
        for commit in (final_head, discard_head, selected_target):
            self.assertFalse(self.commit_exists(commit), commit)

        obstructed = self.run_launcher(arguments)
        self.assertEqual(obstructed.returncode, 2, obstructed.stderr.decode())
        self.assertIn(b"not an exact real directory", obstructed.stderr)
        still_pending = self.manifests()[0]
        self.assertEqual(
            still_pending["state"],
            "retirement-ref-cleanup-pending",
        )
        self.assertIn("retirement_ref_transaction_committed_at", still_pending)
        self.assertIn("retirement_receipt_removed_at", still_pending)
        self.assertNotIn("retirement_completed_at", still_pending)
        self.assertNotIn("cleaned_at", still_pending)
        self.assertIn("retirement_cleanup_warning", still_pending)
        self.assertTrue(temporary.is_file())
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))
        for commit in (final_head, discard_head, selected_target):
            self.assertFalse(self.commit_exists(commit), commit)

        temporary.unlink()
        retry = self.run_launcher(arguments)
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertIn("retirement_receipt_removed_at", cleaned)
        self.assertIn("retirement_completed_at", cleaned)
        self.assertNotIn("retirement_cleanup_warning", cleaned)
        self.assertFalse(os.path.lexists(temporary))
        self.assertEqual(self.retirement_ref_tuple(manifest), (None, None, None))

        repeated = self.run_launcher(arguments)
        self.assertEqual(repeated.returncode, 0, repeated.stderr.decode())
        self.assertEqual(self.manifests()[0], cleaned)

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
        deadline = time.monotonic() + LOCK_CHECKPOINT_TIMEOUT_SECONDS
        while not ready.exists():
            if process.poll() is not None:
                self.fail(f"launcher exited before worker became ready: {process.returncode}")
            if time.monotonic() >= deadline:
                process.kill()
                process.wait(timeout=5)
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
        deadline = time.monotonic() + LOCK_CHECKPOINT_TIMEOUT_SECONDS
        while True:
            status = self.run_launcher(["--triptych-status", manifest["run_id"]])
            if b"interrupted" in status.stdout and b"no" in status.stdout:
                break
            if time.monotonic() >= deadline:
                self.fail(f"orphaned worker did not settle: {status.stdout!r}")
            time.sleep(0.05)
        self.assertTrue(Path(manifest["worktree"]).exists())

    def test_landing_git_child_inherits_repository_and_run_locks(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "git-child-lock-worker.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        marker = self.root / "git-child-lock.ready"
        release = self.root / "git-child-lock.release"
        self.addCleanup(lambda: release.touch(exist_ok=True))
        environment = self.base_environment()
        environment.update(
            self.slow_landing_git_environment(marker=marker, release=release)
        )
        process = subprocess.Popen(
            [str(self.launcher), "--triptych-integrate", manifest["run_id"]],
            cwd=self.control,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + LOCK_CHECKPOINT_TIMEOUT_SECONDS
        while not marker.exists():
            if time.monotonic() >= deadline:
                process.kill()
                process.wait(timeout=5)
                self.fail("landing Git child did not reach its lock checkpoint")
            time.sleep(0.02)
        process.wait(timeout=5)
        self.assertLess(process.returncode, 0)

        state = self.repo_state()
        for lock_path in (
            state / "repository.lock",
            state / "runs" / f"{manifest['run_id']}.lock",
        ):
            with lock_path.open("a+", encoding="utf-8") as stream:
                with self.assertRaises(BlockingIOError, msg=str(lock_path)):
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

        release.touch()
        deadline = time.monotonic() + LOCK_CHECKPOINT_TIMEOUT_SECONDS
        while True:
            available = True
            for lock_path in (
                state / "repository.lock",
                state / "runs" / f"{manifest['run_id']}.lock",
            ):
                with lock_path.open("a+", encoding="utf-8") as stream:
                    try:
                        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except BlockingIOError:
                        available = False
                    else:
                        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            if available:
                break
            if time.monotonic() >= deadline:
                self.fail("landing Git child did not release inherited locks")
            time.sleep(0.02)

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

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
        nested = temporary / "downloads/source"
        nested.mkdir(parents=True)
        (nested / "artifact.bin").write_bytes(b"run-owned artifact")
        outside = self.root / "outside-temp-target"
        outside.mkdir()
        (outside / "preserved.txt").write_text("outside\n", encoding="utf-8")
        (temporary / "outside-link").symlink_to(outside, target_is_directory=True)

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
        self.assertEqual(
            (outside / "preserved.txt").read_text(encoding="utf-8"),
            "outside\n",
        )
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

    def test_integrate_retains_refs_when_tmpdir_is_not_a_real_directory(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "obstructed-tmp.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        temporary = Path(manifest["tmpdir"])
        shutil.rmtree(temporary)
        temporary.write_text("operator-owned obstruction\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(integrate.returncode, 1, integrate.stderr.decode())
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "cleaned-branch-retained")
        self.assertIn("not an exact real directory", retained["cleanup_warning"])
        self.assertTrue(temporary.is_file())
        self.assertEqual(
            temporary.read_text(encoding="utf-8"),
            "operator-owned obstruction\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertIn(manifest["branch"], self.worker_branches())
        self.assertIsNone(self.direct_ref_commit(self.source_anchor_ref(manifest["run_id"])))

        temporary.unlink()
        (temporary / "retry-artifacts").mkdir(parents=True)
        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertFalse(temporary.exists())
        self.assertEqual(self.worker_branches(), [])
        self.assertIsNone(self.direct_ref_commit(self.source_anchor_ref(manifest["run_id"])))
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_cleaned_integration_refuses_a_recreated_tmpdir(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "recreated-tmp.jsonl"),
                "FAKE_CODEX_ACTION": "commit",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        cleaned = self.manifests()[0]
        temporary = Path(cleaned["tmpdir"])
        temporary.mkdir()
        (temporary / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
        checkpoint = self.manifest_file(cleaned).read_bytes()

        for arguments in (
            ["--triptych-integrate", cleaned["run_id"]],
            ["--triptych-clean", cleaned["run_id"]],
        ):
            with self.subTest(arguments=arguments):
                refusal = self.run_launcher(arguments)
                self.assertEqual(refusal.returncode, 2, refusal.stderr.decode())
                self.assertIn(b"retains a temporary path", refusal.stderr)
                self.assertTrue(temporary.is_dir())
                self.assertEqual(self.manifest_file(cleaned).read_bytes(), checkpoint)

        shutil.rmtree(temporary)
        confirmation = self.run_launcher(["--triptych-clean", cleaned["run_id"]])
        self.assertEqual(confirmation.returncode, 0, confirmation.stderr.decode())

    def test_make_integrate_forwards_one_run_id_without_masking_unknown_targets(self) -> None:
        log = self.root / "make-integrate.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "commit"}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]

        missing = self.run_make(["integrate"])
        self.assertEqual(missing.returncode, 2)
        self.assertIn(b"Usage: make integrate RUN=<run-id>", missing.stderr)
        self.assert_control_unchanged()
        self.assertTrue(Path(manifest["worktree"]).exists())

        unknown = self.run_make(["definitely-unknown"])
        self.assertEqual(unknown.returncode, 2)
        self.assertIn(b"No rule to make target", unknown.stderr)
        for pattern_target in ("%", "integ%"):
            patterned = self.run_make([pattern_target])
            self.assertEqual(patterned.returncode, 2)
            self.assertIn(b"No rule to make target", patterned.stderr)

        integrate = self.run_make(["integrate", f"RUN={manifest['run_id']}"])
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
        self.assertNotIn("integration_rollback_started_at", rolled_back)
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

    def test_post_cas_ignored_collision_is_preserved_and_retryable(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "post-cas-ignored-worker.jsonl"),
                "FAKE_CODEX_ACTION": "commit-ignored",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        (self.control / "build").mkdir(exist_ok=True)
        collision = self.control / "build/collision.txt"
        marker = self.root / "post-cas-ignored-collision"

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
                action="dirty",
                dirty_path=collision,
            ),
        )

        self.assertEqual(landing.returncode, 2)
        self.assertTrue(marker.exists())
        self.assertEqual(collision.read_text(encoding="utf-8"), "post-Git dirt\n")
        candidate = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(candidate, manifest["final_head"])
        self.assertTrue(worker.exists())
        failed = self.manifests()[0]
        self.assertEqual(failed["state"], "integration-verification-failed")
        self.assertEqual(failed["integrated_head"], candidate)

        collision.unlink()
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(
            (self.control / "build/collision.txt").read_text(encoding="utf-8"),
            "tracked worker result\n",
        )
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertFalse(worker.exists())

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
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                self.source_anchor_ref(manifest["run_id"]),
                check=False,
            ).returncode,
            1,
        )

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
        self.assertNotIn("integration_rollback_started_at", retained)
        self.assertNotIn("integrated_head", retained)

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), raced_target)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["integrated_head"], landed_head)

    def test_integrate_retains_conflict_with_opaque_managed_diagnostics(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )

        self.assertEqual(integrate.returncode, 2)
        diagnostics = integrate.stderr.decode()
        self.assertIn("conflict", diagnostics.lower())
        self.assertIn(f"--triptych-resolve {manifest['run_id']}", diagnostics)
        self.assertIn(f"--triptych-continue {manifest['run_id']}", diagnostics)
        self.assertIn(f"--triptych-abort {manifest['run_id']}", diagnostics)
        self.assertNotIn("git rebase --continue", diagnostics)
        self.assertNotIn("git rebase --abort", diagnostics)
        self.assertNotIn(manifest["worktree"], diagnostics)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "conflicting primary result\n",
        )
        self.assertTrue(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(worker, "diff", "--name-only", "--diff-filter=U").stdout.splitlines(),
            ["agent-result.txt"],
        )

        conflicted = self.manifests()[0]
        self.assertEqual(conflicted["state"], "integration-conflict")
        self.assertEqual(conflicted["final_head"], source_head)
        self.assertEqual(conflicted["integration_source_head"], source_head)
        self.assertEqual(conflicted["integration_target_head"], target_head)
        self.assertEqual(conflicted["integration_conflict_paths"], ["agent-result.txt"])
        self.assertNotIn("integration_candidate_head", conflicted)
        self.assertNotIn("integrated_head", conflicted)

        status = self.run_launcher(["--triptych-status", manifest["run_id"]])
        self.assertEqual(status.returncode, 0, status.stderr.decode())
        rendered = status.stdout.decode()
        self.assertIn(manifest["run_id"], rendered)
        self.assertIn("integration-conflict", rendered)
        self.assertNotIn(manifest["worktree"], rendered)
        self.assertNotIn(manifest["tmpdir"], rendered)
        self.assertNotIn(self.source_anchor_ref(manifest["run_id"]), rendered)

    def test_rename_destination_conflict_can_be_resolved_and_continued(self) -> None:
        source_name = "rename-source.txt"
        destination_name = "rename-destination.txt"
        source = self.control / source_name
        source.write_text(
            "shared line 1\nshared line 2\nshared line 3\nshared line 4\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", source_name)
        self.git(self.control, "commit", "-m", "Add rename-conflict source")

        worker_log = self.root / "rename-conflict-worker.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(worker_log),
                "FAKE_CODEX_ACTION": "commit-edit-path",
                "FAKE_CODEX_MODIFIED_PATH": source_name,
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])

        self.git(self.control, "mv", source_name, destination_name)
        destination = self.control / destination_name
        destination.write_text(
            "target changed line 1\nshared line 2\nshared line 3\nshared line 4\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", destination_name)
        self.git(self.control, "commit", "-m", "Rename and edit source")
        target_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(integrate.returncode, 2, integrate.stderr.decode())
        conflicted = self.manifests()[0]
        self.assertEqual(conflicted["state"], "integration-conflict")
        self.assertEqual(conflicted["integration_unmerged_paths"], [destination_name])
        self.assertIn(destination_name, conflicted["integration_allowed_staged_paths"])

        resolution, _ = self.resolve_integration_conflict(
            manifest,
            log_name="rename-conflict-resolver.jsonl",
            content="resolved renamed result\n",
            conflict_path=destination_name,
        )
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        review = self.manifests()[0]
        self.assertEqual(review["state"], "integration-review-pending")
        candidate = review["integration_candidate_head"]
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertFalse((worker / source_name).exists())
        self.assertEqual(
            (worker / destination_name).read_text(encoding="utf-8"),
            "resolved renamed result\n",
        )

    def test_post_git_initial_rebase_crash_adopts_managed_conflict(self) -> None:
        manifest, worker, source_head, target_head = self.prepare_integration_conflict()
        marker = self.root / "post-initial-rebase-kill"
        environment = self.post_git_action_environment(
            cwd=worker,
            tokens=["rebase", "--onto"],
            marker=marker,
        )

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=environment,
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-rebase-pending")
        self.assertTrue(self.active_rebase_paths(worker))
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            source_head,
        )
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 2)
        self.assertIn(b"adopted as a managed conflict", retry.stderr)
        self.assertNotIn(os.fsencode(manifest["worktree"]), retry.stderr)
        adopted = self.manifests()[0]
        self.assertEqual(adopted["state"], "integration-conflict")
        self.assertEqual(adopted["integration_conflict_paths"], ["agent-result.txt"])
        self.assertEqual(adopted["integration_source_head"], source_head)

    def test_initial_conflict_adoption_rejects_unrecorded_index_resolution(self) -> None:
        manifest, worker, source_head, target_head = self.prepare_integration_conflict()
        marker = self.root / "pre-adoption-index-tamper-kill"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--onto"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertTrue(self.active_rebase_paths(worker))
        self.assertEqual(self.manifests()[0]["state"], "integration-rebase-pending")

        conflict = worker / "agent-result.txt"
        conflict.write_text("unrecorded external resolution\n", encoding="utf-8")
        self.git(worker, "add", "agent-result.txt")
        staged_tree = self.git(worker, "write-tree").stdout.strip()

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 2)
        diagnostic = retry.stderr.lower()
        self.assertTrue(
            b"unprovable" in diagnostic
            or b"index" in diagnostic
            or b"conflict" in diagnostic,
            diagnostic,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertEqual(retained["integration_source_head"], source_head)
        self.assertEqual(retained["integration_target_head"], target_head)
        self.assertEqual(self.git(worker, "write-tree").stdout.strip(), staged_tree)
        self.assertEqual(conflict.read_text(encoding="utf-8"), "unrecorded external resolution\n")
        self.assertTrue(self.active_rebase_paths(worker))

    def test_post_git_successful_initial_rebase_crash_adopts_and_lands_candidate(
        self,
    ) -> None:
        manifest, worker, source_head, target_head = self.prepare_successful_rebase()
        marker = self.root / "post-successful-initial-rebase-kill"

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--onto"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-rebase-pending")
        candidate = self.git(worker, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(candidate, source_head)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(
                self.control,
                "rev-parse",
                self.source_anchor_ref(manifest["run_id"]),
            ).stdout.strip(),
            source_head,
        )

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integration_candidate_head"], candidate)
        self.assertEqual(cleaned["integrated_head"], candidate)
        self.assertFalse(worker.exists())

    def test_post_git_successful_initial_rebase_crash_allows_exact_anchored_abort(
        self,
    ) -> None:
        manifest, worker, source_head, target_head = self.prepare_successful_rebase()
        marker = self.root / "post-successful-initial-rebase-abort-kill"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--onto"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.assertFalse(self.active_rebase_paths(worker))
        candidate = self.git(worker, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(candidate, source_head)

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertEqual(self.manifests()[0]["state"], "preserved")
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                self.source_anchor_ref(manifest["run_id"]),
                check=False,
            ).returncode,
            1,
        )

    def test_dirty_primary_can_abort_post_git_initial_conflict_crash(self) -> None:
        manifest, worker, source_head, target_head = self.prepare_integration_conflict()
        marker = self.root / "post-initial-rebase-dirty-abort-kill"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--onto"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        (self.control / "unrelated-primary-dirt.txt").write_text(
            "preserve unrelated dirt\n",
            encoding="utf-8",
        )
        status_before = self.git(
            self.control,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            status_before,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(self.manifests()[0]["state"], "preserved")

    def test_post_git_continue_crash_recovers_clean_review_candidate(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        marker = self.root / "post-continue-clean-kill"

        crashed = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--continue"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertEqual(self.manifests()[0]["state"], "integration-continue-pending")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)

        retry = self.run_launcher(["--triptych-continue", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-review-pending")
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD").stdout.strip(),
            recovered["integration_candidate_head"],
        )

    def test_post_git_continue_crash_adopts_later_conflict(self) -> None:
        log = self.root / "two-conflict-worker.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "commit-two-conflicts",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        for index in (1, 2):
            (self.control / f"conflict-{index}.txt").write_text(
                f"target conflict {index}\n",
                encoding="utf-8",
            )
        self.git(self.control, "add", "conflict-1.txt", "conflict-2.txt")
        self.git(self.control, "commit", "-m", "Add two target conflicts")
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertEqual(self.manifests()[0]["integration_unmerged_paths"], ["conflict-1.txt"])
        resolution, _ = self.resolve_integration_conflict(
            manifest,
            conflict_path="conflict-1.txt",
            content="resolved first conflict\n",
        )
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        marker = self.root / "post-continue-later-conflict-kill"

        crashed = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--continue"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertEqual(self.manifests()[0]["state"], "integration-continue-pending")
        self.assertEqual(
            self.git(worker, "diff", "--name-only", "--diff-filter=U").stdout.splitlines(),
            ["conflict-2.txt"],
        )

        retry = self.run_launcher(["--triptych-continue", manifest["run_id"]])

        self.assertEqual(retry.returncode, 2)
        self.assertIn(b"unresolved", retry.stderr.lower())
        adopted = self.manifests()[0]
        self.assertEqual(adopted["state"], "integration-conflict")
        self.assertEqual(
            adopted["integration_conflict_paths"],
            ["conflict-1.txt", "conflict-2.txt"],
        )

    def test_continue_refuses_unresolved_conflict_without_changing_transaction(
        self,
    ) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        status_before = self.git(worker, "status", "--porcelain=v1").stdout
        rebase_paths = self.active_rebase_paths(worker)

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )

        self.assertEqual(continuation.returncode, 2)
        self.assertIn(b"unresolved", continuation.stderr.lower())
        self.assertIn(b"stage", continuation.stderr.lower())
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, status_before)
        self.assertEqual(self.active_rebase_paths(worker), rebase_paths)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-conflict")
        self.assertEqual(retained["integration_source_head"], source_head)
        self.assertEqual(retained["integration_target_head"], target_head)
        self.assertEqual(retained["integration_conflict_paths"], ["agent-result.txt"])

    def test_managed_resolver_stages_only_and_ordinary_reopen_refuses(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        reopen_log = self.root / "conflict-ordinary-reopen.jsonl"

        reopen = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(reopen_log)},
        )
        self.assertEqual(reopen.returncode, 2)
        self.assertIn(b"resolver", reopen.stderr.lower())
        self.assertFalse(reopen_log.exists())

        resolution, resolver_log = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        records = self.records(resolver_log)
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["role"], "resolver")
        self.assertEqual(record["run_id"], manifest["run_id"])
        self.assertEqual(
            record["temporary_environment"],
            {name: manifest["tmpdir"] for name in ("TMPDIR", "TMP", "TEMP")},
        )
        self.assertEqual(Path(record["root"]), worker)
        self.assertEqual(Path(record["workdir"]), worker)
        self.assertEqual(Path(record["process_cwd"]), worker)
        self.assertIsNone(record["branch"])
        resolver_prompt = record["argv"][-1]
        self.assertIn("Resolve and stage only", resolver_prompt)
        self.assertIn("Do not run git rebase", resolver_prompt)
        self.assertIn("launcher owns continuation and abort", resolver_prompt)
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "manually resolved result\n",
        )
        self.assertEqual(
            self.git(worker, "diff", "--name-only", "--diff-filter=U").stdout,
            "",
        )
        self.assertIn("M  agent-result.txt", self.git(worker, "status", "--porcelain=v1").stdout)
        self.assertTrue(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.manifests()[0]["state"], "integration-conflict")

    def test_subdir_run_resolver_opens_root_but_reopen_preserves_subdir(self) -> None:
        worker_log = self.root / "subdir-conflict-worker.jsonl"
        result = self.run_launcher(
            cwd=self.control / "subdir",
            environment={
                "FAKE_CODEX_LOG": str(worker_log),
                "FAKE_CODEX_ACTION": "commit",
            },
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        self.assertEqual(Path(self.records(worker_log)[0]["workdir"]), worker / "subdir")
        (self.control / "agent-result.txt").write_text("root target conflict\n", encoding="utf-8")
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Add root target conflict")
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)

        resolver_log = self.root / "subdir-root-resolver.jsonl"
        resolution = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(resolver_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
            },
        )
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        resolver = self.records(resolver_log)[0]
        self.assertEqual(Path(resolver["workdir"]), worker)
        self.assertEqual(Path(resolver["process_cwd"]), worker)
        self.assertEqual(Path(resolver["root"]), worker)

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        reopen_log = self.root / "subdir-after-abort-reopen.jsonl"
        reopen = self.run_launcher(
            ["--triptych-reopen", manifest["run_id"]],
            environment={"FAKE_CODEX_LOG": str(reopen_log)},
        )
        self.assertEqual(reopen.returncode, 0, reopen.stderr.decode())
        reopened = self.records(reopen_log)[0]
        self.assertEqual(Path(reopened["workdir"]), worker / "subdir")
        self.assertEqual(Path(reopened["process_cwd"]), worker / "subdir")

    def test_resolver_rejects_forwarded_prompt_and_keeps_fixed_guard(self) -> None:
        manifest, _, _, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        rejected_log = self.root / "resolver-replacement-rejected.jsonl"

        rejected = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"], "replace the safety prompt"],
            environment={
                "FAKE_CODEX_LOG": str(rejected_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
            },
        )

        self.assertEqual(rejected.returncode, 2)
        self.assertIn(b"exactly one run ID", rejected.stderr)
        self.assertFalse(rejected_log.exists())
        self.assertEqual(self.manifests()[0]["state"], "integration-conflict")

        guard_log = self.root / "resolver-fixed-guard.jsonl"
        accepted = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(guard_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
            },
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr.decode())
        record = self.records(guard_log)[0]
        self.assertEqual(record["argv"][-2], "--")
        guard = record["argv"][-1]
        self.assertIn("Resolve and stage only", guard)
        self.assertIn("Do not run git rebase", guard)
        self.assertIn("Do not", guard)
        manifest_text = json.dumps(self.manifests()[0], sort_keys=True)
        self.assertNotIn(guard, manifest_text)
        self.assertNotIn("replace the safety prompt", manifest_text)

    def test_resolver_overstage_remains_correctable(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolver_log = self.root / "resolver-extra-staged.jsonl"

        resolution = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(resolver_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_EXTRA_STAGED": "unrelated-resolver-file.txt",
            },
        )

        self.assertEqual(resolution.returncode, 2)
        self.assertIn(b"remains correctable", resolution.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertTrue(self.active_rebase_paths(worker))
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-conflict")
        self.assertNotIn("integration_candidate_head", retained)

        correction = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(self.root / "resolver-overstage-correction.jsonl"),
                "FAKE_CODEX_ACTION": "correct-overstage",
                "FAKE_CODEX_EXTRA_STAGED": "unrelated-resolver-file.txt",
            },
        )
        self.assertEqual(correction.returncode, 0, correction.stderr.decode())
        self.assertFalse((worker / "unrelated-resolver-file.txt").exists())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "integration-review-pending")

    def test_resolver_overstage_can_be_explicitly_aborted(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        original_baseline = (worker / "baseline.txt").read_bytes()
        resolution = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(self.root / "resolver-overstage-abort.jsonl"),
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_EXTRA_STAGED": "baseline.txt",
            },
        )
        self.assertEqual(resolution.returncode, 2)
        self.assertEqual(self.manifests()[0]["state"], "integration-conflict")

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual((worker / "baseline.txt").read_bytes(), original_baseline)

    def test_protected_index_overstage_can_be_corrected(self) -> None:
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "protected-index-worker.jsonl"),
                "FAKE_CODEX_ACTION": "commit-conflict-with-companion",
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        worker = Path(manifest["worktree"])
        (self.control / "agent-result.txt").write_text(
            "conflicting primary result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "agent-result.txt")
        self.git(self.control, "commit", "-m", "Add conflicting primary result")
        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        protected_path = "companion-result.txt"
        original_protected = (worker / protected_path).read_bytes()
        self.assertIn(
            protected_path,
            self.manifests()[0]["integration_protected_index_paths"],
        )

        overstage = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(self.root / "protected-index-overstage.jsonl"),
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_EXTRA_STAGED": protected_path,
            },
        )
        self.assertEqual(overstage.returncode, 2)
        self.assertIn(b"remains correctable", overstage.stderr.lower())
        self.assertEqual(self.manifests()[0]["state"], "integration-conflict")

        correction = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(self.root / "protected-index-correction.jsonl"),
                "FAKE_CODEX_ACTION": "correct-protected-overstage",
                "FAKE_CODEX_EXTRA_STAGED": protected_path,
            },
        )
        self.assertEqual(correction.returncode, 0, correction.stderr.decode())
        self.assertEqual((worker / protected_path).read_bytes(), original_protected)
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "integration-review-pending")

    def test_source_anchor_tamper_quarantines_before_resolver_launch(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.git(self.control, "update-ref", anchor, target_head, source_head)
        resolver_log = self.root / "source-anchor-tamper-resolver.jsonl"

        resolver = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(resolver_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
            },
        )

        self.assertEqual(resolver.returncode, 2)
        self.assertIn(b"source anchor changed", resolver.stderr.lower())
        self.assertFalse(resolver_log.exists())
        self.assertTrue(self.active_rebase_paths(worker))
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("source anchor", retained["integration_recovery_error"])

    def test_initial_rebase_pending_rejects_peeled_tag_anchor_tamper(self) -> None:
        manifest, worker, source_head, _ = self.prepare_integration_conflict()
        marker = self.root / "initial-pending-tag-anchor-kill"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--onto"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        anchor = self.source_anchor_ref(manifest["run_id"])
        tag_ref = f"refs/tags/anchor-tamper-{manifest['run_id']}"
        self.git(self.control, "tag", "-a", tag_ref.removeprefix("refs/tags/"), source_head, "-m", "Anchor tamper")
        tag_object = self.git(self.control, "rev-parse", tag_ref).stdout.strip()
        self.assertNotEqual(tag_object, source_head)
        self.git(self.control, "update-ref", anchor, tag_object, source_head)

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 2)
        self.assertIn(b"unprovable", retry.stderr)
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("preflight", retained["integration_recovery_error"])
        self.assertTrue(self.active_rebase_paths(worker))

    def test_continue_pending_anchor_tamper_records_recovery_failure(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        pending = self.manifests()[0]
        pending["state"] = "integration-continue-pending"
        pending["integration_continue_started_at"] = "2000-01-01T00:00:00+00:00"
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(pending, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.git(self.control, "update-ref", anchor, target_head, source_head)

        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])

        self.assertEqual(continuation.returncode, 2)
        self.assertIn(b"source anchor changed", continuation.stderr.lower())
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("continuation", retained["integration_recovery_error"])
        self.assertTrue(self.active_rebase_paths(worker))

    def test_resolver_cannot_change_launcher_owned_rebase_metadata(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolver_log = self.root / "resolver-metadata-tamper.jsonl"

        resolution = self.run_launcher(
            ["--triptych-resolve", manifest["run_id"]],
            environment={
                "FAKE_CODEX_LOG": str(resolver_log),
                "FAKE_CODEX_ACTION": "tamper-rebase-todo",
            },
        )

        self.assertEqual(resolution.returncode, 2)
        self.assertIn(b"unverified state", resolution.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertTrue(self.active_rebase_paths(worker))
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("altered", retained["integration_recovery_error"])

    def test_exact_interrupted_continue_can_be_retried_by_the_launcher(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        pending = self.manifests()[0]
        pending["state"] = "integration-continue-pending"
        pending["integration_continue_started_at"] = "2000-01-01T00:00:00+00:00"
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(pending, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )

        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        review = self.manifests()[0]
        self.assertEqual(review["state"], "integration-review-pending")
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD").stdout.strip(),
            review["integration_candidate_head"],
        )
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )

    def test_continue_stops_for_review_then_fresh_integrate_lands_and_cleans(
        self,
    ) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        self.assertIn(b"review", continuation.stderr.lower())
        review = self.manifests()[0]
        candidate_head = review["integration_candidate_head"]
        self.assertEqual(review["state"], "integration-review-pending")
        self.assertEqual(review["final_head"], source_head)
        self.assertEqual(review["integration_source_head"], source_head)
        self.assertEqual(review["integration_target_head"], target_head)
        self.assertNotEqual(candidate_head, source_head)
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD").stdout.strip(),
            candidate_head,
        )
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD^").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(worker, "symbolic-ref", "--short", "HEAD").stdout.strip(),
            manifest["branch"],
        )
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )

        landing = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(landing.returncode, 0, landing.stderr.decode())
        self.assertIn(b"integrated and cleaned", landing.stderr)
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            candidate_head,
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "manually resolved result\n",
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integration_candidate_head"], candidate_head)
        self.assertEqual(cleaned["integrated_head"], candidate_head)

    def test_abort_restores_exact_audited_source_and_archives_attempt(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertIn(b"restored", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(worker, "symbolic-ref", "--short", "HEAD").stdout.strip(),
            manifest["branch"],
        )
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "committed result\n",
        )
        restored = self.manifests()[0]
        self.assertEqual(restored["state"], "preserved")
        self.assertEqual(restored["final_head"], source_head)
        self.assertEqual(restored["last_integration_source_head"], source_head)
        self.assertEqual(restored["last_integration_target_head"], target_head)
        self.assertEqual(
            restored["last_integration_conflict_paths"],
            ["agent-result.txt"],
        )
        self.assertNotIn("integration_source_head", restored)
        self.assertNotIn("integration_target_head", restored)
        self.assertNotIn("integration_conflict_paths", restored)
        self.assertNotIn("integration_candidate_head", restored)

    def test_abort_restores_a_clean_review_pending_candidate(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        restored = self.manifests()[0]
        self.assertEqual(restored["state"], "preserved")
        self.assertEqual(restored["last_integration_candidate_head"], candidate)
        self.assertEqual(restored["last_integration_source_head"], source_head)
        self.assertEqual(restored["last_integration_target_head"], target_head)

    def test_abort_restores_pre_landing_verification_failed_candidate(self) -> None:
        failed, worker, source_head, candidate, advanced_target = (
            self.create_pre_landing_manual_verification_failure()
        )
        anchor = self.source_anchor_ref(failed["run_id"])
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        primary_ref = self.git(self.control, "symbolic-ref", "HEAD").stdout.strip()
        primary_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        primary_tree = self.git(self.control, "write-tree").stdout.strip()
        primary_status = self.git(
            self.control,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(self.control, "symbolic-ref", "HEAD").stdout.strip(), primary_ref)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), primary_head)
        self.assertEqual(self.git(self.control, "write-tree").stdout.strip(), primary_tree)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            primary_status,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                anchor,
                check=False,
            ).returncode,
            1,
        )
        restored = self.manifests()[0]
        self.assertEqual(restored["state"], "preserved")
        self.assertEqual(restored["last_integration_source_head"], source_head)
        self.assertEqual(
            restored["last_integration_target_head"],
            failed["integration_target_head"],
        )
        self.assertEqual(restored["last_integration_candidate_head"], candidate)

    def test_abort_refuses_changed_pre_landing_verification_failed_candidate(self) -> None:
        failed, worker, source_head, candidate, advanced_target = (
            self.create_pre_landing_manual_verification_failure()
        )
        anchor = self.source_anchor_ref(failed["run_id"])
        conflict = worker / "agent-result.txt"
        conflict.write_text("changed after verification failure\n", encoding="utf-8")

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"candidate changed", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(
            conflict.read_text(encoding="utf-8"),
            "changed after verification failure\n",
        )
        self.assertNotEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

        self.git(worker, "reset", "--hard", candidate)
        self.git(
            worker,
            "commit",
            "--allow-empty",
            "-m",
            "Change candidate after verification failure",
        )
        changed_head = self.git(worker, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(changed_head, candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")

        retry = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(retry.returncode, 2)
        self.assertIn(b"candidate changed", retry.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), changed_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

    def test_abort_refuses_changed_pre_landing_source_anchor(self) -> None:
        failed, worker, source_head, candidate, advanced_target = (
            self.create_pre_landing_manual_verification_failure()
        )
        anchor = self.source_anchor_ref(failed["run_id"])
        self.git(self.control, "update-ref", anchor, candidate, source_head)

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"source anchor changed", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), candidate)
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("anchor", retained["integration_recovery_error"])

    def test_abort_refuses_verification_failure_with_integrated_head(self) -> None:
        manifest, worker, candidate, advanced_target = (
            self.create_interrupted_manual_verification(advance_target=True)
        )
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 2)
        failed = self.manifests()[0]
        self.assertEqual(failed["state"], "integration-verification-failed")
        self.assertEqual(failed["integrated_head"], candidate)
        anchor = self.source_anchor_ref(failed["run_id"])
        source_head = failed["integration_source_head"]

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"landing result or checkpoint", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

    def test_abort_refuses_verification_failure_with_landing_checkpoint(self) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        marker = self.root / "manual-abort-landing-ref-race"
        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.landing_race_environment(marker=marker, action="ref"),
        )
        self.assertEqual(landing.returncode, 2)
        self.assertTrue(marker.exists())
        failed = self.manifests()[0]
        self.assertEqual(failed["state"], "integration-verification-failed")
        self.assertNotIn("integrated_head", failed)
        for field in (
            "integration_manual_landing_started_at",
            "integration_landing_expected_head",
            "integration_landing_candidate_head",
            "integration_landing_started_at",
        ):
            self.assertIn(field, failed)
        raced_target = self.git(
            self.control,
            "rev-parse",
            "refs/heads/main",
        ).stdout.strip()
        anchor = self.source_anchor_ref(failed["run_id"])
        source_head = failed["integration_source_head"]

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"landing result or checkpoint", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            raced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

    def test_abort_refuses_verification_failure_with_only_manual_landing_checkpoint(
        self,
    ) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        pending = self.manifests()[0]
        checkpoint = "2000-01-01T00:00:00+00:00"
        pending["state"] = "integration-manual-landing-pending"
        pending["integration_manual_landing_started_at"] = checkpoint
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(pending, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.control / "target-after-manual-landing-checkpoint.txt").write_text(
            "target advanced after manual landing checkpoint\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "target-after-manual-landing-checkpoint.txt")
        self.git(
            self.control,
            "commit",
            "-m",
            "Advance target after manual landing checkpoint",
        )
        advanced_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 2)
        failed = self.manifests()[0]
        self.assertEqual(failed["state"], "integration-verification-failed")
        self.assertEqual(failed["integration_manual_landing_started_at"], checkpoint)
        self.assertNotIn("integrated_head", failed)
        for field in (
            "integration_landing_expected_head",
            "integration_landing_candidate_head",
            "integration_landing_started_at",
        ):
            self.assertNotIn(field, failed)
        anchor = self.source_anchor_ref(failed["run_id"])
        source_head = failed["integration_source_head"]

        abort = self.run_launcher(["--triptych-abort", failed["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"landing result or checkpoint", abort.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "refs/heads/main").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

    def test_external_rebase_abort_cannot_masquerade_as_launcher_abort(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])

        self.git(worker, "rebase", "--abort")
        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 2)
        self.assertIn(b"rebase administration changed", abort.stderr)
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-rebase-recovery-failed")
        self.assertIn("rebase tamper", retained["integration_recovery_error"])
        self.assertNotIn("last_integration_aborted_at", retained)
        self.assertEqual(retained["integration_source_head"], source_head)

    def test_abort_adopts_proven_pre_git_rebase_checkpoint(self) -> None:
        manifest, worker, source_head, target_head = self.prepare_integration_conflict()
        anchor = self.source_anchor_ref(manifest["run_id"])
        manifest.update(
            {
                "state": "integration-rebase-pending",
                "integration_previous_state": "preserved",
                "integration_source_head": source_head,
                "integration_target_head": target_head,
                "integration_started_at": "2000-01-01T00:00:00+00:00",
                "integration_source_anchor_created": True,
            }
        )
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.git(self.control, "update-ref", anchor, source_head)

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.manifests()[0]["state"], "preserved")
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                anchor,
                check=False,
            ).returncode,
            1,
        )

    def test_source_anchor_survives_reflog_expiry_gc_and_exact_abort(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]
        self.assertNotEqual(candidate, source_head)

        self.git(
            self.control,
            "reflog",
            "expire",
            "--expire=now",
            "--expire-unreachable=now",
            "--all",
        )
        self.git(self.control, "gc", "--prune=now")

        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(
            self.git(self.control, "cat-file", "-t", source_head).stdout.strip(),
            "commit",
        )
        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertEqual(
            self.git(self.control, "show-ref", "--verify", "--quiet", anchor, check=False).returncode,
            1,
        )

    def test_abort_anchor_cleanup_refusal_is_retryable(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "refuse-abort-anchor-delete"

        refused = self.run_launcher(
            ["--triptych-abort", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "-d", anchor, source_head],
                marker=marker,
                action="refuse",
            ),
        )

        self.assertEqual(refused.returncode, 2)
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "integration-abort-pending")

        retry = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "preserved")
        self.assertEqual(
            self.git(self.control, "show-ref", "--verify", "--quiet", anchor, check=False).returncode,
            1,
        )

    def test_post_git_abort_anchor_delete_crash_is_idempotent(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "post-abort-anchor-delete-kill"

        crashed = self.run_launcher(
            ["--triptych-abort", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "-d", anchor, source_head],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertEqual(self.manifests()[0]["state"], "integration-abort-pending")
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                anchor,
                check=False,
            ).returncode,
            1,
        )

        retry = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "preserved")

    def test_post_git_abort_crash_retries_exact_restoration(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "post-abort-kill"

        crashed = self.run_launcher(
            ["--triptych-abort", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--abort"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertEqual(self.manifests()[0]["state"], "integration-abort-pending")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)

        retry = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "preserved")
        self.assertEqual(
            self.git(self.control, "show-ref", "--verify", "--quiet", anchor, check=False).returncode,
            1,
        )

    def test_refused_git_abort_remains_provable_and_retryable(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "refused-managed-git-abort"

        refused = self.run_launcher(
            ["--triptych-abort", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=worker,
                tokens=["rebase", "--abort"],
                marker=marker,
                action="refuse",
            ),
        )

        self.assertEqual(refused.returncode, 2)
        self.assertTrue(marker.exists())
        self.assertIn(b"still-provable retained state", refused.stderr)
        self.assertTrue(self.active_rebase_paths(worker))
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-abort-pending")
        self.assertEqual(pending["integration_abort_mode"], "rebase")

        retry = self.run_launcher(["--triptych-abort", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "preserved")

    def test_worker_abort_ignores_unrelated_primary_dirt(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        (self.control / "baseline.txt").write_text("dirty primary baseline\n", encoding="utf-8")
        self.git(self.control, "add", "baseline.txt")
        unrelated = self.control / "unrelated-primary-dirt.txt"
        unrelated.write_text("preserve primary dirt\n", encoding="utf-8")
        status_before = self.git(
            self.control,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout
        baseline_before = (self.control / "baseline.txt").read_bytes()

        abort = self.run_launcher(["--triptych-abort", manifest["run_id"]])

        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            status_before,
        )
        self.assertEqual((self.control / "baseline.txt").read_bytes(), baseline_before)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "preserve primary dirt\n")
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")

    def test_abort_ignores_deleted_target_ref(self) -> None:
        self.assert_abort_ignores_target_change("deleted")

    def test_abort_ignores_rewound_target_ref(self) -> None:
        self.assert_abort_ignores_target_change("rewound")

    def test_abort_ignores_unrelated_target_ref(self) -> None:
        self.assert_abort_ignores_target_change("unrelated")

    def test_landing_anchor_cleanup_refusal_retains_ref_for_opaque_retry(self) -> None:
        manifest, _, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "refuse-landing-anchor-delete"

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )

        self.assertEqual(landing.returncode, 1, landing.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertIn(manifest["branch"], self.worker_branches())
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)
        self.assertEqual(self.manifests()[0]["state"], "cleaned-ref-retained")

        (self.control / "after-ref-cleanup-refusal.txt").write_text(
            "advance after cleanup refusal\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "after-ref-cleanup-refusal.txt")
        self.git(self.control, "commit", "-m", "Advance after ref cleanup refusal")
        unsafe_retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(unsafe_retry.returncode, 2)
        self.assertIn(b"not the exact", unsafe_retry.stderr)
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)

        self.git(self.control, "reset", "--hard", candidate)
        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertEqual(
            self.git(self.control, "show-ref", "--verify", "--quiet", anchor, check=False).returncode,
            1,
        )

    def test_post_git_landing_anchor_delete_crash_is_idempotent(self) -> None:
        manifest, _, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "post-landing-anchor-delete-kill"

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "cleaned-ref-retained")
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                anchor,
                check=False,
            ).returncode,
            1,
        )

        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_cleanup_refuses_impossible_partial_ref_transaction(self) -> None:
        manifest, _, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(["--triptych-continue", manifest["run_id"]])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "retain-both-cleanup-refs"
        refused = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="refuse",
            ),
        )
        self.assertEqual(refused.returncode, 1, refused.stderr.decode())

        self.git(self.control, "update-ref", "-d", anchor, source_head)
        missing_anchor = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(missing_anchor.returncode, 2)
        self.assertIn(b"only partial", missing_anchor.stderr)
        self.assertIn(manifest["branch"], self.worker_branches())

        self.git(self.control, "update-ref", anchor, source_head)
        branch_ref = f"refs/heads/{manifest['branch']}"
        self.git(self.control, "update-ref", "-d", branch_ref, candidate)
        missing_branch = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(missing_branch.returncode, 2)
        self.assertIn(b"only partial", missing_branch.stderr)
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), source_head)

    def test_manual_cleanup_atomically_refuses_concurrent_target_advance(self) -> None:
        manifest, _, candidate, target_head = self.create_review_pending_candidate()
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.git(self.control, "merge", "--ff-only", candidate)
        (self.control / "concurrent-cleanup-advance.txt").write_text(
            "concurrent descendant\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "concurrent-cleanup-advance.txt")
        self.git(self.control, "commit", "-m", "Advance target during cleanup")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.git(self.control, "reset", "--hard", target_head)
        marker = self.root / "concurrent-manual-cleanup-target"

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--stdin"],
                marker=marker,
                action="move-ref",
                move_ref=(manifest["target_ref"], descendant, candidate),
            ),
        )

        self.assertEqual(landing.returncode, 1, landing.stderr.decode())
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), descendant)
        self.assertIn(manifest["branch"], self.worker_branches())
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            self.manifests()[0]["integration_source_head"],
        )
        self.assertEqual(self.manifests()[0]["state"], "cleaned-ref-retained")

        self.git(self.control, "reset", "--hard", candidate)
        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_post_git_worktree_removal_crash_adopts_cleanup(self) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "post-worktree-removal-kill"
        temporary = Path(manifest["tmpdir"])
        (temporary / "pending-review").mkdir()
        (temporary / "pending-review/page.png").write_bytes(b"review raster")

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "remove", str(worker)],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertIn(manifest["branch"], self.worker_branches())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-cleanup-pending")
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            pending["integration_source_head"],
        )
        self.assertTrue((temporary / "pending-review/page.png").is_file())

        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.worker_branches(), [])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")
        self.assertFalse(temporary.exists())
        self.assertEqual(
            self.git(
                self.control,
                "show-ref",
                "--verify",
                "--quiet",
                anchor,
                check=False,
            ).returncode,
            1,
        )

    def test_post_git_worktree_unlock_crash_relocks_and_retries_cleanup(self) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        anchor = self.source_anchor_ref(manifest["run_id"])
        marker = self.root / "post-worktree-unlock-kill"

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["worktree", "unlock", str(worker)],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-cleanup-pending")
        self.assertEqual(pending["cleanup_expected_head"], candidate)
        self.assertTrue(worker.exists())
        self.assertNotIn("locked\n", self.worktree_output())
        self.assertEqual(self.git(self.control, "rev-parse", anchor).stdout.strip(), pending["integration_source_head"])

        retry = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_target_advance_during_resolution_retains_completed_candidate(self) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())

        (self.control / "target-during-resolution.txt").write_text(
            "target moved during manual resolution\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "target-during-resolution.txt")
        self.git(self.control, "commit", "-m", "Advance target during resolution")
        advanced_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )

        self.assertEqual(continuation.returncode, 2)
        self.assertIn(b"target advanced", continuation.stderr.lower())
        review = self.manifests()[0]
        candidate = review["integration_candidate_head"]
        self.assertEqual(review["state"], "integration-review-pending")
        self.assertEqual(review["final_head"], source_head)
        self.assertEqual(review["integration_target_head"], target_head)
        self.assertEqual(review["integration_target_mismatch_head"], advanced_target)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertFalse(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            advanced_target,
        )

        landing = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(landing.returncode, 2)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

    def test_target_advance_refuses_review_pending_candidate_without_discarding_it(
        self,
    ) -> None:
        manifest, worker, source_head, target_head, integrate = (
            self.create_integration_conflict()
        )
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())
        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]]
        )
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        candidate = self.manifests()[0]["integration_candidate_head"]

        (self.control / "target-after-resolution.txt").write_text(
            "later target result\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "target-after-resolution.txt")
        self.git(self.control, "commit", "-m", "Advance target after resolution")
        advanced_target = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        landing = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(landing.returncode, 2)
        target_diagnostic = landing.stderr.lower()
        self.assertIn(b"target", target_diagnostic)
        self.assertTrue(
            b"exact" in target_diagnostic or b"advanced" in target_diagnostic,
            target_diagnostic,
        )
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            advanced_target,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertTrue(worker.exists())
        self.assertEqual(
            self.git(worker, "rev-parse", "HEAD^").stdout.strip(),
            target_head,
        )
        retained = self.manifests()[0]
        self.assertEqual(retained["state"], "integration-verification-failed")
        self.assertEqual(retained["final_head"], source_head)
        self.assertEqual(retained["integration_target_head"], target_head)
        self.assertEqual(retained["integration_candidate_head"], candidate)
        self.assertNotIn("integrated_head", retained)

    def test_manual_landing_disables_target_post_merge_hook(self) -> None:
        manifest, _, candidate, _ = self.create_review_pending_candidate()
        hook_marker = self.root / "manual-post-merge-hook-called"
        hook = self.control / ".git/hooks/post-merge"
        hook.write_text(
            "#!/bin/sh\n"
            ': > "$TRIPTYCH_TEST_MANUAL_HOOK_CALLED"\n'
            "exit 97\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment={"TRIPTYCH_TEST_MANUAL_HOOK_CALLED": str(hook_marker)},
        )

        self.assertEqual(landing.returncode, 0, landing.stderr.decode())
        self.assertFalse(hook_marker.exists())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_ordinary_landing_checkout_race_preserves_the_new_checkout(self) -> None:
        self.assert_landing_race(manual=False, action="checkout")

    def test_ordinary_landing_symref_race_preserves_the_new_checkout(self) -> None:
        self.assert_landing_race(manual=False, action="symref")

    def test_ordinary_landing_ref_race_retains_then_retries(self) -> None:
        self.assert_landing_race(manual=False, action="ref")

    def test_manual_landing_checkout_race_preserves_the_new_checkout(self) -> None:
        self.assert_landing_race(manual=True, action="checkout")

    def test_manual_landing_symref_race_preserves_the_new_checkout(self) -> None:
        self.assert_landing_race(manual=True, action="symref")

    def test_manual_landing_ref_race_retains_then_retries(self) -> None:
        self.assert_landing_race(manual=True, action="ref")

    def test_manual_landing_pre_record_crash_recovers_exact_candidate(self) -> None:
        manifest, worker, candidate, target_head = self.create_review_pending_candidate()
        marker = self.root / "post-manual-merge-kill"

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-manual-landing-pending")
        self.assertTrue(pending["integration_manual_resolution"])
        self.assertNotIn("integrated_head", pending)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        anchor = self.source_anchor_ref(manifest["run_id"])
        self.assertEqual(
            self.git(self.control, "rev-parse", anchor).stdout.strip(),
            pending["integration_source_head"],
        )

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integrated_head"], candidate)
        self.assertEqual(
            self.git(self.control, "show-ref", "--verify", "--quiet", anchor, check=False).returncode,
            1,
        )

    def test_manual_landing_descendant_refuses_then_exact_reconciliation_recovers(self) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        marker = self.root / "post-manual-merge-before-descendant"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        (self.control / "descendant-after-manual-crash.txt").write_text(
            "descendant\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "descendant-after-manual-crash.txt")
        self.git(self.control, "commit", "-m", "Advance past manual candidate")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        refusal = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(refusal.returncode, 2)
        diagnostic = refusal.stderr.lower()
        self.assertIn(b"target", diagnostic)
        self.assertTrue(
            b"exact" in diagnostic
            or b"eligible" in diagnostic
            or b"advanced" in diagnostic,
            diagnostic,
        )
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), descendant)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

        self.git(self.control, "reset", "--hard", candidate)
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_manual_landing_unrelated_sibling_refuses_then_exact_recovers(self) -> None:
        manifest, worker, candidate, target_head = self.create_review_pending_candidate()
        marker = self.root / "post-manual-merge-before-sibling"
        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
            ),
        )
        self.assertLess(crashed.returncode, 0)
        self.git(self.control, "reset", "--hard", target_head)
        (self.control / "unrelated-sibling.txt").write_text(
            "unrelated sibling\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "unrelated-sibling.txt")
        self.git(self.control, "commit", "-m", "Create unrelated target sibling")
        sibling = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        refusal = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(refusal.returncode, 2)
        diagnostic = refusal.stderr.lower()
        self.assertIn(b"target", diagnostic)
        self.assertTrue(
            b"exact" in diagnostic
            or b"eligible" in diagnostic
            or b"advanced" in diagnostic,
            diagnostic,
        )
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), sibling)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.manifests()[0]["state"], "integration-verification-failed")

        self.git(self.control, "reset", "--hard", candidate)
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_manual_landing_dirty_verification_recovers_through_integrate(self) -> None:
        manifest, worker, candidate, _ = self.create_review_pending_candidate()
        marker = self.root / "post-manual-merge-dirty"
        dirty = self.control / "unrelated-verification-dirt.txt"

        landing = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
                action="dirty",
                dirty_path=dirty,
            ),
        )

        self.assertEqual(landing.returncode, 2)
        self.assertTrue(dirty.exists())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        failed = self.manifests()[0]
        self.assertTrue(failed["integration_manual_resolution"])
        self.assertEqual(failed["state"], "integration-verification-failed")

        dirty.unlink()
        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_interrupted_manual_verification_retries_exact_candidate_cleanup(
        self,
    ) -> None:
        manifest, _, candidate, target_head = (
            self.create_interrupted_manual_verification(advance_target=False)
        )
        self.assertEqual(target_head, candidate)

        retry = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]]
        )

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            candidate,
        )
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

    def test_interrupted_manual_verification_refuses_descendant_on_integrate(
        self,
    ) -> None:
        manifest, worker, candidate, target_head = (
            self.create_interrupted_manual_verification(advance_target=True)
        )

        retry = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]]
        )

        self.assertEqual(retry.returncode, 2)
        self.assertIn(b"not the exact", retry.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        retained = self.manifests()[0]
        self.assertEqual(
            retained["state"],
            "integration-verification-failed",
        )
        self.assertEqual(retained["integration_candidate_head"], candidate)
        self.assertEqual(retained["integrated_head"], candidate)

    def test_interrupted_manual_verification_refuses_descendant_on_clean(
        self,
    ) -> None:
        manifest, worker, candidate, target_head = (
            self.create_interrupted_manual_verification(advance_target=True)
        )

        cleanup = self.run_launcher(["--triptych-clean", manifest["run_id"]])

        self.assertEqual(cleanup.returncode, 2)
        self.assertIn(b"target changed", cleanup.stderr.lower())
        self.assertEqual(
            self.git(self.control, "rev-parse", "HEAD").stdout.strip(),
            target_head,
        )
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        retained = self.manifests()[0]
        self.assertEqual(
            retained["state"],
            "integration-verification-failed",
        )
        self.assertEqual(retained["integration_candidate_head"], candidate)
        self.assertEqual(retained["integrated_head"], candidate)

    def test_continue_disables_hooks_and_editors(self) -> None:
        manifest, worker, _, target_head, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolution, _ = self.resolve_integration_conflict(manifest)
        self.assertEqual(resolution.returncode, 0, resolution.stderr.decode())

        hook_called = self.root / "continue-hook-called"
        editor_called = self.root / "continue-editor-called"
        hook_script = (
            "#!/bin/sh\n"
            ': > "$TRIPTYCH_TEST_HOOK_CALLED"\n'
            "exit 91\n"
        )
        hooks = self.control / ".git/hooks"
        for name in (
            "pre-commit",
            "prepare-commit-msg",
            "commit-msg",
            "post-commit",
            "post-rewrite",
        ):
            hook = hooks / name
            hook.write_text(hook_script, encoding="utf-8")
            hook.chmod(0o755)
        editor = self.root / "hostile-editor"
        editor.write_text(
            "#!/bin/sh\n"
            ': > "$TRIPTYCH_TEST_EDITOR_CALLED"\n'
            "exit 92\n",
            encoding="utf-8",
        )
        editor.chmod(0o755)

        continuation = self.run_launcher(
            ["--triptych-continue", manifest["run_id"]],
            environment={
                "TRIPTYCH_TEST_HOOK_CALLED": str(hook_called),
                "TRIPTYCH_TEST_EDITOR_CALLED": str(editor_called),
                "GIT_EDITOR": str(editor),
                "GIT_SEQUENCE_EDITOR": str(editor),
                "EDITOR": str(editor),
                "VISUAL": str(editor),
            },
        )

        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        self.assertFalse(hook_called.exists())
        self.assertFalse(editor_called.exists())
        candidate = self.manifests()[0]["integration_candidate_head"]
        self.assertEqual(self.manifests()[0]["state"], "integration-review-pending")
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")

    def test_make_resolve_and_continue_forward_the_opaque_run_id(self) -> None:
        manifest, _, _, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        resolver_log = self.root / "make-conflict-resolver.jsonl"

        resolve = self.run_make(
            ["resolve", f"RUN={manifest['run_id']}"],
            environment={
                "FAKE_CODEX_LOG": str(resolver_log),
                "FAKE_CODEX_ACTION": "stage-conflict",
            },
        )
        self.assertEqual(resolve.returncode, 0, resolve.stderr.decode())
        self.assertEqual(self.records(resolver_log)[0]["role"], "resolver")
        continuation = self.run_make(["continue", f"RUN={manifest['run_id']}"])
        self.assertEqual(continuation.returncode, 0, continuation.stderr.decode())
        self.assertEqual(self.manifests()[0]["state"], "integration-review-pending")
        final_diff = self.run_make(["final-diff", f"RUN={manifest['run_id']}"])
        self.assertEqual(final_diff.returncode, 0, final_diff.stderr.decode())
        self.assertIn(b"manually resolved result", final_diff.stdout)
        self.assertNotIn(os.fsencode(manifest["worktree"]), final_diff.stdout)

    def test_make_status_reopen_and_clean_run_cover_retained_lifecycle(self) -> None:
        first_log = self.root / "make-lifecycle-first.jsonl"
        first = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(first_log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        manifest = self.manifests()[0]

        overview = self.run_make(["status"])
        self.assertEqual(overview.returncode, 0, overview.stderr.decode())
        self.assertIn(os.fsencode(manifest["run_id"]), overview.stdout)
        self.assertIn(b"preserved", overview.stdout)
        self.assertNotIn(os.fsencode(manifest["worktree"]), overview.stdout)

        exact = self.run_make(["status", f"RUN={manifest['run_id']}"])
        self.assertEqual(exact.returncode, 0, exact.stderr.decode())
        self.assertIn(os.fsencode(manifest["run_id"]), exact.stdout)
        self.assertIn(b"preserved", exact.stdout)
        self.assertNotIn(os.fsencode(manifest["worktree"]), exact.stdout)

        positional_compatibility = self.run_make(["status", manifest["run_id"]])
        self.assertEqual(
            positional_compatibility.returncode,
            0,
            positional_compatibility.stderr.decode(),
        )
        self.assertIn(os.fsencode(manifest["run_id"]), positional_compatibility.stdout)
        self.assertNotIn(
            os.fsencode(manifest["worktree"]), positional_compatibility.stdout
        )

        second_log = self.root / "make-lifecycle-second.jsonl"
        reopened = self.run_make(
            ["reopen", f"RUN={manifest['run_id']}"],
            environment={
                "FAKE_CODEX_LOG": str(second_log),
                "FAKE_CODEX_ACTION": "remove-dirty-result",
            },
        )
        self.assertEqual(reopened.returncode, 0, reopened.stderr.decode())
        self.assertEqual(
            self.records(first_log)[0]["root"],
            self.records(second_log)[0]["root"],
        )
        refreshed = self.manifests()[0]
        self.assertEqual(refreshed["state"], "preserved")
        self.assertFalse(refreshed["dirty"])
        self.assertEqual(refreshed["final_head"], self.base_head)

        cleaned = self.run_make(["clean-run", f"RUN={manifest['run_id']}"])
        self.assertEqual(cleaned.returncode, 0, cleaned.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        self.assertEqual(self.manifests()[0]["state"], "cleaned")

        empty_overview = self.run_make(["status"])
        self.assertEqual(
            empty_overview.returncode,
            0,
            empty_overview.stderr.decode(),
        )
        self.assertEqual(empty_overview.stdout, b"No Triptych Codex runs.\n")
        cleaned_exact = self.run_make(["status", f"RUN={manifest['run_id']}"])
        self.assertEqual(
            cleaned_exact.returncode,
            0,
            cleaned_exact.stderr.decode(),
        )
        self.assertIn(os.fsencode(manifest["run_id"]), cleaned_exact.stdout)
        self.assertIn(b"cleaned", cleaned_exact.stdout)

    def test_make_lifecycle_rejects_malformed_and_variable_spoofed_calls(self) -> None:
        manifest, _, _, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        before = manifest_file.read_bytes()
        fake_log = self.root / "malformed-make-resolver.jsonl"
        environment = {
            "FAKE_CODEX_LOG": str(fake_log),
            "FAKE_CODEX_ACTION": "stage-conflict",
        }

        required_targets = (
            "integrate",
            "reopen",
            "resolve",
            "continue",
            "abort",
            "final-diff",
            "clean-run",
        )
        for target in required_targets:
            missing = self.run_make([target], environment=environment)
            self.assertEqual(missing.returncode, 2, (target, missing.stderr.decode()))
            self.assertIn(
                f"Usage: make {target} RUN=<run-id>".encode(), missing.stderr
            )

        extra = self.run_make(
            ["resolve", "unexpected-extra-goal", f"RUN={manifest['run_id']}"],
            environment=environment,
        )
        self.assertEqual(extra.returncode, 2)
        self.assertIn(b"targets must be invoked directly and alone", extra.stderr)

        status_extra = self.run_make(
            ["status", "unexpected-extra-goal", f"RUN={manifest['run_id']}"],
            environment=environment,
        )
        self.assertEqual(status_extra.returncode, 2)
        self.assertIn(
            b"targets must be invoked directly and alone", status_extra.stderr
        )

        build_sentinel = self.control / "build" / "malformed-make-must-not-clean"
        build_sentinel.parent.mkdir(parents=True, exist_ok=True)
        build_sentinel.write_text("preserve\n", encoding="utf-8")
        keep_going = self.run_make(
            ["-k", "resolve", "clean", f"RUN={manifest['run_id']}"],
            environment=environment,
        )
        self.assertEqual(keep_going.returncode, 2)
        self.assertIn(
            b"targets must be invoked directly and alone", keep_going.stderr
        )
        self.assertTrue(build_sentinel.exists())

        reversed_keep_going = self.run_make(
            ["-k", "clean", "resolve", f"RUN={manifest['run_id']}"],
            environment=environment,
        )
        self.assertEqual(reversed_keep_going.returncode, 2)
        self.assertIn(
            b"targets must be invoked directly and alone",
            reversed_keep_going.stderr,
        )
        self.assertTrue(build_sentinel.exists())

        for option in ("-k", "-j"):
            exact_two = self.run_make(
                [option, "resolve", "clean", f"RUN={manifest['run_id']}"],
                environment=environment,
            )
            self.assertEqual(exact_two.returncode, 2, exact_two.stderr.decode())
            self.assertIn(
                b"targets must be invoked directly and alone", exact_two.stderr
            )
            self.assertTrue(build_sentinel.exists())

        malformed_run_ids = (
            "2026071t140723z-5ac7333f8f7c",
            "202607160t140723z-5ac7333f8f7c",
            "20260716t14072z-5ac7333f8f7c",
            "20260716t1407230z-5ac7333f8f7c",
            "20260716T140723z-5ac7333f8f7c",
            "20260716t140723Z-5ac7333f8f7c",
            "20260716t140723z5ac7333f8f7c",
            "20260716t140723z-5ac7333f8f7",
            "20260716t140723z-5ac7333f8f7c0",
            "20260716t140723z-5ac7333f8f7g",
        )
        for malformed_run_id in malformed_run_ids:
            for target in ("resolve", "status"):
                malformed = self.run_make(
                    [target, f"RUN={malformed_run_id}"],
                    environment=environment,
                )
                self.assertEqual(
                    malformed.returncode,
                    2,
                    (target, malformed_run_id, malformed.stderr.decode()),
                )
                self.assertIn(b"invalid Triptych Codex run ID", malformed.stderr)

        for target in ("reopen", "clean-run"):
            malformed = self.run_make(
                [target, "RUN=not-a-run-id"],
                environment=environment,
            )
            self.assertEqual(
                malformed.returncode,
                2,
                (target, malformed.stderr.decode()),
            )
            self.assertIn(b"invalid Triptych Codex run ID", malformed.stderr)

        injection_marker = self.root / "make-run-id-validation-injection-called"
        injection = self.run_make(
            [
                "resolve",
                f"RUN=';touch${{IFS}}{injection_marker};:'",
            ],
            environment=environment,
        )
        self.assertEqual(injection.returncode, 2, injection.stderr.decode())
        self.assertIn(b"invalid Triptych Codex run ID", injection.stderr)
        self.assertFalse(injection_marker.exists())

        launcher_marker = self.root / "overridden-lifecycle-launcher-called"
        launcher_override = self.run_make(
            [
                "status",
                f"RUN={manifest['run_id']}",
                f"WORKTREE_MARSHAL=:; touch {launcher_marker}; :",
                f"WORKTREE_MARSHAL_STATUS_ARGUMENTS=:; touch {launcher_marker}; :",
            ],
            environment=environment,
        )
        self.assertEqual(
            launcher_override.returncode,
            0,
            launcher_override.stderr.decode(),
        )
        self.assertIn(os.fsencode(manifest["run_id"]), launcher_override.stdout)
        self.assertFalse(launcher_marker.exists())

        environment_run = self.run_make(
            ["resolve"],
            environment={**environment, "RUN": manifest["run_id"]},
        )
        self.assertEqual(environment_run.returncode, 2, environment_run.stderr.decode())
        self.assertIn(b"Usage: make resolve RUN=<run-id>", environment_run.stderr)

        internal_spoof = self.run_make(
            [
                "resolve",
                "RUN=not-a-run-id",
                f"_WORKTREE_MARSHAL_RUN_ID={manifest['run_id']}",
            ],
            environment=environment,
        )
        self.assertEqual(internal_spoof.returncode, 2, internal_spoof.stderr.decode())
        self.assertIn(b"invalid Triptych Codex run ID", internal_spoof.stderr)

        goals_spoof = self.run_make(
            ["resolve", f"RUN={manifest['run_id']}", "MAKECMDGOALS=resolve"],
            environment=environment,
        )
        self.assertEqual(goals_spoof.returncode, 2)
        self.assertIn(b"MAKECMDGOALS may not be overridden", goals_spoof.stderr)
        self.assertFalse(fake_log.exists())
        self.assertEqual(manifest_file.read_bytes(), before)

    def test_make_abort_restores_the_conflicted_worker(self) -> None:
        manifest, worker, source_head, _, integrate = self.create_integration_conflict()
        self.assertEqual(integrate.returncode, 2)

        abort = self.run_make(["abort", f"RUN={manifest['run_id']}"])
        self.assertEqual(abort.returncode, 0, abort.stderr.decode())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.manifests()[0]["state"], "preserved")

    def test_final_diff_is_complete_opaque_and_read_only(self) -> None:
        manifest, worker, candidate, target_head = self.create_review_pending_candidate()
        pending = self.manifests()[0]
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_before = manifest_file.read_bytes()
        worker_status = self.git(worker, "status", "--porcelain=v1").stdout
        dirty = self.control / "unrelated-final-diff-dirt.txt"
        dirty.write_text("preserve me\n", encoding="utf-8")
        control_status = self.git(
            self.control,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout
        external_marker = self.root / "external-diff-called"
        external = self.root / "hostile-external-diff"
        external.write_text(
            "#!/bin/sh\n"
            ': > "$TRIPTYCH_TEST_EXTERNAL_DIFF_CALLED"\n'
            "exit 91\n",
            encoding="utf-8",
        )
        external.chmod(0o755)

        review = self.run_launcher(
            ["--triptych-final-diff", manifest["run_id"]],
            environment={
                "GIT_EXTERNAL_DIFF": str(external),
                "TRIPTYCH_TEST_EXTERNAL_DIFF_CALLED": str(external_marker),
            },
        )

        self.assertEqual(review.returncode, 0, review.stderr.decode())
        self.assertIn(b"diff --git a/agent-result.txt b/agent-result.txt", review.stdout)
        self.assertIn(b"manually resolved result", review.stdout)
        self.assertIn(b"conflicting primary result", review.stdout)
        self.assertFalse(external_marker.exists())
        for private in (
            manifest["worktree"],
            manifest["tmpdir"],
            str(self.state),
            str(self.control),
        ):
            self.assertNotIn(os.fsencode(private), review.stdout)
            self.assertNotIn(os.fsencode(private), review.stderr)
        self.assertEqual(manifest_file.read_bytes(), manifest_before)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), candidate)
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, worker_status)
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), target_head)
        self.assertEqual(
            self.git(
                self.control,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            control_status,
        )
        self.assertEqual(pending["state"], "integration-review-pending")

    def test_final_diff_refuses_non_candidate_without_private_paths(self) -> None:
        log = self.root / "final-diff-non-candidate.jsonl"
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(log), "FAKE_CODEX_ACTION": "dirty"}
        )
        self.assertEqual(result.returncode, 0)
        manifest = self.manifests()[0]

        review = self.run_launcher(["--triptych-final-diff", manifest["run_id"]])

        self.assertEqual(review.returncode, 2)
        self.assertIn(b"no manually resolved final candidate", review.stderr)
        self.assertNotIn(os.fsencode(manifest["worktree"]), review.stderr)
        self.assertNotIn(os.fsencode(manifest["tmpdir"]), review.stderr)

        launcher_help = self.run_launcher(["--triptych-help"])
        self.assertEqual(launcher_help.returncode, 0, launcher_help.stderr.decode())
        self.assertIn(b"--triptych-status [RUN_ID]", launcher_help.stdout)
        self.assertIn(b"--triptych-reopen RUN_ID", launcher_help.stdout)
        self.assertIn(b"--triptych-final-diff RUN_ID", launcher_help.stdout)
        self.assertIn(b"--triptych-clean RUN_ID", launcher_help.stdout)
        make_help = self.run_make(["help"])
        self.assertEqual(make_help.returncode, 0, make_help.stderr.decode())
        self.assertIn(b"make status [RUN=<run-id>]", make_help.stdout)
        self.assertIn(b"make reopen RUN=<run-id>", make_help.stdout)
        self.assertIn(b"make final-diff RUN=<run-id>", make_help.stdout)
        self.assertIn(b"make clean-run RUN=<run-id>", make_help.stdout)

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
        first_temporary = Path(first_manifest["tmpdir"])
        second_temporary = Path(second_manifest["tmpdir"])
        (first_temporary / "first-only.txt").write_text("first\n", encoding="utf-8")
        (second_temporary / "second-only.txt").write_text("second\n", encoding="utf-8")

        integrate_first = self.run_launcher(
            ["--triptych-integrate", first_manifest["run_id"]]
        )
        self.assertEqual(integrate_first.returncode, 0, integrate_first.stderr.decode())
        first_landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertFalse(first_temporary.exists())
        self.assertEqual(
            (second_temporary / "second-only.txt").read_text(encoding="utf-8"),
            "second\n",
        )

        integrate_second = self.run_launcher(
            ["--triptych-integrate", second_manifest["run_id"]]
        )
        self.assertEqual(integrate_second.returncode, 0, integrate_second.stderr.decode())
        self.assertFalse(second_temporary.exists())
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
        self.git(
            self.control,
            "update-ref",
            self.source_anchor_ref(manifest["run_id"]),
            source_head,
        )
        recovery_note = worker / "recovery-note.txt"
        recovery_note.write_text("do not discard\n", encoding="utf-8")

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"unprovable", integrate.stderr)
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
        self.git(
            self.control,
            "update-ref",
            self.source_anchor_ref(manifest["run_id"]),
            source_head,
        )

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 2)
        self.assertIn(b"unprovable", integrate.stderr)
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
        self.assertIn(b"unprovable", integrate.stderr)
        self.assertTrue(rebase_marker.exists())
        self.assertEqual(self.git(worker, "status", "--porcelain=v1").stdout, status_before)
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "manual resolution\n",
        )
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-recovery-failed")
        self.assertIn("cannot adopt", recovered["integration_recovery_error"])

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
        self.assertIn(b"unprovable", integrate.stderr)
        self.assertTrue(marker.exists())
        self.assertEqual(self.git(worker, "rev-parse", "HEAD").stdout.strip(), source_head)
        recovered = self.manifests()[0]
        self.assertEqual(recovered["state"], "integration-rebase-recovery-failed")
        self.assertIn("cannot adopt", recovered["integration_recovery_error"])

    def test_integrate_disables_post_merge_hook_during_ordinary_landing(self) -> None:
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
            f'#!/bin/sh\nprintf "%s\\n" "hook result" > "{late_file}"\nexit 97\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

        integrate = self.run_launcher(["--triptych-integrate", manifest["run_id"]])
        self.assertEqual(integrate.returncode, 0, integrate.stderr.decode())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, manifest["final_head"])
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD^").stdout.strip(), advanced_head)
        integrated = self.manifests()[0]
        self.assertEqual(integrated["state"], "cleaned")
        self.assertEqual(integrated["final_head"], manifest["final_head"])
        self.assertEqual(integrated["integrated_head"], landed_head)
        self.assertEqual(integrated["integration_candidate_head"], landed_head)
        self.assertFalse(late_file.exists())
        self.assertFalse(worker.exists())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])

    def test_ordinary_post_cas_descendant_is_adopted_and_cleaned(self) -> None:
        manifest, worker, source_head, target_head = self.prepare_successful_rebase()
        marker = self.root / "ordinary-post-cas-kill"

        crashed = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
            ),
        )

        self.assertLess(crashed.returncode, 0)
        self.assertTrue(marker.exists())
        candidate = self.git(
            self.control,
            "rev-parse",
            "refs/heads/main",
        ).stdout.strip()
        self.assertNotEqual(candidate, source_head)
        self.assertEqual(self.git(worker, "rev-parse", "HEAD^").stdout.strip(), target_head)
        self.assertTrue(worker.exists())
        pending = self.manifests()[0]
        self.assertEqual(pending["state"], "integration-merge-pending")
        self.assertEqual(pending["integration_candidate_head"], candidate)
        self.assertNotIn("integrated_head", pending)

        self.git(self.control, "reset", "--hard", candidate)
        (self.control / "post-cas-descendant.txt").write_text(
            "ordinary descendant\n",
            encoding="utf-8",
        )
        self.git(self.control, "add", "post-cas-descendant.txt")
        self.git(self.control, "commit", "-m", "Advance after ordinary target CAS")
        descendant = self.git(self.control, "rev-parse", "HEAD").stdout.strip()

        retry = self.run_launcher(["--triptych-integrate", manifest["run_id"]])

        self.assertEqual(retry.returncode, 0, retry.stderr.decode())
        self.assertEqual(self.git(self.control, "rev-parse", "HEAD").stdout.strip(), descendant)
        self.assertEqual(
            self.git(self.control, "merge-base", "--is-ancestor", candidate, descendant).returncode,
            0,
        )
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integrated_head"], candidate)
        self.assertFalse(worker.exists())

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
        marker = self.root / "post-landing-worker-dirt"

        integrate = self.run_launcher(
            ["--triptych-integrate", manifest["run_id"]],
            environment=self.post_git_action_environment(
                cwd=self.control,
                tokens=["update-ref", "--no-deref", "refs/heads/main"],
                marker=marker,
                action="dirty",
                dirty_path=late_file,
            ),
        )
        self.assertEqual(integrate.returncode, 2)
        self.assertTrue(marker.exists())
        landed_head = self.git(self.control, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(landed_head, manifest["final_head"])
        self.assertEqual(self.manifests()[0]["integrated_head"], landed_head)
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
        pending_status = self.run_launcher(["--triptych-status"])
        self.assertEqual(pending_status.returncode, 0, pending_status.stderr.decode())
        self.assertIn(os.fsencode(manifest["run_id"]), pending_status.stdout)
        self.assertIn(b"cleaned-branch-retained", pending_status.stdout)

        self.git(self.control, "worktree", "remove", str(competing))
        clean = self.run_launcher(["--triptych-clean", manifest["run_id"]])
        self.assertEqual(clean.returncode, 0, clean.stderr.decode())
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertEqual(self.worker_branches(), [])
        cleaned_manifest = self.manifests()[0]
        self.assertEqual(cleaned_manifest["state"], "cleaned")
        self.assertIn("branch_cleaned_at", cleaned_manifest)
        cleaned_status = self.run_launcher(["--triptych-status"])
        self.assertEqual(cleaned_status.returncode, 0, cleaned_status.stderr.decode())
        self.assertEqual(cleaned_status.stdout, b"No Triptych Codex runs.\n")

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
            stdout, stderr = process.communicate(timeout=COMMAND_TIMEOUT_SECONDS)
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

    def test_status_overview_omits_cleaned_runs_but_exact_lookup_keeps_them(self) -> None:
        cleaned_result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(self.root / "status-cleaned.jsonl")}
        )
        self.assertEqual(cleaned_result.returncode, 0, cleaned_result.stderr.decode())
        cleaned = self.manifests()[0]
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertFalse(Path(cleaned["worktree"]).exists())

        empty_overview = self.run_launcher(["--triptych-status"])
        self.assertEqual(empty_overview.returncode, 0, empty_overview.stderr.decode())
        self.assertEqual(empty_overview.stdout, b"No Triptych Codex runs.\n")

        exact = self.run_launcher(["--triptych-status", cleaned["run_id"]])
        self.assertEqual(exact.returncode, 0, exact.stderr.decode())
        self.assertIn(os.fsencode(cleaned["run_id"]), exact.stdout)
        self.assertIn(b"cleaned", exact.stdout)

        preserved_result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(self.root / "status-preserved.jsonl"),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(
            preserved_result.returncode,
            0,
            preserved_result.stderr.decode(),
        )
        preserved_runs = [
            manifest
            for manifest in self.manifests()
            if manifest["state"] == "preserved"
        ]
        self.assertEqual(len(preserved_runs), 1)
        preserved = preserved_runs[0]

        overview = self.run_launcher(["--triptych-status"])
        self.assertEqual(overview.returncode, 0, overview.stderr.decode())
        self.assertNotIn(os.fsencode(cleaned["run_id"]), overview.stdout)
        self.assertIn(os.fsencode(preserved["run_id"]), overview.stdout)
        self.assertIn(b"preserved", overview.stdout)

    def test_status_overview_validates_cleaned_records_before_omitting_them(self) -> None:
        result = self.run_launcher(
            environment={"FAKE_CODEX_LOG": str(self.root / "status-cleaned-tamper.jsonl")}
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        manifest = self.manifests()[0]
        self.assertEqual(manifest["state"], "cleaned")
        manifest["worktree"] = str(self.control)
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        status = self.run_launcher(["--triptych-status"])

        self.assertEqual(status.returncode, 2)
        self.assertIn(b"unsafe worktree path", status.stderr)

    def test_status_rejects_a_tampered_state_without_printing_private_paths(self) -> None:
        log = self.root / "status-tampered-state.jsonl"
        result = self.run_launcher(
            environment={
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_ACTION": "dirty",
            }
        )
        self.assertEqual(result.returncode, 0)
        manifest = self.manifests()[0]
        manifest["state"] = f"preserved\n{manifest['worktree']}"
        manifest_file = self.repo_state() / "runs" / f"{manifest['run_id']}.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        status = self.run_launcher(["--triptych-status", manifest["run_id"]])

        self.assertEqual(status.returncode, 2)
        self.assertIn(b"invalid lifecycle state", status.stderr)
        self.assertNotIn(os.fsencode(manifest["worktree"]), status.stdout)
        self.assertNotIn(os.fsencode(manifest["worktree"]), status.stderr)


if __name__ == "__main__":
    unittest.main()
