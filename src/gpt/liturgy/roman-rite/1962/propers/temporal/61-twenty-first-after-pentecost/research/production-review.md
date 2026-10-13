# Reviewed three-document installation

## Proper-study v11, install-publication iteration 0 — 2026-10-13

The exact installation packet has SHA-256
`faf257b1070986985f4b8e4d6a555bcb1ac80e7c582b04f826ea125dec373f60`.
The engine's recorded research, study, synthesis, homily, visual and web
reviews all returned PASS at iteration 0. Their results belong to the current
v11 production; none is inherited from the blocked v10 production below.
The visual review reports inspection of all 39 final PDF pages. The web
review reports a complete reading, bidirectional text comparison and locked
Markdown 3.10.3 HTML inspection of the canonical study, including all seventeen
appointed entries and 44 source notes. These are the reviewers' completed
events, not new source or page inspections by the installation worker.

The current artifact snapshot was checked before installation. Each normal
`make install-doc DOC=<id> PROVIDER=gpt` recipe ran with its declared
dependencies and checks, without timestamp changes or dependency suppression.
All three commands completed successfully, and each build and installed PDF
matches the exact hash accepted by visual review:

| Installed PDF below `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/` | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `61-twenty-first-after-pentecost.pdf` | 26 | 447319 | `741ab14fb48442ffaf60f2ca8dbfac866a4eb998c40697ba80bd9525c391f284` |
| `61-twenty-first-after-pentecost-synthesis.pdf` | 10 | 386743 | `17833353408ddf5abd76c6b5d0cc617bd123c8054ea99fd899e2174c5a730f4e` |
| `61-twenty-first-after-pentecost-homily.pdf` | 3 | 245077 | `39081db3f44add36ed7b5a4e99491cb3e1e96b940aa81dff8fff198543435752` |

The canonical Markdown was installed byte for byte from its accepted conversion
to `web/gpt/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost.md`
and staged as required by the publication contract. Its SHA-256 is
`0a12ed464a3838f64e9e16f2820f1f55b87cd599466058919a440701f09fbd44`.
A fresh conversion with Markdown 3.10.3 independently reproduces those bytes.
There is no companion web authority. Accepted prose, metadata, PDF snapshots,
web receipt and engine seals were preserved.

Three `make add-publication` commands created the exact bare, `-synthesis`
and `-homily` records beneath
`release/publications/gpt/liturgy/roman-rite/1962/propers/temporal/`.
Each names its own ID, `library/traditional-latin-mass.md`, status `alpha`
and standing authorization `perpetual-public-repository-2026`; PDF hashes
remain in artifact evidence, not invented release fields. The existing
Sunday 61 ChatGPT cell now links Full PDF, Synthesis PDF, Homily PDF and Read
in manifest order, with exactly one canonical publication marker. The Claude
cell and every other catalog row were preserved. The publication-wiring
checker passes, including snapshot currency, build/install identity, exact
release records, provider ownership, tracked web identity and web eligibility.

The installation evidence summary records subsequent deterministic catalog,
source-inventory, family-ledger and scoped release-binding refreshes and the
full final `make check-sources` outcome. Its native command logs remain local,
unchanged. This audit entry precedes that final refresh and check, so the check
can validate its settled bytes without a later source append invalidating them.
The terminal workflow gate, commit and push belong to the coordinator; this
entry does not claim terminal acceptance or deployment.

The actual limits remain: unspecified territory and Mass-type conditions are
preserved, source reading and collation remain bounded by the research record,
homily duration is estimated rather than a timed human delivery, and the cold
reviews did not establish physical-print use, native-browser PDF inspection,
browser appearance/click behavior or remote-link availability. No such event
is supplied by successful installation.

---

# Replacement-run final artifact preparation

## Proper-study v11, build-artifacts iteration 0

The packet SHA-256 is
`aa4c62e951db6900106c74f91e715fd5cf2d54ad2dbf788628b7017fc8e367a9`.
All three prescribed `make doc` commands completed using normal declared
dependencies. The settled shared revision is `2026-10-13T07:54:09Z`.
No layout, semantic source, research, generation declaration or content-review
seal was changed by this stage.

The current run's four completed review results are PASS. Freshly computed
research, study, synthesis and homily input seals match their native v11
receipts exactly, including the research computation fields. The respective
file maps contain 1,740, 17, 14 and 9 entries; the computation fields are
additional to the research file map. No stale acceptance or upstream owner
repair was found.

## Final outputs and checks

