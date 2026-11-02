# Independent source intake: Pascendi historical English witness

**Source verdict: eligible only as a disclosed damaged partial historical witness.** This decision applies to the exact newly recovered mechanical OCR artifact below. It does not establish complete English coverage, a corrected edition, whole-word image collation, or translation accuracy. Reader-PDF visual judgment is **NOT ASSIGNED** to this role: no reader pages were individually inspected here and no whole-PDF acceptance is claimed.

The separate source role follows the explicitly authorized 24-page exception in `long-pdf-52-protocol.json`. Packet `52.json` SHA-256 is `72681fe09eefcf8b24c8f08f528f515daf1f052a9aada06b97015dafe6061217`; protocol SHA-256 is `46d50e848afb908f9507ff30b68d382001f3a33a1d0294a87ba20a7c35bd7b5a`. Producer acceptance was not inherited.

## Exact reviewed objects

| Object | SHA-256 / extent |
| --- | --- |
| Selected English text | `319308afc17b723c6a47fd2d9cbd1a7e29f0222d85cfc0503c19d2adbfd4f144`; 128,350 bytes; physical LF lines 1–283 |
| Segment controller | `48475ef491c2257e87ed32ade29489ee58a0e98b95568897b7f79a8910be05bc` |
| Retained 26-page native witness | `bb2ea470a77ebe0b686f176e1873f4a2ec440a436451d03f31440fb236984620`; 4,183,461 bytes |
| Restricted whole Boston parent | `d2effe6086361d8f0f05970af1a789e27f34101ec9a1c6aac524bb8055eadf22`; 23,152,624 bytes; 200 PDF pages |
| OCR replay ZIP | `eeb957f8653327f43959be56cffbd891146f1eaea1f8dd7f5d87a39e5dafdd05` |
| Reader PDF, mechanically checked only | `06b622ef09fc4a907d3449bc089aff4ab8d5795ea90056bb901e6642a3f17fa3`; 158,499 bytes; 24 pages |
| Frozen manifest | `023162c76c565c90125cf437c20bca56c427d65404278cee3302cf932dad49dc` |
| Reader receipt | `97f7284878b54d68fa13cf20f7d4ef6785e24e7808d4d752ab36e4bab4051d40` |

The text is container-owned at `src/sources/works/journals/american-catholic-quarterly-review/editions/1907-volume-32/artifacts/boston-pascendi-english-319308afc17b/text.txt`. Its constituent controller is the `boston-fresh-ocr-319308afc17b` segment under the Pascendi work’s `1907-acqr-volume-32-english` edition. Full frozen-row equality, canonical source bytes, controller, artifact records, helper pins, receipt, metadata, and every listed reader/native raster pin were independently checked: 145 checks passed.

## Identity, extent, and rights

The physical issue leaf, parent PDF page 3, directly prints **The American Catholic Quarterly Review, volume XXXII, October 1907, no. 128**, and registration in 1907 by P. J. Ryan. My independent 120-dpi rendering of that parent page exactly matches the viewed issue image: SHA-256 `fb746c4148a0d2ada1c81e15e491fdde5342fdf0758ca5cf8752f6275b170f80`. This establishes the issue date independently of the act’s subscription.

