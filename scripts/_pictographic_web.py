"""The fresh-web handoff: repository binding, scene summary, and the prompt.

The operational gap this closes. `art-seed` emitted a technically complete art
package and then a human had to write, by hand, the prompt that carries it into
a fresh web conversation. That prompt has to state the repository, the exact
commit, the scene's readiness, its panel manifest, which file is the mandatory
edit source, and — the part that was actually hard — what is visibly true in
this particular scene. Written by hand it was rewritten every time, and a
prompt nobody can diff is a prompt nobody reviewed.

Everything here is generated from the compiled contract and from git. Nothing
in this module states a fact about a scene that the contract does not already
carry, and nothing states a durable rule that the protocol does not already
own: the artist's freedoms and the render contract's reserved list are read out
of `RENDERING-PROTOCOL.md` rather than restated, so the two cannot drift.

Deliberately generic. It is given a compiled contract and a camera model, and
it knows nothing about Low Mass, two servers, one panel, or LM-001A. Every
scene-specific sentence comes from scene data, so the same generator will serve
the sung and pontifical forms when their contracts exist.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path


class PromptRefused(Exception):
    """The handoff cannot be generated, so no package may claim to be one."""


# --------------------------------------------------------------------------
# repository binding
# --------------------------------------------------------------------------
def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise PromptRefused(
            f"git {' '.join(args)} failed: {result.stderr.strip() or 'no output'}"
        )
    return result.stdout.strip()


def repository_identity(root: Path, allow_dirty: bool = False) -> dict:
    """Bind the package to an exact commit, or refuse to be canonical.

    A canonical package claims a seed commit, and that claim has to be worth
    something: a reader must be able to check out that commit and regenerate
    the same package. A dirty checkout cannot honour it, so the default is to
    refuse rather than to name a commit whose tree is not what was packaged.

    `allow_dirty` produces a package that says NONCANONICAL everywhere it says
    anything, which is what a development package is for.
    """
    remote = _git(root, "remote", "get-url", "origin")
    # A package states its repository as a fact, so the origin has to be a
    # hosted remote. A filesystem path is a perfectly good git remote and a
    # perfectly bad provenance claim: a local clone would otherwise report a
    # repository named after two directories that happen to be adjacent.
    hosted = re.match(
        r"^(?:(?:https?|ssh|git)://[^/]+/|[\w.-]+@[\w.-]+:)(.+?)(?:\.git)?/?$",
        remote,
    )
    if not hosted:
        raise PromptRefused(
            f"the origin remote {remote!r} is not a hosted repository URL, so "
            "the package cannot state where it came from"
        )
    slug = hosted.group(1)
    if not re.fullmatch(r"[A-Za-z0-9][\w.-]*(?:/[A-Za-z0-9][\w.-]*)+", slug):
        raise PromptRefused(
            f"the origin remote {remote!r} does not name an owner/repository"
        )

    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    commit = _git(root, "rev-parse", "HEAD")
    dirty = bool(_git(root, "status", "--porcelain"))

    if dirty and not allow_dirty:
        raise PromptRefused(
            "the working tree has uncommitted changes, so a canonical package "
            "cannot bind itself to a commit. Commit first, or pass "
            "--development for an explicitly NONCANONICAL package."
        )
    return {
        "repository": slug,
        "branch": branch,
        "seed_commit": commit,
        "canonical": not dirty,
        "worktree": "dirty" if dirty else "clean",
    }


# --------------------------------------------------------------------------
# durable rules, read from the protocol rather than restated
# --------------------------------------------------------------------------
def _bold_list(protocol: str, label: str) -> list[str]:
    match = re.search(
        rf"\*\*{re.escape(label)}\*\*\s*[-—]+\s*(.+?)\.\s*\n\s*\n",
        protocol,
        re.S,
    )
    if not match:
        raise PromptRefused(
            f"the artistic protocol no longer states {label!r} in a form this "
            "generator can read; the prompt would have to invent the rule"
        )
    items = [
        " ".join(part.split()) for part in match.group(1).split(";")
    ]
    items = [item for item in items if item]
    if not items:
        raise PromptRefused(f"the protocol lists nothing under {label!r}")
    return items


def durable_rules(protocol_path: Path) -> dict:
    """The artist's freedoms and the contract's reserved list, from source.

    Restating them here would create a second copy to keep in step with the
    protocol, and the copy would win by being the one the artist actually
    reads.
    """
    if not protocol_path.is_file():
        raise PromptRefused(f"the artistic protocol is missing at {protocol_path}")
    protocol = protocol_path.read_text(encoding="utf-8")
    return {
        "artist_owns": _bold_list(protocol, "Owned by the artist"),
        "contract_owns": _bold_list(
            protocol, "Owned by the render contract, and not the artist"
        ),
    }


# --------------------------------------------------------------------------
# page sides
# --------------------------------------------------------------------------
def page_side_rule(panel: dict, camera_model: dict) -> dict | None:
    """How world sides land on the page, for this panel's own frame.

    Read from the panel's declared frame rather than assumed. A side elevation
    puts altarward on page right and has no Gospel/Epistle page mapping at all,
    so the summary must not claim one.
    """
    frame = (panel.get("camera") or {}).get("frame") or {}
    right = frame.get("page_right_world_direction")
    left = frame.get("page_left_world_direction")
    if not right or not left:
        return None
    directions = {d["id"]: d["vector"] for d in camera_model.get("directions", [])}
    return {"page_right": right, "page_left": left, "vectors": directions}


def _named(value) -> str | None:
    """The contract writes an absent handler as the string "none"."""
    if value in (None, "none", ""):
        return None
    return value


def _lateral_side(x: float) -> str:
    if x > 1e-9:
        return "epistleward"
    if x < -1e-9:
        return "gospelward"
    return "centre"


def page_side_of(x: float, sides: dict | None) -> str | None:
    """Which side of the page a world-x lands on, or None if the view has none."""
    if sides is None:
        return None
    lateral = _lateral_side(x)
    if lateral == "centre":
        return "centre"
    if sides["page_right"] == lateral:
        return "page right"
    if sides["page_left"] == lateral:
        return "page left"
    return None


# --------------------------------------------------------------------------
# scene summary
# --------------------------------------------------------------------------
SIDE_WORD = {
    "epistleward": "Epistle side",
    "gospelward": "Gospel side",
    "centre": "the centreline",
}


def level_name(z: float, levels: dict) -> str:
    for name, value in levels.items():
        if isinstance(value, (int, float)) and abs(value - z) < 1e-6:
            return name.replace("_", " ")
    return None


def actor_facts(contract: dict, panel: dict, camera_model: dict,
                levels: dict) -> list[dict]:
    sides = page_side_rule(panel, camera_model)
    facts = []
    for actor in contract.get("actors") or []:
        position = actor.get("position")
        if position is None:
            raise PromptRefused(
                f"{contract['plate_id']}: actor {actor['id']!r} has no compiled "
                "position, so the summary cannot say where it stands"
            )
        level = level_name(position[2], levels)
        if level is None:
            raise PromptRefused(
                f"{contract['plate_id']}: actor {actor['id']!r} stands at "
                f"elevation {position[2]}, which is not a named sanctuary "
                "level; the summary cannot state its floor relationship"
            )
        hands = actor.get("hands") or {}
        facts.append({
            "id": actor["id"],
            "role": actor.get("role"),
            "lateral": _lateral_side(position[0]),
            "page_side": page_side_of(position[0], sides),
            "level": level,
            "depth": position[1],
            "posture": actor["posture"],
            "bow": actor.get("bow"),
            "facing_yaw_deg": actor.get("body_facing_yaw_deg"),
            "gaze": actor.get("gaze"),
            "hands": hands,
            "side": actor.get("side"),
            "facing": actor.get("facing_semantic"),
            "gestures": list(actor.get("gestures") or []),
            # Agency and attachment are different facts and the contract keeps
            # them apart: a vestment is parented to the priest while handled by
            # nobody, and a book can be carried by one server on behalf of
            # another. Both matter to an artist, so both are collected.
            "holds": sorted({
                item["id"]
                for item in contract.get("objects") or []
                if item.get("handled_by") == actor["id"]
            }),
            "wears_or_carries": sorted({
                item["id"]
                for item in contract.get("objects") or []
                if item.get("parent_transform") == actor["id"]
                and item.get("handled_by") != actor["id"]
            }),
        })
    if not facts:
        raise PromptRefused(
            f"{contract['plate_id']}: no actors, so no visible-invariant "
            "summary can be generated"
        )
    return facts


def object_facts(contract: dict, panel: dict, camera_model: dict,
                 levels: dict) -> list[dict]:
    sides = page_side_rule(panel, camera_model)
    facts = []
    for item in contract.get("objects") or []:
        if item.get("visible") is False:
            continue
        # An object in somebody's hands has no compiled position of its own,
        # and is exactly the object an artist most needs told about. Dropping
        # it because it lacked a position would have let a held Missal be
        # drawn anywhere at all.
        if item.get("position") is None and not item.get("handled_by"):
            continue
        position = item.get("position")
        reading = item.get("reading") or {}
        support = item.get("support") or {}
        facts.append({
            "id": item["id"],
            "lateral": _lateral_side(position[0]) if position else None,
            "page_side": page_side_of(position[0], sides) if position else None,
            "on": level_name(position[2], levels) if position else None,
            "placement_kind": item.get("placement_kind"),
            "placement": item.get("placement"),
            "state": item.get("state_after"),
            "yaw_deg": item.get("yaw_deg"),
            "orientation_rule": item.get("orientation_rule"),
            "held_by": _named(item.get("handled_by")),
            "parent": _named(item.get("parent_transform")),
            "supported_by": reading.get("supported_by") or support.get(
                "supported_by_surface"
            ),
            "support_pitch_deg": reading.get("support_pitch_deg")
            or support.get("pitch_deg"),
            "orientation_immutable": bool(reading.get("identical_on_both_sides")),
        })
    return facts


def sanctuary_facts(master: dict) -> dict:
    steps = master["steps"]
    return {
        "step_count": steps["count"],
        "predella": True,
        "levels": [
            name.replace("_", " ")
            for name, value in master["levels"].items()
            if isinstance(value, (int, float))
        ],
        "first_step_leading_edge": steps["first_leading_edge_y"],
        "altar_parts": [
            part for part in ("body", "mensa", "gradine", "tabernacle",
                              "reredos_hint")
            if part in master["altar"]
        ],
    }


def scene_summary(contract: dict, camera_model: dict, master: dict) -> dict:
    """Everything the prompt says about this scene, as data."""
    panels = contract.get("panels") or []
    if not panels:
        raise PromptRefused(f"{contract['plate_id']}: no declared panel")
    levels = master["levels"]
    primary = panels[0]
    return {
        "actors": actor_facts(contract, primary, camera_model, levels),
        "objects": object_facts(contract, primary, camera_model, levels),
        "sanctuary": sanctuary_facts(master),
        "panels": [
            {
                "id": panel["id"],
                "projection": panel["camera"]["projection"],
                "preset": panel["camera"].get("preset"),
                "page_sides": page_side_rule(panel, camera_model),
            }
            for panel in panels
        ],
    }


def verify_summary(contract: dict, summary: dict) -> None:
    """Refuse a summary that contradicts, or silently drops, scene data.

    Cheap to write and worth having: the summary is what the artist reads, and
    a summary that omits a visible object is a licence to draw it anywhere.
    """
    actors = {actor["id"] for actor in contract.get("actors") or []}
    summarised = {actor["id"] for actor in summary["actors"]}
    if actors != summarised:
        raise PromptRefused(
            f"{contract['plate_id']}: the summary covers actors {sorted(summarised)} "
            f"but the contract declares {sorted(actors)}"
        )

    visible = {
        item["id"]
        for item in contract.get("objects") or []
        if item.get("visible") is not False
        and (item.get("position") is not None or item.get("handled_by"))
    }
    described = {item["id"] for item in summary["objects"]}
    if visible != described:
        raise PromptRefused(
            f"{contract['plate_id']}: the summary describes objects "
            f"{sorted(described)} but the contract places {sorted(visible)}"
        )

    for actor in summary["actors"]:
        source = next(a for a in contract["actors"] if a["id"] == actor["id"])
        if actor["posture"] != source["posture"]:
            raise PromptRefused(
                f"{contract['plate_id']}: the summary calls {actor['id']} "
                f"{actor['posture']!r} and the contract says "
                f"{source['posture']!r}"
            )
        # The page side is derived from the panel's declared frame; the lateral
        # side is derived from the sign of world x. They are two different
        # statements and a disagreement means the frame was misread.
        expected = _lateral_side(source["position"][0])
        if actor["lateral"] != expected:
            raise PromptRefused(
                f"{contract['plate_id']}: the summary puts {actor['id']} "
                f"{actor['lateral']} and its world x is {source['position'][0]}"
            )

    if len(summary["panels"]) != len(contract["panels"]):
        raise PromptRefused(
            f"{contract['plate_id']}: the summary describes "
            f"{len(summary['panels'])} panels and the contract declares "
            f"{len(contract['panels'])}"
        )


# --------------------------------------------------------------------------
# prose
# --------------------------------------------------------------------------
ROLE_WORD = {
    "celebrant": "the celebrant",
    "acolyte-epistle-side": "the Epistle-side server",
    "acolyte-gospel-side": "the Gospel-side server",
}

POSTURE_WORD = {
    "standing": "standing",
    "kneeling": "kneeling",
    "kneeling-erect": "kneeling erect",
    "genuflecting": "genuflecting",
    "walking": "walking",
    "bowing-low-over-altar": "bowing low over the altar",
    "stooping": "stooping",
}


def _wrap(text: str, width: int = 78, indent: str = "  ") -> str:
    """Wrap a generated bullet so a human can read the pasted prompt."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return ("\n" + indent).join(lines)


