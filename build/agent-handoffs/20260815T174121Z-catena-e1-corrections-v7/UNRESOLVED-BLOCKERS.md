# Open items this lane did not touch, and who owns each

None of these was worked around, whitelisted, weakened, expect-marked, skipped
or rebased onto a newer base. Each fails identically at the parent and at this
head, and the two full-discovery logs ship so that can be checked rather than
believed.

## 1. Four stale Catena release bindings

`release/public-alpha.json` records a sha256 per site source. This correction
changes `src/web/browser/catena/catena.js` and
`src/web/browser/catena/catena-model.js`, so their recorded digests no longer
match — which is the binding doing its job. `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical to the parent and were already stale at the parent for reasons
of their own.

**Owner: the release owner.** `refresh-release-bindings` and `approve-release`
were not run. An authorization is a statement that somebody reviewed those
bytes, and this lane is not that somebody.

## 2. The `src/web/data/` guard contradiction, and its two Day-reader failures

`DATA-TEST-CONTRADICTION.md`, preserved in full. Two durable records
contradict each other and resolving it means deciding which is wrong.

**Owner: the Day-reader owner, and whoever owns the earlier authorization.**

## 3. The common browser-gate failure population

The gate's failing assertions are deep-equal at parent and head; the
categories and counts are in `DERIVED-CLAIMS.md`, derived from the two gate
reports rather than typed. They are `single-main-element`,
`primary-controls-meet-target-size` and `skip-link-targets-existing-element`,
and they belong to the shared shell and the layout wrapper, not to this route.

**Owner: the shared shell / common gate.**

## 4. `check-tool-registry`

Eight undeclared sibling dependencies between tools. Untouched, red at both
ends.

**Owner: the tool registry's.**

## 5. `check-examples`

Captured tool transcripts that have diverged from what the tools now print.
Untouched, red at both ends.

**Owner: each tool's.**

## 6. Real-device and assistive-technology verification

Nothing in this package proves what a screen reader says. The evidence is DOM
and rendering evidence: `aria-busy`, the live region's text and current
contents, `document.activeElement`, and what was requested. No AT bus was
available.

**Owner: the real-device/AT prerequisite, still open.**

## 7. `src/web/data/bibles.json` arriving unreadable is reported as "lists no translations"

Found by this lane's second adversarial pass, confirmed, and **not fixed,
because the sentence is not this route's to compose.**

`T.loadBibles()` in `src/web/browser/shared/browser-core.js` does
`const bibles = (file && file.bibles) || [];` and answers
`{ok: false}` carrying a message that names the manifest and says it lists no
translations. A 200 carrying
JSON `null`, or a `bibles` that is a record rather than a list, therefore
reaches a reader as a claim about what the manifest LISTS — drawn from a
document nobody could read. It is the same class this whole correction is
about, at the one seam the correction cannot reach.

The route already carries the truthful sentence for the case it CAN see —
`The published editions could not be read.`, for a manifest whose members are
all unreadable — and it cannot reach this one, because `loadBibles` has
already collapsed the two cases into one message before the route sees it.

**Owner: B0 / the shared shell.** The fix is one line in `loadBibles`: tell a
`bibles` that is not a list apart from a list that is empty. This lane stopped
at the seam and documented it rather than reaching across it, which is what
§3 of its brief requires.

## 8. Protected Liturgy, PDFs, B0/shared shell, unrelated corpus surfaces

Untouched. `git diff --stat` over those paths against the parent is empty.

**Owner: each its own.**

---

## And one this lane found, could not reach, and is not claiming

`startFailed()` is the page's terminal transaction for a bootstrap that cannot
be used. The V6 review asked for a regression driving a **pending render**
through it before releasing the parked work.

That sequence is not reachable from a settled route in this harness, and the
reason is a property of the page rather than of the harness:
after `start()` returns, the only caller of `startFailed()` is `render()`'s
guard `!book || !bible || !Number.isFinite(chapter)`, and every control that
can reach `render()` is populated from validated roots — the book select from
`canonRoot`, the chapter select from a book's own chapter count, the edition
select from `bibleRoot` — while the shim's `<select>` refuses a value no
option carries. So none of the three can be made unreadable once the page has
started.

What V7 supplies instead is the same claim through the terminal transaction a
route **can** reach mid-flight: `V7InvalidatedPendingRenderTest` parks a
chapter spine, changes the address to one that cannot be used — which takes
the invalid-address transaction, calls `T.beginRender()`, clears the region
and the tally, keeps focus and speaks once — captures that state whole, and
only then answers the parked spine, once with a payload and once with a
rejection. Nothing of the terminal state moves, and `released` proves the
completion really happened.

**A reviewer should decide** whether that is the claim the review wanted, or
whether reaching `startFailed()` itself requires a harness change this lane
should have made. It is recorded here rather than presented as done.
