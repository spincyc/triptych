# GPT proper-study register revision, 23 October 2026

## Scope

The maintainer requested the recent GPT proper documents be amended as the
Claude documents were amended under the 21 October register guidance, with an
independent cold review of that guidance and publication to main. The scoped
target is the GPT 1962 Christ the King set: expansive study, concise study and
homily, plus its canonical web edition. This matching set was proposed during
clarification and selected while no older target was supplied. This request
supersedes the earlier deferral of GPT backfill for this
target, without reopening unrelated collections.

Base: `2e030b564f4413b735ddbea3061082ebe981b11a`. The workspace branch remains
`feature/propers/codex`; publication to main uses a non-force update from that
branch. Historical native run acceptance remains historical. This is a
separate register revision and makes no new native workflow acceptance claim.

## Review and verification

The original GPT set builds at 23, 10 and 3 physical pages, confirmed by
`pdfinfo` on the preserved baseline PDFs. All twelve content
preflight checks pass separately for research, synthesis and homily. These are
the comparison baseline, not evidence of register compliance.
The original full-study PDF rebuilt here is byte-identical to its currently
served canonical URL: SHA-256
`d51e0a4fb26291b9066d5dec99690bf75e9e2b7f10648a12360805407947be94`.
The initial aggregate source check stopped on three stale local Claude Christ
the King PDFs whose subjects preceded the already-published amendment. Those
unchanged approved sources were rebuilt and installed; the remaining catalogue
differences are the intended GPT revision awaiting final installation.

### Independent cold review of voice guidance

An independent read-only reviewer examined the exact base above, the
21 October register changes, their workflow routing, the existing house-voice
screen and its tests. It found no material contradiction in the new guidance:
the rule preserves necessary qualifications, requires actual connections,
distinguishes the study's inferences from source attributions, and addresses
overcorrection through its “Plain is not flat” counterweight. The deliberate
absence of a register screen is a recorded tradeoff, not a missing gate.
The house-voice suite passes 63 tests and workflow house-voice passes 72.

The review also demonstrated two precision risks in the older lexical screen,
which remain separate code follow-ups rather than blockers in this revision:

- `scripts/_house_voice.py`, source-search rule: the published source-local
  statement in Claude 1962 leaf 61 `sections/80-date-location.tex` that the
  Catholic Encyclopedia says “no trace of them is found in the Hebrew Bible”
  is refused if placed outside its protected chronology context. The actual
  publication is protected. A constructed manuscript statement ending
  “without harmonization” likewise triggers the compliance-narration rule.
- Its editor rule refuses the constructed source-edition fact “The editor
  places the missing Greek fragment after the Syriac folio.” A source editor
  is not necessarily the study's editor.

Recommended follow-up is narrow rule refinement with those source-fact
negative cases, preserving detection of identifiable publication research and
self-narration. No new register screen is proposed. The reviewer changed no
tracked files and did not claim a new theological or visual verification.

A follow-up review considered whether the allowed example “No commentary on
the Collect survives” invites strengthening a bounded negative search. It
found no contradiction or mandatory substitution: the controlling rules
preserve evidence bounds and prohibit overstatement, and “None of the three
cited commentaries discusses the Collect” passes the screen. A sentence
explicitly warning that a failed search does not establish non-survival would
clarify the example, but this is nonblocking ambiguity, not a demonstrated
unsupported claim in these documents.

The following reviews distinguish content and fidelity acceptance from
rendered artifacts and publication.

### Expansive study revision

The independent census found the developed patristic explanations largely
sound, with the register defects concentrated in introductory framing,
connecting prose, repeated classifications and closing summaries. Revision
therefore preserves the two interpretations and their actual reasoning,
replaces “reading” where it means interpretation, removes invented foils and
coverage certificates, and states the connections formerly hidden in inflated
language. Every existing footnote and source locus is retained.
The source audit confirms all 25 footnotes, quoted spans and emphasized
wording match the base, with balanced TeX braces/environments and a clean
whitespace diff. The revised research content preflight passes all twelve
applicable checks.

The first revised study builds at 22 physical pages with settled references
and no overfull, underfull or undefined-reference warnings. Independent
content/fidelity review checks Augustine's John 115.2,4, Jerome's Daniel VII,
Chrysostom's Colossians II–III and Bellarmine's Psalm arguments against the
retained witnesses and the revision against its base.

Finding `EXP-FID-001` identifies three passages that turned the Postcommunion
into a petition for present service or strength. Its actual request is that
those already nourished, who glory in serving Christ, may reign with him in
heaven. The three passages and analogous opening/map/four-senses wording are
corrected. Present perseverance remains an explicitly interpretive connection
rather than a substitute for the prayer's petition. Independent recheck closes
`EXP-FID-001` and accepts the corrected expansive content revision, with no
remaining blocker. This accepts content and fidelity only, not a native run
or the final rendered artifact.

