# Appendix — stub-dependent conclusions, rechecked

`.scratch/cold-audit/src.py --bible <locus>` has always raised
`ModuleNotFoundError`; `scripts/_bible.py` has never existed on any branch
(`git log --all --diff-filter=A` on it is empty). Every conclusion in the
review record that could have rested on it was re-resolved through the real
machinery: the tracked Douay JSON, `tools/tpt citations`, and the chronology
loader.

**Result: no BLOCKED disposition exists anywhere in the record, and no
conclusion depended on the stub.** All 73 `bible:douay-rheims:` source ids
resolve; 77 of 78 prose-form citations resolve and the one miss is inside a
verbatim quotation using Authorised Version numbering. 27 case groups were
re-resolved and every negative held.

| tool | mechanism | `Gen.5.3` result |
| --- | --- | --- |
| `.scratch/cold-audit/verse.py` | `src/sources/bibles/<ed>/chapters/<Bk>/<ch>.json` → `verses[n]` | WORKS |
| `.scratch/verse.py` | same | WORKS |
| `.scratch/research/ol-verse.py` | same (absolute path) | WORKS |


| file | disposition column | values |
| --- | --- | --- |
| `cold-audit-findings.tsv` | `result` | CHANGES_REQUIRED 104 |
| `post-audit-corrections.tsv` | `audit_result` | CHANGES_REQUIRED 104 |
| `post-audit-corrections.tsv` | `correction_disposition` | fixed 96, withdrawn-after-new-evidence 8 |
| `post-audit-rereview-findings.tsv` | `result` | PASS 91, CHANGES_REQUIRED 23 |
| `final-rereview-corrections.tsv` | `disposition` | fixed 23 |
| `final-acceptance-manifest.tsv` | `prior_result` | PASS 94, CHANGES_REQUIRED 32, not-previously-reviewed 30 |


