# Evidence index

Every path below resolves inside this package. Each entry says what the
artifact is, which corrected class it bears on, what it proves, and **what it
does not prove**. The classes are numbered as in `HANDOFF.md` §7:

1. collection members validated per collection before counting, rendering,
   refusal or absence
2. root and identity joins typed
3. unsupported claims omitted, never guessed
4. findings read as a set; self-contradiction declined; `partial` licensed only
   by `partial-public-domain`
5. canonical verse identity
6. unsafe textual identities unroutable
7. null or unreadable bootstrap terminal, and the canon checked before the
   address is judged
8. lossy oracles replaced

**Fabricated or real?** Every artifact produced by replaying
`tools/tests/test_catena_wave_1.py`, and every captured page and every probed
state but one, is **fabricated-fixture evidence**: the scenarios are
adversarial data written to exercise these classes, and they represent no
holding of this project and no real state of the published site. Artifacts
marked **real-corpus** were measured against the tracked corpus. The two are
never mixed inside one artifact without being labelled inside it: the probe
reports carry `fabricated` per state, and every PNG carries the banner in its
own metadata.

**Where the measurement was taken.** Every head-side log carries `SHA:
4639b139f…`; every parent-side log carries `SHA: 19982ab4…`. The head-side set
was produced in one sequential process, `logs/measure-all.sh`. Earlier
head-side rounds were discarded rather than merged — one contaminated by
concurrent jobs in the same checkout, the later ones predating the fourth and
fifth commits — and `checks.txt` says so in its header.

## Records

| File | What it establishes | What it does not |
| --- | --- | --- |
| `HANDOFF.md` | the task, the branch, the ancestry, which of the four commits touch production, the focused files, the startup commands, the inventory, and what is deliberately absent | it is not a review, and records no disposition |
| `checks.txt` | every command, its exact invocation, its numeric exit, its log, **and the commit it ran at**; what was skipped; what was discarded and why | it does not attribute any number to a commit that could not have produced it, and it records no probe or capture result |
| `BASELINE-COMPARISON.md` | parent against head, suite by suite, with the four gate exclusions named and every comparison measured at both ends | it claims no comparison this package did not run, and it vouches for nothing the capture lane produced |
| `TYPED-PRESENTATION-BOUNDARY.md` | what each grammar and predicate admits and refuses, why each is drawn where it is, and the real-corpus sweep showing nothing tracked is refused | it does not prove any behaviour of the running page; the sweep is over data, not over renders |
| `CORRECTED-ORACLES.md` | class 8 — every oracle this correction changed, with the reason each is recorded under and its line in `tools/tests/test_catena_wave_1.py` | it is a record of what the oracles now assert, not a run of them; the runs are the two parent replays below |
| `LIMITATIONS.md` | twelve things this package does not prove, opening with the four evidence faults the V5 review found | — |
| `REVIEW_REQUEST.md` | six blocking questions, one about a defect the review did not name, three optional | none of them is answered here |
| `UNRESOLVED-BLOCKERS.md` | seven open items, each with its owner, none repaired here | — |
| `DATA-TEST-CONTRADICTION.md` | that no `src/web/data/` path changed and the guard was not weakened, whitelisted, expect-marked or rebased | it does not resolve the contradiction, which is two other owners' records |
| `PRIVACY-AUDIT.md` | the sanitization method, its result, and the sealer's own audited gaps | it bears on no corrected class |
| `commits.txt` | the ancestry, and which commits touch production | — |
| `changed-files.txt` | `git diff --name-status` and `--stat` against the parent, bare | — |
| `changes.patch` | the exact parent→head diff, regenerated at the sealed head: 228,083 bytes, NUL-free, reproducing `git diff 19982ab4..4639b139f` byte for byte | the NUL byte that made the earlier V6 patch binary to `grep` and `diff` is gone with the model's; `checks.txt` V records the verification |

## Logs — the test suites

