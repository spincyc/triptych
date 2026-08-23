# Author or Revise Canonical Proper Leaf

## Your task

Author or revise the canonical proper leaf. The canonical leaf owns the
prose, research, and audit records. The synthesis artifact is mechanically
derived from it.

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
     reuses)
   - The Propers: Interpretive Possibilities (4-6 exploratory proposals)
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
8. Create or update `research/scope.md`.
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
