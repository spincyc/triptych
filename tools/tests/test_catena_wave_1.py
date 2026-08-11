#!/usr/bin/env python3
"""The Catena Omnia page after the Wave 1 (E0) composition and its E1 corrections.

The composition is a stylesheet-led change over classes the page already
emitted, plus bounded operations in `catena.js` and one static disclosure in
`index.html`. The independent review of the first E1 candidate (roadmap,
2026-08-10) required corrections, and each route-owned one is pinned here by
its own test class:

  Finding 2   ChronologyTest — grouping by author alone filed Augustine's 417
              work under a heading dated 401, ahead of Severian's 401; only a
              contiguous author+date run may share a heading.
  Finding 3   LeadsCopyTest — the acquisition list overlaps held works in the
              generated data, so the page may not claim "not yet acquired" or
              "no text of any of them is held"; the copy asserts no more than
              the record proves.
  Finding 4   RightsRenderingTest — every rights/printing/attribution fact the
              payload supplies is rendered (edition_published carries the
              Voicu/BBAW attribution today), an acknowledgement renders ABOVE
              the prose through ONE channel, no supplied field suppresses
              another, malformed values fail safely, and a bare
              `rights: "licensed"` prints truthfully and no more.
  Finding 5   HashValidationTest, VoiceDeepLinkTest, HistoryDeterminismTest —
              typed validation of all four hash keys on cold load and
              hashchange (whole-key voice soundness, chapter ranged against
              the book the page would resolve), failing closed with the URL
              left as written and recovery offered; the deferred-voice deep
              link; deterministic Back/Forward through a route-owned
              hashchange comparison, with arrival normalisation that never
              pushes a history entry.
  Finding 6   StaticDocumentTruthTest, PrintStylesTest, CompositionTest — the
              static document is true without scripts (no permanent Loading,
              no static aria-busy, a real browse entry), narrow enhancement is
              synchronous, and print hides interaction chrome while naming
              itself non-canonical.
  Finding 7   ForcedColorsTest — the reserved paragraph edge forces to Canvas
              and only `.projected` takes CanvasText.
  Finding 8   VoiceCountTruthTest, AbsenceCountTest, ParagraphCountTest,
              AuthorFilterRecoveryTest, IntegrityErrorTest — counts and states
              derive from the typed record, never from a filtered count; an
              expected spine 404 is an error, not an absence; a filter can
              never strand the reader.

The correction independent review of 2026-08-11 (CHANGES REQUIRED at head
`dfc636665`) demanded a second pass over finding 5 and the route-local
robustness findings; those corrections are pinned by their own classes:

  UrlGrammarClosureTest    — the complete multimap: duplicate recognized
              keys refused (identical or contradictory, per the
              reader-state contract), malformed percent-encoding failing
              the closed value grammars, whole-key voice closure.
  HistoryIndependenceTest  — one invalid URL renders ONE page, however it
              arrives; no value borrowed from leftover controls.
  RecoveryFocusTest        — invalid->valid recovery restores focus and
              announces exactly once, by link and by control.
  AsyncTransactionTest     — deferred-request races: stale successes and
              stale failures may not commit; a current failure owns its
              route and its address; rapid A->B->C commits only C.
  CacheRecoveryTest        — rejected loads are evicted, so retry is real.
  BootstrapFailureTest     — index/manifest failures leave no permanent
              "Loading…" and speak once.
  ChronologyTest           — strengthened to exact fragment identity,
              exactly once, in spine order.

The second bounded pass (this one) repairs the remaining route-owned truth
defects the same review recorded, each pinned by its own class:

  TypedTruthStateTest      — ONE typed state (finding 8): blocked-but-held
              is HELD, "nothing held" appears only when nothing is held at
              all, and integrity/invalid/failed states manufacture no
              absence labels ("none here", "none in", empty copy, leads).
  LeadsCopyTest            — (finding 3, route half) rows are unreconciled
              lead entries; the omitted confidence is disclosed; exact row
              identity and order are pinned, not counts.
  RightsRenderingTest, SeverianRightsTraceTest — (finding 4, route half)
              no browser-side precedence: every supplied valid nonempty
              typed field renders; malformed values fail safely; ONE
              point-of-use acknowledgement channel absorbs late payloads
              without duplication; real Severian CC BY-SA metadata is
              traced payload -> route -> rendered acknowledgement.
  AbsenceDisclosureTest    — translation-absence findings are not deferred:
              the disclosure stands open on arrival.

Two independent adversarial audits of this candidate (2026-08-11, R1 and R2)
then drove the page against attacks these tests did not try; each route-owned
finding they returned is repaired and pinned here by its own class, over the
audit's own repro:

  R1-F1  RecoveryFailureFocusTest — the failure arm of `render()` restored no
              focus, so a keyboard recovery whose recovered route failed to
              load left focus on the anchor the failure had removed.
  R1-F2  SupersededArrivalVoiceTest — a deep-linked voice parked by an
              arrival that a reader action then superseded leaked into the
              reader's own render, selection and pushed address.
  R2-F1  SelfWriteEchoTest — the page's own hash write, echoed back one task
              later, was judged against the CURRENT controls; a reader who
              had already moved was reverted to the route the echo named.
  R2-F2  BlockedVoiceClaimTest — (with R1-F4) a standing blocked row of
              unrecorded voice still permitted "— none here", "none in X" and
              an unqualified "No commentary ... is held in X".
  R2-F3/F4/F5  MalformedRecordRenderingTest — the payload body, the lead rows
              and the blocked rows were untyped sinks: "[object Object]" for
              prose, "Date — 42" for apparatus, "undefined — undefined" for
              an author.
  R2-O1  AcknowledgementChannelOrderTest — a malformed spine acknowledgement
              claimed the one channel and erased a valid payload one.

The replay proves behaviour by RUNNING THE PAGE under node — the real
`browser-core.js`, the real `catena-model.js`, the real `catena.js`, against
the repository's own corpus with a stub document and network — rather than by
matching strings in the source. Assertions that only read source text are the
fallback for what a replay cannot reach (static markup, stylesheet blocks).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
CATENA = BROWSER / "catena"
NODE = shutil.which("node")

# `catena-model.js`, byte for byte. The model is UMD and DOM-free, is replayed
# under node by `scripts/_catena.py check`, and no part of E1 touches it: a
# deliberate model change is a deliberate change to this literal. The digest
# is of the tracked file itself — release bindings are the release owner's.
MODEL_SHA256 = "f1ea94f9ec6b54813859c2b526163e90d9de61992b839fe2eb0e349f31ccf57b"

# gzip -9, whole file, mtime pinned to zero. These are the recorded E1
# ceilings — the first candidate raised them to 8,600/13,400 without a waiver
# and the review declined that; the corrected composition fits the originals.
CSS_BUDGET_GZ = 8_000
JS_BUDGET_GZ = 13_000
# The same files with comments stripped: what the composition itself costs.
# Base at main 9b9ff74a7: css 1,813 / js 6,450. The growth is the accepted
# composition plus the correction work this file pins (typed hash validation
# for all four keys, integrity errors, rights facts, chronology grouping,
# filter recovery, route-owned history with arrival replaceState, print and
# forced-colors blocks).
CSS_RULES_BUDGET_GZ = 2_700
JS_CODE_BUDGET_GZ = 8_800

# The review's protected distinctions. The composition deliberately specifies
# no treatment for the `.absence-*` selectors (they render in the page's
# inherited sans and ink — undeclared is the state to protect), and the rest
# keep the section's own palette so they read APART from held commentary.
PROTECTED_SELECTORS = (
    ".absence-note",
    ".absence-list",
    ".absence-reason",
    ".absence-partial",
    ".paragraph-note",
    ".passage-paragraph.projected",
    ".aside-note",
    ".fragment-basis",
    ".spans",
)

PROTECTED_AND_DECLARED = (
    ".paragraph-note",
    ".passage-paragraph.projected",
    ".aside-note",
    ".fragment-basis",
    ".spans",
)


def held(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def without_comments(text: str, *, script: bool = False) -> str:
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if script:
        stripped = re.sub(r"^\s*//.*$", "", stripped, flags=re.M)
    return stripped


def gz(text: str) -> int:
    return len(gzip.compress(text.encode("utf-8"), 9, mtime=0))


def declarations_for(css: str, selector: str) -> list[str]:
    """Every declaration block whose selector list names this exact selector."""
    found: list[str] = []
    for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(css)):
        names = [one.strip() for one in block.group(1).split(",")]
        if any(name == selector or name.endswith(" " + selector) for name in names):
            found.append(block.group(2))
    return found


def media_block(css: str, prelude: str) -> str:
    """The body of one `@media` block, brace-balanced."""
    start = css.index(prelude)
    open_at = css.index("{", start)
    depth = 0
    for at in range(open_at, len(css)):
        if css[at] == "{":
            depth += 1
        elif css[at] == "}":
            depth -= 1
            if depth == 0:
                return css[open_at + 1:at]
    raise AssertionError(f"unbalanced media block at {prelude!r}")


# --------------------------------------------------------------------- replay

# A chapter file carrying a `blocked` entry. EXPLICITLY SYNTHETIC: every
# tracked chapter file carries an empty `blocked` array, so the renderer has
# never fired on real data. It is tested anyway — defensively — because the
# distinction between "never acquired" and "held, and not renderable" is one
# the review protected; the real fixture is the generator's to supply, and
# this one is never served.
BLOCKED_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "fragments": [],
    "sources": {},
    # The second lead row is LOW-INFORMATION on purpose: no author, no
    # date. A row this thin must render only what it carries and never a
    # stronger claim.
    "leads": [{"author": "Origen", "title": "Homiliae in Genesim", "date": 240},
              {"title": "Fragmenta incerta"}],
    "blocked": [
        {
            "author": "Anonymous",
            "work": "Catena in Genesim",
            "reason": "the witness is held only as page images, and no text has been read off them",
        }
    ],
    "refusals": {},
}

# EXPLICITLY SYNTHETIC licence fixture. The corpus today reduces the Severian
# CC BY-SA terms to `rights: "licensed"` — projecting the full metadata is a
# recorded generator prerequisite — so the renderer's acknowledgement /
# attribution / rights_basis handling can only be proved against a labelled
# fixture. Nothing here asserts the corpus already carries these fields.
LICENCE_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
        "0": {
            "author": "Synthetic Author",
            "work": "Synthetic Work",
            "work_id": "work.synthetic",
            "date": 401,
            "language": "grc",
            "voice": "original",
            "rights": "CC BY-SA 4.0",
            "edition": "Synthetic Edition",
            "edition_published": "Synthetic Press, 2018",
            "translators": [],
            "container": "",
            "acknowledgement": "Greek text by A. Editor, CC BY-SA 4.0; share alike.",
            "attribution": "Attribution: A. Editor, Synthetic Academy",
            "rights_basis": "Recorded basis, rendered beside the acknowledgement.",
        },
        "1": {
            "author": "Second Author",
            "work": "Second Work",
            "work_id": "work.second",
            "date": 500,
            "language": "la",
            "voice": "original",
            "rights": "licensed",
            "edition": "Second Edition",
            "edition_published": "",
            "translators": [],
            "container": "",
            "rights_basis": "printed because no acknowledgement is recorded",
        },
        "2": {
            "author": "Third Author",
            "work": "Third Work",
            "work_id": "work.third",
            "date": 600,
            "language": "la",
            "voice": "original",
            "rights": "licensed",
            "edition": "Third Edition",
            "edition_published": "",
            "translators": [],
            "container": "",
            "acknowledgement": "Only an acknowledgement, no basis.",
        },
        # Malformed typed values: a numeric basis, an object acknowledgement
        # and a whitespace attribution must fail safely — never guessed into
        # a legal status, never printed as facts, never hiding `rights`.
        "3": {
            "author": "Fourth Author",
            "work": "Fourth Work",
            "work_id": "work.fourth",
            "date": 700,
            "language": "la",
            "voice": "original",
            "rights": "licensed",
            "edition": "Fourth Edition",
            "edition_published": "",
            "translators": [],
            "container": "",
            "rights_basis": 12345,
            "acknowledgement": {"broken": True},
            "attribution": "   ",
        },
    },
    "fragments": [
        {
            "id": "synthetic-ack",
            "locator": "1",
            "source": "0",
            "review": "inspected",
            "text_words": 4,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 1,
                       "last_chapter": 1, "last_verse": 1},
        },
        {
            "id": "synthetic-late",
            "locator": "2",
            "source": "1",
            "review": "inspected",
            "text_words": 2,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 2,
                       "last_chapter": 1, "last_verse": 2},
        },
        {
            "id": "synthetic-ack-only",
            "locator": "3",
            "source": "2",
            "review": "inspected",
            "text_words": 2,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 3,
                       "last_chapter": 1, "last_verse": 3},
        },
        {
            "id": "synthetic-malformed",
            "locator": "4",
            "source": "3",
            "review": "inspected",
            "text_words": 2,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 4,
                       "last_chapter": 1, "last_verse": 4},
        },
    ],
    "leads": [],
    "blocked": [],
    "refusals": {},
}

# EXPLICITLY SYNTHETIC malformed-record fixture, for the adversarial audit's
# defensive-rendering findings (R2 F3/F4/F5). Every tracked lead and blocked
# array is either empty or well typed, and no tracked payload is malformed, so
# these shapes can only be driven from a labelled fixture. A sound row stands
# beside the broken ones in each list: the guards must withhold garbage without
# withholding what the record really carries.
MALFORMED_RECORD_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
        "0": {
            "author": "Sound Author", "work": "Sound Work",
            "work_id": "work.sound", "date": 401, "language": "la",
            "voice": "original", "rights": "public-domain",
            "edition": "Sound Edition", "edition_published": "",
            "translators": [], "container": "",
        },
    },
    "fragments": [
        {
            "id": "malformed-payload", "locator": "1", "source": "0",
            "review": "inspected", "text_words": 3,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 1,
                       "last_chapter": 1, "last_verse": 1},
        },
    ],
    "leads": [
        {"author": 42, "title": {"broken": True}, "date": [1, 2]},
        {"title": None},
        {"author": "Origen", "title": "Homiliae in Genesim", "date": 240},
    ],
    "blocked": [
        {"author": None, "work": 42},
        {"reason": {"broken": True}},
        {"author": "Anonymous", "work": "Catena in Genesim",
         "reason": "held only as page images"},
    ],
    "refusals": {},
}

# EXPLICITLY SYNTHETIC acknowledgement-order fixture (adversarial audit R2,
# observation O1). Two fragments, each with a spine acknowledgement and a
# payload acknowledgement of opposite soundness: a malformed note may be said
# to be broken, once, without claiming the one channel and erasing the valid
# note the other supply carries — and a valid note already rendered is never
# displaced by a malformed one arriving later.
ACK_ORDER_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
        "0": {
            "author": "Broken Spine Author", "work": "First Work",
            "work_id": "work.broken-spine", "date": 401, "language": "la",
            "voice": "original", "rights": "licensed",
            "edition": "First Edition", "edition_published": "",
            "translators": [], "container": "",
            "acknowledgement": {"broken": True},
        },
        "1": {
            "author": "Sound Spine Author", "work": "Second Work",
            "work_id": "work.sound-spine", "date": 500, "language": "la",
            "voice": "original", "rights": "licensed",
            "edition": "Second Edition", "edition_published": "",
            "translators": [], "container": "",
            "acknowledgement": "Spine licence note, share alike.",
        },
    },
    "fragments": [
        {
            "id": "ack-payload-valid", "locator": "1", "source": "0",
            "review": "inspected", "text_words": 2,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 1,
                       "last_chapter": 1, "last_verse": 1},
        },
        {
            "id": "ack-payload-broken", "locator": "2", "source": "1",
            "review": "inspected", "text_words": 3,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 2,
                       "last_chapter": 1, "last_verse": 2},
        },
    ],
    "leads": [],
    "blocked": [],
    "refusals": {},
}

# The REAL Severian/PTA rights record: the tracked edition file carries the
# CC BY-SA 4.0 licence basis with the Voicu / von Stockhausen / BBAW
# attribution, while the generated catena spine still reduces it to
# `rights: "licensed"` (a recorded generator prerequisite). The trace below
# drives the real string — not an invented one — through payload, route and
# rendered point-of-use acknowledgement.
SEVERIAN_EDITION = json.loads(
    (Path(__file__).resolve().parents[2] /
     "src/web/data/structure/sources/editions/severian-of-gabala/"
     "in-cosmogoniam-homiliae/2018-pta-grc1-2018.json").read_text(encoding="utf-8"))
SEVERIAN_BASIS = SEVERIAN_EDITION["artifacts"][0]["rights_basis"]

GEN1 = "#book=Gen&chapter=1&bible=douay-rheims"
GEN2 = "#book=Gen&chapter=2&bible=douay-rheims"
GEN3 = "#book=Gen&chapter=3&bible=douay-rheims"
GEN42 = "#book=Gen&chapter=42&bible=douay-rheims"
# Genesis 10 holds 71 fragments, every one in its author's own Latin.
GEN10_ENGLISH = "#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en"

SCENARIOS = [
    {"name": "default", "hash": GEN1,
     "steps": [{"do": "openFirstFragment", "label": "opened"}]},
    {"name": "voice-held", "hash": GEN1 + "&voice=translation:en"},
    {"name": "voice-not-held", "hash": GEN1 + "&voice=translation:de"},
    # Genesis 10 holds 71 fragments, every one in its author's own Latin: the
    # selected-empty-voice chapter finding 8 demands be told truthfully.
    {"name": "voice-empty-chapter", "hash": GEN10_ENGLISH},
    {"name": "numbering-refusal", "hash": "#book=Ps&chapter=13&bible=king-james-version"},
    {"name": "acquisition-only", "hash": "#book=Ex&chapter=3&bible=douay-rheims"},
    # Exodus 1 is absent from the index's `present` list: no spine is asked for.
    {"name": "nothing-held", "hash": "#book=Ex&chapter=1&bible=douay-rheims"},
    {"name": "narrow", "hash": GEN1, "narrow": True},
    # The corpus's only single-commentator chapter.
    {"name": "one-commentator", "hash": GEN42},
    {"name": "held-unrenderable", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": BLOCKED_FIXTURE}},
    # The real licensed source: six Severian/PTA fragments under rights
    # "licensed", their attribution carried today in edition_published.
    {"name": "severian-open", "hash": GEN1,
     "steps": [{"do": "openFragmentOf", "author": "Severian of Gabala", "label": "opened"}]},
    {"name": "synthetic-licence", "hash": GEN1,
     "files": {
         "structure/catena/01-gen/001.json": LICENCE_FIXTURE,
         # The first source's payload carries a SECOND acknowledgement: the
         # one canonical channel must render exactly one block, the spine's.
         "structure/catena/text/synthetic-ack.json":
             {"id": "synthetic-ack", "text": "Synthetic words one.",
              "acknowledgement": "Payload duplicate that must not render twice."},
         "structure/catena/text/synthetic-late.json":
             {"id": "synthetic-late", "text": "Late words.",
              "acknowledgement": "Text-file licence note, CC BY-SA 4.0."},
     },
     "steps": [
         {"do": "openFragmentOf", "author": "Synthetic Author", "label": "first-open"},
         {"do": "openFragmentOf", "author": "Second Author", "label": "second-open"},
     ]},
    # The same blocked row standing BESIDE held fragments: one typed truth
    # counts both and contradicts neither.
    {"name": "blocked-with-held", "hash": GEN1,
     "patch": {"structure/catena/01-gen/001.json":
               {"blocked": BLOCKED_FIXTURE["blocked"]}}},
    # An expected spine 404 with a voice cited: the integrity state may not
    # manufacture a "none here" option or a "none in" tally clause.
    {"name": "integrity-404-voice", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": None}},
    # Real Severian metadata end-to-end: the tracked PTA edition record's
    # CC BY-SA rights basis, projected as the source's acknowledgement,
    # rides the payload into the rendered point-of-use licence block over
    # the REAL fragments and the REAL Greek text files.
    {"name": "severian-projected", "hash": GEN1,
     "patch": {"structure/catena/01-gen/001.json":
               {"sources": {"6": {"acknowledgement": SEVERIAN_BASIS}}}},
     "steps": [{"do": "openFragmentOf", "author": "Severian of Gabala",
                "label": "opened"}]},
    # An expected spine that 404s: an integrity error, never "nothing held".
    {"name": "integrity-404", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": None}},
    # Fail-closed typed validation, one scenario per key, cold load.
    {"name": "invalid-book", "hash": "#book=Foo&chapter=1&bible=douay-rheims"},
    {"name": "invalid-chapter", "hash": "#book=Gen&chapter=99&bible=douay-rheims"},
    {"name": "invalid-bible", "hash": "#book=Gen&chapter=1&bible=nope"},
    {"name": "invalid-voice", "hash": GEN1 + "&voice=klingon"},
    {"name": "invalid-voice-colon", "hash": GEN1 + "&voice=translation:"},
    # `original:x` parses to an original VOICE without being the literal key;
    # honouring it self-contradicted (an "original — none here" option beside
    # the held original). The whole key must be sound.
    {"name": "invalid-voice-original-lang", "hash": GEN1 + "&voice=original:x"},
    # An out-of-range chapter with no book cited: ranged against the default.
    {"name": "chapter-only-cold", "hash": "#chapter=999"},
    # The same arriving by hashchange: ranged against the book the ADDRESS
    # resolves to (the default), exactly as it is cold — never the book the
    # reader happened to be on.
    {"name": "chapter-only-change", "hash": "#book=Ex&chapter=3&bible=douay-rheims",
     "steps": [{"do": "hash", "value": "#chapter=999", "label": "broken"}]},
    # Structural grammar: duplicate recognized keys — identical or
    # contradictory — and chapter values off the closed numeral grammar.
    {"name": "duplicate-key-identical",
     "hash": "#book=Gen&book=Gen&chapter=1&bible=douay-rheims"},
    {"name": "duplicate-key-conflicting",
     "hash": "#book=Gen&chapter=1&bible=douay-rheims&book=Foo"},
    # A malformed percent sequence stays literal in URLSearchParams and must
    # fail the closed value grammar rather than pass through.
    {"name": "malformed-encoding", "hash": "#book=G%ZZen&chapter=1&bible=douay-rheims"},
    {"name": "invalid-voice-suffix", "hash": GEN1 + "&voice=translation:en:extra"},
    {"name": "invalid-voice-space", "hash": GEN1 + "&voice=translation:%20en"},
    {"name": "chapter-zero", "hash": "#book=Gen&chapter=0&bible=douay-rheims"},
    {"name": "chapter-negative", "hash": "#book=Gen&chapter=-1&bible=douay-rheims"},
    {"name": "chapter-nonnumeric", "hash": "#book=Gen&chapter=two&bible=douay-rheims"},
    # History independence: the same invalid address arriving over a live
    # valid page, and bounced through Back/Forward, must render the page the
    # cold arrival renders.
    {"name": "invalid-after-navigation", "hash": GEN2,
     "steps": [{"do": "hash", "value": "#book=Gen&chapter=99&bible=douay-rheims",
                "label": "broken"}]},
    {"name": "invalid-back-forward", "hash": GEN1,
     "steps": [
         {"do": "hash", "value": "#book=Foo&chapter=1&bible=douay-rheims", "label": "broken"},
         {"do": "hash", "value": GEN1, "label": "back"},
         {"do": "hash", "value": "#book=Foo&chapter=1&bible=douay-rheims", "label": "forward"},
     ]},
    # Recovery with focus: the reader stands ON the recovery link (keyboard),
    # follows it, and must not be stranded when the link is rebuilt away.
    {"name": "keyboard-recovery", "hash": "#book=Foo&chapter=1&bible=douay-rheims",
     "steps": [{"do": "recoverByLink", "label": "recovered"}]},
    {"name": "control-recovery", "hash": "#book=Foo&chapter=1&bible=douay-rheims",
     "steps": [{"do": "selectChapter", "value": "2", "label": "recovered"}]},
    # Bootstrap failures: no permanent "Loading…", a truthful failure state.
    {"name": "bootstrap-failure", "hash": GEN1,
     "files": {"structure/catena/index.json": None}},
    {"name": "bootstrap-bibles-failure", "hash": GEN1,
     "files": {"bibles.json": None}},
    # Async transactions, on deferred requests. A = Gen 1 (spine parked),
    # B = Gen 2: B commits, then A completes or fails STALE.
    {"name": "race-stale-success", "hash": GEN1, "defer": ["01-gen/001.json"],
     "steps": [
         {"do": "hash", "value": GEN2, "label": "b-committed"},
         {"do": "release", "path": "01-gen/001.json", "label": "a-late"},
     ]},
    {"name": "race-stale-failure", "hash": GEN1, "defer": ["01-gen/001.json"],
     "steps": [
         {"do": "hash", "value": GEN2, "label": "b-committed"},
         {"do": "release", "path": "01-gen/001.json", "outcome": "fail", "label": "a-late"},
     ]},
    # B itself fails — by reader action and by arrival: the error belongs to
    # B and the URL still describes B.
    {"name": "race-b-fails", "hash": GEN1, "defer": ["01-gen/002.json"],
     "steps": [
         {"do": "selectChapter", "value": "2", "label": "b-pending"},
         {"do": "release", "path": "01-gen/002.json", "outcome": "fail", "label": "b-failed"},
     ]},
    {"name": "race-b-fails-arrival", "hash": GEN1, "defer": ["01-gen/002.json"],
     "steps": [
         {"do": "hash", "value": GEN2, "label": "b-pending"},
         {"do": "release", "path": "01-gen/002.json", "outcome": "fail", "label": "b-failed"},
     ]},
    # Rapid A -> B -> C: only C commits, whether the overtaken B later
    # resolves or fails.
    {"name": "race-rapid", "hash": GEN1, "defer": ["01-gen/002.json"],
     "steps": [
         {"do": "hash", "value": GEN2, "label": "b-pending"},
         {"do": "hash", "value": GEN42, "label": "c-committed"},
         {"do": "release", "path": "01-gen/002.json", "label": "b-late"},
     ]},
    {"name": "race-rapid-failure", "hash": GEN1, "defer": ["01-gen/002.json"],
     "steps": [
         {"do": "hash", "value": GEN2, "label": "b-pending"},
         {"do": "hash", "value": GEN42, "label": "c-committed"},
         {"do": "release", "path": "01-gen/002.json", "outcome": "fail", "label": "b-late"},
     ]},
    # Evicted rejections: a failed spine or fragment text is really re-asked
    # on the next visit or retry, and recovers.
    {"name": "spine-retry", "hash": GEN1, "defer": ["01-gen/001.json"],
     "steps": [
         {"do": "release", "path": "01-gen/001.json", "outcome": "fail", "label": "failed"},
         {"do": "hash", "value": GEN2, "label": "away"},
         {"do": "hash", "value": GEN1, "label": "returned"},
         {"do": "release", "path": "01-gen/001.json", "label": "recovered"},
     ]},
    {"name": "fragment-retry", "hash": GEN1, "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "opened"},
         {"do": "release", "path": "structure/catena/text/", "outcome": "fail",
          "label": "failed"},
         {"do": "openFirstFragment", "label": "reopened"},
         {"do": "release", "path": "structure/catena/text/", "label": "recovered"},
     ]},
    # A fragment-text completion landing after the page moved on: the
    # detached fragment takes nothing and the new page is untouched.
    {"name": "fragment-toggle-race", "hash": GEN1, "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "opened"},
         {"do": "hash", "value": GEN2, "label": "moved"},
         {"do": "release", "path": "structure/catena/text/", "label": "late"},
     ]},
    # A broken book beside a sound voice: the seeded control keeps the voice.
    {"name": "invalid-book-with-voice",
     "hash": "#book=Foo&chapter=1&bible=douay-rheims&voice=translation:en"},
    # Value-identical but non-canonical: scrambled order, a leading zero, a
    # percent-encoded colon and an unknown key. Arrival must not rewrite it.
    {"name": "noncanonical-arrival",
     "hash": "#chapter=01&book=Gen&bible=douay-rheims&voice=translation%3Aen&note=kept"},
    # Partial but valid: completed in place, never by pushing an entry.
    {"name": "partial-arrival", "hash": "#book=Gen"},
    {"name": "no-hash-arrival", "hash": ""},
    {"name": "invalid-recovery", "hash": "#book=Foo&chapter=1&bible=douay-rheims",
     "steps": [{"do": "hash", "value": GEN1, "label": "recovered"}]},
    {"name": "hashchange-invalid", "hash": GEN1,
     "steps": [{"do": "hash", "value": "#book=Gen&chapter=99&bible=douay-rheims",
                "label": "broken"}]},
    # Back and Forward, simulated as the browser fires them.
    {"name": "back-forward", "hash": GEN1,
     "steps": [
         {"do": "selectChapter", "value": "2", "label": "stepped"},
         {"do": "hash", "value": GEN1, "label": "back"},
         {"do": "hash", "value": GEN2, "label": "forward"},
     ]},
    # A carried-over exclusion landing on a single-author chapter: the filter
    # must still exist, say so, and offer the way back.
    {"name": "hidden-author-carry", "hash": GEN1,
     "steps": [
         {"do": "toggleAuthor", "author": "Remigius of Auxerre", "label": "hidden"},
         {"do": "hash", "value": GEN42, "label": "gen42"},
         {"do": "toggleAuthor", "author": "Remigius of Auxerre", "label": "restored"},
     ]},
    # ------------------------------------------------------------------------
    # The adversarial audits of 2026-08-11 (R1 and R2, over this candidate).
    # Each scenario is the audit's own repro, driven here so the repair cannot
    # be undone silently.
    # ------------------------------------------------------------------------
    # R1-F1: keyboard recovery whose recovered route then FAILS to load. The
    # link the reader stood on is removed by the failure arm, which used to
    # restore no focus at all.
    {"name": "recovery-load-fails",
     "hash": "#book=Gen&chapter=99&bible=douay-rheims&voice=translation:en",
     "defer": ["01-gen/001.json"],
     "steps": [
         {"do": "recoverByLink", "label": "pending"},
         {"do": "release", "path": "01-gen/001.json", "outcome": "fail",
          "label": "failed"},
     ]},
    # R1-F2: an arrival's parked deep-link voice, superseded by a reader
    # action before its spine lands. The reader's own render must not adopt
    # the abandoned route's voice, in the page or in the address.
    {"name": "parked-voice-superseded", "hash": GEN1, "defer": ["01-gen/002.json"],
     "steps": [
         {"do": "hash", "value": GEN2 + "&voice=translation:la", "label": "parked"},
         {"do": "selectChapter", "value": "3", "label": "reader"},
         {"do": "release", "path": "01-gen/002.json", "label": "late"},
     ]},
    # R2-F1: the page's own hash write, echoed back by the browser one task
    # later — after the reader has moved again. The echo must be consumed, not
    # read as a navigation back to the route it names.
    {"name": "echo-after-action", "hash": GEN1, "defer": ["01-gen/003.json"],
     "steps": [
         {"do": "selectChapter", "value": "2", "label": "committed"},
         {"do": "selectChapter", "value": "3", "label": "pending"},
         {"do": "echo", "label": "echo"},
         {"do": "release", "path": "01-gen/003.json", "label": "released"},
     ]},
    # The same echo with the controls unmoved: the quiet case must stay inert.
    {"name": "echo-unmoved", "hash": GEN1,
     "steps": [
         {"do": "selectChapter", "value": "2", "label": "committed"},
         {"do": "echo", "label": "echo"},
     ]},
    # R2-F2 / R1-F4: a blocked-only chapter with a voice cited by the address.
    {"name": "blocked-voice-link", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": BLOCKED_FIXTURE}},
    # The same claim reached by CONTROL rather than by address: the reader
    # chooses English where it is held, then moves to a blocked-only chapter,
    # so the kept selection arrives without an arrival's reseeding.
    {"name": "blocked-voice-control", "hash": GEN1,
     "files": {"structure/catena/01-gen/002.json": BLOCKED_FIXTURE},
     "steps": [
         {"do": "selectVoice", "value": "translation:en", "label": "chosen"},
         {"do": "selectChapter", "value": "2", "label": "moved"},
     ]},
    # R2-F2 variant (b): renderable fragments in ANOTHER voice beside a
    # blocked row. The absence claim may cover the renderable rows only.
    {"name": "blocked-beside-unshown-voice", "hash": GEN10_ENGLISH,
     "patch": {"structure/catena/01-gen/010.json":
               {"blocked": BLOCKED_FIXTURE["blocked"]}}},
    # R2-F3/F4/F5: malformed payload body, lead rows and blocked rows, each
    # beside a sound row of the same kind.
    {"name": "malformed-record", "hash": GEN1,
     "files": {
         "structure/catena/01-gen/001.json": MALFORMED_RECORD_FIXTURE,
         "structure/catena/text/malformed-payload.json":
             {"id": "malformed-payload", "text": {"broken": True},
              "basis": {"also": "broken"}, "date_basis": 42},
     },
     "steps": [{"do": "openFirstFragment", "label": "opened"}]},
    # R2-O1: a malformed spine acknowledgement beside a VALID payload one,
    # and a valid spine acknowledgement beside a malformed payload one.
    {"name": "acknowledgement-order", "hash": GEN1,
     "files": {
         "structure/catena/01-gen/001.json": ACK_ORDER_FIXTURE,
         "structure/catena/text/ack-payload-valid.json":
             {"id": "ack-payload-valid", "text": "Payload words.",
              "acknowledgement": "Payload licence note, CC BY-SA 4.0."},
         "structure/catena/text/ack-payload-broken.json":
             {"id": "ack-payload-broken", "text": "Second payload words.",
              "acknowledgement": {"broken": True}},
     },
     "steps": [
         {"do": "openFragmentOf", "author": "Broken Spine Author",
          "label": "broken-spine-open"},
         {"do": "openFragmentOf", "author": "Sound Spine Author",
          "label": "sound-spine-open"},
     ]},
]

REPLAY = r"""
'use strict';

