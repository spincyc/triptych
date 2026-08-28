# Final cold acceptance review — Scripture chronology corpus

**Audited corpus: `5b4fe31c0f5c99042412342a854d04ae01936b47`, branch `feature/bible-dating`.**

This is the genuinely cold acceptance review the repair lane asked for. It was
performed in a new session that carried out none of the population, the
named-system correction, the exhaustive Vulgate population, the first cold audit,
the post-audit correction, the targeted re-review, or the final 23-row repair.
It reopened the sources rather than trusting any ledger, report or test in this
tree, including `final-repair-report.md`.

## What was reviewed

| | |
| --- | --- |
| final acceptance cases | 156, every one |
| prior review ids carried | 218 of 218 |
| whole-artifact obligations | Howlett (46 retained claims) and Sloet (16 claims), each enumerated from the loader |
| structural gates | re-measured, not read off a report |

## Head references

```text
origin/main                   2778285849f2973ea89d1cfd5b2751ed4ae58e54
origin/feature/bible-dating   5b4fe31c0f5c99042412342a854d04ae01936b47
local HEAD at review          5b4fe31c0f5c99042412342a854d04ae01936b47
branch advanced beyond target no
working tree at review        clean
```

The manifest's own header names its second diff range as `214797e78..eb38161ba`,
and three commits follow `eb38161ba`. Those three change `PROJECT-WORK.md`,
`promised-deliverables.toml`, the manifest builder, this tree's README, the
manifest, `final-repair-report.md` and `final-rereview-corrections.tsv` — no
chronology YAML and no `coverage.tsv`. Re-running the completeness checker with
`--range 214797e78..HEAD` rather than `..eb38161ba` still passes in both
directions, which is independent confirmation that no production case lies in
those three commits.

## How the sources were reopened

Every registered New Advent artifact this review turned on was **refetched live**
and compared against the retained extraction under `.scratch/cold-audit/text/`,
not read from the extraction alone. Tracked Scripture was read from
`src/sources/bibles/<edition>/chapters/<Book>/<chapter>.json`. Where a lane's
conclusion turned on a single sentence, the sentence is quoted here in full.

`.scratch/cold-audit/src.py --bible <locus>` is a broken stub and always was; it
was used for nothing, and §8 below reports what depended on it.

## Verdict

```text
STATUS                          CHANGES_REQUIRED
AUDIT TYPE                      final genuinely cold Scripture chronology acceptance audit
audited corpus                  5b4fe31c0f5c99042412342a854d04ae01936b47
branch                          feature/bible-dating
origin/feature/bible-dating     5b4fe31c0f5c99042412342a854d04ae01936b47
origin/main                     2778285849f2973ea89d1cfd5b2751ed4ae58e54
branch advanced beyond target   no

REVIEWER INDEPENDENCE
  new clean session/agent                yes
  participated in prior chronology lanes no
  independence requirement satisfied     yes

FINAL ACCEPTANCE MANIFEST
  path                           src/sources/chronology/final-acceptance-manifest.tsv
  expected cases                 156
  reviewed cases                 156
  missing                        0
  duplicates                     0
  historical review ids expected 218
  historical review ids present  218
  completeness checker           passes, both directions, exit 0
  changed production cases outside the manifest   none

RESULT TOTALS
  PASS                           130
  CHANGES_REQUIRED                26
  BLOCKED_SOURCE_UNAVAILABLE       0
  BLOCKED_SOURCE_INSUFFICIENT      0
```

| case type | PASS | CHANGES_REQUIRED |
| --- | ---: | ---: |
| claim | 70 | 3 |
| architecture | 28 | 7 |
| source-record | 14 | 6 |
| binding | 10 | 1 |
| code | 5 | 4 |
| gap | 3 | 3 |
| contract | 0 | 2 |
| **total** | **130** | **26** |

| requirement | recommendation |
| --- | --- |
| `translation-independent-identity` | **PASS** |
| `exhaustive-coverage` | **PASS** |
| `independent-source-audit` | **KEEP OPEN** |
| `scripture-chronology-corpus-2026-08-26` | **IN_PROGRESS** |

The corpus is in better condition than a bare `CHANGES_REQUIRED` suggests, and
the reasons it fails are few and specific. Both requirements this lane could
close, it closes. The third cannot close, because its own text closes it only on
a PASS disposition, and defects survive that acceptance cannot absorb — four of
them wrong answers a consumer reaches today with a single query, and one a
contract silence that makes the largest defect class irreproducible by the next
reviewer.

Nothing here impugns the repair lane. Most of what it fixed is fixed, its two
disclosed hazards were both real and both material to this review, and its
decision to escalate Howlett and Sloet to whole-artifact obligations is what
found three of the most serious defects — none of which is a manifest row.

## Is the acceptance surface complete?

**Yes on the facts. No on the guarantee.**

The manifest holds 156 rows, 156 distinct cases keyed on
`case_type + ":" + claim_or_scope_id`, no duplicates, `FA-001` to `FA-156`. The
218 prior review ids reproduce independently: `cold-audit-findings.tsv` 104,
`post-audit-rereview-findings.tsv` 114, `post-audit-rereview-manifest.tsv` 92,
union 218, every one cited by some row's provenance columns, none orphaned and
none invented. The completeness checker exits 0 in both directions, and it still
does when the second range is extended from `..eb38161ba` to `..HEAD`.

Reviewed independently of that checker:

- **claims** — 73 changed claim keys, 73 manifest rows, no omission and no
  unsupported row;
- **bindings** — 11 and 11; three disappearances across the whole range, each
  with a row;
