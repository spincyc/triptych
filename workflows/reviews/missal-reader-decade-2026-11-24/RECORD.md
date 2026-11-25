# Mass reader review, 24 November 2026 to 23 November 2036

The review covers 3,653 inclusive civil dates in each of the Roman 1962 and postconciliar general calendars. It includes every territorial branch, its principal and other readable formularies, and each named form. An unresolved local observance remains a choice. A commemorated Mass can be opened for study without adopting it as the celebration of the date. Good Friday has its own service.

## Reading checks

The browser checks used Chromium on the production Day and Propers pages. Each navigation compared the selected source event identities and their order against the rendered document, checked for broken text or horizontal overflow, and timed the navigation. The dated Read and Missal passes used the English Ordinary and orations with Latin alongside, and Douay–Rheims with the Clementine Vulgate. Selecting another reading, prayer owner, minister or witness can change the content. Future decrees and individual local calendars can change the celebration on a given date.

| Missal | Mode | Civil dates | Appointments | Browser navigations | Rendered events | Median / p95 navigation (ms) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1962 | Read | 3,653 | 7,040 | 10,693 | 106,980 | 95 / 189 |
| 1962 | Missal | 3,653 | 7,040 | 10,693 | 1,804,374 | 411 / 874 |
| Postconciliar | Read | 3,653 | 6,163 | 9,740 | 62,486 | 74 / 145 |
| Postconciliar | Missal | 3,653 | 6,163 | 9,740 | 652,896 | 221 / 543 |

An appointment identifies a date, territory, Mass and form. Both modes covered the same 13,203 appointments. The replay opened each civil date and also navigated explicitly to its selectable cases, so a navigation can revisit an appointment. Every inspected browser document matched the selected source event sequence, with zero horizontal overflows or broken text values. Navigation timings include local data loading, assembly and rendering in a desktop Chromium session while other checks were running.

The browser also compared the words in 120 historical Vigil language placements and 2,770 modern antiphon language placements per mode. Its timing ends when the requested reading has rendered. Source comparisons run afterward.

The dated 1962 Missal pass checked the Creed heading, its opening and its two continuations as one unit. The reader displayed all four in 1,068 appointments. On the other dated appointments it kept them out of the spoken reading together. The standalone pass applied the same check to all 499 forms.

The terminal checks used the production Node adapter and Textual formatter. Keyboard and compositor checks used actual Textual key events. A live Linux terminal opened the First Sunday of Advent in the publisher’s U.S. English edition using Lynx 2.9.3 and returned to the Collect at the same source dialog. Chromium loaded the publisher’s original page in an on-demand frame, reached the Advent heading and restored focus with Escape. The indexed terminal and the public dated CLI matched on all 651 events across Christmas Night, Christmas Day and the first and third All Souls Masses. Each Christmas form retained its appointed Gloria and Creed. Source and performance measurements for each terminal size are recorded separately. [Terminal verification](TERMINAL.md)

To replay the browser check, serve the production pages and generated browser data, install Selenium 4 and Chromium with a compatible ChromeDriver, then give the script the reader URL and the same-origin data root. Each calendar can be run independently. The optional Propers URL checks standalone Mass forms, Commons, and the individual source choices attached to a memorial. Pass `--mode read` for the separate Read-mode sweep. Repeat `--mass KEY` to check the dates on which particular formularies occur and their standalone forms. The browser verifies the words in each newly sourced antiphon and Vigil passage against its language record. The `--first` and `--last` arguments take inclusive ISO dates. [Browser verifier](verify_web.py)

```sh
python workflows/reviews/missal-reader-decade-2026-11-24/verify_web.py \
  http://localhost:8000/liturgy/day.html /browse roman-1962 \
  --propers-url http://localhost:8000/liturgy/index.html
```

