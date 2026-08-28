# The value that is finished before anyone can see it, and the owner that comes with it

## 1. The findings, and what they actually were

The V15 independent review answered **CHANGES REQUIRED**, recorded at
`67247ecc39a6e5f6224c64ca3ab1af163ee023b1` on
`review/catena-wave-1-e1-corrections-v15-independent`, on two axes: SEMANTIC
CHANGES REQUIRED on transport and final authority, and EVIDENCE CHANGES
REQUIRED on the package. It is published, so this lane's account of a
disposition can be checked against the review itself.

**The first finding is about an instant.** V15 held pending work correctly —
`asking`, keyed on the stable per-row transport owner — and the review said so.
What it did not do is keep unresolved work off the path. `asked` is the promise
returned by `T.loadJSON(path).then(...)`, and `fragmentTexts.set(path, asked)`
ran INSIDE that promise's own fulfilment handler, before the handler returned.
A promise returned by `then` cannot settle until its handler returns, so what
stood at that path at the instant it became reachable was
`Promise { <pending> }`, fulfilling only in the following microtask. The review
probed the exact ordering and observed it. Publication also preceded the freeze.
Ordinary event-loop work cannot interleave there, which is why V15's behavioural
tests were green over it, and a synchronous reentrant operation does not need
the event loop.

**The second finding is about what the shared value was made of.** The value
that eventually stood at that path was the raw parsed JSON object, shallow-frozen
at the top level: not normalized content, not a response wrapper, not a failure
value, not owner-bearing. It kept a mutable prototype, and `M.textPayload` read
its fields at render time by ordinary prototype-sensitive lookup. So a frozen
empty object could change from unreadable to readable after prototype mutation,
between one reader and the next, and an own accessor answering differently on a
second read decided the page. V15's committed oracle checked only top-level
`Object.isFrozen`; it proved neither settled-before-publication nor mutation
safety before a later owner consumed the value.

**The third finding is about the sink.** `M.bodyAsked(row, content)` authorized
any content whenever `row` occurred in `rowOwners`. It received no transport
owner, no completion token, no promise and no generation, and it never compared
`content` with the request made for that row — V15's own direct test
deliberately accepted `{text: "x"}` with no owned completion behind it. An
actual B row therefore accepted arbitrary A content at the boundary. The
production closure supplied the association and the boundary proved nothing.
And the body journal was recorded BEFORE the DOM write, so it said `applied` for
a body that had not been written and could not say whether one ever was.

So the guarantee V15 argued for — that work is owned by the row that asked for
it, all the way to the body — was true of the request and of the pending state,
and false of the publication, of the shared value's contents, and of the
authorization at the sink.

## 2. What the parent actually does

Reproduced at the exact reviewed parent, not argued from the source. A
synchronous reentrant lookup of the path, taken from inside the fulfilment
handler, retrieves an unresolved promise: the parent's path map hands out work
in flight. A payload whose prototype carries `text` renders those words as the
fragment's own, because the parent's projection is a prototype-sensitive read.
An own accessor for `text` is invoked at the parent, so a value that answers
differently on the second read decides what the page says. And an actual B row
handed A's content, or handed a literal no request produced, applies it: the
parent writes it to the page and journals it as applied.

One more thing about the parent is load-bearing. The V15 body-application test
**required the weaker rule to pass**: it asserted that a bare row plus arbitrary
content is a valid application. A test that passes only because the boundary is
open is not a control. It is corrected here, and corrected it fails at the
parent.

## 3. The contract

Six clauses, all of them in `src/web/browser/catena/catena.js` and
`src/web/browser/catena/catena-model.js` and nowhere else.

**A payload is finalized once, at settlement.** `M.textPayload` is the
finalizer, not a render-time projection. Every field is taken by own descriptor
through `ownData`, so nothing inherited is visible and no getter is invoked.
Every field is a scalar by construction: `sealText` admits a boolean or
`sound()`'s string and nothing else, so no nested mutable structure can be in
the result. The record has a null prototype, is frozen, and has the fixed key
set published as `M.TEXT_SCHEMA`. `M.NO_TEXT` is the finished value for a row
that resolves no address at all.

