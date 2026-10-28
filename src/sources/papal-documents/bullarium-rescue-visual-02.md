# Bullarium rescue visual review — batch 02

Layout review completed 2026-10-26: **32 documents, 69 of 69 pages individually inspected; 32 PASS, 0 CHANGES_REQUIRED, 0 excluded.** Every assigned page was opened through `view_image` at original full-page resolution. No prior page reviews were reused.

All measured PDF SHA-256 values and `pdfinfo` page counts matched the assignments before and after inspection. Every assigned raster remained hash-identical through final verification. The actual-view ledger was saved after each document, with intermediate checkpoints for the nine-page document.

No clipping, column overlap, apparent introduced missing text or glyphs, unreadable title/body boundary, unreadable source/rights apparatus, conspicuously flattened table, modern digitizer banner, or terminal furniture-only page was observed. Retained OCR damage, black squares, garbled words, marginal fragments and historical running furniture remain source-quality qualifications. The black squares were confirmed as literal characters in the generated body TeX.

This PASS records visual layout only. It does not establish source collation, authentication, completeness beyond declared witness bounds, doctrinal or juridical verification, or publication approval. No source, PDF, or raster was edited or regenerated.

## Source gate

The assignment pins withdrawal SHA-256 `a3e66221ed8afbd73c6cfab3e41d7d2be8ef7dce597a1bf2d41773b8a1faacbc`. The current gate measured `aa7bf4c374674f5b53846a203f76812bb4e07fdfe8a3cf924d21918146125c79` (revision `2026-10-26T16:11:07Z`) before every document and at final verification, unchanged during review. The dispatch hash difference was reported to the coordinator. No assigned document ID appeared among current affected-unit IDs or supersession prior IDs. Each exact `(id, language, pdf_sha256)` tuple was compared against `supersessions[].prior`, `affected_units[].withdrawn_documents[]`, and direct withdrawal documents before inspection and at the final check; no tuple matched. The global gate hash change therefore blocks no assigned PDF in this batch.

The gate checks, before/after measurements, raster hashes, literal-square checks and actual-view ledger are retained in `.scratch/bullarium_visual_review/rescue/batch-02/review/`.

## Receipt namespaces

Each row preserves its assigned frozen receipt namespace.

| Reference | Assigned receipt SHA-256 |
| --- | --- |
| A | `b8256dabaaeed467420920684323695182b61247530edbff7b9e1371ae92fc71` |
| B | `7db0034ada22d4dac66a12e91490a960e026d79540857026067ab0a72325b5eb` |

## Exact coverage

