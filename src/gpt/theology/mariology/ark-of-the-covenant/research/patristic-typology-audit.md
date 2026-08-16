# Patristic, Saintly, and Liturgical Ark Typology Audit

This audit supports `sections/70-choir-of-witnesses.tex`. It records the
evidence state as of 2026-08-15 and distinguishes authenticated direct
witnesses, checked paraphrases, liturgical reception, traditional but
pseudonymous reception, project synthesis, and rejected attributions.

The governing posture is Catholic ressourcement. Textual and attribution
control protects rather than weakens the patristic case: a secure fourth- and
fifth-century chain, later Byzantine and Latin development, and present Roman
worship remain fully visible without assigning anonymous texts to famous
authors or forcing an early witness to state a later definition verbatim.

## Verification legend

- **D — direct authenticated witness:** the work and locus are accepted and
  directly identify Mary with the Ark or develop the correspondence.
- **T — transmission-qualified direct witness:** the work is accepted, but the
  relevant text survives in an ancient translation or materially later
  manuscript; the transmission state is named in publication.
- **C — critical-locus controlled:** a critical edition and exact locus have
  been identified; published prose paraphrases the substance rather than
  claiming a fresh critical translation.
- **W — working primary text:** the exact locus was inspected in a public-domain
  or scholarly working text that is not represented as the controlling critical
  edition.
- **L — liturgical reception:** an identifiable Greek, Byzantine, Syriac, or
  Roman liturgical text directly applies Ark language to Mary.
- **O — official reception:** an official Holy See or authority-owned text was
  checked at the named locus.
- **M — magisterially received application:** a saintly, patristic, biblical,
  or liturgical image is explicitly received in a modern magisterial text. The
  marker identifies that reception; it does not turn the image into the
  definition or its solitary proof.
- **R — traditional reception with attribution qualification:** the wording is
  evidence of Christian reception, but not of the famous author or date under
  which it once circulated.
- **S — source-grounded project synthesis:** the publication's constructive
  conclusion from identified witnesses; not assigned verbatim to a Father.
- **X — rejected for the claimed use:** the locus does not say Mary is the Ark,
  or the attribution would materially misdate or misstate the evidence.

## Repository-first result

The required exact repository search found extensive Bible corpora, the
catalog-level John Damascene Dormition record, and existing Mariology audits,
but no provider-neutral passage record already controlling the direct
Mary-as-Ark patristic chain.

Reusable local records include:

- `src/sources/works/john-of-damascus/homilies-on-the-dormition/work.toml`;
- `src/sources/works/john-of-damascus/homilies-on-the-dormition/editions/english-allies-london-1898/edition.toml`;
- `src/gpt/theology/mariology/marian-dogmas/research/source-audit.md`, which
  supplies the existing dogmatic and typological limits;
- the public-domain Bible witnesses under `src/sources/bibles/` and
  `src/sources/works/`.

No source-library text is silently treated as a critical patristic edition.

## Authenticated chronological spine

