# Publication size audit

Date: 27 July 2026

## Scope

The final release pass measured every installed PDF under `doc/`, with special
attention to the black-and-white altar-server guides and their pencil-style
diagrams. It also checked the five studies completed or recovered in this pass.

## Current altar-server findings

The four replacement Low-Mass scenes installed later on 27 July supersede the
smaller snapshot originally measured by this audit. The current installed
altar-server guide sizes are:

| Publication | Bytes |
|---|---:|
| Low Mass child guide | 7,847,547 |
| Low Mass trainer manual | 7,860,317 |
| Missa Cantata | 1,258,883 |
| Solemn Mass | 1,304,972 |

The Low Mass trainer manual is therefore the largest installed repository PDF
at this checkpoint, and both Low Mass guides exceed 3 MB. Their increased size
comes from the four full-resolution replacement raster scenes. The source
artwork manifest records their exact binary identities and dimensions; the
production manifest records the exact installed PDF identities.

For comparison, two other publications revised during the same repository
pass currently measure 361,839 bytes for the exorcism history and 391,015 bytes
for the linen-cloths study. These comparison figures are incidental and do not
bind those publications' release state.

## Disposition

The earlier conclusion that no installed publication reached 3 MB is
superseded. No new compression decision is made by this reconciliation:
replacement-art normalization, print-detail comparison, rebuilt-file size,
and every-page visual inspection must be evaluated together before changing
the current assets. Future image-bearing publications should use grayscale or
one-bit assets as the artwork permits, avoid color profiles and unnecessary
alpha channels, and repeat this installed-file audit after the final reviewed
artwork is fixed.
