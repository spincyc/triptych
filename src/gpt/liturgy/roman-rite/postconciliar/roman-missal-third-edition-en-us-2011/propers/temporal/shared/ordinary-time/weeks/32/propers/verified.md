# Ordinary Time Week 32: canonical Missal source owner

Context and bounded research inspection, 2026-11-05. This non-publishable owner holds the common
Missal evidence for parent `PC-S58`. Cycle-specific readings and dated
occurrences belong to their consuming leaves. This record establishes the
inventory at the witness layers stated below; the research collation below is bounded to named witnesses and is not publication acceptance.

## Edition and inspected sources

The governing target is the *Roman Missal, Third Edition, for Use in the
Dioceses of the United States of America* (English, 2011), with the Latin third
typical edition's emended 2008 reprint as its base. The accessible Latin
reproduction identifies itself with 2002; it is not an authenticated 2008
altar-book facsimile. Its physical PDF pages are not asserted to be the
printed book's pagination.

The three complete artifacts below were reacquired on 2026-11-05. Their
hashes and sizes matched the registered records. The named pages were read
in extracted text and rendered page images; no whole-book collation is claimed.

| Witness | Inspected locus | Registered artifact / exact hash |
| --- | --- | --- |
| Latin third typical edition, secondary digital reproduction | Physical PDF pp. 294–295, from the Week XXXII heading through its Prayer after Communion, ending before XXXIII; Ordinary Time rubrics 2–6 on physical p. 268 | `artifact.catholic-church.missale-romanum.vatican-typica-tertia-2002.secondary-digital-pdf-0b458944`; SHA-256 `0b458944824d2ee92854b9664f83e553af0342e0b15a9dc14b00e846405523d7`; 3,333,382 bytes; [complete source](https://media.musicasacra.com/books/latin_missal2002.pdf) |
| ICEL Antiphonary, official CBCEW-hosted excerpt | Printed p. 82 / physical PDF p. 90, Thirty-second Sunday block only | `artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary.antiphonary-pdf`; SHA-256 `e6b82741acc77fb5e0d7c887813f6f2652b4ec088abc8526f5c77320e9762aca`; 1,120,199 bytes; [complete source](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf) |
| FDLC, *Mystagogical Reflections*, 2016, Ordinary Time 31–Christ the King | Printed and physical pp. 8–9, Collect and Prayer after Communion | `artifact.federation-of-diocesan-liturgical-commissions.mystagogical-reflections.2016-collect-and-prayer-after-communion.combo-col-pac-78e-ordinary-31-christ-the-king`; SHA-256 `70fb1ff333ef512ea97469776f70255d5d95facead78ffe45afbc05f5db6727a`; 251,559 bytes; [complete source](https://fdlc.org/wp-content/uploads/2026/05/ComboColPaC78e_ORDINARY_31-CTK_SPI2016.pdf) |

The Antiphonary witnesses the ICEL antiphons, not the U.S. altar-book's
orations. The FDLC pages identify their excerpts as ICEL and report approval
by the U.S. Committee on Divine Worship. Their surrounding reflections and
newly composed prayers are not appointed texts and are excluded from this
inventory.

## Common inventory and boundaries

| Owner unit | Identifier and biblical locus | Finding |
| --- | --- | --- |
| `entrance` | *Intret oratio mea*; cf. Psalm 87:3 Vulgate / 88:3 Hebrew | Both inspected witnesses mark an adaptation. |
| `collect` | *Omnipotens et misericors Deus* | Latin on physical p. 294; approved-English excerpt in FDLC p. 8. The petition concerns freedom from adversity and service to God. |
| `offerings` | *Sacrificiis praesentibus* | Latin on physical p. 294. The prayer concerns the sacramental celebration of the Son's Passion and its inward reception. A U.S. 2011 digital-book candidate was inspected at printed p. 492; its third-party transmission is qualified below. |
| `communion-psalm` | *Dominus regit me*; cf. Psalm 22:1–2 Vulgate / 23:1–2 Hebrew | First of two appointed alternatives; both witnesses mark an adaptation. |
| `communion-luke` | *Cognoverunt discipuli*; Luke 24:35 | Second alternative, introduced by `Vel` / `Or`. The Latin source cites Luke without `Cf.`; the English Antiphonary explicitly prints `Cf.`. Its wording is a liturgical adaptation of the verse, not a whole-verse Bible quotation. |
| `after-communion` | *Gratias tibi, Domine, referimus* | Begins at the bottom of Latin physical p. 294 and concludes at the top of 295; approved-English excerpt in FDLC p. 9. Thanksgiving and the Spirit's preservation of integrity follow Communion. |

The Week XXXII block supplies no Sequence, Offertory antiphon, uniquely
appointed Preface, special Eucharistic Prayer insert, or distinctive concluding
formula. Ordinary Time rubric 4 requires Gloria and Creed on Sundays. Rubric 5
directs the Sunday Prefaces unless the selected Eucharistic Prayer has its own
Preface. Rubric 6 permits either Communion antiphon and prefers one agreeing
with the Gospel where appropriate. Neither option is assigned exclusively to
one Sunday cycle. The Antiphonary's parenthesized psalm/Graduale references
are not evidence that a local assembly selected those chants.

## Rights, source route and remaining collation

The registered rights dispositions remain controlling. No complete protected
liturgical body, source PDF or raster is retained in this owner. Commentary
will use minimal identifiers and source locators; biblical passages may use
an identified public-domain study translation, visibly distinguished from
the approved Lectionary and from the Missal's adaptations. No newly composed
translation or close paraphrase will replace an omitted prayer.

The existing `postconciliar-proper-translations-v1.toml` records a
project-created Collect rendering from an ancient-source lead, a
no-exemplar gap for the approved English Prayer over the Offerings, and a
surface-specific rights exclusion for the FDLC Prayer after Communion.
Those distinct states are not interchangeable. Its Collect lead does not
authorize a new translation or establish exact target-edition fidelity;
independent historical-source work, if useful, remains research rather than
the target's approved English.

The completed research supplement below checks the official 2008
*Variationes* and an identified U.S. digital altar-book candidate. It records
the offerings comparison and the remaining authentication limits. The FDLC Collect has the older conclusion containing “one God”;
the current U.S. GIRM 54, inspected online on 2026-11-05, omits “one.” The old
excerpt is therefore not a current complete recitation text. No replacement
conclusion has been assembled here.

The leaf's three output targets explicitly depend on this owner in the
Makefile. The leaf references this evidence rather than duplicating it.

## Completed research supplement, 2026-11-05

The research worker independently checked all the page images listed above,
after recomputing the source hashes. The Latin and ICEL witnesses agree in
inventory and the three scriptural identifications. Latin `Lc 24,35` is an
identified basis; the English witness explicitly marks an adaptation. The
orations receive analytical discussion, not replacement translations.

The official *Notitiae* 44 (2008), nos. 503–504, **Variationes**, printed
pp. 367–373 (especially the complete *Tempus per annum* subsection at p. 371),
was checked in the exact official PDF
`artifact.holy-see.notitiae.volume-44-numbers-503-504-2008.official-pdf-74c8d174`:
SHA-256 `74c8d1740284984d0f4d64b2223edf805dadfa55aec8a92f8cfba9ab901eca0f`,
1,280,566 bytes, retrieved 2026-11-05. The subsection lists amendments at
Missal pp. 457 and 471; it does not identify a Week XXXII amendment. This is a
bounded negative in that published list, not a collation of the complete
2008 altar book. The registered acquisition audit's ISBN 9788820981204
search was read as prior evidence; a fresh web search for the title, ISBN and
PDF found a commercial catalogue and secondary copies, not an authenticated
2008 complete book. The exact 2008 altar-book limitation remains.
[Official issue](https://www.cultodivino.va/content/dam/cultodivino/rivista-notitiae/2000/notitiae-44-%282008%29/Notitiae-503-504-2008.pdf).

The acquisition audit also led to a complete, 1,518-page U.S. 2011 digital-book
candidate, acquired from the Internet Archive on 2026-11-05. Its title page
(physical p. 1), approval and rights page (p. 2), and Week XXXII (physical
p. 490, **printed p. 492**) were inspected as rendered images. The approval
and publication decrees (physical pp. 6–7) were read in extracted text.
The title specifies the United States, 2011; the approval page names Aymond
and Hilgartner. The Week XXXII page contains all six common owner units and
agrees with the ICEL and FDLC excerpts above. It supplies an inspected
English offerings witness, but is a third-party uploaded digital reproduction,
with no publisher transmission independently authenticated here. Do not
upgrade it to an authenticated publisher facsimile or clear the inventory's
public-text hold. Its old Collect conclusion agrees with the 2016 FDLC
excerpt and is not the current complete recitation text.
[Complete candidate](https://archive.org/download/Roman-Missal-Third-Edition/Roman%20Missal.pdf),
SHA-256 `1cf11339cb0c3a25d78dd8d1fd94c88a50e7175d7122cd562cfb02863df9cb7b`,
56,408,992 bytes. Registration must retain identity and hash without the PDF,
text extraction or page images. No protected body is reproduced here.

A second complete digital witness, the Ignatius Pew Missal planning page
headed *Thirty-Second Sunday in Ordinary Time (Year A)*, was acquired and read
through its copyright footer. SHA-256
`c855f2b3f2b4ff95e543bf6265c5cba8f468f0d9fda37e22ab6482c8a76194fd`,
49,145 bytes, retrieved 2026-11-05. It lacks the Luke Communion option and
prints the older Collect ending. The controlling translations inventory
already rejects this site's offerings text as an authoritative exemplar.
That rejection is preserved; this is a checked, excluded corroborating
candidate, not the source of publishable appointed wording.
[Planning page](https://www.pewmissal.com/brand_new/index.php/planning-guide/ordinary-time-2/thirty-second-sunday-in-ordinary-time-year-a/).

Current U.S. GIRM 54 was checked at the official USCCB site, together with its
parent page's dated confirmation and rights statement. It records the
February 3, 2021 emendation, and its conclusion omits the old extra word.
The full GIRM response receipts are in the consuming leaf's acquisition
handoff. The 2021 change is currentness control, not permission to assemble
a replacement recitation text in this study.

The source audit therefore supports the complete inventory and original
analytical commentary in `rights-limited` mode. It does not support printing
full modern Latin or approved English prayer/antiphon bodies. The antique
Collect lead in the translations inventory has not been independently
collated here and is not used to clear or reproduce a full prayer. No earlier
calendar's Mass or later prayer variant is imported. The Prayer after
Communion's recorded historical relation is revised; an earlier English
version cannot silently stand for this target.
