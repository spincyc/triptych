Verdict: **PASS** for the two-file superscript compatibility repair. No actionable defect was found in the submitted repair. This is converter code review; it does not accept an active web edition, the ten historical regenerated editions, or a publication.

Review base: `8dfccbea84778e2694a47e4c1d4ea7addfcf6336`. The two reviewed subjects are `tools/web-edition` and `tools/tests/test_web_edition_conversion.py`; their exact final SHA-256 values are recorded in `final-hashes.json`. The reviewer made no changes to those subjects, source leaves, PDFs, live workflow runs, release records, indexes, or historical web files.

The underlying renderer mismatch was independently reproduced. Restoring only the base writer dialect caused `\textsuperscript{137}` to become caret-delimited Markdown, and the actual `tools/public-alpha` renderer displayed those carets rather than creating a content superscript. The final dialect at `tools/web-edition:50` disables Pandoc's superscript Markdown extension so the writer emits semantic `<sup>` tags. The owning site's renderer preserves those tags with its required, pinned Python-Markdown dependency. This changes writer representation without rewriting source content or adding a site-wide Markdown extension.

The new regression at `tools/tests/test_web_edition_conversion.py:94` runs conversion through the actual `render_page` function and covers numeric, ordinal, symbolic, escaped, and styled superscripts plus a footnote. The independent probe extended this to bold text, an explicit source link inside a superscript, and an unlinked code locator inside a superscript. All eight content superscripts retained their exact text; emphasis, strong emphasis, anchor, and code children remained semantic HTML. Escaped `a\&b` appeared as `a&b` text through a correctly escaped HTML entity. All link destinations, including footnote reference and return links, were identical before and after. No link was fabricated or dropped.

In the complete mixed-content fixture, replacing only the final `<sup>`/`</sup>` tags with the former caret delimiters reproduced the complete baseline Markdown byte for byte. A separate fixture containing headings, prose, a path, a link, and a footnote but no superscripts produced byte-identical Markdown under both dialects. Unknown macros and the previously rejected non-braced `\path` form still failed before Pandoc. These checks found no incidental content or link changes in the exercised cases.

Independent command outcomes, with fixture and temporary output under `.scratch/implementation-cold-review/web-superscripts/`:

| Check | Exit status | Result |
| --- | --- | --- |
| `python3 -m unittest discover -s tools/tests -p 'test_web_edition*.py' -v` with scratch `TMPDIR` and bytecode disabled | 0 | **75 passed; 0 failures, 0 errors, 0 skipped** |
| `python3 .scratch/implementation-cold-review/web-superscripts/probes.py` with the same environment | 0 | Eight semantic superscripts; unchanged link targets and footnote; only intended Markdown substitution; unchanged non-superscript control; two pre-Pandoc refusals |
| `git diff --check -- tools/web-edition tools/tests/test_web_edition_conversion.py` | 0 | Passed |
| Frozen subject hash comparison | 0 | Both files match the author-frozen identities |

The checks used Pandoc 3.10.2 and the site's enforced `Markdown==3.10.3` dependency. The test did not skip the actual-renderer case.

Limits: this review checks generated Markdown and the HTML emitted by the actual site renderer; it does not claim Chromium screenshot, computed-style, accessibility, complete publication-fidelity, or deployment acceptance. It exercises representative superscript constructs, not all TeX math or nested formatting. Historical output corrections remain with their separately assigned fidelity reviewer and were not regenerated or accepted here. The active TLM/NO productions were not advanced. No defect in the submitted repair required an author revision during this review.

Archive scope: `review.md`, `final-hashes.json`, and `command-outcomes.json` are public-safe review records using repository-relative paths. Raw fixture HTML/Markdown, probe scripts, diffs, and logs remain disposable scratch evidence unless separately retained.
