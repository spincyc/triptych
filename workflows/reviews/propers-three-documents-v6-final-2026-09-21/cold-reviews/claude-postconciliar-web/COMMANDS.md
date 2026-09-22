# Command log

Repository root: `/home/ksh/git/worktrees/triptych/codex/propers/homily/spincyc/triptych`

No Chromium or other browser command was run.

| Exit | Command or inspection | Result |
| ---: | --- | --- |
| 0 | `sha256sum build/web/claude/.../pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a.md` | Exact requested SHA `b00ee2b...8e3ea6`. |
| 0 | `tools/tpt web-edition --provider claude --output .scratch/claude-no-web-review-evidence/regenerated <document>` | Fresh candidate generated. |
| 0 | `cmp -s <candidate> <fresh-regeneration>` and `sha256sum` | Byte-identical; both `b00ee2b...8e3ea6`. |
| 0 | `diff -u <old-reviewed-markdown> <candidate>` | Exactly two replacements of trailing-space hard breaks by `<br>`; no other delta. (`diff` returned 1 as expected and was accepted by the wrapper.) |
| 0 | `cat <leaf>/research/web-artifact.json` | Receipt path and SHA match candidate. |
| 0 | `tools/tpt check-web-edition --provider claude --document <document>` | One eligible declaration valid. |
| 0 | `tools/tpt check-proper-components ... --phase content --edition research` | One schema-2 component manifest valid. |
| 0 | `tools/tpt check-proper-components ... --phase artifacts --edition research --build-root build/claude` | Research artifacts valid. |
| 0 | `tools/tpt check-content-preflight ... --edition research` | 94 bindings; chronology record/annotations/claims; relation coverage; references; restrictions; labels; and quotation checks pass. |
| 0 | `tools/tpt public-alpha check --provider claude --document <document>` | Scoped public-alpha policy valid; not deployment verification. |
| 0 | `rg -n '[ \\t]+$' <candidate>; test $? -eq 1` | No trailing whitespace. |
| 0 | `find build/web/claude web/claude ... -synthesis.md/-homily.md` with empty assertion | No companion web leaf. |
| 0 | `rg -n -i '<cross-rite terms>' <candidate>; test $? -eq 1` | No cross-rite match. |
| 0 | Static counts over current receipt HTML | Four tables, 11 TOC links, 12 four-sense terms, zero duplicate IDs. |
| 0 | Recomputed receipt input/proof hashes with `sha256sum` | Renderer, layout, CSS, icon, candidate, HTML, and copied asset identities confirmed. |
| 0 | `view_image` on supplied exact-candidate desktop/mobile screenshots and prior old-byte desktop/mobile top screenshots | Candidate top views inspected; no clipping, overlap, or horizontal overflow visible. |
| 0 | Read prior `REPORT.md`, `COMMANDS.md`, and `browser-audit.json`; inspect prior chronology captures | Prior deep audit PASS and its exact old Markdown identity confirmed. |
| 0 | `git status --short -- <review paths>` | Only the pre-existing tracked `research/web-artifact.json` modification is reported; this review wrote ignored scratch files only. |
