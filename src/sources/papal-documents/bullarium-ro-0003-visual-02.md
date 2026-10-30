# Bullarium Romanum reading-order visual review 02 (batch bullarium-ro-0003)

**28 PASS, 0 CHANGES_REQUIRED** of 28 assigned PDFs; 46 pages individually opened at full raster size with the Read tool, zero reused. No marginal-summary fusion and no footnote run into a body, synopsis or protocol paragraph was found. The one prior finding (volume VII unit 0024 footnote fusion) is absent from its v2 replacement. Scope: lane 02 of review batch `bullarium-ro-0003`, coordinate-reconstructed readers of the Turin Bullarium Romanum: 27 from volume III (1858; Honorius III to Clement IV; derivative `reading-order-617cb85d7670`) and 1 from volume VII (1862; Pius IV; v2 derivative `reading-order-a11d40af8cde`). Review date 2026-10-28.

## Scope and method

Each assigned PNG from the repository `pdf-review` run was opened as its own full-size image (1700x2200 raster) with the Read tool before its observation was recorded. No contact sheet, thumbnail, new rasterization, source acquisition, word-level collation, text correction or date reconstruction was performed. One JSON observation per page was appended to the lane ledger `observations.jsonl` after viewing.

Each page was checked against the frozen metadata for the displayed title, the responsible issuer, the Latin label and the omission of the unresolved act date. It was also checked for:

- headings, two-column flow, gutter, margins, glyphs, clipping and overlap;
- a natural source closing;
- modern digitizer signatures and raw placeholders;
- the Bullarium reading-order addendum: (a) marginal summaries as separate TAB-led blocks, never fused into a body sentence or hyphen-split word; (b) page-foot footnotes as separate blocks at the page break; (c) natural two-column order; (d) inline running heads, folios and signature marks, and separate marginal blocks that sit between hyphen halves or slightly off their anchor; (e) fragment presentation; (f) non-word OCR noise.

All 28 documents are `printed-act`, so (e) does not apply. Only `bullarium.volume-07.unit-0024.reading-order-v2` carries a `prior_finding`.

Mechanical support was read-only and used lane-local scripts (`mech.py`, `notes_broad.py`, `leafcheck.py`, `notecount.py`, `roles.py`, `artsel.py`). Each selection was split into paragraphs from its derivative `hybrid.txt` at the manifest line ranges. The renderer sets a paragraph break between discontiguous ranges, which was confirmed in the body TeX. Each derivative's own reading-order recipe and page map were resolved through its `artifact.toml` and validation record, and the recipe role of every selected line was checked:

- Every TAB-led line maps to a margin role (ML/MR), and every non-TAB line maps to a non-margin role. There are zero mismatches and zero lines from held pages.
- The selections contain **175 TAB-led marginal blocks**, with 0 paragraphs that mix TAB-led and body lines.
- They contain **21 notes-role blocks (NL/NR)**, and each is its own paragraph with 0 mixed with body, synopsis or protocol rows.
- There are 36 inline running-head rows and 4 printer signature marks (qualifications).

The recipe records two inseparable WORDs on touched leaves: leaf 624, WORD 328595, derivative line 78348; and leaf 806, WORD 428547, line 101530. Both lie outside every assigned selection: unit 0285 starts at line 78391 and unit 0356 ends at line 101436.

The render receipt reports `text_fidelity` `pass` with no warnings for every lane PDF. Every lane log has 0 `Missing character` and 0 `Overfull` entries. No `Google`/`Digitized` string and no bare `None` occurs in any lane body TeX. This support does not replace the visual review.

## Evidence verification

