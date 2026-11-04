"""Source-only checks at the existing liturgical data ownership boundaries.

The component and chronology tools own their versioned contracts.  This module
calls their source phases; it never treats the presence of a publication
manifest, a PDF, or a prose research assertion as evidence of their passing.
Server TeX is a small canonical data format: balanced command arguments and
the inventory rows join its identities without interpreting ceremonial prose.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import re
import sys
import tomllib
from collections import Counter
from functools import lru_cache
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[2]
DICTIONARY = Path("src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary")
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


@lru_cache(maxsize=None)
def _module(relative: str):
    path = CODE_ROOT / relative
    name = "_document_schema_" + re.sub(r"\W", "_", relative)
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Source-owned validators may live beneath src/. Importlib's normal
    # execution can read stale bytecode or add __pycache__ to that evidence
    # tree, so execute the exact current source bytes without a bytecode cache.
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def _text(path: Path) -> str:
    # TeX comments cannot supply a missing identity, import or card face.
    text = path.read_text(encoding="utf-8")
    return _module("tools/check-curriculum-structure")._strip_tex_comments(text)


def _calls(text: str, command: str, count: int):
    """Read balanced mandatory arguments; declarations are not invocations."""
    parser = _module("tools/check-curriculum-structure")
    for match in re.finditer(r"\\" + re.escape(command) + r"(?![A-Za-z@])", text):
        index = parser._skip_space(text, match.end())
        while index < len(text) and text[index] == "[":
            _, index = parser._read_group(text, index, "[", "]", command)
            index = parser._skip_space(text, index)
        if index >= len(text) or text[index] != "{":
            continue
        args = []
        for _ in range(count):
            context = command + (f" {args[0]}" if args else "")
            value, index = parser._read_group(text, index, "{", "}", context)
            args.append(value.strip())
        yield args, match.start(), index


def _role_paths(root: Path, record: dict, role: str) -> set[Path]:
    from _document_schema import _structure_paths
    return {path.resolve() for item in record.get("structure", [])
            if item["role"] == role for path in _structure_paths(root, record, item)}


def _bound(root: Path, record: dict, role: str, expected: set[Path]) -> list[str]:
    actual = _role_paths(root, record, role)
    if actual != {path.resolve() for path in expected}:
        return [f"{role} must name the complete canonical source selection"]
    return []


def _proper(root: Path, record: dict) -> list[str]:
    leaf = root / record["source_dir"]
    path = leaf / "proper-components.toml"
    errors = []
    checker = _module("tools/check-proper-components")
    if path.is_file():
        errors.extend(_bound(root, record, "proper-components", {path}))
        checker.audit_manifest(path, root / "src" / record["provider"], phase="content")
        data = checker.parse_manifest(path)
        if data["schema"] == 2:
            # Lane coverage must not become vacuously complete by deleting an
            # element from every manifest array. Existing typed appointment
            # records retain the source universe independently of those arrays.
            appointment_path = leaf / "research/appointed-texts.json"
            if appointment_path.is_file():
                appointed = json.loads(appointment_path.read_text(encoding="utf-8"))
                keys = [item["key"] for item in appointed.get("elements", [])]
                if len(keys) != len(set(keys)) or set(keys) != set(data["element_keys"]):
                    errors.append("component element keys must match the canonical appointed-text inventory exactly")
            chronology_path = leaf / "research/chronology.toml"
            if chronology_path.is_file():
                chronology = tomllib.loads(chronology_path.read_text(encoding="utf-8"))
                missing = {item["key"] for item in chronology.get("elements", [])} - set(data["element_keys"])
                if missing:
                    errors.append("component coverage omits canonical appointed units: " + ", ".join(sorted(missing)))
        if data["schema"] == 1:
            # The historical source contract does not promise unconditional
            # per-mode imports.  Its union still must reach every fragment.
            from _document_schema import _literal_closure
            reached, _ = _literal_closure(root, record)
            for item in data["components"]:
                if (leaf / item["path"]).resolve() not in {p.resolve() for p in reached}:
                    errors.append(f"proper component {item['key']} is detached from the source entrypoints")
    elif record.get("contracts", {}).get("component_schema"):
        errors.append("declared proper component contract has no proper-components.toml")
    # These checks read canonical records and TeX only.  In particular no aux
    # or PDF phase of check-proper-components is called here.
    preflight = _module("tools/check-content-preflight")
    for check in (preflight.check_chronology_record_current,
                  preflight.check_chronology_annotations_current,
                  preflight.check_chronology_claims_supported):
        problems, _detail = check(leaf, root)
        errors.extend(problems)
    return errors


def _dictionary(root: Path, record: dict) -> list[str]:
    leaf = root / record["source_dir"]
    owner = leaf.parent
    schema_path = owner / "shared/schema/inventory-schema.toml"
    selections_path = owner / "shared/schema/edition-selections.toml"
    paths = sorted((owner / "shared/objects").rglob("*.toml"))
    errors = []
    for role, expected in (("dictionary-schema", {schema_path}),
                           ("dictionary-selections", {selections_path}),
                           ("object-records", set(paths))):
        errors.extend(_bound(root, record, role, expected))
    if not paths:
        return errors + ["dictionary has no canonical object records"]
    validator_module = _module(str(DICTIONARY / "shared/schema/validate_inventory.py"))
    schema = tomllib.loads(schema_path.read_text(encoding="utf-8"))
    selections = tomllib.loads(selections_path.read_text(encoding="utf-8"))
    validator = validator_module.Validator(schema, selections)
    validator.validate(paths)
    errors.extend(str(problem) for problem in validator.problems)
    editions = selections.get("editions", [])
    ids = [edition.get("id") for edition in editions]
    expected_id = "ed-" + ("pontifical" if leaf.name == "pontifical-ceremonies" else leaf.name)
    if len(ids) != len(set(ids)):
        errors.append("dictionary edition selections contain duplicate stable IDs")
    matches = [edition for edition in editions if edition.get("id") == expected_id]
    if len(matches) != 1:
        errors.append(f"dictionary must declare exactly one selection for {expected_id}")
    for edition in editions:
        for field in ("explicit_exclusions", "include_object_ids"):
            values = edition.get(field, [])
            if not isinstance(values, list) or len(values) != len(set(values)):
                errors.append(f"dictionary {edition.get('id')}: invalid or duplicate {field}")
                continue
            for value in values:
                if value not in validator.records:
                    errors.append(f"dictionary {edition.get('id')}: {field} names unknown object {value}")
        for field, schema_field in (("include_workflow_states", "workflow_state"),
                                    ("include_statuses", "statuses"),
                                    ("exclude_statuses", "statuses"),
                                    ("include_periods", "periods"),
                                    ("include_categories", "categories")):
            allowed = schema["fields"][schema_field]["values"]
            values = edition.get(field, [])
            if not isinstance(values, list) or len(values) != len(set(values)) or any(v not in allowed for v in values):
                errors.append(f"dictionary {edition.get('id')}: invalid or duplicate {field}")
        if not edition.get("section_order") or len(edition["section_order"]) != len(set(edition["section_order"])):
            errors.append(f"dictionary {edition.get('id')}: missing or duplicate section order")
    if matches and not validator.problems and not validator.selected(matches[0]):
        errors.append(f"dictionary {expected_id} selects no canonical objects")
    parser = _module("tools/check-curriculum-structure")
    generated = parser._control_sequence_definition_body(_text(leaf / record["entrypoint"]), r"\RSDGeneratedFile", leaf)
    if Path(generated).name != expected_id:
        errors.append(f"dictionary entrypoint must consume its {expected_id} selection")
    return errors


def _rows(text: str, identity: str, columns: int) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        values = [value.strip() for value in line.strip().strip("|").split("|")]
        if len(values) == columns and re.fullmatch(identity, values[0]):
            rows.append(values)
    return rows


def _unique(values: list[str], label: str) -> list[str]:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    return [f"{label}: duplicate stable IDs {', '.join(duplicates)}"] if duplicates else []


def _card_ids(text: str, commands: tuple[tuple[str, int], ...], index: int = 0) -> list[str]:
    return [args[index] for command, count in commands for args, _, _ in _calls(text, command, count)]


def _range_ids(value: str) -> set[str]:
    """Expand the manifest's explicit physical-card ranges, never prose claims."""
    result = set()
    for item in value.split(","):
        start, separator, end = item.strip().partition("--")
        if not separator:
            result.add(start)
            continue
        numeric = re.fullmatch(r"(.*?)(\d+)", start)
        finish = re.fullmatch(r"(.*?)(\d+)", end)
        if numeric and finish and numeric[1] == finish[1]:
            result.update(numeric[1] + str(number).zfill(len(numeric[2]))
                          for number in range(int(numeric[2]), int(finish[2]) + 1))
        elif start[:-1] == end[:-1] and start[-1].isalpha() and end[-1].isalpha():
            result.update(start[:-1] + chr(number) for number in range(ord(start[-1]), ord(end[-1]) + 1))
        else:
            raise ValueError(f"unreadable canonical card range {item!r}")
    return result


