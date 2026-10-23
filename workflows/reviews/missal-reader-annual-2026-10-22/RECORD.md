# Annual Missal reader: source-repair phases

## Scope and state

The governing annual scope is Roman 1962 civil 2026 and the three complete
Postconciliar Missal liturgical years A/2026, B/2027 and C/2028, including each
Advent. The exact intervals and content-first ordering remain in
[`guidance/liturgy-browser-roadmap.md`](../../../guidance/liturgy-browser-roadmap.md#current-priority-complete-annual-minimum-reader-2026-10-20).
The annual promise remains open. A bounded source repair does not establish
correct or complete wording throughout any year.

Phase 1 is **accepted within its bounded source-repair scope**. Its base
is `a17f42c7e6ac61b51579784c4ee6e67108a70d47`. Independent source work was
separated from shared data generation, release bindings and integration checks.
No publication, default-branch integration or deployment is claimed.

## Phase 1: source changes

### Roman 1962: Boniface

The proper Postcommunion is restored from an independently retained Pustet
1862 witness, printed p. 445, PDF p. 531, right column. The complete three
prayers and conclusions were compared with the 1962 control at printed
p. 530, PDF p. 611, nn. 2598–2600. The Collect and Secret retain their previous
body bytes but now name the correct historical source. The historical and
editorial-projection passages record spelling differences separately.

The retained historical page has SHA-256
`883fb31d665d53a701a1d7a32012b6de3bf7d7ce4bfbaef235873595ea7bc9b6`.
The restored body has SHA-256
`5003e0531a176d0ce4d3d1dd0c3476e3a178d3355acbc09b08985dd2386be0c7`.
Direct Latin bodies rise from 1,108 to 1,109. The 491 Mass records and 3,730
direct Proper records remain unchanged.

The three unresolved Common-set choices remain explicit. In particular,
Boniface's printed Secret C 3 and Postcommunion C 4 do not authorize choosing
one uniform Common oration set. The local prayers override the inherited
orations; no missing petition was reconstructed from a Common blank.

Source owners:

- [`roman-1962/propers.yaml`](../../../src/sources/calendars/roman-1962/propers.yaml)
- [`Latin provenance inventory`](../../../src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml)
- [`historical page-image passage`](../../../src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/boniface-three-orations-page-image-2026-10-22.toml)
- [`1962 control passage`](../../../src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/boniface-three-orations-recheck-2026-10-22.toml)

### Roman 1962: Advent English

Eight checked Lasance/Walsh revised-1945 English bodies are added: Advent II
Secret and Postcommunion, and Advent III and IV Collect, Secret and
Postcommunion. Historical translation, target Latin correspondence and
publication remain separate assertions. This is not official English of the
1962 Missal.

The English source pages checked are PDF pp. 107–108, 110–111, 113–114, 131
and 133; the target comparisons use pp. 84–86 and 95–96. The bounded
transcription TSV has SHA-256
`a106d2a587ef20ccd75a28548d95ba35554a383e5cbc6a8fcf75e92e43ff6024`.
Held English rises from 123 to 131 of 1,427 represented slots; ledgered
untranslated slots fall from 1,304 to 1,296. These are represented-slot
counts, not whole-book or annual completion percentages.

Advent II Collect stays unserved. The historical page prints English
“Who livest.” beside Latin “Qui tecum.” Its checked wording is retained only
as evidence, with an explicit witness gap; no conclusion is silently corrected
or supplied from a different witness.

The [`English sidecar`](../../../src/sources/inventories/roman-1962-proper-translations-v1.toml)
and its source references own the exact target joins, eight publications and
one deliberately unserved prayer.

### Postconciliar Missal: Holy Week acclamation referrals

Holy Monday and Tuesday gain their source-established Gospel Acclamation roles
with unavailable bodies. Wednesday gains two non-cumulative referrals to those
roles, requiring explicit selection rather than selecting by source order or
cycle. All three Masses remain partial. Exactly two terminal English
`no-exemplar` rows belong to Monday and Tuesday; Wednesday adds no duplicate
absence owner.

The checked evidence is OLM 1981, artifact p. 194, printed p. 140,
nn. 257–259. The retained raster was reopened; a new full-PDF verification is
not claimed. Four Proper rows are added, no wording or translation is
published, and exact target-2008 correspondence remains unresolved.
Postconciliar English accounting becomes 511 represented slots: 113 held and
398 ledgered untranslated, with zero unaccounted, unmatched or stale rows.

Source owners:

- [`postconciliar/propers.yaml`](../../../src/sources/calendars/postconciliar/propers.yaml)
- [`postconciliar English sidecar`](../../../src/sources/inventories/postconciliar-proper-translations-v1.toml)
- [`OLM source passage`](../../../src/sources/works/catholic-church/ordo-lectionum-missae/editions/latin-editio-typica-altera-1981/passages/holy-week-acclamation-referrals-257-259.toml)

## Phase 1: checks and independent cold review

The pre-repair reader baseline ran 45 tests with two optional skips, exit 0.
`make check-deployment-sources`, `tmt check`, the promise ledger and the
zero-stale-binding check also passed before source repairs.

Focused implementation checks:

| Scope | Actual outcome |
| --- | --- |
| Boniface and related Common/source regressions | 21 tests passed, including eight new tests; exit 0 |
| Advent English and related regressions | 27 tests passed; exit 0 |
| Broader English overlay suite | 49/50 passed; one inherited diagnostic-expectation failure |
| Postconciliar pointer/referral/English suite | 15 tests passed; exit 0 |
| Expanded postconciliar regression suite | 26 tests passed; exit 0 |
| Holy Week CLI selection | 30 invocations across nine annual A/B/C dates, both languages and both Wednesday choices; all exit 0 |
| Calendar validators, source-library validation and whitespace checks after the lanes settled | Exit 0 |

The isolated overlay failure is proved at the committed base and in the
candidate: nine tests, one identical failure, zero errors. The fixture expects
`target owns no body`; the validator instead reports
`Scripture body absence requires an exact English rights-withheld body witness`.
It is not a new text-repair failure and was not hidden by changing its
expectation.

Two fresh, independent cold source reviews inspected the frozen Roman and
postconciliar increments, their source-page evidence, exact identities,
conclusions, rights boundaries, inheritance and regression behavior. Both
returned no actionable findings. A separate additions audit found no
actionable duplication, missing production consumer or misplaced owner.
The conventions review found one required correction in the new annual work
records: replace the book label “Novus Ordo” with the neutral
“Postconciliar Missal.” Both new labels were corrected without changing the
scope or completion criteria.

These are independent AI source/code reviews of the bounded phase, not
ecclesiastical approval or acceptance of the full annual reader.

## Phase 1: integrated validation and acceptance

| Gate | Outcome |
| --- | --- |
| Full annual structural matrix | Seven tests, 2,928 language states and 5,856 JSON/text renders; exit 0, 1,013.94 seconds |
| Native Chromium gate | Twelve harnesses, 257 assertions, no console/request/HTTP diagnostics; exit 0, 237.63 seconds |
| Deployment-source checks | Exit 0, 182.06 seconds |
| Local preview and public artifact build/verification | All four commands exit 0, including GitHub Pages target verification |
| Expanded reader/source regressions after expectation repair | 178 tests, nine optional skips, zero failures/errors; exit 0 |
| Census, source inventory, source-family ledger and release bindings | Current; zero stale bindings; 162 pending review units and zero screened, unchanged |

The broader suite exposed three obsolete corpus expectations. Their repairs
retain strict artifact, permission, hash and exact-target guards while accounting
for Boniface's restored body and the eight additional English bindings.
They do not change source text or runtime behavior. The full annual and native
browser runs apply to the same unchanged source/runtime inputs.

The local environment initially selected Markdown 3.11.2 instead of the pinned
3.10.3. Builds succeeded with the existing pinned scratch environment, without
dependency-file changes. A browser attempt with an overlong temporary socket
path was canceled and rerun successfully with a shorter workspace scratch
path. Neither failed attempt is represented as passing.

A fresh integrated cold reviewer accepted this bounded phase with no blocking
findings. Independent checks confirmed all 491 exact-Mass envelopes match their
full-structure objects, including 487 generation-only changes; all 40 frozen
source-packet paths match; source and census projections are current; and
exactly 505 existing bindings plus four new generated files were updated,
without unrelated authorization changes. The reviewer independently ran 108
source/expectation tests with six skips, 65 browser-model tests with three
skips, and twelve additional CLI invocations, all without failures.
Advent II Collect remains unserved, inherited pre-1955 Boniface Latin remains
withheld, and Holy Wednesday still requires an explicit choice.

This closes Phase 1, not the annual text promise. The complete annual
structural pass cannot establish correct or complete words.

## Phase 2: authorized next source repairs

After Phase 1 acceptance, the source freeze is released for three independent
bounded lanes:

- Eighteen Latin commemoration orations independently matched in full against
  historical and target pages. Ursula's unmatched Postcommunion remains
  excluded; no saint-name insertion is invented.
- Twenty-one exact full-Latin-and-conclusion reuses of eleven already-checked
  Cummiskey English bindings. These are new terminal target joins, not fresh
  page inspections or new translations. Advent II Collect remains excluded.
- Source-checked postconciliar ferial corrections: Lent III Monday's Psalm
  bounds, the conditional Lent V Monday Gospel, Advent I Monday's optional
  reading and Psalm block, and December 21's optional First Reading. Unknown
  actual-use conditions remain unknown; calendar cycles or user choice cannot
  attest them.

Each lane must finish focused validation and a new immutable source-review
handoff before fresh cold review. Shared generation and integrated acceptance
remain separate. The larger weekwide optional Lenten reading sets and contextual
Dedication Secret choices are not silently folded into these repairs.

The inherited overlay fixture's obsolete diagnostic expectation is corrected
in Phase 2 to require the current, specific Scripture-body witness error.
This retains the rejection of the wrong occurrence rather than weakening it to
any error. Its complete 23-test module passes, exit 0. The Phase 1 baseline
failure comparison above remains the historical record.

Phase 2 sanity checks also reproduce an inherited CLI/browser parity defect:
the shared adapter compares JSON object insertion order, rejecting otherwise
identical serialized source-path selections. The bounded integration repair
reuses the existing typed, order-independent appointment-fact identity logic
for the adapter's JSON comparisons. Object key order must not affect identity;
array order, exact fields and values, and raw guard presence remain enforced.
This shared-code repair requires focused positive and negative regressions and
fresh cold review in addition to the separate source reviews.

The two fresh source reviews accept the bounded Roman and postconciliar
changes without actionable findings. The conventions review also returns no
findings. The additions audit identified one duplicate calendar-index test
helper; it is removed in favor of the existing calendar owner.

The repaired adapter passes the real serialized CLI hook: 316 source-path
executions and 12 CLI cases, including reordered object keys and refused
reordered source-path arrays. A broader replay also exposed an inherited test
assumption that the first Ordinary registry witness covered every appointed
English element. The unchanged adapter reproduces that failure. The corrected
test preserves the actual mixed-witness coverage and requires explicit requests
for either incomplete witness to be refused, rather than weakening the
production guard or supplying substitute text. The complete reader-state,
overlay and focused ferial selection now passes 112 tests, exit 0.

These source and focused results do not constitute Phase 2 integrated
acceptance. Generated data, carried census blocks, release fingerprints, annual
renders, native browser checks, local publication gates and fresh integrated
cold review remain the next integration work.

The additional independent cold review of the shared adapter repair and parent
test corrections returns no actionable findings. The corrected sources,
adapter and tests are frozen for integration. Independent discovery may
identify the next source-backed repair batch, but it must not change the frozen
inputs before Phase 2 integrated acceptance.

### Phase 2 integrated validation and acceptance

Fresh canonical generation and the three carried census blocks are current.
All 491 Roman Mass envelopes match their canonical full-structure counterparts.
The 522 changed generated files contain the intended 36 semantic Roman Mass
changes in each Roman projection and four changed postconciliar ferials;
455 Roman envelopes change only their generation identity. The increment adds
exactly eighteen Roman 1962 Latin bodies, no pre-1955 Latin bodies, and
twenty-one English terminal joins. All 131 preceding English entries are
unchanged.

| Fresh check | Result |
| --- | --- |
| Source-library, calendar/source, inventory and census freshness | Pass |
| Parent reader/overlay/ferial regressions | 112 tests pass |
| Focused source/path regressions | 81 tests, one optional skip, pass |
| Expanded affected regressions | 178 tests, nine optional skips, pass |
| Real serialized CLI/source-path checks | 316 executions and 12 CLI cases pass |
| Static seating | 12 forms and 162 candidates pass |
| Complete annual structural matrix | Seven tests, 2,928 language states and 5,856 renders pass |
| Native browser gate | Twelve harnesses and 257 assertions pass |
| Deployment-source gate | Pass |
| Pinned local preview/public builds and artifact verification | Pass |
| Final release bindings | Zero stale |

The scoped binding refresh updates 506 existing hashes and adopts eighteen
new generated Latin fragments. The 1,030 changed rights-table rows belong
exactly to those 524 paths; authority and rights prose do not change.
Source-family refresh changes only the catalog fingerprints, retaining
162 pending families, zero screened families and no atomic-coverage claim.
Roman 1962 English coverage is 152 of 1,427 appointed slots, with 1,275
untranslated and zero unaccounted. Postconciliar English remains 113 of 511,
with 398 untranslated; its 374 non-scriptural Latin slots still have no
resident bodies.

The immutable integration packet is
`20261022T113946Z-missal-reader-annual-phase2-integration`, with sibling ZIP
SHA256 `601d34142d5640523e856b324c23e4c93824cd751b1b0ffe55c35216f8872d2d`.
Its Phase-2-only patch against accepted Phase 1 independently reconstructs
610 exact files, including 84 additions; directory/ZIP inventory, bytes and
CRC are verified. It includes no protected facsimile or private CLI body
payload. No commands remain running in the integration lane.

A fresh independent integrated reviewer accepts bounded Phase 2 with no
blocking findings. The reviewer verifies all 610 preimage origins, packet and
ZIP integrity, current input identity, generated semantic scope, release
authority, and unchanged family dispositions. Independent replay passes
131 tests, then 154 additional tests with seven skips, as well as the
316 source-path executions, 12 CLI cases and 162 seating candidates. A fresh
real CLI payload matches the tested payload. The expensive annual and native
runs are not repeated by the reviewer; their frozen log hashes and current
inputs are verified.

Phase 2 is accepted and its implementation freeze is released only for the
next explicitly selected source batch. These checks establish neither annual
textual completeness nor publication: no commit, push or deployment occurred.

## Phase 3, selected source batches

The next English increment covers twenty-one terminal owners using seven
newly checked Lasance prayers: Common Virgin III Secret and Postcommunion,
Common Confessor-Bishop I Secret, Common Plural Martyrs I Postcommunion,
Paschal Martyr Postcommunion, Fifth Sunday after Easter Postcommunion, and
historical Holy Saturday Secret as an exact witness for the Easter
Sunday/Monday target prayers. Whole historical Latin and actual conclusions
must match the checked target seed; reuse across terminal owners additionally
requires literal complete Latin-and-conclusion equality. This is not permission
to transpose other Holy Saturday material or invent a conclusion.

The twenty-one owners support sixty-six appointment references, not sixty-six
independent owner bodies. Eleven other candidates with unresolved mismatches
remain excluded. The current checked donor pool offers no further exact joins
without acquiring or checking additional historical English. The planned
English census increment is 152 to 173 of 1,427, subject to validation and fresh
cold review. No implementation or annual acceptance is inferred from discovery.

The selected Latin increment adds nineteen checked owner bodies across
Bibiana, Sabbas, the Stephen/John/Holy Innocents octave entries, Thomas of
Canterbury, and Ursula's Postcommunion. Seventeen fill unowned gaps; two
restore removed Collect owners. The full Ursula petition, including its names,
is witnessed by Mame 1922; the insufficient 1862 witness remains insufficient.
The other bodies use checked Pustet 1862 pages. Bibiana's printed name blanks
and every actual target conclusion length must remain explicit; Sabbas's
Secret ends exactly `Qui tecum.` No mixed-facsimile English permission is
generalized into new Latin rights.

The same Latin owner may implement the independently probed, role-only
Dedication split for the Lateran and Peter/Paul basilica entries: four existing
Collect/Postcommunion appointments become resolvable without new bodies or
ledger rows. The two context-dependent Secrets stay unresolved. No church
identity, actual-dedication occasion, ExtraPaschal branch or chant fact is
inferred, and no shared resolver change is authorized.

The selected postconciliar increment adds the complete optional weekday
reading courses of OLM 1981 nn. 236, 243 and 250 to all eighteen Lent III–V
weekdays. Each is a coupled First Reading, Psalm, Verse Before Gospel and
Gospel course; Sunday Second Readings and shortened Sunday Gospels are not
imported. All A/B/C cycles are eligible. The B/C Sunday-nonuse direction is a
preference, not an exclusive eligibility condition or an attested actual-use
fact. Weekday oration compatibility is not asserted.

This adds seventy-two local nodes: fifty-three Scripture-reference nodes and
nineteen composed owners, including an explicit unavailable ferial Verse Before
Gospel for Lent V Tuesday. All eighteen optional acclamations occupy occurrence
two; that Tuesday ferial gap occupies occurrence one. Adapted acclamation
citations remain notes, not literal Bible-body substitutes. No acclamation
text, incipit or translation is published. Their Latin held-unpublished states
retain exact source evidence, while nineteen owner-scoped English
`no-exemplar` rows claim no English rights-withheld witness. The validated
proposal changes postconciliar English accounting from 511/113/398 to
530/113/417 total/available/untranslated, with zero unaccounted. These are
planned changes until implementation checks pass.

The existing Lent V Monday Gospel relation must become one coherent course
without overlapping owners, preserving both Daniel forms and its actual-use
conditions. Unknown source facts stay unknown and must not block the
independently permitted optional course. The same lane corrects Lent III
Tuesday's Psalm start to Vulgate 24:4bc–5ab rather than full verse four
(OLM n. 238). No shared resolver change or implicit stale-choice fallback is
authorized. Source compilation, language accounting, exact pericope bounds,
complete-course admission and displaced-date controls require fresh tests.

### Phase 3 implementation checks, acceptance pending

The Roman English and Latin/Dedication lanes have completed their source
changes and immutable source-review packets. Roman English is 173 of 1,427,
with 1,254 untranslated; pre-1955 inherited English is 160 of 1,378, with
1,218 untranslated. The Latin increment has exactly nineteen bodies and four
role-only appointments, with both Dedication Secrets unresolved. Its ledger
has 1,248 owners, 1,224 permitted/present, 24 removed and 20 unresolved
provenance records. These are source-model counts, not annual completeness.

Parent sanity checks update the Phase 2 English test's two current census
tuples and the newly stale Dedication zero-orations expectation. The same
reference module contained seven previously failing assertions, reproduced
against accepted Phase 2. They are repaired to check the existing explicit
unavailable own Collects, the correct non-bishop Doctor Common for Lawrence,
two already-declared qualified aliases, and appointment-local Paschal
disposition. The strengthened checks retain exact non-Collect Common wording
and terminal provenance, absent Collect bodies, both unresolved Dedication
Secrets, and all twenty-nine Supreme-Pontiff referrals. The complete reference
and Phase 2 exact-English-reuse modules now pass 98 tests, exit 0. No source or
resolver behavior was changed to satisfy those expectations.

The postconciliar course lane is implemented: seventy-two added nodes,
nineteen composed unavailable owners, English 530/113/417 with zero accounting
errors, unchanged 329 Latin ledger owners and no new publication permissions.
All 601 other Mass blocks are byte-identical. Its twenty focused tests pass,
alongside 114 retained and 564 new admission executions, 206 negative controls,
158 additional refusals and eighteen framed static forms. Broad source-path
checks pass 752 executions and twelve mandatory serialized CLI cases; static
seating passes 29 forms, 336 candidates and ninety paths. The inherited Lent
II adjacency-test failure is reproduced on accepted Phase 2; it is not
silently counted as a passing check.

The immutable source packets are:

- `20261022T121540Z-roman-1962-lasance-commons-easter-phase3`,
  ZIP SHA256 `640010702da54f7af476b5e8a5a8efb364ce507e6890a72366ed1b2360a09768`.
- `20261022T121941Z-roman-1962-phase3-winter-ursula-dedication`,
  ZIP SHA256 `fedcc703e428c4c1c398ff848e663f6dea782885662094d286059ec862c294da`.
- `20261022T123134Z-postconciliar-phase3-ferial-courses`,
  ZIP SHA256 `be7063dd91af719b6121b52a55f728608211126ebb28abdf201b1009324e3a30`.

Each contains the complete phase-only patch, exact accepted-Phase-2
preimages, every new file, source evidence, check receipts and independently
verified reconstruction/ZIP bytes. Restricted controls are not redistributed.
The fresh Roman source and parent-guard review, ferial source review,
repository-conventions review and additions audit all return no findings.
The bounded source phase is accepted for integration. All source, runtime and
test inputs are frozen while the integration owner regenerates derived data,
refreshes only scoped release hashes and catalog fingerprints, and replays
the complete annual, native-browser and local-publication gates. Phase 3
integrated acceptance still requires its own fresh cold review.

The independent next-batch investigation identifies the inherited Lent II
failure as a stale adjacency assertion, not an appointment regression. OLM
1981 artifact p. 74 / printed p. 20, nn. 25–27 supports the full C reading
Philippians 3:17–4:1 and its C-only shorter form, 3:20–4:1. Both accepted
predecessor and current Mass objects retain that shorter reading before the
unavailable composed acclamation. A prospective test-only correction passes
all four tests in memory, including exact full/shorter references and every
existing body, rights and Bible-negative assertion. No tracked test has yet
changed during the integration freeze. After the integration owner confirms
all gates finished, that exact test-only correction is applied and all four
tests pass against the tracked file. Every preceding body, rights and
Bible-negative assertion remains. The final handoff is being updated to
capture the correction; no source or runtime change accompanies it.

### Phase 3 integrated validation, cold acceptance pending

Canonical generation, strict source-reader generation, calendar/source and
source-library checks, all three census blocks, final inventory and bindings
pass. All 491 Roman envelopes match the full canonical structure: 435 change
only generation identity and 56 change semantically. Both Roman projections
have 56 semantic Mass changes; postconciliar has exactly eighteen. The 524
generated changes contain nineteen new resident Roman Latin bodies and four
existing Dedication appointments, with no pre-1955 Latin additions. Twenty-one
English owners produce 66 inherited translation fields in each Roman
projection. These field counts are not owner or annual-completeness counts.

Fresh parent guards pass 98 tests; prior regressions pass 112; Roman focused
regressions pass 38; the affected ferial/psalm selection passes twenty. Python
source paths pass 41 tests with one optional skip. Expanded regressions pass
178 tests with nine optional skips. Mandatory serialized CLI/source-path
checks pass 752 executions and twelve CLI cases; seating passes 29 forms,
336 candidates and ninety paths.

The complete annual structural matrix passes seven tests, 2,928 language
states and 5,856 renders. Native browser testing passes twelve harnesses and
257 assertions. Deployment-source checks, pinned local preview/public builds
and artifact verification pass. No browser/server process remains owned.
The initial stale fingerprint and binding checks are resolved by the scoped
owner refreshes; final bindings report zero stale.

Release changes are exactly 507 existing hash updates and nineteen new
generated Latin fragments, 526 paths and 1,033 rights-table rows. Authority,
rights and policy prose remain unchanged. Family refresh changes only the
two catalog fingerprints, retaining 162 pending and zero screened families,
with no atomic-coverage claim. The annual promise remains open.

The first immutable integration packet,
`20261022T130441Z-missal-reader-annual-phase3-integration`, independently
reconstructs 626 changed files against accepted Phase 2. Its sibling ZIP
SHA256 is `f6e7285a8ad5e9746b872bb9f9c3cc9a890432bb2e1501041fe6e5839732e429`.
It retains the formerly failing Lent II test; a new immutable packet will
supersede it with the now-passing test correction. The old packet is preserved.
Unchanged source/runtime and annual/native input identities must be verified
before reusing those expensive results for final cold review.

### Phase 3 conditional-Gospel correction, acceptance reopened

The final test-only repack is created and independently verified:
`20261022T132636Z-missal-reader-annual-phase3-final-integration`,
ZIP SHA256 `7bd4a1ffed4e5cddde74eb4f292510fefe3e2611b3bb30c2268ad17cd44a8074`.
Its 627 changed files reconstruct exactly against accepted Phase 2. All four
Lent II tests pass freshly. The 524 generated files, 91 source snapshots,
23,443 bound site-source hashes and 33 original gate-log hashes match their
observed integration inputs, so the repack correctly distinguishes reused
annual/native/build evidence from newly executed narrow checks. It is preserved,
but does not establish integrated acceptance.

Subsequent Easter-course discovery exposes a concrete source inconsistency.
The parent independently reads the held OLM 1981 images at artifact pages
36–37, Praenotanda n. 81; page 192 / printed 138, n. 251; and page 205 /
printed 151, n. 279. The two local conditional-alternative structures agree,
and n. 81 treats repetition or replacement of a nearby Sunday/weekday text
as a pastoral choice. Neither supplies a condition excluding the principal.
The current n. 251 relation wrongly requires a false actual-use fact before
admitting John 8:1–11 in C.

The authorized Phase 3 correction removes that unsupported restriction from
the two C principal paths, while retaining both Daniel forms and the complete
optional n. 250 course. John 8:12–20 remains conditional on C and explicit true
actual preceding-Sunday use of John 8:1–11. True permits either native Gospel;
false excludes the alternative; unknown never licenses the alternative but
does not exclude an explicitly selected principal. No choice, date or cycle
attests actual use. There is still no default for unresolved choices or alias
for the retired Gospel-only selectors.

Only the postconciliar source, source evidence and affected test lane is
reopened. Roman source inputs remain frozen. The correction adds no body,
translation, permission or compiler feature. The source record must correct its
earlier exclusive-branch claim, with primary guidance and regression evidence.
Because this changes a consumed calendar input, the preceding annual/native
and publication results cannot certify the corrected candidate: regenerate
through the owners and repeat the integration gates, then obtain fresh source
and integrated cold dispositions. The Easter n. 279 implementation and all
Phase 4 candidates remain unauthorized until bounded Phase 3 acceptance.

The correction is implemented and independently accepted for integration.
Its new immutable source packet is
`20261022T135012Z-postconciliar-phase3-ferial-source-correction`,
ZIP SHA256 `81c0447a2971e4b667ef6dc2c200108655842648432e5483555e8c52feb27a2d`.
The full eleven-path ferial patch reconstructs against accepted Phase 2;
the separate nine-path repair patch reconstructs against the frozen final
Phase 3 snapshot. They are alternative bases, never cumulative patches.
Both independent replays match every candidate byte.

Both C principal paths now lack the false-fact restriction. Both conditional
alternatives retain explicit true and optional standing. Corrected source-basis
and passage narratives retain the primary-rule evidence. All 618 other Mass
blocks are byte-identical to frozen Phase 3; the eighteen-Mass overall phase
scope, 72 added nodes, nineteen held-unpublished owners, English 530/113/417
accounting and 329 Latin ledger rows remain unchanged. Shared runtime,
Roman inputs, language ledgers and the parent Lent II guard are untouched.

The complete affected Python selection passes 21 tests; the wider selection
passes 69 tests with one predecessor-dependent skip. Paired admission,
truth/choice/hybrid controls, 752 broad source-path executions and twelve real
CLI cases pass; seating remains 29 forms, 336 candidates and ninety paths.
Both Python and both CJS oracles reject the actual old calendar. Eight further
CLI cases give five expected successes and three expected refusals. Existing
Psalm and predecessor-access limits remain disclosed, not silently waived.

Fresh independent source review returns no findings after reopening the actual
n. 81 and n. 251 page images and independently replaying the 21-test selection,
both old-calendar CJS controls, broad CLI/seating, calendar and source-library
checks, packet identities and source accounting. Separate fresh conventions
and additions reviews also return no findings. The corrected inputs are now
frozen for regeneration and fresh annual, native-browser, source and local
publication integration gates. A new final snapshot and fresh integrated cold
acceptance remain required.

### Phase 3 corrected integration and acceptance

All corrected integration gates pass freshly. The seven-test annual matrix
renders 2,928 language states and 5,856 outputs; the native gate exercises
twelve harnesses and 257 assertions. Deployment-source validation, pinned
preview/public builds and both local artifact verifications pass. These are
new executions after the consumed calendar correction, not reused earlier
passes.

The corrected selections pass 98 parent, 113 prior, 38 Roman, 21 ferial,
69 wider-source tests with one skip, four Lent II tests, 41 source-path tests
with one skip, and 178 expanded tests with nine skips. The 752 broad executions,
twelve serialized CLI cases, 29 seating forms, 336 candidates and ninety paths
pass. Eight additional CLI cases yield five expected successes and three
expected refusals. Of 46 completed commands, 41 exit zero; two preparatory stale
checks are resolved by their owner refreshes, and three CLI refusals correctly
exit two. Optional skips and corrected scratch-harness setup errors remain
disclosed in the receipts.

The immutable corrected integration packet is
`20261022T143150Z-missal-reader-annual-phase3-corrected-integration`;
its sibling ZIP is created and independently verified, SHA256
`173fe5dc7fe9b5c59691fc2ccfd401c7316eb9f387b172983195e5e984cac154`.
Its 628 changed files comprise 532 modifications and 96 additions against
accepted Phase 2. There are 524 generated files and 92 source snapshots.
All 491 Roman envelopes remain canonical and unchanged from the prior Phase 3
snapshot; the corrected product delta is confined to Lent V Monday.
Overall Phase 3 still changes 56 semantic Masses in each Roman projection and
eighteen postconciliar Masses. Release scope remains 507 existing hash refreshes
and nineteen lawful Latin fragment adoptions; the correction refreshes one
existing binding and adopts none. All 23,443 bound site hashes match, and
authority, rights and policy prose remain unchanged. Family state remains
162 pending, zero screened and no atomic-coverage promotion.

A fresh independent integrated review accepts this exact corrected snapshot:
no blockers and no findings. It independently reconstructs all 628 files,
the three parent repairs and fifteen-file correction delta; checks all 749
candidate path identities and all 46 command/log receipts; and passes 161
current Python tests with zero skips, 752 wire executions, seating and eight
repair CLI cases. Both old-calendar CJS controls fail as intended. The reviewer
also reproduces the inherited reference and Lent II failures and verifies the
preserved source, language, rights and no-fallback boundaries. It validates
the expensive fresh parent annual/native/build results by their exact inputs
and log identities rather than claiming to rerun them.

Bounded corrected Phase 3 is accepted. The accepted snapshot is the sole
Phase 4 comparison base; older immutable pairs remain preserved. This closes
neither the annual promise nor missing-body, rights, Common-witness or edition
questions. No staging, commit, push, deployment or history change occurs.

## Phase 4, selected source batches

The Latin lane may implement twenty-three complete source-checked petitions:
twenty-one new ledger owners across Venantius, Anne, Felix/Simplicius/Faustinus/
Beatrice, Sabina, Nicomedes, Euphemia/Lucia/Geminianus, Jerome, Bruno, Francis
Borgia and Callistus, plus restored Alexander/Eventius/Theodulus and Hilary
Postcommunions. Pustet 1862 and Mame 1922 supply independent lawful whole
witnesses; actual 1962 conclusions and explicit name-blank instantiations remain
source-local. Juvenal occurs in the complete Alexander petition and is retained.
No held Holy Week, Albert, Silvester, Doctor addition or unknown Dedication
Secret is cleared by analogy.

The same owner corrects exactly two existing Common Virgin II tokens:
Collect `mine` to `Domine`, Secret `mentis` to `meritis`. Fresh Pustet pages
698–699 and 1962 pages 838–839 establish both whole prayers and short endings.
The Collect's real historical `extitit` versus received `exstitit` spelling is
declared, not mislabeled OCR damage. Keep `N.` and all other canonical bytes.
A new bounded two-prayer projection and fresh source/target bindings preserve
the old shared artifact and all 43 old passage records. The historical Latin
rights anchor is independent of Lasance English nonrenewal. These corrections
are count-neutral; twenty-three bodies would yield 1,269 ledger owners,
1,247 permitted/present, 22 removed and 180 form-aware literal gaps. These
prospective counts are not annual completeness or pre-1955 target attestation.

The independent English lane may bind thirty-one terminal owners: thirty from
nineteen newly image-checked Lasance prayers, with each of twenty-two actual
1962 seed groups separately compared, and one exact reuse of the existing
Cummiskey Marian-Saturday Communion at the Nativity of Mary. Every recipient
requires complete literal Latin-and-conclusion equality, not an incipit or
shared saint name. All 173 prior entries remain unchanged. This would give
204 of 1,427 English owners. Two additional Common Virgin II translations may
be attached only after independent source acceptance of the corrected Latin
bodies and hash bindings; they would give 206, subject to actual validation.
The freshly re-read, verbatim Common Collect supersedes an earlier excluded
scratch paraphrase. Both historical English endings and `N.` remain exact.
Pre-1955 effects and actual reference counts must be derived, not assumed.

The postconciliar lane audits the eighteen Easter II–IV ferial reading courses
against OLM nn. 267–284, artifact pages 201–206 / printed 147–152. Preserve
the 54 independently checked Reading/Psalm/Gospel owners. Add n. 279's
John 10:11–18 only in A with trusted actual preceding-Sunday use of John
10:1–10; the principal remains eligible, including unknown actual use.
Retain explicit choices, no attestation from date or selection, and no
resolver extension. Add n. 272's missing uncited composed acclamation as a
proper-body unavailable owner and English no-exemplar, not a Bible substitute.
Audit the other seventeen acclamations from their actual source; correct
any demonstrated adaptation/composition misclassified as a literal Bible body,
with exact Latin evidence and separate English availability, no fabricated
body hash or new publication permission. Derive the resulting accounting.

Seven independently proved exact John 6 maps may enable their corresponding
modern-numbered Bible addresses, keeping all Vulgate carriers unchanged.
The exact-reference keys also affect the source-checked Sunday B Gospels at
OT XVII, n. 110 / artifact 117 / printed 63, and OT XXI, n. 122 / artifact 122 /
printed 68. The selected scope therefore includes nine raw Gospel owners,
not seven alone. Do not flip the whole chapter or use a derived addressing as
a divergence-target key. N. 276's split endpoint remains unproved by an
independent complete Lectionary terminal body and is not activated. Retain
the three Psalm and one CPDV refusals, and Acts 8:37 absence in WEB Catholic
and RV1895 as a whole-passage refusal.

These three lanes have disjoint source and test ownership. Capture the
accepted Phase 3 preimages before any edit; leave global generation, census,
release bindings and family refresh to integration. Each lane requires new
source sanity and cold review, then full integrated validation and a fresh
immutable acceptance packet. The authenticated 2008 Common-form witness gap,
remaining rights questions and annual textual completion remain open.

### Initial source candidates and cold-review findings

The initial Latin candidate changes 73 paths, six modified and 67 added.
Its 297 tests pass without skips; source-library, calendar, accounting,
registry and whitespace checks pass. Its immutable source packet is
`20261022T152056Z-roman-1962-phase4-latin25-source`. Independent source review
replays all 73 postimages and checks the whole historical and controlling
prayers, but blocks the twenty-three-body tranche on two findings:

- Jerome's Postcommunion, controlling PDF 753 / printed 672 / no. 3741 P
  and Pustet PDF 637 / printed 551, ends only `Per Dominum.` The candidate
  incorrectly expands it and attests that expansion in its evidence and test
  oracle. An independent source-derived regression exposes the error.
- Anne's Secret, Pustet PDF 586 / printed 500, has `mater extitit`; the
  controlling PDF 684 / printed 603 / no. 3181 and canonical body have
  `mater exstitit`. Keep the correct canonical spelling and declare the real
  transformation in the linked evidence and normalization account.

Both findings are independently confirmed from the page images. Correction,
updated dependent hashes and fresh source re-review are required; passing
mechanical tests does not clear them. The initial packet remains preserved.

The same independent review separately accepts the two Common Virgin II
corrections, their bounded projection and current hash bindings. It confirms
the whole prayers and short endings, declared historical spelling difference,
unchanged old artifact and 43 old passages, and 41 retained shared bindings.
This satisfies only the Latin prerequisite for the two Common English
translations. Their attachment is now authorized; English source acceptance
and whole-Phase-4 acceptance remain separate.

The first English candidate implements 31 terminal bindings across 81 paths,
four modified and 77 added: thirty Lasance bindings and one Cummiskey reuse.
It preserves the 173 prior English entries and bindings and 693 prior source
files. Its 10 focused and 89 retained tests pass, as do source and calendar
checks. The immutable source packet is
`20261022T153216Z-roman-1962-english31-phase4-source`. Its full census check
still fails three generated carried-block subtests, with six optional skips;
global regeneration remains deferred until source integration. Source review
is required, including the separately authorized two-binding supplement.

Fresh independent source review accepts those 31 English bindings without
findings. It reopens all nineteen historical prayers on seventeen pages,
separately compares the twenty-two target seed groups, checks all 31 literal
recipient joins and rejects 186 negative mutations. It does not claim a new
Cummiskey page inspection. It also accepts the two fresh historical Common
English exemplars and rejects the older Collect paraphrase; the new attachment
and coherent 33-binding candidate still require review.

### Easter source candidate

The Easter lane implements ten source/test paths, six modified and four new.
Its immutable packet is
`20261022T154627Z-postconciliar-phase4-easter-source`. Both isolated replays
reproduce all ten postimages. Independent source acceptance remains pending.

The existing n. 279 alternate is migrated into the explicit conditional
relation, not duplicated. Only n. 272 adds a proper node, yielding 619 Masses
and 3,514 raw propers. The principal John 10:1–10 remains eligible in all
cycles, including true or unknown preceding-Sunday use; the alternate
John 10:11–18 requires cycle A and the explicit trusted actual-use fact.

The source audit classifies fifteen existing acclamations as adapted units,
retains the two Matthew 4:4b quotations as Bible citations, and adds the
missing uncited n. 272 composition. The sixteen composed owners remain
unavailable, with held Latin evidence and English no-exemplar records:
546 English slots, 113 positive and 433 untranslated, with no accounting
errors or English rights-restricted exemplars. No Latin ledger row or
publication permission is added. Exact independent Latin wording for the two
Matthew quotations remains unestablished; the Bible projection does not
claim exact liturgical wording or an approved translation.

Seven exact John 6 map keys serve all nine selected raw Gospel owners.
The two Sunday-B raw blocks remain unchanged; their source and material-cycle
identities are checked as consumers. All 54 core reading owners, 36 entrance/
Communion owners, 37 Vulgate carriers and 28 other mixed John 6 projections
are preserved. The n. 276 endpoint and other specified refusals remain held.

The lane reports 140 Python executions covering 136 distinct tests, with
135 passing and one disclosed optional skip; 768 broad wire executions and
30 seating forms / 343 candidates / 92 paths pass. Thirteen serialized CLI
captures succeed and the unproved alternate is refused with expected exit 2.
Calendar, source-library and registry checks pass; generated structure
checking still exits 1 for two stale projections, deferred to integration.
These are source-candidate results, not integrated or annual acceptance.

### Corrected source acceptance and whole-phase review

The corrected Latin packet is
`20261022T160217Z-roman-1962-phase4-latin25-corrected-source`, sibling ZIP
SHA256 `f38d554214a6bdddff04543550378b9fce806c927056f9cf1b09f8e30b2db1c3`.
It preserves the initial packet and contains separate, alternative full and
correction-only patches. Independent re-review covers all 35 correction
hunks and reconciles all 73 final postimages, retaining the earlier 25 whole
primary inspections. Both findings are resolved: Jerome retains only the
printed short conclusion, with coherent dependent hashes and bounds; Anne's
canonical body is unchanged and its actual spelling difference is declared.
Common2 remains byte-exact. The source reviewer accepts the other 23 and
therefore the complete bounded Latin25 tranche without new findings.

The author reruns 297 tests successfully. Independent re-review runs the
35 tests in the five modified modules, the original one-test primary-ending
regression, transport, preservation and source-correction audits, source and
calendar validators, registry and whitespace checks successfully. It does not
claim a second independent rerun of all 297 tests. Both alternative patch
replays reproduce the same 73 final postimages.

The final English packet is
`20261022T160214Z-roman-1962-english33-phase4-source`, sibling ZIP SHA256
`0170998440ff39f3b3ddb904a5b80a4002448d226cf1198c0a2fa2ecb1be94df`.
Fresh attachment review accepts both new Common owners and coherent English33
without findings. It covers all fourteen supplement paths, reconciles all
ninety full-phase postimages, preserves the prior 204 entries and bindings
and reuses the primary inspections only after preservation checks.
The final increment is 33 owners / 72 appointment references in each model:
Roman 206 of 1,427 English, 1,221 untranslated; pre-1955 193 of 1,378 English,
1,185 untranslated. All English accounting-error counters are zero. Eight new,
ten prior and 89 retained tests pass independently; the three known carried
Postconciliar census-block failures and six optional skips remain disclosed
pending integration.

Independent Easter review accepts all ten owned postimages without findings.
It reads all eighteen OLM acclamations and both shared Sunday-B appointments,
checks all seven maps across nine consumers and all seven held Bible editions,
and repeats focused, regression, wire, seating and serialized CLI checks.
The sixteen held complete bodies, two unresolved exact Latin quotation
identities, n. 276 endpoint and other specified refusals remain explicit.

The whole-phase additions audit covers all 173 disjoint source paths and
three parent-document deltas. It inventories 3,945 additions or existing-schema
field occurrences, runs 655 repository searches, traces generic source,
binding and ledger readers and returns no findings. Whole-phase conventions
review and fresh integrated annual, browser and publication gates remain
required. These source decisions do not accept Phase 4 integration or close
the annual promise.

The whole-phase conventions review covers all 173 source paths, 253 textual
hunks, three binary historical extracts and the three parent-document deltas,
including the final source-acceptance appendices. It finds one mandatory
departure: n. 272's newly added `name: Gospel Acclamation` is unquoted.
`guidance/sources.md` requires every liturgical name scalar to be quoted,
even when its present punctuation parses safely. The rule and exact changed
line are independently confirmed. Only that new name is to be corrected;
inherited entries are outside this fix. A new immutable Easter packet,
whole-YAML semantic-identity proof and bounded re-review are required.

The conventions review's completed source, calendar, registry, promise and
whitespace checks pass, as do fourteen Latin and eighteen English tests.
Its separate combined Python attempt times out without a result; an invalid
JavaScript invocation also times out after omitting required fixture input
and encountering stale generated structures. Neither attempt is a passing
gate. The correctly invoked source-group wire checks remain separately
recorded; integration must run fresh correct invocations after regeneration.

The one-name correction is sealed in
`20261022T164258Z-postconciliar-phase4-easter-name-quote`, sibling ZIP SHA256
`fb7b6424995d6ff7e52488165f6c8ae667f87436d432330a00a53f405104ff26`.
The earlier Easter pair remains immutable. Independent bounded re-review
confirms exactly two added quote bytes, identical typed YAML, canonical
semantic JSON and production structure, all other nine Easter files unchanged,
and all 163 Latin/English files matching their accepted packets. Both exclusive
patch alternatives replay exactly and ZIP CRC/inventory checks pass.
The author runs 23 fresh focused tests and source validators successfully;
the reviewer checks those logs without claiming an independent rerun.

The conventions finding is resolved and the whole-phase source-conventions
gate is accepted without remaining findings. Retained Easter primary and wire
evidence applies through the independently reproduced semantic-identity
bridge; it is not described as freshly rerun. All three source groups and the
conventions/additions gates are now accepted for integration. Full fresh
generation, census, annual, native-browser and publication gates and a new
independent integrated cold review remain required.

### Phase 4 integrated validation and acceptance

Bounded Phase 4 is accepted after fresh independent integrated cold review,
with no findings or blockers. The complete candidate has 713 changed paths:
173 accepted source paths, 537 owner-derived paths and three parent-document
deltas. There are 531 modifications and 182 additions. All 491 Roman envelopes
are canonical: 429 generation-only changes and 62 semantic changes. Each
Roman model's 62 changed Masses is exactly the source-owner fanout. The twenty
semantic postconciliar Mass changes comprise sixteen changed raw Masses and
four unchanged-raw map consumers: Easter II Friday, Easter III Monday, OT XVII
and OT XXI. Those four change only the Gospel's modern citation/refusal fields;
their Vulgate and other Mass fields remain exact.

Fresh integration commands pass:

| Gate | Result |
| --- | --- |
| Full annual matrix | Seven tests, zero skips; 1,464 coordinates, 2,928 language states, 5,856 renders; 972.284153 seconds |
| Replacement native browser gate | Seven tests, twelve harnesses, 257 assertions; zero skips/timeouts; 235.529606 seconds |
| Deployment-source gate | Exit 0; 182.706132 seconds |
| Public and preview builds | Both exit 0; 24.514988 and 24.999480 seconds |
| Public and preview artifact verification | Both exit 0; 21.413294 and 21.439911 seconds |
| Generated data, census, family and release bindings | All owner checks pass; zero accounting errors |

The first native execution starts before the final preview build finishes and
therefore does not establish final-preview freshness, despite passing its
assertions. It remains labeled freshness-unproved. The replacement runs from
17:37:30.594906 to 17:41:26.124508 UTC, after the preview build completes at
16:59:15.110914 UTC. All 932 frozen input hashes and 23,935 preview files remain
identical before and after. Twelve fresh browser profiles are cleaned, with no
owned jobs remaining and no unexpected console, request or HTTP diagnostics.
The harness contracts intentionally mix source-served and preview-backed routes
with controlled fixtures; this does not claim all assertions consume built HTML.
Concurrency evidence comprises preflight inspection, the frozen execution window
and unchanged inventories, not continuous process auditing.

The independently accepted full directory is
`.scratch/agent-handoffs/20261022T174442Z-missal-reader-annual-phase4-settled-native-integration`;
its sibling ZIP is created and verified, SHA256
`10282d8cd03dd5253485b6336670e303a2fee1030a9e68301ea6b323309e1293`,
34,553,002 bytes and 1,669 files. Inventory SHA256 is
`1c647a03517adc3ef76f46645ecc7c42ad747fb9176b08a366de76fbc11d662f`;
patch SHA256 is
`fd4f52b5cc0b54bfce032d3fc47cd18d4137e59636408a37c7c8fa5a2ae87c31`.
The independently verified native log SHA256 is
`d6545a4ebb9a0f5c57f2213dbacd6c2db97daca6b215f56652f71ae0f5076abc`.
Earlier integration directory/ZIP pairs remain immutable. The new packet keeps
all 79 original command records and adds the replacement native record. Resolved
pre-refresh failures, scratch diagnostic failures and optional skips stay
disclosed; none is relabeled as a successful execution.

The independent reviewer covers all 713 paths and 1,185 textual hunks, checks
the source-chain identities and isolated reconstruction, and verifies the
replacement packet's CRC, every inventory member and exact equivalence of all
713 postimages, 531 preimages, patch and 932 frozen inputs. Its retained fresh
checks include 113 Python executions with six intentional census-prose skips,
eight validators, 22 CLI captures (18 successes and four expected refusals),
258 focused and 768 broad wire executions, and seating checks across 30 forms,
343 candidates and 92 paths. Five actual predecessor-source negative controls
reject the old Common words, Jerome expansion and excluded English paraphrase.
The final native/packet follow-up assesses the recorded fresh execution rather
than rerunning native, annual, deployment, builds or primary-source inspections.
Its final receipt is
`.scratch/phase4-integrated-cold-review-20261022-independent/final-receipt.json`,
SHA256 `0e5eddd9306492b525bfd7413ded6e3278a098131d6a37aca0fdef927fe02f7a`.

Release checking derives exactly 508 refreshes and 25 adoptions, with all
23,468 site hashes exact and no new permission or policy prose. Latin remains
1,247 permitted/present of 1,269 ledger owners, with 22 removed; Roman English
is 206/1,427, pre-1955 English 193/1,378 and postconciliar English 113/546.
The family inventory remains 162 pending, none screened or promoted. No new
pre-1955 Latin permission or target attestation follows. The transported source
extracts are only the three accepted public-domain Latin extracts; protected
scans, rasters and expanded private payloads remain excluded.

This closes bounded Phase 4 only. The settled-native packet is the sole
Phase 5 comparison base. These acceptance and next-scope paragraphs are
post-seal parent-document deltas, not part of the sealed 713-file candidate.
No staging, commit, push, deployment or history change occurs. Annual textual
completion and its three promise requirements remain open.

## Phase 5, selected source batches

Read-only whole-source discovery supports twenty-two Latin prospects: twenty
previously unowned bodies and restored John of the Cross and Vianney Collects.
The seven chant owners are the Alleluias of Common Multiple Martyrs III,
Christmas's explicitly named third/day Mass, Common Single Martyr II,
Advent III, Easter Tuesday and Easter Thursday, and the second Alleluia of
Pentecost Ember Wednesday. Preserve each actual chant framework, including the
absence of a terminal Alleluia where the witness has none.

The other fifteen are the seven Orationes super populum of Ash Wednesday,
Thursday, Friday and Saturday after Ash Wednesday, Lent I Monday and Thursday,
and Lent I Ember Wednesday; that Wednesday's separate Oratio after its Gradual;
Sacred Heart Collect and Secret; Thérèse of the Child Jesus Collect, Secret and
Postcommunion; and the two restored Collects. The Ember Wednesday Oratio is
the occurrence after Gradual no. 462, not the opening Collect or concluding
prayer over the people. Thérèse's Collect is controlling unit 3758, not 3761.
John of the Cross includes the actually witnessed Doctor clause and ends
`Per Dominum nostrum.` Vianney has `sanctum`, not Lasance's `beatum`, and ends
only `Per eundem Dominum.` The historical date and spelling differences remain
declared.

Pustet 1862 and the identified Schott 1929 Latin witness supply the independent
whole petitions; the latter's appendix-date qualification and registered missing
pages remain explicit. Six expanded conclusions and two shortened conclusions
follow the existing transformation rule in `guidance/propers-for-agents.md`.
The six have separate earlier whole-formula/rubric proof, including Pustet
PDF pages 44, 55, 390 and 532, and fresh actual target-ending controls.
Preserve the target's printed stop exactly. Do not expand `etc.`, `in unitate`
or other abbreviations, add an Amen, change an addressee or assemble a petition.
Record every real spelling, pointing and ending transformation. Research hashes
are not canonical approvals. Fresh source implementation and independent
whole-primary review remain required; all other held bodies remain held.

The initial English lane selects fourteen terminal owners / twenty-two effective
references per model from thirteen actual Lasance prayers on twelve union
pages and fourteen separately inspected seeds. They are the two Lent I Ember
Saturday Collect forms; Marian-Saturday II Secret and Marian-Saturday III Postcommunion;
Paschal Multiple Martyrs extra Collect; Epiphany VI Secret; Epiphany III
Postcommunion; Epiphany IV Collect; Virgin Not Martyr Collect; Lourdes Collect and
Secret; Rosary Collect; and October martyrs Secret and Postcommunion.
Five whole Latin collations declare only the established consonantal i/j
transformations: `adjuvante/adiuvante`, `ejusdem/eiusdem`, `cujus/cuius`,
`Majestatem/Maiestatem` and `majestati/maiestati`. This is word collation,
not a normalized lookup: every recipient still requires literal complete
canonical Latin UTF-8, conclusion, wrapping and final newline equality.
Keep the English verbatim, including short endings, placeholders and the
Marian Postcommunion's absent final full stop. Preserve all 206 prior entries.
The separate John Cross and Vianney English leads and six normalized-only donor
groups remain outside this tranche. English nonrenewal, excluded inserts and
Latin permissions retain their distinct bounds.

The postconciliar lane selects fifteen classification repairs among OLM
nn. 285–302, artifact pages 207–212 / printed 153–158: nn. 285–292,
294–295, 297 and 299–302. Preserve the three existing quotation routes at
nn. 293, 296 and 298, all 54 core Reading/Psalm/Gospel bounds and parts, and
the entrance/Communion owners. The fifteen adapted acclamations require proper
body-unavailable and English no-exemplar dispositions, not fabricated held
body hashes, whole-body publication or new permission. No new Bible map, raw
proper node, runtime API or actual-use fact is authorized. Existing Ascension
transfer and morning-Mass notes remain source-local; unknown locality or
service does not license a substitution. Preserve n. 276, Psalm/CPDV/Acts
refusals and the earlier conditional-choice guards.

Capture preimages from the accepted settled-native packet. The three source
lanes have disjoint ownership; global generation, census, family and release
refreshes remain integration work. Each needs source sanity and independent
cold review, followed by whole-phase conventions/additions reviews, fresh
integrated gates and a new independent acceptance review. This scope does not
authorize unsupported words, translations, rights, source editions or annual
completion. The authenticated 2008 Common witness gap remains unresolved.

### Phase 5 integration preflight

Read-only integration preparation verifies 5,328 stable global preimages:
all 499 Proper outputs, 4,823 source-reader outputs and six census/family/
release files. The 537 focused derived paths and 491 canonical Roman envelopes
are included in that inventory. The accepted Phase 4 packet and receipt retain
their verified identities; no active source-author files are read or treated
as new baseline evidence.

The catalog is
`.scratch/annual-phase5-integration-baseline-20261022T181216Z/catalog.json`,
SHA256 `71c076bea51ab1f7a725b23e62b382f576cf87844fede1f15eca85ff9e68f361`.
The separate parent-document capture is a point-in-time post-seal delta and must
be recaptured after later acceptance updates. No global writer, test gate or
integration runs during this preparation. Source cold reviews and explicit
integration authority remain prerequisites.

### Phase 5 independent primary checks, candidate review pending

A new independent postconciliar primary audit reads all six whole OLM pages,
checks all eighteen acclamations and confirms all 54 core appointments against
the immutable accepted baseline. It supports the fifteen source-relative
adaptation classifications and preserves the three quotation routes, without
claiming exact Lectionary wording, approved English or publication permission.
Nn. 292 and 302 have the same citation but different complete units; they must
not be treated as identical. The Ascension-transfer and morning-Mass boundaries
are independently confirmed without inferring actual locality or service.

The baseline's 36 entrance/Communion positions contain thirty explicit owners
and six unmodeled positions: both antiphons at Easter VI Wednesday, Easter VI
Thursday and Easter VII Saturday are absent from the model. Preserve that
baseline without invented nodes; these are not proved liturgical omissions.
The private primary receipt is
`.scratch/phase5-easter-v-vii-cold-primary-20261022-independent-v1/final-receipt.json`,
SHA256 `d2fbd55b2a5ea97b727b95d3eb9067ec555e67b7020173f5f7c4a2247a674978`.
It has no findings. Actual source-candidate paths, bindings, hunks and focused
producer/CLI/JavaScript checks remain unreviewed until the immutable candidate
is available; primary-oracle completion does not accept Phase 5.

The independent Latin primary audit also returns no findings after opening all
twenty-two whole historical and target units, three whole-PDF identities and
63 distinct hash-bound images. It independently confirms the eight ending
transformations and their earlier whole-formula authority, the named forms and
roles, actual Doctor clause, Vianney ending and Thérèse unit 3758. Both Thérèse
Secret witnesses print `solemniter` with one `l`; actual spellings must be
declared rather than silently corrected. Schott's appendix-date attribution
remains corroborated bibliographic inference, not a separate dated imprint.
The receipt is `.scratch/latin22-independent-primary-cold-20261022/primary-receipt.json`,
SHA256 `54fe5c31a1e9c8f990c2df505a48bae4279bc31d71b8a1d4c5255be681c5ca7e`.
This is primary-oracle completion only; actual Latin candidate review remains
required.

### Phase 5 English primary findings and corrected scope

Independent English primary review blocks the initial fourteen-owner scope.
Lasance PDF 1220 / printed 1225 actually has `sanctissimo`; the controlling
PDF 758 / printed 677 / unit 3788 has `sacratissimo`. The discovery incorrectly
transcribed the historical word as the target word and falsely described the
remaining difference as i/j only. This is a different word, not an allowed
spelling transformation. Withdraw the Rosary Collect, restore its accepted-base
untranslated dictionary and retain the mismatch as an explicit barrier.
No semantic similarity, English rendering or Latin permission clears it.

The Virgin-not-martyr Collect at Lasance PDF 1393 / printed 1374 has
`pious devotion. Through our Lord.`, not a colon. Correct only that punctuation
and every dependent English/projection/proof hash. The correct full English
container-LF SHA256 is
`b3df70c3f21895c822ae3ad2a7ce7176176431068b9de134e9e4c4337c7120f4`.
The parent independently confirms both findings on the three image controls.

The source review's corrected oracle has nine strict and four i/j-qualified
roles: thirteen owners from twelve prayers. The revised selected scope is
English13, not English14 with a silent count change; reference and page totals
must be derived from the corrected candidate. All 206 older English entries,
unrelated absence rows, literal receiver joins and earlier mismatch barriers
remain exact. The original source packet
`20261022T183001Z-roman-1962-english14-phase5-source`, ZIP SHA256
`8fd50d02881870448462a02450d5e607dd831579c8318ccdccac39f6c032a13b`,
is preserved, unaccepted, and must be superseded by a new immutable pair.

The independent primary receipt is
`.scratch/phase5-english14-primary-cold-20261022-independent/final-receipt.json`,
SHA256 `56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25`.
Its preliminary self-transcription errors are corrected in new oracle files,
with originals preserved; the corrected independent readings, not the first
drafts, control this disposition. Actual corrected candidate review remains
required.

The parent separately repairs six obsolete English count/owner-set guards
against the initial English14 candidate. All 65 affected tests pass without
skips in 91.260 seconds, preserving exact membership, binding and negative
controls. Those counters and the exact new-artifact group require another
narrow reconciliation after English13 is sealed; this successful earlier run
is not relabeled as validation of the corrected candidate.

### Phase 5 Latin candidate finding and correction

Independent review covers all 83 Latin candidate paths and all changed hunks.
It confirms the twenty-two whole units, framework, role and conclusion controls,
all 1,247 prior bodies and the bounded Pustet/Schott rights chain. It blocks one
false factual attestation: both Schott PDF 1482 / printed [268] and target
PDF 756 / printed 675 / unit 3766 print `solemniter`, but the new body and notes
use `sollemniter` and wrongly attribute that spelling to the target.

Use the actual one-l spelling in this newly added body rather than retaining
an unnecessary house transformation. Correct the projection, notes, passages,
ledger, independent-proof references, tests and every dependent artifact/body
hash. Preserve all other twenty-one new/restored bodies exactly. The initial
`20261022T183412Z-roman-1962-phase5-latin22-source` pair remains immutable and
unaccepted; a corrected source pair and bounded independent re-review are
required. The independent receipt is
`.scratch/latin22-source-cold-review-20261022-independent/final-source-receipt.json`,
SHA256 `ea40273d2f6b8f80e8c01f0af213f13596d762f32a100767ecd319227e802544`.

The review independently reproduces all ten obsolete Latin whole-tree/count/
withholding guard failures against a passing 75-test accepted predecessor.
It also establishes exact equality of 48 unrelated artifact-manifest findings
and one protected-text Sources finding at both the cumulative accepted Phase 4
baseline and this candidate. That proves unchanged failure identity, not rights
clearance or harmlessness. Separate substantive diagnosis is required; payloads
and user work are not deleted or reclassified merely to make tests pass.
Two new Vianney withholding failures require narrow guard repair after source
acceptance. A separate scratch replay's missing Git index is a fixture limit,
not an inherited repository rights finding.

### Phase 5 regression preparation and parallel ownership

Read-only preparation identifies thirteen parent-owned legacy test files:
six Latin, five English and two Postconciliar. It performs no edits or tests.
After corrected source acceptance, repair only the exact authorized changes.
Keep historical body, wrapper and unowned-byte digests by first verifying
fixed accepted postimages, then reconstructing their exact predecessor fields.
Do not replace old preservation digests with broad new whole-tree hashes.
Christmas normalization is restricted to the one named day-Mass Alleluia.
Retain all other forms, negative publication controls and unresolved owners.

Latin accounting is 1,289 ledger rows, 1,269 permitted/present and twenty
removed, comprising seventeen unresolved and three withheld. John of the Cross
removes one unresolved row; Vianney removes one withheld row. Six exact
conclusion supplements include the owner-specific cross-edition Thérèse Collect
case. Generic supplement rules must not be loosened for unrelated owners.

The new Latin22 test pins three legacy files that this authorized repair must
change: October–November, winter/Ursula and Alexander/Hilary. Preserve those
pins in the spelling-corrected source packet. After the parent guard changes
are independently verified, the source-test owner must reconcile exactly those
three hash literals, seal a narrow follow-up and obtain independent review.
Do not delete the checks, introduce a circular test import or present the
intermediate packet as the final combined freeze.

Independent lanes now cover the English13 correction, immutable initial-English
candidate review, Latin spelling correction, Postconciliar candidate review,
and substantive diagnosis of the forty-nine retained rights findings.
The regression-repair plan is complete but remains unapplied pending corrected
source acceptance. Global generation and integration remain unauthorized.

### Phase 5 corrected English13 candidate, source acceptance pending

The English owner seals
`20261022T191653Z-roman-1962-english13-phase5-corrected-source`, ZIP SHA256
`95978f32e440444e099be1830defed82972e78951d6c538d38c7035ad209efb6`.
Its full patch SHA256 is
`21263a788e4170d5ca33d3875dc46576cc7c722bd43f7b4d2a6d5879a8a60dc3`:
42 paths, one modified inventory and 41 new files. Its exclusive correction-only
alternative SHA256 is
`7e576ed5ce495700fb98473db284c7f7f3b587b6429109d42f56399af6833442`:
48 paths, 39 modified, three added and six retired initial-candidate paths.
Both ZIP-only replays produce identical 42-file postimages. Never stack them.
The initial English14 pair remains immutable and unaccepted.

Measured scope is thirteen owners, twelve prayers, thirteen independent target
seeds and eleven historical pages: nine strict and four i/j-qualified cases.
There are twenty-one references in each effective model. The 3,219-byte TSV
SHA256 is `cfd58bf4120c2c506074e0ed17e8e1108ca32dd42806c313dc2b701d1870e979`.
Roman coverage is 219/1427 with 1,208 untranslated; inherited pre-1955 coverage
is 206/1378 with 1,172 untranslated. Accounting errors are zero.

The owner proves the exact restored Rosary absence, corrected Virgin full stop,
all 206 previous dictionaries, 773 old English source files and all fourteen
baseline canonical Latin hashes, including Rosary. Thirteen new tests pass
live, isolated and after the later external drift, without skips. Source,
calendar and tool-registry checks pass. Retained 8/10/89 executions still fail
2/1/3 assertions against provisional English14 parent guards; those are not
reported as green or as preexisting accepted-base failures.

The final-state receipt reports thirty Latin-owned paths differing from the
initial Latin22 packet while the separately authorized Latin correction is
active. Do not restore them or infer English cross-lane writes. Reconcile them
against the corrected Latin packet before claiming a combined freeze. English
postimages and its fourteen seed hashes remain exact; the old whole-other-lane
preservation check itself exits one. Independent corrected-candidate review,
parent guard reconciliation and all integration gates remain required.

### Phase 5 corrected Latin22 candidate, source acceptance pending

The Latin owner seals
`20261022T192306Z-roman-1962-phase5-latin22-solemniter-corrected-source`, ZIP
SHA256 `49d60c3be6e6d5106eb7fbf68401cb8c61778cce382f2720f66f10a7c893769e`.
The full patch SHA256 is
`3966b80f5ecfa5dbc3cfe3fbe47dbe36722ef8cb16380add8fd0ce6a9eb63585`,
inventory SHA256
`4a3b8d4847ae75041c6db9a91c97116cbe24459bce2fd2f9cf47f0806a071c8a`.
The exclusive correction-only alternative SHA256 is
`3fc0d6a50237a3c86b6536c40cbf10ebff1bfacdd0d1d781c2279e23d326c9d3`.
The full candidate remains 83 files, two modified and 81 new; thirty differ
from the rejected initial candidate and 53 remain exact. Both exclusive replay
routes verify all 83 postimages. The 134-file packet has 133 inventoried members
plus the inventory. The initial source pair remains immutable and unaccepted.

Thérèse's corrected one-l body, including final LF, has SHA256
`44ae620a19de8395079129c2c441a1d94df62b63057d618cf37682b000ee32f1`.
The 1,599-byte Schott projection has SHA256
`dab1c4edc0d73c87a91406deb5c6e2178f8bd6ace6b505932ff7b615f47431d4`.
Both actual witnesses are now described truthfully. Obsolete normalization is
removed from both projection manifests, all twenty-two projection notes and
ledger transformation declarations, the new test helper and corrected proof.
Strict source-validated publication refuses the superseded double-l body as a
stale Latin text hash; the actual CLI emits the corrected body and provenance.

All other twenty-one tranche bodies, 1,247 prior bodies and old ledger fields,
unowned bytes, appointment wrappers and remaining removed rows stay exact.
Counts, all seven double openings, three absent terminal Alleluias, six
conclusion expansions and two shortenings are unchanged. Fresh Latin22/library/
reference/damage tests pass 10/61/89/17, 177 total with no skips. Source,
calendar, registry, whitespace, preservation and CLI checks pass. An initial
scratch accounting assertion used the wrong occurrence/status assumption;
its corrected audit passes without source changes, and the failed attempt is
retained rather than reported as green.

The thirty changed paths match the author's stated Latin correction scope;
the English final-state observation must be bridged to these sealed postimages
before a combined freeze. Independent re-review is running. The three old
legacy-test pins remain deliberately unchanged and still require the separately
reviewed reconciliation after parent guard repairs.

### Phase 5 retained-rights diagnosis and checker reconciliation

The separate diagnosis covers all forty-nine findings, receipt
`.scratch/retained-rights-diagnosis-20261022-v1/receipt.json`, SHA256
`dccc1499bde2c2d887be76c1472ba19bc6a0aaf15ffe9126c575c3fc8f50a88b`.
The 48 manifest diagnostics conflate prose-reader eligibility with artifact
retention: fifteen BSB records have conditional permission and the Tournai
record has a bounded legal-exception basis. All sixteen payloads and manifests
already exist unchanged at HEAD; their sizes and hashes verify. They are not
new annual-tranche payloads, unrestricted images or a blanket permission class.
Existing conditions, attribution and outbound-licence exclusions remain.

The Sources diagnostic finds the protected target ID only in verification
`locus` metadata. Its actual controller is a project projection whose 105 words
independently match the retained public-domain Mame 1922 text under declared
orthography. This is not a new direct Common I calendar-ledger binding and
Gregory's separate dated row must not be presented as one. The diagnostic
controls still reject a protected controller and unresolved rights.

The two exact tests still fail with 48+1 findings. The parent authorizes a
bounded test-checker repair, not a new source permission: distinguish reviewed
per-artifact Git retention from prose publication and actual publication
control from verification-only testimony. Preserve fail-closed modern
permission-scoped, unresolved and restricted controls, independent historical
authority, complete provenance and all user payloads. No generic permission
allow-list, path-only waiver, schema change or generated writer is authorized.
The rights-test owner performs this repair before the separately sequenced
Vianney fixture update. Full checker review and fresh tests remain required.
Independent nonpublishing annual work may continue; neither the diagnosis nor
inherited failure equality establishes all-rights-green acceptance or deployment.

### Phase 5 cross-lane sealed-source bridge

The parent independently hashes the three active source archives and compares
all 130 disjoint source paths, 83 Latin + 42 English + five Postconciliar,
against both archive and directory postimages and the live files. All match,
with no cross-owner overlap. Both rejected initial archives retain their exact
identities. The English observer's thirty-path drift set equals the authorized
Latin correction set, and all thirty observed hashes equal the final corrected
Latin postimages. All six retired English-only initial paths are absent and
the three replacement paths match. No restoration or cross-lane source edit
is needed.

Receipt:
`.scratch/phase5-parent-corrected-source-bridge-20261022T193344040375Z.json`,
SHA256 `70d59fc80a6d0167b6a6ae6db51654da446a69ef2c8311f052fcc341b988ca7c`.
This is a point-in-time ownership and integrity check, not source acceptance,
the final combined freeze, global-output freshness, or annual completeness.
Parent guard changes and the three Latin test-pin updates remain outstanding.

### Phase 5 Easter V–VII source/code acceptance

Independent cold review accepts the exact five-file, nineteen-hunk candidate
without findings or blockers. The source ZIP remains
`1de6a2d029f829c680da05aa78b1bda44867eb5ecf1573b1d0524bda3597343d`.
Receipt:
`.scratch/phase5-post-source-candidate-cold-20261022-independent-v1/final-receipt.json`,
SHA256 `122bcfada0a3cc7e9a031f8c354fced3c8232cb11460cdcef4238ed08d0c5a51`.
All eighteen whole acclamations match the independent primary oracle:
fifteen adaptations are held unpublished and n. 293/296/298 retain their
Scripture routes. All 54 core appointments, thirty actual antiphon owners and
six unchanged model absences remain exact; 604 other Mass blocks are
byte-identical. Removing just the fifteen changed acclamation nodes makes the
old and new complete parsed indexes equal. No protected body or publication
permission is added.

Independent archive/privacy/replay checks pass for all five postimages and
two preimages. Nine new and 56 producer tests pass. New browser/CLI checks
cover 216 adapters, 180 held states and 34 actual CLI bridge cases; retained
n. 279 checks cover 258 preparations, 199 refusals, 84 adapters and six bridges.
Additional probes cover 121 admissions and 21 refusals, including eleven CLI
metadata/body-source negatives. All eighteen direct formularies and seventeen
dated positives pass, with the expected n. 294 date refusal preserved.
Bible contracts resolve 375/378 with the same three whole-Psalm refusals.

The retained 32-test suite still has precisely two obsolete 546/433 coverage
assertions, now authorized for 561/448 counter-only repair; 113 positives and
329 Latin owners remain unchanged. Two generated Post JSONs remain stale.
The independent global census exits two because the isolated fixture lacks
cumulative older Roman publication material; this is not a green global check
or independent reproduction of the author's three stale census documents.
Fresh parent generation, census/family checks and integrated gates remain
required. This accepts only the five-file source/code group, not Phase 5 or
the annual promise. The private review runtime is not for transport.

### Phase 5 corrected English and Latin source acceptance

Independent English review accepts the corrected 42-postimage candidate and
48-path correction route, covering 56 full and 62 correction hunks, including
all six deletions. Both primary findings are resolved. All 206 old dictionaries
and 1,208 remaining absence dictionaries remain exact. Thirteen fresh groups
pass without skips; production checks exercise thirteen bindings, 104 refusals,
42 carrier/sanitizer projections and 73 carrier negatives. Canonical negatives
exercise the source-test guard, not a newly claimed runtime Latin-hash guard.
Receipt:
`.scratch/phase5-english13-corrected-cold-20261022-independent/final-receipt.json`,
SHA256 `acd3369c4564bb76e9fb4900398c7384090bd831ff2f566380996378a48449e7`.

Independent Latin re-review accepts all thirty changed files and 58 hunks,
rehashes the 53 unchanged files and closes the earlier P2. All twenty-two strict
lexical digests match the retained primary evidence plus its correcting
supplement. Fresh 177 tests pass without skips. Strict production decisions
refuse 45 altered bodies: the old double-l body, twenty-two appended-Amen bodies
and twenty-two truncations. Actual CLI checks verify truthful attestation,
exact bodies and pre-1955 withholding; the old-body negative is a production
decision test, not a mutated-CLI replay. Both exclusive replay routes, all
payloads, old-body preservation and privacy bounds pass.
Receipt:
`.scratch/latin22-solemniter-cold-rereview-20261022-independent/final-source-receipt.json`,
SHA256 `3d15ddac0abafbecaeffa77ad54bc0b3b872a40a965c638dd0749227a7bd39e8`.
Its `accepted22-authority.json` owns the fixed body/source/postimage controls
for parent Latin guard reconciliation. The three historical legacy-test pins
remain valid at this source-only stage and need their authorized later update.
All three source/code groups are accepted, not the final combined freeze.

### Phase 5 parent Post counters and rights-checker cold acceptance

The parent accepts the exact two-hunk counter repair and stale method rename
after reviewing all changed lines and confirming no old method callers.
The 561/113/448 expectations preserve Latin329, rights/error zeros and every
other assertion. Four retained modules pass 32 tests without skips in
251.276 seconds. The immutable parent Post2 packet is
`20261022T194402Z-phase5-parent-post2-legacy-guards`, ZIP SHA256
`08fec536cf9d0fe5e68de73f56b7e3119cae5cd604af28ea90c9d5dcc93021ce`,
patch SHA256
`0267154add6be3963838a8dcb4a3ca6adff3f00a346fffc97a808800be494af0`.
Parent cold receipt
`.scratch/phase5-parent-post2-cold-20261022T194831304936Z.json`,
SHA256 `f21e8a00ff8d55faaf00ee18b5b69dd04c0d3b6d8e8e90b916571bc5540700da`,
confirms both live postimages. The unchanged successful suite is not rerun
merely to duplicate its result.

The separate one-file rights-checker packet is
`20261022T194211Z-parent-rights-test`, ZIP SHA256
`0b9cbe8925ee9eff7fd8c20ecc56ea8aa79482eb3f9e991c3c9ecc2120885a17`,
patch SHA256
`1d44dd2a69d0f04330bf330736dc1e8e3588bc6cd618b5a74b4811989a9c62ed`,
postimage SHA256
`7601275646afc150a7c7b5e9f4c4f09fe11034e7c6a743be9ac95678b497fbaf`.
All changed hunks and owning readers/validators are reviewed without findings.
Exact accepted retention fingerprints, dated review records and outbound
exclusions distinguish the sixteen retained artifacts from prose clearance.
The Common I exception requires the actual registered controller, independent
105-word historical authority, whole current row and unchanged locus.
No generic permission class or path-only bypass is added.

Fresh parent checks pass thirteen methods without skips in 13.474 seconds;
forward/reverse one-path replay is exact. Reinstating the actual old checker
produces the same 49 diagnostics and seventeen expected assertion events across
two methods, sixteen artifact subtests plus one Sources assertion, with no
errors or skips. An initial scratch audit incorrectly expected two failure
events; that audit, not product code, is corrected. The successful thirteen-test
run is retained rather than rerun. Parent cold receipt:
`.scratch/phase5-parent-rights-cold-20261022T194756858441Z.json`,
SHA256 `ba3a0ec821ef2473b808f37b86e24d2996621af39e0fe889e0b624dc9a6acebb`.
The author's full fifty-method rights run still has exactly two obsolete
Vianney subtest failures; no complete rights-green claim follows.
Whole-phase conventions/additions, remaining guard repairs and integration
remain outstanding.

With all three source groups accepted, the remaining English-five and
Latin-six legacy repairs run in disjoint write lanes. The Latin-six owner
starts from the already accepted rights-checker postimage, not its old HEAD
preimage, and may change only the Vianney CLI expectations in that file.
English preservation scans may observe these separately authorized Latin
test-file changes; they are not authority to revert another lane. No source
wording, global output, parent progress file or new Latin22 test is assigned
to either guard lane. The three historical pins stay unchanged until the
Latin-six patch passes independent review, followed by the source-test owner's
separate exact-pin reconciliation and re-review.

### Phase 5 English-five parent guard acceptance

The English-five patch changes eight hunks, adding nine and removing ten lines.
The parent reviews every hunk: coverage becomes Roman 1427/219/1208 and
pre-1955 1378/206/1172; the exact new-artifact group names thirteen owners and
removes only Rosary Collect. All other assertions and the new English13 test
remain unchanged. Fresh affected regressions pass 66 tests without skips in
86.339 seconds. The older 65-test English14 run remains historical, not
validation of English13.

The immutable packet is
`20261022T195435Z-phase5-parent-english5-legacy-guards`, ZIP SHA256
`d2c39f5cb137a891644c6cd5eae29321384583715e886ffce9afde15fac21339`,
patch SHA256
`81d3f87d7632f66ef1b91576cff56702b5fd29a1df4dcf5f2529167f97c165c5`.
All 32 archive CRCs and both directory and ZIP-only replays pass. The owner's
point-in-time preservation check retains source130, global5328, accepted Post2,
other tests and index. The parent independently confirms all five live
postimages, with no findings, receipt
`.scratch/phase5-parent-english5-cold-20261022T195640295028Z.json`,
SHA256 `9c11e4b79fc76c9e89c5a80945c31ab60438527befbf1f21511d641f08af45cc`.
The unchanged passing suite is not repeated merely to duplicate evidence.
Latin-six repair and its later three-pin reconciliation remain in progress;
whole-phase conventions/additions and all fresh integration gates remain open.

### Refreshed main, bounded TUI incorporation and Catena investigation

The maintainer expands the continuation to refresh local `main`, incorporate the
new terminal reader with the annual missal work, and investigate all held corpus
sources for their appropriate cross-references into Catena Omnia. The two Catena
audits are read-only: full registered-work coverage and the actual Catena pipeline.
No canonical Catena edits or source acquisition are authorized by that audit.

The ref refresh verifies ancestry and compare-and-swap updates local `main` from
`c6da24eda429337fe13d59420a3c489a98a16e66` and `origin/main` from
`a17f42c7e6ac61b51579784c4ee6e67108a70d47` to
`7d74f617ed449604cb6ae48bfc2d084c732f8e67`. Workspace HEAD, feature refs and index
remain unchanged. The five upstream commits are all the lectern reader or its
required tool-input fingerprint followup, not unrelated content.

The approved incorporation frontier is forty-four clean overlay paths and
thirty-one upstream-generated act-history comparison bindings, plus explicit
parent reconciliation of `PROJECT-WORK.md` and `promised-deliverables.toml`.
The comparison changes only replace the `scripts/_tooling.py` fingerprint and
byte size, 33501 to 33721. No generated file is hand-edited. The dirty liturgy
reader adapter remains exact, SHA256
`39fee299256cb0117ead3649afe10fc44bc04e66a9cc486427afc18aa7745184`.
The conflicted shared-record merge candidates are diagnostic only and are not
adopted. The upstream terminal-reader requirements and remaining open modes are
retained, with a new combined-incorporation requirement; a separate corpus audit
promise records the requested matrix and gap plan.

Prep evidence is retained under `.scratch/main-tui-refresh-20261022-prep/`,
including `integration-report.json`, `path-conflict-matrix.json`,
`projection-followup-matrix.json`, `ref-receipt.json` and
`final-preservation.json`. The refresh preserves 47,675 nonignored paths except
the separately authorized, concurrently changing Latin guards. This is a
point-in-time preservation statement, not a combined freeze.

Upstream's forty-six-test, terminal and cold-review results are historical
evidence, not combined checks. The approved local work includes a scratch-only
pinned dependency environment if needed, focused functional and registry checks,
nonmutating projection checks, terminal keyflows and fresh independent cold review.
No commit, push or deployment is authorized. The earlier 5,328-path Phase 5 global
preflight must be explicitly reconciled with the thirty-one comparison changes
and new tool inputs before integration. Annual textual completion remains open.

### Phase 5 Latin-six parent candidate, cold acceptance pending

The six authorized Latin guard files are implemented without source edits or
changes to the new Latin22 test. The owner reports eighty Latin tests, all fifty
rights tests and the explicit CLI case passing without skips. Historical
digests remain literal, both predecessor files reconstruct exactly, and
adversarial normalization checks pass. The earlier accepted rights-checker
postimage is the preimage for its narrow Vianney CLI fixture change.

The immutable packet is
`20261022T202305Z-phase5-parent-latin6-legacy-guards`, ZIP SHA256
`7ff42ea283e61f814c995beb596cc69d023ae9b28f5654fb5a53440c83573a68`,
patch SHA256
`571387371fe495d51827087d0b2c79df3b96769b75f25c5517d7830fd11af11f`,
inventory SHA256
`3803b7d68e3c59f76cd2ff3c647e8a94fc87cb43844835da062a1dc06839e904`.
It contains six candidate files and thirty-four packet files. Its owner reports
CRC, privacy, inventory and extracted-ZIP isolated replay passing, with the
point-in-time source130, global5328, English-five and index preservation checks
unchanged. Subsequent authorized TUI comparison changes are not part of that
earlier preservation claim.

Independent cold review must verify every hunk, the accepted22 source authority,
fail-closed masks, unchanged historical evidence and the entire previously
accepted rights-checker delta before this candidate is accepted. Exactly three
Latin22 historical-test pins remain deferred, not waived. No final source or
global freeze is claimed. After the TUI overlay exists, the full promise check
passes at 89 tracked deliverables and 71 complete; the earlier temporary
missing-TUI-evidence failure is resolved without weakening any requirement.

### Lectern incorporation, functional checks and terminal sanity check

All seventy-five approved paths are incorporated byte- and mode-exact from
`7d74f617ed449604cb6ae48bfc2d084c732f8e67`, with no integration-specific source
delta. The source work, dirty reader adapter, index and feature refs remain
unchanged. The complete immutable packet is
`.scratch/agent-handoffs/20261022T203035Z-lectern-incorporation`, ZIP SHA256
`d00e0ea032b4cc7d506a81ac42724f33c1f84e47ea68ae86abfb353d7808bc45`,
patch SHA256
`e018eaecab6558b426f015a96117630b5b9d9eee541b62b227681690a9cf2bf8`,
inventory SHA256
`7bea28e89184790649a3d4d6beaf86e4486554a21e3e4c104fa27d40940a6d4a`.
Its 133 ZIP members, CRCs, inventories, modes and isolated replay pass.
The original complete build-directory packet and incomplete first assembly
remain unchanged; an exact scratch copy corrects transient storage without
resealing. The copy receipt SHA256 is
`ce673d5f2b838b2a5588b43ee35bf952891fc04b7d7d630fe9416f3aea8cab70`.

With `TERM=xterm-256color`, forty-six lectern methods run under both the system
interpreter and the existing pinned preview interpreter: forty-five pass and one
complementary dependency test skips in each. The pinned run exercises whole
web-edition setting; the system run exercises wrong-Markdown refusal. Initial
`TERM=dumb` runs fail one bare-invocation theme assertion, retained without code
changes. The own shell smoke, two replayable examples with no recapture,
twenty-nine bounded registry methods, `tmt check` and nonmutating 548-file
act-history check pass. The full registry smoke has twelve failing subtests
among forty-seven scripts. These failures are retained, not assumed inherited
or concealed by the bounded pass; a separate read-only diagnosis is in progress.

The parent's isolated tuistory 0.12 runner completes forty-eight successful
interactive step receipts and captures thirty PNGs. All eight default surfaces
and seven further states receive visual inspection. Covered flows include
Read/Missal/Compare, open choices with cancellation, Catena author/fragment/Source
handoff, Law c.1008 withholding, search, help, command palette, three themes,
70x22/110x32/140x42 layouts and whole web-edition rendering under the pinned
Markdown. Two runner expectation failures are retained: an incorrect dialog
word and a surface digit sent while the Sources search input owned focus.
Corrected actions pass without application changes. Step22's voice cycle returns
to Everything held and is not counted as an English-absence check.

Parent evidence is under `.scratch/parent-tuistory-20261022/evidence/`;
`receipt.json` SHA256 is
`e3492ac2e58b452a1aaa1c34b8408b2a9a0e125c864ccae55c55a6d73024fa93`.
All seventy-five live hashes still equal fixed upstream after the checks.
Both sessions close and the owned loopback daemon terminates with exit zero.
These are pre-Phase-5-regeneration checks, not a final annual freeze or
maintainer terminal acceptance. Independent Python-reader and bridge/integration
cold reviews are running; whole-phase and fresh integrated gates remain open.

### Latin-six parent cold acceptance and narrow three-pin candidate

Independent review accepts all six complete guard files and thirty unified
hunks, with no findings or blockers. All twenty-two owners match the reviewer's
accepted source authority, all eighty source pins and eighty-three source
postimages match, and both predecessor files reconstruct exactly. The rights
file retains every byte outside its authorized Vianney CLI fixture method.
All historical digest assignments and methods remain; five new OctNov
adversarial methods are added.

The reviewer passes eighty unique legacy methods with zero failures, errors or
skips: sixty-one complete before a 300-second timeout, then the exact remaining
nineteen pass in 228.303 seconds. This is not reported as one uninterrupted run.
All fifty rights methods pass, plus a separate rerun of the same CLI method.
Independent negative controls reject 406 malformed inputs, accept no bad input,
and call no restoration helper before rejection; all twenty-two positive owners
are accepted. The source130/global5328/other-tests/English-five/index preservation
catalogs remain exact at the scoped check, with the authorized TUI31 classified
separately, not as a whole-tree freeze.

The independent receipt is
`.scratch/latin6-parent-guard-cold-20261022-independent/final-guard-receipt.json`,
SHA256 `632775eb134a2504db62a7ec4672928a07cc97d1ae0d3e922c7e693c57431b04`.
It owns all six accepted hashes. Only after this acceptance does the parent
update exactly three `PRESERVED_FILES` literals in
`tools/tests/test_roman_1962_latin22_phase5.py`. OctNov becomes
`c13d838baf217cf25be163e465a4f90322d8ecf04e89322f237eec105764686e`,
Winter `e7354e1d015919cc47f235fca3aa1f5134afc8fe250765eb24b6d2eafbc71f05`,
Alexander/Hilary
`98cf7be34f0a26c6427b472ea749164ef49df91b5c020bed3484760e90b5463b`.
The old test hash
`bb88875066d1bcae178780d96d91d4451d662281a9a762a8301efff152437e20`
becomes
`7dc3a1569140e14f32fa2c98e607577b05871f3c197a307db67107d731d6afca`.
Exact replacement proof preserves every other source-test byte, assertion and
oracle; ten fresh Latin22 methods pass with zero skips in 26.509 seconds.

The narrow immutable followup is
`20261022T204534Z-phase5-parent-latin22-three-pins`, ZIP SHA256
`e51eebc163d18873677fe84e4630423bc6c441c11094d2959931ed4ea0111914`,
patch SHA256
`9a79d7859bced01c17b991a50ffbb7045c32d4aa7b531f2775554d1ffb7c36d0`,
inventory SHA256
`65678e11eb044a6db60a4f7e8d40e6c5bdbb03b9702cc8ce0673f6b1d64d4475`.
Its eleven files pass privacy, inventory, CRC, ZIP-byte and
forward/reverse/reapply checks. Independent narrow review now accepts the
followup with no findings or blockers. It confirms exactly three literals in
one hunk and every other test byte unchanged. Ten unique methods pass without
failures, errors or skips across two five-method runs after a 120-second
timeout; the continuation takes 314.137 seconds. This is not one uninterrupted
run. Five independent replay checks pass; ZIP CRC and all-byte checks pass
separately. No broad 80/50/177-method suite is repeated.
Receipt
`.scratch/latin22-three-pin-cold-20261022-independent/final-pin-receipt.json`
has SHA256
`99fd0d9c8c8aa7ef4e4e9691e5d5afcac695496664eddafa5a887e9d52a0b780`;
the amended source130 frontier has SHA256
`69cf0dee8d38e565894f97c26b6987097ad781c8eacdf34e54a1bec92eb28fd8`.
It intentionally amends only this one test postimage of the earlier source130
bridge; every original packet remains immutable. No final combined freeze,
annual or publication acceptance is claimed.

### Lectern bridge and integration cold acceptance

The independent non-Python/launcher group accepts all forty-seven assigned paths
and fifty hunks, with no findings or blockers. This includes ten added JavaScript
files, the tool/configuration boundaries and all thirty-one comparison JSONs.
Every comparison semantic change is limited to the authorized tooling hash and
byte size; no text or rights decision changes.

The reviewer exercises fifty-two bridge requests with forty-four assertions and
forty-five gate probes, all passing without skips. Twenty-one runtime dependency
hashes remain exact, the shell smoke syntax passes, and assigned packet/upstream
bytes and modes, the protected adapter and HEAD remain unchanged. Two initial
reviewer harness errors are retained and corrected, not presented as candidate
defects. No full annual, broad suite, build, native or visual acceptance is claimed.

Receipt `.scratch/lectern-node-cold-review-20261022/receipt.json`, SHA256
`92166ee9e20456c6a4918dd1a3c4ad323ff2eae28b72ce6b8d7ace032e8e6e63`,
owns the exact path and hunk closure. The separate twenty-eight-path Python and
launcher review is complete with the findings below. Whole-phase
conventions/additions and final post-regeneration acceptance remain pending.

### Lectern Python findings and bounded repair authority

The independent reviewer reads all twenty-eight files and thirty hunks and
reports nine blocking P2 findings and one P3 finding. Targeted parent inspection
confirms the concrete triggers. The receipt is
`.scratch/lectern-python-cold-review-20261022/receipt.json`; acceptance is false,
not inferred from the accepted bridge group.

The ten findings are: blank month cells emit a missing date; changing Source
editions leaves an old passage delivery valid; Law back-navigation restores the
pane without the active act; History next/previous highlighting cancels the
full-record request; filtering Texts leaves a removed record delivery valid;
rapid Scripture steps use the last response rather than the requested place;
Propers labels a displayed reading with the independent finder's calendar;
snapshot settling returns success after its busy-worker budget expires; the
bare-invocation test inherits `TERM=dumb` while expecting the color theme; and
a whitespace-only initial Catena reference indexes an empty split.

Repair authority is limited to `scripts/lectern/month.py`,
`scripts/lectern/snapshot.py`, the seven affected surface files (Sources, Law,
History, Texts, Scripture, Propers and Catena), and
`tools/tests/test_lectern.py`. It includes regression tests, both interpreters
and terminal environments, the own shell smoke and unchanged example replays.
It excludes new features, source changes, derived authority, broad generation
and publication. A new immutable ten-file correction packet must preserve the
other sixty-five upstream paths and pass independent re-review. The original
seventy-five-path import remains immutable; the corrected frontier will no
longer be described as byte-exact upstream.

### Twelve registry smoke failures: diagnosis and narrow next work

The source of record is
`.scratch/phase5-registry-smoke-diagnosis-20261022/REPORT.md`, with its retained
input comparisons, semantic evidence and preservation receipt. No full
forty-seven-script rerun or synthetic full baseline establishes this diagnosis.

- Four assertions contradict accepted Phase 4 inputs: Ordinary English bindings
  and role wording, the already-positive Advent I English Collect, the unchanged
  151 Western coverage trajectories rather than 78, and two already approved
  shared font assets missing from an exact public-site asset expectation.
- `mass-today` encounters a foreign-recension applicability rejection. Input
  and predicate evidence proves the mechanism, not a full baseline CLI outcome.
  Its structural provenance and safe Roman-1962 positive execution must be
  separated while preserving Pre-1955 refusal.
- Exactly `tests/tools/{mass-ordinary,mass-propers,mass-today,
  missal-coverage-reconciliation,public-alpha}.test` may receive source-specific
  fixture repairs. No blanket allowance, ignored assertion or weakened rights,
  source, actor, closure or applicability guard is authorized. The five-script
  packet requires its own independent cold review.
- Knox, typeset-Bible and web-edition failures require their existing
  outside-repository licensed destination, permitted build destination and
  pinned Markdown environment respectively. No licensed text acquisition or
  relaxation of these protectors is authorized.
- Strict Source-reader projection and the family snapshot await their existing
  owner transforms. Forty edition differences are a retained observation, not
  a new freeze census.
- The chronology annotation and at least the observed Douay-Rheims Bible index
  are stale. Neither inheritance nor Phase 5 causation has yet been proved over
  their complete input closures. Only scratch owner derivation and precise
  affected-output diagnosis are authorized now. An unchanged John 6 mapping
  digest rules out only that one suspected mismatch, not index-wide staleness.

The existing integration preflight must be supplemented if Bible-index owner
outputs are justified. No global-writer window, final combined freeze, annual
acceptance or publication is authorized by these repairs.

### Lectern ten-file correction candidate

All ten confirmed findings now have bounded repairs and regressions. Fourteen
focused methods pass. Each of four full runs, system and pinned interpreters
under `TERM=dumb` and `TERM=xterm-256color`, runs fifty-nine methods: fifty-eight
pass and one complementary dependency skip. The system Markdown version
exercises wrong-lock refusal and skips whole-web-edition rendering; the pinned
version exercises rendering and skips wrong-lock refusal. No final run reports
ResourceWarnings. The first unsupported test-harness `--json` attempt and the
intermediate resource warnings remain recorded, not hidden.

The own smoke assertions, two unchanged example replays and `tmt check` pass.
The smoke's destructive cleanup is disabled only in its retained scratch
wrapper, not in tracked assertions. No broad registry, annual, native, generator
or publication checks are repeated.

Packet `20261022T211037Z-lectern-cold-review-corrections` has ZIP SHA256
`53f21750d24b6b9c1f3020fa1bec52518136e97519e17c860344ec7166fc3c68`,
patch SHA256
`71a9aebbc01b41424fc8981b5ea95a346f38a685d7f782da8fd9609cd91c6259`,
inventory SHA256
`47a0f9abb01830ea19f9535b4867a416611e1b298ef52709fbdedf43ae2e3e5f`.
The final seventy-five-path frontier SHA256 is
`7d3f68ac553fa91dc30d303452f223bf02f7c234d757f3c546946aa8caf00c74`.
It comprises sixty-five unchanged original import paths and ten corrected
paths. Independent re-review is running; this candidate is not yet accepted.
Qualified preservation distinguishes the concurrent Catena research installation
from source/runtime/index/ref and historical-packet preservation.

### Five-fixture blocked candidate and Catena placement correction

The first narrow fixture packet,
`20261022T211211Z-five-shell-fixtures-blocked`, has ZIP SHA256
`81bd177517e93756d62415b1491c4c4cbfe8b0c91aaeda1e2b12ef18c39b8639`.
Exactly five smokes run once: Ordinary exits 1, Propers 2, Today 1, coverage
reconciliation 0, and Public Alpha 1. The packet is explicitly unaccepted.
Ordinary reaches a later Confiteor marker mismatch; Alpha reaches an incomplete
synthetic absence row; and Today's author-added empty-stdout assertion
incorrectly treats a pre-refusal header as successful execution. Source-specific
diagnosis and bounded fixture correction are authorized, without copying current
output as an oracle or relaxing later controls.

Propers correctly refuses four new audit CSVs as unowned source payloads.
The first Catena metadata installation under `src/sources/commentary/research/`
is therefore rejected despite its table and link checks. Its immutable packet
`20261022T211305Z-catena-research-durable-metadata` remains evidence of that
attempt, not acceptance. The correction moves only the fifteen newly authored
metadata files to
`workflows/reviews/corpus-catena-cross-reference-2026-10-22/`, updates current
links and provenance, and preserves exact CSV and historical-receipt bytes.
No source-library allowance, renamed payload, source artifact or new schema is
authorized. Research acceptance is distinct from installation acceptance and
the final parent promise check.

### Seven Bible indexes and one exact chronology annotation

The read-only owner-input diagnosis is complete:
`.scratch/phase5-bible-chronology-staleness-20261022/REPORT.md` and
`exact-difference-catalog.json` distinguish inherited and Phase 5 changes.
The bounded Phase 4 input reconstruction compares 1,904 read paths and closed
calendar, artifact-TSV and chapter membership. It is not a separate execution
of the entire Phase 4 smoke suite. All 9,963 observed product files remain
unchanged during diagnosis.

All seven publishable carried indexes are already stale at accepted Phase 4.
Across them the current required delta is sixty inherited additions, nineteen
inherited removals and twenty-one new removals, with zero surviving
passage-body changes or chapter changes. The only Phase 5 removals, per edition,
are `Colossians 3:1`, `John 16:7, 13` and `John 17:21`. The other eight distinct
references removed from the fifteen acclamation owners remain appointed
elsewhere. Unresolved-refusal lists remain identical; no offsets or additional
text are invented.

Authorize only staged owner generation and installation of `index.yaml` for
`douay-rheims`, `douay-rheims-american-1899`, `clementine-vulgate`,
`catholic-public-domain-version`, `king-james-version`,
`world-english-bible-catholic` and `revised-version-1895`. No canonical chapter,
Bible manifest, projection, calendar, witness, licensed edition or release pin
may change.

Also authorize the registered annotation owner for the exact Claude document
`liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost`.
Its sole changed file is `research/chronology-annotations.tex`; the chronology
record is already current. The required Phase 4 and current postimages are
identical: expose three already-recorded unresolved Psalm occasion groups and
the existing historical subject beside its year. No underlying historical date,
claim or source changes. The leaf's 1 October withdrawal remains intact; no
PDF, web edition, catalog or release publication is authorized.

These eight outputs require exact catalog comparison, focused owner freshness
checks and independent cold review. Any additional leaf failure is unknown and
must stop for diagnosis, not trigger an all-leaf refresh. This narrow writer
authority is not the deferred final global integration window.

### Three environment-sensitive smokes pass without fixture changes

The parent reruns exactly `knox-bible.test`, `typeset-bible.test` and
`web-edition.test` with the pinned interpreter first on PATH, controlled terminal
settings, disabled source caches, and distinct newly created workspace scratch
destinations outside every repository. All three exit 0 and print `ok`.
Git confirms no diff in any of the three fixtures. Python is 3.14.8, Markdown
3.10.3 and Textual 8.2.8.

The unchanged tests exercise licensed-root refusal and cached parsing without
retrieval, output-destination refusal and deterministic typesetting, and pinned
web conversion. No guard, renderer lock or assertion changes. No licensed source
is acquired, and no publication is installed. Receipt
`.scratch/phase5-parent-environment-checks-20261022T2127Z/receipt.json` records
the exact fixture hashes, environment, commands and workspace-relative log
locations. These three narrow successes do not replace the retained 35/47
registry result or establish a whole-tree freeze or annual acceptance.

### Catena research installation accepted; audit promise only closed

The corrected fifteen-file research set now lives at
`workflows/reviews/corpus-catena-cross-reference-2026-10-22/`.
No files remain at the rejected source-library location. Actual source-library
validation changes from exit 1 with five unowned-file diagnostics to exit 0
with zero diagnostics. The four CSVs and all historical receipts remain exact;
the source protector and source records remain unchanged.

The parent reviews the installed-record delta, findings, current provenance,
input identities and README links, then independently passes all fifteen
checksum entries. The reviewed compact tables still contain 1,064 work
classifications, 123 eligible owning registrations, sixteen research relations
and all 73 books. Zero relations are admission-ready. The four constraints and
316 uncertain registrations remain explicit.

The narrow relocation packet is
`20261022T212456Z-catena-audit-location-correction`, ZIP SHA256
`9895f6b5a870215d38062985f9a239b9450b4042edda1e8fad1fdd1bf3263fa1`,
patch SHA256
`48095efd642539adfdc22785ef5c39383398c9325b3453f2edac8ab7a4aa039e`,
inventory SHA256
`afa95f9f5a5ff9f0c1ace0c2f823ba565b59140663a2b723fd6ece60ac2c0fc3`.
Its exclusive basis is the first installation's verified post-state, not another
first-install patch. Directory and ZIP-only replay pass, preserving all original
synthesis and first-install evidence and 1,915 generated Catena files.
Correction receipt SHA256 is
`f6766b18aca06f393def030dd4d6ff9753949f0ca16436ec6655862aa667a7d3`.

Only the two corpus-to-Catena research criteria are marked passed. This closes
neither annual textual completion nor terminal-reader acceptance and authorizes
no source acquisition, fragment/controller repair, translation, dating,
edge insertion, harvest or Catena generation. The root register and ledger own
this later disposition; installed historical status text is not rewritten.

### Expanded integration preflight v2

The read-only supplement at
`.scratch/annual-phase5-preflight-supplement-v2-20261022T212932598126Z/`
records thirteen unique parent guards (English5, Post2, Latin6); the earlier
rights checker overlaps Latin6, not a fourteenth path. The amended source130
retains the same paths, 129 exact hashes and one accepted test postimage.
Named source, guard, TUI, fixture, Bible, research and parent-document cohorts
total 251 disjoint paths outside the old 5,328. The resulting 5,579 prospective
paths are a planning union, not a final candidate census or freeze.

All eight new Bible/annotation paths lack release pins. Known owner outputs
are 5,328 plus TUI31 plus Bible8, or 5,367; TUI code and audit metadata gain no
release adoptions. Accepted scoped Bible outputs must be consumed without
duplicate builds. Whole-phase reviews, final frontier capture, ordinary owner
transforms, scoped release refresh, annual/publication checks and settled
preview/native validation remain required.

Plan SHA256:
`7a2af0cee5eb023c1b8dc5c94de735397608fee15fad40d6410247f51ea2c893`;
catalog SHA256:
`7ea7588611ae3636a92b1ecad1ea35d33c5d4c32d8be400c6c61b6c4efbabfeb`.

The actual Catena audit completion check passes at 89 tracked deliverables,
72 complete. The root register now records the later closure; no sealed
installation or historical receipt is rewritten.

### Two residual TUI blockers after first correction review

Independent re-review closes eight findings, passes fourteen focused methods,
and verifies thirteen distinct old-image methods fail. It retains two blockers:
the Texts lookup-refusal branch clears the cursor without invalidating pending
record delivery, and snapshot cleanup clears the bridge process while an active
reply still dereferences it. Real initial-intent/key and live-worker probes
reproduce both; the latter masks the intended timeout with a worker failure,
not a resource leak. Parent inspection confirms both code paths.

Receipt
`.scratch/lectern-corrections-cold-rereview-20261022-independent/receipt.json`,
SHA256 `56f6350965379196493cbacd013dd71f4bde914fc1f6673e6022f6eedf9bb29e`,
is unaccepted. The thirteen-method negative-control report includes fourteen
subtest failure/error events, not fourteen unique methods. Reviewer harness
errors and the authorized eight Bible/annotation changes remain separately
classified, not product defects attributed to the correction author.

Authorize only `scripts/lectern/surfaces/texts.py`,
`scripts/lectern/snapshot.py`, existing `scripts/lectern/bridge.py` if needed
for lifetime coordination, and `tools/tests/test_lectern.py`. Check all record
ownership-clearing siblings and a real active bridge timeout; do not suppress
worker errors, invent a second bridge or wait blindly for the 120-second
protocol budget. Previously closed corrections and original packets remain
intact. A new narrow packet and independent residual review are required.

### Eight owner outputs implemented and independently accepted

The seven staged registered Bible-index builds and exact annotation owner now
produce exactly the eight approved changes. Twelve focused checks pass,
including both named annotation regressions. The exact delta is sixty inherited
additions, nineteen inherited removals and twenty-one new removals. All 9,387
chapter files, surviving bodies, headers, refusals, source130, publication
files, Git index and refs remain unchanged. No full-shell or global pass is
inferred.

Packet `20261022T212953Z-phase5-eight-derived-refresh` has ZIP SHA256
`fd2e838ef287a29fca18e5dd7d7609e443bb1bbe25cd158e8fd88f37d5de8d11`.
Its forty-eight files include all eight pre/postimages, exact expected catalog,
owner provenance and actual checks; CRC and ZIP-only replay pass.
Independent review now accepts all eight paths and ninety hunks, with no
findings or blockers. Twelve checks and eight negative controls pass.
Receipt
`.scratch/phase5-eight-derived-independent-cold-20261022T213459Z/final-receipt.json`
has SHA256
`87bc50ed5dd3e5d7ed1570f886b1382d6ad72d2bf6b24d8c33fc01bb00fdd663`.
The reviewer makes no canonical edits and claims no global integration
acceptance. The withdrawn Claude leaf stays withdrawn.

### Five-fixture source-specific stop and next bounded corrections

Packet `20261022T214120Z-five-shell-fixtures-source-specific-stop` retains the
next exact five-script result: Ordinary 1, Propers 1, Today 1, reconciliation 0
and Alpha 0, with no rerun or subsequent edit. ZIP SHA256
`752536d626d9bb3b21592be13c914e01890b64935c3d7912ac9ef44eb403a240`;
cumulative five-file patch SHA256
`12e0925bb123c7136ebac9b998ab6301de8e2fd3431ed0e31085aadc5f9513e2`.

All thirty-four independently sourced Lasance body hashes and seventy-seven
exact turn shapes pass, including unknown actor where a printed R. alone does
not establish a server. Old Cummiskey/P55/Latin/Mame controls remain distinct.
The remaining Ordinary assertion incorrectly demands the old Cummiskey note
for the active Lasance witness; preserve Lasance's own historical, unapproved
target and no-full-collation cautions instead.

Propers' obsolete joint Vianney absence expectation must become two controls:
the English beatum/sanctum witness gap remains unavailable, while the accepted
Latin22 Collect is independently permitted, exact body SHA256
`12105ba3649c6e5b37c48e65fd93475d55706432eb8485f495625e32b20ddcb4`.
Secret and Postcommunion remain inherited Common appointments, not two further
newly recovered Vianney bodies. No English or source-rights permission changes.

Today's P55 refusal, apparatus-only output and structural inspection now pass.
Its Eudes fixture expects eleven canonical citation records where the inherited
Common has twelve, including both James 1:12 and Sirach 45:9 in the distinct
Paschal Alleluia. Require the exact source-backed census and resolved text;
the JSON variant inventory does not mean all alternatives execute on 19 August.
Later expanded Roman positives remain unreached, not passed.

The same five fixtures may receive these source-specific corrections and
equivalent already-proved witness/accepted-Phase-5 expectation repairs, keeping
all negative guards and stopping on any new runtime/source/rights/currentness
root cause. A complete five-script run and independent cold review remain
prerequisites. No global or annual acceptance follows from the two passes.

### Residual TUI repair candidate, independent re-review pending

The two residual repairs change exactly Texts, snapshot, the existing bridge
lifetime owner and the test file. Texts shares record-owner invalidation across
clearing paths; the bridge owns coordinated child/stream shutdown, and snapshot
cancels deliveries first. Existing protocol, refusal and timeout semantics remain
subject to independent verification rather than inferred from test success.

Nineteen focused methods pass. Each system and pinned full run passes
sixty-three methods with one complementary dependency skip, sixty-four run
per interpreter. Own smoke, unchanged example replay and registry checks pass;
no final ResourceWarnings occur. Earlier setup and expected preimage failures
remain recorded.

Packet `20261022T215916Z-lectern-residual-corrections` has ZIP SHA256
`ee4b43cab0c5d7af92f8b35b42aff5c3d72f6044ffbd34992a6596917dd4c0c2`,
patch SHA256
`ac1111ea07a6ecff326c7b2017c74e7efd48ba611786e0382e209950f5ba69b8`,
inventory SHA256
`0ce0015638d1c6137affa8033dff2659f1eb0234f50ac5746e6951052315370e`.
Its forty-one members pass CRC, hash/mode, privacy and isolated replay checks.
The new seventy-five-path frontier is sixty-four original-exact paths plus
eleven corrected paths, SHA256
`a5f819576c5f50422db2976658693d8d4074a3122f742bee74a332227953846d`.

The author preserves source130, guards13, all 9,387 Bible chapters, the protected
adapter, Latin22 pin, historical packets, index and refs; known concurrent
authorized work is qualified, not treated as a whole-tree freeze.
The independent residual review now accepts exactly the four-file delta, with
no findings or blockers. Five new focused methods, two retained real reproductions
and three negative controls pass with no ResourceWarnings. The actual initial
bad-leaf/two-Down sequence advances the refusal token, clears record ownership,
and rejects delayed delivery. A live busy-child capture raises the intended
TimeoutError; the CLI exits 70 with empty stdout and the exact settling
diagnostic. Before safety cleanup, children are reaped, streams closed and workers
stopped; the same global owner then restarts the real bridge successfully.
Protocol IDs, out-of-turn handling, Refused and 120-second patience remain
unchanged, while unexpected WorkerFailed still propagates.

The reviewer verifies all forty-one ZIP members and isolated four-file replay,
the final sixty-four-original/eleven-corrected frontier, the earlier eight
closures, and fifty-nine earlier test methods in byte-exact classes. Protected
sources, guards, chapters, history, eight accepted derived outputs and sixteen
Catena metadata paths remain intact. Earlier scratch-harness/sealing failures
are retained, not product failures. Receipt
`.scratch/lectern-residual-cold-rereview-20261022-independent/receipt.json` has
SHA256 `2aace2f6f90924df52a6df73d8dfdbe1559aa81a00a91d913a2ce45857d9532c`.
This review does not independently adopt the author's full-suite/smoke/example
claims. No whole-phase conventions, additions, combined integration or annual
acceptance is inferred; the upstream open product requirements remain open.

### Three fixture passes; bounded census prerequisite and Today reconciliation

Packet `20261022T220848Z-five-shell-three-repairs-currentness-stop` records five
single runs: Ordinary 0, Propers 1, Today 1, reconciliation 0 and Alpha 0.
The three authorized note, Vianney and Eudes repairs pass, as do the settled
Advent JSON/expanded named-Bible positives. This is three passes and two later
failures, not an accepted five-fixture group. ZIP SHA256
`d1c1fe9dcbcc4a38ee82edf5556430a559df3d878041f0e6fa75fa1cb26c6420`;
cumulative five-file patch SHA256
`8328659e04b20b12978514a6943facdb1b0c0820b532f04e6d5c74e78acc8d5e`.

Propers reaches its real census-currentness gate. Quiet diagnostics were removed
by the test sandbox cleanup; the later bounded source count establishes the
3,066-to-3,051 postconciliar scripture-bearing difference from the accepted
fifteen acclamation repairs. No gate is disabled or replaced with fake documents.
Authorize only `tools/tpt mass-propers census --write` for the existing delimited
blocks in `docs/the-mass.md`, `guidance/propers-for-agents.md` and
`src/sources/calendars/README.md`. Capture preimages and all changed cells, prove
all out-of-block bytes exact, check owner currentness and stale negative
controls, and retain scoped release-pin implications for final integration.
These three paths already belong to the old integration preflight, not a new
source or tool ownership expansion. No other generator or source change is
authorized by this prerequisite.

Today next fails the old mass-level `proper collect unavailable:` wording for
17 June 2027. The source for that date and the two later cases owns text-free,
rights-withheld Collects at proper-body scope. Update only the source-specific
availability assertion, proving the own Collect stays unavailable, its Common's
different Collect is not substituted, and placeholder prose is never printed as
prayer. The other two cases and later tier/language/withheld-Latin controls remain
unreached until an actual full Today run. All five complete smokes and independent
review remain required; no global, annual or publication acceptance is inferred.

### Census three-block owner refresh independently accepted

The registered owner alone rewrites the three declared blocks. Each changes
Postconciliar scripture-bearing propers 3,066 to 3,051 and encoded passages
4,045 to 4,030. The fifteen accepted acclamation classifications explain both
subtractions: one proper and one encoded entry each, not eleven distinct
references or a count of individual verses. Six of 327 numeric cells change;
321 cells, all other prose, all out-of-marker bytes, sizes and modes remain
exact. No source, runtime, test, schema, family or release file changes.

Packet `20261022T222335563824Z-phase5-census-three-blocks` has 65 ZIP members,
ZIP SHA256 `d2877e3210d5f94c8ad60d98bdb6fb9dbdb7a59498b20274887e9fae6b84e704`,
patch SHA256 `b2ea608532165782700aab6c92c2fb9ad697576fa9037799cc8899dd821a1714`,
and inventory SHA256
`0fade4467f8dd4e146c898eced7d38147026b4779599ec00c49d7479412f0632`.
The author retains the initial real currentness refusal, one owner write, green
post-check, scratch positive and six correctly refused isolated stale rows.
Two harness-only failures remain recorded without rerunning owners.

Independent parent review recomputes all three exact six-cell deltas and
outside-byte boundaries, checks every ZIP member/hash/mode and live postimage,
joins the accepted source hashes, and freshly runs canonical currentness
(exit 0) and a one-document stale-row negative (expected exit 1). The negative
check writes nothing. ZIP-only forward/reverse replay passes all five steps
with no privacy hits. Three document postimages, accepted Post source, HEAD,
branch, refs and index remain exact across these checks. Receipt
`.scratch/phase5-census-parent-cold-20261022/receipt.json` has SHA256
`0d3dc99a733ef4cef64e6fc8f0c9fa59a457658e953f0faa8f8aae46a5b9bf27`,
accepted true with no findings or blockers. This is a three-block acceptance,
not a new source review, full fixture result or integration acceptance.

Exactly one existing release pin needs the later scoped union:
`docs/the-mass.md`, SHA256
`9ab41bc9197e3ef7b27b9b9bc765788d6f22352e733053df5991a77efcd235a8`
to `a2065af904b87cee79ede3b34fccbf17dfdbf81b1bf835e13e91f14cf5048e91`,
plus its generated rights row and the final `rights_record_sha256`. The other
two documents have no pins. No release write or blanket adoption occurs here.
These three paths were already in the old 5,328-path preflight; ownership and
prospective union counts do not grow. The four settled fixtures enter separate
cold review while Today's final bounded follow-up runs. All five complete
smokes, complete cumulative fixture review and global acceptance remain open.

### Today own-Collect cases pass; later refusal harness still blocks completion

Packet `20261022T224502Z-today-own-collect-later-stop` changes only the
three-date Collect block, one incremental hunk; all other fixtures and the
unchanged suffix remain exact. Actual full Today exits 1 after 555.444 seconds.
All three dates pass English/Latin JSON and expanded checks. Later tier,
language, withheld-Latin expansion, YAML positive and the initial real-library
Propers refusal also pass. Twelve focused calls and 144 rejected author mutations
are retained, not substituted for the failed complete script.

The next unchanged refusal harness cannot load its intended Ordinary partial
JSON: its copied repository lacks `src/web/browser/liturgy/ordinary-seating.js`.
The separate broad PATH restriction also hides Node required by the composed
tool itself, not only calendar-rubrics. These are incomplete fault-isolation
fixtures, not proof that the intended component refusal is wrong. Ordinary and
rubric partial assertions, text refusal diagnostics, final invalid-input
controls and final `ok` remain unreached. Sandbox cleanup removed individual
JSON files, but stdout/stderr diagnostics remain. The first completion delivered
no report; the same worker returned only its retained report without new tools
or reruns. No output was treated as no result, not as a pass.

ZIP SHA256 `3140a1c9f09f5aee876a04825828873ed6c1835cc1cbc7c409ae176656cfaefc`;
incremental patch SHA256
`29cac638279e3d71f0d81dbed440d385767d9b703f939d705e5563dcd6045068`;
cumulative 28-hunk/five-file patch SHA256
`008c9cfa869df14cbc8033ca814a93769344d93799a1ffe3c9422875ae8f74b7`.
The tested Today hash is
`eb4e08ebb447448272cdeebdf75221dc3d6fbdb62284cc37f1b962ad07e0063a`.
The 93-member ZIP passes the author's CRC/inventory/privacy and exact replays.
All 10,132 protected paths and 550 historical pins remain exact; only permitted
census blocks and parent records changed concurrently. No global freeze is
claimed.

Authorize only the Today fixture's incomplete refusal setup and necessary
adjacent assertions: provide the existing shared seating dependency, preserve
the Ordinary invalid-JSON sibling refusal, and isolate a nonzero rubric sibling
refusal in a separate complete fake repository with Node still available.
Keep exact component problems, local refusal and inspectable calendar-days
fallback. Do not hide essential dependencies globally to simulate one sibling,
change runtime behavior, or weaken a failure/absence guard. Retain decisive
JSON diagnostics and run the focused complete tail first. Once it passes with
all unaffected bytes exact, run all five complete scripts once in the pinned
environment with separate outside-workspace sandboxes and long timeouts.
This avoids an extra duplicate full Today preflight; it does not relabel the
previous failure green. Stop on any new failure. Four settled fixtures are under
independent review; the final fifth-file and complete cumulative review remain
required. No global writer, build, annual, native or release action is added.

### Four settled fixture changes independently accepted

Independent review accepts exactly `mass-ordinary`, `mass-propers`,
`missal-coverage-reconciliation` and `public-alpha` test changes, with no findings
or blockers. All four full files (3,170 lines) and all 22 cumulative hunks are
reviewed. Seven targeted CLI checks pass and 511 deliberate negative controls
are rejected. Protected state remains exact; canonical edits and owned jobs
are zero. No complete-four/five smoke or global acceptance is claimed.

Receipt `.scratch/four-shell-cold-20261022-independent/final-four-receipt.json`
has SHA256
`3908810b6643a84ecdc78df0c56b4d6d46581799999985bed82f3d9bca220700`.
It excludes Today. The review worker now independently examines Today's six
settled assertion hunks from the immutable 224502 packet, not the live changing
refusal harness. That bounded continuation must return its own actual result;
the final harness delta, complete-five run and final fifth/all-five acceptance
remain separate pending work.

### Six settled Today assertion hunks independently accepted

The immutable 224502 Today candidate's six cumulative assertion hunks pass
independent review with no findings or blockers. The full frozen 1,103-line file
is read as context, and independent YAML, translation-ledger and Bible source
proofs close all six hunks. Eighteen targeted CLI calls return their expected
statuses; all 509 negative controls are rejected. The earlier four-file receipt
remains unchanged and none of its checks is repeated.

Receipt
`.scratch/today-six-hunk-cold-20261022-independent/partial-today-six-receipt.json`
has SHA256
`cc307ec419f8e9d3d0985ac897e6ba42eac8965066070df2414cfa82bb0de5c4`.
The reviewer conserves 10,685 catalog paths byte/mode-exact and confirms the live
prefix through line 1,020 matches the sealed candidate; the changing tail is
unread and excluded. This is point-in-time, partial assertion acceptance, not a
combined freeze or whole-fifth/all-five acceptance. The old 555.444-second
complete Today run remains exit 1. The final refusal-harness delta and actual
complete-five results still need separate review. Reviewer owned jobs are zero.

### Complete-five run passes; final three-hunk harness review pending

The repaired focused refusal tail exits 0 in 68.460 seconds through final `ok`;
45 targeted negatives are rejected. The original broken tail exits 1 in
68.389 seconds, and an intermediate overstrict commemoration assertion exits
1 in 68.666 seconds before correction. Both failures and decisive diagnostics
remain retained. Only Today's refusal setup and necessary adjacent assertions
change; its preceding Collect assertions, earlier prefix, final text/input
suffix and the other four fixtures remain byte/mode-exact.

The authorized fresh complete-five run invokes each script once in parallel:

| Script | Exit | Seconds |
| --- | ---: | ---: |
| Ordinary | 0 | 9.491 |
| Propers | 0 | 775.345 |
| Today | 0 | 584.841 |
| Reconciliation | 0 | 87.041 |
| Alpha | 0 | 58.468 |

There is no timeout or rerun. Today reaches all three Collect dates, both
languages and views, all tier/language/withheld-Latin positives, repaired
component-refusal assertions, text refusal checks and final invalid-input
controls. Reconciliation intentionally prints no final `ok`; its numeric exit
0 establishes completion. The runner's conservative output-marker Boolean is
retained and qualified, not silently rewritten. These are actual execution
results, pending independent adoption with the final harness review.

Packet `20261022T231509Z-refusal-tail-final-five-pass-pending-review` has 94 ZIP
members. ZIP SHA256
`513a52e8545e92f39ab6b2cf581d621006f321bb56bb5b8742ca00cbe7527fdf`;
incremental three-hunk Today patch SHA256
`3109037bc905fb60838f29129b7993b8063718d232f8f4d44aece951da7c9dba`;
cumulative original-baseline 31-hunk/five-file patch SHA256
`ff5f6fdc16c468afd527159c187068d7be5b80f3c6b70e38c93cd880dc79bd1e`;
inventory SHA256
`dfaea7ee18176fd4ea7fe85a9202b61d9ea84443ae8c90e0d9d701f478a74f84`.
Final Today SHA256
`e862a117ca4891ade79b9fdc9d9e12f7a50a40bc92f291a2eb208099b2d8d201`;
all other fixture hashes match the accepted four-file receipt. CRC, inventory,
privacy, incremental/cumulative and ZIP-only replay checks pass in the author's
packet; they are not self-acceptance.

All 10,135 protected paths and 814 historical pins remain exact, including
source130, guards13, final TUI75, Bible8, Catena16, 9,387 chapters, runtime721
and accepted census3. Index, HEAD, branch and refs remain exact; parent PROJECT
and annual records are the only qualified concurrent changes. The ledger and
older packets remain unchanged. Author owned jobs are zero.

The same independent reviewer now reviews only the final three-hunk harness
delta and complete-five execution/conservation, retaining the accepted four-file
and six-hunk assertion receipts without repeating their checks. Final-fifth and
all-five acceptance, the complete input freeze, whole-phase conventions/additions
reviews and all global/annual/publication/native integration remain pending.

### Exact final-five fixture group independently accepted

Independent final review accepts all five exact installed fixture images with
no findings or blockers. The remaining three Today harness hunks close; 63
predicate and two shell negative controls are rejected. The reviewer adopts
the author's five completed exit-0 runs and conservation proof without another
complete-smoke run. The earlier four-file and six-hunk assertion receipts stay
unchanged, so all 31 cumulative hunks have explicit coverage.

Receipt
`.scratch/final-five-shell-cold-20261022-independent/final-five-receipt.json`
has SHA256
`687f0cb62f9e9758b6bf82d0d9a591084c36fc6c87331d27fb9850a280743d4b`.
The old failed Today packets and intermediate negative evidence remain intact.
The reviewer creates only new read-only evidence, modifies no canonical or
pre-existing path, and reports zero owned jobs. This accepts the exact fixture
group, not annual/global integration.

All source/guard/TUI/fixture/research/census prerequisites are now settled.
Next capture the actual complete accepted-input/dependency frontier and
owned-output preimages, recapture the four parent documents, and assemble the
exact combined review diff against the accepted Phase 4 base. Obtain the
whole-change conventions and additions reviews before the later exclusive
registered-owner transform window. No global writer, source acquisition,
publication, deployment, commit or history action is authorized by this record.

### Superseding integration direction and accepted corrections, 2026-10-23

The maintainer authorizes coherent commits and a non-force push to `main` once
the combined result is consistent. Commits remain on `feature/missal-reader`;
ordinary upstream integration must preserve both accepted local work and fresh
upstream changes without rewriting history. Pushing authorizes its automatic
Pages deployment attempt, not a claim of deployment success.

The maintainer explicitly chooses to defer the exhaustive additions audit and
proceed with integration, full release checks and final integrated cold review.
The sole audit is stopped. Its last formal continuation records 1,147 completed
and 2,498 pending obligations, with 315 lexical JavaScript parameter candidates
still unrefined; its final obligation count is unknown. No later partial
scratch activity is an accepted result. The audit is incomplete, not passed.
Continuation receipt
`.scratch/additions-cold-audit-20261023-continuation-02-sol/receipt.json`
has SHA256
`c8eefd4aa1080475c33743ff99d5af6c4eae8d1aef7602c15d9de7c08fa09322`.
This deliberate sequencing change supersedes the preceding exhaustive-audit
prerequisite. No product promise or other final acceptance gate is waived.

The whole-change conventions review completed all 254 paths, 446 textual hunks
and one binary, requiring changes rather than accepting the original freeze.
Its receipt
`.scratch/phase5-conventions-continuation-20261023/receipt.json`
has SHA256
`52be2cba350f5148e7ad0e6b73664fb45499c71e06d1ffb18bc4b8e05f7e5ec3`.
Its two findings and the additions audit's eight confirmed findings have
independently accepted, bounded corrections:

- Initial terminal cleanup and shared dependency-free surface metadata:
  `.scratch/lectern-cleanups-independent-cold-20261023T003746497009Z/receipt.json`,
  SHA256 `ffd6c1eedc52e8c71f61118d0ea2747b82747c8921d5d7af34df853ea6d360a9`.
- Actual Propers `view.notice` and fixed Law indentation:
  `.scratch/lectern-propers-law-independent-cold-20261023T005350989415Z/receipt.json`,
  SHA256 `96a11853ad4f601350959945b8e752a89faa6cdb293dab66b62182887a3edaa0`.
- Five further proved-unused terminal options/exports, preserving preceding
  corrections:
  `.scratch/lectern-five-trims-independent-cold-20261023T014331832529Z/receipt.json`,
  SHA256 `ecc7e4380bcd6f228678d1d369c0ab4a7493f3153d1813729b0c53a3a792a086`.
- Catena work/edition language distinction:
  `.scratch/conv2-cold-independent-20261023-r1/receipt.json`,
  SHA256 `1bb84972d7f2f5c4287abca170c7af87af7866549b8e56ba57170e3b404e2d83`.

The exclusive installation applies only the latest cumulative fourteen-file
terminal postimages and six Catena metadata postimages, not stacked incremental
patches. Both sealed ZIP hashes and CRCs, all twenty live preimages and accepted
postimages, and canonical modes pass exact joins before mutation. All twenty
installed hashes/modes pass afterwards; the other ten Catena paths remain
unchanged. Installation receipt
`.scratch/phase5-exclusive-install-20261023T023806076068Z/installation-receipt.json`
has SHA256
`e21a6d856e8c49d18b5f7fafcf1b9516b951012b50008c8fb0631cb3fcb0dffe`.
All preimages and historical packets remain preserved.

The Catena correction preserves all 1,064 original-work language cells in a
separate column and corrects 508 owning-edition cells through strict registered
ID joins. All 20,216 other cells and row order remain exact. Seventy rows have
multiple distinct raw edition-language values; 71 rendered cells contain a
semicolon because one raw value is already composite. The latter is not a
71-row distinct-language claim. Historical research receipts remain unchanged;
the new derivation supersedes only current copy bindings and width claims.
Research acceptance still admits zero new Catena fragments.

Bounded publication preparation joins all 26 new payloads and their manifests
to retained accepted evidence: eight historical bounded PDFs, eleven
Latin/projection text files and seven English TSVs, totalling 12,365,713 bytes.
It finds no material basis gap or privacy/protected-text candidate and uses no
whitelist. Evidence lives in
`.scratch/publication-payload-evidence-20261023T021003680833Z/REPORT.md`
and `payload-matrix26.json`. This consumes recorded rights decisions, not a new
legal determination or whole-scan clearance. Conditional retention is not prose
permission. The 571 current generated Proper/Source paths are pre-global
outputs; future changed bodies, final artifacts and every newly reachable
outgoing object still require their exact publication joins and checks.

The original combined freeze remains immutable historical evidence, not a
settled build. This amendment and the installed corrections replace its current
candidate. Next recapture the bounded candidate, run the registered owners
exclusively, review the exact release-binding union, run affected regressions,
the fresh 5,856-render annual matrix, deployment/public-preview gates, a settled
freeze and fresh native checks, then obtain independent integrated acceptance.
Coherent commits, fresh main ancestry and outgoing-object review precede any
non-force push. No source acquisition or broader product completion follows.

### Owner window and annual/local-publication gates pass

The amended pre-owner capture records 1,162 candidate paths and 5,913 observed
candidate/owner paths, with all 5,367 retained owner preimages verified. Its
manifest is
`.scratch/phase5-exclusive-install-20261023T023806076068Z/before-owners.json`,
SHA256 `c9eee6c52d5168fe66a827e9fee72aebf45c273e5ff2eaf37302ed2282a47834`.
Registered source-library/source-inventory checks pass. The Proper writer and
check pass, followed by strict Sources structure, reading check and strict
currentness check. All three census blocks remain current without rewriting.
The family owner changes only audited date, canonical catalog snapshot and
snapshot; all 162 pending review units and zero screened/promoted states remain
exact. History structure is check-only and current.

The exact Proper/Source delta is 538 paths: 505 modified and 33 added, no
retirements. Of the modified paths, 59 change semantic content and 446 change
only generation identity. This is 498 Proper outputs and 40 Sources outputs.
Sources has 4,856 files, 3,599 readable passages and 2,850 explicit withheld
passages. The release owner refreshes one exact 571-path union: fixed32,
generated538 and the already accepted, reader-recognized
`src/sources/inventories/postconciliar-proper-translations-v1.toml` existing
hash pin. This last exact source-ledger pin amends the original generated-only
proposal; it matches the amended source130 frontier and grants no permission.
There are 538 existing hash refreshes, 33 exact adoptions and no retirements.
All other manifest fields, out-of-scope pins and rights prose remain exact.
Final release status is `exact: 0 stale binding(s)`.

The deployment-source gate initially exits 2 on the accepted Claude54 chronology
annotation's stale publication-inventory hash. The registered source-inventory
owner refreshes only the Claude inventory's audited date, snapshot and that one
file hash. All 2,017 file rows, except that hash, and all classifications remain
exact; its paired classification-review file is byte-exact. The annotation
remains SHA256 `677340ee45e1da9df9925240ac79b8a1578fcb493ab311d3fa65c07624d508bd`.
Preimages, failed log and the bounded correction receipt are retained in
`.scratch/phase5-exclusive-install-20261023T023806076068Z/`.
The full corrected deployment-source gate then exits 0, not an inferred pass.

Fresh completed checks:

| Check | Result |
| --- | --- |
| Full annual opt-in matrix | 7 tests, 5,856 renderings, no skips, exit 0, 957.566 seconds |
| Installed terminal reader | 78 tests: 77 pass, one intentional pin-environment skip, exit 0 |
| Regenerated adapter parity/absence guards | 8 pass, exit 0 |
| Generated rights/source guards, group A | 13 pass, exit 0 |
| CLI/source-path guards, group B | 28 tests: 27 pass, one optional exact-predecessor-baseline skip, exit 0 |
| Corrected deployment-source gate | exit 0 |
| Public build / Pages-target verify | both exit 0 |
| Preview build / preview verify | both exit 0 |
| Tool registry / tracked whitespace | 47 tools valid / no errors |

The generated publication ledger verifies all 538 paths, 68 novel
body/provenance carriers (22 Latin, thirteen English and 33 readable Sources),
130 source identities and 26 payload identities. Six retired English paths
remain absent and all sixteen conditional-artifact prose refusals remain.
It records zero actionable findings. The initial scratch checker's
surface-array ordering assumption failed, was corrected to the production
set-order contract and remains retained, not relabeled. Evidence:
`.scratch/final-generated-publication-20261023-readonly/generated-publication-ledger-final.json`
and `test-receipt.json`. This does not clear staged/outgoing objects.

All builders are terminal before the forthcoming settled native freeze. The
fresh annual result is structural evidence, not annual textual completeness.
Native execution, immutable integrated replay and independent integrated cold
acceptance remain pending.

A fresh upstream fetch now identifies main
`74150dd4e9caaeaea191b35b55780219b5196769`, seventeen published missal-history
commits beyond the original five TUI commits. Its 504-path batch includes
source records, native texts, History/Sources projections, release records and
shared progress records, not changed annual calendar appointments. It is not
yet merged here. Subsequent ordinary nonrewriting integration must preserve
both accepted source graphs, refresh their exact generated/release joins and
revalidate affected behavior. This new upstream phase cannot be silently
treated as covered by the present pre-merge candidate or its receipts.

### First settled native run blocked, 2026-10-23

The fresh settled invocation exits 1: seven tests execute twelve harnesses,
251 of 257 assertions pass, six fail and none are skipped. Day integration
fails three coverage/first-visit assertions, visual reset fails two warning-
hierarchy assertions, and Propers integration fails one material-coverage
assertion. No console, request or HTTP diagnostics occur. The observer retains
assertion names and statuses, not their individual raw assertion messages.
Coverage/date fixtures are being checked against the accepted restored texts;
no fixture-only conclusion or runtime acceptance is claimed.

Terminal evidence:
`.scratch/phase5-integrated-execution-20261023T030853050783Z/terminal-receipt.json`,
SHA256 `ffd41e748ddb0ac6c53173fb9b9308086fc6affac2415487716ad8e81e67644d`.
The immutable failed packet is
`.scratch/agent-handoffs/20261023T031746441670Z-phase5-integrated-settled-native-blocked`,
with sibling ZIP SHA256
`a4531fc75f278c029a27e5a154c499762cd9a1a9b1b0cbb661c32479e87da93f`.
Its Phase-4-relative frontier is 796 paths: 584 modified and 212 added,
1,338 text hunks and one binary. Exact repository, public and preview inventory
conservation, response identities, ZIP CRC and ZIP-only replay pass. Those
transport and conservation results do not accept the failed native behavior.

Do not alter or relabel that packet. The bounded repair needs new evidence
and cold review. Unchanged annual, source and payload proofs remain historical
results eligible for exact dependency-based reuse, not permission to suppress
the failure. Integrated acceptance, commits, reconciliation and publication
remain pending.

### Native fixture diagnosis and final-state validation order

All six failures exercise the formerly withheld Vianney Collect. The Propers
failure is in its later withheld-body branch, not its initial Advent assertions.
The accepted Phase 5 source restores Vianney; Anthony Abbot is also already
published and is rejected as a substitute. Claret on 23 October retains a typed,
rights-withheld own Collect, no Common-Collect substitution, and two of three
represented Latin bodies. Seven test-only hunks change the shared partial/
withheld route and first-visit fixed date across three browser harnesses.
All assertions, test names and Advent unresolved-choice/fidelity/reconstruction
guards remain unchanged. No production, source or release file changes.

Author evidence:
`.scratch/reader-fixture-drift-author-20261023T032429772279Z/author-report.json`
and `proof.json`; patch SHA256
`b67a41d5d3139fd6871f526eb4ba65eb8130cdce4ab9c2c2d155465a7e09e703`.
All three Node syntax checks and bounded whitespace checks pass. Twelve source/
preview model cases and eighteen negative controls pass. A separate parent
review traces all seven hunks, the actual Claret YAML owner, first-visit path
and unchanged Propers assertions; it finds no actionable defect in the repair.
This is fixture review, not native DOM/layout acceptance.

The validation order is narrowed to avoid duplicate browser execution:
make honest coherent candidate checkpoints, integrate the already examined
upstream main ordinarily, settle the affected owners and public/preview builds,
then run the complete native suite once and obtain independent integrated cold
acceptance of that actual final candidate. No failing result becomes a pass,
no annual/product criterion is weakened, and no push is allowed before those
gates and outgoing-object review. The immutable failed packet remains unchanged.