def _place_phrase(lateral, page_side, level) -> str:
    where = SIDE_WORD.get(lateral, lateral or "")
    if page_side and page_side != "centre":
        where += f" ({page_side})"
    if level == "floor":
        return f"{where}, in plano on the sanctuary floor"
    if level and level.startswith("step"):
        return f"{where}, on {level}"
    if level:
        return f"{where}, on the {level}"
    return where


def _actor_sentence(actor: dict) -> str:
    role = ROLE_WORD.get(actor.get("role"), actor.get("role"))
    line = f"`{actor['id']}`"
    if role:
        line += f", {role}"
    line += " — " + _place_phrase(
        actor["lateral"], actor.get("page_side"), actor["level"]
    )
    line += f", {POSTURE_WORD.get(actor['posture'], actor['posture'])}"
    if actor.get("bow") and actor["bow"] != "none":
        line += f", with a {actor['bow'].replace('-', ' ')} bow"
    if actor.get("facing"):
        line += f", facing {actor['facing'].replace('-', ' ')}"
    gaze = actor.get("gaze")
    if gaze == "forward":
        line += ", looking ahead"
    elif gaze == "downcast":
        line += ", eyes lowered"
    elif gaze:
        line += f", eyes to the {gaze.replace('-', ' ')}"
    if actor.get("holds"):
        line += ", holding " + ", ".join(f"`{h}`" for h in actor["holds"])
    if actor.get("wears_or_carries"):
        line += ", carrying " + ", ".join(
            f"`{h}`" for h in actor["wears_or_carries"]
        )
    if actor.get("gestures"):
        line += ", making the gesture(s) " + ", ".join(
            g.replace("-", " ") for g in actor["gestures"]
        )
    return _wrap(line + ".")


