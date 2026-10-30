# Independent cold review — packet 34b

Result: **PASS**, two Latin PDFs, eight reader pages. No material blocker was found. This review covers the exact replacement bytes below and the declared source-note separation; producer PASS rows supplied no visual acceptance.

| Work | Exact PDF SHA-256 | Pages individually inspected | Result |
| --- | --- | --- | --- |
| Diuturnum illud — acta.ass.014.ass-014-act-001 | `2b57d1b7b23edbbaf5b48fd55d388d48aa0843cd5e4087c65fb40ed29dc6ced5` | 1, 2, 3, 4, 5, 6 | PASS |
| Paternae providaeque — acta.ass.032.ass-032-l08224 | `ae4b936f4a4c63e77e17336d8dcb3989676e15fcd2c29f931a26c5a5e054692e` | 1, 2 | PASS |

Both packet contact sheets and every listed reader page were opened individually from the exact pinned raster sets at original resolution, one image per transfer. Native actual Diuturnum PDF pages 9 and 10 and Paternae PDF page 217 were also opened individually at original resolution through their proved one-page excerpts. No visual review was inherited or reused; reused pages and reuse proofs are empty.

## Independent mechanical verification

The shared receipt SHA-256 is `04edda9f22905ccb201809b3f2ab04601ca57e87f231b6e1ccc80dea84307f20`; the frozen manifest SHA-256 is `09302898a48d7a8bbd806ea0f30e08a70166747b5c43d82739305509c6474fa6`. Actual PDF hashes and `pdfinfo` page counts agree. Each full packet `source_row` equals its unique frozen-manifest row. Receipt source IDs, selected ranges, hashes, render revision and output identities agree. Current segment and artifact TOML records equal the pinned metadata, and the selected payload/spec/helper/evidence pins match. All declared raster files match at both the output and cache locations; cache receipt PDF identity, page count, renderer fingerprint and tool/font pins agree. There were 132 exact file-pin checks, including repeated checks where evidence refers to the same bytes.

The current pinned `scripts/_papal_source_notes.py` (`a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`) independently passed both exact `tools/papal-source-notes check --spec <pinned-spec> --out <canonical-selected-text> --json` replays. Diuturnum's two note groups produce `f8d640ff987c890347973998920d851194d3628bccf8c10c199b362b8f3c62b4`; Paternae's one group produces `2f4652578ad29c3940b86d138b0210fa6c3b3f32225306ca9842fcc60ccd3d9d`. Selected non-LF bytes and order are preserved.

Using pinned `scripts/_typeset_papal.py` (`1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`), independent `validate_document(source_row, root=repo)` and `pdf_body_fidelity(pdf, validated, pages)` passed for both PDFs. Diuturnum accounts for 28,043 source characters and 124 permitted line-end layout hyphens; Paternae accounts for 9,507 source characters and 42. Each source begins on reader page 1 and extends through its final page. This is the declared whitespace/Unicode/source-aware line-hyphen check, not lexical collation.

Parent and excerpt raw UTF-8 `pdftotext -raw` bytes independently agree for all three mapped native pages. Their first XML page elements from `pdftotext -bbox-layout`, serialized with default `ElementTree.tostring`, also agree byte-for-byte with each other and the packet hashes using `NATIVE_PROOF_METHOD.md`. All exact preceding-body/first-note/last-note LF anchor hashes match.

## Source and page findings

Diuturnum: original historical-text LF 287–290 on native actual page 9 are a four-entry vertically stacked smaller-type note group. LF 329–331 on native page 10 are a three-entry vertically stacked group. Neither assigned group contains side-by-side note columns or row-interleaving. Reader page 4 retains each in a distinct indented paragraph; the generated body TeX explicitly places `\par` before and after both. The retained body interruptions after `im-` and `quantum in` occur at those historical source-page breaks, and the body resumes after the separate note paragraph. They are not note/body fusion. Note labels and citations remain identifiable. Earlier page-break notes on pages 2–3 and later notes on pages 5–6 remain separated. Page 6 is sparse but source-bearing: it retains substantial final body text, blessing, dating, subscription and the final two notes before the ruled source apparatus and rights colophon.

Paternae: original historical-text LF 8379–8383 map to the five vertically stacked smaller-type citations below the centered subscription on native actual page 217. Reader page 2 preserves the blessing, dating and `LEO PP. XIII.` before a distinct indented notes 1–5 paragraph and then the ruled terminal apparatus. Generated body TeX confirms the explicit paragraph boundary. No note-column interleaving or apparatus-only spill occurs.

Across all eight reader pages, the titles, pope/date/language identification, two-column reading order, paragraph indents, source closing and terminal apparatus are readable. No visible clipping, missing glyphs, overlap or obstructed column transition was found. Both PDFs use embedded, subset Latin Modern fonts with Unicode maps; metadata title, Latin subject and Leo XIII author match, and PDF creation/modification times match the fixed render revision. The Diuturnum log has one underfull hbox warning (badness 1019, paragraph lines 22–25); direct page inspection found no material consequence. Paternae has no listed compile warning. No overfull, undefined-reference, missing-character or fatal error was found in the inspected logs.

## Limits and handoff

Literal OCR spelling, source word divisions and spacing remain disclosed limitations. Native evidence is an archival OCR reconstruction; this review establishes the exact excerpt mapping and bounded note geometry, not original-print glyph identity, whole-source lexical or translation accuracy, new historical-source identity/intake approval, or new rights clearance. Any separately owned intake/global gate remains separate. No source, PDF, producer output, shared cache, manifest, installed reader, release record or Git state was changed; all reviewer outputs are confined to the assigned scratch directory. Every Python import and source/helper check ran with `PYTHONDONTWRITEBYTECODE=1` and `TRIPTYCH_LIBRARY_CACHE=0`.

The coordinator owns integration of these exact report bytes at `src/sources/papal-documents/encyclicals-refinement-cold-34b.md`, together with the hash-bound review rows and independent global gates. Detailed reproducible verification is in the reviewer's `verification.json` and `verify.py`.
