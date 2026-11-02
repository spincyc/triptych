# Christi Nomen — independent classic-reader review

2026-10-30. **PASS** for the exact two-page Latin reader identified below. Both reader pages were freshly opened individually at original raster resolution. No inherited page inspection, previous acceptance, or contact-sheet-only coverage is claimed. No blocking layout, source-extent, paragraph-fusion, note-fusion, or source-to-PDF fidelity defect was found.

Canonical report target: `src/sources/papal-documents/encyclicals-direct-baseline-recovery-f.md`. This scratch report is the deliverable for coordinator integration; no canonical source, manifest, PDF, release record, helper, shared raster/cache, or Git state was changed by this lane.

## Scope and selected witness

Document `papal.leo-xiii.hf-l-xiii-enc-24121894-christi-nomen`, language `la`, title *Christi Nomen*, Leo XIII, dated 1894-12-24. The selected input is the retained normalized Vatican web transcription, not a newly reconstructed ASS text. Its visible terminal apparatus says “Uncollated normalized web transcription” and identifies *Acta Sanctae Sedis* 27 (1894–1895), pp. 385–387. The controlling artifact and publication approval further disclaim a facsimile, diplomatic or critical edition, corrected text, and full-work image collation. Those disclosures govern this PASS.

Source URL: <https://www.vatican.va/content/leo-xiii/la/encyclicals/documents/hf_l-xiii_enc_24121894_christi-nomen.html>. The review used retained local bytes and records; it did not fetch or authenticate a current web revision. The exact restricted HTML parent is identified by its recorded hash; parent HTML bytes were not locally re-collated.

The publication approval records exclusion of the modern bibliographic block `*ASS, vol. XXVII (1894-1895), pp. 385-387.` and its title asterisk. The source heading remains. No historical note or substantive body omission was identified by the bounded native checks below. Rights review here confirms the existing affirmative historical-wording basis and its matching input pins; it does not extend that basis to the restricted HTML or native PDF wrapper.

## Byte identity and machine checks

| Object | SHA-256 |
| --- | --- |
| Assigned packet | `23e764d1e28ae53024cc8dfab312cccbe0a9f02271f4b1ff5637c2bb4d40f1b0` |
| Reviewed PDF, 27,438 bytes, 2 pages | `390c577d4376d2e2a8282b2b0465a24e1aaf96a475d12d5869812f5467a75125` |
| Whole receipt | `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e` |
| Frozen manifest | `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342` |
| Source text | `ac616c2012273afd8e6402ee0db553132c24cc7325e866d1a383df1c511323cf` |
| Controlling normalized-text manifest | `3e7b2fbdea4e296ca4528ce25cb3cb4ddb82a714e709b52e9330b387ffa7d238` |
| HTML parent manifest | `2f453fbee9ae1245e4034f2504b9f20684110d3c447049e2eec4c83796b21726` |
| Recorded restricted HTML parent | `c53b3cd3513d885cd0d87e0eeba3e4c4ba3f9a311368770a4a4c1782521e6f31` |
| Shared raster run manifest | `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02` |

The **whole** frozen-manifest source row equals the packet's `source_row`, and the **whole** receipt document equals `receipt_row`; this was not a selected-field comparison. Source identity, source payload, both controller manifests, receipt, frozen manifest, raster-run source/hash/page count, and every file hash/size in the reader's raster cache manifest were checked. The assigned baseline packet's matching document identity and prior checkpoint reference hash were checked without inheriting their inspection or judgment. There is no selected segment controller for this web reader.

Read-only fidelity was rerun with `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python`, `sys.path.insert(0, 'scripts')`, `validate_document(row, Path.cwd())`, and `pdf_body_fidelity(Path(pdf), validated, pages)` from `scripts/_typeset_papal.py`. It passes with exactly the receipt result: method `pdf-raw-source-aware-line-hyphen-nfkc-v3`; 6,344 source characters, 5,488 normalized characters, 41 layout hyphens, source first page 1 and last page 2. This check allows declared whitespace/Unicode compatibility treatment and source-aware line-end layout hyphens; it does not establish historical correctness of the selected words.