def _object_sentence(item: dict) -> str:
    line = f"`{item['id']}`"
    if item.get("lateral"):
        line += " — " + _place_phrase(
            item["lateral"], item.get("page_side"), item.get("on")
        )
    if item.get("held_by"):
        line += f" — in `{item['held_by']}`'s hands"
    elif item.get("parent"):
        line += f" — carried with `{item['parent']}`"
    if item.get("supported_by"):
        line += f", supported by `{item['supported_by']}`"
        if item.get("support_pitch_deg"):
            line += f" and pitched {item['support_pitch_deg']:g}° toward the priest"
    if item.get("state"):
        line += f". {item['state'].rstrip('.')}"
    if item.get("orientation_immutable"):
        line += (
            ". Its reading orientation is fixed by the contract and is the "
            "same on both sides of the altar: it must not be mirrored, "
            "rotated for composition, or squared toward the camera"
        )
    return _wrap(line + ".")


def _same_depth(actors: list[dict]) -> bool:
    depths = {round(actor["depth"], 6) for actor in actors}
    return len(depths) == 1


RAW_ART_FORBIDDEN = (
    "a title", "a plate identifier", "a caption", "a border", "a header",
    "a footer", "a page number", "a source citation", "metadata",
    "explanatory prose", "an inset", "a diagram",
)