| # | case (file) | original conclusion, verbatim | locus re-resolved — true text | verdict |
| --- | --- | --- | --- | --- |
| 1 | `A2-026` / `A2-029` / `RR-024` (findings, corrections, rereview) | "The stored relative.statement was a reordering **the tracked Douay does not contain**"; "Saul enters the discourse only at Acts 13:21" | Acts.13.20 *"As it were, after four hundred and fifty years. And after these things, he gave unto them judges, until Samuel the prophet."*; Acts.13.21 *"And after that they desired a king: and God gave them Saul the son of Cis…"*; Acts.13.19 *"…divided their land among them by lot."* | negative TRUE — PASS |
| 2 | `A3-027` (findings, corrections) | "the claim's own note asserted that the corpus holds no first year of Artaxerxes… **the premise is false**" | 2Esd.1.1 *"…in the month of Casleu, in the twentieth year…"* (no king named); 2Esd.2.1 *"…in the twentieth year of Artaxerxes the king…"* | TRUE — PASS |
| 3 | `A4-004` / `RR-020` | "Exodus 7:25 measures the seven days from the striking of the river, not from the audience of Exodus 5" | Ex.7.25 *"And seven days were fully ended, after that the Lord struck the river."*; Ex.7.20 *"…he struck the water of the river before Pharao…"*; Ex.5.1 *"After these things, Moses and Aaron went in…"* | TRUE — PASS |
| 4 | `A4-006` | "Both cited verses count the three days from the passage of the Red Sea" | Ex.15.22 *"And Moses brought Israel from the Red Sea… they marched three days"*; Num.33.8 *"…they passed through the midst of the sea… having marched three days"*; Num.33.5-7 give Soccoth, Etham, Phihahiroth between | TRUE — PASS |
| 5 | `A8-007` | "the corpus holds, from Num.10.11 and Num.33.16-17, that Haseroth is two stations after a departure dated the twentieth day of the second month of the SECOND year"; "**Scripture supplies no interval at all**" | Num.10.11 *"The second year, in the second month, the twentieth day of the month…"*; Num.33.16-17 graves of lust → Haseroth | TRUE — PASS |
| 6 | `A4-017` / `WD-A4-017` (a **withdrawal**) | withdrawn because "the stored claim carries NO offset: its statement is the within-day sequence" | Ezech.24.18 *"So I spoke to the people in the morning, and my wife died in the evening…"* | TRUE — PASS |
| 7 | `A2-028` / `RR-023` | "The Douay text here reads forty" (after striking an unsourced Greek variant) | 1Kings.4.18 *"…And he judged Israel forty years."* | TRUE — PASS |
| 8 | `A7-017` / `S4-011` | "the text does put the anchor's END at this event"; label must state position, not length | 1Kings.4.11 *"And the ark of God was taken…"*; 4.12; 4.18 | TRUE — PASS |
| 9 | `LEAD-013` / `RR-012` | "the nearest antecedent of 'his reign' is 'the king of Babylon', and 24:8 gives Joachin three months, so **Joachin has no eighth year**" | 4Kings.24.12 *"…and the king of Babylon received him in the eighth year of his reign."*; 4Kings.24.8 *"…he reigned three months in Jerusalem…"*; Jer.25.1 anchor *"(the same is the first year of Nabuchodonosor…)"*; 2Par.36.9 *"…three months and ten days…"* | TRUE — PASS |
| 10 | `LEAD-016` | "27:52-53 is ONE sentence — 52 ends in a comma and 53 completes it"; "verse 53… narrates something the verse itself dates after the Resurrection" | Matt.27.52 *"…many bodies of the saints that had slept arose,"* (comma); 27.53 *"And coming out of the tombs **after his resurrection**…"* | TRUE — PASS |
| 11 | `S3-001` / `S4-005` / `FA-134` / `FA-141` / `FA-142` | "scripture quotation **does not match** the tracked Douay text at the locus cited" (Mark 15:33) | Mark.15.33 *"And when the sixth hour was come, there was darkness over the whole earth until the ninth hour."* | negative TRUE — PASS (fix verified at HEAD, §6) |
| 12 | `G-002` / `FA-128` | "a Scripture string inside quotation marks that **does not match** the tracked Douay" (Ps 77:24) | Ps.77.24 *"And had rained down manna upon them to eat, and had given them the bread of heaven."* | negative TRUE — PASS |
| 13 | `C-006` / `FA-011` / `FA-124` | quotation altered terminal punctuation; "Ps 50:1 and Ps 51:1 really do end in a comma" | Ps.53.1 *"Unto the end, in verses, understanding for David."* (full stop); Ps.50.1 and Ps.51.1 both end *"…for David,"* (comma) | TRUE — PASS |
| 14 | `P-012` / `E2-008` | "**Scripture is genuinely silent** within this event's own scope: 4 Kings 25:4-21 carries no year"; "4 Kings 25:2 and 25:8 are already authored as preferred rank-1 claims" | 4Kings.25.21 *"…so Juda was carried away out of their land."* — no year; 25:2 *"…till the eleventh year of king Sedecias"*; 25:8 *"…the nineteenth year of the king of Babylon…"* | TRUE — PASS |
| 15 | `C-009` / `FA-003` / `FA-004` | "the Douay title of Ps 30 **names no occasion at all**" | Ps.30.1 *"Unto the end, a psalm for David, in an ecstasy."* | negative TRUE — PASS |
| 16 | `G-010` / `FA-045` | Ps 56 and Ps 141 titles both send to the cave | Ps.56.1 *"…when he fled from Saul into the cave. [1 Kings 24.]"*; Ps.141.1 *"…A prayer when he was in the cave. [1 Kings 24.]"* | TRUE — PASS |
| 17 | `FA-139` | Ps 50 title and 2 Kings 12 | Ps.50.2 *"When Nathan the prophet came to him, after he had sinned with Bethsabee. [2 Kings 12.]"*; 2Kings.12.13 *"…I have sinned against the Lord…"* | TRUE — PASS |
| 18 | `A6-021` / `FA-017` | "the war's own unquantified length"; "'A long time' cannot be a duration" | Jos.11.18 *"Josue made war a long time against these kings."*; Jos.11.23 *"…And the land rested from wars."*; Jos.4.19 *"…the tenth day of the first month…"* | TRUE — PASS |
| 19 | `E1-010` / `LEAD-014` / `FA-033` | "the verse puts the Exodus at the interval's start and the Temple at its end" | 3Kings.6.1 *"…in the four hundred and eightieth year after the children of Israel came out of the land of Egypt, in the fourth year of the reign of Solomon…"* | TRUE — PASS |
| 20 | `A3-006` / `E1-018` / `FA-041` | the forty years of 2 Kings 15:7 | 2Kings.15.7 *"And after forty years, Absalom said to king David…"* | TRUE — PASS |
| 21 | `LEAD-015` | the demand for a king | 1Kings.8.5 *"…make us a king, to judge us, as all nations have."* | TRUE — PASS |
| 22 | `A4-013` / `RR-009` / `FA-024` | unmarked elision splicing Ezech 1:1 to 1:2 "across twenty-six dropped words" | Ezech.1.1 *"…on the fifth day of the month, when I was in the midst of the captives by the river Chobar…"*; Ezech.1.2 *"On the fifth day of the month, the same was the fifth year of the captivity of king Joachin,"* | TRUE — PASS |
| 23 | `RR-059` / `FA-079` / `FA-080` | the second prefixed letter's endpoints | 2Mach.1.11 *"Having been delivered by God out of great dangers…"*; 2Mach.2.19 *"For he hath delivered us out of great perils, and hath cleansed the place."* | TRUE — PASS |
| 24 | `S3-001` note; crucifixion #5/#6 | "Nisan = month 1 is correctly grounded" | Ex.12.2 *"…it shall be the first in the months of the year."*; Esth.3.7 *"In the first month (which is called Nisan)…"* | TRUE — PASS |
| 25 | `A5-025` (refuted finding) | "`duration` is structurally unavailable because 'in his days' is not a whole positive number of units" | Gen.10.25 *"…because in his days was the earth divided…"* | TRUE — PASS |
| 26 | `V-008` / `V-012` / `V-013` / `RR-089` / `FA-148` / `FA-152` / `FA-153` — **three withdrawals** | "Esth 4:6, 9:5 and 9:30 are **not printed** by the World English Catholic witness… its Esther 4 prints 1-5 and 7-47, its Esther 9 prints 1-4, 6-29 and 31-32" | Re-run at HEAD: `_deuterocanon._printed('world-english-catholic')` = **2094** loci; `('Esth',4,6)`, `('Esth',9,5)`, `('Esth',9,30)` all **ABSENT**; `('Dan',3,71)`, `('Esth',1,1)`, `('Esth',3,13)`, `('Esth',5,1)`, `('Esth',5,2)`, `('Esth',8,13)` all PRESENT. `_printed('greek')` = **2156**; `('SgThree',1,45)` ABSENT, `('SgThree',1,48)` PRESENT | negative TRUE — PASS. Note these are the **WEC/greek witnesses, not the Douay**; `--bible` could not have produced this evidence even had it worked |
| 27 | `F-021`, `LEAD-001`, `LEAD-002`, `P-012` — the remaining four **withdrawals** | withdrawn on `guidance/sources.md` and on the Haydock facsimile page 776 | no Scripture locus involved | not stub-exposed — PASS |
