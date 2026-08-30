# Catena Omnia — complete implementation and corpus roadmap

## Status and authority

This roadmap translates `guidance/catena-omnia-vision.md` into a complete
long-horizon execution program. It is deliberately more detailed than the
existing E0/E1 Catena lane because E1 solved the first production slice, not the
whole-canon product.

This file does not retroactively create authorization. Existing authority and
ownership continue to come from:

- `guidance/corpus-browser-master-plan.md`;
- `guidance/corpus-browser-roadmap.md`;
- `guidance/corpus-browser-implementation.md`;
- `promised-deliverables.toml`;
- specific Catena, Source, Bible, versification, chronology, Liturgy, release,
  and publication guidance.

Work units below are a **designed program**. An agent must still confirm that the
unit it intends to execute is authorized, that its owner is free, and that no
newer mainline state supersedes the assumptions here.

The roadmap is written from this recovered state:

- current `main` baseline for the program:
  `09437907472581df4a8969010bd494249a3539a5`;
- Catena E1: complete, merged, live, and release-bound;
- Catena E0 composition: accepted and closed to casual redesign;
- E1 merge validation: 1,351 fragments, one solved commentary book, 73 canon
  entries at that checkpoint; counts must be rederived in every future lane;
- B0/B1 candidate at the time this roadmap was authored:
  `3d323f0880859b5cf8d380a7bb04ef29584d1e81` on
  `impl/corpus-foundation-b0-b1`;
- protected Liturgy `day-missal.css` selector scoping remains outside the corpus
  lane unless its owner grants the recorded narrow carve-out;
- inherited corpus-browser blockers still include the generated nested-`main`
  defect, site-wide target-size disposition, and the protected Propers focus/
  skip-link behavior recorded by the artifact gate;
- final non-Liturgy shared-shell cutover is not yet complete.

## Program doctrine

### Build value and foundation in parallel

The roadmap has four concurrent tracks:

1. **Foundation and product surfaces** — shell, Scripture, Sources, Search,
   accessibility, URLs, release integration.
2. **Catena corpus acquisition** — actual commentary text, editions, rights,
   loci, translations, chronology, and verification.
3. **Typed relationships** — Scripture, Liturgy, Source, History, Law, and
   Publications edges.
4. **Independent review and release** — cold product review, source review,
   browser evidence, integration, signing, deployment, and live verification.

Acquisition must not wait for the shell to be perfect. Shell work must not
pretend that a beautiful empty corpus is progress. Relationship work must not
publish edges faster than the source model can prove them.

### One owner per shared seam

Global layout, shared CSS/JS, release bindings, shared generated schemas, and
protected Liturgy files have one owner at a time. Parallel workers use separate
full checkouts and branches. No worktrees, shared index, force-push, or
cross-branch uncommitted state.

### Every wave stops for review

A branch being green or visually coherent does not accept itself. Every
material product, schema, source-acquisition, relationship, or integration wave
has a stopping line and an independent disposition.

### Counts are derived

Do not copy the 1,351/1/73 checkpoint into a future report as current truth.
Every lane that discusses coverage derives its counts from the exact source and
generated tree being reviewed.

## Dependency overview

```text
CURRENT MAIN 094379074
        |
        +--> CO-00 B0/B1 cold disposition and record reconciliation
        |       |
        |       +--> CO-01 foundation blocker closure / permitted carve-out
        |       |       |
        |       |       +--> CO-02 non-Liturgy shell cutover
        |       |               |
        |       |               +--> C2 Home/Publications
        |       |               +--> D1 Publication Reader
        |       |               +--> F1 Sources
        |       |               +--> I0/I1 Scripture
        |       |
        |       +--> scale-safe Catena work that does not need shell cutover
        |
        +--> CO-03 corpus scale benchmark
        |       |
        |       +--> CO-04 acquisition engine hardening
        |               |
        |               +--> CO-05 breadth acquisition waves
        |               +--> CO-06 depth acquisition waves
        |               +--> CO-07 voice/translation expansion
        |
        +--> Sources + Scripture production surfaces
                |
                +--> CO-08 exact source drill-down
                +--> CO-09 Scripture <-> Catena edges
                +--> CO-10 Liturgy -> Catena seam (separate Liturgy authority)
                +--> CO-11 other typed corpus relationships
                        |
                        +--> J0/J1/J2 Search
                        +--> K0/K1 relationship navigation
                        +--> CO-12 advanced Catena views

All tracks --> continuous accessibility/performance/release gates
          --> L0/L1 whole-site acceptance
          --> M0/M1 integration/cutover/final review
```

