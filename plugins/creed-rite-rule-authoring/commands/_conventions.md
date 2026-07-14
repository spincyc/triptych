# Command Conventions

Every user-facing slash command in this plugin applies the following contract. Files whose names begin with `_` are internal conventions, not commands.

## Invocation input

- Treat everything the user supplies with the slash command as controlling task context. It may be labeled fields, ordinary prose, source links, pasted notes, or a mixture.
- Preserve added emphases, guides, limits, exclusions, style preferences, source suggestions, staging requests, and commit instructions. Do not discard material merely because it does not match a suggested field.
- The command's `What to provide` section describes the information that makes the workflow reproducible; it is not a rigid parser. Inspect the repository and infer only what can be established safely. Ask a question only when a missing choice would materially change the result.
- The user's current request and thread context take priority over command defaults. Never treat a command as permission to rewrite Git history, publish externally, contact another person, or restructure unrelated parts of the repository.

## Preflight

1. Confirm the working directory is the Creed, Rite, Rule repository and inspect `git status --short`. Preserve unrelated changes.
2. Read `AGENTS.md`, `README.md`, `guidance/editorial.md`, `guidance/repository.md`, every applicable genre profile, and the target document's source and research records before editing.
3. Identify provider, collection, genre, rite, edition, language or locale, jurisdiction, calendar, and as-of date wherever they matter.
4. Determine whether the invocation creates a document, revises content, changes structure, installs PDFs, commits a stage, or only reports findings. A creation or publication command authorizes its normal repository artifacts; a commit or history rewrite still requires explicit authorization in the invocation or current thread.
5. For mutable doctrine-adjacent discipline, law, judgments, editions, translations, demographics, software behavior, or current institutions, verify the present state from primary or official sources.

## Plan

- State a short, checkable plan before substantial work.
- Separate structural setup from substantive revision when reviewable history benefits from that division.
- Treat source records, canonical fragments, publication artifacts, catalog entries, and guidance updates as part of the same coherent stage when the governing profile requires them.
- Continue through safe in-scope research and implementation. Pause only for a genuinely blocking choice, unavailable controlling source, or authority the user has not granted.

## Commands

- Research from primary, official, edition-identified sources wherever available. Treat OCR, search snippets, aggregations, and secondary citations as leads until checked.
- Keep received text, verified quotation or paraphrase, source-grounded synthesis, original editorial or AI proposal, and unresolved leads distinct.
- Create or update the profile-required scope, source-audit, inventory, status, derivation, edition, or rubric records before claiming completion.
- Preserve one textual owner for shared material. Register every consumer and rebuild all affected consumers after a shared change.
- Refresh the structured generation metadata for the final substantive generation event without exposing machine or session identifiers.
- Build for enough passes to settle references, inspect logs, visually inspect every page, install only reviewed PDFs, and update the README catalog with one artifact link per named column.
- Commit only when authorized. Use a concise subject and the required `AI summary:` body, and stage only the coherent files belonging to the completed stage.

## Verification

- Run the universal and profile-specific quality gates.
- Check source-record completeness, metadata rendering, local links, build/install identity, and every affected consumer.
- Report warnings, unresolved evidence, missing specialist review, and any step not performed. Never convert an unperformed check into a claim of success.

## Summary

Return the outcome first: created or revised documents, source records, installed artifacts, catalog or guidance changes, verification results, commits, and material limitations.

## Next Steps

Name only the next action that remains genuinely useful, such as independent theological review, a missing primary-source collation, plugin refresh, or a separately scoped follow-on document.
