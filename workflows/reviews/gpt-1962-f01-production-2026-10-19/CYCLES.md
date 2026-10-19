# GPT Christ the King: production record

The maintainer authorized provider `gpt`, identity
`liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king`, for Sunday
25 October 2026, with the complete three-document workflow and publication
to `main`. The homily audience is an adult parish assembly. The starting
checkout was clean and fast-forwarded to `c6da24eda` before implementation.

The driver uses the actual `proper-study` engine. Each author stage receives
its compiled packet in a fresh worker at `high`; each cold reviewer receives
its packet without authoring history at `xhigh`. Program gates run through
the engine. Results, repairs and interventions are recorded as they occur;
no unperformed review or publication is implied by this initial record.

An independent preliminary calendar check is read-only. Further research and
authoring follow the workflow's serial dependencies; parallel authors would
share evidence and invalidate the required review boundaries.

## Run and environment

- Workflow: `proper-study`, version 12.
- Run: `3c11005c63dcd584`.
- Seed commit: `dbaed43763020c5deea78e4cf4fcbba124edf58a`.
- Workflow digest: `e6d49782e4c62eb282fbb9ce1e18a27f1e74c81170f26533f5efea288ebf4ff5`.
- Scope gate iteration 0: PASS.
- Context resolution iteration 0: PASS, fresh worker at `high`.
- Research iteration 0: dispatched to a fresh worker at `high`.

The identity gate, promise ledger and tool registry pass. The scope checkpoint
is pushed to `feature/propers/codex`. GitHub authentication was verified outside
the network sandbox after the sandboxed probe failed. Web conversion will use
the existing local Markdown 3.10.3 installation matching the dependency lock;
the system installation is 3.11.1. The existing main publications changed since
the previous workspace baseline were rebuilt and installed through their normal
Make targets, with exit 0, in preparation for whole-site deployment checks.

## Preliminary calendar defects

The independent page-image check located the feast at printed pp. 697–698,
the proper Preface at p. 291, and the precedence/commemoration rules at RG 17(d),
91, 111 and 112. The current FSSP France October Ordo corroborates the universal
feast without resolving unspecified local calendars. The calendar finding aid
omits Communion Psalm 28:11, treats the conditional votive Tract as unconditional,
and omits the three orations and proper Preface. The F01 identity adapter itself
works. A separate source-data owner is correcting the bounded calendar record
before research seals it. The workflow context author independently establishes
its own complete inventory; the preliminary check supplies no acceptance.

## Context resolution, iteration 0

The worker returned its actual PASS result, which the engine accepted. It
created `research/context.md` and the required `main.tex` owner reservation.
The eleven-element inventory includes the proper Preface; it distinguishes
the inactive Tract and Paschal Alleluia and excludes both displaced
commemorations. Three controlling formulary page images were individually
inspected. Rubric-image collation, wording and rights corroboration, source
bindings, reception research and chronology remain research-stage work.

The identity check passed. The source graph validated; the aggregate
`make check-sources` stopped at the expected new-leaf catalogue boundary,
because the downstream `web-edition.toml` declaration does not yet exist.
This is recorded as an incomplete aggregate check, not a pass. The engine
issued research packet 0, SHA-256
`54268de70b4b827b140d39be8f380615ba446e1478f29d21a01e8ccc507a877d`.

## Bounded calendar repair

The separate source-data lane completed the F01 correction. The October list
now carries ten calendar-index elements: the seven scriptural elements and
three composed orations with explicit, text-free witness gaps. The proper
Preface remains documented in the mass notes and verified source passage,
because the existing calendar-index schema excludes Prefaces. The publication
inventory still requires all eleven elements. The inactive votive alternatives
remain identified in the source evidence.

The lane corrected Communion Psalm 28:10–11, removed the unconditional Tract,
and added exactly three corresponding English absence records. It generated
the 1962 and inherited pre-1955 projections and the three owned census blocks.
The inherited projection makes no independent pre-1955 collation claim.
No existing source fingerprint, shared code, or unrelated publication changed.

