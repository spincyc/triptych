# Calendar Verification — 1962 Roman Rite Advent Seasonal Handbook

- **Document:** `gemini/liturgy/roman-rite/1962/seasons/advent` (*Keeping Advent: A Companion to the 1962 Roman Rite*)
- **Governing Norm:** *Codex Rubricarum* (1960), *Rubricae Generales* (RG) nn. 15, 20, 30 a, 71, 91, 109–111 (AAS 52 [1960], pp. 593–740)
- **Verification Scope:** All 7 canonical Advent opening shapes (Nov 27 through Dec 3) and all 101 civil years 2020–2120 inclusive (2,531 total Advent calendar days)
- **Verification Script:** `.scratch/lanes/lane-4/research-liturgy/verify_calendar.py` (Python 3 stdlib `datetime`, exit 0, 0 failures)
- **Sanctoral Control:** Checked against `src/sources/calendars/roman-1962/propers.yaml` and the 1960 *Tabula praecedentiae* (RG n. 91)

---

## 1. Formula and Seasonal Boundary Proof (2020–2120)

Across all 101 civil years from 2020 through 2120:

- **Equivalence check:** RG n. 20 (the Sunday falling on Nov 30 or nearest to it) equals the fourth Sunday strictly preceding Dec 25 in **101 / 101 years** (100% agreement).
- **Distinct opening shapes:** Exactly 7 opening dates occur (Nov 27 through Dec 3), corresponding uniquely to the weekday of Dec 25 (Sunday through Monday).
- **Liturgical bounds (RG n. 71):** Advent opens at First Vespers of the First Sunday of Advent on the preceding Saturday evening and closes at None inclusive on Dec 24 (the Vigil of the Nativity), spanning **22 to 28 calendar days** (28 days when Advent I is Nov 27; 22 days when Advent I is Dec 3).
- **Great O Antiphon acrostic (Dec 17–23):** Forward initials `S-A-R-C-O-R-E` reverse cleanly to `E-R-O C-R-A-S` (*Ero cras*, "Tomorrow I will be").

---

## 2. Master Table of All Seven Canonical Advent Shapes

| Advent I | Days | Dec 25 | Sun II | Sun III (*Gaudete*) | Ember Wed / Fri / Sat | Sun IV | Years in 2020–2120 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nov 27 | 28 | Sun | Dec 4 | Dec 11 | Dec 14 / 16 / 17 | Dec 18 | 15 (2022, 2033, 2039, ...) |
| Nov 28 | 27 | Sat | Dec 5 | Dec 12 | Dec 15 / 17 / 18 | Dec 19 | 15 (2021, 2027, 2032, ...) |
| Nov 29 | 26 | Fri | Dec 6 | Dec 13 | Dec 16 / 18 / 19 | Dec 20 | 15 (2020, 2026, 2037, ...) |
| Nov 30 | 25 | Thu | Dec 7 | Dec 14 | Dec 17 / 19 / 20 | Dec 21 | 14 (2025, 2031, 2036, ...) |
| Dec 1 | 24 | Wed | Dec 8 | Dec 15 | Dec 18 / 20 / 21 | Dec 22 | 14 (2024, 2030, 2041, ...) |
| Dec 2 | 23 | Tue | Dec 9 | Dec 16 | Dec 19 / 21 / 22 | Dec 23 | 14 (2029, 2035, 2040, ...) |
| Dec 3 | 22 | Mon | Dec 10 | Dec 17 | Dec 20 / 22 / 23 | Dec 24 (Vigil) | 14 (2023, 2028, 2034, ...) |

### Ember Day Ranges and Great O Antiphon Intersections

| Movable Day | Date Range | Inside Dec 17–23? | Great O Antiphons Possible at Vespers |
| --- | --- | --- | --- |
| Sunday III (*Gaudete*) | Dec 11–17 | Only on Dec 3 shape (Dec 17) | *O Sapientia* (Dec 17 only) |
| Ember Wednesday | Dec 14–20 | 4 of 7 shapes (Nov 30–Dec 3) | *O Sapientia* (Dec 17) through *O Clavis David* (Dec 20) |
| Ember Friday | Dec 16–22 | 6 of 7 shapes (Nov 28–Dec 3) | *O Sapientia* (Dec 17) through *O Rex Gentium* (Dec 22) |
| Ember Saturday | Dec 17–23 | **All 7 of 7 shapes** | *O Sapientia* (Dec 17) through *O Emmanuel* (Dec 23) |
| Sunday IV | Dec 18–24 | All 6 non-Vigil shapes (Dec 18–23) | *O Adonai* (Dec 18) through *O Emmanuel* (Dec 23); replaced on Dec 24 by I Vespers of Christmas |

---

## 3. Critical 1962 Precedence Collisions Verified

