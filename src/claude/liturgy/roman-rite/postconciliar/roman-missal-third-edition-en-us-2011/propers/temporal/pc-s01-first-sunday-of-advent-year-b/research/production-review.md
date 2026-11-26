# Production and review record

## Author-study

Authored 26 November 2026 in `proper-study` v20, run `99f04ef5cf9b711b`,
seeded at commit `cbccbfcb3be4896c95225d8cd281e2b0684a12e9`, at iteration 0,
by `claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high). The canonical study is *The First Sunday of Advent,
Year B*, formula `PC-S01-B`: the First Sunday of Advent of the *Roman Missal*,
Third Edition, for the dioceses of the United States, with Lectionary no. 2,
for the occurrence of 29 November 2026. No prior, carried or advisory finding
was forwarded to the stage. The research review's standing advisory
RES-NEG-002 and its observation on the Isaiah Passage cell are recorded in
`evaluations/blocking-findings-v1.toml`; how the study observes them is stated
below. No research evidence record was changed at this stage.

### What the study contains

- **Opening** (`sections/00-opening.tex`): the *Ordo*'s title over the first
  reading, the Latin *Descendisti* that the United States English lacks,
  the standing notice on the study English and on numbering where Scripture
  first appears, the Gospel, psalm, letter and prayers in brief, the three
  questions with the authors who answer each, and a twelve-row map of the
  appointed texts (the solemn blessing marked optional), with the rubrics.
- **Appointed texts** (`sections/05-appointed-texts.tex`): the Douay–Rheims
  (Challoner) at every appointed Scripture text, with the words the
  Lectionary does not appoint in brackets (63:16a, 63:18–19 and 64:2 by note,
  the psalm title, v. 2b, v. 3a, vv. 5–14, v. 17, *Etenim*, Mark 13:32); Douay
  64:3 printed whole with the note of `propers/verified.md` finding 1; the
  psalm's *illustra*/*ostende* and v. 16b notes of finding 2; the antiphons by
  Latin incipit and description, their departures stated (owner finding 5) and
  their source verses printed as sources; the Collect, Prayer over the
  Offerings, Preface, Prayer after Communion and solemn blessing by incipit,
  description and short Latin phrases. One `\label{proper-<key>}` stands at
  each of the twelve keys, immediately after a heading naming only that text.
- **Each text in its setting** (`sections/10-texts-in-setting.tex`): what the
  books state about the relations (*Praenotanda* 67, 93, 123; GIRM 61–62;
  Universal Norms 39), the three *Ordo* titles, and each text's literary,
  textual and liturgical setting, including the Gelasian and Verona antecedents
  of the Collect, Prayer over the Offerings, Prayer after Communion and the
  Preface's close (owner findings 6–8), stated as agreements of wording.
- **Three interpretations**, each its own component, each with a section on
  where it strains and its own four senses, under the lane keys of
  `research/interpretations.md`:
  - `rend-the-heavens`, *Rend the Heavens and Come Down: The Cry Answered and
    Still Prayed*. Carrying authors Jerome, Augustine of Hippo, Cyril of
    Jerusalem, Thomas Aquinas. Developed: Jerome, *In Isaiam* XVII (cols.
    645–647, the promise, *Descendisti*, 1 Cor 2:9); Aquinas, *Super Isaiam*
    c. 64 (*dirumperes*, the three senses of *Descendisti*, *Occurristi*
    mystically of Simeon); Augustine, *En. in Ps.* 79.1–2, 9 and 84.9; Cyril,
    *Cat.* 15.1; supporting Bellarmine on Psalms 79 and 84, Chrysostom on 1
    Corinthians 1:7, Aquinas on 1 Corinthians 1:7, Gregory and Bede on the man
    gone abroad.
  - `watch-at-the-door`, *The Watch at the Door: The Hidden Hour and the
    Command to All*. Carrying authors Jerome, Augustine of Hippo, Gregory the
    Great, John Chrysostom, Bede. Developed: Jerome, *In Matt.* IV (cols.
    181–182), credited as Jerome's, with Bede named as transmitter only;
    Chrysostom, *Hom. in Matt.* 77.2–3; Augustine, *Ep.* 199.1.2–3; Gregory,
    *Hom. in Ev.* 13.3, 5 and 6 (and the homily on the talents, through Bede); Bede on Mark 13:34–37 (his own
    allotment); Aquinas on 1 Corinthians 1:8; supporting Bellarmine on Psalm 24
    and Augustine on Psalms 79 and 84.
  - `clay-and-faithful-potter`, *The Clay and the Faithful Potter: Our Failure
    and God's Fidelity*. Carrying authors Jerome, Thomas Aquinas, Augustine of
    Hippo, John Chrysostom. Developed: Jerome, *In Isaiam* XVII (cols.
    643–650: patience, *convertere … sive converte nos*, *ordo praeposterus*,
    Psalm 79:4 at col. 649, the potter and *Ne irascaris*); Aquinas, *Super
    Isaiam* c. 63–64 (*permittendo*, *de ira ad misericordiam* with Psalm 89:13
    and Lamentations 5:21, *praeposterus ordo*, Jeremiah 18); Augustine, *En.
    in Ps.* 24.2, 79.3, 84.9 and 84.15; Chrysostom, *Hom. in 1 Cor.* 2;
    Aquinas, *Super I Cor.* c. 1 lect. 1; supporting Bellarmine on Psalm 79 and
    Bede on Mark 13:34.
- **Comparison** (`sections/50-comparison.tex`): a table and two short
  paragraphs; the two disagreements (Jerome and Aquinas on *Descendisti*;
  Augustine and Bede on the reach of the command) kept as such.
- **Generated Scriptural Date and Location appendix**, then the **Liturgical
  Resolution** appendix with the branch IDs of `research/context.md`, the
  **Scope and Qualifications** appendix and **References**.

### Bounds observed

- *Descendisti* is presented as the Latin's (the *Ordo*'s 64:2b) and its
  absence from the United States English is stated in the opening, in the
  appointed-text note and in the first interpretation's strain.
- Jerome's comments on Matthew 24:36 and 24:42–43 are credited to Jerome; Bede
  is named only as having copied them under Mark 13:32–33. The identification
  of the man abroad and the sentence on the proper place of the flesh are
  credited to Gregory's homily on the talents, and *Vigilat qui …* to Gregory (Hom. 13.3). Gregory's
  three watches and Mark's four are not merged; Theophylact's four are not
  used.
- The psalm refrain's petition and Isaiah 63:17b are kept apart in wording and
  joined only as Jerome (col. 643) and Aquinas ([85023]) join them; no text is
  said to read "turn us" at 63:17.
- God is never made the author of sin; Jerome's patience and Aquinas's
  permission are kept as two accounts. The United States English's permissive
  63:17 and side-by-side 64:4 are described, and the hard forms are taught as
  the Latin's.
- Aquinas's *sine crimine* is given as his reading (without mortal sin) of the
  Latin Paul.
- Jerome's polemical sentences at cols. 644 and 647 and Chrysostom's sentence
  on those who refused the call are not used; the scope appendix says so.
- No liturgical commentator is cited (scope section 3.9). No other Mass of the
  present Missal is named except, once, the Mass for the sowing of fields that
  reuses the Communion antiphon (owner finding 2), and Monday of the First Week
  of Advent, which reuses two prayers (owner finding 3).
- No Scripture date appears outside the generated appendix; the study names
  the appendix by title and uses no `\ref{sec:date-location}`.
- RES-NEG-002 (advisory, research-owned): the study makes no claim that
  Theodoret, Theophylact or Hugh are unheld; its scope appendix names only
  Cassiodorus on Psalm 79, Cyril of Alexandria and Theodoret on Isaiah and
  Lapide on First Corinthians as not opened, and Theophylact only as read in
  the *Catena aurea* and not relied on. The research rows are left for
  their owner.
- The research observation on the Isaiah Passage cell (Clementine numbering
  in the generated table) stands; the scope appendix says the cell prints the
  Clementine numbering, and the prose gives both numberings throughout.

### Verification performed at this stage

Every Douay–Rheims verse printed or quoted was read in the tracked verse files
(Psalms 17, 24, 79, 84, 89, 143; Isaiah 63–64; Jeremiah 18; Lamentations 5;
Matthew 24–25; Mark 13–14; Luke 2, 12; 1 Corinthians 1, 2, 16), and the
Clementine Latin of Isaiah 63:17 and 64:1–8. The English quotations were
re-read in the tracked texts: Augustine, *En. in Ps.* 24 (lines 6850–6883), 79
(39602–39989) and 84 (41616–41672, 41844–41871), NPNF 1/8; Chrysostom, *Hom. in
Matt.* 77 (NPNF 1/10, lines 43018–43050) and *Hom. in 1 Cor.* 2 (NPNF 1/12,
lines 727–851); Cyril, *Cat.* 15.1 (verified passage record); Bellarmine on
Psalms 24, 79 and 84 (verified passage records). The Latin of Gregory (Hom. 9.1,
13.3, 13.5, 13.6) and Bede (on Mark 13:34–37) was re-read in the tracked
electronic texts. The Latin of Jerome (page images), Aquinas (Corpus
Thomisticum) and Augustine's letter 199 is quoted as the reviewed research
records give it and was not re-read at this stage. English renderings of Latin
are the author's.

No file or record of the other provider's leaf for this identity, its release
or production records, the 1962 First Sunday of Advent leaves of either
provider, or the GPT 1962 Advent production record was opened at this stage.

### Substantive length and pages

Measured on the author proof's text layer (running heads excluded): opening
1,443 words; appointed texts 2,250 (of which roughly 1,000 are the printed
Douay–Rheims); each text in its setting 2,451; the three interpretations
2,568, 2,823 and 2,585; comparison 724. Substantive exposition is therefore
about 13,800 words, above the profile's 6,000–10,000 planning range, which
the profile states is not a quota; the length comes from three fully
developed interpretations with their Fathers' reasons, not from repetition,
and reviewers may judge whether any passage should be cut. The terminal
matter adds the generated date appendix (1,023), the liturgical resolution
(966), the scope appendix (1,501) and References (729).

### Checks and proof

- `tools/tpt document-types refresh --leaf claude/<proper>` generated
  `main.tex` and `generated/scriptural-date-location.tex`; `--check` reports
  current.
- `scripts/_proper_study.py check … --phase content --edition research
  --require-presentation --require-format --require-authority
  --require-orientation --require-orientation-v3 --mode source`: pass.
- `check-content-preflight --edition research`: references-used (25 entries),
  identifiers-resolve, bindings-valid (67), restricted-not-reproduced,
  relation-coverage (3 lanes), unquoted-not-quoted, structural-meta-labels (90
  headings), house-voice, chronology-record-current,
  chronology-annotations-current, chronology-claims-supported and
  provenance-matches-run: all pass.
- Web probe: `tools/tpt web-edition --provider claude --output
  build/tpt-runs/99f04ef5cf9b711b/artifacts/author-study-0/web-probe <proper>`
  converted the study; all twelve `proper-<key>` anchors and the section
  anchors are present. The study prints no `\ref`, so the known
  `\ref{sec:date-location}` rendering defect does not arise.
- Author proof (informal, not requested by the packet and not a cold print
  review): `tools/print-document build --document publication:claude/<proper>
  --edition main` refused with "input has no existing file: …/synthesis.tex",
  because the companion is not yet written. The proof was instead compiled
  with `pdflatex` (three passes, settled, no overfull boxes) into
  `build/tpt-runs/99f04ef5cf9b711b/artifacts/author-study-0/proof/study.pdf`,
  with a proof-only revision stamp file in that directory: 31 physical pages,
  SHA-256 `5863c9004cb8d0737d6a7b31e097ed4b0f18a579c64bdf2127bbe78b7660383e`.
- `tools/tpt web-edition check --leaf claude/<proper>` (a later-stage gate,
  not study preflight) refuses for the same reason, "synthesis_entrypoint
  names a missing or empty file: synthesis.tex", until the companions exist.

### Shared defects for their owners

- `tools/print-document build --edition main` requires `synthesis.tex` before
  the companions exist, so the packet's suggested author proof cannot be made
  with the owning tool at this stage (tools owner).
- The generated Isaiah Passage cell prints Clementine numbering with no key
  (generator owner; the research review's standing observation).
- Bede's *In Marci evangelium* locus pattern admits only Mark 10 loci, so the
  Mark 13 binding has no locus (source-library owner; recorded in
  `research/source-bindings.toml`).

## Author-study, iteration 1

Revised 26 November 2026 in the same run, at iteration 1, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), against the study review's nine blocking findings
STU-001 to STU-009 and its advisories STU-010 to STU-014. Only the study's
section files, the generation record and this record changed; no research
evidence record, manifest, format or generated file was changed.

### What changed

- **STU-001.** The three subsections "The rest of the Mass in this
  interpretation" are gone. Their Fathers' contributions now stand where each
  interpretation's argument uses them. In the first: Chrysostom and Aquinas
  on 1 Corinthians 1:7, the Collect's *venienti* and the Prayer over the
  Offerings beside Cyril's two comings; Bellarmine on Psalm 84:13 with
  Augustine on the Alleluia verse's psalm; the solemn blessing with the
  Preface; Gregory and Bede on the man gone abroad. In the second: Bellarmine
  on Psalm 24 after Jerome's "suspended expectation"; Chrysostom on the
  impatient Corinthians after Augustine's bad servant; Gregory's *servat
  operando* beside the Collect; Isaiah 64:6 and the psalm's vow with Augustine
  79.11 after Gregory's definitions of watching; Gregory 13.6 (*Nolite …
  attendere quid habetis*) with the Prayer after Communion; Augustine 84.15 as
  a pastor after Bede's doorkeeper; the Preface's *vigilantes* after Bede on
  the last verse. In the third: the Collect's *Da* after Augustine 84.9; Bede
  on the servants' authority as grace, with the Prayer over the Offerings'
  *de tuis … collata beneficiis*, after Aquinas on God's faithfulness. At
  this iteration a text an interpretation did not use was left out of it or
  given a clause in its four senses. That policy was wrong: the profile
  requires every appointed element to contribute to each interpretation, at
  least by a clause, and the omissions it left (the Alleluia verse, Prayer
  over the Offerings and solemn blessing in the second interpretation, the
  Preface in the third) were repaired at iteration 2 (STU-016).
- **STU-002.** The narration of method and caution is removed from sections
  10, 20, 30, 40 and 50 (the "study's own reasoning" sentences, the forward
  maps and references, "stated as such", "credited to them", "keeps both
  answers without choosing", "kept as they stand"); the comparison row is now
  "Where the Fathers differ". The study's own links are stated once, in plain
  words, where they are drawn.
- **STU-003.** Texts and authors are the subjects only of what they do (the
  Gospel's "answer" in the opening, "holds" in the first interpretation,
  Cyril and the Preface, Jerome on the hidden face, the Entrance Antiphon in
  the third); the remaining instances went with the roll calls.
- **STU-004 and STU-005.** The emphatic fragments, the announced Andrew
  consequence (cut) and the restating closers are removed or rewritten as the
  finding gives them.
- **STU-006.** Aquinas's preferred literal sense of *Descendisti* is the
  descent that freed the people from Egypt everywhere it is reported (first
  interpretation, its strain, comparison table).
- **STU-007.** Chrysostom's Homily 2 on First Corinthians is given in its own
  order in the third interpretation (section 4's answers; section 5's "not
  even did this praise belong to them"; section 7 on v. 8; section 8 on v. 9),
  re-read in the registered passage `…ccel-web-2026-09-28.2.1cor-1.7-9`.
  Section 10 no longer reports his answers; it states the letter's rebukes
  and that Paul calls the Corinthians carnal (3:1).
- **STU-008.** The link between Cyril's unobserved first coming and Isaiah's
  torn heavens is stated once as the study's inference, beside Jerome's
  reading that the hidden coming answered the cry.
- **STU-009.** The Gospel's command is quoted as the *Ordo* opens it
  (*Videte, vigilate*: look, keep awake); a note under the Douay–Rheims of
  Mark 13:33 says that its "and pray" translates the Clementine *et orate*,
  which the *Ordo*'s opening does not show.
- **Advisories.** STU-010: the inaccurate Preface sentence went with the
  second roll call; section 10 states the change correctly. STU-011: the third
  interpretation's opening now matches its body. STU-012: the comparison
  credits Chrysostom with "not I" and Jerome with "not we", and calls only
  Jerome and Aquinas on *Descendisti* a disagreement. STU-013: the map rows for
  the Alleluia verse and Communion Antiphon give the Douay–Rheims, labelled,
  and the appointed-texts description of the Communion Antiphon no longer
  reads as English for it. STU-014: the scope appendix's chronology paragraph
  is a pointer to the generated appendix with the one qualification it does
  not print.

### Verification performed at this iteration

Re-read: Chrysostom, *Hom. in 1 Cor.* 2, sections 4–8 (registered passage
record); Gregory, *Hom. in Ev.* 13.6 (tracked Latin, for *Et cum certa mors
maneat omnibus … Nolite ergo attendere quid habetis, sed quid estis*); the
Douay–Rheims of Matthew 25:33. Every other quotation moved at this iteration
was moved with its existing wording and citation and was not re-read.

### Checks and proof

- `tools/tpt document-types refresh --leaf claude/<proper> --check`: current.
- `scripts/_proper_study.py check` (content phase, research edition, source
  mode, presentation, format, authority, orientation and orientation-v3
  requirements): pass.
- `check-content-preflight --edition research`, all checks including
  provenance-matches-run for this run: pass.
- Web probe into `build/tpt-runs/99f04ef5cf9b711b/artifacts/author-study-1/web-probe`:
  converted; all twelve `proper-<key>` anchors present once. The study
  prints no `\ref`.
- Informal author proof (not a cold print review), compiled with `pdflatex`
  in three settled passes with a proof-only revision stamp into
  `build/tpt-runs/99f04ef5cf9b711b/artifacts/author-study-1/proof/study.pdf`:
  30 physical pages, no overfull boxes, SHA-256
  `c899a0c9576885e4439e343ff770e1d03fb6413c7e032fc100f8f2174168ad79`.

### Substantive length

Measured on the proof's text layer with running heads and page numbers
removed: opening 1,408 words; appointed texts 2,242 (about 1,000 of them
printed Douay–Rheims); each text in its setting 2,182; the three
interpretations 2,149, 2,570 and 2,326; comparison 737; about 13,600 in all.
The iteration-0 proof measures about 14,570 by the same method. The study
remains above the profile's 6,000–10,000 planning range, which is not a
quota.

### Research defect for its owner

`research/interpretations.md` (Reading 1, literal sense) says the people
pray "that God come down as he once did at Sinai and in Egypt (Aquinas's
preferred literal sense)". Aquinas's preferred literal sense is the descent
to free the people from Egypt (`research/scope.md`, the Aquinas row); Sinai
is not his. The study now follows `research/scope.md`. The research record
was not changed at this stage.

### Remaining limitations

The printed United States Lectionary, its 1970 English at Isaiah 64:2, the
Hebrew of Psalm 80:16b, a named United States altar book, the *Book of
Blessings* in print, the antecedents of the solemn blessing and of the first
half of the Preface, and the source of the Entrance Antiphon's *exspectant*
remain unread (`research/scope.md` section 10).

## Author-study, iteration 2

Revised 26 November 2026 in the same run, at iteration 2, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), against the study review's three blocking findings
STU-015 to STU-017 and its advisories STU-018 to STU-022. Only the study's
section files, the generation record and this record changed; no research
evidence record, manifest, format or generated file was changed.

### What changed

- **STU-015.** The first interpretation no longer calls Augustine's comment on
  Psalm 85 (84):8 four words. A new subsection, "Augustine: Christ given, and
  still to be given", reports *En. in Ps.* 84.9 in its own order: *Hoc est
  quod cantavimus*; *salutare tuum, Christum tuum*; Christ already given and
  still asked for, as daily bread is; given as man and to be given as God,
  since men could receive him only as man; sons already in hope, not yet in
  fact (1 Jn 3:2); and the close, to see Christ as the angels see him. The
  question why the Church still prays a cry already answered is put before
  Augustine's answer, then Cyril's two comings follow. The sentences the
  Oxford English omits are translated from the bound Latin passage record
  and marked in the citation as the study's; the citation form is
  "84.9; §6 in the Oxford translation", as in the third interpretation. The
  scope appendix records the abridgement and that Psalm 84 was read in the
  Latin as well. The comparison table and the anagogical sense carry
  Augustine's answer.
- **STU-016.** Every appointed element now has at least a clause in each
  interpretation. Second interpretation: the Prayer over the Offerings beside
  Gregory's *servat operando* and the Collect; the Alleluia verse in the
  moral sense; the solemn blessing in the anagogical sense. Third
  interpretation: the Preface, which calls what those who keep watch await a
  promise (*promissum*), in the anagogical sense. The iteration-1 statement
  of policy above is corrected.
- **STU-017.** The opening keeps the three questions and drops the author
  rosters. Each interpretation's lead names its authors' answers once, in
  fewer words, and states the thesis once in its own words; the shared
  "Put together / Taken together" formula is gone. The third
  interpretation's closing paragraph, which restated its lead, is cut, and
  the first interpretation's sentence on the prayer granted in the flesh is
  trimmed to what it adds. The participle *venienti* is discussed only in
  section 10 (removed from section 05; the first interpretation now says
  only that the Collect asks for the will to go out to meet Christ as he
  comes). The absence of *Descendisti* from the United States English is
  stated in the opening; the first interpretation no longer repeats it and
  the comparison uses it in one clause. The first interpretation's
  "Where this interpretation strains" now holds the Jerome–Aquinas
  disagreement (moved there from the body, not repeated) and the sentence
  that no Father cited sets Isaiah's cry beside Mark's parable; "They are
  read together here because …" is cut. The comparison opens by saying which
  texts each interpretation draws on, compares rather than restates the
  theses, and its closing paragraph, which repeated the table's row on where
  the Fathers differ, is cut. The third interpretation's first strain no
  longer repeats the body; the second interpretation's strain no longer
  repeats Aquinas's sentence.
- **Advisories.** STU-018: the Prayer after Communion is described as
  asking that the mysteries profit those who receive them and stating that
  by them God already teaches them (sections 10, 20, 30, 40); section 10 now
  says that the two Verona prayers ask for what the Missal's prayer says God
  already does. STU-019: "the sense he prefers" for Egypt and "the first/second
  sense Aquinas lists" for the order; the explanation "as prophets speak of
  what is certain to come" is cut. STU-020: Bede, using Gregory's words on
  Matthew's traveller, reads Mark's man gone abroad as Christ ascended; the
  allegorical sense credits the clause on Christ's presence to Bede. STU-021:
  the scope appendix says that Jerome reads the petition of Isaiah 63:17 also
  as *converte nos* and Aquinas sets Lamentations 5:21 beside it, and counts
  the link to the psalm's refrain among the study's observations. STU-022:
  Augustine on 84.15 no longer stands inside Bede's allegory of the
  doorkeeper; he is cited in the second interpretation's moral sense,
  preaching on the Communion Antiphon's verse and asking God to give increase
  to the seed sown in his hearers.

### Verification performed at this iteration

Re-read: Augustine, *En. in Ps.* 84.9 in the registered Latin passage record
(`…latin-migne-corpus-corporum-wikisource-web-2026-09-05.84-9`) and in the
registered Oxford English passage record (`…1888-oxford-coxe.psalm-84-9`),
the second to fix which sentences the English omits; the description of the
two Verona prayers behind the Prayer after Communion in the shared
formulary's `propers/verified.md` (finding 7). Every other quotation kept or
moved at this iteration keeps its existing wording and citation and was not
re-read.

### Checks

- `tools/tpt document-types refresh --leaf claude/<proper> --check`: current.
- `scripts/_proper_study.py check` (content phase, research edition, source
  mode, presentation, format, authority, orientation and orientation-v3
  requirements): pass.
- `check-content-preflight --edition research`, all checks, and
  provenance-matches-run for this run: pass.
- Web probe into `build/tpt-runs/99f04ef5cf9b711b/artifacts/author-study-2/web-probe`:
  converted; all twelve `proper-<key>` anchors present once. The study
  prints no `\ref`.
- No print proof was made at this iteration.

### Substantive length

Measured on the web probe's Markdown from the opening through the
comparison: about 13,580 words (opening 1,296; appointed texts 2,255; each
text in its setting 2,222; the three interpretations 2,332, 2,554 and 2,302;
comparison 621). The iteration-1 figure of about 13,600 was measured on the
proof's text layer, so the two are close but not strictly comparable. The
study remains above the profile's 6,000–10,000 planning range, which is not
a quota.

### Research defect for its owner (standing)

The `research/interpretations.md` Reading 1 literal sense still credits Sinai
to Aquinas's preferred literal sense (iteration 1, above); the study follows
`research/scope.md`. Both `research/scope.md` (the Augustine 84 row) and
`research/interpretations.md` (Reading 1) summarize 84.9 without its
sentences on Christ already given and still to be given as God; the study
reports them from the bound Latin passage record. Neither research record
was changed at this stage.

## Derive-synthesis

Authored 26 November 2026 in the same run, at iteration 0, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), from the expansive study as it passed its third cold
review. No prior, carried or advisory finding was forwarded to the stage. The
stage wrote the `[document.synthesis]` declaration in `publication.toml`, the
five concise components under `sections/concise/`, the generation record's
contribution line and this section; `tools/tpt document-types refresh`
generated `synthesis.tex` and `generated/scriptural-date-location-page.tex`.
The components and roles in `proper-components.toml` were already declared and
are unchanged. No study section, research evidence record or generated
chronology record was changed.

### What the concise study contains

- **Page 1**: the twelve appointed texts in the order of the Mass (the solemn
  blessing marked optional), with a note on colour, Gloria and Creed, the
  Preface's rubric, chant substitution and the study English; then the four
  overview rows, each author named beside the clause he states.
- **Page 2**: the generated Scriptural Date and Location page.
- **Pages 3–4, The Propers: Themes and Movement**: the thesis, the
  *Praenotanda*'s account of Advent readings, and the texts in the order of the
  Mass with what each says, keeps and omits (the antiphon's *qui te
  exspectant*, the Collect's *voluntatem* and *occurrentes*, the prayer of
  Isaiah 63–64 from its Exodus memory to its ruins, *Descendisti* and its
  absence from the United States English, Isaiah 64:3 and 1 Corinthians 2:9 as
  Jerome links them, the psalm's vine, son of man and refrain, Paul's
  thanksgiving and the letter's rebukes, the *Ordo*'s titles, the Gospel's
  setting and its four watches, the Missal's prayers and Preface, Psalm
  85:11–13), ending on the three questions.
- **The Propers: Three Interpretations Compared** (from page 5): the three
  controlling claims in one paragraph; then seven questions at which the
  interpretations meet: *Descendisti* (Jerome against Aquinas's literal
  Exodus, the third interpretation's confession, Augustine 84.9 on Christ
  given as man and to be given as God, Cyril's two comings and the study's own
  inference on the torn heavens, stated as not Cyril's); Isaiah 63:17 and 64:4
  (Jerome's patience and Aquinas's permission, the inverted order, Jerome on
  the clay, the two grounds of asking, Isaiah 64:6 for the second
  interpretation); the petition to turn (Isaiah's *Convertere* and the
  refrain's *converte nos* kept apart in wording and joined only by Jerome and
  Aquinas; Augustine 79.3 and 84.8, Bellarmine; Augustine 79.9 and Bellarmine
  on the son of man; Augustine 79.11 on the vow); the hidden hour and "to all"
  (Jerome on Matthew 24 with Bede named as copyist only, Chrysostom on
  Matthew, Augustine's letter 199, Gregory on Luke 12 and the knock, Bede's
  own allotment on Mark 13:34–37, the Augustine–Bede difference and the
  objection to Augustine, the first and third interpretations' use of the
  parable); 1 Corinthians 1:7–9 (Chrysostom's Homily 2 in its own order, re-read
  for that order in the registered passage record, and Aquinas's lecture,
  each sentence assigned to the interpretation that uses it); the Communion
  verse (Bellarmine's virgin land against Augustine's confessing sinner); the
  Missal's prayers in each interpretation's light; and a closing paragraph with
  a table of the three interpretations' four senses.
- **Appendix: Scope and Qualifications** and **References**, listing only
  sources the concise study cites.

### Bounds observed

- Every attribution is the study's. The study-review advisories STU-023 to
  STU-030 are not carried: no closer sets a text beside the argument without
  its reason; Paul is said to thank God for gifts given and to describe the
  Corinthians as waiting, not to name two comings; Aquinas on Jeremiah 18 is
  not used; Jerome and Aquinas are named rather than "the Fathers"; the scope
  appendix names three relations stated by the books and does not raise the
  *Universal Norms* to one; Bellarmine's References entry gives the Latin and
  the English titles, and the body cites the English.
- Aquinas's literal sense of *Descendisti* is the descent at the Exodus from
  Egypt, not Sinai; Augustine 84.9 includes "given as man, to be given as God",
  following the study and the bound Latin rather than the research rows.
- The Gospel is quoted as the *Ordo* opens it, *Videte, vigilate*; the Prayer
  after Communion is described as stating that God teaches; Gregory's homily on
  the man of Matthew 25 is named as the source of Bede's identification.
- No sacramentary or lectionary history, and no other Mass, is named.
- The concise prints no `\ref`; the full study's date appendix is named by
  title, so the known `\ref{sec:date-location}` rendering defect does not
  arise.

### Verification performed at this stage

Re-read: Chrysostom, *Hom. in 1 Cor.* 2, in the registered passage record
`…homilies-on-first-corinthians.2026-09-28-ccel-web.2.1cor-1.7-9`, to fix the
order of the sentences on the grace of God (line 762), the Day at the doors
(769–770), "Revelation" and patience (776–778), v. 8 (789) and v. 9
(830–851); Augustine, *En. in Ps.* 84, in the tracked Oxford English (lines
41616–41639) and the tracked Latin (sections 8 and 9), which places the
comment "not only our being made alive is from Thee, but our very
conversion" at Latin 84.8, within Oxford §6. Every other quotation is taken
with its wording and citation from the reviewed study and was not re-read.

### Checks and proof

- `tools/tpt document-types refresh --leaf claude/<proper>` wrote
  `synthesis.tex` and `generated/scriptural-date-location-page.tex`; `--check`
  reports current.
- `scripts/_proper_study.py check` (content phase, synthesis and research
  editions, source mode, presentation, format, authority, orientation and
  orientation-v3 requirements): pass.
- `check-content-preflight --edition synthesis`, all checks (references-used:
  18 entries; structural-meta-labels: 22 headings; house-voice: pass), and
  provenance-matches-run for this run: pass. `make check-metadata` and
  `make check-generated-documents-current`: pass.
- Web probe: the synthesis edition converted from its own entrypoint with the
  converter's `edition_selection` into the stage's scratch area; every heading
  is present. `tools/tpt web-edition check --leaf` and `make
  check-proper-components` refuse only because `homily.tex` does not exist yet
  ("homily_entrypoint names a missing or empty file").
- Informal author proof (not requested by the packet and not a cold print
  review), compiled with `pdflatex` in three settled passes with a proof-only
  revision stamp, outside the tree: 12 physical pages, no overfull boxes;
  zref markers place inventory, overview and the four sense rows on page 1,
  chronology on page 2, themes on pages 3–4 and the commentary from page 5;
  the rights colophon shares page 12 with the References. PDF SHA-256
  `98ec9936ec1961494b372b9181aad62512e684d01437357d69821092a2dc364d`.

### Substantive length

Measured on the proof's text layer with running heads and page numbers
removed: page 1, 689 words; Themes and Movement, 1,686; the commentary with
its senses table, 4,487; about 6,860 substantive words in all. The scope
appendix adds 945 and the References 427.

### Shared defects for their owners

- `tools/tpt web-edition check` and `tools/check-proper-components` require
  `homily.tex` before the derive-homily stage can write it (tools owner).
- The research rows that credit Sinai to Aquinas and summarise Augustine 84.9
  without "given as man, to be given as God" stand as recorded above
  (research owner); the concise follows the study.

## Derive-synthesis, iteration 1

Revised 26 November 2026 in the same run, at iteration 1, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), against the synthesis review's three blocking
findings SYN-001 to SYN-003 and its advisories SYN-004 and SYN-005. Only
`sections/concise/02-overview.tex`, `04-themes.tex` and `10-commentary.tex`,
the generation record and this record changed. No study section, research
evidence record, manifest, generated file or publication declaration was
changed. The iteration-0 description above of the Communion verse ("virgin
land against confessing sinner") and of the Missal's prayers "in each
interpretation's light" no longer describes the text.

### What changed

- **SYN-001.** The Communion-verse subsection no longer sets Bellarmine and
  Augustine against each other as two readers who identify the earth
  differently, and no longer says that the earth is the Virgin in one
  interpretation and the confessing sinner in the other. It says that the
  first interpretation reads the verse with Bellarmine and the third with
  Augustine, then gives what each says at the verse: Bellarmine of the
  Incarnation (Ps 84, expl. 7 and 12); Augustine, expounding the same verse,
  after "Truth is sprung out of the earth", "which in this place he takes as
  confession" (84.15). Augustine's own Incarnational reading of v. 12 (84.13)
  is not stated, because it is not in the study.
- **SYN-002.** The themes no longer say that the antiphon "departs from both
  Latin psalters". They say that at that phrase the antiphon does not follow
  the Clementine Vulgate or the *Nova Vulgata*, which read *qui sustinent te*,
  and that the verb *exspectare* "comes again" in the Latin of the Mass. No
  change by the Missal is claimed, and the agreement with Augustine's psalter
  is not stated.
- **SYN-003.** The Missal's-prayers subsection gives each prayer by what it
  says. The Prayer over the Offerings offers gifts from what God has
  bestowed, compared once with Bede's servants who work by the grace given
  them; its second petition stays a prayer of those who keep the watch with
  works, without the chiastic closer. The Preface's sentence allotting a
  phrase to each interpretation is replaced by what its last clause says
  (*vigilantes*, from the verb of the Gospel's *vigilate*; *promissum*). The
  Prayer after Communion is followed by Gregory's *Nolite ergo attendere quid
  habetis, sed quid estis* (13.6) and "Gregory exhorts his hearers; the prayer
  says that God teaches", without the interpretation labels or the maxim
  closer; the solemn blessing keeps only its threefold petition, its two
  comings being given already. The hidden-hour section's restatement of
  Jerome is deleted. The paragraph allotting sentences of Chrysostom and
  Aquinas to the three interpretations is deleted; one clause at Aquinas's
  "day of death" now compares it with Augustine's letter on the Gospel's
  command to all, a link the scope appendix already lists.
- **Advisories.** SYN-004: Aquinas takes *dirumperes* either as a figure
  addressed to one above the heavens or as emptying himself and taking flesh;
  the overview's Moral row credits Jerome only with the disciples living each
  day as if to be judged the next. SYN-005: the themes open on what the
  prophet, Gospel and Preface say rather than a paradox; the question
  answered in the next breath before Augustine 84.9 is removed; the Preface's
  two Latin phrases in the commentary are translated.

### Divergence from the expansive study

The expansive study's Entrance Antiphon subsection (`sections/10-texts-in-setting.tex`)
still says the antiphon is "not a straight quotation of either Latin psalter"
and has *qui te exspectant* "for the psalter's *qui sustinent te*", although
Augustine's psalter (En. Ps. 24.3) reads *qui te exspectant* and
`research/scope.md` §3.6 bounds the claim to the *Nova Vulgata* and the
Clementine. The concise follows the research bound; the study is not
changed here (study owner).

### Verification performed at this iteration

Re-read the tracked Latin of Augustine, *En. in Ps.* 84 (Migne/Wikisource
artifact, sections 14–15), confirming that section 14 offers confession as
*alterum sensum* of v. 12 and section 15 reads v. 13 by it. Re-read
`research/scope.md` §3.6 on the antiphon's wording and the study's passages
on the prayers, Gregory 13.6, Bede and Bellarmine. Every other quotation
stands as it was taken from the reviewed study.

### Checks

`tools/tpt document-types refresh --check`: current. `scripts/_proper_study.py
check` (content phase, synthesis and research editions, source mode,
presentation, format, authority, orientation and orientation-v3): pass.
`check-content-preflight --edition synthesis`, all checks (references-used 18
entries, structural-meta-labels 22 headings, house-voice pass), and
provenance-matches-run for this run: pass. `make check-metadata` and `make
check-generated-documents-current`: pass. Informal author proof (not a cold
print review), `pdflatex` in three passes with a proof-only revision stamp,
outside the tree: 12 physical pages, no overfull boxes; inventory, overview
and the four sense rows on page 1, chronology on page 2, themes on pages 3–4,
commentary from page 5. The concise prints no `\ref`.

### Substantive length

Page 1 about 690 words; Themes and Movement about 1,680; the commentary with
its senses table about 4,360 (iteration 0's 4,487 less the 128 source words
cut); about 6,730 in all. The scope appendix (945) and References (427) are
unchanged.

## Derive-homily

Authored 26 November 2026 in the same run, at iteration 0, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), from the expansive study as it passed its third cold
review and the concise study as it passed its second. No prior, carried or
advisory finding was forwarded to the stage. The stage wrote the
`[document.homily]` declaration in `publication.toml`, the two homily
components `sections/homily/10-homily.tex` and `sections/homily/90-note.tex`,
the generation record's contribution line and this section; `tools/tpt
document-types refresh` generated `homily.tex`. The homily components were
already declared in `proper-components.toml` and are unchanged. No study
section, concise section, research evidence record, generated chronology
record, format file or web-edition record was changed.

### What the homily says

For an adult parish assembly at the Mass of 29 November 2026. Its argument
is the third interpretation, *The Clay and the Faithful Potter*, joined with
the second, *The Watch at the Door*, as the expansive study's comparison
joins them (each keeps the other from its one-sided reading). From the first
it takes only the Preface's two comings; *Descendisti* is not preached,
because the English proclaimed in the United States does not read it, and
the comparison finds that English closer to the third interpretation.

In order: the scene on the Mount of Olives, the parable, the four watches and
"what I say to you, I say to all: Watch"; Augustine's letter 199 on why the
command reaches all; the prayer of Isaiah 63–64 spoken among ruins, the
question why God let his people stray, with Jerome on God's patience; the
confession, ending in "There is none that calleth upon thy name"; the next
verse, in which the same people call on God as Father and name themselves
clay, with Jerome on merits and mercy, clay and sons; the psalm's refrain with
Augustine, "unless he turns us, we will not be turned", and the Collect's
petition for the will to go out to meet Christ; Bede's servants given
authority as the Spirit's grace for good works, and his door of each heart;
Paul's thanks for the Corinthians and "God is faithful", with Chrysostom's
three points on it; one response; the Preface's two comings and its
*vigilantes* as the Gospel's word, and the Prayer after Communion; ending on
1 Corinthians 1:8–9 spoken to the assembly.

**The change the texts make, and the detail that makes it.** The familiar
difficulty is that the command to watch is heard every Advent and known to
be badly kept. Isaiah 64:6–7 is the decisive detail: the people confess that
none calls on God's name or rises to take hold of him, and in the next verse
they call on his name as Father and call themselves clay. With the psalm's
petition that God turn his people and the Collect's petition for the will,
the command becomes something the Church asks of God and begins to keep by
calling on him; Paul's thanksgiving for a faulty church gives its ground,
God's fidelity. The argument would not survive a change of readings: it
rests on the order of Isaiah 64:6–7, on Mark 13:37 and on 1 Corinthians
1:8–9.

**The response.** Before Christmas, in the sacrament of confession, to name
to God the place where one has been asleep and to call on him as Father,
which is what Isaiah's people do in the reading; Augustine on the Communion
verse (*En. in Ps.* 84.15) gives the reason. It is said once. Compared with
the invitations of the series' recent postconciliar homilies (the coin as a
reminder of Jesus' question, the farm and merchandise named and something
given away, the unearned good met with gladness), it is neither a weekly
exercise nor drawn from those Sundays' images.

### Bounds observed

- No new evidence-dependent claim. Every author is credited with what the
  studies credit him with, at the study's locus; the homily's own links are
  listed in the terminal note. Bede is cited only on Mark 13:34–37, his own
  comment; his comment on 13:32–33, which is Jerome's, is not used. Aquinas
  is not cited, so no sentence calls him one of the Fathers.
- The study-review advisories STU-023 to STU-030 and the synthesis advisory
  SYN-006 are not inherited: Paul is not said to name two comings; Aquinas on
  Jeremiah 18 is not used; the solemn blessing is not described at all; the
  Collect, the Preface and the Prayer after Communion are described only in
  part, in words taken from the study's account of the Latin and not from the
  approved English.
- The psalm's refrain is said to ask God to turn his people; Isaiah's
  petition to God to return is not presented as the same words. The Gospel is
  not given the Clementine "and pray". The Prayer after Communion is said to
  state that God teaches by the mysteries.
- Nothing depends on a sung or recited form of the psalm, the Alleluia verse
  or either antiphon: the Communion verse is named as the one the Missal
  gives, and the psalm as the one appointed. The optional blessing is not
  mentioned.
- No Latin is spoken. Scripture is quoted in the Douay–Rheims, named once,
  at four verses; the Lectionary's English and the Missal's approved English
  are not quoted. No anecdote, personal experience or attributed quotation is
  invented. The homily prints no `\ref`.

### Verification performed at this stage

Re-read in the tracked texts: Chrysostom, *Hom. in 1 Cor.* 2, in the
registered passage record `…homilies-on-first-corinthians…2.1cor-1.7-9`, for
"not even did this praise belong to them, but to the grace of God", "lest
after the vehemence of the reproofs they might fall into despair" and "God is
faithful, i.e. true. Now if true, what things He hath promised He will also
perform"; Augustine, *En. in Ps.* 79.3, in the tracked NPNF English ("For
averse we have been from Thee, and except Thou convert us, we shall not be
converted"); Augustine, *En. in Ps.* 84.15, in the tracked Latin passage
record (*Tua ergo peccata potes habere; fructum bonum non habebis, nisi ille
dederit cui confiteris*); Bede, *In Marc.* IV on 13:34–37, in the tracked
Latin. Augustine's letter 199 and Jerome on Isaiah are taken with their
wording and loci from the reviewed study and `research/scope.md` and were not
re-read.

### Length and pace

The spoken body is 1,377 words, counted as whitespace-separated words with
comments and markup removed: about 10.6 minutes at 130 words a minute, 11.0
at 125 and 11.5 at 120. That is arithmetic on the count; no delivery was
timed. The prose was read through in its final form for sense and ease of
speech, silently, not aloud.

### Checks and proof

- `tools/tpt document-types refresh --leaf claude/<proper>` wrote
  `homily.tex`; `--check` reports current.
- `scripts/_proper_study.py check` (content phase, homily, synthesis and
  research editions, source mode, presentation, format, authority and
  orientation-v3 requirements): pass.
- `check-content-preflight --edition homily`, all checks (references-used: 8
  entries; structural-meta-labels: 7 headings; house-voice: pass), and
  provenance-matches-run for this run: pass. `make check-metadata`, `make
  check-generated-documents-current` and `make check-proper-components`: pass.
- Web probe: the homily edition converted from its own entrypoint with the
  converter's `edition_selection` into the stage's scratch area; the speech,
  the note and the References are present. `tools/tpt web-edition check
  --leaf` refuses only because the leaf has no alpha or hold disposition yet,
  which the publication stages own.
- Informal author proof (not requested by the packet and not a cold print
  review), built with `tools/print-document build --edition homily` outside
  the tree: 4 physical pages, the speech in two columns on pages 1–2, the note
  and References on pages 3–4 with the rights colophon on page 4. PDF SHA-256
  `72f20853404ca4d71893cfdc55f8d0d644210de0ec7f747d4f950c960e50f6eb`.

## Derive-homily, iteration 1

Revised 26 November 2026 in the same run, at iteration 1, by
`claude-opus-5-5` in a fresh Claude Code harness subagent (dispatched
reasoning effort high), against the homily review's blocking finding HOM-001
and its advisories HOM-002 to HOM-006. Only `sections/homily/10-homily.tex`,
`sections/homily/90-note.tex`, the generation record and this record
changed; `homily.tex` regenerates unchanged. No study section, concise
section, research evidence record, manifest or publication declaration was
changed. In the iteration-0 description above, the question of Isaiah 63:17,
the word count, the four Douay verses and the closing now read as below.

### What changed

- **HOM-001.** Augustine on the Communion verse (*En. in Ps.* 84.15) is
  spoken as "Your sins, then, you can have of your own; good fruit you will
  not have unless the one to whom you confess gives it", the homily's own
  English of *Tua ergo peccata potes habere; fructum bonum non habebis, nisi
  ille dederit cui confiteris*, checked again in the tracked Latin passage
  record: *ille … cui confiteris* is the subject of *dederit*, so the giver is
  the one confessed to, as in the sentence before (*nisi ille fecerit cui
  confitetur*). The note now says the sentence is quoted in the homily's own
  English and that the studies' English is not the one spoken.
- **Advisories.** HOM-002: the speech keeps the permissive question, then
  gives the Douay's 63:17 ("made us to err", "hardened our heart") as the
  form Jerome explains, naming the Douay there instead of at 64:6. HOM-003:
  Isaiah's people "know they have failed God and say so"; the link to the
  Gospel's sleep is drawn once, in the preacher's voice. HOM-004: the burnt
  house is spoken of "near its end", "now burnt with fire"; Jerome's
  reasoning speaks of "God's mercy" and "he is our Father"; the Chrysostom
  paragraph is divided, the praise that belongs to grace and "faithful, i.e.
  true" in one, the place of "God is faithful" against despair and the
  failure that comes from those who start away in the next, in Chrysostom's
  order; the Preface "uses the Gospel's word of those who give thanks".
  HOM-005: the closing gives 1 Cor 1:8 to Christ, as the speech does
  earlier and as the study's comparison reads it. HOM-006: the note says
  Bede is reported from the Latin given below and Jerome from the expansive
  study's account of his Latin, which that study read on the Migne page
  images (cols. 643–644 and 648–650, in the loci). The note's route
  paragraph was tightened so that the longer account still leaves the rights
  colophon on the last page of the note.

### Shared observation for the study owners

Both studies print the same English of Augustine, *En. in Ps.* 84.15
(`sections/40-clay-and-faithful-potter.tex`; `sections/concise/10-commentary.tex`),
"good fruit you will not have unless he gives it to whom you confess", in
which "to whom you confess" can be heard as the indirect object of "gives".
The Latin stands beside it there. The homily follows the Latin; the studies
are not changed here.

### Verification and checks

Re-read the tracked Latin passage record of *En. in Ps.* 84.15, the tracked
Douay–Rheims (Challoner) Isaiah 63:17 and 64:7–8, and the tracked
Chrysostom passage record of Homily 2 on First Corinthians (sections 4–8),
whose order the divided paragraph follows ("God is faithful, i.e. true …";
"These things … he inserts thus early, lest after the vehemence of the
reproofs they might fall into despair"; "unbelief cometh not of Him that
calleth, but of those who start away from Him"). The spoken body is now
1,398 words by the same count: about 10.8 minutes at 130 words a minute,
11.2 at 125 and 11.7 at 120; no delivery was timed. The revised paragraphs
and the speech as a whole were read through for sense and ease of speech,
silently, not aloud.

`tools/tpt document-types refresh --check`: current. `scripts/_proper_study.py
check` (content phase, homily, synthesis and research editions, source mode,
presentation, format, authority and orientation-v3): pass.
`check-content-preflight --edition homily`, all checks, and
provenance-matches-run for this run: pass. `make check-metadata`, `make
check-generated-documents-current` and `make check-proper-components`: pass.
Informal author proof (not a cold print review), `tools/print-document build
--edition homily` outside the tree: 4 physical pages, the speech in two
columns on pages 1–2, the note and References on pages 3–4 with the rights
colophon on page 4. A first proof of this iteration put the colophon alone
on a fifth page; the shortened route paragraph removed it. The homily
prints no `\ref`.
