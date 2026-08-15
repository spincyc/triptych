# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46` |
| head | `e876b29e5797edcc6e86422daa807f4b1104ec81` |
| review addressed | `f183ed1b0afc6f14574a3507f6eaf3102dc999fa` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 7

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `2a5c7260b14d9b96901b456e663e5288dfae61b6` | Replace raw fragment copying with an explicit typed projection | `scripts/_catena.py`<br>`src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena.py`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `daba483d880005887a1e39aeb74914b2b47e3a7d` | Say the projection's argument once rather than three times | `src/web/browser/catena/catena-model.js`<br>`tools/tests/test_catena_wave_1.py` |
| 3 | `734fc052097603d83d42c44894247a302db9854a` | Close five holes an adversarial pass found in the projection itself | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 4 | `cd3966af695aaf67fb5a54f69625d6cd0efcf208` | Close the same class one level deeper, where a second pass found it | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 5 | `7930ec0a196c37c3251095a083508fb4709573cd` | Trim the model's added prose a second time, and give the question its figures | `src/web/browser/catena/catena-model.js`<br>`tools/tests/test_catena_wave_1.py` |
| 6 | `3e0e495af2b4865a603352ce39c3f3d38b35eedc` | Guard the members, not only the containers, a third time | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 7 | `e876b29e5797edcc6e86422daa807f4b1104ec81` | Record the V7 lane, its blockers, and what it left open | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 8 file(s), 3586 insertion(s), 321 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 189 | 0 |
| M | `guidance/corpus-browser-roadmap.md` | 58 | 1 |
| M | `promised-deliverables.toml` | 78 | 0 |
| M | `scripts/_catena.py` | 31 | 2 |
| M | `src/web/browser/catena/catena-model.js` | 871 | 97 |
| M | `src/web/browser/catena/catena.js` | 131 | 161 |
| M | `tools/tests/test_catena.py` | 78 | 0 |
| M | `tools/tests/test_catena_wave_1.py` | 2150 | 60 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12993 | 12901 | 13000 | 8202 | 7530 | 8800 | 0.369 | 0.416 |
| `src/web/browser/catena/catena-model.js` | 15767 | 27832 | none | 4377 | 7385 | none | 0.722 | 0.735 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 28028 | 40041 | +12013 |
| compressed separately and summed | 28760 | 40733 | +11973 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE (V7)` blocks | 14 |
| classes holding a corrected oracle | 11 |
| test classes added | 13 |

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedRecordRenderingTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `V7UnreadableRootDomainClaimTest`.

The V7 test file replayed against the PARENT's production files — same scenarios, same oracles, other code — fails **74** identities across **16** classes: 9 of the classes V7 adds, and 7 pre-existing classes whose oracles V7 corrected.

Classes V7 adds that do **not** fail at the parent: `V7InvalidatedPendingRenderTest`, `V7MalformedPartialTest`, `V7ModelTotalityTest`, `V7SharedFieldDriftTest`. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 505 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 423 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1856 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1774 | 14 | 13 | 11 | FAILED | 27 |
| sealer | 53 | 0 | 0 | 0 | OK | 0 |
| v7_tests_against_parent | 449 | 74 | 0 | 0 | FAILED | 74 |

Full-discovery FAIL/ERROR identity sets at parent and head are **identical** — 27 entries, 0 only at the head, 0 only at the parent, 0 mentioning catena.

## Browser gate

| | parent | head |
| --- | --- | --- |
| browser | Chrome/151.0.7922.108 | Chrome/151.0.7922.108 |
| assertions | 2290 | 2290 |
| failed | 226 | 226 |
| pages | 171 | 171 |
| passed | 1836 | 1836 |
| routes | 19 | 19 |
| skipped | 228 | 228 |
| states | 9 | 9 |

Failure categories at the head: `single-main-element` 117, `primary-controls-meet-target-size` 82, `skip-link-targets-existing-element` 27.

## Package

| | |
| --- | --- |
| members | 54 |
| bytes | 2073043 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

## Byte and control scan

62 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
