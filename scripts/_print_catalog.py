"""Source reading pages from retained text, never from installed PDF bytes.

The browser catalogue admits papal readers; the frozen release binds their
reviewed selections.  ``validate_document`` owns the actual source bounds and
rights checks.  Reading-plan volumes use the whole-text resolver that also
typesets them, rather than the intentionally smaller calendar citation index.
This module returns escaped body fragments for the site's ordinary page shell.
"""
from __future__ import annotations

import hashlib
import html
import json
from functools import lru_cache
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path, PurePosixPath
import re
import tomllib

import _typeset_papal as papal
from _papal_input_receipt import InputRecords


class PrintCatalogError(ValueError):
    """An advertised reader has no current, fully identified source selection."""


def _require(condition, message):
    if not condition:
        raise PrintCatalogError(message)


def _path(root, value):
    _require(isinstance(value, str) and value and "\\" not in value,
             "source path must be repository-relative")
    relative = PurePosixPath(value)
    _require(not relative.is_absolute() and ".." not in relative.parts
             and not any(ord(c) < 32 for c in value), "unsafe source path")
    _require(relative.suffix.lower() != ".pdf", "PDF bytes are not a source input")
    path = root / relative
    _require(path.resolve().is_relative_to(root.resolve()), "source path escapes repository")
    return path


