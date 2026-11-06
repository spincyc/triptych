"""Real-browser regressions for print links that generate the PDF in place.

A plain click on a `print/…/*.html?print=1` link stays on the page: the
controller reads the edition's selection from the print page, typesets it
under a small progress popover beside the link and offers the PDF there.
Print-page controls themselves are covered by `test_native_print_frontend`.
"""
from __future__ import annotations

import json
import posixpath
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print as native
from ._cdp_drive import drive, act, wait

READER = "web/gpt/liturgy/example.html"
PRINT = "print/gpt/example.html"
OTHER = "print/gpt/other.html"
EXAMPLE = "publication:gpt/example"
SECOND = "publication:gpt/other"
INVALID = "publication:gpt/invalid"
BUNDLES = {EXAMPLE: "c", SECOND: "e", INVALID: "f"}
TITLES = {EXAMPLE: "Canonical edition", SECOND: "Other edition", INVALID: "Invalid edition"}


def rows():
    return {identity: {"id": identity, "output_id": identity, "document": identity, "edition": "main",
                       "title": TITLES[identity]} for identity in BUNDLES}


def context():
    return {"documents": rows(), "source_revision": "a" * 40, "endpoint": "", "archives": {},
            "native_catalog": {"selections": {identity: {
                "bundle_href": "native-tex/sources/" + digit * 64 + ".json",
                "bundle_sha256": digit * 64, "bundle_bytes": 123} for identity, digit in BUNDLES.items()},
                "runtime": {"href": "native-tex/runtime.json", "sha256": "d" * 64, "bytes": 456}}}


def filename(identity):
    return native.download_name(identity, rows()[identity])


def print_page(identity, route, *, corrupt=False):
    """A print page as the site builds it: controls plus the compiler scripts."""
    head, tail = native.extras(route, wasm=True)
    controls = native.controls(identity, route, context())
    if corrupt:
        good = '"source_revision":"' + "a" * 40 + '"'
        assert good in controls
        controls = controls.replace(good, '"source_revision":"not-a-revision"')
    return ('<!doctype html><html><head><meta charset="utf-8">' + head + '</head><body><h1>'
            + TITLES[identity] + '</h1>' + controls + tail + '</body></html>')


# A stand-in for `shared/native-tex.js`: the real compiler's `generate()`
# contract, with progress events shaped like its `downloadProgress()` and
# stage messages, held until the test releases or fails it.
STUB = r"""(()=>{
  window.texLoads=(window.texLoads||[]).concat(MARKER);window.calls=window.calls||[];
  const keep=' Keep this page visible until it finishes.';
  const mib=value=>value.toFixed(1);
  window.TriptychNativeTeX={generate:(options)=>new Promise((resolve,reject)=>{
    const call={bundleURL:options.bundleURL,runtimeURL:options.runtimeURL,bundleSHA256:options.bundleSHA256,
      runtimeSHA256:options.runtimeSHA256,bundleBytes:options.bundleBytes,runtimeBytes:options.runtimeBytes,
      signal:options.signal instanceof AbortSignal,abortedAtStart:options.signal.aborted,aborted:false,via:MARKER};
    calls.push(call);
    options.signal.addEventListener('abort',()=>{call.aborted=true;reject(new DOMException('Cancelled','AbortError'));},{once:true});
    Object.defineProperties(call,{
      bytes:{value:(stage,loaded,total)=>options.onProgress({stage,loadedBytes:loaded*1048576,totalBytes:total*1048576,
        message:stage+' ('+mib(loaded)+' of '+mib(total)+' MiB)…'+keep})},
      say:{value:(message)=>options.onProgress({message:message+keep})},
      ready:{value:()=>options.onProgress({stage:'ready',message:'The typeset PDF is ready.'})},
      release:{value:async()=>{const bytes=new TextEncoder().encode('%PDF-1.4\nin-place fixture\n%%EOF');
        const hash=await crypto.subtle.digest('SHA-256',bytes);
        resolve({bytes,byteLength:bytes.byteLength,
          sha256:Array.from(new Uint8Array(hash),n=>n.toString(16).padStart(2,'0')).join('')});}},
      fail:{value:()=>reject(new Error('Native TeX compilation failed.'))}});
  })};
})();"""


