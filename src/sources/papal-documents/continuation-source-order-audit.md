# Continuation readers: source-order audit

Audit of all 397 installed *Bullarii Romani Continuatio* readers in
`release/papal-documents.json` (corpus `bullarium-continuatio`). It looks for one
defect: marginal summaries or dates fused into body text. The audit ran on
2026-10-28 and was scratch-only; its withdrawal is recorded below. The row-level evidence is in `audit.json`.

## Result

| Vol. | Readers | Confirmed fusion | No geometry leads | Unauditable | Round 1, all leads true | Strong rule, all rounds | Strong rule, held-out round 2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| II | 33 | 0 | 32 | 1 | 5/6 | 7/7 | 2/2 |
| III | 39 | 1 | 35 | 3 | 7/8 | 9/9 | 2/2 |
| IV | 47 | 1 | 46 | 0 | 6/8 | 7/7 | 2/2 |
| V | 8 | 0 | 7 | 1 | 6/6 | 8/8 | 2/2 |
| VII | 17 | 0 | 16 | 1 | 6/6 | 8/8 | 2/2 |
| VIII | 8 | 0 | 6 | 2 | 5/6 | 7/7 | 2/2 |
| X | 8 | 0 | 7 | 1 | 6/6 | 8/8 | 2/2 |
| XI | 4 | 0 | 1 | 3 | 6/6 | 8/8 | 2/2 |
| XII | 5 | 0 | 5 | 0 | 5/6 | 7/7 | 2/2 |
| XIII | 208 | 193 | 13 | 2 | 8/8 | 32/32 | 24/24 |
| XIV | 20 | 17 | 3 | 0 | 8/8 | 16/16 | 8/8 |
| **Total** | **397** | **212** | **171** | **14** | **68/74** | **117/117** | **50/50** |

Each precision cell counts image-checked leads that were true fusions over leads
checked. Wilson 95% lower bounds:

- All leads, round 1: 0.834.
- Strong-rule leads, all rounds: 0.968.
- Held-out round 2 alone: 0.929. Round 2 is the unbiased estimate, because the
  strong rule was fixed after round 1.

The confirmed readers are 205 Latin, 5 multilingual and 2 Italian, with 333
PDF pages in all. They carry 1,462 counted fusion loci. Volumes II–XII differ
sharply from XIII–XIV:

- **II–XII (ABBYY OCR):** marginal summaries mostly sit in their own text
  blocks. The installed readers are almost free of fusion, even though each
  volume has 568–2,968 shared-line leads elsewhere. The first review seems to
  have withdrawn the fused units in these volumes.
- **XIII–XIV (Google scans):** the OCR runs the margin into the body lines.
  210 of the 228 installed readers carry confirmed fusion.

## Inputs

**Release record.** `release/papal-documents.json` lists 397 continuation
readers. Every installed PDF matched its recorded `pdf_sha256`. The file was
rewritten during the audit, at merge `4c840c2f91`, for other corpora. Its
SHA-256 is now `19bc9ccf…dce5`. All 397 continuation rows are unchanged: same
IDs, PDF paths, hashes and line ranges.

**Native XML.** No download was needed. The brief assumed the XML was cached
only for XIII. In fact the whole DjVu XML for all 11 volumes was already cached
under `.scratch/coverage_audit/continuatio/`. Each file matches the SHA-256 and
byte size in `src/sources/papal-documents/bullarium-continuatio-config.json` and
its `xml-*/artifact.toml`.

The token check is the tracked `_xml_pages`. It requires every XML WORD's
whitespace tokens to equal the next raw TXT tokens and all TXT tokens to be
consumed. It passed exactly for every volume, so no volume is unauditable for
lack of matching geometry.

Page modes are counted as reordered / held-measured / held-relaxed / unmeasured.
"Role checks" is the number of WORDs on reordered pages where the replicated
classifier was compared with the tracked proposer, and the number of
disagreements.

| Vol. | XML URL | Bytes | SHA-256 | WORDs = TXT tokens | Page modes | Role checks / disagreements |
|---|---|---:|---|---|---|---|
| II | https://archive.org/download/BRC-Tomo-02/BRC%2002_djvu.xml | 34,872,801 | `02fbf4ad057af88fceca187a4ebf1be06497da2145445cf2dd76a2bb58a1eb10` | 414,535 = 414,535 | 180 / 353 / 24 / 52 | 127,925 / 0 |
| III | https://archive.org/download/BRC-Tomo-03/BRC%2003_djvu.xml | 37,040,796 | `1b9f27141adabb1f2d47f70076d98ed75582e8414830a3929ed1dfce05043ef2` | 446,238 = 446,238 | 276 / 279 / 17 / 44 | 206,586 / 0 |
| IV | https://archive.org/download/BRC-Tomo-04/BRC%2004_djvu.xml | 50,062,723 | `158dc1e891652cdc21ce819d650fe17c512456a85e85798a8b17f412c4327371` | 609,730 = 609,730 | 452 / 340 / 10 / 32 | 336,874 / 0 |
| V | https://archive.org/download/BRC-Tomo-05/BRC%2005_djvu.xml | 30,041,923 | `7f39ecc4169760ca4f1cd4f5d9d74152929fa1c68767a913b9a1542ab3a4a2b3` | 360,190 = 360,190 | 88 / 325 / 34 / 61 | 62,262 / 0 |
| VII | https://archive.org/download/BRC-Tomo-07/BRC%2007_djvu.xml | 42,725,003 | `fcca30e839ef3465c4146b1d151b15e66721264a492971b5008b048031c5252c` | 509,367 = 509,367 | 192 / 391 / 67 / 82 | 134,358 / 0 |
| VIII | https://archive.org/download/BRC-Tomo-08/BRC%2008_djvu.xml | 34,742,056 | `c3b1161ed6f5778255e2c6888a46ca2e54f98d4b1f67aafbcb2f0a519d5b5f8f` | 410,399 = 410,399 | 73 / 389 / 38 / 92 | 50,804 / 0 |
| X | https://archive.org/download/BRC-Tomo-10/BRC%2010_djvu.xml | 13,274,538 | `56a9004801f78613e8ee739b54095b20fcf83d0b3a1ba358fdd009350bb6f639` | 159,267 = 159,267 | 58 / 126 / 16 / 61 | 37,556 / 0 |
| XI | https://archive.org/download/BRC-Tomo-11/BRC%2011_djvu.xml | 28,155,279 | `793892cbfb18c0642ad06951a02c15f2227ad6724c0438861698e3c1c9ee9fcc` | 331,556 = 331,556 | 67 / 330 / 48 / 110 | 41,529 / 0 |
| XII | https://archive.org/download/BRC-Tomo-12/BRC%2012_djvu.xml | 23,567,362 | `2529243689c778fecf151ef72cd6f69122528ced5992806c4b8ded40da0968fa` | 278,678 = 278,678 | 58 / 266 / 56 / 89 | 34,561 / 0 |
| XIII | https://archive.org/download/bub_gb_jZf1dfvcbxUC/bub_gb_jZf1dfvcbxUC_djvu.xml | 23,271,405 | `464e90af66ec412c64f2bca41b4ff6e59fe2032af72cf90742c52b277fc7ae28` | 285,608 WORDs ⇄ 300,257 tokens (multi-token WORDs) | 326 / 126 / 7 / 63 | 189,969 / 0 |
| XIV | https://archive.org/download/bub_gb_-TnrdvrpWEAC/bub_gb_-TnrdvrpWEAC_djvu.xml | 28,683,812 | `3468647b16cdbe26d9faf92a3b686322befa6eec5b56959a3a7ee7463c7dcf92` | 355,177 WORDs ⇄ 365,226 tokens (multi-token WORDs) | 229 / 205 / 15 / 190 | 145,559 / 0 |

**Geometry code.** The audit used `scripts/_bullarium_geometry.py` as committed
at HEAD: blob SHA-256 `2917e0bd401085024dd1c5ec916f1c4398223f35d0ebf0dfa692fc36c988e337`.
Another agent left an uncommitted 41-line working-tree edit to that file at
12:55. It appeared after all proposal and detector runs and was not used.

**Volume XIII calibration.** `geometry propose` reproduced the r3 cont13 recipe
page-for-page. Only the recorded proposer hash differs.

