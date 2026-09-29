# Production review — GPT angelology

Review date: 29 September 2026. Publication: *Angels and the Gift of Being:
A Thomistic Study of Nature, Grace, and Ministry*. Revision timestamp:
`2026-09-29T21:48:19Z`.

## Text and research

The original exposition follows all 118 articles in ST I qq.50–64 and
106–114, with 24 ordered question dossiers and two Christological dossiers.
All fifteen chapters of the Celestial Hierarchy receive exposition. The
canonical question inventory projects to 118 unique appendix rows; nine
stable order keys control the comparative ordering. Twelve lettered appendices
supply the census, orders, parallels, concordance, chronology, calendar,
Scripture, powers, first sin, terminology, witnesses, and terminal scope.

The source audit and its five detailed records preserve actual reading
scopes. All 69 publication bindings are fingerprinted. Source-library validation
passes with 2,908 artifacts, 1,049 editions, 5,199 passages, 94 segments,
776 works, five corpora, and 3,186 bindings across the repository. These
are graph totals, not claims that this publication read the entire library.

A separate Codex research review checked selected difficult determinations
and the Dionysian reception. Resulting corrections include Aquinas's denial
of simultaneous natural cognition through distinct species, the proper
Salmond attribution for Damascene, inclusive Parker chapter pagination,
Gregory's Homily XXXIV, and precise limits of angelic bodily and voluntary
causation. The article grades and owning profile were reconciled with the
maintainer's requested affirmative Catholic voice. This is documented AI
research review; no independent human theological approval is claimed.

## PDF build and visual review

`make doc PROVIDER=gpt DOC=theology/angelology` passes. The final LaTeX log
has no warnings, undefined references, overfull boxes, or underfull boxes.
The 62-page PDF uses embedded, subsetted Latin Modern fonts with Unicode
mapping. Title and subject metadata are present. The common rights colophon
and revision timestamp share the final reference page.

Reviewed PDF SHA-256:
`f2bd6116ad41e7459ce0ab48bebf6327844dc82676908960c77f893617959bec`.

Every physical page was inspected from full-page rasters prepared by the
registered `pdf-review` tool. The coordinator inspected pages 1–21; a separate
reviewer inspected 22–42; the ministry reviewer inspected 43–62. Orphan census
headings and dossier openings were repaired with reserved space. Footnote
markers were attached to their preceding punctuation, the final revision
line separated from the references, and the short names table kept with its
header. Changed ranges were reinspected. A proposed wider census gutter was
reviewed directly by the coordinator: the existing spacing separates the
columns without overlapping text, so no further change was made.

The reviewed intermediate layout had SHA-256
`f558e5ed4bed9bc1e589bfe89cfa8dc6ffe0fc86d67d0a198b29703988aa2b7e`.
The final candidate's page rasters differ only on physical pages 55, 56,
and 62; those three were separately inspected and pass. All other rasters
match the reviewed layout byte for byte. The subsequent blank-line guard
needed by Pandoc leaves the entire PDF byte-identical. Raster directories
are disposable build output; this record retains their scope and result.

## Installation and integration

The reviewed PDF was installed with `make install-doc PROVIDER=gpt
DOC=theology/angelology`; the built and installed SHA-256 values match the
reviewed identity above. The reviewed web edition is installed and its
separate [web review](web-review.md) records conversion and browser checks.
The Faith catalog links the GPT PDF and web reader. The separate unfinished
Claude source is inventoried on its tracked state and explicitly held from
publication. Two initial untracked Claude section files remain outside the
new deliverable and are preserved byte for byte.
The maintainer subsequently authorized pushing the completed work to `main`
and verifying the automatic GitHub Pages deployment.


## Repository validation

The complete `make check-sources` target passes on the tracked deployment
candidate, including the deployment source checks, both publication inventories,
the source-reader and document-catalog projections, containment, and the family
migration ledger. The two pre-existing untracked Claude sections were temporarily
preserved outside the scanned tree and restored in a `finally` block; they are
neither adopted as GPT work nor added to the tracked Claude inventory.

The local clone initially lacked the previously published PDFs, which are
intentionally untracked. To validate the assembled site without rebuilding or
substituting unrelated publications, 234 missing installed PDFs were restored
from the successful live deployment at commit
`a53e262d00d2658ac079801b07b26deeffb05a6d` (Pages run `36506250643`). Every restored
file matches both the live publication manifest and `SHA256SUMS`. All 942
observed build-input files, including the Makefile and workflow, match that
commit; there are no changed or unknown prerequisites. The new GPT angelology
PDF and six installed reading-plan PDFs were preserved unchanged. These restored
files total 267,651,824 bytes. The local receipt is disposable; this durable
record retains the verification scope and deployment basis.

Release bindings, the complete site artifact, promise reconciliation, and
Git delivery are still being finalized.
