# Start here

This is the corrected **Liturgical Instrument** candidate for independent
visual review. Begin with:

1. `REVIEW_REQUEST.md` for the exact decisions requested.
2. `evidence/instrument-before-after-blockers.png` for the five quickest
   blocker comparisons.
3. `evidence/instrument-final-contact-sheet.png` for the complete required
   Instrument matrix.
4. `PLAN-AND-CONTINUITY.md` for the durable reviewer ↔ Codex mailbox,
   measurements, decisions, checks, and resume state.
5. `MEASUREMENTS.md` and `BEFORE-AFTER.md` for exact deltas and image mapping.

The runnable candidate is in `candidate/`. From this handoff directory run
`python3 -m http.server 8000`, then open:

- `http://localhost:8000/candidate/liturgy/reader-visual-reset-day.html?design=instrument#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=0`
- `http://localhost:8000/candidate/liturgy/reader-visual-reset-day.html?design=instrument#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=1&ordinary-lang=en&rubrics=1&why=0`
- `http://localhost:8000/candidate/liturgy/reader-visual-reset-propers.html?design=instrument#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la`

Public cutover remains unauthorized. Acceptance of this correction pass is
the gate for beginning production-integration execution.
