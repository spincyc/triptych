# Committed checkpoint disclosure and integration review

**Disposition: ACCEPT** for the disclosure and integration scope of
`6a1fe6e33..9ff79af29d54644d91792f4eda4d71f6fcfc2506`, reviewed independently
on 25 October 2026. No material publication/disclosure blocker was found in
these committed objects. This verdict does not approve later All Saints prose,
its future artifacts, a completed source aggregate, a site build, a push or a
deployment.

## Exact review boundary and method

The four outgoing commits are `35f548b43`, `24c1b7ce1`, `c04c5ed36` and
`9ff79af29`. The endpoint changes 660 paths. Enumeration with
`git rev-list --objects 6a1fe6e33..9ff79af29` reaches four commits, 139 trees
and **666 new blobs**, including intermediate committed versions. The audit
examined those objects rather than substituting the concurrently changing
worktree. Changed files have ordinary file modes: 658 at `100644` and the two
existing tool executables at `100755`; there is no new symlink or gitlink.

All 666 blob contents and four commit objects were scanned for machine-private
paths, credentials, private network routes, signed or session-bearing download
parameters and request headers. All seven new source PDFs additionally received
text extraction, metadata inspection and attachment checks. There was one
lexical false positive: the prose `authorization:` in
`guidance/liturgy/propers-production-plan.md`, not a request header. No actual
private-environment value, credential, transient signed route or session leak
was found. The PDFs contain no embedded files, JavaScript, forms or encryption;
no private path appeared in their extracted text or metadata. This is a bounded
content inspection, not a claim that pattern matching proves arbitrary data
secret-free.

The applicable repository/editorial contract, source identity and storage
rules, liturgical publication policy, web-data ownership rules, outbound
licence and changed third-party notice governed the judgments below. This
review checked integration and disclosure; it did not repeat the separate
whole-source exegesis or every-page publication reviews.

## Source bytes, rights and ownership

The checkpoint adds **13 artifact manifests: 12 tracked payloads totalling
9,792,728 bytes, and one restricted, metadata-only Ordo record**. All 12
payloads match their committed manifest hashes and byte counts; their hashes
are distinct. The 13-manifest count is not a claim that 13 payloads are retained.

| Evidence retained | Boundary and recorded distribution basis |
| --- | --- |
| Bede, `works/bede/explanatio-apocalypsis/editions/1878-marshall-parker/` | Complete 192-page 1878 Marshall scan, separate uncorrected whole text extraction and five checked comments; United States historical-publication basis, with Google attribution retained separately. |
| Mame, `works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/` | Three complete selected historical pages and six checked Latin bodies; identified 1922 printing, separate derivative ancestry and United States basis. |
| Pustet, `works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/` | Two selected 1862 pages; no whole modern missal delivery or newly authored target rubric is imported. |
| Cummiskey, `works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/` | One original Common Preface page; separately recorded historical basis and retained Google attribution. The earlier whole-object disposition is not silently rewritten. |
| Lasance/Walsh, `works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/` | Seven ordinary numbered pages and six checked English bodies; the existing registration-specific nonrenewal record supplies the United States basis. Later lettered inserts remain excluded. |
| Schuster, `works/ildefonso-schuster/the-sacramentary/editions/` | Four-page 1927 and five-page 1930 chapter derivatives; complete parent hashes and measured size explain bounded retention. Historical rubrics and prefaces are not treated as 1962 appointments. |
| Editorial projection, `works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-25-f02-editorial-projection/` | Nine bounded Latin bodies, with distinct historical testimony and 1962 comparison. Project selection/normalization does not claim ownership of the historical words. |

Paths in this table are relative to `src/sources/`. The exact artifact manifests
own payload identity, extent, transformation and rights; the publication's
`research/source-bindings.toml` and `research/source-dispositions.toml` retain
its local uses and sufficiency judgments. No duplicate retained payload or
newly relocated provider ownership was found.

