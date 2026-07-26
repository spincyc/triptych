# Source audit

Machine-checkable identities, hashes, loci and fingerprints are in
`source-bindings.toml`. This record states what each source was used *for*,
what the verification ceiling is, what was checked and corrected, and what
remains open.

## 1. Verification ceilings

| Source | Ceiling asserted |
| --- | --- |
| 1962 *Missale Romanum* (CMAA facsimile) | visual reading of the identified page images by the authoring agent; the artifact was re-downloaded publication-locally and hashed identically to the registered record before use. Some front-matter loci were read in the artifact's embedded text layer and are marked as such on their passage records. |
| 1861 Cummiskey hand missal | visual reading of the Internet Archive page renditions of the exact hashed scan. |
| Douay-Rheims (Challoner, PG 1581) | exact reading of the tracked verse-text artifacts held in this repository. |
| Trent, Tauchnitz 1887 | visual reading of the page images of printed pp. 118, 119, 120, 121. |
| Trent, Waterworth | visual reading of the page images of printed pp. 156 and 159. |
| *Patrologia Latina* XVI | visual reading of the page images of coll. 462-464. |
| Fortescue, *The Mass* | visual reading of the page images of pp. 172, 227, 232, 234-235, 288, 305, 387, 394. |
| *AAS* 54 (1962) p. 873 | reading of the rendered text of the Vatican archive scan. |
| *AAS* 52 (1960) pp. 593-596 | optical text layer only; identity and dates, not wording. Cited for the acts' existence and dates, which the 1962 Missal's front matter independently supplies. |

No claim in the publication rests on OCR alone for wording. The 1962 facsimile's
embedded text layer was used as a finding aid throughout and every quoted block
was then read at the page image.

## 2. Audit performed on the draft (26 July 2026)

Every rubric statement in the draft was treated as unverified and re-checked
against the facsimile page images. Results:

**Confirmed against the images.**
- n. 424, the six Masses from which the psalm, antiphon, confession,
  absolution, versicles, `Aufer a nobis` and `Oramus te` are all removed.
- n. 425, the omission of `Iudica me` in Masses *de Tempore* from Passion
  Sunday to Maundy Thursday and in Requiems, together with the `Ordo Missae`
  rubric between nn. 1016 and 1017, which adds *inclusive*.
- nn. 427-430 (introit shape, `Gloria Patri`, `Kyrie … novies`), 431-432
  (`Gloria`), 466-476 (lessons, Gospel, homily, Creed), 480-482, 487-499
  (prefaces), 500-503, 507-510, 511-512.
- The 1962 spellings `Genetricis`, `neglegentiis`, `exspecto`, `cotidianum`.
- The full stop after `Iesu Christe` in `Tu solus Altissimus, Iesu Christe. Cum
  Sancto Spiritu` (artifact p. 300), on which an editorial note depends.
- The preface count of sixteen and the boundary between the chanted and
  unchanted series at artifact pp. 364-365 (printed 283/284).
- The absence of any scriptural reference at n. 1128, where the book prints one
  at nn. 1037 and 1039 (artifact p. 402).
- The Saint Joseph clause in both the ordinary `Communicantes` (n. 1090) and
  the shared continuation of the proper forms (printed p. 305), against its
  absence in the 1861 book.

**Corrected.**
1. *`Infra Actionem` numbering.* The draft said the proper forms of `Hanc
   igitur` were printed at nn. 1098-1099. The page image of artifact p. 386
   shows n. 1098 reprinting the **ordinary** `Hanc igitur`, n. 1099 carrying
   the one proper form (Easter Vigil to Low Saturday and Vigil of Pentecost to
   the following Saturday), and n. 1100 reprinting `Quam oblationem`. The
   passage now describes the layout provision correctly.
2. *Saints counted in the Canon.* The draft said the `Nobis quoque` list held
   "seven men and seven women" while printing eight men, and said the Canon
   names "twenty-nine saints". The printed lists hold twenty-six names in
   `Communicantes` and fifteen in `Nobis quoque`: forty-one in all, eight men
   and seven women in the second list. Corrected in both places.
