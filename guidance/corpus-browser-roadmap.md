# Triptych corpus browser roadmap

## Status and authority

This is the detailed execution record for the non-PDF corpus experience
governed by [`corpus-browser-vision.md`](corpus-browser-vision.md).
`PROJECT-WORK.md` and `promised-deliverables.toml` remain the fail-closed
operational authorities for what is promised and complete. This roadmap records
the work-unit detail, evidence gates, and review dispositions they link to; it
does not grant production implementation, integration, publication, or
acceptance authority by itself.

The more specific [`liturgy-browser-vision.md`](liturgy-browser-vision.md)
continues to govern liturgical identity, semantics, state, navigation, and
reader behavior. Canonical Day and Propers are a protected surface family in
this wave. No corpus work may add a literal global masthead, fifth primary
action, second modal owner, Search integration, print redesign, or a competing
visual direction there.

PDFs remain the canonical printable editions. Wave 1 owns visual/product design
and isolated real-data prototypes; it does not own production application logic
or publication prose.

## Exact branch, base, and imported provenance

The A0-A4 foundation began from exact `origin/main` commit
`c27d6915319785686d1df6a1401a489aa9921f6f` on `ux/foundation`. The foundation
roadmap and A4 prototype record were selectively taken from
`ac37b6ffa6022dbab551385d91a12e277bb816cb`; the reviewed Codex foundation head
is `3b5938a0dba88831763ec09c762ae1572007a27e`. Accepted implementation and
architecture findings were inspected at Claude head
`af2c9613ccda48679face4e43f59c002f93056ef`. These SHAs identify reference
inputs; no foundation commit was merged as ancestry.

The current task-specific dispatch supersedes the v2 plan's integration-first
sequence for this Codex wave. `ux/corpus-wave-1` starts directly from exact
current `origin/main` commit
`c27d6915319785686d1df6a1401a489aa9921f6f` and carries forward only accepted
foundation knowledge and required artifacts path by path. The proposed
`corpus/foundation-integration` precursor was **not executed for this dispatch**.
That is a sequencing override, not a claim that the precursor was completed,
rejected, blocked, merged, or waived.

The reviewed Wave 1 head is
`e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`. The bounded correction branch
`ux/corpus-wave-1-review-fixes` starts from that exact commit. Feature-branch
checkpoints may be committed and pushed. Nothing in this roadmap authorizes a
merge or push to `main`, Pages deployment, public cutover, production behavior,
history rewriting, or force-push.

## State and disposition vocabulary

- **Planned**: sequenced but not authorized or started.
- **In progress**: authorized work has begun but has not produced a complete
  review candidate.
- **Candidate**: the committed tracked design and complete evidence package
  await independent disposition.
- **Accepted**, **changes required**, or **rejected**: an independent reviewer
  recorded the lane-specific decision and conditions in tracked authorities.
- **Complete**: every promised requirement and required independent disposition
  passed. A prototype, local check, commit, push, screenshot set, or ZIP cannot
  create this state by itself.

`Blocked` names an actual external dependency. It is not a synonym for pending,
difficult, unstarted, or awaiting ordinary review.

## Reviewed A0-A4 foundation disposition

The independent coordinator review accepted the product model and enough of
the design contract to authorize real-data Wave 1 work. It did not accept the
synthetic prototype as pixel-level production design; every real surface keeps
its own screenshot and external-acceptance gate.

| ID | Deliverable | Owner | State / disposition | Base / branch | Binding follow-up |
| --- | --- | --- | --- | --- | --- |
| A0 | [Repository and public-site inventory](corpus-browser-inventory.md) | Codex | **Accepted** | `c27d691` / `ux/foundation` | Use the route/object/ownership inventory; refresh counts only when release contents materially change. |
| A1 | [Scholarly corpus UX research](corpus-browser-research.md) | Codex | **Accepted** | `c27d691` / `ux/foundation` | Retain borrow/reject/exceed reasoning; research did not authorize a framework or IIIF migration. |
| A2 | Site-wide product and corpus architecture | Codex | **Accepted with coordinator amendments D1-D20** | `c27d691` / `ux/foundation` | “The corpus is the product; pages are typed views into it” governs Wave 1. |
| A3 | Tokens and Reader/Catalogue/Instrument archetypes | Codex | **Accepted as foundation direction only** | `c27d691` / `ux/foundation` | Token roles and archetypes may guide real-data design; exact pixels, heading sizes, masthead density, spacing, and font results are not frozen. |
| A4 | Shared navigation, Jump, Related, and shell interaction | Codex | **Accepted with amendments** | `c27d691` / `ux/foundation` | Jump remains bounded until J0-J2; Related is typed navigation, never recommendations; the protected liturgy adapter remains exclusive. |
| B0/B1 reconnaissance | Claude | **Accepted as implementation input** | `c27d691` / `impl/foundation` | Generator seams, static-host constraints, structural defects, URL compatibility, and existing browser harnesses are binding findings, not permission for a rewrite. |

