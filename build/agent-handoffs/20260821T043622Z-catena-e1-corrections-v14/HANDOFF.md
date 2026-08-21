# Catena E1 — V14 final projection-authority handoff

This package is the evidence for one bounded correction lane and nothing else.
It records no acceptance, marks no separately owned prerequisite complete, and
does not review its own work.

Every figure in this file is derived by `logs/derive-claims.py` at seal time and
rendered in `DERIVED-CLAIMS.md`; where one appears here it is repeated from
there, and `claims.json` is the machine-readable original. Where a figure came
from a command, `checks.txt` names the command and the log.

## 1. Task and intended outcome

Answer the V13 independent review — **CHANGES REQUIRED** at exact head
`6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` — with exactly its stated next
action and nothing else.

**That review has no published branch or commit.** `git ls-remote origin`
carries no `review/catena-wave-1-e1-corrections-v13-independent`; a branch of
that name exists only in a local reviewer checkout, standing at the reviewed
head with no review commit on it. Every earlier lane in this series named a
review SHA. This one cannot, `review_addressed` is empty in `claims.json` and
renders as an em dash in `DERIVED-CLAIMS.md`, and the gap is recorded in
`REVIEW_REQUEST.md` as this package's first blocker rather than filled with a
SHA nobody can fetch.

The review accepted the architecture and passed what V13 got right: one raw
chapter normalized once and held in a `WeakMap`; `requestSnapshot` correct for
one invocation; the inherited `text_prefix` and inherited `text_refused`
closures; the carried `text_path` read once; the page-wide fail-closed
contamination policy as a design; the planted scenarios it judged useful —
the carried path, the spine prefix, the walk over fragments and sources, the
prewarmed cache, rights and provenance, and refusal; and the package protocol V13 built. It found six things:

1. **`src/web/browser/catena/catena-model.js` reads raw `record.unfetched` during projection and
   `src/web/browser/catena/catena.js` rereads raw `file.unfetched` afterwards**, and the second raw
   value can replace the accepted projected chapter with `null` / `NO_CHAPTER`
   — inventing an unavailable state, removing rows and the recorded refusal,
   and altering the tally. Its walking probe answered `undefined` first and a
   forged string second, and observed `unreadable:false`, two reads, and the
   forged later value taken;
2. **"same instance" was not proved with `===`** — the harness independently
   called `chapterProjection(file)` beside each consumer and compared `.id`;
3. **the tally was not recorded as an independent consumer**, being collapsed
   into the rows;
4. **request ownership was reconstructed from path strings** rather than from
   actual projected row identity;
5. **nested source accessors could still produce internally contradictory
   projected semantics** — `sources["1"]` as an own getter declined for
   fragment provenance and invoked for projected voices and editions;
6. **the projection was frozen and its row objects were not.**

Beside them it named two evidence defects: the scenario for the chapter's
list of fragments was not structural, and "13 parent-failing methods" read as thirteen independent
semantic closures when it was eleven semantic methods, a hash pin and a
corrected oracle.

The intended outcome: remove the post-projection raw reread and prove it at the
production sinks with a walking case beside a steady control; observe the
actual object each covered consumer receives and compare it with `===`; record
the tally separately and publish a covered-consumer roster; bind a request to
the projected row object that initiated it, through same-path siblings,
same-path multi-projection and genuinely-late completion; make the member-list
case structural with a control for each effect; normalize nested source entries
and their fields exactly once under one rule; freeze the graph as deep as it is
trusted and assert it directly; audit the sources; and state the method
inventory truthfully — then stop, for a fresh independent review.

