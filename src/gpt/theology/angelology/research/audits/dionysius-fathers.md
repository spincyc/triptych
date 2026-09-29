# Dionysius and Fathers source audit — GPT angelology

> Retained research record, consolidated 2026-09-29. Scratch filenames identify the original acquisition history, not required runtime dependencies. Current durable identities and fingerprints are in [source-bindings.toml](../source-bindings.toml); the [source-audit index](../source-audit.md) records controlling corrections and reading scopes.


Consulted 2026-09-29. This durable record preserves the Dionysian and patristic research evidence. Independent prose was composed from the witnesses below, not from the incomplete Claude narrative. Existing source downloads were reusable evidence, checked at the passages used. No central corpus files were changed by this agent.

## Parker: exact translation and witness

- Work: Dionysius, *On the Heavenly Hierarchy* (also conventionally *Celestial Hierarchy*).
- Translation: John Parker, *The Works of Dionysius the Areopagite*, part II, London and Oxford: James Parker and Co., **1899**, printed pp.1–66.
- Whole-part facsimile: https://archive.org/download/worksofdionysius02pseu/worksofdionysius02pseu.pdf ; metadata https://archive.org/metadata/worksofdionysius02pseu .
- Download: `.scratch/dionysius-fathers/parker1899.pdf`, 9,190,498bytes, SHA256 `90c7fdafa8b74bffccb85ee8a6f3a87eb34be34f9747bd3ae6a33e47ec9e351a`.
- Whole-part IA OCR: https://archive.org/download/worksofdionysius02pseu/worksofdionysius02pseu_djvu.txt ; `.scratch/dionysius-fathers/parker1899-ocr.txt`, SHA256 `dd081ebd3e2817e6481329a614e688b6a1668a1904c758aaf0f04e6c6f427cf0`.
- CH is printed1–66 = **PDF pages27–92 inclusive** (1-based). Part title page PDF7 directly viewed; date1899 legible. 1897 is an earlier research lead, not the edition used for these quotations.
- Complete CH electronic transcription read: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm ; existing `.scratch/sources/text/tert-areopagite_13_heavenly_hierarchy.txt` and raw matching HTML. Roger Pearse2004 footer explicitly places all material on page in public domain and allows copying. Ancient work and Parker1899 translation independently PD in US by age. No copyrighted modern translation used.
- Every chapter was read in full in transcription. All15 chapter headings and the short quotations in manuscript were collated against facsimile. This is not a diplomatic collation of every word of the translation, nor a Greek critical edition.
- Selected facsimile source pages in Parker inspection PDF: 7,27,30,39,42,47,49,50,57,61,67,68,70,72,79,80,81,92. Extra inspection pages43,48,62,69. (All1-based.) Render outputs under `build/gpt/theology/angelology/source-review-dionysius/` and `source-review-dionysius-extra/`.
- Exact chapterXV printed title has **anthromorphic**, retained rather than silently normalized to anthropomorphic. ChapterIV printed question mark is within quoted Angels. Physical line-wrap hyphenation regularized; substantive spelling preserved.
- Parker prints no internal section numbers in V, VI, XIV. PG divides VI into1–2. Manuscript says V/XIV unnumbered; VI.1 refers PG first division.

## PG3: locator witness

- *Patrologiae cursus completus, series Graeca*, vol.III, Migne, Greek text and facing Latin with Balthasar Corderius exposition. Historical printed edition PD.
- IA item https://archive.org/details/Patrologia_Graeca_vol_003 ; used smaller complete facsimile https://archive.org/download/Patrologia_Graeca_vol_003/PG003_text.pdf .
- `.scratch/dionysius-fathers/pg3.pdf`, 32,351,768bytes, SHA256 `4792e56d3fe95bdcc9f86b09821816ce41bfdd33fe4a1484dc58725cc66e9c98`.
- OCR https://archive.org/download/Patrologia_Graeca_vol_003/PG003_djvu.txt ; `.scratch/dionysius-fathers/pg3-ocr.txt`, SHA256 `c3f4056dcf99ef76ac08d0e16445f01bcd43b5a1d75a52b757b545d045ab855e`.
- CH text and interspersed commentary occupy **cols119–340 = PDF60–170**. Chapter ranges below are original Greek/Latin text spans including paired column endpoints; intervening Corderius exposition is not treated as additional Dionysian text. No A–D subcolumn precision is asserted.
- PG was inspected for chapter boundaries, titles/section numerals and column numbers, not translated independently throughout. Source PDF1-based selected pages60,61,62,68,72,73,82,83,84,89,91,98,100,101,103,106,119,120,121,129,130,131,136,137,142,143,146,147,150,153,154,161,163,170. These were rendered and inspected as contact sheets with selected enlarged pages. Full original-language philological collation remains outside the verification claim.

