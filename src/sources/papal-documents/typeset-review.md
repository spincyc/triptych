# Papal typesetter and export review

Reviewed 2026-10-26. Disposition: **PASS within the stated review extent**.
No implementation or canonical source artifacts were edited by this review.
This review checks extraction, typesetting, and export behavior; historical
collation and the legal assessment of each edition remain separately owned.

## Findings and repairs

Two material source-fidelity findings were reported to the implementation
owner and independently rechecked after repair:

- Nested block paragraphs were concatenated without a separator, and HTML
  ordered-list markers were omitted. The extractor now recurses through nested
  blocks, preserves standard list numbering, and refuses custom CSS numbering
  requiring review. Regression cases include adjacent paragraphs, an explicit
  start/value, and reversed Roman numbering. None of the eight admitted Latin
  pages contained the defective structures, so their approved extraction
  hashes did not change because of this repair.
- XeTeX's default TeX ligature mapping changed source ASCII quotes, apostrophes,
  and backticks to curly punctuation. The source font now sets
  `Ligatures=TeXOff`; a compiled regression checks literal punctuation.
  The repaired real PDFs preserve the complete source-body character streams.
  The whole-body comparison is now also enforced by the compilation gate;
  independent comparison was repeated on the compact-apparatus revision.

## Verification

`python3 -m unittest tools.tests.test_typeset_papal tools.tests.test_papal_exports`
passes 27 tests. Tests cover exact payload/manifest agreement, rights refusal,
segment bounds and hashes, unknown selections, duplicate identities, source
escaping, extraction boundaries, punctuation, language-specific citation keys,
closed metadata exports, and source-link validation.

An independent three-page synthetic source was compiled in two distinct output
directories. Both PDFs had SHA-256
`23b957fa92808b0a746956b2ff744443cc6fd48ae8818e68015eeae614aac4f7`.
All 60 paragraph markers extracted in source order; the embedded source link
preserved its query and fragment. All three pages were inspected at full size.

The five longest real catalog titles (250–296 characters) were exported as
Beamer source cards and compiled in two XeLaTeX passes: five pages, no
Overfull, missing-character, or LaTeX warnings. The environment did not provide
Biber, so this review does not assert a bibliography-processor round trip.

All eight admitted Latin source editions pass exact complete-body comparison
against their final PDFs, totaling 378573 normalized source characters over
83 pages. The comparison uses `pdftotext -raw -enc UTF-8` in content-stream
order, removes each exact generated numeric page footer, then applies Unicode
NFKC and whitespace removal. It permits no punctuation or wording substitution.
Each entire normalized source body occurs contiguously in the extracted PDF.
Default `pdftotext` column heuristics interleave some terminal note columns;
that heuristic output must not be mistaken for omitted or reordered source
content. Normal human column order and PDF content-stream order agree.

| Edition | Pages | Reviewed PDF SHA-256 |
| --- | ---: | --- |
| hf-l-xiii-enc-15051891-rerum-novarum | 13 | `6c701c11f3b2500eaf268c63d935726bcf76448ba14c298ac351629e228db540` |
| hf-p-x-enc-19070908-pascendi-dominici-gregis | 19 | `20a0b36920617b655428297eaa9b731ca6748720d255c4691b1a66eea9b174e5` |
| hf-p-xi-enc-19221223-ubi-arcano-dei-consilio | 10 | `179288e6e77214699cfedf4b22b1c088b5696ac89b5871b2c5ae7c33ec03f360` |
| hf-p-xi-enc-11121925-quas-primas | 7 | `8c298d154e0c37c146940c7f3e9a594dcfed64d6ba822273f005714164040741` |
| hf-p-xi-enc-19260228-rerum-ecclesiae | 8 | `f701f8eca97f90000d73a390cb866ff582521ab2abb694939e70aed0b9db5c14` |
| hf-p-xi-enc-19280106-mortalium-animos | 5 | `7ee912a938dfe7733c89178ebd5b8c423d9743599a94f77078375988e0894ea3` |
| hf-p-xi-enc-19280508-miserentissimus-redemptor | 6 | `e8d11da8a6e31cfe724041810103d3198ffd5c2bfad9e63e0bffb17ab0dab238` |
| hf-p-xi-enc-31121929-divini-illius-magistri | 15 | `6fddb3d673d990f352f233a2b4ca0dbd0ef53e7501861fcd22418a1811daf120` |

The five pages of *Mortalium animos* were individually inspected through full-size
rasters made with `tools/pdf-review`. Two-column order, readable margins,
headings, body continuation, signature/date, all 30 endnotes, terminal source
notice, and final-page copyright colophon are intact, with no clipping or
overlap. The compact apparatus revision was rechecked against fresh rasters: pages
1–4 remain pixel-identical to the previously reviewed pages, and revised page
5 was inspected again at full size. The source qualification and copyright
colophon now fit together in the left column of the same final page, without
clipping, overlap, or a separate rights-only page. Both fonts
are embedded with Unicode mapping. The exact reviewed PDF hash is recorded
above. The other seven PDFs received complete mechanical text verification in
this lane; their every-page visual reviews belong to the separately assigned
review lanes.

These results do not turn a normalized web transcription into an image-collated
edition, clear an unreviewed translation, establish historical completeness, or
install/deploy a PDF. All eight source manifests were checked through
`tools/typeset-papal check --manifest src/sources/papal-documents/typeset-manifest.json --json`.