All assigned PDF, receipt, frozen-manifest and raster-run digests matched the assignment pins both before and after inspection, as did every assigned page PNG digest (77 files). The before and after verification records are byte-identical.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment | `a79efd9c163e0b71697eeb6905577528850753e8694baf14c3672766462a9abb` | Scope binding, unchanged |
| Before verification record | `6992d929a4268afd603e1412c0d1aa47b04cb2d4fa60a11de4b2532f932bdb43` | PASS (77/77) |
| After verification record | `6992d929a4268afd603e1412c0d1aa47b04cb2d4fa60a11de4b2532f932bdb43` | PASS; identical digests |
| Inspection ledger `observations.jsonl` | `828dd2c094d8b894529d68ad4ad4a810df942f529373569ac0ca900aa8e8a182` | 46 unique page observations |
| Paragraph scan `mech.json` | `9e3b562026be034a21d5571029443485a1bc9cd29e412e82f81b0eddeb0623ea` | Marginal-block counts |
| Broad note scan `notes-broad.json` | `a4962fcb4d39b1e40d6f33216b0c3a8dd8138361c4ef6dadf0c121311b3c28ba` | Citation vocabulary outside note blocks |
| Role check `leafcheck.json` | `144627d77946d37a7b3efd93d4ce81099fc85ec505b809628916717c47157e07` | TAB/role consistency, leaf status |
| Note-block check `notecount.json` | `b3b6e237b0ef0f407ce2a8c0209f5045a85698ca32de7513af2e054d797ed35f` | Notes-role paragraph membership |

## PDF outcomes

Every document displays "Latin" and omits the unresolved act date. Issuer lines reproduce the printing's OCR protocol formula as frozen. OCR-damaged spellings such as `HonoriQS`, `Gregorins`, `Innocentins`, `Clemeas`, `Clemons` and `Plus` still identify the pope and are qualifications.

| Document | Pages | PDF SHA-256 | Marginal blocks | Note blocks | Status |
| --- | ---: | --- | ---: | ---: | --- |
| `bullarium.volume-03.unit-0182.reading-order` | 1 | `ce2c1719462c1f61cc456e7c4248bd354951011cda087b026de5c4b70c811336` | 2 | 1 | PASS |
| `bullarium.volume-03.unit-0183.reading-order` | 1 | `596f31670e6205cac3f18f55467678fe800399ecf49fcb822c4f3a63d73d4497` | 1 | 1 | PASS |
| `bullarium.volume-03.unit-0190.reading-order` | 3 | `0b92155030229339870988e39dd6df63bddfe01cc9eb2c18cdd5c76f7f9f531c` | 7 | 1 | PASS |
| `bullarium.volume-03.unit-0196.reading-order` | 2 | `fdfa216ab89106c3cec5f4dcce6899211b9a0991915558bab9c509de0fc86f33` | 13 | 0 | PASS |
| `bullarium.volume-03.unit-0197.part-01.reading-order` | 1 | `810895aa9b78b7dbffc681ee962c3a1aa577d695978a0263271de71f6821893a` | 1 | 0 | PASS |
| `bullarium.volume-03.unit-0228.reading-order` | 4 | `08edd3dccc357a57ac412c3c91b4fdc573859fb5bf202b8f9a71556104d9c7e9` | 25 | 0 | PASS |
| `bullarium.volume-03.unit-0235.reading-order` | 3 | `f4ffd156bedc47ba4042b578c2a1ae3743fb83b83f71a250a57f0dd5c2772a8f` | 17 | 0 | PASS |
| `bullarium.volume-03.unit-0236.reading-order` | 2 | `7742de153b354442c4b988aa319f7d36f6b25da69638dc2e49c36113e818e23f` | 8 | 1 | PASS |
| `bullarium.volume-03.unit-0252.reading-order` | 3 | `6fa1ae09db50bd09c2593c9e8037735577ba434021f3fd1a155606f4b62bb05e` | 12 | 2 | PASS |
| `bullarium.volume-03.unit-0274.reading-order` | 1 | `ee3cf55ab41c0eee02c33162a01031261b10c4309799e4a62df230e0137a3c4f` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0276.reading-order` | 1 | `45a085d47713130ea9989fe2e309cba0f1e0798b45e277f543a95fe7fa0db582` | 4 | 1 | PASS |
| `bullarium.volume-03.unit-0285.reading-order` | 1 | `ff4e14f36fb373cee49e2e24dd0a9d0af6f48e6e26433c52cce73ec11a10a678` | 2 | 1 | PASS |
| `bullarium.volume-03.unit-0288.reading-order` | 2 | `57f08144f05fddbad5e4d1828b8dbe4a35bb0514d6307f5b59a8b069668073fe` | 10 | 1 | PASS |
| `bullarium.volume-03.unit-0290.part-01.reading-order` | 1 | `a671002d56988f35d40aa6bb989f66a9503be204628d6440002a5e4b742579da` | 3 | 0 | PASS |
| `bullarium.volume-03.unit-0290.part-02.reading-order` | 1 | `e8bd5f9a7e021e5911515191b3af43b601f0a991b0c2e6918a5a0c547108c397` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0291.reading-order` | 1 | `4a45f830b3794eacdf6f57bd23326d66e4e17fa9f491355157b53bb294743c31` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0294.reading-order` | 2 | `e1670e4129ac17e8a858db88eebb12aef26f70c3bcf4510c4980185354c1aa06` | 9 | 0 | PASS |
| `bullarium.volume-03.unit-0303.reading-order` | 2 | `b19e5fe84f0ce5cd2cda875c1f6435dc6d0374520e77c63c9e0dcb9b443aa98a` | 7 | 1 | PASS |
| `bullarium.volume-03.unit-0304.reading-order` | 2 | `dfe6d79dd861c5196d4682959e0185126d15d1e4e0d054b109d76ae607425a33` | 7 | 1 | PASS |
| `bullarium.volume-03.unit-0324.reading-order` | 1 | `0f5707157e46be3718e1732215e322be0e8f31f1fbf0e275d3aad8a198306890` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0328.reading-order` | 1 | `02aea651d94c020b810881262ff8d6c1c2e6635afed6dabf5b21816f1fabf638` | 2 | 1 | PASS |
| `bullarium.volume-03.unit-0330.reading-order` | 2 | `9853b899ef1494e82a4ea563f0e5cdce53e4afd54dc4d4a5de9089f2a55df706` | 5 | 1 | PASS |
| `bullarium.volume-03.unit-0338.reading-order` | 1 | `5f395a06450f88ce065f44909bd4c19b369a9e1ca7cbadc41ca339d90b0f861c` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0345.reading-order` | 1 | `27b37408220a013871668ccce668d2271ad88f27bb08e51e1563a9902c6944ec` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0354.reading-order` | 1 | `c11aec845c6f5d6cd67414810d5deec49eed33595447f33d48883c10ebe8f3ef` | 3 | 1 | PASS |
| `bullarium.volume-03.unit-0355.reading-order` | 1 | `b0041405cc7d6dcf56d2bb0f0755a20b05df9e66556bc7fee48ec74ef63e09c6` | 3 | 0 | PASS |
| `bullarium.volume-03.unit-0356.reading-order` | 1 | `0382457d26628b5ee6582149ea90085645642b85e501d6a2f69c064aaa43b4d7` | 3 | 0 | PASS |
| `bullarium.volume-07.unit-0024.reading-order-v2` | 3 | `b93ff7a9c2ad4e777bcc49ca8f5d69c0ff56235c9c88f976298b5c98de01dcd9` | 13 | 1 | PASS |