/* The catena page, replayed under node. Every file the page is made of is
 * the real one; only the document, the network and the bible chapter text
 * are stubbed — the chapter text because it is generated into the build. */

const fs = require('fs');
const pathlib = require('path');

const [, , ROOT, PLAN_JSON] = process.argv;
const PLAN = JSON.parse(PLAN_JSON);
const DATA = pathlib.join(ROOT, 'src/web/data');
const BROWSER = pathlib.join(ROOT, 'src/web/browser');

class TextNode {
  constructor(text) { this.nodeType = 3; this.parentNode = null; this.data = String(text); }
  get textContent() { return this.data; }
  set textContent(value) { this.data = String(value); }
}

class ClassList {
  constructor(node) { this.node = node; }
  _names() {
    return this.node.className ? this.node.className.split(/\s+/).filter(Boolean) : [];
  }
  add(...names) {
    const held = this._names();
    for (const name of names) if (!held.includes(name)) held.push(name);
    this.node.className = held.join(' ');
  }
  remove(...names) {
    this.node.className = this._names().filter((one) => !names.includes(one)).join(' ');
  }
  contains(name) { return this._names().includes(name); }
}

class Element {
  constructor(tag) {
    this.nodeType = 1;
    this.localName = String(tag).toLowerCase();
    this.tagName = this.localName.toUpperCase();
    this.childNodes = [];
    this.parentNode = null;
    this.attributes = Object.create(null);
    this.listeners = Object.create(null);
    this.className = '';
    this.style = {};
  }
  get classList() { return new ClassList(this); }
  get firstChild() { return this.childNodes[0] || null; }
  get children() { return this.childNodes.filter((one) => one.nodeType === 1); }
  get id() { return this.attributes.id || ''; }
  set id(value) { this.attributes.id = String(value); }
  appendChild(child) {
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.childNodes.push(child);
    this._childrenChanged();
    return child;
  }
  insertBefore(child, before) {
    if (!before) return this.appendChild(child);
    if (child.parentNode) child.parentNode.removeChild(child);
    const at = this.childNodes.indexOf(before);
    child.parentNode = this;
    this.childNodes.splice(at < 0 ? this.childNodes.length : at, 0, child);
    this._childrenChanged();
    return child;
  }
  removeChild(child) {
    const at = this.childNodes.indexOf(child);
    if (at >= 0) this.childNodes.splice(at, 1);
    child.parentNode = null;
    this._childrenChanged();
    return child;
  }
  _childrenChanged() {}
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
  hasAttribute(name) { return name in this.attributes; }
  removeAttribute(name) { delete this.attributes[name]; }
  contains(node) {
    while (node) { if (node === this) return true; node = node.parentNode; }
    return false;
  }
  focus() { if (global.document) global.document.activeElement = this; }
  addEventListener(type, handler) {
    (this.listeners[type] = this.listeners[type] || []).push(handler);
  }
  dispatch(type) {
    for (const handler of this.listeners[type] || []) handler({ target: this, type: type });
  }
  get textContent() { return this.childNodes.map((one) => one.textContent).join(''); }
  set textContent(value) {
    this.childNodes = [];
    if (value !== '' && value !== null && value !== undefined) {
      this.appendChild(new TextNode(value));
    }
  }
  descendants() {
    const out = [];
    const walk = (node) => {
      for (const child of node.childNodes) {
        if (child.nodeType !== 1) continue;
        out.push(child);
        walk(child);
      }
    };
    walk(this);
    return out;
  }
}