## Method

1. **Proposal.** The tracked tool was run once per volume, writing only below
   this directory:

   ```sh
   tools/bullarium geometry propose \
     --source-txt-record <ocr artifact.toml> \
     --source-xml-record <xml artifact.toml> \
     --input-map .scratch/claude-cont-audit/input-maps/input-map-volume-NN.json \
     --out .scratch/claude-cont-audit/vNN
   ```

2. **Detector mode** (`scripts/detect.py`). Every raw LF line gets the roles of
   its native WORDs:
   - **Reordered pages:** roles come from the recipe rows.
   - **Held pages:** the tracked `measure_page` and the role rules of
     `propose_page` are applied, copied rule for rule but without the page-level
     Hold. Uncertain WORDs get no role, rather than holding the whole page.
   - **Gutter-crossed pages:** measured again with the crossing limit lifted
     (held-relaxed).
   - **Pages whose envelope still fails:** these are "unmeasured", almost all
     `edge-unstable`.

   On every reordered page, the copied classifier matched the tracked
   proposer's role for every WORD: 0 disagreements over 1,367,983 WORDs in the
   11 volumes.
3. **Leads.** A lead is a raw LF line inside a reader's `physical_line_ranges`
   where body-role and margin-role WORDs share the line, and some margin WORD has
   at least 3 letters. This is the brief's definition: 1,516 leads in installed
   readers. Two leads come from an extension: a margin-only line inside a
   blank-line block that also holds a body line, which the typesetter runs into
   the paragraph.
4. **First hand check** (round 1, `samples.json`). At least 6 leads per volume,
   seeded and stratified by page mode. XIII and XIV drew from installed readers.
   II–XII drew every installed-reader lead that was fused in the PDF, then
   volume-wide leads. The round turned up two false-lead modes, with 6 false of
   74:
   - **Body made of specks or junk.** The body-role WORDs are dots or garbage,
     not printed body words (3 cases).
   - **Displaced body start.** A short body word at the start of a line, such as
     `sia`, `rem` or `ita`, sits 0.031–0.044 of the measure outside the left
     body edge. It was classified margin-left on a held page (3 cases).
5. **Strong-lead rule** (`scripts/strong.py`, fixed after round 1). A lead is
   strong when all of these hold:
   - it is a shared raw line;
   - some body-role WORD has at least 3 letters;
   - some margin WORD with at least 3 letters is margin-right, or is margin-left
     and starts at least 0.08 of the measure outside the left body edge.

   In round 1, every true margin-left WORD started at least 0.12 of the measure
   outside the edge. The rule excludes all 6 round-1 false leads.
6. **Second hand check** (round 2, `samples2.json`, held out from the rule):
   - one strong lead from every XIII/XIV reader confirmed only by held-page
     leads that round 1 had not already covered (21 in XIII, 5 in XIV);
   - 2–3 seeded random strong leads per volume.

   All 50 were true. Every confirmed reader whose counted loci lie only on held
   pages (24 in XIII, 9 in XIV) has at least one image-checked true locus.
7. **Native page images.** 123 leaves were fetched from archive.org as whole
   `*_jp2.zip` members. Each was hashed as received and converted to JPEG at the
   XML page size. Every receipt (`images/vNN/leaf-NNNN.receipt.json`) records the
   URL, JP2 byte size, JP2 SHA-256 and JPEG SHA-256. Each lead was viewed as a
   crop: margin WORDs boxed red, the raw line boxed green. The crops are stacked
   in the hashed composites `images/vNN/*composite-*.png` and
   `images/review/*.png`.
8. **PDF mapping** (`scripts/pdfmap.py`). Each lead's raw line was searched in
   the installed PDF's text, with its block neighbours first and the line alone
   second:
   - `pdftotext -layout`, split at the page gutter, left column then right;
   - plain `pdftotext` as a fallback.

   Matching ignores whitespace and hyphens and applies NFKC. This is exactly
   what the release's text-fidelity method declares. All 1,518 detector leads, plus the one
   inseparable WORD below, were found in their PDFs, which gives the page and the
   PDF literal. A lead counts as
   "fused in PDF body text" when the matched span joins its margin WORDs to body
   words of the same raw line, or to an adjacent body line in the same paragraph.
9. **Rendered-PDF check** (`scripts/pdfcrop.py`, `pdfpages/`). 23 readers were
   checked: XIII ×13, XIV ×5, III ×1, IV ×2, V ×1, VII ×1. For each, the whole
   PDF page was rendered with `pdftoppm -r 110` and the fragment was located
   with `pdftotext -bbox`. A crop was viewed and its hashes recorded.
   - **20 confirm** the marginal fragment inside a body or heading sentence.
     Examples: `homi-s««ai«num`, `prae-u*r,®r““•decessoris`,
     `incubue-cum dciuocti-rit`, `firmissima spe Tenor *on«e» adducti`.
   - **3 negative controls** show the expected non-fusion:
     - the vol. IV `sia` lead is body text;
     - the vol. V `Tenor conces ^` and vol. VII `Derogatio con-` leads are their
       own paragraphs.

## Verdict rules

**`confirmed-fusion`.** At least one lead counts. A lead counts in one of three
ways:
- it meets the strong rule and is fused in the PDF text, and no image check
  rejected it;
- it was image-checked as true marginal text and seen in a rendered PDF page
  inside a body or heading paragraph (vol. IV `line-00080003`, a block-type
  lead);
- it is an image-checked inseparable WORD found in the PDF (vol. XIII
  `line-00061499.part-01`; see Recall checks).

**`no-geometry-leads`.** No lead counts, and every worded line of the selection
is on a measured page.
- 157 of these readers had no leads at all.
- 14 had only weak leads, listed in `loci` with a disposition. 13 are
  margin-only lines with speck or junk body WORDs, typeset as their own blocks.
  The 14th, vol. IV `line-00016229` (`sia`), was rejected by image check.

**`unauditable`.** No lead counts, and some worded lines are on unmeasured pages.
All 14 are `edge-unstable`:

| Vol. | Reader | Geometry coverage |
|---|---|---:|
| II | `volume-02.line-00015940` | 93% |
| III | `volume-03.line-00006884.part-02` | 27% |
| III | `volume-03.line-00054934.part-03` | 55% |
| III | `volume-03.line-00055330.part-03` | 35% |
| V | `volume-05.line-00003390.missed-v` | 89% |
| VII | `volume-07.line-00053204` | 61% |
| VIII | `volume-08.line-00068643.part-02` | 0% |
| VIII | `volume-08.line-00069815` | 0% |
| X | `volume-10.line-00005876.part-01` | 0% |
| XI | `volume-11.line-00033598.part-02` | 53% |
| XI | `volume-11.line-00054994.part-01` | 94% |
| XI | `volume-11.line-00077357` | 36% |
| XIII | `volume-13.line-00051765.part-01` | 71% |
| XIII | `volume-13.line-00051765.part-02` | 0% |

**Heading-zone-only confirmations.** In 7 confirmed readers, every counted locus
lies before the first body-start marker (`§`, *memoriam*, a salutation or an
address). In these, a marginal date has run into the act number or the printed
synopsis (`counted_loci_heading_zone_only: true`):

- III `line-00032128`
- IV `line-00080003`
- XIII `line-00010110.part-02`
- XIII `line-00012392.part-02`
- XIII `line-00030434.part-02`
- XIII `line-00034309.part-02`
- XIII `line-00053779.part-02`

Whether these warrant withdrawal is a policy decision. The fusion is real and
visible on the page.

## Recall checks

Recall, the share of real fusions the detector finds, was not measured directly.
Two cheaper checks bound the gap.

**Marginal-summary vocabulary** (`lexicon-check.json`). In the 171 readers
without leads, the check looked for capitalised openings such as Prooemium,
Expositio pr…, Tenor conc…, Derogatio co…, Clausula s…, Ratio conc… and
Dat. die. It flagged a phrase when its line carried body, uncertain or
unmeasured WORDs and shared a block with body or unmeasured lines.
- Only 6 readers were flagged, all on unmeasured pages.
- In the raw text, each flagged phrase is a margin-only block, such as a date
  block or `Tenor conces: / Sluuis.`, not a run-in.
