# Gregory XVI visual review — batch gregory-0005, lane 01

CHANGES_REQUIRED: 49 assigned PDFs, 67 pages individually opened at full size; 48 PASS, 1 CHANGES_REQUIRED. All are new inspections, with zero reused pages. Every document is from volume 2 of the *Acta Gregorii Papae XVI* (Rome: Ex Typographia Polyglotta S. C. de Propaganda Fide, 1901), dated 1839-02-18 to 1839-12-22. No assigned document carried a `prior_finding`.

## Blocking finding

- `gregory-xvi-acta.volume-02.line-00050052` (*Officii memores tuendorum Ecclesiae iurium*, allocution, 1839-07-08), page 1, column 1, first line of the second text block (about one third down the column): the edition page number `341` survives inside a body sentence — `... quae in eodem Borussiae regno contra iura et` / `341 libertatem Ecclesiae gesta fuerant , occasione ...`. The Source note states that page numbers are omitted, so this is page furniture interrupting a body sentence. `pdftotext` of the PDF confirms the token at that locus (`341 libertatem Ecclesiae gesta fuerant`). Pages 2 and 3 of that document are otherwise clean.

## Scope and method

Each assigned page PNG was opened as its own full-size image with the Read tool (1700 × 2200 originals). No contact sheet, thumbnail, new rasterization, source acquisition, word-level collation, text correction or date reconstruction was performed. One observation per page was appended to the lane ledger in batches of two to four pages as the pages were viewed, before this report and the result were written. After the visual pass, a read-only `pdftotext` scan of all 49 assigned PDFs looked for provider signatures (`goog`, `digit`), raw `None` placeholders, `ACTA`/`vol.` running heads, and stray three-digit page numbers in the body; it found only the `341` above and the citation `pag. 318` inside a retained historical footnote.

Each page was checked for the displayed title, responsible issuer, act date and language label against the frozen metadata; headings, two-column flow, gutters, margins and glyphs; natural source closing; modern provider signatures; running heads or page furniture inside body sentences; fused marginal summaries; and raw placeholders such as `None`. Visual review is not installation, and this report makes no installation, deployment, publication or historical-authentication claim.

## Evidence verification

All assigned PDFs, the render receipt, the frozen manifest, the raster-run record and every page PNG (67 files; 119 digests in total) were hashed before and after inspection. Every digest matched its assignment pin both times (before all_match = True, after all_match = True), and the before and after records are byte-identical.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/gregory-0005/receipt.json` | `cd5071d397d7adeac276474d46e57c48ab0c04055df92a44b6405ab673f6059b` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/gregory-0005/frozen-manifest.json` | `ab67648f3199cd0214d39cc7f17847a801dfecfc8ad8e3737faf172de13b5f2a` | Before and after |
| Raster run | `.scratch/claude-review/rasters-gregory-0005/review-run.json` | `a060643196b68161636cdfb7fda163b7ac24bad2dcd2f8a56d8a615114e662be` | Before and after |
| Lane assignment | `.scratch/claude-review/gregory-0005/lane-01/assignment.json` | `cea8216de3a12c732961c2056c03ab546f5c4e4b2cc5e5d8665abf55c9c38174` | Scope binding |
| Page observation ledger | `.scratch/claude-review/gregory-0005/lane-01/observations.jsonl` | `19eb046456894568b7ad5ae8fccfdcabb7b6b880862c40acb129f68f0949e14f` | 67 unique page observations |
| Verification before | `.scratch/claude-review/gregory-0005/lane-01/verification-before.json` | `f9965e4b746dd4547b4753c533bf6c3b563f3ec8d1af04d62a6caae23ea6b08f` | 119 digests matched |
| Verification after | `.scratch/claude-review/gregory-0005/lane-01/verification-after.json` | `f9965e4b746dd4547b4753c533bf6c3b563f3ec8d1af04d62a6caae23ea6b08f` | 119 digests matched |

## Standing qualifications recorded

