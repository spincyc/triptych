# Limitations — what this package does not prove

### 1. The scope is one correction, and the head is not a candidate for acceptance

This head closes one of the V7 review's findings — the namespace at the
request sink — and none of the others. `UNRESOLVED-BLOCKERS.md` lists what
stays open. A review of this package can accept the closure at most; it
cannot accept E1, and the package claims nothing wider.

### 2. The sink proved is the harness's fetch seam

The request journals come from the replay harness's stubbed `fetch` — the
same seam, driven the same way, that the V7 review used to prove the defect.
That is a claim about which addresses the production files hand to the
network boundary; it is not a network capture from a real browser session.
The browser gate did run in real Chromium at both ends, over the built site,
but it asserts the shared shell's generic contract, not this route's request
journal.

### 3. No screenshots, and no route-specific Chromium probe

The stylesheet and the markup are byte-identical to the parent and the
change is semantic; a raster of a valid chapter would be identical at both
ends. `logs/derive-claims.py` counts image pairs from the sealed directory
and reports the count derived rather than an absence described. What replaces
a probe is the head test file replayed against the parent's production files
(`logs/v8-tests-against-parent.log`) and the two request journals side by
side.

### 4. The parent-side battery baselines are inherited, not adjudicated

Full discovery, the make targets and the browser gate fail at the parent and
at the head in the same inherited identities; the package proves the sets
match, not that the sets are acceptable. They belong to their separate
owners.

### 5. The V8 classes' parent decomposition includes an infrastructure fault

The head's test file pins the model by digest, so at the parent it fails the
byte-identity guard as well as the namespace classes. The per-class
decomposition in `DERIVED-CLAIMS.md` is derived from the log rather than
asserted, so the reader can separate the guard's expected failure from the
classes that state the defect.

### 6. Judgements are not derivations

Every figure a machine could derive is derived into `claims.json`. Whether
the namespace boundary is drawn at the right altitude, whether a
wrong-namespace prefix should poison the file's text layer, and whether the
model needs a ceiling are judgements; `REVIEW_REQUEST.md` asks them instead
of asserting them.