- No hit on a measured page suggested a missed fusion.

**Inseparable WORDs** (`inseparable-values.json`, `images/review/inseparable-check.png`).
An inseparable WORD is one OCR WORD holding both body and marginal glyphs; the
shared-line definition cannot catch it. 22 non-confirmed readers carry such
WORDs. Their values are body line-start or line-end words with stray
punctuation, plus one real fusion:
- vol. XIII leaf 465, WORD `nec'00n‘,*r*wn"1’`, which is body `nec` joined to
  the marginal `contrariorum`. It was image-checked and is seen in the rendered
  PDF as `apostolicis, nec'00n‘,*r*wn"1’ non, quatenus`. That reader is
  confirmed.
- Two other candidates were viewed and are plain body words: vol. IV `alte-`
  and vol. XIII `juscumquefaiuiliamlain`.

## Limitations

- **"No geometry leads" means only that.** Other source-order or OCR defects can
  remain in those readers:
  - Column-rule glyphs (`|`, `I`, `]`) inside lines appear, for example, in
    XIII `line-00034213`. Single-character margin tokens are filtered by
    design.
  - WORDs the classifier left uncertain on held pages are ignored.
  - Inseparable WORDs were reviewed only in non-confirmed readers.
- **Marginal blocks that split body words.** The II–XII readers keep marginal
  summaries as separate paragraphs, which is the accepted form for this series.
  But some land between the halves of a hyphenated body word, for example vol. V
  `sicut.ea- / Tenor conces ^ / sionis. / dem expositio`. This audit does not
  call that fusion. The field `info_margin_blocks_splitting_body_word` counts it
  mechanically:
  - 43 non-confirmed readers have at least one such split (II 7, III 6, IV 18,
    V 3, VII 5, VIII 1, X 1, XIII 2);
  - so do 20 confirmed readers.

  Whether this violates the "emitted at its anchor" rule in
  `guidance/papal-documents.md` is for the maintainer to decide.
- **What was checked by eye.** Most confirmed readers rest on the strong rule
  plus a mechanical PDF match, backed by the sampled precision. Not every
  confirmed reader was image-checked. The exceptions:
  - all 33 held-page-only readers have at least one image-checked locus;
  - 20 readers have rendered-PDF confirmation.
- **What the sample does and does not show.** The precision figures are
  sampled, and the per-volume samples for II–XII are small (7–9 strong leads
  each). The counts in Result are not a census of fusion in the volumes. In
  II–XII the leads outside installed readers were sampled only to estimate
  precision.
- **Image evidence is scratch only.** Page images and crops are scratch
  evidence. They are not registered, and no image collation is claimed.

## Reproduce (from the repository root)

```sh
python3 -I .scratch/claude-cont-audit/scripts/detect.py NN   # after geometry propose, per volume
python3 -I .scratch/claude-cont-audit/scripts/pdfmap.py NN
python3 -I .scratch/claude-cont-audit/scripts/sample.py && python3 -I .scratch/claude-cont-audit/scripts/sample2.py
python3 -I .scratch/claude-cont-audit/scripts/fetch.py NN [LEAF ...]
python3 -I .scratch/claude-cont-audit/scripts/crop.py NN [samples2.json r2-]
python3 -I .scratch/claude-cont-audit/scripts/pdfcrop.py
(cd .scratch/claude-cont-audit && python3 -I scripts/lexicon.py 02 03 04 05 07 08 10 11 12 13 14 && python3 -I scripts/assemble.py)
```

## Files

All paths are below `.scratch/claude-cont-audit/`.

| Path | Content |
|---|---|
| `audit.json` | One row per reader: `id`, `language`, `pdf`, `pdf_sha256`, `volume`, `verdict`, `loci` (raw line, leaf, page mode, fused raw literal, PDF page, PDF literal, disposition, image check), coverage, and evidence (`pdf_page_checks`, `source_image_checks`). Also `hand_checks` (124), `volumes` (XML pins, token check, page modes) and `summary`. |
| `vNN/recipe.json`, `vNN/running-heads.tsv` | Proposals from `tools/bullarium geometry propose`. |
| `vNN/detector.json`, `vNN/pdfmap.json` | Detector and PDF-mapping products. |
| `samples.json`, `samples2.json`, `pdfcheck-selection.json` | The checked samples. |
| `images/`, `pdfpages/` | Image evidence and receipts. |
| `lexicon-check.json`, `inseparable-values.json` | Recall checks. |
| `scripts/` | Every script used. |

## Withdrawal applied

On 2026-10-28 the 212 confirmed readers below were withdrawn from the current source plan with explicit prior-to-null supersessions in `historical-series-corrections-manifest.json`; their catalog units are specifically held and their prior admissions archived. Evidence: the coordinate audit record (SHA-256 `c15161f08b7ecbe00c8c7c33d65e7d04b1048afeb44ce1e99c8d668c478898fe`). The 14 unauditable readers stay installed pending manual page review; readers without geometry leads stay installed.

