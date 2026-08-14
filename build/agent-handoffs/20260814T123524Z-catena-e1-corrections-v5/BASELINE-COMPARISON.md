# Base against head — every suite, gate and measurement

Base is `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`, the exact reviewed V4.1
head, run in a **separate clean clone** so no state is shared with the
candidate. Head is `d0218bae2f7db75e181a0a97937264933c35c09f`, the last implementation commit, whose
build-sensitive tree is byte-identical to the final head.

## Focused Catena suite

```
python3 -m unittest discover -s tools/tests -p 'test_catena*.py'
```

| | Base | Head |
| --- | --- | --- |
| tests | 267 | **306** |
| result | OK | **OK** |

The 39 new tests are the regressions the review required, in five classes:
malformed language under Everything held; mixed valid / malformed-record /
scalar / null collection members; the five typed-absence cases; numeric, verse,
path and bootstrap metadata; and seven route-completion scenarios that begin
canonical.

## Full discovery

```
python3 -m unittest discover -s tools/tests
```

| | Base | Head |
| --- | --- | --- |
| tests run | 1,618 | **1,657** (+39) |
| failures | 14 | **14** |
| errors | 13 | **13** |
| skips | 11 | **11** |
| FAIL/ERROR name-set entries | 27 | **27** |

No literal baseline identity is claimed — the head runs more tests. What is
compared is the **set of FAIL and ERROR test names**, and `diff` over the two
sorted sets produces **no output**. The base figures reproduce the V4.1
review's own recorded 1,618 / 14 / 13 / 11 exactly, which is the check that the
comparison environment is the one the review used.

## Browser gate

```
make public-site && node tools/tests/corpus_browser_gate.mjs --json-out <out>
python3 logs/compare-gate.py logs/browser-gate-base.json logs/browser-gate-head.json
```

| | Base | Head |
| --- | --- | --- |
| assertions | 2,290 | **2,290** |
| passed | 1,836 | **1,836** |
| failed | 226 | **226** |
| skipped | 228 | **228** |
| routes × states × pages | 19 × 9 × 171 | 19 × 9 × 171 |

`compare-gate.py` reports:

```
summary equal: True
identity set equal: True
base-only identities: []
head-only identities: []
rows with changed status: 0
rows with changed detail: 0
whole report identical (volatile fields excluded): True
```

**Read the last line precisely.** The comparison excludes four volatile keys —
`generatedAt`, `root`, `durationMs` and `browser` — not one. The V4.1 record's
wording named only `generatedAt`; this is the corrected statement. Every
non-volatile key, including all 226 failure objects with their exact `detail`
strings, is deep-equal.

The 226 failures are the shared shell's: `single-main-element` (117),
`primary-controls-meet-target-size` (82), `skip-link-targets-existing-element`
(27). None is a Catena assertion and none moved.

## `make -k check`

Same three inherited failing targets at base and head:
`check-release-bindings`, `check-tool-registry`, `check-examples`. Exact
outputs and exits are in `checks.txt`; the target list and each target's owner
are in `UNRESOLVED-BLOCKERS.md`. No record here rounds those into a green
repository-wide check.

## Promise ledger

| | Base | Head |
| --- | --- | --- |
| tracked | 29 | **30** |
| complete | 19 | **19** |
| result | valid | **valid** |

The added entry is `corpus-browser-catena-e1-corrections-v5-2026-08-14`, whose
`immutable-v5-handoff` and `fresh-independent-review` requirements are both
**open**. Nothing was marked complete by this lane.

## Catena generator check

```
python3 scripts/_catena.py check
```

`catena valid: fragments=1351 books=1 canon=73`, exit 0, at both base and head.
This matters more than usual for V5: `catena-model.js` is executed under node by
the generator during emit, and `fragmentsOnChapter` — whose membership rule V5
tightened from `Number()` to a positive-safe-integer test — is the function the
generator calls. The check replays it against the solved cases in
`src/sources/commentary/fragment-loci.yaml` and passes unchanged.

## Budgets, gzip -9, whole file, mtime pinned to zero

| File | Measure | V4.1 base | V5 head | Ceiling |
| --- | --- | --- | --- | --- |
| `catena.css` | whole | 7,629 | **7,629** | 8,000 |
| `catena.css` | stripped | 2,676 | **2,676** | 2,700 |
| `catena.js` | whole | 12,970 | **12,990** | 13,000 |
| `catena.js` | stripped | 8,734 | **8,363** | 8,800 |

`catena.css` is byte-identical, not merely equal in size. `catena.js` code is
**371 bytes smaller** because the derivations moved to the unbudgeted model;
the whole-file figure is 20 bytes larger because the boundary is explained
where it lives, leaving 10 bytes of margin. **No ceiling was raised, and no
budget authority was changed.**

## Release bindings

Four stale at base, four stale at head — the same four Catena paths. The
`catena-model.js` and `catena.js` digests differ because those files changed;
`catena.css` and `index.html` are byte-identical to V4.1 and were already
stale. **None was re-signed.** `refresh-release-bindings` and `approve-release`
were not run.
