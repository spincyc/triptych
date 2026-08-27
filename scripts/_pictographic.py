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


# --- the artistic entry path ------------------------------------------------
#
# The only sanctioned door into artistic rendering. It fails closed: a blocked
# scene, a contract that will not compile, a skeleton that will not generate, or
# a panel manifest that disagrees with its skeleton all refuse, and refuse
# without leaving a package behind. There is no force path; an override that
# leaves no trace is indistinguishable from the failure it bypasses.

CANARY_SCENE = "LM-001A"

ART_AGENT_INSTRUCTION = """\
# Art-agent instructions — {plate_id}

Generate only from the supplied compiled render contract and deterministic
skeleton. The skeleton owns composition and geometry. You own artistic
realization only. Do not restage the scene.

## What you are given

- `render-contract.yaml` — the compiled geometry. Authoritative.
- `skeleton.svg` — the deterministic skeleton. Authoritative for composition.
- `provenance.yaml` — identity, baseline commit, panel manifest, readiness.

## Scene

- plate: {plate_id}
- title: {title}
- structural baseline commit: {baseline}
- render-contract version: {version}
- readiness: {readiness}
- declared panels ({panel_count}): {panels}
- additional panels: {additional}
{canary_note}
## What you own

Graphite and pencil texture, line quality, shading and value, facial
naturalism, fabric and vestment realism, architectural detail that moves
nothing, surface finish, and visual hierarchy inside the declared panel.

## What you do not own

Choreography, actor anchors, actor facing, object transforms, Missal
orientation, object possession, crossing precedence, the number of altar steps,
the world-side mapping of Gospel and Epistle, camera projection, declared panel
count, required visible objects, branch selection.

Draw exactly {panel_count} panel(s). Adding an inset, a key, a locator, a
vignette or a plan is a structural failure even if it would help.

The Missal is the known failure mode. Its reading orientation is compiled into
the contract and is the same on the Epistle and Gospel sides. Do not mirror it,
do not rotate it for composition, and do not infer it from which side of the
altar it stands on.

## Review

Return two independent decisions:

    STRUCTURE: PASS | FAIL
    ART:       PASS | FAIL

STRUCTURE asks whether the plate is faithful to the contract and skeleton. ART
asks whether it is publication quality. A plate is approved only when both are
PASS. A structural violation is FAIL, never "approved with notes", however good
the drawing is.

The full rules are in the durable protocol at
`src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/artistic/RENDERING-PROTOCOL.md`.
"""


class SeedRefused(Exception):
    """The artistic entry path refused to seed. Carries the reason."""


def art_seed(directory: Path, scene_id: str, out: Path) -> dict:
    """Prepare the canonical input package for an artistic agent.

    Raises SeedRefused, having written nothing, when the scene may not be
    seeded.
    """
    module = compiler(directory)
    build = module.Compiler()

    try:
        contract = build.compile_scene(scene_id)
    except KeyError as unknown:
        raise SeedRefused(f"unknown scene {scene_id!r}") from unknown
    except Exception as failure:  # a contract that will not compile
        raise SeedRefused(
            f"{scene_id}: the render contract failed to compile: {failure}"
        ) from failure

    readiness = contract["art_readiness"]
    if readiness["status"] != "ready":
        cues = readiness.get("unresolved_cues") or ["(no cue recorded)"]
        listed = "\n".join(f"  - {cue}" for cue in cues)
        raise SeedRefused(
            f"{scene_id} is BLOCKED_FOR_ART and must not be rendered.\n"
            f"Blocking cue(s):\n{listed}\n"
            "Blocked means stop. Resolve the cue in the structural or "
            "render-contract lane, by human review; never by inference, an "
            "aesthetic guess, or an older fenced guide."
        )

    for item in contract["objects"]:
        if item.get("unresolved_placement") and item.get("visible") is not False:
            raise SeedRefused(
                f"{scene_id}: render-critical transform unresolved for "
                f"{item['id']!r}"
            )

    if not contract.get("panels"):
        raise SeedRefused(f"{scene_id}: no declared panel")
    if contract.get("additional_panels") != "forbidden":
        raise SeedRefused(f"{scene_id}: the panel list is not closed")
    if not contract.get("structural_baseline_commit"):
        raise SeedRefused(f"{scene_id}: missing structural provenance")

    try:
        drawing = skeletons(directory).render(contract)
    except Exception as failure:
        raise SeedRefused(
            f"{scene_id}: skeleton generation failed: {failure}"
        ) from failure

    declared = [p["id"] for p in contract["panels"]]
    import re

    drawn = set(re.findall(r"panel ([a-z0-9-]+)</text>", drawing))
    if drawn != set(declared):
        raise SeedRefused(
            f"{scene_id}: declared panels {sorted(declared)} disagree with the "
            f"skeleton's {sorted(drawn)}"
        )

    provenance = {
        "schema": "triptych.mass_pictographic.plate_provenance",
        "plate_id": contract["plate_id"],
        "scene_ids": list(contract["scene_ids"]),
        "title": contract["title"],
        "structural_baseline_commit": contract["structural_baseline_commit"],
        "render_contract_version": contract["render_contract_version"],
        "render_contract_source": "render-contract.yaml",
        "skeleton_source": "skeleton.svg",
        "panel_manifest": declared,
        "additional_panels": contract["additional_panels"],
        "art_readiness": readiness["status"],
        "visible_invariants": list(contract["visible_invariants"]),
        "is_pipeline_canary": scene_id == CANARY_SCENE,
        "structure_review": "PENDING",
        "art_review": "PENDING",
        "provenance_contract": (
            "src/gpt/liturgy/roman-rite/1962/reference/"
            "mass-pictographic-dictionary/artistic/plate-provenance.yaml"
        ),
        "protocol": (
            "src/gpt/liturgy/roman-rite/1962/reference/"
            "mass-pictographic-dictionary/artistic/RENDERING-PROTOCOL.md"
        ),
    }

    canary_note = ""
    if scene_id == CANARY_SCENE:
        canary_note = (
            "\nTHIS SCENE IS THE PIPELINE CANARY. It is rendered before style\n"
            "development begins, and the lane proceeds only once it reaches\n"
            "STRUCTURE = PASS. If it fails structurally, stop and diagnose the\n"
            "pipeline rather than continuing to other scenes.\n"
        )
    instructions = ART_AGENT_INSTRUCTION.format(
        plate_id=contract["plate_id"],
        title=contract["title"],
        baseline=contract["structural_baseline_commit"],
        version=contract["render_contract_version"],
        readiness=readiness["status"],
        panel_count=len(declared),
        panels=", ".join(declared),
        additional=contract["additional_panels"],
        canary_note=canary_note,
    )

    package = out / scene_id
    package.mkdir(parents=True, exist_ok=True)
    (package / "render-contract.yaml").write_text(dump(contract), encoding="utf-8")
    (package / "skeleton.svg").write_text(drawing, encoding="utf-8")
    (package / "provenance.yaml").write_text(dump(provenance), encoding="utf-8")
    (package / "ART-AGENT-INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
    return {"package": package, "provenance": provenance}