Totals: 46 pages, 175 marginal blocks, 21 note blocks, 0 fusions.

## Prior finding

`bullarium.volume-07.unit-0024.reading-order-v2` had this prior finding: in the earlier reader, the left-column note 'i Ex Regest. in Aichiv, Vatic.' on page 1 was run into the proem paragraph after the hyphen-split 'partes uti-'.

**The prior defect is absent.** Page 1 now ends the proem paragraph at 'partes uti-'. The note follows as its own block (derivative line 12889, notes-right role), then the running head 'An. C. i%i Plus i\' pp. 107 An. c. tsei' on its own line (qualification). The body resumes 'liter intendere curamus' in a new paragraph. The preceding act's own notes ('1 Residuum omittitur ... 2 Faciendas, Cherub.', lines 12886-12887) lie between the manifest ranges and are not rendered in this reader.

## Qualifications and nonblocking observations

- **Inline furniture (addendum (d)).** 36 running-head rows appear as their own short paragraphs, each at a source page boundary and often between the halves of a hyphenated body word. 4 printer signature marks also appear:
  - unit 0236 p1: 'Bull. Rom. Voi. ni. 62', at the end of the protocol line before 'siarum';
  - unit 0252 p1: 'Bull Rom. Voi. III. 08', inside the note block after the Gattula citation;
  - unit 0288 p2: 'Bull. Rom. Voi. IH. "9';
  - unit 0303 p2: 'Bull. Rom. Voi III. 82'.

  Short stray one-glyph lines (such as `|`, `!`, `j`, `1`) near page breaks appear in units 0190, 0228, 0236, 0252 and 0303.
