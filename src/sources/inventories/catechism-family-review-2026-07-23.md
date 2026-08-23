# Catechism Source-Family Review

Reviewed on 2026-07-23.

This is the semantic audit checkpoint for
`family.catholic-church.catechism`. It supplements the migration ledger. It is
not a source manifest, does not create a binding, and does not promote legacy
words such as “checked” or “verified” into source-library evidence states.

## Review boundary

The review covered all 42 ledger owners with a positive Catechism trace:

- 8 articles;
- 5 biographies;
- 2 novena parents;
- 14 liturgical publications; and
- 13 theological publications.

It also checked two ownership edges that the trace scan cannot by itself
resolve. `theology/sacraments-at-a-glance` renders the sacramental source
owner’s shared material and therefore needs an inherited evidence binding.
The shared postconciliar proper owner contributes Missal formulary evidence to
its leaves but contains no Catechism occurrence and must not receive a
Catechism binding.

At the audit checkpoint, no reviewed publication had a canonical Catechism
source ID, a retained or hash-pinned Catechism artifact, or a source
fingerprint. Every legacy migration binding therefore began `cataloged`, even
where a local research record honestly preserves an earlier inspection or
verification event. Promotion requires a new review against exact canonical
bytes.

## Identity decision

The recurring family is not one undifferentiated web source. The canonical
graph distinguishes:

1. the promulgated intellectual work, *Catechism of the Catholic Church*;
2. the 1997 Latin typical edition approved and promulgated by
   *Laetamur magnopere*;
3. each materially identified official English expression or dated web state;
4. exact delivery artifacts, including the archived IntraText presentation,
   the current Holy See pages, and the USCCB second-edition flipbook
   representations;
5. addressable paragraph passages;
6. a bounded complete-corpus representation; and
7. the 2018 rescript revising paragraph 2267 as a separate promulgating act
   related to, but not conflated with, the Catechism work.

The 2005 *Compendium of the Catechism of the Catholic Church*, the 1566 Roman
Catechism, Deharbe’s catechism, Luther’s catechisms, the Racovian Catechism,
the 1560 Venetian catechism, and Gregory of Nyssa’s *Great Catechism* are
separate works. Generic prose about “a catechism” is not a Catechism passage
occurrence.

John Paul II’s *Laetamur magnopere* identifies the first French text with
*Fidei depositum* in 1992 and the Latin typical edition promulgated on
1997-08-15 as the definitive text. The 2018 rescript orders the new wording of
paragraph 2267 to be translated and inserted into all editions. Paragraph
numbers alone consequently do not pin wording or amendment state.

## Acquired candidates and rights boundary

The following exact candidates were acquired into run-local temporary storage
for identity and rights review. Their bytes are not repository content.

