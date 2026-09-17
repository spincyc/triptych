# Historical deployed PDF evidence restoration

Retrieved and verified on 2026-09-17 UTC. This restores absent, ignored copies of previously deployed publications; it does not constitute new content or visual acceptance.

## Result

The unchanged default `tools/check-promised-deliverables` went from exit **1** (24 diagnostics) to exit **0**: `Promised-deliverable ledger valid: 37 tracked, 27 complete.`.

Restored **20/20 PDFs**, **571 physical pages**, **132,615,843 bytes**. All 20 public requests returned HTTP 200 and application/pdf. All 20 corpus/source identity comparisons passed, and all 20 rendered generation-metadata checks exited 0. Installed copies match the downloaded SHA-256 values byte for byte. The active `propers-three-documents-2026-09-17` entry remains `in_progress`.

## Scope and verification

- Targets were parsed from the existing TOML ledger: only missing `.pdf` evidence paths in old `pass` requirements; the active new production entry was excluded. Duplicate references collapse to 20 files.
- Each public GitHub Pages URL redirected to the same relative path at `https://mystago.gy/`. Curl configuration files were disabled (`-q`); no credentials or authentication were supplied. HTTPS-only redirects, 10-second connection and 60-second total timeouts, at most three redirects and four concurrent retrievals bounded acquisition.
- Candidates stayed under this lane’s scratch directory until passing PDF signature and terminal EOF checks, successful pdfinfo parsing, exact physical-page count against the current tracked catalogue, and exact title and subject against both catalogue and source-derived preamble.
- Source-derived title and subject use `scripts/_corpus.py:title_of`, the same function used by document-library. A scoped document-library call still walked concurrent new production and reported a missing homily.tex; no unrelated source was changed to bypass that failure.
- Revision must agree between corpus.json and generation-metadata.tex, and PDF ModDate must match that UTC revision exactly. `tools/check-generation-metadata --provider PROVIDER --pdf DOCUMENT SCRATCH_PDF` additionally checks rendered provenance, text extraction, and the existing PDF metadata policy. No PDF was rebuilt or edited.
- Before byte-copy, every destination was confirmed absent, ignored and untracked; the source generation record and downloaded bytes were rehashed. Final installed SHA-256 values were then rechecked.
- Source, guidance, tools, ledger, catalogue, release records, Git index, and the six new Sunday PDF targets were not changed by this lane. No commits, pushes, deployment or task-state changes occurred.

## Inherited-error disposition

The initial 24 diagnostics comprise 22 missing-file evidence references to 20 unique PDF paths, one failed exorcism minimum-page check caused by its missing PDF, and one missing temporal-directory evidence path. Restoring the authorized existing artifacts satisfies the file checks; the 120-page exorcism PDF satisfies its existing minimum, and the temporal directory is created as an ancestor of the authorized proper-50 PDF. No requirement or validator behavior was weakened.

## Evidence and commands

`targets.json` records exact old deliverable/requirement references. `expected-corpus.json` preserves the 20 catalogue expectations used. `receipts.json` records URLs, UTC retrieval times, every exact curl/pdfinfo/generation-check command and exit status, actual and expected metadata, SHA-256, bytes, destination and installation state. `summary.json`, `before.log` and `after.log` hold numeric and raw local validation results.

Commands run from the repository root:

```sh
tools/check-promised-deliverables > .scratch/historical-pdf-restore/before.log 2>&1
# exit 1
python3 .scratch/historical-pdf-restore/restore.py
# 20 verified scratch candidates; no canonical copies written by this command
tools/check-promised-deliverables
# exit 0: Promised-deliverable ledger valid: 37 tracked, 27 complete.
```

Byte-copy was performed only after candidate verification, with exclusive-create writes and SHA-256 comparison before and after. Detailed per-candidate commands follow; public retrieval URLs and destination paths are retained without network headers or private machine paths.

