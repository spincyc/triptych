#!/usr/bin/env python3
"""Validate the durable v0.21 structural checkpoint and its recovered scene corpus."""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent


def load_yaml(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must have a mapping root")
    return value


def check_manifest() -> int:
    count = 0
    for line in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, relative_path = line.split("  ", 1)
        payload = (ROOT / relative_path).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if actual != digest:
            raise AssertionError(f"checksum mismatch: {relative_path}")
        count += 1
    return count


def check_references(corpus: dict) -> None:
    records = (
        corpus["authoritative_sources"]
        + corpus["current_review_projections"]
        + corpus["historical_review_projections"]
        + [{"path": path} for path in corpus["handoff_records"]]
        + corpus["transport_originals"]
        + corpus["recovered_scene_corpus"]["registry"]
        + corpus["recovered_scene_corpus"]["approved_record"]
        + corpus["recovered_scene_corpus"]["generator"]
    )
    for record in records:
        if not (ROOT / record["path"]).is_file():
            raise AssertionError(f"missing corpus path: {record['path']}")
        for field in ("source", "superseded_by", "original", "canonical_repair"):
            target = record.get(field)
            if target and not (ROOT / target).is_file():
                raise AssertionError(f"missing {field} target: {target}")


def check_transport_repair(corpus: dict) -> None:
    relative_path = "LOW-MASS-END-BRANCHES-1962-v0.1.yaml"
    original = (
        ROOT / "transport-originals" / f"{relative_path}.transport-invalid"
    ).read_text(encoding="utf-8")
    canonical = (ROOT / "sources" / relative_path).read_text(encoding="utf-8")
    bad_line = "  execute_only_when_profile_prescribes_and_no_incompatible_following_function\n"
    good_line = "  execute_only_when_profile_prescribes_and_no_incompatible_following_function: yes\n"
    if original.replace(bad_line, good_line) != canonical:
        raise AssertionError("ending-branches repair is not the documented one-token change")
    transport = corpus["transport_originals"][0]
    actual = hashlib.sha256(original.encode()).hexdigest()
    if transport["sha256"] != actual:
        raise AssertionError("transport-original checksum does not match corpus.yaml")


def check_approved_state(corpus: dict, service: dict, branches: dict) -> None:
    assert corpus["version"] == "0.21"
    assert corpus["status"] == "structural-approved"
    assert corpus["approval"] == "human-approved"
    assert corpus["rite"] == "roman-1962"
    assert corpus["form"] == "low-mass"
    assert corpus["mode"] == "spoken"
    assert corpus["server_count"] == 2
    assert corpus["next_phase"]["status"] == "not-started"
    assert corpus["transport_archive"] == {
        "name": "mass-pictographic-handoff-v0.21.tar.gz",
        "sha256": "62bd1ce90528025b43c8942b51252cbebe6b1ccf4be22324746c84b7aee9cd13",
        "retained_in_git": False,
        "reason": "The archive duplicates the individually retained payloads.",
    }

    assert service["status"] == "structural-approved"
    assert service["ablutions"] == {
        "sole_server": "first_acolyte",
        "first": {"liquid": "wine", "chalice": "on_altar"},
        "second": {
            "liquid": "water",
            "chalice": "held_by_priest",
            "first_acolyte_vertical_move": "down_one_step",
        },
        "second_acolyte_role": "none",
    }
    assert service["post_ablution_transfer"] == {
        "condition": "vessels_cleansed",
        "simultaneous": {
            "first_acolyte": "chalice_cloth_to_gospel_side",
            "second_acolyte": "missal_to_epistle_side",
        },
        "first_crossing_front": "second_acolyte",
        "priest_then_receives_chalice_cloth": True,
        "second_crossing_front": "first_acolyte",
        "end_state": "both_acolytes_kneeling_in_normal_positions",
    }

    assert branches["normal_end"]["dismissal"] == "ite_missa_est"
    assert branches["function_follows_mass"]["dismissal"] == "benedicamus_domino"
    assert branches["requiem"]["dismissal"] == "requiescant_in_pace"
    assert not any("gloria" in key.lower() for key in branches)
    assert branches["leonine_prayers"][
        "execute_only_when_profile_prescribes_and_no_incompatible_following_function"
    ] is True


def check_handoff_invariants() -> None:
    summary = (ROOT / "handoff/HANDOFF-SUMMARY.md").read_text(encoding="utf-8")
    normalized = " ".join(summary.replace("**", "").split())
    required = (
        "spoken 1962 Roman Low Mass with two servers",
        "Acolyte 1 (Epistle-side acolyte) moves the missal to the Gospel side",
        "Acolyte 2 moves the missal back to the Epistle side after the vessels have been cleansed",
        "priest reads facing left",
        "1 ring at first genuflection, 1 ring at elevation, 1 ring at second genuflection",
        'Acolyte 1 rings once at each of the three priestly "Domine, non sum dignus" openings',
        "Acolyte 1 alone performs the ablution service",
        "Acolyte 2 does not assist in the ablutions",
        "On the first crossing, Acolyte 2 is in front",
        "this time with Acolyte 1 in front",
        "dismissal is not chosen based on whether the Gloria was said",
    )
    for fragment in required:
        if fragment not in normalized:
            raise AssertionError(f"approved handoff invariant missing: {fragment}")


def check_svg_scene_ids(corpus: dict) -> None:
    source = next(
        record
        for record in corpus["authoritative_sources"]
        if record["kind"] == "deterministic-structural-storyboard"
    )
    svg_path = ROOT / source["path"]
    ET.parse(svg_path)
    text = svg_path.read_text(encoding="utf-8")
    actual: set[str] = set()
    for match in re.finditer(r"(LM-\d{3})([A-Z])(?:/([A-Z]))?", text):
        base, first, second = match.groups()
        actual.add(base + first)
        if second:
            actual.add(base + second)
    expected = set(source["scene_ids"])
    if actual != expected:
        raise AssertionError(
            f"SVG scene IDs differ: expected={sorted(expected)} actual={sorted(actual)}"
        )
    projection = next(
        record
        for record in corpus["current_review_projections"]
        if record.get("source") == source["path"]
    )
    if set(projection["scene_ids"]) != expected:
        raise AssertionError("SVG and current raster projection scene IDs differ")



# --------------------------------------------------------------------------
# Recovered scene corpus (scenes/). See scenes/schema.md for the contract.
# --------------------------------------------------------------------------

SCENES = ROOT / "scenes"


def load_vocabularies() -> dict[str, set[str]]:
    """Read the controlled vocabularies out of scenes/schema.md.

    schema.md is the single source of truth: each entry runs from its bolded
    name to the next blank line, and every backticked token in it is a value.
    """
    text = (SCENES / "schema.md").read_text(encoding="utf-8")
    body = text.split("## Controlled vocabularies", 1)[1]
    body = body.split("## Rules the validator", 1)[0]
    vocab: dict[str, set[str]] = {}
    for block in body.split("\n\n"):
        match = re.match(r"\*\*([a-z ]+)\*\*", block.strip())
        if match:
            vocab[match.group(1).strip()] = set(re.findall(r"`([^`]+)`", block))
    expected = {
        "kind", "voice", "posture", "bow", "facing", "gaze", "hand state",
        "gesture", "object id", "orientation",
    }
    missing = expected - set(vocab)
    if missing:
        raise AssertionError(f"schema.md is missing vocabularies: {sorted(missing)}")
    return vocab


def load_scene_corpus() -> tuple[dict, dict, dict, dict, list[dict], dict[str, str]]:
    inventory = load_yaml("scenes/inventory.yaml")
    geometry = load_yaml("scenes/geometry.yaml")
    invariants = load_yaml("scenes/invariants.yaml")
    conditions = load_yaml("scenes/conditions.yaml")
    scenes: list[dict] = []
    origin: dict[str, str] = {}
    for section in inventory["sections"]:
        relative = f"scenes/{section['file']}"
        document = load_yaml(relative)
        if document["section"]["id"] != section["id"]:
            raise AssertionError(f"{relative} declares the wrong section id")
        for scene in document["scenes"]:
            scenes.append(scene)
            origin[scene["scene_id"]] = relative
    return inventory, geometry, invariants, conditions, scenes, origin


def check_scene_registry(inventory: dict, scenes: list[dict], origin: dict) -> None:
    """Rules 1 and 2: the inventory and the section files agree exactly."""
    rows = {row["scene_id"]: row for row in inventory["scenes"]}
    if len(rows) != len(inventory["scenes"]):
        raise AssertionError("inventory.yaml repeats a scene id")
    seen: set[str] = set()
    for scene in scenes:
        scene_id = scene["scene_id"]
        if scene_id in seen:
            raise AssertionError(f"scene {scene_id} is implemented twice")
        seen.add(scene_id)
        row = rows.get(scene_id)
        if row is None:
            raise AssertionError(f"scene {scene_id} is not in inventory.yaml")
        if origin[scene_id] != f"scenes/{row['file']}":
            raise AssertionError(f"scene {scene_id} lives in the wrong section file")
        for field in ("order", "cluster", "title", "condition", "predecessor",
                      "successor", "bypass_successor"):
            if field == "bypass_successor" and field not in row:
                if scene.get(field) is not None:
                    raise AssertionError(f"{scene_id} declares an unexpected bypass_successor")
                continue
            if scene.get(field) != row.get(field):
                raise AssertionError(
                    f"{scene_id}.{field} is {scene.get(field)!r}, "
                    f"inventory.yaml says {row.get(field)!r}"
                )
    unimplemented = set(rows) - seen
    if unimplemented:
        raise AssertionError(f"inventory scenes with no record: {sorted(unimplemented)}")

    orders = sorted(row["order"] for row in inventory["scenes"])
    if orders != list(range(1, len(orders) + 1)):
        raise AssertionError("inventory order is not dense and 1-based")
    coverage = inventory["coverage"]
    ordered = sorted(inventory["scenes"], key=lambda row: row["order"])
    if coverage["scene_count"] != len(ordered):
        raise AssertionError("coverage.scene_count disagrees with the registry")
    if coverage["first_scene"] != ordered[0]["scene_id"]:
        raise AssertionError("coverage.first_scene disagrees with the registry")
    if coverage["last_scene"] != ordered[-1]["scene_id"]:
        raise AssertionError("coverage.last_scene disagrees with the registry")


def check_scene_order(inventory: dict) -> None:
    """Rules 3 and 4: one coherent chain, and every branch reconnects."""
    ordered = sorted(inventory["scenes"], key=lambda row: row["order"])
    ids = [row["scene_id"] for row in ordered]
    position = {scene_id: index for index, scene_id in enumerate(ids)}
    for index, row in enumerate(ordered):
        expected_predecessor = ids[index - 1] if index else None
        expected_successor = ids[index + 1] if index + 1 < len(ids) else None
        if row["predecessor"] != expected_predecessor:
            raise AssertionError(f"{row['scene_id']} has a broken predecessor link")
        if row["successor"] != expected_successor:
            raise AssertionError(f"{row['scene_id']} has a broken successor link")

    blocks: list[tuple[int, int]] = []
    start = None
    for index, row in enumerate(ordered):
        conditional = row["condition"] != "ALWAYS"
        if conditional and start is None:
            start = index
        if not conditional and start is not None:
            blocks.append((start, index - 1))
            start = None
    if start is not None:
        blocks.append((start, len(ordered) - 1))
    for first, last in blocks:
        if first == 0:
            raise AssertionError("a conditional block cannot open the corpus")
        gate = ordered[first - 1]
        resume = ordered[last + 1]["scene_id"] if last + 1 < len(ordered) else None
        if gate.get("bypass_successor") != resume:
            raise AssertionError(
                f"the conditional block at {ordered[first]['scene_id']} does not "
                f"reconnect: {gate['scene_id']}.bypass_successor is "
                f"{gate.get('bypass_successor')!r}, expected {resume!r}"
            )
    declared = {row["scene_id"] for row in ordered if row.get("bypass_successor")}
    gates = {ordered[first - 1]["scene_id"] for first, _ in blocks}
    if declared != gates:
        raise AssertionError(f"stray bypass_successor on {sorted(declared - gates)}")


def cluster_in_range(cluster: str, span: str) -> bool:
    if ".." in span:
        low, high = span.split("..")
        return low <= cluster <= high
    return cluster == span


def check_scene_records(geometry: dict, invariants: dict, conditions: dict,
                        scenes: list[dict], vocab: dict[str, set[str]]) -> None:
    """Rules 5 to 9: every value resolves and every scene is drawable."""
    anchors = {anchor["id"] for anchor in geometry["anchors"]}
    mensa = {position["id"] for position in geometry["mensa_positions"]["positions"]}
    views = {viewpoint["id"] for viewpoint in geometry["viewpoints"]}
    condition_ids = {condition["id"] for condition in conditions["conditions"]}
    ranges = {rule["id"]: rule["applies_to"] for rule in invariants["invariants"]}
    actors_expected = ["priest", "AC1", "AC2"]

    for scene in scenes:
        scene_id = scene["scene_id"]

        def bad(message: str) -> AssertionError:
            return AssertionError(f"{scene_id}: {message}")

        if scene["kind"] not in vocab["kind"]:
            raise bad(f"unknown kind {scene['kind']!r}")
        if scene["voice"] not in vocab["voice"]:
            raise bad(f"unknown voice {scene['voice']!r}")
        if scene["condition"] not in condition_ids:
            raise bad(f"unknown condition {scene['condition']!r}")
        if scene["camera"]["view"] not in views:
            raise bad(f"unknown camera view {scene['camera']['view']!r}")

        if [actor["id"] for actor in scene["actors"]] != actors_expected:
            raise bad("must list priest, AC1 and AC2 exactly once, in that order")
        for actor in scene["actors"]:
            where = f"actor {actor['id']}"
            if actor["anchor"] not in anchors:
                raise bad(f"{where}: unknown anchor {actor['anchor']!r}")
            if actor["side"] not in {"gospel", "centre", "epistle"}:
                raise bad(f"{where}: unknown side {actor['side']!r}")
            if actor["posture"] not in vocab["posture"]:
                raise bad(f"{where}: unknown posture {actor['posture']!r}")
            if actor["bow"] not in vocab["bow"]:
                raise bad(f"{where}: unknown bow {actor['bow']!r}")
            if actor["facing"] not in vocab["facing"]:
                raise bad(f"{where}: unknown facing {actor['facing']!r}")
            if actor["gaze"] not in vocab["gaze"]:
                raise bad(f"{where}: unknown gaze {actor['gaze']!r}")
            for hand in ("left", "right"):
                state = actor["hands"][hand]
                if state not in vocab["hand state"]:
                    raise bad(f"{where}: unknown {hand} hand state {state!r}")
            for gesture in actor.get("gestures") or []:
                if gesture not in vocab["gesture"]:
                    raise bad(f"{where}: unknown gesture {gesture!r}")
            path = actor.get("path")
            if path:
                for end in ("from", "to"):
                    if path.get(end) and path[end] not in anchors:
                        raise bad(f"{where}: unknown path {end} {path[end]!r}")
                for step in path.get("via") or []:
                    if step not in anchors:
                        raise bad(f"{where}: unknown path step {step!r}")

        for item in scene.get("objects") or []:
            if item["id"] not in vocab["object id"]:
                raise bad(f"unknown object id {item['id']!r}")
            orientation = item.get("orientation")
            if orientation is not None and orientation not in vocab["orientation"]:
                raise bad(f"unknown orientation {orientation!r}")
            placement = item["placement"]
            if isinstance(placement, str) and " " not in placement:
                if placement not in anchors | mensa:
                    raise bad(f"unknown object placement {placement!r}")
            if item["handled_by"] not in {"priest", "AC1", "AC2", "both-acolytes", "none"}:
                raise bad(f"unknown handled_by {item['handled_by']!r}")

        if not scene["invariants"]:
            raise bad("cites no invariant")
        for rule in scene["invariants"]:
            if rule not in ranges:
                raise bad(f"unknown invariant {rule!r}")
            spans = ranges[rule]
            if not any(cluster_in_range(scene["cluster"], span) for span in spans):
                raise bad(f"cites {rule}, which does not govern {scene['cluster']}")

        for variant in scene.get("variants") or []:
            if variant.get("baseline") is not False:
                raise bad(f"variant {variant.get('id')!r} must set baseline: false")

        depth_of = {anchor["id"]: anchor["y"] for anchor in geometry["anchors"]}
        for one in scene["actors"]:
            for other in scene["actors"]:
                y_one, y_other = depth_of[one["anchor"]], depth_of[other["anchor"]]
                if y_one < y_other and one["depth_rank"] >= other["depth_rank"]:
                    raise bad(
                        f"{one['id']} stands nearer the viewer than {other['id']} "
                        "but does not take the smaller depth_rank"
                    )

        if "INV-POS-01" in scene["invariants"]:
            depths = {actor["depth_rank"] for actor in scene["actors"]}
            if len(depths) != 1:
                raise bad("INV-POS-01 requires all three actors at the same depth")

        for item in scene.get("objects") or []:
            if item["id"] == "missal" and item.get("orientation") not in (
                None, "priest-reads-facing-left", "not-applicable"
            ):
                raise bad(
                    "the Missal is always oriented so the priest reads facing left"
                )


def check_named_contradictions(scenes: list[dict]) -> None:
    """Rule 10: refuse every stale contradiction the invariants reject."""
    by_id = {scene["scene_id"]: scene for scene in scenes}

    def actor(scene: dict, actor_id: str) -> dict:
        return next(a for a in scene["actors"] if a["id"] == actor_id)

    def rings(scene: dict, actor_id: str) -> int:
        """Rings by one actor. A null count means the serving profile fixes it."""
        return sum(
            bell.get("count") or 0
            for bell in scene.get("bells") or []
            if bell.get("actor") == actor_id
        )

    def handlers(scene: dict, object_id: str) -> set[str]:
        return {
            item["handled_by"]
            for item in scene.get("objects") or []
            if item["id"] == object_id
        }

    # Missal transfer roles.
    for scene in scenes:
        if "LM-029" <= scene["cluster"] <= "LM-035":
            if "AC2" in handlers(scene, "missal"):
                raise AssertionError(
                    f"{scene['scene_id']}: AC2 must not move the Missal before the Gospel"
                )
        if scene["cluster"] == "LM-136":
            if "AC1" in handlers(scene, "missal"):
                raise AssertionError(
                    f"{scene['scene_id']}: AC1 must not move the Missal after the ablutions"
                )

    # AC1-only post-Communion ablutions.
    for scene_id in ("LM-136A", "LM-136B"):
        scene = by_id[scene_id]
        for object_id in ("wine-cruet", "water-cruet"):
            if "AC2" in handlers(scene, object_id):
                raise AssertionError(
                    f"{scene_id}: AC2 must not serve the post-Communion ablutions"
                )
        if by_id["LM-136A"].get("objects") and not any(
            item["id"] == "wine-cruet" for item in by_id["LM-136A"]["objects"]
        ):
            raise AssertionError("LM-136A: the first ablution is of wine")
    if not any(item["id"] == "water-cruet" for item in by_id["LM-136B"]["objects"]):
        raise AssertionError("LM-136B: the second ablution is of water")

    # Coordinated crossing order: the acolyte in front is nearer the viewer.
    first = by_id["LM-136C"]
    if actor(first, "AC2")["depth_rank"] >= actor(first, "AC1")["depth_rank"]:
        raise AssertionError("LM-136C: AC2 is in front on the first crossing")
    second = by_id["LM-136E"]
    if actor(second, "AC1")["depth_rank"] >= actor(second, "AC2")["depth_rank"]:
        raise AssertionError("LM-136E: AC1 is in front on the second crossing")

    # Consecration bell profile: one ring at each of the six cues, AC1 only.
    for scene_id in ("LM-098A", "LM-099A", "LM-100A", "LM-103A", "LM-103B", "LM-103C"):
        scene = by_id[scene_id]
        if rings(scene, "AC1") != 1:
            raise AssertionError(
                f"{scene_id}: the spoken Low Mass baseline rings once here, "
                "not three times at the elevation"
            )
        if rings(scene, "AC2"):
            raise AssertionError(f"{scene_id}: AC1 is the bell operator, not AC2")

    # Three Domine, non sum dignus rings.
    if rings(by_id["LM-134C"], "AC1") != 3:
        raise AssertionError(
            "LM-134C: AC1 rings once at each of the three priestly "
            "'Domine, non sum dignus' openings"
        )

    # No baseline bell at the minor elevation.
    if by_id["LM-112C"].get("bells"):
        raise AssertionError(
            "LM-112C: a bell at the minor elevation is not the canonical baseline"
        )

    # Only AC1 assists the ascent.
    def raises_hem(scene: dict, actor_id: str) -> bool:
        person = actor(scene, actor_id)
        hands = person["hands"]
        return "raising-alb-hem" in (
            set(person.get("gestures") or []) | {hands["left"], hands["right"]}
        )

    ascent = by_id["LM-013B"]
    if raises_hem(ascent, "AC2"):
        raise AssertionError("LM-013B: only AC1 assists the priest's ascent")
    if not raises_hem(ascent, "AC1"):
        raise AssertionError("LM-013B: AC1 gives the approved ascent assistance")

    # All three sign themselves at the Indulgentiam.
    indulgentiam = by_id["LM-010A"]
    for actor_id in ("priest", "AC1", "AC2"):
        if "sign-of-the-cross" not in (actor(indulgentiam, actor_id).get("gestures") or []):
            raise AssertionError(
                "LM-010A: the priest and both servers sign themselves at the Indulgentiam"
            )

    # The Gloria in excelsis is said at the centre.
    for scene_id in ("LM-022A", "LM-022B", "LM-023A", "LM-024A"):
        if actor(by_id[scene_id], "priest")["side"] != "centre":
            raise AssertionError(
                f"{scene_id}: the Gloria in excelsis is said at the centre, not at the Missal"
            )

    # The corporal is never unfolded at the Offertory.
    for scene in scenes:
        if not ("LM-054" <= scene["cluster"] <= "LM-078"):
            continue
        for item in scene.get("objects") or []:
            if item["id"] != "corporal":
                continue
            if item["handled_by"] != "none":
                raise AssertionError(
                    f"{scene['scene_id']}: the corporal is already unfolded from the "
                    "beginning of Mass and is not handled at the Offertory"
                )

    # The dismissal is not selected by whether the Gloria was said.
    dismissal = by_id["LM-138B"]
    blob = yaml.safe_dump(dismissal).lower()
    for variant in dismissal.get("variants") or []:
        if "gloria" in str(variant.get("applies_when", "")).lower():
            raise AssertionError(
                "LM-138B: the 1962 dismissal is not conditioned on the Gloria"
            )
    if "gloria" in blob and "not" not in blob:
        raise AssertionError("LM-138B: unqualified Gloria reference in the dismissal")


AUTHORED_TREES = ("scenes", "recovery", "storyboards")
AUTHORED_FILES = ("render-storyboards.py",)


def authored_paths() -> set[str]:
    """Every repository-authored file of the recovery layer."""
    paths = {name for name in AUTHORED_FILES}
    for tree in AUTHORED_TREES:
        paths |= {
            str(path.relative_to(ROOT))
            for path in (ROOT / tree).rglob("*")
            if path.is_file()
        }
    return paths


def check_authored_manifest() -> int:
    """Hash the authored layer, and prove the manifest covers all of it.

    This is deliberately separate from MANIFEST.sha256, which covers the
    supplied transport payloads. Keeping the two apart is what preserves the
    distinction between what was approved and supplied and what was written
    here; see recovery/recovery-notes.md.
    """
    count = 0
    listed = set()
    for line in (ROOT / "MANIFEST-AUTHORED.sha256").read_text(
        encoding="utf-8"
    ).splitlines():
        digest, relative_path = line.split("  ", 1)
        payload = (ROOT / relative_path).read_bytes()
        if hashlib.sha256(payload).hexdigest() != digest:
            raise AssertionError(f"authored corpus checksum mismatch: {relative_path}")
        listed.add(relative_path)
        count += 1
    tracked = authored_paths()
    if tracked != listed:
        raise AssertionError(
            f"MANIFEST-AUTHORED.sha256 does not cover the authored layer: "
            f"missing={sorted(tracked - listed)} stale={sorted(listed - tracked)}"
        )
    return count


def check_storyboards(inventory: dict) -> int:
    directory = ROOT / "storyboards"
    files = sorted(directory.glob("*.svg"))
    if not files:
        raise AssertionError("no recovered storyboards found")
    sections = {section["id"] for section in inventory["sections"]}
    for path in files:
        ET.parse(path)
        stem = path.stem.rsplit("-v", 1)[0]
        if stem not in sections:
            raise AssertionError(f"storyboard {path.name} names no known section")
    covered = {path.stem.rsplit("-v", 1)[0] for path in files}
    if covered != sections:
        raise AssertionError(
            f"storyboard coverage gap: {sorted(sections - covered)}"
        )
    return len(files)


def check_scene_corpus() -> tuple[int, int, int]:
    vocab = load_vocabularies()
    inventory, geometry, invariants, conditions, scenes, origin = load_scene_corpus()
    check_scene_registry(inventory, scenes, origin)
    check_scene_order(inventory)
    check_scene_records(geometry, invariants, conditions, scenes, vocab)
    check_named_contradictions(scenes)
    hashed = check_authored_manifest()
    boards = check_storyboards(inventory)
    return len(scenes), hashed, boards


def main() -> None:
    corpus = load_yaml("corpus.yaml")
    service = load_yaml("sources/ABLUTIONS-AND-COORDINATED-TRANSFER-v0.2.yaml")
    branches = load_yaml("sources/LOW-MASS-END-BRANCHES-1962-v0.1.yaml")
    check_references(corpus)
    check_transport_repair(corpus)
    check_approved_state(corpus, service, branches)
    check_handoff_invariants()
    check_svg_scene_ids(corpus)
    count = check_manifest()
    scenes, hashed, boards = check_scene_corpus()
    print(f"PASS: v0.21 corpus ({count} checksummed retained assets)")
    print(
        f"PASS: recovered scene corpus ({scenes} scenes, "
        f"{hashed} checksummed authored files, {boards} storyboards)"
    )


if __name__ == "__main__":
    main()
