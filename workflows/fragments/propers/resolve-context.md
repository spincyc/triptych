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
7. Write the proper's chronology record:

   ```
   tools/tpt proper-chronology record --provider {provider} \
       --document {proper} --write
   ```

   This resolves the formulary's appointed verses through the same calendar
   entry you just read, spells them as loci, asks the Scripture chronology
   corpus about each one, and writes what it answers to
   `src/{provider}/{proper}/research/chronology.toml`. Read the file you have
   written and report in your summary which elements the corpus dates, which
   it dates only by composition, and which it dates nowhere.

## Biblical dates come from one place

`guidance/scripture-chronology.md` §14 governs every later stage of this run
and this stage is where the corpus reaches it:

> A publication or proper that needs biblical chronology MUST read this
> corpus. It MUST NOT independently infer, research, harmonize, or assign a
> replacement biblical date.

The record you write is that reading, carried so that no later stage has to
repeat it and no later stage may replace it. Where the corpus returns
`undated-in-tradition`, `research-pending`, or no assertion at all, that is
its answer and not a gap: the guide will state the absence, and a stage that
fills it with a figure from a commentary, a chronological table, or its own
recollection has broken the contract however good the source looked.

The record is generated. Do not edit it, and do not compose one by hand. If
the command refuses, report the refusal; a refusal is an answer.

## Result

Return a worker result with `disposition: "PASS"` and a summary of the
resolved context, including the mass key, appointed elements, rank, any
applicable substitutions, and the chronology status of each appointed
Scripture.