| Candidate | SHA-256 | Bytes | Finding |
|---|---|---:|---|
| Holy See Latin index | `fb4587784aefc57043cf32cb7e9647f3307a83a51ae1339c40890392eea04b67` | 71,014 | Official Latin navigation artifact in a dated web state |
| Holy See Latin Fifth Commandment page | `8d5f9d14cae3c414cf7584680e8dabb088fce408f250da45f274cb13698b1c80` | 49,562 | Contains revised Latin paragraph 2267 and a separately labelled preservation of the preceding wording |
| Holy See archived English index | `92199edc96afdb8d76df6682fced3a2e631f786c2d171abfed49a3dc64e3e05d` | 38,941 | IntraText delivery dated 2003-11-04; not silently current |
| Holy See archived English “Mary—Mother of Christ, Mother of the Church” page | `779e21c8cef55b17d8dca479303e63d7d10acfd17aa39712c94590413e6aa0a6` | 14,855 | Dated IntraText page containing paragraphs 963–975, including complete paragraph 970 |
| Holy See current English index | `9d6cfe2fc10b3479cc129fdfddf16b0cc924ab1a61f2ec37ac6a6604af9a7ca3` | 106,296 | Mutable current navigation artifact |
| Holy See current English “Respect for Human Life” page | `9e71e262a054b2c617c4a0b29bf2c68937c96b986bf3613ddd7b729e1309fe16` | 123,465 | Contains the 2018 wording of paragraph 2267 |
| Holy See current English sacramental “In Brief” page | `7004d8d92534eecebd07fc9c40ffe57f13b0b38b2d7a6a4564220df872e2787a` | 108,876 | Contains paragraphs 1131–1134 |
| Holy See current English Baptism celebration page | `d42f082af01c15e2dc5010dac51cf8a4a1d6ed24a86d2c541ded0afd96c1c522` | 116,183 | Contains paragraph 1240 and its Latin and Eastern formulas |
| Holy See current English Confirmation signs and rite page | `6289add4b17bb98c524f9911f351e98eb24f895ba33ea1fb2fca20a9092e960b` | 114,583 | Contains paragraph 1300 and its Latin and Eastern formulas |
| Holy See current English Penance and Reconciliation page | `d8a3127ad843691eaa10a945ee3b635f2d8114cccdedc502806c1fd2bbab2759` | 115,345 | Contains paragraph 1449 and the Latin formula of absolution |
| USCCB flipbook landing page | `f90d8aab80ef5af293e4b539c20bd3c2db67367774fe0ac21709244cb0ec2f60` | 4,011 | Identifies the second edition and inclusion of revised paragraph 2267 |
| USCCB flipbook imprint page | `10b80026d520768a446b7010a01b29aaf1c4d15f3fe4ecf2328a5a8bc4d9efea` | 8,537 | Identifies ISBN 978-1-60137-649-7 and first printing, November 2019 |
| USCCB flipbook workspace | `a093c697cda349af4c13d67428699962a5fb2a40453f6458d835ac09a5418dc4` | 29,679 | Identifies the table of contents and digital publication metadata |
| USCCB complete search representation | `def1b7d1465a903d915d5505aae3d99b719167a3f456f1dc2d9bdd676109f49f` | 1,999,929 | One JSON search representation containing all 924 numbered flipbook pages |
| 2018 rescript, English Holy See page | `fa5cea2c6e6ca13bb5a292abcb10598388963a8e1a0aaa7e46cbf93676df932c` | 8,502 | Official English delivery of the amendment act |
| 2018 rescript, Latin Holy See page | `6078b43bd1024ce7b2d51789ccfdcee3b028402c8a4470f6347d79f93f5a058e` | 8,594 | Official Latin delivery of the amendment act |

The Holy See portal terms permit viewing for personal and non-profit use but
prohibit collection, reproduction, dissemination, and transfer absent written
authorization. The USCCB imprint reserves the Catechism and translation rights
and states that reprinting requires permission. Successful public retrieval is
therefore not a repository distribution license. These artifacts are
registered as `restricted`, with exact hashes, retrieval dates, provenance,
and public retrieval routes, but without payloads.

This rights review is complete for the candidates above, not for every
language, historical printing, or third-party delivery artifact. The family
remains `partially-reviewed`.

The official August 2018 *Acta Apostolicae Sedis* issue was also located and
hashed, but its issue PDF belongs to the separate AAS serial family. It must
not be duplicated under the paragraph-2267 act merely because that act occurs
inside the issue.

## Canonical graph decision

The first canonical slice uses these stable identities:

- `work.catholic-church.catechism`;
- `edition.catholic-church.catechism.latin-typical-1997`;
- `edition.catholic-church.catechism.latin-vatican-web-2026-07-23`, because
  the acquired Latin pages incorporate revised paragraph 2267 and cannot be
  attached silently to the fixed 1997 baseline;
- `edition.catholic-church.catechism.english-vatican-archive-2003`;
- `edition.catholic-church.catechism.english-vatican-web-2026-07-23`;
- `edition.catholic-church.catechism.english-usccb-second-2019`;
- exact restricted artifacts beneath those editions;
- a bounded corpus over the exact USCCB 924-page search representation;
- reusable inspected or verified passages for 65–67, 499, 970, 1131, 1240,
  1300, 1449, and 2267, including distinct USCCB 2019 and archived Vatican
  2003 records for paragraph 970;
