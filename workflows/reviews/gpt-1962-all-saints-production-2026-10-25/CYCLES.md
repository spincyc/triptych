# GPT All Saints proper-study production

## Authorized target and native run

The maintainer requested completion of the next Sunday's 1962 Roman Missal
propers on 25 October 2026. The dated target is All Saints, 1 November 2026,
with the privileged commemoration of the Twenty-third Sunday after Pentecost.
The stable identity is
`liturgy/roman-rite/1962/propers/temporal/f02-all-saints`; the complete-text
three-document contract requires the expansive study, concise study, homily
and canonical web edition. The identity/profile/authorization preparation
landed in `24c1b7ce1781f79937f57b66c221b0ed82e219d9`.

| Native fact | Value |
| --- | --- |
| Workflow | `proper-study`, version 15 |
| Run | `fb0417d471635250` |
| Workflow digest | `4218c6138a9943b56536f7736897e8aece682852d8a205a5454ab0d09ee52d83` |
| Seed commit | `24c1b7ce1781f79937f57b66c221b0ed82e219d9` |
| Audience | Adult parish assembly |
| Initial research handoff | Preliminary source leads, independently checked by the native workers |

Every agent stage is SINGLE: one fresh worker without authoring conversation
history at the packet's declared effort. Author stages use `high`; independent
review stages use `xhigh`. Program gates execute through the runner without a
worker. Preparatory text, New Testament reception and Old Testament/liturgical
reception lanes preceded the run and supply leads rather than verdicts.

## Chronology review boundary

The repository's global 528-row chronology source audit and maintainer
acceptance remain open. Earlier propers integrations and the current mandatory
consumer interface coexist with that unfinished global criterion. This
production does not assert that the global corpus has passed that audit.
The present target authorization is bounded to F02, and independent native
research review must inspect every material emitted chronology claim against
its controlling source. Its concrete findings and any limitations belong in
the leaf's research and production records. They do not close the global
promise or stand in for maintainer acceptance of the entire corpus.

## Native progression

