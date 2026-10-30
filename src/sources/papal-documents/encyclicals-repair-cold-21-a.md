# Independent repair acceptance: packet 21-a

PASS for all three assigned Latin readers, 24 pages total. Every reader page was inspected in the contact overview and opened individually at full raster size. No prior review was adopted or counted as page reuse. No clipping, overlap, column-order defect, sustained unreadability, fused source-note/body block, or apparatus-only final page was found.

This is independent reader usability and repaired source-boundary acceptance. It does not certify lexical OCR accuracy, translation accuracy, original-print collation, whole-book completeness, or rights. Native witnesses are Vatican OCR reconstructions; they are not original-print facsimiles.

## Exact reviewed bytes

Packet SHA-256: `fff5628607dd6bf8e19c2d756c89f563992a48b8b8d2bac83bc0a4e442a4a360`. The common brief hash and all 57 packet PDF, receipt, frozen-manifest, source, segment, controller, recipe/spec/map/review record and retained-payload pins matched. Each complete frozen source row equals its packet row. The receipt source/PDF hash, segment, extent, render revision and actual PDF page count agree. Metadata titles and named issuers match these source selections; all subjects identify Latin. The two unresolved act dates are omitted from identification rather than called undated. Every font is embedded with Unicode mapping. `pdfinfo` parsed all PDFs successfully; `qpdf` is unavailable and its syntax check was not run.

| Reader identity | Pages actually inspected, contact and full size | PDF SHA-256 | Receipt SHA-256 |
| --- | --- | --- | --- |
| `acta.ass.010.ass-010-act-001` (la) | 1–14 | `f0eca7f4a5b8884649daa93363c0798d94a64458eb26abe68940836388a1b72c` | `a82c99d6e0411906ec1ea3c713a6b1a6a5430ba4a42b62072a3ce6aff434b8cc` |
| `acta.aas.015.archive.aas.015.l002026` (la) | 1–6 | `f6f8bd3c94c487e4a13d1858505c131f8de2788f007bdf7d35f8f3266aeee1d4` | `8d475409e97bd34e281ac99d24a8094e0c4cb1aefb6d2748abc5e622f6a1f10a` |
| `acta.aas.012.archive.aas.012.l008747` (la) | 1–4 | `7d2360c0f404166a03278091f3da2982f16d0f80b50dab9c8c5f9187d93cc862` | `de0b9daaf706e0e11740d1e0bc51f9877ee22bc8fc0d6136075300725db6e7bd` |

## Method and source replay

All three registered LF partition commands were replayed with `tools/papal-source-notes derive --spec <packet-pinned spec> --out .scratch/cold-repairs-21a/replay-N.txt --json`. The current helper hash is `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`. Its hash checks, ordered selections, explicit note bounds and LF-only construction were read. Every replay reproduced its exact retained output, selected non-LF digest and order-preservation result. Each spec uses the same ranges and controlling artifact/hash as its retained predecessor segment; no selection expansion or contraction occurs.

The archived native-spacing helper was read and executed directly through `replay(recipe, repository_root)`, with the checkout scripts on the import path. Exact helper hash: `b67f55a5075a11a43f23766d477b32c5209a1144262790476e31c4fde2362b49`, retained at `src/sources/works/holy-see/acta-sanctae-sedis/editions/1890-acta-ass-023/artifacts/native-spacing-helper-b67f55a5075a/helper.py`. This independently reproduced the ASS 10 spacing output `1d29bf463a27ab030f5dd8bf5c326719fa8f60a1623b7085b77d4839a24d76bf` and all 1,213 registered map rows exactly, with stream-order differences only on original artifact pages 10 and 12. Each eligible source line uniquely matches its same-page native line after whitespace removal. The four zero-match records remain literal. Native raw extraction was independently regenerated from exact parent artifact pages 3–37 and matched `c6fd3fbf6840d52117487452a6371ba14713f12c6d8e54fb1b00008dcde9ae06`.

The repository PDF body-fidelity function was independently executed against each exact selected source payload and PDF. All passed `pdf-raw-source-aware-line-hyphen-nfkc-v3`: declared whitespace/Unicode normalization and only source-aware line-ending discretionary hyphens; 355, 136 and 94 added layout hyphens respectively. Source coverage begins on reader page 1 and ends on the actual final page in each case. This mechanical check does not establish linguistic accuracy.