**Not** in scope and not attempted: entering another E1 blocker, integration,
merge, deployment, re-signing, cutover, packaging-tooling policy, or any of the
broader blockers in `UNRESOLVED-BLOCKERS.md`.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v14`

Not a detached HEAD. Not merged with `origin/main`, which is
`ac4b9d608f52e23f199c4b3149c73e5fb14c3d59`.

The immutable copy of this package is archived on
`evidence/catena-e1-corrections-v14-handoff`; that branch carries the package
and nothing else.

## 3. Current commit and base commit

| | |
| --- | --- |
| V14 head | `69f2575421ba976271c936b1abd4b39dbe8b98fd` |
| parent, the exact candidate that review answered | `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` |
| review addressed | **none published** — see §1 |
| V13 evidence, carrying the reviewed package | `fd5a1579d724069a06adca39b0a363064a212b1b` on `evidence/catena-e1-corrections-v13-handoff` |
| V13 package this lane supersedes | `20260817T233843Z-catena-e1-corrections-v13`, 1,306,976 bytes, ZIP SHA-256 `0965ca5ed6982a570427ae00e14a5bb7b38143bd36aaa90741fadd9eb93322b7`, re-verified by this lane against its own sidecar and authority record |
| the authoritative package attempt | `package-20260821T043622Z-13j6mmhy`, established only after P8 passed and bound to the archive's own bytes by the `.authority.json` sibling |
| the implementation commit | `5273bd00c`, "Take the chapter once, and let the row that asked own what it asked for" |
| the durable-records commit | `69f257542`, "Record the V14 lane: the row that asked owns what it asked for" — which is this head |

The parent is an ancestor of the head and the range is two commits; both facts
are derived rather than asserted — see `claims.json` under `identity` and
`commits.txt`.

**The V13 package is not modified by this lane.** Its ledger slice is published
evidence on the V13 evidence branch, and appending a supersession row to it
would rewrite an artifact a reviewer may already hold. The supersession is
recorded where cross-lane dispositions have always been recorded: the durable
records, which state V13's disposition as CHANGES REQUIRED and this candidate
as awaiting review. Each lane keeps its own ledger; this lane's is a fresh
`V14` file opened with `--fresh`, which refuses to open over an existing ledger
and refuses cross-lane appends.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was assembled,
and `claims.json` carries `identity.worktree_clean_at_head` derived from
`git status --porcelain` rather than asserted here.

The batteries record tree state **per command**, before and after, so a step
that dirtied the tree is recorded dirty on its own row rather than inheriting a
preflight's `clean`, and a battery refuses to start on a tree that is not
clean. See `checks.txt`.

## 5. Focused files changed

Seven files. **Two are production, and one of those changes by four
statements.**

| file | what it is |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | the sole substantial production change: the projected `unfetched`, the fragment inventory taken once, `normalizeSources`, the observation seam, the row-to-projection binding and row-resolved addresses, the tally's own entry point, and the builders that seal what they return |
| `src/web/browser/catena/catena.js` | four statements: the projected `unfetched` and the removed `file = null`, the tally's own call, and the request asked as a row |
| `tools/tests/test_catena_wave_1.py` | forty-one new methods, their scenarios, and the replay instrumentation that records object identity, request ownership, accessor invocation counts and inventory read counts |
| `PROJECT-WORK.md` | the V14 lane record, including the reconciliation of V13's own ledger against the review it received |
| `guidance/corpus-browser-roadmap.md` | the V14 section, the fifteenth-candidate E1 row and the dated ledger row |
| `guidance/corpus-browser-master-plan.md` | the E1 row moves from the V12 disposition to this one |
| `promised-deliverables.toml` | the V14 deliverable with its twenty-three criteria, and V13's four contradicted criteria reopened fail-closed |

`src/web/data/` has **zero** changes: every adversarial fixture lives in the
test file and is served by the replay harness's own stub network.
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints. No release binding, common gate, shared
shell, Liturgy, PDF or CLI path is touched, and `changed-files.txt` is derived
from `git diff --name-status` rather than typed here.

## 6. Startup commands and route state

All paths are repository-relative. Run from the checkout root.

The focused suite for this route is
`python3 -m unittest discover -s tools/tests -p 'test_catena*.py'`, and this
lane's classes alone are
`python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -k V14`.
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
the URL hash, and the states these regressions exercise are a chapter holding
one fragment, a recorded refusal, a lead entry and a blocked entry; a chapter
holding two fragments that resolve one text address; and a step to a second
chapter that carries that same address, which is how the same-path,
multi-projection and late-completion ownership cases are reached.

The production corpus is entirely present-valid, so **no walking record, no
proxied member list and no accessor-backed source can appear on any real
route**. A record that answers a second read differently, a list that answers
its length twice, and a getter standing where a document should be are all
properties of JavaScript objects and not of JSON documents, so the states this
lane closes are reachable exactly one way: through the replay harness, which
drives the real page under Node against a stub DOM and a stub network, and
which the focused suite runs. Every assertion in this lane is taken at that
page's own sinks — the rendered body, the row count, the refusal, the tally,
the spoken status line, the request journal and the route. That is why the
evidence is what it is, and it is stated rather than glossed.

## 7. Implementation summary

Two production files change, and the page changes by four statements.

`src/web/browser/catena/catena-model.js` carries every semantic addition,
because it has no gzip ceiling and the page has twenty-eight bytes of one.

- **`unfetched` is projected.** `normalizeChapter` already read it once; the
  projection now carries the normalized value, and `chapterUnfetched` answers
  from it. The page's second raw read is gone rather than memoized.
- **The member inventory is taken once.** `Array.prototype.slice.call` reads
  the raw list's length once and each index once; every later question is put
  to the array this file owns. `Array.isArray` is true of a proxy over a real
  array, which is why one read matters.
- **`normalizeSources` normalizes every nested source once, by descriptor.** An
  own accessor at a source key or on a shared field is never invoked, by
  anybody; a key whose value is not a plain record makes the chapter
  unreadable, whole. `translators` is normalized and frozen per edition.
- **`chapterWitness` is a bounded observation seam.** It is handed the exact
  object a consumer is about to read, at the moment it reads it, and is given
  no way to change what is returned; with no recorder installed each call is
  one `if` on a `null`. The authoritative reference is recorded inside
  `chapterProjection` immediately after the projection is made.
- **`rowOwners` binds each projected row to the projection that made it**, and
  `textAsked(row)` resolves a row's address and records the owning row and
  projection at that moment. A row no projection made resolves no address.
- **`chapterTally` is the tally's own entry point.**
- **The graph is sealed where it is made.** `fragmentRow`, `leadRow` and
  `blockedRow` freeze what they return; the extent and translator list are
  sealed with the row; the exported builders and the page hold one contract.
- **`said('acknowledgement')` is asked once** and both facts are derived from
  the one answer.

`src/web/browser/catena/catena.js`:

- `sound(bag(file).unfetched)` becomes `M.chapterUnfetched(file)`, and the
  `if (unfetched) file = null;` line goes — the projection of the page's own
  marker is already empty, so nothing downstream changes and one consumer stops
  seeing a different chapter from the others;
- `M.chapterFragments(file).length` becomes `M.chapterTally(file)`;
- `fragmentText(fragment.text_path)` becomes `fragmentText(fragment)`, and
  `fragmentText` asks the model for the address through the row.

`tools/tests/test_catena_wave_1.py` adds forty-one methods and the scenarios
they drive, and instruments the replay to record the object each consumer
received, the row and projection each request came off, nested accessor
invocation counts and member inventory read counts. The argument is in
`CLAIM-CLOSURE.md`; the figures are in `checks.txt`.

## 8. Known limitations

`LIMITATIONS.md` states seventeen, each in a section of its own. They are: the
V13 review has no published ref; V13's authority-gate negative roster is
neither confirmed nor reopened; the mutation probe covers one scenario;
identity is proved through a seam the production file carries; the nested
source closure is fail-closed and therefore wider than the defect; the walked chapter members that already held at the parent; the add, remove
and reorder cases that already held at the parent; this lane's first attempt ledger
is retired for an operator error the gate caught; P10's rows do not reach the
ledger slice shipped beside the archive; the discard and supersession markers
are covered by no sanitize pass; the model is unbudgeted and grew again;
`src/web/browser/catena/catena.js` has twenty-eight gzipped bytes of headroom; the four stale release bindings that remain
unsigned; the omission of screenshots; the browser gate is red at
both endpoints; `make -k check` is red at both endpoints; and every broader E1
blocker stays open.

## 9. Unresolved decisions

`REVIEW_REQUEST.md` asks four blocking questions and adds two optional notes.
The blockers, in short: whether a correction answering an **unpublished**
review can carry a disposition at all; whether the nested-source rule should be
fail-closed to the whole chapter or should drop the unreadable entry alone;
whether
refusing an address to a **copy** of a projected row is right; and whether one
scenario is enough for the mutation half of the immutability probe. The two
optional notes are whether a test-only observation seam belongs in shipped
browser bytes, and the unbudgeted model's growth, which four lanes have now
carried forward.

`UNRESOLVED-BLOCKERS.md` lists every finding left open with its owner. None was
touched by this lane.

## 10. Artifact inventory

**In the package.** The hand-authored argument: `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `LIMITATIONS.md`,
`UNRESOLVED-BLOCKERS.md`, `PRIVACY-AUDIT.md`, `PROVENANCE.md` and
`EVIDENCE-INDEX.md`. The machine-derived record: `claims.json`,
`DERIVED-CLAIMS.md`, `checks.txt`, `commits.txt`, `changed-files.txt`,
`changes.patch` and `MANIFEST.sha256`. Under `logs/`: `logs/LOG-INDEX.md`,
`logs/attempts.json`, `logs/named-commits.json`, `logs/order-head.txt`, `logs/order-parent.txt`,
the per-attempt transcript directories, and the shipped copies of every tool
this pipeline runs.

