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
import _web_print as web
from .test_web_print_controller import drive, act, wait, idle_arrivals


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
                provider = path.relative_to(ROOT / "release/publications").parts[0]
                self.assertNotIn("publication:" + provider + "/" + record["id"], self.documents)

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

    def test_common_and_legacy_pages_use_native_controls_and_preserve_reading(self):
        identity, row = next(iter(self.documents.items()))
        context = native.site_context(ROOT, documents=self.documents, revision="b" * 40, endpoint="")
        descriptor = {"id": identity, "title": row["title"]}
        page = web._page(descriptor, '<p id="source">Source text.</p>', "print/example.html", native_context=context)
        self.assertIn("Source text.", page["html"])
        self.assertIn('data-native-print-start', page["html"])
        self.assertNotIn('data-web-print-start', page["html"])
        self.assertIn("shared/native-print.js", page["body_extra"])
        inventory = {"pages": {}, "reader_actions": {"reading-plans/full.html": {
            "native_controls": "NATIVE-CONTROLS", "native_head_extra": "NATIVE-HEAD", "native_body_extra": "NATIVE-TAIL"}}}
        legacy = web.decorate_source_page("reading-plans/full.html", {"html": "CANONICAL-READING"}, inventory)
        self.assertEqual(legacy["html"], "NATIVE-CONTROLSCANONICAL-READING")
        self.assertEqual(legacy["body_extra"], "NATIVE-TAIL")

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


def fixture(*, empty=False, failure=None, legacy=False, companion=False, wasm=False, service_prefix=False, auto_option=False):
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
    body = ('<section data-web-print-document="' + identity + '">' + body + '</section>')
    if legacy:
        body += '<article data-print-volume="full"><button data-print-volume-start hidden>Old browser Print</button></article>'
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
    body += '<script>' + hook + '</script><script src="../shared/web-print.js"></script>'
    if legacy:
        body += '<script src="../shared/print-volume.js"></script>'
    body += '<script src="../shared/native-print.js"></script>'
    if auto_option:
        body += "<script>const root=document.querySelector('[data-native-print]');TriptychNativePrint.install(root,JSON.parse(root.querySelector('[data-native-print-manifest]').textContent),{auto:true});</script>"
    responses = {"print/example.html": '<!doctype html><html><body>' + body + '</body></html>',
                 "shared/native-print.js": (ROOT / "src/web/browser/shared/native-print.js").read_text(),
                 "shared/print-volume.js": (ROOT / "src/web/browser/shared/print-volume.js").read_text()}
    return responses


def plan(responses, *, print_query=False, cancellation=False):
    actions = [{"do": "navigate", "url": "/print/example.html" + ("?print=1" if print_query else "")},
               wait("window.TriptychNativePrint && document.querySelector('[data-native-print]').dataset.nativePrintState")]
    actions.append({"do": "click", "selector": "[data-native-print-start]"})
    if cancellation:
        actions.extend([wait("requests.length===1"), act("document.querySelector('[data-native-print-cancel]').click()")])
    actions.extend([wait("!document.querySelector('[data-native-print-start]').disabled"),
                    act("({state:document.querySelector('[data-native-print]').dataset.nativePrintState,status:document.querySelector('[data-native-print-status]').textContent,download:document.querySelector('[data-native-print-download]').getAttribute('href'),hidden:document.querySelector('[data-native-print-download]').hidden,calls:printCalls,downloads:pdfDownloads,requests,oldPrintVisible:!!document.querySelector('[data-print-volume-start]:not([hidden])')})", "result")])
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

    def test_keyboard_print_requests_native_pdf_instead_of_browser_print(self):
        p = plan(fixture())
        p["acts"][2] = {"do": "key", "key": "p", "code": "KeyP", "modifiers": 2}
        result = drive(p)["result"]
        self.assertEqual(result["state"], "ready", result)
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["downloads"], 1)

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
        self.assertEqual(observed["compiler"]["type"], "example.pdf")

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
        result = drive(plan(fixture(legacy=True), print_query=True))["result"]
        self.assertEqual(result["state"], "ready", result)
        self.assertEqual(result["downloads"], 1)
        self.assertEqual(result["calls"], 0)
        self.assertFalse(result["oldPrintVisible"])

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


if __name__ == "__main__":
    unittest.main()