| CH | Parker printed pages | PG3 original-text column span | Quotation collated (locator, printed page) |
|---|---|---|---|
| I | 1–4 |119–124| “gift of goodness” I.1,p1 |
| II |4–13|135–146| “many-footed and many-faced” II.1,p4 |
| III |13–16|163–168| “a sacred order and science and operation” III.1,p13 |
| IV |16–21|177–182| “through goodness” IV.1,p17 |
| V |21–22|195–196| “superior ranks possess the illuminations and powers of their subordinates” unnumbered,p22 |
| VI |23–24|199–202| “alone distinctly knows” VI.1 (PG division),p23 |
| VII |24–31|205–212| “kindling or burning” VII.1,p24 |
| VIII |31–35|237–242| “unslavish elevation” VIII.1,p31 |
| IX |35–40|257–262| “princely and leading function” IX.1,p36 |
| X |41–42|271–274| “more hidden and more manifest” X.1,p41 |
| XI |42–44|283–286| “essence, and power, and energy” XI.2,p43 |
| XII |44–45|291–294| “one harmonious and binding fellowship” XII.2,p44 |
| XIII |46–53|299–308| “through fire” XIII.2,p46 |
| XIV |53–54|321–322| “cannot be numbered by us” unnumbered,p53 |
| XV |54–66|325–340| “honoured by silence” XV.9,p66 |

## Augustine

- *De civitate Dei*, trans. Marcus Dods, *City of God*, volI (Edinburgh T&TClark1871), retained PD Project Gutenberg transcription of complete first volume.
- https://www.gutenberg.org/ebooks/45304 ; retained `src/sources/works/augustine/de-civitate-dei/editions/dods-1871/artifacts/pg45304-body-lf/city-of-god-volume-1.txt`.
- Directly read XI9–10,13–19,29; primary exposition uses XI9–10,13,15–17,29. XI9: created angels, first-light interpretation, participated illumination, evil deprivation. XI10: Trinity's simplicity, creature has gifts it is not. XI13: assurance/perseverance alternatives. XI15–17: pride, natural rank versus moral good, good created nature even in fallen spirits. XI29: angels know Trinity and creatures inWord and creatures inownbeing, selfknowledge.
- No1871 facsimile collation performed in this subtask; manuscript paraphrases rather than quotes Dods. No reading of all22books claimed.

## Basil

- *De Spiritu Sancto / On the Holy Spirit* XVI37–38 directly read; beginning39 for context. Blomfield Jackson, NPNF secondseriesVIII, CCEL full-volume header **Edinburgh T&TClark1895**.
- https://www.ccel.org/ccel/schaff/npnf208.txt ; existing `.scratch/sources/text/ccel-npnf208.txt`; exact retained edition managed by source-library agent.
- ChapterXVI lines9855ff; core37–38 extends through~9994 in this download. It argues from angelic holiness, permanence, worship, prophecy and concord to Spirit's inseparability from FatherSon. Iron/fire analogy distinguishes substance from sanctification. Aerialspirit/immaterialfire tentative language retained as difference from later determinate immateriality.
- PD historical translation; no modern annotation borrowed. Electronic transcription read, no facsimile collation.

## Gregory the Great

- *Homiliae in Evangelia* XXXIV3,6–14 read directly in Latin; wider homily also inspected for context. https://la.wikisource.org/wiki/Homiliarum_in_Evangelia/XXXIV (complete collection https://la.wikisource.org/wiki/Homiliarum_in_Evangelia ).
- Retained `src/sources/works/gregory-the-great/homiliae-in-evangelia/editions/2026-09-17-wikisource/artifacts/complete-extracted-text-dc25dd69/gregory-whole.txt`.
- Ancient Latin PD. Existing complete Wikisource extraction subject to retained CC BY-SA3 metadata/notice as recorded by repository; no new English translation copied. Narrative is original paraphrase of Latin. No PL76 facsimile collation performed and no false exactPLcolumn supplied.
- XXXIV7 ascending names angels,archangels,virtues,powers,principalities,dominions,thrones,cherubim,seraphim. XXXIV8 office/nature;9 scriptural names;10 offices;11 moral analogies;12 Dionysian mission;13 expressly declines to determine personal missions of highestorders, affirms mediated sending and continued contemplation;14 gifts common in charity.
- New Advent ST I108 often prints Gregorian locator **Hom.xx iv / xxiv** where text corresponds **XXXIV**. Manuscript cites Gregory directly asXXXIV rather than reproducing apparent received-locator error. This source discrepancy does not alter argument.

## John of Damascus

