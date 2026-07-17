# Public Release Boundary

The current release manifest contains 48 publications: all 48 exact PDF
snapshots are marked `release`, with none in `review` or on `hold`. The later
16 July 2026 supplemental authorization in
`rights/public-alpha-2026-07-15.md` binds all 48 release PDFs and all 17
then-recorded reader-facing site sources to their exact post-build hashes. The
release gate now also treats the generator, its dependency lock, and both
copied license texts as artifact-affecting inputs. Those four exact bindings
are not added to the historical authorization by this infrastructure change;
public check, build, verification, and deployment therefore fail closed until
a separately reviewed authorization records the complete current inventory.
The earlier perpetual, worldwide, and no-project-initiated-promotion conditions
remain in force for the scope that record actually identifies.

`public-alpha.json` is the exhaustive publication policy for every discovered source document and installed PDF:

- `hold` means the work must not enter either a public build or a private review preview;
- `review` means the work may enter the clearly marked, no-index private preview, but not a public build; and
- `release` means a work-specific record, or an exhaustive shared record that names the work, its effective authorization and duration, and the exact approved PDF SHA-256 have been recorded and verified.

The public build copies rendered HTML, site CSS, license texts, PDFs marked
`release`, and narrowly scoped generated policy, manifest, and checksum files.
It does not copy Markdown, TeX, research records, build intermediates, `.git`,
or repository history. The private preview additionally copies `review` PDFs
and is marked `noindex, nofollow`; it is for local or access-controlled review
only.

The exact La Salette PDF directly analyzes and paraphrases the secret addressed
by the Holy Office decree published at *AAS* 7 (1915) 594. The present force of
that decree's standalone non-penal publication command remains unresolved. On
16 July 2026 the user's explicit direction placed those exact bytes within the
existing user-attested release authority. The project has not independently
verified the represented grantor, authority, or delegation. This
exact-snapshot distribution decision preserves the unresolved juridic question
and is not an ecclesiastical interpretation, dispensation, canonical opinion,
imprimatur, nihil obstat, or approval of the secret or this publication. It
does not supply independent rights, canonical, specialist, liturgical, or
ecclesiastical review. Apparition and cult approvals remain object-limited and
do not approve this publication. Both public-alpha artifacts include this PDF
with the other 47 releases.

For every fully authorized snapshot the generator will:

- refuse public checks, builds, or verification before the effective instant or after any approved PDF or artifact-affecting repository input changes;
- bind every copied PDF and the authorization record to an exact SHA-256;
- bind every reader-facing Markdown, layout, style, copied license text, generator, and dependency-lock input to an exact SHA-256 so later edits require renewed authorization;
- require the installed Markdown renderer version to match the exact version in the bound dependency lock before rendering;
- produce ordinary indexable public pages while retaining no-index controls for the private preview; and
- create no sitemap, feed, public release attachment, announcement, or promotional metadata.

`release` records snapshot-specific distribution authorization and cleared
release gates; it does not raise a work's editorial or ecclesiastical maturity.
No current publication records independent specialist review, an imprimatur,
a nihil obstat, or ecclesiastical approval of the Triptych publication as such.
The snapshot decision clears distribution gates without supplying missing
source collation, independent rights analysis, specialist review, or
ecclesiastical approval. Both canon-law studies remain source-audited
educational works, not canonical opinions or legal advice: the
clerical-discipline study still awaits independent canonical and ecclesiastical
review, and the natural-law study still awaits its disclosed cross-disciplinary
specialist and ecclesiastical review. The virtues reference is internally
source-audited but is not a critical edition; manuscript collation and
comprehensive source-language lexical review have not occurred, and independent
Aristotelian, patristic, Thomistic, moral-theological, pastoral, and clinical
review remain outstanding. The eight postconciliar
proper guides are working exact-snapshot releases under the express exception
recorded in the rights supplement: complete English-oration collation against
an identified U.S. altar-book printing and independent liturgical, biblical,
theological, and historical review remain outstanding. The postconciliar Order
of Mass likewise still lacks exact hands-on formula-level collation against
licensed 2008 Latin and 2011 United States altar books. None of those records
may imply the missing collation or review. The Mount Carmel guide and companion
retain their recorded *Flos Carmeli* witness, attribution, permission, and
non-approval limitations. See the rights record and each publication's linked
research records for the complete boundaries.

The GitHub Pages workflow can build and verify `build/public-alpha/site` and
would upload only that artifact through the `github-pages` environment. Pages
must never publish the repository root or `build/public-alpha/preview`. This
record documents ordinary repository and Pages publication subject to the
no-project-initiated-promotion condition; it does not itself authorize a worker
to perform a push or deployment, which remain separate operations.

Use:

```sh
make check-public-alpha
make prepare-public-alpha > /tmp/public-alpha-candidate.json
make public-preview
make verify-public-preview
make public-site
make verify-public-site
python scripts/public-alpha verify --deployment-target github-pages
```

`prepare-public-alpha` is read-only and deliberately works when old snapshot
hashes are stale or the old source-binding list lacks newly recognized inputs.
It validates the exhaustive publication and current artifact-input scope, then
reports the current 48 PDF hashes and all current Markdown, layout, style,
license, generator, and dependency-lock hashes as a deterministic candidate
inventory. The inventory explicitly confers no approval, changes no manifest
or rights record, and cannot replace the separate review and recorded
authorization required for new snapshots.

The build and verify commands remain distinct gates. A build reports that its
artifact is unverified; run the matching verify command as a later independent
step before any publication operation. Deployment verification must also name
the intended host profile. GitHub Pages verification rejects temporary or
unadvertised artifacts because static Pages hosting cannot execute the required
request-time expiration worker or apply the required headers to every PDF.

Generated files live beneath ignored `build/public-alpha/`. GitHub Pages may
publish only the verified `site/` artifact, never the `preview/` artifact.
Changed PDFs, changed artifact-affecting inputs, and future publications
require renewed exact-snapshot authorization.