- **gaps** — 21 gap rows exist, exactly 6 changed, exactly those 6 are in the
  manifest; the other 15 are byte-identical across both ranges;
- **raw diff** — 84 hunks across the four authored YAML files walked by hand: 83
  map to a manifest row, the 84th is a comment block. **Zero unrepresented
  factual hunks.** `profiles.yaml` is unchanged across the range.
- **the three later commits** — `eb38161ba..HEAD` touches no chronology YAML and
  no `coverage.tsv`.

**No unexplained changed factual state exists outside the manifest.**

What is overstated is the *warrant*. The manifest header says its checker "fails
on any changed case this file omits". The differ underneath it cannot see:

| blind spot | consequence here |
| --- | --- |
| a binding's `note`/`sources` whenever its scope also changed | 3 groups reported as `scope-changed` only, one of them a whole-book Daniel binding re-pointed with a rewritten evidential note |
| event and unit fields entirely — the worker dumps only `.claims` | 11 event-note rewrites and one unit scope+title change invisible; an event or unit added or removed **with no claims** would be wholly invisible, and the corpus now holds two claimless events |
| `profiles.yaml` | never compared |
| the tracked bibles | symlinked into both revisions and only warned about |
| endpoints only, not the path between them | `Ps.70` was genuinely dropped from the Absalom binding at `8264315f9` and restored at `15213f79c`; the endpoints match, so the loss is invisible to the apparatus and visible only to someone who parses all six commits |

The sharpest illustration is the corpus's own flagship correction: the Mark 15:33
misquotation lived in the Crucifixion **event** note, and produces **zero rows**
from the differ. It reached the manifest because three human reviewers recorded
it as prior findings, and for no other reason.

So the surface is complete, and it is complete by human diligence rather than by
the mechanism the artifact cites. That distinction matters for the next wave,
which will be told the mechanism is sufficient.

### What held up under machine sweeps

Two checks worth recording because they are the strongest positive evidence in
this review, and because both were run rather than argued:

- **Quotations.** All **2,513** quoted spans across the four chronology YAML
  files were matched against every verse of the tracked Douay: 440 exact
  matches, 28 near-misses, and all 28 triaged by hand and found legitimate —
  multi-verse joins, marked ellipses, or Augustine's own NPNF rendering,
  each reopened. **No surviving misquotation of tracked Scripture.**
- **The cold audit's own sample predicate.** The manifest header's selection rule
  was re-implemented from scratch against `2330d63a5`: 458 authored claims,
  exclusions of 47/9/2/1 with a union of 57 (two overlaps), pool 401, stratified
  by precision and disposition, `sha256(seed+id)`, round-robin — and it
  **reproduces all 72 ids in their exact order**. The sample really was
  deterministic and really was what it says it was.

## Howlett — whole-artifact ruling

**Source.** `artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04`
— Howlett, James, "Biblical Chronology", *The Catholic Encyclopedia*, vol. 3
(New York: Robert Appleton, 1908), <https://www.newadvent.org/cathen/03731a.htm>.

**Artifact integrity.** The registered `sha256` no longer refetches: registered
`f5f96f04…` / 80 577 bytes against `8c2b33f6…` / 80 218 bytes today. The article
**text** is nevertheless identical. This was established three ways — a fresh
fetch normalised and compared against the retained extraction (the only
differences being spaces inserted before punctuation after New Advent's glossary
hyperlinks, three table-cell boundaries and one Greek span boundary), and against
the independent Wikisource transcription of the same article, in which the
occurrence counts of every figure ruled on here are identical (722 ×1, 721 ×1,
586 ×1, 536 ×2). The `536` in the summary sentence is therefore in the
transmitted text and is not a New Advent artefact.

**Enumeration.** Reproduced from the loader, not from the ledger:

| | |
| --- | --- |
| date claims citing the artifact at HEAD | **46** (all in `events.yaml`; none in `composition.yaml`) |
| binding rows citing it | 1, carrying no date |
| gap rows citing it | 2 |

The repair reports "52 total / 44 retained / 8 withdrawn". That does not
reproduce: 46 stand at HEAD, and the manifest itself lists 11 withdrawn rows
citing the artifact. The arithmetic reconciles on no reading. A ledger defect,
not a corpus defect.

**The withdrawals are right.** Every figure Howlett reaches on Egyptological or
Assyriological ground — Exodus about 1277, Saul 1020, David 1002, Solomon 962,
Temple begun 958, Temple about 969, the revolt about 936 and about 937, Solomon
973-936, David 1013-973 — is **absent from all 46 retained claims** (endpoint
scan: zero hits). They survive only as quoted prose in three subject notes that
say why they are not held. The article marks the departure itself: "This is not
the traditional date of the Exodus", and "We have fixed roughly the date of the
revolt of the Ten Tribes for the year 936 B.C. **But the traditional date is
975**."

There is **no comparison table of B.C. chronologies** in the article; the only
tables are the two patriarchal genealogies. Every one of those figures stands in
Howlett's own running prose, the 969 explicitly "according to Sayce".

**Nothing was withdrawn merely for keeping company with modern criticism.** The
New Testament and Machabean sections — 21 of the 46 — sit in an article that
quotes Wellhausen, Schürer and Cheyne on nearly every page, and are retained on
Howlett's own voice, which is right. The two Ussher-derived figures (1490, 1010)
are retained under the profile's express reporting licence, with Ussher named in
the basis and the licence cited in the note.

**One defect runs the other way**: a passage in which Howlett refuses to date
anything at all is authored as a date. See MF-2.

### The two contestable cases