def stub(marker):
    return STUB.replace("MARKER", json.dumps(marker))


# Observation hooks on the reader page. Automatic downloads are counted and
# suppressed; any link click is recorded with whether its default was
# prevented by the time it reached the window, and `holdNavigation` keeps
# the page in place for clicks the controller must leave alone.
HOOK = r"""
  window.marker=1;window.calls=window.calls||[];window.downloads=[];window.fetches=[];window.clicks=[];
  window.valuenows=[];window.holdNavigation=false;
  const realFetch=window.fetch.bind(window);
  window.fetch=(input,init)=>{fetches.push(String(input instanceof Request?input.url:input));return realFetch(input,init);};
  document.addEventListener('click',event=>{
    const action=event.target instanceof Element&&event.target.closest('.native-print-popover__action[download]');
    if(action){event.preventDefault();downloads.push({href:action.getAttribute('href'),download:action.getAttribute('download')});}
  },true);
  window.addEventListener('click',event=>{
    const link=event.target instanceof Element&&event.target.closest('a[href]');
    if(!link||link.closest('[data-native-print-popover]'))return;
    clicks.push({id:link.id||link.parentElement.className,prevented:event.defaultPrevented});
    if(holdNavigation)event.preventDefault();
  });
  new MutationObserver(records=>{for(const record of records)if(record.target.matches('.native-print-popover__bar'))
    valuenows.push({old:record.oldValue,now:record.target.getAttribute('aria-valuenow')});})
    .observe(document.body,{subtree:true,attributes:true,attributeOldValue:true,attributeFilter:['aria-valuenow']});
  const box=node=>{if(!node)return null;const r=node.getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height};};
  window.snap=(selector)=>{
    const root=document.querySelector('[data-native-print-popover]'),q=s=>root&&root.querySelector(s);
    const action=q('.native-print-popover__action'),bar=q('.native-print-popover__bar'),link=selector&&document.querySelector(selector);
    return {count:document.querySelectorAll('[data-native-print-popover]').length,
      parentIsBody:root?root.parentElement===document.body:null,
      open:root?root.matches(':popover-open')||(!root.hasAttribute('popover')&&!root.hidden):false,
      state:root?root.dataset.state:null,progress:root?root.dataset.progress:null,
      status:root?q('.native-print-popover__status').textContent:null,
      statusRole:root?q('.native-print-popover__status').getAttribute('role'):null,
      amount:root?q('.native-print-popover__amount').textContent:null,
      barRole:bar?bar.getAttribute('role'):null,valuenow:bar?bar.getAttribute('aria-valuenow'):null,
      closeLabel:root?q('.native-print-popover__close').getAttribute('aria-label'):null,
      actionHidden:action?action.hidden:null,actionText:action?action.textContent:null,
      actionHref:action?action.getAttribute('href'):null,actionURL:action&&action.hasAttribute('href')?action.href:null,
      actionDownload:action?action.getAttribute('download'):null,
      linkURL:link?link.href:null,popoverBox:box(root),linkBox:box(link),
      viewport:{width:document.documentElement.clientWidth,height:document.documentElement.clientHeight},
      calls:calls.map(call=>({...call})),downloads:downloads.slice(),fetches:fetches.slice(),clicks:clicks.slice(),
      texLoads:window.texLoads||[],
      texScripts:[...document.querySelectorAll('script[src]')].map(s=>s.src).filter(s=>s.includes('native-tex')),
      origin:location.origin,location:location.pathname+location.search+location.hash,marker:window.marker===1,
      focus:document.activeElement&&(document.activeElement.id||document.activeElement.className)};
  };
"""


def rel(target):
    return posixpath.relpath(target, posixpath.dirname(READER))


