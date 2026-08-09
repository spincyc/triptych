# The didach.ai domain migration

## Status and scope

The governing product decision is made: the future canonical public root is
`https://didach.ai/`. GitHub Pages remains the host, the repository keeps its
name and its `https://spincyc.github.io/triptych/` project URL until cutover,
and nothing in this document authorizes the cutover itself — DNS, the Pages
custom-domain setting, and the deploy that follows them are a separate,
explicitly authorized operation. This document owns the technical architecture
of the move: what was audited, what the canonical-URL model is, what changed
ahead of time, the exact cutover procedure, and how to roll it back.

Visible identity — wordmark, naming hierarchy, favicon, social-card design,
whether readers see "Triptych", "Didach", or both — belongs to the Codex
`ux/didach-identity` lane, which did not exist when this was written. Nothing
here decides identity; the seams below are where its decisions land.

## The audit, and what it found

A repository-wide audit (2026-08-08, base `fc3092de9`) classified every
occurrence of the old host, the `/triptych/` subpath, and absolute self-URLs.
The finding is unusually clean: **the corpus was written host-agnostically,
and the deployment origin exists in exactly two tracked places.**

| Where | What | Disposition |
| --- | --- | --- |
| `tools/public-alpha` (`SITE_SCHEME_HOST`/`SITE_BASE_PATH`/`SITE_ORIGIN`) | the single canonical-origin definition; feeds `og:url`, `og:image`, `twitter:image`, and one act-history apparatus URL | **the migration seam** — see the model below |
| `tools/tests/liturgy_reader_visual_reset_browser.mjs` | live deployed-baseline URL for visual captures | now overridable via `TRIPTYCH_DEPLOYED_BASE`; default follows the deployed site |
| `README.md`, `library/**`, generated pages, browser runtime | all links document-relative; `verify_links` rejects root-relative links as "not portable" | no change needed, at cutover or ever |
| `ABOUT.md`, `CONTRIBUTING.md`, `docs/**` | `github.com/spincyc/triptych` repository links | unaffected — the repository is not renamed |
| `src/sources/**` (3,207 URLs), `src/**/*.tex` (1,799 files), all 192 installed PDFs | third-party acquisition evidence and citations; zero self-URLs, verified by full text and metadata extraction | **never rewritten**; corpus evidence is not site identity |
| tracked `build/agent-handoffs/**`, `build/agent-continuity/**` | ~4,400 old-host occurrences inside frozen handoff evidence | historical record; byte-intact forever |
| `guidance/act-histories.md` §"the origin is not typed here" | the written contract that consumers import the origin from `tools/public-alpha` | still true; keep it true |

Two hazards recorded for any later renaming work, which is out of scope here:
the string `didach` collides with *Didache* — the first-century text — in 44
tracked files, so no global substitution is ever safe; and the visible name
"Triptych" is baked into PDF colophons and `Creator:` metadata, which is the
identity lane's decision, not a URL question.

## The canonical URL model

Two facts, kept separate, joined once, in `tools/public-alpha`:

```python
SITE_SCHEME_HOST = "https://spincyc.github.io"   # where the site is reached
SITE_BASE_PATH = "/triptych"                     # where the artifact is mounted
SITE_ORIGIN = SITE_SCHEME_HOST + SITE_BASE_PATH  # what every consumer reads
```

- **Canonical origin** is a property of the *release*: it names where the
  published artifact is reached and appears only in link-preview metadata and
  in the act-history apparatus, both of which need absolute URLs. `tools/
  act-history` and `tools/release-bindings` import the constant; nothing
  restates it. A preview or unadvertised build carries no absolute URL at all,
  which is why a localhost preview can never leak into canonical identity.
- **Deployment base path** is a property of the *mount*: `/triptych` under the
  project-site URL, `` "" `` under `didach.ai`. It appears in generated output
  in exactly one place — the root-served error page (below). Everything else
  is document-relative, so the same artifact works at any mount, which the
  dual-mount browser gate proves on every run.
- The cutover is therefore a **two-value edit** to the block above
  (`"https://didach.ai"` and `""`), plus the release-binding re-pin that any
  edit to `tools/public-alpha` forces. That forced re-pin is deliberate: the
  origin change cannot land silently.

