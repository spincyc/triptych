# Recognition expansion

Audit date: 2026-11-07. Five independent object records and seven original
monochrome recognition figures extend the dictionary to 87 canonical records.
The whole corpus and every completeness-matrix row remain open.

## Source witnesses and inspection

The existing exact registered artifacts were reused. Their bytes were hashed,
then the named page images were inspected directly; searchable OCR was used
only to locate the passages. No source PDF, page image or received prayer text
is added to the publication.

| Witness | Exact canonical artifact | Inspected evidence | SHA-256 |
| --- | --- | --- | --- |
| *Missale Romanum*, Vatican typical edition, 1962 | `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf` | General Rubrics 133, 135–136 (printed XX / PDF 18), 526–527 (XXXVI / PDF 34); *Ritus servandus* I.3 and II.2 (opening Ritus page / PDF 56), VII.9 (LIX / PDF 61) | `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` |
| Fortescue–O’Connell, *The Ceremonies of the Roman Rite Described*, seventh revised edition, 1943 | `artifact.adrian-fortescue.ceremonies-of-the-roman-rite-described.seventh-revised-1943.dli-internet-archive-pdf` | Printed pp. 6, 10–12, 19–20 / PDF pp. 27, 31–33, 40–41 | `10acb8de9b161ed2c08be7ce767515418bca5d1ed7ddfff2de902179e1b62c7a` |

The Internet Archive item metadata dates the ceremonial 1917; its scanned
edition witness is the seventh revised edition of 1943, which controls the
binding. The earlier ceremonial's folded-chasuble and Palm Sunday color
statements do not govern 1962. The Missal's operative rubrics control the
cope/chasuble distinction and the paten relationship. This audit imports no
obsolete folded-chasuble instruction or earlier cope-color rule.

## Five canonical entries

| Object | Facts established | Deliberate boundary |
| --- | --- | --- |
| `obj-altar-cards` | Separate prayer aids; usual three-card set with a larger central card; central, Epistle and Gospel placements; presence only during Mass | Blank faces omit received texts. Frame, support and relative proportions are representative. No prelatial Canon-book identity is inferred. |
| `obj-altar-frontal` | Front hanging; English frontal and Latin antependium/pallium; distinction from the three cloths covering the altar | The ceremonial's description is not asserted as a universal 1962 requirement. Attachment, dimensions, ornament and changeover remain unprescribed. |
| `obj-biretta` | Ordinary square black cloth cap with three ridges; priest gives cap to minister before the lowest altar step | No rank color, privilege, universal ornament or ordinary server headwear assignment. |
| `obj-cope` | Semicircular cape with a front fastening; specified solemn and related-ceremony uses; no maniple for the celebrant wearing it | No universal ornament, exact tailoring, privileged clasp, or substitution for the Mass chasuble. |
| `obj-humeral-veil` | Broad oblong silk shoulder textile; subdeacon's veiled chalice approach and deacon-to-subdeacon paten relationship in VII.9; Requiem exception | No lay-server sacred-vessel assignment. Other humeral-veil ceremonies require their own exact loci; the present isolated study supplies no complete action sequence. |

All five records supply source-linked identity, appearance, use, ceremonial
presence and handling boundaries, plus placement where relevant. Their aliases,
category and ceremony fields provide catalogue keys. Fourteen existing records
receive reciprocal confusable or related-object links; these organize already
bounded identities without creating additional ritual claims. The print and
web views consume those same canonical records.

## Original figures and rights

The seven new asset paths and their artwork IDs are registered in
`../artwork-manifest.toml`. Each row records the received generator raster and
normalized publication raster separately, including dimensions, mode, byte
count and SHA-256. Only 8-bit grayscale/profile normalization was applied; no
morphology was edited locally. The source-constrained generation brief is
retained, while raw prompts and machine paths remain outside tracked records.

No third-party image was supplied to generation. The source books supply
bounded facts, not pixels or copied received text. Project-content terms apply
to the new illustrations. The generating and dictionary agents independently
inspected the five full-size isolated outputs: three cards; one complete rectangular
front hanging; one square cap with three ridges; one open semicircular cope;
one broad oblong veil. Counts, silhouettes, complete hems and the simple cope
fastening are legible. No baked labels, arrows, text, watermark, clipping or
unrelated objects were observed. The white field is an intentional page ground;
proportions and fine construction are representative within the stated limits.

Two contextual studies disambiguate the otherwise similar rectangular
textiles. The frontal inset separates a front hanging from the top covering
and uncovered side of a simple altar support. It is not a complete prepared
altar; its top-covering silhouette does not teach a cloth count or side drop.
The humeral-veil inset shows the shoulder-and-covered-hand relationship on an
anonymous wearer. The plain underlying garment is illustrative and makes no
minister-specific vesture claim. These limits print beside both paired views.
Both contexts passed independent full-size visual review; no complete action,
sacred-vessel use or sanctuary arrangement is inferred from them.

## Derived editions and verification

The native renderer's fixed plate plans explicitly cover the additions and
retain exact-cover validation. Cards join books, the frontal joins altar
appointments, and the three new wearable objects share comparison space. The
web catalogue groups the humeral veil with the sacred ministers and exposes
its related-ceremony category without claiming unverified ritual uses.

Structural validation reports 87 conforming records. Each of the six generated
admission registers adds exactly the five new objects: comprehensive 69,
altar server 55, sacristan 56, MC/trainer 56, general reader 54, and pontifical
67. Omission counts remain 18, 32, 31, 31, 33 and 20 respectively. Admission is
bounded; no omitted record or complete sanctuary composition is released by
these isolated figures.

All six final native builds passed, totaling 105 pages. Every page received
individual full-size screen review across the dictionary, reader, independent
review and coordinating agents. The last typography adjustment changed only
terminal source apparatus: unchanged body pages transferred review solely by
exact SHA-256 equality of their full-page PNG rasters, and every changed page
was inspected individually. Final PDF hashes, page counts and reviewer scope
are recorded in the [consolidated review](../../../../../../../../../workflows/reviews/sanctuary-visual-expansion-2026-11-07/REVIEW.md).

The final review corrected an MC furnishing-caption collision by selecting
the normal four-object layout, and a comprehensive colophon-only page by
reducing source-note and reference paragraph spacing from 4pt to 3pt while
retaining 8pt type and 9.5pt leading. The final comprehensive rights block
has approximately 37pt of bottom clearance. No clipping, object-label collision,
blank figure slot or rights-only page remains. All PDF fonts are embedded and
subset; build logs show no overfull box, undefined reference, duplicate
destination or rerun warning. This is screen review, not a physical-print or
photocopy trial.

The 29 focused native dictionary tests pass against the settled sources.
Artwork validation passes with no held-asset notices. The browser reader
contains 69 catalogue rows, 71 identified objects and 77 selected drawings;
its catalogue and interaction checks are recorded in the consolidated review.
The seven new artwork rows therefore record factual, rights, visual, print and
consumer review as passed. Release remains a separate pending workflow state;
these receipts do not claim publication or ecclesiastical approval.
