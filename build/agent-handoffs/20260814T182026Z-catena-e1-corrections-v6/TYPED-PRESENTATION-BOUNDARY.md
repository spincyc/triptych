# The typed presentation boundary — what V6 admits, what it refuses, and why

The V5 review returned blocking classes that are one distinction said many
ways: **V5 validated a shape where the contract needed a membership.** A value
was confirmed to be an object and never asked whether it was a member of the
collection it stood in. A value was confirmed to be text and never asked
whether it was an identity this corpus had issued. Both questions have the same
answer shape and V6 answers them in the same place.

## Where the boundary lives, and why it is not in the page

`src/web/browser/catena/catena.js` finished this correction with **7 gzipped
bytes** of whole-file margin, at 12,993 of 13,000. A membership boundary bought
out of seven bytes would be a list of one-off guards at each sink, which is the
shape that produced these defects: each sink fixed alone as it was found, and
no two sinks holding the same opinion.

`src/web/browser/catena/catena-model.js` carries no size ceiling — only a
`MODEL_SHA256` digest pin — and it is the file `catena check` executes under
node during generation. The boundary is there, so the page and the generator
cannot answer the same question differently. `BASELINE-COMPARISON.md` records
what that relocation costs a reader, in both measures, rather than the
flattering one alone.

## The predicates: what each admits and refuses

The first block is the type boundary V3–V5 already carried. The second is what
V6 adds, and it is the identity half.

| Predicate | Admits | Refuses | Why here |
| --- | --- | --- | --- |
| `sound` | a string, trimmed | a record, a list, a number, a flag, blank, whitespace | `String(x)` turns a record into `[object Object]` and a list into accidental comma-joined text |
| `list` | an array | a scalar pretending to be a one-item list | `x \|\| []` turns a string into a container whose `.length` counts characters as works |
| `bag` | a non-array object | a list, a string, `null` | a lookup answers for the prototype as readily as for the record |
| `count` | a finite number | `"1"`, `[1]` | `Number([1])` is `1`: a one-member list numifies to its member |
| `say` | a finite number, or sound text | anything else | dates arrive both ways in this corpus |
| `whole` | a positive safe integer | `0`, negatives, fractions, `1e21`, `"5"`, `[5]`, `true` | `Number(x) > 0` accepted `true` and printed "1 words", and accepted `[4]` for a chapter |
| `tongue` | `/^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$/` | sound text that is not a subtag | `lang` is machine-read: a browser picks hyphenation from it, a screen reader picks a voice |
| `voiceLanguage` | `/^[a-z]{2,3}$/` | everything `tongue` refuses, plus `en-GB` and upper case | a voice key becomes a URL, and the page must accept back the addresses it issues |

**V6 adds four, and they gate identity rather than type.**

| Predicate | Grammar | Admits | Refuses | Why drawn there |
| --- | --- | --- | --- | --- |
| `ident` | `/^[a-z0-9]+([.-][a-z0-9]+)*$/` | fragment ids, work ids, edition ids, canon paths | `"../../etc/passwd"`, `"a b"`, arbitrary prose, `"constructor"`, padded or empty segments | each of these becomes a fetched path, a Source Library href, or a property lookup into a record; sound text is not an identity this corpus issued |
| `bookToken` | `/^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$/` | `Gen`, `1Kings`, `Philem` | any separator but the hyphen, whitespace, path syntax | wider than `ident` because the canon writes the abbreviations a reader cites and the published hash grammar carries them verbatim; still closed, because a token becomes a directory inside a chapter request |
| `trail` | `/^([a-z0-9]+([.-][a-z0-9]+)*\/)+$/` | `structure/catena/01-gen/` | a leading slash, `..`, an empty segment, a query, a scheme | a prefix is the head of a URL this page requests; a path that is not one of this data root's own directories is never made into one |
| `records` | array members that are non-null non-array objects | scalars, nulls, nested lists | a container was validated and its members were not, so one malformed neighbour could throw out of the render and take every valid sibling with it |

**Two identity grammars, because the corpus writes two.** `ident` is lowercase;
`bookToken` additionally admits upper case and digits leading a token. That
seam is deliberate and `REVIEW_REQUEST.md` §6 asks a reviewer to rule on it.

## The member constructors: what one member of each collection IS

`records()` asks whether a member is an object. It never asked whether the
object is a member of *this* collection. Each collection now states the least a
record must say for there to be anything to render or to count, once, in the
model.

