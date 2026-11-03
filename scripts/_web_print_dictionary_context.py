"""Independent source-selected semantic proof for sanctuary dictionary print.

This module does not render HTML. It first reads typed object fields and the
finite native prose vocabulary into a plain context model, then compares that
model with a separately parsed DOM. Final output hashes are deliberately outside
this boundary: a fresh hash cannot excuse a missing field.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re


def text(value):
    return " ".join(value.split())


class Node:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def content(self):
        return "".join(child.content() if isinstance(child, Node) else child for child in self.children)

    def elements(self):
        return [child for child in self.children if isinstance(child, Node)]

    def walk(self):
        for child in self.elements():
            yield child
            yield from child.walk()


class DOM(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.stack = [self.root]
        self.feed(value)
        self.close()
        if len(self.stack) != 1:
            raise ValueError("canonical context: unclosed DOM")

    def handle_starttag(self, tag, attrs):
        if len(dict(attrs)) != len(attrs):
            raise ValueError("canonical context: duplicate DOM attribute")
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) == 1 or self.stack[-1].tag != tag:
            raise ValueError("canonical context: unbalanced DOM")
        self.stack.pop()

    def handle_data(self, value):
        self.stack[-1].children.append(value)


def _frame(node):
    descendants = list(node.walk())
    prefix, events = [], []

    def visit(parent):
        for child in parent.children:
            if isinstance(child, str):
                prefix.append(child)
                continue
            kind = "image" if child.tag == "img" else "link" if child.tag == "a" else "heading" if child.tag in {"h1", "h2", "h3"} else "revision" if child.attrs.get("class") == "revision" else None
            if kind:
                events.append(dict(kind=kind, before_text=text("".join(prefix))))
            visit(child)

    visit(node)
    return dict(text=text(node.content()),
                links=[dict(href=n.attrs.get("href"), text=text(n.content())) for n in descendants if n.tag == "a"],
                images=[{key: n.attrs.get(key) for key in ("data-print-asset", "src", "alt")} for n in descendants if n.tag == "img"],
                headings=[dict(level=n.tag, text=text(n.content())) for n in descendants if n.tag in {"h1", "h2", "h3"}],
                revisions=[text(n.content()) for n in descendants if n.attrs.get("class") == "revision"],
                events=events)


class NativeContext:
    """Plain native-prose interpretation, independent of TeXProse/renderers."""
    def __init__(self, source, api, revision):
        self.source, self.api, self.revision = source, api, revision
        self.assets = {}

    def image(self, value, alt):
        # Recompute the source identity without calling Source.asset, which is
        # part of the rendering path under examination.
        value = self.source.generator.canonical_asset_path(value.strip())
        relative = str(self.api.OWNER / value)
        path = self.source.root / relative
        if not path.is_file() or not path.resolve().is_relative_to(self.source.owner.resolve()):
            raise ValueError(f"required canonical artwork missing or outside owner: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = self.source.expected_asset_hashes.get(value)
        if expected and expected != digest:
            raise ValueError(f"canonical artwork identity changed: {relative}")
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}.get(path.suffix.lower())
        if mime is None:
            raise ValueError(f"unsupported source artwork {relative}")
        target = "assets/print-dictionaries/" + digest[:20] + "-" + path.name
        # URLs belong to the consuming route, not the canonical selection.
        asset = dict(id="asset-" + digest[:20], source=relative, target=target,
                     href=target, sha256=digest, mime=mime)
        self.assets[asset["id"]] = asset
        return {"data-print-asset": asset["id"], "src": target, "alt": alt}

    def prose(self, native):
        links, images, headings, revisions = [], [], [], []
        prefix, events = [], []

        def emit(value):
            prefix.append(value)
            return value

        def event(kind):
            events.append(dict(kind=kind, before_text=text("".join(prefix))))

        def read(value):
            out, i = [], 0
            while i < len(value):
                if value[i] == "{":
                    body, i = self.api.group(value, i)
                    out.append(read(body))
                    continue
                if value[i] != "\\":
                    end = i + 1
                    while end < len(value) and value[end] not in "{\\": end += 1
                    out.append(emit(value[i:end].replace("---", "—").replace("--", "–").replace("~", "\u00a0")))
                    i = end
                    continue
                token = re.match(r"\\([A-Za-z@]+|.)", value[i:], re.S)
                if not token: raise ValueError("canonical context: unreadable native prose")
                command, i = token[1], i + token.end()
                if command in {"textbf", "textit", "emph", "texttt", "MakeUppercase"}:
                    body, i = self.api.group(value, i)
                    out.append(read(body))
                elif command == "href":
                    args, i = self.api.arguments(value, i, 2)
                    event("link")
                    label = read(args[1])
                    links.append(dict(href=args[0], text=text(label)))
                    out.append(label)
                elif command == "DictionaryPlateHeader":
                    args, i = self.api.arguments(value, i, 3)
                    first = read(args[0])
                    event("heading")
                    middle, last = read(args[1]), read(args[2])
                    headings.append(dict(level="h2", text=text(middle)))
                    out.append(first + middle + last)
                elif command == "includegraphics":
                    while i < len(value) and value[i].isspace(): i += 1
                    if value[i:i + 1] == "[": _, i = self.api.group(value, i, "[", "]")
                    path, i = self.api.group(value, i)
                    owner_prefix = str(self.api.OWNER.relative_to("src/gpt")) + "/"
                    if not path.strip().startswith(owner_prefix):
                        raise ValueError("canonical context: artwork outside dictionary")
                    event("image")
                    images.append(self.image(path.strip()[len(owner_prefix):], Path(path.strip()).stem.replace("-", " ")))
                elif command in {"begin", "end"}:
                    environment, i = self.api.group(value, i)
                    if environment not in {"minipage", "center", "titlepage", "tabular"}:
                        raise ValueError(f"canonical context: unsupported native environment {environment}")
                    if command == "begin" and environment == "minipage":
                        while i < len(value) and value[i].isspace(): i += 1
                        if value[i:i + 1] == "[": _, i = self.api.group(value, i, "[", "]")
                        _, i = self.api.group(value, i)
                elif command in {"vspace", "enlargethispage", "thispagestyle", "hypersetup"}:
                    if value[i:i + 1] == "*": i += 1
                    _, i = self.api.group(value, i)
                elif command in {"fontsize", "setlength", "rule"}:
                    _, i = self.api.arguments(value, i, 2)
                elif command == "hrule":
                    size = re.match(r"\s*(?:height|width|depth)\s+[-.\d]+(?:pt|in|em|ex|cm|mm)", value[i:])
                    if size: i += size.end()
                elif command == "AIDisplayDocumentRevisionTimestamp":
                    revision = "Last revised (UTC): " + self.revision
                    event("revision")
                    revisions.append(text(revision)); out.append(emit(revision))
                elif command in {"hfill", "vfill", "quad", "enspace", " ", ",", ";"}:
                    out.append(emit(" "))
                elif command in {"diamond", "textperiodcentered"}:
                    out.append(emit("♦" if command == "diamond" else "·"))
                elif command in {"_", "&", "%", "#", "$", "{", "}"}:
                    out.append(emit(command))
                elif command not in {"par", "clearpage", "noindent", "centering", "raggedleft", "raggedright", "large", "Large", "small", "scriptsize", "footnotesize", "itshape", "bfseries", "selectfont", "appendix", "null", "begingroup", "endgroup", "global", "ifTriptychRightsNoticeRendered", "TriptychRightsNoticeRenderedtrue", "else", "fi", "(", ")"}:
                    raise ValueError(f"canonical context: unsupported native command {command}")
            return "".join(out)

        plain = read(native)
        return dict(text=text(plain), links=links, images=images, headings=headings, revisions=revisions, events=events)


def build_context(source, api, edition, plates, main, title, subtitle, edition_line, revision):
    """Build the canonical expectation before any HTML-producing function runs."""
    native = NativeContext(source, api, revision)
    expand = lambda body: body.replace("#1", title).replace("#2", subtitle).replace("#3", edition_line)
    frames = [dict(role="dictionary-title", frame=native.prose(expand(api.definition(source.format, "DictionaryTitle"))))]
    # A native title currently uses bfseries rather than textbf. If its source
    # acquires a heading macro, the independently expected role follows it.
    if edition["id"] == "ed-comprehensive":
        frames.append(dict(role="opening-composition", frame=native.prose(api.definition(main, "RSDOpeningComposition"))))
    captions = {}
    for args, _, _ in api.calls(source.renderer, "ifdefstring", 4):
        if args[0].strip() == r"\RSDObjectID" and r"\bfseries" in args[2]:
            captions.setdefault(args[1], []).append(native.prose(args[2])["text"])
    rows = []
    for plate in plates:
        header = api.definition(source.renderer, plate["layout_macro"]).split(r"\begin{tabular}", 1)[0]
        header = header.replace("#1", plate["section"]).replace("#2", plate["number"])
        footer = api.definition(source.renderer, plate["end_macro"])
        records = []
        for obj in plate["objects"]:
            record = source.records[obj["id"]]
            artwork, seen = [], set()
            for args, _, _ in api.calls(obj["block"], "RSDArtwork", 8):
                if args[7] == record["id"] and args[2] not in seen:
                    seen.add(args[2]); artwork.append(args)
            artwork = artwork[:obj["artwork_limit"]]
            figures = []
            labels = captions.get(record["id"], []) if len(artwork) > 1 else []
            for index, art in enumerate(artwork):
                figures.append(dict(image=native.image(art[2], record["preferred_english_name"] + " — " + art[1]),
                                    caption=labels[index] if index < len(labels) else ""))
            admitted = {}
            for claim in record["claims"]:
                if claim["evidence_state"] == "editorial-proposal": continue
                kind = claim["kind"]
                if kind in {"identity", "symbolism"}: admitted[kind] = claim["text"]
                elif kind in {"liturgical-use", "ceremonial-presence"}: admitted["use"] = claim["text"]
            fields = [dict(role="name", text=text(record["preferred_english_name"])),
                      dict(role="latin", text=text(record["latin_headword"])),
                      dict(role="object-artwork", figures=figures)]
            description = " ".join(admitted[key] for key in ("identity", "use") if key in admitted)
            if description: fields.append(dict(role="object-description", text=text(description)))
            notes = [note["text"] for note in record.get("audience_note", []) if note["audience"] == edition["audience"]]
            if notes: fields.append(dict(role="audience-note", text=text(obj["audience_label"] + " " + notes[-1])))
            if "symbolism" in admitted: fields.append(dict(role="symbolism", text=text(admitted["symbolism"])))
            qualifications = [claim["text"] for claim in record["claims"] if claim["kind"] in {"variation", "safety", "rights"} and claim["evidence_state"] != "editorial-proposal"]
            qualifications += record.get("handling", {}).get("warnings", [])
            qualifications += ["Scale: " + art[6].replace("-", " ") + "." for art in artwork if art[6] not in {"", "not-applicable"}]
            if qualifications:
                fields.append(dict(role="canonical-qualifications", label="Canonical source qualifications.", items=[text(v) for v in dict.fromkeys(qualifications)]))
            links = []
            for item in record.get("sources", []):
                key = "source-" + hashlib.sha256((record["id"] + ":" + item["id"]).encode()).hexdigest()[:16]
                rows.append(dict(id=key, object_id=record["id"], binding=item["binding"], text=text(item["binding"] + " — " + item["locus"] + ". " + item.get("note", ""))))
                links.append(dict(href="#" + key, text=str(len(rows))))
            if links: fields.append(dict(role="reference-call", text="Source notes: " + ", ".join(v["text"] for v in links) + ".", links=links))
            records.append(dict(id=record["id"], fields=fields))
        frames.append(dict(role="dictionary-plate", id=plate["id"], layout=plate["layout_macro"],
                           header=native.prose(header), records=records, footer=native.prose(footer)))
    frames.append(dict(role="reader-appendix", frame=native.prose(api.definition(source.format, "DictionaryTerminalMatter"))))
    frames.append(dict(role="source-notes", heading="Source notes from the canonical object records", rows=rows))
    frames.append(dict(role="print-review", frame=dict(text="About this browser printThis complete source-selected browser rendering is under audit. Browser pagination and plate breaks have not inherited an earlier PDF review.", links=[], images=[], headings=[dict(level="h2", text="About this browser print")], revisions=[], events=[dict(kind="heading", before_text="")])))
    frames.append(dict(role="dictionary-rights", frame=native.prose(api.definition(source.preamble, "TriptychRightsNotice"))))
    return dict(schema="triptych-dictionary-context/v1", frames=frames,
                assets=sorted(native.assets.values(), key=lambda asset: asset["id"]))


def _equal(actual, expected, where):
    if actual != expected:
        raise ValueError(f"canonical context mismatch: {where}")


def _role(node):
    return "name" if node.tag == "h3" else node.attrs.get("class", node.attrs.get("id", node.tag))


def _layout_text(node, where):
    _equal(text("".join(child for child in node.children if isinstance(child, str))), "", where + " detached text")


def prove_context(expected, article, assets, asset_href=None):
    """Refuse incomplete/altered DOM before the caller computes output pins."""
    document = DOM(article).root
    _layout_text(document, "outside publication")
    roots = document.elements()
    _equal(len(roots), 1, "document root")
    root = roots[0]
    _layout_text(root, "document")
    for descendant in (root, *root.walk()):
        if descendant.tag in {"script", "style", "template", "details", "dialog"} or any(
                key in descendant.attrs for key in ("hidden", "inert", "aria-hidden", "style")):
            raise ValueError("canonical context: concealed or unsupported source field")
    actual_frames = root.elements()
    _equal(len(actual_frames), len(expected["frames"]), "ordered publication frames")
    hrefs = {}
    for asset in expected["assets"]:
        href = asset_href(asset["target"]) if asset_href is not None else asset["href"]
        if not isinstance(href, str) or not href: raise ValueError("asset URL mapper returned no usable URL")
        hrefs[asset["id"]] = href
    expected_assets = [dict(asset, href=hrefs[asset["id"]]) for asset in expected["assets"]]
    _equal(assets, expected_assets, "declared canonical artwork inventory")

    def frame(node, model, where):
        adjusted = dict(model, images=[dict(image, src=hrefs[image["data-print-asset"]]) for image in model["images"]])
        _equal(_frame(node), adjusted, where)

    for node, model in zip(actual_frames, expected["frames"]):
        where = model.get("id", model["role"])
        _equal(_role(node), model["role"], where + " role")
        if "frame" in model:
            frame(node, model["frame"], where)
        elif model["role"] == "dictionary-plate":
            _layout_text(node, where)
            _equal({key: node.attrs.get(key) for key in ("id", "data-print-unit", "data-layout")},
                   {"id": model["id"], "data-print-unit": model["id"], "data-layout": model["layout"]}, where + " identity")
            children = node.elements()
            _equal([_role(child) for child in children], ["canonical-plate-header", "plate-objects", "plate-footer"], where + " frame order")
            frame(children[0], model["header"], where + " header")
            frame(children[2], model["footer"], where + " footer")
            objects = children[1].elements()
            _layout_text(children[1], where + " objects")
            _equal(len(objects), len(model["records"]), where + " object count")
            for obj, record in zip(objects, model["records"]):
                rid = record["id"]
                _layout_text(obj, rid)
                _equal((obj.tag, obj.attrs), ("article", {"class": "dictionary-object", "id": rid, "data-print-unit": rid, "data-source-record": rid}), rid + " ownership")
                fields = obj.elements()
                _equal([_role(field) for field in fields], [field["role"] for field in record["fields"]], rid + " ordered fields")
                for field, wanted in zip(fields, record["fields"]):
                    position = rid + "/" + wanted["role"]
                    tag = {"name": "h3", "object-artwork": "div", "canonical-qualifications": "aside"}.get(wanted["role"], "p")
                    _equal((field.tag, field.attrs), (tag, {} if wanted["role"] == "name" else {"class": wanted["role"]}), position + " role attributes")
                    if "figures" in wanted:
                        _layout_text(field, position)
                        figures = field.elements()
                        _equal(len(figures), len(wanted["figures"]), position + " count")
                        for figure, picture in zip(figures, wanted["figures"]):
                            image = dict(picture["image"], src=hrefs[picture["image"]["data-print-asset"]])
                            _equal(figure.tag, "figure", position + " figure")
                            _equal([n.tag for n in figure.elements()], ["img"] + (["figcaption"] if picture["caption"] else []), position + " caption placement")
                            _equal(figure.elements()[0].attrs, image, position + " image ownership/alt")
                            _equal(text(figure.content()), picture["caption"], position + " caption")
                    elif "items" in wanted:
                        _equal([n.tag for n in field.elements()], ["strong", "ul"], position + " structure")
                        _equal(text(field.elements()[0].content()), wanted["label"], position + " label")
                        _equal([(n.tag, text(n.content())) for n in field.elements()[1].elements()], [("li", v) for v in wanted["items"]], position + " items")
                        _equal(text(field.content()), wanted["label"] + "".join(wanted["items"]), position + " full text")
                    else:
                        _equal(text(field.content()), wanted["text"], position + " text")
                        links = [dict(href=n.attrs.get("href"), text=text(n.content())) for n in field.walk() if n.tag == "a"]
                        _equal(links, wanted.get("links", []), position + " reference links")
        else:
            _layout_text(node, where)
            children = node.elements()
            _equal([child.tag for child in children], ["h2", "ol"], where + " apparatus structure")
            _equal(text(children[0].content()), model["heading"], where + " heading")
            rows = children[1].elements()
            _layout_text(children[1], where + " rows")
            _equal(len(rows), len(model["rows"]), where + " rows")
            for row, wanted in zip(rows, model["rows"]):
                _equal((row.tag, row.attrs), ("li", {"id": wanted["id"], "data-source-object": wanted["object_id"]}), where + " source binding/order")
                _equal(text(row.content()), wanted["text"], where + "/" + wanted["id"])
                _equal([(n.tag, text(n.content())) for n in row.elements()], [("code", wanted["binding"])], where + " binding")
