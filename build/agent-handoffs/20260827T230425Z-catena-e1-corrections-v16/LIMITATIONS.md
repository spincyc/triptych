# Limitations — E1 Catena correction V16

Each heading is one thing this lane did not close, or closed only within a
stated boundary. Nothing here is presented as done.

## The page is larger than the parent left it, and this is the first version that cannot say otherwise

`src/web/browser/catena/catena.js` moves from 12,958 to 12,965 gzipped whole
against its 13,000 ceiling, and from 7,724 to 7,835 stripped against 8,800.
Every version from V4 to V15 could report the page smaller than its
predecessor. This one cannot.

The ceiling had 42 gzipped bytes of headroom when this lane started, and the
correction is not payable out of 42. The ordinary answer was applied and it was
not enough: the three sentences the page may say about a body, the presentation
decision itself and the page's paragraph on its one point-of-use acknowledgement
channel were relocated into `src/web/browser/catena/catena-model.js`, which
carries no ceiling, and the page kept pointers. That paid for most of the change
and not all of it, and the page ends seven gzipped bytes above where V15 left
it. No ceiling was raised, and no load-bearing comment was trimmed to buy a
smaller number, because a comment removed to make an arithmetic sentence true is
a cost paid by every later reader of the file.

## Thirty-five gzipped bytes of headroom is not enough for the next correction

That is what is left under the whole-file ceiling. A later lane adding page
prose, or a page-side branch of any size, will hit the ceiling before it hits a
defect — and this lane has already spent the ordinary answer to that problem
twice over, since V15 spent it once and this lane spent what remained. The next
correction on this page either arrives with a raised ceiling, which no
correction lane is authorized to grant, or arrives with more of the page's own
explanation living somewhere the page is not.

## The model is unbudgeted, grew again, and now has no governing ceiling at all

41,077 to 44,247 gzipped whole and 9,536 to 10,344 stripped, SHA-256
`64a75834abd8f9efa25ae52c76b904a3437ab96a9508ba82309211215d44c3a3`, against no
ceiling in either column — and this lane deliberately added prose and behaviour to it,
as above. This is the sharper form of a disclosure V15 made about combined
route-model payload growth: the file that absorbs every overflow from a
budgeted page is the file nothing governs, and each lane that pays a page
ceiling out of it makes that fact larger. Whether the model and the combined
route payload need a governed ceiling is the budget owner's question, and this
lane raises no ceiling and proposes none.

## Two fixes were identified, costed, and deliberately not made

An adversarial review of the production change found two improvements worth
making. **Neither was made, because each costs more gzipped bytes than the
unraised ceiling has**, and this lane records that rather than paying for it by
raising a ceiling or by trimming load-bearing prose.

**The cache-hit branch tests the finished value for truthiness rather than
asking `fragmentTexts.has(path)`.** A sealed value is always a non-null frozen
object, so on today's schema the two tests cannot disagree and the branch is
exactly correct. It is a latent trap only if the schema ever admits a falsy
sealed value, at which point a cached answer would be silently refetched.
**Cost to fix: 37 gzipped bytes, against 35 of headroom.** It does not fit.

**The body write assigns the class before the words.** Reordering so the words
land first would leave the page wholly untouched by a write that throws before
the body lands. No such throw is reachable — `T.el`, `licence`, `insertBefore`,
`appendChild` and concatenation over `sound()`-typed strings do not throw on
real data — and **the reorder costs about 60 gzipped bytes**, because it breaks
a repeated pattern gzip was compressing. That ordering is also why both
write-failure modes leave the acknowledgement block standing, which is pinned
below.

Both are disclosed, costed and deferred, so that the next lane inherits a
decision rather than a discovery.

## A refused body application now leaves no journal entry at all

