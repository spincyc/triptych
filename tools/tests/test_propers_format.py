"""Opt-in template, lane, font and homily-only column regressions."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.tests.test_proper_components_v2 import ROOT, components, fixture
import _proper_study as study


class ProperFormatTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/propers-format-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data, self.path, self.provider = fixture(self.root)
        self.leaf = self.path.parent
        self.data["format_contract"] = components.FORMAT_CONTRACT
        common = self.root / "src/common"
        common.mkdir()
        for name in ("preamble", "propers-format", "propers-homily"):
            shutil.copyfile(ROOT / "src/common" / f"{name}.tex", common / f"{name}.tex")
        for mode, name in components.ENTRYPOINTS.items():
            entry = self.leaf / name
            body = entry.read_text()
            if mode == "homily":
                body = body.replace(r"\input{proper/sermon.tex}",
                                    "\\begin{properhomily}\n\\input{proper/sermon.tex}\n"
                                    "\\end{properhomily}")
            body = body.replace(r"\begin{document}", "\\begin{document}\n"
                                "\\propertitle{Celebration}{Subtitle}{Edition}{Occasion}")
            imports = "\\input{common/preamble}\n\\input{common/propers-format}\n"
            if mode == "homily":
                imports += "\\input{common/propers-homily}\n"
            entry.write_text(imports + body)
        for lane in self.data["lanes"]:
            path = self.leaf / (lane["key"] + ".tex")
            path.write_text("\\properlane{" + lane["key"] + "}{Interpretation}\n"
                            "\\subsection{An argument}\nSubstantive explanation.\n"
                            "\\begin{fourSenses}\n" + "\n".join(
                                "\\item[" + sense + ".] An explanation."
                                for sense in ("Literal", "Allegorical", "Moral", "Anagogical"))
                            + "\n\\end{fourSenses}\n")

    def audit(self, **kwargs):
        components.audit_v2(self.data, self.path, self.provider, **kwargs)

    def test_shared_template_and_historical_isolation(self):
        self.audit()
        self.assertTrue(components.format_contract(self.data, required=True))
        self.data.pop("format_contract")
        self.assertFalse(components.format_contract(self.data))
        with self.assertRaisesRegex(ValueError, "format_contract"):
            components.format_contract(self.data, required=True)
        self.data["format_contract"] = "invented"
        with self.assertRaisesRegex(ValueError, "format_contract"):
            self.audit(phase="scope")

    def test_missing_reordered_duplicate_or_body_template_imports_fail(self):
        entry = self.leaf / "main.tex"
        original = entry.read_text()
        variants = [
            original.replace("\\input{common/propers-format}\n", ""),
            original.replace("common/preamble", "common/propers-format"),
            original + "\n\\input{common/propers-format}",
            original.replace("\\input{common/propers-format}\n", "")
                    .replace("\\begin{document}", "\\begin{document}\\input{common/propers-format}"),
        ]
        for text in variants:
            entry.write_text(text)
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "shared-template"):
                self.audit()

    def test_local_font_measure_and_template_overrides_fail(self):
        path = self.leaf / "treatment.tex"
        original = path.read_text()
        for override in (r"\usepackage{mathpazo}", r"\usepackage{newpxtext}",
                         r"\geometry{margin=1.3in}", r"\fontsize{13}{18}\selectfont",
                         r"\linespread{1.2}", r"\renewcommand{\rmdefault}{ppl}",
                         r"\renewcommand{\propertitle}[4]{#1}",
                         r"\renewenvironment{fourSenses}{}{}",
                         r"\setlength{\textwidth}{4in}",
                         r"\addtolength{\textheight}{1in}",
                         r"\fancyhead[R]{Local head}",
                         r"\thispagestyle{plain}",
                         r"\markright{Local mark}",
                         r"\definecolor{accent}{rgb}{1,0,0}",
                         r"\color{red}",
                         r"\textcolor{red}{Locally colored text}",
                         r"\setlength{\linewidth}{3in}",
                         r"\textwidth=4in",
                         r"\usepackage{geometry}"):
            path.write_text(original + override)
            with self.subTest(override=override), self.assertRaisesRegex(ValueError, "overrides"):
                self.audit()

    def test_homily_helper_cannot_leak_into_either_study(self):
        for name in ("main.tex", "synthesis.tex"):
            entry = self.leaf / name
            original = entry.read_text()
            for addition in ("\\input{common/propers-homily}\n",
                             "\\begin{properhomily}Text.\\end{properhomily}\n",
                             "\\begin{multicols}{2}Text.\\end{multicols}\n",
                             "\\twocolumn\n"):
                entry.write_text(original + addition)
                with self.subTest(name=name, addition=addition), self.assertRaisesRegex(
                        ValueError, "shared-template|columns"):
                    self.audit()
            entry.write_text(original)

    def test_each_mode_imports_its_components_directly_once_in_manifest_order(self):
        for name in components.ENTRYPOINTS.values():
            entry = self.leaf / name
            original = entry.read_text()
            selected = []
            for item in self.data["components"]:
                if name == "main.tex" and "research" in item["modes"]:
                    selected.append(item["path"])
                elif name == "synthesis.tex" and "synthesis" in item["modes"]:
                    selected.append(item["path"])
                elif name == "homily.tex" and "homily" in item["modes"]:
                    selected.append(item["path"])
            first = "\\input{proper/" + selected[0] + "}"
            second = "\\input{proper/" + selected[1] + "}"
            variants = (
                original + "\n" + first,
                original.replace(first, "TRIPTYCH_FIRST_COMPONENT")
                        .replace(second, first)
                        .replace("TRIPTYCH_FIRST_COMPONENT", second),
            )
            for text in variants:
                entry.write_text(text)
                with self.subTest(name=name, text=text), self.assertRaisesRegex(
                        ValueError, "component imports|homily"):
                    self.audit()
            entry.write_text(original)
            nested_owner = self.leaf / selected[1]
            nested_original = nested_owner.read_text()
            entry.write_text(original.replace(first + "\n", ""))
            nested_owner.write_text(first + "\n" + nested_original)
            with self.subTest(name=name, nested=True), self.assertRaises(ValueError):
                self.audit()
            nested_owner.write_text(nested_original)
            entry.write_text(original)

            # A correct direct import does not excuse a second transitive
            # import of the same manifest component.
            nested_owner.write_text(first + "\n" + nested_original)
            with self.subTest(name=name, nested_duplicate=True), self.assertRaisesRegex(
                    ValueError, "exactly once"):
                self.audit()
            nested_owner.write_text(nested_original)

    def test_homily_apparatus_cannot_also_be_nested_in_spoken_component(self):
        spoken = self.leaf / "sermon.tex"
        original = spoken.read_text()
        spoken.write_text(original + "\n\\input{proper/terminal.tex}\n")
        with self.assertRaisesRegex(ValueError, "exactly once"):
            self.audit()

    def test_homily_only_speech_inside_columns_with_title_and_apparatus_outside(self):
        entry = self.leaf / "homily.tex"
        original = entry.read_text()
        for text in (
            original.replace("\\begin{properhomily}", ""),
            original.replace("\\begin{properhomily}", "\\begin{properhomily}Unowned words."),
            original.replace("\\end{properhomily}", "")
                    .replace("\\input{proper/terminal.tex}",
                             "\\input{proper/terminal.tex}\\end{properhomily}"),
            original.replace("\\propertitle{Celebration}{Subtitle}{Edition}{Occasion}", "")
                    .replace("\\begin{properhomily}",
                             "\\begin{properhomily}\\propertitle{Celebration}{Subtitle}{Edition}{Occasion}"),
            original.replace("\\end{properhomily}",
                             "\\end{properhomily}\\input{proper/sermon.tex}"),
            original.replace("\\begin{properhomily}",
                             "\\input{proper/terminal.tex}\\begin{properhomily}"),
        ):
            entry.write_text(text)
            with self.subTest(text=text), self.assertRaisesRegex(
                    ValueError, "homily|spoken"):
                self.audit()

    def test_lane_heading_key_and_four_sense_layout_are_checked(self):
        path = self.leaf / "augustine.tex"
        original = path.read_text()
        for text in (original.replace("\\properlane{augustine}", "\\properlane{other}"),
                     original.replace("fourSenses", "description"),
                     original.replace("\\item[Moral.]", "\\item[Literal.]"),
                     original + "\\properlane{augustine}{Second heading}"):
            path.write_text(text)
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "lane"):
                self.audit()

    def test_every_shared_format_control_rejects_local_alias_or_undefinition(self):
        shared = "\n".join(
            (self.root / "src/common" / name).read_text()
            for name in ("propers-format.tex", "propers-homily.tex")
        )
        commands = {match.group("name") for match in components.COMMAND_DEFINITION_RE.finditer(shared)}
        commands -= components.FORMAT_CONFIGURATION_COMMANDS
        environments = {
            match.group("name") for match in components.ENVIRONMENT_DEFINITION_RE.finditer(shared)
        }
        controls = commands | environments | {"end" + name for name in environments}
        self.assertTrue({"propertitle", "properlane", "fourSenses", "endfourSenses",
                         "maptable", "endmaptable", "properhomily", "endproperhomily"} <= controls)
        path = self.leaf / "treatment.tex"
        original = path.read_text()
        for control in sorted(controls):
            for source in (r"\relax", r"\undefined"):
                path.write_text(original + f"\n\\let\\{control}{source}\n")
                with self.subTest(control=control, source=source), self.assertRaisesRegex(
                        ValueError, "aliases|definitions|undefinitions"):
                    self.audit(edition="research")
        path.write_text(original)

    def test_computed_shared_definition_is_refused(self):
        path = self.leaf / "treatment.tex"
        path.write_text(path.read_text() +
                        "\\expandafter\\def\\csname propertitle\\endcsname{Spoof}\n")
        with self.assertRaisesRegex(ValueError, "computed control"):
            self.audit(edition="research")

    def test_latex_command_copy_aliases_are_refused(self):
        path = self.leaf / "treatment.tex"
        original = path.read_text()
        for command in ("NewCommandCopy", "RenewCommandCopy", "DeclareCommandCopy",
                        "ProvideCommandCopy"):
            path.write_text(original + f"\\{command}\\propertitle\\relax\n")
            with self.subTest(command=command), self.assertRaisesRegex(
                    ValueError, "command-copy aliases"):
                self.audit(edition="research")
        path.write_text(original)

    def test_rendered_fonts_must_be_latin_modern_and_embedded(self):
        header = "name type encoding emb sub uni object ID\n----\n"
        for name, embedded, ok in (("ABCDEF+LMRoman10-Regular", "yes", True),
                                   ("ABCDEF+LMMathSymbols10-Regular", "yes", True),
                                   ("ABCDEF+Palladio", "yes", False),
                                   ("ABCDEF+LMRoman10-Regular", "no", False)):
            result = subprocess.CompletedProcess([], 0, header +
                f"{name} Type 1 Custom {embedded} yes yes 12 0\n", "")
            with self.subTest(name=name, embedded=embedded), patch.object(
                    components.subprocess, "run", return_value=result):
                if ok:
                    components.format_artifacts(self.data, self.root, components.MODES)
                else:
                    with self.assertRaisesRegex(ValueError, "embedded Latin Modern"):
                        components.format_artifacts(self.data, self.root, components.MODES)

    def test_current_workflow_requires_both_contracts(self):
        pipeline = json.loads((ROOT / "workflows/pipelines/proper-study.json").read_text())
        self.assertEqual(pipeline["version"], 6)
        checks = [check["command"] for stage in pipeline["stages"]
                  for check in stage.get("checks", [])
                  if "--require-presentation" in check["command"]]
        self.assertEqual(len(checks), 5)
        self.assertTrue(all("--require-format" in command for command in checks))
        with patch.object(study, "scope"), patch.object(study, "manifest", return_value={"schema": 2}):
            with self.assertRaisesRegex(ValueError, "format_contract"):
                study.check(self.root, "gpt", "proper", "content", "research", require_format=True)

    @unittest.skipUnless(shutil.which("pdflatex") and shutil.which("pdffonts"), "requires TeX and Poppler")
    def test_real_template_retains_baseline_and_homily_columns(self):
        build = self.root / "build"
        build.mkdir()
        source = build / "proof.tex"
        common = (self.root / "src/common").as_posix()
        source.write_text(
            "\\input{" + common + "/preamble}\n\\input{" + common + "/propers-format}\n"
            "\\input{" + common + "/propers-homily}\n"
            "\\renewcommand{\\tptheadsunday}{Sunday head}\n"
            "\\begin{document}\\propertitle{Title}{Subtitle}{Edition}{Occasion}\n"
            "\\makeatletter\\typeout{BASE-SIZE=\\f@size}\\makeatother\n"
            "\\typeout{TEXT-WIDTH=\\the\\textwidth}\n"
            "\\properlane{proof}{Shared lane}\n"
            "\\begin{fourSenses}"
            "\\item[Literal.] Literal proof.\\item[Allegorical.] Allegorical proof."
            "\\item[Moral.] Moral proof.\\item[Anagogical.] Anagogical proof."
            "\\end{fourSenses}\n"
            "\\begin{maptable}A & B & C\\\\\\end{maptable}\n"
            "\\begin{comparisontable}{One}{Two}{Three}{Four}"
            "E & F & G & H\\\\\\end{comparisontable}\n"
            "\\begin{properhomily}\\typeout{SPEECH-WIDTH=\\the\\linewidth}\n"
            + "A spoken paragraph that remains in the shared type.\n\n" * 120
            + "\\end{properhomily}\\typeout{NOTE-WIDTH=\\the\\linewidth}\n"
            "\\section*{Source note}Separate apparatus.\\end{document}\n")
        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                 source.name], cwd=build, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout[-2500:])
        import re
        values = dict(re.findall(r"(BASE-SIZE|TEXT-WIDTH|SPEECH-WIDTH|NOTE-WIDTH)=([0-9.]+)", result.stdout))
        self.assertEqual(values["BASE-SIZE"], "10.95")  # article's standard 11pt size
        self.assertAlmostEqual(float(values["TEXT-WIDTH"]), 7 * 72.27, places=2)
        self.assertLess(float(values["SPEECH-WIDTH"]), float(values["TEXT-WIDTH"]) / 2)
        self.assertEqual(values["NOTE-WIDTH"], values["TEXT-WIDTH"])
        components.format_artifacts({"outputs": {"homily": "proof"}}, build, ("homily",))
        extracted = subprocess.run(
            ["pdftotext", "-layout", "proof.pdf", "-"], cwd=build,
            capture_output=True, text=True, check=True).stdout.split("\f")
        self.assertEqual(extracted[0].count("Title"), 1)
        self.assertNotIn("Sunday head", extracted[0])
        self.assertNotIn("Homily", extracted[0])
        self.assertTrue(any("Sunday head" in page and "Homily" in page
                            for page in extracted[1:]))
        joined = "\n".join(extracted)
        for text in ("Shared lane", "Literal proof", "A", "One", "Four"):
            self.assertIn(text, joined)
        fonts = subprocess.run(
            ["pdffonts", "proof.pdf"], cwd=build, capture_output=True,
            text=True, check=True).stdout
        self.assertNotIn("LMRoman10-Italic", fonts)

    @unittest.skipUnless(shutil.which("pdflatex") and shutil.which("pdftotext"),
                         "requires TeX and Poppler")
    def test_rendered_obfuscated_inputs_are_rejected_by_the_semantic_graph(self):
        (self.leaf / "unowned.tex").write_text("UNDECLARED MEANING-BEARING PROSE.\n")
        treatment = self.leaf / "treatment.tex"
        original = treatment.read_text()
        attacks = (
            ("computed", r"\csname input\endcsname{proper/unowned}", "computed control"),
            ("hex", r"\^^69nput{proper/unowned}", "character-code notation"),
        )
        environment = dict(os.environ)
        environment["TEXINPUTS"] = "../:"
        for name, attack, error in attacks:
            treatment.write_text(original + attack + "\n")
            build = self.root / f"{name}-input-build"
            build.mkdir()
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-output-directory", str(build), "proper/main.tex"],
                cwd=self.provider, env=environment, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-2500:])
            extracted = subprocess.run(
                ["pdftotext", str(build / "main.pdf"), "-"], capture_output=True,
                text=True, check=True,
            ).stdout
            self.assertIn("UNDECLARED MEANING-BEARING PROSE", extracted)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, error):
                self.audit(edition="research")
        treatment.write_text(original)

    @unittest.skipUnless(shutil.which("pdflatex"), "requires TeX")
    def test_rendered_aliases_cannot_replace_shared_homily_columns(self):
        common = (self.root / "src/common").as_posix()
        attacks = (
            ("hex-let", r"\^^6cet\properhomily\quote" + "\n"
             + r"\^^6cet\endproperhomily\endquote", "character-code notation"),
            ("command-copy", r"\RenewCommandCopy\properhomily\quote" + "\n"
             + r"\RenewCommandCopy\endproperhomily\endquote", "command-copy aliases"),
        )
        entry = self.leaf / "homily.tex"
        original = entry.read_text()
        for name, attack, error in attacks:
            source = self.root / f"{name}.tex"
            source.write_text(
                "\\input{" + common + "/preamble}\n"
                "\\input{" + common + "/propers-format}\n"
                "\\input{" + common + "/propers-homily}\n"
                + attack + "\n\\begin{document}\n"
                "\\typeout{TEXT-WIDTH=\\the\\textwidth}\n"
                "\\begin{properhomily}\\typeout{SPOOF-WIDTH=\\the\\linewidth}"
                "Rendered alias proof.\\end{properhomily}\n\\end{document}\n"
            )
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", source.name],
                cwd=self.root, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-2500:])
            values = dict(re.findall(r"(TEXT-WIDTH|SPOOF-WIDTH)=([0-9.]+)", result.stdout))
            self.assertGreater(float(values["SPOOF-WIDTH"]),
                               float(values["TEXT-WIDTH"]) * 0.75)
            entry.write_text(original.replace(r"\begin{document}",
                                              attack + "\n\\begin{document}"))
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, error):
                self.audit(edition="homily")
        entry.write_text(original)


if __name__ == "__main__":
    unittest.main()
