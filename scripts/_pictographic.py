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


def web(directory: Path):
    return _module(ROOT / "scripts" / "_pictographic_web.py", "_pictographic_web")


def underlays(directory: Path):
    return _module(directory / "underlay.py", "_pictographic_underlay")


def composition_digest(directory: Path) -> tuple[str, dict]:
    """Hash the files that decide what a published plate looks like.

    The visual review is bound to this digest. Anything that can change the
    composition - the sanctuary, the camera, or the renderer itself - is in it,
    so an approval cannot outlive the picture it was given for.
    """
    import hashlib
    import yaml

    master = yaml.safe_load(
        (directory / "sanctuary-master.yaml").read_text(encoding="utf-8")
    )
    review = master.get("underlay_visual_review") or {}
    digest = hashlib.sha256()
    for name in review.get("digest_inputs") or []:
        source = directory / name
        if not source.is_file():
            raise SeedRefused(
                f"composition digest input {name!r} is missing; the visual "
                "review cannot be verified"
            )
        body = source.read_bytes()
        if name == "sanctuary-master.yaml":
            # Exclude the recorded digest itself, or refreshing it would always
            # invalidate it.
            body = b"\n".join(
                line for line in body.split(b"\n")
                if not line.strip().startswith(b"reviewed_geometry_digest:")
            )
        digest.update(name.encode("utf-8"))
        digest.update(hashlib.sha256(body).digest())
    return digest.hexdigest(), review


def require_visual_review(directory: Path, scene_id: str) -> None:
    """Refuse to seed art from a composition nobody has looked at.

    Fail-closed in both directions: an unapproved preset is refused, and so is
    an approval whose geometry has moved since it was given.
    """
    current, review = composition_digest(directory)
    if review.get("status") != "approved":
        raise SeedRefused(
            f"{scene_id}: the publication composition is not approved "
            f"(underlay_visual_review.status = {review.get('status')!r}). "
            "Render the canary, look at it, and record the review in "
            "sanctuary-master.yaml before seeding art."
        )
    recorded = review.get("reviewed_geometry_digest")
    if recorded != current:
        raise SeedRefused(
            f"{scene_id}: the publication composition has changed since it was "
            f"last looked at (recorded {recorded!r}, current {current!r}). "
            f"Re-render the canary {review.get('canary')}, answer the gate "
            "questions again, and refresh the digest with "
            "`tpt pictographic composition-review --refresh` only after "
            "actually looking at it."
        )


def load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


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


def underlay_module(directory: Path):
    return underlays(directory)


def compile_scene(directory: Path, scene_id: str) -> dict:
    return compiler(directory).Compiler().compile_scene(scene_id)


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

Generate only by editing the supplied render underlay. The underlay owns
composition and geometry. You own artistic realization only. Do not restage the
scene, and do not compose a fresh image from any description of it.

## EDIT THE ATTACHED `render-underlay.png`. Do not create a fresh composition.

`render-underlay.png` is the mandatory source image. Load it into an image
EDIT / style-transformation operation and render artistic quality onto that
exact geometry. Do not use it as loose inspiration for a text-to-image
generation.

**If your image tool cannot use the underlay as an image-edit source, STOP and
report that limitation. Do not substitute text-to-image generation.** A fresh
composition is how the Missal ended up on the wrong side of the altar twice.

## What you are given

- `render-underlay.png` — **the mandatory edit source.** It owns all visible
  geometry: object identity, object side, orientation, human placement, camera
  and panel count.
- `render-underlay.svg` — the same drawing as vectors, if useful.
- `render-contract.yaml` — the compiled geometry in numbers. Supporting
  authority for review.
- `skeleton.svg` — the diagnostic schematic, with labels and angles. Supporting
  authority only; it is a debugging view, never the conditioning image.
- `provenance.yaml` — identity, baseline commit, panel manifest, readiness.

## Produce scene art only

Do not generate a title, a caption, a plate identifier, metadata, a source
citation, a border, a header or a footer. Those are deterministic typography
handled after approval by the publication compositor. Invented prose describing
the scene is not acceptable in the raw art.

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