All outputs are beneath
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`:

| File | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `61-twenty-first-after-pentecost.pdf` | 26 | 447319 | `741ab14fb48442ffaf60f2ca8dbfac866a4eb998c40697ba80bd9525c391f284` |
| `61-twenty-first-after-pentecost-synthesis.pdf` | 10 | 386743 | `17833353408ddf5abd76c6b5d0cc617bd123c8054ea99fd899e2174c5a730f4e` |
| `61-twenty-first-after-pentecost-homily.pdf` | 3 | 245077 | `39081db3f44add36ed7b5a4e99491cb3e1e96b940aa81dff8fff198543435752` |

The artifact and component checks pass, including the presentation, shared
format, author-standing and orientation contracts. Settled concise auxiliary
markers place inventory and all four sense rows on physical page 1,
chronology on 2, themes on 3–4 and developed commentary on 5. The native
auxiliary and logs are retained beside exact copies of the final PDFs.

All three settled TeX logs have no warnings, overfull or underfull boxes,
undefined references, missing characters or fatal errors. The `infwarerr`
package's descriptive banner is not a warning. The normal builds validate
metadata and navigation; the study and concise navigation reports resolve
57 and 14 contents entries respectively. Poppler parsed and extracted every
PDF, reported unencrypted Letter-size PDF 1.7 with no suspect structure,
JavaScript or embedded attachments, and the review helper rasterized every
page successfully. All 14 study, 15 concise and 10 homily font rows are
embedded, subset and Unicode-mapped Latin Modern. Every extraction contains
one final revision timestamp, no unresolved question-mark marker and no
replacement character. Study and concise extracted text match their accepted
v11 proofs exactly after substituting only the revision timestamp; the homily
is byte-identical to its accepted proof.

The study and concise files are 16.80 and 37.77 KiB per page. The homily's
79.78 KiB per page crosses the size-review trigger: inspection found a small
245,077-byte three-page PDF with ten embedded font rows and no raster images.
It is retained without source-independent PDF optimization. None exceeds
1 MiB.

## Snapshot, rasters and locator confirmation

The prescribed snapshot command wrote `research/artifacts.json`, SHA-256
`d26470d08971982c593f4b704935f0bf311def792b6afec3f419b534ba9a0271`.
It binds the three PDF hashes, render-input hashes and settled pagination
auxiliaries. The approved `tools/tpt pdf-review` generated all 39 full-page
rasters in
`build/tpt-runs/ed4bc29b18cf1150/artifacts/build-artifacts-0000/rasters/`.
The helper's native receipt is unchanged; logs and other evidence are outside
that replaceable child.

The worker opened the final concise page 2 and study pages 24–25. SYN-001's
corrected pointer visibly reads **Matthew, p. 24**. The final study's entire
Matthew subsection, both paragraphs and its footnote 43 occupy physical
page 24; Ephesians begins physical page 25. The shared finalization timestamp
has therefore not invalidated that locator. No change was needed.

`build-summary.json` in the stage evidence directory is an original compact
public summary, explicitly not a normalized native receipt. Native helper
receipts, logs and operational reports remain unchanged local evidence;
public-candidate and local-only boundaries are recorded separately. This stage
claims artifact preparation and the targeted locator inspection, not the next
worker's complete cold visual review or a new source collation. Shared source
inventory and document-catalogue refresh remain publication-owner work. No
PDF was installed, no workflow was advanced, and no staging, commit or push
was performed. All stage-started subprocesses completed.

---

# Replacement-run homily author verification

## Proper-study v11, derive-homily iteration 0

The fresh high-effort GPT-6 author read the complete packet, SHA-256
`c1fb0b0f2646421152843df513d30efaf1008974e667e1b06c6a17f52ce2d06f`,
and both reviewed studies in full: the 26-page expansive proof, SHA-256
`878b887f73817f3a5d28100248efd6988f19bd7be262fffd7a8cfbaf7a2a524f`,
and the 10-page concise proof, SHA-256
`ac9b8f56e6982d2da2ebeb7312d4bb5ce5ae342cba84f83f3383b1c6e83cee1d`.
The homily entrypoint, spoken body and terminal apparatus were retained after
independent comparison with those arguments and their evidence. No earlier
production verdict supplies this stage's judgment. The shared generation
record preserves the exact v11 provenance and adds this contribution; the
current finalization timestamp is `2026-10-13T07:54:09Z`.

The speech develops the first reading, mercy received and given. Its decisive
detail is Matthew 18:26,29: the second servant repeats the first servant's
own plea. The contrast between complete remission received and even a delay
refused changes the listener's question from what the neighbor owes to what
received mercy requires. Ephesians 6:12,15 then exposes revenge against a
human neighbor as a misdirected spiritual battle; the Collect's continuing
mercy, Secret's saving initiative and Postcommunion's inward fruit carry the
argument through the Mass. Job's uprightness retains the studies' distinction
between culpable refusal and a sufferer's pain. Replacing these texts with
unrelated readings would remove both the repeated-plea inference and the
armor-for-peace connection, rather than merely change an illustrative verse.

## Oral sense and evidence checked

A fresh textual rehearsal followed all twenty paragraphs in their spoken
order, checking antecedents, sentence length, transitions and the return to
the opening plea. The narrative establishes the first gift before the second
encounter; the warning leads into Aquinas's distinction without cancelling
judgment; the pain/correction paragraph prevents an accusation against the
injured; the practical response grows out of the grip image; the final
movement returns to received help and the neighbor outside the church.
The speech remains continuous prose, with natural attributions and no inline
apparatus, stage directions, invented experience or closing recited prayer.
No wording change was needed in this pass.

The recomputed count is **1,257 spoken words**, retaining internal apostrophes
and hyphens and excluding title, terminal apparatus and metadata. At
110–120 words per minute this is **10.5–11.4 minutes before pauses**, or
approximately **11–12 minutes with brief pauses**. The 1,257 tokens match
the PDF's raw extraction in order after removal of running matter and
normalization of typographic ligatures and discretionary line hyphens.
This is an estimated duration and textual oral-clarity review, not an audible
or timed human delivery.

The author reread Chrysostom's Matthew LXI §§1–4 and the opening of §5,
Augustine's Sermon 83 §§1–8, Chrysostom's Ephesians XXII exposition through
the spiritual-conflict moral discussion, Aquinas III q.88 aa.1–2, and
Schuster III pp.178–181 in their retained textual witnesses. The exact
Gospel quotations and prayer explanations were checked against the canonical
appointed-text collation and both studies. Chrysostom supports the gift
exceeding the request and the repeated plea; Augustine supports the
debtor/creditor identity and inward pardon with correction; Aquinas preserves
real remission alongside new culpability; Schuster supports reception's claim
upon mind, heart and will. These are bounded readings of historical
transcriptions and, for Schuster, OCR. No new facsimile collation, acquisition,
research sweep or independent re-verification of the full research dossier
is claimed. No upstream defect requiring repair was identified.

## Fresh proof and checks

The proof is
`build/tpt-runs/ed4bc29b18cf1150/artifacts/derive-homily-0000/homily-proof.pdf`:
**3 Letter pages**, **245077 bytes**, SHA-256
`39081db3f44add36ed7b5a4e99491cb3e1e96b940aa81dff8fff198543435752`.
It is byte-identical to the checked build.

- Homily `make doc`, artifact component checking and complete homily content
  preflight passed, including 34 source bindings and five used references.
  Both contents anchors resolve. The settled TeX log has no warning,
  overfull/underfull box, undefined reference, missing character or error.
- Every page was individually opened as a full-page raster generated by
  `tools/tpt pdf-review` in this stage's dedicated `rasters/` child. Pages
  1–2 contain the full-width title followed by the two-column speech; page 3
  contains the source/delivery note, References, revision and rights colophon.
  No clipping, collision, stranded heading or illegible type was observed.
- All ten font rows are embedded, subset and Unicode-mapped Latin Modern.
  The PDF has no creation date or JavaScript; its modification date agrees
  with the revision. Extracted speech matches the source as described above.
- `make check-sources` exited 2 on shared document-catalogue drift and stale
  publication-inventory hashes. Source-library validation passed, including
  3815 bindings. The shared projections remain the later publication owner's
  work and were not changed here.

## Ownership and handback boundary

Only `generation-metadata.tex` and this production record changed in this
stage; the independently inspected homily sources were retained unchanged.
Accepted research, study and concise sources, shared source owners and code
were not edited. The stage evidence holds exact PDF, auxiliary, log, extraction,
font and metadata bytes plus page rasters. Compact original JSON summaries
explicitly identify public candidates; native logs, auxiliary, helper receipts
and cache remain unchanged local operational evidence. No sanitized native
receipt is offered as an original.

This is author verification, not cold homily acceptance. The final family
build must settle common metadata and recheck all three outputs. No install,
staging, commit, push or workflow advancement was performed. All author-started
subprocesses completed; no server or background process remains running.

---

# Replacement-run concise author verification

## Proper-study v11, derive-synthesis iteration 0

The fresh high-effort GPT-6 author read the complete packet, SHA-256
`6188e5fcc89ddfcdc84fe142f216a576528a8795336a172841b7f219611271f0`,
and compared every concise component with the complete accepted 26-page
expansive proof, SHA-256
`878b887f73817f3a5d28100248efd6988f19bd7be262fffd7a8cfbaf7a2a524f`.
The current context, scope, interpretations and generated chronology were
also inspected. No previous author or reviewer verdict supplied this judgment.

The existing concise argument was retained after that comparison. Its five
questions interleave received mercy and protected pilgrimage: the gift creates
an obligation to forgive, while real deliverance begins a journey requiring
perseverance. Aquinas's later distinctions remain distinct from the Fathers'
preaching; Chrysostom's disputed Ephesians readings and Schuster's present
judgment remain beside the other witnesses' answers. Job's innocence, the
limits of a modern sufferer's diagnosis, correction alongside forgiveness,
conditional mission and Luke prayers, and each reading's spiritual senses
survive compression. No new evidence-dependent claim was added.

SYN-001 was corrected by checking the current proof: Matthew's complete
historical subsection and its source note occupy physical page 24; Ephesians
begins page 25. The concise page-2 pointer now says Matthew, p. 24. The nine
generated chronology rows, short sourced contexts and row spacing were
retained. The other expansive page pointers were checked against the same
proof. The shared generation record preserves the exact v11 provenance and
adds the actual contribution; the finalization timestamp is
`2026-10-13T07:20:51Z`. The already conforming manifest required no change.

## Concise proof and actual checks

The proof is
`build/tpt-runs/ed4bc29b18cf1150/artifacts/derive-synthesis-0000/synthesis-proof.pdf`:
10 Letter pages, 386743 bytes, SHA-256
`ac9b8f56e6982d2da2ebeb7312d4bb5ce5ae342cba84f83f3383b1c6e83cee1d`.
The recomputed substantive count is 4135 words: inventory 242, overview 70,
themes 978, developed commentary 2845. English-alphabet tokens retain internal
apostrophes and hyphens; headings are included, while footnotes, TeX commands,
marker arguments, chronology and terminal apparatus are excluded.

- The requested synthesis `make doc` and artifact component check passed.
  The settled auxiliary places inventory and all four overview senses on
  physical page 1, chronology on 2, themes on 3–4, and commentary on 5.
  All 14 contents anchors and generation checks passed.
- Complete synthesis content preflight passed: 34 bindings, current chronology,
  nine exact orientation rows, two declared interpretations and used references.
- The settled TeX log has no warnings, overfull or underfull boxes, undefined
  references, missing characters or fatal diagnostics. All 15 font rows are
  embedded, subset and Unicode mapped. The PDF has no creation date or
  JavaScript; its modification date agrees with the revision.
- The approved `tools/tpt pdf-review` generated the ten page rasters. Every
  page was individually inspected. Page 2 pairs each passage with its subject,
  place and alternatives legibly; the Matthew locator reads p. 24. The Exodus
  interval ends at Temple construction, David's era remains attribution,
  and the Galilean teaching event remains separate from Gospel composition.
  Pages 3–4 contain substantive movement; pages 5–9 deepen the comparison;
  page 10 contains references, timestamp and the readable rights colophon.
  No clipping, overlap, broken table or stranded heading was observed.
- `make check-sources` exited 2 on shared document-catalogue drift and stale
  publication-inventory hashes, including the changed concise chronology and
  other current owner changes. Source-library validation passed. The shared
  projections belong to the coordinator's later reconciliation and were not
  changed by this author.

## Concise evidence and ownership boundary

The stage evidence directory retains exact PDF, auxiliary and TeX log bytes,
extracted text, metadata/font reports, word count and publication rasters.
Its compact `author-evidence.json` and `evidence-boundary.json` are original
public summaries and candidate inventories, not native tool receipts. Native
logs, auxiliary, helper receipt and cache remain unchanged local evidence.
No historical source collation, new source acquisition or cold acceptance is
claimed. Accepted research and study prose were not edited. The final family
build must recheck the cross-document pointers after shared metadata settles.
No installation, staging, commit, push or engine advance was performed.
All author-started subprocesses completed; no server or background process
remains running.

---

# Replacement-run study author verification

## Proper-study v11, author-study iteration 0

This fresh high-effort GPT-6 worker read the complete current packet, SHA-256
`464001aa2bbc5b973602f7fca5b947b68b8bc7240f8a30ab1dfd4006a0f68476`,
for run `ed4bc29b18cf1150`. The records below this section describe the old
v10 run; their verdicts do not constitute acceptance of this replacement run.
The present result is an author-stage proof, pending the real content gate and
independent cold review.

The existing manuscript was independently read against the current reviewed
context, scope, source plan and interpretations. Its two complete arguments
remain distinct: received pardon calls for mercy, and received deliverance
sustains an unfinished pilgrimage. The 17 appointed elements, historical
English qualifications, conditional mission and St Luke prayers, all four
senses in each reading, source differences and historical appendix remain
substantively intact. Focused primary-text rereading included Chrysostom's
Matthew LXI and the Ephesians XXII passage on 6:9, Augustine's Sermon 83 and
Psalm 118 Caph, Gregory's permission/malice and without-cause distinctions,
Aquinas's treatment of returning sins, and Schuster's Sunday exposition.
This was not a new full facsimile collation or a replacement research review.
The existing Ephesians 6:9 connection to Matthew 18:32 is correctly identified
as reception of the preceding verse, not as whole-Mass patristic commentary.

All 17 `proper-*` labels now immediately follow their own appointed-text
headings. The already conforming component manifest was retained; only its
extra blank EOF line was removed. The appointed-text and commentary files
also received only authorized EOF whitespace cleanup beyond the new labels.
Generation metadata records this v11 run, packet workflow digest, seed commit
and current author contribution; its revision is `2026-10-13T06:44:25Z`.
Web eligibility was reinspected on 2026-10-13. That declaration and the author
conversion probe are not web acceptance receipts.

## Proof and checks

The current proof is
`build/tpt-runs/ed4bc29b18cf1150/artifacts/author-study-0000/study-proof.pdf`:
26 Letter pages, 447319 bytes, SHA-256
`878b887f73817f3a5d28100248efd6988f19bd7be262fffd7a8cfbaf7a2a524f`.
The substantive core contains 7233 words by the documented token method:
opening 651, commentary 2088, mercy reading 1983, pilgrimage reading 2193,
comparison 318. Appointed quotations, historical appendix and terminal
apparatus are excluded; the four-senses summaries are included.

- `make doc` passed, including all 57 contents anchors and generation checks.
- Research-edition artifact component checking and content preflight passed.
  Preflight validated 34 bindings, both lanes and the current chronology
  apparatus, including nine complete orientation rows.
- The author web probe passed. All 17 Markdown anchors were individually
  matched to their source headings; the converter's rendered-target audit
  passed. Probe Markdown SHA-256:
  `f317bc98ce51aca0cc291c5d8c1fa2f205b9fb6d9c2991bf76f931cf5f17b479`.
- The final TeX log contains no warnings, overfull/underfull boxes, undefined
  references or missing characters. All 14 font rows are embedded, subset
  and Unicode mapped. Poppler reports unencrypted PDF 1.7, no JavaScript,
  no creation date, and the expected revision modification date.
- Every page has extracted text without unresolved-reference or replacement
  markers. The current revision and rights colophon appear on page 26.
- The approved `tools/tpt pdf-review` helper generated all 26 full-page
  rasters. Each page was inspected individually: opening and branch table
  (1–2), appointed texts (3–10), commentary (10–14), mercy reading (14–17),
  pilgrimage reading (18–21), comparison (22), chronology table and discussion
  (23–25), qualifications and references (25–26). No clipping, overlapping
  matter, broken table, stranded heading or illegible footer was found.
  Sparse lane endings and the comparison page are deliberate section breaks.
- `make check-sources` reached the known shared document-catalogue drift in
  `src/web/data/structure/documents/corpus.json` and exited 2. That projection
  belongs to the later coordinator stage; it was not changed in this lane.

## Evidence and ownership boundary

The evidence directory above retains the proof, extraction, font and metadata
reports, verification facts, author web probe and approved-helper rasters.
`evidence-boundary.json` allowlists public candidates and records their hashes.
Native command logs, the TeX log and auxiliary, helper receipt, cache and any
unlisted files remain local operational evidence; no native receipt was
silently rewritten. Public candidate text and PDF text/metadata were screened
for host paths and process identifiers. Publication rasters contain only the
reviewed pages. These are review candidates, not installed artifacts.

Accepted research and shared source evidence were not edited. Companion
manuscripts, old archives and seals remain outside this author's changes.
No install, staging, commit, push or engine transition was performed. All
build/check/render subprocesses finished; no server or background process
was left running.

---

# Final three-document artifact build

## Build-artifacts iteration 0

The fresh GPT-6 worker at high effort executed the complete proper-study v10
packet for run `a72731c5491066a3`, SHA-256
`0de56b683e35a6da261dd2131289b4838c83e4af51ebb3b4510fe6795f22110b`.
All three required `make doc` invocations passed with the current shared
render-source revision `2026-10-13T04:24:11Z`. The study and concise study
were recompiled; Make correctly reused the current homily PDF. No accepted
prose, research, layout source, generation declaration, or content seal changed.

The build directory is `build/gpt/liturgy/roman-rite/1962/propers/temporal/`.
Its exact final outputs are:

| PDF filename | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `61-twenty-first-after-pentecost.pdf` | 26 | 447318 | `53a30dd4b8d95831a3540252484508c8ef3c28792a9e05e19032a78ba809635d` |
| `61-twenty-first-after-pentecost-synthesis.pdf` | 10 | 386752 | `ccb26a8cc49035b06ecfe6067679b6eef4c7d318ec59f45152bfccd1f49af325` |
| `61-twenty-first-after-pentecost-homily.pdf` | 3 | 245076 | `cf59a2d2cd49c33189a55712761da1934c1e0ed909284e5a6d9622f775dc9e17` |

The required snapshot command produced `research/artifacts.json`, SHA-256
`9cdfa0bfa5d687e3b8f71b8aa512b48b639d7563025cb91b4e5e620f37d0e1a9`.
It records the actual PDF bytes, render inputs and pagination auxiliaries;
it is not an approval or a claim of visual review.

## Settled checks and retained evidence

Evidence is retained beneath
`build/tpt-runs/a72731c5491066a3/artifacts/build-artifacts-0000/`.
The `study-final.pdf`, `synthesis-final.pdf` and `homily-final.pdf` copies
are byte-identical to the outputs above. Their matching auxiliaries,
PDF metadata, font reports, layout and raw extractions, diagnostic summaries,
snapshot copy and `verification.json` accompany them outside `rasters/`.

- The complete artifact component check passes. All 13 concise zref markers
  settle on the required physical pages: inventory, overview and its four
  sense rows on 1; chronology on 2; themes start on 3 and end on 4;
  commentary starts on 5. The study and concise extents meet their ranges.
- All three native final TeX logs were checked for fatal diagnostics,
  warnings, overfull/underfull boxes, undefined references and missing
  characters: none was present. The concise auxiliary SHA-256 is
  `2bfdb9c12bb938b301e7352611b4e71ea54209a60b8fbb193cab564204c643b1`;
  its native log SHA-256 is
  `3979b3ff6373c33187f3db3bbad33ee85687cf33d54e989589616f9764298106`.
- The repository anchor checker passes all 57 study, 14 concise and 2 homily
  contents anchors. Poppler reads all PDFs as unencrypted PDF 1.7, Letter
  pages, with no JavaScript. Every font is embedded, subset and Unicode-mapped
  Latin Modern: 14, 15 and 10 font rows respectively. PDF modification dates
  match the shared revision; creation dates are absent.
- Every extracted page contains text, with no unresolved-reference or
  replacement-character marker. Layout extraction matches each respective
  final author proof exactly after normalizing only the revision timestamp.
  The concise opening and terminal matter were also inspected in extraction.
  The 1,257 homily spoken tokens match the source in order after removing
  running matter and normalizing line-break hyphenation and ligatures from
  raw extraction. Each PDF displays the current revision once and retains
  the rights colophon on its final page.
- `tools/tpt pdf-review` completed successfully in the dedicated `rasters/`
  child and produced all 39 full-page rasters. The sanitized public raster
  evidence has SHA-256
  `c63b254f81dff51ea3a010d05cc76ad2b6dbb23ee23c913971b9dad9b4c5d464`.
  It explicitly identifies its native receipt hash and allowlist derivation;
  native helper receipts and original logs remain local operational evidence.
  The files named `*-log-diagnostics.sanitized.txt` are diagnostic-only
  derivatives, not complete native logs. `public-evidence.sha256` binds these
  public derivatives and the other retained evidence. Public text evidence
  was screened for machine-specific path prefixes.

## Boundary and remaining work

This stage performed no fresh source verification and gives no cold visual
verdict. The separate visual worker must inspect every final page. Neither
`qpdf` nor `mutool` was available; structural checks used Poppler metadata
and extraction, repository anchor validation and successful all-page rendering.
The known aggregate document-catalogue drift remains a downstream publication
responsibility; this worker did not rerun or modify that global wiring.

Only this production audit and the tool-generated artifact snapshot changed
under the canonical leaf. All build, check and raster processes completed;
no background process remains. No installation, staging, commit, push or
workflow advancement was performed.

# Homily: author verification

## Current proof: derive-homily iteration 0

The fresh GPT-6 author at high effort completed the homily for proper-study
v10, run `a72731c5491066a3`, from the complete packet SHA-256
`c9d297825dc00025e30ba91adfdca862238f7172e88ac9220f95d7e9f3a13e74`.
Both accepted studies and their research arguments were read directly.
Their prose and research remain unchanged. The shared generation record
adds the actual homily contribution and records render-source revision
`2026-10-13T04:24:11Z`.

The finished speech, **The Words He Would Not Hear**, addresses an adult
parish assembly and develops the `mercy-received` reading. Its decisive
detail is the repeated plea for patience in Matthew 18:26,29, followed by
the deliberate refusal in verse 30. The king gives more than the first
servant requests; that recipient refuses even what his companion requests.
The listener's governing question therefore changes from what another owes
to what received mercy requires. The Epistle's exclusion of flesh and blood
as the ultimate enemy and the Postcommunion's inward fruit develop that
same argument. Job's initial uprightness prevents identifying every wounded
person with the condemned servant. Aquinas's real-pardon/new-culpability
distinction preserves the warning without making prior remission unreal.

The spoken component contains **1,257 words**, counted as alphabetic word
tokens with internal apostrophes and hyphens retained. Title, apparatus,
references and metadata are excluded. At 110–120 words per minute, the
estimate is **10.5–11.4 minutes before pauses**, approximately **11–12 minutes
with brief pauses**. A textual rehearsal checked sense, transitions, sentence
length, and oral clarity; one cumbersome sentence about completed pardon
was divided into two short sentences. No audible or timed human rehearsal,
personal experience, clerical identity, or new received prayer is claimed.

## Homily proof and checks

Evidence is retained under the repository-relative directory
`build/tpt-runs/a72731c5491066a3/artifacts/derive-homily-0000/`.
The proof `homily-proof.pdf` has **3 pages**, **245,076 bytes**, and SHA-256
`cf59a2d2cd49c33189a55712761da1934c1e0ed909284e5a6d9622f775dc9e17`.
It is byte-identical to the checked build. Speech occupies pages 1–2;
source/delivery note, References, revision and rights share page 3.

- `make doc` passed, including generation metadata and individual contents
  anchors. The settled TeX log has no warning, overfull/underfull box,
  undefined reference, missing character, or error.
- The homily artifact component check and complete homily content preflight
  passed. The latter validates 34 bindings and five used reference entries.
  The existing manifest already declared both homily components, so no
  manifest change was needed.
- Every page was opened as a full-page raster produced by `tools/pdf-review`
  in the dedicated replaceable `rasters/` child. The full-width title,
  two-column speech, running head, separate terminal page and compact rights
  colophon were inspected. No clipping, collision, stranded heading or
  illegible text was observed. Font inspection found embedded, subset,
  Unicode-mapped Latin Modern fonts; PDF structure reports Letter pages.
- The 1,257 spoken tokens match the PDF extraction in order after title,
  running heads and page numbers are removed. This comparison uses
  `pdftotext -raw`: its default extraction interleaves the two columns.
  Source whitespace checks passed. Proof logs have workstation prefixes
  removed; native raster-helper cache receipts are operational artifacts,
  not public evidence.
- `make check-sources` was run and exited 2 at `check-document-catalogue`:
  the generated document catalog has drifted from the completed sources.
  The tool requests `document-library structure`. This shared catalog belongs
  to the coordinator/publication owner and was reported for reconciliation;
  the homily author did not change it or the shared source inventories.

## Homily evidence and handback limits

The author directly read the accepted appointed texts and evidence maps,
Chrysostom's relevant Matthew LXI exposition (especially §§3–5),
Augustine's Sermon 83 §§1–8, Aquinas III q.88 a.1 and a.2's answer, the
relevant spiritual-conflict passage of Chrysostom's Ephesians XXII, and
Schuster's Secret/Postcommunion discussion on p.181. These were readings
of retained historical-text witnesses, including Schuster's OCR, not new
facsimile collations or a new exhaustive research sweep. The accepted
Missal collation and source limits remain controlling. No new source-dependent
claim, upstream defect, or shared-code repair was introduced.

Only the homily entrypoint, its two local components, the shared generation
record and this production record changed in this stage. All author-started
build, check and raster processes completed; no background process remains.
No staging, commit, push, installation or workflow advancement occurred.
Cold homily review, the final build of all three documents with the shared
timestamp, and the remaining independent artifact and publication reviews
remain required. This proof is author verification, not their acceptance.

# Concise study: author verification

## Current proof: derive-synthesis iteration 0

The fresh GPT-6 author at high effort derived the concise comparison for
proper-study v10, run `a72731c5491066a3`, from the complete packet SHA-256
`47ca5e8860547fe897d80744e622e57dfa403c09c13d5f758a21c5763f212b0b`.
The shared generation record preserves the workflow digest and seed commit,
adds the actual contribution, and records final render-source revision
`2026-10-13T03:56:10Z`.

The proof contains **10 physical pages** and **4,135 substantive words**:
inventory 242, overview 70, themes 978, and developed commentary 2,845.
The count uses English-alphabet word tokens with internal apostrophes and
hyphens retained. It includes headings and sense distillations but excludes
footnotes, TeX commands and marker arguments, generated chronology and its
historical notes, terminal apparatus, and generation metadata. It adapts the
existing study-author counting procedure; this is a prose count, not a count
of every printed token.

All seventeen dated or conditional inventory elements are present. The
mission and St Luke conditions retain their distinctions. The two accepted
whole-formulary readings are compared through questions of release, renewed
judgment, protection, sacramental food, and the Church's petition for judgment.
The comparison preserves the difference between innocent Job and the guilty
servant; Aquinas's distinction between completed remission and new liability;
Gregory's distinction between evil intent and bounded permitted power; the
historical editor's disagreement with Chrysostom; and Schuster's present
privation beside Augustine's and Bellarmine's final expectation. The later
commentary develops the witnesses' reasoning rather than repeating the opening.

## Retained proof and physical evidence

All paths below are relative to the repository. The proof directory is
`build/tpt-runs/a72731c5491066a3/artifacts/derive-synthesis-0000/`.

- `synthesis-proof.pdf`: 386,752 bytes; SHA-256
  `873a34706aeb564af9f308632dd120350c10d2930b56440438742621f06da7ab`.
- `synthesis-proof.aux`: 5,083 bytes; SHA-256
  `2bfdb9c12bb938b301e7352611b4e71ea54209a60b8fbb193cab564204c643b1`.
- `synthesis-proof.log`: 44,334 bytes; SHA-256
  `ae535e28d9643abbc527e816954e9c856b42b386c3b41371c77beb4433389c14`.
  Workstation prefixes were removed from this retained log; the original
  build log's SHA-256 is
  `6e28900e95738fd43d6be23f50e9fedffd55f4b51ccd64cdff528459b9fd20ab`.
  Diagnostics were checked against the original log before sanitization.

The auxiliary markers place inventory start/end, overview start/end, and all
four individual sense rows on physical page 1; chronology start/end on page 2;
themes start on page 3 and end on page 4; and commentary start on page 5.
The scope occupies page 9; References, revision and rights occupy page 10.
The PDF and auxiliary copies are byte-identical to the checked build.

Every final page, 1–10, was opened as a full-page raster generated by
`tools/pdf-review`, beneath the dedicated replaceable `rasters/` child.
No clipping, collision, stranded heading, broken table or illegible footnote
was observed. Page 2 was also checked as a reader's orientation table at
ordinary full-page size: the Gospel event and composition remain separate,
the Exodus interval remains distinct from Psalm composition, and the Davidic
attribution remains conditional. Modest spacing separates the nine row calls.
Short place phrases preserve the actual dated subjects; adjacent notes give
precise expansive-appendix pages and sources. No page-reference command enters
a row argument and no generated date, alternative or relation label changed.

## Actual checks and limits

- The required `make doc` completed successfully. All 14 contents anchors
  resolve. The synthesis-edition artifact component check and all twelve
  content preflight checks pass, including 34 bindings, nine generated
  chronology rows, current canonical chronology, five used reference entries,
  both interpretive lanes, rights and house voice.
- The original final TeX log contains no warning, overfull/underfull box,
  undefined reference, missing character or error. `pdfinfo`, `pdffonts`,
  text extraction and `git diff --check` pass. Pages are US Letter; all
  Latin Modern fonts are embedded, subset and Unicode-mapped. The visible
  revision matches the shared metadata. PDF extraction contains no unresolved
  page-reference marker.
- `make check-sources` was run and exits 2 after validating the reusable
  source library, including 3,815 bindings: the document catalogue requires
  the future declared `homily.tex`. The synthesis-stage artifact gate passes.
  This is a downstream dependency; no placeholder or shared-code edit was made.

The author read the accepted expansive text and canonical research directly,
including the chronology and its evidence bounds. Aquinas III q.88 aa.1–4 was
also reread in the retained English transcription for the technical account of
remission and renewed liability. This was not a new facsimile collation or a
new research sweep. Other source-verification limits remain those of the
accepted research and expansive-study records. No new evidence-dependent claim
or upstream defect requiring repair was identified.

Changed files are `synthesis.tex`, the six declared files under
`sections/concise/`, `generation-metadata.tex`, and this production record.
The existing manifest already declares their correct mode membership and
presentation owners and did not require editing. Accepted research, expansive
prose, generated chronology, source owners and shared code were not edited.
All author-started build, check and raster processes completed; no background
process remains. No staging, commit, push, installation or workflow advancement
was performed. This is author verification only: fresh concise review, homily
production, the final three-document build and independent reviews remain
required after the shared generation metadata has settled.

# Expansive study: author verification

## Current proof: author-study iteration 2

The fresh GPT-6 author at high effort reconciled the historical appendix with
the corrected research account, from packet SHA-256
`7f9dfc8f86a5c68f08b25b7b83924369ec3d2840bc0395ed5421f11a32eaafc2`.
Haydock's three reported conjectures now distinguish David instructing young
Solomon, David writing under Saul's persecution, and Daniel consoling the
captives. The Davidic chronology remains conditional and does not date the
Psalm's occasion or verse 81. Augustine's Mosaic-authorship caveat now cites
Psalm 89 §2 (NPNF Psalm 90). No generated date, source-owned qualification,
appointed text, or core argument changed. The final render-source revision
is `2026-10-13T03:24:49Z`.

The final author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0002/study-proof.pdf`:
**26 physical pages**, 447,319 bytes, SHA-256
`324c562aebd7ba283666721403b192f9a2a9fda11a43cb063e720192b21553aa`.
The iteration 1 and iteration 0 records below describe their earlier bytes.

