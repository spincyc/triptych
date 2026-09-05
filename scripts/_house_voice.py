"""Refuse reader-facing prose whose subject is the guide rather than a source.

`guidance/editorial.md` states the test in one sentence: "When a sentence is
doubtful, look at its grammatical subject. A qualifying sentence is legitimate
when its subject is a source, a text, a witness, or a fact ... The same
sentence is the defect when its subject is the guide, the reading, or an
evidence class."  The same file's "State the finding, not the process that
produced it" adds that naming the discipline is itself the defect: prose
saying that a difference was retained rather than silently harmonised, that a
negative result is bounded and correctable, or that a reading is documented
reception, is narrating compliance where it should simply be compliant.

That is linter work, and until now it was not being done by a linter.  One
production run of a 1962 proper guide spent its whole evaluation budget on it:
three successive max-effort AI evaluations of the same leaf found roughly 96
instances, then about 10, then 22, each pass repairing the ones it had named
and the next finding a fresh subset of the same habit.  A five-lane evaluation
is the wrong instrument for a defect that has a fixed vocabulary.

The screen favours precision far above recall, and for the reason the Latin
body screen beside it gives: a refused leaf costs one rewrite, and a wrongly
refused sentence costs evidence, because the worker acting on the refusal
deletes the clause.  Every rule here therefore fires on a *form*, never on a
topic, and four things the guidance protects are cut out of the text before
any rule runs:

- the terminal `Appendix: Scope and Qualifications` and `References`, which
  are qualification by design;
- the page-2 sheet, whose explanatory row is *required* to carry the modern
  critical horizon;
- the exploratory notice of `The Propers: Interpretive Possibilities`, and
  every proposal field whose name says it is the strongest-limit field, in
  each of the three ways the profile lets that field be headed;
- LaTeX comments, which no reader sees.

## What a first cold review broke, and what it cost

The subject test was not one.  It read one word either side of the work's
name, so `<noun> this repository <finite verb>` passed it -- which is a
*relative clause*, not a sentence.  The prose that reaches is exactly the
prose this screen exists to protect: "No Collect, Secret or Postcommunion of
any of the fifteen 1962 identities this repository has collated ... asks for
food" is a bounded negative result whose denominator sits in the clause the
screen pointed at, and "printed in the Pustet Missal of Ratisbon, 1862, which
this repository tracks as public-domain text" is the 17 U.S.C. \u00a7103(b)
rights basis for printing the Latin at all.  A worker told either is a defect
deletes it, and the first sentence becomes a false universal about the Missal
while the second loses the ground of its own lawfulness.

So the name must now *begin a clause* -- start of file, after `.` `;` `:` `?`
`!` or an em dash, after a paragraph break, or after a coordinating
conjunction -- before any rule that claims to find a subject fires, and the
same guard was put on the library, the guide's-own-apparatus and page-N rules,
which had none at all.

Four more rules went in the same pass, and the reason is the same one: they
fired on subject matter rather than on form, in a library that has that
subject matter.  `digests?` refuses "The \\work{Digest} of Justinian treats the
same question" and "Isidore's Book V is a compressed digest of late Roman
jurisprudence", both of which stand in this corpus now.  `no leaf` refuses
"The fig tree bore no leaf" and "No leaf of the Ottobonianus carries the
rubric".  `(this|the) (sweep|revision|pipeline|workflow)` refuses "The
revision of 1568 removed the sequence".  Between them the two carried one
locus in twelve leaves -- `no leaf` had it and the other four words had
nothing.  `earlier (form|draft|version) of this` refuses
"An earlier form of this antiphon stands in the Ottobonianus margin", and now
has to reach the work's own name.  `page N's` was kept and put under the
clause test instead, a page of a source having a possessive too.

Recall was spent to buy all of it, and the trade is the one
`guidance/editorial.md` asks for: this screen "reports a sentence to rewrite,
never a sentence to delete".

What the rules deliberately do NOT catch is written into the tests beside
them.  A bounded negative result whose subject is the source or the extent
actually searched is legitimate and stays; so does a claim-local evidence
state, a source's own status, a claim-local rights basis, and every sentence
that names the repository anywhere but in its own subject position -- "of the
fifteen formularies collated in this repository" states a denominator, and a
rule that refused it would invite a worker to delete the denominator.
"""

from __future__ import annotations