The diagram is a dependency map, not permission to skip the master plan's own
accepted IDs. Where an existing C/D/F/I/J/K/L/M unit owns the work, this roadmap
adds Catena-specific acceptance criteria rather than renaming the owner.

# Phase 0 — reconcile the current candidate before building more

## CO-00 — independent B0/B1 cold review

### Objective

Disposition the current shared-foundation candidate from a clean checkout and
make the durable record internally consistent before it becomes ancestry for
more corpus work.

### Required inputs

- `main` `09437907472581df4a8969010bd494249a3539a5`;
- feature candidate beginning at `3d323f0880859b5cf8d380a7bb04ef29584d1e81`;
- `guidance/corpus-browser-master-plan.md`;
- `guidance/corpus-browser-vision.md`;
- `guidance/corpus-browser-roadmap.md`;
- `guidance/corpus-browser-implementation.md`;
- `promised-deliverables.toml`;
- the new Catena vision and roadmap.

### Cold-review questions

1. Does `check-browser-models` protect the model-driving suites it claims to
   protect without accidentally turning `make check` into the whole test suite?
2. Are every named exclusion and its reason still true at the exact review head?
3. Does `SiteChromeScopeTest` prove a class of collision rather than bless a
   one-off patch?
4. Is the `sources.css` scoping change render-neutral on Sources and inert on
   other routes?
5. Is `day-missal.css` genuinely the only remaining unscoped site-chrome
   exception of that class?
6. Has the branch altered any protected Liturgy source, global shell owner,
   release binding, Catena production path, or unexpected file?
7. Do base/head full-discovery identities reproduce?
8. Reconcile the recorded validation discrepancy: the candidate commit prose
   says the base's 24 failures reproduced with no new identity, while the final
   handoff reported 25 with one additional stale-binding oracle failure. The
   review must rerun and state which is true on the exact reviewed head.
9. Reconcile “three commits pushed” with the branch's actual commit distance
   from main; distinguish commits created by the execution from total branch
   ancestry.
10. Do the 2,290 Chromium artifact identities remain byte-identical between
    base and candidate where claimed?

### Allowed outcome

Record one of:

- `ACCEPT`;
- `ACCEPT_WITH_RECORD_CORRECTION`;
- `CHANGES_REQUIRED`;
- `BLOCKED_BY_PROTECTED_OWNER`.

### Stop line

No merge, release signing, deployment, or Liturgy edit merely because CO-00
passes.

## CO-01 — finish the shared-foundation hardening promise

### Objective

Close only the remaining work genuinely owned by the B0/B1 foundation promise,
without resurrecting withdrawn reader-shell centralization.

### Work

1. If the protected Liturgy owner has granted the exact narrow selector-scoping
   carve-out, apply only the mechanical page scope to the twelve recorded
   `body > .site-header` selectors in `day-missal.css` and prove no rendered-DOM
   or product change.
2. If no carve-out exists, keep the deliverable `blocked`; do not work around
   ownership by moving Liturgy CSS, copying the rules, or weakening the gate.
3. Preserve step 6 as withdrawn. Do not promote `reader-shell.js/css` to shared.
4. Preserve steps 7 and 8 as unimplemented until a real pair of production
   surfaces demonstrates neutral shared primitives/accessibility blocks.
5. Resolve the release-binding path only under release authority after the
   implementation candidate is accepted. Never hand-edit the hash.

### Acceptance

- collision suite green except no unrecorded exemptions;
- relevant real-Chromium route evidence unchanged;
- protected Liturgy product behavior byte/DOM equivalent where touched;
- release-binding refresh scoped to authorized paths only;
- promise ledger moves only when every criterion truly passes.

# Phase 1 — finish the corpus surface foundation

## CO-02 — final non-Liturgy shared-shell cutover

This is the existing final shared-shell program work, not a Catena redesign.

### Catena requirements

The final shell must prove on `/catena/`:

- Commentary is the current global domain;
- Scripture locus remains the first content fact after the shell;
- the shell does not add a second Catena title or duplicate current-domain
  identity;
