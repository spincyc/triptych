# Bullarium reading-order visual review bullarium-ro-0003 — lane 05

PASS: 19 assigned PDFs, 45 pages individually opened at full size; zero blocking findings. All 45 are new inspections, with zero reused pages. Eight replacement readers carried a `prior_finding`; each prior footnote fusion is confirmed absent. This report covers only lane 05 of batch `bullarium-ro-0003`: seven Sixtus V readers from the 1883 Naples volume VIII, eight readers from the 1865 Turin volume IX (Sixtus V, Gregory XIV, Clement VIII) and four Clement VIII readers from the 1867 Turin volume XI.

## Scope and method

Each assigned page PNG, produced by the repository's `pdf-review` tool for this batch, was opened as its own full-size image with the Read tool (1700 x 2200 originals). No contact sheet, thumbnail or new raster pass was used. One JSON line per page was appended to the lane's `observations.jsonl` after each document. To locate loci precisely, the reading-order derivative lines named in each frozen source note were consulted and PDF text was extracted with `pdftotext` into the lane directory; these were aids only, and every status rests on the opened page image.

Each title line, responsible issuer, date treatment and language label was compared with the frozen metadata. Headings, two-column flow, gutters, margins, glyphs, natural closing, source notes and terminal source/rights apparatus were inspected, together with the series addendum for coordinate-reconstructed Bullarium readers: marginal summaries as separate TAB-led blocks, page-foot notes as separate blocks at the page break, natural two-column order, inline running heads, folios and signature marks, and short non-word OCR noise. No word-level collation, text correction, date reconstruction or extent decision was made.

