---
name: proper-1962
description: Create a source-audited 1962 Roman Rite temporal, ritual, votive, or other proper guide. Use for a defined formulary requiring checked Missal text, structural exposition, source records, compact material, and publication artifacts.
---

# 1962 Propers

Create a complete guide to a defined formulary in the 1962 Roman Missal, with a checked liturgical text, structural exposition, compact companion material, and any required sacramental appendix.

## What to provide

Treat the user's complete request and thread context as controlling input, whether it follows the suggestions below or is entirely free-form.

- The exact formulary, feast, temporal day, ritual Mass, votive Mass, or other proper and its intended catalog placement.
- Its rank, occurrence or use context, internal ordering key if known, and the Missal pages, headings, cross-references, or facsimile links already identified.
- Seasonal substitutions, commemorations, classes, ritual variables, sacramental circumstances, or local calendar assumptions that matter.
- Desired thesis, symbolic or patristic emphases, compact-use needs, disputed questions, and all free-form sources, guides, exclusions, limits, staging, or commit instructions.

## Preflight

1. Read `../../references/conventions.md` completely, apply it, and read `guidance/liturgy/roman-1962-propers.md` completely.
2. Identify the exact 1962 edition, formulary locus, heading, inherited common or cross-reference, calendar context, and every affected catalog status field.
3. Use a public facsimile or equivalent edition witness as the transcription baseline; use OCR only as a finding aid and record every verified locus.
4. Inspect the nearest completed proper, shared sacramental-summary consumers if applicable, and the Makefile target and publication mirror.

## Plan

Define the proper’s source boundary, ordered liturgical units, guide architecture, compact and speculative layers, sacramental consumer relationship, research records, catalog identity, publication artifacts, and discrete commit stage.

## Actions

1. Create or revise the proper under the appropriate `src/gpt/liturgy/roman-1962/propers/` collection leaf without exposing internal ordering keys in reader-facing titles or prose.
2. Preserve every appointed element, rubric, cross-reference, seasonal replacement, commemoration rule, and variant that belongs to the bounded formulary. Create or update `research/retrieved.txt`, `research/verified.md`, `research/scope.md`, and the source audit required by the profile.
3. Give the reader the guide’s controlling claim and the entire liturgical sequence early. Keep the opening liturgical synopsis and the *In Illo Tempore* layer in their profile-defined locations.
4. Supply unit-by-unit scriptural, patristic, historical, ritual, doctrinal, and symbolic exposition with calibrated claims. Keep expansive synthesis and clearly labeled speculative proposals distinct from verified received meaning.
5. Produce the profile-required compact synthesis and any warranted quotable material. When a ritual guide consumes sacramental theology, import the canonical sacramental summary rather than copying it.
6. Refresh structured generation metadata and the README’s guide, source, and theology-status columns. Use the exact catalog status vocabulary required by the profile.
7. Build for enough passes to settle contents and references, inspect logs and every page, rebuild every shared consumer, and install only the reviewed PDF.

## Verification

Run the full 1962-proper gates: edition and locus identity, transcription, sequence completeness, rubric and variant handling, source records, page architecture, claim calibration, sacramental import identity, metadata, catalog statuses and links, clean build, every-page inspection, and installed/build identity.

## Summary

Report the formulary and catalog location, edition loci, records and sources checked, guide layers completed, shared consumers rebuilt, PDF and README changes, verification, authorized commit, and unresolved liturgical or textual questions.

## Next Steps

Name the single facsimile collation, rubrical review, patristic check, or sacramental review most valuable next.
