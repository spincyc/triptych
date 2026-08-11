# Repository Instructions

## Project

This repository contains **Triptych: AI Driven Studies in Catholic Faith, Worship, and Law** (`triptych`), a source-first collection of liturgical, theological, and canonical study documents.

`guidance/the-shape.md` states the few ideas the rest of this guidance keeps
applying, and the incidents that produced them. It governs nothing on its own and
is the shortest way to understand why the rules below are shaped as they are.

Read these files before changing document content, structure, or build behavior:

1. `README.md` for the landing page, which is also the catalog index, `ABOUT.md` for the consumer overview, and the section pages under `library/` for publication listings and supporting records.
2. `CONTRIBUTING.md` for the public contribution paths and ordinary-language agent workflow.
3. `LICENSE` and `THIRD_PARTY.md` for the applicable license boundary and excluded source material.
4. `guidance/editorial.md` for the universal evidence, attribution, metadata, review, and publication standard.
5. `guidance/repository.md` for source ownership, target paths, mirrored publications, and build rules.
6. The one or more profiles that govern the requested document.

Read `guidance/sources.md` before adding, migrating, storing, or reusing a
repository-wide external source, corpus, edition, artifact, passage record, or
publication binding.

The documents above govern publications. A second family governs the tracked
data and the apparatus over it, and nothing else routes to them — read the one
that owns what you are about to touch, **before** touching it, because each is
largely a register of how that data has already gone wrong:

| Before you touch | Read |
| --- | --- |
| a task requiring external visual, product, source, architectural, or acceptance review | `guidance/external-review-handoffs.md` |
| a mass, proper, or rubric in `src/sources/calendars/` | `guidance/propers-for-agents.md` |
| anything the browser fetches from `src/web/data/` | `guidance/web-data.md` |
| the site layout template, `assets/site.css`, `src/web/browser/shared/`, site navigation, route generation in `tools/public-alpha`, or any non-PDF web surface outside liturgy | `guidance/corpus-browser-implementation.md`, `guidance/corpus-browser-master-plan.md` |
| non-liturgy corpus browser work: Home or Publications routes; the web publication Reader; Catena or Sources routes; or shared non-liturgy shell, navigation, search, context, responsive, or print presentation | `guidance/corpus-browser-master-plan.md`, `guidance/corpus-browser-vision.md`, `guidance/corpus-browser-roadmap.md`, `guidance/corpus-browser-implementation.md`, plus the existing universal, profile, and owning-surface guidance as applicable — including `guidance/web-editions.md` for the Reader, the Catena guidance below, `guidance/sources.md` for Sources, and `guidance/web-data.md` for fetched data |
| liturgy browser HTML, CSS, or JavaScript; Day or Propers routes; shared liturgical rendering; modes or navigation; responsive or print presentation; calendar or source apparatus; comparison views; or browser-visible recension coverage | `guidance/liturgy-browser-vision.md`, `guidance/liturgy-browser-roadmap.md` |
| a bible edition, its index, or its chapter fragments | `guidance/bibles-for-agents.md` |
| a verse or chapter numbering question across editions | `guidance/versification.md` |
| commentary fragments, the harvest, or the catena page | `guidance/catena.md`, `guidance/reading-plan-for-agents.md` |
| a liturgical act history or its stations and lines | `guidance/act-histories.md`, `guidance/time-machine.md` |
| a missal witness, its rights, or its acquisition state | `guidance/missals.md` |
| a calendar recension and its departures from a base | `guidance/recensions.md` |
| whether a publication's research has gone stale | `guidance/staleness.md` |
| a promised deliverable and whether it is met | `guidance/promised-deliverables.md` |

The non-liturgy corpus browser route does not govern the Liturgy browser or
relax its dedicated routing and protections.

The remaining production plans and handoffs are maintainer records, linked from
the profile or registry that owns their subject rather than from here.

The user's request takes priority when it deliberately changes a project convention. Record the new convention in the correct universal or profile guidance rather than leaving the implementation and guidance inconsistent.

## Profile routing

Select profiles by the document's actual genre and sources, not by superficial similarity:

- 1962 Roman Rite temporal, ritual, votive, or other proper guides: `guidance/liturgy/roman-1962-propers.md`
- edition-specific references for assembling the Ordinary and propers under the 1962 calendar and rubrics: `guidance/liturgy/roman-1962-assembly.md`
- 1962 Roman Rite altar-server response, pronunciation, memorization, and ceremonial training guides for Low Mass, Missa Cantata, and Solemn Mass: `guidance/liturgy/roman-1962-server-training.md`
- comprehensive and use-derived pictorial dictionaries of Roman sanctuary composition, objects, linens, vessels, books, vestments, insignia, and related ceremonies at the 1962 horizon: `guidance/liturgy/roman-1962-pictorial-dictionaries.md`
- self-paced Ecclesiastical Latin curricula centered on the 1962 Missal, including modular teaching packets, reference, practice, assessments, and keys: `guidance/curriculums/ecclesiastical-latin.md`
- edition-specific histories and complete normative inventories of Roman calendars: `guidance/liturgy/roman-calendar-references.md`, plus the profile for the identified edition where its rules are used
- recurring Roman calendar arithmetic used by any liturgical document — movable anchors, the Sunday `A`/`B`/`C` and weekday `I`/`II` Lectionary cycles, postconciliar Ordinary Time week numbering, and the 1962 resumed-Sunday mechanism: `guidance/liturgy/calendar-computation.md`
- postconciliar Roman Rite proper guides: `guidance/liturgy/postconciliar-propers.md`, with permanent IDs, keys, slugs, counts, and occurrence grammar in `guidance/liturgy/postconciliar-propers-registry.md` and edition dispositions under the selected `<edition-locale>/propers/registry/`
- expositions of the Ordinary or Order of Mass in either form: `guidance/liturgy/ordinary-expositions.md`
- the sacramental treatise, at-a-glance companion, or their shared fragments: `guidance/theology/sacramental-reference.md`
- the comprehensive reference on theological, cardinal, intellectual, and annexed virtues: `guidance/theology/virtues.md`
- the Rosary, Marian-apparition judgment studies, or other repeatable Mariological reference works: `guidance/theology/mariology.md`
- historical and hagiographic lives in the biographies collection: `guidance/biographies.md`
- comprehensive historical reference works on heresies, censured propositions, and ecclesial responses: `guidance/theology/heresies.md`
- novenas and other works in the numbered novena collection: `guidance/devotions/novenas.md`
- repeatable source-first histories of texts, institutions, events, or reception: `guidance/history/historical-accounts.md`
- discursive articles on faith, theology, canon law, or Scripture: `guidance/articles.md`

A document may require more than one profile only when it truly combines genres. For example, a canonical article about a liturgical question follows the articles profile for its argument and the relevant liturgical profile for edition-specific textual claims. State which profile governs each part rather than merging their templates.

The sacramental treatise and its at-a-glance companion are established theological reference works with shared canonical fragments. Follow the universal guidance, their sacramental-reference profile, and their local research scope; do not impose a Mass-propers or discursive-article template on them.

If no profile fits a requested repeatable series, add or revise a profile before multiplying documents. Keep universal guidance genre-neutral. Put rite-, edition-, locale-, calendar-, jurisdiction-, page-, and section-specific rules in the appropriate profile, not in this file or the universal editorial standard.

## Codex sessions

A Codex session may work directly in the current checkout, including the primary
checkout, within the authority granted for its task. Inspect and preserve
unrelated changes before mutation.

Direct sessions have standing authority to create ordinary coherent commits for authorized work and to push validated checkpoints regularly to `origin/main`. Before each push, verify the exact outgoing range, confirm that every newly reachable object is intended for public disclosure, and run the checks required by the affected guidance. A push to `origin/main` triggers the GitHub Pages workflow and therefore authorizes that automatic deployment attempt. This standing authority does not permit force-pushing, rewriting published history, integrating retained workers, changing remotes, or triggering any other deployment.

## Claude sessions

A Claude session works in its own full checkout on its own branch, never in a
checkout another agent holds, and commits there as ordinary implementation.

On 2026-08-08 the maintainer granted one narrower standing authority: **a bug
fix found against `main` may be merged to `main` and pushed, provided the merge
is a clean rebase and a genuine fast-forward.** It is bounded in four ways, and
the bounds are the reason it was granted.

- **Bug fixes only.** Feature branches, redesign lanes, and anything awaiting
  independent review still go to a feature branch and stop there.
- **Fast-forward only.** If a rebase is not clean, or `main` is no longer an
  ancestor, stop and report. Never force, never rewrite published history.