| Reader | Language | Fused loci | First locus |
|---|---|---:|---|
| `bullarium-continuatio.volume-03.line-00032128` | la | 1 | leaf 161, LF 32131: `- Dat. die tg.` |
| `bullarium-continuatio.volume-04.line-00080003` | la | 1 | leaf 427, LF 80008: `januarii 1772.` |
| `bullarium-continuatio.volume-13.line-00003320.part-01` | la | 1 | leaf 32, LF 3357: `per hanc sanctam Sedem nonnullis ;` |
| `bullarium-continuatio.volume-13.line-00004866.part-01` | la | 8 | leaf 44, LF 4870: `annovir. Dignitatibus, ct canonicis ecclesiae]` |
| `bullarium-continuatio.volume-13.line-00004866.part-02` | la | 8 | leaf 45, LF 5000: `anno vii. Revocantur nonnulla rescripta obre-` |
| `bullarium-continuatio.volume-13.line-00004866.part-03` | la | 3 | leaf 45, LF 5098: `CCCCXX. Dat. die` |
| `bullarium-continuatio.volume-13.line-00004866.part-04` | la | 9 | leaf 47, LF 5283: `aJ»o°vU. Dismembratio nonnullarum ecclesia-` |
| `bullarium-continuatio.volume-13.line-00004866.part-05` | la | 8 | leaf 48, LF 5418: `Dat. di. ccccxxin.` |
| `bullarium-continuatio.volume-13.line-00004866.part-06` | la | 2 | leaf 49, LF 5650: `§. 3. INon obstantibus constitutio- I)rro?,lio“m-` |
| `bullarium-continuatio.volume-13.line-00004866.part-09` | la | 3 | leaf 56, LF 6476: `itefcrantar §. 4. Inter caetera, quae in apo-` |
| `bullarium-continuatio.volume-13.line-00007069.part-01` | la | 1 | leaf 60, LF 7129: `- -c* ^ i^°n obstantibus constitu- cw-^»!ro rfw` |
| `bullarium-continuatio.volume-13.line-00007069.part-03` | la | 6 | leaf 63, LF 7427: `Concessio officii duplicis secundae Awo°m -` |
| `bullarium-continuatio.volume-13.line-00007069.part-04` | la | 3 | leaf 64, LF 7572: `§. 2. Nos igitur ipsos exponentes Tcnotcoot»` |
| `bullarium-continuatio.volume-13.line-00007632.part-02` | la | 6 | leaf 66, LF 7881: `Nominatio superiorum ordinis sancti. Xwi^vti.` |
| `bullarium-continuatio.volume-13.line-00008048` | la | 4 | leaf 68, LF 8075: `Expositio pr«- in Christo lilii Nostri Naapoleonis Gal-` |
| `bullarium-continuatio.volume-13.line-00008173.part-01` | la | 4 | leaf 69, LF 8185: `Praemium» §• 4; 1 atema Nostra sollicitudo` |
| `bullarium-continuatio.volume-13.line-00008173.part-02` | la | 2 | leaf 69, LF 8271: `pplicatio bonorum cappellaniae fun- .J^vii` |
| `bullarium-continuatio.volume-13.line-00008291.part-03` | la | 4 | leaf 73, LF 8810: `Jj.3. Quare Nos piis, enixisque lo- B»u6c««i.` |
| `bullarium-continuatio.volume-13.line-00008291.part-05` | la | 10 | leaf 76, LF 9146: `t 1(J, . r , 26 angulli` |
| `bullarium-continuatio.volume-13.line-00008291.part-06` | la | 13 | leaf 79, LF 9501: `anno VII. Beatifiratio venerabilis servi Dei Jo-` |
| `bullarium-continuatio.volume-13.line-00008291.part-07` | la | 10 | leaf 81, LF 9798: `* s'P,™b‘1’ Confirmatio conventionis initae inter` |
| `bullarium-continuatio.volume-13.line-00008291.part-08` | la | 6 | leaf 82, LF 9986: `CCCCXLV. Dat. die` |
| `bullarium-continuatio.volume-13.line-00010110.part-01` | la | 9 | leaf 83, LF 10136: `§. t. Ixaper exponi fecit Nobis tiiposii.p™-` |
| `bullarium-continuatio.volume-13.line-00010110.part-02` | la | 2 | leaf 85, LF 10322: `mi. dic CCCCXLVII.` |
| `bullarium-continuatio.volume-13.line-00010110.part-04` | la | 7 | leaf 89, LF 10866: `CCCCIL. - 7 tkb dit` |
| `bullarium-continuatio.volume-13.line-00011004.part-01` | la | 4 | leaf 90, LF 11031: `j. 4. Romanorum pontificum Praemium,` |
| `bullarium-continuatio.volume-13.line-00011004.part-02` | mul | 8 | leaf 91, LF 11126: `Dal. dte CCCCLL` |
| `bullarium-continuatio.volume-13.line-00011004.part-03` | la | 12 | leaf 92, LF 11254: `im. dti. CCCCLI1.` |
| `bullarium-continuatio.volume-13.line-00011004.part-04` | la | 9 | leaf 93, LF 11409: `CCCCLtn. Dal. di®` |
| `bullarium-continuatio.volume-13.line-00011575` | la | 21 | leaf 95, LF 11638: `lVM-riptio d- %. 2. Nomine modo eharissimac` |
| `bullarium-continuatio.volume-13.line-00012392.part-01` | la | 6 | leaf 100, LF 12406: `M.mortDtar 5- I . tjum Nos alias certis ra-` |
| `bullarium-continuatio.volume-13.line-00012392.part-02` | la | 2 | leaf 101, LF 12480: `I1M. die CCCCLVII.` |
| `bullarium-continuatio.volume-13.line-00012606.part-01` | la | 6 | leaf 102, LF 12613: `vii. Facultas instituendi in collegio nostrae` |
| `bullarium-continuatio.volume-13.line-00012606.part-02` | la | 6 | leaf 103, LF 12762: `am.o ni. Concessio officii , ct missae s. Ludo-` |
| `bullarium-continuatio.volume-13.line-00012892` | la | 2 | leaf 104, LF 12965: `§. 4. Volumus autem, ut praesen- Fide» haben-` |
| `bullarium-continuatio.volume-13.line-00012981.part-01` | la | 2 | leaf 104, LF 13000: `§• 4- Quum venerabilis frater Expoiitio pre` |
| `bullarium-continuatio.volume-13.line-00013710.part-01` | la | 8 | leaf 110, LF 13725: `Etpmiiio pr©- §. 4. lxupcr Nobis exponi fecit` |
| `bullarium-continuatio.volume-13.line-00013710.part-02` | la | 6 | leaf 111, LF 13841: `E*,>n»iiio pm vnum sicut Nobis dilecti` |
| `bullarium-continuatio.volume-13.line-00013710.part-03` | mul | 24 | leaf 111, LF 13901: `CCCCLXY. Dat. <j «©` |
| `bullarium-continuatio.volume-13.line-00013710.part-04` | la | 14 | leaf 114, LF 14298: `§. 4. Pro parte dilecti fdii Vin- Exponitor pri` |
| `bullarium-continuatio.volume-13.line-00014444.part-01` | la | 4 | leaf 115, LF 14457: `§. 1. Exponi Nobis nuper fece- ExpoOuo pr«` |
| `bullarium-continuatio.volume-13.line-00014444.part-02` | la | 16 | leaf 117, LF 14689: `Electio prioris generalis ordinis \\. anM vu<` |
| `bullarium-continuatio.volume-13.line-00014444.part-03` | la | 7 | leaf 119, LF 14904: `anno vil. Confirmatio privilegiorum, ct gratia-` |
| `bullarium-continuatio.volume-13.line-00015125.part-01` | la | 7 | leaf 121, LF 15191: `F.spo«itio Pre §. 2. Cum itaque, sicut Nobis` |
| `bullarium-continuatio.volume-13.line-00015125.part-03` | la | 26 | leaf 123, LF 15470: `anno vir. Novae leges servandae in nova pon-` |
| `bullarium-continuatio.volume-13.line-00015125.part-05` | la | 2 | leaf 127, LF 16062: `Concessio missae propriae beatae Ma- >uno` |
| `bullarium-continuatio.volume-13.line-00016156` | la | 33 | leaf 128, LF 16190: `8. 2. Postquam felicis recorda- Hinori* re-` |
| `bullarium-continuatio.volume-13.line-00016255.part-02` | la | 5 | leaf 132, LF 16766: `CCCCLXXVI. d... dic` |
| `bullarium-continuatio.volume-13.line-00016994.part-01` | la | 2 | leaf 134, LF 17042: `- i-C*' 3' ^os 'Psos exponentes spe- Tmcranar` |
| `bullarium-continuatio.volume-13.line-00016994.part-02` | la | 2 | leaf 135, LF 17169: `5- 2. Cum igitur nomine cha- »ns««op™` |
| `bullarium-continuatio.volume-13.line-00017297.part-02` | la | 4 | leaf 138, LF 17326: `u» tui. Concessio indulgentiae plenariae asse-` |
| `bullarium-continuatio.volume-13.line-00017412.part-01` | la | 4 | leaf 139, LF 17443: `Evposilio pre- 5. 4 . 1 vuper exponi Robis fecit d> |` |
| `bullarium-continuatio.volume-13.line-00017412.part-02` | la | 5 | leaf 140, LF 17640: `CCCCLXXXI. Dat. di.` |
| `bullarium-continuatio.volume-13.line-00017412.part-03` | la | 3 | leaf 141, LF 17771: `r 12 maii` |
| `bullarium-continuatio.volume-13.line-00018231.part-02` | la | 24 | leaf 147, LF 18599: `§. 5. Inter has saeculo decimo General™ i au` |
| `bullarium-continuatio.volume-13.line-00019546.part-02` | la | 35 | leaf 153, LF 19574: `8. t. Jn evangelicaparabola,«jua Pmmiiu».` |
| `bullarium-continuatio.volume-13.line-00019546.part-03` | la | 39 | leaf 163, LF 20915: `mm* viii. Canoni**!*1* beati Frandv j Caraariol®` |
| `bullarium-continuatio.volume-13.line-00023189.part-02` | la | 6 | leaf 187, LF 24210: `•nuo vm. tertia maii, ct undecima julii visi-` |
| `bullarium-continuatio.volume-13.line-00023189.part-03` | la | 25 | leaf 187, LF 24278: `Declaratio ampliationis ecclesiasticae i)»t dii` |
| `bullarium-continuatio.volume-13.line-00024935.part-01` | la | 1 | leaf 192, LF 25021: `§. 5. Abdicationem vpro ct unio- C'»*»"!* Cla-` |
| `bullarium-continuatio.volume-13.line-00024935.part-02` | la | 12 | leaf 193, LF 25110: `alia* liturae Florentinus <le hac jnoriah vita ,nn-` |
| `bullarium-continuatio.volume-13.line-00024935.part-03` | la | 6 | leaf 195, LF 25463: `§. 5. Nos igitur dictas exponen- T.nor conoo^` |
| `bullarium-continuatio.volume-13.line-00024935.part-04` | la | 6 | leaf 196, LF 25538: `'IsiiT" Suppressio beneficii ecclesiastici sub` |
| `bullarium-continuatio.volume-13.line-00024935.part-05` | la | 6 | leaf 198, LF 25883: `Rcintcgratio constitutionis Pii V. vi *nno VUI.` |
| `bullarium-continuatio.volume-13.line-00024935.part-06` | la | 2 | leaf 199, LF 26029: `lecti lilii moderni iniusiouarii bene cum.` |
| `bullarium-continuatio.volume-13.line-00024935.part-07` | la | 4 | leaf 200, LF 26100: `•tmo vir. loris pro dignitatibus , et canonicis` |
| `bullarium-continuatio.volume-13.line-00024935.part-08` | la | 6 | leaf 201, LF 26200: `•nno vii. Indultum utendi libro canonis in me-` |
| `bullarium-continuatio.volume-13.line-00024935.part-09` | la | 7 | leaf 201, LF 26287: `ID. Dat. die` |
| `bullarium-continuatio.volume-13.line-00024935.part-10` | it | 30 | leaf 202, LF 26392: `D, Dat. dio` |
| `bullarium-continuatio.volume-13.line-00026755.part-01` | la | 3 | leaf 205, LF 26768: `ExpQMtiopro- 5. 4. C^uum penes ordinem fra-` |
| `bullarium-continuatio.volume-13.line-00026755.part-02` | la | 2 | leaf 206, LF 26966: `§. 4. Non obstantibus constitu- D«rogaiio c*n` |
| `bullarium-continuatio.volume-13.line-00026979.part-01` | la | 5 | leaf 206, LF 26992: `§. 1. Exponi Nobis nuper fe- Rxpwiiio pre-` |
| `bullarium-continuatio.volume-13.line-00026979.part-02` | la | 6 | leaf 207, LF 27076: `DIV. Dit.` |
| `bullarium-continuatio.volume-13.line-00029444.part-02` | la | 12 | leaf 229, LF 30041: `Ti-nor meri- !• ^ .Quam vigore rescripti per I` |
| `bullarium-continuatio.volume-13.line-00030172.part-01` | la | 5 | leaf 230, LF 30189: `pr*e miiam. §• ^ AVomanorum pontificum` |
| `bullarium-continuatio.volume-13.line-00030172.part-02` | la | 6 | leaf 231, LF 30288: `iio£" Translatio missaect officii proprii hta-` |
| `bullarium-continuatio.volume-13.line-00030434.part-01` | la | 8 | leaf 232, LF 30462: `praecedentes SIOIO in ChriSlO fllftO iSostPO \lCtO-` |
| `bullarium-continuatio.volume-13.line-00030434.part-02` | la | 1 | leaf 233, LF 30567: `Hat. die ' '• DXI.` |
| `bullarium-continuatio.volume-13.line-00030434.part-03` | la | 8 | leaf 233, LF 30681: `5. t . Nuper a congregatione ve- Tenor` |
| `bullarium-continuatio.volume-13.line-00030434.part-04` | la | 3 | leaf 234, LF 30794: `Dismembratioecclesiacepiscopalis Cra- .on.°vj|L` |
| `bullarium-continuatio.volume-13.line-00030434.part-05` | la | 13 | leaf 236, LF 30973: `19 augusti f` |
| `bullarium-continuatio.volume-13.line-00031218.part-01` | la | 4 | leaf 237, LF 31258: `§. 5. Cum itaque sicut Nobis di- &p«aiopr».` |
| `bullarium-continuatio.volume-13.line-00031218.part-02` | la | 4 | leaf 238, LF 31357: `DXVI. Diu die` |
| `bullarium-continuatio.volume-13.line-00033301.part-02` | la | 3 | leaf 257, LF 34010: `Tenor eouc«*- §. 2. ISos igitur ipsos exponen-` |
| `bullarium-continuatio.volume-13.line-00033301.part-03` | la | 1 | leaf 257, LF 34107: `8. 1. Impositum Nobis nuper luo ripstiuofv»-` |
| `bullarium-continuatio.volume-13.line-00034309.part-02` | la | 1 | leaf 259, LF 34356: `Nominatio ad vitam ad titulum ex >ouo vm.` |
| `bullarium-continuatio.volume-13.line-00034614.part-01` | la | 8 | leaf 261, LF 34618: `22 re|i«'*n»brii ^ # ,` |
| `bullarium-continuatio.volume-13.line-00034614.part-02` | la | 11 | leaf 262, LF 34784: `DXXIV. Dat. die` |
| `bullarium-continuatio.volume-13.line-00035940` | mul | 26 | leaf 271, LF 35967: `§. \ . il uper exponi fecerunt No* Expando P«` |
| `bullarium-continuatio.volume-13.line-00036073.part-02` | la | 7 | leaf 273, LF 36202: `'DXXVn, Dat die` |
| `bullarium-continuatio.volume-13.line-00036073.part-03` | la | 4 | leaf 274, LF 36333: `Exfotitio pre l • * • globis nuper exponi fecit J` |
| `bullarium-continuatio.volume-13.line-00036073.part-04` | la | 3 | leaf 275, LF 36494: `DXX1X. D-t. die` |
| `bullarium-continuatio.volume-13.line-00036573.part-01` | la | 3 | leaf 276, LF 36587: `Proeuiam. §. 4 . In summo apostolatus api-` |
| `bullarium-continuatio.volume-13.line-00036573.part-02` | la | 15 | leaf 277, LF 36686: `Dat- di. I DXXXL` |
| `bullarium-continuatio.volume-13.line-00036573.part-03` | la | 9 | leaf 279, LF 36942: `Dat. die » DXXXII.` |
| `bullarium-continuatio.volume-13.line-00036573.part-04` | la | 3 | leaf 280, LF 37166: `§. 5. Nos igitur, attentis desuper t«w>tcod«b` |
| `bullarium-continuatio.volume-13.line-00037259.part-01` | la | 2 | leaf 281, LF 37339: `§. 4. Non obstantibus constitutio- Derogatio` |
| `bullarium-continuatio.volume-13.line-00037259.part-02` | la | 5 | leaf 282, LF 37376: `sum t"iu. Declaratio , qaod cardinales ah orbe` |
| `bullarium-continuatio.volume-13.line-00037562.part-01` | la | 13 | leaf 283, LF 37601: `§. si. Iis vero , qui orationi hu- au* piesari*.` |
| `bullarium-continuatio.volume-13.line-00037562.part-02` | la | 32 | leaf 284, LF 37758: `Dxxxvn. Dat. die` |
| `bullarium-continuatio.volume-13.line-00040839.part-01` | mul | 6 | leaf 309, LF 41096: `Confirmatio , S- 3- Ad plenam autem modifi-` |
| `bullarium-continuatio.volume-13.line-00040839.part-02` | la | 6 | leaf 310, LF 41181: `juiio, te- §• 1 • ^*d augendam fidelium re*` |
| `bullarium-continuatio.volume-13.line-00040839.part-03` | la | 4 | leaf 310, LF 41232: `DXLin. I)il. die` |
| `bullarium-continuatio.volume-13.line-00040839.part-05` | la | 14 | leaf 313, LF 41550: `D)l- die DXLV.` |
| `bullarium-continuatio.volume-13.line-00041726.part-01` | la | 2 | leaf 314, LF 41742: `iProenAro §. Illud Nos memoria repeten-` |
| `bullarium-continuatio.volume-13.line-00041726.part-02` | la | 6 | leaf 316, LF 42010: `ancto ix. Concessio facultatis altematim abscn-` |
| `bullarium-continuatio.volume-13.line-00044282` | la | 6 | leaf 333, LF 44352: `§. 3. Nec non eisdem nunc , et Dr*;gna»>* aic` |
| `bullarium-continuatio.volume-13.line-00044637.part-01` | la | 4 | leaf 335, LF 44657: `I- i. Romanorum pontificuir p.0,m;am` |
| `bullarium-continuatio.volume-13.line-00044637.part-02` | la | 9 | leaf 336, LF 44752: `Facultas aggregandi, ct conferendi MUO n.` |
| `bullarium-continuatio.volume-13.line-00044637.part-03` | la | 8 | leaf 337, LF 44867: `DLV. Dat. die` |
| `bullarium-continuatio.volume-13.line-00045029.part-01` | la | 1 | leaf 338, LF 45048: `$. 4. Nobis expositum est no- f*pom»o pre-` |
| `bullarium-continuatio.volume-13.line-00045029.part-02` | la | 4 | leaf 339, LF 45165: `DLV1I. Dat. di.` |
| `bullarium-continuatio.volume-13.line-00045029.part-03` | la | 7 | leaf 340, LF 45262: `DLVI1I . Dat. die` |
| `bullarium-continuatio.volume-13.line-00045029.part-04` | la | 2 | leaf 341, LF 45402: `DLIX Dat. ilia` |
| `bullarium-continuatio.volume-13.line-00045555.part-01` | la | 4 | leaf 345, LF 45671: `ci»uhiU si»l* §. Decernentes ipsas prae-` |
| `bullarium-continuatio.volume-13.line-00045555.part-02` | la | 4 | leaf 345, LF 45708: `DLXI. Dat. dic` |
| `bullarium-continuatio.volume-13.line-00045885.part-01` | it | 5 | leaf 348, LF 45902: `«uno xv. Gratiarum aclio Deo omnipotenti fa-` |
| `bullarium-continuatio.volume-13.line-00045885.part-02` | la | 9 | leaf 349, LF 46068: `Subjectio capituli parochialis ecclesiae anno XV*` |
| `bullarium-continuatio.volume-13.line-00045885.part-04` | mul | 6 | leaf 351, LF 46359: `Concessio juris privativi colligendi m^xv.` |
| `bullarium-continuatio.volume-13.line-00045885.part-05` | la | 8 | leaf 353, LF 46549: `Dat. dic DLXV1.` |
| `bullarium-continuatio.volume-13.line-00046688.part-02` | la | 32 | leaf 354, LF 46731: `Memomur ... S- »•. »«1«* *<»lri pastoralis ofi` |
| `bullarium-continuatio.volume-13.line-00046688.part-03` | la | 2 | leaf 357, LF 47128: `e.oim.um $ i- Xlomanorum pontificum` |
| `bullarium-continuatio.volume-13.line-00046688.part-04` | la | 3 | leaf 359, LF 47407: `ut niractano- 1- nnitas, indubitata Sedis a posto-` |
| `bullarium-continuatio.volume-13.line-00046688.part-05` | la | 5 | leaf 359, LF 47441: `DLXX. Dat. «Kf*` |
| `bullarium-continuatio.volume-13.line-00046688.part-06` | la | 9 | leaf 360, LF 47548: `25 ««ptcmbrfi DLXXI.` |
| `bullarium-continuatio.volume-13.line-00046688.part-07` | la | 5 | leaf 362, LF 47842: `•odo *xt. Assignatio fructuum ex multiplico` |
| `bullarium-continuatio.volume-13.line-00046688.part-08` | la | 12 | leaf 363, LF 48010: `DLXXIII. Dat. d .` |
| `bullarium-continuatio.volume-13.line-00048295` | la | 1 | leaf 365, LF 48320: `2. Cuin itaque , sicut dilecti FxpoiiiK>|»*-` |
| `bullarium-continuatio.volume-13.line-00048420.part-01` | la | 2 | leaf 366, LF 48445: `§. 2. Quum itaque ad Tarum , quo Tenor oou««*-` |
| `bullarium-continuatio.volume-13.line-00048420.part-02` | la | 3 | leaf 367, LF 48500: `n*u dic DLXXYI.` |
| `bullarium-continuatio.volume-13.line-00048420.part-03` | la | 14 | leaf 368, LF 48743: `5. I . Dtidum a felicis recorda- Tenor lii.r.-` |
| `bullarium-continuatio.volume-13.line-00049036.part-02` | la | 7 | leaf 372, LF 49181: `•ouo xv Applicatio legati pii missarum in au-` |
| `bullarium-continuatio.volume-13.line-00049036.part-03` | la | 8 | leaf 373, LF 49310: `ann« *xv. Assignatiobonorum, exqnorum reddi` |
| `bullarium-continuatio.volume-13.line-00049438.part-01` | la | 7 | leaf 374, LF 49503: `§. 2. Nos igitur firmissima spe Tenor *on«e»` |
| `bullarium-continuatio.volume-13.line-00049438.part-02` | la | 8 | leaf 375, LF 49630: `Concessio collaris violacei, et crocis Mooxr.` |
| `bullarium-continuatio.volume-13.line-00049730.part-01` | la | 4 | leaf 376, LF 49734: `anmaiv Communicatio privilegiorum apostoli-` |
| `bullarium-continuatio.volume-13.line-00049984` | la | 1 | leaf 378, LF 50066: `§. 2. Nos igitur ipsum moder- «wmi*` |
| `bullarium-continuatio.volume-13.line-00050114.part-02` | la | 3 | leaf 379, LF 50155: `«boVIv. Magistratui civitatis Anagninae in-` |
| `bullarium-continuatio.volume-13.line-00050114.part-03` | la | 8 | leaf 380, LF 50274: `«nuoiv. Concessio coenobii nuncupati beatae` |
| `bullarium-continuatio.volume-13.line-00050114.part-04` | la | 1 | leaf 382, LF 50567: `u»ra>i um. tionibus,et ordinationibus apostolicis,` |
| `bullarium-continuatio.volume-13.line-00050591.part-01` | la | 4 | leaf 382, LF 50607: `n*** «JUr 5- 1 • \"uoniam ob longam va-` |
| `bullarium-continuatio.volume-13.line-00050591.part-02` | la | 7 | leaf 383, LF 50723: `I)ti. die DLXXXIX.` |
| `bullarium-continuatio.volume-13.line-00050591.part-03` | la | 12 | leaf 384, LF 50809: `maaiv Concessio facultatum pro superiore` |
| `bullarium-continuatio.volume-13.line-00050915` | la | 3 | leaf 384, LF 50936: `§. t. Exponi Nobis nuper fe- Eirciiio p»` |
| `bullarium-continuatio.volume-13.line-00051001.part-02` | la | 7 | leaf 385, LF 51008: `Erectio clericorum regularium Socie- »rao xr.` |
| `bullarium-continuatio.volume-13.line-00051001.part-03` | la | 5 | leaf 388, LF 51235: `D*». dtp Dxan.` |
| `bullarium-continuatio.volume-13.line-00051001.part-04` | la | 11 | leaf 389, LF 51389: `DXCIV . Dat. die` |
| `bullarium-continuatio.volume-13.line-00051001.part-05` | la | 5 | leaf 390, LF 51498: `»’"xvi seminarii in civitatae Aqui-` |
| `bullarium-continuatio.volume-13.line-00052095` | la | 2 | leaf 395, LF 52208: `iw>q»iineon S* 4. Non obstantibus conslitu-` |
| `bullarium-continuatio.volume-13.line-00052224` | la | 7 | leaf 395, LF 52240: `cu,r,,,'° fre lectorum filiorum moderni cleri ^ ct` |
| `bullarium-continuatio.volume-13.line-00052339.part-02` | la | 7 | leaf 397, LF 52456: `•una^xvi. Applicatio nonnullorum bonorum jam` |
| `bullarium-continuatio.volume-13.line-00052627.part-01` | la | 4 | leaf 398, LF 52716: `§. 5. Auditis itaque nonnullis c*nc**-` |
| `bullarium-continuatio.volume-13.line-00052627.part-02` | la | 4 | leaf 400, LF 52919: `imminutio festorum in districtu vi- xvt.` |
| `bullarium-continuatio.volume-13.line-00052627.part-03` | la | 18 | leaf 401, LF 53078: `. 13 jortii` |
| `bullarium-continuatio.volume-13.line-00053779.part-01` | la | 8 | leaf 407, LF 53783: `iJt Confirmatio decretorum editorum a` |
| `bullarium-continuatio.volume-13.line-00053779.part-02` | la | 1 | leaf 408, LF 53931: `taiio xvi. Allocutio habita io cousistorio secreto` |
| `bullarium-continuatio.volume-13.line-00053779.part-03` | la | 3 | leaf 409, LF 54070: `•nno \VL Facultas empbithenticandi mola m fru-` |
| `bullarium-continuatio.volume-13.line-00054210` | la | 4 | leaf 410, LF 54265: `|. 2. Nos igitur attentis desuper .Unot MBeei` |
| `bullarium-continuatio.volume-13.line-00054374` | la | 3 | leaf 412, LF 54466: `mWiiitm*, et lanarum cathcdralium , et collegiate-` |
| `bullarium-continuatio.volume-13.line-00054504.part-01` | la | 3 | leaf 412, LF 54521: `Rilio , « to- $• H ♦ Ad augendam fidelium I` |
| `bullarium-continuatio.volume-13.line-00054504.part-02` | la | 1 | leaf 413, LF 54711: `nonicos desuper a quoquam quovis um imum,` |
| `bullarium-continuatio.volume-13.line-00054504.part-03` | la | 10 | leaf 414, LF 54756: `Dnt die DCXin. I` |
| `bullarium-continuatio.volume-13.line-00055050` | la | 6 | leaf 417, LF 55191: `Monitura »p« 3. Quum autem ecclesia, ve- I` |
| `bullarium-continuatio.volume-13.line-00055286.part-01` | la | 1 | leaf 417, LF 55307: `$. t . In supremo apostolicae di- proemj**` |
| `bullarium-continuatio.volume-13.line-00055286.part-02` | la | 5 | leaf 421, LF 55854: `DCXVL Dlt. ai*` |
| `bullarium-continuatio.volume-13.line-00055952.part-01` | la | 3 | leaf 422, LF 55967: `p ra-emim S- L An sanctae apostolicae Se-` |
| `bullarium-continuatio.volume-13.line-00055952.part-02` | la | 8 | leaf 423, LF 56053: `Dit. die DCXVIII.` |
| `bullarium-continuatio.volume-13.line-00055952.part-04` | la | 4 | leaf 424, LF 56238: `‘ BCXX. 'i' * mt.fc` |
| `bullarium-continuatio.volume-13.line-00057590.part-02` | la | 4 | leaf 438, LF 57994: `Concessio novorum indumentorum ,nno xvi.` |
| `bullarium-continuatio.volume-13.line-00057590.part-04` | la | 14 | leaf 441, LF 58317: `rut di, DCXXIV.` |
| `bullarium-continuatio.volume-13.line-00057590.part-05` | la | 4 | leaf 442, LF 58529: `. 1 5 wpMmfaril` |
| `bullarium-continuatio.volume-13.line-00058622.part-01` | la | 2 | leaf 444, LF 58755: `riaonli iol>- 5- 4. Decernentes insuper ipsasprae-` |
| `bullarium-continuatio.volume-13.line-00058622.part-02` | la | 5 | leaf 444, LF 58822: `Ampliatio facultatis jam concessae ca- »uno .\vi,` |
| `bullarium-continuatio.volume-13.line-00058882.part-02` | la | 4 | leaf 445, LF 58986: `2. Cum itaque sicut Nobis nu- E*pwUi*pr*` |
| `bullarium-continuatio.volume-13.line-00059074.part-01` | la | 2 | leaf 447, LF 59182: `Dei ito eoa $. A. ISon obstantibus constitu-` |
| `bullarium-continuatio.volume-13.line-00059074.part-02` | la | 3 | leaf 447, LF 59200: `DCXXX. • Dat. <!'•` |
| `bullarium-continuatio.volume-13.line-00059074.part-03` | la | 7 | leaf 448, LF 59350: `Confirmatio concessionis emphitheu- ann0 xyi.` |
| `bullarium-continuatio.volume-13.line-00059074.part-04` | la | 4 | leaf 450, LF 59624: `Dcxxxn. dic` |
| `bullarium-continuatio.volume-13.line-00059758` | la | 5 | leaf 452, LF 59844: `CnmmiiMo $' 2' f'as ‘«‘hir dictum expo-` |
| `bullarium-continuatio.volume-13.line-00059903.part-01` | la | 26 | leaf 452, LF 59907: `Declaratio partis primae cap. -1 5. S- 5- «njivt.` |
| `bullarium-continuatio.volume-13.line-00059903.part-02` | la | 5 | leaf 455, LF 60228: `uno ivi. Extensio facultatis alienandi non nul-` |
| `bullarium-continuatio.volume-13.line-00059903.part-03` | la | 17 | leaf 456, LF 60410: `Consulitur nominationibus vicario- «nno'1'vi.` |
| `bullarium-continuatio.volume-13.line-00059903.part-04` | la | 12 | leaf 458, LF 60659: `DCXXXVH. DH.au.,` |
| `bullarium-continuatio.volume-13.line-00061499.part-01` | la | 1 | leaf 465, LF 61581: `ordinationibus apostolicis, nec'00n‘,*r*wn"1’ non ,` |
| `bullarium-continuatio.volume-13.line-00061499.part-04` | la | 10 | leaf 467, LF 61788: `Commutatio in commendatu benelicu xvi.` |
| `bullarium-continuatio.volume-13.line-00062060.part-02` | la | 3 | leaf 471, LF 62248: `Confirmatio resolutionis captae a capi- xvi` |
| `bullarium-continuatio.volume-13.line-00062312.part-02` | la | 3 | leaf 472, LF 62391: `§. 2. Cum itaque sicut Nobis ex- Expono pr«` |
| `bullarium-continuatio.volume-13.line-00062312.part-03` | la | 3 | leaf 473, LF 62469: `Amu a* »DCXLVIl.` |
| `bullarium-continuatio.volume-13.line-00062312.part-04` | la | 9 | leaf 474, LF 62633: `DCXLVm. Dat. «i«` |
| `bullarium-continuatio.volume-13.line-00062312.part-05` | la | 5 | leaf 475, LF 62788: `DCIL. Dat. die` |
| `bullarium-continuatio.volume-13.line-00062978.part-01` | la | 4 | leaf 477, LF 62996: `pre ,` |
| `bullarium-continuatio.volume-13.line-00062978.part-04` | la | 7 | leaf 489, LF 64436: `T)al. die DCL11I.` |
| `bullarium-continuatio.volume-13.line-00062978.part-06` | la | 6 | leaf 493, LF 64929: `•“»» xvi collaris violacei pro dignitati-` |
| `bullarium-continuatio.volume-13.line-00065071.part-01` | la | 2 | leaf 494, LF 65092: `Y-xposiito pre $• Kixpoiii nobis nuper fecit` |
| `bullarium-continuatio.volume-13.line-00065071.part-02` | la | 4 | leaf 495, LF 65300: `§. 4. Nos sperantes ex pia insti- Tenor ««ee*-` |
| `bullarium-continuatio.volume-14.line-00004115.part-03` | la | 5 | leaf 40, LF 4431: `mino xvii Concessili Tiovorum insignii] m prò` |
| `bullarium-continuatio.volume-14.line-00007104.part-01` | la | 4 | leaf 61, LF 7109: `XVII iConfirmatio privilegiorum piac socie-` |
| `bullarium-continuatio.volume-14.line-00007367` | la | 5 | leaf 63, LF 7371: `5iài6. Concessio indulgentiae plenariae as- j` |
| `bullarium-continuatio.volume-14.line-00028699.part-02` | la | 3 | leaf 215, LF 28837: `DCLXXXY n -bfci` |
| `bullarium-continuatio.volume-14.line-00028699.part-04` | la | 6 | leaf 217, LF 29041: `roora.u». pjcc nierilis licei imparihus consti-` |
| `bullarium-continuatio.volume-14.line-00033764.part-02` | la | 4 | leaf 254, LF 33946: `xtil XJnio honorum duornm simplicium` |
| `bullarium-continuatio.volume-14.line-00034086.part-01` | la | 1 | leaf 255, LF 34153: `cordationis Benedirti pp. XIV. prae- u*r,®r““•` |
| `bullarium-continuatio.volume-14.line-00036809.part-01` | la | 6 | leaf 275, LF 36821: `hwIvìl Applicalo honorum canonica tu* va*` |
| `bullarium-continuatio.volume-14.line-00040876.part-01` | la | 4 | leaf 307, LF 40906: `Expaiiti* pre- ijjjj archipresby ter , et canonici insi-` |
| `bullarium-continuatio.volume-14.line-00042032.part-03` | la | 2 | leaf 318, LF 42631: `Dat- ^io '■ nccxxrv. ’i ì` |
| `bullarium-continuatio.volume-14.line-00045176.part-05` | la | 2 | leaf 355, LF 47367: `■ano xviii. Confirmatio superiori* eletti a mo-` |
| `bullarium-continuatio.volume-14.line-00045176.part-06` | la | 3 | leaf 356, LF 47513: `.n... xtuu Facultas nomlnandi cxtraneum sacer-` |
| `bullarium-continuatio.volume-14.line-00045176.part-07` | la | 4 | leaf 357, LF 47621: `uu» imi. buppressio , cl divisto inter patronos` |
| `bullarium-continuatio.volume-14.line-00053407.part-03` | la | 3 | leaf 403, LF 53778: `■ S- 4- Ex certa itaqne scienlia , Te««r cancri` |
| `bullarium-continuatio.volume-14.line-00078003.part-02` | la | 5 | leaf 584, LF 78359: `•am aviti Facultas concessa dignitatihus , et` |
| `bullarium-continuatio.volume-14.line-00078003.part-03` | la | 5 | leaf 585, LF 78501: `» dcc«mbc«* ' « ' * .` |
| `bullarium-continuatio.volume-14.line-00078623.part-03` | la | 7 | leaf 591, LF 79191: `DCCLXVIII. »«• Jie` |

