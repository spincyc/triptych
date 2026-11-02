# Gregory XVI Acta readers: visual review, gregory-0002 lane 02

Reviewer: Claude page-review worker (lane `gregory-0002/lane-02`). Scope: 38 newly admitted Gregory XVI Acta (Rome 1901–1902, volume 1) reader PDFs, 66 pages, assigned by `.scratch/claude-review/gregory-0002/lane-02/assignment.json`.

## Result

- Documents: 38; PASS 36; CHANGES_REQUIRED 2.
- Pages individually opened at full size with the Read tool: 66 of 66; reused pages: 0.
- Page statuses: PASS 63; CHANGES_REQUIRED 3.
- No document had a `prior_finding`.

Blocking findings:

- `gregory-xvi-acta.volume-01.line-00015640`: CHANGES_REQUIRED: annexed 'Tabella territoriale della legazione di Velletri' is collapsed into run-on paragraphs of garbled OCR (governi, place names and population figures run together) on page 3 right column (after the dating clause, beginning under 'Governo di Velletri') and page 4 left column (ending 'Totale della popolazione » 51504'); the table structure is not rendered. The reader's source note discloses 'The annexed table is printed as poorly recognized OCR', but the disclosure does not cure the collapsed-table layout.
- `gregory-xvi-acta.volume-01.line-00018307.part-01`: CHANGES_REQUIRED: the source's own dating note (footnote 2) is fused into a body sentence on page 1, left column, lower half: '2 Documentum hoc in originali refert annum millesimum octigentesimum trigesimum secundum; tamen' is set between 'respicit ven. servi Dei Ioannis' and 'Sarcander, odio catholicae fidei ...', splitting the name; the note's continuation 'invenitur iuxta seriem chronologicam anni primi Pontificatus Gregorii XVI.' appears separately in the right column after the dating clause 'anno secundo ?.'. The note must be set as a separate historical note, not interleaved with body words.

## Method

Each page PNG produced by the repository `pdf-review` tool (raster run below) was opened individually at full size; no contact sheet or thumbnail was used, and no page was re-rasterized. Each page was checked for title line, responsible issuer, date and language against the frozen metadata; headings, two-column flow, gutter, margins and glyphs (clipping, overlap, tofu); natural source closing; modern digitizer signatures; running heads or page furniture inside body sentences; marginal summaries or notes fused into body sentences; raw placeholders such as `None`; and whether the final page carries source content rather than only project apparatus. `pdftotext` was used only as a supplementary locator (e.g. searching for `Google`, `None`, running heads) and to confirm loci of findings already seen in the rasters.

Across the set, title lines, issuers, dates and the Latin/Italian labels match the frozen metadata. No clipping, overlap, missing or tofu glyphs, modern digitizer signature, journal running head, raw `None` placeholder or project-colophon-only final page was observed. Every final page carries the act's own dating clause ahead of the source/rights apparatus; sparse final pages hold genuine closing text.

## Integrity verification

Before and after review all 107 assigned digests (receipt, manifest, raster run, 38 PDFs, 66 page PNGs) were rehashed and matched the assignment (`verification-before.json`: all_match=True; `verification-after.json`: all_match=True).

| Artifact | Path | SHA256 |
|---|---|---|
| receipt | `.scratch/typeset_pipeline/claude/gregory-0002/receipt.json` | `f51816f16825bbc2ac084f0a7b4cd3daad1395e9bd69d13f5ed8de6eb8f26d49` |
| manifest | `.scratch/typeset_pipeline/claude/gregory-0002/frozen-manifest.json` | `4938980dfa1e67320b11898e1d3c22033d9bb96f235382d342fb21ad409d3574` |
| raster_run | `.scratch/claude-review/rasters-gregory-0002/review-run.json` | `f8248e8d5cf51943f723939f4f16fc258a50cfef3a20e9a37156f0e741522a57` |

## Documents

