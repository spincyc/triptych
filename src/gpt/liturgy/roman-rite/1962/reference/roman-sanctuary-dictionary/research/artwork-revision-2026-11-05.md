# Six dictionary figure revisions — 2026-11-05

The fixed-altar, tabernacle, ciborium, and standing-crucifix studies add four
source-audited objects. The amice and maniple studies restore the central
crosses presupposed by the 1962 Missal, *Ritus servandus* I.3. The earlier
plain amice/maniple drawings and their alpha derivatives are rejected for
current use; their generation history remains in the artwork manifest.

## Figure identities and findings

| Figure | Inspection finding |
| --- | --- |
| `art-altar-stone-study` | Bare stone mensa joined to a stable solid base; no cabinetry, cloth, ornament, or appointments. This is one representative fixed-altar form. |
| `art-tabernacle-casket-study` | Modest solid casket with two outward-opening hinged doors and an empty interior. The isolated view does not depict permanent mounting or the veil used during reservation. |
| `art-ciborium-covered-study` | One foot, stem, knop, broad cup, and fitted lid with visible seam. The unveiled morphology view contains no Hosts and does not show reservation preparation. |
| `art-altar-crucifix-standing-study` | One coherent cross, corpus, short support, and stable base. No processional pole, lettering, plaque, candles, or companion objects. The base is illustrative. |
| `art-amice-central-cross-study` | Complete rectangle and two ties, with one cross centered across the upper cloth and adequate cloth margin. The exact coordinate and stitch form are representative. |
| `art-maniple-central-cross-study` | One cross on the visible outer midpoint fold of the band; both hanging ends remain complete. No added terminal crosses or fringe. |

The artwork-producing agent inspected every received figure, every normalized
figure composited on white at full size, and a 360-pixel longest-edge preview.
The coordinating agent independently inspected all six full-size white-ground
figures and accepted the source-bounded morphology and cross repairs. The
crosses remain legible in the small previews. These are screen figure reviews;
they establish neither physical print nor photocopy results.

## Sources actually inspected

The artwork lane read the source-page images for Fortescue's seventh revised
edition (1943), printed pp. 3, 6, and 16 (artifact PDF pp. 24, 27, and 37),
and the 1962 Missal's *Rubricae generales* 525–529, printed p. XXXVI (PDF p.
34), and *Ritus servandus* I.3 (opening Ritus page, PDF p. 56). The object
records own exact source identifiers and the claim-level verification.

The source-content lane separately checked canon 1269–1270 and *Ritus
servandus* X.6–7. This artwork review does not assert an additional image
collation of those passages. The registered Metropolitan Museum object
469881 JSON was read for its separate cross, corpus, and base measurements.
That medieval example supports only component morphology here. Its photograph
was neither inspected nor supplied to generation; no historical reproduction
or universal pedestal design is claimed.

## Generation and inputs

Every selected figure was made by a separate built-in image-generation call
with transparency requested. Exact prompts, received identities, normalized
identities, and generator disclosure are durable in
[`artwork-manifest.toml`](artwork-manifest.toml). The interface did not expose
the exact model/version or runtime.

The four new studies used the project-owned `art-chalice-isolated-v2` and
`art-paten-isolated-v2` as style references only: fine graphite texture,
restrained tonal modeling, clear contour, and complete isolated silhouette.
Their ornament was not transferred. No third-party image was supplied.

Each vestment correction used its previous alpha figure as the edit target
and a white-ground technical preview of the same bytes as supporting input.
The previews introduced no new morphology. The generator preserved the
principal silhouette, ties or band, and fold arrangement while rescaling and
slightly redrawing texture; these are not pixel-exact overlays. The corrected
figure IDs name their rejected precursors in the manifest.

One separate extraction attempt on the altar failed to remove the white
fringe and slightly redrew texture. It was discarded; the initial selected
altar is the registered figure. No extraction edit is part of the selected
figure's provenance chain.

## Normalization and white-ground limit