- **Marginal placement (addendum (d)).** Many marginal blocks are set between the halves of a hyphenated body word or just after the sentence they annotate. Each loci is listed in the ledger. Examples:
  - 0183, between 'ad' and 'Ecclesiam';
  - 0196, between 'Du-' and 'blinen.';
  - 0235 p2, at 'distin-/clum', 'cor-/rectione', 'religio-/nis' and 'In-/super';
  - 0252, at 'hono-/rem', 'aposto-/licae', 'auclo-/rilalem' and 'as-/sensus';
  - 0288 p2, at 'ec-/clesiaslicam';
  - 0291, at 'du-/cilur';
  - 0304, at 'sus-/pensos';
  - 0330, at 'po-/lesiatis';
  - 0024-v2 p3, at 'capi-/tulum'.

  Each is a complete separate block, so none is a fusion. In units 0303 and 0330, the last line of a marginal summary ('ducenda', 'bano.') does not appear in the derivative at all. This is an OCR omission, not a fusion.
- **Protocol run-on.** In units 0228 (line 60111), 0235 and 0330, the protocol opening ('Gregorins episcopus servus ...', 'Urbanus episcopus servus ...') follows the last synopsis item in the same paragraph because the derivative has no blank line there. Source order is intact, and no marginal or note text is involved. This is a qualification. In units 0328 and 0024-v2, the dating clause and the editorial 'Dat. die ...' caption share one paragraph, which is also source closing.
- **Non-word OCR noise (addendum (f)).** Short speck and show-through runs inside body lines occur in most units: for example '. . . .. ' ' . - -i i' (0182), '. ... i - -i i' (0190, inside 'cle-/menter'), and '● I ● !■ ■ ● J'' (0330, inside 'ordi-/naliones'). For every run in units 0303, 0304, 0324, 0330, 0338, 0345, 0354, 0356 and 0024-v2, the derivative's coordinate recipe assigns the WORDs to a body role (L/R), and the adjacent marginal summary is rendered as its own complete block. They are treated as non-blocking noise. Disclosed uncertainty, where letter-like fragments occur:
  - 0228 p2: 'd- ●. l'I . . l'I lu' opening the §10 continuation;
  - 0303 p1: '„ .' ^-tj ,■ i ● ● j' before 'yjUajjj Goi-l(a', where the adjacent marginal ends 'carceri manci-' without its final line;
  - 0024-v2 p2: '●. 1 ruL >● ■ ●●<./>' inside 'offi-/cialibus', and 'd-, . . .● 1 i„' before 'ignilatem'.

  None forms a recognizable marginal word, and the recipe places each in the body column. Without a facsimile they cannot be proven to be speck, show-through or marginal glyphs. They were not counted as fusions.
- **Speck rows split from body text.** In unit 0324, the first line of §1, §2 and §5 and its continuation fall in separate paragraphs. A raw OCR speck row, coordinate-assigned to body-right, opens each continuation beside the marginal rows. This is a layout qualification only.
- **Other literal OCR features.** Section numbering confusion is retained: 0228 shows §15, §14, §13 in content order 13, 14, 15, and 0294 has §5 twice. Abbreviated sanctions ('Nulli ergo ... etc.') appear in 0294, 0328, 0338, 0354, 0355, 0356 and 0024-v2. The 0356 dating clause 'nonis iunii' conflicts with the caption 'die 5 iulii'. These were retained and not repaired. The in-body editorial cross-reference '(Videm Innocentio IV, comtitut. XIV, pag. 535 1.' in 0290.part-02 is printed body text (body-right role), not a page-foot note.
- **Sparse final pages with genuine source closing.** 0190 p3, 0252 p3, 0294 p2, 0303 p2, 0304 p2, 0330 p2 and 0024-v2 p3 each carry dating and caption before the apparatus. None is a colophon-only page. Single-page acts whose right column holds only apparatus or the licence line (0182, 0197.part-01, 0290.part-01, 0328, 0338, 0355, 0356) are short documents, not layout defects.

## Individual page evidence

Every row below is an actual full-size inspection with status PASS. The ledger records the exact raster path, PDF hash and a fuller observation for each page. All PNG hashes were verified before and after viewing. "Unit" abbreviates `bullarium.volume-03.unit-NNNN.reading-order`, and `0024-v2` is `bullarium.volume-07.unit-0024.reading-order-v2`.

| Unit | Page | PNG SHA-256 | Observation |
| --- | ---: | --- | --- |
| 0182 | 1 | `74af566d8cd6b59d662c3e81a392d488768d1d3ebbeaa26fafcb5760e07adf98` | Header matches; 2 marginal blocks separate; noise run in body (f); Datum + Dat.; note '(1) Ex Regest. Valic.' own block. |
| 0183 | 1 | `9c3543e0991cc7567339393eb451afedfd7a53a8f593c1d03a8ce4a4926c3380` | Header matches; note '^l) Ex. Regest. Vatic,' own block; running head inline; 1 marginal block separate; natural close. |
| 0190 | 1 | `ec963bc58138cd09c8f4143107cf65a9f96d5e502b8e856aed86e65fcb125a0d` | Header matches; note '(I) E\ Rogpst. Vaiic.' own block; running head; marginals separate; speck run in 'cle-/menter' (f). |
| 0190 | 2 | `33e93b92692b959021e2d80cc2bac0f11b0b10d3c4ba34ed039e2e2e50ef1391` | Two running heads inline; 5 marginal blocks separate (two between hyphen halves); stray glyph lines. |
| 0190 | 3 | `c42ce21266984aaf44a73095b5b811e99215568f5b95cb21e1aec4c69d3785ba` | Sparse final page: Datum Lalerani ... + Dat. caption before apparatus. |
| 0196 | 1 | `52055f88ea598e39da3f9ad6f3e475fb80d7fa69cff99e97ee59bd737965af0d` | Header matches; 6 marginal blocks separate; running head inline; noise runs (f). |
| 0196 | 2 | `4768735689f182a046f7bb6ed38a9da36cf4845b4749f3bc2000d11c45990141` | 7 marginal blocks separate; running head inline; Dalum Reale ... + Dat. caption. |
| 0197.part-01 | 1 | `946da0555d794574aacc8937b1c7e1a5a15764d98c289122dbaaad71c8408ace` | Header (incipit title) matches; 1 marginal block; short act; Dalum Reale ... + Dat. |
| 0228 | 1 | `2a1cb76c8524eaf196506f9f35c6e5a81100f1457ed117dd0bbddff803dd06ad` | Header matches; protocol follows synopsis in same paragraph (qualification); two running heads; 4 marginal blocks separate. |
| 0228 | 2 | `4a9d6b2114090ce1d87c59487d96e9ee8eaf07a78f8f24b6d70329e04e15a4f6` | 8 marginal blocks separate; noise runs at §9/§10 (f, uncertainty disclosed); running head. |
| 0228 | 3 | `ae41942101cd428b641ef03c2eca6cde0a43295d23e363a0dad147a5e96e07e2` | 10 marginal blocks separate; literal §15/§14/§13 numbering; running head inline. |
| 0228 | 4 | `31879e0b173526400ea31565160b9322faa603dbca453123309ea39ae84e56be` | 3 marginal blocks; noise in §26 (f); running head; Datum + Dat. caption. |
| 0235 | 1 | `aad3ae3fc511751ddaf1936cfa965d1721cb69a2ada5505ba3186e586915ef22` | Header matches; protocol run-on after synopsis (qualification); 6 marginal blocks; running head. |
| 0235 | 2 | `06e90e371eadb948309217c2dab9b7eb3d27e51e40b0c3b5626eb797f3b2a9b3` | 10 marginal blocks separate (several between hyphen halves); running head inline. |
| 0235 | 3 | `e888f239f31fda27f1dd160be6f57a8c4d1f0fb63e9f98f6161a52196cf63783` | Marginal separate; running head; profession formula, sanction, Datum + Dat. |
| 0236 | 1 | `66363fbf3ef5c08ba5c299e903c3d8f2c4754da9a0204e0c886640ce1dd00885` | Header matches; signature 'Bull. Rom. Voi. ni. 62' inline; running head; 4 marginal blocks separate. |
| 0236 | 2 | `654fc8c1fb91516cfd656d87bc92971b50877013564fe72bbb7c542c46968a47` | Marginals separate; note '(i) .\Jdcndunfi forsan ...' own block; stray glyphs + running head; Dat. + caption. |
| 0252 | 1 | `020fa5059f4f56f32c264799840b9176d1801cdf3119112ff913828e6cc795ab` | Header matches; note '(I) Ex originali edidit Gattula ...' own block with signature mark; running head; 4 marginals separate. |
| 0252 | 2 | `10787688e57c3c7efe991e7568b28d7da1097ec382e9b3d256b48b2bd4d24a59` | Note '(I) Forsilan est.' own block; stray glyphs + running head; 5 marginals separate; noise (f). |
| 0252 | 3 | `cd66b534a9bf7e161ccf5873cc99c40a1f092e497253948e666168b98eb34134` | 3 marginals separate; running head; Datum Lugduni ... + Dat. caption. |
| 0274 | 1 | `70e0d8b95b6f7d959a1185d286b2ad5a243ddbc2c4e05d8048f30f90ddca2bbd` | Header matches; 3 marginals; note '{{) Ex Raynaldo ...' own block; running head; Datum + Dat. |
| 0276 | 1 | `3272e5a9fc28889f84cb3fbe75664e52e4efeac287e88153d875d8d1314bfa09` | Header matches; marginals separate; note '(1) Ex Regest. Vatiu.' own block; running head; natural close. |
| 0285 | 1 | `5daefb55e96d7dfd57e1587d5d2ac9500ebf0f4a7e311a38cf32051dd48c80af` | Header matches; 2 marginals; noise runs (f); note '(i) £.v Rrgcst. Vatic.' own block; running head; natural close. |
| 0288 | 1 | `e9df8cc3947e45b61988678dc2a52cfd42e5ca4fbefd740577ed4c52a1d85f33` | Header matches; 7 marginals separate; noise (f); note '(1) Ex Regest. Valle.' own block; running head. |
| 0288 | 2 | `ac684eec5a9d1c49436cd7bb8ce55def9add7909a29eb5bf54998be39593ed53` | Signature mark + running head inline; 3 marginals separate; Dalum Anagniae ... + Dat. |
| 0290.part-01 | 1 | `6440d6ada89e4f8bc9f968571291f6de15598eb4825562c88fe1183f4da65f53` | Header matches; 3 marginal blocks; short act; Dalum Laterani ... + Dat. |
| 0290.part-02 | 1 | `5f03888b9151c8716f1ab5a842e95d7dd7109e222ae6c718a7f10ce870d5ec1c` | Header matches; 3 marginals; in-body cross-reference is body; note '(1) Ex Regest. Vatic.' own block; running head. |
| 0291 | 1 | `ce497917a152661a853aca55fb4d8c753b44d3027ebe21a5819580c64462f50a` | Header matches; 3 marginals; Datum + Dat.; note '(1) Ex Codice Diplomat. ...' own block. |
| 0294 | 1 | `afaa3d65d501df3afcc2eba3e3d202bf2ac6367fabd81c00c801a4d8e67f541c` | Header matches; 5 marginals separate; noise (f); running head inline. |
| 0294 | 2 | `70e127ecb5ab3bba79807fd777d3f22ecddad6fbd132dec555a85d67ac02e867` | 4 marginals separate; §6-§9; Nulli ergo etc.; Dalum + Dal. caption. |
| 0303 | 1 | `72b9d0172796353a2ae07c446dce06730ac85ce7abd0e3d7afa168b8a4086553` | Header matches; 5 marginals separate; body-role noise (f, uncertainty disclosed); note '(l) Ex Dugloss. ...' own block; running head. |
| 0303 | 2 | `69b2c0ca0a4cc84bb297a7ee0c433070ee2ee02d01c9e8656155ce4e46bc950a` | 2 marginals separate; signature mark inline; Dalum Laterani ... + Dal. |
| 0304 | 1 | `73ddf62f1b1a8ed19d5fb86257410b6b8d3b5774ad20644dfdd0065800c4575a` | Header matches; 7 marginal blocks separate; body-role noise (f); note '(l) Ex Regest. Va(ic.' own block; running head. |
| 0304 | 2 | `02236fbae9b710d2de1eb696ef5977c0cc785d87182e589f3436fdf5e19515db` | Final page: end of mandate, Daium Anagniae ... + Dal. caption. |
| 0324 | 1 | `6ae578cdc7d45bbabfcceb7bb5bc5ea6ea45376a81118ca58dc729f3e15d0a67` | Header matches; 3 marginals; speck rows open §1/§2/§5 continuations (qualification); note own block; running head; natural close. |
| 0328 | 1 | `571b9ff2b8f9bc7d74fce177d50b4e17b381ce476faf50424f74505b7cb5971f` | Header matches; 2 marginals; Nulli ergo etc.; Datum + Dal. in one paragraph; note '(1) Ex Regesl. Vatic.' own block. |
| 0330 | 1 | `f6efc55d26590a1cb98d9bf387954328a893dca5b642a28120abd9fcada3ff5f` | Header matches; protocol run-on (qualification); 5 marginals separate; noise (f); note '(1) Edidit Wilkins ...' own block; running head. |
| 0330 | 2 | `31daa4b01cd229dec49d862d34a35f350f7135a5c01a401506465c39819b6945` | Sparse final page: Datum apud Urbem Veterem ... + caption before apparatus. |
| 0338 | 1 | `0dfb9338adab0a67294aa8315f54e6d8ef3ed2e5a4d9cb588d7ef08c87bc90f4` | Header matches; 3 marginals separate; body-role noise (f); Nulli ergo etc.; Dalum + Dat.; note '(I) Ex Regest. Valic.' own block. |
| 0345 | 1 | `59237d3af1c5afd1ee2e53fbb9114b69984df7982975e3631088b15429fdab43` | Header matches; 2 marginals + stray mark; note '(1) Ex Regest. Vatic.' own block; running head; Datum + Dal. |
| 0354 | 1 | `13d32b66ea30d239a039aa1eb8906b603d924458ea11a8e5b8bb59b2a0a40604` | Header matches; 3 marginals separate; body-role noise (f); Nulli ergo etc.; Dalum + caption; note '(t) Ex Regest. Vatic. — ...' own block. |
| 0355 | 1 | `1ad7cdef6161b98203f9b804576de203b6b04d1e92e82bf9b3a68e7621fae319` | Header (incipit title) matches; running head inline before protocol; 3 marginals; Nulli ergo etc.; Dalum + Dal. |
| 0356 | 1 | `f253fb0096f428075058348aaae07a6f4f97283b41c0716d5adaf71682cba8e9` | Header matches (long protocol issuer, fully visible); 3 marginals; noise (f); running head; Daium + Dal. (iunii/iulii literal conflict). |
| 0024-v2 | 1 | `24d7f0611515ded899ef3429dd68fcf3d9b7614cce00050124d7278af0fe7102` | Header matches; prior note fusion absent: note own block after 'partes uti-', running head, body resumes; 4 marginals separate. |
| 0024-v2 | 2 | `0039c7704336680243837b57dae1b83fd136d7074ff75a4668fdc98dd1d984f8` | Two running heads inline; 8 marginal blocks separate; body-role noise (f, 'ruL' uncertainty disclosed). |
| 0024-v2 | 3 | `e51e1bbb2b74787f0e0b84ed11d457a7e92b0db0552793cc68d7542d8753885f` | 2 marginals separate; noise before 'giQii(,3' (f); Nulli ergo etc.; Datum Romae ... + Dat. caption. |

## Limitations

- **Source text.** The text is literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. Spelling, OCR corruption, noise tokens, literal section numbering and the source's conflicting or damaged dates were not judged or repaired, and no date was inferred.
- **Kind of review.** This is a layout review only. It makes no word-level collation against the printing or scan and no facsimile inspection. Classifying letter-like noise as body-column OCR noise relies on the derivative's coordinate role assignment and is disclosed where uncertain.
- **Note detection.** Note detection used the recipe's notes roles and a citation-vocabulary scan. A page-foot note that the OCR or the recipe classified as body, and that carries no citation vocabulary, could escape the mechanical scan. The visual review found none.
- **No other claims.** This report makes no historical-authentication, rights, publication, installation or deployment claim. The successful render receipt and source admission are upstream evidence, not findings of this lane.