**Only a finished value is published.** `M.textPayload(file)` runs to
completion, and only then does `fragmentTexts.set(path, content)` run. There is
no instant at which a path lookup returns unresolved or partial work, including
from a synchronous reentrant lookup inside the settle handler. The
first-settled-answer rule stands unchanged: a request released late may not
displace an answer another row already has.

**The answer does not travel alone.** A settled transport is sealed into one
frozen envelope carrying the exact `rowTransport` owner beside the finalized
value, minted only against an owner this model is currently holding for that
owner's own row and only around content this model itself finalized. Membership
is a `WeakSet`, so a literal of the same shape is not one. `null` for a forged,
foreign, scalar, `null` or null-prototype owner — fail-closed, one step later
than `rowTransport`.

**The envelope is never shared.** It is per-caller by construction, because the
owner is in it, and it never becomes the path-cache value. A finished value
already in the cache is rebound to a later owner through that owner's OWN
envelope, which is what keeps the cached value owner-independent and keeps A's
owner from crossing into B.

**Application asks the completion, not the row.** `M.bodyAsked(row, completed)`
requires that the completion be one this model sealed, that its owner be the
transport held for that very row, and that the owner's projection be the
projection that made the row. Three exact-object comparisons, none of them a
path, an id or a string.

**The record follows the write.** `M.bodyApplied(row, completed, wrote)`
appends only when the completion is still owner-valid and the write is
confirmed by reading the node back. A write that throws and a write that
silently does not take each leave no entry at all, and the throwing case resets
the retry flag truthfully. Each entry binds the owner object, the row, the
projection, the address, the finalized content value itself, whether the
completion was a failure, and the post-write success state.

A reported transport failure is owned exactly as a fulfilled body is, through
`M.textFailed` and the same sink. A failure is an answer.

## 4. The ten semantic closures, and what is deliberately not among them

Each is asserted at a production sink and replayed at both endpoints.

1. **No reentrant pending path publication.** The path map receives only a
   value that has been finalized, so no synchronous reentrant lookup retrieves
   unresolved or partial work at any instant.
2. **Finalized normalized immutable cache values only.** What is shared by path
   is a frozen, null-prototype, scalar-only record over a fixed key set — never
   a promise, never a raw parsed file.
3. **Mutable-prototype payload closure.** Fields are taken by own descriptor at
   settlement, so an inherited `text` cannot make an unreadable payload
   readable and no own accessor is ever invoked.
4. **Exact completion-envelope owner.** The completion carries the exact
   `rowTransport` owner and is sealed so a same-shaped literal is not one.
5. **Cross-owner arbitrary content rejected.** An actual B row presented with
   A's completion, or with content no request produced, applies nothing.
6. **Body application tied to the completion owner.** Application requires the
   completion's owner to be the transport held for that row and that owner's
   projection to be the projection that made it.
7. **Post-write journal ordering.** The body record follows the confirmed DOM
   write rather than preceding it.
8. **Write-failure no-false-applied record.** An unconfirmed write appends no
   entry, so the journal cannot claim a body that never reached the page.
9. **The provenance-specific committed `===` assertion** the review found
   missing from an equality matrix that claimed the whole roster.
10. **The observation-accounting semantic correction.** The `getPrototypeOf`
    observation caused by key enumeration is counted and stated, and the
    conflicting `has` versus own-property-test terminology is corrected.

**Three categories are kept apart from those ten, because the V15 review found
them conflated.** *Regressions*: everything the review passed and this lane
preserved — the row-transport owner model, the A-held/B-independent vector and
its terminal fields, the wrapper closure, the per-name substitute record, the
failure isolation and owner-local retry, the accessor cases, the throwing
mutations, the downstream rerender, and the inherited V14 closures. All are
replayed and all still pass, and not one of them is counted here. *Pins*: a
byte-identity hash pin fails at the parent because bytes differ, which is
arithmetic and not meaning. *Audits*: a consumer-roster audit proves a roster is
complete, not that a defect is closed. Counting any of the three among the
closures would inflate the claim, and V15 was told so.