- Browse/Menu and Jump do not steal fragment or chapter URL state;
- opening/closing an overlay preserves reading position and returns focus;
- 320px and 200% text preserve one reading order and no document overflow;
- no shell CSS changes solid/dashed chain semantics;
- no Catena route gains a second `main` landmark;
- no global Search label appears before J0-J2 actually earns it.

### Stop line

Protected Liturgy receives none of this shell.

## Existing C2 — Home and Publications implementation

### Catena integration requirement

Home should make Commentary discoverable as one of the corpus tasks/destinations
without turning Catena into a featured dashboard card. Publications may expose
works about commentary but do not become a second commentary catalogue.

## Existing D1 — Publication Reader

### Catena integration requirement

A publication may link to Catena only when its source/structure owns an exact
Scripture relationship. Do not keyword-link prose to Catena automatically.

## Existing F1 — Source Library production implementation

F1 is a major Catena dependency because every held fragment should ultimately
have a clean source drill-down.

### Required Catena cases

- one Catena fragment whose passage is controlled directly by an Artifact;
- one whose passage is controlled through a Segment, when real data exists;
- readable edition;
- withheld edition;
- original-language readable / translation unavailable;
- required acknowledgement;
- exact return path to the Catena fragment/locus where technically practical.

## Existing I0/I1 — Scripture product

Scripture is Catena's natural sibling.

### Required design contract

- Scripture remains a plain Reader when commentary is not requested;
- an exact locus with held commentary may expose a quiet `Commentary` transition;
- a locus with no held commentary must not imply that the tradition is silent;
- the target preserves Bible/numbering state where supported;
- Catena exposes the reciprocal return to the Scripture Reader;
- no duplicate Scripture-text source is created for Catena.

# Phase 2 — prove Catena can scale before multiplying the corpus

## CO-03 — whole-canon scale benchmark

### Objective

Measure the current architecture under realistic corpus-growth fixtures before
changing chunking, transport, cache, or model boundaries.

### Build three generated stress fixtures

Fixtures must use the real schema and generator but synthetic/public-safe text
where needed so they do not create fake corpus claims:

1. **Wide canon:** commentary present in many books/chapters with shallow depth.
2. **Deep chapter:** hundreds or low thousands of fragments attached to one
   chapter, varied authors/works/extents/voices.
3. **Mixed rights/voice:** original, translations, blocked, absent, refusals,
   cross-chapter extents, and malformed/unsupported cases.

Keep fixtures outside published production data unless an owning test-fixture
path already exists.

### Measure

- generated index size compressed/uncompressed;
- per-book and per-chapter manifest size;
- first Catena route HTML/CSS/JS bytes;
- requests before Scripture appears;
- requests before first held commentary appears;
- fragment-text request count under representative reading;
- cold/warm cache behavior;
- time to interactive on representative desktop and throttled mobile hardware;
- main-thread render time for 10/100/500/1000 fragment chains;
- memory after opening many fragments;
- browser find behavior under lazy loading;
- URL/history performance;
- generator time and memory;
- public-site artifact growth;
- GitHub Pages path/request constraints;
- no-JavaScript truth;
- screen-reader/keyboard operation in the deep-chain fixture.

### Decision gate

Choose one of:

- current per-book/per-chapter scheme remains adequate;
- bounded manifest partitioning is needed;
- fragment metadata and fragment text need different chunking;
- search requires a separate lazy index;
- another change is justified by measured evidence.

No framework or server migration may be selected merely because the synthetic
fixture is large.

# Phase 3 — make acquisition a production system

## CO-04 — acquisition pipeline hardening

### Objective

Turn commentary acquisition from a successful pilot process into a repeatable
whole-canon production lane.

### Required pipeline stages

```text
L1 lead
 -> candidate work/edition identification
 -> rights triage
 -> artifact acquisition
 -> edition/artifact registration
 -> text extraction/transcription
 -> passage record creation
 -> Scripture-extent establishment
 -> chronology/attribution review
 -> voice/translation identity
 -> fragment verification
 -> generator validation
 -> Catena render review
 -> release eligibility
```

Each arrow must have a typed state or a documented refusal. A work cannot jump
from “AI says it comments here” to publishable fragment.

### Tooling goals

