# Jerome source-retention re-review

Verdict: **CHANGES REQUIRED** for the exact four files hashed in `final-subject-hashes.json`. All four original findings are addressed in substance, but one new schema defect prevents acceptance. Source records were read-only; initial review, checks, and hash files remain unchanged.

## Remaining defect

Location: `src/sources/works/jerome/commentarii-in-isaiam/editions/2026-09-17-dco-latin-web/artifacts/pars-4-pdf-97785e2b/artifact.toml:19–20`.

The repair adds `access_limitations` and `identity_search` as top-level artifact fields. Neither is accepted by the frozen artifact schema. `tools/tpt source-library validate` exits 1 and explicitly reports `unknown fields: access_limitations, identity_search`. The executable field list in `tools/source-library` supports `provenance` and `notes`, where this information belongs.

Required correction: preserve the identity-search account in `provenance` and the derivative/access assessment in `notes` (or another already supported explanatory field), then remove both unsupported keys. Do not extend the frozen schema to accommodate this metadata repair. Rerun validation and refresh the exact subject hashes before acceptance. The incidental missing spaces in `pages30–32` and `on2026-09-17` can be corrected in the same edit.

## Original findings

| Finding | Re-review disposition |
| --- | --- |
| Rights status overstated | Addressed: `rights_status = "unresolved"` and the basis explicitly disclaims an established PDF-specific restriction. No modern PDF redistribution permission is invented. |
| Remote retention decision incomplete | Addressed in substance: the record explicitly states no offline source substitute and no size obstacle; explains the unidentified base/editorial apparatus; assesses extraction without pretending a stripped body has an affirmative basis; leaves redistribution pending justified separation or an identified witness. Bracketed `Al.` apparatus is present on p. 32 in the previously checked exact PDF. This is an honest unresolved boundary, not a finding that the body is necessarily protected or permanently unretainable. The text must reside in an accepted field. |
| Alias-search provenance absent | Addressed in substance: actual commands, bound, and results are recorded as a follow-up after registration. Independent replay of the source-reader search returned one Jerome Isaiah work/edition/artifact/passage and zero readable passages. Broad metadata search and the narrow Jerome-title search found no competing Jerome Isaiah work. The text must reside in `provenance`/`notes`. |
| Edition date at end of path | Addressed: the subtree is now `editions/2026-09-17-dco-latin-web/`; the three old manifest paths are absent. All four stable IDs are preserved; work and edition record bytes are unchanged. |

The passage adds accurate bounds for the 55:10–11 continuation, pp. 30–32. The previously checked 55:6–9 locus remains pp. 27–30. The same complete offered 228-page PDF remains pinned to `97785e2b71a8bdc60e866af2309a205b119bce40cc16a237692a2cdda41ab7e9`, 643,374 bytes; both the supplied PDF and this review's independent download still match. No new source retrieval or historical-image collation was necessary because those exact bytes did not change.

## Checks and scope

- `tools/tpt source-library validate`: exit **1**, one source-record unknown-fields diagnostic plus **11 separate active publication-binding diagnostics**. Those consumer errors are not counted as defects in the four source records and are not accepted or repaired by this review. Log: `rereview-validation.log`.
- `tools/tpt source-reader list --author Jerome --find Isaiah --plain`: exit **0**, the stated one-work result reproduced. This non-strict listing does not override validation failure. Log: `rereview-source-reader.log`.
- `rg -l -i '(hieronym|jerome|eusebii|isaiam|isaiah)' src/sources/works --glob work.toml`: exit **0**, bounded alias results checked; log: `rereview-alias-search.log`.
- `rg -n -i 'Commentariorum in Isaiam|Commentarii in Isaiam|In Isaiam|Commentary on Isaiah' src/sources/works/jerome -g work.toml`: exit **0**, only the registered Jerome Isaiah work; log: `rereview-narrow-alias-search.log`.
- Hash/identity/old-path checks: four manifest hashes equal the repair handoff; all original IDs remain; all three old manifest paths are absent; exact PDF hash/size match; initial review artifacts match their original report inventory.

No interpretation or publication evidence-sufficiency judgment, appointment claim, publication build, binding acceptance, source edit, global inventory write, staging, or commit is included. No nested agents were used.

Snapshot boundary: the coordinator subsequently reported that the author was moving the two fields. A final live-hash assertion therefore exited 1 because the artifact had changed after the recorded inspection. This report and `final-subject-hashes.json` preserve the inspected `7b786e1c…` artifact state; they do not evaluate the later edit. A newly frozen handoff is required for its focused recheck.
