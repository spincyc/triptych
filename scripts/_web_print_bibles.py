"""Complete Bible print products from canonical verse-text source artifacts.

The existing Edition/Book resolver owns native order, addresses, and rights.
Every chunk ends at a complete native chapter. The common print catalogue owns
publication shells, runtime descriptors, assets, and cache serialization.
"""
from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
from itertools import groupby
import json
import re
from pathlib import Path
import tomllib

import _print_catalog as catalog
from _bible_artifacts import select_book_index
from document_schema_checks.source_editions import check_book_index, check_verse_addresses

SCHEMA = "triptych-web-print-document/v1"
PART_BUDGET = 180_000


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode("utf-8")).hexdigest()


def normalized_text(fragment):
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.words = []
        def handle_data(self, data):
            self.words.append(data)
    parser = Text()
    parser.feed(fragment)
    return " ".join("".join(parser.words).split())


class Coverage(HTMLParser):
    """Read emitted coverage independently of the renderer's source iteration."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.units, self.verses = [], [], []
        self.stack = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "data-print-unit" in attrs:
            self.units.append(attrs["data-print-unit"])
        if tag == "span" and attrs.get("class") == "verse":
            need(self.current is None, "nested verse markup")
            self.current = {"key": attrs["data-verse-key"], "label": [], "body": []}

    def handle_endtag(self, tag):
        if tag == "span" and self.current is not None:
            verse = self.current
            self.verses.append((verse["key"], "".join(verse["label"]).strip(),
                                " ".join("".join(verse["body"]).split())))
            self.current = None
        need(self.stack and self.stack[-1][0] == tag, "unbalanced generated HTML")
        self.stack.pop()

    def handle_data(self, data):
        if self.current is not None:
            destination = "label" if any(tag == "sup" for tag, _ in self.stack) else "body"
            self.current[destination].append(data)


def chapter_key(token, number):
    return f"chapter-{token}-{number}"


def chapter_html(book, number, verses, paragraphs):
    """Native addresses, including non-one openings and omitted verse numbers."""
    key = chapter_key(book.token, number)
    lines = [f'<section class="bible-chapter" id="{key}" data-print-unit="{key}">',
             '<h4>' + html.escape(f"{book.name} {number}") + '</h4>']
    pending = []
    def flush():
        if pending:
            lines.append('<p class="bible-paragraph">' + ' '.join(pending) + '</p>')
            pending.clear()
    printed = catalog._bible_typesetter().paragraphs_module().PRINTED
    for verse, text in verses:
        if (book.token, number, verse) in paragraphs:
            flush()
        # The pilcrow has its own element so text fidelity can distinguish the
        # source's printed mark from words in the retained verse payload.
        mark = '¶ ' if paragraphs.get((book.token, number, verse)) == printed else ''
        pending.append(f'<span class="verse" data-verse-key="{book.token}:{number}:{verse}">' +
                       f'<sup class="verse-number">{verse}</sup> ' + mark + html.escape(text) + '</span>')
    flush()
    return '\n'.join([*lines, '</section>'])


def part(identifier, output_id, source_digest, body, *, href=None, selector=None, counts=None):
    fragment = '<section data-print-part="' + identifier + '" data-print-document="' + output_id + \
               '" data-print-source="' + source_digest + '">\n' + body + '\n</section>'
    read = Coverage()
    read.feed(fragment)
    result = {"id": identifier, "html": fragment,
              "expected_ids": read.ids, "units": read.units, "counts": counts or {}}
    result.update({"href": href} if href else {"selector": selector})
    return result


def apparatus(edition, transformations):
    record = edition.record
    fields = [("Edition", record.get("title", edition.edition)), ("Publication", record.get("publication", "")),
              ("Edition date", record.get("date", "")), ("Language", edition.language),
              ("Numbering", edition.numbering), ("Psalter", edition.psalter),
              ("Psalm inscriptions", edition.psalm_titles)]
    lines = ['<h2>Source and rights</h2>']
    for label, value in fields:
        if value:
            lines.append('<p><strong>' + html.escape(label) + '.</strong> ' + html.escape(str(value)) + '</p>')
    revision = record.get("revision") or record.get("revision_timestamp")
    lines.append('<p><strong>Source revision.</strong> ' +
                 (html.escape(str(revision)) if revision else 'Not stated in the identified edition record.') + '</p>')
    if record.get("notes"):
        lines += ['<h3>Edition qualifications</h3>', catalog._paragraphs(record["notes"])]
    lines += ['<h3>Retained extent</h3>',
              '<p>This copy contains every row of the identified canonical verse-text artifacts. The recorded transformations below identify the source printing’s apparatus and headings excluded from those artifacts.</p>']
    for transformation in transformations:
        lines.append(catalog._paragraphs(transformation))
    for label in ("status", "jurisdiction", "basis"):
        lines.append('<p><strong>' + label.title() + '.</strong> ' + html.escape(edition.rights[label]) + '</p>')
    lines += ['<p>Unmarked paragraph divisions follow the tracked witness projection; ¶ reproduces this edition’s own printed paragraph mark.</p>',
              '<p>Triptych organization and typography: CC BY 4.0. Source text retains its own rights. See LICENSE and THIRD_PARTY.md.</p>']
    return '\n'.join(lines)


def _context_event(role, text, offset, *, chapter="", strong=(), scope=()):
    return [role, " ".join(str(text).split()), offset, chapter, list(strong), list(scope)]


def canonical_context(registered, edition, module, counts, source_digest):
    """Derive non-verse obligations from canonical records before rendering."""
    record = edition.record
    title = record.get("title") or registered["edition"]
    metadata = {"id": "bible:" + edition.id, "output_id": "bible:" + edition.id,
                "print_type": "bible", "title": title, "language": registered["language"],
                "source_id": registered["source_id"], "source_digest": source_digest,
                "root_route": f"print/bibles/{edition.id}.html", "counts": dict(counts)}
    events, chapters = [], {}
    def add(role, text, offset=0, **kwargs):
        events.append(_context_event(role, text, offset, **kwargs))
    add("h1", title, scope=("header",))
    add("p", registered["edition"], scope=("header",))
    add("p", f'Complete canonical verse text: {counts["books"]} books, {counts["chapters"]} chapters, {counts["verses"]} verses.', scope=("header",))
    add("p", "Verse-text edition. All verse text retained by the identified source extraction, with its own numbering. That extraction leaves out apparatus and some unnumbered headings; its exact limits appear under Source and rights.",
        strong=("Verse-text edition.",), scope=("header",))
    offset, division = 0, None
    for book in edition.books:
        if division != book.testament:
            division = book.testament
            add("h2.bible-division", module.TESTAMENTS.get(division, division), offset)
        add("h3.bible-book", book.title, offset)
        for number, rows in groupby(book.verses, key=lambda row: row[0]):
            key = chapter_key(book.token, number)
            chapters[key] = {"token": book.token, "number": number}
            add("chapter", key, offset, chapter=key)
            add("h4", f"{book.name} {number}", offset, chapter=key,
                scope=("section.bible-chapter",))
            offset += sum(1 for _ in rows)
    add("h2", "Source and rights", offset)
    fields = [("Edition", record.get("title", registered["edition"])),
              ("Publication", record.get("publication", "")), ("Edition date", record.get("date", "")),
              ("Language", registered["language"]), ("Numbering", registered["numbering"]),
              ("Psalter", registered["psalter"]), ("Psalm inscriptions", registered["psalm_titles"])]
    for label, value in fields:
        if value:
            add("p", f"{label}. {value}", offset, strong=(label + ".",))
    revision = record.get("revision") or record.get("revision_timestamp")
    add("p", "Source revision. " + (str(revision) if revision else "Not stated in the identified edition record."),
        offset, strong=("Source revision.",))
    def paragraphs(value):
        for paragraph in re.split(r"\n\s*\n", str(value)):
            if paragraph.strip():
                add("p", paragraph.strip(), offset)
    if record.get("notes"):
        add("h3", "Edition qualifications", offset)
        paragraphs(record["notes"])
    add("h3", "Retained extent", offset)
    add("p", "This copy contains every row of the identified canonical verse-text artifacts. The recorded transformations below identify the source printing’s apparatus and headings excluded from those artifacts.", offset)
    transformations = []
    for book in edition.books:
        artifact = tomllib.loads(book.path.with_name("artifact.toml").read_text())
        transformation = artifact.get("transformation")
        if transformation and transformation not in transformations:
            transformations.append(transformation)
            paragraphs(transformation)
    for label in ("status", "jurisdiction", "basis"):
        add("p", f"{label.title()}. {edition.rights[label]}", offset, strong=(label.title() + ".",))
    add("p", "Unmarked paragraph divisions follow the tracked witness projection; ¶ reproduces this edition’s own printed paragraph mark.", offset)
    add("p", "Triptych organization and typography: CC BY 4.0. Source text retains its own rights. See LICENSE and THIRD_PARTY.md.", offset)
    return {"metadata": metadata, "events": events, "chapters": chapters}


class ContextCoverage(HTMLParser):
    """Read all non-verse text, semantic roles and positions in the verse stream."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.events, self.units = [], [], []
        self.verse_count, self.outer, self.block, self.strong = 0, None, None, None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        need(tag in {"section", "header", "h1", "h2", "h3", "h4", "p", "strong", "span", "sup"},
             "canonical Bible context has an unexpected element")
        need(not any(key in attrs for key in ("lang", "xml:lang", "href")),
             "canonical Bible context has unexpected link/language metadata")
        if not self.stack:
            need(self.outer is None and tag == "section", "canonical Bible context lacks one part wrapper")
            self.outer = attrs
        elif "data-print-part" in attrs:
            need(False, "canonical Bible context has nested part identity")
        scope = tuple(parent + ("." + data["class"] if data.get("class") else "")
                      for parent, data in self.stack[1:])
        self.stack.append((tag, attrs))
        chapter = next((data.get("id", "") for parent, data in reversed(self.stack)
                        if parent == "section" and data.get("class") == "bible-chapter"), "")
        if tag == "section" and attrs.get("class") == "bible-chapter":
            self.units.append(chapter)
            self.events.append(_context_event("chapter", chapter, self.verse_count,
                                               chapter=chapter, scope=scope))
        if tag in {"h1", "h2", "h3", "h4", "p"} and attrs.get("class") != "bible-paragraph":
            need(self.block is None, "canonical Bible context has nested text blocks")
            self.block = {"tag": tag, "role": tag + ("." + attrs["class"] if attrs.get("class") else ""),
                          "text": [], "strong": [], "offset": self.verse_count,
                          "chapter": chapter, "scope": scope}
        if tag == "span" and attrs.get("class") == "verse":
            need(self.block is None, "canonical Bible context embeds verses inside a notice")
        if tag == "strong":
            need(self.block is not None and self.strong is None,
                 "canonical Bible context has misplaced emphasis")
            self.strong = []

    def handle_data(self, data):
        if self.block is not None:
            self.block["text"].append(data)
            if self.strong is not None:
                self.strong.append(data)
        elif data.strip():
            need(any(tag == "span" and attrs.get("class") == "verse" for tag, attrs in self.stack),
                 "canonical Bible context has unaccounted text")

    def handle_endtag(self, tag):
        need(self.stack and self.stack[-1][0] == tag, "unbalanced canonical Bible context")
        attrs = self.stack[-1][1]
        if tag == "strong":
            self.block["strong"].append(" ".join("".join(self.strong).split()))
            self.strong = None
        if self.block is not None and tag == self.block["tag"]:
            block = self.block
            self.events.append(_context_event(block["role"], "".join(block["text"]), block["offset"],
                chapter=block["chapter"], strong=block["strong"], scope=block["scope"]))
            self.block = None
        if tag == "span" and attrs.get("class") == "verse":
            self.verse_count += 1
        self.stack.pop()