- **Acta running-title issuers (non-blocking, coordinator ruling).** Seven consistorial allocutions display the volume running title as issuer, each matching its frozen metadata: `g2 ACTA GREGORII PP. XVI.` (line-00057446.part-02, line-00057446.part-01), `ACTA GREGORII PP. XVI.` (line-00057760.part-02, line-00057923, line-00050052, line-00050477), `ACTA GREGORII PP. VES` (line-00058002, line-00058089; OCR-damaged XVI) and `ACTA GREGORIT PP. XVI.` (line-00055948; OCR-damaged GREGORII). All still identify Gregory XVI.
- **Other issuer forms.** `GREGORIUS EPISCOPUS` (line-00049766, a bull) and `-GREGORIUS PP. XVI.` with a stray OCR dash (line-00057300) match metadata; `GREGORIUS PP. XVI` without the final stop appears in line-00043824 and line-00049576.
- **Sparse final pages.** line-00052244 page 2 (full dating clause plus notes) and line-00056763.part-03 page 2 (dating-clause tail `anno nono.` plus notes) carry genuine source closing and are not notices-only pages.
- **Retained historical notes.** line-00056217.part-03 (edition note `(N. E.)`), line-00056763.part-01 (the letter's citation notes 2–6) and line-00057446.part-01 (note on the reserved cardinals) keep separately set historical notes, each disclosed in the Source note. In line-00056763.part-01 the citation notes stand at the foot of page 1 column 2, between `... Pius VII, eodem quo sui decessores` and the continuation `religionis et charitatis spiritu inductus` at the top of page 2. That follows the source's page-foot placement. The notes are not fused into a body line, so this is recorded as a qualification, not a blocking defect.
- **Disclosed date discrepancy (limitation).** line-00052658.part-01 (1839-09-03) prints `pontificatus Nostri anno octavo`, while other acts of this period print `anno nono`. It is recorded literally; no date was inferred or repaired.

## Per-document results

### `gregory-xvi-acta.volume-02.line-00057446.part-02` — PASS

- Title: Quo in pretio habendi illi sint — Allocutio de cardinalibus Ioanne Soglia et Antonio Tosti evulgandis
- Issuer line: `g2 ACTA GREGORII PP. XVI.`; date 1839-02-18; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-02-18-gregory-xvi-acta-volume-02-line-00057446-part-02-3971b909-la/1839-02-18-gregory-xvi-acta-volume-02-line-00057446-part-02-3971b909-la.pdf`
- PDF SHA-256: `a9882114da230a73f9ad07171df7db23c112ad64f33f6ef9f3791c16c762549c`; pages: 1
- Page 1 PNG `05d79d08fc18e6ed835a21689c082621db3efb833ee708ad03ba12ed4e49827d` — PASS: Title, issuer, 1839-02-18 and Latin match metadata. Two columns flow normally; allocution closes with 'Quid vobis videtur?', the declaration and 'In nomine Patris ... Amen,'. Source/rights notes follow in column 2. No clipping, overlap, tofu, Google signature, running head or fused marginal summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'g2 ACTA GREGORII PP. XVI.' is the volume running title with a stray OCR mark, matching frozen metadata (standing coordinator ruling for Acta allocutions).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00043543.part-01` — PASS

- Title: De universi dominici gregis salute — Henricus Hugues vicarius apostolicus Calpensis (Gibraltariae)
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-03-15; language `la`; type `papal-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-03-15-gregory-xvi-acta-volume-02-line-00043543-part-01-1e11c8f3-la/1839-03-15-gregory-xvi-acta-volume-02-line-00043543-part-01-1e11c8f3-la.pdf`
- PDF SHA-256: `948b3cdb66928b484a5dee3d2cf9b772770e742a44fefeaa51eb096718644543`; pages: 1
- Page 1 PNG `73c1fc54b9dbde4896ca52212c93979eccbb6fda588c8cf489fe3e42d4fcdb72` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-03-15, Latin match. Single-column-length text in left column with address, protocol, body, 'Mandamus propterea etc.' and dating clause 'Datum Romae ... anno nono,'. Notes follow. Clean layout, no defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00043703` — PASS

- Title: Literas libentissime accepimus — Nicolao I imperatori Russorum
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-04-06; language `la`; type `papal-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-04-06-gregory-xvi-acta-volume-02-line-00043703-5334a0da-la/1839-04-06-gregory-xvi-acta-volume-02-line-00043703-5334a0da-la.pdf`
- PDF SHA-256: `34aef5ce408c6f620f67daa60ca25b12514142b61d2f330e250cc233ac392ef7`; pages: 1
- Page 1 PNG `0b7a6f974c383682828a83382212c845041c885a840d105b74ae461d975d9ffc` — PASS: Title, issuer, 1839-04-06, Latin match. Two columns flow normally to dating clause 'Datum Romae apud ee Petrum die sexta aprilis ... anno nono.' then notes. No glyph, furniture or signature defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00043824` — PASS

- Title: Cum propter egregias — Iacobus Philippus cardinalis Franzoni protector oppidi Visso
- Issuer line: `GREGORIUS PP. XVI`; date 1839-04-12; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-04-12-gregory-xvi-acta-volume-02-line-00043824-9902c04e-la/1839-04-12-gregory-xvi-acta-volume-02-line-00043824-9902c04e-la.pdf`
- PDF SHA-256: `f16618506077a1ed5edc58291c31446b9d3cf75cf8ae341ae93a2a0e277600f3`; pages: 1
- Page 1 PNG `e2b9ec5014efe7325ae3a79135015c97c30f8ed66c3d70cd99ad1604d5e7962d` — PASS: Title, issuer GREGORIUS PP. XVI, 1839-04-12, Latin match. Address, protocol, salutation, body, non obstantibus and dating clause 'Datum Romae ... anno nono,' in column 1. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking layout note: the Source note fills the foot of column 1 and the short project licence line ('Triptych organization and typesetting: CC BY 4.0 ...') breaks to the top of column 2. Page also carries the full source body and dating clause, so this is not a notices-only page.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00043900` — PASS

- Title: Romanorum munificentia Pontificum — Cappa magna, lychnus et ferula canonicis collegialis Balernae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-04-16; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-04-16-gregory-xvi-acta-volume-02-line-00043900-db049784-la/1839-04-16-gregory-xvi-acta-volume-02-line-00043900-db049784-la.pdf`
- PDF SHA-256: `f130cc83636f597bcb2c91cccd62b71f71a87768821c26b0486d13469021fb9b`; pages: 1
- Page 1 PNG `f8fe28a1af8ff881bf2b264f334a08b7a91279f2b67b089a20993fafdd8e99ef` — PASS: Title, issuer, 1839-04-16, Latin match. Two columns flow normally; some OCR line-fragment paragraph breaks ('iudices ordinarios...', '_collegii etiam...') are literal OCR segmentation, not layout defects. Closes with dating clause then notes. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00044004.part-01` — PASS

- Title: Romanorum indulgentia Pontificum — Rochettum canonicis collegialis Serravallis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-04-19; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-04-19-gregory-xvi-acta-volume-02-line-00044004-part-01-798eaac0-la/1839-04-19-gregory-xvi-acta-volume-02-line-00044004-part-01-798eaac0-la.pdf`
- PDF SHA-256: `1054f9f69fc2f8d5d67629c497afe93d8cc30dc2053ae508b75a508b75a00049`; pages: 1
- Page 1 PNG `fe3d77e6cc84d4e13939a93434f90db7921062ba8bb78970420b81e1e6d8f9f8` — PASS: Title, issuer, 1839-04-19, Latin match. Two columns flow normally; literal OCR line-fragment breaks only. Closes with 'Datum Romae ... anno nono.' then notes. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00057760.part-02` — PASS

- Title: Virtutes ac merita beati Alphonsi de Ligorio — Allocutio in consistorio semipublico de canonizatione b. Alphonsi
- Issuer line: `ACTA GREGORII PP. XVI.`; date 1839-05-08; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-08-gregory-xvi-acta-volume-02-line-00057760-part-02-001b4200-la/1839-05-08-gregory-xvi-acta-volume-02-line-00057760-part-02-001b4200-la.pdf`
- PDF SHA-256: `94b4db5e523abca470eccac271a0e8a39cc917ca9f261347c91580139bc05bac`; pages: 1
- Page 1 PNG `a18f5b45399242ba0de391b5d1b450a772283dd86ce724fd8a28a48bc70a0a7e` — PASS: Title, 1839-05-08, Latin match. Body in column 1 from 'Venerabiles fratres' to the closing response '... sententiam proferemus.'; source notes in column 2. A literal OCR '©' after 'Ligorio,' is OCR noise, not a layout defect. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. XVI.' is the volume running title, matching frozen metadata (standing coordinator ruling for Acta allocutions).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00044004.part-02` — PASS

- Title: Cum religiosae familiae — Translatio festi s. Francisci de Paula pro regno Siciliae citra Pharum
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-10; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-10-gregory-xvi-acta-volume-02-line-00044004-part-02-9771adab-la/1839-05-10-gregory-xvi-acta-volume-02-line-00044004-part-02-9771adab-la.pdf`
- PDF SHA-256: `61bf3379c19310c0af711e4834aa4b77716154189807945326ca56d76b64478a`; pages: 1
- Page 1 PNG `2ea442f5c1c3fbccf73f38bbc5bf5b518da6fcccd47ad5c6b9b6240ec7abb70a` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-05-10, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono,' then notes. Literal OCR line-fragment breaks only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00057923` — PASS

- Title: Quam b. Francisci de Hieronymo speciem — Allocutio in consistorio semipublico de canonizatione b. Francisci de Hieronymo
- Issuer line: `ACTA GREGORII PP. XVI.`; date 1839-05-10; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-10-gregory-xvi-acta-volume-02-line-00057923-550c71be-la/1839-05-10-gregory-xvi-acta-volume-02-line-00057923-550c71be-la.pdf`
- PDF SHA-256: `73d69b8a02bfe79a84d56f6157785ae2b246dd69c193ea57b16cd7e2a54652de`; pages: 1
- Page 1 PNG `f8db9b2117e034201e99bc3ffb9b6a1353a54d6cd92d69a3599f83d632841c29` — PASS: Title (three lines), 1839-05-10, Latin match. Allocution body in column 1 closes with '... ad eius voluntatem possimus.' Notes follow. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. XVI.' is the volume running title, matching frozen metadata (standing coordinator ruling for Acta allocutions).; Page 1: Non-blocking layout note: the Source note begins at the foot of column 1 and continues at the top of column 2.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00044004.part-03` — PASS

- Title: Romani Pontifices de universae christianae — Administratio piae domus ssmae Crucis in via Longa religiosis Boni Pastoris tributa
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-11; language `la`; type `motu-proprio`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-11-gregory-xvi-acta-volume-02-line-00044004-part-03-338866bc-la/1839-05-11-gregory-xvi-acta-volume-02-line-00044004-part-03-338866bc-la.pdf`
- PDF SHA-256: `d88091b01ed29d00d857ee54009e64eb68c4bba161855105c147048f83907cfb`; pages: 2
- Page 1 PNG `1894e96d645aa7f0de022eb86767daafc4d25c8c423e72593b737c51b35726a4` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-05-11, Latin match. Dense two-column body flows normally from protocol into column 2 and onward to page 2. Literal OCR line-fragment breaks only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `168f8581abc15e4bca8dc271da39607bb9d4e82d3c2b55729dfefe6c48ea91b8` — PASS: Page 2 of 2. Body continues in column 1 through decernentes, non obstantibus and dating clause 'Datum Romae ... anno nono,'. Notes follow. Genuine source closing present. No blocking defects.
- Findings: Page 2: Non-blocking layout note: the Source note begins at the foot of column 1 and continues at the top of column 2.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00058002` — PASS

- Title: Exempla virtutum sancti Petri de Alcantara — Allocutio in consistorio semipublico de canonizatione b. Ioannis Iosephi a Cruce
- Issuer line: `ACTA GREGORII PP. VES`; date 1839-05-15; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-15-gregory-xvi-acta-volume-02-line-00058002-7248030c-la/1839-05-15-gregory-xvi-acta-volume-02-line-00058002-7248030c-la.pdf`
- PDF SHA-256: `2a17775e832561054ec318efbe5fe474b0e1cad9f86539fbd2ae925059130fd9`; pages: 1
- Page 1 PNG `4159a0a01e2a32724a7e8d059662daebc49831f06ab348a5461f9fa57b498e77` — PASS: Title (three lines), 1839-05-15, Latin match. Allocution body in column 1 closes with '... bene ac feliciter expediatur.' Notes in column 2. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. VES' is the OCR-damaged volume running title (XVI read as VES), matching frozen metadata and still identifying the pope (standing coordinator rulings).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00044004.part-04` — PASS

- Title: Romanorum beneficentia Pontificum — Collare violaceum et aureum numisma canonicis cathedralis Massae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-17; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-17-gregory-xvi-acta-volume-02-line-00044004-part-04-97736c4c-la/1839-05-17-gregory-xvi-acta-volume-02-line-00044004-part-04-97736c4c-la.pdf`
- PDF SHA-256: `75707f9d45cd6ba8739b0bbc46dbbe994467aa5e7577eb6ba75ce5d2f1df7d1a`; pages: 1
- Page 1 PNG `3c2c88bd7face6c95f878754e5e0deef430428ebd41260157353c758d2c2db85` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-05-17, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR noise ('€X', 're-~') is not a layout defect. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00044539.part-01` — PASS

- Title: Ex munere pastoralis ministerii — Erectio vicariatus apostolici latini ritus in Aegypto et Arabia
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-17; language `la`; type `motu-proprio`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-17-gregory-xvi-acta-volume-02-line-00044539-part-01-4170bdce-la/1839-05-17-gregory-xvi-acta-volume-02-line-00044539-part-01-4170bdce-la.pdf`
- PDF SHA-256: `ed5726eea32b0ce74132069994a89637beb913d7340467546d72d936522a89d9`; pages: 1
- Page 1 PNG `cdcaddc77d81f275c86fbe531619ef1dede80886c4ea2d6ad5a954cd1c5a9fbf` — PASS: Title, issuer, 1839-05-17, Latin match. Dating clause 'Datum Romae apud sanctum Petrum sub annulo' runs from foot of column 1 into column 2 '... anno nono..' in normal reading order; notes follow. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00058089` — PASS

- Title: Insigne instituti Seraphici decus — Allocutio in consistorio semipublico de canonizatione b. Pacifici a S. Severino
- Issuer line: `ACTA GREGORII PP. VES`; date 1839-05-17; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-17-gregory-xvi-acta-volume-02-line-00058089-55b9818f-la/1839-05-17-gregory-xvi-acta-volume-02-line-00058089-55b9818f-la.pdf`
- PDF SHA-256: `f965438cbd74fbd4b6f4f2832a49c0fae280680b8282c5d36257b1e8e48cdbe1`; pages: 1
- Page 1 PNG `37de8afbf6fb99b59ccfb0996bdd2e361aa0ed6aea38b41c3888e88290b9d085` — PASS: Title, 1839-05-17, Latin match. Allocution body in column 1 closes with '... ut lumen suum Nobis benignus impertiat.' Notes follow in column 1; column 2 empty. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. VES' is the OCR-damaged volume running title (XVI read as VES), matching frozen metadata and still identifying the pope (standing coordinator rulings).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00048064` — PASS

- Title: Pastorale officium Nobis — Perpetuus a Solero vicarius apostolicus Aegypti et Arabiae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-28; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-28-gregory-xvi-acta-volume-02-line-00048064-bb2fd15a-la/1839-05-28-gregory-xvi-acta-volume-02-line-00048064-bb2fd15a-la.pdf`
- PDF SHA-256: `d338315c525f310867e5af704b3520780713ee8a71972e59f0ab8384e42a2b1d`; pages: 1
- Page 1 PNG `595d9498a23ccc28c32055074dbc3f2bdc8836bb3ee6a48f436dc9ad9f849858` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-05-28, Latin match. Address, protocol, salutation and body flow through two columns to dating clause 'Datum Romae ... anno nono.' then notes. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00048157` — PASS

- Title: Cum ad ecclesiastica negotia — Franciscus Villardell visitator apostolicus patriarchatus Chaldaeorum
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-28; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-28-gregory-xvi-acta-volume-02-line-00048157-601a3634-la/1839-05-28-gregory-xvi-acta-volume-02-line-00048157-601a3634-la.pdf`
- PDF SHA-256: `ca585280387da130f70e085459b6e985f2e728f8e522bf1c26eb0cc371d01343`; pages: 1
- Page 1 PNG `3c2fa554103f3a43e649c32205f78f2996c6416b7a9e286ad1a21a26eb4e9a70` — PASS: Title, issuer, 1839-05-28, Latin match. Address, protocol, body, 'Mandamus propterea etc.' and dating clause in column 1 followed by notes; column 2 empty. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00048219` — PASS

- Title: Romani beneficentia Pontificis — Rocchetum canonicis collegiatae Castri Novi ad Scriviam
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-28; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-28-gregory-xvi-acta-volume-02-line-00048219-caa41271-la/1839-05-28-gregory-xvi-acta-volume-02-line-00048219-caa41271-la.pdf`
- PDF SHA-256: `ec118173dd5d1a610f2149ec23a04c28248ab36bcb61f617b40e9a882ff3ae92`; pages: 1
- Page 1 PNG `35f372f4986a3c15a3a3aff1f9c3c5f2fe24e92bce9c30d8bfcfa7f861630f72` — PASS: Title, issuer, 1839-05-28, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR line-fragment break only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00048325` — PASS

- Title: Cum christifidelibus rituum orientalium — Perpetuus a Solero delegatus apostolicus pro Aegypto et Arabia
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-28; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-28-gregory-xvi-acta-volume-02-line-00048325-223df887-la/1839-05-28-gregory-xvi-acta-volume-02-line-00048325-223df887-la.pdf`
- PDF SHA-256: `6dab373a3797e3ae4346cd0c01d26f4469799953b95e03d4cf0a53674a841f98`; pages: 1
- Page 1 PNG `ac5aa7b79ed5bbcd474ffa139e4bafe810403c3516cd0a1643c4f4a2ca3f970d` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-05-28, Latin match. Address, protocol, body, non obstantibus and dating clause 'Datum Romae ... anno nono.' in column 1; notes follow; column 2 empty. Literal OCR line-fragment breaks only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00048401` — PASS

- Title: In suprema Principis Apostolorum specula — Erectio collegiatae ecclesiae s. Laurentii Urbisaliae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-05-28; language `la`; type `motu-proprio`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-05-28-gregory-xvi-acta-volume-02-line-00048401-e5e81c1d-la/1839-05-28-gregory-xvi-acta-volume-02-line-00048401-e5e81c1d-la.pdf`
- PDF SHA-256: `1453c960174780bc799ef578f0bf617b4b6c4ccc7da9c05c6a2e742a10179e16`; pages: 4
- Page 1 PNG `f8c0aab11de65a564b23625d4eb7f1b6c6b32fe41789e7fa4b1084b1b64ee553` — PASS: Page 1 of 4. Title, issuer GREGORIUS PP. XVI., 1839-05-28, Latin match. Dense two-column body flows normally; literal OCR stray bars ('|') and line-fragment breaks are OCR artefacts, not running heads or fused summaries. No clipping, overlap, tofu or signature.
- Page 2 PNG `736f20decf91a7740af059c2ea50fdc56154af3f21e0692950abc9728bdacc88` — PASS: Page 2 of 4. Full two-column body continues in normal order without page furniture, running heads, provider signatures or fused marginal summaries. No clipping or overlap.
- Page 3 PNG `146dd1ab71cacd92be24d843e705425ab05640ea1af040e9269a88349c60734a` — PASS: Page 3 of 4. Full two-column body continues in normal order; no running heads, page furniture, signatures, fused summaries, clipping or overlap.
- Page 4 PNG `7d85f1b1cea2508cb94fc309c03ebca1902118f1a1492e61eceb963918a0a34a` — PASS: Page 4 of 4. Column 1 carries the body's end: decernentes, non obstantibus, transumpta clause and dating clause 'Datum Romae ... anno nono.' followed by notes; column 2 empty. Genuine source-bearing final page. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00049953` — PASS

- Title: Romani Pontifices honorum insignia — Lychnus manuleatus canonicis metropolitanae Senensis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-06-05; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-06-05-gregory-xvi-acta-volume-02-line-00049953-367b8a56-la/1839-06-05-gregory-xvi-acta-volume-02-line-00049953-367b8a56-la.pdf`
- PDF SHA-256: `f612a2039040e396f1cde9cd31d7443a761a6bc602c33f3fd701ee867e046fc4`; pages: 1
- Page 1 PNG `d51fc6973f1ed4eaf248070abaeef27eb80ba1f2a36fe4cd72ed8c555f24b0a0` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-06-05, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR line-fragment breaks only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00049576` — PASS

- Title: Romanus Pontifex externa honorum insignia — Mozzetta violacea canonicis sanctuarii s. Mariae in Horto Clavarii
- Issuer line: `GREGORIUS PP. XVI`; date 1839-06-18; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-06-18-gregory-xvi-acta-volume-02-line-00049576-8a9192d0-la/1839-06-18-gregory-xvi-acta-volume-02-line-00049576-8a9192d0-la.pdf`
- PDF SHA-256: `75fc753aaff67e4722da78ce1e8520b1b54fd3f52be558ab4e0e09b58c5f3b12`; pages: 1
- Page 1 PNG `03d0b87dbdddbc94d075686f741f18c0c7c7b1043c28359db9612250de793e4d` — PASS: Title, issuer GREGORIUS PP. XVI, 1839-06-18, Latin match. Body fills column 1; dating clause 'Datum Romae ... anno nono.' opens column 2 followed by notes. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00049679` — PASS

- Title: Patriarchalem basilicam Nostram Lateranensem — Calix aureus basilicae Lateranensi donatus
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-06-21; language `la`; type `papal-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-06-21-gregory-xvi-acta-volume-02-line-00049679-b1caf58b-la/1839-06-21-gregory-xvi-acta-volume-02-line-00049679-b1caf58b-la.pdf`
- PDF SHA-256: `8a942853df511baccd4bb13de5a3b6c0c1e7fe3a28126907be676cb24aea10bf`; pages: 1
- Page 1 PNG `31356620e3116a1e460333ebdeeb44bc60fb3f7e7fa806afe05afe30cd5cfd76` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-06-21, Latin match. Address, protocol, salutation and body in column 1; dating clause opens column 2 followed by notes. Literal OCR noise ('eid2:m_') only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00049766` — PASS

- Title: Romani Pontifices, quibus universalis Ecclesiae procuratio — Suppressio tituli s. Eusebii et erectio tituli s. Gregorii in Monte Caelio
- Issuer line: `GREGORIUS EPISCOPUS`; date 1839-06-28; language `la`; type `bull`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-06-28-gregory-xvi-acta-volume-02-line-00049766-3409e243-la/1839-06-28-gregory-xvi-acta-volume-02-line-00049766-3409e243-la.pdf`
- PDF SHA-256: `444bd8db7ffe2995e2a0fef26733f6767237bfec5cc46e5f4e83ff44ac93b9f5`; pages: 2
- Page 1 PNG `c1b2a89dd7334ef2597832a69c6e7839f3280c49be1894e2b32d0c533f32b24f` — PASS: Page 1 of 2. Title (three lines), issuer GREGORIUS EPISCOPUS (bull form, matching metadata), 1839-06-28, Latin match. Protocol 'servus servorum Dei / ad perpetuam rei memoriam' then dense two-column body in normal order. Literal OCR line-fragment breaks only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `e39a010e4a3bf15406ed0368de0fad41629dd5e6207cad55b09948a079d64962` — PASS: Page 2 of 2. Body ends in column 1 with non obstantibus, sanction clause 'Nulli ergo omnino hominum ...' and dating clause 'Datum Romae ... anno incarnationis dominicae ... quarto kalendas iulias, ... anno nono,' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050052` — CHANGES_REQUIRED

- Title: Officii memores tuendorum Ecclesiae iurium — Allocutio de archiepiscopo Gnesnensi et Posnaniensi a Borussico gubernio damnato
- Issuer line: `ACTA GREGORII PP. XVI.`; date 1839-07-08; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-07-08-gregory-xvi-acta-volume-02-line-00050052-a7cf491e-la/1839-07-08-gregory-xvi-acta-volume-02-line-00050052-a7cf491e-la.pdf`
- PDF SHA-256: `e28c1b78c24afff3b5e3663f66ab1dfb7b0b659c1d5c4484a18529acc1c0d8f1`; pages: 3
- Page 1 PNG `e13b996cc989b7ceefe3cdac3d71946b837d1c88a9c9e2e07c0b6ed282f48a50` — CHANGES_REQUIRED: Page 1 of 3. Title (three lines), 1839-07-08, Latin match. Two-column body flows normally apart from the stray edition page number '341' fused into a body sentence at the head of column 1's second block. No clipping, overlap, tofu or provider signature.
- Page 2 PNG `02e49e018c3f42e58ab2b63cc2f292e1158c9f56998a9a0f53a927b05231c580` — PASS: Page 2 of 3. Full two-column body continues in normal order; no running heads, page numbers, signatures, fused summaries, clipping or overlap. Literal OCR line-fragment breaks only.
- Page 3 PNG `9739088a88beda8f3b181d78f33bd10ad7e48a66d37195f42673ea8dc61f4fb5` — PASS: Page 3 of 3. Body ends in column 1 with '... in eiusdem bonum convertat.', the allocution's natural close, followed by notes; column 2 empty. Genuine source-bearing final page. No blocking defects on this page.
- Findings: Page 1: Page furniture interrupting a body sentence: page 1, column 1, first line of the second text block (about one third down the column), the edition page number '341' is set inside the sentence '... quae in eodem Borussiae regno contra iura et | 341 libertatem Ecclesiae gesta fuerant ...'. The source note says page numbers are omitted; this one survives mid-sentence.; Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. XVI.' is the volume running title, matching frozen metadata (standing coordinator ruling for Acta allocutions).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050477` — PASS

- Title: Quanta, propter insignia in Ecclesiam promerita — Allocutio de cardinalibus Bianchi, de Angelis, Ferretti et Pignatelli
- Issuer line: `ACTA GREGORII PP. XVI.`; date 1839-07-08; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-07-08-gregory-xvi-acta-volume-02-line-00050477-b1d06e84-la/1839-07-08-gregory-xvi-acta-volume-02-line-00050477-b1d06e84-la.pdf`
- PDF SHA-256: `6fa4a2642220d46e0d1c080509d7e02bd27d31f35392d0df104a55fa8912812c`; pages: 2
- Page 1 PNG `9d77e9e7dc001970e80de0fb8f8c832ad69f418e257dec0076859c0a5490eb8f` — PASS: Page 1 of 2. Title, 1839-07-08, Latin match. Two-column body flows normally through the four cardinal notices, 'Quid vobis videtur?' and the start of the declaration. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `8d243bf484fd757d23e84d97537a12a4134d488a04af2b9612482825f1fb36b5` — PASS: Page 2 of 2. Column 1 completes the declaration list, the dispensation clause and 'In nomine Patris >X< et Filii 9 et Spiri- tus >¥ Sancti. Amen.' (literal OCR of cross glyphs), followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORII PP. XVI.' is the volume running title, matching frozen metadata (standing coordinator ruling for Acta allocutions).; Page 1: Non-blocking layout note: the address 'Venerabiles fratres' shares the first line with the incipit, and the opening sentence is broken by literal OCR line-fragment paragraph breaks.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050365` — PASS

- Title: Veliterna ecclesia — Collare, vestis talaris et fascia violacea capitulo cathedralis Veliternae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-07-12; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-07-12-gregory-xvi-acta-volume-02-line-00050365-0145405a-la/1839-07-12-gregory-xvi-acta-volume-02-line-00050365-0145405a-la.pdf`
- PDF SHA-256: `d55cdf57ef0d1426184eade005c54381fff62a800670fddfa5011bb44c6be0a8`; pages: 1
- Page 1 PNG `ede476afff29e2d4c6b76a42f0167abe39fb59acec13c3dbbefd363887e01e1a` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-07-12, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR line-fragment breaks only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050591` — PASS

- Title: Cum Nobis nihil potius — Archisodalitas B. Mariae Virginis a Providentia in ecclesia s. Caroli ad Catinarios
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-07-16; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-07-16-gregory-xvi-acta-volume-02-line-00050591-28efe7c8-la/1839-07-16-gregory-xvi-acta-volume-02-line-00050591-28efe7c8-la.pdf`
- PDF SHA-256: `d0b3c80c4f1a87f5c3d47ef105966302d8779c481e58eb066304841b70d506c9`; pages: 1
- Page 1 PNG `8bb0dcd3d7813e7591c16ab7c3774c5af2a4e4b928c2dfaf0554a7d1aa3264e4` — PASS: Title, issuer, 1839-07-16, Latin match. Two columns flow normally to dating clause 'Datum Romae apud s. Mariam Maiorem ... anno nono.' then notes. Literal OCR noise ('E<ponendum', 'tentar1') only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050903` — PASS

- Title: Romanorum munificentia Pontificum — Floccus violaceus in pileo canonicis cathedralis Comaclensis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-07-30; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-07-30-gregory-xvi-acta-volume-02-line-00050903-6098f79e-la/1839-07-30-gregory-xvi-acta-volume-02-line-00050903-6098f79e-la.pdf`
- PDF SHA-256: `fe2edced46cdb2de7cecbc50763acc67eaad7b84f4829447c4dc4b5f1871a81b`; pages: 1
- Page 1 PNG `0020dd952f89909d99363e6751b26e3ce1d14d052ff8c791270319782e8418b4` — PASS: Title, issuer, 1839-07-30, Latin match. Two columns flow normally to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono.' then notes. Literal OCR stray degree mark after 'memoriam.' is OCR noise. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00050991` — PASS

- Title: Cum Nobis innotuerit in Tunquino Orientali — Facultas eligendi vicarium apostolicum et coadiutorem Tunquini Orientalis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-02; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-02-gregory-xvi-acta-volume-02-line-00050991-6059937e-la/1839-08-02-gregory-xvi-acta-volume-02-line-00050991-6059937e-la.pdf`
- PDF SHA-256: `54350972023652fc62b471adae70f78bc5417b52d11dd89cf1ade584f714a931`; pages: 2
- Page 1 PNG `dd352c5bf4267b6c136ed39888956979ed531f4cfc06b86ca422a38e44d6cafc` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-08-02, Latin match. Address, protocol, salutation and dense two-column body flow normally. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `72a1033e8d3ee2550da19ac85db6c2084ad0d70be68810932c8c4fbd8974d517` — PASS: Page 2 of 2. Column 1 completes the non obstantibus clause and dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono.' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00051279.part-02` — PASS

- Title: Romani Pontifices honorum insignia — Rocchetum et mozzetta violacea canonicis collegialis Roccagorgae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-06; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-06-gregory-xvi-acta-volume-02-line-00051279-part-02-9cce6599-la/1839-08-06-gregory-xvi-acta-volume-02-line-00051279-part-02-9cce6599-la.pdf`
- PDF SHA-256: `2d776793a63e7f1da2576f88d17fe618107b917d3b88c480dcba77cebe6dce04`; pages: 1
- Page 1 PNG `d6b480d2b51281fc2c7b4f919633b31a301402cbd895bedbe338fbc54771b772` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-08-06, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR line-fragment breaks (one ending in a dash) only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00051526.part-02` — PASS

- Title: Cum ex recta sedulaque iuventutis institutione — Publicae scholae Anagninae cum seminario coniunctae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-09; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-09-gregory-xvi-acta-volume-02-line-00051526-part-02-115b4bbb-la/1839-08-09-gregory-xvi-acta-volume-02-line-00051526-part-02-115b4bbb-la.pdf`
- PDF SHA-256: `133ec57f60a08ab5661a040f91e617887c402b0138737861657b39473397b279`; pages: 2
- Page 1 PNG `644c150b05ac4c6f8d408d1f171cbd06254162e04e6644bbf67dd350fc095a93` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-08-09, Latin match. Dense two-column body flows normally; literal OCR line-fragment breaks and noise ('d2', 'p2nsitandam') only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `36d2ca3ff11fceb147c20320d7a1bf7f1f1861dc8270dad6f6c58a1aef4746c6` — PASS: Page 2 of 2. Body continues through decernentes and non obstantibus to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono,' then notes in column 2. Stray OCR bar after 'Anagni-' is OCR noise. Genuine source closing. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00051911` — PASS

- Title: Romanus Pontifex honorum insignia — Parva aurea crux et lychnus manuleatus canonicis cathedralis Fesulanae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-13; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-13-gregory-xvi-acta-volume-02-line-00051911-7c087d8f-la/1839-08-13-gregory-xvi-acta-volume-02-line-00051911-7c087d8f-la.pdf`
- PDF SHA-256: `dbd5a982be46b89d3741a4ee31f81d4761661925ed3d7756d28822a6ad2b533b`; pages: 1
- Page 1 PNG `33bff9cd16e9ea0ea0759edd4c69855b9dfe1f77d62e9daf23f3c495d1c4d893` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-08-13, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR stray bar/period at line-fragment breaks only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052014` — PASS

- Title: Mutinensis ecclesia originis vetustate — Focale, floccus et tibialia violacei coloris capitulo cathedralis Mutinensis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-14; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-14-gregory-xvi-acta-volume-02-line-00052014-1d0be6f2-la/1839-08-14-gregory-xvi-acta-volume-02-line-00052014-1d0be6f2-la.pdf`
- PDF SHA-256: `db8211bede3ab69177830c5f4addddcd211497b222017df034b639ee1ed18298`; pages: 1
- Page 1 PNG `b1244faf3df01116d53bd74c3c6fac6d8f1afbe64171a0f39c15442707af73b0` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-08-14, Latin match. Two columns flow normally to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono.' then notes. Literal OCR noise only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052133` — PASS

- Title: Romani Pontificis beneficentia — Cappa magna et cotta canonicis collegialis Montis Rubbiani
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-16; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-16-gregory-xvi-acta-volume-02-line-00052133-fe0dcdca-la/1839-08-16-gregory-xvi-acta-volume-02-line-00052133-fe0dcdca-la.pdf`
- PDF SHA-256: `d73d7180434fb8e2bfe7b88f47bf6f02644c335813427968043dac8098b21652`; pages: 1
- Page 1 PNG `ace5215c24cd07e0368a211bb6a5d0ebb8342a1084674000b64f20ded35eae1d` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-08-16, Latin match. Two columns flow normally to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono,' then notes. Stray OCR bar at a line-fragment break is OCR noise. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052244` — PASS

- Title: Ad ceteras animi angustias — Nicolao episcopo Waterfordiensi et Lismorensi de concordia inter clerum et Franciscales
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-19; language `la`; type `papal-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-19-gregory-xvi-acta-volume-02-line-00052244-7351d07c-la/1839-08-19-gregory-xvi-acta-volume-02-line-00052244-7351d07c-la.pdf`
- PDF SHA-256: `e761b8002043e331992dbdbd21ece3ad471ef6ba018c88fbb1fc3a4d6c9ad306`; pages: 2
- Page 1 PNG `517b3e94fecb16e7c813bc7dfa240ba995a8ab8b173a76f8532f70aa360b2cf0` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-08-19, Latin match. Address, protocol, salutation and body flow through two columns to '... apostolicam benedictionem ... peramanter impertimur.' Literal OCR stray bars and fragment breaks only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `b3a67a7090356039290cd511e34ec43bf8e5ad81124ecec8b7c870411e5185cd` — PASS: Page 2 of 2. Column 1 holds the dating clause and notes; rest blank. Genuine source closing. No blocking defects.
- Findings: Page 1: Non-blocking layout note: column 2 ends about halfway down page 1 after the apostolic benediction, leaving its lower half blank, and the dating clause with the notes begins page 2 (apparently kept together with the closing apparatus). No text is lost or reordered.; Page 2: Non-blocking qualification: sparse final page carrying only the genuine dating clause 'Datum Romae apud sanctam Mariam Maiorem die decima nona augusti ... anno nono,' and the notes; the dating clause is source-bearing, so this is not a notices-only page.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052386.part-01` — PASS

- Title: Illustres inter pontificiae Nostrae ditionis urbes — Collare, vestis talaris et fascia capitulo cathedralis Anagninae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-30; language `la`; type `indult`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-30-gregory-xvi-acta-volume-02-line-00052386-part-01-ac9fb6cb-la/1839-08-30-gregory-xvi-acta-volume-02-line-00052386-part-01-ac9fb6cb-la.pdf`
- PDF SHA-256: `0d7d6a54e549408c6d9d78b1641c0fb3075d468210d4a928154d611b7eae88d4`; pages: 1
- Page 1 PNG `1e8b6b5271ac0a3394c4f7b0dd4f8cf1b54d55312899a456629dbd62cd4939ae` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-08-30, Latin match. Two columns flow normally to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono,' then notes. Literal OCR noise ('VII]', 'lV') only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052386.part-02` — PASS

