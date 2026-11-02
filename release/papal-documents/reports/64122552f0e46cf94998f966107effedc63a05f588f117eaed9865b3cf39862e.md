# Independent cold review — packet 37

**SOURCE RECOVERY: PASS, bounded to the two declared quotation tokens.**
**PDF: PASS, one English reader, all 8 current pages freshly inspected.**

The reviewed work is Leo XIII, *Divinum illud munus*, historical English chapter *The Holy Spirit*, ID `papal.leo-xiii.hf-l-xiii-enc-09051897-divinum-illud-munus`. This acceptance concerns the exact new source and PDF below. It does not retroactively accept the predecessor source, PDF, or held review.

## Exact inputs

| Input | SHA-256 |
| --- | --- |
| Packet 37 | `f4bb55a4f045baf5897ea435fb250aa7d1c8935be7534bf6aee7dd1c10faa102` |
| Current selected source, 36,438 bytes, 163 LF-delimited lines | `ba3ad11b1ec60e61cbd795d6ecabd15dfb13fce21c02c218f63c852f636447fa` |
| Current PDF, 63,945 bytes, 8 pages | `3cb96b0916cdac84f454320046526c3292a3099a49016f0062934239eeb847f3` |
| Current receipt | `b8891ceec90545b36b6b9a763abe647c1381b41c51cefaf736269cb0baef0fa5` |
| Frozen/source-selection manifest | `2717639208b3bc43ebb6e1fd233022114dd862e6fb3d7af33d3b5939220ad059` |
| Retained quote recipe | `515043936327c67617dfc1d1a697d6d7471a9e35f20cdc4c9fec96a14c734e45` |
| Retained native/OCR evidence ZIP | `c40a614cc0deb4b209b0802c739bfe60652703a9b94706151d0a9a9711a997f7` |
| Duquesne whole native PDF | `f422eae464c648326b8cf9063f6147ef56b2a5f5d8f7c739015505e76f435c05` |

The packet source row equals the matching frozen manifest row in full, and equals the proposed replacement row. Segment metadata and all 47 packet ancestor-artifact metadata objects equal their current TOML records. Their record/payload hashes, byte extents, schema/controller relations, recipe and helper pins, receipt links, producer-evidence pins, and raster/cache pins checked successfully. Verification records 199 successful pin-check instances, including repeated references. These are identity checks; author production review supplies no independent visual acceptance here.

## Bounded SOURCE RECOVERY decision

I read the retained standalone MIT replay implementation before executing it into this review's exclusive scratch. The exact held input is `05fccc3f45dcf497469491527999a6f0d3a8329cede1f3455f1536cdc15db75f`. At selected source LF121, corresponding to parent LF2729, only these zero-based half-open byte spans change:

| Held span | Held token | Exact raw `context-ocr.txt` slice | Recovered token |
| --- | --- | --- | --- |
| `[30297,30305)` | `helier>e` | `[146,153)` | `believe` |
| `[30336,30342)` | `sJiall` | `[184,189)` | `shall` |

The guarded replay verified source and evidence hashes, all nine ZIP evidence-member hashes and sizes, original token/context bytes, exact raw OCR slices, surrounding full-page/context OCR agreement, TSV rows and confidence, output size/hash, and LF count. A separate construction from unchanged byte intervals and the two raw slices equals the current source. Every other byte is exact, including punctuation, whitespace, historical-note boundaries and all 163 LFs.

I independently rerendered actual Duquesne parent PDF page 443, printed page 437, at the retained 3,600-pixel scale. Its PNG SHA-256 is `417a39d3bada73fb8f4bb69295c417042806a000342928ecd7db9705c62079d1`, exactly matching the packet. Rendering the ZIP's native one-page excerpt yields identical PNG bytes. Context crop `1880x400+150+1350` and tight crop `1880x245+150+1440` both match the retained crop pixels exactly, absolute error zero. Independent JPEG quality-95 conversions reproduce all three packet review-JPEG hashes. No fresh `pdfseparate` byte-equality claim is made; random PDF IDs are immaterial to the proved raster equality.

I freshly viewed the actual full native page, its context crop, and its tighter crop. The italic printed glyphs clearly read **believe** and **shall**. The context and full-page OCR word boxes agree after translation by `(150,1350)`:

| Token | Context `(left,top,width,height)` | Full native box | Confidence |
| --- | --- | --- | --- |
| believe | `(694,110,178,52)` | `(844,1460,178,52)` | 96.299927 |
| shall | `(63,188,128,48)` | `(213,1538,128,48)` | 95.861137 |

The tighter crop's raw OCR reads `belveve`; that contrary recognition remains retained and was read. It does not outweigh the direct glyphs and matching full-page/context recognition and geometry. No OCR rerun or model-supplied wording entered the source replay.

