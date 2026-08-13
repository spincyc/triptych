# Limitations — what this package does not prove

## Both V4 gaps are closed; these are the new edges

### 1. Screenshots prove rendering, not announcement

53 real PNGs exist. They show the corrected copy in a real browser at real
viewports. They do **not** show what a screen reader says. No AT bus, screen
reader, or assistive-technology client was available or exercised, and a picture
of an `aria-live` region is not evidence that it was announced.

V4's `AT-LIMITATION.md` is **not superseded** by this package. Announcement
remains evidenced structurally, by replayed status writes in the focused suite.

### 2. Print evidence is CSS emulation, not PDF

The `--print` images are `Emulation.setEmulatedMedia` with `media: print`. That
is the browser applying print stylesheets, captured deterministically. It is not
a PDF export and not a physical page. The repository has no deterministic
print-to-PDF harness, and this lane did not invent one.

### 3. Forced-colors evidence is browser emulation

`forced-colors: active` via CDP. It is not Windows High Contrast on real
hardware, and it does not prove system-level colour substitution.

### 4. Text-200% and scale-400% were not captured as images

The shared gate exercises both as assertions across all 19 routes, identically at
base and head. This lane did not duplicate that visually.

### 5. The copy correction is bounded to the fail-closed umbrella

Three strings. Other phrasing on the page that a page-wide neutrality standard
would likely also fail was deliberately left alone — see `REVIEW_REQUEST.md`
question 2. This is a scope decision, disclosed, not an oversight.

### 6. The neutrality regression is a substring blacklist

It forbids five diagnostic phrases in the umbrella. A newly invented
non-neutral formulation would pass it. Disclosed in `REVIEW_REQUEST.md`
question 6.

### 7. The package digest is a transport digest

`SHA256SUMS`-style `sha256sum` of the archive proves the archive received is the
archive sent. It does **not** prove reproducible construction: zip entry
timestamps are local mtimes. `MANIFEST.sha256` is the content proof.

### 8. Inherited state this lane did not repair, and could not

- Four stale release bindings; nothing re-signed.
- The `src/web/data/` test contradiction.
- 226 common-gate failures owned by the shared shell.
- `check-tool-registry`, `check-examples`.
- The branch-topology/records discrepancy described in `REVIEW_REQUEST.md`
  question 5: the V3 review commit is not an ancestor of this branch, so the
  reviewer's own records and reopened deliverable statuses are absent at this
  head.

### 9. What "identical" means here, precisely

The browser-gate claim is literal: every key of the report except `generatedAt`
is deep-equal across 480,881 bytes, including all 226 failure objects. The
full-suite claim is weaker by construction — the head runs **one more test**
than the base, so the runs are not identical; what is identical is the 27-entry
FAIL/ERROR **name set**, compared with `diff(1)`, which produced no output.
No literal baseline identity is claimed for the full suite.
