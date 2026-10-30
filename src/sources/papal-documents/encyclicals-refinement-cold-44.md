# Independent cold review: packet 44

Review date: 2026-10-30. Intended canonical report: `src/sources/papal-documents/encyclicals-refinement-cold-44.md`; that target was left unwritten by this reviewer.

Both current PDFs **PASS**. Separately, the bounded Non mediocri whitespace/source-readability repair **PASS** and the Superiore metadata/apparatus-only repair **PASS**. These decisions cover the exact replacement bytes below. The superseded failed PDFs and earlier failed review retain their original dispositions; no earlier visual inspection was reused.

| Document / identity / language | Exact PDF SHA-256 | Pages freshly inspected individually | Separate repair decision |
| --- | --- | --- | --- |
| Non mediocri cura / `acta.ass.026.ass-026-l07953` / `la` | `61b25f717f5a0f46cba310af332d4b9f6192eaf43d611637e13d4e094732688e` | 1, 2 | PASS: bounded whitespace repair and restored readability |
| Superiore anno / `acta.ass.017.ass-017-act-001` / `la` | `0337c3c87ba589e44a514c6d45496139e875d8e5d1a4c45c9f9ab8d18b4273c3` | 1, 2 | PASS: explicit OCR characterization, unchanged source body |

All four current reader pages were viewed freshly at full raster resolution, as were both reader contact sheets. All five Non mediocri native OCR pages 199–203 were viewed freshly at full raster resolution. Each image was opened separately with original MIME/resolution and automatic display detail. No visual review was inherited, no page reused, and no new raster render or cache mutation was performed. Actual coverage was persisted during review in `actualcoverage.json` under this packet's exclusive scratch.

## Exact inputs and verification

The packet SHA-256 is `da1807befbe281e9214b592a30210695fe5f873a2bc81b6cb06262101d34a3c9`. Its cache-disabled brief matched `6a1aa4da7df4b21b53617a1065405644d5f3ae08fccb0e02adbbb3fbe08d221d`. The common receipt matched `4ca4333db336ffc87589cb0a25ae6c430c6ce0a7a4dcb3073312941568b208b8`; the frozen manifest and input selection manifest matched `33357111aa334696957a25424e3561eca0029f7d881aed64d514b57a79c76117`.

Complete source rows equal their matching frozen-manifest rows and the proposed-current rows. Receipt identities, source hashes/ranges, output hashes, page counts and render revisions agree. Every pinned segment and artifact TOML parsed equal to the packet's complete metadata object. Packet/controller/recipe/payload/helper/producer-evidence/raster/cache pins, including actual cached and delivered raster sizes and hashes, matched. Final input rechecking covered 148 pin checks, including repeated shared pins. Exact checks and page-specific native proof hashes are retained in this review's `verification.json`.

| Current source | Complete controlling text SHA-256 | Selection |
| --- | --- | --- |
| Non mediocri | `da68d4ac35e8f3774a24f8dda673f42449e3cb41e76ccf21a7a99341a4c59fdf` | New derivative LF 1–155 |
| Superiore | `94e21c27a3d1a5f07bb02b85a3c0ccd908c29f4894a55b603eecd43b165c8902` | LF 1819–1863; 1866–1906; 1908–1944 |

The selected segments matched `c2bf74297b655c1e81768e3a107a383d534963b904e721fb10cf085c308bf82f` and `0e35b5dbb3cb2030df63aff4fc52cc921b58e0416811c576ed728d26837baf6d`, respectively. The controlling records retain their artifact-specific United States public-domain bases and excluded-wrapper boundaries. This review checked those exact recorded bases and their source identities; it makes no new rights adjudication, printing-date determination, or original-print verification. The ASS 17 printing-year uncertainty remains explicit in its source record.

