# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `e876b29e5797edcc6e86422daa807f4b1104ec81` |
| head | `7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8` |
| review addressed | `d9ad5ec1ae35c308a0da5ed3456fd05fdad97cbd` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 2

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `fbd85d5607428cab22e62fa0c451422eda0710a9` | Close the Catena text namespace at the request sink | `src/web/browser/catena/catena-model.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8` | Record the V8 lane: the namespace closure, and what stays open | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 5 file(s), 398 insertion(s), 12 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 87 | 0 |
| M | `guidance/corpus-browser-roadmap.md` | 31 | 1 |
| M | `promised-deliverables.toml` | 42 | 0 |
| M | `src/web/browser/catena/catena-model.js` | 49 | 10 |
| M | `tools/tests/test_catena_wave_1.py` | 189 | 1 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12901 | 12901 | 13000 | 7530 | 7530 | 8800 | 0.416 | 0.416 |
| `src/web/browser/catena/catena-model.js` | 27832 | 28346 | none | 7385 | 7485 | none | 0.735 | 0.736 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 40041 | 40557 | +516 |
| compressed separately and summed | 40733 | 41247 | +514 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE (V8)` blocks | 0 |
| classes holding a corrected oracle | 0 |
| test classes added | 1 |

Classes holding a corrected oracle: .

The V8 test file replayed against the PARENT's production files — same scenarios, same oracles, other code — fails **8** identities across **2** classes: 1 of the classes V8 adds, and 1 pre-existing classes whose oracles V8 corrected.

Classes V8 adds that do **not** fail at the parent: none. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 510 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 505 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1861 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1856 | 14 | 13 | 11 | FAILED | 27 |
| sealer | 53 | 0 | 0 | 0 | OK | 0 |
| v8_tests_against_parent | 454 | 8 | 0 | 0 | FAILED | 8 |

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
| members | 57 |
| bytes | 3058709 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

## Byte and control scan

62 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
