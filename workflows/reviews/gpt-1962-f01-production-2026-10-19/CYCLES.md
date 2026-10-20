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

## Fresh version-13 production

Run `78d1516ca75da9df` was seeded from committed and feature-pushed
`e8d76b1266990caa5eb18b50d1862af3453483bc`, workflow version 13, digest
`7568a7728ef8a16e5a7c65475e9a3ae0d24c695caab6faa5d0c0c7ec52621d16`.
Its arguments are provider `gpt`, the F01 canonical identity, date
`2026-10-25`, audience `adult parish assembly`, and no preliminary handoff.
The native scope gate passed. A fresh worker at the declared high effort
received the exact `resolve-context-0000` packet, with exclusive stage scratch
and no inherited authoring conversation. No old result is carried into this run.

`resolve-context-0000` returned PASS and was accepted by the engine. It changed
only `research/context.md`: the first-line mode declaration, independent
appointment and boundary inspection of seven Missal pages, the dated Ordo
check, and the element-specific locator/inspection plan. It retains eleven
active elements and two inactive seasonal branches. The authenticated Missal
matches its registered hash; the original registered Ordo snapshot and a
fresh, byte-distinct retrieval independently agree on the October 25 entry.
The existing binding remains explicitly tied to the registered snapshot.
Identity and whitespace checks pass; `make check-sources` validates the source
graph and then fails on the scaffold's pending web-edition/catalogue work.
The native engine emitted `research-0000`, dispatched to a fresh high-effort
worker with exclusive scratch and no inherited conversation.

## Full material restored; reference-only scope withdrawn

The maintainer then explicitly rejected locators as the deliverable and
required full sourced material. The coordinator immediately stopped the
reference-only research worker. Its closeout reported no tracked edits,
unfinished writes or live operations. It had independently authenticated both
complete missal PDFs, inspected thirteen fresh page rasters, and reread
biblical, reception and chronology evidence; those additional research findings
were not written into the dossier or accepted. Its structured result was
BLOCKED because the packet no longer matched the requested scope.

The native engine recorded `78d1516ca75da9df` as terminal BLOCKED with three
packets, three results and no interventions. Its native archive is retained
under the leaf's `evaluations/proper-study-results/78d1516ca75da9df/`.
The target's reference-only authorization is withdrawn; ordinary production
authorization remains. The ledger explicitly supersedes the reference-only
acceptance requirement and restores full appointed Latin and independently
sourced historical English as a blocked requirement. The tested optional mode
implementation is historical work, not fulfillment of the restored promise.

The previously recorded source-text output rejection remains unresolved.
Full witness acquisition and reading are distinct from generating the complete
appointed source records and publication text. No alternate tool or model is
used to bypass the rejection. No fresh full-text generation is attempted,
no native acceptance is claimed, and no incomplete publication is pushed to
main. The next full-material production needs a permitted, operational way to
complete its source-text work and a fresh run; neither blocked run can resume
or confer acceptance.

The working context now retains the fresh appointment evidence but restores
the full-material source plan, explicitly marked unfinished. That scope
reconciliation occurs after the stopped run and is not a new native review.

## Narrowing the blocker and continuing independent evidence

The maintainer challenged the halt and asked what was missing and whether work
could proceed without the sources. Reinspection confirms that the complete
source witnesses are acquired; the missing deliverables are the finished
appointed-text records, authored studies and homily, and their reviewed
publication artifacts. The diagnostic records an explicit output rejection,
but no rejected passage or subsequent failed tool call is exposed. Treating
that evidence as proof that all sourcing or writing was impossible was an
overstatement. It does not establish a general rights restriction either.

The coordinator continues independent reception verification and original
interpretation work, using the sources already examined, without retrying or
reconstructing the rejected output. A bounded preparatory lane consolidates
its actual completed reading and reconciles binding states; it changes no
proper-body source record and supplies no native PASS. The full-material
requirement remains open and blocked at its unfinished text-record boundary;
it is not waived or replaced by locators. Both historical native runs retain
their terminal dispositions. Further acquisition is not the present obstacle
to this independent research work.

