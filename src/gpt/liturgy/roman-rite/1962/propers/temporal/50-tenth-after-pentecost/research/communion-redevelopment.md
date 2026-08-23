# Communion redevelopment record

## Scope

This record controls only the Tenth Sunday after Pentecost Communion,
`Acceptabis sacrificium iustitiae`. It separates the appointed 1962 antiphon,
the complete biblical verse, direct reception, and related chant uses. It does
not revise shared bindings or the assembled document while parallel component
work is active.

## Textual correction

The 1962 *Missale Romanum*, item 1540, prints:

> Acceptabis sacrificium iustitiae, oblationes et holocausta, super altare
> tuum, Domine.

The complete Vulgate Psalm 50:21 reads:

> Tunc acceptabis sacrificium iustitiae, oblationes et holocausta; tunc
> imponent super altare tuum vitulos.

The antiphon omits both `tunc` clauses and the calves, retains the sacrificial
nouns and altar phrase, and adds `Domine`. The current appointed-text section
correctly transcribes that Latin but pairs it with the complete Douay–Rheims
verse, including both “then” clauses and “then shall they lay calves upon thy
altar.” Those words are not appointed and must not be printed as though they
translated the antiphon. Recommended replacement:

> Thou shalt accept a sacrifice of justice, oblations and whole burnt
> offerings, upon thy altar, O Lord.

This is an editorially literal translation of the appointed Latin and must be
labeled as such. The complete registered Douay–Rheims verse remains useful as
canonical context, but belongs in exposition or a clearly labeled context
note.

## Direct reception checked

- Augustine, *Enarratio in Psalmum 50* §23 is the direct verse locus. The
  previous §21 citation is wrong: §21 treats verses 18–19 and the one saving
  sacrifice prefigured by former victims. Section 22 treats
  Zion and Jerusalem; §23 treats verse 21, identifying the sacrifice of
  justice with praise and the holocaust with the whole person taken by divine
  fire, including bodily immortality. The local passage does not specifically
  identify verse 21 with Eucharistic oblation. These are received Christian
  readings, not the literal-historical horizon and not evidence of the Roman
  antiphon's compilation.
- Aquinas, *Super Psalmo 50*, Corpus Thomisticum paragraph 87290, gives three
  readings of the verse. The first includes Christ's self-offering and the
  saints' self-offering; another treats works of justice and mercy as
  sacrifice and complete dedication as holocaust. Report the plurality rather
  than presenting one gloss as exhaustive.
- Theodoret, *Interpretatio in Psalmum 50*, PG 80, cols. 1252–1256, reads the
  close as a plea for pity on the city, restoration of its former prosperity,
  rebuilding of the walls, and worship according to the Law. Use as
  literal-historical reception, not as proof of a securely dated redactional
  history.
- The NABRE note to Psalm 51:20–21 reports that “most scholars” regard these
  verses as a post-587 addition associated with the rebuilt Temple. Attribute
  that judgment precisely and retain it as historical-critical orientation,
  not certainty or a reason to fragment the received canonical text.

## Chant reception and limits

The exact 1962 Communion form is attested by the edition-identified Missal.
Hesbert's *Antiphonale Missarum Sextuplex* registers the Communion at Thursday
after Ash Wednesday (no. 38, witnesses B C K S) and the Tenth Sunday after
Pentecost (no. 182, witnesses R B K S). The Gregorian index also catalogs
manuscript loci and a Mode IV melody, but those indexed leads have not all
been visually checked.

The published exposition may say that the chant had more than one early
medieval Mass assignment. It may not say which assignment originated first or
why, infer the age of the later Mode IV melody, or use an index as a
substitute for checking a named manuscript image.

## Replacement block for the shared research matrix

| Passage and proper | Direct ancient exegesis checked | Medieval and chant reception checked | Retained use and material negatives |
| --- | --- | --- | --- |
| Ps 50:21, liturgically adapted (Communion) | Augustine, *Enarratio in Ps. 50* §§21–23, with the source verse at §23; Theodoret, PG 80, cols. 1252–1256 | Aquinas, *Super Psalmo 50*, id 87290; Hesbert, *Antiphonale Missarum Sextuplex* nos. 38 and 182 | The Missal omits both `tunc` clauses and the calves, retains sacrifice and altar, and adds `Domine`; its English must follow the antiphon. Theodoret's restored-city reading, Augustine's praise and whole-person holocaust, and Aquinas's Christological, ecclesial, moral, and eschatological senses remain distinguishable. None proves compiler intent or makes the verse direct Eucharistic commentary. The NABRE note reports a majority post-587 hypothesis for vv. 20–21, not certainty. |

## Proposed binding additions for serialized integration

The shared `research/source-bindings.toml` should add or bind the following
only after canonical source records exist and their exact identifiers and
fingerprints have been verified:

```toml
[[bindings]]
source_id = "passage.augustine.enarrationes-in-psalmos.[edition].psalm-50-21-23"
loci = ["Enarratio in Psalmum 50, sections 21-23; verse 21 at section 23"]
role = "reception"
states = ["cataloged", "acquired", "inspected", "verified"]
context = "Direct reception of the Communion's psalm verse; sections 21-22 preserve the contrition-and-Zion sequence, while section 23 treats the appointed verse."

[[bindings]]
source_id = "passage.thomas-aquinas.super-psalmos.[edition].psalm-50-87290"
loci = ["Super Psalmo 50, paragraph 87290"]
role = "reception"
states = ["cataloged", "acquired", "inspected", "verified"]
context = "Direct medieval reception of Psalm 50:21 through Christ's sacrifice, saintly self-offering, works of justice and mercy, and whole self-dedication."

[[bindings]]
source_id = "passage.theodoret-of-cyrus.interpretatio-in-psalmos.[edition].psalm-50-cols-1252-1256"
loci = ["PG 80, columns 1252-1256"]
role = "reception"
states = ["cataloged", "acquired", "inspected", "verified"]
context = "Direct Greek reception of Psalm 50's closing movement, used with its historical and genre limits."
```

Do not invent the bracketed edition keys or fingerprints. The controlling
Missal binding already proves the appointed shortened form. The registered
Douay–Rheims artifact should retain `Ps.50.21` as canonical context, but it
must no longer be described as controlling a verbatim English translation of
this shortened antiphon.

## Sources checked

- *Missale Romanum* (Vatican typical edition, 1962), printed pp. 389–390,
  item 1540: controlling appointed text.
- Augustine, *Enarratio in Psalmum 50* §§21–23, Latin text at
  `augustinus.it/latino/esposizioni_salmi/esposizione_salmo_066_testo.htm`.
- Thomas Aquinas, *Super Psalmo 50*, paragraph 87290, Latin/English display at
  `isidore.co/aquinas/PsalmsAquinas/ThoPs50H51.htm`; canonical Corpus
  Thomisticum locus to be preferred in publication.
- Theodoret of Cyrus, *Interpretatio in Psalmos*, PG 80, cols. 1252–1256, as
  checked in the parent research audit.
- René-Jean Hesbert, *Antiphonale Missarum Sextuplex*, nos. 38 and 182;
  Gregorian-index manuscript listings used as discovery and concordance
  evidence only unless exact folios are visually checked.
- NABRE Psalm 51 and note to verses 20–21 at
  `bible.usccb.org/bible/psalms/51`, for the expressly attributed
  historical-critical orientation.