/* The one element that needs real semantics: assigning a value no option
 * carries selects nothing and reads back empty. */
class SelectElement extends Element {
  constructor(tag) { super(tag); this.selectedIndex = -1; }
  _options() { return this.descendants().filter((one) => one.localName === 'option'); }
  _childrenChanged() {
    const options = this._options();
    if (!options.length) this.selectedIndex = -1;
    else if (this.selectedIndex < 0 && options.length === 1) this.selectedIndex = 0;
  }
  get value() {
    const options = this._options();
    if (this.selectedIndex < 0 || this.selectedIndex >= options.length) return '';
    const one = options[this.selectedIndex].value;
    return one === undefined ? '' : String(one);
  }
  set value(wanted) {
    this.selectedIndex = this._options().findIndex(
      (one) => String(one.value === undefined ? '' : one.value) === String(wanted));
  }
}

function createElement(tag) {
  const name = String(tag).toLowerCase();
  return name === 'select' ? new SelectElement(name) : new Element(name);
}

function matches(node, selector) {
  if (selector.startsWith('#')) return node.id === selector.slice(1);
  if (selector.startsWith('.')) return new ClassList(node).contains(selector.slice(1));
  const [tag, ...classes] = selector.split('.');
  if (tag && node.localName !== tag.toLowerCase()) return false;
  return classes.every((one) => new ClassList(node).contains(one));
}

function makeDocument() {
  const root = new Element('html');
  const body = new Element('body');
  body.className = 'catena-page';
  root.appendChild(body);
  const document = {
    documentElement: root,
    body: body,
    activeElement: body,
    listeners: Object.create(null),
    createElement: createElement,
    createTextNode: (text) => new TextNode(text),
    getElementById: (id) => root.descendants().find((one) => one.id === id) || null,
    querySelector: (s) => root.descendants().find((one) => matches(one, s)) || null,
    querySelectorAll: (s) => root.descendants().filter((one) => matches(one, s)),
    addEventListener: (type, handler) => {
      (document.listeners[type] = document.listeners[type] || []).push(handler);
    }
  };
  return document;
}

/* The shape of the STATIC catena/index.html the script reaches into: empty
 * reference, "Needs JavaScript" placeholder options, the open controls
 * disclosure, and a static-entry section in main — no aria-busy, no
 * "Loading" placeholder. */
function buildPage(document) {
  const body = document.body;
  const add = (parent, tag, id, className) => {
    const node = document.createElement(tag);
    if (id) node.id = id;
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  };
  const header = add(body, 'header', null, 'page-header');
  // CHANGED PIN (review 2026-08-11, robustness): the primary Scripture locus
  // was absent from heading navigation; the reference line is now an h2.
  const line = add(header, 'h2', null, 'reference-line');
  add(line, 'span', 'reference');
  add(line, 'span', 'reference-book', 'reference-book');
  add(header, 'p', 'tally', 'tally');
  add(body, 'div', 'banner', 'banner');

  const disclosure = add(body, 'details', 'controls-filter', 'controls-filter');
  disclosure.open = true;
  add(disclosure, 'summary').textContent = 'Change chapter and commentary voice';
  const controls = add(disclosure, 'form', 'controls', 'controls');
  // The bible and voice fields wear `print-identity`, as the page's do.
  const printed = { 'bible-select': 1, 'language-select': 1 };
  for (const id of ['book-select', 'chapter-select', 'bible-select', 'language-select']) {
    const field = add(controls, 'div', null, printed[id] ? 'field print-identity' : 'field');
    const select = add(field, 'select', id);
    select.disabled = true;
    const option = add(select, 'option');
    option.value = '';
    option.textContent = 'Needs JavaScript';
  }
  const steps = add(controls, 'div', null, 'field field-steps');
  add(steps, 'button', 'prev-button').disabled = true;
  add(steps, 'button', 'next-button').disabled = true;

  const reading = add(body, 'main', 'reading', 'reading');
  reading.setAttribute('tabindex', '-1');
  const entry = add(reading, 'section', null, 'static-entry');
  add(entry, 'p').textContent = 'Catena Omnia sets a chapter of Scripture beside every commentary fragment this project holds on it.';
  return { reading: reading, controlsDisclosure: disclosure };
}

const VERSES = {};
for (let n = 1; n <= 31; n += 1) VERSES[String(n)] = 'Verse ' + n + ' of the stub chapter.';

function corpusFile(path) {
  const chapter = /^([a-z0-9-]+)\/chapters\/([^/]+)\/(\d+)\.json$/.exec(path);
  if (chapter) return { book: chapter[2], chapter: Number(chapter[3]), verses: VERSES };
  const onDisk = pathlib.join(DATA, path);
  if (!fs.existsSync(onDisk)) return null;
  return JSON.parse(fs.readFileSync(onDisk, 'utf8'));
}

/* A scenario `patch` edits INSIDE a real corpus file — one field of one
 * source, one array — so a trace can ride real data with a projected
 * field, without replacing the whole record. */
function mergeInto(base, extra) {
  for (const key in extra) {
    const value = extra[key];
    if (base[key] && typeof base[key] === 'object'
        && value && typeof value === 'object' && !Array.isArray(value)) {
      mergeInto(base[key], value);
    } else {
      base[key] = value;
    }
  }
}

function inspect(page, document, location, fetched, hashWrites, replaced, statusWrites) {
  const reading = page.reading;
  const nodes = reading.descendants();
  const withClass = (name) => nodes.filter((one) => new ClassList(one).contains(name));
  const first = (name) => withClass(name)[0] || null;
  const text = (node) => (node ? node.textContent : null);
  const byId = (id) => document.getElementById(id);
  const filter = first('author-filter');
  const link = first('fragment-whole');
  const status = byId('reading-status');
  const groups = withClass('author').map((item) => {
    const inside = item.descendants();
    const of = (name) => {
      const found = inside.find((one) => new ClassList(one).contains(name));
      return found ? found.textContent : null;
    };
    const body = inside.find((one) => new ClassList(one).contains('author-body'));
    return {
      author: of('author-name'),
      date: of('author-date'),
      count: of('author-count'),
      open: Boolean(body && body.open),
      hidden: Boolean(item.hidden)
    };
  });
  const errors = withClass('catena-error').map((section) => {
    const inside = section.descendants();
    const anchor = inside.find((one) => one.localName === 'a');
    return {
      heading: section.children[0] ? section.children[0].textContent : null,
      state: section.getAttribute('data-state'),
      details: inside
        .filter((one) => new ClassList(one).contains('error-detail'))
        .map((one) => one.textContent),
      recoveryHref: anchor ? anchor.href : null
    };
  });
  const ackPlacement = withClass('fragment-body')
    .filter((body) => body.descendants()
      .some((one) => new ClassList(one).contains('fragment-acknowledgement')))
    .map((body) => {
      const kids = body.children.map((one) => one.className || one.localName);
      return kids.indexOf('fragment-acknowledgement') < kids.findIndex(
        (one) => String(one).startsWith('fragment-text'));
    });
  return {
    hash: location.hash,
    referenceText: text(byId('reference')),
    tallyText: text(byId('tally')),
    statusText: text(status),
    voice: byId('language-select').value,
    voiceLabels: byId('language-select').descendants()
      .filter((one) => one.localName === 'option')
      .map((one) => one.textContent),
    selectValues: {
      book: byId('book-select').value,
      chapter: byId('chapter-select').value,
      bible: byId('bible-select').value
    },
    controlsOpen: Boolean(page.controlsDisclosure.open),
    classes: [...new Set(nodes.map((one) => one.className).filter(Boolean))].sort(),
    dataStates: [...new Set(nodes
      .filter((one) => one.hasAttribute('data-state'))
      .map((one) => one.getAttribute('data-state')))].sort(),
    chapterOpen: Boolean((first('chapter-body') || {}).open),
    chapterCounts: withClass('chapter-count').map(text),
    authorGroups: groups,
    authorFilterInDisclosure: Boolean(
      filter && filter.parentNode
        && new ClassList(filter.parentNode).contains('author-filter-disclosure')),
    authorFilterOpen: Boolean(filter && filter.parentNode && filter.parentNode.open),
    filterLabels: filter
      ? filter.descendants().filter((one) => new ClassList(one).contains('author-toggle'))
          .map(text)
      : [],
    filterChecked: filter
      ? filter.descendants().filter((one) => one.localName === 'input')
          .map((one) => Boolean(one.checked))
      : [],
    fragmentCount: withClass('fragment').length,
    linkText: text(link),
    linkHref: link ? link.href : null,
    refusal: text(first('refusal')),
    paragraphNote: text(first('paragraph-note')),
    projected: nodes.filter((one) => new ClassList(one).contains('projected')).length,
    paragraphs: withClass('passage-paragraph').length,
    spans: withClass('spans').map(text),
    absenceSummary: first('absence-note') ? text(first('absence-note').children[0]) : null,
    absenceOpen: Boolean(first('absence-note') && first('absence-note').open),
    absenceReasons: withClass('absence-reason').map(text),
    absencePartials: withClass('absence-partial').map(text),
    sectionHeadings: withClass('section-heading').map(text),
    asideNotes: withClass('aside-note').map(text),
    leads: withClass('lead').map(text),
    blocked: withClass('blocked').map(text),
    fragmentTexts: withClass('fragment-text').map(text),
    fragmentBases: withClass('fragment-basis').map(text),
    sourceLines: withClass('fragment-source').map(text),
    acknowledgements: withClass('fragment-acknowledgement').map(text),
    acknowledgementAboveText: ackPlacement,
    languages: withClass('fragment-language').map(text),
    states: withClass('state').map(text),
    errorSections: errors,
    staticEntry: Boolean(first('static-entry')),
    // The commentary fragments BY IDENTITY, in rendered order, read off the
    // one identity-bearing node each carries (the pinned Source Library
    // href) — for the exactly-once chronology invariant.
    fragmentIds: withClass('fragment').map((item) => {
      const whole = item.descendants().find(
        (one) => new ClassList(one).contains('fragment-whole'));
      return whole
        ? decodeURIComponent(String(whole.href).replace('../sources/#passage=', ''))
        : null;
    }),
    activeElement: document.activeElement
      ? (document.activeElement.id || document.activeElement.localName)
      : null,
    stepButtons: [
      Boolean(byId('prev-button') && byId('prev-button').disabled),
      Boolean(byId('next-button') && byId('next-button').disabled)
    ],
    bookLabels: byId('book-select').descendants()
      .filter((one) => one.localName === 'option')
      .map((one) => one.textContent).slice(0, 3),
    statusWrites: (statusWrites || []).slice(),
    hashWrites: (hashWrites || []).slice(),
    replaced: (replaced || []).slice(),
    fetched: fetched.slice()
  };
}

async function settle() {
  for (let turn = 0; turn < 400; turn += 1) await Promise.resolve();
  await new Promise((accept) => setTimeout(accept, 0));
  for (let turn = 0; turn < 400; turn += 1) await Promise.resolve();
}

