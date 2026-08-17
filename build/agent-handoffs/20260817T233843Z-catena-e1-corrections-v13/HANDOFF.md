# Catena E1 — V13 one-chapter-projection handoff

This package is the evidence for one bounded correction lane and nothing
else. It records no acceptance, marks no separately owned prerequisite
complete, and does not review its own work.

Every figure in this file is derived by `logs/derive-claims.py` at seal time
and rendered in `DERIVED-CLAIMS.md`; where one appears here it is repeated
from there, and `claims.json` is the machine-readable original. Where a
figure came from a command, `checks.txt` names the command and the log.

## 1. Task and intended outcome

Answer the V12 independent review — **CHANGES REQUIRED** — with exactly its
stated next action and nothing else.

The review accepted `requestSnapshot` for one invocation and refused what the
page did with it. It passed the local closures, the page-wide fail-closed
contamination policy as a design, ordinary request behaviour, the
malformed/unestablished wording, the cold, present-valid and prewarmed
controls, the 36-field late vector, P8's non-execution and read-only
identity, the archive's arithmetic, the untouched earlier packages, and the
ownership boundaries. It found nine things:

1. one raw chapter was **projected three times**, so a record could answer one
   way while readability was decided and another way while the render was
   built, and the reported descriptor counts proved no source revisit;
2. `v12-drifting-carried-path` was **vacuous** — it exhausted its two values
   inside a projection that issues no request;
3. `logs/journal-dump.py` enumerated scenarios from a hand-maintained list
   that stopped at V11, so the packaged head and parent journals were
   byte-identical, carried no V12 scenario, and supported none of the
   closures the package claimed;
4. authority was established **before P7 and P8**, so a later failure left the
   sealed bytes still claiming it;
5. the authority gate accepted **six contradictions** it should have refused,
   and consumed neither the archive, the sidecar, the P8 transcript, the
   external ledger nor the sibling markers;
6. the attempt history was **not append-only in practice** — discarded
   attempts and set-aside cohorts absent, ordinals reused, terminal reasons
   empty, chronology internally untruthful;
7. the handoff inventory check was **lexical**, computing every verdict from
   `HANDOFF.md`'s text alone, never stat'ing a sibling, and accepting a
   limitation count that did not match the file;
8. **privacy was a blocker in two ways** — the tracked outer logs exposed the
   workspace path, the account name and the tool anchor, and a generic
   temporary root and a flattened workspace slug survived inside the archive;
9. the executed-byte claim covered **four of fifteen** shipped executables,
   and ran at P8, which proves shipped against trusted rather than executed
   against shipped.

The intended outcome: normalize each loaded chapter's request-critical state
**once**, hold that trusted projection, pass it unchanged through readability,
tally, request, cache, body and ownership; make all six planted scenarios
non-vacuous and ship their journals; and issue one package whose ledger,
authority, inventory, privacy scan and tool digests can each be checked
mechanically — then stop, for a fresh independent review.