def check_context(expected, parts, metadata):
    need(all(metadata.get(key) == value for key, value in expected["metadata"].items()),
         "canonical Bible context metadata differs from source")
    events, offset = [], 0
    for index, chunk in enumerate(parts):
        read = ContextCoverage()
        read.feed(chunk["html"])
        need(not read.stack, "unclosed canonical Bible context")
        need(read.outer == {"data-print-part": chunk["id"], "data-print-document": metadata["id"],
                            "data-print-source": metadata["source_digest"]},
             "canonical Bible context part wrapper differs from source")
        if index == 0 or index == len(parts) - 1:
            identifier = "bible-introduction" if index == 0 else "bible-apparatus"
            need(chunk["id"] == identifier and chunk.get("selector") == f'[data-print-part="{identifier}"]'
                 and "href" not in chunk and not read.units,
                 "canonical Bible context inline selection differs from source")
        else:
            need(read.units and all(unit in expected["chapters"] for unit in read.units),
                 "canonical Bible context part lacks known chapters")
            first = expected["chapters"][read.units[0]]
            identifier = f'book-{first["token"].lower()}-chapter-{first["number"]}'
            need(chunk["id"] == identifier and "selector" not in chunk
                 and chunk.get("href") == f'{metadata["id"].removeprefix("bible:")}/{identifier}.html'
                 and all(expected["chapters"][unit]["token"] == first["token"] for unit in read.units),
                 "canonical Bible context chunk route differs from source")
        for event in read.events:
            event[2] += offset
            events.append(event)
        offset += read.verse_count
    need(events == expected["events"], "canonical Bible context text, roles or order differ from source")


