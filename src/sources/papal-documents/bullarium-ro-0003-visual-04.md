# Bullarium Romanum reading-order visual review: batch bullarium-ro-0003, lane 04

**18 PASS, 1 CHANGES_REQUIRED** of 19 assigned PDFs. I opened all 45 pages one at a time at full raster size and reused none. The one CHANGES_REQUIRED finding is a printed page-foot note run into a body paragraph (addendum b). I found no marginal-summary fusion. Scope: lane 04 of review batch `bullarium-ro-0003`, coordinate-reconstructed reading-order readers from the Naples Bullarium Romanum, vol. VIII (1883): eight Gregory XIII acts (units 0093-0143) and eleven Sixtus V acts (units 0152-0203). Reviewed 2026-10-28.

## Scope and method

I opened each assigned PNG from the repository `pdf-review` run as its own full-size image (1700x2200) with the Read tool before recording any observation. After each document I appended one JSON line per page to `observations.jsonl` in the lane directory. I did not use contact sheets or thumbnails. I did no re-rasterization, source acquisition, word-level collation, text correction or date reconstruction.

On each page I checked the displayed title, the responsible-issuer line, the Latin label and the omission of the unresolved act date against the frozen metadata. I also checked headings, the two-column flow and gutter, margins, glyphs, clipping and overlap, the natural source closing, modern digitizer signatures and raw placeholders. Per the series addendum I checked (a) that every marginal summary is a separate TAB-led block, (b) that every page-foot note is a separate block at the page break, (c) the reading order of the two columns, (d) running heads, folios and signature marks left inline, (e) fragment presentation and (f) non-word OCR noise inside body lines. No assigned document is a fragment; all are `printed-act` extents. No document carries a `prior_finding`.

Mechanical support used read-only, lane-local scripts (`mech.py`, `notes.py`, `pagebreaks.py`, `leafnotes.py`, `rawctx.py`). They split each selection of the reading-order derivative `hybrid.txt` into paragraphs at the manifest line ranges and found **151 TAB-led blocks**, no paragraph mixing TAB-led and body lines, no `Missing character` or `Overfull \hbox` entry in any lane PDF log, and no `Google`/`Digitized` string or bare `None` in any lane body TeX. `leafnotes.py` compared every page-foot note block recorded by the derivative's recipe for each touched leaf with the note lines in that leaf's output, so every printed note is accounted for. `rawctx.py` showed the raw (pre-reorder) OCR line for each doubtful body-noise locus, to tell non-word specks in the body column from marginal words. This mechanical check supports the visual review; it does not replace it.

## Evidence verification

I computed digests for all assigned PDFs, the receipt, the frozen manifest, the raster-run record and every assigned page PNG before and after inspection. They matched the assignment pins both times (67 files), and the before and after verification records are byte-identical.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment | `b51b8627ca314983a4c24961755f34d152202e7f9ed59add7771cbab58087388` | Scope binding, unchanged |
| Before verification record | `fe8262fd1bd391f1cf1bfa52777812d40f20f37746954747a3a932cc9a522482` | PASS |
| After verification record | `fe8262fd1bd391f1cf1bfa52777812d40f20f37746954747a3a932cc9a522482` | PASS; identical digests |
| Inspection ledger `observations.jsonl` | `32e0e80768cb81e71cbcf0c7f1d149db60ca507e52241a5c1a05e680f0461997` | 45 unique page observations |
| Mechanical scan `mech.json` | `1565265e0705ffc594684ca4166ff37708db907070fc05b746fd15f8fe575ef7` | Marginal blocks, mixed paragraphs, TeX/log scans |
| Note accounting `leafnotes.json` / `notes.json` | `11f780991aab83b7fc389b0e63b5be755d7c536763d40c7071d83c34ccd0de26` / `081edc544fb88c363f616b0796f3d1aed5915b84155b016f81e5e6f72f904a4e` | Recipe note blocks vs rendered note paragraphs |
| Page-break scan `pagebreaks.json` | `5d6eef1c9289e4bc5b2308ae43c17ee1e69583142354ae9afa94dc88efc2a43a` | Running heads and signature marks with preceding paragraph |

