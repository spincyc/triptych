# Final repair and cold-acceptance handoff — Scripture chronology corpus

This lane closed the twenty-three `CHANGES_REQUIRED` rows of the targeted cold
re-review, and nothing else. It authored no new chronology, broadened no
corpus, integrated nothing, merged nothing, and accepted nothing. What it
produces is a **review surface** and a request: that a genuinely cold reviewer,
in a new session, review all of it.

## Head references, by sha

```text
audited corpus        2330d63a5e132b2f0df1b951b8c6182bf0a25695
                      what the cold independent source audit reviewed.

correction target     214797e784be0f20b40e6e64aefbe928e80d69c4
                      what the post-audit correction lane produced, and what
                      the targeted cold re-review reviewed.

                      post-audit-correction-report.md line 9 names
                      15213f79ca956f11ec8fb0844c6d25ec418af34a as "correction
                      final HEAD". That sha is the lane's last CORPUS-AFFECTING
                      commit, not its final head: the report was first written
                      one commit later, at 82e6a1bff, and last edited at
                      214797e78 itself. The six commits between them change no
                      chronology YAML, no coverage.tsv and no scripts/ file;
                      they change the review artifacts, the README,
                      PROJECT-WORK.md, promised-deliverables.toml, the derived
                      web source view, the stored transcripts of
                      tools/scripture-chronology and tools/source-reader, and --
                      at bff00167f -- one shell gate's ASSERTION, which is more
                      than recording, so the report's implicit "nothing but
                      recording" is slightly too strong.

                      Line 9 is deliberately LEFT AS IT STANDS. This block
                      supersedes it. post-audit-rereview-findings.tsv cites that
                      report by line number, and rewriting the line would make a
                      published finding in immutable review evidence
                      unreproducible against the tree -- the finding would erase
                      itself.

review-artifact head  fdab026bed84293e6f1ceb4bb9b2366c0d1f699e
                      where the targeted cold re-review's OWN artifacts landed:
                      post-audit-rereview-report.md and
                      post-audit-rereview-findings.tsv, added there and
                      unmodified since. It is NOT what that review reviewed.
                      Its report says "review target: 214797e78 (branch
                      feature/bible-dating, == HEAD)" and "branch advanced
                      beyond the target: no"; both were true when written and
                      both are false now, and neither is amended, for the same
                      reason as line 9 above.

current repair head   this lane's HEAD on feature/bible-dating.
                      Every "this lane" below means the interval
                      214797e78..HEAD.

origin/main           2778285849f2973ea89d1cfd5b2751ed4ae58e54
```

## What the review evidence says, and what is not touched

Four files are immutable review evidence and are unchanged by this lane:

```text
src/sources/chronology/cold-audit-report.md
src/sources/chronology/cold-audit-findings.tsv
src/sources/chronology/post-audit-rereview-report.md
src/sources/chronology/post-audit-rereview-findings.tsv
```

`post-audit-corrections.tsv` and `post-audit-correction-report.md` are also
left as written. They are the completed record of what an earlier lane decided
against a frozen commit, and the re-review cites both. Where this lane found
one of their statements false, the correction is recorded here and in
`final-rereview-corrections.tsv`, never by rewriting them. Two rows are
re-dispositioned that way: **A4-017**, whose withdrawal rested on a loader
constraint the loader does not impose, and **F-021**, recorded as defeated when
one limb of it was never addressed.

## The final acceptance manifest is derived, not chosen

`src/sources/chronology/final-acceptance-manifest.tsv` is the review surface.
It is the union of two production diffs --

```text
2330d63a5..214797e78    the post-audit correction lane
214797e78..<this head>  this repair lane
```

-- taken by loading **each revision's corpus through that revision's own
loader** and diffing the loaded objects, so that a reformat cannot hide a
change and a loader that has since tightened cannot refuse to read the older
side. Cases are deduplicated on `case_type + ":" + claim_or_scope_id`.