V15's `M.bodyAsked(row, content)` called `witnessed('body', …)` unconditionally,
before returning its verdict, so **every attempt was witnessed including every
refusal**: a stale or cross-owner application that the boundary turned away
still left a `body` row in the request journal saying it had been turned away.
V16 moved the record after the write. `M.bodyApplied` appends only when the
completion is still owner-valid **and** `wrote === true`, and `M.bodyAsked`
itself witnesses nothing.

The consequence is exact and it is a real loss: the journal no longer
positively records that a stale or cross-owner application was declined. The
negative cases are still proved, twice over — by the boundary returning `false`
in a committed direct assertion, and by the rendered page being unchanged — but
the page-level journal ROW that V15 had is gone, and a reviewer who expects to
audit refusals from the journal alone will not find them there.

This is a deliberate consequence of taking the record AFTER the write rather
than before it, which is what the review required. It is disclosed as a cost of
that correction and not as an oversight.

## The completion envelope's halves cannot be supplied by the DATA, and no more than that

`M.textCompleted` and `M.textFailed` mint an envelope only against an owner the
model is currently holding for that owner's own row and only around content the
model itself finalized, and membership is sealed in a `WeakSet`, so a
same-shaped literal is not one of these. **A hostile chapter, source record or
fragment file therefore cannot mint either half**, because neither is derivable
from anything the data carries. That is the defect the review found, and it is
closed.

**It is not a security boundary against code already running in the realm.** A
recorder installed through the exported `chapterWitness` receives the page's
actual row objects, and from a real row both `M.rowTransport` and
`M.textPayload` will mint valid halves in about five lines. In-realm code can
also write the DOM directly and needs no envelope at all. Any unqualified claim
that the two halves "cannot be supplied from outside" is refutable by a
five-line probe, and no such claim is made in this package.

## The confirmed write is confirmed over the body, not over everything beside it

`M.bodyApplied` appends only after the page reads the node back, and what it
reads back is `text.textContent` — the fragment's words. The acknowledgement
block and the `Extent —` and `Date —` apparatus paragraphs that may be appended
alongside are **not** confirmed. A journal entry therefore means the body
reached the page; it does not mean that every node beside it did.

That boundary is **pinned rather than asserted in prose**: the two
write-failure modes leave DIFFERENT partial states, and the suite fixes both. A
silent non-take still draws the `Extent —` and `Date —` apparatus, because the
assignment returned and everything after it ran; a throw draws none of it; and
**both** leave the acknowledgement block standing, because it is written before
the words.

What is closed is the negative claim, and it is the one that matters for the
defect: a body that did not reach the page leaves no entry saying it did. A
write that throws and a write that silently does not take both append nothing.
**The retry flag is deliberately NOT reset in the write's `catch`.** An earlier
revision reset it there; the reset was removed after an adversarial review found
it created an incoherent arm — a throw AFTER the body had landed would leave the
body on the page, no journal entry, and an invited second full application out
of the memoised completion. `asked = false` occurs only in the transport-failure
arm, because a network failure is retryable and a failed DOM write is not, and
both write-failure modes now end identically: no entry, no false success, no
second attempt. **The disclosed consequence is that a write which silently does
not take leaves the fragment showing its previous state with no way for the
reader to retry.** No such failure is reachable in a real DOM; it is disclosed
because the arm exists. Nothing in this package
should be read as a stronger confirmation than the code performs.

## A row that resolves no address now mints a transport owner, and the journal shows it

`M.rowTransport(row)` is consulted unconditionally in `fragmentText`, where V15
consulted it only when an address resolved. A projected row whose record names
no text file therefore produces a transport owner — its `path` is `''` — and one
`transport` witness, where V15 produced neither. That is deliberate: "this
fragment carries no text file" is a body application like any other, and it must
be owned by a completion the model sealed rather than applied on a bare
row-membership test. The consequence is that the request journal carries one
more transport row for such rows than V15's did. It is disclosed here rather
than left for a reviewer to find as a count that moved without explanation.

## The publication and mutation vectors are reachable only through the replay harness

