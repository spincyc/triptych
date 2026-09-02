"""Curated production regression set for integration/catena-e1.

This file is the production-relevant subset of the V16 wave-1 suite
(tools/tests/test_catena_wave_1.py at cc1f2fb8625f044558c26edd358b99cd7dcc7646,
17,315 lines), curated per the integration manifest: focused normal-policy
regressions for accepted publication atomicity, owner/completion identity,
same-path/late isolation, exact voices, refusal/absence/provenance, path
namespace closure, cache isolation, malformed canonical data, the governed
budgets, and the generator contract.

INVENTORY, MEASURED RATHER THAN CLAIMED
---------------------------------------
The integration review disproved the first curation's account of its own
exclusions ("8 hostile + 40 non-manifest"), so the numbers here are counted the
same way for both files — a class is RUNNABLE if it defines at least one
`test_` method, and a test is such a method:

    this file        71 runnable classes, 394 tests, 3 dependency-only bases
                     (ReplayTest, V14ProjectionAuthorityBase,
                     V16PublicationBase)
    V16 wave-1      105 runnable classes, 604 tests, 3 dependency-only bases
    omitted          36 runnable classes, 221 tests
    added here        2 runnable classes, 13 tests
                     (AbsenceRowFlatteningTest, RecoveryFocusVisibilityTest —
                     the two corrections the review required)

Two retained classes are one test lighter than in wave-1: `FrozenContractTest`
lost the forbidden candidate SHA pin, and `V15TransportOwnershipTest` lost the
write-break probe its seam no longer carries.

WHAT IS DELIBERATELY NOT HERE
-----------------------------
No synthetic hostile machinery: no planted prototypes, accessors, `Proxy`
walkers, thenables or realm pollution; no evidence-package or attempt-history
validation; no candidate or source identity pin of any kind. Those cases stay
with the convergence hardening backlog and the original wave-1 file. The replay
harness (REPLAY, SCENARIOS, the DOM shim and ReplayTest) is carried only as far
as the retained classes reach: SCENARIOS holds only the entries they read, and
the harness holds only the seams those entries use.

WHAT THE OMISSION COST, AND WHAT IT MUST NOT
--------------------------------------------
The review named the ordinary coverage the first curation lost along with its
hostile classes; it is restored here rather than argued away — chronology
grouping, absence and paragraph counts, author-filter recovery, leads copy,
shared-field generator drift, null and list bootstrap truth, visible failure
text, and unregressed Scripture. All nine coverage categories the correction
requires are represented: `PayloadTest` holds the governed budgets and
`V7SharedFieldDriftTest` reads `scripts/_catena.py` itself for the generator
contract.
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

def browser_binary() -> str | None:
    """A Chromium the correction's focus proof can be observed in.

    The repository's own installer deliberately omits the browser, so a host
    without one skips the live run with a reason that names the variable which
    would enable it rather than reporting a pass nobody observed. The candidate
    list matches `test_corpus_browser_gate.py`.
    """
    named = os.environ.get("TRIPTYCH_CHROME")
    if named:
        return named if Path(named).is_file() else None
    for candidate in ("/usr/bin/chromium", "/usr/bin/chromium-browser",
                      "/usr/bin/google-chrome-stable", "/usr/bin/google-chrome"):
        if Path(candidate).is_file():
            return candidate
    return shutil.which("chromium") or shutil.which("google-chrome-stable")

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

# THE TWO TERMINAL SENTENCES, AND THEY ARE DIFFERENT CLAIMS. V10, the V9
# review: absence — no text reference stated — and refusal — a reference
# stated and declined — collapsed into the first sentence, which is false of
# a fragment whose spine stated a reference. The refused sentence is pinned
# here byte-exactly against `M.TEXT_REFUSED`, the model's own export, so the
# page and the suite cannot drift apart.
#
# V11, the V10 review: there are THREE no-text claims, not two. The refused
# sentence asserts that a reference WAS SUPPLIED and is unusable AS WRITTEN,
# and the V10 lane gave that sentence to every malformed state — a spine whose
# `text_prefix` was `null`, a record, a list, a number, a flag, '' or
# whitespace, and a direct claim that was bare, contradictory, inherited or
# accessor-backed. None of those establishes either fact. The third sentence
# is what is left when the state cannot truthfully say more.
NO_TEXT_SAID = "This fragment carries no text file, so nothing of it can be shown."

REFUSED_SAID = ("A text reference was supplied for this fragment, "
                "but it cannot be used as written, so no text is shown.")

UNESTABLISHED_SAID = ("No text reference is established for this fragment, "
                      "so no text is shown.")

# THE OWNED REQUEST JOURNAL, WRITTEN FROM THIS SIDE. V11, the V10 review:
# the live harness recorded ownership and the packaged dump kept only the
# flat path list, so the ownership claim could not be reproduced from the
# package. A journal row is now the five facts a reader needs without the
# harness — WHICH request, WHERE it went, WHAT KIND of record it asks for,
# WHOSE step issued it, and WHAT BECAME of it — and this is the expected
# side of the same rule the replay's `kindOf` states in JavaScript.
def _request_kind(path):
    if path == "bibles.json":
        return "editions"
    if path == "structure/catena/index.json":
        return "catena-index"
    if path == "structure/paragraphs/index.json":
        return "paragraph-index"
    if path.startswith("structure/catena/text/"):
        return "text"
    if path.startswith("structure/catena/"):
        return "spine"
    if path.startswith("structure/paragraphs/"):
        return "paragraphs"
    return "scripture"

def request_journal(entries):
    """Expected journal rows from `(path, phase)` or `(path, phase, outcome)`.

    `completed` is the ordinary outcome; a parked request reads `held` until
    it is let go and `released` afterwards, so a snapshot taken either side
    of a release says which one it is.
    """
    return [{"seq": seq, "path": entry[0], "kind": _request_kind(entry[0]),
             "phase": entry[1],
             "outcome": entry[2] if len(entry) > 2 else "completed"}
            for seq, entry in enumerate(entries)]

GEN1 = "#book=Gen&chapter=1&bible=douay-rheims"

GEN2 = "#book=Gen&chapter=2&bible=douay-rheims"

GEN3 = "#book=Gen&chapter=3&bible=douay-rheims"

GEN42 = "#book=Gen&chapter=42&bible=douay-rheims"

# Genesis 10 holds 71 fragments, every one in its author's own Latin.
GEN10_ENGLISH = "#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en"

# EXPLICITLY SYNTHETIC malformed-STRUCTURE fixture (V4, the V3 review's
# remaining typed-presentation findings). The tracked corpus types everything
# it carries, so these shapes can only be driven from a labelled fixture. Each
# malformed value stands beside a sound one: withholding garbage must cost no
# valid fact, and must not strand the render.
MALFORMED_STRUCTURE_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
        # The control. Every field sound, and the work whose absence rows the
        # scenario patches into the index.
        "0": {"author": "Sound Author", "work": "Sound Work",
              "work_id": "work.sound", "date": 401, "language": "en",
              "voice": "translation", "rights": "public-domain",
              "edition": "Sound Edition", "edition_published": "1899",
              "translators": ["Sound Hand"], "container": ""},
        # A TRANSLATED LANGUAGE that is not text. It must never become a voice
        # key, a control value, a `lang` attribute, or a URL the page then
        # refuses on the way back in.
        "1": {"author": "Language Author", "work": "Language Work",
              "work_id": "work.language", "date": 402, "language": {"code": "en"},
              "voice": "translation", "rights": "public-domain",
              "edition": "Language Edition", "edition_published": "",
              "translators": [], "container": ""},
        # A SCALAR translator container. A string is not a one-item list, and
        # was widened into a validated-looking attribution of translation.
        "2": {"author": "Scalar Author", "work": "Scalar Work",
              "work_id": "work.scalar", "date": 403, "language": "en",
              "voice": "translation", "rights": "public-domain",
              "edition": "Scalar Edition", "edition_published": "",
              "translators": "Not A List", "container": ""},
        # An AUTHOR that cannot be named. Two of these are not one man, and the
        # filter key they collapsed into was shared across every chapter.
        "3": {"author": {"name": "not text"}, "work": "Nameless Work One",
              "work_id": "work.nameless1", "date": 404, "language": "en",
              "voice": "translation", "rights": "public-domain",
              "edition": "Nameless Edition", "edition_published": "",
              "translators": [], "container": ""},
        "4": {"author": ["also", "not text"], "work": "Nameless Work Two",
              "work_id": "work.nameless2", "date": 404, "language": "en",
              "voice": "translation", "rights": "public-domain",
              "edition": "Nameless Edition", "edition_published": "",
              "translators": [], "container": ""},
    },
    "fragments": [
        {"id": "shape-control", "locator": "1", "source": "0",
         "review": "inspected", "text_words": 2,
         "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 1,
                    "last_chapter": 1, "last_verse": 1}},
        {"id": "shape-language", "locator": "2", "source": "1",
         "review": "inspected", "text_words": 2,
         "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 2,
                    "last_chapter": 1, "last_verse": 2}},
        # STRUCTURED EXTENT MEMBERS. Objects stringified into a locus; two
        # arrays are never `===`, so they also claimed a chapter crossing.
        {"id": "shape-extent-object", "locator": "3", "source": "2",
         "review": "inspected", "text_words": 2,
         "extent": {"token": "Gen", "first_chapter": {"n": 1}, "first_verse": 1,
                    "last_chapter": {"n": 1}, "last_verse": 2}},
        {"id": "shape-extent-list", "locator": "4", "source": "3",
         "review": "inspected", "text_words": 2,
         "extent": {"token": "Gen", "first_chapter": [1], "first_verse": [1],
                    "last_chapter": [1], "last_verse": [2]}},
        {"id": "shape-extent-absent", "locator": "5", "source": "4",
         "review": "inspected", "text_words": 2, "extent": {}},
    ],
    # CONTAINERS THAT ARE NOT LISTS. A string satisfied `.length`, so the tally
    # counted characters as works and the refusal claimed a boundary.
    "leads": "not a list",
    "blocked": {"length": 2},
    "refusals": {"douay-rheims": "not a list"},
}

# Absence rows for the same works, every displayed field malformed in turn.
#
# V5 REBUILT THIS FIXTURE AROUND `finding`, because the V4.1 review proved the
# old one was proving the wrong thing. Not one of these rows carried a
# `finding` — the field the generator ALWAYS writes, from a list closed at
# four values in `scripts/_catena.py` — and the page classified a row by
# whether a `partial` string happened to be attached. So five malformed
# neighbours were being counted into "N works standing here have no English
# this project may publish": a closed claim about somebody's publishing
# rights, manufactured out of records that said nothing of the kind.
#
# The rows below now put a real typed finding beside malformed siblings, and
# malformed findings beside sound siblings, so the two questions are separable.
MALFORMED_ABSENCES = {
    "absences": {
        # The control: a valid typed finding, sound siblings.
        "work.sound": [{"language": "en", "finding": "partial-public-domain",
                        "reason": "A sound recorded reason.",
                        "partial": "a sound partial offer"}],
        # A VALID TYPED FINDING WITH MALFORMED NEIGHBOURS. `in-copyright` is a
        # fact about the law and survives an unreadable reason beside it; the
        # unreadable reason is withheld, and takes the finding with it nowhere.
        "work.language": [{"language": "en", "finding": "in-copyright",
                           "reason": {"text": "not text"},
                           "partial": {"offer": "not text"}}],
        # A finding that is not text at all.
        "work.scalar": [{"language": "en", "finding": ["not", "text"],
                         "reason": ["not", "text"], "partial": 42}],
        # Well-formed text naming no finding this project defines. It must not
        # be answered with the nearest finding that IS defined.
        "work.nameless1": [{"language": "en", "finding": "no-such-finding",
                            "reason": "   ", "partial": True}],
        # No finding at all, beside a blank `partial` — the exact pair the
        # untyped classification read as a closed publishing negative.
        "work.nameless2": [{"language": "en", "reason": None, "partial": "   "}],
    }
}

def _voice_source(n, **over):
    """One well-formed source record, so a fixture varies ONE field at a time."""
    record = {"author": "Author %d" % n, "work": "Work %d" % n,
              "work_id": "typed.work%d" % n, "date": 300 + n, "language": "la",
              "voice": "original", "rights": "public-domain",
              "edition": "Edition %d" % n, "edition_published": "1900",
              "translators": [], "container": ""}
    record.update(over)
    return record

def _voice_fragment(n, **over):
    """One well-formed fragment on Genesis 1, at its own verse."""
    record = {"id": "typed-%d" % n, "locator": str(n), "source": str(n),
              "review": "verified", "text_words": 4,
              "extent": {"token": "Gen", "first_chapter": 1, "first_verse": n,
                         "last_chapter": 1, "last_verse": n}}
    record.update(over)
    return record

# --------------------------------------------------------------------------
# V5 §5 — a language that is not a language, under EVERYTHING HELD
#
# The V4.1 review replayed exactly this in real Chromium and got
# `lang="[object Object]"` on an otherwise complete page. The committed
# malformed-language scenario could not see it: it FILTERED the offending
# fragment out under a translation selection, so the attribute was never
# rendered, and the shim did not reflect `lang` in any case. Everything held
# renders every one of these side by side.
MALFORMED_LANGUAGE_FIXTURE = {
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {
        "1": _voice_source(1, language="la"),
        "2": _voice_source(2, language={"code": "la"}),
        "3": _voice_source(3, language=["la"]),
        "4": _voice_source(4, language=42),
        "5": _voice_source(5, language=True),
        "6": _voice_source(6, language="   "),
        "7": _voice_source(7, language=""),
        "8": _voice_source(8, language=None),
        # Sound text, and still not a language code. `sound()` passed it and
        # the shared namer printed it back as a language, uppercased.
        "9": _voice_source(9, language="not a language code"),
    },
    "fragments": [_voice_fragment(n) for n in range(1, 10)],
    "leads": [], "blocked": [], "refusals": {},
}

# --------------------------------------------------------------------------
# V5 §6 — the required mixed collection, applied to every collection at once
#
# valid member, malformed record, scalar, null, valid member. The questions
# are the same for each: do the valid siblings survive, is the count of the
# valid members alone, and can a malformed member manufacture a refusal.
MIXED_COLLECTION_FIXTURE = {
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {
        "1": _voice_source(1, author="First Author", work="First Work"),
        "5": _voice_source(5, author="Last Author", work="Last Work"),
    },
    "fragments": [
        _voice_fragment(1, id="mixed-first"),
        # A RECORD whose id is not one. It is a fragment — it counts, it
        # renders, it names its author — but it addresses no text file, and
        # `[object Object].json` is never requested for it.
        _voice_fragment(2, id={"not": "an id"}, source="1"),
        7,
        None,
        _voice_fragment(5, id="mixed-last"),
    ],
    "leads": [
        {"author": "Lead One", "title": "Lead Work One", "date": "500"},
        {"author": {"n": 1}, "title": ["x"], "date": {}},
        13,
        None,
        {"author": "Lead Two", "title": "Lead Work Two", "date": "600"},
    ],
    "blocked": [
        {"author": "Blocked One", "work": "Blocked Work One", "reason": "rights"},
        {"author": 5, "work": [], "reason": {}},
        21,
        None,
        {"author": "Blocked Two", "work": "Blocked Work Two", "reason": "rights"},
    ],
    # One valid refusal record among three malformed members: the boundary
    # note is the valid record's, said once, not four times.
    "refusals": {"douay-rheims": [
        None, 4, "not a record",
        {"chapter": 1, "verse": None, "kind": "displaced",
         "note": "the numbering of this chapter is displaced in this edition"},
    ]},
}

# The same chapter with NO valid refusal record at all. Three malformed
# members satisfied `.length` and made the page claim a boundary the
# projection never refused.
MIXED_NO_REFUSAL_FIXTURE = dict(
    MIXED_COLLECTION_FIXTURE,
    refusals={"douay-rheims": [None, 4, "not a record"]})

# --------------------------------------------------------------------------
# V5 §7 — the five absence cases, each a different way a record can fail to
# support the negative this page used to print regardless.
TYPED_ABSENCE_FIXTURE = {
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    # Every work stands here in its author's own Latin, so English is empty
    # and the absence view carries the whole claim.
    "sources": {str(n): _voice_source(n) for n in range(1, 6)},
    "fragments": [_voice_fragment(n) for n in range(1, 6)],
    "leads": [], "blocked": [], "refusals": {},
}

TYPED_ABSENCE_INDEX = {
    "absences": {
        # 1. A valid typed absence that DOES support a closed negative.
        "typed.work1": [{"language": "en", "finding": "none-published",
                         "reason": "No English translation has been published."}],
        # 2. A malformed finding TYPE, beside a sound reason. The reason is a
        #    fact the record states and survives; the finding supports nothing,
        #    so no count and no claim may be drawn from this row.
        "typed.work2": [{"language": "en", "finding": {"kind": "in-copyright"},
                         "reason": "A reason that outlives its finding."}],
        # 3. A valid finding beside malformed siblings. `in-copyright` is a
        #    fact about the law and is not discarded because its neighbour is
        #    unreadable.
        "typed.work3": [{"language": "en", "finding": "in-copyright",
                         "reason": ["not", "text"], "partial": 3}],
        # 4. `not-surveyed` — the finding whose entire content is that NOBODY
        #    HAS LOOKED. Classified by `partial` truthiness it became "no
        #    English this project may publish": a closed claim about publishing
        #    rights, manufactured out of an admission of ignorance.
        "typed.work4": [{"language": "en", "finding": "not-surveyed",
                         "reason": ""}],
        # 5. A LIST mixing malformed members with a valid typed absence.
        "typed.work5": [None, 11, "not a record",
                        {"language": "en", "finding": "partial-public-domain",
                         "reason": "Only part of it is out of copyright.",
                         "partial": "the 1893 selection"}],
    }
}

# --------------------------------------------------------------------------
# V5 §8 — numeric, verse, path and bootstrap metadata
#
# The chapter TEXT, malformed: keys that `Number()` would take for verses the
# chapter never numbered, and values that concatenation would print as
# Scripture.
MALFORMED_VERSES = {
    "book": "Gen", "chapter": 1,
    "verses": {
        "1": "The first verse, sound.",
        "2": {"text": "not text"},
        "3": ["also", "not text"],
        "4": None,
        "5": "   ",
        "6": 6,
        " 7 ": "A verse this chapter never numbered.",
        "8.0": "Nor this one.",
        "1e3": "Nor this.",
        "0": "Nor a verse zero.",
        "-2": "Nor a negative verse.",
        "9": "The last verse, sound.",
    },
}

# Paragraph marks that are not marks. Any truthy value opened a paragraph
# while counting as neither kind, so the page printed paragraphs and, beneath
# them, the note saying no paragraph division is held for this chapter.
MALFORMED_BREAKS = {
    "edition": "douay-rheims", "token": "Gen", "chapter": 1,
    "breaks": {"9": "guessed", "1": {"kind": "printed"}, "3": 1},
}

# Numbers that are not the numbers this corpus counts by, and paths that are
# not paths. `Number(x) > 0` printed "1 words" for a boolean; a record in a
# path composed a URL the page then requested.
MALFORMED_NUMBER_FIXTURE = {
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {str(n): _voice_source(n) for n in range(1, 8)},
    "fragments": [
        _voice_fragment(1, text_words=1200),
        _voice_fragment(2, text_words="1200"),
        _voice_fragment(3, text_words=[1200]),
        _voice_fragment(4, text_words=True),
        _voice_fragment(5, text_words=12.5),
        _voice_fragment(6, text_words=0),
        _voice_fragment(7, text_words=-3),
    ],
    "leads": [], "blocked": [], "refusals": {},
}

# The index itself, malformed — the record the page reads BEFORE it can say
# anything at all, and the one whose failure used to leave "Loading…" standing.
def _broken_index(**over):
    base = {
        "numbering": "vulgate",
        "canon": [{"token": "Gen", "name": "Genesis", "chapters": 50,
                   "testament": "old", "path": "01-gen"}],
        "held": [{"token": "Gen", "name": "Genesis", "chapters": 50,
                  "fragments": 1, "path": "structure/catena/01-gen/",
                  "present": [1], "languages": ["la"]}],
        "voices": ["original"],
        "absences": {},
        "chapter_digits": 3,
    }
    base.update(over)
    return base

# --------------------------------------------------------------------------
# V6 — the fixtures below are self-labeling, and that is a requirement rather
# than a courtesy.
#
# The V5 review found that the package's fabricated data was disclosed in
# prose alone: every JSON dump, every probe row and every capture read, on its
# own, as a record of this corpus. Detached from the Markdown that disclaimed
# them they were indistinguishable from real holdings of the project. So every
# V6 fixture root carries the banner below, inertly — no reader of this page
# looks at the key, and any artifact captured from one of these fixtures
# carries its own denial with it.
ADVERSARIAL = "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"

def _fixture(record):
    """One fabricated file root, stamped as fabricated."""
    stamped = dict(record)
    stamped["_adversarial"] = ADVERSARIAL
    return stamped

def _edition(id_, label, language):
    """One published-edition record, varying only its language."""
    return {"id": id_, "label": label, "language": language,
            "numbering": "vulgate", "psalter": "gallican",
            "psalm_titles": "numbered", "edition": "Synthetic edition record",
            "rights": "public-domain"}

# V6 §5 — the ROOT language record, which is where the review found
# `Douay-Rheims ([object Object])` still reaching a reader. Every malformed
# form stands beside two sound ones, and the sound ones must keep their claim.
V6_BIBLE_LANGUAGES = _fixture({"bibles": [
    _edition("douay-rheims", "Douay-Rheims", {"code": "en"}),
    _edition("list-language", "List Language", ["en"]),
    _edition("number-language", "Number Language", 42),
    _edition("boolean-language", "Boolean Language", True),
    _edition("null-language", "Null Language", None),
    _edition("empty-language", "Empty Language", ""),
    _edition("blank-language", "Blank Language", "   "),
    _edition("prose-language", "Prose Language", "not a language code"),
    _edition("clementine-vulgate", "Clementine Vulgate", "la"),
]})

# An edition record that cannot name ITSELF is not an edition: it can be no
# option, no route value and no fetched directory. One sound edition stands
# behind each, so refusing the broken one must not empty the control.
V6_BIBLE_IDENTITIES = _fixture({"bibles": [
    _edition("douay-rheims", "Douay-Rheims", "en"),
    _edition("../../escape", "Escaping Edition", "en"),
    _edition("has space", "Spaced Edition", "en"),
    _edition("", "Nameless Edition", "en"),
    dict(_edition("no-label", "", "en")),
    _edition("clementine-vulgate", "Clementine Vulgate", "la"),
]})

# V6 §11 — textual identities that are sound TEXT and no identity of this
# corpus. Each becomes a fetched path, a link href or a property lookup.
V6_UNSAFE_IDENTITY_FIXTURE = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {str(n): _voice_source(n) for n in range(1, 11)},
    "fragments": [
        _voice_fragment(1, id="safe-first"),
        _voice_fragment(2, id="../../../etc/passwd"),
        _voice_fragment(3, id="a space is not an id"),
        _voice_fragment(4, id="Upper.Case"),
        _voice_fragment(5, id="   "),
        _voice_fragment(6, id="trailing/"),
        _voice_fragment(7, id="%2e%2e%2fsecret"),
        # A SOURCE KEY THAT IS NOT A STRING. `sources[["1"]]` is `sources["1"]`
        # — a one-member list is coerced by the lookup itself, so this
        # fragment took a real edition's author, rights and language while
        # naming no edition at all.
        _voice_fragment(8, id="coerced-source", source=["1"]),
        # And a key that is not a member of the record but of every object.
        _voice_fragment(9, id="proto-source", source="constructor"),
        _voice_fragment(10, id="safe-last"),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

V7_TEXT_PATH_FIXTURE = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {str(n): _voice_source(n) for n in range(1, 13)},
    "fragments": [
        _voice_fragment(1, id="path-valid"),
        _voice_fragment(2, id="path-object", text_path={"a": "b"}),
        _voice_fragment(3, id="path-array",
                        text_path=["structure/catena/text/path-valid.json"]),
        _voice_fragment(4, id="path-number", text_path=7),
        _voice_fragment(5, id="path-null", text_path=None),
        _voice_fragment(6, id="path-empty", text_path=""),
        _voice_fragment(7, id="path-space", text_path="   "),
        _voice_fragment(8, id="path-traversal", text_path="../../../etc/passwd.json"),
        _voice_fragment(9, id="path-absolute", text_path="/etc/passwd.json"),
        _voice_fragment(10, id="path-encoded", text_path="%2e%2e%2fsecret.json"),
        _voice_fragment(11, id="path-boolean", text_path=True),
        # THE V6 HOLE, EXACTLY AS THE REVIEW PROVED IT. The id is a record, so
        # V6 composed nothing and left the record's own `text_path` standing,
        # and the page then requested it. Its author still names it, so it is
        # still a fragment and still opens.
        _voice_fragment(12, id={"not": "an id"},
                        text_path="../../../etc/shadow.json"),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# The SAMPLE-CORPUS shape: a spine that states no `text_prefix`, so nothing can
# be composed and a carried `text_path` is the only candidate there is. It is
# accepted, and only when it is a relative JSON file of this data root's own
# grammar whose stem is this fragment's own validated id — so the one thing it
# can address is the text of the fragment that carried it.
V7_TEXT_PATH_NO_PREFIX = _fixture({
    "token": "Gen", "chapter": 1,
    "sources": {str(n): _voice_source(n) for n in range(1, 11)},
    "fragments": [
        _voice_fragment(1, id="carried-valid",
                        text_path="structure/catena/text/carried-valid.json"),
        # Sound, relative, of the right grammar — and it names SOME OTHER
        # file. A path that is not this fragment's text is not this fragment's
        # text however well formed it is.
        _voice_fragment(2, id="carried-other",
                        text_path="structure/catena/text/somebody-else.json"),
        _voice_fragment(3, id="carried-object", text_path={"a": "b"}),
        _voice_fragment(4, id="carried-array",
                        text_path=["structure/catena/text/carried-array.json"]),
        _voice_fragment(5, id="carried-number", text_path=7),
        _voice_fragment(6, id="carried-traversal",
                        text_path="../../../etc/passwd.json"),
        _voice_fragment(7, id="carried-absolute",
                        text_path="/structure/catena/text/carried-absolute.json"),
        _voice_fragment(8, id="carried-encoded",
                        text_path="structure/%2e%2e/carried-encoded.json"),
        _voice_fragment(9, id="carried-space", text_path="   "),
        # A directory, not a file: `trail`'s grammar is not `leaf`'s.
        _voice_fragment(10, id="carried-dir",
                        text_path="structure/catena/text/"),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# The reviewer's first vector: a well-formed directory of this data root that
# is not this route's. Every fragment id is readable, so V7 composed and
# fetched `structure/paragraphs/<id>.json` for each.
V8_WRONG_NAMESPACE_PREFIX = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/paragraphs/",
    "sources": {str(n): _voice_source(n) for n in range(1, 4)},
    "fragments": [
        _voice_fragment(1, id="same-stem-1"),
        _voice_fragment(2, id="same-stem-2"),
        _voice_fragment(3, id="same-stem-3"),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# The byte-exact question, asked of the prefix: the RIGHT namespace wrapped in
# whitespace was trimmed into validity, which is the page deciding what the
# record meant and then requesting it.
V8_PADDED_PREFIX = _fixture(dict(
    V8_WRONG_NAMESPACE_PREFIX, text_prefix="  structure/catena/text/  "))

# A text body PLANTED at the same-stem wrong-namespace address the reviewer's
# reproduction fetched. If the closure leaks, this is served, rendered, and
# caught by content as well as by the journal.
V8_PLANTED_TEXT = _fixture({
    "id": "same-stem-1",
    "text": "PLANTED WRONG-NAMESPACE BODY — not this route's text."})

# The reviewer's second vector and its family: carried paths whose tail looks
# like an identity of this corpus while the namespace is someone else's. Only
# the first fragment's path is inside `structure/catena/text/` byte-exactly.
V8_WRONG_NAMESPACE_CARRIED = _fixture({
    "token": "Gen", "chapter": 1,
    "sources": {str(n): _voice_source(n) for n in range(1, 11)},
    "fragments": [
        _voice_fragment(1, id="ns-valid",
                        text_path="structure/catena/text/ns-valid.json"),
        # THE V7 REPRODUCTION EXACTLY: same stem, under the Paragraphs text
        # directory, with no prefix to displace it.
        _voice_fragment(2, id="ns-paragraphs-text",
                        text_path="structure/paragraphs/text/ns-paragraphs-text.json"),
        _voice_fragment(3, id="ns-paragraphs",
                        text_path="structure/paragraphs/ns-paragraphs.json"),
        _voice_fragment(4, id="ns-parent",
                        text_path="structure/catena/ns-parent.json"),
        _voice_fragment(5, id="ns-root",
                        text_path="structure/ns-root.json"),
        _voice_fragment(6, id="ns-sibling",
                        text_path="douay-rheims/chapters/gen/ns-sibling.json"),
        _voice_fragment(7, id="ns-traversal-in",
                        text_path="../structure/catena/text/ns-traversal-in.json"),
        _voice_fragment(8, id="ns-absolute",
                        text_path="/structure/catena/text/ns-absolute.json"),
        # `structure/catena/textual/` is another namespace, not a longer
        # spelling of this one: the boundary is the closing slash.
        _voice_fragment(9, id="ns-boundary",
                        text_path="structure/catena/textual/ns-boundary.json"),
        # The RIGHT namespace, wrapped in whitespace. Trimmed into validity is
        # repair, and repair is the page deciding what the record meant.
        _voice_fragment(10, id="ns-padded",
                        text_path="  structure/catena/text/ns-padded.json  "),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

V9_REFUSED_PREFIX_WITH_CARRIED = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/paragraphs/",
    "sources": {"1": _voice_source(1)},
    "fragments": [
        _voice_fragment(1, id="fallback-owned",
                        text_path="structure/catena/text/fallback-owned.json"),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# The RIGHT namespace wrapped in whitespace, beside the same valid carried
# path: a statement refused for needing repair is still a statement, and it
# opens no carried door either.
V9_PADDED_PREFIX_WITH_CARRIED = _fixture(dict(
    V9_REFUSED_PREFIX_WITH_CARRIED, text_prefix="  structure/catena/text/  "))

# The same fragment under NO prefix at all — the one state whose carried
# path may stand, so the closure is measured against the door it must not
# close.
V9_ABSENT_PREFIX_WITH_CARRIED = _fixture({
    key: value for key, value in V9_REFUSED_PREFIX_WITH_CARRIED.items()
    if key != "text_prefix"})

# A VALID prefix beside the same valid same-stem carried path: the prefix
# already determines text identity, so the carried address is never asked —
# and a planted body waits there to catch the page if it is.
V9_VALID_PREFIX_WITH_CARRIED = _fixture(dict(
    V9_REFUSED_PREFIX_WITH_CARRIED,
    text_prefix="structure/catena/text/deeper/"))

# The refused spine again, on Genesis 2, so a prewarmed or held chapter 1
# can walk into it: same carried path, same planted body, other chapter.
V9_REFUSED_PREFIX_GEN2 = _fixture({
    "token": "Gen", "chapter": 2, "text_prefix": "structure/paragraphs/",
    "sources": {"1": _voice_source(1)},
    "fragments": [
        _voice_fragment(1, id="fallback-owned",
                        text_path="structure/catena/text/fallback-owned.json",
                        extent={"token": "Gen", "first_chapter": 2,
                                "first_verse": 1, "last_chapter": 2,
                                "last_verse": 1}),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# The body PLANTED at the carried address: reachable through genuine absence
# and through nothing else. If refusal, repair, prewarming or late work ever
# serves it, content catches what the journal catches.
V9_PLANTED_FALLBACK = _fixture({
    "id": "fallback-owned",
    "text": "PLANTED FALLBACK BODY — reachable only through genuine absence."})

# What the VALID prefix composes for the same fragment, so the valid route
# stays a rendering route while the carried address goes unasked.
V9_COMPOSED_DEEPER = _fixture({
    "id": "fallback-owned",
    "text": "Composed from the stated prefix and the fragment's own id."})





















def _members_spine(members):
    """One chapter carrying exactly these fragments and nothing else."""
    return _fixture({
        "token": "Gen", "chapter": 1,
        "sources": {"1": _voice_source(1), "2": _voice_source(2),
                    "3": _voice_source(3)},
        "fragments": members,
        "leads": [], "blocked": [], "refusals": {},
    })






# TWO ROWS, ONE ADDRESS. Both fragments carry the same own id, so both
# resolve the same carried address through genuine absence — and they are
# two different projected row objects standing at two different verses. A
# request owned by its path cannot tell them apart; a request owned by the
# row it came off can.
V14_SAME_PATH_SPINE = _fixture({
    "token": "Gen", "chapter": 1,
    "sources": {"1": _voice_source(1), "2": _voice_source(2)},
    "fragments": [
        _voice_fragment(1, id="fallback-owned", locator="first",
                        text_path="structure/catena/text/fallback-owned.json"),
        _voice_fragment(2, id="fallback-owned", locator="second", source="2",
                        text_path="structure/catena/text/fallback-owned.json",
                        extent={"token": "Gen", "first_chapter": 1,
                                "first_verse": 2, "last_chapter": 1,
                                "last_verse": 2}),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# THE SAME ADDRESS AGAIN, ON ANOTHER CHAPTER. A second chapter is a second
# projection: the request must stay with the projection and the row that
# initiated it, and must not collapse onto the address the two share.
V14_SAME_PATH_GEN2 = _fixture({
    "token": "Gen", "chapter": 2,
    "sources": {"1": _voice_source(1)},
    "fragments": [
        _voice_fragment(1, id="fallback-owned", locator="second-chapter",
                        text_path="structure/catena/text/fallback-owned.json",
                        extent={"token": "Gen", "first_chapter": 2,
                                "first_verse": 1, "last_chapter": 2,
                                "last_verse": 1}),
    ],
    "leads": [], "blocked": [], "refusals": {},
})

# ================================================================ V15 §§9-11
# TWO DISTINGUISHABLE ANSWERS AT ONE ADDRESS.
#
# The V14 review's decisive finding: the late proof planted ONE body at ONE
# path, so "B rendered the words it asked for" and "B rendered the words A
# asked for" were the same sentence, and the green oracle required the leak.
# Two documents served in turn at one address separate them, and nothing
# else can: a body is the only thing a reader sees, and a proof that reads
# only the journal proves only what the journal was told.
V15_BODY_A = _fixture({
    "id": "fallback-owned", "language": "la",
    "text": "PLANTED BODY A — the answer the row in projection A asked for."})

V15_BODY_B = _fixture({
    "id": "fallback-owned", "language": "la",
    "text": "PLANTED BODY B — the answer the row in projection B asked for."})













# A CHAPTER WHOSE SPINE IS A DOCUMENT AND NOT A SPINE, on two chapters, so a
# reader can walk from one to the other and back. The page substitutes a
# record of its own for a spine it cannot read; under V14 it minted a fresh
# literal every time it was asked, and a fresh record is a fresh authority.
V15_NOT_A_SPINE = ["not", "a", "spine"]


# ==========================================================================
# V7 §7 — an absence row about a work the record cannot name
#
# `absenceRows` deduplicated on `work_id` and read the author and the work
# afterwards, so a source stating neither took the row for that work — a blank
# `<li>` under a summary counting it as a work standing here — and the valid
# sibling carrying the same work id and both its names was skipped behind it.
V7_ABSENCE_SLOT_FIXTURE = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {
        # The hollow source stands FIRST, which is what made it the winner.
        "1": {"work_id": "typed.work1", "language": "la", "voice": "original",
              "rights": "public-domain", "translators": [], "container": "",
              "edition": "Edition 1", "edition_published": "1900", "date": 301},
        "2": _voice_source(1),
    },
    "fragments": [_voice_fragment(1, source="1"), _voice_fragment(2, source="2")],
    "leads": [], "blocked": [], "refusals": {},
})

V7_ABSENCE_SLOT_INDEX = _fixture({"absences": {
    "typed.work1": [{"language": "en", "finding": "none-published",
                     "reason": "No English translation has been published."}],
}})

# The absence members themselves, hollow: a record naming no language is about
# nothing, and a scalar and a null are not records at all. None of them may
# make a row, take a slot, or enter a count.
V7_ABSENCE_MEMBER_INDEX = _fixture({"absences": {
    "typed.work1": [{}, None, 4, "not a record",
                    {"language": "en", "finding": "in-copyright",
                     "reason": "The only rendering is in copyright."}],
    "typed.work2": [{}, None, 9],
}})

# ==========================================================================
# V7 §8 — a refusal that states no locus
#
# "Boundary not established" is the strongest sentence this page says about a
# text it did not write. V6 required only a nonempty `note`, so a note filed
# under any chapter, carrying no recognized `kind`, established it.
V7_REFUSAL_FIXTURE = _fixture({
    "token": "Gen", "chapter": 2, "text_prefix": "structure/catena/text/",
    "sources": {"1": _voice_source(1)},
    "fragments": [_voice_fragment(1, id="refusal-sibling",
                                  extent={"token": "Gen", "first_chapter": 2,
                                          "first_verse": 1, "last_chapter": 2,
                                          "last_verse": 1})],
    "leads": [], "blocked": [],
    "refusals": {"douay-rheims": [
        # A note about ANOTHER chapter.
        {"chapter": 1, "verse": None, "kind": "displaced",
         "note": "a note about the chapter before this one"},
        # A note with no kind the projection ever recorded.
        {"chapter": 2, "verse": None, "note": "a note carrying no kind"},
        # A kind that is not one of the two.
        {"chapter": 2, "verse": None, "kind": "invented",
         "note": "a note carrying a kind this projection never wrote"},
        # A chapter that is not a number.
        {"chapter": "2", "verse": None, "kind": "displaced",
         "note": "a note whose chapter is text"},
        # Hollow, and a note that is only whitespace.
        {}, {"kind": "displaced", "chapter": 2, "note": "   "},
    ]},
})

# The same chapter with ONE well-formed record among the malformed ones, last,
# so a valid refusal is still found however the broken members are arranged.
V7_REFUSAL_VALID = _fixture(dict(
    V7_REFUSAL_FIXTURE,
    refusals={"douay-rheims": list(
        V7_REFUSAL_FIXTURE["refusals"]["douay-rheims"]) + [
            {"chapter": 2, "verse": None, "kind": "displaced",
             "note": "the numbering of this chapter is displaced in this edition"}]}))

# ==========================================================================
# V7 §10 — `partial`, and the rights prose it may license
#
# `partial` is prose or it is nothing: the generator writes it as a
# whitespace-collapsed string and omits it when empty. Every form below is a
# malformed value or a value detached from the one finding that can license
# it, and none may reach "Partly public domain — …".
V7_PARTIAL_INDEX = _fixture({"absences": {
    "typed.work1": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": {"offer": "a record, not prose"}}],
    "typed.work2": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": ["a", "list"]}],
    "typed.work3": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": 1893}],
    "typed.work4": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": True}],
    "typed.work5": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": None}],
}})

# A `partial` that IS prose, attached to a parent that cannot license it, and
# one attached to a contradiction — so the offer is refused by the parent's
# state rather than by its own type.
V7_PARTIAL_PARENT_INDEX = _fixture({"absences": {
    "typed.work1": [{"language": "en", "finding": "in-copyright",
                     "reason": "The only rendering is in copyright.",
                     "partial": "an offer beside a closed finding"}],
    "typed.work2": [{"language": "en", "partial": "an offer beside no finding"}],
    "typed.work3": [
        {"language": "en", "finding": "partial-public-domain",
         "reason": "Some of it is out of copyright.",
         "partial": "an offer on one side of a contradiction"},
        {"language": "en", "finding": "none-published",
         "reason": "No English translation has been published."}],
    "typed.work4": [{"language": "en", "finding": "partial-public-domain",
                     "reason": "Some of it is out of copyright.",
                     "partial": "the offer that is genuinely licensed"}],
    "typed.work5": [{"language": "en", "finding": "not-surveyed",
                     "partial": "an offer beside an admission"}],
}})

# `held` is not a list at all: V6 read it as this index holding nothing in any
# book, and said `Nothing held here` of every chapter.
V7_HELD_NOT_A_LIST = _broken_index(held={"Gen": [1]})

# `held` is a list whose one member cannot say which book it is about. It might
# have been this one, so no emptiness may be drawn from the list carrying it.
V7_HELD_UNREADABLE_MEMBER = _broken_index(held=[{"path": "structure/catena/01-gen/",
                                                "present": [1]}])

# A digit width nobody can read composed the WRONG path and reported the 404
# it caused as a broken record — a real request against a file that cannot be.
V7_HELD_BAD_DIGITS = _broken_index(chapter_digits={"width": 3})

# A canon that states one book readably and one not. The readable book still
# serves; what the incomplete list may not do is prove a token is outside it.
V7_PARTIAL_CANON = _broken_index(canon=[
    {"token": "Gen", "name": "Genesis", "chapters": 50,
     "testament": "old", "path": "01-gen"},
    {"name": "A book whose token nobody can read", "chapters": 12},
])

# A voices list carrying a member outside the published route grammar. It is
# not a key this page could ever match an address against, so the list is not
# ground for saying an address names a voice this corpus does not hold.
V7_PARTIAL_VOICES = _broken_index(voices=["original", {"key": "translation:en"}])

# The paragraph LAYER root, unreadable. `bag()` made it `{}`, no path was
# composed, and no path composed was printed as this edition opening no
# paragraph here.
V7_PARAGRAPH_ROOT_SCALAR = "not a paragraph index"

# The paragraph file for ONE chapter, unreadable in three ways.
V7_PARAGRAPH_FILE_SCALAR = "not a paragraph file"

V7_PARAGRAPH_FILE_BREAKS = _fixture({"token": "Gen", "chapter": 1,
                                     "edition": "douay-rheims",
                                     "breaks": "not a break record"})

# A verses container that is a LIST. `loadChapter` admits it — `typeof [] ===
# "object"` — so the page received `{ok: true}` and then reported a chapter of
# Scripture as carrying no verses.
V7_VERSES_LIST = {"book": "Gen", "chapter": 1,
                  "verses": ["In principio", "Terra autem erat inanis"]}

# And one that is a record with keys the page cannot read: genuinely
# unreadable, and already distinguished — pinned here so the two answers stay
# apart under V7's reading.
V7_VERSES_UNREADABLE = {"book": "Gen", "chapter": 1,
                        "verses": {"first": "In principio", "01": "padded"}}

# V6 §9 — one verse, written more than one way. `^[0-9]+$` admitted `"01"`
# beside `"1"` and `Number()` folded them together, so verse 1 rendered twice.
V6_PADDED_VERSES = _fixture({
    "book": "Gen", "chapter": 1,
    "verses": {
        "1": "The first verse, sound.",
        "2": "The second verse, sound.",
        "01": "A padded encoding of verse one.",
        "001": "A twice-padded encoding of verse one.",
        "0002": "A padded encoding of verse two.",
        # A padded key with NO canonical sibling: it is not a third verse
        # arriving under an unusual name, it is a key this chapter never wrote.
        "03": "A padded verse three, with no canonical sibling.",
    },
})

# The remaining verse identities, none of which numbers a verse.
V6_UNSAFE_VERSES = _fixture({
    "book": "Gen", "chapter": 1,
    "verses": {
        "1": "The only verse this chapter numbers.",
        "0": "Verse zero.",
        "-2": "A negative verse.",
        "1.5": "A fractional verse.",
        "1e3": "An exponent.",
        " 4 ": "A verse with whitespace in its number.",
        "": "A verse with no number at all.",
        "../5": "A verse whose number is a path.",
        "true": "A verse whose number is a flag.",
    },
})

# V6 §7 — the SAME finding set, listed two ways. The review proved selection
# was first-match, so these two scenarios rendered different rights claims
# about the same works.
_CLOSED_ROW = {"language": "en", "finding": "none-published",
               "reason": "No English translation has been published."}

_PARTIAL_ROW = {"language": "en", "finding": "partial-public-domain",
                "reason": "Only part of it is out of copyright.",
                "partial": "the 1893 selection"}

_UNSURVEYED_ROW = {"language": "en", "finding": "not-surveyed", "reason": ""}

_MALFORMED_ROW = {"language": "en", "finding": {"kind": "in-copyright"},
                  "reason": "A reason standing beside an unreadable finding."}

_UNKNOWN_ROW = {"language": "en", "finding": "no-such-finding",
                "reason": "A finding this project does not define."}

def _finding_order(flip):
    """Every required §7 permutation, in one order or the other."""
    def pair(first, second):
        return [second, first] if flip else [first, second]
    return _fixture({"absences": {
        # a valid absence beside a malformed record
        "typed.work1": pair(_CLOSED_ROW, _MALFORMED_ROW),
        # a valid partial beside a malformed record
        "typed.work2": pair(_PARTIAL_ROW, _MALFORMED_ROW),
        # a valid unsurveyed beside a malformed record
        "typed.work3": pair(_UNSURVEYED_ROW, _MALFORMED_ROW),
        # TWO valid typed findings that say different things. Neither may be
        # chosen over the other by position, and the harsher may not be
        # chosen at all: the record contradicts itself and the page says so.
        "typed.work4": pair(_CLOSED_ROW, _PARTIAL_ROW),
        # an unknown finding beside a valid typed one
        "typed.work5": pair(_UNKNOWN_ROW, _CLOSED_ROW),
    }})

# V6 §8 — `partial` detached from any finding that could license it.
V6_STRAY_PARTIAL_INDEX = _fixture({"absences": {
    "typed.work1": [{"language": "en", "finding": "not-surveyed",
                     "partial": "a stray offer beside an admission"}],
    "typed.work2": [{"language": "en", "finding": "no-such-finding",
                     "partial": "a stray offer beside an unknown finding"}],
    "typed.work3": [{"language": "en",
                     "partial": "a stray offer beside no finding at all"}],
    "typed.work4": [_PARTIAL_ROW],
    "typed.work5": [{"language": "en", "finding": "in-copyright",
                     "reason": "A living author's rendering.",
                     "partial": "a stray offer beside a closed finding"}],
}})

# V6 §6 — a malformed HELD record standing before the valid one, and after it.
# `find` stopped at the first and made the whole book unreadable.
def _held_order(flip):
    broken = {"token": "Gen", "path": "../../escape/", "present": [1]}
    sound_ = {"token": "Gen", "name": "Genesis", "chapters": 50, "fragments": 1,
              "path": "structure/catena/01-gen/", "present": [1],
              "languages": ["la"]}
    return _broken_index(held=[sound_, broken] if flip else [broken, sound_])

# V6 §6 — the required mixed collection with the malformed members MOVED. The
# same set of members in a different order must produce the same page.
V6_MIXED_REORDERED = _fixture({
    "token": "Gen", "chapter": 1, "text_prefix": "structure/catena/text/",
    "sources": {
        "1": _voice_source(1, author="First Author", work="First Work"),
        "5": _voice_source(5, author="Last Author", work="Last Work"),
    },
    "fragments": [
        None,
        _voice_fragment(1, id="mixed-first"),
        7,
        _voice_fragment(2, id={"not": "an id"}, source="1"),
        _voice_fragment(5, id="mixed-last"),
    ],
    "leads": [
        13,
        {"author": "Lead One", "title": "Lead Work One", "date": "500"},
        None,
        {"author": "Lead Two", "title": "Lead Work Two", "date": "600"},
        {"author": {"n": 1}, "title": ["x"], "date": {}},
    ],
    "blocked": [
        {"author": 5, "work": [], "reason": {}},
        None,
        {"author": "Blocked One", "work": "Blocked Work One", "reason": "rights"},
        21,
        {"author": "Blocked Two", "work": "Blocked Work Two", "reason": "rights"},
    ],
    # The valid refusal record LAST, behind three that state nothing.
    "refusals": {"douay-rheims": [
        {}, {"note": {"broken": True}}, {"kind": "displaced"},
        {"chapter": 1, "verse": None, "kind": "displaced",
         "note": "the numbering of this chapter is displaced in this edition"},
    ]},
})

# The same chapter whose refusal list holds only records that state nothing.
# `{}` satisfied the record shape and manufactured "Boundary not established"
# — a claim about Scripture's own numbering, made by an empty object.
V6_EMPTY_REFUSAL = _fixture(dict(
    V6_MIXED_REORDERED,
    refusals={"douay-rheims": [{}, {"note": "   "}, {"kind": "displaced"}]}))

# The replay plan: only the scenarios the curated classes read.
SCENARIOS = [
    {"name": "default", "hash": GEN1,
     "steps": [{"do": "openFirstFragment", "label": "opened"}]},
    {"name": "voice-held", "hash": GEN1 + "&voice=translation:en"},
    # THE V3 DEFECT, pinned as its correction. Greek stands in this corpus
    # only as `original:grc`; there are zero Greek translations. A language
    # inventory cannot tell those apart, so V3 read "Genesis holds Greek" and
    # offered a Greek translation nobody has. The exact key is unsupported.
    {"name": "unsupported-voice-greek", "hash": GEN1 + "&voice=translation:grc"},
    # Well formed, and in a language the corpus holds NOTHING in. `zz` is
    # unassigned; `de` is a real ISO code this project has never held a
    # fragment in. Grammar admits both; support must admit neither.
    {"name": "unsupported-voice", "hash": GEN1 + "&voice=translation:zz"},
    # The second supported translation, so "supported" is not a synonym for
    # English: `translation:la` is one source entry in the whole corpus.
    {"name": "voice-latin", "hash": GEN1 + "&voice=translation:la"},
    # Well formed by shape but naming NO language, and one carrying a second
    # delimiter: both are malformed, and must not reach the support question.
    {"name": "voice-empty-language", "hash": GEN1 + "&voice=translation:"},
    {"name": "voice-extra-delimiter", "hash": GEN1 + "&voice=translation:en:extra"},
    # The refused Greek key over a live document, and back again: the refusal
    # must not strand the page or lose the reader's supported voice.
    {"name": "unsupported-greek-change", "hash": GEN1 + "&voice=translation:en",
     "steps": [{"do": "hash", "value": GEN1 + "&voice=translation:grc",
                "label": "greek"},
               {"do": "hash", "value": GEN1 + "&voice=translation:en",
                "label": "supported-again"}]},
    # Every remaining typed sink at once, under a supported translation so the
    # absence view renders beside the chapter.
    {"name": "malformed-structure", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": MALFORMED_STRUCTURE_FIXTURE},
     "patch": {"structure/catena/index.json": MALFORMED_ABSENCES}},
    # Case is part of the closed grammar, so an upper-case code is MALFORMED
    # and not merely unsupported: the two refusals must not collapse.
    {"name": "invalid-voice-upper", "hash": GEN1 + "&voice=translation:EN"},
    {"name": "unsupported-voice-real-code", "hash": GEN1 + "&voice=translation:de"},
    # Supported -> unsupported -> supported over a live document: the refusal
    # must not strand the page in the error state or lose the reader's voice.
    {"name": "unsupported-voice-change", "hash": GEN1 + "&voice=translation:en",
     "steps": [{"do": "hash", "value": GEN1 + "&voice=translation:zz",
                "label": "unsupported"},
               {"do": "hash", "value": GEN1 + "&voice=translation:en",
                "label": "supported-again"}]},
    # Genesis 10 holds 71 fragments, every one in its author's own Latin: the
    # selected-empty-voice chapter finding 8 demands be told truthfully.
    {"name": "voice-empty-chapter", "hash": GEN10_ENGLISH},
    {"name": "numbering-refusal", "hash": "#book=Ps&chapter=13&bible=king-james-version"},
    {"name": "acquisition-only", "hash": "#book=Ex&chapter=3&bible=douay-rheims"},
    # Exodus 1 is absent from the index's `present` list: no spine is asked for.
    {"name": "nothing-held", "hash": "#book=Ex&chapter=1&bible=douay-rheims"},
    {"name": "narrow", "hash": GEN1, "narrow": True},
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
    # ---------------------------------------------------------------- V5 §5
    # Everything held, which is the selection the review's own replay used.
    {"name": "malformed-language-held", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MALFORMED_LANGUAGE_FIXTURE}},
    # And a Bible whose own language is a record, which reached the passage
    # element's `lang` by the same route and was never under test at all.
    {"name": "malformed-bible-language", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MALFORMED_LANGUAGE_FIXTURE},
     "patch": {"bibles.json": {"bibles": [
         {"id": "douay-rheims", "label": "Douay-Rheims", "language": {"code": "en"},
          "numbering": "vulgate", "psalter": "vulgate", "psalm_titles": "included",
          "edition": "1899", "rights": "public-domain"}]}}},
    # ---------------------------------------------------------------- V5 §6
    {"name": "mixed-collection", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MIXED_COLLECTION_FIXTURE}},
    {"name": "mixed-no-refusal", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MIXED_NO_REFUSAL_FIXTURE}},
    # ---------------------------------------------------------------- V5 §7
    {"name": "typed-absence", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": TYPED_ABSENCE_FIXTURE},
     "patch": {"structure/catena/index.json": TYPED_ABSENCE_INDEX}},
    # ---------------------------------------------------------------- V5 §8
    {"name": "malformed-verses", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json": MALFORMED_VERSES,
               "structure/paragraphs/douay-rheims/01-gen/001.json": MALFORMED_BREAKS}},
    # Every verse unreadable, but verses DID arrive. "carries no verses" is a
    # claim about the edition and this page may not make it from a parse
    # failure.
    {"name": "unreadable-verses", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json":
               {"book": "Gen", "chapter": 1, "verses": {"1": {}, "2": ["x"]}}}},
    {"name": "malformed-numbers", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MALFORMED_NUMBER_FIXTURE}},
    # A held path that is not text. Composed raw it became a fetched URL.
    {"name": "malformed-held-path", "hash": GEN1,
     "files": {"structure/catena/index.json": _broken_index(
         held=[{"token": "Gen", "path": {"at": "somewhere"}, "present": [1]}])}},
    # A `present` list this page cannot read. Absence from an unreadable list
    # proves nothing, so it may not become "Nothing held here".
    {"name": "unreadable-present", "hash": GEN1,
     "files": {"structure/catena/index.json": _broken_index(
         held=[{"token": "Gen", "path": "structure/catena/01-gen/",
                "present": [1, {"chapter": 2}]}])}},
    # Bootstrap: a canon whose members are not books. This threw between the
    # last fetch and the first render, outside every funnel, and left the page
    # saying "Loading…" for ever with its controls disabled.
    {"name": "malformed-canon", "hash": "",
     "files": {"structure/catena/index.json": _broken_index(
         canon=[None, 7, "Gen", {"token": "Gen"}])}},
    # An index that is not a record at all.
    {"name": "scalar-index", "hash": "",
     "files": {"structure/catena/index.json": "not an index"}},
    # ---------------------------------------------------------------- V5 §9
    # Route completion, not parse rejection. Each of these begins CANONICAL
    # and meets malformed data afterwards, because the committed scenarios all
    # began malformed and therefore proved nothing about a page that had
    # already established a route and a history.
    #
    # 1 + 4 + 6. A valid bootstrap, a real route, then a chapter whose
    # collection members are malformed — reached by a reader action, so the
    # push/replace question is live.
    {"name": "arrival-then-malformed-member", "hash": GEN1,
     "files": {"structure/catena/01-gen/002.json": MIXED_COLLECTION_FIXTURE},
     "steps": [{"do": "selectChapter", "value": "2", "label": "moved"}]},
    # The same, arriving by address rather than by action: an arrival may
    # complete in place but may never push.
    {"name": "hash-then-malformed-member", "hash": GEN1,
     "files": {"structure/catena/01-gen/002.json": MIXED_COLLECTION_FIXTURE},
     "steps": [{"do": "hash", "value": GEN2, "label": "moved"}]},
    # 2. PARTIAL ARRIVAL. The spine is parked in flight while the chapter text
    # and the paragraph layer land; the malformed spine arrives last.
    {"name": "partial-arrival-malformed", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MIXED_COLLECTION_FIXTURE},
     "defer": ["structure/catena/01-gen/"],
     "steps": [
         # Releasing nothing: the label is how a snapshot is taken WHILE the
         # spine is still in flight, which is the state under test.
         {"do": "release", "path": "nothing-matches-this", "label": "pending"},
         {"do": "release", "path": "structure/catena/01-gen/001.json",
          "label": "arrived"}]},
    # 3 + 5 + 7. A malformed ACTION payload on an otherwise valid route, then
    # a retry that succeeds. Opening a fragment must complete its own state
    # and touch the route not at all.
    {"name": "malformed-action-then-retry", "hash": GEN1,
     "files": {"structure/catena/text/mixed-first.json":
               {"id": "mixed-first", "text": {"not": "text"},
                "basis": ["not", "text"], "date_basis": 5},
               "structure/catena/01-gen/001.json": MIXED_COLLECTION_FIXTURE},
     "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "opened"},
         {"do": "release", "path": "structure/catena/text/mixed-first.json",
          "label": "malformed-arrived"},
         {"do": "selectChapter", "value": "2", "label": "moved-after"},
     ]},
    # ---------------------------------------------------------------- §5
    # THE ROOT LANGUAGE RECORD. The review read `Douay-Rheims ([object
    # Object])` out of the edition control in real Chromium; nothing here
    # could see it, because the control was never projected and because the
    # page guessed `en` wherever it rejected a language.
    {"name": "bible-language-forms", "hash": GEN1,
     "files": {"bibles.json": V6_BIBLE_LANGUAGES}},
    # The same page under a supported translation, so the fragment sink, the
    # passage sink, the chip, the filter and the absence view all render.
    {"name": "bible-language-forms-voice", "hash": GEN1 + "&voice=translation:en",
     "files": {"bibles.json": V6_BIBLE_LANGUAGES}},
    # An edition that cannot name itself is no edition; the sound ones stand.
    {"name": "bible-identity-forms", "hash": GEN1,
     "files": {"bibles.json": V6_BIBLE_IDENTITIES}},
    # ---------------------------------------------------------------- §6
    # The required mixed collection with every malformed member MOVED, and
    # the valid refusal record standing last behind three that state nothing.
    {"name": "mixed-reordered", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V6_MIXED_REORDERED}},
    # Refusal records that satisfy the shape and state nothing at all.
    {"name": "empty-refusal-records", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V6_EMPTY_REFUSAL}},
    # A malformed HELD record before the valid one, and after it.
    {"name": "held-malformed-first", "hash": GEN1,
     "files": {"structure/catena/index.json": _held_order(False)}},
    {"name": "held-malformed-last", "hash": GEN1,
     "files": {"structure/catena/index.json": _held_order(True)}},
    # ---------------------------------------------------------------- §7
    # THE SAME FINDING SET, LISTED TWO WAYS.
    {"name": "finding-order", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": TYPED_ABSENCE_FIXTURE},
     "patch": {"structure/catena/index.json": _finding_order(False)}},
    {"name": "finding-order-reversed", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": TYPED_ABSENCE_FIXTURE},
     "patch": {"structure/catena/index.json": _finding_order(True)}},
    # ---------------------------------------------------------------- §8
    # `partial` detached from every finding that could license the words.
    {"name": "stray-partial", "hash": GEN1 + "&voice=translation:en",
     "files": {"structure/catena/01-gen/001.json": TYPED_ABSENCE_FIXTURE},
     "patch": {"structure/catena/index.json": V6_STRAY_PARTIAL_INDEX}},
    # ---------------------------------------------------------------- §9
    # ONE VERSE, WRITTEN MORE THAN ONE WAY.
    {"name": "padded-verses", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json": V6_PADDED_VERSES}},
    {"name": "unsafe-verses", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json": V6_UNSAFE_VERSES}},
    # THE SAME FIXTURE WITH EVERY REFUSED FRAGMENT ACTUALLY OPENED. Opening
    # is what turns an id into a URL, so a scenario that opens only the safe
    # one proves nothing about the six it refused: the assertion that no
    # unsafe path was requested would hold because nothing asked.
    {"name": "unsafe-identities-opened", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V6_UNSAFE_IDENTITY_FIXTURE},
     "steps": [
         {"do": "openFragmentOf", "author": "Author 2", "label": "traversal"},
         {"do": "openFragmentOf", "author": "Author 3", "label": "spaced"},
         {"do": "openFragmentOf", "author": "Author 4", "label": "uppercase"},
         {"do": "openFragmentOf", "author": "Author 5", "label": "blank"},
         {"do": "openFragmentOf", "author": "Author 6", "label": "trailing"},
         {"do": "openFragmentOf", "author": "Author 7", "label": "encoded"},
         {"do": "openFragmentOf", "author": "Author 1", "label": "safe"},
     ]},
    # AN EDITION ID CITED BY THE ADDRESS. An id becomes a directory in the
    # chapter request, so an edition record that cannot name itself must not
    # be routable: admitted to the manifest it was a published edition so far
    # as the address grammar could tell, and the page fetched through it.
    {"name": "unsafe-bible-route", "hash": "#book=Gen&chapter=1&bible=../../escape",
     "files": {"bibles.json": V6_BIBLE_IDENTITIES}},
    {"name": "null-index", "hash": GEN1,
     "raw": {"structure/catena/index.json": None}},
    {"name": "null-index-cold", "hash": "",
     "raw": {"structure/catena/index.json": None}},
    {"name": "null-bibles", "hash": GEN1, "raw": {"bibles.json": None}},
    {"name": "list-index", "hash": GEN1,
     "raw": {"structure/catena/index.json": [1, 2, 3]}},
    # --------------------------------------------------------------- §13
    # GENUINELY LATE STALE WORK. A is started and HELD; B is begun and
    # allowed to settle completely; only then does A complete. The V5 §9
    # scenarios released before navigating, so no late work ever existed.
    {"name": "genuinely-late-action", "hash": GEN1,
     "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "a-held"},
         {"do": "selectChapter", "value": "2", "label": "b-settled"},
         {"do": "release", "path": "structure/catena/text/", "label": "a-late"},
     ]},
    {"name": "genuinely-late-action-failure", "hash": GEN1,
     "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "a-held"},
         {"do": "selectChapter", "value": "2", "label": "b-settled"},
         {"do": "release", "path": "structure/catena/text/", "outcome": "fail",
          "label": "a-late"},
     ]},
    # The same shape over a MALFORMED payload, which is where the V5 class
    # made its claim without ever creating late work.
    {"name": "genuinely-late-malformed", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": MIXED_COLLECTION_FIXTURE,
               "structure/catena/text/mixed-first.json":
                   {"id": "mixed-first", "text": {"not": "text"},
                    "basis": ["not", "text"], "date_basis": 5}},
     "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "a-held"},
         {"do": "selectChapter", "value": "2", "label": "b-settled"},
         {"do": "release", "path": "structure/catena/text/", "label": "a-late"},
     ]},
    # A spine held while the reader walks into an INVALID address, which is a
    # terminal state of its own: the held work must not repaint the refusal.
    {"name": "late-after-invalidation", "hash": GEN1, "defer": ["01-gen/001.json"],
     "steps": [
         {"do": "hash", "value": "#book=Foo&chapter=1&bible=douay-rheims",
          "label": "invalid"},
         {"do": "release", "path": "01-gen/001.json", "label": "late"},
     ]},
    # =============================================================== V7 §5
    # `text_path` at the REQUEST SINK. Every fragment is opened, so every
    # request the chapter can cause has been made by the time `fetched` is
    # read; a scenario that opens one fragment proves nothing about the ten
    # beside it.
    {"name": "v7-text-path", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V7_TEXT_PATH_FIXTURE},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    {"name": "v7-text-path-no-prefix", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V7_TEXT_PATH_NO_PREFIX},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    # =============================================================== V8 §1
    # The NAMESPACE at the request sink. A body is PLANTED at the same-stem
    # wrong-namespace address in each scenario, so a leak would be served and
    # rendered rather than quietly 404ing — the journal and the content both
    # have to stay clean.
    {"name": "v8-wrong-namespace-prefix", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V8_WRONG_NAMESPACE_PREFIX,
               "structure/paragraphs/same-stem-1.json": V8_PLANTED_TEXT},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    {"name": "v8-padded-prefix", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V8_PADDED_PREFIX,
               "structure/catena/text/same-stem-1.json": V8_PLANTED_TEXT},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    {"name": "v8-wrong-namespace-carried", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V8_WRONG_NAMESPACE_CARRIED,
               "structure/paragraphs/text/ns-paragraphs-text.json":
                   V8_PLANTED_TEXT},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    # =============================================================== V9 §1
    # The composed escape, cold: a REFUSED prefix beside a valid carried
    # path composes nothing — not the refused form, not the carried form.
    {"name": "v9-refused-prefix-carried", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_REFUSED_PREFIX_WITH_CARRIED,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    {"name": "v9-padded-prefix-carried", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_PADDED_PREFIX_WITH_CARRIED,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    # The door itself, from the two sides that keep it: genuine absence
    # opens it, and a valid prefix never needs it.
    {"name": "v9-absent-prefix-carried", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_ABSENT_PREFIX_WITH_CARRIED,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    {"name": "v9-valid-prefix-carried", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_VALID_PREFIX_WITH_CARRIED,
               "structure/catena/text/deeper/fallback-owned.json":
                   V9_COMPOSED_DEEPER,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    # PREWARMED: chapter 1 loads the carried body legitimately, under no
    # prefix; chapter 2 states a prefix this page refuses while carrying the
    # SAME path. The cached body must not be substituted, and the refused
    # route must cause no new request.
    {"name": "v9-prewarmed-fallback", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_ABSENT_PREFIX_WITH_CARRIED,
               "structure/catena/01-gen/002.json": V9_REFUSED_PREFIX_GEN2,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [
         {"do": "openEveryFragment", "label": "prewarmed"},
         {"do": "selectChapter", "value": "2", "label": "refused"},
         {"do": "openEveryFragment", "label": "opened"},
     ]},
    # GENUINELY LATE: A opens the carried body under genuine absence and is
    # HELD; B walks into the refused chapter, opens its rows and settles
    # terminal; only then does A complete. The refused route owns nothing A
    # can move.
    {"name": "v9-late-fallback", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json":
                   V9_ABSENT_PREFIX_WITH_CARRIED,
               "structure/catena/01-gen/002.json": V9_REFUSED_PREFIX_GEN2,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "defer": ["structure/catena/text/"],
     "steps": [
         {"do": "openFirstFragment", "label": "a-held"},
         {"do": "selectChapter", "value": "2", "label": "b-settled"},
         {"do": "openEveryFragment", "label": "b-opened"},
         {"do": "release", "path": "structure/catena/text/",
          "label": "a-late"},
     ]},
    # ============================================================= V14 §10-13
    # TWO ROWS, ONE ADDRESS. Ownership by path string cannot say which of two
    # projected rows asked; ownership by the row object can.
    {"name": "v14-same-path-rows", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openFirstFragment", "label": "first"},
               {"do": "openEveryFragment", "label": "both"}]},
    # TWO PROJECTIONS, ONE ADDRESS. A second chapter is a second projection
    # carrying the same text address; the request stays with the projection
    # and the row that made it.
    {"name": "v14-two-projections-one-path", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE,
               "structure/catena/01-gen/002.json": V14_SAME_PATH_GEN2,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "steps": [{"do": "openFirstFragment", "label": "first"},
               {"do": "selectChapter", "value": "2", "label": "second"},
               {"do": "openEveryFragment", "label": "opened"}]},
    # A GENUINELY LATE COMPLETION ON A SHARED ADDRESS. Projection A's row
    # starts the request; the request is held; projection B becomes the page
    # and carries the same address; then A completes.
    {"name": "v14-late-same-path", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE,
               "structure/catena/01-gen/002.json": V14_SAME_PATH_GEN2,
               "structure/catena/text/fallback-owned.json":
                   V9_PLANTED_FALLBACK},
     "defer": ["structure/catena/text/fallback-owned.json"],
     "steps": [{"do": "openFirstFragment", "label": "asked"},
               {"do": "selectChapter", "value": "2", "label": "moved"},
               {"do": "openEveryFragment", "label": "reopened"},
               {"do": "release",
                "path": "structure/catena/text/fallback-owned.json",
                "label": "late"}]},
    # =============================================================== V15 §§9-19
    # A HELD, B SETTLED, A LATE — with two documents at one address, and only
    # the FIRST ask of that address parked. B's own request goes through while
    # A's is still in the air. Under V14 there is no second request to let
    # through: B joins A's unresolved promise, stands at `Loading…` until A is
    # released, and then renders A's body.
    {"name": "v15-late-same-path", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE,
               "structure/catena/01-gen/002.json": V14_SAME_PATH_GEN2},
     "bodies": {"structure/catena/text/fallback-owned.json":
                [V15_BODY_A, V15_BODY_B]},
     "deferTurn": {"structure/catena/text/fallback-owned.json": [0]},
     "steps": [{"do": "openFirstFragment", "label": "a-held"},
               {"do": "selectChapter", "value": "2", "label": "moved"},
               {"do": "openEveryFragment", "label": "b-settled"},
               {"do": "release",
                "path": "structure/catena/text/fallback-owned.json",
                "label": "a-late"}]},
    # THE SAME SEQUENCE WITH ONE ADDRESS AND ONE BODY, so the discriminator
    # above is not the two documents doing the work on their own: the route,
    # the row and the projection move exactly as before.
    {"name": "v15-late-same-path-control", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE,
               "structure/catena/01-gen/002.json": V14_SAME_PATH_GEN2},
     "bodies": {"structure/catena/text/fallback-owned.json": [V15_BODY_B]},
     "deferTurn": {"structure/catena/text/fallback-owned.json": [0]},
     "steps": [{"do": "openFirstFragment", "label": "a-held"},
               {"do": "selectChapter", "value": "2", "label": "moved"},
               {"do": "openEveryFragment", "label": "b-settled"},
               {"do": "release",
                "path": "structure/catena/text/fallback-owned.json",
                "label": "a-late"}]},
    # TWO ROWS, ONE ADDRESS, ONE TURN. Both ask before either answer arrives,
    # so neither can be served from a value that has settled: this is the
    # pending case, and under V14 the second row joined the first's request.
    {"name": "v15-same-path-together", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE},
     "bodies": {"structure/catena/text/fallback-owned.json":
                [V15_BODY_A, V15_BODY_B]},
     "steps": [{"do": "openEveryFragment", "label": "both"}]},
    # ONE OWNER'S FAILURE IS NOT ANOTHER'S. The first ask of the shared
    # address is answered 404 and the second a document, in the same turn.
    # Under a path-keyed pending cache the second row joins the first row's
    # rejection and reports a text that was never asked for on its behalf.
    {"name": "v15-same-path-one-fails", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE},
     "bodies": {"structure/catena/text/fallback-owned.json":
                [None, V15_BODY_B]},
     "steps": [{"do": "openEveryFragment", "label": "both"}]},
    # THE SETTLED VALUE, SHARED SAFELY. Row one asks and settles; row two
    # asks afterwards and is answered from what settled, with no request of
    # its own — and applies it as ITSELF.
    {"name": "v15-settled-then-shared", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": V14_SAME_PATH_SPINE},
     "bodies": {"structure/catena/text/fallback-owned.json":
                [V15_BODY_A, V15_BODY_B]},
     "steps": [{"do": "openFirstFragment", "label": "first"},
               {"do": "openEveryFragment", "label": "second"}]},
    # AN UNREADABLE SPINE, RENDERED TWICE. The page substitutes a record for a
    # spine that is a document and not a spine. Under V14 it made a fresh
    # literal on every ask, so one unreadable chapter became a new authority
    # per render and the projection count climbed with the reader's steps.
    {"name": "v15-unreadable-rerendered", "hash": GEN1,
     "raw": {"structure/catena/01-gen/001.json": V15_NOT_A_SPINE},
     "steps": [{"do": "selectChapter", "value": "2", "label": "away"},
               {"do": "selectChapter", "value": "1", "label": "back"}]},
    # ================================================================ V16 §G
    # EVERY CONSUMER OF ONE CHAPTER, ON ONE PAGE. The provenance line is
    # drawn only where a reader asks for a translation that is not held, and
    # no committed scenario asked for one AND opened a body — so provenance
    # and the three ownership consumers had never met on one authority.
    {"name": "v16-whole-roster", "hash": GEN1 + "&voice=translation:en",
     "steps": [{"do": "openEveryFragment", "label": "opened"}]},
    # =============================================================== V7 §7
    {"name": "v7-absence-slot", "hash": GEN10_ENGLISH,
     "files": {"structure/catena/01-gen/010.json": V7_ABSENCE_SLOT_FIXTURE,
               "structure/catena/index.json": _broken_index(
                   absences=V7_ABSENCE_SLOT_INDEX["absences"],
                   voices=["original", "translation:en"],
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 2, "path": "structure/catena/01-gen/",
                          "present": [10], "languages": ["la"]}])}},
    {"name": "v7-absence-members", "hash": GEN10_ENGLISH,
     "files": {"structure/catena/01-gen/010.json": TYPED_ABSENCE_FIXTURE,
               "structure/catena/index.json": _broken_index(
                   absences=V7_ABSENCE_MEMBER_INDEX["absences"],
                   voices=["original", "translation:en"],
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 5, "path": "structure/catena/01-gen/",
                          "present": [10], "languages": ["la"]}])}},
    # =============================================================== V7 §8
    {"name": "v7-refusal-locus", "hash": "#book=Gen&chapter=2&bible=douay-rheims",
     "files": {"structure/catena/01-gen/002.json": V7_REFUSAL_FIXTURE,
               "structure/catena/index.json": _broken_index(
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 1, "path": "structure/catena/01-gen/",
                          "present": [2], "languages": ["la"]}])}},
    {"name": "v7-refusal-valid", "hash": "#book=Gen&chapter=2&bible=douay-rheims",
     "files": {"structure/catena/01-gen/002.json": V7_REFUSAL_VALID,
               "structure/catena/index.json": _broken_index(
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 1, "path": "structure/catena/01-gen/",
                          "present": [2], "languages": ["la"]}])}},
    # ============================================================== V7 §10
    {"name": "v7-partial-values", "hash": GEN10_ENGLISH,
     "files": {"structure/catena/01-gen/010.json": TYPED_ABSENCE_FIXTURE,
               "structure/catena/index.json": _broken_index(
                   absences=V7_PARTIAL_INDEX["absences"],
                   voices=["original", "translation:en"],
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 5, "path": "structure/catena/01-gen/",
                          "present": [10], "languages": ["la"]}])}},
    {"name": "v7-partial-parents", "hash": GEN10_ENGLISH,
     "files": {"structure/catena/01-gen/010.json": TYPED_ABSENCE_FIXTURE,
               "structure/catena/index.json": _broken_index(
                   absences=V7_PARTIAL_PARENT_INDEX["absences"],
                   voices=["original", "translation:en"],
                   held=[{"token": "Gen", "name": "Genesis", "chapters": 50,
                          "fragments": 5, "path": "structure/catena/01-gen/",
                          "present": [10], "languages": ["la"]}])}},
    # ============================================================== V7 §11
    # Roots that cannot support the claim V6 drew from them. Each is read at
    # the sinks a reader actually meets: the tally, the announcement, the
    # notice, and what was requested.
    {"name": "v7-held-not-a-list", "hash": GEN1,
     "files": {"structure/catena/index.json": V7_HELD_NOT_A_LIST}},
    {"name": "v7-held-unreadable-member", "hash": GEN1,
     "files": {"structure/catena/index.json": V7_HELD_UNREADABLE_MEMBER}},
    {"name": "v7-held-bad-digits", "hash": GEN1,
     "files": {"structure/catena/index.json": V7_HELD_BAD_DIGITS}},
    {"name": "v7-partial-canon", "hash": "#book=Zzz&chapter=1&bible=douay-rheims",
     "files": {"structure/catena/index.json": V7_PARTIAL_CANON}},
    {"name": "v7-partial-voices", "hash": "#book=Gen&chapter=1&bible=douay-rheims"
                                          "&voice=translation:en",
     "files": {"structure/catena/index.json": V7_PARTIAL_VOICES}},
    # A paragraph record this page reads perfectly, which records no break.
    # That is the one shape that may say the edition holds no division here.
    {"name": "v7-empty-breaks", "hash": GEN1,
     "files": {"structure/paragraphs/douay-rheims/01-gen/001.json":
               {"edition": "douay-rheims", "token": "Gen", "chapter": 1,
                "breaks": {}}}},
    {"name": "v7-paragraph-root", "hash": GEN1,
     "raw": {"structure/paragraphs/index.json": V7_PARAGRAPH_ROOT_SCALAR}},
    {"name": "v7-paragraph-file", "hash": GEN1,
     "raw": {"structure/paragraphs/douay-rheims/01-gen/001.json":
             V7_PARAGRAPH_FILE_SCALAR}},
    {"name": "v7-paragraph-breaks", "hash": GEN1,
     "files": {"structure/paragraphs/douay-rheims/01-gen/001.json":
               V7_PARAGRAPH_FILE_BREAKS}},
    {"name": "v7-verses-list", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json": V7_VERSES_LIST}},
    {"name": "v7-verses-unreadable", "hash": GEN1,
     "files": {"douay-rheims/chapters/Gen/1.json": V7_VERSES_UNREADABLE}},
]

REPLAY = r"""
'use strict';