| File | Class | What it proves | What it does not |
| --- | --- | --- | --- |
| `logs/focused-catena-head.log` | all | the focused Catena suite at the head: 423 tests, OK, exit 0, verbose | a green suite is not a review, and every scenario in it is fabricated |
| `logs/focused-catena-parent.log` | all | the same command at the parent's own tree and own test file: 306 tests, OK, exit 0 | — |
| `logs/all-tests-head.log` | all | full discovery at the head: 1,774 tests, 14 failures, 13 errors, 11 skips, exit 1, on a clean tree with no other job in the checkout | it does not show any Catena failure, because there is none; the 27 failing identities are other owners' |
| `logs/all-tests-parent.log` | all | the same command at the parent: 1,657 / 14 / 13 / 11, exit 1 | — |
| `logs/names-parent.txt`, `logs/names-head.txt` | all | the two sorted 27-entry FAIL/ERROR identity sets, byte-identical | **the identity is the result, not the evidence.** Two identical files prove nothing alone; the two differing source logs and the extraction script ship so it can be re-derived |
| `logs/names.sh` | all | the extraction both files were derived by; re-running it over each shipped log reproduces the shipped name file byte for byte | — |
| `logs/v6-tests-against-parent.log` | 1–8, **fabricated** | that the correction's own regressions cannot even run against the uncorrected parent: `TypeError: Cannot read properties of null (reading 'canon')`, 62 `setUpClass` errors, only 31 tests reporting at all, exit 1; it records the SHA-256 of both production files at that tree, and both match the parent blobs | it gives no per-class reading — the process dies. The line the harness reports, 981, is line 979 of the file at the parent; the difference is the replay wrapper. the test file it ran is the head's, and the log's TREE line names the head it came from |
| `logs/v6-tests-against-parent-filtered.log` | 1–8, **fabricated** | the per-class reading: Ran 371, 71 failures, 14 errors, exit 1; 85 FAIL/ERROR identities across 24 distinct classes | four V6 classes do **not** fail here, and one that does — `FrozenContractTest` — fails on the `MODEL_SHA256` pin rather than on behaviour. The decomposition is in `BASELINE-COMPARISON.md` |
| `logs/parent-run-filter.patch` | 1–8 | the exact filter that made the run above possible, as a literal diff: three scenarios dropped, named in the patch | it is not a description of a filter; V5 narrated one and preserved none |

## Logs — the browser gate

| File | Class | What it proves | What it does not |
| --- | --- | --- | --- |
| `logs/gate-head.json`, `logs/gate-parent.json` | none directly; **real-corpus** | the two whole gate reports over real built sites: 2,290 assertions, 1,836 pass, 226 fail, 228 skip at each end | the gate visits real corpus addresses only, which cannot exhibit malformed-data behaviour, so it bears on no corrected class. Exit 1 at both ends is the inherited common-gate failure population |
| `logs/gate-head.log`, `logs/gate-parent.log` | — | the two invocations, their exits and their counts, each with the commit it ran at | the head-side log names the chromium binary by absolute path; `checks.txt` J records the same command with that one value elided, because no absolute path may appear in a document of this package |
| `logs/gate-comparison.log` | — | `summary equal`, equal identity sets, 0 changed statuses, 0 changed details, whole report deep-equal, exit 0, parent and head SHAs both in its header | **the deep-equality excludes four volatile fields — `generatedAt`, `root`, `durationMs`, `browser` — not one** |
| `logs/compare-gate.py` | — | the comparison itself, re-runnable by a reviewer; its docstring and its `VOLATILE` set both name all four excluded fields | — |
| `logs/public-site-head.log`, `logs/public-site-parent.log` | — | that each gate ran against a site built from the tree it is attributed to, exit 0 at both | `make public-site` writes `build/public-alpha/site` and verifies nothing |

## Logs — the repository-wide and short checks

| File | Class | What it proves | What it does not |
| --- | --- | --- | --- |
| `logs/measure-all.sh` | — | that the head-side set is one sequential process, not a set of jobs that may have overlapped | it does not cover the parent side or the capture lane |
| `logs/misc.sh` | — | the exact code behind the short checks, including the budget measurement | — |
| `logs/make-k-check-head.log`, `logs/make-k-check-parent.log` | — | exit 2 at **both** ends, failing at the same three targets and the same three Makefile lines; the head-side run was taken after the full suite finished rather than beside it | it does not show any of the three being repaired here — each is owned elsewhere. Nothing here rounds them into a green repository-wide check |
| `logs/misc-checks-head.log` §A, `logs/misc-checks-parent.log` §A | — | the promise ledger valid at both ends: 31 tracked at the head, 30 at the parent, 19 complete at each, exit 0 | it does not mark anything complete |
| §B at both ends | 1, 5, **real-corpus** | `catena valid: fragments=1351 books=1 canon=73`, exit 0 at both ends — the tightened membership and identity rules did not move the emitted chapter view, since the generator executes this model during emit | it exercises the generator's solved cases, not the page |
| §C at both ends | — | four stale release bindings at both ends, exit 1, all four listed; none re-signed | it is not a comparison of *counts only*: two of the four actual digests changed, and the entry says which |
| §D at both ends, and §E at the head | — | the twelve budget figures and the relocation in both measures — concatenated-and-gzipped, and gzipped-separately-then-summed | the head log's §D echoes a description rather than an invocation; `logs/misc.sh` §D carries the code, and this lane re-derived every figure from the git blobs (`checks.txt` P) |
| `logs/misc-checks-head.log` §F | — | `src/web/data/`, `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` byte-identical to the parent | — |
| `logs/misc-checks-head.log` §G, `logs/misc-checks-parent.log` §E | — | `file` reports both production sources as UTF-8 text at **both** ends | it does not show the three commits in between, when the model was binary to `grep` and `diff`; `TYPED-PRESENTATION-BOUNDARY.md` records that, and `checks.txt` S is the check |

