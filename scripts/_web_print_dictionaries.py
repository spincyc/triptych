"""Complete canonical sanctuary-dictionary browser print products.

No generated TeX or tracked source is written. The existing generator decides
admission, edition selection, plate order, object order and artwork ownership.
The browser reflows those plates; it does not inherit old PDF visual approval.
"""
from __future__ import annotations

import hashlib
import html
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import sys
import tomllib

OWNER = Path("src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary")
LEAVES = {"ed-comprehensive": "comprehensive", "ed-altar-server": "altar-server",
          "ed-sacristan": "sacristan", "ed-mc-trainer": "mc-trainer",
          "ed-general-reader": "general-reader", "ed-pontifical": "pontifical-ceremonies"}
MAX_PART_BYTES = 750_000


def source_module(path: Path, name: str):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def clean_tex(text: str) -> str:
    out = []
    for line in text.splitlines():
        for index, char in enumerate(line):
            if char == "%":
                preceding = len(line[:index]) - len(line[:index].rstrip("\\"))
                if not preceding % 2:
                    line = line[:index]
                    break
        out.append(line)
    return "\n".join(out)


def group(text: str, start: int, opening="{", closing="}"):
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] != opening:
        raise ValueError(f"expected {opening} at {text[start:start + 70]!r}")
    depth, index = 1, start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if not depth:
                return text[start + 1:index], index + 1
        index += 1
    raise ValueError("unterminated source group")


def arguments(text: str, index: int, count: int):
    values = []
    for _ in range(count):
        value, index = group(text, index)
        values.append(value)
    return values, index


def calls(text: str, command: str, count: int):
    for match in re.finditer(r"\\" + re.escape(command) + r"(?![A-Za-z@])", text):
        index = match.end()
        while index < len(text) and text[index].isspace():
            index += 1
        while index < len(text) and text[index] == "[":
            _, index = group(text, index, "[", "]")
            while index < len(text) and text[index].isspace():
                index += 1
        if index < len(text) and text[index] == "{":
            args, end = arguments(text, index, count)
            yield args, match.start(), end


def definition(text: str, name: str) -> str:
    found = []
    for match in re.finditer(r"\\(?:newcommand|renewcommand|providecommand)\s*\{\\" + re.escape(name) + r"\}", text):
        index = match.end()
        while index < len(text) and text[index].isspace():
            index += 1
        while index < len(text) and text[index] == "[":
            _, index = group(text, index, "[", "]")
            while index < len(text) and text[index].isspace():
                index += 1
        found.append(group(text, index)[0])
    if len(found) != 1:
        raise ValueError(f"expected one canonical definition {name}; found {len(found)}")
    return found[0]


