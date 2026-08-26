#!/usr/bin/env python3
"""Validate the durable v0.21 structural checkpoint."""

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
    print(f"PASS: v0.21 corpus ({count} checksummed retained assets)")


if __name__ == "__main__":
    main()