def _manifest_card_ids(text: str, prefix: str) -> set[str]:
    for line in text.splitlines():
        if line.startswith("| " + prefix):
            field = line.strip().strip("|").split("|", 1)[0].strip()
            return _range_ids(field)
    raise ValueError(f"flash-card manifest has no {prefix} selection")


def _conditional(text: str, states: dict[str, bool]) -> str:
    """Resolve only named source selectors, retaining unknown TeX unchanged."""
    token = re.compile(r"\\if[A-Za-z@]+|\\else(?![A-Za-z@])|\\fi(?![A-Za-z@])")
    stack, chunks, offset = [], [], 0
    active = True
    for match in token.finditer(text):
        if active:
            chunks.append(text[offset:match.start()])
        name = match.group(0)
        if name.startswith(r"\if"):
            known = name in states
            stack.append((active, known, states.get(name, True)))
            active = active and states.get(name, True)
            if not known and active:
                chunks.append(name)
        elif stack:
            parent, known, value = stack[-1]
            if name == r"\else":
                active = parent and (not value if known else True)
                if not known and active:
                    chunks.append(name)
            else:
                stack.pop()
                active = parent
                if not known and active:
                    chunks.append(name)
        elif active:
            chunks.append(name)
        offset = match.end()
    if active:
        chunks.append(text[offset:])
    return "".join(chunks)


