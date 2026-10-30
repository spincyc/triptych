# Independent cold review 30b — Iucunda sane

PASS — 1 PDF, 8 reader pages. No material source-boundary or layout blocker found.

Reviewed identity: `acta.ass.036.ass-036-l020506`, Latin, Pius X, *Iucunda sane* (ASS 36). This is a mechanical historical source reader with disclosed literal OCR limitations.

| Exact input | SHA-256 |
| --- | --- |
| Final PDF | `6be1f18ba97f88316afa1faa3b5d05bf40e065c774d61428f06528e9d91ae5cf` |
| Receipt | `28005d63d94eac18dbb80967f62b74655355b7ae60fd7a82d2fe1645fe399627` |
| Frozen manifest | `0bdf8490c7fbf11c9396a272f49c5d072c04e643fcdc89c437a9129f5c945c66` |
| Selected source payload | `bb189df41a86cf3adb66eb29c7c2fbda9cb777ddea22137615a58a150b8e6261` |
| LF partition spec | `f8303a22123188fa17efe3d073a5dbb88f05efe2b0fca1847ae4180871fcdb44` |
| Separate native page-525 PDF | `f225ca7b07a634b1992212f1791dd34046f482be9b852be75a8860bde291a19c` |

PDF: `.scratch/encyclical-notes-10-late/final-readers-02/undated-acta-ass-036-ass-036-l020506-c88a1cb1-la/undated-acta-ass-036-ass-036-l020506-c88a1cb1-la.pdf`. Actual `pdfinfo` count is 8; file size is 65,893 bytes. The packet, brief, assembly spec, receipt, frozen manifest, selected source, controller, artifact records, payloads, boundary-review record, current helpers, raster runs and cache receipts match their exact pins. All 78 packet/output/cache file checks passed and were repeated before finalization. The assembly producer report/reviews pins and renderer executable/font pins also match. Production records supplied identities and evidence pointers only; their visual coverage was not inherited.

The full source row equals the matching frozen-manifest row. Receipt source/PDF identities agree. Parsed controller and artifact metadata equal the packet values. Pinned `validate_document` passed selected source, controlling artifact, edition and segment checks. Independently running current `tools/source-library` common-record validation on all six pinned artifacts and the selected segment returned zero errors. This validates five schema1 artifacts, a supported schema2 native-parent artifact, and the schema2 segment. The native-parent schema2 declaration is supported explicitly by the current validator, including its page count. Source schema acceptance here remains bounded to these records; whole-library validation is a separate coordinator check.

Each reader/native cache receipt agrees with its page count, PDF hash, exact file list and renderer fingerprint. Renderer fingerprints and cache keys were recomputed. Every listed output and cache raster file matched its size and hash. No rasterizer was rerun and no shared cache was changed.

Both contact sheets were inspected. Reader pages **1, 2, 3, 4, 5, 6, 7 and 8** were each opened individually from the packet's exact `pages/page-N.png` at original resolution with `view_image(detail="original")`, one image per tool call. No pages or visual proofs were reused. Native excerpt page 1, mapped to actual parent page **525**, was also opened individually at original resolution. Per-image paths, hashes and pixel dimensions are recorded in `verification.json`.

| Reader pages | Direct visual finding |
| --- | --- |
| 1 | Title, Pius X/Latin identification, source heading, address, protocol and incipit are legible; two columns follow normal reading order. |
| 2–5 | Readable continuous columns, indented body and distinct historical source-note paragraphs. Notes retained at historical source breaks do not constitute fusion. No clipping, overlap or missing rendered glyphs observed. |
| 6 | Body ends at the foot of the left column with `dévastant (6).` The repaired six-note block starts separately at the top of the right column and is followed by a separate `Veri sacerdotis...` paragraph. |
| 7 | Body and historical notes remain legible in normal column order; literal OCR oddities remain. |
| 8 | Sparse source-bearing ending retains the blessing, dating clause, `PIUS PP. X`, and two historical source notes. Compact terminal apparatus and common rights colophon fit below. This is not an apparatus-only page. |

Independent LF-only reconstruction from the spec matched the entire selected source: 38,490 bytes over 716 LF records. All selected non-LF bytes and their order equal the original selected ranges; the SHA-256 without LF is `867fb1ea710c4c76d4730bf2d79976a3a2047136a8419ffeaf21beb9e524e7b7`. The exact read-only command `tools/papal-source-notes check --spec src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-spec-iucunda-sane-f8303a221231/spec.json --out src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-blocks-iucunda-sane-bb189df41a86/text.txt --json` exited 0 with `status: pass`, one note group, and preservation flags true. Current pinned `scripts/_papal_source_notes.py` has SHA-256 `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`.

Source inspection covered the selected beginning/address/protocol (parent LF 20500 onward), source closing/subscription and final notes through LF 21214, exact repair LF **21044–21049** with preceding body LF 21038–21043, and generated TeX around the repair. The generated body exactly equals `render_body(validated)`. Explicit `\par` boundaries occur before `(1) i Cor. i, 18.` and after `(6) Ibid. i, 11.`. The source's isolated leading `i` on LF 21048 and marginal OCR glyphs remain literal, as do OCR labels `(5)` and `Í4)`; no lexical repair was inferred.

Only the separate exact `ass036-p525.pdf` supplied native visual evidence. Its actual count is one page. Parent PDF page 525 and subset page 1 have byte-identical `pdftotext -raw` output (SHA-256 `a04bf8be971fda72dda7dbcb32aeb1d18f87a88563a84e5c9390a4f048d3d79f`) and byte-identical serialized ElementTree page geometry under the documented proof method (SHA-256 `fc0043d448bb3689bc4b254ae748b89fc139d2381a99d31ed9f774a90171a6a6`). All twelve pinned lower-page line boxes were independently matched. Six smaller note lines occupy y=490.5707–548.8007 below the preceding body ending at y=480.3381; the isolated `i` sits separately at x=21.0. Direct visual inspection confirms this separation. The older composite wrong-page diagnostic was not used.

Pinned `_typeset_papal.py` SHA-256 `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` independently replayed `validate_document` and `pdf_body_fidelity`: **pass**, method `pdf-raw-source-aware-line-hyphen-nfkc-v3`, all 8 pages, source starts p1 and ends p8, 31,950 normalized source characters, 163 permitted layout hyphens. Fonts are embedded/subsetted Latin Modern Roman 17/10 regular and Roman 8 bold/regular, all with Unicode maps. Metadata identifies Pius X and Latin; dates match revision `2026-10-30T12:46:54Z`. Letter pages, no encryption, forms or JavaScript were reported. The disclosed underfull title-paragraph warning has no material visible defect.

Review limits: Independent review of exact final PDF bytes, all eight reader page rasters, bounded source LF boundaries and native OCR reconstruction page 525. No inherited visual coverage or review reuse. No translation accuracy, whole-source lexical collation, original-print image collation, historical-source intake/identity clearance, new rights clearance, installation or deployment certification. Literal OCR word divisions, note labels and isolated marginal glyphs remain preserved. The native Vatican PDF is an OCR reconstruction; its geometry supports this bounded note partition rather than original-print image identity. Separate source-intake and release gates remain independent. Every command/import used `PYTHONDONTWRITEBYTECODE=1` and `TRIPTYCH_LIBRARY_CACHE=0`. Only the exclusive reviewer scratch directory was written.

Canonical report destination (coordinator copy only): `src/sources/papal-documents/encyclicals-refinement-cold-30b.md`. Detailed results, native proof bytes, fonts and metadata remain in this scratch directory.
