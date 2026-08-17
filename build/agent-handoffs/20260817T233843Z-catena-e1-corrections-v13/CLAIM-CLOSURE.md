# One chapter, normalized once, and what that closes

This is the technical argument of the V13 lane. It states what the defect
was, what the contract now is, what the shape costs, why the page is nearly
untouched, what proves it, and what is left open. Every figure it cites is
derived in `claims.json` and rendered in `DERIVED-CLAIMS.md`; no number is
typed here.

## 1. The finding, and what it actually was

The V12 independent review accepted `requestSnapshot` **for one invocation**
— one `Object.getPrototypeOf`, one descriptor per requested name, no accessor
invoked, frozen null-prototype `stated` and `value` beside a frozen verdict —
and refused what the page did with it.

The same raw spine and the same raw fragments were projected three times.
`spineUnreadable` called `chapterFragments` to ask whether a non-empty
fragment list yielded a readable row, and threw the rows away. The tally
called it again to keep a length. `renderChain` called it a third time and
kept the rows that reach request, cache, body and ownership. Three passes
over one raw chapter are three observations of it, and the counts V12
reported — parent 6, V12 3 — were one descriptor read per projection times
three. The review said exactly what that does not establish: the counts do
not prove no source revisit.

**So the defect is not a second read inside one projection. It is a chapter
record that answers one way while readability is being decided and another
way while the render is being built.** A page in that state renders,
requests, caches and attributes from an answer nothing had approved: the
projection that decided a row was readable and the projection that produced
the row are two different projections, and only the first was ever tested.

And the reach was wider than `text_path`. `chapterVoices` walked the raw
`sources` again to build the voice control; `absenceRows` walked it a third
time and re-read `work_id`, `author` and `work` off each raw member;
`refusalNote` re-read the raw `refusals` on every edition and chapter the
reader moved to. The reader's own provenance line and the strongest sentence
this page prints — a recorded refusal — were therefore composed from reads
that no readability decision had ever seen.

## 2. The contract

**One raw chapter is normalized once, and every consumer is handed what that
normalization returned.**

`normalizeChapter(record)` reads each request-critical member of the spine
into a local **exactly once** — `fragments`, `sources`, `refusals`,
`unfetched`, `blocked`, `leads`, and `text_prefix` through the V12 snapshot —
because two reads of one name are two observations of it. From those locals
alone it:

- projects the fragment rows, and freezes each row where it is made, together
  with its `extent` and its `translators`;
- walks `sources` **once**, gathering the voice offers and the edition
  triples the absence disclosure reads, and taking the readability verdict
  from that same walk rather than from a second one;
- normalizes the recorded refusals into a null-prototype map of frozen
  `{kind, chapter, note}` rows keyed by edition;
- returns a **frozen null-prototype** record carrying its own pass number and
  identity, the readability verdict, the prefix claim, the rows, the voices,
  the editions, the refusals, the blocked rows and the leads.

`chapterProjection(file)` holds that record against the raw chapter in a
`WeakMap` and returns the held instance on every later ask. A payload that is
not a record resolves to one shared frozen `NO_CHAPTER` whose pass is zero,
so `null`, a list, a string and a number are not four chapters and do not
become four projections.

`spineUnreadable`, `chapterFragments`, `chapterVoices`, `chapterBlocked`,
`chapterLeads`, `refusalNote` and `absenceRows` all answer from the
projection and reach past it to the raw chapter **nowhere**.

Stated so it need not be inferred:

- **one raw chapter load is one normalization**, however many consumers ask,
  and however many times the reader changes voice, steps an arrow or forces a
  re-render;
- what a consumer receives is **the same instance**, not an equal value;
- every member of that instance is frozen own data on a null prototype, so a
  mutation of the raw chapter after it was read cannot reach a consumer that
  already holds the projection;
- **the request is owned by the projection that produced the row carrying its
  address**, because the page composes no text address of its own — the only
  thing that can name one is a row, and a row comes from exactly one
  projection.

## 3. Identity is made observable, not argued

The review required proof of the same normalized instance and not of equal
values, and a claim about instances cannot be settled by comparing outputs.

`chapterProjection` is exported and returns the held projection.
`chapterPasses()` returns how many raw chapters this page has normalized,
ever — taken before a render and after, its difference is the count of raw
chapters read, not the count of consumers that asked. The replay harness asks
every model entry point that takes a chapter **which projection it resolved
to, before it answers**, so "one identity, everywhere" is a comparison of
recorded lists rather than an assertion.

The roster of consumers is named, and the identity test requires every name
in it. A later lane that adds a chapter consumer and does not route it
through the projection fails on the name that is missing rather than passing
quietly.

## 4. What the shape costs

Stated plainly, because these are the questions `REVIEW_REQUEST.md` puts to
the reviewer.

