"""Real generated catalogue geometry and navigation, with no browser packages.

Run with TRIPTYCH_CATALOGUE_BROWSER=1, TRIPTYCH_CHROME and
TRIPTYCH_CATALOGUE_EVIDENCE (an ignored scratch directory). Requires chromedriver.
The server disables caching so history must also work without the back/forward cache.
"""
from __future__ import annotations

import base64
import functools
import http.server
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import threading
import time
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = "library/traditional-latin-mass.html"
PROPER = "web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.html"
OTHER = "web/gpt/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.html"
SYNTHESIS = PROPER.removesuffix(".html") + "-synthesis.html"
HOMILY = PROPER.removesuffix(".html") + "-homily.html"
PRINT_PROPER = PROPER.replace("web/", "print/", 1)
PRINT_SYNTHESIS = SYNTHESIS.replace("web/", "print/", 1)
ROW = "[...document.querySelectorAll('tbody tr')].find(r=>r.cells[0].textContent.trim()==='57')"
TABLE = f"{ROW}.closest('table')"


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


@unittest.skipUnless(os.environ.get("TRIPTYCH_CATALOGUE_BROWSER") == "1",
                     "set TRIPTYCH_CATALOGUE_BROWSER=1 for real Chromium catalogue checks")
class CatalogueNavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome = os.environ.get("TRIPTYCH_CHROME", "/usr/bin/chromium")
        driver = shutil.which("chromedriver")
        if not Path(chrome).is_file() or not driver:
            raise unittest.SkipTest("Chromium and chromedriver are required")
        cls.evidence = Path(os.environ.get(
            "TRIPTYCH_CATALOGUE_EVIDENCE", ROOT / ".scratch/catalogue-navigation"))
        cls.evidence.mkdir(parents=True, exist_ok=True)
        cls.site = cls.evidence / "site"
        loader = importlib.machinery.SourceFileLoader("catalogue_site", str(ROOT / "tools/public-alpha"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        with tool.held_repository_inputs():
            manifest = tool.load_manifest()
            included = tool.included_publications(tool.publication_map(manifest), False)
            authorization = tool.artifact_authorization(manifest, included)
            cls.catalogues = {route: source for source, route in tool.PAGE_MAP.items()
                              if source == "README.md" or source.startswith("library/")}
            for route, source in cls.catalogues.items():
                target = cls.site / route
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(tool.render_source_page(
                    source, route, set(included), False, authorization))
            # Use the production source-first renderer for both reviewed readers and
            # truthful print-option pages; no installed PDF is a fixture input.
            for route in (PROPER, OTHER, SYNTHESIS, HOMILY, PRINT_PROPER, PRINT_SYNTHESIS):
                _, provider, leaf = route.removesuffix(".html").split("/", 2)
                if (provider, leaf) not in included:
                    raise AssertionError(f"browser fixture publication is not admitted: {provider}/{leaf}")
                target = cls.site / route
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(tool.render_publication_print_page(
                    provider, leaf, route, False, authorization))
            for asset in ("site.css", "icon.png", "social-card.png"):
                destination = cls.site / "assets" / asset
                destination.parent.mkdir(parents=True, exist_ok=True)
                source = ROOT / "release/public-alpha/assets" / asset
                if asset == "site.css" and os.environ.get("TRIPTYCH_CATALOGUE_CSS"):
                    source = Path(os.environ["TRIPTYCH_CATALOGUE_CSS"])
                shutil.copyfile(source, destination)
            destination = cls.site / "shared/catalogue-navigation.js"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "src/web/browser/shared/catalogue-navigation.js", destination)
            for route, source in tool.web_browser_pages().items():
                page = tool.render_browser_page(source, route, False, {})
                if 'class="catalogue-table' in page or 'shared/catalogue-navigation.js' in page:
                    raise AssertionError(f"app opted into landing component: {route}")
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
            functools.partial(QuietServer, directory=cls.site))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.origin = f"http://127.0.0.1:{cls.server.server_port}/"
        with socket.socket() as port:
            port.bind(("127.0.0.1", 0))
            driver_port = port.getsockname()[1]
        cls.webdriver = f"http://127.0.0.1:{driver_port}"
        log = (cls.evidence / "chromedriver.log").open("w")
        cls.addClassCleanup(log.close)
        cls.driver = subprocess.Popen([driver, f"--port={driver_port}"], stdout=log, stderr=log)
        cls.addClassCleanup(cls.stop_driver)
        for _ in range(100):
            try:
                cls.request("GET", "/status")
                break
            except OSError:
                time.sleep(.05)
        else:
            raise RuntimeError("chromedriver did not start")
        cls.chrome = chrome

    @classmethod
    def stop_driver(cls):
        cls.driver.terminate()
        cls.driver.wait(timeout=10)

    @classmethod
    def request(cls, method, path, data=None):
        request = urllib.request.Request(cls.webdriver + path, method=method,
            data=None if data is None else json.dumps(data).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=20) as response:
            value = json.load(response)["value"]
        if isinstance(value, dict) and "error" in value:
            raise RuntimeError(value)
        return value

    def setUp(self):
        value = self.request("POST", "/session", {"capabilities": {"alwaysMatch": {
            "browserName": "chrome", "goog:loggingPrefs": {"browser": "ALL"},
            "goog:chromeOptions": {"binary": self.chrome, "args": ["--headless=new",
                "--no-sandbox", "--disable-dev-shm-usage", "--disable-features=BackForwardCache"]}}}})
        self.session = "/session/" + value["sessionId"]
        self.addCleanup(lambda: self.request("DELETE", self.session))
        self.viewport(1440, 900)

    def command(self, path, data=None):
        return self.request("POST", self.session + path, data or {})

    def run_js(self, script):
        return self.command("/execute/sync", {"script": script, "args": []})

    def viewport(self, width, height):
        self.command("/goog/cdp/execute", {"cmd": "Emulation.setDeviceMetricsOverride",
            "params": {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False}})

    def visit(self, route):
        self.command("/url", {"url": self.origin + route})
        time.sleep(.1)

    def screenshot(self, name):
        data = self.request("GET", self.session + "/screenshot")
        (self.evidence / (name + ".png")).write_bytes(base64.b64decode(data))

    def catalogue_position(self):
        return self.run_js("return scrollY")

    def focused_table_links(self):
        return self.run_js("""return [...document.querySelectorAll('.catalogue-table td a')].map(a=>{a.focus();const b=a.getBoundingClientRect(),h=a.closest('table').tHead.getBoundingClientRect(),s=getComputedStyle(a),ring=parseFloat(s.outlineWidth)+parseFloat(s.outlineOffset);return {text:a.textContent,top:b.top,headerBottom:Math.max(0,h.bottom),visible:b.top-ring>=Math.max(0,h.bottom)-1&&b.bottom+ring<=innerHeight+1};});""")

    def test_density_sticky_headers_and_reflow(self):
        report = []
        for route in (CATALOGUE, "library/novus-ordo-liturgy.html"):
            self.visit(route)
            for width, height in ((1440, 900), (1024, 768), (768, 1024), (393, 852), (320, 852)):
                self.viewport(width, height)
                # Compare the same real table section before and after at every size.
                self.run_js("const r=[...document.querySelectorAll('tbody tr')].find(r=>r.textContent.includes('Eleventh')&&r.textContent.includes('Read'));r.scrollIntoView({behavior:'instant',block:'start'});scrollBy({top:-r.closest('table').tHead.getBoundingClientRect().height-8,behavior:'instant'});")
                time.sleep(.05)
                metrics = self.run_js("""const row=[...document.querySelectorAll('tbody tr')].find(r=>r.textContent.includes('Eleventh')&&r.textContent.includes('Read'));const table=row.closest('table');const head=table.tHead;return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,rowHeight:row.getBoundingClientRect().height,headerTop:head.getBoundingClientRect().top,headerBottom:head.getBoundingClientRect().bottom,visibleRows:[...table.tBodies[0].rows].filter(r=>{const b=r.getBoundingClientRect();return b.top>=Math.max(0,head.getBoundingClientRect().bottom)&&b.bottom<=innerHeight}).length,headers:[...head.querySelectorAll('th')].map(h=>({text:h.textContent,scope:h.scope}))};""")
                report.append({"route": route, **metrics})
                self.screenshot(Path(route).stem + f"-{width}")
            ax = self.command("/goog/cdp/execute", {"cmd": "Accessibility.getFullAXTree", "params": {}})
            roles = [node.get("role", {}).get("value") for node in ax["nodes"]]
            self.assertIn("table", roles)
            self.assertIn("columnheader", roles)
        (self.evidence / "layout.json").write_text(json.dumps(report, indent=2))
        for metrics in report:
            with self.subTest(route=metrics["route"], width=metrics["width"]):
                self.assertLessEqual(metrics["documentWidth"], metrics["width"])
                self.assertAlmostEqual(metrics["headerTop"], 0, delta=1)
                self.assertTrue(all(h["scope"] == "col" for h in metrics["headers"]))
                if metrics["width"] == 1440:
                    self.assertGreaterEqual(metrics["visibleRows"], 16)

    def test_history_and_breadcrumb_return(self):
        self.visit(CATALOGUE)
        self.run_js(f"{ROW}.scrollIntoView({{behavior:'instant',block:'center'}})")
        catalogue_y = self.catalogue_position()
        self.run_js(f"{ROW}.querySelector('a[href$=\"57-seventeenth-after-pentecost.html\"]').click()")
        time.sleep(.15)
        self.assertTrue(self.run_js("return location.pathname").endswith(PROPER))
        self.run_js("scrollTo({top:2400,behavior:'instant'})")
        proper_y = self.catalogue_position()
        self.command("/back")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), catalogue_y, delta=2)
        self.command("/forward")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), proper_y, delta=2)
        self.run_js("document.querySelector('.breadcrumb a[href$=\"traditional-latin-mass.html\"]').click()")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), catalogue_y, delta=2)
        self.run_js("document.querySelector('a[href$=\"59-nineteenth-after-pentecost.html\"]').click()")
        time.sleep(.15)
        self.assertTrue(self.run_js("return location.pathname").endswith(OTHER))
        self.command("/back")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), catalogue_y, delta=2)
        (self.evidence / "history.json").write_text(json.dumps({
            "catalogueY": catalogue_y, "properY": proper_y,
            "backForwardCache": "disabled", "breadcrumbReturn": True,
            "secondProperLink": True}, indent=2))

    def test_explicit_anchor_and_storage_unavailable(self):
        self.command("/goog/cdp/execute", {"cmd": "Page.addScriptToEvaluateOnNewDocument",
            "params": {"source": "history.replaceState=()=>{throw new Error('State blocked')};Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage blocked')}})"}})
        self.visit(CATALOGUE + "#sunday-propers-calendar")
        self.assertAlmostEqual(self.run_js("return document.querySelector('#sunday-propers-calendar').getBoundingClientRect().top"), 0, delta=2)
        self.run_js(f"{ROW}.scrollIntoView({{behavior:'instant',block:'center'}})")
        before = self.catalogue_position()
        self.run_js(f"{ROW}.querySelector('a[href$=\"57-seventeenth-after-pentecost.html\"]').click()")
        time.sleep(.15)
        self.command("/back")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), before, delta=2)
        errors = self.command("/log", {"type": "browser"})
        self.assertEqual([entry for entry in errors if entry["level"] == "SEVERE"], [])

    def test_source_first_companions_and_print_return(self):
        report = []
        for prefix in ("", "triptych/"):
            for route in (SYNTHESIS, HOMILY):
                self.visit(prefix + CATALOGUE)
                links = self.run_js(f"return [...{ROW}.cells[2].querySelectorAll('a')].map(a=>({{text:a.textContent,path:new URL(a.href).pathname}}))")
                self.assertEqual({link["path"] for link in links},
                                 {"/" + prefix + path for path in (PROPER, SYNTHESIS, HOMILY)})
                self.assertFalse(any("PDF" in link["text"] for link in links), links)
                self.run_js(f"{ROW}.scrollIntoView({{behavior:'instant',block:'center'}})")
                before = self.catalogue_position()
                self.run_js(f"{ROW}.querySelector('a[href$=\"{Path(route).name}\"]').click()")
                time.sleep(.15)
                self.assertTrue(self.run_js("return location.pathname").endswith(route))
                self.assertIn("A browser reading edition is not available for this output.",
                              self.run_js("return document.querySelector('main').innerText"))
                self.assertEqual(self.run_js("return document.querySelectorAll('.catalogue-table,script[src$=\"catalogue-navigation.js\"]').length"), 0)
                self.command("/back")
                time.sleep(.15)
                self.assertAlmostEqual(self.catalogue_position(), before, delta=2)
                self.command("/forward")
                time.sleep(.15)
                self.assertTrue(self.run_js("return location.pathname").endswith(route))
                report.append({"prefix": prefix, "route": route, "catalogueY": before,
                               "nativeBackForward": True, "printOptionsNotice": True})

            for landing, print_route, destination in (
                (CATALOGUE, PRINT_PROPER, '.breadcrumb a[href$="traditional-latin-mass.html"]'),
                ("index.html", PRINT_SYNTHESIS, '.site-header nav a[href$="index.html"]'),
            ):
                self.visit(prefix + landing)
                self.run_js("document.querySelector('main table').scrollIntoView({behavior:'instant',block:'start'});scrollBy({top:100,behavior:'instant'})")
                before = self.catalogue_position()
                self.assertGreater(before, 100)
                self.visit(prefix + print_route)
                self.assertEqual(self.run_js("return document.querySelectorAll('.catalogue-table,script[src$=\"catalogue-navigation.js\"]').length"), 0)
                self.run_js(f"document.querySelector({json.dumps(destination)}).click()")
                time.sleep(.15)
                self.assertEqual(self.run_js("return location.pathname"), "/" + prefix + landing)
                self.assertAlmostEqual(self.catalogue_position(), before, delta=2)
                report.append({"prefix": prefix, "route": print_route, "landing": landing,
                               "landingY": before, "ordinaryReturn": True})
        (self.evidence / "source-first-navigation.json").write_text(json.dumps(report, indent=2))

    def test_no_script_native_history(self):
        self.command("/goog/cdp/execute", {"cmd": "Emulation.setScriptExecutionDisabled",
            "params": {"value": True}})
        self.visit(CATALOGUE + "#sunday-propers-calendar")
        self.run_js(f"{ROW}.scrollIntoView({{behavior:'instant',block:'center'}})")
        before = self.catalogue_position()
        self.assertGreater(before, 1000)
        link = self.command("/element", {"using": "css selector", "value": f'a[href$="{Path(PROPER).name}"]'})
        element = link["element-6066-11e4-a52e-4f735466cecf"]
        self.command(f"/element/{element}/click")
        self.assertTrue(self.request("GET", self.session + "/url").endswith(PROPER))
        self.command("/back")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), before, delta=2)

    def test_enlarged_text_and_print(self):
        self.viewport(320, 852)
        for route in (CATALOGUE, "library/novus-ordo-liturgy.html", "index.html",
                      "library/faith.html", "library/prayer.html", "library/ecclesiastical-latin.html"):
            self.visit(route)
            self.run_js("document.documentElement.style.fontSize='200%'")
            self.assertLessEqual(self.run_js("return document.documentElement.scrollWidth"), 320)
            self.run_js("document.querySelector('.catalogue-table').scrollIntoView({behavior:'instant'})")
            self.screenshot(Path(route).stem + "-320-text-200")
            self.command("/goog/cdp/execute", {"cmd": "Emulation.setEmulatedMedia",
                "params": {"media": "print"}})
            self.assertEqual(self.run_js("return getComputedStyle(document.querySelector('.catalogue-table thead')).position"), "static")
            self.command("/goog/cdp/execute", {"cmd": "Emulation.setEmulatedMedia",
                "params": {"media": ""}})

    def test_keyboard_focus_clears_sticky_headers(self):
        report = []
        for width, scale in ((1440, 1), (393, 1), (320, 1), (320, 2)):
            self.viewport(width, 900 if width == 1440 else 852)
            self.command("/goog/cdp/execute", {"cmd": "Emulation.setScriptExecutionDisabled",
                "params": {"value": scale == 2}})
            self.visit(CATALOGUE)
            self.run_js(f"document.documentElement.style.fontSize='{scale * 100}%';const a={ROW}.querySelector('a');a.focus();a.scrollIntoView({{behavior:'instant',block:'center'}})")
            for reverse in (True, False):
                for step in range(60):
                    keys = [{"type": "keyDown", "value": "\ue004"},
                            {"type": "keyUp", "value": "\ue004"}]
                    if reverse:
                        keys = [{"type": "keyDown", "value": "\ue008"}, *keys,
                                {"type": "keyUp", "value": "\ue008"}]
                    self.command("/actions", {"actions": [{"type": "key", "id": "keyboard", "actions": keys}]})
                    metric = self.run_js("""const a=document.activeElement, table=a.closest('table');if(!table)return null;const b=a.getBoundingClientRect(),h=table.tHead.getBoundingClientRect(),s=getComputedStyle(a),ring=parseFloat(s.outlineWidth)+parseFloat(s.outlineOffset);return {top:b.top,bottom:b.bottom,headerBottom:Math.max(0,h.bottom),viewport:innerHeight,ring,visible:b.top-ring>=Math.max(0,h.bottom)-1&&b.bottom+ring<=innerHeight+1};""")
                    if metric:
                        report.append({"width": width, "textScale": scale,
                            "reverse": reverse, "step": step, **metric})
                    if reverse and step == 15:
                        self.screenshot(f"keyboard-{width}-text-{scale}")
        (self.evidence / "keyboard.json").write_text(json.dumps(report, indent=2))
        self.assertGreater(len(report), 400)
        self.assertEqual([row for row in report if not row["visible"]], [])

    def test_static_landing_tables_share_component(self):
        report = []
        for route in self.catalogues:
            self.visit(route)
            for width in (1440, 393, 320):
                self.viewport(width, 900 if width == 1440 else 852)
                metrics = self.run_js("""const tables=[...document.querySelectorAll('main table')];return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,tables:tables.map(t=>{t.scrollIntoView({behavior:'instant',block:'start'});scrollBy({top:Math.min(80,Math.max(0,(t.getBoundingClientRect().height-t.tHead.getBoundingClientRect().height)/2)),behavior:'instant'});const b=t.getBoundingClientRect(),h=t.tHead.getBoundingClientRect(),expected=Math.min(Math.max(0,b.top),b.bottom-h.height);return {component:t.classList.contains('catalogue-table'),headers:[...t.querySelectorAll('th')].every(h=>h.scope==='col'),sticky:getComputedStyle(t.tHead).position==='sticky',aligned:Math.abs(h.top-expected)<2};})};""")
                report.append({"route": route, **metrics})
                if route in ("index.html", "library/faith.html", "library/prayer.html", "library/ecclesiastical-latin.html"):
                    self.run_js("document.querySelector('table').scrollIntoView({behavior:'instant'})")
                    self.screenshot(Path(route).stem + f"-{width}")
                self.assertLessEqual(metrics["documentWidth"], width, (route, metrics))
                self.assertTrue(all(all(t.values()) for t in metrics["tables"]), (route, metrics))
            # Focus every actual table link; the real Tab traversal is covered above.
            focused = self.focused_table_links()
            self.assertEqual([row for row in focused if not row["visible"]], [], (route, focused))
        (self.evidence / "static-landings.json").write_text(json.dumps(report, indent=2))

    def test_static_landings_without_script_at_enlarged_text(self):
        self.viewport(320, 852)
        self.command("/goog/cdp/execute", {"cmd": "Emulation.setScriptExecutionDisabled",
            "params": {"value": True}})
        for route in ("index.html", "library/faith.html", "library/prayer.html", "library/ecclesiastical-latin.html"):
            self.visit(route)
            self.run_js("document.documentElement.style.fontSize='200%'")
            self.assertLessEqual(self.run_js("return document.documentElement.scrollWidth"), 320)
            focused = self.focused_table_links()
            self.assertEqual([row for row in focused if not row["visible"]], [], (route, focused))

    def test_root_and_catalogue_return_under_project_path(self):
        self.viewport(393, 852)
        self.visit("triptych/")
        self.assertEqual(self.run_js("return [...document.querySelectorAll('main table:first-of-type tbody td:first-child a')].map(a=>a.textContent.trim())"),
                         ["Faith", "Scripture", "Liturgy", "History", "Formation", "Mary", "Law"])
        self.run_js("const a=document.querySelector('table a[href$=\"law-and-church-discipline.html\"]');a.scrollIntoView({behavior:'instant',block:'center'})")
        root_y = self.catalogue_position()
        self.assertGreater(root_y, 100)
        self.run_js("document.querySelector('table a[href$=\"law-and-church-discipline.html\"]').click()")
        time.sleep(.15)
        self.run_js("document.querySelector('.site-header nav a[href$=\"index.html\"]').click()")
        time.sleep(.15)
        self.assertAlmostEqual(self.catalogue_position(), root_y, delta=2)
        self.assertTrue(self.run_js("return location.pathname").startswith("/triptych/"))

    def test_table_text_contrast(self):
        report = []
        for route in self.catalogues:
            self.visit(route)
            for width in (1440, 393, 320):
                self.viewport(width, 900 if width == 1440 else 852)
                self.run_js("scrollTo({top:0,behavior:'instant'})")
                # A full-page capture must retain the viewport's scrollbar gutter,
                # otherwise removing the scrollbar can reflow text after measurement.
                self.run_js("""if(innerWidth>document.documentElement.clientWidth){
                    const s=document.createElement('style');s.id='contrast-layout-probe';
                    s.textContent='html{scrollbar-gutter:stable!important}';document.head.append(s);
                }""")
                targets = self.run_js("""
                    const canvas=document.createElement('canvas');canvas.width=canvas.height=1;
                    const context=canvas.getContext('2d');
                    return [...document.querySelectorAll('.catalogue-table th,.catalogue-table a')].map(el=>{
                      const style=getComputedStyle(el),range=document.createRange();range.selectNodeContents(el);
                      context.clearRect(0,0,1,1);context.fillStyle=style.color;context.fillRect(0,0,1,1);
                      const foreground=[...context.getImageData(0,0,1,1).data];
                      let opacity=1;for(let p=el;p;p=p.parentElement)opacity*=Number(getComputedStyle(p).opacity);
                      foreground[3]*=opacity;
                      return {kind:el.tagName==='TH'?'header':'link',text:el.textContent.trim(),foreground,
                        rects:[...range.getClientRects()].filter(r=>r.width&&r.height).map(r=>({x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height}))};
                    }).filter(t=>t.rects.length);
                """)
                # Hide foreground paint, preserving layout and every background layer.
                # The resulting pixels resolve gradients and alpha compositing in Chromium.
                self.run_js("""const s=document.createElement('style');s.id='contrast-background-probe';
                    s.textContent='* ,*::before,*::after{color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important;border-color:transparent!important;outline:none!important}';
                    document.head.append(s);return new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done)));""")
                size = self.command("/goog/cdp/execute", {"cmd": "Page.getLayoutMetrics", "params": {}})["cssContentSize"]
                frame = self.command("/goog/cdp/execute", {"cmd": "Page.captureScreenshot", "params": {
                    "format": "png", "captureBeyondViewport": True,
                    "clip": {"x": 0, "y": 0, "width": size["width"], "height": size["height"], "scale": 1}}})
                values = self.command("/execute/async", {"script": """
                    const [encoded,targets,done]=arguments,image=new Image();
                    const linear=v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4};
                    const luminance=c=>.2126*linear(c[0])+.7152*linear(c[1])+.0722*linear(c[2]);
                    image.onerror=()=>done({error:'Could not decode Chromium background capture'});
                    image.onload=()=>{
                      const canvas=document.createElement('canvas');canvas.width=image.width;canvas.height=image.height;
                      const context=canvas.getContext('2d',{willReadFrequently:true});context.drawImage(image,0,0);
                      done(targets.map(target=>{
                        let ratio=Infinity,background=null;const alpha=target.foreground[3]/255;
                        for(const r of target.rects){
                          const x=Math.max(0,Math.floor(r.x)),y=Math.max(0,Math.floor(r.y));
                          const w=Math.min(image.width-x,Math.ceil(r.x+r.width)-x),h=Math.min(image.height-y,Math.ceil(r.y+r.height)-y);
                          if(w<=0||h<=0)continue;
                          const pixels=context.getImageData(x,y,w,h).data;
                          for(let i=0;i<pixels.length;i+=4){
                            const bg=[pixels[i],pixels[i+1],pixels[i+2]],fg=bg.map((v,c)=>target.foreground[c]*alpha+v*(1-alpha));
                            const a=luminance(bg),b=luminance(fg),contrast=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
                            if(contrast<ratio){ratio=contrast;background=bg;}
                          }
                        }
                        return {kind:target.kind,text:target.text,foreground:target.foreground,background,ratio};
                      }));
                    };
                    image.src='data:image/png;base64,'+encoded;
                """, "args": [frame["data"], targets]})
                self.run_js("document.querySelector('#contrast-background-probe').remove()")
                self.run_js("document.querySelector('#contrast-layout-probe')?.remove()")
                self.assertIsInstance(values, list, values)
                report.append({"route": route, "width": width, "targets": values})
                if route in ("index.html", "library/faith.html", "library/scripture.html") and width == 393:
                    self.run_js("document.querySelector('table').scrollIntoView({behavior:'instant'})")
                    self.screenshot("contrast-" + Path(route).stem + "-393")
        (self.evidence / "contrast.json").write_text(json.dumps(report, indent=2))
        failures = [{"route": row["route"], "width": row["width"], **target}
                    for row in report for target in row["targets"] if target["ratio"] < 4.5]
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
