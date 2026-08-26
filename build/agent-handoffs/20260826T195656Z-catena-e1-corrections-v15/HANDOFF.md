# Catena E1 — V15 transport and completion ownership handoff

This package is the evidence for one bounded correction lane and nothing else.
It records no acceptance, marks no separately owned prerequisite complete, and
does not review its own work.

Every figure in this file is derived by `logs/derive-claims.py` at seal time and
rendered in `DERIVED-CLAIMS.md`; where one appears here it is repeated from
there, and `claims.json` is the machine-readable original. Where a figure came
from a command, `checks.txt` names the command and the log.

## 1. Task and intended outcome

Answer the V14 independent review — **CHANGES REQUIRED** at exact head
`69f2575421ba976271c936b1abd4b39dbe8b98fd`, recorded at review commit
`0d11766ec232b2b4e46a7d1b0ada56ef22370004` on
`review/catena-wave-1-e1-corrections-v14-independent` — with exactly its stated
next action and nothing else.

**This lane can name the review it answers, and V14 could not.** The V13 review
V14 had to answer was never published, and V14 recorded that gap rather than
filling it; every lane from V5 to V12 named its review by commit, and this one
does again. The V13 identity is still truthfully absent. It is V13's gap alone,
this lane does not need it, and it does not invent it.

The review passed, and this lane does not reopen: the post-projection
`unfetched` closure and its walking case; the raw authority inventory of the
chapter members the page reads; the tally as a consumer of its own; the raw post-projection audit;
the structural member add, remove, reorder, phantom and tally matrix; the
top-level and nested hostile source refusals; seventeen frozen structures at
their exact null-prototype scope; the carried-path and spine-prefix closures;
the fulfilled prewarm body proof; the rights, provenance and refusal DOM cases;
ordinary ownership through address selection; and the package protocol itself.

It found **one decisive semantic defect**:

> projection/row ownership is preserved through address selection, but
> discarded by the global path-keyed pending Promise cache before
> completion/body application.

`fragmentText(row)` asked the model for the address THROUGH the exact projected
row — and then reduced the answer to a path and entered a module-scope `Map`
keyed on that path alone, which held the unresolved PROMISE. A second projected
row carrying the same address did not make a request. It found unfinished work
under that key and joined it, and was handed the answer the first row's request
had been made for. Two owners became one owner. The paths matched, and that was
taken for ownership.

Beside it the review found: body application absent from the actual-object
identity roster; page-side helpers able to create a second valid-looking
authority over one chapter; the promised nested **edition** accessor case
missing from a matrix that claimed it; a descriptor count reported as one read
when it is three per source key and two per stated field; deep immutability
proved without a downstream rerender; and the evidence package materially
defective in the eight respects `PROVENANCE.md` enumerates.

The intended outcome: keep pending text work owned by the initiating row and
projection through transport, completion and body application, or share only
fulfilled immutable values; hold A, let same-path B settle independently with a
distinguishable body, then release A and prove B unchanged by actual object
identity; complete the body-application consumer roster; close the wrapper
ambiguity, the missing edition case, the descriptor accounting and the
downstream-mutation proof; and rebuild the evidence with exact portable
commands, a complete disclosed history and a coherent record of which tool
bytes ran — then
stop, for a fresh independent review.