def _canonical(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class _Records:
    """Read and pin each potentially shared release input just once per build."""

    def __init__(self, root):
        self.root, self.payloads, self.documents = root, {}, {}
        self.snapshots = InputRecords(root)

    def read(self, value, pin=None):
        _require(not str(value).startswith("release/papal-documents/inputs/"),
                 "historical snapshots require explicit header/row extraction access")
        path = _path(self.root, value)
        if value not in self.payloads:
            try:
                self.payloads[value] = path.read_bytes()
            except OSError as error:
                raise PrintCatalogError(f"missing source input: {value}") from error
        payload = self.payloads[value]
        if pin is not None:
            _require(hashlib.sha256(payload).hexdigest() == pin.get("sha256"),
                     f"source evidence SHA-256 mismatch: {value}")
            if "bytes" in pin:
                _require(len(payload) == pin["bytes"], f"source evidence size mismatch: {value}")
        return payload

    def json(self, value, pin=None):
        payload = self.read(value, pin)
        if value not in self.documents:
            try:
                self.documents[value] = json.loads(payload)
            except (ValueError, UnicodeError) as error:
                raise PrintCatalogError(f"invalid source JSON: {value}") from error
        return self.documents[value]

    def ref(self, ref):
        return self.json(ref["path"], ref)


def _identity(row):
    return row.get("id"), row.get("language")


def _indexed(rows, label):
    result = {}
    for row in rows:
        key = _identity(row)
        _require(all(isinstance(value, str) and value for value in key)
                 and key not in result, f"duplicate or invalid {label} identity")
        result[key] = row
    return result


def _normalized(row, manifest):
    return {**{key: value for key, value in row.items() if key != "collection_corpus"},
            "revision": row.get("revision", manifest["revision"])}


def _review(records, released):
    """Check retained all-page review evidence without touching its PDF output."""
    review_ref = released["review"]
    _require(review_ref.get("status") == "PASS", "papal reader lacks release PASS evidence")
    audit = records.snapshots.header(review_ref["audit"])
    review = records.snapshots.row(review_ref["audit"], review_ref["audit"]["row_index"])
    _require(_identity(review) == _identity(released) and review.get("status") == "PASS"
             and review.get("pdf_sha256") == released["pdf_sha256"]
             and review.get("pages") == released["pages"], "papal review identity disagrees")
    _require(review_ref.get("original_receipt_sha256") ==
             review.get("receipt_sha256", audit.get("frozen_receipt_sha256"))
             and review_ref.get("current_receipt_sha256") == released["receipt"]["sha256"],
             "papal review receipt binding disagrees")
    pages = released["pages"]

    def page_set(name):
        values = review.get(name)
        _require(isinstance(values, list) and all(type(n) is int and 1 <= n <= pages for n in values)
                 and len(values) == len(set(values)), "invalid papal review page coverage")
        return set(values)

    inspected, reused = page_set("individually_inspected_pages"), page_set("reused_pages")
    _require(not inspected & reused and inspected | reused == set(range(1, pages + 1)),
             "papal PASS review must cover every page")
    reports = review_ref["reports"]
    report = reports[review["report"]]
    records.read(report["path"], report)
    _require(report["sha256"] == review["report_sha256"], "papal review report disagrees")
    proved = []
    for proof in review.get("reuse_proofs", []):
        _require(proof.get("page") in reused and re.fullmatch(r"[a-f0-9]{64}",
                 proof.get("current_raster_sha256", ""))
                 and proof["current_raster_sha256"] == proof.get("prior_raster_sha256")
                 and re.fullmatch(r"[a-f0-9]{64}", proof.get("prior_pdf_sha256", "")),
                 "invalid papal reused-page proof")
        prior = reports[proof["prior_report"]]
        records.read(prior["path"], prior)
        _require(prior["sha256"] == proof["prior_report_sha256"], "papal prior report disagrees")
        proved.append(proof["page"])
    _require(len(proved) == len(set(proved)) and set(proved) == reused,
             "papal reused pages lack exact proofs")


def _current_plan(records, release, wanted):
    plan = records.snapshots.header(release["source_plan"])
    provenance = plan.get("selection_plan", {})
    _require(provenance.get("schema") == "triptych-papal-source-plan/v1",
             "papal release requires a frozen source-selection plan")
    pinned = set()
    for item in provenance["inputs"]:
        records.read(item["path"], item)
        pinned.add(item["sha256"])
    # An added withdrawal must take effect even when the frozen release and
    # all of its old inputs are still byte-identical.  Existing source-plan
    # inputs remain the authority; an unplanned change requires a fresh release.
    folder = records.root / "src/sources/papal-documents"
    for path in sorted(folder.glob("*.json")):
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() in pinned:
            continue
        data = json.loads(payload)
        if data.get("schema") != papal.SCHEMA:
            continue
        for item in data.get("supersessions", []):
            _require(_identity(item.get("prior", {})) not in wanted,
                     "papal reader has a source supersession outside its frozen release")
    return plan, records.snapshots.plan_rows(release["source_plan"])


def _paragraphs(text):
    return "\n".join("<p>" + html.escape(part.strip()) + "</p>"
                     for part in re.split(r"\n\s*\n", str(text)) if part.strip())


def _papal_body(document, reader):
    escape = html.escape
    language = document["language"]
    identification = " · ".join(str(part) for part in
        (document["pope"], document.get("date"),
         document.get("language_label") or papal.LANGUAGES[language]) if part)
    lines = ['<article class="source-reader" lang="' + escape(language, quote=True) + '">',
             '<header><h1>' + escape(document["title"]) + '</h1><p>' +
             escape(identification) + '</p></header>']
    if reader["extent"] == "fragment":
        lines.append('<p class="source-extent">Historical fragment; the source note describes its extent.</p>')
    elif reader["extent"] == "damaged":
        lines.append('<p class="source-extent">Source witness with textual damage; see the source note.</p>')
    lines.append('<div class="source-text">')
    # The source schema only asserts heading/paragraph roles.  In particular
    # do not invent anchors for a damaged note marker or infer signatures and
    # headings from capitalization in historical OCR.
    for block in document["blocks"]:
        tag = "h2" if block["kind"] == "heading" else "p"
        lines.append(f'<{tag}>' + escape(block["text"]) + f'</{tag}>')
    lines.extend(['</div>', '<footer class="source-apparatus"><h2>Source and rights</h2>',
        '<p><a href="' + escape(document["source_url"], quote=True) + '">Source witness</a>' +
        (': ' + escape(reader["witness"]) if reader.get("witness") else '') + '.</p>',
        _paragraphs(document.get("source_note", "Text reproduced from the identified source witness. Its wording and numbering are preserved.")),
        _paragraphs(document.get("rights_notice", document["rights_basis"])),
        '<p>Triptych organization and typesetting: CC BY 4.0. Source text retains its own rights. See LICENSE and THIRD_PARTY.md.</p>',
        '</footer></article>'])
    return "\n".join(lines)


def _papal_pages(root, *, data_root=None, data_source_paths=()):
    records = _Records(root)
    index_path, release_path = "src/web/data/encyclicals/index.json", "release/papal-documents.json"
    generated_index = (Path(data_root) / "encyclicals/index.json") if data_root is not None else root / index_path
    if data_root is not None:
        _require(generated_index.is_file(), "verified browser products omit the declared encyclicals index")
        _require(bool(data_source_paths), "verified browser products require canonical source input declarations")
        for value in data_source_paths:
            _path(root, value)
            _require(not value.startswith(("build/", ".scratch/")),
                     "browser product inputs must name canonical source declarations")
    if not generated_index.exists():
        _require(not (root / "src/sources/papal-documents/encyclicals-index.json").exists(),
                 "declared encyclicals require a verified browser-product data root")
        return {}  # This artifact declares no papal reader admissions.
    index = json.loads(generated_index.read_bytes()) if data_root is not None else records.json(index_path)
    release = records.json(release_path)
    readers = [reader for act in index["encyclicals"] for reader in act["readers"]]
    _require(len(readers) == index["counts"]["readers"], "papal browser reader count disagrees")
    wanted = {(row["release_id"], row["language"]) for row in readers}
    _require(len(wanted) == len(readers), "duplicate papal browser reader")
    plan_header, plan_rows = _current_plan(records, release, wanted)
    current = _indexed(plan_rows, "source plan")
    installed = _indexed(release["documents"], "release")
    pages = {}
    for reader in readers:
        key = reader["release_id"], reader["language"]
        _require(key in installed and key in current, "advertised papal reader is not a current release selection")
        row = installed[key]
        _require(reader["pdf"] == row["pdf"] and reader["pdf_sha256"] == row["pdf_sha256"]
                 and reader["pages"] == row["pages"], "papal browser/release identity disagrees")
        _require(reader["extent"] in {"complete", "fragment", "damaged"}, "unknown papal source extent")
        source = row["source"]
        manifest = records.snapshots.header(row["manifest"])
        frozen = records.snapshots.row(row["manifest"], row["manifest"]["row_index"])
        _require(_canonical(_normalized(frozen, manifest)) == _canonical(source)
                 and _canonical(_normalized(current[key], {"revision": source["revision"]})) == _canonical(source),
                 "papal release source bounds disagree with frozen/current selection")
        receipt = records.snapshots.header(row["receipt"])
        rendered = records.snapshots.row(row["receipt"], row["receipt"]["row_index"])
        _require(_identity(rendered) == key and rendered.get("status") == "compiled"
                 and rendered.get("pdf_sha256") == row["pdf_sha256"]
                 and rendered.get("pages") == row["pages"]
                 and rendered.get("text_fidelity", {}).get("status") == "pass",
                 "papal receipt does not bind a faithful released reader")
        _require(receipt["revision"] == manifest["revision"]
                 and rendered.get("render_revision", receipt["revision"]) == row["render_revision"]
                 and row["render_revision"] == source["revision"], "papal rendering revision disagrees")
        if "input_manifest_sha256" in receipt:
            _require(receipt["input_manifest_sha256"] == row["manifest"]["sha256"],
                     "papal receipt input manifest disagrees")
        for receipt_key, source_key in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"),
                ("segment_id", "segment_id"), ("physical_line_ranges", "physical_line_ranges")):
            _require(rendered.get(receipt_key) == source.get(source_key), "papal receipt source selection disagrees")
        _review(records, row)
        document = papal.validate_document(source, root)
        relative_pdf = PurePosixPath(row["pdf"])
        _require(relative_pdf.parent == PurePosixPath("pdf/papal-documents")
                 and relative_pdf.suffix == ".pdf", "unexpected papal legacy route")
        route = f"papal-documents/{relative_pdf.stem}.html"
        source_paths = {"scripts/_print_catalog.py", "scripts/_typeset_papal.py",
            "src/sources/inventories/papal-documents-rights-v1.toml", "LICENSE", "THIRD_PARTY.md",
            release_path, source["text_path"],
            str(PurePosixPath(source["text_path"]).parent / "artifact.toml"),
            }
        source_paths.update(data_source_paths if data_root is not None else (index_path,))
        source_paths.update(records.snapshots.inputs_for(
            release["source_plan"], row["manifest"], row["receipt"], row["review"]["audit"]))
        source_paths.update(item["path"] for item in row["review"]["reports"].values())
        source_paths.update(item["path"] for item in
            plan_header["selection_plan"]["inputs"])
        if source.get("segment_path"):
            source_paths.add(source["segment_path"])
            source_paths.add(str(PurePosixPath(source["segment_path"]).parents[1] / "edition.toml"))
        else:
            source_paths.add(str(PurePosixPath(source["text_path"]).parents[2] / "edition.toml"))
        _require(route not in pages, "colliding papal HTML routes")
        pages[route] = {"title": document["title"], "html": _papal_body(document, reader),
            "source_paths": sorted(source_paths), "legacy_pdf": row["pdf"],
            "output_id": f'papal:{row["id"]}/{row["language"]}'}
    return pages