/* The catena page, replayed under node. Every file the page is made of is
 * the real one; only the document, the network and the bible chapter text
 * are stubbed — the chapter text because it is generated into the build. */

const fs = require('fs');
const pathlib = require('path');

// V7: the plan arrives as a FILE, not as an argv element. V6 passed the whole
// scenario list as one argument, and the V7 additions carried it past
// `ARG_MAX` — `OSError: [Errno 7] Argument list too long`, which is a limit of
// the operating system and not of the harness. A path costs nothing and has no
// ceiling.
const [, , ROOT, PLAN_PATH] = process.argv;
const PLAN = JSON.parse(fs.readFileSync(PLAN_PATH, 'utf8'));
const DATA = pathlib.join(ROOT, 'src/web/data');
const BROWSER = pathlib.join(ROOT, 'src/web/browser');

/* WHAT THE PAGE LET ESCAPE.
 *
 * Node aborts the process on an unhandled rejection, so a page that lets a
 * failing body write out of its own settle handler would take the whole
 * replay down with it — every scenario in the plan, not only the one that
 * forced the failure — and the probe would be deciding the result instead of
 * reporting it. Recording them keeps the run alive and turns the escape into
 * a FACT about the page: a sink that contains its writes escapes nothing,
 * and one that does not escapes exactly once per failure it did not catch.
 *
 * Nothing is suppressed. Every escape is journalled with the scenario and
 * the step in force, and the assertions require the journal to be empty. */
const escaped = [];
let currentScenario = '';
let currentStep = 'start';
process.on('unhandledRejection', (reason) => {
  escaped.push({
    scenario: currentScenario,
    step: currentStep,
    said: String((reason && reason.message) || reason)
  });
});

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
  /* `lang` REFLECTS, exactly as `id` above does and exactly as the HTML DOM
   * does. This is not shim convenience: it is the whole reason the V4.1
   * review could see `lang="[object Object]"` in real Chromium while every
   * committed test here passed. `element.lang = value` is an IDL attribute
   * whose setter writes the CONTENT attribute, stringifying whatever it is
   * given; a shim that stored it as a plain JavaScript property made the one
   * sink the review proved invisible to the one harness that could have
   * caught it. Reflecting it here is what makes the regression adversarial. */
  get lang() { return this.attributes.lang || ''; }
  set lang(value) { this.attributes.lang = String(value); }
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

