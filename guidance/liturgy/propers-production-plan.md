# Propers Production Plan

This is a production plan, not a catalog and not a publication commitment. It tracks the complete fixed inventory of proper-guide identities and targets in both Roman Rite propers collections against what each provider has actually published. Identities and formula keys are permanent and may not be reassigned or renumbered. Inclusion of a row here is not a commitment to author, build, review, or publish any particular guide, and confers no editorial, rights, or ecclesiastical clearance.

Authority stays where it already lives. The postconciliar identities, formula keys, slug grammar, canonical order, Lectionary locators, ownership paths, and counts are owned by [the postconciliar proper registry](postconciliar-propers-registry.md); the reusable guide architecture is owned by [the postconciliar proper profile](postconciliar-propers.md). The 1962 series identities, resumed-Sunday mechanism, and `F`/`M` prefixes are owned by [the 1962 proper-guide profile](roman-1962-propers.md). Repository paths are owned by [the repository rules](../repository.md). This plan restates and tracks; it never originates. Where a registry or profile revision lands, this file follows it.

Reader-facing catalogs under `library/` list published works only. This plan is the maintainer view and is deliberately not mirrored there.

## Totals

Status observed on the working tree at the time of writing.

| Collection segment | Permanent identities | Fixed targets | gpt published | claude published | gpt remaining | claude remaining |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Postconciliar Proper of Time (`PC-S`) | 60 | 184 | 9 | 0 | 175 | 184 |
| Postconciliar conditional Scrutiny Ritual Masses | 0 new | 3 | 0 | 0 | 3 | 3 |
| Postconciliar weekday fallbacks | 0 new | 6 | 0 | 0 | 6 | 6 |
| Postconciliar General Calendar replacements (`PC-R`) | 9 | 16 or 22 | 0 | 0 | 16 or 22 | 16 or 22 |
| **Postconciliar total** | **69** | **209 or 215** | **9** | **0** | **200 or 206** | **209 or 215** |
| 1962 temporal Sundays (`01`–`52`) | 52 | 52 | 9 | 0 | 43 | 52 |
| 1962 resumed Epiphany variants (`46R`–`49R`) | 4 | 4 | 0 | 0 | 4 | 4 |
| 1962 Sunday-assigned feasts (`F`) | not enumerated | not enumerated | 0 | 0 | not enumerated | not enumerated |
| 1962 ritual, votive, and other (`M`) | not enumerated | not enumerated | 1 | 0 | not enumerated | not enumerated |
| **1962 fixed total** | **56** | **56** | **9** | **0** | **47** | **56** |

**Remaining across both collections, fixed inventory only: 247 or 253 for `gpt`, 265 or 271 for `claude`.** The pair of figures is the registry's own `PC-R08` fork, not an uncertainty in this plan: 209 assumes the 16-target replacement shape and 215 the 22-target shape. Neither figure counts the open-ended 1962 `F` and `M` series, resolver-generated overlays, or a future `PC-W` weekday collection.

In progress and therefore still counted as remaining: 1 under `claude`. Detail is in the tables below.

### Count reconciliation

Every count in this plan was recomputed from the registry's own per-parent key lists and agrees with the registry's stated totals. No disagreement was found.

- Summing the registry's per-parent counts gives 184 baseline Proper-of-Time targets, 79 for `PC-S01`–`PC-S25` and 105 for `PC-S26`–`PC-S60`, exactly as the registry states.
- Adding the three conditional Scrutiny Ritual Masses gives 187; adding the six weekday fallbacks to the 184 gives 190, and both together give 193. All three match the registry.
- Summing the replacement matrix gives 13 fixed `PC-R` targets plus the `PC-R08` expansion of 3 or 9, so 16 or 22, matching the registry.
- 184 + 3 + 16 = 203 and 184 + 3 + 22 = 209 fixed registry queue; with the six weekday fallbacks, 209 or 215 working inventory. All match the registry.
- Every `PC-S26`–`PC-S57` Lectionary number printed in the registry was independently recomputed with the registry's own formula `64 + 3 × (parent − 26) + cycle offset` and agrees in all 96 cells. The printed numbers are therefore used directly below, not derived.
- The 1962 profile states 52 temporal Sunday identities and four resumed variants. This plan reconstructs the 52-item enumeration, which the profile does not print; the note under that table states exactly which rows are quoted, which are read off existing leaves, and which are derived.

### How status was derived

Status was read from the working tree and `release/public-alpha.json`, never from memory.

- `published` — a leaf directory exists under `src/<provider>/` and its publication id carries `status: release` in `release/public-alpha.json`. Release ids are bare for `gpt` and prefixed `claude:` for `claude`.
- `in progress` — a leaf directory exists under `src/<provider>/` with no `release` record.
- `not started` — no leaf directory exists.

No `claude` proper guide appears in the release manifest; the `claude` publications recorded there are in `articles`, `biographies`, `history`, and `theology`. An `in progress` cell is a snapshot of a live working tree and goes stale as soon as authoring lands.

A `published` cell records only that a reviewed leaf is installed and release-cleared. It does not assert that the target is profile-final. The gpt edition's own `propers/registry/formula-dispositions.md` records the nine evaluated targets as working guides that are not profile-final, and makes no disposition for the other 175.

## Postconciliar collection

Edition-locale is a parameter of the plan, not of the registry. Let `<proper-root>` mean `src/<provider>/liturgy/roman-rite/postconciliar/<edition-locale>/propers`. Instantiated edition-locales: `roman-missal-third-edition-en-us-2011` under `gpt`. Owner paths below are relative to `<proper-root>` and name the non-publishable canonical formulary owner the registry prescribes. Each publishable leaf lives at `<proper-root>/temporal/<full-publication-slug>/` for `PC-S`, including the conditional Scrutiny leaves, and at `<proper-root>/general-calendar/<full-publication-slug>/` for `PC-R`.

### `PC-S` parent index

The 60 permanent Proper-of-Time identities in canonical registry order, with the required slug stem, the canonical formulary owner, the registry's target count, and how many of those targets each provider has published.

