"""Print pages, Print actions, public admission and native artwork selection."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print as native
import _native_print_artwork as artwork
from _document_schema import release_record


def context(*, wasm=False, archive=False):
    identity = "publication:gpt/example-synthesis"
    row = {"id": identity, "output_id": identity, "document": "publication:gpt/example",
           "edition": "synthesis", "title": "Canonical <edition>"}
    value = {"documents": {identity: row}, "source_revision": "a" * 40, "endpoint": "", "archives": {}}
    if archive:
        value["archives"][identity] = {"url": "https://github.com/spincyc/triptych-artifacts/releases/download/prints-abcdef0/x.pdf",
                                       "snapshot": "abcdef0" + "0" * 33}
    if wasm:
        value["native_catalog"] = {"selections": {identity: {
            "bundle_href": "native-tex/sources/" + "c" * 64 + ".json", "bundle_sha256": "c" * 64, "bundle_bytes": 1}},
            "runtime": {"href": "native-tex/runtime.json", "sha256": "d" * 64, "bytes": 2}}
    return identity, value


class PrintPageTests(unittest.TestCase):
    def test_routes_keep_print_paths_and_place_source_editions_under_print(self):
        self.assertEqual(native.print_route("publication:gpt/a/b-homily"), "print/gpt/a/b-homily.html")
        self.assertEqual(native.print_route("bible:douay-rheims"), "print/bibles/douay-rheims.html")
        self.assertEqual(native.print_route("papal:x/la", "papal-documents/x--la.html"),
                         "print/papal-documents/x--la.html")
        self.assertEqual(native.print_route("reading-plan:v", "reading-plans/v.html"), "print/reading-plans/v.html")
        for identity, reader in (("papal:x/la", None), ("papal:x/la", "print/papal-documents/x.html"),
                                 ("reading-plan:v", "../v.html"), ("other:v", "v.html"), ("bible:../x", None)):
            with self.subTest(identity=identity, reader=reader), self.assertRaises(native.NativePrintError):
                native.print_route(identity, reader)

    def test_landing_is_small_and_carries_identity_controls_archive_and_reader(self):
        identity, value = context(wasm=True, archive=True)
        route = "print/gpt/example-synthesis.html"
        page = native.landing(identity, route, value, label="ChatGPT edition · Synthesis",
                              reader="web/gpt/example.html")
        body = page["html"]
        self.assertEqual((page["output_id"], page["title"]), (identity, "Canonical <edition>"))
        self.assertIn("<h1>Canonical &lt;edition&gt;</h1>", body)
        self.assertIn("ChatGPT edition · Synthesis", body)
        self.assertIn("in your browser", body)
        self.assertIn("data-native-print-start", body)
        self.assertIn("Download earlier TeX PDF", body)
        self.assertIn('href="../../web/gpt/example.html">Read this edition online', body)
        self.assertIn("shared/native-tex.js", page["body_extra"])
        self.assertIn("shared/native-print.css", page["head_extra"])
        self.assertNotIn("web-print", body + page["head_extra"] + page["body_extra"])
        self.assertLess(len(body.encode()), 4_000)

    def test_landing_without_reader_or_compiler_names_the_service_and_offers_no_reading(self):
        identity, value = context()
        page = native.landing(identity, "print/gpt/example-synthesis.html", value, label="Synthesis")
        self.assertNotIn("Read this edition online", page["html"])
        self.assertNotIn("in your browser", page["html"])
        self.assertNotIn("native-tex.js", page["body_extra"])
        with self.assertRaises(native.NativePrintError):
            native.landing("publication:gpt/held", "print/gpt/held.html", value, label="Held")
        with self.assertRaises(native.NativePrintError):
            native.landing(identity, "print/gpt/example-synthesis.html", value, label=" ")

    def test_reader_fragment_link_and_reader_action_are_route_relative(self):
        identity, value = context()
        page = native.landing(identity, "print/bibles/x.html", value, label="Complete Bible",
                              reader="sources/index.html#edition=edition.x", reader_label="Find it <here>")
        self.assertIn('href="../../sources/index.html#edition=edition.x">Find it &lt;here&gt;</a>', page["html"])
        action = native.reader_action("papal-documents/x.html", "print/papal-documents/x.html")
        self.assertEqual(action, '<p class="print-actions"><a href="../print/papal-documents/x.html?print=1">'
                                 'Print / Generate PDF</a></p>')
        with self.assertRaises(native.NativePrintError):
            native.reader_action("web/gpt/x.html", "web/gpt/x.html")


class AdmissionTests(unittest.TestCase):
    def test_admission_inputs_name_every_declaration_and_disposition(self):
        inputs = native.admission_inputs(ROOT)
        for row in native._admitted_recipes(ROOT):
            if row["family"] == "publication":
                self.assertIn("release/publications/" + row["provider"] + "/" + row["document"] + ".json", inputs)
                self.assertIn("src/" + row["provider"] + "/" + row["canonical"] + "/web-edition.toml", inputs)
        held = [path.relative_to(ROOT).as_posix() for path in (ROOT / "release/publications").glob("*/**/*.json")
                if json.loads(path.read_bytes()).get("status") == "hold"]
        self.assertTrue(set(held) <= set(inputs))
        self.assertTrue(all((ROOT / path).is_file() for path in inputs))

    def test_holds_and_withdrawals_are_not_admitted_and_bibles_are(self):
        documents = native.admitted_documents(ROOT)
        families = {identity.partition(":")[0] for identity in documents}
        self.assertEqual(families, {"publication", "bible", "papal", "reading-plan"})
        recipes = native._admitted_recipes(ROOT)
        self.assertEqual({row["id"] for row in recipes},
                         {identity for identity in documents if identity.startswith(("publication:", "bible:"))})
        for path in (ROOT / "release/publications").glob("*/**/*.json"):
            record = release_record(ROOT, path)
            provider = path.relative_to(ROOT / "release/publications").parts[0]
            if record.get("status") == "hold":
                self.assertNotIn("publication:" + provider + "/" + record["id"], documents)
        for path in ROOT.glob("src/*/**/web-edition.toml"):
            if tomllib.loads(path.read_text(encoding="utf-8")).get("withdrawn"):
                provider = path.relative_to(ROOT / "src").parts[0]
                leaf = path.parent.relative_to(ROOT / "src" / provider).as_posix()
                self.assertFalse(any(row["document"] == "publication:" + provider + "/" + leaf
                                     for row in documents.values()))


class ArtworkSelectionTests(unittest.TestCase):
    def test_dictionary_editions_select_owned_raster_artwork_only(self):
        owner = "src/gpt/" + artwork.DICTIONARY + "/"
        every = {path.relative_to(ROOT).as_posix() for path in (ROOT / owner).rglob("*.png")}
        for leaf in artwork.DICTIONARY_LEAVES:
            with self.subTest(leaf=leaf):
                selected, inputs = artwork.dictionary_artwork(ROOT, "gpt", artwork.DICTIONARY + "/" + leaf)
                self.assertTrue(selected)
                self.assertLess(len(selected), len(every))
                self.assertTrue(all(path.startswith(owner) and (ROOT / path).is_file() for path in selected))
                self.assertIn(owner + leaf + "/main.tex", inputs)
                self.assertIn(artwork.HELPER, inputs)
                self.assertIn("tools/source-library", inputs)
                self.assertTrue(any(path.startswith("src/sources/") and path.endswith("/edition.toml")
                                    for path in inputs), "exact source edition labels must affect bundle identity")
                self.assertTrue(any(path.startswith("src/sources/") and "/artifacts/" in path
                                    and path.endswith(".toml") for path in inputs),
                                "source binding metadata must affect bundle identity")
        with self.assertRaises(artwork.ArtworkError):
            artwork.dictionary_artwork(ROOT, "gpt", artwork.DICTIONARY + "/unknown")

    def test_server_guides_select_pencil_plates_through_active_diagrams_and_cards_none(self):
        owner = "src/gpt/" + artwork.SERVER + "/"
        dictionary = "src/gpt/" + artwork.DICTIONARY + "/shared/artwork/pencil/"
        pencil = re.compile("(?:" + re.escape(owner + "shared/artwork/pencil/") + "|"
                            + re.escape(dictionary) + r")[A-Za-z0-9._/-]+\.png")
        reused = {dictionary + value for value in (
            "books/RPD-FIG-books-0001-in-use-missal-on-stand-v3-alpha.png",
            "RPD-FIG-service-objects-0103-paired-cruets-v2-alpha.png",
            "RPD-FIG-service-objects-0106-lavabo-basin-manuterge-v2-alpha.png",
            "RPD-FIG-sacred-vessels-0007-iso-communion-plate.png",
            "compositions/RPD-FIG-prepared-chalice-0001-formation-alpha.png")}
        low_movement_ids = set(range(53, 69)) | {75, 76, 77, 78}
        for leaf in ("01-low-mass", "01-low-mass-trainer-manual", "02-missa-cantata", "03-solemn-mass"):
            with self.subTest(leaf=leaf):
                selected, inputs = artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/" + leaf)
                self.assertTrue(selected)
                self.assertTrue(all(pencil.fullmatch(path) for path in selected))
                self.assertIn(owner + leaf + "/main.tex", inputs)
                self.assertIn(owner + "shared/sanctuary-scenes.tex", inputs)
                low = leaf.startswith("01-")
                self.assertIn(owner + "shared/" + ("low" if low else "sung") + "-mass-diagrams.tex", inputs)
                self.assertNotIn(owner + "shared/" + ("sung" if low else "low") + "-mass-diagrams.tex", inputs)
                self.assertIn(owner + "shared/artwork/pencil/ASG-ART-032-sanctuary-master.png", selected)
                ids = {int(match[1]) for path in selected
                       if (match := re.search(r"/ASG-ART-(\d+)-", path))}
                if low:
                    self.assertEqual({path for path in selected if path.startswith(dictionary)}, reused)
                    self.assertTrue(low_movement_ids <= ids, "every movement and resting-object sprite is needed")
                    self.assertFalse({26, 42, 44, 45, 49} & ids, "superseded action plates must stay out")
                    for name in ("low-mass-movement.tex", "low-mass-objects.tex"):
                        self.assertIn(owner + "shared/" + name, inputs)
                else:
                    self.assertIn(owner + "shared/sung-movement-atlas.tex", inputs)
                    self.assertFalse(low_movement_ids & ids)
                    self.assertFalse(selected & reused)
                    expected_ablutions = {72, 73, 74} if leaf == "02-missa-cantata" else {69, 70, 71}
                    self.assertTrue(expected_ablutions <= ids)
                    self.assertFalse({17, 18, 30} & ids, "superseded sung ablution tableaux must stay out")
                    for name in ("low-mass-movement.tex", "low-mass-objects.tex"):
                        self.assertNotIn(owner + "shared/" + name, inputs)
        for leaf in ("01-low-mass-flash-cards", "02-missa-cantata-cue-cards", "03-solemn-mass-cue-cards"):
            with self.subTest(leaf=leaf):
                self.assertEqual(artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/" + leaf),
                                 (set(), {artwork.HELPER}))
        every = set((ROOT / "src/gpt" / artwork.SERVER / "shared/artwork/pencil").glob("*.png"))
        sung, _ = artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/02-missa-cantata")
        self.assertLess(len(sung), len(every))


class ServerArtworkPathTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/native-print-tests/artwork"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="selector-tests-", dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.server = artwork.SERVER + "/shared/artwork/pencil/"
        self.dictionary = artwork.DICTIONARY + "/shared/artwork/pencil/"

    def image(self, provider, relative):
        path = self.root / "src" / provider / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
        return path

    def test_only_literal_graphics_select_images_from_the_same_provider(self):
        for provider in ("gpt", "claude"):
            with self.subTest(provider=provider):
                paths = [self.image(provider, name) for name in
                         (self.server + "server.png", self.dictionary + "books/missal.png",
                          self.dictionary + "compositions/chalice.png")]
                unrelated = self.image(provider, self.dictionary + "unused.png")
                source = "\n".join(r"\includegraphics[width=2cm]{" + path.relative_to(
                    self.root / "src" / provider).as_posix() + "}" for path in paths)
                source += "\n% " + r"\includegraphics{" + self.dictionary + "unused.png}\n"
                source += self.dictionary + "unused.png"  # A filename mention is not a graphics call.
                selected = artwork._server_graphics(self.root, provider, source)
                self.assertEqual(selected, {path.relative_to(self.root).as_posix() for path in paths})
                self.assertNotIn(unrelated.relative_to(self.root).as_posix(), selected)

    def test_graphics_paths_reject_escape_dynamic_missing_and_symlink_inputs(self):
        target = self.image("gpt", self.server + "valid.png")
        linked = target.with_name("linked.png")
        linked.symlink_to(target)
        directory_link = target.parent / "linked-directory"
        directory_link.symlink_to(target.parent, target_is_directory=True)
        cases = (
            self.server + "../valid.png", self.server + "nested/../../valid.png",
            self.server + "*.png", self.server + "#1.png", self.server + r"\ImageName.png",
            self.server + r"\ImageName{valid}.png",
            self.server + "valid.jpg", self.server + "missing.png",
            self.server + "linked.png", self.server + "linked-directory/valid.png",
            artwork.DICTIONARY + "/research/valid.png", "src/claude/" + self.server + "valid.png",
            str(target),
        )
        for value in cases:
            with self.subTest(value=value), self.assertRaises(artwork.ArtworkError):
                artwork._server_graphics(self.root, "gpt", r"\includegraphics{" + value + "}")


if __name__ == "__main__":
    unittest.main()