## 5. The finalized value, measured rather than asserted

These are properties of the shipped model, measured directly against it:

- the finalized value has a **null prototype**;
- it is **frozen**;
- its key set is **exactly** `M.TEXT_SCHEMA`;
- **every one of its values is a string or a boolean**, so there is no nested
  structure in it to mutate;
- an **inherited** `text`, `basis` or `acknowledgement` is refused, and the
  payload reads unreadable rather than borrowing the prototype's words;
- an **own accessor** for `text` is declined with **zero getter invocations** —
  not "the value was not used", but "the function was never called";
- a **nested mutable object** supplied for `basis` is refused to `''`, and
  mutating that object afterwards changes nothing in the finalized record;
- **forged, scalar, `null` and null-prototype owners** all yield `null` from
  `M.textCompleted` and `M.textFailed`;
- `M.bodyAsked` **fails closed** on a scalar row and on an unsealed envelope of
  the right shape;
- `M.failureSaid` is **total** against a `message` accessor that throws: it
  returns a sentence rather than propagating out of the sink.

## 6. Observation accounting, exactly, and corrected

Over one sources record, across the whole projection, counted in six kinds
named for the operations they are — `value_gets`, `getter_invocations`,
`has_operator`, `own_descriptor_reads`, `enumerations`,
`prototype_observations`:

- **zero** value reads that would run an own accessor, and **zero** accessor
  invocations;
- **zero** `in` tests;
- **three** `getOwnPropertyDescriptor` observations per source key;
- **two** per shared field the record states, and **one** per field it does
  not;
- **one** key enumeration;
- **one** `getPrototypeOf` observation, caused by that enumeration;
- **nothing further on a second render.**

`Object.hasOwn` lands in the descriptor count because it *is*
`[[GetOwnProperty]]`. It is an own-property TEST performed through the
descriptor trap, and V15's prose called that bucket `has` while the `in`
operator's `[[HasProperty]]` had no bucket of its own; the two words were used
interchangeably and that is corrected. V15 also measured a key list that
required a prototype read and reported no prototype bucket at all, while
describing its four kinds as everything that happens. That omission is the
tenth closure above.

So the claim this lane is entitled to make is narrower than "the record is
observed once", and it is stated in that narrower form: **no hostile inherited
or accessor value becomes semantic authority — no value read runs, no accessor
is invoked, and every semantic member is taken from the record's own descriptor
table.** It is not claimed that six kinds are the only kinds of observation that
could ever occur.

## 7. What the shape costs

**A row that resolves no address now mints a transport owner.**
`M.rowTransport(row)` is consulted unconditionally in `fragmentText`, where V15
consulted it only when an address resolved, so a row whose record names no text
file produces an owner with an empty `path` and one `transport` witness where
V15 produced neither. That is deliberate: "this fragment carries no text file"
is a body application like any other, and it must be owned by a completion the
model sealed rather than applied on a bare row-membership test. The request
journal carries one more transport row for such rows than V15's did.

**The confirmation is over the body, not over everything beside it.** What is
read back is `text.textContent`. The acknowledgement block and the `Extent —`
and `Date —` apparatus paragraphs are not confirmed, so a journal entry means
the body reached the page and not that every node beside it did. The claim that
IS closed is the negative one: a body that did not reach the page leaves no
entry saying it did.

**Ownership is an object the page passes.** Nothing the DATA carries can mint
an envelope or apply a body, which is the point, and it is also a constraint on
anything that later wants to drive this transport from outside. The claim is
exactly that strong and no stronger: in-realm code holding a recorder installed
through the exported `chapterWitness` receives the page's actual row objects,
and from a real row both `M.rowTransport` and `M.textPayload` will mint valid
halves in five lines. This is not a security boundary against code already
running in the realm — such code can write the DOM directly and needs no
envelope — and the unqualified claim that the halves cannot be supplied from
outside is refutable by a five-line probe and is not made here.

## 8. What it costs the page, and the prose that moved out of it