- The required `make doc`, research-edition artifact component check, and
  complete research-edition content preflight passed. All 57 contents anchors
  resolve. The settled TeX log has no warning, overfull/underfull box, undefined
  reference, missing character, or error. The preflight validates all nine
  generated chronology rows and their currency, 34 source bindings, and
  14 used reference entries.
- The existing text-comparison/count procedure was rerun. All 17 Latin and
  17 English displayed bodies still match the collation under its documented
  formatting normalization; the unchanged core exposition has **7,233
  substantive words**, counted by the method below.
- Every final page, 1–26, was opened as a full-page raster from
  `tools/pdf-review`. No clipping, collisions, broken table, stranded heading,
  or illegible footnote was observed. Page 24 contains the corrected paragraph
  and Augustine locator; the chronology and references retain their previous
  page locations. The revision and rights colophon fit on page 26.
- PDF structure, extracted text, fonts, source whitespace, and the proof's
  byte identity with the checked build were checked. The proof has Letter
  pages and embedded/subset/Unicode-mapped Latin Modern fonts, one visible
  revision, and no unresolved page-reference marker.
- `make check-sources` validates the reusable source library, including
  3,815 bindings, then exits 2 because the document catalogue requires the
  declared future `homily.tex`. The study-stage artifact gate passes. This
  remains a later-stage dependency; no placeholder or shared-code repair was
  made.