## Binding coordinator decisions D1-D20

1. **Publications:** `/texts/` keeps its route and uses **Publications** as its
   compact public label. It is a discovery view, not a second owning catalogue.
2. **Protected liturgy:** do not modify canonical Day/Propers ownership,
   `reader-shell.js`, or `reader-instrument.css` while the separate Live Reader
   task owns those seams.
3. **Provider terminology:** use **Independent treatment** for a visible
   provider-qualified work and **Parallel treatment** only as a relationship
   label. Provider remains explicit metadata. A provider output is not a Source
   Library edition unless it satisfies that model.
4. **Archetypes:** Reader, Catalogue, and Instrument share identity, token
   roles, spacing logic, accessibility, URL discipline, and contextual
   navigation—not one universal layout.
5. **Visual roles:** retain warm paper, near-black text, restrained oxblood,
   strong blue focus, serif reading, UI sans fallbacks, square controls, quiet
   rules, restrained chrome, and content dominance. Exact values remain subject
   to real-data evidence; no production design may assume Inter is installed.
6. **Global navigation:** the durable destinations are Publications, Sources,
   Scripture, Liturgy, History, Law, and Commentary. The wordmark links Home;
   a separate Home item survives only if 1024-pixel and 200% evidence stays calm.
7. **Home:** preserve Faith, Scripture, Liturgy, History, Formation, Mary, and
   Law in their current order and identity unless a separately recorded
   repository-guidance amendment proves a better real-data alternative.
8. **One owning catalogue:** facets may aggregate treatments and formats but
   may not create another publication ownership hierarchy or PDF home.
9. **Web editions:** `web-editions.md` controls D0. Do not create or edit a
   second prose copy for presentation; preserve revision, colophon, omissions,
   and canonical PDF relationships.
10. **Durable memory:** decisive facts belong in tracked corpus guidance,
    owning surface guidance, `PROJECT-WORK.md`, and the promise ledger—not only
    chat, ignored handoffs, or `build/agent-continuity/`.
11. **Evidence:** use 1440x900, 1024x768, 768x1024, 393x852, and 320x852 plus
    200% text, exact 320 CSS-pixel reflow, representative 400% zoom/reflow,
    keyboard, forced colors, reduced motion, browser print where applicable,
    no-JavaScript truth, and console/network/HTTP/accessible-name checks. Do not
    create pixel baselines before a real-data surface is independently accepted.
12. **Static constraints:** no webfont or icon-library dependency, framework
    migration, root-relative link that breaks `/triptych/`, rejected asset
    type, server dependency, or unmeasured payload expansion.
13. **Search:** A4 Jump is only an explicit fixture. Production Search remains
    J0-J2; no page may present fixture title matching as global search.
14. **Relationships:** show only repository-owned structured edges. Never infer
    a connection from title, keyword, or intellectual plausibility.
15. **Rights and absence:** progressive disclosure may defer hashes, extended
    provenance, long legal apparatus, and secondary technical metadata. It may
    not hide required licence acknowledgement, withholding reason, typed
    absence/unread/unsupported/invalid state, or the difference between access
    and redistribution rights.
16. **Local progress:** defer it. If later proposed for publications it must be
    storage-optional and explicit URL state must win; Day retains no memory.
17. **Architecture debt:** repair shared/generator problems incrementally with
    path-specific proof. Do not turn B0 or any design lane into a browser-stack
    rewrite.
18. **Concurrent liturgy:** the Live Reader — Ritual Flow & Orientation promise
    remains separate and in progress. Re-read its eventual mainline result
    before entering any formerly protected seam.
19. **Git authority:** coherent feature-branch commits and pushes are allowed;
    main integration, deployment, force-push, and history rewriting are not.
20. **Checkout discipline:** parallel lanes use separate full checkouts and
    branches, never worktrees or a shared index.

## Wave 1 real-data design register

Independent review of `ux/corpus-wave-1` at exact head `e42b928...` produced a
split disposition. The review package was
`20260809T000346Z-corpus-wave-1-design-review.zip`; its manifest was
independently verified. The accepted rows do not make F0 or the shared shell
accepted.