3. *Martyrs of the `Communicantes`.* The draft said "four pairs" and then named
   one solitary and two pairs. Corrected.
4. *Source of the incense blessing.* The draft derived `stantis a dextris
   altaris incensi` from Apocalypse 8, 3. That verse has an angel with a censer
   before the altar but no angel at its right; the borrowed phrase is Luke 1,
   11. Corrected, and the rejected identification is recorded as a `lead`
   binding so it cannot be silently reintroduced.
5. *Trent citations.* Two claims (session XXII chapter III on Masses in honour
   of the saints, and chapter VII on the water) were carried without source
   records. Chapter VII stood on an already registered page; chapter III did
   not, so `sessio-22-decretum-3` and the artifact `leaf-125-image` were
   created and the page was read. Both quotations are now exact, including the
   Tauchnitz `coelis` and the council's `facimus` against the Missal's
   `agimus`.
6. *Fortescue on the Kyrie.* Pages 232 and 234 were cited without records, and
   the supporting matter runs onto p. 235. `p-232` and `p-234-235` were created,
   the pages read, and the paragraph rewritten to quote Gregory's letter as
   Fortescue prints it and to add his express rejection of John the Deacon's
   ascription.
7. *Chant settings of `Ite, missa est`.* Counted at the page images: eight
   under n. 1134, not seven, and all under one marginal number.
8. *Presentation of the opening antiphon.* An `appointed` block carried an
   editorial `Ant.` label the missal does not print. Replaced by the book's own
   rubric cues.

**Left open.**
- The identity of the `sanctus Angelus tuus` of `Supplices`. The tradition has
  never agreed; the Milanese parallel's plural `angelorum tuorum` is a datum,
  not a solution.
- Andrew's presence, alone beside Peter and Paul, in `Libera nos`. No
  consulted source explains it.
- The internal disagreement in the 1962 volume about the date of *Rubricarum
  instructum* (23 versus 25 July 1960).

## 3. Rights

| Material | Status |
| --- | --- |
| 1962 Latin liturgical text | old enough to be public domain in the United States; quoted as evidence in framed blocks, never offered for recitation |
| CMAA facsimile bytes | rights `unresolved`; recorded by hash, not retained, not redistributed |
| 1861 English | public domain in the United States by publication date |
| Cummiskey scan bytes | Google digitisation, rights `unresolved`; recorded by hash, not retained |
| Douay-Rheims Challoner text | public domain; tracked artifacts already held in this repository |
| Trent (Tauchnitz 1887, Waterworth 1848), *PL* XVI (1880), Fortescue (1922) | public domain in the United States by age of publication; page images recorded by hash, not retained |
| *AAS* 52 and 54 | official acts; cited, not reproduced |

No English wording in the publication is a translation made by its author.
Where an English wording of a prayer appears it is quoted from the 1861 book at
an identified page; where no public-domain English witness exists the
publication writes third-person analysis and says that it is doing so.

## 4. Relations to other publications

- The Claude study of the postconciliar Order of Mass
  (`liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/ordinary/00-order-of-mass`)
  holds that the alteration of the dominical words is the deepest textual change
  between the two books. This study supplies one half of that comparison — the
  1962 chalice form with `mysterium fidei` and `Haec quotiescumque feceritis`,
  read at artifact p. 388 — and states the agreement explicitly in its
  synthesis. Neither study is a dependency of the other; the shared ground is
  the wording of the 1962 forms, and it is verified independently on each side.
- The 1962 assembly and calendar references under
  `liturgy/roman-rite/1962/reference/` use the same controlling facsimile and
  the same marginal-number locator system. No fragment is shared and no text is
  imported.

## 5. Review state

Source-audited 26 July 2026 by the authoring agent against the records above.
No independent specialist, historical, liturgical, theological or canonical
review has taken place, and no such label is claimed.
