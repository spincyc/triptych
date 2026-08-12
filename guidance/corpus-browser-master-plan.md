# Triptych corpus browser master plan

## Status and authority

This is the current program-level authority for Triptych's non-PDF corpus
experience. It replaces the superseded v1 dispatch, integration precursor,
agent prompts, and amendment stack that formerly appeared in this file. A
fresh contributor should not reconstruct current instructions from that
historical sequence.

The original independent review disposition applied to:

- reviewed branch: `ux/corpus-wave-1`;
- reviewed head: `e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`;
- reviewed package: `20260809T000346Z-corpus-wave-1-design-review.zip`;
- review date: 2026-08-08; and
- package manifest: independently verified.

The correction checkpoint is
`ux/corpus-wave-1-review-fixes`, created from that exact reviewed head. It may
record dispositions, correct F0 and the shared non-Liturgy shell in the
isolated design prototype, reconcile durable authority, create review evidence,
commit, and push that named feature branch. It may not merge or push `main`,
deploy, cut over production, implement production behavior, rewrite history,
alter canonical PDFs, or enter protected Liturgy.

For this dispatched program, Codex owns product and visual design,
design-correction evidence, and independent product review. Claude owns
production implementation, coding, and implementation testing on the named
implementation lanes. That role split does not authorize either side to cross
single-owner files, integrate a retained worker, accept its own work, merge,
deploy, or bypass the explicit stopping lines below.

The governing documents divide responsibility as follows:

- this file owns program boundaries, reviewed decisions, work sequencing, and
  authority;
- [corpus-browser-vision.md](corpus-browser-vision.md) owns site-wide product,
  visual, interaction, responsive, accessibility, URL, and performance rules;
- [corpus-browser-roadmap.md](corpus-browser-roadmap.md) owns work-unit state,
  evidence, and review disposition;
- [corpus-browser-implementation.md](corpus-browser-implementation.md) owns
  generator seams, measured technical facts, risks, and safe implementation
  order;
- specific surface guidance owns its data and semantics; and
- `PROJECT-WORK.md` and `promised-deliverables.toml` remain the fail-closed
  operational authorities for promised completion.

No one of these files may silently grant authority withheld by another. The
more specific owning guidance controls within its subject.

## Mission

**The corpus is the product; pages are typed views into it.** Triptych should
let a reader move among publications, source evidence, Scripture, commentary,
Liturgy, historical acts, and law without blurring the identity, authority,
rights, availability, or uncertainty of any object.

The Liturgical Instrument remains the quality benchmark for calm reading,
disciplined measure, restrained chrome, useful first content, source honesty,
responsive reflow, and accessible operation. It is also a protected exception,
not a template to be wrapped in new global chrome.

Installed reviewed PDFs remain the canonical printable editions. Browser
print is a useful non-canonical fallback and must not become a collateral
typesetting project.

## Non-negotiable boundaries

1. Preserve public routes, route-owned hashes and queries, canonical PDF
   relationships, provider identity, rights and absence states, and the static
   GitHub Pages delivery model.
2. Use actual generated public data for acceptance evidence. Missing records,
   relationships, or states are documented as limits and never fabricated.
3. Show only repository-owned structured relationships. A title, keyword,
   proximity, or plausible scholarly connection is not an edge.
4. Keep protected production files under `src/web/browser/liturgy/`, their
   fixtures, tests, release bindings, and accepted four-action shell unchanged
   until their owning Liturgy work explicitly releases or carves out a seam.
5. Do not introduce a webfont, icon library, framework, server dependency,
   root-relative project link, unapproved asset type, global Search, or
   unmeasured payload expansion as part of the corpus foundation.
6. Parallel work uses separate full checkouts and branches. It does not use
   worktrees or a shared index.
7. Design, implementation, acceptance, integration, push, cutover, and
   deployment are distinct states and authorities.

## Source identity and evidence topology

The reusable source library's exact model is not a linear
Work-to-Passage hierarchy:

```text
Work
  owns Edition

Edition
  owns Artifact
  owns Segment
  owns Passage

Passage
  is controlled by Artifact directly
  or by Segment, which identifies its controlling Artifact
```

Artifact, Segment, and Passage are edition-owned sibling records. A Segment
may point to a container Artifact truthfully owned under another Work. That
evidence edge neither transfers nor duplicates the container bytes. Interface
copy and diagrams must keep structural ownership distinct from the Passage's
controller relation.

