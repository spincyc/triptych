# Research scope: The Order of Mass (Claude edition)

## Question and reader

What does the Roman Order of Mass, in the state printed in the 2008 Latin *editio typica
tertia emendata*, actually contain; what does the General Instruction require of each movement;
where did each movement come from; and what is it for? Subordinate to that: what exactly did the
2011 English translation for the United States change, and on what authority?

The intended reader is a serious lay reader, cleric, religious, catechist, or student who can
follow liturgical vocabulary and a little Latin but should not need a ceremonial manual. The
work is a sequential exposition of a received rite with its law, history, and meaning. It is not
an altar book, a ceremonial, a critical edition, a text for recitation, a translation, or a
polemic for or against the reform.

## Governing guidance

- `guidance/editorial.md`
- `guidance/repository.md`
- `guidance/sources.md`
- `guidance/liturgy/ordinary-expositions.md`
- `guidance/web-editions.md`

The postconciliar propers profiles do not govern this document. Its architecture follows the
Order of Mass's own sequence and the General Instruction's own division of the Mass into two
constitutive parts framed by opening and concluding rites.

## Method and publication architecture

After title and contents, the publication opens with its governing thesis and a usable map of
the received action by the Missal's own numbering, then follows the movements in order:
Introductory Rites; Liturgy of the Word; Creed and Universal Prayer; Preparation of the Gifts;
the Eucharistic Prayer's common grammar; the Roman Canon; Prayers II, III, and IV; Communion
Rite; Concluding Rites. A dedicated section then treats the 2011 English and the published rule
under which it was made, and a whole-action section closes with a clearly labelled **Project
synthesis** block carrying the judgement, its reasons, the strongest counterargument at full
strength, and the specific finding that would overturn it.

Terminal apparatus follows in the profile's order: **Scope, Edition, and Qualifications**;
**Development and Edition Timeline**; **References**; **Generation Metadata**.

Each movement receives the treatment its own form requires: a procession through agents,
direction, and destination; a dialogue through speakers and what the answer concedes; a psalm
through its mode of use; an oration through address, silence, and mediation; the Eucharistic
Prayer through anaphoral grammar rather than a checklist. These are coverage controls, not
repeated visible fields.

## Source hierarchy

1. **Controlling rite.** *Missale Romanum*, editio typica tertia (2002) in the registered
   secondary digital reproduction, plus the official 2008 *Notitiae* notice and variation list
   that define the emended reprint; the Latin *Institutio Generalis* in the same reproduction;
   the United States English General Instruction, Chapter II.
2. **Promulgating and governing acts.** Paul VI, *Missale Romanum* (Latin); *Sacrosanctum
   Concilium*; *Liturgiam authenticam*; the CDW circular letter of 17 October 2006 on
   *pro multis*.
3. **Comparand.** *Missale Romanum*, editio typica 1962, at the Canon and at named points.
4. **Ancient witnesses, at exact loci.** Justin, *First Apology* 65–67; the Verona Latin of the
   church order conventionally called *Traditio apostolica* (Hauler 1900); Ambrose (or the
   author of *De sacramentis*), *De sacramentis* IV (PL 16, 1880).

Every source in classes 1–4 was reached and read for this study, at the loci recorded in
`source-audit.md`. Nothing is cited from memory or from a secondary summary except where the
References page says so explicitly under "Cited but not examined."

## Claim discipline

- "The Order of Mass" means the *Ordo Missae*, nn. 1–146, not the sung Ordinary and not the
  Missal.
- The Mass is one act with two constitutive parts and two frames; "two tables" does not mean two
  services.
- Christ's modes of presence named by *Sacrosanctum Concilium* 7 are distinct and are not
  flattened.
- The faithful truly offer the spotless victim and learn to offer themselves; this does not make
  the assembly a collective celebrant.
- Restored function, retained text, relocated element, edited inheritance, new composition, and
  new option are distinct historical claims and are kept distinct.
- Patristic witnesses show what was already there; they are never made commentators on modern
  rubrics.
- Territorial statements are for the dioceses of the United States and are dated 25 July 2026.

## Prayer, quotation, and rights boundary

The Latin *editio typica* is quoted where the argument requires it, as evidence and not as text
for recitation. The approved 2011 English of the Order of Mass — the people's parts, the
orations, and the Eucharistic Prayers — is under copyright and is **not** reproduced. Where an
argument turns on a short English phrase whose exact wording is the point at issue, that phrase
is quoted and no more: "and with your spirit," "consubstantial with the Father," "for many,"
"under my roof." No approved English is paraphrased closely enough to reconstruct it.

Where that leaves an element without English, the study says so in that element's own place:
at the Collect, at the Prayer over the Offerings, at the Prayer after Communion, at the
dismissal formulas, and in the dedicated section on the 2011 English, which states exactly what
the constraint left undone. The Lectionary text is under copyright and is never reproduced. No
scriptural passage required quotation in English; biblical loci are cited, not quoted, so the
repository's public-domain Douay–Rheims was not needed.

## Known uncertainties and exclusions

- No exact artifact of the 2008 altar book was obtained. The 2008 state is controlled by the
  published variation list, which the 2008 notice itself says is not exhaustive of typographic
  corrections. Every 2008 claim is bounded accordingly.
- The controlling Latin artifact is a secondary digitally typeset reproduction with visible
  typesetting defects, not a page facsimile of the printed altar book.
- General Instruction chapters III and IV of the United States English state were not
  obtainable: the host returned an interstitial challenge page. Nothing rests on nn. 160 or
  281–287; the gap is declared in the Communion Rite in place.
- The authorship, date, place, and redactional unity of the *Traditio apostolica* are disputed;
  no attribution to Hippolytus is made.
- The drafting history of the new Eucharistic Prayers is not established here; promulgation by
  papal act is documented, individual authorship is not claimed.
- Prayer IV's relation to the Antiochene family is asserted at the level of form only; no
  edition of the anaphora of St Basil was examined.
- The sections of the Roman Canon are not dated severally.
- The present canonical discipline governing the 1962 Missal is out of scope.
- Independent review by a liturgical historian, a patristics specialist, a Latinist, and a
  sacramental theologian remains outstanding.

## Review record

### Initial production review — 2026-07-26

Sources were acquired and read on 25 July 2026 (UTC dates of the working session; the document
timestamp is 2026-07-26T03:14:06Z). The Latin Missal reproduction and the 2008 *Notitiae* issue
were re-downloaded and found byte-identical to their registered artifact hashes. The 1962
facsimile, the Migne PL 16 leaves, and the Hauler leaves were read at rendered page images
rather than OCR.

A settled two-pass build produced a 38-page PDF. The final log contained no fatal error,
undefined reference, overfull or underfull box, or unresolved rerun or layout warning.
Generation metadata validated (one canonical record). The web edition converted, retaining every
section, all 91 notes, the generation-metadata disclosure, and the rights colophon.

Review rasters were generated through `scripts/pdf-review` into a session-private output
directory (the shared `build/pdf-review` root was being cleared by concurrent work) and every
rendered page was inspected. Three defects were found and corrected: six endnote markers
orphaned onto their own lines after tables and framed blocks, which printed as stray numerals
(fixed by attaching each note to the sentence introducing its block); a References entry opening
with a bracketed phrase that LaTeX took as an optional item label and set clipped in the left
margin; and a chronologically misordered pair of rows in the development timeline. All pages
were re-inspected after the correction.

This is internal production review only. It grants no independent editorial, specialist,
rights, theological, or ecclesiastical approval, and no release clearance attaches to these
bytes.
