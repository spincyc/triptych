# Eighth Sunday after Pentecost — source audit

Provider: Anthropic Claude. Every check below was performed on **2026-07-25**
against the named witness. "Checked" means the passage was retrieved and read at
the stated locus in the stated witness; it does not assert collation against a
critical edition or a print original except where page images are expressly
recorded. No search, source, or verification event is recorded here that did not
occur. Search boundaries, negative results, and unresolved leads are in
`scope.md`.

## 1. The controlling missal — verified by page image

Witness: Church Music Association of America facsimile of the *Missale Romanum*,
editio typica (Vatican City, 1962),
<https://media.churchmusicassociation.org/pdf/missale62.pdf>, downloaded
2026-07-25, SHA-256
`648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` — identical
to the hash on the tracked artifact manifest, so the exact remote bytes are
confirmed. Pages were rendered at 300 dpi and read column by column.

| Locus (printed / PDF) | Claim served | Evidence state |
|---|---|---|
| pp. 387–388 / 468–469 | the ten appointed elements, their headings, marginal nos. 1512–1521, scriptural references, wording, punctuation, accents, ligatures; `Credo` after the Gospel; `Præfatio de Ssma Trinitate` after the Secret; the formulary's opening and closing boundaries | image-collated; verified |
| p. 387 / 468 | printed heading `DOMINICA OCTAVA post Pentecosten` and rank `II classis` | image-collated |
| p. XII / 10 | `Rubricæ generales` nn. 10, 11, 12, 14, 16, 17: Sundays are of class I or II; the list of class I Sundays; `Omnes aliæ dominicæ sunt II classis`; impeded Sundays are neither anticipated nor resumed; a class II Sunday is preferred to class II feasts, except that a class I or II feast of the Lord takes its place with no commemoration, and except the Commemoration of All the Faithful Departed | image-collated. Printed page number confirmed by reading the running header of the following leaf (p. XIII) |
| p. 382 / 463 | the Fourth Sunday after Pentecost's Epistle is `Rom. 8, 18-23` | heading image-collated |
| p. 467 / 548 | the Purification of the B.V.M., no. 2107: Introit `Suscépimus, Deus, misericórdiam tuam`, reference `Ps. 47, 10-11`, psalm verse `Ps. ibid., 2`, `℣. Glória Patri` — verbatim identical to no. 1512 | image-collated |
| pp. 384–390 / 465–471 | the epistle sequence of the Sundays after Pentecost VI (Rom 6:3–11), VII (Rom 6:19–23), VIII (Rom 8:12–17), IX (1 Cor 10:6–13) | headings read in the facsimile's text layer and confirmed against the page images for VIII; VI, VII and IX read in the text layer only |

Limit: the facsimile's own embedded text layer is ABBYY OCR and was used only to
locate leaves. It is retained unedited in `../propers/retrieved.txt`, SHA-256
`95adec9b9f246e98412a52640cc284458141841aff716b1b271e5932fa6ac6ed`.

## 2. The English witness — verified by page image

Witness: *The Roman Missal translated into the English language for the use of
the laity* (Philadelphia: Eugene Cummiskey, 1861), Internet Archive item
`romanmissaltran00churgoog`, <https://archive.org/details/romanmissaltran00churgoog>.
Internet Archive metadata records `possible-copyright-status: NOT_IN_COPYRIGHT`;
the 1861 imprint is in any event long out of copyright in the United States.

| Locus | Claim served | Evidence state |
|---|---|---|
| p. 411 (leaf 419) | English of the Introit, Collect; the printed footnote "Introit for Candlemas-Day also" | page image read |
| p. 412 (leaf 420) | English of the Epistle, Gradual, Alleluia, and the opening of the Gospel; the Latin of the Alleluia printed as `et laudabilis valde` | page image read |
| p. 413 (leaf 421) | English of the rest of the Gospel, `CREDO`, Offertory, Secret, Communion, Postcommunion | page image read |