FORBIDDEN_CHANGES = (
    "moving an actor",
    "reassigning an actor's side",
    "changing an actor's facing",
    "changing an actor's posture",
    "moving an object",
    "reorienting an object",
    "mirroring the Missal",
    "reorienting the Missal",
    "changing the camera",
    "changing the framing",
    "changing the number of altar steps",
    "restaging the sanctuary",
    "changing a path or a crossing order",
    "deleting a required visible object",
    "adding a panel that is not declared",
    "generating a title, caption, header or footer",
    "adding an alternate camera",
    "adding a plan or top-view inset",
)


# --------------------------------------------------------------------------
# the prompt
# --------------------------------------------------------------------------
# Deterministic required sections. A prompt missing any of these is not a
# handoff, it is a note, so generation fails rather than shipping one.
PROMPT_SECTIONS = (
    "Project identity",
    "Package inventory",
    "The mandatory edit source",
    "Scene identity",
    "What is visibly true in this scene",
    "What you may improve",
    "What you must not change",
    "Raw art only",
    "Review gates",
    "When to stop",
)

FILE_ROLES = (
    ("render-underlay.png", "mandatory image-edit source; visible geometry authority"),
    ("render-underlay.svg", "the same drawing as vectors"),
    ("render-contract.yaml", "compiled geometry in numbers; review authority"),
    ("skeleton.svg", "diagnostic schematic; never the conditioning image"),
    ("ART-AGENT-INSTRUCTIONS.md", "generated scene-art rules"),
    ("provenance.yaml", "identity, readiness, panel manifest, provenance"),
    ("PACKAGE-MANIFEST.yaml", "package integrity and file roles"),
    ("WEB-AGENT-PROMPT.md", "this prompt"),
)