`AGENTS.md` forbids machine-private hostnames in tracked sources; the
canonical public origin is not that. It is release metadata, tracked in one
place, the same way `SITE_NAME` is.

### The error page is the one base-anchored surface

GitHub Pages serves `404.html` for any missing route while the browser keeps
the missed URL as the document base, so relative links in that page resolve
against whatever directory the reader mistyped. The 404 page therefore links
through `SITE_BASE_PATH` (`page_link` in `tools/public-alpha`), and
`verify_links` enforces both halves: root-relative links remain a hard error
in every ordinary page, and the error page must be base-anchored — a
document-relative link there is now also an error. `ROOT_SERVED_ERROR_PAGES`
names the set. Before this change, deep-path 404s loaded no stylesheet on the
current site; the fix predates the migration on purpose, so cutover changes
the anchor value rather than introducing the mechanism.

### The depth invariant

Every served browser page sits exactly one directory below the site root, so
the runtime's relative resolutions — `../browse` for data,
`../shared/browser-core.js` for the core, `../<entrance>/` for
cross-instrument links — mean the same thing at every mount.
`src/web/browser/shared/browser-core.js` states it; the non-recursive glob in
`web_browser_pages()` makes deeper pages impossible today;
`tools/tests/test_didach_domain.py` holds the rule if either ever changes.

## Ownership map