| ID | Lang | Date | Pages | PDF SHA256 | Status |
|---|---|---|---|---|---|
| `gregory-xvi-acta.volume-01.line-00015361` | la | 1832-01-27 | 1 | `8cc1f868fdfd7bdb5366d9b00f680bd5d5fb8014de435bf0c137a7ccb0d81a9b` | PASS |
| `gregory-xvi-acta.volume-01.line-00015640` | it | 1832-02-01 | 4 | `93349e35b5c7d5ecb72c457c7e46d3834924c51364a227a0e8cca4e4c6e587d2` | CHANGES_REQUIRED |
| `gregory-xvi-acta.volume-01.line-00016179` | la | 1832-02-01 | 6 | `e37dd2589e3eb5fc8faebf22ff47e4128d529410c98b45f61d401b42d8ca94bc` | PASS |
| `gregory-xvi-acta.volume-01.line-00016997` | la | 1832-02-03 | 3 | `a68a43dee464d6a8f4fdd2dbf075152420a28ab6544b62fdb6170a1890ee7bbe` | PASS |
| `gregory-xvi-acta.volume-01.line-00017334` | la | 1832-02-07 | 2 | `2cabcd3827988140b69934a12193d2b98779795e49acae59b71f372fb5b749b6` | PASS |
| `gregory-xvi-acta.volume-01.line-00017491` | la | 1832-02-17 | 1 | `716400cd80306954d876d15df7024ed62401a718e26008887768cfa48213e02a` | PASS |
| `gregory-xvi-acta.volume-01.line-00017575.part-01` | la | 1832-02-21 | 2 | `151e4e92a0369590ea697ddd323439c3c9d7c41e2a34ac5039d38c879c56a744` | PASS |
| `gregory-xvi-acta.volume-01.line-00017575.part-02` | la | 1832-02-21 | 1 | `4fa16bf7cc3b0118521957ad1f2f784a771f186bbd460cb4719bc3a805da53b2` | PASS |
| `gregory-xvi-acta.volume-01.line-00018165` | la | 1832-03-19 | 1 | `d05f3db33155eeb3bb488635ad1b003cf33a277de3f9d800a3a061f49974b69f` | PASS |
| `gregory-xvi-acta.volume-01.line-00018225` | la | 1832-03-19 | 1 | `4be94b5e3ae6efae921a91948f40c050e7f4771028ea5686f98a4fc9bc494f36` | PASS |
| `gregory-xvi-acta.volume-01.line-00018307.part-01` | la | 1832-03-24 | 1 | `a938f210d74488beed46098fe922c4b7ff24febae1813a3b69942a6e9be420a7` | CHANGES_REQUIRED |
| `gregory-xvi-acta.volume-01.line-00018307.part-02` | la | 1832-03-24 | 2 | `a5a268eab4f030ecf800a1f6ec81e49fe775e2fff961710e536244803af25a1e` | PASS |
| `gregory-xvi-acta.volume-01.line-00017794` | la | 1832-03-27 | 3 | `93708e21cb584da987c8b19ebe3e977090e9b5c26690096b8ab5d24c6da5ac8f` | PASS |
| `gregory-xvi-acta.volume-01.line-00018572` | la | 1832-04-03 | 2 | `b60ba1419f273369c30822160affd6cb818fdd3983ae59a04c295eb5d51176d2` | PASS |
| `gregory-xvi-acta.volume-01.line-00018767.part-01` | la | 1832-04-05 | 2 | `184c80f4d0d6f8aff150b17cf01a48db1764cebe731d9d65170675f520469a6a` | PASS |
| `gregory-xvi-acta.volume-01.line-00018767.part-02` | la | 1832-04-13 | 1 | `8997117a925f2ad82614ca1b5f750a83745c8db540c56d2306bb7ded608df36a` | PASS |
| `gregory-xvi-acta.volume-01.line-00019031` | la | 1832-04-16 | 1 | `6ba7c25c2c66b261b09c519e532a285dfee9149b54b1fc3f0d454a3d528ff2c8` | PASS |
| `gregory-xvi-acta.volume-01.line-00019104` | la | 1832-04-16 | 1 | `3295bb6a69b9675f8ab868980156bcc1a3f8851f910f619155066835a6d77563` | PASS |
| `gregory-xvi-acta.volume-01.line-00020111` | la | 1832-05-04 | 2 | `593c83835fb890fc46fdba4c3326058a6058b9b703fdace5cd8886f819eeaf32` | PASS |
| `gregory-xvi-acta.volume-01.line-00020264` | la | 1832-05-08 | 1 | `e8969f13a8c699a8b211e9fed450d931b7455522760a4c4207913cd52f6e4dfe` | PASS |
| `gregory-xvi-acta.volume-01.line-00020326.part-01` | la | 1832-05-11 | 4 | `a6206edceb73abc59b31856031da0f66c2062297a76f12fbfed503a841cfdfaf` | PASS |
| `gregory-xvi-acta.volume-01.line-00020326.part-02` | la | 1832-05-11 | 1 | `d387aff29c48d3534403d39643f8a93a5682c22a7454c47baff27950387947ec` | PASS |
| `gregory-xvi-acta.volume-01.line-00020916.part-01` | la | 1832-05-11 | 1 | `b6dddf4d1334d85befa7f6528b6fd0a3499a32275ad627b3b99917de98f2d079` | PASS |
| `gregory-xvi-acta.volume-01.line-00020916.part-02` | la | 1832-05-15 | 3 | `2f6cf82b4671c0fb7e6af42d5137a5404dac747c6894c56845872b1b70946eb7` | PASS |
| `gregory-xvi-acta.volume-01.line-00021293` | la | 1832-05-18 | 1 | `6e6f57c888179a4012f1fe7aee35838a8585fd42f79ac61b30e7f46c2f1cad50` | PASS |
| `gregory-xvi-acta.volume-01.line-00021419` | la | 1832-05-18 | 1 | `04f718e1d994652a439686ee7384a9c27e37dd11284c7ac480e486bbea5f0341` | PASS |
| `gregory-xvi-acta.volume-01.line-00021520.part-01` | la | 1832-05-18 | 1 | `71a1676006a183af12cffcbf86e87c1d5288a64df1ac44ed5edc72b88bfa84a1` | PASS |
| `gregory-xvi-acta.volume-01.line-00021520.part-02` | la | 1832-05-22 | 1 | `ac47dc3f893c9c73643057059ecc22b6706c74010686ed1c55b397733970f986` | PASS |
| `gregory-xvi-acta.volume-01.line-00021975.part-02` | la | 1832-06-05 | 1 | `4f0b0af4343c64be59b6f725a2bbd89704786b7369bfa91c2f095114402774f6` | PASS |
| `gregory-xvi-acta.volume-01.line-00022412.part-01` | la | 1832-06-09 | 2 | `8362e40b3454109e9cf93c421f22dc93df8ba9e99fd5af9e449bf8c7b7a456d9` | PASS |
| `gregory-xvi-acta.volume-01.line-00022888.part-02` | la | 1832-06-19 | 1 | `79d74f1860d645c5ad3291ca31633c34a1abe03e0439cb7f3689d920e0263690` | PASS |
| `gregory-xvi-acta.volume-01.line-00023191` | la | 1832-06-19 | 2 | `904ef68abe0fbe7581e43c904ecf6ffad3c42be661c53c87eb7437b51e844d7e` | PASS |
| `gregory-xvi-acta.volume-01.line-00023414` | la | 1832-06-21 | 2 | `52f32259709183d0f91b6e0fc78c9b491de21a0a9ef90f71b865072e2a3cb15d` | PASS |
| `gregory-xvi-acta.volume-01.line-00023693` | la | 1832-06-22 | 2 | `cde5b6d18a567655014ec7f43ef6b25696783f3927bd74f4c95cafa5508d2ae1` | PASS |
| `gregory-xvi-acta.volume-01.line-00023846.part-01` | la | 1832-06-22 | 1 | `af151381c85b7137cc4f15de8a4d63fa1922a48a8b76492992e052d36abfb911` | PASS |
| `gregory-xvi-acta.volume-01.line-00023846.part-02` | la | 1832-06-22 | 1 | `d8adec00729f1c86e1812936a956cbeb90e5d6128c15758f6ee63f1ea172636f` | PASS |
| `gregory-xvi-acta.volume-01.line-00024057` | la | 1832-06-26 | 1 | `93c48d96e0fcebabdda0c6f1e7371c9a2b7bf61d4391058c482c36f66faf2b56` | PASS |
| `gregory-xvi-acta.volume-01.line-00024191.part-02` | la | 1832-07-10 | 2 | `12b8a4414ed36991993596a445196d0030a3d0cb92766041954bcbffca00eed0` | PASS |

## Per-document findings and page record

### `gregory-xvi-acta.volume-01.line-00015361`

Benedicentes Domino — Approbatio Rosarii viventis cum indulgentiis — GREGORIUS PP. XVI. · 1832-01-27 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-01-27-gregory-xvi-acta-volume-01-line-00015361-b6460291-la/1832-01-27-gregory-xvi-acta-volume-01-line-00015361-b6460291-la.pdf` (`8cc1f868fdfd7bdb5366d9b00f680bd5d5fb8014de435bf0c137a7ccb0d81a9b`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `3b196f51407048a5110195adb5fe6ad5357f35109e74ee21c1911a547aa609f1` | PASS | Title, GREGORIUS PP. XVI., 1832-01-27, Latin match metadata. Two-column body flows normally from protocol to Datum Romae ... pontificatus Nostri anno primo; source/rights apparatus follows the dating clause in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00015640`

