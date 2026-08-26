"""Regression tests for create-or-replay workflow seeding."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import PASS, WorkflowError  # noqa: E402
from test_workflow_adversarial import engine_for, make_repo  # noqa: E402


def snapshot_tree(root: Path) -> dict[str, bytes]:
    """Return every regular file below root by relative path and raw bytes."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class SeedIdempotencyTests(unittest.TestCase):
    """The engine preserves and verifies one immutable bootstrap."""

    def setUp(self) -> None:
        self.repo = make_repo()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.engine = engine_for(self.repo)
        self.args = {"doc": "d1", "provider": "gpt"}

    def seed_bytes(self) -> bytes:
        return self.engine.seed_bytes("adv-wf", self.args)

    def test_repeated_seed_replays_bytes_without_any_run_write(self):
        first = self.seed_bytes()
        response = json.loads(first)
        run_dir = self.engine.run_dir(response["run_id"])
        before = snapshot_tree(run_dir)

        mutations = (
            "_acquire_seed_lock", "_create_seed_bytes", "_write_new_file",
            "_commit", "save_state", "_emit_event",
        )
        patches = [
            mock.patch.object(
                self.engine, name,
                side_effect=AssertionError(f"repeat seed called {name}"),
            )
            for name in mutations
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        second = self.seed_bytes()

        self.assertEqual(first, second)
        self.assertEqual(second, (run_dir / "bootstrap.json").read_bytes())
        self.assertEqual(before, snapshot_tree(run_dir))
        self.assertEqual(second[-1:], b"\n")
        self.assertNotEqual(second[-2:], b"\n\n")
        self.assertEqual(set(response), {
            "bootstrap_version", "instructions", "iteration",
            "normalized_args", "packet_hash", "packet_path", "repo_commit",
            "run_id", "stage", "workflow_digest", "workflow_id",
            "workflow_version",
        })
        self.assertEqual(response["bootstrap_version"], 1)
        self.assertEqual(response["workflow_id"], "adv-wf")
        self.assertEqual(response["workflow_version"], 1)
        self.assertEqual(len(response["workflow_digest"]), 64)
        self.assertEqual(response["stage"], "stage-a")
        self.assertEqual(response["iteration"], 0)
        self.assertEqual(len(response["packet_hash"]), 64)
        self.assertFalse(Path(response["packet_path"]).is_absolute())
        self.assertNotIn(str(self.repo).encode(), first)
        self.assertNotIn(str(self.repo), response["instructions"])
        self.assertIn(response["packet_path"], response["instructions"])
        self.assertIn(
            f"4. Run: tools/tpt adv-wf d1 advance {response['run_id']} "
            f"--result <path>",
            response["instructions"],
        )
        packet = self.repo / response["packet_path"]
        self.assertEqual(
            hashlib.sha256(packet.read_bytes()).hexdigest(),
            response["packet_hash"],
        )
        events = (run_dir / "events.jsonl").read_text().splitlines()
        self.assertEqual(len(events), 2)
        self.assertEqual(len(list((run_dir / "packets").iterdir())), 1)
        self.assertEqual(len(list((run_dir / "results").iterdir())), 0)
        self.assertEqual(
            [path.name for path in self.engine.runs_dir.iterdir()],
            [response["run_id"]],
        )

    def test_seed_after_progress_still_replays_original_bootstrap(self):
        first = self.seed_bytes()
        run_id = json.loads(first)["run_id"]
        result = self.repo / "result.json"
        result.write_text(json.dumps({
            "stage": "stage-a", "iteration": 0,
            "disposition": PASS, "summary": "done",
        }), encoding="utf-8")
        advanced = self.engine.advance(run_id, result_path=str(result))
        self.assertEqual(advanced["stage"], "stage-b")
        run_dir = self.engine.run_dir(run_id)
        before = snapshot_tree(run_dir)

        later = self.seed_bytes()

        self.assertEqual(first, later)
        self.assertEqual(before, snapshot_tree(run_dir))
        status = self.engine.status(run_id)
        self.assertEqual(status["current_stage"], "stage-b")
        self.assertEqual(status["results_received"], 1)
        self.assertEqual(status["packets_emitted"], 2)
        self.assertEqual(len(status["transitions"]), 1)
        replay = self.engine.replay(run_id)
        self.assertEqual(replay["stage"], "stage-b")
        self.assertTrue(replay["deterministic"])

    def test_terminal_run_still_replays_original_bootstrap(self):
        first = self.seed_bytes()
        run_id = json.loads(first)["run_id"]

        def advance_result(name: str, evaluator: bool = False) -> None:
            packet = self.engine.load_state(run_id)["packet_hashes"][-1]
            body = {
                "stage": packet["stage"],
                "iteration": packet["iteration"],
                "disposition": PASS,
            }
            if evaluator:
                body["findings"] = []
            else:
                body["summary"] = "done"
            path = self.repo / f"{name}.json"
            path.write_text(json.dumps(body), encoding="utf-8")
            self.engine.advance(run_id, result_path=str(path))

        advance_result("a")
        advance_result("b")
        advance_result("evaluate", evaluator=True)
        self.engine.advance(run_id, run_gate=True)
        advance_result("visual", evaluator=True)
        accepted = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(accepted["disposition"], "ACCEPTED")
        run_dir = self.engine.run_dir(run_id)
        before = snapshot_tree(run_dir)

        self.assertEqual(self.seed_bytes(), first)
        self.assertEqual(snapshot_tree(run_dir), before)

    def test_source_mutation_fails_closed_without_run_changes(self):
        first = json.loads(self.seed_bytes())
        run_dir = self.engine.run_dir(first["run_id"])
        fragment = self.repo / "workflows/fragments/synthetic/work-a.md"
        fragment.write_text("# changed\n", encoding="utf-8")
        before = snapshot_tree(run_dir)

        with self.assertRaisesRegex(WorkflowError, "workflow source changed"):
            self.seed_bytes()

        self.assertEqual(before, snapshot_tree(run_dir))

    def test_corrupt_bootstrap_fails_closed_without_reconstruction(self):
        response = json.loads(self.seed_bytes())
        run_dir = self.engine.run_dir(response["run_id"])
        path = run_dir / "bootstrap.json"
        altered = json.loads(path.read_bytes())
        altered["instructions"] = "invented replacement"
        path.write_text(
            json.dumps(altered, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest_path = run_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["bootstrap"]["sha256"] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        before = snapshot_tree(run_dir)

        with self.assertRaisesRegex(WorkflowError, "canonical response"):
            self.seed_bytes()

        self.assertEqual(before, snapshot_tree(run_dir))

    def test_missing_legacy_bootstrap_fails_seed_but_not_other_commands(self):
        response = json.loads(self.seed_bytes())
        run_id = response["run_id"]
        run_dir = self.engine.run_dir(run_id)
        (run_dir / "bootstrap.json").unlink()
        manifest_path = run_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        del manifest["bootstrap"]
        manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        self.assertEqual(self.engine.status(run_id)["current_stage"], "stage-a")
        self.assertTrue(self.engine.replay(run_id)["deterministic"])
        with self.assertRaisesRegex(WorkflowError, "predates replayable"):
            self.seed_bytes()
        result = self.repo / "legacy-result.json"
        result.write_text(json.dumps({
            "stage": "stage-a", "iteration": 0,
            "disposition": PASS, "summary": "continue old run",
        }), encoding="utf-8")
        self.assertEqual(
            self.engine.advance(run_id, result_path=str(result))["stage"],
            "stage-b",
        )

    def test_initial_packet_tamper_fails_closed(self):
        response = json.loads(self.seed_bytes())
        packet = self.repo / response["packet_path"]
        packet.write_bytes(packet.read_bytes() + b"tamper\n")
        with self.assertRaisesRegex(WorkflowError, "packet hash is inconsistent"):
            self.seed_bytes()

    def test_coordinated_initial_packet_tamper_fails_recompilation(self):
        response = json.loads(self.seed_bytes())
        run_dir = self.engine.run_dir(response["run_id"])
        packet = self.repo / response["packet_path"]
        packet.write_bytes(packet.read_bytes() + b"coordinated tamper\n")
        altered_hash = hashlib.sha256(packet.read_bytes()).hexdigest()
        state_path = run_dir / "state.json"
        state = json.loads(state_path.read_text())
        state["packet_hashes"][0]["hash"] = altered_hash
        state_path.write_text(
            json.dumps(state, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        bootstrap_path = run_dir / "bootstrap.json"
        bootstrap = json.loads(bootstrap_path.read_text())
        bootstrap["packet_hash"] = altered_hash
        bootstrap_path.write_text(
            json.dumps(bootstrap, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest_path = run_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["bootstrap"]["sha256"] = hashlib.sha256(
            bootstrap_path.read_bytes()
        ).hexdigest()
        manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        before = snapshot_tree(run_dir)

        with self.assertRaisesRegex(WorkflowError, "pristine seed state"):
            self.seed_bytes()

        self.assertEqual(before, snapshot_tree(run_dir))

    def test_semantically_corrupt_state_fails_closed(self):
        response = json.loads(self.seed_bytes())
        run_dir = self.engine.run_dir(response["run_id"])
        state_path = run_dir / "state.json"
        state = json.loads(state_path.read_text())
        state["current_stage"] = "not-a-stage"
        state_path.write_text(
            json.dumps(state, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        before = snapshot_tree(run_dir)

        with self.assertRaisesRegex(WorkflowError, "current stage disagrees"):
            self.seed_bytes()

        self.assertEqual(before, snapshot_tree(run_dir))

    def test_state_disposition_cannot_disagree_with_hashed_result(self):
        response = json.loads(self.seed_bytes())
        run_id = response["run_id"]
        result = self.repo / "result.json"
        result.write_text(json.dumps({
            "stage": "stage-a", "iteration": 0,
            "disposition": PASS, "summary": "done",
        }), encoding="utf-8")
        self.engine.advance(run_id, result_path=str(result))
        run_dir = self.engine.run_dir(run_id)
        state_path = run_dir / "state.json"
        state = json.loads(state_path.read_text())
        state["result_hashes"][0]["disposition"] = "CORRUPT"
        state["transitions"][0]["disposition"] = "CORRUPT"
        state_path.write_text(
            json.dumps(state, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        before = snapshot_tree(run_dir)

        with self.assertRaisesRegex(WorkflowError, "recorded JSON"):
            self.seed_bytes()

        self.assertEqual(before, snapshot_tree(run_dir))

    def test_non_object_state_is_a_controlled_workflow_error(self):
        response = json.loads(self.seed_bytes())
        state_path = self.engine.run_dir(response["run_id"]) / "state.json"
        state_path.write_text("[]\n", encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "expected a JSON object"):
            self.seed_bytes()

    def test_symlinked_state_and_manifest_are_rejected(self):
        for evidence in ("state.json", "manifest.json"):
            with self.subTest(evidence=evidence):
                response = json.loads(self.seed_bytes())
                run_dir = self.engine.run_dir(response["run_id"])
                path = run_dir / evidence
                external = self.repo / f"external-{evidence}"
                path.replace(external)
                path.symlink_to(external)
                before = external.read_bytes()
                with self.assertRaisesRegex(WorkflowError, "symlink"):
                    self.seed_bytes()
                self.assertEqual(before, external.read_bytes())
                shutil.rmtree(self.engine.runs_dir)

    def test_symlinked_packet_directory_is_rejected(self):
        response = json.loads(self.seed_bytes())
        run_dir = self.engine.run_dir(response["run_id"])
        packets = run_dir / "packets"
        external = self.repo / "external-packets"
        packets.replace(external)
        packets.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(WorkflowError, "directory is a symlink"):
            self.seed_bytes()

    def test_colliding_run_id_cannot_replay_different_arguments(self):
        first = json.loads(self.seed_bytes())
        with mock.patch.object(
            self.engine, "compute_run_id", return_value=first["run_id"]
        ):
            with self.assertRaisesRegex(WorkflowError, "normalized_args"):
                self.engine.seed_bytes(
                    "adv-wf", {"doc": "another", "provider": "gpt"}
                )

    def test_symlinked_run_directory_is_rejected(self):
        workflow = self.engine.load_workflow("adv-wf")
        commit = self.engine.get_repo_commit()
        run_id = self.engine.compute_run_id("adv-wf", 1, commit, self.args)
        sentinel = self.repo / "sentinel"
        sentinel.mkdir()
        self.engine.runs_dir.mkdir(parents=True)
        self.engine.run_dir(run_id).symlink_to(sentinel, target_is_directory=True)

        with self.assertRaisesRegex(WorkflowError, "symlink"):
            self.seed_bytes()

        self.assertEqual(list(sentinel.iterdir()), [])

    def test_failed_bootstrap_write_leaves_no_published_run(self):
        original = self.engine._write_new_file

        def fail_bootstrap(run_id: str, path: Path, payload: bytes) -> None:
            if path.name == "bootstrap.json":
                raise WorkflowError("injected bootstrap failure")
            original(run_id, path, payload)

        with mock.patch.object(
            self.engine, "_write_new_file", side_effect=fail_bootstrap
        ):
            with self.assertRaisesRegex(WorkflowError, "injected"):
                self.seed_bytes()
        self.assertEqual(list(self.engine.runs_dir.iterdir()), [])
        self.assertEqual(json.loads(self.seed_bytes())["stage"], "stage-a")


class SeedIdempotencyCliTests(unittest.TestCase):
    """The actual launcher emits the stored bootstrap bytes verbatim."""

    def setUp(self) -> None:
        self.repo = make_repo()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        (self.repo / "tools").mkdir()
        (self.repo / "scripts").mkdir()
        shutil.copy2(ROOT / "tools/tpt", self.repo / "tools/tpt")
        for name in ("_workflow.py", "_tooling.py"):
            shutil.copy2(ROOT / "scripts" / name, self.repo / "scripts" / name)
        (self.repo / "tmt.json").write_text(
            json.dumps({"tools": {}}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.launcher = self.repo / "tools/tpt"
        self.command = [
            str(self.launcher), "adv-wf", "d1", "seed",
            "--provider", "gpt",
        ]

    def run_seed(self) -> subprocess.CompletedProcess:
        return self.run_cli(*self.command[1:])

    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(self.launcher), *args], cwd=self.repo,
            capture_output=True, text=False,
            env={**os.environ, "PYTHONHASHSEED": "2718", "LC_ALL": "C"},
        )

    def test_raw_cli_bytes_and_whole_run_tree_are_idempotent(self):
        first = self.run_seed()
        self.assertEqual(first.returncode, 0, first.stderr)
        response = json.loads(first.stdout)
        run_dir = self.repo / "build/tpt-runs" / response["run_id"]
        before = snapshot_tree(run_dir)

        second = self.run_seed()

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, snapshot_tree(run_dir))
        self.assertEqual(
            hashlib.sha256(first.stdout).hexdigest(),
            hashlib.sha256(second.stdout).hexdigest(),
        )

    def test_cli_seed_after_progress_remains_the_original_bootstrap(self):
        first = self.run_seed()
        self.assertEqual(first.returncode, 0, first.stderr)
        response = json.loads(first.stdout)
        run_id = response["run_id"]
        result = self.repo / "result.json"
        result.write_text(json.dumps({
            "stage": "stage-a", "iteration": 0,
            "disposition": PASS, "summary": "done",
        }), encoding="utf-8")
        advanced = self.run_cli(
            "adv-wf", "d1", "advance", run_id,
            "--result", str(result),
        )
        self.assertEqual(advanced.returncode, 0, advanced.stderr)
        self.assertEqual(json.loads(advanced.stdout)["stage"], "stage-b")
        run_dir = self.repo / "build/tpt-runs" / run_id
        before = snapshot_tree(run_dir)

        later = self.run_seed()

        self.assertEqual(later.returncode, 0, later.stderr)
        self.assertEqual(first.stdout, later.stdout)
        self.assertEqual(before, snapshot_tree(run_dir))
        status = self.run_cli("adv-wf", "d1", "status", run_id)
        self.assertEqual(status.returncode, 0, status.stderr)
        status_body = json.loads(status.stdout)
        self.assertEqual(status_body["current_stage"], "stage-b")
        self.assertEqual(status_body["results_received"], 1)
        replay = self.run_cli("adv-wf", "d1", "replay", run_id)
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(json.loads(replay.stdout)["stage"], "stage-b")

    def test_cli_workflow_mutation_fails_closed_without_stdout_or_writes(self):
        first = self.run_seed()
        self.assertEqual(first.returncode, 0, first.stderr)
        run_id = json.loads(first.stdout)["run_id"]
        fragment = self.repo / "workflows/fragments/synthetic/work-a.md"
        fragment.write_text("# changed\n", encoding="utf-8")
        run_dir = self.repo / "build/tpt-runs" / run_id
        before = snapshot_tree(run_dir)

        repeated = self.run_seed()

        self.assertEqual(repeated.returncode, 2)
        self.assertEqual(repeated.stdout, b"")
        self.assertIn(b"workflow source changed", repeated.stderr)
        self.assertEqual(before, snapshot_tree(run_dir))

    def test_cli_corrupt_bootstrap_fails_closed_without_reconstruction(self):
        first = self.run_seed()
        self.assertEqual(first.returncode, 0, first.stderr)
        run_id = json.loads(first.stdout)["run_id"]
        run_dir = self.repo / "build/tpt-runs" / run_id
        bootstrap = run_dir / "bootstrap.json"
        altered = json.loads(bootstrap.read_bytes())
        altered["stage"] = "invented"
        bootstrap.write_text(
            json.dumps(altered, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        before = snapshot_tree(run_dir)

        repeated = self.run_seed()

        self.assertEqual(repeated.returncode, 2)
        self.assertEqual(repeated.stdout, b"")
        self.assertIn(b"manifest hash", repeated.stderr)
        self.assertEqual(before, snapshot_tree(run_dir))

    def test_concurrent_cli_seeds_converge_on_one_bootstrap(self):
        processes = [
            subprocess.Popen(
                self.command, cwd=self.repo,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            for _ in range(16)
        ]
        completed = [process.communicate(timeout=20) for process in processes]
        for process, (_, stderr) in zip(processes, completed):
            self.assertEqual(process.returncode, 0, stderr)
        outputs = [stdout for stdout, _ in completed]
        self.assertTrue(all(output == outputs[0] for output in outputs))
        response = json.loads(outputs[0])
        run_dir = self.repo / "build/tpt-runs" / response["run_id"]
        self.assertEqual(
            (run_dir / "events.jsonl").read_text().count("\n"), 2
        )
        self.assertEqual(len(list((run_dir / "packets").iterdir())), 1)
        self.assertEqual(
            [path.name for path in (self.repo / "build/tpt-runs").iterdir()],
            [response["run_id"]],
        )


if __name__ == "__main__":
    unittest.main()
