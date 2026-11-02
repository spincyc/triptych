# Bullarium reading-order visual review 08 — bullarium-ro-0003

CHANGES_REQUIRED for one reader. Lane 08 of batch `bullarium-ro-0003` covered 22 assigned PDFs: 20 complete printed-act readers from Bullarium Romanum volume 11 (1867 Turin) and two fragment readers, from volume 3 (1858 Turin) and volume 8 (1883 Naples). Each of the 46 pages was individually opened at full size; none were reused. Twenty-one PDFs PASS. One PDF, `bullarium.volume-03.unit-0173.part-02.reading-order.fragment`, has a blocking marginal-summary fusion on page 2. No assigned document carried a `prior_finding`.

## Scope and method

Every assigned page PNG listed in `assignment.json` was opened as its own full-size image with the Read tool (1700 × 2200 raster, displayed at 1545 × 2000). No contact sheet, thumbnail or new raster pass was used. A page was recorded in the inspection ledger only after it had been viewed. The rasters are the ones produced by the repository's `pdf-review` tool for this batch.

On each page, the displayed title line, responsible issuer, language label and the omission of the unresolved date were compared with the frozen metadata. Headings, two-column flow, gutter, margins and glyphs were inspected, as were natural closings, historical notes and the terminal source/rights apparatus. Pages were checked for modern provider signatures, raw placeholders and running heads interrupting body text. The series addendum for coordinate-reconstructed Bullarium readers was also applied. Marginal summaries must stand as separate blocks, never inside a body sentence. Page-foot notes must be separate blocks at the page break. Body text must read in natural order. Fragments must show a fragment title and a missing-content notice. Non-word OCR noise was distinguished from marginal wording.

Where the image showed a short non-word string or an unusual placement next to a marginal summary, the generated body TeX (read-only) and the volume's retained raw OCR text (`src/sources/works/bullarium-romanum/volume-NN/editions/*/artifacts/ocr-*/ocr.txt`, read-only) were consulted. These sources show whether the string sits on the body side or the marginal side of the source row. They were used only to classify what the image showed; no wording was judged, corrected or collated.

## Evidence verification

All assigned PDFs, the receipt, the frozen manifest, the shared raster-run record and all 46 page PNGs were hashed before and after inspection. Every digest matched its assignment pin both times (71 files; before and after records identical).

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt (`.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json`) | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest (`.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json`) | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run (`.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json`) | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment (`assignment.json`) | `a0a7c93060d848c958a9decdf405a70a0654ca01308d957a23ffcdf0c12cf23a` | Scope binding; unchanged |
| Before verification record (`verification-before.json`) | `67dff56063978149f795a3e783e04f7538e2c14c6a9bbc10492b562913704500` | All 71 match |
| After verification record (`verification-after.json`) | `9e996b8fa3fd5b51d50661ea03d75cc43953294d11be6ba9c4b520b57e4297a9` | All 71 match; identical to before |
| Inspection ledger (`observations.jsonl`) | `9b2e11fe55b8a0021c4441203af24c41e80a0bcd3281f5916d0dd4da5f59fa34` | 46 unique page observations |

Lane records are in `.scratch/claude-review/bullarium-ro-0003/lane-08/`.

## PDF outcomes

All are Latin (`la`) and carry no resolved act date. The title lines correctly omit the date and never describe a source as undated.