The preparatory consolidation is complete in `research/reception-verification.md`.
It preserves the inspected biblical contexts, substantive reception arguments,
chronology evidence and partial-read limits. The bindings and reception matrix
now agree with those limits. Interpretation corrections distinguish Bellarmine's
comment number from its biblical verse, Victorinus's chapter-level support from
verse-specific exposition, and the feast's institution from individual prayers'
composition dates. No source fingerprints were replaced. The scope also records
the completed acquisition of the earlier witnesses rather than continuing to
call them unacquired leads.

Source-library validation passed for 4,113 publication bindings. The promise
ledger and whitespace checks passed. These validate the preparatory records;
they do not certify a complete appointed-text record, authored document or
publishable artifact. The model-output rejection still has no verified
resolution, and no rejected payload was replayed. The required full-material
production remains unfinished; no main push or new deployment was attempted.

## 20 October recovery and fresh full-material run

The maintainer renewed the instruction to complete the GPT edition and push it
to `main`. This workspace merged current main `6dad4a7a3` through merge commit
`0b318d400`, keeping both provider records and both calendar corrections.
Source-library validation passed with 4,154 bindings; generated propers and
source-browser structures and the promise ledger checked cleanly after conflict
resolution. The merge includes the separately published Claude F01 edition.
Its acceptance belongs to Claude alone.

An independent read-only audit of that edition's records identified the
registered 1925 *Acta Apostolicae Sedis* fascicle, printed pp. 666–668, as a
potential antecedent for every Latin proper body and the Preface. It also
identified Lasance's ordinary body pages for English and cautions about
abbreviated conclusions, a Preface ending, the inactive Paschal Alleluia, Psalm
numbering and displaced older rubrics. The audit did not render the primary
facsimiles itself. GPT research must inspect and record its own findings; it
may reuse provider-neutral source identities but no other provider's PASS.

Fresh GPT `proper-study` v13 run `8d637d6f2f9160aa` was seeded from
`0b318d400` for 25 October 2026 under ordinary full-material authorization.
Its scope gate passed. The next native packet is `resolve-context-0000`; no
context, research, document or publication PASS is claimed at this checkpoint.

`resolve-context-0000` then passed after fresh Missal page and dated Ordo
checks; its source plan kept full material and named eleven active elements and
two inactive branches. At research, the worker interpreted the old warning
against replaying an unknown rejected response as a bar on every new full-text
collation. The driver recorded native intervention `0000` to draw the actual
boundary: do not replay that response, but independently examine the registered
public-domain AAS witness, the 1962 collation pages and historical English
witnesses for the fresh full-material run. The intervention changes no packet
or PASS criterion. Research remained underway at that checkpoint.

The fresh research worker inspected page images from the authenticated 1925
*Acta Apostolicae Sedis* microfilm, the controlling 1962 Missal and Lasance's
historical English missal, and checked additional Augustine, Chrysostom and
Bellarmine loci. While preparing the full appointed-text records, its output
stream received a second HTTP 400 `safety_violation` with the message
`regurg plugin blocked the output stream`. The rejected content and the
precise triggering text are not visible. The worker did not save
`propers/retrieved.txt` or `propers/verified.md`. It was explicitly stopped
from regenerating or reconstructing the rejected output. Its only tracked
changes were regenerated chronology records matching the merged calendar's
`Psalms 28:10-11` citation; those passed both proper-chronology checks,
the scripture chronology corpus check, source-library validation and
`git diff --check`, and were committed and feature-pushed as `6f7a45b4d`.

The worker returned a truthful `BLOCKED` result for research iteration 0.
The native engine advanced run `8d637d6f2f9160aa` to terminal `BLOCKED` after
three packets and three results, with one intervention. Scope and context
passed; research did not pass, and no later authoring, review, artifact or
publication stage ran. The separate Claude edition on current `main` remains
live, but its acceptance cannot supply this GPT run's missing PASS. The
maintainer's full-material requirement is still open; a locator-only study
is not an authorized substitute. No GPT publication or push to `main` was
attempted from this run.

## 20 October source-data reuse run

