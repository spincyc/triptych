# Dated Occurrences — 2026 (U.S. Postconciliar Roman Rite, Gemini)

This file records dated civil-year occurrence resolutions for authorized Gemini
postconciliar targets under `roman-missal-third-edition-en-us-2011` in 2026.
Dated entries are resolved independently under
[`guidance/liturgy/calendar-computation.md`](../../../../../../../guidance/liturgy/calendar-computation.md)
and corroborated against dated official United States calendar witnesses;
computed arithmetic alone is never treated as an occurrence authority.

## Verified Occurrences

### 2026-11-29 (Sunday) — First Sunday of Advent (`PC-S01-B`)

- **Civil date:** Sunday, 29 November 2026 (`2026-11-29`).
- **Resolved celebration:** First Sunday of Advent (*Dominica I Adventus*).
- **Permanent parent and formula key:** `PC-S01` / `PC-S01-B`.
- **Full publication slug:** `pc-s01-first-sunday-of-advent-year-b`.
- **Canonical shared Missal formulary owner:** [`pc-s01-first-sunday-of-advent`](../temporal/shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md) (offline collation bounds completed in `research`).
- **Lectionary locator:** *Ordo Lectionum Missae* (1981) / *Lectionary for Mass* (U.S., 1998/2002), No. 2 (Year B).
- **Liturgical year and cycle resolution:**
  - Under *Universal Norms on the Liturgical Year and the Calendar* (NUALC) nn. 40 and 44 and *General Introduction to the Lectionary* (OLM *Praenotanda*) n. 66.2 (fn. 102), the liturgical year turns at Evening Prayer I of the First Sunday of Advent (the Sunday falling on or closest to 30 November; equivalently the fourth Sunday before 25 December). Because 25 December 2026 is a Friday (and 30 November 2026 is a Monday), Sunday, 29 November 2026 is the First Sunday of Advent and opens **liturgical year 2026–2027** (running 2026-11-29 through 2027-11-27, ending in civil year `Y = 2027`).
  - **Sunday Lectionary cycle:** `2027 mod 3 = 2` → **Year B**.
  - **Requested study cycle vs. actual appointed cycle on 2026-11-29:** Requested target `PC-S01-B` is **Year B**; the actual appointed cycle on `2026-11-29` is **Year B**. They match exactly (no divergence or substitution).
  - **Independent weekday Lectionary cycle:** `Y = 2027` (odd) → **Year I** (OLM *Praenotanda* nn. 65, 69). Recorded for liturgical-year completeness only; the weekday cycle governs the Ordinary Time ferial course alone and does not apply to Sundays or to Advent weekdays (OLM *Praenotanda* n. 69).
- **Precedence, occurrence, and territorial check:**
  - **Table of Liturgical Days (NUALC 59):** Place 2 (Part I — Sundays of Advent, Lent, and Easter). Outranks every solemnity of the General Roman Calendar (place 3), proper solemnity (place 4), feast of the Lord (place 5), and all lower ranks; no commemoration is admitted (NUALC 60).
  - **General Roman Calendar check:** No fixed-date celebration is inscribed on 29 November (`src/sources/calendars/postconciliar/propers.yaml` records 0 entries for `11-29`; Saint Andrew, Apostle, Feast, occurs on Monday, `2026-11-30`).
  - **U.S. Proper Calendar check:** No U.S. national proper celebration falls on 29 November (Thanksgiving Day falls on the fourth Thursday of November, `2026-11-26`). Diocesan, religious, and parish proper calendars lie outside universal/national resolution, and even a proper solemnity on 29 November would yield to the First Sunday of Advent under NUALC 5 and 59.
- **Liturgical color:** Unverified offline in tracked GIRM records (no GIRM 346 passage is extracted in `src/sources/`; left as an explicit offline verification boundary).
- **Verification basis and completed offline research bounds:**
  - **Computed finding aid:** `tools/tpt calendar-days day --calendar postconciliar --date 2026-11-29 --format json` returns `appointed = "advent-1"`, `year = 2027`, `lectionary.sunday = "B"`, `lectionary.weekday = "I"`, `candidates = ["advent-1"]`, `commemorations = []`, `unresolved = []`.
  - **Dated official U.S. calendar witnesses in `src/sources/` (reconciled in leaf `research/source-bindings.toml`):**
    1. USCCB, *Liturgical Calendar for the Dioceses of the United States of America 2026* (full PDF catalog lead `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`, SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02`), verified front-matter passage `passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.principal-celebrations-and-cycles` (artifact pp. 7–8, verified 2026-07-25), bounding liturgical year 2026 by the First Sundays of Advent on 30 November 2025 and 29 November 2026.
    2. USCCB, *Liturgical Calendar for the Dioceses of the United States of America 2027* (full PDF catalog lead `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2027.usccb-pdf-d7997b57`, SHA-256 `d7997b57de96fdbf6433af917a65597b108c720c930f3c39356bf0f5058074ce`), verified front-matter passage `passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2027.principal-celebrations-and-cycles` (artifact pp. 7–8, verified 2026-07-25), opening liturgical year 2027 on the First Sunday of Advent, 29 November 2026, under Sunday Cycle B and Weekday Cycle I.
    3. USCCB Daily Readings dated page for 29 November 2026 (`artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-11-23-page-for-2026-11-29.lectionary-2-27c3cb63`, SHA-256 `27c3cb635b7bdbbac6aa8be8015c44aa55dbeef8c15ad46b2b075ab418b6f9ab`, `https://bible.usccb.org/bible/readings/112926.cfm`, retrieved 2026-11-23), registered as restricted identity metadata (`lead`) attesting U.S. Lectionary No. 2 on `2026-11-29`.
    4. Calendar-variations currentness catalog leads: USCCB *Liturgical Calendar* publication index (`artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-publication-index.2026-11-05-web.official-html-9939c12b`, retrieved 2026-11-05) and Dicastery for Divine Worship *Calendarium Romanum* variations index (`artifact.dicastery-for-divine-worship-and-the-discipline-of-the-sacraments.calendarium-romanum-web-index.2026-10-25-english-web.official-html-4531f6b6`, retrieved 2026-10-25).
  - **Closed offline research boundary (as of 2026-11-25):** The `research` stage completed offline without external network access; the restricted bytes of `2026cal.pdf`, `2027cal.pdf`, and `112926.cfm` are not retained in Git and were not reopened offline. Occurrence and Year B / Weekday Cycle I resolution rest on the verified `principal-celebrations-and-cycles` passages of the 2026 and 2027 USCCB calendars corroborated against `tools/tpt calendar-days`, while direct inspection of the 29 November 2026 day-entry page of `2027cal.pdf` and live HTML of `112926.cfm` remains an explicit open offline boundary rather than a pending retrieval gate.
