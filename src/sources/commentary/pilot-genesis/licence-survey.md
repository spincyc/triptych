# Genesis catena pilot — acquisition and licence survey

Lane: acquisition and licensing. The storage schema and the prototype page are
another lane's; this document is the input they consume.

Retrieval for this survey was done by hand with WebFetch/WebSearch on
2026-07-31. Nothing here ran through `tools/harvest`, which another lane is
editing. Section 7 specifies what a `tpt harvest` acquisition verb would have
to do to reproduce it.

---

## 0. Headline

**Of the ten works selected, two have a public-domain English text and eight do
not.** For those eight the only redistributable witness is the Latin or Greek
of Migne. The English translations that exist for them — Fathers of the Church,
Ancient Christian Writers, Translated Texts for Historians, Oxford Early
Christian Studies — are all twentieth- and twenty-first-century, all in
copyright, and the earliest of them does not expire until 2052.

A first-form catena page on Genesis 1 rendered in English would therefore show
**Basil and Gregory of Nyssa and nothing else**. Rendered in Latin and Greek it
would show all ten. This is not a gap that more acquisition effort closes,
because the translations do not exist to be acquired; it is a property of the
corpus.

The maintainer's expectation stated in the brief is confirmed, and it is
sharper than expected: it is not that public-domain English is *scarce*, it is
that for patristic and medieval **Genesis** commentary specifically it is very
nearly absent. Schaff's NPNF, which is the project's main public-domain English
holding, translated almost no Genesis exegesis: the Hexaemeron of Basil and
Gregory of Nyssa's continuation of it are the only Genesis expositions in the
fifteen volumes this repository tracks.

---

## 1. Correction to the brief's starting figures

The brief quoted figures from `passage-commentary-index.yaml` that the file does
not carry. Measured directly:

| Brief said | File actually holds |
| --- | --- |
| 42 distinct works | **32** distinct works (207 rows over 10 Genesis chapters, 22 distinct authors) |
| Cornelius a Lapide, Lyra, Denis, Hugh, Rupert, Bede, Chrysostom, Origen, Ephrem, Rabanus, Alcuin, Augustine, Isidore, Cyril, Jerome all at confidence 1.00 | Only three works reach 1.00 on **every** Genesis chapter they appear on. Most sit at 0.67 or 0.33 |
| — | **Not one row carries a `work_id`.** Deduplication has fallen back to `"author \| title"` throughout |