The complete pinned Internet Archive metadata identifies `americancatholic32unse_2`, contributor **Boston College**, the same issue title, publication date 1907, and Philadelphia publisher Hardy and Mahony. Its generic `date` value 1876 is contradicted by its specific issue title, publication field, and physical dated leaf; it is not used to date this issue. The parent’s complete size and SHA-1 match the metadata file record. The primary object is the [Boston College issue](https://archive.org/details/americancatholic32unse_2), distinct from the Toronto annual and SIM microfilm; neither alternate copy supplied words or images to this intake.

Native page 705 starts the historical English text under **The Doctrines of the Modernists**, with the full episcopal address, Pius X attribution, salutation, and opening. Native page 730 contains the final benediction, Rome/8 September 1907 dating clause, and Pius X subscription. These anchors, the continuous historical text and three-part/seven-remedy structure identify this as the historical English Pascendi expression. The translator is unrecorded; no named translator or official modern-translation authority is inferred.

Independent native parity checks establish that retained pages 1–26 equal complete parent PDF pages **131–156**, in order, by page geometry, extracted text, and native-image hashes. The two contact sheets cover all printed folios **705–730**. Direct native views checked printed 705, 706, 723, 725, 726, 727, 728, 729, and 730. Part I begins on 706, Part II on 723, Part III on 725; remedies I–VII and their substantial body text continue through 729, followed by the closing on 730. No adjacent constituent or modern wrapper was seen within the selected bounds. This is an extent finding, not a word-for-word completeness certification.

The identified English printing and faithful native-page reproduction have an affirmative **United States** public-domain basis. The issue’s own 1907 publication evidence controls this assessment. The Copyright Office’s current [Circular 15A, page 2](https://www.copyright.gov/circs/circ15a.pdf), checked 2026-10-30, states the pre-1931 United States publication cutoff. This application is consistent with `papal-documents-rights-v1.toml`; it makes no worldwide claim. Modern library/digitization wrappers remain excluded. The full parent remains restricted and was read in place, with no duplicate whole PDF or shared-cache modification. Historical English is excluded from the project’s CC BY 4.0 grant.

## Physical damage and OCR limits

The native full page and a JPEG95 crop independently show that printed **705 physically repeats/substitutes a substantive church/reformers line**, immediately followed by the broken continuation into “is most sacred”. This is a printing defect. The source preserves the damaged sequence; absent words were never typed, inferred, translated, or imported from another witness. This defect blocks every complete-English or complete-act claim, while permitting this explicitly labeled damaged partial witness.

The cleaner Boston pages 726/728 are physically readable at the late loci affected by severe earlier OCR corruption. The new local OCR removes that severe machine failure without introducing model-authored corrections. Ordinary OCR defects remain. For example, the native Part II and Part III headings are mechanically recognized at source LF201/221 as `PART I.` and `PART Il. REMEDIES.`; their substantial sections are present. Spelling, punctuation, line-end hyphen fragments, and other uncollated words remain. No whole-source lexical or translation certification is offered.

## Independent replay

The exact retained `replay.py` and entire recipe were read before execution. Implementation SHA-256 is `b8fa5da8f914d4dbb5ea54c281bc4074c42a9445828cf0dfd0ae3ce01c1bea85`; recipe is `fc4ebe969204635b30afec0ac147bb155c107edcafd190b6a884234f64466319`. All 66 declared raw/model/license/implementation members and the complete 67-member ZIP set match. Replay software carries the retained MIT grant; the unmodified Tesseract `tessdata_fast` 4.1.0 English model carries Apache-2.0. Independent full upstream model/license retrieval hashes also match: model `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`, license `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

Raw-TXT assembly and a second independently implemented selection reproduced all 128,350 source bytes. Full replay from the retained native PDF verified all 26 full 300-dpi grayscale rasters, body crops, raw TXT/TSV pairs, five special crop images and OCR streams, and the final selected text. The special opening drop-cap uses all-uppercase recognition rather than a supplied expected letter; the p.729 line/final-word crops are visibly source-supported. Native-parent parity was independently replayed through the existing MIT helper, with outputs solely in this role’s scratch area.

Current uncached `source-library validate` returned exit 0: artifact=11108, corpus=5, edition=14304, passage=9532, segment=10882, work=10944, bindings=4398. Every Python import/CLI used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`. The independent current `validate_document`/`pdf_body_fidelity` replay passed over 24 pages, 127,960 source characters, 105,911 normalized characters and 200 permitted layout hyphens. Four reader fonts are embedded; PDF title/English subject/Pius X author and tracked-revision dates match. These mechanical checks grant no visual reader-PDF acceptance.

## Actual visual evidence

Each image below was displayed alone using `tools.view_image` with `detail: original`, followed by `image` with automatic detail and the returned MIME. Findings were persisted immediately in `observations.jsonl`. The two JPEG95 crops have exact source-raster hashes and xywh geometry in `crop-geometry.json`; source/cache rasters were unchanged.

| Actually viewed extent | Image SHA-256 |
| --- | --- |
| native witness pages 1–20, printed 705–724 contact overview | `c6221aed0c43266fdccec96ad281b6caf84a7f8af0eb19948defc0325a6cecef` |
| native witness pages 21–26, printed 725–730 contact overview | `8eaa1c715df8224d1ef206fe5a3496dc9448821eae0fa2cea0e728b58eadc3ec` |
| physical dated issue opening leaf | `fb746c4148a0d2ada1c81e15e491fdde5342fdf0758ca5cf8752f6275b170f80` |
| native full page1 printed705 | `ab0c8bff7afea927bc0a3c7e0d44fb10b0a20f5f66322532cbd797f9c92a31df` |
| additional historical page printed578 | `f5d86779155c552c7ca6eeac24882a7b04af708446e7239ef9b286923e027d77` |
| native full page26 printed730 | `29fcb0b4134d1abacfb94a414f10d09f68473af2657516ef25962ede244e9c06` |
| native full page25 printed729 | `358c7abf43a6dc68693b56d9f4f61758b10873ac8c53b81da2719f9b64dc0106` |
| native full page22 printed726 | `403595d8fb3eab70e028971c414c55484e56806915e35d03bee12b8edc41737f` |
| native full page24 printed728 | `94e5b7ba859a4a5916a1a768d8192d918e7da1abb75c80a93849696fbe10c202` |
| native full page23 printed727 | `4b51c2aa8e1edb611313eaa5642385d4fa4598535407917ef066806e2dac0f36` |
| native full page21 printed725 | `ac4bee2265888d95ab4b3b0023788dd41b17d00baec0c4fbee94f2ee4535b9dc` |
| native full page19 printed723 | `136827eb1220ec916aba9fb8c617a78277a1d67d14e80239ee01665ed02c5dcf` |
| native full page2 printed706 | `7e7378fe7b60ea76a1158c58b7366a89a85ed8951a858649afad0c63d7999092` |
| printed705 Gravity of the Situation paragraph | `920f9e0226bb6507e2069ec517cbac9a46d5c959719250998c1fb14957a2373c` |
| printed729 VII final remedy | `2ff7db8b528704396fa6cd6353323589e4ff332948c6ac13852627072ff19cad` |

The extra image named `unse-issue-opening.png` actually shows printed 578; it was recorded as context only and supplies no issue-date proof. Contact overview is not full-resolution lexical collation. There were no reader-PDF image views and no reuse of prior visual acceptance.

No blocker remains for this narrowly bounded source-intake eligibility. Complete English coverage remains blocked by the actual printing defect. Reader visual acceptance, supersession of earlier consumer pins, installation, and deployment remain separate coordinator decisions.
