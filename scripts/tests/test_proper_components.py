from __future__ import annotations

import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "scripts" / "check-proper-components"
loader = importlib.machinery.SourceFileLoader("proper_components", str(PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


class ProperComponentTests(unittest.TestCase):
    def component_tree(self, directory: str, *, appointed_modes: str = '["research"]',
                       treatment_modes: str = '["research"]',
                       swap_tail: bool = False):
        provider = Path(directory) / "src" / "gpt"
        leaf = provider / "proper"
        leaf.mkdir(parents=True)
        for name in (
            "main.tex", "synthesis.tex", "appointed.tex", "treatment.tex",
            "brief.tex", "grounded.tex", "exploratory.tex", "notable.tex",
            "terminal.tex", "brief-refs.tex",
        ):
            (leaf / name).write_text("% fixture\n", encoding="utf-8")
        components = [
            ("appointed", "appointed-text", "appointed.tex", appointed_modes),
            ("treatment", "proper-treatment", "treatment.tex", treatment_modes),
            ("brief", "brief-synthesis", "brief.tex", '["research", "synthesis"]'),
            ("grounded", "source-grounded-synthesis", "grounded.tex",
             '["research", "synthesis"]'),
            ("exploratory", "exploratory-synthesis", "exploratory.tex",
             '["research", "synthesis"]'),
            ("notable", "notable-quotable", "notable.tex",
             '["research", "synthesis"]'),
            ("terminal", "terminal-apparatus", "terminal.tex",
             '["research", "synthesis"]'),
        ]
        if swap_tail:
            components[4], components[5] = components[5], components[4]
        blocks = []
        for key, kind, path, modes in components:
            references = '["brief-refs.tex"]' if key == "brief" else "[]"
            blocks.append(
                f'[[components]]\nkey = "{key}"\nkind = "{kind}"\n'
                f'path = "{path}"\nmodes = {modes}\ndepends_on = []\n'
                f'element_keys = ["introit", "gospel"]\nreferences = {references}\n'
            )
        manifest = (
            'schema = 1\nrecord_type = "proper-components"\ndocument = "proper"\n'
            'entrypoint = "main.tex"\nsynthesis_entrypoint = "synthesis.tex"\n'
            'appointed_text_completeness = "complete"\n'
            'element_keys = ["introit", "gospel"]\n'
            '[outputs]\nresearch = "proper"\nsynthesis = "proper-synthesis"\n'
            'web = "proper"\ncanonical_label = "Full PDF"\n'
            'synthesis_label = "Synthesis PDF"\n\n' + "\n".join(blocks) +
            '\n[[relations]]\nkey = "opening-to-gospel"\n'
            'element_keys = ["introit", "gospel"]\n'
            'evidence = ["source-grounded-synthesis"]\n'
        )
        path = leaf / "proper-components.toml"
        path.write_text(manifest, encoding="utf-8")
        return path, provider

    def test_manifest_enforces_agreed_mode_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory)
            module.audit_manifest(path, provider)

    def test_synthesis_must_omit_appointed_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(
                directory, appointed_modes='["research", "synthesis"]'
            )
            with self.assertRaisesRegex(ValueError, "appointed-text"):
                module.audit_manifest(path, provider)

    def test_synthesis_may_retain_substantive_proper_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(
                directory, treatment_modes='["research", "synthesis"]'
            )
            module.audit_manifest(path, provider)

    def test_exploratory_precedes_notable(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory, swap_tail=True)
            with self.assertRaisesRegex(ValueError, "component order"):
                module.audit_manifest(path, provider)

    def test_rights_limited_text_requires_research_label(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory)
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'appointed_text_completeness = "complete"',
                'appointed_text_completeness = "rights-limited"',
            )
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Research PDF"):
                module.audit_manifest(path, provider)

    def test_exact_two_page_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            aux = Path(directory) / "guide.aux"
            aux.write_text(
                "\\newlabel{triptych:brief-synthesis:start}{{}{7}}\n"
                "\\newlabel{triptych:brief-synthesis:end}{{}{8}}\n"
                "\\newlabel{triptych:brief-synthesis:next}{{}{9}}\n",
                encoding="utf-8",
            )
            module.validate_brief_pages(aux)

    def test_rejects_spilled_brief_synthesis(self):
        with tempfile.TemporaryDirectory() as directory:
            aux = Path(directory) / "guide.aux"
            aux.write_text(
                "\\newlabel{triptych:brief-synthesis:start}{{}{7}}\n"
                "\\newlabel{triptych:brief-synthesis:end}{{}{9}}\n"
                "\\newlabel{triptych:brief-synthesis:next}{{}{10}}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "exactly two"):
                module.validate_brief_pages(aux)


if __name__ == "__main__":
    unittest.main()