| Date | Author, work, and exact locus | Language and source control | Status | Published use and boundary |
| --- | --- | --- | --- | --- |
| fourth century, before 373 | Ephrem the Syrian, *Hymns on the Nativity* 16.16–17 and 4.112–13; Edmund Beck, *Des heiligen Ephraem des Syrers Hymnen de Nativitate (Epiphania)*, CSCO 186/187, *Scriptores Syri* 82/83 (1959) | Genuine Syriac Ephrem; Beck's critical Syriac/German loci are identified, but this project did not perform a fresh direct Syriac collation. | D / C | At 16.16–17 Ephrem pictures Joseph rising to minister before his Lord dwelling in Mary, as a priest before the Ark because of divine holiness; Moses' stone tablets are contrasted with the pure tablet in whom the Creator's Son dwells. At 4.112–13 Mary is “that Ark,” whose hidden indwelling power overthrows Satan as the captured Ark overthrew Dagon. Earliest secure direct witness in this audit and a positive virginal-service source. The alpha uses independently worded paraphrase checked against identified translations; it publishes no direct English quotation from Beck or the Syriac. |
| 392 | Epiphanius of Salamis, *De mensuris et ponderibus / On Weights and Measures* §35, CPG 3746; James Elmer Dean, *The Syriac Version of Epiphanius' Treatise on Weights and Measures*, SAOC 11 (1935), pp. 52–54, Syriac folios 65b–65d | Greek work; the complete relevant passage survives in Syriac. Dean's English was checked as a working translation, but no public-domain conclusion is relied upon. One manuscript variant reads “new” where Dean prints “living.” | T / W | Directly calls Mary the holy/living Ark prefigured in the wilderness; contrasts written and living Word; explicitly reads David's dancing as prophetic of John's leap when Mary enters Elizabeth's house. Publish only independently worded paraphrase controlled by the Syriac passage, not Dean's English or a claim of checked Greek. |
| late fourth or early fifth century | Maximus of Turin, *Sermo* 42.5, ed. A. Mutzenbecher, CCSL 23 (1962), pp. 171–72, especially p. 172, lines 105–12; older mapping Bruni 99 / PL 57, Sermo 104 | Latin; Mutzenbecher classes the sermon as most probably genuine Maximus. Older Ambrosian transmission is obsolete as authorship. | D / C | Directly asks what the Ark signifies if not holy Mary; reads David's dance, tablets/Law/voice versus heir/Gospel/Word, and gold within/outward as virginity's splendor. Strongest secure direct Latin patristic witness in this audit. |
| ca. 406–425 | Proclus of Constantinople, authentic *Homily V, On the Holy Virgin Theotokos* §3, CPG 5804, BHG 1134; Nicholas Constas, *Proclus of Constantinople and the Cult of the Virgin in Late Antiquity* (Brill, 2003), pp. 262–63, lines approximately 98–102; legacy locus PG 65:720B–C | Extant Greek; one of Constas's secure Homilies 1–5. | D / C | Mary is venerated as mother, servant, cloud, bridal chamber, and Ark of the Lord; continuation contrasts the Law with the Lawgiver carried in her womb. Translate *proskyneitai* as “is venerated/reverenced,” not “is worshipped.” It says “Ark of the Lord/Master,” not literally the later title “Ark of the Covenant.” |
| ca. 430s | Hesychius of Jerusalem, Marian *Homily V* (also “Homily I on the Holy Mary Theotokos”), §§1 and 3, CPG 6569, BHG 1132; M. Aubineau, *Les homélies festales d'Hésychius de Jérusalem*, vol. 1, Subsidia Hagiographica 59 (1978), pp. 158–68 | Authentic extant Greek; Aubineau's critical locus identified; synchronized working Greek/English and a separate French working translation were checked. | D / C / W | Applies Ps 131/132:8's Ark directly to the Virgin Theotokos; compares Mary favorably with Noah's Ark; joins Spirit, overshadowing, Son's indwelling, and incorruptible Life. Typological application does not erase the psalm's historical/liturgical sense. |
| fifth century, traditionally ca. 455–479 | *Oratio in sanctam Mariam Deiparam* §2, transmitted under Chrysippus of Jerusalem, CPG 6705, BHG 1144n; M. Jugie, “Homélies mariales byzantines II,” *Patrologia Orientalis* 19 (1926), pp. 336–43, especially p. 338, Greek lines 1–13 | Greek; Jugie's edition rests chiefly on Paris gr. 1173, fols. 16r–18v (eleventh century). Jugie defended the attribution and noted stylistic agreement with Chrysippus's secure Theodore encomium; this project did not independently establish a later critical consensus. | T / C | Directly calls the ever-virgin Theotokos the royal and exceedingly precious Ark that received the treasure of all holiness, distinguished from Noah's vessel and the stone-tablet Ark; her Creator is architect and indweller. Use as a qualified transmitted witness traditionally assigned to the fifth century, not as an unqualified authenticity anchor. The paragraph does not carry a manna-to-living-Bread claim. |
| eighth century | John of Damascus, authentic *Second Homily on the Dormition* §§2, 12–13, CPG 8062; B. Kotter, *Die Schriften des Johannes von Damaskos*, vol. 5, PTS 29 (1988); compare Allies (1898), pp. 168, 188ff., and Brian E. Daley, *On the Dormition of Mary*, pp. 215–17 | Greek; exact critical loci identified. The local 1898 Allies edition is public domain but lacks section numbers. | D / C | Section 2 calls Mary the sacred and living Ark taking up abode in the temple not made by hands; §§12–13 develop Ark procession and the true/heavenly Holy of Holies. Used as mature Dormition/Assumption reception and fittingness, not as proof of an apostolic narrative. The interpolated Euthymiac History in Homily II §18 does not carry the claim. |
| twelfth century | Peter of Celle, *Liber de panibus* ch. 21, PL 202:1018–20 | Authentic Latin work | D / C | Joins Mary's betrothal to Joseph, conception by the Spirit, temple, and Ark imagery in one chapter; calls the mother Ark of the Covenant containing the sanctification of creature and Creator. No Uzzah–Joseph equation. |
| thirteenth century | Bonaventure, *De Purificatione Beatae Virginis Mariae*, Sermo I, *collatio*; Quaracchi IX, p. 638b; retained in J.-G. Bougerol, *Sermons de diversis* II, Sermo 39 (1993), pp. 517–30 | Authentic Latin; retained by the modern critical editor | D / C | Identifies the Ark overshadowed by cherubim with the glorious Virgin, filled with divine lights and wholly intent upon divine things. The mapping makes gold signify contemplative purity; it does not explicitly make acacia signify virginity. |
| thirteenth century | Anthony of Padua, *In Assumptione Beatae Mariae Virginis*, exordium §2; *Sermones dominicales et festivi*, ed. Costa et al., vol. II (Padua, 1979), Marian sermons pp. 103–50 | Authentic Latin; authority-owned Basilica text also checked | D / C / M | Applies the arising Ark to the Virgin Mother's bodily Assumption into the heavenly bridal chamber. Pius XII receives the passage in *Munificentissimus Deus* §29. <https://www.santantonio.org/it/sermoni/sermoni-mariani/assunzione-al-cielo-della-beata-vergine-maria?latin=1> |

