# Limitations of this package

Each heading is a full sentence, so a reader who scans only the headings
still reads the limitation. Nothing here is a defect found by review; these
are the boundaries of what this lane did, stated by the lane that did it.

## 1. The read-once contract is a claim about one projection, not about one page render.

`requestSnapshot` reads a request-critical descriptor exactly once per
projection. The page projects one chapter spine **three** times per render —
through `spineUnreadable`, through the tally, and again through
`renderChain` — so a whole render asks each fragment's request-critical
descriptor three times, once per projection. That is measured, not inferred,
and it is pinned at exactly three so that a change to the projection count
fails loudly rather than silently changing which value a drifting descriptor
lands on.

No projection ever holds two values, which is the property the review
required. But a reviewer who reads "read once" as "asked once per render"
will find three, and should read `REVIEW_REQUEST.md` §5, which asks whether
collapsing the three projections is worth a later lane.

## 2. A polluted `Object.prototype` closes every row on the page, not one.

This is the deliberate cost of the contamination rule, and it is wider than
V11's, which asked only about the claim's own three members. With any of the
five request-critical names reachable on `Object.prototype`, every fragment
of every chapter resolves to the conservative malformed/unestablished state.
The reasoning is in `CLAIM-CLOSURE.md` §3 and the question is put to the
reviewer in `REVIEW_REQUEST.md` §2. The alternative — contaminating only the
record whose polluted read was consumed — was considered and rejected, not
overlooked.

## 3. The authoritative attempt's terminal row is written before the archive exists.

Nothing may write inside the package directory after the manifest is taken,
so the sealing attempt's terminal `authoritative` row is written immediately
before it — at which instant P7 (archive) and P8 (final verification) have
not run. The row therefore claims that the package **directory** is sealed,
which is true when it is written; the ZIP's identity and the P8 verdict live
in the sidecar and the outer invocation log, and the coherence check binds
the three together. The backstop is that a P7 or P8 failure writes a discard
marker into the directory and the coherence check refuses any package
carrying one. `REVIEW_REQUEST.md` §4 asks whether that is acceptable.

## 4. `id` is snapshotted but is not a contamination name.

Two lists, and they are not the same list. The names whose **value** is read
through the snapshot are `text_prefix` on the spine and, on the fragment,
the carried `text_path` and `id`. The names whose **presence above a record**
contaminates it are `text_prefix`, `text_path`, `text_refused`, `stated` and
`trail`. `id` is in the first and not the second: it is read through the
snapshot because it chooses the composed address, but adding it to the
contamination set would reopen a disposition the V11 review passed. Adding it would reopen a
disposition the V11 review passed. The asymmetry is pinned rather than
argued: a fragment whose only `id` is `Object.prototype`'s composes no
address at all, and a fragment carrying its own `id` behaves exactly as it
does in an unpolluted realm.

## 5. The snapshot covers request-critical state and nothing wider.

It was deliberately not broadened into all Catena semantics. `chapterVoices`
and `absenceRows` still rescan raw sources; the wide fragment and edition
contracts are still validated field by field; `spineUnreadable` still reads
`fragments`, `sources`, `refusals` and `unfetched` by plain lookup, because
readability is not a request-critical decision and the V5, V6 and V11
reviews each settled that shape. Those are recorded open in
`UNRESOLVED-BLOCKERS.md`.

## 6. `src/web/browser/catena/catena.js` is unchanged, so the page still reads three fields off the row inside its toggle handler.

`fragment.text_refused`, `fragment.text_note` and `fragment.text_path` are
three separate property lookups made inside an event handler that fires
arbitrarily long after the row was projected. They are reads of a **trusted
projection** — every member an own data property, which V11 proved and the
review passed — not reads of a raw record, so the snapshot boundary did not
need to cross into rendering. The refusal is still consumed before the
request sink and that ordering is still pinned. A reviewer who wants the
boundary carried into the page should say so; the page has 20 gzipped bytes
of its ceiling left, so it would cost a budget conversation.

## 7. The screenshots show a fixture corpus, not the tracked corpus.

The three inputs this lane closes cannot occur in the tracked data — a
prototype and a drifting descriptor are properties of a JavaScript object,
not of a JSON document — so the adversarial captures are driven from a
scratchpad fixture corpus, with every fabricated record stamped
`ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA` and visible as such in the
image. No file under `src/web/data/` was read, written or altered to produce
them. Each capture opened the fragment disclosure and read the rendered
sentence back out of the DOM before the shutter, and the text read is
recorded per image, so no image can claim a state it did not show.

## 8. Headless Chromium is not a device and is not an assistive technology.

The browser gate and the captures both run headless Chromium. No real-device
and no assistive-technology evidence exists for this route; that is
separately owned and remains open.

## 9. The batteries measure two endpoints, and the failure sets are compared rather than the exit codes.

`make -k check`, full discovery, the browser gate and the release-bindings
check are red at this head and were red at the parent, for reasons no part of
this correction causes. Every one of them is measured at **both** endpoints
in this package and compared as a failure set, because an exit code alone
cannot distinguish an inherited failure from a caused one. Where a figure is
quoted, the log it came from is named.

## 10. The assembly pipeline is not under version control in this workspace.

The tools under `logs/` are carried forward from the previous sealed package,
with this lane's additions beside them, and they run from a trusted directory
outside both checkouts. There is
therefore no commit that pins them; P8 records each tool's trusted and
shipped SHA-256 instead and fails hard on divergence. This limitation is
inherited from the previous lane and is unchanged by this one.

## 11. Four battery runs were set aside before the ones that shipped.

Two wrote a step transcript that was empty — the browser gate's, which is the
same finding the V11 review made against V11, and the restore step's, whose
emptiness meant success. One measured an implementation head this package
does not name, because its own figures corrected the durable record and that
moved the head. One measured a checkout left dirty by the previous run's own
substitution step, and reported the head's counts as the parent's. All four
were caught by a gate rather than by inspection, all four were set aside
rather than deleted, their ledgers and log roots are retained outside this
package, none produced a figure used anywhere in it, and `PROVENANCE.md` §7
states every cause and the three tool changes they forced.

## 12. This lane did not review itself.

No disposition is recorded here, no separately owned prerequisite is marked
complete, and nothing in this package is an acceptance. The sole next action
is a fresh independent review of the exact head this package names.
