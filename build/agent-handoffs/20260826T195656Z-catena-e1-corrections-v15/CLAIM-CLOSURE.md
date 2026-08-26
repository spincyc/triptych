# The owner that asked, and what its answer may be shared with

## 1. The finding, and what it actually was

The V14 independent review answered **CHANGES REQUIRED**, recorded at
`0d11766ec232b2b4e46a7d1b0ada56ef22370004` on
`review/catena-wave-1-e1-corrections-v14-independent`. Unlike the V13 review V14
had to answer, it is published, so this lane's account of a disposition can be
checked against the review itself.

The finding it required is one defect and it is worth stating without
softening. V14 closed ownership at address *resolution*: the page hands the
model a row, the model resolves the fragment's text address through that row's
own identity, and a row no projection made resolves nothing. That much held.
What the review found is that ownership did not survive resolution. The
resolved path was handed on as a bare string to a module-scope `Map` keyed on
the path alone, and that map held the **unresolved promise**. A second
projected row carrying the same address therefore made no request of its own.
It joined the first row's pending promise and was handed the answer that
request was made for.

So the guarantee V14 argued for — that a request is owned by the row that
asked for it — was true of the question and false of the answer.

## 2. What the parent actually does

Reproduced at the exact reviewed parent, not argued from the source: with
owner A's request held, owner B's page renders `Loading…` — B is waiting on a
request B never made. When A is released, B renders **`PLANTED BODY A`**: the
document A asked for, under B's row, on B's route, in B's projection. No
refusal, no marker, no seam a reader could see. The page states another
owner's document as B's own text.

One more thing about the parent is load-bearing, and it is the reason this is
a semantic defect and not a missing test. The V14 method that was green over
this path **required the leak to pass**: it asserted the shared-promise
behaviour as correct. A test that passes only because the defect is present is
not a control. It is corrected here, and corrected it fails at the parent.

## 3. The contract

Five clauses, all of them in `src/web/browser/catena/catena.js` and
`src/web/browser/catena/catena-model.js` and nowhere else.

**A path may key only a settled answer.** The path map holds no pending work
at any instant a caller could reach it: the promise is entered into the map
from inside that promise's own settle handler, so there is no window in which
an unresolved value is reachable by path. The map's key was never the problem;
what it held was.

**Work in flight is held against the owner, not against the address.**
`M.rowTransport(row)` returns one frozen owner object per projected row,
carrying the row, the projection that made it, and the address that row asks.
Two rows at the same address are two owners with two pieces of work. The
copy-refusal rule V14 introduced stands unchanged beneath it: a row no
projection made gets no owner, so it resolves no address and starts no
transport.

**Body application is asked, at the body application.**
`M.bodyAsked(row, content)` is asked at the sink where the body is written,
not near it, and records the projection, the row and the value written. A row
no projection made applies nothing. This is the same discipline as the
identity recorder the previous lane introduced: the record is taken where the
effect happens, so what is proved is what the consumer received rather than
what a second call to the model would have returned.

**A reported transport failure is owned exactly as a fulfilled body is.** A
failure is an answer. It travels the same owner and is recorded through the
same sink, so one owner's failure cannot become another owner's rendered
state.

**The substitute record for a spine the page cannot read is made once per
name and reused.** It is created once, per name, and shared. It is a settled
immutable value with no owner-specific content, which is the class of thing
sharing is safe for; that class is stated here on purpose, because the whole
finding is about sharing something outside it.

And one ordering rule that falls out of the first clause and had to be made
explicit: **the first settled answer at a path is not displaced by a request
released later.** A slow request that resolves after a fast one does not
overwrite the answer already standing.

## 4. What the closure inventory covers

Ten semantic items, each asserted at a production sink and replayed at both
endpoints:

1. unresolved same-path work is not shared across owners;
2. B settles independently while A is held;
3. A arriving late cannot change what B has;
4. actual body-application row ownership — the row the body is written under;
5. body-application projection identity;
6. wrapper projection identity;
7. same-path multi-projection completion isolation;
8. safe sharing of a fulfilled immutable value;
9. cross-owner failure isolation;
10. downstream rerender after an attempted mutation.

Items 8 and 10 are the ones that keep the rule honest. Item 8 says what
sharing is still permitted, so the closure is a rule and not a blanket ban.
Item 10 says the isolation survives a rerender rather than holding only on the
first paint.

## 5. Two proof gaps closed — and they were not production defects

Two of this lane's vectors close gaps in the *record*, not defects in the
product, and the record has to say so.

**The nested EDITION accessor case.** The previous lane promised it and did
not ask it. It is asked directly here, and the parent already answers it
correctly: one coherent outcome across edition, printing, provenance line,
rights, voices and readable state. What changed is that the claim is now
proved instead of promised.

**Observation accounting.** The previous record asserted a shape of
observation it had not counted. It is counted here, and the count is stated in
§6 exactly, including the part that is larger than a reader might expect.

Neither of these is a closure of a defect and neither is presented as one.

## 6. Observation accounting, exactly

Over one sources record, across the whole projection:

- **zero** value reads that would run an own accessor;
- **zero** `in` tests;
- **three** `getOwnPropertyDescriptor` observations per source key;
- **two** per shared field the record states, and **one** per field it does
  not;