The accepted files under the leaf's `sections/` have SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `00-opening.tex` | `ecdc960f00cbd966cddf67c97350dbb684208edafeb24a5a7fb896aed61393e5` |
| `20-commentary.tex` | `1c91b033395d32176cbc59936fbcf70b1098daf2cf9915d462f7baba741cfafc` |
| `30-hearing-king.tex` | `957c49a736689a51b633603d41d7e57289ea46bfb5762d5ef41e1de1832919ab` |
| `40-reconciled-creation.tex` | `029987c1ce86f56bfc828a225526a278983a37f95f57b1f0971093cc46198c25` |
| `50-comparison.tex` | `4a75a2ac3d3abd0d98c5fad6758d7ee89b579d86e53474b6b792f64d5d149abb` |

### Concise study revision

The concise revision derives from the accepted expansive text. It replaces
the interpretation inventories, repeated closing summaries and unsupported
contrasts with the reasoning of the appointed passages and their commentators.
The themes pages follow the Mass's texts; the later commentary compares the
arguments at their actual differences. The H5 chronology note now names the
existing source's placement near the end of Domitian's reign instead of the
production phrase “broad reign-bound”; generated dates and row keys are intact.

The revised synthesis builds at 10 pages, with inventory and overview on 1,
chronology on 2, themes on 3–4 and commentary beginning on 5. Its preflight
passes. All 23 original footnote texts and the 23 input/chronology-row/zlabel
declarations are retained exactly. Fresh independent content/fidelity review
accepts the concise revision with no material blocker or advisory. It recovers
both arguments from the concise prose alone, checks their interleaving and
retained source arguments, and confirms the actual prayer petitions and
cross-text inference attributions. It performs no new facsimile or chronology
research and grants no native-run or rendered-artifact acceptance.

Accepted hashes relative to the canonical leaf:

| File | SHA-256 |
| --- | --- |
| `sections/concise/01-inventory.tex` | `f60d210cdc1b1c7f6bc17c2db9012ccf9e131fe672bbe3708059d044f18d7023` |
| `sections/concise/02-overview.tex` | `88707d7d38d022583eb522eb79b3da5bca648b13cb683568c6a06e4221182340` |
| `sections/concise/03-chronology.tex` | `fa34e2fe633eadaf856534cba051b0bbbf6e63628cb77118343d7fcd402bc4f8` |
| `sections/concise/04-themes.tex` | `20875eacfc8ad6509d239c5a62cccfa24c1ef4dbb0d227658d02d8686298ae2e` |
| `sections/concise/10-commentary.tex` | `93c09f29e9d946db23e3af80e1852da70ce831534a5c873f0da41c013a5293ce` |
| `sections/concise/90-apparatus.tex` | `d9ef7c42ebccf75ceeb1ca0304c7f3e4a924456261eab7c66f9f06856c332e85` |
| `synthesis.tex` | `19aeb1e83c0f4bb7a69febd253c97bb74bdd3ddafee99717eb03cd2ae9b1fa01` |

### Homily revision

The spoken argument retains Augustine's distinction of origin and presence,
grace-enabled inward hearing, Chrysostom's office analogy and his argument
about peace throughout the Church. One response follows the worked example
of a resented correction: acknowledge one's own fault to the person concerned.
The stock weekly call, list of possible applications and repeated closing
instructions are removed. The terminal note identifies cross-text connections
and the correction example as the homily's synthesis and application.

The speech contains 1,259 words in Pandoc's plain-text rendering, an estimated
10.1–11.4 minutes at 110–125 words per minute. No audible rehearsal or timed
human delivery is claimed. Independent homily review accepts content,
fidelity and oral clarity with no material blocker. It checks the retained
Augustine and Chrysostom arguments, the actual prayers and both upstream
studies, confirms the word count independently, and finds no consequential
reasoning or needed attribution lost. It grants no native-run or rendered
acceptance.

Accepted hashes relative to the canonical leaf:

| File | SHA-256 |
| --- | --- |
| `sections/homily/10-body.tex` | `85e7a57feba408d0fe8d634fc4e7c9bd22f1b2e3b598d6acfdea1327f0eb24b2` |
| `sections/homily/90-apparatus.tex` | `5f2b534c6614c6b7fe21d2d2c77e7f688ab36f07dde4f292d276476ef4d00bfa` |
| `homily.tex` | `dd4ec5204788387d38668079ab2d7bf878e544a14d4ff372982851749fd93871` |

The render source is finalized at `2026-10-23T19:40:04Z`. The existing
generation provenance remains the original version-13 run; a new contribution
records this register revision without manufacturing a new engine acceptance.
### Final artifacts and web edition

A fresh independent visual reviewer opens every page at full raster size:
expansive 1–22, concise 1–10 and homily 1–3. All three are accepted without a
visual blocker. No clipping, overlap, stranded heading, sparse spill or
rights-only page is found. The concise physical opening is correct and both
themes pages contain substantive argument. The homily's two-column speech is
distinct from its page-3 source/delivery note. Final timestamps and colophons
are readable on terminal content pages. All fonts are embedded Latin Modern
with Unicode mappings; anchors and generation-metadata checks pass, and the
settled logs contain no overflow, underflow or reference warnings.

