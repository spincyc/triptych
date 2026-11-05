# Publish the reviewed source and web family

Validate `publication.toml`, all three declared output entrypoints, the exact
source/evidence review closure, and current source identities before publishing.
Follow `guidance/document-schemas.md`; do not create or install PDFs to satisfy
this source/HTML stage. No generated PDF belongs in Git or the ordinary site
artifact. A changed source or evidence closure returns to its actual review
owner; a receipt cannot renew acceptance.

There is no web edition to install. The site converts this study and its
synthesis and homily companions from their canonical TeX whenever it is built,
and no copy of their text is tracked (`guidance/web-editions.md`). Confirm that
the reviewed conversion `build/web/{provider}/{proper}.md` is still exactly what
current sources convert to and that `tools/tpt web-edition check --leaf
{provider}/{proper}` passes. Record the passed web review in the leaf's
`web-edition.toml` as its inspection: `inspected` (the review date),
`inspected_by` (the reviewing provider and run) and `inspection` (the method and
conversion hash), following `guidance/web-editions.md`. A companion reader is
converter-verified unless a review of its own conversion passed.

Create or confirm one per-publication release record for each declared source
output, the study and its `-synthesis` and `-homily` companions, with
`make add-publication ID=<output id> CATALOG=<catalog> PROVIDER={provider}
STATUS=alpha`. The catalog is `library/traditional-latin-mass.md` for 1962 and
`library/novus-ordo-liturgy.md` for postconciliar. Read and preserve correct
existing records. All three records must name the exact IDs, owning catalog,
and applicable standing authorization; generated print hashes are separate.

Wire the existing Sunday's row to the canonical reader and any actually
available reader-facing formats in the manifest's declared order. Keep source
and review apparatus in its owning records. Change only this provider's entries
in the correct cycle cell; preserve other providers and cycles. Add exactly one
canonical publication marker using the primary-provider rule in
`release/public-alpha.json`. Do not create extra rows for companions or links
to absent PDFs. A cross-reference to this study from another row needs its
own `triptych-publication-reference` marker and is not part of this stage;
the gate requires exactly one owning row.

Refresh the deterministic document catalog and source/release inventories with
their owning tools. Serialize shared catalog and release-manifest writes with
the coordinator when other productions are active. Follow the repository's
scoped release-refresh rule; do not adopt unrelated concurrent changes.
Return the exact paths this stage changed, with their hashes. The driver then
commits them, re-records the browser products (`tools/browser-products
record`, then `check`), because the new leaf changes their inputs, and adopts
the scoped release bindings (`make refresh-release-bindings ADOPT=1
ONLY="<this production's paths>"`) before advancing to the terminal gate.
Record completed source and web reviews and publication facts in the production
audit using actual engine results and receipts, never invented acceptance.

The terminal gate checks current source/schema/metadata contracts, independent
source and web review identities, exact release records, catalog links, release
bindings, document catalog, and web freshness. Source/release/authorization
checks remain global; this family's acceptance does not approve an unrelated
publication or deployment. On a failed gate sent here, repair wiring only.
Report stale reviewed inputs so production returns to their proper boundary.

If the packet also requests print export, use the separate printing workflow in
`docs/printing.md`. Only selected outputs are exported. A print review covers
exact bytes after real full-page inspection and all applicable profile gates;
source or HTML acceptance alone does not supply that review. Return concrete
source/web paths and records, any separate print receipt, or BLOCKED with the
real obstacle.
