#!/usr/bin/env python3
"""Every document this project holds, read once from the documents themselves.

This module is the single derivation of the corpus. Four separate facts about a
publication live in four different files, and before this module each of them
was read by whichever tool happened to need it:

    src/<provider>/<leaf>/main.tex               what it is called
    src/<provider>/<leaf>/generation-metadata.tex  who contributed and when
    src/<provider>/<leaf>/web-edition.toml       whether it may be read in a browser
    release/publications/<provider>/<leaf>.json  where it is catalogued, and under
                                                 which authorization it is served

Nothing here validates. `check-generation-metadata` owns the provenance gate,
`check-web-edition` owns the eligibility gate, and `public-alpha` owns the
release gate; each of those refuses a record this module would happily read.
The division is deliberate: a validator states what a record must be, a reader
states what it says, and collapsing the two would mean a catalogue that quietly
dropped every document whose record it disliked.

## Why the title is evaluated rather than matched

A document's title is the one fact here that no single file states. Of the 186
issues this repository builds, 152 declare `pdftitle` in their own `main.tex`
and 34 do not: the Ecclesiastical Latin modules and cumulative reviews declare
`\\ModuleTitle` in `module-data.tex`, and a shared shell three `\\input`s away
composes the printed title out of it and the module's id. A regular expression
over `main.tex` therefore finds nothing for a seventh of the corpus, and a
regular expression that reached into `module-data.tex` instead would produce
`Form, Case, and Agreement` where the document is actually called
`Ecclesiastical Latin — EL-M01: Form, Case, and Agreement`.

So `title_of` walks the preamble the way the build does — following `\\input`,
recording `\\newcommand` and `\\def`, taking the branch a `\\ifdefined` selects,
and stopping at `\\begin{document}` — and expands whatever `pdftitle` finally
holds. That is more machinery than a regex, and it earns it: every one of the
186 titles and all 186 subjects it derives are byte-identical to what `pdfinfo`
reads out of the built PDF. `document-library check` performs exactly that
comparison, so a document whose preamble grows a construct this walk cannot
follow fails loudly instead of being catalogued under a plausible wrong name.

The synthesis issues are why the walk starts from an entry file rather than
always from `main.tex`. Two shapes exist in the corpus and both are current: a
`synthesis.tex` that defines `\\TriptychSynthesisEdition` and inputs `main.tex`,
which branches on it, and a `synthesis.tex` that is a standalone preamble of its
own. Evaluating from the entry file handles both without knowing which it is.

## Absence

A title that cannot be found is not filled in. The document is carried with
`title` set to None and `title_absent` saying so, and the caller prints it by
path. The count of such documents is reported on every run — including when it
is zero, which it is today — because a gap nobody counts is a gap that gets
filled the first time someone finds the blank inconvenient.
"""
from __future__ import annotations

import functools
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PDF_ROOT = ROOT / "pdf"
PUBLICATION_ROOT = ROOT / "release" / "publications"

# The two editions this project issues. A third provider directory would be a
# third edition and is not assumed anywhere: the set is read from here.
PROVIDERS = ("claude", "gpt")

MAIN = "main.tex"
SYNTHESIS = "synthesis.tex"
GENERATION_METADATA = "generation-metadata.tex"
WEB_EDITION_RECORD = "web-edition.toml"

# A leaf builds one PDF, or two where it carries a synthesis edition: the same
# document set twice, once whole and once with the appointed texts and the
# per-element sweep left out. They are issues of one document and not two
# documents, so they hang off the document rather than doubling the corpus.
FULL = "full"
SYNTHESIS_ISSUE = "synthesis"
SYNTHESIS_SUFFIX = "-synthesis"


class CorpusError(RuntimeError):
    """A document's own sources could not be read as this module expects."""


# --- Provenance ------------------------------------------------------------
#
# These declarations are the shape `check-generation-metadata` enforces, and
# they are declared here so that the gate and this reader cannot disagree about
# what a provenance record looks like. That tool imports them.