**Fall of Samaria, 722/721 — PASS.** Adopted in Howlett's own voice ("We conclude
then…"), attributed to nobody, at the terminus of an Assyrian-canon
reconciliation. Admissible because the profile's exclusion bites on a modern
figure used to *adjust* or *correct* a traditional one, and 722/721 adjusts
nothing: the corpus independently holds `B.C. 721` from the Petavius table and
`722 B.C.` from Reid's "Captivities of the Israelites". Held `disputed` among
four claims with nothing preferred. The precision `interval` is right — the
guidance defines it as "the subject falls somewhere within from..to", which is
what a "722 or 721" disjunction asserts.

**Third captivity, 536 against 586 — PASS.** The article prints 586 once, in
section 7, and 536 twice: once as "the destruction of Jerusalem 536 B.C." in the
summary sentence, and once in section 8 as "The first band of captives returned
to Jerusalem under Zorobabel in the first year of Cyrus, i.e. 536 B.C."

It is a printing error for 586, and the article's own arithmetic proves it:
Howlett gives Achaz at **741 B.C.** and, in the next sentence, "from Achaz to the
destruction of Jerusalem, **a period of 155 years**". 741 − 155 = **586**. A 536
destruction would make that interval 205 years, would make the next section
("From the destruction of Jerusalem to the birth of Jesus Christ") span zero
years, and would have Jerusalem destroyed in the year the exiles returned from
the captivity that destruction caused. No combination of figures in the article
reaches 536 as a destruction date; 536 is reachable only as the first year of
Cyrus.

Production holds it as `alternate`, recorded exactly as printed, with the note:
"It contradicts the same article, which elsewhere gives 586 and puts the return
under Cyrus at 536; it has the look of a printing error, but this corpus does not
silently repair a source." That is the right disposition. Deleting it suppresses
a ranked source's statement; reading it silently as 586 is exactly the "silent
harmonisation of two claims into a third nobody asserted" the profile forbids.
`basis: derived` occurs zero times in `events.yaml`, so no harmonising third
figure exists anywhere.

## Sloet — whole-artifact ruling

**Source.** `artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08654a-645bba6c`
— Sloet, Dominicus, "Chronology of the Kings", *The Catholic Encyclopedia*, vol. 8
(New York: Robert Appleton, 1910), <https://www.newadvent.org/cathen/08654a.htm>,
sha256 `645bba6c…`, 54 683 bytes, retrieved 2026-08-26. Refetched live during this
review; the article text is identical to the retained extraction, the differences
being extractor artefacts (table-cell separators, spacing around punctuation).

**The article carries three tables, and they are not one object.**

*Table 1* sets out the Bible's own regnal data and prints no B.C. years. Nothing
in the corpus rests on it.

*Table 2* is Petavius's, introduced as the received scheme:

> "The celebrated seventeenth-century Jesuit **Petavius** composed in a very
> ingenious manner two chronological tables which, as brought by him into
> relation with the pre-Christian chronology have, with few alterations, **been
> in vogue for a long time**. These tables are here combined and presented as
> one."

*Table 3* is Sloet's own, and he states its ground himself:

> "**Since the deciphering of the Assyro-Babylonian inscriptions, the chronology
> of the period of Kings before 730 B.C. has become untenable.** We give here the
> points of chronological contact between the Assyro-Babylonian history and
> Sacred Scripture, as also those of Egyptian history."

> "The table below gives the chronology of the kings of Juda and of Israel, as
> nearly as possible in accordance with the figures of the Bible, **in
> conjunction with the data of profane history**."

and he emends Scripture from it, in the table's own Remarks column — "Reigned 33,
not 41, years", "'Third year of Osee' is incorrect" — on the ground that the
synchronisms "are not historical, but must have been introduced into the Bible by
a 'speculator'", citing Winckler.

**Ruling.** The phrase "in conjunction with the data of profane history" is not
by itself disqualifying, and this review declines to rule on the phrase. In a
1910 Catholic reference work "profane history" means secular history as distinct
from sacred, and harmonising with it in that broad sense is what Petavius and
Eusebius both do; if the phrase alone disqualified a table, ranks 4 and 5 of the
profile would fall with rank 6.

What decides it is the referent Sloet fixes two paragraphs earlier: **Assyro-
Babylonian inscriptions and Egyptian chronology, deployed to declare the received
scheme untenable and to emend Scripture, with Winckler cited for the result.**
That is the narrow class `catholic-traditional-v1` excludes by name — "Modern
critical, archaeological, Egyptological and Assyriological chronology … not
consulted, not used to adjust a traditional date, and not treated as a
correction." The profile's reporting licence is granted to Ussher by name and to
nothing else, so no reporting defence is available.

**Petavius is admissible; Sloet's own table is not.** Ten held claims rest on the
Petavius table and pass. Six rest on Sloet's own table and fail.

**The corpus already applied this rule to the other author.** Howlett's 958,
"about 969", 936 and "about 937" were withdrawn for resting on Sayce's
Egyptological and Assyriological reckoning. `israel.monarchy.temple-begun` now
holds a 969 withdrawn from Howlett and retained from Sloet, and its own subject
note concedes the gap: "The 969 this event still holds is Sloet's own table …
which this lane did not rule." One event, one number, two authors, one method,
opposite dispositions.

## The contract defect, and why it is the first thing to fix

Three lanes reached this independently, and it is the finding that governs the
correction order.

`profiles.yaml` admits the 1907-1914 Catholic Encyclopedia at rank 6.
`guidance/scripture-chronology.md` §4.3 excludes "Modern critical,
archaeological, Egyptological and Assyriological chronology" — "Not consulted,
not used to adjust a traditional date, and not treated as a correction."

