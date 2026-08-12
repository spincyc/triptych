# Unrecognized ("stranger") hash keys — corrected statement

This is an **evidence correction**, not a new URL contract. No implementation
was changed to make the earlier prose true, and no URL behaviour changed in V3.

## 1. The V2 statement this record corrects

`20260811T212656Z-catena-e1-corrections-v2/HANDOFF.md`, §7, lines 137–142:

    - **URL grammar, failing closed** (finding 5). The raw multimap is validated, so
      a recognized key cited twice is refused even when the two citations agree,
      while a stranger's key is neither honoured nor disturbed; …

The load-bearing phrase is "**a stranger's key is neither honoured nor
disturbed**", stated without qualification as a summary of corrected route
behaviour. It is true of the *validator* and false of the *route*.

The same package already contradicted itself: its own `LIMITATIONS.md` §7a and
`REVIEW_REQUEST.md` blocker 3 both disclose that partial-address completion
discards stranger keys. The independent review recorded that conflict
(finding 11) and required the handoff to "state precisely that stranger keys
survive already-complete valid addresses but are discarded when partial-address
completion rewrites from recognized keys."

The sealed V2 package is unchanged. The same sentence also appeared in one
tracked durable record, `guidance/corpus-browser-roadmap.md`, and in a source
comment in `src/web/browser/catena/catena.js`; **both are corrected at this head.**

A terminology note the corrected statement adopts: the route's reader state
lives in the **hash fragment**, not the query string. The only true query
parameter in play is `?data=`, read once by the shared core and never written by
any route. The corrected wording says "hash key".

## 2. The exact actual behaviour

**Unrecognized hash keys are judged by nothing.** `hashProblems` iterates a
closed list — `book`, `chapter`, `bible`, `voice` — so a stranger key is never
validated, never refused, and never reported, including when it is itself cited
twice.

**They survive exactly as long as the route writes nothing.** Every write the
route makes replaces the *whole* fragment with those four keys alone; there is
no merge, no carry-forward, and no stranger-preserving serializer anywhere in
the file. Preservation is a consequence of not writing, not a preservation rule.

| Path | Trigger | Stranger keys | Deciding code |
| --- | --- | --- | --- |
| Valid, value-identical address (including scrambled order, `chapter=01`, `%3A`) | `identical === true`, so nothing is written at all | **preserved, byte for byte** | `src/web/browser/catena/catena.js` `writeRoute`, the four-key `identical` test and its early return |
| Invalid address / duplicate recognized key | `renderInvalid`, which never touches history | **preserved** — but the recovery link it offers drops them | `onArrival`; `renderInvalid`; `link.href = currentHashText()` |
| Partial or otherwise non-identical arrival | completed in place with `replaceState(…, currentHashText())` | **discarded** | `writeRoute` arrival arm + `currentHashText` |
| Reader action (control change, prev/next, arrow) | pushes through `T.writeHash` with the four pairs | **discarded** | `writeRoute` reader arm + shared `writeHash` |
| Async chapter-load failure | still reaches `writeRoute(wasArrival)` | discarded or preserved, per the arm above | the `catch` in `render()` |
| Echo / no-op hashchange | no render, no write | untouched | the `selfWrote` and `currentHashText` guards |

Back and Forward are **not** a separate case: there is no `popstate` handler,
and hash navigation re-enters the same single `onArrival` the cold load uses.
One consequence is worth stating plainly because it is invisible in the address
bar: because completion uses `replaceState`, arriving at a *partial,
stranger-bearing* history entry via Back rewrites **that history entry in
place**, so the stranger is destroyed in the back-stack, not merely in the
current URL.

## 3. What is proven, and what is only read

Proven by test at this head:

- one unrecognized key (`note=kept`) on a value-identical, non-canonically
  spelled arrival is kept byte for byte, with zero writes and zero replaces
  (`test_an_equivalent_arrival_address_is_never_rewritten`);
- a partial arrival and a hashless arrival are completed in place to the
  four-key canonical text and push nothing;
- a reader action pushes exactly those four keys — also pinned cross-file by
  `tools/tests/test_browser_url_contract.py`;
- an invalid or duplicate-key address leaves the fragment exactly as written.

**Not proven by test — read from the code, and labelled as such:**

- that an unrecognized key is *discarded* by partial completion or by a reader
  action (no scenario carries a stranger on a non-identical address);
- that an unrecognized key *survives* an invalid address, a duplicate-key
  refusal, or a duplicate of itself;
- that the recovery link drops it;
- that `replaceState` destroys it in the restored history entry on Back;
- anything about `?data=` alongside the route: the replay harness fixes
  `location.search` to `''`.

**No universal preservation is claimed.** V3 deliberately did not add these
tests: each would pin URL behaviour that the review did not ask to change, and
the review's instruction was to correct the statement, not to extend the
contract. Closing them would take four scenarios —
`#BOOK=Foo&book=Gen&chapter=2`; a stranger-bearing complete address followed by
a chapter change; a stranger on an invalid address; and `note=a&note=b`. That
is a decision for the reviewer, and it is raised as a question rather than taken
here.

## 4. The corrected sentence

> Unrecognized hash keys are read by nothing and refused by nothing: the
> validator judges only `book`, `chapter`, `bible` and `voice`. They survive
> exactly as long as the route writes nothing — on an address that already
> parses to the rendered state, and on an invalid or duplicate-key address that
> is left as written. Every write the route makes replaces the whole fragment
> with those four keys alone, so an unrecognized key is discarded when a partial
> or otherwise non-identical arrival is completed in place, when a reader action
> pushes an entry, and in the recovery link the invalid page offers. Preservation
> is a consequence of not writing, not a preservation rule.