**Not** in scope and not attempted: entering another E1 blocker, integration,
merge, deployment, re-signing, cutover, or any of the broader blockers in
`UNRESOLVED-BLOCKERS.md`.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v13`

Not a detached HEAD. Not merged with `origin/main`, which is
`549bf0790503bd873dd8ce6ea0a64cc34f91271d`.

The immutable copy of this package is archived on
`evidence/catena-e1-corrections-v13-handoff`; that branch carries the package
and nothing else.

## 3. Current commit and base commit

| | |
| --- | --- |
| V13 head | `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` |
| parent, the exact candidate that review answered | `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` |
| review addressed | `728c3e3b3d0d6e899f0da33e06a08a116375896f` on `review/catena-wave-1-e1-corrections-v12-independent` |
| V12 evidence inspected by that review | `05306fcfe221c1b0456501463e02323047635607` |
| V12 package that review verified | `20260817T194757Z-catena-e1-corrections-v12`, 1,842,342 bytes across 81 archive entries, ZIP SHA-256 `fa43918166b2d708c7911e3604834499260884d8433b9cd665bd7fc0ccf40890` |
| the authoritative package attempt | `package-20260817T233843Z-18once13`, established only after P8 passed and bound to the archive's own bytes by `20260817T233843Z-catena-e1-corrections-v13.authority.json` |
| the implementation commit | `42959f4c9`, "Normalize the chapter once, and let nothing read it again" |

The parent is an ancestor of the head, the range is
`two` commits, and both facts are derived rather
than asserted — see `claims.json` under `identity` and `commits.txt`.

The V12 review branch is a **sibling** at the reviewed head. It is not merged
in; this lane states its disposition rather than importing its commits.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was assembled,
and `claims.json` carries `identity.worktree_clean_at_head` derived from
`git status --porcelain` rather than asserted here.

The batteries record tree state **per command**, before and after, so a step
that dirtied the tree is recorded dirty on its own row rather than inheriting
a preflight's `clean`, and a battery refuses to start on a tree that is not
clean. See `checks.txt`.

## 5. Focused files changed

Seven files. **Two are production, and one of those changes by two lines.**

| file | what it is |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | the sole substantial production change |
| `src/web/browser/catena/catena.js` | two lines: the page's last two reads of raw chapter state become projection reads |
| `tools/tests/test_catena_wave_1.py` | the six walking scenarios, their controls, the identity tests and the harness hooks they need |
| `PROJECT-WORK.md` | the durable lane record |
| `guidance/corpus-browser-roadmap.md` | the dated correction section, the candidate row, the ledger row |
| `guidance/corpus-browser-master-plan.md` | the E1 disposition row |
| `promised-deliverables.toml` | the V13 deliverable, and V12's reconciliation |

Deliberately **not** changed, and verifiable from `changed-files.txt`:
`src/web/browser/catena/catena.css`, `src/web/browser/catena/index.html`,
everything under `src/web/data/`, the release bindings, the common browser
gate, the shared shell, Liturgy, the PDFs, the CLI architecture, and every
budget ceiling.

## 6. Startup commands and route state

All paths are repository-relative. Run from the checkout root.

The focused suite for this route is
`python3 -m unittest discover -s tools/tests -p 'test_catena*.py'`, and this
lane's class alone is
`python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -k V13`.
The generator-side structural check is `python3 scripts/_catena.py check` and
the promise ledger is `tools/tpt check-promised-deliverables`.

To see the page itself, build the public artifact with `make public-site` and
serve it with `python3 -m http.server --directory build/public-alpha/site`.
Then open the route with its required state:
`/catena/#book=Gen&chapter=1&bible=douay-rheims`. The real-browser gate over
that artifact is `node tools/tests/corpus_browser_gate.mjs`; set
`TRIPTYCH_CHROME` to the browser binary unless google-chrome-stable is the
one present.

Everything, including the inherited red targets, is `make -k check` and
`python3 -m unittest discover -s tools/tests`.

The route under review is the Catena Omnia page. Its route state is carried in
the URL hash, and the state the regressions exercise is a chapter holding one
fragment, plus one scenario that steps to a second chapter to prove the
census counts raw chapters and not consumers.

The production corpus is entirely present-valid, so **no walking record can
appear on any real route**. A record that answers a second read differently is
a property of a JavaScript object and not of a JSON document, so the states
this lane closes are reachable exactly one way: through the replay harness,
which drives the page under Node against a stub DOM and a stub network, and
which the focused suite runs. That is why the evidence is what it is, and it
is stated rather than glossed.

## 7. Implementation summary

`CLAIM-CLOSURE.md` is the full argument. In brief:

**The defect was not a second read inside one projection.** V12 closed that.
The defect was that one raw chapter was observed three times — `spineUnreadable`
projected to decide readability and threw the rows away, the tally projected
again to keep a length, `renderChain` projected a third time and kept the rows
that reach request, cache, body and ownership — so the projection that decided
a row was readable and the projection that produced the row were two different
projections, and only the first was ever tested. The reach was wider than
`text_path`: the voice control, the absence disclosure and the recorded
refusal each walked the raw record again, so the reader's provenance line and
the strongest sentence this page prints were composed from reads no
readability decision had seen.

