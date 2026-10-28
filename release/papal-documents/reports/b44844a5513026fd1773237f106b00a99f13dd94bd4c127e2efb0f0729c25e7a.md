# Latin source editions: visual review

Reviewed 26 October 2026 under `guidance/papal-documents.md` and the repository
PDF-review contract. The final renderer revision is `2026-10-26T02:57:48Z`.

Every page listed below was initially inspected as an individual full-page
raster, in addition to each document's contact sheet. After the declared
*Quas primas* source correction and compact source-notice revision, all 30
final page PNGs were compared with that reviewed set: 26 are byte-identical.
The four changed pages—*Rerum novarum* 13, *Ubi arcano Dei consilio* 10, and
*Quas primas* 6–7—were opened individually and reviewed again. Both raster
sets were generated with the repository's `tools/pdf-review` helper. This
record covers visual usability; the separate mechanical text, provenance,
rights and historical source checks remain separately owned.

| Document | Pages inspected | Reviewed PDF SHA-256 | Disposition |
| --- | --- | --- | --- |
| *Rerum novarum*, Latin, 15 May 1891 | 1–13, all 13 pages | `6c701c11f3b2500eaf268c63d935726bcf76448ba14c298ac351629e228db540` | PASS |
| *Ubi arcano Dei consilio*, Latin, 23 December 1922 | 1–10, all 10 pages | `179288e6e77214699cfedf4b22b1c088b5696ac89b5871b2c5ae7c33ec03f360` | PASS |
| *Quas primas*, Latin, 11 December 1925 | 1–7, all 7 pages | `8c298d154e0c37c146940c7f3e9a594dcfed64d6ba822273f005714164040741` | PASS |

## Findings

Across all 30 pages, the two columns read left to right in their intended
sequence. The identification blocks, dense body pages, signatures, dating
clauses, historical endnotes, terminal source notes and rights colophons are
legible. No clipping, overlapping text, missing-glyph boxes, intrusion into
the gutter or footer, illegible source notice, or detached rights-only page
was observed. These are observations of rendered layout, not a claim of full
collation against the historical printing.

*Rerum novarum* page 13 is sparse: its closing body text, signature and dating
clause, followed by the source and rights apparatus, occupy the upper part of
the first column; the second column is empty. The preceding page is full and
the final page includes substantive source text. This natural ending is a
nonblocking composition observation, rather than a blank or rights-only spill
page.

The initial *Quas primas* review found a material reading defect near the top
of the right column on page 6: one source paragraph ended `quae a C`, followed
by a separately indented paragraph beginning `hristo perfecta societas`.
That split was present in the normalized source artifact ending
`latin-text-2564bfc8f013`; the initial PDF hash was
`af0bed412373245637d3c7a025e68249f1fbd62e1ddd3d5122037fcfd2712648`.
The source approval in `publication-approvals.json` now records the declared
join against AAS 17 (1925), printed pages 608–609, supplying no letters and
making no other wording change. The final derivative is
`artifact.pius-xi.quas-primas.2026-10-26-vatican-la.latin-text-549b7a6e70f9`,
SHA-256 `549b7a6e70f9f799e74781980f2586a06a1f75d9553c82d1cccd2e7c3914b31d`.
The final page-6 raster visibly reads `quae a Christo perfecta societas`
within the continuous paragraph. Page 7's reflow, dating clause, signature,
notes and compact terminal notice are clean. The finding is resolved.

The final compact source notices and rights colophons are readable and do not
overlap body text or page numbers. *Ubi arcano Dei consilio* page 10 carries
the source notice continuously from the bottom of the left column to the top
of the right column, with the colophon following. No blocking visual finding
remains. A changed source derivative or changed PDF requires a new
hash-specific review disposition; this record does not preapprove regenerated
bytes.
