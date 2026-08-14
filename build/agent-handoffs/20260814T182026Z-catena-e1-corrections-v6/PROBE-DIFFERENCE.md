# What real Chromium read at each head

Both runs used the same tool, the same fixtures and the same browser, over two
built sites: the parent `19982ab433dd25704ed60b1ac6ddb678bc3a98f9` and this
head. Eleven states, ten fabricated and one real-corpus, each labelled as such
in the report. `logs/probe-parent.json` and `logs/probe-head.json` are the two
reports; `logs/probe-parent.stdout.txt` and `logs/probe-head.stdout.txt` are the
runs' console output verbatim.

Every value in the table below was **measured at both heads**. Nothing here is
inferred from the code or carried over from a previous package.

| Class | Parent `19982ab4`, measured | This head, measured |
| --- | --- | --- |
| Root/Bible language | `#bible-select` offered `Douay-Rheims ([object Object])`, `Number Language (42)`, `Boolean Language (true)`, `Blank Language (   )`, `Prose Language (not a language code)`. `.passage` carried `lang="en"`. | Options are the label alone for every unreadable language; `Clementine Vulgate (la)` keeps the one sound claim. `.passage` carries **no** `lang` attribute — omitted, not guessed. |
| Testament | `#reference-book` read `New Testament` over Genesis. | `#reference-book` is empty. |
| Collection members | Tally `3 fragments held · 3 works held, not renderable yet · 3 lead entries`; one blank lead row and one blank blocked row stood in the document; the refusal read `Boundary not established.  Commentary on Genesis 1 is anchored…` — the claim made with the reason sentence missing. | Tally `3 fragments held · 2 works held… · 2 lead entries`; no blank rows; the refusal states its reason. |
| Order-independent findings | The two orders produced **different pages**: `terminalReadsEqual: false`, `differingKeys: ["absenceReasons","absenceSummary"]`. Reversed, the page said `One work … has no English this project may publish; … 3 have a finding this page cannot read`. | `terminalReadsEqual: true`, `differingKeys: []`. Both orders say the same sentence. |
| Stray `partial` | Five `.absence-partial` lines: four of them stray offers beside `not-surveyed`, an unknown finding, no finding at all, and a closed finding. | One line — the only one a `partial-public-domain` finding licenses. |
| Padded verse keys | `.verse-num` read `["1","1","1","2","2","3"]` and the chip said `6 verses`. | `["1","2"]`, chip `2 verses`. |
| Unsafe textual identity | 15 URLs requested, including `/browse/etc/passwd.json`, `…/text/%2e%2e%2fsecret.json`, `…/text/Upper.Case.json`, `…/text/a%20space%20is%20not%20an%20id.json` and `…/text/trailing/.json`. | 10 URLs; none of those five. |
| Null bootstrap | Reference read `Loading…` for ever; `aria-busy` was **absent**; the status region was **absent**; all four controls read `Loading…`. | Reference `Unavailable`; `aria-busy="false"`; status `The catena index could not be read.`; controls `Unavailable`. |

## The one class where the two heads do not differ

**Genuinely late stale work shows no difference between the parent and this
head, and that is recorded as a true negative rather than dressed as a finding.**

In the `late-stale-work` state the probe starts an action, holds its response,
lets a newer action settle completely, and then releases the held one. At both
heads `hash`, the tally, `aria-busy="false"`, the status line, the chapter
control and the focused element are unchanged across `a-held`, `b-settled` and
`a-late`, and no fragment text is ever anything but its placeholder.

Two things follow, and both belong in the record:

1. **The V5 review's finding about this class was about the PROOF, not the
   behaviour.** Its complaint was that the V5 "nothing stale" case released the
   payload before navigating, so no late work existed and the oracle could not
   fail. That is corrected in the suite — `GenuinelyLateStaleWorkTest` holds A,
   settles B, then releases A, and `LateWorkReallyHappenedTest` asserts the
   harness's count of requests actually let go. V6 adds the proof; it did not
   need to change this behaviour.
2. **The probe is blunt here and says so.** The held request is a fragment-text
   fetch whose target node is destroyed by the chapter change, so it has little
   opportunity to commit at either head. A held *spine* fetch would be a sharper
   probe of the same class. No difference was claimed and no picture was taken.

The behaviour V6 *did* change in this area is the invalidation of pending work
by a terminal state — `startFailed` now calls `beginRender`, clears the tally
and completes focus — and that is evidenced by the null-bootstrap row above and
by `NullBootstrapTerminalStateTest`, not by the late-stale-work state.

## Focus

`document.activeElement` is recorded for all 11 states and all 15 reads in
**both** reports; a checker over both files reports no missing focus field.
`grep -ic focus` returns 32 on each report. The V5 tool and both its reports
returned zero, while three V5 records stated the probe read the focused element.

The focus measured is the same at both heads. It is stated as three distinct
kinds and never as a fourth: `body` outside the reading region where nothing
moved focus, `summary.fragment-head` inside it where the probe opened a
fragment, and `select#chapter-select` where the probe operated the control. The
probe focuses a control before operating it, because a bare programmatic click
leaves focus on `body` and a focus reading taken after one is a reading of a
state no reader is ever in.