| Reader | Exact partition spec SHA-256 | Replayed selected source SHA-256 | Historical note groups |
| --- | --- | --- | --- |
| `acta.ass.010.ass-010-act-001` | `74ca6f6d452e1ca133b15e635e115b232842d41a0883d386e98c22b756f68339` | `ccbcb0ce6c7e956a61b39b4174c3eb61a9d802bf8dc764f6045ba99b532ca080` | 11 |
| `acta.aas.015.archive.aas.015.l002026` | `28a7c5f9fa40715bccb7a58c76e676381d79d3c39082b4ca98550b0075a54c03` | `5e7ca2997a67d35f19f9692bc6e5f4f38a5966dc0226925b9337ac370c6eaf9d` | 7 |
| `acta.aas.012.archive.aas.012.l008747` | `e3227c7681e3fbedebeef1f37eb6e9225b14b4ba98c1d12473bfab02de1b48f0` | `685ae00f71212d5815dbaf2d36c05fb7cb67af24efb9314d94f0c3ed0773770d` | 10 |

## Independent native and rendered-page findings

Native excerpt offsets were checked against source maps/reviews and exact full-parent hashes, not inferred from thumbnail labels. Bounded `pdftotext -raw` extraction from each parent equals its respective excerpt text. All inspected reader/native raster files match their cache manifests. Existing rasters were opened read-only; no PDF, source, cache or canonical report was changed and no renderer was run.

| Source | Exact parent PDF SHA-256 | Original artifact pages in native contact overview | Original pages opened full size |
| --- | --- | --- | --- |
| ASS 10 / Quae in patriarchatu | `5e4948a4a916d488169fb7dd5822b05f6d40872c7865f970c6f5fb892fb2ab65` | 3–37 | 3, 7, 10, 12, 13, 15, 16, 18, 20, 22, 24, 31, 32, 36, 37 |
| AAS 15 / Rerum omnium source heading | `acab305a3df26a4fe1dfe3c37c9287d8a180b40ba4690a2a2a4239fbb779d33e` | 49–63 | 49, 50, 52, 53, 54, 55, 57, 60, 63 |
| AAS 12 / Pacem Dei source heading | `213147b403a66e191d125ef059e48098d26afd750af4327724ca31036c495813` | 209–218 | 209–218 |

**Quae in patriarchatu: PASS, reader pages 1–14.** The first page gives a compact title, Pius IX, known act date and Latin; body follows immediately in two justified columns. All eleven source-note groups occupy distinct page-foot regions in the native witness and independent paragraph blocks in the reader. Original note pages 7, 10, 12, 13, 15, 16, 18, 24, 31, 32 and 36 correspond to reader note blocks on pages 2, 3, 4, 5, 5, 6, 7, 9, 12, 12 and 14. The native pages with raw-stream differences (10, 12) have one body column plus separate footnotes; retaining source layout-LF order is supported. Original pages 20 and 22 explain the unchanged zero-match body/reference-layout records. Literal hard hyphens, split words, malformed glyphs, isolated characters and displaced reference figures remain visible and reduce reading comfort, without sustained unreadability. The sparse final page 14 retains continuing body, a separate historical note, blessing, dating clause and PIUS PP. IX subscription above a rule and compact apparatus. Original page 37 independently supports that ending.

**AAS 15 Rerum omnium source heading: PASS, reader pages 1–6.** The long literal heading fits, followed by Pius XI and Latin, with no unresolved date inserted. All seven native footnote groups are single-column page-foot notes. Original note pages 50, 52, 53, 54, 55, 57 and 60 correspond to separate reader blocks on pages 1, 2, 2, 3, 3, 4 and 5. Hard-line word fragments, detached reference figures and occasional spaced letters remain literal but usable. The sparse final page 6 contains genuine continuing source text, blessing, the historical January dating clause and damaged OCR subscription before ruled apparatus; native original page 63 confirms the same damaged subscription. Acceptance does not correct or certify its lettering.

**AAS 12 Pacem Dei source heading: PASS, reader pages 1–4.** The long literal title, Benedict XV and Latin fit. All ten original pages carry distinct single-column page-foot note groups, with no marginal/body mixture or interleaved note columns. Original pages 209–218 correspond to reader note blocks on pages 1, 1, 2, 2, 2, 3, 3, 4, 4 and 4. Each LF group was checked with adjacent raw records and against native placement. The duplicated/detached reference figure on original page 210 and isolated quotation mark on original page 218 remain literal, visibly separated where partitioned. Hard hyphens and OCR fragments remain usable. Reader page 4 retains body, blessing, dating clause, BENEDICTUS PP. XV subscription and final historical notes before the ruled project apparatus; original page 218 supports the source-bearing ending.

No blocking changes are requested. The source notes on the final pages accurately keep the mechanical OCR and non-collation limits visible. The review does not expand source evidence states or supersede existing provenance/rights judgments.

Detailed command results, exact source-row comparisons, native parent/excerpt and raster integrity, LF preservation checks and page logs are in `.scratch/cold-repairs-21a/verification.json`; the inspected LF note records and immediate context are in `note-loci.txt`. The report is intended for exact-byte copying by the coordinator to `src/sources/papal-documents/encyclicals-repair-cold-21-a.md`.