| Stage | Iteration | Disposition | Evidence |
| --- | ---: | --- | --- |
| scope-gate | 0 | PASS | Runner result and exit-code scope validation |
| resolve-context | 0 | PASS | Fresh `high` worker; exact fourteen-row dated inventory, source plan and reserved owner; packet SHA-256 `97725821b05cbe012077e2206bd9aa32b03fc51acf9be8111044c955b1d01963` |
| research | 0 | PASS | Fresh `high` worker; fourteen-element collation, complete-context/reception audit, two interpretations, exact existing-source bindings and registrar receipts; packet SHA-256 `e4e42e23c9a9cdd2bdae94398cc2e7644f3a528108ed0ba64d9e98aea59f7d64` |
| source-registration | 0 | PASS | Fresh `high` worker; 72 bindings, 75 dispositions, five admitted Bede passages and registered lawful retained evidence; packet SHA-256 `7e609bfa775db80c9f155fc6325cc9cee11ce80840ed32f13e7aeb5c1d048e29` |
| research-preflight | 0 | PASS | Native program gate; packet SHA-256 `21d4fdbf6937529e73d4182eeb6edb08eea87adc051fb810b3c47b99078ef2be` |
| research-review | 0 | PASS | Fresh `xhigh` reviewer; source difficulties, distinct arguments, dates, boundaries, bindings and dispositions independently checked; no findings; packet SHA-256 `053663e7fd72d8ed5ed66ab4c51c527f9c3b05363dab976563897925e96d8404` |
| author-study | 0 | PASS | Fresh `high` worker; settled 22-page proof, every page inspected, clean scoped checks and web probe; packet SHA-256 `1aca5d8f90591bc1b7cf29ea5d9089e40b4836970af4a9f48a60adb869849c69` |
| study-preflight | 0 | PASS | Native program gate; packet SHA-256 `99adf4db8d1495e6fa9f286188a805dbfb46b1465afed54f8d0279324d68a898` |
| study-review | 0 | CHANGES_REQUIRED | `STU-001`: integrate the Lesson's actual words into the second interpretation using checked evidence; `STU-002`: isolated editorial instructions in the earth comparison, advisory; packet SHA-256 `060689d832f9357b1d7ef9b3af72b8e778f0e1bc6e8a8ffe5c2a7277bb26626d` |
| author-study | 1 | PASS | `STU-001` repair reported and advisory cleared; 22-page proof SHA-256 `c9d409ae77be7d0214d2716a65f867072d1bf7dcc9c6397f29f2203a1638dc61`; packet SHA-256 `dae34cebc0f4e53c823ad2f7bf4f167f13b08a25bf662ecea76135521ec8dbb0` |
| study-preflight | 1 | PASS | Native program gate; packet SHA-256 `9232219cac24bae4ffb97b0fddcb2bcf8094779ce3def6f67cbd226d116e5b4a` |
| study-review | 1 | PASS | Lesson argument and inherited-earth distinction independently checked; all 18 sealed study files intact; no findings; packet SHA-256 `c69bf76a078969e1502ef66b52026da5fc11a26b1797516816b7e38250d99993` |
| derive-synthesis | 0 | PASS | Fresh `high` worker; ten-page proof, fixed opening and all pages inspected; proof SHA-256 `4e26fe55a269fa81a6b2c473cc9e4d00ebdff525c9e49344c7ccb6270e99acea`; packet SHA-256 `2a30cba9f2244cef4c3cd0c9d9b0b2f20181bb170ada96bac25bf259bb13402f` |
| synthesis-preflight | 0 | PASS | Native program gate; packet SHA-256 `f91b9707d41a6f29fef8d2e1dfa3921ba3d6ded23ee1b5a16d90c64e791a0901` |
| synthesis-review | 0 | PASS | Fresh `xhigh` reviewer; both arguments independently reconstructed, exact source claims and chronology qualifications checked, ten pages inspected; no findings; packet SHA-256 `3b0328010a68cf6cd73952d4352b23904e8e42f22dd49a8b588dbfe6e023a52f` |
| derive-homily | 0 | PASS | Fresh `high` worker; 1,236 spoken words, estimated 10.3–11.2 minutes, three-page proof inspected; scoped checks pass; proof SHA-256 `4adaca1195f3e3b7e06f92069a1e59b808c08b1d841e32dbdb0fddbbc0f4f2e5`; packet SHA-256 `0fbbade2899eb8eb0dda019be2a895069c7f9646dae2c871368a280fde31d70d` |
| homily-preflight | 0 | PASS | Native program gate; packet SHA-256 `7c3ec487ce84064b78208d6a7cbc56785da8b513da7f4bee1c1544444d4d897c` |
| homily-review | 0 | PASS | Fresh `xhigh` reviewer; source-and-speech review, independently counted 1,236 words and all nine sealed inputs checked; no findings; packet SHA-256 `e6f13b1969bd97ef575e02a9d461db2886c4d2b3a70f98548fff0b29e57a2a27` |
| build-artifacts | 0 | PASS | Fresh `high` worker; normal Make builds, 22/10/3 pages, settled concise physical markers, clean logs, embedded fonts, full extraction, snapshot and 35 bounded rasters; no source/layout edits; packet SHA-256 `13c18eacc9a501aea127cd3256e37c5ee3cd752ed245cc0a466377dff93d7bdd` |
| artifact-gates | 0 | PASS | Native program gate; packet SHA-256 `f6c85fc49ad72fe3942dfafd243f3875b31ec269cf572585c5b85824af824d87` |
| visual-review | 0 | PASS | Fresh `xhigh` reviewer; all 35 full pages and four contact sheets inspected, 30 receipt-bound and 74 raster files checked, readable chronology and settled concise markers; no findings; packet SHA-256 `c92f928a41f101af44b00544ebfae5be6f5dfcad9751cd4f42a0083189fe7fde` |
| generate-web | 0 | PASS | Fresh `high` worker; canonical Markdown generated and snapshotted with pinned dependencies, both lanes/four senses/14 text anchors/56 source notes preserved; no source edits; packet SHA-256 `d42db767012445b5ddae029bba939860ef8db5ab4ee7a2daa864e020490d0e65` |
| web-review | 0 | PASS | Fresh `xhigh` reviewer; exact conversion/source/PDF, 1280×900 and 393×852 CDP, 17 screenshots, 125 resolving fragment links and all source notes checked; one nonblocking source-prose advisory `WEB-REGISTER-001`; packet SHA-256 `5e9025609378e231e3d9fbc5d1305480fc242bb545afc84a08f5be0a94da2437` |
| install-publication | 0 | PASS | Fresh `high` worker; three normal Make installs preserve reviewed hashes, exact canonical Markdown and three alpha records installed; actual shared receipt verified; packet SHA-256 `36a9eae593c3f0a4bb25979d771b731fd6063150663eb68d53604e97b9624184` |
| publication-gates | 0 | PASS → ACCEPTED | Native terminal program gate; immutable seals and all five declared checks pass, no escalations; packet SHA-256 `14c585d8c7b0cd7140eb37b3449ce8c1eb9d82b967b697d0fbfd918b479827ac` |

