# Research handoff: revision of the Claude Twenty-ninth Sunday

Identity `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`,
provider `claude`, Sunday 18 October 2026, audience "adult parish assembly".

On 16 October 2026 the maintainer asked for the issues that the first
accepted run (`4d16b5e19d25dad9`, `proper-study` v11) left standing to be fixed,
and for its sourcing to be fixed, and the result pushed to `main`. This
revision run carries that request. The published leaf, its records and the
first run's archive under `evaluations/proper-study-results/4d16b5e19d25dad9/`
are the starting point. Everything below is a **lead**: verify it against the
sources; nothing here is inherited verification or an inherited verdict.

This remains an independent Claude production. Do not open the GPT leaf for the
same identity, its PDFs or web edition, or its workflow records.

## What changed in the shared tools before this run

- `proper-study` is at version 12. New runs declare
  `chronology_presentation = "orientation-v2"` and generate the page-2 rows with
  `--presentation orientation-v2` (`guidance/scripture-chronology.md` §14.1).
  Version 2 gives the narrated-event row only to Gospel pericope keys, never to
  `gospel-acclamation`; prints verse ranges with the en dash; and names each
  psalm citation's numbering with the other system's psalm. The first run's
  workaround, keying the acclamation `acclamation`, is no longer needed; keep
  it or restore the conventional `gospel-acclamation`, and say which.