| Constructor | A member must | A record that cannot | The defect it closes |
| --- | --- | --- | --- |
| `canonBook` | state a `bookToken`, a sound name and a `whole` chapter count | is not a book of this canon and is left out | a `null` member threw during startup, outside every funnel |
| `bibleRecord` | state an `ident` id and a sound label | is not an offered edition | `\|\| 'en'` made an unreadable language an English Bible, in the option a reader chooses and in the `lang` a screen reader speaks from |
| `leadRow` | name an author or a title | is not a lead entry, renders nothing and enters no count | an empty `<li>` was still counted into "3 unreconciled lead entries" |
| `blockedRow` | name what is held, or why it cannot be shown | is not a blocked row | a record stating nothing counted as a work held and turned the sentence into a claim about what this project possesses |
| `refusalNote` | carry a sound `note` | refuses nothing | `{}` printed "Boundary not established." — a claim about Scripture's own numbering, made by an empty record |
| `absenceRows` | carry a recognized `finding`, read across every same-language record | enters no class count and is spoken as a finding this page cannot read | first-match selection let an unreadable record erase a valid finding, and the same two records in the other order kept it |

Refusing a malformed member costs the record nothing it really states: the
valid siblings stand, in their original relative order, and the count is a
count of what stood. `mixed-collection` tallies `3 fragments held · 2 works
held, not renderable yet · 2 lead entries`, where V5 pinned `3 · 3 · 3` with
two blank rows standing in the document.

**The asymmetry in that tally is deliberate.** The third fragment states its
author, work, date and extent and only its **id** is unreadable, so it renders
a row and is a fragment held here minus one fact. The rejected lead and blocked
records state nothing at all. V5 argued the opposite and the review rejected
the argument; `REVIEW_REQUEST.md` §3 asks a reviewer to rule on the line V6
drew.

## The three-valued answers

Two derivations refuse to collapse "no" into "nothing".

`chapterPath(index, token, chapter)` answers a path, `''` for a real recorded
emptiness, or `null` for a record that can establish neither. **"Nothing held
here" is a claim about the corpus**, and a record this page cannot read
establishes no such claim, so a malformed `present` list or a malformed `path`
reaches the broken-record notice instead. Every entry for a book is read, not
the first object-shaped one, because a malformed same-token record was masking
a valid sibling standing behind it.

`absenceRows` gathers the recognized findings across all same-language records
for one work. One distinct recognized finding is the record speaking. **Two
different ones are a record contradicting itself**, and the row carries no
finding, enters no class count and is spoken as "a finding this page cannot
read" rather than resolved to the harsher of the two claims.

Which record's prose stands for a row is chosen without reference to position —
the record that states the most, ties broken lexically — so the same set yields
the same row in any order. That rule is arbitrary and deterministic, and
`REVIEW_REQUEST.md` §2 says so and asks.

## Findings, and the four the generator writes

`scripts/_catena.py` closes `finding` at four values so a fifth has to be
argued for rather than typed. V6 maps each to what it licenses and adds no
fifth:

| finding | the page may say |
| --- | --- |
| `none-published` | no English this project may publish |
| `in-copyright` | no English this project may publish |
| `partial-public-domain` | only a partly public domain English, not yet taken |
| `not-surveyed` | **has not been surveyed for English** |
| anything else | **has a finding this page cannot read**, and enters no count |

`partial` refines a finding and never establishes one: the `offer` clause is
derived beside the finding that licenses it, so a stray `partial` string on an
unknown or `not-surveyed` row can no longer print "Partly public domain" — a
rights claim about somebody's text manufactured out of a field beside a finding
that supports no such thing.

## Verse identity

`chapterLines` numbers a verse from `^[1-9][0-9]*$` and nothing else.
`^[0-9]+$` admitted `"01"` and `"001"` beside `"1"`, and `Number()` folded all
three onto verse 1, so a chapter carrying two encodings of one verse rendered
verse 1 twice, in two paragraphs, each claiming to be the verse the edition
numbers 1. **V6 rejects rather than normalizes**: folding would silently merge
two records that disagree about which is verse 1, which is the failure mode
`src/sources/commentary/passage-commentary-index.yaml` is already recorded as
having. `REVIEW_REQUEST.md` §5 asks a reviewer to rule on rejection for an
edition that consistently pads.

## Terminal state, and the order the bootstrap asks in

`index = bag(index)` at the root: JSON `null` is a valid document and not an
index, and read raw it threw past the request catch and left "Loading…"
standing for ever. `startFailed` is now a transaction — it invalidates pending
render work, clears the tally, blanks the testament line and completes focus —
so a render in flight can no longer repaint over the failure.

**And the canon is checked before the address is judged.** Judged against an
empty canon, the page answered *"book=Gen is not a book of this canon"* — a
claim about the canon, drawn from a parse failure, presented to the reader as a
fault in their own address. **The review did not name this defect.** It
appeared only while writing the required regression, because a null index
reached `hashProblems` before it reached the render funnel. `REVIEW_REQUEST.md`
asks whether correcting an unnamed defect found this way belongs inside a
bounded correction.

## No real corpus value is refused

The grammars above were applied to every tracked value they gate. The regular
expressions were read out of `src/web/browser/catena/catena-model.js`; the
values were read out of `src/web/data/` and `src/sources/bibles/` at the head.
**Nothing the corpus holds is refused.**

