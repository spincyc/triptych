# Final integration cold review — proper-study v6 release candidate

## Verdict: PASS

I found no release blocker in the exact candidate reviewed at HEAD
`77f4db0855ff2dc7867400d6dc0be0c704e06a5a`. The outgoing tracked binary diff
against `origin/main` hashes to
`8bae373ed191a975d603bd2830c6d3b6b5facfd0973e9ee8a153a50f6c098685`.
The candidate coherently implements and exercises the three-document proper
study contract, keeps the 1962 and postconciliar families independent, restores
the established synthesis style, and installs the exact reviewed publication
bytes.

This was a read-only review of tracked content. I changed no tracked file and
made no commit, workflow advance, installation, or external mutation. I wrote
only this ignored `.scratch/final-integration-v6/` review record and disposable
files under `/tmp`.

## State machine and source graph

Proper-study v6 requires the shared format contract at content, artifact, and
publication gates. The semantic graph admits only literal, one-time recursive
imports, rejects hidden TeX execution and local replacement of shared
presentation commands, seals each lane's research-owned evidence, reconciles
its accepted graph with TeX recorder inputs, and requires the exact canonical
postconciliar shared owner. The workflow route remains the complete sequence
from scope and context through independent research, study, synthesis, homily,
artifact, visual, web, installation, and terminal publication review.

I independently ran the six focused unittest modules covering proper format,
component closure, study preflight, chronology, web conversion, and workflow
routing: **426 tests passed**. All four live publication checks passed with
`--require-presentation --require-format`. `make check-web-editions-current`
also passed. The requested pytest launcher was unavailable in the system Python;
this is not a skipped test because the repository's unittest invocation ran the
same selected modules successfully.

The durable hardening report additionally binds 308 focused tests, 346 adjacent
tests, 144 live content checks, 12 wrapper checks, four isolated conversions,
and four recorder/semantic-graph reconciliations. Its reviewed implementation
is part of the outgoing commit range.

## Rite and owner isolation

The four manifests have the correct family identity and calendar:
`roman-1962` only beneath each provider's 1962 tree and `postconciliar` only
beneath the U.S. 2011 edition tree. A direct scan of active files (excluding
historical evaluation packets) found **zero cross-family path or calendar
references** in all four leaves. All four publication checks re-resolved their
complete component and dependency graphs successfully.

The independent chronology/rite audit inspected 159 path-valued liturgical
references and found zero crossing references. The postconciliar shared-owner
resolver is tied to the exact edition/formulary publication-slug row and has no
1962 fallback. Shared Scripture source records are evidence sources, not a
shared liturgical owner. The selected Matthew comparison remains a separately
sealed comparison profile and never enters either default chronology answer.

## Twelve PDFs and four Sunday web editions

Every file, byte count, SHA-256, and page count in
`workflows/reviews/propers-three-documents-v6-final-2026-09-21/artifact-identities.json`
recomputed exactly: **16/16 records match**. The twelve PDF extents are:

| Owner | Expansive | Concise | Homily |
| --- | ---: | ---: | ---: |
| GPT 1962 | 22 | 10 | 3 |
| GPT postconciliar | 20 | 10 | 3 |
| Claude 1962 | 31 | 10 | 3 |
| Claude postconciliar | 31 | 10 | 4 |

All 157 pages use embedded Latin Modern-family fonts. Each expansive study has
exactly three `properlane` sections and each lane has exactly one four-senses
block containing Literal, Allegorical, Moral, and Anagogical entries. All four
concise PDFs place the four senses with the complete proper map on page 1,
Scriptural Date and Location on page 2, Themes and Movement on pages 3–4, and
Detailed Commentary from page 5. Homily speech is structurally isolated in the
shared two-column `properhomily` environment before its terminal apparatus.

The four installed Sunday Markdown editions recompute to the recorded hashes:

