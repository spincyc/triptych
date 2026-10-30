# Bullarium Romanum reading-order visual review: batch bullarium-ro-0002, lane 04

**19 PASS, 7 CHANGES_REQUIRED** of 26 assigned PDFs. I opened all 61 pages one at a time at full raster size and reused none. Every CHANGES_REQUIRED finding is the same kind of defect: a printed page-foot note run into a body paragraph (addendum b). I found no marginal-summary fusion. Scope: lane 04 of review batch `bullarium-ro-0002`, coordinate-reconstructed reading-order readers from the Turin Bullarium Romanum: vol. VII (1862; three Pius V acts) and vol. IX (1865; 23 Sixtus V acts). Reviewed 2026-10-28.

## Scope and method

I opened each assigned PNG from the repository `pdf-review` run as its own full-size image (1700x2200) with the Read tool before recording any observation. After each small group of pages, I appended one JSON line per page to `observations.jsonl` in the lane directory. I did not use contact sheets or thumbnails. I did no re-rasterization, source acquisition, word-level collation, text correction or date reconstruction.

On each page I checked the following against the frozen metadata: the displayed title, the responsible-issuer line, the Latin label, and that the unresolved act date is left out. I also checked headings, the two-column flow and gutter, margins, glyphs, clipping and overlap, the natural source closing, modern digitizer signatures and raw placeholders. Per the series addendum I checked (a) that every marginal summary is a separate TAB-led block, (b) that every page-foot note is a separate block at the page break, (c) the reading order of the two columns, (d) running heads, folios and signature marks left inline, and (e) fragment presentation. No assigned document is a fragment; all are `printed-act` extents.

Mechanical support used read-only, lane-local scripts (`mech.py`, `notes.py`, `notes2.py`). They split each selection of the reading-order derivative `hybrid.txt` into paragraphs at the manifest line ranges. The scan found **256 TAB-led marginal paragraphs**, no paragraph mixing TAB-led and body lines, no `Missing character` or `Overfull \hbox` entry in any lane PDF log, and no `Google`/`Digitized` string or bare `None` in any lane body TeX. Every printed note that the note scans and the page views located was then checked visually on its page. This mechanical check supports the visual review; it does not replace it.

## Evidence verification