Every Python import and source-library invocation used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`. Current uncached `tools/source-library validate` exited 0: `artifact=11108 corpus=5 edition=14304 passage=9532 segment=10882 work=10944 bindings=4398`. No shared library cache was read, filled, removed or restored by the review's source-library invocations.

## Non mediocri: source repair PASS

The complete parent native PDF matched `02f81d1d13781d2f7d27d4aa327d7ec83bbe5ea8ec22f785eda20dd4ce777446`. A fresh complete `pdftotext -layout -enc UTF-8 -eol unix` extraction reproduced `a8cd732f0494656ff44e5b26d7f8645736ab91509f3822d6ff7ca391046733ec`. Replaying its declared whole-volume wrapper exclusions reproduced the predecessor historical text `15a33cfd01401e070c0b912e4154be4f7d163d6730ac8f1cd64ed6096d756d3d` exactly.

The bounded fresh `pdftotext -bbox-layout -f 199 -l 203 -enc UTF-8` output reproduced retained bbox `439437c317351f32b3d25891abde92ad7ebdd0fde1a985fefbbe396d4275b70b`. For every supplied single-page native excerpt, parent page 199, 200, 201, 202 or 203 was independently compared with excerpt page 1. Complete `pdftotext -raw -enc UTF-8` stdout bytes were equal and nonempty. The bbox page elements were byte-equal under the documented `ElementTree.tostring(page)` default serialization, including the tail. Independent WORD value/coordinate comparisons were also equal. Thus the inspected excerpt rasters have proved parent-page mappings; producer assertions were not substituted for this proof. Exact per-page raw/bbox hashes and WORD counts are in `verification.json`.

The source-specific preparation code was read before execution and its recorded MIT license checked. Running exact retained code `5ceeff1a55cca986b83d5926210d2701f1e16af740e13ee9ae4ff5410052bf87` against the pinned bbox into this review's scratch reproduced native word-line witness `993d6853bb1852f51675dcd96537c4f77be51b182235a5d7606934153dad627f` and geometry map `4a337059f206f0fc7ca910dbd7911c2ec096901e49106f72e79a773489aa0575` byte-for-byte.

An independent XML/coordinate cross-check also accounted for every one of the **5,973 native WORD objects exactly once**, with values and coordinates unchanged. It verified all 192 grouped native lines, their x ordering and each inter-WORD gap, reconstructed every line/page byte, and checked LINE membership within the 0.5-point y tolerance. Actual fragments in a group shared the same y anchor; the smallest separation between groups was 1.366 points. There were 4,478 joined inter-WORD gaps and 1,303 separated gaps. The largest joined gap was **1.93050 points**, the smallest separated gap **2.93931 points**, with no gap inside that interval. The **2.5-point threshold** falls within this clear interval. This is a geometrical whitespace determination without inferred or corrected source words.

The current native-spacing helper matched pinned SHA-256 `7c7393f6b366bc986e7d106d217a769fabba5a48edd645a7bd02b463eb64d82c`. Replaying recipe `8fb696268e8df9f88c9cedeb08cd96c103b8d69b5a6b835f45088da029355e7b` into reviewer scratch reproduced the current source exactly. Its source-to-native map equals retained map `0a1de657d6d91013a6a1e9cbd08b719d6b66d3356ea480de6afcd0346f54709a`: **143 selected nonblank LF lines have unique native matches; zero retained-original exceptions; zero stream-order exceptions**. The independent cross-check confirms all nonwhitespace characters, selected range order, original LF/blank boundaries, literal hard hyphens and note separation remain unchanged. The five predecessor selections are LF 7948–7955; 7957–7998; 8000–8040; 8042–8081; 8083–8102.

Fresh native observations establish the bounded ownership and note judgments. Page 199 ends a preceding act with its own subscription, then separately begins this act's title and incipit. Page 200 has the distinct historical note (1) at page foot; the note remains its own paragraph in reader page 1, followed by the page-201 continuation `implevere.`. Page 201 ends with literal `At-`, retained before page 202's `qui` continuation. Pages 201–202 have no additional notes. Page 203 retains the blessing, dating clause and papal subscription before the distinct `EX S. CONGREGATIONE CONCILII / ANDRIEN.` instrument. Neither adjacent act enters the current selection; no additional boundary note was found in the inspected five pages.

Fresh reader inspection confirms that the former sustained letter-by-letter fragmentation no longer impedes continuous reading. Remaining hard hyphens, their source spacing, and isolated OCR name/glyph anomalies remain disclosed witness limitations. This repair establishes neither lexical accuracy nor original-print glyph identity: the native PDF is an **archival OCR reconstruction**.

## Superiore: metadata/apparatus repair PASS

The current source row differs from the prior frozen row only in **`source_note` and `revision`**. Artifact identity, complete source hash, segment, exact ranges and source text are unchanged. The selected source text and old/current generated `.body.tex` bytes are exactly equal; the body TeX hash is `51de565b6a291c770a9482114c185424d8dd115de531321ab7344973130a6bdd`. Source/PDF fidelity also passes independently against the old PDF's unchanged body.

The complete native parent PDF matched `118157e6dd95aa54268c18f116ca4a290c3262909e847da008e0b4869963e9dc`. A fresh whole-volume layout extraction reproduced `5910f5f15ac33394dc76d6ff3ca20793f04242ef72c8f1e16a888efce426af05`; the declared historical wrapper exclusion reproduced the current `94e21c27…` payload byte-for-byte. This is an exact derivation check, without a new visual or lexical collation of native ASS 17 pages.

Fresh reader page 2 explicitly identifies **archival OCR text reconstruction**, mechanical extraction with pdftotext, retained OCR spelling/spacing, and the absence of original-print facsimile collation. It displays revision `2026-10-30T16:58:32Z` once. The previous metadata blocker is therefore closed. The inherited spaced protocol/address, literal source hyphens, damaged Roman year, `Jais`, and `Apostoli- ' eae` remain visible and disclosed; this apparatus repair does not claim to correct them or admit a new source.

