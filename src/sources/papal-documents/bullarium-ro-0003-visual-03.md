# Bullarium Romanum reading-order visual review 03 (batch bullarium-ro-0003)

**16 PASS, 3 CHANGES_REQUIRED** of 19 assigned PDFs; 46 pages individually opened at full raster size, zero reused. All three CHANGES_REQUIRED findings are the same defect: a single native OCR WORD joins marginal-summary glyphs with the body's hyphen continuation, so the body word is emitted inside a marginal block and is missing from the body sentence (inseparable marginal/body mixture; addendum check (a) and the guidance's inseparable-mixture rule). No page-foot footnote is run into a body, synopsis or protocol paragraph, and every one of the eight `prior_finding` footnote fusions is now absent. Scope: lane 03 of review batch `bullarium-ro-0003`. Volume VII readers come from the Turin 1862 coordinate reading-order derivative `reading-order-a11d40af8cde`, volume VIII readers from the Naples 1883 derivative `reading-order-d3f5fdf5c043`.

## Scope and method

The repository `pdf-review` run produced each assigned PNG (1700x2200). Each was opened as its own full-size image with the Read tool before its observation was recorded. One JSON observation per page was then appended to the lane ledger `observations.jsonl`. The page-1 images of the two volume VII CHANGES_REQUIRED documents were opened a second time to confirm the loci that the geometry check found. No contact sheet, thumbnail, new rasterization, source acquisition, word-level collation, text correction or date reconstruction was performed.

Each page was checked against the frozen metadata for the displayed title, the responsible-issuer line and the Latin label. The unresolved act date is omitted from every title line, as the metadata requires. Each page was also checked for:

- headings, two-column flow and gutter, margins, glyphs, clipping and overlap;
- natural source closing;
- modern digitizer signatures and raw placeholders;
- the series addendum checks:
  - (a) marginal summaries set as separate TAB-led blocks and never fused into body text;
  - (b) page-foot notes set as separate blocks at the page break;
  - (c) natural two-column order;
  - (d) inline running heads, folios and signature marks, and separate marginal blocks that are mis-anchored (recorded as qualifications);
  - (e) fragment presentation;
  - (f) non-word OCR noise.

The responsible-issuer line is the printing's own protocol line ("Pius Papa IV ...", "Gregorius Papa XIII dilecto filio ..."), and it matches the metadata in every document.

Mechanical support used read-only, lane-local scripts:

- `scan.py`, `texcheck.py`: split each manifest line range of the derivative `hybrid.txt` into blank-line paragraphs. The scan counted **159 TAB-led marginal blocks** and found **0 paragraphs mixing TAB-led and body lines**. Each body TeX has exactly one `\par` per derivative paragraph. No PDF log has a `Missing character` or `Overfull \hbox` entry. No body TeX contains `Google`, `Googie`, `Digiti`/`Digili` or a bare `None`.
- `edgescan.py`, `straddle.py`, `probescan.py`: located native WORDs whose bounding boxes cross a body/marginal column edge by more than 15-20 px. They used three existing read-only geometry records: the geometry-screen page bands and native WORD cache, and the accepted-fusion-audit probes, which cover the leaves missing from the cache (vol. VII leaves 422 and 697; vol. VIII leaves 114 and 115). Each lead was traced to the derivative and the raw OCR line, and the three mixtures were confirmed on the page images. Every other crossing WORD was checked. Each is a running head spanning the page, a body word overrunning its own column end, or a marginal word whose box overhangs only an interline row of non-word specks. No other WORD carries both marginal and body glyphs.
- Leaf coverage: vol. VII leaves 204-205 are absent from the reading-order page map (no text, not reconstructed). Vol. VII leaf 698 and vol. VIII leaf 116 have no WORD geometry in either record. Only text and visual review covers them: one short closing page of `unit-0143` and the closing lines of `unit-0026`. No reconstructed lane leaf is a held raw-OCR page (all `recipe-whitespace`).

This supports, but does not replace, the visual review.

## Evidence verification