- GPT 1962: `a90987a6a5e6bfcb0e7cc98c9802ae1812f057e21c5811abaa7b5217659ea9bf`
- GPT postconciliar: `245d39ec02d1ea3b147b0131134fd3f7b39db96d3483ba2a1fe531340c1fa2cd`
- Claude 1962: `d9009d445a8e438ffe603e4dd063535f5795db790cb2b7ca6688b5ed6c3df830`
- Claude postconciliar: `b00ee2b37eac785eb0f616f7ef99b685ca8ea5b276c891c9e1b94467af8e3ea6`

The provider/rite production and browser cold reviews preserved beside the
release record inspected every page and responsive web route and record no
unresolved finding.

## Accepted v6 run archives

Both archives are complete and exact copies of their live engine evidence:

- `090e496c9d6d4104`: 23 packets and 23 results; 49 mapped engine files plus
  terminal status/replay and record; disposition `ACCEPTED`.
- `bbe114e132356b38`: 30 packets and 30 results; 63 mapped engine files plus
  terminal status/replay and record; disposition `ACCEPTED`.

For each archive, `seed-manifest.json`, `seed-bootstrap.json`,
`terminal-state.json`, every packet, and every result are byte-identical to
`build/tpt-runs/<run>/`. Fresh `status` and `replay` outputs are byte-identical
to the archived terminal files; replay reports `recorded_file_intact: true`.
No credential, private-key, authorization header, `/home/ksh`, or `/tmp` string
was found in either tracked archive.

## Ancillary web regeneration

All 15 ancillary web changes are current deterministic output from the changed
semantic-break converter, and every current file has zero trailing-space or
tab lines. Fourteen editions have byte-for-byte equivalent normalized Pandoc
plain content before and after regeneration; only semantic `<br>` markup and
serializer layout changed.

The fifteenth is GPT's 1962 *Assembling the Mass*. Its prior generated edition
lost the print-only checkbox geometry. The revised source has:

- exactly **24** semantic `☐` glyphs;
- exactly **16** checkbox table rows and **8** checkbox list items;
- built HTML with all 24 glyphs attached to those same 16 `tr` and 8 `li`
  ancestors, and no unattached glyph;
- no literal or whitespace-variant `<p>-</p>`;
- an exact **17,660-token** substantive-word sequence match to the prior
  edition after removing markup and checkbox geometry.

Thus the repair restores semantic controls without prose loss. The source and
browser build each contain one checkbox table and one checkbox list. The new
web-edition regression derives the expected checkbox count from the TeX source
and checks both attachment cases.

## Ledgers, projections, promises, and scope

The refreshed generated state passes:

- GPT inventory: 142 publications, 2,360 source-surface files, 11 owners;
- Claude inventory: 54 publications, 1,322 source-surface files, 5 owners;
- source library: 2,746 artifacts, 992 editions, 5,182 passages, 726 works,
  2,868 bindings;
- document projection: 142 works, 196 documents, 6,281 pages;
- source-reader projection: 4,052 current files;
- source-family migration check and publication inventories;
- release bindings: zero stale bindings;
- promised-deliverable ledger; and
- `git diff --check`.

The two current deliverables correctly remain `in_progress` with only their
main/Pages requirements open. That is the truthful pre-push state, not a
candidate defect. After the reviewed commit reaches `origin/main` and the exact
Pages run/routes are verified, those two requirements and the corresponding
project-work publication paragraph must be closed with the observed deployment
evidence.

Every outgoing path belongs to one of these task-owned groups: shared
proper-study/chronology/web mechanics and tests; the four provider/rite leaves;
source evidence and its generated inventory/projection records; installed and
release-bound publications; the two exact run archives; durable cold-review
records; promise/project memory; or the 15 converter-driven regenerated web
editions. I found no unrelated or accidental change.

## Reproducing the verdict

The exact invocations are summarized in `COMMANDS.md`; hashes are in
`HASHES.sha256`. Relevant checks all exited zero. The only initial nonzero was
`python3 -m pytest`, because pytest is not installed; the equivalent direct
unittest run then passed all 426 tests.
