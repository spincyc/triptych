"""Native-PDF admission and real-browser request/absence/error regressions."""
from __future__ import annotations

from collections import Counter
import copy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print as native
from ._cdp_drive import drive, act, wait, idle_arrivals


class NativeAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = native.admitted_documents(ROOT)

    def test_exact_public_universe_excludes_holds_and_unadvertised_papal_sources(self):
        self.assertEqual(Counter(identity.partition(":")[0] for identity in self.documents),
                         {"publication": 281, "bible": 7, "papal": 350, "reading-plan": 6})
        self.assertNotIn("bible:knox", self.documents)
        selected = {(row["document"], row["edition"]) for row in self.documents.values()}
        self.assertEqual(len(selected), 644)
        release = json.loads((ROOT / "release/papal-documents.json").read_bytes())
        self.assertGreater(len(release["documents"]), 350)
        for path in (ROOT / "release/publications").glob("**/*.json"):
            record = json.loads(path.read_bytes())
            if record["status"] == "hold":
                # A release record's id is derived from its path, not stored.
                relative = path.relative_to(ROOT / "release/publications")
                provider, leaf = relative.parts[0], relative.relative_to(relative.parts[0]).with_suffix("").as_posix()
                self.assertNotIn("publication:" + provider + "/" + leaf, self.documents)

    def test_companion_request_uses_canonical_owner_and_exact_edition(self):
        row = self.documents["publication:gpt/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis"]
        self.assertEqual(row["edition"], "synthesis")
        self.assertEqual(row["document"] + "-synthesis", row["id"])

    def test_endpoint_has_no_implicit_host_or_credential(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(native.service_endpoint(ROOT), "")
        for value in ("https://user:secret@example.org", "http://example.org", "https://example.org/v1",
                      "https://example.org/?token=private", "https://example.org/#fragment", "https://example.org/../other"):
            with self.subTest(value=value), patch.dict(os.environ, {"TRIPTYCH_NATIVE_PRINT_ENDPOINT": value}):
                with self.assertRaises(native.NativePrintError):
                    native.service_endpoint(ROOT)
        with patch.dict(os.environ, {"TRIPTYCH_NATIVE_PRINT_ENDPOINT": "https://example.org/print/"}):
            self.assertEqual(native.service_endpoint(ROOT), "https://example.org/print")

    def test_controls_disclose_historical_tex_pdf_without_substituting_it(self):
        identity = next(key for key in self.documents if key.startswith("publication:") and
                        key in native._archives(ROOT))
        context = native.site_context(ROOT, documents=self.documents, revision="a" * 40, endpoint="")
        controls = native.controls(identity, "print/example.html", context)
        self.assertIn("Download earlier TeX PDF", controls)
        self.assertIn("may precede the current text", controls)
        self.assertIn('"endpoint":""', controls)
        self.assertNotIn("window.print", controls)
        with self.assertRaises(native.NativePrintError):
            native.controls("publication:gpt/held", "print/held.html", context)

    def test_download_names_are_unique_portable_and_carry_the_identity(self):
        names = {identity: native.download_name(identity, row) for identity, row in self.documents.items()}
        repeated = {name: count for name, count in Counter(names.values()).items() if count > 1}
        self.assertEqual(repeated, {})
        self.assertEqual(len(set(names.values())), len(self.documents))
        for identity, name in names.items():
            self.assertRegex(name, r"\A[a-z0-9][a-z0-9-]*\.pdf\Z", identity)
            self.assertLessEqual(len(name), 195, identity)
            if identity.startswith("papal:"):
                self.assertTrue(name.endswith("-" + identity.rpartition("/")[2] + ".pdf"), name)
            if identity.startswith("publication:"):
                self.assertTrue(name.endswith("-" + identity.split(":")[1].split("/")[0] + ".pdf"), name)
        prefix = "publication:{}/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis"
        self.assertEqual(names[prefix.format("claude")], "1962-f02-all-saints-synthesis-claude.pdf")
        self.assertEqual(names[prefix.format("gpt")], "1962-f02-all-saints-synthesis-gpt.pdf")
        self.assertEqual(names["publication:gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive"],
                         "1962-roman-sanctuary-dictionary-comprehensive-gpt.pdf")
        self.assertEqual(names["papal:papal.leo-xiii.hf-l-xiii-enc-15051891-rerum-novarum/en"], "1891-05-15-rerum-novarum-en.pdf")
        self.assertEqual(names["bible:douay-rheims"], "douay-rheims-bible.pdf")
        context = native.site_context(ROOT, documents=self.documents, revision="a" * 40, endpoint="")
        identity = "papal:papal.leo-xiii.hf-l-xiii-enc-15051891-rerum-novarum/la"
        self.assertIn('"filename":"1891-05-15-rerum-novarum-la.pdf"', native.controls(identity, "papal/x.html", context))

    def test_compiler_bundles_bind_every_admitted_output_and_project_relative_routes(self):
        identity = next(iter(self.documents))
        catalog = {"selections": {key: {"bundle_href": "native-tex/sources/" + "c" * 64 + ".json",
                    "bundle_sha256": "c" * 64, "bundle_bytes": 123} for key in self.documents},
                   "runtime": {"href": "native-tex/runtime.json", "sha256": "d" * 64, "bytes": 456}}
        context = native.site_context(ROOT, documents=self.documents, revision="a" * 40, native_catalog=catalog)
        html = native.controls(identity, "print/gpt/long/path/example.html", context)
        self.assertIn('"bundle":"../../../../native-tex/sources/', html)
        self.assertIn('"runtime_sha256":"' + "d" * 64, html)
        self.assertIn("shared/native-tex.js", native.extras("print/example.html", wasm=True)[1])
        del catalog["selections"][identity]
        with self.assertRaises(native.NativePrintError):
            native.site_context(ROOT, documents=self.documents, revision="a" * 40, native_catalog=catalog)


def fixture(*, empty=False, failure=None, companion=False, wasm=False, service_prefix=False, auto_option=False):
    identity = "publication:gpt/example" + ("-synthesis" if companion else "")
    chosen = {"id": identity, "output_id": identity, "document": "publication:gpt/example",
              "edition": "synthesis" if companion else "main", "title": "Canonical edition"}
    context = {"documents": {identity: chosen}, "source_revision": "a" * 40,
               "endpoint": "" if empty else "http://localhost:9999", "archives": {}}
    if service_prefix:
        context["endpoint"] += "/typesetting"
    if wasm:
        context["native_catalog"] = {"selections": {identity: {
            "bundle_href": "native-tex/sources/" + "c" * 64 + ".json", "bundle_sha256": "c" * 64, "bundle_bytes": 123}},
            "runtime": {"href": "native-tex/runtime.json", "sha256": "d" * 64, "bytes": 456}}
    body = native.controls(identity, "print/example.html", context)
    body = '<section>' + body + '</section>'
    hook = """
      window.printCalls=0; window.print=()=>{window.printCalls++;throw Error('Browser print must not run');};
      window.pdfDownloads=0; document.querySelector('[data-native-print-download]').click=()=>{window.pdfDownloads++;};
      window.requests=[];window.compilerRequests=[];window.polls=0;
      const chosen=JSON.parse(document.querySelector('[data-native-print-manifest]').textContent);
      const row={key:'b'.repeat(64),source_revision:chosen.source_revision,document:chosen.document,edition:chosen.edition,
        output_id:chosen.id,state:'queued',status_url:'/v1/jobs/'+'b'.repeat(64),pdf_url:null,error:null};
      window.fetch=async(url,options)=>{
        window.requests.push({url,method:options.method||'GET',credentials:options.credentials,body:options.body||null});
        FAILURE
        if(options.method!=='POST')row.state=++window.polls>=2?'ready':'building';
        if(row.state==='ready')row.pdf_url=row.status_url+'/pdf';
        return new Response(JSON.stringify(row),{status:200,headers:{'Content-Type':'application/json'}});
      };
    """
    changes = {
        "stale": "return new Response('{}',{status:409,headers:{'Content-Type':'application/json'}});",
        "different": "row.document='publication:gpt/other';",
        "host": "row.status_url='https://attacker.example/v1/jobs/'+row.key;",
        "failed": "row.state='failed';row.error='Native TeX compilation failed.';",
        "partial": "row.pdf_url=row.status_url+'/pdf';",
        "pending": "await new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('Cancelled','AbortError')),{once:true}));",
    }
    hook = hook.replace("FAILURE", changes.get(failure, ""))
    if wasm:
        hook += """
          window.TriptychNativeTeX={generate:async(options)=>{
            window.compilerRequests.push({bundleURL:options.bundleURL,runtimeURL:options.runtimeURL,
              bundleSHA256:options.bundleSHA256,bundleBytes:options.bundleBytes,
              runtimeSHA256:options.runtimeSHA256,runtimeBytes:options.runtimeBytes});
            options.onProgress({message:'Typesetting the original source…'});
            const bytes=new TextEncoder().encode('%PDF-1.4\\nSynthetic protocol fixture.\\n%%EOF');
            const hash=await crypto.subtle.digest('SHA-256',bytes);
            let sha256=Array.from(new Uint8Array(hash),n=>n.toString(16).padStart(2,'0')).join('');
            BAD_SHA
            return {bytes,sha256,byteLength:bytes.byteLength,passes:2,log:''};
          }};
        """.replace("BAD_SHA", "sha256='e'.repeat(64);" if failure == "wasm-sha" else "")
    body += '<script>' + hook + '</script>'
    body += '<script src="../shared/native-print.js"></script>'
    if auto_option:
        body += "<script>const root=document.querySelector('[data-native-print]');TriptychNativePrint.install(root,JSON.parse(root.querySelector('[data-native-print-manifest]').textContent),{auto:true});</script>"
    responses = {"print/example.html": '<!doctype html><html><body>' + body + '</body></html>',
                 "shared/native-print.js": (ROOT / "src/web/browser/shared/native-print.js").read_text()}
    return responses


def plan(responses, *, print_query=False, cancellation=False):
    actions = [{"do": "navigate", "url": "/print/example.html" + ("?print=1" if print_query else "")},
               wait("window.TriptychNativePrint && document.querySelector('[data-native-print]').dataset.nativePrintState")]
    actions.append({"do": "click", "selector": "[data-native-print-start]"})
    if cancellation:
        actions.extend([wait("requests.length===1"), act("document.querySelector('[data-native-print-cancel]').click()")])
    actions.extend([wait("!document.querySelector('[data-native-print-start]').disabled"),
                    act("({state:document.querySelector('[data-native-print]').dataset.nativePrintState,status:document.querySelector('[data-native-print-status]').textContent,download:document.querySelector('[data-native-print-download]').getAttribute('href'),hidden:document.querySelector('[data-native-print-download]').hidden,calls:printCalls,downloads:pdfDownloads,requests})", "result")])
    return {"responses": responses, "acts": actions}


class NativeBrowserTests(unittest.TestCase):
    def test_navigation_query_reload_and_background_never_request_a_pdf(self):
        for wasm in [False, True]:
            for auto_option in [False, True]:
                with self.subTest(wasm=wasm, auto_option=auto_option):
                    p = plan(fixture(wasm=wasm, auto_option=auto_option), print_query=True)
                    idle = "({state:document.querySelector('[data-native-print]').dataset.nativePrintState,requests,compilerRequests,downloads:pdfDownloads,calls:printCalls,busy:document.querySelector('[data-native-print]').hasAttribute('aria-busy'),hidden:document.querySelector('[data-native-print-download]').hidden})"
                    loaded = wait("document.readyState==='complete' && window.TriptychNativePrint")
                    p['acts'] = [*idle_arrivals('/print/example.html', loaded, idle),
                        *p['acts'][2:], act('compilerRequests.length', 'compilations')]
                    seen = drive(p)
                    for arrival in ['normal', 'query', 'reload', 'background']:
                        self.assertEqual(seen[arrival], {'state': 'idle', 'requests': [], 'compilerRequests': [],
                            'downloads': 0, 'calls': 0, 'busy': False, 'hidden': True}, seen)
                    self.assertTrue(seen['hidden'], seen)
                    self.assertEqual(seen['result']['state'], 'ready', seen)
                    self.assertEqual(seen['result']['downloads'], 1, seen)
                    self.assertEqual(seen['compilations'], int(wasm), seen)
                    self.assertEqual(len([request for request in seen['result']['requests'] if request['method'] == 'POST']),
                                     int(not wasm), seen)

    def test_service_paths_keep_the_configured_reverse_proxy_prefix(self):
        result = drive(plan(fixture(service_prefix=True), print_query=True))["result"]
        self.assertEqual(result["state"], "ready", result)
        self.assertEqual(result["downloads"], 1)
        self.assertEqual(result["calls"], 0)
        self.assertTrue(all(row["url"].startswith("http://localhost:9999/typesetting/v1/jobs")
                            for row in result["requests"]))
        self.assertTrue(result["download"].startswith("http://localhost:9999/typesetting/v1/jobs/"))

    def test_native_wasm_compiler_takes_precedence_and_downloads_verified_pdf(self):
        p = plan(fixture(wasm=True, empty=True), print_query=True)
        p["acts"].append(act("({requests:compilerRequests,type:document.querySelector('[data-native-print-download]').download})", "compiler"))
        observed = drive(p)
        result = observed["result"]
        self.assertEqual(result["state"], "ready", observed)
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["requests"], [])
        self.assertEqual(result["downloads"], 1)
        self.assertTrue(result["download"].startswith("blob:"))
        request = observed["compiler"]["requests"][0]
        self.assertEqual(request["bundleSHA256"], "c" * 64)
        self.assertEqual(request["runtimeSHA256"], "d" * 64)
        self.assertEqual(request["bundleBytes"], 123)
        self.assertEqual(observed["compiler"]["type"], "example-gpt.pdf")

    def test_changed_compiler_pdf_is_refused_without_browser_or_service_fallback(self):
        result = drive(plan(fixture(wasm=True, failure="wasm-sha"), print_query=True))["result"]
        self.assertEqual(result["state"], "error", result)
        self.assertIn("failed verification", result["status"])
        self.assertEqual(result["requests"], [])
        self.assertEqual(result["downloads"], 0)
        self.assertEqual(result["calls"], 0)

    def test_click_companion_requests_native_tex_and_exposes_download(self):
        result = drive(plan(fixture(companion=True)))["result"]
        self.assertEqual(result["state"], "ready", result)
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["downloads"], 1)
        request = json.loads(result["requests"][0]["body"])
        self.assertEqual(request, {"document": "publication:gpt/example", "edition": "synthesis", "source_revision": "a" * 40})
        self.assertTrue(all(item["credentials"] == "omit" for item in result["requests"]))
        self.assertFalse(result["hidden"])
        self.assertTrue(result["download"].endswith("/pdf"))

    def test_explicit_native_volume_action_never_opens_browser_print(self):
        result = drive(plan(fixture(), print_query=True))["result"]
        self.assertEqual(result["state"], "ready", result)
        self.assertEqual(result["downloads"], 1)
        self.assertEqual(result["calls"], 0)

    def test_unconfigured_service_refuses_without_fetch_or_browser_fallback(self):
        result = drive(plan(fixture(empty=True), print_query=True))["result"]
        self.assertEqual(result["state"], "error", result)
        self.assertIn("not connected", result["status"])
        self.assertEqual(result["requests"], [])
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["downloads"], 0)

    def test_mismatch_failure_and_unfinished_download_are_refused(self):
        for failure in ("stale", "different", "host", "failed", "partial"):
            with self.subTest(failure=failure):
                result = drive(plan(fixture(failure=failure), print_query=True))["result"]
                self.assertEqual(result["state"], "error", result)
                self.assertTrue(result["hidden"])
                self.assertIsNone(result["download"])
                self.assertEqual(result["calls"], 0)
                self.assertEqual(result["downloads"], 0)

    def test_cancellation_aborts_pending_request_without_printing(self):
        result = drive(plan(fixture(failure="pending"), cancellation=True))["result"]
        self.assertEqual(result["state"], "cancelled", result)
        self.assertTrue(result["hidden"])
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["downloads"], 0)


