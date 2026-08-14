# Parent against head — what was compared, how, and what differed

Parent is `19982ab433dd25704ed60b1ac6ddb678bc3a98f9`, the exact reviewed V5
head, run in a separate checkout so no state is shared with the candidate. Head
is `4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46`.

## Everything below was freshly rerun, and here is how that is checkable

- **Every head-side measurement was taken at `4639b139f`, on a clean tree, in
  one sequential process.** That process ships as `logs/measure-all.sh`: the
  focused suite, full discovery, `make -k check`, the site build, the gate, the
  gate comparison and the short read-only checks are lines in one script, so
  each waits for the one before it rather than being coordinated by a watcher.
- **Earlier head-side rounds were discarded, not merged.** In the first,
  background waiters let `make -k check` and the gate run concurrently with
  full discovery in the same checkout; all four write under `build/`, and two
  of them at once is a measurement of neither. The later ones predated the
  fourth and fifth commits. There is exactly one head-side run of each command
  in this package.
- The parent tree did not move as the head advanced, so the parent-side **full
  discovery** and **gate** runs were not re-taken; the parent-side **focused
  suite**, **`make -k check`** and **short read-only checks** were added later,
  and **both parent replays were re-run against the head's own test file**.
  Each parent-side log records its own run at `19982ab4`.

Nothing in this document is carried forward from the V4.1 or V5 packages, and
no historical figure is used as a parent-side measurement. **One class of
evidence is not compared here**: the real-Chromium probe and the capture pairs,
which were measured at both ends by a separate lane and are compared in
`PROBE-DIFFERENCE.md` and `SCREENSHOT-METHOD.md`. Nothing in this document
depends on them.

## Full discovery

```
python3 -m unittest discover -s tools/tests
```

| | Parent `19982ab4` | Head `4639b139f` |
| --- | --- | --- |
| tests run | 1,657 | **1,774** (+117) |
| failures | 14 | **14** |
| errors | 13 | **13** |
| skips | 11 | **11** |
| exit | 1 | **1** |
| duration | 489.732s | 485.669s |
| FAIL/ERROR identity-set entries | 27 | **27** |

`logs/all-tests-parent.log`, `logs/all-tests-head.log`.

The head runs 117 more tests, so **no literal count identity is claimed and
none is available**. What is compared is the **set of fully qualified FAIL and
ERROR identities**, extracted by `logs/names.sh` and compared with `diff`,
which produces no output.

**`logs/names-parent.txt` and `logs/names-head.txt` are byte-identical, and
that is the result being reported, not evidence for it.** Two identical files
prove nothing on their own. Both source logs ship, they differ, and the
extraction script ships, so the identity can be re-derived; this lane
re-derived it, and running `logs/names.sh` over each shipped log reproduces the
corresponding shipped name file byte for byte.

The 27 identities fall in `test_public_alpha` (8), `test_tool_registry` (7),
`test_index_bible` (5), `test_day_missal_integration` (2),
`test_day_reader_integration` (2), `test_propers_reader_integration` (2) and
`test_mass_ordinary` (1). **None is a Catena test.** The two
`test_day_reader_integration` entries are the `src/web/data/` guard
contradiction — see `DATA-TEST-CONTRADICTION.md`.

## Focused Catena suite

```
python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v
```

| | Parent | Head |
| --- | --- | --- |
| tests run | 306 | **423** (+117) |
| result | OK | **OK** |
| exit | 0 | **0** |
| duration | 2.664s | 2.948s |

`logs/focused-catena-parent.log`, `logs/focused-catena-head.log`. The parent
run is over the parent's own tree and its own test file; nothing of V6 is
present in it. The `+117` is the same difference full discovery shows, which is
the check that the two measurements are of the same change.

## The V6 test file replayed against the parent

Not a parent-versus-head comparison of one command, but the check that the new
regressions fail on the code they were written to catch.

| | Result |
| --- | --- |
| unfiltered, parent tree | harness dies: `TypeError: Cannot read properties of null (reading 'canon')`; **62** `setUpClass` errors; only 31 tests report at all; exit 1 |
| filtered, parent tree | **Ran 371, 71 failures, 14 errors**, exit 1 |

`logs/v6-tests-against-parent.log`,
`logs/v6-tests-against-parent-filtered.log`, filter
`logs/parent-run-filter.patch`.

