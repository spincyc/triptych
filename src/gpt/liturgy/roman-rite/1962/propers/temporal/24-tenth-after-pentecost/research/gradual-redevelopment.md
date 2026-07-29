# Gradual redevelopment record

This focused record supports the replacement Gradual commentary in
`sections/20-gradual-redevelopment.tex`. It supplements, and does not silently
rewrite, the work-wide research scope and source bindings.

## Text and ordering

- The controlling 1962 Missal prints Psalm 16:8 and 2 in that order:
  `Custodi me, Domine, ut pupillam oculi: sub umbra alarum tuarum protege me`,
  then `De vultu tuo iudicium meum prodeat: oculi tui videant aequitatem`.
- The selected Latin begins within verse 8 and omits
  `a resistentibus dexterae tuae`. The former English block reproduced that
  unappointed clause from the complete Douay--Rheims/Challoner verse; the
  corrected block begins at “Keep me as the apple of thy eye.”
- The chant reverses the canonical order of verses 2 and 8. Any account of a
  protection-to-judgment movement is a textual observation about the appointed
  order, not the Psalm's native sequence or evidence of compiler intent.

## Reception and exact loci

- Thomas Aquinas, *Super Psalmo 16*, no. 1
  (`Corpus Thomisticum` identifier 86899): while expounding the opening
  `non in labiis dolosis`, Aquinas explicitly contrasts Luke 18's Pharisee,
  who was not heard, with the other worshiper who prayed rightly, was heard,
  and descended justified. This directly bridges the Psalm's immediate
  canonical context to the appointed Gospel, but does not directly expound
  the Gradual's selected verses.
- Aquinas, *Super Psalmo 16*, no. 1, on verse 2: judgment comes from divine
  knowledge; Aquinas distinguishes equity accommodated to human nature from
  severity. No. 3 (identifier 86901), on verse 8: the pupil signifies
  diligent and safe protection; further Christological, moral, angelic, and
  Passion readings are alternatives received through the Gloss.
- Augustine, *Enarratio in Psalmum 16*, §§2, 8: Christ-and-body voice and a
  Christological reading of the pupil. These are spiritual reception, not an
  exclusive historical sense.
- Cassiodorus, *Expositio in Psalterium*, Psalm 16, §§8 and 14: God's sight
  supplies judgment without external testimony; the pupil is precious and
  discerning, and wings signify protection, mercy, and charity. These exact
  loci replace the opaque and inaccurate “local vv. 9 and 3.”
- Theodoret of Cyrus, *Interpretatio in Psalmos*, PG 80, cols. 968--969:
  divine discernment and shelter. This locus is retained only at the bounded
  level independently checked.
- Jerome, *Epistula 106*, §8, to Sunnia and Fretela: on Psalm 16:2 he defends
  `oculi tui` against Greek copies reported as `oculi mei`; on Psalm 16:8 he
  says `Domine` is absent from Hebrew and the other translators. These are
  recensional observations, not corrections to the Missal.

## Required work-wide integration

The serialized integrator should:

1. Replace the present combined Gradual/Alleluia detailed-commentary
   subsection with separate element subsections, importing
   `sections/20-gradual-redevelopment.tex` for the Gradual.
2. Update the Gradual row of the reception matrix with Aquinas's direct
   Luke-18 bridge and the exact Cassiodorus and Jerome loci above.
3. Add only actually used references and repository source bindings. Minimum
   reference loci are Aquinas, *Super Psalmo 16*, nos. 1 and 3; Cassiodorus,
   Psalm 16 §§8, 14; and Jerome, *Letter 106*, §8.
4. Preserve the distinction between the Missal's appointed text, the full
   biblical verse, canonical context, and later reception.