function inspect(page, document, location, fetched, hashWrites, replaced, statusWrites, released, requests, replacedStates, history) {
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
    /* EVERY DOM LANGUAGE ATTRIBUTE UNDER THE READING REGION, projected as
     * `class=value` so an assertion can name the sink and the value together.
     * Projected for every scenario, not only the malformed ones, so the
     * cross-scenario coercion sweep covers it too. */
    langAttributes: nodes.filter((one) => one.hasAttribute('lang'))
      .map((one) => (one.className || one.localName) + '=' + one.getAttribute('lang')),
    chapterOpen: Boolean((first('chapter-body') || {}).open),
    chapterCounts: withClass('chapter-count').map(text),
    /* THE RENDERED SCRIPTURE ITSELF, verse by verse, in rendered order.
     * V6. The V5 verse-coercion oracle read `fragmentTexts` — the COMMENTARY —
     * while the fixture it defended corrupted the bible chapter, so a value
     * coerced into Scripture, a verse the chapter never numbered, and one
     * verse rendered twice under two encodings of its own number were all
     * invisible to every test in this file. These are the production sink. */
    verseNumbers: withClass('verse-num').map(text),
    verseTexts: withClass('verse').map(text),
    /* THE WORD-TALLY CHIPS THEMSELVES. `classes` is a deduplicated SET, so
     * the V5 tally oracle read the same value for one chip and for seven. */
    lengths: withClass('fragment-length').map(text),
    /* HOW MANY REFUSALS STAND. "Stated once" was asserted with `assertIn`. */
    refusalCount: withClass('refusal').length,
    /* THE EDITION OPTIONS AS A READER SEES THEM. The V5 review read
     * `Douay-Rheims ([object Object])` out of this control in real Chromium
     * and nothing here could see it: the select was never projected. */
    bibleLabels: byId('bible-select').descendants()
      .filter((one) => one.localName === 'option')
      .map((one) => one.textContent),
    /* AND THE VALUES BEHIND THEM, which are what a selection writes into the
     * route and into a request. A label a reader reads and a value the page
     * routes on are two facts, and only the first was projected. */
    bibleValues: byId('bible-select').descendants()
      .filter((one) => one.localName === 'option')
      .map((one) => String(one.value === undefined ? '' : one.value)),
    /* THE TESTAMENT CLAIM. `New Testament` was printed by an `else`. */
    referenceBookText: text(byId('reference-book')),
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
    /* WHICH WORK EACH ABSENCE ROW IS ABOUT. V6: without these, a claim that
     * "this work is the one whose finding the page declined" could only be
     * inferred from counts and from the per-row reasons, never named. An
     * absence is a claim about a particular man's particular book, so the
     * assertion has to be able to say which. */
    absenceAuthors: withClass('absence-author').map(text),
    absenceWorks: withClass('absence-work').map(text),
    /* WHAT AN ABSENCE ROW SAYS WHEN THE MARKUP IS TAKEN AWAY. The two
     * identity spans are adjacent element children, so the row's flattened
     * text is what a screen reader announces and what a copy takes — and
     * without a delimiter BETWEEN them, two facts read as one word. This is
     * the recursive `textContent` of the row itself, taken exactly as the
     * accessibility tree would take it, so a separator supplied only by CSS
     * (a margin, a `::before`, a gap) would leave it unchanged and the
     * assertion would still fail. */
    absenceRowTexts: withClass('absence').map(text),
    /* AND WHAT THE ROW IS MADE OF, in order. A text node between the two
     * spans is a different DOM from two adjacent spans, and only the first
     * survives being flattened. `#text` names a node whose content is not
     * empty, so a zero-width or whitespace-only filler is not counted as a
     * delimiter. */
    absenceRowNodes: withClass('absence').map((row) => row.childNodes
      .filter((one) => one.nodeType !== 3 || String(one.textContent).trim())
      .map((one) => one.nodeType === 3 ? '#text' : (one.className || one.localName))),
    sectionHeadings: withClass('section-heading').map(text),
    asideNotes: withClass('aside-note').map(text),
    // V7. `T.notice()` is where the page states what it could NOT read about
    // a chapter of Scripture, and no projection carried it: the V6 oracles
    // could only assert that the wrong sentence was absent, never that the
    // right one was present. "Carries no verses" and "arrived in a form this
    // page cannot read" are two different claims and both are read here.
    notices: withClass('notice').map(text),
    leads: withClass('lead').map(text),
    blocked: withClass('blocked').map(text),
    fragmentTexts: withClass('fragment-text').map(text),
    fragmentBases: withClass('fragment-basis').map(text),
    sourceLines: withClass('fragment-source').map(text),
    acknowledgements: withClass('fragment-acknowledgement').map(text),
    acknowledgementAboveText: ackPlacement,
    languages: withClass('fragment-language').map(text),
    // The fragment's own identity chips. They were outside every projection,
    // so the no-coercion sweep could not see a value coerced into them.
    authors: withClass('fragment-author').map(text),
    works: withClass('fragment-work').map(text),
    dates: withClass('fragment-date').map(text),
    extents: withClass('fragment-extent').map(text),
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
    // TERMINAL STATE. Nothing could see a region left claiming work in
    // progress, which is how a render-tail throw hid behind a green suite.
    busy: byId('reading') ? byId('reading').getAttribute('aria-busy') : null,
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
    /* THE VISIBLE FAILURE PARAGRAPH. `T.fail` writes `<p class="error">` into
     * the reading region AND speaks the same words; nothing projected the
     * first, so every terminal-failure assertion was really an assertion
     * about the announcement channel alone. These are two sinks and a page
     * that spoke without rendering would have passed. */
    failureText: (nodes.find((one) => new ClassList(one).contains('error')) || {}).textContent
      || null,
    /* HOW MANY PARKED REQUESTS HAVE ACTUALLY BEEN LET GO. A late completion
     * that changes nothing is otherwise indistinguishable from one the page
     * never subscribed to, so "nothing stale survived" could be true because
     * nothing late ever happened. */
    released: released ? released.count : 0,
    statusWrites: (statusWrites || []).slice(),
    hashWrites: (hashWrites || []).slice(),
    replaced: (replaced || []).slice(),
    /* THE STATE ARGUMENT OF EVERY history WRITE, and the standing
     * history.state. V10, the V9 review: "history.state is not captured by
     * the replay at all" — so a late completion writing state could not be
     * seen, and no vector could pin it. */
    replacedStates: (replacedStates || []).slice(),
    historyState: history && history.state !== undefined ? history.state : null,
    /* THE JOURNAL, OWNED. V10, the V9 review: ownership was inferred by
     * slicing `fetched` against a prior snapshot's length, so a substitute
     * request could hide inside an equal count. Each request carries its
     * sequence and the step in force when it was made — 'start' is the
     * bootstrap, before any step ran. */
    requests: (requests || []).map(
      (one) => ({ seq: one.seq, path: one.path, kind: one.kind,
                  phase: one.phase, outcome: one.outcome })),
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
  /* Every state argument handed to replaceState, in order, and a standing
   * `history.state` the projection can read — the sink the V9 review found
   * the replay did not capture at all. */
  const replacedStates = [];
  const location = {
    search: '',
    pathname: '/catena/',
    get hash() { return hashValue; },
    set hash(next) { hashValue = String(next); hashWrites.push(hashValue); }
  };
  const window = {
    location: location,
    history: {
      state: null,
      replaceState: (state, title, url) => {
        const target = String(url);
        const cut = target.indexOf('#');
        hashValue = cut >= 0 ? target.slice(cut) : '';
        replaced.push(target);
        replacedStates.push(state === undefined ? null : state);
        window.history.state = state === undefined ? null : state;
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
  /* THE OWNED JOURNAL. Beside the flat path list, each request records its
   * sequence and the step in force when it was made, so a test asserts WHOSE
   * request each one is rather than slicing counts. */
  const requests = [];
  const phase = { now: 'start' };

  /* Requests parked in flight: a scenario naming path fragments in `defer`
   * holds every matching response until a `release` step resolves it (or
   * rejects it as a transport failure) — real interleaving, not timing
   * luck. */
  const parked = new Map();
  /* How many parked requests have actually been let go. A test that
   * claims nothing stale survived must be able to show that something
   * late really happened. */
  const released = { count: 0 };

  /* V13: THE PROJECTION IDENTITIES EACH CONSUMER SAW, THE ROWS EACH
   * PROJECTION PRODUCED, AND THE PROJECTION EACH REQUEST BELONGS TO.
   * Declared here, above the transport, because `fetch` writes into
   * `owners` and the model wrappers below write into the other two. */
  const projectionIds = {};
  const projectionRows = [];
  const owners = {};
  /* V14: THE OBJECT EACH CONSUMER ACTUALLY RECEIVED.
   *
   * The V13 review refused V13's identity proof, and was exact about why:
   * the harness called `chapterProjection(file)` itself, beside the
   * consumer, and compared `.id` STRINGS. Two equal ids are two equal
   * strings. What a reviewer is owed is the reference that crossed the
   * consumer boundary, taken where it crossed it.
   *
   * `chapterWitness` is a bounded observation seam in the model: it hands
   * this recorder the exact object the consumer is about to read, and it
   * cannot change what the consumer gets. Identity is decided HERE, in the
   * same realm, by a `Map` keyed on the object — SameValueZero on an object
   * key IS `===`. The integers below are labels for that decision, not the
   * decision; two consumers sharing a label shared an object. */
  const identities = new Map();
  let identityNext = 0;
  const refOf = (object) => {
    if (object === null || typeof object !== 'object') return -1;
    if (!identities.has(object)) identities.set(object, ++identityNext);
    return identities.get(object);
  };
  const witnessLog = [];
  const consumerRefs = {};
  const authoritativeRefs = [];
  const projectionRowRefs = {};
  /* THE ASK THAT CAUSED THE REQUEST ABOUT TO BE MADE. `fragmentText(row)`
   * asks the model for the row's address and then reaches the transport in
   * the same synchronous turn, so the transport consumes the ask that caused
   * it rather than looking for a projected row whose path string matches.
   * A cache hit consumes nothing, which is why the next ask clears it. */
  let pendingAsk = null;
  const asks = [];
  /* V15: THE TRANSPORT OWNER, AND THE BODY APPLICATION.
   *
   * The V14 review found ownership recorded at the address decision and
   * nowhere afterwards, so the roster ended one step before the step that
   * writes the page. `transports` is what the page asked the model for when
   * it created a request — the owner object, the row inside it and the
   * address — and `applied` is what the page held when it wrote a body: the
   * row, the projection that row belongs to, and the content itself. Neither
   * is inferred from a path afterwards. */
  const transports = [];
  const applied = [];
  /* THE BODY A TEXT REQUEST WAS ANSWERED WITH, short enough to read in a
   * ledger and long enough to name a planted marker. */
  /* Taken by OWN DESCRIPTOR, for the same reason the model takes its
   * members that way. This is the journal's own reading of a served
   * document, and a journal that ran a planted accessor — or answered from
   * a planted prototype — would be reporting on itself. It is not a
   * consumer and it may not behave like one. */
  const bodyOf = (doc) => {
    if (!doc || typeof doc !== 'object') return '';
    const spot = Object.getOwnPropertyDescriptor(doc, 'text');
    const said = spot && Object.hasOwn(spot, 'value') ? spot.value : undefined;
    return typeof said === 'string' ? said.slice(0, 48) : '';
  };
  currentScenario = scenario.name;
  currentStep = 'start';

  global.window = window;
  global.document = document;
  global.location = location;
  /* WHAT KIND OF REQUEST IT WAS. V11: the packaged journal has to be
   * readable without the harness, so the type each address stands for is
   * recorded beside it rather than inferred from a prefix by whoever reads
   * the log. Derived from the address alone — no request may name its own
   * kind. */
  const kindOf = (path) =>
    path === 'bibles.json' ? 'editions'
      : path === 'structure/catena/index.json' ? 'catena-index'
        : path === 'structure/paragraphs/index.json' ? 'paragraph-index'
          : path.startsWith('structure/catena/text/') ? 'text'
            : path.startsWith('structure/catena/') ? 'spine'
              : path.startsWith('structure/paragraphs/') ? 'paragraphs'
                : 'scripture';
  global.fetch = async (url) => {
    const path = String(url).replace(/^\.\.\/browse\//, '');
    fetched.push(path);
    /* The journal entry is MUTABLE ON PURPOSE: `outcome` is the one field
     * that moves after the request is made, so a snapshot taken while a
     * request is parked says `held` and the same entry says `released`
     * once it is let go. That is what makes a genuinely-late proof
     * readable from the journal alone. */
    const record = { seq: requests.length, path: path, kind: kindOf(path),
                     phase: phase.now, outcome: 'completed' };
    requests.push(record);
    const has = Object.prototype.hasOwnProperty.call(overrides, path);
    /* V15: HOW MANY TIMES THIS PATH HAS BEEN ASKED, counting this one. Under
     * V14 the question could not arise: one path was one request whatever
     * asked, so one body per path was all a scenario could need. V15 lets two
     * owners ask one address, and a proof that B rendered B's own answer
     * needs A's answer and B's to be DIFFERENT DOCUMENTS at the same path.
     * `bodies` names the answers in order; the last repeats. */
    const turn = fetched.filter((one) => one === path).length - 1;
    const takes = (scenario.bodies || {})[path];
    const body = takes
      ? JSON.parse(JSON.stringify(takes[Math.min(turn, takes.length - 1)]))
      : has ? overrides[path] : corpusFile(path);
    const extra = (scenario.patch || {})[path];
    if (extra && body) mergeInto(body, extra);
    /* A SUCCESSFUL FETCH THAT ANSWERS JSON `null`, which `files` cannot
     * express: there a null body IS the 404, and the two are different facts
     * about the world. A 200 carrying `null` is a valid JSON document that
     * is not the record asked for, and it is the one the V5 review proved
     * threw past the request catch and left the page loading for ever. */
    const raw = scenario.raw || {};
    const rawly = Object.prototype.hasOwnProperty.call(raw, path);
    const served = body;
    const finished = served;
    /* V13: WHO OWNS THIS REQUEST. The page composes no text address of its
     * own, so a `structure/catena/text/…` request can only have come off a
     * projected row — and the row names which projection made it. A request
     * no projection's rows account for is recorded with an empty owner
     * rather than attributed to the nearest one. */
    const held = record.kind === 'text'
      ? projectionRows.filter((one) => one.paths.indexOf(path) !== -1)[0]
      : undefined;
    /* V14: THE ASK THAT CAUSED THIS REQUEST, consumed here. The V13 review
     * found ownership reconstructed by taking the FIRST projected row whose
     * path string matched, which is ambiguous the moment two rows carry one
     * path. The model records the row and its projection when the address is
     * resolved, and the transport takes that record rather than searching
     * for one. The path match survives only as the parent's answer, where
     * there is no ask to consume. */
    const caused = record.kind === 'text' ? pendingAsk : null;
    if (record.kind === 'text') pendingAsk = null;
    owners[record.seq] = {
      // THE ROUTE AS IT STOOD WHEN THE REQUEST WAS MADE, not as it stands
      // when the journal is read. A prewarmed body is fetched under chapter
      // one and read under chapter two, and a journal that stamped both with
      // the later hash would say the earlier request was made somewhere it
      // was not.
      route: location.hash,
      projection: caused ? caused.id : (held ? held.id : ''),
      // V14: the owner as an OBJECT, not as a matched string. -1 where the
      // model exposed no ask, which is the parent.
      owner: caused ? caused.row : -1,
      ownerProjection: caused ? caused.projection : -1,
      ownerPath: caused ? caused.path : '',
      byPath: held ? held.id : '',
      body: held || record.kind === 'text'
        ? bodyOf(rawly ? raw[path] : served) : ''
    };
    const answering = async () => finished;
    const response = rawly
      ? { ok: true, status: 200, json: async () => raw[path] }
      : (served === null || served === undefined)
        ? { ok: false, status: 404, json: async () => null }
        : { ok: true, status: 200, json: answering };
    /* V15: WHICH ASK OF THIS PATH IS HELD. `defer` parks every request whose
     * path carries the piece, which is the whole of the V14 axis. `deferTurn`
     * parks only the listed asks of it, so A's request may be held while B's
     * request for the same address goes through — the sequence the V14 review
     * required and V14 could not construct, because there was no second
     * request to let through. */
    const turning = scenario.deferTurn || {};
    const named = Object.keys(turning).filter((piece) => path.includes(piece))[0];
    const park = named !== undefined
      ? turning[named].indexOf(turn) !== -1
      : (scenario.defer || []).some((piece) => path.includes(piece));
    if (park) {
      record.outcome = 'held';
      return new Promise((resolve, reject) => {
        if (!parked.has(path)) parked.set(path, []);
        parked.get(path).push({
          resolve: () => { record.outcome = 'released'; resolve(response); },
          reject: (error) => { record.outcome = 'failed'; reject(error); }
        });
      });
    }
    return response;
  };

  for (const file of ['shared/browser-core.js', 'catena/catena-model.js', 'catena/catena.js']) {
    const source = fs.readFileSync(pathlib.join(BROWSER, file), 'utf8');
    new Function('window', 'self', 'document', 'fetch', 'location', source)(
      window, window, document, global.fetch, location);
  }
  /* V13: WHICH PROJECTION EACH CONSUMER READ, AND WHICH ONE OWNS EACH
   * REQUEST.
   *
   * The V12 review asked for two things this records. §6: prove that ONE
   * normalized projection identity is what readability, the tally, the
   * rendering, the request/cache/body and the ownership line each used —
   * "not only equal values". §13: ship the ownership rows so a reviewer can
   * check the claim without rerunning the harness.
   *
   * Every model entry point that takes a chapter is asked, before it
   * answers, which projection that chapter resolves to. `chapterProjection`
   * is itself the memoized lookup, so ASKING costs nothing: it returns the
   * projection already made and advances no pass. The ids each consumer saw
   * are kept as a set per consumer, so "one identity, everywhere" is a
   * comparison of lists and not of values.
   *
   * `owners` binds a request to a projection through the row that carried
   * its address: the page composes no text address of its own, so the only
   * thing that can name `structure/catena/text/…` is a row, and the row came
   * from exactly one projection. */
  /* THE PARENT HAS NO PROJECTION TO ASK ABOUT, and this file is replayed
   * against the uncorrected parent as evidence. So every hook below degrades
   * to a recorded absence rather than throwing: at the parent the ids are ''
   * and the census is 0, which is a fact about the parent and reads as one,
   * and every behavioural scenario still runs and still differs. */
  {
    const model = window.CatenaModel;
    const asked = (file) => (typeof model.chapterProjection === 'function'
      ? model.chapterProjection(file).id : '');
    const note = (who, file) => {
      const id = asked(file);
      if (!projectionIds[who]) projectionIds[who] = [];
      if (!projectionIds[who].includes(id)) projectionIds[who].push(id);
      return id;
    };
    const watch = (who, name, at) => {
      const real = model[name];
      if (typeof real !== 'function') return;
      model[name] = function () {
        note(who, arguments[at || 0]);
        return real.apply(this, arguments);
      };
    };
    watch('readability', 'spineUnreadable');
    watch('voices', 'chapterVoices');
    watch('blocked', 'chapterBlocked');
    watch('leads', 'chapterLeads');
    watch('refusal', 'refusalNote');
    watch('absences', 'absenceRows', 1);
    const projected = model.chapterFragments;
    model.chapterFragments = function (file) {
      const id = note('rows', file);
      const made = projected.apply(this, arguments);
      const paths = made.map((row) => row.text_path).filter(Boolean);
      const held = projectionRows.filter((one) => one.id === id)[0];
      if (held) held.paths = paths;
      else projectionRows.push({ id: id, paths: paths });
      return made;
    };
  }
  /* V14: THE WITNESS. Installed on the production seam, never around it.
   *
   * The recorder is handed the projection each consumer is about to read,
   * at the moment the consumer reads it, and — for the request consumer —
   * the row whose address is being resolved. Nothing here recomputes a
   * projection: `rowProjection` is a `WeakMap` lookup on the row itself, so
   * asking it advances no pass and normalizes nothing.
   *
   * At the parent there is no `chapterWitness`, so every V14 identity
   * journal is empty there. That is the parent's answer to the review's
   * first finding and it reads as one: the parent cannot show which object
   * any consumer received, because it offers no way to look. */
  if (typeof window.CatenaModel.chapterWitness === 'function') {
    const model = window.CatenaModel;
    model.chapterWitness((consumer, projection, detail) => {
      const ref = refOf(projection);
      if (consumer === 'normalize') {
        if (authoritativeRefs.indexOf(ref) === -1) {
          authoritativeRefs.push(ref);
          projectionRowRefs[ref] = (projection.rows || []).map(refOf);
        }
      }
      if (!consumerRefs[consumer]) consumerRefs[consumer] = [];
      if (consumerRefs[consumer].indexOf(ref) === -1) {
        consumerRefs[consumer].push(ref);
      }
      const entry = { consumer: consumer, projection: ref, step: phase.now };
      if (consumer === 'request') {
        entry.row = refOf(detail);
        entry.path = detail && typeof detail === 'object'
          ? String(detail.text_path || '') : '';
        entry.owned = refOf(model.rowProjection(detail));
        entry.id = projection.id;
        asks.push(entry);
        pendingAsk = { row: entry.row, projection: entry.projection,
                       id: entry.id, path: entry.path };
      }
      if (consumer === 'transport') {
        entry.owner = refOf(detail);
        entry.row = refOf(detail && detail.row);
        entry.held = refOf(detail && detail.projection);
        entry.path = detail ? String(detail.path || '') : '';
        entry.owned = refOf(model.rowProjection(detail && detail.row));
        entry.id = projection.id;
        transports.push(entry);
      }
      if (consumer === 'body') {
        const wrote = detail && detail.row;
        entry.row = refOf(wrote);
        entry.owned = refOf(model.rowProjection(wrote));
        entry.path = wrote && typeof wrote === 'object'
          ? String(wrote.text_path || '') : '';
        entry.id = projection.id;
        entry.body = bodyOf(detail && detail.content);
        entry.frozen = Boolean(detail && detail.content
          && typeof detail.content === 'object'
          && Object.isFrozen(detail.content));
        /* V16 §D: EVERYTHING THE APPLICATION BOUND, as objects. V15's body
         * detail was `{row, content}` and nothing else, so the sink could
         * be tied to a row and to no transport, no owner and no address —
         * which is precisely how an actual B row came to authorize A's
         * answer. The owner, the projection the owner holds, the address it
         * asked, the finalized value's own identity, whether the completion
         * was a failure and whether the write was confirmed are each taken
         * HERE, at the recording, and each is a label — so `===` is what
         * the assertions downstream are really asking.
         *
         * At the parent these fields are absent from the detail and read
         * as `-1` / `false`, which is the parent's own answer: it recorded
         * an application it could not tie to an owner or to a write. */
        entry.owner = refOf(detail && detail.owner);
        entry.ownerProjection = refOf(detail && detail.projection);
        entry.ownerPath = detail && detail.path !== undefined
          ? String(detail.path || '') : '';
        entry.content = refOf(detail && detail.content);
        entry.failed = Boolean(detail && detail.failed);
        entry.wrote = Boolean(detail && detail.wrote === true);
        const held = detail && detail.content;
        const object = held !== null && typeof held === 'object';
        entry.contentKeys = object ? Object.keys(held) : [];
        entry.contentPrototype = !object ? '-'
          : Object.getPrototypeOf(held) === null ? 'null'
            : Object.getPrototypeOf(held) === Object.prototype
              ? 'Object' : 'other';
        entry.contentScalars = object && entry.contentKeys.every(
          (name) => typeof held[name] === 'string'
            || typeof held[name] === 'boolean');
        /* V16 §C: THE VALUES THEMSELVES, taken by OWN DESCRIPTOR for the
         * same reason `bodyOf` is. Without them the sealed record could be
         * asserted to have the right SHAPE while carrying members no file
         * stated — which is exactly the defect a polluted `Object.prototype`
         * produces in a value built from an ordinary literal, and it is
         * invisible to a key list. */
        entry.contentValues = {};
        for (const name of entry.contentKeys) {
          const spot = Object.getOwnPropertyDescriptor(held, name);
          entry.contentValues[name] =
            spot && Object.hasOwn(spot, 'value') ? spot.value : null;
        }
        applied.push(entry);
      }
      witnessLog.push(entry);
    });
  }
  /* THE OWNERSHIP JOURNAL, derived from the request journal so its outcomes
   * move with it. A journalled request IS a cache miss: the page's cache
   * answers before `fetch` is reached, so a body that is shown with no row
   * here is the hit, and that absence is the claim a test asserts. */
  const ownershipNow = () => requests.map((one) => ({
    seq: one.seq,
    scenario: scenario.name,
    route: (owners[one.seq] || {}).route || '',
    projection: (owners[one.seq] || {}).projection || '',
    // V14: the owning ROW and its projection, as object labels, beside the
    // projection id the path match used to be the only source of.
    owner: (owners[one.seq] || {}).owner === undefined
      ? -1 : owners[one.seq].owner,
    ownerProjection: (owners[one.seq] || {}).ownerProjection === undefined
      ? -1 : owners[one.seq].ownerProjection,
    ownerPath: (owners[one.seq] || {}).ownerPath || '',
    byPath: (owners[one.seq] || {}).byPath || '',
    path: one.path,
    kind: one.kind,
    step: one.phase,
    outcome: one.outcome,
    cache: 'miss',
    body: (owners[one.seq] || {}).body || ''
  }));
  /* ONE SNAPSHOT, TAKEN THE SAME WAY EVERYWHERE. V13: the bootstrap
   * snapshot was taken by a second call that carried none of the ownership
   * axes, so a dump that asked for them found a hole in the first snapshot
   * of every scenario. There is one taker now, and everything it takes
   * carries the same fields. */
  const take = () => {
    const taken = inspect(page, document, location, fetched, hashWrites, replaced, statusWrites, released, requests, replacedStates, window.history);
    taken.ownership = ownershipNow();
    taken.projectionIds = JSON.parse(JSON.stringify(projectionIds));
    taken.projectionPasses = (typeof window.CatenaModel.chapterPasses === 'function' ? window.CatenaModel.chapterPasses() : 0);
    taken.consumerRefs = JSON.parse(JSON.stringify(consumerRefs));
    taken.authoritativeRefs = authoritativeRefs.slice();
    taken.projectionRowRefs = JSON.parse(JSON.stringify(projectionRowRefs));
    taken.witness = JSON.parse(JSON.stringify(witnessLog));
    taken.asks = JSON.parse(JSON.stringify(asks));
    taken.transports = JSON.parse(JSON.stringify(transports));
    taken.applied = JSON.parse(JSON.stringify(applied));
    taken.escaped = escaped.filter((one) => one.scenario === scenario.name)
      .map((one) => ({ step: one.step, said: one.said }));
    return taken;
  };
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
  snapshots.start = take();

  for (const step of scenario.steps || []) {
    // The step's label is in force BEFORE it runs, so every request it
    // causes is journalled under the step that owns it.
    phase.now = step.label || step.do;
    currentStep = phase.now;
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
          released.count += 1;
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
    // V7 §5. Opening ONE fragment cannot fail on a request the page composes
    // for a different one, and the `text_path` regressions are a claim about
    // every member of a collection at once. This opens all of them, in the
    // order they stand, and settles once at the end — so `fetched` afterwards
    // is the complete set of requests the whole chapter can cause.
    } else if (step.do === 'openEveryFragment') {
      for (const body of page.reading.descendants()
             .filter((one) => new ClassList(one).contains('fragment-body'))) {
        body.open = true;
        body.dispatch('toggle');
      }
      await settle();
    }
    /* V13: the ownership journal and the projection census travel WITH the
     * snapshot, so a step's sinks and the projection that owns them are read
     * together rather than joined by hand afterwards. */
    snapshots[step.label || step.do] = take();
  }

  const report = take();
  report.snapshots = snapshots;
  report.ownership = ownershipNow();
  report.projectionIds = projectionIds;
  report.projectionPasses = (typeof window.CatenaModel.chapterPasses === 'function' ? window.CatenaModel.chapterPasses() : 0);
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
        plan_handle, plan_path = tempfile.mkstemp(suffix=".json",
                                                  prefix="catena-plan-")
        os.close(plan_handle)
        try:
            Path(path).write_text(REPLAY, encoding="utf-8")
            Path(plan_path).write_text(json.dumps(SCENARIOS), encoding="utf-8")
            result = subprocess.run(
                [NODE, path, str(ROOT), plan_path],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0:
                raise AssertionError(result.stderr.strip() or "the replay harness exited non-zero")
            _REPLAYED = json.loads(result.stdout)
        finally:
            os.unlink(path)
            os.unlink(plan_path)
    return _REPLAYED


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
        self.assertEqual(error["heading"], "This address cannot be used as written")
        self.assertEqual(error["state"], "error")
        self.assertTrue(any(named in one for one in error["details"]),
                        f"{named!r} not named in {error['details']}")
        self.assertTrue(error["recoveryHref"], "recovery must be offered")
        self.assertEqual(page["referenceText"], "Address not used")
        self.assertEqual(page["fragmentCount"], 0, "no content may render under the error")
        self.assertFalse([one for one in page["fetched"] if "/chapters/" in one],
                         "no chapter may be fetched for an invalid address")

    @staticmethod
    def rendered_state(snap: dict) -> dict:
        """The rendered state alone — the projections that must be identical
        for one URL + data whatever the arrival path — with the per-session
        history/network journals left out."""
        journals = {"fetched", "hashWrites", "replaced", "statusWrites",
                    "snapshots", "released", "requests", "replacedStates",
                    "ownership", "projectionIds", "projectionPasses",
                    # V14: the identity and ownership journals are
                    # per-session records of HOW the page was reached, never
                    # of what it rendered.
                    "consumerRefs", "authoritativeRefs", "projectionRowRefs",
                    "witness", "asks",
                    # V15: the transport-owner and body-application journals
                    # are per-session records of WHO asked and who wrote, not
                    # of what stands on the page.
                    "transports", "applied", "escaped"}
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
        # SUPPORTED, and not held on THIS chapter. Genesis 10 holds originals
        # only, while `translation:en` is held elsewhere in the corpus, so
        # "none here" is a true statement about a chapter rather than an
        # invented statement about the holdings.
        page = self.page("voice-empty-chapter")
        self.assertEqual(page["voice"], "translation:en")
        self.assertEqual(page["hash"], GEN10_ENGLISH)
        self.assertEqual(page["hashWrites"], [])
        self.assertIn("English translation — none here", page["voiceLabels"])
        self.assertEqual(page["fragmentCount"], 0)


class UnsupportedVoiceTest(ReplayTest):
    """V3 finding 5/8 — shape is not support.

    `voice=translation:zz` satisfied the two-to-three-lowercase-letter grammar
    and was then carried into the page as though the corpus held a ZZ
    translation and merely had none on this chapter, producing the invented
    claim "none in ZZ translation". A voice naming a language the index holds
    nothing in is a different thing from a voice the chapter lacks, and the
    page must not spend a holding it has never had to describe one.
    """

    UNSUPPORTED = ("unsupported-voice", "unsupported-voice-real-code")

    def test_an_unsupported_voice_fails_closed(self):
        self.assert_failed_closed(
            "unsupported-voice",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:zz",
            "voice=translation:zz is not a voice this corpus holds")

    def test_a_real_but_unheld_language_code_fails_closed_the_same_way(self):
        # `de` is well formed and nameable; the corpus has never held a German
        # fragment, so naming it is exactly the same invention as `zz`.
        self.assert_failed_closed(
            "unsupported-voice-real-code",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:de",
            "voice=translation:de is not a voice this corpus holds")

    def test_an_upper_case_code_is_malformed_rather_than_unsupported(self):
        # `EN` names a language the corpus does hold; it still fails the closed
        # lowercase grammar, and must be refused for the shape, not the set.
        self.assert_failed_closed(
            "invalid-voice-upper",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:EN",
            "voice=translation:EN is not a voice —")

    def test_the_refusal_is_distinct_from_the_malformed_one(self):
        # Three states, not two: malformed shape, supported voice, and a
        # well-formed voice the corpus cannot answer.
        malformed = self.page("invalid-voice")["errorSections"][0]["details"]
        unsupported = self.page("unsupported-voice")["errorSections"][0]["details"]
        self.assertTrue(any("is not a voice —" in one for one in malformed))
        self.assertFalse(any("is not a voice —" in one for one in unsupported))
        self.assertTrue(any("this corpus holds" in one for one in unsupported))
        self.assertFalse(any("this corpus holds" in one for one in malformed))

    def test_no_unsupported_voice_ever_claims_a_holding(self):
        # The review's exact complaint, asserted as a contradiction: no
        # rendered state may name the language or claim an absence in it.
        for name in self.UNSUPPORTED:
            page = self.page(name)
            with self.subTest(scenario=name):
                rendered = json.dumps(self.rendered_state(page), ensure_ascii=False)
                for invented in ("none in ZZ translation", "ZZ translation",
                                 "none in German translation", "German translation",
                                 "none here"):
                    self.assertNotIn(invented, rendered)
                self.assertEqual(page["tallyText"], "")
                self.assertEqual(page["voiceLabels"], ["Everything held"])

    def test_the_unsupported_voice_is_dropped_from_the_recovery_route(self):
        # The rest of the address is sound, so recovery keeps it and offers
        # the page without the voice it cannot honour.
        page = self.page("unsupported-voice")
        self.assertEqual(page["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")

    def test_a_supported_voice_survives_a_pass_through_an_unsupported_one(self):
        # supported -> unsupported -> supported, over one live document.
        first = self.snapshot("unsupported-voice-change", "start")
        self.assertEqual(first["voice"], "translation:en")
        self.assertEqual(first["fragmentCount"], 14)
        broken = self.snapshot("unsupported-voice-change", "unsupported")
        self.assertEqual(broken["referenceText"], "Address not used")
        self.assertEqual(broken["fragmentCount"], 0)
        back = self.snapshot("unsupported-voice-change", "supported-again")
        self.assertEqual(back["voice"], "translation:en")
        self.assertEqual(back["fragmentCount"], 14)
        self.assertEqual(back["hash"], GEN1 + "&voice=translation:en")

    def test_the_supported_set_is_read_from_the_index_not_from_the_key(self):
        # The closed set is Catena-owned runtime truth the route already has,
        # never manufactured from the voice string or from a new request.
        script = held(CATENA / "catena.js")
        # The WHOLE key against the whole keys the corpus holds. A language
        # inventory is not a voice authority: `held[].languages` carries `grc`
        # because Greek stands here as an original, and answering support from
        # it manufactured `translation:grc`.
        # V5 tightened the container the same line reads: `|| []` turned a
        # STRING `voices` into a container whose `.includes` matches by
        # substring, so `translation:e` passed against a corpus holding only
        # `translation:en`. `list()` refuses a scalar outright. The assertion
        # below is the stricter form of the same requirement, not a relaxation.
        # CORRECTED ORACLE (V7). The line this named moved to
        # `catena-model.js` with the rest of the address judgment, and it
        # moved because it was WRONG in a way a source-text assertion could
        # not see: `list(index.voices)` answers `[]` for a voices value nobody
        # can read, so every address was then told this corpus holds no such
        # voice — a negative about the corpus drawn from a parse failure. The
        # requirement is unchanged and the assertion follows it to the file
        # that now carries it: the WHOLE key, against the whole keys the
        # corpus states, read as keys rather than as a container of anything.
        model = held(CATENA / "catena-model.js")
        self.assertIn("!list(bag(voices).keys).includes(voice)", model)
        self.assertNotIn("(index.voices || [])", script + model)
        self.assertNotIn("(one.languages || []).includes(", script + model)
        self.assertEqual(self.page("unsupported-voice")["fetched"],
                         ["structure/catena/index.json", "bibles.json",
                          "structure/paragraphs/index.json"])

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
        self.assertEqual(over["referenceText"], "Address not used")


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
        self.assertIn("The address is unchanged", spoken[0])
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
            ["The address is unchanged; the values not used are listed."])


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


class RecoveryFocusVisibilityTest(unittest.TestCase):
    """The integration review's second merge blocker — the ring nobody drew.

    `RecoveryFocusTest` and `RecoveryFailureFocusTest` above assert that
    recovery lands on `#reading`, on both the success and the failure arm, and
    both passed the whole time. They could not see the defect, and the reason
    they could not is worth stating: the replay shim has no cascade and no
    computed style. It reports `activeElement`, which was right; the shared
    shell's `.reading:focus { outline: none }` then out-ranked the universal
    `:focus-visible` rule, and the browser drew nothing. A keyboard reader was
    being moved somewhere the page would not show them.

    So this class asserts nothing itself. It runs the real-Chromium harness
    against the BUILT artifact and reads its report, because a computed
    outline is the only form the claim can honestly take. The harness compares
    the focused region with the same region at rest, measures the ring's
    contrast against the surface behind it from resolved colours, and checks
    the mouse case on a document of its own — Chromium keeps the
    focus-visible state of an element that already had it, so a press tested
    straight after a keyboard recovery would answer a different question.

    Its falsifiability is not assumed: reverting the two corrections in a copy
    of the build makes `absence-rows-read-apart-when-flattened`,
    `recovery-focus-is-visible-in-real-chromium` and
    `failed-recovery-focus-is-visible-in-real-chromium` fail with
    `outline-style is none — this is the reviewed defect` and
    `flattened together: Ambrose of MilanHexameron…`, and nothing else moves.
    """

    HARNESS = ROOT / "tools/tests/catena_recovery_focus_gate.mjs"
    SITE = ROOT / "build/public-alpha/site"

    #: Every assertion the harness is required to make. A name that stops
    #: being reported is a weakened proof, and the run is checked against this
    #: list rather than against its own output.
    REQUIRED = (
        # blocker 1, in the browser as well as in the shim
        "absence-rows-read-apart-when-flattened",
        # blocker 2, success path
        "recovery-offer-is-a-keyboard-reachable-link",
        "recovery-link-itself-shows-a-focus-ring",
        "recovery-focus-lands-on-the-reading-region",
        "recovery-focus-is-visible-in-real-chromium",
        "the-page-really-recovered-behind-the-ring",
        # blocker 2, no permanent mouse decoration
        "a-mouse-press-on-the-region-draws-no-ring",
        "a-keyboard-arrival-after-the-press-still-draws-the-ring",
        # blocker 2, failure/recovery path
        "the-failing-recovery-offer-is-still-keyboard-reachable",
        "the-recovery-really-failed",
        "failed-recovery-focus-is-visible-in-real-chromium",
        "the-failure-a-reader-is-standing-on-is-the-one-they-can-read",
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.source = held(cls.HARNESS)

    def test_the_harness_is_syntactically_valid_javascript(self) -> None:
        if NODE is None:
            raise unittest.SkipTest("node is not installed")
        subprocess.run([NODE, "--check", str(self.HARNESS)], cwd=ROOT, check=True)

    def test_the_harness_depends_on_nothing_outside_the_node_standard_library(self) -> None:
        # This host has no npm and no node_modules, and a proof that cannot be
        # run is not a proof.
        found = re.findall(r"^import\s+[^;]*?from\s+'([^']+)'", self.source, re.M)
        self.assertTrue(found, "the harness imports nothing at all")
        for one in found:
            self.assertTrue(one.startswith("node:"), f"{one} is not a node: builtin")

    def test_the_harness_reads_computed_style_and_not_the_stylesheet(self) -> None:
        # The whole point of the correction's proof: what the BROWSER resolved,
        # taken off the element the browser reports as active. A harness that
        # searched `catena.css` for a selector would pass with the ring still
        # suppressed by the shared shell.
        self.assertIn("getComputedStyle", self.source)
        self.assertIn("document.activeElement", self.source)
        self.assertIn("matches(':focus-visible')", self.source)
        self.assertNotIn("catena.css", self.source)

    def test_the_harness_is_honest_when_it_cannot_observe_anything(self) -> None:
        self.assertIn("const EXIT_NO_BROWSER = 3", self.source)
        self.assertIn("TRIPTYCH_CHROME", self.source)
        self.assertIn("reports nothing rather than reporting a pass", self.source)

    def test_the_harness_asserts_a_difference_and_a_contrast_not_a_colour(self) -> None:
        # A region that always carried a ring would satisfy every absolute
        # assertion and tell a reader nothing, and "sufficient contrast" is a
        # number. Both are read from resolved values, so the stylesheet may say
        # `var(--focus)` and the proof still holds.
        self.assertIn("RESTING_READING", self.source)
        self.assertIn("indistinguishable from the resting state", self.source)
        self.assertIn("0.2126", self.source, "WCAG relative luminance is not computed")
        self.assertIn("contrast.ratio >= 3", self.source)

    def test_real_chromium_shows_the_recovery_focus(self) -> None:
        binary = browser_binary()
        if binary is None:
            raise unittest.SkipTest(
                "no Chromium binary is installed; set TRIPTYCH_CHROME to one "
                "(the repository installer deliberately omits the browser)")
        if not (self.SITE / "catena/index.html").is_file():
            raise unittest.SkipTest(
                "no built Catena page at build/public-alpha/site; run `make public-site`")
        if NODE is None:
            raise unittest.SkipTest("node is not installed")
        environment = dict(os.environ)
        environment.setdefault("TRIPTYCH_CHROME", binary)
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "focus.json"
            finished = subprocess.run(
                [NODE, str(self.HARNESS), "--json-out", str(report_path)],
                cwd=ROOT, env=environment,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertIn(finished.returncode, (0, 1),
                          finished.stderr.decode()[-2000:])
            self.assertTrue(report_path.is_file(),
                            finished.stderr.decode()[-2000:])
            report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertTrue(report["chromium"].startswith(("Chrome/", "HeadlessChrome/")),
                        report["chromium"])
        recorded = {one["name"]: one for one in report["assertions"]}
        for name in self.REQUIRED:
            with self.subTest(assertion=name):
                self.assertIn(name, recorded, "the harness stopped making this claim")
                self.assertEqual(recorded[name]["status"], "pass",
                                 recorded[name]["detail"])
        self.assertEqual(report["failures"], [])
        self.assertEqual(report["consoleProblems"], [],
                         "the recovery path must not log an error")
        # The two decisive readings, asserted here as well as in the harness,
        # so the numbers a reviewer needs are in the test that owns the claim.
        for name in ("recovery-focus-is-visible-in-real-chromium",
                     "failed-recovery-focus-is-visible-in-real-chromium"):
            with self.subTest(path=name):
                where = recorded[name]["detail"]["where"]
                self.assertTrue(where["isReading"])
                self.assertTrue(where["matchesFocusVisible"])
                self.assertNotEqual(where["outlineStyle"], "none")
                self.assertGreaterEqual(float(where["outlineWidth"].rstrip("px")), 2.0)
                self.assertEqual(recorded[name]["detail"]["resting"]["outlineStyle"],
                                 "none", "the region must rest without a ring")
                self.assertGreaterEqual(
                    recorded[name]["detail"]["contrast"]["ratio"], 3.0)


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
        # CORRECTED ORACLE (V7). This pinned `[""]` — an EMPTY paragraph where
        # the father's prose belongs — and called it correct because the
        # malformed value had been withheld. The V6 review found the other
        # half: a route that finishes with an empty paragraph has not told the
        # reader anything, and an empty paragraph is what a fragment whose
        # text is genuinely blank would look like too. The page opened a
        # fragment, fetched its payload, could not read it, and said nothing.
        #
        # Nothing OF THE PAYLOAD is still rendered, which was always the
        # requirement; what is added is the page saying so.
        opened = self.snapshot("malformed-record", "opened")
        self.assertEqual(
            opened["fragmentTexts"],
            ["The text of this fragment arrived in a form this page cannot read."],
            "the audit found '[object Object]' as the fragment's words")
        self.assertEqual(opened["fragmentBases"], [],
                         "and 'Extent — [object Object]' and 'Date — 42' beneath them")

    # CORRECTED ORACLES (V6). The two below pinned `["", "", "…"]` — two blank
    # rows standing in the document and counted in the tally — and called it
    # correct because the malformed values were withheld. Withholding the
    # words was never the whole requirement: a row that names nothing is not a
    # thin entry, it is not an entry, and counting it told the reader this
    # project has three leads and three works it cannot name.
    def test_malformed_lead_rows_render_no_words_and_the_sound_row_does(self):
        page = self.page("malformed-record")
        self.assertEqual(page["leads"], ["Origen — Homiliae in Genesim (240)"],
                         "no blank row stands where a record named nothing")
        # And the count is of what the page can state, said in the singular.
        self.assertEqual(
            page["asideNotes"][0],
            "1 unreconciled lead entry on the acquisition record for this "
            "chapter, which omits its confidence. An entry establishes no "
            "distinct work, no possession and nothing renderable, and the "
            "list is not checked against the commentary above.")

    def test_malformed_blocked_rows_name_no_author_and_the_sound_row_does(self):
        page = self.page("malformed-record")
        self.assertEqual(
            page["blocked"],
            ["Anonymous — Catena in Genesimheld only as page images"])
        self.assertEqual(page["tallyText"],
                         "1 fragment held · 1 work held, not renderable yet"
                         " · 1 lead entry on the acquisition list")
        # The announcement is the same clauses in the same order, so the two
        # cannot disagree about how much this project holds.
        self.assertEqual(
            page["statusWrites"],
            ["Genesis 1, Douay-Rheims (Challoner), 1 fragment held, 1 work "
             "held, not renderable yet, 1 lead entry on the acquisition list."])

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

    def test_the_only_focus_rule_defers_to_the_shared_role(self):
        # NARROWED PIN (integration review 2026-08-28). The 2026-08-11 finding
        # was that the route INVENTED a focus appearance of its own, overriding
        # the accepted shared role with a thinner rule; the remedy pinned here
        # was "no focus rule of any kind". That form of the pin was too wide:
        # the shared sheet's `.reading:focus { outline: none }` outranks the
        # universal `:focus-visible`, and this page is the one that moves focus
        # into `#reading`, so deference produced an INVISIBLE indicator on the
        # one target the page focuses itself.
        #
        # So the pin now says what the 2026-08-11 finding actually protects:
        # exactly one focus rule, for that one target, asking for the shared
        # role's own `var(--focus)` and inventing no colour, no width of its
        # own choosing and no second decoration; and nothing keyed on bare
        # `:focus`, so a mouse click on the region stays undecorated.
        rules = re.findall(r"([^{}]*:focus[^{}]*)\{([^{}]*)\}", without_comments(self.css))
        self.assertEqual(len(rules), 1, rules)
        selector, body = rules[0]
        self.assertEqual(selector.strip(), ".catena-page .reading:focus-visible")
        self.assertEqual(body.strip(), "outline: 3px solid var(--focus);")
        self.assertNotIn(":focus-visible", self.block,
                         "print takes no focus rule")
        # Bare `:focus` anywhere would decorate a mouse click as well.
        self.assertEqual(len(re.findall(r":focus(?!-visible)", without_comments(self.css))), 0)

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

    def test_the_shared_refusal_umbrella_stays_neutral(self):
        # V3 review, "Fail-closed presentation": one styled error surface may
        # be reused, but its SHARED copy — reference line, heading, status
        # write — must not diagnose. "address could not be read" was untrue of
        # a value that parsed cleanly and is merely unsupported, and "names
        # what the page does not have" asserted a holdings negative for an
        # address refused on SHAPE. The umbrella states the outcome; only the
        # per-value detail states the reason. A regression re-diagnoses here.
        for name in ("unsupported-voice-greek", "invalid-book"):
            with self.subTest(scenario=name):
                page = self.page(name)
                error = page["errorSections"][0]
                umbrella = " ".join(
                    [error["heading"], page["referenceText"]] + page["statusWrites"])
                for claim in ("could not be read", "not recognised", "invalid",
                              "does not have", "unreadable"):
                    self.assertNotIn(claim, umbrella,
                                     f"{claim!r} diagnoses in shared copy: {umbrella!r}")
                # The reason survives, typed, on the value it belongs to.
                self.assertTrue(any("is not a" in one for one in error["details"]),
                                error["details"])

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

    def test_the_name_joiner_consumes_nothing_it_is_given(self):
        """CORRECTED ORACLE (V7). This pinned a precondition that expired.

        V3 rewrote `joinNames` to `pop()` rather than `slice()` to buy bytes
        in the page, which left a caller's array emptied as a side effect; the
        precondition — every caller hands it a freshly mapped array — was
        pinned here as a source-text scan of `src/web/browser/catena/catena.js`
        because the ceiling left no room to say it in a comment.

        V5 moved the function to `src/web/browser/catena/catena-model.js`,
        which carries no ceiling, and restored the non-mutating form. The
        precondition has not held since, and the assertion went on passing
        because it read the SHAPE of two call sites rather than the property
        they existed to protect. V7 moved both call sites into the model with
        the sentences they compose, and the scan then found nothing to check
        and failed on the count — which is the first time it has said anything
        true about `joinNames` since V5.

        So it asks the real question, of the real function, by running it:
        does it leave its argument alone? The file's own doctrine is that a
        source-text assertion is the fallback for what a replay cannot reach,
        and this is reachable.
        """
        answer = subprocess.run(
            [NODE, "-e",
             "const M = require(process.argv[1]);"
             "const given = ['Latin', 'Greek', 'English'];"
             "const said = M.joinNames(given);"
             "process.stdout.write(JSON.stringify("
             "{said: said, after: given}));",
             str(CATENA / "catena-model.js")],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(0, answer.returncode, answer.stderr)
        answer = json.loads(answer.stdout)
        self.assertEqual(answer["said"], "Latin, Greek and English")
        self.assertEqual(answer["after"], ["Latin", "Greek", "English"],
                         "joinNames consumed the list it was given")

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


class ExactVoiceKeyTest(ReplayTest):
    """The V3 defect, and the distinction it destroyed.

    Support, language existence and chapter availability are three different
    questions. V3 answered the first with the second: `index.held[].languages`
    carries `grc` because Greek stands in this corpus as an ORIGINAL, and from
    that V3 concluded a Greek translation was supported and rendered "Greek
    translation — none here" — a statement about holdings nobody has.
    """

    def test_a_greek_translation_fails_closed(self):
        self.assert_failed_closed(
            "unsupported-voice-greek",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc",
            "voice=translation:grc is not a voice this corpus holds")

    def test_the_greek_refusal_never_claims_a_holding(self):
        # THE PINNED SENTENCE. Neither this wording nor any equivalent absence
        # or holdings claim may appear for a voice the corpus does not have.
        page = self.page("unsupported-voice-greek")
        self.assertNotIn("Greek translation — none here", page["voiceLabels"])
        for label in page["voiceLabels"]:
            self.assertNotIn("Greek", label)
        for note in page["asideNotes"]:
            self.assertNotIn("Greek", note)
        for said in page["statusWrites"]:
            self.assertNotIn("Greek", said)
        self.assertEqual(page["voiceLabels"], ["Everything held"])

    def test_the_second_supported_translation_is_honoured(self):
        # `translation:la` is ONE source entry in the whole corpus. Support is
        # not a synonym for English, and the exact set must carry it.
        page = self.page("voice-latin")
        self.assertEqual(page["voice"], "translation:la")
        self.assertEqual(page["hashWrites"], [])
        self.assertFalse(page["errorSections"])
        self.assertEqual(page["fragmentCount"], 9)

    def test_a_voice_naming_no_language_is_malformed(self):
        self.assert_failed_closed(
            "voice-empty-language",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:",
            "voice=translation: is not a voice")

    def test_a_second_delimiter_is_malformed(self):
        # Malformed by SHAPE, not unsupported by set: the two refusals are
        # different findings and must not collapse into one.
        self.assert_failed_closed(
            "voice-extra-delimiter",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en:extra",
            "voice=translation:en:extra is not a voice")

    def test_the_refusal_does_not_strand_the_reader_s_supported_voice(self):
        # supported -> unsupported -> supported, over a live document.
        greek = self.snapshot("unsupported-greek-change", "greek")
        self.assertEqual(greek["referenceText"], "Address not used")
        self.assertEqual(greek["fragmentCount"], 0)
        self.assertEqual(greek["busy"], "false")
        self.assertNotIn("Greek translation — none here", greek["voiceLabels"])
        back = self.snapshot("unsupported-greek-change", "supported-again")
        self.assertEqual(back["voice"], "translation:en")
        self.assertEqual(back["fragmentCount"], 14)
        self.assertEqual(back["busy"], "false")

    def test_the_published_projection_is_the_exact_key_set(self):
        # The corpus holds four (voice, language) SOURCE PAIRS — original:grc,
        # original:la, translation:en, translation:la — which the route's own
        # `voiceKey` projects onto three keys, because a reader asking for the
        # author's own language asks one question and not one per language.
        index = json.loads(
            (ROOT / "src/web/data/structure/catena/index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["voices"],
                         ["original", "translation:en", "translation:la"])
        self.assertNotIn("translation:grc", index["voices"])
        pairs = set()
        for path in sorted((ROOT / "src/web/data/structure/catena").glob("*/[0-9]*.json")):
            spine = json.loads(path.read_text(encoding="utf-8"))
            for source in (spine.get("sources") or {}).values():
                pairs.add((source.get("voice"), source.get("language")))
        self.assertEqual(pairs, {("original", "grc"), ("original", "la"),
                                 ("translation", "en"), ("translation", "la")})


class TypedStructureBoundaryTest(ReplayTest):
    """The nine sinks the V3 review left open, driven at once.

    One boundary, not nine special cases: unknown or malformed structured data
    must not become visible prose, a filter, a label, a count, or terminal
    state. Every malformed value in the fixture stands beside a sound one,
    because the requirement is not that garbage is withheld — it is that
    withholding garbage costs no valid fact and strands no render.
    """

    def test_the_region_never_stays_busy(self):
        # THE TERMINAL RULE. Non-list `leads`, `blocked` and `refusals` all
        # threw out of the render tail, which stood outside the funnel.
        page = self.page("malformed-structure")
        self.assertEqual(page["busy"], "false")
        self.assertTrue(page["statusWrites"], "the render must still announce")

    def test_malformed_extent_members_state_no_locus(self):
        # Structured members stringified into "Genesis [object Object]:1", and
        # absent ones into "Genesis undefined:undefined". The book alone is
        # true; the structure is left for a renderer that understands it.
        page = self.page("malformed-structure")
        self.assertEqual(page["extents"],
                         ["Genesis 1:1", "Genesis", "Genesis", "Genesis"])

    def test_no_boundary_crossing_is_claimed_from_a_malformed_extent(self):
        self.assertEqual(self.page("malformed-structure")["spans"], [])

    def test_a_scalar_translator_container_attributes_nobody(self):
        # A string is not a one-item list. "Not A List" was printed as
        # "tr. Not A List" — an attribution of translation nobody recorded.
        page = self.page("malformed-structure")
        for line in page["sourceLines"]:
            self.assertNotIn("Not A List", line)
        self.assertTrue(any("tr. Sound Hand" in one for one in page["sourceLines"]),
                        "the sound translator list must survive beside it")

    def test_a_malformed_language_never_becomes_a_voice_or_a_url(self):
        # It composed `translation:[object Object]` — a select value the page
        # wrote into history and then refused on the way back in.
        page = self.page("malformed-structure")
        self.assertEqual(page["voiceLabels"], ["Everything held", "English translation"])
        for written in page["hashWrites"]:
            self.assertNotIn("object", written)

    def test_unnamed_authors_get_no_shared_filter_key(self):
        # Two unnamed authors are not one man, and `hiddenAuthors` persists
        # across chapters, so a key of '' switched off every author-less
        # fragment in the corpus and force-opened a filter elsewhere.
        page = self.page("malformed-structure")
        self.assertEqual(page["filterLabels"], ["Sound Author", "Scalar Author"])
        for label in page["filterLabels"]:
            self.assertTrue(label.strip(), "a toggle with no name has no accessible name")

    def test_valid_siblings_survive_every_malformed_neighbour(self):
        page = self.page("malformed-structure")
        self.assertEqual(page["authors"], ["Sound Author", "Scalar Author", "", ""])
        # The unnameable authors still carry their WORKS: coupling the two
        # fields lost a held work's title whenever its author was missing.
        self.assertEqual(page["works"], ["Sound Work", "Scalar Work",
                                         "Nameless Work One", "Nameless Work Two"])

    def test_absence_counts_and_words_are_one_typed_value(self):
        # THE SHARPEST CASE. Untyped, the truthiness of `partial` moved a work
        # out of "no publishable translation" and into "only a partly public
        # domain one, not yet taken" — a different claim about somebody's
        # rights, made by an object, a number, a boolean and a blank string.
        page = self.page("malformed-structure")
        self.assertEqual(page["absenceReasons"], ["A sound recorded reason."])
        self.assertEqual(page["absencePartials"],
                         ["Partly public domain — a sound partial offer"])
        self.assertIn("1 has only a partly public domain", page["absenceSummary"])

    def test_containers_that_are_not_lists_count_nothing(self):
        # A string satisfied `.length`, so the tally counted characters as
        # works held and the refusal claimed a boundary nobody established.
        page = self.page("malformed-structure")
        self.assertEqual(page["leads"], [])
        self.assertEqual(page["blocked"], [])
        for said in page["statusWrites"]:
            self.assertNotIn("not renderable yet", said)
            self.assertNotIn("lead entr", said)

    def test_nothing_malformed_reaches_the_page_as_words(self):
        # The sweep reads only what the page SAYS — the text-bearing
        # projections — so a boolean in the harness's own report cannot be
        # mistaken for a boolean coerced into prose.
        page = self.page("malformed-structure")
        said = []
        for key in ("authors", "works", "dates", "extents", "spans", "languages",
                    "voiceLabels", "filterLabels", "absenceReasons",
                    "absencePartials", "sectionHeadings", "asideNotes", "leads",
                    "blocked", "sourceLines", "acknowledgements", "states",
                    "statusWrites", "hashWrites"):
            said.extend(page.get(key) or [])
        said.append(page.get("absenceSummary") or "")
        rendered = " ¶ ".join(str(one) for one in said)
        for token in ("[object Object]", "[OBJECT OBJECT]", "undefined", "null",
                      "not text", "NaN", "true", "false"):
            self.assertNotIn(token, rendered, f"{token!r} reached the page")


class MalformedLanguageAttributeTest(ReplayTest):
    """V5 §5 — a language that is not a language reaches no DOM attribute.

    The V4.1 review replayed an Everything-held page in real Chromium 151 and
    read `lang="[object Object]"` off the fragment text while the page
    otherwise completed normally. Nothing here could see it: the committed
    malformed-language scenario filtered the offending fragment out under a
    translation selection, and the harness stored `element.lang` as a plain
    JavaScript property rather than reflecting it into the content attribute
    the way the HTML DOM does. Both halves are corrected — the shim reflects,
    and these scenarios hold everything.
    """

    def test_no_language_attribute_is_ever_a_coerced_value(self):
        for name in ("malformed-language-held", "malformed-bible-language"):
            page = self.page(name)
            for written in page["langAttributes"]:
                for artefact in ("[object Object]", "undefined", "null", "true",
                                 "42", "NaN", "not a language code"):
                    self.assertNotIn(artefact, written, f"{name}: {written}")

    def test_every_language_attribute_is_a_language_subtag(self):
        # Not merely "not an object": the attribute is machine-read, so the
        # value has to be a code a consumer can act on.
        page = self.page("malformed-language-held")
        self.assertTrue(page["langAttributes"], "the page must write some lang")
        for written in page["langAttributes"]:
            code = written.split("=", 1)[1]
            self.assertRegex(code, r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$", written)

    def test_the_sound_language_survives_its_malformed_neighbours(self):
        # Nine fragments stand; exactly one states a language, and it keeps it.
        #
        # CORRECTED ORACLE (V6). V5 pinned `["fragment-text=la"] +
        # ["fragment-text=en"] * 8` and called it survival. Eight of those
        # nine records intend LATIN and state a language nobody can read; the
        # page answered each with `en`, so a screen reader was told to read
        # Latin commentary in an English voice on the authority of `|| 'en'`.
        # A guessed fact is not a smaller defect than a coerced one, and the
        # requirement is to OMIT the claim, not to substitute a default.
        page = self.page("malformed-language-held")
        self.assertEqual(page["fragmentCount"], 9)
        self.assertEqual(
            [one for one in page["langAttributes"] if one.startswith("fragment-text=")],
            ["fragment-text=la"],
            "the eight unreadable languages must carry no lang at all")

    def test_a_malformed_language_reaches_no_visible_prose(self):
        # `sound()` passed "not a language code", and the shared namer printed
        # it straight back, uppercased, as though it named a language.
        page = self.page("malformed-language-held")
        self.assertEqual(page["languages"], ["Latin — the author\u2019s own"])

    def test_a_malformed_bible_language_reaches_no_passage_attribute(self):
        # CORRECTED ORACLE (V6). V5 required the passage element to carry
        # `lang="en"` for a Bible whose language is `{"code": "en"}` — which
        # is to require the page to READ the malformed value and act on what
        # it guessed it meant. The edition states no language this page can
        # use, so the passage makes no language claim, and the option names
        # the edition without one.
        page = self.page("malformed-bible-language")
        self.assertEqual(
            [one for one in page["langAttributes"] if one.startswith("passage=")], [],
            "an edition that states no readable language claims none")
        self.assertEqual(page["bibleLabels"], ["Douay-Rheims"],
                         "and the option is the label alone, not `(...)`")

    def test_the_page_still_completes_under_every_malformed_language(self):
        for name in ("malformed-language-held", "malformed-bible-language"):
            page = self.page(name)
            self.assertEqual(page["busy"], "false", name)
            self.assertTrue(page["statusWrites"], name)
            self.assertFalse(page["errorSections"], name)


class TypedAbsenceFindingTest(ReplayTest):
    """V5 §7 — an absence claims exactly what its typed finding supports.

    The generator closes `finding` at four values and says a different thing
    with each: `none-published` is about the world, `in-copyright` about the
    law, `partial-public-domain` is an offer not taken, and `not-surveyed` is
    an admission that nobody looked. The page read none of them, classifying a
    row by whether a `partial` string was attached — so `not-surveyed`, and
    every malformed neighbour, was spoken as "no English this project may
    publish".
    """

    def test_each_finding_speaks_only_for_itself(self):
        page = self.page("typed-absence")
        self.assertEqual(
            page["absenceSummary"],
            "2 works standing here have no English this project may publish;"
            " 1 has only a partly public domain English, not yet taken;"
            " 1 has not been surveyed for English;"
            " 1 has a finding this page cannot read")

    def test_not_surveyed_never_becomes_a_publishing_negative(self):
        page = self.page("typed-absence")
        said = page["absenceSummary"]
        # One closed clause, counting two works, and `not-surveyed` is not
        # one of them: four rows would have been counted before V5.
        self.assertIn("2 works standing here have no English", said)
        self.assertIn("1 has not been surveyed for English", said)

    def test_a_malformed_finding_supports_no_claim_and_no_count(self):
        page = self.page("typed-absence")
        self.assertIn("1 has a finding this page cannot read", page["absenceSummary"])

    def test_a_valid_finding_survives_malformed_sibling_metadata(self):
        # `typed.work3` states `in-copyright` beside an unreadable reason; the
        # finding is counted and the reason withheld, not the other way about.
        # That half is V6's and is unchanged: a fact about the law survives a
        # malformed neighbour.
        #
        # CORRECTED ORACLE (V7). The middle entry was `typed.work2`'s reason —
        # "A reason that outlives its finding." — a sound sentence standing
        # beside a finding that is a RECORD, so the page could read no finding
        # for that row at all. V6 printed it anyway, under a summary saying
        # this work has a finding the page cannot read.
        #
        # The V6 review named that as a leak: a reason is a rights statement
        # about somebody's text, and what licenses it is the finding it
        # belongs to. Where no finding could be read, nothing licenses the
        # prose, and the row says only what it can support — this work stands
        # here, and its finding could not be read. The reason genuinely does
        # not outlive its finding, which is what the fixture's own name for it
        # was asserting the other way about.
        page = self.page("typed-absence")
        self.assertEqual(
            page["absenceReasons"],
            ["No English translation has been published.",
             "Only part of it is out of copyright."])
        self.assertNotIn("A reason that outlives its finding.",
                         page["absenceReasons"])
        # The row itself is not deleted: five works stand, and work2 among them.
        self.assertEqual(len(page["absenceAuthors"]), 5)

    def test_a_malformed_member_does_not_stand_in_for_the_valid_one(self):
        page = self.page("typed-absence")
        self.assertEqual(page["absencePartials"],
                         ["Partly public domain \u2014 the 1893 selection"])

    def test_the_absence_view_completes_and_stands_open(self):
        page = self.page("typed-absence")
        self.assertTrue(page["absenceOpen"])
        self.assertEqual(page["busy"], "false")
        self.assertIn("absence", page["dataStates"])


class NumericVerseAndPathTest(ReplayTest):
    """V5 §8 — numbers, verses, paths and the bootstrap record."""

    def test_only_plainly_numbered_verses_with_readable_words_are_shown(self):
        page = self.page("malformed-verses")
        self.assertEqual(page["chapterCounts"][0], "2 verses")

    def test_no_verse_value_is_coerced_into_scripture(self):
        # CORRECTED ORACLE (V6). This read `fragmentTexts` — the COMMENTARY —
        # while the fixture it defends corrupts the bible chapter, so it
        # inspected a sink the defect could not reach and would have passed
        # with `[object Object]` standing in Scripture. It now reads the
        # rendered verses; `RenderedScriptureTruthTest` carries the sweep
        # across every chapter fixture.
        page = self.page("malformed-verses")
        rendered = " ".join(str(one) for one in page["verseTexts"])
        for artefact in ("[object Object]", "also,not text", "undefined", "null"):
            self.assertNotIn(artefact, rendered)

    def test_a_mark_that_is_not_a_mark_opens_no_paragraph(self):
        # Any truthy value opened a paragraph and counted as neither kind, so
        # the page printed paragraphs and denied holding any division. The
        # first half of that is V5's correction and is unchanged.
        #
        # CORRECTED ORACLE (V7). The second half — the note then saying none
        # is held — is the manufactured negative the V6 review named for this
        # exact record ("a malformed paragraph root can render `No paragraph
        # division held`"). `MALFORMED_BREAKS` STATES a division at verses 1,
        # 3 and 9; the page cannot read any of the three, and denying that the
        # edition divides the chapter is a claim about how it sets its text
        # drawn from a record nobody could read.
        page = self.page("malformed-verses")
        self.assertEqual(page["paragraphs"], 1)
        self.assertNotIn("No paragraph division is held", page["paragraphNote"])
        self.assertIn("could not be read", page["paragraphNote"])

    def test_unreadable_verses_are_not_reported_as_none(self):
        # "carries no verses" is a claim about the edition, and a parse
        # failure does not establish it.
        page = self.page("unreadable-verses")
        rendered = " ".join(page["asideNotes"] + page["sectionHeadings"])
        self.assertEqual(page["busy"], "false")
        self.assertNotIn("carries no verses", str(page["classes"]) + rendered)

    def test_a_word_tally_is_a_number_the_record_wrote(self):
        # Seven fragments, and exactly one states a tally this page may print.
        #
        # CORRECTED ORACLE (V6). This counted `page["classes"]`, which the
        # harness builds as `[...new Set(...)]` — a deduplicated set of class
        # names. One chip and seven chips both reduce to
        # `["fragment-length"]`, so the assertion could not fail on the defect
        # it was written for: reverting the gate to `Number(x) > 0` renders
        # `1 words` for a boolean and `12.5 words` for a fraction and this
        # test still passed. It now reads the chips themselves.
        page = self.page("malformed-numbers")
        self.assertEqual(page["fragmentCount"], 7)
        self.assertEqual(page["lengths"], ["1,200 words"])

    def test_a_malformed_held_path_is_never_requested(self):
        page = self.page("malformed-held-path")
        for asked in page["fetched"]:
            self.assertNotIn("object", asked)
        self.assertEqual(page["busy"], "false")

    def test_a_malformed_held_record_reports_a_fault_not_an_emptiness(self):
        page = self.page("malformed-held-path")
        self.assertTrue(page["errorSections"], "a broken record is an error")
        self.assertNotIn("Nothing held here", str(page["tallyText"]))

    def test_an_unreadable_present_list_proves_no_absence(self):
        page = self.page("unreadable-present")
        self.assertNotEqual(page["tallyText"], "Nothing held here")
        self.assertTrue(page["errorSections"])
        self.assertEqual(page["busy"], "false")

    def test_a_malformed_canon_never_leaves_the_page_loading(self):
        # THE BOOTSTRAP BLOCKER. This threw between the last fetch and the
        # first render, outside both funnels, and the page stood at "Loading…"
        # with every control disabled and nothing said.
        for name in ("malformed-canon", "scalar-index"):
            page = self.page(name)
            self.assertNotEqual(page["referenceText"], "Loading\u2026", name)
            self.assertTrue(page["statusWrites"], f"{name}: the failure must be spoken")
            self.assertNotIn("Loading", " ".join(page["bookLabels"]), name)


class RouteCompletionAfterMalformedDataTest(ReplayTest):
    """V5 §9 — the application completes its state machine, not merely a parse.

    Every committed malformed scenario began malformed, so none of them proved
    anything about a page that had already established a route, a history and
    a rendered chapter before the malformed data arrived. These begin
    canonical.
    """

    def test_a_reader_action_into_a_malformed_chapter_pushes_exactly_once(self):
        moved = self.snapshot("arrival-then-malformed-member", "moved")
        self.assertEqual(moved["hash"], GEN2)
        self.assertEqual(moved["hashWrites"], [GEN2],
                         "a reader step pushes one entry, malformed data or not")
        self.assertEqual(moved["replaced"], [])
        self.assertEqual(moved["busy"], "false")

    def test_an_address_into_a_malformed_chapter_never_pushes(self):
        moved = self.snapshot("hash-then-malformed-member", "moved")
        self.assertEqual(moved["hash"], GEN2)
        self.assertEqual(moved["hashWrites"], [],
                         "an arrival is completed in place, never by pushing")
        self.assertEqual(moved["busy"], "false")

    def test_the_route_state_stays_coherent_across_the_malformed_chapter(self):
        for name in ("arrival-then-malformed-member", "hash-then-malformed-member"):
            moved = self.snapshot(name, "moved")
            self.assertEqual(moved["referenceText"], "Genesis 2", name)
            self.assertEqual(moved["selectValues"],
                             {"book": "Gen", "chapter": "2", "bible": "douay-rheims"},
                             name)
            self.assertEqual(moved["stepButtons"], [False, False], name)

    def test_the_valid_siblings_and_the_tally_survive_the_move(self):
        for name in ("arrival-then-malformed-member", "hash-then-malformed-member"):
            moved = self.snapshot(name, "moved")
            self.assertEqual(moved["fragmentCount"], 3, name)
            self.assertIn("3 fragments held", moved["tallyText"], name)

    def test_the_move_announces_itself_exactly_once_more(self):
        # The whole announcement journal, in order: the cold arrival speaks
        # once and the move speaks once. Neither doubles, and neither is lost
        # because the chapter it moved into is malformed.
        moved = self.snapshot("arrival-then-malformed-member", "moved")["statusWrites"]
        self.assertEqual(len(moved), 2, moved)
        self.assertTrue(moved[0].startswith("Genesis 1, "), moved[0])
        self.assertTrue(moved[1].startswith("Genesis 2, "), moved[1])

    def test_a_partial_arrival_completes_when_the_malformed_spine_lands(self):
        pending = self.snapshot("partial-arrival-malformed", "pending")
        self.assertEqual(pending["busy"], "true",
                         "the region is busy while the spine is in flight")
        self.assertEqual(pending["statusWrites"], [],
                         "nothing is announced before the record arrives")
        arrived = self.snapshot("partial-arrival-malformed", "arrived")
        self.assertEqual(arrived["busy"], "false")
        self.assertEqual(arrived["hash"], GEN1)
        self.assertEqual(arrived["hashWrites"], [],
                         "a partial arrival is completed in place")
        self.assertEqual(arrived["fragmentCount"], 3)
        self.assertTrue(arrived["statusWrites"])

    def test_a_partial_arrival_keeps_its_valid_siblings_and_claims_nothing(self):
        arrived = self.snapshot("partial-arrival-malformed", "arrived")
        self.assertNotEqual(arrived["tallyText"], "Nothing held here")
        # The one valid refusal record among three malformed members survives
        # the partial arrival and is stated once.
        self.assertIn("Boundary not established", arrived["refusal"])
        self.assertNotIn("absence", arrived["dataStates"])

    def test_a_malformed_action_payload_settles_its_own_fragment_only(self):
        arrived = self.snapshot("malformed-action-then-retry", "malformed-arrived")
        # The payload's body is unreadable, so the fragment shows nothing of
        # itself — and says so rather than standing at "Loading…" for ever.
        self.assertNotIn("Loading\u2026", arrived["fragmentTexts"][0])
        self.assertEqual(arrived["fragmentBases"], [],
                         "an unreadable basis renders nothing")

    def test_a_malformed_action_touches_neither_route_nor_history(self):
        opened = self.snapshot("malformed-action-then-retry", "opened")
        arrived = self.snapshot("malformed-action-then-retry", "malformed-arrived")
        for page in (opened, arrived):
            self.assertEqual(page["hash"], GEN1)
            self.assertEqual(page["hashWrites"], [])
            self.assertEqual(page["busy"], "false",
                             "opening a fragment does not make the region busy")

    def test_a_later_valid_action_still_completes_after_a_malformed_one(self):
        moved = self.snapshot("malformed-action-then-retry", "moved-after")
        self.assertEqual(moved["hash"], GEN2)
        self.assertEqual(moved["hashWrites"], [GEN2])
        self.assertEqual(moved["busy"], "false")
        self.assertEqual(moved["referenceText"], "Genesis 2")

    def test_nothing_stale_survives_the_rejected_payload(self):
        moved = self.snapshot("malformed-action-then-retry", "moved-after")
        self.assertFalse(moved["errorSections"])
        for said in moved["fragmentTexts"]:
            self.assertNotIn("[object Object]", said)


class EmptyRefusalRecordTest(ReplayTest):
    """V6 §6 — a record that states nothing refuses nothing.

    "Boundary not established" is a claim about Scripture's own verse division
    in a published edition: that this project knows the numbering moves here
    and will not guess where to. `{}` satisfied the record shape and made that
    claim. So did `{"note": "   "}` and `{"kind": "displaced"}` — a kind with
    no chapter, no verse and no note states nothing a reader can act on. The
    shape gate is not the content gate, and the count of refusals must be the
    count of records that actually refuse something.
    """

    def test_records_that_state_nothing_manufacture_no_refusal(self):
        page = self.page("empty-refusal-records")
        self.assertIsNone(page["refusal"])
        # Counted, not asserted by a substring: three empty records that each
        # rendered an empty refusal node would satisfy `assertIsNone` on the
        # first node's text and still stand in the document three times.
        self.assertEqual(page["refusalCount"], 0)
        self.assertNotIn("refusal", page["dataStates"])

    def test_no_refusal_prose_reaches_the_page_from_an_empty_record(self):
        # The sentence is assembled from the edition's own name and the
        # chapter's, so a half-built refusal would carry none of the fixture's
        # words. The sweep reads the whole rendered state for the claim itself.
        rendered = json.dumps(
            self.rendered_state(self.page("empty-refusal-records")),
            ensure_ascii=False)
        for claim in ("Boundary not established", "not established", "displaced",
                      "numbering"):
            self.assertNotIn(claim, rendered,
                             f"{claim!r} was manufactured from a record that "
                             "states nothing")

    def test_the_rest_of_the_chapter_is_untouched_by_the_empty_records(self):
        # Refusing to manufacture a refusal must cost nothing else. The fixture
        # is `mixed-reordered` with only its refusal list replaced, so every
        # other projection must match that page exactly.
        page = self.page("empty-refusal-records")
        moved = self.page("mixed-reordered")
        for key in ("fragmentCount", "fragmentIds", "authors", "works",
                    "extents", "leads", "blocked", "tallyText",
                    "sectionHeadings", "asideNotes", "statusWrites",
                    "referenceText", "fetched"):
            with self.subTest(projection=key):
                self.assertEqual(page[key], moved[key])
        self.assertEqual(
            page["tallyText"],
            "3 fragments held · 2 works held, not renderable yet"
            " · 2 lead entries on the acquisition list")
        self.assertEqual(
            page["statusWrites"],
            ["Genesis 1, Douay-Rheims (Challoner), 3 fragments held, 2 works "
             "held, not renderable yet, 2 lead entries on the acquisition list."])
        # `dataStates` is a deduplicated SET and cannot count anything; it is
        # read here only for the presence question the class turns on, and the
        # count is `refusalCount` above.
        self.assertEqual(page["dataStates"], ["blocked", "held", "lead"])

    def test_the_page_terminates_with_every_refusal_record_rejected(self):
        page = self.page("empty-refusal-records")
        self.assertEqual(page["busy"], "false")
        self.assertTrue(page["statusWrites"])
        self.assertEqual(page["errorSections"], [])


class NeutralRefusalUmbrellaTest(ReplayTest):
    """V6 §16 — the shared fail-closed copy still states the outcome only.

    Three strings carry every refused address: the reference line, the error
    heading, and the one status write. They are shared by every reason an
    address can be refused, so each has to be true of all of them — the
    diagnosis belongs to the per-value detail, which names the one value and
    what it is not. This class pins the three verbatim and then proves the
    collection-member work in §6 did not reach them: normalizing a member is
    not refusing an address, and a malformed object member must never be
    presented as a typed refusal of any kind.
    """

    #: Every scenario in the §6 collection-member and index-sibling lane.
    _COLLECTION_SCENARIOS = (
        "mixed-collection", "mixed-no-refusal", "mixed-reordered",
        "empty-refusal-records", "held-malformed-first", "held-malformed-last",
        "malformed-record",
    )

    def test_the_three_umbrella_strings_are_verbatim(self):
        page = self.page("invalid-book")
        self.assertEqual(page["referenceText"], "Address not used")
        self.assertEqual(page["errorSections"][0]["heading"],
                         "This address cannot be used as written")
        self.assertEqual(
            page["statusWrites"],
            ["The address is unchanged; the values not used are listed."],
            "one write, and it neither diagnoses nor names a holding")
        # The reason is not lost — it stands, typed, on the value it is about.
        self.assertEqual(page["errorSections"][0]["details"],
                         ["book=Foo is not a book of this canon."])

    def test_no_collection_member_scenario_reaches_the_umbrella(self):
        # A member the page cannot read is a member it drops; it is not an
        # address the reader wrote wrongly. If a normalization failure ever
        # falls through to the fail-closed surface, the reader is told their
        # own URL is at fault for a defect in the data.
        for name in self._COLLECTION_SCENARIOS:
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["errorSections"], [])
                self.assertEqual(page["referenceText"], "Genesis 1")
                rendered = json.dumps(self.rendered_state(page), ensure_ascii=False)
                said = rendered + " ¶ " + " ¶ ".join(page["statusWrites"])
                for umbrella in ("Address not used",
                                 "This address cannot be used as written",
                                 "The address is unchanged; the values not used"
                                 " are listed."):
                    self.assertNotIn(umbrella, said,
                                     f"{name} reached the fail-closed umbrella")

    def test_a_malformed_object_member_never_reaches_typed_refusal_presentation(self):
        # `{"note": {"broken": true}}`, `{}`, `{"kind": "displaced"}` and a
        # bare `"not a record"` all satisfy some part of the refusal record's
        # shape. None of them refuses anything, so none may be presented as a
        # refusal — neither as the typed sentence nor as an empty node wearing
        # the refusal state.
        for name in ("mixed-no-refusal", "empty-refusal-records"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertIsNone(page["refusal"])
                self.assertEqual(page["refusalCount"], 0)
                self.assertNotIn("refusal", page["dataStates"])
                rendered = json.dumps(self.rendered_state(page), ensure_ascii=False)
                self.assertNotIn("Boundary not established", rendered)


class CanonicalVerseIdentityTest(ReplayTest):
    """V6 §9 — one verse is one verse, whatever way its number is written.

    `^[0-9]+$` admitted `"01"`, `"001"` and `"0002"` beside `"1"` and `"2"`,
    and `Number()` folded each padded key onto the verse it padded. So a
    chapter carrying two encodings of one verse rendered that verse TWICE, in
    two paragraphs, each `sup.verse-num` claiming to be the verse the edition
    numbers 1 — and a padded key with no canonical sibling invented a verse
    the chapter never wrote. Nothing in V5 could see any of it: the verse
    oracle read `fragmentTexts`, which is the COMMENTARY, so the rendered
    Scripture was never asserted about at all. These read `.verse-num` and
    `.verse` — the production sink — as exact lists.
    """

    # The padded keys of V6_PADDED_VERSES, by the TEXT each would print if it
    # were admitted. Asserting on the text and not the key is deliberate: the
    # defect was a duplicate verse 1, and a duplicate is invisible to any
    # oracle that only looks at how many distinct numbers appeared.
    PADDED_TEXT = (
        "A padded encoding of verse one.",
        "A twice-padded encoding of verse one.",
        "A padded encoding of verse two.",
        "A padded verse three, with no canonical sibling.",
    )

    # Every verse identity of V6_UNSAFE_VERSES that numbers no verse of this
    # chapter, by the text standing against it.
    UNSAFE_TEXT = (
        "Verse zero.",
        "A negative verse.",
        "A fractional verse.",
        "An exponent.",
        "A verse with whitespace in its number.",
        "A verse with no number at all.",
        "A verse whose number is a path.",
        "A verse whose number is a flag.",
    )

    def test_one_verse_written_two_ways_is_numbered_once(self):
        # THE DEFECT, PINNED EXACTLY. Two verses arrived under six keys; two
        # verse numbers and two verse bodies may render. An exact list is the
        # only oracle that catches this — a set, a count of distinct numbers,
        # or a substring search would all have passed on the duplicate.
        page = self.page("padded-verses")
        self.assertEqual(page["verseNumbers"], ["1", "2"])
        self.assertEqual(page["verseTexts"],
                         ["1The first verse, sound. ",
                          "2The second verse, sound. "])

    def test_no_padded_encoding_reaches_the_reader_as_scripture(self):
        # A noncanonical key is a malformed key: not a second verse, and not a
        # silent overwrite of the first. So the canonical text stands and the
        # padded text is printed nowhere.
        page = self.page("padded-verses")
        rendered = " ¶ ".join(page["verseTexts"])
        for said in self.PADDED_TEXT:
            self.assertNotIn(said, rendered, f"{said!r} was rendered as Scripture")

    def test_a_padded_key_with_no_sibling_invents_no_verse(self):
        # `"03"` folds onto nothing. It is not verse 3 arriving under an
        # unusual name; the chapter never numbered a verse 3, and refusing the
        # key must neither add a third verse nor renumber the two sound ones.
        page = self.page("padded-verses")
        self.assertNotIn("3", page["verseNumbers"])
        self.assertEqual(page["chapterCounts"], ["2 verses"])

    def test_only_canonically_numbered_verses_are_shown(self):
        # `"0"`, `"-2"`, `"1.5"`, `"1e3"`, `" 4 "`, `""`, `"../5"` and `"true"`
        # are sound text and no verse identity of this corpus. One sound key
        # stands with them, and it must survive their refusal intact.
        page = self.page("unsafe-verses")
        self.assertEqual(page["verseNumbers"], ["1"])
        self.assertEqual(page["verseTexts"],
                         ["1The only verse this chapter numbers. "])
        self.assertEqual(page["chapterCounts"], ["1 verse"])

    def test_no_refused_verse_identity_renders_its_text(self):
        # Refusing the KEY must also withhold the value: a verse the chapter
        # never numbered may not appear unnumbered, or under a neighbour's
        # number, or appended to a sound verse's words.
        page = self.page("unsafe-verses")
        rendered = " ¶ ".join(page["verseTexts"])
        for said in self.UNSAFE_TEXT:
            self.assertNotIn(said, rendered, f"{said!r} was rendered as Scripture")


class RenderedScriptureTruthTest(ReplayTest):
    """V6 §10 — the oracles read the sink the reader reads.

    The V5 verse-coercion oracle swept `fragmentTexts` and `tallyText` while
    the fixture it defended corrupted the bible chapter, so it proved nothing
    about rendered Scripture; and the verse count was checked as a chip string
    with no reference to the verses that actually rendered beneath it, so a
    chip and its chapter could disagree freely. These assert `.verse`,
    `.verse-num` and the chip together, across every chapter fixture in the
    package and the real corpus beside them.
    """

    # Every scenario that renders a chapter under a verse-count chip.
    NUMBERED = ("padded-verses", "unsafe-verses", "malformed-verses", "default")

    # Every scenario whose bible chapter is adversarial, plus the one whose
    # verses all arrived unreadable.
    SWEPT = ("malformed-verses", "unsafe-verses", "padded-verses",
             "unreadable-verses")

    def test_the_verse_chip_counts_the_verses_that_rendered(self):
        # The chip is a claim ABOUT the passage below it. Deriving the expected
        # string from `len(verseNumbers)` means neither side can drift: a
        # doubled verse 1 would have moved the count and the chip together
        # only if the code that wrote them agreed, which is the point.
        for name in self.NUMBERED:
            page = self.page(name)
            shown = len(page["verseNumbers"])
            self.assertEqual(shown, len(page["verseTexts"]), name)
            self.assertEqual(
                page["chapterCounts"][0],
                f"{shown} verse" + ("" if shown == 1 else "s"), name)

    def test_no_value_is_coerced_into_rendered_scripture(self):
        # THE SWEEP, MOVED ONTO THE REAL SINK. `{"text": "not text"}`,
        # `["also", "not text"]`, `None`, `6` and a whitespace string all stood
        # under canonical keys, and concatenation would have printed each of
        # them as the words of a verse of Genesis.
        for name in self.SWEPT:
            page = self.page(name)
            rendered = " ¶ ".join(
                str(one) for one in page["verseTexts"] + page["verseNumbers"])
            for token in ("[object Object]", "also,not text", "undefined",
                          "null", "true", "NaN"):
                self.assertNotIn(token, rendered, f"{name}: {token!r} is not Scripture")

    def test_unreadable_verses_render_no_scripture_and_claim_no_chapter(self):
        # Verses DID arrive and none could be read. Nothing may be printed as
        # Scripture, and no verse-count chip may stand over an empty passage.
        page = self.page("unreadable-verses")
        self.assertEqual(page["verseTexts"], [])
        self.assertEqual(page["verseNumbers"], [])
        self.assertEqual(page["chapterCounts"], [])

    def test_a_mark_that_is_not_a_mark_opens_no_paragraph(self):
        # MALFORMED_BREAKS holds `"guessed"`, `{"kind": "printed"}` and `1`.
        # Any truthy value used to open a paragraph while counting as neither
        # kind, so the page printed paragraphs and, beneath them, the note
        # denying it holds any division. Asserted against all three sinks — the
        # paragraphs rendered, the projected marks drawn, and the exact words
        # of the note — because the contradiction lived between them.
        #
        # CORRECTED ORACLE (V7). The three sinks are still read together and
        # the first two are unchanged. The third is not: the record STATES a
        # division at three verses and states it in three ways this page
        # cannot read, so "no paragraph division is held" denies something the
        # record asserted. The contradiction the V5 note lived between is
        # replaced by the sentence that covers both halves — the chapter runs
        # on unmarked because nothing readable marked it, and whether the
        # edition divides it is not established here.
        page = self.page("malformed-verses")
        self.assertEqual(page["paragraphs"], 1, "one unmarked paragraph runs on")
        self.assertEqual(page["projected"], 0)
        self.assertEqual(
            page["paragraphNote"],
            "The paragraph record for this chapter in this edition could not "
            "be read, so whether it divides the chapter is not established "
            "here.")

    def test_every_chapter_page_terminates_and_announces(self):
        # THE TERMINAL RULE, for each fixture this lane drives. Refusing a
        # verse identity, a verse value or a mark must cost no render.
        for name in self.SWEPT + ("malformed-numbers", "default"):
            page = self.page(name)
            self.assertEqual(page["busy"], "false", name)
            self.assertTrue(page["statusWrites"], f"{name}: the render must announce")


class UnregressedScriptureTest(ReplayTest):
    """V6 §9/§10 — the canonical grammar refuses nothing the corpus holds.

    The positive control, and the guard against over-tightening. A verse-key
    rule strict enough to refuse `"01"` must still admit every key the real
    chapter writes, and a tally rule strict enough to refuse `True` must still
    print every tally the real records state.
    """

    def test_the_real_chapter_numbers_every_verse_it_holds(self):
        # Genesis 1, in full and in order, with no verse lost to the canonical
        # key test and none doubled.
        page = self.page("default")
        self.assertEqual(page["verseNumbers"], [str(n) for n in range(1, 32)])
        self.assertEqual(len(page["verseTexts"]), 31)
        self.assertEqual(page["verseTexts"][0], "1Verse 1 of the stub chapter. ")
        self.assertEqual(page["verseTexts"][30], "31Verse 31 of the stub chapter. ")

    def test_the_real_chapter_states_its_own_counts(self):
        self.assertEqual(self.page("default")["chapterCounts"],
                         ["31 verses", "8 paragraphs"])

    def test_every_real_fragment_still_prints_its_tally(self):
        # 107 fragments, 107 chips — asserted as a count of the chips
        # THEMSELVES, which the deduplicated projection could never express.
        page = self.page("default")
        self.assertEqual(page["fragmentCount"], 107)
        self.assertEqual(len(page["lengths"]), page["fragmentCount"])


class FindingOrderIndependenceTest(ReplayTest):
    """V6 §7 — one finding set says one thing, however it is listed.

    Selection was FIRST-MATCH. An unreadable same-language record standing
    before a valid one erased the finding behind it, and the very same two
    records in the other order kept it — so what this page said about a work's
    rights was a property of where the generator happened to write a record,
    not of what the record states. `finding-order` and `finding-order-reversed`
    carry the identical five works and the identical records per work, listed
    in opposite orders, and exist to be read against each other.

    Two claims are pinned together here, and neither alone is enough: the two
    pages must AGREE, and they must agree on the ONE sentence the records
    license. Agreement alone would survive a change that broke both orders in
    the same way; the exact sentence alone would not see the flip.
    """

    # The one sentence, clause by clause. The five works stand in the spine's
    # order, `typed.work1` .. `typed.work5`, and each contributes exactly one
    # row:
    #
    #   work1  none-published + malformed      -> closed      \  "2 works ...
    #   work5  unknown + none-published        -> closed      /   may publish"
    #   work2  partial-public-domain + malformed -> untaken   ->  "1 has only
    #                                                              a partly ..."
    #   work3  not-surveyed + malformed        -> unsurveyed  ->  "1 has not
    #                                                              been surveyed"
    #   work4  none-published + partial-public-domain (BOTH valid, and
    #          different) -> the record contradicts itself, the page declines
    #          -> ''                                          ->  "1 has a
    #                                                              finding this
    #                                                              page cannot
    #                                                              read"
    #
    # A class no row stands on gets no clause; `in-copyright` never appears
    # here, so there is no fifth clause and no zero anywhere in the sentence.
    SUMMARY = (
        "2 works standing here have no English this project may publish;"
        " 1 has only a partly public domain English, not yet taken;"
        " 1 has not been surveyed for English;"
        " 1 has a finding this page cannot read")

    # CORRECTED ORACLE (V7). `absenceReasons` is one entry per row THAT STATES
    # A REASON THE PAGE MAY REPEAT, in row order: work1, work2, work5. `work3`
    # states no reason at all.
    #
    # V6 listed FOUR, and the fourth was work4's — the contradictory pair. The
    # V6 review found that the page, having just declined to state work4's
    # finding, went on to print one of the two contradicting records' `reason`
    # underneath the declining, chosen by ranking the two on length. That
    # sentence reads to a reader as the reason this work is not held in
    # English, and it is one side of a contradiction the page has said it
    # cannot resolve. A reason is licensed by the finding it belongs to; where
    # no one finding could be read, no reason may stand for the row.
    #
    # So the reason count and the row count now differ by TWO rows, not one:
    # work3, which states no reason, and work4, whose reasons the page
    # declines with its finding.
    REASONS = [
        "No English translation has been published.",  # work1
        "Only part of it is out of copyright.",        # work2
        "No English translation has been published.",  # work5
    ]

    PARTIALS = ["Partly public domain — the 1893 selection"]

    def both(self):
        return self.page("finding-order"), self.page("finding-order-reversed")

    def clauses(self, page):
        """The summary's clauses, and there are four of them.

        The length is asserted here so that a page which loses a whole clause
        — the shape the first-match defect took, three works collapsing into
        one "cannot read" — fails as a claim about the sentence rather than as
        an index error inside the test that reads it.
        """
        said = page["absenceSummary"].split("; ")
        self.assertEqual(len(said), 4, page["absenceSummary"])
        return said

    def test_the_same_finding_set_reads_the_same_in_either_order(self):
        listed, reversed_ = self.both()
        # The absence semantics, named projection by named projection, so a
        # failure says WHICH claim moved with the listing order.
        for key in ("absenceSummary", "absenceReasons", "absencePartials",
                    "absenceOpen", "tallyText"):
            self.assertEqual(listed[key], reversed_[key],
                             "%s moved with the listing order" % key)
        # And then the whole rendered page, because a finding reaches more
        # sinks than the absence view and the order must reach none of them.
        self.assertEqual(self.rendered_state(listed), self.rendered_state(reversed_))
        self.assertEqual(listed["statusWrites"], reversed_["statusWrites"])

    def test_the_summary_is_this_one_sentence_in_either_order(self):
        # Pinned exactly, in both orders, so a change that breaks the two
        # identically still fails: agreement is not the whole claim.
        for page in self.both():
            self.assertEqual(page["absenceSummary"], self.SUMMARY)
            # Four clauses, one per finding class any row stands on.
            self.assertEqual(len(page["absenceSummary"].split("; ")), 4)

    def test_a_malformed_record_never_stands_in_for_the_valid_finding_beside_it(self):
        # work1, work2 and work3 each pair one valid typed finding with one
        # malformed record. Listed first, the malformed record used to take the
        # row: work1 fell out of the closed clause, work2 out of the partial
        # clause and work3 out of the surveyed clause, and all three landed in
        # "cannot read" — in one order only.
        #
        # The malformed record's own prose is the tell. It states a sound
        # `reason`, and that reason belongs to a finding the page cannot read;
        # the row's prose is taken from a record CARRYING THE CHOSEN FINDING,
        # so the malformed neighbour's words never reach the page.
        for page in self.both():
            self.assertEqual(page["absenceReasons"], self.REASONS)
            self.assertNotIn("A reason standing beside an unreadable finding.",
                             page["absenceReasons"])
            # V7: nor does the prose of EITHER side of work4's contradiction
            # stand for work4. Exactly one partial-public-domain reason is on
            # the page, and it is work2's.
            self.assertEqual(
                page["absenceReasons"].count("Only part of it is out of copyright."),
                1, "a declined contradiction contributed a reason")

    def test_an_unknown_finding_never_stands_in_for_the_valid_one(self):
        # work5 pairs `no-such-finding` with a valid `none-published`. An
        # unknown finding is carried and claims nothing, so the valid one is
        # the record speaking and work5 is the second work in the closed
        # clause. Had the unknown taken the row, the first clause would read
        # "One work standing here has" and the last would count two.
        for page in self.both():
            clauses = self.clauses(page)
            self.assertEqual(
                clauses[0],
                "2 works standing here have no English this project may publish")
            self.assertEqual(clauses[3], "1 has a finding this page cannot read")

    def test_not_surveyed_is_never_counted_into_a_publishing_negative(self):
        # `not-surveyed` says only that nobody has looked. work3 states it
        # beside a malformed record, and neither the malformed neighbour nor
        # the old `partial`-truthiness reading may promote it: an admission of
        # ignorance is not "no English this project may publish", and a weaker
        # record never yields a stronger negative.
        for page in self.both():
            clauses = self.clauses(page)
            self.assertEqual(clauses[2], "1 has not been surveyed for English")
            # Exactly two works carry the closed negative — work1 and work5.
            # Three would mean work3 had been swept in.
            self.assertEqual(
                clauses[0],
                "2 works standing here have no English this project may publish")

    def test_a_self_contradicting_record_is_declined_and_never_resolved(self):
        # work4 states `none-published` AND `partial-public-domain`, both
        # valid, both typed, and they say different things. The page chooses
        # NEITHER — and in particular not the harsher, which is how an absence
        # gets manufactured. First-match chose whichever was written first, so
        # this single work read as a closed negative in one order and as an
        # untaken offer in the other.
        for page in self.both():
            clauses = self.clauses(page)
            # It is counted, once, as unreadable.
            self.assertEqual(clauses[3], "1 has a finding this page cannot read")
            # And it is counted into neither of the two classes it names: the
            # closed clause holds work1 and work5, the untaken clause work2.
            self.assertEqual(
                clauses[0],
                "2 works standing here have no English this project may publish")
            self.assertEqual(
                clauses[1],
                "1 has only a partly public domain English, not yet taken")
            # Its `partial` string is not rendered either: a refused finding
            # licenses no offer. One partial line stands, and it is work2's.
            self.assertEqual(page["absencePartials"], self.PARTIALS)

    def test_valid_facts_survive_beside_the_records_the_page_refuses(self):
        # CORRECTED ORACLE (V7). Refusing what cannot be read must cost the
        # record nothing it really states — and work4's reason is not such a
        # thing. work4 carries TWO valid findings that say different things,
        # the page declines to choose between them, and a reason belonging to
        # one of the two is not a fact standing apart from that choice: it is
        # the choice, in prose. V6 rendered it, and the V6 review named that as
        # a leaked rights statement.
        #
        # What survives is what the row states independently of the finding:
        # work4 keeps its author and its work, and still stands as a row.
        #
        # The companion case — a valid finding standing beside a `reason` that
        # is not text — is `typed.work3` of the `typed-absence` scenario, is
        # pinned by `TypedAbsenceFindingTest`, and is deliberately unchanged:
        # there the finding IS readable, so the row still speaks with it.
        for page in self.both():
            self.assertEqual(page["absenceReasons"], self.REASONS)
            self.assertEqual(len(page["absenceReasons"]), 3)
            self.assertNotIn("Only part of it is out of copyright.",
                             page["absenceReasons"][2:],
                             "the declined contradiction still speaks")
            self.assertIn("1 has not been surveyed for English",
                          page["absenceSummary"].split("; "))
            # work4 is still a row: declining its finding is not deleting it.
            self.assertEqual(len(page["absenceAuthors"]), 5)

    def test_both_orders_complete_and_stand_open(self):
        # A render-tail throw would leave the region claiming work in progress
        # and every assertion above reading a half-built page.
        for page in self.both():
            self.assertEqual(page["busy"], "false")
            self.assertTrue(page["absenceOpen"])
            self.assertIn("absence", page["dataStates"])
            self.assertEqual(
                page["statusWrites"],
                ["Genesis 1, Douay-Rheims (Challoner), 5 fragments held,"
                 " none in English translation."])


class StrayPartialOfferTest(ReplayTest):
    """V6 §8 — `partial` refines a finding and never establishes one.

    The page classified an absence row by whether a `partial` string happened
    to be attached, so any string in that field was printed as "Partly public
    domain — …" whatever finding it sat beside. That is a rights claim about
    somebody's text, made about a work nobody has surveyed, about a finding
    this project does not define, about a record naming no finding at all, and
    about a work whose finding is that it is IN COPYRIGHT. Only the finding
    that says it in its own name licenses the words.

    `stray-partial` attaches an offer to each of those four, and one genuine
    `partial-public-domain` record stands among them so that refusing the
    strays cannot be mistaken for refusing them all.
    """

    # Clause by clause, in spine order `typed.work1` .. `typed.work5`:
    #
    #   work5  in-copyright + stray partial      -> closed      -> "One work
    #                                                              standing
    #                                                              here has ..."
    #   work4  partial-public-domain, genuine    -> untaken     -> "1 has only
    #                                                              a partly ..."
    #   work1  not-surveyed + stray partial      -> unsurveyed  -> "1 has not
    #                                                              been surveyed"
    #   work2  unknown finding + stray partial   -> ''          \  "2 have a
    #   work3  no finding at all + stray partial -> ''          /   finding this
    #                                                              page cannot
    #                                                              read"
    #
    # The first clause names the works and so reads "One work standing here
    # has"; every later clause carries the number alone.
    SUMMARY = (
        "One work standing here has no English this project may publish;"
        " 1 has only a partly public domain English, not yet taken;"
        " 1 has not been surveyed for English;"
        " 2 have a finding this page cannot read")

    STRAYS = (
        "a stray offer beside an admission",
        "a stray offer beside an unknown finding",
        "a stray offer beside no finding at all",
        "a stray offer beside a closed finding",
    )

    def test_the_summary_is_this_one_sentence(self):
        self.assertEqual(self.page("stray-partial")["absenceSummary"], self.SUMMARY)

    def test_exactly_one_partial_line_renders_and_it_is_the_genuine_one(self):
        # Before V6 this list held FIVE entries — one per `partial` string in
        # the fixture — of which four were public-domain claims about text no
        # record says anything of the kind about. An exact one-element list is
        # the whole assertion: a count taken with `assertIn` would have passed
        # on the defect.
        self.assertEqual(self.page("stray-partial")["absencePartials"],
                         ["Partly public domain — the 1893 selection"])

    def test_no_stray_offer_reaches_the_page_as_words(self):
        # The offers are refused, not merely uncounted: none of the four may
        # surface anywhere a reader reads or a screen reader speaks.
        page = self.page("stray-partial")
        said = ([page["absenceSummary"] or ""] + page["absenceReasons"]
                + page["absencePartials"] + page["asideNotes"]
                + page["sectionHeadings"] + page["statusWrites"])
        rendered = "\n".join(said)
        for stray in self.STRAYS:
            self.assertNotIn(stray, rendered)

    def test_a_stray_offer_never_moves_its_row_into_another_class(self):
        # Each row stands on its own finding and the offer beside it changes
        # nothing. `not-surveyed` stays an admission rather than becoming a
        # publishing negative; `in-copyright` stays closed rather than becoming
        # an untaken offer; the unknown finding and the missing one stay
        # unreadable. The untaken clause counts ONE — the genuine record — and
        # would have counted five.
        self.assertEqual(
            self.page("stray-partial")["absenceSummary"].split("; "),
            ["One work standing here has no English this project may publish",
             "1 has only a partly public domain English, not yet taken",
             "1 has not been surveyed for English",
             "2 have a finding this page cannot read"])

    def test_a_reason_the_record_really_states_survives_the_refused_offer(self):
        # work5 states a reason beside a `partial` the page throws away, and
        # work4 states one beside a `partial` it keeps. Both reasons render, in
        # row order; the three rows that state no reason contribute no line.
        self.assertEqual(self.page("stray-partial")["absenceReasons"],
                         ["Only part of it is out of copyright.",   # work4
                          "A living author's rendering."])          # work5

    def test_the_stray_partial_page_completes_and_stands_open(self):
        page = self.page("stray-partial")
        self.assertEqual(page["busy"], "false")
        self.assertTrue(page["absenceOpen"])
        self.assertIn("absence", page["dataStates"])
        self.assertEqual(
            page["statusWrites"],
            ["Genesis 1, Douay-Rheims (Challoner), 5 fragments held,"
             " none in English translation."])


class AbsenceRowIdentityTest(ReplayTest):
    """V6 §7 — which work each absence row is about, said rather than inferred.

    An absence is a claim about a particular man's particular book: that no
    English of it has been published, or that its rights are held, or that
    nobody has looked. Until V6 nothing here could name the row — the counts
    and the per-row reasons were the only handle — so "the declined row is
    work4" was an inference from arithmetic rather than an assertion about the
    page. `absence-author` and `absence-work` are now projected, and the five
    rows are named in the order the spine gives them, in either record order.
    """

    ROWS = (["Author 1", "Author 2", "Author 3", "Author 4", "Author 5"],
            ["Work 1", "Work 2", "Work 3", "Work 4", "Work 5"])

    def test_every_work_keeps_its_row_whichever_order_the_findings_arrive(self):
        # Five works stand under this chapter and five rows render. The
        # malformed and contradictory records cost no work its row — the
        # correction refuses a CLAIM it cannot support, not the record's
        # existence, and a work whose finding the page declines is still a
        # work standing here that the reader is owed a line about.
        for name in ("finding-order", "finding-order-reversed"):
            page = self.page(name)
            self.assertEqual(page["absenceAuthors"], self.ROWS[0], name)
            self.assertEqual(page["absenceWorks"], self.ROWS[1], name)

    def test_the_stray_partial_page_keeps_all_five_rows_too(self):
        page = self.page("stray-partial")
        self.assertEqual(page["absenceAuthors"], self.ROWS[0])
        self.assertEqual(page["absenceWorks"], self.ROWS[1])

    def test_the_row_identities_are_the_spine_order_not_the_finding_order(self):
        # The rows follow `sources`, which is the order the chapter file
        # writes its editions in; reversing the ABSENCE records inside the
        # index moves nothing here. That is the invariance stated as identity
        # rather than as a count.
        self.assertEqual(self.page("finding-order")["absenceWorks"],
                         self.page("finding-order-reversed")["absenceWorks"])


class AbsenceRowFlatteningTest(ReplayTest):
    """The integration review's first merge blocker — two facts, one word.

    `renderAbsences` appended `.absence-author` and `.absence-work` as
    ADJACENT element children with nothing between them, so the row's
    flattened text — what a screen reader announces, what a copy takes, what
    a text-only rendering shows — read `Ambrose of MilanHexameron`. The
    author and the title are two separate claims about the corpus and they
    were being handed to a reader joined into one string.

    The correction is a text node, not a style. A margin, a `gap` or a
    `::before` would move the two spans apart on screen and leave the
    flattened text exactly as it was, so every assertion here reads the
    row's recursive `textContent` and its child-node sequence rather than
    its appearance. The `absence-reason` and `absence-partial` paragraphs
    that follow are BLOCK elements, and their boundary is structural; only
    the two inline identity spans needed a delimiter of their own.
    """

    #: The delimiter the page already uses between an author and a work, in
    #: `renderLeads`. The absence rows now match it rather than inventing a
    #: second convention.
    APART = " — "

    def test_every_absence_row_states_the_author_apart_from_the_work(self):
        # The real production route, not a fixture: Genesis 1 under
        # `translation:en`, whose eight absence rows are the rows the review
        # read `Ambrose of MilanHexameron` off.
        page = self.page("voice-held")
        rows = page["absenceRowTexts"]
        self.assertEqual(len(rows), 8, "the eight recorded absences must stand")
        for author, work, said in zip(page["absenceAuthors"],
                                      page["absenceWorks"], rows):
            with self.subTest(work=work):
                self.assertTrue(said.startswith(author + self.APART + work),
                                f"{said[:80]!r} does not separate its identities")
                self.assertNotIn(author + work, said,
                                 "the author and the work are flattened together")

    def test_the_reviewed_row_is_the_reviewed_row(self):
        # The exact string the review reported, asserted absent, and the
        # exact string that must stand in its place. Pinned by name so a
        # regression is recognisable as the reported defect and not merely as
        # a failed loop.
        rows = self.page("voice-held")["absenceRowTexts"]
        ambrose = next(one for one in rows if one.startswith("Ambrose of Milan"))
        self.assertNotIn("Ambrose of MilanHexameron", ambrose)
        self.assertTrue(ambrose.startswith("Ambrose of Milan — Hexameron"))

    def test_a_row_about_another_author_is_separated_the_same_way(self):
        # THE ADJACENT-IDENTITY CONTROL. A fix written for one row would pass
        # the assertion above and fail here. Two further real rows are named:
        # one whose author is a single word, and the last row of the eight —
        # the two shapes a positional patch is most likely to miss.
        rows = self.page("voice-held")["absenceRowTexts"]
        for opening in ("Jerome — Liber quaestionum hebraicarum in Genesim",
                        "Remigius of Auxerre — Commentarius in Genesim"):
            with self.subTest(row=opening):
                self.assertTrue(any(one.startswith(opening) for one in rows),
                                f"no row opens {opening!r}")

    def test_the_delimiter_is_a_node_in_the_document(self):
        # The claim CSS cannot make. Between the two identity spans there is
        # a non-empty TEXT NODE, in that position, in every row — on the real
        # route and on the typed fixture whose rows carry no reason at all,
        # so the shortest possible row is checked too.
        for name in ("voice-held", "typed-absence"):
            for row in self.page(name)["absenceRowNodes"]:
                with self.subTest(scenario=name, row=row):
                    self.assertEqual(row[:3],
                                     ["absence-author", "#text", "absence-work"])

    def test_no_row_ends_or_opens_with_a_dangling_delimiter(self):
        # The delimiter is written only where BOTH halves are there, so a row
        # the record could not name in full would carry no orphaned dash. No
        # production route reaches that state — `V7AbsenceMemberTest` proves
        # a hollow source takes no slot — and this is the guard's own pin.
        for name in ("voice-held", "typed-absence", "voice-empty-chapter"):
            for said in self.page(name)["absenceRowTexts"]:
                with self.subTest(scenario=name, row=said[:40]):
                    self.assertFalse(said.startswith(self.APART.lstrip()), said)
                    self.assertFalse(said.rstrip().endswith("—"), said)

    def test_the_separated_rows_still_stand_in_an_open_disclosure(self):
        # The correction is inside the disclosure the absence contract
        # requires to be OPEN on arrival, and it changed neither the state
        # nor the count nor the summary that names it.
        page = self.page("voice-held")
        self.assertTrue(page["absenceOpen"],
                        "the reasons must still be visible without interaction")
        self.assertEqual(
            page["absenceSummary"],
            "6 works standing here have no English this project may publish; "
            "2 have only a partly public domain English, not yet taken")
        self.assertEqual(len(page["absenceReasons"]), 8)
        self.assertEqual(len(page["absencePartials"]), 2)
        self.assertIn("absence", page["dataStates"])

    def test_the_delimiter_matches_the_convention_the_leads_already_keep(self):
        # One page, one grammar. `renderLeads` has always written
        # `author — title`, so the absence rows now read the same way rather
        # than introducing a second separator a reader has to learn.
        page = self.page("voice-held")
        lead = next((one for one in page["leads"] if self.APART in one), None)
        self.assertIsNotNone(lead, "a lead entry with both identities is owed")
        self.assertIn(self.APART, page["absenceRowTexts"][0])


class RootLanguageIdentityTest(ReplayTest):
    """V6 §5 — the ROOT language record, and the two ways it lied.

    The V5 review read `Douay-Rheims ([object Object])` out of the edition
    control in real Chromium. Nothing in this file could see it: the control
    was never projected. The correction that followed had to answer two
    defects at once, because the first repair invited the second.

    A language identity is usable only if it satisfies the accepted code
    contract — `/^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$/`. COERCION printed the
    unreadable value back at the reader; SUBSTITUTION answered it with `en`
    because a default was to hand, which told a screen reader to read a
    Latin edition in an English voice on the authority of `|| 'en'`. A
    guessed fact is not a smaller defect than a coerced one. The claim is
    OMITTED, and `V6_BIBLE_LANGUAGES` stands nine editions in a row to prove
    it: an object, a list, a number, a boolean, null, empty, whitespace,
    arbitrary prose, and two sound codes that must keep everything they say.
    """

    # The exact reading of the edition control, for both scenarios. Every
    # entry is the label ALONE where the record states no readable language,
    # and label + `(code)` where it states one.
    #
    # PRE-V6 this list read `Douay-Rheims ([object Object])`,
    # `List Language (en)`, `Number Language (42)`, `Boolean Language (true)`
    # and `Null Language (en)` — a coerced record, a coerced scalar, and a
    # guessed default standing in for three languages nobody stated.
    OPTIONS = ["Douay-Rheims", "List Language", "Number Language",
               "Boolean Language", "Null Language", "Empty Language",
               "Blank Language", "Prose Language", "Clementine Vulgate (la)"]

    # Every request the page makes for either page. No language reaches one.
    FETCHED = ["structure/catena/index.json", "bibles.json",
               "structure/paragraphs/index.json",
               "structure/catena/01-gen/001.json",
               "douay-rheims/chapters/Gen/1.json",
               "structure/paragraphs/douay-rheims/01-gen/001.json"]

    def test_an_unreadable_edition_language_is_omitted_from_its_option(self):
        # The whole control, in order, for both selections: the parenthetical
        # is a language claim and it is made only where a language was stated.
        for name in ("bible-language-forms", "bible-language-forms-voice"):
            self.assertEqual(self.page(name)["bibleLabels"], self.OPTIONS, name)

    def test_no_edition_language_is_guessed_for_the_passage(self):
        # `body.lang = bible.language || 'en'` is how Douay-Rheims, whose
        # language here is `{"code": "en"}`, made the whole passage element
        # claim English. The edition states no language this page can use, so
        # the passage makes no language claim at all.
        for name in ("bible-language-forms", "bible-language-forms-voice"):
            page = self.page(name)
            self.assertEqual(
                [one for one in page["langAttributes"] if one.startswith("passage=")],
                [], f"{name}: an unreadable language claims nothing")

    def test_the_sound_control_still_writes_the_passage_language(self):
        # Omission is not silence everywhere: the real manifest states `en`
        # for Douay-Rheims and the passage carries it. Without this the test
        # above would also pass on a page that had stopped writing `lang`.
        self.assertEqual(
            [one for one in self.page("default")["langAttributes"]
             if one.startswith("passage=")],
            ["passage=en"])

    def test_every_language_attribute_written_is_a_language_subtag(self):
        # The fragment sink, counted rather than deduplicated: 107 fragments
        # under Everything held, each carrying its own source's sound code,
        # and 14 under the English translation. `classes` and `dataStates`
        # are sets and would read the same for one attribute and for a
        # hundred; `langAttributes` is the whole journal in rendered order.
        held = self.page("bible-language-forms")["langAttributes"]
        self.assertEqual(len(held), 107)
        # Counted, so the three sinks account for all 107 and none is a
        # substitute for another: 88 Latin, 14 English, 5 Greek.
        self.assertEqual([held.count(one) for one in
                          ("fragment-text=la", "fragment-text=en", "fragment-text=grc")],
                         [88, 14, 5])
        voiced = self.page("bible-language-forms-voice")["langAttributes"]
        self.assertEqual(voiced, ["fragment-text=en"] * 14)
        for written in held + voiced:
            code = written.split("=", 1)[1]
            self.assertRegex(code, r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$", written)

    def test_no_unreadable_language_reaches_a_route_or_a_request(self):
        # A language becomes a voice key, a select value and a URL. None of
        # these nine ever composed one: the page writes no history entry, the
        # selection is the reader's own, and the request journal is the six
        # files a Genesis 1 arrival asks for and nothing beside them.
        for name in ("bible-language-forms", "bible-language-forms-voice"):
            page = self.page(name)
            self.assertEqual(page["fetched"], self.FETCHED, name)
            self.assertEqual(page["hashWrites"], [], name)
            self.assertEqual(page["replaced"], [], name)
            self.assertEqual(page["selectValues"],
                             {"book": "Gen", "chapter": "1", "bible": "douay-rheims"},
                             name)

    def test_nothing_unreadable_reaches_the_page_as_words(self):
        # The reader-facing prose alone, so a value in the harness's own
        # report cannot be mistaken for a value coerced into the page.
        for name in ("bible-language-forms", "bible-language-forms-voice"):
            page = self.page(name)
            said = []
            for key in ("bibleLabels", "voiceLabels", "filterLabels", "languages",
                        "sectionHeadings", "asideNotes", "statusWrites",
                        "hashWrites", "bookLabels"):
                said.extend(page.get(key) or [])
            said.append(page.get("tallyText") or "")
            said.append(page.get("referenceText") or "")
            rendered = " ¶ ".join(str(one) for one in said)
            for token in ("[object Object]", "undefined", "null", "true", "42",
                          "not a language code"):
                self.assertNotIn(token, rendered, f"{name}: {token!r} reached the page")

    def test_refusing_nine_languages_costs_no_other_fact(self):
        # Withholding an unreadable claim must cost nothing that WAS stated.
        # Under the English translation the whole page still stands: the voice
        # control, the tally, the filter, the absence view and the testament.
        page = self.page("bible-language-forms-voice")
        self.assertEqual(page["voice"], "translation:en")
        self.assertEqual(page["voiceLabels"],
                         ["Everything held", "The author’s own language",
                          "English translation", "Latin translation"])
        self.assertEqual(page["fragmentCount"], 14)
        self.assertEqual(page["tallyText"],
                         "107 fragments held · 14 in English translation · "
                         "33 lead entries on the acquisition list")
        self.assertEqual(page["filterLabels"],
                         ["Basil of Caesarea", "Gregory of Nyssa",
                          "Augustine of Hippo", "Martin Luther"])
        self.assertEqual(page["absenceSummary"],
                         "6 works standing here have no English this project may "
                         "publish; 2 have only a partly public domain English, "
                         "not yet taken")
        self.assertEqual(page["referenceBookText"], "Old Testament")

    def test_both_pages_terminate(self):
        for name in ("bible-language-forms", "bible-language-forms-voice"):
            page = self.page(name)
            self.assertEqual(page["busy"], "false", name)
            self.assertTrue(page["statusWrites"], name)
            self.assertEqual(page["errorSections"], [], name)


class EditionIdentityTest(ReplayTest):
    """V6 §5 — an edition that cannot name itself is no edition.

    An edition id is three things at once: the value of an option, the
    `bible` term of the published route, and a directory inside every chapter
    request. `sound()` asks only whether text arrived, so `"../../escape"`,
    `"has space"` and `""` were each an edition so far as this page was
    concerned — offered to a reader, written into a URL and composed into a
    fetch. An id that is not an identity of this corpus, or a record with no
    label to show, names nothing and is left out; `V6_BIBLE_IDENTITIES`
    stands two sound editions beside the four broken ones because refusing a
    broken record must not empty the control.
    """

    # The four ways a record fails to name itself here, each of which reached
    # a URL before V6.
    UNNAMEABLE = ("../../escape", "has space", "Escaping Edition",
                  "Spaced Edition", "Nameless Edition", "no-label")

    def test_only_the_editions_that_can_name_themselves_are_offered(self):
        # Two of six. PRE-V6 this control offered six options, four of which
        # named no edition — including one whose value was `""` and one whose
        # value walked out of the data root.
        self.assertEqual(self.page("bible-identity-forms")["bibleLabels"],
                         ["Douay-Rheims (en)", "Clementine Vulgate (la)"])

    def test_no_unnameable_id_reaches_a_request(self):
        # The whole request journal, exactly: six files, every one of them
        # under the edition the reader actually selected.
        page = self.page("bible-identity-forms")
        self.assertEqual(page["fetched"],
                         ["structure/catena/index.json", "bibles.json",
                          "structure/paragraphs/index.json",
                          "structure/catena/01-gen/001.json",
                          "douay-rheims/chapters/Gen/1.json",
                          "structure/paragraphs/douay-rheims/01-gen/001.json"])
        for asked in page["fetched"]:
            self.assertNotIn("..", asked, asked)
            for form in self.UNNAMEABLE:
                self.assertNotIn(form, asked, asked)

    def test_no_unnameable_id_reaches_the_route(self):
        # The route keeps the reader's own edition and the page writes no
        # history entry of its own, so no broken id was ever a route value.
        page = self.page("bible-identity-forms")
        self.assertEqual(page["hash"], "#book=Gen&chapter=1&bible=douay-rheims")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["selectValues"],
                         {"book": "Gen", "chapter": "1", "bible": "douay-rheims"})

    def test_the_sound_editions_beside_them_are_untouched(self):
        # The whole chapter renders as it does from the real manifest: the
        # passage carries the edition's language, the verses and paragraphs
        # are counted, and every fragment stands.
        page = self.page("bible-identity-forms")
        self.assertEqual(
            [one for one in page["langAttributes"] if one.startswith("passage=")],
            ["passage=en"])
        self.assertEqual(page["chapterCounts"], ["31 verses", "8 paragraphs"])
        self.assertEqual(page["verseNumbers"], [str(n) for n in range(1, 32)])
        self.assertEqual(page["referenceText"], "Genesis 1")
        self.assertEqual(page["referenceBookText"], "Old Testament")
        self.assertEqual(page["fragmentCount"], 107)
        self.assertEqual(page["tallyText"],
                         "107 fragments held · 33 lead entries on the acquisition list")

    def test_the_page_terminates(self):
        page = self.page("bible-identity-forms")
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["statusWrites"],
                         ["Genesis 1, Douay-Rheims, 107 fragments held, "
                          "33 lead entries on the acquisition list."])
        self.assertEqual(page["errorSections"], [])


class NullBootstrapTerminalStateTest(ReplayTest):
    """V6 §12 — a SUCCESSFUL fetch that answers `null` is a terminal state.

    `bootstrap-failure` proves only the 404. A 200 carrying JSON `null` — or a
    list, or a scalar — is a valid document that is not the record asked for,
    and it arrives INSIDE the request's success arm: the read threw past the
    request catch, between the last fetch and the first render, and the page
    stood at "Loading…" for ever with every control dead, no tally, no
    announcement and no way to learn why. Nothing in the V5 suite could see it,
    because a page that never finishes rendering fails no assertion that only
    reads the parts it did render.

    Each of these pins the WHOLE terminal state: no "Loading…" left in the
    reference or in a control, `aria-busy` resolved to false, one exact spoken
    line, no tally, no content, and no mutation of the address the reader typed.
    """

    # Every bootstrap that cannot produce a page ends in the SAME shell. The
    # shell is stated once here and the tests below name it, so a regression
    # that half-renders one of these fails on the field it broke.
    SHELL = {
        "referenceText": "Unavailable",
        "referenceBookText": "",
        "bookLabels": ["Unavailable"],
        "voiceLabels": ["Unavailable"],
        "bibleLabels": ["Unavailable"],
        "selectValues": {"book": "", "chapter": "", "bible": ""},
        "tallyText": "",
        "busy": "false",
        "activeElement": "body",
        "hashWrites": [],
        "replaced": [],
        "errorSections": [],
        "fragmentCount": 0,
        "fragmentIds": [],
        "sectionHeadings": [],
        "verseNumbers": [],
        "leads": [],
        "blocked": [],
        "staticEntry": False,
        "stepButtons": [True, True],
    }

    def assert_terminal_shell(self, name: str, spoken: str):
        page = self.page(name)
        for key, value in self.SHELL.items():
            self.assertEqual(page[key], value, f"{name}: {key}")
        # The failure's own words, in the region and on the single announcement
        # channel, said exactly once. `T.fail` writes the same string to both,
        # so the visible paragraph and the spoken line are pinned together.
        self.assertEqual(page["statusWrites"], [spoken], name)
        self.assertEqual(page["statusText"], spoken, name)
        # `classes` is a deduplicated SET and is used here for IDENTITY, never
        # for a count: the failure paragraph is the only classed node standing
        # in the reading region, so no half-built chapter survives beneath it.
        self.assertEqual(page["classes"], ["error"], name)

    def test_a_null_index_ends_in_a_stated_failure_not_a_permanent_loading(self):
        # THE DEFECT ITSELF: 200 + `null` for the catena index, under a real
        # deep link. Before V6 the reference and all four controls said
        # "Loading…" for ever and `statusWrites` was empty.
        self.assert_terminal_shell("null-index", "The catena index could not be read.")
        page = self.page("null-index")
        self.assertNotIn("Loading", page["referenceText"])
        self.assertNotIn("Loading…", page["bookLabels"])
        self.assertEqual(page["hash"], GEN1, "the reader's address is left alone")

    def test_a_cold_null_index_ends_in_the_same_stated_failure(self):
        self.assert_terminal_shell("null-index-cold",
                                   "The catena index could not be read.")
        self.assertEqual(self.page("null-index-cold")["hash"], "",
                         "no hash arrived and none may be manufactured")

    def test_a_null_translation_list_names_its_own_failure(self):
        # A different record, so a different reason: the page may not report
        # the index for a manifest that answered `null`.
        self.assert_terminal_shell("null-bibles", "bibles.json lists no translations.")
        self.assertEqual(self.page("null-bibles")["hash"], GEN1)

    def test_a_list_shaped_index_ends_in_a_stated_failure(self):
        self.assert_terminal_shell("list-index", "The catena index could not be read.")
        self.assertEqual(self.page("list-index")["hash"], GEN1)

    def test_the_neighbouring_unreadable_roots_end_the_same_way(self):
        # The already-committed shapes, pinned to the same exact journal so the
        # `null` correction cannot be made by special-casing one body form.
        for name in ("malformed-canon", "scalar-index"):
            with self.subTest(scenario=name):
                self.assert_terminal_shell(
                    name, "The catena index could not be read.")

    def test_a_transport_failure_still_says_transport_and_not_unreadable(self):
        # The 404 and the unreadable 200 are DIFFERENT facts about the world
        # and must not collapse into one sentence.
        self.assert_terminal_shell(
            "bootstrap-failure",
            "The catena index could not be loaded:"
            " ../browse/structure/catena/index.json was not found (404)")
        self.assert_terminal_shell(
            "bootstrap-bibles-failure",
            "The translation list could not be loaded:"
            " ../browse/bibles.json was not found (404)")

    def test_every_unusable_bootstrap_renders_one_identical_terminal_page(self):
        # The whole rendered state, not a chosen field: eight bootstrap
        # failures, one shell, differing ONLY in the reason given and in the
        # address the reader arrived with.
        journals = {"fetched", "hashWrites", "replaced", "statusWrites",
                    "snapshots", "released", "requests", "replacedStates",
                    "descriptorReads", "spineReads", "ownership",
                    "projectionIds", "projectionPasses",
                    # V14: the identity, ownership, accessor and inventory
                    # journals are per-session records of HOW the page was
                    # reached, never of what it rendered.
                    "consumerRefs", "authoritativeRefs", "projectionRowRefs",
                    "witness", "asks", "sourceCalls", "memberReads",
                    # V15: the transport-owner and body-application journals
                    # are per-session records of WHO asked and who wrote, not
                    # of what stands on the page.
                    "transports", "applied", "observations",
                    "publication", "writeBreak", "escaped",
                    "immutability"}
        base = {key: value for key, value in self.page("null-index").items()
                if key not in journals
                     and key not in ("hash", "statusText", "failureText")}
        for name in ("null-index-cold", "list-index", "malformed-canon",
                     "scalar-index", "null-bibles", "bootstrap-failure",
                     "bootstrap-bibles-failure"):
            with self.subTest(scenario=name):
                other = {key: value for key, value in self.page(name).items()
                         if key not in journals
                     and key not in ("hash", "statusText", "failureText")}
                self.assertEqual(other, base)

    def test_no_unusable_bootstrap_asks_for_a_chapter_or_writes_a_route(self):
        # Three root requests and nothing else: a page that cannot read its
        # index must not go on to fetch, tally or push anything.
        for name in ("null-index", "null-index-cold", "null-bibles", "list-index",
                     "malformed-canon", "scalar-index", "bootstrap-failure",
                     "bootstrap-bibles-failure"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["fetched"],
                                 ["structure/catena/index.json", "bibles.json",
                                  "structure/paragraphs/index.json"])
                self.assertEqual(page["hashWrites"], [])
                self.assertEqual(page["replaced"], [])


class GenuinelyLateStaleWorkTest(ReplayTest):
    """V6 §13 — work that completes AFTER the next state has fully settled.

    The V5 §9 scenarios released every parked request BEFORE navigating away,
    so no late work ever existed and "nothing stale survives" could not fail.
    These hold action A open across B: A's request is issued, B is chosen and
    allowed to settle completely, and ONLY THEN is A resolved or rejected.

    The proof of lateness is asserted, not assumed:
    `test_the_late_work_is_really_late` shows the request was issued before B,
    had not completed when B began, and is released by a step that stands after
    B's step in the scenario itself.
    """

    # The keys a stale completion could plausibly move: route, history,
    # announcement, tally, busy, focus and everything rendered.
    #
    # CORRECTED ORACLE (V7). The V6 guard omitted the FINAL STATUS SINK. It
    # compared `statusWrites` — the journal of everything ever spoken — which
    # a late completion cannot shorten and could only lengthen. What a reader
    # or a screen reader actually meets is `statusText`, the live region's
    # current contents, and a stale write that REPLACED the standing
    # announcement with an older one would leave the journal identical and
    # the region wrong. The V6 review named that gap, and it is the reason
    # the rest of this list is now enumerated rather than sampled: every
    # projection the page writes on a settled route is guarded, so a sink
    # added later is guarded by having to be added here too.
    GUARDED = ("hash", "hashWrites", "replaced", "statusWrites", "statusText",
               "tallyText", "busy", "activeElement", "referenceText",
               "selectValues", "fragmentCount", "fragmentIds", "fragmentTexts",
               "errorSections", "sectionHeadings", "failureText", "notices",
               "dataStates", "asideNotes", "refusalCount", "refusal",
               "absenceSummary", "absenceReasons", "absencePartials",
               "paragraphNote", "chapterCounts", "verseNumbers", "leads",
               "blocked", "voice", "voiceLabels", "stepButtons", "classes",
               "langAttributes", "acknowledgements", "authorGroups")

    GEN1_SPOKEN = ("Genesis 1, Douay-Rheims (Challoner), 107 fragments held,"
                   " 33 lead entries on the acquisition list.")
    GEN2_SPOKEN = ("Genesis 2, Douay-Rheims (Challoner), 99 fragments held,"
                   " 31 lead entries on the acquisition list.")
    GEN2_TALLY = "99 fragments held · 31 lead entries on the acquisition list"
    GEN2_HEADINGS = ["99 fragments held here",
                     "Believed to comment here — the acquisition list"]

    def steps_of(self, name: str) -> list:
        return [one for one in SCENARIOS if one["name"] == name][0].get("steps", [])

    def assert_unchanged_by_the_late_completion(self, name, settled, late):
        """Every guarded key, compared AND pinned by the caller: identical
        snapshots prove the late work changed nothing, and the caller's exact
        values prove the pair is not identically wrong."""
        before = self.snapshot(name, settled)
        after = self.snapshot(name, late)
        for key in self.GUARDED:
            self.assertEqual(after[key], before[key], f"{name}: {key} moved late")
        # And it asked for nothing new on its way past — nor did the settled
        # route acquire any request ownership it did not already hold.
        self.assertEqual(after["fetched"], before["fetched"], name)
        # The release really happened: `released` counts parked requests LET
        # GO, so a late completion that changed nothing is told apart from one
        # that never occurred.
        self.assertGreater(after["released"], before["released"], name)
        return after

    def test_the_late_work_is_really_late(self):
        # Without this the rest is vacuous. Three facts, in order:
        for name in ("genuinely-late-action", "genuinely-late-action-failure",
                     "genuinely-late-malformed"):
            with self.subTest(scenario=name):
                order = [(one["do"], one.get("label")) for one in self.steps_of(name)]
                # 1. the release stands AFTER the navigation in the scenario.
                self.assertEqual([one[0] for one in order],
                                 ["openFirstFragment", "selectChapter", "release"],
                                 name)
                self.assertEqual([one[1] for one in order],
                                 ["a-held", "b-settled", "a-late"], name)
                held = self.snapshot(name, "a-held")
                # 2. A's request really went out before B was chosen ...
                asked = [one for one in held["fetched"]
                         if one.startswith("structure/catena/text/")]
                self.assertEqual(len(asked), 1, name)
                # ... and the release step names the request that was parked.
                release = self.steps_of(name)[2]
                self.assertIn(release["path"], asked[0], name)
                # 3. and it had NOT completed: the opened fragment still stands
                # at "Loading…", where the same action undeferred (`default`,
                # "opened") shows its text on the spot.
                self.assertEqual(held["fragmentTexts"][0], "Loading…", name)
                self.assertNotEqual(
                    self.snapshot("default", "opened")["fragmentTexts"][0],
                    "Loading…",
                    "the control: an undeferred open completes immediately")

    def test_a_genuinely_late_success_changes_nothing_of_the_settled_route(self):
        after = self.assert_unchanged_by_the_late_completion(
            "genuinely-late-action", "b-settled", "a-late")
        self.assertEqual(after["hash"], GEN2)
        self.assertEqual(after["hashWrites"], [GEN2],
                         "B's action pushed exactly one entry, and A adds none")
        self.assertEqual(after["replaced"], [])
        self.assertEqual(after["statusWrites"], [self.GEN1_SPOKEN, self.GEN2_SPOKEN],
                         "the late arrival speaks nothing, and unsays nothing")
        self.assertEqual(after["tallyText"], self.GEN2_TALLY)
        self.assertEqual(after["busy"], "false")
        self.assertEqual(after["activeElement"], "chapter-select")
        self.assertEqual(after["referenceText"], "Genesis 2")
        self.assertEqual(after["selectValues"],
                         {"book": "Gen", "chapter": "2", "bible": "douay-rheims"})
        self.assertEqual(after["fragmentCount"], 99)
        self.assertEqual(len(after["fragmentIds"]), 99)
        self.assertEqual(after["fragmentIds"][0],
                         "passage.ambrose.hexameron.latin-migne-pl-14.6")
        self.assertEqual(
            after["fragmentIds"][-1],
            "passage.martin-luther.lectures-on-genesis"
            ".lenker-minneapolis-1904.genesis-2")
        self.assertEqual(after["errorSections"], [])
        self.assertEqual(after["sectionHeadings"], self.GEN2_HEADINGS)
        # Genesis 1's text landed into a detached fragment: no Genesis 2
        # fragment may show it, and none may be opened by it.
        self.assertEqual(set(after["fragmentTexts"]), {"Loading…"})

    def test_a_genuinely_late_failure_erases_nothing_of_the_settled_route(self):
        after = self.assert_unchanged_by_the_late_completion(
            "genuinely-late-action-failure", "b-settled", "a-late")
        self.assertEqual(after["hash"], GEN2)
        self.assertEqual(after["hashWrites"], [GEN2])
        self.assertEqual(after["replaced"], [])
        # THE CENTRAL CLAIM: a stale REJECTION owns no error. The exact journal
        # is pinned, not merely searched for "could not be loaded", so a failure
        # notice appended here fails on the whole list.
        self.assertEqual(after["statusWrites"], [self.GEN1_SPOKEN, self.GEN2_SPOKEN])
        self.assertEqual(after["tallyText"], self.GEN2_TALLY)
        self.assertEqual(after["busy"], "false",
                         "a stale rejection may not leave the region busy")
        self.assertEqual(after["activeElement"], "chapter-select")
        self.assertEqual(after["referenceText"], "Genesis 2")
        self.assertEqual(after["selectValues"],
                         {"book": "Gen", "chapter": "2", "bible": "douay-rheims"})
        self.assertEqual(after["fragmentCount"], 99)
        self.assertEqual(after["errorSections"], [])
        self.assertEqual(after["sectionHeadings"], self.GEN2_HEADINGS)
        for said in after["fragmentTexts"]:
            self.assertNotIn("could not be loaded", said,
                             "the failure belongs to a chapter the reader left")

    def test_a_genuinely_late_malformed_payload_settles_nothing_of_its_own(self):
        # The shape the V5 class claimed and never created: an UNREADABLE
        # payload completing after the page has moved on. A malformed body is
        # read on arrival, so this is the arm most likely to throw into the
        # current page's render.
        after = self.assert_unchanged_by_the_late_completion(
            "genuinely-late-malformed", "b-settled", "a-late")
        self.assertEqual(after["hash"], GEN2)
        self.assertEqual(after["hashWrites"], [GEN2])
        self.assertEqual(after["replaced"], [])
        self.assertEqual(
            after["statusWrites"],
            ["Genesis 1, Douay-Rheims (Challoner), 3 fragments held,"
             " 2 works held, not renderable yet,"
             " 2 lead entries on the acquisition list.",
             self.GEN2_SPOKEN])
        self.assertEqual(after["tallyText"], self.GEN2_TALLY,
                         "Genesis 1's tally may not be restored by a late read")
        self.assertEqual(after["busy"], "false")
        self.assertEqual(after["activeElement"], "chapter-select")
        self.assertEqual(after["referenceText"], "Genesis 2")
        self.assertEqual(after["fragmentCount"], 99)
        self.assertEqual(after["errorSections"], [])
        self.assertEqual(after["sectionHeadings"], self.GEN2_HEADINGS)
        # The refusal record belonged to the malformed Genesis 1 fixture; it
        # may not reappear beside Genesis 2's ninety-nine.
        self.assertEqual(after["refusalCount"], 0)
        for said in after["fragmentTexts"]:
            self.assertNotIn("[object Object]", said)

    def test_a_late_spine_cannot_repaint_a_refused_address(self):
        # An invalid address is a terminal state of its own, rendered by a
        # different arm from every success path. A spine held across it lands
        # with a chapter in hand and a page that must not accept it.
        order = [(one["do"], one.get("label"))
                 for one in self.steps_of("late-after-invalidation")]
        self.assertEqual(order, [("hash", "invalid"), ("release", "late")])
        invalid = self.snapshot("late-after-invalidation", "invalid")
        # The spine really was in flight: it was asked for, and Genesis 1 was
        # never announced, so its render never completed before the refusal.
        self.assertIn("structure/catena/01-gen/001.json", invalid["fetched"])
        self.assertEqual(invalid["statusWrites"],
                         ["The address is unchanged; the values not used are listed."])
        after = self.assert_unchanged_by_the_late_completion(
            "late-after-invalidation", "invalid", "late")
        self.assertEqual(after["hash"], "#book=Foo&chapter=1&bible=douay-rheims")
        self.assertEqual(after["hashWrites"], [],
                         "neither the refusal nor the late spine writes a route")
        self.assertEqual(after["replaced"], [])
        self.assertEqual(after["statusWrites"],
                         ["The address is unchanged; the values not used are listed."])
        self.assertEqual(after["tallyText"], "",
                         "a refused address counts nothing, however late")
        self.assertEqual(after["busy"], "false")
        self.assertEqual(after["activeElement"], "body")
        self.assertEqual(after["referenceText"], "Address not used")
        self.assertEqual(after["selectValues"],
                         {"book": "Gen", "chapter": "1", "bible": "douay-rheims"})
        self.assertEqual(after["fragmentCount"], 0)
        self.assertEqual(after["fragmentIds"], [])
        self.assertEqual(after["sectionHeadings"],
                         ["This address cannot be used as written"])
        self.assertEqual(
            after["errorSections"],
            [{"heading": "This address cannot be used as written",
              "state": "error",
              "details": ["book=Foo is not a book of this canon."],
              "recoveryHref": GEN1}])


class RoutableIdentityTest(ReplayTest):
    """V6 §11 — a refused identity never becomes a URL, proved by asking.

    The identity tests beside this one pin that an unsafe id is carried as no
    identity: it composes no href and `fragmentIds` records nothing for it.
    That is necessary and it is not sufficient, and the distinction is the
    same one the V5 review made about evidence generally. OPENING a fragment
    is what turns its id into a fetched URL, and a scenario that opens only
    the safe fragment cannot fail on the defect: "no unsafe path was
    requested" holds because nothing asked. These two scenarios ask.
    """

    # Six ids that are sound TEXT and name nothing here: a traversal, a
    # spaced string, an upper-case form, whitespace, a trailing separator,
    # and a percent-encoded traversal.
    REFUSED = ("passwd", "etc", "..", "%2e", "Upper", "trailing/", " ")

    def test_opening_every_refused_fragment_composes_no_request(self):
        # Seven fragments opened, one text file fetched. Before V6 the six
        # refused ids each appended themselves to the text prefix, so
        # `structure/catena/text/../../../etc/passwd.json` was requested.
        page = self.page("unsafe-identities-opened")
        self.assertEqual(page["fetched"], [
            "structure/catena/index.json",
            "bibles.json",
            "structure/paragraphs/index.json",
            "structure/catena/01-gen/001.json",
            "douay-rheims/chapters/Gen/1.json",
            "structure/paragraphs/douay-rheims/01-gen/001.json",
            "structure/catena/text/safe-first.json",
        ])
        for asked in page["fetched"]:
            for form in self.REFUSED:
                self.assertNotIn(form, asked, f"{form!r} reached {asked!r}")

    def test_a_refused_fragment_says_it_carries_no_text_rather_than_loading(self):
        # The reader who opens one is told, exactly once, and is not left at
        # "Loading…" for a request that will never be made.
        page = self.page("unsafe-identities-opened")
        self.assertEqual(page["fragmentTexts"][1:7], [
            "This fragment carries no text file, so nothing of it can be shown."] * 6)
        # And the ones never opened are still standing at their placeholder,
        # which is what proves the six above were really opened.
        self.assertEqual(page["fragmentTexts"][7:], ["Loading…"] * 3)

    def test_the_safe_sibling_is_the_one_thing_asked_for(self):
        page = self.page("unsafe-identities-opened")
        self.assertEqual(page["fragmentIds"],
                         ["safe-first", None, None, None, None, None, None,
                          "coerced-source", "proto-source", "safe-last"])
        self.assertEqual(page["fragmentCount"], 10,
                         "refusing six identities costs no fragment its row")
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["statusWrites"],
                         ["Genesis 1, Douay-Rheims (Challoner), 10 fragments held."])

    def test_an_edition_that_cannot_name_itself_is_not_a_route(self):
        # The other half of the same question, one level up. An edition id is
        # a directory in the chapter request, so an unnameable one admitted to
        # the manifest was a published edition as far as the address grammar
        # could tell, and the page fetched `../../escape/chapters/Gen/1.json`.
        # It is now refused before the manifest, so the address fails closed.
        #
        # CORRECTED ORACLE (V7). The failing closed is unchanged and is the
        # whole of the security claim: the reader's text is kept, no request
        # is composed through the refused id, and the recovery link stands.
        # What is corrected is the SENTENCE. This manifest carries four
        # records that cannot name themselves — one of them the very value
        # cited — so the page could not read the set of published editions
        # whole, and "is not a published edition" is a claim about what this
        # project publishes made out of a manifest it failed to read. The V6
        # review named that class of sentence a semantic-integrity blocker.
        # The page now says the thing it can support.
        page = self.page("unsafe-bible-route")
        self.assertEqual(page["hash"], "#book=Gen&chapter=1&bible=../../escape",
                         "the URL keeps the reader's own text")
        self.assertEqual(page["referenceText"], "Address not used")
        self.assertEqual(page["errorSections"], [{
            "heading": "This address cannot be used as written",
            "state": "error",
            "details": ["bible=../../escape is not a value this page could match;"
                        " the record it would be matched against could not be"
                        " read whole."],
            "recoveryHref": "#book=Gen&chapter=1&bible=douay-rheims",
        }])
        self.assertEqual(page["fetched"], ["structure/catena/index.json",
                                           "bibles.json",
                                           "structure/paragraphs/index.json"],
                         "nothing was fetched through the refused id")

    def test_only_the_nameable_editions_are_offered_as_route_values(self):
        # The label a reader reads and the value the page routes on are two
        # facts. Both are now projected, and both name only the two editions
        # whose records can identify themselves.
        page = self.page("unsafe-bible-route")
        self.assertEqual(page["bibleLabels"],
                         ["Douay-Rheims (en)", "Clementine Vulgate (la)"])
        self.assertEqual(page["bibleValues"], ["douay-rheims", "clementine-vulgate"])
        self.assertEqual(page["busy"], "false")


class VisibleFailureTextTest(ReplayTest):
    """V6 §10 — the failure a reader SEES, not only the one it is told.

    `T.fail` writes a paragraph into the reading region and speaks the same
    words through the status channel. Only the second was ever projected, so
    every terminal-failure assertion in this file was really an assertion
    about the announcement — and a page that spoke without rendering, or
    rendered something other than what it said, would have passed all of them.
    """

    SPOKEN = {
        "null-index": "The catena index could not be read.",
        "null-index-cold": "The catena index could not be read.",
        "list-index": "The catena index could not be read.",
        "malformed-canon": "The catena index could not be read.",
        "scalar-index": "The catena index could not be read.",
        "null-bibles": "bibles.json lists no translations.",
    }

    def test_the_page_shows_the_failure_it_announces(self):
        for name, said in self.SPOKEN.items():
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["failureText"], said,
                                 "the visible paragraph is the failure")
                self.assertEqual(page["statusText"], said,
                                 "and the spoken line is the same words")

    def test_a_page_that_rendered_never_shows_a_failure_paragraph(self):
        for name in ("default", "mixed-collection", "finding-order",
                     "padded-verses", "unsafe-identities-opened"):
            with self.subTest(scenario=name):
                self.assertIsNone(self.page(name)["failureText"])


class V7TextPathRequestSinkTest(ReplayTest):
    """V7 §5 — an unvalidated `text_path` reaches no request.

    `chapterFragments` copied every raw property forward and then overwrote
    `text_path` only when the file's prefix AND the fragment's id could both
    be read. Where either could not, the record's own value survived the copy
    and `openFragment` handed it to `T.loadJSON`. The twelfth fragment of
    `V7_TEXT_PATH_FIXTURE` is that case exactly.

    Both scenarios OPEN EVERY FRAGMENT, because a request is only composed
    when a fragment is opened and a scenario that opens one proves nothing
    about the eleven beside it.
    """

    BOOTSTRAP = [
        "structure/catena/index.json",
        "bibles.json",
        "structure/paragraphs/index.json",
        "structure/catena/01-gen/001.json",
        "douay-rheims/chapters/Gen/1.json",
        "structure/paragraphs/douay-rheims/01-gen/001.json",
    ]

    # The eleven fragments whose id can be read, each addressed by the path
    # the page COMPOSED from the file's own prefix and the fragment's own id.
    # The twelfth names no identity, so it addresses nothing.
    COMPOSED = ["structure/catena/text/%s.json" % one for one in (
        "path-valid", "path-object", "path-array", "path-number", "path-null",
        "path-empty", "path-space", "path-traversal", "path-absolute",
        "path-encoded", "path-boolean")]

    def opened(self, name):
        return self.snapshot(name, "opened")

    def test_every_request_is_composed_and_none_is_carried(self):
        # The whole request journal, in order, pinned entire. Not "no `..`
        # appears": the exact set, so a request this page should not make
        # fails here whatever it looks like.
        self.assertEqual(self.opened("v7-text-path")["fetched"],
                         self.BOOTSTRAP + self.COMPOSED)

    def test_the_proven_v6_hole_makes_no_request_at_all(self):
        # A record id and an injected traversal, together — the combination
        # the V6 review proved reached the sink. Neither identity can be read,
        # so nothing is composed and nothing is carried: the fragment says it
        # carries no text file, which is the truth about it.
        fetched = self.opened("v7-text-path")["fetched"]
        self.assertNotIn("../../../etc/shadow.json", fetched)
        self.assertFalse([one for one in fetched if "etc/" in one or ".." in one],
                         fetched)
        page = self.opened("v7-text-path")
        self.assertEqual(
            page["fragmentTexts"][11],
            "This fragment carries no text file, so nothing of it can be shown.")

    def test_no_malformed_value_survives_projection_into_a_url(self):
        # Object, array, number, null, empty, whitespace, traversal, absolute,
        # percent-encoded and boolean, all standing on fragments whose ids ARE
        # readable. Every one of them is addressed by its own composed path,
        # so not one of the carried values reached a URL in any form —
        # stringified, encoded, or kept as a fallback.
        fetched = self.opened("v7-text-path")["fetched"]
        for carried in ("[object Object]", "%2e", "/etc/", "..", "shadow"):
            with self.subTest(carried=carried):
                self.assertFalse([one for one in fetched if carried in one],
                                 "%r reached the request sink" % carried)
        # And every request the chapter made was composed from a fragment's
        # own id, so no coerced form of a carried value can be hiding in one.
        for one in fetched[len(self.BOOTSTRAP):]:
            self.assertIn(one, self.COMPOSED, one)

    def test_the_whole_chapter_still_stands_and_terminates(self):
        # Refusing eleven carried paths costs no fragment its row, and the
        # route completes: a page that fails closed by falling over is not
        # failing closed.
        page = self.opened("v7-text-path")
        self.assertEqual(page["fragmentCount"], 12)
        self.assertEqual(page["tallyText"], "12 fragments held")
        self.assertEqual(page["statusWrites"],
                         ["Genesis 1, Douay-Rheims (Challoner), 12 fragments held."])
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["errorSections"], [])
        self.assertEqual(page["hash"], GEN1)
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["activeElement"], "body")
        self.assertIsNone(page["failureText"])

    def test_a_carried_path_is_taken_only_for_the_fragment_that_owns_it(self):
        # THE SAMPLE-CORPUS SHAPE. This spine states no `text_prefix`, so
        # nothing can be composed and the carried value is the only candidate
        # there is. It is accepted for exactly one of the ten fragments: the
        # one whose path is a relative JSON file of this data root's grammar
        # AND whose stem is that fragment's own validated id.
        #
        # `carried-other` is the discriminating case. Its path is sound,
        # relative, correctly formed and inside the text directory — and it
        # names somebody else's file, so it is not this fragment's text and is
        # not requested.
        self.assertEqual(
            self.opened("v7-text-path-no-prefix")["fetched"],
            self.BOOTSTRAP + ["structure/catena/text/carried-valid.json"])

    def test_the_nine_refused_carriers_say_they_carry_no_text(self):
        page = self.opened("v7-text-path-no-prefix")
        self.assertEqual(page["fragmentCount"], 10)
        said = "This fragment carries no text file, so nothing of it can be shown."
        self.assertEqual(page["fragmentTexts"][1:], [said] * 9)
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["tallyText"], "10 fragments held")


class V8TextNamespaceRequestSinkTest(ReplayTest):
    """V8 §1 — only the owned namespace reaches the request sink.

    The V7 review proved the hole at `fetch`, twice: a well-formed prefix of
    another directory composed `structure/paragraphs/<id>.json` and requested
    it, and a carried `structure/paragraphs/text/<same-id>.json` passed the
    same-stem check and fetched a real Sources text sharing that id. Both
    scenarios plant a body at the wrong-namespace address, so a leak here is a
    SERVED, RENDERED page — caught by the journal and by the words alike.

    Every scenario opens every fragment, so `fetched` afterwards is the
    complete set of requests the whole chapter can cause.
    """

    BOOTSTRAP = V7TextPathRequestSinkTest.BOOTSTRAP

    NO_TEXT = NO_TEXT_SAID
    REFUSED = REFUSED_SAID

    def opened(self, name):
        return self.snapshot(name, "opened")

    def test_a_wrong_namespace_prefix_composes_no_request(self):
        # The whole journal, pinned entire: three readable ids under a
        # `structure/paragraphs/` prefix compose nothing — not the carried
        # form, not a same-stem fallback, not a rewritten one.
        page = self.opened("v8-wrong-namespace-prefix")
        self.assertEqual(page["fetched"], self.BOOTSTRAP)

    def test_a_padded_right_namespace_prefix_is_not_repaired(self):
        # `"  structure/catena/text/  "` trimmed into validity composed a
        # VALID address, which is why the planted body sits at one: repair is
        # the page deciding what the record meant, and it makes no request.
        page = self.opened("v8-padded-prefix")
        self.assertEqual(page["fetched"], self.BOOTSTRAP)

    def test_a_carried_path_is_requested_only_inside_the_owned_namespace(self):
        # Ten same-looking tails; one owned namespace. The journal holds the
        # bootstrap and exactly one text request, and every post-bootstrap
        # request begins with the byte-exact namespace.
        page = self.opened("v8-wrong-namespace-carried")
        self.assertEqual(page["fetched"],
                         self.BOOTSTRAP + ["structure/catena/text/ns-valid.json"])
        for one in page["fetched"][len(self.BOOTSTRAP):]:
            self.assertTrue(one.startswith("structure/catena/text/"), one)

    def test_the_planted_wrong_namespace_body_is_never_shown(self):
        # The reviewer's reproduction rendered the other namespace's words.
        # Here the same words are planted and must appear NOWHERE: not as a
        # fragment's text, not as stale substitution, not as an absence claim.
        for name in ("v8-wrong-namespace-prefix", "v8-padded-prefix",
                     "v8-wrong-namespace-carried"):
            with self.subTest(scenario=name):
                page = self.opened(name)
                self.assertFalse(
                    [one for one in page["fetched"] if "PLANTED" in one])
                for said in page["fragmentTexts"]:
                    self.assertNotIn("PLANTED", said)
                    self.assertNotIn("not this route's text", said)

    def test_each_refused_fragment_states_its_own_terminal_claim(self):
        # A refused address is not a fragment lost and not a claim invented:
        # the row stands and the route terminates — busy released, status
        # written, no error section, no history write, nothing replaced. V10:
        # the two no-text states say different things, because they ARE
        # different things. A STATED wrong-namespace prefix is a refusal, and
        # the row says so; a carried path discarded under a spine that stated
        # NO prefix is genuine absence, and the absence sentence stands.
        prefixed = self.opened("v8-wrong-namespace-prefix")
        self.assertEqual(prefixed["fragmentCount"], 3)
        self.assertEqual(prefixed["fragmentTexts"], [self.REFUSED] * 3)
        self.assertEqual(prefixed["tallyText"], "3 fragments held")
        self.assertEqual(prefixed["statusWrites"],
                         ["Genesis 1, Douay-Rheims (Challoner), 3 fragments held."])
        carried = self.opened("v8-wrong-namespace-carried")
        self.assertEqual(carried["fragmentCount"], 10)
        self.assertEqual(carried["fragmentTexts"][1:], [self.NO_TEXT] * 9)
        for page in (prefixed, carried):
            self.assertEqual(page["busy"], "false")
            self.assertEqual(page["errorSections"], [])
            self.assertEqual(page["hash"], GEN1)
            self.assertEqual(page["hashWrites"], [])
            self.assertEqual(page["replaced"], [])
            self.assertIsNone(page["failureText"])


class V9ComposedPrefixFallbackClosureTest(ReplayTest):
    """V9 §1 — refusal opens no carried door; only genuine absence does.

    The V8 review proved the composed escape the primitive validators could
    not see: a prefix the file stated and the page REFUSED collapsed into the
    same '' as a prefix the file never stated, and the carried `text_path`
    door opened on that one ''. The reviewer's exact vector — a
    `structure/paragraphs/` prefix beside a valid carried
    `structure/catena/text/fallback-owned.json` — fetched the carried file
    and rendered its planted body as an ordinary success.

    Three states, each pinned at the production sinks: ABSENT may consult a
    validated carried path; PRESENT-VALID composes from the prefix and asks
    no fallback; PRESENT-INVALID is terminal — no request, no substitution,
    no stale body, cold, prewarmed, or late.
    """

    BOOTSTRAP = V7TextPathRequestSinkTest.BOOTSTRAP

    NO_TEXT = NO_TEXT_SAID
    REFUSED = REFUSED_SAID

    FALLBACK = "structure/catena/text/fallback-owned.json"

    # What walking to Genesis 2 costs, exactly: the spine, the Scripture,
    # and the paragraph layer — never a text body.
    GEN2_ARRIVAL = ["structure/catena/01-gen/002.json",
                    "douay-rheims/chapters/Gen/2.json",
                    "structure/paragraphs/douay-rheims/01-gen/002.json"]

    GEN1_SPOKEN = "Genesis 1, Douay-Rheims (Challoner), 1 fragment held."
    GEN2_SPOKEN = "Genesis 2, Douay-Rheims (Challoner), 1 fragment held."

    def opened(self, name):
        return self.snapshot(name, "opened")

    @staticmethod
    def journal(pairs):
        # The OWNED journal a snapshot must hold, entire: each request's
        # path beside the step that owns it, in sequence — V10, the V9
        # review: ownership was inferred from counts, and a substitute
        # request could hide inside an equal count. V11 adds the kind each
        # address asks for and what became of the request, so the packaged
        # journal reproduces the ownership claim without the harness.
        return request_journal(pairs)

    @classmethod
    def owned(cls, tail):
        return cls.journal(
            [(path, "start") for path in cls.BOOTSTRAP] + tail)

    def test_the_v8_escape_composes_no_request_cold(self):
        # THE CENTRAL ACCEPTANCE REGRESSION: the reviewer's exact vector and
        # its padded twin, from a cold page. The whole journal, pinned
        # entire: no refused-prefix request, no carried-fallback request, no
        # other text-body request.
        for name in ("v9-refused-prefix-carried", "v9-padded-prefix-carried"):
            with self.subTest(scenario=name):
                page = self.opened(name)
                self.assertEqual(page["fetched"], self.BOOTSTRAP)

    def test_the_planted_fallback_body_reaches_no_sink(self):
        # The reviewer's reproduction rendered the carried body. Here the
        # same body must appear NOWHERE: not in the journal, not as a
        # fragment's text, not as an absence claim.
        for name in ("v9-refused-prefix-carried", "v9-padded-prefix-carried"):
            with self.subTest(scenario=name):
                page = self.opened(name)
                self.assertFalse(
                    [one for one in page["fetched"] if "PLANTED" in one])
                for said in page["fragmentTexts"]:
                    self.assertNotIn("PLANTED", said)
                    self.assertNotIn("genuine absence", said)

    def test_the_refused_route_terminates_truthfully_cold(self):
        # Every terminal sink, enumerated and pinned to its EXPECTED value:
        # the row stands under its own identity and says its stated
        # reference was refused — not that it carries no file — the tally
        # counts it, the status is written once and STANDING, busy is
        # released, the route, history and history.state are the reader's
        # own, focus stayed on the body a cold arrival leaves it on, every
        # request is the bootstrap's, and nothing failed. V10: the V9 focus
        # assertion compared another scenario whose own focus was unpinned,
        # and the refused row still spoke the absence sentence.
        for name in ("v9-refused-prefix-carried", "v9-padded-prefix-carried"):
            with self.subTest(scenario=name):
                page = self.opened(name)
                self.assertEqual(page["fetched"], self.BOOTSTRAP)
                self.assertEqual(page["requests"], self.owned([]))
                self.assertEqual(page["fragmentCount"], 1)
                self.assertEqual(page["fragmentIds"], ["fallback-owned"])
                self.assertEqual(page["fragmentTexts"], [self.REFUSED])
                self.assertNotIn(self.NO_TEXT, page["fragmentTexts"])
                self.assertEqual(page["tallyText"], "1 fragment held")
                self.assertEqual(page["statusWrites"], [self.GEN1_SPOKEN])
                self.assertEqual(page["statusText"], self.GEN1_SPOKEN)
                self.assertEqual(page["busy"], "false")
                self.assertEqual(page["hash"], GEN1)
                self.assertEqual(page["hashWrites"], [])
                self.assertEqual(page["replaced"], [])
                self.assertEqual(page["replacedStates"], [])
                self.assertIsNone(page["historyState"])
                self.assertEqual(page["errorSections"], [])
                self.assertIsNone(page["failureText"])
                self.assertEqual(page["activeElement"], "body")

    def test_genuine_absence_still_opens_the_carried_door(self):
        # The door this closure must NOT close: no prefix stated, a valid
        # same-stem carried path — exactly one request, and the body shows.
        page = self.opened("v9-absent-prefix-carried")
        self.assertEqual(page["fetched"], self.BOOTSTRAP + [self.FALLBACK])
        self.assertEqual(page["requests"],
                         self.owned([(self.FALLBACK, "opened")]))
        self.assertEqual(len(page["fragmentTexts"]), 1)
        self.assertIn("PLANTED FALLBACK BODY", page["fragmentTexts"][0])
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["errorSections"], [])

    def test_a_valid_prefix_composes_its_own_address_and_asks_no_fallback(self):
        # PRESENT-VALID: the prefix determines text identity, so the one
        # request is the composed address — the carried address, planted and
        # valid, goes unasked — and the WHOLE terminal vector is pinned,
        # because the V9 review found this control asserted only request and
        # body. No refused sentence and no absence sentence stands anywhere
        # on a row whose reference was honoured.
        page = self.opened("v9-valid-prefix-carried")
        composed = "structure/catena/text/deeper/fallback-owned.json"
        self.assertEqual(page["fetched"], self.BOOTSTRAP + [composed])
        self.assertEqual(page["requests"], self.owned([(composed, "opened")]))
        self.assertEqual(page["fragmentCount"], 1)
        self.assertEqual(page["fragmentIds"], ["fallback-owned"])
        self.assertEqual(
            page["fragmentTexts"],
            ["Composed from the stated prefix and the fragment's own id."])
        self.assertNotIn(self.REFUSED, page["fragmentTexts"])
        self.assertNotIn(self.NO_TEXT, page["fragmentTexts"])
        self.assertEqual(page["tallyText"], "1 fragment held")
        self.assertEqual(page["statusWrites"], [self.GEN1_SPOKEN])
        self.assertEqual(page["statusText"], self.GEN1_SPOKEN)
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["hash"], GEN1)
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["replacedStates"], [])
        self.assertIsNone(page["historyState"])
        self.assertEqual(page["errorSections"], [])
        self.assertIsNone(page["failureText"])
        self.assertEqual(page["activeElement"], "body")

    def test_a_prewarmed_fallback_is_not_substituted_into_the_refused_route(self):
        # The cache is keyed by path, so a body already fetched under
        # genuine absence could be substituted WITHOUT a request. The
        # refused route must neither ask again nor reuse. V10: the WHOLE
        # final journal is pinned with each request's owner — the V9 filter
        # over a slice would have passed a substitute wrong-namespace
        # request — and the terminal vector is pinned entire: row identity,
        # refused sentence, announcement journal, history, history.state,
        # focus on the select the reader walked with, and no stale body.
        prewarmed = self.snapshot("v9-prewarmed-fallback", "prewarmed")
        self.assertEqual(prewarmed["fetched"], self.BOOTSTRAP + [self.FALLBACK])
        self.assertIn("PLANTED FALLBACK BODY", prewarmed["fragmentTexts"][0])
        page = self.snapshot("v9-prewarmed-fallback", "opened")
        self.assertEqual(page["fetched"],
                         self.BOOTSTRAP + [self.FALLBACK] + self.GEN2_ARRIVAL)
        self.assertEqual(
            page["requests"],
            self.owned([(self.FALLBACK, "prewarmed")]
                       + [(path, "refused") for path in self.GEN2_ARRIVAL]))
        self.assertEqual(page["fragmentCount"], 1)
        self.assertEqual(page["fragmentIds"], ["fallback-owned"])
        self.assertEqual(page["fragmentTexts"], [self.REFUSED])
        self.assertNotIn(self.NO_TEXT, page["fragmentTexts"])
        for said in page["fragmentTexts"]:
            self.assertNotIn("PLANTED", said)
        self.assertEqual(page["tallyText"], "1 fragment held")
        self.assertEqual(page["statusWrites"],
                         [self.GEN1_SPOKEN, self.GEN2_SPOKEN])
        self.assertEqual(page["statusText"], self.GEN2_SPOKEN)
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["hash"], GEN2)
        self.assertEqual(page["hashWrites"], [GEN2])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["replacedStates"], [])
        self.assertIsNone(page["historyState"])
        self.assertEqual(page["errorSections"], [])
        self.assertIsNone(page["failureText"])
        self.assertEqual(page["activeElement"], "chapter-select")

    def test_the_late_fallback_is_really_late(self):
        # Without this the late guard is vacuous: A's request really went
        # out before B was chosen, and it had NOT completed — the opened
        # fragment still stands at "Loading…".
        held = self.snapshot("v9-late-fallback", "a-held")
        asked = [one for one in held["fetched"]
                 if one.startswith("structure/catena/text/")]
        self.assertEqual(asked, [self.FALLBACK])
        self.assertEqual(held["fragmentTexts"][0], "Loading…")

    def expected_b_terminal(self, fallback="held"):
        # B'S WHOLE TERMINAL VECTOR, AS EXPECTED VALUES.
        #
        # `fallback` is what has become of A's parked request at the moment
        # of the snapshot — `held` before the release, `released` after. It
        # is the ONE fact the release is permitted to change, and pinning it
        # explicitly at both ends is how the proof shows the release really
        # happened while every other sink stood still.
        #
        # V11, the V10 review: the V10 lane pinned seventeen keys of which
        # only thirteen were guarded, so twenty-three of the thirty-six
        # guarded projections — the reference line, the selects, the
        # headings, the data states, the refusal and absence sinks, the
        # paragraph note, the counts, the verse numbers, the leads, the
        # blocked list, the voice and its labels, the step buttons, the
        # class vocabulary, the language attributes, the acknowledgements
        # and the author groups — were held by `before == after` alone and
        # could have been IDENTICALLY WRONG at both ends of the release.
        #
        # Every one of the thirty-six now has its expected value here, and
        # `test_every_guarded_field_has_an_expected_value` fails the moment
        # a field is added to the guard without being pinned here too. Four
        # more keys are pinned beside them — `fetched`, `requests`,
        # `replacedStates` and `historyState` — which the guard does not
        # carry and the proof needs.
        return {
            # --- the request sinks -------------------------------------
            "fetched": self.BOOTSTRAP + [self.FALLBACK] + self.GEN2_ARRIVAL,
            "requests": self.owned(
                [(self.FALLBACK, "a-held", fallback)]
                + [(path, "b-settled") for path in self.GEN2_ARRIVAL]),
            # --- the row, and what it says -----------------------------
            "fragmentCount": 1,
            "fragmentIds": ["fallback-owned"],
            "fragmentTexts": [self.REFUSED],
            "sectionHeadings": ["One fragment held here"],
            "dataStates": ["held"],
            "authorGroups": [{"author": "Author 1", "date": "301",
                              "count": "1 fragment", "open": True,
                              "hidden": False}],
            "acknowledgements": [],
            # --- the chapter around it ---------------------------------
            "referenceText": "Genesis 2",
            "tallyText": "1 fragment held",
            "chapterCounts": ["31 verses", "3 paragraphs"],
            "verseNumbers": [str(number) for number in range(1, 32)],
            "paragraphNote": ("Paragraphs: 2 are projected from the "
                              "witnesses that concur, and marked."),
            # --- the controls ------------------------------------------
            "selectValues": {"book": "Gen", "chapter": "2",
                             "bible": "douay-rheims"},
            "voice": "",
            "voiceLabels": ["Everything held", "The author’s own language"],
            "stepButtons": [False, False],
            # --- announcement, busy, route, focus ----------------------
            "statusWrites": [self.GEN1_SPOKEN, self.GEN2_SPOKEN],
            "statusText": self.GEN2_SPOKEN,
            "busy": "false",
            "hash": GEN2,
            "hashWrites": [GEN2],
            "replaced": [],
            "replacedStates": [],
            "historyState": None,
            "activeElement": "chapter-select",
            # --- every sink that must stay EMPTY -----------------------
            "errorSections": [],
            "failureText": None,
            "notices": [],
            "asideNotes": [],
            "leads": [],
            "blocked": [],
            "refusalCount": 0,
            "refusal": None,
            "absenceSummary": None,
            "absenceReasons": [],
            "absencePartials": [],
            # --- the rendered vocabulary -------------------------------
            # The whole class set, so a substituted, duplicated or dropped
            # node is visible as a vocabulary change rather than only as a
            # count. `fragment-text missing` is the refused row's own hook.
            "classes": [
                "author", "author-body", "author-count", "author-date",
                "author-fragments", "author-head", "author-name", "chain",
                "chain-column", "chapter", "chapter-body", "chapter-count",
                "chapter-head", "chapter-name", "fragment",
                "fragment-apparatus", "fragment-author", "fragment-body",
                "fragment-date", "fragment-extent", "fragment-head",
                "fragment-language", "fragment-length", "fragment-source",
                "fragment-text missing", "fragment-whole", "fragment-work",
                "paragraph-note", "passage", "passage-paragraph",
                "passage-paragraph projected", "section-heading", "sep",
                "verse", "verse-num"],
            "langAttributes": ["passage=en", "fragment-text missing=la"],
        }

    def test_every_guarded_field_has_an_expected_value(self):
        # THE COVERAGE PIN ITSELF. The V10 defect was not a wrong value; it
        # was twenty-three fields with no expected value at all, invisible
        # because the guard only compared. This asserts the arithmetic the
        # review had to do by hand, so a later lane cannot widen the guard
        # without widening the proof.
        guarded = set(GenuinelyLateStaleWorkTest.GUARDED)
        pinned = set(self.expected_b_terminal())
        self.assertEqual(len(guarded), 36)
        self.assertEqual(
            sorted(guarded - pinned), [],
            "guarded fields left to before/after equality alone")
        # And the four the proof adds beyond the guard are really beyond it.
        self.assertEqual(sorted(pinned - guarded),
                         ["fetched", "historyState", "replacedStates",
                          "requests"])

    def test_a_late_fallback_cannot_touch_the_refused_terminal_state(self):
        # B settled terminal with its rows open; A completes late. Every
        # guarded projection of the settled route is still compared entire,
        # and on top of the comparison — which cannot see a value
        # identically wrong on both sides — every material B sink is pinned
        # to its EXPECTED value before AND after the release: the owned
        # journal, the row under its own identity, the refused sentence, the
        # announcement journal and the standing status, tally, busy, route,
        # history and history.state, focus, and the error and failure sinks.
        # The release itself is pinned exactly: zero let go before, one
        # after, and the late request stays owned by A's own step.
        before = self.snapshot("v9-late-fallback", "b-opened")
        after = self.snapshot("v9-late-fallback", "a-late")
        for key in GenuinelyLateStaleWorkTest.GUARDED:
            self.assertEqual(after[key], before[key], f"{key} moved late")
        for label, snap, fallback in (("b-opened", before, "held"),
                                      ("a-late", after, "released")):
            with self.subTest(snapshot=label):
                for key, value in self.expected_b_terminal(fallback).items():
                    self.assertEqual(snap[key], value, f"{label}: {key}")
                self.assertNotIn(self.NO_TEXT, snap["fragmentTexts"])
                self.assertNotIn(UNESTABLISHED_SAID, snap["fragmentTexts"])
                for said in snap["fragmentTexts"]:
                    self.assertNotIn("PLANTED", said)
        # THE RELEASE, PINNED EXACTLY. Zero let go while B settled, one
        # afterwards — and the journal names WHICH request moved and to
        # what, so "something late happened" is not taken on the count.
        self.assertEqual(before["released"], 0)
        self.assertEqual(after["released"], 1)
        moved = [(one["seq"], one["path"], one["outcome"])
                 for one, then in zip(after["requests"], before["requests"])
                 if one != then]
        self.assertEqual(moved, [(6, self.FALLBACK, "released")])