**Not** in scope and not attempted: entering another E1 blocker, integration,
merge, deployment, re-signing any release-owned record, cutover, or any of the
broader blockers in `UNRESOLVED-BLOCKERS.md`.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v15`

Not a detached HEAD. Not merged with `origin/main`, which is
`e4085889fc1b3d2e6721b21166394fe5ea2dea9b`.

The immutable copy of this package is archived on
`evidence/catena-e1-corrections-v15-handoff`; that branch carries the package
and nothing else.

## 3. Current commit and base commit

| | |
| --- | --- |
| V15 head | `b9202882badbbbc364f1dd3d9057d2710ee47552` |
| parent, the exact candidate that review answered | `69f2575421ba976271c936b1abd4b39dbe8b98fd` |
| review addressed | `0d11766ec232b2b4e46a7d1b0ada56ef22370004` on `review/catena-wave-1-e1-corrections-v14-independent` |
| V14 evidence, carrying the reviewed package | `f74f8f4d4de44e21afdbef1fc4e9589a9898e986` on `evidence/catena-e1-corrections-v14-handoff` |
| V14 package this lane supersedes | `20260821T043622Z-catena-e1-corrections-v14`, 1,366,960 bytes, ZIP SHA-256 `414f303954d79b966f4d7f0ad6814376c0014fb73f8e2b78a0d4dc2495124bb1`; its own archive is the authority on how many members it holds |
| the implementation commit | `d53562245`, "Hold a request against the row that asked, all the way to the body" |
| the durable-records commit | `fc643930b`, "Record the V15 lane: pending work belongs to the row that asked" |
| the disclosure commit | `df246f77e`, "Disclose what the ownership split costs, and measure it" |
| the provenance correction | `b9202882b`, "Correct which review in this sequence was the unpublished one" — which is this head |
| the authoritative package attempt | `package-20260826T195656Z-06v11wpe`, established only after P8 passed and bound to the archive's own bytes by the `.authority.json` sibling |

The parent is an ancestor of the head and the range is four commits; both facts
are derived rather than asserted — see `claims.json` under `identity` and
`commits.txt`.

**The V14 package is not modified by this lane.** Its ledger slice is published
evidence on the V14 evidence branch, and appending a supersession row to it
would rewrite an artifact a reviewer may already hold. The supersession is
recorded where cross-lane dispositions have always been recorded: the durable
records. Each lane keeps its own ledger; this lane's is a fresh `V15` file.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was assembled,
and `claims.json` carries `identity.worktree_clean_at_head` derived from
`git status --porcelain` rather than asserted here. It also carries
`workspace_mode`, `worktree` and `git_dir_kind`, which V14 could not state and
this lane can: this lane ran in a fresh standalone clone with a real `.git`
directory and no worktree.

The batteries record tree state **per command**, before and after, so a step
that dirtied the tree is recorded dirty on its own row, and a battery refuses to
start on a tree that is not clean. See `checks.txt`.

## 5. Focused files changed

Seven files. **Two are production, and the page changes by roughly fourteen
lines.**

| file | what it is |
| --- | --- |
| `src/web/browser/catena/catena.js` | the transport itself: a path map that holds only settled answers and takes them from inside their own settle handler, a per-owner request held against `M.rowTransport(row)`, the frozen shared value, the first-settled-answer rule, the body application bound to `M.bodyAsked`, and one substitute record per name for a spine the page cannot read |
| `src/web/browser/catena/catena-model.js` | `rowTransport`, the frozen per-row transport owner; `bodyAsked`, asked at the body application; both witnessed as consumers; and three paragraphs of the page's own prose, moved here because the page has a ceiling and this file has none |
| `tools/tests/test_catena_wave_1.py` | nineteen new methods, their scenarios, the corrected late oracle with its former assertions quoted in place, and the replay instrumentation that records the transport owner, the body application and the four kinds of observation apart |
| `PROJECT-WORK.md` | the V15 lane record |
| `guidance/corpus-browser-roadmap.md` | the V15 section, the sixteenth-candidate E1 row and the dated ledger row |
| `guidance/corpus-browser-master-plan.md` | the E1 row moves from the V13 disposition to the V14 one |
| `promised-deliverables.toml` | the V15 deliverable with its twenty criteria |

A seventh file, `PROJECT-WORK.md`, also carries the measured disclosure of what
the ownership split costs: two owners asking one address concurrently now make
two requests where V14 made one, and across all 562 chapter spines under
`src/web/data/structure/catena/`, holding 1,356 fragments, no chapter has two
fragments sharing a text address or an id — so the concurrent case does not
arise on any page served from the tracked corpus.

`src/web/data/` has **zero** changes: every adversarial fixture lives in the
test file and is served by the replay harness's own stub network.
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints. No release binding, common gate, shared shell,
Liturgy, PDF or CLI path is touched, and `changed-files.txt` is derived from
`git diff --name-status` rather than typed here.

## 6. Startup commands and route state

All paths are repository-relative. Run from the checkout root.

The focused suite for this route is
`python3 -m unittest discover -s tools/tests -p 'test_catena*.py'`, and this
lane's own classes are
`python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -k V15`.
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
the URL hash. The states this lane closes are reached by opening a chapter whose
two fragments resolve ONE text address, and by stepping to a second chapter that
carries that same address while the first chapter's request is still in flight.

The production corpus is entirely present-valid, and no real server holds one
request open while a reader steps to another chapter, so **the held-transport
states are not reachable on any real route**. They are properties of when an
answer arrives, not of any JSON document, so this lane's cases are reachable
exactly one way: through the replay harness, which drives the real page under
Node against a stub DOM and a stub network whose answers can be parked and
released one ask at a time. Every assertion is taken at that page's own sinks —
the rendered body text, the row count, the refusal, the tally, the spoken status
line, the request journal, the ownership journal and the route.

## 7. Implementation summary

**`src/web/browser/catena/catena.js`.** A path map may hold only a SETTLED
answer, and it receives the promise from inside that promise's own settle
handler:

```js
const asked = T.loadJSON(path).then(
  (file) => {
    if (!fragmentTexts.has(path)) fragmentTexts.set(path, asked);
    return Object.freeze(file);
  },
  (error) => { asking.delete(owner); throw error; }
);
asking.set(owner, asked);
```

Nothing unresolved is reachable through `fragmentTexts`, because nothing
unresolved is ever put there. Work in flight is held in `asking`, a `WeakMap`
keyed on the owner the model hands out for the row. A failure settles nothing at
the path and releases only that owner's work, so retry stays real and no owner's
failure suppresses another's request. `Object.freeze` is applied where the value
becomes shareable. `if (!fragmentTexts.has(path))` is the first-settled-answer
rule: a request released late may not displace an answer another row already
has.

Body application is bound to ownership at the sink:

```js
if (!reading.contains(details) || !M.bodyAsked(fragment, loaded)) return;
```

Containment first, so a stale completion returns before it records anything and
the application roster holds the applications that HAPPENED. The failure arm
carries the same guard, because a reported failure is a body applied.

`gone(path)` returns one substitute record per name, so a spine the page cannot
read is one projection however often it is asked.

**`src/web/browser/catena/catena-model.js`.**

- **`rowTransport(row)`** is one frozen owner object per projected row, carrying
  the row, the projection that made it and the address it asks. It is created
  once and held against the row in a `WeakMap`, so the owner of a request is the
  same object when the request completes as when it was made, and a same-path
  sibling, a second projection of the same chapter and a re-render each own
  their own. `null` for a row no projection of this file made.
- **`bodyAsked(row, content)`** is asked AT the body application and records the
  projection, the row and the value being written. `false` for a row no
  projection made — fail-closed, one step later than `textAsked`.
- Both are witnessed, so the covered-consumer roster gains `transport` and
  `body` and now reaches the step that writes the page.
- Three paragraphs of the page's own prose moved here: why a 200 that is not a
  spine is not an empty chapter, why neither the paragraph layer nor its index
  may decide the page, and what the absence disclosure may say. The page has
  twenty-eight gzipped bytes of headroom under its whole-file ceiling and this
  correction is not payable out of twenty-eight; this file carries no ceiling.
  The page kept one-line pointers. This is disclosed in `LIMITATIONS.md`.

**`tools/tests/test_catena_wave_1.py`** adds nineteen methods and their
scenarios, and instruments the replay to record the transport owner, the body
application with the content and its frozen state, and four kinds of observation
apart. It also adds two harness capabilities the V14 proof could not have: one
address may answer two DIFFERENT documents in turn, and one ask of an address
may be parked while another goes through. Without the first, "B rendered the
words it asked for" and "B rendered the words A asked for" are the same
sentence, which is exactly why the V14 oracle could be green over the leak.

The argument is in `CLAIM-CLOSURE.md`; the figures are in `checks.txt`.

## 8. Known limitations

`LIMITATIONS.md` states them, each in a section of its own. In short: three
paragraphs of the page's prose now live in the model and a reader of the page
follows a pointer to them; the edition-accessor and observation-accounting work
closes PROOF gaps the review named rather than production defects, and the
parent passes those methods; the model is unbudgeted and grew again;
`src/web/browser/catena/catena.js` has a whole-file ceiling with very little
headroom; four stale release bindings remain unsigned; screenshots are omitted;
the browser gate is red at both endpoints; `make -k check` is red at both
endpoints; and every broader E1 blocker stays open.

## 9. Unresolved decisions

`REVIEW_REQUEST.md` carries the blocking questions and the optional notes.
`UNRESOLVED-BLOCKERS.md` lists every finding left open with its owner. None was
touched by this lane.

## 10. Artifact inventory

**In the package.** The hand-authored argument: `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `LIMITATIONS.md`,
`UNRESOLVED-BLOCKERS.md`, `PRIVACY-AUDIT.md`, `PROVENANCE.md` and
`EVIDENCE-INDEX.md`. The machine-derived record: `claims.json`,
`DERIVED-CLAIMS.md`, `checks.txt`, `commits.txt`, `changed-files.txt`,
`changes.patch` and `MANIFEST.sha256`. Under `logs/`: `logs/LOG-INDEX.md`,
`logs/attempts.json`, `logs/named-commits.json`, `logs/order-head.txt`,
`logs/order-parent.txt`, the per-attempt transcript directories, and the shipped
copies of every tool this pipeline runs.

