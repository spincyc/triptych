# Catena E1 — V11 claim-closure handoff

This is the factual entry point, and it is meant to be readable alone. The
protocol requires ten contents; the V10 package carried eight, because its
limitations and its unresolved decisions were three lines of filenames
instead of statements. Sections 8 and 9 below state them here, in this file.
The sibling documents are the fuller treatment, not the location of the
answer.

## 1. Task and intended outcome

Answer the fresh independent review of V10 — disposition **CHANGES
REQUIRED** — with exactly the review's stated next action and nothing else:
close the exported claim boundary over its MEMBERS rather than only its
shapes; stop one sentence from asserting two facts that most of the states
it was given had not established; complete the genuinely-late terminal
vector from 13 guarded fields to all 36; give the packaged request journal
the ownership the live harness already recorded; and correct the package,
provenance and privacy defects the review found.

The intended outcome is a **reviewable** head, not an accepted one. This
lane records no acceptance of its own work, marks no separately owned
prerequisite complete, and does not review itself. It merges nothing,
re-signs nothing, deploys nothing and integrates nothing. Every finding
outside those five is open and untouched, and the reviews' own records on
their review branches remain the authoritative statement of each.

This package mutates nothing. It names, and does not touch, the earlier
sealed packages on their evidence branches. It supersedes the V10 package
in the protocol's sense — a corrected handoff is a new package that names
the earlier one — while that sealed artifact stands exactly as its review
left it.

## 2. Branch

Branch: `impl/catena-wave-1-e1-corrections-v11`. This is a branch, not a
`detached HEAD`.

## 3. Current commit and base commit

Head (current commit SHA): `0255b84996e1dc24da3ce75ac318c4f774b7957c`.

