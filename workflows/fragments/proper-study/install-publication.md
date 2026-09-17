# Install and wire the reviewed three-document family

Install the three accepted PDFs with `make install-doc DOC=<id>
PROVIDER={provider}`, for the bare ID, `-synthesis`, and `-homily`. Do not
retypeset or alter accepted content. Confirm the artifact snapshot is still
current. Install the reviewed canonical Markdown from
`build/web/{provider}/{proper}.md` to `web/{provider}/{proper}.md`, byte for
byte, and stage that Markdown so the publication gate can prove it is tracked.
Do not create a separate companion web authority.

Create one per-publication release record for each PDF using
`make add-publication ID=<id> CATALOG=<catalog> PROVIDER={provider} STATUS=alpha`.
The catalog is `library/traditional-latin-mass.md` for 1962 and
`library/novus-ordo-liturgy.md` for postconciliar. Read and preserve a correct
existing record rather than overwriting it blindly. All three records must
name the exact IDs and catalog and the standing authorization.

Wire the existing Sunday's row to all three PDFs and the canonical web page,
in the output-label order the schema-2 manifest declares. Change only this
provider's entries in the correct cycle cell; preserve other providers and
cycles. Add exactly one canonical publication marker using the primary-provider
rule in `release/public-alpha.json`. Do not create extra rows for companions.

Refresh the deterministic document catalog and source/release inventories with
their owning tools. Serialize shared catalog and release-manifest writes with
the coordinator when other productions are active. Follow the repository's
scoped release-refresh rule; do not adopt unrelated concurrent changes.
Record completed reviews and installation facts in the production audit using
the actual engine results and receipts, never invented acceptance.

The terminal program gate decides acceptance: installed/build byte identity,
current artifact and web receipts, source/metadata contracts, exact release
records, catalog links, release bindings, document catalog, and web freshness.
The public-alpha check is scoped to this canonical owner's three outputs;
unrelated absent PDFs are not evidence of failure of these outputs or a global
deployment approval. Source/release/authorization checks remain global. The
engine checks its immutable accepted review seals before these terminal checks
and routes stale evidence to its actual author; refreshing a receipt cannot
renew acceptance. On a failed publication gate sent here, repair wiring only. A stale reviewed source or
artifact is not repaired by changing a receipt or claiming the old review;
report the defect so production can return to its proper review boundary.
Return concrete installed paths and records, or BLOCKED with the real obstacle.