Unauditable readers kept installed:

- `bullarium-continuatio.volume-02.line-00015940` (geometry coverage 0.9297)
- `bullarium-continuatio.volume-03.line-00006884.part-02` (geometry coverage 0.2685)
- `bullarium-continuatio.volume-03.line-00054934.part-03` (geometry coverage 0.5532)
- `bullarium-continuatio.volume-03.line-00055330.part-03` (geometry coverage 0.3514)
- `bullarium-continuatio.volume-05.line-00003390.missed-v` (geometry coverage 0.8854)
- `bullarium-continuatio.volume-07.line-00053204` (geometry coverage 0.6056)
- `bullarium-continuatio.volume-08.line-00068643.part-02` (geometry coverage 0.0)
- `bullarium-continuatio.volume-08.line-00069815` (geometry coverage 0.0)
- `bullarium-continuatio.volume-10.line-00005876.part-01` (geometry coverage 0.0)
- `bullarium-continuatio.volume-11.line-00033598.part-02` (geometry coverage 0.5333)
- `bullarium-continuatio.volume-11.line-00054994.part-01` (geometry coverage 0.9448)
- `bullarium-continuatio.volume-11.line-00077357` (geometry coverage 0.3587)
- `bullarium-continuatio.volume-13.line-00051765.part-01` (geometry coverage 0.7063)
- `bullarium-continuatio.volume-13.line-00051765.part-02` (geometry coverage 0.0)