All 19 assigned PDF digests, the receipt, frozen-manifest and raster-run digests, and all 46 page PNG digests (68 files) were computed before and after inspection. Every digest matched its assignment pin both times. The before and after records list identical item hashes and differ only in their `phase` label.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment | `fd46c7413d4e906937577850e404b3c37169c2e3f0be62975fb294a313630f13` | Scope binding, unchanged |
| Before verification record | `cfea79811dfb008ad7d029f7d8ec3cd4cb7ff86aa2510503ee4e9768c5c95a9f` | PASS, 68/68 |
| After verification record | `1ff20e631d417d522ed42395f5b3ca7e2a9662d94a0ba17ba5faca1335d77cb0` | PASS, 68/68; identical item hashes |
| Inspection ledger `observations.jsonl` | `4746b82860cc764f3dc5edf2ce4c12333738089b33c2a03ae2826f348d4be794` | 46 unique page observations |
| Derivative vol. VII `reading-order-a11d40af8cde/hybrid.txt` | `a11d40af8cde81ae63a6877aa6168ea08e317d2e7cfcaac8f0f48d8f881d34a8` | Read only |
| Derivative vol. VIII `reading-order-d3f5fdf5c043/hybrid.txt` | `d3f5fdf5c0430cd6881da2914a4dbcb0b73a4ec9d229c0cc4bb22740c504c0f7` | Read only |
| Geometry screen `geometry_screen_engine/full-0001/screen.json` | `4e9b9c2b79976e83acb3c529385451918d33cecdd93bd9f372d8730e50167ff7` | Read only (leads) |
| Geometry page bands `geometry_screen_engine/full-0001/pages.json.gz` | `2a45ed55105a8df76a5658349f399967b883bda8113f1b2eefa753a77517f35b` | Read only (leads) |
| Fusion-audit probes `accepted_fusion_audit/review-07-10/probes.json` | `1b4fac8be06ff3da3841e7817f14241807acba06c7d977f151262ce2ac9d6b9f` | Read only (leads) |
| Paragraph scan `scan.json` / edge scan `edgescan.json` / TeX check `texcheck.json` | `f49bdafdf31223fb6bc1b80993e2773716b16f8f4f6b82b80a41b49430e61fa2` / `ddbe76b5a7b480d587cc303f6d19fbfcdad36e9db3cca5fcdeea83b8a32a9d19` / `3710683f7c89995fcd0cb8e0736d4412c754a423861a576c98f12b7a712ad9b1` | 159 marginal blocks, 0 mixed paragraphs; 0 missing glyphs |

## PDF outcomes

All documents display "Latin" and are `extent_kind = printed-act`. None is a historical fragment, so check (e) has no applicable document; `part-01` is a segmentation part. Counts are derivative blocks inside the selected ranges: marginal = TAB-led blocks, including stray one-glyph and running-head-fragment blocks; note = separate printed-note blocks.

