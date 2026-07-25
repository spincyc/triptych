# Natural and Positive, Divine and Human — Source Audit

All checks below were performed publication-locally by the authoring agent on
2026-07-25 (UTC). "Fetched and hashed" means a direct HTTPS fetch of the named
URL whose exact response bytes were hashed with SHA-256 and read; quoted
wording in the article was extracted verbatim from those exact responses.
Working glosses are project translations governed by the quoted original.
This audit records verification events and ceilings; interpretive use is
governed by `scope.md` and the article's notes.

## Witness table (fetched, hashed, read 2026-07-25)

| Source / text | Witness (host path) | SHA-256 prefix | Record |
|---|---|---|---|
| CIC 1983, Book I LA (cann. 1–203) | vatican.va `/archive/cod-iuris-canonici/latin/.../cic_liberI_la.html` | `799c13a1` | codex LA edition + canon passages |
| CIC 1983, Book II LA | same path `liberII` | `be259afe` | codex LA edition |
| CIC 1983, Book III LA | same path `liberIII` | `9184880a` | codex LA edition |
| CIC 1983, Book IV LA | same path `liberIV` | `853b93dd` | codex LA edition |
| CIC 1983, Book V LA | same path `liberV` | `3a448a0d` | codex LA edition |
| CIC 1983, Book VI LA (rev.) | same path `liberVI` | `8a85a5ec` | byte-identical to registered artifact; passages canon-1315, canon-1399 added |
| CIC 1983, Book VII LA | same path `liberVII` | `7eb4bdf0` | codex LA edition (search coverage only) |
| CIC 1983, EN pages (15) | vatican.va `/archive/cod-iuris-canonici/eng/documents/...` (cann. 1-6, 7-22, 23-28, 35-93, 96-123, 129-144, 145-196, 197-199, 204-207, 368-430, 747-755, 998-1165, 1244-1253, 1254-1310, 1311-1363) | `a16345e2`, `b7f054a1`, `924caad0`, `95c544ce`, `f2fa43fa`, `15e12e7a`, `f63eac34`, `0e783517`, `84395b3c`, `1d281846`, `70557828`, `e421c905`, `2dc7e394`, `c75ff659`, `d698995e` | codex EN edition + canon passages |
| CIC 1983, Book VI Part II EN | `.../cic_lib6-cann1364-1399_en.html` | `94b1139b` | byte-identical to registered artifact; passage canon-1399 added |
| ST I-II qq. 90–92, 93, 94, 95–97 LA | corpusthomisticum.org `sth2090/2093/2094/2095.html` | `b06d31d0`, `5660edff`, `af568d0c`, `4532fe3e` | LA edition + 30 locus passages |
| ST I-II qq. 90–97 EN | newadvent.org `summa/2090–2097.htm` | `77ff23e8`, `55572b27`, `cd8d5c5d`, `c10a1a29`, `7b3b7b77`, `24bcdcd7`, `2cf77cb5`, `ba465f73` | EN edition + 30 locus passages |
| Isidore, Etym. (Lindsay 1911 vol. 1) leaf 192 | iiif.archive.org `isidori01isiduoft$192/full/1200,/...` | `3f3ff160` | tracked page image + passages V.2, V.3 |
| Isidore leaf 193 | same, `$193` | `030a7de2` | tracked page image + passage V.4 |
| Isidore leaf 196 | same, `$196` | `c08402f2` | tracked page image + passage V.21 |
| Isidore OCR (discovery aid) | archive.org `isidori01isiduoft_djvu.txt` | `b140ae8c` | remote artifact |
| Gratian, Decretum (Friedberg/MDZ), 11 chapter pages | geschichte.digitale-sammlungen.de `/decretum-gratiani/kapitel/dc_chapter_0_0004, 0005, 0011, 0031, 0033, 0034, 0050, 0051, 0059, 0060, 0071` | `104c8aed`, `a4219bab`, `5d1858ba`, `8844e915`, `c567e557`, `d1989db9`, `51448ab0`, `c477e8cb`, `361947e1`, `9d2420f3`, `3d676141` | edition + 11 passages |
| CCC natural moral law EN | vatican.va `/content/catechism/en/.../i_the_natural_moral_law.html` | `306f5fd2` | EN edition + passage 1954-1960 |
| CCC Lex moralis LA (1950–1986) | vatican.va `/archive/catechism_lt/p3s1c3a1_lt.htm` | `c57ac098` | LA edition + passages 1950-1953, 1954-1960 |
| Veritatis splendor EN | vatican.va `/content/john-paul-ii/en/encyclicals/.../veritatis-splendor.html` | `144095cc` | work + edition + passages 12, 40-45 |
| Sacrae disciplinae leges EN | vatican.va `/content/john-paul-ii/en/apost_constitutions/...` | `e1b87d2b` | byte-identical to registered artifact; bound |
| Pascite gregem Dei EN | vatican.va `/content/francesco/en/apost_constitutions/...` | `ec0209f7` | new artifact (registered response `8bee6401` no longer served); bound |
| Dignitatis humanae EN | vatican.va `/archive/hist_councils/ii_vatican_council/documents/...dignitatis-humanae_en.html` | `0ce2da9b` | byte-identical to registered artifact; existing passage 1-3 bound |