**Neither says what happens when the rank-6 work's own voice IS that
chronology**, which is the normal case for every pre-exilic absolute B.C. year in
this corpus.

The word "consult" occurs exactly twice in 992 lines, and at §4.2 its subject is
the corpus, which makes §4.3 read as a test on what may be *asserted*. §15.1(3)
makes *voice* the discriminator. Both point the same way. The corpus went the
other way, and inconsistently, inside one article and one event:

| passage | voice | disposition |
| --- | --- | --- |
| Howlett: "the date of the Exodus was about 1277 … Solomon in 962, and the Temple was begun, 958 B.C." | his own | **withdrawn** |
| Howlett, adjacent sentence, same voice: "But the traditional date is 975" | his own | kept, **preferred** |
| Sloet's own table, of which his article says it is drawn up "in conjunction with the data of profane history" | his own | kept, **alternate** |

And the corpus cites, as if it were text, a rule that is not in the contract:
"the express reporting licence of guidance/scripture-chronology.md 4.3, **which
is granted to Ussher by name and to nothing else**." That is an inference from
silence. It happens to be the right inference — it is the rule that actually
decided several withdrawals — but a rule that exists only as silence cannot be
applied twice the same way, and here it was not.

**The consequence for acceptance.** `profile-boundary-leak` is the manifest's
largest class, 17 rows. Until §4.3 states the author's-method test, no ruling in
that class is reproducible by a second reviewer, which is precisely what
`independent-source-audit` exists to guarantee. **Fix the contract first, then
apply it once, consistently, to Howlett, to Sloet, and to the five preferred
modern-critical figures outside the surface.** Correcting the claims first would
leave the next lane to re-derive the same inconsistency from the same silence.

Suggested text, to be stated in §4.3 and in `profiles.yaml`'s `non_authorities`
entry: *a ranked Catholic source's rank attaches to what it transmits from the
tradition, not to a reconstruction its author builds on excluded method; no
reporting licence covers such a reconstruction, because §4.3's licence is granted
to Ussher by name and to nothing else.*

## Structural validation — re-measured, not read off a report

| gate | invocation | exit | result |
| --- | --- | --- | --- |
| chronology unit tests | `python3 -m unittest tools.tests.test_chronology` | 0 | **94 / 94** |
| validate | `tools/tpt scripture-chronology validate` | 0 | 1 profile, 279 events, 62 composition units, 375 bindings, 21 gaps, 73 books |
| check | `tools/tpt scripture-chronology check` | 0 | coverage table current, 1880 rows |
| coverage | `tools/tpt scripture-chronology coverage` | 0 | 35 809 verses, 1880 runs, 12 541 dated, 16 504 composition-only, 6 764 undated-in-tradition |
| manifest completeness | `scripts/check_final_acceptance_manifest.py` | 0 | 156 rows / 156 cases / 121 production-diff cases / **218 of 218** prior review ids |
| duplicate-key gate | the regression test | 0 | OK, and it fails when the check is neutered on a copy |
| promised deliverables | `tools/tpt check-promised-deliverables` + tests | 0 | ledger valid, 31 tracked, 22 complete |
| source reader | `check`, `structure --check`, tests | 0 | green; projection current, 2358 files |
| projection / versification | per-module | mixed | projection, loci, psalms, psalter, deuterocanon, coverage all OK; recensions and index_bible fail, both inherited |
| full suite | `python3 -m unittest discover -s tools/tests` | 1 | **1830 tests, 36 failures** |
| check-examples | `make check-examples` | 2 | 221 captured, 212 replayed, **4 diverged** |
| tmt check | `tmt check` | 1 | 8 undeclared sibling uses |
| make -k check | `make -k check` | 2 | 4 failing targets |

**Failure names were compared, not counts.** The 36-failure set is a **strict
subset** of the merge-base set at `22528396a` (37). The one base-only failure is
absent at HEAD. **0 introduced, 1 removed.** Test count 1830 against the base's
1736 is exactly +94, the chronology module. Failing modules are
`test_public_alpha`, `test_index_bible`, `test_mass_ordinary`,
`test_calendar_rubrics`, `test_commentary_index`, the three reader-integration
modules, `test_recensions`, `test_document_library`, the two liturgy-reader
modules and `test_tool_registry`. **Chronology-related failures: zero.**

`tmt check`'s 8 are byte-identical to the baseline log, and
`scripture-chronology` is not among them. `make -k check`'s four targets are the
baseline's four, and `check-scripture-chronology` passes inside it.

**One correction to the repair report.** Its `check-examples` "identical
divergence set" is wrong as stated: HEAD diverges on 4 invocations
(`calendar-spine:46`, `tpt:78`, `tpt:87`, `tpt:99`) where the merge-base diverges
on 6. HEAD is a strict subset, and it is not identical to the prior branch log
either, which recorded 6. Nothing new diverges and the count moved down twice —
a reporting inaccuracy, not a corpus defect. All 11 captured
`scripture-chronology` examples replay `ok`.

`scripture-chronology build` was never invoked against the checkout; the only
`build` in the suite runs inside a `mktemp -d` sandbox with `--root`. The working
tree was clean before, throughout and after.

## Material findings

Each block: case, source, source locus, the final production assertion, the
defect, and the exact required correction. Ordered by severity.

### MF-1 — a rank-1 Scripture claim suppressed on the judgement of a declared non-authority

