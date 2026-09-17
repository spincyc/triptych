# Final Jerome source-retention re-review

Verdict: **PASS**, limited to the exact four source records in `accepted-subject-hashes.json`. The original four findings and the subsequent unsupported-fields defect are resolved. This accepts the accuracy of the recorded unresolved retention posture; it does not clear the PDF or extracted text for redistribution, establish a historical edition, or accept any publication's interpretation, appointment, or evidence sufficiency.

The final artifact is `src/sources/works/jerome/commentarii-in-isaiam/editions/2026-09-17-dco-latin-web/artifacts/pars-4-pdf-97785e2b/artifact.toml`, SHA-256 `3254550e744db5ecf606f7ff943e368da72e6072daa04d5460751964aa55976b`.

| Finding | Final disposition |
| --- | --- |
| Restricted status without an established restriction | Resolved: `rights_status = "unresolved"`; no PDF-specific restriction or redistribution permission is invented. Exact PDF bytes remain outside the artifact directory. |
| Incomplete remote-only retention account | Resolved: `notes` now records the concrete unidentified edition/editorial-apparatus obstacle, the assessed derivative route, absence of a size obstacle, and absence of any offline source substitute. Separation or an identified historical witness remains necessary before redistribution can be justified. A scholarly paraphrase is expressly not represented as a retained source. |
| Alias-search provenance missing | Resolved: the actual bounded follow-up queries, routes, and results now reside in accepted `provenance`, explicitly after initial registration. Their material results were independently reproduced during the prior re-review; this final edit preserves that account. |
| Date-suffix edition path | Resolved: the date-prefixed edition directory remains; all original stable IDs are preserved and the three old manifest paths are absent. |
| Unsupported repair fields | Resolved: `access_limitations` and `identity_search` are absent. Their assessed content is preserved in `notes` and `provenance`, without a schema change. |

The other three record hashes are unchanged from the prior inspected repair snapshot. Source-local identity and bounds therefore retain the earlier direct checks: complete offered Pars 4, 228 pages, books XV–XVIII; Isaiah 55:6–9 at pp. 27–30; immediate 55:10–11 continuation at pp. 30–32. Both local copies of the complete offered PDF still match SHA-256 `97785e2b71a8bdc60e866af2309a205b119bce40cc16a237692a2cdda41ab7e9`, 643,374 bytes. No second acquisition or repeated visual collation was needed for unchanged exact bytes. The recorded certificate-validation limitation remains.

Checks executed from the repository root:

| Exact command | Exit | Result |
| --- | --- | --- |
| `tools/tpt source-library validate > .scratch/jerome-retention-cold-review/final-validation.log 2>&1` | 0 | Entire source library valid: artifact=2727, corpus=5, edition=988, passage=5160, segment=89, work=723, bindings=2665. No source or consumer-binding diagnostic in this run. |
| `/usr/bin/python3 .scratch/jerome-retention-cold-review/final-verify.py > .scratch/jerome-retention-cold-review/final-verify.log 2>&1` | 0 | All four exact handoff hashes match; unsupported fields absent; required explanatory content present; other records unchanged; stable IDs preserved; old paths absent; PDF hash/size unchanged; no payload in the artifact directory; prior review/report hashes unchanged. |

The earlier consumer errors were reported separately in their own snapshots; their absence from this validation run does not expand this review into publication acceptance. No source records, publication records, global inventories, staging, or commits were changed by the reviewer. The original review, first re-review, checks, and hash inventories are preserved. The only outputs of this final check are new files under `.scratch/jerome-retention-cold-review/`.
