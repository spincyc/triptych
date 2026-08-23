# Seed Stage

This is the initial stage of the 1962 propers synthesis production workflow.

## Your task

You are seeding a proper guide production run. Confirm the target proper
exists in the repository and gather the initial context needed for the
workflow.

## Steps

1. Confirm the proper leaf directory exists at
   `src/{provider}/{proper}/`.
2. Read the `proper-components.toml` manifest if it exists.
3. Read the `guidance/liturgy/roman-1962-propers.md` profile.
4. Read the `guidance/editorial.md` universal editorial standard.
5. Read the `guidance/repository.md` repository and build rules.
6. Identify the proper's calendar entry in
   `src/sources/calendars/roman-1962/propers.yaml`.
7. Summarize the current state of the proper leaf: what exists, what is
   missing, and what the workflow will need to produce.

## Result

Return a worker result with `disposition: "PASS"` and a summary of the
proper's current state, including:
- whether the leaf directory exists
- whether `proper-components.toml` exists
- whether `main.tex` exists
- whether `synthesis.tex` exists
- whether the proper has a calendar entry
- any missing prerequisites for the workflow