## PDF outcomes

| Document | Issuer | Status | Pages | PDF SHA-256 | Marginal blocks | Note blocks (separate / fused) |
| --- | --- | --- | ---: | --- | ---: | --- |
| `bullarium.volume-08.unit-0093.reading-order` | Gregory XIII | PASS | 2 | `7a920db9648fbcc25dd3be1ba2fbed6b3683cb7dff85ebc13800a43808aa2698` | 6 | 0 / 0 |
| `bullarium.volume-08.unit-0103.reading-order` | Gregory XIII | PASS | 1 | `c862289a8c4d96f5fbf54d25293ea964520c2f80af746a0565134b64b191dcef` | 4 | 0 / 0 |
| `bullarium.volume-08.unit-0104.reading-order` | Gregory XIII | PASS | 3 | `7271665a1d710b700af9118211fcf9f038757f6efc6502ff324dfff0863fd314` | 9 | 2 / 0 |
| `bullarium.volume-08.unit-0117.reading-order` | Gregory XIII | PASS | 2 | `53f18dc726c2aa15c221ada559f5bd186ac0849a030f72da989b280fd259d11b` | 6 | 1 / 0 |
| `bullarium.volume-08.unit-0121.reading-order` | Gregory XIII | PASS | 2 | `f1bf1112e100751ed1d9112af09524bc16773b24cf6248f6fbec41230f24403f` | 4 | 0 / 0 |
| `bullarium.volume-08.unit-0139.reading-order` | Gregory XIII | PASS | 3 | `96e04285d3bc7286ea36041afb25636962d40f40d2d7b411ae4c6122d68bb2c4` | 9 | 1 / 0 |
| `bullarium.volume-08.unit-0142.reading-order` | Gregory XIII | PASS | 4 | `3f120a2ce0bcda3160f4b10e22e4ff66ba75d46c3e068dd153b78b6f346a2248` | 13 | 1 / 0 |
| `bullarium.volume-08.unit-0143.reading-order` | Gregory XIII | PASS | 3 | `c023c542dc030ecf1f159e617fc81f16dd5bcc7af380827b7dc17ab3a2c38c40` | 8 | 0 / 0 |
| `bullarium.volume-08.unit-0152.reading-order` | Sixtus V | PASS | 2 | `e4cbfb9e24e1a8adc5cdbb50ca8ec7e38e9d0bf32b8acd4a2128261038829185` | 6 | 1 / 0 |
| `bullarium.volume-08.unit-0167.reading-order` | Sixtus V | PASS | 2 | `acfdcbca31dd5ac5bd0ecfa03e19f9cbf02836d0207e5319e5f91bf8d42ad779` | 6 | 1 / 0 |
| `bullarium.volume-08.unit-0168.reading-order` | Sixtus V | PASS | 2 | `30115d716ca17364766d13e6f71ba86eb532b9a485a490e8e9c1b575298024e2` | 9 | 1 / 0 |
| `bullarium.volume-08.unit-0173.reading-order` | Sixtus V | PASS | 1 | `3ce29f764e7f560848ca05dfb5c9936f85dd095f9551c58ab29987c019bc2ce4` | 3 | 3 / 0 |
| `bullarium.volume-08.unit-0176.reading-order` | Sixtus V | CHANGES_REQUIRED | 2 | `ba9063513b304b4e7ffa105e1565c108daf990b24db1ece392daa550576bdde7` | 7 | 1 / 1 |
| `bullarium.volume-08.unit-0186.reading-order` | Sixtus V | PASS | 2 | `0f68097d4d52ac7cdd00243348ac694cc44bd5e92ae73f25cda8fe59ea9e0d4d` | 8 | 1 / 0 |
| `bullarium.volume-08.unit-0187.reading-order` | Sixtus V | PASS | 2 | `25cd6a69effe05e22228b4525ca2b96f8264968c4a8815205879c156515abc22` | 7 | 2 / 0 |
| `bullarium.volume-08.unit-0189.reading-order` | Sixtus V | PASS | 3 | `5356f9cfa0a942285b3da07cb5503625ec9228af0c5cee1f9eddb3a76764b81f` | 12 | 1 / 0 |
| `bullarium.volume-08.unit-0191.reading-order` | Sixtus V | PASS | 4 | `bf983c11f6d698b57fda264241f847708a837a923c7c9865521a609cf6ab330c` | 7 | 1 / 0 |
| `bullarium.volume-08.unit-0193.reading-order` | Sixtus V | PASS | 3 | `8ad48e1095049ccacd251311fd5b67b8ae07a88d6a037c4d9219f5463396ab76` | 16 | 1 / 0 |
| `bullarium.volume-08.unit-0203.reading-order` | Sixtus V | PASS | 2 | `10c4633e5e270a8059807b11c139a89aa045f3b45cb26c92fd397b5720a3a497` | 11 | 2 / 0 |

