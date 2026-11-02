"""Check canonical curriculum selections and prompt/solution source structure.

The existing curriculum checker owns stable lessons, worksheet IDs, variants,
course registry coverage and the shared layout machinery.  Its source audit is
separate from its rendered hierarchy/PDF audit.  These publication checks use
that source audit and connect each leaf to the actual packet/assessment shell.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from document_schema_checks.liturgy import _bound, _calls, _module, _text


def _signature(owner: Path) -> tuple:
    return tuple((str(path.relative_to(owner)), path.stat().st_mtime_ns, path.stat().st_size)
                 for path in sorted(owner.rglob("*"))
                 if path.is_file() and path.suffix in {".tex", ".sty", ".md"})


@lru_cache(maxsize=4)
def _audit(owner: str, signature: tuple) -> tuple[str, ...]:
    # The signature invalidates cached source results after an edit.  Several
    # dozen publications share this owner; no PDF is read or compiled here.
    checker = _module("tools/check-curriculum-structure")
    try:
        checker.audit_sources(Path(owner))
    except (OSError, UnicodeError, ValueError) as error:
        return tuple(str(error).splitlines())
    return ()


def _imports(text: str) -> list[str]:
    return [args[0] for args, _, _ in _calls(text, "input", 1)]


def _parts(text: str) -> list[str]:
    return [args[0] for args, _, _ in _calls(text, "part", 1)]


def _solution_mode(body: str, input_name: str, expected: str) -> bool:
    selected = [(start, args) for args, start, _ in _calls(body, "input", 1)
                if args[0] == input_name]
    if len(selected) != 1:
        return False
    modes = re.findall(r"\\solutions(true|false)(?![A-Za-z@])", body[:selected[0][0]])
    return bool(modes) and modes[-1] == expected


def _require_import(text: str, candidates: set[str], label: str) -> list[str]:
    found = [value.removesuffix(".tex") for value in _imports(text)]
    return [] if sum(value in candidates for value in found) == 1 else [
        f"curriculum entrypoint must import its canonical {label} exactly once"]


def _exercise_answers(owner: Path) -> list[str]:
    errors = []
    for path in sorted((owner / "shared/exercises").rglob("*.tex")):
        text = _text(path)
        for command, count in (("Exercise", 2), ("ShortExercise", 2),
                               ("LongExercise", 2), ("PassageExercise", 3)):
            for args, _, _ in _calls(text, command, count):
                if any(not value for value in args):
                    errors.append(f"{path.relative_to(owner)}: {command} requires its prompt and matching answer/model")
    # The stable ID is the selected assessment ID plus the source item
    # ordinal. The shared renderer (checked by audit_sources) owns both modes.
    assessment_path = owner / "shared/assessments/all.tex"
    for args, _, _ in _calls(_text(assessment_path), "AssessmentItem", 2):
        if any(not value for value in args):
            errors.append("canonical review item requires its prompt and matching answer/model")
    return errors


@lru_cache(maxsize=4)
def _answers(owner: str, signature: tuple) -> tuple[str, ...]:
    return tuple(_exercise_answers(Path(owner)))


def _packet(root: Path, record: dict, owner: Path, checker) -> list[str]:
    leaf = root / record["source_dir"]
    entry = _text(leaf / record["entrypoint"])
    data_path = leaf / "module-data.tex"
    data = _text(data_path)
    course_id = owner.relative_to(root / "src" / record["provider"]).as_posix()
    errors = []
    if checker._macro_value(entry, "CourseRoot", leaf) != course_id:
        errors.append("packet CourseRoot must name its canonical curriculum owner")
    if checker._macro_value(entry, "ModuleLeaf", leaf) != record["leaf"]:
        errors.append("packet ModuleLeaf must name this publication")
    errors.extend(_require_import(entry, {r"\ModuleLeaf/module-data", record["leaf"] + "/module-data"}, "module selection"))
    errors.extend(_require_import(entry, {r"\CourseRoot/shared/module-shell", course_id + "/shared/module-shell"}, "six-Part shell"))
    errors.extend(_bound(root, record, "module-selection", {data_path}))
    shell_path = owner / "shared/module-shell.tex"
    shell = _text(shell_path)
    parts = list(_calls(shell, "part", 1))
    if [args[0] for args, _, _ in parts] != list(checker.MODULE_PARTS):
        errors.append("packet shell must retain the six canonical Parts in order")
        return errors
    bodies = {args[0]: shell[end:parts[index + 1][1] if index + 1 < len(parts) else len(shell)]
              for index, (args, _, end) in enumerate(parts)}
    teaching = bodies["Teaching"]
    if _imports(teaching).count(r"\ModuleLessonSource") != 1:
        errors.append("Teaching must consume the selected stable lesson source once")
    practice, answers = bodies["Cumulative Practice"], bodies["Answers and Models"]
    for name, body, mode in (("Cumulative Practice", practice, "false"),
                             ("Answers and Models", answers, "true")):
        if not _solution_mode(body, r"\ModuleExerciseSource", mode):
            errors.append(f"{name} must render the same authoritative exercise source in its own solution mode")
        for command, value in (("SelectCourseUnits", r"\ModuleUnit"),
                               ("SelectWorksheetVariants", r"\ModuleWorksheetVariants")):
            if [args[0] for args, _, _ in _calls(body, command, 1)] != [value]:
                errors.append(f"{name} must use the canonical {command} selection exactly once")
    for command, part, argument in (("RenderModuleMemoryLearner", "Memory Work", r"\ModuleMemorySet"),
                                     ("RenderModuleMemorySolutions", "Answers and Models", r"\ModuleMemorySet"),
                                     ("RenderModuleReaderSet", "Reading and Composition", r"\ModuleReaderSet"),
                                     ("RenderModuleReaderSet", "Answers and Models", r"\ModuleReaderSet")):
        if [args[0] for args, _, _ in _calls(bodies[part], command, 1)] != [argument]:
            errors.append(f"{part} is detached from its canonical {command} source selection")
    # Do not accept a source field that merely names an existing unrelated file.
    for macro in ("ModuleLessonSource", "ModuleExerciseSource"):
        source = checker._source_path(owner, checker._macro_value(data, macro, data_path), data_path)
        units = checker._course_units(source)
        selected = checker._macro_value(data, "ModuleUnit", data_path).split(",")
        for unit in selected:
            if unit.strip() not in units:
                errors.append(f"{macro} omits selected stable lesson {unit.strip()}")
    return errors


def _assessment(root: Path, record: dict, owner: Path, checker) -> list[str]:
    leaf = root / record["source_dir"]
    entry = _text(leaf / record["entrypoint"])
    course_id = owner.relative_to(root / "src" / record["provider"]).as_posix()
    errors = _require_import(entry, {r"\CourseRoot/shared/assessment-shell", course_id + "/shared/assessment-shell"}, "review shell")
    shell = _text(owner / "shared/assessment-shell.tex").split(r"\begin{document}", 1)[-1]
    parts = list(_calls(shell, "part", 1))
    if _parts(shell) != list(checker.ASSESSMENT_PARTS):
        return errors + ["assessment shell must retain task-before-answer Part order"]
    for name, start, end in (("Review Forms", parts[1][2], parts[2][1]),
                             ("Answers and Models", parts[2][2], parts[3][1])):
        body = shell[start:end]
        if [args[0] for args, _, _ in _calls(body, "SelectAssessments", 1)] != [r"\AssessmentSelection"] or _imports(body).count(r"\CourseRoot/shared/assessments/all") != 1:
            errors.append(f"{name} must use the same canonical review IDs and answer source")
        if not _solution_mode(body, r"\CourseRoot/shared/assessments/all", "false" if name == "Review Forms" else "true"):
            errors.append(f"{name} must select its solution mode before rendering the canonical review source")
    return errors


def check(root: Path, record: dict) -> list[str]:
    if not record.get("kind", "").startswith("curriculum-"):
        return []
    root = Path(root).resolve()
    owner = root / "src" / record["provider"] / "curriculums/ecclesiastical-latin"
    checker = _module("tools/check-curriculum-structure")
    try:
        signature = _signature(owner)
        errors = list(_audit(str(owner), signature))
        errors.extend(_answers(str(owner), signature))
        if record["kind"] in {"curriculum-packet", "curriculum-poetry"}:
            errors.extend(_packet(root, record, owner, checker))
        elif record["kind"] == "curriculum-assessment":
            errors.extend(_assessment(root, record, owner, checker))
        return errors
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError, ImportError) as error:
        return [f"curriculum source structure: {error}"]
