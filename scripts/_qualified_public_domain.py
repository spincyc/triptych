"""The `qualified-public-domain` publication basis: one scoped token, one owner.

Publication policy section 1, priority 6 ("ambiguous but defensible basis ->
prefer publication, document the argument, mark the basis explicitly") needs a
mark a reader can see and a validator can hold. This module is that mark's
single implementation. It is GENERAL within its scope rather than a finite
hash-pinned list: any text meeting the limits of an adopted rights record may be
admitted, and every consumer refuses a text that does not.

The holding, the limits and the verbatim notices live in the adopted rights
record (`RECORDS`); this module reads that record's `[admission]` table from the
repository this code belongs to -- never from a caller-selected tree, so a
sandbox or a stray copy cannot widen it -- and applies it to:

* Latin provenance ledger rows (`latin_row_problems`, `calendar_problems`,
  `source_problems`), called by `_proper_latin`. A later typical edition
  (1970 and after) adds no right in unchanged preexisting wording, so a target
  slot of such an edition may carry the token where its wording equals the
  earlier Holy See publication -- but that edition is only ever the text-free
  comparison target, never the source or the carrier;
* English translation ledger entries (`translation_problems`) and project study
  English over admitted Latin (`study_translation_problems`), called by
  `check-calendar-masses` and `mass-propers`;
* Ordinary inventory witnesses (`ordinary_witness_problems`), called by
  `mass-ordinary`;
* source-library artifacts carrying the token as `rights_status`
  (`artifact_problems`), called by `source-library`.

A text on this basis is never `public-domain`: it is published, and it says
why, at the point of use, on every surface.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable, Mapping
import re
import tomllib

BASIS = "qualified-public-domain"
RECORD = "src/sources/inventories/holy-see-twenty-year-term-rights-v1.toml"
# The adopted records this token may cite. A new record is a new rights basis
# and therefore a reviewed code change, not a data edit.
RECORDS = (RECORD,)
TRUSTED_REPOSITORY = Path(__file__).resolve().parents[1]

# Latin provenance-ledger fields only a row on this basis may carry. They make
# the record's limits L1-L3 checkable per text: which Holy See publication first
# published these words, when, under which imprint and body, and by which United
# States formality the work is independently in the public domain.
ROW_FIELDS = (
    "first_publication",
    "first_publication_year",
    "first_publication_imprint",
    "first_publication_body",
    "us_formality",
)
EXACT_RELATIONSHIPS = frozenset(
    {"exact-transcription", "collated-exact", "editorial-projection-exact-to-target"}
)
# Artifact rights a public publication source of an admitted text may carry.
PUBLIC_SOURCE_RIGHTS = frozenset({BASIS, "public-domain"})
NOTICE_KINDS = ("latin", "english_carried", "english_study")


class AdmissionError(ValueError):
    """The adopted record is missing, unadopted, or its contract is malformed."""


def _strings(value: object) -> bool:
    return (isinstance(value, list) and bool(value)
            and all(isinstance(one, str) and one.strip() for one in value)
            and len(set(value)) == len(value))


def _year(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@lru_cache(maxsize=None)
def admission(record: str = RECORD) -> Mapping[str, object]:
    """The validated `[admission]` contract of one adopted record. Fails closed."""
    if record not in RECORDS:
        raise AdmissionError(f"{record!r} is not an adopted {BASIS} rights record")
    root = TRUSTED_REPOSITORY.resolve()
    path = root / record
    try:
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise AdmissionError(f"{record} escapes its repository")
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise AdmissionError(f"{record} is unreadable: {error}") from error
    if document.get("status") != "adopted" or document.get("basis_token") != BASIS:
        raise AdmissionError(f"{record} is not an adopted {BASIS} record")
    table = document.get("admission")
    if not isinstance(table, dict) or table.get("token") != BASIS:
        raise AdmissionError(f"{record} has no [admission] table for {BASIS}")
    years = table.get("first_publication_years")
    formalities = table.get("us_formalities")
    notices = table.get("notices")
    later = table.get("later_editions")
    if (not isinstance(years, list) or len(years) != 2 or not all(map(_year, years))
            or years[0] > years[1]
            or not _strings(table.get("imprints")) or not _strings(table.get("bodies"))
            or not isinstance(later, dict)
            or not _strings(later.get("target_calendars"))
            or not _strings(later.get("target_editions"))
            or not _strings(later.get("excluded_first_publication_terms"))
            or not _year(later.get("excluded_first_publication_from"))
            or not isinstance(formalities, dict) or not formalities
            or not all(_year(one) for one in formalities.values())
            or not isinstance(notices, dict)
            or any(not isinstance(notices.get(kind), str) or not notices[kind].strip()
                   for kind in NOTICE_KINDS)):
        raise AdmissionError(f"{record} [admission] is malformed")
    return {
        "record": record,
        "years": (years[0], years[1]),
        "imprints": frozenset(table["imprints"]),
        "bodies": frozenset(table["bodies"]),
        "target_calendars": frozenset(later["target_calendars"]),
        "target_editions": frozenset(later["target_editions"]),
        "excluded_terms": tuple(one.casefold() for one in later["excluded_first_publication_terms"]),
        "excluded_from": later["excluded_first_publication_from"],
        "us_formalities": dict(formalities),
        "notices": dict(notices),
    }


def notice(kind: str, record: str = RECORD) -> str:
    """The verbatim notice of one kind (`latin`, `english_carried`, `english_study`)."""
    return str(admission(record)["notices"][kind])


def notices(record: str = RECORD) -> frozenset[str]:
    return frozenset(admission(record)["notices"].values())


def _contract(authority: object) -> tuple[Mapping[str, object] | None, list[str]]:
    if authority not in RECORDS:
        return None, [f"{BASIS} publication_authority must name its adopted rights "
                      f"record {RECORD}"]
    try:
        return admission(str(authority)), []
    except AdmissionError as error:
        return None, [str(error)]


def latin_row_problems(row: Mapping[str, object]) -> list[str]:
    """Contract of one Latin provenance-ledger row; empty for unrelated rows."""
    declared = [field for field in ROW_FIELDS if field in row]
    if row.get("publication_basis") != BASIS:
        if declared:
            return [f"only a {BASIS} row declares {', '.join(declared)}"]
        return []
    contract, problems = _contract(row.get("publication_authority"))
    if contract is None:
        return problems
    if row.get("notice") != contract["notices"]["latin"]:
        problems.append(f"{BASIS} requires the record's verbatim Latin notice "
                        f"([admission.notices].latin of {contract['record']})")
    citation = row.get("first_publication")
    if not isinstance(citation, str) or not citation.strip():
        problems.append(f"{BASIS} requires first_publication naming the Holy See "
                        "publication that first published these words")
    year = row.get("first_publication_year")
    first, last = contract["years"]
    if not _year(year):
        problems.append(f"{BASIS} requires an integer first_publication_year")
    elif year < first:
        problems.append(f"{BASIS} refuses a first publication of {year}: before {first} "
                        "the words are public-domain on the ordinary basis and must "
                        "not be marked qualified")
    elif year > last:
        problems.append(f"{BASIS} refuses a first publication of {year}: a work "
                        f"published after {last} had not exhausted its source term by "
                        "1 January 1996 (postconciliar 1976+ editions are outside it)")
    if isinstance(citation, str) and any(term in citation.casefold()
                                         for term in contract["excluded_terms"]):
        cited_years = [int(one) for one in re.findall(r"(?<!\d)(1[89]\d\d|20\d\d)(?!\d)", citation)]
        if ((_year(year) and year >= contract["excluded_from"])
                or any(one >= contract["excluded_from"] for one in cited_years)):
            problems.append(f"{BASIS} refuses a first publication in a "
                            f"{contract['excluded_from']}-or-later Missal edition: those "
                            "editions are only ever comparison targets, and their own "
                            "status is held by postconciliar-latin-rights-v1.toml")
    if row.get("first_publication_imprint") not in contract["imprints"]:
        problems.append(f"{BASIS} first_publication_imprint must be one of "
                        f"{sorted(contract['imprints'])}: first publication in "
                        "Vatican City is a limit of the record")
    if row.get("first_publication_body") not in contract["bodies"]:
        problems.append(f"{BASIS} first_publication_body must be one of "
                        f"{sorted(contract['bodies'])}: publication under the Holy "
                        "See's name and at its expense is a limit of the record")
    formality = row.get("us_formality")
    limit = contract["us_formalities"].get(formality) if isinstance(formality, str) else None
    if limit is None:
        problems.append(f"{BASIS} us_formality must be one of "
                        f"{sorted(contract['us_formalities'])}")
    elif _year(year) and first <= year <= last and year > limit:
        problems.append(f"{BASIS} refuses us_formality {formality!r} for a {year} "
                        f"publication: it reaches only works first published by {limit} "
                        "(a 1964-1977 publication with notice was renewed automatically)")
    if row.get("publication_status") == "permitted":
        if row.get("provenance_status") != "collated":
            problems.append(f"{BASIS} publication requires per-text collation")
        if row.get("relationship") not in EXACT_RELATIONSHIPS:
            problems.append(f"{BASIS} publication requires an exact witness relationship")
    return problems


def calendar_problems(row: Mapping[str, object], calendar: str) -> list[str]:
    """Static per-calendar requirements (no source graph needed).

    A row in a calendar whose target is a later typical edition must name the
    text-free comparison against that target; `source_problems` checks what it
    names.
    """
    if row.get("publication_basis") != BASIS:
        return []
    contract, problems = _contract(row.get("publication_authority"))
    if contract is None:
        return problems
    verification = row.get("verification_source_id")
    if (calendar in contract["target_calendars"]
            and (not isinstance(verification, str) or not verification.strip())):
        return [f"{BASIS} in the {calendar} calendar requires verification_source_id: "
                "the text-free comparison passage on its later typical edition"]
    return []


def _editions(source_id: str, sources: Mapping[str, Mapping[str, object]],
              backing: Callable) -> set[str]:
    """Every edition a source record is, or is backed or projected from."""
    record = sources.get(source_id) or {}
    editions = {record.get("edition_id")}
    artifact = backing(source_id, sources)
    if artifact is not None:
        editions.add(artifact.get("edition_id"))
        parents = list(artifact.get("projected_from") or [])
        if isinstance(artifact.get("derived_from"), str):
            parents.append(artifact["derived_from"])
        for parent in parents:
            editions.add((sources.get(str(parent)) or {}).get("edition_id"))
            parent_artifact = backing(str(parent), sources)
            if parent_artifact is not None:
                editions.add(parent_artifact.get("edition_id"))
    return {one for one in editions if isinstance(one, str) and one}


def source_problems(row: Mapping[str, object], sources: Mapping[str, Mapping[str, object]],
                    backing: Callable, *, calendar: str = "") -> list[str]:
    """Source-graph contract of a permitted row on the token.

    `backing(source_id, sources)` returns the artifact behind an exact witness.
    Every public publication source must itself be distributable here and at
    least one must carry the token, so the words' own carrier is never silently
    promoted to `public-domain`. No source, carrier or carrier parent may be a
    later typical edition: the words come from the earlier Holy See publication.
    In a later-edition calendar the row must name a text-free comparison passage
    on that edition as its verification witness.
    """
    if row.get("publication_basis") != BASIS:
        return []
    contract, problems = _contract(row.get("publication_authority"))
    if contract is None:
        return problems
    targets = contract["target_editions"]
    rights: dict[str, str] = {}
    for source_id in row.get("publication_source_ids") or []:
        source_id = str(source_id)
        artifact = backing(source_id, sources)
        if artifact is not None:
            rights[source_id] = str(artifact.get("rights_status") or "")
        if _editions(source_id, sources, backing) & targets:
            problems.append(f"{BASIS} publication source {source_id!r} is or derives from "
                            "a later typical edition; the carrier must be the earlier Holy "
                            "See publication or a transcription of it")
    problems.extend(f"{BASIS} publication source {source_id!r} has rights_status "
                    f"{status!r}; only {sorted(PUBLIC_SOURCE_RIGHTS)} may be cited"
                    for source_id, status in sorted(rights.items())
                    if status not in PUBLIC_SOURCE_RIGHTS)
    if BASIS not in rights.values():
        problems.append(f"{BASIS} publication requires a publication_source_ids "
                        f"artifact with rights_status {BASIS!r}")
    witness = row.get("source_id")
    if isinstance(witness, str) and _editions(witness, sources, backing) & targets:
        problems.append(f"{BASIS} provenance source_id must witness the earlier Holy See "
                        "publication, never a later typical edition")
    if calendar in contract["target_calendars"]:
        verification = str(row.get("verification_source_id") or "")
        record = sources.get(verification) or {}
        if (record.get("record_type") != "passage"
                or not _editions(verification, sources, backing) & targets):
            problems.append(f"{BASIS} in the {calendar} calendar requires "
                            "verification_source_id to be a comparison passage on its "
                            "later typical edition")
        elif "text" in record:
            problems.append(f"{BASIS} target comparison passage must be text-free")
    return problems


def translation_problems(entry: Mapping[str, object]) -> list[str]:
    """English carried from a lapsed United States book over admitted Latin."""
    if entry.get("rights") != BASIS:
        return []
    problems = []
    if entry.get("lang") != "en":
        problems.append(f"{BASIS} translation is defined for English only")
    if not isinstance(entry.get("source_id"), str) or not str(entry["source_id"]).strip():
        problems.append(f"{BASIS} translation must name its source_id")
    try:
        expected = notice("english_carried")
    except AdmissionError as error:
        return [*problems, str(error)]
    if entry.get("notice") != expected:
        problems.append(f"{BASIS} translation requires the record's verbatim notice "
                        f"([admission.notices].english_carried of {RECORD})")
    return problems


def study_translation_problems(translations: Iterable[Mapping[str, object]]) -> list[str]:
    """Project study English over admitted Latin is visibly qualified too."""
    try:
        expected = notice("english_study")
    except AdmissionError as error:
        return [str(error)]
    return [f"project study English over {BASIS} Latin requires the record's verbatim "
            f"notice ([admission.notices].english_study of {RECORD})"
            for one in translations
            if one.get("rights") == "project-created" and one.get("notice") != expected]


def ordinary_witness_problems(entry: Mapping[str, object]) -> list[str]:
    """An Ordinary witness on this basis carries its notice as its acknowledgement.

    The Ordinary reader prints a witness's `acknowledgement` beside every
    element whose words it supplies, so the notice travels with the words.
    """
    if entry.get("rights") != BASIS:
        return []
    kind = {"la": "latin", "en": "english_carried"}.get(str(entry.get("lang")))
    if kind is None:
        return [f"{BASIS} Ordinary witness is defined for Latin and English only"]
    try:
        expected = notice(kind)
    except AdmissionError as error:
        return [str(error)]
    if entry.get("acknowledgement") != expected:
        return [f"{BASIS} Ordinary witness acknowledgement must be the record's verbatim "
                f"{kind} notice ([admission.notices].{kind} of {RECORD})"]
    return []


def artifact_problems(data: Mapping[str, object]) -> list[str]:
    """A source-library artifact whose rights_status is the token."""
    if data.get("rights_status") != BASIS:
        return []
    problems = []
    if data.get("rights_jurisdiction") != "United States":
        problems.append(f'{BASIS} artifact requires rights_jurisdiction = "United States"')
    basis = data.get("rights_basis")
    try:
        expected = (notice("latin"), notice("english_carried"))
    except AdmissionError as error:
        return [*problems, str(error)]
    if (not isinstance(basis, str) or RECORD not in basis
            or not any(one in basis for one in expected)):
        problems.append(f"{BASIS} artifact rights_basis must cite {RECORD} and carry "
                        "its verbatim latin or english_carried notice")
    return problems