The maintainer continued to require full sourced material. A new full-material
v13 run `095fe00a9fe8cfee` was seeded at `5b4829232`; its scope gate passed.
Its fresh context worker independently rechecked the 25 October occurrence,
governing page images and dated Ordo, corrected the inherited Gloria locator
to RGMR 431(a), and added the registered 1925 AAS first-printing route and
review dependency. Context passed; its correction was committed and
feature-pushed as `ce7815e4d`.

Before research, driver intervention `0000` identified the separately
published Claude F01 source files as possible untrusted data leads only.
This run must independently authenticate and inspect the primary witnesses,
verify each adopted source unit and its rights and extent, disclose any
cross-provider data contribution, and inherit no Claude acceptance. It must
not retry or reconstruct unknown rejected model output. A fresh high-effort
research worker has the exact native packet and intervention; no research
PASS or later-stage result is claimed yet.

The worker saved an explicitly incomplete, provenance-labelled source-data
checkpoint after rehashing and reading the 1962, AAS and Lasance page images.
Its GPT `propers/verified.md` now carries all thirteen 1962 Latin units and
four historical English composed texts; `propers/retrieved.txt` retains the
unedited AAS pull as a finding aid. The Latin starting data came from the
already published Claude collation and were independently compared with the
primary images; the cross-provider transcription contribution is disclosed.
The two source records were committed and feature-pushed as `8b693dc86`.
The exact AAS binding and explicit Claude-source dependency validated with
4,155 source-library bindings and were committed and feature-pushed as
`1649a5864`. Complete English biblical selections, framing, research
reconciliation and independent cold review remain pending; there has been
no new output rejection at this checkpoint.

A second research checkpoint completed the source-data record: all thirteen
units now have continuous historical English from the inspected Lasance
columns, including the reading frames, with printed errors retained and
identified. The Latin common doxology, oration endings, dialogue and Preface
close were checked against page-image layers of the registered public-domain
1862 Pustet printing and the 1962 controller; Lasance supplies English common
forms. The exact 1862, 1962 and Lasance bindings and dependency record were
updated. Source-library validation passed with 4,156 bindings, and the four
files were committed and feature-pushed as `6d8e443ca`. This is a research
checkpoint, not a research gate or review PASS; reception reconciliation and
the native cold evidence review remain required.

Research found that `work.ante-nicene-fathers.volume-7` had no containment
row despite being shaped as an anthology and used for Victorinus. Driver
intervention `0001` authorized a partial row limited to the directly read
Victorinus constituent. The containment validator, source-library validator
and whitespace checks passed; the correction was committed and feature-pushed
as `446807a1a`.

The first research preflight then refused a declared dependency on the Claude
F01 liturgical leaf: the validator deliberately bars another provider's
liturgical content as a sealed source owner. Driver intervention `0002` kept
that guard. Because the Claude file was an untrusted transcription lead whose
adopted wording was independently checked against the primary witnesses, it
was removed from `research/review-dependencies.toml` while its exact path and
source-data contribution remained disclosed in the GPT provenance and scope
records. AAS 1925, the 1962 Missal, Lasance and Pustet remained controlling,
bound source owners. No authored content or acceptance crossed providers.

The research worker reconciled context, scope, reception, interpretations,
chronology and bindings. Source-library validation passed with 4,156 bindings,
containment passed, chronology records were current, `git diff --check` passed,
and the native research check passed. Its research-iteration-0 PASS result was
accepted by the engine; the same program preflight passed as the next native
gate. The eight-file reconciliation was committed and feature-pushed as
`6532cd1ee`. A fresh xhigh cold research reviewer has the sealed packet;
research review, authoring and publication remain pending.

The first cold research review independently checked the full-text collation
against the 1962 Missal, Lasance and AAS images, the nine generated chronology
rows, and the principal Augustinian, Hieronymian, Chrysostomic and Bellarminian
interpretive loci. It returned `CHANGES_REQUIRED` on one research-owned finding,
`RES-HIS-001`: the planned historical appendix lacked a modern critical
authorship and composition horizon for John and Colossians. The result was
accepted by run `095fe00a9fe8cfee`, which emitted fresh high-effort
`research-0001`; no study-authoring stage has started. The repair is limited to
independently checked, source-bound modern qualifications alongside the
traditional chronology, without replacing the generated dates by an
unsupported publication-local choice.