No browser engine in this package witnesses a reentrant path lookup, a payload
whose prototype is mutated after caching, or a `textContent` write that does not
take. They are reachable one way: the replay harness, which drives the real page
under Node against a stub DOM and a stub network. The states are properties of
when a value becomes reachable and what it is made of, not of any JSON document,
and no real server or reader produces them — which is why they are adversarial
and why the browser gate cannot see them. The assertions are exact and taken at
the page's own sinks; they are not raster evidence and are not presented as any.

## The publication probe is in the engine, not in the page

`fragmentTexts` is a module-scope `Map` inside the page's own IIFE. Nothing
exported reaches it, and adding an export so a test could look would be the test
changing the thing it asserts about. `Map.prototype` is therefore wrapped once
for the whole replay realm, answering exactly as it did, recording only a string
key carrying the probed path and only while a scenario has asked for a probe.
The assertion that results is about what the engine saw, not about what the page
published, and a reviewer should read it that way. The structural fact beside it
— that the value handed to `set` is the return of a function that has already
run to completion — is what carries the claim; the probe corroborates it at
every instant this lane could name, and cannot prove that no instant exists
which nobody named.

## The completion envelope is unforgeable and opaque

Membership is a `WeakSet`, which is exactly what makes a same-shaped literal
refusable from outside the module. It also means a value that looks correct in
every observable respect can still be refused, and a reviewer reading a value in
a debugger cannot see why. Unforgeability was chosen over legibility here, and
`REVIEW_REQUEST.md` puts that trade to the reviewer rather than presenting it as
neutral.

## Ownership is recorded in shipped bytes, at the sink

`M.bodyAsked` and `M.bodyApplied` are asked at the body application in
production code, and `M.rowTransport` and `M.textCompleted` mint their objects
there too. Recording the ownership where the effect happens is why the proof is
about what the consumer received rather than about what a second call would have
returned — and it means the observation seam is in shipped browser bytes, not in
the harness. That was already true of the identity recorder two lanes ago; this
lane adds to it rather than removing it, and it is now a third lane in a row
doing so.

## Some of this lane's work closes proof gaps, not defects

The provenance-specific `===` assertion and the observation-accounting
correction close gaps in the RECORD that the V15 review named. The parent
already resolves provenance through the authoritative object, and the parent
already performs the prototype observation this lane now counts; what changed is
that the claim is proved and stated instead of asserted. Neither is a production
correction. They are counted among this lane's semantic closures because the
review named them as required changes, and they are described in
`CLAIM-CLOSURE.md` as what they are rather than as behaviour that was wrong.

## Preserved V15 behaviour is regression, and is counted as regression

The row-transport owner model, the A-held/B-independent vector and its terminal
fields, the wrapper-created-authority closure, the per-name substitute record,
failure isolation and owner-local retry, the hostile accessor cases, the
throwing mutations, the downstream rerender and the inherited V14 closures are
all replayed here and all still pass. **None of them is counted among this
lane's closures.** **11** of this lane's 48 new methods pass
at both endpoints; they pin behaviour that already held, and they are recorded
as coverage and controls. A byte-identity hash pin is a pin and a consumer-roster
audit is an audit, and neither is a semantic closure. The V15 review found those
categories conflated, and the record would be false if it repeated the
conflation.

## This lane's evidence tooling is its own work, and its verdict on it is not independent

Most of the evidence closures are corrections to tools this package ships under
`logs/`. A pipeline that was wrong about seven of its own command rows may still
be wrong about an eighth; a classifier that no longer accepts prose by prefix is
not thereby a correct classifier; and a completeness checker that models the
failures it has been shown does not model every failure of its kind.
`REVIEW_REQUEST.md` asks the reviewer for that verdict rather than recording
one.

## A battery of this lane was stopped from outside itself, and contributes no validation result

The head battery of ordinal 06, attempt `head-20260827T150233Z-06zg9rhq`, was
**externally interrupted**: the background process running it was terminated by
something that was not the battery, after three steps had passed green. No step
failed and no guard refused. Its execution disposition is terminally
**`abandoned`**, its evidence disposition is **`unevidenced`** and permanently
so, and its reason is recorded verbatim on its own ledger row and quoted in
`PROVENANCE.md` §13.

