# Paten catalog-exemplar artwork review

Review date: 2026-07-27

Asset: `shared/artwork/pencil/RPD-FIG-sacred-vessels-0003-comparison-paten-exemplar.png`
SHA-256: `7c344a7fe84a1995303f82559e4e7447cee468a4c35466267edd7e9e1ac9c85f`

## Decision

Accepted for the altar-server alpha consumer, with release still pending.

The plate is explicitly one Met catalog exemplar. Its dimensioned top and
side views are bounded by object 463080's catalog record; the prepared inset
is bounded by *Missale Romanum* 1962, *Ritus servandus* I.1. It does not claim
that the exemplar's silhouette or decoration is universal.

The distinct Communion plate is not drawn. The plate states only the checked
X.7 distinction: it is the under-chin `patina`, not the celebrant's `patena`,
and its visual form remains unresolved.

## Generation and normalization

The built-in image-generation tool received the exact Met Open Access image as
a reference. The complete initial and targeted-correction prompts are retained
in `research/artwork-manifest.toml`. The selected correction output was
1536 by 1024 sRGB, 2,198,320 bytes, SHA-256
`95f3d1e2339413577f13ca6ea846da1cc1b6d58e9c039da0c362644604faa60c`.

The generated common-scale inset remained proportionally inexact and was
therefore removed rather than published. The surviving plate was converted to
stripped Gray8 without resampling. The normalized file is 628,594 bytes,
SHA-256 `7c344a7fe84a1995303f82559e4e7447cee468a4c35466267edd7e9e1ac9c85f`.

## Visual and rights review

- top, side, and prepared views are complete and unclipped;
- the 16.3 cm diameter and 1.2 cm height labels are legible;
- the prepared inset visibly places paten above purificator above chalice;
- no host, hands, people, handled plate, raised-edge plate, or Communion-plate
  drawing appears;
- graphite remains legible after grayscale normalization; and
- the Met reference image is marked Public Domain under its Open Access
  record; the project raster is newly generated and does not redistribute the
  reference photograph.

Actual composed-page review and print/release approval remain separate gates.