Across the lane: 151 TAB-led blocks. Of these, 143 are marginal summaries (some heavily OCR-damaged) and 8 are stray glyph or furniture blocks (`*` twice and `i I` in 0189, `*` in 0139, `.` in 0143, `•` in 0176, and in 0104 the fragment `' -` and the running-head piece `àn. C. 1582`). Every one is set as its own block; none is fused into a body sentence or a hyphen-split word. There are 21 printed page-foot note blocks: 20 set as their own blocks (acceptable) and 1 run into a body paragraph (blocking). The 0173 count of three is note 1 (its head at the first page break and its continuation `ratioues libi indicavi ...` after the dating line) plus note `1 Omittitur tenor ...`. Eleven further recipe note blocks on touched leaves belong to neighbouring acts outside these selections and do not appear in these readers (leaves 378, 420, 460, 546, 560, 601, 765, 774, 777 left, 781 and 835).

## Findings (CHANGES_REQUIRED)

- `bullarium.volume-08.unit-0176.reading-order`: BLOCKING (addendum b): printed page-foot note '■ Haec moderatio est fortasse extensa etiam ad provinciam Dalmatiae et luslinopolilanam.' is run into the § 4 body paragraph (same paragraph, no break) at p. 2, left column, immediately after the hyphen-split body word 'aliteriudicandietin-' (reading-order derivative LF lines 79622-79624; the raw OCR sets the note after a blank line, and the recipe records no note block on leaf 700); the body resumes 'terprelandi facultale' after the running head '1. e. 1580 SIXTI'S V pp. r.S.T An C. 1586'.

The recipe that drives the derivative records no note block on leaf 700, so this note is emitted as an ordinary body row. A derivative fix that recognises the `■`-marked page-foot note on leaf 700 and ends the § 4 paragraph before it would clear the finding. Page 1 of the same reader passes.

## Qualifications (non-blocking)