| Concern | Owner |
| --- | --- |
| canonical origin, base path, error-page anchoring, portability verify | `tools/public-alpha` |
| origin consumers | `tools/act-history`, `tools/release-bindings` (import, never restate) |
| link-preview correctness checks | `verify_link_previews` in `tools/public-alpha`; `tools/tests/test_public_alpha.py` |
| migration contracts (origin composition, link portability, depth invariant) | `tools/tests/test_didach_domain.py` |
| dual-mount browser proof | `tools/tests/public_site_mount_browser.mjs` + `tools/tests/harness/static-site-server.mjs`, run by `make check-site-mounts` |
| deployed visual baselines | `tools/tests/liturgy_reader_visual_reset_browser.mjs` (`TRIPTYCH_DEPLOYED_BASE`) |
| Pages workflow | `.github/workflows/pages.yml` (origin-free; URL comes from the deploy action's output) |

## GitHub Pages facts the plan rests on

Verified against current GitHub documentation and, where the docs are silent,
empirically against a live custom-domain project site (2026-08-09; doc pages:
About custom domains, Managing a custom domain, Verifying a custom domain,
Troubleshooting, Securing with HTTPS, Custom workflows).

- **CNAME files are irrelevant to this repository.** For custom-workflow
  (Actions) deployments GitHub states: "If you are publishing from a custom
  GitHub Actions workflow, no `CNAME` file is created, and any existing
  `CNAME` file is ignored and is not required." The custom domain lives in
  repository **Settings → Pages** alone. The artifact's exhaustive file-set
  verification therefore rightly continues to reject a stray `CNAME`.
- **Old URLs redirect well.** With a custom domain configured on a project
  site, `https://spincyc.github.io/triptych/<path>?<query>` answers **301**
  to `https://didach.ai/<path>?<query>` — repository segment stripped, path
  and query preserved; fragments survive by standard client behavior (a
  redirect without a fragment keeps the original's). The docs do not promise
  this; it is observed behavior, persists while the domain stays configured,
  and stops if the domain is removed. No custom redirect machinery is needed
  or possible on Pages.
- **The subpath disappears at cutover.** The site serves at the domain root;
  that is exactly the deployment shape the dual-mount gate already exercises.
- **HTTPS** is provisioned from Let's Encrypt after the domain saves and the
  DNS check passes — up to an hour for the certificate, up to 24 h before
  "Enforce HTTPS" unlocks. If CAA records exist, one must allow
  `letsencrypt.org`. Stray `@`-host A/AAAA/ALIAS/ANAME records break
  issuance. Do not proxy the DNS (no Cloudflare orange-cloud): proxying in
  front of Enforce HTTPS is the classic redirect-loop cause.
- **Domain verification is recommended, not required**, and prevents takeover
  while the domain is unlinked: TXT record at
  `_github-pages-challenge-spincyc.didach.ai` with the token from profile
  Settings → Pages → Add a domain. Verifying the apex covers `www`. Keep the
  record permanently. Do not create wildcard DNS records.
- **A user site's custom domain would cascade over project sites; a project
  site's does not.** Setting didach.ai on this repository affects no other
  `spincyc` project site.

## robots, sitemap, and canonical metadata

- `robots.txt` (`Allow: /`) is generated at the artifact root. Today that is
  `/triptych/robots.txt`, which crawlers never read — robots.txt is honored
  only at an origin root — so the file is currently inert and becomes live
  for the first time at `didach.ai/robots.txt`. Its content is correct for
  that moment. **Caution recorded:** the preview variant writes
  `Disallow: /`; a preview artifact must never be deployed to an origin root,
  and the artifact verifier's preview/public separation is what prevents it.
- There is deliberately **no sitemap** and **no `<link rel="canonical">`**;
  two browser tests assert the canonical link's absence on retained noindex
  routes. Introducing them is a product decision for the corpus-redesign
  lanes, not a migration prerequisite; if introduced, both must derive from
  `SITE_ORIGIN` so the cutover stays a two-value edit.
- Per-page `og:url`/`og:image`/`twitter:image` follow `SITE_ORIGIN`
  automatically and are re-verified against it on every build.

## Test strategy

- `tools/tests/test_didach_domain.py` (in `make check-tests`): origin
  composition, `page_link`/`relative_link` shapes, both halves of the
  `verify_links` portability contract, and the depth invariant.
- `make check-site-mounts` (browser-optional, skips with reason): serves the
  built artifact at `/` and at `/triptych` and proves, per mount: every
  entrance cold-loads with clean console/network, data loads through the
  runtime's own relative `../browse` (no `?data=` override), hash deep links
  survive, every request stays inside the mount (catches `//`, duplicated
  segments, and origin leaks), assets and a PDF answer, and a missed deep URL
  serves the base-anchored 404 whose links resolve at the built base path.
  This preserves the subpath regression coverage the project-site era
  provided, after the canonical site moves to `/`.
- The pre-existing gates continue to bind: `verify_links` (no root-relative
  links outside the error page), the exhaustive artifact file-set, and the
  byte-exact rendered-page comparison between build and verify.

## Migration stages

1. **Done ahead of cutover** (this lane, branch `impl/didach-domain`): the
   origin/base split, the base-anchored error page and its verify contract,
   the dual-mount gate, the deployed-baseline override, this document.
2. **Awaiting Codex:** the `ux/didach-identity` decisions — visible naming,
   icon, social card. Technical constraints for that lane: the icon is
   `release/public-alpha/assets/icon.png` (referenced 180×180), the social
   card is `release/public-alpha/assets/social-card.png` (og:image, absolute,
   ≥ 900 px wide, no text per TN3156), `SITE_NAME` sits beside `SITE_ORIGIN`,
   and all four are release-bound inputs whose change forces a re-pin.
3. **Cutover** (separately authorized): below.
4. **After cutover:** the follow-ups listed at the end.

## Cutover checklist

Preconditions, all provable locally:

- [ ] `make check-deployment-sources`, `make public-site`,
      `tools/tpt public-alpha verify --deployment-target github-pages` green.
- [ ] `make check-site-mounts` green at both mounts.
- [ ] `python -m unittest tools.tests.test_didach_domain` green.
- [ ] DNS records created and propagated (verify with
      `dig didach.ai +noall +answer -t A` and `dig www.didach.ai +noall +answer`):

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
| CNAME | `www` | `spincyc.github.io` |
| TXT | `_github-pages-challenge-spincyc` | token from the verification UI |

  No other `@`-host address records; CAA (if any) allows `letsencrypt.org`;
  records DNS-only, never proxied.
- [ ] Domain verified in profile Settings → Pages (recommended before, and
      the TXT record stays forever).

The cut, in order — each step reversible before the next:

1. Edit `tools/public-alpha`: `SITE_SCHEME_HOST = "https://didach.ai"`,
   `SITE_BASE_PATH = ""`. Run
   `make refresh-release-bindings ONLY="tools/public-alpha"`, rebuild,
   re-verify, rerun `make check-site-mounts` — at the root mount the 404
   assets now resolve, which is the built-for-root proof.
2. Commit and merge to `main` under the ordinary integration authority (this
   is a deploy-affecting change: the push is the deployment).
3. Repository **Settings → Pages → Custom domain**: enter `didach.ai` (the
   apex — GitHub then redirects `www` to it), Save. Do not add a CNAME file.
4. Wait for the DNS check and the Let's Encrypt certificate (minutes to
   ~1 h), then enable **Enforce HTTPS** (may take up to 24 h to unlock).

Post-cutover verification, immediately:

- `https://didach.ai/` serves the home page over HTTPS; `http://` redirects.
- `https://www.didach.ai/anything` redirects to the apex.
- `https://spincyc.github.io/triptych/liturgy/day.html#date=…` → 301 →
  `https://didach.ai/liturgy/day.html` with the fragment surviving.
- A deep PDF URL redirects and serves.
- Catena → Sources and liturgy deep links work; browser console and network
  panels clean on the entrances; `og:url` on any page names `didach.ai`;
  `didach.ai/robots.txt` answers `Allow: /`.
- A deliberately missing URL serves the styled 404.
- `TRIPTYCH_DEPLOYED_BASE=https://didach.ai/liturgy/` capture run succeeds.

## Rollback

Settings → Pages → **Remove** next to the custom domain restores serving at
`spincyc.github.io/triptych/` immediately; the github.io→didach.ai redirects
stop. Then revert the two-value edit (or merge the revert commit), re-pin,
push — the artifact is again built for the subpath. Leave the verification
TXT record in place: it is what prevents another account from claiming the
domain on Pages while it is unlinked. The DNS address records may stay
(didach.ai then serves GitHub's 404) or be repointed; neither affects the
github.io site. A re-cutover restarts certificate provisioning from scratch.

## Risk register

| Risk | Standing |
| --- | --- |
| Root-relative link regression breaks one mount | `verify_links` hard-fails it; dual-mount gate double-checks in a real browser |
| A page lands deeper than one directory and `../browse` breaks | depth-invariant test; non-recursive glob makes it structurally impossible today |
| Origin restated somewhere new and forgotten at cutover | import-the-owner convention (`act-histories.md` contract); audit found no third copy; `test_didach_domain` pins composition |
| 404 anchored to the wrong base after cutover | mount gate asserts anchor equals the built base path and resolves at the deployed combination |
| Preview `Disallow: /` robots reaches the live root | preview/public artifact separation in `public-alpha` verify |
| HTTPS stalls at cutover | known delays documented above; remove/re-add restarts provisioning; rollback is one setting |
| Redirect loop via DNS proxying | records are DNS-only by checklist |
| Old links die if the domain is ever unlinked | redirects live only while the domain is configured — treat removal as a breaking event; verification TXT prevents takeover |
| In-flight corpus-browser branches assert "no CNAME/sitemap/canonical mechanism exists" | true when written, superseded by this document; reconcile their guidance when they land |

## Unresolved questions

- Whether didach.ai should gain a sitemap and `<link rel="canonical">` once
  it is the root — a discovery/product decision for the corpus-redesign
  lanes; both must derive from `SITE_ORIGIN` if adopted.
- Whether the four liturgy browser harnesses should adopt the shared
  `tools/tests/harness/static-site-server.mjs` and a parameterized mount —
  recommended, but they are gates of the in-progress liturgy lane and were
  deliberately not entered here beyond the one-line deployed-base override.
- The `ux/didach-identity` decisions themselves.

## After cutover

- Update this document's status line and the register entry.
- Reconcile the corpus-browser guidance statements listed in the risk table.
- Consider retiring the `/triptych` leg of `check-site-mounts` only if the
  project-site URL is ever formally abandoned; until then the redirect keeps
  old links alive and the subpath coverage keeps them honest.
