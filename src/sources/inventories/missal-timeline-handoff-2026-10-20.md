# Missal timeline continuation handoff

This is the clean-agent restart point requested on 2026-10-20. The full all-rite
project remains in progress. The research checkpoint is
`1356d8eaa56341687106c52170e450f29867f9b5`, pushed to
`origin/feature/missal-timeline`; the worktree was clean when this handoff began.
The handoff itself follows in a separate commit. Earlier counts below the current
checkpoint in [PROJECT-WORK.md](../../../PROJECT-WORK.md#all-rite-missal-timeline-recovery-and-expansion-2026-10-16)
describe their dated snapshots.

## Resume and authority

The requested outcome includes historical coverage for every Catholic rite,
shared ancestry and extinct local uses; sufficiently distinct versions;
regional, religious-order and missionary permissions; organized witnesses and
complete structured texts; meaningful generated Git diffs; and interactive and
printed chronology. The user permits sub-agents. A reconciled catalogue or a
bounded reader review does not fulfill the complete project.

Read the workspace and repository `AGENTS.md`, the linked project-work section,
and the `all-rite-missal-timeline-2026-10-16` entry in
[promised-deliverables.toml](../../../promised-deliverables.toml). Then follow
[time-machine sections 11 and 12](../../../guidance/time-machine.md#11-historical-and-language-scope-agreed-2026-10-16)
and [act-histories section 20](../../../guidance/act-histories.md#20-discovery-coverage-and-bounded-text-reconstructions).
Read the source, missal, publication-rights and web-data guidance before changing
their respective owners. The 2026-10-20 request for this tracked handoff
supersedes the earlier instruction against another handoff for this checkpoint;
all substantive completion criteria remain open where their evidence is open.

Keep this workspace on `feature/missal-timeline`. Commit coherent changes with
an `AI summary:` body, explicitly naming the intended commit paths. Publish
with `git push -u origin feature/missal-timeline` after inspecting the outgoing
range and newly reachable objects. Default-branch integration, a new hosted
corpus repository and website deployment are outside this checkpoint. Disposable
research belongs only in the workspace or clone's permitted `.scratch/` location.
No prior agent handle, untracked packet or local process is needed to resume.

## Current evidence owners

Paths in this table are relative to the repository root. Prefer these owners
over counts or summaries in this handoff after subsequent edits.

| Owner | Purpose |
| --- | --- |
| `src/sources/inventories/eastern-eucharistic-books-timeline-v1.toml` | Eastern candidates, inspected sources, Church coverage, approval and reception qualifications. |
| `src/sources/inventories/western-eucharistic-books-timeline-v1.toml` | Western candidates, exact books and discovery clusters, local-use and order coverage. |
| `src/sources/inventories/eucharistic-stages/*.json` | Canonical traditions, bounded dated states, transitions, source loci and explicit gaps. |
| `src/sources/inventories/eucharistic-stage-coverage-v1.json` | All route mappings, exact input fingerprints, witness and dossier snapshots, component gaps and next sources. |
| `src/sources/inventories/eucharistic-research-reviews/regional-mission-permissions-2026-10-20.json` | Scoped permission findings, authority, territory, component extent, actual-use status and remaining work. |
| `src/sources/inventories/catholic-eucharistic-history-v1.toml` | Catalogue routing, accepted act slices, presentation groups and comparison adapters. |
| `src/sources/inventories/eucharistic-book-relationships-v1.toml` | Typed sharing, borrowing, reception and ancestry research; independent of textual inheritance. |
| `src/sources/inventories/eucharistic-books/` | Checked native constituent bindings and separately declared extents. |
| `src/sources/inventories/eucharistic-source-retention-decision-v1.toml` | Exact retained payloads and itemized deferrals; source-library manifests own distribution bases. |
| `src/web/data/structure/act-history/` | Generated browser projection; regenerate through `tools/act-history structure`. |
| `src/web/browser/history/` | Reader implementation; new data alone has not received fresh interactive acceptance. |

`tools/act-history` owns catalogue, corpus and projection generation. Its helpers
are `scripts/_eucharistic_history.py`, `scripts/_eucharistic_stages.py` and
`scripts/_eucharistic_texts.py`. `tools/missal-coverage-reconciliation` checks
the source owners against the audit. The original recovery report is
[missal-timeline-recovery-2026-10-16.md](missal-timeline-recovery-2026-10-16.md);
its early counts and access gaps are historical checkpoints.

## Measured research checkpoint

| Object | Count or disposition at `1356d8eaa` |
| --- | --- |
| Eastern inventory | 440 candidates, 373 sources, 23 Church or tradition coverage rows. |
| Western inventory | 1,161 candidates, 899 sources, 73 trajectories or discovery rows. |
| Combined catalogue | 1,660 records including 59 legacy act/witness records; these are not distinct-version counts. |
| Stage dossiers | 29 dossiers and 142 declared traditions. |
| Stages | 272: 261 documented and 11 provisional. |
| Transitions | 76; no new transition was inferred from the latest bibliographic expansion. |
| Declared stage gaps | 177. |
| Text coverage | 256 stages not transcribed, 16 partial, zero complete whole-book stages. |
| Route status | 85 selected-stage routes, nine related-dossier or local-reception gaps, two without a new researched sequence. |
| Routes without any mapped stage | Nine; Greek and Italo-Albanian have related source-book stages but unverified local reception. |
| Permission register | 49 findings across 32 route IDs; a bounded sample, not an exhaustive permission census. |
| Generated history projection | 539 files across three slices, 118 act stations and 23 lines; these count different objects from the stage layer. |

## Completed research and important corrections

Four pushed checkpoints preserve the latest work:

| Commit | Result |
| --- | --- |
| `69da32e366612e7accd8fa35a02bba9413bc8894` | Initial regional book states and scoped permission register. |
| `82a9a276c32b8128d42f9ccdacb48e152f070428` | Bursfelde, Évora, German regional, northern/central regional and Blaj states. |
| `36a8085089c8087af919274d8dd4aa0f5a5db286` | Registered the read-only reconciliation tool in the launcher and added its smoke test. |
| `1356d8eaa56341687106c52170e450f29867f9b5` | Nine further dossiers, exact candidate repairs, expanded permission register, reconciled audit and generated projection. |

The nine new dossiers are `central-europe-round3.json`,
`early-western-round2.json`, `eastern-local-round2.json`,
`french-local-round2.json`, `italian-local-round2.json`,
`northwest-round2.json`, `other-orders-round2.json`,
`residual-orders-round3.json` and `residual-western-round3.json`. They added
102 bounded stages to the preceding 170-stage checkpoint.

Keep these decisions with their source-qualified records:

- Exact Mainz, Augsburg, Bamberg, Bremen, Eichstätt, Utrecht and Riga books now
  have candidate IDs distinct from discovery clusters. Four Cluny printings
  also have exact candidates. Do not link a dated single-book stage back to an
  aggregate cluster merely because its family label matches.
- The Hospitaller stage uses `additional-orders-hospitaller-bnf-b320-1553`.
  BnF corrects B-320 to 1553; unresolved Lyon copies remain separate leads.
  A distinct 1551 edition has not been established.
- The Roman Greek Hieratikon bears 1950 on its title but finishes printing in
  March 1952. Its stage uses the 1952 publication coordinate. Évora preserves
  its 1509 colophon versus probable 1519 printing distinction. The OSA
  1491/1496 conflict remains unpositioned. Riga's disputed dating also remains
  unpositioned.
- Verona cod. LXXXV(80) uses the catalogue copying range 551–600. That date
  does not date the underlying libelli or establish public liturgical use.
- `byz-ugcc-2024` is now an active Ukrainian candidate. The promulgation and
  official April implementation interview support the Church's operative
  received language. They do not identify a first celebration, prove uniform
  compliance or establish an inspected complete printed volume.
- The OCD 2025 proper's signed Latin decree gives 30 November 2025, subject
  to publication; the order's news item gives 20 November. The discrepancy is
  retained. Local calendar grades concern named houses, and the book remains
  a proper rather than a complete independent Roman Missal.

The permission register also covers Zaire, Indian ritual concessions, personal
ordinariates, Chiapas adaptations, the Broome recognitio gap, mission-language
faculties, Keren Blin/Ge'ez, regional Byzantine books, diocesan and order propers,
Dogon/Ibanag/Welsh component translations, Jerusalem, PIME, Minims and others.
Each finding's own approval, pending, extent and actual-use fields control.

## Outstanding work and concrete next inputs

The audit's `missing_stage_chain`, `next_sources`, `gap_ids` and each dossier's
`gaps` are the detailed work queue. The table below prioritizes remaining
source-book and local-reception questions; it does not replace the 177 gaps.

| Route or work | Next evidence |
| --- | --- |
| `albanian` | Elbasan Catholic community book inventory, exact title/approbation leaves and dated use. Orthodox Albanian and Italo-Albanian books cannot be transferred to this row by language. |
| `macedonian` | Exact celebrant title/imprint, Greek or Slavonic exemplar and dated use. The official 9 December 2009 approval identifies translated Chrysostom/Basil liturgies without supplying these book facts. |
| `hungarian` | Fuller 1646 copy or title/colophon images, dated Nyírderzs ownership/use and later sequence. Habina's 1775 estate inventory supports ownership of the 1692/1695 book, not altar use. |
| `greek`, `italo-albanian` | Separate Roman Greek publication from reception at Grottaferrata, Lungro, Piana and the Greek exarchate; locate local calendar/rubric and adoption evidence. |
| `ocso` | Exact Latin Mass proper, lectionary and approving decrees, including the reported 1983 prayers; establish branch and house reception without assigning a medieval OCSO identity. |
| `italian-padua` | E 57 Eucharistic rubrics and local Mass-book holdings; distinguish Padua from the Passau label Pataviense. |
| `italian-monza` | Liber ordinarius Modoetiensis and exact Monza/Berengar sacramentary contents; separate Roman, Ambrosian and local material. |
| `italian-ravenna` | Fragment identities, layers and provenance; an Advent prayer group does not establish a complete annual Mass book. |
| `italian-other-uses` | Composite index; qualified child routes own the individual books. Do not manufacture another sequence for the index. |
| `roman-historical-vernacular-witness-controls` | Buzuku identity, surviving contents, losses, authorization and reception remain explicit controls under the deferred independent-translation scope. |
| Historical sequence and text | Acquire and collate exact originals and named component gaps, including Rome 1634. Build complete structured books in native divisions; verify boundaries and literal text before inheritance or reconstruction. |
| Regional and missionary variants | Expand the permission census by rite, jurisdiction and period. Obtain original instruments, exact approved books and dated implementation where only summaries or permission are known. |
| Reader acceptance | Freshly test the expanded catalogue and chronology, accessibility and print evidence. Earlier bounded reviews do not establish acceptance of changed catalogue bytes or exhaustive historical coverage. |

Continue useful work across independent lanes when one original is unavailable.
Assign exclusive dossier and inventory lanes, integrate centrally, and preserve
each reviewer finding until it has an evidence-backed disposition. Received
modern-language service books require evidenced Church approval and use under
the owning scope; translation origin alone neither admits nor excludes them.

## Validation and efficient continuation

The research checkpoint passed:

- `tools/missal-coverage-reconciliation --json`: `ok`, zero findings.
- `tools/source-library validate`: 3,190 artifacts, 1,160 editions, 990 works,
  5,457 passages, 110 segments and 3,955 bindings.
- `tools/act-history structure --check`: all 539 tracked files current.
- `PYTHONPATH=tools/tests python -m unittest tools.tests.test_eucharistic_stages tools.tests.test_eucharistic_history -q`: 84 tests passed.
- `sh tests/tools/missal-coverage-reconciliation.test`, `tools/tpt --check`
  and `git diff --check` passed.

The wider tool-registry run was not green. Reported issues included stale
act-history example/fixture expectations, a chronology-annotation preflight
discrepancy and a Markdown dependency-lock mismatch. The missing reconciliation
smoke test was fixed in `36a808508`. No completed final whole-registry rerun
establishes a current failure set. Later broad structure/registry runs were
stopped while repeating expensive projection and unrelated smoke checks; do not
report those interrupted runs as passing or treat their partial output as a
new baseline. Use focused gates for the next actual change, and compare base
and changed results if investigating those wider failures.

For research changes, keep inventory candidate membership and source IDs,
exact stage witnesses, audit input hashes and snapshots, and generated browser
data coherent. Run reconciliation after the owning files stabilize; never
refresh fingerprints to conceal an unexplained mismatch. Regenerate with
`tools/act-history structure`, then run its read-only `--check`. Derived
comparison files may change solely because their pinned input fingerprints
change. Run the focused tests and rights/source checks required by the files
actually changed. The registry is in `tmt.json`.

This handoff adds no source payload, historical transition, complete text,
browser behavior or deployment. Its persistence checks are local-link review,
ledger validation and diff review. Re-check Git state before resuming: later
commits take precedence over this checkpoint's counts.