- `work.holy-see.catechism-2267-rescript-2018`; and
- distinct Latin and English delivery editions and artifacts for that act.

The bounded USCCB search representation identifies all 924 numbered entries
delivered by that exact endpoint, without pretending that its extracted text
is a complete intellectual or textual corpus, a facsimile, or verification of
any publication claim. Its array order is not canonical page order, and its
text can contain extraction defects. Because the restricted bytes are not
distributed, an ordinary clone cannot search or replay it; the exact hash and
entry coordinates instead support bounded lawful reacquisition and manual
reinspection. Page images or another authoritative presentation remain
necessary where typography, punctuation, or exact formula wording is
consequential.

## Consumer decisions

The target codes below have these meanings:

- **work** — the legacy record did not identify an exact English expression;
- **archive-en** — the legacy record identifies the archived Holy See English
  presentation;
- **web-en** — the legacy record identifies the modern Holy See English
  presentation;
- **mixed-en** — loci were taken from both archived and modern official
  English presentations and must remain split until artifact review; and
- **2267-act** — the 2018 amendment act is an additional currentness control.

All rows begin `cataloged`. Role and interpretation remain local.

### Articles, biographies, and devotions

| Owner | Catechism loci | Local role | Initial target and qualification |
|---|---|---|---|
| `articles/canon-law/clerical-celibacy-chastity-and-continence` | 2337–2350; 1577–1580 | textual-control | web-en; the first range has stronger legacy review than the second |
| `articles/canon-law/natural-positive-divine-human-law` | 1750–1761; 1776–1802; 1950–1986; 2234–2246; 2284–2287 | textual-control | web-en; canon-law sources remain legal control |
| `articles/faith/at-the-end-of-every-why` | 221; 257; 1812–1829; 1965–1974; 1987–2011; 2095–2097 | textual-control | web-en |
| `articles/faith/council-missal-and-crisis` | 74–100; 748–975; 1322–1419; 2032–2051 | context | archive-en; broad bibliography, not a claim-level inspection |
| `articles/faith/freemasonry-and-the-catholic-church` | 391–395; 405; 813–822; 1237; 1262–1274; 1451–1460; 1673; 1735; 1857–1861; 2104–2117; 2150–2155; 2477–2479 | textual-control and context | work; no exact CCC URL or expression was pinned |
| `articles/faith/ontological-vertigo` | 301; 306–308 | textual-control | web-en; contains a short exact quotation |
| `articles/faith/the-due-return` | 1730–1748; 1817–1821; 1854–1864; 1950–1974; 2030–2043; 2060–2100; 2168–2195 | textual-control | web-en; Code remains juridical control |
| `articles/faith/trustful-surrender-to-divine-providence` | 268–278; 295; 301–324; 475; 599–614; 1376; 1730–1761; 1806; 1857–1861; 1989–2002; 2725; 2734–2745 | textual-control | web-en |
| `biographies/origen` | 362–366; 988–1004; 1016–1017; 1033–1037 | reception | web-en; doctrinal boundary, not an ancient historical witness |
| `biographies/saint-paul` | 442; 787–795; 1987–2029 | reception | web-en, but only a top-level index was recorded |
| `biographies/saint-peter` | 552–553; 880–882 | reception | web-en, but only a top-level index was recorded |
| `biographies/saint-thomas-aquinas` | 369; 372; 2334–2335; 2414; 2267 | reception and currentness-control | archive-en plus 2267-act; the revised paragraph must remain distinct |
| `biographies/tertullian` | 228; 852; 991; 1015; 1446; 1642; 1951; 2271; 2761; 2774; 2779; 2814; 2817 | reception | archive-en; selective later reception, not direct Tertullian evidence |
| `devotions/novenas/00-ascension-to-pentecost` | 243–248; 683–747; 733–741; 797–801; 965–970; 1076; 1285–1321; 1695; 1830–1832; 1996–2005; 2623; 2670–2672 | textual-control | work; the rendered reference omits 965–970 and differs from the audit at 797–801 |
| `devotions/novenas/10-our-lady-of-mount-carmel` | 487–507; 963–975; 1021–1037; 1667–1673; 2016; 2673–2679 | textual-control | work; rendered references omit the judgment and purgatory range |