def check_coverage(expected_units, expected_verses, parts, *, context=None, metadata=None):
    """Expected records come from canonical source rows, not rendered markup."""
    need(len({row["id"] for row in parts}) == len(parts), "duplicate output part identity")
    actual_units, actual_verses = [], []
    for chunk in parts:
        need(len(chunk["html"].encode()) <= 750_000, "HTML part exceeds site budget")
        read = Coverage()
        read.feed(chunk["html"])
        actual_units.extend(read.units)
        actual_verses.extend(read.verses)
    need(actual_units == [unit["id"] for unit in expected_units], "chapter coverage differs from canonical source")
    need(actual_verses == expected_verses, "native verse addresses, labels or wording differ from canonical source")
    if context is not None:
        check_context(context, parts, metadata)
    # Seal bytes only after the complete independently sourced selection passes.
    for chunk in parts:
        chunk["text_sha256"] = sha(normalized_text(chunk["html"]))
        chunk["html_sha256"] = sha(chunk["html"])


def source_paths(root, module, edition):
    """Bind this edition and the shared paragraph projection, without other text.

    The plan resolver also binds a cross-edition concordance corpus. A whole
    native edition does not select that corpus: its only shared textual-input
    dependency is the existing paragraph projection.
    """
    paths = catalog._bible_sources(root, module, edition)
    owner = edition.artifacts.parent.relative_to(root).as_posix() + "/"
    douay = root / "src/sources/works" / module.registry()["douay-rheims"]["artifacts"]
    shared = {
        path.relative_to(root).as_posix()
        for path in douay.glob("paragraph-projection-*/*")
        if path.is_file() and path.suffix in {".tsv", ".toml"}
    }
    paths = {path for path in paths if not path.startswith("src/sources/")
             or path.startswith(owner) or path in shared}
    return paths | {"scripts/_web_print_bibles.py", "scripts/_projection.py",
                    "scripts/document_schema_checks/source_editions.py",
                    "src/common/document-schemas/bible-book-index.schema.json"}


