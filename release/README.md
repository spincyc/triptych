# Public Release Boundary

The full Triptych development repository remains private. Public distribution is made from a generated, history-free site artifact, never by changing this repository's visibility or publishing its root.

`public-alpha.json` is the exhaustive publication policy for every discovered source document and installed PDF:

- `hold` means the work must not enter either a public build or a private review preview;
- `review` means the work may enter the clearly marked, no-index private preview, but not a public build; and
- `release` means a work-specific record, or an exhaustive shared record that names the work, its effective authorization and duration, and the exact approved PDF SHA-256 have been recorded and verified.

The public build copies rendered HTML, site CSS, license texts, PDFs marked `release`, and narrowly scoped generated policy, manifest, and checksum files. It does not copy Markdown, TeX, research records, build intermediates, `.git`, or repository history. The private preview additionally copies `review` PDFs and is marked `noindex, nofollow`; it is for local or access-controlled review only.

The current 24-PDF snapshot has a user-attested perpetual authorization recorded at `rights/public-alpha-2026-07-15.md`. It is effective from 15 July 2026, has no expiration date, and permits worldwide public access only under an unadvertised-hosting condition. The generator therefore:

- refuses public checks, builds, or verification before the effective instant or after any approved PDF or reader-facing site source changes;
- binds every copied PDF and the authorization record to an exact SHA-256;
- binds every reader-facing Markdown, layout, and style input to an exact SHA-256 so later edits require renewed authorization;
- emits `noindex`, `nofollow`, `noarchive`, `nosnippet`, and `noimageindex` directives;
- emits `_headers` so a compatible static host applies the directives to direct PDF responses as well as HTML; and
- creates no sitemap, feed, release attachment, announcement, or promotional metadata.

Search directives are advisory, not access control. Deploy the artifact to Cloudflare Pages or an equivalent static host that honors the generated `_headers` rules for every HTML and PDF response, and verify the live headers before sharing the direct URL. A host that does not apply response headers to PDFs is not sufficient for the unadvertised condition. The generator retains cutoff-worker support for a future time-limited authorization, but the current perpetual release does not emit or require a worker. GitHub Pages is therefore not the publication target for this release.

Use:

```sh
make check-public-alpha
make public-preview
make verify-public-preview
make public-site
make verify-public-site
```

Generated files live beneath ignored `build/public-alpha/`. A later public repository or Pages deployment must be created only from the verified `site/` artifact. Never publish the `preview/` artifact.