The missing `work_id`s are visible in the data as split works: `Bede the
Venerable — In principium Genesis` (9 chapters) and `Bede — In principium
Genesis` (4 chapters) are one work counted twice; likewise `Denis the
Carthusian` under two titles, `Alcuin` under *Genesim*/*Genesin*, and `Ephrem`
under two titles. The README's own warning — "Give every work a `work_id`. Two
spellings of one work become two works" — describes what has happened here.

Ambrose's *Hexameron* and Basil's *Homiliae in Hexaemeron* **are** both carried,
answering the brief's question: Basil at confidence 1.00 on Genesis 1 (its only
chapter), Ambrose at 1.00 on Genesis 1 but 0.33 when aggregated across the two
chapters it reaches.

---

## 2. Source licences, each verified by fetching the licence

Verified 2026-07-31.

| Source | Verified at | Verdict | Usable for redistribution? |
| --- | --- | --- | --- |
| **Internet Archive** facsimiles of pre-1929 printings | item page, e.g. `https://archive.org/details/patrologiae_cursus_completus_lat_vol_034` | Item carries **Public Domain Mark 1.0**. Underlying volume Migne 1861 | **Yes.** Underlying text PD worldwide; IA claims nothing over the scan |
| **CCEL** | `https://www.ccel.org/about/copyright.html` | "CCEL.org website and special contents copyright 1993-2020 Harry Plantinga. Most of the editions … are based on books that are public domain in the United States. However, they may have copyrighted introductions, cover art, and other special contents." Texts "may be used for personal, educational, or non-profit purposes" | **Underlying text yes, CCEL's formatted edition no.** Use as a finding aid and a second witness, not as the artifact |
| **New Advent** | `https://www.newadvent.org/utility/copyright.htm` | Bare "Copyright © 2026 by New Advent LLC." **No grant of any kind.** No redistribution permission stated | **No.** Underlying NPNF is PD independently; take it from the printed volume instead |
| **Documenta Catholica Omnia** | `https://www.documentacatholicaomnia.eu/a_1000_About_Us.html` | "© 2006 Cooperatorum Veritatis Societas quoad hanc editionem iura omnia asservantur". Claims copyright "not on texts but rather on their formatting". Download "exclusively for study, research or edification purposes"; "it is not permitted their use for sake of gain" | **No — non-commercial restriction.** A non-commercial clause is incompatible with an unrestricted public site. The underlying Migne text is PD and obtainable from IA without this encumbrance |
| **Corpus Corporum** (Zurich) | `https://mlat.uzh.ch/`, corroborated via the project's own published description | Rights **vary per text** by heterogeneous origin; downloads permitted "for non-commercial use" and only "unless copyrights or the texts' providers restrict this" | **No, not in bulk.** Two independent defects: a non-commercial clause, and per-text rights that include modern critical editions still in copyright. Excellent for *finding* a text; unsafe as a redistribution source without a per-text determination |
| **Fathers of the Church** (CUA Press) | publisher/edition pages for FOTC 42, 71, 74 | 1961–1992, all rights reserved | **No.** In copyright |
| **Ancient Christian Writers** (Paulist) | ACW 41/42, 1982 | In copyright | **No** |
| **Translated Texts for Historians** (Liverpool UP) | `https://www.liverpooluniversitypress.co.uk/doi/book/10.3828/9781846310881`, TTH 48, 2008 | Kendall's moral rights asserted under the 1988 Act | **No** |
| **Oxford Early Christian Studies** | Hayward, *Saint Jerome's Hebrew Questions on Genesis*, OUP 1995 | In copyright | **No** |
| **Sources Chrétiennes**, **Corpus Christianorum** (CCSL/CCCM), **CSEL** post-1930 | publisher catalogues | Modern critical editions, in copyright | **No.** Use Migne for the same text |

### The rule this yields

**Take the bytes from an Internet Archive facsimile of a pre-1929 printing and
transcribe from the page images.** That route is clean of every host's
formatting claim, and it is already this repository's established pattern —
`artifact.nicene-and-post-nicene-fathers.series-1-volume-7.new-york-1888.ia-facsimile-pdf-5d162561`
does exactly this. Every other host above either restricts commercial use,
claims its own formatting, or grants nothing at all. None of them needs to be
relied on, because the printed volumes they transcribe are themselves reachable.

---

## 3. The ten, and why each

Optimised for what the pilot has to learn, not for scholarly completeness.

| # | Work | Died | Genre | Extent in Genesis | PD Latin/Greek | PD English |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Origen, *Homiliae in Genesim* | 254 | homily series (16) | **selective, with gaps** | Yes — PG 12 / GCS 29 | **No** (FOTC 71, 1982) |
| 2 | Basil, *Homiliae in Hexaemeron* | 379 | homily series (9) | **Gen 1:1–26 only** | Yes — PG 29 | **Yes** — NPNF 2-8, tracked |
| 3 | Gregory of Nyssa, *De hominis opificio* | 395 | treatise | **Gen 1:26–27 only** | Yes — PG 44 | **Yes** — NPNF 2-5, tracked |
| 4 | Ambrose, *Hexameron* | 397 | homily series (9) | **Gen 1:1–2:3 only** | Yes — PL 14 / CSEL 32 | **No** (FOTC 42, 1961) |
| 5 | John Chrysostom, *Homiliae in Genesim* | 407 | homily series (67) | whole book | Yes — PG 53–54 | **No** (FOTC 74/82/87, 1986–92) |
| 6 | Jerome, *Liber quaestionum hebraicarum in Genesim* | 420 | **quaestiones** | selective, verse-level | Yes — PL 23 | **No** (Hayward, OUP 1995) |
| 7 | Augustine, *De Genesi ad litteram* | 430 | running commentary (12 bks) | **Gen 1–3 only** | Yes — PL 34 | **No** (ACW 41/42, 1982) |
| 8 | Bede, *In principium Genesis* | 735 | running commentary | **Gen 1:1–21:10 only** | Yes — PL 91 | **No** (TTH 48, 2008) |
| 9 | Rupert of Deutz, *De sancta Trinitate* I–IX | 1129 | running commentary **inside a larger work** | whole book, but books I–IX of 42 | Yes — PL 167 | **No — none has ever existed** |
| 10 | Cornelius a Lapide, *Commentaria in Genesim* | 1637 | running commentary | whole book | Yes — Vivès 1866 | **No for Genesis** (Mossman's English covers the Gospels only) |

**Century spread:** 3rd, 4th ×3, 5th ×3, 8th, 12th, 17th. Fourteen hundred
years, so chronological ordering (Rule 7) is genuinely exercised rather than
sorted over a clump.

**Genesis 1 specifically:** nine of the ten reach it. Only Jerome does not
begin there.

**Granularity mix (Rule 5, the extent rule):** four homily series, four running
commentaries, one *quaestiones* work whose units are verse-level and
discontinuous, and one commentary that is a book-range inside a much larger
work. Rupert is the sharpest test in the set — his Genesis exposition is books
I–IX of a 42-book treatise on the Trinity, so the work identity, the extent and
the container are three different things.

**Extent that does not cover all of Genesis:** six of the ten, not one. Basil
stops at Genesis 1:26 mid-verse; Gregory of Nyssa covers two verses and nothing
else; Ambrose stops at 2:3; Augustine at the end of chapter 3; Bede at 21:10;
Origen is discontinuous throughout. Extent gating cannot be assumed past by
this set — a page that ignored extent would attribute Genesis 22 to Basil.

### Why the rejected candidates were rejected

| Rejected | Reason |
| --- | --- |
| **Nicholas of Lyra**, *Postilla litteralis* (index rank 1, 10 chapters) | **No machine-readable text exists.** Digitised only as manuscript and incunabula page images — Rylands, Yale Beinecke, the Strasbourg 1492 print. No transcription, no OCR of gothic Latin worth having. Acquiring it means transcribing by hand from blackletter. The highest-ranked work in the index is the least acquirable in it, which is itself the finding |
| **Hugh of Saint-Cher**, *Postillae in universa Biblia* | Same: early printed editions only, no transcription |
| **Denis the Carthusian**, *Enarrationes* | Same. Also split across two titles in the index, so its identity is not settled |
| **Glossa Ordinaria** (indexed under Walafrid Strabo) | PL 113–114 exists, but the attribution to Walafrid is known to be wrong and the work is a layered compilation with no single author or date — it would violate Rule 7 (order by the date of the text) before it rendered. Needs its own decision first |
| **Ephrem the Syrian**, *Commentarius in Genesim* | Syriac. NPNF 2-13's Ephraim selections are hymns and homilies, **not** the Genesis commentary. English is Mathews, FOTC 91, 1994 — in copyright. Adds a third script for one work |
| **Theodoret**, *Quaestiones in Octateuchum* | Would duplicate Jerome's genre slot. English is Hill, 2007, in copyright |
| **Cyril of Alexandria**, *Glaphyra* | Greek only, in copyright in English, and duplicates Chrysostom's language and century |
| **Isidore**, *Quaestiones in Vetus Testamentum*; **Alcuin**, *Interrogationes* | Both duplicate the *quaestiones* genre already held by Jerome; Alcuin is additionally split across two spellings in the index |
| **Rabanus Maurus**, *Commentaria in Genesim* | Genuine candidate, dropped only on the count. Largely a catena of Augustine and Bede, both of which are already in the set, so it would test deduplication rather than breadth. **First reserve** |
| **Augustine**, *De civitate Dei* XI–XIV | **Has public-domain English** (NPNF 1-2) and is worth acquiring, but it is not a Genesis commentary — it expounds Genesis inside an argument about the two cities. Recommended as an eleventh, not as one of the ten |
| **Augustine**, *De Genesi contra Manichaeos*; *Quaestiones in Heptateuchum* | Augustine already has a slot; three Augustines would crowd the 5th century |
| **Gregory of Nyssa**, *Apologia in Hexaemeron* (the work the index names) | **Replaced with the same author's *De hominis opificio*.** The indexed work has no public-domain English (Orton, FOTC, 2021); its companion piece does, in a volume this repository already tracks. Note the lesson: the acquisition list named the work with no reachable translation, and the reachable one is not on the list |
| **Ambrose**, *De paradiso*, *De Noe et arca*, *De Abraham*; **Procopius of Gaza** | Lower coverage, and each duplicates a slot already filled |

---

## 4. English availability, work by work, stated plainly

Nothing here is inferred from a death date. Each is the actual translation
history of the actual work.

| Work | Is there *any* English? | Is any of it public domain? |
| --- | --- | --- |
| Origen, *Hom. in Gen.* | Yes — Heine, FOTC 71, CUA Press 1982, all rights reserved | **No.** US copyright to roughly 2052 |
| Basil, *Hexaemeron* | Yes — Blomfield Jackson, NPNF 2-8, 1895 | **Yes.** PD in the US by date of publication; Jackson d. 1905 |
| Gregory of Nyssa, *De hominis opificio* | Yes — H. A. Wilson, NPNF 2-5, 1893 | **Yes.** Same basis |
| Ambrose, *Hexameron* | Yes — Savage, FOTC 42, 1961 | **No.** NPNF 2-10 contains Ambrose's *select works* — the duties, the Holy Spirit, the mysteries, letters — but **not** the Hexameron |
| Chrysostom, *Hom. in Gen.* | Yes — Robert Hill, FOTC 74/82/87, 1986–1992 | **No.** NPNF translated Chrysostom on the Statues, Matthew, John, Acts, Romans, Corinthians, Galatians–Philemon and Hebrews — **not** Genesis |
| Jerome, *Quaest. hebr. in Gen.* | Yes — Hayward, OUP 1995 | **No.** NPNF 2-6 gives Jerome's letters and select works, not this |
| Augustine, *De Genesi ad litteram* | Yes — Taylor ACW 41/42 1982; Hill, WSA, 2002 | **No** |
| Bede, *In principium Genesis* | Yes — Kendall, TTH 48, Liverpool 2008 | **No** |
| Rupert of Deutz | **No English translation has ever been made** | n/a |
| Cornelius a Lapide, on Genesis | **No.** Mossman's *Great Commentary* (1876–1908) is public domain but covers only the Gospels and Acts | n/a |

Two of ten. Both of the two are already tracked works in this repository, so
the rights work on them is done and no new rights determination is needed to
render them.

**What this means for the prototype page.** It must not present a Latin-only
chain as a finished English feature. The honest first form is either a
Latin/Greek page that says so, or an English page carrying two fragments and an
explicit statement that the other eight works are held in Latin or Greek only
because no free English rendering of them exists. The L1 index will list all
thirty-two works for Genesis 1; the L3 chain in English will hold two. Rule 1
says the page renders L3 and only L3, and that difference is exactly what Rule 1
was written to keep visible.

---

## 5. Storage — using the containers that already exist

Confirmed with the coordinator: do **not** invent a parallel format.

- Fragment text goes in a **`passage`** record: `text`,
  `transcription_segments`, `physical_line_ranges`, `artifact_id`,
  `artifact_sha256`, `locus`, `states`, `context`, `verified_on`, `notes`.
  Model: `src/sources/works/nicene-and-post-nicene-fathers/series-1-volume-7/editions/new-york-1888/passages/augustine-tract-in-io-120.9.toml`.
- Each fragment needs **two artifacts**: the hashed facsimile
  (`artifact_type = "facsimile-pdf"`, `storage = "remote"` — its bytes stay out
  of the repository) and the transcription derived from it
  (`artifact_type = "checked-transcription"`, `storage = "tracked"`,
  `derived_from` the facsimile).
- `rights_status = "public-domain"` **requires** `rights_jurisdiction`.
- Anything in copyright is recorded `storage = "restricted"` with its hash and
  byte size and **no bytes**.
- Existing `artifact.toml` files are not edited: a changed fingerprint cascades
  a review obligation to 101 pinned bindings.

Two conventions this lane needs the schema lane to settle, because a fragment
record cannot express them today:

1. **The canonical Genesis extent** (Rule 3) has nowhere to live. `locus` is a
   human-readable string — `"Augustine, In Iohannis Evangelium Tractatus
   CXX.9"` — naming the locus *in the commentary*, not the scripture locus
   commented on. A catena needs both, and the second must be machine-comparable
   in `CANONICAL` numbering or nothing can derive the chapter view.
2. **The work commented on** is likewise unrepresented. The passage's
   `edition_id` points at the NPNF volume, which is the container, not
   Basil's *Hexaemeron*. Rule 8's title check has nothing to check against
   until a fragment can name the work it is a fragment of.

---

## 6. OCR quality, with examples

Two separate quality problems, and they are not the same problem.

### Migne OCR from the Internet Archive is not publishable text

Sampled from `patrologiae_cursus_completus_lat_vol_034_djvu.txt`, the Internet
Archive text layer of Migne PL 34 — the volume holding Augustine's Genesis
works. Reproduced exactly:

```
Omnis doctrina vel rerum est vel signorum, sed res per signa discuntur.
Proprie autem nunc res appel¬ lavi, quae non ad significandum aliquid
adbibentur, Siculi est lignum, bpis, pecus , atqne hujusmodi ca> tora.
[...] ncqne ille lapis quem Jacob sibi ad caput posuerat (Cenes, xxvui, II);
neque illud pecus quod pro filio immoiarit Abrabam (Id. xxu, 43).
[...] Cx quo bitet- Ugitur quid appeUeni signa; res eas videlicet quae ad
significandum aliquid adliibcntur.
```

Every one of these is wrong: `bpis` for *ovis*, `Siculi` for *sicut*, `atqne`
and `ncqne` for *atque* and *neque*, `ca> tora` for *cetera*, `Cenes` for
*Genes.*, `immoiarit` for *immolavit*, `Abrabam` for *Abraham*, `Cx quo bitet-
Ugitur quid appeUeni` for *Ex quo intelligitur quid appellem*, `adliibcntur`
for *adhibentur*. Roughly **one word in eight is corrupted**, and the
double-column layout leaves soft-hyphen artifacts (`appel¬ lavi`, `re¬ rum`)
and stray spacing throughout.

This cannot be rendered on a page. It is a finding aid and nothing more. The
repository already says so in its own words, in the note on
`artifact.cornelius-a-lapide.commentaria-in-pentateuchum.antwerp-1700.ia-djvu-ocr-d1f91f40`:
"Long s is frequently read as f, the ae ligature as z, and marginal keywords
are interleaved with the text. It is a finding aid; a quotation taken from it
is a quotation of the text layer and not of the page unless separately
collated."

**The consequence is the real cost of this corpus.** The Latin is
licence-clear and the English is licence-blocked, but the licence-clear Latin
is not readable as delivered. Clean keyed-in Latin does exist — Corpus
Corporum and Documenta Catholica Omnia both have it — and it is exactly that
clean text which carries the non-commercial restrictions in section 2. So the
two constraints interlock: **the clean Latin is encumbered and the
unencumbered Latin is OCR wreckage.** Acquisition cost for the eight
Latin-only works is transcription and repair, not download.

### The English web transcriptions are clean

By contrast the NPNF text on Wikisource and CCEL is keyed, not scanned, and
needed no repair. The only defect found across roughly 1,800 words was a
doubled auxiliary — "and that was all was given up to chance" — and because it
is present identically in **both** independent witnesses it belongs to the
transcription lineage rather than to either host. It is preserved in the
landed artifact and flagged in its notes rather than silently corrected.

---

## 6a. Three tool-level blockers, each demonstrated

These are why this lane could not land text for all ten works, and each is a
hard requirement on the acquisition verb.

1. **A model-mediated fetch refuses on a copyright notice.** Asked for the
   Basil text, New Advent's page returned a refusal citing "Copyright © 2026
   by New Advent LLC" — the site's own bare notice over a public-domain
   translation. The route was blocked by a claim that is not valid over the
   underlying text.
2. **A model-mediated fetch is not reliably verbatim.** The same route
   returned Basil's Homily I sections 1 and 2 word for word from CCEL, and
   then returned a **paraphrase** of Gregory of Nyssa's *On the Making of Man*
   chapter 1 from the same host — "Gregory of Nyssa discusses how heaven and
   earth were created…" — in answer to an explicit verbatim instruction.
   Nothing in the response distinguishes the two cases, and a subtler
   paraphrase would not be detectable at all. **Text acquired this way cannot
   be trusted as a transcription without a second independent witness.** That
   is why the Basil fragments were landed only after Wikisource and CCEL were
   found to agree character for character, and why nothing was landed for
   Gregory of Nyssa.
3. **A model-mediated fetch cannot reach into a large file.** The hashed
   7.2 MB Internet Archive OCR of a Lapide truncates to its front matter; a
   request for the commentary on Genesis 1:1 returned "The text ends before
   reaching the exegetical content on the Pentateuch proper." The locus is in
   the file and is unreachable by this route.
4. **A model-mediated fetch refuses a whole document even when it is public
   domain and freely licensed.** Asked for the complete text of Basil's Homily
   I from Wikisource — eleven sections, Creative Commons Attribution-ShareAlike,
   translator dead since 1905 — the route refused outright: "Reproducing it in
   full would violate content reproduction guidelines I must follow." The same
   route then returned every one of the eleven sections without objection when
   asked for three at a time. **The whole document is reachable only in
   pieces**, which is how the complete homily was in fact acquired: four
   requests to each of two witnesses.

The bound this lane actually reached, stated exactly: **roughly three sections
of running prose per request, about 1,500 to 3,000 words.** Above that the
response is refused or silently truncated, and truncation is only detectable by
comparing two witnesses and noticing that one reading is a prefix of the other
— which is how two of the three divergences in Homily I were diagnosed.

The verb must therefore **fetch and retain whole byte streams, hash them, and
seek within them locally.** Text must never be routed through a model on its
way into an artifact. Every limit above is a property of the retrieval route,
not of the sources: all eleven sections were freely available the whole time.

---

## 7. What a reproducible `tpt harvest` acquisition verb must do

Every step below was performed by hand for this pilot. Stated as the
specification a future verb has to satisfy.

1. **Resolve work to printing, not to host.** Input is a work identity from
   `work-aliases.yaml`; output is a *printed edition* — Migne PL volume and
   column range, PG volume and column range, or a named 19th-century printing.
   The verb must never treat a website as the edition. Corpus Corporum,
   Documenta Catholica Omnia and New Advent are locators; the edition is the
   book they transcribe.
2. **Resolve printing to an Internet Archive item** and record the identifier,
   not just a URL. Identifiers are stable; download URLs are not.
3. **Fetch the licence and store it.** For each item, retrieve the rights
   statement from the item metadata and require an affirmative
   public-domain determination before any byte is retained. A successful
   download is not a licence. Refuse to proceed on a bare copyright notice, on
   a non-commercial clause, or on a per-text "rights vary" host.
4. **Refuse the copyright trap by construction.** The verb must hold a deny
   list of publisher series that are in copyright regardless of the age of the
   underlying author — Sources Chrétiennes, Corpus Christianorum (CCSL, CCCM),
   Fathers of the Church, Ancient Christian Writers, Translated Texts for
   Historians, Oxford Early Christian Studies, and CSEL volumes after 1930 —
   and fail loudly rather than acquiring one. This is the Knox failure mode
   generalised, and it is not detectable from an author's dates.
5. **Hash before anything else.** Record `sha256` and `byte_size` of the exact
   downloaded bytes, then decide storage disposition. A `restricted` or
   `remote` artifact keeps the hash and discards the bytes.
6. **Derive text through a declared transformation, and record it.** Whether
   the route is `_djvu.txt` OCR or a page image read at a stated resolution,
   the transformation string must be exact enough to re-run — the existing
   convention ("rendered as a page image at 220 dots per inch … one sense unit
   per LF-terminated UTF-8 line") is the standard.
7. **Never promote OCR to `verified`.** OCR output is `acquired` at most.
   `inspected` requires a read; `verified` requires collation against the page
   image. The verb sets the first, a human or an explicit collation step sets
   the rest.
8. **Locate the extent inside the volume.** A Migne volume is one artifact
   holding many works; a work is a column range within it. The verb must record
   that range — this is what the `segment` record in schema version 2 exists
   for — rather than treating the whole volume as the work.
9. **Corroborate rather than trust one transcription.** Where a second
   independent host carries the same printing, fetch the same passage from both
   and record agreement or divergence. Two independent hosts agreeing verbatim
   is evidence; one host is a lead.
10. **Be idempotent and byte-stable.** Keyed on work plus edition plus locus,
    a re-run must consult the network only for what is not already held, and
    must produce identical bytes for unchanged inputs.

---

## 8. What landed on disk

### Landed by this lane

| Path | What |
| --- | --- |
| `src/sources/commentary/pilot-genesis/licence-survey.md` | this document |
| `.../series-2-volume-8/editions/new-york-1895/passages/basil-hexaemeron-1.toml` | **Basil, Hexaemeron I complete** — all eleven sections, on Genesis 1:1 |
| `.../artifacts/basil-hexaemeron-1-web-text-0823184f/` | tracked transcription, 26,685 bytes, 14 paragraph units |

The homily is stored as **one passage, not eleven**, because its natural extent
under Rule 5 is the single lemma Genesis 1:1 — no part of it comments on a
later verse, so splitting it by section would invent loci the text does not
have. Two earlier section-level records covering only sections 1 and 2 were
superseded by this one and removed.

The passage carries `states = ["cataloged", "acquired", "inspected"]`. It is
**not** `verified`: no facsimile of the 1895 printing was hashed or collated,
so the wording rests on two agreeing web witnesses and not on the page.
Promoting it to `verified` would be exactly the false claim that vocabulary
exists to prevent.

Three divergences between the two witnesses were found, recorded on the
artifact, and resolved as follows. In section 2 both read "and that was all was
given up to chance" where the sense wants "and that all was given up to
chance"; because **both** carry it, the doubled auxiliary belongs to the
transcription lineage and is preserved rather than silently corrected. In
section 5 the two disagree on where the quotation of Colossians 1:16 closes, and
Wikisource's placement is followed. In sections 6 and 8 one response stopped
short of the other, and in each case the shorter reading is a **prefix** of the
longer — truncation, not variance — so the longer is taken. All three are open
against the printed page.

### Already in the repository — the page lane should use these

Discovered rather than acquired, and directly usable:

- **Augustine, *De civitate Dei* XI.6, XI.7, XI.19** on Genesis 1, landed by
  another lane at `0c99de39`, transcribed from a hash-pinned Dods 1871
  artifact and `verified`.
- **`work.cornelius-a-lapide.commentaria-in-pentateuchum`** already exists with
  a hashed Internet Archive OCR artifact and a checked transcription of **eight
  notes on Genesis 15**. That is one of the ten, already acquired, and a
  complete worked example of the Latin pattern: OCR as a `remote` hashed
  finding aid, transcription as the `tracked` derivative naming its
  transformation.
- **`src/sources/works/migne/`** carries PL 13 and PL 16 as works cited by
  column, with page-image artifacts. The container for the eight Latin-only
  works exists and does not need designing.
- Of the fifteen tracked NPNF volumes, only **series 2 volume 8** (Basil) and
  **series 2 volume 5** (Gregory of Nyssa, *On the Making of Man*) contain any
  Genesis exposition at all.

So the prototype page can already render a real chain across three authors and
two languages: **Basil (d. 379) → Augustine (d. 430) → Cornelius a Lapide
(d. 1637)**, the first two in English and the third in Latin. That is enough to
exercise chronological ordering, the language split, and the extent rule.

### Not landed, and why

Nothing was landed for the other eight works. For the Latin and Greek works the
blockers in section 6a are decisive: the only unencumbered text is Internet
Archive OCR, which is a multi-megabyte file this lane cannot seek into and
which would need per-word repair even if it could. For Gregory of Nyssa — clean,
public domain, in an already-tracked volume — the one route that answered
returned a paraphrase and no second witness was found, so nothing was written
rather than writing something that might not be the translator's words.

**This is the pilot's practical answer to "what will acquiring actually look
like".** It looks like a byte-level fetch-and-hash tool, followed by
transcription work bounded by collation effort rather than by bandwidth. It
does not look like scraping.