@lru_cache(maxsize=1)
def _bible_typesetter():
    path = Path(__file__).resolve().parents[1] / "tools/typeset-bible"
    loader = SourceFileLoader("_print_catalog_typeset_bible", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


def _verse_html(edition, verses, paragraphs):
    """Preserve carrier book/chapter/verse labels and registered paragraph marks."""
    lines, opened, paragraph = [], None, []
    printed = _bible_typesetter().paragraphs_module().PRINTED

    def flush():
        if paragraph:
            lines.append('<p class="bible-paragraph">' + " ".join(paragraph) + '</p>')
            paragraph.clear()

    for token, chapter, verse, text in verses:
        if opened != (token, chapter):
            flush()
            opened = token, chapter
            lines.append('<h4>' + html.escape(f"{edition.name_of(token)} {chapter}") + '</h4>')
        elif (token, chapter, verse) in paragraphs:
            flush()
        mark = '¶ ' if paragraphs.get((token, chapter, verse)) == printed else ''
        paragraph.append('<span class="verse"><sup class="verse-number">' + str(verse) +
                         '</sup> ' + mark + html.escape(text) + '</span>')
    flush()
    return "\n".join(lines)


def _bible_sources(root, module, edition, records=None):
    records = records or _Records(root)
    for book in edition.books:
        artifact_path = book.path.with_name("artifact.toml").relative_to(root).as_posix()
        artifact = tomllib.loads(records.read(artifact_path).decode("utf-8"))
        _require(artifact.get("record_type") == "artifact" and artifact.get("storage") == "tracked"
                 and _path(root, artifact.get("path")) == book.path,
                 "Bible verse file lacks its canonical tracked artifact")
        payload = records.read(artifact["path"])
        _require(hashlib.sha256(payload).hexdigest() == artifact.get("sha256")
                 and len(payload) == artifact.get("byte_size"), "Bible verse artifact SHA-256/size mismatch")
    paths = {"scripts/_print_catalog.py", "tools/typeset-bible", "tools/index-bible",
             "scripts/_bible_editions.py", "scripts/_bible_artifacts.py", "scripts/_psalms.py",
             "scripts/_psalter.py", "scripts/_deuterocanon.py", "scripts/_paragraphs.py",
             "LICENSE", "THIRD_PARTY.md"}
    paths.add((edition.artifacts.parent / "edition.toml").relative_to(root).as_posix())
    for path in edition.artifacts.rglob("*"):
        if path.suffix in {".tsv", ".toml"} and path.is_file():
            paths.add(path.relative_to(root).as_posix())
    # Cross-edition resolution reads the one tracked Douay concordance.
    registered = module.registry()["douay-rheims"]
    douay = root / "src/sources/works" / registered["artifacts"]
    for path in douay.rglob("*"):
        if path.suffix in {".tsv", ".toml"} and path.is_file():
            paths.add(path.relative_to(root).as_posix())
    return paths


def _period_html(volume, period, readings):
    key = str(period["key"])
    _require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key), "unsafe canonical period key")
    lines = ['<section data-volume-id="' + html.escape(volume.id, quote=True) +
             '" data-volume-period="' + key + '" data-volume-digest="' + volume.digest() + '"><h2>' +
             html.escape(str(period.get("label") or key)) + '</h2>', _paragraphs(period.get("summary", ""))]
    for reading in readings:
        lines += [f'<section id="reading-{reading["order"]}"><h3>' +
                  html.escape(f'{reading["order"]}. {reading["title"]}') + '</h3>',
                  '<p class="scripture-reference">' + html.escape(reading["cited"]) +
                  (' — here ' + html.escape(reading["here"]) if reading["here"] else '') + '</p>',
                  _paragraphs(reading["note"])]
        if reading["refused"]:
            lines.append('<aside class="reading-refusal"><p><strong>This edition does not carry this reading.</strong> ' +
                         html.escape(reading["refused"]) + '</p></aside>')
        else:
            _require(reading["verses"], "resolved reading has no canonical verse text")
            lines.append(_verse_html(volume.edition, reading["verses"], volume.paragraphs))
        lines.append('</section>')
    return "\n".join([*lines, '</section>'])


