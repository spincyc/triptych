"""The native print compile gate fails closed on tiny synthetic bundles.

Each case materializes a served-format bundle through the same path the gate
uses for the admitted universe, then compiles it with host TeX. Cases that need
an engine skip where it is absent; the parsing and set checks never do.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print_bundles as bundles
import _native_print_compile as gate

REVISION = "0" * 40
IDENTITY = "publication:gpt/tests/synthetic"
SHARED_PART = b"Shared words, delivered by URL.\n"
# The browser runtime carries Latin Modern and Libertinus, not Computer Modern.
LMODERN = b"\\usepackage[T1]{fontenc}\n\\usepackage{lmodern}\n"
GOOD = (b"\\documentclass{article}\n" + LMODERN + b"\\begin{document}\nSee section~\\ref{s}.\n"
        b"\\section{Synthetic}\\label{s}\n\\input{part}\n\\end{document}\n")


def have(*programs):
    return all(shutil.which(program) for program in programs)


def served(identity, files, *, engine="pdftex", shared=None):
    """One bundle in the exact transport shape the Pages build serves."""
    records, assets = [], {}
    for path, payload in sorted({**files, **(shared or {})}.items()):
        if shared and path in shared:
            digest = hashlib.sha256(payload).hexdigest()
            assets["native-tex/assets/" + digest + ".bin"] = payload
            records.append({"path": path, "encoding": "url", "href": "../assets/" + digest + ".bin",
                            "bytes": len(payload), "sha256": digest})
        else:
            records.append({"path": path, "encoding": "utf8", "content": payload.decode("utf-8"),
                            "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    bundle = {"schema": bundles.SCHEMA, "document": identity, "output_id": identity, "edition": "main",
              "title": "Synthetic", "source_revision": REVISION, "engine": engine,
              "format": gate.ENGINES[engine], "entrypoint": "src/test/main.tex", "cwd": "src/test",
              "environment": {"TEXINPUTS": "..:"} if engine == "pdftex" else {},
              "options": dict(gate.OPTIONS), "files": records}
    bundle["render_sha256"] = bundles.render_identity(bundle)
    bundle["content_sha256"] = hashlib.sha256(bundles.canonical(bundle)).hexdigest()
    payload = bundles.canonical(bundle) + b"\n"
    route = "native-tex/sources/" + bundle["content_sha256"] + ".json"
    assets[route] = payload
    return {"route": route, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}, assets


def catalog(*entries):
    result = {"schema": bundles.CATALOG_SCHEMA, "source_revision": REVISION, "bundles": {}, "assets": {}}
    for identity, (described, assets) in entries:
        result["bundles"][identity] = described
        result["assets"].update(assets)
    return result


class Workspace(unittest.TestCase):
    def setUp(self):
        base = ROOT / ".scratch/native-print-compile-tests"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.out = self.work / "out"
        self.runtime = ROOT / gate.RUNTIME

    def prepare(self, main=GOOD, *, engine="pdftex", extra=None, identity=IDENTITY):
        files = {"src/test/main.tex": main, **(extra or {})}
        shared = {"src/test/part.tex": SHARED_PART} if b"\\input{part}" in main else None
        built = catalog((identity, served(identity, files, engine=engine, shared=shared)))
        return gate.materialize(built, {identity: {}}, self.out, revision=REVISION, epoch=1700000000)

    def runtime_without(self, *names, prefix=None):
        manifest = json.loads(self.runtime.read_text(encoding="utf-8"))
        manifest["texFiles"] = [row for row in manifest["texFiles"] if row["name"] not in names
                                and not (prefix and row["name"].startswith(prefix))]
        path = self.work / "runtime.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def compile(self, runtime=None):
        summary = gate.compile_all(self.out, runtime_path=runtime or self.runtime, jobs=2)
        receipts = [json.loads(path.read_text(encoding="utf-8")) for path in (self.out / "receipts").glob("*.json")]
        return summary, receipts


class PureChecks(Workspace):
    def test_runtime_members_match_by_name_or_lookup_stem_of_the_same_format(self):
        runtime = gate.load_runtime(self.runtime)
        self.assertIsNotNone(gate.runtime_member(runtime, "article.cls"))
        self.assertIsNotNone(gate.runtime_member(runtime, "ecrm1095.tfm"))  # registered as `ecrm1095`
        self.assertIsNone(gate.runtime_member(runtime, "ecrm1095.otf"))
        self.assertIsNone(gate.runtime_member(runtime, "definitely-not-a-runtime-member.sty"))

    def test_driver_trace_keeps_successful_opens_split_by_mode(self):
        trace = ("kdebug:fopen(/fonts/a.otf, rb) => 0x55\nkdebug:fopen(/fonts/missing.otf, rb) => (nil)\n"
                 "kdebug:fopen(out.pdf, wb) => 0x56\nkdebug:fclose(0x55) => 0\n")
        reads, writes = gate.parse_fopen_trace(trace, Path("/work"))
        self.assertEqual(reads, {"/fonts/a.otf"})
        self.assertEqual(writes, {"/work/out.pdf"})

    def test_admitted_and_prepared_sets_must_agree_before_anything_is_written(self):
        built = catalog((IDENTITY, served(IDENTITY, {"src/test/main.tex": b"x"})))
        with self.assertRaisesRegex(gate.CompileError, "missing .*publication:gpt/tests/other"):
            gate.materialize(built, {IDENTITY: {}, "publication:gpt/tests/other": {}}, self.out,
                             revision=REVISION, epoch=0)
        with self.assertRaisesRegex(gate.CompileError, "unadmitted .*publication:gpt/tests/synthetic"):
            gate.materialize(built, {"publication:gpt/tests/other": {}}, self.out, revision=REVISION, epoch=0)
        with self.assertRaisesRegex(gate.CompileError, "no native print edition is admitted"):
            gate.materialize(catalog(), {}, self.out, revision=REVISION, epoch=0)
        self.assertFalse(self.out.exists())

    def test_materialized_set_must_match_the_index_before_compilation(self):
        self.prepare()
        extra = self.out / "editions" / "unadmitted-edition"
        extra.mkdir()
        with self.assertRaisesRegex(gate.CompileError, "materialized native print directories differ"):
            gate.compile_all(self.out, runtime_path=self.runtime, jobs=1)
        extra.rmdir()
        shutil.rmtree(next((self.out / "editions").iterdir()))
        with self.assertRaisesRegex(gate.CompileError, "materialized native print directories differ"):
            gate.compile_all(self.out, runtime_path=self.runtime, jobs=1)

    def test_changed_source_after_preparation_is_refused(self):
        index = self.prepare()
        edition = index["editions"][IDENTITY]
        (self.out / "editions" / edition["directory"] / "src/test/main.tex").write_bytes(b"changed\n")
        with self.assertRaisesRegex(gate.CompileError, "changed after preparation"):
            gate.compile_all(self.out, runtime_path=self.runtime, jobs=1)

    def test_preparation_never_replaces_an_unrelated_directory(self):
        self.out.mkdir()
        (self.out / "keep.txt").write_text("not ours\n", encoding="utf-8")
        with self.assertRaisesRegex(gate.CompileError, "did not prepare"):
            self.prepare()
        self.assertTrue((self.out / "keep.txt").is_file())


@unittest.skipUnless(have("pdflatex", "pdfinfo"), "host pdfTeX and poppler are required")
class PdfTeXGate(Workspace):
    def test_synthetic_bundle_compiles_from_its_bundle_and_runtime_alone(self):
        self.prepare()
        summary, (receipt,) = self.compile()
        self.assertEqual(summary["status"], "pass", receipt)
        self.assertEqual((receipt["status"], receipt["engine"], receipt["passes"], receipt["pages"]),
                         ("pass", "pdftex", 2, 1))
        self.assertRegex(receipt["pdf_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(receipt["closure"]["bundle_files_opened"], 2)
        self.assertGreater(receipt["closure"]["runtime_members_opened"], 0)
        self.assertTrue((self.out / "summary.json").is_file())
        with self.assertRaisesRegex(gate.CompileError, "already compiled"):
            gate.compile_all(self.out, runtime_path=self.runtime, jobs=1)

    def test_broken_bundle_fails(self):
        self.prepare(b"\\documentclass{article}\n\\begin{document}\n\\undefinedmacro\n\\end{document}\n")
        summary, (receipt,) = self.compile()
        self.assertEqual((summary["status"], summary["failed"]), ("fail", [IDENTITY]))
        self.assertIn("pdflatex exited 1 on pass 1", receipt["problems"])
        self.assertIsNone(receipt["pdf_sha256"])

    def test_package_absent_from_the_runtime_is_a_closure_violation(self):
        self.prepare()
        summary, (receipt,) = self.compile(self.runtime_without("size10.clo", "size10"))
        self.assertEqual(summary["status"], "fail")
        self.assertTrue(any(problem.startswith("opened a file outside the bundle and the runtime: ")
                            and problem.endswith("/size10.clo") for problem in receipt["problems"]), receipt)

    def test_work_tree_file_outside_the_bundle_is_a_closure_violation(self):
        index = self.prepare(b"\\documentclass{article}\n" + LMODERN + b"\\begin{document}\n\\input{stray}\n\\end{document}\n")
        base = self.out / "editions" / index["editions"][IDENTITY]["directory"]
        (base / "src/test/stray.tex").write_text("Not in the bundle.\n", encoding="utf-8")
        summary, (receipt,) = self.compile()
        self.assertEqual(summary["status"], "fail")
        self.assertIn("opened a work-tree file outside the bundle: src/test/stray.tex", receipt["problems"])

    def test_edition_that_never_settles_fails_at_the_maximum_passes(self):
        self.prepare(b"\\documentclass{article}\n" + LMODERN + b"\\makeatletter\n\\newcount\\runs\n"
                     b"\\def\\seen#1{\\global\\runs=#1\\relax}\n"
                     b"\\AtBeginDocument{\\global\\advance\\runs by 1 "
                     b"\\immediate\\write\\@auxout{\\string\\seen{\\the\\runs}}}\n"
                     b"\\makeatother\n\\begin{document}\nRun \\the\\runs.\n\\end{document}\n")
        summary, (receipt,) = self.compile()
        self.assertEqual(summary["status"], "fail")
        self.assertEqual(receipt["passes"], gate.OPTIONS["max_passes"])
        self.assertIn("references or contents did not settle within 8 passes", receipt["problems"])


@unittest.skipUnless(have("xelatex", "xdvipdfmx", "pdfinfo", "kpsewhich"), "host XeTeX and poppler are required")
class XeTeXGate(Workspace):
    SOURCE = (b"\\documentclass{article}\n\\usepackage{fontspec}\n"
              b"\\setmainfont[Ligatures=TeXOff]{Latin Modern Roman}\n"
              b"\\begin{document}\nAgnus Dei.\n\\end{document}\n")

    def test_runtime_font_family_compiles_and_is_traced_through_the_driver(self):
        self.prepare(self.SOURCE, engine="xetex")
        summary, (receipt,) = self.compile()
        self.assertEqual(summary["status"], "pass", receipt)
        self.assertEqual(receipt["engine"], "xetex")
        self.assertEqual(summary["runtime_fonts_located"], summary["runtime_fonts"])

    def test_font_family_absent_from_the_runtime_fails(self):
        # Removing one optical size is not enough: fontconfig, like the
        # browser's font database, then resolves the family to another runtime
        # face. With no Latin Modern Roman face at all, the family is unknown.
        self.prepare(self.SOURCE, engine="xetex")
        summary, (receipt,) = self.compile(self.runtime_without(prefix="lmroman"))
        self.assertEqual(summary["status"], "fail", receipt)
        self.assertEqual(summary["runtime_fonts_located"], summary["runtime_fonts"])
        self.assertIn("xelatex exited 1 on pass 1", receipt["problems"])
        self.assertTrue(any("not be found" in line or "not found" in line for line in receipt["output_tail"]))


if __name__ == "__main__":
    unittest.main()