- deterministic candidate manifest;
- source/edition ID validation;
- duplicate-fragment detection;
- overlap and cross-chapter extent checks;
- canonical projection checks;
- title/work-extent checks;
- author/date/attribution validation;
- language/voice validation;
- rights-state enforcement before public generation;
- transcription provenance and artifact digest validation;
- generated coverage report;
- dry-run release eligibility report;
- rerunnable failure/resume semantics.

### Cold acquisition review

A reviewer samples both accepted and refused candidates. Passing only the happy
path is insufficient.

## CO-05 — breadth acquisition waves

### Objective

Expand beyond the initial solved commentary book without simply deepening the
already rich area.

### Selection algorithm

At the start of every breadth wave, generate a ranked candidate list from
current data. Score candidates using repository-owned facts only:

- canonical book/chapter currently under-covered;
- known L1 work availability;
- redistributable rights likelihood already established;
- stable artifact availability;
- exact locus tractability;
- original-language value;
- translation availability;
- chronological diversity;
- liturgical-reading intersection where a structured binding exists;
- acquisition/verification cost.

The score is a planning aid, not an authority claim. A human/agent reviewer may
override it with a recorded reason.

### Suggested breadth tranches

Do not freeze these as theological priority. Recompute against available source
truth.

- **B1:** ensure more than one biblical book is genuinely solved end-to-end;
- **B2:** establish representative Old Testament, Psalter/Wisdom, Gospel, Pauline,
  Catholic Epistle, and Apocalypse coverage;
- **B3:** cover every canonical book with at least one honestly solved locus
  where publishable commentary can actually be acquired;
- **B4:** move from book breadth toward chapter breadth within each major corpus
  region;
- **B5:** pursue whole-canon chapter coverage where source survival makes that a
  meaningful target.

A book with no lawful obtainable commentary is not failed work; it receives a
recorded acquisition state rather than invented filler.

### Acceptance per tranche

- all new fragments pass Catena model/generator checks;
- every displayed text has edition and rights identity;
- no lead appears as text;
- projection/refusal behavior tested on affected loci;
- route-level browser evidence for representative new books;
- generated coverage report checked against source records;
- independent source sample review;
- no release until bindings and public-only filters pass.

## CO-06 — depth acquisition waves

### Objective

Build a historically meaningful chain rather than one token fragment per book.

### Dimensions

- additional Fathers and early witnesses;
- medieval and scholastic commentary;
- later Catholic commentators where rights/source model permit;
- multiple works by a major commentator without title conflation;
- chronologically separated witnesses;
- disputed/pseudonymous material honestly labelled;
- full natural extents rather than arbitrary verse clipping;
- alternative source editions where a real comparison purpose exists.

### Anti-metric

“Fragments added” alone is not a success measure. A depth wave reports author,
work, period, language, rights, and chapter distribution so duplicated or
narrow growth cannot masquerade as breadth.

## CO-07 — commentary voice and translation expansion

### Objective

Make original and translated voices first-class without confusing language with
provenance.

### Work

- derive current voice coverage by work/fragment;
- identify public-domain or project-permitted translations;
- record translation-of-translation chains explicitly;
- add voice-specific fragment text only under an edition/translation owner;
- preserve original when translation is absent;
- add accessibility labels that say “author's own language” versus
  “English translation” rather than bare ambiguous language names;
- ensure URL state reproduces voice selection;
- test chapters where chosen voice is unavailable but another is held.

### Possible project-created translation lane

If Triptych later authorizes project-created translations, define it separately:
source text, translator/provider identity, revision, review, licence, and status
must be explicit. A draft AI translation is not silently equivalent to a
published historical translation.

# Phase 4 — deepen source and citation behavior

## CO-08 — exact source drill-down and fragment citation

### Objective

Make every fragment independently citable and auditable without cluttering the
chain.

### Deliverables

- stable fragment anchor design;
- visible human citation;
- source edition link;
- passage/artifact/segment route into Sources;
- rights acknowledgement at point of use;
- review/verification status;
- copy-citation action;
- return-to-Catena behavior preserving Scripture locus and voice;
- print citation form;
- tests proving anchors survive regenerated neighboring corpus data.

### Acceptance

A cold reviewer starts from the public fragment, follows the source chain to the
exact evidence, then returns to the same fragment without repository knowledge.

# Phase 5 — connect the corpus with typed edges

## CO-09 — Scripture <-> Catena

Owned jointly by the accepted Scripture implementation and Catena relationship
work.

### Minimum edge

`Scripture canonical extent -> has held commentary -> Catena derived view`

