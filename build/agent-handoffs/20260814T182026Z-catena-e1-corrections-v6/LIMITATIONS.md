# Limitations — what this package does not prove

The V5 package listed nine limitations and not one of them named the three
defects its independent review then found in the evidence: five before/after
capture pairs that were byte-identical while four documents described each as
showing a visible change, a focus claim made in three records by an instrument
that never read `document.activeElement`, and a parent crash narrated in two
documents and preserved in none. A limitations record that omits the evidence's
own faults is not a limitations record. §§1–4 below are those three faults and
their corrections, stated first because they are the reason this package exists.

### 1. The fixtures are fabricated, and every artifact says so in itself

The probe serves a **fixture site root**: it injects malformed JSON in the
response path of its own static server, over a real built site. Those fixtures
are adversarial test data. **They represent no holding of this project, no
corpus record, and no real state of the published site.** The built site is
never modified; the injection is in the response path, so
`build/public-alpha/site` on disk is byte-identical before and after a run.

V5 disclosed this in prose only, and its review found that every machine
artifact — both probe JSONs, both screenshot indexes, every PNG — read on its
own as a record of real corpus behaviour. In V6 the disclosure is IN the
artifacts: every probe JSON root and every per-state record carries
`"fabricated": true` and the banner
`ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA`, and every fixture V6 added to
`tools/tests/test_catena_wave_1.py` carries the same banner inertly at its root
(ten of them, built through one `_fixture()` helper), so anything captured from
one denies its own authenticity without depending on prose beside it.

**Precisely**: the ten V6 fixtures are stamped in the data. The fixtures
inherited from V3/V4/V4.1/V5 are not — they carry the `EXPLICITLY SYNTHETIC`
comment block each was written with, which is adjacent metadata rather than a
property of the value. Stamping them too would have meant a fourth commit and a
re-measurement of every number in this package after the head was already
sealed, so it is recorded here as a known gap rather than done quietly or
claimed as done. Real-corpus evidence is labelled `"fabricated": false` and is
never mixed under the fabricated banner.

### 2. Screenshots are audited by digest, and byte-identical pairs are named as such

Every before/after pair in this package was hashed by `logs/pair-audit.py`,
which exits non-zero if any claimed pair is byte-identical. Each pair is
classified as **byte-identical (no visual difference)**, **byte-different but
visually equivalent**, or **meaningfully different, with the changed region
named**. Where a correction is invisible in a raster — a `lang` attribute, a
URL that was or was not requested, `aria-busy`, the focused element — no
screenshot is offered at all, because a picture cannot bear on the claim and
offering one would be offering evidence that cannot support it.

**Result for this package**: 16 pairs audited, **none byte-identical, none
visually equivalent, all 16 genuinely different**, exit 0. One capture was
produced, audited, found byte-identical and **deleted** — `bible-language-forms`
at 393x852, where the page folds its controls disclosure shut so the element
carrying the finding is not rendered at all. Three others were byte-identical
framed to the viewport and were **re-framed rather than deleted**, because the
absence disclosure they evidence sits below the fold. `SCREENSHOT-METHOD.md`
records both decisions.

**Much of this correction is still not visible in a raster.** Three states carry
no picture at all — a requested URL, `aria-busy`, focus and a `lang` attribute
are not in an image — and for those the evidence is `logs/probe-parent.json`
read against `logs/probe-head.json`.

### 3. Focus is measured, and only what was measured is claimed

V5's records said its probe "reads `aria-busy`, the status region's text and
the focused element"; `grep -i focus` over that tool and both its outputs
returned nothing. The V6 probe reads `document.activeElement` and records the
focused element's id, tag and whether it lies inside `#reading`, for every
state, and again after a genuinely late completion.

**This remains rendering and DOM evidence, not announcement evidence.** No AT
bus or screen reader was available. Nothing here proves what a screen reader
says. The real-device-or-AT prerequisite remains open with its owner and is not
superseded by anything in this package.

**One class shows no difference between the two heads, and it is recorded as a
true negative.** Genuinely late stale work behaves identically at the parent and
at this head: the V5 review's finding there was about the PROOF — its "nothing
stale" case released the payload before navigating, so no late work existed —
and V6 supplies the proof without needing to change the behaviour. The probe is
also blunt in that state and says so. `PROBE-DIFFERENCE.md` sets out both
points. Nothing in this package claims a repair that was not made.