Leaf-to-printed-page mapping taken from the item's `scandata.xml`. The 1843
Philadelphia printing of the same translation (`romanmissaltran00englgoog`,
pp. 411–413) was read in OCR and agrees; it independently attests the
`nimis`/`valde` split in the Introit and Alleluia.

Limits recorded in the publication: this is a nineteenth-century hand-missal
translation, not an approved liturgical translation; its rank headings are
pre-1962; it silently drops `propítius` in the Collect and renders the Gradual's
`in locum refúgii` as "a place of refuge," where the Douay of Ps 30:3 has "a
house of refuge."

## 3. Scripture — checked

Witness: drbo.org, Clementine Vulgate (`/lvb/chapter/…`) and Douay–Rheims
(`/chapter/…`), read 2026-07-25.

| Locus | Claim served |
|---|---|
| Ps 17:27–28, 31–32 (Lat. and Eng.) | the Offertory collation; the psalm's turn from rescue to a general rule |
| Ps 17:1 (Eng.) | the superscription naming deliverance from Saul |
| 2 Kings (2 Sam) 22:1 (Eng.) | the same occasion clause; the doublet |
| Ps 30:2–4 (Lat. and Eng.) | the Gradual collation; `in domum refugii`; the overlap with Ps 70 |
| Ps 33:1–2, 8–10 (Lat. and Eng.) | the Communion collation; the psalm title naming Achimelech |
| 1 Kings (1 Sam) 21:10–15 (Eng.) | the king of Geth named *Achis* |
| Ps 47:1–2, 10–11 (Lat. and Eng.) | the Introit and Alleluia collation; `sic` against the missal's `ita`; `laudabilis nimis` |
| Ps 70:1–3 (Lat. and Eng.) | the Gradual-verse collation; `in locum munitum`; the Rechabite title |
| Luke 16:1–13 (Lat. and Eng.) | the Gospel collation; the unread vv. 10–13 |
| Rom 8:12–18 (Lat. and Eng.) | the Epistle collation; `hi filii Dei sunt`; the unread second half of v. 17 |

Limit: drbo.org is a mutable web presentation of the Clementine text and the
Challoner Douay–Rheims. It is used as the standard of comparison and for
canonical context; it never controls the appointed wording.

## 4. Patristic and medieval witnesses — checked at work and locus

### Augustine

| Work and locus | Claim served | Witness | Limit |
|---|---|---|---|
| *Enarr. in Ps.* 17.28, 17.32 | the humble as the self-accusing, the proud through Rom 10:3; God as "the hoped-for inheritance" possessed by the sons | newadvent.org/fathers/1801018.htm | NPNF English; page titled "Psalm 18"; inline verse numbers one lower than the Vulgate |
| *Enarr. in Ps.* 30 (Enarratio I) §§1, 3 | the Mediator speaks first, then the redeemed people; the gloss on `esto mihi in Deum protectorem`; the lemma `in domum refugii` | .../1801031.htm | NPNF carries Enarratio I only |
| *Enarr. in Ps.* 33 (sermo 2) §§1, 11 | Christ "carried in His Own Hands"; `Hoc est corpus meum`; John 6:52–53; "if you understand not, you are king Achis" | .../1801034.htm | the page prints sermo 2 only, so its section numbers do not match the Latin edition |
| *Enarr. in Ps.* 47 §§2, 8, 9 | Daniel 2:35 and the mountain that came to us; the lemma `in medio populi tui` and the threshing-floor argument; universality against the sectarian remnant; John 1:12 at the close of §8 | .../1801048.htm | **the §8 lemma is `populi`, not `templi`** — recorded in the publication as a limit on citing Augustine here |
| *Enarr. in Ps.* 70 (sermo 1) §§3, 5 | the lemma `Deus, in te speravi; Domine, non confundar in aeternum`; "confounded in Adam"; "God Himself has become the place of your fleeing unto" | .../1801071.htm | |
| *De spiritu et littera* 32.56 | "Abba, Father" as circumcision and uncircumcision in one cry | .../1502.htm | |
| *Sermo* 113 (NPNF Sermon 63) §§1–2 | the saints and the `minimi` as receivers; mammon as Hebrew cognate to Punic; the refutation of plunder-then-give; "give alms of your righteous labours"; "you cannot corrupt Christ your Judge" | .../160363.htm | |
| *Quaest. Evang.* II.34 | "not everything is for imitation"; `non enim domino nostro facienda est in aliquo fraus`; the `e contrario` structure; riches only to the wicked; the receivers are the just and holy, not God's debtors | Latin as transmitted in Aquinas, *Catena aurea in Lucam* c. 16 l. 2, corpusthomisticum.org/clc14.html | quoted from the *Catena*'s clean Latin; the underlying work is named |