### Requirements

- edge generated from actual fragment extents;
- count, if shown, names the counted object type;
- no commentary link implies complete coverage;
- verse/range link maps through canonical identity;
- selected Bible projection preserved where possible;
- reciprocal return path;
- narrow/mobile evidence;
- no duplicate data store.

## CO-10 — Liturgy -> Catena

### Preconditions

- protected Liturgy owner explicitly authorizes a context seam;
- the liturgical unit has a structured Scripture binding;
- the current reader's four-action architecture remains intact.

### Product behavior

From Study/Details or another accepted low-chrome seam, expose
`Commentary on <exact locus>` when held commentary exists. If no held commentary
exists, do not add a noisy disabled action by default; a deeper Study state may
still explain acquisition status if that becomes an accepted product need.

### Return behavior

Catena should preserve enough referrer/context state, or Liturgy should encode a
stable return URL, so the reader can return to the same liturgical unit without
reconstructing the day manually.

### Explicitly forbidden

- fifth primary Day/Propers action;
- Catena pane beside the liturgy;
- non-Liturgy masthead injected into the protected reader;
- guessed Scripture binding from prose;
- source or commentary text duplicated into Liturgy's DOM merely for the link.

## CO-11 — History, Law, Sources, and Publications relationships

### Rule

Add only relationships whose owning domain has an exact structured edge.

Examples that may eventually be legitimate:

- a historical act explicitly governing a Bible/commentary edition or source
  history;
- a publication whose structured binding names the same Scripture locus;
- a Source passage that is the Catena fragment itself;
- a canon whose owning commentary/publication explicitly links the scriptural
  authority.

Keyword similarity is never enough.

# Phase 6 — typed discovery

## Existing J0 — Search product design

Catena contributes requirements, not a separate search product.

### Required Catena search jobs

- exact Bible citation -> Scripture/Catena targets;
- commentator name/alias -> author-qualified fragment/work results;
- commentary work -> work identity plus held fragment coverage;
- phrase within public fragment text;
- exact source/fragment ID;
- language/voice;
- period/date filter;
- explicit no-result and rights-withheld states.

## Existing J1 — public-only search benchmark

Measure:

- index bytes compressed;
- public-rights leak assertions;
- cold/warm query latency;
- worker/main-thread cost;
- mobile memory;
- exact citation precision;
- ambiguity handling;
- Latin/Greek/mixed-script behavior;
- fragment-text indexing cost;
- subpath compatibility.

## Existing J2 — selected search implementation

Only after J0/J1. Search may route to Catena fragments but never generate an AI
answer in place of them.

# Phase 7 — advanced Catena views

## CO-12A — in-page structured filtering

Add only after real deep chapters demonstrate need.

Candidate filters:

- commentator;
- work;
- historical period;
- original versus translation voice;
- language;
- held review state where reader-facing use is justified.

Default remains the complete applicable chronological chain. Filters are visible
and removable and belong in URL state if they materially change displayed
content.

## CO-12B — fragment comparison

Start with same-fragment comparisons because identity is strongest:

1. original + translation;
2. translation A + translation B;
3. edition/recension A + B when the Source model owns equivalence.

Do not start with model-generated “similar passages.”

## CO-12C — author/work trajectories

Derived views may show one author or one work across Scripture. Store no second
placement table. Reuse fragment natural extents and derived chapter membership.

## CO-12D — tradition threads

### Precondition

A typed thematic-edge schema and review process exists.

### Delivery

A thread names its theme, every supporting fragment, every Scripture locus, who
established/reviewed the edge, and what the edge means. It distinguishes:

- source explicitly says the theme;
- editor classifies the passage under the theme;
- AI proposed the edge, awaiting review.

Only reviewed edges reach the public thread.

## CO-12E — derived AI synthesis

### Precondition

The source chain and citation system are mature enough that synthesis can cite
stable fragments.

### Rules

- separate product surface/disclosure;
- provider/model/revision identity;
- exact fragment citations;
- no source-less claims;
- no rewriting absence into consensus;
- regenerate/review when cited fragment identity changes;
- never insert synthesis into chronological commentary chain;
- no implication of Magisterial authority.

This is optional. Catena is already complete as a source instrument without it.

# Phase 8 — continuous quality gates

## CO-Q1 — model/generator integrity

Every Catena-affecting branch runs:

- source/schema validation;
- Catena derivation check using the browser model itself;
- generated-data determinism;
- cross-chapter extent cases;
- malformed/hostile structured-data boundary tests appropriate to the production
  model;
- rights/public-filter tests;
- URL/hash/history contract tests.

Do not restore arbitrary implementation SHA pins as correctness tests.

## CO-Q2 — production browser contract

Maintain a curated production suite that covers product semantics, not every
historical hostile experiment. Required categories include:

- Scripture survives;
- held commentary renders;
- lead/blocked/refusal/absence/error distinctions;
- chronology/order;
- voice switching and absence;
- lazy text transport;
- focus recovery and visible focus;
- no-JavaScript truth;
- source/rights acknowledgement;
- URL state;
- print behavior;
- narrow layout.

## CO-Q3 — built-artifact Chromium gate

Every shared foundation or release change that reaches Catena runs the governed
viewport/state matrix over the **built artifact**, not source files alone.

Catena-specific assertions include:

- one `main`;
- no 320px horizontal overflow;
- practical targets under the accepted project rule;
- accessible names;
- no console/network failure;
- skip link lands on the correct landmark;
- focus visibility;
- overlay dismissal and return;
- solid/dashed distinctions survive forced colors;
- Scripture remains before commentary in narrow reading order.

## CO-Q4 — visual cold review

Capture comparable evidence at 1440x900, 1024x768, 768x1024, 393x852, and
320x852 plus 200% text and representative 400% zoom/reflow.

Reviewers answer:

- Is Scripture still obviously the anchor?
- Is the first commentator reachable without a wall of controls?
- Does a 50+ fragment chain still read as a chain rather than a database dump?
- Are lead/refusal states impossible to mistake for text?
- Does source apparatus remain quiet but discoverable?
- Does the shared shell dominate the page?
- Does mobile remain one reading order?

## CO-Q5 — rights cold review

Sample newly acquired fragments and prove the rendered text, edition,
translation, acknowledgement, and public artifact agree. A source being
publicly downloadable is not by itself a rights basis.

## CO-Q6 — accessibility cold review

Keyboard and screen-reader review is required on representative deep and sparse
chapters, not only the original pilot chapter.

# Phase 9 — release, integration, and deployment

## CO-R1 — candidate construction

An integration candidate contains only reviewed source, generated, test,
guidance, and release-record paths authorized for the wave. Do not use an old
feature branch as a patch queue without re-reading current main.

## CO-R2 — release binding

After source acceptance and under release authority:

- refresh only the exact changed published paths;
- regenerate rights records mechanically;
- do not hand-edit SHA-256 values;
- verify no unrelated stale path is carried forward.

## CO-R3 — pre-merge verification

At minimum for a material Catena release:

- Catena generator/model check;
- Catena source tests;
- curated Catena production suite;
- static browser checks;
- relevant shared browser-model gate;
- built-artifact Chromium Catena route;
- public-site build;
- public-preview verification;
- release-binding verification;
- public-alpha deployment-target verification;
- full discovery identity comparison against base, reported by identity rather
  than exit code alone.

## CO-R4 — independent integration review

Review exact candidate head. No self-acceptance.

## CO-R5 — merge and deploy

Only under maintainer authorization. Verify:

- intended commit is on `origin/main`;
- candidate ancestry is present;
- release bindings correspond to merged production bytes;
- Pages workflow reaches Configure/Upload/Deploy rather than failing earlier;
- live `/catena/` and representative data routes serve expected bytes;
- route behavior is checked in a real browser;
- rollback/recovery path is recorded.

# Phase 10 — whole-site acceptance

## Existing L0/L1 — visual/accessibility acceptance

Catena participates as the mature Instrument reference surface. Whole-site
acceptance should verify common identity without homogenizing Catena into the
same composition as Publications or Liturgy.

## Existing M0/M1 — final integration/cutover/review

The corpus program is not complete until the accepted Home, Publications,
Reader, Sources, Scripture, History, Law, Commentary, Search, relationships,
and protected Liturgy coexist under one navigable public product without
identity, accessibility, rights, or URL regression.

# Phase 11 — ongoing operations after “complete”

Catena Omnia is an accumulating corpus. Product completion does not mean source
acquisition stops.

## CO-O1 — periodic acquisition rounds