**The projection is per raw chapter object, not per chapter address.** The
`WeakMap` keys on the record the page received. Two fetches of one chapter
produce two raw records, and therefore two projections and two passes. That
is the honest answer for a page whose cache holds one record per address, and
it is not the answer a reader would give to "how many times was Genesis 1
normalized?" if the cache were bypassed.

**A projected row is frozen where it is made.** That is a change in what any
holder of a row may do with it, not only inside this page: the harness hook
that used to assign onto a row now copies. A frozen row cannot be repaired in
place by a later lane, and that is deliberate — the row is the only channel
across the model/page boundary and it is now made once for a whole render.

**Retention is tied to the page's own cache.** The `WeakMap` holds a
projection exactly as long as something else holds the raw chapter, and the
cache in the page holds every loaded chapter for the life of the page.
Nothing is retained that the page was not already retaining, and nothing is
released early either.

**A polluted `Object.prototype` still closes every row on the page.** That is
the V12 contamination policy, which this review accepted as a design, and it
is unchanged here. The cost is unchanged with it: in a polluted realm this
page shows a chapter of unestablished rows.

## 5. Why `src/web/browser/catena/catena.js` is nearly untouched

Two lines. `M.blockedRows(file && file.blocked)` and `M.leadRows(file &&
file.leads)` became `M.chapterBlocked(file)` and `M.chapterLeads(file)` —
those two reads were the page's last reads of raw chapter state, and they are
now the projection's. Everything else the page consumes was already a
projected row, and the row is now frozen as well as own-data.

The page **gets smaller**: 12,974 of 13,000 gzipped whole and 7,546 of 8,800
stripped, against the parent's 12,980 and 7,554, so its whole-file headroom
improves from 20 to 26 gzipped bytes. The correction lands in
`src/web/browser/catena/catena-model.js`, which has no ceiling at all, and
the model grows from 34,367 to 36,679 gzipped whole and 8,258 to 8,873
stripped. That is disclosed rather than presented as unchanged load, and
whether the model needs a governed ceiling remains the budget owner's
question, re-asked in `REVIEW_REQUEST.md`.

## 6. What proves it

**Six scenarios, each walking a different member, each firing at a different
sink.** The review found `v12-drifting-carried-path` vacuous: it consumed its
valid-then-alternate pair inside the readability projection, which issues no
request, so it passed by never reaching a sink. Each V13 scenario instead
walks **one member of the chapter between projections** and plants something
at an address only a later projection can reach.

| scenario | walked member | at the parent | asks | at this head |
| --- | --- | --- | --- | --- |
| `v13-walking-carried-path` | fragment `text_path` | fetches and renders `…/text/deeper/fallback-owned.json` | 3 | asks once, requests the validated `…/text/fallback-owned.json` |
| `v13-walking-spine-prefix` | spine `text_prefix` | composes and fetches the deeper address | 3 | asks once, composes the first |
| `v13-walking-chapter-members` | `fragments` | renders and fetches a body off members readability never approved | 5 | asks once, no text request |
| `v13-walking-sources` | `sources` | puts a forged rights claim on the reader's own provenance line | 8 | asks once, clean |
| `v13-walking-refusals` | `refusals` | prints a Rule 4 boundary the record never stated | 4 | asks once, none |
| `v13-prewarmed-walking-path` | fragment `text_path`, second chapter | misses a warm cache and fetches a second body | 3 | asks once, the cache hits, the held body is served |

Every one of the six stands beside a `-control` sibling that holds the walked
member at the walked-**to** value, so the planted thing is proved reachable
and renderable by a page entitled to reach it. A scenario that leaks nothing
because nothing could be leaked is not a closure, and the control is what
separates the two.

**Against the uncorrected parent**, this head's test file fails twenty-seven
ways across thirteen methods.

**One committed assertion required the wrong answer and is corrected with its
reason.** `v12-drifting-carried-path` was pinned to make no text request at
all. That was the scenario exhausting its two values inside a projection that
cannot request — the review's own finding — and not a closure; it now
requests the one address the one projection validated. The page-level
descriptor pin moves from three to one for the same reason: V12 pinned "one
ask per projection, three projections per render", and the review named that
number as the defect rather than the proof. No other expected value moved.

**And the package can now show its own ownership.** The journal roster is
derived from the test file itself rather than from a hand-maintained list, so
every declared scenario is journalled and no scenario can be proved in a test
and absent from the evidence. Each row carries its sequence, its scenario,
the route as it stood **when the request was made**, the owning projection,
the path, the kind, the owning step, the outcome, the cache disposition and
the body.

## 7. What is not closed here

The projection is bounded to one chapter's request-critical state and was
deliberately not broadened into all Catena semantics. The wide fragment and
edition contracts are still validated field by field; orphan raw sources
still manufacture offers and rows; the CLI and the browser still implement
the same semantics twice. Projection is not yet the sole semantic source for
this route.

Every blocker the V12 review left open is listed in
`UNRESOLVED-BLOCKERS.md`, and none of them is touched.