class V9PrefixStateClassificationTest(unittest.TestCase):
    """V9 §1 — the model itself holds three states, not a truthy two.

    Driven through the exported production model, because the page's replay
    can only see the states the composition lets out. ABSENT means the spine
    record does not carry the `text_prefix` property; everything carried —
    null, a record, a list, a number, a flag, '', whitespace, the wrong
    namespace, traversal, an absolute path, a malformed encoding, the padded
    right namespace, the `textual/` boundary spoof — is a statement, and a
    statement that fails `textTrail` is REFUSED: terminal, fallback
    forbidden, and kept on the row as `text_refused`.
    """

    CARRIED = "structure/catena/text/fallback-owned.json"

    def classified(self):
        script = """
        const M = require(%r);
        const carried = %r;
        const base = () => ({
          sources: {"1": {author: "A", work: "W"}},
          fragments: [{id: "fallback-owned", source: "1",
                       text_path: carried}]});
        const row = (file) => {
          const one = M.chapterFragments(file)[0];
          return {path: one.text_path, refused: one.text_refused};
        };
        const valid = base();
        valid.text_prefix = "structure/catena/text/deeper/";
        const refusedValues = [
          null, {}, [], 5, true, "", "   ",
          "structure/paragraphs/",
          "  structure/catena/text/  ",
          "../structure/catena/text/",
          "/structure/catena/text/",
          "structure/catena/%%2e%%2e/text/",
          "structure/catena/textual/"];
        console.log(JSON.stringify({
          absent: row(base()),
          valid: row(valid),
          refused: refusedValues.map((value) => {
            const file = base();
            file.text_prefix = value;
            return row(file);
          })}));
        """ % (str(CATENA / "catena-model.js"), self.CARRIED)
        done = subprocess.run(["node", "-e", script],
                              capture_output=True, text=True, check=True)
        return json.loads(done.stdout)

    def test_absent_valid_and_refused_are_three_states(self):
        told = self.classified()
        # ABSENT: the carried door may open, and nothing was refused.
        self.assertEqual(told["absent"],
                         {"path": self.CARRIED, "refused": False})
        # PRESENT-VALID: composed from the statement, carried door unasked.
        self.assertEqual(
            told["valid"],
            {"path": "structure/catena/text/deeper/fallback-owned.json",
             "refused": False})
        # PRESENT-INVALID, thirteen ways: terminal, and the refusal kept.
        self.assertEqual(told["refused"],
                         [{"path": "", "refused": True}] * 13)