import re

# --- Cutting the text down to what a reader actually reads -----------------

# What stands where *content* was cut out, as against markup. It is not
# whitespace and no rule may cross it. A rule's literal spaces are `\s+`,
# because the defect crosses line ends constantly; when a cut region was
# spaces too, the words on either side of it joined and the screen reported
# phrases that are not in the file -- "It follows the
# \texttt{research/scope.md} workflow of Augustine" was refused for "the
# workflow". Newlines survive inside a cut region so that a reported line is
# still the line the editor shows.
GAP = "\x00"

# A `%` opens a comment when an EVEN number of backslashes precedes it: `\%`
# is a printed percent sign and `\\%` is a comment after a line break. The
# earlier one-character lookbehind read the second as an escape and screened
# a comment as reader-facing prose.
COMMENT = re.compile(r"(?<!\\)((?:\\\\)*)%[^\n]*")
# Any macro call that stands at the start of a line, which is where a heading
# stands. `\section*{...}` is the ordinary form, but one published leaf heads
# its appendix `\section{...}` with no star and a leaf-local `\newcommand`
# alias would be a third form; six of the twenty published propers already
# alias an *environment*, so this is not hypothetical. A heading missed here
# is a protected region screened, which is the opposite of the rule.
LINE_MACRO = re.compile(r"(?m)^[ \t]*\\[A-Za-z@]+\*?[ \t]*(?=\{)")
# `\section` only: a `\subsection*` inside the terminal appendix is part of
# the appendix, and reading it as a boundary ends the protected region at the
# appendix's first sub-heading and screens the rest of it.
SECTIONING = re.compile(r"\\section\*?\Z")
# The three sections the guidance exempts wholesale. `References` and the
# terminal appendix are qualification by design; the page-2 sheet is where the
# profile *requires* the principal modern critical horizon to stand, and the
# lane that found the 22 loci rested none of them on it.
EXEMPT_SECTION = re.compile(
    r"\A(?:References|Appendix\b.*|Scriptural Date and Location)\Z")
INTERPRETIVE = "The Propers: Interpretive Possibilities"
PROPOSAL = re.compile(r"\\begin\{proposal\}")
PFIELD = re.compile(r"\\pfield\{([^{}]*)\}\s*\{")
# The profile's fifth field, in every heading it allows: "end with the
# strongest material limit, alternative, or disconfirming condition". A field
# of the author's own devising is not inside that carve-out, which is exactly
# how the one defect in a proposal survived four sweeps; but a proposal that
# heads the field `Disconfirming condition` is inside it, and reading only
# `limit` stripped the carve-out from that proposal.
LIMIT_FIELD = re.compile(r"\b(?:limits?|alternatives?|disconfirming)\b", re.I)
# Arguments that are typeset as machine text or are not typeset at all. A
# `\texttt{research/scope.md}` is a path the profile tells the guide to print;
# it is not the guide taking itself as a subject.
OPAQUE = re.compile(
    r"\\(?:texttt|nolinkurl|url|href|label|ref|pageref|input|include"
    r"|hypersetup|cue|properrefs|wlocus|sourceurl)\s*\{")


def _cut(text: str, start: int, stop: int) -> str:
    """Replace a span's content with `GAP`, keeping newlines and offsets.

    Offsets have to survive so that a match can still be reported at the line
    the author has to open, and so that a quotation can be read back out of
    the source rather than out of the masked text. Newlines have to survive so
    that the line numbers are the ones the editor shows.
    """
    span = text[start:stop]
    return (text[:start]
            + "".join(GAP if ch != "\n" else ch for ch in span)
            + text[stop:])


def _closing(text: str, opening: int) -> int:
    """The offset just past the brace group opening at `opening`."""
    depth, index = 0, opening
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
                return index + 1
        index += 1
    return len(text)


def _uncomment(text: str) -> str:
    """Every LaTeX comment cut out, the escaping counted and not guessed."""
    return COMMENT.sub(
        lambda hit: hit.group(1) + GAP * (len(hit.group(0))
                                          - len(hit.group(1))),
        text)


def _plain(text: str) -> str:
    """A heading's argument reduced to the words it prints."""
    text = re.sub(r"\\[A-Za-z@]+", " ", text)
    return " ".join(text.replace("{", " ").replace("}", " ").split())


