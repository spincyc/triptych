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
