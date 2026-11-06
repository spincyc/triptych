"""Positive artwork selection for native TeX bundles of illustrated publications.

A Make shared-directory glob is not admission: a bundle carries only the raster
artwork its selected edition typesets. Two canonical owners make that choice
in TeX rather than in a filename list, so it is read from their sources here:

- the Roman sanctuary dictionary, whose generator selects each edition's
  records, plates and per-object artwork;
- the altar-server guides, whose diagram macros reach pencil plates through
  their definition closure under each guide's edition switches.

Nothing here invokes TeX, renders a document or writes a file.
"""
from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
from pathlib import Path
import re
import sys
import tomllib

HELPER = "scripts/_native_print_artwork.py"
DICTIONARY = "liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
DICTIONARY_LEAVES = {"comprehensive": "ed-comprehensive", "altar-server": "ed-altar-server",
                     "sacristan": "ed-sacristan", "mc-trainer": "ed-mc-trainer",
                     "general-reader": "ed-general-reader", "pontifical-ceremonies": "ed-pontifical"}
SERVER = "liturgy/roman-rite/1962/reference/altar-server-guides"
_DIAGRAM_FILES = ("low-mass-diagrams.tex", "sung-mass-diagrams.tex")
# Only these top-level dimensions have two canonical definitions: the first
# branch is the trainer manual's and the second the child booklet's.
_BRANCHED = {"LMSceneXUnit", "LMSceneYUnit", "LMPencilSceneHeight", "LMPencilPairHeight", "LMLavaboHeight"}
_GRAPHICS = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\]\s*)?\{([^{}]*)\}")


class ArtworkError(ValueError):
    pass


def _need(condition, message):
    if not condition:
        raise ArtworkError(message)


def _module(path: Path, name: str):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    sys.modules[name] = module
    # The sanctuary validator lives beneath src/, where importlib's bytecode
    # cache would add an ignored __pycache__ to browser-product inputs (it
    # staled five families on 2026-11-05). Execute the current source bytes
    # without a cache, as document_schema_checks/liturgy.py does.
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


# --- Roman sanctuary dictionary ---------------------------------------------

def _clean(text: str) -> str:
    """Drop unescaped TeX comments line by line."""
    out = []
    for line in text.splitlines():
        for index, char in enumerate(line):
            if char == "%" and not (len(line[:index]) - len(line[:index].rstrip("\\"))) % 2:
                line = line[:index]
                break
        out.append(line)
    return "\n".join(out)


def _group(text: str, start: int, opening="{", closing="}"):
    while start < len(text) and text[start].isspace():
        start += 1
    _need(start < len(text) and text[start] == opening, "expected a canonical TeX group")
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
    raise ArtworkError("unterminated canonical TeX group")


def _arguments(text: str, index: int, count: int):
    values = []
    for _ in range(count):
        value, index = _group(text, index)
        values.append(value)
    return values, index