def _duplex(text: str, *, low_mass: bool = False) -> list[str]:
    """Check source sheet descriptors, not rendered alignment or PDF parity."""
    environment = "tikzpicture" if low_mass else "flashgrid"
    pattern = re.compile(r"\\begin\{" + environment + r"\}(.*?)\\end\{" + environment + r"\}", re.S)
    grids = []
    for grid in pattern.findall(text):
        if low_mass:
            fronts = [args for args, _, _ in _calls(grid, "LowMassFrontCard", 5)]
            backs = [args for args, _, _ in _calls(grid, "LowMassBackCard", 5)]
        else:
            fronts = [args for command, count in (("integratedresponsefront", 3), ("flashfront", 2))
                      for args, _, _ in _calls(grid, command, count)]
            # Different back renderers share one grid; keep source order.
            backs = [args for _, args in sorted((start, args)
                     for command, count in (("storedresponseback", 2), ("integratedresponseback", 6),
                                             ("denseintegratedresponseback", 6), ("actionflashback", 4))
                     for args, start, _ in _calls(grid, command, count))]
        if fronts or backs:
            grids.append((fronts, backs))
    errors = []
    if not grids or len(grids) % 2:
        return ["card source must contain complete front/back sheet pairs"]
    all_fronts, all_backs = [], []
    for offset in range(0, len(grids), 2):
        front, unexpected_back = grids[offset]
        unexpected_front, back = grids[offset + 1]
        identity_index = 2 if low_mass else 0
        front_ids = [args[identity_index] for args in front]
        back_ids = [args[identity_index] for args in back]
        all_fronts.extend(front_ids)
        all_backs.extend(back_ids)
        mirrored = [item for index in range(0, len(front_ids), 2) for item in front_ids[index:index + 2][::-1]]
        if unexpected_back or unexpected_front or not front or len(front) > (8 if low_mass else 6) or back_ids != mirrored:
            errors.append(f"card sheet {offset // 2 + 1} must pair each front with its row-mirrored back")
        if low_mass and set(front_ids) == set(back_ids):
            by_id = {args[2]: args for args in back}
            for args in front:
                paired = by_id[args[2]]
                if paired[1] != args[1] or paired[3] != args[3] or paired[0] == args[0]:
                    errors.append(f"card {args[2]}: front/back coordinates or stage disagree")
    errors.extend(_unique(all_fronts, "card fronts"))
    errors.extend(_unique(all_backs, "card backs"))
    return errors


