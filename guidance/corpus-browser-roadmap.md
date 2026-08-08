# Triptych corpus browser roadmap

## Status and authority

This is the detailed program ledger for the non-PDF corpus experience governed
by [`corpus-browser-vision.md`](corpus-browser-vision.md). `PROJECT-WORK.md` and
`promised-deliverables.toml` remain the fail-closed operational authorities for
what is promised and complete. This roadmap supplies the work-unit detail they
link to; it grants no implementation, integration, publication, or acceptance
authority by itself.

The more specific [`liturgy-browser-vision.md`](liturgy-browser-vision.md)
continues to govern liturgical semantics and reader behavior. A production
conflict returns to the owning vision/profile and independent review rather
than being silently resolved here.

The A0-A4 foundation began from exact `origin/main` commit
`c27d6915319785686d1df6a1401a489aa9921f6f` in a separate full clone on branch
`ux/foundation`. It owns design records and an isolated review prototype only.
Production application logic, canonical PDFs, public cutover, and integration
into `main` are outside this task.

## State and disposition vocabulary

- **Planned**: sequenced but not authorized or started.
- **In progress**: authorized work has begun but has not produced a review
  candidate.
- **Candidate**: locally complete evidence awaits independent disposition.
- **Accepted** or **rejected**: an independent reviewer recorded the decision
  and any conditions in the promise ledger and this roadmap.
- **Complete**: every promised requirement and required independent disposition
  has passed; a local gate alone cannot create this state.

`Blocked` always names an external dependency or decision. It is not a synonym
for pending, difficult, or merely unstarted work.

## A0-A4 foundation record

| ID | Deliverable | Owner | State | Base / branch | Depends on | Local gate and evidence | Disposition / follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | Repository and public-site inventory | Codex | Candidate | `c27d691` / `ux/foundation` | None | Exact generated artifact census, route/surface/state/ownership matrix, current visual debt, live parity, and protected liturgy boundary in [`corpus-browser-inventory.md`](corpus-browser-inventory.md) plus handoff captures | Independent review pending; feed every downstream route owner |
| A1 | Scholarly corpus UX research | Codex | Candidate | `c27d691` / `ux/foundation` | None | Dated primary/official sources, fact/inference boundary, borrow/reject/exceed synthesis, search/IIIF disposition, and limitations in [`corpus-browser-research.md`](corpus-browser-research.md) | Independent review pending; refresh mutable observations when implementation begins |
| A2 | Site-wide product vision | Codex | Candidate | `c27d691` / `ux/foundation` | A0, A1 | Complete information architecture, object model, shell, visual language, URL/static/PDF/accessibility contracts, rejected approaches, blockers, and completion definition in [`corpus-browser-vision.md`](corpus-browser-vision.md) | Four blocking reviewer questions remain; no production authority |
| A3 | Tokens and Reader/Catalogue/Instrument archetypes | Codex | Candidate | `c27d691` / `ux/foundation` | A2 | Isolated synthetic prototype, local-only assets, static contract, real-Chromium desktop/mobile/320/200%/forced-color/reduced-motion/print evidence | Independent visual/product/accessibility review pending |
| A4 | Shared navigation, Jump, Related, and shell interaction | Codex | Candidate | `c27d691` / `ux/foundation` | A2 | One-shell prototype; visible desktop nav; narrow Menu; synthetic Jump and zero state; invoker-keyed typed Related; focus restoration; bounded review queries; no URL/data mutation | Independent interaction/IA review pending; Search remains J0-J2 |

### Foundation acceptance gates

- The corpus remains the product; pages remain typed views of corpus objects.
- Reader, Catalogue, and Instrument share tokens and a quiet shell while
  retaining purpose-built compositions.
- The accepted Liturgical Instrument remains protected: no literal global
  masthead, fifth action, second modal owner, or production asset mutation.
- Relationships are structured and typed or visibly synthetic; no unavailable
  production search/data capability is claimed.
- Existing public paths and route state are unchanged.
- The prototype is isolated, fully noindex, local-only, excluded from the
  public artifact, and makes no corpus, theological, historical, liturgical, or
  canonical claim.
- 320 CSS pixels, 200% text, forced colors, reduced motion, keyboard/focus,
  target size, console/network health, and browser print have reproducible
  evidence.
