# Multi-Decade Programmatic Calendar Verification: Postconciliar Advent (2020–2120)

- **Publication:** `gemini/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/seasons/advent`
- **Calendar:** Postconciliar Roman Rite (General Roman Calendar with United States Proper Calendar norms for Dec 8 and Dec 12)
- **Verification span:** 101 consecutive Advent seasons, civil years 2020 through 2120 (inclusive)
- **Verification date:** 2026-11-27
- **Cross-check tool:** `tools/calendar-days day --calendar postconciliar --date <DATE> --json` (15 boundary/collision dates tested; 100% agreement with independent Python computation)

## Controlling Calendar Rules

1. **Opening and closing (`Normae Universales de Anno Liturgico et de Calendario`, nn. 39–42):**
   - Advent opens with Evening Prayer I of the Sunday falling on or nearest to November 30 (equivalently, the Fourth Sunday before December 25, always inside **November 27 – December 3**).
   - Advent concludes before Evening Prayer I of the Nativity of the Lord on the evening of **December 24**.
2. **Sunday Lectionary Cycle (`Ordo Lectionum Missae` 1981, *Praenotanda* n. 66.2):**
   - Determined by the civil year `Y` in which the liturgical year **ends** (i.e., `advent_year + 1`):
     - `Y mod 3 == 1` → **Year A** (Matthew)
     - `Y mod 3 == 2` → **Year B** (Mark)
     - `Y mod 3 == 0` → **Year C** (Luke)
   - Weekday Lectionary Cycle I/II governs Ordinary Time only; Advent weekdays repeat the same annual course every year (with Year A offering an optional Isaiah 4:2–6 first reading on Monday of Week 1 when Isaiah 2:1–5 was proclaimed the day before, OLM n. 175).