Calendar validation, chronology loci and summary, generated calendar freshness,
census freshness, source-library validation, Ordinary validation and whitespace
checks all passed. Source-reader freshness identified the new passage's two
dependent projection files; the research owner will refresh them together with
its adopted sources. The aggregate source gate remains incomplete at the
new publication's pending inventory and catalogue entries. The coordinator
reviewed the source-data diff and accepted this bounded handoff for integration;
it does not replace the workflow's cold research review.

## Research worker interruption

Research iteration 0's worker stopped with a provider output error before
returning structured JSON. The engine remained awaiting the same packet; no
PASS or other research result was submitted. Its retained source extracts,
page-review material and generated chronology were inspected for recovery.
The same worker was resumed against the same packet and boundaries, with an
instruction to verify the saved state and complete the outstanding work.
This is a worker execution retry, not a workflow intervention or acceptance.

The resumed worker encountered the same output error a second time. A
diagnostic-only continuation identified the operation as reading the Lasance
extract in preparation for `propers/verified.md`; that file and the remaining
research records had not been saved. The coordinator stopped retries of that
operation and resumed independent, non-quoting research and source metadata.
It supplied an unverified 1926 pamphlet and a 1927 Schott digitization as
possible distinct historical-witness leads. Those leads establish no textual
or rights claim until the research owner actually checks them. The native
stage remains research iteration 0 throughout this execution recovery.

## Alternate-witness acquisition

The coordinator made a bounded, read-only acquisition and identity check,
leaving adoption, exact collation and source registration to the single
research-stage author. The complete Husslein pamphlet, *Christ the King*,
America Press, seventh printing with a 1926 copyright and imprimatur, was
retrieved from `https://distantreader.org/stacks/pamphlets/pdf/005197412.pdf`
(36 PDF pages, 2,572,265 bytes; SHA-256
`473775a5455cbbeeb5c8d88080c8c97239c08024fa6a2a27c2fcc6d77f689bb2`).
The `www` hostname failed certificate validation; the canonical hostname
succeeded with normal TLS verification. Inspected title, approval and printed
pp. 28–31 establish an expressly attributed historical English rendering of
the Mass at pp. 29–31, including the orations and Preface. Its older Sunday
commemoration rule is not the governing 1962 rule.

The complete Schott/Bihlmeyer scan was retrieved from
`https://missale.online/assets/liturgia/downloads/schott-1927-messbuch.pdf`
(1,495 PDF pages, 62,711,309 bytes; SHA-256
`4511fa924e0f260185576b220e25f24d4d130b8af64700fb720e0b03f1b07f92`).
The website and PDF metadata call it 1927, but the inspected title and printer
line identify a 1929 printing of the second revised edition, retaining 1927
approvals. Inspected printed pp. 1105–1108 contain Latin and German Mass
texts, with the proper Preface inline. The researcher must inspect the
preceding Introit page and establish the full relevant bound independently.
The host reports four missing scan pages; no whole-book completeness is
asserted. Both payloads remain in coordinator scratch, with source-page
rasters generated by `pdf-review`. These acquisition facts do not constitute
research acceptance or a blanket redistribution decision.

The research worker encountered a third provider output interruption after
successfully saving its alternate-witness metadata, bounded rights record and
scratch transcription. Its diagnostic continuation identified the last
successful write and image-view call, but could not identify a later rejected
operation. The same worker resumed from the saved state, retaining the
completed work and leaving any expressly refused operation untouched. No
stage result or acceptance was inferred from this interruption, and the
engine still awaits research iteration 0.

## Terminal research blocker and preserved checkpoint

A fourth output interruption left the research incomplete. The coordinator
stopped source-text production and requested a diagnostic closeout only. The
worker returned its actual BLOCKED result: complete Latin collation, text
adoption, record reconciliation and final validation were not finished.
Neither `propers/verified.md` nor `propers/retrieved.txt` exists. No cold
research review or subsequent production stage ran. The failed output's exact
operation could not be established; the saved scratch transcription was not
regenerated during closeout.

The engine accepted that result and reached terminal BLOCKED at research,
with three packets, three results and zero interventions. The native archive
under the leaf's `evaluations/proper-study-results/3c11005c63dcd584/` preserves
the actual packets, results, hashes, bootstrap, status and replay. It is an
archive of an incomplete run, not publication approval. Continuing production
requires a new native run and independent verification of retained evidence.

