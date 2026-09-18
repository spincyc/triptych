# Three-document proper-study production evaluation

**Both actual Sunday productions reached ACCEPTED.** Their six independently
reviewed PDFs and two canonical web editions are installed with exact accepted
byte identity. The independently reviewed v2 recipe changes are now applied
and pass their live checks. Final integration cold review remains pending.

## Contract and evidence ownership

For 20 September 2026, each proper owns an expansive study, an interleaved
concise study, and a standalone homily: three PDFs and one canonical study web
edition. Every interpretation must treat the whole formulary, develop its own
four senses, and draw substantively on at least two Fathers or saints. Cold
review judges source support, depth, coherence, comparison, oral clarity and
beauty; schema completeness alone proves none of them.

The [1962 production record][tlm] and [postconciliar production record][no]
belong to entirely separate calendar, proper, research, interpretation,
review and publication trees. Separation covers every prayer, chant, reading
and option. Shared mechanics, notices and independently used neutral sources
do not create shared liturgical ownership. The [implementation review][impl]
verified direct and indirect opposite-family import rejection, including real
TeX recorder probes in both directions and all three outputs.

Both actual runs use `proper-study` v1, frozen at seed `af9b2d10a`, digest
`1375f708d8670b2f4ccaf1869cfaa6fe67fe6946dc2b962c766bcdc499d3b47e`:
1962 `80a724fb8410dc3d`; postconciliar `8f4e6454c021280a`.
Exact results remain in each leaf's own [1962 result archive][tlm-results]
and [postconciliar result archive][no-results].

## What production and independent review changed

**Review identity and repair routing.** Initial implementation review found
that acceptance was not bound to reviewed bytes, late staleness could return
to an owner unable to repair it, and a single-publication gate required
unrelated installed PDFs. Engine-owned seals, ordered owner repair routes
with downstream re-review, and a scoped three-PDF gate resolved these defects
without relaxing global release policy. Independent review passed 156 focused
tests and actual import probes. Synthetic repair-to-acceptance tests establish
engine behavior, not actual Sunday acceptance. A comment-only `main.tex`
scaffold also resolved new-leaf binding validation before authoring. [Evidence][impl]

**Complete research boundaries.** The real 1962 preflight rejected global
guidance and review receipts incorrectly declared as external source owners;
research iteration 1 corrected the declaration. Postconciliar research
review 0 found missing controlling rights evidence; review 1 then found
missing GIRM authority. Research iteration 2 passed cold review with a
235-file boundary including all fifteen added records. The profile now
requires a complete adopted-authority sweep, initially and after repairs,
and explicitly distinguishes prose links from sealed dependencies. Both
clarifications passed independent review. A bounded driver check found the
1962 112-file boundary current; this was not a second scholarly review.
[Dependency review][dependencies]; [authority review][authority].

**Reliable individual builds.** The real 1962 build was blocked by a
provider-wide metadata check encountering the legitimate unfinished
postconciliar scaffold. Scoping that check initially introduced a cached-build
hole: deleting the selected publication's metadata still succeeded. Cold
review reproduced it; an unconditional selected-source audit repaired it.
Re-review passed 55 tests, ten installation/bulk scenarios, and compatibility
checks of all 192 historical canonical sources. Bulk gates remain global.
[Evidence][metadata]

**Evidence preservation and executable recipes.** Raster generation replaced
its destination, deleting twelve known transient reports and an earlier homily
proof; some older contents had not been inventoried. Canonical build mirrors
and all sixteen then-completed engine results survived. Missing historical
evidence is not claimed recovered. Independently accepted guidance now
requires dedicated raster children outside other evidence. The frozen web
recipe also doubles the provider directory; current execution records an
exact-byte relocation. The [original prepared v2 correction][v2] passed cold
review; its negative controls reproduced both v1 defects. A [revised variant][v2-current]
adds only the new Markdown helper to the test fixture's copy list and passes
106 owning tests plus two postconciliar command tests. Its independent
supplement passed five command tests and a missing-helper negative control.
A final [installation addendum][v2-install] resolves contradictory instructions
about retypesetting: normal Make dependency checks must run, and an installation
may pass only when both rebuilt and installed bytes match the independently
accepted hashes. A mismatch is a real terminal `BLOCKED` result; no automatic
repair transition or fabricated `PASS` is supplied. The final six-file variant
passed its independent addendum review and was applied only after both real
runs reached ACCEPTED and their terminal archives were complete. The actual
guarded application exited 0, and all 106 owning tests then passed in the live
tree without skips. Original setup failures and their corrections remain
recorded. The [live application record][v2-live] preserves the exact six file
hashes, original-state identities and post-application checks.
[Raster review][raster]