### Working primary links

- Epiphanius, Dean PDF:
  <https://web.english.upenn.edu/~cavitch/pdf-library/Epiphanius_Treatise_Weights_Measures.pdf>
- Epiphanius searchable working transcription:
  <https://tertullian.org/fathers/epiphanius_weights_03_text.htm>
- Hesychius synchronized Greek/English working text:
  <https://catholiclibrary.org/library/view?chunk.id=00000005&docId=%2FFathers-Synchronized-EN%2FHesychius__Homilia_i_de_sancta_Maria_deipara.en.html>
- Hesychius French working text:
  <https://www.patristique.org/Hesychius-de-Jerusalem-En-l.html>
- Vatican use of John Damascene's living-Ark language, Benedict XVI,
  Assumption homily, 15 August 2011:
  <https://www.vatican.va/content/benedict-xvi/en/homilies/2011/documents/hf_ben-xvi_hom_20110815_assunzione.html>
- Syri.ac guide to Ephrem's genuine and transmitted corpora:
  <https://syri.ac/brock/ephrem>
- Public-domain old translation of the hymn now numbered *Nativity* 16
  (printed there as Hymn XI):
  <https://catholiclibrary.org/library/view?chunk.id=00000027&docId=%2FFathers-EN%2Fnpnf.000891.EphraimTheSyrianAndAphrahatThePersianSage.EphraimSyrusNineteenHymnsontheNativityofChristintheFlesh.html>