**It contributes no validation result to any authoritative V16 claim** — not a
count, not a size, not a digest, not a pass and not a fail. The head cohort was
measured again, cold and from the beginning, first under ordinal 07 and — once
P8 had refused that cohort's driver bytes — again under ordinal 16, and every
head-side figure this package reports comes from the transcripts of attempt
`head-20260827T194839Z-166gh2tz`.

Attempt 06's partial cohort is **retained for history and audit only**, outside
this package, with a digest listing of every file it wrote. It is retained
because destroying the record of an interrupted run is how a history comes to
look tidier than it was; it is outside the package because it supports nothing
in the package. The limitation, stated plainly: a reviewer holding this archive
cannot inspect that cohort, and nothing here asks them to, because no claim
depends on it.

## A completed cohort of this lane measured a head this package does not report

The head battery of ordinal 05, attempt `head-20260827T144631Z-05qmtgwx`, ran
to completion and every step of it passed:

    execution disposition = complete
    evidence disposition  = set-aside
    reason                = it measured a superseded V16 head

It measured head `251900b14`. Commit `cc1f2fb86` then removed from the lane
record the figures a record cannot truthfully state about itself, so the head
this package reports is not the head that cohort measured. **No final validation
figure in this package derives from attempt 05.** Its `complete` row is
untouched — setting a cohort aside appends a row on the evidence axis and
alters nothing about how the attempt ended — and the shipping-head measurement
source is now attempt `head-20260827T194839Z-166gh2tz` of ordinal 16, exactly as
the shipping-parent source is attempt `parent-20260827T193049Z-15pnpphq` of
ordinal 15. The section below records why those, and not the cohorts of ordinals
04 and 07 that first held the disposition.

The limitation this creates is small and is stated anyway: a reader comparing
this package against the lane's raw log directories will find a head cohort
whose figures are not the ones reported here, and the ledger row rather than
this paragraph is what tells them why.

## Two cohorts of this lane were recorded authoritative and were then superseded

The cold parent cohort of ordinal 04, attempt
`parent-20260827T143106Z-04hy5j4v`, and the cold head cohort of ordinal 07,
attempt `head-20260827T154350Z-079xrp6n`, ran, completed, and were recorded
`authoritative` the moment their batteries ended — before any package had been
sealed from them:

    execution disposition = complete   (unchanged, and it still says complete)
    evidence disposition  = authoritative, and then superseded
    reason                = what ran was not what shipped

**What caught it was P8**, the phase that compares each tool's EXECUTED digest
against the trusted anchor and against the copy the package SHIPS. Those
cohorts had executed `logs/battery.sh` at
`04ca35cb5969aea92d983c9793b5dc2d0d427c8a0ca356fa91db95bb8cc58c9c`; this
package ships that driver at
`cca4d2840116e2e101c68d9bdf8db1305f545b838015a837514f4464b73b947c`. The
verifier refused the archive in exactly those terms, and the whole difference
between the two files is header comment prose — the driver's header was
rewritten when this lane split execution disposition from evidence disposition.
**The check is right, and an accurate account of the difference is not a
defence.** An archive whose shipped driver is not the driver that took its
measurements cannot say which copy any of its figures is about, however innocent
the changed bytes turn out to be; the remedy is to measure the endpoints again,
not to argue the difference away. That is what was done, and this section is the
disclosure of it rather than a footnote to it.

