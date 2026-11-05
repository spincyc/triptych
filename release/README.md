# Public Alpha

Triptych publishes one generated public-alpha artifact. Every publication owns
an independent record under `release/publications/<provider>/<leaf-id>.json`.
The generator discovers those records and their canonical source owners,
deriving eligible reader editions and admitted print selections. Counts are
generated rather than tracked.

An `alpha` record means the current declared publication may be included when
its source integrity, rights and lawful distribution, safety, reproducibility,
mechanical validity, and basic visual usability checks pass. A `hold` record is
excluded. `Published` describes deployment of a verified alpha artifact, not
editorial promotion, completeness, official status, or external approval.

The standing authorization is recorded in `public-alpha.json` and
`rights/public-alpha-2026-07-15.md`. Publication records reference that
authorization without storing PDF hashes. Source identities, reader routes,
the native-print selection inventory, and `SHA256SUMS` are generated during
artifact construction. The manifest records `stored_pdfs: false`. The
historical snapshot hash table in the rights record remains
audit history; ordinary publication changes do not rewrite it. The exact
approved site sources are inventoried only in the `site_sources` object of
`public-alpha.json`; the rights record binds that inventory by one digest,
defined in its site-source section, which `tools/release-bindings refresh`
writes and `status` verifies.

Each publication's own source and research records retain material source,
rights, safety, edition, jurisdiction, currentness, and scope facts. Catalogs
provide terse navigation. Internal release state is not rendered in reader
editions or public-site banners. A work-wide reliance boundary appears once in
the document's terminal qualifications; claim-local limits remain with the
affected claim.

The public build contains reader HTML, browser data, CSS, license texts, and
narrowly scoped generated policy, manifest, and checksum files. Its one source
transport is the admitted editions' exact native TeX render bundles, with
verified engine, package and font assets under their delivery and license
manifests. It excludes other authoring sources, research records, build
intermediates, repository metadata, history, private-preview output and PDFs.

PDF generation is an explicit reader action or a separate selected print
export. The independent Pages `print-compile` gate validates admitted source
bundles and discards its PDFs; it supplies no print-layout review. Historical
PDF links, where offered, use separately verified archive deliveries. See
[`docs/printing.md`](../docs/printing.md) and the native-bundle boundary in
[`guidance/repository.md`](../guidance/repository.md).

Use:

```sh
make check-public-alpha
make prepare-public-alpha
make public-preview
make verify-public-preview
make public-site
make verify-public-site
```

Preparation reports current inputs and hashes but grants no authority. Build
and verification are separate. Verification checks the complete artifact file
set, current rendered pages, local links and fragments, catalog reachability,
checksums, dependency lock, excluded publications, forbidden paths and file
types, and machine-private data.

Only the maintainer may authorize integration, push, or deployment. The Pages
workflow publishes only `build/public-alpha/site`, never the repository root or
private preview.
