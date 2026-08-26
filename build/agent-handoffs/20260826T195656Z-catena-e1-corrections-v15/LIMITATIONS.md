# Limitations — E1 Catena correction V15

Each heading is one thing this lane did not close, or closed only within a
stated boundary. Nothing here is presented as done.

## Three explanations were moved out of the page and into the unbudgeted model

`src/web/browser/catena/catena.js` had 28 gzipped bytes of headroom under its
13,000 ceiling when this lane started. To hold under it, three paragraphs of
the page's own prose were relocated into
`src/web/browser/catena/catena-model.js`, which carries no ceiling: why a 200
that is not a spine is not an empty chapter; why neither the paragraph layer
nor its index may decide the page; and what the absence disclosure may say.
The page keeps a one-line pointer to each.

This is a cost, not a tidy-up. A reader of `src/web/browser/catena/catena.js` now follows a pointer
for three explanations that used to stand in front of them, and the file that
receives them is the one file in this pair whose growth nothing governs. The
alternative was raising a ceiling, which this lane is not authorized to do.

## The edition-accessor and observation-accounting work closes proof gaps, not defects

Two of this lane's vectors prove things the parent already did correctly. The
nested EDITION accessor case was promised by the previous lane and not asked;
asked directly, it answers coherently across edition, printing, provenance
line, rights, voices and readable state **at the parent as well as at the
candidate**. The observation accounting likewise counts what was previously
asserted. Neither is a production correction, neither is counted among this
lane's semantic closures, and the record would be false if it implied
otherwise.

## The observation claim is narrower than "the record is observed once"

Over one sources record there are three `getOwnPropertyDescriptor`
observations per source key — `Object.hasOwn` counts among them, because it is
`[[GetOwnProperty]]` — two per shared field the record states and one per
field it does not, one key enumeration, and nothing further on a second
render. What is proved is that no consumer runs a hostile value accessor and
that no consumer reaches past the projection to observe the record again. It
is not proved, and not claimed, that the record is observed a minimal number
of times. `CLAIM-CLOSURE.md` §6 states the full accounting.

## The model is unbudgeted and grew again

39,724 to 41,077 gzipped whole and 9,396 to 9,536 stripped, against no
ceiling in either column — and this lane deliberately added prose to it, as
above. Whether the model and the combined route payload need a governed
ceiling is the budget owner's question, and it is older with every lane that
discloses it.

## `src/web/browser/catena/catena.js` is still against its ceiling

12,958 gzipped whole against 13,000. The page is smaller than the parent left
it and larger stripped, 7,546 to 7,724 against 8,800. A later lane adding page
prose will hit the whole-file ceiling before it hits a defect, and this lane
has already spent the ordinary answer to that problem.

## Eight of the nineteen new methods pass at both endpoints

They pin behaviour that already held. They are recorded as coverage and
controls and are not counted among the closures. Fourteen methods fail at the
exact parent; `DERIVED-CLAIMS.md` and `checks.txt` carry the run figures.

## The model byte-identity hash pin is a pin, not a closure

It is one of the fourteen parent-failing methods, and it fails at the parent
because the model's bytes differ, not because the parent's meaning was wrong.
It is classified as a pin wherever it is counted.

## Ownership is recorded in shipped bytes, at the sink

`M.bodyAsked(row, content)` is asked at the body application in production
code, and `M.rowTransport(row)` mints the owner object there too. Recording
the ownership where the effect happens is why the proof is about what the
consumer received rather than about what a second call would have returned —
and it means the observation seam is in shipped bytes, not in the harness.
That was already true of the identity recorder the previous lane introduced;
this lane adds to it rather than removing it.

## Concurrent same-path requests are no longer deduplicated

Two owners at one address now do two pieces of transport. Sharing in-flight
work by path is the mechanism that leaked, so it is gone rather than repaired.
The settled map still prevents a second retrieval once an answer exists, but
the concurrent case costs a request it did not cost at the parent.

