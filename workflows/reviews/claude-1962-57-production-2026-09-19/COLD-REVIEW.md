# Cold review of the Claude Seventeenth Sunday delivery

An independent reviewer with no part in the production read the sixteen
commits `0c5aeb364..1a2e66c1c` and the tree they produce, after that range had
been pushed to `main` and deployed. It was asked to judge the work, not to
defend it, and to say what it could not verify. Its verdict: **sound as
published, with one register correction owed before the next handoff.**

## Findings and what was done about each

| # | Severity | Finding | Disposition |
| ---: | --- | --- | --- |
| 1 | substantive | The narrative says sixteen cycles. The run has fifteen non-PASS transitions: fourteen review-driven and one gate failure. The count double-counted the one review whose findings split across two owners, and its own tables already summed to fifteen. | **Corrected** in `CYCLES.md` and `PROJECT-WORK.md`. The claim that six cycles were repair-generated is likewise corrected to five, with the fifth named. |
| 2 | substantive | `PROJECT-WORK.md` still told the next reader that six legacy convergence defects were open and that no engine change was authorized, after `d637adf6e` had repaired one of the six under a later authorization. | **Corrected** with a dated superseding paragraph; five remain open. The recovery record carries the same clarification. |
| 3 | minor | `CYCLES.md` said both standing research-owned advisories were in intervention 0001; only the Aquinas one is. | **Corrected.** The second is recorded in the standing-findings file and in `author-study` iteration 7's result. |
| 4 | minor | "Two remain that no stage could clear" is true but reads as though only two advisories stand; fifteen advisories and nine observations stand in all. | **Corrected** by giving the total beside it. |
| 5 | minor | `ca3448f7f` says each installed PDF hashes to what its cold reviewers read. Exact for the visual review and the homily; not for the two studies' content reviews, whose proofs predate the shared-timestamp rebuild. | **Recorded** in `CYCLES.md`, since a pushed commit message cannot be corrected in place. The artifact gate re-verified every seal after that rebuild. |
| 6 | minor | `9d076ac69` regenerated the catalogue without re-recording the site-source approval, so that intermediate commit fails `public-alpha verify`; `1a2e66c1c` repairs it. | **Recorded.** Only the final tree is represented as deployable, and it is the tree pushed and verified. |
| 7 | minor | The study runs to 13,918 substantive words against a "roughly 6,000–10,000" planning range. | **No change.** The profile states a range and not a quota, the PDF is inside its 20–50-page contract, and the excess is disclosed in the production record. |
| 8 | minor | "86 accepted results" means schema-accepted submissions, fifteen of which were CHANGES_REQUIRED or FAIL. | **No change**; the archive's own table gives every disposition. |

## What the review verified independently

It did not take the records' word for the artifacts. It copied the tree without
`build/` or `.git` into a scratch area and rebuilt all three documents, which
came out **byte-identical** to the installed PDFs at 38, 12 and 5 pages. It
confirmed the concise document's fixed opening from the settled auxiliary file
rather than from prose, re-counted the homily's spoken body at exactly 1,429
words, verified all 86 packet and 86 result hashes in the run archive, and
reproduced the finding counts, the stage tallies and the budget position
(`stage_novel` 3 of 4 at its worst, so no stage came closer to a stop).

It also tested whether the five workflow repairs are real by reverting each in
its own copy: every one produced failures, including the shared-reviser fix
failing five of its six cases, and the full suite passes at 946 tests. It
judged the census edit in `test_workflow_synthesis_preflight` legitimate rather
than a green-wash, on the evidence that the assertion was already red at
`0c5aeb364` with sixteen leaves and that the substantive list of six refused
leaves is textually unchanged and now runs.

## What it could not verify, in its own terms

The scholarly substance — patristic loci, Migne transcriptions, Missal page and
rubric numbers — which is a content review and was the business of the run's
own cold reviewers. That every stage ran as a fresh worker at its declared
effort: unfalsifiable from the tree, and intervention 0000 is testimony rather
than proof. The recovery survey of clones outside this checkout. The Pages run
itself, which is recorded separately in `deployment-evidence.json`.
