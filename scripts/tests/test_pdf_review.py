from __future__ import annotations

import fcntl
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/pdf-review"


def load_review_module():
    loader = importlib.machinery.SourceFileLoader("triptych_pdf_review", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


review = load_review_module()


FAKE_TOOL = r"""
#!/usr/bin/env python3
import fcntl
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time

counter_path = Path(os.environ["PDF_REVIEW_TEST_COUNTER"])
log_path = Path(os.environ["PDF_REVIEW_TEST_LOG"])

def update_counter(delta):
    counter_path.parent.mkdir(parents=True, exist_ok=True)
    with counter_path.open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        stream.seek(0)
        text = stream.read()
        state = json.loads(text) if text else {"current": 0, "maximum": 0}
        state["current"] += delta
        state["maximum"] = max(state["maximum"], state["current"])
        stream.seek(0)
        stream.truncate()
        json.dump(state, stream)
        stream.flush()
        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

def log_record(record):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        stream.write(json.dumps(record) + "\n")
        stream.flush()
        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

def terminate(_signum, _frame):
    time.sleep(float(os.environ.get("PDF_REVIEW_TEST_TERM_DELAY", "0")))
    raise SystemExit(143)

previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM})
signal.signal(signal.SIGTERM, terminate)
update_counter(1)
try:
    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
    mode = Path(sys.argv[0]).name
    args = sys.argv[1:]
    log_record(
        {
            "mode": mode,
            "args": args,
            "address_space": resource.getrlimit(resource.RLIMIT_AS),
            "limits": {
                name: os.environ.get(name)
                for name in (
                    "MAGICK_MEMORY_LIMIT",
                    "MAGICK_MAP_LIMIT",
                    "MAGICK_DISK_LIMIT",
                    "MAGICK_AREA_LIMIT",
                    "MAGICK_THREAD_LIMIT",
                    "OMP_NUM_THREADS",
                )
            },
        }
    )
    if mode == "fake-pdftoppm":
        source = Path(args[-2])
        prefix = Path(args[-1])
        peer_marker = Path(os.environ["PDF_REVIEW_TEST_PEER_MARKER"])
        if "fail" in source.name:
            deadline = time.monotonic() + 5
            while not peer_marker.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            sys.stderr.write("x" * 200000 + "diagnostic-tail-marker\n")
            log_record({"mode": "failure-ready"})
            raise SystemExit(7)
        peer_marker.write_bytes(b"ready")
        time.sleep(float(os.environ.get("PDF_REVIEW_TEST_DELAY", "0.02")))
        prefix.parent.mkdir(parents=True, exist_ok=True)
        for page in range(1, int(os.environ.get("PDF_REVIEW_TEST_PAGES", "3")) + 1):
            prefix.with_name(f"{prefix.name}-{page}.png").write_bytes(b"png")
    elif mode == "fake-magick":
        time.sleep(float(os.environ.get("PDF_REVIEW_TEST_DELAY", "0.02")))
        output = Path(args[-1])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"png")
    else:
        raise SystemExit(9)
finally:
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM})
    update_counter(-1)
    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
"""


PLAN_HARNESS = r"""
#!/usr/bin/env python3
import importlib.machinery
import importlib.util
from pathlib import Path
import sys

script = Path(sys.argv[1])
sys.argv = [sys.argv[0], *sys.argv[2:]]
loader = importlib.machinery.SourceFileLoader("triptych_pdf_review_harness", str(script))
spec = importlib.util.spec_from_loader(loader.name, loader)
assert spec is not None
module = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = module
loader.exec_module(module)
module.current_plan = lambda override=None: module.make_plan(
    8 * module.GIB, None, 4, override
)
raise SystemExit(module.main())
"""


class ResourcePlanningTests(unittest.TestCase):
    def test_cgroup_location_accounts_for_a_non_root_mount(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            mount = root / "cgroup"
            mount.mkdir()
            cgroup_file = root / "self.cgroup"
            cgroup_file.write_text("0::/containers/example/session.scope\n", encoding="utf-8")
            mountinfo_file = root / "mountinfo"
            mountinfo_file.write_text(
                f"1 0 0:1 /containers/example {mount} rw - cgroup2 cgroup2 rw\n",
                encoding="utf-8",
            )
            self.assertEqual(
                review.cgroup2_location(cgroup_file, mountinfo_file),
                (mount, mount / "session.scope"),
            )
            self.assertTrue(review.unified_cgroup_member(cgroup_file))

    def test_memory_and_cpu_choose_the_strictest_bound(self) -> None:
        plan = review.make_plan(8 * review.GIB, 3 * review.GIB, 14)
        self.assertEqual(plan.effective_available, 3 * review.GIB)
        self.assertEqual(plan.jobs, 2)

    def test_low_memory_fails_closed_and_unknown_uses_one_worker(self) -> None:
        with self.assertRaisesRegex(review.ReviewError, "insufficient memory"):
            review.make_plan(512 * review.MIB, None, 14)
        self.assertEqual(review.make_plan(None, None, 14).jobs, 1)

    def test_cpu_and_explicit_override_semantics(self) -> None:
        self.assertEqual(review.make_plan(16 * review.GIB, None, 2).jobs, 2)
        self.assertEqual(review.make_plan(16 * review.GIB, None, 8, override=2).jobs, 2)
        with self.assertRaisesRegex(review.ReviewError, "insufficient memory"):
            review.make_plan(512 * review.MIB, None, 2, override=5)

    def test_legacy_cgroup_controllers_are_detected_for_safe_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cgroup_file = Path(temporary) / "self.cgroup"
            cgroup_file.write_text(
                "5:cpu,cpuacct:/session\n4:memory:/session\n0::/session\n",
                encoding="utf-8",
            )
            self.assertEqual(
                review.legacy_cgroup_controllers(cgroup_file),
                {"cpu", "cpuacct", "memory"},
            )

    def test_unknown_legacy_limits_fail_closed(self) -> None:
        with (
            mock.patch.object(review, "cgroup2_location", return_value=None),
            mock.patch.object(review, "unified_cgroup_member", return_value=False),
            mock.patch.object(review, "legacy_cgroup_controllers", return_value={"memory"}),
            mock.patch.object(review, "parse_memavailable", return_value=8 * review.GIB),
            mock.patch.object(review, "available_cpus", return_value=8),
        ):
            with self.assertRaisesRegex(review.ReviewError, "insufficient memory"):
                review.current_plan()

    def test_unreadable_unified_limits_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary) / "cgroup"
            leaf = mount / "session.scope"
            leaf.mkdir(parents=True)
            with (
                mock.patch.object(review, "cgroup2_location", return_value=(mount, leaf)),
                mock.patch.object(review, "parse_memavailable", return_value=8 * review.GIB),
                mock.patch.object(review, "available_cpus", return_value=8),
            ):
                with self.assertRaisesRegex(review.ReviewError, "insufficient memory"):
                    review.current_plan()

    def test_mount_root_may_omit_resource_control_interfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary) / "cgroup"
            leaf = mount / "session.scope"
            leaf.mkdir(parents=True)
            (leaf / "memory.current").write_text("1024", encoding="utf-8")
            (leaf / "memory.max").write_text("max", encoding="utf-8")
            (leaf / "memory.high").write_text("max", encoding="utf-8")
            (leaf / "cpu.max").write_text("max 100000", encoding="utf-8")
            self.assertEqual(review.cgroup_memory_probe(mount, leaf), (None, True))
            self.assertEqual(review.cgroup_cpu_probe(mount, leaf), (None, True))

    def test_missing_non_root_ancestor_is_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary) / "cgroup"
            leaf = mount / "parent/session.scope"
            leaf.mkdir(parents=True)
            (leaf / "memory.current").write_text("1024", encoding="utf-8")
            (leaf / "memory.max").write_text("max", encoding="utf-8")
            (leaf / "memory.high").write_text("max", encoding="utf-8")
            (leaf / "cpu.max").write_text("max 100000", encoding="utf-8")
            self.assertEqual(review.cgroup_memory_probe(mount, leaf), (None, False))
            self.assertEqual(review.cgroup_cpu_probe(mount, leaf), (None, False))

    def test_limited_child_preserves_a_lower_inherited_soft_limit(self) -> None:
        inherited_limit = 256 * review.MIB
        bootstrap = """
import os
import resource
import sys

resource.setrlimit(resource.RLIMIT_AS, (int(sys.argv[2]), resource.RLIM_INFINITY))
os.execv(
    sys.executable,
    [
        sys.executable,
        sys.argv[1],
        "--_limit-child",
        str(1024 * 1024 * 1024),
        "--",
        sys.executable,
        "-c",
        "import resource; print(resource.getrlimit(resource.RLIMIT_AS)[0])",
    ],
)
"""
        result = subprocess.run(
            [sys.executable, "-c", bootstrap, str(SCRIPT), str(inherited_limit)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(int(result.stdout.strip()), inherited_limit)

    def test_cgroup_ancestor_memory_and_cpu_limits(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            mount = Path(temporary) / "cgroup"
            leaf = mount / "user.slice/session.scope"
            leaf.mkdir(parents=True)
            (mount / "memory.max").write_text(str(10 * review.GIB), encoding="utf-8")
            (mount / "memory.high").write_text("max", encoding="utf-8")
            (mount / "memory.current").write_text(str(4 * review.GIB), encoding="utf-8")
            (mount / "cpu.max").write_text("400000 100000", encoding="utf-8")
            parent = leaf.parent
            (parent / "memory.max").write_text(str(6 * review.GIB), encoding="utf-8")
            (parent / "memory.high").write_text("max", encoding="utf-8")
            (parent / "memory.current").write_text(str(3 * review.GIB), encoding="utf-8")
            (parent / "cpu.max").write_text("300000 100000", encoding="utf-8")
            (leaf / "memory.max").write_text("max", encoding="utf-8")
            (leaf / "memory.high").write_text(str(4 * review.GIB), encoding="utf-8")
            (leaf / "memory.current").write_text(str(3 * review.GIB), encoding="utf-8")
            (leaf / "cpu.max").write_text("150000 100000", encoding="utf-8")
            self.assertEqual(review.cgroup_memory_headroom(mount, leaf), review.GIB)
            self.assertEqual(review.cgroup_cpu_quota(mount, leaf), 2)


class PdfReviewCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="triptych-pdf-review-test-", dir="/tmp"
        )
        self.root = Path(self.temporary.name)
        self.counter = self.root / "counter.json"
        self.log = self.root / "commands.jsonl"
        self.output = self.root / "output"
        self.fake_pdftoppm = self.root / "fake-pdftoppm"
        self.fake_magick = self.root / "fake-magick"
        self.plan_harness = self.root / "plan-harness"
        source = textwrap.dedent(FAKE_TOOL).lstrip()
        for executable in (self.fake_pdftoppm, self.fake_magick):
            executable.write_text(source, encoding="utf-8")
            executable.chmod(0o755)
        self.plan_harness.write_text(
            textwrap.dedent(PLAN_HARNESS).lstrip(), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def environment(
        self,
        *,
        pages: int = 3,
        delay: float = 0.02,
        term_delay: float = 0,
    ) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "TRIPTYCH_PDF_REVIEW_PDFTOPPM": str(self.fake_pdftoppm),
                "TRIPTYCH_PDF_REVIEW_MAGICK": str(self.fake_magick),
                "PDF_REVIEW_TEST_COUNTER": str(self.counter),
                "PDF_REVIEW_TEST_LOG": str(self.log),
                "PDF_REVIEW_TEST_PAGES": str(pages),
                "PDF_REVIEW_TEST_DELAY": str(delay),
                "PDF_REVIEW_TEST_TERM_DELAY": str(term_delay),
                "PDF_REVIEW_TEST_PEER_MARKER": str(self.root / "peer-started"),
            }
        )
        return environment

    def pdfs(self, names: list[str]) -> list[Path]:
        result = []
        for name in names:
            path = self.root / name
            path.write_bytes(b"pdf")
            result.append(path)
        return result

    def invoke(
        self,
        pdfs: list[Path],
        *,
        jobs: int = 2,
        pages: int = 3,
        delay: float = 0.02,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                str(jobs),
                "--output",
                str(self.output),
                *(str(path) for path in pdfs),
            ],
            cwd=ROOT,
            env=self.environment(pages=pages, delay=delay),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )

    def records(self) -> list[dict]:
        with self.log.open(encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_SH)
            try:
                return [json.loads(line) for line in stream.read().splitlines()]
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def counter_state(self) -> dict[str, int]:
        with self.counter.open(encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_SH)
            try:
                return json.loads(stream.read())
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def test_worker_pool_never_exceeds_selected_jobs(self) -> None:
        result = self.invoke(
            self.pdfs([f"document-{number}.pdf" for number in range(5)]),
            jobs=2,
            delay=0.2,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        state = self.counter_state()
        self.assertEqual(state["current"], 0)
        self.assertEqual(state["maximum"], 2)
        self.assertEqual(len(list(self.output.rglob("pages/page-1.png"))), 5)
        for record in self.records():
            self.assertEqual(
                record["address_space"],
                [review.CHILD_ADDRESS_SPACE_BYTES, review.CHILD_ADDRESS_SPACE_BYTES],
            )

    def test_contact_sheets_are_batched_and_magick_is_hard_limited(self) -> None:
        result = self.invoke(self.pdfs(["large.pdf"]), jobs=1, pages=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        magick_records = [record for record in self.records() if record["mode"] == "fake-magick"]
        self.assertEqual(len(magick_records), 3)
        for record in magick_records:
            args = record["args"]
            self.assertIn("montage", args)
            self.assertLessEqual(args.count("-label"), review.CONTACT_BATCH_SIZE)
            for resource, value in (
                ("memory", review.MAGICK_MEMORY),
                ("map", review.MAGICK_MAP),
                ("disk", review.MAGICK_DISK),
                ("area", review.MAGICK_AREA),
                ("thread", "1"),
            ):
                index = args.index(resource)
                self.assertEqual(args[index - 1], "-limit")
                self.assertEqual(args[index + 1], value)
            self.assertEqual(record["limits"]["MAGICK_MEMORY_LIMIT"], review.MAGICK_MEMORY)
            self.assertEqual(record["limits"]["MAGICK_MAP_LIMIT"], review.MAGICK_MAP)
            self.assertEqual(record["limits"]["MAGICK_DISK_LIMIT"], review.MAGICK_DISK)
            self.assertEqual(record["limits"]["MAGICK_AREA_LIMIT"], review.MAGICK_AREA)
            self.assertEqual(record["limits"]["MAGICK_THREAD_LIMIT"], "1")
            self.assertEqual(record["limits"]["OMP_NUM_THREADS"], "1")
        self.assertEqual(len(list(self.output.rglob("contact-sheets/sheet-*.png"))), 3)

    def test_competing_invocations_are_serialized_by_the_shared_lock(self) -> None:
        first, second = self.pdfs(["first.pdf", "second.pdf"])
        environment = self.environment(pages=1, delay=0.15)
        commands = [
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                "1",
                "--output",
                str(self.root / output_name),
                str(pdf),
            ]
            for output_name, pdf in (("first-output", first), ("second-output", second))
        ]
        processes = [
            subprocess.Popen(
                command,
                cwd=ROOT,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for command in commands
        ]
        results = [process.communicate(timeout=20) for process in processes]
        for process, (_stdout, stderr) in zip(processes, results, strict=True):
            self.assertEqual(process.returncode, 0, stderr)
        state = self.counter_state()
        self.assertEqual(state["current"], 0)
        self.assertEqual(state["maximum"], 1)

    def test_child_failure_terminates_other_workers_and_leaves_no_processes(self) -> None:
        result = self.invoke(
            self.pdfs(["slow-one.pdf", "fail.pdf", "slow-two.pdf"]),
            jobs=3,
            delay=1.0,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("command failed", result.stderr)
        self.assertIn("diagnostic-tail-marker", result.stderr)
        self.assertLess(len(result.stderr.encode()), review.DIAGNOSTIC_TAIL_BYTES + 2048)
        self.assertEqual(self.counter_state()["current"], 0)
        self.assertFalse(any(self.output.rglob(".tmp-*")))

    def test_signals_cannot_interrupt_failure_cleanup(self) -> None:
        pdfs = self.pdfs(["slow-one.pdf", "fail.pdf", "slow-two.pdf"])
        process = subprocess.Popen(
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                "3",
                "--output",
                str(self.output),
                *(str(pdf) for pdf in pdfs),
            ],
            cwd=ROOT,
            env=self.environment(pages=1, delay=5.0, term_delay=0.5),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                records = self.records()
            except FileNotFoundError:
                records = []
            if any(record["mode"] == "failure-ready" for record in records):
                break
            time.sleep(0.02)
        else:
            process.kill()
            process.communicate(timeout=10)
            self.fail("parallel failure scenario did not start")
        time.sleep(0.1)
        for repeated_signal in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
            try:
                process.send_signal(repeated_signal)
            except ProcessLookupError:
                break
        _stdout, stderr = process.communicate(timeout=20)
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn("command failed", stderr)
        self.assertEqual(self.counter_state()["current"], 0)
        self.assertFalse(any(self.output.rglob(".tmp-*")))

    def test_repeated_signals_do_not_interrupt_child_cleanup(self) -> None:
        pdf = self.pdfs(["slow.pdf"])[0]
        process = subprocess.Popen(
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                "1",
                "--output",
                str(self.output),
                str(pdf),
            ],
            cwd=ROOT,
            env=self.environment(pages=1, delay=5.0, term_delay=0.5),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                if self.counter_state().get("current", 0) > 0:
                    break
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            time.sleep(0.02)
        else:
            process.kill()
            process.communicate(timeout=10)
            self.fail("bounded child did not start")
        process.send_signal(signal.SIGTERM)
        time.sleep(0.05)
        for repeated_signal in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
            try:
                process.send_signal(repeated_signal)
            except ProcessLookupError:
                break
        _stdout, stderr = process.communicate(timeout=20)
        self.assertEqual(process.returncode, 128 + signal.SIGTERM, stderr)
        self.assertIn("terminated by SIGTERM", stderr)
        self.assertEqual(self.counter_state()["current"], 0)
        self.assertFalse(any(self.output.rglob(".tmp-*")))

    def test_invalid_job_override_is_rejected(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--jobs", "0", "--explain"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("positive integer", result.stderr)


if __name__ == "__main__":
    unittest.main()
