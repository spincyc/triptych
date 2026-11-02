# Independent cold review — encyclical refinements, packet 27

PASS for both assigned Latin readers: 2 PDFs, 13 of 13 reader pages individually inspected. No material source-boundary or layout blocker was found. Longinqua is unchanged and outside this packet.

| Reader | Document ID | Exact reviewed PDF SHA-256 | Pages individually inspected |
| --- | --- | --- | --- |
| Quinquagesimo ante anno | acta.aas.021.aas-021-l28668 | f088632ee71ade5e6a48bb14f187a23372db2f28065070dce8c9d995a4dac007 | 1, 2, 3, 4, 5, 6, 7 |
| Vehementer nos | acta.ass.039.ass-039-l000032 | a2bb45e3e258f7087070ec50f31dfa5f674a2534b33aa0402a0c366522f425b2 | 1, 2, 3, 4, 5, 6 |

## Byte identity, schema and replay

The two actual PDF page counts, selected-source hashes, receipt, frozen manifest, segment controllers, artifact metadata and retained source-note spec/geometry/source-review pins matched packet 27. Both source rows equal their matching frozen-manifest rows in full. The shared receipt is `c8c5cedca855916ebfed943a762e389f82af71428f126b342a6d6a82e1de481b`; the frozen manifest is `e05c8acb2ab97505ef91be1fb0d643fbb835e98dc56df97aa320160c24e4c49d`. All 74 recorded packet/input pin checks remained exact at the final recheck. Every listed reader and native raster matched both output and cache copies in size and SHA-256; raster availability supplied no inherited visual acceptance.

With `PYTHONDONTWRITEBYTECODE=1`, I independently ran each exact `tools/papal-source-notes check --spec <packet-pinned spec> --out <canonical selected text> --json`. Both returned exact replay success, preserving selected non-LF bytes and order. The current helper SHA-256 is `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`.

I independently imported the packet-pinned `scripts/_typeset_papal.py` (`1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`) and ran `validate_document(source_row, root=repo)` followed by `pdf_body_fidelity(pdf, validated, actual_pages)` for both documents. Both passed, matching the packet's fidelity results: Quinquagesimo 34,193 selected characters, 28,784 normalized characters and 195 permitted line-end hyphens; Vehementer 29,128 selected characters, 22,254 normalized characters and 74 permitted line-end hyphens. Source begins on reader page 1 and ends on the final reader page in both. `read_manifest` accepted the frozen manifest schema and selected controllers. A fresh `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0 tools/source-library validate` passed: artifact=10880, corpus=5, edition=14277, passage=9140, segment=10870, work=10925, bindings=4398.

An initial default-cache library invocation returned seven unrelated Aeterni ASS012 provenance errors. The fresh uncached PASS supersedes that result. Default loader cache hit versus implicit write was not instrumented; I performed no shared-cache cleanup or direct mutation, and disabled caching for the fresh validation.

`pdfinfo`, `pdffonts`, complete raw-PDF body extraction and the actual TeX logs were inspected. Every font is embedded, subset and Unicode-mapped Latin Modern. Titles, Latin subject and papal authors agree with the source rows. Creation and modification timestamps equal the pinned render revision, 2026-10-30T12:03:14Z. Both PDFs are unencrypted, have no JavaScript and have the expected letter page size. Quinquagesimo has no compile warnings; Vehementer has the two disclosed underfull hbox warnings (badness 1533 and 1226, source protocol lines 14–26), with no clipping or unreadable protocol. Neither log reports fatal, undefined-reference or overfull failures.

## Direct visual findings

I inspected both reader contact sheets, all 13 reader pages individually from the original full-resolution rasters, all four native excerpt contact sheets and native artifact pages 708, 714, 715 (AAS 21) and 14 (ASS 39) individually. Each image was transferred alone using original image bytes and automatic display detail. No page acceptance was reused.

Quinquagesimo's long literal identification and repeated historical protocol remain legible on page 1. Page 2 left visibly separates the literal `1 / I AC. I, 17.` note from the surrounding body. Page 4 left separately sets `1 / Nicolaus II, Litt. decr. Pastoralis sollicitudinis-` between the literal source divisions `perspe-` and `ctam`; page 4 right separately sets `2 / Litt. 10 febr. 1913` between `amis-` and `sione`. The source-page positions and word divisions remain literal. Page 7 retains substantial closing prose, the dating clause and `PIUS PP. X I` subscription before the terminal source apparatus and rights colophon.

Vehementer's substantive address/protocol is retained on page 1. Existing historical reference blocks on pages 2 and 3 remain distinct. Page 5 right visibly places `(ij Rom. XIII, 12.` and `(2) Act. v, 41.` in separate paragraphs after the body ending `Gallia;`, followed by continuing body. Sparse page 6 is source-bearing: it retains closing prose, prayer, blessing, dating clause and `PIUS PP. X`, then the source apparatus and rights colophon. It is not an apparatus-only page.

Across every reader page, the two-column sequence, paragraph starts, title/body distinction, margins, glyph rendering, page feet and terminal apparatus were legible. No clipping, overlap, missing-glyph box, body-note fusion or unreadable line was observed.

## Source inspection bounds and qualifications

The complete selected derived text was mechanically validated and compared to the PDFs. Direct source-text inspection covered the beginning/protocol, ending/subscription, and repaired LF note anchors. The selected derivative controllers cover Quinquagesimo LF 1–624 and Vehementer LF 1–500. Original parent note LF ranges are Quinquagesimo 28749–28750, 28981–28982, 29021–29022 and Vehementer 467–469; literal note text and empty LF records on both sides were checked, together with explicit TeX paragraph boundaries.

The exact complete native parent PDF hashes and each excerpt PDF hash matched. I independently replayed each parent-to-excerpt page mapping: complete `pdftotext -raw` bytes and ElementTree-serialized `-bbox-layout` page elements matched the packet hashes and one another. Page dimensions and every recorded bottom-line text/bounding box matched the native PDFs. Native inspection confirms the four repaired groups are smaller references below their last body lines, separated vertically. The retained source/geometry reviews were read and their pins checked; earlier selection decisions and all excluded interior gaps were not independently re-adjudicated here.

This PASS accepts these exact mechanical readers and the bounded LF-note repairs. OCR spelling, spacing, interrupted words and reconstruction defects remain disclosed. Native Vatican OCR PDFs are reconstructions; this review does not claim original-print facsimile identity, whole-work lexical collation, translation accuracy, a new historical witness, new rights clearance, installation or deployment approval. Any separately assigned source-intake or identity gate retains its own scope.
