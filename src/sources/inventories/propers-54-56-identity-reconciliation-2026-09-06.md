# Proper 54–56 source identity reconciliation — 2026-09-06

This is the bounded source-identity migration requested during integration of the GPT Fourteenth, Fifteenth and Sixteenth Sundays after Pentecost. It changes evidence metadata and review pins; it neither revises publication prose nor records a new research sweep, source retrieval, substantive content evaluation, facsimile collation or publication acceptance. The governing rules are [source identity, immutable artifacts and consumer review](../../../guidance/sources.md).

The source inputs are the published 54 commit `4d84f142e32e1ef6a3005633c85a6335ebfaa942`, 55 commit `0aef1d1cd34ef5be6a0d270ce3747d39900d06e1`, and 56 source checkpoint `f310d7369`. Their history is retained through integration. Earlier research briefs remain unchanged and may contain the retired IDs below; this mapping supplies their current interpretation. An old identifier is not evidence that different source bytes were consulted.

## Canonical choices

- Wilson belongs to the already registered 1915 Henry Bradshaw Society printing, not a second edition created by downloading its facsimile in 2026. The same applies to the 1927 English Schuster printing and its uncorrected Internet Archive OCR. Their canonical edition records are unchanged, so existing consumers of other artifacts in those editions acquire no new review obligation from this migration.
- Aquinas’s identical September 2026 cps31 response is retained under the 56 acquisition owner, which also identifies the other newly registered installments. The older July edition and its other responses are outside this collision repair. The combined exact response remains restricted; the retained metadata preserves 54’s restricted assessment and 56’s unresolved-rights assessment, both of which withhold the response. No source payload or newly inferred derivative is introduced.
- Chrysostom’s Latin-title and English-title registrations identify the same Greek work and Gross Alexander/NPNF I.13 New Advent English presentation. The 54 work and edition IDs are canonical. Alternate work titles are combined; Joannes Chrysostomus is recorded as an author/search alias in the description. Composition remains unknown.
- The two September New Advent Augustine records both identify Tweed/NPNF I.8 (1888), with the same 2026-09-05 web-state date; the more explicit 54 edition ID is retained. Fourteen separately hashed responses now represent eight modern-numbered Psalm pages: 34, 40, 47, 84, 86, 92, 95 and 118. Differing delivery bytes remain differing artifacts. The earlier July editions and the separate CCEL delivery used by 56 remain separate.
- Francis de Sales already has the same work ID in both branches. Its actual title aliases remain Introduction to the Devout Life, Philothea and Philothée; François de Sales is preserved as an author/search alias in the description. The French and English editions remain distinct, with their existing translation and access qualifications.

Canonical artifact provenance/notes preserve the original independent acquisition receipts and exact extents. Wilson includes all three 54/55/56 campaigns and their different supplement/introduction and marginal-chant bounds. Historical campaign notes remain labeled as such; the combined holdings do not retroactively expand an earlier inspection.

## Exact old-ID to canonical-ID map

