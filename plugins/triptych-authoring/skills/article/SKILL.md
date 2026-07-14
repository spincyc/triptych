---
name: article
description: Create or substantially revise a source-audited Catholic faith, theology, canon-law, or mixed article. Use for discursive works whose structure follows a governing question and evidence rather than a liturgical or reference template.
---

# Articles

Create or substantially revise a discursive article whose structure follows its governing question and evidence.

## What to provide

Treat the user's complete request and thread context as controlling input, whether it follows the suggestions below or is entirely free-form.

- The question, proposed title, or existing article path, and whether the task is creation or revision.
- The desired thesis, correction, controversy, or conclusion to test rather than assume.
- The intended reader and desired theological, historical, devotional, legal, or comparative depth.
- For canon law: code or body of law, Church or persons, jurisdiction, material facts, and as-of date.
- Helpful authorities, source links, objections, schools of thought, required sections, exclusions, and any free-form context, guides, style preferences, limits, staging, or commit instructions.

## Preflight

1. Read `../../references/conventions.md` completely, apply it, and read `guidance/articles.md` completely.
2. Inspect comparable article leaves and their `research/scope.md`, `research/source-audit.md`, specialized matrices or inventories, and `generation-metadata.tex`.
3. Classify the work as faith/theology, canon law, or mixed. Name any liturgical or reference profile that controls a genuinely distinct edition-specific part.
4. For mutable law, discipline, statistics, or institutional status, establish the governing authority and current as-of boundary before drafting.

## Plan

Define the question, scope, audience, thesis to be tested, authority classes, counterarguments, source boundary, material limitations, source records, document architecture, publication target, and authorized commit boundary.

## Actions

1. Create or update the correct leaf under `src/gpt/articles/faith/` or `src/gpt/articles/canon-law/`.
2. Build a claim-driven source audit from Scripture, authoritative texts, primary historical evidence, and fit secondary scholarship. Preserve disagreement and rejected leads.
3. For theology, distinguish dogma, definitive teaching, non-definitive magisterium, patristic or liturgical witness, common teaching, disputed opinion, prudence, and project synthesis.
4. For canon law, begin with a legal scope block and distinguish text from interpretation, validity from liceity, obligation from permission, and universal law from particular, proper, special, or exceptional law.
5. Draft the argument in its natural order, give serious objections fair treatment, and avoid attributing the project's synthesis to cited authorities.
6. Complete references, research records, structured generation metadata, copyright review, build, visual inspection, installation, and the README row with separate artifact columns.

## Verification

Check every consequential quotation, locus, authority label, legal currentness claim, counterargument, source-record mapping, metadata field, PDF page, installed artifact, and catalog link under the article and universal completion gates.

## Summary

Report the article path and thesis, principal authority classes and sources used, records and artifact updated, verification completed, commit if authorized, and unresolved specialist review.

## Next Steps

Name only the most consequential remaining theological, legal, historical, statistical, or editorial review.
