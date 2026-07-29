# Public Alpha

Triptych publishes one generated public-alpha artifact. Every publication owns
an independent record under `release/publications/<provider>/<leaf-id>.json`.
The generator discovers those records and the source and installed PDF trees;
counts are generated rather than tracked.

An `alpha` record means the current installed publication may be included when
its source integrity, rights and lawful distribution, safety, reproducibility,
mechanical validity, and basic visual usability checks pass. A `hold` record is
excluded. `Published` describes deployment of a verified alpha artifact, not
editorial promotion, completeness, official status, or external approval.

The standing authorization is recorded in `public-alpha.json` and
`rights/public-alpha-2026-07-15.md`. Publication records reference that
authorization without storing PDF hashes. Current PDF hashes, the aggregate
publication inventory, and `SHA256SUMS` are generated during artifact
construction. Historical snapshot and site-source hash tables in the rights
record remain audit history; ordinary publication changes do not rewrite them.

Each publication's own source and research records retain material source,
rights, safety, edition, jurisdiction, currentness, and scope facts. Catalogs
provide terse navigation. Internal release state is not rendered in reader
editions or public-site banners. A work-wide reliance boundary appears once in
the document's terminal qualifications; claim-local limits remain with the
affected claim.

The public build contains rendered HTML, CSS, license texts, alpha PDFs,
eligible web editions, and narrowly scoped generated policy, manifest, and
checksum files. It excludes authoring sources, research records, build
intermediates, repository metadata, history, and private-preview output.

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