**Beside the package**, and therefore *not* members of the manifest, because
each is written after the seal the manifest describes, named here by exact
filename:

- `20260821T043622Z-catena-e1-corrections-v14.zip` — the archive;
- `20260821T043622Z-catena-e1-corrections-v14.zip.sha256` — its digest and byte size;
- `20260821T043622Z-catena-e1-corrections-v14.assemble.log` — the outer invocation log;
- `20260821T043622Z-catena-e1-corrections-v14.verify-final.log` — the read-only P8 transcript;
- `20260821T043622Z-catena-e1-corrections-v14.authority.json` — the post-P8 final authority record;
- `20260821T043622Z-catena-e1-corrections-v14.executed-tools.json` — the contemporaneous executed-tool digests;
- `20260821T043622Z-catena-e1-corrections-v14.tool-bytes.json` — the P8 tool-byte comparison table;
- `20260821T043622Z-catena-e1-corrections-v14.attempts.jsonl` — the complete append-only attempt and battery history;
- `20260821T043622Z-catena-e1-corrections-v14.authority-coherence.log` — the pre-publication authority gate's transcript;
- `20260821T043622Z-catena-e1-corrections-v14.handoff-inventory.log` — this inventory's own transcript.

The outer-sanitization pass writes two more of its own, whose names end
`.outer-sanitize.log` and `.outer-scan.log`. They are named here by their
suffixes rather than asserted as present because that pass runs last, after the
inventory and the authority gate, so that it can rewrite and re-scan their
transcripts too — and its own records therefore do not exist at the moment this
inventory is checked.

**Conditional artifact classes, and why any is omitted.** Screenshots are
**omitted**. This lane changes no ordinary visible composition:
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints — SHA-256
`733e84909e0e8049629187352d3800be320e469da7be200e860378bcc28851c5` and
`7779d1f19ca175fd315cd7164f5347cc3c08d68b20b3b68a9219429b02bb8fa8` — and
`src/web/browser/catena/catena.js` changes four statements. The visible
differences this correction does produce are reachable only from adversarial
payloads, and each is asserted at its exact DOM sink, by rendered text, row
count, refusal presence, tally string, spoken status line, request journal and
route. A sources record is **omitted**: this lane adds no external source,
edition, artifact or passage record, and `src/web/data/` has zero changes. A
`logs/` directory is **present**.