| ID | Surface and bounded output | Independent disposition | Binding follow-up |
| --- | --- | --- | --- |
| C0 | **Home / corpus entry.** Task entrances plus seven editorial portals. | **Accepted.** | Preserve the accepted composition. Do not force every task above the fold at 200% text; preserve semantic order and reflow. |
| C1 | **Publications `/texts/`.** List-first discovery, facets, independent treatments, format availability, and zero state. | **Accepted.** | Preserve the composition and one-owning-catalogue rule. Redundant rule/spacing cleanup is optional implementation polish. |
| D0 | **Publication Reader.** One reading plane, provider and revision identity, Contents, rights, stable loci, and canonical PDF. | **Accepted.** | Preserve typography and interaction. Production must make identity and PDF truth static, retain hash/focus/table semantics, and treat browser print only as fallback. |
| E0 | **Catena Omnia.** Scripture anchor plus chronological and typed commentary chain. | **Accepted.** | Production may proceed independently without editing shared shell owners or protected Liturgy; preserve every held, lead, absence, refusal, and error state. |
| F0 | **Source Library.** Work -> Edition ownership with edition-owned sibling Artifact, Segment, and Passage records and a separate Passage controller relation. | **Changes required.** | Correct the false linear lede/hierarchy and one-passage navigation; production F1 remains blocked until the correction receives independent acceptance. |
| Shared shell | **Non-Liturgy shell.** Current domain, durable browse access, bounded Jump, responsive identity. | **Changes required.** | Use one wide current-location signal and a bounded wide Browse control; retain compact domain, Menu, and Jump. Final cutover remains blocked pending acceptance. |
| Accessibility and resilience | Production requirement. | **Accepted as a requirement; production proof outstanding.** | Production must prove one `main`, 320px no-overflow, focus/dialog behavior, forced colors, reduced motion, hash/history, `/triptych/` links, no-JS truth, and static PDF access. |
| Browser print | Non-canonical fallback. | **Accepted only as a non-canonical fallback.** | Hide interactive chrome and preserve obvious canonical-PDF access; do not reproduce the typeset PDF. |

### Review-fix checkpoint

The correction branch may change only the isolated design layer, focused tests,
and durable authorities needed to:

- make the Source lede and labels express the exact sibling/controller model;
- omit or unequivocally disable Previous and Next when an Edition has one
  Passage;
- remove duplicated wide current-domain identity;
- present one meaningful wide Browse control while retaining compact Menu and
  bounded Jump; and
- optionally remove Source-only redundant filter/result spacing when already
  touching that layout.

It may not redesign C0, C1, D0, or E0, implement production behavior, enter
protected Liturgy, change a PDF, route, hash contract, public build mapping, or
deployment state. Its fresh evidence must cover wide shell states on all five
surfaces, compact Home and Instrument states at 393px and 320px, corrected
Sources wide and narrow, the one-Passage state in normal and forced colors, and
keyboard focus on the wide Browse control.

The new ZIP is evidence transport, not acceptance. At this checkpoint F0 and
the shared shell remained **changes required** until an independent reviewer
accepted the corrected states and that disposition was recorded here and in
the fail-closed authorities.

### Final correction disposition

Independent review of packaged head
`ecbd93a0575c4b890cc814af7cd20d01f5af7beb` and the fresh immutable package
`20260809T021953Z-corpus-wave-1-review-fixes.zip` (SHA-256
`d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`)
recorded both required dispositions:

- **F0 Source Library — ACCEPT.** The corrected design distinguishes
  Work/Edition ownership from the Artifact/Segment relation controlling
  Passage text. Its reviewed one-Passage state retains the selector, exact
  `Passage 1 of 1`, rights, provenance, and inspection-scope truth while
  omitting impossible Previous and Next actions.
- **Shared non-Liturgy shell — ACCEPT.** Wide surfaces show exactly one
  current-location signal, no duplicate wide domain identity, and Browse as a
  bounded destination control distinct from Jump. Compact surfaces preserve
  domain identity, Menu, Jump, target sizing, and no document-level overflow
  at 393 and 320 CSS pixels.

These dispositions preserve C0, C1, D0, and E0 and the protected Liturgy, PDF,
production-route, and hash boundaries. They close only the F0 and shared-shell
design-review gates; the disposable overlay remains design evidence rather
than production application logic.

The following findings are non-blocking only for design acceptance and retain
their distinct downstream classifications:

- the inherited nested-`main` defect remains a production blocker;
- Reader table-cell reflow and full no-JavaScript behavior remain production
  obligations;
- implementation and hardening must add comprehensive Menu/Browse destination
  activation tests;
- the prototype stylesheet used 8,171 of its 8,192-byte gzip-9 ceiling and
  supplies neither meaningful extension headroom nor a production CSS budget;
  and
- the stale Fortescue Artifact note remains with its proper source-data
  authority owner and is not corrected by this disposition.

## E1 Catena integration candidate — 2026-08-28

