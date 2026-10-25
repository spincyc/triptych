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
| author-study | 0 | In progress | Fresh `high` worker; packet SHA-256 `1aca5d8f90591bc1b7cf29ea5d9089e40b4836970af4a9f48a60adb869849c69` |

Research acceptance authorizes drafting within its checked boundary. No
future prose, artifact, web or publication acceptance is inferred from it.
Terminal run packets and results will be
archived into the canonical leaf using `proper-study-run-archive`; the live
ignored runner directory is not durable evidence.

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

Source registration retained 13 lawful new artifacts totalling 9,792,728
bytes, including exact historical Missal pages and checked Bede evidence.
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

## Preparation checks

- `tools/check-proper-identity --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints`: passed.
- `python3 scripts/_proper_study.py check --provider gpt --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --date 2026-11-01 --phase scope`: passed.
- `python3 -m unittest tools.tests.test_check_proper_identity`: 18 tests passed.
- `python3 scripts/replay_examples.py --tool check-proper-identity`: four examples replayed, no divergence.
- `tools/tpt check-calendar-masses --calendar roman-1962`: passed after the exact fixed-date/catalog crosswalk was extended for F02.
- `git diff --check`: passed on the preparation diff.