The standalone Missal pass opened all 499 Roman forms, including 30 Commons, and all 689 modern forms, including 60 Common forms. On the modern forms it checked 1,176 English prayer positions, 990 Latin formulary links and a further 326 English and 47 Latin passage links. Across 134 memorials it checked 268 independently selectable prayer positions, 1,144 permitted source choices and 1,215 source occurrences. It also exercised the two choices on each of the 36 optional Lenten prayers. At the ten Easter Vigils and in standalone Propers, both Read and Missal carried the three bilingual passages locally and retained both consultation editions.

The Presentation’s Gospel comparison retains its longer and shorter readings and the independent candle-lighting and procession choices. The production Share and Print suite checked seven cases, including its six-page comparison PDF. The two Gospel citations and their opening verses appear together on page 4. [Comparison and print checks](../../../tools/tests/liturgy_reader_share_print_browser.mjs)

## Edition and source boundaries

The Latin 1962 facsimile links identify a page of the verified 1,088-page altar Missal for each of the 499 modeled forms. The book’s referrals retain the named Common or formulary. The opening is directly accessible from the special Holy Week rites. The standalone Propers reader also offers 34 off-date chant appointments in 32 formularies. Each opens at the actual chant page. Five include the complete bilingual Marian Common Tract, and nine also identify a Common biblical appointment. The three Requiems and Pentecost Tuesday retain their exact biblical citations to Fourth Esdras alongside their complete Missal chants, an independently attested Latin text and an original English study translation. The choice of Bible determines whether it can also display the separate biblical passage. [1962 facsimile inventory](../../../src/sources/inventories/roman-1962-missal-witness-links-v1.toml)