REVISION_RE = re.compile(r"^\\AIDocumentRevisionTimestamp\{([^{}]+)\}\s*$", re.MULTILINE)
CONTRIBUTION_RE = re.compile(
    r"^\\AIModelContribution\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}\s*$", re.MULTILINE
)
INHERITANCE_RE = re.compile(
    r"^\\AIInheritedGenerationMetadata\{([^{}]+)\}\s*$", re.MULTILINE
)
PRODUCTION_RE = re.compile(
    r"^\\AIGenerationProvenance"
    r"\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}\s*$",
    re.MULTILINE,
)

# The one field value that is a record rather than a value. Every consumer maps
# it to absence and none of them may guess past it.
UNKNOWN = "unknown"

# The six groups of that declaration, in the order it writes them. Named here,
# once, so the gate that enforces the record and the catalogue that publishes it
# cannot come to disagree about what its fields are called.
PRODUCTION_FIELDS = (
    "workflow_id",
    "workflow_version",
    "workflow_digest",
    "run_id",
    "seed_commit",
    "install_commit",
)


def active_tex(text: str) -> str:
    """Remove TeX comments, so a commented-out declaration states nothing."""
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


@dataclass(frozen=True)
class Contribution:
    """One model's turn at a document.

    The three groups of `\\AIModelContribution`, named as the provenance gate
    has always named them: which model, what of its configuration was exposed,
    and the agent and runtime it ran under. One vocabulary, so the gate and the
    catalogue describe the same record with the same words.
    """

    model: str
    qualifiers: str
    runtime: str


@dataclass(frozen=True)
class Production:
    """What produced a document, and what the project state was at that point.

    The six groups of `\\AIGenerationProvenance`, each either a value or None.
    None is the record the source wrote as `unknown`: the fact was not
    recoverable. It is not a default and nothing downstream may fill it in.

    ``seed_commit`` and ``install_commit`` are two different facts and neither
    substitutes for the other. A run's commit is pinned when the run is seeded
    and the engine never rechecks it against HEAD, so it states the repository
    the run was bound to. ``install_commit`` states where the produced artifact
    actually entered the tree, which for a run of any length is a later commit.

    The 187 install commits already in the corpus were backfilled from history
    rather than recorded by the run that installed them, so the derivation is
    written here in full and is reproducible from any checkout of this history:

        git log --follow --diff-filter=AM --format=%H -1 -- pdf/<leaf>.pdf

    where `<leaf>` is `<provider>/<leaf>.pdf` under `pdf/`.

    Three clauses and each is load-bearing. ``--follow`` crosses the renames
    the installed PDFs have been through — `185fb2324` renamed `doc/` to
    `pdf/`, and `6d9b74ad9` and `d7fe32ba2` renumbered the propers registries.
    ``--diff-filter=AM`` is what keeps those three commits from being the
    answer: a pure rename touches the path without installing anything, and the
    commit that installed a PDF is the last one that added or modified its
    bytes. ``-1`` takes that latest install. Run against every document in the
    corpus this reproduces all 187 recorded values and no other rule tried
    reproduces any of them.

    A leaf whose PDF is not installed has no install commit and records
    `unknown`; there is nothing to derive and nothing is invented.
    """

    workflow_id: str | None
    workflow_version: str | None
    workflow_digest: str | None
    run_id: str | None
    seed_commit: str | None
    install_commit: str | None

    @property
    def recorded(self) -> bool:
        """Whether anything at all about this document's production is known."""
        return any(
            field is not None
            for field in (
                self.workflow_id,
                self.workflow_version,
                self.workflow_digest,
                self.run_id,
                self.seed_commit,
                self.install_commit,
            )
        )


@dataclass(frozen=True)
class Provenance:
    """When a document was last revised, and by which models in which roles.

    ``inherits`` names another leaf instead of restating its contributions. Six
    documents in this corpus are set from a sibling's sources — a daily-prayer
    extract of a novena, cue cards cut from a trainer manual, a one-page
    companion to a treatise — and each records the pointer rather than a copy of
    the ledger it would otherwise have to be kept in step with. A consumer that
    wants the models follows the pointer; it is never resolved into a second
    copy here.
    """

    revised: str
    contributions: tuple[Contribution, ...]
    inherits: str | None
    produced: Production | None