The author read the current research evidence directly and inspected the
previously acquired Haydock facsimile images of printed pages 780–781
(PDF pages 816–817). Page 781 confirms the three conjectures and general
Davidic attribution. This was a fresh visual inspection of those retained
images, not a new download or whole-artifact hash verification. The author
also read Augustine's Psalm 90 §§1–3 directly in the retained NPNF/CCEL
transcription: §2 contains the authorship caveat. That reading was not a
fresh print-edition collation. Other accepted source checks and limitations
remain those of the earlier stages; this was no new exhaustive research sweep.

Only the historical appendix, generation record, and this production record
changed in this iteration. Canonical source owners and generated chronology
remain unchanged. No additional upstream research need or shared-code defect
was identified. All author-started build, check, and raster processes completed;
no background process remains. No staging, commit, push, installation, or
workflow advancement was performed. Cold study review and the subsequent
companion and publication stages remain required.

## Prior proof: author-study iteration 1

The fresh GPT-6 author at high effort completed the three forwarded mechanical
repairs from packet SHA-256
`54517be9d1f0df3603ae2ae5efee3b120d7229b5b02007c6ffc4d8b53ef320d5`.
The terminal scope and References now have separate semantic headings; the
scope paragraph formerly after the bibliography is with the other scope
paragraphs. The nine chronology cells retain their complete contextual prose,
with their page references consolidated directly below the table. No generated
date, source-owned qualification, appointed text, or interpretive argument
changed. The final render-source revision is `2026-10-13T02:24:13Z`.

