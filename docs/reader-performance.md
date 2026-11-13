# Reader setup and performance

Lectern opens the selected reading from canonical sources through the shared
thin index under `src/index/`. It does not need a complete browser-product
cache before its first use. The website still publishes complete, verified
browser products. These are separate operations with different costs.

## First checkout

Use a partial clone to defer historical file contents while retaining the
complete commit graph:

```sh
git clone --filter=blob:none https://github.com/spincyc/triptych.git
cd triptych
```

Git downloads the current checked-out source tree. Historical blobs are
fetched later when an operation needs them, so the first history-dependent
operation may use the network. This does not shrink remote history or an
existing clone, and it does not provide a sparse source checkout. The reader
currently expects its selected canonical files to exist locally; it does not
silently fetch missing sources. Exact binary evidence packs retain their
separate, explicit delivery process.

Avoid `--depth`: edition revision timestamps depend on complete history, and
the revision owner refuses shallow clones. Retaining the commit graph with
`--filter=blob:none` preserves that history model while deferring old file
bodies. Partial-clone transfer savings and first-use latency must be measured
against a server that supports filtering; removing current PDFs alone proves
neither.

An assigned workspace branch governs work in that checkout. Keep it and use
its own clone instructions rather than creating another checkout in place.

## Open the terminal reader

Install Python 3.11 or later, Node and Git, then prepare the pinned Python
dependencies from the repository root:

```sh
python3 -m venv .scratch/lectern-venv
.scratch/lectern-venv/bin/python -m pip install -r requirements-tui.txt
tools/lectern open --surface day
```

Lectern selects that environment automatically. Install the locked converter
before opening publication editions that need conversion:

```sh
python3 scripts/_install_web_edition_pandoc.py --fetch --bin-dir .scratch/web-edition-toolchain
tools/lectern open --surface texts
```

The converter installer is an explicit download. Ordinary startup does not
install tools. See the [Lectern guide](../scripts/lectern/README.md) for controls,
snapshot output and surface behavior.

The index contains IDs, paths, hashes and discovery metadata. It contains no
copy of the corpus's reading text. The existing source producers transform a
selected record only when requested, and the browser models interpret and
render it. A selected large edition can still take time to parse or convert.

Startup checks index membership using Git and dirty paths. Each canonical
body actually consumed is separately checked by SHA-256 and size. A fresh
reading session is needed after changing sources and refreshing their index.
An error about stale or missing input is a maintenance failure, not an empty
catalogue or permission to use older text.

The disposable selected-record cache is `.scratch/reader-data`. Its entries
bind code, history, dependency hashes and projected bytes. It can be discarded
and recreated by opening the same readings. `TRIPTYCH_BROWSER_DATA_ROOT`
selects the complete browser-product cache for publication; changing it does
not change Lectern's ordinary reading cache.

## Index maintenance and full checks

Derived index metadata accompanies the canonical changes it describes.
It is maintained explicitly, never repaired during startup. Regeneration uses
the canonical producers and their existing rights and admission filters;
checking independently replays those derivations. Do not hand-edit a row to
make a reader accept changed sources.

Use the complete maintenance commands:

```sh
tools/corpus-index refresh --readers
tools/corpus-index check --readers
```

`refresh --readers` uses each surface's input fingerprint to update changed
discovery through its existing producer, then updates the generic address
layer. Unchanged path and manifest identities are reused. `check --readers`
independently replays every discovery projection and hashes and parses the
complete address scope. The compact `src/index/readers.json` binds surface
input and output aggregates; it does not duplicate the per-file inventory.

Without `--readers`, `refresh` updates only the generic layer and refuses stale
surface proofs. It cannot bless old discovery metadata after a canonical
change. Sources also exposes the narrower owner commands `tools/source-reader
index` and `tools/source-reader index --check`; an isolated owner refresh still
needs complete index maintenance before reading.

Publication discovery requires committed source and producer inputs so
revision dates remain reproducible. Commit those changes on the assigned
branch first, refresh and check the index, then review and commit the derived
metadata. Its recorded generation commit must remain an ancestor of the
current checkout, with no intervening commit changing the publication runtime
inputs; metadata-only commits remain valid. The catalogue and selected-edition
reader check that history binding without reading historical source bodies.