- Title: Romano quidem decet Pontifici — Immutatio piae institutionis canonici Tarquini pro ruricolis Verulanis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-08-31; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-08-31-gregory-xvi-acta-volume-02-line-00052386-part-02-8d326a80-la/1839-08-31-gregory-xvi-acta-volume-02-line-00052386-part-02-8d326a80-la.pdf`
- PDF SHA-256: `f1718b062a86d42d7bcf809f8aab882acbdb1ae7fb1587fe2f4eacd5b119a97d`; pages: 2
- Page 1 PNG `f432513ac86a4b3e90b53c14066b398a7a83063a7882b86cebcbe271236a7046` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-08-31, Latin match. Dense two-column body flows normally. Literal OCR line-fragment breaks only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `e3494c64825edbcc8ce46b415cd851ecc1a85714f67724c71be3d3419b2559ca` — PASS: Page 2 of 2. Column 1 completes the decree, non obstantibus and dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono,' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052658.part-01` — PASS

- Title: Ex pastoralis ministerii munere — Provincia Chang-tong a dioecesi Pekinensi separata et in vicariatum apostolicum erecta
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-09-03; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-09-03-gregory-xvi-acta-volume-02-line-00052658-part-01-7e35661d-la/1839-09-03-gregory-xvi-acta-volume-02-line-00052658-part-01-7e35661d-la.pdf`
- PDF SHA-256: `f3c3831c46f0a07e3d637acaf1e76d3948afc8cc9761971a63875a084ff68b93`; pages: 1
- Page 1 PNG `49d9f9c4d8c52a404a1ae17f547d897fa39516aac2a23bb0565cc7aab26e8341` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-09-03, Latin match. Two columns flow normally to dating clause 'Datum Romae ... tertia septembris ... anno octavo.' then notes. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.; Page 1: Limitation, not a defect: the printed dating clause reads 'pontificatus Nostri anno octavo' while the metadata date is 1839-09-03 (the ninth pontifical year for other acts of this date range); recorded literally, no date inferred or repaired.

### `gregory-xvi-acta.volume-02.line-00052860` — PASS

- Title: Exponendum Nobis curasti — Facultas erigendi sodalitatem Scapularis et stationes Viae Crucis in dioecesi Iuliae Caesareae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-09-06; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-09-06-gregory-xvi-acta-volume-02-line-00052860-a73cc842-la/1839-09-06-gregory-xvi-acta-volume-02-line-00052860-a73cc842-la.pdf`
- PDF SHA-256: `c34920c68dc0b9743bb5457b451c2977f1540ad58239da6afca1496e9de202aa`; pages: 1
- Page 1 PNG `83dba2f5cac9bb9bce4ceb8485c654784e301175d08956197529750a7f773508` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-09-06, Latin match. Address, protocol, salutation, body, non obstantibus and dating clause 'Datum Romae ... anno nono.' in column 1 followed by notes; column 2 empty. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00052937` — PASS

- Title: Honorum insignia iis profecto ecclesiasticis viris — Rocchetum et mantellone priori sodalitatis B. M. V. de Monte Carmelo oppidi Scanno
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-09-13; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-09-13-gregory-xvi-acta-volume-02-line-00052937-4a35ffa5-la/1839-09-13-gregory-xvi-acta-volume-02-line-00052937-4a35ffa5-la.pdf`
- PDF SHA-256: `f21043f6f165ce77c4084a022b07bc33c36ecca6cc81853fa850dc59de163689`; pages: 1
- Page 1 PNG `5ba0ef94cbca1d8643b8a14b0c49da5b8c89309cf283070835f6faac84cbde1e` — PASS: Title (three lines), issuer GREGORIUS PP. XVI., 1839-09-13, Latin match. Two columns flow normally to dating clause 'Datum Romae ... anno nono.' then notes. Literal OCR stray dash in the year only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00054029` — PASS

- Title: Ex pastoralis ministerii munere — Vicariatus apostolicus missionum Germaniae septemtrionalis et Daniae ab episcopo Paderbonensi distractus
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-09-17; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-09-17-gregory-xvi-acta-volume-02-line-00054029-b30e8061-la/1839-09-17-gregory-xvi-acta-volume-02-line-00054029-b30e8061-la.pdf`
- PDF SHA-256: `d1ddb55dd82d9f55742233c3241c49f1e331d6a96aaee132ee96365f7928ce9c`; pages: 1
- Page 1 PNG `09769e479201a6ba3dc58b95a387cb87c2be7a8f664492f498670b3989171044` — PASS: Title (three lines), issuer GREGORIUS PP. XVI., 1839-09-17, Latin match. Protocol, body, 'Decernentes ... firmas etc.' and dating clause 'Datum Romae ... anno nono.' in column 1, then notes. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking layout note: the Source note begins at the foot of column 1 and continues at the top of column 2.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00055948` — PASS

- Title: Multa quidem gravia et acerba — Allocutio de Ruthenorum defectione in Lithuania et Alba Russia
- Issuer line: `ACTA GREGORIT PP. XVI.`; date 1839-11-22; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-11-22-gregory-xvi-acta-volume-02-line-00055948-834c6f13-la/1839-11-22-gregory-xvi-acta-volume-02-line-00055948-834c6f13-la.pdf`
- PDF SHA-256: `c18238d8fef2a0f21550245dcbda39e2d720766039069debe48596b7012852d0`; pages: 2
- Page 1 PNG `e75b5044de5ded714d1b78d285d462fb3ef60a4cc5c62110f8460c880a9e3daf` — PASS: Page 1 of 2. Title, 1839-11-22, Latin match. Dense two-column allocution body flows normally; stray OCR bars ('|') inside lines are OCR noise, not running heads or fused summaries. No clipping, overlap, tofu or signature.
- Page 2 PNG `24811a78c352ac2e57d3bcbeee415523411468e72575640123a52d44d0780857` — PASS: Page 2 of 2. Body continues through both columns to the allocution's natural close '... clementissime largiatur.' then notes in column 2. Literal OCR fragment breaks only. Genuine source-bearing final page. No blocking defects.
- Findings: Page 1: Non-blocking qualification: issuer line 'ACTA GREGORIT PP. XVI.' is the OCR-damaged volume running title (GREGORII read as GREGORIT), matching frozen metadata and still identifying the pope (standing coordinator rulings).; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00056217.part-01` — PASS

- Title: In Apostolicae Sedis fastigio collocati — Ecclesia Deiparae Virginis in Monte Carmelo in basilicam minorem erecta
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-11-26; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-11-26-gregory-xvi-acta-volume-02-line-00056217-part-01-89f2bb34-la/1839-11-26-gregory-xvi-acta-volume-02-line-00056217-part-01-89f2bb34-la.pdf`
- PDF SHA-256: `fa2482378b9bea5a08ed5897978c33a4a5655b200a52234b0c2dfb8a0cf2bb4a`; pages: 1
- Page 1 PNG `f9a66f9fa8f7c722c93d02dfdc80bc5739c692290ddc3152e86824b9aef48859` — PASS: Title, issuer GREGORIUS PP. XVI., 1839-11-26, Latin match. Two columns flow normally to dating clause 'Datum Romae apud sanctam Mariam Maiorem ... anno nono.' then notes. Literal OCR noise ('©', '°') only. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00056217.part-03` — PASS

- Title: Dolorem, quo iamdiu afficimur — Antonio Ignatio archiepiscopo Friburgensi de clericis novatoribus et matrimoniis mixtis
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-11-30; language `la`; type `papal-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-11-30-gregory-xvi-acta-volume-02-line-00056217-part-03-9ae5f55e-la/1839-11-30-gregory-xvi-acta-volume-02-line-00056217-part-03-9ae5f55e-la.pdf`
- PDF SHA-256: `bd9e60c8c47add72dfefefacff664dab6660e84f623eaed7e55d239a80627d39`; pages: 2
- Page 1 PNG `d9369617523d56f5c6aac934e28c85148f61b36930db4c10a871906c69bdd61a` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-11-30, Latin match. Address, 'Friburgum in Brisgovia GREGORIUS PP. XVI.', salutation and dense two-column body flow normally. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `d572811b444c5c09376cb69cc7e0c47f107054ab6185c474ff72c92a12c1b548` — PASS: Page 2 of 2. Body continues through both columns to the benediction and dating clause 'Datum Romae apud s. Mariam Maiorem ... anno nono.', then the edition note and project notes. Genuine source-bearing final page. No blocking defects.
- Findings: Page 2: Non-blocking qualification: the edition's textual note '1 Videtur aliquid deesse: forsan verbum initа. (N. E.)' is separately set after the dating clause and disclosed in the Source note as retained; it is a historical edition note, not project furniture.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00056763.part-01` — PASS