| Reviewed and installed PDF | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `f01-christ-the-king.pdf` | 22 | 474097 | `974a970bb94750e7a9bd0d31d7a36f6bdf00796f49807c407d877d2068c6dc14` |
| `f01-christ-the-king-synthesis.pdf` | 10 | 405886 | `6d169f83a6ecaaf552f3818ea907c3dd42ec9c29f359223763f5e689fdc4d676` |
| `f01-christ-the-king-homily.pdf` | 3 | 246529 | `0f6ec5744e40c8c1efbcb13d8a2cdeb2958e6a81c90ad891e7531b5db014bce3` |

Each installed mirror is byte-identical to the reviewed build. The homily's
80.3 KiB per page exceeds the 75 KiB/page investigation trigger. Inspection
finds no raster images, embedded subset Latin Modern font entries, and size
close to the 246082-byte baseline. No independent PDF optimization is made.
The other size triggers are not reached.

The page-2 visual lookup pairs John 18:33–37 with Jesus before Pilate at
Jerusalem in the governor's hall, and **Date unresolved**. The separate
composition row identifies traditional Ephesus and the disputed alternatives
c. A.D. 90–100 and A.D. 96–100; a composition date is not presented as the
trial's date. The review is screen inspection, not physical-print or
assistive-technology testing. The PDFs remain untagged. Default `pdftotext`
interleaves the homily's columns, while `pdftotext -raw` retains spoken order;
visual and print acceptance are unaffected.

An independent web fidelity reviewer accepts generated Markdown SHA-256
`b42680fe8d4c26c60230bb25db4aaa3b549994528a0845fd074017bb11adf2fb`,
compared with the accepted TeX and final full PDF. All ten sections, eleven
appointed anchors, nine chronology rows, two four-sense lists, 26 quotation
blocks, 30 notes and 66 table cells survive. It checks 603 sentence spans,
manually reconciles two interrupted by PDF page furniture, and finds no added
or lost substantive content. The locked renderer finds no duplicate IDs,
unresolved local links, raw TeX or model/provenance leakage. Timestamp and
rights notice each occur once. The reviewed Markdown is installed unchanged.

System Markdown 3.11.2 is correctly refused by the converter; conversion and
release tooling use the existing isolated environment with project-locked
Markdown 3.10.3 and PyYAML 6.0.3. No dependency lock or global environment is
changed. The web declaration's review date becomes 23 October, and reconversion
preserves the accepted Markdown hash.

The owning snapshot helpers refresh `research/artifacts.json` and
`research/web-artifact.json` to the reviewed bytes. Those are current artifact
receipts, not renewed native-run acceptance. The publication inventory and
family ledger are refreshed, preserving classification and pending family
screening. The catalogue changes only this GPT entry and its aggregate page
count. Release bindings refresh only this canonical web edition and catalogue,
plus their derived rights-table digest.

### Publication gates

All twelve content preflight checks pass independently for each final edition.
The mechanical proper-study publication check passes with presentation,
format, author standing and orientation-v2 requirements. `make
check-web-editions-current`, `make public-site`, `public-alpha verify
--deployment-target github-pages` and `make check-release-bindings` pass with
zero stale release bindings. The complete `make check-sources` aggregate also
returns 0, including `check-deployment-sources`, source graph, both publication
inventories, current catalogue, generated source/calendar/Proper/Ordinary
data, commentator coverage and family ledger. Its 162 pending family-screening
units remain honestly pending under the routine gate; no completion audit or
waiver is claimed.

The first combined Make invocation returned exit 2 because executable
subprocesses launched through `tools/tpt` selected system Markdown 3.11.2
despite the parent Make `PYTHON` override. Selecting the locked environment
through `PATH` as well fixes the invocation. The repeated web/currentness and
site build and verifier all return 0; this is an environment correction, with
no renderer, dependency-lock or document-byte change.

| Final check | Exit |
| --- | ---: |
| Three-edition PDF build, metadata, components and anchors | 0 |
| Content preflight, each of research/synthesis/homily | 0 |
| Mechanical proper-study publication check | 0 |
| `make check-sources` (includes deployment-source gate) | 0 |
| `make check-web-editions-current` | 0 |
| `make public-site` | 0 |
| `public-alpha verify --deployment-target github-pages` | 0 |
| `make check-release-bindings` | 0 |
| `tmt check`, `tpt --check`, promise validator and whitespace check | 0 |

The staged scope is the single GPT set, its current receipts and mirrors,
catalogue and derived bindings/inventories, and this review and promise
bookkeeping. No transient rasters, logs, scratch scripts, source acquisitions,
unrelated publications or native-run state enter the change. Publication to
main and verification of its resulting Actions and live artifacts remain open.