| Values | Count | Gated by | Refused |
| --- | --- | --- | --- |
| canon book tokens (`src/web/data/structure/catena/index.json`) | 73 | `bookToken` | 0 |
| canon book paths | 73 | `ident` | 0 |
| canon chapter counts | 73 | `whole` | 0 |
| canon testaments | 73, all `old` or `new` | `TESTAMENTS` membership | 0 |
| held-index book paths | 61 | `trail` | 0 |
| held-index `present` members | every one a positive integer | `whole` | 0 |
| index `texts` prefix | 1 | `trail` | 0 |
| fragment ids (562 chapter spine files) | 1,356 occurrences, **1,351 distinct** | `ident` | 0 |
| work ids | 227 occurrences, **12 distinct** | `ident` | 0 |
| chapter-file `text_prefix` | 562 occurrences, 1 distinct | `trail` | 0 |
| source languages | 3 distinct | `tongue` **and** `voiceLanguage` | 0 |
| absence work-id keys | 8 | `ident` | 0 |
| absence languages | 1 distinct | `tongue` | 0 |
| refusal rows | **112**, every one `kind: displaced` with a sound `note` | `refusalNote` | 0 |
| refusal edition keys | 7 | `ident` | 0 |
| published edition ids (`src/web/data/bibles.json`) | **7** | `ident` | 0 |
| published edition languages | 7 | `tongue` | 0 |
| paragraph-layer edition keys and paths | 7 and 7 | `ident`, `trail` | 0 |
| paragraph break marks (5,547 files) | 16,710, only `printed` (2,970) and `projected` (13,740) | `BREAK_KINDS` | 0 |
| paragraph break keys | 16,710 | `^[1-9][0-9]*$` | 0 |
| verse keys, all 7 tracked editions (`src/sources/bibles/`, 9,387 chapter files) | **252,288** | `^[1-9][0-9]*$` | 0 |

The last row is the load-bearing one for the padded-key decision: **no tracked
edition pads a verse number**, so rejecting `"01"` refuses nothing any edition
in this corpus writes. The same sweep over the built site
(`build/public-alpha/site/browse/`) gives the same 9,387 files and 252,288 keys
with none refused, and the served catena index is byte-identical to its source
copy — so the served surface and the tracked source agree.

Every figure above is reproducible at the head with a read-only walk of those
two directories; `checks.txt` Y records the sweep. **This is real-corpus
evidence, not fixture evidence.** Everything the regressions exercise is
fabricated, and `EVIDENCE-INDEX.md` marks each artifact as one or the other.

There is one refusal the corpus does exercise and this table cannot show: no
tracked absence row carries `not-surveyed`, so the clause that names it is
proven only by fabricated fixtures.

## What was not weakened

- The four gzip ceilings are the parent's constants, unraised.
- `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html`
  are byte-identical to the parent.
- `MODEL_SHA256` was re-pinned, deliberately, because
  `src/web/browser/catena/catena-model.js` changed deliberately. It reads
  `adb61eb7…` at the head, which is the model's actual digest and the value
  `release-bindings status` reports as stale. That leaves one release binding
  stale, unsigned and correctly fail-closed. **It was not re-signed.**
- Ten oracles that expected the defects were corrected in place, each with its
  reason recorded in the file, in nine `CORRECTED ORACLE (V6)` blocks across
  five pre-existing classes — not deleted, and not relaxed to accommodate
  output. `CORRECTED-ORACLES.md` is the per-oracle record. One of those five,
  `NumericVerseAndPathTest`, does not fail at the parent, and
  `BASELINE-COMPARISON.md` keeps it out of the regression count for that
  reason.

## One disclosure about the source itself, found and fixed

The separator in the `absenceRows` tie-break key was written as a **raw NUL
byte** rather than as its escape, from the first commit of this correction to
the third. Line 670 of `src/web/browser/catena/catena-model.js` now reads

```
const rank = (one) => sound(one.reason) + '\u0000' + sound(one.partial);
```

and the fourth commit, `83cb63b61`, is what put the escape there.

Nothing about the running page changed. The string value is identical either
way, the comparison is by length first and the separator's own length is
constant, no test pinned it, and no behaviour moved: the focused suite is 423
green at the head and `catena check` passes at both ends.

What it cost was the reader of the evidence. `file` called the model `data`,
and `grep`, `diff` and every pager treated the production source — and the
patch shipped beside it — as **binary**, reporting "Binary file matches"
instead of the matching line unless invoked with `-a`. A separator nobody can
see in the file they are reviewing is the wrong separator.

The check that would have caught it now ships at both ends: `file
src/web/browser/catena/catena.js src/web/browser/catena/catena-model.js`
returns `JavaScript source, Unicode text, UTF-8 text` for both files at the
parent (`logs/misc-checks-parent.log` §E) and at the head
(`logs/misc-checks-head.log` §G). The parent is text, the head is text, and the
three commits between were not. This is recorded rather than quietly repaired,
because the defect was this lane's, it was invisible in the artifact that
carried it, and it was found by a verification pass rather than by any check
this package would otherwise have run.