3. **Two-phase weekday architecture (`Normae Universales` nn. 16b, 42, 59; OLM nn. 175–201):**
   - **Phase I (week-keyed, Monday of Week 1 through December 16):** 17 Lectionary positions exist (`Mon–Sat` of Week 1 [6], `Mon–Sat` of Week 2 [6], `Mon–Fri` of Week 3 [5]; OLM prints **no** Saturday of Week 3 because Saturday of Week 3 always falls on or after December 17, when Phase II begins).
   - **Phase II (date-keyed privileged ferias, December 17–24):** 8 Lectionary positions (OLM nn. 193–200), ranking at Table of Liturgical Days no. 9 (above all memorials; IGMR 355a permits only substituting a memorial's Collect). The Fourth Sunday of Advent always falls inside **December 18–24**, displacing one privileged weekday; when Advent 3 falls on December 17 and Advent 4 on December 24, **two** privileged weekdays (Dec 17 and Dec 24) are displaced by Sundays.
4. **United States Marian overlaps (`Normae Universales` nn. 5, 59, 60; USCCB Proper Calendar):**
   - **December 8 (Solemnity of the Immaculate Conception):** Rank 3 vs. Sundays of Advent Rank 2. When Dec 8 falls on the Second Sunday of Advent, the Sunday prevails and the Solemnity transfers to Monday, December 9.
   - **December 12 (Feast of Our Lady of Guadalupe in the U.S.):** Rank 8 vs. Sundays of Advent Rank 2. When Dec 12 falls on the Third Sunday of Advent, the Sunday prevails and the Feast is omitted for that liturgical year (never transferred).

## 101-Year Summary Statistics (2020–2120)

| Metric | Verified Result | Count / Breakdown (out of 101 seasons) |
|---|---|---|
| Earliest First Sunday of Advent | **November 27** | 15 seasons (e.g., 2022, 2033, 2039, 2044) |
| Latest First Sunday of Advent | **December 3** | 14 seasons (e.g., 2023, 2028, 2034, 2045) |
| Shortest Advent (Adv 1 through Dec 24 morning) | **22 days** | 14 seasons (Adv 1 = Dec 3; Adv 4 = Dec 24) |
| Longest Advent (Adv 1 through Dec 24 morning) | **28 days** | 15 seasons (Adv 1 = Nov 27; Adv 4 = Dec 18) |
| Week-3 weekdays held (Mon–Fri before Dec 17) | **0 to 5 weekdays** | 0 days: 28 yrs; 1 day: 14; 2 days: 14; 3 days: 15; 4 days: 15; 5 days: 15 |
| Privileged weekdays held (Dec 17–24) | **6 or 7 weekdays** | 7 days: 87 seasons; 6 days: 14 seasons (when Adv 3 = Dec 17 & Adv 4 = Dec 24) |
| Dec 8 falls on Second Sunday of Advent (→ Mon Dec 9) | **14 seasons** | 2020–2050: **2024, 2030, 2041, 2047** |
| Dec 12 falls on Third Sunday of Advent (omitted in U.S.) | **15 seasons** | 2020–2050: **2021, 2027, 2032, 2038, 2049** |
| Dec 17 falls on Third Sunday & Dec 24 on Fourth Sunday | **14 seasons** | 2020–2050: **2023, 2028, 2034, 2045** |

### First Sunday Date Distribution (2020–2120)
- **Nov 27** (28 days): 15 seasons
- **Nov 28** (27 days): 15 seasons
- **Nov 29** (26 days): 15 seasons
- **Nov 30** (25 days): 14 seasons
- **Dec 01** (24 days): 14 seasons
- **Dec 02** (23 days): 14 seasons
- **Dec 03** (22 days): 14 seasons

## Worked Multi-Year Table (2024–2040)

| Advent Year | Liturgical Year Ends | Cycle | Adv 1 | Adv 2 | Adv 3 | Adv 4 | Length | Wk 3 Wkdays | Dec 17–24 Wkdays | Dec 8 | Dec 12 | Dec 24 |
|---:|---:|:---:|:---:|:---:|:---:|:---:|---:|---:|---:|:---:|:---:|:---:|
| 2024 | 2025 | C | Dec 1 | Dec 8 | Dec 15 | Dec 22 | 24 | 1 | 7 | **Sun → Mon Dec 9** | Thu | Tue |
| 2025 | 2026 | A | Nov 30 | Dec 7 | Dec 14 | Dec 21 | 25 | 2 | 7 | Mon | Fri | Wed |
| **2026** | **2027** | **B** | **Nov 29** | **Dec 6** | **Dec 13** | **Dec 20** | **26** | **3** | **7** | **Tue** | **Sat** | **Thu** |
| 2027 | 2028 | C | Nov 28 | Dec 5 | Dec 12 | Dec 19 | 27 | 4 | 7 | Wed | **Sun (omitted)** | Fri |
| 2028 | 2029 | A | Dec 3 | Dec 10 | Dec 17 | Dec 24 | 22 | 0 | 6 | Fri | Tue | **Sun (Adv 4)** |
| 2029 | 2030 | B | Dec 2 | Dec 9 | Dec 16 | Dec 23 | 23 | 0 | 7 | Sat | Wed | Mon |
| 2030 | 2031 | C | Dec 1 | Dec 8 | Dec 15 | Dec 22 | 24 | 1 | 7 | **Sun → Mon Dec 9** | Thu | Tue |
| 2031 | 2032 | A | Nov 30 | Dec 7 | Dec 14 | Dec 21 | 25 | 2 | 7 | Mon | Fri | Wed |
| 2032 | 2033 | B | Nov 28 | Dec 5 | Dec 12 | Dec 19 | 27 | 4 | 7 | Wed | **Sun (omitted)** | Fri |
| 2033 | 2034 | C | Nov 27 | Dec 4 | Dec 11 | Dec 18 | 28 | 5 | 7 | Thu | Mon | Sat |
| 2034 | 2035 | A | Dec 3 | Dec 10 | Dec 17 | Dec 24 | 22 | 0 | 6 | Fri | Tue | **Sun (Adv 4)** |
| 2035 | 2036 | B | Dec 2 | Dec 9 | Dec 16 | Dec 23 | 23 | 0 | 7 | Sat | Wed | Mon |
| 2036 | 2037 | C | Nov 30 | Dec 7 | Dec 14 | Dec 21 | 25 | 2 | 7 | Mon | Fri | Wed |
| 2037 | 2038 | A | Nov 29 | Dec 6 | Dec 13 | Dec 20 | 26 | 3 | 7 | Tue | Sat | Thu |
| 2038 | 2039 | B | Nov 28 | Dec 5 | Dec 12 | Dec 19 | 27 | 4 | 7 | Wed | **Sun (omitted)** | Fri |
| 2039 | 2040 | C | Nov 27 | Dec 4 | Dec 11 | Dec 18 | 28 | 5 | 7 | Thu | Mon | Sat |
| 2040 | 2041 | A | Dec 2 | Dec 9 | Dec 16 | Dec 23 | 23 | 0 | 7 | Sat | Wed | Mon |

## Cross-Check Against `tools/calendar-days`

All 15 boundary dates tested via `tools/calendar-days day --calendar postconciliar --date <DATE> --json` matched the programmatic calculation:
- `2024-12-08`: Second Sunday of Advent (Year C); `2024-12-09`: Immaculate Conception transferred (Solemnity).
- `2026-11-29`: First Sunday of Advent (Year B); `2026-12-08`: Immaculate Conception (Solemnity); `2026-12-12`: Our Lady of Guadalupe; `2026-12-17`: Dec 17 privileged feria; `2026-12-20`: Fourth Sunday of Advent (Year B); `2026-12-24`: Dec 24 morning feria (handoff to Nativity Evening Prayer I in the evening).
- `2027-11-28`: First Sunday of Advent (Year C); `2027-12-12`: Third Sunday of Advent (Guadalupe displaced).
- `2028-12-03`: First Sunday of Advent (Year A, shortest 22-day Advent); `2028-12-17`: Third Sunday of Advent (Dec 17 feria displaced); `2028-12-24`: Fourth Sunday of Advent (Dec 24 morning feria displaced; Nativity Vigil Mass in evening).
- `2030-12-08`: Second Sunday of Advent (Year C; Dec 8 transferred to Mon Dec 9).
- `2033-11-27`: First Sunday of Advent (Year C, longest 28-day Advent, all 5 Week-3 weekdays held).