## Syriac and virginal-marriage witnesses

The main chapter deliberately states the Joseph synthesis positively: true
marriage, mutual continence, obedient reception, naming, protection, and
household service. It does not derive Joseph's vocation from Uzzah.

| Witness | Exact locus | Status | Safe use |
| --- | --- | --- | --- |
| Origen, *Homiliae in Lucam* 13.7 | SC 87, pp. 214–15; authentic Origen transmitted in Jerome's Latin translation | T / C | Calls Joseph *dispensator ortus dominici*, steward or minister of the Lord's birth. Early positive service language; not yet a full theory of virginal marriage. |
| Ambrose, *Expositio Evangelii secundum Lucam* II.2 and II.5 | CCSL 14; authentic Latin | D / C | Joseph as husband witnesses Mary's chastity; calling Mary spouse does not remove virginity but testifies to marriage and its celebration. |
| Augustine, *De nuptiis et concupiscentia* I.11.12–13 | CSEL 42, pp. 224–25; authentic, written 419–420 | D / C | Strongest patristic locus: mutually chosen perpetual continence makes the bond firmer rather than breaking it; Mary and Joseph are truly spouses and parents in mind and purpose, though not by Joseph's begetting; offspring, fidelity, and sacramental bond are present. |
| Augustine, *Sermo* 51.10.16 and 51.13.21 | PL 38:342, 344–45; authentic | D / C | Mary is wife in chastity and Joseph husband in chastity; Joseph's marital affection and authority make his fatherhood real without begetting. |
| Bernard of Clairvaux, *In laudibus Virginis Matris / Super Missus est* II.16 | *Sancti Bernardi Opera* IV, pp. 33–34; authentic, ca. 1118–1123 | D / C | God entrusts the mystery to Joseph, who may carry, lead, embrace, kiss, nourish, and guard Christ. Strong saintly witness to tender, active custody. |
| Thomas Aquinas, *Summa theologiae* III, q.29, a.2 | Corpus Thomisticum primary Latin | D / W | The marriage of Mary and Joseph is true; mutual consent and an intended virginal form are compatible because the marriage's goods are present according to this singular vocation. Thomas is a Doctor and saintly synthesis, not a patristic witness. |
| *Collectio missarum de BMV*, Mass 1, “Holy Mary of Nazareth,” preface | Official Roman liturgy; decree Prot. N. 309/86, 15 August 1986; *editio typica* published 1987 | O / L | Presents Mary and Joseph's bond as a love that is at once marital and virginal. Concise public liturgical synthesis of true marriage and shared virginity; the publication paraphrases rather than quoting an approved translation. |
| John Paul II, *Redemptoris custos* 7–8, 17–21, especially 18–20 | Official papal synthesis with patristic notes | O / M | Upholding the marriage is necessary alongside virginal conception; Joseph and Mary make an exclusive gift of self, and conjugal love is born anew in the Spirit. Controls the positive Catholic synthesis. |
| Ephrem, *Hymns on the Nativity* 16.16–17 | Beck, CSCO 186/187 (1959); genuine Syriac Ephrem; critical locus identified without a fresh project collation of the Syriac | D / C | Earliest secure direct Ark witness in the audit and a uniquely positive Josephine source: Joseph ministers before the Lord dwelling in Mary as a priest before the Ark, followed by Moses' stone tablets and Joseph's attendance upon the pure tablet where the Creator's Son dwells. The alpha uses an independent paraphrase checked against identified translations and publishes no direct English quotation; Syriac specialist collation remains desirable but nonblocking. |

Primary Latin for Aquinas:
<https://www.corpusthomisticum.org/sth4027.html>

Official controlling synthesis:
<https://www.vatican.va/content/john-paul-ii/en/apost_exhortations/documents/hf_jp-ii_exh_15081989_redemptoris-custos.html>