`src/web/browser/catena/catena.js` is **larger** than the parent left it:
12,958 → 12,965 gzipped whole against a 13,000 ceiling, and 7,724 → 7,835
stripped against 8,800. `src/web/browser/catena/catena.css` is 7,629 against
8,000 whole and 2,676 against 2,700 stripped, byte-identical to the parent, and
`src/web/browser/catena/index.html` is byte-identical. **No ceiling was
raised.**

The ceiling had 42 gzipped bytes of headroom at the parent, and this correction
is not payable out of 42. So the three sentences the page may say about a body,
the presentation decision itself — `M.bodySaying` and `M.failureSaid` — and the
page's paragraph on its one point-of-use acknowledgement channel were relocated
into the uncapped model, and the page kept pointers. That is the same arithmetic
this repository has recorded at every version since V4. What is different this
time is the outcome: the relocation paid for most of the change and not all of
it, and the page ends **seven gzipped bytes above** where V15 left it, with
thirty-five bytes under an unraised ceiling. Every
version from V4 to V15 could report the page smaller than its predecessor. This
one cannot, and says so rather than trimming load-bearing prose to buy the
sentence.

The model, which carries no ceiling, went 41,077 → 44,247 whole and
9,536 → 10,344 stripped, SHA-256
`64a75834abd8f9efa25ae52c76b904a3437ab96a9508ba82309211215d44c3a3`. Disclosed,
not presented as unchanged load.

**Two fixes were identified, costed and deliberately not made**, because each
costs more gzipped bytes than the unraised ceiling has. The cache-hit branch
tests the finished value for truthiness rather than asking
`fragmentTexts.has(path)`; a sealed value is always a non-null object, so this
is exactly correct on today's schema and is a latent trap only if the schema
ever admits a falsy sealed value — cost to fix **37 gzipped bytes against 35 of
headroom**. And the body write assigns the class before the words; reordering so
the words land first would leave the page wholly untouched by a write that
throws before the body lands, but no such throw is reachable (`T.el`, `licence`,
`insertBefore`, `appendChild` and concatenation over `sound()`-typed strings do
not throw on real data) and the reorder costs **about 60 gzipped bytes**,
because it breaks a repeated pattern gzip was compressing. Both are recorded as
disclosed, costed and deferred rather than paid for by raising a ceiling or
trimming load-bearing prose.

## 9. The evidence defects, and what actually caused them

`PROVENANCE.md` enumerates them with their root causes; three are worth stating
here because they bear on how this file's own figures should be read.

**The example figure in V15's prose was not supported by V15's own shipped
transcripts, and the review was right to say so.** The prose claimed a bare
thirty, naming no measure and no build state; the two transcripts that settle it
are members of the PREDECESSOR
package and of no part of this one —
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15/logs/attempt-01/make-check-parent.log`
and
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15/logs/attempt-02/make-check-head.log`,
committed on `evidence/catena-e1-corrections-v15-handoff` and named here by the
repository path they occupy there — and each reports twenty-eight `DIFF` rows
over twenty-seven distinct commands, and each summarises `28 diverged … 2
volatile line(s) declared`, which is the tool's own summary field quoted
verbatim and not a phrasing this package adopts. That observation stands
unaltered here. **Those V15 figures are HISTORICAL, inferred from shipped V15
evidence taken on a warm tree, and they are never presented as a V16 replay:**
in the locked measures they are `divergent_rows` twenty-eight,
`distinct_divergent_identities` twenty-seven, `volatile_rows` two and
`total_differing_rows` thirty.

**The review's account of WHY does not survive measurement, and this lane says
so rather than inheriting it.** The reading offered set twenty-eight of what it
called examples — a word that names neither `divergent_rows` nor
`distinct_divergent_identities`, and the reason this lane does not reuse it —
beside two separately declared volatile lines, against a durable claim of
thirty, which presents thirty as decomposing into those two figures. The
review's sentence is quoted verbatim in `PROVENANCE.md` §16, once, so that what
is being refused is on the record in its own words rather than paraphrased into
agreement. It cannot decompose that way. In `scripts/replay_examples.py` the
divergence figure is a run outcome computed from the run's own result lists. The volatile
figure is `sum(len(lines) for lines in VOLATILE.values())` over a static
module-level table: it counts DECLARED LINES over the source tree and is
unaffected by which tools ran.
Both captures that table names are masked BEFORE comparison, and they appear in
every transcript as `ok` and `absent`, never as `DIFF` rows — so they were never
in the set they are supposed to be taken out of. The equality is an arithmetic
coincidence and it closed the question on the wrong cause.