**Faithful web conversion.** Braced path locators first failed conversion.
Cold review of the repair then found silently corrupted delimiter syntax;
the final implementation explicitly refuses unsupported forms and passed
74 tests plus nine probes. Actual 1962 web review next required replacing
visible caret verse markers with semantic superscripts (`WEB-001`); fresh
review passed the corrected conversion. The shared superscript repair passed
75 code tests. Separate historical review accepted precisely 47 replacements
across ten existing editions, preserving all other Markdown and rendered HTML
bytes and all 220 source/support inputs. No historical PDF review occurred.
Ordinary whitespace checking exited 2 for three inherited semantic hard
breaks; the narrowly EOL-aware check exited 0. [Path review][paths];
[superscript reviews][superscripts].

**Semantic web targets.** Postconciliar web review found all eleven required
element anchors missing. Source-owned labels now identify each text/locator,
including grouped prayers and alternative Communions, without inferring roles
across calendar families. Cold converter review found two further defects:
the audit omitted title-generated IDs, and missing explicit links silently
became prose. The repair validates complete final HTML and refuses unresolved
proper links. A shared Markdown primitive avoids a reverse CLI dependency
while using the site's exact renderer. Independent rereview passed this
scope: 144/144 complete historical HTML outputs and 20/20 legacy conversions
are byte-identical. Of 199 tests, 198 passed; the missing, not-yet-installed
postconciliar web edition caused the same remaining error with baseline
tools. After legitimate installation, the [exact one-case rerun][installed-test]
passed (exit 0); the entire older 199-test command was not rerun. Initial
harness failures are retained. This is code/rendering fidelity, not
publication acceptance. [Initial and final anchor reviews][anchors]

A later browser check found inherited breadcrumb names inconsistent with the
repository's apparatus rule. The [naming addendum][breadcrumbs] independently
accepts exactly two display-string changes, to “1962 Missal” and
“Postconciliar Missal.” Four full rendered-page comparisons preserve every URL,
ID and other HTML byte. The earlier 144-page parity applies to its earlier
frozen renderer; this later intentional naming difference is distinct. Both
actual web reviewers retain earlier captures and inspect final previews using
the corrected renderer. No article source or PDF changed.

## Actual document outcomes

| Family | Expansive study | Concise study | Homily |
| --- | --- | --- | --- |
| 1962 | 7,443 substantive words; 23 pages | 1,686 words; 5 pages | 1,283 spoken-body words; 4 pages |
| Postconciliar | 6,608 substantive words; 20 pages | 1,750 words; 5 pages | 1,288 spoken-body words; 4 pages |

The three-document division produces different reading experiences. The 1962
study asks what heals the commanded heart, what gathers many people under one
Lord, and how worship becomes a faithful life. Each argument crosses all ten
proper elements; its four senses retain historical speakers, Christ and his
Church, concrete conduct, and final consummation. The postconciliar study asks
what divine generosity makes possible, how conversion answers it now, and how
one people is gathered through the ages. Its eleven-element coverage preserves
the two Communion alternatives as alternatives. Neither study claims that its
editorial lanes are historical schools or that a Father expounded this exact
Sunday's complete formulary.

The concise documents compare answers at the relevant point in the argument.
The 1962 version retains differing accounts of the praying voice, confession,
vows and judgment. The postconciliar version preserves competing readings of
the vineyard and hours, differing accounts of the payment order, and the
Fathers' refusal to locate envy in heaven. Compression therefore leaves the
reader able to recognize alternatives instead of receiving a false consensus.