def _heads(text: str) -> list[tuple[int, str]]:
    """Every section heading, including one written through an alias.

    A sectioning command counts wherever it stands at the start of a line,
    starred or not. Any other line-initial macro counts only when its whole
    argument is one of the protected names and nothing follows it on the line
    -- which is a heading and not a `\\textbf{References}` inside a sentence.
    """
    found: list[tuple[int, str]] = []
    for hit in LINE_MACRO.finditer(text):
        opening = hit.end()
        stop = _closing(text, opening)
        name = _plain(text[opening + 1:stop - 1])
        if SECTIONING.search(hit.group(0).strip()):
            found.append((hit.start(), name))
        elif (EXEMPT_SECTION.match(name) or name == INTERPRETIVE) and \
                not text[stop:].split("\n", 1)[0].strip():
            found.append((hit.start(), name))
    return found


def exempt(text: str) -> tuple[str, list[tuple[int, str]]]:
    """The file with every protected region cut out, and what went unread.

    Markup survives this pass: the run-in label rule reads `\\textbf{...}`,
    which the next pass removes.

    The second half of the return is the regions no rule could be run over,
    reported rather than silently dropped. Six of twelve leaves write their
    interpretive section with no `\\pfield` at all, and nothing else marks
    where the protected exploratory notice ends and the proposals begin; the
    section is therefore cut, and a check that said nothing about it would let
    half the corpus's discovery section be screened by neither this nor
    `proposal-fields`, with dropping the markup a legal way to silence both.
    """
    text = _uncomment(text)
    unread: list[tuple[int, str]] = []
    heads = _heads(text)
    for index, (at, name) in enumerate(heads):
        stop = heads[index + 1][0] if index + 1 < len(heads) else len(text)
        if EXEMPT_SECTION.match(name):
            text = _cut(text, at, stop)
        elif name == INTERPRETIVE:
            if not PFIELD.search(text, at, stop):
                unread.append((at, name))
                text = _cut(text, at, stop)
                continue
            first = PROPOSAL.search(text, at, stop)
            text = _cut(text, at, first.start() if first else stop)
    for hit in list(PFIELD.finditer(text)):
        if LIMIT_FIELD.search(hit.group(1)):
            text = _cut(text, hit.start(), _closing(text, hit.end() - 1))
    return text, unread


def prose(text: str) -> str:
    """The exempted text reduced to the words, with every offset preserved.

    Markup goes to spaces, because the words on either side of a `\\textbf{`
    are adjacent on the page. Content goes to `GAP`, because the words on
    either side of a dropped `\\texttt{research/scope.md}` are not.
    """
    while True:
        hit = OPAQUE.search(text)
        if not hit:
            break
        text = _cut(text, hit.start(), _closing(text, hit.end() - 1))
    text = re.sub(r"\\[A-Za-z@]+", lambda m: " " * len(m.group(0)), text)
    text = re.sub(r"\\.", "  ", text)
    return text.replace("{", " ").replace("}", " ")


# --- The rules -------------------------------------------------------------

def _pattern(body: str) -> re.Pattern:
    """A rule, with every space made whitespace-tolerant.

    The defect crosses line ends constantly -- "a count over those records and
    not over the\\n\\work{Missale Romanum}" is one sentence in two lines -- and
    a line-at-a-time reader finds about half of it. `GAP` is not whitespace,
    so this tolerance cannot carry a rule across something that was cut.
    """
    return re.compile(body.replace(" ", r"\s+"), re.I)


# The work itself, in every name the leaves give it.
SELF = r"(?:guide|project|repository|document|leaf|publication)"
# A finite verb after the work's name is what makes the work the subject.
# Without this test "the reading undecim controls this publication" -- where
# the work is the object -- is refused, and it is ordinary correct prose.
FOLLOWS_A_SUBJECT = _pattern(
    r"(?:says|said|prints|printed|states|stated|reports|reported|treats"
    r"|treated|holds|held|tracks|tracked|registers|registered|carries"
    r"|carried|quotes|quoted|adopts|adopted|has|have|had|is|was|are|were"
    r"|makes|made|gives|gave|does|did|uses|used|reads|reaches|reached|takes"
    r"|took|calls|called|names|named|follows|followed|rests|rested|asserts"
    r"|asserted|claims|claimed|declines|declined|prefers|preferred|omits"
    r"|omitted|leaves|left|supplies|supplied|composed|translated|adapted"
    r"|paraphrased|collated|met|would|will|may|might|can|could|must|should"
    r"|shall|never|itself)\b")