def _skip_options(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    while index < len(text) and text[index] == "[":
        _, index = _group(text, index, "[", "]")
        while index < len(text) and text[index].isspace():
            index += 1
    return index


def _calls(text: str, command: str, count: int):
    for match in re.finditer(r"\\" + re.escape(command) + r"(?![A-Za-z@])", text):
        index = _skip_options(text, match.end())
        if index < len(text) and text[index] == "{":
            args, end = _arguments(text, index, count)
            yield args, match.start(), end


def _definition(text: str, name: str) -> str:
    found = []
    for match in re.finditer(r"\\(?:newcommand|renewcommand|providecommand)\s*\{\\" + re.escape(name) + r"\}", text):
        found.append(_group(text, _skip_options(text, match.end()))[0])
    _need(len(found) == 1, f"expected one canonical definition of {name}")
    return found[0]


def dictionary_artwork(root: Path, provider: str, canonical: str) -> tuple[set[str], set[str]]:
    """Return one dictionary edition's typeset artwork and the sources choosing it.

    The generator selects records and plates. Within a plate, a hero or tall
    card shows its record's first artwork and every other card its first two
    distinct artworks; fixed matter contributes its literal graphics.
    """
    root = Path(root).resolve()
    _need(provider == "gpt" and canonical.startswith(DICTIONARY + "/"), "no canonical sanctuary dictionary owner")
    leaf = canonical.removeprefix(DICTIONARY + "/")
    _need(leaf in DICTIONARY_LEAVES, "unknown sanctuary dictionary edition: " + canonical)
    owner = root / "src" / provider / DICTIONARY
    generator = _module(root / "tools/render-sanctuary-dictionary", "_native_print_dictionary_generator")
    checker = _module(owner / "shared/schema/validate_inventory.py", "_native_print_dictionary_validator")
    schema_path = owner / "shared/schema/inventory-schema.toml"
    selections_path = owner / "shared/schema/edition-selections.toml"
    manifest_path = owner / "research/artwork-manifest.toml"
    selections = tomllib.loads(selections_path.read_text(encoding="utf-8"))
    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    record_paths = sorted((owner / "shared/objects").rglob("*.toml"))
    validator = checker.Validator(tomllib.loads(schema_path.read_text(encoding="utf-8")), selections)
    validator.validate(record_paths)
    _need(not validator.problems, "\n".join(str(problem) for problem in validator.problems))
    records = {key: data for key, (_, data) in validator.records.items()}
    editions = [row for row in selections["editions"] if row["id"] == DICTIONARY_LEAVES[leaf]]
    _need(len(editions) == 1, "unknown or duplicate canonical dictionary edition")
    edition = editions[0]
    alpha = generator.canonical_alpha_assets(manifest)
    chosen = sorted((record for record in records.values()
                     if generator.alpha_selected(record, edition, alpha)
                     and record["id"] not in generator.PUBLIC_RENDER_HOLD_IDS),
                    key=lambda record: (record.get("sort_name", record["preferred_english_name"]).casefold(), record["id"]))
    _need(bool(chosen), "canonical dictionary edition selects no admitted records")
    generated = "\n".join(generator.dense_edition_tex(chosen, edition, generator.resolve_artwork_render_owners(records)))
    renderer = _clean((owner / "shared/generated-record-renderer.tex").read_text(encoding="utf-8"))
    style = _clean((owner / "shared/dictionary-format.tex").read_text(encoding="utf-8"))
    preamble = _clean((root / "src/common/preamble.tex").read_text(encoding="utf-8"))
    main = _clean((owner / leaf / "main.tex").read_text(encoding="utf-8"))
    values, placed = [], []
    fixed = [_definition(style, "DictionaryTitle"), _definition(style, "DictionaryTerminalMatter"),
             _definition(preamble, "TriptychRightsNotice")]
    if leaf == "comprehensive":
        fixed.append(_definition(main, "RSDOpeningComposition"))
    starts = list(re.finditer(r"\\(RSD[A-Za-z]+PlateStart)\b", generated))
    for index, start in enumerate(starts):
        _, body_start = _arguments(generated, start.end(), 2)
        body = generated[body_start:starts[index + 1].start() if index + 1 < len(starts) else len(generated)]
        ends = re.findall(r"\\(RSD[A-Za-z]+PlateEnd)\b", body)
        _need(len(ends) == 1, "canonical dictionary plate has an ambiguous end")
        fixed += [_definition(renderer, start[1]).split(r"\begin{tabular}", 1)[0], _definition(renderer, ends[0])]
        objects = list(_calls(body, "RSDObjectRecord", 3))
        for ordinal, (record, begin, _) in enumerate(objects):
            finish = objects[ordinal + 1][1] if ordinal + 1 < len(objects) else len(body)
            previous = body.rfind(r"\RSDEndObjectRecord", 0, begin)
            prefix = body[previous + len(r"\RSDEndObjectRecord") if previous >= 0 else 0:begin]
            single = bool(re.search(r"\\RSDStory(?:Tall)?HeroNext\b", prefix)) or r"\RSDTallCardNext" in prefix
            artworks = []
            for args, _, _ in _calls(body[begin:finish], "RSDArtwork", 8):
                if args[7] == record[0] and args[2] not in artworks:
                    artworks.append(args[2])
            values += artworks[:1 if single else 2]
            placed.append(record[0])
    _need(len(placed) == len(set(placed)) and set(placed) == {record["id"] for record in chosen},
          "canonical plates differ from the selected dictionary record universe")
    prefix = DICTIONARY + "/"
    for text in fixed:
        for value in _GRAPHICS.findall(text):
            _need(value.strip().startswith(prefix), "dictionary artwork outside its owner: " + value)
            values.append(value.strip()[len(prefix):])
    expected = {row["path"]: row.get("technical", {}).get("sha256") for row in manifest.get("asset_files", [])}
    selected = set()
    for value in values:
        value = generator.canonical_asset_path(value.strip())
        path = owner / value
        _need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(owner.resolve())
              and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg"},
              "required canonical dictionary artwork is missing or unsupported: " + value)
        _need(not expected.get(value) or hashlib.sha256(path.read_bytes()).hexdigest() == expected[value],
              "canonical dictionary artwork identity changed: " + value)
        selected.add(_relative(root, path))
    inputs = {_relative(root, path) for path in (
        *record_paths, schema_path, selections_path, manifest_path, root / "tools/render-sanctuary-dictionary",
        owner / "shared/schema/validate_inventory.py", owner / "shared/dictionary-format.tex",
        owner / "shared/generated-record-renderer.tex", owner / "shared/schema/object-record-api.tex",
        owner / "shared/publication-shell.tex", root / "src/common/preamble.tex", owner / leaf / "main.tex",
        owner / leaf / "generation-metadata.tex", owner / leaf / "publication.toml")}
    inputs.update(_relative(root, path) for path in generator.source_note_inputs(root, chosen))
    return selected, inputs | {HELPER}


