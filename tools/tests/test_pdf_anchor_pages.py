"""A titlesec heading's PDF destination must be on the heading's own page.

common/preamble installs hyperref's titlesec hooks. Without them a numbered
titlesec heading's anchor is set where its counter steps, so a heading that
titlesec moves to the next page leaves its anchor, and every contents link and
bookmark to it, on the page before. The build gate (tools/check-pdf-anchors)
reads anchor names and cannot see a page, so these tests prove the mechanism:
the hooks are installed, and a pushed heading keeps its destination.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DOCUMENT = r"""\input{%(preamble)s}
\usepackage[nobottomtitles*]{titlesec}
\renewcommand{\bottomtitlespace}{.25\textheight}
\begin{document}
\tableofcontents
\section{First heading}
%(filler)s
\section{Pushed heading}
Text after the pushed heading.
\section*{Unnumbered heading}
\addcontentsline{toc}{section}{Unnumbered heading}
\end{document}
"""


@unittest.skipUnless(shutil.which("pdflatex") and shutil.which("pdfinfo")
                     and shutil.which("pdftotext"), "requires TeX and Poppler")
class TitlesecAnchorPageTests(unittest.TestCase):
    def build(self, preamble: Path, filler_lines: int) -> tuple[dict[str, int], list[str]]:
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            filler = "\n\n".join(f"Paragraph {n} of filler text." for n in range(filler_lines))
            (build / "probe.tex").write_text(
                DOCUMENT % {"preamble": preamble.with_suffix("").as_posix(), "filler": filler})
            for _ in range(2):
                result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                         "probe.tex"], cwd=build, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout[-2000:])
            dests = subprocess.run(["pdfinfo", "-dests", "probe.pdf"], cwd=build,
                                   capture_output=True, text=True, check=True).stdout
            pages = {name: int(page) for page, name in
                     re.findall(r"^\s*(\d+)\s+\[.*?\]\s+\"([^\"]+)\"", dests, re.M)}
            text = subprocess.run(["pdftotext", "probe.pdf", "-"], cwd=build,
                                  capture_output=True, text=True, check=True).stdout.split("\f")
            return pages, text

    def heading_page(self, text: list[str], heading: str) -> int:
        found = [index + 1 for index, page in enumerate(text) if heading in page]
        return found[-1]  # the contents page names it too; the heading comes last

    def pushed_case(self, preamble: Path) -> tuple[int, int, dict[str, int], list[str]]:
        # Grow the filler until titlesec pushes the second heading to a new page.
        for lines in range(30, 90):
            pages, text = self.build(preamble, lines)
            heading = self.heading_page(text, "Pushed heading")
            first = self.heading_page(text, "Paragraph 0 of filler")
            if heading > first:
                return heading, lines, pages, text
        self.fail("no filler length pushed the heading to the next page")

    def test_pushed_numbered_heading_keeps_its_anchor(self):
        heading, _, pages, _ = self.pushed_case(ROOT / "src/common/preamble.tex")
        self.assertEqual(pages["section.2"], heading)

    def hook_meanings(self, preamble: Path) -> tuple[str, str]:
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            (build / "hooks.tex").write_text(
                "\\input{" + preamble.with_suffix("").as_posix() + "}\n\\usepackage{titlesec}\n"
                "\\begin{document}\\makeatletter\n"
                "\\typeout{STEP=\\meaning\\ttl@Hy@steplink}\n"
                "\\typeout{REF=\\meaning\\ttl@Hy@refstepcounter}\n"
                "\\makeatother x\\end{document}\n")
            result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                     "hooks.tex"], cwd=build, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout[-2000:])
            log = (build / "hooks.log").read_text(errors="replace").replace("\n", "")
            step = re.search(r"STEP=(.*?)REF=", log, re.S).group(1)
            ref = re.search(r"REF=(.*?)(?:\)|$)", log, re.S).group(1)
            return step, ref

    def test_titlesec_loaded_after_the_preamble_gets_hyperrefs_hooks(self):
        step, ref = self.hook_meanings(ROOT / "src/common/preamble.tex")
        self.assertIn("Hy@MakeCurrentHrefAuto", step)
        self.assertIn("Hy@raisedlink", ref)

    def test_without_the_preamble_hooks_titlesec_gobbles_the_anchor(self):
        # The guard is real: with the hooks removed, titlesec's own fallback
        # leaves unnumbered headings without an anchor and numbered ones
        # anchored where the counter steps.
        source = (ROOT / "src/common/preamble.tex").read_text()
        start = source.index("\\def\\tpt@ttl@steplink")
        end = source.index("\\makeatother", source.index("\\AddToHook{package/titlesec/after}"))
        with tempfile.TemporaryDirectory() as temporary:
            stripped = Path(temporary) / "preamble.tex"
            stripped.write_text(source[:start] + source[end:])
            step, ref = self.hook_meanings(stripped)
        # \\@gobble: its meaning is an empty body that takes one argument.
        self.assertEqual(step.strip(), "\\long macro:#1->")
        self.assertNotIn("Hy@raisedlink", ref)

if __name__ == "__main__":
    unittest.main()