- *Exposition of the Orthodox Faith* II3–4 read completely in S.D.F.Salmond translation, NPNF secondseriesIX, CCEL header **Edinburgh T&TClark1898**. Do not describe this witnessed header asNY1899.
- https://www.ccel.org/ccel/schaff/npnf209.txt ; existing `.scratch/sources/text/ccel-npnf209.txt`.
- II3 begins~30061; II4 follows afternotes and extends~30300. II3 created,free,incorporeal intellectual life; grace, illumination, circumscription, mission, triads; explicit uncertainty whether equalessence; preference forangelsbeforevisiblecreation. II4 fall, deprivation, permission, prediction, temptation, finality.
- PD historical translation; transcription only, no facsimile collation.

## Aquinas

- *Summa theologiae*, English Dominican Fathers secondrev1920, New Advent electronic transcription, fullquestions in reused `.scratch/sources/text/na-summa-NNNN.txt` where NNNN=1050 forI50,1108 forI108,etc. URLs https://www.newadvent.org/summa/1050.htm etc.
- Main CHconcordance checked against complete I106,107,108,112 and relevant I54,55,111 passages. Additional comparisons are marked as comparisons, not represented as directCHcitations. Greek-to-Latin medieval translation history not independently collated; Parker is not Aquinas's translation.
- I1a9 consulted directly at https://www.newadvent.org/summa/1001.htm . Body usesCHI veils. Ad3's printedCHreference says**i** although developed dissimilar-symbol argument isCHII. Readernote and concordance explicitly preserve the discrepancy.
- Corrected locator during check: exclusion of hierarchy fromTrinity is **I108a1 body**, notad2. Definingquote also occursobjection2.
- Nonexhaustive claims only. No numerical tally of allDionysiancitations.

## Historical identity and dating

- Benedict XVI general audience14May2008, official Vatican https://www.vatican.va/content/benedict-xvi/en/audiences/2008/documents/hf_ben-xvi_aud_20080514.html . Existing `.scratch/sources/text/vat-ben16-aud-20080514.txt` directly read dating/pseudonym/Proclus paragraphs. Copyrighted contemporary text; brief original paraphrase only, not corpusredistribution by this agent.
- Eric Perl, “Pseudo-Dionysius the Areopagite,” *Cambridge History of Philosophy in Late Antiquity*,ch42, publisherpublicsummary, online28May2011, https://doi.org/10.1017/CHOL9780521194846.014 . Summary directly read; it explicitly dates late5th/early6th and identifiesActs17:34 persona. Fullchapter NOT read or retained. Copyrighted: metadata+shortparaphrase only. Publisherwebpage prints anomalousprintyear2000; manuscript usesonline2011 rather than assertingprintyear.
- Traditionalapostolicattribution, historicalcompositiondate, and theologicalreception remain distinct. No claim of apostolic authorship established by modernhistory; no theological conclusion inferred from pseudonym alone.

## Verification ceiling and integrated records

All5ownedTeX files have balancedliteralbracecounts and no unexpected controlcharacters. CH has15orderedsubsections and15quotationlocators. Integrated production checks are recorded separately by root. Registered source identities, provenance, rights and fingerprints appear in source-bindings.toml and the source library. Auditconcordance is manuallyselected, never exhaustivelycounted. PGinspection supports columnmap; Parkerfacsimile supports titles/shortquotations; narrative content comes from fullreadCHtranslation and selectedFathers. No claim to completeAugustine/Basil/Gregory/Damascene study or exhaustive modernliterature.

### Retained-witness confirmation after acquisition

Source-library agent acquired `.scratch/source-library/perl-cambridge.html` and `.txt`, and `.scratch/source-library/st-i1.html` and `.txt`. Both raw HTML documents were inspected through simple tag removal; the derived Perl summary at lines940ff and ST I1 article9 were then inspected as well. They confirm the same consulted passages as the browser witnesses. Binding may therefore identify those acquired exact files, with the same reading ceiling: Perl publisher summary only, not full chapter; ST I1 article9 directly read. The integrated source bindings now identify durable artifacts and fingerprints.


### Inclusive Parker pagination correction

Rechecked all fifteen chapter boundaries against the acquired facsimile and page-separated PDF text after reviewer noted shared transition pages. My initial ranges incorrectly stopped short of shared end/start pages for I, II, III, VI, VII, XIII, XIV. Correct inclusive ranges are I1–4; II4–13; III13–16; IV16–21; V21–22; VI23–24; VII24–31; VIII31–35; IX35–40; X41–42; XI42–44; XII44–45; XIII46–53; XIV53–54; XV54–66. The chapter footnotes and appendix04 now match this corrected table. Shared pages4,13,16,24,31,53,54 were reinspected at full size: each visibly contains the preceding chapter's conclusion above the next chapter heading. The short-quotation page locators were already correct and do not change.