The complete `.log` (482 lines), `.pass-1.txt` (79 lines), and `.pass-2.txt` (69 lines) were read. Pass 1 has the ordinary PageLabels, label-change, and outline rerun warnings. Pass 2 resolves them. The final log and pass 2 show no fatal error, undefined reference, missing character, overflow, underfull box, or unresolved warning; all three records terminate with a two-page output. Their hashes are respectively `9274695423481197a79d38eba50404af5528e8a1cbffd836ad874d61d47c4a7a`, `bc1c833ea9bf160f4aab3bc2e8697cfe7ec4863133dd5b787050bf31680c85ca`, and `d008f23ab900e5c4ca52860f8c9d01980cd32c9626195312ee3b54c2b04913bd`.

`/usr/bin/pdfinfo`, `/usr/bin/pdffonts`, and `/usr/bin/pdftotext` in both `-raw -enc UTF-8` and `-layout -enc UTF-8` modes ran successfully. The PDF is unencrypted PDF 1.7, US Letter, with no JavaScript or forms. Metadata names *Christi Nomen*, Leo XIII, and Latin; creation/modification dates correspond to revision `2026-10-30T02:56:48Z`. All four Latin Modern font subsets are embedded and have Unicode mappings: Roman 17 regular, Roman 10 regular, Roman 8 bold, and Roman 8 regular. The PDF is untagged; no accessibility-conformance certification is implied.

Raw extraction follows the entire left column and then right column, followed by the next page. The page-1 column transition `colla-` → `tis diligenter` and page transition `moderato-` → `ribus eius` agree with visual reading. The layout extraction was also read and shows the expected physical two-column arrangement on page 1. Page 2 finishes in the left column with its right column empty.

## Actual reader-page observations

| Page | Fresh full-size observation | Raster SHA-256 |
| --- | --- | --- |
| 1 | Restrained centered title and clear pope/date/Latin line. Retained all-capital source heading is flush left. Both columns are readable with distinct gutter, consistent leading and paragraph indents, without clipping, collisions, severe word-space stretching, or missing glyphs. The second paragraph continues across columns normally; the third starts separately in the right column. Isolated source defects are visible, as described below. | `7a3f2e42399537b424dee6bd45a818543a63a12a84f8db9c21628d3541a0af8a` |
| 2 | Continues the split word from page 1, then gives the separately indented final body paragraph, complete blessing, dating clause, and `LEO PP. XIII`. The small terminal source/rights apparatus is legible below a short rule, clearly separate from papal wording. The empty right column is acceptable: this page has substantial authentic body text and the genuine closing, not merely project apparatus. | `5d8bcae0f7bdcc408c18c9ba92c3cb34309f3e3395263d1882cdc8150f70804d` |

Both rasters were opened individually using `view_image` with `detail: original`; the contact sheet was not used as a substitute. `individually_inspected_pages = [1, 2]`, `reused_pages = []`, and `reuse_proofs = []`.

## Bounded native witness and source boundaries

The complete native delivery `.scratch/papal_leo_review/ASS-27-1894-95-ocr.pdf` is 3,273,989 bytes, 768 pages, SHA-256 `cef47d120d5700533b8de81d136a7d5d90790157755e4cca2400b2cb0e189fd4`. Its bytes, page count, URL and size agree with the controlling native artifact and the document's publication approval. Native artifact-manifest hash: `56a2da60ad24e6d2e08ada7c3236b0d5bc7a25927db28b96d3b369de36955c6d`; publication-approvals file hash at review: `6a90b18c2237b9654905ac27338318bd8c2906a450d68061f33a6bca5fdc871f`.

The native artifact is an **OCR reconstruction**, produced by ABBYY FineReader, and the source record calls it `archival-ocr-pdf`. Rendered native glyphs are therefore not proof of the original printing's glyphs. The entire native PDF was extracted with `/usr/bin/pdftotext -layout` into this lane's scratch. This established 768 page sections, actual ordinal correspondence, and adjacent text boundaries. Ordinals **385, 386, 387** carry printed labels **385, 386, 387**. The constituent's archival locator likewise records artifact pages 385–387, closing lines 15262–15264, and no retained historical-note ranges.