| Destination | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `pdf/gpt/theology/mariology/ark-of-the-covenant.pdf` | 46 | 6856128 | `0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da` |
| `pdf/claude/theology/mariology/ark-of-the-covenant.pdf` | 65 | 1073502 | `7877add8a640a9d2f237eb149e35440bc8c392ce84fe30a24e16a03b54c3d7d0` |
| `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf` | 18 | 491184 | `e178f4527fcb61897904082758280fe2f776915649125369dbb605d5b9e1ecd7` |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf` | 18 | 512878 | `0c75179b791e4609d4dcbc090d2f5f8f9f232e2213253ff32f505dd1981277b0` |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf` | 16 | 449234 | `8c4e600d9d399c4899acda02370cca57c7634c5a58de2e79015627c9cd0f533f` |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf` | 13 | 437540 | `55f8350dadef4aad0808786a789119b698d0020334849f7e19c49115dacdc7c6` |
| `pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf` | 120 | 764589 | `960c517f9b4bf716f0f39cbccce32fbd8e49fc0aee58db8184822a8cad365fd8` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf` | 13 | 17834324 | `1d6d8e87927b671f5cbc2fe8215e80ea26a1150f92ee47084b9b6a2555668e20` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf` | 11 | 17731157 | `064698f20dae028eb9e9c77a9d2d6add68bb378125a4ac415854bddcf2260706` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf` | 11 | 17888111 | `a1c73dae1be5cdfb5c64aeb821da5858aa2bf06c1e07200f39fead0c9f6c91fd` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf` | 10 | 18059017 | `803f92f2239a6c2923b33185e7a66bbbcc9681d6c078d8ed1fa254fb6951df8f` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf` | 12 | 18099062 | `8240b82fe9f764747fdc0bf0d8005c2c4abd64c4ee17e645a8a053c8177c09a0` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf` | 16 | 24286779 | `dc0da7ba4de58bb1ca4ae5c8c8d5388164a92eae9ae6348c4095961c5d7fcd2a` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf` | 34 | 2363826 | `1338773cc10044789ffc1c76dc850d9418806823efd0d02cd3edfbfb436cb12d` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf` | 13 | 628470 | `abcd27d40cf04af3cec3be36ca67f6b0a6e480e452cade65203a186f7b004909` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf` | 30 | 2707272 | `c026383c946a4ac48a1469fb388355f25173ed90cb931dc650a356a7c57811c9` |
| `pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf` | 12 | 630490 | `b2703a930eafcfb245f987ae48b98554d5eec2dcdaff08867d105103d2eb4ad6` |
| `pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf` | 34 | 574710 | `20576607f017b22e3b01e478e561a16062b1ad35220dcc9aef868c9f19618e94` |
| `pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf` | 36 | 589947 | `98aeb73ba787c1406f63e2addeff5dc360f6f1dc6cc1c5191936e4efc5589a09` |
| `pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf` | 43 | 637623 | `972ae45194ba9cb4c5fadf676863673dd68873ac53145678ed5fae5cc5e5b734` |

## Exact per-candidate commands

### pdf/gpt/theology/mariology/ark-of-the-covenant.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf
tools/check-generation-metadata --provider gpt --pdf theology/mariology/ark-of-the-covenant .scratch/historical-pdf-restore/downloads/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf
```

### pdf/claude/theology/mariology/ark-of-the-covenant.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/claude/theology/mariology/ark-of-the-covenant.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/claude/theology/mariology/ark-of-the-covenant.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/claude/theology/mariology/ark-of-the-covenant.pdf
tools/check-generation-metadata --provider claude --pdf theology/mariology/ark-of-the-covenant .scratch/historical-pdf-restore/downloads/pdf/claude/theology/mariology/ark-of-the-covenant.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost.pdf
```

### pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf
```

### pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf
```

### pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf
```

### pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf
tools/check-generation-metadata --provider gpt --pdf history/catholic-exorcism/01-history-and-current-practice .scratch/historical-pdf-restore/downloads/pdf/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf
```

### pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf
tools/check-generation-metadata --provider gpt --pdf liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards .scratch/historical-pdf-restore/downloads/pdf/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf
```

### pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf
tools/check-generation-metadata --provider claude --pdf liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost.pdf
```

### pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf
tools/check-generation-metadata --provider claude --pdf liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost.pdf
```

### pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf

```sh
curl -q --fail --silent --show-error --location --max-redirs 3 --connect-timeout 10 --max-time 60 --proto =https --proto-redir =https --output .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf --write-out '%{http_code}
%{content_type}
%{url_effective}
' https://spincyc.github.io/triptych/pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf
pdfinfo -rawdates .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf
tools/check-generation-metadata --provider claude --pdf liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost .scratch/historical-pdf-restore/downloads/pdf/claude/liturgy/roman-rite/1962/propers/temporal/53-thirteenth-after-pentecost.pdf
```