WORK_NAMED = _pattern(rf"\b(?:this|the) {SELF}\b")
# What can stand immediately before a clause's first word. A coordinating
# conjunction opens a second main clause; a relative pronoun, a preposition
# and a bare noun do not, and those are the three that carried the false
# positives.
CLAUSE_OPENER = re.compile(r"\b(?:and|but|or|nor|yet|so)\Z", re.I)
CLAUSE_ENDING = ".;:!?"
# A sentence in this corpus ends inside its quotation marks as often as
# outside them -- ``they print ``Pseudo-Chrys.'' The guide names the source
# that way'' -- and a closing `''` read as an ordinary word ends the sentence
# test one character early.
CLOSERS = "'’\"”)]}"
PARAGRAPH_BREAK = re.compile(r"\n[ \t\r]*\n[ \t\r\n]*\Z")


def begins_a_clause(text: str, start: int) -> bool:
    """Whether what stands at `start` opens a clause of its own.

    This is the whole difference between a sentence subject and the subject of
    a relative clause, and the difference between a screen that protects a
    denominator and one that deletes it. "No Collect ... of any of the fifteen
    1962 identities this repository has collated" and "the Pustet Missal of
    1862, which this repository tracks as public-domain text" both put a
    finite verb after the work's name; in neither is the work the subject of
    the sentence, and in both the clause carries something -- the denominator
    of a negative result, the rights basis for printing the Latin -- that the
    sentence cannot lose.

    A `GAP` before the name is content this screen could not read, so it is
    not a clause boundary either.
    """
    head = text[:start].rstrip(" \t\r")
    if not head:
        return True
    if head.endswith("\n"):
        if PARAGRAPH_BREAK.search(head):
            return True
        head = head.rstrip(" \t\r\n")
        if not head:
            return True
    closed = head.rstrip(CLOSERS)
    if head.endswith("---") or (closed and closed[-1] in CLAUSE_ENDING):
        return True
    return bool(CLAUSE_OPENER.search(head))


