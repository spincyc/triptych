#!/usr/bin/env python3
"""Regression checks for the fresh-web art-seed handoff.

The gap these come from was operational rather than geometric. `art-seed`
emitted a technically complete art package and a human then wrote, from memory,
the prompt that carried it into a fresh web conversation. That prompt has to
state the repository, the exact commit, the scene's readiness and panel
manifest, which file is the mandatory edit source, and what is visibly true in
this particular scene. Written by hand it was rewritten every time, and a
prompt nobody can diff is a prompt nobody reviewed.

So the prompt is generated, and these tests hold the properties that make a
generated prompt worth more than a remembered one: that its facts come from the
scene rather than from a template, that it binds to a real commit, that it says
the same thing twice running, and that a package which cannot honour all of
that is never written at all.
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "pictographic"
DICTIONARY = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
)
LAYER = DICTIONARY / "render-contract/low-mass/v1"
CONTRACTS = LAYER / "contracts"
PROTOCOL = DICTIONARY / "artistic/RENDERING-PROTOCOL.md"

CALENDAR, FORM = "roman-1962", "low-mass"

# The pipeline canary.
CANARY = "LM-001A"
# A second art-ready scene, chosen to share as little as possible with the
# canary: a different camera preset (which declares no page mapping at all),
# nine objects instead of four, the Missal on the Gospel side, and an object in
# the priest's hands.
SECOND = "LM-060A"
# The only art-ready scene that is both seedable and multi-panel, and it also
# carries the Missal in a server's hands rather than on the mensa.
MULTI_PANEL = "LM-032B"
# Blocked, with a single short cue.
BLOCKED = "LM-128A"

PACKAGE_FILES = (
    "WEB-AGENT-PROMPT.md",
    "ART-AGENT-INSTRUCTIONS.md",
    "PACKAGE-MANIFEST.yaml",
    "render-underlay.png",
    "render-underlay.svg",
    "render-contract.yaml",
    "skeleton.svg",
    "provenance.yaml",
)


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def seed(scene: str, out: Path, development: bool = True):
    """Run the canonical CLI, which is the thing an operator actually types."""
    command = [
        sys.executable, str(CLI), "art-seed", CALENDAR, FORM, scene,
        "--out", str(out),
    ]
    if development:
        command.append("--development")
    return subprocess.run(command, capture_output=True, text=True, cwd=ROOT)


class PackageShapeTests(unittest.TestCase):
    """The package is the whole handoff, or it is not a handoff."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.result = seed(CANARY, cls.tmp)
        if cls.result.returncode != 0:
            raise AssertionError(cls.result.stdout + cls.result.stderr)
        cls.package = cls.tmp / CANARY
        cls.prompt = (cls.package / "WEB-AGENT-PROMPT.md").read_text(
            encoding="utf-8"
        )
        cls.manifest = load(cls.package / "PACKAGE-MANIFEST.yaml")
        cls.provenance = load(cls.package / "provenance.yaml")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_declared_file_is_present_and_not_empty(self):
        for name in PACKAGE_FILES:
            with self.subTest(file=name):
                path = self.package / name
                self.assertTrue(path.is_file(), f"{name} is missing")
                self.assertGreater(path.stat().st_size, 0, f"{name} is empty")

    def test_the_package_holds_nothing_undeclared(self):
        """A file nobody gave a role to is a file nobody reviewed."""
        present = {p.name for p in self.package.iterdir()}
        self.assertEqual(present, set(PACKAGE_FILES))

    def test_the_manifest_checksums_every_other_file(self):
        import hashlib

        listed = {row["path"]: row["sha256"] for row in self.manifest["files"]}
        self.assertEqual(
            set(listed), set(PACKAGE_FILES) - {"PACKAGE-MANIFEST.yaml"},
            "the manifest and the package disagree about what is in it",
        )
        for name, digest in listed.items():
            with self.subTest(file=name):
                actual = hashlib.sha256(
                    (self.package / name).read_bytes()
                ).hexdigest()
                self.assertEqual(actual, digest, f"{name} does not match")

    def test_no_file_carries_an_unclassified_role(self):
        for row in self.manifest["files"]:
            self.assertNotEqual(row["role"], "unclassified", row["path"])

    def test_neither_review_gate_is_pre_approved(self):
        for field in ("structure_review", "art_review"):
            self.assertEqual(self.manifest[field], "PENDING")
            self.assertEqual(self.provenance[field], "PENDING")

    def test_the_manifest_names_the_edit_source_and_the_prompt(self):
        self.assertEqual(
            self.manifest["mandatory_edit_source"], "render-underlay.png"
        )
        self.assertEqual(self.manifest["web_prompt"], "WEB-AGENT-PROMPT.md")
        self.assertEqual(self.manifest["generation_mode"], "image-edit")