| Document ID | Receipt | PDF SHA-256, before = after | All individually inspected pages | Disposition |
| --- | --- | --- | --- | --- |
| `bullarium.volume-02.unit-0090` | A | `e02f0c438b6b8c7c31f3f8ad7b57edf1635ef28a80c7e4beaa40b291a664ae40` | 1, 2 | PASS |
| `bullarium.volume-02.unit-0356` | A | `59adf54b36ac4a68407bd51d033b7b9247ed8155c344b1133919cda108459672` | 1, 2 | PASS |
| `bullarium.volume-03.unit-0139` | A | `79f26861bac35f7a236c9247ea125758710d06298346baab245adc731fa52080` | 1 | PASS |
| `bullarium.volume-04.unit-0120` | A | `7f2b6c2645aacb8d6a93368b4d460a73222dc3361f33f6aea407a3478e8e030a` | 1, 2, 3 | PASS |
| `bullarium.volume-04.unit-0126` | A | `048eec3c2417aca4907060736f4271b70762c6b7e0735e7dd3621a64d6da18fd` | 1 | PASS |
| `bullarium.volume-04.unit-0173.fragment` | B | `94be7a720093e800486b4b6952f33c81e2533359bf57c0717b90bb78a0271090` | 1, 2 | PASS |
| `bullarium.volume-05.unit-0061` | A | `bf9ff2b4f7a4bd91328b8feb8379825c5abe5fa29312176f4b2f552b97d6971c` | 1 | PASS |
| `bullarium.volume-07.unit-0080` | A | `b2c171d7b7601d7342365e401a7c9c9fa15120d992ffe3b05acd1c04f79f5e83` | 1, 2 | PASS |
| `bullarium.volume-09.unit-0168` | A | `259cbb2f50f443b2d21d762704bee7df2983db0b7936dbf885221c1e90490536` | 1, 2 | PASS |
| `bullarium.volume-10.unit-0015` | A | `ee8f37a6a7dade82b27e43e6cbffff979217e0eaaeda64e6a3196fa976f30b94` | 1, 2, 3 | PASS |
| `bullarium.volume-10.unit-0033` | A | `559c3f61c94ea194b079301dfe798ba977228cf2ab3753bcded71aea9f4a1197` | 1 | PASS |
| `bullarium.volume-11.unit-0102` | A | `94982d8b35d527acd26b073df26a0c171cd96a41bbe7e7382b60cf2c18920001` | 1, 2 | PASS |
| `bullarium.volume-13.unit-0014` | A | `022a0450cca016d389577e067db99b718a50254fe1b5a8958e9fdb71f584b315` | 1 | PASS |
| `bullarium.volume-13.unit-0140` | A | `83316f904d30254c24a5da2d7ab994e8fa711ddf47f5b718cbcc0640d6690d13` | 1, 2 | PASS |
| `bullarium.volume-14.unit-0226` | A | `f09f5d38efc4e08313911f37d0aa6d405fbd897d3dc3da2b005344b101237ef9` | 1, 2 | PASS |
| `bullarium.volume-15.unit-0181` | A | `efe60e4f39a550db3cc4db312dca42567fc5439f7c0d9c473ce00e93b7e9d836` | 1, 2, 3, 4 | PASS |
| `bullarium.volume-15.unit-0193` | A | `b4ce1244be53f68336f40f221e1390c1eb2e65216e1feedc7ba8abb4d7fd0d0b` | 1, 2 | PASS |
| `bullarium.volume-15.unit-0207` | A | `b8fc127eb7f13202737800d207d99b46d42acee63ad81ea79e79f60af1f4a81d` | 1 | PASS |
| `bullarium.volume-16.unit-0031` | A | `1ecc7bb65c887172ba35074a0d38d118bab5373d6680b177b3b275d637a5e4a9` | 1, 2, 3 | PASS |
| `bullarium.volume-16.unit-0155` | A | `b32114d494262f1a2fce88c96b1e94a02477352c4468832d4fad3fe1f6846de5` | 1, 2 | PASS |
| `bullarium.volume-16.unit-0299` | A | `758f05be1de19802518a6bb06f34acb4b291d636cfebeb0b5a901bf265a39031` | 1, 2 | PASS |
| `bullarium.volume-17.unit-0248` | A | `5118730ad71688ce8e14d6fd50c2975e45d59aead1c22264ec7d799bfd41e978` | 1 | PASS |
| `bullarium.volume-17.unit-0258` | A | `ab28f3df93e742767b063154f80d4aedb0cbe9fb0bc6f67711d4f8c3fd1a2cce` | 1, 2 | PASS |
| `bullarium.volume-19.unit-0152` | A | `731b03f3a6de673869e6639f7b8e656774f653a832e4891a638e44100f727c68` | 1, 2 | PASS |
| `bullarium.volume-21.unit-0035` | A | `12bb96c89f099c2aa5659b469c78401bb17e0512669ac97225206182ec3f0049` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0013` | A | `3fb7d817a34959c2ac925e192626626059b642f451a5a42a8efaf28689bb13fa` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0068` | A | `2cfc7aff5ef65bb212cd75857949a6d48ba6e4c40dda8f940441dd26c2aa2c77` | 1, 2, 3 | PASS |
| `bullarium.volume-22.unit-0171` | A | `060a3a772fc7662ab0e598cd71f3516900f27a61e9f8ae7ce7e88b2ea1b75fa6` | 1, 2, 3, 4, 5, 6, 7, 8, 9 | PASS |
| `bullarium.volume-22.unit-0183` | A | `dccb5b12343865bc67714ef2785d786a7b4c00634ff297cd605ff4265dfc8543` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0191` | A | `1b92ade08727c8254271c8715a873ab7a6ff8c74b4e6f1f76497b46cedfa0c3a` | 1 | PASS |
| `bullarium.volume-23.unit-0078` | A | `33b4a273f7d5040e2ac235cc8240a627025f36fb33d1f3fe637ff9ff0f8f411a` | 1, 2 | PASS |
| `bullarium.volume-24.unit-0086` | A | `6681480f6a76e1a9ded59490f747b86f6e77c59c43ba81954f3bcf82ac6b838d` | 1, 2 | PASS |

## Material qualifications

- `bullarium.volume-02.unit-0090`: Page 1 contains conspicuous retained OCR corruption and black squares; layout remains legible without overlap or clipping. The black squares are literal characters in the generated body TeX; they are not introduced missing-glyph replacements.
- `bullarium.volume-02.unit-0356`: Page 1 retains black squares and damaged OCR; historical subscriptions and dating clauses on page 2 are readable. No layout blocker. The black squares are literal characters in the generated body TeX; they are not introduced missing-glyph replacements.
- `bullarium.volume-04.unit-0120`: Page 3 is sparse but retains genuine concluding clauses and historical dating before the readable source/rights apparatus; qualified composition limit. Retained OCR corruption and black squares remain source-quality qualifications. The black squares are literal characters in the generated body TeX; they are not introduced missing-glyph replacements.
- `bullarium.volume-09.unit-0168`: Page 2 is sparse but retains the concluding historical clause and genuine dating before readable source/rights apparatus; qualified composition limit. Page 1 title ends with isolated retained punctuation on a separate centered line; title/body boundary remains clear.
- `bullarium.volume-13.unit-0140`: Page 2 is sparse but retains substantive concluding clauses and historical dating before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-14.unit-0226`: Page 2 is sparse but retains substantive closing clauses and historical dating before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-15.unit-0193`: Page 2 is sparse but retains genuine historical dating and a source note before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-16.unit-0031`: Page 3 is sparse but retains the continuation of the genuine historical dating clause before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-17.unit-0258`: Page 2 is sparse but retains substantive closing clauses, genuine historical dating and a source note before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-22.unit-0171`: Pages 4-6 and 8 retain extensive garbled OCR fragments and black squares, especially page 5; the fragments are visibly separated without clipping or column overlap. Source-quality qualification. The black squares are literal characters in the generated body TeX; they are not introduced missing-glyph replacements.
- `bullarium.volume-22.unit-0183`: Page 2 is sparse but retains genuine historical dating before readable source/rights apparatus; qualified composition limit. The French wording on page 1 is a quoted bibliographic title within the Latin act, not a substantial foreign-language act section.
- `bullarium.volume-23.unit-0078`: Page 2 is sparse but retains substantive closing clauses, genuine historical dating and a cardinal subscription before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-24.unit-0086`: Page 2 is sparse but retains substantive closing clauses and genuine historical dating before readable source/rights apparatus; qualified composition limit.

No unresolved layout blocker was found.