| ID | Proper-of-Time identity | Required slug stem | Canonical formulary owner | Targets | gpt | claude |
| --- | --- | --- | --- | ---: | ---: | ---: |
| PC-S01 | First Sunday of Advent | `pc-s01-first-sunday-of-advent` | `temporal/shared/formularies/pc-s01-first-sunday-of-advent/` | 3 | 0/3 | 0/3 |
| PC-S02 | Second Sunday of Advent | `pc-s02-second-sunday-of-advent` | `temporal/shared/formularies/pc-s02-second-sunday-of-advent/` | 3 | 0/3 | 0/3 |
| PC-S03 | Third Sunday of Advent | `pc-s03-third-sunday-of-advent` | `temporal/shared/formularies/pc-s03-third-sunday-of-advent/` | 3 | 0/3 | 0/3 |
| PC-S04 | Fourth Sunday of Advent | `pc-s04-fourth-sunday-of-advent` | `temporal/shared/formularies/pc-s04-fourth-sunday-of-advent/` | 3 | 0/3 | 0/3 |
| PC-S05 | Nativity of the Lord | `pc-s05-nativity-of-the-lord` | `temporal/shared/formularies/pc-s05-nativity-of-the-lord/` | 4 | 0/4 | 0/4 |
| PC-S06 | Holy Family of Jesus, Mary, and Joseph | `pc-s06-holy-family-of-jesus-mary-and-joseph` | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | 3 | 0/3 | 0/3 |
| PC-S07 | Mary, the Holy Mother of God | `pc-s07-mary-holy-mother-of-god` | `temporal/shared/formularies/pc-s07-mary-holy-mother-of-god/` | 1 | 0/1 | 0/1 |
| PC-S08 | Second Sunday after the Nativity | `pc-s08-second-sunday-after-the-nativity` | `temporal/shared/formularies/pc-s08-second-sunday-after-the-nativity/` | 1 | 0/1 | 0/1 |
| PC-S09 | Epiphany of the Lord | `pc-s09-epiphany-of-the-lord` | `temporal/shared/formularies/pc-s09-epiphany-of-the-lord/` | 2 | 0/2 | 0/2 |
| PC-S10 | Baptism of the Lord | `pc-s10-baptism-of-the-lord` | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | 3 | 0/3 | 0/3 |
| PC-S11 | First Sunday of Lent | `pc-s11-first-sunday-of-lent` | `temporal/shared/formularies/pc-s11-first-sunday-of-lent/` | 3 | 0/3 | 0/3 |
| PC-S12 | Second Sunday of Lent | `pc-s12-second-sunday-of-lent` | `temporal/shared/formularies/pc-s12-second-sunday-of-lent/` | 3 | 0/3 | 0/3 |
| PC-S13 | Third Sunday of Lent | `pc-s13-third-sunday-of-lent` | `temporal/shared/formularies/pc-s13-third-sunday-of-lent/` | 3 | 0/3 | 0/3 |
| PC-S14 | Fourth Sunday of Lent | `pc-s14-fourth-sunday-of-lent` | `temporal/shared/formularies/pc-s14-fourth-sunday-of-lent/` | 3 | 0/3 | 0/3 |
| PC-S15 | Fifth Sunday of Lent | `pc-s15-fifth-sunday-of-lent` | `temporal/shared/formularies/pc-s15-fifth-sunday-of-lent/` | 3 | 0/3 | 0/3 |
| PC-S16 | Palm Sunday of the Passion of the Lord | `pc-s16-palm-sunday-of-the-passion-of-the-lord` | `temporal/shared/formularies/pc-s16-palm-sunday-of-the-passion-of-the-lord/` | 3 | 0/3 | 0/3 |
| PC-S17 | Easter Sunday of the Resurrection of the Lord | `pc-s17-easter-sunday-of-the-resurrection-of-the-lord` | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | 6 | 0/6 | 0/6 |
| PC-S18 | Second Sunday of Easter | `pc-s18-second-sunday-of-easter` | `temporal/shared/formularies/pc-s18-second-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S19 | Third Sunday of Easter | `pc-s19-third-sunday-of-easter` | `temporal/shared/formularies/pc-s19-third-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S20 | Fourth Sunday of Easter | `pc-s20-fourth-sunday-of-easter` | `temporal/shared/formularies/pc-s20-fourth-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S21 | Fifth Sunday of Easter | `pc-s21-fifth-sunday-of-easter` | `temporal/shared/formularies/pc-s21-fifth-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S22 | Sixth Sunday of Easter | `pc-s22-sixth-sunday-of-easter` | `temporal/shared/formularies/pc-s22-sixth-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S23 | Ascension of the Lord | `pc-s23-ascension-of-the-lord` | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | 6 | 0/6 | 0/6 |
| PC-S24 | Seventh Sunday of Easter | `pc-s24-seventh-sunday-of-easter` | `temporal/shared/formularies/pc-s24-seventh-sunday-of-easter/` | 3 | 0/3 | 0/3 |
| PC-S25 | Pentecost Sunday | `pc-s25-pentecost-sunday` | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | 5 | 0/5 | 0/5 |
| PC-S26 | Second Sunday in Ordinary Time | `pc-s26-second-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/02/` | 3 | 0/3 | 0/3 |
| PC-S27 | Third Sunday in Ordinary Time | `pc-s27-third-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/03/` | 3 | 0/3 | 0/3 |
| PC-S28 | Fourth Sunday in Ordinary Time | `pc-s28-fourth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/04/` | 3 | 0/3 | 0/3 |
| PC-S29 | Fifth Sunday in Ordinary Time | `pc-s29-fifth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/05/` | 3 | 0/3 | 0/3 |
| PC-S30 | Sixth Sunday in Ordinary Time | `pc-s30-sixth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/06/` | 3 | 0/3 | 0/3 |
| PC-S31 | Seventh Sunday in Ordinary Time | `pc-s31-seventh-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/07/` | 3 | 0/3 | 0/3 |
| PC-S32 | Eighth Sunday in Ordinary Time | `pc-s32-eighth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/08/` | 3 | 0/3 | 0/3 |
| PC-S33 | Ninth Sunday in Ordinary Time | `pc-s33-ninth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/09/` | 3 | 0/3 | 0/3 |
| PC-S34 | Tenth Sunday in Ordinary Time | `pc-s34-tenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/10/` | 3 | 0/3 | 0/3 |
| PC-S35 | Eleventh Sunday in Ordinary Time | `pc-s35-eleventh-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/11/` | 3 | 1/3 | 0/3 |
| PC-S36 | Twelfth Sunday in Ordinary Time | `pc-s36-twelfth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/12/` | 3 | 1/3 | 0/3 |
| PC-S37 | Thirteenth Sunday in Ordinary Time | `pc-s37-thirteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/13/` | 3 | 1/3 | 0/3 |
| PC-S38 | Fourteenth Sunday in Ordinary Time | `pc-s38-fourteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/14/` | 3 | 1/3 | 0/3 |
| PC-S39 | Fifteenth Sunday in Ordinary Time | `pc-s39-fifteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/15/` | 3 | 1/3 | 0/3 |
| PC-S40 | Sixteenth Sunday in Ordinary Time | `pc-s40-sixteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/16/` | 3 | 1/3 | 0/3 |
| PC-S41 | Seventeenth Sunday in Ordinary Time | `pc-s41-seventeenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/17/` | 3 | 1/3 | 0/3 |
| PC-S42 | Eighteenth Sunday in Ordinary Time | `pc-s42-eighteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/18/` | 3 | 0/3 | 0/3 |
| PC-S43 | Nineteenth Sunday in Ordinary Time | `pc-s43-nineteenth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/19/` | 3 | 0/3 | 0/3 |
| PC-S44 | Twentieth Sunday in Ordinary Time | `pc-s44-twentieth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/20/` | 3 | 0/3 | 0/3 |
| PC-S45 | Twenty-first Sunday in Ordinary Time | `pc-s45-twenty-first-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/21/` | 3 | 0/3 | 0/3 |
| PC-S46 | Twenty-second Sunday in Ordinary Time | `pc-s46-twenty-second-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/22/` | 3 | 0/3 | 0/3 |
| PC-S47 | Twenty-third Sunday in Ordinary Time | `pc-s47-twenty-third-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/23/` | 3 | 0/3 | 0/3 |
| PC-S48 | Twenty-fourth Sunday in Ordinary Time | `pc-s48-twenty-fourth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/24/` | 3 | 0/3 | 0/3 |
| PC-S49 | Twenty-fifth Sunday in Ordinary Time | `pc-s49-twenty-fifth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/25/` | 3 | 0/3 | 0/3 |
| PC-S50 | Twenty-sixth Sunday in Ordinary Time | `pc-s50-twenty-sixth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/26/` | 3 | 0/3 | 0/3 |
| PC-S51 | Twenty-seventh Sunday in Ordinary Time | `pc-s51-twenty-seventh-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/27/` | 3 | 0/3 | 0/3 |
| PC-S52 | Twenty-eighth Sunday in Ordinary Time | `pc-s52-twenty-eighth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/28/` | 3 | 0/3 | 0/3 |
| PC-S53 | Twenty-ninth Sunday in Ordinary Time | `pc-s53-twenty-ninth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/29/` | 3 | 0/3 | 0/3 |
| PC-S54 | Thirtieth Sunday in Ordinary Time | `pc-s54-thirtieth-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/30/` | 3 | 0/3 | 0/3 |
| PC-S55 | Thirty-first Sunday in Ordinary Time | `pc-s55-thirty-first-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/31/` | 3 | 0/3 | 0/3 |
| PC-S56 | Thirty-second Sunday in Ordinary Time | `pc-s56-thirty-second-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/32/` | 3 | 0/3 | 0/3 |
| PC-S57 | Thirty-third Sunday in Ordinary Time | `pc-s57-thirty-third-sunday-in-ordinary-time` | `temporal/shared/ordinary-time/weeks/33/` | 3 | 0/3 | 0/3 |
| PC-S58 | Most Holy Trinity | `pc-s58-most-holy-trinity` | `temporal/shared/formularies/pc-s58-most-holy-trinity/` | 3 | 1/3 | 0/3 |
| PC-S59 | Most Holy Body and Blood of Christ | `pc-s59-most-holy-body-and-blood-of-christ` | `temporal/shared/formularies/pc-s59-most-holy-body-and-blood-of-christ/` | 3 | 1/3 | 0/3 |
| PC-S60 | Our Lord Jesus Christ, King of the Universe, the Last Sunday in Ordinary Time | `pc-s60-our-lord-jesus-christ-king-of-the-universe` | `temporal/shared/formularies/pc-s60-our-lord-jesus-christ-king-of-the-universe/` | 3 | 0/3 | 0/3 |

The Ordinary Time owner is computable from the parent: `PC-S26`–`PC-S57` take `weeks/NN` where `NN` is the parent number minus 24, in two digits. `PC-S58`, `PC-S59`, and `PC-S60` are Solemnities of the Lord with their own `shared/formularies/` owners and consume no `weeks/NN`. Weeks `01` and `34` have no numbered Sunday consumer.

Coverage shape is fixed per appointed form: three cycle-specific keys or one directly collated `ABC` key, never both. `PC-S07`, `PC-S08`, and the `PC-S05`, `PC-S09`, and Pentecost Vigil forms carry `ABC`; `PC-S25` places its two `ABC` Vigil forms before its three A/B/C Day forms. There is no `PC-S` identity for a First Sunday in Ordinary Time and none for a Thirty-fourth Sunday.

### `PC-S` baseline formula target queue

The registry's canonical creation queue, 184 rows, in registry order: parent order `PC-S01`–`PC-S60`, then `A`, `B`, `C` or `ABC` within a parent, then appointed forms in the order the Missal prints them. Formula keys are reproduced verbatim. Lectionary numbers are the registry's printed structural locators in the *Ordo Lectionum Missae* sequence.

| # | Parent | Occurrence | Formula key | Cycle | Lect. | Owner under `<proper-root>` | gpt | claude |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PC-S01 | First Sunday of Advent | `PC-S01-A` | A | 1 | `temporal/shared/formularies/pc-s01-first-sunday-of-advent/` | not started | not started |
| 2 | PC-S01 | First Sunday of Advent | `PC-S01-B` | B | 2 | `temporal/shared/formularies/pc-s01-first-sunday-of-advent/` | not started | not started |
| 3 | PC-S01 | First Sunday of Advent | `PC-S01-C` | C | 3 | `temporal/shared/formularies/pc-s01-first-sunday-of-advent/` | not started | not started |
| 4 | PC-S02 | Second Sunday of Advent | `PC-S02-A` | A | 4 | `temporal/shared/formularies/pc-s02-second-sunday-of-advent/` | not started | not started |
| 5 | PC-S02 | Second Sunday of Advent | `PC-S02-B` | B | 5 | `temporal/shared/formularies/pc-s02-second-sunday-of-advent/` | not started | not started |
| 6 | PC-S02 | Second Sunday of Advent | `PC-S02-C` | C | 6 | `temporal/shared/formularies/pc-s02-second-sunday-of-advent/` | not started | not started |
| 7 | PC-S03 | Third Sunday of Advent | `PC-S03-A` | A | 7 | `temporal/shared/formularies/pc-s03-third-sunday-of-advent/` | not started | not started |
| 8 | PC-S03 | Third Sunday of Advent | `PC-S03-B` | B | 8 | `temporal/shared/formularies/pc-s03-third-sunday-of-advent/` | not started | not started |
| 9 | PC-S03 | Third Sunday of Advent | `PC-S03-C` | C | 9 | `temporal/shared/formularies/pc-s03-third-sunday-of-advent/` | not started | not started |
| 10 | PC-S04 | Fourth Sunday of Advent | `PC-S04-A` | A | 10 | `temporal/shared/formularies/pc-s04-fourth-sunday-of-advent/` | not started | not started |
| 11 | PC-S04 | Fourth Sunday of Advent | `PC-S04-B` | B | 11 | `temporal/shared/formularies/pc-s04-fourth-sunday-of-advent/` | not started | not started |
| 12 | PC-S04 | Fourth Sunday of Advent | `PC-S04-C` | C | 12 | `temporal/shared/formularies/pc-s04-fourth-sunday-of-advent/` | not started | not started |
| 13 | PC-S05 | Nativity of the Lord | `PC-S05-ABC-VIGIL` | ABC | 13 | `temporal/shared/formularies/pc-s05-nativity-of-the-lord/` | not started | not started |
| 14 | PC-S05 | Nativity of the Lord | `PC-S05-ABC-NIGHT` | ABC | 14 | `temporal/shared/formularies/pc-s05-nativity-of-the-lord/` | not started | not started |
| 15 | PC-S05 | Nativity of the Lord | `PC-S05-ABC-DAWN` | ABC | 15 | `temporal/shared/formularies/pc-s05-nativity-of-the-lord/` | not started | not started |
| 16 | PC-S05 | Nativity of the Lord | `PC-S05-ABC-DAY` | ABC | 16 | `temporal/shared/formularies/pc-s05-nativity-of-the-lord/` | not started | not started |
| 17 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-A` | A | 17‡ | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 18 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-B` | B | 17‡ | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 19 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-C` | C | 17‡ | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 20 | PC-S07 | Mary, the Holy Mother of God | `PC-S07-ABC` | ABC | 18 | `temporal/shared/formularies/pc-s07-mary-holy-mother-of-god/` | not started | not started |
| 21 | PC-S08 | Second Sunday after the Nativity | `PC-S08-ABC` | ABC | 19 | `temporal/shared/formularies/pc-s08-second-sunday-after-the-nativity/` | not started | not started |
| 22 | PC-S09 | Epiphany of the Lord | `PC-S09-ABC-VIGIL` | ABC | 20‡ | `temporal/shared/formularies/pc-s09-epiphany-of-the-lord/` | not started | not started |
| 23 | PC-S09 | Epiphany of the Lord | `PC-S09-ABC-DAY` | ABC | 20‡ | `temporal/shared/formularies/pc-s09-epiphany-of-the-lord/` | not started | not started |
| 24 | PC-S10 | Baptism of the Lord | `PC-S10-A` | A | 21‡ | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |
| 25 | PC-S10 | Baptism of the Lord | `PC-S10-B` | B | 21‡ | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |
| 26 | PC-S10 | Baptism of the Lord | `PC-S10-C` | C | 21‡ | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |
| 27 | PC-S11 | First Sunday of Lent | `PC-S11-A` | A | 22 | `temporal/shared/formularies/pc-s11-first-sunday-of-lent/` | not started | not started |
| 28 | PC-S11 | First Sunday of Lent | `PC-S11-B` | B | 23 | `temporal/shared/formularies/pc-s11-first-sunday-of-lent/` | not started | not started |
| 29 | PC-S11 | First Sunday of Lent | `PC-S11-C` | C | 24 | `temporal/shared/formularies/pc-s11-first-sunday-of-lent/` | not started | not started |
| 30 | PC-S12 | Second Sunday of Lent | `PC-S12-A` | A | 25 | `temporal/shared/formularies/pc-s12-second-sunday-of-lent/` | not started | not started |
| 31 | PC-S12 | Second Sunday of Lent | `PC-S12-B` | B | 26 | `temporal/shared/formularies/pc-s12-second-sunday-of-lent/` | not started | not started |
| 32 | PC-S12 | Second Sunday of Lent | `PC-S12-C` | C | 27 | `temporal/shared/formularies/pc-s12-second-sunday-of-lent/` | not started | not started |
| 33 | PC-S13 | Third Sunday of Lent | `PC-S13-A` | A | 28 | `temporal/shared/formularies/pc-s13-third-sunday-of-lent/` | not started | not started |
| 34 | PC-S13 | Third Sunday of Lent | `PC-S13-B` | B | 29 | `temporal/shared/formularies/pc-s13-third-sunday-of-lent/` | not started | not started |
| 35 | PC-S13 | Third Sunday of Lent | `PC-S13-C` | C | 30 | `temporal/shared/formularies/pc-s13-third-sunday-of-lent/` | not started | not started |
| 36 | PC-S14 | Fourth Sunday of Lent | `PC-S14-A` | A | 31 | `temporal/shared/formularies/pc-s14-fourth-sunday-of-lent/` | not started | not started |
| 37 | PC-S14 | Fourth Sunday of Lent | `PC-S14-B` | B | 32 | `temporal/shared/formularies/pc-s14-fourth-sunday-of-lent/` | not started | not started |
| 38 | PC-S14 | Fourth Sunday of Lent | `PC-S14-C` | C | 33 | `temporal/shared/formularies/pc-s14-fourth-sunday-of-lent/` | not started | not started |
| 39 | PC-S15 | Fifth Sunday of Lent | `PC-S15-A` | A | 34 | `temporal/shared/formularies/pc-s15-fifth-sunday-of-lent/` | not started | not started |
| 40 | PC-S15 | Fifth Sunday of Lent | `PC-S15-B` | B | 35 | `temporal/shared/formularies/pc-s15-fifth-sunday-of-lent/` | not started | not started |
| 41 | PC-S15 | Fifth Sunday of Lent | `PC-S15-C` | C | 36 | `temporal/shared/formularies/pc-s15-fifth-sunday-of-lent/` | not started | not started |
| 42 | PC-S16 | Palm Sunday of the Passion of the Lord | `PC-S16-A` | A | 37-A/38-A | `temporal/shared/formularies/pc-s16-palm-sunday-of-the-passion-of-the-lord/` | not started | not started |
| 43 | PC-S16 | Palm Sunday of the Passion of the Lord | `PC-S16-B` | B | 37-B/38-B | `temporal/shared/formularies/pc-s16-palm-sunday-of-the-passion-of-the-lord/` | not started | not started |
| 44 | PC-S16 | Palm Sunday of the Passion of the Lord | `PC-S16-C` | C | 37-C/38-C | `temporal/shared/formularies/pc-s16-palm-sunday-of-the-passion-of-the-lord/` | not started | not started |
| 45 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-A-VIGIL` | A | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 46 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-A-DAY` | A | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 47 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-B-VIGIL` | B | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 48 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-B-DAY` | B | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 49 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-C-VIGIL` | C | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 50 | PC-S17 | Easter Sunday of the Resurrection of the Lord | `PC-S17-C-DAY` | C | 41, 42† | `temporal/shared/formularies/pc-s17-easter-sunday-of-the-resurrection-of-the-lord/` | not started | not started |
| 51 | PC-S18 | Second Sunday of Easter | `PC-S18-A` | A | 43 | `temporal/shared/formularies/pc-s18-second-sunday-of-easter/` | not started | not started |
| 52 | PC-S18 | Second Sunday of Easter | `PC-S18-B` | B | 44 | `temporal/shared/formularies/pc-s18-second-sunday-of-easter/` | not started | not started |
| 53 | PC-S18 | Second Sunday of Easter | `PC-S18-C` | C | 45 | `temporal/shared/formularies/pc-s18-second-sunday-of-easter/` | not started | not started |
| 54 | PC-S19 | Third Sunday of Easter | `PC-S19-A` | A | 46 | `temporal/shared/formularies/pc-s19-third-sunday-of-easter/` | not started | not started |
| 55 | PC-S19 | Third Sunday of Easter | `PC-S19-B` | B | 47 | `temporal/shared/formularies/pc-s19-third-sunday-of-easter/` | not started | not started |
| 56 | PC-S19 | Third Sunday of Easter | `PC-S19-C` | C | 48 | `temporal/shared/formularies/pc-s19-third-sunday-of-easter/` | not started | not started |
| 57 | PC-S20 | Fourth Sunday of Easter | `PC-S20-A` | A | 49 | `temporal/shared/formularies/pc-s20-fourth-sunday-of-easter/` | not started | not started |
| 58 | PC-S20 | Fourth Sunday of Easter | `PC-S20-B` | B | 50 | `temporal/shared/formularies/pc-s20-fourth-sunday-of-easter/` | not started | not started |
| 59 | PC-S20 | Fourth Sunday of Easter | `PC-S20-C` | C | 51 | `temporal/shared/formularies/pc-s20-fourth-sunday-of-easter/` | not started | not started |
| 60 | PC-S21 | Fifth Sunday of Easter | `PC-S21-A` | A | 52 | `temporal/shared/formularies/pc-s21-fifth-sunday-of-easter/` | not started | not started |
| 61 | PC-S21 | Fifth Sunday of Easter | `PC-S21-B` | B | 53 | `temporal/shared/formularies/pc-s21-fifth-sunday-of-easter/` | not started | not started |
| 62 | PC-S21 | Fifth Sunday of Easter | `PC-S21-C` | C | 54 | `temporal/shared/formularies/pc-s21-fifth-sunday-of-easter/` | not started | not started |
| 63 | PC-S22 | Sixth Sunday of Easter | `PC-S22-A` | A | 55 | `temporal/shared/formularies/pc-s22-sixth-sunday-of-easter/` | not started | not started |
| 64 | PC-S22 | Sixth Sunday of Easter | `PC-S22-B` | B | 56 | `temporal/shared/formularies/pc-s22-sixth-sunday-of-easter/` | not started | not started |
| 65 | PC-S22 | Sixth Sunday of Easter | `PC-S22-C` | C | 57 | `temporal/shared/formularies/pc-s22-sixth-sunday-of-easter/` | not started | not started |
| 66 | PC-S23 | Ascension of the Lord | `PC-S23-A-VIGIL` | A | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 67 | PC-S23 | Ascension of the Lord | `PC-S23-A-DAY` | A | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 68 | PC-S23 | Ascension of the Lord | `PC-S23-B-VIGIL` | B | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 69 | PC-S23 | Ascension of the Lord | `PC-S23-B-DAY` | B | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 70 | PC-S23 | Ascension of the Lord | `PC-S23-C-VIGIL` | C | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 71 | PC-S23 | Ascension of the Lord | `PC-S23-C-DAY` | C | 58‡ | `temporal/shared/formularies/pc-s23-ascension-of-the-lord/` | not started | not started |
| 72 | PC-S24 | Seventh Sunday of Easter | `PC-S24-A` | A | 59 | `temporal/shared/formularies/pc-s24-seventh-sunday-of-easter/` | not started | not started |
| 73 | PC-S24 | Seventh Sunday of Easter | `PC-S24-B` | B | 60 | `temporal/shared/formularies/pc-s24-seventh-sunday-of-easter/` | not started | not started |
| 74 | PC-S24 | Seventh Sunday of Easter | `PC-S24-C` | C | 61 | `temporal/shared/formularies/pc-s24-seventh-sunday-of-easter/` | not started | not started |
| 75 | PC-S25 | Pentecost Sunday | `PC-S25-ABC-VIGIL` | ABC | 62, 62a, 63† | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | not started | not started |
| 76 | PC-S25 | Pentecost Sunday | `PC-S25-ABC-EXTENDED-VIGIL` | ABC | 62, 62a, 63† | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | not started | not started |
| 77 | PC-S25 | Pentecost Sunday | `PC-S25-A-DAY` | A | 62, 62a, 63† | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | not started | not started |
| 78 | PC-S25 | Pentecost Sunday | `PC-S25-B-DAY` | B | 62, 62a, 63† | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | not started | not started |
| 79 | PC-S25 | Pentecost Sunday | `PC-S25-C-DAY` | C | 62, 62a, 63† | `temporal/shared/formularies/pc-s25-pentecost-sunday/` | not started | not started |
| 80 | PC-S26 | Second Sunday in Ordinary Time | `PC-S26-A` | A | 64 | `temporal/shared/ordinary-time/weeks/02/` | not started | not started |
| 81 | PC-S26 | Second Sunday in Ordinary Time | `PC-S26-B` | B | 65 | `temporal/shared/ordinary-time/weeks/02/` | not started | not started |
| 82 | PC-S26 | Second Sunday in Ordinary Time | `PC-S26-C` | C | 66 | `temporal/shared/ordinary-time/weeks/02/` | not started | not started |
| 83 | PC-S27 | Third Sunday in Ordinary Time | `PC-S27-A` | A | 67 | `temporal/shared/ordinary-time/weeks/03/` | not started | not started |
| 84 | PC-S27 | Third Sunday in Ordinary Time | `PC-S27-B` | B | 68 | `temporal/shared/ordinary-time/weeks/03/` | not started | not started |
| 85 | PC-S27 | Third Sunday in Ordinary Time | `PC-S27-C` | C | 69 | `temporal/shared/ordinary-time/weeks/03/` | not started | not started |
| 86 | PC-S28 | Fourth Sunday in Ordinary Time | `PC-S28-A` | A | 70 | `temporal/shared/ordinary-time/weeks/04/` | not started | not started |
| 87 | PC-S28 | Fourth Sunday in Ordinary Time | `PC-S28-B` | B | 71 | `temporal/shared/ordinary-time/weeks/04/` | not started | not started |
| 88 | PC-S28 | Fourth Sunday in Ordinary Time | `PC-S28-C` | C | 72 | `temporal/shared/ordinary-time/weeks/04/` | not started | not started |
| 89 | PC-S29 | Fifth Sunday in Ordinary Time | `PC-S29-A` | A | 73 | `temporal/shared/ordinary-time/weeks/05/` | not started | not started |
| 90 | PC-S29 | Fifth Sunday in Ordinary Time | `PC-S29-B` | B | 74 | `temporal/shared/ordinary-time/weeks/05/` | not started | not started |
| 91 | PC-S29 | Fifth Sunday in Ordinary Time | `PC-S29-C` | C | 75 | `temporal/shared/ordinary-time/weeks/05/` | not started | not started |
| 92 | PC-S30 | Sixth Sunday in Ordinary Time | `PC-S30-A` | A | 76 | `temporal/shared/ordinary-time/weeks/06/` | not started | not started |
| 93 | PC-S30 | Sixth Sunday in Ordinary Time | `PC-S30-B` | B | 77 | `temporal/shared/ordinary-time/weeks/06/` | not started | not started |
| 94 | PC-S30 | Sixth Sunday in Ordinary Time | `PC-S30-C` | C | 78 | `temporal/shared/ordinary-time/weeks/06/` | not started | not started |
| 95 | PC-S31 | Seventh Sunday in Ordinary Time | `PC-S31-A` | A | 79 | `temporal/shared/ordinary-time/weeks/07/` | not started | not started |
| 96 | PC-S31 | Seventh Sunday in Ordinary Time | `PC-S31-B` | B | 80 | `temporal/shared/ordinary-time/weeks/07/` | not started | not started |
| 97 | PC-S31 | Seventh Sunday in Ordinary Time | `PC-S31-C` | C | 81 | `temporal/shared/ordinary-time/weeks/07/` | not started | not started |
| 98 | PC-S32 | Eighth Sunday in Ordinary Time | `PC-S32-A` | A | 82 | `temporal/shared/ordinary-time/weeks/08/` | not started | not started |
| 99 | PC-S32 | Eighth Sunday in Ordinary Time | `PC-S32-B` | B | 83 | `temporal/shared/ordinary-time/weeks/08/` | not started | not started |
| 100 | PC-S32 | Eighth Sunday in Ordinary Time | `PC-S32-C` | C | 84 | `temporal/shared/ordinary-time/weeks/08/` | not started | not started |
| 101 | PC-S33 | Ninth Sunday in Ordinary Time | `PC-S33-A` | A | 85 | `temporal/shared/ordinary-time/weeks/09/` | not started | not started |
| 102 | PC-S33 | Ninth Sunday in Ordinary Time | `PC-S33-B` | B | 86 | `temporal/shared/ordinary-time/weeks/09/` | not started | not started |
| 103 | PC-S33 | Ninth Sunday in Ordinary Time | `PC-S33-C` | C | 87 | `temporal/shared/ordinary-time/weeks/09/` | not started | not started |
| 104 | PC-S34 | Tenth Sunday in Ordinary Time | `PC-S34-A` | A | 88 | `temporal/shared/ordinary-time/weeks/10/` | not started | not started |
| 105 | PC-S34 | Tenth Sunday in Ordinary Time | `PC-S34-B` | B | 89 | `temporal/shared/ordinary-time/weeks/10/` | not started | not started |
| 106 | PC-S34 | Tenth Sunday in Ordinary Time | `PC-S34-C` | C | 90 | `temporal/shared/ordinary-time/weeks/10/` | not started | not started |
| 107 | PC-S35 | Eleventh Sunday in Ordinary Time | `PC-S35-A` | A | 91 | `temporal/shared/ordinary-time/weeks/11/` | published | not started |
| 108 | PC-S35 | Eleventh Sunday in Ordinary Time | `PC-S35-B` | B | 92 | `temporal/shared/ordinary-time/weeks/11/` | not started | not started |
| 109 | PC-S35 | Eleventh Sunday in Ordinary Time | `PC-S35-C` | C | 93 | `temporal/shared/ordinary-time/weeks/11/` | not started | not started |
| 110 | PC-S36 | Twelfth Sunday in Ordinary Time | `PC-S36-A` | A | 94 | `temporal/shared/ordinary-time/weeks/12/` | published | not started |
| 111 | PC-S36 | Twelfth Sunday in Ordinary Time | `PC-S36-B` | B | 95 | `temporal/shared/ordinary-time/weeks/12/` | not started | not started |
| 112 | PC-S36 | Twelfth Sunday in Ordinary Time | `PC-S36-C` | C | 96 | `temporal/shared/ordinary-time/weeks/12/` | not started | not started |
| 113 | PC-S37 | Thirteenth Sunday in Ordinary Time | `PC-S37-A` | A | 97 | `temporal/shared/ordinary-time/weeks/13/` | published | not started |
| 114 | PC-S37 | Thirteenth Sunday in Ordinary Time | `PC-S37-B` | B | 98 | `temporal/shared/ordinary-time/weeks/13/` | not started | not started |
| 115 | PC-S37 | Thirteenth Sunday in Ordinary Time | `PC-S37-C` | C | 99 | `temporal/shared/ordinary-time/weeks/13/` | not started | not started |
| 116 | PC-S38 | Fourteenth Sunday in Ordinary Time | `PC-S38-A` | A | 100 | `temporal/shared/ordinary-time/weeks/14/` | published | not started |
| 117 | PC-S38 | Fourteenth Sunday in Ordinary Time | `PC-S38-B` | B | 101 | `temporal/shared/ordinary-time/weeks/14/` | not started | not started |
| 118 | PC-S38 | Fourteenth Sunday in Ordinary Time | `PC-S38-C` | C | 102 | `temporal/shared/ordinary-time/weeks/14/` | not started | not started |
| 119 | PC-S39 | Fifteenth Sunday in Ordinary Time | `PC-S39-A` | A | 103 | `temporal/shared/ordinary-time/weeks/15/` | published | not started |
| 120 | PC-S39 | Fifteenth Sunday in Ordinary Time | `PC-S39-B` | B | 104 | `temporal/shared/ordinary-time/weeks/15/` | not started | not started |
| 121 | PC-S39 | Fifteenth Sunday in Ordinary Time | `PC-S39-C` | C | 105 | `temporal/shared/ordinary-time/weeks/15/` | not started | not started |
| 122 | PC-S40 | Sixteenth Sunday in Ordinary Time | `PC-S40-A` | A | 106 | `temporal/shared/ordinary-time/weeks/16/` | published | not started |
| 123 | PC-S40 | Sixteenth Sunday in Ordinary Time | `PC-S40-B` | B | 107 | `temporal/shared/ordinary-time/weeks/16/` | not started | not started |
| 124 | PC-S40 | Sixteenth Sunday in Ordinary Time | `PC-S40-C` | C | 108 | `temporal/shared/ordinary-time/weeks/16/` | not started | not started |
| 125 | PC-S41 | Seventeenth Sunday in Ordinary Time | `PC-S41-A` | A | 109 | `temporal/shared/ordinary-time/weeks/17/` | published | not started |
| 126 | PC-S41 | Seventeenth Sunday in Ordinary Time | `PC-S41-B` | B | 110 | `temporal/shared/ordinary-time/weeks/17/` | not started | not started |
| 127 | PC-S41 | Seventeenth Sunday in Ordinary Time | `PC-S41-C` | C | 111 | `temporal/shared/ordinary-time/weeks/17/` | not started | not started |
| 128 | PC-S42 | Eighteenth Sunday in Ordinary Time | `PC-S42-A` | A | 112 | `temporal/shared/ordinary-time/weeks/18/` | not started | not started |
| 129 | PC-S42 | Eighteenth Sunday in Ordinary Time | `PC-S42-B` | B | 113 | `temporal/shared/ordinary-time/weeks/18/` | not started | not started |
| 130 | PC-S42 | Eighteenth Sunday in Ordinary Time | `PC-S42-C` | C | 114 | `temporal/shared/ordinary-time/weeks/18/` | not started | not started |
| 131 | PC-S43 | Nineteenth Sunday in Ordinary Time | `PC-S43-A` | A | 115 | `temporal/shared/ordinary-time/weeks/19/` | not started | not started |
| 132 | PC-S43 | Nineteenth Sunday in Ordinary Time | `PC-S43-B` | B | 116 | `temporal/shared/ordinary-time/weeks/19/` | not started | not started |
| 133 | PC-S43 | Nineteenth Sunday in Ordinary Time | `PC-S43-C` | C | 117 | `temporal/shared/ordinary-time/weeks/19/` | not started | not started |
| 134 | PC-S44 | Twentieth Sunday in Ordinary Time | `PC-S44-A` | A | 118 | `temporal/shared/ordinary-time/weeks/20/` | not started | not started |
| 135 | PC-S44 | Twentieth Sunday in Ordinary Time | `PC-S44-B` | B | 119 | `temporal/shared/ordinary-time/weeks/20/` | not started | not started |
| 136 | PC-S44 | Twentieth Sunday in Ordinary Time | `PC-S44-C` | C | 120 | `temporal/shared/ordinary-time/weeks/20/` | not started | not started |
| 137 | PC-S45 | Twenty-first Sunday in Ordinary Time | `PC-S45-A` | A | 121 | `temporal/shared/ordinary-time/weeks/21/` | not started | not started |
| 138 | PC-S45 | Twenty-first Sunday in Ordinary Time | `PC-S45-B` | B | 122 | `temporal/shared/ordinary-time/weeks/21/` | not started | not started |
| 139 | PC-S45 | Twenty-first Sunday in Ordinary Time | `PC-S45-C` | C | 123 | `temporal/shared/ordinary-time/weeks/21/` | not started | not started |
| 140 | PC-S46 | Twenty-second Sunday in Ordinary Time | `PC-S46-A` | A | 124 | `temporal/shared/ordinary-time/weeks/22/` | not started | not started |
| 141 | PC-S46 | Twenty-second Sunday in Ordinary Time | `PC-S46-B` | B | 125 | `temporal/shared/ordinary-time/weeks/22/` | not started | not started |
| 142 | PC-S46 | Twenty-second Sunday in Ordinary Time | `PC-S46-C` | C | 126 | `temporal/shared/ordinary-time/weeks/22/` | not started | not started |
| 143 | PC-S47 | Twenty-third Sunday in Ordinary Time | `PC-S47-A` | A | 127 | `temporal/shared/ordinary-time/weeks/23/` | not started | not started |
| 144 | PC-S47 | Twenty-third Sunday in Ordinary Time | `PC-S47-B` | B | 128 | `temporal/shared/ordinary-time/weeks/23/` | not started | not started |
| 145 | PC-S47 | Twenty-third Sunday in Ordinary Time | `PC-S47-C` | C | 129 | `temporal/shared/ordinary-time/weeks/23/` | not started | not started |
| 146 | PC-S48 | Twenty-fourth Sunday in Ordinary Time | `PC-S48-A` | A | 130 | `temporal/shared/ordinary-time/weeks/24/` | not started | not started |
| 147 | PC-S48 | Twenty-fourth Sunday in Ordinary Time | `PC-S48-B` | B | 131 | `temporal/shared/ordinary-time/weeks/24/` | not started | not started |
| 148 | PC-S48 | Twenty-fourth Sunday in Ordinary Time | `PC-S48-C` | C | 132 | `temporal/shared/ordinary-time/weeks/24/` | not started | not started |
| 149 | PC-S49 | Twenty-fifth Sunday in Ordinary Time | `PC-S49-A` | A | 133 | `temporal/shared/ordinary-time/weeks/25/` | not started | not started |
| 150 | PC-S49 | Twenty-fifth Sunday in Ordinary Time | `PC-S49-B` | B | 134 | `temporal/shared/ordinary-time/weeks/25/` | not started | not started |
| 151 | PC-S49 | Twenty-fifth Sunday in Ordinary Time | `PC-S49-C` | C | 135 | `temporal/shared/ordinary-time/weeks/25/` | not started | not started |
| 152 | PC-S50 | Twenty-sixth Sunday in Ordinary Time | `PC-S50-A` | A | 136 | `temporal/shared/ordinary-time/weeks/26/` | not started | not started |
| 153 | PC-S50 | Twenty-sixth Sunday in Ordinary Time | `PC-S50-B` | B | 137 | `temporal/shared/ordinary-time/weeks/26/` | not started | not started |
| 154 | PC-S50 | Twenty-sixth Sunday in Ordinary Time | `PC-S50-C` | C | 138 | `temporal/shared/ordinary-time/weeks/26/` | not started | not started |
| 155 | PC-S51 | Twenty-seventh Sunday in Ordinary Time | `PC-S51-A` | A | 139 | `temporal/shared/ordinary-time/weeks/27/` | not started | not started |
| 156 | PC-S51 | Twenty-seventh Sunday in Ordinary Time | `PC-S51-B` | B | 140 | `temporal/shared/ordinary-time/weeks/27/` | not started | not started |
| 157 | PC-S51 | Twenty-seventh Sunday in Ordinary Time | `PC-S51-C` | C | 141 | `temporal/shared/ordinary-time/weeks/27/` | not started | not started |
| 158 | PC-S52 | Twenty-eighth Sunday in Ordinary Time | `PC-S52-A` | A | 142 | `temporal/shared/ordinary-time/weeks/28/` | not started | not started |
| 159 | PC-S52 | Twenty-eighth Sunday in Ordinary Time | `PC-S52-B` | B | 143 | `temporal/shared/ordinary-time/weeks/28/` | not started | not started |
| 160 | PC-S52 | Twenty-eighth Sunday in Ordinary Time | `PC-S52-C` | C | 144 | `temporal/shared/ordinary-time/weeks/28/` | not started | not started |
| 161 | PC-S53 | Twenty-ninth Sunday in Ordinary Time | `PC-S53-A` | A | 145 | `temporal/shared/ordinary-time/weeks/29/` | not started | not started |
| 162 | PC-S53 | Twenty-ninth Sunday in Ordinary Time | `PC-S53-B` | B | 146 | `temporal/shared/ordinary-time/weeks/29/` | not started | not started |
| 163 | PC-S53 | Twenty-ninth Sunday in Ordinary Time | `PC-S53-C` | C | 147 | `temporal/shared/ordinary-time/weeks/29/` | not started | not started |
| 164 | PC-S54 | Thirtieth Sunday in Ordinary Time | `PC-S54-A` | A | 148 | `temporal/shared/ordinary-time/weeks/30/` | not started | not started |
| 165 | PC-S54 | Thirtieth Sunday in Ordinary Time | `PC-S54-B` | B | 149 | `temporal/shared/ordinary-time/weeks/30/` | not started | not started |
| 166 | PC-S54 | Thirtieth Sunday in Ordinary Time | `PC-S54-C` | C | 150 | `temporal/shared/ordinary-time/weeks/30/` | not started | not started |
| 167 | PC-S55 | Thirty-first Sunday in Ordinary Time | `PC-S55-A` | A | 151 | `temporal/shared/ordinary-time/weeks/31/` | not started | not started |
| 168 | PC-S55 | Thirty-first Sunday in Ordinary Time | `PC-S55-B` | B | 152 | `temporal/shared/ordinary-time/weeks/31/` | not started | not started |
| 169 | PC-S55 | Thirty-first Sunday in Ordinary Time | `PC-S55-C` | C | 153 | `temporal/shared/ordinary-time/weeks/31/` | not started | not started |
| 170 | PC-S56 | Thirty-second Sunday in Ordinary Time | `PC-S56-A` | A | 154 | `temporal/shared/ordinary-time/weeks/32/` | not started | not started |
| 171 | PC-S56 | Thirty-second Sunday in Ordinary Time | `PC-S56-B` | B | 155 | `temporal/shared/ordinary-time/weeks/32/` | not started | not started |
| 172 | PC-S56 | Thirty-second Sunday in Ordinary Time | `PC-S56-C` | C | 156 | `temporal/shared/ordinary-time/weeks/32/` | not started | not started |
| 173 | PC-S57 | Thirty-third Sunday in Ordinary Time | `PC-S57-A` | A | 157 | `temporal/shared/ordinary-time/weeks/33/` | not started | not started |
| 174 | PC-S57 | Thirty-third Sunday in Ordinary Time | `PC-S57-B` | B | 158 | `temporal/shared/ordinary-time/weeks/33/` | not started | not started |
| 175 | PC-S57 | Thirty-third Sunday in Ordinary Time | `PC-S57-C` | C | 159 | `temporal/shared/ordinary-time/weeks/33/` | not started | not started |
| 176 | PC-S58 | Most Holy Trinity | `PC-S58-A` | A | 164 | `temporal/shared/formularies/pc-s58-most-holy-trinity/` | published | not started |
| 177 | PC-S58 | Most Holy Trinity | `PC-S58-B` | B | 165 | `temporal/shared/formularies/pc-s58-most-holy-trinity/` | not started | not started |
| 178 | PC-S58 | Most Holy Trinity | `PC-S58-C` | C | 166 | `temporal/shared/formularies/pc-s58-most-holy-trinity/` | not started | not started |
| 179 | PC-S59 | Most Holy Body and Blood of Christ | `PC-S59-A` | A | 167 | `temporal/shared/formularies/pc-s59-most-holy-body-and-blood-of-christ/` | published | not started |
| 180 | PC-S59 | Most Holy Body and Blood of Christ | `PC-S59-B` | B | 168 | `temporal/shared/formularies/pc-s59-most-holy-body-and-blood-of-christ/` | not started | not started |
| 181 | PC-S59 | Most Holy Body and Blood of Christ | `PC-S59-C` | C | 169 | `temporal/shared/formularies/pc-s59-most-holy-body-and-blood-of-christ/` | not started | not started |
| 182 | PC-S60 | Our Lord Jesus Christ, King of the Universe, the Last Sunday in Ordinary Time | `PC-S60-A` | A | 160 | `temporal/shared/formularies/pc-s60-our-lord-jesus-christ-king-of-the-universe/` | not started | not started |
| 183 | PC-S60 | Our Lord Jesus Christ, King of the Universe, the Last Sunday in Ordinary Time | `PC-S60-B` | B | 161 | `temporal/shared/formularies/pc-s60-our-lord-jesus-christ-king-of-the-universe/` | not started | not started |
| 184 | PC-S60 | Our Lord Jesus Christ, King of the Universe, the Last Sunday in Ordinary Time | `PC-S60-C` | C | 162 | `temporal/shared/formularies/pc-s60-our-lord-jesus-christ-king-of-the-universe/` | not started | not started |

‡ The registry prints one Lectionary number for the parent's whole key group and does not assign a distinct number per key; the number is repeated here rather than split.

† The registry prints a number set for the parent without stating a per-key assignment. `PC-S17` carries `41, 42` across six keys and `PC-S25` carries `62, 62a, 63` across five. The set is repeated on each row; do not infer a per-key locator from it.

`PC-S16` carries paired locators because Palm Sunday's procession Gospel and Mass readings are separately numbered per cycle.

### Conditional Scrutiny Ritual Masses

Three conditional formula targets that substitute distinct Ritual Mass formularies. They raise the Proper-of-Time-linked Sunday queue from 184 to 187, apply only when the corresponding Scrutiny is celebrated and the governing books admit the Ritual Mass, and do not become duplicate temporal-formulary owners. Their leaves remain in the temporal Sunday queue and import the ritual owner.

| Parent | Occurrence | Formula key | Required slug suffix | Cycle | Lect. | Owner under `<proper-root>` | gpt | claude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PC-S13 | Third Sunday of Lent | `PC-S13-ABC-FIRST-SCRUTINY` | `-abc-first-scrutiny` | ABC | 28 (derived) | `ritual/shared/formularies/celebration-of-the-scrutinies/` | not started | not started |
| PC-S14 | Fourth Sunday of Lent | `PC-S14-ABC-SECOND-SCRUTINY` | `-abc-second-scrutiny` | ABC | 31 (derived) | `ritual/shared/formularies/celebration-of-the-scrutinies/` | not started | not started |
| PC-S15 | Fifth Sunday of Lent | `PC-S15-ABC-THIRD-SCRUTINY` | `-abc-third-scrutiny` | ABC | 34 (derived) | `ritual/shared/formularies/celebration-of-the-scrutinies/` | not started | not started |

The registry prints no Lectionary number for these three keys. It does state that they use the Year A initiation readings in every actual cycle, so the numbers above are derived by taking each parent's Year A locator from the baseline queue. Treat them as derived, and collate the selected edition before relying on them.

### Weekday fallback targets

Only two parents require prebuilt weekday fallbacks, because the fallback changes the Liturgy of the Word. These six keys follow the Sunday registry but do not count as Sunday formulas; with the 184 they make the temporal production queue 190, or 193 with the three Scrutiny keys.

| Order | Parent | Occurrence | Formula key | Required slug suffix | Cycle | Lect. | Owner under `<proper-root>` | gpt | claude |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-A-O-DECEMBER-30` | `-year-a-december-30` | A | — | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 2 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-B-O-DECEMBER-30` | `-year-b-december-30` | B | — | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 3 | PC-S06 | Holy Family of Jesus, Mary, and Joseph | `PC-S06-C-O-DECEMBER-30` | `-year-c-december-30` | C | — | `temporal/shared/formularies/pc-s06-holy-family-of-jesus-mary-and-joseph/` | not started | not started |
| 4 | PC-S10 | Baptism of the Lord | `PC-S10-A-O-MONDAY` | `-year-a-monday` | A | — | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |
| 5 | PC-S10 | Baptism of the Lord | `PC-S10-B-O-MONDAY` | `-year-b-monday` | B | — | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |
| 6 | PC-S10 | Baptism of the Lord | `PC-S10-C-O-MONDAY` | `-year-c-monday` | C | — | `temporal/shared/formularies/pc-s10-baptism-of-the-lord/` | not started | not started |

Each uses one reading before the Gospel. The registry prints no separate Lectionary number for a fallback; the parent's own locator governs, and the actual appointed arrangement must be collated in the selected edition. Nativity on a weekday, Mary on January 1, Epiphany on January 6, Ascension on Thursday, and Corpus Christi on Thursday reuse their existing targets. Pentecost on Monday or Tuesday is a conditional reuse edge, not a target.

### `PC-R` General Calendar replacements

Nine permanent replacement identities for universal fixed-date General Calendar celebrations that are not owned by `PC-S` and can replace a Sunday in Christmas Time or Ordinary Time. They have their own source ownership, do not enter or renumber the `PC-S` sequence, and use the `general-calendar` paths. The registry's as-of date for exhaustiveness is 15 July 2026.

| ID | Date | General Calendar celebration | Required slug stem | Canonical formulary owner | Targets | gpt | claude |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| PC-R01 | February 2 | Presentation of the Lord | `pc-r01-presentation-of-the-lord` | `general-calendar/shared/formularies/pc-r01-presentation-of-the-lord/` | 1 | 0/1 | 0/1 |
| PC-R02 | June 24 | Nativity of Saint John the Baptist | `pc-r02-nativity-of-saint-john-the-baptist` | `general-calendar/shared/formularies/pc-r02-nativity-of-saint-john-the-baptist/` | 2 | 0/2 | 0/2 |
| PC-R03 | June 29 | Saints Peter and Paul, Apostles | `pc-r03-saints-peter-and-paul-apostles` | `general-calendar/shared/formularies/pc-r03-saints-peter-and-paul-apostles/` | 2 | 0/2 | 0/2 |
| PC-R04 | August 6 | Transfiguration of the Lord | `pc-r04-transfiguration-of-the-lord` | `general-calendar/shared/formularies/pc-r04-transfiguration-of-the-lord/` | 3 | 0/3 | 0/3 |
| PC-R05 | August 15 | Assumption of the Blessed Virgin Mary | `pc-r05-assumption-of-the-blessed-virgin-mary` | `general-calendar/shared/formularies/pc-r05-assumption-of-the-blessed-virgin-mary/` | 2 | 0/2 | 0/2 |
| PC-R06 | September 14 | Exaltation of the Holy Cross | `pc-r06-exaltation-of-the-holy-cross` | `general-calendar/shared/formularies/pc-r06-exaltation-of-the-holy-cross/` | 1 | 0/1 | 0/1 |
| PC-R07 | November 1 | All Saints | `pc-r07-all-saints` | `general-calendar/shared/formularies/pc-r07-all-saints/` | 1 | 0/1 | 0/1 |
| PC-R08 | November 2 | Commemoration of All the Faithful Departed | `pc-r08-commemoration-of-all-the-faithful-departed` | `general-calendar/shared/formularies/pc-r08-commemoration-of-all-the-faithful-departed/` | 3 or 9 | 0/3 or 9 | 0/3 or 9 |
| PC-R09 | November 9 | Dedication of the Lateran Basilica | `pc-r09-dedication-of-the-lateran-basilica` | `general-calendar/shared/formularies/pc-r09-dedication-of-the-lateran-basilica/` | 1 | 0/1 | 0/1 |

Replacement formula keys, in registry order:

| # | ID | Occurrence | Formula key | Cycle | Lect. | gpt | claude |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | PC-R01 | Presentation of the Lord | `PC-R01-ABC-O-SUNDAY` | ABC | — | not started | not started |
| 2 | PC-R02 | Nativity of Saint John the Baptist | `PC-R02-ABC-VIGIL` | ABC | — | not started | not started |
| 3 | PC-R02 | Nativity of Saint John the Baptist | `PC-R02-ABC-DAY` | ABC | — | not started | not started |
| 4 | PC-R03 | Saints Peter and Paul, Apostles | `PC-R03-ABC-VIGIL` | ABC | — | not started | not started |
| 5 | PC-R03 | Saints Peter and Paul, Apostles | `PC-R03-ABC-DAY` | ABC | — | not started | not started |
| 6 | PC-R04 | Transfiguration of the Lord | `PC-R04-A-O-SUNDAY` | A | — | not started | not started |
| 7 | PC-R04 | Transfiguration of the Lord | `PC-R04-B-O-SUNDAY` | B | — | not started | not started |
| 8 | PC-R04 | Transfiguration of the Lord | `PC-R04-C-O-SUNDAY` | C | — | not started | not started |
| 9 | PC-R05 | Assumption of the Blessed Virgin Mary | `PC-R05-ABC-VIGIL` | ABC | — | not started | not started |
| 10 | PC-R05 | Assumption of the Blessed Virgin Mary | `PC-R05-ABC-DAY` | ABC | — | not started | not started |
| 11 | PC-R06 | Exaltation of the Holy Cross | `PC-R06-ABC-O-SUNDAY` | ABC | — | not started | not started |
| 12 | PC-R07 | All Saints | `PC-R07-ABC` | ABC | — | not started | not started |
| 13 | PC-R09 | Dedication of the Lateran Basilica | `PC-R09-ABC-O-SUNDAY` | ABC | — | not started | not started |

`PC-R08` is an edition-resolved fork; select exactly one expansion after collating the approved Lectionary, and never both.

| Expansion | Condition | Formula keys | Count |
| --- | --- | --- | ---: |
| Invariant | the complete reading inventory is invariant across the Sunday cycles | `PC-R08-ABC-FORMULARY-1`, `PC-R08-ABC-FORMULARY-2`, `PC-R08-ABC-FORMULARY-3` | 3 |
| Cycle-distinguished | the edition appoints A/B/C sets | `PC-R08-A-FORMULARY-1` … `PC-R08-C-FORMULARY-3`, nine keys in registry order | 9 |

Neither expansion is selected for either provider, and no `PC-R08` leaf exists. The gpt edition-locale record is explicitly **unresolved and fail-closed** on `PC-R08`: the U.S. All Souls reading structure has not been collated against a complete identified approved U.S. Lectionary edition, so that edition claims neither the 16-target nor the 22-target replacement shape. Until that resolves, gpt's own replacement queue length is undetermined and the 16-or-22 fork above stands open for both providers.

The mandatory `-O-SUNDAY` component on `PC-R01`, `PC-R04`, `PC-R06`, and `PC-R09` records that these Feasts use both pre-Gospel readings when they replace a Sunday but only one on a weekday. Keep the weekday rule in the shared owner; create no `PC-R` weekday publication key before a weekday collection is defined. The registry prints no Lectionary numbers for the `PC-R` matrix, so no locator is asserted here.

Reserved and out of scope for this plan: `PC-W`, the future full weekday collection. No `PC-W` ID or slug may be assigned until the registry adds its complete inventory, slug grammar, and layout. Territorial, diocesan, religious, parish, and church-proper overlays, other admitted Ritual Masses, Masses for Various Needs and Occasions, and Votive Masses are resolver-generated and admit no finite universal total in advance.

## Roman Missal 1962 collection

The 1962 books appoint one annual set of propers with no A/B/C Lectionary cycle and no *Ordo Lectionum Missae* numbering, so the cycle and Lectionary-number columns are not applicable to this collection and are omitted rather than filled with invented values. Leaves live at `src/<provider>/liturgy/roman-rite/1962/propers/temporal/<nn-slug>/` and `.../propers/ritual/<slug>/` per the repository rules. The profile fixes no slug grammar for this collection, so a slug is shown only where a leaf actually exists.

### Temporal Sunday series `01`–`52`

Stable Lent-first repository order. These are catalog identities, not the occurrence schedule of a civil year.

| ID | Occurrence | Enumeration source | Leaf slug | gpt | claude |
| ---: | --- | --- | --- | --- | --- |
| 01 | First Sunday of Lent | profile | — | not started | not started |
| 02 | Second Sunday of Lent | derived | — | not started | not started |
| 03 | Third Sunday of Lent | derived | — | not started | not started |
| 04 | Fourth Sunday of Lent | derived | — | not started | not started |
| 05 | First Sunday of the Passion (Passion Sunday) | derived | — | not started | not started |
| 06 | Second Sunday of the Passion (Palm Sunday) | derived | — | not started | not started |
| 07 | Easter Sunday | derived | — | not started | not started |
| 08 | Low Sunday (First Sunday after Easter) | derived | — | not started | not started |
| 09 | Second Sunday after Easter | derived | — | not started | not started |
| 10 | Third Sunday after Easter | derived | — | not started | not started |
| 11 | Fourth Sunday after Easter | derived | — | not started | not started |
| 12 | Fifth Sunday after Easter | derived | — | not started | not started |
| 13 | Sunday after the Ascension | derived | — | not started | not started |
| 14 | Pentecost Sunday | derived | — | not started | not started |
| 15 | Trinity Sunday (First Sunday after Pentecost) | existing leaf | `15-trinity-sunday` | published | not started |
| 16 | Second Sunday after Pentecost | existing leaf | `16-second-after-pentecost` | published | not started |
| 17 | Third Sunday after Pentecost | existing leaf | `17-third-after-pentecost` | published | not started |
| 18 | Fourth Sunday after Pentecost | existing leaf | `18-fourth-after-pentecost` | published | not started |
| 19 | Fifth Sunday after Pentecost | existing leaf | `19-fifth-after-pentecost` | published | not started |
| 20 | Sixth Sunday after Pentecost | existing leaf | `20-sixth-after-pentecost` | published | not started |
| 21 | Seventh Sunday after Pentecost | existing leaf | `21-seventh-after-pentecost` | published | not started |
| 22 | Eighth Sunday after Pentecost | existing leaf | `22-eighth-after-pentecost` | published | not started |
| 23 | Ninth Sunday after Pentecost | existing leaf | `23-ninth-after-pentecost` | published | in progress |
| 24 | Tenth Sunday after Pentecost | derived | — | not started | not started |
| 25 | Eleventh Sunday after Pentecost | derived | — | not started | not started |
| 26 | Twelfth Sunday after Pentecost | derived | — | not started | not started |
| 27 | Thirteenth Sunday after Pentecost | derived | — | not started | not started |
| 28 | Fourteenth Sunday after Pentecost | derived | — | not started | not started |
| 29 | Fifteenth Sunday after Pentecost | derived | — | not started | not started |
| 30 | Sixteenth Sunday after Pentecost | derived | — | not started | not started |
| 31 | Seventeenth Sunday after Pentecost | derived | — | not started | not started |
| 32 | Eighteenth Sunday after Pentecost | derived | — | not started | not started |
| 33 | Nineteenth Sunday after Pentecost | derived | — | not started | not started |
| 34 | Twentieth Sunday after Pentecost | derived | — | not started | not started |
| 35 | Twenty-first Sunday after Pentecost | derived | — | not started | not started |
| 36 | Twenty-second Sunday after Pentecost | derived | — | not started | not started |
| 37 | Twenty-third Sunday after Pentecost | derived | — | not started | not started |
| 38 | Twenty-fourth and Last Sunday after Pentecost | derived | — | not started | not started |
| 39 | First Sunday of Advent | derived | — | not started | not started |
| 40 | Second Sunday of Advent | derived | — | not started | not started |
| 41 | Third Sunday of Advent | derived | — | not started | not started |
| 42 | Fourth Sunday of Advent | derived | — | not started | not started |
| 43 | Sunday within the Octave of the Nativity | derived | — | not started | not started |
| 44 | First Sunday after the Epiphany (Feast of the Holy Family) | derived | — | not started | not started |
| 45 | Second Sunday after the Epiphany | derived | — | not started | not started |
| 46 | Third Sunday after the Epiphany | profile | — | not started | not started |
| 47 | Fourth Sunday after the Epiphany | profile | — | not started | not started |
| 48 | Fifth Sunday after the Epiphany | profile | — | not started | not started |
| 49 | Sixth Sunday after the Epiphany | profile | — | not started | not started |
| 50 | Septuagesima Sunday | derived | — | not started | not started |
| 51 | Sexagesima Sunday | derived | — | not started | not started |
| 52 | Quinquagesima Sunday | profile | — | not started | not started |

**Enumeration is reconstructed, not quoted.** The profile prints only three anchors — `01` is the First Sunday of Lent, `52` is Quinquagesima, and `46R`–`49R` are the resumed Third through Sixth Sundays after the Epiphany — and never prints the 52-item list. Rows marked `profile` are those anchors, which also fix `46`–`49` as the Third through Sixth Sundays after the Epiphany. Rows marked `existing leaf` are read from leaf directory names and the release manifest, which fix `15` as Trinity Sunday and `16`–`23` as the Second through Ninth Sundays after Pentecost. Rows marked `derived` are filled by the 1962 Temporale's own printed order between fixed anchors, which leaves no free choice: `02`–`14` is exactly the thirteen Sundays the missal prints between the First Sunday of Lent and Trinity Sunday, `24`–`38` is exactly the fifteen Sundays from the Tenth to the Twenty-fourth and Last after Pentecost, `45` is forced by `46`, and `50`–`51` are forced by `52`. Verify each identity against the controlling facsimile before creating its leaf.

The two least-constrained slots are `43` and `44`, the only two positions between the fourth Sunday of Advent and the Second Sunday after the Epiphany. The 1962 Temporale prints exactly two Sunday formularies there — the Sunday within the Octave of the Nativity and the First Sunday after the Epiphany, on which the Feast of the Holy Family is kept — and the Most Holy Name of Jesus, kept on the Sunday from January 2 through January 5, stands in the Proper of Saints rather than the Temporale and so falls to the `F` series. If the registry-owning profile later prints its own enumeration and it differs, the profile controls and this table is corrected, not the reverse.

### Resumed Epiphany variants `46R`–`49R`

Each is a separately sourced formulary variant under its shared ordinal, combining the relevant Epiphany orations, Epistle, and Gospel with the chants appointed for resumed use after Pentecost. The annual calendar decides how many are used and in what year; the identities are permanent regardless. They are resumed between the Twenty-third and the Last Sunday after Pentecost, and the Last Sunday remains the Twenty-fourth.

| ID | Occurrence | Shared ordinal | Leaf slug | gpt | claude |
| --- | --- | ---: | --- | --- | --- |
| 46R | Third Sunday after the Epiphany, resumed after Pentecost | 46 | — | not started | not started |
| 47R | Fourth Sunday after the Epiphany, resumed after Pentecost | 47 | — | not started | not started |
| 48R | Fifth Sunday after the Epiphany, resumed after Pentecost | 48 | — | not started | not started |
| 49R | Sixth Sunday after the Epiphany, resumed after Pentecost | 49 | — | not started | not started |

### `F` series — general-calendar feasts assigned to Sunday

`F` identifies a general-calendar feast assigned to Sunday without a stable temporal ordinal. The profile fixes no inventory, no numbering, and no count for this series, and forbids inventing a permanent Sunday number for a fixed-date, movable, or local feast. Each candidate's printed place and occurrence rule must be verified in the 1962 books before an identity is assigned. Nothing is published in this series under either provider, and the repository rules fix no directory for it beyond `propers/`, so an owning path is not asserted here.

### `M` series — ritual, votive, and other non-Sunday guides

`M` identifies a ritual, votive, or other non-Sunday guide. The prefix states no rank, permission, or authority to replace an occurring Mass. The profile fixes no inventory or count for this series. Leaves live under `src/<provider>/liturgy/roman-rite/1962/propers/ritual/`.

| ID | Occurrence | Leaf slug | gpt | claude |
| --- | --- | --- | --- | --- |
| M01 | The Nuptial Mass | `m01-nuptial-mass` | published | not started |

A ritual Mass celebrated with or for a non-Eucharistic sacrament additionally requires the canonical sacramental summary imported from `src/<provider>/theology/sacraments/summaries/`.

## Two editions per target

Every target in this plan is now two publications, not one: a study
edition at the bare id and a full-text edition at the same id with a
`-full-text` suffix, defined by [the 1962 profile](roman-1962-propers.md)
and [the postconciliar profile](postconciliar-propers.md). The counts in
this file remain counts of **targets**, not of publications; multiply by
two for the publication figure. The pair shares one identity, one owner,
one research trail, and one set of source bindings, so a target is not
half-done when only one edition exists — but a target is not finished
until both do.

The English requirement is retrospective. Every proper published before
this revision was authored under the previous rule, which printed the
appointed Latin in full and supplied no English. Those leaves are
superseded in form, not in research: their collation findings, reception
matrices, and commentary stand, and a rebuild carries them forward
rather than repeating the work. Each provider reissues its own leaves.

## Maintenance

Refresh this file when a leaf is created, released, or withdrawn, when a provider gains an edition-locale, or when the registry or either profile revises an identity, key, order, path, or count. A registry revision controls; correct this plan to match it and never the reverse. Do not resolve a count fork here that the registry leaves open, and do not promote a branch, an optional reading path, or an unregistered edition difference into a row.
