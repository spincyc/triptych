# Baseline comparison — V4.1 head against its exact parent

Base `e40720d5d622e8b0528b8c714cc5caee0b21cee3`
Head `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`

Both sides were run **in the same clone**, base first by detaching to the parent
commit and rebuilding, so the comparison is not confounded by a second machine
or a second checkout. Nothing below is inherited from V4's package; every number
was measured in this lane.

## Full discovery

`python3 -m unittest discover -s tools/tests`

| | base `e40720d5d` | head `f93757854` |
| --- | --- | --- |
| tests run | 1,617 | **1,618** |
| failures | 14 | **14** |
| errors | 13 | **13** |
| skips | 11 | **11** |
| wall clock | 482.092 s | 483.470 s |
| exit | 1 | 1 |

The single extra test at head is
`TypedStateTest.test_the_shared_refusal_umbrella_stays_neutral`, added by this
lane.

### Failure identity, not failure count

The 27 `FAIL:`/`ERROR:` lines were extracted from each log, sorted, and compared
with `diff(1)`:

    base names: 27   head names: 27
    IDENTICAL failure/error name sets

`diff` produced no output. **No failure is introduced by V4.1, none is removed,
and none changes identity.**

## Browser gate

Real Chromium `151.0.7922.108`, `tools/tests/corpus_browser_gate.mjs`, over a
`make public-site` artifact built on each side.

| | base | head |
| --- | --- | --- |
| routes / states / pages | 19 / 9 / 171 | 19 / 9 / 171 |
| assertions | 2,290 | 2,290 |
| passed / failed / skipped | 1,836 / 226 / 228 | 1,836 / 226 / 228 |

Compared with `logs/compare-gate.py`, key by key:

| key | identical | bytes |
| --- | --- | --- |
| `assertions` | **True** | 399,178 |
| `failures` | **True** | 54,412 |
| `pages` | **True** | 23,259 |
| `summary` | **True** | 1,982 |
| `routes`, `states`, `counts`, `bounds`, `phases`, `chrome`, `root`, `overflowTolerancePx` | **True** | — |
| `generatedAt` | False | 26 |

**Every key except `generatedAt` is deep-equal, across 480,881 bytes of report,
including all 226 failure objects.** This is a literal object-for-object
identity claim and it is proven, not asserted. `generatedAt` differs only
because the two runs happened at different clock times.

## `make -k check`

| | base | head |
| --- | --- | --- |
| exit | 2 | 2 |
| failing targets | `check-release-bindings`, `check-tool-registry`, `check-examples` | the same three |

## Budgets

| measure | base | head | ceiling | movement |
| --- | --- | --- | --- | --- |
| `catena.css` whole | 7,629 | **7,629** | 8,000 | byte-identical |
| `catena.css` rules only | 2,676 | **2,676** | 2,700 | byte-identical |
| `catena.js` whole | 12,981 | **12,970** | 13,000 | **−11** |
| `catena.js` code only | 8,749 | **8,734** | 8,800 | **−15** |

No ceiling was raised. The correction has **negative** JavaScript cost: the
replacement strings are shorter than the ones they replace. The stated ideal of
"zero JavaScript growth" is met with margin.

## Classification of every difference

| difference | classification |
| --- | --- |
| +1 test at head (1,617 → 1,618) | **introduced by V4.1** — the new refusal-neutrality regression |
| `catena.js` gzip −11 / −15 bytes | **introduced by V4.1** — shorter copy |
| `catena.js` actual release-binding hash | **introduced by V4.1**, but the binding was **already stale** at base; count stays 4 |
| 14 failures / 13 errors, all 27 names | **inherited** — identical at base and head |
| 226 gate failures (`single-main-element`, `primary-controls-meet-target-size`, `skip-link-targets-existing-element`) | **inherited** and **separately owned** (common gate / shared shell) |
| `check-tool-registry`, `check-examples` | **inherited** and **separately owned** |
| `check-release-bindings` stale: 4 | **inherited** and **separately owned** (release) |
| `test_candidate_does_not_leak_fixture_or_discovery_records` and siblings | **inherited** from V4 and a pre-existing propers lane; see `DATA-TEST-CONTRADICTION.md` |
| `generatedAt` in the gate reports | **environment-sensitive** (clock) |
| 53 PNGs | **evidence-only** — no production effect |

**Introduced by V4.1 and requiring judgment: none beyond the copy itself.**
