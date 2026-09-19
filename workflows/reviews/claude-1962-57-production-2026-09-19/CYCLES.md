# Every cycle the Claude Seventeenth Sunday production entered

Run `1e02dc05f2df9940`, `proper-study` v3, provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`,
date 2026-09-20. Seeded at commit `72616eb9c`, terminal disposition
**ACCEPTED**. 86 packets, 86 accepted results, 3 interventions. The engine's
own record is archived in the leaf under
`evaluations/proper-study-results/1e02dc05f2df9940/`; this file is the
driver's account of why the run went round, which the run directory does not
state.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 5 | 3 |
| study-review | 8 | 5 |
| synthesis-review | 5 | 2 |
| homily-review | 6 | 3 |
| visual-review | 2 | 1 |
| artifact-gates | 3 | 1 |

Sixteen cycles in all: fifteen driven by a review finding and one by a
mechanical seal. No stage ever exhausted a budget. The closest approach was
`study-review` at three consecutive purely-novel failing rounds against
`max_novel_iterations` of four — one round short of the stop that hands the
decision to a person.

## The cycles, in order

| # | Stage that found it | Owner it went to | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | A negative search of the 1894 Gelasian that was false; a Gregorian Supplement locus mis-cited in five places; an anagogical sense resting on two verses this Mass does not sing; a printed oration conclusion over-read as significant |
| 2 | research-review 1 | research | The Postcommunion's other occurrence in the Missal misattributed to the Second Sunday of Lent — the page's running head had misled the researcher |
| 3 | research-review 2 | research | Prose added by the previous repair invented a difference between Theodoret and Chrysostom, the ellipsis in its own quotation of Chrysostom hiding the agreement |
| 4 | study-review 0 | research, then study | Two dossier fields the bound encyclopedia supplies were missing; separately, the comparison claimed all three readings cite Trent when the second never mentions it |
| 5 | synthesis-review 0 | synthesis | Pruned references dropped two loci the text relies on and kept three it no longer uses |
| 6 | homily-review 0 | homily | The opening denied the Pharisees the answer the Gospel gives them, and the speech contradicted itself later; a patristic locus off by one paragraph |
| 7 | homily-review 1 | homily | A philological turn on the Collect that the leaf's own records, the Augustine gloss beside it, and both companions contradict |
| 8 | homily-review 2 | homily | The sentence that replaced it disclaimed a compiler's intention in reader-facing prose, which the amended profile forbids |
| 9 | artifact-gates 0 | study | Not a defect in any document: deriving the companion had extended the shared `format.tex`, staling the study's content seal. The whole chain re-ran |
| 10 | visual-review 0 | study | Running heads overprinting on page 20; the References section carrying the appendix's running head |
| 11 | study-review 3 | study | Chrysostom's reciprocity glossed in one direction only, contradicting the leaf's own homily |
| 12 | study-review 4 | study | A psalm citation introduced by that repair: the words are Vulgate 13:1, cited as 53:1 |
| 13 | study-review 5 | study | The contribution record claimed an audit update that the same iteration had drafted and reverted |
| 14 | study-review 6 | study | Augustine's sentence quoted without the member carrying its antithesis, leaving an unqualified denial that the Word and the flesh are one |
| 15 | synthesis-review 3 | synthesis | Compression turned the Introit's whole verse plus half-verse into "two half-verses", contradicted by the next clause |

## What the cycles were actually made of

**Six of the fifteen were created by the repair of an earlier finding.** Not
by carelessness: a repair is new material in a dense document, and the next
cold reader reads it. Cycle 3 came from an advisory that asked for a witness
to be added; cycle 12 from printing the proof texts that cycle 11 required;
cycle 13 from the record written for an edit that the same round correctly
reverted; cycle 15 from the compression that paid for propagating cycles
11–14 into the companion. One advisory in the concise document was introduced
by a previous review's own prescribed wording.

**Two came from the boundary between owners, not from the documents.** Cycle
9 was a mechanical seal, correct in principle — a content review is valid only
over the bytes it read — costing a full re-author and re-review of all three
documents for two LaTeX environments the study never invokes. Cycle 4 split
across two owners, and the finding for the later owner waited as a carried
finding while the earlier one was repaired, which is the engine working as
designed.

**Everything else was a real defect in the work**, and the ones that matter
most were invisible to every mechanical gate: a false claim of having searched
a source, an invented disagreement between two Fathers, a quotation truncated
into a doctrinal error, a homily telling an assembly something its own records
deny. No page-count check, log check or component check can reach any of them.

**The advisory channel carried weight it was not designed to carry.** Across
the run, reviewers filed 60 distinct advisories against 21 distinct blocking
findings, 20 of them from a review and one from the artifact gate's seal check. Authors
cleared most of them while already in the files, which is what the channel is
for. Two remain that no stage in the run could clear because they belong to a
reviewed research record: Aquinas is absent from the interpretation audit
though the manifest and the study develop him, and the Augustine clause the
study now turns on is not transcribed into the research records. The evidence
for both is present and verified. They are recorded in the leaf's
standing-findings file, in intervention 0001, and here.

## What was repaired in the workflow because of this run

Recorded in full in the commit that carries them; each is pinned by a test in
`tools/tests/test_workflow_advisory_ownership.py`.

| Defect | Evidence from this run |
| --- | --- |
| An advisory died when a *different* evaluator passed | Three study advisories never reached the author who owns their files |
| The review schemas refused the `accepted` severity their own packets document | A reviewer followed its packet and had its whole submission refused |
| `proper-study` scoped no re-read, where the older pipelines scope theirs | Three consecutive purely-novel review rounds, one short of the stop |
| A run's own standing-findings record made derived PDFs stale | Installation retypeset two documents and moved the clock in a sealed log |

One further gap is recorded and not repaired: the chronology tools read data
files that the engine neither seals nor lists, so each leaf must trace them by
hand. Three reviewers raised it; the leaf now declares them itself, and the
last research reviewer traced every file the tools open and found all of them
inside the seal. The fix is a design choice between sealing those inputs with
the computation code and having the tool print what it opened, and it is the
owner's to make.

## The host deviation

Every stage ran as a fresh Claude Code harness subagent, which inherits the
driver session's reasoning effort of `xhigh`. Stages whose packets declare
`high` — every author stage — therefore ran one level above their declared
effort; the `xhigh` reviews ran exactly at theirs. No stage ran below its
declared level. A pinned-effort subagent definition could not be loaded
without restarting the host session, and headless workers at an explicit
effort were refused by the host's permission policy. Intervention 0000 records
this against the run.