The homilies develop one speakable argument apiece. The 1962 homily begins with
the next sentence spoken to a difficult person, moves through the twofold
command and David's Lord to Paul's patient common life, and connects the
Mass's petitions and sacramental healing to a concrete act of charity. The
postconciliar homily begins with the worker whose promised wage loses its joy
when another receives it, tests that reaction through Isaiah's mercy and
Paul's service, and ends with gratitude enacted for another person's good.
Both use a recurring concrete situation, questions, explanation of scriptural
details, a sacramental connection and a practicable response. Their source and
delivery notes remain outside the spoken argument. Independent reviews support
these bounded judgments; a live congregation's comprehension and a preacher's
actual delivery have not been measured.

The 1962 production retained 57 actual engine results: 53 PASS, three FAIL,
and one CHANGES_REQUIRED. Its failed research preflight corrected the source
boundary. Web review required proper superscripts. Two actual publication
gates rejected stale study approvals, first after layout improvements and
then after ten source labels; each returned to the real author and fresh
independent downstream reviews. Removing four unnecessary page breaks and
adding widow/orphan protection reduced the study from 26 to 23 pages without
cutting prose. Final study, concise, homily and visual reviews are iteration 2;
final web review is iteration 3. All 32 final PDF pages passed. The last normal
Make installation reproduced the approved bytes, including its companion
rebuilds. Actual publication-gates iteration 2 reached ACCEPTED with no
findings or escalations. [Production record][tlm]

The postconciliar production retained 44 actual engine results: 40 PASS and
four CHANGES_REQUIRED. Two research reviews enlarged the authority/rights
boundary. Study review 0 replaced recurring narration about the writer's
editorial policy with concrete source conclusions (`STU-001`), reducing
6,806 substantive words to 6,608 while preserving the alternatives. Visual
review 0 passed with two nonblocking typography advisories; the original
verdict and severities remain intact. Web review 0 then required eleven
source-owned anchors (`WEB-001`). Study author 2 added them and repaired
study spacing, the widow and page-turn hyphen. The ensuing concise owner
also corrected paragraph termination before its apparatus. Fresh study 2,
concise 1 and homily 1 reviews passed, followed by independent visual 1
inspection of all 29 pages and web 1 review. Normal installation reproduced
all approved bytes. Actual publication-gates iteration 0 reached ACCEPTED
with no findings or escalations. [Production record][no]

All six PDFs retain their own research/synthesis/homily identities and
edition-specific catalog links. Each rite has exactly one canonical web
edition and one catalog marker. The 1962 row preserves the other provider's
status; the postconciliar Year A cell preserves Years B and C as Planned.
The six per-PDF alpha records use the existing standing authorization.
Homily durations remain estimates: 10.7–11.7 minutes for the 1962 homily at
110–120 words per minute, and 10.3–11.2 minutes for the postconciliar homily
at 115–125. No audible rehearsal is claimed.

## Source integrity and remaining limits

The [retained-commentary audit][commentary] required explicit, bounded
composition metadata for sixteen new works. [Jerome Isaiah review][jerome]
resolved record/schema defects but retained unresolved delivery rights and
no offline protected payload. The registered GILM PDF proved 44 pages rather
than 45; its existing consumer fingerprint changed without changing quotations
or loci. [Source integration review][sources] covers integration and notices,
not the Sunday arguments.

A 1962 reviewer's alleged missing Latin word was found at the full page's
right margin and independently withdrawn. The unsubmitted report remains
distinct from the accepted result; no source was altered to fit the finding.
Postconciliar full official 2008 Latin/U.S. 2011 altar-book collation remains
incomplete. Its public-domain English is study wording, not approved
proclamation text; full protected ICEL/CCD English is not republished.

Separately, twenty missing historical PDFs (571 pages) were restored with
identity, metadata and byte checks. This repaired inherited ledger evidence
absence, not historical content acceptance. The [restoration report][restore]
and exact receipts are now durable.