I also independently replayed the inherited boundary recipe `7e4b9463904b9fc4df65e636c9442d6ad9f6b34e6603e7ff4bf9b214a7ddc304` to the exact held source. I rendered and viewed both pages of the pinned native excerpt `e378aa5f2cdf10f3169dc4a59605e0a53e71a5a5b668ddd122709a5cda3c8989`: parent 439/printed 433 shows the running head above the body beginning “present and exists”; parent 441/printed 435 shows the note numeral `vi`. This corroborates the inherited 16-byte running-head exclusion and two-byte numeral recovery. It does not enlarge the new two-token aperture or certify the older encoding repair across the whole chapter.

The prior PDF `8fdc6e4203514ae85f7befaa9cd8fbff6ad8d2942d4a0e8852a2680f5d793f8d` still matches its held bytes. Its prior report `1f4403d2cf0b87f43c04f7bba079daddcfebadb36b6d1c81ce2893fac02dd817` and review remain **CHANGES_REQUIRED**. Their original malformed-quotation finding is resolved for the new bytes only.

## Current PDF inspection

I opened the packet's exact contact sheet and then every current full-resolution page raster, pages **1, 2, 3, 4, 5, 6, 7, 8**, separately in this review. No page or judgment was inherited. Raster-cache reuse is only reuse of hash-checked images. The packet cache receipt, renderer fingerprint, PDF identity, and all 17 image files in each of the output and cache locations match.

| Page | Fresh visual finding |
| --- | --- |
| 1 | Title, pope, act date and English label clear; substantive opening follows directly; ordinary two-column continuation and separate historical-note paragraphs remain legible. |
| 2 | Columns and all-capital source heading fit; historical references remain separate from adjoining body paragraphs. |
| 3 | Incarnation/Church material and heading read in column order; the historical note blocks are visually separate. |
| 4 | Souls-of-the-just heading fits without clipping; reference blocks and body continuation remain distinguishable. |
| 5 | The excluded running head is absent before “present and exists”; body and note blocks remain legible in their retained order. |
| 6 | Recovered `vi` reference and both corrected quotation tokens are visible; no clipping, overlap, missing glyph or quote layout problem. The separate literal `De\it.` reference remains an inherited OCR qualification. |
| 7 | Separate historical folio/running-head paragraph `438 THE HOLY ... SPIRIT.` is retained before the continued body; it is not fused into that paragraph. The source closes with the Apostolic Benediction and retained notes. |
| 8 | Sparse but source-bearing: historical notes [2]–[4] precede the ruled Source apparatus and compact rights colophon. The page is not apparatus-only. |

No material layout blocker was found. Paragraphs, headings and source notes remain distinguishable; columns preserve normal left-then-right order. Historical notes interrupt some continued source sentences at retained source-page breaks, including pages 1 and 3. Their actual separate paragraph boundaries were checked; this is a disclosed source-order limitation, not newly fused typesetting. Original OCR word divisions, distorted reference marks and spelling remain visible throughout, rather than being silently corrected.

The current TeX log contains only the declared underfull hbox, badness 3219 at lines 171–172; no overflow, undefined-reference or fatal-error entry was found by the focused log scan. PDF metadata identifies *The Holy Spirit*, Leo XIII, and English, with the declared revision instant. `pdfinfo` confirms eight unencrypted letter-size PDF 1.7 pages. All four font resources are embedded subsets with Unicode maps. No size-review threshold is reached.

## Independent mechanical checks and limits

All source-library invocations and Python imports used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`. A fresh uncached whole-library validation succeeded: artifact=10894, corpus=5, edition=14277, passage=9140, segment=10873, work=10925, bindings=4398. This is a current successful run, not the predecessor's historical sibling-error result. Schema 2 and its artifact `page_count` support were accepted by the actual validator. The frozen-manifest `typeset-papal check` independently returned valid.

Using the pinned current `scripts/_typeset_papal.py`, I independently called `validate_document` and `pdf_body_fidelity`. Result: **pass**, method `pdf-raw-source-aware-line-hyphen-nfkc-v3`, 36,408 source characters, 29,680 normalized characters, 33 permitted layout hyphens, source coverage pages 1–8. This proves mechanical source/PDF fidelity within that method, separately from native-glyph judgment.

The bounded repair and basic reading-layout decisions pass with the stated qualifications. This review does **not** certify full-print lexical collation, translation accuracy, every inherited OCR word, the historical heading's May 4 date against the catalog's May 9 date, whole-source completeness against a full native printing, or new rights clearance. Direct native inspection here reaches only Duquesne parent pages 439, 441 and 443 and the stated quote crops. The source and apparatus continue to disclose their broader transcription limitations.

Only this review's exclusive scratch was written. Source/canonical/producer files, manifests, shared caches, PDFs, installed outputs and Git state were not mutated. Canonical target `src/sources/papal-documents/encyclicals-refinement-cold-37.md` remains unwritten by this reviewer; root owns copying these exact report bytes and subsequent integration.