### Others

| Work and locus | Claim served | Witness | Limit |
|---|---|---|---|
| Ambrose, *Exp. in Lucam* VII.245 | `Nec reprehenditur villicus … praedicatur`; the allurement reading; angels and saints as receivers | *Patrologia Latina* text at mlat.uzh.ch (PL 15 col. 1764); the allurement and angels sentences also in the *Catena*, c. 16 l. 2 | machine-read Migne; §-number is Migne's. **Negative result: Ambrose does not treat the narrative of vv. 1–8 at all**; his chapter XVI covers vv. 13, 9, 12 in that order |
| Jerome, *Ep.* 121 ad Algasiam q. 6 | the defrauded master's praise; fraud toward the master, prudence for himself; `mamona` as Syriac; the parable as exhortation to remit debts; `non quoslibet pauperes`; the method statement against finding definite persons in a parable; Theophilus of Antioch's allegory; the negative result on Origen and Didymus | *Patrologia Latina* text at mlat.uzh.ch (PL 22 coll. 1018–1021) | machine-read Migne; New Advent's page for this letter prints only the list of questions, without the answers |
| John Chrysostom, *Hom. in Rom.* XIV | debtors to the Spirit; grace before debt; the flesh as follower not leader; adoption named instead of freedom; the spirit of bondage as the letter; `Abba` as Hebrew and as the initiate's first word; joint-heirship | newadvent.org/fathers/210214.htm | NPNF English; the homily opens on Rom 8:12–13, so the whole appointed lection falls inside it |
| John Chrysostom, *Hom. in Heb.* I | "it is not they who receive us, but our own work"; the argument from the absent possessive | newadvent.org/fathers/240201.htm; Latin form in the *Catena*, c. 16 l. 2 | illuminating reuse, not commentary on the pericope — labelled as such in the publication |
| Gregory the Great, *Moralia* XXI.19.29 | the poor as `patroni` | *Catena aurea* c. 16 l. 2 | cited as transmitted; **negative result: Gregory has no homily on this pericope** (*Hom. in Ev.* 40 is Dives and Lazarus) |
| Bede, *In Lucam* V | every possessor of money is a steward; the excuses eschatologised (the foolish virgins); `prudentiores in generatione sua` limited against Isaiah's woe; "whose works a man does, of him he is called a son" | *Patrologia Latina* text at mlat.uzh.ch (PL 92 coll. 528–531) | machine-read Migne. Its `cui fraudem faciebat` differs from Augustine's `qui`; **the variant is not used and no claim rests on it** |
| Cyril of Alexandria, *Comm. in Lucam*, Sermon 108 | the refusal to allegorise; the rich man as the accused steward; the lemma "when it has failed"; the translator's note on the tense | R. Payne Smith's translation from the Syriac, Internet Archive `p2commentaryupon00cyriuoft`, pp. 507–510 | a nineteenth-century English translation from Syriac, read in archive.org OCR; not the Greek |
| Basil; Theophylact; "Origen" | inherited injustice in a patrimony; goods given for the brethren's need; the commendation as `abusive dictum` | *Catena aurea* c. 16 l. 2 | **cited at the level of transmission only**; the underlying works were not opened. The "Origen" attribution is expressly bounded in the publication, since Jerome reports he could not find Origen on this parable |
| Theophilus of Antioch | the allegory of the rich man as God and the steward as Paul | inside Jerome, *Ep.* 121 q. 6 | survives, so far as this search established, only there; cited as *apud Hieronymum* |

