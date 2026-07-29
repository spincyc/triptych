# Staleness review — 2026-07-29

## Exact stale-provider explanation

The repository contains only a GPT edition of
`liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies`;
there is no Claude edition of this leaf. Immediately before review,

```text
scripts/research-staleness explain gpt \
  liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies
```

reported exactly one changed input:

```text
src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies/research/guide-map.md
```

The reviewed ledger copy had SHA-256
`6e65069fb13361c8b99bdafde7df57aa5cbefa172508f30830e37e396e1fa5ca`;
the current map has SHA-256
`51dc1daffad0d2eb6f2455577d6fb1530159bb0a52c7072da3dbe8e83b45912d`.
The map changed from a held, empty structural prototype into the bounded
public-alpha account now consumed by the leaf. No sibling-provider,
reusable-source, canonical-inventory, plate, artwork, source-audit, or
production record is named by the exact explanation.

## Candidate treatments

- `build/staleness/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies/modified/`
  is the minimal source-equivalent treatment of the current shell.
- `build/staleness/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies/rewritten/`
  is a research-first treatment derived from the profile, edition selection,
  canonical records, generated view, manifests, and audits. It changes only
  the compact title/opening wording; it consumes the same authoritative
  selection and plates.

Both are ignored audit candidates, not installed replacements.
Each candidate settled in two pdfTeX passes at sixteen US-Letter pages. The
logs contain no fatal error, undefined control sequence, overfull box, or
rerun request. Both reproduce the same four underfull-box warnings from the
shared generated view (badness 1308, 2538, 3838, and 1436); this audit does
not misstate those inherited warnings as resolved and does not substitute for
the ordinary every-page visual gate.

## Consequential-claim comparison

| Claim family | Old/current publication | Modified | Rewritten | Effect of changed map |
|---|---|---|---|---|
| Publication state | Bounded public Alpha with the reliance boundary in terminal qualifications | Same | Same | Adds the public-alpha state relative to the old ledger map; agrees with the current publication. |
| Selection | Canonical `ed-pontifical` union of publication-ready pontifical/prelatial records and genuinely required/useful pontifical relevance, excluding unresolved status and the lavatory image | Same | Same | Adds the populated selection and replaces the empty-prototype account; no candidate disagreement. |
| Inventory size | Forty-three admitted canonical records | Same | Same | Adds a bounded count, not a completeness claim. |
| Visual proximity | Does not create pontifical relevance | Same | Same | Strengthens the selection boundary; all treatments agree. |
| Pontifical vesture and insignia | Sourced identity, layering, bearer, rank, privilege, and occasion distinctions only | Same | Same | Adds rendered, admitted records while retaining source ceilings; no contradiction. |
| Ordinary appointments, lights, books, linens, vessels, furnishings, and incense | Enter only where recorded as ordinary pontifical-Mass support; they are not reclassified as insignia or distinct pontifical forms | Same | Same | Adds multiple supporting families and repeatedly strengthens the non-insignia boundary. |
| Materials, dimensions, ornament, scale, morphology, arrangement, and handling | Asserted only where the canonical record supports them; otherwise expressly not universalized | Same | Same | Adds source-minimal limits for Lavabo articles, altar cloths, incense set, thurible, cruets, Communion plate, chalice/paten, books, and other supporting objects. |
| Safety and operations | Thurible, candle-service tool, elevation torch, and other potentially hazardous objects receive non-operational limits | Same | Same | Adds or strengthens local safety limits; no candidate disagreement. |
| Processional and sacristy supports | Processional cross is optional/local ordinary support; cross-or-image and signal bell preserve their alternatives/local-practice limits | Same | Same | Adds qualified supporting-object treatment and avoids pontifical reassignment. |
| Epistle and Gospel books | Exact-source minister/use relationships only; no asserted binding morphology, material, dimensions, alias, or ordinary Gospel lectern | Same | Same | Adds a tightly bounded book relationship; no substantive disagreement. |
| Sacristy lavatory | Canonical preparation record retained but withheld pictorially pending a checked material exemplar | Same | Same | Adds a visible evidentiary hold rather than plausible morphology. |
| Holy-water vessel and aspergillum | Ordinary related-ceremony support with bounded Asperges relationship and documented sprinkler variants | Same | Same | Adds a qualified related-ceremony family; no pontifical-insignia claim. |
| Conopaeum and Eucharistic ombrellino | Cross-referenced related-ceremony objects only; neither becomes pontifical insignia | Same | Same | Adds and strengthens the taxonomy split. |
| Explicit exclusions | Altar bells, Holy Week lectern, and book markers lack a proved pontifical-specific relationship | Same | Same | Removes them from the admitted edition rather than inferring relevance. |
| External review | No external-review admission path; Alpha follows the repository's source, rights, safety, reproducibility, mechanical, and visual gate | Same | Same | Removes the obsolete priestly-review hold/admission model. |
| Authority and completeness | Study reference, not an official liturgical book, local direction, complete corpus, or full ceremonial sequence | Same | Same | Replaces the empty-prototype warning with accurate bounded-alpha qualifications without enlarging authority. |
| Web edition | Ineligible pending a mechanically valid, visually checked rendering | Same | Same | No effect; the changed guide map makes no web-readiness claim. |

Relative to the ledger-era guide map, the changed record adds the populated
Alpha selection, removes the obsolete empty-prototype and external-review
model, strengthens many source and taxonomy limits, and excludes unsupported
relationships. It neither weakens nor contradicts a consequential claim in
the old/current publication. The modified and rewritten candidates differ in
title and opening rhetoric only; they agree on every object-selection,
classification, source-ceiling, safety, authority, and omission claim.

## Verdict

**No material change to the current publication.** The staleness is the
edition-local map catching up from its ledger-era held-prototype state to the
already rendered bounded Alpha. Both candidates independently support the
current canonical selection and qualifications. No source, inventory, plate,
artwork, PDF, web, catalog, or release replacement is warranted. This review
does not rebaseline the edition.
