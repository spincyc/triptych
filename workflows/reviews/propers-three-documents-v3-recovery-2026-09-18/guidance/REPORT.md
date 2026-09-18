# Proper-study v3 guidance cold review

Verdict: **PASS for the reviewed guidance and workflow contract.** No blocking guidance finding remains in the frozen final snapshot. This is not acceptance of either revised Sunday production or a substitute for the independent implementation review.

Reviewed base: `6f552cc63729bfa2a6970c13bdf92bf1257651db`. The reviewed changes were uncommitted. The complete reviewed file hashes are in `final/SHA256SUMS`, with exact copies under `final/snapshot/`. `final/SUPPORTING_SHA256SUMS` separately identifies four implementation files inspected only at the relevant contract seams. `final/changes.patch` records the focused tracked-file diff; the new artifact-gate schema is included in the snapshot.

## Scope and method

Read the applicable personal and repository guidance, both proper profiles and their established opening schema, the three-document profile, the chronology guidance, the proper-study operator section, and every proper-study fragment. Compared the changed guidance with HEAD and traced authoring, research sealing, proof building, review, repair, and publication ordering through the pipeline and relevant implementation. The exclusive write boundary was this review scratch directory; no subject, index, production, source, or shared file was edited.

The contract now clearly requires:

- An expansive 20–50-page study, including apparatus, developing two to five distinct whole-formulary interpretations. Each uses substantive compatible arguments from at least two Fathers or saints and has its own four senses.
- A 10–12-page concise study, including apparatus, with the complete inventory and exactly four overview rows on physical page 1; only Scriptural Date and Location on page 2; substantial Themes and Movement on pages 3–4; and developed interleaved comparison beginning on page 5. The earlier 1,500–2,500-word and one-third limits are explicitly superseded.
- A separately authored, directly speakable exegetical and pedagogical homily, ordinarily 10–12 minutes, with delivery estimates distinguished from an actual timed performance.
- Separate physical 1962 and postconciliar ownership through appointments, options, research, interpretation, outputs, and review evidence. Neutral primary sources and generic mechanics do not transfer liturgical appointments.
- Checked sources and rights, faithful uncertainty and alternatives, and a reviewed home for the concise chronology in the expansive study. Page counts and markers cannot replace substantive or visual judgment, and padding is explicitly refused.
- Fresh production identities and independent review after the clarified requirement. Historical accepted runs and verdicts cannot be restamped or inherited.

## Findings and final dispositions

| ID | Initial defect and reproducible consequence | Final disposition |
| --- | --- | --- |
| GUD-01 | `research.md:23–32` requires generated postconciliar chronology before study drafting, while `author-study.md:18–27` creates or revises the component manifest afterward. The original adapter required and fingerprinted the entire manifest, so a new leaf could not reach research review and ordinary later component edits made approved chronology stale. | **Resolved.** `guidance/scripture-chronology.md:1269–1272,1299–1306` now defines research-owned appointment inputs with an optional manifest identity/inventory check. Inspection of `_proper_chronology_inputs.py:123–152` confirms the presentation manifest is neither a generation prerequisite nor a byte dependency; meaningful identity/inventory disagreements still refuse. |
| GUD-02 | The chronology profile required adapter modules in the research seal, but declared external dependencies were restricted to `src/` and the engine added no computation dependencies. An author could not satisfy both instructions by declaring the scripts. | **Resolved.** `guidance/liturgy/propers-three-documents.md:106–109` distinguishes the engine-owned computation seal from external source owners. The v3 research-review command explicitly requests `--review-contract proper-study-v3`; `_proper_study.review_inputs` requires the chronology records and separately includes the computation inputs. The default historical seal shape is not silently changed. |
| GUD-03 | `study-review.md:20–22` required a complete PDF and `synthesis-review.md:11–16` required settled physical-page evidence, but the first explicit build instruction came after homily review. Neither preceding author fragment produced those required proofs. | **Resolved.** `author-study.md:42–49` and `derive-synthesis.md:34–42` now require settled author proofs, the correct edition-scoped artifact check, and exact artifact paths/hashes before cold review. These proofs do not replace the later shared-metadata build and full visual review. The documented CLI flags were checked against the actual tool help. |
| GUD-04 | Build guidance permitted source layout edits while content seals included those same TeX/style bytes. Visual guidance routed all typesetting defects to artifacts; stale upstream approval was only discovered at the terminal gate. | **Resolved.** `build-artifacts.md:13–20` now makes invalidation explicit. `artifact-gates` checks exactly research, study, synthesis, and homily seals and routes to the earliest affected author before visual review. `visual-review.md:22–27` routes source/style repairs to their source owner and reserves artifacts for regeneration from unchanged approved sources. `OPERATOR.md` documents the same sequence. |

An intermediate workflow load refused the new artifact checkpoint because its reused publication schema admitted repair targets absent from its routes. The final dedicated `proper-study-artifact-gate.json` admits exactly the four routed upstream owners, and the workflow now loads successfully.

## Verification and limits

| Check | Exit | Result |
| --- | ---: | --- |
| `tools/check-proper-components --help` | 0 | Confirmed `--phase artifacts --edition research` and `--edition synthesis` are supported. |
| `tools/tpt workflow show proper-study`, intermediate state | 2 | Recorded the artifact-gate schema/route mismatch described above. |
| `tools/tpt workflow show proper-study`, final state | 0 | Definition and referenced schema load; output retained in `workflow-show.txt`. |
| `git diff --check --` followed by the reviewed guidance, fragment, pipeline, and schema paths | 0 | No whitespace defects in the focused diff. |
| `sha256sum -c final/SHA256SUMS` from the repository root, using this review directory's manifest path | 0 | All 23 reviewed files matched their frozen copies. |
| Equivalent supporting-manifest verification | 0 | All four implementation seam files matched their frozen copies. |

No revised publication was built, visually accepted, installed, or published by this review. No external source claim or rights determination was independently re-researched; this review checked that the production contract preserves those required checks. Engine routing, pagination, chronology, and historical-compatibility regression execution belongs to the independent implementation review and is not claimed here. The two actual v3 productions must still earn their own research, content, visual, web, and terminal acceptance.

All retained review material uses repository-relative paths. No commit or push was made by this review lane.