The convergence review branch `review/catena-e1-convergence` (commit
`f1a5bbad763b847ded8799748223898de6ad4de9`) recorded
**`READY_FOR_INTEGRATION_BRANCH`** with zero `MERGE_BLOCKER` and zero
`INTEGRATION_BLOCKER` findings, **`CANCEL_V17_SEMANTIC`**, three
`HARDENING_BACKLOG` findings, eight `EVIDENCE_TOOLING_BACKLOG` findings, and
twenty `SEPARATELY_OWNED` concerns. Acting on that disposition,
`integration/catena-e1` was built from the exact authorized main base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` (origin `main` had not moved past
it) with the reviewed V16 source `cc1f2fb8625f044558c26edd358b99cd7dcc7646`
used as final implementation truth, not as a patch queue. The candidate
carries the manifest only: the final route-owned
`src/web/browser/catena/catena-model.js`, `catena.js`, `catena.css`, and
`index.html` (main had made no independent change to them since the reviewed
fork); the `scripts/_catena.py` voice-authority change with its deterministic
regeneration of `src/web/data/structure/catena/index.json` (adding the held
`voices` key `original`, `translation:en`, `translation:la`) and the Isaiah 8
chapter file `27-is/008.json`, byte-identical to the reviewed V16 generated
output; the 78-line generator-contract expansion of `tools/tests/test_catena.py`;
and `tools/tests/test_catena_production.py`, 419 production-policy regressions
curated verbatim from the V16 wave-1 suite (publication atomicity,
owner/completion identity, same-path/late isolation, exact voices with
`translation:grc` refusal, refusal/absence/provenance truthfulness, path
namespace closure, cache completion isolation, malformed canonical data, and
the governed budget assertions). The 17,315-line synthetic harness, the
hostile prototype/getter/thenable classes, evidence tooling, and V16-side
records were excluded; the three hardening findings and eight evidence-tooling
findings remain backlog, and the twenty separately owned concerns were not
touched. Release bindings were not refreshed; no merge, deploy, or release
signing occurred.

Fresh validation on the candidate: `python3 scripts/_catena.py check` reports
1,351 fragments / 1 book / 73 canon entries; `test_catena.py` 56/56 and the
curated suite 419/419 under node; static browser checks 5/5; real-Chromium
route-only runs over `/catena/index.html` produced the same 121 assertion
identities with the same 95 pass / 14 inherited shared-shell fail / 12 skip
statuses at the exact base and at the candidate, zero status changes; full
discovery ran 1,736 tests at the base (46 failures, 13 errors, 11 skips) and
2,159 tests at the candidate with the identical failure and error identities
and zero Catena failures; governed gzip-9 budgets measure CSS 7,629/8,000
whole, JS 12,965/13,000 whole, with the suite's stripped-ceiling assertions
passing (2,700 and 8,800) and `catena-model.js` uncapped. Status: **awaiting
independent integration review**, per the fixed loop (one independent review,
at most one bounded correction pass, one confirmation review, merge). E1 is
not accepted and not integrated.

The independent integration review (branch `review/catena-e1-integration`,
commit `c3698563e3b45e35a672db37616e39ef27eb3d08`) then returned **CHANGES
REQUIRED** against candidate head
`9810a29c38f6138069d11cb7c735d8bb8b190326`: two `MERGE_BLOCKER` findings, two
`BOUNDED_INTEGRATION_CORRECTION` findings, `GenuinelyLateStaleWorkTest`
ratified, and one new `HARDENING_BACKLOG` finding (the empty no-JavaScript
`h2`). The one authorized bounded correction pass fixed exactly those four and
opened no lane:

- **Translation-absence identity.** `renderAbsences` rendered
  `.absence-author` and `.absence-work` as adjacent element children, so a row
  flattened to `Ambrose of MilanHexameron` for a screen reader, a copy, or a
  text-only rendering. A semantic `' — '` text node now stands between them,
  written only where both halves are present, matching the `renderLeads`
  convention — a DOM delimiter, not a CSS gap, because a gap is not text.
  `AbsenceRowFlatteningTest` pins the flattened text and the child-node order on
  the real production route, with an adjacent-identity control over further real
  rows and the disclosure state asserted unchanged.
- **Keyboard recovery focus.** Recovery lands on `#reading`, where the shared
  shell's `.reading:focus { outline: none }` out-ranked the universal
  `:focus-visible` rule and the browser drew nothing. One rule,
  `.catena-page .reading:focus-visible { outline: 3px solid var(--focus); }`,
  restores a keyboard-only ring in the section's own violet ink; the shared
  shell is untouched, the mouse case stays undecorated, and the offset survives
  from the universal rule. `tools/tests/catena_recovery_focus_gate.mjs` drives
  real Chromium over the BUILT artifact and reads `getComputedStyle` on the
  element the browser reports as active, on the success path and the reviewed
  failure/recovery path, requiring a painted ring distinguishable from the
  region at rest at 3:1 contrast or better (measured 10.95:1); it exits 3, and
  its Python test skips with the enabling variable named, when no browser or no
  build is present.
- **Curated-suite cleanup.** The forbidden candidate SHA pin is gone and not
  replaced; twelve hostile/evidence-only classes, one hostile method and every
  harness seam that existed only for them are gone; the over-wide 2026-08-11
  print pin is narrowed to the one focus rule that now exists;
  `GenuinelyLateStaleWorkTest` is retained as ratified; and the ordinary
  coverage lost with the hostile classes is restored (chronology, absence and
  paragraph counts, author-filter recovery, leads copy, shared-field generator
  drift, null/list bootstrap truth, visible failure text, unregressed
  Scripture). The disproved `8 hostile + 40 non-manifest` split is replaced by a
  measured inventory counted the same way for both files: 71 runnable classes /
  394 tests here against 105 / 604 in wave-1, so 36 runnable classes and 221
  tests omitted, 2 classes and 13 tests added by the correction, and three
  dependency-only bases each side. All nine required coverage categories remain
  represented.
