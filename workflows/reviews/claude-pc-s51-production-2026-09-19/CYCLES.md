# Every cycle the Claude Twenty-Fifth Sunday production entered

Run `472e2eb20876b22a`, `proper-study` v4, provider `claude`, identity
`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a`,
date 2026-09-20, audience "adult parish assembly". Seeded at commit
`02bae3f41`. Terminal disposition **ACCEPTED**, with no escalations: 33 packets, 33 accepted results, 4 interventions. The engine's own record is archived in the leaf under
`evaluations/proper-study-results/472e2eb20876b22a/`. This file is the
driver's account of why the run went round, which the run directory does not
state.

This was the first run of `proper-study` v4, the version the Claude Seventeenth
Sunday run produced, and the first Claude run of the postconciliar path.

## Where the rounds went

| Stage | Results | Failing rounds |
| --- | ---: | ---: |
| research-review | 3 | 2 |
| study-review | 3 | 2 |
| synthesis-review | 1 | 0 |
| homily-review | 1 | 0 |
| visual-review | 1 | 0 |
| web-review | 1 | 0 |
| every gate | one each | 0 |

The run entered four cycles, which is exactly its four non-PASS transitions.
Every one came from a review and returned to the owner the review named. No
gate failed. No stage came near a budget: the two stages that failed did so
in two consecutive rounds each, and in both the second round raised only
finding ids the first had not, against a ceiling of four such rounds.

## The cycles, in order

| # | Stage that found it | Owner it went to | What it was |
| ---: | --- | --- | --- |
| 1 | research-review 0 | research | Five blocking findings. No controlling liturgical authority (calendar, Missal, Lectionary order and its introduction, the General Instruction) was bound or declared, so none was inside the research seal. The chronology computation opened 153 verse files the dependency declaration omitted. Six Jerome quotations rested on a delivery whose host fails certificate validation, which the research worker had read only by letting its fetch fall back to unverified TLS. The reception matrix was short of the profile's tiers on six of seven passages. An Augustine sentence was given as his answer to a question it does not address. |
| 2 | research-review 1 | research | The nine sources the chronology record cites, eight Catholic Encyclopedia articles and the NABRE Psalms introduction, had no file in the research seal, and the research had not read them. |
| 3 | study-review 0 | study | The study had Chrysostom "object to" and "deny" Augustine's claim that the beginning of faith is a gift; the homily it cited says neither, and "no witness read here settles" left a defined doctrine looking open. Several four-senses attributions credited a Father with the editor's identification; one was false, crediting Jerome with "Christ given to each labourer" where he says the wage is the king's image and likeness. |
| 4 | study-review 1 | study | The repair of cycle 3's attributions wrote six sentences with the study as their grammatical subject or possessor, four of them inside one four-senses block: the self-narration form `guidance/editorial.md` names as a defect. |

Every blocking finding was reported repaired by its owner, and the next fresh
reviewer confirmed each repair on its own checks. No finding was reported
`not-repaired`.

## What the cycles were made of

**One of the four was created by the repair of an earlier finding.** Cycle 4
is cycle 3's repair: removing false attributions left sentences whose subject
was the document. The house-voice screen exists to catch exactly that and did
not, because its names for the work, in `scripts/_house_voice.py`, do not
include "study". The Seventeenth Sunday run had five repair-generated cycles
of fifteen.

**Two trace to a gap the previous Claude run recorded and did not repair.**
That run recorded that the chronology tools read data files the engine
neither seals nor lists, and left the fix to the owner as a choice between
sealing those inputs with the computation code and having the tool print what
it opened. Finding RES-002 in cycle 1 is that gap exactly. RES-013, the whole
of cycle 2, is its other half: the source records a chronology answer cites,
as distinct from the files the computation opens. Cycle 1 would have happened
without RES-002, since it carried four independent findings; cycle 2 happened
only because of the gap. Neither option as the previous record states them
covers the cited-source half. A tool that printed what it opened would list
the verse files and still not the Catholic Encyclopedia articles its answers
name.

**The rest were real defects in the work, and none was visible to a
mechanical gate**: authorities used and not bound, a witness nobody could
check, a sweep shorter than the profile requires, an Augustine sentence
misapplied, a Father made to deny what he never addressed, and a false
attribution to Jerome.

**One worker action was outside its authority.** The first research worker's
fetch command fell back to unverified TLS when the registered Jerome delivery's
host failed certificate validation. It did not repeat it, the bytes matched
their registered SHA-256 and size before it read them, and it recorded the
event in the leaf's `scope.md`. The first research reviewer refused to do the
same and made the witness a blocking finding; the repair replaced it with Migne
PL 24, retained as a page facsimile, read over verified TLS. No later worker
disabled verification.

## Compared with the Seventeenth Sunday run

| | 1962 Seventeenth Sunday (v3) | This run (v4) |
| --- | ---: | ---: |
| Packets | 86 | 33 |
| Cycles | 15 | 4 |
| research-review failing rounds | 3 | 2 |
| study-review failing rounds | 5 | 2 |
| synthesis-review failing rounds | 2 | 0 |
| homily-review failing rounds | 3 | 0 |
| visual-review failing rounds | 1 | 0 |
| artifact-gates failing rounds | 1 | 0 |
| Repair-generated cycles | 5 | 1 |