## Current reader-page decisions

| Reader page | Fresh full-resolution observation |
| --- | --- |
| Non mediocri 1 | Compact title, pope, date and Latin identification. Readable word spacing, normal left-column then right-column continuation. Historical note (1) visibly occupies a separate paragraph. No clipping, collision, overflow or glyph-loss blocks. |
| Non mediocri 2 | Substantial body in both columns, blessing, actual date and `LEO PP. XIII.` before the short terminal rule. Source/OCR qualification, revision and rights colophon are readable and separate. No apparatus-only page. |
| Superiore 1 | Compact identification, complete original protocol/address, dense but legible two-column body in normal reading order. Source letterspacing and hard hyphens remain literal. No clipping or overlap. |
| Superiore 2 | Substantial continuation, blessing, date and papal subscription precede the terminal source notice. The corrected OCR characterization is readable. The compact common colophon continues at the top of the right column on the same physical source-bearing final page; no spill page or collision. |

Independent `validate_document(source_row, root=repo)` and `pdf_body_fidelity(pdf, validated, pages)` calls used current typesetter `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`. Both returned `pass` and exactly matched their receipt fidelity objects under `pdf-raw-source-aware-line-hyphen-nfkc-v3`. Non mediocri has 8,627 selected source characters, 7,468 normalized characters and 58 layout hyphens; Superiore has 7,011, 5,855 and 33 respectively. Both source bodies start on page 1 and reach page 2. This check preserves original source hyphens and permits only declared source-aware physical-line-end additions, whitespace and Unicode compatibility normalization; it does not independently establish word segmentation.

PDF metadata identifies the correct titles, Leo XIII and Latin source editions. Both raw creation/modification dates are `D:20261030165832Z`, equal to the tracked render revision. Both are two-page, unencrypted US Letter PDFs, without forms or JavaScript. All listed Latin Modern fonts are embedded, subset and Unicode mapped. PDF sizes are 31,001 and 28,775 bytes. Complete final logs and second-pass outputs contain no fatal errors, undefined references, missing-character, overfull, underfull or unresolved warning findings. Raw text extraction and visible column continuations support normal reading order.

## Preservation, scope and disposition

The earlier failed Non mediocri PDF remains `8db27bb4d6f817fca420a5781984a5bf2919bbad482cbc9fbedaccc95d235a91`; the earlier failed Superiore PDF remains `d2bc466686ca280ffb535383356753563339aa9e8841c1dc95650225cbbba37b`. Their frozen input, receipt, old segment and source pins remain intact. The old independent report remains `0552ec6dd51b8b102ccd49919dc46eb5f66845c23f64bc16badf1b23942c8470` and reviews remain `1cb80e1b747c3342d8ddf4b9e22cd753169a98d9fa4bab7cd107e67316dfa78c`; their CHANGES_REQUIRED judgments are not retroactively changed.

No material source-repair, metadata or PDF-layout blocker remains within this packet's assigned scope. These are bounded repair and every-page PDF decisions, without whole-print lexical collation, original-print facsimile identity, translation review, independent rights clearance, whole-volume inspection, new source intake, installation, admission or deployment approval. Superiore native pages were not freshly viewed in this review; its independent repair decision rests on exact unchanged-body/controller comparison, truthful current apparatus and all current reader pages. Non mediocri's native inspection covers all five identified reconstructed pages, not the historical original printing.

All review-created files remain under `.scratch/encyclical-refinement-package/cold-review-44/`. No source, producer output, manifest, shared cache, installed PDF or Git state was edited. The coordinator owns canonical copying and admission. No generic handoff directory or ZIP was created: this lane produces the requested review report, structured decisions and verification evidence only.