| Source ID | Language | Page count | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- |
| `bullarium.volume-11.unit-0132.reading-order` | `la` | 2 | 1, 2 | `219f5e5d5bba7207c461ec7405456f322548d0d880bfeccd834931eebab63c57` | PASS |
| `bullarium.volume-11.unit-0136.part-02.reading-order` | `la` | 1 | 1 | `87336a0c98fb2e257fb8f472accba0c81ceba8f45d2d51ba3279544ec9843449` | PASS |
| `bullarium.volume-11.unit-0140.reading-order` | `la` | 1 | 1 | `2196d01a7374658897718075b4c5bfc27dd23caf907d7123fa81aa1f5c469eff` | PASS |
| `bullarium.volume-11.unit-0143.reading-order` | `la` | 2 | 1, 2 | `02ab5ec20900222af32db91f9a249199825a7867c85fae4eb010cb2c48245f99` | PASS |
| `bullarium.volume-11.unit-0144.reading-order` | `la` | 2 | 1, 2 | `fe340f795ceed538f2f1f0df3d9094a41e403889af89357ed357650c979cfd8f` | PASS |
| `bullarium.volume-11.unit-0151.reading-order` | `la` | 1 | 1 | `88a63eef5a223fe37fd038ca1ece558de66984c2b54c0d9b48f623583f98a7f0` | PASS |
| `bullarium.volume-11.unit-0155.reading-order` | `la` | 2 | 1, 2 | `40193643e2dbc2158e2f66f9b2927602cbee2481bc079fb1d098c055a4cea3b2` | PASS |
| `bullarium.volume-11.unit-0157.reading-order` | `la` | 1 | 1 | `e3117542a496d5d9c70599a2a1656e5efe6cd5e628e3203c558c6e6e0ceef8dc` | PASS |
| `bullarium.volume-11.unit-0163.reading-order` | `la` | 2 | 1, 2 | `4727a706b3566f3b7dc275aa5752f5f997afc88db24e2faf193fcef7df91426e` | PASS |
| `bullarium.volume-11.unit-0165.reading-order` | `la` | 2 | 1, 2 | `53a33856d1c75306403bc2df2300ea15473cfee574681fc1837162a9774a15b0` | PASS |
| `bullarium.volume-11.unit-0166.reading-order` | `la` | 2 | 1, 2 | `a1c10189dade773c4df62d42b4833043fed4c99bfd437cea063bbc3d0df3b209` | PASS |
| `bullarium.volume-11.unit-0169.reading-order` | `la` | 2 | 1, 2 | `b56e305fc282c1f5212fe62da11109d666301a5167225bd8b42fd148105c7bf4` | PASS |
| `bullarium.volume-11.unit-0171.reading-order` | `la` | 2 | 1, 2 | `13f376cce3d6157d5d1814f386b5c785700a6cac32d6dfe0042e45e1b2faf176` | PASS |
| `bullarium.volume-11.unit-0177.reading-order` | `la` | 2 | 1, 2 | `ee83c12d1dcb49e7f602f8b7130e37c15a6e83616b784fd43a90c1922f90126c` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | `la` | 6 | 1, 2, 3, 4, 5, 6 | `6def3b6098464a479928e13e02130cfce4878eddde47f585b980dd402f6cacd2` | PASS |
| `bullarium.volume-11.unit-0180.reading-order` | `la` | 1 | 1 | `fc7d6722b2cf5d783e4b991ef865f5bf2459eb5d7cacaccad8d04d538f29d324` | PASS |
| `bullarium.volume-11.unit-0182.reading-order` | `la` | 2 | 1, 2 | `8642f0737bd2387d47d4ea80225796c02295aef6d450037dc336da2ce0860406` | PASS |
| `bullarium.volume-11.unit-0184.reading-order` | `la` | 2 | 1, 2 | `e2a04442604d5a4959054514fc68a3924341b722dc07a72fe0398c47b5c2cca9` | PASS |
| `bullarium.volume-11.unit-0186.reading-order` | `la` | 3 | 1, 2, 3 | `ed960632135e84221274657dc79ec674bdc539c1fd82aaf2d4d1f3d485ed7558` | PASS |
| `bullarium.volume-11.unit-0188.reading-order` | `la` | 2 | 1, 2 | `2e7d161fbd09221cb7360fc72de8f601f836b6789eb9caaceca54909219f69b2` | PASS |
| `bullarium.volume-03.unit-0173.part-02.reading-order.fragment` | `la` | 3 | 1, 2, 3 | `cb34bdfeb93f85b2305aa160f8e18dffdab3bfd347735d7f51e44d6180fc7c40` | CHANGES_REQUIRED |
| `bullarium.volume-08.unit-0090.reading-order.fragment` | `la` | 3 | 1, 2, 3 | `cbedf7a8c3f981898d6ec74b805392887fd27418e09f0aad621b94f1bb80f71f` | PASS |

