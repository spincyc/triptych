# 101-Year Calendar & Rubric Verification: 1962 Roman Rite *Tempus Nativitatis* (2020/2021–2120/2121)

- **Document:** `gemini/liturgy/roman-rite/1962/seasons/christmas` (*Keeping Christmas: A Companion to the 1962 Roman Rite*)
- **Span Verified:** **101 consecutive Christmas seasons** (`2020/2021` through `2120/2121`), covering **1,212 *Tempus Nativitatis* liturgical days** (25 December through 5 January inclusive, RG 72 a) plus both boundary days: 24 December (*In Vigilia Nativitatis Domini*) and 6 January (*In Epiphania Domini*).
- **Rubric Engine Cross-Check:** All **7 possible 25 December weekday shapes** (1 representative season per shape × 14 days 24 Dec – 6 Jan = **98 liturgical days**) were cross-checked directly against the repository's 1962 rubric engine (`tools/calendar-days` + `tools/calendar-rubrics` reading `src/sources/calendars/roman-1962/rubrics.yaml`).
- **Result:** **0 discrepancies / 98 representative days** (`exit 0`); **0 uncovered days and 0 ambiguous overlaps** across all 1,212 *Tempus Nativitatis* days in Appendix A (`sections/90-daily-course.tex`).

---

## 1. Distribution of the Seven 25 December Weekday Shapes (2020/2021–2120/2121)

Because Christmas Day (25 December) is fixed on the solar calendar and the 12-day span 25 December – 5 January never crosses 29 February, **the weekday of 25 December uniquely determines the entire structural shape of the 1962 Christmas season**.

| 25 Dec Weekday | Seasons in 2020–2120 | Representative Season | 24 Dec Weekday | Sun within Octave | Most Holy Name of Jesus | Non-Holy-Name Sat in 2–5 Jan (`missa-de-s-maria-in-sabbato-2`, row 27) | 2–5 Jan Mon–Fri Ferias (Jan 1 Mass, row 28) |
|---|---:|---|---|---|---|---|---:|
| **Sunday** | **15** | `2022/2023` | Sat | **NONE** (25 Dec is Sun) | **Mon 2 Jan** (fallback) | **NONE** (Sat is 31 Dec / 7 Jan) | 3 (3, 4, 5 Jan) |
| **Monday** | **14** | `2023/2024` | **Sun** (replaces Adv IV) | **Sun 31 Dec** (St. Sylvester & Day 7 omitted) | **Tue 2 Jan** (fallback) | **NONE** (Sat is 30 Dec / 6 Jan) | 3 (3, 4, 5 Jan) |
| **Tuesday** | **14** | `2029/2030` | Mon | **Sun 30 Dec** (Day 6 omitted) | **Wed 2 Jan** (fallback) | **Sat 5 Jan** (with St. Telesphorus comm. Low only) | 2 (3, 4 Jan) |
| **Wednesday** | **14** | `2024/2025` | Tue | **Sun 29 Dec** (St. Thomas & Day 5 omitted) | **Sun 5 Jan** (St. Telesphorus omitted!) | **Sat 4 Jan** | 2 (2, 3 Jan) |
| **Thursday** | **14** | `2025/2026` | Wed | **Sun 28 Dec** (Holy Innocents comm. Low only) | **Sun 4 Jan** | **Sat 3 Jan** | 2 (2, 5 Jan) |
| **Friday** | **15** | `2026/2027` | Thu | **Sun 27 Dec** (St. John comm. Low only) | **Sun 3 Jan** | **Sat 2 Jan** | 2 (4, 5 Jan) |
| **Saturday** | **15** | `2027/2028` | Fri | **Sun 26 Dec** (St. Stephen comm. Low only) | **Sun 2 Jan** | **NONE** (Sat is 1 Jan / 8 Jan) | 3 (3, 4, 5 Jan) |
| **TOTAL** | **101** | — | — | **86 seasons with Sun; 15 NONE** | **58 Sunday / 43 Jan 2 fallback** | **57 seasons with Sat BVM / 44 NONE** | **246 feria days** |

*Partition check on all 404 days in 2–5 January across 101 seasons:* `101 Most Holy Name days + 57 Saturday BVM days + 246 Mon–Fri feria days = 404 days` (exact partition).