**The limitation, and it is a limitation of the record and not only of the
run.** Because the evidence disposition had already been recorded, and a
battery's evidence axis was strictly irreversible, there was at that moment no
verb in the ledger for what had plainly happened: those cohorts could not be set
aside, because they had been carried, and they could not be un-recorded without
deleting a row that was true when it was written. The battery axis therefore
gained the one succession the package axis already had,
`authoritative → superseded`, on the same reasoning — refusing it would leave
deleting the predecessor's history as the only available remedy, which is the
V12 defect rather than the cure. `superseded` is terminal, nothing follows it,
and the `authoritative` row it follows is left exactly as written, because those
attempts really did hold that disposition for the time they held it.
`set-aside` stays terminal and cannot be superseded, because that would assert
a cohort had once been carried when it never was.

**The lesson, which is the generalisable part and is stated rather than
implied.** An evidence disposition of `authoritative` belongs AFTER a seal has
proved that a cohort's tools are the shipped ones — not at the moment a battery
ends. Recording it early is what made this correction necessary, and this
package says so rather than presenting the shipping cohorts as though they had
always been the only ones. Both endpoints were measured again against frozen
drivers; every tool the shipping batteries executed — `logs/battery.sh`,
`logs/gate-summary.py`, `logs/gzip-sizes.py` and `logs/journal-dump.py` — matches its shipped
copy byte for byte; and that identity was established before any evidence
disposition was recorded the second time.

**They reproduced the same cold counts, and that is recorded as a CONTROL and
as nothing more.** Two independent pairs of cold runs landing on the same
`divergent_rows`, `distinct_divergent_identities`, `volatile_rows` and
`total_differing_rows` is a small check that the figure is a property of the
measurement rather than of one run, and it is worth recording for exactly that
and for nothing else. **Authoritative V16 validation derives from the cold
cohorts under ordinals 15 and 16 and from no other cohort**, and no sentence in
this package presents ordinals 04 and 07 as a source of any figure.

**What a reviewer holding this archive cannot do.** No figure in this package
derives from attempt 04 or attempt 07, and their transcripts are not members:
they are retained local-only under
`spincyc/v16-retired/attempt-04-07-driver-drift/`, beside a sidecar listing
every file they hold. A reviewer can identify that tree by digest and file count
and cannot audit its contents from this package, and no claim here asks them to.
`PROVENANCE.md` §13 carries both ledger rows with their recorded reasons and
§15 the retention table.

## Every cohort this lane did not carry is retained outside the package, and none of them may support a figure

**The governing rule: no authoritative claim in this package requires an
unsanitized, builder-local artifact.** The figures come from the two shipped
cohorts, `logs/attempt-15/` and `logs/attempt-16/`, which are members and are
scanned and re-scanned like every other member. Five cohorts are retained
local-only, under `spincyc/v16-retired/`, each beside a sibling `.sha256`
listing every file it holds: `attempt-01-refused` (12 files, 785,632 bytes),
`attempt-03-warm` (14 files, 10,112,329 bytes), `attempt-04-07-driver-drift`
(27 files, 19,669,322 bytes), `attempt-05-superseded-head` (13 files, 9,556,761
bytes) and `attempt-06-abandoned` (5 files, 110,007 bytes). The middle one holds
both superseded cohorts, the parent of ordinal 04 and the head of ordinal 07,
in one tree because one cause superseded both. `PROVENANCE.md` §15 carries the
table with each cohort's evidence status and the reason it was retained.

**None of them is shipped, and the reason is the same one that kept V15's
retired ledgers out**: they hold raw pre-sanitization absolute paths, they are
evidence for nothing this package claims, and shipping unscanned bytes into a
sealed archive is the defect rather than the disclosure. A reviewer handed one
can identify it by digest and file count. A reviewer who wants to audit its
contents cannot do so from this package, and no claim here asks them to.

The first of those directories is named `attempt-01-refused`, and the name
predates the terminology correction this lane made: that attempt's execution
disposition is **`failed`**, with **guard refusal** as its cause. The directory
name is left as it is rather than rewritten, because renaming a retained
artifact to match later prose is how a record stops being a record.

## This lane retired a ledger, and does not claim otherwise