| Source ID | Pages | Pages inspected | Marginal blocks | Note blocks | Prior finding | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bullarium.volume-07.unit-0040.reading-order-v2` | 4 | 1, 2, 3, 4 | 19 | 2 | yes | `82679cb29516404d1b2a8d646124f042499d4dde21cf2da2139139b0675cb48b` | PASS |
| `bullarium.volume-07.unit-0081.reading-order-v2` | 2 | 1, 2 | 6 | 1 | yes | `cd0be2caa67932123a4fb90431f6e3128b00e5228ef23b9709248519613b8ac0` | PASS |
| `bullarium.volume-07.unit-0119.reading-order-v2` | 3 | 1, 2, 3 | 14 | 3 | yes | `f30a7e8c3ec6c6f3be60b36a6b5ef696bf7d2145a6ea0b044736801927c4b816` | PASS |
| `bullarium.volume-07.unit-0143.reading-order-v2` | 2 | 1, 2 | 8 | 1 | yes | `10d865704b568cf7400e773c791247b9f6e201b2d1ba186921c48a4d0e95eacb` | CHANGES_REQUIRED |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 5 | 1, 2, 3, 4, 5 | 8 | 3 | yes | `2633161643a219d11e96d7ab0b29af936c3984c84ae127468d20a65e5e109f3a` | CHANGES_REQUIRED |
| `bullarium.volume-07.unit-0174.reading-order-v2` | 3 | 1, 2, 3 | 24 | 2 | yes | `680fbc240e49bdd7152f692660e89dda3b130b6b1578681ecce023a140dff0e8` | PASS |
| `bullarium.volume-07.unit-0205.part-01.reading-order-v2` | 2 | 1, 2 | 8 | 2 | yes | `2c95edff035f6d864accd62187612968622b6db4980103c0e7094cdd53e76c43` | PASS |
| `bullarium.volume-07.unit-0209.reading-order-v2` | 4 | 1, 2, 3, 4 | 18 | 2 | yes | `462f1e53eddc99322d0aac8f512124ea3f16b109f2a2ea8bea5c1bee95c742f3` | PASS |
| `bullarium.volume-08.unit-0002.reading-order` | 4 | 1, 2, 3, 4 | 4 | 1 | no | `36de6af316928cffa11687c754efe85474cd2ce0a079c2667d83ec40e8e5c4cf` | PASS |
| `bullarium.volume-08.unit-0004.reading-order` | 1 | 1 | 6 | 0 | no | `d0d1be91afbd5b7006c71b32290151e0cfcbe9fee6b25abda4308b2907b26e15` | PASS |
| `bullarium.volume-08.unit-0005.reading-order` | 1 | 1 | 5 | 2 | no | `314241faaf1512d8832e6158c6bfcd9e15055a8796c226fedbaf3cc15c1eb5ba` | PASS |
| `bullarium.volume-08.unit-0006.reading-order` | 2 | 1, 2 | 8 | 1 | no | `7f42414c29e4d7b25f9e036e990fbd57086e0f997ba2069994c11ee0134a5180` | PASS |
| `bullarium.volume-08.unit-0026.reading-order` | 2 | 1, 2 | 5 | 2 | no | `e1affed5bf60000239192dacd77a36573663884767bdc861139c301e2cdfb9bc` | PASS |
| `bullarium.volume-08.unit-0028.reading-order` | 1 | 1 | 4 | 1 | no | `a013b559474a3aac09e5695cf1f7daa3dd7bdea6d308feb3b9f81ddbc5e92765` | PASS |
| `bullarium.volume-08.unit-0031.reading-order` | 2 | 1, 2 | 4 | 0 | no | `2c575f8187d43041abd919d90d68b4e5ca87266df2ac9a60081d26e26bd5f852` | CHANGES_REQUIRED |
| `bullarium.volume-08.unit-0044.reading-order` | 2 | 1, 2 | 6 | 2 | no | `a00fe7a63db4586fd12c1cb5c4319a96640c982ecf159d7332b51a9688b9b78e` | PASS |
| `bullarium.volume-08.unit-0085.reading-order` | 2 | 1, 2 | 4 | 1 | no | `7b87fcef802516cab60cd3b54799aa12fbd265bc180d5967bd2cfc367ddf07e1` | PASS |
| `bullarium.volume-08.unit-0091.reading-order` | 2 | 1, 2 | 3 | 1 | no | `2b53cb80c5fe7609016a68f583166e3d3b14c5824acb1223a1c3c5e60e456f6f` | PASS |
| `bullarium.volume-08.unit-0092.reading-order` | 2 | 1, 2 | 5 | 1 | no | `a972d740233902d3319bb9c650510877a9f1931d97dd0dea01e88c7822a2a133` | PASS |

Totals: 159 marginal blocks and 28 note blocks seen. Fusions found: 3 marginal/body WORD mixtures (below); 0 footnotes run into a body, synopsis or protocol paragraph; 0 marginal words inside a body sentence; 0 interleaved note/body lines.

## Blocking findings

1. **`bullarium.volume-07.unit-0143.reading-order-v2`, page 1, left column, §1 (BLOCKING).** The marginal block `Donaiio prò serviiute, quani illa non exce- m'',;i'ur'''""''one` ends with the native WORD `m'',;i'ur'''""''one`. The WORD is on vol. VII leaf 697, number 347348, with bbox x 27-336. The marginal column there lies at x≈27-210 and the body column starts at x≈222. This one WORD joins marginal glyphs to the body continuation `...one` of hyphen-split `asser-` (raw OCR line 79517: `m'',;i'ur'''""''one constare debeai, et de quantitale,`; derivative line 80038). On the page the body reads `quarum ex eoiiiin asser- j -i t` / `constare debeai`, and the continuation is printed inside the marginal block.
2. **`bullarium.volume-07.unit-0165.reading-order-v2`, page 1, left column, §1 (BLOCKING).** The marginal block `ne. cihoii- cus hoc collo- gium prò ora- vS',TZ;«'ncbat ci doiatorai;` contains the native WORD `vS',TZ;«'ncbat` (vol. VII leaf 770, bbox x 262-600; body column starts x≈460). The WORD joins marginal glyphs with the body continuation `...ncbat` of hyphen-split `con-` (raw OCR line 88504: `vS',TZ;«'ncbat quod alias, postquam clarae me-`; derivative line 89030). On the page the body reads `petitio con- quod alias, postquam clarae me-`.
3. **`bullarium.volume-08.unit-0031.reading-order`, page 1, left column, §1 (BLOCKING).** The marginal block `rriviiegium furi prò sub- conec.nrbiiB et oniiiii »p>-i"ii-minum ci ìli repudi Nt«a- polis` contains the native WORD `»p>-i"ii-minum`. The WORD is on vol. VIII leaf 122, number 56308, with bbox x 219-463. The marginal column lies at x≈127-300 and the body column starts at x≈330. This one WORD joins marginal glyphs with the body continuation `minum` of hyphen-split `cri-` (raw OCR line 12715: `oniiiii »p>-i"ii-minum el delictorum per quoscumciiie sub-`; derivative line 12759). On the page the body reads `excessuum, cri- el delictorum per quoscumciiie sub-`.