## Blocking finding

`bullarium.volume-03.unit-0173.part-02.reading-order.fragment` has a marginal word fused into a body sentence on page 2, column 1, lower third. The locus sits beside the marginal summary that the SUMMARIUM lists as "Peraeta huiusmodi restilutio". The rendered body sentence reads:

> mandans ipsos per … venerabilem fratrem nostrum episcopum **Tmodj** aurinensem vicarium suura in corpora- lem possessionem induci

The marginal block itself is rendered as `P«r»euhuia«- rtetitatlo.` and lacks its middle word. The raw OCR (volume 3 `ocr.txt`, line 46091) has the row `Tmodj  rtetitatlo.`. One OCR word, `Tmodj`, combines what appears to be the body initial `T` of *Taurinensem* (the body continues `aurinensem`) with `modj`, the marginal's `modi` of *huius- modi*. Coordinate XML for that row is remote and was not consulted, so the exact glyph ownership of `T` is not settled here. Either way, marginal-summary wording stands inside a body sentence. That is blocking under addendum (a) and (f). The guidance treats a single OCR WORD joining marginal and body glyphs as an inseparable mixture that keeps the unit held for a character-geometry pass rather than admitted with a disclosure.

The other two pages of this fragment show no blocking defect. Its fragment title, missing-content notice and raw-OCR-labelled extent statement are correct.

## Addendum checks: marginal and note blocks

These counts are visual. Garbled or all-noise TAB-led marginal blocks are counted as blocks. A note block that holds two notes is counted once, with the note count given separately.

| Source ID | Marginal blocks | Note blocks | Marginal fusions | Footnote run into body |
| --- | --- | --- | --- | --- |
| `bullarium.volume-11.unit-0132.reading-order` | 7 | 8 | 0 | 0 |
| `bullarium.volume-11.unit-0136.part-02.reading-order` | 5 | 3 | 0 | 0 |
| `bullarium.volume-11.unit-0140.reading-order` | 3 | 1 | 0 | 0 |
| `bullarium.volume-11.unit-0143.reading-order` | 8 | 2 | 0 | 0 |
| `bullarium.volume-11.unit-0144.reading-order` | 10 | 3 | 0 | 0 |
| `bullarium.volume-11.unit-0151.reading-order` | 4 | 2 | 0 | 0 |
| `bullarium.volume-11.unit-0155.reading-order` | 3 (one all-noise) | 4 | 0 | 0 |
| `bullarium.volume-11.unit-0157.reading-order` | 4 | 1 | 0 | 0 |
| `bullarium.volume-11.unit-0163.reading-order` | 6 | 2 | 0 | 0 |
| `bullarium.volume-11.unit-0165.reading-order` | 8 | 4 | 0 | 0 |
| `bullarium.volume-11.unit-0166.reading-order` | 8 | 2 | 0 | 0 |
| `bullarium.volume-11.unit-0169.reading-order` | 8 | 4 | 0 | 0 |
| `bullarium.volume-11.unit-0171.reading-order` | 6 | 5 | 0 | 0 |
| `bullarium.volume-11.unit-0177.reading-order` | 5 (one summary split in two) | 3 | 0 | 0 |
| `bullarium.volume-11.unit-0179.reading-order` | 33 (one all-noise; one summary split in two) | 4 | 0 | 0 |
| `bullarium.volume-11.unit-0180.reading-order` | 6 (one summary split in two) | 3 | 0 | 0 |
| `bullarium.volume-11.unit-0182.reading-order` | 6 | 3 (4 notes) | 0 | 0 |
| `bullarium.volume-11.unit-0184.reading-order` | 6 (one summary split in two) | 2 | 0 | 0 |
| `bullarium.volume-11.unit-0186.reading-order` | 9 | 9 | 0 | 0 |
| `bullarium.volume-11.unit-0188.reading-order` | 4 | 3 | 0 | 0 |
| `bullarium.volume-03.unit-0173.part-02.reading-order.fragment` | 10 | 3 (4 notes) | **1** (`Tmodj`, page 2) | 0 |
| `bullarium.volume-08.unit-0090.reading-order.fragment` | 19 | 2 | 0 | 0 |
| **Total** | **178** | **73 (75 notes)** | **1** | **0** |