class V14ProjectionAuthorityBase(ReplayTest):
    """Shared vocabulary for the V14 lane."""

    V9 = V9ComposedPrefixFallbackClosureTest
    BOOTSTRAP = V9.BOOTSTRAP
    CARRIED = "structure/catena/text/fallback-owned.json"
    HELD_BODY = "PLANTED FALLBACK BODY"
    NO_FILE = ("This fragment carries no text file, so nothing of it can "
               "be shown.")
    UNAVAILABLE = "The commentary record did not load"
    UNAVAILABLE_SPOKEN = "commentary record unavailable"
    HELD_TALLY = ("1 fragment held · 1 work held, not renderable yet · "
                  "1 lead entry on the acquisition list")
    # EVERY CONSUMER OF A CHAPTER THIS PAGE HAS. V13 named six and folded the
    # tally into the rows; the V13 review required the tally recorded
    # separately, and `unfetched`, the request and the provenance line are
    # three more the six did not name. A consumer added later that does not
    # route through the projection fails the roster by the name that is
    # missing rather than passing quietly.
    # V15, the V14 review: `request` observed the row and its projection at
    # the ADDRESS decision and nothing afterwards, so the roster ended one
    # step before the step that writes the page. `transport` is the owner
    # object a request is created against, and `body` is the application
    # itself — asked as the row, at the sink, carrying the content.
    CONSUMERS = ("readability", "unfetched", "tally", "rows", "voices",
                 "blocked", "leads", "refusal", "request", "transport",
                 "body", "provenance")
    # The consumers a chapter reaches on an ordinary readable render. The
    # provenance line is drawn only where the reader asks for a translation
    # that is not held, so it is not on every page.
    RENDERED_CONSUMERS = ("readability", "unfetched", "tally", "rows",
                          "voices", "blocked", "leads", "refusal")

    def owned(self, tail=()):
        return request_journal(
            [(path, "start") for path in self.BOOTSTRAP] + list(tail))

    def asks(self, name, label="opened"):
        """Every address this page resolved through a projected row."""
        return self.snapshot(name, label)["asks"]

    def one_authority(self, name, label="opened"):
        """The single authoritative projection of a readable chapter."""
        page = self.snapshot(name, label)
        self.assertEqual(len(page["authoritativeRefs"]), 1,
                         "one raw chapter, one normalization")
        return page, page["authoritativeRefs"][0]