- Title: In supremo apostolatus fastigio — Reprobatio commercii Nigritarum
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-12-03; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-12-03-gregory-xvi-acta-volume-02-line-00056763-part-01-91f8f500-la/1839-12-03-gregory-xvi-acta-volume-02-line-00056763-part-01-91f8f500-la.pdf`
- PDF SHA-256: `c9b828869e171f6e0fc2629f28481ec2a9c45698f354876ce345bf1d84cdd927`; pages: 2
- Page 1 PNG `8da66c3720a8d8029f566369dc020ccf5a3712c133bbe9e61598eafd846ea5cd` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-12-03, Latin match. Protocol 'ad futuram rei memoriam' and dense two-column body flow normally. No clipping, overlap, tofu, provider signature, running head or fused marginal summary.
- Page 2 PNG `f947f98661951b5e5088339c15bc70f193df1a73eef0224ee6c3fdccd5ebd4d2` — PASS: Page 2 of 2. Column 1 completes the body, the publication clause and dating clause 'Datum Romae ... tertia decembris ... anno nono.' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: Page 1: Non-blocking qualification: the letter's own citation notes (2, 3, 4, 5 [OCR '>'], 6) are set as separate paragraphs at the foot of column 2 in source page order, between '... Pius VII, eodem quo sui decessores' and the continuation 'religionis et charitatis spiritu inductus' at the top of page 2. They are separately set historical notes (disclosed as retained in the Source note), not fused into a body line, so not blocking; recorded because a body sentence spans them.; Page 1: Literal OCR note-marker damage ('+', '>', '°', '}') is a limitation, not a layout defect.; Page 2: Non-blocking layout note: the Source note begins at the foot of column 1 and continues at the top of column 2.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00056763.part-02` — PASS

