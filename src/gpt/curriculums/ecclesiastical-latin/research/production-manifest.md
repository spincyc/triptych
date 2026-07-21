# Ecclesiastical Latin — Production Manifest

## Record boundary

- **Audit date:** 2026-07-21.
- **Object:** the complete exact installed set of 52 independent
  Ecclesiastical Latin leaves: two course companions, 46 two-session learning
  modules, and four stage-assessment companions.
- **Installed total:** 920 pages and 24,936,030 bytes.
- **Publication state:** corrected working snapshots installed at the user's
  direction; changed-byte distribution remains on hold pending renewed exact-
  snapshot authorization.

The hashes below identify byte-identical files under the mirrored curriculum
build and installed paths. They replace the immediately preceding corrected
installed set of 52 PDFs, 920 pages, and 24,966,965 bytes. The release record
intentionally retains the superseded hashes authorized on 20 July 2026, so
its exact-snapshot check fails closed for every changed curriculum PDF until
renewed authorization is recorded.

## Verification state

All 52 candidates completed the repository build recipe and the complete
source-and-rendered structure audit after the whole-curriculum contents
repair. Chapter numbering now restarts at 1 within each Part, contents entries
show a visibly nested Part--chapter--section hierarchy, unnumbered peer entries
reserve the same title gutter as their numbered peers, and PDF destinations
qualify chapter numbers with the containing Part. The formerly unnumbered
first chapter in EL-II.1's `Core Lesson` is now numbered and participates in
that hierarchy.

The settled automated checks cover generation metadata, Part-scoped chapter
sequences, chapter-scoped section sequences, semantic destination definitions,
contents and bookmark structure, and rendered contents geometry. The rendered
gate checks title and number columns, nested indentation, unnumbered alignment,
multi-page contents, wrapped-title continuation indentation, and rows whose
roman and italic text has different baselines. The complete audit also retains
the existing checks for source selection, worksheet and assessment
identifiers, terminal keys, chapter/first-solution co-location, later-form page
starts, indivisible exercise and assessment items, blank or rule-only pages,
isolated advancement boxes, and sparse form continuations.

The bounded review tool produced an exact-byte raster set of all 920 pages and
55 contact sheets. Review was divided into four nonoverlapping ranges: the two
companions and 12 foundations packets (14 PDFs, 269 pages, 17 sheets), the 14
core-grammar packets (246 pages, 14 sheets), the 12 missal-reading packets and
four stage assessments (16 PDFs, 273 pages, 16 sheets), and the eight advanced
packets (132 pages, eight sheets). Cache hashes across all four ranges matched
the current build. Every rendered page was inspected through those
sheets, with full-resolution checks of contents pages and identified high-risk
pages. The complete exact set showed no clipping, overflow,
blank-or-rule-only pages, or remaining contents-hierarchy defect.

This manifest records a technically and visually verified installed working
set, not a completed universal production review or a changed-byte release
authorization. The source and answer audits record the content-level checking
and remaining evidence limits.

## Exact installed snapshots

Paths are relative to both `build/gpt/curriculums/ecclesiastical-latin/` and
the byte-identical installed mirror at
`doc/gpt/curriculums/ecclesiastical-latin/`.

