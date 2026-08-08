# Corpus browser foundation continuity

## Tracking exception

This task-specific continuity record is intentionally tracked under
`build/agent-continuity/` as the exception authorized by the master plan and
current repository practice. Generated screenshots, logs, handoff directories,
and ZIPs remain ignored. Only this exact continuity file is force-added.

## Resume header

- Objective: execute Codex-owned A0-A4 from
  `docs/triptych-world-class-corpus-master-plan.md` and stop at independent
  acceptance.
- Base: `c27d6915319785686d1df6a1401a489aa9921f6f`
- Branch: `ux/foundation`
- Checkout form: separate full clone, not a worktree
- Reviewed head: the commit containing this file; resolve exactly with
  `git log -1 --format=%H -- build/agent-continuity/corpus-browser-foundation.md`
- Production/public state: unchanged; nothing merged, pushed, deployed, or
  installed
- External-review disposition: **open**; A0-A4 are candidates, not accepted
- Planned immutable review output:
  `build/agent-handoffs/20260808T191722Z-corpus-browser-foundation/` and sibling
  `.zip`

## Objective and bounded scope

Inventory the complete generated public surface and its source ownership;
synthesize checked scholarly-interface and accessibility research; define the
site-wide product vision, object model, visual system, and Reader/Catalogue/
Instrument archetypes; design shared navigation, bounded synthetic Jump,
typed contextual Related behavior, and shell interactions; commit all durable
memory; and assemble one verified standard handoff.

The task does not own production browser implementation, generated public data,
route migration, search indexing, canonical PDFs, accepted liturgy assets,
integration, push, deployment, or review acceptance. The isolated prototype is
synthetic, fully noindex, local-only, and excluded from public build mappings.

## Completed

- Reconciled the directions/master plan with global guidance, repository
  authority, the promise ledger, current `origin/main`, and concurrent liturgy
  Ritual Flow WIP.
- Created the separate clone and branch from the exact current remote base.
- A0: inventoried a 20,441-file artifact, 144 HTML pages, 192 PDFs, 19,957 JSON
  files, 13 browser entrances plus four noindex liturgy evidence pages, route
  state, ownership, link/navigation debt, narrow-screen debt, and public/live
  parity in `guidance/corpus-browser-inventory.md`.
- A1: checked official/primary documentation for Sefaria, Scaife/Perseus,
  Corpus Thomisticum, IIIF/Vatican, TEI/CTS, catalogues, GOV.UK/USWDS,
  ecclesial references, WCAG/APG, and static search precedents; recorded
  borrow/reject/exceed conclusions and limitations in
  `guidance/corpus-browser-research.md`.
- A2: completed `guidance/corpus-browser-vision.md`, including corpus IA,
  Work/Edition/Artifact/Segment/Passage identity, provider-treatment boundary,
  protected liturgy adapter, exact token roles, three archetypes, responsive/
  accessibility/URL/static/PDF contracts, twelve rejected approaches, four
  blockers, and world-class completion.
- A3/A4: built the isolated prototype under
  `src/web/browser/prototypes/corpus-foundation/` and dependency-free static and
  real-Chromium gates. The fixture demonstrates one non-liturgy shell, current
  domain, desktop/navigation Menu, functional bounded Jump and zero state,
  functional Catalogue filtering/zero state, invoker-keyed directed Related
  sets, explicit unsupported Catalogue context, focus return, and responsive
  archetype composition.
- Reconciled `PROJECT-WORK.md`, `promised-deliverables.toml`, and the complete
  A0-M1 roadmap. A0-A4 local requirements pass; independent disposition stays
  open and keeps the deliverable candidate.
- Captured and visually inspected 14 current-site baseline images and 17
  prototype states at original resolution, including desktop, mobile, 320px,
  200% text, 400%-reflow equivalent, keyboard focus, forced colors, reduced
  motion, menus, Jump/empty, Related, and browser print.
- Recorded one tmt note for the repeatable public-route inventory derivation.

## Not complete

- Independent review has not occurred. No agent self-review is represented as
  external, human, specialist, ecclesiastical, product, or accessibility
  acceptance.
- The reviewer must answer the four blockers in the vision and
  `REVIEW_REQUEST.md` and return accept, reject, or changes-required for A2-A4.
- B0-M1 remain planned and unauthorized. In particular, A4 Jump is not global
  production search; J0-J2 must design, benchmark, and implement that system.
- No production route, global shell, relationship projection, PDF, or public
  artifact has changed.

## Learned facts and decisions

- Home is currently the Library; `/library/` is not a public entrance. The
  candidate compact label **Publications** points to `/texts/` without changing
  that route, but this vocabulary needs reviewer disposition.
- Provider outputs are independent provider-qualified treatments, not
  bibliographic Source Editions. Grouping cannot merge their provenance.
- The accepted liturgy reader is a visual/accessibility benchmark and protected
  adapter. Current `main` also contains a separate unaccepted Ritual Flow delta;
  current captures must not be called the accepted oracle.
- Canonical Day and Propers retain exactly Date/Browse, Contents, Mode, and
  Details; they receive no literal global masthead, fifth action, second modal
  owner, or new sticky chrome under this foundation.
- Reader Contents and Instrument evidence stay in flow in the prototype so they
  do not squeeze or move their primary planes.
