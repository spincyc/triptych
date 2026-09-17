# Historical web superscript fidelity review

**PASS.** No blocking finding in the ten historical web editions reviewed against commit `8dfccbea84778e2694a47e4c1d4ea7addfcf6336`. The reviewed changes are uncommitted on `feature/codex/propers/homily`; the commit remained the same through verification.

All ten editions reproduced their committed bytes with the converter loaded from that commit and their worktree bytes with the current converter. The underlying source inputs are unchanged. Each of the 47 replacements converts the former caret-delimited superscript into a semantic HTML `sup` element and preserves its payload. Reversing those replacements reproduces every original Markdown byte, including surrounding words, nonbreaking spaces, links, notes, tables, hard breaks, revision timestamps, and rights colophons.

The review separately matched all 47 superscript payloads to the assembled LaTeX source: 24 verse numbers; four manuscript suffixes; two Italian ordinal marks; one calendar-table asterisk; four quoted note markers; six French quotation/title ordinals; four indulgence-reference ordinals; and two canonical-reference ring marks. No theological, historical, legal, or liturgical proposition was changed.

The actual `tools/public-alpha.render_page` implementation rendered every before/after edition with its locked Python-Markdown **3.10.3**, site template, and actual extensions (`tables`, `sane_lists`, `toc`, `footnotes`, `attr_list`, `fenced_code`). Every new superscript is an actual `sup` node, with the correct text, order, and surrounding element ancestry. The escaped Markdown asterisk becomes `*`, not a visible backslash. Reversing only these 47 actual HTML elements reproduces the complete before HTML byte-for-byte. Existing footnote superscripts, 1,056 links, 1,280 IDs, 78 tables, 878 table rows, 2,583 table cells, and 77 hard breaks are preserved across the ten rendered pages. These counts include the rendered site shell where applicable.

The three warnings from ordinary `git diff --check` are real **exit 2** output, not a clean check: lines **415–417** of the Claude postconciliar calendar already ended in two spaces in the pinned commit. Those exact spaces remain, match explicit LaTeX line breaks, and produce the same three `br` nodes before and after rendering. Removing them would change the quoted passage's line structure. The check with only end-of-line whitespace warnings disabled exits **0**. This is a justified preservation of semantic Markdown hard breaks, not newly introduced accidental whitespace.

An independent source/closure inventory compared **220 tracked files** byte-for-byte with the pinned commit: the author's 213 protected publication-source files plus seven additional shared inputs/tool support files. All are unchanged. The author's 213 entries are source files, not a set of hashed PDFs. No PDF generation, modification, installation, or PDF fidelity claim was part of this review.

| Reviewed web file | Superscripts | Worktree SHA-256 |
| --- | ---: | --- |
| `web/claude/articles/scripture/the-linen-cloths-at-the-empty-tomb.md` | 24 | `9a6e3d2b5f072c76ff8bf905c41f6df192e56a60db6ad74bf9820a4d861381b9` |
| `web/claude/history/biblical-translations/01-septuagint.md` | 4 | `408c5dde4ff3306f12590e3f1d5754d7d395cee7f491a38c53212e4258273631` |
| `web/claude/history/traditional-priestly-institutes/01-sspx.md` | 2 | `4b243f0d4ce12ce7f22c2497ea8a28b3fd6d96b934997d493243d2d52d470975` |
| `web/claude/liturgy/roman-rite/1962/reference/liturgical-calendar.md` | 1 | `ebeda8550a97387d0b17ac6a9837d63dff34e476d9f90fa98ab6b72002b61df6` |
| `web/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/reference/liturgical-calendar.md` | 4 | `e8ab5f489b6c60415e6326a417cc13c0d79bc2a5347d678d303ca57432286546` |
| `web/claude/theology/mariology/la-salette.md` | 5 | `45a16419a5996e21018ea6543232e562f0b3e35e3adfe923eb60268ec9f6872f` |
| `web/claude/theology/mariology/lourdes.md` | 1 | `db33c3a6a2d8e360163466a35d372b57b9637688808afe1becc66b58ef35bcd2` |
| `web/gpt/theology/mariology/angelus.md` | 2 | `d892de527108ad549b3ae4d983e18d4d781dbe4ffa3186230a598a4ec9f82a3c` |
| `web/gpt/theology/mariology/la-salette.md` | 2 | `77be1cbe13b7101cae00cb41eaa3c6da905d22024fe0e22b50f23299d6b1d968` |
| `web/gpt/theology/mariology/regina-coeli.md` | 2 | `4014a9b6f3803f24b37ca3298200eb0ec8bb0d5d3a8c6ebc0db98b9a604b2f24` |

`checks.txt` records exact principal commands and numeric exits. `commands.json` contains the complete subprocess command ledger; `results.json` holds before/after subject hashes, source and rendered payloads, DOM ancestry, and per-file counts. `protected-inputs.json` records the 220 unchanged tracked input hashes. `changes.patch`, `source-loci.json`, `whitespace-check.txt`, the regenerated Markdown, and both complete rendered HTML sets provide the bounded reproduction evidence. `review.py` reproduces the checks without writing any reviewed source or publication file.

**Bounds:** this is independent acceptance of historical formatting fidelity only. It is not acceptance of any new Sunday publication, new prose, three-document workflow, or release, and it is not a full historical theological/source re-review. It establishes actual site HTML semantics, not a fresh browser screenshot, responsive-layout, assistive-technology, or full-page PDF review. No external communication, staging, commit, release edit, or publication action was performed. The coordinator owns any required consolidated handoff package and durable review disposition; this review creates no handoff ZIP.