### Governing Joseph–Uzzah conclusion

- No authenticated Father or saint has been located who says “Joseph is the new
  Uzzah” or who treats marital intercourse as intrinsically defiling.
- 2 Samuel 6 and 1 Chronicles 13, 15 concern the Ark's cultically disordered
  handling and the prescribed Levitical manner of carrying it.
- Matthew 1 instead gives a positive divine command: Joseph must take Mary as
  wife. His reception, naming, flight, return, labor, and household guardianship
  are the controlling evangelical grammar.
- The publication may use Uzzah only as a distant contrast: holy Presence is not
  seized or domesticated but received according to God's command. This is S,
  not a patristic quotation or the literal sense of the Uzzah narrative.

## Liturgical reception

| Witness and locus | Language/status | Direct content | Evidentiary boundary |
| --- | --- | --- | --- |
| Akathist Hymn, alphabetic stanza 23 (letter psi), twelfth and last oikos, beginning *Psallontes sou ton tokon* | Greek; ancient received liturgical text; nearly the whole manuscript tradition is anonymous, despite proposals including Romanos, Sergius, George of Pisidia, and Germanus | Greets Mary as the Ark gilded by the Spirit within a tabernacle/Holy-of-Holies cluster. | L. Proves ancient Byzantine liturgical reception, not the identity of a named author or Luke's intention by itself. Current GOARCH service, 27 March 2026, pp. 32–33: <https://digitalchantstand.goarch.org/goa/dcs/p/s/2026/03/27/co/gr-en/se.m03.d28.co.pdf>. Vatican note on manuscript anonymity: <https://www.vatican.va/news_services/liturgy/documents/ns_lit_doc_20001208_akathistos_en.html>. |
| Byzantine Menaion, Annunciation, Canon, Ode 9 heirmos | Greek; current Byzantine use; Menaion heading assigns it to “John the Monk,” traditionally identified as John Damascene; present as traditional rather than critically settled authorship | Calls Mary the living Ark of God, excludes the hand of the uninitiated, and invites believing lips to echo the angelic greeting. | L. The cultic image concerns Marian holiness. It names neither Uzzah nor Joseph and does not depict marriage as defilement. Current GOARCH Divine Liturgy, 25 March 2026, p. 23: <https://digitalchantstand.goarch.org/goa/dcs/p/s/2026/03/25/li/gr-en/se.m03.d25.li.pdf>. |
| Dormition Matins, Canon I, received/ascribed to Cosmas of Maiuma, Ode 3 | Greek Byzantine liturgy; authorship traditionally received as Cosmas and prudently described as ascribed to him | Punished hands preserve reverence for the living Ark in whom the Word became flesh. | L. The immediate referent is the Dormition story of the audacious man, conventionally Jephonias/Jechonias, not the biblical Uzzah. Uzzah is at most typological resonance; there is no Josephine application. Current GOARCH Matins, 15 August 2026, p. 17: <https://digitalchantstand.goarch.org/goa/dcs/p/s/2026/08/15/ma3/gr-en/se.m08.d15.ma3.pdf>. |
| Same Dormition Canon I, Odes 6 and 8 | Greek Byzantine liturgy | Ode 6 joins manna jar, Aaron's rod, God-written tablet, holy Ark, Holy of Holies, and Bread-of-Life table; Ode 8 addresses Mary as divine Ark of holiness and tabernacle of the living God. | L. Strong Christological and Assumption reception, not independent history of Mary's end. Same current service, pp. 24–25, 30. |
| Dormition Great Vespers, August 14, anonymous Menaion sticheron, plagal first mode | Greek Byzantine liturgy | The Ark of God goes to her place of rest. | L. Direct Psalm 132:8/Ark-rest reception applied to Mary's heavenly translation; do not assign a named Father without evidence. <https://digitalchantstand.goarch.org/goa/dcs/h/s/2026/08/14/ve2/en/index.html> |
| Akathist Hymn, alphabetic stanza 7 (letter zeta), commonly Kontakion 4 | Greek; part of the anonymous received Akathist | Calls Joseph *sophron*—temperate, self-controlled, or chaste—and shows him receiving the Spirit-conceived mystery after doubt. | L. Positive Josephine liturgical witness, but it neither states the Uzzah analogy nor by itself unfolds lifelong virginal marriage. Same 27 March 2026 service, p. 12. |
| Litany of Loreto, invocation *Foederis arca* | Latin; official current Roman text | Invokes Mary as “Ark of the Covenant.” | O. Establishes authoritative devotional title and reception; the litany is not a critical commentary on Luke. |
| Congregation for Divine Worship, *Collectio missarum de Beata Maria Virgine*, *editio typica* (LEV, 1987), Formulary 3, Visitation, introduction p. 11 and collect p. 12 | Latin; official Roman liturgical book approved by decree Prot. N. 309/86, 15 August 1986 | Calls Mary *novi foederis arca* who brings salvation and joy into Elizabeth's house; the official introduction explicitly compares the household blessing with 1 Chr 13:14. | O. Especially strong official reception of the Visitation correspondence. The copyrighted Latin is quoted only briefly. |
| Same collection, Formulary 23, “Mary, Temple of the Lord,” preface, printed p. 94 | Latin; official Roman liturgical book | Calls Mary *arca novi foederis continens novae legis Auctorem*, containing Jesus Christ, author of the new law. | O. Direct Christological control: the contained treasure is Christ. |