- **one** key enumeration;
- **nothing further on a second render.**

`Object.hasOwn` is counted under descriptors, because it *is*
`[[GetOwnProperty]]`. That is exactly why the per-key figure is three and not
two: an accounting that called `hasOwn` "not an observation" would report the
smaller, nicer number and would be wrong.

So the claim this lane is entitled to make is narrower than "the record is
observed once", and it is stated in that narrower form: **no consumer runs a
hostile value accessor, and no consumer reaches past the projection to observe
the record again.** The record is observed several times, by descriptor, and
the number is above.

## 7. What the shape costs

**Two owners at one address do two pieces of work.** Deduplicating concurrent
in-flight requests by path is exactly the mechanism that leaked, and it is
gone. Where the previous lane made one request for two rows at the same
address, this one makes two. The saving that costs is real and it is smaller
than the defect it removes; the settled map still prevents a *second*
retrieval once an answer exists.

**First settled wins.** A later-released request does not replace an answer
already standing at that path. That is deliberate, and it means the page
prefers a stable answer over the freshest one within a render.

**The owner is an object, not a string.** Ownership can no longer be
reconstructed by anyone holding the path — which is the point, and also means
a caller outside the projection cannot ask about work at an address at all.

## 8. What it costs the page, and the prose that moved out of it

`src/web/browser/catena/catena.js` is **smaller** than the parent left it at
12,972 → 12,958 gzipped whole against a 13,000 ceiling, and larger stripped at
7,546 → 7,724 against 8,800. `src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html` are byte-identical. No ceiling was raised.

That whole-file figure was bought, and the price is disclosed rather than
absorbed. The ceiling had 28 gzipped bytes of headroom at the parent, so three
paragraphs of the page's own prose were relocated into the uncapped model:
why a 200 that is not a spine is not an empty chapter; why neither the
paragraph layer nor its index may decide the page; and what the absence
disclosure may say. The page keeps a one-line pointer to each. A reader of
`src/web/browser/catena/catena.js` now follows a pointer for three explanations that used to stand in
front of them, and `LIMITATIONS.md` records that as a cost of this lane, not
as a tidy-up.

The model, which carries no ceiling, went 39,724 → 41,077 whole and
9,396 → 9,536 stripped. Disclosed, not presented as unchanged load.

## 9. The evidence defects, and what actually caused them

Of the eight defects the review named in the evidence itself, and which
`PROVENANCE.md` enumerates, six are defects in the pipeline's own tools and are
fixed there. The two that are not — the P8 table's ordering against later
executions, and `claims.json` under-deriving figures the prose repeats — are
recorded in `PROVENANCE.md` rather than restated here.

The six are the reason this lane changed pipeline tools as well as production
ones:

- two browser-gate commands recorded `ELIDED`;
- the load-bearing parent-replay command recorded `PROSE`;
- `logs/compare-gate.py` labelled unexecuted despite its own assembly transcript;
- a combined `16`-and-`11` label that mixed invocation rows with unique-tool rows;
- a history that claimed `complete` and `append-only` while omitting a
  set-aside cohort and the P10 rows, and while disclosing a two-row
  replacement;
- a mechanical `COMPLETE` verdict that tested none of the above.

Two root causes were found rather than guessed at. The `ELIDED` verdicts came
from the capitalised English word `JSON` appearing inside a quoted `echo` note
the battery composes — not from any filename, and not from the `$WORKSPACE`
and `$EVIDENCE` symbols, which the classifier exempts. The `PROSE` verdict
came from `cp` being absent from the classifier's list of command heads. Both
are classifier defects, and both had the same effect on a reviewer: the
command that carries the load was the command they could not read.

## 10. What proves it

Every claim above is asserted at a production sink in
`tools/tests/test_catena_wave_1.py` and replayed at both endpoints. The
focused Catena suite is 615 green at the candidate and 596 at the parent.

Nineteen methods are new. **Fourteen methods fail at the exact parent** —
eleven of the new ones, plus the corrected late-answer oracle, the
consumer-roster audit, and the model byte-identity hash pin. The remaining
eight new methods pass at both endpoints; they are coverage and controls, and
they are recorded as coverage and controls, not as closures.

One of those fourteen is classified here rather than counted: **the model
byte-identity hash pin is a pin, not a semantic closure.** It fails at the
parent because the model's bytes differ, which is arithmetic and not meaning.
Counting it among the semantic closures would inflate the claim by exactly one
and it is excluded from them for that reason.

`checks.txt` carries every command with its exit and its log; `claims.json`
and `DERIVED-CLAIMS.md` carry every figure; the per-attempt transcript
directories under `logs/` carry the runs. The parent replay is the
load-bearing artefact, and the rendered sentences on both sides of it —
`Loading…` and `PLANTED BODY A` under an owner that asked for neither — are
recorded there rather than described here.

## 11. What is not closed here

`LIMITATIONS.md` states every boundary and `UNRESOLVED-BLOCKERS.md` states
every finding left open with its owner. Three that bear directly on this
claim: eight new methods pass at both endpoints and pin existing behaviour;
the edition-accessor and observation-accounting vectors close gaps in the
proof and not defects in the product; and the three relocated paragraphs make
`src/web/browser/catena/catena.js` less self-explanatory than the parent left it in exchange for the
bytes this lane needed.
