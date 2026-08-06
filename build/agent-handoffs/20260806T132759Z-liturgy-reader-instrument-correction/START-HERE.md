# Start here

This is the narrow Round 1 re-review package for the selected **Liturgical
Instrument** foundation. The direction and the six accepted Round 0 findings
are frozen. Review only the intermediate-width and extreme-reflow shell.

1. Read `REVIEW_REQUEST.md` for the three exact dispositions requested.
2. Open `evidence/round1-shell-before-after.png` for the two blocker pairs.
3. Inspect every original under `evidence/screenshots/after/`, beginning with
   `01-day-read-1024x768.png` and `08-text-200-percent-393x852.png`.
4. Read `MEASUREMENTS.md`, `BEFORE-AFTER.md`, and `checks.txt` for measured
   geometry and regression dispositions.
5. Read `PLAN-AND-CONTINUITY.md` for the exact reviewer message, Codex response,
   decisions, and stopping point.

The compact candidate is in `candidate/`. From this directory run
`python3 -m http.server 8000`, then open:

- `http://localhost:8000/candidate/liturgy/reader-visual-reset-day.html?design=instrument#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=0`
- `http://localhost:8000/candidate/liturgy/reader-visual-reset-day.html?design=instrument#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=1&ordinary-lang=en&rubrics=1&why=0`

Production-integration execution and public cutover remain unauthorized.
