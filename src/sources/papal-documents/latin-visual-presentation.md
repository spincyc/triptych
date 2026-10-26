# Latin reader visual review: Pascendi and Rerum Ecclesiae

Review date: 26 October 2026 UTC. This review covers the rendered page
composition of the two editions below. Mechanical source/PDF comparison,
source collation, and rights review have separate owners and dispositions.

## Initial reviewed artifacts

| Edition | Pages inspected | PDF SHA-256 | Visual disposition |
| --- | --- | --- | --- |
| Pius X, *Pascendi Dominici Gregis*, Latin, 8 September 1907 | Every page, 1–20 | `bbbc24f3ec884db076d9b6b6bdd154c605cdef4684c0a672e7f3280b948783e1` | **CHANGES_REQUIRED**: terminal apparatus spills to page 20. |
| Pius XI, *Rerum Ecclesiae*, Latin, 28 February 1926 | Every page, 1–8 | `2246aa49d38c7832286b047573ad501010b938772b0344390bab023360e4cf43` | **PASS** for page composition. |

The PDFs were independently hashed and their page counts checked against the
typesetting receipt. Review rasters and contact sheets were generated with
`tools/pdf-review`, using a dedicated output directory. Every page was opened
as a readable individual page raster after the complete contact sheets were
inspected; the opening and closing pages were also inspected at original
raster size.

## Page findings

| Edition and pages | Finding |
| --- | --- |
| *Pascendi*, 1–18 | Compact identification, readable two-column text, consistent paragraph spacing, clear gutter, and unclipped page numbers. No visible replacement glyph, text collision, or marginal overflow. |
| *Pascendi*, 19–20 | The papal text and signature end on page 19. The Source section starts at the bottom of its right column and splits a sentence across the page boundary. Page 20 contains only the continuation of the source note, revision timestamp, and rights colophon, occupying seven short lines at the top of the left column. The nearly empty additional page fails the terminal-apparatus composition requirement. Keep the substantive text unchanged and fit its source apparatus and compact colophon on the final substantive page. |
| *Rerum Ecclesiae*, 1–7 | Identification, headings, two-column text, references, signature, and page numbers remain readable and unclipped. The body-to-endnote transition on page 7 is clear. |
| *Rerum Ecclesiae*, 8 | Retained notes 8–20 precede the Source apparatus and legible rights colophon. The final right column is unused, but the page contains substantive historical notes and is not a page generated solely for the modern notice. No clipping or collision. |

The visual review also referred a textual observation to the source-fidelity
owner: *Rerum Ecclesiae* page 5 prints the paragraph beginning “At si
curandum, ut alumnorum indigenarum frequentia” twice. This review does not
determine whether that repetition belongs to the controlling web witness,
the historical printing, or an extraction error, and it does not authorize
alteration of source wording.

## Accepted replacement artifacts

| Edition | Reviewed pages | PDF SHA-256 | Visual disposition |
| --- | --- | --- | --- |
| *Pascendi Dominici Gregis*, Latin | Every page, 1–19 | `dfb3d8e6acfa94aac853d898ebc43bd075adb0fd6ab67c19225c48e3777b9030` | **PASS** |
| *Rerum Ecclesiae*, Latin | Every page, 1–8 | `3d45713fbeeb846dc1fcff5662e45094037cb1a8d895e8dd080b5212400e595a` | **PASS** for composition; textual observation remains with the fidelity owner. |

Both replacements were independently rehashed and rerasterized through
`tools/pdf-review` into a second dedicated output directory. Exact PNG
SHA-256 comparisons show that *Pascendi* pages 1–18 and *Rerum Ecclesiae*
pages 1–7 are identical to the individually inspected pages above. The
revised *Pascendi* page 19 and *Rerum Ecclesiae* page 8 were opened and
inspected at original raster size. The accepted replacements therefore have
complete visual coverage across all 27 remaining pages.

The compact run-in Source label and smaller terminal apparatus fit on
*Pascendi* page 19 after its signature. The source note, revision, and
two-line rights colophon remain legible, with a clear separation from the
papal text and the page number. The former page 20 is eliminated without
changing any of the first 18 pages. *Rerum Ecclesiae* keeps the endnotes and
compact apparatus together on page 8 with no clipping, collisions, or
overflow. The initial spill-page finding is resolved for these exact hashes.
