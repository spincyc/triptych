"""Refuse a Latin body that is a recogniser reading rather than a page reading.

Every Latin body in the calendars is transcribed from a scanned Missal, and the
recognisers this project reads damage Latin in a small number of recognisable
families.  A damaged string is the dangerous kind of wrong: it is well-formed,
it hashes cleanly, it looks like Latin, and it survives every structural check
there is.  On 2026-09-03 a backfill wave stored 133 such strings as publishable
bodies, and nothing downstream would have caught one of them.

The families, with the readings that produced them:

    D6minum, parit£rque, cael6stis    a printed stress accent read as a digit
                                      or a currency sign
    qusesumus, quxsumus, beatse       the ae ligature read as se, as x, or --
    tua?                              as a question mark
    potiique, siipplices, commiinio   u read as ii before a consonant
    TJraesta, "eus > *l u keato"      an ornamental initial dropped or mangled
    IoannemOr                         two words welded across a line break

The screen deliberately favours precision over recall.  Its own false positives
taught it why: it once refused praesidiis, gaudiis and obsequiis, where -iis is
the ordinary ablative plural rather than u-read-as-ii, and a length rule meant
to catch a word split at a break refused cor, ego, mea, da, ita and fac.  One
lane's finalizer had already DELETED several such words from a body on that
reasoning.  A refused body is recoverable in a moment; a silently deleted word
is not.
"""

from __future__ import annotations

import re

# A printable-character allowlist was tried and removed. Every one of its five
# firings on landed bodies was legitimate liturgical typography: the digits of a
# printed citation ("Ps. 77, 1"), a genuine question ("Quare, Domine, irasceris
# in populo tuo?"), a genuine exclamation, the + of the sign of the cross, the
# guillemets of a quotation, and the / that separates the strophes of Gloria
# laus. The one damaged body it caught -- "eus > *l u keato Petro" -- is
# refused by the word rules on that same body. A screen that blocks publication
# must favour precision.
#
# Control characters stay refused, because they are never text: a page-separator
# \x0c carried into a provenance note once made the whole TOML ledger unreadable,
# which surfaced as one proper's "missing entry" when in fact no row parsed.
CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
# A denylist, unlike the allowlist, can be honest: these characters occur in no
# Latin prayer, rubric or chant mark, so one in a body is a recogniser artefact.
# This is what catches a wholly mangled opening like "eus > *l u keato Petro".
IMPOSSIBLE_CHARACTERS = re.compile(r"[<>|\\_~#@%^=${}\[\]`]")
ACCENT_AS_DIGIT = re.compile(r"[A-Za-z]*[0-9£&§¢®©][A-Za-z]+|[A-Za-z]+[0-9£&§¢®©][A-Za-z]*")
# -iis ending a word is the ablative plural and must survive; the damage always
# has letters after the consonant.  The ae-as-se rule fires word-finally only,
# where beatse lives, so that obsequiis and praesentibus are left alone.
DAMAGED_SEQUENCE = re.compile(
    r"qux|qus[aeiou]|prse|ssecul|sseter|tj[a-z]|^xs|[a-z]{2}[0-9]"
    r"|[bcdfgtvz]se$|ii[bcdfgklmnpqrstvx][a-z]",
    re.I,
)
WELDED_WORDS = re.compile(r"^[A-Za-zÆæ]+[a-zæ][A-ZÆ][A-Za-zÆæ]*$")
KNOWN_GOOD = frozenset(
    {
        "remedii", "mysteriis", "gaudii", "auxilii", "ministerii", "sacrificii",
        "beneficii", "iudicii", "judicii", "obsequii", "imperii", "silentii",
        "principii", "consilii", "exercitii", "martyrii",
    }
)


def body_damage(text: str) -> list[str]:
    """Tokens, or whole-body signals, that read as recogniser damage.

    Returns an empty list for a clean body.  A control character is reported
    first and on its own terms: it is not merely damage but makes the TOML
    provenance ledger unreadable, which once surfaced as a single proper's
    "missing entry" when in fact no row in the file could be parsed.
    """
    found: list[str] = []
    control = sorted({character for character in text if CONTROL_CHARACTERS.match(character)})
    if control:
        found.append("control characters: " + " ".join(repr(one) for one in control))
    impossible = sorted({character for character in text if IMPOSSIBLE_CHARACTERS.match(character)})
    if impossible:
        found.append("characters no prayer carries: " + " ".join(repr(one) for one in impossible))
    for word in re.findall(r"[^\s]+", text):
        word = word.strip(".,:;!'’()-")
        if not word or word.lower() in KNOWN_GOOD:
            continue
        if ACCENT_AS_DIGIT.fullmatch(word) or DAMAGED_SEQUENCE.search(word) or WELDED_WORDS.match(word):
            found.append(word)
    return found