Actual nonterminal replays reproduced both current packets
(`deterministic=true`). Terminal replay checks retained packet integrity and
reports `deterministic=null`; it does not re-perform history or resolve old
workflow versions.

## Final integration and verification

Both terminal archives preserve the actual packets, results and immutable
production identities. Final integration inspection found that the 1962 archive
initially retained packet hashes but not the packet texts. All 57 still-existing
engine packet files were copied verbatim into that same owning archive, each
checked against the engine's recorded hash. A separate packet-archive manifest
proves that all 68 previous archive files, the production audit, state and
immutable manifest remained unchanged. Earlier present-tense checkpoints in
the chronological production audit describe their historical stage; its full
stage table and terminal section govern the final ACCEPTED disposition.

Every final content, visual and web review seal still
matches its current inputs; all six installed PDF hashes match the approved
builds. The [identity export][v2-identities] records each exact path, hash and
page count. Application of v2 left both original state and immutable-manifest
files byte-identical. Four actual status/replay commands then exited 0:
both v1 productions remain ACCEPTED, with intact retained packets. The current
workflow is v2, digest
`4e4bbd64b71b60bd9e04c9fa7592ecb52c85e05cad1349c41941fa4d31e4e4d2`;
these Sunday publications are not represented as a new v2 production.

The final document catalogue reports 142 works, 194 documents, 218 issues and
6,220 pages. Updating its current-workflow declaration preserves every produced
work record. Source-inventory refresh reports 142 publications and 2,286 files,
with all 142 classification arrays unchanged. The family ledger honestly retains
153 pending review units, zero screened families and no complete atomic citation
coverage. Final `make check-sources` and `make check-release-bindings` both
exited 0 after the terminal archives and v2 application; the latter reports
zero stale bindings. These gates do not close unrelated corpus acceptance work.

The final integration cold review remains pending. After that review and the
corresponding register/ledger reconciliation, the reviewed state will be
committed on `feature/codex/propers/homily` and an ignored transport package
assembled from that exact commit. Package creation is not itself an approval.
No default-branch integration, public-site deployment or human oral rehearsal
is claimed.

[tlm]: ../../src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost/research/production-review.md
[no]: ../../src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a/research/production-review.md
[tlm-results]: ../../src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost/evaluations/proper-study-results/80a724fb8410dc3d/
[no-results]: ../../src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a/evaluations/proper-study-results/8f4e6454c021280a/
[impl]: propers-three-documents-implementation-2026-09-17.md
[dependencies]: propers-three-documents-dependencies-2026-09-17.md
[authority]: propers-three-documents-authority-sweep-2026-09-17.md
[metadata]: propers-three-documents-scoped-metadata-2026-09-17/review.md
[raster]: propers-three-documents-raster-destinations-2026-09-17.md
[v2]: propers-three-documents-recipes-v2-2026-09-17/prepared/REPORT.md
[v2-current]: propers-three-documents-recipes-v2-2026-09-17/renderer-helper-addendum/REPORT.md
[v2-install]: propers-three-documents-recipes-v2-2026-09-17/installation-addendum/REPORT.md
[v2-live]: propers-three-documents-recipes-v2-2026-09-17/live-application/RECORD.md
[v2-identities]: propers-three-documents-recipes-v2-2026-09-17/live-application/final-artifact-identity.json
[paths]: propers-three-documents-web-path-2026-09-17/review.md
[superscripts]: propers-three-documents-web-superscripts-2026-09-17/README.md
[anchors]: propers-three-documents-web-anchors-2026-09-17/README.md
[breadcrumbs]: propers-three-documents-web-anchors-2026-09-17/breadcrumb-addendum/cold-review/REPORT.md
[installed-test]: propers-three-documents-web-anchors-2026-09-17/post-install-verification.md
[commentary]: retained-commentary-review-2026-09-17/review.md
[jerome]: jerome-isaiah-retention-2026-09-17/final/final-rereview.md
[sources]: source-integration-2026-09-17/README.md
[restore]: historical-pdf-evidence-restoration-2026-09-17/report.md