class CanaryPromptTests(unittest.TestCase):
    """The canary's prompt must state the canary's facts."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        result = seed(CANARY, cls.tmp)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        cls.prompt = (cls.tmp / CANARY / "WEB-AGENT-PROMPT.md").read_text(
            encoding="utf-8"
        )
        cls.contract = load(CONTRACTS / f"{CANARY}.yaml")
        # The prompt is wrapped for a human to read, so a phrase can straddle a
        # line break. Phrase assertions run against the unwrapped text; the
        # ones that care about layout use the raw prompt.
        cls.flat = " ".join(cls.prompt.split())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def assertPrompt(self, pattern, message):
        self.assertRegex(self.flat, pattern, message)

    def test_it_identifies_the_project_and_the_repository(self):
        self.assertIn("Triptych", self.prompt)
        self.assertIn("spincyc/triptych", self.prompt)
        self.assertIn("feature/pictographic", self.prompt)

    def test_it_names_the_exact_current_commit(self):
        """Not a literal in a template: the commit this checkout is on."""
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True,
        ).stdout.strip()
        self.assertIn(head, self.prompt)

    def test_it_states_scene_identity_from_the_contract(self):
        self.assertIn(CANARY, self.prompt)
        self.assertIn(self.contract["title"], self.prompt)
        self.assertIn("Readiness: ready", self.prompt)
        self.assertIn("Pipeline canary: yes", self.prompt)
        self.assertIn("Declared panels (1): primary", self.prompt)
        self.assertIn("Additional panels: forbidden", self.prompt)
        self.assertIn(self.contract["structural_baseline_commit"], self.prompt)

    def test_it_makes_the_edit_source_unmistakable(self):
        self.assertIn(
            "**EDIT THE ATTACHED `render-underlay.png`. DO NOT CREATE A FRESH "
            "COMPOSITION.**",
            self.flat,
        )
        self.assertPrompt(
            r"cannot perform an edit using `render-underlay\.png`.{0,60}STOP",
            "the prompt does not fail closed when the tool cannot edit",
        )
        self.assertIn("Do not substitute fresh generation", self.flat)

    def test_the_skeleton_is_never_offered_as_the_conditioning_image(self):
        self.assertPrompt(
            r"`skeleton\.svg`[^\n]*never the conditioning image",
            "skeleton.svg is not marked as diagnostic-only",
        )

    def test_it_places_each_actor_on_its_own_side_and_level(self):
        for actor, side in (
            ("AC2", "Gospel side (page left)"),
            ("AC1", "Epistle side (page right)"),
        ):
            with self.subTest(actor=actor):
                self.assertPrompt(
                    rf"`{actor}`[^`]*{re.escape(side)}",
                    f"{actor} is not placed on {side}",
                )
        self.assertPrompt(
            r"`priest`[^`]*the centreline",
            "the priest is not placed on the centreline",
        )
        self.assertEqual(
            self.flat.count("in plano on the sanctuary floor"), 3,
            "not all three actors are stated to stand in plano",
        )

    def test_it_states_the_actors_share_one_depth(self):
        self.assertIn("same canonical depth", self.prompt)

    def test_it_states_the_sanctuary_step_count(self):
        self.assertIn("Exactly 3 altar steps and a predella", self.prompt)

    def test_it_states_the_missal_side_support_and_immutability(self):
        missal = re.search(r"- `missal`.*?(?= - `| ## )", self.flat)
        self.assertIsNotNone(missal, "the Missal is not described at all")
        text = missal.group(0)
        self.assertIn("Epistle side (page right)", text)
        self.assertIn("missal-stand", text)
        self.assertIn("pitched 24", text)
        self.assertIn("must not be mirrored", text)
        self.assertIn("squared toward the camera", text)

    def test_it_carries_the_raw_art_rule(self):
        self.assertIn("Raw art only", self.prompt)
        for banned in ("a title", "a caption", "a border", "a page number"):
            self.assertIn(banned, self.prompt)
        self.assertIn("publication compositor", self.prompt)

    def test_it_carries_both_gates_in_order(self):
        self.assertIn("STRUCTURE = PASS | FAIL | PENDING", self.prompt)
        self.assertIn("ART       = PASS | FAIL | PENDING", self.prompt)
        self.assertIn("only after STRUCTURE passes", self.prompt)
        self.assertIn("stop the lane", self.prompt)

    def test_it_stops_at_one_candidate(self):
        self.assertIn(
            "Generate exactly one candidate and stop for human review",
            self.prompt,
        )
        self.assertIn("BLOCKED FOR ART", self.prompt)

    def test_it_forbids_reconstructing_the_scene_from_outside(self):
        for clause in ("do not consult `main`", "historical serving guides",
                       "Do not browse"):
            self.assertIn(clause, self.prompt)


class SecondSceneTests(unittest.TestCase):
    """A second scene must get its own facts, not the canary's."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        result = seed(SECOND, cls.tmp)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        cls.prompt = (cls.tmp / SECOND / "WEB-AGENT-PROMPT.md").read_text(
            encoding="utf-8"
        )
        cls.contract = load(CONTRACTS / f"{SECOND}.yaml")
        cls.canary_contract = load(CONTRACTS / f"{CANARY}.yaml")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_canary_paragraph_is_absent(self):
        self.assertIn("Pipeline canary: no", self.prompt)
        self.assertNotIn("This scene is the pipeline canary", self.prompt)

    def test_no_canary_facts_leak_in(self):
        self.assertNotIn(CANARY, self.prompt)
        self.assertNotIn(self.canary_contract["title"], self.prompt)

    def test_its_own_identity_is_used(self):
        self.assertIn(SECOND, self.prompt)
        self.assertIn(self.contract["title"], self.prompt)

    def test_the_object_summary_comes_from_this_scene(self):
        described = set(re.findall(r"^- `([a-z-]+)`", self.prompt, re.M))
        placed = {
            item["id"] for item in self.contract["objects"]
            if item.get("visible") is not False
            and (item.get("position") is not None or item.get("handled_by")
                 not in (None, "none"))
        }
        self.assertTrue(
            placed <= described,
            f"objects {sorted(placed - described)} are placed but not described",
        )

    def test_a_panel_without_a_declared_page_mapping_says_so(self):
        """Honesty about what the contract does not state.

        An over-the-shoulder camera declares no page-right direction, so the
        summary has no Gospel/Epistle page mapping to offer and must not invent
        one. Saying "page left" there would be a guess presented as geometry.
        """
        frames = [
            (panel["camera"].get("frame") or {}).get(
                "page_right_world_direction"
            )
            for panel in self.contract["panels"]
        ]
        self.assertTrue(
            any(frame is None for frame in frames),
            f"{SECOND} no longer exercises the undeclared-page-mapping path",
        )
        self.assertIn("declare no Gospel/Epistle page mapping", self.prompt)
        self.assertNotIn("(page left)", self.prompt)
        self.assertNotIn("(page right)", self.prompt)


