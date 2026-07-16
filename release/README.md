# Public Release Boundary

The complete Triptych repository and its reachable rewritten history are authorized for public GitHub visibility. The reader-facing website is still made from a generated, history-free artifact so GitHub Pages exposes the polished landing page and approved library rather than treating the repository root as the website.

`public-alpha.json` is the exhaustive publication policy for every discovered source document and installed PDF:

- `hold` means the work must not enter either a public build or a private review preview;
- `review` means the work may enter the clearly marked, no-index private preview, but not a public build; and
- `release` means a work-specific record, or an exhaustive shared record that names the work, its effective authorization and duration, and the exact approved PDF SHA-256 have been recorded and verified.

The public build copies rendered HTML, site CSS, license texts, PDFs marked `release`, and narrowly scoped generated policy, manifest, and checksum files. It does not copy Markdown, TeX, research records, build intermediates, `.git`, or repository history. The private preview additionally copies `review` PDFs and is marked `noindex, nofollow`; it is for local or access-controlled review only.

The exact 27-PDF reader-site snapshot has a user-attested perpetual authorization recorded at `rights/public-alpha-2026-07-15.md`. It is effective from 15 July 2026, has no expiration date, and permits worldwide public repository visibility and GitHub Pages hosting for that recorded scope. Those 27 manifest entries remain released. The new historical-heresy reference is a twenty-eighth entry and is held pending work-specific rights review; it is not covered by the earlier source or PDF inventory, and pushing it to a public branch would itself be publication. The new section and changed navigation also fall outside the earlier exact site-source hashes, so the public-alpha check intentionally fails closed until a later authorization records the complete revised reader-facing snapshot. The prior record retains the supplemental confirmations and exact inventories described there; it must not be silently expanded or reused for the new work. Its unadvertised condition prohibits a separate project-initiated announcement or promotion but permits ordinary GitHub and search discovery for the authorized snapshot. Once a renewed exact snapshot is recorded, the generator will:

- refuse public checks, builds, or verification before the effective instant or after any approved PDF or reader-facing site source changes;
- bind every copied PDF and the authorization record to an exact SHA-256;
- bind every reader-facing Markdown, layout, and style input to an exact SHA-256 so later edits require renewed authorization;
- produce ordinary indexable public pages while retaining no-index controls for the private preview; and
- create no sitemap, feed, public release attachment, announcement, or promotional metadata.

`release` records snapshot-specific distribution authorization and cleared release gates; it does not raise a work's editorial or ecclesiastical maturity. `hold` keeps the new historical-heresy PDF out of both public and private-preview artifacts. No current publication records independent specialist review or ecclesiastical approval of the Triptych publication as such. The canon-law study remains a source-audited educational work rather than a canonical opinion or legal advice. The postconciliar Order of Mass still lacks exact hands-on formula-level collation against licensed 2008 Latin and 2011 United States altar books. Its PDF and the earlier works' linked research records preserve their recorded limitations. The Mount Carmel guide and companion retain the recorded *Flos Carmeli* witness, attribution, permission, and non-approval limitations. See the rights record and each publication's linked research records for the complete boundaries.

The GitHub Pages workflow builds and verifies `build/public-alpha/site`, uploads only that artifact, and deploys it through the `github-pages` environment. The repository may be public, but Pages must never publish the repository root or `build/public-alpha/preview`. The current perpetual public build needs no cutoff worker or custom response headers. The generator retains stricter no-index and cutoff controls for a future authorization that requires them.

Use:

```sh
make check-public-alpha
make public-preview
make verify-public-preview
make public-site
make verify-public-site
```

Generated files live beneath ignored `build/public-alpha/`. GitHub Pages publishes only the verified `site/` artifact. Never publish the `preview/` artifact. Because the repository itself is public, review publication authority and private-data boundaries before every push; changed PDFs and future publications require their ordinary recorded clearance.