**The cause is neither arithmetic nor prose but BUILD STATE, and the difference
is a MEASUREMENT-SURFACE difference rather than a V16 parent/head behaviour
delta.** Measured independently at the exact parent in a clean checkout not
under `/tmp`, a cold `build/` reports thirty divergent rows over twenty-eight
distinct divergent identities and an immediately repeated warm run reports
twenty-eight divergent rows over twenty-seven distinct divergent identities; the
entire delta is two captures of `tools/mass-ordinary check --out
build/example-ordinary`, whose comparison directory a later capture in the same
target writes and nothing cleans. In V15's shipped transcripts both of those
captures read `ok`, the warm signature, so V15 quoted a cold figure while
shipping a warm log and the record never said which tree it was measuring.
**The two authoritative V16 cold cohorts — the parent under ordinal 15 and the
head under ordinal 16 — agree exactly on all four measures**, so nothing in this
comparison is a behaviour change between the endpoints this package ships; what
moved is the surface the measurement was taken on. Row count, distinct identity
count and volatile-line count are three quantities of three kinds and this file
never blurs them into one.

**And there is ONE additional identity, not two — it contributes two ROWS.**
Set-differencing the divergent command identities in both directions: exactly
one identity is in the V16 cold set and not in the V15 warm set, and nothing at
all is in the V15 set and not in the V16 one, so the cold set is a strict
superset. That identity is `tools/mass-ordinary check --out
build/example-ordinary`, captured twice in `tools/mass-ordinary`, so distinct
diverging commands go twenty-seven to twenty-eight while rows go twenty-eight to
thirty. Any phrasing about "the two additional identities" is the row-versus-name
conflation this package is correcting elsewhere, and it is not used. The
mechanical derivation, including the controlled experiment that shows the tree
is not the variable and the live reproduction of the transition, is
`logs/divergence-reconciliation.json`; `PROVENANCE.md` §16 states it in full.
The set difference is machine-derived and lives in that member under
`v16_minus_v15_distinct_identities` and `v15_minus_v16_distinct_identities`, the
second of which is empty; this file cites those fields rather than retyping
their contents, because a figure retyped into prose is a figure that can drift
from its derivation.

**Where the authority for these figures sits, and where it does not.** The
authoritative V16 basis is the pair of cold cohorts under ordinals 15 and 16,
recorded in that member under `authoritative_basis`; their four measures are
`figures.v16_parent` and `figures.v16_head` and `v16_endpoints_equal` is true.
The V15 figures above are historical reconciliation context and no V16
validation figure derives from them. **The superseded cohorts under ordinals 04
and 07 are a CONTROL and nothing else:** they reproduced the same cold counts,
which is a small independent check that the figure is a property of the
measurement rather than of one run, and that is the whole of their standing.
They are not an authoritative V16 measurement source, no figure in this package
derives from either of them, and no sentence in this package presents them as a
source of one.

**What this package takes from that is not a number but a rule: a count is
meaningless without the state it was taken in, and this package states both.**
It reports divergent ROWS and distinct COMMAND STRINGS separately, keeps the
volatile figure apart as the static declaration it is and never sums it with
either, records `build-state=COLD|WARM` at preflight, and pins **no constant at
all** — a check pinning thirty, or twenty-eight, would be wrong in one state or
the other. It refuses the unsound SHAPE, refuses a prose figure this package's
own transcript does not support, and refuses a summary line that disagrees with
its own `DIFF` rows.