def art_seed(directory: Path, scene_id: str, out: Path,
             allow_dirty: bool = False) -> dict:
    """Prepare the canonical input package for an artistic agent.

    The package is the whole handoff, including the prompt that carries it into
    a fresh web conversation. Nothing about the transition is left for a human
    to reconstruct from memory.

    Raises SeedRefused, having written nothing, when the scene may not be
    seeded. `allow_dirty` produces an explicitly NONCANONICAL development
    package instead of refusing an uncommitted tree.
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

    # The gates above are about the SCENE: whether it may be drawn at all.
    # These two are about the PACKAGE: whether this checkout may build one.
    # They come second on purpose. A blocked scene seeded from a dirty tree has
    # two problems, and the one the operator needs told about is the blocked
    # scene; reporting the working tree instead would hide a liturgical
    # refusal behind a workflow one.
    require_visual_review(directory, scene_id)

    handoff = web(directory)
    try:
        identity = handoff.repository_identity(ROOT, allow_dirty=allow_dirty)
        rules = handoff.durable_rules(
            OWNER / "artistic" / "RENDERING-PROTOCOL.md"
        )
    except handoff.PromptRefused as refusal:
        raise SeedRefused(f"{scene_id}: {refusal}") from refusal

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

    # The render underlay is the mandatory visual conditioning input. Without a
    # recognizable projected drawing the artist is back to reconstructing the
    # scene from labels, which is the failure this whole layer exists to end.
    module = underlays(directory)
    try:
        underlay_svg = module.Underlay().render(contract)
    except Exception as failure:
        raise SeedRefused(
            f"{scene_id}: render underlay could not be generated: {failure}"
        ) from failure

    missing = [
        item["id"]
        for item in contract["objects"]
        if item.get("position") is not None
        and item.get("visible") is not False
        and item["id"] not in module.Underlay().library
    ]
    if missing:
        raise SeedRefused(
            f"{scene_id}: no recognizable underlay geometry for visible "
            f"object(s) {sorted(set(missing))}. Add it to "
            "underlay-objects.yaml rather than shipping an anonymous mark."
        )

    package = out / scene_id
    package.mkdir(parents=True, exist_ok=True)
    (package / "render-contract.yaml").write_text(dump(contract), encoding="utf-8")
    (package / "skeleton.svg").write_text(drawing, encoding="utf-8")
    (package / "provenance.yaml").write_text(dump(provenance), encoding="utf-8")

    underlay_path = package / "render-underlay.svg"
    underlay_path.write_text(underlay_svg, encoding="utf-8")
    raster_path = package / "render-underlay.png"
    try:
        module.rasterize(underlay_path, raster_path)
    except Exception as failure:
        # Leave no half-package behind: a partial seed is exactly the weak
        # package that invites restaging.
        for stray in package.iterdir():
            stray.unlink()
        package.rmdir()
        raise SeedRefused(
            f"{scene_id}: underlay rasterization failed: {failure}"
        ) from failure

    import hashlib

    raster = raster_path.read_bytes()
    provenance["render_underlay_source"] = "render-underlay.png"
    provenance["render_underlay_svg_source"] = "render-underlay.svg"
    provenance["render_underlay_sha256"] = hashlib.sha256(raster).hexdigest()
    provenance["skeleton_source"] = "skeleton.svg"
    provenance["generation_mode"] = "image-edit"
    provenance["raw_scene_art"] = None
    provenance["publication_plate"] = None
    width, height = module.PANEL_W * len(declared), module.PANEL_H
    provenance["render_underlay_width"] = width * module.RASTER_SCALE
    provenance["render_underlay_height"] = height * module.RASTER_SCALE
    provenance["repository"] = identity["repository"]
    provenance["branch"] = identity["branch"]
    provenance["seed_commit"] = identity["seed_commit"]
    provenance["canonical_package"] = identity["canonical"]
    provenance["web_prompt"] = "WEB-AGENT-PROMPT.md"
    provenance["package_manifest"] = "PACKAGE-MANIFEST.yaml"
    (package / "provenance.yaml").write_text(dump(provenance), encoding="utf-8")
    (package / "ART-AGENT-INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")

    # The fresh-web handoff. Anything that goes wrong from here takes the whole
    # package with it: a package holding every file but the prompt is exactly
    # the half-valid seed that sends a human back to writing one by hand.
    def discard():
        for stray in sorted(package.iterdir()):
            stray.unlink()
        package.rmdir()

    try:
        camera_model = load_yaml(directory / "camera-model.yaml")
        master = load_yaml(directory / "sanctuary-master.yaml")
        summary = handoff.scene_summary(contract, camera_model, master)
        handoff.verify_summary(contract, summary)
        prompt = handoff.render_prompt(
            contract, provenance, identity, summary, rules
        )
        handoff.check_prompt_complete(prompt)
        (package / "WEB-AGENT-PROMPT.md").write_text(prompt, encoding="utf-8")
        manifest = handoff.package_manifest(
            package, contract, provenance, identity
        )
        (package / "PACKAGE-MANIFEST.yaml").write_text(
            dump(manifest), encoding="utf-8"
        )
    except handoff.PromptRefused as refusal:
        discard()
        raise SeedRefused(f"{scene_id}: {refusal}") from refusal
    except Exception as failure:
        discard()
        raise SeedRefused(
            f"{scene_id}: the fresh-web handoff could not be generated: "
            f"{failure}"
        ) from failure

    return {
        "package": package,
        "provenance": provenance,
        "manifest": manifest,
        "identity": identity,
    }
