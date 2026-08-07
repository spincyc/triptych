# Live Reader ritual-flow baseline

## Boundary

- Phase: Live Reader — Ritual Flow & Orientation
- Synchronized start: `1bca6a0ee862fce5873d6b0c2d92389e78ca018b`
- Canonical Day source SHA-256: `9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`
- Canonical Propers source SHA-256: `a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`
- Accepted cutover: `9b5f21c0ca26bf02af03d207ddd2617021e16fb3`
- Qualifying Pages run: `31175722949`

The accepted live first viewport is the protected baseline. This phase measures
and improves sustained reading after identity and major headings leave the
viewport. It does not use the old public reader as an oracle; the live canonical
reader, retained production candidates, and accepted Instrument oracle own the
comparison.

## Required pre-change capture matrix

The governed Chromium harness will capture original pixels and exact URL/hash,
viewport, scroll target and position, semantic location, current Contents item,
geometry, overflow, focus, console, network, and HTTP results for:

- Roman 1962 Day Missal at 1440×900 and 393×852: top, Lessons/Offertory,
  Preface, Canon, Communion/post-Communion, and a deep conditional/alternative
  Ordinary region.
- Postconciliar Day at 1440×900 and 393×852: top, deep reading, and deep
  Ordinary/ritual states.
- Day Read at 1440×900 and 393×852: top and deep.
- Propers Read at 1440×900 and 393×852: top and deep.
- Existing why, territorial, Roman partial, postconciliar partial-English,
  200% text, keyboard focus, forced colors, and reduced-motion states.

## Initial visual diagnosis

Before correction, the shared shell exposes four actions but no persistent
current division/unit after the identifying headings scroll away. Contents marks
one current row but does not place that row into view when opened. Production
Ordinary markup distinguishes some rubrics and options, yet long conditional or
reference material is not uniformly classifiable from presentation hooks and
therefore cannot be visually demoted until its existing source-owned state is
proved. The capture and full-size inspection record will be appended here; no
measurement will be manufactured in advance.

## Protected measurements

- Read measure at 768×1024: approximately 636 px / 75 characters.
- First-principal-text positions: must remain within a small measured tolerance
  of the accepted live reader.
- Shell actions: four, with accepted rail/dock geometry and 200% labeled reflow.
- Text obscured by any new persistent locus: zero.
- Required horizontal overflow: zero.

## Capture results

The authoritative pre-change run is
`build/agent-continuity/liturgy-reader-ritual-flow-baseline-captures-v4/`.
It was captured only after rebuilding and verifying the locked private preview;
an earlier local run against stale preview bytes was rejected and is not used as
evidence. The authoritative run passed 24/24 governed assertions, produced 61
named original-pixel canonical captures, and recorded zero console, required
request, HTTP, unnamed-control, duplicate-ID, or required-overflow defects.

Protected first-view measurements exactly match the accepted cutover:

| State | First principal text | Text width | Shell |
| --- | ---: | ---: | ---: |
| Day Read 1440×900 | 306.09 px | 636 px | 68×334.34 px rail |
| Day Read 768×1024 | 268.03 px | 636 px / about 75 characters | 768×73.19 px dock |
| Day Read 393×852 | 287.91 px | 351 px | 393×73.19 px dock |
| Roman Missal 1440×900 | 316.98 px | 441.56 px principal line | 68×334.34 px rail |
| Roman Missal 393×852 | 320.66 px | 351 px | 393×73.19 px dock |
| Roman Missal 320×852 | 336.84 px | 278 px | 320×73.19 px dock |
| Propers Read 1440×900 | 306.91 px | 636 px | 68×334.34 px rail |
| Propers Read 393×852 | 258.48 px | 353 px | 393×73.19 px dock |

The Contents defect is also measured. Its scroller starts at 103.58 px and
ends at 891.58 px on desktop; without automatic placement, the near-end current
row begins at 1010.56 px and is not visible. On 393×852, Canon begins at
857.56 px and near-end at 1077.19 px, both below the 169.2–852 px visible
scroller. At 200% text Canon begins at 1682.66 px below the 253.2–852 px
visible scroller. Every baseline Contents `scrollTop` is zero.

Full-size inspection confirms the governing visual diagnosis. Deep Canon,
Preface, Communion and conclusion states retain the accepted reading plane but
offer no persistent locus once their own headings leave view. Roman source-held
Preface/conditional forms remain equally present because production does not
resolve their applicability; this is a semantic limitation, not permission to
hide one. Positively classified rubrics and notes are subordinate but can be
made calmer, especially on mobile. The postconciliar deep state honestly shows
sparse held Ordinary coverage rather than a fabricated continuous prayer.
