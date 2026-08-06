# Production isolation

- Public `liturgy/day.html` and `liturgy/index.html` are byte-unchanged from the
  integration base and contain no link to either candidate or visual oracle.
- Day and Propers production-reader candidates remain unlinked and retain
  their existing public-alpha publication policy; this integration does not
  change their robots metadata.
- The accepted visual-reset prototype remains byte-unchanged, unlinked, and
  noindex as the comparison oracle.
- `reader-shell.js`, reader state and adapters, assembly, production renderers,
  Ordinary seating, data, calendars, sources, editions, and translations are
  unchanged.
- The bounded Day/Propers JavaScript composition changes retain existing text,
  semantic order, IDs, locations, focus ownership, and winning-render checks.
- No external dependency, font, icon service, CDN, logo, or runtime request was
  added.
- Public navigation and public cutover remain unauthorized.