**The correction is one normalization.** `normalizeChapter` reads each
request-critical member of the spine into a local exactly once — `fragments`,
`sources`, `refusals`, `unfetched`, `blocked`, `leads`, and `text_prefix`
through the V12 snapshot — projects the rows and freezes each with its extent
and translators, walks `sources` once for the voices and the editions, takes
the readability verdict from that same walk, normalizes the recorded refusals
into a null-prototype map of frozen rows, and returns a frozen null-prototype
projection. `chapterProjection` holds it against the raw record in a
`WeakMap`. `spineUnreadable`, `chapterFragments`, `chapterVoices`,
`chapterBlocked`, `chapterLeads`, `refusalNote` and `absenceRows` all answer
from it and reach past it to the raw chapter nowhere.

**Identity is observable rather than argued.** `chapterProjection` is
exported, `chapterPasses()` is the census of raw chapters normalized, and the
replay harness asks every model entry point that takes a chapter which
projection it resolved to before it answers — so "one identity, everywhere" is
a comparison of recorded lists. A consumer not routed through the projection
fails the identity test by the name that is missing.

**`src/web/browser/catena/catena.js` changes by two lines and gets smaller.**
`M.blockedRows(file && file.blocked)` and `M.leadRows(file && file.leads)`
were the page's last reads of raw chapter state and became
`M.chapterBlocked(file)` and `M.chapterLeads(file)`. The page's whole-file
headroom improves from 20 to 26 gzipped bytes.

**Six of six are non-vacuous, and each fires at a different sink.** Each
scenario walks a single member of the chapter between projections and plants
something only a later projection can reach; each stands beside a control
holding that member at the walked-to value, so every planted thing is proved
reachable and renderable. At the parent the walked carried path fetches and
renders the deeper address, the walked prefix composes and fetches the same,
the walked member list renders and fetches a body off members readability
never approved, the walked editions put a forged rights claim on the reader's
provenance line, the walked refusals print a Rule 4 boundary the record never
stated, and the prewarmed walk misses a warm cache to fetch a second body. The
parent asks the walked member 3, 3, 5, 8, 4 and 3 times for one render; this
head asks each exactly once.

**One committed assertion required the wrong answer and is corrected with its
reason.** `v12-drifting-carried-path` was pinned to make no text request at
all — the scenario exhausting its two values in a projection that cannot
request, which is what made it vacuous — and now requests the one address the
one projection validated. The page-level descriptor pin moves from three to
one for the same reason. No other expected value moved.

**The package can now show what it claims.** The journal roster is derived
from the test file rather than hand-maintained. Final authority is
established after P8 and binds the archive's basename, byte size, SHA-256, P8
result and post-P8 rehash, each recomputed from the archive; an in-package row
may claim at most `sealed`. The authority gate consumes every post-P8 artifact
and its negative roster covers each of the six contradictions it previously
accepted; run against the V12 package it refuses it. The ledger identity is
pinned to the lane, ordinals are monotonic and never reused, every terminal
state carries its reason, a battery may be recorded set aside, and chronology
is checked. The inventory tool resolves every referenced path, recomputes
every quoted digest, discovers and stats every sibling including its own
output, and counts members, logs, journals, tools and ledger rows
mechanically. Every tool invocation records the SHA-256 of the exact bytes
immediately before it runs, and P8 compares executed against trusted against
shipped. The sanitizer's pattern gaps are closed, it gains a mode for
non-member files, and every outer sibling is sanitized and re-scanned before
it is committed.