def render_bible(root: Path, edition_id: str, *, part_budget: int = PART_BUDGET) -> dict:
    """Return one complete canonical edition as a typed PrintProduct dict."""
    root = Path(root).resolve()
    need(1_000 <= part_budget <= 750_000, "part budget must leave room below the site HTML limit")
    module = catalog._bible_typesetter()
    registered = module.entry(module.registry(), edition_id)  # Refuses Knox before reading its payload.
    source_root = root / "src/sources/works"
    edition = module.Edition(edition_id, registered, source_root)
    row_schema = json.loads((root / "src/common/document-schemas/bible-book-index.schema.json").read_text())
    check_book_index(select_book_index(edition.artifacts.parent), row_schema)
    selected_paths = source_paths(root, module, edition)
    edition.load()
    for book in edition.books:
        check_verse_addresses(book)
    bible = module.indexer().Bible(edition.artifacts)
    paragraphs = module.paragraphs_module().breaks(edition.artifacts, bible)
    source_files = sorted((name, sha((root / name).read_bytes())) for name in selected_paths
                          if name.startswith("src/sources/") or name in {"LICENSE", "THIRD_PARTY.md"})
    source_digest = sha(canonical({"edition": registered, "files": source_files}))
    sources, expected_units, expected_verses, transformations = {}, [], [], []
    for book in edition.books:
        artifact = tomllib.loads(book.path.with_name("artifact.toml").read_text())
        sources[f"book:{book.token}"] = {"artifact_id": artifact["id"],
            "path": book.path.relative_to(root).as_posix(), "sha256": artifact["sha256"]}
        if artifact.get("transformation") and artifact["transformation"] not in transformations:
            transformations.append(artifact["transformation"])
        for chapter, rows in groupby(book.verses, key=lambda row: row[0]):
            key = chapter_key(book.token, chapter)
            expected_units.append({"id": key, "source": f"book:{book.token}#{chapter}", "occurrence": "1"})
            for _chapter, verse, text in rows:
                mark = '¶ ' if paragraphs.get((book.token, chapter, verse)) == module.paragraphs_module().PRINTED else ''
                expected_verses.append((f"{book.token}:{chapter}:{verse}", str(verse),
                                        ' '.join((mark + text).split())))
    output_id = "bible:" + edition_id
    counts = {"books": len(edition.books), "chapters": len(expected_units), "verses": len(expected_verses)}
    title = edition.record.get("title") or edition.edition
    context = canonical_context(registered, edition, module, counts, source_digest)
    context_digest = sha(canonical(context))
    selection_digest = sha(canonical({"output_id": output_id, "source_digest": source_digest,
        "expected_units": expected_units, "verse_keys": [key for key, _, _ in expected_verses],
        "context_sha256": context_digest}))
    intro = '<header><h1>' + html.escape(title) + '</h1><p>' + html.escape(edition.edition) + '</p>' + \
            '<p>Complete canonical verse text: ' + f'{counts["books"]} books, {counts["chapters"]} chapters, {counts["verses"]} verses.' + '</p>' + \
            '<p><strong>Verse-text edition.</strong> All verse text retained by the identified source extraction, with its own numbering. That extraction leaves out apparatus and some unnumbered headings; its exact limits appear under Source and rights.</p></header>'
    parts = [part("bible-introduction", output_id, source_digest, intro,
                  selector='[data-print-part="bible-introduction"]')]
    division = None
    for book in edition.books:
        prefix = ''
        if division != book.testament:
            division = book.testament
            prefix = '<h2 class="bible-division">' + html.escape(module.TESTAMENTS.get(division, division)) + '</h2>\n'
        prefix += '<h3 class="bible-book">' + html.escape(book.title) + '</h3>\n'
        group, first, group_bytes = [], None, len(prefix.encode())
        for chapter, rows in groupby(book.verses, key=lambda row: row[0]):
            rendered = chapter_html(book, chapter, [(verse, text) for _, verse, text in rows], paragraphs)
            need(len(rendered.encode()) + 500 < part_budget, f"{edition_id} {book.token} {chapter}: chapter exceeds chunk budget")
            if group and group_bytes + len(rendered.encode()) + 500 > part_budget:
                identifier = f"book-{book.token.lower()}-chapter-{first}"
                body = prefix + '\n'.join(group)
                parts.append(part(identifier, output_id, source_digest, body,
                    href=f"{edition_id}/{identifier}.html", counts={".verse": sum(x.count('class="verse"') for x in group),
                    ".bible-chapter": len(group), ".bible-book": 1 if prefix else 0}))
                prefix, group, first, group_bytes = '', [], None, 0
            if first is None:
                first = chapter
            group.append(rendered)
            group_bytes += len(rendered.encode()) + 1
        if group:
            identifier = f"book-{book.token.lower()}-chapter-{first}"
            parts.append(part(identifier, output_id, source_digest, prefix + '\n'.join(group),
                href=f"{edition_id}/{identifier}.html", counts={".verse": sum(x.count('class="verse"') for x in group),
                ".bible-chapter": len(group), ".bible-book": 1 if prefix else 0}))
    parts.append(part("bible-apparatus", output_id, source_digest, apparatus(edition, transformations),
                      selector='[data-print-part="bible-apparatus"]'))
    product = {"schema": SCHEMA, "output_id": output_id, "id": output_id, "print_type": "bible",
        "title": title, "language": edition.language, "source_id": edition.source_id,
        "source_digest": source_digest, "context_sha256": context_digest,
        "selection_digest": selection_digest, "expected_units": expected_units,
        "counts": counts, "parts": parts, "assets": [], "fonts": [],
        "sources": sources, "source_paths": sorted(selected_paths), "root_route": f"print/bibles/{edition_id}.html"}
    check_coverage(expected_units, expected_verses, parts, context=context, metadata=product)
    product["coverage_result"] = {"status": "pass", "output_id": output_id, "source_digest": source_digest,
        "selection_digest": selection_digest, "expected_units": expected_units,
        "context_sha256": context_digest, "context_records": len(context["events"]),
        "counts": counts, "verse_rows_sha256": edition.digest()}
    return product