- Running heads (e.g. `An. C. 1586 fi^-^ RrLLARimi ROMANUM An. C. ISgil`) are left inline on their own lines at the source page breaks in every multi-leaf document, often between the halves of a hyphenated word (addendum d).
- Printer signature marks are left inline (addendum d): own line in 0121 p. 2 (`Bull. Rom. Voi. Vili. 58`), 0139 p. 2 (`BuÌL Rom. Voi. Vili. 07`) and 0167 p. 2 (`BuU. Uum. Voi. Vili. «a`); as the last line of the § 3 body paragraph at the page break in 0093 (`Uu!L lìom. Voi. Vili. 10`, top of p. 2 left column, between `convcn-/tum`); and inside the page-foot note block in 0104 p. 1 (`Bull. Rom. Yol. YIII. 51`), 0142 p. 1 (`Bull. Hom. Voi. Vili. 68`), 0189 p. 1 (`UuU. liom. t'y/. \m 94`) and 0203 p. 1 (`Dilli. Rom. Voi. Vili. 103`).
- Separate marginal or stray blocks sit between the halves of a hyphenated word or a little early or late (addendum d): 0117 p. 1 `caosaconsu- ...` between `eorumdem` and `Francorum`; 0139 p. 1 `sancu Maori-` mid-sentence; 0168 p. 1 `CnniraTe- ...` between `domorum,` and `guai'dianos`; 0176 p. 2 `le-/neatur` (stray `•`); 0186 p. 2 `praedc-/cessorem`; 0191 p. 2 `per-/sonis`; 0193 p. 1 `nu-/meruin` and p. 2 `annis Caiyiniae ...` inside § 6. At first-leaf page breaks the separate note block, running head and marginal block together fall between hyphen halves in 0139 p. 1 `praeci-/piiaiii`, 0142 p. 1 `iagres-/siis`, 0152 p. 1 `qu3-/vis` and 0173 p. 1 `delri-/monta`; each note there is its own block.
- Short runs of non-word OCR noise remain inside body lines (addendum f), e.g. 0093 `^^jg` (§ 3) and `^.^^.jj p„ijii(,[` (§ 6); 0104 `Cer- r^ • ne • T , ^. viensem` (§ 4); 0142 `. .- 1 i* !_• • •„`; 0167 `fun- , . , ^ , . . ^^ . _ gebatur`; 0187 `.- • . i .• -i ■•`; 0193 `per ''''^''^^ ^''^'^' ^^' praedeccssoris`. For each doubtful locus the raw OCR line shows the run in the body column beside margin rows whose words are all present in the separate marginal block, and no run contains marginal-summary words. Whether some runs stand for damaged body words (for example the 0093 and 0193 runs) cannot be told from layout and is left uncorrected; it does not change the outcome. 0121's proem is heavily OCR-damaged body text, not fusion.
- Cosmetic paragraph breaks inside a sentence occur where the raw OCR has margin rows and blank lines: 0139 p. 2 § 3 after `quodliceatprajdictoEmmanueli`, 0189 p. 3 § 7 after `provin- . '■ .`, 0203 p. 1 § 3 after `ac in`. No text is fused.
- Stray single-glyph lines appear before running heads (0167 p. 2: nine lines `I ; 1 \ ! I I j I`; 0193 p. 1: eight lines `i | i [ ,■ ! i :`; also 0103, 0139, 0189, 0193 p. 2). The `▲` (0167 running head) and `▼` (0176 marginal) glyphs are literal source OCR characters and render; no tofu or missing glyph was seen.
- The issuer lines are OCR-damaged but match the metadata and still identify the pope (e.g. `Gregorias Papa XIII`, `GregoriDS episcopas`, `Sìxtas Papa T, ad fatnram rei memoriam`, `SixtQs Papa V, ad fatmam`). In 0167, 0186 and 0187 the issuer line carries the address and salutation, as recorded in the metadata. No act date is shown in any title line; the literal source dating remains in the body.
- Sparse final pages in 0104 (p. 3), 0117 (p. 2), 0142 (p. 4) and 0191 (p. 4) each hold genuine source closing (the end of the Datum clause and/or the `Dat.` line) before the source note and rights colophon. None is a page of notices only. Every other reader ends with its Datum clause and `Dat.` line in the body columns; 0173's single page closes with the Datum/`Dat.` lines followed by its two historical note blocks.
- 0173 and 0193 use two LF ranges; the excluded lines are the next act (XXXVII) and the preceding act's page-foot note respectively, as the source notes disclose.

## Limitations

Literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. This is a layout and structure review only. It makes no word-level collation, historical authentication, rights, publication, installation or deployment claim. Marginal and note roles were judged from the rendered pages, the derivative's paragraphing, its recipe and the raw OCR lines; I did not consult the remote facsimile.

## Page inspection ledger

