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

The new ZIP is evidence transport, not acceptance. F0 and the shared shell
remain **changes required** until an independent reviewer accepts the corrected
states and that disposition is recorded here and in the fail-closed authorities.

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
| B0/B1 shared non-liturgy implementation and harness | Authorized separately; not owned by this design branch | May use accepted A3/A4 direction and implementation findings; must stop before inventing C0/C1/D0/E0/F0 compositions and must not enter protected liturgy files. |
| C2/D1 production surface implementation | Eligible after the shell ownership boundary is clean | C0/C1/D0 are accepted; avoid branches that contend for global generator, site CSS, release binding, or shell files. |
| E1 Catena production implementation | Authorized independently | E0 is accepted; do not edit shared shell/global owners or protected Liturgy. |
| F1 Sources production implementation | **Blocked** | Requires independent acceptance of the F0 correction. |
| Final shared-shell cutover | **Blocked** | Requires independent acceptance of the shell correction and a clean implementation-foundation checkpoint. |
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

## Next Codex tasks

1. Complete the bounded F0 and shell corrections without reopening C0, C1, D0,
   or E0; run and inspect the focused real-data evidence matrix.
2. Produce a fresh verified one-root correction ZIP and obtain independent
   accepted, changes-required, or rejected dispositions for F0 and the shell.
3. Keep F1 and final shell cutover blocked until those exact dispositions are
   accepted and recorded. E1 may proceed independently within its ownership
   boundary; C2/D1 wait for a clean shell ownership checkpoint.
4. Do not merge or deploy `main`, alter protected Liturgy, change a canonical
   PDF, or infer missing source relationships.

Append later findings and dispositions. Do not rewrite earlier rows to make the
sequence appear cleaner.