Provider-qualified ChatGPT and Claude publications are not Source Editions.
Use **Independent treatment** when distinguishing them for readers and
**Parallel treatment** only for a recorded relationship between two treatments.
Provider remains explicit metadata.

## Accepted product foundation

Triptych uses three related surface archetypes:

- **Reader** for sustained text;
- **Catalogue** for discovery and selection; and
- **Instrument** for data-dense research.

They share identity language, semantic token roles, accessibility behavior,
URL discipline, and contextual-navigation grammar. They do not share one
universal composition.

The durable top-level corpus destinations are Publications, Sources,
Scripture, Liturgy, History, Law, and Commentary. The Triptych wordmark is a
Home affordance. `Publications` is the public label for `/texts/`; it remains a
discovery view rather than a second owning catalogue or canonical PDF home.

The seven editorial portals remain Faith, Scripture, Liturgy, History,
Formation, Mary, and Law, in their existing order and muted identities. A
change to that contract requires an explicit amendment to `repository.md`.

The accepted visual direction is semantic rather than pixel-frozen: warm
paper-neutral surfaces, near-black text, restrained oxblood, strong blue
focus, serif reading, robust UI-sans fallbacks, quiet rules, square controls,
and content dominance. Exact type size, spacing, density, and breakpoint
geometry remain real-data decisions.

## Binding coordinator decisions D1-D20

1. `/texts/` is labelled **Publications** and remains a discovery view, not a
   second ownership hierarchy.
2. Canonical Day and Propers retain their accepted exclusive Liturgy adapter;
   no corpus masthead, fifth action, second modal owner, Search, or print
   redesign enters those routes.
3. Provider publications use Independent/Parallel treatment terminology and
   remain distinct from Source Editions.
4. Reader, Catalogue, and Instrument share roles and behavior, not one layout.
5. Token roles are accepted; synthetic prototype pixels and an assumed Inter
   installation are not.
6. Global information architecture has seven durable destinations; visible
   desktop count and geometry are decided by calm real-data evidence.
7. Home combines task entrances with the seven preserved editorial portals.
8. Publications facets never create a second owning catalogue.
9. `web-editions.md` controls the publication Reader; presentation never forks
   or silently edits publication prose.
10. Durable facts live in tracked guidance and operational ledgers, not only
    chat, ignored continuity, screenshots, or handoff ZIPs.
11. The comparable evidence matrix is 1440x900, 1024x768, 768x1024, 393x852,
    and 320x852, plus 200% text, exact 320-CSS-pixel reflow, meaningful 400%
    zoom/reflow, keyboard, forced colors, reduced motion, applicable browser
    print, no-JavaScript truth, and console/network/HTTP/accessibility checks.
12. Static-host, asset, payload, subpath, and no-framework constraints remain
    binding.
13. **Jump** is bounded navigation, not Search. Search remains J0 to J1 to J2:
    typed design, measured public-only index, then selected implementation.
14. Contextual navigation exposes only proven structured relationships.
15. Progressive disclosure may defer hashes and extended apparatus; it may not
    defer a required licence acknowledgement, withholding reason, typed
    absence, or the difference between availability and redistribution rights.
16. Local reading progress remains deferred; Day's no-memory behavior is
    intentional.
17. Generator and browser debt is repaired incrementally with path-specific
    proof, not through a foundation rewrite.
18. Concurrent Liturgy work remains separate; re-read its resulting mainline
    state before requesting access to a former protected seam.
19. Coherent named feature-branch commits and pushes are allowed; main
    integration, deployment, force-push, and history rewriting are not.
20. Parallel lanes use separate full checkouts and branches, never worktrees or
    a shared index.

## Wave 1 independent review disposition

| Unit | Disposition | Production status |
| --- | --- | --- |
| C0 Home / corpus entry | **Accepted** | Accepted design contract |
| C1 Publications | **Accepted** | Accepted design contract |
| D0 Publication Reader | **Accepted** | Accepted design contract |
| E0 Catena Omnia | **Accepted** | Accepted design contract |
| F0 Source Library | **Accepted** | Design contract accepted; production implementation remains separately owned |
| Shared non-Liturgy shell | **Accepted** | Design contract accepted; final production cutover remains blocked |
| Accessibility and resilience | **Accepted as a requirement** | Production proof outstanding |
| Browser print | **Accepted only as a non-canonical fallback** | Canonical PDF remains authoritative |