class MultiPanelTests(unittest.TestCase):
    """Panel count comes from the scene, never from an assumption."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        result = seed(MULTI_PANEL, cls.tmp)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        cls.prompt = (cls.tmp / MULTI_PANEL / "WEB-AGENT-PROMPT.md").read_text(
            encoding="utf-8"
        )
        cls.manifest = load(cls.tmp / MULTI_PANEL / "PACKAGE-MANIFEST.yaml")
        cls.contract = load(CONTRACTS / f"{MULTI_PANEL}.yaml")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_scene_really_has_more_than_one_panel(self):
        self.assertGreater(
            len(self.contract["panels"]), 1,
            f"{MULTI_PANEL} no longer exercises the multi-panel path",
        )

    def test_every_declared_panel_is_named(self):
        ids = [panel["id"] for panel in self.contract["panels"]]
        self.assertIn(f"Declared panels ({len(ids)}): {', '.join(ids)}",
                      self.prompt)
        for panel_id in ids:
            with self.subTest(panel=panel_id):
                self.assertIn(f"`{panel_id}`", self.prompt)
        self.assertEqual(self.manifest["panel_manifest"], ids)

    def test_the_draw_instruction_counts_the_real_panels(self):
        self.assertIn(
            f"Draw exactly {len(self.contract['panels'])} panel(s)", self.prompt
        )

    def test_the_additional_panel_policy_is_the_contracts(self):
        self.assertIn(
            f"Additional panels: {self.contract['additional_panels']}",
            self.prompt,
        )

    def test_an_object_in_a_servers_hands_is_still_described(self):
        """The object most easily lost, and the one most easily misdrawn.

        A carried object has no compiled position, so a summary keyed on
        position alone drops it — and an undescribed Missal may be drawn
        anywhere at all.
        """
        held = [
            item for item in self.contract["objects"]
            if item.get("position") is None
            and item.get("handled_by") not in (None, "none")
        ]
        self.assertTrue(held, f"{MULTI_PANEL} carries nothing by hand any more")
        for item in held:
            with self.subTest(item=item["id"]):
                self.assertRegex(
                    self.prompt,
                    rf"- `{item['id']}`[^\n]*(\n\s+)?[^\n]*"
                    rf"`{item['handled_by']}`",
                    f"{item['id']} is not described as held by "
                    f"{item['handled_by']}",
                )


class BlockedSceneTests(unittest.TestCase):
    """A blocked scene produces a refusal and no attachable package."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_the_scene_is_still_blocked(self):
        contract = load(CONTRACTS / f"{BLOCKED}.yaml")
        self.assertNotEqual(contract["art_readiness"]["status"], "ready")

    def test_it_exits_nonzero_and_quotes_the_blocker(self):
        result = seed(BLOCKED, self.tmp)
        self.assertNotEqual(result.returncode, 0)
        cue = load(CONTRACTS / f"{BLOCKED}.yaml")["blocked_cues"][0]
        self.assertIn(cue, result.stderr)

    def test_the_scene_refusal_outranks_the_working_tree(self):
        """Which refusal an operator is shown, when more than one applies.

        A blocked scene seeded from a dirty tree has two problems. The one that
        matters is the blocked scene: it is a statement about the liturgy that
        somebody has to resolve by review. Reporting the working tree instead
        hides a liturgical refusal behind a workflow one, and the operator
        commits, re-runs, and only then learns the real answer.
        """
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT,
            capture_output=True, text=True,
        ).stdout.strip()
        result = seed(BLOCKED, self.tmp, development=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKED_FOR_ART", result.stderr)
        if dirty:
            self.assertNotIn("uncommitted changes", result.stderr)

    def test_it_writes_no_package_at_all(self):
        seed(BLOCKED, self.tmp)
        self.assertFalse(
            (self.tmp / BLOCKED).exists(),
            "a refused seed left a package behind",
        )


class GitBindingTests(unittest.TestCase):
    """A canonical package names a commit, so it must mean it."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.web = module(
            ROOT / "scripts" / "_pictographic_web.py", "_handoff_web"
        )

    def test_a_dirty_tree_cannot_produce_a_canonical_package(self):
        """Proved against a scratch clone, so this repo is never perturbed."""
        with tempfile.TemporaryDirectory() as scratch:
            clone = Path(scratch) / "repo"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT),
                 str(clone)],
                check=True, capture_output=True,
            )
            # A clone's origin is a filesystem path, which is not a repository
            # name; give it the real one so this exercises the dirty-tree rule
            # rather than the remote-name rule.
            subprocess.run(
                ["git", "remote", "set-url", "origin",
                 "https://github.com/spincyc/triptych.git"],
                cwd=clone, check=True, capture_output=True,
            )
            self.web.repository_identity(clone)  # clean: no refusal
            (clone / "DIRTY.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(self.web.PromptRefused) as refusal:
                self.web.repository_identity(clone)
            self.assertIn("uncommitted", str(refusal.exception))
            identity = self.web.repository_identity(clone, allow_dirty=True)
            self.assertFalse(identity["canonical"])
            self.assertEqual(identity["worktree"], "dirty")

    def test_a_remote_that_is_not_a_repository_is_refused(self):
        """A package states its origin as a fact, so it must be one."""
        with tempfile.TemporaryDirectory() as scratch:
            clone = Path(scratch) / "repo"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT),
                 str(clone)],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "remote", "set-url", "origin", "/tmp/somewhere"],
                cwd=clone, check=True, capture_output=True,
            )
            with self.assertRaises(self.web.PromptRefused) as refusal:
                self.web.repository_identity(clone)
            self.assertIn("not a hosted repository URL",
                          str(refusal.exception))

    def test_a_development_package_says_so_everywhere(self):
        """It must not be mistakable for a canonical handoff.

        Built against a scratch clone that is actually dirty. `--development`
        permits an uncommitted tree rather than forcing a label, so on a clean
        checkout it correctly yields a canonical package; the property worth
        holding is that a package built from a dirty tree says so in every
        place a reader might look.
        """
        with tempfile.TemporaryDirectory() as scratch:
            clone = Path(scratch) / "repo"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT),
                 str(clone)],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "remote", "set-url", "origin",
                 "https://github.com/spincyc/triptych.git"],
                cwd=clone, check=True, capture_output=True,
            )
            (clone / "DIRTY.txt").write_text("uncommitted", encoding="utf-8")
            out = Path(scratch) / "seed"
            result = subprocess.run(
                [sys.executable, str(clone / "tools" / "pictographic"),
                 "art-seed", CALENDAR, FORM, CANARY, "--out", str(out),
                 "--development"],
                capture_output=True, text=True, cwd=clone,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("NONCANONICAL", result.stdout)
            prompt = (out / CANARY / "WEB-AGENT-PROMPT.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("NONCANONICAL DEVELOPMENT PACKAGE", prompt)
            self.assertIn("Working tree at generation: dirty", prompt)
            manifest = load(out / CANARY / "PACKAGE-MANIFEST.yaml")
            self.assertFalse(manifest["canonical"])
            self.assertEqual(
                manifest["package_type"], "pictographic-art-seed-development"
            )
            provenance = load(out / CANARY / "provenance.yaml")
            self.assertFalse(provenance["canonical_package"])

    def test_a_clean_tree_yields_a_canonical_package(self):
        """The flag permits dirt; it does not manufacture it."""
        result = seed(CANARY, self.tmp, development=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = load(self.tmp / CANARY / "PACKAGE-MANIFEST.yaml")
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT,
            capture_output=True, text=True,
        ).stdout.strip()
        self.assertEqual(manifest["canonical"], not dirty)
        self.assertEqual(
            manifest["package_type"],
            "pictographic-art-seed" if not dirty
            else "pictographic-art-seed-development",
        )

    def test_the_commit_is_never_a_literal_in_the_generator(self):
        """The regression that keeps the prompt honest over time.

        The prompt must read the commit from the repository. A hash frozen into
        the generator would keep printing whatever was true on the day it was
        written, and would look exactly as authoritative.
        """
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True,
        ).stdout.strip()
        for path in (
            ROOT / "scripts" / "_pictographic_web.py",
            ROOT / "scripts" / "_pictographic.py",
        ):
            with self.subTest(source=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotIn(head, source)
                self.assertNotIn(head[:9], source)

    def test_the_captured_transcript_declares_its_commit_line_volatile(self):
        """The CLI's example transcript is captured output, so it does hold a
        hash. That is allowed only because the line is registered as volatile
        and replayed against a pattern; otherwise it would rot silently and be
        mistaken for a template value.
        """
        replay = module(
            ROOT / "scripts" / "replay_examples.py", "_handoff_replay"
        )
        command = (
            "tools/pictographic art-seed roman-1962 low-mass LM-001A "
            "--out build/example-art-seed"
        )
        declared = replay.VOLATILE.get(command)
        self.assertIsNotNone(
            declared, "the art-seed transcript declares no volatile line"
        )
        pattern, reason = next(iter(declared.values()))
        self.assertRegex(
            "  commit 0123456789ab on feature/pictographic (spincyc/triptych)",
            pattern,
            "the volatile pattern no longer matches the line it covers",
        )
        self.assertNotRegex(
            "  commit 0123456789ab on some-branch (someone/else)", pattern,
            "the volatile pattern is an exemption wearing a regex",
        )
        self.assertTrue(reason)


class DeterminismTests(unittest.TestCase):
    """The same commit must produce the same package, byte for byte."""

    def test_two_runs_agree_on_every_file(self):
        first, second = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, first, True)
        self.addCleanup(shutil.rmtree, second, True)
        for out in (first, second):
            result = seed(CANARY, out)
            self.assertEqual(result.returncode, 0, result.stderr)
        for name in PACKAGE_FILES:
            with self.subTest(file=name):
                self.assertEqual(
                    (first / CANARY / name).read_bytes(),
                    (second / CANARY / name).read_bytes(),
                    f"{name} differs between two runs of the same commit",
                )


class SummaryContractTests(unittest.TestCase):
    """The summary is checked against the contract, not merely rendered."""

    @classmethod
    def setUpClass(cls):
        cls.web = module(
            ROOT / "scripts" / "_pictographic_web.py", "_summary_web"
        )
        cls.camera = load(LAYER / "camera-model.yaml")
        cls.master = load(LAYER / "sanctuary-master.yaml")

    def summary(self, scene):
        contract = load(CONTRACTS / f"{scene}.yaml")
        return contract, self.web.scene_summary(
            contract, self.camera, self.master
        )

    def test_every_actor_and_placed_object_is_covered(self):
        for scene in (CANARY, SECOND, MULTI_PANEL):
            with self.subTest(scene=scene):
                contract, summary = self.summary(scene)
                self.web.verify_summary(contract, summary)

    def test_the_summary_agrees_with_the_contract_field_by_field(self):
        contract, summary = self.summary(CANARY)
        for actor in summary["actors"]:
            source = next(
                a for a in contract["actors"] if a["id"] == actor["id"]
            )
            self.assertEqual(actor["posture"], source["posture"])
            self.assertEqual(actor["facing"], source["facing_semantic"])
            expected = (
                "epistleward" if source["position"][0] > 0
                else "gospelward" if source["position"][0] < 0 else "centre"
            )
            self.assertEqual(actor["lateral"], expected)
        self.assertEqual(len(summary["panels"]), len(contract["panels"]))
        self.assertEqual(
            summary["sanctuary"]["step_count"], self.master["steps"]["count"]
        )

    def test_a_dropped_object_is_refused(self):
        """Non-vacuity: the verifier has to actually notice a gap."""
        contract, summary = self.summary(CANARY)
        summary["objects"] = summary["objects"][:-1]
        with self.assertRaises(self.web.PromptRefused):
            self.web.verify_summary(contract, summary)

    def test_a_contradicted_posture_is_refused(self):
        contract, summary = self.summary(CANARY)
        summary["actors"][0]["posture"] = "kneeling"
        with self.assertRaises(self.web.PromptRefused):
            self.web.verify_summary(contract, summary)

    def test_an_actor_off_a_named_level_is_refused(self):
        contract, _ = self.summary(CANARY)
        contract["actors"][0]["position"] = [0.0, 0.0, 0.07]
        with self.assertRaises(self.web.PromptRefused):
            self.web.scene_summary(contract, self.camera, self.master)


class DurableRuleTests(unittest.TestCase):
    """The prompt quotes the protocol; it does not keep its own copy."""

    @classmethod
    def setUpClass(cls):
        cls.web = module(
            ROOT / "scripts" / "_pictographic_web.py", "_rules_web"
        )

    @staticmethod
    def flat(text: str) -> str:
        """The protocol is wrapped prose; compare on words, not on lines."""
        return " ".join(text.split())

    def test_both_lists_are_read_out_of_the_protocol(self):
        rules = self.web.durable_rules(PROTOCOL)
        self.assertGreater(len(rules["artist_owns"]), 4)
        self.assertGreater(len(rules["contract_owns"]), 4)
        protocol = self.flat(PROTOCOL.read_text(encoding="utf-8"))
        for item in rules["artist_owns"] + rules["contract_owns"]:
            with self.subTest(item=item):
                self.assertIn(item, protocol)

    def test_a_protocol_that_stops_saying_it_fails_generation(self):
        """Better to refuse than to fall back on a remembered rule."""
        with tempfile.TemporaryDirectory() as scratch:
            copy = Path(scratch) / "PROTOCOL.md"
            copy.write_text(
                PROTOCOL.read_text(encoding="utf-8").replace(
                    "**Owned by the artist**", "Owned by the artist", 1
                ),
                encoding="utf-8",
            )
            with self.assertRaises(self.web.PromptRefused):
                self.web.durable_rules(copy)

    def test_the_protocol_stays_free_of_scene_and_commit_facts(self):
        """Durable means durable: no commit hashes, no generated identity."""
        protocol = PROTOCOL.read_text(encoding="utf-8")
        self.assertNotRegex(
            protocol, r"\bseed commit\b",
            "the durable protocol has acquired a generated-prompt fact",
        )
        self.assertNotRegex(
            protocol, r"\b[0-9a-f]{9,40}\b",
            "the durable protocol has acquired a commit hash",
        )

    # The prompt speaks to an image model and the protocol speaks to a reader,
    # so a few of the same bans are worded differently. The mapping is explicit
    # rather than fuzzy, so that a ban added to the prompt without a home in
    # the protocol fails here instead of passing on a loose substring.
    PROTOCOL_WORDING = {
        "a page number": "pagination",
        "explanatory prose": "descriptive prose",
        "an inset": "inset",
        "a diagram": "diagram",
        "a plate identifier": "plate identifier",
    }

    def test_the_raw_art_ban_matches_the_protocol(self):
        """The generator names the banned furniture; the protocol owns it."""
        protocol = self.flat(PROTOCOL.read_text(encoding="utf-8")).lower()
        for item in self.web.RAW_ART_FORBIDDEN:
            noun = self.PROTOCOL_WORDING.get(item, item.split(" ", 1)[-1])
            with self.subTest(item=item):
                self.assertIn(
                    noun.lower(), protocol,
                    f"the prompt bans {item!r} but the protocol never mentions "
                    f"{noun!r}",
                )


class PromptCompletenessTests(unittest.TestCase):
    """A prompt missing a section is not shipped."""

    @classmethod
    def setUpClass(cls):
        cls.web = module(
            ROOT / "scripts" / "_pictographic_web.py", "_complete_web"
        )
        cls.tmp = Path(tempfile.mkdtemp())
        result = seed(CANARY, cls.tmp)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        cls.prompt = (cls.tmp / CANARY / "WEB-AGENT-PROMPT.md").read_text(
            encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_required_section_is_present(self):
        for section in self.web.PROMPT_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(f"## {section}", self.prompt)
        self.web.check_prompt_complete(self.prompt)

    def test_a_missing_section_is_refused(self):
        for section in self.web.PROMPT_SECTIONS:
            with self.subTest(section=section):
                damaged = self.prompt.replace(f"## {section}", "## Something", 1)
                with self.assertRaises(self.web.PromptRefused):
                    self.web.check_prompt_complete(damaged)


class OperatorConsoleTests(unittest.TestCase):
    """What the operator is told, which is the whole point of the lane."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.result = seed(CANARY, cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_it_states_readiness_and_the_workflow(self):
        out = self.result.stdout
        self.assertIn("ART SEED READY", out)
        self.assertIn("Fresh-web workflow:", out)
        for step in ("Attach the entire emitted package",
                     "Open WEB-AGENT-PROMPT.md",
                     "Paste it verbatim",
                     "EDIT render-underlay.png",
                     "exactly one candidate",
                     "STRUCTURE review"):
            with self.subTest(step=step):
                self.assertIn(step, out)

    def test_it_does_not_dump_the_prompt(self):
        """The prompt is attached and pasted, not scrolled past."""
        self.assertNotIn("## What is visibly true in this scene",
                         self.result.stdout)
        self.assertLess(len(self.result.stdout.splitlines()), 30)

    def test_it_names_the_commit_and_the_canary(self):
        self.assertIn("feature/pictographic", self.result.stdout)
        self.assertIn("spincyc/triptych", self.result.stdout)
        self.assertIn("PIPELINE CANARY", self.result.stdout)


if __name__ == "__main__":
    unittest.main()
