---
description: Create a full bilingual novena and its canonical condensed daily prayer companion.
argument-hint: "<devotion, mystery, saint, feast, or event> [calendar, prayers, traditions, free-form guidance and limits]"
---

# /novena

Create a new source-audited novena in the numbered collection together with its recitation-only daily prayer book.

## What to provide

The user's complete invocation context is:

$ARGUMENTS

Treat all of it as controlling input, whether it follows the suggestions below or is entirely free-form.

- The devotion, divine mystery, saint, title, feast, or saving event that orders the novena.
- Its principal annual placement or desired date rule, including territory or calendar when relevant.
- The proper addressee of prayer and any received prayers, hymns, antiphons, litanies, Latin or Greek witnesses, or preferred public-domain English versions.
- Any apparition, promise, indulgence, scapular, confraternity, shrine, or approval tradition that requires exact status treatment.
- Intended reader, desired daily themes or acts, source suggestions, exclusions, and all free-form context, guides, literary preferences, limits, staging, or commit instructions.

## Preflight

1. Apply `commands/_conventions.md` and read `guidance/devotions/novenas.md` completely.
2. Inspect the existing novena order, choose the next stable internal `N10`-spaced key without exposing it in reader-facing text, and confirm that the proposed work is not already present.
3. Identify every calendar, jurisdiction, private-revelation, approval, indulgence, translation, or copyright fact requiring current official verification.
4. Inspect an existing full-guide/companion pair and the Makefile's cross-document dependency pattern.

## Plan

Define the full guide, canonical prayer fragments, condensed companion, scope and source records, calendar rule, nine-day architecture, approval boundaries, build dependencies, adjacent catalog rows, and discrete commit stages requested by the user.

## Commands

1. Create the full leaf at `src/gpt/devotions/novenas/<numbered-document>/` and its sibling `<numbered-document>-daily-prayer/`.
2. Establish historical provenance, the ninefold rationale, liturgical relationship, calendar rule with a dated example, doctrinal object, and exact status of every received tradition.
3. Give each day a distinct scriptural center, source-grounded meditation, intention, examination or act, and unique prayer.
4. Print every recited English prayer beside its complete Latin or Greek witness. Record whether each text and translation is official, received, public domain, licensed, materially adapted, or project-composed.
5. Put every prayer shared with the companion in a canonical fragment owned by the full guide. The companion imports those fragments, adds no independent theology or prayer, uses inherited generation metadata, and keeps `research/derivation.md`.
6. Complete the full guide's `research/scope.md`, `research/source-audit.md`, `research/prayer-inventory.md`, any needed status record, and structured generation metadata.
7. Register dependencies, build and inspect both consumers, compare rendered prayer texts exactly apart from line wrapping, install both PDFs, and place the companion immediately after the full guide in the README.

## Verification

Run every novena and companion completion gate: doctrine and addressee, public/private revelation boundaries, calendar reproducibility, nine distinct days, bilingual completeness, translation ownership, approval and indulgence currentness, one-to-one derivation, metadata, dependency rebuilds, every-page inspection, installed/build identity, and catalog links.

## Summary

Report the two source leaves and PDFs, calendar placement, principal prayer witnesses and statuses, source and derivation records, verification, authorized commits, and outstanding linguistic, liturgical, historical, theological, or ecclesiastical review.

## Next Steps

Name the single specialist review or missing source collation most important before treating the prayer book as mature.