- **Record integrity.** The candidate ledger entry now carries its one
  `<!-- promised-deliverable: … -->` work-register marker, the recorded
  generator command is the executable `python3 scripts/_catena.py check` rather
  than the mode-644 `scripts/_catena.py check`, and full discovery was rerun at
  the exact base and the exact corrected head.

Fresh validation at the corrected head: `python3 scripts/_catena.py check`
reports 1,351 fragments / 1 book / 73 canon entries; regeneration of
`src/web/data` is byte-identical (zero changed paths); `test_catena.py` 56/56
and the corrected curated suite 394/394 including the live Chromium gate; static
browser checks 5/5; governed gzip-9 budgets CSS 7,921/8,000 whole and
2,698/2,700 stripped, JS 12,992/13,000 whole and 7,843/8,800 stripped, no
ceiling raised; real-Chromium route-only runs over `/catena/index.html` produce
the same 121 assertion identities and the same 95/14/12 statuses at the exact
base and the corrected head, zero identity and zero status changes; full
discovery ran 1,736 tests at the base and 2,134 at the corrected head, both
reporting 46 failures, 13 errors and 11 skips over the identical 24 failure and
13 error identities, so zero new integration-caused failure identities and zero
Catena failures. Status:
**awaiting one confirmation Codex review** scoped to these four corrections and
a regression check. E1 remains unaccepted and unintegrated; no merge, deploy,
release signing, or self-acceptance occurred.

## Structured-data limits and blocked follow-ups

Safe current relationship categories are explicit containment,
passage-to-artifact/segment, Catena fragment-to-Scripture locus, Catena
passage-to-Source Library passage, act descent/change/history,
document-to-owning-catalogue page, and Mass-to-propers-to-Scripture resolution.
Even these appear only where the actual record exposes the edge.

The following are **blocked on separate repository-owned schema, generator,
and verification work**, not blockers to producing honest Wave 1 designs:

- `translation_of`, `used_by`, `derived_from`, inferred canon
  correspondences, Law-to-Source citations, and generic Related edges;
- a corpus-wide typed relationship projection with direction, derivation,
  revision, and public/no-leak guarantees;
- a true global Search index and recognizers for citations, aliases, IDs, and
  multilingual text (J0-J2);
- side-by-side provider comparison until both browser-readable treatments and
  stable alignment semantics are proven;
- IIIF viewing until a concrete witness, rights disposition, and measured
  accessibility/performance need exist;
- an honest unread passage or commentary-fragment fixture: all 2,751 current
  passages are inspected, so unread remains a future schema/data state and must
  not be fabricated for design evidence;
- disputed-attribution and held-unrenderable Catena presentation until a lawful
  structured record exists; the current generated Catena has no admissible
  instance of either state;
- local reading progress, generated freshness/featured claims, or corpus counts
  without deterministic release-owned inputs.

Designs may show an explicit unsupported/absent state or record a future corpus
opportunity. They must not simulate the missing relationship, search result,
comparison, text, or metadata in the UI.

## Remaining program sequence

| Work | Current state | Exact dependency / stopping line |
| --- | --- | --- |
| B0/B1 shared non-liturgy implementation and harness | Steps 1-4 and 9 satisfied on `main`; step 5 partial; remediated candidate on `impl/corpus-foundation-b0-b1`, awaiting independent rereview | The step-by-step disposition, evidence, and the one remaining blocker are `guidance/corpus-browser-implementation.md` §11.1, the cold disposition is §11.2, and the remediation of its two `CHANGES_REQUIRED` findings is §11.3, which own them; do not restate the matrix here. Steps 6, 7, and 8 are not open work for this lane: 6 is withdrawn by D2/D18, and 7 and 8 wait on a surface lane that needs them. The blocker is `day-missal.css`'s twelve unscoped `body > .site-header` selectors, which need a protected-Liturgy carve-out. |
| C2/D1 production surface implementation | Eligible after the shell ownership boundary is clean | C0/C1/D0 are accepted; avoid branches that contend for global generator, site CSS, release binding, or shell files. |
| E1 Catena production implementation | **Complete, merged, and live from `main`** | Confirmed by review `7dfd944494a8d9355264579156214f16d3722a9f`; candidate `b832cdc5b` merged as `85f41e4e4`; ledger entry `complete`. A closed lane: a later shared change reaching `/catena/index.html` must prove no product regression there. |
| F1 Sources production implementation | Eligible only for separate owner-authorized dispatch | The F0 design-review dependency is satisfied; no production implementation is started or authorized by this disposition. |
| Final shared-shell cutover | **Blocked** | The shell design-review dependency is satisfied; cutover still requires a clean implementation-foundation checkpoint and explicit cutover authority. |
| G0/H0/I0/J0 and implementation partners | Planned Wave 2 | Do not begin merely because Wave 1 prototypes exist; follow owning guidance and exact accepted dependencies. |
| K0/K1 typed relationships | Planned | Requires accepted owning surfaces and verified structured edges; schema gaps above remain explicit. |
| L0/L1 visual and accessibility acceptance | Planned | Requires implemented representative surfaces and complete real-data matrices. Automated checks cannot supply independent visual judgment. |
| M0/M1 integration, cutover, and final acceptance | Planned | Requires accepted lanes and explicit maintainer publication authority. This branch may not merge or deploy main. |

