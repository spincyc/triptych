# Catena E1 — V12 stable request-snapshot handoff

This package is the evidence for one bounded correction lane and nothing
else. It records no acceptance, marks no separately owned prerequisite
complete, and does not review its own work.

Every figure in this file is derived by `logs/derive-claims.py` at seal time
and rendered in `DERIVED-CLAIMS.md`; where one appears here it is repeated
from there, and `claims.json` is the machine-readable original. Where a
figure came from a command, `checks.txt` names the command and the log.

## 1. Task and intended outcome

Answer the V11 independent review — **CHANGES REQUIRED** — with exactly its
stated next action and nothing else.

The review accepted the fail-closed prototype-pollution policy as a design
and found V11 applied it to some of the ways in and not to others. It named
three implementation defects and one package defect:

1. an inherited valid spine `text_prefix` was classified as **genuine
   absence**, which is the one state that reopens the carried fallback, so a
   polluted spine reached `fragmentText`, the page's cache and `T.loadJSON`
   with a live address;
2. `Object.prototype.text_refused = true` did **not** close an otherwise
   own-valid claim, because `ownContract` asked about three names and this
   is a fourth, so the claim still composed its request;
3. the carried `text_path` descriptor was **read twice**, so a drifting
   descriptor validated one address and handed `fetch` another;
4. the package could not say which package it was: its ledger called a
   **superseded** attempt authoritative and the attempt that actually
   shipped unresolved, and repeated assemblies reused log names.

The intended outcome: normalize request-critical state exactly once into a
stable trusted snapshot, close all three request defects at the production
sinks with planted evidence, and issue one self-consistent authoritative
package — then stop, for a fresh independent review.

**Not** in scope and not attempted: integration, merge, deployment,
re-signing, cutover, or any of the broader blockers in
`UNRESOLVED-BLOCKERS.md`.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v12`

Not a detached HEAD. Not merged with `origin/main`, which is
`549bf0790503bd873dd8ce6ea0a64cc34f91271d`.

The immutable copy of this package is archived on
`evidence/catena-e1-corrections-v12-handoff`; that branch carries the
package and nothing else.

## 3. Current commit and base commit

| | |
| --- | --- |
| V12 head | `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` |
| parent, the exact candidate that review answered | `0255b84996e1dc24da3ce75ac318c4f774b7957c` |
| review addressed | `22b9bdad5e71920a103e3ec3bcf2f79bba50cebb` on `review/catena-wave-1-e1-corrections-v11-independent` |
| V11 evidence inspected by that review | `0ec8cae646f0e3e60c76635b88e51439c7146796` |
| V11 package that review verified | `20260816T172726Z-catena-e1-corrections-v11`, ZIP SHA-256 `00e93c0f539a7928281912038f135b44666aebb84af4249cb906f54238cae257` |

The parent is an ancestor of the head, the range is **two** commits, and
both facts are derived rather than asserted — see `claims.json` under
`identity` and `commits.txt`.

The V11 review branch is a **sibling** at the reviewed head. It is not
merged in; this lane states its disposition rather than importing its
commits.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was
assembled, and `claims.json` carries `identity.worktree_clean_at_head`
derived from `git status --porcelain` rather than asserted here.

The batteries record tree state **per command**, before and after, so a step
that dirtied the tree would be recorded dirty on its own row rather than
inheriting a preflight's `clean`. See `checks.txt`.

## 5. Focused files changed

Six files. **One is production.**

| file | what it is |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | the only production change |
| `tools/tests/test_catena_wave_1.py` | the regressions and the harness hooks they need |
| `PROJECT-WORK.md` | the durable lane record |
| `guidance/corpus-browser-roadmap.md` | the dated correction section, the candidate row, the ledger row |
| `guidance/corpus-browser-master-plan.md` | the E1 disposition row |
| `promised-deliverables.toml` | the V12 deliverable, and V11's reconciliation |

Deliberately **not** changed, and verifiable from `changed-files.txt`:
`src/web/browser/catena/catena.js`, `src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, everything under `src/web/data/`, the
release bindings, the common browser gate, the shared shell, Liturgy, the
PDFs, the CLI architecture, and every budget ceiling.

## 6. Startup commands and route state

All paths are repository-relative. Run from the checkout root.