def _leaf_reading(root: Path, record: dict, leaf: Path) -> str:
    """The entrypoint as TeX reads the leaf's own sources, comments removed.

    Each literal input of a ``.tex`` file inside the leaf is replaced by that
    file's text, recursively and in reading order, resolved as the literal
    closure resolves it. Inputs outside the leaf (the shared bank and format)
    and computed inputs stay as written: the closure owns those. A source the
    entrypoint does not reach contributes nothing.
    """
    from _document_schema import INPUT_RE
    leaf = leaf.resolve()
    bases = (root / "src" / record["provider"], root / "src")

    def read(path: Path, active: tuple[Path, ...]) -> str:
        def inline(match: re.Match) -> str:
            argument = match.group(1).strip()
            if "\\" in argument or "#" in argument:
                return match.group(0)
            for base in (path.parent,) + bases:
                for candidate in (base / argument, base / f"{argument}.tex"):
                    if candidate.is_file():
                        target = candidate.resolve()
                        if (target.suffix == ".tex" and target.is_relative_to(leaf)
                                and target not in active):
                            return read(target, active + (target,))
                        return match.group(0)
            return match.group(0)
        return INPUT_RE.sub(inline, _text(path))

    entrypoint = (leaf / record["entrypoint"]).resolve()
    return read(entrypoint, (entrypoint,))