Three things the earlier 92-row manifest could not see, all now in scope:

- **The 92 rows are 96 cases.** Two rows duplicate others (`RR-090` is `RR-031`
  again; `RR-077` is the seven Flood-to-Abram claim rows again as one hard
  case) and two rows are bundles (`RR-091` names two source records, `RR-092`
  names six). A reviewer assigning one row per reviewer would have
  double-assigned two claims and under-reviewed the source registry by six
  records.
- **Four binding groups changed materially with no scope change**, and the
  earlier manifest compared scope alone. Two of the four are corrected
  misquotations of the tracked Douay -- the exact class three auditors
  independently raised.
- **The guidance contract and the loader changed** across the range and no row
  enumerated them. `GUIDANCE-6` was caught by a reviewer's eye, not by the
  apparatus.

Completeness is proved, not asserted:

```sh
python3 scripts/check_final_acceptance_manifest.py \
    --range 2330d63a5..214797e78 --range 214797e78..<this head>
```

fails on any changed case the manifest omits, any manifest row no diff
supports, and any prior review id -- all 218 across the three prior artifacts --
that no row's provenance columns cite.

## The final acceptance review must be genuinely cold

The targeted re-review disclosed its own limitation: it ran in the same session
as the lane whose work it reviewed. This lane is in the same position and makes
no acceptance claim of any kind.

**The final acceptance review must run in a clean new agent or session that did
not perform the population, the first audit, the post-audit correction, the
targeted re-review, or this repair.** No same-session subagent arrangement
satisfies `independent-source-audit`. That reviewer must:

- read repository artifacts only;
- review **every** row of `final-acceptance-manifest.tsv`;
- reopen the sources rather than trust any ledger, report or test here --
  including this file;
- run the structural gates;
- return PASS or CHANGES_REQUIRED per row and overall;
- independently recommend the promise states.

## Two hazards a cold reviewer will otherwise hit

**New Advent's bytes drift, and two registered hashes no longer refetch.**
`03731a` (Howlett, "Biblical Chronology") and `08654a` refetch today at hashes
that do not match their registered `sha256`. The drift is New Advent's page
furniture, not article text: the retained extractions under
`.scratch/cold-audit/text/` carry every quoted sentence, and that cache is the
evidence of record. The same is true of the `11646c` and `10596a` pairs, where
the whole 359-byte delta between the two registered retrievals of each page is
one injected Cloudflare analytics tag and the article text is identical in
both. Those four records now say so in their own notes.

**`.scratch/cold-audit/src.py --bible <locus>` is a broken stub.** It raises
`ModuleNotFoundError` and always has. Read tracked Scripture from the JSON:
`src/sources/bibles/douay-rheims/chapters/<Book>/<chapter>.json`, key
`verses["<n>"]`. `src.py <artifact-id>` and `src.py <artifact-id> -g REGEX` do
work and are the source reader. Any earlier lane that reported a Scripture
locus blocked may have been blocked by this stub rather than by the source.

**And one CLI footgun:** `--root` works only *after* the verb.
`scripture-chronology --root P query …` silently answers from the invoking
checkout instead of from `P`.

## Promise state

`scripture-chronology-corpus-2026-08-26` remains **`in_progress`**. This lane
marks nothing pass.

| Requirement | State after this lane |
| --- | --- |
| `translation-independent-identity` | `READY_FOR_FINAL_COLD_ACCEPTANCE` — none of the 23 corrections touches it |
| `exhaustive-coverage` | `READY_FOR_FINAL_COLD_ACCEPTANCE` under the criterion as written, which requires a research-gap category and not zero `research-pending` |
| `independent-source-audit` | **OPEN.** Only a genuinely cold reviewer can close it. |

The seven native `research-pending` loci are preserved. No date was invented to
close them, and the criterion was not rewritten to excuse them.

## Not in this lane

No new chronology population. No propers integration, and none may begin until
a maintainer accepts and merges. No merge. No acceptance.