**Validation, measured at both endpoints** — this head and the exact reviewed
parent — because an exit code cannot tell an inherited failure from a caused
one. Focused Catena is **555** green at this head, up from **544** at the
parent, and this head's test file replayed against the parent fails
twenty-seven ways across thirteen methods. `scripts/_catena.py check` passes at
1,351 fragments / 1 book / 73 canon entries. Full discovery is **1,906** at
this head and **1,895** at the parent, with the identical inherited 14
failures, 13 errors and 11 skips at both, and the same 27-entry
failure-and-error identity set — **none of them a Catena identity**.
`make -k check` exits 2 on the same four inherited targets at both endpoints:
`check-web-editions-current`, `check-release-bindings`, `check-tool-registry`
and `check-examples`. The browser gate is identical at both endpoints, and
identical to the V10, V11 and V12 reports: 2,290 assertions — 1,836 pass, 226
fail, 228 skip — across 171 pages and 19 routes. The promise ledger validates at 38 tracked /
19 complete. Budgets are unraised: `src/web/browser/catena/catena.css` is byte-identical at both
endpoints at 7,629/8,000 whole and 2,676/2,700 stripped, and `src/web/browser/catena/catena.js` is
smaller at both, 12,974/13,000 and 7,546/8,800 against the parent's 12,980 and
7,554. The unbudgeted model grows 34,367 to 36,679 gzipped whole and 8,258 to
8,873 stripped. `src/web/data/` has zero changes. Four stale Catena release
bindings remain fail-closed and unsigned; none was re-signed.

## 8. Known limitations

Stated in full in `LIMITATIONS.md`, **twelve** of them. The four a reviewer
should read first:

1. **The projection is per raw chapter object, not per chapter address.** One
   raw chapter load is one normalization however many consumers ask; a second
   fetch of the same address is a second raw record and a second projection,
   and the census counts two.
2. **A projected row is frozen where it is made**, which is a capability
   removed as well as a seal applied: the replay harness's own hook had to
   change from assigning onto a row to copying it.
3. **Final authority is a sidecar outside the archive.** An archive cannot
   contain its own digest, so the binding runs one way, and a reviewer holding
   only the ZIP holds the sealed candidate rather than the authority.
4. **The model is unbudgeted and grew again**, from 34,367 to 36,679 gzipped
   whole, while both governed measures on this route improve.

## 9. Unresolved decisions

These are open questions this lane did not settle, and they are put to the
reviewer as questions in `REVIEW_REQUEST.md` rather than answered here.

1. **Is one projection per raw chapter load the contract the review meant**,
   or does acceptance require one projection per chapter address, or per
   render, across cache misses this lane does not prevent?
2. **Is freezing the projected rows acceptable**, given it changes what a
   harness — and any later consumer — may do with a row?
3. **Is `WeakMap` retention right**, when the page's own cache already retains
   every raw chapter for the life of the page?
4. **Is authority as an external sidecar bound one way to the archive
   acceptable**, given the archive cannot contain the record that establishes
   it?
5. **Does the model need a governed ceiling now?** It has none and grew again
   in this lane. Re-asked, not answered; the budget owner's.

## 10. Artifact inventory

Every member of this package, and every artifact that lives beside it. The
inventory is checked by `logs/handoff-inventory.py`, which resolves every path
named here, discovers and stats every sibling including its own output, and
recomputes every digest quoted; its transcript is a sibling and is named
below.