def read_production(text: str, path: Path) -> Production | None:
    """Read the one production record, or None where a document states none."""
    found = PRODUCTION_RE.findall(text)
    if not found:
        return None
    if len(found) > 1:
        raise CorpusError(
            f"{path.relative_to(ROOT)}: expected one generation-provenance "
            f"record, found {len(found)}"
        )
    fields = [None if value.strip() == UNKNOWN else value.strip() for value in found[0]]
    return Production(*fields)


def read_provenance(path: Path) -> Provenance:
    text = active_tex(path.read_text(encoding="utf-8"))
    revisions = REVISION_RE.findall(text)
    if len(revisions) != 1:
        raise CorpusError(
            f"{path.relative_to(ROOT)}: expected one revision timestamp, "
            f"found {len(revisions)}"
        )
    inherits = INHERITANCE_RE.findall(text)
    return Provenance(
        revised=revisions[0],
        contributions=tuple(
            Contribution(*parts) for parts in CONTRIBUTION_RE.findall(text)
        ),
        inherits=inherits[0] if inherits else None,
        produced=read_production(text, path),
    )


# --- The workflows now declared --------------------------------------------
#
# Drift is a comparison, and this is its right-hand side: what the pipelines
# say today. It is read from the tracked pipeline definitions and from nothing
# else — not from a run, and not from HEAD — because the catalogue it lands in
# must be byte-reproducible from the tree, and a commit-derived value would
# make `document-library structure --check` fail on every commit that followed.
#
# Two facts travel, not one, because they answer two different questions and
# only one of them is maintained by hand.
#
#   `version` is an integer somebody types. It moves when an operator decides a
#   run bound to the old number must be seeded again. Nothing forces it.
#
#   `digest` is `WorkflowEngine.workflow_source_digest`: the pipeline JSON plus
#   the bytes of every fragment and every schema the pipeline references. It
#   moves the instant any of that guidance is edited, whether or not anyone
#   remembered the version.
#
# Carrying only the version meant that the stated purpose of this comparison —
# knowing which documents were produced under guidance that has since changed —
# was not met: a fragment could be rewritten and every document still read as
# current. The digest is the fact that actually answers it. It is a pure
# function of tracked bytes, so it keeps this catalogue byte-reproducible.

PIPELINE_ROOT = ROOT / "workflows" / "pipelines"
WORKFLOW_ROOT = ROOT / "workflows"


@dataclass(frozen=True)
class Workflow:
    identifier: str
    version: str
    digest: str | None


