# Resolve / Materialize Context

## Your task

Resolve and materialize the liturgical context for the target proper. This
means identifying the exact formulary, its appointed texts, and the
calendrical context that governs it.

## Steps

1. Use `tools/tpt mass-propers show --calendar roman-1962 --mass <key>` to
   resolve the proper's mass entry and its propers.
2. Identify the mass key from the calendar that corresponds to this proper.
3. Record the appointed elements (Introit, Collect, Epistle, Gradual,
   Alleluia/Tract, Gospel, Offertory, Secret, Communion, Postcommunion).
4. Identify any seasonal substitutions, commemorations, or ritual additions
   that apply.
5. Record the proper's rank, occurrence rule, and place in the 1962 Missal.
6. Use `tools/tpt calendar-rubrics assign --calendar roman-1962 --date <date>`
   if a specific date context is needed.

## Result

Return a worker result with `disposition: "PASS"` and a summary of the
resolved context, including the mass key, appointed elements, rank, and any
applicable substitutions.