## Held readers audited before installation

On 2026-10-28 the same method audited the 199 continuation readers that had passed page review but were held from installation (coordinate audit record SHA-256 `cc9257b13336248119137c1547d0e7a96894d057e15c031ff1f3336003637db3`; strong-lead precision 59/60 image-checked, cumulative 176/177). The 21 confirmed continuatio-0016 readers below are withdrawn with prior-to-null supersessions and never installed; the 8 unauditable ones stay held for manual page review. Of the 28 provider-mark corrections, 27 show confirmed fusion and stay uninstalled.

| Reader | Volume | Fused loci | First locus |
|---|---|---:|---|
| `bullarium-continuatio.volume-03.line-00078926` | III | 1 | leaf 415, LF 78929: `Dat. die tr.` |
| `bullarium-continuatio.volume-03.line-00089480` | III | 1 | leaf 473, LF 89483: `Dat. die 12.` |
| `bullarium-continuatio.volume-03.line-00093972.part-01` | III | 1 | leaf 499, LF 93975: `Dat. die 29.` |
| `bullarium-continuatio.volume-06.line-00086386.part-01` | VI | 1 | leaf 497, LF 86376: `Anno VII GConcessio indulgentia plenarim , asse-` |
| `bullarium-continuatio.volume-15.line-00059791.part-03` | XV | 3 | leaf 417, LF 59979: `iui. du Dispensatio episcopi Orthosiensis a cura` |
| `bullarium-continuatio.volume-15.line-00065860.part-02` | XV | 3 | leaf 460, LF 66076: `"Sff cietatis nuncupatae sacrae Familiae ere-` |
| `bullarium-continuatio.volume-15.line-00066523.part-01` | XV | 1 | leaf 463, LF 66542: `wtiriM olim metropolitanae ecclesiae Parisiensi` |
| `bullarium-continuatio.volume-15.line-00068796.part-03` | XV | 2 | leaf 483, LF 69282: `piL 4i« Subjectio sedis Montispessulani metropoli-` |
| `bullarium-continuatio.volume-15.line-00069498.part-01` | XV | 3 | leaf 484, LF 69500: `Cessatio juris melropolitici archiepiscopi oit st*` |
| `bullarium-continuatio.volume-15.line-00090847.part-05` | XV | 3 | leaf 595, LF 91330: `* *SS‘U dae ab illis, qui nomen dederint con-` |
| `bullarium-continuatio.volume-15.line-00093250` | XV | 2 | leaf 608, LF 93252: `Deputatio temporanei administratoris ec- r»i diu` |
| `bullarium-continuatio.volume-15.line-00097145` | XV | 2 | leaf 636, LF 97150: `XX,M exislenlium favore mulierum adscripia-` |
| `bullarium-continuatio.volume-15.line-00097575.part-02` | XV | 2 | leaf 640, LF 97733: `b«uo ei ie- cesiuni circumscripliorieri^! scn>` |
| `bullarium-continuatio.volume-19.line-00058106` | XIX | 11 | leaf 417, LF 58113: `p«t dia Regulae sequendae in distributione aquae` |
| `bullarium-continuatio.volume-19.line-00085838.part-01` | XIX | 1 | leaf 603, LF 85861: `VtimbIu Maronitarum natio a praedecesso-` |
| `bullarium-continuatio.volume-19.line-00085838.part-02` | XIX | 2 | leaf 604, LF 85948: `Pir. Jfe ' J' '` |
| `bullarium-continuatio.volume-19.line-00086108` | XIX | 2 | leaf 605, LF 86111: `s janii Encyclica litera porrecta venerabilibus fra-` |
| `bullarium-continuatio.volume-19.line-00086831.part-02` | XIX | 2 | leaf 610, LF 86907: `J. 1. Jn sublimi principis apostolo- ,rWi4` |
| `bullarium-continuatio.volume-19.line-00087543.part-01` | XIX | 4 | leaf 615, LF 87549: `n , «» r jg mpiU` |
| `bullarium-continuatio.volume-19.line-00087543.part-02` | XIX | 2 | leaf 616, LF 87654: `tut. si. Collatio muoeris legali pro insula sancti` |
| `bullarium-continuatio.volume-19.line-00087779` | XIX | 1 | leaf 617, LF 87785: `"SST* atolico.` |

