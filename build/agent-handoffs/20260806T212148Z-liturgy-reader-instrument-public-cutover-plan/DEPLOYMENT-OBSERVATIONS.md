# Deployment and static-publication observations

- GitHub Pages builds a static artifact through `.github/workflows/pages.yml`.
- `tools/public-alpha` renders every top-level liturgy HTML page and copies the
  top-level CSS/JavaScript assets; there is no hidden route alias.
- No service worker, Cache API, webmanifest, sitemap, rewrite layer, or runtime
  external dependency was found.
- All four route entry points share `src/web/browser/liturgy/`, so the selected
  same-path mechanism preserves relative CSS/JS and `../browse` data bases.
- Deployed unversioned HTML/CSS/JavaScript has been observed with
  `Cache-Control: max-age=600`; later forward and rollback verification must be
  mixed-cache compatible, cache-bypassed first, and repeated after 600 seconds.
- `/liturgy/` and `/liturgy/index.html` are the same static bytes, not a server
  redirect. The explicit external contract remains `/liturgy/index.html`.
- Latest successful planning boundary: Pages run `31127811306` at
  `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`.
- Accepted integrated product deployment: Pages run `31125898045` at
  `5444d89fc9b379a1babef5b2220323fe1508b2b3`.
- No deployment result is claimed for planning-only commits whose workflow run
  had not materialized in the Actions API at the recorded query.