The cost is measured rather than left open. Across all 562 chapter spines under
`src/web/data/structure/catena/`, holding 1,356 fragments, **no chapter has two
fragments sharing a text address or an id**, so no page served from the tracked
corpus has two owners for one address at all and the concurrent case does not
arise on any real route. The ordinary first-load request count is pinned
exactly and is unchanged. What is NOT measured is a corpus this project does
not yet hold: a chapter that legitimately stands two fragments on one text file
would pay one extra request per additional owner, once, until the answer
settles.

## Two attempt ledgers of this lane are retired, and both are disclosed here

Neither was rewritten. A ledger this lane could not carry forward was set down
whole and a fresh one opened, and what each contained is stated here so a
reviewer meeting either file can tell which it is.

**The first** was opened when the batteries were started against a head that a
records correction then superseded. It allocated attempt ordinal 1 and recorded
three completed parent steps — the focused Catena suite, the Catena structural
check and the promise ledger — before the operator stopped it. It has no
terminal row because nothing terminated it. It is 2,501 bytes over five rows,
SHA-256 `64683c0b8bb9624278cb136e8e8cbcbd4875bff571a1a128a870bdb6cb01ed90`.

The correction that superseded the head is worth naming, because it is the kind
of thing this record exists to catch: the durable records said the review this
lane answers is the first in the sequence with a published commit. It is not.
Every review from V5 to V12 was published; V13's alone was not, and that is the
gap V14 recorded.

**The second** carried both batteries to completion and then five package
attempts, four discarded and one that reached its sealed terminal row. It is
45,619 bytes over eighty rows, SHA-256
`5b0c380cf7fab7b507dfedd6bdc0a6ade71cea38522937bf1a6bf851565ec117`. It was
retired because of a defect in the OPERATOR's inputs that the ledger's own audit
caught and would not let past: the package timestamp had been chosen an hour
before the attempts it named, and an attempt id that claims to have been minted
long before its own first row is exactly what an anti-backdating rule exists to
refuse. Every package attempt in that ledger shares one timestamp by
construction, so no later attempt in it could ever have passed. The ledger was
therefore set down rather than argued with.

**No archive was produced by either.** The four discarded package attempts were
refused at P2, P5, P5 and P4 — an evidence-index reference to a bare tool name,
a discarded predecessor's log root named but not shipped, the same again, and an
ambiguous battery log created by staging a predecessor's transcripts — and the
fifth was refused at the ledger audit before P7 ever ran. Not one of them wrote
a ZIP, and no figure in this package comes from any of them. Every number here
was measured again, from the beginning, in the authoritative cohorts this
package ships.

Both retired files are kept whole outside the package. They are not shipped:
they are evidence for nothing, and shipping a ledger no claim rests on would
invite exactly the confusion this section exists to prevent. Their digests are
above so a reviewer handed either can tell which it is.

## The V13 independent review still has no published ref

`origin` carries no `review/catena-wave-1-e1-corrections-v13-independent`, and
this lane cannot publish another lane's review. The V14 review **is**
published, at `0d11766ec232b2b4e46a7d1b0ada56ef22370004`, so the provenance
chain is intact from that link forward and broken at the one before it. The
gap is left empty.

## V13's `authority-negative-fixtures` requirement is not answered here either

This lane's scope is transport ownership and the evidence defects the V14
review named; it does not dispose of a promise the review did not raise. The
promise ledger — 40 tracked, 19 complete — is the authority on that
requirement's state, not this file.

## The attempt history's own disclosures are in the history, not here

The V14 review found a history claiming `complete` and `append-only` while
omitting a set-aside cohort and the P10 rows and while disclosing a row
replacement. This lane corrected the record so that those disclosures are
made where the verdict is made. `PROVENANCE.md` and the packaged history are
the authority on what this lane's own history contains; nothing about it is
restated here, because a second copy of a disclosure is how the first one goes
stale.

## P10's rows reach the slice beside the archive and cannot reach the member inside it