# Every rule, and whether it claims to have found a *subject*. A rule that
# does is run only where its words begin a clause; `guidance/editorial.md`
# tests the grammatical subject of the sentence, and nothing weaker is that
# test.
RULES: tuple[tuple[str, re.Pattern, bool], ...] = (
    # `guidance/liturgy/roman-1962-propers.md`, Appendix: Scope and
    # Qualifications: "Leave retrieval mechanics, checksums, query detail,
    # discarded leads, and operational audit in those records." Whether a
    # file's bytes matched a registered digest changes the truth of no claim
    # about a witness; the reading either is or is not what the page carries.
    #
    # `digests?` stood here and is gone: this is a corpus that cites the
    # \work{Digest} of Justinian and writes "Isidore's Book V is a compressed
    # digest of late Roman jurisprudence", both of which it refused.
    ("retrieval mechanics stand in the body",
     _pattern(r"\bhash(?:es|ed|ing)?\b|\bhash-[a-z]+|\bchecksums?\b"), False),
    # The work as possessor of a claim-making act: "this guide's collation",
    # "this guide's own collation", "the leaf's source bindings".
    ("the work possesses the finding",
     _pattern(rf"\b(?:this|the) {SELF}['\u2019]s\b"), False),
    # The production pipeline named to a reader who cannot know what it is.
    # `provider` fires only in the possessive, where it can only be the
    # repository's own word for `src/<provider>/`: a guide is free to call God
    # the provider of every good thing, and this is a theological corpus.
    # `earlier form of this` now has to reach the work's own name, or it
    # refuses "An earlier form of this antiphon stands in the Ottobonianus
    # margin"; `no leaf` and `(this|the) (sweep|revision|pipeline|workflow)`
    # are gone, the first because "The fig tree bore no leaf" and a codex's
    # leaf are both ordinary here and the second because "The revision of
    # 1568 removed the sequence" is the plainest possible sentence about a
    # missal. Between them they were carrying one locus in twelve leaves.
    ("the production pipeline is named",
     _pattern(r"\bproviders?['\u2019]s\b"
              r"|\b(?:this|the|no|any|one) lanes?\b"
              rf"|\bearlier (?:form|draft|version|state) of this {SELF}\b"),
     False),
    # The source library as subject: "the library's sole registered
    # treatment". Written so that the Library of Congress, which a gallery
    # entry cites, is left alone -- and now so that "the one medieval preacher
    # the library registers on this Epistle expounds it beside a different
    # Gospel", where the subject is the preacher and the clause states the
    # extent searched, is left alone too.
    ("the source library is the subject",
     _pattern(r"\bthe library(?:['\u2019]s|"
              r" (?:registers|holds|carries|has|registered|catalogues))\b"),
     True),
    # The guide's own pages and apparatus as subject: "page 1's allegorical
    # row prints", "the page-2 dossier reports", "the terminal appendix
    # states", "the entry's value is". Under the clause test, because a page
    # can be a source's page, an entry can be a catalogue's entry, and a
    # cross-reference to the appendix from inside a sentence is not a subject.
    ("the guide's own apparatus is the subject",
     _pattern(r"\bpage[~ ]?\d+['\u2019]s\b"
              r"|\bthe page-\d+ (?:dossier|sheet|row)\b"
              r"|\bthe terminal appendix\b"
              r"|\bAppendix: Scope and Qualifications\b"
              r"|\bthe (?:gallery|entry)['\u2019]s\b"), True),
    # A meta-label on the guide's own count, in the sentence that gives the
    # denominator anyway: "a statement about fifteen collated formularies and
    # not about the Missal", "a count over those records and not over the
    # Missale Romanum".
    ("the count is labelled instead of stated",
     _pattern(r"\bnot (?:about|over) the Missal"
              r"|\bis a judge?ment and not a (?:measurement|count|fact)\b"),
     False),
    # `guidance/editorial.md`: prose saying "that a difference was retained
    # rather than silently harmonised ... is narrating compliance where it
    # should simply be compliant". Only the guide's own restraint fires here:
    # a source that harmonises two Gospels, and an English that flattens a
    # Latin distinction, are facts about those texts and are left alone.
    ("the discipline is narrated instead of kept",
     _pattern(r"(?:rather than|instead of(?: being)?|without) (?:silently )?"
              r"harmoni[sz](?:ed|ing|ation)"
              r"|\bno harmoni[sz]ation\b|\badopts no harmoni"
              r"|(?:is|are|was|were|nor) not flattened"
              r"|\bnot flattened into\b|\brather than flattened\b"
              r"|\bbounded and correctable\b"
              r"|\b(?:negatives?|absences?|counts?) (?:is|are) bounded\b"
              r"|\bas documented reception\b"
              r"|\b(?:bounds|qualifications|caveats|limits) travels? with\b"
              r"|\bnone is asserted\b|\bis not asserted here\b"), False),
    # The evidence-class disclaimer that trails a claim already attributed:
    # "is cited for the compilation and never as a vote", "reported as his
    # opinion and never as a fact". The reporting verb is required, so that
    # "the letters stand before the section numbers and not as part of them"
    # -- a statement about a printed page -- is not touched.
    ("the evidence class is disclaimed after the claim",
     _pattern(r"\b(?:reported|cited|attributed|treated|restated|published"
              r"|stands|stand|stood)\b[^.]{0,60}?"
              r"\bnever (?:as|restated as|treated as)\b"), False),
)

# A bold run-in label that counts the guide's own bounds. The profile: "A
# heading, a run-in label, or a table column that prints the discipline -- a
# retained control, a caveat field, a note that a difference was not
# harmonised -- is the defect." Only a *count* of them fires, so that a bold
# lead-in naming the appointed bounds of a psalm is left alone.
RUN_IN_LABEL = re.compile(
    r"\\textbf\{\s*(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine)\s"
    r"[^{}]{0,30}?\b(?:bounds|qualifications|caveats)\b[^{}]{0,40}\}",
    re.I)

# How far either way a quotation may reach for its sentence.
REACH = 240
QUOTED = 300
# A sentence ends at `.`, `!` or `?` followed by space and then something that
# starts a sentence. `pp.~136--138`, `Gal.\ 5:16--24` and `vol.~III` end no
# sentence, and a quotation that stopped at one of them would hand a worker
# half a clause.
SENTENCE_END = re.compile(
    r"[.!?][\"'\u2019\u201d)\}\]]*\s+(?=[\\A-Z\u201c`\"])")