- **case** `event:israel.divided-kingdom.fall-of-samaria`, subject note (`events.yaml`)
- **source** `artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08654a-645bba6c` — Sloet, "Chronology of the Kings"
- **source locus** the paragraphs preceding Sloet's own table: "That these synchronisms are not historical, but must have been introduced into the Bible by a 'speculator', is proved by what follows"; and the table's Remarks column, "'Third year of Osee' is incorrect"
- **production asserts** "Sloet's 'Chronology of the Kings' argues at length that those Ezechias-Osee synchronisms are not historical and prints in its own table the remark that 'Third year of Osee' is incorrect, **so no relative claim is authored from them here**."
- **defect** A declared non-authority's critical judgement is the stated ground for authoring nothing from a rank-1 locus. The tracked Douay is not silent: `4Kings/18.json` v10 reads "And took it. For after three years, in the sixth year of Ezechias, that is, in the ninth year of Osee, king of Israel, Samaria was taken:", and `4Kings/17.json` v6 gives the ninth year of Osee. `israel.divided-kingdom.ezechias-accession` already exists and is already used as a relative anchor elsewhere. `profiles.yaml` says a lower rank is consulted only where every higher rank is silent and that a higher rank never yields to a lower; §4.3 excludes the authority relied on.
- **required correction** Delete the Sloet clause as a ground. Either author the rank-1 relative claim — "in the sixth year of Ezechias", relative to `ezechias-accession`, sourced `bible:douay-rheims:4Kings.18.10` — or, if authoring is out of scope for a repair lane, state the ground for the silence as the absence of an anchor for Osee's accession, which is true. Sloet's objection may remain only as a marked profile boundary.
- **severity** high

### MF-2 — a source's refusal to date is authored as a date, and is displayed

- **case** `event:israel.primeval.creation#1`
- **source** `artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04` — Howlett, "Biblical Chronology"
- **source locus** the opening of the section "Creation of the world": "At least 200 dates have been suggested, varying from 3483 to 6934 years B.C., all based on the supposition that the Bible enables us to settle the point. **But it does nothing of the sort.**"
- **production asserts** a `catholic-traditional-v1` claim, `disposition: disputed`, `precision: interval`, 6934 B.C. to 3483 B.C., label "varying from 3483 to 6934 years B.C."
- **defect** Two parts. (i) The passage is a refusal, not a claim: Howlett canvasses 200 proposals, rejects the premise of all of them, and in the same section asserts an "immense antiquity" of a different order entirely. A rank-6 work's refusal to date is not a rank-6 date. (ii) The claim's own note states the defect correctly — "they are not a Catholic chronology of the Creation and **must never be displayed as one**" — and then justifies retention with a sentence that has no warrant in the article: "Recorded as an interval because the article's own sentence is that the true date lies somewhere in that spread and Scripture will not narrow it." The article says the opposite. And the prohibition is broken in fact: `query Gen.1.1` returns the row beside Usher's 4004 B.C., both `disputed`, indistinguishable in kind.
- **required correction** Withdraw `israel.primeval.creation#1`. Move the quotation and its point into the event's subject note, which already opens "The subject the tradition dates least, and says so", or into a gap row scoped to Genesis 1. If the row is kept for any reason, strike the unsupported justifying sentence. No other ordinal on the event changes; `#0` is a different artifact and untouched.
- **severity** high

### MF-3 — Sloet's own table is an excluded reconstruction; six held claims rest on it

- **cases** `israel.monarchy.david-accession#1` (B.C. 1012), `israel.monarchy.solomon-accession#1` (972), `israel.monarchy.temple-begun#3` (969), `israel.divided-kingdom.division#2` (933-2), `israel.divided-kingdom.fall-of-samaria#3` (722-1), `israel.divided-kingdom.ezechias-accession#1` (718-7)
- **source** the same Sloet artifact
- **source locus** "Since the deciphering of the Assyro-Babylonian inscriptions, the chronology of the period of Kings before 730 B.C. has become untenable"; and "The table below gives the chronology of the kings of Juda and of Israel … in conjunction with the data of profane history"
- **production asserts** six live claims under `catholic-traditional-v1`, three of whose own bases say "harmonised with the Assyrian data"
- **defect** The table's declared method is the class §4.3 excludes, and the profile's reporting licence is granted to Ussher by name and to nothing else. The corpus withdrew Howlett's 958, "about 969", 936 and "about 937" on exactly this ground, and `temple-begun` now holds a 969 withdrawn from one author and retained from another. Its own note concedes the gap: "which this lane did not rule."
- **required correction** Withdraw the six, recording each in its event's subject note in the shape already used for the withdrawn Howlett figures. Do **not** re-dispose them as `alternate`: the profile has no comparison-only disposition. Consequentially, `david-accession`, `solomon-accession` and `ezechias-accession` each fall to a single Petavius claim and must move `disputed` → `preferred`; three event notes asserting "two figures … apart" must be rewritten; and `division#0`'s note, which rests its preference partly on "The only competing figure now held is Sloet's own table at B.C. 933-2", must be rewritten because it would name a deleted claim.
  **The ten claims resting on the Petavius table reproduced in the same article are admissible and must not be touched.** Production's own basis strings already draw that line.
- **severity** high

### MF-4 — a binding scope that returns a factually wrong answer