- Canonical PDFs are named but not mutated or imitated.
- Durable records and prototype sources are committed before the immutable
  external-review package is assembled.
- A0-A4 remain candidates until a reviewer answers every blocking question and
  a tracked disposition accepts or rejects them.

## Full program register

Later rows preserve the master plan rather than authorize work. Their base and
branch are **unset** until a task starts from an explicitly accepted commit.
Each later owner must replace “unset” with exact values, run the owning
guidance, and bind one standard evidence handoff.

| ID | Owner / lane | State | Base / branch | Dependencies | Acceptance gate and evidence handoff | Disposition / follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| B0 | Claude / Foundation | Planned | unset / unset | accepted A3, A4 | Production shared shell primitives; route adapter and no-JS truth; tests, accessibility checks, screenshots | Await A3/A4 acceptance; preserve liturgy adapter |
| B1 | Claude / Foundation | Planned | unset / unset | accepted A3 | Site-wide viewport, zoom, forced-color, keyboard, console, and capture harness with reproducible logs | Reuse A3 harness principles, not prototype code ownership |
| C0 | Codex / Catalogue | Planned | unset / unset | accepted A2, A3 | Home corpus-map and two section prototypes; honest generated counts; before/after matrix | Resolve Publications/Home vocabulary first |
| C1 | Codex / Catalogue | Planned | unset / unset | accepted A2, A3 | Publications/Every Document faceting and provider-treatment design; filter/mobile/empty-state captures | Preserve existing routes and independent treatments |
| C2 | Claude / Catalogue | Planned | unset / unset | accepted C0, C1, B0 | Production Home/section/Publications implementation with deterministic data and focused browser evidence | No implementation before design disposition |
| D0 | Codex / Reader | Planned | unset / unset | accepted A2, A3 | Long-form Reader for representative publication with contents, citation return, source context, PDF action, long-paper desktop/mobile evidence | Browser cannot replace canonical PDF |
| D1 | Claude / Reader | Planned | unset / unset | accepted D0, B0 | Reusable publication Reader renderer/styles with representative corpus, DOM, no-JS, print, and route tests | Preserve provider/title/source bindings |
| E0 | Codex / Commentary | Planned | unset / unset | accepted A2, A3 | Signature Scripture/commentary-chain UX across sparse/dense/partial/cross-chapter states and mobile | Follow Catena/reading-plan/Bible/versification guidance |
| E1 | Claude / Commentary | Planned | unset / unset | accepted E0, B0 | Production Commentary with model parity, DOM/accessibility, route, and real-data captures | No keyword-inferred edges |
| F0 | Codex / Sources | Planned | unset / unset | accepted A2, A3 | Evidence-observatory design across readable, withheld, external-only, multi-edition, rights, and partial states | Preserve Work/Edition/Artifact/Segment/Passage |
| F1 | Claude / Sources | Planned | unset / unset | accepted F0, B0 | Production Sources with data parity, ID/rights/no-leak, accessibility, route, and real-record evidence | IIIF only for a justified reviewed witness |
| G0 | Codex / History | Planned | unset / unset | accepted A2, A3 | Missal Line/prayer lineage across branch, station, gap, broken-line, and partial-fragment states | Follow act-history/time-machine semantics |
| G1 | Claude / History | Planned | unset / unset | accepted G0, B0 | Production History with semantic, fragment, route, responsive, and visual regression evidence | No raw-diff default |
| H0 | Codex / Law | Planned | unset / unset | accepted A2, A3 | Citation-first canon/history/act design across exact, changed, unchanged, public-domain, withheld, unread, and jurisdiction states | Name governing code and as-of identity |
| H1 | Claude / Law | Planned | unset / unset | accepted H0, B0 | Production Law with code-qualified deep-link, state, accessibility, and corpus-data tests | No fuzzy substitution for cited canons |
| I0 | Codex / Scripture | Planned | unset / unset | accepted A2, A3 | Story of Salvation three-depth journey and corpus pivots with desktop/mobile evidence | Follow Bible/reading-plan/versification guidance |
| I1 | Claude / Scripture | Planned | unset / unset | accepted I0, B0 | Production Scripture plan with translation, numbering, citation, route, and browser tests | No silent edition/numbering normalization |
| J0 | Codex / Search | Planned | unset / unset | accepted A2, inventory | Typed search UX, result taxonomy, exact/ambiguous/invalid/empty states, palette/sheet prototype | A4 Jump is only a precedent fixture |
| J1 | Claude / Search | Planned | unset / unset | accepted J0 | Public-only static index feasibility with bytes, requests, init, p50/p95, memory, multilingual, and no-leak benchmarks | Select no engine before results |
| J2 | Claude / Search | Planned | unset / unset | accepted J1, B0 | Production cross-corpus typed search with representative multi-domain queries and shareable static state | Fail closed on ambiguity and private data |
| K0 | Codex / Relationships | Planned | unset / unset | accepted E0-I0 | Typed contextual-relationship model and task walkthroughs across corpus domains | Edge type/direction/derivation/revision required |
| K1 | Claude / Relationships | Planned | unset / unset | accepted K0 and owning surfaces | Generated public relationship projection, link integrity, no-leak, deep-link, and route evidence | No generic recommendations |
| L0 | Codex / Acceptance | Planned | unset / unset | accepted C0-K0 | Site-wide 320/393/tablet/zoom visual-coherence review and one contact-sheet handoff | Include representative real corpus states |
| L1 | Claude + Codex judgment / Acceptance | Planned | unset / unset | implemented surfaces | WCAG 2.2 AA core-flow evidence: keyboard, zoom, forced colors, reduced motion, screen-reader and real-device notes | Automated checks are necessary, not sufficient |
| M0 | Claude / Integration | Planned | unset / unset | accepted implementation lanes | Clean integration range; full project/publication/browser gates; public-intent audit; Pages and deployed parity if separately authorized | Ordinary integration only; no history rewrite |
| M1 | Codex / Acceptance | Planned | unset / unset | accepted M0 | Final independent world-class completion disposition and immutable release handoff ZIP | Completion only after explicit tracked review |