def reader_page(*, preset=False):
    """A reader page with the real Print action, more print links and decoys."""
    gap = 'style="margin-top:110px"'
    links = [
        '<p ' + gap + '><a id="other" href="' + rel(OTHER) + '?print=1#contents">Generate PDF</a></p>',
        '<p ' + gap + '><a id="missing" href="' + rel("print/gpt/missing.html") + '?print=1">Generate PDF</a></p>',
        '<p ' + gap + '><a id="invalid" href="' + rel("print/gpt/invalid.html") + '?print=1">Generate PDF</a></p>',
        '<p ' + gap + '><a id="bare" href="' + rel("print/gpt/bare.html") + '?print=1">Generate PDF</a></p>',
        '<p ' + gap + '><button id="elsewhere" type="button">Elsewhere</button></p>',
        '<p ' + gap + '><a id="noquery" href="' + rel(PRINT) + '">Print page</a> '
        '<a id="print10" href="' + rel(PRINT) + '?print=10">Ten</a> '
        '<a id="notprint" href="' + rel("web/gpt/other.html") + '?print=1">Not print</a> '
        '<a id="blank" target="_blank" href="' + rel(PRINT) + '?print=1">New tab</a> '
        '<a id="download" download href="' + rel(PRINT) + '?print=1">Download</a> '
        '<a id="cross" href="https://example.org/print/gpt/example.html?print=1">Elsewhere</a></p>',
        '<div style="height:2400px"></div><p><a id="low" href="' + rel(PRINT) + '?print=1">Generate PDF</a></p>'
        '<div style="height:400px"></div>',
    ]
    content = ('<article><h1>Example</h1>' + native.reader_action(READER, PRINT)
               + '<p>Reading text.</p>' + "".join(links) + '</article>')
    head, tail = native.link_extras(READER, content)
    assert head and tail, "the reader page must load the link controller"
    hook = HOOK + (stub("inline") if preset else "")
    page = ('<!doctype html><html><head><meta charset="utf-8">' + head + '</head>'
            '<body style="margin:0;padding:24px;font:16px/1.5 Georgia,serif">'
            + content + '<script>' + hook + '</script>' + tail + '</body></html>')
    return {
        READER: page,
        PRINT: print_page(EXAMPLE, PRINT),
        OTHER: print_page(SECOND, OTHER),
        "print/gpt/invalid.html": print_page(INVALID, "print/gpt/invalid.html", corrupt=True),
        "print/gpt/bare.html": '<!doctype html><html><body><h1>No controls</h1></body></html>',
        "shared/native-print.js": (ROOT / "src/web/browser/shared/native-print.js").read_text(),
        "shared/native-print.css": (ROOT / "src/web/browser/shared/native-print.css").read_text(),
        "shared/native-tex.js": stub("file"),
    }


ACTION = ".print-actions a"
LOADED = wait("document.readyState==='complete' && window.TriptychNativePrint && window.snap")
ESCAPE = {"do": "key", "key": "Escape", "code": "Escape"}


def opened():
    return [{"do": "navigate", "url": "/" + READER}, LOADED]


def snap(name, selector=ACTION):
    return act("snap(" + json.dumps(selector) + ")", name)


def bundle(origin, identity):
    return origin + "/native-tex/sources/" + BUNDLES[identity] * 64 + ".json"