The V15 review's finding about ordinals was that allocation had been
file-scoped, so moving a ledger aside restarted it and one lane reissued
ordinals across three files while each file's own identity row truthfully said
an ordinal is never reissued. **This lane also retired a ledger — once,
deliberately — and it would be dishonest to present that as a lane that kept
one file.** `build/agent-handoffs/attempt-ledger.jsonl` holds ordinals 1 to 3
and is retired, 21,536 bytes over 29 rows, SHA-256
`d7fd68ce256f94d1efca59d3248960a5d6d6999ea4aa2d06c60cf6cb2c901d87`;
`build/agent-handoffs/attempt-ledger-02.jsonl` holds ordinals 4 onward and is
live. Both paths are repository-relative in the builder's checkout, and neither
file is a member of this package or a sibling of it: they are named here by
where they actually sit, because a limitation that pointed at a package member
which does not exist would be a second defect rather than a disclosure.
`PRIVACY-AUDIT.md` records why the retired one in particular is never shipped.

What is different is the guarantee behind it. The retirement verb writes the
predecessor's spent ordinals into the successor's opening lane row, and the
allocator unions them into the spent set, so the second ledger opened at
ordinal 04 and `reused_ordinal_count` is derived across both files rather than
asserted about either. The residual limitation is honest and small: the live
ledger's digest moves every time an attempt appends a row, so it is bound by
name and row count at the seal rather than by a digest, and a digest written
for it in any member would be stale before that member shipped.

## The V15 predecessor history is stated from outside V15's shipped slice

The complete V15 attempt history spans three ledgers, one shipped and two
retired and never shipped. What this package can offer for the two retired ones
is their byte counts, row counts and SHA-256 digests —
`64683c0b8bb9624278cb136e8e8cbcbd4875bff571a1a128a870bdb6cb01ed90` and
`5b0c380cf7fab7b507dfedd6bdc0a6ade71cea38522937bf1a6bf851565ec117` — and a
statement of what each contained. Neither file is shipped: they are evidence for
nothing in this lane, they hold raw pre-sanitization absolute paths in their
`command` fields, and shipping them would put uncovered bytes into a sealed
archive. A reviewer handed either can identify it by digest. A reviewer who
wants to audit their contents cannot do so from this package.

## This lane's own post-seal rows reach the slice beside the archive, not the member inside it

`logs/attempts.json` is written before the manifest is taken and sealed into the
archive; the final verification, the authority record and the publication gates
all run afterwards. The rows for those phases do not exist when that member is
written, and adding them later would mean rewriting a sealed archive and
re-taking a manifest already verified against the archive's own bytes. Nothing
in this lane mutates a sealed archive, so that member stops where it stops and
always will. The slice beside the archive carries every row appended after it is
derived, and the in-package record that the post-seal phases ran is the pair of
gate transcripts named in `HANDOFF.md` §10.

## Four classes of builder-local artifact are outside every privacy scan

The discard and supersession markers, which carry local-offset timestamps and
free-text failure reasons; any retired ledger, whose `command` fields hold raw
pre-sanitization absolute paths; the lane-wide executed-tool journal; and any
retained discarded package tree, one of which in the V15 lane died before its
seal and still holds raw absolute paths. The published archive and its named
siblings are scanned and re-scanned; **these are not**, and this package makes
no broader all-retained-artifacts privacy claim. The V15 review declined that
claim and this lane does not renew it. `PRIVACY-AUDIT.md` states the boundary in
its own words.

## The V13 independent review still has no published ref

`origin` carries no `review/catena-wave-1-e1-corrections-v13-independent`, and
this lane cannot publish another lane's review. The V14 and V15 reviews are both
published, so the provenance chain is intact from V14 forward and broken at the
link before it. The gap is left empty.

## Four release bindings remain stale and unsigned

`src/web/browser/catena/catena-model.js`,
`src/web/browser/catena/catena.js`, `src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html`. None is re-signed by this lane; all four
fail closed under `make -k check`, which is the correct behaviour and not a
defect this lane may clear. The CSS and the HTML are byte-identical to the
parent and are stale for reasons this lane did not create.