Official edition record:
<https://www.cultodivino.va/en/formazione/pubblicazioni/libri-liturgici/aliae/collectio-missarum-de-beata-maria-virgine.html>

The Latin pages were inspected in a complete facsimile hosted by Liturgia.it:
<https://www.liturgia.it/content/BMV/Collectio%20Missarum%20de%20Beata%20Maria%20Virgine%20%281987%29.pdf>.
The 1987 Latin is copyrighted by Libreria Editrice Vaticana; approved modern
English liturgical text is not reproduced. Liturgy witnesses the Church's
received faith; poetic figures are not silently converted into juridical
definitions or historical chronicles.

## Modern magisterial reception

| Source and locus | Status | Safe use |
| --- | --- | --- |
| Paul VI, *Marialis cultus* 6 | O | At the Annunciation Mary receives the one Mediator in her body and becomes the true Ark of the Covenant and true Temple of God. <https://www.vatican.va/content/paul-vi/en/apost_exhortations/documents/hf_p-vi_exh_19740202_marialis-cultus.html> |
| Paul VI, *Marialis cultus* 26 | O / M | The Spirit's overshadowing consecrates and makes fruitful Mary's virginity; Paul VI receives the Fathers' and ecclesial writers' Ark titles. Strong official bridge among overshadowing, virginity, and patristic reception; not an independent proof of the dogma. Same official link. |
| *Catechism of the Catholic Church* 2676 | O | Mary is Daughter Zion in person, Ark of the Covenant, and dwelling of the Lord's glory. Stable catechetical synthesis. <https://www.vatican.va/content/catechism/en/part_four/section_one/chapter_two/article_2.html> |
| John Paul II, Regina Caeli, 5 May 2002 | O | “Mary is the Ark of the Covenant” in whom heaven and earth meet because human and divine natures are united in the person of the Son. Direct modern Christological reception. <https://www.vatican.va/holy_father/john_paul_ii/angelus/2002/documents/hf_jp-ii_reg_20020505_en.html> |
| Benedict XVI, Assumption homily, 15 August 2006 | O | Luke's allusions disclose Mary as true Ark and fulfillment of Temple/dwelling imagery. <https://www.vatican.va/content/benedict-xvi/en/homilies/2006/documents/hf_ben-xvi_hom_20060815_assunzione-maria.html> |
| Benedict XVI, Homily for the Assumption, 15 August 2011 | O / M | Receives John Damascene's “living Ark” and the Ark's entry into God's rest as Assumption fittingness. Does not replace the exact object of *Munificentissimus Deus* §44. Official link above. |
| Benedict XVI, Angelus, 23 December 2012 | O | John's leap calls David's dance to mind; Mary is the Ark of the New Covenant bearing Jesus. <https://www.vatican.va/content/benedict-xvi/en/angelus/2012/documents/hf_ben-xvi_ang_20121223.html> |
| Pius XII, *Munificentissimus Deus* §§21, 26–27, 30 | O / M | Controls the distinction between patristic/liturgical fittingness and the exact defined object; Psalm 132 and Ark imagery occur within a cumulative tradition, not as a hidden canonical Dormition narrative. <https://www.vatican.va/content/pius-xii/en/apost_constitutions/documents/hf_p-xii_apc_19501101_munificentissimus-deus.html> |