class V14RequestOwnershipTest(V14ProjectionAuthorityBase):
    """V14 §§10-13 — a request is owned by the row that asked for it.

    The V13 review found ownership reconstructed after the fact by taking the
    first projected row whose path string matched the request path. Two rows
    carrying one address are then one owner, and a late completion belongs to
    whichever row a search finds first.

    The page no longer hands a string to the transport. `fragmentText(row)`
    resolves the address THROUGH the row, and the model records the row
    object and the projection that made it at the moment the address is
    resolved. Ownership is an object association from the moment the request
    exists.
    """

    def test_a_row_no_projection_made_addresses_nothing(self):
        # The rule underneath the ownership record: only a row this model
        # projected may resolve an address at all. A copy of a row is not
        # that row.
        told = json.loads(subprocess.run(
            [NODE, "-e", (
                "const M = require(process.argv[1]);"
                "const asked = (row) => (typeof M.textAsked === 'function'"
                " ? M.textAsked(row) : 'NO ROW-BOUND ADDRESS');"
                "const owns = (row) => (typeof M.rowProjection === 'function'"
                " ? M.rowProjection(row) : null);"
                "const file = {fragments: [{id: 'fallback-owned',"
                " source: '1', text_path:"
                " 'structure/catena/text/fallback-owned.json'}],"
                " sources: {'1': {author: 'A', work: 'W'}}};"
                "const made = M.chapterProjection(file);"
                "const row = made.rows[0];"
                "const copy = Object.assign({}, row);"
                "console.log(JSON.stringify({"
                " owned: asked(row),"
                " copied: asked(copy),"
                " forged: asked({text_path: row.text_path}),"
                " scalar: asked('structure/catena/text/x.json'),"
                " nothing: asked(null),"
                " sameProjection: owns(row) === made,"
                " copyProjection: owns(copy) === made}));"),
             str(CATENA / "catena-model.js")],
            capture_output=True, text=True, check=True).stdout)
        self.assertEqual(told["owned"], self.CARRIED)
        self.assertEqual(told["copied"], "")
        self.assertEqual(told["forged"], "")
        self.assertEqual(told["scalar"], "")
        self.assertEqual(told["nothing"], "")
        self.assertTrue(told["sameProjection"])
        self.assertFalse(told["copyProjection"])

    def test_two_rows_carrying_one_address_are_two_owners(self):
        # V14 §11. Both fragments carry the same own id, so both resolve the
        # same carried address through genuine absence. One request is made
        # and the second row is answered from the cache — so the request
        # journal alone cannot say who asked, and the ask journal can.
        page = self.snapshot("v14-same-path-rows", "both")
        asked = page["asks"]
        self.assertEqual(len(asked), 2, "both rows asked")
        self.assertEqual([one["path"] for one in asked],
                         [self.CARRIED, self.CARRIED])
        self.assertNotEqual(asked[0]["row"], asked[1]["row"],
                            "a sibling row hijacked the first row's identity")
        self.assertEqual([one["step"] for one in asked], ["first", "both"])
        # ONE PROJECTION OWNS BOTH, and each ask says so by the row's own
        # binding rather than by the path they share.
        self.assertEqual(len(page["authoritativeRefs"]), 1)
        authority = page["authoritativeRefs"][0]
        for one in asked:
            self.assertEqual(one["projection"], authority)
            self.assertEqual(one["owned"], authority)
        # Both rows are this projection's rows, by identity.
        rows = page["projectionRowRefs"][str(authority)]
        self.assertEqual(sorted([one["row"] for one in asked]), sorted(rows))
        # One request, two bodies rendered: the second is the cache.
        self.assertEqual([one for one in page["fetched"]
                          if one == self.CARRIED], [self.CARRIED])
        self.assertEqual(page["fragmentTexts"],
                         [page["fragmentTexts"][0]] * 2)
        self.assertIn(self.HELD_BODY, page["fragmentTexts"][0])

    def test_the_journal_names_the_owner_by_object_and_not_by_path(self):
        rows = [one for one in self.snapshot("v14-same-path-rows",
                                             "both")["ownership"]
                if one["kind"] == "text"]
        self.assertEqual(len(rows), 1, "one request was made")
        self.assertEqual(rows[0]["path"], self.CARRIED)
        self.assertNotEqual(rows[0]["owner"], -1,
                            "the journal could not name an owning row")
        self.assertNotEqual(rows[0]["ownerProjection"], -1)
        self.assertEqual(rows[0]["projection"], "chapter-projection-1")

    def test_one_address_across_two_projections_stays_with_its_own(self):
        # V14 §12. Projection A's row and projection B's row carry the same
        # text address. The ask records the projection that made the asking
        # row, so the request does not collapse onto the address.
        page = self.snapshot("v14-two-projections-one-path", "opened")
        asked = page["asks"]
        self.assertEqual(len(asked), 2)
        self.assertEqual([one["path"] for one in asked],
                         [self.CARRIED, self.CARRIED])
        self.assertNotEqual(asked[0]["projection"], asked[1]["projection"],
                            "one address collapsed two projections into one")
        self.assertNotEqual(asked[0]["row"], asked[1]["row"])
        self.assertEqual(asked[0]["id"], "chapter-projection-1")
        self.assertEqual(asked[1]["id"], "chapter-projection-2")
        for one in asked:
            self.assertEqual(one["owned"], one["projection"],
                             "a row was attributed to a projection that did "
                             "not make it")

    def test_a_genuinely_late_completion_belongs_to_the_row_that_asked(self):
        # V14 §13. Projection A's row starts the request; the request is
        # held; projection B becomes the page carrying the SAME address; the
        # request is released. A's completion may not apply to B because the
        # strings match.
        asked = self.snapshot("v14-late-same-path", "asked")
        self.assertEqual(len(asked["asks"]), 1)
        first = asked["asks"][0]
        self.assertEqual(first["step"], "asked")
        self.assertEqual(first["path"], self.CARRIED)
        held = [one for one in asked["requests"]
                if one["path"] == self.CARRIED]
        self.assertEqual([one["outcome"] for one in held], ["held"])
        # B settles while A is still held, and asks as ITSELF.
        reopened = self.snapshot("v14-late-same-path", "reopened")
        self.assertEqual(len(reopened["asks"]), 2)
        second = reopened["asks"][1]
        self.assertNotEqual(second["row"], first["row"])
        self.assertNotEqual(second["projection"], first["projection"])
        self.assertEqual(second["owned"], second["projection"])
        self.assertEqual(second["step"], "reopened")
        # A's row and projection are unchanged by B settling — ownership is
        # recorded, not recomputed.
        self.assertEqual(reopened["asks"][0], first)
        late = self.snapshot("v14-late-same-path", "late")
        self.assertEqual(reopened["asks"][0], late["asks"][0])
        # V15, THE V14 REVIEW'S DECISIVE FINDING, AND THE OLD ORACLE THIS
        # REPLACES. What stood here was:
        #
        #     self.assertEqual([one["outcome"] for one in late["requests"]
        #                       if one["path"] == self.CARRIED], ["released"])
        #     self.assertIn(self.HELD_BODY, late["fragmentTexts"][0])
        #
        # ONE request for the address across two owners in two projections,
        # and B's rendered prose taken from it. Both of those are only
        # satisfiable if B never asked — if B subscribed to A's unresolved
        # promise and was handed the answer A's request was made for. The
        # oracle required the leak, which is why it was green over it.
        #
        # The correct expectation is that each owner has its own transport.
        # Both are parked here, because this scenario defers the address
        # rather than one ask of it, so both are released together; the
        # decisive sequence — A held while B settles — is
        # `v15-late-same-path`, below.
        released = [one for one in late["requests"]
                    if one["path"] == self.CARRIED]
        self.assertEqual([one["outcome"] for one in released],
                         ["released", "released"])
        self.assertEqual([one["phase"] for one in released],
                         ["asked", "reopened"])
        # And the page the reader is on is B's, showing B's own row.
        self.assertEqual(late["hash"], GEN2)
        self.assertEqual(late["fragmentCount"], 1)
        self.assertIn(self.HELD_BODY, late["fragmentTexts"][0])
        self.assertEqual(late["sourceLines"][0][:len("second-chapter")],
                         "second-chapter")
        self.assertEqual(late["busy"], "false")
        # The body B is showing was applied for B's row, off B's projection.
        wrote = late["applied"][-1]
        self.assertEqual(wrote["row"], second["row"])
        self.assertEqual(wrote["owned"], second["projection"])