The [web-data contract](../guidance/web-data.md#tracked-discovery-and-ordinary-indexed-reading)
owns the precise freshness and publication boundary. Full source checks,
rights checks and publication checks retain their normal scope. In a
workspace, the complete site path remains:

```sh
export TRIPTYCH_BROWSER_DATA_ROOT=.scratch/browser-data
tools/browser-products build
tools/browser-products check
make public-site
```

An intentional canonical change may require explicit browser-product
recording before that build. Follow [Web data](../guidance/web-data.md#what-a-family-key-covers)
for its independent derivation and review requirements. A successful terminal
read is not evidence that a complete publication build or source audit ran.

## Measuring the change

Measure first opening and repeated opening separately. State the selected
surface and reading, index state, selected-record cache state, complete
browser-product cache state, dependency installation and Git fetch policy.
Time until the requested reading has settled, rather than until a loading
screen appears. Record total transfer bytes separately from elapsed time.

A useful headless reading is:

```sh
tools/lectern snapshot --surface day --date 2026-10-22 --size 120x36
```

Compare the complete rendered reading, qualifications and available choices
as well as time. A smaller result caused by omitting records, refusing an
offered selection or hiding unresolved material is not a performance gain.
For Sources, distinguish initial browsing from complete search: initial
browsing needs only the first bounded work-metadata shard, while a search,
filter or changed sort must cover the complete discovery catalogue.

The earlier observations were about 42 seconds for a warm Day open and
15 minutes 38 seconds for a cache-assisted rebuild of five of thirteen
browser-product families. The latter was not a fully cold site build.

The November 2026 implementation measurements include:

| Operation | Before | Indexed or selective path |
| --- | ---: | ---: |
| Day startup / settled snapshot, 120×40 | approximately 42 s | 6–7 s cold; 2–3 s warm |
| Sources initial discovery JSON | 11.23 MB | 262.5 KB |
| Day, 15 January, initial JSON | 23.30 MB | 1.50 MB |
| Liturgy Compare initial JSON | 30.69 MB | 2.61 MB |
| Postconciliar Browse initial JSON | 8.76 MB | 1.17 MB |
| History catalogue derivation | 19.83 s | 0.54 s |
| One article conversion | 2.05 s | 1.15 s |

Transfer figures are uncompressed payload sizes, not network latency. Sources
initial discovery is a 194 KB root plus one 68 KB shard of 128 works; it renders
40 works per page. Complete search, changed filtering/sorting and deep-ID
navigation still load all discovery shards. History's catalogue remains
11.58 MB: its generation is faster, but this change does not split its web
transfer. Selected History texts and comparisons avoid the complete producer.

The liturgy comparisons used the actual new producer output and the previous
complete output through native browser readers. All 1,599 selected Mass
payloads matched the complete Mass objects, and the reader tests retained
the same text, choices, qualifications and existing invalid-state refusals.
Complete calendars remain generated for independent publication checks and
legacy consumers; the interactive readers fetch the thin discovery and selected
Mass payloads. Those generated products remain outside Git.

The timings above are individual local observations, not throughput guarantees.
Index authoring and independent complete publication checks still perform full
corpus work. They are not a first-reader bootstrap requirement.

A controlled filtered clone of the implementation retained all 3,113 commits
and all 80,871 tracked source paths. Its complete graph initially transferred
17.27 MB of pack data; normal checkout brought total pack data to 637.87 MB,
compared with about 5.1 GiB of objects in the existing full clone. Local file
transport took 1.50 seconds for the graph and 21.34 seconds for checkout. These
are transport/size experiments, not predictions of GitHub download time.

With dependency installation already complete, that fresh checkout opened the
12 November 2026 Day reading in 5.97 seconds, then 2.20 seconds warm. Sources
opened in 2.09 seconds and Publications discovery in 2.36 seconds. Canonical
text appeared in the settled snapshots. With Git lazy fetching disabled, no
fetch occurred, object storage was unchanged and 73,977 historical objects
remained absent. No browser-data family was prepared. The original working
checkout measured 7.11/2.58 seconds for the same cold/warm Day snapshots while
other validation work was running.

The first complete metadata derivation took 9 minutes 38 seconds; an unchanged
`refresh --readers` took 7.71 seconds and reused all 80,287 inputs without
rehashing or reparsing them. This is maintainer work: the resulting metadata
ships in Git, so a first-time reader does not repeat it. The measured metadata
occupied about 54.4 MB as files and 16.4 MB as compressed Git blobs, including
the generic integrity/address layer and all five discovery surfaces. This
adds lookup metadata without duplicating reading bodies or rewriting history.