Provider-mark corrections with confirmed fusion:

- `bullarium-continuatio.volume-18.line-00015238.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00015238.part-02.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00015470.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00016096.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00016498.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00016916.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00017193.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00017494.part-02.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00017701.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00017862.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00017980.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00018492.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00018761.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00019727.discovery-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00020089.discovery-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00020473.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00021533.discovery-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00021533.discovery-03.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00021533.discovery-04.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00022620.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00022878.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00023244.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00023326.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00023558.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00024403.part-01.provider-marks-omitted-v2`
- `bullarium-continuatio.volume-18.line-00024403.part-02.provider-marks-omitted-v2`

Unauditable readers held for manual review:

- `bullarium-continuatio.volume-01.line-00056519` (geometry coverage 0.7391)
- `bullarium-continuatio.volume-04.line-00113320` (geometry coverage 0.7294)
- `bullarium-continuatio.volume-04.line-00140383` (geometry coverage 0.3382)
- `bullarium-continuatio.volume-04.line-00141657.part-01` (geometry coverage 0.9545)
- `bullarium-continuatio.volume-06.line-00059641.part-02` (geometry coverage 0.4962)
- `bullarium-continuatio.volume-06.line-00060243.part-01` (geometry coverage 0.6271)
- `bullarium-continuatio.volume-06.line-00106172` (geometry coverage 0.9116)
- `bullarium-continuatio.volume-16.line-00046344` (geometry coverage 0.8428)