# --- Altar-server guides ------------------------------------------------------

def _web_edition(root: Path):
    return _module(root / "tools/web-edition", "_native_print_web_edition")


def _diagram_definitions(shared: Path, variant: str) -> dict[str, dict]:
    pattern = re.compile(r"\\(?:re)?newcommand\s*\{\\([A-Za-z]+)\}\s*(?:\[\d+\])?\s*(?:\[[^\]]*\])?\s*\{")
    result, alternatives = {}, {}
    for name in _DIAGRAM_FILES:
        text = (shared / name).read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            depth, position = 1, match.end()
            while depth:
                _need(position < len(text), "unterminated canonical diagram definition")
                if text[position] == "%" and text[position - 1] != "\\":
                    position = text.find("\n", position)
                    _need(position >= 0, "unterminated canonical diagram comment")
                    continue
                if text[position] in "{}":
                    escapes, back = 0, position - 1
                    while back >= 0 and text[back] == "\\":
                        escapes, back = escapes + 1, back - 1
                    if not escapes % 2:
                        depth += 1 if text[position] == "{" else -1
                position += 1
            row = {"tex": text[match.start():position], "body": text[match.end():position - 1]}
            alternatives.setdefault(match[1], []).append(row)
            result[match[1]] = row
    for name, options in alternatives.items():
        if len(options) > 1:
            _need(name in _BRANCHED and len(options) == 2, "unhandled duplicate diagram definition: " + name)
            result[name] = options[0 if variant == "trainer" else 1]
    return result