The Ascension novena’s use of the 2005 *Compendium* for two hymns is a
separate-work direct witness. Its daily-prayer companion inherits that hymn
dependency, not the parent’s doctrinal Catechism bindings. The Mount Carmel
daily-prayer companion imports prayer fragments only and does not inherit the
parent’s Catechism bindings.

### Liturgy

| Owner | Catechism loci | Local role | Initial target and qualification |
|---|---|---|---|
| `liturgy/roman-rite/1962/ordinary/00-ordinary-of-the-mass` | 605; 1066–1209; 1322–1419; 1544–1553 | official-control | archive-en; never 1962 textual or rubrical control |
| `liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass` | core 1601, 1623, 1638–1642, 1652; analogue 1655–1658, 1663, 1666, 2378–2379 | currentness-control and analogue | web-en; keep the proposal-search loci separate from core controls |
| `liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost` | 1127–1129; 1385; 1391–1395; 1402–1405 | official-control | web-en |
| `liturgy/roman-rite/comparative/two-missals-one-sacrifice` | 1066–1209; 1322–1419; 1536–1666, especially 1127–1128 and 1362–1381 | official-control | work; the record does not pin language, edition, URL, or date |
| `liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/ordinary/00-order-of-mass` | 185–1065; 1066–1209; 1213–1284; 1322–1419 | official-control | archive-en; bibliography omits matrix-only 185–1065 and 1213–1284 |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s37-eleventh-sunday-in-ordinary-time-year-a` | 781–786 | context | work |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s38-twelfth-sunday-in-ordinary-time-year-a` | 302–314; 402–412 | context | work |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s39-thirteenth-sunday-in-ordinary-time-year-a` | 1213; 1227; 1265–1270 | context | work |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s40-fourteenth-sunday-in-ordinary-time-year-a` | 541–550 | context | web-en; shared passage candidate with S39–S41 |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s41-fifteenth-sunday-in-ordinary-time-year-a` | 541–550 | context | web-en; reuse the same future passage |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-sixteenth-sunday-in-ordinary-time-year-a` | 301–324; 541–550 | context | web-en; reuses the Providence and Kingdom page clusters |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s43-seventeenth-sunday-in-ordinary-time-year-a` | 121–123; 128–130; 311–312; 541–546 | context and official-control | split work and web-en; the recorded Creator URL supports 311–312, not the other ranges |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s26-most-holy-trinity-year-a` | 232–267 | official-control | web-en |
| `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s27-most-holy-body-and-blood-of-christ-year-a` | 1322–1419 | official-control | web-en |

The comparative publication’s reference to the Roman Catechism of 1566 is not
a Catechism-family passage. Postconciliar leaf publications inherit only their
shared Missal formulary evidence; their Catechism interpretation remains
leaf-owned.

### Theology