def digest_paths(root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for value in sorted(set(paths)):
        digest.update(value.encode() + b"\0" + (root / value).read_bytes() + b"\0")
    return digest.hexdigest()


def json_digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class Source:
    def __init__(self, root: Path):
        self.root = root.resolve()
        if str(self.root / "scripts") not in sys.path:
            sys.path.insert(0, str(self.root / "scripts"))
        self.owner = self.root / OWNER
        self.generator = source_module(self.root / "tools/render-sanctuary-dictionary", "_web_print_dictionary_generator")
        validator_module = source_module(self.owner / "shared/schema/validate_inventory.py", "_web_print_dictionary_validator")
        schema_path = self.owner / "shared/schema/inventory-schema.toml"
        selections_path = self.owner / "shared/schema/edition-selections.toml"
        manifest_path = self.owner / "research/artwork-manifest.toml"
        self.schema = tomllib.loads(schema_path.read_text())
        self.selections = tomllib.loads(selections_path.read_text())
        self.manifest = tomllib.loads(manifest_path.read_text())
        record_paths = sorted((self.owner / "shared/objects").rglob("*.toml"))
        validator = validator_module.Validator(self.schema, self.selections)
        validator.validate(record_paths)
        if validator.problems:
            raise ValueError("\n".join(str(p) for p in validator.problems))
        self.records = {key: data for key, (_, data) in validator.records.items()}
        self.record_paths = {key: str(path.relative_to(self.root))
                             for key, (path, _) in validator.records.items()}
        self.alpha_assets = self.generator.canonical_alpha_assets(self.manifest)
        self.art_owners = self.generator.resolve_artwork_render_owners(self.records)
        self.format = clean_tex((self.owner / "shared/dictionary-format.tex").read_text())
        self.renderer = clean_tex((self.owner / "shared/generated-record-renderer.tex").read_text())
        self.preamble = clean_tex((self.root / "src/common/preamble.tex").read_text())
        self.common_paths = [str(p.relative_to(self.root)) for p in record_paths] + [
            str(p.relative_to(self.root)) for p in (schema_path, selections_path, manifest_path,
            self.root / "tools/render-sanctuary-dictionary", self.owner / "shared/schema/validate_inventory.py",
            self.owner / "shared/dictionary-format.tex", self.owner / "shared/generated-record-renderer.tex",
            self.owner / "shared/schema/object-record-api.tex", self.owner / "shared/publication-shell.tex",
            self.root / "src/common/preamble.tex")]
        self.assets = {}
        self.expected_asset_hashes = {}
        for asset in self.manifest.get("asset_files", []):
            expected = asset.get("technical", {}).get("sha256")
            if expected:
                self.expected_asset_hashes[asset["path"]] = expected

    def asset(self, value: str, *, alt: str, caption: str = "") -> tuple[str, dict]:
        value = self.generator.canonical_asset_path(value.strip())
        relative = str(OWNER / value)
        path = self.root / relative
        if not path.is_file() or not path.resolve().is_relative_to(self.owner.resolve()):
            raise ValueError(f"required canonical artwork missing or outside owner: {relative}")
        if relative not in self.assets:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            expected = self.expected_asset_hashes.get(value)
            if expected and digest != expected:
                raise ValueError(f"canonical artwork identity changed: {relative}")
            extension = path.suffix.lower()
            if extension not in {".png", ".jpg", ".jpeg", ".svg"}:
                raise ValueError(f"unsupported source artwork {relative}")
            target = "assets/print-dictionaries/" + digest[:20] + "-" + path.name
            self.assets[relative] = dict(id="asset-" + digest[:20], source=relative, target=target,
                                        href=target, sha256=digest,
                                        mime={".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}[extension])
        entry = self.assets[relative]
        image = '<img data-print-asset="' + entry["id"] + '" src="' + html.escape(entry["href"], quote=True) + '" alt="' + html.escape(alt, quote=True) + '">'
        return '<figure>' + image + ('<figcaption>' + html.escape(caption) + '</figcaption>' if caption else '') + '</figure>', entry

    def canonical(self, edition_id: str):
        editions = [edition for edition in self.selections["editions"] if edition["id"] == edition_id]
        if len(editions) != 1:
            raise ValueError(f"unknown or duplicate canonical edition {edition_id}")
        edition = editions[0]
        chosen = [record for record in self.records.values()
                  if self.generator.alpha_selected(record, edition, self.alpha_assets)
                  and record["id"] not in self.generator.PUBLIC_RENDER_HOLD_IDS]
        chosen.sort(key=lambda record: (record.get("sort_name", record["preferred_english_name"]).casefold(), record["id"]))
        if not chosen:
            raise ValueError("canonical edition selects no admitted records")
        generated = "\n".join(self.generator.dense_edition_tex(chosen, edition, self.art_owners))
        starts = list(re.finditer(r"\\(RSD[A-Za-z]+PlateStart)\b", generated))
        plates = []
        for index, start in enumerate(starts):
            args, body_start = arguments(generated, start.end(), 2)
            end = starts[index + 1].start() if index + 1 < len(starts) else len(generated)
            body = generated[body_start:end]
            objects = []
            calls_in_plate = list(calls(body, "RSDObjectRecord", 3))
            for ordinal, (record_args, begin, _) in enumerate(calls_in_plate):
                finish = calls_in_plate[ordinal + 1][1] if ordinal + 1 < len(calls_in_plate) else len(body)
                last_record = body.rfind(r"\RSDEndObjectRecord", 0, begin)
                prefix = body[last_record + len(r"\RSDEndObjectRecord") if last_record >= 0 else 0:begin]
                hero = bool(re.search(r"\\RSDStory(?:Tall)?HeroNext\b", prefix))
                single = hero or r"\RSDTallCardNext" in prefix
                objects.append(dict(id=record_args[0], block=body[begin:finish], artwork_limit=1 if single else 2,
                                    audience_label="Look for." if hero else "Reader note."))
            plate_id = edition_id + "-" + slug(args[0]) + "-" + args[1]
            end_macro = re.findall(r"\\(RSD[A-Za-z]+PlateEnd)\b", body)
            if len(end_macro) != 1:
                raise ValueError(f"canonical plate {plate_id} has ambiguous end")
            plates.append(dict(id=plate_id, section=args[0], number=args[1],
                               layout_macro=start[1], end_macro=end_macro[0], objects=objects))
        ordered = [obj["id"] for plate in plates for obj in plate["objects"]]
        if len(ordered) != len(set(ordered)) or set(ordered) != {record["id"] for record in chosen}:
            raise ValueError("canonical plate output differs from the independently selected record universe")
        return edition, plates, ordered


class TeXProse:
    """Strict converter for the small canonical title/opening/terminal macros."""
    def __init__(self, source: Source, *, revision: str, required_assets: dict):
        self.source, self.revision, self.required_assets = source, revision, required_assets

    def render(self, text: str) -> str:
        output, index = [], 0
        while index < len(text):
            char = text[index]
            if char == "{":
                body, index = group(text, index)
                output.append(self.render(body))
                continue
            if char != "\\":
                end = text.find("\\", index)
                brace = text.find("{", index)
                end = min(value for value in (end, brace, len(text)) if value >= index)
                chunk = text[index:end]
                chunk = chunk.replace("---", "—").replace("--", "–").replace("~", "\u00a0")
                output.append(re.sub(r"\n\s*\n", "<br><br>\n", html.escape(chunk)))
                index = end
                continue
            token = re.match(r"\\([A-Za-z@]+|.)", text[index:], re.S)
            if not token:
                raise ValueError("unreadable TeX command")
            command = token[1]
            index += token.end()
            if command in {"textbf", "textit", "emph", "texttt", "MakeUppercase"}:
                body, index = group(text, index)
                tag = {"textbf": "strong", "textit": "em", "emph": "em", "texttt": "code", "MakeUppercase": "span"}[command]
                output.append(f"<{tag}" + (' class="source-uppercase"' if command == "MakeUppercase" else '') + ">" + self.render(body) + f"</{tag}>")
            elif command == "href":
                args, index = arguments(text, index, 2)
                output.append('<a href="' + html.escape(args[0], quote=True) + '">' + self.render(args[1]) + '</a>')
            elif command == "DictionaryPlateHeader":
                args, index = arguments(text, index, 3)
                output.append('<header class="plate-heading"><p>' + self.render(args[0]) + '</p><h2>' + self.render(args[1]) + '</h2><p>' + self.render(args[2]) + '</p></header>')
            elif command == "includegraphics":
                while index < len(text) and text[index].isspace(): index += 1
                if text[index:index + 1] == "[": _, index = group(text, index, "[", "]")
                value, index = group(text, index)
                prefix = str(OWNER.relative_to("src/gpt")) + "/"
                if not value.strip().startswith(prefix):
                    raise ValueError(f"unexpected artwork outside dictionary {value}")
                figure, asset = self.source.asset(value.strip()[len(prefix):], alt=Path(value.strip()).stem.replace("-", " "))
                self.required_assets[asset["id"]] = asset
                output.append(figure)
            elif command in {"begin", "end"}:
                environment, index = group(text, index)
                if environment not in {"minipage", "center"}: raise ValueError(f"unsupported source environment {environment}")
                if command == "begin":
                    while index < len(text) and text[index].isspace(): index += 1
                    if text[index:index + 1] == "[": _, index = group(text, index, "[", "]")
                    if environment == "minipage": _, index = group(text, index)
                    output.append('<div class="source-' + environment + '">')
                else:
                    output.append('</div>')
            elif command in {"vspace", "enlargethispage", "thispagestyle"}:
                if text[index:index + 1] == "*": index += 1
                _, index = group(text, index)
            elif command in {"fontsize", "setlength", "rule"}:
                _, index = arguments(text, index, 2)
            elif command == "hrule":
                dimension = re.match(r"\s*(?:height|width|depth)\s+[-.\d]+(?:pt|in|em|ex|cm|mm)", text[index:])
                if dimension: index += dimension.end()
                output.append('<hr>')
            elif command == "AIDisplayDocumentRevisionTimestamp":
                output.append('<p class="revision">Last revised (UTC): ' + html.escape(self.revision) + '</p>')
            elif command in {"par", "clearpage"}:
                output.append('<br>')
            elif command in {"hfill", "vfill", "quad", "enspace", " ", ",", ";"}:
                output.append(' ')
            elif command in {"diamond", "textperiodcentered"}:
                output.append('♦' if command == "diamond" else '·')
            elif command in {"_", "&", "%", "#", "$", "{", "}"}:
                output.append(html.escape(command))
            elif command in {"noindent", "centering", "raggedleft", "raggedright", "large", "Large", "small", "scriptsize", "footnotesize", "itshape", "bfseries", "selectfont", "appendix", "null", "begingroup", "endgroup", "global", "ifTriptychRightsNoticeRendered", "TriptychRightsNoticeRenderedtrue", "else", "fi", "(", ")"}:
                pass
            else:
                raise ValueError(f"unsupported canonical print-prose command \\{command}")
        return "".join(output)


def _visible_claims(record):
    result = {}
    for claim in record["claims"]:
        if claim["evidence_state"] == "editorial-proposal": continue
        kind = claim["kind"]
        if kind in {"identity", "symbolism"}: result[kind] = claim
        elif kind in {"liturgical-use", "ceremonial-presence"}: result["use"] = claim
    return result


def _captions(renderer: str):
    result = {}
    for args, _, _ in calls(renderer, "ifdefstring", 4):
        if args[0].strip() != r"\RSDObjectID": continue
        match = re.search(r"\\bfseries\s+([^}]+)", args[2])
        if match: result.setdefault(args[1], []).append(match[1].strip())
    return result


def _record_html(source, edition, obj, required_assets, reference_rows):
    record = source.records[obj["id"]]
    esc = html.escape
    lines = ['<article class="dictionary-object" id="' + record["id"] + '" data-print-unit="' + record["id"] + '" data-source-record="' + record["id"] + '">',
             '<h3>' + esc(record["preferred_english_name"]) + '</h3><p class="latin">' + esc(record["latin_headword"]) + '</p>']
    artworks = []
    for args, _, _ in calls(obj["block"], "RSDArtwork", 8):
        if args[7] == record["id"] and args[2] not in {art[2] for art in artworks}:
            artworks.append(args)
    artworks = artworks[:obj["artwork_limit"]]
    captions = _captions(source.renderer).get(record["id"], []) if len(artworks) > 1 else []
    lines.append('<div class="object-artwork">')
    for index, args in enumerate(artworks):
        caption = captions[index] if index < len(captions) else ""
        figure, asset = source.asset(args[2], alt=record["preferred_english_name"] + " — " + args[1], caption=caption)
        required_assets[asset["id"]] = asset
        lines.append(figure)
    lines.append('</div>')
    claims = _visible_claims(record)
    if claims.get("identity") or claims.get("use"):
        lines.append('<p class="object-description">' + " ".join(esc(claims[key]["text"]) for key in ("identity", "use") if key in claims) + '</p>')
    notes = [note for note in record.get("audience_note", []) if note["audience"] == edition["audience"]]
    if notes:
        lines.append('<p class="audience-note"><strong>' + obj["audience_label"] + '</strong> ' + esc(notes[-1]["text"]) + '</p>')
    if "symbolism" in claims:
        lines.append('<p class="symbolism"><em>' + esc(claims["symbolism"]["text"]) + '</em></p>')
    # Existing canonical limits accompany the displayed evidence. These are
    # explicitly marked source notes, not silently rewritten print prose.
    qualifications = [claim["text"] for claim in record["claims"] if claim["kind"] in {"variation", "safety", "rights"} and claim["evidence_state"] != "editorial-proposal"]
    qualifications += record.get("handling", {}).get("warnings", [])
    qualifications += ["Scale: " + args[6].replace("-", " ") + "." for args in artworks if args[6] not in {"", "not-applicable"}]
    if qualifications:
        lines.append('<aside class="canonical-qualifications"><strong>Canonical source qualifications.</strong><ul>' + ''.join('<li>' + esc(value) + '</li>' for value in dict.fromkeys(qualifications)) + '</ul></aside>')
    references = []
    for item in record.get("sources", []):
        key = record["id"] + ":" + item["id"]
        source_id = "source-" + hashlib.sha256(key.encode()).hexdigest()[:16]
        reference_rows.append((source_id, record["id"], item))
        references.append('<a href="#' + source_id + '">' + str(len(reference_rows)) + '</a>')
    if references: lines.append('<p class="reference-call">Source notes: ' + ', '.join(references) + '.</p>')
    lines.append('</article>')
    return "\n".join(lines)


def render_dictionary(root, provider, output_id, *, asset_href=None, _source=None):
    """Return one complete print Product; never writes a cache, site or source.

    ``asset_href`` maps an asset's target to the consuming page's URL. The
    ``source``/``target`` pair remains unchanged for the publisher to copy.
    Expected plate and record units come from the canonical owner before any
    HTML is rendered. Reviewed-reader eligibility remains independent.
    """
    from _web_print_common import normalize_html, part_statistics
    from _web_print_dictionary_context import build_context, prove_context

    root = Path(root).resolve()
    if provider != "gpt": raise ValueError("no canonical sanctuary dictionary owner for this provider")
    leaf = str(output_id).removeprefix("publication:").removeprefix("gpt/")
    matches = [key for key, name in LEAVES.items() if leaf == str(OWNER.relative_to("src/gpt") / name) or leaf == name or leaf == key]
    if len(matches) != 1: raise ValueError(f"unknown dictionary print output {output_id}")
    edition_id = matches[0]
    leaf_name = LEAVES[edition_id]
    source = _source or Source(root)
    if source.root != root:
        raise ValueError("dictionary source owner belongs to another repository root")
    edition, plates, ordered = source.canonical(edition_id)
    leaf_dir = source.owner / leaf_name
    main = clean_tex((leaf_dir / "main.tex").read_text())
    metadata = clean_tex((leaf_dir / "generation-metadata.tex").read_text())
    revisions = list(calls(metadata, "AIDocumentRevisionTimestamp", 1))
    if len(revisions) != 1 or not revisions[0][0][0].strip():
        raise ValueError("dictionary publication requires one exact authored revision timestamp")
    revision = revisions[0][0][0]
    title = definition(main, "RSDTitle")
    subtitle = definition(main, "RSDSubtitle")
    edition_line = definition(main, "RSDEditionLine")
    eligibility_path = leaf_dir / "web-edition.toml"
    eligibility = tomllib.loads(eligibility_path.read_text())
    canonical_id = "publication:gpt/" + str(OWNER.relative_to("src/gpt") / leaf_name)
    source_paths = source.common_paths + [str(path.relative_to(root)) for path in (leaf_dir / "main.tex", leaf_dir / "generation-metadata.tex", eligibility_path, leaf_dir / "publication.toml")]
    text_source_digest = digest_paths(root, source_paths)
    expected_units = []
    for index, plate in enumerate(plates):
        expected_units.append(dict(id=plate["id"], source="tools/render-sanctuary-dictionary#" + edition_id + "/" + slug(plate["section"]), occurrence=index + 1))
        expected_units.extend(dict(id=obj["id"], source=source.record_paths[obj["id"]], occurrence=1)
                              for obj in plate["objects"])
    # Independent typed/native expectations precede every rendering function.
    # Fresh output hashes alone cannot establish that source fields survived.
    expected_context = build_context(source, sys.modules[__name__], edition, plates,
                                     main, title, subtitle, edition_line, revision)
    context_sha256 = json_digest(expected_context)
    selection = dict(edition_id=edition_id, selected_record_ids=ordered,
                     plates=[dict(id=p["id"], objects=[o["id"] for o in p["objects"]], layout_macro=p["layout_macro"]) for p in plates],
                     context_sha256=context_sha256)
    selection_digest = json_digest(selection)
    required_assets, reference_rows = {}, []
    tex = TeXProse(source, revision=revision, required_assets=required_assets)
    opening = definition(source.format, "DictionaryTitle")
    opening = opening.replace("#1", title).replace("#2", subtitle).replace("#3", edition_line)
    # Titlepage page anchors and ornaments are presentation controls.
    opening = re.sub(r"\\hypersetup\{[^{}]*\}", "", opening)
    opening = opening.replace(r"\begin{titlepage}", "").replace(r"\end{titlepage}", "")
    title_html = tex.render(opening)
    title_html = title_html.replace('<strong>' + html.escape(title) + '</strong>',
                                    '<h1>' + html.escape(title) + '</h1>', 1)
    body = ['<header class="dictionary-title">' + title_html + '</header>']
    if leaf_name == "comprehensive":
        body.append('<section id="dictionary-opening-witness" class="opening-composition">' + tex.render(definition(main, "RSDOpeningComposition")) + '</section>')
    for plate in plates:
        header = definition(source.renderer, plate["layout_macro"]).split(r"\begin{tabular}", 1)[0]
        header = header.replace("#1", plate["section"]).replace("#2", plate["number"])
        body.append('<section class="dictionary-plate" id="' + plate["id"] + '" data-print-unit="' + plate["id"] + '" data-layout="' + plate["layout_macro"] + '"><header role="heading" aria-level="2" class="canonical-plate-header">' + tex.render(header) + '</header><div class="plate-objects">')
        for obj in plate["objects"]:
            body.append(_record_html(source, edition, obj, required_assets, reference_rows))
        footer = definition(source.renderer, plate["end_macro"])
        # End macros close layout tables before their actual reader footer.
        for expression in (r"\\end\{tabular\}", r"\\end\{minipage\}"):
            footer = re.sub(expression, "", footer)
        body.append('</div><footer class="plate-footer">' + tex.render(footer) + '</footer></section>')
    body.append('<section id="dictionary-reader-appendix" class="reader-appendix">' + tex.render(definition(source.format, "DictionaryTerminalMatter")) + '</section>')
    body.append('<section id="dictionary-source-notes" class="source-notes"><h2>Source notes from the canonical object records</h2><ol>')
    for key, object_id, item in reference_rows:
        body.append('<li id="' + key + '" data-source-object="' + object_id + '"><code>' + html.escape(item["binding"]) + '</code> — ' + html.escape(item["locus"]) + '. ' + html.escape(item.get("note", "")) + '</li>')
    body.append('</ol></section>')
    body.append('<aside id="browser-print-review" class="print-review"><h2>About this browser print</h2><p>This complete source-selected browser rendering is under audit. Browser pagination and plate breaks have not inherited an earlier PDF review.</p></aside>')
    body.append('<footer id="dictionary-rights">' + tex.render(definition(source.preamble, "TriptychRightsNotice")) + '</footer>')
    source_digest = json_digest(dict(text_sources=text_source_digest, artwork=[
        dict(source=asset["source"], sha256=asset["sha256"])
        for asset in sorted(required_assets.values(), key=lambda item: item["source"])]))
    part_id = edition_id + "-complete"
    article = '<article class="dictionary-print" lang="en" data-print-part="' + part_id + '" data-print-document="' + canonical_id + '" data-print-source="' + source_digest + '">\n' + '\n'.join(body) + '\n</article>'
    assets = [dict(asset) for asset in sorted(required_assets.values(), key=lambda asset: asset["id"])]
    if asset_href is not None:
        for asset in assets:
            href = asset_href(asset["target"])
            if not isinstance(href, str) or not href:
                raise ValueError("asset URL mapper returned no usable URL")
            article = article.replace('src="' + html.escape(asset["href"], quote=True) + '"', 'src="' + html.escape(href, quote=True) + '"')
            asset["href"] = href
    article = normalize_html(article)
    prove_context(expected_context, article, assets, asset_href=asset_href)
    if len(article.encode()) >= MAX_PART_BYTES: raise ValueError("dictionary part exceeds 750KB contract")
    statistics = part_statistics(article, part_id=part_id,
                                 selectors=("img", "figcaption", "figure", "h2", "h3", "li"))
    if statistics["units"] != [unit["id"] for unit in expected_units]:
        raise ValueError("rendered record/plate coverage disagrees with canonical owner")
    if len(statistics["expected_ids"]) != len(set(statistics["expected_ids"])):
        raise ValueError("duplicate browser-print DOM identities")
    part = dict(id=part_id, html=article,
                html_sha256=hashlib.sha256(article.encode("utf-8")).hexdigest(),
                selector="[data-print-part='" + part_id + "']", **statistics)
    coverage = dict(status="pass", output_id=canonical_id, source_digest=source_digest, selection_digest=selection_digest,
                    expected_units=expected_units, context_sha256=context_sha256, expected_context=expected_context)
    descriptor = dict(schema="triptych-web-print-document/v1", id=canonical_id, title=title, language="en", print_type="plates",
                      source_digest=source_digest, selection_digest=selection_digest, expected_units=expected_units, coverage_result=coverage,
                      parts=[{key: value for key, value in part.items() if key != "html"}],
                      assets=[{key: asset[key] for key in ("id", "href", "sha256", "mime")} for asset in assets], fonts=[])
    return dict(output_id=canonical_id, print_type="plates", title=title, language="en", source_digest=source_digest, selection_digest=selection_digest,
                expected_units=expected_units, coverage_result=coverage, parts=[part], assets=assets, print_descriptor=descriptor,
                source_paths=sorted(set(source_paths)), selection=selection, reader_eligibility=eligibility["eligibility"],
                print_admission="under-audit", record_count=len(ordered), plate_count=len(plates), reference_count=len(reference_rows))