*Partition check on all 1,212 days in 25 December–5 January across 101 seasons:* `101 Christmas Days + 86 Sundays within Octave + 86 St. Stephen + 86 St. John + 87 Holy Innocents + 87 Day 5 + 87 Day 6 + 87 Day 7 + 101 Octave Days (1 Jan) + 101 Most Holy Name + 57 Saturday BVM + 246 Mon–Fri ferias = 1,212 days` (exact partition; Appendix A Table 1 + Table 2 covers every day with 0 gaps and 0 overlaps).

### Exact Year Lists for All Seven Shapes (Named by the Civil Year of 25 December)

- **25 Dec = Sunday (15):** 2022, 2033, 2039, 2044, 2050, 2061, 2067, 2072, 2078, 2089, 2095, 2101, 2107, 2112, 2118.
- **25 Dec = Monday (14):** 2023, 2028, 2034, 2045, 2051, 2056, 2062, 2073, 2079, 2084, 2090, 2102, 2113, 2119.
- **25 Dec = Tuesday (14):** 2029, 2035, 2040, 2046, 2057, 2063, 2068, 2074, 2085, 2091, 2096, 2103, 2108, 2114.
- **25 Dec = Wednesday (14):** 2024, 2030, 2041, 2047, 2052, 2058, 2069, 2075, 2080, 2086, 2097, 2109, 2115, 2120.
- **25 Dec = Thursday (14):** 2025, 2031, 2036, 2042, 2053, 2059, 2064, 2070, 2081, 2087, 2092, 2098, 2104, 2110.
- **25 Dec = Friday (15):** 2020, 2026, 2037, 2043, 2048, 2054, 2065, 2071, 2076, 2082, 2093, 2099, 2105, 2111, 2116.
- **25 Dec = Saturday (15):** 2021, 2027, 2032, 2038, 2049, 2055, 2060, 2066, 2077, 2083, 2088, 2094, 2100, 2106, 2117.

---

## 2. Critical Rubrical Collisions Verified Against `tools/calendar-rubrics`

1. **Sunday 24 December Vigil (14/101 seasons, 25 Dec = Mon, e.g. `2023-12-24`):** Vigil of the Nativity (I cl., RG 91 row 5) replaces Advent IV (I cl., row 6) outright with no commemoration (RG 30 a) and sings the Sunday conditional Alleluia *Crastina die delebitur* (1962 p. 15 no. 102).
2. **Sunday within the Octave vs. 26–28 December (44/101 seasons):** Under 1960 precedence (RG 91 row 15 vs. row 16), Sunday within the Octave wins over St. Stephen (26 Dec, 15×), St. John (27 Dec, 15×), and Holy Innocents (28 Dec, 14×); the impeded saint receives an ordinary commemoration in **Low Mass only** (RG 111 a–b). When 25 December is Sunday (15/101 seasons), no Sunday within the Octave occurs anywhere in the year.
3. **Sunday within the Octave vs. 29 & 31 December (28/101 seasons):** On Sunday 29 December (14×) and Sunday 31 December (14×), the Sunday supersedes Days 5 and 7 and **omits St. Thomas of Canterbury and St. Sylvester I even in Low Mass** (RG 16 a, 111 b).
4. **Weekdays 26–28 December (Mon–Sat):** II cl. saint's feast wins (row 16) with **privileged commemoration of the Christmas Octave** (RG 109 c) in **both Low and Sung Masses** (using the Day Mass orations *Concede*, *Oblata*, *Praesta*). On 28 December, Holy Innocents is vested in **red** unconditionally (RG 124 e), abolishing folded chasubles (RG 137), and saying *Gloria*, *Te Deum*, *Alleluia* (*Laudate, pueri*, 1962 p. 27 unit 186), and *Ite, missa est* (RGMR 507).
5. **Most Holy Name of Jesus on Sunday 5 January (14/101 seasons, 25 Dec = Wed, e.g. `2025-01-05`):** Most Holy Name (II cl. feast of the Lord, row 14) **omits St. Telesphorus completely** (`omitted: ["comm-s-telesphori-papae-martyris"]`) even in Low Mass (RG 16 a, 111 b).
6. **Non-Holy-Name Saturdays in 2–5 January (`missa-de-s-maria-in-sabbato-2`, 57/101 seasons):** Obligatory IV cl. Office and Mass of Our Lady on Saturday (RG 78, RG 91 row 27, RGMR 270 & 515 b) outranks the IV cl. feria (row 28), taking *Vultum tuum* (1962 pp. [44]–[45]) with *Gloria*, **BVM Preface (*Et te in veneratione*)** (not the Nativity Preface, because 2–5 January lacks the Octave override of 26–31 December on 1962 p. 284), no Creed, and common *Communicantes*. On Saturday 5 January (14/101 seasons, 25 Dec = Tue, e.g. `2030-01-05`), Low Mass adds the ordinary commemoration of St. Telesphorus.
7. **Mon–Fri Ferias in 2–5 January (246 days / 101 seasons):** IV cl. feria (row 28) repeating the 1 January Mass (*Puer natus est*, 1962 p. 34 exception to RGMR 299) with *Gloria* and Nativity Preface (*tamquam de Tempore*), without Creed or proper *Communicantes*; Low Mass adds St. Telesphorus on Mon–Fri 5 January (73/101 seasons; `73 Mon–Fri + 14 Sat + 14 Sun = 101`).
8. **5 January Dusk Handoff (RG 72 a–b):** *Tempus Nativitatis* closes at None of 5 January inclusive; First Vespers of the Epiphany opens *Tempus Epiphaniae*.

