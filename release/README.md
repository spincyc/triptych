# Public Release Boundary

The complete Triptych repository and its reachable rewritten history are authorized for public GitHub visibility. The reader-facing website is still made from a generated, history-free artifact so GitHub Pages exposes the polished landing page and approved library rather than treating the repository root as the website.

`public-alpha.json` is the exhaustive publication policy for every discovered source document and installed PDF:

- `hold` means the work must not enter either a public build or a private review preview;
- `review` means the work may enter the clearly marked, no-index private preview, but not a public build; and
- `release` means a work-specific record, or an exhaustive shared record that names the work, its effective authorization and duration, and the exact approved PDF SHA-256 have been recorded and verified.

The public build copies rendered HTML, site CSS, license texts, PDFs marked `release`, and narrowly scoped generated policy, manifest, and checksum files. It does not copy Markdown, TeX, research records, build intermediates, `.git`, or repository history. The private preview additionally copies `review` PDFs and is marked `noindex, nofollow`; it is for local or access-controlled review only.

The current repository and exact 27-PDF snapshot have a user-attested perpetual authorization recorded at `rights/public-alpha-2026-07-15.md`. It is effective from 15 July 2026, has no expiration date, and permits worldwide public repository visibility and GitHub Pages hosting. All 27 manifest entries are released. The record retains the earlier supplemental confirmations for the Eighth Sunday after Pentecost and the revised 1962 Ordinary, then records the current-batch clearance for six standardized 1962 proper PDFs, both revised Mount Carmel PDFs, the new clerical-celibacy canon-law study, the new postconciliar Order of Mass exposition, and all changed reader-facing site sources. The exact inventories bind every approved PDF and site input. Its unadvertised condition prohibits a separate project-initiated announcement or promotion but permits ordinary GitHub and search discovery. The generator therefore:

- refuses public checks, builds, or verification before the effective instant or after any approved PDF or reader-facing site source changes;
- binds every copied PDF and the authorization record to an exact SHA-256;
- binds every reader-facing Markdown, layout, and style input to an exact SHA-256 so later edits require renewed authorization;
- produces ordinary indexable public pages while retaining no-index controls for the private preview; and
- creates no sitemap, feed, public release attachment, announcement, or promotional metadata.

`release` records snapshot-specific distribution authorization and cleared release gates; it does not raise a work's editorial or ecclesiastical maturity. No current publication records independent specialist review or ecclesiastical approval of the Triptych publication as such. The canon-law study remains a source-audited educational work rather than a canonical opinion or legal advice. The postconciliar Order of Mass still lacks exact hands-on formula-level collation against licensed 2008 Latin and 2011 United States altar books. Its PDF and both new works' linked research records preserve their accurate pre-clearance hold statements; the later rights record supersedes those statements only as to distribution status for the exact snapshots. The Mount Carmel guide and companion retain the recorded *Flos Carmeli* witness, attribution, permission, and non-approval limitations. See the rights record and each publication's linked research records for the complete boundaries.

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