| Document | Page | PNG SHA-256 | Status |
| --- | ---: | --- | --- |
| `volume-08.unit-0093` | 1 | `26f4cbe572ecb1d6f006699384e879d6e3b7a273ef4c48b355ab4bcc2c63905a` | PASS |
| `volume-08.unit-0093` | 2 | `e9744aa0ff3b3c58a506a5edbce48ed773cd95f357bec9f86d34dd7efe5a0efd` | PASS |
| `volume-08.unit-0103` | 1 | `65a5b45d105c0ca5aab6926d0cf202f7dc920d60d8d640d4f4f2eeabfd0f09bf` | PASS |
| `volume-08.unit-0104` | 1 | `f3b4c078ead95b78ad8e94d53edca5865eeebd8757744d4be82c5d2922873f61` | PASS |
| `volume-08.unit-0104` | 2 | `1c3c5c6bfa0406166228a5f9601eae2015feccf03ae510c7f1026c97bec00dd4` | PASS |
| `volume-08.unit-0104` | 3 | `e60421e6f5ee131f1769cae290dba73141b8761081d97dded1b5014051ce3726` | PASS |
| `volume-08.unit-0117` | 1 | `a3b8e8de185303967f9d1347fcc676884cce78ef889aedc09f608f433052b538` | PASS |
| `volume-08.unit-0117` | 2 | `afd1a42350a019572c294780e5a7a40a9be96dd2bd20c70aeb0fa832212f45b9` | PASS |
| `volume-08.unit-0121` | 1 | `86f41c8186e2e5890d101069e4fcd9c7cdce60de14780234ced3fbe3ffb72dfe` | PASS |
| `volume-08.unit-0121` | 2 | `a5af5e21b6121a02bf5aaa13037252de65e455f24c7be56d67826f17b05a6495` | PASS |
| `volume-08.unit-0139` | 1 | `f86f76d1d88ea846fa5e0246b6a91f8922f6721f9bd88f65d343d9df8f2e2712` | PASS |
| `volume-08.unit-0139` | 2 | `517d5af2b7720fb1e36cd2da1f026ad458d0d5e1413fee0998caad130b61f3d0` | PASS |
| `volume-08.unit-0139` | 3 | `13b33e2601defaa145a25924207ba56ea8203a4a52680caaea3cc6e7c5b4a954` | PASS |
| `volume-08.unit-0142` | 1 | `0627623f7bada5b98f68ba4f12e36995e381bc99bc3ec8d3a1c01b33784a9613` | PASS |
| `volume-08.unit-0142` | 2 | `3b2cabc463bca5f3fab2ea01d21a24009aec59efda82c13f960f3159d179094e` | PASS |
| `volume-08.unit-0142` | 3 | `9d0a78a08a73a8848f5ad8eb5ba371db02441be90ac0e1a39544020a5f6f8987` | PASS |
| `volume-08.unit-0142` | 4 | `86880dae15bfaf12531fc40e424d4f004e3d5131e29b78fbd5a71487b25d1cd3` | PASS |
| `volume-08.unit-0143` | 1 | `f04669878f0b4809b13183dc55ca2fc90f18a32b9fbe583458be114dcec07c79` | PASS |
| `volume-08.unit-0143` | 2 | `84b012f3fa6e2a78601b551f2b9d0f7c716ad990c998487ce7711be69b2e0512` | PASS |
| `volume-08.unit-0143` | 3 | `656176d5ad4e906fe8d789d90990a40c93f2d1fe864c9e3f2d3ccda62e8715da` | PASS |
| `volume-08.unit-0152` | 1 | `77c088b65b5417c6ab1d38c955d13d7d414a1187bffe29cb7b672ee1efa7e0c9` | PASS |
| `volume-08.unit-0152` | 2 | `141a9b798daaf03a40615f2e9b584420690f7500e5f58c8c09874fe684a16324` | PASS |
| `volume-08.unit-0167` | 1 | `11ad52daf825afbd6612e0b072069aa35afeb20e6a6a175c2134565e3e0cd061` | PASS |
| `volume-08.unit-0167` | 2 | `4a4370e5ed3186b03fce5640da5f8389646aa745c4a69a0274480c42aa81221a` | PASS |
| `volume-08.unit-0168` | 1 | `35820f06ccac33efdc00cdbccb8c99f85bf800a254869d5f23f6f7dd06172284` | PASS |
| `volume-08.unit-0168` | 2 | `1e59ed5408719212282ac43b9f3ceb0af47b194bca3bad74396929f7a2588728` | PASS |
| `volume-08.unit-0173` | 1 | `984755e2c5854f0c051427e987a5a2bec13682640e9df6a893d81a0f6bcf0d7a` | PASS |
| `volume-08.unit-0176` | 1 | `1b71f86dc8fb539269466bd8e8bd8324fe3be89917473865858b7c71bbb9c014` | PASS |
| `volume-08.unit-0176` | 2 | `d56c82904d2660a1d54d57e2a6dc0ecb9c5ff9d7f9b5518727b49d013fad5571` | CHANGES_REQUIRED |
| `volume-08.unit-0186` | 1 | `309fa14b19f203abde585ff444cd9f911650963dd8f61b11bcdbfff0c1da53d8` | PASS |
| `volume-08.unit-0186` | 2 | `4d361d027c34656ae99be11e5f4a31bb6b30ea23b53dfcadc0657fbbe3da6137` | PASS |
| `volume-08.unit-0187` | 1 | `90f051a9a8b47ce0ce6b8a5765bea2b9f4b32f73ccf0bd3a34455a2116dbb049` | PASS |
| `volume-08.unit-0187` | 2 | `1ac7df6762565821bb5722013ece6eace66ddd1c2c40f30e48dcdd22e016fabe` | PASS |
| `volume-08.unit-0189` | 1 | `f51bdf97dc0aca40fde1789aae61e6d6d7925bbb8b719e36370411d59d5a49f6` | PASS |
| `volume-08.unit-0189` | 2 | `cdd1c84d93da0f550dd46828c65fdb745abe3c59b926fcfd40f312526de47e46` | PASS |
| `volume-08.unit-0189` | 3 | `718fa3f02f6436069a8fba7f78d6ac47dac0e3f2abd224d8ef304065ca0a4994` | PASS |
| `volume-08.unit-0191` | 1 | `c0fc102a7e04d82ce84034ba7c0100344b21556d89d30e011c8aac9011358cf5` | PASS |
| `volume-08.unit-0191` | 2 | `2c03e409e544a137ad8e72838e4b3ff0798296cdad717950558aca31fa061eb9` | PASS |
| `volume-08.unit-0191` | 3 | `c98754964ad56f63aba6773490e8829d453532065ed437ac0c71da4bfd2d6125` | PASS |
| `volume-08.unit-0191` | 4 | `ca9da29a10de4b8b842682d53ef2afb5fd5f8371b16e2ebb191a1692a29eb044` | PASS |
| `volume-08.unit-0193` | 1 | `b33479eced0382a2831d83a31ddecf416b13862153d7c22e35591a9deef99ad5` | PASS |
| `volume-08.unit-0193` | 2 | `b6a0e568b77adbe37b8a27b9c14c5eac8029989cd8de467d1fefd64848f3f58e` | PASS |
| `volume-08.unit-0193` | 3 | `270949ba98f08fee9c554bd6fe3036884f65aec291eded96806e4ef9ca5ab6b6` | PASS |
| `volume-08.unit-0203` | 1 | `ee3d6b58b7d5ae3c35b69d7c7612e770dcb30a3d36709f27d567be6d9b589349` | PASS |
| `volume-08.unit-0203` | 2 | `28c1c53dc048a77c81feb13ae0fe517e96077a4adcade6c5c6074f4ab1a9123e` | PASS |
