# Claude postconciliar final cold review — commands

Working directory: `/home/ksh/git/worktrees/triptych/codex/propers/homily/spincyc/triptych`

All review writes were confined to `.scratch/final-cold-claude-no/` and `build/final-cold-claude-no/`.

## Instructions and review setup

- Read workspace and repository `AGENTS.md`; the personal `ai-guidance` files named by workspace instructions were unavailable at the previously checked resolved locations.
- Read the applicable proper-study and postconciliar-propers guidance and the leaf's source/research records.
- `tools/pdf-review --help` — exit 0.

## Exact-byte inspection

- `sha256sum <study> <synthesis> <homily>` — exit 0; matched `HASHES.sha256`.
- `pdfinfo <pdf>` for all three — exit 0; 31/10/4 U.S.-Letter pages.
- `tools/pdf-review --output build/final-cold-claude-no <study> <synthesis> <homily>` — exit 0. `review-run.json` records the same exact hashes and page counts.
- `pdftotext -layout <pdf> .scratch/final-cold-claude-no/{study,synthesis,homily}.txt` — exit 0 for all three.
- Opened every study page 1–31, synthesis page 1–10, and homily page 1–4 at original raster resolution using `view_image`.

## Content and artifact gates

Document ID:

`liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a`

For each of `research`, `synthesis`, and `homily`:

- `tools/check-content-preflight --provider claude --document <id> --edition <edition>` — exit 0.
- `tools/check-proper-components --provider claude --document <id> --phase content --edition <edition>` — exit 0.
- `tools/check-proper-components --provider claude --document <id> --phase artifacts --edition <edition> --build-root build/claude --aux <edition-aux>` — exit 0.
- `python3 scripts/_proper_study.py check --provider claude --document <id> --phase artifacts --edition <edition> --require-presentation --require-format` — exit 0.

For each exact PDF:

- `tools/check-generation-metadata --provider claude --pdf <output-id> <pdf>` — exit 0.
- `pdffonts <pdf>` — exit 0; every font embedded, subset, and Unicode-mapped.

Additional gates:

- `tools/proper-chronology record --provider claude --document <id> --check` — exit 0.
- `tools/proper-chronology annotations --provider claude --document <id> --check` — exit 0.
- `python3 -m unittest tools.tests.test_propers_format tools.tests.test_proper_pagination tools.tests.test_proper_components tools.tests.test_proper_components_v2` — exit 0; 73 tests.
- `git diff --check -- src/common/propers-format.tex src/common/propers-homily.tex <leaf>` — exit 0.

## Log and boundary scans

- `rg -n -i 'overfull|underfull|undefined|multiply defined|latex warning|fatal error|emergency stop|rerun to get' <three logs>` — exit 1, the desired no-match result.
- `rg -n --glob '!**/evaluations/**' 'roman-rite/1962|/1962/|roman-1962|missal-1962|traditional-latin-mass' <leaf> <three fls files>` — exit 1, the desired no-match result.
- `qpdf --check <pdf>` was not run because `qpdf` is unavailable. No install was attempted.

## Result

Every substantive, visual, source, artifact, metadata, chronology, isolation, and focused regression gate passed. The exact-byte verdict is **PASS**.
