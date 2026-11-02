"""Source-only facts for theological references and nine-day devotions.

These adapters read the existing inventories and literal TeX source graph.
They neither evaluate arbitrary TeX nor certify the scholarship in a dossier.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re

from _corpus import active_tex, _brace_group, expand


KINDS = {
    "novena", "novena-companion", "sacraments", "sacraments-summary",
    "angelology", "virtues", "heresies", "marian-dogma", "marian-apparition",
    "marian-prayer", "marian-rosary", "marian-monograph", "marian-authority",
}
SACRAMENTS = ("baptism", "confirmation", "eucharist", "penance", "anointing", "orders", "matrimony")
DOGMAS = ("divine-motherhood", "perpetual-virginity", "immaculate-conception", "assumption")
# Article extents of the controlling question inventory, common to both editions.
ANGEL_ARTICLES = dict(zip(
    (*range(50, 65), *range(106, 115)),
    (5, 3, 3, 3, 5, 3, 3, 5, 7, 4, 5, 4, 9, 9, 4, 4, 5, 8, 4, 4, 4, 4, 8, 5),
))
INPUT = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")


def _without_definitions(text: str, macros: dict[str, str] | None = None) -> str:
    """An input mentioned in an uncalled macro is not an executed import."""
    pattern = re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?\s*(?:\{\\[A-Za-z@]+\}|\\[A-Za-z@]+)\s*(?:\[[^\]]*\]\s*){0,2}\{|\\(?:[gex]?def)\s*\\[A-Za-z@]+[^{}]*\{")
    cursor = 0
    result = []
    for match in pattern.finditer(text):
        if match.start() < cursor:
            continue
        try:
            body, end = _brace_group(text, match.end() - 1)
        except ValueError:
            continue
        result += [text[cursor:match.start()], "\n" * text[match.start():end].count("\n")]
        if macros is not None and "#" not in body and "#" not in match.group() and not re.search(r"\[[1-9]", match.group()):
            name = re.search(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|[gex]?def)\*?\s*\{?\\([A-Za-z@]+)", match.group())
            if name:
                macros[name.group(1)] = body
        cursor = end
    return "".join(result) + text[cursor:]


def _normal(value: str) -> str:
    return re.sub(r"[^\w]+", " ", value.casefold().replace("_", " ")).strip()


def _plain(value: str) -> str:
    """Remove formatting commands, retaining their textual brace arguments."""
    value = re.sub(r"\\(?:label|ref|pageref|cite|url)\{[^{}]*\}", "", value)
    value = re.sub(r"\\[A-Za-z@]+\*?", " ", value)
    return re.sub(r"[{}~`*]", " ", value).strip()


def commands(text: str, name: str, count: int = 1) -> list[tuple[int, list[str]]]:
    """Balanced literal command arguments; comments do not create commands."""
    text = active_tex(text)
    result = []
    for match in re.finditer(r"\\" + re.escape(name) + r"\*?(?![A-Za-z@])\s*", text):
        cursor = match.end()
        arguments = []
        for _ in range(count):
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if text[cursor:cursor + 1] != "{":
                break
            try:
                argument, cursor = _brace_group(text, cursor)
            except ValueError:
                break
            arguments.append(argument)
        if len(arguments) == count:
            result.append((match.start(), arguments))
    return result


def markdown_tables(text: str) -> list[list[dict[str, str]]]:
    """Read Markdown table records, including escaped pipes in prose cells."""
    tables = []
    lines = text.splitlines()
    index = 0
    while index + 1 < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        header = [_normal(c) for c in re.split(r"(?<!\\)\|", lines[index].strip().strip("|"))]
        separator = re.split(r"(?<!\\)\|", lines[index + 1].strip().strip("|"))
        if len(separator) != len(header) or not all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in separator):
            index += 1
            continue
        index += 2
        rows = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            cells = [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", lines[index].strip().strip("|"))]
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
            else:
                rows.append({"_malformed": lines[index]})
            index += 1
        tables.append(rows)
    return tables


def tex_rows(text: str) -> list[list[str]]:
    """Split alignment rows at top-level TeX separators, preserving cell groups."""
    result, cells, cell = [], [], []
    depth, index = 0, 0
    text = active_tex(text)
    while index < len(text):
        token = text[index:index + 2]
        if token == "\\\\" and depth == 0:
            cells.append("".join(cell).strip())
            result.append(cells)
            cells, cell = [], []
            index += 2
            continue
        character = text[index]
        if character == "\\" and index + 1 < len(text) and text[index + 1] in "{}&%":
            cell.extend(text[index:index + 2])
            index += 2
            continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
        if character == "&" and depth == 0:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(character)
        index += 1
    return result


def table_rows(text: str) -> list[list[str]]:
    """Read alignment bodies independently of any enclosing font-size group."""
    rows = []
    text = active_tex(text)
    for match in re.finditer(r"\\begin\{(longtable|tabularx|tabular)\}", text):
        cursor = match.end()
        for _ in range(2 if match.group(1) == "tabularx" else 1):
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if text[cursor:cursor + 1] == "{":
                _, cursor = _brace_group(text, cursor)
        end = text.find(r"\end{" + match.group(1) + "}", cursor)
        if end >= 0:
            rows.extend(tex_rows(text[cursor:end]))
    return rows


def role_paths(root: Path, record: dict, role: str) -> list[Path]:
    from _document_schema import _structure_paths
    result = []
    for item in record.get("structure", []):
        if item.get("role") == role:
            result.extend(_structure_paths(root, record, item))
    return list(dict.fromkeys(p.resolve() for p in result))


def role_text(root: Path, record: dict, role: str) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in role_paths(root, record, role))


def substantive(text: str) -> bool:
    """A title, comments, or table scaffold alone is not a research record."""
    lines = []
    source_lines = text.splitlines()
    for index, line in enumerate(source_lines):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "%", "<!--")):
            continue
        if re.fullmatch(r"[| :\-]+", stripped):
            continue
        if stripped.startswith("|") and index + 1 < len(source_lines) and re.fullmatch(r"[| :\-]+", source_lines[index + 1].strip()):
            continue
        lines.append(stripped)
    return bool(re.search(r"[A-Za-zÀ-ž]{2}", " ".join(lines)))


def record_rows(root: Path, record: dict, role: str, columns: tuple[str, ...]) -> list[dict[str, str]]:
    result = []
    for table in markdown_tables(role_text(root, record, role)):
        if any(all(c in row for c in columns) for row in table):
            result.extend(table)
    return result


def _resolve(root: Path, record: dict, source: Path, argument: str) -> Path | None:
    if "\\" in argument or "#" in argument or ".." in Path(argument).parts or Path(argument).is_absolute():
        return None
    for base in (source.parent, root / "src" / record["provider"], root / "src"):
        for candidate in (base / argument, base / (argument + ".tex")):
            if candidate.is_file() and candidate.resolve().is_relative_to(root.resolve()):
                return candidate.resolve()
    return None


@dataclass
class SourceView:
    occurrences: list[Path]
    texts: dict[Path, str]

    @property
    def text(self) -> str:
        return "\n".join(self.texts[p] for p in self.occurrences)


def source_view(root: Path, record: dict) -> SourceView:
    """Retain literal import multiplicity, excluding package and shared formatting."""
    occurrences, texts, macros = [], {}, {}

    def visit(source: Path, stack: tuple[Path, ...]) -> None:
        source = source.resolve()
        if source in stack or len(stack) > 40:
            return  # The core source-graph gate reports cycles and unsafe edges.
        text = _without_definitions(active_tex(source.read_text(encoding="utf-8")), macros)
        if not stack and r"\begin{document}" in text:
            text = text.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
        text = expand(text, macros)
        texts[source] = text
        occurrences.append(source)
        for match in INPUT.finditer(text):
            target = _resolve(root, record, source, match.group(1).strip())
            if target is None:
                continue
            relative = target.relative_to(root)
            if relative.parts[:2] == ("src", "common") or target.stem.endswith(("format", "preamble")):
                continue
            visit(target, (*stack, source))

    entry = root / record["source_dir"] / record.get("entrypoint", "main.tex")
    visit(entry, ())
    # Constant appendix macros can be defined in an imported section and used
    # later by its caller. This is the same bounded substitution as _corpus.
    texts = {source: expand(text, macros) for source, text in texts.items()}
    return SourceView(occurrences, texts)


def _once(errors: list[str], paths: list[Path], view: SourceView, label: str) -> None:
    counts = Counter(view.occurrences)
    for source in paths:
        if not source.is_file() or not substantive(active_tex(source.read_text(encoding="utf-8"))):
            errors.append(f"{label}: missing or empty canonical source {source.name}")
        elif counts[source.resolve()] != 1:
            errors.append(f"{label}: {source.name} must be imported exactly once (found {counts[source.resolve()]})")


def _exact_numbers(errors: list[str], values: list[int], expected: set[int], label: str) -> None:
    counts = Counter(values)
    missing = sorted(expected - counts.keys())
    duplicates = sorted(k for k, v in counts.items() if v != 1)
    extra = sorted(counts.keys() - expected)
    if missing or duplicates or extra:
        errors.append(f"{label}: missing={missing}, duplicate={duplicates}, unexpected={extra}")


def _inventory_links(root: Path, record: dict, rows: list[dict], view: SourceView, fields: tuple[str, ...], errors: list[str]) -> None:
    labels = {a[0] for _, a in commands(view.text, "label")}
    base = root / record["source_dir"]
    for row in rows:
        for field in fields:
            value = row.get(field, "")
            for match in re.finditer(r"(?:sections|appendices)/[\w./-]+\.tex", value):
                target = (base / match.group()).resolve()
                if target not in view.texts:
                    errors.append(f"inventory destination is absent from source graph: {match.group()}")
            for match in re.finditer(r"\b(?:sec|app):[\w:-]+", value):
                if match.group() not in labels:
                    errors.append(f"inventory body label does not resolve: {match.group()}")


def _novena(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    from _document_schema import _owner
    owner = _owner(root, record["provider"], record["leaf"]).resolve()
    prayers = sorted((owner / "prayers").glob("day-*.tex"))
    identities = []
    for prayer in prayers:
        match = re.fullmatch(r"day-0?([1-9])-.+", prayer.stem)
        if match:
            identities.append(int(match.group(1)))
    _exact_numbers(errors, identities, set(range(1, 10)), "canonical daily-prayer inventory")
    _once(errors, prayers, view, "daily prayer")
    prayer_texts = []
    for prayer in prayers:
        pairs = commands(prayer.read_text(encoding="utf-8"), "bilingualprayer", 4)
        prayer_texts.extend(tuple(re.sub(r"\s+", " ", v).strip() for v in args[2:]) for _, args in pairs)
    if len(prayer_texts) != len(set(prayer_texts)):
        errors.append("daily proper prayers repeat the same canonical vocal text")
    if record["kind"] == "novena":
        days = [p for p in view.occurrences if p.parent == owner / "days"]
        day_numbers = []
        for day in days:
            headings = commands(view.texts[day], "section")
            match = re.match(r"Day\s+([1-9])\b", headings[0][1][0]) if headings else None
            if match:
                number = int(match.group(1))
                day_numbers.append(number)
                imported = [p for m in INPUT.finditer(view.texts[day])
                            if (p := _resolve(root, record, day, m.group(1))) in prayers]
                if len(imported) != 1 or not imported[0].stem.startswith(f"day-{number:02d}-"):
                    errors.append(f"day {number}: requires its one canonical proper prayer import")
            else:
                errors.append(f"day source has no numbered day identity: {day.name}")
        _exact_numbers(errors, day_numbers, set(range(1, 10)), "nine day imports")
        if len(day_numbers) == 9 and day_numbers != list(range(1, 10)):
            errors.append("nine day imports must follow day order 1–9")
        rows = record_rows(root, record, "prayer-inventory", ("prayer",))
        inventory_days = []
        for row in rows:
            match = re.match(r"Day\s+([1-9])\b", row.get("prayer", ""), re.I)
            if match:
                inventory_days.append(int(match.group(1)))
                if any(not v.strip() for v in row.values()):
                    errors.append(f"prayer inventory day {match.group(1)} has an empty field")
        _exact_numbers(errors, inventory_days, set(range(1, 10)), "prayer-inventory day map")
    else:
        days = [int(a[0]) for _, a in commands(view.text, "recitationday", 2) if a[0].isdigit()]
        _exact_numbers(errors, days, set(range(1, 10)), "companion recitation days")
        if len(days) == 9 and days != list(range(1, 10)):
            errors.append("companion recitation days must follow day order 1–9")
        local_prayers = [p for p in view.occurrences if p.parent.name == "prayers" and not p.is_relative_to(owner)]
        if local_prayers:
            errors.append("novena companion imports independent prayer fragments")


def _sacraments(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    from _document_schema import _owner
    owner = _owner(root, record["provider"], record["leaf"]).resolve()
    summaries = [owner / "summaries" / (name + ".tex") for name in SACRAMENTS]
    _once(errors, summaries, view, "seven sacramental summaries")
    if [p for p in view.occurrences if p.parent == owner / "summaries"] != summaries:
        errors.append("sacramental summaries must contain exactly the seven canonical imports in order")
    for role in ("sacrament-matrix", "sacrament-lexicon"):
        _once(errors, role_paths(root, record, role), view, role)
    if record["kind"] == "sacraments":
        treatments = []
        for name in SACRAMENTS:
            matches = list((owner / "sections").glob(f"*-{name}.tex"))
            if len(matches) != 1:
                errors.append(f"sacramental treatment {name}: requires one canonical section")
            treatments.extend(matches)
        _once(errors, treatments, view, "seven sacramental treatments")
    initiation = role_paths(root, record, "initiation-table")
    _once(errors, initiation, view, "initiation table")
    for source in initiation:
        churches = []
        for row in table_rows(source.read_text(encoding="utf-8")):
            if len(row) == 5 and "Church" in row[1] and r"\textbf" not in row[1]:
                churches.append(_normal(_plain(row[1])))
        if len(churches) != 24 or len(set(churches)) != 24:
            errors.append(f"initiation table must have 24 distinct Church rows (found {len(churches)}, distinct {len(set(churches))})")
    if record["kind"] == "sacraments-summary":
        entry = root / record["source_dir"] / record["entrypoint"]
        text = view.texts[entry.resolve()]
        body = text.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
        allowed = {p.resolve() for role in ("sacrament-matrix", "sacrament-lexicon", "sacrament-summaries", "initiation-table", "generation", "generation-metadata") for p in role_paths(root, record, role)}
        for match in INPUT.finditer(body):
            target = _resolve(root, record, entry, match.group(1))
            if target not in allowed:
                errors.append(f"sacramental companion has an independent content import: {match.group(1)}")
        body = INPUT.sub("", body)
        for start, args in reversed(commands(body, "newcommand", 2)):
            # Hook definitions are typesetting, not an independent prose surface.
            cursor = start
            for _ in range(2):
                cursor = body.find("{", cursor)
                _, cursor = _brace_group(body, cursor)
            body = body[:start] + body[cursor:]
        if re.search(r"[A-Za-zÀ-ž]{2}", _plain(body)):
            errors.append("sacramental companion contains independent prose outside canonical imports")


def _angelology(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    rows = []
    for table in markdown_tables(role_text(root, record, "question-inventory")):
        if any("key" in r and "determination" in r for r in table):
            rows.extend(table)
    pairs, keys = [], []
    for row in rows:
        key = row.get("key", "").strip("` ")
        if not key:
            errors.append("question inventory has a malformed row or missing key")
            continue
        keys.append(key)
        if "question" in row and "article" in row and row["question"].isdigit() and row["article"].isdigit():
            pair = ("I", int(row["question"]), int(row["article"]))
        else:
            match = re.fullmatch(r"(I|III) q\.\s*(\d+) a\.\s*(\d+)", row.get("locus", ""))
            pair = (match.group(1), int(match.group(2)), int(match.group(3))) if match else None
        if pair is None:
            errors.append(f"question inventory key {key}: missing question/article identity")
        else:
            pairs.append(pair)
        fields = ["determination", "grade"]
        fields += [field for field in ("title", "article as posed", "sed contra", "sed contra authority", "body", "body label", "grade basis") if field in row]
        if any(not row.get(field, "").strip() for field in fields):
            errors.append(f"question inventory key {key}: article, determination, grade, authority, and destination fields must be nonempty")
    if len(keys) != len(set(keys)) or len(pairs) != len(set(pairs)):
        errors.append("question inventory duplicates a stable key or Summa article")
    expected = {("I", q, a) for q, maximum in ANGEL_ARTICLES.items() for a in range(1, maximum + 1)}
    missing = sorted(expected - set(pairs))
    if missing:
        errors.append("question inventory missing mandatory Summa articles: " + ", ".join(f"{p} {q}.{a}" for p, q, a in missing))
    _inventory_links(root, record, rows, view, ("body", "body label"), errors)
    hierarchy = [p for p in view.occurrences if "celestial-hierarchy" in p.stem]
    if len(hierarchy) != 1:
        errors.append("Celestial Hierarchy requires one canonical exposition source")
    else:
        text = view.texts[hierarchy[0]]
        chapters = commands(text, "chchapter", 4)
        if chapters:
            identities = [int(a[3].removeprefix("sec:ch")) for _, a in chapters if re.fullmatch(r"sec:ch\d+", a[3])]
        else:
            roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")
            identities = [roman.index(m.group(1)) + 1 for _, a in commands(text, "subsection") if (m := re.match(r"([IVX]+):", a[0])) and m.group(1) in roman]
        if identities != list(range(1, 16)):
            errors.append(f"Celestial Hierarchy requires chapters 1–15 once in order (found {identities})")
    census = [p for p in view.occurrences if "article-census" in p.stem]
    if len(census) != 1:
        errors.append("angelology requires one article-census projection")
    else:
        actual = []
        text = view.texts[census[0]]
        boundaries = list(re.finditer(r"\\(?:subsection|paragraph)\{(Question\s+(\d+)|(?P<part>I|III) q\.~?(?P<question>\d+)[^{}]*)\}", text))
        for index, match in enumerate(boundaries):
            part = match.group("part") or "I"
            question = int(match.group(2) or match.group("question"))
            end = boundaries[index + 1].start() if index + 1 < len(boundaries) else len(text)
            for row in table_rows(text[match.end():end]):
                number = re.search(r"(?:\\textbf\{)(\d+)\.?(?:\})", row[0]) or re.search(r"(?:^|\n)\s*(\d+)\s*$", row[0])
                if len(row) in (3, 5) and number:
                    actual.append((part, question, int(number.group(1))))
        if Counter(actual) != Counter(pairs):
            errors.append("article census does not project the question inventory exactly once per article")


def _virtues(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    rows, counted = [], []
    for table in markdown_tables(role_text(root, record, "virtue-inventory")):
        candidates = [r for r in table if "sort" in r and "stable key" in r]
        rows.extend(candidates)
        counted.extend(r for r in candidates if "preferred term and source term" in r)
    keys = [r["stable key"].strip("` ") for r in rows]
    sorts = [r["sort"] for r in rows]
    if not keys:
        errors.append("virtue inventory has no canonical stable-key rows")
    if len(keys) != len(set(keys)) or len(sorts) != len(set(sorts)):
        errors.append("virtue inventory duplicates a stable key or sort key")
    for row in counted:
        for field in ("class and provenance", "formal object characteristic act", "exact primary loci", "opposition"):
            if not row.get(field, "").strip():
                errors.append(f"virtue {row['stable key']}: missing {field}")
    census = [p for p in view.occurrences if "synoptic-table" in p.stem]
    if counted and len(census) == 1:
        text = view.texts[census[0]].split(r"\subsection{Qualified", 1)[0]
        projected = [r for r in table_rows(text) if len(r) == 5 and not any(r"\textbf" in c for c in r) and r"\begin" not in r[0]]
        if len(projected) != len(counted):
            errors.append(f"virtue census row count disagrees with counted inventory ({len(projected)} vs {len(counted)})")
        for canonical, row in zip(counted, projected):
            # The inventory explicitly permits alternative names with "or";
            # source-language parentheticals are not additional English rows.
            preferred = _normal(_plain(canonical["preferred term and source term"].split("(", 1)[0]))
            names = preferred.split(" or ")
            if _normal(_plain(row[2])) not in names + [preferred]:
                errors.append(f"virtue census label/order disagrees with stable key {canonical['stable key']}: {row[2]}")
    elif counted:
        errors.append("virtues require one canonical census projection")


def _dogmas(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    owner = root / record["source_dir"]
    for dogma in DOGMAS:
        paths = list((owner / "sections").glob(f"*-{dogma}.tex"))
        if len(paths) != 1:
            errors.append(f"Marian dogma {dogma}: requires one canonical treatment")
        _once(errors, paths, view, "four Marian dogmas")
    synopses = [p for p in view.occurrences if "synops" in p.stem]
    if len(synopses) != 1:
        errors.append("Marian dogmas require one canonical synopsis source")
        return
    text = view.texts[synopses[0]]
    headings = [a[0] for _, a in commands(text, "subsection")]
    if not headings:
        headings = [a[1] for _, a in commands(text, "begin", 2) if a[0] == "dogmasynopsis"]
    values = []
    for heading in headings:
        normalized = _normal(_plain(heading))
        for index, dogma in enumerate(DOGMAS):
            if dogma.replace("-", " ") in normalized:
                values.append(index)
    _exact_numbers(errors, values, set(range(4)), "four dogma synopses")


def _apparitions(root: Path, record: dict, errors: list[str]) -> None:
    text = role_text(root, record, "corpus-status")
    tables = markdown_tables(text)
    inventories = []
    for table in tables:
        records = [r for r in table if set(r) & {"event", "experience", "tradition", "case", "corpus element"} or {"authority", "act", "object"} <= r.keys()]
        if not records:
            continue
        inventories.extend(records)
        identities = []
        for row in records:
            identity = next((row[c] for c in ("event", "experience", "tradition", "case", "corpus element") if c in row), row.get("date", "") + " " + row.get("act", ""))
            identities.append(_normal(identity))
            if any(not value.strip() for value in row.values()):
                errors.append(f"apparition corpus item {identity}: empty status/dossier field")
            if not set(row) & {"competent act or reception", "ddf approval and local promulgation", "ecclesial reception", "current controlling status", "source or competent act", "source competent act", "controlling status used in the appendix", "status", "act"}:
                errors.append(f"apparition corpus item {identity}: no competent-act or status field")
        if len(identities) != len(set(identities)):
            errors.append("apparition corpus repeats an identity within one disposition table")
    # Single-event editions also use named prose fields, a profile-authorized
    # inventory form. Preserve their historical regime rather than recoding it.
    fields = {_normal(m.group(1)): m.group(2).strip() for m in re.finditer(
        r"(?ms)^\s*-\s*\*\*(.+?):\*\*(.*?)(?=^\s*-\s*\*\*|^##|\Z)", text)}
    if "stable identity" in fields or re.search(r"(?m)^## Event dossier\b", text):
        for label, pattern in (("stable identity", r"stable identity"), ("jurisdiction", r"jurisdiction"), ("authority/act", r"authority.*act"), ("object judged", r"exact object judged"), ("current status", r"current controlling status")):
            if not any(re.search(pattern, key) and value for key, value in fields.items()):
                errors.append(f"apparition event dossier lacks {label}")
    elif not inventories:
        errors.append("apparition corpus-status has no recognizable event/status dossier records")


def _heresies(root: Path, record: dict, view: SourceView, errors: list[str]) -> None:
    tables = markdown_tables(role_text(root, record, "corpus-inventory"))
    keyed = [table for table in tables if any("key" in row and "disposition" in row for row in table)]
    for table in keyed:
        keys = [row["key"].strip("` ") for row in table if "key" in row]
        if len(keys) != len(set(keys)):
            errors.append("heresy census duplicates a stable key within one disposition ledger")
        for row in table:
            if "_malformed" in row or any(not value.strip() for value in row.values()):
                errors.append("heresy census has a malformed or empty disposition record")
    if not keyed:
        errors.append("heresy corpus inventory has no stable-key disposition records")
    rows = [row for table in tables for row in table]
    _inventory_links(root, record, rows, view, ("destination", "target", "body", "latex destination", "exact latex destination"), errors)


def check(root: Path, record: dict) -> list[str]:
    """Return reproducible source defects, never unperformed editorial reviews."""
    if record.get("kind") not in KINDS:
        return []
    root = Path(root).resolve()
    errors = []
    view = source_view(root, record)
    for role in ("question-inventory", "order-inventory", "virtue-inventory", "prayer-inventory", "corpus-status", "corpus-inventory", "terminology-audit", "prayer-text-audit", "derivation"):
        for source in role_paths(root, record, role):
            if not substantive(source.read_text(encoding="utf-8")):
                errors.append(f"{role}: record has no substantive content")
    kind = record["kind"]
    if kind.startswith("novena"):
        _novena(root, record, view, errors)
    elif kind.startswith("sacraments"):
        _sacraments(root, record, view, errors)
    elif kind == "angelology":
        _angelology(root, record, view, errors)
    elif kind == "virtues":
        _virtues(root, record, view, errors)
    elif kind == "marian-dogma":
        _dogmas(root, record, view, errors)
    elif kind == "marian-apparition":
        _apparitions(root, record, errors)
    elif kind == "heresies":
        _heresies(root, record, view, errors)
    return list(dict.fromkeys(errors))


def editorial_requirements(record: dict) -> list[str]:
    """Obligations outside this adapter's machine evidence; not a pass status."""
    if record.get("kind") not in KINDS:
        return []
    return list(record.get("profile_definition", {}).get("requirements", []))
