# GPT PC-S54-A production record

The requested target is the U.S. postconciliar Twenty-eighth Sunday in
Ordinary Time, Year A, 11 October 2026, for an adult parish assembly. The
canonical leaf is
`src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a/`.

## Run identity

- Workflow: `proper-study`, version 9.
- Digest: `ef8058d0bd73437c67569a8d24ce67dac4c273fef7688aef8a54dec9e7986b13`.
- Run: `beb2231b657a358d`.
- Seed commit: `742d56bd0152eba02999c6e9afb47ae3340c5a72`.
- Workspace branch: `feature/propers/codex`.

The native packets, results and engine state control the workflow. Every
authored stage uses a fresh worker at high effort; every judgment review
uses a fresh reviewer at xhigh effort with no authoring conversation. Gates
run through the engine. No worker commits, publishes or advances the run.
This production opens only the named GPT postconciliar identity.

## Current state

The scope gate passed. Context resolution is in progress; no study, source
acceptance or publication is claimed. A separate read-only identity check
confirmed the dated USCCB assignment and Year A against its 2026 calendar.
That finding is an input lead, not the workflow's context or research verdict.
The calendar and registry agree on Lectionary 142 and both Gospel lengths,
Matthew 22:1–14 and 22:1–10. Unspecified local overlays are not resolved.

The initial deliverable validator rejected missing evidence pointers on the
open requirements. Commit `72fa0d381` supplied them and corrected the earlier
commit message's premature validation claim; the ledger then passed with 60
entries. The run's seed remains its original commit.

Baseline `make check-sources` exited zero before the new leaf was created.
Its ordinary source-family gate retains 157 pending screening units; this
production does not claim to complete that separate screening project.
`tmt check`, `tools/tpt check-promised-deliverables` and `git diff --check`
also exited zero. These baseline checks are not final publication checks.

## Evidence retention

Native workflow records will be archived without manufacturing verdicts or
editing accepted inputs. Transient acquisitions, author proofs and visual
review artifacts remain outside tracked sources. Restricted source payloads
do not enter the public archive. Local installation, workflow acceptance,
branch publication and live deployment remain distinct states.

`checkpoints/context-dispatched/` preserves the exact native records after
the scope gate and first context dispatch. No author or reviewer result is
present there.
