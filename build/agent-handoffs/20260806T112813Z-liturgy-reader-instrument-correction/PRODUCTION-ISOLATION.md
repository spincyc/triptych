# Production isolation

- Public `src/web/browser/liturgy/day.html` and `index.html` were not modified.
- Accepted `day-reader.html`, `propers-reader.html`, shared `reader-shell.*`,
  state, adapters, seating, production Day/Propers renderers, and liturgical
  data retain the hashes enforced by
  `tools.tests.test_liturgy_reader_visual_reset`.
- All new composition code is limited to `reader-visual-reset.css` and
  `reader-visual-reset.js`; the evidence harness and static tests are the only
  test-layer changes.
- The prototype is unlinked, carries noindex/nofollow/noarchive metadata, and
  makes no external runtime request.
- Deployed CSS and JavaScript SHA-256 values exactly matched the task sources
  after Pages run `31094868150`.
- Public cutover and production-integration execution remain unauthorized.
