# Public Release Boundary

The full Triptych development repository remains private. Public distribution is made from a generated, history-free site artifact, never by changing this repository's visibility or publishing its root.

`public-alpha.json` is the exhaustive publication policy for every discovered source document and installed PDF:

- `hold` means the work must not enter either a public build or a private review preview;
- `review` means the work may enter the clearly marked, no-index private preview, but not a public build; and
- `release` means a work-specific rights record, approval date, and exact approved PDF SHA-256 have been recorded and verified.

The public build copies only rendered HTML, site CSS, license texts, and PDFs marked `release`. It does not copy Markdown, TeX, research records, build intermediates, `.git`, or repository history. The private preview additionally copies `review` PDFs and is marked `noindex, nofollow`; it is for local or access-controlled review only.

Use:

```sh
make check-public-alpha
make public-preview
make verify-public-preview
make public-site
make verify-public-site
```

Generated files live beneath ignored `build/public-alpha/`. A later public repository or Pages deployment must be created only from the verified `site/` artifact. Never publish the `preview/` artifact.