The four accepted surface compositions are closed to redesign in the review-fix
checkpoint. A shell correction may appear on their evidence routes, but it may
not reopen their typography, hierarchy, interaction model, or epistemic states.

Independent review of packaged correction head
`ecbd93a0575c4b890cc814af7cd20d01f5af7beb` recorded **F0 Source Library —
ACCEPT** and **Shared non-Liturgy shell — ACCEPT**. These are design-contract
dispositions only. They do not accept the disposable overlay as production
logic or authorize implementation, integration, deployment, public cutover,
protected Liturgy changes, or canonical PDF changes.

### C0 Home contract

Preserve the task-first corpus entrance and all seven editorial portals. Do not
turn it into a dashboard, card wall, or giant hero. At 200% text, preserve
semantic order and reflow; do not force all tasks above the fold.

### C1 Publications contract

Preserve the list-first catalogue, visible object counts, compact filter
disclosure, provider/treatment distinctions, zero state, and technical record
disclosure. Read and PDF actions remain discoverable. Redundant rule and result
spacing are optional production polish, not authority to redesign the page.

### D0 Publication Reader contract

Preserve the dominant reading plane, measure, provider qualification,
canonical-PDF action, revision/rights access, and on-demand Contents. Production
must make provider and PDF truth available without optional enhancement
JavaScript, preserve heading fragments and history, implement dialog focus
semantics, and make wide tables labelled keyboard-scroll regions. Browser print
does not replace the installed PDF.

### E0 Catena contract

Preserve Scripture as the anchor and commentary as the chronological and typed
chain. Keep held commentary, acquisition leads, translation absence, numbering
refusal, uncertain paragraph boundaries, and error states distinct. Narrow
screens use one reading order. E0 production may proceed independently only on
a branch that does not edit global shell owners or protected Liturgy.

### F0 correction contract

Keep the accepted Work/Edition identity, readable/withheld distinction,
inspection-summary label, rights truth, and Artifact disclosure. Correct only:

1. copy or hierarchy cues that imply Work -> Edition -> Artifact -> Passage;
2. one-passage navigation so the selector and exact `Passage 1 of 1` remain
   while impossible Previous and Next actions are omitted; and
3. optional Source-only redundant rule/spacing polish when already touching
   the affected selector.

The corrected F0 design contract is **accepted**. F1 implementation remains a
separately owned production lane and is not implemented or authorized by that
design disposition alone.

### Shared shell correction contract

At wide widths, show one current-location signal through stable navigation and
do not repeat the current domain beside the wordmark. Use one meaningful,
bounded **Browse** control rather than a generic Menu beside visible desktop
navigation. Do not create an eight-link bar.

At compact widths, retain the domain label, **Menu**, and bounded **Jump**.
Browse and Menu are responsive labels for one invoker and one seven-destination
dialog, not separate controls. The current destination is marked with
`aria-current`; Escape and dismissal restore focus and scroll. Jump remains a
bounded fixture and never claims global Search.

The corrected shell design contract is **accepted**. Final production cutover
remains blocked on clean foundation plumbing and explicit cutover authority.
Protected Liturgy never receives it.

## Accessibility, resilience, URLs, and print

Production must prove, rather than merely promise:

- exactly one `main` landmark on each generated page;
- no document-level overflow at 320 CSS pixels;
- named controls, visible and unobscured focus, practical targets, modal
  containment, Escape close, and focus return;
- forced-colors legibility and reduced-motion behavior;
- durable public routes and route-owned hash/history behavior;
- relative links that work beneath `/triptych/`;
- useful identity, content, browse entry, legal/source truth, and canonical PDF
  access without enhancement JavaScript; and
- clean browser print that hides interactive chrome and points to the canonical
  PDF rather than imitating it.

The inherited nested-`main`, narrow overflow, router history, selector
collision, and missing-focus defects recorded in the implementation guidance
remain production debt. An injected prototype may prove that it did not worsen
them; it cannot close them.

## Implementation sequence and ownership

