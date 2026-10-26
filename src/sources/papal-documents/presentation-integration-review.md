# Presentation integration check, 2026-10-26

The metadata-only Beamer exporter was exercised with four real catalog
records: Quanta cura/Syllabus, the three-act Bogdanffy delivery, Lex propria,
and the corrected Monasterii Sanctae Mariae record. Two XeLaTeX passes produced
four pages. All four individual full-page rasters from `tools/pdf-review`
were inspected; no clipping, overlap, missing glyph, or misleading single-act
title was found.

The checked local PDF SHA-256 was
`73f9c96ad4f25fa9594a196e013a6163b3688f7ddd8d5a99cb093fbc2d8a19c5`;
its TeX SHA-256 was
`f3ba83be4be26761458dc49aea535f00e74547c30f61363d4305bf08195fe37a`.
The local example is under
`.scratch/presentation_integration/reviewed-role-cards/`; these hashes record
that review copy, not an installed publication or a byte-reproducibility claim
for a later Beamer build.

The cards name reviewed constituents of compound sources, identify a curial
regulation's actual issuer, and distinguish a corrected delivered title from
the erroneous index label. They carry source links and stable citation keys
without copying source bodies. The catalog's `source-links.json` maps those
catalog identities to canonical source-library works and editions.

The [reuse guide](../../../docs/papal-documents.md) gives executable export
commands, BibLaTeX citation keys, generated body-fragment imports, and unchanged
PDF appendices. Body fragments retain controlling artifact/hash comments;
their consuming publication supplies visible attribution, fonts, source
bindings, and its own review. Source cards and bibliography entries do not
establish a checked textual claim.
