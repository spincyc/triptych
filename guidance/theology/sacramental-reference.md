# Sacramental Reference Works

This profile governs the canonical sacramental treatise at `src/gpt/theology/sacraments/`, its mechanically composed at-a-glance companion at `src/gpt/theology/sacraments-at-a-glance/`, and their shared fragments. These are theological reference works, not proper guides or discursive articles; they follow the universal editorial standard and the treatise’s local research scope without inheriting either genre’s document template.

## Source ownership

The treatise owns the theological content. Its `fragments/`, `sections/`, `summaries/`, `summary-preamble.tex`, and `generation-metadata.tex` have one authoritative home. The at-a-glance companion and ritual-Mass appendices import those sources directly; they must not keep editable theological copies. The treatise renders its complete provenance once in a terminal `Generation Metadata` section; the companion may import its inheritance declaration earlier when that import is nonprinting and required mechanically.

The at-a-glance document is a retrieval compilation, not an independent research ceiling. Its local `generation-metadata.tex` contains its own `\AIDocumentRevisionTimestamp` followed by `\AIInheritedGenerationMetadata{theology/sacraments}`; `main.tex` imports the record, the common rights page prints the local timestamp once, and no duplicate model-provenance block is printed. The catalog explicitly names that inherited provenance. Any substantive correction begins in the treatise’s canonical source and research record, then every consumer is rebuilt and restamped. Independent prose added to a companion ceases to be mechanically derived and requires its own source audit and generation metadata.

## Treatise contract

The full sacramental reference document:

- begins with a title page and table of contents, then immediately enters the continuous theological treatment without a provenance, limitation, scope, method, or lexicon block;
- retains every chapter-specific analytical table in its relevant chapter;
- keeps `References` immediately before the terminal appendices;
- begins the terminal appendices with `Scope, Terms, and Qualifications`, containing the work-wide corpus, method, source hierarchy, authority and jurisdictional bounds, terminology controls, limitations, rights, and review state together with the metaphysical and sacramental lexicon;
- then places the complete matter–form–subject–minister–effect matrix, the single initiation-practice table for all twenty-four Catholic Churches *sui iuris*, and the seven one-page summaries in canonical order;
- ends with terminal structured generation metadata; and
- keeps every summary to one page and structurally consistent with the other summaries.

Define an indispensable technical term concisely at first use when the argument would otherwise be unreadable, but do not reproduce the full lexicon before the treatment. A jurisdictional difference, disputed theological classification, or sacrament-specific qualification remains in the chapter and summary it governs.

Every sacrament defines its matter or quasi-matter and sacramental form, identifies the intermediate reality and proper grace, and states what formal, relational, or substantial change occurs. Full treatments and summaries distinguish primary proper, intrinsic secondary, contingent, and ultimate ends where those distinctions apply. Eucharistic transubstantiation is never confused with the determining sacramental words or with a change of accidents.

## At-a-glance contract

The companion contains exactly the shared master matrix, lexicon, seven canonical summaries in sacramental order, and the single twenty-four-Church initiation page. These are its usable content rather than preliminary apparatus, so their retrieval order may remain matrix, lexicon, summaries, and initiation table. It contains no independent theological copy or prose. Its catalog entry names the canonical treatise, so it inherits that source’s generation provenance under the mechanically derived companion exception in the universal editorial standard.

## Shared-consumer validation

After changing a shared fragment, build and inspect:

1. `theology/sacraments`;
2. `theology/sacraments-at-a-glance`; and
3. every ritual guide importing an affected summary.

Verify warning-free builds, correct contents and appendix destinations, one-page summary boundaries, readable tables, and byte-identical installed/build PDFs. The treatise’s terminal metadata must display its tracked revision timestamp and AI contribution provenance once; do not duplicate the same block on the title page. Also confirm that the continuous treatment begins immediately after the title and contents and that the lexicon and work-wide qualifications occur only in the terminal appendix.