Focus is claimed in three distinct kinds, and they are not interchangeable:
focus TARGET (a rebuild moves focus somewhere named), focus RECOVERY (a rebuild
that swallows the focused node hands focus to the reading region), and
NO-FOCUS-MOVEMENT (nothing moved it; the reader's focus stayed theirs). Most
V6 states are the third kind and are labelled as such rather than dressed as
recovery.

### 4. Both parent runs are preserved, including the one that crashes

Replaying the V6 test file against the uncorrected parent with **no filter**
raises `TypeError: Cannot read properties of null (reading 'canon')` out of
`catena.js:981` — the JSON-null bootstrap this correction fixes — which escapes
the node process and errors every `ReplayTest` class in `setUpClass`. That run
ships whole as `logs/v6-tests-against-parent.log`. The filter needed to get a
per-class reading drops exactly three scenarios and ships as
`logs/parent-run-filter.patch`, a literal diff, not a description of one.

### 5. Every check records the head it ran at

V5 claimed all measurements were taken at one commit, and its 30-entry promise
ledger output could only have come from a later one. `checks.txt` here carries a
per-check SHA column. Where a number depends on which commit is checked out —
the ledger count above all — it is attributed to that commit and to no other.

### 6. The name-set comparison is a derived identity, not independent evidence

`logs/names-parent.txt` and `logs/names-head.txt` are byte-identical, which is
the result being reported and not a proof of it. Both source logs ship, they
differ, and the extraction script ships with them, so the identity can be
re-derived rather than taken on trust. The head runs 117 more tests than the
parent, so **no literal count identity is claimed**; what is compared is the set
of fully qualified FAIL/ERROR identities.

### 7. The browser-gate identity claim excludes four fields, not one

`logs/compare-gate.py` reports the whole report deep-equal, excluding
`generatedAt`, `root`, `durationMs` and `browser`. The V4.1 record named only
the first. The correct statement is: **every non-volatile key of the report is
deep-equal across both runs, with those four excluded.**

### 8. The package digest is a transport digest

The ZIP digest sidecar proves the archive received is the archive sent. It does
**not** prove reproducible construction: ZIP entry timestamps are local mtimes.
`MANIFEST.sha256` is the content proof and survives repacking, and
`logs/sanitize-and-seal.py --verify` re-checks both.

### 9. The sealer is hardened and tested, and one class remains unsolvable by pattern

`logs/sanitize-and-seal.py` gains a verify mode, a screenshot-pair audit, a
stale-manifest fix, a completed timezone table, and repaired false positives on
ordinary screenshot coordinates and version triples; `logs/test-sanitize-and-seal.py`
is 45 focused tests over exactly those behaviours and is itself a sealable
package member. One class is still not solvable by pattern: an absolute path
outside `$HOME`, the repository root and the scratch directory is
unrecognisable as private. It is handled by policy — this package contains no
such path — not by the tool. A second, inherent: the account-name and hostname
checks match the operator's runtime identity on word boundaries, so a reviewer
whose account name is an ordinary English word may see a false hit; the
documented answer is to set `SANITIZE_USER`/`SANITIZE_HOST`.

### 10. No print or forced-colors evidence is added

V4.1's accepted 53-image matrix covers print and forced-colors emulation for the
real corpus states, and V6 changed no CSS — `src/web/browser/catena/catena.css` is byte-identical.
Nothing in this correction bears on those media, so no successor capture was
made. The V4.1 matrix is neither superseded nor re-issued here.

### 11. What this correction does not settle, and did not touch

- Four stale Catena release bindings, including the new `src/web/browser/catena/catena-model.js`
  digest. Correctly fail-closed; none re-signed. The release owner's.
- The `src/web/data/` test contradiction, preserved untouched, and the two
  Day-reader guard failures it causes — which fail identically at the parent.
  The Day-reader owner's.
- The common-gate failure population: 226 failing assertions, deep-equal at both
  ends. The shared shell's.
- `check-tool-registry` and `check-examples`. Their own owners'.

None was worked around, whitelisted, weakened or expect-marked. Each is recorded
with its owner in `UNRESOLVED-BLOCKERS.md`.

### 12. This lane does not review its own work

Nothing here is an acceptance. The disposition on this head is owed by a fresh
independent review, and no measurement in this package is offered as a substitute
for one.