The source-reader projection
`src/web/data/structure/sources/editions/fsspx/ordo/2026-2026-10-25-web.json`
contains identity and the restricted/unresolved state, with no passages or HTML
payload. Restricted 1962 facsimile, modern Corpus Thomisticum response, Ordo HTML
and modern Haydock delivery bytes are not added. The new
`propers/retrieved.txt` contains expressly labelled Mame/Pustet finding-aid
material, not those restricted deliveries. The addition to `THIRD_PARTY.md`
accurately excludes the historical wording, facsimiles and digitizer material
from the project licence.

Date ownership is preserved. Bede's `work.toml` dates composition to
c. 710–716 with the translator's qualified basis; its `edition.toml` dates the
English printing to 1878. Direct inspection of the committed scan's title and
preface iv confirms both the 1878 imprint and the stated composition range.
The new Ordo edition is a dated web state, not a historical printing. Selected
source-page inspections also show the declared historical page families and
retained digitizer/delivery attribution. This review does not independently
re-adjudicate the previously recorded rights instruments or claim clearance in
other jurisdictions.

## Generated data and protected provider boundary

Independent exhaustive JSON comparison reproduces the complete Proper delta:
491 files change only their generation digest; one file changes that digest
and the All Saints registry value; two aggregate files change only that registry
value, from `1962-11-01` to `F02`. No Proper wording changes. The complete
537-file data delta comprises 494 Proper, 36 Source and seven Catena files.
The Catena additions are the five separately admitted Bede comments and their
chapter/index apparatus; they do not turn the deferred commentary into admitted
text.

The endpoint tree object IDs for `src/claude/`, `web/claude/`,
`src/sources/inventories/claude-publications-v1.toml` and
`src/sources/inventories/claude-classification-review-v1.toml` equal the base.
No release, catalogue-page, shared browser implementation or unrelated provider
change is introduced by this range. Local restoration of already published
Claude PDFs is outside tracked Git disclosure and does not alter these protected
trees.

## Acceptance records and remaining gates

The four-essay production receipt's 28 source/web/installed-PDF hash checks
pass against the committed source/web bytes and local installed PDFs. The
accepted page counts total 96: 24/24/25/23. Each essay's references and source
bindings equal the base. The receipt preserves its entire preceding publication
object exactly under `previous_publication`; its old deployment evidence is
therefore historical evidence, not a new deployment assertion. Publication PDFs
are ignored under the repository's existing deployment-build policy, so their
absence from this Git diff is expected.

`research-acceptance.json` matches both actual native result hashes and PASS
dispositions. Every one of the independent research review's **1,779 sealed
file hashes** matches the committed endpoint. These checks establish identity
and truthful reporting of the completed research event; they do not accept
future author output. At the endpoint, F02 `main.tex` is exactly the single
comment reserving its source owner, and there is no committed F02 web declaration
or installed-publication claim.

`PROJECT-WORK.md`, `promised-deliverables.toml`, `RECORD.md`, the native
`CYCLES.md` and shared essay receipt consistently leave the full Sunday workflow,
integrated publication checks and main/live publication open. The aggregate
receipt explicitly records `make check-sources` exit 2 at the known pre-author
missing web declaration, distinguishes reached checks from downstream recipes
that did not run, and sets its global-source-pass fields false. Its completed
registration operations are not represented as a completed global gate.
The 163 source-family units remain pending; no overall migration or atomic
citation acceptance is asserted.

The documented F02 authorization is bounded to this target. The global 528-row
chronology audit remains open, including its recorded authorization/consumer
contract contradiction. Neither the native research PASS nor the separate
Wisdom inspection is presented as global corpus or maintainer acceptance.

`git diff --check 6a1fe6e33..9ff79af29` passes. No source or generated data was
changed by this audit. Scratch object inventories, scan candidates, PDF metadata,
hash checks and comparison results are under the ignored
`.scratch/publication-cold-audit/`; this tracked report preserves the durable
verdict and its limits. The coordinator must still review the later delta and
run the required final source, artifact, release/site, push and deployment gates
before reporting the user's complete request fulfilled.