Both runs are over the parent's production files with only
`tools/tests/test_catena_wave_1.py` replaced; the unfiltered log records the
SHA-256 of both production files at that tree and both match the parent blobs.
The filter drops exactly three scenarios — `null-index`, `null-index-cold`,
`list-index` — and ships as a literal diff.

**The test file replayed in both runs is the one at the head**, `4639b139f`:
both were re-run after the fourth and fifth commits, each log's TREE line names
the head the file came from, and `logs/parent-run-filter.patch` was regenerated
against it. The unfiltered run reproduces exactly — `Ran 31`, 62 `setUpClass`
errors, the same `TypeError` — and the filtered one at 371 / 71 / 14, 85
identities over 24 classes.

The filtered run's 85 FAIL/ERROR identities fall across 24 distinct classes:

| | |
| --- | --- |
| 19 | of the 23 classes V6 adds |
| 4 | pre-existing classes that hold corrected oracles **and** fail here: `MalformedRecordRenderingTest`, `MalformedLanguageAttributeTest`, `MixedCollectionMemberTest`, `UntypedProvenanceTest` |
| 1 | `FrozenContractTest`, whose `MODEL_SHA256` pin fails at the parent by construction because the model differs; it holds no corrected oracle |

Two neighbouring sets do not coincide with that decomposition and are not
folded into it. Corrected oracles live in **five** pre-existing classes — the
four above and `NumericVerseAndPathTest`, which does **not** fail at the
parent. And four of the classes V6 adds do not fail either —
`AbsenceRowIdentityTest`, `CountedWordTallyTest`, `RenderedScriptureTruthTest`,
`UnregressedScriptureTest` — being the real-corpus positive control and three
oracles reading production sinks for behaviour V5 had already made correct. A
regression defending an earlier fix with a better instrument does not prove
this one, and neither set is counted as though it did.

## Browser gate

```
TRIPTYCH_CHROME=<chromium binary> node tools/tests/corpus_browser_gate.mjs --json-out <out>
python3 logs/compare-gate.py logs/gate-parent.json logs/gate-head.json
```

| | Parent | Head |
| --- | --- | --- |
| assertions | 2,290 | **2,290** |
| passed | 1,836 | **1,836** |
| failed | 226 | **226** |
| skipped | 228 | **228** |
| routes × states × pages | 19 × 9 × 171 | 19 × 9 × 171 |
| exit | 1 | **1** |

`compare-gate.py` reports `summary equal: True`, 17 assertion objects on each
side, an equal identity set, no side-only identities, 0 rows with a changed
status, 0 rows with a changed detail, and

```
whole report identical (volatile fields excluded): True
```

**Read that line precisely. The comparison excludes FOUR volatile fields, not
one: `generatedAt`, `root`, `durationMs` and `browser`.** The V4.1 record's
wording named only `generatedAt`; this is the corrected statement. Every
non-volatile key of the whole report — including all 226 failure objects with
their exact `detail` strings — is deep-equal across the two runs, with those
four excluded. The tool's own docstring names all four.

The 226 failures are the shared shell's: `single-main-element` (117),
`primary-controls-meet-target-size` (82), `skip-link-targets-existing-element`
(27). None is a Catena assertion and none moved. See `UNRESOLVED-BLOCKERS.md`
§3.

## Budgets — gzip -9, whole file, mtime pinned to zero

Measured at both ends: `logs/misc-checks-head.log` §D,
`logs/misc-checks-parent.log` §D.

| File | Measure | Parent | Head | Ceiling |
| --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | whole | 7,629 | **7,629** | 8,000 |
| `src/web/browser/catena/catena.css` | stripped | 2,676 | **2,676** | 2,700 |
| `src/web/browser/catena/catena.js` | whole | 12,990 | **12,993** (+3) | 13,000 |
| `src/web/browser/catena/catena.js` | stripped | 8,363 | **8,202** (−161) | 8,800 |
| `src/web/browser/catena/catena-model.js` | whole | 11,171 | **15,767** (+4,596) | **none** |
| `src/web/browser/catena/catena-model.js` | stripped | 3,284 | **4,377** (+1,093) | **none** |

`catena.css` is byte-identical to the parent, not merely equal in size. The
four ceiling constants are unchanged from the parent; **no ceiling was raised
and no budget authority was changed.** `catena-model.js` carries no size
ceiling — only the `MODEL_SHA256` digest pin, re-pinned deliberately, at the
head to `adb61eb7…`.