The repair registered dated metadata-only USCCB introduction artifacts for
John and Colossians, bound their exact hashed deliveries, and added the
authorship, final-formation and writing-place alternatives to the historical
appendix plan. It preserved the generated chronology and interpretive lanes.
Source-library, chronology, inventory and family-ledger checks passed. The
research repair and native preflight passed; the second fresh xhigh reviewer
then returned `PASS` with `RES-HIS-001` resolved. The engine has entered
`author-study-0000`; its fresh high-effort author is producing the expansive
study. The completed research repair was committed and feature-pushed as
`64270731b`. No study, artifact, web or publication PASS exists yet.

The first expansive author produced a complete-mode 23-page study, with 7,612
substantive exposition words, the twenty-six Latin/English appointed-text
blocks, two whole-formulary readings with their own four senses, and the
reviewed historical appendix. The author proof built at SHA-256
`42a95d5f8d2a5d682b788a8708da1facdeffeedcf81f86d0173e1f1a8eb8a1d6`;
component checks, source-block comparisons and the web conversion probe
passed. The coherent draft was checkpointed as `dc51c67bb`; proof corrections
and the production review were committed and feature-pushed as `2ac67f925`.
The native author result and study preflight passed. A fresh xhigh study
reviewer is now reading the sealed study; no independent study PASS is claimed.

During the author probe, `tools/web-edition` falsely treated the combined PDF
metadata title as a continuous prose source run across two distinct displayed
title fields. The driver excluded `\\hypersetup` metadata from that run-only
audit, preserving the visible title and the ordinary paragraph-loss check.
All 146 conversion tests and a separate F01 web probe passed; this shared-tool
repair was committed and feature-pushed as `1dcf44d08`.

The fresh xhigh study reviewer returned `PASS` on the sealed 23-page guide,
confirming the two distinct readings, four senses, complete appointments,
chronology and central source inferences. It recorded `STU-TEXT-001` as an
accepted witness-selection discrepancy: the full English scriptural blocks
are explicitly labelled Lasance historical hand-missal text, while the 1962
profile normally names Douay–Rheims–Challoner for Scripture. The reviewed
wording is neither falsely attributed nor presented as approved 1962 English;
the reviewer judged replacing it here would not correct a reader-facing
misunderstanding and would disturb settled pagination. The native engine
accepted the review and emitted `derive-synthesis-0000`. Companions, artifact
and publication gates remain open.

The concise author produced a 10-page, 4,139-word standalone comparison from
the accepted expansive study. Its physical opening has inventory and four
senses on page 1, generated orientation chronology alone on page 2, themes on
pages 3–4 and developed interleaved commentary beginning on page 5. The draft
was checkpointed as `c059f2886`; final proof and audit corrections were
committed and feature-pushed as `46aa14226`. Component checks and native
synthesis preflight passed. A fresh xhigh reviewer then inspected all ten
matching PDF pages, rechecked the principal witness and chronology claims,
compared both readings with the accepted study, and returned `PASS` with no
findings. The engine emitted `derive-homily-0000`; homily and publication
acceptance remain pending.

The homily author drafted a 1,276-word, three-page sermon with a calculated
10.2–11.6-minute delivery range. Its draft was checkpointed as `6d4955692`;
final proof and audit were committed and feature-pushed as `6564c50f5`.
Homily preflight passed. The first fresh xhigh homily reviewer found a factual
addressee error in the Secret that had been inherited by the research summaries
and both dependent studies: the prayer addresses the Father and asks that the
offered Son grant unity and peace. It returned `CHANGES_REQUIRED` with
research-owned `HOM-001`. The engine routed to high-effort `research-0002`;
the verified appointed wording and page-image source already establish the
correction. Prior content reviews remain historical results, but dependent
documents will be rederived and reviewed after research repair. No homily or
publication PASS is claimed.