Exact full hashes for every witness are in the corresponding
`src/sources/works/.../artifact.toml` records; the prefixes above are an index,
not the record of authority.

## Canon verification

Every canon quoted in the article (cc. 1 [orientation], 5, 6, 7, 8, 9, 11, 17,
19, 20, 21, 22, 23–28, 85–93, 98, 113, 129, 145, 199, 207, 375, 748, 750, 751,
1008, 1059, 1075, 1078–1080, 1084, 1163, 1165, 1249, 1290, 1315, 1399) was
extracted verbatim from the exact fetched Latin book page and, where an English
rendering is quoted, from the exact fetched English canon-range page. Ceilings:
the web deliveries are not the *Acta Apostolicae Sedis*; no AAS collation was
performed; currentness is asserted for the quoted canons as delivered on
2026-07-25, not as a completed search of every amending act. Delivery defects
found and recorded, not repaired: c. 11 EN "efficient use of reason" (LA
*sufficienti rationis usu*); c. 9 LA "in eisde praeteritis"; c. 20 LA "ili";
c. 1315 §1 LA "divinamcongrua".

## Bounded search: divine-law vocabulary inventory

Method: case-insensitive literal scans of the text extracted from the seven
exact fetched Latin book pages for the patterns `divin*` and the collocations
`ius naturale` / `lex naturalis` / `iuris naturalis` / `lege naturali`,
segmented by canon (script-assisted; 2026-07-25). Result: 65 matched canon
contexts; those invoking law-categories are tabled in section 8; the remainder
is predominantly *cultus divinus* (divine worship) vocabulary plus formation
and spirituality usages (e.g. cc. 211, 222, 252, 646, 663), which the article
expressly distinguishes from taxonomy usage. Ceilings: literal raw-text method
over restricted (unretained) responses — the search is replayable only by
refetching; it cannot exclude periphrastic invocations (c. 1084 §1 *ex ipsa
eius natura* was found by reading, not by the scan); it is not a negative
claim about the Code beyond the stated method. No source-library search
receipt exists because the artifacts are not retained or indexable; the claim
is publication-local and correctable.

## Isidore verification

Etym. V.ii, V.iii, V.iv (body), and V.xxi were read visually at the retained
width-1200 IIIF page images of leaves 192, 193, and 196 of the Lindsay 1911
scan (tracked artifacts with recorded public-domain basis); the full-size
renditions were also read during research. The OCR discovery text agrees with
the visual readings at every quoted phrase. V.v–viii were read on leaf 193;
V.i and V.xx reach the article only as received in Gratian (D.7 c.1 was
fetched but not used; D.4 pr. quotes V.xx), and Etym. II.x was checked at OCR
level only — the article marks both ceilings. Chapter numbering follows
Lindsay.

## Gratian verification

The eleven MDZ chapter pages were fetched, hashed, and read; the dicta
Gratiani and chapter texts quoted in section 7 were extracted verbatim. The
MDZ edition transcribes Friedberg 1879; the article's claims are bounded to
that vulgate witness. The archive.org scan of Friedberg vol. 1
(`bub_gb_sfwfAQAAMAAJ`, OCR hash `a2dec9a2...`) was downloaded as a candidate
witness but its OCR of the opening distinctions proved unusable and no claim
rests on it; recorded here as a negative research event.

## Magisterial texts

CCC: the EN natural-moral-law page carries 1954–1960; the LA article page
carries 1950–1986 and is the control; CCC 1950–1953 are quoted from the Latin
with labeled working glosses because the registered EN page does not carry
them. VS: EN official delivery; the Latin AAS text was not collated. DH: EN
delivery byte-identical to the registered 2026-07-23 state; DH 3 quoted from
it. Promulgation facts for the 1983 Code and the Book VI revision were
verified at the two constitutions' EN pages as described in the witness table.

## Consequential exclusions

- No CCEO canon was examined; no Eastern-law conclusion is drawn or implied.
- The 1917 Code was not re-verified for this leaf; the two comparisons made
  (c. 8 §1 promulgation; forty-year custom) are carried at reported level and
  marked as such.
- The Roman-law texts behind Isidore (Digest, Institutes) were not examined;
  Isidore is cited as transmitter.
- The new-natural-law and classical-Thomist dispute literature was not
  consulted at source; positions are mapped from standard self-descriptions
  and the article says so.
- The standard Code commentaries were consulted for orientation only and are
  not cited as establishing any contested position.
- CCC 1902–1903 and VS 46–48 are referenced at reported level (read in the
  same dated deliveries but outside the registered passage set).

## Build note

The final build log contains zero overfull or underfull box reports and no
LaTeX warnings; one "ignored: Infinite glue shrinkage found in box being
split" message accompanies a longtable page split, identical in kind to the
message emitted by the sibling faith article's own build with the shared
preamble, and has no visible effect on output (page-by-page raster review
performed).