| Owner | Catechism loci | Local role | Initial target and qualification |
|---|---|---|---|
| `theology/heresies` | 27–49; 185–267; 385–421; 456–483; 638–682; 675–677; 748–870; 976–987; 1987–2029; 2088–2089 | official-control and currentness-control | web-en; keep apostasy at 2088–2089 distinct |
| `theology/mariology/angelus` | 456–511; 963–975, especially 970 | official-control | archive-en |
| `theology/mariology/apparitions` | 65–67; 956; 963–975; 1324; 2115–2117; 2617–2619; 2673–2679 | official-control | web-en |
| `theology/mariology/champion` | 4–10; 65–67; 302–314; 309–314; 426–429; 849–856; 970; 1210–1498; 1817–1821; 2221–2231; 2683–2684 | official-control | mixed-en |
| `theology/mariology/fatima` | 65–67; 668–682; 963–975; 1033–1037; 1362–1372; 2006–2011; 2683–2684 | official-control | mixed-en |
| `theology/mariology/guadalupe` | 65–67; 970; 1159–1162; 2131–2132 | official-control | web-en |
| `theology/mariology/la-salette` | 65–67; 970; 2168–2195; 2683–2684 | official-control | web-en |
| `theology/mariology/lourdes` | 65–67; 490–493; 547–550; 963–975; 1213–1284; 1500–1525 | official-control | mixed-en |
| `theology/mariology/marian-dogmas` | 65–67; 396–421; 456–511; 659–682; 946–975; 1618–1620; 2673–2679 | official-control; textual-control at 499 | mixed-en; patristic and conciliar references “through CCC” are reception, not primary inspection |
| `theology/mariology/regina-coeli` | 638–658; 963–975, especially 966 and 970 | official-control | archive-en |
| `theology/mariology/rosary` | 65–67; 244–248; 475; 484–486; 495; 529; 534–550; 554–556; 571–623; 638–667; 717; 731–741; 767–768; 963–972; 1213–1284; 1322–1419; 1427–1429; 1471–1479; 2617–2619; 2673–2679; 2705–2708 | official-control | mixed-en; conciliar references “through CCC” remain reception evidence |
| `theology/sacraments` | 1076–1209; 1210–1666, with exact wording at 1131, 1240, 1300, and 1449 | official-control and textual-control | web-en; highest-priority exact-passage replay |
| `theology/virtues` | 1716–1729; 1803–1811; 1812–1829; 1830–1845; 2337 | official-control | web-en |

`theology/sacraments-at-a-glance` inherits the sacramental owner’s exact
wording and doctrinal ranges through rendered shared fragments and summaries.
The 1962 Nuptial Mass separately imports the Matrimony summary and therefore
needs its own inherited binding for 1618–1666, especially 1623. Mariology’s
shared formatting files contain no Catechism source material.

## End-to-end reuse proofs

### Current Vatican sacramental passages

The sacramental pair now proves the source model with a complete, deliberately
narrow replay. Four exact current Holy See English HTML responses were acquired
into run-local restricted storage, hashed, inspected in context, and collated
against the rendered official pages. The repository records their immutable
artifact identities and verified paragraph records without distributing the
responses or excerpts.

Both publications bind the same four passage IDs. The fingerprints below are
properties of the shared source graph and therefore recur unchanged in each
consumer; publication-local role, claim, review date, and context remain in
the two binding records.

| Passage | Shared source fingerprint | Treatise claim | Companion path |
|---|---|---|---|
| 1131 | `sha256:07edd5b79e89a98627ac86e5ade88d61a52d2ae4e65037d12c1e39e8c3b1e322` | The formal definition is a checked editorial synthesis, not a verbatim quotation | Direct import of the treatise-owned master matrix |
| 1240 | `sha256:a5fddc2fa9d2e9ec844e91bd0dd828e2f137ab4f02ea39dbc22302c164c2f35e` | Latin and Eastern baptismal formulas | Direct import of the treatise-owned Baptism summary |
| 1300 | `sha256:0b46767599cbf289aaaf6e5aa2bb322849c052a470506657e5a2bf37588609ed` | Current Latin and Eastern Confirmation formulas | Direct import of the treatise-owned Confirmation summary |
| 1449 | `sha256:1c86747958f4605500efcb17169331c6871f503a59612aac5c0d37fcea7521fa` | Latin absolution conclusion | Direct import of the treatise-owned Penance summary |

The review checked the treatise-owned source files, the companion’s unchanged
direct imports, and the relevant installed render pages in both publications.
No rendered wording changed, so this research-only promotion does not rebuild
or replace either installed PDF.

