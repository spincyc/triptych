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

The scope gate and context resolution passed. The engine accepted the actual
`research-0000` worker result, then research-preflight-0000 rejected two
guidance paths in a dependency list restricted to source owners under `src/`.
The engine dispatched `research-0001` to a fresh high-effort worker. That worker
repaired the declaration, explicitly included the registered rights-authority
owners and recorded its bounded audit. Research-preflight-0001 passed and the
engine dispatched research-review-0000 to a fresh xhigh-effort reviewer against
its actual 1,768-file v4 research seal. That independent review passed with no
findings: all sealed files and 16 computation inputs matched, and the reviewer
checked the actual liturgical, reception and chronology evidence. Acceptance
retains the recorded exact-book, translation, chronology and unadopted-source
limits. A fresh high-effort author completed the 21-page expansive proof with
6,537 substantive words. All 21 initial pages were inspected, then the affected
pages rechecked after a chronology-table boundary repair and keeping the first
four-senses block together. The settled author proof is 461,386 bytes, SHA-256
`ef5d28fc061b8abd44738053a0f56135edcff24eb52cb326ddd0a8481087525b`.
Study-preflight-0000 passed. Fresh xhigh-effort study-review-0000 supported the
arguments, branch distinctions and coverage but returned CHANGES_REQUIRED for
STU-001: the historical appendix changes the NABRE introduction's “probably
at least a decade later” after A.D. 70 into “probably in the following decade.”
The generated chronology is correct; the prose adds an unsupported narrowing.
The engine dispatched author-study-0001 for the study-owned repair. The author
corrected only the historical wording, shared generation metadata and production
audit, preserving accepted research. Its 21-page proof has SHA-256
`c5ada91b5330bcff1f38437d1399ccefc767c16d4495b2daf2309379a154fa93`;
only pages 17 and 21 differ from the prior rasters and were inspected again.
Study-preflight-0001 and fresh xhigh study-review-0001 passed. The independent
review checked the current source fingerprint and proof, supporting source
loci and the retained Matthew introduction. STU-001 is resolved with no
blocking findings remaining. Checkpoints `1852e3c23` and `a60cc4c3a` are pushed,
preserving both study versions and their proof identities. The engine has
dispatched derive-synthesis-0000 to a fresh high-effort author. Its settled
concise proof has 10 pages and 3,255 substantive words, SHA-256
`65433c3386fc7f8acc5682b2d9af949cb09d4cf195c76f18680a15f558f90cf4`.
It interleaves both accepted interpretations after the prescribed four-page
opening. Author checks and all-page inspection pass; the actual
synthesis-preflight-0000 and fresh xhigh synthesis-review-0000 passed with no
findings. The reviewer verified the sealed inputs, exact supporting loci,
appointment images, chronology qualifications and all ten proof pages. The
engine dispatched derive-homily-0000 to a fresh high-effort author. Its
three-page proof has 1,208 spoken words, estimated at 10.1–11.0 minutes at
110–120 words per minute, SHA-256
`ab4c94523f4263905959012c7bc67e5c0c3a25f22e6113fef68de1481050719c`.
The textual turn is Paul's commendation of shared distress immediately after
his confession of Christ's strength. The author performed silent prose
rehearsal and inspected all three pages; no timed human delivery is claimed.
Homily-preflight-0000 passed and fresh xhigh homily-review-0000 is underway.
Homily, final visual, web and publication acceptance remain pending.
A separate read-only identity check
confirmed the dated USCCB assignment and Year A against its 2026 calendar.
That finding is an input lead, not the workflow's context or research verdict.
The calendar and registry agree on Lectionary 142 and both Gospel lengths,
Matthew 22:1–14 and 22:1–10. Unspecified local overlays are not resolved.

The context worker established the canonical week-28 owner, all three explicit
Makefile edges, edition adoption and occurrence, a reserved unpublished
entrypoint, context, source plan, instance manifest and composition audit.
It reacquired four complete registered PDFs with matching hashes and inspected
five relevant page images, and independently opened the U.S. readings and
GIRM. Source-library, link, scaffold and build-dependency checks passed.
The first research dossier adds 29 bindings, complete twelve-branch reception
matrices for two distinct readings, generated chronology and annotations, and
bounded repeated searches. Exact 2008/2011 altar-book collation and a primary
English offerings exemplar remain unclaimed; the dossier explains the limits
of the inspected witnesses. No protected prayer is reconstructed.

Six new exact source artifacts, four editions, one work and one OLM passage
validate. The only new tracked payload is the whole public-domain CCEL NPNF2
VII download. The source-reader refresh changes only the six affected edition
projections and index, preserving 3,081 readable passages. Source-reader rights
and currency checks, source containment, publication inventory and the family
ledger pass. The preexisting empty-family bootstrap ledger accepts the changed
canonical catalog under the tool's explicit bootstrap rule; all 158 owner
screening units remain pending and atomic citation coverage remains false.

The mid-production `make check-sources` exits 2 because document-library requires
the future author-study `web-edition.toml` beside the reserved `main.tex`.
The log is retained in the task scratch directory. Author-study has since
supplied that declaration. The complete source and catalog checks will run
again after the actual companion and publication records exist; that earlier
failed invocation is not reclassified as a pass.

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