- **The deploy gates run first, locally.** `make check-deployment-sources`,
  `make public-site`, and `public-alpha verify --deployment-target github-pages`
  are exactly what the Pages workflow runs; run all three and the fix's own
  tests before pushing.
- **The push is the deployment.** A push to `origin/main` triggers the Pages
  workflow, so pushing authorizes that publication. Verify the run afterwards
  rather than assuming it.

Inherited failures are not a reason to stop: `make check` is red at the base for
reasons no bug fix causes. Compare failure sets, not exit codes, and say which
set you compared against.

## Work sequence

Before editing:

1. Inspect the worktree and preserve unrelated user changes.
2. Identify the document's provider, collection, genre, rite, edition, language or locale, jurisdiction, and as-of date where applicable.
3. Read the applicable profile completely and inspect the document's source and research records.
4. Confirm whether the request authorizes content changes, structural moves, installed PDF changes, commits, integration, updating local `main`, pushing a named ref, deployment, or history rewriting; do not infer broader authority from a narrower request.

During research and drafting:

- verify claims from primary, official, edition-identified sources wherever available;
- treat OCR, searchable transcriptions, aggregations, and secondary citations as leads until checked as the profile requires;
- keep verified source text, checked quotation or paraphrase, source-grounded synthesis, original editorial or AI proposal, and unverified leads distinct;
- preserve material disagreement, uncertainty, jurisdiction, and currentness rather than silently harmonizing sources;
- update the repository-owned source and research records required by the profile;
- cite only sources actually used and do not invent a search, verification event, quotation, attribution, doctrine, law, or historical fact;
- keep third-party quotations focused, record their known rights status, and comply with copyright and redistribution limits;
- never put credentials, tokens, hostnames, usernames, machine-specific paths, network addresses, hardware identifiers, or session identifiers into tracked sources or metadata.

When legal rules, current discipline, translations, software, or other mutable facts matter, verify their present state. Canon-law work must name the governing body of law, jurisdiction, promulgating authority, effective or as-of date, and material amendments or authentic interpretations. It remains a study aid, not legal advice.

## Repository and build discipline

Preserve the provider hierarchy under `src/<provider>/`; the present providers are `gpt` and `claude`. New and migrated documents follow the collection schema in `guidance/repository.md`; their installed PDFs and transient artifacts mirror the same relative path under `pdf/<provider>/` and `build/<provider>/`.

- Tracked inputs and audit records belong under `src/`.
- Provider-neutral reusable external-source records and lawful retained
  artifacts belong under `src/sources/` and follow `guidance/sources.md`.
- Reviewed, publishable PDFs belong under `pdf/`.
- Reviewed, publishable web editions belong under `web/`, generated from the
  same sources and governed by `guidance/web-editions.md`.
- LaTeX intermediates, logs, caches, and other reproducible artifacts belong only under ignored `build/`.
- Shared theological or typesetting text has one authoritative source and is imported by its consumers; do not create drifting copies.
- Never use `pdf/` as a build directory or treat `build/` as an authoritative input.

Use `rg` or `rg --files` first for repository search. Use history-preserving moves for tracked paths, and update imports, build dependencies, catalogs, links, attributes, and installed mirrors coherently. Existing relative TeX imports and shared-fragment consumers must be checked before moving a source directory.

Build each affected document for enough passes to settle references and contents. Inspect logs for fatal errors, undefined references, overflow, and layout warnings. Generate review rasters and contact sheets only as `guidance/repository.md` requires. Visually inspect every rendered page, then install only the reviewed PDF. When a shared source changes, build and inspect every affected consumer. Run the profile's quality gates in addition to the universal gates in `guidance/editorial.md`.

## Commits and history

Keep structural refactors separate from substantive document revisions when the requested order permits it. Stage only the coherent files requested, verify the staged diff, and use a concise commit subject plus the `AI summary:` body required by `guidance/repository.md`. Source records and the installed PDF belong in the same content-revision commit when the profile requires both.

Do not amend, rebase, filter, force-update a ref, or otherwise rewrite history unless the user explicitly requests history rewriting and its consequences have been assessed. A project rename normally belongs in a new commit; local checkout and hosted-repository names are external operations.

<!-- tmt:agents v1 -->
Before writing any script, read tmt.json and prefer a listed tool
(`tools/<id> --help`). After deriving anything repeatable, run
`tmt note <slug>`; at two notes build it with `tmt new <slug>`.
Keep the registry honest with `tmt check`.
<!-- /tmt:agents -->