For every passage, reverse-use lookup returns exactly
`theology/sacraments` and `theology/sacraments-at-a-glance`. Impact lookup from
the controlling artifact reaches its passage and both consumers. A regression
fixture now binds two independent publications to one shared passage, changes
valid shared passage metadata, and proves that validation reports two stale
consumer fingerprints requiring the same replacement value. Impact remains
available to a review workflow that explicitly disables stale-fingerprint
checking, while ordinary validation fails closed.

The same invalidation was then replayed against a run-local mirror of the
actual source graph and both sacramental binding files. Its 11-binding baseline
validated; changing paragraph 1131’s shared metadata produced exactly two
stale diagnostics, one for each real consumer, with the same replacement
fingerprint.

This proof does not substitute the distinct USCCB 2019 expression for the
Vatican web expression. That distinction matters at paragraphs 1300 and 1449,
where wording or punctuation differs. Nor do four verified passages promote
the broad 1076–1209 and 1210–1666 ranges: both consumers retain those range
bindings as `cataloged` until a bounded range-level review is performed.

### Archived Vatican paragraph 970

A second vertical slice acquired and checked the exact archived Vatican
English page containing paragraphs 963–975. The page is a dated 2003 IntraText
expression, not the current Vatican web state and not the USCCB 2019 edition.
Its exact restricted artifact and paragraph 970 now have a shared canonical
identity without distributing the response or a source-text payload.

Seven publications bind the same archived paragraph record and fingerprint,
`sha256:979d13d27cd9ad7570cf774a31d80a1b260ac4156d9d5532864b290c49342364`:

- `theology/mariology/angelus`;
- `theology/mariology/champion`;
- `theology/mariology/fatima`;
- `theology/mariology/lourdes`;
- `theology/mariology/marian-dogmas`;
- `theology/mariology/regina-coeli`; and
- `theology/mariology/rosary`.

Their local contexts distinguish prayer, apparition discernment, dogmatic
synthesis, and Rosary exposition while sharing the same checked control:
Mary's cooperation and influence depend wholly on Christ's unique mediation.
Each broader archived-edition row remains `cataloged`; inspection of paragraph
970 does not promote the surrounding ranges.

Reverse-use lookup returns exactly those seven consumers, and impact lookup
from the controlling artifact reaches paragraph 970 and all seven. A run-local
mirror of the actual graph validated before mutation; changing valid shared
passage metadata then produced exactly seven stale-fingerprint diagnostics
with one common replacement value.

The existing USCCB 2019 paragraph-970 record remains a separate expression.
The Guadalupe and La Salette publications point to modern Vatican web
material, so they do not inherit this archived passage merely because their
legacy loci also include paragraph 970.

## Implemented result

The implemented graph contains 77 Catechism binding rows across 43
publications: the 42 positive trace owners plus the inherited
`theology/sacraments-at-a-glance` consumer. Thirteen rows target the work,
twelve broad rows and seven passage rows target the archived Vatican English
state, and forty-five rows target the current Vatican English web state. Eight
current-web and seven archived-English passage rows are verified reuse
bindings; the other 62 Catechism rows remain catalog-only. One additional
catalog-only binding connects the Saint Thomas Aquinas biography to the 2018
paragraph-2267 rescript, yielding 78 Catechism-family and amendment-act
bindings in total.

No publication binding substitutes the acquired USCCB edition, and neither
novena daily-prayer companion carries a Catechism binding. All 65 rows in the
original migration checkpoint began `cataloged`; the sacramental proof
replaced two of those rows with eight verified passage bindings, while the
archived paragraph-970 proof added seven exact bindings without promoting or
removing the broad legacy rows. The 16 acquired artifacts remain restricted
provenance records without repository
payloads, and the bounded USCCB corpus remains a reacquisition aid rather than
ordinary-clone searchable text.

All legacy source audits, scopes, and rendered references remain in place.
Their removal is deferred until a later comparison proves that the canonical
graph preserves every local role, date, limitation, and discrepancy.
