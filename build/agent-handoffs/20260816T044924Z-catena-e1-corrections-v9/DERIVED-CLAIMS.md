# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8` |
| head | `3c5b78249193df065c4e1c2ee5a98e5989c6e582` |
| review addressed | `611b5eed8128ad5f84f6bf73ac9f9ead5959ab7f` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 3

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `6c651782479a2ff1a5df4c87aaafcf913dd2568d` | Give the stated prefix its third state, and close the carried door behind it | `src/web/browser/catena/catena-model.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `6c160bf01037381ab1e9f89edf64d0cc5150f4b2` | Pin the three states at the sinks, cold, prewarmed, and late | `tools/tests/test_catena_wave_1.py` |
| 3 | `3c5b78249193df065c4e1c2ee5a98e5989c6e582` | Record the V9 lane: the composed closure, and the package told the truth | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 5 file(s), 600 insertion(s), 14 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 103 | 0 |
| M | `guidance/corpus-browser-roadmap.md` | 36 | 1 |
| M | `promised-deliverables.toml` | 48 | 0 |
| M | `src/web/browser/catena/catena-model.js` | 52 | 11 |
| M | `tools/tests/test_catena_wave_1.py` | 361 | 2 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12901 | 12901 | 13000 | 7530 | 7530 | 8800 | 0.416 | 0.416 |
| `src/web/browser/catena/catena-model.js` | 28346 | 29179 | none | 7485 | 7571 | none | 0.736 | 0.741 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 40557 | 41392 | +835 |
| compressed separately and summed | 41247 | 42080 | +833 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE (V8)` blocks | 0 |
| classes holding a corrected oracle | 0 |
| test classes added | 2 |

Classes holding a corrected oracle: .

The V8 test file replayed against the PARENT's production files — same scenarios, same oracles, other code — fails **10** identities across **3** classes: 2 of the classes V8 adds, and 1 pre-existing classes whose oracles V8 corrected.

Classes V8 adds that do **not** fail at the parent: none. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 519 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 510 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1870 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1861 | 14 | 13 | 11 | FAILED | 27 |
| sealer | 82 | 0 | 0 | 0 | OK | 0 |
| v8_tests_against_parent | 463 | 10 | 0 | 0 | FAILED | 10 |

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

Failure categories at the head: `primary-controls-meet-target-size` 82, `single-main-element` 117, `skip-link-targets-existing-element` 27.

## Package

The inventory below covers ONLY the members frozen before this file was written. A member written at or after the derivation is named under *derived members*, never sized or hashed: its bytes did not exist when the rows froze, and a number typed for it here would be the V8 defect this file corrects. The package-total and final-byte authority is `MANIFEST.sha256` together with the ZIP and its sidecar.

| | |
| --- | --- |
| evidence members (frozen) | 54 |
| evidence bytes (sum of the rows) | 3162581 |
| derived members (named, unsized) | 5 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

60 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