**The compare gate had one sound half and one degenerate half, and both are
recorded.** `walk()` keyed assertions on the NAME alone, so thousands of
assertion ROWS collapsed onto a handful of diagnostic NAMES under last-write-wins
and the rest were discarded before the per-row diagnostics ran — while the
output called them assertion objects. The VERDICT line was nonetheless sound:
the final comparison is over the whole report object, every assertion included,
minus the named volatile fields. The whole-report equality proof stands; only
the localising diagnostics were degenerate, and saying only the first half would
have been as untrue as saying only the second.

That gate's own figures are therefore reported as three quantities and never as
one: `total_gate_rows` **2,290**, `normalized_reports_equal` **yes**, and
`distinct_diagnostic_names_or_categories` **17**. The seventeen are a diagnostic
vocabulary; they do not enumerate the 2,290-row identity universe, and nothing
in this package should be read as saying that a small diagnostic category count
is that universe.

**The tool accounting sealed two unlabelled count sets in one package**, taken
at different phases, neither labelled by phase, with nothing reconciling them —
and beneath both, several supposed invocations were synthesized placeholders
carrying a fabricated time, phase and log, three fields a tool that never ran
cannot have, while the two scripts that drove the build were marked not
executed because neither recorder can see itself. What ships here is one
phase-labelled schema whose execution state is derived from what the run
recorded.

## 10. What proves it

Every claim above is asserted at a production sink in
`tools/tests/test_catena_wave_1.py` and replayed at both endpoints. The focused
Catena suite is **660/660** at the candidate and **615/615** at the
exact V15 parent.

**48 methods are new and 3 were removed or renamed.** At the exact parent,
**39 distinct METHODS fail over 288 failure ROWS, with zero errors** — both
counts given, apart, because one method alone
(`test_every_body_this_page_applied_is_a_finished_scalar_record`) emits 192
`subTest` rows as it sweeps every applied body in the plan, and reporting one
figure as the other is the conflation this package is correcting elsewhere.

Those 39 are counted by KIND, not summed into a single discrimination claim:

- **30 fail for a SEMANTIC reason** — the defect is present at the parent.
  Representative parent messages: `'promise' != 'absent'`; `a pending answer is
  reachable by path`; `the body applied an object the path never held`; `an
  actual row still authorizes an arbitrary literal`; `a body nobody can read
  was journalled as applied`; `assignThrew did not throw`; and the parent
  rendering `FORGED INHERITED BODY`, `FORGED LATE BODY` and `FORGED ACCESSOR
  BODY` to the reader.
- **6 fail because THE MECHANISM IS ABSENT**, and are counted apart and named
  as absence-readings rather than advertised as discriminators. These are the
  pollution and schema probes, where V15 has no `sealText`, `NO_TEXT`,
  `TEXT_SCHEMA` or `bodySaying` at all; they now fail with an explicit *"this
  endpoint seals no such value at all — the mechanism is absent, which is a
  different reading from a value that carries the wrong members"* rather than a
  `TypeError`. The V15 review criticised the previous lane for advertising a
  discriminator that failed the parent only because a witness was missing, and
  folding these six into the semantic thirty would repeat that exactly.
- **2 are source-text closures** —
  `V14UnfetchedProjectionTest.test_the_page_reads_no_raw_chapter_member_after_projection`,
  extended, and `…test_the_page_states_no_body_sentence_the_model_states`, new.
- **1 is a hash PIN** — `FrozenContractTest.test_the_model_is_byte_identical`.
  A pin, not a closure, counted apart as V15's record correctly did.

The 3 removed or renamed methods are named so a reviewer can find them:
`V15TransportOwnershipTest.test_a_row_no_projection_made_owns_no_transport_and_writes_nothing`,
rebuilt as the transport half plus four content negatives — **this is the exact
assertion the review named, the one that asserted `M.bodyAsked(row,
{text:'x'})` true** — and
`V15ObservationAccountingTest.test_no_value_read_of_a_source_record_happens_at_all`
and `…test_the_descriptor_count_is_three_per_key_and_two_per_stated_field`,
replaced by three methods under the six-field vocabulary.

**11 of the new methods pass at both endpoints.** They are coverage and
controls, and they are recorded as coverage and controls, not as closures. Pins
and audits are recorded as pins and audits.