- The study and synthesis preflights carry a locus-aware `references-used`
  check (every locus a References entry names must be cited in that document)
  and an extended house-voice screen (`guidance/editorial.md`, "A screen finds
  some of this"). Measured against the published leaf, the new references-used
  check refuses one concise References locus: Douay–Rheims Matthew 21:45–46,
  which the prose paraphrases without citing.
- The site stylesheet now sets the three-column page-2 table on one grid line
  at phone width (the web-review observation below).

## Sourcing to fix

1. **United States GIRM, chapters II, VII and VIII.** Chapter VIII and, in the
   first run, all three chapter pages returned HTTP 403 on re-read. The
   records register the states the context stage read under the hashes it
   recorded. Re-read the official pages, or another official USCCB witness of
   the same 2011 text with the 2021 emendations, by a lawful route. Register
   what you actually read, and verify every paragraph the documents rely on
   (61, 62 and any other) at its locus. If an official text cannot be read,
   say so in the records and do not let the documents rest on it beyond what
   was verified.
2. **The dated USCCB readings page for 18 October 2026 (Lectionary 145).** It
   also returned 403 and is registered from the context stage's hash.
   Re-read it, or verify the Lectionary 145 locators and the
   psalm verse selection against another official witness, and register what
   you read.
3. **NABRE Psalms introduction.** Read in states whose bytes differ from the
   registered state and from each other. Register the state actually read,
   or rest on the registered state only for what its bytes show.
4. **Gelasian (Wilson 1894) and Verona (Feltoe 1896) page images.** Quoted from
   PDFs that are not in the source library. Register lawful public-domain
   page-image excerpts, as was done for the Patrologia Latina and Aquinas
   facsimiles, and bind them.
5. **Schuster and Fromage (and Honorius's interleaved columns).** Read only in
   OCR. Verify every locus the records or documents use against page images,
   register facsimile excerpts where a locus is used, and correct the records.
6. **World Mission Sunday.** 18 October 2026 is the penultimate Sunday of
   October. No dated witness was sought for a mission observance; the
   context keeps that branch conditional and unsupplied. Seek dated official
   witnesses (the Holy See's message for World Mission Day 2026, the United
   States observance, and the Missal's and GIRM's rules for the Mass for the
   Evangelization of Peoples on a Sunday in Ordinary Time). Resolve the branch
   on that evidence, and keep the observance out of the documents unless the
   evidence makes it part of this Sunday's celebration.
7. **The *maiestas* lexical claim (RES-013).** Marked unverified because the
   library held no Latin lexicon. Verify it in a lawful public-domain lexicon
   such as Lewis and Short (1879) and register it, or drop the claim.

## Standing findings of run 4d16b5e19d25dad9

These come verbatim from the leaf's `evaluations/blocking-findings-v1.toml`.
Each "Required result" says what fixing it means; the conditional "if the
file is reopened" wording now applies, because this run reopens every owner.

- **STU-004** (accepted, study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/interpretations.md, Reading 1, 'Element contributions' table, Responsorial psalm row, Basis cell: "(his v. 7 reads \"worship and honour\"; ...)"
  - Problem: The research record still says that Augustine's v. 7 reads 'worship and honour'. His Latin at En. in Ps. 95.8 reads 'afferte Domino gloriam et honorem' (latin-migne-corpus-corporum-wikisource enarrationes-part-10.txt line 118); 'worship and honour' is the NPNF English. The study no longer reproduces the claim (STU-002 repaired), and research/production-review.md records the defect for the research owner.
  - Required result: Whenever the research records are next reopened by their owner, the parenthesis says that the NPNF English renders v. 7 'worship and honour' while Augustine's Latin reads gloriam et honorem.
- **VIS-001** (accepted, visual-review). Location: Expansive study, physical page 28 (end of The Three Interpretations Compared, sections/50-comparison.tex; forced page break before sections/80-date-location.tex)
  - Problem: The comparison's closing paragraph (seven lines: the first and third can be preached together; each interpretation's principal difficulty) stands alone at the top of page 28, about 14% of the text block, and the rest of the page is empty because the Scriptural Date and Location appendix begins on a fresh page 29.
  - Required result: If the study is repaginated for another reason, end The Three Interpretations Compared on page 27, or follow it on the same page with the next section, without padding, type reduction or cutting the paragraph.
- **WEB-001** (accepted, web-review). Location: build/web/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a.md line 600 (Appendix: Scope and Qualifications, 'Text control.' paragraph, last sentence); source src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/90-apparatus.tex lines 33-36
  - Problem: Reader-facing text names a production stage. The sentence says the branch rows rest on the United States General Instruction 'as read, in its official chapter pages, at the stage that resolved this Sunday's context; a later attempt to read the same pages again was refused by the publisher's site'. 'The stage that resolved this Sunday's context' is workflow-process language that a reader cannot interpret. The research PDF carries the same words, and the conversion reproduces them faithfully, so this is a study-writing defect, not a conversion defect.
  - Required result: If sections/90-apparatus.tex is reopened for another reason, identify the reading by its date instead of a production stage, for example: 'as read in its official chapter pages on 16 October 2026; a later attempt that day to read them again was refused by the publisher's site'. Then regenerate the web edition.
- **HOM-001** (advisory, homily-review). Location: sections/homily/10-homily.tex, fourth movement (the worn coin restamped), the sentence beginning "In Saint Mark's words, which one of the two Communion antiphons today takes up"
  - Problem: The relative clause "which one of the two Communion antiphons today takes up" puts liturgical apparatus inside the speech. It refers to a Missal option that an assembly rarely hears as such, because a hymn often replaces the antiphon. It also holds a ten-word aside between "In Saint Mark's words" and the quotation, which makes this the hardest sentence in the speech to follow by ear. The argument does not need it: Mark 10:45 carries the point as Scripture, and the terminal note already records the branch and the antiphon relation.
  - Required result: Introduce Mark 10:45 directly as Scripture without the embedded antiphon clause, for example "In Saint Mark's Gospel the Son of man came ...". If the link to the Communion antiphon is kept, give it a short sentence of its own after the quotation, one that stays true whichever antiphon or substitute is sung. Keep the terminal note's branch statement consistent with whatever the speech then says.
- **HOM-002** (advisory, homily-review). Location: research/scope.md section 2, textual-observations paragraph ("in v. 8, bring sacrifices (*tollite hostias*, not sung)"), on which the sentence "The psalm told us how to come: 'Bring up sacrifices, and come into his courts.'" in the seventh movement of sections/homily/10-homily.tex depends
  - Problem: Scope section 2's parenthetical says that v. 8's "bring sacrifices" is not sung. That contradicts three other statements in the records: the Ordo and US locator 7-8, given as whole verses in propers/verified.md (unit 4) and research/context.md (row 4); context.md's list of what is not sung (v. 2, v. 6 and the middle clause of v. 10 only); and scope.md's own section-2 table row for Psalm 95, which marks v. 8 without "not sung". The homily's claim that the psalm told the assembly to come into his courts with sacrifices holds only if v. 8b is sung. The bound locator supports the homily, so the defect is the research record's inconsistent parenthetical and not the speech. A later reader of scope.md would still find the homily's sentence contradicted there.
  - Required result: Make the research records agree that v. 8 is sung whole by correcting the scope.md section 2 parenthetical when the research owner next touches that file. Alternatively, if a reading of the printed Lectionary shows v. 8b omitted, revise the homily's sentence so that it no longer says the psalm told the assembly to bring sacrifices into his courts.
- **RES-014** (advisory, research-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/scope.md section 8.3, row 'Composition of the Psalms (`row-6e9c8175463dbd35`)', Source and locus cell ('which this stage could not re-read (section 8.2)'); src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/scope.md section 10, lead 8 ('and its current state'); src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/source-bindings.toml, binding of artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08179b-d4ee13fd-article-text (loci 'line 7' and the 701 sentence)
  - Problem: The third pass re-read the NABRE Psalms introduction. Section 5 records the delivery (74,093 bytes, SHA-256 03234893...); this review re-fetched it byte-identically and found the dating sentence; section 8.2 now relies on it. But section 8.3 still calls it a source 'which this stage could not re-read (section 8.2)', and section 10 lead 8 still lists 'its current state' as outstanding. Likewise, section 8.2 now reports reading Souvay at lines 9 and 11, while the Souvay article-text binding's loci name only line 7 and the 701 sentence. Nothing the studies may print changes, since the planned phrase stays 'Place of composition unknown', but the record contradicts itself about what this research read.
  - Required result: Section 8.3's row says that the label's source was read at the third pass in a current delivery (section 8.2) and names no place of composition. Lead 8 keeps only the registered state of 28 July 2026 as outstanding. The Souvay article-text binding's loci name line 9 and line 11 beside line 7.
- **RES-015** (advisory, research-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/interpretations.md, Reading 3, 'The strongest difficulty, and how the witnesses meet it', second sentence ('Matthew says only that the Pharisees went and took counsel how to ensnare him in his speech (22:15 ...); the text does not say whether their purpose was known')
  - Problem: Matthew 22:18 says that Jesus knew their wickedness: Douay 'But Jesus knowing their wickedness' (47-matthew.tsv line 746); Clementine 'Cognita autem Jesus nequitia eorum'. Those are the words that prompt this difficulty. Jerome's 'Prima virtus est respondentis ...' (PL 26 col. 163, page image) and Aquinas's 'Et primo respondet ad mentem eorum ... Dei autem respondere ad mentem' (Venice p. 283, page image) are each written under that lemma. The paragraph instead anchors the question in 22:15 and says that 'the text does not say whether their purpose was known'. That means known to others beforehand, but read plainly it contradicts v. 18. A study following it could write that Matthew is silent on whether their purpose was known.
  - Required result: The paragraph anchors the question in 22:18 ('knowing their wickedness', cognita ... nequitia eorum), the lemma under which Jerome and Aquinas write. It says only that the text does not say whether anyone else knew their purpose beforehand. The rest of the RES-009 repair stays as it stands.
- **STU-010** (advisory, study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/10-each-element.tex lines 230-231 ('Bellarmine calls the pupil ``frail and delicate''.'); src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/30-cyrus-and-caesar.tex lines 229-231 ('In the psalm the verse continues by asking protection from those who resist God's right hand')
  - Problem: Two small misdescriptions at Psalm 16 (17):8. (a) Bellarmine (O'Sullivan, tracked text line 535) calls the apple of the eye 'a most delicate, though valuable article', then says 'such are we, frail and delicate'. The quoted words describe the petitioners, not the pupil. (b) In the Clementine and the Douay-Rheims, 'From them that resist thy right hand' opens v. 8, before 'keep me', as the study itself prints at 05-appointed-texts.tex lines 33-34 and 44. The verse does not 'continue' with it.
  - Required result: (a) attributes the quoted words to their own referent, for example 'Bellarmine calls the pupil "a most delicate, though valuable article", and those who pray "frail and delicate"'. (b) says that the same verse opens by asking protection from those who resist God's right hand, words the antiphon leaves out.
- **STU-011** (advisory, study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/30-cyrus-and-caesar.tex lines 190-196 ('For Chrysostom and Augustine the debt is one of justice that binds every Christian ... They disagree about why Caesar is owed anything at all'); src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/50-comparison.tex lines 33-34 and 76-78
  - Problem: The preserved disagreement over the ground of the debt is fully evidenced for Hilary and Ambrose, by quotation, but only asserted for Chrysostom and Augustine. The only Chrysostom ground the reader is shown is the coin's image and superscription (lines 107-112). That is close to Hilary's 'si rebus illius incubamus', so the summary 'They disagree about why Caesar is owed anything at all' is not made intelligible by the evidence on the page. The sentences that show the other ground stand at loci the study already cites: Augustine En. in Ps. 124.7, 'thus hath God ordained His Church, that every power ordained in the world may have honour, and sometimes from those who are better than those in power' (NPNF tracked line 61102-61103); and Chrysostom Hom. in Rom. 23, 'if thou be an Apostle even, or an Evangelist, or a Prophet, or anything whatsoever, inasmuch as this subjection is not subversive of religion' (tracked lines 46234-46236), whose last clause the study already quotes.
  - Required result: The disagreement section shows the Chrysostom and Augustine ground in their own words at the loci already cited. Otherwise the section and the comparison narrow the stated difference to what the quoted words show: whether one who keeps nothing of the world's goods still owes Caesar.
- **STU-012** (advisory, study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/90-apparatus.tex lines 101-109 ('The questioners' paragraph, last sentence: 'Augustine's definition of the whited wall is used without the application he gives it in its section.')
  - Problem: The sentence closes a paragraph about Fathers who pass from the questioners to the Jewish people, and about Nostra aetate 4. Placed there, it implies that Augustine's whited-wall application at En. in Ps. 95.3 is anti-Jewish. In that section the application is to the Donatist party ('Getulia, Numidia, Mauritania, Byzacium'; NPNF tracked lines 47915-47940), as research/scope.md section 3.10 and research/production-review.md record.
  - Required result: The appendix names the application as Augustine's charge against the Donatist party, or moves the sentence out of the paragraph about the questioners, so that no reader takes it for anti-Jewish polemic.
- **STU-013** (advisory, study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/production-review.md, 'Author-study, iteration 1', 'Proof' list (lines 227-239)
  - Problem: The iteration-1 proof entry gives the page count but not the SHA-256 of the checked PDF, which the iteration-0 entry did give. The three-document profile asks the production record to carry checked artifacts and hashes. The reviewed build is 84e8166a38f5af6ae622412a962e5b4b67bde847af65f44814084176c6756db8 (37 pages), byte-identical to the author's iteration-1 proof.
  - Required result: The next author that updates the production record adds the iteration-1 proof's SHA-256 beside its page count.
- **SYN-004** (advisory, synthesis-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/concise/10-commentary.tex lines 215-217: 'Hilary: Christ knew interna cogitationum secreta, "for God sees everything hidden within men" (23.1)' (PDF pp. 7-8)
  - Problem: After the SYN-002 repair this is the one witness phrase in the commentary still given only in Latin. The English beside it renders Hilary's parenthesis and not the phrase itself, which is the object of what Christ knew. A reader without Latin gets the sense from context but not Hilary's words. The expansive study renders the phrase as 'knowing the inner secrets of their thoughts' (sections/40-sincere-heart.tex lines 83-85).
  - Required result: Give the phrase the expansive study's rendering (for example 'the inner secrets of their thoughts') beside or in place of the Latin. Add no new claim and do not change the type size.
- **SYN-005** (advisory, synthesis-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/production-review.md, 'Derive-synthesis, iteration 1', Repairs, SYN-002 bullet: 'and so do four further unglossed phrases (Aquinas's "as if he said", his "to Christ, that is, to the king", "because it belongs to man to answer words", and "inasmuch as they have something of the light")'
  - Problem: The record undercounts what the repair changed. A fifth phrase outside SYN-002's list also lost its Latin to an English rendering: Jerome's 'Prima virtus est respondentis, interrogantium mentem cognoscere' is now 'the first virtue of one who answers is to know the mind of those who ask' (10-commentary.tex lines 220-221), and the record does not mention it. The production audit is meant to state the revision exactly.
  - Required result: The next author to update the production record corrects the bullet to five further phrases and names Jerome's 'the first virtue of one who answers'. Nothing else needs to change.
- **VIS-002** (advisory, visual-review). Location: Expansive study, physical page 29, Scriptural Date and Location table (sections/80-date-location.tex)
  - Problem: Unlike the concise page-2 table, the study's table has no space between rows within a book group, so where the Passage cell is the tallest in its row, adjacent rows' Passage cells run together at the ordinary line pitch: the first two psalm rows form one unbroken ten-line block, and the two 'Responsorial Psalm: Psalm 96:1, 3, ...' rows form one six-line block of identical labels. A row boundary is visible only from where the Occurrence and Date cells start.
  - Required result: Row boundaries visible in the Passage column as on concise page 2 (for example the same inter-row spacing the concise component uses), with the table still on page 29 and its type size unchanged.
- **VIS-003** (advisory, visual-review). Location: Expansive study, physical page 7, first line (The Appointed Texts, Douay-Rheims Phil 2:15-16 block; sections/05-appointed-texts.tex, the \notread after 'word of life')
  - Problem: The marked unappointed words print as 'the word of life[ to my glory in the day of Christ: ...]': the word space falls inside the bracket and none precedes it, which reads as a typesetting slip beside the other bracketed omissions on pages 5-8.
  - Required result: The bracket set as 'the word of life [to my glory in the day of Christ: because I have not run in vain, nor laboured in vain.]', with the space before the opening bracket.
- **VIS-004** (advisory, visual-review). Location: Homily, physical page 1, left column, the movement break after 'and he calls them hypocrites.' (sections/homily/10-homily.tex inside the shared properhomily environment)
  - Problem: The two-column environment sets flush-bottom columns, and the left column's only stretchable glue is this \bigskip, so the break opens to about 0.8 in (158 px at 200 dpi) where every other movement break in the speech measures about 0.28-0.30 in (55-60 px). On the homily's first page it reads as a hole rather than one of the uniform breaks a speaker uses to find his place.
  - Required result: Every movement break in the speech of the same height on every page, without changing the spoken text; the general remedy is ragged-bottom columns in the shared homily environment, a maintainer-level shared change beyond this leaf.
- **Observation** (research-review). Location: scripts/_proper_chronology.py, orientation builder line 1465 (element.key.startswith("gospel")) against the detailed-annotation path line 1292 (element.key == "gospel")
  - Still present. Any postconciliar orientation-v1 leaf that keys its acclamation 'gospel-acclamation' gets a narrated-event row for that element; this leaf avoided it only by re-keying (scope.md 8.1). The defect is in a shared tool that no stage of this run may repair, and no generator test criterion covers it.
- **Observation** (research-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/context.md, branch row mass-for-evangelization-of-peoples (line 294) and the closing note at line 425
  - The branch stays conditional and not supplied, and no dated witness was sought for a mission observance on 18 October 2026. Line 425 rightly requires one before any study mentions such an observance. Recorded again so that the standing record keeps the sighting the earlier rounds made.
- **Observation** (study-review). Location: src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/sections/80-date-location.tex orientation table (rendered p. 29) and src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a/research/chronology-annotations.tex orientation rows
  - Still present: the generated Passage cells print the antiphons' psalms in Vulgate numbering ('Cf. Psalm 16:6, 8', 'Cf. Psalm 32:18-19') and the responsorial psalm in Hebrew numbering ('Psalm 96:1, 3 ...') with no numbering marker. Only the notes beneath reconcile them. This is generator output, and its likely cause is a missing orientation-row criterion.
- **Observation** (study-review). Location: tools/tpt check-content-preflight --check house-voice (study-preflight 0000 log: 'no sentence taking the guide, its apparatus or the repository as its subject', exit 0)
  - The screen passed the iteration-0 text, which still had sentences of the forms 'the editor joins', 'the interpretation does not' and 'No commentary on' that STU-001 later removed. These forms appear to be a missing lexical criterion of that screen.
- **Observation** (visual-review). Location: Concise page 2 and study page 29, Passage column of the generated orientation rows (refs from research/chronology-inputs.toml)
  - The generator prints the input ref strings verbatim, so verse ranges show ASCII hyphens (Psalm 32:18-19, Isaiah 45:1, 4-6, Matthew 22:15-21, 1 Thessalonians 1:1-5b) beside the en-dash ranges of the page-1 map and the notes; other leaves' inputs use the same ASCII form, so this looks like a missing display-normalization rule at the generator rather than a leaf defect.
- **Observation** (web-review). Location: release/public-alpha/assets/site.css lines 596-627 (the 760px rules for the Scriptural Date and Location dossier), applied to the orientation-v1 table at build/web/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a.md lines 526-539, rendered at 390 px
  - At phone width the dossier rules set this three-column orientation-v1 table on a two-column grid: Passage and Occurrence on one line, Date beneath, with an empty cell beside 'Date' in the header block and beside each date. The stylesheet's comment and rules describe only the four-column dossier. Every row still pairs passage, occurrence and date legibly, so nothing is lost here, but no rule fits the three-column orientation shape the newer propers now publish.