Luminose prove di fedeltà inconcussa — Erezione della legazione di Velletri — GREGORIUS PP. XVI. · 1832-02-01 · it · motu-proprio. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-01-gregory-xvi-acta-volume-01-line-00015640-f99e1922-it/1832-02-01-gregory-xvi-acta-volume-01-line-00015640-f99e1922-it.pdf` (`93349e35b5c7d5ecb72c457c7e46d3834924c51364a227a0e8cca4e4c6e587d2`), 4 page(s). Status: **CHANGES_REQUIRED**.

- CHANGES_REQUIRED: annexed 'Tabella territoriale della legazione di Velletri' is collapsed into run-on paragraphs of garbled OCR (governi, place names and population figures run together) on page 3 right column (after the dating clause, beginning under 'Governo di Velletri') and page 4 left column (ending 'Totale della popolazione » 51504'); the table structure is not rendered. The reader's source note discloses 'The annexed table is printed as poorly recognized OCR', but the disclosure does not cure the collapsed-table layout.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `12199e4f0b341f709450cae2c0e7caba04247026af3e9be11370bc72dca91e56` | PASS | Title, GREGORIUS PP. XVI., 1832-02-01, Italian match metadata. Two columns flow normally; literal OCR noise (@, pit, /') only. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `9e57932b88c2a8c4c21e7e5158714ac62c53e990703cfed5133a91c947238c89` | PASS | Body continues with numbered §§ and articles as separate short lines (literal OCR '2e', '36', '8M.'); columns, gutter and margins clean. No running head, digitizer signature or fused marginal. |
| 3 | `05dcd4111cda5e44ec7fee5bfabd9a76ae1c63bb28c4280f29c7213d34a45b45` | CHANGES_REQUIRED | §§ VI–XIII and derogation clause flow normally to the dating clause; table heading 'Governo di Velletri' then collapsed table text begins in right column. No clipping, overlap, tofu or digitizer signature. |
| 4 | `7e49295065c0ceac54ad413a094cc0aafa163ba0a6e66f8677937e70ee8cea6d` | CHANGES_REQUIRED | Final page carries source content (table remainder and total) before the source/rights apparatus, so not a colophon-only page; right column empty. No clipping, overlap, tofu or digitizer signature. |

### `gregory-xvi-acta.volume-01.line-00016179`

Exhibita siquidem Nobis — Reintegratio collegiatae Civitatis Novae et erectio paroeciae in portu — GREGORIUS EPISCOPUS · 1832-02-01 · la · bull. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-01-gregory-xvi-acta-volume-01-line-00016179-4c915a83-la/1832-02-01-gregory-xvi-acta-volume-01-line-00016179-4c915a83-la.pdf` (`e37dd2589e3eb5fc8faebf22ff47e4128d529410c98b45f61d401b42d8ca94bc`), 6 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: Responsible issuer displayed as 'GREGORIUS EPISCOPUS' per frozen metadata (bull protocol).

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `5e520b5f3a226d2771ccf8fae00c671778710e198b16b2f30ce09030637cb22a` | PASS | Title, GREGORIUS EPISCOPUS (matches frozen issuer), 1832-02-01, Latin. Address, bull protocol and salutation precede two-column body; columns, gutter, margins clean. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `506f0b1990ff7bc450fa85a5c3bc2c115d17f472ce2f29be351e222e2c30e7d1` | PASS | Dense two-column body continues; short split lines ('-ac memoratam ...', '/ proprietates ...') are literal OCR line breaks, not running heads. No clipping, overlap or digitizer signature. |
| 3 | `123e4e8d143b5730d422d1e140398f41c27677c0e7876cb3e91f157b076448aa` | PASS | Body continues in both columns; literal OCR glyph noise (€, ¢) renders without tofu. No running head, marginal fusion or digitizer signature. |
| 4 | `a67e1154a36fc3a41bb76600540b3155c6bc9047ecf29f9f3758464d94434c5a` | PASS | Body continues; isolated split lines are literal OCR breaks. Margins and gutter clean; no running head, digitizer signature or fused marginal. |
| 5 | `58fc63debee41060b549b78ca49d08ac28280ebf3947d861ec5ce3b0052ef267` | PASS | Non obstantibus clause and derogations flow normally across columns. No clipping, overlap, tofu or digitizer signature. |
| 6 | `ae339f60df4782062cb4fafff9f194a215f6c760f7ca9a5eb79ed61be84c0308` | PASS | Source-bearing final page: body closes with 'Datum Romae apud sanctum Petrum anno incarnationis Dominicae ... kalendis februarii, pontificatus Nostri anno secundo'; source/rights apparatus follows in right column. No clipping or furniture-only ending. |

### `gregory-xvi-acta.volume-01.line-00016997`

