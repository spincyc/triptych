# GPT Nineteenth Sunday production

Run `b686b7a44f0e35e7`, `proper-study` v7, provider `gpt`, identity
`liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
date `2026-10-04`, audience `adult parish assembly`.

The run is pinned to seed commit
`a1320fb62298ed6b1cf10d82d252212a03a484d0` and workflow digest
`9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
Its disposition is pending. No artifact has been accepted or installed.

## Transitions

| Stage | Iteration | Result | Evidence |
| --- | ---: | --- | --- |
| scope-gate | 0 | PASS | Exact provider and permanent-identity authorization passed. |

Context resolution is active. Every agent stage uses a fresh worker with no
inherited authoring conversation and the packet's declared reasoning effort.
Author stages use `high`; review stages use `xhigh`. No nested workers are
authorized by this workflow.

## Validation baseline

Before publication authoring, `make check-sources`, `make check-release-bindings`
and `tmt check` passed. The release binding check reported zero stale bindings.
The promise-ledger check has identical failures against the seed ledger and
the newly registered target: ignored older PDFs are absent from a fresh clone.
Those failures are not new-target acceptance and remain separately identified.

## Scope

The target has three PDFs and one canonical web edition. Work is integrated
on the workspace branch `feature/propers/codex`; no main-branch merge or live
deployment is claimed. The source owner will archive the actual workflow
packets, results, terminal status and review evidence at completion.
