"""Real layout regression for enlarged source titles in the published shell.

The small DOM fixture asserts no historical fact and is not site acceptance.
It uses the three owning stylesheets in their actual published load order.
"""
from __future__ import annotations

import html
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import urllib.parse

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("history_browser", ROOT / "scripts/_history_browser_acceptance.py")
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
TITLE = ("Խորհրդատետր [Khorhrdatetr] / Lyturgia Armena, Rome 1677: "
         "FSL A/711, distinct 19-page setting with correction appendices")


class HistoryNarrowTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("chromedriver") or not shutil.which("chromium"):
            raise unittest.SkipTest("Chromium and chromedriver are required")
        scratch = owner.inside(ROOT, Path(os.environ.get(
            "HISTORY_NARROW_TEST_SCRATCH", ".scratch/history-narrow-tests")))
        if not scratch.is_relative_to(ROOT / ".scratch"):
            raise ValueError("test outputs must remain in repository scratch")
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        cls.addClassCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        document = directory / "title.html"
        document.write_text("""<!doctype html><html lang="en"><meta charset="utf-8">
<link rel="stylesheet" href="/release/public-alpha/assets/site.css">
<link rel="stylesheet" href="/src/web/browser/shared/browser-core.css">
<link rel="stylesheet" href="/src/web/browser/history/history.css">
<body><header class="site-header"></header>
<main class="page-shell page-browser section-toned section-green history-page">
<section id="catalogue-detail" class="panel"><h3 class="panel-title">""" +
            html.escape(TITLE) + "</h3><p>Source metadata remains below the complete title.</p></section></main>",
            encoding="utf-8")
        output = directory / "browser"
        output.mkdir()
        cls.browser = owner.Browser(ROOT, output, "http://127.0.0.1:0/history/", ROOT)
        cls.addClassCleanup(cls.browser.close)
        cls.browser.start()
        cls.url = urllib.parse.urljoin(cls.browser.url, "/" + document.relative_to(ROOT).as_posix())

    def measure(self, width, text_size):
        b = self.browser
        b.cdp("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        b.call("POST", "/url", {"url": self.url})
        b.js("document.documentElement.style.fontSize=arguments[0]", text_size)
        return b.js("""const t=document.querySelector('.panel-title'),c=getComputedStyle(t);
const words=[...t.textContent.matchAll(/\\S+/gu)].map(m=>{
 const r=document.createRange();r.setStart(t.firstChild,m.index);r.setEnd(t.firstChild,m.index+m[0].length);
 return {word:m[0],lines:new Set([...r.getClientRects()].map(p=>p.y)).size};
});return {text:t.textContent,fontSize:parseFloat(c.fontSize),words,
 client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth};""")

    def test_double_size_title_keeps_fitting_words_whole(self):
        measured = self.measure(320, "200%")
        words = {row["word"]: row["lines"] for row in measured["words"]}
        for word in ("[Khorhrdatetr]", "Lyturgia", "Armena,", "correction", "appendices"):
            with self.subTest(word=word):
                self.assertEqual(words[word], 1, "A fitting title word should wrap at its boundary")

    def test_enlargement_preserves_all_words_and_reflows(self):
        ordinary = self.measure(320, "100%")
        enlarged = self.measure(320, "200%")
        for measured in (ordinary, enlarged):
            self.assertEqual(measured["text"], TITLE)
            self.assertLessEqual(measured["scroll"], measured["client"])
        self.assertAlmostEqual(enlarged["fontSize"] / ordinary["fontSize"], 2)


if __name__ == "__main__":
    unittest.main()
