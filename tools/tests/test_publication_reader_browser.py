"""Real publication-reader interactions against a complete public-alpha artifact.

Run with TRIPTYCH_READER_BROWSER=1 and TRIPTYCH_READER_SITE pointing at the
already generated site. TRIPTYCH_READER_EVIDENCE selects an ignored scratch
directory for screenshots and measured reports. No synthetic publication body
or browser package is used. The server also exposes the /triptych/ project path.
"""
from __future__ import annotations

import base64
import functools
import http.server
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import threading
import time
import unittest
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
LEAF = "gpt/liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany"
FULL = "web/" + LEAF + ".html"
SYNTHESIS = "print/" + LEAF + "-synthesis.html"
HOMILY = "print/" + LEAF + "-homily.html"
OTHER = "web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.html"
CATALOGUE = "library/traditional-latin-mass.html"
ROUTES = (FULL, SYNTHESIS, HOMILY, OTHER)
VIEWPORTS = ((1440, 900), (1024, 768), (768, 1024), (393, 852), (320, 852))


class QuietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def translate_path(self, path):
        if path.startswith("/triptych/"):
            path = path[len("/triptych"):]
        return super().translate_path(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class ReaderBrowser:
    """Small stdlib WebDriver client, also usable for baseline evidence capture."""

    def __init__(self, evidence):
        self.evidence = Path(evidence)
        self.evidence.mkdir(parents=True, exist_ok=True)
        chrome = os.environ.get("TRIPTYCH_CHROME", "/usr/bin/chromium")
        driver = shutil.which("chromedriver")
        if not Path(chrome).is_file() or not driver:
            raise RuntimeError("Chromium and chromedriver are required")
        with socket.socket() as port:
            port.bind(("127.0.0.1", 0))
            driver_port = port.getsockname()[1]
        self.webdriver = f"http://127.0.0.1:{driver_port}"
        self.log = (self.evidence / "chromedriver.log").open("w")
        # Chrome's Unix socket name includes TMPDIR. Keep the relative path
        # short even when evidence is nested beneath descriptive test names.
        runtime = self.evidence.resolve()
        while len(os.path.relpath(runtime / "tmp", ROOT)) > 55:
            if runtime.parent == runtime or runtime == ROOT:
                raise RuntimeError("Choose a shorter scratch evidence directory")
            runtime = runtime.parent
        temporary = runtime / "tmp"
        temporary.mkdir(exist_ok=True)
        environment = {**os.environ, "TMPDIR": os.path.relpath(temporary, ROOT)}
        self.driver = subprocess.Popen([driver, f"--port={driver_port}"],
            stdout=self.log, stderr=self.log, cwd=ROOT, env=environment)
        self.session = None
        try:
            self.wait(lambda: self.request("GET", "/status"), timeout=10)
            value = self.request("POST", "/session", {"capabilities": {"alwaysMatch": {
                "browserName": "chrome", "goog:loggingPrefs": {"browser": "ALL"},
                "goog:chromeOptions": {"binary": chrome, "args": ["--headless=new",
                    "--no-sandbox", "--disable-dev-shm-usage",
                    "--disable-features=BackForwardCache"]}}}})
            self.session = "/session/" + value["sessionId"]
            self.viewport(1440, 900)
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.session:
            self.request("DELETE", self.session)
            self.session = None
        self.driver.terminate()
        self.driver.wait(timeout=10)
        self.log.close()

    def request(self, method, path, data=None):
        request = urllib.request.Request(self.webdriver + path, method=method,
            data=None if data is None else json.dumps(data).encode(),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                value = json.load(response)["value"]
        except urllib.error.HTTPError as error:
            with error:
                raise RuntimeError(error.read().decode()) from error
        if isinstance(value, dict) and "error" in value:
            raise RuntimeError(value)
        return value

    def command(self, path, data=None):
        return self.request("POST", self.session + path, data or {})

    def js(self, script, *args):
        return self.command("/execute/sync", {"script": script, "args": list(args)})

    def cdp(self, command, **params):
        return self.command("/goog/cdp/execute", {"cmd": command, "params": params})

    @staticmethod
    def wait(predicate, timeout=8):
        deadline = time.monotonic() + timeout
        last = None
        while time.monotonic() < deadline:
            try:
                value = predicate()
                if value:
                    return value
            except (OSError, RuntimeError) as error:
                last = error
            time.sleep(.05)
        raise AssertionError(f"Browser condition did not become true: {last}")

    def viewport(self, width, height):
        self.cdp("Emulation.setDeviceMetricsOverride", width=width, height=height,
                 deviceScaleFactor=1, mobile=False)

    def visit(self, url):
        self.command("/url", {"url": url})
        self.wait(lambda: self.js("return document.readyState === 'complete'"))
        time.sleep(.15)

    def screenshot(self, name):
        data = self.request("GET", self.session + "/screenshot")
        target = self.evidence / (name + ".png")
        target.write_bytes(base64.b64decode(data))
        return str(target)

    def click(self, selector):
        element = self.command("/element", {"using": "css selector", "value": selector})
        identity = element["element-6066-11e4-a52e-4f735466cecf"]
        self.command("/element/" + identity + "/click")


@unittest.skipUnless(os.environ.get("TRIPTYCH_READER_BROWSER") == "1",
                     "set TRIPTYCH_READER_BROWSER=1 for real publication-reader checks")
class PublicationReaderBrowserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = Path(os.environ.get("TRIPTYCH_READER_SITE", ROOT / "build/public-alpha/site"))
        missing = [route for route in ROUTES if not (cls.site / route).is_file()]
        if missing:
            raise RuntimeError("Generate the complete public-alpha artifact first: " + ", ".join(missing))
        cls.evidence = Path(os.environ.get("TRIPTYCH_READER_EVIDENCE",
            ROOT / ".scratch/reader-redesign-20261103/browser/after"))
        cls.evidence.mkdir(parents=True, exist_ok=True)
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
            functools.partial(QuietServer, directory=cls.site))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.origin = f"http://127.0.0.1:{cls.server.server_port}/"

    def setUp(self):
        self.browser = ReaderBrowser(self.evidence / self._testMethodName)
        self.addCleanup(self.browser.close)

    def visit(self, route):
        self.browser.visit(self.origin + route)
        self.assertEqual(self.browser.js("return document.querySelectorAll('main').length"), 1)
        self.assertTrue(self.browser.js("return !!document.querySelector('[data-reader-content]')"))

    def assert_console_clean(self):
        errors = self.browser.command("/log", {"type": "browser"})
        self.assertEqual([entry for entry in errors if entry["level"] == "SEVERE"], [])

    def test_reading_width_reflow_and_actual_tables(self):
        report = []
        for route in ROUTES:
            self.visit(route)
            for width, height in VIEWPORTS:
                self.browser.viewport(width, height)
                self.browser.js("scrollTo({top:0,behavior:'instant'})")
                metrics = self.browser.js("""const content=document.querySelector('[data-reader-content]');
                    return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,
                      contentWidth:content.getBoundingClientRect().width,
                      tables:[...content.querySelectorAll('table')].map(t=>({width:t.getBoundingClientRect().width,
                        client:t.parentElement.clientWidth,scroll:t.parentElement.scrollWidth})),
                      textLength:content.innerText.length,headings:content.querySelectorAll('h2,h3,h4').length};""")
                report.append({"route": route, **metrics})
                self.browser.screenshot(Path(route).stem + f"-{width}")
                if metrics["tables"] and width in (1440, 393, 320):
                    self.browser.js("document.querySelector('[data-reader-content] table').scrollIntoView({block:'start',behavior:'instant'});scrollBy({top:-160,behavior:'instant'})")
                    self.browser.screenshot(Path(route).stem + f"-table-{width}")
                with self.subTest(route=route, width=width):
                    self.assertLessEqual(metrics["documentWidth"], width + 1)
                    self.assertGreater(metrics["textLength"], 1000)
                    if width == 1440:
                        self.assertGreaterEqual(metrics["contentWidth"], 800)
                    if width <= 393:
                        self.assertGreaterEqual(metrics["contentWidth"], width - 64)
            self.assert_console_clean()
        (self.evidence / "layout.json").write_text(json.dumps(report, indent=2))
        desktop = [row["contentWidth"] for row in report if row["width"] == 1440]
        self.assertLessEqual(max(desktop) - min(desktop), 80)

    def test_source_spanned_chronology_notes_keep_the_reading_width(self):
        routes = (
            "web/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.html",
            "web/gpt/liturgy/roman-rite/1962/propers/temporal/43-third-after-pentecost.html",
        )
        report = []
        for route in routes:
            self.visit(route)
            for width, height in ((1440, 900), (390, 844)):
                self.browser.viewport(width, height)
                metrics = self.browser.js("""const content=document.querySelector('[data-reader-content]');
                    const tables=[...content.querySelectorAll('table')].filter(table=>{
                      const heading=table.querySelector('thead')?.innerText || '';
                      return heading.includes('Location') && heading.includes('Date');
                    });
                    return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,
                      notes:tables.flatMap(table=>[...table.querySelectorAll('td[colspan="4"]')].map(cell=>{
                        const bounds=cell.getBoundingClientRect(),row=cell.parentElement.getBoundingClientRect();
                        return {text:cell.innerText.length,cells:cell.parentElement.children.length,
                          width:bounds.width,rowWidth:row.width,left:bounds.left-row.left,
                          client:cell.clientWidth,scroll:cell.scrollWidth};
                      }))};""")
                report.append({"route": route, **metrics})
                with self.subTest(route=route, width=width):
                    self.assertTrue(metrics["notes"], "Source multicolumn notes were lost")
                    self.assertLessEqual(metrics["documentWidth"], metrics["width"] + 1)
                    for note in metrics["notes"]:
                        self.assertGreater(note["text"], 20)
                        self.assertEqual(note["cells"], 1)
                        self.assertLessEqual(abs(note["left"]), 2)
                        self.assertLessEqual(abs(note["width"] - note["rowWidth"]), 2)
                        self.assertLessEqual(note["scroll"], note["client"] + 1)
                self.assert_console_clean()
        (self.evidence / "source-spanned-chronology.json").write_text(
            json.dumps(report, indent=2) + "\n")

    def test_section_links_focus_reload_and_back(self):
        for prefix in ("", "triptych/"):
            self.visit(prefix + FULL)
            links = self.browser.js("""return [...document.querySelectorAll('[data-reader-toc] a[href^="#"]')]
                .map(a=>({href:a.hash,text:a.textContent.trim(),exists:!!document.getElementById(decodeURIComponent(a.hash.slice(1)))}));""")
            self.assertGreater(len(links), 3)
            self.assertTrue(all(link["exists"] for link in links))
            target = links[len(links) // 2]["href"]
            self.browser.js("document.querySelector('[data-reader-toc]').open=true;", target)
            self.browser.js("document.querySelector('[data-reader-toc] a[href='+CSS.escape(arguments[0])+']').click()", target)
            self.browser.wait(lambda: self.browser.js("return location.hash") == target)
            # Native fragments move the sequential keyboard starting point without
            # mutating the sealed body's headings to add tabindex attributes.
            self.browser.command("/actions", {"actions": [{"type": "key", "id": "keyboard", "actions": [
                {"type": "keyDown", "value": "\ue004"}, {"type": "keyUp", "value": "\ue004"}]}]})
            self.assertTrue(self.browser.js("return !!document.activeElement.closest('[data-reader-content]')"))
            self.browser.command("/refresh")
            time.sleep(.2)
            top = self.browser.js("return document.getElementById(decodeURIComponent(location.hash.slice(1))).getBoundingClientRect().top")
            self.assertGreaterEqual(top, -2)
            self.assertLess(top, 250)
            self.browser.command("/back")
            self.browser.wait(lambda: not self.browser.js("return location.hash"))
            self.assert_console_clean()

    def test_treatments_and_neighbor_sundays_are_real_routes(self):
        for prefix in ("", "triptych/"):
            self.visit(prefix + FULL)
            treatments = self.browser.js("return [...document.querySelectorAll('.publication-reader__treatments a')].map(a=>a.textContent.trim())")
            self.assertEqual(treatments, ["Full Study Guide", "Synthesis", "Homily"])
            for label in treatments:
                self.browser.js("[...document.querySelectorAll('.publication-reader__treatments a')].find(a=>a.textContent.trim()===arguments[0]).click()", label)
                self.browser.wait(lambda: self.browser.js("return document.querySelector('.publication-reader__treatments [aria-current=page]')?.textContent.trim()") == label)
                self.assertTrue(self.browser.js("return location.pathname").startswith("/" + prefix))
                self.assertGreater(self.browser.js("return document.querySelector('[data-reader-content]').innerText.length"), 1000)
                self.assert_console_clean()
            current = self.browser.js("return location.href")
            previous = self.browser.js("return document.querySelector('.publication-reader__browse a[rel=prev]').href")
            self.assertNotEqual(previous, current)
            self.browser.js("document.querySelector('.publication-reader__browse a[rel=prev]').click()")
            self.browser.wait(lambda: self.browser.js("return location.href") == previous)
            self.assertEqual(self.browser.js("return document.querySelector('.publication-reader__treatments [aria-current=page]').textContent.trim()"), "Homily")
            self.browser.js("document.querySelector('.publication-reader__browse a[rel=next]').click()")
            self.browser.wait(lambda: "66-" in self.browser.js("return location.pathname"))
            self.assert_console_clean()

    def test_history_restores_reader_and_catalogue_positions(self):
        self.browser.visit(self.origin + CATALOGUE)
        self.browser.js("const a=document.querySelector('a[href$=\"66-resumed-fifth-after-epiphany.html\"]');a.scrollIntoView({block:'center',behavior:'instant'});")
        catalogue_y = self.browser.js("return scrollY")
        self.browser.js("document.querySelector('a[href$=\"66-resumed-fifth-after-epiphany.html\"]').click()")
        self.browser.wait(lambda: bool(self.browser.js("return document.querySelector('[data-reader-content]')")))
        self.browser.js("scrollTo({top:2600,behavior:'instant'})")
        time.sleep(.2)
        reader_y = self.browser.js("return scrollY")
        self.browser.js("document.querySelector('.publication-reader__treatments a:nth-child(2)').click()")
        self.browser.wait(lambda: "synthesis" in self.browser.js("return location.pathname"))
        self.browser.command("/back")
        time.sleep(.35)
        self.assertAlmostEqual(self.browser.js("return scrollY"), reader_y, delta=3)
        self.browser.command("/back")
        time.sleep(.35)
        self.assertAlmostEqual(self.browser.js("return scrollY"), catalogue_y, delta=3)
        self.browser.command("/forward")
        time.sleep(.35)
        self.assertAlmostEqual(self.browser.js("return scrollY"), reader_y, delta=3)
        self.assert_console_clean()

    def test_selector_keyboard_and_accessible_names(self):
        for route in (FULL, SYNTHESIS, HOMILY):
            self.visit(route)
            result = self.browser.cdp("Accessibility.getFullAXTree")
            (self.evidence / (Path(route).stem + "-accessibility.json")).write_text(json.dumps(result, indent=2))
            exposed = [node for node in result["nodes"] if not node.get("ignored")]
            unnamed = [node for node in exposed if
                       node.get("role", {}).get("value") in {"button", "combobox", "link"} and
                       not node.get("name", {}).get("value", "").strip()]
            self.assertEqual(unnamed, [])
            roles = [node.get("role", {}).get("value") for node in exposed]
            self.assertEqual(roles.count("main"), 1)
            self.assertIn("heading", roles)
            names = [node.get("name", {}).get("value") for node in exposed]
            self.assertIn("Treatments", names)
            self.assertIn("Document sections", names)
        self.visit(FULL)
        self.browser.js("document.querySelector('[data-reader-document-select]').focus()")
        outline = self.browser.js("return getComputedStyle(document.activeElement).outlineWidth")
        self.assertGreater(float(outline.removesuffix("px")), 0)
        selection = self.browser.js("""const s=document.querySelector('[data-reader-document-select]');
            s.selectedIndex=Math.max(0,s.selectedIndex-1);const target=new URL(s.value,location.href).href;
            s.dispatchEvent(new Event('change',{bubbles:true}));return target;""")
        self.browser.wait(lambda: self.browser.js("return location.href") == selection)
        self.assert_console_clean()

    def test_no_script_and_unavailable_storage_keep_navigation(self):
        self.browser.cdp("Emulation.setScriptExecutionDisabled", value=True)
        self.visit(SYNTHESIS)
        self.browser.click('.publication-reader__treatments a:last-child')
        self.browser.wait(lambda: "homily" in self.browser.js("return location.pathname"))
        self.assertGreater(self.browser.js("return document.querySelector('[data-reader-content]').innerText.length"), 1000)
        self.browser.cdp("Emulation.setScriptExecutionDisabled", value=False)
        self.browser.cdp("Page.addScriptToEvaluateOnNewDocument", source="Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage unavailable')}})")
        self.visit(FULL)
        self.browser.js("document.querySelector('[data-reader-toc] a:nth-of-type(1)').click()")
        self.browser.wait(lambda: bool(self.browser.js("return location.hash")))
        self.assert_console_clean()

    def test_forced_colors_reduced_motion_and_text_reflow(self):
        self.browser.cdp("Emulation.setEmulatedMedia", features=[
            {"name": "forced-colors", "value": "active"},
            {"name": "prefers-reduced-motion", "value": "reduce"}])
        self.browser.viewport(320, 852)
        self.visit(FULL)
        self.browser.screenshot("forced-colors-reduced-motion-320")
        self.assertLessEqual(self.browser.js("return document.documentElement.scrollWidth"), 321)
        self.browser.cdp("Emulation.setEmulatedMedia", features=[])
        self.browser.viewport(1440, 900)
        self.browser.js("document.documentElement.style.fontSize='200%'")
        self.assertLessEqual(self.browser.js("return document.documentElement.scrollWidth"), 1441)
        self.browser.screenshot("text-200-percent-1440")

    def test_missal_apps_keep_their_own_reader(self):
        for route in ("liturgy/day.html", "liturgy/propers-reader.html"):
            for prefix in ("", "triptych/"):
                self.browser.visit(self.origin + prefix + route)
                self.assertEqual(self.browser.js("return document.querySelectorAll('main').length"), 1)
                self.assertFalse(self.browser.js("return !!document.querySelector('.publication-reader')"))
                assets = self.browser.js("return [...document.querySelectorAll('script[src],link[rel=stylesheet]')].map(e=>e.src||e.href)")
                self.assertFalse(any("publication-reader." in asset for asset in assets))

    def test_complete_print_uses_native_pdf_protocol_without_browser_printing(self):
        # This bounded integration test exercises the real page's selection,
        # native controller and browser download with an explicit compiler
        # response fixture. It does not compile TeX or assess PDF typography.
        # Real engine/content/font acceptance runs separately on the built site.
        payload = b"%PDF-1.4\n% Synthetic native-print protocol fixture\n%%EOF\n"
        published = json.loads((self.site / "PUBLICATION-MANIFEST.json").read_text())
        self.visit(FULL)
        address = self.browser.js("return document.querySelector('[data-web-print-reader] .print-actions a').href")
        self.assertEqual(address, self.origin + "print/" + LEAF + ".html?print=1")
        for route in ("print/" + LEAF + ".html", SYNTHESIS, HOMILY):
            self.visit(route)
            downloads = (self.evidence / self._testMethodName / Path(route).stem / "downloads").resolve()
            shutil.rmtree(downloads, ignore_errors=True)
            downloads.mkdir(parents=True, exist_ok=True)
            self.browser.cdp("Browser.setDownloadBehavior", behavior="allow", downloadPath=str(downloads))
            self.browser.js("""
                window.readerPrintCalls=0;
                window.print=()=>{window.readerPrintCalls++;};
                window.readerCompilerCalls=[];
                const fixture=Uint8Array.from(arguments[0]);
                window.TriptychNativeTeX=Object.freeze({generate:async options=>{
                  window.readerCompilerCalls.push({bundle:options.bundleURL,runtime:options.runtimeURL,
                    bundle_sha256:options.bundleSHA256,runtime_sha256:options.runtimeSHA256});
                  const hash=await crypto.subtle.digest('SHA-256',fixture);
                  return {bytes:fixture,byteLength:fixture.byteLength,
                    sha256:[...new Uint8Array(hash)].map(n=>n.toString(16).padStart(2,'0')).join('')};
                }});""", list(payload))
            self.browser.click('[data-native-print-start]')
            self.browser.wait(lambda: self.browser.js("return document.querySelector('[data-native-print]').dataset.nativePrintState==='ready'"), timeout=15)
            result = self.browser.js("""return {
                selection:JSON.parse(document.querySelector('[data-native-print-manifest]').textContent),
                compiler:window.readerCompilerCalls,printCalls:window.readerPrintCalls,
                frames:document.querySelectorAll('[data-web-print-frame]').length,
                download:document.querySelector('[data-native-print-download]').download,
                downloadVisible:!document.querySelector('[data-native-print-download]').hidden};""")
            self.assertEqual(result["selection"]["id"], "publication:" + route.removeprefix("print/").removesuffix(".html"))
            self.assertEqual(result["selection"]["document"], "publication:" + LEAF)
            self.assertEqual(result["selection"]["edition"], "synthesis" if route == SYNTHESIS else "homily" if route == HOMILY else "main")
            self.assertEqual(result["selection"]["source_revision"], published["native_print"]["source_revision"])
            self.assertEqual(len(result["compiler"]), 1)
            self.assertEqual(result["compiler"][0]["bundle"], urllib.parse.urljoin(self.origin + route, result["selection"]["wasm"]["bundle"]))
            self.assertEqual(result["compiler"][0]["runtime"], urllib.parse.urljoin(self.origin + route, result["selection"]["wasm"]["runtime"]))
            self.assertEqual(result["compiler"][0]["bundle_sha256"], result["selection"]["wasm"]["bundle_sha256"])
            self.assertEqual(result["compiler"][0]["runtime_sha256"], result["selection"]["wasm"]["runtime_sha256"])
            self.assertEqual(result["printCalls"], 0)
            self.assertEqual(result["frames"], 0)
            self.assertTrue(result["downloadVisible"])
            downloaded = downloads / result["download"]
            self.browser.wait(lambda: downloaded.is_file(), timeout=15)
            self.assertEqual(downloaded.read_bytes(), payload)
            result["synthetic_fixture_sha256"] = hashlib.sha256(payload).hexdigest()
            self.assert_console_clean()
            (self.evidence / (Path(route).stem + "-print.json")).write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    unittest.main()