The focused suite for this route is
`python3 -m unittest discover -s tools/tests -p 'test_catena*.py'`, and the
two V12 classes alone are
`python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -k V12`.
The generator-side structural check is `python3 scripts/_catena.py check` and
the promise ledger is `tools/tpt check-promised-deliverables`.

To see the page itself, build the public artifact with `make public-site` and
serve it with `python3 -m http.server --directory build/public-alpha/site`.
Then open the route with its required state:
`/catena/#book=Gen&chapter=1&bible=douay-rheims`. The real-browser gate over
that artifact is `node tools/tests/corpus_browser_gate.mjs`; set
`TRIPTYCH_CHROME` to the browser binary unless google-chrome-stable is the one
present.

Everything, including the inherited red targets, is `make -k check` and
`python3 -m unittest discover -s tools/tests`.

The route under review is the Catena Omnia page. Its route state is carried in
the URL hash, and the state the regressions exercise is a chapter holding one
fragment.

The production corpus is entirely present-valid, so **no contaminated state
can appear on any real route**. The three inputs this lane closes cannot be
reached from the tracked corpus at all, because a prototype and a drifting
descriptor are properties of a JavaScript object and not of a JSON document.
They are reachable only two ways: through the replay harness's stub network,
which the focused suite drives, and through the fixture corpus the screenshots
were captured from, whose every fragment renders the literal string
`ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA` in its own bytes, so each
such image is self-identifying. That is why the evidence is what it is, and it
is stated rather than glossed.

## 7. Implementation summary

`CLAIM-CLOSURE.md` is the full argument. In brief:

**The three findings are one defect** — the raw record was observed more
than once, and the observations were allowed to disagree. `ownData` made an
inherited member *invisible*, and invisible is not the same as refused: an
inherited prefix produced the claim that means genuine absence. `ownContract`
asked the prototype about three names, so a fourth went unasked. And the
carried path's descriptor was read once to test its stem and again for the
value, so the address that reached the network had passed no test.

**The correction is one function.** `requestSnapshot(record, names)` performs
exactly one `Object.getPrototypeOf` and exactly one
`Object.getOwnPropertyDescriptor` per requested name, and returns a
**null-prototype** record of **frozen own data**. Everything downstream — the
fallback decision, the composed address, the carried address, the refusal,
the ownership journal and the row the renderer consumes — is answered from
it. `REQUEST_MEMBERS` names the five fields that decide whether a request
happens, where it goes, and who owns the answer.

**The contract, stated so it need not be inferred:**

- a request-critical field answered by an **accessor** is declined without
  being called — invocation count **zero**, not one;
- a request-critical field answered by a **data descriptor** is read
  **exactly once per projection**, so the value validated is by construction
  the value projected and requested;
- **contamination** — a prototype of the record's own, anything above it
  naming a request-critical member, or an own accessor on one — is neither
  absence nor an ordinary refusal, but the single conservative
  malformed/unestablished state.

**`src/web/browser/catena/catena.js` is untouched.** The row it consumes is already a trusted
projection of own data properties, so the boundary did not need to cross
into rendering; the refusal is still consumed before the request sink and
that ordering is still pinned by its harness hook against a control that
really does fetch.

**Two committed assertions required the wrong answer and are corrected with
their reasons.** The spine's inherited prefix was pinned *equal to genuine
absence* — the review named that assertion — and an inherited carried path,
an accessor carried path and an inherited id were pinned as ordinary no-text
rows. Each now reaches the same conservative state as every other
contaminated claim. No other expected value in the file moved, and every
change makes a closure stricter.

**The package can now say which package it is.** V11 wrote `authoritative`
for both a completed validation battery and a sealing package attempt, so
the count could never be one. The two vocabularies are separated, their
legal transitions are stated in `PROVENANCE.md`, only a package attempt may
be authoritative, and exactly one may be. Every attempt writes into its own
log root. A coherence gate runs before publication and refuses on a second
authoritative attempt, on an authoritative attempt that is not this package
or this head, on an attempt both authoritative and superseded, on an
unresolved attempt described as final, and on any disagreement between the
ledger, the outer invocation log and the package's own prose.

That gate is proved by 18 focused tests, and one of them runs it against the
**sealed V11 package** and requires it to refuse — reproducing the
independent review's own finding without being told what it was.