Two-column body text reads in natural order in every reader. Both fragments show a `Fragment:` title line. Each apparatus says "Fragment witness: part of the act is absent from this printing" and labels its extent statement's line numbers as raw OCR line numbers.

## Qualifications and non-blocking observations

- **Inline running heads, folios and signature marks** (addendum (d)) remain in every multi-leaf reader. Examples: `Ali. C. Ifi07 'liO BULLARIVM ROMANUM An. C. 1607` (unit-0132 p. 1); `An. C. 1607 PAULUS V PP. 453 An. C. 4607` inside a § 1 sentence (unit-0136.part-02); `An. C. 1610 65'l- nilLIARIUM nOMANUM An. G. 1610` interrupting the body rubric (unit-0188 p. 1); `:. 1080 r.Ri'.coniri ; XIII TP. 3^7 An. C. 1580` inside § 12 (volume-08 fragment p. 2). Signature marks also appear inside note blocks: `Bull. Bom. Voi. XI. 56` (unit-0132), `Bull. Rom. — Voi. XI. 71` (unit-0163), `Bull. nom. - Voi. XI. "9` (unit-0180). One stands inline at a § 7 paragraph break: `BuU. lìom. — Voi. XI. 72` (unit-0165 p. 2). All are recorded and non-blocking in this series.
- **Marginal blocks placed between halves of a hyphenated word or a little early/late** (addendum (d)). Hyphen-split examples: unit-0132 p. 1 (`eos-`/`dem`); volume-03 fragment p. 1 (`univer-`/`sorum`, `in-`/`vocanlibus`, `res-`/`ponderunt`); volume-03 fragment p. 2 (`Ra-`/`dicofanum`, `ve-`/`nerabilem`, `ple-`/`parie`); unit-0179 p. 5 (`in-`/`dulgentiis`); volume-08 fragment p. 1 (`maie-`/`latis`). Early or late placements: unit-0143 p. 1 (`praemissis, et` … `quibusvis`); unit-0171 p. 1. The printing breaks some summaries across a page or column boundary. Their two parts stand as separate blocks: unit-0177 p. 1, unit-0179 p. 5, unit-0180 p. 1, unit-0184 p. 1. No such block sits inside a body line.
- **Non-word OCR noise inside body lines** (addendum (f)). Examples: unit-0144 § 4 and § 7; unit-0151 § 1–2; unit-0163 § 1; unit-0165 § 3–4 and § 8; unit-0166 § 3–6; unit-0169 § 3–7; unit-0179 §§ 2, 4, 12–18; unit-0180 § 1–2; unit-0184 § 1, 3; unit-0186 § 2, 6; unit-0188 § 2–3. For each, the raw OCR places the specks on the body side of the row, and the adjacent marginal summary is complete as its own block. The two- or three-letter fragments `io` (unit-0179 p. 2, § 13) and `Al-` (unit-0179 p. 3, § 16) cannot be identified as marginal wording. The adjacent marginals read through to their ends, so these are recorded as noise of uncertain origin rather than as fusions. In the volume-08 fragment (§ 4, `om- jjì,jq j„ Ubera`), the garbled string sits body-side after a complete marginal and takes the place of the body word *nimoda*. It is recorded as garbled body text, without certainty.
- **Stray one-glyph paragraphs and all-noise blocks.** Examples: the twelve-glyph vertical run (`i ! ; 1 j [ 1 ] ! ; j ,`) before the running head in unit-0155 p. 1, and the TAB-led noise block on unit-0155 p. 2. Others are in unit-0143 p. 1, unit-0144 p. 2, unit-0165 p. 2, unit-0171 p. 2, unit-0177 p. 1, unit-0179 pp. 3–5, unit-0182 p. 1 and unit-0188 p. 1. None carries words or interrupts a word.
- **Shared blocks.** In unit-0182 p. 2 two page-foot notes share one block (`1 Haec praepositio … 2 rtepelilio …`). The raw OCR prints them on separate lines. In the volume-03 fragment p. 3, notes `(I)` and `(2)` share one block, as the printing does. Neither runs into body, synopsis or protocol text, so both are non-blocking. In unit-0177 p. 1, the final rubric line and the first address line share one paragraph; both are source heading text in source order.
- **Literal OCR loss** in unit-0179 p. 1. The exordium reads `Christianae randa prò sui munciis`: a body line is missing from the source OCR, and `randa` is the body-side tail of the lost line (raw OCR), not marginal wording.
- **Rubric spillover.** The frozen titles of unit-0144 and unit-0157 end where the OCR title block ends. Rubric text beyond them (unit-0144: `Hierosolymitanì, donec regnum An- gliae … revertahir '.`) is kept in the body after an inline running head.
- **Sparse final pages with genuine source closing:** unit-0143 p. 2, unit-0177 p. 2, unit-0179 p. 6, unit-0186 p. 3, volume-03 fragment p. 3 and volume-08 fragment p. 3. Each carries a dating clause or subscription and/or historical notes before the apparatus; none is a colophon-only page.
- **Issuer lines.** Issuer lines reproduce the frozen literal attribution, including `Paulus Papa V-`, `Pauliis Papa V,`, `Paulus Episcopus`, `Honorins eplscopns` and `Gregorins episcopus servas servorum Dei, ad perpetaam rei memoriam.`. Each still identifies the pope.
- No modern provider signature (for example "Digitized by Google"), raw `None` placeholder, clipping, overlap, tofu glyph or collapsed table was seen on any page.

