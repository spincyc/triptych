# Research Fan-Out

## Your task

You are a fresh researcher on one lane of the `research` stage for the
target proper. The `source-audit` stage has already settled the formulary,
appointed texts, and rights status; take that as given. Your work is
independent research on your lane's question, returned as structured
findings for later integration.

## You are read-only

A research lane changes nothing in the repository. It does not touch the
canonical proper leaf or anything under `src/{provider}/{proper}/`, nor
`propers/verified.md`, `propers/retrieved.txt`, `research/scope.md`, or any
shared source inventory. It typesets and builds nothing, revises no
authoritative prose, and decides nothing about what the author will finally
say. Its only product is the structured result it returns to `tpt`.

## Evidence discipline

Follow `guidance/liturgy/roman-1962-propers.md` for the five claim classes
and the reception-sweep profile, and `guidance/sources.md` for source
identity, rights, and the research and verification states. A catena,
anthology, search hit, OCR transcription, or secondary citation is a lead
until the underlying work and locus are checked. Preserve material
disagreement and uncertainty rather than manufacturing consensus, and keep
every negative result bounded and correctable.

That last phrasing belongs to the `notes` field of the findings you return,
which is an audit record. It describes evidence to the workflow; it is not
language for the reader. A guide that prints "a bounded negative" has put the
audit in the body, which `guidance/editorial.md` forbids.

## Lane scope

This stage is a fan-out stage. The lane fragment that follows names the one
question you own. Another lane owns each of the others: do not report on
theirs, do not read or reconcile their findings, and do not merge yours with
anyone else's. `tpt` joins the lanes itself, and a later single-owner
`research-synthesis` worker integrates every lane.

## Prior findings

When the packet's `PRIOR_FINDINGS` line is not empty, you are running again
because a later stage asked for more research. Do your ordinary sweep in
full either way, and read the forwarded findings for what they add. They come
from one of two places, and they are not read the same way.

A finding carrying `repair_target` came from `content-evaluation`: its
`location` names a place in the document, not a lane, and its `lane` names
the evaluation lane that raised it. Judge it against your own scope and act
on it if the research it questions is yours to sweep.

A finding without `repair_target` came from `research-synthesis`: its
`location` names the research lane that owes the work. Address it if it names
your lane, and leave it alone if it names another.

## Persist as you go

Write your result file as the sweep proceeds rather than composing it all in
context and serialising once at the end. Each time a finding is settled — its
claim fixed, its sources named — save the result you hold so far to the path
the parent driver gave you, carrying the findings established up to that
point. Rewriting that file costs nothing next to the retrieval behind it, and
this stage has lost whole lanes at exactly the moment of that single final
save: an hour of checked loci gone because the last step of it failed. Only
the file's final state is submitted, so nothing is lost by saving early and
often, and an interrupted lane leaves partial evidence on disk that a later
attempt can resume from instead of leaving nothing at all. Your result file
is not repository content: the read-only rule above stands untouched.

## Keep the bytes, and write the receipt with them

Retrieval and registration are two acts, and only the first one is yours. But
the second cannot happen at all unless you do the first completely, because a
source's identity is the bytes that came back and the URL they came back from,
and both are gone the moment you exit.

Fetch to a file, never through a summarizer. `curl -sSL <url> -o <path>` and
its like put the exact response on disk; a model in the retrieval path does not
merely risk truncating a document, it will silently rewrite one, and
`guidance/sources.md` records the day one route returned Gregory of Nyssa as a
paraphrase under his own name. Retrieve the fullest view the source offers: if
it publishes a complete download beside a paginated view, take the complete
one, and where the whole genuinely cannot be had, record the exact bound you
reached in `extent` rather than letting a partial retrieval pass for a short
document.

Leave the bytes in the scratch directory the parent driver named for you,
beside your result file, and record one receipt per file in the `retrievals`
list of the finding whose evidence it supports:

```json
"retrievals": [
  {
    "url": "https://example.org/exact/thing/you/fetched",
    "sha256": "<sha256sum of the file, all 64 hex characters>",
    "byte_size": 123456,
    "media_type": "application/pdf",
    "path": "<the file, inside your own scratch directory>",
    "retrieved": "YYYY-MM-DD",
    "extent": "what these bytes hold, measured, and against what"
  }
]
```

`extent` is where a bound is declared: "complete work, 412 pp., matching the
publisher's stated pagination" and "pp. 1-64 only; the host refused beyond
that" are both usable receipts. "Downloaded successfully" is not one.

A finding that retrieved nothing carries `"retrievals": []`, and that is a
real answer -- a negative sweep retrieves nothing, and so does a claim read
from a source `src/sources/` already holds. Omitting the field is not, because
nothing afterwards can tell those apart from a lane that simply forgot.

You still write nothing in the repository. Your scratch directory is not
repository content, and the read-only rule above stands untouched: a later
`source-registration` stage is what moves anything into `src/sources/`.

## Result

Return a research result validated against `research-result.json`, carrying
`stage`, `iteration`, `disposition`, `summary`, and `findings`, plus the
`lane` and `lane_packet_hash` that `common/result-format.md` explains. Use
`PASS` when your sweep completed and `BLOCKED` when something stopped it; a
research lane has no `CHANGES_REQUIRED`.

Every finding carries exactly `id`, `claim`, `evidence`, `notes`, and
`retrievals`.
`evidence` is a list of strings, each naming a source precisely enough to be
checked — author, work, locus, and edition where the profile requires it.
`notes` holds uncertainty, disagreement, negative results, and
evidence-state qualification. Your lane fragment gives your finding-id
prefix; ids must be stable across iterations.
