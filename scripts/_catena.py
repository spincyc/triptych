#!/usr/bin/env python3
"""The catena's edge from a held commentary fragment to the scripture it is on.

`guidance/catena.md` settles the design; this validates and derives it. The
short version of what was found and what follows:

The container already exists. A `passage` record in the source library holds a
fragment's text, its edition, its rights basis and its locator, and validates
every transcribed segment against hash-pinned bytes. Nothing had to be invented
for L3, and inventing a parallel record would have been a second copy of a
solved problem.

What did not exist is the edge. A passage's `locus` addresses the *commentary*
("11.7" is De civitate Dei XI.7), so no query could return the fragments on
Genesis 1. `src/sources/commentary/fragment-loci.yaml` is that edge, kept beside
the source records rather than inside them: adding a field to a passage would
move its `source_fingerprint`, and 101 tracked binding files pin fingerprints.

Three things this file refuses, because a catena that fakes its refusals is
worth less than an empty page:

* an extent in any numbering but `_projection.CANONICAL`, which is the whole of
  Rule 3 — a fragment stored against a bare "Psalm 9:22" is anchored to nothing;
* a fragment whose work-alias group reaches books its canonical title does not
  name, which is Rule 8 and TASK-100. `guidance/catena.md` reports two such
  groups; measured here there are four. Aquinas and Theophylact are the two it
  names, and beside them stand Albert the Great's commentary on the Twelve
  Minor Prophets filed under *Commentarii in Amos prophetam* and Theodoret's
  Jeremiah-Baruch-Lamentations filed under *Commentarius in Ieremiam*;
* a fragment whose passage record reaches, through its edition, a work that is
  not the work the fragment claims. That is not pedantry: the NPNF volumes are
  tracked as anthologies whose `responsible` is Philip Schaff, so a label
  derived from the container would print Schaff as the author of Augustine.

The author is derived here and stored nowhere. `work_id` names a work record and
its `responsible` is the author; `work_alias` is the key into the harvest's
`work-aliases.yaml`; the two must agree, and that agreement is the work-identity
reconciliation `src/sources/commentary/README.md` asks for and nothing had
performed — every `work_id` in the harvested index is still null.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any, Iterable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _projection  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

SCHEMA = "triptych-commentary-fragment-loci/v1"

# The edge file, the alias table it references, and the bible whose book tokens
# and chapter counts define the canonical extents. The Clementine is the
# canonical Latin witness and declares `numbering: vulgate`, which is what
# `_projection.CANONICAL` projects into.
EDGES_RELATIVE = Path("src/sources/commentary/fragment-loci.yaml")
ALIASES_RELATIVE = Path("src/sources/commentary/work-aliases.yaml")
INDEX_RELATIVE = Path("src/sources/commentary/passage-commentary-index.yaml")
CANONICAL_BIBLE = "clementine-vulgate"
BIBLES_RELATIVE = Path("src/sources/bibles")
MODEL_RELATIVE = Path("src/web/browser/catena/catena-model.js")

FRAGMENT_FIELDS = {
    "passage_id",
    "work_id",
    "work_alias",
    "text_date",
    "text_date_basis",
    "numbering",
    "extent",
    "basis",
}
EXTENT_FIELDS = {
    "token",
    "first_chapter",
    "first_verse",
    "last_chapter",
    "last_verse",
}

# An artifact may only reach the page under one of these. `rights_status` is
# recorded per artifact rather than per edition — `guidance/catena.md` Rule 9
# says the edition carries the licence, and the library actually puts it one
# level down, on the exact bytes, which is stricter and is why the rule is read
# that way here. Anything else is not hidden at render time: it never enters the
# emitted structure at all, exactly as an unpublishable bible is absent from
# `bibles.json` rather than filtered in the browser.
PUBLISHABLE_RIGHTS = {"public-domain", "licensed-for-redistribution"}

# Latin forms of the book names that commentary titles actually use. Declared,
# not derived, and the reason is worth stating: the tracked book indexes carry
# English names, tokens and Douay titles, and no tracked artifact in this
# repository holds the Latin accusative and genitive a title declines into. The
# guard against a hand-typed table drifting is that every key must be a token
# the canonical book index knows, which `book_forms` enforces.
LATIN_BOOK_FORMS = {
    "Gen": ("genesim", "genesin", "genesis", "genesi", "hexaemeron", "hexameron"),
    "Ex": ("exodum", "exodi"),
    "Lev": ("leviticum", "levitici"),
    "Num": ("numeros", "numerorum"),
    "Deut": ("deuteronomium", "deuteronomii"),
    "Jos": ("iosue", "josue"),
    "Job": ("iob", "job"),
    "Ps": ("psalmos", "psalmorum", "psalmis", "psalterium", "psalmi"),
    "Prov": ("proverbia", "proverbiorum"),
    "Eccles": ("ecclesiasten", "ecclesiastes"),
    "Cant": ("cantica", "canticum", "canticorum"),
    "Is": ("isaiam", "isaias", "esaiam"),
    "Jer": ("ieremiam", "jeremiam", "ieremias"),
    "Lam": ("lamentationes", "threnos", "threni"),
    "Bar": ("baruch",),
    "Ezech": ("ezechielem", "ezechiel"),
    "Dan": ("danielem", "daniel"),
    "Os": ("osee", "oseam"),
    "Joel": ("ioelem", "joelem"),
    "Amos": ("amos",),
    "Abd": ("abdiam", "abdias"),
    "Jon": ("ionam", "jonam", "ionas"),
    "Mich": ("michaeam", "michaeas", "micheam"),
    "Nah": ("nahum", "naum"),
    "Hab": ("habacuc", "habakkuk"),
    "Soph": ("sophoniam", "sophonias"),
    "Agg": ("aggaeum", "aggaeus"),
    "Zach": ("zachariam", "zacharias"),
    "Mal": ("malachiam", "malachias"),
    "Matt": ("matthaeum", "mattheum", "matthaei"),
    "Mark": ("marcum", "marci"),
    "Luke": ("lucam", "lucae"),
    "John": ("ioannem", "johannem", "iohannis", "ioannis", "johannis"),
    "Acts": ("actus apostolorum", "acta apostolorum"),
    "Rom": ("romanos", "romanis"),
    "1Cor": ("i ad corinthios", "primam ad corinthios", "i corinthios"),
    "2Cor": ("ii ad corinthios", "secundam ad corinthios", "ii corinthios"),
    "Gal": ("galatas", "galatis"),
    "Eph": ("ephesios", "ephesiis"),
    "Phil": ("philippenses", "philippensibus"),
    "Col": ("colossenses", "colossensibus"),
    "1Thess": ("i ad thessalonicenses", "primam ad thessalonicenses", "i thessalonicenses"),
    "2Thess": ("ii ad thessalonicenses", "secundam ad thessalonicenses", "ii thessalonicenses"),
    "1Tim": ("i ad timotheum", "primam ad timotheum", "i timotheum"),
    "2Tim": ("ii ad timotheum", "secundam ad timotheum", "ii timotheum"),
    "Tit": ("titum", "tito"),
    "Philem": ("philemonem", "philemoni"),
    "Heb": ("hebraeos", "hebreos"),
    "Apoc": ("apocalypsim", "apocalypsin", "apocalypsis"),
}

# English forms a title uses that the book index does not spell. Same guard.
ENGLISH_BOOK_FORMS = {
    "Ps": ("psalms", "psalter"),
    "Cant": ("song of songs", "canticle of canticles"),
    "Apoc": ("revelation", "apocalypse"),
    "1Cor": ("first corinthians", "1 corinthians"),
    "2Cor": ("second corinthians", "2 corinthians"),
    "1Thess": ("first thessalonians", "1 thessalonians"),
    "2Thess": ("second thessalonians", "2 thessalonians"),
    "1Tim": ("first timothy", "1 timothy"),
    "2Tim": ("second timothy", "2 timothy"),
}


class CatenaError(RuntimeError):
    """The edge could not be read or derived, with the reason to act on."""


class Extent(NamedTuple):
    """A canonical range. `first` and `last` are (chapter, verse) points."""

    token: str
    first_chapter: int
    first_verse: int
    last_chapter: int
    last_verse: int

    def touches(self, chapter: int) -> bool:
        return self.first_chapter <= chapter <= self.last_chapter

    def spans_chapters(self) -> bool:
        return self.last_chapter > self.first_chapter


def _yaml():
    try:
        import yaml
    except ModuleNotFoundError as error:  # pragma: no cover - environment
        raise CatenaError("PyYAML is required to read the commentary sources") from error
    return yaml


def _load_yaml(path: Path) -> Any:
    if not path.is_file():
        raise CatenaError(f"{path}: not found")
    with path.open(encoding="utf-8") as handle:
        return _yaml().safe_load(handle)


# ---------------------------------------------------------------------------
# The canon, enumerated
# ---------------------------------------------------------------------------


def _book_index(root: Path) -> list[dict[str, str]]:
    """The canonical edition's book index, read from its one tracked artifact."""
    found = sorted(
        (root / "src/sources/works").glob(
            "*/*/editions/*/artifacts/book-index-*/book-index.tsv"
        )
    )
    wanted = [path for path in found if "vulgata-clementina" in path.as_posix()]
    if len(wanted) != 1:
        raise CatenaError(
            f"expected one Clementine book index under {root}, found {len(wanted)}"
        )
    with wanted[0].open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canon(root: Path = ROOT) -> list[dict[str, Any]]:
    """Every book of the canon in order, with its chapter count.

    Derived, never enumerated by hand: the order and the names come from the
    canonical edition's tracked book index, and the chapter count is how many
    chapter fragments that edition actually carries. Nothing in this repository
    enumerated the canon before — every existing structure file covers only what
    a calendar or a reading plan happens to cite — so a page that walks the
    Bible chapter by chapter had nothing to walk.
    """
    chapters_root = root / BIBLES_RELATIVE / CANONICAL_BIBLE / "chapters"
    if not chapters_root.is_dir():
        raise CatenaError(f"{chapters_root}: the canonical edition has no chapters")
    books: list[dict[str, Any]] = []
    for record in _book_index(root):
        token = (record.get("token") or "").strip()
        directory = chapters_root / token
        if not directory.is_dir():
            continue
        numbers = sorted(
            int(path.stem) for path in directory.glob("*.json") if path.stem.isdigit()
        )
        if not numbers:
            continue
        books.append(
            {
                "token": token,
                "name": (record.get("modern_name") or token).strip(),
                "title": (record.get("douay_title") or "").strip(),
                "testament": (record.get("testament") or "").strip(),
                "chapters": len(numbers),
                "last_chapter": numbers[-1],
            }
        )
    if not books:
        raise CatenaError(f"{chapters_root}: no book of the canon could be enumerated")
    return books