The closeout exposed two unsupported `rights_status = "mixed"` values in
the new facsimile metadata. The coordinator replaced them with the existing
`restricted` vocabulary, matching their metadata-only storage and explicit
whole-delivery exclusion. The bounded historical-text inventory remains
distinct from those delivery records; no facsimile payload or new proper-body
transcription is committed. The coordinator also corrected spacing in that
inventory and refreshed the source-reader projections through their owning
tool. The source graph then validated. These bounded checkpoint repairs do
not complete research or confer a review seal.

The promise remains blocked, with acceptance, installed artifacts, main
publication and live verification unmet. Only the feature branch receives
this incomplete checkpoint; no main push or deployment was performed.
All delegated lanes are closed, with no live operation
remaining. Additional authors or reviewers are not dispatched because the
engine has stopped before their required evidence boundary.

Checkpoint verification passed source-library validation, calendar validation,
calendar projection freshness, census freshness, source-reader freshness,
chronology generation, promise-ledger validation, tool-registry validation and
whitespace checks. A second native archive generated into scratch compared
byte-for-byte equal to the retained archive. `make check-sources` remains
unsuccessful: the incomplete leaf lacks its later-stage publication inventory
and `web-edition.toml`/catalogue declarations. The declarations are not fabricated
to obtain a passing check. Release bindings and deployment gates remain
unfinished with the publication; this feature checkpoint is not deployable.

The feature checkpoint contains 59 intended paths. Its sole newly retained
source payload is the complete CCEL *Ante-Nicene Fathers* VII text, whose
registered delivery states public-domain status; the modern official pages and
both alternate missal facsimiles remain metadata-only. The outgoing additions
were screened for machine-local paths and common credential patterns, with no
match. No PDF publication, facsimile scan or scratch transcription is included.

## Authorized reference-only scope, 19 October

The maintainer explicitly approved continuing with original commentary and
precise source citations and links, without reproducing the full Latin or
English propers. The three PDFs, canonical web edition, complete appointed
inventory, source verification, independent reviews and main deployment remain
required. This changes the publication's scope; it neither changes historical
source rights nor authorizes a retry of rejected source-text production.

The production plan now records the exact provider/identity authorization.
The promise ledger retains the unmet version-12 requirement with an explicit
maintainer-authorized waiver and adds the reference-only contract and fresh
version-13 acceptance requirements. The old terminal archive remains intact.

Two implementation lanes have exclusive ownership: one updates the owning
profiles and workflow instructions, and one updates the component/gate checks
and focused tests. The coordinator owns this record, production authorization,
project/ledger state and adjacent license/catalog descriptions. A separate
review will assess the integrated contract before a new production run begins.

Advancing the workflow version exposed a historical ledger check that looked
for version 12 in the current mutable pipeline file. Its criterion and PASS
remain unchanged; the check now reads the accepted Claude PC-S55 revision's
existing, immutable seed manifest, which records `workflow_version: 12`.
No historical run, receipt or publication input was altered.

The initial focused compatibility suite ran 221 tests successfully, with one
existing archival-fixture skip. A broader run found one author-registry failure
(Cyril of Alexandria in the unrelated Claude Twentieth Sunday manifest) and
five errors in two pagination tests whose mocks lack `presentation`. Both
the implementer and independent reviewer reproduced that exact failure set
against the unchanged base code. The registry and whitespace checks pass.

Independent review found one boundary defect: the generic schema-2 component
validator admitted reference-only postconciliar manifests, although the native
production gate correctly rejected them and the profile limits this mode to
1962. The finding is accepted and routed for a narrow calendar restriction
and standalone regression test before production is seeded. Exact provider
authorization remains the native production gate's responsibility.

The repaired component helper now permits reference-only only for schema 2
with `calendar = "roman-1962"`. Two additional regression tests cover canonical
postconciliar rejection and missing/invalid calendars while preserving existing
complete and rights-limited behavior. All 72 focused repair tests pass. The
independent reviewer closed the finding and returned PASS with no remaining
findings; its 139-test run had 138 passes and only the baseline-confirmed
author-registry failure. Promise-ledger, tool-registry and whitespace checks
also pass. This closes implementation validation only, not native production
or any substantive review. The version-13 workflow is committed before seeding
the fresh run; the incomplete publication is still not deployable to main.