## Individual page evidence

Every row is an individual full-size inspection. The ledger (`observations.jsonl`) records each page's exact raster path, PDF hash and observation text.

| Source ID | Page | PNG SHA-256 | Status |
| --- | --- | --- | --- |
| `bullarium.volume-11.unit-0132.reading-order` | 1 | `bf7097adee72f097e670282b3b2ce08a584d9861bd865587150ebaefddcf6866` | PASS |
| `bullarium.volume-11.unit-0132.reading-order` | 2 | `73651db03a76f27b4473afe77363b0bc65f7f7585f6e24f7ec9cb69ae3447e10` | PASS |
| `bullarium.volume-11.unit-0136.part-02.reading-order` | 1 | `d05e305921f668c973fab4477a0838e24be2dfd410a42f0d48ed609c6ad1059f` | PASS |
| `bullarium.volume-11.unit-0140.reading-order` | 1 | `cff2df1672aa20c2ffd3a3d4c4f92a35457474404c80da3a676dd617f1b8bb28` | PASS |
| `bullarium.volume-11.unit-0143.reading-order` | 1 | `ee5d5feb647f7dc8c188192dc9c8ebb2c54fe7ed1c4c7f8e6ce391021853b6ed` | PASS |
| `bullarium.volume-11.unit-0143.reading-order` | 2 | `431bdf0167925d46d6eebb6aea4ecb3fa9471c342f11f993d26ed5c263413556` | PASS |
| `bullarium.volume-11.unit-0144.reading-order` | 1 | `c217ae163b5a531628e6cfdb767f07343e67dd810c151a7854559506e3bbeabd` | PASS |
| `bullarium.volume-11.unit-0144.reading-order` | 2 | `a0e2aafa67fa9434fe08a9ff384b55cda8c866672789c09909d1eaefec706b1b` | PASS |
| `bullarium.volume-11.unit-0151.reading-order` | 1 | `5e5116844b19aed1650d09a61f812021883d01737f3703b6dab7d151e040bcfe` | PASS |
| `bullarium.volume-11.unit-0155.reading-order` | 1 | `4e86b15ee722756483c24acbb0fb642686a814433c06ed3d12b9946fd7f5481c` | PASS |
| `bullarium.volume-11.unit-0155.reading-order` | 2 | `cabff51baa93fa3c640603e26a0856fad54cbab273bda99afb802b5ea919e755` | PASS |
| `bullarium.volume-11.unit-0157.reading-order` | 1 | `4f6c2f7b5a20ffcdc0a82dd720578c280a04c8976f51f08fa597fa36c6f76b95` | PASS |
| `bullarium.volume-11.unit-0163.reading-order` | 1 | `22d211a65c5b7688f28ad252ff4b7c0b1dbfdbfbfbf1ee73ebb3bb6e94db07df` | PASS |
| `bullarium.volume-11.unit-0163.reading-order` | 2 | `f8806073df35a348b4bd6487a7bf8c17c6d74bdb461ed9584814b88dc952b3c3` | PASS |
| `bullarium.volume-11.unit-0165.reading-order` | 1 | `c1cd237568be72782979d4c63fcc5088024abee97f38b8f3b468d4c5e7422d4b` | PASS |
| `bullarium.volume-11.unit-0165.reading-order` | 2 | `357e5ac95b390006c83f309dba5d3871f34114400471757c75b3402cbf075db6` | PASS |
| `bullarium.volume-11.unit-0166.reading-order` | 1 | `10b09e57ab096f88a115f947e14a99bacca9c148ff7b7ca45b1fd50c625a75d0` | PASS |
| `bullarium.volume-11.unit-0166.reading-order` | 2 | `58a0cc5913e8150fe03b2dba020ff513e0190f1dbd366098773d92d8856fc89d` | PASS |
| `bullarium.volume-11.unit-0169.reading-order` | 1 | `a8d613643d6d32067b6b99bbcadf71e6c6200b6dbe3f1f66ce920c8c2d92f5d2` | PASS |
| `bullarium.volume-11.unit-0169.reading-order` | 2 | `d328b08ecd1ad89d35a27916e9aab461b1e993a164e0cacdbd627c101d2edcc1` | PASS |
| `bullarium.volume-11.unit-0171.reading-order` | 1 | `295cd5404da68655c463352318726bcb6ea6b8415925b8ad0f272422c1767863` | PASS |
| `bullarium.volume-11.unit-0171.reading-order` | 2 | `e1453a5fe936491951156ef601594bbad9f0150f88288e428f488eb45dbdd6a9` | PASS |
| `bullarium.volume-11.unit-0177.reading-order` | 1 | `102044b9b1d7c1e54b0b03884be955ff6c644a9119d3a18aef28bc78145d6969` | PASS |
| `bullarium.volume-11.unit-0177.reading-order` | 2 | `170276f5a1a9fcb6569d8a2f2d880f59ee90ba2aaaf4b81b5f0e0e6b11708a25` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 1 | `11c08f98cacd49235cb696b6b57796eb533311e698add87a95a7b6ec49592587` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 2 | `8bc1fbfc5f479377dc3a8d130ba18fcb796d8e021e149a9f9d911e44e92a28b0` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 3 | `c1ded2058c78da3d4fe931acffed8fb721115895a66d2e849645091294b4ae07` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 4 | `6911a7d0e66faa4e65711e0f94227743e8b8d913c69a1642101d7dc7de8b65eb` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 5 | `d39fd825b40eb376ba333b7026eb061fe24d4e76d82560836eca2bc8fe87b42c` | PASS |
| `bullarium.volume-11.unit-0179.reading-order` | 6 | `920edced45f5d6a41afb13269e2270f9db81e1ff9fe4d300d2a5cad9141a2959` | PASS |
| `bullarium.volume-11.unit-0180.reading-order` | 1 | `0e8399b820986e3ae796954a6cc0cb55e8448f58d535b98fe2a7bf1e377f111f` | PASS |
| `bullarium.volume-11.unit-0182.reading-order` | 1 | `bf399ec6b66a6127faf5b463c39405f6b43cb9771c8fd245a2e80bda0abf3b7b` | PASS |
| `bullarium.volume-11.unit-0182.reading-order` | 2 | `1d643ff3826f023b29aea6bac08f0b1d691bd6fb6591bd97f4a02df4f93538cd` | PASS |
| `bullarium.volume-11.unit-0184.reading-order` | 1 | `f6444e763d40adc62cb0af1d81033d5c9106f07543cd14bfd2ac306b02b6e224` | PASS |
| `bullarium.volume-11.unit-0184.reading-order` | 2 | `bf1760c0ecf672674e2f66fd0a1a0a967ed784a3b5182735db36b8b11a1637ca` | PASS |
| `bullarium.volume-11.unit-0186.reading-order` | 1 | `b7f65a1cddf13401915f85901be8a94b984634c9ef6f9b1199db07fe2d199971` | PASS |
| `bullarium.volume-11.unit-0186.reading-order` | 2 | `0c76be7b86a1a385051c227a4e472908890731ed79c7fe3244ec6647c443378f` | PASS |
| `bullarium.volume-11.unit-0186.reading-order` | 3 | `2cf93d8bef964d407780c9299522386387493176c17d8b476b96961531ef03ef` | PASS |
| `bullarium.volume-11.unit-0188.reading-order` | 1 | `7438efc0fbe8c8d54b53d9e9bebaf5f57dbc7b9948452b942f5832e144308f61` | PASS |
| `bullarium.volume-11.unit-0188.reading-order` | 2 | `96ac4f97caad839cdc43e46e5690aca0f966852f1db259aab0a1733de238bce1` | PASS |
| `bullarium.volume-03.unit-0173.part-02.reading-order.fragment` | 1 | `60316ef2e893960d8b005dda0becb78689267027aad7aa5b4385a96adae278c7` | PASS |
| `bullarium.volume-03.unit-0173.part-02.reading-order.fragment` | 2 | `23f2105aaa6107f7b4b743af1abd30137628cd56dae1424cc0cf112d95da2860` | CHANGES_REQUIRED |
| `bullarium.volume-03.unit-0173.part-02.reading-order.fragment` | 3 | `def7b058fa3ad448695991f6f4b210acb66841ce3009a57cca79c184c439db8b` | PASS |
| `bullarium.volume-08.unit-0090.reading-order.fragment` | 1 | `6c4773b95f2928319e6682a4dcd09fe91c3fa60f6cc48639bec500f8b10c3d4f` | PASS |
| `bullarium.volume-08.unit-0090.reading-order.fragment` | 2 | `b6ecf371760264d19d0b9611b8c2268a11e0ef78da0022ed42ec261963aad36d` | PASS |
| `bullarium.volume-08.unit-0090.reading-order.fragment` | 3 | `439d198d1bb81cd1424736c0b3ccd6d9af43900ba172e7f2fa1d0952c3f6d646` | PASS |

## Limitations

These are literal, uncorrected, uncollated historical OCR readers, rendered as mechanical two-column source editions. This review covers layout and the visual separation of marginal summaries, notes and furniture only. It does not collate words against the printing or a facsimile. It makes no claim about historical authentication, juridical interpretation, rights adjudication, publication, installation or deployment, and it normalizes no dates. Literal OCR corruption, odd spellings, unexpanded abbreviations and non-word noise remain as source limitations. Raw OCR text and generated TeX were consulted read-only, only to classify what the page images showed. Coordinate XML was not available locally, so the glyph-level ownership inside the fused word `Tmodj` is not settled beyond the evidence stated above. PASS concerns only the hash-bound visual review extent recorded here.
