# Historical English encoding snapshot: final visual review

**PASS for draft visual layout of all 31 exact PDFs, covering all 210 physical pages.** The review combines 103 pages newly opened individually with 107 pages carried forward only by complete PNG byte equality to earlier individually reviewed rasters.

The frozen typesetting receipt SHA-256 is `6c6f508f3bc1859b33cf2c2501a301428ef3bc7d4cbce2b7efd784de08a2e634`; snapshot revision is `2026-10-26T05:10:28Z`. Compilation reports zero warnings and passing complete source-body text fidelity for all 31 PDFs. Those renderer checks are distinct from this visual judgment.

The machine-readable [shared visual audit](english-visual-review.json), schema `triptych-papal-visual-review/v1`, has SHA-256 `427e48339215eb967d2b98885e89984e5edb278243e650fbb2312904ec8666b5`. It pins every current ID, language, PDF hash, page count, tracked report hash, disjoint page coverage and reuse proof. Every reused page pins both equal raster hashes, its prior reviewed PDF hash, and the prior report hash. Rejected Officiorum and Philippine iterations remain explicitly rejected history rather than current PASS rows.

The durable [raster comparison](english-encoding-raster-comparison.json), schema `triptych-english-page-raster-comparison/v1`, has SHA-256 `d007562ea110c3b39643b84fb1d684ad8495588369e0fe127c861205d62cf11e`. All revised rasters were produced once centrally with `tools/pdf-review --jobs 2`; baseline reviewed rasters were reused without rerendering. The exact comparison requires the same renderer fingerprint and validates both manifests before comparing complete PNG byte streams.

| Review report | Scope | Current individual inspection | Exact prior-page reuse |
| --- | --- | ---: | ---: |
| [Changed-source partition 1](english-encoding-visual-1.md) | 2 PDFs | 21 | 0 |
| [Changed-source partition 2](english-encoding-visual-2.md) | 3 PDFs | 21 | 0 |
| [Changed-source partition 3](english-encoding-visual-3.md) | 3 PDFs | 20 | 0 |
| [Changed-source partition 4](english-encoding-visual-4.md) | 3 PDFs | 20 | 0 |
| [Unchanged-source continuity](english-encoding-visual-continuity.md) | 20 PDFs | 21 | 107 |

Every page of the 11 encoding-changed selections was individually inspected again. For the other 20 selections, every raster difference was inspected: the final source/revision/rights notice page in each document, plus the Philippine title page. The long title and issuer/language identification fit without an invented date. All final notices remain legible and share a physical page with source text or historical notes. No new clipping, overlap, missing-font box, stranded heading, or project-apparatus-only spill was found. Officiorum retains its accepted heading-chain repairs.

The encoding repair improves punctuation display while preserving substantial OCR word damage, broken words, intrusive citation lines and residual running heads. Literal square markers in Providentissimus, Tametsi and Vigesimo are retained source symbols rather than missing-font substitutions. The documented source-heading date discrepancies remain explicit. These qualifications prevent a layout PASS from being presented as a clean transcription, full historical print collation, verified translation, or official English text. The Philippine selection remains expressly abridged.

Original English review reports remain unchanged as hash-specific history. No PDF, source payload, manifest or renderer was changed during this renewed review. Installation, publication and deployment are separate steps.
