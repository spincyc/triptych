# The request-critical snapshot, and what it closes

This is the technical argument of the V12 lane. It states the contract, why
each part of it is shaped as it is, and what the shape costs. Every figure
it cites is derived in `claims.json` and rendered in `DERIVED-CLAIMS.md`; no
number is typed here.

## 1. Three findings, one defect

The V11 independent review found three ways into the production request sink
that no record's own bytes had stated. They read as three, and they are one:

**the raw record was observed more than once, and the observations were
allowed to disagree.**

- **The spine's `text_prefix`.** V11 read the value with `ownData` — a
  descriptor read, so nothing inherited crossed — and then asked the raw
  record a *second* time, with `Object.hasOwn`, for whether the property was
  present at all. For a record whose prefix lived on its prototype, both
  answers were the same answer a record that never mentioned a prefix gives:
  value `undefined`, presence `false`. The claim that came out was
  bit-identical to genuine absence. Genuine absence is the one state that
  reopens the carried fallback, so a polluted spine reached `fragmentText`,
  the page's cache and `T.loadJSON` with a live address.

  Invisible is not the same as refused. `ownData` closed every way a
  prototype could *open* something and left open the way a prototype could
  make a record look like it had said nothing — and saying nothing is a
  meaningful thing to say here.

- **`text_refused`.** `ownContract` asked `Object.prototype` about `stated`,
  `said` and `trail`, and about nothing else. With
  `Object.prototype.text_refused = true`, an otherwise own-valid claim
  stayed clean and composed its address. The contamination was not read
  wrongly; it was not read at all.

- **The carried `text_path`.** The fallback arm called
  `ownData(own, 'text_path')` twice — once inside the own-stem test, once
  for the value it returned. Two calls are two observations. A
  `getOwnPropertyDescriptor` trap that answers one address first and another
  second passed the stem test with the first and handed `fetch` the second,
  and the address that reached the network had passed no test at all. No
  amount of validation repairs that, because the thing validated was never
  the thing used.

## 2. The contract

**The request-critical state of one record is taken once and then held.**

`requestSnapshot(record, names)` performs, for one record:

- exactly **one** `Object.getPrototypeOf`;
- exactly **one** `Object.getOwnPropertyDescriptor` per requested name;

and returns a record with a **null prototype**, carrying two frozen
own-data members — `stated`, which says whether each name was present, and
`value`, which carries what each name's data descriptor held — beside one
boolean, `sound`.

Nothing else in the model asks a raw record a request-critical question. The
fallback decision, the composed address, the carried address, the refusal,
the ownership journal and the row the renderer consumes are all answered
from the snapshot.

`REQUEST_MEMBERS` names the five fields that decide whether a request
happens, where it goes, and who owns the answer:

    text_prefix    text_path    text_refused    stated    trail

`sound` is false when the record has a prototype of its own, when anything
above it names one of those five, or when a requested name is an own
**accessor**.

### What the two halves of the contract say

- **An accessor is declined without being called.** The invocation count is
  **zero**, not one. V11 proved ordinary accessors need never be invoked,
  and that is a stronger property than reading one once and trusting the
  answer; keeping it was not optional. What V12 adds is refusing to read the
  *absence* of a `value` on an accessor's descriptor as the absence of a
  statement — which is the same mistake, one field over.
- **A data descriptor is read exactly once per projection.** The value
  validated is, by construction, the value projected and requested. There is
  no second read for a drifting descriptor to answer differently.

### Where contamination lands

Not in a fourth state. A contaminated record resolves to the state the route
already has for input it cannot establish anything from: **malformed /
unestablished**, saying only

> No text reference is established for this fragment, so no text is shown.

Concretely, a contaminated spine yields the claim `{stated: true, said:
false, trail: ''}` — something was said here, this page cannot say a textual
value was supplied, and no usable trail survives. That is neither the one
absence shape nor a valid statement, so it composes nothing, opens no
carried door, and takes the conservative sentence. No new vocabulary was
added to the claim contract, and `fragmentRow` remains callable by its
existing three-member exported signature.

## 3. What the shape costs

Stated plainly, because it is the question `REVIEW_REQUEST.md` blocker 2
asks:

**A polluted `Object.prototype` closes every row on the page, not one.**

A prototype is not a property of one record. A page that renders one row
from a polluted realm and refuses another is a page deciding, per row, which
half of a contradiction to believe — which is exactly the adjudication this
gate exists to refuse. The alternative, contaminating only the record whose
polluted read was actually consumed, was considered and rejected on that
ground. The cost is real and it is not hidden: in a polluted realm this page
shows a chapter of unestablished rows.

The three ordinary dispositions are unaffected, and are asserted beside every
closure as positive controls:

| the record's own bytes | what happens |
| --- | --- |
| genuine absence, valid same-stem carried path | the carried path is requested, its body renders |
| own present-valid prefix | the composed address is requested, its body renders |
| own present-invalid prefix | zero requests, refused state, the supplied-and-refused sentence |

## 4. Why `src/web/browser/catena/catena.js` is untouched

The snapshot boundary did not need to cross into rendering. The row the page
consumes is already a trusted projection whose every member is an own data
property — V11 proved that and the review passed it — so the page's three
reads of `text_refused`, `text_note` and `text_path` inside its toggle
handler are reads of derived, trusted state, not of a raw record. The
refusal is still consumed before the request sink, and that ordering is
still pinned by a harness hook against a control that really does fetch.

The page also stands at 20 gzipped bytes of its ceiling, and the model has
none. Putting the correction where the ceiling is not is the same choice V10
and V11 made, for the same reason, and it is disclosed rather than presented
as unchanged load.

## 5. What proves it

Two boundaries, and the second is the one that matters.

**At the model.** A matrix drives the review's exact reproductions; ten
inherited and `Object.prototype` combinations, including a getter-backed
refusal marker and each of `stated`, `trail` and `text_path` polluted
independently; and six drifting descriptors — a drifting getter, valid then
wrong namespace, valid then traversal, a counter, throw-on-second-read, and
alternating body identity. It asserts one descriptor ask per projection,
**zero** accessor invocations, and that no second value reaches projection,
request, body or ownership.

**At the production sinks.** Six replay scenarios drive the same three
inputs through `T.loadJSON`, the page's cache and the renderer, with a
deterministic body planted at every address each defect could reach, so a
leak is a served and rendered page rather than an absence nobody forbade.
Each stands beside a non-vacuity control on the same bytes that really does
fetch and render.

Two harness hooks exist because neither a prototype nor a drifting
descriptor is a document, and so neither `files` nor `raw` can express one: a
served record may be given an ancestor, and `Object.prototype` may be
polluted for exactly one scenario and is removed in a `finally` — because a
leak there would silently contaminate every scenario after it, which is
precisely the failure the hook exists to catch.

**Against the uncorrected parent**, the same file fails ten ways across nine
methods. The alternating descriptor **fetches and renders**
structure/catena/text/other.json; the inherited refusal marker fetches both
the composed and the carried address; and the prewarmed contaminated route
serves the planted fallback body to the reader.

**And statically.** With comments removed, the four request-critical property
names are written in exactly three lines of the model — the list that
declares them and the two calls that take a snapshot — and exactly two
functions in the file read a descriptor. A later lane that reaches for one
off a raw record fails at the line it writes.

## 6. What is not closed here

The snapshot covers request-critical state and is deliberately not broadened
into all Catena semantics. Projection is still not the sole semantic source
beyond this boundary; the wide fragment and edition contracts are still
validated field by field. Every blocker the V11 review left open is listed
in `UNRESOLVED-BLOCKERS.md` and none of them is touched.