def _server(root: Path, record: dict) -> list[str]:
    from _document_schema import _literal_closure
    leaf = root / record["source_dir"]
    owner = leaf.parent
    bank_path = owner / "shared/response-reference.tex"
    bank = _text(bank_path)
    errors = _bound(root, record, "response-inventory", {owner / "research/response-inventory.md"})
    inventory = (owner / "research/response-inventory.md").read_text(encoding="utf-8")
    card_manifest = (owner / "research/flash-card-manifest.md").read_text(encoding="utf-8")
    inventory_rows = _rows(inventory, r"A\d+", 6)
    inventory_ids = [row[0] for row in inventory_rows]
    errors.extend(_unique(inventory_ids, "response inventory"))
    definitions = []
    for command in ("serveranswer", "RegisterServerData"):
        for args, _, _ in _calls(bank, command, 6):
            identity = args[0].split(" --- ", 1)[0]
            if re.fullmatch(r"A\d+", identity):
                definitions.append(identity)
                if any(not value for value in args[1:]):
                    errors.append(f"response {identity} has an empty teaching field")
    errors.extend(_unique(definitions, "response data"))
    if not inventory_ids or set(definitions) != set(inventory_ids):
        errors.append("response data must match the complete canonical inventory IDs")
    for command, count in (("DefineResponseVoice", 4), ("DefineResponseJob", 4), ("DefineResponseCue", 2)):
        entries = [args for args, _, _ in _calls(bank, command, count) if re.fullmatch(r"A\d+", args[0])]
        identities = [args[0] for args in entries]
        errors.extend(_unique(identities, command))
        if set(identities) != set(inventory_ids) or any(not value for args in entries for value in args[1:]):
            errors.append(f"each canonical response requires its complete {command} record")
    reached, _ = _literal_closure(root, record)
    reached = {path.resolve() for path in reached}
    if bank_path.resolve() not in reached:
        errors.append("server entrypoint is detached from the canonical response bank")
    # Every literal response lookup in every selected source must resolve.
    for path in reached:
        if not path.is_relative_to(owner.resolve()) or path.suffix != ".tex":
            continue
        for command in ("ServerLatinData", "ServerLearnerData", "ServerSoundData", "ServerIPAData", "ServerMeaningData"):
            for args, _, _ in _calls(_text(path), command, 1):
                if re.fullmatch(r"A\d+", args[0]) and args[0] not in definitions:
                    errors.append(f"{path.name}: unknown response lookup {args[0]}")
    name = leaf.name
    sung = name.startswith(("02-", "03-"))
    if sung:
        prefix, stem = ("MC", "missa-cantata") if name.startswith("02-") else ("SO", "solemn")
        action_path = owner / f"shared/{stem}-ceremony.tex"
        action_rows = _rows((owner / "research/ceremonial-inventory.md").read_text(encoding="utf-8"), prefix + r"-\d{3}", 11)
        inventory_actions = [row[0] for row in action_rows]
        action_data = [args for args, _, _ in _calls(_text(action_path), "actionrowid", 5)]
        actions = [args[0] for args in action_data]
        errors.extend(_unique(inventory_actions, "ceremonial inventory"))
        errors.extend(_unique(actions, "ceremonial actions"))
        if not inventory_actions or actions != inventory_actions:
            errors.append(f"{prefix} chronological actions must match their ordered canonical inventory")
        if any(not value for args in action_data for value in args):
            errors.append(f"{prefix} canonical actions require all five source fields")
        if record["kind"] == "server-sung" and action_path.resolve() not in reached:
            errors.append("sung guide is detached from its canonical ceremonial route")
        if record["kind"] == "server-sung" and (owner / f"shared/{stem}-role-sheets.tex").resolve() not in reached:
            errors.append("sung guide is detached from its canonical role sheets")
        if record["kind"] == "server-cards":
            cards_path = owner / f"shared/{stem}-action-cards.tex"
            if cards_path.resolve() not in reached:
                errors.append("sung cards are detached from their canonical action selection")
            card_text = _text(cards_path)
            errors.extend(_duplex(card_text))
            selected = set(_card_ids(card_text, (("flashfront", 2),)))
            if selected != _manifest_card_ids(card_manifest, prefix + "-A"):
                errors.append(f"{prefix} action cards must retain every physical-card manifest ID")
            for args, _, _ in _calls(card_text, "actionflashback", 4):
                if not all(args):
                    errors.append(f"action card {args[0]} has an empty paired field")
            for first, last in re.findall(prefix + r"-(\d{3})(?:--(?:" + prefix + r"-)?(\d{3}))?", card_text):
                for number in range(int(first), int(last or first) + 1):
                    if f"{prefix}-{number:03d}" not in inventory_actions:
                        errors.append(f"action card references unknown canonical action {prefix}-{number:03d}")
            states = {r"\ifMissaCantataGuide": prefix == "MC", r"\ifLowMassGuide": False,
                      r"\ifSolemnMassGuide": prefix == "SO", r"\ifCardsOnlyGuide": True,
                      r"\ifResponseDataOnlyGuide": False}
            response_deck = _conditional(bank, states)
            errors.extend(_duplex(response_deck))
            if set(_card_ids(response_deck, (("integratedresponsefront", 3),))) != _manifest_card_ids(card_manifest, "R01"):
                errors.append("response cards must retain every physical-card manifest ID")
    elif record["kind"] == "server-cards":
        # The generated entrypoint inputs the leaf's format.tex and sheets; the
        # deck is what the entrypoint reads of the leaf's own sources.
        deck = _leaf_reading(root, record, leaf)
        errors.extend(_duplex(deck, low_mass=True))
        selected = _rows(card_manifest, r"LM-F\d{2} / \d{2}", 4)
        expected = {row[0].split(" / ")[1]: row for row in selected}
        front_ids = _card_ids(deck, (("LowMassFrontCard", 5),), 2)
        if not expected or set(front_ids) != set(expected):
            errors.append("Low Mass cards must retain every physical-card manifest ID")
        for args, _, _ in _calls(deck, "LowMassBackCard", 5):
            row = expected.get(args[2])
            if row is None:
                continue
            if args[3] != row[1].strip("`"):
                errors.append(f"Low Mass card {args[2]} changes its canonical stage")
            bank_ids = [values[0] for values, _, _ in _calls(args[4], "ServerLatinData", 1)]
            if row[2] != "A14" and bank_ids != [row[2]]:
                errors.append(f"Low Mass card {args[2]} is detached from canonical response {row[2]}")
    else:
        route = owner / "shared/low-mass-ceremony.tex"
        if route.resolve() not in reached:
            errors.append("Low Mass publication is detached from the shared child/trainer route")
    return errors


