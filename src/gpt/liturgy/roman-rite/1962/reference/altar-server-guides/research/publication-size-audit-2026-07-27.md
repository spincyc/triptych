# Publication size audit

Date: 27 July 2026

## Scope

The final release pass measured every installed PDF under `doc/`, with special
attention to the black-and-white altar-server guides and their pencil-style
diagrams. It also checked the five studies completed or recovered in this pass.

## Findings

- The largest installed PDF is the Low Mass trainer manual at 2,836,532 bytes.
- The reader Low Mass guide is 2,823,041 bytes.
- The Missa Cantata and Solemn Mass guides are 1,259,750 and 1,304,241 bytes.
- The completed Abraham, exorcism, and Claude Ordinary PDFs are 295,990,
  361,988, and 579,180 bytes.
- The recovered John 6 and linen-cloths PDFs are 331,662 and 391,311 bytes.
- The Low Mass guide's pencil diagrams are grayscale raster images at about
  400--450 ppi. Their embedded streams are approximately 492--606 KB each.
- No installed PDF reaches 3 MB, and no empty tracked or untracked directory
  residue remained outside reproducible build output.

## Disposition

No further compression is warranted for this release. Converting the pencil
art to one-bit line work would reduce size but would also discard the tonal
texture that gives the diagrams their intended hand-drawn character. The
current grayscale assets retain that character while keeping every installed
publication below 3 MB. Future image-bearing publications should use grayscale
or one-bit assets as the artwork permits, avoid color profiles and unnecessary
alpha channels, and repeat this installed-file audit before release.