Every final file is an 8-bit grayscale-alpha PNG. The existing
`artwork-library normalize` implementation disables alpha, so the technical
conversion used ImageMagick's `-colorspace Gray -strip -depth 8 -define
png:color-type=4` without clipping, content editing, resizing, or alpha
changes. Alpha-channel absolute error was zero for every before/after pair.
The received and normalized dimensions, bytes, hashes, placement limits,
and comparison values are recorded in the manifest.

| Figure | Normalized RGBA RMSE |
| --- | ---: |
| Altar | 0.00247798 |
| Tabernacle | 0.00232689 |
| Ciborium | 0.00207467 |
| Altar crucifix | 0.00167021 |
| Amice | 0.00140682 |
| Maniple | 0.00108334 |

All six have genuine alpha, but the cutouts are not pristine on dark grounds.
Altar, crucifix, amice, and maniple retain diffuse white fringe; the other two
have narrow white edge remnants. These disappear on the intended white page.
Use these assets only on white, without overlapping the fringes over another
figure. The screen review found no gray scene background, frame, caption,
letters, arrows, watermark, or clipping on white.

## Admission and current review state

The six object records remain `art-reviewed`, their current artwork links remain
`liturgically-checked`, and the file records remain `canonical-alpha-eligible`
under the existing source-bounded alpha admission contract. Following the exact
78-page native PDF screen review below and the coordinator's current 66-object
gallery selection review, only the six new full figure records advance to
`consumer-review-passed`, with `reviews.print` and `reviews.consumer` marked
`passed`. Here print means the assembled native print-PDF screen check on white;
it does not mean a physical printer or photocopy test. Gallery use is likewise
limited to its inspected white-ground presentation. `reviews.release` remains
`pending`; no deployment or publication-release approval is inferred. The
validator accepts this truthful intermediate state without requiring a release
pass or any validation-rule change.

At initial figure admission, plate, consumer, print, and release reviews were
pending. The assembled native-page review below records the later screen event
for exact output identities. Historical reviews of superseded drawings do not
transfer to them.

## Assembled native-page review — 2026-11-05

The artwork lane built all six canonical print recipes with `tools/print-document`
after the permanent isolated-build path correction and the final source captions.
The first altar-server build exposed a mostly empty missal-stand page; an explicit
six-plus-seven sanctuary plan removed it without dropping any admitted object.
The vestment-only companion slice now declares only its own section order, so
full-edition plate coverage remains strict. The renderer suite passed all 21 tests.

Every page of each final output is covered by full-size visual inspection using
the memory-bounded `tools/pdf-review` page rasters (2200-pixel longest edge, four
workers), not by contact sheets alone. Comprehensive pages 1–2, 4–5, and 7–13
were inspected in the first successful build and have byte-identical final page
rasters; its changed pages 3, 6, and 14 were inspected again. The altar-server
title page likewise remained byte-identical; all its final pages 2–11 were
inspected again after regrouping. All final pages of the other four editions
were inspected directly. This covers 78 final physical PDF pages.

| Edition | Objects | Pages inspected | Changed-figure pages (physical PDF numbers) | Bytes | PDF SHA-256 |
| --- | ---: | --- | --- | ---: | --- |
| altar-server | 48 | 1–11 | 2–4 and 8 | 24231764 | `a5ae4b3b1b9bd4250c814af74b8116cbbb9efe57f4bfca1be03c472b431f7a49` |
| comprehensive | 49 | 1–14 | 3, 5–6, and 11 | 23972817 | `4eb0044fd949b9d93963fe08af267133f3332b84b470ab2935adc000fa017866` |
| general-reader | 47 | 1–12 | 2, 5, and 10 | 24062100 | `0ea5bba83b63db2b32cad934a689088fd40f835e98151118c8979d51cff241ba` |
| mc-trainer | 49 | 1–11 | 2, 4, and 9 | 24414536 | `f571b26c03a34a93b7dd20b1b86a438282e59fe64ecb01da9481f01d69fef195` |
| pontifical-ceremonies | 60 | 1–17 | 4, 7, and 12 | 31241239 | `790fca407021160ae330c1a0495fc69d268e5736791f981377ec14474b534304` |
| sacristan | 49 | 1–13 | 2, 7, and 10 | 24456911 | `6f174725c673936161427abc3596542051e6cd6b8d7d1252b2222da732c33a09` |

The final figures keep complete silhouettes on white and do not overlap other
figures. The amice and maniple crosses remain visible in every audience edition.
The bare-altar preparation qualifier and both reservation-veiling qualifiers are
present in the assembled captions, including the denser seven-object plates.
English names, Latin headwords, audience boundaries, and the comprehensive
historical-witness source caption remain readable and inside their allotted cells.
No missing figure, glyph, clipped text, collision, or accidental blank page was
found. Spacious comparison plates and title/terminal pages retain intentional
white space; the accidental singleton page was removed.

All six TeX logs have zero overfull boxes and zero missing-character notices.
The MC/trainer log has six underfull paragraphs and the pontifical log has three;
their visible spacing was inspected and accepted. All reported fonts are embedded
Latin Modern fonts. Every output is US Letter (612 × 792 pt), PDF 1.7.
`tools/artwork-library check-pdf` passed for every output. Its above-450-dpi
review notices number 54/52/50/55/56/51 for altar-server/comprehensive/
general-reader/MC-trainer/pontifical/sacristan respectively, reaching 1856 dpi
in the densest uses. The original grayscale artwork is retained without new
lossy compression or layout-specific downsampling; screen clarity passes, but
the image-heavy files remain about 24–31 MB. These size and resolution notices
are acknowledged review triggers, not hidden validation failures.

The assembled-page consumer screen review passes for these exact outputs on
white. This is neither a physical printer/photocopy test nor a browser-WASM
byte-equivalence test, and it makes no unperformed release approval. The normal
print receipts correctly still say `generated-unreviewed`: they report generation;
this dated audit records the separate visual event. The subsequent coordinator-authorized lifecycle reconciliation above retains
the physical-print limitation.

### Reproduction and disposable evidence

Run from the repository root, for each of the six edition directory names above:

```sh
TRIPTYCH_PRINT_WORK_ROOT="$PWD/.scratch/dictionary-art/print-work-final" tools/print-document build --document publication:gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/<edition> --out .scratch/dictionary-art/print-final/<edition>
tools/pdf-review --output .scratch/dictionary-art/page-review-final --cache .scratch/dictionary-art/page-cache --jobs 4 .scratch/dictionary-art/print-final/*/*.pdf
```

PDFs and generation receipts are under `.scratch/dictionary-art/print-final/`;
their full recipe-named filenames and identities are also recorded in
`.scratch/dictionary-art/final-pdf-identities.json`. Every output directory holds
`text.txt`, `fonts.txt`, and `artwork-pdf-check.txt`. Full-size page rasters are
under `.scratch/dictionary-art/page-review-final/.scratch/dictionary-art/print-final/`
followed by the edition, recipe stem, and `pages/page-NN.png`. The bounded review
run receipt is `.scratch/dictionary-art/page-review-final/review-run.json`.
All these generated artifacts are disposable and are not tracked.

The native engine was pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026/Arch Linux).
Page review used Poppler 26.10.0 and ImageMagick 7.1.2-35. The page-review
renderer fingerprint was
`8d88ad4054fb4e93622f96a810cb598089045791d769cdc7f3b03ec4fe3787fa`.
Each `.print.json` receipt contains the complete hashed input inventory.
Selected controlling file identities at inspection:

- `Makefile`: `10af49cd073942dab90a55aeb162b9ebbd76f4a5e1a2a94adf4b80ea92d851d6`
- `tools/render-sanctuary-dictionary`: `9b2476b3fe844ec822c10a905688e6dc669a75795df53fb07842cbdd263c9cea`
- `src/common/document-types/sanctuary-dictionary-v1/main.template.tex`: `88af7dab403f974d409c386b258ce1588e77a1f3a86a2c9832ad9449540cf780`


### Final heading correction and superseding output identities

The final renderer uses “Vessels and linens” for the comprehensive mixed vessel
and textile plates, and “Water and Communion vessels” for the MC/trainer plate.
Canonical section IDs and admitted objects remain unchanged. The renderer suite
again passed all 21 tests. The generated TeX for altar-server, general-reader,
pontifical, and sacristan, plus the vestments-only companion, is byte-identical
to the preceding reviewed generation; comprehensive and MC/trainer contain the
heading corrections. All six native editions were nevertheless rebuilt and
passed `tools/artwork-library check-pdf` again.

These identities supersede the preceding PDF hash table. Of the 78 resulting
page rasters, 69 are byte-identical to the individually inspected preceding set.
The nine changed pages were inspected again at full size: comprehensive 6, 7,
and 14; MC/trainer 9 and 11; altar-server 11; general-reader 12; pontifical 17;
and sacristan 13. Three pages contain the heading corrections; the six terminal
pages contain updated revision timestamps. The longer headings and complete
right-hand plate numbers remain within the page margins. Terminal metadata and
rights text remain readable and unclipped. No further visual defect was found.
The white-ground consumer screen pass therefore covers all 78 pages of this
superseding set, with the same physical-print and release limitations above.

| Edition | Pages | Bytes | Final PDF SHA-256 |
| --- | ---: | ---: | --- |
| altar-server | 11 | 24231553 | `8046729fde6cdd4e17d90fe8f818e995bf4fd990553dc256adff58588fae4e4a` |
| comprehensive | 14 | 23972623 | `f33e663199102f9b04014d7e6a50635dc93ef114c2e995ef5bec92b637f92428` |
| general-reader | 12 | 24062098 | `de0c34a0a2cd8df21b82f0f42f30c2a35d18ffbafe50c9f5a5a00c6e1222d627` |
| mc-trainer | 11 | 24414569 | `1da9ba0e9d7254f8d4aaf1f68a0d33687d6868b2d87d69a525380a6adf12c5ce` |
| pontifical-ceremonies | 17 | 31241238 | `7b34a7aca2621a187c174b7c782e57356744eab45dc6c48c8d2d0cea3aaf88e7` |
| sacristan | 13 | 24456694 | `02e741d09e642a248d980d8c07f50eda3579447483181c7a0f43ab880ff69493` |

Exact disposable PDF paths (relative to repository root):

- `.scratch/dictionary-art/print-labels/altar-server/altar-server--8d6ef9ee7792363f.pdf`
- `.scratch/dictionary-art/print-labels/comprehensive/comprehensive--8d7a3290a3baac13.pdf`
- `.scratch/dictionary-art/print-labels/general-reader/general-reader--b3d3775d79dfdc4e.pdf`
- `.scratch/dictionary-art/print-labels/mc-trainer/mc-trainer--8bbc52076ee3ca6f.pdf`
- `.scratch/dictionary-art/print-labels/pontifical-ceremonies/pontifical-ceremonies--8a620eda7508c98c.pdf`
- `.scratch/dictionary-art/print-labels/sacristan/sacristan--730c028c11eb6146.pdf`

The same build commands above apply with `print-work-labels`, `print-labels`,
and `page-review-labels` replacing their `*-final` counterparts. Exact output
identities and changed-page lists are in
`.scratch/dictionary-art/label-pdf-identities.json`; generated-TeX comparisons
are in `.scratch/dictionary-art/generated-label-comparison.json`. Each PDF has
its generation receipt and text/font/artwork-check evidence beside it. Full-size
page rasters and the bounded review receipt are under
`.scratch/dictionary-art/page-review-labels/` with the same nested path convention
and renderer fingerprint recorded above. The final controlling renderer SHA-256
is `fb89516776b4ef2b03320c52421844a0fedafb5ffc49274cd4654a07846105ec`.
The final renderer-test log is
`.scratch/dictionary-art/renderer-tests-final.log`.


The final lifecycle-only manifest reconciliation was validated with
`tools/check-roman-sanctuary-artwork` (zero held object-link notices) and
`tools/artwork-library check` (pass). Regenerating the dictionary produced all
13 TeX files byte-identically to the final heading-corrected generation: the six
full editions, their six omission reports, and the vestments-only companion.
The comparison is recorded in
`.scratch/dictionary-art/generated-lifecycle-comparison.json`. Thus the review
state update changes none of the reviewed page content; the exact reviewed PDF
identities above remain the evidence for the screen event. Release remains
pending for all six new figures.