Under the guidance, a unit containing an OCR WORD that joins marginal and body glyphs stays held for a character-geometry pass and is not admitted with a disclosure. In each of the three documents every other page is clean.

## Prior findings (footnote fusion) re-checked

Each of the eight `-v2` replacements carried a `prior_finding` for a page-foot note run into a body paragraph. The prior footnote fusion is now absent in all eight. Each prior locus is now its own note block, or the hyphen-split body word now runs on inside the body with the note set separately at the page break:

- **`unit-0040`**, p.1 left column. `t De materia liebraeorum ... pag. 498.` is its own block after `ex certa scien-`; the running head follows as its own block; the body resumes `Ma, ac de apostolicae`.
- **`unit-0081`**, p.1 left column. `i Ex Regest. in Arcliiv. Valic. — ... pag. 97.` is its own block after `si secus super bis a quo-`; the running head follows; the body resumes `quam, quavis auctoritate`.
- **`unit-0119`**, p.2. `com- munitcr` now runs on in the body. `i Leg. forte eccìesiam (r. t.).` is its own block at the right-column page break, followed by the separate note `1 Forte super dieta resignatione (r. t.).`.
- **`unit-0143`**, p.1. `lain- quain` runs on in the body. `1 Es. Kegest, in Secret. Breviuni.` is its own block at the right-column page break; its block also holds only the signature mark `Bull. Rom. Voi. VII. 81`. This document is still CHANGES_REQUIRED for the separate finding 1 above.
- **`unit-0165`**, p.2. `concernen- tia, fieri iussit` runs on in the body. `(I) Legimus dioecesi (r. t).` and `(I) Novortnn, Uipoll (r. t.).` are separate blocks at the page break. This document is still CHANGES_REQUIRED for the separate finding 2 above.
- **`unit-0174`**, p.1. The proem block ends `san-`. The note `{ Alili roform:UÌo ... consliUilionesubseq.` is its own block; the running head follows; the body resumes `ctionibusque`.
- **`unit-0205.part-01`**, p.1. The §2 block ends `certum et determinatum inte-`. `1 De poenis eiusmodi cambiorum ... pag. 207.` and `i Sua fmus addit Cherub. (b. t.).` are separate blocks; the running head follows; the body resumes `resse`.
- **`unit-0209`**, p.2. The §5 block ends `peccalorum-`. `I lliiiusmodi of/ìcia eliam addit (n. T.).` is its own block; the running head follows; the body resumes `que remissionibus`.

## Per-document notes (non-blocking qualifications)

Running heads, folios and printer signature marks left inline as their own blocks are recorded as addendum (d) qualifications in every multi-page document. Short non-word OCR noise inside body lines (`T-i 1 • 1 u ■ •`, `^ ^ ^ . . &.`, `,.,• , .`, `g[ g^jgy|Qg` and similar) is addendum (f) literal noise. In each such case the neighbouring marginal summary is complete as its own block. The ledger lists each locus by page and column. Further notable loci:

- `unit-0040`:
  - Stray marginal blocks: `.` inside the in-body heading copy; `i` between `su-`/`per` (p.3, §15); `An. C.` between `for-`/`tioribiis` (p.3).
  - Noise-led block `» ° .....` splitting §5 (p.2).
  - Final page 4 holds the dating clause and registration line.
- `unit-0119`: stray marginal `,` between `apo-`/`slolicarum`, and `Qu.uue ,` placed mid-sentence (p.1). Note `1 Legendum fortassis ex parte (r. t.)-` shares its block only with the signature mark `Bull. Rom. Voi. VII. 10` (p.2).
- `unit-0205.part-01`: stray marginal blocks `'^` and `1` mid-sentence in §1.
- `unit-0209`: stray marginal `1` between `ta-`/`men` (p.2) and `^ "` between `prae-`/`senlibus` (p.3).
- `volume-08.unit-0002`: stray marginal `•` and one-glyph `1` (p.3).
- `volume-08.unit-0004`: marginal `ConlrtTenien- liom pocuM.` between `fue-`/`riiit` (§3).
- `volume-08.unit-0005`: separately selected note lines 1622-1623 (`1 Omittilur tenor ...`) set after the registration line. The note marker is in the body (`suscepti 1.`).
- `volume-08.unit-0006`:
  - Marginal `Proicmiuiii.` sits after the first body line.
  - Stray `.` and `•` blocks, the latter between `ka-`/`lendis` in the dating clause.
  - The page 2 closing holds the cursors' publication notice and subscription.
- `volume-08.unit-0026`: note `i Ex Regest. in Secret. Brevium.` sits between `tnen-`/`nio`, and running-head fragment `An. C. 157'»` is set as a marginal block (p.2).
- `volume-08.unit-0031`: printed notes on leaf 122 (derivative lines 12747-12749, 12751) lie outside the selected ranges and do not appear. Their ownership is an upstream selection fact, not evaluated here.
- `volume-08.unit-0044`: geometry lead `ha-` checked. The marginal WORD overhangs only an interline noise row and the §4 body is intact. Signature mark `Bull Rom. Voi. Vili. -20` appears on p.2.
- `volume-08.unit-0085`: signature mark `Bull. Rom. Voi. mi. 42` runs on at the end of the §1 body block (inline mark, non-blocking).
- `volume-08.unit-0091`:
  - Note `1 Simileni eonstitutionem ...` is set as its own block where the page breaks inside the dating clause. That is an edition note at a page break, which is non-blocking.
  - Geometry lead `prò` was checked and is non-blocking.
  - Page 2 opens with a running head followed by the rest of the dating clause and the registration line.
- `volume-08.unit-0092`: stray marginal `*` inside the heading copy. Note block `1 Ex Regest. ... 2 Legendum forsan alteixandi (r. t.J.` holds two printed notes and no body text.

Every document ends with genuine source closing: a dating clause, a registration (`Dat. die ...`) line and, where printed, subscriptions or a publication notice. The project Source and licence apparatus follows. No final page holds only project notices or running-head furniture. No clipping, overlap, tofu glyph, collapsed table, stranded heading, digitizer signature or raw placeholder was seen.

## Page raster hashes