- **case** FA-005, binding group `narrated-event -> life-of-christ.crucifixion`
- **source** `bible:douay-rheims:Matt.27.52`, `Matt.27.53`
- **source locus** `src/sources/bibles/douay-rheims/chapters/Matt/27.json` v53: "And coming out of the tombs **after his resurrection**, came into the holy city and appeared to many."
- **production asserts** `query Matt.27.53` returns seven Crucifixion dates, every one marked `direct`
- **defect** A verse whose own words place its action after the Resurrection is answered with the dates of the Crucifixion, unqualified. The binding carries a note disclosing the difficulty and stating that the scope is deliberately not cut, but a binding's `note` and `sources` reach no consumer — neither renderer prints them — so the disclosure is review prose only. The scope is also reported as `direct` rather than `inherited`, because the inheritance test is `span.first is None and span.last is None`, which a 22-verse range fails.
- **required correction** Cut 27:53 out of the scope: `{first: 33, last: 52}` and `{first: 54, last: 54}`. Optionally bind 27:52-53 to a claimless event. Separately, fix the `inherited` test for verse-range binding scopes (composition uses `or` and is correct; bindings use `and`).
- **severity** medium-high — this row is `not-previously-reviewed`

### MF-5 — the manifest's two provenance columns are ordered oppositely

- **case** the review apparatus, `scripts/build_final_acceptance_manifest.py:245-246`
- **production asserts** `";".join(sorted(set(case["ranges"])))` against `";".join(dict.fromkeys(case["why"]))`
- **defect** `sorted()` puts `214797e78..eb38161ba` before `2330d63a5..214797e78`; `why` stays chronological. **24 rows carry both ranges** and therefore pair the columns backwards. FA-051 shows it on its face: `changed:note;withdrawn` — a claim cannot have its note changed after it was withdrawn. It does not affect the completeness proof, which keys on `case_type + ":" + claim_or_scope_id`, but it misattributes every change in 24 rows in the one artifact the cold reviewer is told to work from.
- **required correction** `";".join(dict.fromkeys(case["ranges"]))`, then regenerate.
- **severity** medium

### MF-6 — the completeness guarantee is stronger than the mechanism that proves it

- **case** `scripts/chronology_review_diff.py` and `scripts/check_final_acceptance_manifest.py` (FA-086..FA-089)
- **defect** The manifest header says the checker "fails on any changed case this file omits". The differ is blind to: a binding's `note`/`sources` whenever its scope also changed (3 groups here, reported only as `scope-changed`); **event and unit fields entirely** — `WORKER` dumps only `event.claims`/`unit.claims`, hiding 11 event-note rewrites and one unit scope+title change, and an event or unit added or removed with no claims would be wholly invisible, a shape the corpus now holds two of; `profiles.yaml`, never compared; the tracked bibles, symlinked and only warned about. The corpus's own flagship correction — the Mark 15:33 misquotation in the Crucifixion **event** note — produces zero rows from the differ and reached the manifest only because three humans recorded it as prior findings.
- **the corpus is nevertheless complete**: claims 73/73, bindings 11/11, gaps 6/6, and 83 of 84 raw diff hunks map to a manifest row with the 84th comment-only. **No unexplained changed factual state exists outside the manifest.** But it is complete by human diligence, not by the cited mechanism.
- **required correction** Report binding fields unconditionally; add a subjects section emitting event/unit `title`, `parent`, `scope` and `note`; add a profiles section; put the bibles in `diff_sources`. Until then, amend the manifest header and the two docstrings so they claim what the apparatus actually proves.
- **severity** medium — it is the guarantee, not the corpus, that is overstated

### MF-7 — the profile boundary is unsettled in the contract, and applied inconsistently

See the profile section. Five claims outside the review surface hold a
modern-critical or Assyriological figure in `preferred` position, three of them
disclosing it in their own notes. The rule the corpus actually applied is stated
nowhere. **The contract must be corrected before the claims are**, or the next
lane will re-derive the same inconsistency.
- **required correction** State the author's-method test in §4.3 and in
  `profiles.yaml`'s `non_authorities` entry: a ranked Catholic source's rank
  attaches to what it transmits from the tradition, not to a reconstruction its
  author builds on excluded method, and no reporting licence covers it because
  §4.3's is granted to Ussher by name and to nothing else. Then apply it once,
  consistently, to Howlett, to Sloet and to these five.
- **severity** high (contract)

### MF-10 — the review record misattributes an article's author, five times

- **cases** FA-127 (`prior-finding:F-005`) and FA-097 (`undated-in-tradition @ Eccles`), both in this manifest; `post-audit-rereview-findings.tsv` RR-072; and `cold-audit-findings.tsv` / `post-audit-corrections.tsv` F-005
- **source** `artifact.catholic-encyclopedia.volume-5.new-york-1909.newadvent-05244b-2fe7b66b`
- **production asserts** the manifest's `source_locus` names the article's author as **"Hoberg (tr.)"**; the two cold-audit rows name **"Schumacher"**
- **defect** New Advent's own printed citation block reads *Gietmann, Gerhard.
  "Ecclesiastes." The Catholic Encyclopedia. Vol. 5. New York: Robert Appleton
  Company, 1909*, and the tracked artifact record carries that citation in its
  `notes`. Neither "Hoberg" nor "Schumacher" occurs anywhere on the page. The
  corpus itself is right — `gaps.yaml` names no author — so nothing factual is
  falsified; the wrong name is carried only by the review apparatus, which is
  what a cold reviewer is told to work from.
- **required correction** In `final-acceptance-manifest.tsv`, FA-127 and FA-097:
  `Hoberg (tr.), "Ecclesiastes", CE vol. 5 (1909)` → `Gietmann, …`. The three
  rows in the immutable ledgers should be corrected by a superseding note rather
  than rewritten, on the same principle the repair lane applied to line 9.
- **severity** minor

### MF-11 — the review apparatus does not watch itself