def _bullets(lines) -> str:
    return "\n".join(f"- {line}" for line in lines)


def render_prompt(contract: dict, provenance: dict, identity: dict,
                  summary: dict, rules: dict) -> str:
    """The whole fresh-web handoff, as one pasteable document."""
    canonical = identity["canonical"]
    plate = contract["plate_id"]
    panels = summary["panels"]
    actors = summary["actors"]
    sanctuary = summary["sanctuary"]

    banner = "" if canonical else (
        "> **NONCANONICAL DEVELOPMENT PACKAGE.** It was generated from a dirty\n"
        "> working tree, so the commit named below does not describe the files\n"
        "> that produced it. Do not use it for a canonical plate.\n\n"
    )

    canary = ""
    if provenance.get("is_pipeline_canary"):
        canary = "\n" + _wrap(
            "**This scene is the pipeline canary.** It is rendered before any "
            "style development begins, and the lane proceeds only once it "
            "reaches STRUCTURE = PASS. If it fails structurally, stop: the "
            "pipeline is what needs diagnosing, not the drawing. Do not go on "
            "to another scene, and do not start a style sheet.",
            indent="",
        ) + "\n"

    same_depth = ""
    if len(actors) > 1 and _same_depth(actors):
        same_depth = "\n" + _wrap(
            f"All {len(actors)} actors stand at the same canonical depth from "
            "the altar. They are level with one another, and none is in front "
            "of another.",
            indent="",
        ) + "\n"

    # A panel whose camera declares no page mapping has none, and the summary
    # must not invent one. Over-the-shoulder and detail views are shot from
    # inside the sanctuary and a plan has no left or right at all.
    unmapped = [
        panel["id"] for panel in panels if panel.get("page_sides") is None
    ]
    page_note = ""
    if unmapped:
        page_note = "\n" + _wrap(
            "The panel(s) " + ", ".join(f"`{p}`" for p in unmapped)
            + " declare no Gospel/Epistle page mapping, so this summary states "
            "world sides for them rather than page sides. Preserve the sides "
            "the underlay already draws; do not reason about page left and "
            "page right for those panels.",
            indent="",
        ) + "\n"

    panel_lines = [
        f"`{panel['id']}` — {panel['projection']}"
        + (f", camera preset `{panel['preset']}`" if panel.get("preset") else "")
        for panel in panels
    ]

    return f"""\
# Artistic rendering handoff — {plate}

{banner}You are the human-guided artistic rendering agent for the Triptych
project. You have been handed a complete rendering package. It is the whole of
your input: everything you need is attached, and nothing outside it may be used
to decide what this picture contains.

## Project identity

- Repository: `{identity['repository']}`
- Branch: `{identity['branch']}`
- Seed commit: `{identity['seed_commit']}`
- Working tree at generation: {identity['worktree']}
- Package status: {'CANONICAL' if canonical else 'NONCANONICAL (development)'}
- Structural baseline commit: `{contract['structural_baseline_commit']}`
- Render-contract version: `{contract['render_contract_version']}`
- Artistic protocol: `{provenance['protocol']}`

Knowing the repository is for provenance and for the next handoff. It is not
permission to go and look at it. Do not browse to reconstruct the choreography,
do not search for alternate scene definitions, do not consult `main`, do not
use historical serving guides, and do not restage from remembered rubrics. The
attached package is the complete rendering input.

## Package inventory

{_bullets(f"`{name}` — {role}" for name, role in FILE_ROLES)}

The authority order is that list. `render-underlay.png` owns what is visible;
`render-contract.yaml` settles numerical questions during review; `skeleton.svg`
is a debugging view and is **never** the image you condition on.

## The mandatory edit source

**EDIT THE ATTACHED `render-underlay.png`. DO NOT CREATE A FRESH COMPOSITION.**

Load `render-underlay.png` into an image EDIT or image-to-image transformation
and render artistic quality onto that exact geometry. Do not use it as loose
inspiration for a text-to-image generation.

**If the available image tool cannot perform an edit using
`render-underlay.png` as the source image, STOP and report that limitation. Do
not substitute fresh generation.** A fresh composition is how the Missal ended
up on the wrong side of the altar twice.

## Scene identity

- Plate: {plate}
- Scene(s): {', '.join(contract['scene_ids'])}
- Title: {contract['title']}
- Readiness: {provenance['art_readiness']}
- Pipeline canary: {'yes' if provenance.get('is_pipeline_canary') else 'no'}
- Declared panels ({len(panels)}): {', '.join(p['id'] for p in panels)}
- Additional panels: {contract['additional_panels']}

{_bullets(panel_lines)}

Draw exactly {len(panels)} panel(s). Adding an inset, a key, a locator, a
vignette or a plan is a structural failure even if it would help.
{canary}
## What is visibly true in this scene

These facts are generated from the compiled contract for this scene. They
describe what the underlay already draws. Your job is to make them beautiful,
not to reconsider them.

### Actors

{_bullets(_actor_sentence(actor) for actor in actors)}
{same_depth}{page_note}
### Sanctuary

- Exactly {sanctuary['step_count']} altar steps and a predella. Do not add,
  remove or merge a step, and do not count the sanctuary floor as a step.
- The actors' levels are named above. Every figure meets the floor or the step
  it is placed on; none of them floats.
- The altar keeps its modelled massing: {', '.join(
    part.replace('_hint', '') for part in sanctuary['altar_parts'])}. Detail may
  be refined inside that massing, but none of it may move.

### Objects

{_bullets(_object_sentence(item) for item in summary['objects'])}

## What you may improve

{_bullets(rules['artist_owns'])}

## What you must not change

These belong to the render contract, not to the artist:

{_bullets(rules['contract_owns'])}

Concretely, every one of the following is a structural failure rather than a
stylistic preference. You must not do any of them:

{_bullets(FORBIDDEN_CHANGES)}

## Raw art only

Return the drawn scene and nothing else. Do not generate {', '.join(
    RAW_ART_FORBIDDEN)}. Publication typography is handled later by the
deterministic publication compositor.

## Review gates

Two independent decisions, reported separately:

    STRUCTURE = PASS | FAIL | PENDING
    ART       = PASS | FAIL | PENDING

STRUCTURE asks whether the plate is faithful to the contract. It checks the
panel count, the camera and projection, actor placement, actor facing, each
actor's floor or step relationship, the sanctuary geometry, the step and
predella geometry, object placement, object orientation, the Missal's
orientation, path and crossing order where the scene has them, the presence of
every required visible object, and the absence of generated page furniture.

ART is asked **only after STRUCTURE passes**: drawing quality, anatomy,
vestments, hands, architecture, graphite technique, tonal hierarchy, clarity
and publication finish.

A plate is approved only when both are PASS. A structural violation is FAIL,
never "approved with notes", however good the drawing is. If STRUCTURE fails,
stop the lane and diagnose the failure before any aesthetic iteration.

## When to stop

Generate exactly one candidate and stop for human review. Do not produce
variants, do not build a style sheet, do not continue to another scene, and do
not approve your own work.

If the package contains a genuine contradiction affecting visible geometry,
stop and report it in this form:

    BLOCKED FOR ART

    Exact ambiguity:
    ...

    Files/fields involved:
    ...

Do not resolve it from your own knowledge, from research, from historical
guides, from another branch, or for visual convenience.
"""