def _volume_intro(volume):
    plan = volume.plan
    lines = [_paragraphs(plan.description(volume.tier))]
    if plan.omissions:
        lines += ['<section><h2>What this plan does not read</h2>', _paragraphs(plan.omissions), '</section>']
    return "\n".join(lines)


def _volume_rights(volume):
    rights = volume.edition.rights
    return "\n".join(['<footer class="source-apparatus"><h2>Edition and rights</h2>',
        '<p>' + html.escape(volume.edition.label) + '. ' +
        html.escape(str(volume.edition.record.get("publication", ""))) + '</p>',
        '<p>' + html.escape(rights["status"] + ' · ' + rights["jurisdiction"]) + '</p>',
        _paragraphs(rights["basis"]),
        '<p>Unmarked paragraph divisions follow the tracked witness projection; ¶ reproduces this edition’s own printed paragraph mark.</p>',
        '<p>The plan, periods, titles and notes are project-created content, CC BY 4.0. Source text retains its own rights.</p>',
        '</footer>'])


def _reading_plan_pages(root):
    plan_root = root / "src/sources/reading-plans"
    if not list(plan_root.glob("*.yaml")):
        return {}  # This artifact declares no canonical reading-plan volumes.
    module = _bible_typesetter()
    pages, records = {}, _Records(root)
    for plan in module.plans(plan_root):
        for tier, name in module.volumes(plan):
            volume = module.Volume(plan, tier, name, root / "src/sources/works")
            title = f"{plan.name}: {plan.track(tier)} ({volume.edition.label})"
            paths = _bible_sources(root, module, volume.edition, records)
            paths.add(plan.path.relative_to(root).as_posix())
            header = '<header><h1>' + html.escape(title) + '</h1></header>'
            intro, rights = _volume_intro(volume), _volume_rights(volume)
            periods = [_period_html(volume, period, readings) for period, readings in volume.periods]
            article = '<article class="source-reader reading-plan" lang="' + html.escape(volume.edition.language) + '">'
            body = "\n".join([article, header, intro, *periods, rights, '</article>'])
            root_route = f"reading-plans/{volume.id}.html"
            page = {"title": title, "html": body, "source_paths": sorted(paths),
                    "legacy_pdf": f"pdf/reading-plans/{volume.id}.pdf",
                    "output_id": "reading-plan:" + volume.id}
            if len(body.encode("utf-8")) > 800_000:
                # A volume over the page budget reads as one page per period,
                # each with the volume's rights; its root keeps the contents.
                links, part_routes = [], []
                for (period, _), content in zip(volume.periods, periods):
                    key = period["key"]
                    part_route = f"reading-plans/{volume.id}/period-{key}.html"
                    part_routes.append(part_route)
                    part_title = f'{period["label"]} — {title}'
                    part_body = "\n".join([article, '<header><h1>' + html.escape(part_title) + '</h1>',
                        '<p><a href="../' + volume.id + '.html">Complete volume contents</a></p></header>',
                        content, rights, '</article>'])
                    _require(len(part_body.encode("utf-8")) < 800_000,
                             f"canonical period exceeds the bounded HTML budget: {part_route}")
                    pages[part_route] = {"title": part_title, "html": part_body, "source_paths": sorted(paths)}
                    links.append('<li><a href="' + volume.id + '/period-' + key + '.html">' +
                                 html.escape(period["label"]) + '</a></li>')
                page.update({"part_routes": part_routes, "html": "\n".join([
                    article, header, intro, '<nav aria-label="Volume sections"><ol>', *links, '</ol></nav>',
                    rights, '</article>'])})
            pages[root_route] = page
    return pages


def source_pages(root, *, data_root=None, data_source_paths=()):
    """Every admitted source reader and issued reading-plan track, or an error.

    No PDF needs to exist.  A missing, changed, withdrawn or unbound source is
    a build failure, never an empty reader or a silently shortened catalogue.
    """
    root = Path(root).resolve()
    return {**_papal_pages(root, data_root=data_root, data_source_paths=data_source_paths), **_reading_plan_pages(root)}


def legacy_pdf_routes(root):
    """Map canonical historic PDF routes to their complete source HTML page."""
    return {page["legacy_pdf"]: route for route, page in source_pages(root).items() if page.get("legacy_pdf")}