- Search and Related are object routers, not answer/recommendation engines.
  Exact typed IDs/citations precede lexical matches; ambiguous or unsupported
  state remains explicit; no nearest-object substitution is allowed.
- Static no-JavaScript pages own identity and core truth. GitHub Pages supplies
  no API, request-time policy, rewrite layer, or state-specific metadata.
- A digest proves byte identity only. Rights, authority, correctness,
  verification, and availability require separate human-readable fields.

## Checks and evidence

- `git diff --check`: exit 0.
- `tools/tpt check-promised-deliverables`: exit 0; 25 tracked deliverables,
  18 complete; this foundation remains candidate.
- `python3 -m unittest tools.tests.test_corpus_foundation_prototype -v`: exit 0;
  11 of 11 tests pass.
- `node tools/tests/corpus_foundation_prototype_browser.mjs`: exit 0; 11 of 11
  assertions pass; 0 console warnings/errors, failed requests, HTTP failures,
  document/body overflow findings, undersized primary controls, and unnamed
  interactive accessibility nodes.
- Browser evidence capture: exit 0; 17 screenshots plus browser-print PDF,
  measurements, and JSON report. All 17 were inspected at original resolution.
- Current-site baseline capture: exit 0; 14 screenshots. All 14 were inspected
  at original resolution.
- `tools/tpt public-alpha check`: exit 0; 186 alpha publications, 0 hold.
- `tools/tpt public-alpha build`: exit 0.
- `tools/tpt public-alpha verify --deployment-target github-pages`: exit 0;
  20,441 files. `SHA256SUMS` is
  `58ca5460a62260716b18daa0dcd8bc8501577041b6f1ad8644b372868aeb7327`;
  `PUBLICATION-MANIFEST.json` is
  `20dd5afeef2720de9838319991fbd36d3f83f38cf94cc070905b46e5e7937130`.
- `make check`: exit 2 only at unchanged `check-tool-registry`; every preceding
  metadata, web, proper, catalogue, source, inventory, promise, public-alpha,
  and release-binding target passed.
- The remaining targets were run explicitly after that stop. Calendar masses,
  rubrics, propers census, Mass Ordinary, Catena, and commentary coverage pass.
  the underlying example replay exits 1, making the `make` target and grouped
  command exit 2: 201 captured, 192 replayed, 29 diverged, 35 already labelled
  known stale, 6 intentionally never run, 3 unavailable here, and 2 volatile
  lines declared.
- `tmt check`: exit 1 with eight unchanged undeclared
  sibling dependencies. No tmt registry or tool file is changed by this task.
- The fresh public artifact hashes match the A0 baseline, proving the nested
  prototype remains outside public publication mappings.

## Blockers and open questions

Independent judgment is the only A0-A4 acceptance blocker:

1. Accept **Publications** for `/texts/`, or retain another Home/Library label?
2. Accept the exclusive liturgy adapter with no literal global masthead or
   fifth action?
3. Accept **parallel provider treatment** as the public terminology?
4. Accept, reject, or return changes for the token system, three archetypes,
   static shell, bounded Jump boundary, contextual Related contract, and
   responsive compositions?

The unchanged tmt dependency declarations and stale example transcripts are
repository-wide defects outside this task. They block a green aggregate
`make check`, not the focused prototype or public-artifact gates. Do not fix or
recapture them under A0-A4 without separate scope.

## Failed or rejected approaches

- Rejected a permanent Reader Contents sidebar and fractional Instrument rail
  after review showed they narrowed or shifted the primary plane; both are now
  in flow.
- Rejected a decorative Catalogue filter; the fixture now filters, counts, and
  exposes a truthful zero state.
- Rejected one context-free Related list; the fixture now keys directed edge
  sets by source object and has an explicit Catalogue no-fixture state.
- Rejected calling the synthetic title fixture global search; its public label
  is Jump and its boundary is visible.
- Rejected a raw `pageScaleFactor: 4` screenshot because it magnified without
  layout reflow and therefore misrepresented the WCAG state. The handoff uses
  a labelled 320px reflow equivalent from a 1280px baseline, plus separate 200%
  text evidence.
- Rejected dashboard, card-grid, faux-medieval, universal-layout, provider-
  conflation, digest-first, generic recommendation, framework migration, and
  premature IIIF directions in the vision's RA-01 through RA-12 record.

## Review disposition

Internal parallel audits and the final design red-team found no remaining
RA-01 through RA-12 contradiction. That is internal evidence only. External
disposition remains **not requested / open**, so the foundation is a candidate
and production foundation work may not begin.

## Exact next action

Open the verified sibling ZIP named in the resume header, begin with
`HANDOFF.md`, inspect the numbered contact sheet and the exact A2-A4 source
diff, answer every blocker in `REVIEW_REQUEST.md`, and record the resulting
accept/reject/changes-required disposition in the roadmap, promise ledger,
project register, and this file. If accepted, choose an exact accepted base for
B0/B1 in a new full checkout; do not merge this branch merely to preview it.

## Checkpoint history

| Checkpoint | Meaning |
| --- | --- |
| `c27d6915319785686d1df6a1401a489aa9921f6f` | Exact `origin/main` base; no foundation work |
| containing commit | A0-A4 durable candidate, isolated prototype/tests, reconciled ledgers, and continuity; no production/public mutation |

No commit in this history is merged, pushed, deployed, or externally accepted
by this task.