Run bounded, reviewable rounds with an explicit target: breadth, a particular
work family, original-language recovery, public-domain translation, or a
specific under-covered region.

## CO-O2 — source correction propagation

A corrected attribution, date, extent, edition, rights state, or transcription
must invalidate/regenerate every derived Catena view that depends on it.

## CO-O3 — stale relationship audit

When a fragment ID or Scripture extent changes, verify typed Search, Scripture,
Liturgy, thread, publication, and source links. No dangling derived edge may
silently point to a neighboring fragment.

## CO-O4 — coverage reporting

Generate internal reports for breadth/depth/voice/period/rights/review-state
coverage. Publicize only counts whose object definitions are stable and whose
values come from the same release artifact.

## CO-O5 — periodic cold product review

As corpus depth grows, repeat the product questions. A composition that is
excellent for ten commentators may fail for five hundred. Growth earns a new
review when measured evidence shows the existing design is no longer calm; size
alone does not authorize redesign.

# Suggested parallel work packets after CO-00

Once the current candidate receives an independent disposition, these work
packets can proceed in separate full checkouts when their owners are free:

| Packet | Scope | Can run while shell blocked? | Primary stop line |
| --- | --- | ---: | --- |
| P-A | CO-03 scale benchmark | Yes | Evidence and architecture decision only; no speculative rewrite. |
| P-B | CO-04 acquisition-pipeline hardening | Yes | No public corpus change without independent source review. |
| P-C | Next CO-05 breadth acquisition tranche | Yes | Candidate fragments only; release separately. |
| P-D | F1 Sources implementation | Per master-plan authorization | No global-owner collision. |
| P-E | I0/I1 Scripture design/implementation | Per master-plan authorization | Preserve Catena and canonical Bible identity. |
| P-F | B0/B1 blocker closure | Only with required ownership/carve-out | Mechanical scope only; no Liturgy redesign. |
| P-G | J0 Search design | Yes, if authorized | No engine selection or production Search before J1. |

Do not run P-D/P-E/P-F in parallel if they need the same shared generator,
layout, or CSS owner.

# Completion definitions

## “Catena interface complete”

The route is accessible, responsive, source-auditable, stable in URL behavior,
integrated with the accepted corpus shell, and has accepted Scripture/Source
transitions. This can be true long before whole-canon acquisition is complete.

## “Catena corpus broad”

Every major canonical region and eventually every book has at least one honestly
solved locus where surviving rights-permitted sources make that possible. Gaps
are explicitly acquisition gaps.

## “Catena corpus deep”

Representative loci contain multiple chronologically and linguistically diverse
commentators with exact source/rights identity, not merely duplicate editions or
near-identical fragments.

## “Catena Omnia mature”

The product can navigate the whole canonical space, derives all views from one
fragment truth, provides deep source/citation behavior, supports original and
translated voices, connects to Scripture and other Triptych products through
proved edges, scales under real corpus depth, and preserves epistemic
transparency under every supported state.

“Mature” still does not mean “all commentary in existence acquired.”

# Cold review of this roadmap

## Method

The roadmap was reread as an execution plan by a reviewer instructed to look for
unbounded scope, false dependencies, premature architecture, ownership
violations, release shortcuts, and the common failure mode of spending years on
framework work before increasing the actual corpus.

## Disposition

**ACCEPT WITH BINDING CONDITIONS — all conditions below are incorporated into
the roadmap above.**

### Findings

