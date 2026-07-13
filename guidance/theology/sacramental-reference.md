# Sacramental Reference Works

This profile governs the canonical sacramental treatise at `src/gpt/theology/sacraments/`, its mechanically composed at-a-glance companion at `src/gpt/theology/sacraments-at-a-glance/`, and their shared fragments. These are theological reference works, not proper guides or discursive articles; they follow the universal editorial standard and the treatise’s local research scope without inheriting either genre’s document template.

## Source ownership

The treatise owns the theological content. Its `fragments/`, `sections/`, `summaries/`, `summary-preamble.tex`, and `generation-metadata.tex` have one authoritative home. The at-a-glance companion and ritual-Mass appendices import those sources directly; they must not keep editable theological copies.

The at-a-glance document is a retrieval compilation, not an independent research ceiling. Its local `generation-metadata.tex` contains only an `\AIInheritedGenerationMetadata{theology/sacraments}` declaration, which `main.tex` imports without printing a duplicate block; the catalog explicitly names that inherited provenance. Any substantive correction begins in the treatise’s canonical source and research record, then every consumer is rebuilt. Independent prose added to a companion ceases to be mechanically derived and requires its own source audit and generation metadata.

## Treatise contract

The full sacramental reference document:

- begins with a title page rendering its structured, nonduplicated AI-generation metadata and a table of contents;
- places the metaphysical and sacramental lexicon before the continuous main treatment;
- retains every chapter-specific analytical table in its relevant chapter;
- keeps `References` immediately before the terminal appendices;
- places the complete matter–form–subject–minister–effect matrix, the single initiation-practice table for all twenty-four Catholic Churches *sui iuris*, and the seven one-page summaries in canonical order in those appendices; and
- keeps every summary to one page and structurally consistent with the other summaries.

Every sacrament defines its matter or quasi-matter and sacramental form, identifies the intermediate reality and proper grace, and states what formal, relational, or substantial change occurs. Full treatments and summaries distinguish primary proper, intrinsic secondary, contingent, and ultimate ends where those distinctions apply. Eucharistic transubstantiation is never confused with the determining sacramental words or with a change of accidents.

## At-a-glance contract

The companion contains exactly the shared master matrix, lexicon, seven canonical summaries in sacramental order, and the single twenty-four-Church initiation page. It contains no independent theological copy or prose. Its catalog entry names the canonical treatise, so it inherits that source’s generation provenance under the mechanically derived companion exception in the universal editorial standard.

## Shared-consumer validation

After changing a shared fragment, build and inspect:

1. `theology/sacraments`;
2. `theology/sacraments-at-a-glance`; and
3. every ritual guide importing an affected summary.

Verify warning-free builds, correct contents and appendix destinations, one-page summary boundaries, readable tables, and byte-identical installed/build PDFs. The treatise’s title-page metadata must describe its final generation event once; do not duplicate the same block at the end.