Inter gravissimas — Ad archiepiscopum primatem Armenorum Constantinopolitanum — GREGORIUS PP. XVI. · 1832-02-03 · la · encyclical. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-03-gregory-xvi-acta-volume-01-line-00016997-aa7129f7-la/1832-02-03-gregory-xvi-acta-volume-01-line-00016997-aa7129f7-la.pdf` (`a68a43dee464d6a8f4fdd2dbf075152420a28ab6544b62fdb6170a1890ee7bbe`), 3 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `8c1051407fc797dac1060b02e5c1b82058c101ba0d290030b353b7d2ea1cad77` | PASS | Title, GREGORIUS PP. XVI., 1832-02-03, Latin match metadata. Address and salutation precede two-column body; columns, gutter and margins clean. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `743807a55fb0ac10be9d78ffed5e47a3ddd4b65b0cca32b6499279d678ebaf4d` | PASS | Body continues in both columns; literal OCR breaks only. No running head, digitizer signature, fused marginal or overlap. |
| 3 | `5e187ef6137b82dbca0ea32c79bbecffcfbe2bb48377283b14af9f0685a282a8` | PASS | Source-bearing final page: body concludes with apostolic blessing and 'Datum Romae apud sanctum Petrum sub annulo piscatoris die tertia februarii ... pontificatus Nostri anno secundo'; apparatus follows in left column, right column empty. Not colophon-only. |

### `gregory-xvi-acta.volume-01.line-00017334`

Neminem vestrum profecto latet — Commissarius pro restauratione templi S. Mariae ab Angelis ad Assisium — GREGORIUS PP. XVI. · 1832-02-07 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-07-gregory-xvi-acta-volume-01-line-00017334-72cade5a-la/1832-02-07-gregory-xvi-acta-volume-01-line-00017334-72cade5a-la.pdf` (`2cabcd3827988140b69934a12193d2b98779795e49acae59b71f372fb5b749b6`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `e1d27a5881af4ee0f095b8e184102a7c5d7d7a1387caa75693e63860aee7ad79` | PASS | Title, GREGORIUS PP. XVI., 1832-02-07, Latin match metadata. Address, intitulation and salutation precede two-column body; columns, gutter and margins clean. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `b985b664c99fefb9399d73ae8db4ee5cf7f08dcdd6e2ae7a41cd49c587edc6f5` | PASS | Source-bearing final page: blessing and 'Datum Romae apud sanctum Petrum sub annulo piscatoris die septima febr. ... pontificatus Nostri anno secundo'; apparatus follows; right column empty. Not colophon-only. |

### `gregory-xvi-acta.volume-01.line-00017491`

Quoniam nobiles — Titulus baronis pro Antonio Trasmundo — GREGORIUS PP. XVI. · 1832-02-17 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-17-gregory-xvi-acta-volume-01-line-00017491-49d7c8fb-la/1832-02-17-gregory-xvi-acta-volume-01-line-00017491-49d7c8fb-la.pdf` (`716400cd80306954d876d15df7024ed62401a718e26008887768cfa48213e02a`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `cca39d1f913bedafbb97e0374c666b30c9caac5ad46383b9b2ea73fd213f1d46` | PASS | Title, GREGORIUS PP. XVI., 1832-02-17, Latin match metadata. Single-page brief: address, intitulation, body and 'Datum Romae ... die decima septima februarii ... anno secundo'; source apparatus breaks from left column foot to right column top, readable. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00017575.part-01`

Divini Nostri Reparatoris — Templum et collegium Ss. Redemptoris Syracusis — GREGORIUS PP. XVI.- · 1832-02-21 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-21-gregory-xvi-acta-volume-01-line-00017575-part-01-0b2891e6-la/1832-02-21-gregory-xvi-acta-volume-01-line-00017575-part-01-0b2891e6-la.pdf` (`151e4e92a0369590ea697ddd323439c3c9d7c41e2a34ac5039d38c879c56a744`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: Displayed issuer is the frozen metadata form 'GREGORIUS PP. XVI.-' with a literal trailing hyphen.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `7c5421f645f267634db8f8797db8f1902ac5d0fd453cdecae7bc9fee0a4a4f2e` | PASS | Title, issuer 'GREGORIUS PP. XVI.-' (literal OCR trailing hyphen, identical to frozen metadata), 1832-02-21, Latin. Two-column body flows; right column ends partway with literal 'contigerit attentari.' then continues on p2. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `76996ca309f060880e8d7b4068eac1818cb171d43b770c50ffb90ae4cb78cbb6` | PASS | Source-bearing final page: Non obstantibus clause and 'Datum Romae ... die vigesima prima februarii ... pontificatus Nostri anno secundo,'; apparatus follows; right column empty. Not colophon-only. |

### `gregory-xvi-acta.volume-01.line-00017575.part-02`

Eximia atque egregia virtutum merita — Titulus comitis pro Audentio Amorelli — GREGORIUS PP. XVI. · 1832-02-21 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-02-21-gregory-xvi-acta-volume-01-line-00017575-part-02-1c5876da-la/1832-02-21-gregory-xvi-acta-volume-01-line-00017575-part-02-1c5876da-la.pdf` (`4fa16bf7cc3b0118521957ad1f2f784a771f186bbd460cb4719bc3a805da53b2`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `965d070a6ffef2fdb2a8271262b7181b6247b0b4fc665bbf96543ee16d10f746` | PASS | Title, GREGORIUS PP. XVI., 1832-02-21, Latin match metadata. Single-page brief: intitulation, salutation, body and 'Datum Romae ... die vigesima prima februarii ... anno secundo'; apparatus split across column foot and right-column top, readable. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00018165`

Etsi ex litteris — Ad Ferdinandum Hispaniarum regem de partu reginae — GREGORIUS PP. XVI. · 1832-03-19 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-03-19-gregory-xvi-acta-volume-01-line-00018165-2b17a110-la/1832-03-19-gregory-xvi-acta-volume-01-line-00018165-2b17a110-la.pdf` (`d05f3db33155eeb3bb488635ad1b003cf33a277de3f9d800a3a061f49974b69f`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `ef7852ec330216502e65a09a205a3d30171fe61025805da96ce8c8aeefd7c7b9` | PASS | Title, GREGORIUS PP. XVI., 1832-03-19, Latin match metadata. Short letter in left column: address, intitulation, salutation, body, 'Datum Romae apud:s. Petrum die decima nona martii ... anno secundo'; apparatus follows; right column empty (sparse single page with genuine closing). No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00018225`

Nihil impensius optantes — Ad Ferdinandum Hispaniarum regem de dispensatione pro Sebastiano infante — GREGORIUS PP. XVI. · 1832-03-19 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-03-19-gregory-xvi-acta-volume-01-line-00018225-67564359-la/1832-03-19-gregory-xvi-acta-volume-01-line-00018225-67564359-la.pdf` (`4be94b5e3ae6efae921a91948f40c050e7f4771028ea5686f98a4fc9bc494f36`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `d50b3460a82c8340a988dc9c000cfafa7d3257fc4a5be6e246856b8c87cab44d` | PASS | Title, GREGORIUS PP. XVI., 1832-03-19, Latin match metadata. Short letter in left column with address, intitulation, body and dating clause 'Datum Romae apud sanctum Petrum, sub. annulo piscatoris die decima nona martii ... anno secutido,'; apparatus follows; right column empty. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00018307.part-01`

Litteris ad Pium VIII — Ad cardinalem Rodulphum archiducem archiepiscopum Olomucensem — GREGORIUS PP. XVI. · 1832-03-24 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-03-24-gregory-xvi-acta-volume-01-line-00018307-part-01-0f6cabe6-la/1832-03-24-gregory-xvi-acta-volume-01-line-00018307-part-01-0f6cabe6-la.pdf` (`a938f210d74488beed46098fe922c4b7ff24febae1813a3b69942a6e9be420a7`), 1 page(s). Status: **CHANGES_REQUIRED**.

- CHANGES_REQUIRED: the source's own dating note (footnote 2) is fused into a body sentence on page 1, left column, lower half: '2 Documentum hoc in originali refert annum millesimum octigentesimum trigesimum secundum; tamen' is set between 'respicit ven. servi Dei Ioannis' and 'Sarcander, odio catholicae fidei ...', splitting the name; the note's continuation 'invenitur iuxta seriem chronologicam anni primi Pontificatus Gregorii XVI.' appears separately in the right column after the dating clause 'anno secundo ?.'. The note must be set as a separate historical note, not interleaved with body words.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `578960ae2c4c01ff6ce65fa44f81296935532ed4e906735390b1ef6c3c6598e2` | CHANGES_REQUIRED | Title, GREGORIUS PP. XVI., 1832-03-24, Latin match metadata; body closes with 'Datum Romae apud s. Petrum sub annulo piscatoris die vigesima quarta martli ... anno secundo ?.' then the note tail and apparatus. No clipping, overlap, tofu or digitizer signature. |

### `gregory-xvi-acta.volume-01.line-00018307.part-02`

Apostolatus officium — Raphael Barissich episcopus Azotensis — GREGORIUS PP. XVI. · 1832-03-24 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-03-24-gregory-xvi-acta-volume-01-line-00018307-part-02-6c2da58c-la/1832-03-24-gregory-xvi-acta-volume-01-line-00018307-part-02-6c2da58c-la.pdf` (`a5a268eab4f030ecf800a1f6ec81e49fe775e2fff961710e536244803af25a1e`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `ea7eaeeee1e5c83ce1949fd51375c85316186bcb741ecce7c3513cdced5d3375` | PASS | Title, GREGORIUS PP. XVI., 1832-03-24, Latin match metadata. Address, intitulation, salutation and two-column body; columns, gutter, margins clean. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `ec6785a76d11855911bc7549291ec57eaeb370dddbd078c095f6b0d993ffe921` | PASS | Source-bearing final page: Non obstantibus clause and 'Datum Romae apud s. Petrum ... die vigesima quarta martii ... pontificatus Nostri anno secundo.'; apparatus follows; right column empty. Not colophon-only. |

### `gregory-xvi-acta.volume-01.line-00017794`

Universalis Ecclesiae regimen — Erectio sedis archiepiscopalis Syracusanae — GREGORIUS EPISCOPUS · 1832-03-27 · la · bull. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-03-27-gregory-xvi-acta-volume-01-line-00017794-8c303915-la/1832-03-27-gregory-xvi-acta-volume-01-line-00017794-8c303915-la.pdf` (`93708e21cb584da987c8b19ebe3e977090e9b5c26690096b8ab5d24c6da5ac8f`), 3 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: Responsible issuer displayed as 'GREGORIUS EPISCOPUS' per frozen metadata (bull protocol).

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `80f7e08db13391b774c979a62712d46523ae01d1c97c793f7f081650e8d036c0` | PASS | Title, GREGORIUS EPISCOPUS (matches frozen issuer), 1832-03-27, Latin. Bull protocol 'GREGORIUS EPISCOPUS servus servorum Dei ad perpetuam rei memoriam' then two-column body; literal OCR noise only. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `8a841fc6ad815c5733bdad06109bc76766e5d79bf09e3f34a735d6d4c50c05ce` | PASS | Dispositive body and derogations flow across both columns; short split lines are literal OCR breaks. No running head, fused marginal or digitizer signature. |
| 3 | `0b269312d20265bac64eca6e662f32cd0c1f5b39a2acaf664854fc79fe80a661` | PASS | Source-bearing final page: derogation, Nulli ergo sanction (literal trailing '7' OCR mark) and 'Datum Romae apud sanctum Petrum anno incarnationis dominicae ... sexto kalendas aprilis, pontificatus Nostri anno secundo.,'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00018572`

In suprema pastoralis ministerii — De electione supremorum moderatorum ordinum in Hispania — GREGORIUS PP. XVI. · 1832-04-03 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-04-03-gregory-xvi-acta-volume-01-line-00018572-7f4a32b6-la/1832-04-03-gregory-xvi-acta-volume-01-line-00018572-7f4a32b6-la.pdf` (`b60ba1419f273369c30822160affd6cb818fdd3983ae59a04c295eb5d51176d2`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `8b80aafaec38d1cfcdd030b329cb7e5f9d5b14290e2e88f4d52cfc5b5bf6258a` | PASS | Title, GREGORIUS PP. XVI., 1832-04-03, Latin match metadata. Intitulation 'ad perpetuam rei memoriam' then two-column body; literal OCR breaks/noise only. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `89908898a6f2fd7edd5b08757d5ca018ddaa2a52d9381b7e7176fe5226c9a32d` | PASS | Source-bearing final page: decernentes and non obstantibus clauses, 'Datum Romae apud sanctum Petrum sub annulo piscatoris die tertia aprilis ... anno secundo.'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00018767.part-01`

Quum Nostris litteris — Contrezy coadiutor vicariatus Siamensis — GREGORIUS PP. XVI. · 1832-04-05 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-04-05-gregory-xvi-acta-volume-01-line-00018767-part-01-0feb3ed8-la/1832-04-05-gregory-xvi-acta-volume-01-line-00018767-part-01-0feb3ed8-la.pdf` (`184c80f4d0d6f8aff150b17cf01a48db1764cebe731d9d65170675f520469a6a`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `8d8217bf1c5e6a001c888510c6b280c980641989a5784e96b2c88249c4699beb` | PASS | Title, GREGORIUS PP. XVI., 1832-04-05, Latin match metadata. Address, intitulation, salutation, two-column body; columns, gutter, margins clean. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `a0a804e25c62c6ba9a0650a5fc11e90910193d7e8cb1ba7a32cee3376cb8ba64` | PASS | Source-bearing final page: sanction clause (literal garbled OCR 'uam _rite / q ? gq .'), non obstantibus and 'Datum Romae apud s. Petrum ... die quinta aprilis ... anno secundo.'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00018767.part-02`

Exponendum Nobis curavit — De canone cappellaniae SS. Antonii et Sebastiani dioecesis Tifernatis — GREGORIUS PP. XVI. · 1832-04-13 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-04-13-gregory-xvi-acta-volume-01-line-00018767-part-02-35d72156-la/1832-04-13-gregory-xvi-acta-volume-01-line-00018767-part-02-35d72156-la.pdf` (`8997117a925f2ad82614ca1b5f750a83745c8db540c56d2306bb7ded608df36a`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `c3ff66a558ec977adb2d598bff83c461940b5799dfec707647055b485e7f97aa` | PASS | Title, GREGORIUS PP. XVI., 1832-04-13, Latin match metadata. Single-page brief in left column (address with literal OCR ': / :'), body and 'Datum Romae ... die decima tertia aprilis ... anno secundo.'; apparatus in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00019031`

Quam in regiae tuae maiestatis luctu — Ad Carolum Albertum Sardiniae regem — GREGORIUS PP. XVI. · 1832-04-16 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-04-16-gregory-xvi-acta-volume-01-line-00019031-b403ba34-la/1832-04-16-gregory-xvi-acta-volume-01-line-00019031-b403ba34-la.pdf` (`6ba7c25c2c66b261b09c519e532a285dfee9149b54b1fc3f0d454a3d528ff2c8`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `7afe6387d169d040a7fde235d2a00e02152a8e96a681cf7cdf648fe69357b6ec` | PASS | Title, GREGORIUS PP. XVI., 1832-04-16, Latin match metadata. Single-page letter: address, intitulation, salutation, body and 'Datum Romae apud s. Petrum ... die decima sexta aprilis ... anno secundo.'; apparatus split from left-column foot to right-column top. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00019104`

Ut ea omnia — Ad Leopoldum magnum ducem Etruriae de morte uxoris — GREGORIUS PP. XVI. · 1832-04-16 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-04-16-gregory-xvi-acta-volume-01-line-00019104-0b8c4536-la/1832-04-16-gregory-xvi-acta-volume-01-line-00019104-0b8c4536-la.pdf` (`3295bb6a69b9675f8ab868980156bcc1a3f8851f910f619155066835a6d77563`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `30d6f18ac971dc822454ff03e92a82e5e2baf5cc1f91a3100fe469222503860f` | PASS | Title, GREGORIUS PP. XVI., 1832-04-16, Latin match metadata. Single-page letter with address, intitulation, body and 'Datum Romae ... die decima sexta aprilis ... anno secundo.'; apparatus split across columns, readable. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00020111`

Apostolatus officium — Petrus Dominicus Marcellinus Bonamie episcopus Babylonensis — GREGORIUS PP. XVI. · 1832-05-04 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-04-gregory-xvi-acta-volume-01-line-00020111-abc4f5ef-la/1832-05-04-gregory-xvi-acta-volume-01-line-00020111-abc4f5ef-la.pdf` (`593c83835fb890fc46fdba4c3326058a6058b9b703fdace5cd8886f819eeaf32`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `3fc40cb5918fbf9f3e1c64bade0d269992473b3f878719c2f7a133683c065147` | PASS | Title, GREGORIUS PP. XVI., 1832-05-04, Latin match metadata. Address, intitulation, salutation and two-column body to non obstantibus and start of dating clause. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `9984433fdeab1d0a56812e5b7352b0f711514a66d175f5926a31b0164612f27a` | PASS | Sparse source-bearing final page: completion of the dating clause 'piscatoris die quarta maii ... pontificatus Nostri anno secundo.' followed by apparatus; genuine source closing, not colophon-only. |

### `gregory-xvi-acta.volume-01.line-00020264`

Animi sensus pleni pietatis — Ad Franciscum Antonium Hispaniarum infantem — GREGORIUS PP. XVI. · 1832-05-08 · la · letter. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-08-gregory-xvi-acta-volume-01-line-00020264-01da59e4-la/1832-05-08-gregory-xvi-acta-volume-01-line-00020264-01da59e4-la.pdf` (`e8969f13a8c699a8b211e9fed450d931b7455522760a4c4207913cd52f6e4dfe`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `47dd4271c43ef63eee21eba0d4c843adc32d4a6216319b94da7f3d007c8d8f9b` | PASS | Title, GREGORIUS PP. XVI., 1832-05-08, Latin match metadata. Single-page letter in left column: address, intitulation, body, 'Datum Romae apud s. Petrum ... die octava maii ... anno secundo.'; apparatus follows; right column empty. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00020326.part-01`

Romanae Ecclesiae, quae omnium ecclesiarum mater — Ecclesia S. Blasii in via Iulia Armenis concessa — GREGORIUS PP. XVI. · 1832-05-11 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-11-gregory-xvi-acta-volume-01-line-00020326-part-01-4bd82989-la/1832-05-11-gregory-xvi-acta-volume-01-line-00020326-part-01-4bd82989-la.pdf` (`a6206edceb73abc59b31856031da0f66c2062297a76f12fbfed503a841cfdfaf`), 4 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: The annexed tabella cited in the text is not printed in this edition, as the reader's source note discloses.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `9fc2f037ee5e3f3c1bfb1450029e1b81350b53f97af498e11fc1c13523a3d3c0` | PASS | Title, GREGORIUS PP. XVI., 1832-05-11, Latin match metadata. Intitulation 'ad futuram rei memoriam' and two-column narrative body; literal OCR breaks only. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `6cbc773ddc0ab9a0e9e768e3faa20c7b4ad60077cbf6a2f3c3517adae6811031` | PASS | Dispositive body continues across both columns; short split lines are literal OCR breaks. No running head, fused marginal, overlap or digitizer signature. |
| 3 | `27e49b6d82d4d2dda70f290480806af210e4287d5797f076353809b2a6969200` | PASS | Body continues (protector/primicerius provisions, missarum onera, decernentes clause); literal OCR noise (®, /, —) renders without tofu. No running head, fused marginal or digitizer signature. |
| 4 | `2577fc42a0d1c90b5243b33722eaa3de80c3bac866ec41f8a23a1c20c2083a72` | PASS | Source-bearing final page: decernentes/non obstantibus clauses and 'Datum Romae apud sanctum Petrum ... die decima prima maii ... ponti- ficatus Nos anno secundo.'; apparatus discloses that the annexed tabella cited in the text is not printed in this edition; right column empty. |

### `gregory-xvi-acta.volume-01.line-00020326.part-02`

Quum in hoc amplissimo — Titulus baronis pro Fabio Danzetta — GREGORIUS PP. XVI. · 1832-05-11 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-11-gregory-xvi-acta-volume-01-line-00020326-part-02-fc47ecc7-la/1832-05-11-gregory-xvi-acta-volume-01-line-00020326-part-02-fc47ecc7-la.pdf` (`d387aff29c48d3534403d39643f8a93a5682c22a7454c47baff27950387947ec`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `2dc1b6181f680e081cdcf6ec788482fcf63ceac7a7cf52dbe9a7203664c80184` | PASS | Title, GREGORIUS PP. XVI., 1832-05-11, Latin match metadata. Single-page brief: address, intitulation, body (literal OCR '©»'), 'Datum Romae ... die decima prima maii ... anno secundo.'; apparatus split across columns. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00020916.part-01`

Exponi Nobis nuper fecit — Indulgentiae pro monialibus S. Francisci in Hispania — GREGORIUS PP. XVI. · 1832-05-11 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-11-gregory-xvi-acta-volume-01-line-00020916-part-01-16a5cd6b-la/1832-05-11-gregory-xvi-acta-volume-01-line-00020916-part-01-16a5cd6b-la.pdf` (`b6dddf4d1334d85befa7f6528b6fd0a3499a32275ad627b3b99917de98f2d079`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `936e8e81bf6e8ff963dc9b3a33a0b2a51aa0cb164534c935cd4cdfa6bd5cc35f` | PASS | Title, GREGORIUS PP. XVI., 1832-05-11, Latin match metadata. Single-page brief: intitulation 'ad perpetuam rei memoriam', body, non obstantibus and 'Datum Romae ... die decima prima maii ... anno secundo.'; source apparatus continues from left-column foot to right-column top. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00020916.part-02`

Provida Romani Pontificis — Suppressio beneficii pro schola oppidi Montiani — GREGORIUS PP. XVI. · 1832-05-15 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-15-gregory-xvi-acta-volume-01-line-00020916-part-02-71ceb60e-la/1832-05-15-gregory-xvi-acta-volume-01-line-00020916-part-02-71ceb60e-la.pdf` (`2f6cf82b4671c0fb7e6af42d5137a5404dac747c6894c56845872b1b70946eb7`), 3 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: Dating clause ends in literal OCR corruption 'pontificatus Neatri anno Seotndtt:'.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `7ac97f24036e7d0091ef5743a7986f07ff38b35b8bc02830effc28512bf65c34` | PASS | Title, GREGORIUS PP. XVI., 1832-05-15, Latin match metadata. Address, intitulation, salutation and two-column body; literal OCR noise (®, /) without tofu. No clipping, overlap, digitizer signature or running head. |
| 2 | `ee90c777797f5007e51b0093bf9ce06aaca7f5b1f9ba0815ec0dcb7b00c1b5ec` | PASS | Body continues through decernentes and non obstantibus clauses; right column ends with 'Volumus autem quod usque dum suppres-' continuing on p3. No running head, fused marginal, overlap or digitizer signature. |
| 3 | `2e8a80d6ad0586771cc0063e4e6391f5d211b5339f8ec91d3978fe0e180c9959` | PASS | Source-bearing final page: 'Volumus autem' clause completion and dating clause 'Datum Romae ... die decima quinta maii ... pontificatus Neatri anno Seotndtt:' (literal OCR corruption); apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00021293`

Piorum hominum societates — Archisodalitas S. Venantii Camerini — GREGORIUS PP. XVI. · 1832-05-18 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-18-gregory-xvi-acta-volume-01-line-00021293-f74174c5-la/1832-05-18-gregory-xvi-acta-volume-01-line-00021293-f74174c5-la.pdf` (`6e6f57c888179a4012f1fe7aee35838a8585fd42f79ac61b30e7f46c2f1cad50`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `87d4043b3f152352560e916066c98d7dc88a0f593e0e2b60ee57e18cce60eea1` | PASS | Title, GREGORIUS PP. XVI., 1832-05-18, Latin match metadata. Single-page brief in two columns: intitulation, body, decernentes, non obstantibus and 'Datum Romae ... die decima octava maii ... anno secundo.'; apparatus in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00021419`

Praesentissimum sane patrocinium — Sodalitates B.M.V. a Candelaria in dioecesi S. Fidei — GREGORIUS PP. XVI. · 1832-05-18 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-18-gregory-xvi-acta-volume-01-line-00021419-d23ab5b3-la/1832-05-18-gregory-xvi-acta-volume-01-line-00021419-d23ab5b3-la.pdf` (`04f718e1d994652a439686ee7384a9c27e37dd11284c7ac480e486bbea5f0341`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `7960533463d2288581e7d88408a4508506ae884536818f500e39abd610829183` | PASS | Title, GREGORIUS PP. XVI., 1832-05-18, Latin match metadata. Single-page brief: address, intitulation, body in left column; dating clause 'Datum Romae ... die decima octava maii ... anno secundo.' heads the right column followed by apparatus. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00021520.part-01`

Ad augendam fidelium religionem — Indulgentiae ecclesiarum Augustinianorum Recollectorum S. Fidei de Bogota — GREGORIUS PP. XVI. · 1832-05-18 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-18-gregory-xvi-acta-volume-01-line-00021520-part-01-eed4e2e6-la/1832-05-18-gregory-xvi-acta-volume-01-line-00021520-part-01-eed4e2e6-la.pdf` (`71a1676006a183af12cffcbf86e87c1d5288a64df1ac44ed5edc72b88bfa84a1`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `973755c654548d8849985b026eab8e95c9444a3561c6c53e62eb1892a6c80973` | PASS | Title, GREGORIUS PP. XVI., 1832-05-18, Latin match metadata. Single-page brief in left column: intitulation, grant, clauses and 'Datum Romae ... die decima octava maii ... anno secundo.'; apparatus follows; right column empty. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00021520.part-02`

Piorum hominum societates — Archisodalitas Ss. Rosarii Iesu et Mariae in Urbe — GREGORIUS PP. XVI. · 1832-05-22 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-05-22-gregory-xvi-acta-volume-01-line-00021520-part-02-d477d1f3-la/1832-05-22-gregory-xvi-acta-volume-01-line-00021520-part-02-d477d1f3-la.pdf` (`ac47dc3f893c9c73643057059ecc22b6706c74010686ed1c55b397733970f986`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `bc184b7dc84b27132fce56dbf5dbe54cf633cc90bd27a9544a5bedf45c7cce02` | PASS | Title, GREGORIUS PP. XVI., 1832-05-22, Latin match metadata. Single-page brief in two columns: intitulation, body, decernentes, non obstantibus and 'Datum Romae ... die vigesima secunda maii ... anno secundo.'; apparatus in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00021975.part-02`

Romani Pontifices, quibus nihil gratius — Titulus comitis pro Philippo Marini — GREGORIUS PP. XVI. · 1832-06-05 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-05-gregory-xvi-acta-volume-01-line-00021975-part-02-5b1a4e33-la/1832-06-05-gregory-xvi-acta-volume-01-line-00021975-part-02-5b1a4e33-la.pdf` (`4f0b0af4343c64be59b6f725a2bbd89704786b7369bfa91c2f095114402774f6`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `a215bb9c252c2d9aabd3a71cebe6448c6bef1b837b7f66a405beb958d47b285c` | PASS | Title, GREGORIUS PP. XVI., 1832-06-05, Latin match metadata. Single-page brief: address, intitulation, body in left column; dating clause 'Datum Romae ... die quinta iunii millesimo octingentesimo / trigesimo secundo, pontificatus Nostri anno secundo.' continues to right-column top, then apparatus. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00022412.part-01`

Cum primum ad aures — Ad archiepiscopos et episcopos Poloniae de obedientia potestatibus praestanda — GREGORIUS PP. XVI. · 1832-06-09 · la · encyclical. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-09-gregory-xvi-acta-volume-01-line-00022412-part-01-ffb81e56-la/1832-06-09-gregory-xvi-acta-volume-01-line-00022412-part-01-ffb81e56-la.pdf` (`8362e40b3454109e9cf93c421f22dc93df8ba9e99fd5af9e449bf8c7b7a456d9`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `cbf0369546ca84324b7bd61126cf3e0c37172804d97b49a21274df73d6cdf876` | PASS | Title, GREGORIUS PP. XVI., 1832-06-09, Latin match metadata. Address 'ad omnes archiepiscopos et episcopos in Poloniae regno', intitulation, salutation and two-column body with inline scriptural/patristic citations (source's own). No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `951c905f4933ee00ce5e22d7d4802dc8e4a9db904532a11e4e8ffbae850433b0` | PASS | Source-bearing final page: body concludes with apostolic blessing and 'Datum Romae apud sanctum Petrum die nona iunii ... pontificatus Nostri anno secundo.'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00022888.part-02`

Cum civili societati — Titulus principis pro Urbano Del Drago Biscia Gentili — GREGORIUS PP. XVI. · 1832-06-19 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-19-gregory-xvi-acta-volume-01-line-00022888-part-02-2e37ab7f-la/1832-06-19-gregory-xvi-acta-volume-01-line-00022888-part-02-2e37ab7f-la.pdf` (`79d74f1860d645c5ad3291ca31633c34a1abe03e0439cb7f3689d920e0263690`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `cfcc2906013db8abf4f6bae3d2a78613acd7f560cd58afa3705d3c156199cab6` | PASS | Title, GREGORIUS PP. XVI., 1832-06-19, Latin match metadata. Single-page brief in two columns: address, intitulation, body, non obstantibus and 'Datum Romae ... die decima nona iunii ... anno secundo.'; apparatus follows in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00023191`

Maximas inter gravissimasque curas — Visitator apostolicus monasterii Altae Combae — GREGORIUS PP. XVI. · 1832-06-19 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-19-gregory-xvi-acta-volume-01-line-00023191-09669ac8-la/1832-06-19-gregory-xvi-acta-volume-01-line-00023191-09669ac8-la.pdf` (`904ef68abe0fbe7581e43c904ecf6ffad3c42be661c53c87eb7437b51e844d7e`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `4f3ff24483e72fd0f252ad5d200f40489bd06ed8c437d61e1a1c4c968fbba930` | PASS | Title, GREGORIUS PP. XVI., 1832-06-19, Latin match metadata. Address, intitulation, salutation (literal OCR stray '4' and 'ts &' lines) and two-column body. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `4fd0c8edcc6c40ab4648aff3936dce950651e48bf5d60ed3afd1abde5f464e45` | PASS | Source-bearing final page: mandates, decernentes, non obstantibus and 'Datum Romae apud s, Petrum ... die decima nona iunii ... anno secundo.'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00023414`

Quod de rei publicae tranquillitate — Excommunicatio rebellium Anconae — GREGORIUS PP. XVI. · 1832-06-21 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-21-gregory-xvi-acta-volume-01-line-00023414-d9ce9bb8-la/1832-06-21-gregory-xvi-acta-volume-01-line-00023414-d9ce9bb8-la.pdf` (`52f32259709183d0f91b6e0fc78c9b491de21a0a9ef90f71b865072e2a3cb15d`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `7a9f827eb5f99ec17f671174de93ec593429b0d6109a7bd8b3156ca7a31dcfd7` | PASS | Title, GREGORIUS PP. XVI., 1832-06-21, Latin match metadata. Intitulation 'ad perpetuam rei memoriam' and two-column narrative body with quoted citations; literal OCR breaks only. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `e0052a13ae7ed738eaa9c415cfcc60ec949d56c2dfeed155ab88e50bfb4c16ec` | PASS | Source-bearing final page: excommunication decree, decernentes clause and 'Datum Romae apud sanctum Petrum ... die vigesima prima iunii ... pontificatus Nostri anno secundo,'; apparatus follows in right column. No clipping, overlap, tofu (literal '®' renders), digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00023693`

Apostolatus officium — Theodorus Giud episcopus Halyensis — GREGORIUS PP. XVI. · 1832-06-22 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-22-gregory-xvi-acta-volume-01-line-00023693-b220f2b1-la/1832-06-22-gregory-xvi-acta-volume-01-line-00023693-b220f2b1-la.pdf` (`cde5b6d18a567655014ec7f43ef6b25696783f3927bd74f4c95cafa5508d2ae1`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `09525db82d3a211ec2d8a507c52323aa88eefe3231ac23fef77deeab8336be08` | PASS | Title, GREGORIUS PP. XVI., 1832-06-22, Latin match metadata. Address, intitulation, salutation and two-column body to the faculty grant; right column ends short with page break before the 'Volumus' clause. No clipping, overlap, tofu, digitizer signature or running head. |
| 2 | `58d4e69896cfa74a21e0797fbf5a0000ba50fe7003e383fd4c6cbdcbd82bbd1e` | PASS | Source-bearing final page: 'Volumus tamen' clause, non obstantibus and 'Datum Romae apud s. Petrum ... die vigesima secunda iunii ... anno secundo.'; apparatus follows; right column empty. |

### `gregory-xvi-acta.volume-01.line-00023846.part-01`

Pastorale officium — Theodorus Giud vicarius apostolicus Coptorum — GREGORIUS PP. XVI. · 1832-06-22 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-22-gregory-xvi-acta-volume-01-line-00023846-part-01-4d00790e-la/1832-06-22-gregory-xvi-acta-volume-01-line-00023846-part-01-4d00790e-la.pdf` (`af151381c85b7137cc4f15de8a4d63fa1922a48a8b76492992e052d36abfb911`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `32ee2e1c0b2dbce18c9d39d280d933438bf1d69fb0b750439cb70ce79223745a` | PASS | Title, GREGORIUS PP. XVI., 1832-06-22, Latin match metadata. Single-page brief: address, intitulation, body, non obstantibus and dating clause continuing to right-column top ('anno secundo.'), then apparatus. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00023846.part-02`

Piorum hominum societates — Archisodalitas in basilica S. Mariae in Cosmedin — GREGORIUS PP. XVI. · 1832-06-22 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-22-gregory-xvi-acta-volume-01-line-00023846-part-02-c21d84bf-la/1832-06-22-gregory-xvi-acta-volume-01-line-00023846-part-02-c21d84bf-la.pdf` (`d8adec00729f1c86e1812936a956cbeb90e5d6128c15758f6ee63f1ea172636f`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `cfa6e2834f88b2567658033925de0e1a36433472b4c215f1553344bb42967cc1` | PASS | Title, GREGORIUS PP. XVI., 1832-06-22, Latin match metadata. Single-page brief in two columns: intitulation 'ad futuram rei memoriam', body, decernentes/non obstantibus and '* Datum Romae ... die vigesima secunda iunii ... anno secundo,'; apparatus follows in right column. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00024057`

Exponendum Nobis curavit — Emphyteusis bonorum paroeciae S. Ioannis Evangelistae Ravennae — GREGORII PP. XVI. · 1832-06-26 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-06-26-gregory-xvi-acta-volume-01-line-00024057-4b09c0c9-la/1832-06-26-gregory-xvi-acta-volume-01-line-00024057-4b09c0c9-la.pdf` (`93c48d96e0fcebabdda0c6f1e7371c9a2b7bf61d4391058c482c36f66faf2b56`), 1 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.
- Limitation: Displayed issuer is the frozen metadata form 'GREGORII PP. XVI.' (genitive); the body intitulation reads literal OCR 'GREGORIUS PP. AVE'.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `2552566b55fac43293e531731139aea2ccd8400c759c192b70638b6930eeca67` | PASS | Title line issuer 'GREGORII PP. XVI.' matches the frozen metadata issuer; 1832-06-26, Latin. Single-page brief in two columns (literal OCR 'GREGORIUS PP. AVE', 'anbieabilta', 'Hxponendum'), dating clause 'Datum Romae apud s. Petrum sub Peetil piscatoris die vigesima sexta iunii ... anno secundo.'; apparatus follows. No clipping, overlap, tofu, digitizer signature or running head. |

### `gregory-xvi-acta.volume-01.line-00024191.part-02`

Cum, sicut Nobis nuper expositum fuit — Indulgentiae Filiarum Charitatis — GREGORIUS PP. XVI. · 1832-07-10 · la · brief. PDF `.scratch/typeset_pipeline/claude/gregory-0002/1832-07-10-gregory-xvi-acta-volume-01-line-00024191-part-02-506184ba-la/1832-07-10-gregory-xvi-acta-volume-01-line-00024191-part-02-506184ba-la.pdf` (`12b8a4414ed36991993596a445196d0030a3d0cb92766041954bcbffca00eed0`), 2 page(s). Status: **PASS**.

- No blocking finding: title, issuer, date and language match frozen metadata; two-column flow, margins and glyphs clean; no digitizer signature, running head, fused marginal/note, raw placeholder or colophon-only final page; natural dating clause retained.
- No prior_finding was assigned for this document.

| Page | PNG SHA256 | Status | Observation |
|---|---|---|---|
| 1 | `adead1ddafe3eed7aa8d13a04d0c35d1b54d773bde280444b8ea6aa25b1ca029` | PASS | Title, GREGORIUS PP. XVI., 1832-07-10, Latin match metadata. Intitulation 'ad futuram rei memoriam' and two-column body of indulgence grants; literal OCR noise (©, ~) without tofu. No clipping, overlap, digitizer signature or running head. |
| 2 | `d0b6c046ce13325b6ade96c179ceb7721a4bc8b8571ee7074a6fc46bfe1c74bd` | PASS | Source-bearing final page: 'Volumus autem' transumpt clause completion and 'Datum Romae apud sanctum Petrum ... die decima iulii ... pontificatus Nostri anno secundo.'; apparatus follows; right column empty. |

## Limitations

- Uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition; literal OCR corruption, odd spellings and stray glyphs are recorded as limitations, not defects.
- Layout review only: no word-level collation, historical authentication, facsimile comparison, publication or installation claim.
- Disclosed source-note qualifications (e.g. the unprinted annexed tabella of `line-00020326.part-01`) are recorded, not repaired. No date was inferred or repaired.
- This report does not modify source records, inventories, PDFs or release records; remediation of the two CHANGES_REQUIRED readers is left to the owning pipeline.