| Severity | Finding | Correction incorporated |
| --- | --- | --- |
| Critical | A purely serial roadmap would block valuable acquisition behind shared-shell and protected-Liturgy work. | Split the program into concurrent foundation, acquisition, relationship, and review/release tracks; acquisition/scale work may proceed without shell cutover. |
| Critical | Full-canon acquisition could multiply data before the current static model is proven at scale. | Insert CO-03 measured scale benchmark before large growth or transport redesign. |
| Major | The next agent could treat this new roadmap as authorization and bypass existing owners. | State explicitly that this is designed program guidance; existing master plan, ledger, and specific owners still grant authority. |
| Major | The current B0/B1 validation record contains a material internal inconsistency. | Make reconciliation of 24-vs-25 failure identities and branch commit count the first cold-review task in CO-00. |
| Major | Liturgy-to-Catena is valuable enough that a worker may rationalize entering protected files. | Put the transition behind a Liturgy-owned seam and explicitly forbid a fifth action, new masthead, guessed binding, or Catena pane. |
| Major | “Acquire the whole canon” is unbounded and can optimize raw fragment count. | Split breadth and depth waves; require generated multidimensional coverage reports and bounded tranches. |
| Major | Search or thematic work could precede exact Source/Scripture relationships and become inference-driven. | Sequence typed relationships before advanced navigation; Search remains J0/J1/J2; tradition threads require a reviewed edge schema. |
| Major | A new large corpus could create a second chapter-placement store for speed. | Keep natural extent as the only stored placement truth; benchmarks may change chunking, not semantics. |
| Major | Rights and translation work can be treated as post-processing after text acquisition. | Put rights triage before acquisition publication and make voice/translation a dedicated workstream with exact edition ownership. |
| Moderate | Product quality could be reviewed only on the original pilot chapter. | Require sparse, deep, new-book, mixed-rights, narrow-screen, and no-JS evidence in continuous gates. |
| Moderate | Source Library work and Catena citation could duplicate evidence presentation. | Keep Catena source disclosure concise and route full evidence into F1 Sources; test round-trip navigation. |
| Moderate | Advanced AI synthesis is seductive enough to become an early deliverable. | Place it late, optional, and dependent on stable fragment citations; source Catena is complete without it. |
| Moderate | Release binding and deployment could be bundled into implementation branches because generated hashes are mechanically obvious. | Preserve separate release authority, scoped refresh, independent integration review, and live verification. |
| Moderate | A single “complete” state is impossible for an accumulating commentary corpus. | Define interface-complete, broad, deep, mature, and ongoing operational states separately. |
| Minor | A fixed list of “important” biblical books could encode taste rather than current source opportunity. | Use a generated acquisition score and only illustrative breadth tranches; recompute from actual corpus/source facts. |

## Roadmap sanity conclusion

The roadmap is viable **only if the project continues to resist two opposite
failure modes**:

1. infrastructure perfectionism — endlessly hardening the shell while Catena
   still covers too little Scripture; and
2. corpus-count maximalism — ingesting huge amounts of text faster than rights,
   locus, chronology, source identity, accessibility, and static delivery can
   support.

The program should deliberately advance foundation and corpus value together.

## Exact next action from this roadmap

The next cold agent should **not** begin a new Catena feature.

It should first independently review the current
`impl/corpus-foundation-b0-b1` branch at its fetched remote head, including these
new vision/roadmap documents, reproduce the B0/B1 evidence from a clean checkout,
resolve the validation-record inconsistency, and issue an independent
disposition. Only after that disposition should an authorized continuation lane
select the next packet from the dependency map.

# Independent cold disposition, 2026-08-30

The required independent review was performed from a fresh full checkout at
exact fetched head `407dfad76061460e1b3f5e3ad65ea41c73c5f746`.

**Roadmap disposition: ACCEPT.** The roadmap sequences a measured whole-canon
scale benchmark before transport redesign, advances bounded acquisition breadth
and depth alongside foundation work, keeps source/rights/voice review in the
acquisition path, requires typed relationships before advanced navigation,
preserves Search as J0/J1/J2, and keeps review, release signing, deployment, and
protected-Liturgy authority separate. It does not require years of shell work
before adding corpus value and does not select a premature framework.

**CO-00 B0/B1 disposition: CHANGES_REQUIRED.** Two claimed fail-closed
properties are not enforced at the reviewed head:

1. `test_browser_model_gate.py` contains the coverage assertion that discovers a
   future JavaScript-driving suite, but `make check` runs only the modules named
   by `BROWSER_MODEL_TESTS`; it does not run that meta-test. The new suite can
   therefore remain absent from the gate and pass `make check`.
2. `SiteChromeScopeTest` does not prove the stated selector class. It misses a
   broad element selector such as `a`, treats a non-layout class inside
   `:not(...)` as positive page scope, and freezes the protected exception only
   by selector count rather than exact selector identity. Existing
   `scripture/scripture.css` `a` and `a:hover` rules demonstrate that
   `day-missal.css` is not proved to be the only remaining rule that would reach
   site chrome if instrument stylesheets were bundled.

The earlier “Exact next action” is now fulfilled and superseded. No Catena
feature lane is authorized by this review. A later bounded correction lane may
repair the two gates and request confirmation; the protected
`day-missal.css` blocker remains separately owned and untouched.