## 8. Known limitations

Stated in full in `LIMITATIONS.md`, eleven of them. The four a reviewer
should read first:

1. **Read-once is per projection, not per render.** The page projects one
   spine three times (readability gate, tally, chain), so a whole render
   asks each request-critical descriptor three times — once per projection,
   never twice within one. The count is pinned at exactly three so a change
   fails loudly.
2. **A polluted `Object.prototype` closes every row on the page, not one.**
   That is the deliberate cost of the contamination rule and it is wider
   than V11's. The alternative was considered and rejected, for the reason
   given in `CLAIM-CLOSURE.md` §3.
3. **The authoritative terminal row is written before the archive exists**,
   because nothing may write inside the package after the manifest. It
   claims the sealed *directory*; the ZIP identity and the P8 verdict live
   in the sidecar and the outer log, bound together by the coherence gate,
   with a P7/P8 discard marker as the backstop.
4. **The screenshots show a fixture corpus, not the tracked corpus**, for
   the reason in §6. No file under `src/web/data/` was read, written or
   altered to produce them, and every capture read the rendered sentence
   back out of the DOM before the shutter.

## 9. Unresolved decisions

These are open questions this lane did not settle, and they are put to the
reviewer as questions in `REVIEW_REQUEST.md` rather than answered here.

1. **Is one descriptor read per projection the contract the review meant**,
   or does acceptance require one ask per whole render — which this lane
   does not deliver?
2. **Is page-wide fail-closed the right cost** for prototype contamination,
   or is a realm-wide refusal worse than the request it prevents?
3. **Are the three corrected expected values right?** In particular, should
   an inherited or accessor-backed carried path be *unestablished*, or
   remain an ordinary absence row on the ground that the fragment genuinely
   states no usable address of its own?
4. **Is a terminal row written before verification acceptable**, given the
   discard-marker backstop, or must the terminal word wait until after P8
   even at the cost of living outside the sealed bytes?
5. **Is collapsing the page's three projections per render worth a later
   lane?** Measured, not inferred; not a defect the review named.
6. **Does the model need a governed ceiling?** It has none and grew again in
   this lane. Re-asked, not answered; the budget owner's.

## 10. Artifact inventory

Every member of this package, and every artifact that lives beside it.

**Documents at the package root** — `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `PROVENANCE.md`,
`EVIDENCE-INDEX.md`, `DERIVED-CLAIMS.md`, `PRIVACY-AUDIT.md`,
`LIMITATIONS.md`, `UNRESOLVED-BLOCKERS.md`.

**Derived records at the package root** — `claims.json`, `checks.txt`,
`commits.txt`, `changed-files.txt`, `changes.patch`, `MANIFEST.sha256`.

**`logs/`** — one root per attempt, plus the pipeline's own sources and
transcripts. `logs/LOG-INDEX.md` is the mechanically derived index of every
one of them, and `logs/attempts.json` is the attempt ledger.

**`screenshots/`** — the before/after captures, `screenshots/INDEX.md`, and
`screenshots/capture-metadata.json`.

**Siblings, which live beside this directory and not inside it** —
20260817T194757Z-catena-e1-corrections-v12.zip, the transport copy;
20260817T194757Z-catena-e1-corrections-v12.zip.sha256, carrying its SHA-256 and its byte size;
20260817T194757Z-catena-e1-corrections-v12.assemble.log, the outer invocation log;
20260817T194757Z-catena-e1-corrections-v12.verify-final.log, the read-only P8 transcript; and
20260817T194757Z-catena-e1-corrections-v12.authority-coherence.log, the pre-publication authority gate's
transcript. They are outside the package because four of them cannot exist
until after the manifest is taken, and the fifth is the manifest's own
subject.

**Conditional artifact classes, and why any is omitted.** Screenshots are
required for this lane and are present. Print, no-JavaScript and
keyboard-focus captures are **omitted**: this correction changes no HTML and
no CSS, and the V11 review explicitly accepted that omission for the same
reason at the same route. A a sources record is **omitted**: this lane adds no
external source, edition, artifact or passage record. Real-device and
assistive-technology evidence is **omitted** because none exists for this
route; headless Chromium is not a device and is not an assistive
technology, and that gap is separately owned and recorded open.
