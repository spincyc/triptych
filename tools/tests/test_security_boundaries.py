"""Adversarial checks for executable-code and filesystem trust boundaries."""

from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402
import _proper_latin  # noqa: E402
import _recensions  # noqa: E402


def load_tool(name: str):
    loader = SourceFileLoader(
        f"test_security_{name.replace('-', '_')}", str(ROOT / "tools" / name)
    )
    spec = spec_from_loader(loader.name, loader)
    if spec is None:  # pragma: no cover - a broken checkout
        raise RuntimeError(f"cannot load {name}")
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


class ExecutableCodeBoundaryTests(unittest.TestCase):
    def test_external_calendar_root_cannot_supply_source_library_code(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            repository = Path(room) / "untrusted"
            calendars = repository / "src" / "sources" / "calendars"
            calendars.mkdir(parents=True)
            tools = repository / "tools"
            tools.mkdir()
            sentinel = Path(room) / "executed"
            (tools / "source-library").write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('executed', encoding='utf-8')\n",
                encoding="utf-8",
            )

            cache_key = repository.resolve()
            _proper_latin._SOURCE_LIBRARY_CACHE.pop(cache_key, None)
            try:
                _proper_latin._source_library_records(calendars)
            finally:
                _proper_latin._SOURCE_LIBRARY_CACHE.pop(cache_key, None)

            self.assertFalse(
                sentinel.exists(),
                "a data root selected by --root must never supply executable Python",
            )


class OutputConfinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.propers = load_tool("mass-propers")
        cls.ordinary = load_tool("mass-ordinary")

    def symlinked_output(self, room: str, kind: str) -> tuple[Path, Path]:
        base = Path(room)
        output = base / "output"
        (output / "structure").mkdir(parents=True)
        victim = base / "victim"
        victim.mkdir()
        sentinel = victim / "keep.json"
        sentinel.write_text('{"keep":true}\n', encoding="utf-8")
        (output / "structure" / kind).symlink_to(victim, target_is_directory=True)
        return output, sentinel

    def test_mass_propers_refuses_symlinked_owned_directory_before_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            output, sentinel = self.symlinked_output(room, "propers")
            with self.assertRaisesRegex(ValueError, "propers output path is a symlink"):
                self.propers.run_structure(
                    argparse.Namespace(out=str(output), root="not-read")
                )
            self.assertTrue(sentinel.is_file())

    def test_mass_ordinary_refuses_symlinked_owned_directory_before_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            output, sentinel = self.symlinked_output(room, "ordinary")
            with self.assertRaisesRegex(
                self.ordinary.SourceError, "Ordinary output path is a symlink"
            ):
                self.ordinary.run_structure(argparse.Namespace(out=str(output)))
            self.assertTrue(sentinel.is_file())


class RepositoryReferenceConfinementTests(unittest.TestCase):
    def test_recension_reference_cannot_follow_a_symlink_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            base = Path(room)
            repository = base / "repository"
            repository.mkdir()
            outside = base / "outside.json"
            outside.write_text('{"record":{"schema":"fixture"}}\n', encoding="utf-8")
            (repository / "evidence.json").symlink_to(outside)

            problem = _recensions._reference_problem(
                repository, "evidence.json#/record", "coverage_ref"
            )

            self.assertIn("escapes the repository through a symlink", problem or "")

    def test_calendar_coverage_record_cannot_follow_a_symlink_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            base = Path(room)
            repository = base / "repository"
            repository.mkdir()
            outside = base / "outside.toml"
            outside.write_text('[[records]]\nid = "outside"\n', encoding="utf-8")
            (repository / "evidence.toml").symlink_to(outside)

            problem = _calendars._coverage_record_problem(
                repository, "evidence.toml#id=outside", "record"
            )

            self.assertIn("escapes the repository through a symlink", problem or "")

    def test_act_inventory_extends_cannot_follow_a_symlink_outside_directory(self) -> None:
        with tempfile.TemporaryDirectory() as room:
            base = Path(room)
            inventory = base / "repository" / "inventories"
            inventory.mkdir(parents=True)
            outside = base / "outside.toml"
            outside.write_text(
                'acts_schema = 1\n[[acts]]\nid = "outside-act"\n', encoding="utf-8"
            )
            (inventory / "outside.toml").symlink_to(outside)
            source = inventory / "acts.toml"
            source.write_text(
                'acts_schema = 1\nextends = "outside.toml"\n', encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "escapes its local directory"):
                _calendars._act_ids(source)


if __name__ == "__main__":
    unittest.main()