def check_prompt_complete(prompt: str) -> None:
    missing = [name for name in PROMPT_SECTIONS if f"## {name}" not in prompt]
    if missing:
        raise PromptRefused(
            f"the generated prompt is missing required section(s): {missing}"
        )


# --------------------------------------------------------------------------
# package manifest
# --------------------------------------------------------------------------
def package_manifest(package: Path, contract: dict, provenance: dict,
                     identity: dict) -> dict:
    """A machine-readable inventory, so package integrity is auditable."""
    roles = dict(FILE_ROLES)
    files = []
    for path in sorted(package.iterdir()):
        if not path.is_file() or path.name == "PACKAGE-MANIFEST.yaml":
            continue
        files.append({
            "path": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "role": roles.get(path.name, "unclassified"),
        })
    unclassified = [f["path"] for f in files if f["role"] == "unclassified"]
    if unclassified:
        raise PromptRefused(
            f"the package contains file(s) with no declared role: {unclassified}"
        )
    return {
        "schema": "triptych.mass_pictographic.art_seed_package",
        "version": "1.0",
        "package_type": "pictographic-art-seed"
        if identity["canonical"] else "pictographic-art-seed-development",
        "canonical": identity["canonical"],
        "repository": identity["repository"],
        "branch": identity["branch"],
        "seed_commit": identity["seed_commit"],
        "worktree_at_generation": identity["worktree"],
        "plate_id": contract["plate_id"],
        "scene_ids": list(contract["scene_ids"]),
        "structural_baseline_commit": contract["structural_baseline_commit"],
        "render_contract_version": contract["render_contract_version"],
        "art_readiness": provenance["art_readiness"],
        "is_pipeline_canary": provenance["is_pipeline_canary"],
        "mandatory_edit_source": "render-underlay.png",
        "generation_mode": provenance["generation_mode"],
        "web_prompt": "WEB-AGENT-PROMPT.md",
        "panel_manifest": list(provenance["panel_manifest"]),
        "additional_panels": contract["additional_panels"],
        "structure_review": provenance["structure_review"],
        "art_review": provenance["art_review"],
        "files": files,
    }