## Progress ledger

| Date | Work | Evidence-backed result | Commit or handoff |
| --- | --- | --- | --- |
| 2026-08-08 | A0-A4 foundation | Inventory, research, corpus architecture, three archetypes, isolated synthetic prototype, Menu, bounded Jump, typed Related, responsive behavior, and browser gates were produced from `c27d691`; the coordinator accepted A0/A1, accepted A2/A4 with D1-D20 amendments, and accepted A3 as direction only. | Source roadmap/prototype commit `ac37b6f`; reviewed Codex head `3b5938a`; Claude findings head `af2c961`. |
| 2026-08-08 | Direct Wave 1 dispatch | Created `ux/corpus-wave-1` directly from current `origin/main` `c27d691`; did not execute or merge the proposed foundation-integration precursor; authorized C0, C1, D0, E0, and F0 real-data visual/product work. | Base `c27d6915319785686d1df6a1401a489aa9921f6f`; branch `ux/corpus-wave-1`; external acceptance open. |
| 2026-08-09 | Wave 1 Candidate checkpoint | Completed the isolated real-route prototype and 83-case matrix over all five surfaces. The exact browser report records 1,979 assertions, 1,917 passes, 62 disclosed inherited findings, and zero gating failures; 83 main captures and every page of the 236-page print were inspected. Protected Liturgy, PDFs, prose, production browser sources, release bindings, and deployment remain unchanged. | `build/agent-handoffs/20260809T000346Z-corpus-wave-1-design-review/`; exact branch head and ZIP digest are recorded in the handoff; external acceptance remains open. |
| 2026-08-08 | Independent Wave 1 review | Accepted C0 Home, C1 Publications, D0 Reader, and E0 Catena; required changes to F0 and the shared non-Liturgy shell; accepted accessibility/resilience as a production requirement and browser print only as a non-canonical fallback. | Reviewed head `e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`; verified package `20260809T000346Z-corpus-wave-1-design-review.zip`. |
| 2026-08-08 | Review-fix dispatch | Authorized `ux/corpus-wave-1-review-fixes` from exact reviewed head for bounded F0, shell, evidence, and authority corrections only. | F0 and shell remain changes required pending a fresh independent disposition; no production/main/deploy authority. |
| 2026-08-09 | Review-fix implementation and test checkpoint | Completed the bounded F0 and shared-shell prototype corrections without reopening C0, C1, D0, or E0. The full capture run covered 85 real-route cases and 2,296 assertions with zero gating failures. Its 64 disclosed non-gating findings comprise 52 inherited nested-`main` findings, eight before-state useful-content findings, two before-only narrow-overflow findings, and two inherited Reader no-JavaScript overlay limitations. Protected Liturgy production and canonical PDF paths have zero reviewed-base-to-head changes. | Authority reconciliation `3bfb9df10e1bd4b8d4d2b56aeb430c897f67700a`; design/test head `c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6`. F0 and shell remain changes required until independent acceptance. The earlier correction package `20260809T014145Z-corpus-wave-1-review-fixes` is superseded for protocol defects; a fresh immutable package follows this tracking repair. |
| 2026-08-09 | Final F0 and shared-shell design review | Independent review recorded **F0 Source Library — ACCEPT** and **Shared non-Liturgy shell — ACCEPT**, preserving C0/C1/D0/E0 and protected Liturgy/PDF/routes/hashes while carrying the disclosed production and data obligations forward. | Reviewed and packaged head `ecbd93a0575c4b890cc814af7cd20d01f5af7beb`; package `20260809T021953Z-corpus-wave-1-review-fixes.zip`; SHA-256 `d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`. |
| 2026-08-28 | E1 Catena integration candidate | Built `integration/catena-e1` from the exact convergence-authorized main base per the review's bring-across manifest: final Catena route/model/HTML/CSS, the generator voice-authority change with its deterministic generated data, the generator-contract test expansion, and 419 curated production regressions. Fresh validation passed structure (1,351/1/73), focused Catena (56 and 419), static checks 5/5, identical 121-identity Chromium route runs at base and candidate (95/14/12, zero changes), governed CSS/JS budgets, and full discovery with zero new failure identities and zero Catena failures. Status **awaiting independent integration review**; not accepted, not integrated, no merge/deploy/release binding. | Convergence review `f1a5bbad763b847ded8799748223898de6ad4de9`; integration base `2778285849f2973ea89d1cfd5b2751ed4ae58e54`; V16 source `cc1f2fb8625f044558c26edd358b99cd7dcc7646`; branch `integration/catena-e1`; candidate head is the commit carrying this row. |
| 2026-08-28 | E1 Catena bounded integration correction | Independent integration review `c3698563e3b45e35a672db37616e39ef27eb3d08` returned **CHANGES REQUIRED** (2 `MERGE_BLOCKER`, 2 `BOUNDED_INTEGRATION_CORRECTION`, `GenuinelyLateStaleWorkTest` ratified, one new `HARDENING_BACKLOG`). The one authorized bounded pass fixed exactly those four: a semantic DOM delimiter between the absence author and work (`Ambrose of MilanHexameron` no longer flattens into one word), a keyboard-only visible focus ring for recovery on `#reading` proved in real Chromium on the success and failure paths, curated-suite cleanup with the SHA pin and hostile machinery removed, lost ordinary coverage restored and a measured 71-class/394-test inventory replacing the disproved `8 + 40` split, and record integrity (work-register marker, executable `python3 scripts/_catena.py check`, discovery rerun at exact base and head). Zero new integration-caused failure identities; zero Chromium route identity or status changes; no ceiling raised. Status **awaiting one confirmation Codex review**; not accepted, not integrated, no merge/deploy/release binding. | Integration review `c3698563e3b45e35a672db37616e39ef27eb3d08`; reviewed candidate head `9810a29c38f6138069d11cb7c735d8bb8b190326`; integration base `2778285849f2973ea89d1cfd5b2751ed4ae58e54`; branch `integration/catena-e1`; corrected head is the commit carrying this row. |
| 2026-08-30 | B0/B1 current-main convergence candidate | Reconciled the B0/B1 sequence against `origin/main` `094379074` path by path rather than replaying the old hardening branch. Steps 2, 4, and 9 were already satisfied and were left alone; step 1's baseline was re-measured (2,707 tests, 24 failures, 0 errors, 11 skipped, all 24 in `test_tool_registry`, nothing browser-related red); step 3 was missing and is implemented as `check-browser-models` (12 modules, 358 tests, about 162 s, inside `make check`) with `test_browser_model_gate.py` holding its coverage honest; step 5's (a), (b), and (c) were confirmed landed on `main`, a fifth hazard of the same class was found in `sources.css` and scoped, and (d) `day-missal.css` remains blocked by protected Liturgy. Steps 6, 7, and 8 were deliberately not executed. Neutrality proved by real Chromium: 19 routes x 9 states, base and candidate identical at 2,290 assertions, 1,850 passed, 212 failed, 228 skipped, with byte-identical rows including every detail string; five reader harnesses all-green; full discovery unchanged from the base. One deliberately stale release binding, `src/web/browser/sources/sources.css`, is left for the release step. Status **awaiting independent review**; no merge, deploy, release signing, or self-acceptance. | Dispatch base `09437907472581df4a8969010bd494249a3539a5`; branch `impl/corpus-foundation-b0-b1`; the step matrix and the exact carve-out are owned by `guidance/corpus-browser-implementation.md` §11.1 and are not restated here; candidate head is the commit carrying this row. |
| 2026-08-30 | Independent B0/B1 cold disposition and Catena Omnia review | **B0/B1 — CHANGES REQUIRED.** The named gate is narrow and reaches its present modules, but its future-suite meta-test is not itself under `make check`; the collision detector misses broad element selectors and negative pseudo-class scope and freezes the protected exception only by count. Exact-host discovery is 2,707 / 23 failures / 10 skips at base and 2,719 / 24 failures / 10 skips at head, with exactly one new stale-binding oracle identity; the twelve named modules are 362 tests and took 166 s without fail-fast. Chromium remains byte-identical at 2,290 rows. Protected Liturgy and closed Catena E0/E1 remain untouched. **Catena Omnia vision — ACCEPT_WITH_CORRECTIONS:** narrow projection-refusal order was reconciled with accepted E1 behavior. **Catena Omnia roadmap — ACCEPT:** scale, acquisition, typed-edge, Search, authority, review, and release sequencing are sound. No merge, deploy, signing, Liturgy edit, or next feature lane is authorized. | Reviewed base `09437907472581df4a8969010bd494249a3539a5`; reviewed candidate `407dfad76061460e1b3f5e3ad65ea41c73c5f746`; correction commit is the commit carrying this row. |
| 2026-08-30 | B0/B1 cold-review remediation candidate | Fixed exactly the two `CHANGES_REQUIRED` findings and nothing else. (1) The coverage meta-test is now a `check` prerequisite: a separate `BROWSER_MODEL_GATE_TESTS` variable and a `check-browser-model-coverage` target that `check-browser-models` requires, so it runs before the model loop; the module grew 8 to 22 tests, walking the prerequisite graph from `check` and replaying `make -n` rather than trusting the text, and a synthetic unnamed browser-driving suite now makes both targets exit 2. (2) The collision detector no longer reads selector text for class names: it renders the build's own `wrap_in_layout` for both shells and asks whether a selector can match a chrome element, with `:not()` and `:root` evaluated, positive-only scope, `:is()`/`:where()` scoped only when every alternative is, and anything unclassifiable raising; bare `a` and `.site-header:not(.route-only)` are now caught, the protected exception is four files with exact ordered selector inventories rather than the count twelve, and the suite grew 15 to 32 tests. Three further unscoped hazards of the same class were found inside the protected reader family (`reader-shell.css`, `reader-instrument.css`, `reader-visual-reset.css`) and are recorded with their authority, not corrected. `scripture.css`'s bare `a`/`a:hover` are scoped through `:where(.plan-page, .track-page)`; measured in Chromium, in-content links are unchanged and the footer links return from `rgb(69, 63, 56)` to the site-owned `rgb(143, 53, 64)` that `/texts/`, `/law/`, `/history/` and `/sources/` already render — the intended effect, disclosed on `no-visual-or-product-decision`. The named gate is now 13 modules and 401 tests where it was 12 and 362; the Chromium artifact gate stays byte-identical at 2,290 rows / 1,850 pass / 212 fail / 228 skip; discovery is 2,719 / 24 / 0 / 10 at base and 2,750 / 24 / 0 / 10 at the candidate with identical failure identities and the 31 new tests accounted for. Two release bindings are deliberately stale and unrefreshed. `shared-shell-blocking-collisions-resolved` stays `blocked`. Status **awaiting independent cold rereview**; no merge, deploy, signing, binding refresh, self-acceptance, protected-Liturgy edit, Catena edit, or next lane. | Remediation base `e135e65bbea80877eb75a39945b750fc7566642f`; branch `impl/corpus-foundation-b0-b1`; the findings, the strengthened contract and its stated limits, the four exact inventories, and every measurement are owned by `guidance/corpus-browser-implementation.md` §11.3 and are not restated here; candidate head is the commit carrying this row. |

