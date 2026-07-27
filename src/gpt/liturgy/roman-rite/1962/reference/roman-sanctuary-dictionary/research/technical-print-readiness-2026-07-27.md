# Artwork technical print-readiness audit

Audit date: 2026-07-27
Scope: the current altar-server review PDFs, the historical dictionary proof,
and every tracked dictionary PNG.

This is a technical preflight, not factual, ceremonial, rights, physical-print,
photocopy, consumer, or release approval.

## Disposition

- The canonical dictionary artwork TOML reconciles with every tracked PNG:
  dimensions, bit depth, color mode, bytes, and SHA-256 all match.
- Every non-rejected dictionary PNG is now stripped 8-bit grayscale without
  alpha or an embedded color profile.
- The three rejected vestment studies remain exact RGB research leads. They
  are not publication inputs and were deliberately not normalized.
- The two historical proof assets were project-created and publication-facing,
  so they were safely normalized without resizing. The early-medieval plate
  changed from 1,907,506-byte RGB to 704,175-byte grayscale; its normalized
  SHA-256 is
  `613ee9f2fbba6f64c0386bce82d53bda02205cf1a97540d94f53b30244957b69`.
  The pre-1955 plate changed from 1,888,324-byte RGB to 611,323-byte
  grayscale; its normalized SHA-256 is
  `3263d01430d30c57209f1e4ecbcf1e7279771aceb0d96c4a819566bd3b7b8916`.
- The pre-1955 plate had one hard print-resolution failure: 238 effective dpi
  at its former 4.85-inch placement. Its maximum proof placement is now 3.35
  inches, producing 345 effective dpi. The early-medieval plate remains 311
  effective dpi. The rebuilt two-page proof has no log warning.
- Low Mass child artwork has no sub-300-dpi failure. Two compact ablution
  figures on page 22 render at 470 effective dpi, above the repository's
  450-dpi investigation trigger.
- The Low Mass trainer has no sub-300-dpi failure. Eleven compact figures
  render at 577 or 706 effective dpi. These are investigation triggers caused
  by deliberately smaller trainer-lane placements, not evidence of inadequate
  source resolution or print degradation. No additional downsampling is
  warranted while the same canonical assets also serve the larger child
  placements.
- Missa Cantata and Solemn Mass review PDFs render their pencil scenes at 327
  and 326 effective dpi respectively, with no technical trigger.
- The six current dictionary priestly-review PDFs each contain six embedded
  review images across six portrait pages. No image falls below 300 effective
  dpi. Five portrait assets render at 1,082 effective dpi and the landscape
  paten asset at 721 effective dpi in each consumer. Those high-resolution
  investigation triggers arise from compact review-grid placement, not
  inadequate source resolution. They do not replace full-size visual,
  physical-print, or monochrome-photocopy inspection.

## Automation

`scripts/artwork-library check` now understands the canonical
`[[asset_files]]` manifest as well as the compact manifest form. It validates
path confinement, unique identities and paths, PNG structure and CRCs,
dimensions, bit depth, mode, byte count, SHA-256, and the grayscale/no-alpha/
no-profile publication contract while preserving rejected research leads.

`scripts/artwork-library check-pdf` uses Poppler's embedded-image report to
fail images below 300 effective dpi and separately report images above the
450-dpi investigation trigger. `--strict-review-triggers` is available for a
review job that should stop on either condition.

`scripts/artwork-library normalize` writes through an atomic same-directory
temporary and verifies the result before replacement. It must be used only for
project-owned publishing assets; acquired evidence artifacts remain outside
its authority.

## Gates still open

- actual-size print and monochrome-photocopy inspection;
- full-size factual and visual inspection of every figure;
- independent liturgical and ceremonial review;
- rights, consumer, and release review;
- rendered reconciliation of the comprehensive and use-derived review copies
  after every further source, selection, artwork, or typesetting change.