**Documents at the package root** — `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `PROVENANCE.md`,
`EVIDENCE-INDEX.md`, `DERIVED-CLAIMS.md`, `PRIVACY-AUDIT.md`,
`LIMITATIONS.md`, `UNRESOLVED-BLOCKERS.md`.

**Derived records at the package root** — `claims.json`, `checks.txt`,
`commits.txt`, `changed-files.txt`, `changes.patch`, `MANIFEST.sha256`.

**`logs/`** — one root per attempt, plus the pipeline's own sources and
transcripts. `logs/LOG-INDEX.md` is the mechanically derived index of every
one of them, and `logs/attempts.json` is this lane's ledger rows.

**The archive, and where its identity is stated.** This member cannot
state it. `MANIFEST.sha256` is taken before the archive exists, and nothing
writes inside the package after that instant, so a byte count and a digest of
the archive written HERE would be a number composed before its subject. The
archive's identity is therefore stated by the sibling records that are written
after it: `20260817T233843Z-catena-e1-corrections-v13.zip.sha256`, which carries its SHA-256 and its
byte size, and `20260817T233843Z-catena-e1-corrections-v13.authority.json`, which carries the
basename, the byte size, the SHA-256, the P8 verdict and the post-P8 rehash
digest together, each recomputed from the archive itself rather than carried
forward from the step that made it. P8 recomputes the same two values before
and after every check it runs and fails hard if they differ. The binding runs
one way — the record names the archive's digest, and the archive contains no
member matching `*.authority.json` — so there is no self-reference to unwind.

**Siblings, which live beside this directory and not inside it.** Ten
siblings, each named exactly, because a package that omits one of its own
outputs from its inventory is the V12 finding this list exists to answer:

- `20260817T233843Z-catena-e1-corrections-v13.zip` — the archive, the transport copy of this
  directory;
- `20260817T233843Z-catena-e1-corrections-v13.zip.sha256` — its digest-and-size sidecar;
- `20260817T233843Z-catena-e1-corrections-v13.assemble.log` — the outer invocation log;
- `20260817T233843Z-catena-e1-corrections-v13.verify-final.log` — the read-only P8 transcript;
- `20260817T233843Z-catena-e1-corrections-v13.authority.json` — the post-P8 final authority
  record, naming the attempt, the exact head, the archive's basename, byte size
  and SHA-256, the P8 result and the post-P8 rehash result;
- `20260817T233843Z-catena-e1-corrections-v13.executed-tools.json` — the contemporaneous
  executed-tool digests, one row per invocation, taken from the exact bytes
  immediately before each ran;
- `20260817T233843Z-catena-e1-corrections-v13.tool-bytes.json` — the P8 tool-byte comparison
  table: executed against trusted against shipped, per tool, with each tool's
  disposition;
- [`20260817T233843Z-catena-e1-corrections-v13.attempts.jsonl`](20260817T233843Z-catena-e1-corrections-v13.attempts.jsonl) — the complete
  append-only attempt ledger for this package, every attempt and every battery
  cohort;
- `20260817T233843Z-catena-e1-corrections-v13.authority-coherence.log` — the pre-publication
  authority gate's transcript;
- `20260817T233843Z-catena-e1-corrections-v13.handoff-inventory.log` — the handoff inventory's
  transcript, which is itself discovered and stat'd by the run that writes it.

They are outside the package because none of them can exist until after the
manifest is taken, and because the archive must not contain the record that
names its own digest.

**Two further artifacts join them after these gates, and cannot be named here
as present.** The outer-sanitization pass runs last of all, after the inventory
and the authority gate, precisely so that it can rewrite and re-scan their
transcripts too; its own two transcripts are named for this package and carry
the `.outer-sanitize.log` and `.outer-scan.log` suffixes. Naming them as
members of the list above would be this file asserting the existence of
something that does not exist when the list is checked, which is the class of
claim this inventory exists to refuse. The pass's own record of what it
rewrote and what it then found is what those two carry.

**Conditional artifact classes, and why any is omitted.** Screenshots are
**omitted**. This correction changes no HTML and no CSS: `src/web/browser/catena/catena.css` is
byte-identical at both endpoints, and `src/web/browser/catena/catena.js` changes two lines that swap
one model call for another. What differs visibly is which body text a walking
adversarial fixture causes to render, and that difference is asserted at the
DOM by the replay harness and journalled per request in the packaged ownership
journals — which records what rendered and what was asked for, rather than a
raster of it. Print, no-JavaScript and keyboard-focus captures are **omitted**
for the same no-HTML-no-CSS reason, which the V11 and V12 reviews each
accepted at this route. A sources record is **omitted**: this lane adds no
external source, edition, artifact or passage record. Real-device and
assistive-technology evidence is **omitted** because none exists for this
route; headless Chromium is not a device and is not an assistive technology,
and that gap is separately owned and recorded open.