| Former ID | Canonical ID |
| --- | --- |
| `edition.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915-facsimile-web-2026-09-05` | `edition.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915` |
| `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915-facsimile-web-2026-09-05.ia-gregorian-pdf-96fd93c7` | `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7` |
| `edition.ildefonso-schuster.the-sacramentary.english-volume-3-ia-ocr-web-2026-09-05` | `edition.ildefonso-schuster.the-sacramentary.burns-oates-washbourne-english-1927` |
| `artifact.ildefonso-schuster.the-sacramentary.english-volume-3-ia-ocr-web-2026-09-05.ia-volume-3-ocr-4d8c8988` | `artifact.ildefonso-schuster.the-sacramentary.burns-oates-washbourne-english-1927.ia-volume-3-ocr-4d8c8988` |
| `edition.thomas-aquinas.super-psalmos.2026-09-05-latin-corpusthomisticum` | `edition.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05` |
| `artifact.thomas-aquinas.super-psalmos.2026-09-05-latin-corpusthomisticum.cps31-html-e2d50b43` | `artifact.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05.cps31-html-e2d50b43` |
| `work.john-chrysostom.commentary-on-galatians` | `work.john-chrysostom.in-epistulam-ad-galatas-commentarius` |
| `edition.john-chrysostom.commentary-on-galatians.english-alexander-npnf1-13-newadvent` | `edition.john-chrysostom.in-epistulam-ad-galatas-commentarius.2026-09-05-alexander-npnf1-13-newadvent` |
| `edition.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |

The same-ID work collision `work.francis-de-sales.introduction-a-la-vie-devote` needs no identifier migration. The 54 and 55 Wilson artifact IDs also already agree; their two retained filenames are resolved to `source.pdf` under the canonical artifact, and the exact duplicate `gregorian-wilson-1915.pdf` is removed. The old path remains interpretable through that same unchanged artifact ID.

## Exact duplicate-byte evidence

For each retained duplicate pair, both locally held byte streams were read and their SHA-256 and byte counts checked against both manifests before the redundant copy was removed. Aquinas is a restricted/hash-only response: both independent manifests and preserved acquisition receipts agree on digest, size and URL; this reconciliation did not retrieve the withheld bytes again and does not claim a fresh byte-stream comparison for it.

| Canonical artifact | SHA-256 | Bytes | Retained payload or disposition |
| --- | --- | ---: | --- |
| `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7` | `96fd93c73f8c9df47b6911981155b8b02cf2f2183ca6e87baad15128682d8681` | 28655931 | `src/sources/works/catholic-church/sacramentarium-gregorianum-hadrianum/editions/wilson-1915/artifacts/ia-pdf-96fd93c7/source.pdf` |
| `artifact.ildefonso-schuster.the-sacramentary.burns-oates-washbourne-english-1927.ia-volume-3-ocr-4d8c8988` | `4d8c8988b954b4841acc7bbdcd91c55f54efb0de46dc66340bcc7e400a65e419` | 1149699 | `src/sources/works/ildefonso-schuster/the-sacramentary/editions/burns-oates-washbourne-english-1927/artifacts/ia-volume-3-ocr-4d8c8988/schuster-sacramentary-3-1927-ia-ocr.txt` |
| `artifact.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05.cps31-html-e2d50b43` | `e2d50b43f0036d33450b908632ba6d741277edb8ad9381c851eddeb005f90749` | 359759 | Restricted; metadata and original acquisition receipts only |

The Wilson receipt formerly using the 55 filename separately matches the same 28,655,931-byte digest above. Its manifest was compared directly with the 54 and 56 records. The canonical retained Wilson file remains the complete 432-page scan. The Schuster OCR remains the complete 27,628-line, 1,149,699-byte download, with its existing same-edition scan as `derived_from`; no OCR words or normalization changed.

## Distinct responses preserved under corrected ownership

Only the enclosing directory and `edition_id` change in these eight manifests. Their stable IDs, exact hashes, URLs, retrieval dates, sizes, rights, provenance, inspection qualifiers and all other fields remain unchanged. This follows the schema’s separate stable-ID and enclosing-owner rules; an ID need not be respelled to match its new parent.

| Artifact ID, retained unchanged | SHA-256, retained unchanged | Canonical enclosing edition |
| --- | --- | --- |
| `artifact.john-chrysostom.commentary-on-galatians.english-alexander-npnf1-13-newadvent.chapter-6-html-0c6d91cf` | `0c6d91cf356aa88e12f7cbfbffd9124a8a2ddc540ac1c0f03ce0cb184617cf8a` | `edition.john-chrysostom.in-epistulam-ad-galatas-commentarius.2026-09-05-alexander-npnf1-13-newadvent` |
| `artifact.john-chrysostom.commentary-on-galatians.english-alexander-npnf1-13-newadvent.chapter-5-html-2da003ae` | `2da003aec2493c295a2e3760de99e9b4a6c50d094f75aefc8721aaaba686bdc3` | `edition.john-chrysostom.in-epistulam-ad-galatas-commentarius.2026-09-05-alexander-npnf1-13-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-92-html-c37b1ddb` | `c37b1ddb316bac6b23c58cd183ea5c932bca764fb9febcac1f0237c445449c13` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-47-html-9a6255a7` | `9a6255a7c2eb5a939715c278ed3342c9b0ee678c0bc5985e877f4a81178378fe` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-40-html-3fab0826` | `3fab0826d8bc1d340efc83bc94780b7d8a67e82e78e1d0c74481426be69a6670` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-86-html-4f242c3f` | `4f242c3fe1ac52516dcbcbdfad52c5fd00ed5cf31c202a22f18e3887093847d0` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-95-html-e0350e93` | `e0350e9324ba00022beb3855a50e0cbaa26fc56bd7aaab760f5c63847d887bb0` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |
| `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-47-html-8d6a5c65` | `8d6a5c6566f241aa3c0d2fdae96ab28d5ddf1a8c021ea7ffe48dc99c7aa04587` | `edition.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent` |

## Consumer review

Source-library dependency/fingerprint impact was compared before and after the correction. Exactly 20 existing bindings require new review pins: eight in GPT54, nine in GPT55 and three in GPT56. No binding outside those three publications changed. Each affected binding’s actual loci, source role, evidence state, response identity and existing local evidence qualifications were read before repinning. The bindings retain their original loci, states, roles and any verification dates, and append a dated metadata-only review context. The unused duplicate Schuster OCR registration has no directly bound publication; all three guides continue binding the unchanged facsimile for their printed-page evidence.

The following review is of the source identities and already recorded evidence, not a claim to have independently repeated the original passage inspections:

| Publication | Bound source family | Unchanged loci and evidence reviewed |
| --- | --- | --- |
| GPT54 | Augustine/Tweed/New Advent | Latin Ps 83.3–15; 117.4,6; 94.1–4; 33.8–14, second exposition. Compared PAT-001–003, PAT-011 and the referenced precedent records, modern host numbering versus Latin loci, and whole-page receipt bounds. Historical ellipses remain identified. |
| GPT54 | Chrysostom/Alexander | Chapter 5 at Galatians 5:16–24; PAT-007/PRE-007, including immediate neighboring context. Same named translation and response; no Greek-text verification is inferred. |
| GPT54 | Aquinas | Ps 33 nn.8–9, units 87112–87113, PAT-012; the identical cps31 response also carries 56’s separate Psalm 39 locus. |
| GPT54 | Francis de Sales | English III.10 and III.14, PAT-024. Related illumination and bounded English-artifact negative remain distinct from direct Matthew exegesis; no translator name is newly supplied. |
| GPT54 | Wilson | Supplement XXXIII pp.173–174, p.173 notes a–c and introduction xvii–xxii, xxx, xliv–xlv; LIT-003–004. Prayer bodies and separately transmitted marginal chants remain distinct. |
| GPT55 | Augustine/Tweed/New Advent | 39.2–5; 46.2–3; 85.1–6; 91.1–4; 94.5–6,10. The scope’s individual reception findings and receipts distinguish modern host headings, Latin numbering and the quoted versus contextual verses. |
| GPT55 | Chrysostom/Alexander | Chapter 5 lemmata 5:25–26 and chapter 6 lemmata 6:1–10; both original response digests and the bounded reception inspection survive. |
| GPT55 | Wilson | Supplement XXXII–XXXIIII pp.173–174 and introduction xvii–xviii, xxi, xliv–xlv; LIT-008–009. Wilson’s argued supplement attribution is not a newly settled prayer-composer attribution. |
| GPT55 | Liturgical Year continuation | Existing 56 metadata had corrected the artifact’s imprint to 1909 and retained the same full PDF. GPT55’s existing binding already explicitly identified the 1909 second-edition continuation, title page and preface, with printed pp.348,350–351,354–355; its wording agrees with that correction. |
| GPT56 | Aquinas | Ps39 nn.6–7, unit87202, PAT-013. This is distinct from54’s Ps33 unit within the same restricted response. |
| GPT56 | Francis de Sales | French III.5, full chapter and preceding IV ending. The binding continues describing a French-inspected paraphrase and seating-language echo, not a new translated devotional text. |
| GPT56 | Wilson | Printed pp.133–135,173 note c,174 and introduction xvii–xviii,xxx,xli,xliv–xlv. Alternate Collect use, Sunday XVII prayer triad and the distinct marginal chant group remain separate historical claims. |

The incidental stale GPT55 Liturgical Year pin is reviewed against the already corrected source, not repaired by a new source edit in this migration. That retained PDF was independently hashed: `95ba98e2d71e4374c4e5262935c71d5d2479b64b34dd3da290b60209ebd92690`, 11,026,232 bytes. Its existing legacy machine ID still contains `1900`; the source metadata, unchanged research qualification and dated binding review identify the actual 1909 printing and avoid attributing the unnamed continuation writer personally to Guéranger.

## Historical search-receipt limits

GPT55’s PRE-001 and PRE-003 describe a historical 551-file working-tree search at seed `b743814e521622eb8dbea56316e6138d45e8f7f3`, including pre-existing worktree changes. The cited transient inventories and search logs are not independently retained or reverified by this integration; no clean-snapshot reproduction is claimed. The reported absence of a GPT56 leaf applies only to that stated earlier search boundary and says nothing about the current combined tree. The substantive external-source loci and their tracked evidence records remain unchanged. The immutable research brief is preserved; this qualification records its evidentiary limits without reconstructing a missing receipt.

## Reviewed pin transitions

The publication number identifies `src/gpt/liturgy/roman-rite/1962/propers/temporal/<number>-<ordinal>-after-pentecost/research/source-bindings.toml`. Artifact IDs below are the resulting canonical IDs; retired direct targets are mapped above. Every transition carries its own dated review in that binding’s context.

| Publication | Resulting source ID | Prior fingerprint | Reviewed fingerprint |
| --- | --- | --- | --- |
| 54 | `artifact.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent.psalm-84-html-cb27202d` | `sha256:46f908bf2198b537054f072bc9ab0a63ab1b5e04e05f95e9f46d8faadd56cf8f` | `sha256:42a8e6f3912ee0e0f0702744675b344938275ce71b52b8463759970482ebb981` |
| 54 | `artifact.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent.psalm-118-html-b9b8069f` | `sha256:d73f8cc28d2a6dd8803c11cad324e6a2a1fd8f1a9b28177680351e56d9830599` | `sha256:edf0ef7328043e07dfe4e3f3ee5ab1122745234e76afa94b04452881ba37b25d` |
| 54 | `artifact.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent.psalm-95-html-c3e9ddc0` | `sha256:989a76d3ee21c8d0baa99b737c64bf284b32db6c86594dc5e690f84865bf0344` | `sha256:eb2bf8e7db4bca19bbb8ec93677f51eab63e8932c22c0ea326e8771232b3ed08` |
| 54 | `artifact.augustine.enarrationes-in-psalmos.2026-09-05-tweed-npnf1-8-newadvent.psalm-34-html-9c76e7c7` | `sha256:4ccf17026206bcb5b529ab1e651f71e6463ec5cee975f961d706fcf5deeb8cd8` | `sha256:b555851816b34b3da7690523e65ce195308da8b5add0264625266c989399660a` |
| 54 | `artifact.john-chrysostom.in-epistulam-ad-galatas-commentarius.2026-09-05-alexander-npnf1-13-newadvent.galatians-5-html-36c9b32b` | `sha256:9002b05eb7ecfb07f77e7c1e1ef1014668eb73ad48b52ba2f2cdd4a08a35c5df` | `sha256:892ee9c104e3b413d7e55ccedbfcfb2f267a5aedd5f6520425dfcb4f5d1ef86b` |
| 54 | `artifact.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05.cps31-html-e2d50b43` | `sha256:d4014adf8ff3edaaaa1e55e1f0043e611a828535d95750007ef4081a474a2111` | `sha256:11dc9cdea389b800174e01e20c09884009e778b75849f6accb566c6137d81489` |
| 54 | `artifact.francis-de-sales.introduction-a-la-vie-devote.2026-09-05-ccel-english.full-html-d61a5a3d` | `sha256:f1ae211f3184687d7f27effb08ba1adb3f373eb6560ddbf16e102a27a0674ac8` | `sha256:39988cc7727756c4ba6f01f8bcbe3a557dbeb8c39bc440c5fd7f83d4efddfc1c` |
| 54 | `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7` | `sha256:c189ad536b25c7d8f68ca0b40f14d0c0c075ab6d9699d1bd724b3c404abddb61` | `sha256:b6b2f002fa1d0aecd709fb76d2379c4470e563def3d4c752cad2a2d1b1d6ffb0` |
| 55 | `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-40-html-3fab0826` | `sha256:b65e9599bcae985aeb24fe890b8335055adad9619245bfe527dbe3c1049c973c` | `sha256:64ee785d0d9292b394b62845e0865ca0ad6b66af1de5bfc20d1e06c341244452` |
| 55 | `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-47-html-8d6a5c65` | `sha256:3afa4ee8e4f9505f56c5b71a141affc622f91de932874691d86fb7c9aa3da485` | `sha256:3226c2a21deb6bf718f9fe62289ffe6bab85788d5a3346b3e3f59c636b37b741` |
| 55 | `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-86-html-4f242c3f` | `sha256:090d71934cd78a4a20e6d18af25662fa0b2efbd6a0d2d2d33153cabdc0b5dd7d` | `sha256:f7965f8ddf74c8d900bcf636caa4ea96bce275e439092d67a68773b179cae408` |
| 55 | `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-92-html-c37b1ddb` | `sha256:c6ccb15a61bfb36d56e7a88d7d4c9fa8ac285b5d11d423a6501dd083ef811134` | `sha256:5a76062880fc02f3360b68c3520bdf1d76bcc5e5c5ae091095f9e59f0c86139b` |
| 55 | `artifact.augustine.enarrationes-in-psalmos.english-npnf1-8-newadvent.psalm-95-html-e0350e93` | `sha256:93f1146a5acd1635ce70c014f3268337ea8d28545265a7d6ad88c591b308e658` | `sha256:110dc074118a3357ca7390f69079ee9fbe97963ea053a4c1b9aa10c1b1529349` |
| 55 | `artifact.john-chrysostom.commentary-on-galatians.english-alexander-npnf1-13-newadvent.chapter-5-html-2da003ae` | `sha256:30dbee2527919c956e57b2e7722c8803bea90f661b0912f8136e557dcc971c64` | `sha256:469ea59ad627f93c0272e3b8fc59a74da9da4ceb7d1738fc9e7d3042ab992c1a` |
| 55 | `artifact.john-chrysostom.commentary-on-galatians.english-alexander-npnf1-13-newadvent.chapter-6-html-0c6d91cf` | `sha256:f198eeccd5310929c43e135cee36082562037b97e41fe6f6ccb11589c2873482` | `sha256:b2e9bd65aa94276a0cfe0eed983e7268248f5d5158ed18d87db6beb20a9977f7` |
| 55 | `artifact.prosper-gueranger.the-liturgical-year.english-duffy-1900-volume-11.ia-pdf-95ba98e2` | `sha256:0c284a75a9d4ba61141e669e20bac150113946f19b1240b58607e61bec7164ad` | `sha256:41e33739805822d7fa17bd959aee1a9bc45e53b9142ac700e0871842608e5a50` |
| 55 | `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7` | `sha256:15006657d03720381f421ced5c581fc6ab69a336a106175358e252e2d478851d` | `sha256:b6b2f002fa1d0aecd709fb76d2379c4470e563def3d4c752cad2a2d1b1d6ffb0` |
| 56 | `artifact.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05.cps31-html-e2d50b43` | `sha256:65e3345fa7f02600df0265d3d9aaccf1cde1d79d8681c896030714e77162702c` | `sha256:11dc9cdea389b800174e01e20c09884009e778b75849f6accb566c6137d81489` |
| 56 | `artifact.francis-de-sales.introduction-a-la-vie-devote.perisse-freres-french-gutenberg.gutenberg-53540-text-c2d4183f` | `sha256:55c6aaea597ec3e335fd6aded867cdccbfbb302f9e3a97ba99f5697a1d298b62` | `sha256:ee493f29c7284f8a952cf21e1a66a18caee81af7ef5c95b66364099de3e010cc` |
| 56 | `artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7` | `sha256:526b28124af7c546fcb1271db4c26676a08ecf5bde94ee2a97cf2bed6eec8762` | `sha256:b6b2f002fa1d0aecd709fb76d2379c4470e563def3d4c752cad2a2d1b1d6ffb0` |

## Verification and limits

- The source graph validates with `tools/tpt source-library validate`: artifact=2302, corpus=5, edition=808, passage=5127, segment=77, work=600, bindings=2355.
- Duplicate retained bytes are eliminated; no original source payload is rewritten. The eight distinct moved responses keep all fields except their enclosing `edition_id`.
- All 20 repinned bindings preserve their prior loci, roles, states, verification dates and other evidence fields; only the reviewed source target where mapped, fingerprint and dated context change.
- This audit does not declare source-inventory, family-ledger, projected browser catalogue, release bindings, rendered PDFs or public deployment current. Those combined-tree generators and publication gates belong to the integrating coordinator.