**Beside the package**, and therefore *not* members of the manifest, because
each is written after the seal the manifest describes, named here by exact
filename:

- `20260826T195656Z-catena-e1-corrections-v15.zip` — the archive;
- `20260826T195656Z-catena-e1-corrections-v15.zip.sha256` — its digest and byte size;
- `20260826T195656Z-catena-e1-corrections-v15.assemble.log` — the outer invocation log;
- `20260826T195656Z-catena-e1-corrections-v15.verify-final.log` — the read-only P8 transcript;
- `20260826T195656Z-catena-e1-corrections-v15.authority.json` — the post-P8 final authority record;
- `20260826T195656Z-catena-e1-corrections-v15.executed-tools.json` — the contemporaneous executed-tool digests;
- `20260826T195656Z-catena-e1-corrections-v15.tool-bytes.json` — the P8 tool-byte comparison table;
- `20260826T195656Z-catena-e1-corrections-v15.attempts.jsonl` — this lane's attempt and battery history;
- `20260826T195656Z-catena-e1-corrections-v15.authority-coherence.log` — the pre-publication authority gate's transcript;
- `20260826T195656Z-catena-e1-corrections-v15.handoff-inventory.log` — this inventory's own transcript.

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
`7779d1f19ca175fd315cd7164f5347cc3c08d68b20b3b68a9219429b02bb8fa8` — and the
page's own change is in when an answer is applied and to whom, not in what the
page draws. The visible differences this correction does produce are reachable
only from a held transport, and each is asserted at its exact DOM sink, by
rendered text, row count, refusal presence, tally string, spoken status line,
request journal, ownership journal and route. A sources record is **omitted**:
this lane adds no external source, edition, artifact or passage record, and
`src/web/data/` has zero changes. A `logs/` directory is **present**.