## Foundation evidence handoff

The foundation closes locally with one unique package governed by
[`external-review-handoffs.md`](external-review-handoffs.md). It contains the
exact base, branch, reviewed head, commits, focused changes, route and state
inventories, checked research, prototype sources, before/after screenshots,
desktop/mobile/320/200%/forced-color states, contact sheet and index, commands
with numeric statuses, known limitations, blocking questions, and exact next
tasks. The ZIP has one root directory and is byte-verified after creation.

Creating or inspecting the package does not mark A0-A4 accepted. A reviewer
must return an explicit accept/reject/changes-required disposition for each
blocking question. That disposition is then recorded here,
`promised-deliverables.toml`, `PROJECT-WORK.md`, and the continuity record before
any B0/B1 production foundation starts.

## Progress ledger

| Date | Work | Evidence-backed result | Commit or handoff |
| --- | --- | --- | --- |
| 2026-08-08 | A0-A4 kickoff | Created an isolated full clone; recorded exact current remote base; transferred the governing master plan; reconciled concurrent liturgy WIP; reserved production routes/PDFs from mutation | Base `c27d6915319785686d1df6a1401a489aa9921f6f`; branch `ux/foundation` |
| 2026-08-08 | A0/A1 synthesis | Reconciled a 20,441-file generated artifact, 144 HTML routes, corpus/state counts, ownership/debt, current visual baseline, and checked scholarly/accessibility precedents | Inventory/research records in the containing commit |
| 2026-08-08 | A2 candidate | Defined the information architecture, object/provider distinction, protected liturgy adapter, exact visual language, URL/static/PDF boundaries, twelve rejected approaches, four blockers, and completion test | Vision record in the containing commit |
| 2026-08-08 | A3/A4 candidate | Built an isolated synthetic noindex prototype and static/real-Chromium gates for three archetypes, shared shell, Menu, Jump, contextual Related, 320px, 200%, forced colors, reduced motion, focus, overflow, and print | Prototype/tests in the containing commit |
| 2026-08-08 | Foundation validation | Focused static and Chromium gates pass; 31 current/prototype screenshots were inspected; fresh 20,441-file public artifact is byte-identical at its two control hashes. Aggregate `make check` remains stopped by unchanged tmt dependency declarations and stale example transcripts, recorded in continuity and the handoff. | Candidate checkpoint is the containing commit; review output `20260808T191722Z-corpus-browser-foundation` |

Append later findings and independent dispositions. Do not rewrite completed
rows to make the sequence look cleaner.