- Title: Gravissimas inter curas — Prioratus ordinis ss. Mauritii et Lazari in oppido Torre Luserna et unio paroeciae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-12-03; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-12-03-gregory-xvi-acta-volume-02-line-00056763-part-02-4592092d-la/1839-12-03-gregory-xvi-acta-volume-02-line-00056763-part-02-4592092d-la.pdf`
- PDF SHA-256: `cd1051566786910d2950e359a779142ef24ef2a0cec919084733710399f2b184`; pages: 2
- Page 1 PNG `8219b017ee321236b744b097aed3d18801a19fde5de1c3322413cbc3acc6246a` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-12-03, Latin match. Dense two-column body flows normally. Literal OCR noise only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `827213083c50055be331f4b3bde3eaac4be5a7e62d40cd81692ac34ecb4afdc4` — PASS: Page 2 of 2. Column 1 completes the decree, non obstantibus and dating clause 'Datum Romae apud s. Mariam Maiorem ... tertia decembris ... anno nono.' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00056763.part-03` — PASS

- Title: Apostolatus officium — Facultas eligendi coadiutorem vicarii apostolici Cochinchinae
- Issuer line: `GREGORIUS PP. XVI.`; date 1839-12-10; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-12-10-gregory-xvi-acta-volume-02-line-00056763-part-03-d353a65e-la/1839-12-10-gregory-xvi-acta-volume-02-line-00056763-part-03-d353a65e-la.pdf`
- PDF SHA-256: `e8fc8b7e451d174fa99560ad1889ddd2a1f086eed9781df2ff3c077e7fd50603`; pages: 2
- Page 1 PNG `aedd113d3bc04326fed9144bd59181bbde680571e2a9acbef6f97e35c7382eae` — PASS: Page 1 of 2. Title, issuer GREGORIUS PP. XVI., 1839-12-10, Latin match. Two-column body flows normally to the start of the dating clause at the foot of column 2 ('... pontificatus Nostri'), continuing on page 2. Literal OCR noise ('€O', 's2u', stray bar) only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `99e8cff86e8f70c07c2430004ac910583e8ab3f7f3326ed6d77d2fd8611267e3` — PASS: Page 2 of 2. Column 1 holds 'anno nono.' completing 'Datum Romae ... pontificatus Nostri' from page 1, then notes; rest blank. No blocking defects.
- Findings: Page 2: Non-blocking qualification: sparse final page carrying only the last words of the genuine dating clause ('anno nono.') and the notes. The dating-clause tail is source-bearing, so this is not a notices-only page; recorded as a sparse-final-page qualification.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00057300` — PASS