def _calendar(root: Path, record: dict) -> list[str]:
    """Reconcile counts only where the historical inventory declares them."""
    from _document_schema import _literal_closure
    paths = _role_paths(root, record, "calendar-inventory")
    if not paths:
        return []  # The common required-role check owns this diagnostic.
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    counts = {row[0]: int(row[1]) for row in _rows(text, "|".join(MONTHS), 3) if row[1].isdigit()}
    if not counts:
        return []  # A partial historical inventory declares a different scope.
    reached, _ = _literal_closure(root, record)
    actual = Counter()
    errors = []
    calendar = _module("tools/calendar-spine")
    postconciliar = "/postconciliar/" in record["leaf"]
    held_dates = set()
    for path in sorted(reached):
        if path.suffix != ".tex" or not path.is_relative_to((root / record["source_dir"]).resolve()):
            continue
        source = _text(path)
        if postconciliar:
            if not calendar.TABLE_MONTH.search(source):
                continue
            entries = calendar.parse_table(path.parent, (path.name,))
            for entry in entries:
                key = (entry["month"], entry["day"], entry["discriminator"])
                if key in held_dates:
                    errors.append(f"calendar: duplicate singular fixed-date source row {key}")
                held_dates.add(key)
            continue
        events = [(start, "month", args) for args, start, _ in _calls(source, "calmonth", 1)]
        events += [(start, "entry", args) for args, start, _ in _calls(source, "calentry", 3)]
        month, dates = None, set()
        for _, kind, args in sorted(events):
            if kind == "month":
                month = args[0] if args[0] in MONTHS else None
                dates = set()
            elif month:
                actual[month] += 1
                if args[0] in dates:
                    errors.append(f"calendar {month}: duplicate fixed-date source row {args[0]}")
                dates.add(args[0])
    if postconciliar:
        # This historical table explicitly counts dates, not celebration
        # rows. The owning parser retains discriminators for coequal choices.
        distinct = {(month, day) for month, day, _ in held_dates}
        actual = Counter(MONTHS[month - 1] for month, _ in distinct)
    for month, count in counts.items():
        if actual[month] != count:
            errors.append(f"calendar {month}: {actual[month]} source rows disagree with {count} inventoried rows")
    return errors


def check(root: Path, record: dict) -> list[str]:
    """Return structural defects without reading artifacts or mutating inputs."""
    kind = record.get("kind", "")
    selected = (_proper if kind in {"proper-1962", "proper-postconciliar"} else
                _dictionary if kind == "pictorial-dictionary" else
                _server if kind.startswith("server-") else
                _calendar if kind == "calendar-reference" else None)
    if selected is None:
        return []
    try:
        return selected(Path(root).resolve(), record)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError, ImportError) as error:
        return [f"{kind} source structure: {error}"]