- **case** `scripts/chronology_review_diff.py` (FA-089)
- **defect** None of the differ's sections covers `src/sources/chronology/*.tsv`.
  Changing the seed line in `cold-audit-manifest.tsv`'s header on a clone
  produced **no report at all**. That header is the predicate that regenerates
  the cold audit's deterministic sample, and the reproduction check the
  post-audit lane promised for it does not exist at HEAD — nothing under
  `tools/tests`, `tests` or `scripts` mentions the seed. The header reproduces
  today; nothing would notice if it stopped.
- **required correction** Put the review TSVs under the differ, or add the
  promised reproduction check as a test.
- **severity** minor

## Promised-deliverable recommendations

### `translation-independent-identity` — **PASS**

All five criteria of the requirement, and the three additional checks the
acceptance brief names, were verified by construction rather than by reading the
tests:

| criterion | evidence |
| --- | --- |
| named-system ownership | four ownership positions in production (three `numbering:` declarations, all `vulgate`, and one `scope: {system: greek}`); **zero edition ids in an ownership position**, against ~1027 edition-id occurrences all of which are `sources:` or basis prose |
| Vulgate preference | `query Ps.51.5 --system hebrew` resolves to `Ps.50.5`, `mapping: shared`, and returns the Vulgate's own assertion; zero hebrew spans authored |
| native distinct chronology | `query Ecclus.1.1 --system greek` returns `composition-only`, "not long after … 132 B.C."; Gigot's article reopened |
| mapping refusal ≠ chronology refusal | both axes answer independently; and the **code was fixed first** (`392da1a29`, `_chronology.py` +529, the `.test` file untouched in that range), with the gate strengthened an hour later — not a test moved to match broken code |
| full-span gate | proved by building mixed-span fixtures: the replayed pre-fix predicate admits them, HEAD refuses them and names the interior verse; a control with the same span and a different date correctly loads, so the gate refuses a duplicated fact rather than a safe correspondence |
| unknown-system typed refusal | `douay-rheims`, `knox`, `vulgate-clementine`, `septuagint` all return `not-alignable`, exit 1 |
| Hebrew Psalm safe-sharing refusal | vulgate Ps 51 is the Saul superscription, hebrew Ps 51 is the Miserere and resolves to Ps 50; number-identity sharing would be wrong at 2380 of 2528 loci |

Two `CHANGES_REQUIRED` were found in this area and neither defeats the criterion:
a `--json` exit-code regression (`query` with `--json` exits 0 where the plain
form exits 1), and a latent parameter-rebinding leak in `_scope` that no
production scope triggers. Both should be fixed; neither is evidence that
chronology identity rests on translation editions.

### `exhaustive-coverage` — **PASS**

The universe reproduces independently. Computed from `book-index.tsv`, the
Clementine chapter JSON, `psalm-numbering.tsv`, `deuterocanon-numbering.tsv` and
the three witnesses' `verse-text-*.tsv`, **without importing the loader**:

```text
Vulgate primary                        35,809
  (cross-check: globbing every Clementine chapter file, ignoring
   the index, gives 35,809 as well)
greek     printed 2,156 − shared 800                    + 1,356
hebrew    printed 2,528 − shared 2,528                  +     0
world-english-catholic
          printed 2,094 − shared 730 − already counted 1,358  +     6
                                                       -------
declared universe                      37,171
```

Every intermediate matches `coverage --json` exactly. No alias double-counting:
the 6,221 alias rows are read by `_projection` and `_psalter` only, by no code on
the universe path, and the expanded coverage table has zero duplicates and an
empty set difference against the Clementine's printed verses in both directions.
`hebrew +0` is right three ways — structurally (the psalm concordance is
validated on read to tile all 150 psalms with equal run lengths, so it cannot
yield an unmapped hebrew locus), by policy, and empirically across all 2,528.

Every supported locus reaches exactly one typed status, the six categories the
criterion names are reported, and no headline percentage is printed. The seven
native `research-pending` loci are honest: the corpus holds exactly one native
scope and no native gap row, all seven return empty assertion lists, and no date
was invented to close them.