def server_artwork(root: Path, provider: str, canonical: str) -> tuple[set[str], set[str]]:
    """Return one server guide's pencil artwork and the sources choosing it.

    The guide's edition switches select its active text; every diagram macro
    invoked there contributes the pencil plates named in its definition
    closure. Card companions typeset no artwork.
    """
    root = Path(root).resolve()
    _need(provider in {"gpt", "claude"} and canonical.startswith(SERVER + "/"), "no canonical server-guide owner")
    name = canonical.rsplit("/", 1)[-1]
    if name.endswith(("flash-cards", "cue-cards")):
        return set(), {HELPER}
    from document_schema_checks import liturgy
    web = _web_edition(root)
    owner = root / "src" / provider / SERVER
    form = "low" if name.startswith("01-") else "cantata" if name.startswith("02-") else "solemn"
    trainer = "trainer-manual" in name
    states = {r"\ifLowMassGuide": form == "low", r"\ifMissaCantataGuide": form == "cantata",
              r"\ifSolemnMassGuide": form == "solemn", r"\ifCardsOnlyGuide": form == "low",
              r"\ifResponseDataOnlyGuide": form == "low", r"\ifTrainerManualGuide": trainer,
              r"\ifChildBookletGuide": form == "low" and not trainer, r"\ifTriptychRightsNoticeRendered": False}
    inputs = {HELPER, "scripts/document_schema_checks/liturgy.py", "tools/web-edition"}

    def read(path: Path) -> str:
        _need(not path.is_symlink() and path.resolve().is_relative_to(root) and path.is_file(),
              "server-guide source escapes the repository or is missing")
        inputs.add(_relative(root, path))
        return path.read_text(encoding="utf-8")

    def calls(text, command, count):
        return list(liturgy._calls(web.mask_tex_comments(text), command, count))

    main_path = owner / name / "main.tex"
    main = read(main_path)
    definitions, _ = web.command_definitions(read(owner / "shared" / _DIAGRAM_FILES[form != "low"]))
    diagrams = {key for key in definitions if key.startswith("LMScene") or key.endswith("Diagram")}
    used = set()

    def scan(value):
        _, selected = web.command_definitions(liturgy._conditional(web.strip_tex_comments(value), states))
        for args, _, _ in calls(selected, "input", 1):
            source = root / "src" / provider / (args[0] + ("" if args[0].endswith(".tex") else ".tex"))
            text = read(source)
            if not args[0].endswith("sung-mass-diagrams"):
                scan(text)
        used.update(command for command in diagrams
                    if re.search(re.escape("\\" + command) + r"(?![A-Za-z@])", selected))

    if form == "low":
        raw = read(owner / "shared/low-mass-ceremony.tex")
        scenes = sorted((start, end, args) for command in ("BeginLMPage", "BeginLMSingleScenePage", "ContinueLMPairedScene")
                        for args, start, end in calls(raw, command, 3))
        _need(bool(scenes), "Low Mass ceremony has no canonical scenes")
        scan(raw[:scenes[0][0]])
        for index, (start, end, args) in enumerate(scenes):
            if trainer:
                scan(args[2])
            scan(raw[end:scenes[index + 1][0] if index + 1 < len(scenes) else len(raw)])
    else:
        scan(web.split_document(main)[1])
    variant = "trainer" if trainer else "child" if form == "low" else "sung"
    shared = owner / "shared"
    every = _diagram_definitions(shared, "child")
    selected_definitions = _diagram_definitions(shared, variant)
    plate = re.compile(re.escape(SERVER) + r"/shared/artwork/pencil/[A-Za-z0-9._-]+\.png")
    selected = set()
    for macro in sorted(used):
        _need(macro in every and macro not in {"LMSceneXUnit", "LMSceneYUnit"}
              and macro.startswith("LMScene") == (variant != "sung"),
              "selected server diagram has no canonical definition: " + macro)
        closure, queue = set(), [macro]
        while queue:
            item = queue.pop()
            if item in closure:
                continue
            closure.add(item)
            queue.extend(found for found in re.findall(r"\\([A-Za-z]+)", selected_definitions[item]["body"])
                         if found in every and found not in closure)
        for item in closure:
            selected.update("src/" + provider + "/" + value for value in plate.findall(selected_definitions[item]["tex"]))
    for value in selected:
        _need((root / value).is_file(), "selected server artwork is missing: " + value)
    return selected, inputs