Research acceptance authorizes drafting within its checked boundary. No
future prose, artifact, web or publication acceptance is inferred from it.
Terminal run packets and results are archived using
`proper-study-run-archive`; the live ignored runner directory is not durable
evidence.

Author proof hashes identify the bytes inspected within each authoring phase.
The later artifact snapshot, independent visual review and installed-byte
comparison determine the final publication hashes after shared generation
metadata has settled.

The web reviewer classified `WEB-REGISTER-001` as nonblocking: the closing
process sentence in `sections/70-date-location.tex` should be deleted when
that source passage is next revised, preserving its qualified historical
alternatives. It is retained in this production's accepted bytes rather than
silently changed after the source, PDF and web reviews.

The resolver's optional broad `make check-sources` invocation was stopped
during its silent `act-history` prerequisite after 3m44s without a verdict.
Its exact context/identity checks passed. Shared inventory refresh and global
source/deployment checks remain with the outer coordinator; the source-owner
scaffold is intentionally completed by the later authoring stage.

The research worker's final checks accepted the existing source graph and
37 local bindings, the canonical chronology record, and its generated
orientation-v2 annotations. The source-registration handoff preserves the
exact new-source receipts and the work still owned by the registrar; this
research result grants neither source-registration nor cold-review acceptance.

Source registration added 13 artifact manifests: 12 retained payloads totalling
9,792,728 bytes, including exact historical Missal pages and checked Bede
evidence, plus one restricted metadata-only Ordo record with no retained
payload.
All 37 original binding dictionaries and fingerprints remained unchanged.
Local source-library, source-disposition and Catena admission checks passed.
The outer coordinator generated the Source, Catena and Proper projections
and refreshed the publication inventories, classification and family ledger.
The broad `make check-sources` exited 2 at the intentional pre-author scaffold:
the document catalogue required the later `web-edition.toml`. The recipes after
that refusal did not run. No global source PASS, fabricated web declaration,
early provenance import or completed publication is asserted. The independent
root-owned Catena structure-currentness check was still running when the
registration result was submitted; its eventual outcome is recorded separately.

That check subsequently passed against 2,048 generated Catena files. Every
aggregate operation is terminal. The complete actual commands and outcomes
are retained in
[`source-registration-aggregate.json`](../gpt-flt-and-sunday-2026-10-25/source-registration-aggregate.json).
The generated-data delta is 537 files; 163 family review units remain pending.
This focused success does not change the recorded pre-author refusal of the
broad source aggregate or close the global chronology audit.

