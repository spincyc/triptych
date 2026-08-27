"""Shared logic for the pictographic render-contract tool.

Lives outside tools/ so that the registry scan, which requires every file in
tools/ to be a registered tool, stays clean.

Loads the render-contract modules that sit beside the corpus they describe,
rather than duplicating them here: the compiler and the skeleton generator are
the authority, and this module only routes to them.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"

CALENDARS = {"roman-1962"}
FORMS = {"low-mass"}
CONTRACT_VERSION_DIR = "v1"


def contract_dir(calendar: str, form: str) -> Path:
    if calendar not in CALENDARS:
        raise SystemExit(f"unknown calendar {calendar!r}; known: {sorted(CALENDARS)}")
    if form not in FORMS:
        raise SystemExit(f"unknown form {form!r}; known: {sorted(FORMS)}")
    return OWNER / "render-contract" / form / CONTRACT_VERSION_DIR


def _module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compiler(directory: Path):
    return _module(directory / "compile.py", "_pictographic_compile")


def skeletons(directory: Path):
    return _module(directory / "skeleton.py", "_pictographic_skeleton")


def dump(data: dict) -> str:
    import yaml

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)


def write_contract(directory: Path, scene_id: str, out: Path) -> Path:
    module = compiler(directory)
    contract = module.Compiler().compile_scene(scene_id)
    target = out / "contracts" / f"{scene_id}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump(contract), encoding="utf-8")
    return target


def write_skeleton(directory: Path, scene_id: str, out: Path) -> Path:
    module = compiler(directory)
    contract = module.Compiler().compile_scene(scene_id)
    drawing = skeletons(directory).render(contract)
    target = out / "skeletons" / f"{scene_id}.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(drawing, encoding="utf-8")
    return target


def readiness_report(directory: Path) -> dict:
    module = compiler(directory)
    _, readiness = module.Compiler().compile_all()
    return readiness