## Attribution and quotation audit

| Common citation | Actual evidence state | Disposition |
| --- | --- | --- |
| Hippolytus, *Commentary on Daniel* 4.24.3, as an early Mary-as-Ark text | The grammatically controlling Ark is Christ's own body offered into the world, not Mary. | X for Mary-as-Ark. Do not use to move the typology into the early third century. |
| “Gregory Thaumaturgus, Homily I on the Annunciation,” CPG 1775; PG 10:1151–54 | Rich direct Ark language, including gold within and without, but transmitted among dubious/spurious works. | R. Cite as Pseudo-Gregory, date uncertain; valuable reception, not third-century Gregory. |
| Pseudo-Chrysostom, *Contra haereticos et in Sanctam Deiparam*, PG 59:710 | Direct Marian Ark wording in a work not accepted as Chrysostom's. | R. May document reception only under pseudonymous attribution. |
| Proclus, *Homily VI*, CPG 5805; PG 65:721–57 | Rich gilded-Ark/tabernacle language; modern bibliography marks the work pseudo-Proclus or attribution uncertain. | R. Use authentic Homily V §3 for the secure Proclean spine. |
| Turin “Athanasius” Marian homily, CPG 2187 | Coptic/disputed Marian homily; Athanasian attribution rejected or doubtful. | R/X. Do not claim a secure fourth-century Greek Athanasius witness. |
| “Ambrose, Sermon 42,” *Ante arcam ergo saltavit* | The David/John and Mary-Ark passage was printed in the Ambrosian transmission, but Mutzenbecher places it as most probably genuine Maximus of Turin, *Sermo* 42.5, CCSL 23, pp. 171–72. | X under Ambrose; D/C under qualified Maximus. Ambrosian literary influence is not Ambrosian authorship. |
| Bonaventure, *De Nativitate BMV*, Sermo V, q. IX, Quaracchi IX, pp. 715a–19a | Rich thirteenth-century Ark synthesis—construction, contents, efficacy, honor, incorruptible material/virginity, gold, manna, rod, tablets, David, and Uzzah—but Bougerol did not retain it among Bonaventure's secure sermons; parts of the transmission are anonymous. | R. Cite as a thirteenth-century Marian sermon printed in the older Quaracchi Bonaventure corpus, not simply as St.~Bonaventure. Its Uzzah application concerns irreverent thought about Mary, not Joseph. |
| Pseudo-Modestus, Dormition homily, CPG 7876 | Later work, probably after 680/681, not secure Modestus of Jerusalem. | R. It can witness mature Dormition reception under the pseudonymous name, not Modestus's date. |
| Pseudo-Ildefonsus, *Libellus de Corona Virginis* | Printed among supposititious works; direct medieval Ark imagery. | R. Preserve only as anonymous/pseudonymous Latin reception. |
| Ark sermons printed under Bernard, including material attached to the *Salve Regina* | Attribution is not secure Bernard of Clairvaux without critical corpus confirmation. | R. Do not use as Bernard's personal teaching. |
| John Damascene, *Second Dormition Homily* §18, Euthymiac History | Widely treated as interpolation. | X for the main spine. Authentic §§2, 12–13 and the other Dormition passages suffice. |

