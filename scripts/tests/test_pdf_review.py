from __future__ import annotations

import fcntl
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import signal
import shutil
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
import hashlib
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
    record = {
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
    if mode == "fake-pdftoppm" and args != ["-v"]:
        record["source_sha256"] = hashlib.sha256(Path(args[-2]).read_bytes()).hexdigest()
    log_record(record)
    if (mode == "fake-pdftoppm" and args == ["-v"]) or (
        mode == "fake-magick" and args == ["-version"]
    ):
        print(f"{mode} {os.environ.get('PDF_REVIEW_TEST_TOOL_VERSION', '1.0')}")
    elif mode == "fake-pdftoppm":
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
    elif mode == "fake-magick" and args[0] == "mogrify":
        time.sleep(float(os.environ.get("PDF_REVIEW_TEST_DELAY", "0.02")))
        output = Path(args[args.index("-path") + 1])
        output.mkdir(parents=True, exist_ok=True)
        input_start = args.index("-thumbnail") + 2
        for source in args[input_start:]:
            source_path = Path(source)
            (output / source_path.name).write_bytes(b"thumbnail")
    elif mode == "fake-magick" and args[0] == "montage":
        time.sleep(float(os.environ.get("PDF_REVIEW_TEST_DELAY", "0.02")))
        if os.environ.get("PDF_REVIEW_TEST_MUTATE_FONT") == "1":
            Path(os.environ["PDF_REVIEW_TEST_FONT"]).write_bytes(b"raced font update")
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
import os
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
module.review_lock_path = lambda: Path(os.environ["PDF_REVIEW_TEST_LOCK"])
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


class ArtifactPathTests(unittest.TestCase):
    def test_managed_worker_accepts_only_a_tmpdir_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_id = "20260722t000000z-000000000000"
            managed_root = Path(temporary) / "tmp" / run_id
            managed_root.mkdir(parents=True)
            environment = {
                "TMPDIR": str(managed_root),
                "TMP": str(managed_root),
                "TEMP": str(managed_root),
                "TRIPTYCH_CODEX_ROLE": "worker",
                "TRIPTYCH_CODEX_RUN_ID": run_id,
            }
            with mock.patch.dict(os.environ, environment, clear=True):
                expected = managed_root / "review"
                self.assertEqual(review.validate_output_root(expected), expected.resolve())
                with self.assertRaisesRegex(review.ReviewError, "managed TMPDIR"):
                    review.validate_cache_root(managed_root)
                with self.assertRaisesRegex(review.ReviewError, "managed TMPDIR"):
                    review.validate_output_root(Path("/tmp/unmanaged-review-output"))

    def test_unmanaged_invocation_ignores_a_caller_selected_tmpdir(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {"TMPDIR": temporary},
            clear=True,
        ):
            with self.assertRaisesRegex(review.ReviewError, "/tmp"):
                review.validate_output_root(Path(temporary) / "review")
            output = Path("/tmp/triptych-pdf-review-unmanaged")
            self.assertEqual(review.validate_output_root(output), output.resolve())


class PdfReviewCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_root = ROOT / "build/test-tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(
            prefix="triptych-pdf-review-test-", dir=temporary_root
        )
        self.root = Path(self.temporary.name)
        self.counter = self.root / "counter.json"
        self.log = self.root / "commands.jsonl"
        self.output = self.root / "output"
        self.cache = self.root / "cache"
        self.fake_pdftoppm = self.root / "fake-pdftoppm"
        self.fake_magick = self.root / "fake-magick"
        self.fake_kpsewhich = self.root / "fake-kpsewhich"
        self.contact_font = self.root / review.CONTACT_FONT_FILENAME
        self.plan_harness = self.root / "plan-harness"
        source = textwrap.dedent(FAKE_TOOL).lstrip()
        for executable in (self.fake_pdftoppm, self.fake_magick):
            executable.write_text(source, encoding="utf-8")
            executable.chmod(0o755)
        self.contact_font.write_bytes(b"test Latin Modern Sans font")
        self.fake_kpsewhich.write_text(
            """#!/bin/sh
if [ "$1" != lmsans10-regular.otf ]; then
    exit 2
fi
printf '%s\\n' "$PDF_REVIEW_TEST_FONT"
""",
            encoding="utf-8",
        )
        self.fake_kpsewhich.chmod(0o755)
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
        tool_version: str = "1.0",
        mutate_font: bool = False,
        use_default_font: bool = False,
    ) -> dict[str, str]:
        environment = os.environ.copy()
        environment.pop("TRIPTYCH_PDF_REVIEW_FONT", None)
        environment.update(
            {
                "TRIPTYCH_PDF_REVIEW_PDFTOPPM": str(self.fake_pdftoppm),
                "TRIPTYCH_PDF_REVIEW_MAGICK": str(self.fake_magick),
                "TRIPTYCH_PDF_REVIEW_KPSEWHICH": str(self.fake_kpsewhich),
                "PDF_REVIEW_TEST_COUNTER": str(self.counter),
                "PDF_REVIEW_TEST_LOG": str(self.log),
                "PDF_REVIEW_TEST_PAGES": str(pages),
                "PDF_REVIEW_TEST_DELAY": str(delay),
                "PDF_REVIEW_TEST_TERM_DELAY": str(term_delay),
                "PDF_REVIEW_TEST_TOOL_VERSION": tool_version,
                "PDF_REVIEW_TEST_PEER_MARKER": str(self.root / "peer-started"),
                "PDF_REVIEW_TEST_LOCK": str(self.root / "review.lock"),
                "PDF_REVIEW_TEST_FONT": str(self.contact_font),
                "PDF_REVIEW_TEST_MUTATE_FONT": "1" if mutate_font else "0",
            }
        )
        if not use_default_font:
            environment["TRIPTYCH_PDF_REVIEW_FONT"] = str(self.contact_font)
        return environment

    def pdfs(self, names: list[str]) -> list[Path]:
        result = []
        for name in names:
            path = self.root / name
            path.write_bytes(f"pdf:{name}".encode())
            result.append(path)
        return result

    def invoke(
        self,
        pdfs: list[Path],
        *,
        jobs: int = 2,
        pages: int = 3,
        delay: float = 0.02,
        output: Path | None = None,
        cache: Path | None = None,
        extra: list[str] | None = None,
        tool_version: str = "1.0",
        mutate_font: bool = False,
        use_default_font: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        selected_output = self.output if output is None else output
        selected_cache = self.cache if cache is None else cache
        return subprocess.run(
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                str(jobs),
                "--output",
                str(selected_output),
                "--cache",
                str(selected_cache),
                *(extra or []),
                *(str(path) for path in pdfs),
            ],
            cwd=ROOT,
            env=self.environment(
                pages=pages,
                delay=delay,
                tool_version=tool_version,
                mutate_font=mutate_font,
                use_default_font=use_default_font,
            ),
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
        pdftoppm_records = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(pdftoppm_records), 5)
        for record in self.records():
            self.assertEqual(
                record["address_space"],
                [review.CHILD_ADDRESS_SPACE_BYTES, review.CHILD_ADDRESS_SPACE_BYTES],
            )

    def test_contact_sheets_are_batched_and_magick_is_hard_limited(self) -> None:
        result = self.invoke(self.pdfs(["large.pdf"]), jobs=1, pages=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        magick_records = [
            record
            for record in self.records()
            if record["mode"] == "fake-magick" and record["args"][:1] == ["montage"]
        ]
        self.assertEqual(len(magick_records), 3)
        for record in magick_records:
            args = record["args"]
            self.assertIn("montage", args)
            self.assertEqual(
                args[args.index("-font") + 1], str(self.contact_font.resolve())
            )
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

    def test_default_contact_font_is_resolved_with_kpsewhich(self) -> None:
        result = self.invoke(
            self.pdfs(["default-font.pdf"]), jobs=1, use_default_font=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        montage = next(
            record
            for record in self.records()
            if record["mode"] == "fake-magick" and record["args"][:1] == ["montage"]
        )
        self.assertEqual(
            montage["args"][montage["args"].index("-font") + 1],
            str(self.contact_font.resolve()),
        )

    def test_full_pages_are_rasterized_once_and_thumbnails_are_derived(self) -> None:
        result = self.invoke(self.pdfs(["single-pass.pdf"]), jobs=1, pages=7)
        self.assertEqual(result.returncode, 0, result.stderr)
        records = self.records()
        raster_commands = [
            record
            for record in records
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 1)
        self.assertEqual(
            raster_commands[0]["args"][raster_commands[0]["args"].index("-scale-to") + 1],
            str(review.FULL_PAGE_MAX_DIMENSION),
        )
        mogrify_commands = [
            record
            for record in records
            if record["mode"] == "fake-magick" and record["args"][:1] == ["mogrify"]
        ]
        self.assertEqual(len(mogrify_commands), 1)
        self.assertIn("-thumbnail", mogrify_commands[0]["args"])
        self.assertEqual(len(list(self.output.rglob("thumbnails/page-*.png"))), 7)

    def test_content_addressed_cache_avoids_rerendering_for_a_new_output(self) -> None:
        pdf = self.pdfs(["cached.pdf"])[0]
        first_output = self.root / "first-output"
        second_output = self.root / "second-output"
        first = self.invoke([pdf], jobs=1, output=first_output)
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.invoke([pdf], jobs=1, output=second_output)
        self.assertEqual(second.returncode, 0, second.stderr)
        raster_commands = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 1)
        self.assertTrue(any(second_output.rglob("pages/page-1.png")))
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 1)
        metadata = json.loads((entries[0] / review.METADATA_NAME).read_text())
        self.assertEqual(metadata["pdf_sha256"], review.sha256_file(pdf))
        self.assertIn("pdftoppm", metadata["renderer"]["tools"])
        self.assertEqual(
            metadata["renderer"]["raster"]["full_page_max_dimension"],
            review.FULL_PAGE_MAX_DIMENSION,
        )
        self.assertEqual(
            metadata["renderer"]["contact_sheets"]["geometry"],
            review.CONTACT_GEOMETRY,
        )
        self.assertEqual(
            metadata["renderer"]["contact_sheets"]["font"],
            {
                "path": str(self.contact_font.resolve()),
                "sha256": review.sha256_file(self.contact_font),
            },
        )
        shutil.rmtree(first_output)
        shutil.rmtree(second_output)
        shutil.rmtree(self.cache)
        self.assertFalse(first_output.exists())
        self.assertFalse(second_output.exists())
        self.assertFalse(self.cache.exists())

    def test_renderer_version_change_invalidates_the_cache(self) -> None:
        pdf = self.pdfs(["versioned.pdf"])[0]
        first = self.invoke([pdf], jobs=1, output=self.root / "version-one")
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.invoke(
            [pdf],
            jobs=1,
            output=self.root / "version-two",
            tool_version="2.0",
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        raster_commands = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 2)
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 2)

    def test_contact_font_change_invalidates_the_cache(self) -> None:
        pdf = self.pdfs(["font-versioned.pdf"])[0]
        first = self.invoke([pdf], jobs=1, output=self.root / "font-one")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.contact_font.write_bytes(b"revised Latin Modern Sans font")
        second = self.invoke([pdf], jobs=1, output=self.root / "font-two")
        self.assertEqual(second.returncode, 0, second.stderr)
        raster_commands = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 2)
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 2)

    def test_missing_contact_font_fails_before_rendering(self) -> None:
        pdf = self.pdfs(["missing-font.pdf"])[0]
        self.contact_font.unlink()
        result = self.invoke([pdf], jobs=1)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot resolve review contact-sheet font", result.stderr)
        self.assertFalse(self.log.exists())

    def test_contact_font_race_fails_without_caching_the_render(self) -> None:
        pdf = self.pdfs(["raced-font.pdf"])[0]
        result = self.invoke([pdf], jobs=1, mutate_font=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("font changed during rendering", result.stderr)
        self.assertFalse(any((self.cache / "objects").glob("*/*")))

    def test_same_size_cache_corruption_is_detected_and_rerendered(self) -> None:
        pdf = self.pdfs(["corruption.pdf"])[0]
        first = self.invoke([pdf], jobs=1, output=self.root / "before-corruption")
        self.assertEqual(first.returncode, 0, first.stderr)
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 1)
        cached_page = entries[0] / "pages/page-1.png"
        self.assertEqual(cached_page.read_bytes(), b"png")
        cached_page.chmod(0o644)
        cached_page.write_bytes(b"bad")
        cached_page.chmod(0o444)
        second = self.invoke([pdf], jobs=1, output=self.root / "after-corruption")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(cached_page.read_bytes(), b"png")
        raster_commands = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 2)

    def test_invalid_cache_cleanup_never_chmods_descendant_symlink_targets(self) -> None:
        pdf = self.pdfs(["symlink-cache.pdf"])[0]
        first = self.invoke([pdf], jobs=1, output=self.root / "before-symlinks")
        self.assertEqual(first.returncode, 0, first.stderr)
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 1)
        target_file = self.root / "symlink-target.txt"
        target_directory = self.root / "symlink-target-directory"
        target_file.write_bytes(b"outside-cache")
        target_directory.mkdir()
        target_file.chmod(0o600)
        target_directory.chmod(0o700)
        (entries[0] / "outside-file").symlink_to(target_file)
        (entries[0] / "outside-directory").symlink_to(
            target_directory, target_is_directory=True
        )

        second = self.invoke([pdf], jobs=1, output=self.root / "after-symlinks")

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(target_file.stat().st_mode & 0o777, 0o600)
        self.assertEqual(target_directory.stat().st_mode & 0o777, 0o700)
        self.assertEqual(target_file.read_bytes(), b"outside-cache")

    def test_changed_against_skips_identical_pdf_with_a_cold_cache(self) -> None:
        build_root = self.root / "build/gpt"
        installed_root = self.root / "doc/gpt"
        build_root.mkdir(parents=True)
        installed_root.mkdir(parents=True)
        same = build_root / "same.pdf"
        changed = build_root / "changed.pdf"
        same.write_bytes(b"same-pdf")
        changed.write_bytes(b"new-pdf")
        (installed_root / "same.pdf").write_bytes(b"same-pdf")
        (installed_root / "changed.pdf").write_bytes(b"old-pdf")
        result = self.invoke(
            [same, changed],
            jobs=1,
            extra=["--changed-against", str(installed_root)],
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skipped 1 byte-identical PDF", result.stderr)
        self.assertNotIn(str(same) + " ->", result.stdout)
        self.assertIn(str(changed) + " ->", result.stdout)
        raster_commands = [
            record
            for record in self.records()
            if record["mode"] == "fake-pdftoppm" and record["args"] != ["-v"]
        ]
        self.assertEqual(len(raster_commands), 1)

    def test_no_change_run_atomically_replaces_stale_output_with_empty_manifest(self) -> None:
        build_root = self.root / "build/gpt"
        installed_root = self.root / "doc/gpt"
        build_root.mkdir(parents=True)
        installed_root.mkdir(parents=True)
        source = build_root / "document.pdf"
        installed = installed_root / source.name
        source.write_bytes(b"new-pdf")
        installed.write_bytes(b"old-pdf")
        arguments = ["--changed-against", str(installed_root)]

        first = self.invoke([source], jobs=1, extra=arguments)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue(any(self.output.rglob("pages/page-1.png")))
        first_manifest = json.loads(
            (self.output / review.RUN_MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(len(first_manifest["pdfs"]), 1)

        installed.write_bytes(source.read_bytes())
        second = self.invoke([source], jobs=1, extra=arguments)

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("no changed PDFs selected", second.stderr)
        self.assertEqual(
            [path.name for path in self.output.iterdir()],
            [review.RUN_MANIFEST_NAME],
        )
        second_manifest = json.loads(
            (self.output / review.RUN_MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(second_manifest["schema"], review.RUN_MANIFEST_SCHEMA)
        self.assertEqual(second_manifest["pdfs"], [])
        self.assertIsNone(second_manifest["renderer_fingerprint"])
        self.assertFalse(
            any(self.output.parent.glob(f".{self.output.name}.tmp-*"))
        )

    def test_changed_run_removes_outputs_for_pdfs_no_longer_selected(self) -> None:
        build_root = self.root / "changed-build/gpt"
        installed_root = self.root / "changed-doc/gpt"
        build_root.mkdir(parents=True)
        installed_root.mkdir(parents=True)
        first_source = build_root / "first.pdf"
        second_source = build_root / "second.pdf"
        first_source.write_bytes(b"new-first")
        second_source.write_bytes(b"new-second")
        (installed_root / first_source.name).write_bytes(b"old-first")
        (installed_root / second_source.name).write_bytes(b"old-second")
        arguments = ["--changed-against", str(installed_root)]

        first = self.invoke([first_source, second_source], jobs=2, extra=arguments)
        self.assertEqual(first.returncode, 0, first.stderr)
        first_manifest = json.loads(
            (self.output / review.RUN_MANIFEST_NAME).read_text(encoding="utf-8")
        )
        first_outputs = {
            record["source"]: self.output / record["output"]
            for record in first_manifest["pdfs"]
        }
        self.assertEqual(len(first_outputs), 2)
        first_label = review.manifest_source(first_source)
        second_label = review.manifest_source(second_source)

        (installed_root / first_source.name).write_bytes(first_source.read_bytes())
        second = self.invoke([first_source, second_source], jobs=2, extra=arguments)

        self.assertEqual(second.returncode, 0, second.stderr)
        second_manifest = json.loads(
            (self.output / review.RUN_MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(
            [record["source"] for record in second_manifest["pdfs"]],
            [second_label],
        )
        self.assertFalse(first_outputs[first_label].exists())
        self.assertTrue(first_outputs[second_label].exists())

    def test_changed_selection_is_bound_to_an_immutable_source_snapshot(self) -> None:
        build_root = self.root / "selection-build/gpt"
        installed_root = self.root / "selection-doc/gpt"
        build_root.mkdir(parents=True)
        installed_root.mkdir(parents=True)
        source = build_root / "document.pdf"
        installed = installed_root / source.name
        source.write_bytes(b"same-at-snapshot")
        installed.write_bytes(b"same-at-snapshot")
        task = review.task_for_pdf(str(source))

        with mock.patch.object(
            review, "review_lock_path", return_value=self.root / "selection.lock"
        ):
            with review.exclusive_review_lock():
                with review.snapshotted_pdf_tasks(
                    [task], self.root, "selection-output"
                ) as snapshots:
                    source.write_bytes(b"changed-after-snapshot")
                    selected, unchanged = review.select_changed_against(
                        snapshots, installed_root
                    )
                    self.assertEqual(selected, [])
                    self.assertEqual(len(unchanged), 1)
                    self.assertEqual(
                        snapshots[0].pdf_sha256,
                        hashlib.sha256(b"same-at-snapshot").hexdigest(),
                    )

    def test_rendering_uses_the_exact_pdf_snapshot_bound_to_the_cache_hash(self) -> None:
        pdf = self.pdfs(["replace-during-render.pdf"])[0]
        original = b"original-pdf-bytes"
        replacement = b"replacement-pdf-bytes"
        original_digest = hashlib.sha256(original).hexdigest()
        pdf.write_bytes(original)
        process = subprocess.Popen(
            [
                sys.executable,
                str(self.plan_harness),
                str(SCRIPT),
                "--jobs",
                "1",
                "--output",
                str(self.output),
                "--cache",
                str(self.cache),
                str(pdf),
            ],
            cwd=ROOT,
            env=self.environment(pages=1, delay=1.0),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 5
        raster_record: dict | None = None
        while time.monotonic() < deadline:
            try:
                records = self.records()
            except FileNotFoundError:
                records = []
            raster_record = next(
                (
                    record
                    for record in records
                    if record["mode"] == "fake-pdftoppm"
                    and record["args"] != ["-v"]
                ),
                None,
            )
            if raster_record is not None:
                break
            time.sleep(0.02)
        else:
            process.kill()
            process.communicate(timeout=10)
            self.fail("PDF raster command did not start")

        pdf.write_bytes(replacement)
        _stdout, stderr = process.communicate(timeout=20)

        self.assertEqual(process.returncode, 0, stderr)
        assert raster_record is not None
        self.assertEqual(raster_record["source_sha256"], original_digest)
        self.assertNotEqual(Path(raster_record["args"][-2]), pdf)
        manifest = json.loads(
            (self.output / review.RUN_MANIFEST_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["pdfs"][0]["pdf_sha256"], original_digest)
        entries = [
            path
            for path in (self.cache / "objects").glob("*/*")
            if path.is_dir()
        ]
        self.assertEqual(len(entries), 1)
        metadata = json.loads(
            (entries[0] / review.METADATA_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["pdf_sha256"], original_digest)
        self.assertFalse(
            any(self.output.parent.glob(f".{self.output.name}.snapshots-*"))
        )

    def test_failed_review_keeps_the_preceding_output_transaction_intact(self) -> None:
        good = self.pdfs(["good.pdf"])[0]
        first = self.invoke([good], jobs=1, pages=1)
        self.assertEqual(first.returncode, 0, first.stderr)
        before = {
            path.relative_to(self.output): path.read_bytes()
            for path in self.output.rglob("*")
            if path.is_file()
        }

        failed = self.invoke(self.pdfs(["fail.pdf"]), jobs=1, pages=1)

        self.assertNotEqual(failed.returncode, 0)
        after = {
            path.relative_to(self.output): path.read_bytes()
            for path in self.output.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)
        self.assertFalse(
            any(self.output.parent.glob(f".{self.output.name}.tmp-*"))
        )
        self.assertFalse(
            any(self.output.parent.glob(f".{self.output.name}.snapshots-*"))
        )

    def test_git_selection_maps_build_pdf_to_its_doc_mirror(self) -> None:
        task = review.PdfTask(
            source=ROOT / "build/gpt/example/document.pdf",
            relative_output=Path("build/gpt/example/document"),
        )
        with mock.patch.object(
            review,
            "git_changed_pdf_paths",
            return_value={Path("doc/gpt/example/document.pdf")},
        ):
            self.assertEqual(review.select_git_changed([task], "HEAD", None), [task])

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
                "--cache",
                str(self.cache),
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
        self.assertFalse(any(self.cache.rglob(".tmp-*")))

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
                "--cache",
                str(self.cache),
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
        self.assertFalse(any(self.cache.rglob(".tmp-*")))

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
                "--cache",
                str(self.cache),
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
        self.assertFalse(any(self.cache.rglob(".tmp-*")))

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
