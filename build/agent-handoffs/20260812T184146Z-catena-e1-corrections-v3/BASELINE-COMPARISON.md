# BASELINE-COMPARISON — reviewed V2 head versus this head

| Side | Commit | How it was measured |
| --- | --- | --- |
| Baseline | `17f031b37840d8320c664a128d72b502108fe075` | the exact head the 2026-08-12 independent review dispositioned; measured in this same working tree before any edit, and again in a separate clean clone of that commit for the full-suite comparison |
| Head | `f2c9bc49dd29499734193b264ba9da21304b27f1` | this package's reviewed state |

Four classes are kept apart below, because collapsing them is how a package
produces a false "no regressions" claim.

## 1. Browser artifact gate — identical, in identity, status AND detail

    $ make public-site && make check-browser-gate

| Measure | Baseline | Head |
| --- | --- | --- |
| routes / states / pages | 19 / 9 / 171 | 19 / 9 / 171 |
| assertions | 2,290 | 2,290 |
| pass / fail / skip | 1,836 / 226 / 228 | 1,836 / 226 / 228 |
| exit status | 1 | 1 |

Compared as complete assertion objects keyed by `(route, state, name)`:

- the identity set is **equal** — no row appeared, disappeared or moved;
- **0** rows changed status;
- **0** rows changed `detail` text.

This is a stronger result than V2 reported for itself. V2 recorded 15 Catena
`detail` texts differing from pristine main and correctly declined to call the
rows byte-identical. V3 changes no rendered output for any state the gate
visits, so the reports are equal object-for-object.

The 14 failing Catena rows are unchanged in both: 9 `single-main-element`
(`found 2 <main> elements`) and 5 `primary-controls-meet-target-size`. Every
control named in the latter is a shared shell or navigation link — "Triptych",
"The Source Library", "Every Document" and so on — not a Catena-owned control.
Both belong to the B0/shared-shell owner and are recorded in
`UNRESOLVED-BLOCKERS.md` row 8. This lane changed no CSS and no markup.

## 2. Inherited `make -k check` failures

    $ make -k check      # MAKE_EXIT=2, both sides

**Exactly three targets fail, on both sides, and they are the same three:**
`check-release-bindings`, `check-tool-registry`, `check-examples`.

`check-tool-registry` reports the same 8 sibling-declaration findings on both
sides (`calendar-days`, `calendar-rubrics`, `mass-ordinary`, `mass-propers` ×2,
`mass-today` ×2, `source-reader`). Nothing in this lane touches the registry.

The other 17 targets pass on both sides, including `check-catena`
(`catena valid: fragments=1351 books=1 canon=73`) and `check-browser-static`.

## 3. The expected release-owned failure, unchanged in identity

`check-release-bindings` fails closed on both sides with the **same three
paths** and the same `stale: 3 stale binding(s)`:

| Path | recorded | actual at baseline | actual at head |
| --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | `aa564bc2…0099d6` | `733e8490…8851c5` | `733e8490…8851c5` — **unchanged** |
| `src/web/browser/catena/catena.js` | `51aaa3cf…6d20d0` | `023663d2…2b9625` | `fb03ee65…3cf591` — **changed, as expected** |
| `src/web/browser/catena/index.html` | `45c491ab…acc440d` | `7779d1f1…2bb8fa8` | `7779d1f1…2bb8fa8` — **unchanged** |

Only `src/web/browser/catena/catena.js` moves, because it is the only site source this lane edited.
The two unchanged `actual` digests are independent confirmation that
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are byte-identical to the reviewed head.

`refresh-release-bindings` was **not** run. This lane holds no authority to
re-sign, and the fail-closed state is deliberate. See `UNRESOLVED-BLOCKERS.md`
row 4 and `REVIEW_REQUEST.md` blocker 5.

## 4. Example-replay divergences — the counts and the set difference

| Side | Line |
| --- | --- |
| Baseline | `201 captured example(s); 192 replayed, 30 diverged, …` |
| Head | `201 captured example(s); 192 replayed, 28 diverged, …` |

**The head set is a strict subset of the baseline set. There is no new
divergence — the set difference in that direction is empty.** Two baseline
`DIFF` lines are absent at head, both of them the same command:

    DIFF    tools/mass-ordinary check --out build/example-ordinary

That command writes into `build/`, which is git-ignored and whose contents
differ between the two runs (the head run followed a `make public-site` in the
same tree). This is pre-existing build-state sensitivity in an unrelated tool's
example capture, not an effect of this lane, which touches no ordinary,
calendar or propers path. It is reported rather than smoothed over, and no
expected failure was altered to obtain it.

The one Catena-attributable divergence — `tools/public-alpha verify --preview`,
which is §3's unsigned-binding condition seen through the public-alpha verifier
— is present on **both** sides and remains open.

## 5. Test suites

    $ python3 -m unittest discover -s tools/tests -p 'test_catena*.py'

| Side | Result |
| --- | --- |
| Baseline | 231 tests, OK |
| Head | 249 tests, OK |

The 18 added tests are the unsupported-voice and untyped-provenance
regressions, the upper-case grammar case, and the `joinNames` precondition pin.
One existing test changed rather than being added:
`test_a_voice_the_chapter_lacks_is_kept_and_named_rather_than_widened` used
`translation:de`, a language the corpus has never held, and asserted the page
render `German translation — none here`. That assertion pinned the defect the
review found, so it is retargeted to `translation:grc` — a language the corpus
really does hold, and which Genesis 1 really does not hold a translation in —
and the `de` case is now pinned as a refusal in `UnsupportedVoiceTest`. No test
was deleted, weakened or marked expected-failure.

The full `unittest discover` over `tools/tests` was also run on both sides, in a
separate clean clone of the baseline commit, so the failure sets could be
compared directly rather than assumed. See `logs/all-tests-comparison.log`.

## 6. Budgets

Measured with the repository's own function — `gzip.compress(text, 9, mtime=0)`
over the whole file, and over the file with comments stripped.

| Budget | Ceiling | Baseline | Head | Change |
| --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` whole | 8,000 | 7,629 | 7,629 | 0 (byte-identical file) |
| `src/web/browser/catena/catena.css` rules only | 2,700 | 2,676 | 2,676 | 0 |
| `src/web/browser/catena/catena.js` whole | 13,000 | 12,996 | 12,995 | **−1** |
| `src/web/browser/catena/catena.js` code only | 8,800 | 8,795 | 8,799 | +4 |

**No ceiling was raised.** The whole-file measure went *down* despite the
correction. The comment-stripped measure rose by 4 bytes and stands 1 byte
clear; what that cost in source prose is disclosed in `LIMITATIONS.md` §3.

## 7. What did change, deliberately

`src/web/browser/catena/catena.js` and `tools/tests/test_catena_wave_1.py`, plus
four durable authority records. Nothing else. `src/web/browser/catena/catena-model.js` is byte-identical
to main at SHA-256 `f1ea94f9…ccf57b`, asserted by the focused suite itself.