| Work | State | Stopping line |
| --- | --- | --- |
| B0/B1 shared foundation and neutral browser gates | Authorized implementation work | One global owner; ingest the shell correction only after independent acceptance; do not enter protected Liturgy or invent surface composition. |
| C2 Home/Publications implementation | Eligible after clean shared-shell ownership | Implement the accepted C0/C1 contracts; do not duplicate global owners across branches. |
| D1 Reader implementation | Eligible after clean shared-shell ownership | Rendering and presentation only; preserve web-edition source ownership and canonical PDFs. |
| E1 Catena implementation | **Changes required** at pass-2 head `17f031b37840d8320c664a128d72b502108fe075` (fresh independent review 2026-08-12) | The bounded pass-2 correction preserves E0 and corrects the reviewed URL, history, asynchronous-state, truth-state, lead, print, focus, and accessibility-implementation defects, but malformed provenance values still reach visible text through JavaScript coercion and the exact-head handoff contains contradictory URL-preservation prose plus a false AT-SPI-launcher absence claim. The generator/data, release, common-gate, B0/shared-shell, real-AT/system-forced-colors evidence, protected Liturgy, and PDF prerequisites remain separately owned. E1 stays off main; only a smallest bounded Catena route/test and handoff correction may follow. |
| F1 Sources implementation | Eligible only for separate owner-authorized dispatch | The F0 design-review dependency is satisfied; no production implementation is started or authorized by the disposition. |
| Final shared-shell cutover | **Blocked** | The shell design-review dependency is satisfied; cutover still requires clean foundation plumbing and explicit authority. |
| G0/G1 History; H0/H1 Law; I0/I1 Scripture | Planned | Follow their owning guidance and accepted foundation. |
| J0/J1/J2 Search | Planned | Typed product design, measured public-only index, selected implementation. |
| K0/K1 relationships | Planned | Requires verified schema/generator edges and accepted owning surfaces. |
| L0/L1 whole-site visual/accessibility acceptance | Planned | Requires implemented surfaces and complete evidence. |
| M0/M1 integration, cutover, final review | Planned | Requires accepted lanes and explicit maintainer authority. |

Global generator, layout, site CSS, release binding, and shell files have one
implementation owner at a time. Surface branches do not independently edit
them. Implementation findings do not authorize broad refactoring.

## Correction evidence and handoff

The review-fix checkpoint must run the focused static and real-Chromium matrix
over the generated preview and recapture at least:

- wide default shell on Home, Publications, Reader, Catena, and Sources;
- 393px and 320px shell states on Home and at least one Instrument;
- corrected Sources at wide and narrow widths;
- the one-passage Source state in normal and forced colors; and
- visible keyboard focus on the changed wide Browse control.

Evidence uses existing real routes, data, rights states, and hash contracts. It
must prove protected Liturgy production assets, installed PDFs, publication
prose, production browser sources, release bindings, and public deployment
state are unchanged.

The fresh handoff follows `external-review-handoffs.md`: unique timestamped
directory and sibling one-root ZIP, core files, focused patch, numeric check
results, screenshots and index/contact sheet, sources used, manifest, exact
base/head/branch, limitations, and specific blocker questions. The package is
ignored review output and is not acceptance by itself.

## Recorded foundation and execution history

These facts explain ancestry and review provenance; they are not active
dispatch instructions:

- foundation base: `origin/main` at
  `c27d6915319785686d1df6a1401a489aa9921f6f`;
- reviewed Codex foundation head:
  `3b5938a0dba88831763ec09c762ae1572007a27e`;
- foundation prototype source:
  `ac37b6ffa6022dbab551385d91a12e277bb816cb`;
- reviewed implementation reconnaissance:
  `af2c9613ccda48679face4e43f59c002f93056ef`;
- Wave 1 was dispatched directly from the foundation base rather than through
  the proposed `corpus/foundation-integration` precursor; and
- Wave 1 Candidate was committed and pushed at `e42b928...`, then independently
  reviewed with the split disposition recorded above.

The unexecuted integration precursor is historical context only. It must not be
created retroactively or treated as a dependency.

## Completion and change control

World-class completion requires truthful object identity and availability,
purpose-built surfaces, typed auditable relationships, useful public discovery,
obvious canonical PDFs, compatible routes, deterministic generation, and
independent product, source, rights, accessibility, performance, and release
acceptance. Shared colors or a green prototype matrix are not completion.

Amend this plan only for a deliberate program-level boundary, independently
reviewed disposition, work-sequencing change, or authority grant. Put visual
rules in the vision, measured technical facts in the implementation guidance,
and dated execution evidence in the roadmap. Do not append a new contradictory
master plan beneath this one; rewrite the controlling statement in place and
preserve history only where it explains current constraints.
