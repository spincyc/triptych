"""Plain CLI launch is independent of shell activation and working directory."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_lectern import ROOT, _lectern_tool
from lectern.repo import Refused


class LecternRuntimeTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch").mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="lectern-runtime-", dir=ROOT / ".scratch")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.tool = _lectern_tool()
        self.environment = self.root / ".scratch/lectern-venv"
        self.python = self.environment / "bin/python"
        self.enterContext(patch.object(self.tool, "ROOT", self.root))
        self.enterContext(patch.dict(os.environ, {"PATH": "/host/bin", "VIRTUAL_ENV": "/other/env"}, clear=True))
        self.runtime = SimpleNamespace(prefix="/host", flags=SimpleNamespace(isolated=0),
                                       argv=["lectern", "snapshot", "--ref", "Phil 1:21", "--leaf", "é test"])
        self.enterContext(patch.object(self.tool, "sys", self.runtime))
        self.execute = self.enterContext(patch.object(os, "execve"))

    def install_environment(self):
        self.python.parent.mkdir(parents=True)
        self.python.write_text("#!/bin/sh\nexit 0\n")
        self.python.chmod(0o755)

    def test_local_runtime_preserves_argv_and_isolates_shell_python_settings(self):
        self.install_environment()
        os.environ.update(PYTHONHOME="/wrong/home", PYTHONPATH="/wrong/imports",
                          PYTHONUSERBASE="/wrong/packages", PYTHONINSPECT="1")
        self.tool._prepare_runtime()
        executable, argv, environment = self.execute.call_args.args
        self.assertEqual(executable, str(self.python))
        self.assertEqual(argv, [str(self.python), "-I", "-B", str(self.root / "tools/lectern"),
                                *self.runtime.argv[1:]])
        self.assertEqual(environment["VIRTUAL_ENV"], str(self.environment))
        self.assertEqual(environment["PATH"].split(os.pathsep)[0], str(self.python.parent))
        self.assertEqual(environment["TRIPTYCH_BROWSER_DATA_ROOT"], str(self.root / ".scratch/browser-data"))
        for key in ("PYTHONHOME", "PYTHONPATH", "PYTHONUSERBASE", "PYTHONINSPECT"):
            self.assertNotIn(key, environment)
        self.assertEqual(environment["PYTHONNOUSERSITE"], "1")
        self.assertEqual(environment["TRIPTYCH_LECTERN_RUNTIME"], str(self.environment))

    def test_selected_isolated_environment_does_not_reexec_or_leak_loop_marker(self):
        self.install_environment()
        self.runtime.prefix = str(self.environment)
        self.runtime.flags.isolated = 1
        os.environ["TRIPTYCH_LECTERN_RUNTIME"] = str(self.environment)
        self.tool._prepare_runtime()
        self.tool._prepare_runtime()
        self.execute.assert_not_called()
        self.assertNotIn("TRIPTYCH_LECTERN_RUNTIME", os.environ)
        self.assertEqual(os.environ["PATH"].split(os.pathsep).count(str(self.python.parent)), 1)

    def test_activated_but_not_isolated_environment_reexecs(self):
        self.install_environment()
        self.runtime.prefix = str(self.environment)
        self.tool._prepare_runtime()
        self.execute.assert_called_once()

    def test_failed_environment_selection_refuses_instead_of_looping(self):
        self.install_environment()
        os.environ["TRIPTYCH_LECTERN_RUNTIME"] = str(self.environment)
        with self.assertRaisesRegex(Refused, "did not select its isolated Python"):
            self.tool._prepare_runtime()
        self.execute.assert_not_called()

    def test_missing_environment_keeps_host_and_explicit_cache(self):
        os.environ["TRIPTYCH_BROWSER_DATA_ROOT"] = ".scratch/custom-cache"
        self.tool._prepare_runtime()
        self.execute.assert_not_called()
        self.assertEqual(os.environ["TRIPTYCH_BROWSER_DATA_ROOT"], ".scratch/custom-cache")
        self.assertEqual(os.environ["VIRTUAL_ENV"], "/other/env")
        self.assertFalse(self.environment.exists())

    def test_cache_default_is_anchored_to_repository_not_working_directory(self):
        self.tool._prepare_runtime()
        self.assertEqual(os.environ["TRIPTYCH_BROWSER_DATA_ROOT"], str(self.root / ".scratch/browser-data"))
        self.execute.assert_not_called()

    def test_prepared_converter_is_discovered_and_explicit_override_is_preserved(self):
        converter = self.root / ".scratch/web-edition-toolchain/pandoc"
        converter.parent.mkdir(parents=True)
        converter.touch()
        os.environ["TRIPTYCH_PANDOC"] = "/custom/pandoc"
        self.tool._prepare_runtime()
        self.assertEqual(os.environ["PATH"].split(os.pathsep)[0], str(converter.parent))
        self.assertEqual(os.environ["TRIPTYCH_PANDOC"], "/custom/pandoc")

    def test_broken_environment_and_execution_failure_refuse_concisely(self):
        self.environment.mkdir(parents=True)
        with self.assertRaisesRegex(Refused, "local.*Python is unavailable"):
            self.tool._prepare_runtime()
        self.execute.assert_not_called()
        self.install_environment()
        self.execute.side_effect = OSError("not executable")
        with self.assertRaisesRegex(Refused, "Python could not start: not executable"):
            self.tool._prepare_runtime()

    def test_help_and_bad_arguments_do_not_bootstrap_even_with_broken_environment(self):
        self.environment.mkdir(parents=True)
        # Use the real sys module here so argparse can print its ordinary help.
        import sys
        with patch.object(self.tool, "sys", sys):
            for arguments, status in ((["--help"], 0), (["open", "--help"], 0),
                                      (["snapshot", "--help"], 0),
                                      (["snapshot", "--surface", "invalid"], 2)):
                with (self.subTest(arguments=arguments),
                      patch.object(sys, "argv", ["lectern", *arguments]),
                      patch("sys.stdout", new_callable=io.StringIO),
                      patch("sys.stderr", new_callable=io.StringIO),
                      patch.object(self.tool, "_prepare_runtime") as prepare):
                    with self.assertRaises(SystemExit) as stopped:
                        self.tool.main()
                    self.assertEqual(stopped.exception.code, status)
                prepare.assert_not_called()

    def test_real_cli_dispatch_bootstraps_after_parsing_and_before_reading(self):
        import sys
        events = []
        with (patch.object(self.tool, "sys", sys), patch.object(sys, "argv", ["lectern", "snapshot"]),
              patch.object(self.tool, "_prepare_runtime", side_effect=lambda: events.append("runtime")),
              patch.object(self.tool, "snapshot", side_effect=lambda args: events.append("reader") or "screen\n"),
              patch("sys.stdout", new_callable=io.StringIO)):
            self.assertEqual(self.tool.main(), 0)
        self.assertEqual(events, ["runtime", "reader"])

    def test_real_process_selects_isolated_venv_from_foreign_environment_and_cwd(self):
        # Exercise real execve and Python's venv discovery. Only the expensive
        # product/UI consumers are stand-ins; the launcher and CLI are real.
        for name in ("tools/lectern", "scripts/_tooling.py", "scripts/lectern/__init__.py",
                     "scripts/lectern/repo.py"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        (self.root / "scripts/_corpus_index.py").write_text(
            "class CorpusIndexError(Exception): pass\n"
            "class CorpusIndex:\n    def __init__(self, root): pass\n")
        (self.root / "scripts/lectern/bridge.py").write_text(
            "class Bridge:\n    def close(self): pass\nBRIDGE_PROCESS = Bridge()\n")
        (self.root / "scripts/lectern/snapshot.py").write_text(
            "import json, os, sys\n"
            "def render(**options):\n"
            "    return json.dumps({'prefix': sys.prefix, 'isolated': sys.flags.isolated,\n"
            "        'environment': dict(os.environ), 'cwd': os.getcwd(), 'options': options}) + '\\n'\n")
        subprocess.run([sys.executable, "-I", "-m", "venv", "--without-pip", str(self.environment)],
                       check=True, capture_output=True, text=True, timeout=30)
        cwd = self.root / "another working directory"
        cwd.mkdir()
        inherited = dict(os.environ, PYTHONHOME=sys.base_prefix, PYTHONPATH="/foreign/imports",
                         VIRTUAL_ENV="/foreign/environment")
        done = subprocess.run(
            [sys.executable, str(self.root / "tools/lectern"), "snapshot", "--ref", "Phil 1:21 — é"],
            cwd=cwd, env=inherited, capture_output=True, text=True, timeout=30)
        self.assertEqual(done.returncode, 0, done.stderr)
        shown = json.loads(done.stdout)
        self.assertEqual(Path(shown["prefix"]), self.environment)
        self.assertEqual(shown["isolated"], 1)
        self.assertEqual(shown["cwd"], str(cwd))
        self.assertEqual(shown["options"]["intent"]["ref"], "Phil 1:21 — é")
        self.assertEqual(shown["environment"]["TRIPTYCH_BROWSER_DATA_ROOT"],
                         str(self.root / ".scratch/browser-data"))
        self.assertEqual(shown["environment"]["VIRTUAL_ENV"], str(self.environment))
        for name in ("PYTHONHOME", "PYTHONPATH", "TRIPTYCH_LECTERN_RUNTIME"):
            self.assertNotIn(name, shown["environment"])


if __name__ == "__main__":
    unittest.main()