class V15TransportOwnershipTest(V14ProjectionAuthorityBase):
    """V15 §§5-19 — ownership through pending transport, completion and body.

    The V14 review found ownership recorded at the ADDRESS decision and
    discarded one line later. `fragmentText(row)` resolved the address through
    the row and then entered a module-scope `Map` keyed on the path alone,
    holding the PROMISE. A second row carrying the same address did not ask:
    it found an unresolved promise there and joined it, so two owners became
    one and the answer the first row's request was made for was rendered under
    the second. The paths matched, and that was taken for ownership.

    A path string is not an owner and a promise keyed by one is not ownership.
    What is shared by path now is only ever an ANSWER — the promise is entered
    into `fragmentTexts` from inside its own settle handler, so nothing
    unresolved is ever reachable through it — and work in flight is held
    against the owner the model hands out for the row, `M.rowTransport(row)`:
    one frozen object per projected row, carrying the row, the projection that
    made it and the address it asks.

    The proofs here are ordered as the failure chain was: two rows in one turn
    are two transports; one owner's failure is not another's; a settled value
    may be shared and is still applied as the row that asked; and — the
    decisive one — A is held, B settles on the same address while A is still
    in the air, B renders the body B asked for, and A's late release changes
    nothing about B.
    """

    A_BODY = "PLANTED BODY A"
    B_BODY = "PLANTED BODY B"
    NOT_PUBLISHED = "The text of this fragment was not published beside the page."
    LATE = "v15-late-same-path"

    def text_requests(self, snap):
        return [one for one in snap["requests"] if one["path"] == self.CARRIED]

    def ownership(self, name, label):
        """The packaged ownership rows of one scenario's text requests."""
        return [one for one in self.snapshot(name, label)["ownership"]
                if one["kind"] == "text"]

    # ------------------------------------------------------- §§7, 15, 16

    def test_two_rows_in_one_turn_are_two_transports(self):
        # THE PENDING CASE. Both rows ask before either answer arrives, so
        # neither can be served from a value that has settled. Under V14
        # exactly one request left the page and both rows rendered its body.
        page = self.snapshot("v15-same-path-together", "both")
        asked = self.text_requests(page)
        self.assertEqual([one["outcome"] for one in asked],
                         ["completed", "completed"],
                         "one owner joined the other's request")
        # Two transports, two owner objects, two rows — one projection, one
        # address. The address is not what tells them apart.
        owners = page["transports"]
        self.assertEqual(len(owners), 2)
        self.assertNotEqual(owners[0]["owner"], owners[1]["owner"])
        self.assertNotEqual(owners[0]["row"], owners[1]["row"])
        self.assertEqual([one["path"] for one in owners],
                         [self.CARRIED, self.CARRIED])
        authority = page["authoritativeRefs"]
        self.assertEqual(len(authority), 1)
        for one in owners:
            self.assertEqual(one["held"], authority[0])
            self.assertEqual(one["owned"], authority[0])
            self.assertEqual(one["projection"], authority[0])
        # And each row rendered the answer ITS OWN request returned.
        self.assertEqual(len(page["fragmentTexts"]), 2)
        self.assertIn(self.A_BODY, page["fragmentTexts"][0])
        self.assertIn(self.B_BODY, page["fragmentTexts"][1])
        self.assertNotIn(self.B_BODY, page["fragmentTexts"][0])
        self.assertNotIn(self.A_BODY, page["fragmentTexts"][1])

    def test_one_owners_failure_is_not_another_owners(self):
        # §21. The first ask of the shared address is answered 404 and the
        # second a document, in the same turn. A rejection held by path is a
        # rejection every waiting row receives, and the row that receives it
        # reports a failure against a request nobody made on its behalf.
        page = self.snapshot("v15-same-path-one-fails", "both")
        self.assertEqual(len(self.text_requests(page)), 2)
        self.assertEqual(page["fragmentTexts"][0], self.NOT_PUBLISHED)
        self.assertIn(self.B_BODY, page["fragmentTexts"][1])
        # The failing row's body is applied too, and owned exactly as a
        # fulfilled one is: a reported failure is a body.
        wrote = page["applied"]
        self.assertEqual(len(wrote), 2)
        rows = page["projectionRowRefs"][str(page["authoritativeRefs"][0])]
        for one in wrote:
            self.assertIn(one["row"], rows)
            self.assertEqual(one["owned"], page["authoritativeRefs"][0])
        # V16 EXTENDS THIS. What V15 could not ask is whether the failure —
        # or a rejected promise, or anything intermediate — reached the
        # SHARED CACHE, because nothing could look at it. The same sequence
        # with the path watched is
        # `V16PublicationAtomicityTest.test_no_failure_and_no_intermediate_value_is_published`.

    # ------------------------------------------------------------ §19

    def test_a_settled_value_is_shared_and_applied_as_the_row_that_asked(self):
        # THE SAFE-SHARING RULE, PROVED SEPARATELY. Row one asks and settles;
        # row two asks afterwards, is answered from the value that settled and
        # makes no request — and applies it AS ITSELF, off its own row, with
        # its own ownership recorded at the application.
        first = self.snapshot("v15-settled-then-shared", "first")
        self.assertEqual(len(self.text_requests(first)), 1)
        self.assertIn(self.A_BODY, first["fragmentTexts"][0])
        self.assertEqual(first["fragmentTexts"][1], "Loading…")
        page = self.snapshot("v15-settled-then-shared", "second")
        # NO SECOND REQUEST: the sharing is real, and it is by value.
        self.assertEqual(len(self.text_requests(page)), 1)
        # Both rows show the settled answer — the one document that path
        # answered — and the second row never sees the body its own turn of
        # the scenario would have served, because it never asked.
        self.assertIn(self.A_BODY, page["fragmentTexts"][0])
        self.assertIn(self.A_BODY, page["fragmentTexts"][1])
        self.assertNotIn(self.B_BODY, page["fragmentTexts"][1])
        # Two transports all the same: sharing a VALUE is not sharing an
        # owner, and the second row's ownership is recorded at its own ask.
        owners = page["transports"]
        self.assertEqual(len(owners), 2)
        self.assertNotEqual(owners[0]["owner"], owners[1]["owner"])
        # Two applications, each owned by the row that made it, and the value
        # applied is frozen — what one row's request settled may carry
        # nothing of that row into the next.
        wrote = page["applied"]
        self.assertEqual(len(wrote), 2)
        self.assertNotEqual(wrote[0]["row"], wrote[1]["row"])
        self.assertEqual(wrote[0]["row"], owners[0]["row"])
        self.assertEqual(wrote[1]["row"], owners[1]["row"])
        for one in wrote:
            self.assertEqual(one["owned"], page["authoritativeRefs"][0])
            self.assertTrue(one["frozen"], "a shared value is not immutable")
        # NOTHING UNRESOLVED IS EVER SHARED BY PATH. While the first row's
        # request was still in the air the second row could not have found it:
        # the held case proves that directly, below.

    # ---------------------------------------------------- §§9, 10, 17, 18

    #: B's terminal state, pinned value by value BEFORE A is released. Every
    #: field `GenuinelyLateStaleWorkTest.GUARDED` names is here, so the late
    #: release is compared against expected values and not only against
    #: whatever the earlier snapshot happened to hold.
    B_TERMINAL = {
        "hash": GEN2,
        "hashWrites": [GEN2],
        "replaced": [],
        "replacedStates": [],
        "historyState": None,
        "statusWrites": ["Genesis 1, Douay-Rheims (Challoner), 2 fragments held.",
                         "Genesis 2, Douay-Rheims (Challoner), 1 fragment held."],
        "statusText": "Genesis 2, Douay-Rheims (Challoner), 1 fragment held.",
        "tallyText": "1 fragment held",
        "busy": "false",
        "activeElement": "chapter-select",
        "referenceText": "Genesis 2",
        "selectValues": {"book": "Gen", "chapter": "2", "bible": "douay-rheims"},
        "fragmentCount": 1,
        "fragmentIds": ["fallback-owned"],
        "fragmentTexts": [
            "PLANTED BODY B — the answer the row in projection B asked for."],
        "errorSections": [],
        "sectionHeadings": ["One fragment held here"],
        "failureText": None,
        "notices": [],
        "dataStates": ["held"],
        "asideNotes": [],
        "refusalCount": 0,
        "refusal": None,
        "absenceSummary": None,
        "absenceReasons": [],
        "absencePartials": [],
        "paragraphNote": ("Paragraphs: 2 are projected from the witnesses "
                          "that concur, and marked."),
        "chapterCounts": ["31 verses", "3 paragraphs"],
        "verseNumbers": [str(number) for number in range(1, 32)],
        "leads": [],
        "blocked": [],
        "voice": "",
        "voiceLabels": ["Everything held", "The author’s own language"],
        "stepButtons": [False, False],
        "classes": [
            "author", "author-body", "author-count", "author-date",
            "author-fragments", "author-head", "author-name", "chain",
            "chain-column", "chapter", "chapter-body", "chapter-count",
            "chapter-head", "chapter-name", "fragment", "fragment-apparatus",
            "fragment-author", "fragment-body", "fragment-date",
            "fragment-extent", "fragment-head", "fragment-language",
            "fragment-length", "fragment-source", "fragment-text",
            "fragment-whole", "fragment-work", "paragraph-note", "passage",
            "passage-paragraph", "passage-paragraph projected",
            "section-heading", "sep", "verse", "verse-num"],
        "langAttributes": ["passage=en", "fragment-text=la"],
        "acknowledgements": [],
        "authorGroups": [{"author": "Author 1", "date": "301",
                          "count": "1 fragment", "open": True,
                          "hidden": False}],
    }

    def test_every_guarded_field_of_b_is_pinned(self):
        # The same coverage rule the V9 terminal vector carries: a field left
        # to before/after equality alone is a field that could move together
        # at both ends and be called unchanged.
        guarded = set(GenuinelyLateStaleWorkTest.GUARDED)
        self.assertEqual(len(guarded), 36)
        self.assertEqual(sorted(guarded - set(self.B_TERMINAL)), [])

    def test_b_settles_independently_while_a_is_still_held(self):
        # ★ THE DECISIVE V15 SEQUENCE ★  §§9-10.
        #
        # A asks under chapter 1 and its transport is HELD. The reader moves
        # to chapter 2, whose row carries the same address. B asks — and
        # settles, with A's request still in the air — and renders the body
        # B's own request returned. Under V14 there is no second request at
        # all: B joins A's promise, stands at `Loading…`, and is filled with
        # A's body when A is released.
        held = self.snapshot(self.LATE, "a-held")
        first = self.text_requests(held)
        self.assertEqual([one["outcome"] for one in first], ["held"])
        self.assertEqual(first[0]["phase"], "a-held")
        self.assertEqual(held["fragmentTexts"], ["Loading…", "Loading…"],
                         "A's page may show nothing while A is held")
        self.assertEqual(held["applied"], [], "nothing was written yet")

        page = self.snapshot(self.LATE, "b-settled")
        both = self.text_requests(page)
        # TWO transports on ONE address, and A's is STILL HELD.
        self.assertEqual([one["outcome"] for one in both],
                         ["held", "completed"],
                         "B did not settle while A was held")
        self.assertEqual([one["phase"] for one in both], ["a-held", "b-settled"])
        # B rendered the answer B asked for, and never A's.
        self.assertEqual(len(page["fragmentTexts"]), 1)
        self.assertIn(self.B_BODY, page["fragmentTexts"][0])
        self.assertNotIn(self.A_BODY, page["fragmentTexts"][0])
        # ONE application so far, and it is B's: B's row, B's projection.
        self.assertEqual(len(page["applied"]), 1)
        wrote = page["applied"][0]
        self.assertIn(self.B_BODY, wrote["body"])
        owners = page["transports"]
        self.assertEqual(len(owners), 2)
        self.assertNotEqual(owners[0]["owner"], owners[1]["owner"])
        self.assertNotEqual(owners[0]["row"], owners[1]["row"])
        self.assertNotEqual(owners[0]["held"], owners[1]["held"])
        self.assertEqual(wrote["row"], owners[1]["row"])
        self.assertEqual(wrote["owned"], owners[1]["held"])
        self.assertEqual(wrote["id"], "chapter-projection-2")
        # THE PATH-MATCH ANSWER IS THE WRONG ONE, and the journal says so in
        # the same row: searching the rows for a matching address names
        # chapter one's projection for a request chapter two's row made.
        tail = self.ownership(self.LATE, "b-settled")[-1]
        self.assertEqual(tail["path"], self.CARRIED)
        self.assertEqual(tail["projection"], "chapter-projection-2")
        self.assertEqual(tail["byPath"], "chapter-projection-1")
        self.assertEqual(tail["route"], GEN2)
        # And B's terminal state is exactly this, before anything is released.
        self.assert_b_terminal(page)

    def test_a_late_release_cannot_change_anything_of_b(self):
        # §§17-18. A completes after B has settled and after the route it was
        # made under has been replaced. It may change nothing a reader can
        # see, nothing the page recorded, and nothing about ownership.
        before = self.snapshot(self.LATE, "b-settled")
        after = self.snapshot(self.LATE, "a-late")
        for key in GenuinelyLateStaleWorkTest.GUARDED:
            with self.subTest(field=key):
                self.assertEqual(after[key], before[key], key + " moved late")
        self.assert_b_terminal(after)
        # The late release really happened, and it is the ONLY thing that
        # moved in the whole journal.
        self.assertEqual(before["released"], 0)
        self.assertEqual(after["released"], 1)
        self.assertEqual(after["fetched"], before["fetched"])
        moved = [(one["seq"], one["path"], one["outcome"])
                 for one, then in zip(after["requests"], before["requests"])
                 if one != then]
        self.assertEqual(moved, [(6, self.CARRIED, "released")])
        # NO SECOND APPLICATION. A's completion wrote nothing, so it is not
        # in the application roster at all — the containment check refuses it
        # before ownership is even recorded.
        self.assertEqual(after["applied"], before["applied"])
        self.assertEqual(len(after["applied"]), 1)
        # A's own ask and transport are unchanged: ownership is recorded, not
        # recomputed when the answer arrives.
        self.assertEqual(after["asks"], before["asks"])
        self.assertEqual(after["transports"], before["transports"])

    def test_the_distinguishable_bodies_are_not_doing_the_work(self):
        # NON-VACUITY THE OTHER WAY. The same sequence with ONE document at
        # the address moves the route, the row and the projection exactly as
        # before, so the discrimination above is the ownership and not the
        # two planted bodies.
        page = self.snapshot("v15-late-same-path-control", "b-settled")
        self.assertEqual([one["outcome"] for one in self.text_requests(page)],
                         ["held", "completed"])
        self.assertIn(self.B_BODY, page["fragmentTexts"][0])
        late = self.snapshot("v15-late-same-path-control", "a-late")
        self.assertEqual(late["fragmentTexts"], page["fragmentTexts"])
        self.assertEqual(late["applied"], page["applied"])
        self.assertEqual(late["released"], 1)

    def assert_b_terminal(self, snap):
        for key, value in self.B_TERMINAL.items():
            with self.subTest(field=key):
                self.assertEqual(snap[key], value)

    # ------------------------------------------------------------ §§12-13

    def test_the_transport_owner_carries_the_row_and_its_projection(self):
        # §15. The request is created against an object identity, and that
        # object holds the row that initiated it and the projection that made
        # the row. Nothing downstream searches rows for a matching path.
        page, authority = self.one_authority("v15-same-path-together", "both")
        rows = page["projectionRowRefs"][str(authority)]
        for one in page["transports"]:
            self.assertIn(one["row"], rows)
            self.assertEqual(one["held"], authority)
            self.assertEqual(one["owned"], authority)
            self.assertNotEqual(one["owner"], one["row"],
                                "the owner is an object of its own")
        # One owner per row, for the life of the row: the two rows here ask
        # once each, and the two owner objects are distinct.
        self.assertEqual(len({one["owner"] for one in page["transports"]}), 2)

    # V16, THE V15 REVIEW. The direct model probe that stood here is now
    # `V16CompletionEnvelopeTest`, and it is there rather than here because
    # what it asks changed. V15's copy asserted
    # `M.bodyAsked(row, {text: 'x'})` to be TRUE and called that ownership:
    # the row was real, the content was a literal nobody had asked for, and
    # the boundary said yes. The review named that assertion by name. The
    # transport half of the probe is unchanged and travels with it, beside
    # the completion-envelope cases V15 had no shape for.

    # ------------------------------------------------------------ §14

    def test_an_unreadable_spine_is_one_substitute_however_often_it_is_asked(self):
        # §14, the wrapper ambiguity. The page substitutes a record of its own
        # for a spine that is a document and not a spine. Under V14 that
        # record was a fresh literal on every ask, so walking away from an
        # unreadable chapter and back made a NEW authority over it and the
        # projection count climbed with the reader's steps.
        away = self.snapshot("v15-unreadable-rerendered", "away")
        back = self.snapshot("v15-unreadable-rerendered", "back")
        self.assertEqual(away["projectionPasses"], back["projectionPasses"])
        self.assertEqual(away["authoritativeRefs"], back["authoritativeRefs"])
        self.assertEqual(len(back["authoritativeRefs"]), 2,
                         "one unreadable chapter and one readable one")
        # The unreadable chapter still says so, and says it the same way both
        # times it is rendered — the substitute being reused is not the
        # chapter quietly rendering as something else.
        start = self.snapshot("v15-unreadable-rerendered", "start")
        self.assertEqual(back["fragmentCount"], 0)
        for key in ("fragmentCount", "fragmentIds", "fragmentTexts",
                    "sectionHeadings", "tallyText", "notices", "asideNotes",
                    "errorSections", "dataStates", "refusalCount", "leads",
                    "blocked", "statusText"):
            with self.subTest(field=key):
                self.assertEqual(back[key], start[key])