The current author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0001/study-proof.pdf`:
**26 physical pages**, 447,250 bytes, SHA-256
`b4717e5f3508a872c6e59c9a213cb85708871ef7e1447bcdd004e94477ac4f54`.
The previous proof and verification below describe iteration 0, not these
current bytes.

- The required `make doc` and research-edition artifact component check passed.
  All 57 contents anchors resolve. The settled TeX log has no warning,
  overfull/underfull box, undefined reference, missing character, or error.
- All three forwarded checks pass: `references-used` recognizes 14 used
  entries; `unquoted-not-quoted` finds no conflict; and
  `chronology-claims-supported` validates all nine generated rows. The complete
  research-edition content preflight also passes, including chronology record
  and annotation currency, 34 source bindings, rights, house voice, and both
  whole-formulary lane declarations.
- The existing text-comparison/count procedure was rerun: all 17 Latin and 17
  English displayed bodies match the collation after its documented formatting
  normalization. The unchanged core exposition has **7,233 substantive words**
  by the method below.
- Every final page was opened as a full-page raster generated by
  `tools/pdf-review`. No clipping, collisions, broken table, stranded heading,
  or illegible footnote was observed. On page 23, the source-reference line
  correctly directs Esther to page 23; Job, Psalms, and Matthew to page 24;
  and Ephesians to page 25. References begins on page 25 and continues on
  page 26. The revision and compact rights colophon remain on page 26.
- PDF structure, text extraction, and fonts were checked: Letter pages,
  embedded/subset/Unicode-mapped Latin Modern fonts, one visible revision,
  and no unresolved page-reference marker. The proof is byte-identical to
  the checked build; the leaf's whitespace check passes.
- `make check-sources` was attempted. The reusable source library validates
  (including 3,815 bindings), but the aggregate exits 2 because its document
  catalogue check requires the declared, future `homily.tex`. The study-stage
  artifact gate permits those future companions and passes. No placeholder
  companion or shared-code change was introduced to satisfy a later-stage gate.

This repair reused the reviewed evidence map, chronology, and source limits;
it did not repeat the earlier author or research stage's external-source
inspection and claims no new source verification. All accepted research files,
source owners, and the two arguments remain unchanged. No new upstream
research need or shared-code defect was identified. The changed leaf files
are the historical appendix, study apparatus, generation record, and this
production record. All author-started build, check, and raster processes
completed; no background process remains. No staging, commit, push,
installation, or workflow advancement was performed. Cold study review and
all companion and publication stages remain the workflow's responsibility.

## Scope and provenance

Completed author-study iteration 0 for proper-study v10, run
`a72731c5491066a3`, from packet SHA-256
`373b377ba75ab6ba011a91b82c5aa35da7a59db405cdc044864c65fecffb5ef9`.
The author was GPT-6 at high effort through OpenAI Codex. The canonical
generation record carries the packet's workflow digest and seed commit;
the final render-relevant revision timestamp is `2026-10-13T02:17:00Z`.

The study concerns only the 1962 Twenty-first Sunday after Pentecost on
18 October 2026. It includes all seventeen appointed or conditional elements,
the documented mission-day and St Luke branches, detailed commentary, two
whole-formulary readings with their own four senses, a concluding comparison,
the reviewed chronology and historical appendix, and terminal references and
rights. No local calendar is supplied or inferred. The manifest declares the
future concise study and homily; those documents were not authored in this
stage. Accepted research, acquired sources, and shared code remain unchanged.

The core exposition contains approximately **7,233 substantive words**:
opening and map 651; element commentary 2,088; mercy reading 1,983;
pilgrimage reading 2,193; concluding comparison 318. The count uses
English-alphabet word tokens with internal apostrophes and hyphens retained,
excluding footnotes, TeX commands, displayed appointed texts, the historical
appendix, and terminal apparatus. It includes the readings' sense distillations.

## Proof and actual checks

The author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0000/study-proof.pdf`.
It has **26 physical pages** and SHA-256
`4f51be986a33deb748895c8f3f5825f33c81247ab9fad8bc4dc043d1ea9b4403`.

- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost PROVIDER=gpt`
  completed. Generation metadata and PDF navigation checks passed; all 56
  contents anchors resolve individually. The final build log contains no
  warning, overfull/underfull box, undefined-reference, missing-character, or
  TeX-error diagnostics.
- `tools/check-proper-components --provider gpt --document liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost --phase artifacts --edition research`
  passed. The study uses shared formatting and the full schema-2 declaration.
- All seventeen Latin and seventeen English displayed bodies match
  `propers/verified.md` exactly after TeX escaping, verse-label formatting,
  and outer-whitespace trimming. No lexical change or new translation was
  introduced. Historical English variants and biblical comparators are
  identified at their uses.
- `pdfinfo`, `pdffonts`, text extraction, and the leaf's `git diff --check`
  were inspected. The proof is US Letter; its Latin Modern fonts are embedded,
  subset, and Unicode-mapped. The main source uses the required 11-point
  article and shared 0.75-inch margins.
- `tools/pdf-review` generated full-page rasters in the stage artifact's
  dedicated `rasters/` child. Every page was inspected at full-page scale
  across the settled drafts. The final proof's pages 5–10 are byte-identical
  PNGs to the inspected 27-page draft; the final proof's other unchanged
  pages are identical to the inspected preceding 26-page proof. Final pages
  1–4, 20, and 23–26 were also viewed directly after the last rebuild.
  The last rebuild changed only page 20's corrected Augustine verse locator
  and page 26's timestamp; both were inspected again. No clipping, collisions,
  broken tables, stranded headings, or unreadable footnotes were observed.

The proof directory contains the logs, font and PDF reports, text-integrity
and word-count result, diagnostic result, raster comparison, and structured
author evidence. Workstation prefixes were removed from archived logs.

## Native evidence read and limits

The author read the canonical evidence maps and source records, then opened
the retained texts rather than treating an earlier PASS as verification:
Chrysostom's Matthew LXI §§1–5 and Ephesians XXII–XXIV (including the disputed
editorial notes); Augustine's Sermon 83, Psalm 89 §§1–4, Psalm 113 §§1–6,
Psalm 118 Aleph and Caph, and De Trinitate III preface §3; Gregory's Moralia
II.10.16–11.19 and the relevant III.3.3–6.8 exposition; Aquinas III q.88
aa.1–4; Bellarmine's relevant Psalm 89, 113, and 118 verse comments; and
Schuster III pp.178–181. Carrying authors make distinct substantive arguments
within each reading. Whole-Mass constructions remain the study's editorial
work; disagreements and differences of emphasis are retained.

The registered Douay–Rheims biblical context was read for Esther 13–14,
Job 1–2, Matthew's surrounding discourse and geographical transitions,
Ephesians 6 and the relevant earlier ethical context, and the appointed
Psalm contexts. Retained historical Catholic Encyclopedia discussions were
read for Esther, Ephesians, Matthew, New Testament dating, biblical
chronology, Paul, and David. The two official USCCB book introductions were
reopened to confirm their bounded Job and Psalms dating claims; their modern
prose is paraphrased, not used as study-text English. That current web
inspection was not a hash comparison to the acquisition-time pages.

This stage is not a fresh critical Greek or Latin edition or a new exhaustive
research sweep. It reuses the accepted Missal collation and rights decisions.
The author did not repeat every liturgical facsimile collation or independently
inspect the Haydock page image. Gregory was read in the retained reset
transcription, Schuster in retained OCR, and De Trinitate in the disclosed
later-revised web delivery; no new author-side facsimile verification is
claimed for those witnesses. No upstream defect requiring a research repair
was identified.

## Handback boundary

This record describes author verification only. Cold study review, derivation
and review of both companions, the shared-timestamp three-document build,
and independent visual and publication reviews remain workflow work.
All author-started build and raster processes completed; no server, browser,
or background worker remains running. No Git staging, commit, push, or
workflow advancement was performed by this author.