Only those three necessary native pages were extracted with `/usr/bin/pdfseparate -f 385 -l 387`, then rendered through repository `tools/pdf-review --output .scratch/direct-baseline-recovery/child-f/native-rasters --cache .scratch/direct-baseline-recovery/child-f/native-cache --jobs 1` with the three extracted PDFs. All three resulting pages were individually opened at original raster resolution; their cache pins and extracted-PDF hashes were verified. No shared native raster/cache was written, and no raw parallel rasterization was used.

| Native page | Actual inspected evidence |
| --- | --- |
| 385 | Fresh source heading followed directly by `Christi nomen et regnum`; no omitted intervening salutation in this reconstruction. First body paragraph ends at `Venerabiles Fratres, sollertiam.` and the next separately indented paragraph starts `Nam, quod probe nostis`. The bottom Acta/fascicle line is publishing furniture, not a source note. Page ends mid-second-paragraph at `Inde etiam satis`. |
| 386 | Begins with continuation `compertae sunt ...`; the complete continuation ends `aequum est a Nobis impendi.` before the separately indented `Namque ut Orientalibus`. This checks both sides of the paragraph boundary rather than mistaking a page interruption for fusion. The third paragraph continues to page 387 after `com-`. No footnote, marginal summary, or alien act interrupts it. |
| 387 | Starts `mendalione Nostra ...` and completes the third paragraph at `in idem subministrare.` before separately indented `Id est igitur`. The final paragraph ends `amantissime impertimus.`, followed by a separate dating clause and centered subscription. The next distinct heading and `Longinqua oceani spatia` begin after that subscription; none enters the reader. |

The immediately preceding ordinal 384 was checked as layout text, not claimed as a viewed image: it ends a different S. C. Rituum response with its officials' subscription. Together with the freshly viewed start of page 385, this supports the opening boundary. The native page-385/386 and 386/387 continuations and all four body-paragraph boundaries agree structurally with the web reader. Dashes inside those paragraphs do not establish new missing paragraphs. No historical footnotes or note-bearing block appears within this act on the three viewed native pages; the approval's excluded bibliography is modern source apparatus. No missing substantive extent or imported neighboring text was observed within this bounded check.

Native raster hashes, ordinals 385/386/387 respectively: `a1cb274cb72211f950fa2ffc43fe7875d152bf32e5f91a7fbeb2c171f3b8fb94`, `9109523ad114d524a7c2741012a340ecd29f42640bf39b85256ee6d67bb92af7`, `c638b807673d6c9a45967db568d2248c9f3ab9ef635a9bc3c48cfcecc556b035`.

## Findings and limits

One **minor, nonblocking** finding applies to reader page 1: isolated inherited transcription defects include `explora vim us`, `litus`, and `commendalione`. They are already present in the exact selected web text and also occur in the native OCR reconstruction at pages 386–387. They are not fresh typesetting damage, sustained nonsensical body text, note fusion, or materially unreadable spacing. The selected edition visibly declares its uncollated status; accepting these bytes does not certify the spellings as original Latin. A later corrected edition would require separately identified derivative evidence and review, rather than silently changing this witness.

This review establishes complete mechanical fidelity to the selected web source, actual inspection of every reader page, and bounded native source-extent/paragraph/note checks. It does **not** claim full lexical collation against the native PDF or an original facsimile, original-print glyph verification, a current-website comparison, a new rights opinion, or acceptance of any other reader. The three native images were used for boundaries, local suspicious loci, and notes only. Prior reviewer results are not coverage here.

Supporting owned evidence: `identity-check.json` (SHA-256 `bb359537a24803dedb118844a0011fd6f835f7345b47a396af7800a14c4ed227`), `build-diagnostics.json` (`1653b76a4056e66be4b0bdbdfbd9ecba968d5ac29747a2a04dd5ea0544084f8f`), and `native-evidence.json` (`541db5b8d7f196cd87157f08c654735096c8b5cd16c4222936d6b8e6e427566e`), plus complete layout/raw text and metadata/font outputs. No generic handoff ZIP was required for this explicitly assigned scratch-result lane. No blockers remain and no live operation is being handed off.