def _quote(source: str, start: int, stop: int) -> str:
    """The match, in the source's own words, grown to its sentence.

    Read out of the *source* and not out of the masked text, because every
    pass above preserves offsets and lengths precisely so that it can be. The
    masked text has spaces where the markup was, so a quotation taken from it
    is a string that does not occur in the file the worker has to open, cannot
    be searched for, and reads as though the screen had misquoted the leaf.
    """
    left = max(0, start - REACH)
    opening = left
    # `start + 1`, because a sentence boundary standing immediately before the
    # match ends with a lookahead at the match's own first character: cut the
    # search at `start` and that boundary can never match, and the quotation
    # silently grows a whole preceding sentence -- which is how a refusal
    # aimed at "The project claims no rights in this text" came to quote the
    # §103(b) rights clause in front of it as though that were the defect.
    for hit in SENTENCE_END.finditer(source, left,
                                     min(len(source), start + 1)):
        if hit.end() <= start:
            opening = hit.end()
    for hit in re.finditer(r"\n[ \t\r]*\n", source[left:start]):
        opening = max(opening, left + hit.end())
    closing = min(len(source), stop + REACH)
    ahead = SENTENCE_END.search(source, stop, closing)
    if ahead:
        closing = ahead.start() + len(ahead.group(0).rstrip())
    else:
        para = re.search(r"\n[ \t\r]*\n", source[stop:closing])
        if para:
            closing = stop + para.start()
    # A quotation that does not contain the words the rule saw is no use to
    # the worker holding it, so a long sentence is trimmed around the match
    # rather than from its end.
    if closing - opening > QUOTED:
        spare = QUOTED - min(stop - start, QUOTED)
        opening = max(opening, start - spare // 2)
        closing = min(closing, max(stop, opening + QUOTED))
        opening = max(0, min(opening, closing - QUOTED))
    return " ".join(source[opening:closing].split())


def _is_the_subject(text: str, hit: re.Match) -> bool:
    """Whether the work named at `hit` is the subject of its own clause.

    Two tests, and both are needed. The name must begin a clause, or the
    subject of a relative clause is read as the subject of the sentence and
    the screen refuses denominators, bounded negatives and rights bases. A
    finite verb must follow it, or "the reading undecim controls this
    publication" is refused and the work is the object of the sentence, not
    its subject.
    """
    return (begins_a_clause(text, hit.start())
            and bool(FOLLOWS_A_SUBJECT.match(text[hit.end():hit.end() + 80]
                                             .lstrip())))


def unscreened(source: str) -> list[tuple[int, str]]:
    """Every region of the file no rule could be run over, with its line.

    A non-answer, said outright. `proposal-fields` beside this reports "not in
    scope" when a leaf marks no proposal, for the same reason: what a check
    cannot read it must not report as read.
    """
    marked = _uncomment(source)
    return [(marked.count("\n", 0, at) + 1, name)
            for at, name in exempt(source)[1]]


def house_voice(source: str) -> list[tuple[int, str, str]]:
    """Every place the file speaks about itself instead of about a source.

    Returns `(line, what the rule saw, the sentence it saw it in)`, sorted by
    line. An empty list is a file whose reader-facing prose keeps a source, a
    text, a witness or a fact in the subject position throughout -- or, where
    `unscreened` names a region, a file part of which no rule was run over.
    """
    marked = exempt(source)[0]
    words = prose(marked)
    found: list[tuple[int, str, str]] = []
    for label, rule, subject in RULES:
        for hit in rule.finditer(words):
            if subject and not begins_a_clause(words, hit.start()):
                continue
            found.append((hit.start(), label, _quote(source, *hit.span())))
    for hit in WORK_NAMED.finditer(words):
        if _is_the_subject(words, hit):
            found.append((hit.start(), "the work is the subject",
                          _quote(source, *hit.span())))
    for hit in RUN_IN_LABEL.finditer(marked):
        found.append((hit.start(), "a run-in label prints the discipline",
                      _quote(source, *hit.span())))
    seen: set[tuple[int, str]] = set()
    report = []
    for at, label, quotation in sorted(found):
        if (at, label) in seen:
            continue
        seen.add((at, label))
        report.append((words.count("\n", 0, at) + 1, label, quotation))
    return report