async function run(scenario) {
  const document = makeDocument();
  /* The address bar: assignments to location.hash are the PUSHING writes a
   * browser turns into history entries, so they are recorded; the harness's
   * own Back/Forward simulation bypasses the setter, exactly as a browser
   * restoring a hash does not re-assign it. replaceState swaps the entry in
   * place and is recorded separately. */
  let hashValue = scenario.hash || '';
  const hashWrites = [];
  const replaced = [];
  const location = {
    search: '',
    pathname: '/catena/',
    get hash() { return hashValue; },
    set hash(next) { hashValue = String(next); hashWrites.push(hashValue); }
  };
  const window = {
    location: location,
    history: {
      replaceState: (state, title, url) => {
        const target = String(url);
        const cut = target.indexOf('#');
        hashValue = cut >= 0 ? target.slice(cut) : '';
        replaced.push(target);
      }
    },
    listeners: Object.create(null),
    addEventListener: (type, handler) => {
      (window.listeners[type] = window.listeners[type] || []).push(handler);
    },
    matchMedia: (query) => ({
      media: query,
      matches: Boolean(scenario.narrow) && /max-width/.test(query)
    })
  };
  const page = buildPage(document);
  const overrides = scenario.files || {};
  const fetched = [];

  /* Requests parked in flight: a scenario naming path fragments in `defer`
   * holds every matching response until a `release` step resolves it (or
   * rejects it as a transport failure) — real interleaving, not timing
   * luck. */
  const parked = new Map();

  global.window = window;
  global.document = document;
  global.location = location;
  global.fetch = async (url) => {
    const path = String(url).replace(/^\.\.\/browse\//, '');
    fetched.push(path);
    const has = Object.prototype.hasOwnProperty.call(overrides, path);
    const body = has ? overrides[path] : corpusFile(path);
    const extra = (scenario.patch || {})[path];
    if (extra && body) mergeInto(body, extra);
    const response = (body === null || body === undefined)
      ? { ok: false, status: 404, json: async () => null }
      : { ok: true, status: 200, json: async () => body };
    if ((scenario.defer || []).some((piece) => path.includes(piece))) {
      return new Promise((resolve, reject) => {
        if (!parked.has(path)) parked.set(path, []);
        parked.get(path).push({ resolve: () => resolve(response), reject: reject });
      });
    }
    return response;
  };

  for (const file of ['shared/browser-core.js', 'catena/catena-model.js', 'catena/catena.js']) {
    const source = fs.readFileSync(pathlib.join(BROWSER, file), 'utf8');
    new Function('window', 'self', 'document', 'fetch', 'location', source)(
      window, window, document, global.fetch, location);
  }
  // Every spoken line, in order — the single announcement channel, so
  // duplicate or missing announcements are visible, not just the last one.
  // `fail` speaks through its own internal reference to statusLine, so it
  // is recorded at its own seam.
  const statusWrites = [];
  const realStatus = window.Triptych.statusLine;
  window.Triptych.statusLine = (text) => {
    statusWrites.push(String(text));
    realStatus(text);
  };
  const realFail = window.Triptych.fail;
  window.Triptych.fail = (text, target) => {
    statusWrites.push(String(text));
    realFail(text, target);
  };
  await settle();

  const snapshots = {};
  snapshots.start = inspect(page, document, location, fetched, hashWrites, replaced, statusWrites);

  for (const step of scenario.steps || []) {
    if (step.do === 'hash') {
      // The browser: Back, Forward, or a typed hash — the URL changes and a
      // hashchange event fires. The raw assignment bypasses the recording
      // setter: history restoration is not a page-initiated write.
      hashValue = step.value;
      for (const handler of window.listeners.hashchange || []) handler({});
      await settle();
    } else if (step.do === 'recoverByLink') {
      // Keyboard recovery: the reader is ON the recovery link when
      // following it, and the navigation is the browser's own, not a page
      // write — like the raw `hash` step, but carrying focus.
      const anchor = page.reading.descendants().find(
        (one) => one.localName === 'a' && one.parentNode
          && new ClassList(one.parentNode).contains('error-recovery'));
      if (anchor) {
        document.activeElement = anchor;
        hashValue = anchor.href;
        for (const handler of window.listeners.hashchange || []) handler({});
      }
      await settle();
    } else if (step.do === 'echo') {
      // The browser's DELAYED dispatch of the page's OWN location.hash
      // write: assignment and event are separated by a task, so the event
      // can land after the reader has already acted. The hash is unchanged
      // since the write — that is what makes it an echo and not a move.
      for (const handler of window.listeners.hashchange || []) handler({});
      await settle();
    } else if (step.do === 'selectVoice') {
      const select = document.getElementById('language-select');
      document.activeElement = select;
      select.value = step.value;
      select.dispatch('change');
      await settle();
    } else if (step.do === 'release') {
      // Let a parked request finish — successfully, or as the transport
      // failure the reader's network really produces.
      for (const [path, waiting] of Array.from(parked)) {
        if (!path.includes(step.path)) continue;
        parked.delete(path);
        for (const one of waiting) {
          if (step.outcome === 'fail') one.reject(new Error('the network failed'));
          else one.resolve();
        }
      }
      await settle();
    } else if (step.do === 'selectChapter') {
      const select = document.getElementById('chapter-select');
      document.activeElement = select;
      select.value = step.value;
      select.dispatch('change');
      await settle();
    } else if (step.do === 'toggleAuthor') {
      const filter = document.querySelector('.author-filter');
      const label = filter && filter.descendants().find(
        (one) => new ClassList(one).contains('author-toggle')
          && one.textContent === step.author);
      if (label) {
        const box = label.descendants().find((one) => one.localName === 'input');
        box.checked = !box.checked;
        box.dispatch('change');
      }
      await settle();
    } else if (step.do === 'openFragmentOf') {
      const item = page.reading.descendants().find(
        (one) => new ClassList(one).contains('fragment')
          && one.descendants().some((deep) =>
            new ClassList(deep).contains('fragment-author')
              && deep.textContent === step.author));
      const body = item && item.descendants().find(
        (one) => new ClassList(one).contains('fragment-body'));
      if (body) {
        body.open = true;
        body.dispatch('toggle');
      }
      await settle();
    } else if (step.do === 'openFirstFragment') {
      const body = page.reading.descendants()
        .find((one) => new ClassList(one).contains('fragment-body'));
      if (body) {
        body.open = true;
        body.dispatch('toggle');
      }
      await settle();
    }
    snapshots[step.label || step.do] = inspect(page, document, location, fetched, hashWrites, replaced, statusWrites);
  }

  const report = inspect(page, document, location, fetched, hashWrites, replaced, statusWrites);
  report.snapshots = snapshots;
  return report;
}

(async () => {
  const report = {};
  for (const scenario of PLAN) {
    try {
      report[scenario.name] = await run(scenario);
    } catch (error) {
      report[scenario.name] = { error: String((error && error.stack) || error) };
    }
  }
  process.stdout.write(JSON.stringify(report));
})();
"""


_REPLAYED: dict | None = None


def replayed() -> dict:
    """Run every scenario once; the corpus is large and the states are many."""
    global _REPLAYED
    if _REPLAYED is None:
        handle, path = tempfile.mkstemp(suffix=".js", prefix="catena-replay-")
        os.close(handle)
        try:
            Path(path).write_text(REPLAY, encoding="utf-8")
            result = subprocess.run(
                [NODE, path, str(ROOT), json.dumps(SCENARIOS)],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0:
                raise AssertionError(result.stderr.strip() or "the replay harness exited non-zero")
            _REPLAYED = json.loads(result.stdout)
        finally:
            os.unlink(path)
    return _REPLAYED


@unittest.skipIf(NODE is None, "node is not installed; the page cannot be replayed")
class ReplayTest(unittest.TestCase):
    """Base for every test that reads the replayed page."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = replayed()

    def page(self, name: str) -> dict:
        one = self.pages[name]
        self.assertNotIn("error", one, one.get("error", ""))
        return one

    def snapshot(self, name: str, label: str) -> dict:
        return self.page(name)["snapshots"][label]

    def assert_failed_closed(self, name: str, written: str, named: str):
        page = self.page(name)
        self.assertEqual(page["hash"], written, "the URL keeps the reader's own text")
        self.assertTrue(page["errorSections"], "a visible error state is owed")
        error = page["errorSections"][0]
        self.assertEqual(error["heading"], "This address names what the page does not have")
        self.assertEqual(error["state"], "error")
        self.assertTrue(any(named in one for one in error["details"]),
                        f"{named!r} not named in {error['details']}")
        self.assertTrue(error["recoveryHref"], "recovery must be offered")
        self.assertEqual(page["referenceText"], "Address not recognised")
        self.assertEqual(page["fragmentCount"], 0, "no content may render under the error")
        self.assertFalse([one for one in page["fetched"] if "/chapters/" in one],
                         "no chapter may be fetched for an invalid address")

    @staticmethod
    def rendered_state(snap: dict) -> dict:
        """The rendered state alone — the projections that must be identical
        for one URL + data whatever the arrival path — with the per-session
        history/network journals left out."""
        journals = {"fetched", "hashWrites", "replaced", "statusWrites", "snapshots"}
        return {key: value for key, value in snap.items() if key not in journals}


class ChronologyTest(ReplayTest):
    """Finding 2 — the chain's chronology survives grouping.

    The generator orders fragments by text date. The first candidate then
    coalesced every work by author, so Genesis 1 rendered Augustine 401,
    Augustine 417 and Severian 401 under one Augustine heading labelled 401.
    Only a CONTIGUOUS run by one author with one date may share a heading.
    """

    EXPECTED = [
        ("Basil of Caesarea", "378", 18),
        ("Gregory of Nyssa", "379", 1),
        ("Ambrose of Milan", "386", 6),
        ("Jerome", "391", 2),
        ("Augustine of Hippo", "401", 4),
        ("Severian of Gabala", "401", 5),
        ("Augustine of Hippo", "417", 3),
        ("Bede", "717", 35),
        ("Alcuin of York", "796", 4),
        ("Angelomus of Luxeuil", "845", 17),
        ("Remigius of Auxerre", "890", 11),
        ("Martin Luther", "1535", 1),
    ]

    def test_genesis_1_renders_twelve_groups_in_text_date_order(self):
        groups = self.page("default")["authorGroups"]
        self.assertEqual(
            [(one["author"], one["date"]) for one in groups],
            [(author, date) for author, date, _ in self.EXPECTED],
        )

    def test_augustine_severian_augustine_stand_as_three_groups(self):
        groups = self.page("default")["authorGroups"]
        middle = [(one["author"], one["date"]) for one in groups[4:7]]
        self.assertEqual(middle, [
            ("Augustine of Hippo", "401"),
            ("Severian of Gabala", "401"),
            ("Augustine of Hippo", "417"),
        ])

    def test_the_groups_carry_every_fragment_exactly_once(self):
        groups = self.page("default")["authorGroups"]
        counts = [int(re.match(r"(\d+)", one["count"]).group(1)) for one in groups]
        self.assertEqual(counts, [count for _, _, count in self.EXPECTED])
        self.assertEqual(sum(counts), 107)
        self.assertEqual(self.page("default")["fragmentCount"], 107)

    def test_every_expected_fragment_id_renders_exactly_once_in_order(self):
        # The correction review asked chronology to be proved by IDENTITY,
        # not by counts: every fragment id the generated spine carries, in
        # the spine's own order, none duplicated by coalescing, none lost.
        spine = json.loads(
            (ROOT / "src/web/data/structure/catena/01-gen/001.json")
            .read_text(encoding="utf-8"))
        expected = [one["id"] for one in spine["fragments"]]
        self.assertEqual(len(set(expected)), len(expected),
                         "the spine itself must not repeat an id")
        self.assertEqual(self.page("default")["fragmentIds"], expected)

    def test_the_sparse_chapter_also_renders_by_exact_identity(self):
        spine = json.loads(
            (ROOT / "src/web/data/structure/catena/01-gen/042.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(self.page("one-commentator")["fragmentIds"],
                         [one["id"] for one in spine["fragments"]])


class VoiceCountTruthTest(ReplayTest):
    """Finding 8a — the tally states the corpus, never the filter.

    Genesis 10 holds 71 fragments, all in their authors' own Latin. Selecting
    English used to headline "Nothing held here"; the corpus truth now leads
    and the empty selection is a second clause.
    """

    def test_an_empty_voice_selection_never_reads_as_an_empty_chapter(self):
        # CHANGED PIN (finding 3 tally clause, finding 8 announcement): the
        # 2026-08-11 review requires the tally to stop calling lead rows
        # "works", and the announcement now speaks the tally's own clauses
        # ("none in English translation" carries what ", 0 shown" said).
        page = self.page("voice-empty-chapter")
        self.assertEqual(
            page["tallyText"],
            "71 fragments held · none in English translation"
            " · 28 lead entries on the acquisition list")
        self.assertNotIn("Nothing", page["tallyText"])
        self.assertIn("71 fragments held, none in English translation",
                      page["statusText"])
        self.assertTrue(any(
            "71 fragments are held here, in the author’s own language" in one
            for one in page["asideNotes"]))

    def test_a_voice_showing_a_subset_is_a_second_clause(self):
        page = self.page("voice-held")
        self.assertEqual(
            page["tallyText"],
            "107 fragments held · 14 in English translation"
            " · 33 lead entries on the acquisition list")

    def test_the_unfiltered_tally_counts_the_corpus(self):
        self.assertEqual(
            self.page("default")["tallyText"],
            "107 fragments held · 33 lead entries on the acquisition list")

    def test_a_chapter_with_nothing_says_nothing_held(self):
        self.assertEqual(self.page("nothing-held")["tallyText"], "Nothing held here")


class AbsenceCountTest(ReplayTest):
    """Finding 8b — partial-public-domain findings are counted apart.

    Two of Genesis 1's eight recorded English absences are partly public
    domain; filing them under "no English this project may publish" overstated
    the bar the record actually sets.
    """

    def test_the_heading_counts_the_two_findings_apart(self):
        page = self.page("voice-held")
        self.assertEqual(
            page["absenceSummary"],
            "6 works standing here have no English this project may publish; "
            "2 have only a partly public domain English, not yet taken")

    def test_every_absence_still_carries_its_reason_and_partials_their_offer(self):
        page = self.page("voice-held")
        self.assertEqual(len(page["absenceReasons"]), 8)
        self.assertTrue(all(one.strip() for one in page["absenceReasons"]))
        self.assertEqual(len(page["absencePartials"]), 2)
        self.assertTrue(all(one.startswith("Partly public domain — ")
                            for one in page["absencePartials"]))


class ParagraphCountTest(ReplayTest):
    """Finding 8c — the paragraph chip counts paragraphs, not breaks.

    Genesis 1 in the Douay edition carries seven projected BREAKS, which open
    eight PARAGRAPHS; the chip used to print the break count under the word
    "paragraphs".
    """

    def test_the_chip_counts_the_paragraphs_on_the_page(self):
        page = self.page("default")
        self.assertEqual(page["projected"], 7)
        self.assertEqual(page["paragraphs"], 8)
        self.assertIn("8 paragraphs", page["chapterCounts"])
        self.assertNotIn("7 paragraphs", page["chapterCounts"])

    def test_the_note_still_speaks_of_breaks_in_those_words(self):
        self.assertEqual(
            self.page("default")["paragraphNote"],
            "Paragraphs: 7 are projected from the witnesses that concur, and marked.")

    def test_a_chapter_with_no_paragraph_data_says_it_runs_on(self):
        note = self.page("numbering-refusal")["paragraphNote"]
        self.assertIn("No paragraph division is held for this chapter", note)
        self.assertIn("Another edition’s paragraphs are not borrowed for it.", note)


class AuthorFilterRecoveryTest(ReplayTest):
    """Finding 8d — a filter can never strand the reader.

    Exclusions persist across chapters, so a sole author switched off
    elsewhere used to leave a chapter with zero visible fragments and no
    control at all. The filter now exists whenever an exclusion touches the
    chapter, the heading says everything is switched off, and the disclosure
    opens itself.
    """

    def test_a_fresh_single_author_chapter_grows_no_filter(self):
        page = self.page("one-commentator")
        self.assertEqual(page["fragmentCount"], 3)
        self.assertEqual(len(page["authorGroups"]), 1)
        self.assertFalse(page["authorFilterInDisclosure"])

    def test_a_partial_filter_is_reported_against_the_held_total(self):
        hidden = self.snapshot("hidden-author-carry", "hidden")
        self.assertIn("107 fragments held here — 96 shown", hidden["sectionHeadings"])

    def test_a_carried_exclusion_still_offers_the_switch_on_a_sole_author(self):
        gen42 = self.snapshot("hidden-author-carry", "gen42")
        self.assertEqual(gen42["filterLabels"], ["Remigius of Auxerre"])
        self.assertEqual(gen42["filterChecked"], [False])
        self.assertTrue(gen42["authorFilterOpen"],
                        "the disclosure must open when everything is hidden")
        self.assertIn(
            "3 fragments held here — none shown; every author is switched off below",
            gen42["sectionHeadings"])
        self.assertTrue(all(one["hidden"] for one in gen42["authorGroups"]))

    def test_the_switch_restores_the_chain(self):
        restored = self.snapshot("hidden-author-carry", "restored")
        self.assertIn("3 fragments held here", restored["sectionHeadings"])
        self.assertFalse(any(one["hidden"] for one in restored["authorGroups"]))


class IntegrityErrorTest(ReplayTest):
    """Finding 8e — an expected spine that 404s is an error, not an absence.

    The index lists Genesis 1 as present; when its record cannot be fetched
    the page must not say "nothing is held here", which the record proves
    false.
    """

    def test_a_missing_expected_record_renders_as_an_error(self):
        page = self.page("integrity-404")
        self.assertTrue(page["errorSections"])
        error = page["errorSections"][0]
        self.assertEqual(error["heading"], "This chapter’s commentary record did not load")
        self.assertEqual(error["state"], "error")
        self.assertTrue(any("structure/catena/01-gen/001.json" in one
                            for one in error["details"]))

    def test_the_error_never_claims_emptiness(self):
        page = self.page("integrity-404")
        self.assertNotIn("No commentary on this chapter is held yet.", page["asideNotes"])
        self.assertNotIn("Nothing", page["tallyText"])
        self.assertEqual(page["tallyText"], "The commentary record did not load")
        self.assertIn("commentary record unavailable", page["statusText"])

    def test_the_scripture_itself_still_renders(self):
        self.assertTrue(self.page("integrity-404")["chapterOpen"])

    def test_a_chapter_the_index_omits_is_still_a_plain_absence(self):
        page = self.page("nothing-held")
        self.assertFalse(page["errorSections"])
        self.assertIn("No commentary on this chapter is held yet.", page["asideNotes"])
        self.assertFalse(
            [one for one in page["fetched"] if one.startswith("structure/catena/02-ex/")],
            "a chapter the index does not list must not be asked for")


class LeadsCopyTest(ReplayTest):
    """Finding 3, route half — rows are UNRECONCILED LEAD ENTRIES.

    The generated leads overlap held works on real chapters and the
    projection strips the record's confidence, so the page may not call a
    row a "work", may not say "printed as recorded", and may claim neither
    "not yet acquired" nor that no text of any lead is held. The copy
    discloses the omitted confidence; identity reconciliation stays the
    generator's. Rows render unhidden, unreordered, by exact identity.
    """

    NOTE_15 = (
        "15 unreconciled lead entries on the acquisition record for this "
        "chapter, which omits its confidence. An entry establishes no "
        "distinct work, no possession and nothing renderable, and the list "
        "is not checked against the commentary above.")

    def test_the_heading_and_note_claim_only_the_record(self):
        # CHANGED PIN: the 2026-08-11 review found "works ... printed as
        # recorded" overstated a projection that omits confidence and does
        # not establish distinct works; the earlier pin REQUIRED that copy.
        page = self.page("acquisition-only")
        self.assertIn("Believed to comment here — the acquisition list",
                      page["sectionHeadings"])
        note = next(one for one in page["asideNotes"]
                    if "acquisition record" in one)
        self.assertEqual(note, self.NOTE_15)

    def test_the_old_overclaims_are_gone(self):
        script = held(CATENA / "catena.js")
        page_source = held(CATENA / "index.html")
        for overclaim in ("not yet acquired", "no text of any",
                          "printed as recorded"):
            self.assertNotIn(overclaim, script)
            self.assertNotIn(overclaim, page_source)
        # No route copy may call a lead row a confirmed work.
        self.assertNotIn("works the acquisition record", script)
        self.assertNotIn("works on the acquisition list", script)

    def test_the_rows_render_unhidden(self):
        page = self.page("acquisition-only")
        self.assertEqual(page["fragmentCount"], 0)
        self.assertEqual(len(page["leads"]), 15)
        # Genesis 1's 33 rows include held works; they are not hidden here.
        self.assertEqual(len(self.page("default")["leads"]), 33)

    def test_the_rows_render_exact_identity_in_record_order(self):
        # The review demanded exact row identity/order, not counts alone:
        # every author/title/date string of the Genesis 1 record, in the
        # record's own order.
        spine = json.loads(
            (ROOT / "src/web/data/structure/catena/01-gen/001.json")
            .read_text(encoding="utf-8"))
        expected = [
            (lead.get("author") + " — " if lead.get("author") else "") +
            (lead.get("title") or "") +
            (" (" + str(lead["date"]) + ")" if lead.get("date") else "")
            for lead in spine["leads"]]
        self.assertEqual(len(expected), 33)
        self.assertEqual(
            expected[0],
            "Alcuin of York — Interrogationes et responsiones in Genesim (804)")
        self.assertEqual(expected[-1], "Walafrid Strabo — Glossa ordinaria (849)")
        self.assertEqual(self.page("default")["leads"], expected)

    def test_a_low_information_lead_row_claims_nothing_stronger(self):
        # A row with only a title renders only the title — no "undefined",
        # no invented author, date, possession or renderability.
        page = self.page("held-unrenderable")
        self.assertIn("Fragmenta incerta", page["leads"])
        self.assertNotIn("undefined", " ".join(page["leads"]))
        note = next(one for one in page["asideNotes"]
                    if "acquisition record" in one)
        self.assertTrue(note.startswith("2 unreconciled lead entries"), note)

    def test_the_tally_speaks_of_the_list_not_of_acquisition_state(self):
        # CHANGED PIN: "works" became "lead entries" (finding 3).
        self.assertIn("lead entries on the acquisition list",
                      self.page("default")["tallyText"])
        self.assertNotIn("works on the acquisition list",
                         self.page("default")["tallyText"])


class RightsRenderingTest(ReplayTest):
    """Finding 4, route half — every rights fact the payload supplies renders.

    The corpus today reduces the Severian CC BY-SA terms to `rights:
    "licensed"` plus an `edition_published` line that carries the Voicu /
    von Stockhausen / BBAW attribution prose; projecting the full licence
    metadata is a recorded generator prerequisite. The page renders every
    supplied, valid, nonempty typed field — no browser-side precedence, no
    suppression — through ONE point-of-use acknowledgement channel, and a
    malformed value fails safely rather than becoming a guessed status.
    """

    def test_the_severian_provenance_prints_everything_the_spine_carries(self):
        lines = [one for one in self.page("severian-open")["sourceLines"]
                 if "Patristic Text Archive" in one]
        self.assertEqual(len(lines), 5, "five Severian fragments stand on Genesis 1")
        for line in lines:
            self.assertIn("In cosmogoniam homiliae 1-6, Patristic Text Archive edition pta-grc1", line)
            self.assertIn("Berlin-Brandenburgische Akademie der Wissenschaften, 2018", line)
            self.assertIn("Sever J. Voicu", line)
            self.assertIn("licensed", line)
            self.assertIn("inspected, not collated", line)

    def test_a_bare_licensed_rights_value_prints_truthfully_and_no_more(self):
        page = self.page("severian-open")
        self.assertFalse(page["acknowledgements"],
                         "no acknowledgement exists in the payload; none may be invented")
        self.assertTrue(all("public-domain" in one or "licensed" in one
                            for one in page["sourceLines"]))

    def test_every_fragment_prints_its_edition_printing(self):
        # Every Genesis 1 source records an edition_published; each line
        # carries it (NPNF shown as the concrete witness).
        self.assertTrue(any("New York: Christian Literature Company, 1895" in one
                            for one in self.page("default")["sourceLines"]))

    def test_provenance_stands_whether_or_not_the_text_loads(self):
        # Source lines exist for all 107 fragments before any text is fetched.
        self.assertEqual(len(self.page("voice-held")["snapshots"]["start"]["fetched"]), 6)
        self.assertEqual(len(self.page("default")["sourceLines"]), 107)

    def test_a_recorded_acknowledgement_renders_above_the_prose(self):
        """SYNTHETIC fixture: the corpus does not yet project these fields."""
        start = self.snapshot("synthetic-licence", "first-open")
        self.assertIn("Licence: Greek text by A. Editor, CC BY-SA 4.0; share alike.",
                      start["acknowledgements"])
        self.assertTrue(all(start["acknowledgementAboveText"]),
                        "the acknowledgement must precede the prose it covers")
        self.assertIn("Attribution: A. Editor, Synthetic Academy",
                      start["sourceLines"][0])

    def test_no_acknowledgement_suppresses_a_supplied_rights_basis(self):
        """CHANGED PIN: the 2026-08-11 review found the route suppressed a
        supplied `rights_basis` whenever any acknowledgement was truthy; the
        earlier pin asserted that suppression. Every supplied, valid,
        nonempty typed field now renders."""
        page = self.snapshot("synthetic-licence", "second-open")
        self.assertIn("Recorded basis, rendered beside the acknowledgement.",
                      page["sourceLines"][0])
        self.assertIn("printed because no acknowledgement is recorded",
                      page["sourceLines"][1])

    def test_a_valid_rights_basis_alone_renders_and_a_late_payload_joins_it(self):
        """SYNTHETIC fixture, second source: `rights_basis` in the spine, an
        acknowledgement arriving only with the lazily fetched text file. The
        late payload fills the ONE channel; the basis is untouched."""
        page = self.snapshot("synthetic-licence", "second-open")
        self.assertIn("printed because no acknowledgement is recorded",
                      page["sourceLines"][1])
        self.assertIn("Licence: Text-file licence note, CC BY-SA 4.0.",
                      page["acknowledgements"])
        self.assertTrue(all(page["acknowledgementAboveText"]))

    def test_a_valid_acknowledgement_alone_renders_alone(self):
        """SYNTHETIC fixture, third source: acknowledgement, no basis."""
        page = self.page("synthetic-licence")
        self.assertIn("Licence: Only an acknowledgement, no basis.",
                      page["acknowledgements"])
        third_line = page["sourceLines"][2]
        self.assertIn("licensed", third_line)
        self.assertIn("Third Edition", third_line)

    def test_two_supplies_render_exactly_one_acknowledgement(self):
        # The first source's spine AND its text payload both carry a note;
        # the one canonical channel renders the spine's block exactly once
        # and the payload's duplicate never.
        for label in ("first-open", "second-open"):
            page = self.snapshot("synthetic-licence", label)
            spine_note = "Licence: Greek text by A. Editor, CC BY-SA 4.0; share alike."
            self.assertEqual(page["acknowledgements"].count(spine_note), 1, label)
            self.assertNotIn("Payload duplicate that must not render twice.",
                             " ".join(page["acknowledgements"]))

    def test_malformed_values_fail_safely_and_hide_nothing_valid(self):
        """SYNTHETIC fixture, fourth source: a numeric `rights_basis`, an
        object `acknowledgement` and a whitespace `attribution` are not
        facts. None renders as one, none is guessed into a legal status,
        and the valid `rights` beside them still renders."""
        page = self.page("synthetic-licence")
        fourth_line = page["sourceLines"][3]
        self.assertIn("licensed", fourth_line)
        self.assertIn("Fourth Edition", fourth_line)
        self.assertNotIn("12345", fourth_line)
        joined = " ".join(page["acknowledgements"])
        self.assertNotIn("[object Object]", joined + " " + fourth_line)
        self.assertIn("The recorded acknowledgement is malformed and not shown.",
                      page["acknowledgements"])

    def test_absent_metadata_invents_nothing(self):
        # Real corpus truth: no Severian source record carries an
        # acknowledgement or a rights basis today, and none is invented.
        page = self.page("severian-open")
        self.assertFalse(page["acknowledgements"])
        self.assertNotIn("malformed", " ".join(page["sourceLines"]))


class HashValidationTest(ReplayTest):
    """Finding 5 — the cited state fails closed, cold and on hashchange.

    Every invalid value is retained in the URL exactly as written, named in a
    visible error state, and answered with recovery; no default is silently
    selected and no stale chapter stands under a broken address.
    """

    def test_an_unknown_book_fails_closed(self):
        self.assert_failed_closed(
            "invalid-book", "#book=Foo&chapter=1&bible=douay-rheims",
            "book=Foo is not a book of this canon")
        self.assertEqual(self.page("invalid-book")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")

    def test_a_chapter_out_of_range_fails_closed(self):
        self.assert_failed_closed(
            "invalid-chapter", "#book=Gen&chapter=99&bible=douay-rheims",
            "chapter=99 is not a chapter of Genesis, which has 50")

    def test_an_unknown_bible_fails_closed(self):
        self.assert_failed_closed(
            "invalid-bible", "#book=Gen&chapter=1&bible=nope",
            "bible=nope is not a published edition")

    def test_a_malformed_voice_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice", "#book=Gen&chapter=1&bible=douay-rheims&voice=klingon",
            "voice=klingon is not a voice")

    def test_a_voice_with_no_language_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice-colon", "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:",
            "voice=translation: is not a voice")

    def test_an_original_carrying_a_language_fails_closed(self):
        # `parseVoiceKey('original:x')` yields voice === original; honouring
        # the fragment of a key rendered a self-contradicting page.
        self.assert_failed_closed(
            "invalid-voice-original-lang",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=original:x",
            "voice=original:x is not a voice")

    def test_a_bookless_out_of_range_chapter_fails_closed_cold(self):
        self.assert_failed_closed(
            "chapter-only-cold", "#chapter=999",
            "chapter=999 is not a chapter of Genesis, which has 50")

    def test_an_out_of_range_chapter_is_ranged_history_independently(self):
        # The correction review found the anchor history-dependent: this
        # address used to be judged against the book the reader was on. It
        # is now judged against the book the ADDRESS resolves to, so the
        # hashchange arrival renders exactly what the cold arrival renders.
        broken = self.snapshot("chapter-only-change", "broken")
        self.assertEqual(broken["hash"], "#chapter=999")
        self.assertTrue(broken["errorSections"])
        self.assertTrue(any(
            "chapter=999 is not a chapter of Genesis, which has 50" in one
            for one in broken["errorSections"][0]["details"]))
        self.assertEqual(broken["fragmentCount"], 0,
                         "the stale Exodus 3 chain must not stand under the broken address")
        self.assertEqual(self.rendered_state(broken),
                         self.rendered_state(self.page("chapter-only-cold")))

    def test_the_invalid_path_seeds_the_voice_control(self):
        # Never a control left saying "Loading…" on the honesty page itself.
        # CHANGED PIN: the 2026-08-11 review found invalid states labelling
        # a selected voice "none here" — an absence claim the unresolved
        # route cannot make; the kept selection now claims nothing.
        self.assertEqual(self.page("invalid-book")["voiceLabels"], ["Everything held"])
        with_voice = self.page("invalid-book-with-voice")
        self.assertIn("English translation", with_voice["voiceLabels"])
        self.assertNotIn("English translation — none here", with_voice["voiceLabels"])
        self.assertEqual(with_voice["voice"], "translation:en")
        self.assertEqual(
            with_voice["errorSections"][0]["recoveryHref"],
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation%3Aen")

    def test_recovery_keeps_every_sound_value(self):
        # book is broken; chapter and bible are sound and survive; the broken
        # key falls to the default rather than being guessed.
        self.assertEqual(self.page("invalid-chapter")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")
        self.assertEqual(self.page("invalid-voice")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")

    def test_the_recovery_link_recovers(self):
        recovered = self.snapshot("invalid-recovery", "recovered")
        self.assertFalse(recovered["errorSections"])
        self.assertEqual(recovered["referenceText"], "Genesis 1")
        self.assertEqual(recovered["fragmentCount"], 107)

    def test_an_invalid_hashchange_replaces_rather_than_leaves_stale_content(self):
        broken = self.snapshot("hashchange-invalid", "broken")
        self.assertEqual(broken["hash"], "#book=Gen&chapter=99&bible=douay-rheims")
        self.assertTrue(broken["errorSections"])
        self.assertEqual(broken["fragmentCount"], 0,
                         "the stale chapter must not stand under the broken address")

    def test_the_controls_take_defaults_but_the_page_does_not_render_them(self):
        page = self.page("invalid-book")
        self.assertEqual(page["selectValues"]["book"], "Gen")
        self.assertEqual(page["fragmentCount"], 0)


class VoiceDeepLinkTest(ReplayTest):
    """Finding 5 — the deferred `voice` deep link, ported from the candidate.

    `start()` used to assign the hash's voice before any option carrying it
    existed; the selection read back empty and the reader's URL was rewritten
    without the key they were sent.
    """

    def test_a_voice_the_chapter_holds_is_honoured_and_kept_in_the_hash(self):
        page = self.page("voice-held")
        self.assertEqual(page["voice"], "translation:en")
        # The arriving address parses to the rendered state, so it is kept
        # byte for byte — no canonicalising rewrite, no extra history entry.
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:en")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["fragmentCount"], 14)
        self.assertTrue(any("Showing English translation only" in one
                            for one in page["asideNotes"]))

    def test_a_voice_the_chapter_lacks_is_kept_and_named_rather_than_widened(self):
        page = self.page("voice-not-held")
        self.assertEqual(page["voice"], "translation:de")
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:de")
        self.assertEqual(page["hashWrites"], [])
        self.assertIn("German translation — none here", page["voiceLabels"])
        self.assertEqual(page["fragmentCount"], 0)

    def test_the_page_no_longer_assigns_the_voice_before_the_options_exist(self):
        script = held(CATENA / "catena.js")
        # The deferral now lives in `seedControls`, the one seeding every
        # arrival shares; no path assigns a cited voice straight to the
        # control before an option can hold it.
        self.assertNotIn("voiceSelect.value = hash.get('voice')", script)
        self.assertNotIn("voiceSelect.value = next.get('voice')", script)
        self.assertIn("wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';",
                      script)
        self.assertIn("const wanted = voiceSelect.value || wantedVoice;", script)


class HistoryDeterminismTest(ReplayTest):
    """Finding 5 — Back and Forward both render, deterministically.

    The shared `T.onHashChange` recognises the router's own writes by a
    remembered string (`lastWritten`, shared/browser-core.js:937-961); after
    Back restores a hash the router's write finds it already in place,
    returns early, and the remembered string goes stale — Forward is then
    swallowed. The route now compares the arriving hash against what its
    current state would write, so its own echoes are skipped and every
    reader move renders. The shared swallow itself remains the shared
    owner's to fix.
    """

    def test_stepping_writes_the_new_chapter_to_the_url(self):
        stepped = self.snapshot("back-forward", "stepped")
        self.assertEqual(stepped["hash"], "#book=Gen&chapter=2&bible=douay-rheims")
        self.assertEqual(stepped["referenceText"], "Genesis 2")

    def test_back_restores_the_earlier_chapter(self):
        back = self.snapshot("back-forward", "back")
        self.assertEqual(back["referenceText"], "Genesis 1")
        self.assertEqual(back["selectValues"]["chapter"], "1")
        self.assertEqual(back["hash"], "#book=Gen&chapter=1&bible=douay-rheims")

    def test_forward_after_back_renders_rather_than_being_swallowed(self):
        forward = self.snapshot("back-forward", "forward")
        self.assertEqual(forward["referenceText"], "Genesis 2")
        self.assertEqual(forward["selectValues"]["chapter"], "2")

    def test_the_route_listens_for_itself_rather_than_through_the_stale_swallow(self):
        script = held(CATENA / "catena.js")
        self.assertNotIn("T.onHashChange(", script)
        self.assertIn("window.addEventListener('hashchange'", script)
        self.assertIn("window.location.hash === currentHashText()", script)

    def test_an_equivalent_arrival_address_is_never_rewritten(self):
        # Scrambled order, `chapter=01`, `%3A`, and an unknown key all parse
        # to the state the page renders; rewriting any of them would push a
        # history entry Back could only bounce off.
        page = self.page("noncanonical-arrival")
        self.assertEqual(
            page["hash"],
            "#chapter=01&book=Gen&bible=douay-rheims&voice=translation%3Aen&note=kept")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["referenceText"], "Genesis 1")
        self.assertEqual(page["voice"], "translation:en")

    def test_a_partial_arrival_is_completed_in_place_not_by_pushing(self):
        page = self.page("partial-arrival")
        self.assertEqual(page["hashWrites"], [],
                         "arrival normalisation must not push a history entry")
        self.assertEqual(page["replaced"], ["#book=Gen&chapter=1&bible=douay-rheims"])
        self.assertEqual(page["hash"], "#book=Gen&chapter=1&bible=douay-rheims")

    def test_a_hashless_arrival_is_completed_in_place_not_by_pushing(self):
        page = self.page("no-hash-arrival")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], ["#book=Gen&chapter=1&bible=douay-rheims"])

    def test_reader_actions_still_push_exactly_one_entry(self):
        # The chapter step is the one page-initiated write in the scenario;
        # the initial canonical arrival and both history moves write nothing.
        page = self.page("back-forward")
        self.assertEqual(page["hashWrites"], ["#book=Gen&chapter=2&bible=douay-rheims"])


class UrlGrammarClosureTest(ReplayTest):
    """Finding 5, second pass — the parser validates the complete multimap.

    A recognized key cited twice is refused even when the citations agree
    (the reader-state contract: a semantic URL key occurs at most once);
    a malformed percent sequence stays literal in URLSearchParams and must
    fail the closed value grammars; and `voice` is a CLOSED grammar — no
    suffix, no whitespace, no second colon. Mixed valid + invalid keys are
    pinned by `invalid-book-with-voice` above.
    """

    def test_an_identical_duplicate_key_fails_closed(self):
        self.assert_failed_closed(
            "duplicate-key-identical", "#book=Gen&book=Gen&chapter=1&bible=douay-rheims",
            "book=Gen, Gen is cited more than once")

    def test_a_contradictory_duplicate_key_fails_closed(self):
        self.assert_failed_closed(
            "duplicate-key-conflicting", "#book=Gen&chapter=1&bible=douay-rheims&book=Foo",
            "book=Gen, Foo is cited more than once")

    def test_malformed_percent_encoding_fails_closed(self):
        # URLSearchParams keeps the undecodable sequence literal; the closed
        # book grammar refuses it, and the address stays as written.
        self.assert_failed_closed(
            "malformed-encoding", "#book=G%ZZen&chapter=1&bible=douay-rheims",
            "book=G%ZZen is not a book of this canon")

    def test_a_voice_with_a_suffix_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice-suffix", GEN1 + "&voice=translation:en:extra",
            "voice=translation:en:extra is not a voice")

    def test_a_voice_with_whitespace_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice-space", GEN1 + "&voice=translation:%20en",
            "voice=translation: en is not a voice")

    def test_chapter_zero_fails_closed(self):
        self.assert_failed_closed(
            "chapter-zero", "#book=Gen&chapter=0&bible=douay-rheims",
            "chapter=0 is not a chapter of Genesis, which has 50")

    def test_a_negative_chapter_fails_closed(self):
        self.assert_failed_closed(
            "chapter-negative", "#book=Gen&chapter=-1&bible=douay-rheims",
            "chapter=-1 is not a chapter of Genesis, which has 50")

    def test_a_nonnumeric_chapter_fails_closed(self):
        self.assert_failed_closed(
            "chapter-nonnumeric", "#book=Gen&chapter=two&bible=douay-rheims",
            "chapter=two is not a chapter of Genesis, which has 50")