## Tools shipped as evidence

Lane-local, following the precedent V4 set. `REVIEW_REQUEST.md` §8 asks whether
they belong in `tools/` instead.

| File | What it is |
| --- | --- |
| `logs/sanitize-and-seal.py` | the sealer: normalize → scan → index-check → pair audit → manifest, refusing to write a manifest on any hit |
| `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | 46 tests over the sealer's own behaviours, exit 0, and itself a sealable package member. The 46th pins a fix made during assembly: the index check counted `MANIFEST.sha256` as missing, because the tool writes the manifest after the check runs. It tests the instrument, not this package's content |
| `logs/compare-gate.py` | the gate deep-equal, excluding four volatile fields |
| `logs/names.sh` | the FAIL/ERROR identity extraction |
| `logs/measure-all.sh`, `logs/misc.sh` | the measurement run itself, shipped so the order and the isolation are checkable rather than asserted |
| `logs/v5-package-verify.log` | the V5 package digest claimed, measured and recorded in its sidecar, all three equal. It proves the sealed V5 package was not mutated; it proves nothing about V6 |

## Real-corpus evidence in this package

Only these bear on the real corpus. Everything else that exercises a corrected
class is fabricated.

- `logs/misc-checks-head.log` §B and `logs/misc-checks-parent.log` §B — `catena
  check` over the tracked commentary, at both ends.
- `logs/gate-head.json`, `logs/gate-parent.json` — real built sites, real
  addresses, no malformed-data state reachable.
- The grammar sweep recorded in `TYPED-PRESENTATION-BOUNDARY.md` and
  `checks.txt` Y: 1,351 fragment ids, 12 work ids, 73 canon tokens and paths, 7
  edition ids, 112 refusal rows, 16,710 paragraph break marks and 252,288 verse
  keys, none refused. It has **no log file**; it is a read-only walk of
  `src/web/data/` and `src/sources/bibles/` reproducible at the head.
- `logs/probe-head.json` and `logs/probe-parent.json`, the `late-stale-work`
  state only — the one probed state driven by the real corpus, `fabricated:
  false`, and the one that shows no difference between the two heads.
- Within the fabricated suites, four V6 test classes are not malformed-data
  regressions at all: `AbsenceRowIdentityTest` is the real-corpus positive
  control, and `CountedWordTallyTest`, `RenderedScriptureTruthTest` and
  `UnregressedScriptureTest` read production sinks for behaviour V5 had already
  made correct. They pass at the parent, and `BASELINE-COMPARISON.md` keeps
  them out of the regression count.

## Fabricated-fixture evidence, and how it says so

Every scenario replayed by `tools/tests/test_catena_wave_1.py` is adversarial
test data. `LIMITATIONS.md` §1 is the statement of record, and it is true as
written: **all ten V6 fixture roots**, and the roots the two V6 fixture
factories build, pass through `_fixture()` and carry `_adversarial:
"ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"`. The fourth commit stamped
the last one, `V6_TESTAMENT_INDEX`. The fixture roots inherited from earlier
waves carry no such key, so a reviewer grepping the banner should expect the V6
roots and not one per fixture in the file.

No artifact in this package is a rendering of a real corpus address under a
malformed value, because no real corpus value is malformed. That is what the
sweep above shows, and it is also why most of this correction cannot be
photographed.

## The real-Chromium probe

Produced by a separate lane; `PROBE-DIFFERENCE.md` is its record and
`SCREENSHOT-METHOD.md` describes the instrument. Indexed here against the
classes it bears on.

| File | Class | What it proves | What it does not |
| --- | --- | --- | --- |
| `logs/probe-catena.mjs` | 1–7 | the instrument: it serves a built site, injects the fixtures **in the response path** so the built artifact on disk is never modified, drives headless Chromium over the DevTools Protocol, reads the live DOM and the resource log, records `document.activeElement`, and captures PNGs | it is a tool, not a measurement; and injection in the response path means the site it serves is not the site that would be published |
| `logs/probe-head.json` | 1–7, **mixed** | eleven states read at the head, ten fabricated and one real-corpus, each labelled in the file; the root carries `fabricated: true` and a `represents` banner | **it is rendering and DOM evidence, not announcement evidence.** No AT bus or screen reader was available, and nothing in it proves what a screen reader says |
| `logs/probe-parent.json` | 1–7, **mixed** | the same eleven states, same fixtures, same browser, at the parent — so every row of `PROBE-DIFFERENCE.md` is measured at both ends rather than inferred from the code | — |
| `logs/probe-head.stdout.txt`, `logs/probe-parent.stdout.txt` | — | each run's console output verbatim: 11 states, 10 fabricated and 1 real-corpus, 8 states captured as 15 PNGs, and the three states not captured named with their reason | — |
| `logs/fixtures-source.json` | 1–7 | the fixtures the probe used, extracted mechanically from `tools/tests/test_catena_wave_1.py`, so a reviewer can check that the pictures and the regressions are of the same data | it is the extraction, not a proof of the extraction; the check is to read it against the test file |

What the two reports establish, class by class, is in `PROBE-DIFFERENCE.md`:
the edition options and the `lang` sinks (classes 2 and 3), the testament line
(3), the tally and the blank rows and the refusal sentence (1), the two finding
orders reading the same (4), the single licensed partial line (4), the verse
numbers (5), the URLs never requested (6), and the terminal bootstrap state
(7).

**One state is real-corpus and shows no difference between the two heads.**
`late-stale-work` carries `fabricated: false`, was captured at neither end, and
is recorded as a true negative: the V5 review's finding about that class was
about the proof, not the behaviour, and the suite — not the probe — is where V6
answers it. That it is stated rather than dropped is itself part of the
evidence.

## The pair audit

| File | What it proves | What it does not |
| --- | --- | --- |
| `logs/pair-audit.py` | the classifier: each `before--`/`after--` pair is **(a)** byte-identical, **(b)** byte-different but within tolerance in every channel, or **(c)** genuinely differing, with the pixel count and the **bounding box** of the change. (a) and (b) exit non-zero, and the sealer runs it as a hard gate | it classifies difference; it does not judge whether the difference is the right one |
| `logs/pair-audit.txt`, `logs/pair-audit.json` | the result for this package: **16 pairs audited, 0 byte-identical, 0 visually equivalent, 16 differing, 0 unpaired**, with both digests and the changed region for each | a bounding box constrains a description; it does not supply one |

This is the direct answer to the V5 review's finding that five of ten claimed
pairs were byte-identical while four documents described each as showing a
visible change.

## Screenshots

`screenshots/` holds **30 PNGs in 15 pairs**, plus
`screenshots/before--probe-index.json` and
`screenshots/after--probe-index.json`. **Every image is a page under fabricated
adversarial data**; none shows a holding of this project or a real state of the
published site.

| State captured | Viewports | Class |
| --- | --- | --- |
| `bible-language-forms` | 1440x900 | 2, 3 |
| `malformed-testament` | 1440x900, 393x852 | 3 |
| `mixed-collection-members` | 1440x900, 393x852 | 1 |
| `finding-order`, `finding-order-reversed` | 1440x900, 393x852 each | 4 |
| `stray-partial` | 1440x900, 393x852 | 4 |
| `padded-verse-keys` | 1440x900, 393x852 | 5 |
| `null-bootstrap` | 1440x900, 393x852 | 7 |

**Three states were deliberately not captured**, and the omission is part of
the record rather than a gap in it: `unsafe-textual-identity` (the finding is
which URL was requested), `late-stale-work` (the finding is `hash`,
`aria-busy`, focus and the tally after a late completion), and
`bible-language-forms-voice` (additional `lang` attributes on a state already
captured). A fourth capture, `bible-language-forms` at 393x852, was produced,
audited byte-identical, diagnosed — at that width the controls disclosure is
folded shut on load, so the element carrying the finding is not rendered — and
removed rather than shipped as a picture that frames none of its claim.
`SCREENSHOT-METHOD.md` records all four decisions.

Three states — `finding-order`, `finding-order-reversed` and `stray-partial` —
are captured **beyond** the viewport their filename names, because the absence
disclosure they turn on sits below the fold and a frame cut to the viewport was
byte-identical. The pixel totals in the table below show it: those frames are
several times the area of a 393x852 or 1440x900 screen.

Each PNG carries an `iTXt` `Comment` chunk reading `ADVERSARIAL TEST FIXTURE —
NOT REAL CORPUS DATA | state=<name> | fabricated=true`, so an image detached
from this package still denies its own authenticity. The banner is metadata
rather than paint, because burning it into the pixels would alter the rendering
the picture is evidence of. Both index files carry the same banner at their
root and on every entry, with each file's `sha256`, `bytes` and `frame`, and
neither asserts a difference on its own authority: every entry records
`differenceEstablishedBy: "pair-audit.py over a before--/after-- pair"`.

Every pair, with the verdict the audit returned for it. Reading a row: the
audit establishes that the two frames differ and where; what the difference
means is the claim of `PROBE-DIFFERENCE.md` and `SCREENSHOT-METHOD.md`, not of
the audit and not of this table.

| Pair | Class | Audited verdict, from `logs/pair-audit.txt` |
| --- | --- | --- |
| `screenshots/before--catena--bible-language-forms--1440x900.png` / `screenshots/after--catena--bible-language-forms--1440x900.png` | 2, 3 | pixels differ, 689 of 1,296,000, changed region x 981..1097, y 399..413 |
| `screenshots/before--catena--finding-order--1440x900.png` / `screenshots/after--catena--finding-order--1440x900.png` | 4 | pixels differ, 4,872 of 5,123,520, changed region x 780..1120, y 1110..1205 |
| `screenshots/before--catena--finding-order--393x852.png` / `screenshots/after--catena--finding-order--393x852.png` | 4 | pixels differ, 7,019 of 1,870,287, changed region x 33..348, y 3699..3820 |
| `screenshots/before--catena--finding-order-reversed--1440x900.png` / `screenshots/after--catena--finding-order-reversed--1440x900.png` | 4 | pixels differ, 30,392 of 5,123,520, changed region x 754..1120, y 686..1306 |
| `screenshots/before--catena--finding-order-reversed--393x852.png` / `screenshots/after--catena--finding-order-reversed--393x852.png` | 4 | pixels differ; the two frames are different heights, so no single box is quoted |
| `screenshots/before--catena--malformed-testament--1440x900.png` / `screenshots/after--catena--malformed-testament--1440x900.png` | 3 | pixels differ, 507 of 1,296,000, changed region x 394..510, y 228..235 |
| `screenshots/before--catena--malformed-testament--393x852.png` / `screenshots/after--catena--malformed-testament--393x852.png` | 3 | pixels differ, 410 of 334,836, changed region x 108..210, y 221..227 |
| `screenshots/before--catena--mixed-collection-members--1440x900.png` / `screenshots/after--catena--mixed-collection-members--1440x900.png` | 1 | pixels differ, 14,030 of 1,296,000, changed region x 430..1140, y 253..724 |
| `screenshots/before--catena--mixed-collection-members--393x852.png` / `screenshots/after--catena--mixed-collection-members--393x852.png` | 1 | pixels differ, 37,398 of 334,836, changed region x 10..368, y 245..851 |
| `screenshots/before--catena--null-bootstrap--1440x900.png` / `screenshots/after--catena--null-bootstrap--1440x900.png` | 7 | pixels differ, 58,181 of 1,296,000, changed region x 298..1140, y 221..899 |
| `screenshots/before--catena--null-bootstrap--393x852.png` / `screenshots/after--catena--null-bootstrap--393x852.png` | 7 | pixels differ, 54,799 of 334,836, changed region x 23..368, y 215..850 |
| `screenshots/before--catena--padded-verse-keys--1440x900.png` / `screenshots/after--catena--padded-verse-keys--1440x900.png` | 5 | pixels differ, 14,469 of 1,296,000, changed region x 297..714, y 595..843 |
| `screenshots/before--catena--padded-verse-keys--393x852.png` / `screenshots/after--catena--padded-verse-keys--393x852.png` | 5 | pixels differ, 22,165 of 334,836, changed region x 22..368, y 408..851 |
| `screenshots/before--catena--stray-partial--1440x900.png` / `screenshots/after--catena--stray-partial--1440x900.png` | 4 | pixels differ, 22,112 of 5,123,520, changed region x 763..1139, y 865..1396 |
| `screenshots/before--catena--stray-partial--393x852.png` / `screenshots/after--catena--stray-partial--393x852.png` | 4 | pixels differ; the two frames are different heights, so no single box is quoted |
| `screenshots/before--probe-index.json` / `screenshots/after--probe-index.json` | — | differing; digests only, not a raster |

**What no screenshot in this package proves:** anything invisible in a raster.
A `lang` attribute, a URL that was or was not requested, `aria-busy`, and the
focused element are all outside a picture, and the probe reports rather than
the images are the evidence for them. **Most of this correction is of that
kind**, which is why eight states of eleven are captured and three are not.