`checks.txt` carries every command with its working directory, its argument
vector, its exit and its log; `claims.json` and `DERIVED-CLAIMS.md` carry every
figure; the per-attempt transcript directories under `logs/` carry the runs. The
parent replay is the load-bearing artefact, and what the parent renders — a
prototype's words standing as a fragment's own text, and a body applied under a
row that never asked for it — is recorded there rather than described here.

## 10a. Which cohorts these figures come from, and which contribute nothing

Every figure in this file is a measurement, and a measurement belongs to the
attempt that took it. **Every head-side figure above derives from the cold
shipping-head cohort, attempt `head-20260827T194839Z-166gh2tz` of ordinal 16,
and every parent-side figure from the cold parent cohort, attempt
`parent-20260827T193049Z-15pnpphq` of ordinal 15.** Those are the two battery
attempts whose evidence disposition is `authoritative`; the derivation is
`logs/attempt-history.json` and the history it renders is `PROVENANCE.md` §13.

**That history is complete across two ledger files rather than inside one, and
this file says so at the point where it sends a reader to it.** This lane
retired its first attempt ledger after ordinal 03 and opened a successor in its
place. What was replaced was the file and not its contents: no row in either was
rewritten or deleted, each ledger is append-only within itself, and the retired
file is retained whole and bound by digest. The successor's opening `lane` row
carries the retired file's digest, byte count, row count, the ordinals it spent,
the attempts it held and the reason it stopped; `PROVENANCE.md` §15 records both
files with that reason and §6 states the allocation rule that makes the move
safe; and `logs/attempt-history.json` is the derivation taken across the pair.
**No ordinal was reissued across the move** — `reused_ordinal_count` is zero over
both files rather than over the shipped one alone, which is the correction to the
predecessor lane's defect of letting ordinal 01 name three different attempts in
one lane.

**They are not the cohorts that first held that disposition, and this section
says so rather than letting the shipping pair stand for the whole story.** The
cold cohorts of ordinals 04 and 07 measured the same two endpoints, completed,
and were recorded `authoritative` as soon as their batteries ended — before any
package had been sealed from them. P8, which compares each tool's executed
digest against the copy the archive ships, then refused: those cohorts had
executed `logs/battery.sh` at
`04ca35cb5969aea92d983c9793b5dc2d0d427c8a0ca356fa91db95bb8cc58c9c` while this
package ships that driver at
`cca4d2840116e2e101c68d9bdf8db1305f545b838015a837514f4464b73b947c`. What ran
was not what shipped, on a difference of header comment prose alone, and the
remedy was to measure again rather than to argue that the changed bytes could
not matter. Both endpoints were measured again against frozen drivers; every
tool the shipping batteries executed matches its shipped copy byte for byte;
and the evidence disposition was recorded only after that identity had been
established. Ordinals 04 and 07 are `superseded`, their `authoritative` rows
stand where they were written, and **no figure above derives from either.**
The lesson `PROVENANCE.md` §3 draws from it is that an evidence disposition of
`authoritative` belongs after a seal has proved a cohort's tools are the
shipped ones, not at the moment a battery ends.

**Two further cohorts of this lane contribute nothing to anything above, and
are named here rather than left out.** The battery of ordinal 05 completed and
its evidence is `set-aside`, because it measured head `251900b14`, which
`cc1f2fb86` superseded; no claim, count, size or digest in this file derives
from it. The battery of ordinal 06 is terminally `abandoned` — it was stopped
from outside itself after three green steps, no step failed, and no guard
refused — and **it contributes no validation result to any authoritative claim
in this package**; it is retained for history and audit only, outside the
archive. No cohort was deleted to make the record look shorter, and none of
them may be read as supporting a figure.

## 11. What is not closed here

`LIMITATIONS.md` states every boundary and `UNRESOLVED-BLOCKERS.md` states every
finding left open with its owner. Four that bear directly on this claim: the
post-write confirmation covers the body text alone; the reentrant and mutation
vectors are reachable only through the replay harness and no browser engine
witnesses them; the page's remaining whole-file headroom is now too small for
the next correction of any size; and the uncapped model grew again while the
question of a governing ceiling stayed with its owner.