class HistoryIndependenceTest(ReplayTest):
    """Finding 5, second pass — one invalid URL renders ONE page.

    The correction review found identical invalid addresses rendering
    differently depending on the controls the reader left behind. Every
    arrival now reseeds the controls from the address and the data alone,
    so a cold paste, a hashchange over a valid page, and Back/Forward all
    land on identical rendered state.
    """

    def test_an_invalid_arrival_over_a_valid_page_matches_the_cold_arrival(self):
        over = self.snapshot("invalid-after-navigation", "broken")
        self.assertEqual(self.rendered_state(over),
                         self.rendered_state(self.page("invalid-chapter")))

    def test_back_and_forward_land_on_the_same_invalid_page(self):
        broken = self.snapshot("invalid-back-forward", "broken")
        forward = self.snapshot("invalid-back-forward", "forward")
        self.assertEqual(self.rendered_state(broken), self.rendered_state(forward))
        self.assertEqual(self.rendered_state(forward),
                         self.rendered_state(self.page("invalid-book")))

    def test_a_mixed_invalid_arrival_leaves_no_stale_valid_controls(self):
        over = self.snapshot("invalid-after-navigation", "broken")
        self.assertEqual(over["selectValues"],
                         {"book": "Gen", "chapter": "1", "bible": "douay-rheims"})
        self.assertEqual(over["voiceLabels"], ["Everything held"])
        self.assertEqual(over["stepButtons"], [True, False],
                         "the step buttons must reflect the reseeded controls")
        self.assertEqual(over["referenceText"], "Address not recognised")