class V16PublicationBase(V14ProjectionAuthorityBase):
    """Shared vocabulary for the V16 lane.

    The V15 review's exact next action, in the order it stated it: normalize
    the payload ONCE into an owner-independent immutable scalar record;
    publish it only after it is finished, never the initiating owner's
    pending promise; prove that with an inside-settlement and reentrant
    oracle and with mutation-before-a-later-owner; carry a per-caller
    completion envelope holding the exact transport owner to the body sink
    and require that owner at application; record the application after the
    write; add the missing provenance identity assertion; and correct the
    observation prose.
    """

    #: The finalized record's key set, deterministic and in order. Pinned
    #: here as a literal AND asked of the model itself in
    #: `V16CompletionEnvelopeTest`, so this list is the reviewed schema and
    #: not a transcription of whatever the model happens to emit.
    SCHEMA = ["present", "unreadable", "text", "basis", "date_basis",
              "acknowledgement", "acknowledgement_broken"]
    NOT_PUBLISHED = "The text of this fragment was not published beside the page."
    A_BODY = "PLANTED BODY A"
    B_BODY = "PLANTED BODY B"


class V16CompletionEnvelopeTest(V16PublicationBase):
    """V16 §D — the answer stops travelling alone.

    The V15 review's boundary finding, stated exactly: `M.bodyAsked(row,
    content)` authorized ANY content whenever `row` occurred in `rowOwners`.
    It received no transport owner, no completion token, no promise and no
    generation, and it did not compare the content with the request made for
    that row. An actual B row therefore accepted arbitrary A content at the
    sink. The association held in production only because one closure
    happened to carry both halves — and the review's own words for the
    committed oracle were that "the direct test intentionally accepts
    `{text: "x"}` without any owned completion".

    A settled transport is now sealed into one frozen envelope carrying the
    exact `rowTransport` owner beside the value, minted only against an owner
    this file is holding for that owner's own row and only around content
    this file itself finalized. The envelope — not the value — reaches the
    body, and `bodyAsked` makes three exact-object comparisons: that the
    envelope is one this file sealed, that its owner is the transport held
    for this very row, and that the owner's projection is the projection that
    made the row. None of them is a path, a row id, a projection id string,
    the current rows or the current route.
    """

    #: The model probe, run once. Every entry point is reached through
    #: `call`, so an export the parent does not have answers
    #: 'NO SUCH EXPORT' instead of taking the whole probe down — a missing
    #: export and a wrong answer are two different readings and the
    #: discrimination record has to be able to tell them apart.
    PROBE = r"""
    'use strict';
    const M = require(process.argv[1]);
    const raw = JSON.parse(process.argv[2]);
    const has = (name) => typeof M[name] === 'function';
    const call = (name, ...args) =>
      (has(name) ? M[name].apply(M, args) : 'NO SUCH EXPORT');
    const made = M.chapterProjection(raw);
    const rowA = made.rows[0];
    const rowB = made.rows[1];
    const ownerA = M.rowTransport(rowA);
    const ownerB = M.rowTransport(rowB);
    const forgedOwner = Object.assign({}, ownerA);
    const contentA = call('textPayload', { text: 'THE WORDS',
                                           basis: 'AN EXTENT' });
    const doneA = call('textCompleted', ownerA, contentA);
    const doneB = call('textCompleted', ownerB, contentA);
    const failedA = call('textFailed', ownerA, new Error('the network failed'));
    const literal = { owner: ownerA, failed: false, content: contentA,
                      error: null };
    const keys = contentA && typeof contentA === 'object'
      ? Object.keys(contentA) : [];
    const mutated = (() => {
      if (!contentA || typeof contentA !== 'object') return null;
      const before = contentA.text;
      const tried = (change) => {
        try { change(); return false; } catch (error) { return true; }
      };
      return {
        assignThrew: tried(() => { contentA.text = 'FORGED'; }),
        addThrew: tried(() => { contentA.extra = 'FORGED'; }),
        deleteThrew: tried(() => { delete contentA.basis; }),
        protoThrew: tried(
          () => Object.setPrototypeOf(contentA, { text: 'FORGED ABOVE' })),
        held: contentA.text === before,
        keptBasis: contentA.basis === 'AN EXTENT',
        noExtra: contentA.extra === undefined,
        stillNullPrototype: Object.getPrototypeOf(contentA) === null
      };
    })();
    console.log(JSON.stringify({
      twoRows: made.rows.length,
      ownersDiffer: ownerA !== ownerB,
      onePathTwoOwners: ownerA.path === ownerB.path,
      contentFrozen: Object.isFrozen(contentA),
      contentPrototype: Object.getPrototypeOf(contentA) === null ? 'null'
        : Object.getPrototypeOf(contentA) === Object.prototype
          ? 'Object' : 'other',
      contentKeys: keys,
      schema: Array.isArray(M.TEXT_SCHEMA)
        ? M.TEXT_SCHEMA.slice() : 'NO SUCH EXPORT',
      schemaFrozen: Array.isArray(M.TEXT_SCHEMA)
        ? Object.isFrozen(M.TEXT_SCHEMA) : 'NO SUCH EXPORT',
      contentScalars: keys.every((n) => typeof contentA[n] === 'string'
        || typeof contentA[n] === 'boolean'),
      mutation: mutated,
      sealedOwn: doneA !== null && doneA !== 'NO SUCH EXPORT',
      sealedCarriesOwner: doneA ? doneA.owner === ownerA : null,
      sealedCarriesContent: doneA ? doneA.content === contentA : null,
      sealedFrozen: doneA ? Object.isFrozen(doneA) : null,
      forgedOwnerSealsNothing: call('textCompleted', forgedOwner, contentA),
      unmintedContentSealsNothing:
        call('textCompleted', ownerA, { present: true, text: 'x' }),
      failureSealed: failedA !== null && failedA !== 'NO SUCH EXPORT',
      failureCarriesNoContent: failedA ? failedA.content === null : null,
      forgedOwnerFailsNothing: call('textFailed', forgedOwner,
                                    new Error('x')),
      noTextIsMinted: has('textCompleted') && M.NO_TEXT !== undefined
        ? M.textCompleted(ownerA, M.NO_TEXT) !== null : 'NO SUCH EXPORT',
      wroteOwn: call('bodyAsked', rowA, doneA),
      wroteLiteral: call('bodyAsked', rowA, { text: 'x' }),
      wroteShapedLiteral: call('bodyAsked', rowA, literal),
      wroteBareContent: call('bodyAsked', rowA, contentA),
      wroteForeign: call('bodyAsked', rowB, doneA),
      wroteRebound: call('bodyAsked', rowB, doneB),
      reboundSameValue: doneB ? doneB.content === contentA : null,
      reboundOwnOwner: doneB
        ? doneB.owner === ownerB && doneB.owner !== ownerA : null,
      wroteFailure: call('bodyAsked', rowA, failedA),
      appliedConfirmed: call('bodyApplied', rowA, doneA, true),
      appliedUnconfirmed: call('bodyApplied', rowA, doneA, false),
      appliedTruthy: call('bodyApplied', rowA, doneA, 'true'),
      appliedForeign: call('bodyApplied', rowB, doneA, true)
    }));
    """

    @classmethod
    def told(cls):
        if not hasattr(cls, "_told"):
            cls._told = json.loads(subprocess.run(
                [NODE, "-e", cls.PROBE, str(CATENA / "catena-model.js"),
                 json.dumps(V14_SAME_PATH_SPINE)],
                capture_output=True, text=True, check=True).stdout)
        return cls._told

    def test_two_same_path_rows_are_two_owners_and_the_content_is_neither(self):
        told = self.told()
        self.assertEqual(told["twoRows"], 2)
        self.assertTrue(told["ownersDiffer"])
        self.assertTrue(told["onePathTwoOwners"],
                        "the fixture stopped being a same-path fixture")

    def test_the_finalized_content_is_the_models_own_deterministic_schema(self):
        # The key list this lane reviews, pinned as a literal AND taken from
        # the model, so the two are asserted against each other rather than
        # one being a transcription of the other.
        told = self.told()
        self.assertEqual(told["schema"], self.SCHEMA)
        self.assertIs(told["schemaFrozen"], True)
        self.assertEqual(told["contentKeys"], self.SCHEMA)
        self.assertIs(told["contentFrozen"], True)
        self.assertEqual(told["contentPrototype"], "null")
        self.assertIs(told["contentScalars"], True)

    def test_the_finalized_content_cannot_be_changed(self):
        # Every way there is to change a record, and what the value says
        # afterwards. The assignment, the addition, the deletion and the
        # reparenting all throw, and each value is what it was — including
        # the prototype, which is the member the V15 defect travelled
        # through.
        said = self.told()["mutation"]
        for what in ("assignThrew", "addThrew", "deleteThrew", "protoThrew"):
            with self.subTest(attempt=what):
                self.assertIs(said[what], True, what + " did not throw")
        for what in ("held", "keptBasis", "noExtra", "stillNullPrototype"):
            with self.subTest(value=what):
                self.assertIs(said[what], True, what + " moved")

    def test_a_row_no_projection_made_owns_no_transport_and_writes_nothing(self):
        # THE V15 FAIL-CLOSED RULE, one and two steps later. A row this file
        # did not project creates no transport at all, and a body may not be
        # applied for it. Kept from V15 unchanged in what it asks about the
        # TRANSPORT; the content half of it is asked below, where V16 moved
        # it.
        told = json.loads(subprocess.run(
            [NODE, "-e", """
            const M = require(process.argv[1]);
            const raw = JSON.parse(process.argv[2]);
            const made = M.chapterProjection(raw);
            const row = made.rows[0];
            const copy = Object.assign({}, row);
            const forged = { text_path: 'structure/catena/text/forged.json' };
            const owner = M.rowTransport(row);
            console.log(JSON.stringify({
              owned: owner !== null,
              same: M.rowTransport(row) === owner,
              carries: owner && owner.row === row
                       && owner.projection === made
                       && owner.path === row.text_path,
              frozen: owner !== null && Object.isFrozen(owner),
              copy: M.rowTransport(copy),
              forged: M.rowTransport(forged),
              scalar: M.rowTransport('x'),
              nothing: M.rowTransport(null),
              wroteCopy: M.bodyAsked(copy, { text: 'x' }),
              wroteForged: M.bodyAsked(forged, { text: 'x' }),
              wroteScalar: M.bodyAsked(7, { text: 'x' })
            }));
            """, str(CATENA / "catena-model.js"),
             json.dumps(V14_SAME_PATH_SPINE)],
            capture_output=True, text=True, check=True).stdout)
        self.assertTrue(told["owned"])
        self.assertTrue(told["same"], "one owner per row, held against it")
        self.assertTrue(told["carries"])
        self.assertTrue(told["frozen"])
        self.assertIsNone(told["copy"])
        self.assertIsNone(told["forged"])
        self.assertIsNone(told["scalar"])
        self.assertIsNone(told["nothing"])
        self.assertFalse(told["wroteCopy"])
        self.assertFalse(told["wroteForged"])
        self.assertFalse(told["wroteScalar"])

    def test_an_actual_row_no_longer_authorizes_arbitrary_content(self):
        # ★ THE CORRECTION THE V15 REVIEW NAMED BY NAME ★
        #
        # V15's committed probe asserted `M.bodyAsked(row, {text: 'x'})` to
        # be TRUE and called that ownership. It was not ownership: the row
        # was real, the content was a literal nobody had asked for, and the
        # boundary said yes. It says no now, and so does every other shape
        # that is not this row's own sealed completion — a bare finalized
        # value, an object literal wearing the envelope's four fields, and a
        # completion sealed for the other row.
        told = self.told()
        self.assertIs(told["wroteOwn"], True,
                      "this row's own sealed completion must be accepted")
        self.assertIs(told["wroteLiteral"], False,
                      "an actual row still authorizes an arbitrary literal")
        self.assertIs(told["wroteShapedLiteral"], False,
                      "a forged envelope of the right shape was accepted")
        self.assertIs(told["wroteBareContent"], False,
                      "content with no owner was accepted")
        self.assertIs(told["wroteForeign"], False,
                      "row B accepted a completion sealed for row A")

    def test_the_envelope_can_be_minted_from_neither_half_alone(self):
        # FAIL-CLOSED ON BOTH INPUTS, one step later than `rowTransport`. A
        # copy of an owner is not that owner; a record this file did not
        # finalize is not content. Neither can be supplied from outside, so
        # a forged envelope cannot be assembled at all.
        told = self.told()
        self.assertTrue(told["sealedOwn"])
        self.assertIs(told["sealedCarriesOwner"], True)
        self.assertIs(told["sealedCarriesContent"], True)
        self.assertIs(told["sealedFrozen"], True)
        self.assertIsNone(told["forgedOwnerSealsNothing"],
                          "a forged owner sealed a completion")
        self.assertIsNone(told["unmintedContentSealsNothing"],
                          "content this file never made was sealed")
        self.assertIsNone(told["forgedOwnerFailsNothing"])
        self.assertIs(told["noTextIsMinted"], True,
                      "NO_TEXT is not one of this file's own values")

    def test_a_reported_failure_is_a_body_and_is_owned_as_one(self):
        told = self.told()
        self.assertTrue(told["failureSealed"])
        self.assertIs(told["failureCarriesNoContent"], True)
        self.assertIs(told["wroteFailure"], True)

    def test_a_finished_value_rebinds_to_the_owner_that_reuses_it(self):
        # THE SAME-PATH FULFILLED-CACHE REBINDING, at the model boundary. The
        # value A's request produced is owner-independent, so B may have it —
        # through B'S OWN envelope. A's owner never crosses: the envelope B
        # holds carries B's owner, the value inside it is the very object A
        # was given, and the boundary accepts B's envelope for B's row and
        # A's for A's.
        told = self.told()
        self.assertIs(told["wroteRebound"], True)
        self.assertIs(told["reboundSameValue"], True,
                      "the cached value was copied instead of shared")
        self.assertIs(told["reboundOwnOwner"], True,
                      "the second owner inherited the first owner's envelope")

    def test_the_journal_entry_follows_a_confirmed_write_and_nothing_else(self):
        # §E AT THE MODEL BOUNDARY. `wrote` is the page's own answer to
        # whether the write landed, and only `true` is an answer: `false` and
        # a truthy string are both refused, so an unconfirmed application
        # cannot become a journal entry by being merely plausible.
        told = self.told()
        self.assertIs(told["appliedConfirmed"], True)
        self.assertIs(told["appliedUnconfirmed"], False)
        self.assertIs(told["appliedTruthy"], False,
                      "a truthy value passed for a confirmed write")
        self.assertIs(told["appliedForeign"], False)


class V16ConsumerIdentityRosterTest(V16PublicationBase):
    """V16 §G — an actual `===` for every consumer, provenance included.

    The V15 review: "the full name roster passes, though the committed
    equality matrix lacks a provenance-specific `===` assertion". Source
    inspection and an independent replay confirmed the behaviour; what was
    missing was the committed assertion, and roster logging is not one.

    The production boundary is `catena-model.js`'s `absenceRows`, which reads
    `witnessed('provenance', chapterProjection(file)).editions`. It is drawn
    only where a reader asks for a translation that is not held, and no
    committed scenario asked for one AND opened a body — so provenance and
    the three ownership consumers had never stood on one authority. They do
    here, and every one of the twelve is asserted by identity.
    """

    def test_all_twelve_consumers_read_the_object_the_normalization_made(self):
        # ONE chapter, ONE normalization, TWELVE consumers, each asserted
        # against the reference recorded where the projection was MADE.
        page, authority = self.one_authority("v16-whole-roster", "opened")
        for consumer in self.CONSUMERS:
            with self.subTest(consumer=consumer):
                self.assertIn(consumer, page["consumerRefs"],
                              consumer + " is not routed through the "
                              "projection")
                self.assertEqual(page["consumerRefs"][consumer], [authority],
                                 consumer + " read an object the "
                                 "normalization did not make")

    def test_the_provenance_line_reads_the_authoritative_projection(self):
        # ★ THE MISSING ASSERTION ★  Named on its own, because the review
        # named it on its own: the object `absenceRows` consumed IS the
        # object the normalization made, compared as an object.
        page, authority = self.one_authority("v16-whole-roster", "opened")
        self.assertEqual(page["consumerRefs"]["provenance"], [authority])
        self.assertEqual(page["consumerRefs"]["provenance"],
                         page["consumerRefs"]["normalize"])
        # NON-VACUITY: the boundary really was reached on this page — the
        # absence disclosure it draws is standing on it.
        self.assertTrue(page["absenceReasons"],
                        "no absence was drawn, so provenance proves nothing")
        seen = [one["consumer"] for one in page["witness"]]
        self.assertIn("provenance", seen)

    def test_the_roster_and_the_identity_matrix_cover_the_same_names(self):
        # The gap the V15 review's phrasing points at: the V14 matrix
        # iterated `RENDERED_CONSUMERS`, which is eight of the twelve. The
        # matrix above iterates all twelve, and this asserts that the eight
        # are a strict subset of them rather than a second roster that could
        # drift.
        self.assertEqual(len(self.CONSUMERS), 12)
        self.assertEqual(sorted(set(self.RENDERED_CONSUMERS)
                                - set(self.CONSUMERS)), [])
        self.assertEqual(len(self.RENDERED_CONSUMERS), 8)


class V7AbsenceMemberTest(ReplayTest):
    """V7 §7 — an absence row about a work the record can name.

    Two defects, one seam. `absenceRows` deduplicated on `work_id` and read
    the author and the work AFTERWARDS, so a source stating neither took the
    row for that work — a blank entry under a summary counting it as a work
    standing here — and the valid sibling carrying the same work id and both
    its names was skipped behind it as a duplicate. And a member naming a
    language and nothing else was an absence record, so `{}` beside it made a
    row it could not support.
    """

    def test_a_source_that_cannot_name_the_work_takes_no_slot(self):
        # The hollow source stands FIRST in the fixture, which is what made it
        # the winner. The row is now the valid sibling's, named in full.
        page = self.page("v7-absence-slot")
        self.assertEqual(page["absenceAuthors"], ["Author 1"])
        self.assertEqual(page["absenceWorks"], ["Work 1"])
        self.assertEqual(page["absenceReasons"],
                         ["No English translation has been published."])
        self.assertEqual(
            page["absenceSummary"],
            "One work standing here has no English this project may publish")

    def test_no_blank_absence_row_stands(self):
        for name in ("v7-absence-slot", "v7-absence-members"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertNotIn("", page["absenceAuthors"])
                self.assertNotIn("", page["absenceWorks"])
                self.assertEqual(len(page["absenceAuthors"]),
                                 len(page["absenceWorks"]))

    def test_hollow_members_make_no_row_and_mask_no_sibling(self):
        # `typed.work1` lists `{}`, `null`, `4` and a string before its one
        # real record; `typed.work2` lists only hollow members. The first
        # speaks with its valid member; the second says nothing at all,
        # because a work no member says anything readable about is a work this
        # page has nothing to report.
        page = self.page("v7-absence-members")
        self.assertEqual(page["absenceAuthors"], ["Author 1"])
        self.assertEqual(page["absenceReasons"],
                         ["The only rendering is in copyright."])
        self.assertEqual(
            page["absenceSummary"],
            "One work standing here has no English this project may publish")

    def test_the_absence_pages_terminate(self):
        for name in ("v7-absence-slot", "v7-absence-members"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["busy"], "false")
                self.assertEqual(page["hash"], GEN10_ENGLISH)
                self.assertEqual(page["hashWrites"], [])
                self.assertEqual(page["replaced"], [])
                self.assertEqual(page["errorSections"], [])
                self.assertIsNone(page["failureText"])
                self.assertIn("absence", page["dataStates"])
                self.assertTrue(page["absenceOpen"])
                self.assertEqual(len(page["statusWrites"]), 1)


class V7RefusalLocusTest(ReplayTest):
    """V7 §8 — "Boundary not established" needs the whole typed record.

    It is the strongest sentence this page says about a text it did not
    write. V6 required a nonempty `note` and nothing else, so a note filed
    under another chapter, or carrying no `kind` the projection ever recorded,
    established it. `V7_REFUSAL_FIXTURE` is Genesis 2 and holds six records
    that each fail one clause of the contract; `V7_REFUSAL_VALID` adds one
    well-formed record LAST, so a valid refusal is still found whatever stands
    in front of it.
    """

    def test_no_malformed_or_misfiled_record_establishes_the_boundary(self):
        page = self.page("v7-refusal-locus")
        self.assertEqual(page["refusalCount"], 0)
        self.assertIsNone(page["refusal"])
        self.assertNotIn("refusal", page["dataStates"])
        # And none of the six notes reaches the page in any other form.
        for note in ("a note about the chapter before this one",
                     "a note carrying no kind",
                     "a note carrying a kind this projection never wrote",
                     "a note whose chapter is text"):
            with self.subTest(note=note):
                self.assertNotIn(note, " ".join(
                    page["asideNotes"] + page["sectionHeadings"]
                    + page["statusWrites"] + [page["tallyText"] or ""]))

    def test_the_one_well_formed_record_still_refuses_from_last_place(self):
        page = self.page("v7-refusal-valid")
        self.assertEqual(page["refusalCount"], 1)
        self.assertIn("Boundary not established.", page["refusal"])
        self.assertIn("the numbering of this chapter is displaced",
                      page["refusal"].lower())
        self.assertIn("refusal", page["dataStates"])

    def test_the_chapter_is_untouched_by_either_answer(self):
        # Refusing six records must cost the chapter nothing it really holds,
        # and establishing one must not either.
        refused, valid = (self.page("v7-refusal-locus"),
                          self.page("v7-refusal-valid"))
        for page in (refused, valid):
            self.assertEqual(page["fragmentCount"], 1)
            self.assertEqual(page["fragmentIds"], ["refusal-sibling"])
            self.assertEqual(page["tallyText"], "1 fragment held")
            self.assertEqual(page["busy"], "false")
            self.assertEqual(page["errorSections"], [])
            self.assertEqual(page["hashWrites"], [])
            self.assertEqual(page["replaced"], [])
            self.assertIsNone(page["failureText"])
            self.assertEqual(
                page["statusWrites"],
                ["Genesis 2, Douay-Rheims (Challoner), 1 fragment held."])
        # The refusal is the ONLY difference the two pages carry.
        self.assertEqual(set(valid["dataStates"]) - set(refused["dataStates"]),
                         {"refusal"})


class V7ContradictoryFindingRightsTest(ReplayTest):
    """V7 §9 — a contradiction leaks no selected rights prose.

    V6 blanked the FINDING when recognized findings conflicted and then chose
    one record's `reason` and `partial` by ranking them on length, and
    rendered that reason. So the page declined to say which rights claim the
    record made and then printed one of them anyway, picked by an arbitrary
    rule, underneath a summary saying it could not read the finding.

    `finding-order` and `finding-order-reversed` carry the same contradictory
    pair in opposite orders, so the claim is made twice over.
    """

    # work4 carries BOTH of these sentences, one on each side of its
    # contradiction, and V6 printed the second of them for work4 because
    # ranking on length preferred the record that also carried a `partial`.
    # The other four works say them legitimately: work1 and work5 the first,
    # work2 the second. So the leak is caught by COUNT — three reasons, in
    # these exact multiplicities, and a fourth would be work4 speaking.
    LEAKS = {"No English translation has been published.": 2,  # work1, work5
             "Only part of it is out of copyright.": 1}        # work2

    def both(self):
        return self.page("finding-order"), self.page("finding-order-reversed")

    def test_the_contradictory_work_contributes_no_reason(self):
        for page in self.both():
            for said, times in self.LEAKS.items():
                with self.subTest(said=said):
                    self.assertEqual(page["absenceReasons"].count(said), times,
                                     "a declined contradiction spoke")
            self.assertEqual(len(page["absenceReasons"]), 3)
            self.assertEqual(len(page["absenceAuthors"]), 5,
                             "declining a finding is not deleting the row")

    def test_no_partial_offer_comes_from_the_contradiction(self):
        for page in self.both():
            self.assertEqual(page["absencePartials"],
                             ["Partly public domain — the 1893 selection"])

    def test_neither_side_is_chosen_and_neither_is_the_harsher(self):
        # `none-published` is the harsher of work4's two claims and
        # `partial-public-domain` the gentler. Neither may be counted, so the
        # closed clause counts two works and not three, and the untaken clause
        # one and not two.
        for page in self.both():
            clauses = page["absenceSummary"].split("; ")
            self.assertEqual(
                clauses[0],
                "2 works standing here have no English this project may publish")
            self.assertEqual(
                clauses[1], "1 has only a partly public domain English, not yet taken")
            self.assertEqual(clauses[3], "1 has a finding this page cannot read")

    def test_the_two_orders_are_one_page(self):
        listed, flipped = self.both()
        self.assertEqual(self.rendered_state(listed), self.rendered_state(flipped))
        self.assertEqual(listed["statusWrites"], flipped["statusWrites"])
        self.assertEqual(listed["busy"], "false")
        self.assertEqual(listed["hashWrites"], [])
        self.assertEqual(listed["replaced"], [])
        self.assertIsNone(listed["failureText"])


class V7MalformedPartialTest(ReplayTest):
    """V7 §10 — `partial` is prose licensed by one finding, or it is nothing.

    The contract is the generator's: a whitespace-collapsed string, omitted
    when empty, meaningful only under `partial-public-domain`. Two scenarios,
    because a `partial` can fail in two independent ways — its own VALUE can
    be malformed, or its PARENT can be a state that licenses no offer — and
    the assertion in both cases is the rendered rights prose, not a helper.
    """

    OFFER = "Partly public domain"

    def test_no_malformed_value_becomes_an_offer(self):
        # Five works, each `partial-public-domain` — so the finding licenses
        # an offer — each carrying a `partial` that is a record, a list, a
        # number, a flag or a null. Five rows stand in the untaken class and
        # not one offer is printed.
        page = self.page("v7-partial-values")
        self.assertEqual(page["absencePartials"], [])
        self.assertEqual(
            page["absenceSummary"],
            "5 works standing here have only a partly public domain English,"
            " not yet taken")
        self.assertEqual(len(page["absenceAuthors"]), 5)

    def test_only_a_licensed_parent_prints_the_offer(self):
        # Five works, each carrying a `partial` that IS prose: beside a closed
        # finding, beside no finding, on one side of a contradiction, beside
        # the finding that licenses it, and beside an admission that nobody
        # looked. Exactly one offer is printed.
        page = self.page("v7-partial-parents")
        self.assertEqual(page["absencePartials"],
                         ["Partly public domain — the offer that is"
                          " genuinely licensed"])
        for stray in ("an offer beside a closed finding",
                      "an offer beside no finding",
                      "an offer on one side of a contradiction",
                      "an offer beside an admission"):
            with self.subTest(stray=stray):
                self.assertNotIn(stray, " ".join(
                    page["absencePartials"] + page["absenceReasons"]
                    + [page["absenceSummary"] or ""]))

    def test_the_rights_pages_terminate(self):
        for name in ("v7-partial-values", "v7-partial-parents"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["busy"], "false")
                self.assertEqual(page["hash"], GEN10_ENGLISH)
                self.assertEqual(page["hashWrites"], [])
                self.assertEqual(page["replaced"], [])
                self.assertEqual(page["errorSections"], [])
                self.assertIsNone(page["failureText"])
                self.assertEqual(len(page["statusWrites"]), 1)


class V7UnreadableRootDomainClaimTest(ReplayTest):
    """V7 §11 — an unreadable root makes no claim about the corpus.

    "We read the corpus and found nothing" and "we could not establish what
    the corpus holds" are not interchangeable sentences, and every case below
    was answering the first while meaning the second.
    """

    UNAVAILABLE = "The commentary record did not load"
    SPOKEN = ("Genesis 1, Douay-Rheims (Challoner),"
              " commentary record unavailable.")
    HELD = ("v7-held-not-a-list", "v7-held-unreadable-member",
            "v7-held-bad-digits")

    def test_an_unreadable_holdings_root_never_says_nothing_is_held(self):
        # `held` as a record, `held` as a list whose member cannot say which
        # book it is about, and a `chapter_digits` nobody can read. V6
        # answered all three with `Nothing held here`.
        for name in self.HELD:
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["tallyText"], self.UNAVAILABLE)
                self.assertNotIn("Nothing held", page["tallyText"])
                self.assertEqual(page["statusWrites"], [self.SPOKEN])
                self.assertEqual(page["sectionHeadings"],
                                 ["This chapter’s commentary record did not load"])
                self.assertEqual(page["asideNotes"], [],
                                 "no emptiness is stated beside the fault")

    def test_an_unreadable_holdings_root_asks_for_no_chapter_record(self):
        # A digit width nobody can read used to compose the WRONG path and
        # request it, then report the 404 it caused as a broken record. A
        # record this page cannot read is not a URL.
        for name in self.HELD:
            with self.subTest(scenario=name):
                self.assertFalse(
                    [one for one in self.page(name)["fetched"]
                     if one.startswith("structure/catena/01-gen/")],
                    "a chapter record was requested from an unreadable index")

    def test_the_unreadable_holdings_root_terminates(self):
        for name in self.HELD:
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["busy"], "false")
                self.assertEqual(page["hash"], GEN1)
                self.assertEqual(page["hashWrites"], [])
                self.assertEqual(page["replaced"], [])
                self.assertEqual(page["activeElement"], "body")
                self.assertEqual(page["referenceText"], "Genesis 1")
                self.assertEqual(page["dataStates"], ["error"])

    def test_an_incomplete_canon_makes_no_claim_about_the_canon(self):
        # One book readable, one not. The readable book still serves the page;
        # what the incomplete list may not do is prove a token is outside it.
        page = self.page("v7-partial-canon")
        detail = page["errorSections"][0]["details"]
        self.assertEqual(detail, [
            "book=Zzz is not a value this page could match; the record it"
            " would be matched against could not be read whole."])
        self.assertNotIn("is not a book of this canon", " ".join(detail))
        self.assertEqual(page["referenceText"], "Address not used")
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["hash"], "#book=Zzz&chapter=1&bible=douay-rheims")
        self.assertEqual(page["hashWrites"], [])

    def test_an_unreadable_voices_root_makes_no_claim_about_the_voices(self):
        page = self.page("v7-partial-voices")
        detail = page["errorSections"][0]["details"]
        self.assertEqual(detail, [
            "voice=translation:en is not a value this page could match; the"
            " record it would be matched against could not be read whole."])
        self.assertNotIn("is not a voice this corpus holds", " ".join(detail))
        self.assertEqual(page["busy"], "false")
        self.assertEqual(page["hashWrites"], [])

    def test_neither_incomplete_root_asks_for_anything_beyond_the_roots(self):
        for name in ("v7-partial-canon", "v7-partial-voices"):
            with self.subTest(scenario=name):
                self.assertEqual(self.page(name)["fetched"], [
                    "structure/catena/index.json",
                    "bibles.json",
                    "structure/paragraphs/index.json",
                ])

    PARAGRAPH_UNREAD = ("The paragraph record for this chapter in this edition"
                        " could not be read, so whether it divides the chapter"
                        " is not established here.")

    def test_an_unreadable_paragraph_record_claims_no_division(self):
        # The layer ROOT unreadable, the chapter FILE unreadable, and the
        # file's `breaks` unreadable. V6 printed "No paragraph division is
        # held for this chapter in this edition, so it runs on" for all three
        # — a claim about how an edition sets its text, drawn from a file
        # nobody could read.
        for name in ("v7-paragraph-root", "v7-paragraph-file",
                     "v7-paragraph-breaks"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["paragraphNote"], self.PARAGRAPH_UNREAD)
                self.assertNotIn("No paragraph division is held",
                                 page["paragraphNote"])
                # The chapter itself is untouched: refusing the layer is not
                # refusing the Scripture it would have divided.
                self.assertEqual(page["chapterCounts"], ["31 verses"])
                self.assertEqual(page["busy"], "false")
                self.assertEqual(page["errorSections"], [])

    def test_an_unreadable_paragraph_root_composes_no_request(self):
        self.assertNotIn(
            "structure/paragraphs/douay-rheims/01-gen/001.json",
            self.page("v7-paragraph-root")["fetched"])

    def test_a_readable_paragraph_layer_still_says_it_holds_none(self):
        # The other half of the same claim, and the reason this correction is
        # narrow: where the record CAN be read and records no division, the
        # page still says so, in those words.
        #
        # CORRECTED ORACLE (V7). This used `malformed-verses` as its control,
        # which was the wrong scenario for it: that fixture's `breaks` states
        # three marks and none is readable, so it is an example of the thing
        # this test exists to distinguish rather than of the thing it is
        # distinguishing from. `v7-empty-breaks` is the real control — a
        # paragraph record this page reads perfectly, which records no break.
        self.assertEqual(
            self.page("v7-empty-breaks")["paragraphNote"],
            "No paragraph division is held for this chapter in this edition, "
            "so it runs on. Another edition’s paragraphs are not borrowed "
            "for it.")

    VERSES_UNREAD = "Not shown: Genesis 1 arrived in a form this page cannot read."

    def test_an_unreadable_verses_container_is_never_reported_as_none(self):
        # `loadChapter` belongs to the shared shell and admits an ARRAY,
        # because `typeof [] === "object"`; the page then counted its keys,
        # found none, and told the reader a chapter of Scripture carries no
        # verses. The sentence is now asserted in the positive, which the V6
        # oracle could not do: it had no projection for the notice and could
        # only say the wrong words were absent.
        for name in ("v7-verses-list", "v7-verses-unreadable",
                     "unreadable-verses"):
            with self.subTest(scenario=name):
                page = self.page(name)
                self.assertEqual(page["notices"], [self.VERSES_UNREAD])
                self.assertNotIn("carries no verses", " ".join(page["notices"]))
                self.assertEqual(page["busy"], "false")
                self.assertIsNone(page["failureText"])

    def test_the_chapter_beside_the_unreadable_verses_still_stands(self):
        # An unreadable edition text is not an unreadable chapter of
        # commentary: the catena is rendered, counted and announced in full.
        page = self.page("v7-verses-list")
        self.assertEqual(page["tallyText"],
                         "107 fragments held · 33 lead entries"
                         " on the acquisition list")
        self.assertEqual(page["errorSections"], [])
        self.assertEqual(page["hashWrites"], [])


class V7SharedFieldDriftTest(unittest.TestCase):
    """V7 — the two lists that name the fold's shared fields must not drift.

    `_fold_shared` in `scripts/_catena.py` decides which fields are written
    once per edition under `sources`; `SHARED_WITH_EDITION` in
    `src/web/browser/catena/catena-model.js` decides which a fragment may
    inherit from there. Nothing related them, so a field added to the Python
    tuple would be written only under `sources` and silently dropped from
    every fragment — a real fact of the corpus, gone, with no test to notice.

    The JS list is deliberately WIDER: `attribution`, `rights_basis` and
    `acknowledgement` are terms-of-the-edition facts the page renders and the
    generator does not currently emit. Wider is safe; narrower is the defect.
    """

    def test_every_field_the_generator_shares_may_be_inherited(self):
        python = re.search(r"SHARED_WITH_EDITION = \(([^)]*)\)",
                           held(ROOT / "scripts/_catena.py"), re.S).group(1)
        emitted = set(re.findall(r'"([a-z_]+)"', python))
        model = re.search(r"const SHARED_WITH_EDITION = \[([^\]]*)\]",
                          held(CATENA / "catena-model.js"), re.S).group(1)
        inherited = set(re.findall(r"'([a-z_]+)'", model))
        self.assertTrue(emitted, "the generator's tuple was not found")
        self.assertTrue(inherited, "the model's list was not found")
        missing = sorted(emitted - inherited)
        self.assertEqual(missing, [],
                         "the generator shares these and a fragment cannot "
                         "inherit them, so they are dropped from every row")

    def test_no_per_fragment_field_may_be_inherited(self):
        """And the other direction, which is the one V7 got wrong first.

        `id`, `text_path`, `locator`, `review`, `text_words` and `extent` are
        written per fragment. Letting a fragment inherit `id` gave two
        fragments of one edition the same Source Library link and the same
        text request.
        """
        model = re.search(r"const SHARED_WITH_EDITION = \[([^\]]*)\]",
                          held(CATENA / "catena-model.js"), re.S).group(1)
        inherited = set(re.findall(r"'([a-z_]+)'", model))
        for own in ("id", "text_path", "locator", "review", "text_words",
                    "extent", "source"):
            with self.subTest(field=own):
                self.assertNotIn(own, inherited)


if __name__ == "__main__":
    unittest.main()
