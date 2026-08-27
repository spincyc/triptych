# Author or Revise Canonical Proper Leaf

## Your task

Author or revise the canonical proper leaf. The canonical leaf owns the
prose, research, and audit records. The synthesis artifact is mechanically
derived from it.

Work from the research brief the `research-synthesis` stage wrote to
`research/scope.md`, and not from any prose a controller composed for you.
`research/scope.md` is immutable input owned by `research-synthesis`. Read
it; do not edit, overwrite, append to, or regenerate it. Anything authoring
learns belongs in the files this stage owns, listed below.

## Steps

1. Create or update `main.tex` with the full research sequence:
   - Page 1: Propers map and four senses (Literal, Allegorical, Moral,
     Anagogical)
   - Page 2: Scriptural Date and Location (exactly one physical page,
     forced boundaries)
   - The Propers: Themes and Movement (begins page 3, exactly two complete
     pages, both substantively filled)
   - The Propers: Detailed Commentary (begins page 5)
   - The Propers: Notable and Quotable (3-5 non-obvious cultural/literary
     reuses: exactly the entries the brief's `Notable-and-quotable audit`
     covers)
   - The Propers: Interpretive Possibilities (4-6 exploratory proposals:
     exactly the ones the brief's `Interpretive-proposal audit` covers)
   - Sacramental Appendix (when required)
   - Appendix: Scope and Qualifications
   - References
   - Generation Metadata
2. Create or update `synthesis.tex` as a 2-line stub that defines
   `\TriptychSynthesisEdition` and inputs `main.tex`.
3. Create or update `proper-components.toml` with the component manifest.
4. Create or update `format.tex` with leaf-local LaTeX macros.
5. Create or update `generation-metadata.tex` with AI model contribution
   records.
6. Create or update `web-edition.toml` with web edition eligibility.
7. Create or update `propers/verified.md` and `propers/retrieved.txt`.
8. Leave `research/scope.md` exactly as you found it. Authoring adds no
   audit record to it: the profile keeps operational audit in that record and
   has the Scope and Qualifications appendix point at it rather than repeat
   it. Publish only what the brief's audits cover. If an audit is missing, if
   it covers entries you cannot publish, or if the gallery or the proposals
   you would publish differ from the audited ones, block rather than publish
   an unaudited entry or amend the audit yourself.
9. Ensure the brief synthesis markers
   (`triptych:brief-synthesis:start`, `:end`, `:next`) are placed correctly
   for the two-page gate.
10. Follow `guidance/editorial.md` for evidence states, attribution,
    metadata, review, and publication standards.
11. Follow `guidance/repository.md` for source ownership, target paths, and
    build rules.

## A restatement inherits the evidence state of what it restates

The guide says the same things at several lengths. A claim worked out at
length in `The Propers: Detailed Commentary` comes back compressed in `The
Propers: Themes and Movement`, in the two-page brief synthesis, in the
four-senses table on page 1, in a `Notable and Quotable` entry, and in an
`Interpretive Possibilities` proposal. Length is the only thing that changes.
A claim is not better evidenced for being said briefly: if it is an
unverified lead in the commentary it is a lead in every short form of it; if
a witness reaches the guide through a catena, an anthology, or an OCR
transcription and the commentary says so, the short form says so too; if a
negative result is bounded — one corpus, one language, a literal-string
sweep — the short form keeps that bound and never promotes it into plain
absence. The qualifications the brief attaches to a claim travel with the
claim into every place it appears, at whatever length, and an exploratory
proposal is labeled one wherever it is restated.

Compression is where this fails, and it fails invisibly: each section reads
well on its own, and only the pair shows the drop, so a reader who meets the
short form alone is told something the evidence does not support. Where a
short form has no room for the qualification, it has no room for the claim
either. Say less, or say it as the lead it is.

## Pagination constraints

- Page 1: propers map + four senses, no work-wide apparatus
- Page 2: Scriptural Date and Location only, exactly one physical page
- Themes and Movement: pages 3-4, exactly two complete readable pages
- Detailed Commentary: begins page 5
- Brief synthesis: must occupy exactly two physical pages (N and N+1)

## Result

Return a worker result with `disposition: "PASS"`, the artifact path
(pointing to `main.tex`), and a summary of what was authored or revised.

If `research/scope.md` is insufficient, contradictory, missing evidence you
need, or otherwise unsuitable to author from safely, do not repair it and do
not author around it. Return `disposition: "BLOCKED"`, naming in the summary
exactly what the brief lacks. The run stops there, and the deficiency is on
the record where the workflow can act on it; a brief quietly patched by the
author would leave no such record.

Needing evidence the brief does not carry is that insufficiency, and it is
the case most easily misread as something else. It is not a gap for this
stage to fill. Retrieving evidence is out of scope for authoring, whatever
the source and however easy the retrieval looks: no fetch, no download, no
reaching past the brief into a catalog, a library, or an edition the brief
did not put in your hands, and nothing recalled from model memory to stand
in for a date, a place, a genre, a locus, or an attribution. Ease is not
permission. A source one command away is as far out of scope as one nobody
holds, because evidence gathered here is evidence no research lane swept, no
coverage audit saw, and no rights check cleared.

The brief states, section by section, whether it supplies that section's
evidence. Where it says a section's evidence is not there, that is not a gap
for you to close either: write the section to the bound the brief records,
because a bounded negative is itself something the guide is meant to carry.
Where you need what the brief neither carries nor bounds, block, naming the
section and the evidence it wanted. That block costs one stage; authoring
around it costs a full research round, and a guide resting on evidence no
stage audited costs more than either.