| Snapshot | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `00-course-guide.pdf` | 37 | 458751 | `f39c5e2e7ca27e13589117ae6811123218be5f6589ca5a63a1ce6acb1b53ae7b` |
| `00-reference-grammar.pdf` | 30 | 565591 | `64141fffcf7ec17a948bf2f99da498e0701a0b89a0464b83e954dfd15b0d8f7e` |
| `01-foundations/01-grammar-bridge.pdf` | 17 | 500115 | `57cc23f41d69f8076d9ff1a881c1c9ee387db0922e03480208669b6fc9fca2a7` |
| `01-foundations/02-case-number-gender-agreement.pdf` | 16 | 495163 | `695867bdea591267f84d81b794e242cb76108f686c9520e83c51cd583020ab77` |
| `01-foundations/03-first-second-declensions.pdf` | 16 | 493966 | `38f073bc83035e7e902ce2feccb8335e5c9eb70a90ae56d16dc5981ddbe5b739` |
| `01-foundations/04-third-declension.pdf` | 16 | 489403 | `71b63f386c5408f1a55163b63454766b3861eee2d68d99ea04d09da3a037e230` |
| `01-foundations/05-fourth-fifth-declensions.pdf` | 16 | 493947 | `794264d6e1e15b697ef3e72edaf54677a917aa94eb5b7c99617a46bb0b9ead0c` |
| `01-foundations/06-adjectives-agreement.pdf` | 17 | 521206 | `7fefcba7f1c9aeef2274a2422c1eb111e85d3e1bae545059f1030bbda32e9ab7` |
| `01-foundations/07-sum-possum.pdf` | 16 | 572868 | `66ee409ee53ebc45329575eef368bced1bb044620358d1dd6295cd31bb74723d` |
| `01-foundations/08-present-active-system.pdf` | 16 | 521052 | `c7a4b4822a3013f9a527f2e19d90ae3d6273ce57edf23cadc287c9a3df05232b` |
| `01-foundations/09-perfect-active-system.pdf` | 16 | 491975 | `06186955e75f24e44c578c4c4e83a882a4e9bb54dee68d8b6d43f36997020ae0` |
| `01-foundations/10-passive-deponents.pdf` | 17 | 540412 | `c2e8658ea29d0a475c53b983076078047dc2cfe8a7be0c09d58aa81f252e58bf` |
| `01-foundations/11-pronouns-prepositions.pdf` | 18 | 562202 | `336b46967748659102831f040e1c555c498cd5e91dc71826bcb7e2c0f5bd9093` |
| `01-foundations/12-repeatable-missal-reading.pdf` | 21 | 474621 | `3ca64fe51ca467759447aff45d92ed5226ba25d6a36d8648ecdd10f322d7de36` |
| `02-core-grammar/13-relative-interrogative-indefinite-pronouns.pdf` | 19 | 490196 | `fa5d9669c8fc277b15d7713d903836ed25bc9a61017590f593b6fc4a92ca8cbe` |
| `02-core-grammar/14-comparison-adverbs-numerals.pdf` | 18 | 463722 | `8b18ce3f9b3a423763b24a15f055a4b4a57d77ab5a818d032250a2b0335f0e7f` |
| `02-core-grammar/15-infinitives-indirect-statement.pdf` | 17 | 462730 | `57f50495c7a79abc967a75e6b2702a4e6fcac1c59d9d4d99570f8278bee981f6` |
| `02-core-grammar/16-participles-ablative-absolute.pdf` | 18 | 468373 | `fc22a09603680218465da4a895ec41adf6d83e186e91b60a5777431247cc5cab` |
| `02-core-grammar/17-subjunctive-morphology-sequence.pdf` | 18 | 466809 | `d39d5449f4f93c3bcfbd0182d95d0f32c7bea77bca14c463adda6233ace26aa8` |
| `02-core-grammar/18-purpose-result-indirect-command.pdf` | 17 | 505477 | `0c022618ab40d5062f0c17cafdbd40f5504fad1ddc3aea521611c27ab4365016` |
| `02-core-grammar/19-substantive-clauses.pdf` | 18 | 467355 | `4629533ec0bf99c9051f6c47179f571303863b553ee54b0f3611e6073249b140` |
| `02-core-grammar/20-temporal-causal-concessive.pdf` | 18 | 542445 | `f0d3a4bfb9fdd15159d98997c21a0c52fc3d0e63460a7290e2488326f8e434ba` |
| `02-core-grammar/21-conditions.pdf` | 17 | 461202 | `7507d3169b3afdd8c656c715a160016ef7fca1f7ed497de7bb7f81cae07ae501` |
| `02-core-grammar/22-relative-characteristic.pdf` | 16 | 463003 | `e0e46b4e6d9fe385b322624776df5697813647ed4f395607137f0199dab0b36f` |
| `02-core-grammar/23-commands-wishes-fearing.pdf` | 17 | 462754 | `9ba23e1f68980cd9b64e4f1dd2247544dd4acc47c32151e47d532ed6700ead0e` |
| `02-core-grammar/24-verbal-nouns-periphrastics.pdf` | 17 | 464106 | `0f0304c2be54de3b2a277b93d63dbd208299943e8f123dbf54cb54fb036ab988` |
| `02-core-grammar/25-adverbial-cases.pdf` | 17 | 483584 | `5ffbd7c2e24b55d8e31ea4fdac599e577c6b78d7e9d674eec6aa604621be2a82` |
| `02-core-grammar/26-liturgical-compression.pdf` | 19 | 472233 | `4a6db315c9bca2006199e5e62b12c558a540f311d81f0f4565e8250ea1b4f36d` |
| `03-missal-reading/27-independent-reader-workflow.pdf` | 18 | 467886 | `1e91d81510dc431a17a46bbe019434c5cabac6c1475cb876cadece87af716a05` |
| `03-missal-reading/28-ordinary-fixed-order.pdf` | 16 | 465550 | `3d929f1ac67b55d3c43751d65ef0b4ede731b6c65f762e00a93e5a94509c3ac6` |
| `03-missal-reading/29-collects.pdf` | 16 | 463342 | `d5edc3b7a797419b9f0c905a9726e53e39b6b394c621e8f709ef6be9606e37c3` |
| `03-missal-reading/30-secrets-postcommunions.pdf` | 16 | 461726 | `9a449e5312fb469adcfe4e68c0e7e3820867ff40929bfad79d23ae079cd2a250` |
| `03-missal-reading/31-lessons-epistles.pdf` | 16 | 463758 | `83ee86df3a28972e2245e0a9eeae999809b97800a5d6a124714dd80a3bea86f9` |
| `03-missal-reading/32-gospels.pdf` | 16 | 463413 | `6b953d70f0b0262e62b1bec20b8eb9b7abfbe487c7b6da64129248b9c583c2a0` |
| `03-missal-reading/33-chants-sequences.pdf` | 16 | 474509 | `4a1224955686d68310467b7a161607eb06b8d793107765d75c7f702a9c2f6857` |
| `03-missal-reading/34-prefaces-roman-canon.pdf` | 17 | 506678 | `0e7d3bd623d9628dc4b8ed96636e692b38fc201fdf6049ba13b46ba98560391b` |
| `03-missal-reading/35-temporal-cycle.pdf` | 17 | 461729 | `be5accbbfbedd64a823af854cb7a2cb126991b52110426e75515ac6e811756a2` |
| `03-missal-reading/36-sanctoral-commons.pdf` | 17 | 463548 | `aed4959adf3c28f56b54c26a7dad92626fb1bc0da052909500c2f00cb4dade25` |
| `03-missal-reading/37-requiem-holy-week.pdf` | 18 | 466361 | `f83ccefd69147646ff4551ee2d686ce6ba0162cfe66326ef5cbd3163bb4f9dc3` |
| `03-missal-reading/38-full-mass-capstone.pdf` | 16 | 445304 | `5fd2442d71d15ab37de2cf2e6a3fd58f858db72955bb2a19fba33bf347c95313` |
| `04-advanced/39-register-across-time.pdf` | 16 | 489106 | `ede7e08c6d4c387ab794423131261e05cae7997f2fddb2ed03c9c78328422b94` |
| `04-advanced/40-vulgate-texture.pdf` | 16 | 460747 | `5d6e5c5f76f9dc480b69f76157e7957ffe7cc65db6dde1cf5bd0cfc4fbc568cf` |
| `04-advanced/41-allusion-context-typology.pdf` | 16 | 484321 | `5cba5b3c19b95ee5c8ecfd46c5462b10f7aeae7111ca63afc1731b32784b8d72` |
| `04-advanced/42-rhetoric-periodic-prose.pdf` | 16 | 458619 | `b7daaa1789d0c54e9e8d4a4e23a31a663ffe2bbc21785a71f2a95efeefb7fba8` |
| `04-advanced/43-textual-comparison-commentary.pdf` | 16 | 440918 | `c40e8bb5861a7c7b96d9776278b1474f60c321c7e4a040a0b9a92fa505bc3041` |
| `04-advanced/44-controlled-imitation.pdf` | 16 | 455899 | `e7d2c41335cb7d6ed017d5517168f585dddf25248b6e011bef7efe4309d7c945` |
| `04-advanced/45-guided-composition.pdf` | 19 | 444125 | `02140a667727b4dc81a98abefa9393dba77d7beb3a8c82ac38ae877967f17fd5` |
| `04-advanced/46-free-composition-research.pdf` | 17 | 442584 | `9b552be00310ffc9271051bf2b9418384f61b4260f66a30837c74c7834ab9b97` |
| `05-stage-assessments/01-foundations.pdf` | 19 | 450194 | `f2ba55f816d8a919fbd2251b8457bee89d38620bf40725d28191b75d9342fc67` |
| `05-stage-assessments/02-core-grammar.pdf` | 19 | 453359 | `621e698d73e757f79306e459f6f361b2d08b2b7c64237511ccc6556eac3b06ec` |
| `05-stage-assessments/03-missal-reading.pdf` | 20 | 456017 | `2fafc83f577ab63a30b5cb2e0cdd4b5c4fee54dbec99529eb4a846e01b70f1dc` |
| `05-stage-assessments/04-advanced.pdf` | 16 | 441076 | `3ad1a473f4f8dfc5a2f071083672969b46567301461f93583cfaa5ec1700652b` |

## Consequential limitations and publication boundary

Page-image collation remains incomplete, the donor tree contains no local
license, and the distribution basis for received liturgical text remains
unresolved. Successful compilation, internal review, and exact hashing do not
alter those facts.

The release record preserves the maintainer's 20 July 2026 exact-snapshot
exception for the earlier installed bytes. It does not establish donor
ownership, an open license, broader permission for liturgical wording,
profile-final status, independent review, or distribution authority for the
corrected snapshots recorded here.

This manifest records the user-directed installation and commit preparation.
It does not authorize changed-byte distribution, integration, push, or
deployment.