| 2026-08-31 | B0/B1 selector-oracle remediation candidate | The third independent cold review reproduced two classes of unsoundness in the Python selector analyzer for VALID CSS — unmodelled pseudo-classes treated as satisfiable, which reverses conservative reasoning inside `:not()` (`a:not(:hover)`, `.site-header:not(:focus-within)`, `[class~="SITE-HEADER" i]`), and route scope inferred from raw text (`a[href$=".html"]`, a `:has()` global alternative, a `:is()` tautology) — so the analyzer's "fails closed" claim was false. The verdict moved to the browser: `tools/tests/site_chrome_selector_oracle.mjs` drives one real Chromium over 36 shells rendered by `wrap_in_layout` (neutral, all thirteen published browser pages, four site pages) and answers per arm whether it selects a layout-owned element, under a bounded user-state walk (hover, active, keyboard focus/`:focus-visible`, fragment target) on the deciding states; refusals (invalid/unsupported here, or `:visited`) are reported and unsafe, pseudo-element arms are judged by their origin with a sentinel proving the direction, and Python keeps only extraction, identity normalization, orchestration and inventory comparison — the hand-written matcher and scope inferencer are deleted. The verdict is a differential: unsafe means reaching chrome in the neutral shell, whatever route-looking text an arm carries. All six counterexamples are now caught with recorded witnesses; the browser reproduces the four protected inventories exactly (12/3/2/3) and finds zero new hazards across 1,193 arms; Scripture's accepted scoping classifies safe; no production byte changed, so the stale-binding set stays exactly Scripture and Sources CSS. `test_browser_collisions` is 34 tests in 9.1 s in one session; `test_browser_model_gate` stays 22/OK. `shared-shell-blocking-collisions-resolved` stays `blocked`. Status **awaiting independent cold rereview**; no merge, deploy, signing, binding refresh, self-acceptance, protected-Liturgy edit, Catena edit, or next lane. | Instruction commit `2440e3e84929c81bc42631bcd3622c592f71da39`; branch `impl/corpus-foundation-b0-b1`; the architecture, the state matrix and its bound, the refusal policy, and every measurement are owned by `guidance/corpus-browser-implementation.md` §11.4 and are not restated here; candidate head is the commit carrying this row. |

## Next Codex tasks

No further Codex design or implementation task is authorized by this
acceptance. After this acceptance/continuity-only update is committed and
pushed and its resulting HEAD SHA is reported, stop. Production implementation
remains owned by the appropriate Claude lanes under separate authority. This
acceptance does not authorize merging the disposable prototype, merging or
pushing `main`, deployment, public cutover, protected Liturgy edits, or
canonical PDF changes.

Append later findings and dispositions. Do not rewrite earlier rows to make the
sequence appear cleaner.