The classification `R` is not a theological condemnation. A pseudonymous text
may remain orthodox, beautiful, influential, and liturgically fruitful. The
qualification answers the narrower historical questions “who wrote it?” and
“how early is this exact witness?”

## Dogmatic and theological control

| Marian doctrine | What the Ark witnesses illuminate | What they do not independently establish |
| --- | --- | --- |
| Divine motherhood | Strongest and most direct relation: Mary bears not tablets but the Lawgiver, not created manna but the incarnate Bread, not a sign only but the divine person according to his humanity. | They do not imply that Mary originates the divine nature or becomes divine. |
| Perpetual virginity | Holy vessel, gold within and without, “incorruptible wood,” sealed sanctuary, and undivided consecration form a longstanding fittingness-language. Joseph and Mary's true marriage gives the vocation a personal covenantal form. | They do not make marriage or conjugal union unclean, nor does every material detail equal an anatomical proposition. |
| Immaculate Conception | Holiness, purity, precious material, divine preparation, and total belonging to Christ accord with preservative grace. | No checked ancient Ark witness articulates the complete 1854 object: preservation from original sin from the first instant in view of Christ's merits. |
| Assumption | Psalm 132:8, the living Ark entering the heavenly Holy of Holies, and Dormition worship form a mature and powerful fittingness. | They are not a canonical eyewitness narrative, do not settle Mary's death, and do not replace *Munificentissimus Deus* §44. |

The safest synthesis is: **the four dogmas disclose the full Christological and
ecclesial resonance that Catholic Tradition finds in the New-Ark image**. The
publication should not say that the Ark by itself proves or mechanically
predicts all four definitions.

## Translation, rights, and quotation controls

- Dean's 1935 Epiphanius translation is a rights-unresolved working witness;
  the publication uses independently worded paraphrase controlled by the
  Syriac passage. Allies's 1898 Damascene translation is a public-domain
  working witness. Edition and transmission limits remain visible.
- Constas, Aubineau, Beck, Kotter, Daley, and modern critical translations are
  used to identify loci and control bounded paraphrase according to the audit's
  stated inspection level. No substantial copyrighted translation is
  reproduced, and no direct project collation of Beck's Syriac is claimed.
- McVey's and Brock's modern English Ephrem translations are protected and are
  used only to check the sense; the publication employs an independent
  paraphrase anchored to Beck's identified critical locus. The old
  public-domain rendering is a secondary comparison and its “Hymn XI” is mapped
  to Beck's *Nativity* 16.
- Original-language phrases are kept short and tied to an exact work/locus.
  English prose in the chapter is either a short conventional rendering or a
  bounded paraphrase, not represented as a newly established critical text.
- Online patristic libraries and scans are locating/working witnesses. A
  searchable transcription is not called an autograph or critical edition.
- Official Holy See English pages may control modern magisterial wording.
  Official liturgical Latin should control short Roman titles and phrases.
- No detached quotation graphic, unattributed devotional website, or secondary
  article carries a consequential authenticity claim.

## Remaining specialist checks

1. A future Syriac specialist collation of the independent Ephrem paraphrase
   against Beck's text remains desirable. It is nonblocking for alpha because
   the work, locus, authenticity, and substance are secure and the publication
   prints no direct English quotation from the Syriac or Beck.
2. Seek external specialist review in Greek and Syriac patristics, hymnography,
   and Latin medieval sermon attribution before final publication.

These checks limit quotation precision, not the secure central conclusion. The
authenticated Ephrem–Epiphanius–Maximus–Proclus–Hesychius–Damascene spine,
together with the qualified Chrysippus transmission, establishes ancient and
mature Catholic reception of Mary as the living Ark.
