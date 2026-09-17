# Independent shared-source integration review

**PASS. No blocking or optional finding within the reviewed scope.**

Reviewed on 2026-09-17 against HEAD `af9b2d10a98a6aac2ce44cc84d6358ede8e630e8`, branch `feature/codex/propers/homily`. The subject is the uncommitted 58-file integration snapshot: the GILM artifact correction, its existing comparative-publication binding, the Claude publication inventory, and 55 changed/new files under `src/web/data/structure/sources/`.

The exact subject paths and SHA-256 values are in `reviewed-file-hashes.json` and the equivalent `reviewed-file-hashes.sha256`. The JSON manifest has SHA-256 `9305707b3c73037e3c9516e1bc6b308b5d2446fe0d170e95b6bf6abb5e7d678b`; the sha256sum manifest has SHA-256 `44dc7ac55cca591f052148d066b7a5e5b4480ee78eb26f9c566fae181adcec5f`. `focused.patch` preserves the tracked delta; the manifests also cover all 50 new projection files.

## Findings and evidence

| Subject | Independent result |
| --- | --- |
| GILM artifact | The exact local acquisition is 298,474 bytes, SHA-256 `d286cb135d608cebc47a398e7c8c3040384f9bd5e58cca01b9b96902c32fb9f1`. Independent `pdfinfo` reports 44 pages. Parsed comparison with HEAD proves that only `page_count` and its explanatory `notes` changed. Storage remains `remote`, rights remain `unresolved`, and no payload was added. The generated edition changes only its page count. |
| Existing GILM consumer | Reverse-use discovery finds only the comparative study's artifact binding. Parsed comparison proves that only this binding's fingerprint changed, to independently recomputed `sha256:97dd78f86f5f8c638e2932a98fdccb9ca91bc6579333d69e8457efa945323ef8`. Its article-number loci, translation-control role, inspection state and limiting context remain identical. Its source audit and edition record identify the same witness; no 45-page claim was found. The correction therefore supports accepting this fingerprint without changing a publication claim or rendered output. |
| Claude inventory | All 1,127 inventory file hashes match current bytes. Exactly 38 hashes changed: 37 now match bytes already present at HEAD, and the remaining one is the reviewed GILM consumer binding. Apart from `audited_on`, the overall snapshot, and those file hashes, the complete parsed inventory is identical to HEAD. Its 52-publication universe, classifications, ownership, ordering and other fields are preserved. The inventory replay passes against its classification review. The older reconciliation note's count of 37 is correctly understood as predating the additional binding update. |
| Projection and index | Strict regeneration comparison finds all 4,048 source-browser files current. Independent checks of the 29 affected edition files compare 83 artifact rows and 830 passage rows against raw TOML records. Source and controller identity, cross-work segment ownership, rights, storage, evidence states, verification dates and existing index identities/routes agree. The index adds 17 works, 25 editions, 25 artifacts, 33 passages and 25 readable passages; existing identities and rights remain intact. |
| Newly emitted text | Every one of the 25 new text payloads equals its controlling record's exact transcription or physical-line slice. Segment-controlled ranges remain within their declared segment bounds and exact controller hash. OCR and transcription cautions remain with their passage metadata; acquisition or inspection is not promoted to verification. Licensed Gregory text carries the recorded CC BY-SA 3.0 basis, source/history route and contributor attribution in the payload, plus the acknowledgement in the edition row. The retained derivative and third-party notice disclose the extraction and licensing boundary. |
| Withheld text | The other eight new passages comprise five `no-transcription` cases and three rights refusals. FSSP's Ordo, ICRSP's Ordo and Jerome's Isaiah delivery remain `unresolved`, unreadable and without text payloads. Their public passage rows contain identity and refusal metadata, not source context, notes, text or text paths. Withheld artifacts omit prose-bearing rights-basis/notes fields. Existing GILM passages remain withheld. No protected or unresolved text was exposed by this integration. |

The upstream source-retention reviews were evidence, not substitutes for checking this integration. At the independent comparison, all 126 files in the accepted retained-commentary snapshot and all four files in the accepted Jerome snapshot matched their recorded hashes. This review independently checked how those records and bytes are projected; it did not repeat every historical image or legal-source investigation. `evidence-file-hashes.json` identifies the supporting files mechanically examined; `verification-results.json` records the individual new passage dispositions and changed inventory hashes.

After that comparison, the coordinator added a separate URW font notice to `THIRD_PARTY.md`. That notice is the only subsequent mismatch against the 126-file upstream snapshot and is reviewed separately in `font-notice-review.md`; it does not change any of these 58 integration subjects. The initial successful check, evidence hashes and subject snapshot remain preserved rather than being replaced by the supplement.

## Commands and results

Commands ran from the repository root. Logs and the independent script are in this review directory. Each check below exited 0.

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 tools/source-reader structure --strict --check` | Source-library validation succeeds; all 4,048 generated files match. `projection-check.log`. |
| `PYTHONDONTWRITEBYTECODE=1 tools/source-reader check --strict` | 5,160 passages, 3,059 readable, 2,101 withheld with reasons; the existing browser model replay passes. `reader-check.log`. |
| `PYTHONDONTWRITEBYTECODE=1 tools/source-inventory check src/sources/inventories/claude-publications-v1.toml --review src/sources/inventories/claude-classification-review-v1.toml` | 52 publications, 1,127 source-surface files and five owners valid. `inventory-check.log`. |
| `sha256sum .scratch/no-production/research-0/gilm.pdf` | Exact registered hash above. Independently repeated by `verify.py`. |
| `pdfinfo .scratch/no-production/research-0/gilm.pdf` | 44 pages and 298,474 bytes. `gilm-pdfinfo.log`. |
| `tools/source-library uses artifact.catholic-church.ordo-lectionum-missae.english-liturgy-office-web-2026-07-25.liturgy-office-pdf-d286cb13 --format json` | One consumer, as described above. `gilm-uses.json`. |
| `PYTHONDONTWRITEBYTECODE=1 tools/source-library fingerprint artifact.catholic-church.ordo-lectionum-missae.english-liturgy-office-web-2026-07-25.liturgy-office-pdf-d286cb13` | Matches the refreshed binding. `gilm-fingerprint.log`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 .scratch/source-integration-review/verify.py` | All independent comparisons above pass; all 58 subject hashes unchanged. `verify.log`, `verification-results.json`. |

The exact focused `git diff --check` command and final hash-verification commands are recorded in `commands-results.json`; they also pass. The exploratory consumer search for `45`/`forty.five` returned only unrelated artifact identifiers and digest substrings, recorded in `consumer-page-count-search.log`.

## Scope limits

This verdict accepts shared integration only. It does not accept either active TLM or NO publication, its authored research, interpretation, appointment claims, evidence sufficiency, rendered documents, or release. Neither production leaf's authored content was read or modified. Publication ownership remains separate; the shared library does not merge their local judgments.

No subject file, source record, production leaf, staging state, branch or commit was changed by this reviewer. The only writes were under `.scratch/source-integration-review/`. No nested delegation occurred. Unchanged browser UI code, visual review, publication builds and the coordinator's final repository-wide gates were outside this data-integration review and were not claimed as completed here.