## 5. Thomas Aquinas — checked

Witness: corpusthomisticum.org, read 2026-07-25.

| Locus | Claim served | URL |
|---|---|---|
| *Super Rom.* c. 8 l. 2 | `ergo debitores sumus spiritui sancto propter beneficia ab eo recepta` | /cro05.html |
| *Super Rom.* c. 8 l. 3 | the Spirit's leading and free will with Phil 2:13; `abba` Hebrew and `pater` Latin or Greek for the two peoples; `clamamus` as intensity of heart with Ex 14:15; heir as receiver of the principal goods with Gen 25:5; `bonum autem principale quo Deus dives est, est ipsemet`; the objection from the father's death and the two answers; `cohaeredes autem Christi, quia ipse … est principalis haeres`; `non autem nos faciliori modo debemus haereditatem adipisci` | /cro05.html |
| *ST* III q. 23 aa. 1–4 | adoption makes the adopted fit by grace; a. 1 ad 3 `sine detrimento patris semper viventis` and the citation of the Gloss on Rom 8; a. 2 adoption is the whole Trinity's; a. 3 only the rational creature having charity; a. 4 Christ is in no way an adopted son | /sth4016.html |
| *ST* II-II q. 32 a. 7 | arg. 1 from Lk 16:9; `sed contra` from Augustine's sermon; the threefold distinction on ill-gotten goods (restitution owed; simony; `turpe lucrum`); ad 1 stacking Augustine's two readings, Ambrose's, Basil's, and `iniquitatis, idest inaequalitatis` | /sth3027.html |
| *ST* I-II q. 114 a. 6 ad 3 | the three modes in which the poor "receive" into eternal dwellings: impetration, congruous merit, and "materially speaking" | reported from the *Summa*'s text; the article was identified through the research pass and its content is used only at this level of generality |
| *Catena aurea in Lucam* c. 16 l. 1–2 | the checked Latin transmission of Augustine, Ambrose, Gregory, Chrysostom, Basil, Theophylact and "Origen" on this pericope | /clc14.html (the file carries capp. 14–18) |

Limit: Corpus Thomisticum prints Busa index numbers, not Marietti paragraph
numbers, for the Pauline commentaries. No Marietti number is claimed.

## 6. Documented later uses — checked

| Source | Locus | Witness | Rights |
|---|---|---|---|
| Trollope, *The Way We Live Now* (1875) | ch. LXXXI, "Mr. Cohenlupe Leaves London" | Project Gutenberg ebook 5231; chapter identified from the body heading preceding the passage | public domain |
| Trollope, *Barchester Towers* (1857) | ch. XXXIX, "The Lookalofts and the Greenacres" | PG ebook 3409 | public domain |
| Kingsley, *Westward Ho!* (1855) | ch. XVIII, "How They Took the Pearls at Margarita" | PG ebook 1860 | public domain |
| Ruskin, *Sesame and Lilies* (1865) | lecture I, "Of Kings' Treasuries" | PG ebook 1293 | public domain |
| UK House of Commons | Representation of the People (No. 2) Bill, 3 February 1931, HC Deb vol. 247, cc. 1662–1664 | Historic Hansard, api.parliament.uk | Parliamentary copyright; Open Parliament Licence |

Every quotation printed in the guide was read in the witness named here. Chapter
numbers were determined from the running chapter headings in the source texts,
not from a secondary index.

## 7. Repository source-library records bound

Bindings are declared in `source-bindings.toml`. The CMAA facsimile artifact
already existed in the provider-neutral source library and was bound, not
created; its recorded hash was independently reproduced by this edition on
2026-07-25. No new source-library record was required for this leaf, and none
was created.