| Collision Key | Trigger Shape | 1960 *Codex Rubricarum* Rule | Verified Years (2020–2040) |
| --- | --- | --- | --- |
| `dec-08-on-sun-ii` | Advent I = Dec 1 | Immaculate Conception (I cl., RG n. 91 row 4) **wins** over Sunday II (I cl., row 6); Sunday II receives the single privileged commemoration (RG nn. 15, 109 a, 111 a). | 2024, 2030 |
| `dec-24-on-sun-iv` | Advent I = Dec 3 | Vigil of the Nativity (I cl., RG n. 91 row 5) **replaces** Sunday IV (row 6) with **no commemoration** of Sunday IV (RG n. 30 a). In the same year, *O Sapientia* falls on *Gaudete* Sunday (Dec 17). | 2023, 2028, 2034 |
| `dec-21-on-sun-iv` | Advent I = Nov 30 | Sunday IV (I cl., row 6) **wins** over St. Thomas, Apostle (II cl., row 16); St. Thomas is omitted (not a privileged commemoration on a I-class Sunday, RG nn. 109, 111 a). | 2025, 2031, 2036 |
| `dec-21-on-ember-sat` | Advent I = Dec 1 | St. Thomas, Apostle (II cl., row 16) **wins** over Ember Saturday (II cl. feria, row 18); Ember Saturday receives the privileged commemoration (RG nn. 109 e, 111 a). | 2024, 2030 |
| `dec-21-on-ember-fri` | Advent I = Dec 2 | St. Thomas, Apostle (II cl., row 16) **wins** over Ember Friday (II cl. feria, row 18); Ember Friday receives the privileged commemoration (RG nn. 109 e, 111 a). | 2029, 2035 |
| `nov-30-on-sun-i` | Advent I = Nov 30 | Sunday I (I cl., row 6) **wins** over St. Andrew, Apostle (II cl., row 16); St. Andrew is omitted. | 2025, 2031, 2036 |
| `dec-13-on-sun-iii` | Advent I = Nov 29 | Sunday III (I cl., row 6) **wins** over St. Lucy (III cl., row 24); St. Lucy is omitted. | 2020, 2026, 2037 |
| `dec-16-on-ember` | Advent I = Nov 27 or Nov 29 | Ember Friday (Nov 27 shape) or Ember Wednesday (Nov 29 shape) (II cl. feria, row 18) **wins** over St. Eusebius (III cl., row 24); St. Eusebius receives an ordinary commemoration at Low and conventual Mass (omitted at non-conventual sung Mass, RG nn. 110–111). | 2020, 2022, 2026, 2033, 2037, 2039 |

---

## 4. Evergreen Two-Track Daily Course Verification (Appendix A)

The handbook's evergreen daily course (`sections/90-daily-course.tex`) partitions every Advent cleanly into two disjoint tracks:

1. **Movable Weekly Track (Advent I through Dec 16):** Week I (Sun–Sat), Week II (Sun–Sat), and the pre-Dec 17 days of Week III (including any Ember Day occurring on Dec 14–16).
2. **Fixed Final Track (Dec 17 through Dec 24):** The seven Great O Antiphon days (Dec 17–23) and the Vigil of the Nativity (Dec 24), carrying explicit movable-day overlays for Sunday III (if Dec 17), Ember Wednesday/Friday/Saturday (whenever they fall inside Dec 17–23), and Sunday IV (if Dec 18–23; replaced by the Vigil on Dec 24).

### Exhaustive Partition Proof (2,531 Days, 2020–2120)

- **Total Advent days verified:** 2,531
- **Uncovered days:** **0**
- **Ambiguous primary-slot overlaps:** **0**
- **Week I bounds:** Always ends Dec 3–9 (strictly before Dec 17).
- **Week II bounds:** Always ends Dec 10–16 (always on or before Dec 16).
- **Week IV bounds:** Always falls inside Dec 18–24 (100% inside the Fixed Final Track).

### Exact Handoff Across All Seven Shapes (Dec 16 to Dec 17)

| Advent I Shape | Last Movable Slot (Dec 16) | First Fixed Slot (Dec 17, *O Sapientia*) | Week III Overlays Inside Dec 17–23 |
| --- | --- | --- | --- |
| Nov 27 | Week III Friday (Ember Fri) | Dec 17 + Ember Saturday | Ember Sat (Dec 17) |
| Nov 28 | Week III Thursday | Dec 17 + Ember Friday | Ember Fri (Dec 17), Ember Sat (Dec 18) |
| Nov 29 | Week III Wednesday (Ember Wed) | Dec 17 (feria) | Ember Fri (Dec 18), Ember Sat (Dec 19) |
| Nov 30 | Week III Tuesday | Dec 17 + Ember Wednesday | Ember Wed (Dec 17), Fri (Dec 19), Sat (Dec 20) |
| Dec 1 | Week III Monday | Dec 17 (feria) | Ember Wed (Dec 18), Fri (Dec 20), Sat (Dec 21, after St. Thomas) |
| Dec 2 | Week III Sunday (*Gaudete*) | Dec 17 (feria) | Ember Wed (Dec 19), Fri (Dec 21, after St. Thomas), Sat (Dec 22) |
| Dec 3 | Week II Saturday | Dec 17 + Sunday III (*Gaudete*) | Sun III (Dec 17), Ember Wed (Dec 20), Fri (Dec 22), Sat (Dec 23) |

All tables in `sections/06-first-week.tex`, `sections/09-ember-days.tex`, `sections/10-fourth-week-and-great-antiphons.tex`, `sections/11-vigil-of-the-nativity.tex`, and `sections/90-daily-course.tex` were checked line-by-line against this report with zero discrepancies.