The initial expansive author iteration 0 proof had 22 pages and 460,080 bytes, with SHA-256
`6b86bdd980f598783bfdf5dafcd4020b2a391cfeae6ea18fd1cc6b1da0db7cb2`.
Its content/artifact checks and pinned-dependency conversion probe passed.
The author's broad `make check-sources` subsequently exited 2 because the
document catalogue required the future `homily.tex`; this authoring stage
explicitly permits future companion files to remain absent. No companion stub
or aggregate repair was manufactured. The native study preflight and cold
study review remained separate judgments. The later accepted study proof is
the iteration 1 hash recorded in the progression table.

## Reviewed and installed outputs

The normal `make install-doc` recipes exited 0 for all three outputs. Every
build PDF and installed PDF matches the immutable visual-review bytes. The
canonical Markdown was copied byte for byte, independently verified and staged
by the root coordinator. Its accepted SHA-256 is
`a5fa4507b9e9c2f56a461afe67d941b739b92cf34efef6397097fc7958ff30f8`.

| Output below `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/` | Pages | SHA-256 |
| --- | ---: | --- |
| `f02-all-saints.pdf` | 22 | `0e357f23576aeb6bad9e70b970b391c0a33b33f6ec80c3ca8cd66e4d6f5be8bd` |
| `f02-all-saints-synthesis.pdf` | 10 | `921dfd64e8585cb5a8864f00211c790591d1658f6283aecfa137143c291bc25b` |
| `f02-all-saints-homily.pdf` | 3 | `4adaca1195f3e3b7e06f92069a1e59b808c08b1d841e32dbdb0fddbbc0f4f2e5` |

The root coordinator's actual preterminal shared integration is recorded in
[`preterminal-integration.json`](../gpt-flt-and-sunday-2026-10-25/preterminal-integration.json),
SHA-256 `2ebf3a6c9c34e0f8fdbf5e999f4f7a2635e6363306dc0aa11e75de24985678fc`.
Its twelve focused commands exited 0. Complete source, site and deployment
checks remain the root coordinator's final work after the terminal archive
and subsequent publication-inventory/family refresh. Native acceptance does
not claim those later checks or close the global chronology audit.

## Terminal archive and final lane checks

`tools/proper-study-run-archive fb0417d471635250 --cycles
workflows/reviews/gpt-1962-all-saints-production-2026-10-25/CYCLES.md`
exited 0 and archived the actual `ACCEPTED` run under the leaf's
`evaluations/proper-study-results/fb0417d471635250/`: 25 results, 25 packets,
zero interventions and 55 files in total. A second archive to
`.scratch/tlm-discovery/final-archive-check` exited 0; `diff -qr` between
the two trees exited 0 with no differences.

The archive's `record.md` SHA-256 is
`2e599e2b60bd97913fabce1678c385e70d8da1a83c21cd50c114495b96bbf960`.
Its actual terminal gate result SHA-256 is
`87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a`;
`terminal-status.json` is
`e289c554436a1dc02c03bb06a3140aa888f9769787ae911c6a5dac1ff8677764`.
The final lane's whitespace check passed. A scoped scan of the leaf and this
review record found no private home/tmp paths, local preview addresses or
machine account strings. No commit, push or index mutation was performed by
this production lane; the root coordinator staged the reviewed Markdown and
owns final global integration and deployment.

## Preparation checks

- `tools/check-proper-identity --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints`: passed.
- `python3 scripts/_proper_study.py check --provider gpt --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --date 2026-11-01 --phase scope`: passed.
- `python3 -m unittest tools.tests.test_check_proper_identity`: 18 tests passed.
- `python3 scripts/replay_examples.py --tool check-proper-identity`: four examples replayed, no divergence.
- `tools/tpt check-calendar-masses --calendar roman-1962`: passed after the exact fixed-date/catalog crosswalk was extended for F02.
- `git diff --check`: passed on the preparation diff.