All 19 readers display the Latin label, match the frozen title and issuer exactly, and omit the unresolved date from the title line without calling the source undated. No visible clipping, overlap, missing-glyph block, collapsed table, raw `None` placeholder, modern digitizer signature ("Digitized by Google" or damaged variants) or stranded heading was found. Every final page carries genuine source closing (dating clause and/or the source's own dating line and notes) before the project's Source and rights apparatus; none holds only project notices or running-head furniture.

This report does not authorize installation and makes no claim that installation, deployment, publication or historical authentication has occurred.

## Evidence verification

All 19 PDFs, the render receipt, the frozen manifest, the shared raster-run record and all 45 page PNGs were hashed before inspection (`verification-before.json`) and again after inspection (`verification-after.json`). Every one of the 67 digests matched its assignment pin both times, and the two records list identical digests.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment `assignment.json` | `46403e376568deab596ea6725c7ab6f0e16d4e96fa014b7367651a1b6620a054` | Unchanged before and after |
| Before verification record | `18db2e7d5fd982749b92a008b217470f8ba84dda88cc8d31508c546477702d0b` | 67/67 match |
| After verification record | `c1e35f61cff6e94d29ed558a0e8a5be9cf5172c1c667484ac8e10ece289734c6` | 67/67 match; identical to before |
| Inspection ledger `observations.jsonl` | `45933fbbdebbb5e34c17288162b33f44fab6323ca1ccc5dfd51a00e7a5e34a51` | 45 unique page observations |

## PDF outcomes

Marginal blocks are the TAB-led marginal-summary blocks in each reader's selected derivative ranges, all seen rendered as separate blocks (stray single-mark marginal blocks such as `.`, `,` or `●` included). Note blocks are the printed page-foot or terminal source-note blocks seen.

| Source ID | Issuer (frozen) | Lang. | Pages | PDF SHA-256 | Marginal blocks | Note blocks | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bullarium.volume-08.unit-0206.reading-order` | Sixtus Papa V, moto proprio, etc. | `la` | 2 | `13a6632dd98ea1f173f4ed697382a8fd3287f12fe1782b54c49f8cfffca7a06d` | 13 | 2 | PASS |
| `bullarium.volume-08.unit-0208.reading-order` | Sixtus Papa V, ad perpetuam rei memoriam. | `la` | 3 | `37ba619209a76c90827fcb830efa0550a87c89c65ce8dc67d71eb47b69349195` | 11 | 1 | PASS |
| `bullarium.volume-08.unit-0213.reading-order` | SixtQS Papa V, ad perpetnam rei memoriam. | `la` | 2 | `e8fb47950f849f30181804558b943eb5557a664d0fa4cdd436ade7d52c395355` | 4 | 1 | PASS |
| `bullarium.volume-08.unit-0214.reading-order` | Sixtas Papa V, ad perpetnam rei memoriam. | `la` | 2 | `0ca92198a886613916562e3daf90937917ca1bbb5ae5ecaf878810e1b8a107da` | 4 | 1 | PASS |
| `bullarium.volume-08.unit-0222.reading-order` | SixtDsFapa V, ad perpetaam rei memoriam. | `la` | 2 | `99fb9849a96ae54b7dcf6703e81f4042cc64d33f4975654fe16e68ba15e0d922` | 8 | 1 | PASS |
| `bullarium.volume-08.unit-0227.reading-order` | Sixtns Papa V, ad perpetnam rei memoriam. | `la` | 2 | `909a3ef5e48fa24d6df0a6af82fea85e65bb2fa6e171dd1946eea3dc68ff50f3` | 6 | 1 | PASS |
| `bullarium.volume-08.unit-0235.reading-order` | SixtDs episcopas, servas servoram Dei, ad perpetuam rei memoriam. | `la` | 2 | `73e14666672a19fc9e0114150a78bed15c062f0a90b4fb8bf2e26e5318063d1f` | 10 | 2 | PASS |
| `bullarium.volume-09.unit-0004.reading-order-v2` | Sixtas Papa V, ad perpetnam rei memoriam. | `la` | 3 | `bee661bcf65a412cf8f4199d3a4b8b0939fbde78fff1bcc6f745233db3af4511` | 13 | 4 | PASS |
| `bullarium.volume-09.unit-0005.part-01.reading-order-v2` | Sixtus episcopus, servus servorumDei, ad perpetuam rei memoriam. | `la` | 3 | `31d3d690c686939a2538b6bbc5e3a9952ea08783cc311737d91abb9c2b335dee` | 10 | 2 | PASS |
| `bullarium.volume-09.unit-0005.part-02.reading-order-v2` | Sixtus episcopus, servus servorum Dei, al perpetuam rei memoriam. | `la` | 3 | `1c0919eb61ddd71cf2b6e8c5a2da547e56197c1d89221f33ab59519829df3712` | 13 | 1 | PASS |
| `bullarium.volume-09.unit-0017.reading-order-v2` | Sixtas Papa V, ad futuram rei memoriam. | `la` | 2 | `5e4c8f0600c38bc3caf736d287e9e548022f56a9f9dc89b1c879a6ebc770c57a` | 7 | 1 | PASS |
| `bullarium.volume-09.unit-0025.reading-order-v2` | Sixtus Papa V, ad perpetuam rei memoriam. | `la` | 2 | `f434c3807d7de0057ed255f1e017db465dee8ec31e56499d133d5b46fb2c3155` | 9 | 2 | PASS |
| `bullarium.volume-09.unit-0058.reading-order-v2` | Sixtus Papa V, ad perpetuam rei memoriam. | `la` | 2 | `d5b2f8843cfad5335b296b09746df9c6eba56c2c1bf51ace4186912358824d9c` | 11 | 1 | PASS |
| `bullarium.volume-09.unit-0095.reading-order-v2` | Gregorius episcopus servus servorura Dei, ad perpetuam rei memoriam. | `la` | 4 | `aa5b958c0257583f0df9e119b84c19e38553f2254df976a4bc45e54779185b2e` | 19 | 3 | PASS |
| `bullarium.volume-09.unit-0131.reading-order-v2` | Clemens Papa Vili, ad perpetuam rei memoriam. | `la` | 2 | `3d70013b6ce9f597d2c346a92c9ba461f1421deed788d855957e98076994c3e3` | 6 | 1 | PASS |
| `bullarium.volume-11.unit-0003.reading-order` | Clemens Papa Vili, | `la` | 2 | `e86cbe45067b5b839ec60b88ef88ccf6fe914088557279e28d8547eb6affbaf9` | 7 | 1 | PASS |
| `bullarium.volume-11.unit-0006.reading-order` | Clemens Papa Vili. | `la` | 2 | `937e26a4c67cb37814a0e026250f35aeb8ba2adfb60064a97d6f33d94c441a2e` | 4 | 1 | PASS |
| `bullarium.volume-11.unit-0009.reading-order` | Clemens Papa Vili, | `la` | 2 | `1da7f1318278e4ebf9442a0b8ee8c4cda88b311a1d6b34116c7d3d0c666c09e4` | 6 | 1 | PASS |
| `bullarium.volume-11.unit-0010.reading-order` | Clemens Papa Vili, | `la` | 3 | `547d04fcb65a076d01f4b5b619475ad6c7d9fb23812dce2af49a7ba0d9c7a138` | 8 | 8 | PASS |

Totals: 19 PDFs, 45 pages, 169 marginal blocks, 35 note blocks, 0 fusions, 19 PASS, 0 CHANGES_REQUIRED.

## Page rasters inspected

| Source ID | Page | PNG SHA-256 |
| --- | --- | --- |
| `bullarium.volume-08.unit-0206.reading-order` | 1 | `f594a9287a012db70fad4186bf6d4c9cd2d903e96de9c2f86d6874911206d29e` |
| `bullarium.volume-08.unit-0206.reading-order` | 2 | `97690706610d7c4dd49934ec328c1cab3c4f13b237419d217258ec24c5b37d84` |
| `bullarium.volume-08.unit-0208.reading-order` | 1 | `7e02d12c1ce18c620a83cd7db51922fbcf2f5a3293678131a82c62b7f1882a69` |
| `bullarium.volume-08.unit-0208.reading-order` | 2 | `0591e35dad3cb56fd9d34d04d6a25fad7acd8dfd4cbeb66d881e4b5e7efc8f38` |
| `bullarium.volume-08.unit-0208.reading-order` | 3 | `61e9f2d34e5ca8017c84280b352d64cc52092468db5942d0051b5ff5bae3b45c` |
| `bullarium.volume-08.unit-0213.reading-order` | 1 | `056e7c99d8a111c409e5d8a0a52d99d2c43b1b8158c99f9ce55837cdd4136bd8` |
| `bullarium.volume-08.unit-0213.reading-order` | 2 | `2924cd8ce269dff8024d3b1842619774bd99859beb9303dd08d2a0b716b37d0a` |
| `bullarium.volume-08.unit-0214.reading-order` | 1 | `b778db866479a973ce6cceed1286c36dc44297b853922276d1bfabc6f090c1ba` |
| `bullarium.volume-08.unit-0214.reading-order` | 2 | `1c2a9d92860b7adc430122e07325e5ae0db6d69bcb994fc637437ee75d4f23aa` |
| `bullarium.volume-08.unit-0222.reading-order` | 1 | `5f0cff941c2855e48db69e024b5289431bf1b3c388a82787fa6657adf3faea5c` |
| `bullarium.volume-08.unit-0222.reading-order` | 2 | `5d718c08f8fe322bd227dddcae23c7415b4f493d3acdc5a11ccd43005fb7ae85` |
| `bullarium.volume-08.unit-0227.reading-order` | 1 | `7e02f70565c20f13783f2dd60163e93daf894f53d226d7b96e3a7687b024eb95` |
| `bullarium.volume-08.unit-0227.reading-order` | 2 | `341c402b55eac15c48c60dc3f608cd8eb32853aa9398ccbe424036c5b7742120` |
| `bullarium.volume-08.unit-0235.reading-order` | 1 | `170c1b3d81aa3249fa8143ea7fd7b8cc56d81b72534b2ca3783a5821f3cfb732` |
| `bullarium.volume-08.unit-0235.reading-order` | 2 | `36e9fc396c40f9d04bfe124f2bf9c16709acc8233c710f80fea1a256a3b006cb` |
| `bullarium.volume-09.unit-0004.reading-order-v2` | 1 | `1e1302650736b49108432a085364a4b2aa0fff35bb27349f10a2a29da2e54da8` |
| `bullarium.volume-09.unit-0004.reading-order-v2` | 2 | `69fbc20007d876a15317f87d6f411206bca0d46c0f087aa2f845a19225406429` |
| `bullarium.volume-09.unit-0004.reading-order-v2` | 3 | `2552e737de44d3908b79f08ba0c71ee3636dae5224b5bc4741a4457f3e87fbfe` |
| `bullarium.volume-09.unit-0005.part-01.reading-order-v2` | 1 | `e7bf2f3fd75f214279c90d301ef353127a1df5f5c9a5d31502d5dd2e6d096139` |
| `bullarium.volume-09.unit-0005.part-01.reading-order-v2` | 2 | `2308ea8adc2bffd59a4f0d5b904a4ed4396c57f1ca8f732cc03185b4139fdf08` |
| `bullarium.volume-09.unit-0005.part-01.reading-order-v2` | 3 | `25931aed54602f341966e69b6891ea3c804d0fabbe21ae6c4506422cd3ae89c7` |
| `bullarium.volume-09.unit-0005.part-02.reading-order-v2` | 1 | `c0c82bd3e3a3d6fbd947335ef662443fa09d6401c9b48c6d51941edb5b81fab0` |
| `bullarium.volume-09.unit-0005.part-02.reading-order-v2` | 2 | `9de36dd3ad7f8a35063e4902bb38c41a180e936da0975864d3be4386996348a9` |
| `bullarium.volume-09.unit-0005.part-02.reading-order-v2` | 3 | `de97124fbdc81de14de6e95566f3bc0d0fd3167d7dca5bf170b3492faaf9aea3` |
| `bullarium.volume-09.unit-0017.reading-order-v2` | 1 | `8b6e55ac4074d7e147592dcb1b2fe8c4b237797a66cb1bac6b18bf07233cf49b` |
| `bullarium.volume-09.unit-0017.reading-order-v2` | 2 | `094547dfcb3ea8b8684ef34b3c218458691927955ba62079e81896b827966b81` |
| `bullarium.volume-09.unit-0025.reading-order-v2` | 1 | `24e9249bfc64550174eb244379a57b4c09d7f82aa5689c30cdb803707487705e` |
| `bullarium.volume-09.unit-0025.reading-order-v2` | 2 | `20890e9eadefc9339b9a779b38671652411867f3d5f665e8c9ef074916e0ab02` |
| `bullarium.volume-09.unit-0058.reading-order-v2` | 1 | `c519e899de13093af7e9fd2f524932527159f67a4b41b03232c0603a548e53e3` |
| `bullarium.volume-09.unit-0058.reading-order-v2` | 2 | `8207fdab4f4f040a5a25c5186d4b19b2362ab64a29d6c72fbcd40158906b5e35` |
| `bullarium.volume-09.unit-0095.reading-order-v2` | 1 | `91cfbed94678b6ebd59c752522856de27766a89df178095d9300ab0076431e5f` |
| `bullarium.volume-09.unit-0095.reading-order-v2` | 2 | `38ffd7e5b09c17e24a524db0e32f344dd6108fa8fd5ee1af044908ed282c3838` |
| `bullarium.volume-09.unit-0095.reading-order-v2` | 3 | `c8ee131d98969ce9d2addecb29711eb6d70e36087394f0732988ea08d1736fb2` |
| `bullarium.volume-09.unit-0095.reading-order-v2` | 4 | `f4b956d4f4a225298ee871384e7901e752f9fe8b512543439f6340085ef6c8ea` |
| `bullarium.volume-09.unit-0131.reading-order-v2` | 1 | `706e4faaec5774f89013b6a81566567ced803e6c879a7af29c1f722424ff4d33` |
| `bullarium.volume-09.unit-0131.reading-order-v2` | 2 | `0a2b391e8d4e948ebc47a029adaf105dcc23bbc6f7ab03e23b7812e3f0783716` |
| `bullarium.volume-11.unit-0003.reading-order` | 1 | `eaa17db155ee0e6dc2d66883a6a486fc314cf042da916b2b3b405b2077755635` |
| `bullarium.volume-11.unit-0003.reading-order` | 2 | `af996c9a6b04de1e465ac73e8e80a129f381383391b49361f5da89e5eb7a7c73` |
| `bullarium.volume-11.unit-0006.reading-order` | 1 | `eec9da956c0adbebe7204306dd360a6d7aedd316794bb612911ea73e972cd9e3` |
| `bullarium.volume-11.unit-0006.reading-order` | 2 | `2718e0a3e81dca8428a8c5848d4443b2f9f175197d351a977e09f8c06f3e7459` |
| `bullarium.volume-11.unit-0009.reading-order` | 1 | `671c20272efb6266a372c94c2bdb7d569606e133adc097ff02b5f665d2a97e73` |
| `bullarium.volume-11.unit-0009.reading-order` | 2 | `8b12b680bed6dbbf671e921f0726bf15f7f5beaebd4dbdfa78935ce01d925f32` |
| `bullarium.volume-11.unit-0010.reading-order` | 1 | `3d1a6cf3b56860bd0274fd55dc4d4d94c8f3a2551b41104d1460c60fb27ae080` |
| `bullarium.volume-11.unit-0010.reading-order` | 2 | `24020434bdb8b61fb90a570061ecda612ccd593e25cdcacf2d6644486a313162` |
| `bullarium.volume-11.unit-0010.reading-order` | 3 | `7b3f8c5e318e5dfda8ef2ad82b47db1d6897ab56cb8d2c6310d4285af61e0f4d` |

## Prior findings

Each of the eight `-v2` replacement readers in volume IX carried a prior finding that a printed page-foot note had been run into a body paragraph. Each prior defect is now absent:

- `bullarium.volume-09.unit-0004.reading-order-v2`: § 3 on page 2 reads 'qualcnus nondum confccerint, debeanlo- mnino inlra annum ...' with no note text. The note '1. Foulaiiinus legit vivitur (r. t.)-' (derivative LF 3316) is its own block at the page break on page 3, left column, before the running head.
- `bullarium.volume-09.unit-0005.part-01.reading-order-v2`: § 6 on page 3 runs continuously '... ac amplialiour, et super omnibus privative quoad omnes alios iudices ...'. The notes 'i Vide latius liicinf. 2 Cher legit. (jiianlKm- VìS (R. T.)-' form a separate note block at the page break, left column, after § 8 'omnino regi-'.
- `bullarium.volume-09.unit-0005.part-02.reading-order-v2`: on page 2, left column, § 5 ends 'ac tam per cum edenda quam a-'. The note 'Ea oniitlit Mainardus, quia in omnium mani- bus versabantur 'k. t.).' is its own block, followed by the running head and the body resuming 'lia desuper de mandato ...'.
- `bullarium.volume-09.unit-0017.reading-order-v2`: the proem on page 1 runs 'dilectorum filiorum fra- trum Ordinis ...'. The note '{ Ex Regest. in Secret. Brevium.' is its own block at the page break, right column.
- `bullarium.volume-09.unit-0025.reading-order-v2`: the opening sentence on page 1 reads 'gaudemus au- dientes aelatem ...'. The note 'I Ex Regest. ìu Secret. Brev-' is its own block at the head of the right column, after 'superasi, ne-'.
- `bullarium.volume-09.unit-0058.reading-order-v2`: § 1 on page 1 runs 'fiscalatusetcommissaria- tus ab ol'lieio ...'. The note 'i Ex Regest. in Secret. Brevium.' is its own block at the page break, right column. The printer signature mark 'Bull. Rom. Voi. IX. 30' shares that note line, which is non-blocking under addendum (d).
- `bullarium.volume-09.unit-0095.reading-order-v2`: the note 'I r.HKHUB. In qua sii, loco verboruin in alio. (R. T.)' is one complete block on page 4, left column, after '§ 10 ... ul personae' and before the running head. Its '(R. T.)' tail no longer opens a body paragraph. The paragraph containing 'Plus Papa lY, praedecessor noster, statuii ohseivandam' (page 3, right column, into page 4) contains no note text.
- `bullarium.volume-09.unit-0131.reading-order-v2`: § 4 on page 1 runs 'et seu le- gationis Avenionensis ...' with no note text. The note '●i Tenorem istius Constitutionis oraisil in sua editione Mainardus ... pag. 438.' (LF 62528-62530) is its own block after the closing on page 2.

## Addendum audit: fusions and placements

No marginal summary was found fused into a body sentence or a hyphen-split word (addendum a). No page-foot note was found run into a body, synopsis or protocol paragraph (addendum b). Two-column text reads in natural order on all 45 pages (addendum c). No reader is a fragment (addendum e). The fusion count is zero.

The following non-blocking qualifications were recorded with their loci. The full per-page list is in `observations.jsonl`.

- Running heads and folios (addendum d) appear as their own inline blocks in every multi-page reader, typically right after a page-foot note. Printer signature marks were left inline or sharing a note line at these loci: unit-0214 page 1, right column ('UuU. Rum. Voi. Vili. lUS' at the end of a § 2 body line); unit-0005.part-01 page 2, left column ('Bull. Rom Voi. IX. * 4' at the end of a § 3 body line); unit-0058 page 1, right column (in the note line); and vol. XI unit-0010 page 2, left column ('Bull. Rom. - Voi. XI. 4' in the note line).
- Marginal blocks are set as their own blocks but placed mid-sentence or between the halves of a hyphenated word (addendum d). Loci:
  - unit-0213 page 1, left column, § 1.
  - unit-0235 page 1, right column, § 5.
  - unit-0227 page 1, right column, '''' between 'con-/fluimt'.
  - vol. IX unit-0004 page 1, between 'palriar-/chis', with the running head.
  - unit-0005.part-01 page 3, right column, § 9.
  - unit-0017 page 2, left column, '-' in § 3.
  - unit-0025 page 1, left column, three marginal blocks, one between 'consi-/lium'.
  - unit-0058 page 1, right column.
  - unit-0095 page 3, left column.
  - vol. XI unit-0006 page 1, left column.
  - unit-0010 page 1, right column, '●' between 'duxis-/set'.
  - unit-0206 page 2, left column, ',' between 'lil-/leris'.
- Short non-word OCR noise inside body lines (addendum f) occurs in most readers, sometimes splitting one sentence into two paragraphs. Examples are unit-0208 § 1 '" ; . . _', unit-0005.part-02 §§ 3-4 and § 9, and vol. XI unit-0010 §§ 3-7. In each case the run contains only punctuation, isolated glyphs or OCR-garbled fragments at body positions, and the adjacent marginal summary is complete as its own block. Two loci hold corrupted letter strings rather than pure punctuation; on inspection they are read as damaged body OCR, not marginal words. They are unit-0208 page 1 '^'''^o^'.cuf'' ^'c, "I', where the body name stands, and unit-0005.part-02 page 1 '' o> e- ,-c!Tcnte', at the 'regente' position.
- Stacked single-glyph OCR lines are set as their own blocks at column feet: unit-0208 page 2, unit-0227 page 1, vol. IX unit-0004 page 3 and unit-0095 page 2.

## Per-document findings

- `bullarium.volume-08.unit-0206.reading-order` (2 pages): PASS. Proem marginal 'fonsì'iiuii«:ii'' and two page-foot notes are separate blocks. Running heads appear inline on pages 1 and 2, and a stray ',' marginal sits in § 7. Natural closing: 'Datum Romae ... anno ii.', 'Fiat motu proprio', the publication note, the cursors' subscription and 'Dal. die 5 aprilis 1587'.
- `bullarium.volume-08.unit-0208.reading-order` (3 pages): PASS. Non-word noise appears in §§ 1-5, with no marginal words. Page 2 has a stack of single-glyph lines at the foot of the left column. Page 3 is sparse, with genuine closing 'Datuin Romae ... die xxiv aprilis MiM.xxxvii ...' and 'Dal. die 24 aprilis 1587, ponlif. an. ii.'.
- `bullarium.volume-08.unit-0213.reading-order` (2 pages): PASS. The heading is set in three source-break blocks and a marginal is placed mid-sentence in § 1. Page 2 is sparse, with genuine closing 'Datum Romae ... die xv maii MDLxxxvii ...' and 'Dat. die 15 maii 1587 ...'.
- `bullarium.volume-08.unit-0214.reading-order` (2 pages): PASS. A signature mark stands inline in § 2. Closing: 'Datum Romae apud Sanclura Marcum ... die iv iunii ...' and 'Ddl. die 4 iunii 1587 ...'.
- `bullarium.volume-08.unit-0222.reading-order` (2 pages): PASS. Noise appears in § 6, and a stray '●' marginal stands on page 2. Closing: 'Datum Romae ... die v seplernbris MDLXxxvii ...' and 'Dal. die 5 sepl. 158'' ...'.
- `bullarium.volume-08.unit-0227.reading-order` (2 pages): PASS. A stray ''' marginal stands between 'con-/fluimt', single-glyph lines follow the note, and the § 4 sentence is split at noise. Closing: 'Datum Romae ... die xxxi oclobris ...' and 'Uat. die 31 octobr. 1587 ...'.
- `bullarium.volume-08.unit-0235.reading-order` (2 pages): PASS. One marginal is mid-sentence in § 5, and noise appears in §§ 1, 2, 5 and 6. Closing: sanction clauses, 'Datum Romae ... idibns marlii ...' and 'bai. die 15 marlii 1588 ...', followed by the source note 'i Ui saprà in eius const. cxii ...' as its own block.
- `bullarium.volume-09.unit-0004.reading-order-v2` (3 pages): PASS, and the prior finding is absent. The dating clause 'die xx iulii MDLXXXViii' and the date line 'Dai. die 20 iunii 1588' differ literally; this is recorded, not repaired. The terminal note '1 Deest forsan fuciat (r. t.).' is its own block.
- `bullarium.volume-09.unit-0005.part-01.reading-order-v2` (3 pages): PASS, and the prior finding is absent. The frozen title is the first part of the printed heading, whose remainder continues in the body. The title line matches the metadata. Closing: 'Dalum Romae ... kalendis augusti ...' and 'Dal. die i augusti 1588 ...'.
- `bullarium.volume-09.unit-0005.part-02.reading-order-v2` (3 pages): PASS, and the prior finding is absent. Noise splits sentences in §§ 3-5. Closing: 'Datum Romae apud S. Peirum ... pridie kaicndas nove'mbris ...' and 'Dat. die 31 od. 1588 ...'.
- `bullarium.volume-09.unit-0017.reading-order-v2` (2 pages): PASS, and the prior finding is absent. Closing: 'Datum Romae ... die celava aprilis MDLXXXix ...' and 'Dal. die 8 aprilis 1589 ...'.
- `bullarium.volume-09.unit-0025.reading-order-v2` (2 pages): PASS, and the prior finding is absent. Three marginals stand mid-sentence on page 1. The note '1 Guida ex Ihciitonico ...' is its own block. Closing: 'Dalum Romae ... die xi novem- bris MDLXxxix ...' and 'Dal. die \ì iiovemb. 1589 ...'.
- `bullarium.volume-09.unit-0058.reading-order-v2` (2 pages): PASS, and the prior finding is absent. Closing: 'Datuni Romae ... die xv augusti MDLXxxvn ...' and 'Dat. die 15 aug. 1587 ...'.
- `bullarium.volume-09.unit-0095.reading-order-v2` (4 pages): PASS, and the prior finding is absent. The issuer is 'Gregorius episcopus servus servorura Dei', matching the metadata. Closing: 'Nulli ergo, eie.', 'Dalnni Romae in Monte Quirinali ... idibus maii ...' and 'Dal. die 15 maii 1591 ...'.
- `bullarium.volume-09.unit-0131.reading-order-v2` (2 pages): PASS, and the prior finding is absent. Page 2 is sparse, with genuine closing 'Dalum Romae ... die xxviii februarii MDXcii ...', 'Dat. die 28 februarii 1592 ...' and the source note.
- `bullarium.volume-11.unit-0003.reading-order` (2 pages): PASS. The note '2 ExRegest. in Secret. Brevium.' is its own block. Page 2 is sparse, with genuine closing 'Datum Romae ... die xiv aprilis MDCiii ...' and 'Dal. die 14 aprilis 1603 ...'.
- `bullarium.volume-11.unit-0006.reading-order` (2 pages): PASS. The address and salutation are separate blocks, and the § 1 sentence is split at noise. Page 2 is sparse, with genuine closing 'Dalum Romae apud S. Marcum ... die xvni iulii mdciii ...' and 'Dal. die 18 iulii 1603 ...'.
- `bullarium.volume-11.unit-0009.reading-order` (2 pages): PASS. The embedded decree's dating line is its own block. Page 2 opens with a running head, then the marginal, § 5 and genuine closing 'Dalum Romae ... die xxiv iulii mdciii ...' and 'Dal. die 24 iulii 1603 ...'.
- `bullarium.volume-11.unit-0010.reading-order` (3 pages): PASS. All eight note blocks are separate, and one shared note block holds notes 2 and 3. Noise inside the cited date '... apriiis , ..,. , 1 . j- ... MDCii' is recorded literally. Page 3 is sparse, with genuine closing 'Datum Romae ... die ii augusti mdciii ...', 'Dal. die 2 augusti 1603 ...' and the note '1 Huiusmodi quoque rescriptum exulat a Bul- lario (r. t).'.

Some derivative note lines adjacent to a selection lie outside its frozen ranges: unit-0235 LF 118931-118932, vol. XI unit-0003 LF 7786-7790, unit-0009 LF 9704 and vol. IX unit-0131 LF 62399-62402. Extent is upstream evidence, and this layout review does not judge it.

## Limitations

- The text is literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. Odd spellings, OCR corruption, garbled marginal summaries and literal or conflicting source dates are limitations, not defects, and no date was inferred or repaired.
- This is a layout and visual review only. No word-level collation against the printed volumes, no WORD-coordinate audit, no historical authentication and no source-extent judgment was performed.
- Derivative text and `pdftotext` output were used only to locate loci, and every status rests on the opened page image.
- This report makes no publication, installation or deployment claim.