| Source ID | Page | PNG SHA-256 |
| --- | --- | --- |
| `bullarium.volume-07.unit-0040.reading-order-v2` | 1 | `db5bfad4f73d4b58842b5d647745bd8cc984f7024da8d6051fd7e9ea75ee71ee` |
| `bullarium.volume-07.unit-0040.reading-order-v2` | 2 | `39d00e736f3e52916d279a25114d02767975196e1c71213b97e4521c1d713cfd` |
| `bullarium.volume-07.unit-0040.reading-order-v2` | 3 | `274ebd4d46026139b301942ff866e1c891b0bd3870cfc5df3f2281499b159bf3` |
| `bullarium.volume-07.unit-0040.reading-order-v2` | 4 | `a510d6820a4c2e3cbf649ad7617cdcb53a979bcea6d49888a401ff9eed6b7939` |
| `bullarium.volume-07.unit-0081.reading-order-v2` | 1 | `9f7a01cbd67662358894250a5ae573a6f4f9ba059a49a985dcc812d0cd26ca3e` |
| `bullarium.volume-07.unit-0081.reading-order-v2` | 2 | `84f113813d6ce36bea8a79cf46da589b6d4ef9f4df463a3c203d03752707248b` |
| `bullarium.volume-07.unit-0119.reading-order-v2` | 1 | `9fb965fd8edbccf2101a2d075d0b90b2dc2828b5e25c664bdf232c20d758c1a7` |
| `bullarium.volume-07.unit-0119.reading-order-v2` | 2 | `b96fbbe7012df408f77b53354330bd4ecf6b9a81a1536451999c19e234ff361a` |
| `bullarium.volume-07.unit-0119.reading-order-v2` | 3 | `6971bd0ba9ede814de3f52b87a167d8abe9a99f57ea1168081ee11b029e79479` |
| `bullarium.volume-07.unit-0143.reading-order-v2` | 1 | `9679d9888bbdf51dd15028f8d7d96ab081425bd39f5a4959e59322925dd640d3` |
| `bullarium.volume-07.unit-0143.reading-order-v2` | 2 | `62dab80870b9a4bdd844f5dc4941fac051bbcdac6b7ea0722075c1868b473ba6` |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 1 | `b75a9a79305365a79cd20b9050a55fa58bac78d6c2b0b0163cc64be69da8a54e` |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 2 | `a82c0d2d74ff08eef633183667c6ac025526faba3dc316774c1696280382f223` |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 3 | `80ad00a21949cc4e55b7b6c52ee78b71d0c22f82d284096cfb509c3bfaaef274` |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 4 | `a869bd76bdc190f780a1c5aceb2090f122569df4df3e6e617c8165ecb7aa24f6` |
| `bullarium.volume-07.unit-0165.reading-order-v2` | 5 | `b9606aad793a042aac667f7d53f5fba129888010f56ee874a5452433fb7b3c38` |
| `bullarium.volume-07.unit-0174.reading-order-v2` | 1 | `6e89462d0ef44cf5a7e9ec7d72dc96e5e1f105bd7f5bbe8ea94a9e5b78e010ac` |
| `bullarium.volume-07.unit-0174.reading-order-v2` | 2 | `aaf8bb6ece954d927912ca2ac502aa064e082c6c073fcce1514e9321a8e75093` |
| `bullarium.volume-07.unit-0174.reading-order-v2` | 3 | `4206462688b549eb0e841e13052cf81b9336c8c1be248ea54d65d3983fbf4bc9` |
| `bullarium.volume-07.unit-0205.part-01.reading-order-v2` | 1 | `64f2897b922e083263bcd363ff6d6bca82dd877e138d7f3028c5188c2e6b1eec` |
| `bullarium.volume-07.unit-0205.part-01.reading-order-v2` | 2 | `33c05744080d025def2a19bbc59db46367b8daf1978f88702594405a03b8dd4c` |
| `bullarium.volume-07.unit-0209.reading-order-v2` | 1 | `e9b7ec0078983e40c9d725fc348eae09e79ce7a72c106d2c599cd321ffabde3b` |
| `bullarium.volume-07.unit-0209.reading-order-v2` | 2 | `11c0b15ae035c1fe0966b0afb77419a868230bb538bd709dfbb00aecfdc181d5` |
| `bullarium.volume-07.unit-0209.reading-order-v2` | 3 | `ccf307b295852a8047d26e8cc697b867e2749b8a50a34837fc6e220054392c80` |
| `bullarium.volume-07.unit-0209.reading-order-v2` | 4 | `b09df5f1230f97084f22b33ba5c61bce9ddedff5aa9ab1188c2a884fbf8181bb` |
| `bullarium.volume-08.unit-0002.reading-order` | 1 | `d289f4e6122250cab72daed374f263130f9028e03dbbd340d1123811b01084f8` |
| `bullarium.volume-08.unit-0002.reading-order` | 2 | `1d507575190e7455938f5ae117671d5d71fd0f4581de5d0d6d313984147f6606` |
| `bullarium.volume-08.unit-0002.reading-order` | 3 | `9e525c2bc5380f1d290f41ab1f2af0d8064484ee572cb16f701bb5f27c3d00c1` |
| `bullarium.volume-08.unit-0002.reading-order` | 4 | `498f4da05708afa19f7fe194dee11a49617e862cc0a02ef104746800c3a28ff8` |
| `bullarium.volume-08.unit-0004.reading-order` | 1 | `030b715a4db5fcf9f3dffb7ceec9630470cc6cab072636eefbbbad02f6203cc4` |
| `bullarium.volume-08.unit-0005.reading-order` | 1 | `e533a5d85893bf2535d416d04c9e3e3ba57128520a779d5a950901e245565a36` |
| `bullarium.volume-08.unit-0006.reading-order` | 1 | `ffaca0a8a75d290989958e09d432f6cc9aaecc0d2bc07f435a991663f96229ce` |
| `bullarium.volume-08.unit-0006.reading-order` | 2 | `8724f475ae7e971d8af2a428dd92a7fb8942656e4ee65b61d4fe8ae64d677dee` |
| `bullarium.volume-08.unit-0026.reading-order` | 1 | `e16c30543dd0e336578897cf399f12f79c3f0b86013ead0489bc7802edc79f2f` |
| `bullarium.volume-08.unit-0026.reading-order` | 2 | `08ae4cef0dab3d3a8ebb9114f4c1e127d5dadb9a0a7bebf453d7b0c69f6ec5fe` |
| `bullarium.volume-08.unit-0028.reading-order` | 1 | `01dc597a9ec883250de0a64f18e9f253d4dd8a27d763d91db2a15cf68e433a86` |
| `bullarium.volume-08.unit-0031.reading-order` | 1 | `dc73cbd9594305c58d20dd5b3d1d36a8231d95b799770bd18b10a4b31dcfff43` |
| `bullarium.volume-08.unit-0031.reading-order` | 2 | `86bd890f789d711a4fa60971f0877a9a981132fe977794f908315083e7398380` |
| `bullarium.volume-08.unit-0044.reading-order` | 1 | `954d5689c2886188a18b8bdfd7bc289601c3e5b43d1d4650f822a56c521958f5` |
| `bullarium.volume-08.unit-0044.reading-order` | 2 | `85aff5996fd20f198f387117ac74cd0d3303846675bbfc8e53a3db23625daef2` |
| `bullarium.volume-08.unit-0085.reading-order` | 1 | `54f7794726d2a0685be4d1d0b10aded06a86e3211c72816bd534b9da59bf3467` |
| `bullarium.volume-08.unit-0085.reading-order` | 2 | `9e22cfb7e9fd5e1617b5de259f7b7f08943fa0440f77bf33998a1ef5cc4ec711` |
| `bullarium.volume-08.unit-0091.reading-order` | 1 | `18a982ab9395dc2a6d2f8b370d2ba758c95205c58dbe6b5e2435b4ff3c783a15` |
| `bullarium.volume-08.unit-0091.reading-order` | 2 | `1280bdd404fbb916217403b426320e555ff9e10a3624c123928be6dc5eae9062` |
| `bullarium.volume-08.unit-0092.reading-order` | 1 | `fd212351f6f64aeaeff7831b668a2f6517b0d3e922b4437263c73fc5a5078bc6` |
| `bullarium.volume-08.unit-0092.reading-order` | 2 | `bf8bfb9d81d1614032b92b4c0d2913efb51ba9233264d5675460e72a3985bf0c` |

## Limitations

- These readers are literal, uncorrected, uncollated historical OCR, rendered mechanically. This review covers layout only. It makes no word-level collation, correction, historical-authentication, publication, installation or deployment claim. Odd spellings, OCR corruption and literal dates are limitations, not defects. No date was inferred or repaired.
- The geometry evidence relies on existing native WORD bounding boxes and fitted column bands. Some leaves lack recorded geometry: vol. VII 698 and vol. VIII 116. Leaves without native text were not reconstructed: vol. VII 204-205. Only text and visual review covers those leaves. The mixture judgement rests on WORD extents, column edges and raw OCR adjacency. No character-level geometry or facsimile image was examined.
- Marginal and note block counts are mechanical counts of derivative blocks inside the selected ranges. Ownership of printed notes excluded by the selection ranges is an upstream fact that this lane did not evaluate.
- Source admission, rights, render success and source fidelity are upstream evidence, not findings of this visual lane.