This lane also re-derived all twelve figures independently from the git blobs
at `19982ab4` and `4639b139f`, using the algorithm of `gz()` and
`without_comments()` in `tools/tests/test_catena_wave_1.py`, and reproduced
every one (`checks.txt` P).

### The relocation, disclosed

`catena.js` finished this correction 7 gzipped bytes under its ceiling, and
`catena-model.js` grew by 4,596 whole bytes. Of that growth, 1,093 bytes are
composition and **3,503 bytes are explanatory comment**, which the model
carries deliberately because it carries no ceiling.

| | Parent | Head | Δ |
| --- | --- | --- | --- |
| the two files concatenated and gzipped as one stream | 23,449 | **28,028** | **+4,579** |
| the two files gzipped separately and the sizes summed | 24,161 | **28,760** | **+4,599** |

They are different measures and different numbers, and both are recorded so
that neither can be quoted as the other (`logs/misc-checks-head.log` §E).

**Formal compliance is real and is not the same statement as unchanged
practical load.** A reader of the route fetches both files.

## Promise ledger

| | Parent | Head |
| --- | --- | --- |
| tracked | 30 | **31** |
| complete | 19 | **19** |
| result | valid, exit 0 | **valid, exit 0** |

`logs/misc-checks-parent.log` §A, `logs/misc-checks-head.log` §A. **Measured at
both ends**, which is the direct answer to the V5 provenance defect: V5
attributed a 30-entry ledger output to a commit that could not have produced
it.

The added entry is `corpus-browser-catena-e1-corrections-v6-2026-08-14`,
`in_progress`, with three of its ten requirements `open`. **Nothing was marked
complete by this lane.**

## Catena generator check

```
python3 scripts/_catena.py check
```

`catena valid: fragments=1351 books=1 canon=73`, exit 0, at **both** ends
(`logs/misc-checks-parent.log` §B, `logs/misc-checks-head.log` §B). This
matters more than usual here: `catena-model.js` is executed under node by the
generator during emit, and the membership and identity rules this correction
tightened are the ones the generator calls. The same three numbers come out at
both ends.

## Release bindings

Four stale at **both** ends, exit 1, the same four Catena paths, all four
listed in full at each end (`logs/misc-checks-parent.log` §C,
`logs/misc-checks-head.log` §C). What V6 changed is two of the four *actual*
digests — `catena-model.js` from `f1ed1379…` to `adb61eb7…`, `catena.js` from
`8bb2834a…` to `3dc290ef…` — not the count. `catena.css` and `index.html` are
byte-identical at both ends and were already stale at the parent. **None was
re-signed**; `refresh-release-bindings` and `approve-release` were not run.

## The production sources are text

```
file src/web/browser/catena/catena.js src/web/browser/catena/catena-model.js
```

`JavaScript source, Unicode text, UTF-8 text` for both files at **both** ends
(`logs/misc-checks-parent.log` §E, `logs/misc-checks-head.log` §G).

This comparison exists because it once failed in between. A raw NUL byte
written as a separator in the model's `absenceRows` sort key made
`catena-model.js` — and the shipped patch — binary to `grep`, `diff` and a
pager from the first commit of this correction to the third; the fourth commit
replaced it with its escape. The parent is text and the head is text. See
`TYPED-PRESENTATION-BOUNDARY.md`.

## `make -k check`

| | Parent | Head |
| --- | --- | --- |
| exit | 2 | **2** |
| failing targets | `check-release-bindings` (Makefile:598), `check-tool-registry` (803), `check-examples` (791) | **the same three, at the same three lines** |

`logs/make-k-check-parent.log`, `logs/make-k-check-head.log`. The head-side run
was taken at `4639b139f` after the full suite finished, not beside it; the
parent-side run was taken on the parent's own clean tree.

The three failures are inherited, and now measured rather than asserted: each
target is owned elsewhere and recorded with its owner in
`UNRESOLVED-BLOCKERS.md`, the release-binding target's failure is measured at
both ends above, and `check-tool-registry` and `check-examples` are untouched
by a correction that adds no file to `tools/` and changes no captured
transcript. **No record here rounds those into a green repository-wide check.**

## Byte-identity of the untouched paths

```
git diff --stat 19982ab4..HEAD -- src/web/data src/web/browser/catena/catena.css src/web/browser/catena/index.html
```

No output, at `4639b139f` (`logs/misc-checks-head.log` §F) and as re-run by
this lane. `src/web/data/`, `catena.css` and `index.html` are byte-identical to
the parent.