def interactive_fixture():
    """A held compiler the test releases or fails, on a page with in-page links."""
    identity = "papal:papal.leo-xiii.hf-l-xiii-enc-15051891-rerum-novarum/en"
    row = {"id": identity, "output_id": identity, "document": identity, "edition": "main", "title": "Rerum Novarum"}
    context = {"documents": {identity: row}, "source_revision": "a" * 40, "endpoint": "", "archives": {},
               "native_catalog": {"selections": {identity: {
                   "bundle_href": "native-tex/sources/" + "c" * 64 + ".json", "bundle_sha256": "c" * 64, "bundle_bytes": 123}},
                   "runtime": {"href": "native-tex/runtime.json", "sha256": "d" * 64, "bytes": 456}}}
    head, tail = native.extras("papal-documents/example.html")
    hook = """
      window.calls=[];window.announcements=0;window.keys=[];window.progressTexts=[];
      window.TriptychNativeTeX={generate:(options)=>new Promise((resolve,reject)=>{
        const call={aborted:false};calls.push(call);
        options.signal.addEventListener('abort',()=>{call.aborted=true;reject(new DOMException('Cancelled','AbortError'));},{once:true});
        const stage='Checking the original sources and print runtime';
        for(let index=0;index<=60;index++){options.onProgress({stage,loadedBytes:index*1048576,totalBytes:60*1048576,
          message:stage+' ('+index+'.0 of 60.0 MiB)… Keep this page visible until it finishes.'});
          progressTexts.push(document.querySelector('[data-native-print-progress]').textContent);}
        for(let pass=1;pass<=2;pass++)for(let repeat=0;repeat<3;repeat++)
          options.onProgress({message:'Typesetting with the original TeX layout (pass '+pass+')… Keep this page visible until it finishes.'});
        options.onProgress({stage:'ready',message:'The typeset PDF is ready.'});
        call.release=async()=>{const bytes=new TextEncoder().encode('%PDF-1.4\\nheld fixture\\n%%EOF');
          const hash=await crypto.subtle.digest('SHA-256',bytes);
          resolve({bytes,byteLength:bytes.byteLength,sha256:Array.from(new Uint8Array(hash),n=>n.toString(16).padStart(2,'0')).join('')});};
        call.fail=()=>reject(new Error('Native TeX compilation failed.'));
      })};
      addEventListener('keydown',event=>{if(event.key==='p')keys.push({prevented:event.defaultPrevented,shift:event.shiftKey});});
    """
    body = ('<nav><a id="toc" href="#part-2">Part 2</a> <a id="elsewhere" href="#part-3">Part 3</a></nav>'
            + native.controls(identity, "papal-documents/example.html", context)
            + '<div style="height:3000px"></div><h2 id="part-2">Part 2</h2><div style="height:3000px"></div>'
            + '<h2 id="part-3">Part 3</h2><script>' + hook + '</script>' + tail
            + '<script>window.downloads=0;document.querySelector("[data-native-print-download]").addEventListener("click",'
            + 'event=>{event.preventDefault();downloads++;});new MutationObserver(records=>{announcements+=records.length;})'
            + '.observe(document.querySelector("[data-native-print-status]"),{childList:true,characterData:true,subtree:true});</script>')
    page = ('<!doctype html><html><head>' + head + '</head><body style="font-family:Georgia,serif">'
            + body + '</body></html>')
    return {"papal-documents/example.html": page,
            "shared/native-print.js": (ROOT / "src/web/browser/shared/native-print.js").read_text(),
            "shared/native-print.css": (ROOT / "src/web/browser/shared/native-print.css").read_text()}