- Title: Apostolatus officium — Facultas eligendi coadiutorem vicarii apostolici Tunquini Occidentalis
- Issuer line: `-GREGORIUS PP. XVI.`; date 1839-12-10; language `la`; type `apostolic-letter`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-12-10-gregory-xvi-acta-volume-02-line-00057300-9725b184-la/1839-12-10-gregory-xvi-acta-volume-02-line-00057300-9725b184-la.pdf`
- PDF SHA-256: `b441336e05abc946f206d6e90af5cf0dc83c94190fcaee32b7b310ae3c93d248`; pages: 2
- Page 1 PNG `f16c4a5ca4061046bac6edfbb3572a3e9b533ecfa60941ad9b0e99004354021a` — PASS: Page 1 of 2. Title, 1839-12-10, Latin match. Two-column body flows normally to '... inviolabiliter observarie'. Literal OCR noise ('~', stray 'i') only. No clipping, overlap, tofu, signature, running head or fused summary.
- Page 2 PNG `ad2adf7c8a11b9495222e99ed113802dcb8b539de145d65d2e0181beab5d5fae` — PASS: Page 2 of 2. Column 1 holds the non obstantibus clause and dating clause 'Datum Romae apud sanctam Mariam Maiorem ... decima decembris ... anno nono.' followed by notes. Genuine source-bearing final page. No blocking defects.
- Findings: Page 1: Non-blocking qualification: issuer line '-GREGORIUS PP. XVI.' (title line and protocol) carries a stray OCR leading dash; it matches the frozen metadata and still identifies the pope (standing coordinator ruling).; Page 1: Non-blocking layout note: column 2 ends about two-thirds down page 1 and the non obstantibus paragraph begins page 2; no text lost or reordered.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

### `gregory-xvi-acta.volume-02.line-00057446.part-01` — PASS

- Title: Gravissimas inter aerumnas — Allocutio de creatione cardinalis Hugonis Roberti de la Tour d’Auvergne Lauraguais
- Issuer line: `g2 ACTA GREGORII PP. XVI.`; date 1839-12-22; language `la`; type `consistorial-allocution`
- PDF: `.scratch/typeset_pipeline/claude/gregory-0005/1839-12-22-gregory-xvi-acta-volume-02-line-00057446-part-01-c96ee9a6-la/1839-12-22-gregory-xvi-acta-volume-02-line-00057446-part-01-c96ee9a6-la.pdf`
- PDF SHA-256: `ed1a2d2e3dd8ef0c08b5d4fc9fd1c1eae35e7cb9303ee2bb24cbe80bd6422f8e`; pages: 1
- Page 1 PNG `3840222740d689698ce5e32027f0365a099f3bc3a7173d24278f05aafba440d3` — PASS: Title, 1839-12-22, Latin match. Allocution body flows from column 1 into column 2 through 'Quid vobis videtur?', the creation formula, the in-pectore reservation and 'In nomine Patris ... Amen.' (literal OCR of cross glyphs), then the historical note and project notes. No clipping, overlap, tofu, signature, running head or fused summary.
- Findings: Page 1: Non-blocking qualification: issuer line 'g2 ACTA GREGORII PP. XVI.' is the volume running title with a stray OCR mark, matching frozen metadata (standing coordinator ruling for Acta allocutions).; Page 1: Non-blocking qualification: the edition's historical note on the reserved cardinals ('? Ex his unus est loANNES Marta Mastat-FERRETTI; ... Pii IX nomen suscipiens.') is separately set after the closing formula and disclosed as retained in the Source note.; No prior_finding was assigned for this document.
- Limitations: Literal, uncorrected, uncollated historical OCR; word divisions, spellings, punctuation and isolated glyph noise were not judged or repaired.; Layout review only; no word-level collation, historical authentication, publication or installation claim.

## Limitations

These readers are literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. This review covers layout and identification only: no word-level collation, no judgment or repair of wording, no historical authentication, and no publication, installation or deployment claim. The `-ocr` source text cannot establish the original printing's glyphs or pagination. Dates are taken from the frozen metadata and were not reconstructed.