class RecoveryFocusTest(ReplayTest):
    """Finding 5 / robustness, second pass — recovery keeps the reader.

    Following the recovery link destroys the link itself; focus must land
    on the reading region (`tabindex="-1"`, the skip-link target), with
    exactly one announcement per state. Recovery through a control keeps
    focus on that control.
    """

    def test_keyboard_recovery_moves_focus_to_the_reading_region(self):
        recovered = self.snapshot("keyboard-recovery", "recovered")
        self.assertFalse(recovered["errorSections"])
        self.assertEqual(recovered["referenceText"], "Genesis 1")
        self.assertEqual(recovered["fragmentCount"], 107)
        self.assertEqual(recovered["activeElement"], "reading",
                         "focus must not be stranded on the removed link")

    def test_recovery_announces_the_new_page_exactly_once(self):
        spoken = self.snapshot("keyboard-recovery", "recovered")["statusWrites"]
        self.assertEqual(len(spoken), 2, spoken)
        self.assertIn("The address could not be read", spoken[0])
        self.assertTrue(spoken[1].startswith("Genesis 1, "), spoken[1])

    def test_the_recovered_address_is_the_links_own_text(self):
        recovered = self.snapshot("keyboard-recovery", "recovered")
        self.assertEqual(recovered["hash"], "#book=Gen&chapter=1&bible=douay-rheims")
        self.assertEqual(recovered["hashWrites"], [],
                         "following a link is not a page-initiated write")

    def test_recovery_through_a_control_keeps_focus_on_the_control(self):
        recovered = self.snapshot("control-recovery", "recovered")
        self.assertFalse(recovered["errorSections"])
        self.assertEqual(recovered["referenceText"], "Genesis 2")
        self.assertEqual(recovered["activeElement"], "chapter-select")
        self.assertEqual(recovered["hashWrites"],
                         ["#book=Gen&chapter=2&bible=douay-rheims"],
                         "a reader action pushes exactly one entry")

    def test_an_invalid_arrival_speaks_exactly_once(self):
        self.assertEqual(
            self.page("invalid-book")["statusWrites"],
            ["The address could not be read; its invalid values are shown, unchanged."])


class AsyncTransactionTest(ReplayTest):
    """Finding 5, second pass — every async completion proves ownership.

    Deferred requests interleave real overtaking navigations: a stale
    success may not repaint, a stale failure may not overwrite, a current
    failure belongs to the route the URL describes, and in a rapid
    A -> B -> C only C commits — in success and failure permutations.
    """

    def test_a_stale_success_does_not_repaint_the_newer_route(self):
        late = self.snapshot("race-stale-success", "a-late")
        self.assertEqual(late["referenceText"], "Genesis 2")
        self.assertEqual(late["hash"], GEN2)
        self.assertFalse(late["errorSections"])
        self.assertEqual(self.rendered_state(late),
                         self.rendered_state(self.snapshot("race-stale-success", "b-committed")))

    def test_a_stale_failure_does_not_erase_the_newer_route(self):
        late = self.snapshot("race-stale-failure", "a-late")
        self.assertEqual(late["referenceText"], "Genesis 2")
        self.assertFalse(late["errorSections"])
        self.assertFalse(any("could not be loaded" in one for one in late["statusWrites"]))
        self.assertEqual(self.rendered_state(late),
                         self.rendered_state(self.snapshot("race-stale-failure", "b-committed")))

    def test_a_failing_action_owns_its_error_and_writes_its_address(self):
        failed = self.snapshot("race-b-fails", "b-failed")
        self.assertEqual(failed["referenceText"], "Genesis 2")
        self.assertEqual(failed["hash"], GEN2, "the URL must still describe B")
        self.assertEqual(failed["hashWrites"], [GEN2],
                         "the failed action still writes its route, once")
        self.assertTrue(any("could not be loaded" in one for one in failed["statusWrites"]))
        self.assertEqual(failed["fragmentCount"], 0,
                         "no stale Genesis 1 content may stand under the failure")

    def test_a_failing_arrival_owns_its_error_without_a_pushing_write(self):
        failed = self.snapshot("race-b-fails-arrival", "b-failed")
        self.assertEqual(failed["referenceText"], "Genesis 2")
        self.assertEqual(failed["hash"], GEN2)
        self.assertEqual(failed["hashWrites"], [],
                         "an arrival never becomes a pushing write, even failing")
        self.assertEqual(failed["fragmentCount"], 0)

    def test_rapid_navigation_commits_only_the_last_route(self):
        for name in ("race-rapid", "race-rapid-failure"):
            with self.subTest(scenario=name):
                late = self.snapshot(name, "b-late")
                self.assertEqual(late["referenceText"], "Genesis 42")
                self.assertEqual(late["hash"], GEN42)
                self.assertFalse(late["errorSections"])
                self.assertEqual(late["fragmentCount"], 3)


class CacheRecoveryTest(ReplayTest):
    """Second pass — a rejected load is evicted, so retry is real.

    The first correction cached rejected spine/text promises forever: the
    page offered "reloading may recover it" while never asking again, and
    the fragment retry re-consumed the same rejection.
    """

    def test_a_failed_spine_is_reasked_on_return_and_recovers(self):
        failed = self.snapshot("spine-retry", "failed")
        self.assertTrue(any("could not be loaded" in one for one in failed["statusWrites"]))
        recovered = self.snapshot("spine-retry", "recovered")
        self.assertEqual(recovered["referenceText"], "Genesis 1")
        self.assertEqual(recovered["fragmentCount"], 107)
        asked = [one for one in recovered["fetched"]
                 if one == "structure/catena/01-gen/001.json"]
        self.assertEqual(len(asked), 2, "the return visit must really ask again")

    def test_a_failed_fragment_text_retries_and_recovers(self):
        failed = self.snapshot("fragment-retry", "failed")
        self.assertTrue(any("could not be loaded" in one for one in failed["fragmentTexts"]))
        recovered = self.snapshot("fragment-retry", "recovered")
        self.assertTrue(
            [one for one in recovered["fragmentTexts"]
             if one != "Loading…" and "could not be loaded" not in one],
            "the reopened fragment must show its recovered text")
        asked = [one for one in recovered["fetched"]
                 if one.startswith("structure/catena/text/")]
        self.assertEqual(len(asked), 2, "the retry must really ask again")

    def test_a_late_text_completion_cannot_touch_the_new_page(self):
        late = self.snapshot("fragment-toggle-race", "late")
        self.assertEqual(late["referenceText"], "Genesis 2")
        self.assertTrue(all(one == "Loading…" for one in late["fragmentTexts"]),
                        "the overtaken completion must not surface anywhere")


class BootstrapFailureTest(ReplayTest):
    """Robustness, second pass — a failed bootstrap tells the truth.

    An index or manifest that never arrives used to leave "Loading…"
    standing in the reference and all four selects forever. The failure now
    renders as one, and the single status channel says why, once.
    """

    def test_a_missing_index_leaves_no_permanent_loading(self):
        page = self.page("bootstrap-failure")
        self.assertEqual(page["referenceText"], "Unavailable")
        self.assertEqual(page["bookLabels"], ["Unavailable"])
        self.assertEqual(page["voiceLabels"], ["Unavailable"])
        self.assertFalse(page["staticEntry"], "the failure replaces the static entry")
        self.assertEqual(len(page["statusWrites"]), 1, page["statusWrites"])
        self.assertIn("The catena index could not be loaded", page["statusWrites"][0])

    def test_a_missing_manifest_leaves_no_permanent_loading(self):
        page = self.page("bootstrap-bibles-failure")
        self.assertEqual(page["referenceText"], "Unavailable")
        self.assertEqual(page["bookLabels"], ["Unavailable"])
        self.assertEqual(len(page["statusWrites"]), 1, page["statusWrites"])
        self.assertIn("The translation list could not be loaded", page["statusWrites"][0])


class TypedTruthStateTest(ReplayTest):
    """Finding 8, second pass — one typed state; contradictions impossible.

    A synthetic blocked record used to render "Nothing held here", "No
    commentary ... held yet" and "Held, and not renderable yet" at once,
    because the tally counted only renderable fragments while blocked rows
    rendered separately. Blocked-but-held is HELD: the absence copy may
    appear only when no fragment AND no blocked row is held, and integrity,
    invalid and failed states manufacture no absence labels at all.
    """

    def test_a_blocked_only_chapter_never_claims_nothing_held(self):
        page = self.page("held-unrenderable")
        self.assertEqual(
            page["tallyText"],
            "1 work held, not renderable yet"
            " · 2 lead entries on the acquisition list")
        self.assertNotIn("Nothing", page["tallyText"])
        self.assertNotIn("No commentary on this chapter is held yet.",
                         page["asideNotes"])
        self.assertIn("Held, and not renderable yet", page["sectionHeadings"])
        self.assertIn("1 work held, not renderable yet", page["statusText"])

    def test_the_blocked_only_empty_note_points_at_the_held_rows(self):
        self.assertIn(
            "Nothing held on this chapter is renderable yet; what is held, "
            "and why it cannot be shown, stands below.",
            self.page("held-unrenderable")["asideNotes"])

    def test_blocked_rows_beside_fragments_count_in_the_same_tally(self):
        page = self.page("blocked-with-held")
        self.assertEqual(
            page["tallyText"],
            "107 fragments held · 1 work held, not renderable yet"
            " · 33 lead entries on the acquisition list")
        self.assertIn("Held, and not renderable yet", page["sectionHeadings"])
        self.assertEqual(page["fragmentCount"], 107)
        self.assertEqual(len(page["blocked"]), 1)

    def test_true_absence_still_says_nothing_held(self):
        page = self.page("nothing-held")
        self.assertEqual(page["tallyText"], "Nothing held here")
        self.assertIn("No commentary on this chapter is held yet.",
                      page["asideNotes"])
        self.assertFalse(page["blocked"])

    def test_an_integrity_failure_manufactures_no_voice_absence(self):
        # The review: "Integrity and invalid states can also label a
        # selected voice 'none here'." An unloadable record proves nothing
        # held OR absent, so the kept selection claims nothing.
        page = self.page("integrity-404-voice")
        self.assertEqual(page["voiceLabels"],
                         ["Everything held", "English translation"])
        self.assertEqual(page["voice"], "translation:en")
        self.assertEqual(page["tallyText"], "The commentary record did not load")
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:en")

    def test_a_failed_load_manufactures_no_absence_claims(self):
        # After a transport failure the tally is cleared, the voice control
        # is reseeded without a "none here" claim, and no stale corpus
        # count stands under the failure.
        failed = self.snapshot("race-b-fails", "b-failed")
        self.assertEqual(failed["tallyText"], "")
        self.assertFalse([one for one in failed["voiceLabels"]
                          if "none here" in one])

    def test_every_state_keeps_its_own_node(self):
        # Exact state-to-node association: each typed claim renders on the
        # node that carries its `data-state`, and never on another page.
        blocked = self.page("held-unrenderable")
        self.assertEqual(blocked["blocked"],
                         ["Anonymous — Catena in Genesimthe witness is held only "
                          "as page images, and no text has been read off them"])
        self.assertIn("blocked", blocked["dataStates"])
        self.assertNotIn("error", blocked["dataStates"])
        integrity = self.page("integrity-404")
        self.assertIn("error", integrity["dataStates"])
        for absent in ("blocked", "lead", "absence"):
            self.assertNotIn(absent, integrity["dataStates"])
        invalid = self.page("invalid-book")
        self.assertEqual(invalid["dataStates"], ["error"])

    def test_no_state_ever_collapses_into_absence(self):
        # The rejection sweep the review demanded: across EVERY replayed
        # page and snapshot, a blocked row never stands beside an absence
        # claim, and an error or unloaded record never claims absence,
        # emptiness, a "none here" voice or an acquisition-list clause.
        for name in self.pages:
            page = self.page(name)
            snaps = [("final", page)] + list(page.get("snapshots", {}).items())
            for label, snap in snaps:
                with self.subTest(scenario=name, snapshot=label):
                    tally = snap["tallyText"] or ""
                    if snap["blocked"]:
                        self.assertNotIn("Nothing", tally)
                        self.assertNotIn(
                            "No commentary on this chapter is held yet.",
                            snap["asideNotes"])
                    if ("error" in snap["dataStates"]
                            or tally == "The commentary record did not load"
                            or tally == ""):
                        self.assertNotIn("none in", tally)
                        self.assertNotIn("Nothing", tally)
                        self.assertNotIn("acquisition list", tally)
                        self.assertFalse([one for one in snap["voiceLabels"]
                                          if "none here" in one])


class SeverianRightsTraceTest(ReplayTest):
    """Finding 4, real-payload half — real Severian metadata, end to end.

    The tracked PTA edition record carries the CC BY-SA 4.0 licence basis
    and the Voicu / von Stockhausen / BBAW attribution; the generated spine
    still reduces it to `rights: "licensed"` (a recorded generator
    prerequisite). The trace drives the REAL tracked string through the
    chapter payload and the route to the rendered point-of-use
    acknowledgement over the real fragments and real Greek text files, so
    the route is proved faithful before the generator projection lands.
    """

    def test_the_tracked_record_really_carries_the_terms(self):
        self.assertIn("CC BY-SA 4.0", SEVERIAN_BASIS)
        self.assertIn("Sever J. Voicu", SEVERIAN_BASIS)
        self.assertIn("Annette von Stockhausen", SEVERIAN_BASIS)
        self.assertIn("Berlin-Brandenburgische Akademie der Wissenschaften",
                      SEVERIAN_BASIS)

    def test_the_spine_still_reduces_the_terms_to_licensed(self):
        # The generator-owned gap this trace does NOT close, pinned so the
        # trace cannot be mistaken for the projection itself.
        spine = json.loads(
            (ROOT / "src/web/data/structure/catena/01-gen/001.json")
            .read_text(encoding="utf-8"))
        severian = spine["sources"]["6"]
        self.assertEqual(severian["rights"], "licensed")
        self.assertNotIn("acknowledgement", severian)
        self.assertNotIn("rights_basis", severian)
        self.assertIn("Sever J. Voicu", severian["edition_published"])

    def test_the_projected_acknowledgement_renders_verbatim_once_per_fragment(self):
        opened = self.snapshot("severian-projected", "opened")
        self.assertEqual(opened["acknowledgements"],
                         ["Licence: " + SEVERIAN_BASIS] * 5,
                         "five Severian fragments stand on Genesis 1, each "
                         "carrying the one acknowledgement exactly once")
        self.assertTrue(all(opened["acknowledgementAboveText"]))

    def test_the_real_greek_prose_stands_beneath_the_terms(self):
        opened = self.snapshot("severian-projected", "opened")
        texts = [one for one in opened["fragmentTexts"] if one != "Loading…"]
        self.assertEqual(len(texts), 1)
        self.assertGreater(len(texts[0]), 100,
                           "the real homily text file renders beneath it")


class AbsenceDisclosureTest(ReplayTest):
    """Robustness, second pass — absence findings are not deferred.

    Per-work translation-absence reasons sat in a CLOSED disclosure despite
    the non-deferrable absence contract. The disclosure now stands OPEN on
    arrival — the reasons are visible without interaction — and a reader
    may only fold them away; partly-public-domain material stays counted
    apart from what the project may not publish at all.
    """

    def test_the_absence_disclosure_stands_open_on_arrival(self):
        page = self.page("voice-held")
        self.assertTrue(page["absenceSummary"])
        self.assertTrue(page["absenceOpen"],
                        "the reasons must be visible without interaction")
        self.assertEqual(len(page["absenceReasons"]), 8)
        self.assertEqual(len(page["absencePartials"]), 2)

    def test_the_empty_voice_chapter_also_opens_its_absences(self):
        page = self.page("voice-empty-chapter")
        if page["absenceSummary"]:
            self.assertTrue(page["absenceOpen"])


