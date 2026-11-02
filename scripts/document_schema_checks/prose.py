"""Machine-checkable evidence architecture for prose publications.

The argument, chronology, and source judgments require editorial inspection.
Here a ledger must exist, contain content, and retain checkable destinations.
"""
from __future__ import annotations

from pathlib import Path
import re

from .reference import (
    _normal, _plain, commands, markdown_tables, role_paths, role_text,
    source_view, substantive, table_rows,
)


KINDS = {"article-faith", "article-canon-law", "article-scripture", "biography", "history-parish", "history-translation", "history-account"}
RECORDS = {
    "biography": ("scope", "source-audit", "chronology", "tradition-audit"),
    "history-parish": ("scope", "source-audit", "evidence-map", "pastor-succession"),
    "history-translation": ("scope", "source-audit", "evidence-map"),
    "history-account": ("scope", "source-audit", "evidence-map"),
}


def _ledger(root: Path, record: dict, role: str, errors: list[str]) -> None:
    sources = role_paths(root, record, role)
    if not sources:
        errors.append(f"missing required {role} record")
        return
    for source in sources:
        text = source.read_text(encoding="utf-8")
        if not substantive(text):
            errors.append(f"{role}: record contains no substantive content")
        for table in markdown_tables(text):
            identities = []
            for row in table:
                if "_malformed" in row:
                    errors.append(f"{role}: malformed table record")
                    continue
                # Only explicit keys are identities; repeated names/dates can
                # describe separate events, witnesses, or competing chronologies.
                if "key" in row:
                    identities.append(row["key"])
                if any(not value.strip() for value in row.values()):
                    errors.append(f"{role}: empty ledger field")
            if len(identities) != len(set(identities)):
                errors.append(f"{role}: duplicate stable ledger key")


def _legal_scope(root: Path, record: dict, view, errors: list[str]) -> None:
    # Some existing editions define a constant appendix macro in one source
    # and invoke it in their entrypoint; its heading is in the expanded view.
    text = view.text
    headings = [a[0] for name in ("section", "subsection", "subsubsection", "paragraph") for _, a in commands(text, name)]
    if not any(re.search(r"legal\s+scope", _plain(h), re.I) for h in headings):
        errors.append("canon-law article requires a reader-facing Legal Scope and Currentness block")
    scope = role_text(root, record, "scope") + "\n" + text
    # These are presence checks, not an assessment of the law's correctness or
    # present force. Neither date nor jurisdiction is guessed from metadata.
    requirements = {
        "identified governing law": r"\b(?:CIC|CCEO|Codex|Code|body of law|bodies of law)\b",
        "jurisdiction/persons": r"\b(?:jurisdiction|Latin Church|Eastern Catholic|persons|territor)\b",
        "as-of date": r"\b20\d\d-\d\d-\d\d\b",
        "amendments/currentness": r"\b(?:amendment|amendments|currentness|checked|effective|revised)\b",
    }
    for label, pattern in requirements.items():
        if not re.search(pattern, scope, re.I):
            errors.append(f"canon-law scope lacks {label}")


def _pastors(root: Path, record: dict, view, errors: list[str]) -> None:
    paths = role_paths(root, record, "pastor-succession")
    if len(paths) != 1:
        errors.append("parish history requires one canonical pastor-succession list")
        return
    source = paths[0]
    if view.occurrences.count(source) != 1:
        errors.append("pastor-succession list must be imported exactly once")
    text = source.read_text(encoding="utf-8")
    rows = [r for r in table_rows(text) if len(r) == 4 and not any(r"\textbf" in c for c in r)]
    if not rows:
        errors.append("pastor-succession list has no office/date/evidence rows")
    for row in rows:
        if any(not _plain(cell).strip() for cell in row):
            errors.append("pastor-succession list has an empty name/status, office, date, or witness field")
    # Order only this profile-mandated apparatus; history has no universal
    # timeline requirement and articles have no mandatory opening thesis.
    position = view.occurrences.index(source) if source in view.occurrences else -1
    scope = [p for p in role_paths(root, record, "scope-appendix") if p in view.occurrences]
    references = [p for p in role_paths(root, record, "references") if p in view.occurrences]
    if scope and position <= max(view.occurrences.index(p) for p in scope):
        errors.append("pastor-succession list must follow the terminal historical-scope appendix")
    if references and position >= min(view.occurrences.index(p) for p in references):
        errors.append("pastor-succession list must precede references")
    labels = {a[0] for _, a in commands(view.text, "label")}
    for name in ("ref", "pageref"):
        for _, args in commands(text, name):
            if args[0] not in labels:
                errors.append(f"pastor-succession reference does not resolve: {args[0]}")


def check(root: Path, record: dict) -> list[str]:
    if record.get("kind") not in KINDS:
        return []
    root = Path(root).resolve()
    errors = []
    roles = RECORDS.get(record["kind"], ("scope", "source-audit"))
    for role in roles:
        _ledger(root, record, role, errors)
    audit_paths = [p for role in roles if role != "pastor-succession" for p in role_paths(root, record, role)]
    if len(audit_paths) != len(set(audit_paths)):
        errors.append("distinct research roles must not alias the same record")
    view = source_view(root, record)
    if record["kind"] == "article-canon-law":
        _legal_scope(root, record, view, errors)
    if record["kind"] == "history-parish":
        _pastors(root, record, view, errors)
    return list(dict.fromkeys(errors))


def editorial_requirements(record: dict) -> list[str]:
    if record.get("kind") not in KINDS:
        return []
    return list(record.get("profile_definition", {}).get("requirements", []))