class InPlaceGenerationTests(unittest.TestCase):
    def assertInViewport(self, seen):
        box, view = seen["popoverBox"], seen["viewport"]
        self.assertGreater(box["width"], 0, seen)
        self.assertGreaterEqual(box["top"], 0, seen)
        self.assertGreaterEqual(box["left"], 0, seen)
        self.assertLessEqual(box["bottom"], view["height"], seen)
        self.assertLessEqual(box["right"], view["width"], seen)

    def test_plain_click_stays_on_page_and_saves_the_print_page_edition(self):
        steps = ("calls[0].bytes('Checking the original sources and print runtime',0,60)",
                 "calls[0].bytes('Checking the original sources and print runtime',30,60)",
                 "calls[0].bytes('Checking the original sources and print runtime',60,60)",
                 "calls[0].bytes('Downloading original fonts and packages',5,10)",
                 "calls[0].bytes('Downloading the typesetter',10,20)",
                 "calls[0].say('Starting the typesetter…')",
                 "calls[0].say('Typesetting with the original TeX layout (pass 1)…')",
                 "calls[0].say('Typesetting with the original TeX layout (pass 2)…')",
                 # A rerun that fetches more fonts must not move the bar back.
                 "calls[0].bytes('Downloading original fonts and packages',1,4)",
                 "calls[0].say('Loading the original fonts selected by this document…')",
                 "calls[0].say('Typesetting with the original TeX layout (pass 3)…')",
                 "calls[0].say('Embedding the original fonts in the typeset PDF…')",
                 "calls[0].ready()")
        progress = "[" + ",".join("(" + step + ",snap())" for step in steps) + "]"
        seen = drive({"responses": reader_page(), "acts": [
            *opened(), snap("idle"),
            {"do": "click", "selector": ACTION}, wait("calls.length===1"), snap("preparing"),
            act(progress, "progress"),
            act("calls[0].release()"), wait("snap().state==='ready'"), snap("ready"),
            act("fetch(document.querySelector('.native-print-popover__action').href).then(r=>r.text())", "blob"),
            {"do": "sleep", "ms": 300}, snap("settled"),
            {"do": "click", "selector": ".native-print-popover__close"}, snap("closed"),
            act("valuenows", "valuenows"),
        ]})
        self.assertEqual((seen["idle"]["count"], seen["idle"]["calls"], seen["idle"]["fetches"]), (0, [], []), seen["idle"])
        self.assertEqual(seen["idle"]["texScripts"], [], "the compiler loads only on first use")

        preparing = seen["preparing"]
        origin = preparing["origin"]
        # 1. No navigation: same document, same address, click default prevented.
        self.assertTrue(preparing["marker"], preparing)
        self.assertEqual(preparing["location"], "/" + READER)
        self.assertEqual(preparing["clicks"], [{"id": "print-actions", "prevented": True}])
        # 2. The selection comes from the print page; resources resolve against it.
        self.assertEqual(preparing["fetches"], [origin + "/" + PRINT])
        call = preparing["calls"][0]
        self.assertEqual(call["bundleURL"], bundle(origin, EXAMPLE), call)
        self.assertEqual(call["runtimeURL"], origin + "/native-tex/runtime.json", call)
        self.assertEqual((call["bundleSHA256"], call["runtimeSHA256"], call["bundleBytes"], call["runtimeBytes"]),
                         ("c" * 64, "d" * 64, 123, 456))
        self.assertTrue(call["signal"])
        self.assertFalse(call["abortedAtStart"])
        # 3. The compiler script came from beside native-print.js, once.
        self.assertEqual(preparing["texScripts"], [origin + "/shared/native-tex.js"])
        self.assertEqual(preparing["texLoads"], ["file"])
        self.assertEqual(call["via"], "file")
        # 4. One popover on <body>, running, cancellable, bar not yet measured.
        self.assertEqual((preparing["count"], preparing["parentIsBody"], preparing["open"]), (1, True, True), preparing)
        self.assertEqual((preparing["state"], preparing["progress"], preparing["valuenow"]),
                         ("preparing", "indeterminate", None), preparing)
        self.assertEqual((preparing["statusRole"], preparing["barRole"]), ("status", "progressbar"))
        self.assertEqual(preparing["closeLabel"], "Cancel PDF generation")
        self.assertTrue(preparing["actionHidden"])
        # 9. Within the viewport, below the link.
        self.assertInViewport(preparing)
        self.assertGreaterEqual(preparing["popoverBox"]["top"], preparing["linkBox"]["bottom"], preparing)

        steps = seen["progress"]
        labels = [step["status"] for step in steps]
        self.assertEqual(labels[:8], ["Checking sources"] * 3 + ["Downloading fonts", "Downloading typesetter",
                                      "Starting typesetter", "Typesetting · pass 1", "Typesetting · pass 2"], labels)
        self.assertEqual(labels[10], "Typesetting · pass 3", labels)
        self.assertEqual(labels[11], "Embedding fonts", labels)
        self.assertFalse(any("Keep this page visible" in label for label in labels), labels)
        self.assertEqual([step["amount"] for step in steps[:5]],
                         ["0.0 of 60.0 MiB", "30.0 of 60.0 MiB", "60.0 of 60.0 MiB", "5.0 of 10.0 MiB", "10.0 of 20.0 MiB"])
        self.assertEqual(steps[6]["amount"], "")
        self.assertEqual(steps[0]["progress"], "determinate")
        values = [int(step["valuenow"]) for step in steps]
        self.assertEqual(values, sorted(values), values)
        self.assertLess(values[0], values[-1], values)
        self.assertTrue(all(step["state"] == "preparing" for step in steps), steps)
        self.assertTrue(all(step["downloads"] == [] for step in steps))

        ready = seen["ready"]
        self.assertEqual((ready["state"], ready["progress"], ready["valuenow"], ready["status"], ready["amount"]),
                         ("ready", "determinate", "100", "PDF ready", ""), ready)
        self.assertEqual((ready["actionHidden"], ready["actionText"], ready["actionDownload"], ready["closeLabel"]),
                         (False, "Save PDF", filename(EXAMPLE), "Close"), ready)
        self.assertTrue(ready["actionHref"].startswith("blob:"), ready)
        self.assertEqual(ready["downloads"], [{"href": ready["actionHref"], "download": filename(EXAMPLE)}])
        self.assertTrue(seen["blob"].startswith("%PDF-"))
        self.assertEqual(seen["settled"]["downloads"], ready["downloads"], "the PDF is offered automatically once")
        self.assertEqual((ready["marker"], ready["location"], ready["count"]), (True, "/" + READER, 1))
        self.assertInViewport(ready)
        # Every value the bar ever showed in this run, in order.
        shown = [int(row["now"]) for row in seen["valuenows"] if row["now"] is not None]
        self.assertEqual(shown, sorted(shown), seen["valuenows"])
        self.assertEqual(shown[-1], 100)

        closed = seen["closed"]
        self.assertEqual((closed["state"], closed["open"], closed["count"]), ("closed", False, 1), closed)
        self.assertEqual(closed["downloads"], ready["downloads"])

    def test_loaded_compiler_is_reused_and_a_new_link_supersedes_a_running_one(self):
        dynamic = ("(()=>{const link=document.createElement('a');link.id='dynamic';link.textContent='Print complete edition';"
                   "link.href=" + json.dumps(rel(OTHER) + "?print=1") + ";const p=document.createElement('p');"
                   "p.style.marginTop='110px';p.append(link);document.querySelector('#elsewhere').parentElement.after(p);})()")
        seen = drive({"responses": reader_page(preset=True), "acts": [
            *opened(),
            {"do": "click", "selector": ACTION}, wait("calls.length===1"),
            {"do": "click", "selector": ACTION}, {"do": "sleep", "ms": 400}, snap("again"),
            {"do": "click", "selector": "#other"}, wait("calls.length===2"), snap("switched", "#other"),
            act("calls[1].release()"), wait("snap().state==='ready'"), snap("ready", "#other"),
            act(dynamic), {"do": "click", "selector": "#dynamic"}, wait("calls.length===3"),
            act("calls[2].release()"), wait("snap().state==='ready' && downloads.length===2"), snap("dynamic", "#dynamic"),
        ]})
        again = seen["again"]
        origin = again["origin"]
        # 3. A compiler already on the page is used; no script is injected.
        self.assertEqual(again["texLoads"], ["inline"], again)
        self.assertEqual(again["texScripts"], [], again)
        # 8. The same link again while running starts nothing new.
        self.assertEqual((len(again["calls"]), again["calls"][0]["aborted"], again["state"]), (1, False, "preparing"), again)
        self.assertEqual(again["fetches"], [origin + "/" + PRINT], again)
        switched = seen["switched"]
        # 8. A different link aborts the running build and starts its own;
        # 2. its query and fragment are not part of the print page request.
        self.assertTrue(switched["calls"][0]["aborted"], switched)
        self.assertFalse(switched["calls"][1]["aborted"], switched)
        self.assertEqual(switched["calls"][1]["bundleURL"], bundle(origin, SECOND))
        self.assertEqual(switched["fetches"], [origin + "/" + PRINT, origin + "/" + OTHER], switched)
        self.assertEqual((switched["state"], switched["count"], switched["location"]), ("preparing", 1, "/" + READER))
        self.assertGreaterEqual(switched["popoverBox"]["top"], switched["linkBox"]["bottom"], switched)
        ready = seen["ready"]
        self.assertEqual(ready["downloads"], [{"href": ready["actionHref"], "download": filename(SECOND)}], ready)
        self.assertEqual(ready["texLoads"], ["inline"])
        # A link added after load (as the Sources page does) is handled too.
        late = seen["dynamic"]
        self.assertEqual(late["calls"][2]["bundleURL"], bundle(origin, SECOND))
        self.assertEqual(len(late["downloads"]), 2, late)
        self.assertEqual((late["count"], late["marker"], late["location"]), (1, True, "/" + READER), late)
        self.assertEqual(late["texScripts"], [])

    def test_escape_and_cancel_stop_a_running_build(self):
        seen = drive({"responses": reader_page(), "acts": [
            *opened(),
            {"do": "click", "selector": ACTION}, wait("calls.length===1"),
            act("document.querySelector('#elsewhere').focus()"), ESCAPE, {"do": "sleep", "ms": 100}, snap("unfocused"),
            act("document.querySelector(" + json.dumps(ACTION) + ").focus()"), ESCAPE, snap("fromLink"),
            {"do": "click", "selector": ACTION}, wait("calls.length===2"),
            act("document.querySelector('.native-print-popover__close').focus()"), ESCAPE, snap("fromPopover"),
            {"do": "click", "selector": ACTION}, wait("calls.length===3"), snap("running"),
            {"do": "click", "selector": ".native-print-popover__close"}, snap("cancelled"),
        ]})
        unfocused = seen["unfocused"]
        self.assertEqual((unfocused["state"], unfocused["calls"][0]["aborted"]), ("preparing", False), unfocused)
        for name, index in (("fromLink", 0), ("fromPopover", 1)):
            with self.subTest(name):
                observed = seen[name]
                self.assertTrue(observed["calls"][index]["aborted"], observed)
                self.assertEqual((observed["state"], observed["open"]), ("closed", False), observed)
        running = seen["running"]
        self.assertEqual(running["closeLabel"], "Cancel PDF generation")
        cancelled = seen["cancelled"]
        self.assertTrue(cancelled["calls"][2]["aborted"], cancelled)
        self.assertEqual((cancelled["state"], cancelled["open"], cancelled["count"]), ("closed", False, 1), cancelled)
        self.assertEqual(cancelled["downloads"], [])
        self.assertEqual((cancelled["marker"], cancelled["location"]), (True, "/" + READER))

    def test_leaving_the_page_aborts_a_running_build(self):
        hide = "dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}))"
        seen = drive({"responses": reader_page(), "acts": [
            *opened(), {"do": "click", "selector": ACTION}, wait("calls.length===1"), snap("running"),
            act(hide), snap("left"), act("calls[0].release()"), {"do": "sleep", "ms": 200}, snap("late"),
        ]})
        self.assertEqual(seen["running"]["state"], "preparing")
        left = seen["left"]
        self.assertTrue(left["calls"][0]["aborted"], left)
        self.assertEqual((left["state"], left["open"]), ("closed", False), left)
        self.assertEqual((seen["late"]["state"], seen["late"]["downloads"]), ("closed", []), seen["late"])

    def test_modified_new_tab_download_and_foreign_clicks_keep_the_browser_default(self):
        probe = """(()=>{holdNavigation=true;const out=[];
          const click=(selector,init)=>{clicks.length=0;const link=document.querySelector(selector);
            const event=new MouseEvent('click',{bubbles:true,cancelable:true,view:window,...init});
            link.dispatchEvent(event);out.push({selector,init,seen:clicks.slice()});};
          for(const init of [{ctrlKey:true},{metaKey:true},{shiftKey:true},{altKey:true},{button:1}])click(ACTION,init);
          for(const id of ['#blank','#download','#noquery','#print10','#notprint','#cross'])click(id,{});
          return out;})()""".replace("ACTION", json.dumps(ACTION))
        seen = drive({"responses": reader_page(), "acts": [
            *opened(), act(probe, "ignored"), {"do": "sleep", "ms": 300}, snap("after"),
            act("(()=>{const event=new MouseEvent('click',{bubbles:true,cancelable:true,view:window});"
                "document.querySelector(" + json.dumps(ACTION) + ").dispatchEvent(event);return event.defaultPrevented;})()",
                "control"),
        ]})
        self.assertEqual(len(seen["ignored"]), 11)
        for row in seen["ignored"]:
            with self.subTest(selector=row["selector"], init=row["init"]):
                # Seen at the window, after every page listener; the probe
                # itself then holds navigation so the page stays put.
                self.assertEqual([click["prevented"] for click in row["seen"]], [False], row)
        after = seen["after"]
        self.assertEqual((after["count"], after["calls"], after["fetches"], after["texScripts"]), (0, [], [], []), after)
        self.assertTrue(after["marker"])
        # The same dispatch without a modifier is intercepted: the probe can see it.
        self.assertTrue(seen["control"])

    def test_failures_offer_the_print_page_instead_of_a_pdf(self):
        error = lambda count: wait("snap().state==='error' && fetches.length===" + str(count))
        seen = drive({"responses": reader_page(), "acts": [
            *opened(),
            {"do": "click", "selector": "#missing"}, error(1), snap("missing", "#missing"),
            {"do": "click", "selector": "#invalid"}, error(2), snap("invalid", "#invalid"),
            {"do": "click", "selector": "#bare"}, error(3), snap("bare", "#bare"),
            {"do": "click", "selector": ACTION}, wait("calls.length===1"),
            act("calls[0].bytes('Downloading the typesetter',4,20)"), act("calls[0].fail()"),
            error(4), snap("rejected"),
        ]})
        for name, detail in (("missing", "could not be loaded"), ("invalid", "selection is incomplete"),
                             ("bare", "no PDF selection"), ("rejected", "compilation failed")):
            with self.subTest(name):
                observed = seen[name]
                self.assertEqual((observed["state"], observed["count"], observed["open"]), ("error", 1, True), observed)
                self.assertTrue(observed["status"].startswith("PDF unavailable: "), observed)
                self.assertIn(detail, observed["status"])
                self.assertEqual((observed["actionHidden"], observed["actionText"], observed["actionDownload"]),
                                 (False, "Open print page", None), observed)
                self.assertEqual(observed["actionURL"], observed["linkURL"], observed)
                self.assertEqual(observed["closeLabel"], "Close")
                self.assertEqual(observed["amount"], "")
                self.assertEqual(observed["downloads"], [])
                self.assertEqual((observed["marker"], observed["location"]), (True, "/" + READER))
                self.assertInViewport(observed)
        self.assertEqual(seen["bare"]["texScripts"], [], "no compiler loads for an edition that has no selection")

    def test_open_print_page_action_opens_the_print_page(self):
        here = "({location:location.pathname+location.search,marker:window.marker===1,builds:window.calls?calls.length:null})"
        seen = drive({"responses": reader_page(), "acts": [
            *opened(), {"do": "click", "selector": ACTION}, wait("calls.length===1"),
            act("calls[0].fail()"), wait("snap().state==='error'"), snap("error"),
            {"do": "click", "selector": ".native-print-popover__action"}, {"do": "sleep", "ms": 1500}, act(here, "after"),
        ]})
        self.assertEqual(seen["error"]["actionText"], "Open print page")
        after = seen["after"]
        self.assertEqual(after["location"], "/" + PRINT + "?print=1", after)
        self.assertFalse(after["marker"], after)

    def test_popover_stays_within_the_viewport_beside_a_link_at_its_edge(self):
        edge = ("(()=>{const r=document.querySelector('#low').getBoundingClientRect();"
                "scrollBy(0,r.bottom-(document.documentElement.clientHeight-10));})()")
        seen = drive({"responses": reader_page(), "acts": [
            *opened(), act(edge), {"do": "sleep", "ms": 100},
            {"do": "click", "selector": "#low"}, wait("calls.length===1"), {"do": "sleep", "ms": 100}, snap("edge", "#low"),
        ]})
        observed = seen["edge"]
        self.assertEqual(observed["state"], "preparing", observed)
        self.assertGreater(observed["linkBox"]["bottom"], observed["viewport"]["height"] - 20, observed)
        self.assertInViewport(observed)
        # No room below, so it sits above rather than over the link.
        self.assertLessEqual(observed["popoverBox"]["bottom"], observed["linkBox"]["top"], observed)


if __name__ == "__main__":
    unittest.main()