class RecoveryFailureFocusTest(ReplayTest):
    """Adversarial audit R1, finding F1 — a recovery that FAILS keeps the reader.

    Both success arms captured and restored focus (`refocus` in `render()`,
    and `renderInvalid`), but `render()`'s catch arm did not: `T.fail` clears
    the reading region, taking with it the recovery link the keyboard reader
    was standing on, and nothing restored focus. That is the reviewer's
    "invalid-state recovery loses focus" defect (spec §8, "do not strand
    focus in a removed control") surviving on the failure path, reachable by
    any action that fails while focus is inside `#reading`.
    """

    def test_the_reader_really_stands_on_the_link_the_failure_removes(self):
        # Without this the rest proves nothing: the anchor must hold focus
        # while the route it recovered to is still in flight.
        pending = self.snapshot("recovery-load-fails", "pending")
        self.assertEqual(pending["activeElement"], "a")
        self.assertEqual(pending["referenceText"], "Genesis 1")

    def test_a_failing_recovery_hands_focus_to_the_reading_region(self):
        failed = self.snapshot("recovery-load-fails", "failed")
        self.assertEqual(failed["activeElement"], "reading",
                         "the audit found focus left on the removed anchor")
        self.assertEqual(failed["classes"], ["error"],
                         "the failure notice is all that stands in the region")
        self.assertFalse(failed["errorSections"])

    def test_the_failing_recovery_speaks_once_and_claims_nothing(self):
        failed = self.snapshot("recovery-load-fails", "failed")
        self.assertEqual(len(failed["statusWrites"]), 2, failed["statusWrites"])
        self.assertIn("This chapter could not be loaded", failed["statusWrites"][1])
        self.assertEqual(failed["tallyText"], "")
        self.assertEqual(failed["voice"], "translation:en")
        self.assertEqual(failed["voiceLabels"],
                         ["Everything held", "English translation"],
                         "a failed load proves no voice absent")

    def test_the_failing_recovery_leaves_the_recovered_address_alone(self):
        failed = self.snapshot("recovery-load-fails", "failed")
        self.assertEqual(
            failed["hash"],
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation%3Aen")
        self.assertEqual(failed["hashWrites"], [])
        self.assertEqual(failed["replaced"], [],
                         "the address already describes the failed route")


class SupersededArrivalVoiceTest(ReplayTest):
    """Adversarial audit R1, finding F2 — a superseded arrival keeps its voice.

    `wantedVoice` parks a deep-linked voice until an option can hold it, but
    only `fillVoices` consumed it and a discarded render never reaches
    `fillVoices`. A reader action taken while the arrival's spine was still
    in flight then adopted the abandoned route's voice — selecting it,
    rendering under it and pushing it into history, though no rendered page
    ever showed it and the reader never chose it (§7 "nothing borrowed from a
    leftover selection", §9). A render that is not an arrival's now clears
    the parked voice before it can be read.
    """

    def test_the_arrival_really_parks_its_voice_before_the_reader_acts(self):
        parked = self.snapshot("parked-voice-superseded", "parked")
        self.assertEqual(parked["hash"], GEN2 + "&voice=translation:la")
        self.assertEqual(parked["voice"], "", "no option can hold it yet")
        self.assertEqual(parked["referenceText"], "Genesis 2")

    def test_the_readers_own_action_renders_the_readers_own_voice(self):
        reader = self.snapshot("parked-voice-superseded", "reader")
        self.assertEqual(reader["referenceText"], "Genesis 3")
        self.assertEqual(reader["voice"], "")
        self.assertEqual(reader["voiceLabels"],
                         ["Everything held", "The author’s own language",
                          "English translation"],
                         "a Latin translation was never a voice of this page")
        self.assertEqual(reader["fragmentCount"], 86)

    def test_the_pushed_address_is_the_readers_own_route(self):
        reader = self.snapshot("parked-voice-superseded", "reader")
        self.assertEqual(reader["hash"], GEN3)
        self.assertNotIn("voice", reader["hash"])
        self.assertEqual(reader["hashWrites"], [GEN3],
                         "the abandoned arrival's voice may not ride the push")

    def test_the_overtaken_spine_changes_nothing_when_it_lands(self):
        self.assertEqual(
            self.rendered_state(self.snapshot("parked-voice-superseded", "late")),
            self.rendered_state(self.snapshot("parked-voice-superseded", "reader")))
        self.assertEqual(
            self.page("parked-voice-superseded")["tallyText"],
            "86 fragments held · 31 lead entries on the acquisition list")


class SelfWriteEchoTest(ReplayTest):
    """Adversarial audit R2, finding F1 — the route's own echo cannot revert it.

    A `location.hash` assignment and the browser's `hashchange` dispatch are
    one task apart. The listener recognised its own write by comparing the
    arriving hash against what the CURRENT controls would write, so a reader
    who acted inside that window (key-repeat arrows, a second select) moved
    the controls out from under the comparison: the echo was then read as a
    reader navigation, `onArrival` reseeded the controls back to the OLD
    route, and the reader's in-flight render was discarded as stale — page
    and URL ending on a chapter the reader had already left, which §9
    forbids ("an obsolete request must not mutate newer state"). The route
    now records the exact text it wrote and consumes that echo once.
    """

    def test_the_echo_lands_after_the_reader_has_already_moved(self):
        pending = self.snapshot("echo-after-action", "pending")
        self.assertEqual(pending["selectValues"]["chapter"], "3")
        self.assertEqual(pending["hash"], GEN2,
                         "the chapter-2 write is still the address; 3 has not committed")

    def test_the_echo_neither_speaks_nor_moves_the_controls(self):
        echo = self.snapshot("echo-after-action", "echo")
        self.assertEqual(echo["selectValues"]["chapter"], "3",
                         "the audit found the controls snapping back to 2")
        self.assertEqual(echo["referenceText"], "Genesis 3")
        self.assertEqual(len(echo["statusWrites"]), 2, echo["statusWrites"])
        self.assertEqual(
            self.rendered_state(echo),
            self.rendered_state(self.snapshot("echo-after-action", "pending")),
            "the echo may change nothing at all")

    def test_the_readers_render_still_commits_after_its_own_echo(self):
        page = self.page("echo-after-action")
        self.assertEqual(page["referenceText"], "Genesis 3")
        self.assertEqual(page["selectValues"]["chapter"], "3")
        self.assertEqual(page["fragmentCount"], 86)
        self.assertEqual(page["hash"], GEN3)
        self.assertEqual(page["hashWrites"], [GEN2, GEN3],
                         "one write per commit, and no write for the echo")
        self.assertEqual(len(page["statusWrites"]), 3, page["statusWrites"])
        self.assertTrue(page["statusWrites"][2].startswith("Genesis 3, "),
                        page["statusWrites"][2])

    def test_the_quiet_echo_stays_inert(self):
        committed = self.snapshot("echo-unmoved", "committed")
        echo = self.snapshot("echo-unmoved", "echo")
        self.assertEqual(self.rendered_state(echo), self.rendered_state(committed))
        self.assertEqual(echo["statusWrites"], committed["statusWrites"],
                         "an echo is silent whether or not the reader moved")
        self.assertEqual(echo["fetched"], committed["fetched"],
                         "and asks for nothing")

    def test_the_route_consumes_its_own_write_by_identity(self):
        # By the identity of the write, not by a comparison against controls
        # the reader may already have moved.
        #
        # CHANGED PIN: the text is remembered before the SHARED writer pushes
        # it. The first correction assigned `location.hash` here directly,
        # which dropped the published `T.writeHash([...])` pair literal that
        # `test_browser_url_contract` requires of every instrument (its
        # WRITTEN_HASH_KEYS registry, and catena is not a COMPUTED_HASH_WRITERS
        # entry). `currentHashText` serializes exactly what that writer writes,
        # so the remembered text still matches the echo byte for byte.
        script = held(CATENA / "catena.js")
        self.assertIn("selfWrote = currentHashText();", script)
        self.assertIn("T.writeHash([['book', bookSelect.value],", script)
        self.assertIn(
            "if (window.location.hash === selfWrote) return void (selfWrote = null);",
            script)


class BlockedVoiceClaimTest(ReplayTest):
    """Adversarial audits R2 F2 and R1 F4 — a blocked row is not an absence.

    `fillVoices`' `unknown` flag covered the unfetched, invalid and failed
    states but not a standing blocked row, so a blocked-only chapter labelled
    the kept voice "— none here"; and beside blocked rows of unrecorded voice
    the chain's empty note and the tally's "none in X" clause asserted an
    absence the record cannot prove (§10, "held ... must not be summarized as
    'nothing held'"; "do not manufacture 'none here'"). A standing blocked
    row now suppresses the option's absence claim, scopes the chain's note to
    the RENDERABLE rows and withholds the counted clause — while a chapter
    with nothing blocked still states the absence it can prove.
    """

    def test_a_blocked_only_chapter_manufactures_no_voice_absence(self):
        page = self.page("blocked-voice-link")
        self.assertEqual(page["voiceLabels"],
                         ["Everything held", "English translation"])
        self.assertEqual(page["voice"], "translation:en")
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:en")
        self.assertEqual(page["tallyText"],
                         "1 work held, not renderable yet"
                         " · 2 lead entries on the acquisition list")
        self.assertEqual(page["asideNotes"][0],
                         "Nothing held on this chapter is renderable yet; what is "
                         "held, and why it cannot be shown, stands below.")
        self.assertFalse([one for one in page["asideNotes"]
                          if "is held in English translation" in one],
                         "no commentary-absence aside may stand beside held rows")

    def test_the_same_holds_for_a_voice_chosen_by_control(self):
        # Reached without an arrival to reseed anything: English chosen where
        # it IS held, then a move onto the blocked-only chapter.
        chosen = self.snapshot("blocked-voice-control", "chosen")
        self.assertIn("14 in English translation", chosen["tallyText"])
        moved = self.snapshot("blocked-voice-control", "moved")
        self.assertEqual(moved["voice"], "translation:en")
        self.assertEqual(moved["voiceLabels"],
                         ["Everything held", "English translation"])
        self.assertEqual(moved["tallyText"],
                         "1 work held, not renderable yet"
                         " · 2 lead entries on the acquisition list")
        self.assertEqual(moved["asideNotes"][0],
                         "Nothing held on this chapter is renderable yet; what is "
                         "held, and why it cannot be shown, stands below.")
        self.assertEqual(moved["hash"], GEN2 + "&voice=translation%3Aen")

    def test_an_absence_beside_blocked_rows_covers_the_renderable_rows_only(self):
        page = self.page("blocked-beside-unshown-voice")
        self.assertEqual(page["voiceLabels"],
                         ["Everything held", "The author’s own language",
                          "English translation"])
        self.assertEqual(page["asideNotes"][0],
                         "No renderable commentary on this chapter is held in English "
                         "translation. 71 fragments are held here, in the author’s own "
                         "language; choose “Everything held” to see them.")
        self.assertEqual(page["tallyText"],
                         "71 fragments held · 1 work held, not renderable yet"
                         " · 28 lead entries on the acquisition list")
        self.assertNotIn("none in", page["tallyText"])
        self.assertEqual(page["statusText"],
                         "Genesis 10, Douay-Rheims (Challoner), 71 fragments held, "
                         "1 work held, not renderable yet, 28 lead entries on the "
                         "acquisition list.")

    def test_with_nothing_blocked_the_provable_absence_is_still_stated(self):
        # The contrast that keeps the suppression honest: the same chapter and
        # the same voice, with no blocked row, proves the absence and says so
        # in all three places the blocked case withholds it.
        page = self.page("voice-empty-chapter")
        self.assertIn("English translation — none here", page["voiceLabels"])
        self.assertIn("none in English translation", page["tallyText"])
        self.assertEqual(page["asideNotes"][0],
                         "No commentary on this chapter is held in English "
                         "translation. 71 fragments are held here, in the author’s own "
                         "language; choose “Everything held” to see them.")


class MalformedRecordRenderingTest(ReplayTest):
    """Adversarial audit R2, findings F3, F4 and F5 — broken values are not words.

    The typed-value discipline `sound()` covered the rights metadata but not
    the payload's own body (`text`, `basis`, `date_basis`), the lead rows or
    the blocked rows, so a malformed record printed "[object Object]" as a
    father's prose, "Extent — [object Object]" and "Date — 42" as apparatus,
    and "undefined — undefined" as an author. §10's "malformed data is not
    evidence of absence" cuts both ways: it is not renderable fact either
    (§12, fail-safe). Every one of those sinks is typed now, and a sound row
    standing beside the broken ones still renders in full.
    """

    def test_a_malformed_payload_body_renders_nothing_of_itself(self):
        opened = self.snapshot("malformed-record", "opened")
        self.assertEqual(opened["fragmentTexts"], [""],
                         "the audit found '[object Object]' as the fragment's words")
        self.assertEqual(opened["fragmentBases"], [],
                         "and 'Extent — [object Object]' and 'Date — 42' beneath them")

    def test_malformed_lead_rows_render_no_words_and_the_sound_row_does(self):
        page = self.page("malformed-record")
        self.assertEqual(page["leads"],
                         ["", "", "Origen — Homiliae in Genesim (240)"])
        # The COUNT stays the record's — three rows ARE on the acquisition
        # record for this chapter, and the note claims nothing more of them.
        self.assertIn("3 unreconciled lead entries on the acquisition record",
                      page["asideNotes"][0])

    def test_malformed_blocked_rows_name_no_author_and_the_sound_row_does(self):
        page = self.page("malformed-record")
        self.assertEqual(
            page["blocked"],
            ["", "", "Anonymous — Catena in Genesimheld only as page images"])
        self.assertEqual(page["tallyText"],
                         "1 fragment held · 3 works held, not renderable yet"
                         " · 3 lead entries on the acquisition list")

    def test_no_replayed_page_ever_coerces_a_value_into_words(self):
        # The sweep the audit's malformed matrices invite: across every
        # scenario and every snapshot, no rendered projection carries a
        # coercion artefact of a value the record did not supply as text.
        for name in self.pages:
            page = self.page(name)
            snaps = [("final", page)] + list(page.get("snapshots", {}).items())
            for label, snap in snaps:
                with self.subTest(scenario=name, snapshot=label):
                    rendered = json.dumps(self.rendered_state(snap), ensure_ascii=False)
                    for artefact in ("[object Object]", "undefined", "NaN"):
                        self.assertNotIn(artefact, rendered)


class AcknowledgementChannelOrderTest(ReplayTest):
    """Adversarial audit R2, observation O1 — a broken note cannot claim the channel.

    The one point-of-use acknowledgement channel is first-supply-wins, and a
    malformed spine acknowledgement used to take it outright: the marker
    rendered and a VALID payload acknowledgement arriving later was dropped —
    one supplied field silently erasing another independently relevant one,
    which §12 forbids. The channel now records whether what claimed it was
    SOUND: a malformed note is said once and still yields to a valid one,
    while a valid note already rendered is never displaced by a malformed
    note arriving after it, and no fragment ever shows two valid blocks.
    """

    def test_the_malformed_spine_note_is_said_once_before_any_payload_lands(self):
        start = self.snapshot("acknowledgement-order", "start")
        self.assertEqual(start["acknowledgements"],
                         ["The recorded acknowledgement is malformed and not shown.",
                          "Licence: Spine licence note, share alike."])
        self.assertEqual(start["fragmentTexts"], ["Loading…", "Loading…"])

    def test_a_valid_payload_note_still_renders_behind_a_malformed_spine_note(self):
        opened = self.snapshot("acknowledgement-order", "broken-spine-open")
        self.assertEqual(opened["acknowledgements"],
                         ["The recorded acknowledgement is malformed and not shown.",
                          "Licence: Payload licence note, CC BY-SA 4.0.",
                          "Licence: Spine licence note, share alike."])
        self.assertEqual(opened["fragmentTexts"], ["Payload words.", "Loading…"])

    def test_a_malformed_payload_note_displaces_no_valid_spine_note(self):
        page = self.page("acknowledgement-order")
        self.assertEqual(page["fragmentTexts"],
                         ["Payload words.", "Second payload words."])
        self.assertEqual(page["acknowledgements"],
                         ["The recorded acknowledgement is malformed and not shown.",
                          "Licence: Payload licence note, CC BY-SA 4.0.",
                          "Licence: Spine licence note, share alike."])
        self.assertEqual(
            page["acknowledgements"].count(
                "The recorded acknowledgement is malformed and not shown."),
            1, "the malformed note is said once, on the fragment that carries it")
        self.assertEqual(
            len([one for one in page["acknowledgements"]
                 if one.startswith("Licence: ")]), 2,
            "exactly one valid block on each of the two fragments")
        self.assertEqual(page["acknowledgementAboveText"], [True, True],
                         "and every block still stands above the prose")


class StaticDocumentTruthTest(unittest.TestCase):
    """Findings 6 and 8f — the static document is true without scripts.

    No permanent "Loading…", no static aria-busy, no disabled selects
    pretending to load; the main region owns real prose, an honest statement
    that this edition needs JavaScript, and working same-origin links. The
    footer's account of what opens agrees with what actually opens.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.page = held(CATENA / "index.html")

    def test_nothing_static_claims_to_be_loading(self):
        rendered = re.sub(r"<!--.*?-->", "", self.page, flags=re.S)
        self.assertNotIn("Loading", rendered)
        self.assertNotIn("aria-busy", rendered)
        self.assertNotIn('class="placeholder"', rendered)

    def test_the_selects_say_the_truth_as_served(self):
        self.assertEqual(self.page.count('<option value="">Needs JavaScript</option>'), 4)

    def test_the_main_region_owns_static_truth_and_browse_entries(self):
        main = self.page[self.page.index("<main"):self.page.index("</main>")]
        self.assertIn("static-entry", main)
        self.assertIn("needs JavaScript", main)
        self.assertIn('href="../sources/"', main)
        self.assertIn('href="../"', main)
        self.assertIn("rights", main)

    def test_the_controls_disclosure_is_static_open_and_wraps_the_form(self):
        self.assertIn('<details id="controls-filter" class="controls-filter" open>', self.page)
        self.assertIn("<summary>Change chapter and commentary voice</summary>", self.page)
        opening = self.page.index('<details id="controls-filter"')
        form = self.page.index('<form id="controls"')
        closing = self.page.index("</details>", opening)
        self.assertLess(opening, form)
        self.assertLess(self.page.index("</form>"), closing)

    def test_the_footer_agrees_with_what_actually_opens(self):
        # Conditional on rendering, so it is also true with scripts off.
        self.assertIn("Once the page renders, the chapter and the first commentator "
                      "stand open", self.page)
        self.assertNotIn("Everything here is closed until you open it", self.page)
        self.assertNotIn("stand open on arrival", self.page)

    def test_the_footer_keeps_its_six_entrances(self):
        for entrance in ("../scripture/", "../liturgy/", "../history/",
                         "../law/", "../sources/", "../texts/"):
            self.assertIn(f'href="{entrance}"', self.page)


class PrintStylesTest(unittest.TestCase):
    """Finding 6 — browser print is truthful and useful away from the page.

    Modelled on liturgy/reader-instrument.css and the corpus-foundation
    prototype (both read-only): interaction chrome goes, the reading order
    stands, and a print-only note says the paper copy is not canonical.

    The correction review added the other half of the truth: the printed
    chapter must name its Scripture edition ("The selected Douay-Rheims
    Scripture edition disappears when the controls are hidden"), and paper
    must not keep navigation, loopback links or interaction prose ("the
    printed footer still speaks of opening closed fragments and retains
    navigation"). Pagination keeps headings with their content ("page three
    is almost blank under an orphaned author heading").
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")
        cls.page = held(CATENA / "index.html")
        cls.block = media_block(cls.css, "@media print")
        # Every selector of every `display: none !important` rule, one by one.
        cls.hidden = [
            one.strip()
            for match in re.finditer(r"([^{}]+)\{([^{}]*)\}",
                                     without_comments(cls.block))
            if "display: none !important" in match.group(2)
            for one in match.group(1).split(",")]

    def test_the_interaction_chrome_is_hidden(self):
        # CHANGED PIN (review 2026-08-11, finding 6): `.controls-filter` is
        # no longer hidden wholesale — its two identity fields must print —
        # so what hides is its summary and every non-identity field.
        for chrome in (".catena-page .controls-filter > summary",
                    ".catena-page .controls .field:not(.print-identity)",
                    ".catena-page .author-filter-disclosure",
                    ".catena-page .skip-link", ".catena-page .banner"):
            self.assertIn(chrome, self.hidden)

    def test_the_loopback_navigation_and_recovery_links_are_hidden(self):
        # Ten "Open this passage in the Source Library" annotations, the six
        # footer entrances, the interaction paragraph and the error-recovery
        # link were all on paper; none belongs there.
        for interactive in (".catena-page .fragment-whole",
                            ".catena-page .footer-entrances",
                            ".catena-page .footer-interaction",
                            ".catena-page .error-recovery"):
            self.assertIn(interactive, self.hidden)

    def test_the_footer_split_matches_the_page(self):
        # The classes the print rules hide are the footer paragraphs that
        # speak of opening and of the other entrances; the paragraph that
        # states what the page holds carries neither class and prints.
        self.assertIn('<p class="footer-interaction">', self.page)
        self.assertIn('<p class="footer-entrances">', self.page)
        footer = self.page[self.page.index("<footer"):]
        self.assertEqual(footer.count("<p"), 3)
        self.assertEqual(footer.count('<p class="footer-'), 2)

    def test_the_scripture_edition_prints(self):
        # The mandated identity: the selected edition (and the commentary
        # voice beside it) survives into print as a plain line — Chromium
        # prints a select as its selected option's text.
        for selector in self.hidden:
            self.assertFalse(selector.endswith(".print-identity"),
                             f"{selector} hides the printed identity")
        self.assertIn(".catena-page .print-identity select", self.block)
        self.assertIn("appearance: none", self.block)
        # Folded controls must still print their identity lines.
        self.assertIn(".catena-page .controls-filter::details-content "
                      "{ content-visibility: visible; }", self.block)

    def test_the_identity_fields_are_the_bible_and_the_voice(self):
        for control in ("bible-select", "language-select"):
            field = self.page.index(f'<select id="{control}"')
            opened = self.page.rindex('<div class="field', 0, field)
            self.assertIn('class="field print-identity"',
                          self.page[opened:field], control)

    def test_pagination_keeps_headings_with_their_content(self):
        self.assertIn("orphans: 3", self.block)
        self.assertIn("widows: 3", self.block)
        self.assertIn("break-after: avoid", self.block)
        for kept in (".catena-page summary,", ".catena-page .section-heading,",
                     ".catena-page .reference-line { break-after: avoid; }"):
            self.assertIn(kept, self.block)
        # CHANGED PIN (review 2026-08-11, finding 6): `.author` left the
        # break-inside: avoid pair — a whole unbreakable author run is what
        # orphaned its heading — while a single fragment stays unbroken.
        self.assertIn(".catena-page .fragment { break-inside: avoid; }", self.block)
        self.assertNotIn(".author {", self.block)
        self.assertNotIn(".author,", self.block)
        for unit in (".fragment-source", ".fragment-acknowledgement",
                     ".paragraph-note"):
            self.assertIn(unit, self.block)

    def test_the_focus_overrides_are_gone(self):
        # CHANGED PIN (review 2026-08-11, finding 7): the route overrode the
        # accepted strong-blue shared focus role with a thinner violet rule.
        # The remedy is deference: no focus rule of any kind lives here, so
        # the shared universal `:focus-visible` outline governs.
        self.assertNotIn(":focus-visible", self.css)
        self.assertNotIn(":focus", self.css)

    def test_the_scripture_locus_is_a_heading(self):
        # Robustness finding: "the primary Scripture locus is absent from
        # heading navigation." The reference line is now an h2 under the
        # page's single h1, its ids and visual line unchanged.
        self.assertIn('<h2 class="reference-line">', self.page)
        self.assertIn("</h2>", self.page)
        self.assertNotIn('<p class="reference-line">', self.page)
        line = self.page[self.page.index('<h2 class="reference-line">'):]
        line = line[:line.index("</h2>")]
        self.assertIn('<span id="reference">', line)
        self.assertIn('id="reference-book"', line)
        self.assertEqual(self.page.count("<h1"), 1)

    def test_the_reading_order_returns_to_document_flow(self):
        self.assertIn(".catena-page .reading { display: block; }", self.block)

    def test_the_page_names_browser_print_as_non_canonical(self):
        self.assertIn("Browser print", self.block)
        self.assertIn("not a", self.block)
        self.assertIn("canonical rendering", self.block)

    def test_every_print_rule_is_scoped_to_the_page(self):
        for selector_list in re.findall(r"([^{}]+)\{", without_comments(self.block)):
            for one in selector_list.split(","):
                one = one.strip()
                if not one:
                    continue
                self.assertTrue(one.startswith(".catena-page"),
                                f"print rule {one!r} is not scoped to .catena-page")


class ForcedColorsTest(unittest.TestCase):
    """Finding 7 — the reserved paragraph edge does not lie in forced colors.

    Every paragraph reserves a transparent 2px border; forced-colors mode
    would materialise it as CanvasText and hand an ordinary passage the same
    mark as a projected boundary. The base forces to Canvas and only
    `.projected` takes CanvasText.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")
        cls.block = media_block(cls.css, "@media (forced-colors: active)")

    def test_the_base_border_forces_to_canvas_and_projected_to_canvastext(self):
        self.assertIn(".catena-page .passage-paragraph { border-left-color: Canvas; }",
                      self.block)
        self.assertIn(
            ".catena-page .passage-paragraph.projected { border-left-color: CanvasText; }",
            self.block)

    def test_the_base_rule_still_reserves_the_transparent_edge(self):
        reserved = " ".join(declarations_for(self.css, ".passage-paragraph"))
        self.assertIn("border-left: 2px solid transparent", reserved)

    def test_the_refusal_keeps_a_visible_rule(self):
        self.assertIn(".catena-page .refusal { border-left-color: CanvasText; }",
                      self.block)

    def test_focus_is_left_to_the_shared_sheet_here_too(self):
        # CHANGED PIN (review 2026-08-11, finding 7): this block used to remap
        # the route's own `:focus-visible` outlines to Highlight, which only
        # existed because the route overrode the accepted shared focus role.
        # Those overrides are deleted, so nothing here may touch focus either:
        # the shared 3px outline governs and the system forces its colour.
        self.assertNotIn(":focus", self.block)
        self.assertNotIn("outline", self.block)

    def test_presence_and_absence_stay_apart_by_line_style(self):
        # Solid (held) against dashed (lead/blocked/refusal) survives forced
        # colors because it is a style, not a colour; assert the styles.
        dashed = " ".join(declarations_for(self.css, ".lead"))
        self.assertIn("1px dashed", dashed)
        for selector in (".fragment", ".author"):
            for block in declarations_for(self.css, selector):
                self.assertNotIn("dashed", block)


class ComposedButNotSimplifiedTest(unittest.TestCase):
    """The composition reaches held commentary and stops there.

    The corrected composition speaks the shared sheet's own vocabulary — the
    candidate's one-off `--tp-*` palette is gone — and the protected
    epistemic selectors keep the section's palette, so they read apart from
    held commentary rather than with it.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")

    def test_no_second_palette_lives_in_this_stylesheet(self):
        self.assertNotIn("--tp-", self.css)
        # And nothing here declares custom properties or styles the shell.
        self.assertNotIn(":root", without_comments(self.css))
        for selector in re.findall(r"(?m)^([^\s@/][^{]*)\{", without_comments(self.css)):
            for one in selector.split(","):
                self.assertNotIn(one.strip(), {"html", "body"})

    def test_the_protected_selectors_that_were_declared_still_are(self):
        for selector in PROTECTED_AND_DECLARED:
            with self.subTest(selector=selector):
                self.assertTrue(declarations_for(self.css, selector),
                                f"{selector} is no longer declared at all")

    def test_the_absence_selectors_stay_deliberately_undeclared(self):
        for selector in PROTECTED_SELECTORS[:4]:
            with self.subTest(selector=selector):
                self.assertFalse(
                    declarations_for(self.css, selector),
                    f"{selector} gained rules; undeclared is the protected state")

    def test_a_projected_break_is_still_drawn_and_a_printed_one_is_not(self):
        blocks = declarations_for(self.css, ".passage-paragraph.projected")
        base = [one for one in blocks if "CanvasText" not in one]
        self.assertEqual(len(base), 1)
        self.assertIn("border-left-color: var(--section-pale)", base[0])

    def test_an_extent_crossing_a_boundary_is_not_normalised_into_the_chips(self):
        spans = " ".join(declarations_for(self.css, ".spans"))
        self.assertIn("color: var(--section-ink)", spans)
        self.assertIn("font-weight: 600", spans)
        chips = declarations_for(self.css, ".fragment-extent")
        self.assertTrue(any("--ink-soft" in one for one in chips),
                        "the extent itself joins the normalised card catalogue")

    def test_the_card_catalogue_speaks_one_voice(self):
        catalogue = None
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(self.css)):
            names = {one.strip() for one in block.group(1).split(",")}
            if names >= {".fragment-date", ".fragment-extent", ".fragment-language",
                         ".fragment-length", ".author-date", ".author-count"}:
                catalogue = block.group(2)
        self.assertIsNotNone(catalogue)
        self.assertIn("0.8125rem", catalogue)
        self.assertIn("var(--ink-soft)", catalogue)

    def test_what_cannot_be_read_takes_a_dashed_rule_and_commentary_never_does(self):
        dashed = None
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(self.css)):
            names = {one.strip() for one in block.group(1).split(",")}
            if names == {".lead", ".blocked", ".refusal"}:
                dashed = block.group(2)
        self.assertIsNotNone(dashed, "the lead/blocked/refusal rule is the distinction")
        self.assertIn("border-bottom: 1px dashed", dashed)

    def test_the_refusal_alone_takes_the_negative_ink_among_content_states(self):
        refusal = " ".join(declarations_for(self.css, ".refusal"))
        self.assertIn("border-left: 0.2rem solid var(--notice)", refusal)
        self.assertIn("color: var(--notice)", refusal)
        for selector in (".fragment", ".author", ".lead", ".blocked",
                         ".aside-note", ".absence-note"):
            for block in declarations_for(self.css, selector):
                self.assertNotIn("--notice", block,
                                 f"{selector} may not take the negative ink")

    def test_the_truthful_column_comment_replaced_the_pinned_claim(self):
        self.assertNotIn("never scrolls away", self.css)
        self.assertNotIn("never has to be scrolled", self.css)
        self.assertIn("not pinned", self.css)


class CompositionTest(ReplayTest):
    """The accepted E0 composition, in the corrected mechanics."""

    def test_the_chapter_opens_and_the_first_group_opens_with_it(self):
        page = self.page("default")
        self.assertTrue(page["chapterOpen"])
        opened = [one["open"] for one in page["authorGroups"]]
        self.assertTrue(opened[0])
        self.assertFalse(any(opened[1:]),
                         "only the first group opens; the rest wait to be asked")

    def test_the_author_filter_is_folded_and_closed_when_nothing_is_hidden(self):
        page = self.page("default")
        self.assertTrue(page["authorFilterInDisclosure"])
        self.assertFalse(page["authorFilterOpen"])

    def test_the_controls_fold_synchronously_on_a_narrow_viewport(self):
        self.assertTrue(self.page("default")["controlsOpen"])
        self.assertFalse(self.page("narrow")["controlsOpen"])
        # Synchronously: before the first awaited fetch, so a slow connection
        # cannot shift the page after the fact.
        script = held(CATENA / "catena.js")
        start = script.index("async function start()")
        fold = script.index("controlsDisclosure.open = false", start)
        first_await = script.index("await Promise.all", start)
        self.assertLess(fold, first_await)

    def test_the_wide_grid_uses_explicit_rows_and_no_magic_span(self):
        css = held(CATENA / "catena.css")
        self.assertIn("@media (min-width: 64.0625rem)", css)
        self.assertIn("grid-template-columns: minmax(20rem, 26rem) minmax(0, 44rem)", css)
        self.assertIn("grid-template-rows: auto auto", css)
        self.assertIn("grid-row: 1 / -1", css)
        self.assertNotIn("span 100", css)

    def test_the_script_builds_one_column_for_everything_beside_the_chapter(self):
        page = self.page("default")
        self.assertIn("chain-column", " ".join(page["classes"]))


class TypedStateTest(ReplayTest):
    """Every state the corpus can put on this page, still told apart.

    Held text, an acquisition-list row, a translation absence, a numbering
    refusal, a blocked work, and an error are six different claims; each
    keeps its own class, its own words, and a `data-state` where the DOM
    would otherwise carry the difference only in CSS.
    """

    def test_a_held_fragment_renders_its_text_and_its_apparatus(self):
        page = self.page("default")
        body = [one for one in page["fragmentTexts"] if one != "Loading…"]
        self.assertTrue(body, "opening a fragment must fetch and show its text")
        self.assertTrue(any(one.startswith("Extent — ") for one in page["fragmentBases"]))
        self.assertTrue(any("not collated" in one for one in page["states"]))

    def test_a_numbering_refusal_refuses_rather_than_guesses(self):
        page = self.page("numbering-refusal")
        self.assertIsNotNone(page["refusal"])
        self.assertTrue(page["refusal"].startswith("Boundary not established. "))
        self.assertIn("anchored in Vulgate numbering", page["refusal"])
        self.assertIn("will not guess where the boundary moves to", page["refusal"])
        self.assertIn("King James", page["refusal"])

    def test_a_fragment_that_crosses_a_chapter_boundary_says_so(self):
        page = self.page("default")
        self.assertTrue(page["spans"])
        self.assertEqual(set(page["spans"]), {"— runs across the chapter boundary"})

    def test_the_voice_chip_says_whose_the_language_is(self):
        page = self.page("default")
        self.assertIn("Latin — the author’s own", page["languages"])
        self.assertIn("English translation", page["languages"])
        self.assertIn("Latin translation", page["languages"])

    def test_held_and_not_renderable_keeps_its_own_heading_and_reason(self):
        """SYNTHETIC fixture: no tracked chapter carries a blocked row yet.

        The renderer ships anyway — the distinction between a work nobody
        acquired and a work held that cannot be shown is protected — and the
        real fixture is the generator's to supply.
        """
        page = self.page("held-unrenderable")
        self.assertIn("Held, and not renderable yet", page["sectionHeadings"])
        self.assertEqual(len(page["blocked"]), 1)
        self.assertIn("Anonymous — Catena in Genesim", page["blocked"][0])
        self.assertIn("held only as page images", page["blocked"][0])
        self.assertIn("Believed to comment here — the acquisition list",
                      page["sectionHeadings"])

    def test_each_state_carries_its_typed_attribute(self):
        self.assertIn("held", self.page("default")["dataStates"])
        self.assertIn("lead", self.page("default")["dataStates"])
        self.assertIn("absence", self.page("voice-held")["dataStates"])
        self.assertIn("refusal", self.page("numbering-refusal")["dataStates"])
        self.assertIn("blocked", self.page("held-unrenderable")["dataStates"])
        self.assertIn("error", self.page("integrity-404")["dataStates"])
        self.assertIn("error", self.page("invalid-book")["dataStates"])

    def test_each_state_keeps_a_class_of_its_own(self):
        seen: set[str] = set()
        for name in self.pages:
            page = self.page(name)
            for one in page["classes"]:
                seen |= set(one.split())
        for name in ("fragment", "lead", "blocked", "refusal", "absence-note",
                     "paragraph-note", "passage-paragraph", "projected", "spans",
                     "aside-note", "fragment-basis", "catena-error",
                     "fragment-acknowledgement", "chain-column"):
            with self.subTest(**{"class": name}):
                self.assertIn(name, seen)


class PayloadTest(ReplayTest):
    """What the composition costs a reader, and what it does not cost them."""

    def test_the_stylesheet_holds_the_recorded_ceiling(self):
        css = held(CATENA / "catena.css")
        self.assertLessEqual(gz(css), CSS_BUDGET_GZ, f"catena.css is {gz(css)} B gzipped")
        rules = gz(without_comments(css))
        self.assertLessEqual(rules, CSS_RULES_BUDGET_GZ,
                             f"the declarations alone are {rules} B gzipped")

    def test_the_script_holds_the_recorded_ceiling(self):
        script = held(CATENA / "catena.js")
        self.assertLessEqual(gz(script), JS_BUDGET_GZ, f"catena.js is {gz(script)} B gzipped")
        code = gz(without_comments(script, script=True))
        self.assertLessEqual(code, JS_CODE_BUDGET_GZ, f"the code alone is {code} B gzipped")

    def test_the_corrections_added_no_request_to_a_first_load(self):
        quiet = self.page("voice-held")["fetched"]
        self.assertEqual(quiet, [
            "structure/catena/index.json",
            "bibles.json",
            "structure/paragraphs/index.json",
            "structure/catena/01-gen/001.json",
            "douay-rheims/chapters/Gen/1.json",
            "structure/paragraphs/douay-rheims/01-gen/001.json",
        ])
        opened = self.page("default")["fetched"]
        self.assertEqual(len(opened), len(quiet) + 1)
        self.assertTrue(opened[-1].startswith("structure/catena/text/"))

    def test_an_invalid_address_costs_only_the_indexes(self):
        self.assertEqual(self.page("invalid-book")["fetched"], [
            "structure/catena/index.json",
            "bibles.json",
            "structure/paragraphs/index.json",
        ])


class FrozenContractTest(ReplayTest):
    """What this lane was not allowed to move, and did not."""

    def test_the_one_cross_entrance_link_still_points_where_it_did(self):
        script = held(CATENA / "catena.js")
        self.assertIn(
            "whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);", script)
        page = self.page("default")
        self.assertTrue(page["linkHref"].startswith("../sources/#passage=passage."))
        self.assertEqual(page["linkText"], "Open this passage in the Source Library")

    def test_the_catena_tree_still_reaches_exactly_one_other_entrance(self):
        hits = []
        for source in sorted(CATENA.glob("*.js")):
            hits += [(source.name, one)
                     for one in re.findall(r"\.href = '(\.\./[^']*)", held(source))]
        self.assertEqual(len(hits), 1, hits)

    def test_the_model_is_byte_identical(self):
        digest = hashlib.sha256((CATENA / "catena-model.js").read_bytes()).hexdigest()
        self.assertEqual(
            digest, MODEL_SHA256,
            "catena-model.js moved; it is UMD, DOM-free, replayed by `catena check`, "
            "and no part of this correction touches it")

    def test_the_model_names_no_part_of_a_document(self):
        source = without_comments(held(CATENA / "catena-model.js"), script=True)
        for name in ("document", "window", "HTMLElement", "querySelector"):
            with self.subTest(name=name):
                self.assertNotIn(name, source)

    def test_the_legacy_language_key_stays_unhonoured(self):
        # Pinned in full by test_browser_url_contract.py:537; restated here so
        # a correction to this file cannot quietly "fix" the old key.
        script = held(CATENA / "catena.js")
        self.assertNotIn("hash.get('language')", script)
        self.assertNotIn("next.get('language')", script)


if __name__ == "__main__":
    unittest.main()