**On the stricter reading:** the criterion requires a research-**gap category**,
not an empty one. The 2026-08-27 ledger note ("stays open while any locus is
`research-pending`") imposes a test the criterion as written does not carry. If
the maintainer intends that stricter rule, the criterion must be amended to say
so rather than enforced from a note.

### `independent-source-audit` — **KEEP OPEN**

This review is genuinely cold and reviewed all 156 cases, and it satisfies the
procedural half of the requirement. It cannot close it, because the requirement
closes only when the independent disposition is PASS, and it is not:
material factual and profile defects remain (MF-1 through MF-4), the contract
that would make the largest defect class reproducible is unsettled (MF-7), and
the apparatus that proves the acceptance surface complete is weaker than its
stated guarantee (MF-6).

### `scripture-chronology-corpus-2026-08-26` — **IN_PROGRESS**

Two of the three open requirements are recommended to pass. The third is not, so
the deliverable is not complete. Per the acceptance brief, the overall
deliverable is not partially called complete.

## Overall disposition

**CHANGES_REQUIRED.**

Not because the corpus is unreliable in bulk. Most of it survived a hostile
reading: the Flood-to-Call correction is right and was proved right from the
article's own table cells; the duplicate-key gate is a real parse-time refusal
that bites when neutered; the claimless-event contract and the loader agree on
all five limbs; the stub that could have poisoned the whole evidence base turns
out to have poisoned nothing; the coverage universe reproduces exactly from the
data without the loader; the named-system criteria all hold, and the code was
fixed before the test rather than the test moved to match the code; structural
validation introduces no regression at all; and no unexplained changed factual
state exists outside the manifest.

It is `CHANGES_REQUIRED` because a small number of defects are of a kind that
acceptance cannot absorb:

1. **A rank-1 Scripture claim is suppressed on the judgement of a declared
   non-authority** (MF-1). This inverts the profile's central rule, in the
   corpus's own prose, where a reader will read it as the reason for a silence.
2. **A source's refusal to date is authored as a date, and displayed** (MF-2).
   The record itself says it must never be displayed as one.
3. **Six claims rest on a table whose author declares its method to be the one
   the profile excludes**, while the same figure was withdrawn from another
   author on that ground (MF-3).
4. **A verse is answered with the date of an event it says happened
   afterwards** (MF-4), on a row nobody had reviewed before.
5. **The contract does not settle the question the largest defect class turns
   on** (MF-7), so that class is not reproducible by a second reviewer — which
   is the one thing `independent-source-audit` exists to guarantee.

The corrections are bounded and mostly small. What they are not is optional: four
of the five are wrong answers a consumer can reach today with a single query.

## Appendices

Three appendices accompany this report, each a table rather than prose:

| appendix | holds |
| --- | --- |
| `final-acceptance-findings.tsv` | all 156 cases, PASS rows included |
| Howlett | all 46 retained claims citing `newadvent-03731a-f5f96f04`, with the grounding sentence quoted, the source voice classified, and the admissibility ruling |
| Sloet | all 16 claims citing `newadvent-08654a-645bba6c`, split into the 10 resting on the Petavius table and the 6 resting on Sloet's own |
| stub evidence | every conclusion in the review record that could have depended on `.scratch/cold-audit/src.py --bible`, and the result of re-resolving it through the real machinery |

### Source-voice vocabulary used in the Howlett appendix

```text
howlett-own-assertion     he asserts the figure himself
reports-ussher
reports-modern-critical   Sayce, Driver, Wellhausen, Assyriological or
                          Egyptological data, "critical scholars"
reports-other-catholic    Mangenot, Sloet, Vigouroux, another Catholic chronologist
contrast-of-schemes       traditional and modern set side by side, neither adopted
scripture-restatement     restating what the sacred text itself says
```

### On the durability of the evidence

144 distinct source records are cited by the corpus and all 144 are registered —
no dangling reference. 127 are `artifact` records with `storage = "remote"` and
`rights_status = "restricted"`: the bytes are deliberately not retained, because
New Advent's transcription carries a site copyright. 17 are `passage` records
over the Haydock PDF, whose pages are retained.

Of the 127, twelve have no retained text extraction either, so their evidence of
record is `source_url` + `sha256` + `byte_size` and nothing more. The extractions
that do exist live under `.scratch/`, which is untracked and which `wt tidy`
deletes without asking.

Every claim this review turned on was reopenable today, and most were reopened
twice — against the retained extraction and against a live refetch. But a
reviewer with a fresh clone and no network has no evidence at all; a reviewer
with a fresh clone and a network must refetch, and two registered hashes already
do not reproduce (MF-8). This is a consequence of the rights position rather than
a defect in the corpus, and it is recorded as an observation, not as a
`CHANGES_REQUIRED`. It is worth a maintainer's decision before the corpus becomes
a canonical dependency, because the acceptance evidence is less durable than the
acceptance record implies.

## Next safe lane

One bounded correction lane, containing only the enumerated failed cases and
nothing else, followed by another genuinely cold targeted review of every changed
case.

**Order matters.** Do the contract first:

1. **`guidance/scripture-chronology.md` §4.3 and `profiles.yaml`** — state the
   author's-method test (MF-7), and state the Ussher-only reporting licence as
   text rather than leaving it as the silence the corpus already cites as if it
   were text. Nothing else in the queue is reproducible until this is settled.
2. **`guidance/sources.md` routing and §15.1** — add the §15.1 entry for
   `overbroad-silence-on-partial-evidence`, cross-reference the sources.md
   paragraph, say that the bound governs gap-row `reason` prose and not only
   `notes`, and add an `AGENTS.md` routing row for negative and silence claims.
   Fix §15.1(1)'s `_bible` pointer, which names a module that has never existed
   on any branch.

Then the factual corrections, each of which is small once the contract is fixed:

3. MF-1 — the `fall-of-samaria` suppressed rank-1 claim.
4. MF-2 — withdraw `israel.primeval.creation#1`.
5. MF-3 — the six Sloet claims, and the four consequential note and disposition
   edits they force. **Do not touch the ten Petavius claims.**
6. MF-4 — cut Matt 27:53 out of the Crucifixion binding scope.
7. The wording of the Gen, Num, Ex and Lam gap rows; the Leviticus "nowhere at
   length" clause; FA-042's stale count; FA-066's Abdias second opinion;
   FA-118's omitted index entry and the same omission where it is reproduced in
   `gaps.yaml`; FA-121's five letters.
8. The apparatus: MF-5's column ordering, MF-6's differ blind spots and the three
   overstated docstrings, MF-8's cache naming and the two non-reproducing hashes.

**Then apply the same rule to what this review found outside the surface** — the
five `preferred` modern-critical figures, the Zacharias whole-book range that
harmonises two source claims into a third, and the uncited Jerome and Eusebius
quotations. These are not repair-lane failures; they are the same classes,
uncorrected, and they will be re-derived by the next reviewer if left.

**Do not merge, and do not begin the propers-consumer integration lane.** The
chronology corpus is a canonical factual dependency for every future proper,
which is the reason this gate exists.

**What should NOT be reopened.** The Flood-to-Call correction, the duplicate-key
gate, the claimless-event contract, WD-A4-017, the six new article records, the
named-system criteria, the coverage universe, and the structural gates all passed
a hostile reading. Reopening them would cost more than it can find.
