"""Three-edition ownership and staged structural checks, with legacy isolation."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_components as components
import _corpus


def load(name):
    loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


def fixture(root: Path):
    provider = root / "src/gpt"
    leaf = provider / "proper"
    leaf.mkdir(parents=True)
    (leaf / "research").mkdir()
    elements = ["introit", "collect", "gospel", "communion"]
    data = dict(schema=2, record_type="proper-components", document="proper", calendar="roman-1962",
                entrypoint="main.tex", synthesis_entrypoint="synthesis.tex",
                homily_entrypoint="homily.tex", appointed_text_completeness="complete",
                element_keys=elements,
                outputs=dict(research="proper", synthesis="proper-synthesis", homily="proper-homily",
                             web="proper", canonical_label="Full PDF", synthesis_label="Synthesis PDF",
                             homily_label="Homily PDF"), components=[], lanes=[])
    for key, kind, modes in (
        ("appointed", "appointed-text", ["research"]),
        ("treatment", "proper-treatment", ["research"]),
        ("augustine", "interpretive-lane", ["research"]),
        ("gregory", "interpretive-lane", ["research"]),
        ("integrated", "integrated-commentary", ["synthesis"]),
        ("sermon", "homily", ["homily"]),
        ("terminal", "terminal-apparatus", list(components.MODES)),
    ):
        data["components"].append(dict(key=key, kind=kind, path=key + ".tex", modes=modes,
                                       element_keys=list(elements), references=[], depends_on=[]))
        (leaf / (key + ".tex")).write_text("Substantive fixture text.\n")
    for key in ("augustine", "gregory"):
        data["lanes"].append(dict(key=key, authors=[key.title(), "Thomas Aquinas"],
                                  sources=["research/sources.md"],
                                  senses=sorted(components.SENSES), element_keys=list(elements),
                                  component_keys=[key]))
    (leaf / "research/sources.md").write_text("Checked loci in source records.\n")
    (leaf / "generation-metadata.tex").write_text("Fixture provenance.\n")
    for mode, name in components.ENTRYPOINTS.items():
        body = "\\hypersetup{pdftitle={" + mode + "}}\n\\begin{document}\n"
        body += "".join("\\input{proper/" + item["path"] + "}\n"
                        for item in data["components"] if mode in item["modes"])
        body += "\\input{proper/generation-metadata}\n\\end{document}\n"
        (leaf / name).write_text(body)
    return data, leaf / components.MANIFEST, provider


def save(data, path):
    lines = []
    for key, value in data.items():
        if key not in {"outputs", "components", "lanes"}:
            lines.append(f"{key} = {json.dumps(value)}")
    lines.append("[outputs]")
    lines.extend(f"{key} = {json.dumps(value)}" for key, value in data["outputs"].items())
    for kind in ("components", "lanes"):
        for item in data[kind]:
            lines.append(f"[[{kind}]]")
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in item.items())
    path.write_text("\n".join(lines) + "\n")


class ProperV2Tests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch/components").mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / ".scratch/components")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data, self.path, self.provider = fixture(self.root)
        save(self.data, self.path)

    def audit(self, **kwargs):
        components.audit_v2(self.data, self.path, self.provider, **kwargs)

    def test_complete_three_edition_graph(self):
        self.audit()

    def test_calendar_identity_is_required(self):
        self.data.pop("calendar")
        with self.assertRaisesRegex(ValueError, "calendar"):
            self.audit(phase="scope")

    def test_opposite_calendar_content_is_refused_in_both_directions(self):
        families = ("1962/propers/temporal/leaf", "postconciliar/en-us-2011/propers/temporal/leaf")
        for own, other in (families, families[::-1]):
            with self.subTest(own=own):
                leaf = self.provider / "liturgy/roman-rite" / own
                target = self.provider / "liturgy/roman-rite" / other / "shared.tex"
                leaf.mkdir(parents=True, exist_ok=True)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("Separate calendar text.\n")
                entry = leaf / "main.tex"
                entry.write_text("\\input{" + target.relative_to(self.provider).as_posix() + "}\n")
                with self.assertRaisesRegex(ValueError, "calendar/proper boundary"):
                    components.include_graph(entry, leaf, self.provider)

    def test_postconciliar_locale_content_cannot_cross(self):
        leaf = self.provider / "liturgy/roman-rite/postconciliar/en-us-2011/propers/temporal/leaf"
        target = self.provider / "liturgy/roman-rite/postconciliar/en-gb-2011/propers/shared/text.tex"
        leaf.mkdir(parents=True)
        target.parent.mkdir(parents=True)
        target.write_text("Other territorial book.\n")
        entry = leaf / "main.tex"
        entry.write_text("\\input{" + target.relative_to(self.provider).as_posix() + "}\n")
        with self.assertRaisesRegex(ValueError, "edition/locale boundary"):
            components.include_graph(entry, leaf, self.provider)

    def test_five_complete_distinct_lanes_are_accepted(self):
        research = self.path.parent / "main.tex"
        for key in ("ambrose", "chrysostom", "bede"):
            component = copy.deepcopy(self.data["components"][2])
            component.update(key=key, path=key + ".tex")
            self.data["components"].append(component)
            lane = copy.deepcopy(self.data["lanes"][0])
            lane.update(key=key, authors=[key.title(), "Thomas Aquinas"], component_keys=[key])
            self.data["lanes"].append(lane)
            (self.path.parent / (key + ".tex")).write_text("Whole-proper fixture lane.\n")
            research.write_text(research.read_text() + "\\input{proper/" + key + "}\n")
        self.audit()

    def test_lane_count_boundaries(self):
        for count in (0, 1, 6):
            with self.subTest(count=count):
                data = copy.deepcopy(self.data)
                data["lanes"] = (data["lanes"] * 3)[:count]
                with self.assertRaisesRegex(ValueError, "2–5"):
                    components.audit_v2(data, self.path, self.provider)

    def test_each_lane_requires_every_sense_and_element(self):
        for field in ("senses", "element_keys"):
            data = copy.deepcopy(self.data)
            data["lanes"][0][field].pop()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "four senses|every element"):
                components.audit_v2(data, self.path, self.provider)

    def test_lane_requires_authors_and_sources(self):
        for field in ("authors", "sources"):
            data = copy.deepcopy(self.data)
            data["lanes"][0][field] = []
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                components.audit_v2(data, self.path, self.provider)

    def test_each_lane_requires_two_distinct_authors(self):
        for authors in (["Augustine"], ["Augustine", " augustine "]):
            self.data["lanes"][0]["authors"] = authors
            with self.subTest(authors=authors), self.assertRaisesRegex(ValueError, "two distinct authors"):
                self.audit()

    def test_lane_component_binding_is_unique(self):
        self.data["lanes"][1]["component_keys"] = ["augustine"]
        with self.assertRaisesRegex(ValueError, "distinct research"):
            self.audit()

    def test_missing_homily_is_only_allowed_before_its_content_stage(self):
        (self.path.parent / "homily.tex").unlink()
        (self.path.parent / "sermon.tex").unlink()
        self.audit(phase="scope")
        self.audit(edition="research")
        with self.assertRaisesRegex(ValueError, "homily_entrypoint"):
            self.audit()

    def test_missing_lane_source_fails_content(self):
        (self.path.parent / "research/sources.md").unlink()
        with self.assertRaisesRegex(ValueError, "source"):
            self.audit()

    def test_lane_sources_have_one_research_owner(self):
        outside = self.path.parent / "sources.md"
        outside.write_text("Duplicate audit outside its owner.\n")
        self.data["lanes"][0]["sources"] = ["sources.md"]
        with self.assertRaisesRegex(ValueError, "owned beneath research"):
            self.audit()

    def test_no_output_can_escape_or_create_a_second_web_identity(self):
        for key, value in (("homily", "../stolen"), ("web", "proper-homily")):
            data = copy.deepcopy(self.data)
            data["outputs"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "outputs"):
                components.audit_v2(data, self.path, self.provider)

    def test_symlink_escape_is_refused(self):
        outside = self.root / "outside.tex"
        outside.write_text("Unowned content.")
        fragment = self.path.parent / "sermon.tex"
        fragment.unlink()
        fragment.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "inside the canonical leaf"):
            self.audit()

    def test_missing_and_cross_mode_includes_are_refused(self):
        entry = self.path.parent / "homily.tex"
        original = entry.read_text()
        for text in (original.replace("\\input{proper/sermon.tex}", ""),
                     original + "\\input{proper/appointed.tex}\n"):
            entry.write_text(text)
            with self.assertRaisesRegex(ValueError, "include graph"):
                self.audit()

    def test_conditional_and_cyclic_includes_are_refused(self):
        fragment = self.path.parent / "sermon.tex"
        for text in ("\\iffalse\\input{proper/sermon}\\fi", "\\input{proper/sermon}",
                     "\\newcommand{\\Unused}{\\input{proper/sermon}}"):
            fragment.write_text(text)
            with self.assertRaisesRegex(ValueError, "unconditional|cycle"):
                self.audit()

    def test_undeclared_local_fragment_cannot_bypass_modes(self):
        extra = self.path.parent / "extra.tex"
        extra.write_text("Unregistered sermon text.\n")
        entry = self.path.parent / "homily.tex"
        entry.write_text(entry.read_text() + "\\input{proper/extra}\n")
        with self.assertRaisesRegex(ValueError, "undeclared local"):
            self.audit()

    def test_missing_include_is_not_confused_with_an_empty_graph(self):
        entry = self.path.parent / "homily.tex"
        entry.write_text(entry.read_text() + "\\input{proper/missing}\n")
        with self.assertRaisesRegex(ValueError, "missing include"):
            self.audit()

    def test_homily_cannot_become_a_second_editable_leaf(self):
        (self.provider / "proper-homily").mkdir()
        with self.assertRaisesRegex(ValueError, "second editable leaf"):
            self.audit(phase="scope")

    def test_artifacts_requires_every_pdf(self):
        build = self.root / "review-pdfs"
        build.mkdir()
        for name in ("proper", "proper-synthesis"):
            (build / f"{name}.pdf").write_bytes(b"%PDF-1.7\nfixture")
        with self.assertRaisesRegex(ValueError, "homily output"):
            self.audit(phase="artifacts", build_root=build)
        (build / "proper-homily.pdf").write_bytes(b"%PDF-1.7\nfixture")
        self.audit(phase="artifacts", build_root=build)

    def test_v2_aux_needs_no_legacy_page_markers(self):
        aux = self.root / "empty.aux"
        aux.write_text("No fixed pagination.\n")
        result = subprocess.run([str(ROOT / "tools/check-proper-components"), "--root", str(self.root),
                                 "--document", "proper", "--aux", str(aux)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_homily_metadata_resolves_one_canonical_owner(self):
        checker = load("check-generation-metadata")
        source = checker.resolve_source(self.provider, "proper-homily")
        self.assertEqual(source.leaf, self.path.parent)
        self.assertEqual(source.entry.name, "homily.tex")
        checker.validate_provenance_input(source)
        source.entry.write_text(source.entry.read_text() + "\\input{proper/generation-metadata}\n")
        with self.assertRaisesRegex(ValueError, "exactly once"):
            checker.validate_provenance_input(source)

    def test_catalogue_carries_homily_as_third_issue(self):
        with mock.patch.multiple(_corpus, ROOT=self.root, SRC=self.root / "src",
                                 PDF_ROOT=self.root / "pdf", PUBLICATION_ROOT=self.root / "release/publications"):
            issues = _corpus._issues_of(self.path.parent, "gpt", "proper", False)
        self.assertEqual([issue.kind for issue in issues], ["full", "synthesis", "homily"])
        self.assertEqual(issues[-1].title.text, "homily")

    def test_publication_discovery_and_owner(self):
        public = load("public-alpha")
        with mock.patch.object(public, "ROOT", self.root):
            self.assertEqual(public.discover_source_ids("gpt"), {"proper", "proper-synthesis", "proper-homily"})
            self.assertEqual(public.publication_source_path("gpt", "proper-homily"), self.path)

    def test_make_discovers_and_builds_homily_from_canonical_owner(self):
        shutil.copy2(ROOT / "Makefile", self.root / "Makefile")
        for directory in ("tools", "scripts"):
            (self.root / directory).mkdir()
        for name in ("_proper_components.py", "_tooling.py"):
            shutil.copy2(ROOT / "scripts" / name, self.root / "scripts" / name)
        shutil.copy2(ROOT / "tools/check-proper-components", self.root / "tools/check-proper-components")
        launcher = self.root / "tools/tpt"
        launcher.write_text('#!/usr/bin/env python3\nimport os, sys\nos.execv("./tools/" + sys.argv[1], sys.argv[1:])\n')
        launcher.chmod(0o755)
        result = subprocess.run(["make", "-n", "build/gpt/proper-homily.pdf"], cwd=self.root,
                                 capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("proper/homily.tex", result.stdout)
        self.assertIn("--pdf 'proper-homily'", result.stdout)
        listed = subprocess.run(["make", "-s", "list"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertIn("proper-homily", listed.stdout)


if __name__ == "__main__":
    unittest.main()
