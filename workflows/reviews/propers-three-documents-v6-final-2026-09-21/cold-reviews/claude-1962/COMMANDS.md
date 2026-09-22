# Commands and exit status

Working directory:
`/home/ksh/git/worktrees/triptych/codex/propers/homily/spincyc/triptych`

The commands below were run against the final frozen bytes. Expected no-match
`rg` scans return 1 and are labelled as such.

## Review setup

```text
tools/pdf-review --help
```

Exit 0. Applicable workspace, repository, 1962-propers, three-document, and
external-review guidance was read before review.

```text
tools/pdf-review \
  --output build/final-cold-claude-tlm/final-candidate \
  --jobs 2 \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf
```

Exit 0. Every resulting page raster was opened with `view_image` at
`detail=original`: 31 study pages, 10 synthesis pages, and 3 homily pages.

## Exact identity and PDF structure

```text
sha256sum \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf
```

Exit 0; hashes match `HASHES.sha256`.

```text
pdfinfo <each of the three PDFs>
pdffonts <each of the three PDFs>
pdftotext -layout <study PDF> .scratch/final-cold-claude-tlm/study.txt
pdftotext -layout <synthesis PDF> .scratch/final-cold-claude-tlm/synthesis.txt
pdftotext -layout <homily PDF> .scratch/final-cold-claude-tlm/homily.txt
```

All exit 0. `pdfinfo` reports 31/10/3 US Letter pages and the expected titles,
subjects, byte sizes, and revision date. `pdffonts` reports every listed Latin
Modern font embedded, subsetted, and Unicode-mapped.

```text
rg -n -i \
  'postconciliar|novus|ordinary time|roman-missal-third|pc-s51|semi-continuous|semicontinuous' \
  .scratch/final-cold-claude-tlm/study.txt \
  .scratch/final-cold-claude-tlm/synthesis.txt \
  .scratch/final-cold-claude-tlm/homily.txt
```

Exit 1, expected: no match.

```text
rg -n '�|\uFFFD' \
  .scratch/final-cold-claude-tlm/study.txt \
  .scratch/final-cold-claude-tlm/synthesis.txt \
  .scratch/final-cold-claude-tlm/homily.txt
```

Exit 1, expected: no replacement character.

Page-splitting the synthesis text on form feed confirmed page 1's complete
inventory and single occurrences of `Literal`, `Allegorical`, `Moral`, and
`Anagogical`; page 2's sole section is `Scriptural Date and Location`; pages
3–4 are `The Propers: Themes and Movement`; page 5 begins
`The Propers: Detailed Commentary`.

## Live-source and log scans

```text
rg -n -i \
  'ordinary time|semi-continuous|semicontinuous|novus ordo|roman-missal-third|pc-s51' \
  src/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --glob '!**/evaluations/**'
```

Exit 1, expected: no match in live source. Historical evaluation packets were
excluded because they preserve superseded review prompts and findings rather
than feed the publication.

```text
rg -n \
  '^(Overfull|Underfull|!|LaTeX Warning|Package .* Warning|pdfTeX warning|Missing character)' \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.log \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.log \
  build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.log
```

Exit 1, expected: no layout report, warning, missing character, or TeX error.
The log trailers report output of 31 pages/540318 bytes, 10 pages/450164
bytes, and 3 pages/275035 bytes.

```text
git diff --check -- \
  src/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost
```

Exit 0.

## Edition gates

For every `<edition>` in `research synthesis homily`:

```text
tools/check-content-preflight \
  --provider claude \
  --document liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --edition <edition>

tools/check-proper-components \
  --provider claude \
  --document liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --phase content \
  --edition <edition>

tools/check-proper-components \
  --provider claude \
  --document liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --phase artifacts \
  --edition <edition> \
  --build-root build/claude

python3 scripts/_proper_study.py check \
  --provider claude \
  --document liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --phase content \
  --edition <edition> \
  --require-presentation \
  --require-format

python3 scripts/_proper_study.py check \
  --provider claude \
  --document liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost \
  --phase artifacts \
  --edition <edition> \
  --require-presentation \
  --require-format
```

All 15 invocations exit 0. The refreshed `research/artifacts.json` records the
three frozen hashes and current render inputs.

## Final checksum verification

```text
sha256sum -c .scratch/final-cold-claude-tlm/HASHES.sha256
```

Exit 0; all three artifacts report `OK`.