## Screenshots are omitted

`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints, and the visible differences this lane produces
are adversarial-only: a prototype's words standing as a fragment's own text, a
body applied under a row that never asked for it, a write that does not take.
They are asserted at the exact DOM sinks rather than photographed.
`guidance/external-review-handoffs.md` requires raster evidence where a review
concerns browser-visible behaviour; this one concerns publication timing, value
shape and application ownership, and the DOM assertions are exact.

## The browser gate is red

It is identically red at both endpoints, at **2,290 assertion ROWS across 17
diagnostic NAMES — 1,836 pass / 226 fail / 228 skip over 171 pages, 19 routes
and 9 states**, on Chromium 151.0.7922.173, and its failures fall entirely in
inherited classes: the 226 failing rows land in exactly three names,
`single-main-element` 117, `primary-controls-meet-target-size` 82 and
`skip-link-targets-existing-element` 27. **Rows and names are stated apart on
purpose**, because reporting one as the other is the defect the previous lane's
diagnostics had. It is compared against the parent
report rather than passed; the comparison is in the gate transcripts named in
`HANDOFF.md` §10. Nothing in this lane touches its causes. The comparison's
localising diagnostics are rebuilt in this lane's tooling, because V15's keyed
them on the assertion NAME alone and collapsed 2,290 assertion ROWS onto 17
diagnostic NAMES; the whole-report equality verdict was sound at V15 and is
unchanged in kind here.

The gate's own figures are reported as three quantities and never folded into
one: `total_gate_rows` **2,290**, `normalized_reports_equal` **yes**, and
`distinct_diagnostic_names_or_categories` **17**. The first is the identity
universe, the second is a verdict and not a count at all, and the third is a
diagnostic vocabulary and not a row-identity universe. No sentence here should
be read as implying that a small diagnostic category count equals the full
2,290-row identity universe.

## `make -k check` is red

It exits 2 on exactly four inherited top-level targets:
`check-web-editions-current`, `check-release-bindings`, `check-tool-registry`
and `check-examples`, at `Makefile:554`, `:598`, `:803` and `:791`. Compared as
a set, not as an exit code. **`check-tool-registry` is genuinely RUN here
because `tmt` is installed; on a box without `tmt` it skips rather than fails
and only THREE targets are red — which is not a change, and must not be read as
one.** `check-examples` reports its divergent rows and its separately declared
volatile lines as two figures of two different kinds, and this package never
sums them into a single count of anything.

**Four measures, named apart, and never collapsed.** `divergent_rows` counts
captured rows the replay marked `DIFF`, and a command captured twice contributes
two. `distinct_divergent_identities` counts the distinct command strings among
those rows. `volatile_rows` counts lines declared volatile in a static source
table and masked before comparison, which are never `DIFF` rows and are no part
of `divergent_rows`. `total_differing_rows` is the sum of the first and third,
stated only as that sum. **At the authoritative V16 cold cohorts, under ordinals
15 and 16, which agree exactly:**
30 `divergent_rows` over 28 `distinct_divergent_identities`, plus 2 `volatile_rows`, for 32 `total_differing_rows`.

**And it never states any of them without the BUILD STATE it was taken
in**, because these figures are state-sensitive: 30 divergent rows over 28
distinct divergent identities on a cold `build/`, and 28 divergent rows over 27
distinct divergent identities on a warm one, from
the same commit and the same command. The entire delta is two captures of
`tools/mass-ordinary check --out build/example-ordinary`, whose comparison
directory a LATER capture in the same target writes. **That is ONE command
identity contributing TWO rows, not two identities** — the set-difference runs
one way only and the cold set is a strict superset of the warm one — and saying
it the other way would be the row-versus-name conflation this package exists in
part to correct. **`check-examples` must therefore be run exactly once per fresh
clone.** This is the root cause of the defect the V15 review correctly caught in
V15's prose: V15 quoted a cold figure while shipping a warm log, and the record
never said which tree it measured. **The warm figures are HISTORICAL, inferred
from shipped V15 evidence, and are not a V16 replay; the difference between them
and this package's cold figures is a MEASUREMENT-SURFACE difference and not a
V16 parent/head behaviour delta**, since the two authoritative V16 cold cohorts
agree exactly on all four measures. This package records
`build-state=COLD|WARM` at preflight, reports divergent ROWS and distinct
COMMAND STRINGS separately, and **pins no constant** — a check pinning 30, or
28, would be wrong in one build state or the other. The mechanical derivation
is the member `logs/divergence-reconciliation.json`, and `PROVENANCE.md` §16
states it in full, including where this lane's reconciliation departs from the
review's own diagnosis.

## `tools/mass-ordinary` has no `PREPARE` entry, and that is not this lane's to fix

The state-sensitivity above is not a property of `check-examples` in general.
It is a property of one tool's captures. `build/example-ordinary` is written by
a later capture in the same target — `tools/mass-ordinary structure --out
build/example-ordinary` — and it is never cleaned up, because `mass-ordinary`
appears in neither the `SCRATCH` table nor the `PREPARE` table of
`scripts/replay_examples.py`. So the two earlier `check` captures compare
against a directory that does not exist on a cold tree and does exist on a warm
one.

**`typeset-bible` has exactly this shape and is already handled**, with a
`PREPARE` entry whose own comment describes the identical problem: the capture
records the second run, which is the one that reports unchanged, because a
first render into an empty tree writes instead. A `PREPARE` entry for
`mass-ordinary` would make its `check` captures state-independent and would
remove the whole ambiguity this lane spent its reconciliation on.

**This lane does not add one.** `scripts/replay_examples.py` and
`tools/mass-ordinary` are outside this correction's scope, and a lane answering
a review about publication atomicity does not quietly change an unrelated tool's
example fixtures. It is disclosed here as an underlying defect belonging to
another owner, recorded in `UNRESOLVED-BLOCKERS.md` with that owner, and left
open.

## The predecessor package's build state is an inference, not a record

Where this package compares its own example figures against V15's, it describes
V15's transcripts as WARM. **That is an inference, and it is stated as one.**
V15's `logs/order-parent.txt` and `logs/order-head.txt` carry no `build-state`
line at all, so nothing in that package records which tree it measured. The
inference is drawn mechanically from V15's own transcripts: the two
`tools/mass-ordinary check --out build/example-ordinary` captures read `ok`,
which is only possible when `build/example-ordinary` already existed and was
current. It is sound, and it is still an inference about a fact no artifact
states.

This lane's battery records `build-state=COLD|WARM` at preflight, so its own
figures never need inferring, and a later reviewer comparing against them is
reading a recorded fact rather than reconstructing one. That is the whole of
the improvement; it does not retroactively make V15's state a record.

## The packaged parent-only PDF error is not fixed and not claimed

`test_pdf_review.PdfReviewCommandTests.test_repeated_signals_do_not_interrupt_child_cleanup`
was established two reviews ago as an unrelated signal-timing flake, separately
owned. This lane does not touch PDF. Where a fresh replay's failure identities
differ from the sealed transcript's, the difference is recorded rather than
hidden, as the V15 review recorded the tool-registry identity it met.

## Every broader E1 blocker stays open

Full sole-source semantic projection beyond this bounded chapter; orphan raw
sources; source-only fragments still counting; scalar and nested translator
coercion; malformed and padded absence rows; the broader selection and ordering
defects; refusal verse typing; unreadable roots and the unreadable
`src/web/data/bibles.json` prose; the broader terminal and corrected-oracle
proofs; the CLI/web duplicated semantic model; the historical data seam.
Release bindings, the common gate, B0/shared shell, real-device and
assistive-technology evidence, protected Liturgy and PDFs are separately owned.
E1 is not integrated: `origin/main` stands at
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` and nothing here is merged into it.