def _source_digest(definition: dict, workflow_root: Path) -> str | None:
    """The workflow-source digest of one pipeline, or None where it cannot be had.

    The engine owns the recipe. Recomputing it here would be a second
    derivation of the value a run binds itself to, and the two would differ the
    first time the recipe changed.
    """
    scripts = str(Path(__file__).resolve().parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    try:
        from _workflow import WorkflowEngine, WorkflowError
    except ImportError:  # pragma: no cover - the engine is part of this repo
        return None
    engine = WorkflowEngine(ROOT, workflow_root)
    try:
        return engine.workflow_source_digest(definition)
    except (WorkflowError, KeyError, OSError):
        # A pipeline whose fragments or schemas cannot be read has no digest.
        # That is an absence and is written as one; it is never filled in, and
        # `declared_workflows` refuses a pipeline that states no identity at
        # all, so a missing digest cannot be mistaken for a missing workflow.
        return None


def declared_workflows(root: Path | None = None) -> tuple[Workflow, ...]:
    """Every pipeline this repository currently declares, with version and digest.

    A pipeline that states no `id` or no `version` is refused rather than
    skipped. Skipping it was how the whole comparison could go dark with every
    check green: an unreadable or malformed definition removed the right-hand
    side, every verdict fell silent, and silence is what this file says a
    document with no recorded origin looks like. The two are not the same, so
    they may not produce the same output.
    """
    where = PIPELINE_ROOT if root is None else root
    workflow_root = WORKFLOW_ROOT if root is None else where.parent
    if not where.is_dir():
        raise CorpusError(
            f"no workflow pipelines beneath {where}; the drift comparison has "
            f"no right-hand side and cannot be made"
        )
    found: list[Workflow] = []
    for path in sorted(where.glob("*.json")):
        try:
            definition = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CorpusError(f"cannot read {path}: {error}") from error
        identifier = definition.get("id")
        version = definition.get("version")
        if identifier is None or version is None:
            raise CorpusError(
                f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: "
                f"a pipeline must declare both `id` and `version`; a definition "
                f"missing either would silently remove one side of every "
                f"drift comparison"
            )
        found.append(
            Workflow(
                identifier=str(identifier),
                version=str(version),
                digest=_source_digest(definition, workflow_root),
            )
        )
    if not found:
        raise CorpusError(
            f"no workflow pipeline in {where} declares an identity; the drift "
            f"comparison has no right-hand side and cannot be made"
        )
    return tuple(found)


# --- The title, evaluated --------------------------------------------------

_STEP = re.compile(
    # \input{...} and \include{...}
    r"\\(?:input|include)\s*\{(?P<input>[^{}]*)\}"
    # \newcommand{\Name}, \newcommand\Name, \renewcommand..., \providecommand...
    r"|\\(?:new|renew|provide)command\s*(?:\{\\(?P<defined>[A-Za-z@]+)\}"
    r"|\\(?P<bare>[A-Za-z@]+))"
    # \def\Name
    r"|\\def\s*\\(?P<deffed>[A-Za-z@]+)"
    r"|\\hypersetup\s*(?P<hypersetup>\{)"
    # Conditionals. Only \ifdefined and \ifundefined are evaluated; every other
    # \if is tracked so that its \else and \fi cannot be mistaken for one of
    # theirs, and both of its branches are read, since none of them has ever
    # guarded a title and a wrongly skipped branch is worse than a read one.
    r"|\\(?P<conditional>if[a-zA-Z@]*)\b\s*(?:\\(?P<tested>[A-Za-z@]+))?"
    r"|\\(?P<otherwise>else)\b"
    r"|\\(?P<end>fi)\b"
    r"|\\begin\s*\{(?P<document>document)\}"
)
_MACRO_REFERENCE = re.compile(r"\\([A-Za-z@]+)\s?")
_PDF_KEY = re.compile(r"\bpdf(title|subject)\s*=\s*")
_EVALUATED_CONDITIONALS = ("ifdefined", "ifundefined")
_INPUT_DEPTH_LIMIT = 24
_EXPANSION_ROUNDS = 8


def _brace_group(text: str, start: int) -> tuple[str, int]:
    """Return the balanced group beginning at ``text[start] == '{'``, and its end."""
    if text[start : start + 1] != "{":
        raise CorpusError("expected a brace group")
    depth, index = 0, start
    while index < len(text):
        character = text[index]
        if character == "\\":
            index += 2
            continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
        index += 1
    raise CorpusError("unbalanced brace group")


def _skip_optional(text: str, index: int) -> int:
    """Advance past whitespace and any ``[n]`` arguments a definition carries."""
    while True:
        while index < len(text) and text[index] in " \t\n":
            index += 1
        if text[index : index + 1] != "[":
            return index
        closing = text.find("]", index)
        if closing < 0:
            return index
        index = closing + 1


def expand(value: str, macros: dict[str, str]) -> str:
    """Substitute recorded macros until the value stops changing."""
    for _ in range(_EXPANSION_ROUNDS):
        if not _MACRO_REFERENCE.search(value):
            return value
        substituted = _MACRO_REFERENCE.sub(
            lambda match: macros.get(match.group(1), match.group(0)), value
        )
        if substituted == value:
            return value
        value = substituted
    return value


class _Reached(Exception):
    """`\\begin{document}`: everything the preamble had to say has been said."""


@dataclass
class _Walk:
    """The state one preamble evaluation carries across its `\\input` chain."""

    provider: str
    macros: dict[str, str]
    values: dict[str, str]
    origins: dict[str, Path]
    templates: dict[str, str]
    # One entry per open conditional: True while the branch being read is taken.
    frames: list[bool]

    @property
    def emitting(self) -> bool:
        return all(self.frames)


def _resolve_input(argument: str, provider: str) -> Path | None:
    """Resolve one `\\input` the way the build's ``TEXINPUTS`` does."""
    candidate = Path(argument)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    for base in (SRC / provider, SRC):
        for path in (base / argument, base / f"{argument}.tex"):
            if path.is_file():
                return path
    return None


def _walk(path: Path, walk: _Walk, depth: int = 0) -> None:
    if depth > _INPUT_DEPTH_LIMIT:
        raise CorpusError(f"{path.relative_to(ROOT)}: input nesting is too deep")
    text = active_tex(path.read_text(encoding="utf-8"))
    index = 0
    while (match := _STEP.search(text, index)) is not None:
        index = match.end()
        if match.group("input") is not None:
            if not walk.emitting:
                continue
            target = _resolve_input(expand(match.group("input").strip(), walk.macros), walk.provider)
            # The shared preamble sets no title and pulls in the whole package
            # list; skipping it is what keeps this walk to the leaf's own text.
            if target is not None and target.stem != "preamble":
                _walk(target, walk, depth + 1)
            continue

        name = match.group("defined") or match.group("bare") or match.group("deffed")
        if name is not None:
            cursor = _skip_optional(text, index)
            if text[cursor : cursor + 1] != "{":
                continue
            body, index = _brace_group(text, cursor)
            if walk.emitting:
                walk.macros[name] = body
            continue

        if match.group("hypersetup") is not None:
            body, index = _brace_group(text, match.end() - 1)
            if walk.emitting:
                _read_hypersetup(body, path, walk)
            continue

        conditional = match.group("conditional")
        if conditional is not None:
            if conditional in _EVALUATED_CONDITIONALS:
                defined = match.group("tested") in walk.macros
                walk.frames.append(defined if conditional == "ifdefined" else not defined)
            else:
                walk.frames.append(True)
            continue

        if match.group("otherwise") is not None:
            if walk.frames:
                walk.frames[-1] = not walk.frames[-1]
            continue

        if match.group("end") is not None:
            if walk.frames:
                walk.frames.pop()
            continue

        if match.group("document") is not None and walk.emitting:
            raise _Reached


def _read_hypersetup(body: str, path: Path, walk: _Walk) -> None:
    for key in _PDF_KEY.finditer(body):
        field = key.group(1)
        if body[key.end() : key.end() + 1] == "{":
            value, _ = _brace_group(body, key.end())
        else:
            cut = body.find(",", key.end())
            value = body[key.end() : cut if cut >= 0 else len(body)]
        walk.templates[field] = value.strip()
        walk.values[field] = expand(value.strip(), walk.macros)
        walk.origins[field] = path


@dataclass(frozen=True)
class Title:
    """What a document is called, and where that came from.

    ``template`` is written only when the declared value was composed out of
    macros, because a template identical to the title is a restatement that can
    later disagree with it. ``absent`` carries the reason in place of a title
    the sources do not state; exactly one of ``text`` and ``absent`` is set.
    """

    text: str | None
    subject: str | None
    source: str | None
    template: str | None
    absent: str | None


NO_TITLE = "no pdftitle is declared anywhere in this document's own sources"


def title_of(entry: Path, provider: str) -> Title:
    """Evaluate ``entry``'s preamble and return the title it finally declares."""
    walk = _Walk(
        provider=provider, macros={}, values={}, origins={}, templates={}, frames=[]
    )
    try:
        _walk(entry, walk)
    except _Reached:
        pass
    text = walk.values.get("title")
    if text is None:
        return Title(None, None, None, None, NO_TITLE)
    template = walk.templates.get("title")
    origin = walk.origins["title"]
    return Title(
        text=text,
        subject=walk.values.get("subject") or None,
        source=origin.relative_to(ROOT).as_posix(),
        template=template if template != text else None,
        absent=None,
    )


# --- The built PDF ---------------------------------------------------------
#
# The only fact here that no source file states. `pdfinfo` is already required
# by `make check-tools` and used by `check-generation-metadata`, so this adds no
# dependency; a checkout without it gets a stated refusal rather than a
# catalogue whose extents are quietly missing.

PDFINFO = "pdfinfo"
NO_PDF = "no PDF is installed for this issue"


@dataclass(frozen=True)
class PdfMetadata:
    pages: int
    title: str
    subject: str


class PdfInfoUnavailable(CorpusError):
    pass


def read_pdf(path: Path) -> PdfMetadata:
    """Read one built PDF's page count and its own title and subject."""
    try:
        completed = subprocess.run(
            [PDFINFO, str(path)], capture_output=True, text=True, check=False
        )
    except FileNotFoundError as error:  # pragma: no cover - environment-dependent
        raise PdfInfoUnavailable(
            f"{PDFINFO} is not installed; it is required to read a document's extent"
        ) from error
    if completed.returncode != 0:
        raise CorpusError(
            f"{PDFINFO} failed for {path.relative_to(ROOT)}: {completed.stderr.strip()}"
        )
    fields: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        label, separator, value = line.partition(":")
        if separator:
            fields.setdefault(label.strip(), value.strip())
    try:
        pages = int(fields.get("Pages", ""))
    except ValueError as error:
        raise CorpusError(
            f"{PDFINFO} reported no page count for {path.relative_to(ROOT)}"
        ) from error
    return PdfMetadata(
        pages=pages, title=fields.get("Title", ""), subject=fields.get("Subject", "")
    )


# --- Records the gates own -------------------------------------------------


def read_web_edition(path: Path) -> dict:
    """Read one leaf's web-edition declaration. `check-web-edition` validates it."""
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise CorpusError(f"cannot read {path.relative_to(ROOT)}: {error}") from error


def read_publication(path: Path) -> dict:
    """Read one publication's release record. `public-alpha` validates it."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CorpusError(f"cannot read {path.relative_to(ROOT)}: {error}") from error


def eligible_document_ids(source_root: Path | None = None) -> set[tuple[str, str]]:
    """Every leaf whose own record declares a publishable web edition.

    The release builder reads this rather than globbing the records a second
    time: the set decides which pages the artifact renders, and two walks of the
    same records would be two answers waiting to differ.

    The tree is the caller's, not this module's. That is not a courtesy — the
    release tool's tests repoint its root at a fixture and then ask it what it
    would publish, and a walk that answered from the real checkout instead would
    hand a fixture the whole corpus and pass while doing it.
    """
    root = SRC if source_root is None else source_root
    eligible: set[tuple[str, str]] = set()
    for record_path in sorted(root.glob(f"*/**/{WEB_EDITION_RECORD}")):
        if read_web_edition(record_path).get("eligibility") != "eligible":
            continue
        relative = record_path.parent.relative_to(root)
        eligible.add((relative.parts[0], "/".join(relative.parts[1:])))
    return eligible


# --- One document ----------------------------------------------------------


@dataclass(frozen=True)
class Issue:
    """One PDF a document builds: the whole of it, or its synthesis edition."""

    kind: str
    stem: str
    entry: str
    title: Title
    pdf: str | None
    pdf_absent: str | None
    pages: int | None
    status: str | None
    authorization: str | None


@dataclass(frozen=True)
class Document:
    """One provider's edition of one work, with everything recorded about it."""

    provider: str
    leaf: str
    section: str
    catalog: str | None
    provenance: Provenance
    eligibility: str
    reviewed: str
    basis: str | None
    rationale: str | None
    blocking_constructs: tuple[str, ...]
    web_page: str | None
    issues: tuple[Issue, ...]

    @property
    def key(self) -> tuple[str, str]:
        return (self.provider, self.leaf)

    @property
    def pages(self) -> int | None:
        """The extent of the whole document; a synthesis is a cut of it, not more."""
        return next((issue.pages for issue in self.issues if issue.kind == FULL), None)

    @property
    def models(self) -> tuple[str, ...]:
        """Each model that contributed, once, in the order it first appears."""
        seen: dict[str, None] = {}
        for contribution in self.provenance.contributions:
            seen.setdefault(contribution.model, None)
        return tuple(seen)


def _issues_of(directory: Path, provider: str, leaf: str, extents: bool) -> tuple[Issue, ...]:
    entries = [(FULL, directory / MAIN, leaf)]
    if (directory / SYNTHESIS).is_file():
        entries.append((SYNTHESIS_ISSUE, directory / SYNTHESIS, leaf + SYNTHESIS_SUFFIX))

    issues = []
    for kind, entry, stem in entries:
        pdf = PDF_ROOT / provider / f"{stem}.pdf"
        built = pdf.is_file() and not pdf.is_symlink()
        record_path = PUBLICATION_ROOT / provider / f"{stem}.json"
        record = read_publication(record_path) if record_path.is_file() else {}
        issues.append(
            Issue(
                kind=kind,
                stem=stem,
                entry=entry.relative_to(ROOT).as_posix(),
                title=title_of(entry, provider),
                pdf=pdf.relative_to(ROOT).as_posix() if built else None,
                pdf_absent=None if built else NO_PDF,
                pages=read_pdf(pdf).pages if built and extents else None,
                status=record.get("status"),
                authorization=record.get("authorization"),
            )
        )
    return tuple(issues)


def _catalog_of(provider: str, leaf: str) -> str | None:
    record_path = PUBLICATION_ROOT / provider / f"{leaf}.json"
    if not record_path.is_file():
        return None
    return read_publication(record_path).get("catalog")


@functools.lru_cache(maxsize=8)
def documents(
    *, providers: tuple[str, ...] = PROVIDERS, extents: bool = True
) -> tuple[Document, ...]:
    """Read every document under the given providers, in (provider, leaf) order.

    ``extents=False`` skips the `pdfinfo` pass, which is the only part of this
    that shells out. A caller that wants names and authorship and not page
    counts should use it; a caller that wants to compare against the built PDF
    must not.

    Memoized per argument pair. With ``extents=True`` this starts one `pdfinfo`
    per document --- 188 processes, 1.37s --- and the test suite asks for the
    same catalogue about eight times in a run. Both arguments are hashable and
    `Document` is a frozen dataclass in a tuple, so the cached answer cannot be
    edited by one caller under another. It caches for the life of a process: a
    long-lived one that rebuilds a PDF and expects a new page count from the
    same process must call `documents.cache_clear()`, which no caller does
    today because every one of them is a short-lived command.
    """
    found: list[Document] = []
    for provider in providers:
        if provider not in PROVIDERS:
            raise CorpusError(f"unknown provider: {provider}")
        root = SRC / provider
        for main in sorted(root.glob(f"**/{MAIN}")):
            directory = main.parent
            leaf = directory.relative_to(root).as_posix()
            record_path = directory / WEB_EDITION_RECORD
            if not record_path.is_file():
                raise CorpusError(
                    f"{main.relative_to(ROOT)}: no {WEB_EDITION_RECORD} beside it"
                )
            record = read_web_edition(record_path)
            metadata = directory / GENERATION_METADATA
            if not metadata.is_file():
                raise CorpusError(
                    f"{main.relative_to(ROOT)}: no {GENERATION_METADATA} beside it"
                )
            eligibility = str(record.get("eligibility", ""))
            web = ROOT / "web" / provider / f"{leaf}.md"
            found.append(
                Document(
                    provider=provider,
                    leaf=leaf,
                    section=leaf.split("/")[0],
                    catalog=_catalog_of(provider, leaf),
                    provenance=read_provenance(metadata),
                    eligibility=eligibility,
                    reviewed=str(record.get("reviewed", "")),
                    basis=record.get("basis"),
                    rationale=record.get("rationale"),
                    blocking_constructs=tuple(record.get("blocking_constructs") or ()),
                    web_page=(
                        f"web/{provider}/{leaf}.html"
                        if eligibility == "eligible" and web.is_file()
                        else None
                    ),
                    issues=_issues_of(directory, provider, leaf, extents),
                )
            )
    return tuple(found)