Base (the task's parent, and the exact reviewed V10 candidate):
`ea15d16d22d7ceaed989ed9907c236f967738a03`.

Review answered: `f7cad8b0219de8343a0b2cce95e89558ded6946e`, on branch
`review/catena-wave-1-e1-corrections-v10-independent`. That review
independently inspected the V10 evidence commit
`ff49c83e4f26570bd4c07d8fc8703f94c331d92a` and independently verified the
V10 package's archive SHA-256
`4c71d1c15bd1f1992bf29a1d84342f11a8b671b5b5bd6bdcc4341de091e23e2f`. It is a
sibling of this line at the reviewed head and is **not merged in**; this
package states its disposition rather than importing its commits.

The head is the base plus two commits:
`3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8`, the production correction and
its proof, and `0255b84996e1dc24da3ce75ac318c4f774b7957c`, the durable
records. Current `origin/main` is
`e7f468e842727a817631d12f0854f8249556a8ff`; this lane is **not integrated**
with it.

Every identity above is also derived mechanically: `claims.json` and its
rendering `DERIVED-CLAIMS.md` are computed in one pass from the frozen
member inventory, and `logs/head-consistency.py` refuses a package whose
prose names a commit those claims do not entitle it to name. The commits
this package discusses without having been produced from them are declared,
each with its reason, in `logs/named-commits.json`.

## 4. Uncommitted changes

The reviewed state is the committed head with **no uncommitted changes**.
Both battery ledgers open with a contemporaneous preflight recording the
exact `sha=` and `porcelain=clean`, and — new in V11 — every command row
carries its own `TREE-BEFORE:` and `TREE-AFTER:` reading rather than
inheriting the preflight. One recorded command deliberately dirties the
tree: on the parent side, `head-tests-against-parent` copies the head's test
file over the parent's before running it, because the substitution is what
makes the run mean what it means. That row and the row after it are recorded
dirty on their own rows, and the parent battery's postflight closes dirty
too — the overlay was not reverted before that battery ended, and the ledger
records what it observed rather than a clean tree it did not. Nothing about
the reviewed head depends on it: the head battery opens and closes clean at
the head, and the two dirty parent rows are exactly the two steps whose
purpose is to run the head's test file against the parent's production
files. `logs/order-head.txt` and `logs/order-parent.txt` are the ledgers.

## 5. Focused files changed

Two commits, seven files, 1,208 insertions and 47 deletions against the
base.

Production:

- `src/web/browser/catena/catena-model.js` — the own-data descriptor
  reading of every semantic claim member, the projected `said` member, and
  the choice between the two no-text sentences.
- `src/web/browser/catena/catena.js` — one line: the row now carries the
  model's chosen note instead of the single refused constant.

Proof:

- `tools/tests/test_catena_wave_1.py` — the fourteen-case inherited and
  accessor matrix, the sink-driving sweep, the 36-field late vector with its
  coverage test, and the renderer-ordering hook.

Durable records:

- `PROJECT-WORK.md`, `guidance/corpus-browser-roadmap.md`,
  `guidance/corpus-browser-master-plan.md`, `promised-deliverables.toml`.

Untouched and byte-identical to the base:
`src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, `scripts/_catena.py`, and every file
under `src/web/data/`. `changed-files.txt` is the derived inventory and
`changes.patch` the exact diff, both regenerated at the sealed head.

## 6. Startup commands and route state

From the repository root, build and serve the public artifact:

    make public-site
    python3 -m http.server --directory build/public-alpha/site

Then open the route with its required state:

`/catena/#book=Gen&chapter=1&bible=douay-rheims`

The production corpus is entirely present-valid, so **no no-text sentence
can appear on any real route**. The three no-text states are reached only
through adversarial fixtures, two ways:

- the replay harness, which the focused suite drives:
  `python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py'`;
- the page's own documented `?data=` parameter pointed at a four-chapter
  fixture corpus outside the tracked data, which is how the adversarial
  screenshots were captured. Every fixture fragment renders the literal
  string `ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA` in its own bytes,
  so each such image is self-identifying.

Three read-only verification commands, each checked against the tool's own
argument parser before being published here — the V10 package published two
that could not run, one missing a required positional and one passing an
archive positionally to a parser that takes `--zip`:

    python3 logs/sanitize-and-seal.py . --check-only
    python3 logs/sanitize-and-seal.py . --verify
    python3 verify-final-package.py --zip PACKAGE.zip --sidecar PACKAGE.zip.sha256

The first two run from the extracted package root, where `.` is the required
`package` positional. The third runs from a trusted directory **outside**
the archive: its `--tools` argument defaults to the directory holding the
verifier that is running, so running the extracted copy would make the trust
anchor archive-derived. Substitute the package's own name for `PACKAGE`.

## 7. Implementation summary

**The exported claim boundary closed only its shapes.** `bag()` established
that a record had arrived, and ordinary property lookup then answered from
wherever it found an answer. So `Object.create({stated: false, trail: ''})`
presented itself as this route's own absence and opened the carried fallback
door, and an inherited valid statement composed a text address the page
never derived; mixed forms did the same, and an accessor could run merely
because the boundary read it. The committed matrix was eight plain object
literals and probed none of that.

Now every semantic member is read **once, as an own DATA property**, through
`Object.getOwnPropertyDescriptor`. Nothing inherited is seen. An own
accessor is **never invoked** — asserted at zero invocations — so a getter
with a side effect does not run and a drifting getter has no second read to
disagree with. Where a claim's own three-member contract — `stated`, `said`,
`trail` — is partly written above it, the claim **fails closed** rather than
being adjudicated. The same reading covers the spine's own `text_prefix`,
the carried `text_path`, the fragment's `id` and `source`, the edition join
and the extent members.

**One sentence was doing the work of two.** `A text reference was supplied
for this fragment, but it cannot be used as written` asserts that a
reference was supplied and that it was written unusably. V10 gave it to
every state that resolved no text — `null`, a record, a list, a number, a
flag, `''`, whitespace, and every bare, contradictory, inherited or
accessor-backed claim — none of which establishes either fact. A third
sentence now exists for those states: `No text reference is established for
this fragment, so no text is shown.` It makes no holdings, file-existence,
request-failure or blame claim. The stronger sentence is kept only where
both facts hold: a real `structure/paragraphs/` prefix, and the right
namespace wrapped in whitespace.

**The proof's three holes are pinned shut.** A fourteen-case inherited and
accessor matrix pins that no such claim creates a request, reopens the
carried door, composes a path, changes the refusal or absence state, renders
a body or alters ownership — with the accessors asserted at zero calls, and
the ordinary dispositions asserted beside it as positive controls. Every
unestablished prefix is now driven to the **visible and the request sink**
against a planted carried body, where the V10 neutrality test inspected a
constant and drove nothing. The genuinely-late terminal vector states an
expected value for **all 36** guarded fields at both ends of the release,
with a coverage test that fails the moment a field joins the guard without
joining the proof, and a renderer hook pins the before-the-sink ordering
against a control that really does fetch.

**The packaged journal now reproduces ownership.** Each row states sequence,
address, the kind of record that address holds, the owning phase, and the
outcome: completed, held, released or failed.

**The package protocol is corrected where the review found it false.** P8
executes no Python out of the reviewed archive; it runs trusted
out-of-archive copies, records each tool's trusted and shipped SHA-256,
fails hard on divergence, and rehashes the archive after every check with an
explicit pre/post equality verdict. Provenance is read per command. Log
identity is allocated from an append-only attempt ledger outside the
package, so an ordinal names the attempt and a slug names the step. Archive
entries carry a fixed epoch and derived modes. The sanitizer gained
convention-shaped workspace and lane-evidence rules and moves a local
timestamp to its UTC instant instead of blanking the offset. And a new
inventory tool checks this file against the protocol's ten required contents
and reproduces the review's eight-of-ten finding against the V10 package
unaided.

**Measured at this head.** Focused Catena 534 green, up from 522.
`scripts/_catena.py check` 1,351 fragments / 1 book / 73 canon entries. Full
discovery 1,885 tests, with the inherited 14 failures / 13 errors / 11 skips
and the same 27-entry identity set, none of them a Catena identity. Browser
gate 2,290 assertions at 1,836 / 226 / 228 over 171 pages and 19 routes,
identical to the V10 report. Promise ledger valid at 36 tracked / 19
complete. `make -k check` exits 2 on the **same four targets at the parent
and at this head** — `check-web-editions-current`,
`check-release-bindings`, `check-tool-registry`, `check-examples` — measured
at both endpoints, all four inherited; V10's claim that the web-editions
target was additional at its head was false and is not repeated. Budgets
unraised: `src/web/browser/catena/catena.css` byte-identical at 7,629/8,000
whole and 2,676/2,700 stripped; `src/web/browser/catena/catena.js`
12,980/13,000 whole and 7,554/8,800 stripped — smaller than V10's 12,987, so
the page's headroom improves from 13 gzipped bytes to 20. The unbudgeted
model grows 29,741 to 32,406 gzipped whole, disclosed rather than presented
as unchanged load. Four stale release bindings remain fail-closed and
unsigned; none was re-signed. `src/web/data/` has zero changes.

**One measurement caution.** Full discovery run concurrently with
`make -k check` reports 250 errors instead of 13, because that target builds
and then removes `build/.web-current` and the public site underneath the
tests. Every figure above comes from an isolated, ledgered run; the raced
run is recorded as discarded and backs no claim.

## 8. Known limitations

These are stated here, not delegated. `LIMITATIONS.md` is the fuller
treatment of the same twelve.

1. **The scope is one correction, and this head is not a candidate for
   acceptance.** A review of this package can accept the claim closure at
   most. It cannot accept E1, and this package claims nothing wider.
2. **The request sink proved is the replay harness's stubbed `fetch`
   seam, not a real network capture.** It is a claim about which addresses
   the production files hand to the network boundary, when, and under which
   phase. The browser gate did run in real Chromium at both ends, over the
   built site, but it asserts the shared shell's generic contract, not this
   route's request journal.
3. **The own-data closure covers the claim's small fixed contract and the
   request-composing members only.** The wide fragment and edition
   contracts remain field-validated rather than prototype-hardened. That is
   a deliberate boundary of this correction, not a completed hardening.
4. **Fail-closed has a real cost.** A polluted object prototype closes every
   valid row on the page rather than one contradictory row. The alternative
   — ignoring inherited values — was rejected because the route's own
   directions require that an own valid state beside an inherited refusal
   marker make no request.
5. **The pipeline that builds this package is not under version control in
   this workspace.** The P8 trust anchor is therefore recorded by path and
   per-tool SHA-256 rather than by a commit. It sits outside the archive but
   is not independent of the party that built the package, and the
   transcript says so verbatim.
6. **Six of the eight adversarial screenshot pairs are byte-identical, by
   design.** The absent, present-valid and refused states render exactly as
   the parent rendered them at both viewports. Two pairs differ, both the
   unestablished state: 11,392 of 1,296,000 pixels at 1440x900 and 13,639 of
   334,836 at 393x852. Nothing here asserts a visual difference that was not
   captured, or what an uncaptured image would have shown.
7. **Print, no-JavaScript and keyboard-focus captures were not produced.**
   The changed sentence sits inside a `<details>` disclosure a print
   stylesheet does not open by itself; with scripts off the route serves a
   static block and no fragments at all, so an image would show the same
   thing twice. **For the keyboard-focus capture there is no stated reason
   at all** — it simply was not taken, and this package carries no
   focus-visible raster evidence for the changed row. The gate reports do
   carry a `focus-indicator-differs-from-resting` phase over all 171 pages,
   but that is a check of the shared shell's generic contract, not an image
   and not evidence about this row.
8. **The screenshots were captured at the first of this lane's two
   commits**, `3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8`, and the capture
   metadata says so. The exact head is one commit later; the two differ only
   in durable records, and the four Catena files a browser loads are
   byte-identical between them, which is why the captures bind to the head.
   They are not relabelled, because they were not taken there.
9. **The parent-side battery figures are inherited, not adjudicated.** The
   package proves the failing sets match at both endpoints under named
   volatile exclusions; it does not prove they are acceptable. A pinned
   expected value is called a vector here; a parent-side figure is called
   inherited; neither is called a baseline.
10. **One figure is only valid in isolation.** The raced full-discovery run
    is discarded and used nowhere, and this is recorded because it is the
    shape of an error this package came close to making.
11. **The 36-field vector is complete for the guard, not for the route.**
    Broader terminal proofs for the other corrected classes remain open.
12. **Judgements are not derivations.** Whether the conservative sentence is
    truthful enough, whether fail-closed is right, whether the vector is
    complete, and whether the corrected protocol answers the review are
    judgements, and they are asked rather than asserted.

## 9. Unresolved decisions

Two kinds, and both are stated here rather than pointed at.
`REVIEW_REQUEST.md` carries the questions in full and
`UNRESOLVED-BLOCKERS.md` the open findings in full.

**Decisions this lane could not make for itself, and asks a reviewer to
make.** Is the conservative sentence `No text reference is established for
this fragment, so no text is shown.` truthful and neutral enough, and
distinct enough from the other two, to accept? Is fail-closed the right
disposition for a claim whose three-member contract is partly inherited,
given that the page-wide failure mode is the price? Is the 36-field vector
now complete, and is the guard itself the right set of 36? Does the
corrected package protocol answer the review's package, provenance and
privacy findings, and is a per-tool digest anchor an acceptable substitute
for a commit-pinned one? Two further questions are optional: whether the
no-text rows should carry a machine-readable marker as well as a sentence,
and — re-asked, not answered — whether the model and the combined route
payload need a governed ceiling.

**Findings left open, each with the lane or role that owns it.** Owned by
the next authorized E1 correction lane: projection is still not the sole
semantic source beyond this inherited-claim boundary; orphan raw sources
still manufacture voice offers and absence rows; a `source`-only fragment is
invalid and still counts; scalar and nested translator coercion; malformed
and padded absence findings, including the padded `" none-published "` false
negative; refusal `verse` typing, unchecked in five shapes; broader partial
selection, neither closed nor order-independent, including the non-injective
ranking key; unreadable roots still becoming Catena claims, and the
unreadable `src/web/data/bibles.json` prose; and the broader terminal and
corrected-oracle proofs outside this lane's vectors. **One of those items is
unenumerated and is stated as such**: the corrected oracles that still bless
the defects are recorded by the reviews as a class, not as a list, and
neither the review records nor this package enumerates them — that is a gap
in the record, not a claim that the class is small.

Owned by a separately authorized integration lane: the duplicated semantic
model across `scripts/_catena.py` and the browser model. Owned by the budget
owner: the uncapped model and combined route payload, disclosed here and
governed nowhere. Owned elsewhere entirely, and none of it this lane's or
the next E1 lane's: the historical `src/web/data/` Day-reader guard
contradiction; the four stale release bindings, fail-closed and unsigned;
the common browser gate's inherited failure population; B0 and the shared
shell; real-device and assistive-technology evidence; protected Liturgy;
PDF prerequisites; and the eventual reconciliation of the cumulative
implementation and review history at integration time.

**E1 is not integrated**, and nothing in this package authorizes a merge,
a re-signing, a deployment or a cutover.

## 10. Artifact inventory

Every member of the package, and every artifact beside it. A member marked
*pending* does not exist while this file is being staged; the phase of
`logs/assemble.sh` that writes it is named, and `EVIDENCE-INDEX.md` repeats
the same states.

**The protocol's four core files.** `HANDOFF.md` — this file.
`REVIEW_REQUEST.md` — questions only, as `Blockers` and `Optional feedback`.
`changes.patch` — pending, P1; the exact base-to-head diff. `checks.txt` —
pending, P1; every command with its exact invocation, numeric exit,
timestamps and unique log.

**The argument.** `EVIDENCE-INDEX.md` — every member and every sibling with
its state and its limits; it names itself, which the V10 index did not.
`CLAIM-CLOSURE.md` — the contract, the mechanism, the boundary not reached,
and the evidence; it replaces the V10 package's presentation-closure
document. `PROVENANCE.md` — where the batteries ran, how provenance is read
per command, and what was discarded. `LIMITATIONS.md` — the twelve above, in
full. `UNRESOLVED-BLOCKERS.md` — every open finding with its owner.
`PRIVACY-AUDIT.md` — the sanitization method and which claims become true
only at the seal.

**The derived record.** `claims.json` and `DERIVED-CLAIMS.md` — pending, P4;
every figure, derived once from the frozen inventory. `MANIFEST.sha256` —
pending, P6; the authoritative member list and content proof. `commits.txt`
and `changed-files.txt` — pending, P1; the ancestry and the changed-file
inventory.

**`screenshots/`** — present: 31 images plus two records. Sixteen
adversarial images form the eight before/after pairs described in §8.6, at
1440x900 and 393x852. Fifteen real-corpus images cover the changed route at
desktop, laptop, tablet, handset and narrow widths and under forced colors,
reduced motion, 400% page scale and 200% text, plus the Home, Reader, Source
Library and Publications shells as untouched-shell evidence.
`screenshots/INDEX.md` is the capture lane's own record and
`screenshots/capture-metadata.json` carries the per-image browser, viewport,
emulation, checkout and the DOM text read back before each shutter.

**`logs/`** — present. Both battery ordering ledgers
(`logs/order-head.txt`, `logs/order-parent.txt`); one log per recorded
command at each endpoint, covering the focused Catena suite, the Catena data
check, the promise ledger, full discovery, `make -k check`, the release
bindings, the site build, the browser gate, the gzip budgets, the browser
statics at the head, the request journals at both ends, and the head test
file run against the parent's production files; the two whole browser-gate
JSON reports (`logs/browser-gate-head.json`,
`logs/browser-gate-parent.json`); `logs/named-commits.json`; and the
pipeline sources that produced all of it. Written during assembly:
`logs/LOG-INDEX.md` and `logs/attempts.json` (P1),
`logs/gate-comparison.log` (P1), `logs/sealer-tests.log` (P1),
`logs/seal.log` and `logs/seal-check.log` (P2), `logs/derive-claims.log`
(P4), `logs/head-consistency.log` (P5). **Take every exact log filename
from `logs/LOG-INDEX.md`**, which is derived from the ledgers and the
directory rather than typed: a log is named `<attempt ordinal>-<slug>-<side>.log`,
the ordinal names the attempt and the slug names the step, so the two sides
carry different ordinals because they are two attempts.

**Beside the package, not inside it.** Four siblings, each named for the
package's own UTC stamp and slug — `STAMP` below stands for the timestamp
the assembly allocates, because the assembly is what fixes it:
20260816T172114Z-catena-e1-corrections-v11.zip, the transport copy;
20260816T172114Z-catena-e1-corrections-v11.zip.sha256, its digest and byte size;
20260816T172114Z-catena-e1-corrections-v11.verify-final.log, the read-only post-seal
verification, which ships beside the archive because a verification of the
final bytes cannot be among them; and
20260816T172114Z-catena-e1-corrections-v11.assemble.log, the outer assembly
invocation log, written while the package is still being built. The
append-only attempt ledger at
`build/agent-handoffs/attempt-ledger.jsonl` also lives outside the package
and spans every attempt ever made; the rows this package was built from are
copied into `logs/attempts.json`.

**Conditional classes, and why any is omitted.** `screenshots/` is present
because this correction changes browser-visible copy, so before and after
images are required; six of the eight pairs are byte-identical by design and
two differ, and print, no-JavaScript and keyboard-focus captures were not
produced, for the reasons in §8.7. `logs/` is present. A **sources record is
omitted**: this lane consumed no external source, since every input is this
repository's own review records, code, tests and durable records, so there
is no locus, date or rights question for a reviewer to evaluate.

**Discarded work.** This package does not claim that nothing was discarded.
`logs/attempts.json` is the enumerated authority, giving every attempt this
package was built from a terminal disposition and one reason; a raced
full-discovery measurement and the informal pre-battery runs are discarded
and back no figure, as `PROVENANCE.md` records.