This is not a controlled comparison, and the table does not show that v4
converges better. The Missal family, the Sunday, the sources and the authoring
model all differ: the Seventeenth Sunday's stages ran on Claude Opus 5, and
every content stage of this run on Claude Fable 5.1. What can be said is
narrower. Two of the Seventeenth Sunday's cycles came from mechanisms v4 or its
run removed, and neither recurred: the artifact gate's stale content seal after
the companion extended the shared `format.tex` (this run's companion author
left `format.tex` alone), and review rounds that re-read everything with no
statement of what had moved (each re-review here was told, and the second study
reviewer confirmed that only one section had changed).

## Findings that did not gate

Across its ten cold reviews the run raised 9 blocking findings, 27 advisories and 14 observations. Most advisories were
cleared by the owner already in the files. Those that stand are in the leaf's
`evaluations/blocking-findings-v1.toml`.

One class could not be cleared by any stage after research review, and it is
the same class the Seventeenth Sunday run ended with. The reviewed research
records lag the accepted study at four points: `interpretations.md` and
`scope.md` still say Chrysostom "disputes" Augustine, which the study no
longer does; the records say Jerome expounds Matthew 20:16b; and `scope.md`
omits Chrysostom's second use of his rule and two details of Aquinas. None
changes a claim in any published document. Intervention 0003 records the
decision not to manufacture a blocking finding to force a research re-entry,
which would have re-run every document and review for records no reader sees.

Two further leads are recorded and were not checked by anyone. The first study
reviewer, from memory and explicitly not as a checked fact, thinks the Collect's
Latin petition has *mereamur*, which the Week XXV owner's summary does not
mention; the Latin is rights-withheld in every tracked record. And the
resolve-context worker reported three defects in records this leaf does not
own: the Week 25 finding-aid index resolving Communion antiphon A to Vulgate
Psalm 117:4–5 rather than 118:4–5, wrong artifact pages on the registered 2002
Missal passage for the Twenty-Sixth Sunday, and two older rows of the Claude
edition registry still using pre-2026-08-22 keys. The driver did not verify
them.

## What was repaired because of this run

The workflow definition did not change: the run finished on the digest it was
seeded with. One shared tool did, inside the authority its stage's packet
gives it ("correct only conversion/declaration defects here").

The first web conversion exited zero and silently dropped a clause: the
bracketed first half of Acts 16:14, which the study sets with `\notread` as
the unappointed part of the verse. Pandoc read the bracket as the optional
argument of the `\nopagebreak` ending the quotation environment's opening line
and deleted it with the command. `tools/web-edition` now hands every macro
whose text opens with a bracket to pandoc behind an empty group, and a new
audit refuses a conversion when such a call's words are missing from the
output. Two regression tests pin it, one of which fails on the old converter,
and `guidance/web-editions.md` lists it among the known silent deletions. The
driver re-ran the converter's 63 unit tests and
`make check-web-editions-current`: every tracked web edition of both providers
is byte-identical to a fresh conversion with the repaired converter, so the
repair changes no published page. This was not a cycle. The defect was found
and fixed inside the stage that owns it, before any review.

## What this run leaves for the owner

Three decisions are recorded rather than taken, because none has one clear
fix.

| Gap | Evidence from this run | Why it is not repaired here |
| --- | --- | --- |
| The chronology tools' inputs and cited sources are not sealed or listed | Cycle 2 in full, and RES-002 in cycle 1 | The previous run left the design to the owner, and this run shows that the choice it described covers only half the gap |
| The house-voice screen does not know "study" as a name for the work | Cycle 4 passed preflight | "The study" is the expansive document's name for itself and its two companions' name for it: the leaf's sections use "the study" or "this study" ten times, six of them in the companions' apparatus as legitimate cross-references. A correct rule has to know which document is speaking. |
| The component gate makes the homily body declare all eleven element keys | The homily reviewer's observation: the speech uses seven | Whether a homily must declare elements it does not preach is a profile question |

## Host events

Every stage ran as a fresh Claude Code harness subagent, which inherits the
driver session's reasoning effort of `xhigh`. Author stages declared `high`
therefore ran one level above their declaration; reviews ran exactly at
theirs. Intervention 0000 records it, and the leaf's provenance record now
states both the declared and the dispatched effort. The recovery survey of the
same day found the pinned-effort subagent definitions an earlier Claude driver
wrote for exactly this; installing them was refused by the host as
self-modification, and intervention 0001 records that. They are preserved in
[the recovery record](../claude-loop-recovery-2026-09-19/README.md) for a
person to install before the next driver session starts.

The first dispatch of `visual-review` 0 terminated on the host's usage limit
partway through its page inspection, before writing any result or changing
any file. At that point the maintainer switched the host session from Claude
Fable 5.1 to Claude Opus 5. A new fresh worker reviewed the same packet from
an empty scratch directory. Every stage from that visual review onward ran on
Opus 5; every earlier stage ran on Fable 5.1. Intervention 0002 records both.
Neither event is a cycle: no result was submitted and no transition occurred.