SNAPSHOT = """(()=>{const root=document.querySelector('[data-native-print]'),q=s=>root.querySelector(s);
  const download=q('[data-native-print-download]');
  return {state:root.dataset.nativePrintState,status:q('[data-native-print-status]').textContent,
    progress:q('[data-native-print-progress]').textContent,startDisabled:q('[data-native-print-start]').disabled,
    cancelHidden:q('[data-native-print-cancel]').hidden,downloadHidden:download.hidden,href:download.getAttribute('href'),
    filename:download.download,focus:document.activeElement.dataset&&Object.keys(document.activeElement.dataset)[0]||document.activeElement.id||document.activeElement.tagName,
    calls:calls.length,aborted:calls.map(call=>call.aborted),hash:location.hash,announcements,downloads};})()"""


def held(name):
    return act(SNAPSHOT, name)


class NativeInteractionTests(unittest.TestCase):
    """In-page navigation, keyboard print, focus, announcements and file name."""

    def test_in_page_navigation_keyboard_print_focus_and_announcements(self):
        observed = drive({"responses": interactive_fixture(), "acts": [
            {"do": "navigate", "url": "/papal-documents/example.html"},
            wait("document.querySelector('[data-native-print]').dataset.nativePrintState==='idle'"),
            act("(()=>{const style=getComputedStyle(document.querySelector('[data-native-print-start]'));"
                "return {font:style.fontFamily,border:style.borderTopStyle,radius:style.borderTopLeftRadius,"
                "statusHeight:document.querySelector('[data-native-print-status]').getBoundingClientRect().height};})()", "style"),
            {"do": "key", "key": "p", "code": "KeyP", "modifiers": 2},
            {"do": "key", "key": "p", "code": "KeyP", "modifiers": 10},
            held("afterKeys"),
            {"do": "click", "selector": "[data-native-print-start]"},
            wait("calls.length===1"), held("started"),
            {"do": "key", "key": "p", "code": "KeyP", "modifiers": 2},
            {"do": "click", "selector": "#toc"}, wait("location.hash==='#part-2'"),
            act("scrollTo(0,0);history.back()"), wait("location.hash===''"),
            held("duringNavigation"),
            act("calls[0].release()"), wait("document.querySelector('[data-native-print]').dataset.nativePrintState==='ready'"),
            held("ready"),
            {"do": "click", "selector": "#toc"}, wait("location.hash==='#part-2'"),
            act("scrollTo(0,0);history.back()"), wait("location.hash===''"),
            act("location.hash='part-3'"), wait("location.hash==='#part-3'"),
            held("afterNavigation"),
            act("fetch(document.querySelector('[data-native-print-download]').href).then(response=>response.text())", "blob"),
            act("keys", "keys"), act("progressTexts", "progressTexts"),
        ]})
        self.assertEqual(observed["style"]["font"], "Georgia, serif", observed)
        self.assertEqual(observed["style"]["border"], "solid")
        self.assertEqual(observed["style"]["statusHeight"], 0)
        self.assertEqual(observed["keys"], [{"prevented": False, "shift": False}, {"prevented": False, "shift": True},
                                            {"prevented": False, "shift": False}])
        self.assertEqual(observed["afterKeys"]["state"], "idle")
        self.assertEqual(observed["afterKeys"]["calls"], 0)
        started = observed["started"]
        self.assertEqual((started["state"], started["focus"], started["startDisabled"], started["cancelHidden"]),
                         ("preparing", "nativePrintCancel", True, False), started)
        during = observed["duringNavigation"]
        self.assertEqual((during["state"], during["aborted"], during["calls"]), ("preparing", [False], 1), during)
        # Bytes went to the non-live line; the typesetting stage then cleared it.
        self.assertEqual(during["progress"], "")
        self.assertIn("30.0 of 60.0 MiB", observed["progressTexts"])
        self.assertIn("60.0 of 60.0 MiB", observed["progressTexts"])
        self.assertIn("pass 2", during["status"])
        ready = observed["ready"]
        self.assertEqual((ready["state"], ready["focus"], ready["downloadHidden"], ready["downloads"]),
                         ("ready", "nativePrintDownload", False, 1), ready)
        self.assertEqual(ready["filename"], "1891-05-15-rerum-novarum-en.pdf")
        self.assertEqual(ready["progress"], "")
        # Preparing, one byte stage, two typesetting passes and ready: not one per progress event.
        self.assertEqual(ready["announcements"], 5, ready)
        after = observed["afterNavigation"]
        self.assertEqual((after["state"], after["downloadHidden"], after["href"], after["status"]),
                         ("ready", False, ready["href"], ready["status"]), after)
        self.assertTrue(after["href"].startswith("blob:"))
        self.assertTrue(observed["blob"].startswith("%PDF-"))

    def test_leaving_cancelling_failing_and_returning_keep_controls_coherent(self):
        hide = "dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}))"
        show = "dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))"
        state = "document.querySelector('[data-native-print]').dataset.nativePrintState"
        observed = drive({"responses": interactive_fixture(), "acts": [
            {"do": "navigate", "url": "/papal-documents/example.html"}, wait(state + "==='idle'"),
            {"do": "click", "selector": "[data-native-print-start]"}, wait("calls.length===1"),
            act(hide), held("leftDuringBuild"), act(show), held("returnedAfterBuildStopped"),
            {"do": "click", "selector": "[data-native-print-start]"}, wait("calls.length===2"),
            act("calls[1].release()"), wait(state + "==='ready'"),
            act(hide), act(show), held("returnedToReady"),
            act("fetch(document.querySelector('[data-native-print-download]').href).then(response=>response.text())", "blob"),
            {"do": "click", "selector": "[data-native-print-start]"}, wait("calls.length===3"),
            {"do": "click", "selector": "[data-native-print-cancel]"}, wait(state + "==='cancelled'"),
            held("cancelled"),
            {"do": "click", "selector": "[data-native-print-start]"}, wait("calls.length===4"),
            act("calls[3].fail()"), wait(state + "==='error'"), held("failed"),
            {"do": "click", "selector": "[data-native-print-start]"}, wait("calls.length===5"),
            act("document.querySelector('#elsewhere').focus()"),
            act("calls[4].release()"), wait(state + "==='ready'"), held("readerMovedOn"),
        ]})
        left = observed["leftDuringBuild"]
        self.assertEqual((left["state"], left["aborted"], left["startDisabled"], left["cancelHidden"]),
                         ("cancelled", [True], False, True), left)
        self.assertIn("left this page", left["status"])
        back = observed["returnedAfterBuildStopped"]
        self.assertEqual((back["state"], back["downloadHidden"], back["startDisabled"]), ("cancelled", True, False), back)
        ready = observed["returnedToReady"]
        self.assertEqual((ready["state"], ready["downloadHidden"], ready["cancelHidden"]), ("ready", False, True), ready)
        self.assertIn("ready", ready["status"])
        self.assertTrue(observed["blob"].startswith("%PDF-"))
        cancelled = observed["cancelled"]
        self.assertEqual((cancelled["focus"], cancelled["downloadHidden"], cancelled["aborted"][2]),
                         ("nativePrintStart", True, True), cancelled)
        failed = observed["failed"]
        self.assertEqual((failed["focus"], failed["downloadHidden"], failed["startDisabled"]),
                         ("nativePrintStart", True, False), failed)
        self.assertIn("compilation failed", failed["status"])
        self.assertEqual(observed["readerMovedOn"]["focus"], "elsewhere")


if __name__ == "__main__":
    unittest.main()