I computed digests for all assigned PDFs, the receipt, the frozen manifest, the raster-run record and every assigned page PNG before and after inspection. They matched the assignment pins both times (90 files), and the before and after verification records are byte-identical.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0002/receipt.json` | `6abaf3f0a23aecea64d5a76485c69926ade5926fd2b88a89840f787ded6bc46a` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0002/frozen-manifest.json` | `ce384dfe75cde78b6427f00c878a870507a47e1a9422408dbfa0bfefb0d7b11a` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0002/review-run.json` | `d91c149a7573666400708bd0104faa48443b257929563ed9769ee787ec4f7a20` | Before and after |
| Lane assignment | `ba656d36e7c23f8fd9a383d003358befc52a0f970ecbacb068b3f45c20b2b0cb` | Scope binding, unchanged |
| Before verification record | `f65917713b569f8bd25f680959acd4f1a0ee28d04f4fce86b17f066566101c72` | PASS |
| After verification record | `f65917713b569f8bd25f680959acd4f1a0ee28d04f4fce86b17f066566101c72` | PASS; identical digests |
| Inspection ledger `observations.jsonl` | `66a95ea53e21b4e7e0513402b949162ef407b7677d7286bc7cd3c8fc7daf7ba5` | 61 unique page observations |
| Mechanical scan `mech.json` | `e26ee02b477394580da84ee35e233d9fefcf31aeeaf7ac9db7add5670e3e274d` | Marginal blocks, mixed paragraphs, TeX/log scans |
| Note scans `notes.json` / `notes2.json` | `7a6e8c12a56f0a1b3c0d3b8c520e76ec3ceb8959eeffc9834fb346155d845a5b` / `b7c68f88739ba68a16a52024b73bbea866e9295db8a13feb82bc098064ddf601` | Note paragraph membership |

## PDF outcomes

| Document | Status | Pages | PDF SHA-256 | Marginal blocks | Note blocks (separate / fused) |
| --- | --- | ---: | --- | ---: | --- |
| `bullarium.volume-07.unit-0205.part-03.reading-order` | PASS | 4 | `a539065b370976b8eb3f978d55b0c11c0009438d4fa87fc22060c636ea0cb151` | 15 | 0 / 0 |
| `bullarium.volume-07.unit-0207.reading-order` | PASS | 1 | `c9f67ba2eff9ddb9b9c175baa690fd9f1904c2d3f7b18b6fa4de6a9960379f02` | 3 | 0 / 0 |
| `bullarium.volume-07.unit-0209.reading-order` | CHANGES_REQUIRED | 4 | `38cc69331f2e32dad55d90cc42c15ea7dea8bbf053fb29c0a0d4c88f0cecbab1` | 18 | 1 / 1 |
| `bullarium.volume-09.unit-0001.reading-order` | PASS | 2 | `12846d3a0e9e7bb239d8eb48dc83c8ed9ce69581bedfa7e412adc36614a13bc4` | 7 | 1 / 0 |
| `bullarium.volume-09.unit-0002.reading-order` | PASS | 2 | `a90b4e0e67adca6c44aad109555e203bfb595c272bbf069fabbbab6281228b0e` | 14 | 0 / 0 |
| `bullarium.volume-09.unit-0004.reading-order` | CHANGES_REQUIRED | 3 | `faa6ef0c0cb1164215711b2167cded537f7ac2100fd716b8ccf668eb4e1d7632` | 13 | 3 / 1 |
| `bullarium.volume-09.unit-0005.part-01.reading-order` | CHANGES_REQUIRED | 3 | `716c39b5eef884f4b9be534696f7b7443a5317c70f265ba5adc6f02dff9d083c` | 10 | 1 / 1 |
| `bullarium.volume-09.unit-0005.part-02.reading-order` | CHANGES_REQUIRED | 3 | `bbf3126580b343b98a063e698c06f2be22a712991bf922acdd567dc12d35e620` | 13 | 0 / 1 |
| `bullarium.volume-09.unit-0011.reading-order` | PASS | 2 | `80d723b4698bd666941e37b6aea70c24189c2b3917f364a7306e24a038cce264` | 5 | 1 / 0 |
| `bullarium.volume-09.unit-0017.reading-order` | CHANGES_REQUIRED | 2 | `50cfcc809659185ee748aaeddf87a41d58f9b92f7ed33e5745d206ad659a1ab1` | 7 | 0 / 1 |
| `bullarium.volume-09.unit-0019.reading-order` | PASS | 1 | `1a82a74632f8ff9e2592212d0a966e920259373a8831a400f41348d7d8ca1df9` | 3 | 1 / 0 |
| `bullarium.volume-09.unit-0023.reading-order` | PASS | 2 | `d6ed04b599f42461e4172894dacd4c43c1af6fe2a808574e87d16d891ebe41d8` | 13 | 1 / 0 |
| `bullarium.volume-09.unit-0025.reading-order` | CHANGES_REQUIRED | 2 | `067552e8c266072cf531d7658532b4e67442c84599e3c3e249f5bab05b56e6f0` | 9 | 1 / 1 |
| `bullarium.volume-09.unit-0026.reading-order` | PASS | 3 | `860a4999557066a8018cc08ea1d64f3d3da1b5c3a3a2d1dc773bb88d73237876` | 11 | 1 / 0 |
| `bullarium.volume-09.unit-0028.reading-order` | PASS | 2 | `80262824356237c2024b16fbfe258929133f93e58bd03513043bf83ec67f6a69` | 7 | 3 / 0 |
| `bullarium.volume-09.unit-0029.reading-order` | PASS | 3 | `acce7310d4be5cd773e382862c88d18297c6ea87420d7d355c5cc77a3c77cbde` | 16 | 1 / 0 |
| `bullarium.volume-09.unit-0034.reading-order` | PASS | 4 | `6c0c15ccba99a5cb16977ae48abe602a486c4b5a0d5a415fc80030e44824fa60` | 19 | 2 / 0 |
| `bullarium.volume-09.unit-0040.reading-order` | PASS | 2 | `2f93836e088cf1c1c7ea30686d8385322b5b35ab7c0c1f188cfbd3e1db391adb` | 7 | 1 / 0 |
| `bullarium.volume-09.unit-0045.reading-order` | PASS | 2 | `cb542fdf65597c0ed892a0ee7f76826ff60cfffaaf77d7ec91a88db805082a5b` | 11 | 1 / 0 |
| `bullarium.volume-09.unit-0052.reading-order` | PASS | 2 | `fe9994b810140a8be95a53172d700f79dde9af9418316bc2e59001f62cfffe47` | 5 | 1 / 0 |
| `bullarium.volume-09.unit-0058.reading-order` | CHANGES_REQUIRED | 2 | `6ea724dafafe78fc6a01d94564cbf0064f3cd8db1390216f340a10491e3d806f` | 11 | 0 / 1 |
| `bullarium.volume-09.unit-0059.reading-order` | PASS | 3 | `a38691cd28aa54d8b230ff922c05475b5fd788e670a0db60d9168a90697d8cb1` | 9 | 1 / 0 |
| `bullarium.volume-09.unit-0061.reading-order` | PASS | 2 | `57304e80646ca105eab7d5bdd792b50fce17a891eebb3ada08802de5025c5b93` | 12 | 1 / 0 |
| `bullarium.volume-09.unit-0065.reading-order` | PASS | 1 | `3e5417550c6ec56894abec14a11d1f4c28d53c5cafac52152d6a9395b913be18` | 4 | 1 / 0 |
| `bullarium.volume-09.unit-0066.reading-order` | PASS | 2 | `873cee5259583ace7cd70ad1cd86fdc257fa081ec4dc15acfd894673724740f3` | 5 | 1 / 0 |
| `bullarium.volume-09.unit-0069.reading-order` | PASS | 2 | `d6e3b2b0f97abd83e10dacfec00502361c99dfab8f6861bd0a1e2f59dcd34fa0` | 9 | 1 / 0 |

Across the lane: 256 marginal blocks, all set as separate blocks and none fused into a body sentence or hyphen-split word. There are 32 printed page-foot note occurrences: 25 set as their own blocks (acceptable) and 7 run into body paragraphs (blocking).

## Findings (CHANGES_REQUIRED)

- `bullarium.volume-07.unit-0209.reading-order`: BLOCKING (addendum b): printed page-foot note "I  lliiiusmodi of/ìcia eliam addit (n. T.)." is run into a body paragraph (same paragraph, no break) at p. 2, left column, end of § 5 (source LF line 111652), after "sicut de indulgcntiis peccalorum-"; body resumes "que remissionibus" after the running head.
- `bullarium.volume-09.unit-0004.reading-order`: BLOCKING (addendum b): printed page-foot note "1. Foulaiiinus legit vivitur (r. t.)-" is run into a body paragraph (same paragraph, no break) at p. 2, right column, § 3 (source LF line 3257), opens the body paragraph continuing "qualcnus nondum confccerint, debeanlo- mnino ...".
- `bullarium.volume-09.unit-0005.part-01.reading-order`: BLOCKING (addendum b): printed page-foot note "i Vide latius liicinf.   2 Cher legit. (jiianlKm- VìS (R. T.)-" is run into a body paragraph (same paragraph, no break) at p. 3, left column, end of § 6 (source LF lines 3703-3704), opens the body paragraph continuing "et super omnibus privative quoad omnes alios iudices ...".
- `bullarium.volume-09.unit-0005.part-02.reading-order`: BLOCKING (addendum b): printed page-foot note "Ea oniitlit Mainardus, quia in omnium mani- bus versabantur 'k. t.)." is run into a body paragraph (same paragraph, no break) at p. 2, left column, § 5 (source LF lines 4005-4006), after "ac tam per cum edenda quam a-"; body resumes "lia desuper ..." after the running head.
- `bullarium.volume-09.unit-0017.reading-order`: BLOCKING (addendum b): printed page-foot note "{ Ex Regest. in Secret. Brevium." is run into a body paragraph (same paragraph, no break) at p. 1, left column, proem (source LF line 11951), after "rum propositum dilectorum filiorum fra-", splitting "fra-/trum".
- `bullarium.volume-09.unit-0025.reading-order`: BLOCKING (addendum b): printed page-foot note "I Ex Regest. ìu Secret. Brev-" is run into a body paragraph (same paragraph, no break) at p. 1, left column, first proem sentence (source LF line 15639), between the halves of "au-/dientes" in "Vehemenler in Domino gaudemus au- ... dientes aelatem".
- `bullarium.volume-09.unit-0058.reading-order`: BLOCKING (addendum b): printed page-foot note "i Ex Regest. in Secret. Brevium." is run into a body paragraph (same paragraph, no break) at p. 1, left column, end of § 1 (source LF line 33922), after "dieta officia fiscalatusetcommissaria-", between the halves of "commissaria-/tus".

The fused-note pattern recurs: the printing's page-foot note is emitted inside the paragraph that spans the page or column break, not as its own block. In vol. IX this most often happens with the provenance note "Ex Regest. in Secret. Brevium" when the note falls mid-paragraph on the act's first leaf. A derivative fix that ends the body paragraph before each page-foot note block would clear all seven.

## Qualifications (non-blocking)

- Running heads (e.g. "An. C. 1589 SIXTUS V PP. 141 An. C. 1589") are left inline as their own lines at the source page breaks in almost every multi-leaf document (addendum d).
- Printer signature marks are left inline (addendum d). Inside a body line: vol. IX 0005.part-01 p. 2 ("Bull. Rom Voi. IX. * 4", left col.), 0026 p. 2 ("Bull. Rum. Voi. IX. 17", left col.), 0045 p. 2 ("Bull. fiom. Vul. IX. 32", left col.). On their own line: vol. VII 0205.part-03 p. 2, 0209 p. 1; vol. IX 0034 p. 2, 0058 p. 1, 0069 p. 2.
- Separate marginal or stray blocks are placed between the halves of a hyphenated word (addendum d). Vol. VII: 0207 p. 1 "animadver-/sio"; 0209 p. 2 "ta-/men" and p. 3 "prae-/senlibus". Vol. IX: 0001 p. 2 "unicui-/que"; 0025 p. 1 "consi-/lium"; 0026 p. 1 "praede-/ccssor"; 0045 p. 2 "regu-/laribus"; 0052 p. 1 "cuius-/vis"; 0059 p. 2 "ar-/cbiconfraternitatem" and "conces-/serimus"; 0061 p. 1 "va-/lidas"; 0069 p. 1 "fe-/licis".
- The issuer lines are OCR-damaged but match the metadata and still identify the pope (e.g. "Sixtas Papa T", "Plus episcopas servus servoram Dei", "Pius ... ad perpstuam rei raemoriam"). In 0019, 0034 and 0066 the issuer line carries the address and salutation, as recorded in the metadata.
- Many body lines contain non-lexical OCR noise tokens (e.g. "• . ■ , ^^"). These are literal source OCR with no legible marginal-summary words, so they are not treated as fusions.
- Sparse final pages in 0209, 0001, 0005.part-02, 0011, 0017, 0026, 0029, 0034, 0040, 0045, 0052 and 0066 each hold genuine source closing (dating clause, "Dat." line or printed note) before the source note and rights colophon. None is a page of notices only.
- In 0058 the title wrapping leaves the closing mark "'." alone on a line. This is cosmetic.

## Page inspection ledger

| Document | Page | PNG SHA-256 | Status |
| --- | ---: | --- | --- |
| `volume-07.unit-0205.part-03` | 1 | `ac143859c9ba8bf5d5436b4d60efa8e6167d14b369e1730511e0d4aab31647ee` | PASS |
| `volume-07.unit-0205.part-03` | 2 | `d872eca85e19cff29806770b3ee7ef9c5f17d005cb93c4a030a6511f3a38e561` | PASS |
| `volume-07.unit-0205.part-03` | 3 | `a63d860ae851cc29dd8145b64e3b1ead6fdccda9a6ef04ed60d117d63d414081` | PASS |
| `volume-07.unit-0205.part-03` | 4 | `bcfe49f869574eb23d2021589694e68d9ca9bb3710286b8412ed07c1e47ffe77` | PASS |
| `volume-07.unit-0207` | 1 | `b8ffb5586fb275eeac5ab2cd44abd9775ee80b28556d8ad7a9154443c442f6bd` | PASS |
| `volume-07.unit-0209` | 1 | `e9b7ec0078983e40c9d725fc348eae09e79ce7a72c106d2c599cd321ffabde3b` | PASS |
| `volume-07.unit-0209` | 2 | `7f718b9795f451e3a0e194eb413f26bfaddc4219529a803cb9120d5838d493e0` | CHANGES_REQUIRED |
| `volume-07.unit-0209` | 3 | `ccf307b295852a8047d26e8cc697b867e2749b8a50a34837fc6e220054392c80` | PASS |
| `volume-07.unit-0209` | 4 | `7374a631d48d468aadfaff66aff468a3e1a4d74c3586d4376cac0ab6ad99fa01` | PASS |
| `volume-09.unit-0001` | 1 | `bcae1805f1c0c8499e1da67a69f290a5d3e08434b3af9985653cec20e2c3cbd1` | PASS |
| `volume-09.unit-0001` | 2 | `1fe17a3d9c06ad5458118a47608b522dd4a7abff9cadf6689241e29b9c997541` | PASS |
| `volume-09.unit-0002` | 1 | `e129e385201dd399822fb751b06029bda7a27280ab00ee6e776c297766a73c1a` | PASS |
| `volume-09.unit-0002` | 2 | `307331c0acf5a1999ffb859cf6632bbfb59124af10ca446792e9637d8feac225` | PASS |
| `volume-09.unit-0004` | 1 | `1e1302650736b49108432a085364a4b2aa0fff35bb27349f10a2a29da2e54da8` | PASS |
| `volume-09.unit-0004` | 2 | `edd24f3acb05720bd2d0a13aaff0d3f62fa6b4604cb608f9d030a4663b3bdb30` | CHANGES_REQUIRED |
| `volume-09.unit-0004` | 3 | `daeac59b5f917952b4274b070161ec8482ea7285f05b4e7328ecc33764650041` | PASS |
| `volume-09.unit-0005.part-01` | 1 | `e7bf2f3fd75f214279c90d301ef353127a1df5f5c9a5d31502d5dd2e6d096139` | PASS |
| `volume-09.unit-0005.part-01` | 2 | `2308ea8adc2bffd59a4f0d5b904a4ed4396c57f1ca8f732cc03185b4139fdf08` | PASS |
| `volume-09.unit-0005.part-01` | 3 | `fe4fa67c7c43ecefc7120e6fa0bb23762ed78b3ae7cb8dbeae1a958921ca9896` | CHANGES_REQUIRED |
| `volume-09.unit-0005.part-02` | 1 | `c0c82bd3e3a3d6fbd947335ef662443fa09d6401c9b48c6d51941edb5b81fab0` | PASS |
| `volume-09.unit-0005.part-02` | 2 | `7decedb988bc9369c16e65a4b3652a60478776814ed643296938c1f720cff0fc` | CHANGES_REQUIRED |
| `volume-09.unit-0005.part-02` | 3 | `0a32ca6d24020c509c19a10ee73db716c1fee4a157713fbdf1f5de738dce3281` | PASS |
| `volume-09.unit-0011` | 1 | `d92912bd687c1e3b6ca5e004ecb686a5dfeb90180f90ac6c594489610b924b9f` | PASS |
| `volume-09.unit-0011` | 2 | `657130b7e0facb399dcca52fb9f116925a6226a7e86bd2531bcfcd9aea2ae050` | PASS |
| `volume-09.unit-0017` | 1 | `3568a2e2afb9ca5afb972010667777b8d209284f31b3af6173f92a857a280c05` | CHANGES_REQUIRED |
| `volume-09.unit-0017` | 2 | `d3db999ee75ead335407005147b4cdc2b7526d0fa1eb05110f2076e7f4b24d71` | PASS |
| `volume-09.unit-0019` | 1 | `f29ed6edf48d6af1af88af1c4dbf0bafc7e3ec4da4e7ddf7ed9be653ec461ce0` | PASS |
| `volume-09.unit-0023` | 1 | `b3794cbab367f3053d451542af7edbc54158044df72645d73a5154fe5b3c69b3` | PASS |
| `volume-09.unit-0023` | 2 | `614763bfdffd563c8b24d012835a648e7ae7a78ae71f4ca743052e2981989f19` | PASS |
| `volume-09.unit-0025` | 1 | `10c3a6e5e7ab2b91d22e4c97c2497816fb76d819d061ef2bede0798331573da9` | CHANGES_REQUIRED |
| `volume-09.unit-0025` | 2 | `cad7a0fca0ae105768a3d3a032b894eab2ac459432033f6d4875760b9a444485` | PASS |
| `volume-09.unit-0026` | 1 | `6c4a35b2f046f91a29a4e3905dbe9b7847635dc2037da41518b0a060ed8cc99a` | PASS |
| `volume-09.unit-0026` | 2 | `08b53234b577970e7b87b55fe0d620bafc5e6714b2c303b17fbe368e2c5e847d` | PASS |
| `volume-09.unit-0026` | 3 | `0a9d534d612e252f23159e26da43fb41c69723f7d22c45db9b4213dfdbe880c2` | PASS |
| `volume-09.unit-0028` | 1 | `5202c254d6626651ccdd8c68514ea3eedcbd45768223eca0f4182c5c54572503` | PASS |
| `volume-09.unit-0028` | 2 | `36c729f6728b903aa5a82330f161386547c43d2ac85fd356f4fbb7b7fc75a3cd` | PASS |
| `volume-09.unit-0029` | 1 | `e6c2347b8abde13908525ab4c0887852a2a61ba2f9dae99038ad79eedcf47b99` | PASS |
| `volume-09.unit-0029` | 2 | `e12092ed893486595520949f9b376045fd37b4d19e12cb960821f8ac814dd4bb` | PASS |
| `volume-09.unit-0029` | 3 | `4641a1ac59a5b1895d267907ab8d3d5c7764099b639090e3acedcc30429b5809` | PASS |
| `volume-09.unit-0034` | 1 | `95df6b2f7d4010f736f1ef28e7ef4f6d274075917fd15a7dcaa0da4cbbcf894e` | PASS |
| `volume-09.unit-0034` | 2 | `c19e78d9087d5b4c24bef89034af575688cf946aff6bfa0fc8e9c242a0068fa9` | PASS |
| `volume-09.unit-0034` | 3 | `6c4b4e0bd2277cedb2a739579e79b75aa18a8316d546477625a8a50329f9435f` | PASS |
| `volume-09.unit-0034` | 4 | `61e26afee861106e06c7aeaa609ea557e49a0f94582ad56b70a802019f8b5b04` | PASS |
| `volume-09.unit-0040` | 1 | `eb871708c3f1ac1af584f1b20090e9de4559efb8ec03011c150a19aa28f3be57` | PASS |
| `volume-09.unit-0040` | 2 | `1b21c3bfdb153188c2c1dd2de227f365479120bd94bd8cc8d45aa9b8a7bad867` | PASS |
| `volume-09.unit-0045` | 1 | `f8c96eb160309a9ff52f51d67ac48d7f52d7e70f2ff8cec77ae9a2e24751f927` | PASS |
| `volume-09.unit-0045` | 2 | `e8d8c525c5a0d800b586b905f326385beac07b4032ac4b85855ad56b5f6e704b` | PASS |
| `volume-09.unit-0052` | 1 | `d3348eb00d9fb6a5a32326ba70a6eed1c0d1f8f3d816b5613e9f61a514257c91` | PASS |
| `volume-09.unit-0052` | 2 | `74d812dd478733a92bedcdcc8b106bb21a1e4fbc856525c5f91c9ca3cbcf4822` | PASS |
| `volume-09.unit-0058` | 1 | `82304c180481ee07b0e058906c7baac4f222cb871000b69ca7a590ca75ff94ee` | CHANGES_REQUIRED |
| `volume-09.unit-0058` | 2 | `0b3958ada67ef00baa0f4936080339d4b3fc4c875136a883f5fcb67d38b77e34` | PASS |
| `volume-09.unit-0059` | 1 | `8c534ab4e9ee08f3463f32f05a6fb4d98d31ad38c9869ce35614b3e8ddb9cdf0` | PASS |
| `volume-09.unit-0059` | 2 | `55e4982de903beffd7a634d83e334353aa4c5b87b92aff2bf8dde2e63c2f6ec3` | PASS |
| `volume-09.unit-0059` | 3 | `55fc17d6ab2421d9845ea1567516af0201d79f028b0e9f626162fe11c41b0013` | PASS |
| `volume-09.unit-0061` | 1 | `31d6a5c18738d47a0826e05d6d6ab0fb683c3d6145a36b70beb3e9fa8c0b93bd` | PASS |
| `volume-09.unit-0061` | 2 | `7b2c4e8cf1a2bd81de2840fb3af2c02112ac41863af5fd046ff9ca9b96b2f668` | PASS |
| `volume-09.unit-0065` | 1 | `ecde5b950c934603af2f72e490af299cc50f3aa27d787806d46f08cd6c0bbf75` | PASS |
| `volume-09.unit-0066` | 1 | `2711e023474d27df1625ca9ef87c6ead37d1f521a881065ac93a3c704b14559c` | PASS |
| `volume-09.unit-0066` | 2 | `387c6db4618d17c52513e45932da838bddd8f698871d32037fd41628917f9971` | PASS |
| `volume-09.unit-0069` | 1 | `f40fa3aafc22bda43b03765c6f7d02998091dde7df896315132a63885ab7a984` | PASS |
| `volume-09.unit-0069` | 2 | `1421f3117cf637ffacc1d003cbeb9c0eb51e2aa4a31924f76798c6fdb0a37589` | PASS |

## Limitations

- The text is literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. Spelling, OCR corruption and noise tokens were not judged or repaired.
- The OCR dating lines contain conflicting or garbled dates (e.g. 0011 "Dat. die 1 ianuar. 1580" against "mdlxxxix"; 0029 "Dat. unno 1580"; 0040 "4590"; 0069 "6 nov." against "vi decembris"). These are limitations; no date was inferred or repaired.
- This is a layout and structure review only. It makes no word-level collation, historical authentication, rights, publication or installation claim, and it does not verify page-label or leaf-bound statements against the facsimile.
- Note detection combined mechanical scans with visual page review. A note with no recognisable marker that sits silently inside a body paragraph could still escape both.