def _chapter_ceiling(root: Path) -> dict[str, int]:
    return {book["token"]: book["last_chapter"] for book in canon(root)}


def _verse_ceiling(root: Path, token: str, chapter: int) -> int | None:
    path = root / BIBLES_RELATIVE / CANONICAL_BIBLE / "chapters" / token / f"{chapter}.json"
    if not path.is_file():
        return None
    verses = json.loads(path.read_text(encoding="utf-8")).get("verses") or {}
    numbers = [int(key) for key in verses if str(key).isdigit()]
    return max(numbers) if numbers else None


# ---------------------------------------------------------------------------
# Rule 8 — a title that does not cover its work
# ---------------------------------------------------------------------------


def book_forms(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    """Every lowercase name by which a title may call a book, keyed by token."""
    index = {
        (record.get("token") or "").strip(): record for record in _book_index(root)
    }
    forms: dict[str, tuple[str, ...]] = {}
    for token, record in index.items():
        names = {(record.get("modern_name") or "").strip().lower()}
        names.add((record.get("douay_title") or "").strip().lower())
        for alternate in (record.get("alternate_names") or "").split(";"):
            alternate = alternate.strip().lower()
            if len(alternate) > 3 and not alternate.endswith("."):
                names.add(alternate)
        forms[token] = tuple(sorted(name for name in names if len(name) > 3))
    for declared in (LATIN_BOOK_FORMS, ENGLISH_BOOK_FORMS):
        for token, extra in declared.items():
            # A token the index does not carry is skipped rather than refused,
            # because a fixture index carries three books and a typo in the
            # declared table is a defect in this file, not in the caller's
            # root. `undeclared_form_tokens` is what a test asserts on.
            if token not in index:
                continue
            forms[token] = tuple(sorted(set(forms.get(token, ())) | set(extra)))
    return forms


def undeclared_form_tokens(root: Path = ROOT) -> list[str]:
    """Declared book forms naming a token the canonical index does not carry."""
    known = {(record.get("token") or "").strip() for record in _book_index(root)}
    declared = set(LATIN_BOOK_FORMS) | set(ENGLISH_BOOK_FORMS)
    return sorted(declared - known)


# A personal name qualifying another book's title is not a second book. `In
# Apocalypsim Iohannis` names one book and `Expositio in Lamentationes
# Hieremiae` names one book, and reading the qualifier as the Gospel or as the
# prophecy reported six failures where five are real — the plausible-and-wrong
# answer this apparatus exists to catch. Stripped before matching rather than
# subtracted after, so one mechanism covers both.
QUALIFIERS = (
    re.compile(r"\b(apocalyps\w+) (?:beati |sancti )?(?:i|j)o(?:h)?ann\w+"),
    re.compile(r"\b(lamentation\w+|threno\w+|threni) (?:of )?(?:h?ieremia\w*|jeremiah)"),
)


def _books_named(title: str, forms: dict[str, tuple[str, ...]]) -> set[str]:
    lowered = " " + re.sub(r"[^a-z0-9 ]+", " ", title.lower()) + " "
    lowered = re.sub(r"\s+", " ", lowered)
    for qualifier in QUALIFIERS:
        lowered = qualifier.sub(r"\1", lowered)
    named: set[str] = set()
    for token, names in forms.items():
        for name in names:
            if f" {name} " in lowered:
                named.add(token)
                break
    return named


def title_covers_group(group: dict[str, Any], forms: dict[str, tuple[str, ...]]) -> str:
    """Empty when the group's canonical title covers its extent, else the reason.

    Rule 8, and it is cheap exactly as `guidance/catena.md` says: a group's
    canonical title must not name a book that the group's member titles do not
    all share. The failure it catches is a work named after one tenth of itself,
    which on a catena page is a rendered false claim rather than a cataloguing
    infelicity.
    """
    titles = [title for title in group.get("titles") or () if str(title).strip()]
    if not titles:
        return ""
    named = _books_named(str(group.get("work") or ""), forms)
    if not named:
        # A title that names no book claims none, so it cannot claim too few.
        # `Expositio in omnes divi Pauli epistolas` is the right name for a
        # Pauline commentary and `De civitate Dei` names no book at all.
        return ""
    spanned: set[str] = set()
    for title in titles:
        spanned |= _books_named(str(title), forms)
    uncovered = sorted(spanned - named)
    if not uncovered:
        return ""
    return (
        f"the canonical title names {', '.join(sorted(named))} while the group "
        f"also reaches {', '.join(uncovered)}"
    )


def failing_groups(root: Path = ROOT) -> list[tuple[str, str, str]]:
    """Every alias group whose canonical title does not cover its extent."""
    forms = book_forms(root)
    groups = _load_yaml(root / ALIASES_RELATIVE).get("groups") or []
    failures = []
    for group in groups:
        reason = title_covers_group(group, forms)
        if reason:
            failures.append((str(group.get("author")), str(group.get("work")), reason))
    return sorted(failures)


# ---------------------------------------------------------------------------
# The source library, read for the few records a fragment reaches
# ---------------------------------------------------------------------------


def _records(root: Path, pattern: str) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for path in sorted((root / "src/sources").glob(pattern)):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        identifier = data.get("id")
        if isinstance(identifier, str):
            found[identifier] = data
    return found


class Sources(NamedTuple):
    """The records a fragment can reach, loaded once."""

    works: dict[str, dict[str, Any]]
    editions: dict[str, dict[str, Any]]
    artifacts: dict[str, dict[str, Any]]
    segments: dict[str, dict[str, Any]]
    passages: dict[str, dict[str, Any]]


def load_sources(root: Path = ROOT) -> Sources:
    return Sources(
        works=_records(root, "works/*/*/work.toml"),
        editions=_records(root, "works/*/*/editions/*/edition.toml"),
        artifacts=_records(root, "works/*/*/editions/*/artifacts/*/artifact.toml"),
        segments=_records(root, "works/*/*/editions/*/segments/*.toml"),
        passages=_records(root, "works/*/*/editions/*/passages/*.toml"),
    )


# ---------------------------------------------------------------------------
# The edge itself
# ---------------------------------------------------------------------------


def load_edges(root: Path = ROOT) -> dict[str, Any]:
    data = _load_yaml(root / EDGES_RELATIVE)
    if not isinstance(data, dict):
        raise CatenaError(f"{EDGES_RELATIVE}: not a mapping")
    if data.get("schema") != SCHEMA:
        raise CatenaError(
            f"{EDGES_RELATIVE}: declares schema {data.get('schema')!r}, expected {SCHEMA!r}"
        )
    return data


def _extent(value: Any) -> Extent | None:
    if not isinstance(value, dict) or set(value) != EXTENT_FIELDS:
        return None
    try:
        return Extent(
            token=str(value["token"]),
            first_chapter=int(value["first_chapter"]),
            first_verse=int(value["first_verse"]),
            last_chapter=int(value["last_chapter"]),
            last_verse=int(value["last_verse"]),
        )
    except (TypeError, ValueError):
        return None


def validate(root: Path = ROOT) -> list[str]:
    """Every reason the edge cannot be rendered, in a deterministic order."""
    errors: list[str] = []
    where = EDGES_RELATIVE.as_posix()
    data = load_edges(root)

    declared = data.get("numbering")
    if declared != _projection.CANONICAL:
        errors.append(
            f"{where}: numbering is {declared!r}; a fragment anchors to "
            f"{_projection.CANONICAL!r} and to nothing else (Rule 3)"
        )

    sources = load_sources(root)
    forms = book_forms(root)
    groups = {
        (str(group.get("author")), str(group.get("work"))): group
        for group in _load_yaml(root / ALIASES_RELATIVE).get("groups") or []
    }
    ceilings = _chapter_ceiling(root)

    fragments = data.get("fragments")
    if not isinstance(fragments, list) or not fragments:
        errors.append(f"{where}: fragments must be a nonempty list")
        return sorted(errors)

    seen: set[str] = set()
    for ordinal, fragment in enumerate(fragments, start=1):
        label = f"{where}: fragments[{ordinal}]"
        if not isinstance(fragment, dict):
            errors.append(f"{label} must be a mapping")
            continue
        unknown = sorted(set(fragment) - FRAGMENT_FIELDS)
        missing = sorted(FRAGMENT_FIELDS - set(fragment))
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        if missing:
            errors.append(f"{label} is missing: {', '.join(missing)}")
            continue

        passage_id = str(fragment["passage_id"])
        label = f"{where}: {passage_id}"
        if passage_id in seen:
            errors.append(f"{label} appears twice")
        seen.add(passage_id)

        if fragment.get("numbering") != _projection.CANONICAL:
            errors.append(
                f"{label} declares numbering {fragment.get('numbering')!r}, "
                f"not {_projection.CANONICAL!r} (Rule 3)"
            )

        if not isinstance(fragment.get("text_date"), int) or isinstance(
            fragment.get("text_date"), bool
        ):
            errors.append(f"{label} needs an integer text_date (Rule 7)")
        for field in ("text_date_basis", "basis"):
            if not str(fragment.get(field) or "").strip():
                errors.append(f"{label} needs a {field}")

        extent = _extent(fragment.get("extent"))
        if extent is None:
            errors.append(
                f"{label} extent needs exactly {', '.join(sorted(EXTENT_FIELDS))}"
            )
        else:
            errors.extend(_extent_errors(root, label, extent, ceilings))

        # The work, and the author derived from it once.
        work_id = str(fragment["work_id"])
        work = sources.works.get(work_id)
        if work is None:
            errors.append(f"{label} names work {work_id}, which is not a work record")
        author = str((work or {}).get("responsible") or "").strip()
        if work is not None and not author:
            errors.append(f"{label}: {work_id} has no responsible, so no author is derivable")

        alias = fragment.get("work_alias")
        if not isinstance(alias, dict) or set(alias) != {"author", "work"}:
            errors.append(f"{label} work_alias needs exactly author and work")
        else:
            key = (str(alias["author"]), str(alias["work"]))
            group = groups.get(key)
            if group is None:
                errors.append(
                    f"{label} work_alias {key[0]} / {key[1]} resolves to no group "
                    f"in {ALIASES_RELATIVE.as_posix()}"
                )
            else:
                if author and key[0] != author:
                    errors.append(
                        f"{label}: {work_id} is by {author!r} and the alias group is "
                        f"by {key[0]!r}; the two identity spaces disagree"
                    )
                reason = title_covers_group(group, forms)
                if reason:
                    errors.append(
                        f"{label} cannot render: {key[0]} / {key[1]} fails the title "
                        f"check because {reason} (Rule 8, TASK-100)"
                    )

        errors.extend(_passage_errors(sources, label, passage_id, work_id))

    errors.extend(_blocked_errors(sources, data, where, seen))
    errors.extend(_solved_case_errors(data, where, seen))
    return sorted(errors)


def _blocked_errors(
    sources: Sources, data: dict[str, Any], where: str, rendered: set[str]
) -> list[str]:
    """A recorded refusal must be real, and must not be a place to hide a fragment.

    Every blocked passage has to exist, has to carry both a reason and a fix,
    and must not also stand in the rendered list. Without the last check the
    block would be a second answer to the same question, which is the fault this
    whole file is arranged to avoid.
    """
    errors: list[str] = []
    for ordinal, entry in enumerate(data.get("blocked") or (), start=1):
        label = f"{where}: blocked[{ordinal}]"
        if not isinstance(entry, dict) or set(entry) != {
            "passage_ids",
            "work_alias",
            "reason",
            "fix",
        }:
            errors.append(f"{label} needs passage_ids, work_alias, reason and fix")
            continue
        for field in ("reason", "fix"):
            if not str(entry.get(field) or "").strip():
                errors.append(f"{label} needs a {field}")
        identifiers = entry.get("passage_ids")
        if not isinstance(identifiers, list) or not identifiers:
            errors.append(f"{label} needs at least one passage_id")
            continue
        for passage_id in identifiers:
            passage_id = str(passage_id)
            if passage_id not in sources.passages:
                errors.append(f"{label} names {passage_id}, which is not a passage record")
            if passage_id in rendered:
                errors.append(
                    f"{label} names {passage_id}, which is also rendered above; a "
                    f"fragment is blocked or held, never both"
                )
    return errors


def _extent_errors(
    root: Path, label: str, extent: Extent, ceilings: dict[str, int]
) -> list[str]:
    errors: list[str] = []
    if extent.token not in ceilings:
        errors.append(
            f"{label} extent names book {extent.token!r}, which the canonical "
            f"edition does not carry"
        )
        return errors
    if (extent.first_chapter, extent.first_verse) > (
        extent.last_chapter,
        extent.last_verse,
    ):
        errors.append(f"{label} extent ends before it begins")
    for chapter in (extent.first_chapter, extent.last_chapter):
        if chapter < 1 or chapter > ceilings[extent.token]:
            errors.append(
                f"{label} extent names {extent.token} {chapter}, past the "
                f"canonical last chapter {ceilings[extent.token]}"
            )
    for chapter, verse in (
        (extent.first_chapter, extent.first_verse),
        (extent.last_chapter, extent.last_verse),
    ):
        ceiling = _verse_ceiling(root, extent.token, chapter)
        if ceiling is not None and (verse < 1 or verse > ceiling):
            errors.append(
                f"{label} extent names {extent.token} {chapter}:{verse}, past the "
                f"canonical last verse {ceiling}"
            )
    return errors


def _passage_errors(
    sources: Sources, label: str, passage_id: str, work_id: str
) -> list[str]:
    errors: list[str] = []
    passage = sources.passages.get(passage_id)
    if passage is None:
        errors.append(f"{label} is not a passage record in the source library")
        return errors
    if not str(passage.get("locator") or passage.get("locus") or "").strip():
        errors.append(f"{label} has no locator, so a reader cannot check it")

    edition_id = str(passage.get("edition_id") or "")
    segment_id = passage.get("segment_id")
    if isinstance(segment_id, str) and segment_id:
        segment = sources.segments.get(segment_id)
        if segment is None:
            errors.append(f"{label} names segment {segment_id}, which does not resolve")
        else:
            edition_id = str(segment.get("edition_id") or edition_id)
    edition = sources.editions.get(edition_id)
    if edition is None:
        errors.append(f"{label} reaches no edition record through {edition_id}")
        return errors
    reached = str(edition.get("work_id") or "")
    if reached != work_id:
        errors.append(
            f"{label} claims {work_id} but its edition belongs to {reached}; a label "
            f"derived from the container would name the wrong author"
        )
    if not str(edition.get("language") or "").strip():
        errors.append(f"{label}: {edition_id} declares no language")

    artifact_id = str(passage.get("artifact_id") or "")
    artifact = sources.artifacts.get(artifact_id)
    if artifact is None:
        errors.append(
            f"{label} reaches no artifact through {artifact_id or '(none)'}, so it "
            f"carries no licence (Rule 9)"
        )
        return errors
    rights = str(artifact.get("rights_status") or "")
    if rights not in PUBLISHABLE_RIGHTS:
        errors.append(
            f"{label}: {artifact_id} is {rights or 'unstated'}, which may not be "
            f"published (Rule 9)"
        )
    if not str(artifact.get("rights_basis") or "").strip():
        errors.append(f"{label}: {artifact_id} records no rights_basis")
    return errors


def _solved_case_errors(data: dict[str, Any], where: str, known: set[str]) -> list[str]:
    errors: list[str] = []
    for ordinal, case in enumerate(data.get("solved_chapters") or (), start=1):
        if not isinstance(case, dict) or set(case) != {"token", "chapter", "passage_ids"}:
            errors.append(
                f"{where}: solved_chapters[{ordinal}] needs token, chapter and passage_ids"
            )
            continue
        for passage_id in case["passage_ids"] or ():
            if str(passage_id) not in known:
                errors.append(
                    f"{where}: solved_chapters[{ordinal}] names {passage_id}, which is "
                    f"not a fragment above"
                )
    return errors


# ---------------------------------------------------------------------------
# What the browser is given
# ---------------------------------------------------------------------------


def fragments_for_book(root: Path, token: str) -> list[dict[str, Any]]:
    """Every held fragment on a book, at its own extent, in chronological order.

    Chapter-keyed nothing: Rule 5 stores the extent and derives the view, and
    Rule 6 wants a fragment that spans chapters to appear under each of them
    once rather than be cut at the boundary. Both are properties of a reader's
    question, so both are answered in the browser from this, and no chapter
    table is written to disk for anything to disagree with.

    Rule 7's order is by the date of the text, then by author, work and extent,
    so that a tie and a missing year both sort the same way on every build.
    """
    data = load_edges(root)
    sources = load_sources(root)
    rows: list[dict[str, Any]] = []
    for fragment in data.get("fragments") or ():
        extent = _extent(fragment.get("extent"))
        if extent is None or extent.token != token:
            continue
        passage = sources.passages.get(str(fragment["passage_id"])) or {}
        work = sources.works.get(str(fragment["work_id"])) or {}
        edition_id = str(passage.get("edition_id") or "")
        edition = sources.editions.get(edition_id) or {}
        artifact = sources.artifacts.get(str(passage.get("artifact_id") or "")) or {}
        rows.append(
            {
                "id": str(fragment["passage_id"]),
                # Derived, never stored beside the work reference.
                "author": str(work.get("responsible") or ""),
                "work": str(work.get("title") or ""),
                "date": fragment.get("text_date"),
                "date_basis": str(fragment.get("text_date_basis") or ""),
                "language": str(edition.get("language") or ""),
                "edition": str(edition.get("title") or ""),
                "edition_published": str(edition.get("publication") or ""),
                "translators": list(edition.get("translators") or ()),
                "locator": str(passage.get("locus") or ""),
                "rights": str(artifact.get("rights_status") or ""),
                "basis": str(fragment.get("basis") or ""),
                "text": str(passage.get("text") or ""),
                "extent": {
                    "token": extent.token,
                    "first_chapter": extent.first_chapter,
                    "first_verse": extent.first_verse,
                    "last_chapter": extent.last_chapter,
                    "last_verse": extent.last_verse,
                },
            }
        )
    rows.sort(key=lambda row: (
        row["date"] if isinstance(row["date"], int) else 1 << 30,
        row["author"],
        row["work"],
        row["extent"]["first_chapter"],
        row["extent"]["first_verse"],
        row["id"],
    ))
    return rows


def leads_for_book(root: Path, token: str, name: str) -> dict[str, list[dict[str, str]]]:
    """L1 rows for a book, keyed by chapter, with the confidence removed.

    Rule 2 is enforced here rather than in the page. Once a work's fragments are
    held its L1 confidence is irrelevant for presence, and a confidence printed
    beside a real excerpt invites a reader to discount a text that is simply
    there. Dropping the column at generation is the same guard `bibles.json`
    uses against a licensed edition: a page cannot show what it was never sent.
    """
    index = _load_yaml(root / INDEX_RELATIVE)
    prefix = f"{name} "
    leads: dict[str, list[dict[str, str]]] = {}
    for entry in index.get("passages") or ():
        passage = str(entry.get("passage") or "")
        if not passage.startswith(prefix):
            continue
        rest = passage[len(prefix):]
        if not rest.isdigit():
            continue
        works = []
        for work in entry.get("works") or ():
            works.append(
                {
                    "author": str(work.get("author") or "Unknown"),
                    "title": str(work.get("title") or ""),
                    "date": work.get("date"),
                }
            )
        works.sort(key=lambda row: (
            row["date"] if isinstance(row["date"], int) else 1 << 30,
            row["author"],
            row["title"],
        ))
        leads[rest] = works
    return leads


def structure(root: Path = ROOT, out: Path | None = None) -> list[Path]:
    """Write what the browser fetches: one file per book, and one index.

    Additive in both directions, which `guidance/web-data.md` makes the rule
    rather than a preference. A new fragment grows one book file; a new
    translation of a fragment is another fragment in the same file; a new book
    is one more file. Nothing is keyed by chapter and nothing by translation, so
    nothing here multiplies.
    """
    out = out or (root / "src/web/data")
    written: list[Path] = []
    directory = out / "structure" / "catena"
    directory.mkdir(parents=True, exist_ok=True)
    books = canon(root)
    index: list[dict[str, Any]] = []
    for book in books:
        rows = fragments_for_book(root, book["token"])
        leads = leads_for_book(root, book["token"], book["name"])
        if not rows and not leads:
            continue
        path = directory / f"{book['token']}.json"
        path.write_text(
            json.dumps(
                {
                    "token": book["token"],
                    "name": book["name"],
                    "chapters": book["last_chapter"],
                    "numbering": _projection.CANONICAL,
                    "fragments": rows,
                    "leads": leads,
                },
                ensure_ascii=False,
                indent=1,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        written.append(path)
        index.append(
            {
                "token": book["token"],
                "name": book["name"],
                "chapters": book["last_chapter"],
                "fragments": len(rows),
            }
        )
    path = directory / "index.json"
    path.write_text(
        json.dumps(
            {
                "numbering": _projection.CANONICAL,
                "canon": books,
                "held": index,
            },
            ensure_ascii=False,
            indent=1,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    written.append(path)
    return written


# ---------------------------------------------------------------------------
# The chapter derivation, replayed where node exists
# ---------------------------------------------------------------------------

HARNESS = """
const fs = require('fs');
const path = process.argv[1];
const source = fs.readFileSync(path, 'utf8');
const module_ = { exports: {} };
new Function('module', 'exports', source)(module_, module_.exports);
const cases = JSON.parse(process.argv[2]);
const answers = cases.cases.map(function (one) {
  return module_.exports.fragmentsOnChapter(cases.fragments, one.chapter).map(
    function (fragment) { return fragment.id; }
  );
});
process.stdout.write(JSON.stringify(answers));
"""


def replay_solved_chapters(root: Path = ROOT) -> tuple[list[str], str]:
    """Run the browser's own chapter derivation over the declared cases.

    The derivation exists once, in the page's model, because the page is what
    performs it. Re-deriving it here in Python would be the second copy this
    repository keeps being bitten by, so this runs the same file instead —
    `calendar-rubrics check` does exactly this for the liturgy assembly model.
    Where node is absent the check says which verification it did not perform
    rather than passing quietly.
    """
    model = root / MODEL_RELATIVE
    if not model.is_file():
        return ([f"{MODEL_RELATIVE.as_posix()}: not found"], "")
    data = load_edges(root)
    cases = list(data.get("solved_chapters") or ())
    fragments = [
        {"id": str(fragment["passage_id"]), "extent": fragment["extent"]}
        for fragment in data.get("fragments") or ()
    ]
    payload = json.dumps({"fragments": fragments, "cases": cases})
    try:
        result = subprocess.run(
            ["node", "-e", HARNESS, str(model), payload],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return ([], "node is not installed; the chapter derivation was not replayed")
    if result.returncode != 0:
        return ([f"the chapter derivation failed: {result.stderr.strip()}"], "")
    answers = json.loads(result.stdout)
    errors = []
    for case, answer in zip(cases, answers):
        expected = [str(one) for one in case.get("passage_ids") or ()]
        if sorted(answer) != sorted(expected):
            errors.append(
                f"{case.get('token')} {case.get('chapter')}: the derivation returned "
                f"{sorted(answer)}, the solved case says {sorted(expected)}"
            )
    return (errors, "")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _check(root: Path) -> int:
    errors = validate(root)
    replay_errors, skipped = replay_solved_chapters(root)
    errors.extend(replay_errors)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"catena invalid: {len(errors)} error(s)", file=sys.stderr)
        return 1
    data = load_edges(root)
    held = len(data.get("fragments") or ())
    books = {
        str(fragment["extent"]["token"]) for fragment in data.get("fragments") or ()
    }
    print(f"catena valid: fragments={held} books={len(books)} canon={len(canon(root))}")
    if skipped:
        print(skipped)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="catena", description="Validate and derive the catena's scripture edge."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    verbs = parser.add_subparsers(dest="verb", required=True)
    verbs.add_parser("check", help="validate the edge and replay the chapter cases")
    verbs.add_parser("canon", help="print the enumerated canon as JSON")
    verbs.add_parser("titles", help="print the alias groups failing the title check")
    emit = verbs.add_parser("structure", help="write what the browser fetches")
    emit.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.verb == "check":
            return _check(root)
        if args.verb == "canon":
            print(json.dumps(canon(root), ensure_ascii=False, indent=1))
            return 0
        if args.verb == "titles":
            for author, work, reason in failing_groups(root):
                print(f"{author}\t{work}\t{reason}")
            return 0
        for path in structure(root, args.out):
            print(path.relative_to(root) if path.is_relative_to(root) else path)
        return 0
    except CatenaError as error:
        print(f"catena: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