The slice beside the archive now carries them: `<package>.attempts.jsonl` is
derived at P9 and is inside nothing sealed, and every row appended to the lane
ledger after that point is mirrored into it — P9's own derivation row, both P10
gate rows, the executed-tool re-render row and the P10 completion row.

The in-package member `logs/attempts.json` does not, and the reason is
structural rather than an oversight. It is written at P5, proved by the manifest
at P6 and sealed into the archive at P7; P8, P9 and P10 all run afterwards. The
rows do not exist when the member is written, and adding them later would mean
rewriting a sealed archive and re-taking a manifest already verified against the
ZIP's own bytes. Nothing in this lane mutates a sealed archive, so that member
stops at P5 and always will.

A reviewer who wants the gates' rows reads the sibling. The in-package record
that P10 ran is the pair of gate transcripts named in `HANDOFF.md` §10.

## The discard and supersession markers are covered by no sanitize pass

`<pkg>/DISCARDED.txt`, `<pkg>/logs/DISCARDED-<attempt>.txt`,
`<zip>.DISCARDED.txt`, `<stamp>-<name>.SUPERSEDED.txt` and a battery's own
`DISCARDED-<attempt>.txt` are outside every sanitize walk and every named
sibling list, and `logs/assemble.sh` skips the outer sanitization phase
entirely on a run that has already failed — which is exactly the run on which
a marker exists. Their contents are symbolic by construction, and this
package's standard is that "by construction" is an argument and not a check.
No such marker is committed for this lane's authoritative attempt unless one
exists, and if one does it is scanned by hand with the sanitizer's file mode
before it is added.

## Four release bindings remain stale and unsigned

`src/web/browser/catena/catena-model.js`,
`src/web/browser/catena/catena.js`, `src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html`. None is re-signed by this lane; all four
fail closed under `make -k check`, which is the correct behaviour and not a
defect this lane may clear. The CSS and the HTML are byte-identical to the
parent and are stale for reasons this lane did not create.

## Screenshots are omitted

`src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html` are byte-identical at both endpoints, and
the visible differences this lane produces are adversarial-only: they appear
when one owner's request is held against another's. They are asserted at the
exact DOM sinks, including the rendered `Loading…` and the rendered body text,
rather than photographed. `guidance/external-review-handoffs.md` requires
raster evidence where a review concerns browser-visible behaviour; this one
concerns transport ownership, and the DOM assertions are exact.

## The browser gate is red

2,290 assertions at the candidate: 1,836 pass, 226 fail, 228 skip, over 171
pages and 19 routes. The failures fall entirely in three inherited classes —
117 nested `main`, 82 target size, 27 skip link. It is compared against the
parent report rather than passed; the comparison is in the gate transcripts
named in `HANDOFF.md` §10. Nothing in this lane touches its causes.

## `make -k check` is red

It exits 2 on exactly four inherited targets: `check-web-editions-current`,
`check-release-bindings`, `check-tool-registry` and `check-examples`. Compared
as a set, not as an exit code.

## The packaged parent-only PDF error is not fixed and not claimed

`test_pdf_review.PdfReviewCommandTests.test_repeated_signals_do_not_interrupt_child_cleanup`
was established by the previous review as an unrelated signal-timing flake,
separately owned. This lane does not touch PDF.

## Every broader E1 blocker stays open

Full sole-source semantic projection beyond this bounded chapter; orphan raw
sources; source-only fragments still counting; scalar and nested translator
coercion; malformed and padded absence rows; the broader selection and
ordering defects; refusal verse typing; unreadable roots and the unreadable
`src/web/data/bibles.json` prose; the broader terminal and corrected-oracle
proofs; the CLI/web duplicated semantic model; the historical data seam.
Release bindings, the common gate, B0/shared shell, real-device and
assistive-technology evidence, protected Liturgy and PDFs are separately
owned. E1 is not integrated: `origin/main` stands at
`e4085889fc1b3d2e6721b21166394fe5ea2dea9b` and nothing here is merged into it.
