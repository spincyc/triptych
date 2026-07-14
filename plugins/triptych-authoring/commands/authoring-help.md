---
description: Choose the correct Triptych authoring workflow and identify the inputs it needs.
argument-hint: "[document idea, target path, or desired outcome] [free-form context and limits]"
---

# /authoring-help

Route a proposed creation, revision, audit, or publication task to the narrowest applicable command and profile without changing repository files.

## What to provide

The user's complete invocation context is:

$ARGUMENTS

Treat all of it as controlling input, whether it follows the suggestions below or is entirely free-form.

- A document idea, existing title or path, problem to solve, or desired publication outcome.
- Any known rite, edition, language, territory, calendar, jurisdiction, source corpus, or as-of date.
- Any free-form context, desired emphases, guides, exclusions, limits, staging, or review concerns.

## Preflight

1. Read `plugins/triptych-authoring/commands/_conventions.md`.
2. Inspect the README catalog and profile routing in `AGENTS.md`.
3. If an existing target is named, locate it and identify its controlling profile without editing it.

## Plan

Classify the request by actual object and source needs, not merely by words in the title. Identify any secondary profile that genuinely governs a distinct part of a mixed work.

## Commands

Recommend exactly one primary command when possible:

- `/article` for discursive faith, theology, canon-law, or mixed essays;
- `/novena` for a full novena and condensed prayer book;
- `/mariology` for Rosary, dogma, devotional, or general Mariological references;
- `/apparition` for apparition events, messages, judgments, or authority-qualified corpora;
- `/proper-1962` or `/proper-postconciliar` for variable liturgical formularies;
- `/ordinary` for stable Mass texts, ritual sequence, or cross-edition Order-of-Mass exposition;
- `/assembly-1962` for calendar, precedence, Mass-class, commemoration, or formulary-assembly rules;
- `/sacrament` for the canonical sacramental treatise and derived consumers;
- `/revise` for a cross-cutting change to an existing document;
- `/audit` for report-first or explicitly authorized remediation;
- `/publish` for completed source that needs artifact and catalog handling.

List the minimum blocking input and the most useful optional input for the selected command. Treat the user's existing prose as valid free-form input; do not force it into a form.

## Verification

Confirm that the recommended command's profile owns the requested object and that no existing specialized profile has been bypassed.

## Summary

Return the selected command, a one-sentence reason, the information already supplied, and the few remaining inputs that would materially improve or unblock the work.

## Next Steps

Show one ready-to-run invocation using the user's own context. Do not edit files or begin research until the user invokes or otherwise authorizes the selected workflow.