The modern inventories distinguish the U.S. English Missal, the English Antiphonary, Canadian Lectionary and Holy See supplements. They preserve the scope of a Collect, antiphon or direction to a Common at the individual form. The public eMissal’s U.S. version is dated 26 October 2021. Its index contains several misleading or missing bookmarks. The inventory records those cases and identifies the precise consulted editions. The postconciliar Ordinary has verified publisher links for all 72 represented elements, including the 2011 episcopal excerpts and the full English Eucharistic Prayers. [U.S. reader published by Australian Liturgy](https://liturgy.au/product/roman-emissal-usa-epub/) · [Dated English Missal](../../../src/sources/inventories/postconciliar-emissal-proper-links-v1.toml) · [Other proper witnesses](../../../src/sources/inventories/postconciliar-missal-witness-links-v1.toml) · [Ordinary sources](../../../src/sources/inventories/postconciliar-ordo-missae-v1.toml)

The English publisher supplies the current edition online. A source consultation adds no offline words to the corpus. The reader marks historical and study wording beside the text. The 2002 Latin Missal and its supplements have separate source identities, and a comparison with the 2008 reprint requires its own evidence. [Publication policy](../../../guidance/liturgical-text-publication-policy.md)

The 1962 Palm Sunday Passion and the permitted additional Low Mass Gospel use the rubrics of their respective courses. Holy Tuesday and Holy Wednesday carry their Passion appointments. At the evening Mass on Holy Thursday, the choice of solemn or authorized Low Mass and the decision about the washing of feet govern the text shown. Each Easter Vigil includes its pre-Mass rites, the Vigil Mass and Lauds at Communion. The nocturnal Preface, the Easter *Communicantes* opening and the double-Alleluia dismissal have local Latin and historical English from Alessandro Mazzinelli’s *Office of Holy Week* (Baltimore, 1870), printed pages 514–515 and 517. The Preface leads into the separately appointed Sanctus. The variable *Communicantes* rejoins the Canon before the 1962 continuation naming Saint Joseph. Both readers also offer the 1962 altar Missal page and the English passage in a private bilingual hand missal. Good Friday opens the printed service. [1962 Ordinary](../../../src/sources/inventories/roman-1962-ordo-missae-v1.toml) · [Baltimore witness](../../../src/sources/works/alexander-mazzinelli/the-office-of-holy-week/editions/baltimore-kelly-piet-1870/edition.toml) · [Bilingual Vigil hand missal](https://extraordinaryform.org/masses/EasterVigilM20.pdf#page=2)

In the modern calendar, a weekday can use the prayers of any of the 34 weeks of Ordinary Time. For each of the 204 eligible weekday formularies the tests exercised all 34 sources, retaining the dated weekday’s readings. A memorial can select the Prayer over the Offerings and Prayer after Communion independently from its permitted sources. Week I and Week XXXIV are available for those choices even when the corresponding Sunday celebrates another feast. Across the ten years, 10 Ash Wednesdays have their dismissal prayer and 360 other Lenten weekdays have the choice to pray or omit the Prayer over the People. Seven ferial prayers have full historically witnessed Latin and study English, used on 70 of these dates. The Ash Wednesday distribution chants and the Presentation candle-lighting and procession chants retain their particular liturgical seats. The shorter modern Fourth Esdras antiphons on Easter II and at All Souls have both local texts and source links for the particular occurrence in each language. [Calendar rubrics](../../../src/sources/calendars/postconciliar/rubrics.yaml) · [Memorial prayer appointments](../../../src/sources/inventories/postconciliar-memorial-prayer-sources-v1.toml)

The modern edition has complete earlier Latin witnesses and original study English for 89 antiphon positions. Ten belonged to the Commons and lacked local bodies. Seventy-nine dated positions previously offered the appointed Scripture as a Bible reconstruction. The new antiphons preserve each appointment’s Bible reference, option number and source spelling. The Nativity Mass at Night also inherits one of these pairs. The standalone browser check selected all 90 occurrences in both modes, including their alternatives. The two Commons containing the ten new local texts retain the approved Antiphonary links at their original pages. A comparison of all 1,601 Mass files in the three generated missals verified all 388 previously catalogued language-specific consultation links. The reader reopened all 25 forms of the two affected Commons in each mode after the link restoration. The Latin witnesses come from the Clementine Vulgate and the Tours Missal of 1922. [Historical antiphon sources](../../../src/sources/works/triptych/postconciliar-latin-proper-editorial-projection/editions/2026-11-24-historical-antiphons/edition.toml)

The modern Kyrie displays the six Greek acclamations in the Latin column and the six historical English glosses in the English column. The source credits distinguish the early wording from its arrangement for the modern rite. Both columns mark the three calls and responses. The separate Kyrie is omitted when the selected Penitential Act has already included it. [Greek source arrangement](../../../src/sources/works/triptych/postconciliar-kyrie-greek-study-arrangement) · [General Instruction, paragraph 52](https://www.vatican.va/content/dam/wss/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html)

For the responsorial Psalm at Saturday of Ordinary Time XXIV in Year II, the 1981 *Ordo lectionum Missae* appoints three groups down to the closing verse. The Nova Vulgata, the four Vulgate-numbered editions offered here, and the three English editions using Hebrew numbering divide those verses differently. The shared reconstruction preserves the closing words in all seven Bibles and attributes each reading to its edition. [Lectionary source record](../../../src/sources/works/catholic-church/ordo-lectionum-missae/editions/latin-editio-typica-altera-1981/passages/olm-448-ii-responsorial-psalm.toml)

Ten Latin Proper chants in eight 1962 Masses have verified publication text in the 1922 Tours Mame Missal. The affected Masses occur on 80 dates in the reviewed decade. The browser reopened them in both modes and the native reader checked 90 appointed chant placements. The source change preserved the Latin and English bodies. The editorial record keeps the historical comparison and the page in the independent publication witness. [1962 Latin source records](../../../src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml)

The independent census distinguishes a published missal text, a historical or study translation, a Bible reconstruction, a confirmed prayer with unavailable wording, and a missing or unresolved appointment. DOM agreement proves that the reader renders the assembled material. The census and its source witnesses determine how much of the printed edition that material supplies. [Readiness tool](../../../tools/complete-missal)

## Coverage at the reviewed source cut

| Independent finding aid | Represented | Established but unrepresented | Target correspondence unresolved |
| --- | ---: | ---: | ---: |
| Roman 1962 | 4,307 | 0 | 3,685 |
| Postconciliar | 277 | 0 | 2,440 |

These counts apply to the independently enumerated slices. The 34 off-date 1962 chant appointments count in the standalone votive setting. All eight formerly missing established postconciliar roles have a place in their respective rites.

| Local composed or mixed Proper targets | English held | Latin held | Exact target Latin |
| --- | ---: | ---: | ---: |
| Roman 1962 | 1,486 / 1,486 | 1,486 / 1,486 | 1,482 |
| Postconciliar | 573 / 1,799 | 395 / 1,764 | 371 |

The target denominator is language-specific and counts each represented text once. English holdings include historical and original study translations. Four locally held 1962 Latin texts have an unresolved exact-edition classification in the census. They are the Secret of the Immaculate Conception, the Introit of Thursday in the third week of Lent, and two entries for Holy Thursday evening, the direction when there is no washing of feet and the hymn at the transfer of the Blessed Sacrament. The public consultation action supplies the edition at the selected place. The postconciliar inventory marks the 1,226 remaining English targets as unavailable for local publication and 1,369 Latin targets as locally unresolved. A future authoritative publication decision or a separately verified historical exemplar can change that status. [Independent source inventory](../../../src/sources/inventories/missal-expected-targets-v1.toml) · [Corpus census](../../../src/sources/calendars/README.md)

## Release verification

Two independent builds of the registered website data produced identical bytes across 13 product families and 30,398 files. The normal product installer and checker both passed. The 1,657 release files compared directly with the audited reader data included all 1,614 Proper files, 34 calendar files, four Ordinary files, four rubric files and the Bible catalogue. All hashes matched. The committed reader index passed its independent check over 85,424 files and 60,305 records. [Browser product record](../../../release/browser-products.json)

The corpus census validated all fifteen completeness dimensions. Its strict readiness check returned `ready: false`, with 39 unresolved dimension cells across the modeled families. The release manifest bound 360 newly recognized sources and updated 42 existing digests. The final binding check reported zero stale entries. The public-alpha source and rights check passed for all 310 publication records. The 19 groups of browser prayer-choice checks passed against the refreshed release. The two modern content and seasonal-antiphon test modules passed all 23 tests on the final data. The commands below reproduce the stored product, index and census checks.

```sh
tools/browser-products check
tools/release-bindings status
tools/public-alpha check
tools/corpus-index check --readers
tools/complete-missal --check --json
tools/complete-missal --readiness --require-resolved --json
```

## Historical test receipt

The current coverage checks verified the three alternate prayers in the Common of Supreme Pontiffs against their individual Latin witnesses and English study translations. An October source-batch receipt still requires an older digest of the complete artifact-delivery manifest. The unchanged receipt rejected the upstream `d87793fa01` inputs as well as the reviewed inputs here. Twelve historical methods in the coverage suite reach that guard. Its expected digest and the archived receipt were preserved. [Source-batch guard](../../../tools/tests/_source_batch_guards.py) · [Coverage checks](../../../tools/tests/test_missal_coverage.py)

Two modern checks previously failed on the upstream inputs as well. The seasonal antiphon test now compares the archival declarations for all eleven historical withholdings with their original bytes, then checks the ten later independent English admissions and the remaining Easter Monday option. The CLI test opens the Nativity Mass at Dawn. Its Prayer after Communion has a documented English restriction and an unavailable Latin body, so the two language selections can be checked on the same actual prayer. Both tests passed. [Seasonal antiphon receipt](../../../tools/tests/test_postconciliar_seasonal_antiphon_recovery.py) · [Modern content checks](../../../tools/tests/test_postconciliar_content_integrity.py)