---

## 3. Engine-Verified Representative Schedules (All 7 Shapes, 98 Days, 0 Discrepancies)

| Shape (25 Dec) | Rep. Season | 24 Dec | 26–31 Dec Notable Collisions | 1 Jan | 2–5 Jan Schedule |
|---|---|---|---|---|---|
| **Sunday** (15×) | `2022/2023` | Sat Vigil | Mon–Wed *Comites* (+Oct.); Thu–Sat Days 5–7; **no Sun in Oct.** | Sun Oct. Day | Mon 2 Jan Holy Name; Tue–Thu 3–5 Jan Ferias (5 Jan +Telesph. Low) |
| **Monday** (14×) | `2023/2024` | **Sun Vigil** (replaces Adv IV) | Tue–Thu *Comites* (+Oct.); Fri–Sat Days 5–6; **Sun 31 Dec Sun in Oct.** (omits Sylvester) | Mon Oct. Day | Tue 2 Jan Holy Name; Wed–Fri 3–5 Jan Ferias (5 Jan +Telesph. Low) |
| **Tuesday** (14×) | `2029/2030` | Mon Vigil | Wed–Fri *Comites* (+Oct.); Sat Day 5 (+Thomas Low); **Sun 30 Dec Sun in Oct.**; Mon Day 7 (+Sylvester Low) | Tue Oct. Day | Wed 2 Jan Holy Name; Thu–Fri 3–4 Jan Ferias; **Sat 5 Jan BVM Sat II** (+Telesph. Low) |
| **Wednesday** (14×) | `2024/2025` | Tue Vigil | Thu–Sat *Comites* (+Oct.); **Sun 29 Dec Sun in Oct.** (omits Thomas); Mon–Tue Days 6–7 | Wed Oct. Day | Thu–Fri 2–3 Jan Ferias; **Sat 4 Jan BVM Sat II**; **Sun 5 Jan Holy Name** (omits Telesph.) |
| **Thursday** (14×) | `2025/2026` | Wed Vigil | Fri–Sat Stephen/John (+Oct.); **Sun 28 Dec Sun in Oct.** (+Innocents Low only); Mon–Wed Days 5–7 | Thu Oct. Day | Fri 2 Jan Feria; **Sat 3 Jan BVM Sat II**; **Sun 4 Jan Holy Name**; Mon 5 Jan Feria (+Telesph. Low) |
| **Friday** (15×) | `2026/2027` | Thu Vigil | Sat Stephen (+Oct.); **Sun 27 Dec Sun in Oct.** (+John Low only); Mon Innocents (+Oct.); Tue–Thu Days 5–7 | Fri Oct. Day | **Sat 2 Jan BVM Sat II**; **Sun 3 Jan Holy Name**; Mon–Tue 4–5 Jan Ferias (5 Jan +Telesph. Low) |
| **Saturday** (15×) | `2027/2028` | Fri Vigil | **Sun 26 Dec Sun in Oct.** (+Stephen Low only); Mon–Tue John/Innocents (+Oct.); Wed–Fri Days 5–7 | Sat Oct. Day | **Sun 2 Jan Holy Name**; Mon–Wed 3–5 Jan Ferias (5 Jan +Telesph. Low) |
