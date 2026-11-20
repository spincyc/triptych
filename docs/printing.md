# Printing Triptych

Use an edition's **Generate PDF** action. The native print implementation runs
the actual TeX engine against that edition's canonical sources, original
templates and fonts. It produces a PDF with the authored page layout, tables,
footnotes and illustrations. Open the completed PDF to print it or save it.
The PDF is generated in your browser when requested and is never checked into
Git. The site does not depend on a separately maintained collection of PDFs.

The admitted print catalogue at the 2026-11-03 migration has 644 edition roots.
These are generation choices, not a stored collection of 644 PDFs:

| Family | Editions |
| --- | ---: |
| Provider publications, including declared companions | 281 |
| Bibles | 7 |
| Papal source selections | 350 |
| Reading-plan volumes | 6 |

Each edition has a small print page under `print/`: its title and edition or
companion label, the **Generate PDF** controls, any earlier printed edition,
and a link to read it online where a web reader exists. Web readers keep
their reading presentation. Each carries a **Generate PDF** action at the top
of the page, which typesets the edition without leaving the page: a small
progress bar appears beside the link, and the PDF downloads when it is ready.
Cancel it from that popover. Open the link in a new tab to use the print
page instead, and select **Generate PDF** there; opening or reloading the print
page does not start it. The library's tables link each document's page, not its
PDF: open the document, then use its Generate PDF action. The selected edition includes its own notes,
appendices, references, revision and rights notices. Companions, such as a
proper's concise study or homily, select their own TeX entrypoint.

Native PDF generation is the only print format. The site no longer prepares
HTML editions for the browser's own Print or Save as PDF command; applied to a
web reader, that command prints the page as shown, with different typography
and pagination. Use the generated PDF for the designed layout; follow its
paper, scale and duplex instructions when printing cards or paired pages.
Generation alone is not a new physical-printer inspection.

The browser-native implementation uses WebAssembly TeX and verified source,
package and font files. It assembles the requested edition from its canonical
sections and current shared styles, then typesets that selection. Changes to
style or structure update these inputs without rebuilding gigabytes of PDFs
before site publication. A first request may download the required engine and
fonts; progress and errors remain visible. Generation time depends on the
edition, device and connection.

The runtime loads common TeX files first and fetches additional verified font
data when the typesetter needs it. It retries from fresh inputs when more font
data is required and can use the complete original inventory. The edition
retains its original fonts throughout.

Repeated sections and styles share verified source objects across editions;
bounded compressed transfers reduce repetition without changing the TeX files
the engine sees. PDF generation includes every image selected by the edition.

A generated file can be saved by the reader. A disposable browser cache may
reuse an exact result only while its source, style and typesetter identities
still match. That cache is optional and supplies no publication authority;
neither a saved file nor an earlier printing substitutes for current inputs.
Native TeX remains responsible for the authored layout.

Where an edition offers **Earlier printed edition**, that link preserves a verified
historical fixed layout in the external archive. It is distinct from a newly
generated current print edition. The exact public snapshot,
PDF hashes and delivery are recorded in `release/print-archive.json`.

The shared provider style uses fast lossless PDF stream compression. In one
recorded 11-page dictionary comparison, changing compression level 9 to 1
reduced generation from 36.553 to 4.424 seconds and increased the PDF from
17.73 to 19.78 MB. All eleven page rasters at 144 DPI, extracted text and font
inventories matched. This was a desktop Chromium case with local delivery,
not a physical-device or cold-network timing promise. The
[compression review](../workflows/reviews/no-pdfs-recovery-2026-11-03/compression.json)
records the exact outputs and limits; Bible, reading-plan and papal styles
are separate and unchanged by this setting.

## Generate one edition locally

For a local build using the selected recipe's installed TeX toolchain, run
these commands from the repository root:

```sh
tools/print-document list --family publication --provider gpt
tools/print-document check --document publication:gpt/theology/angelology
tools/print-document build --document publication:gpt/theology/angelology --out .scratch/print/angelology
```

`--out` is an output directory. The command reports the selected recipe,
dependencies, generated files and receipt. The default destination is under
`.scratch/print-document/`. It does not install files into a tracked tree,
publish a download, or build other documents.

For a proper with declared companions, select its canonical leaf and edition:

```sh
tools/print-document build --document publication:gpt/liturgy/roman-rite/1962/propers/temporal/f02-all-saints --edition synthesis --out .scratch/print/all-saints-synthesis
```

`--edition main` selects the canonical publication; `research` and `full`
are aliases for it. `synthesis` and `homily` are available only where the
source owner declares them. List the actual recipes before choosing an edition.

Provider-neutral source editions use their own identities:

| Identity | Selects |
| --- | --- |
| `publication:gpt/<leaf>` or `publication:claude/<leaf>` | One provider publication and its selected edition. |
| `bible:<id>` | One publishable Bible edition under its own rights. |
| `reading-plan:<volume>` | One declared reading-plan volume. |
| `papal:<id>/<language>` | One admitted papal source reading selection. |

Use `tools/print-document list --family bible`, `--family reading-plan`, or
`--family papal` to obtain exact available IDs. Bibles and reading-plan
recipes can also emit standalone TeX with `--output-format tex`; this prepares
the source without compiling a PDF. Check `tools/print-document build --help`
for supported formats and options.

## Dependencies and review

The print command validates the selected canonical inputs and uses the owning
typesetter. A PDF build needs that recipe's TeX engine, packages and fonts;
the command reports a missing dependency instead of generating a substitute.
Existing authored typography, artwork, content selection and source notices
remain part of the recipe.

Every admitted edition is also compiled before the site deploys. The Pages
`print-compile` matrix divides the sorted admission list into eight disjoint
partitions. Each runner prepares its bundles from the checkout and typesets
them in the pinned TeX Live toolchain with the engine the bundle names and
the browser's pass policy.
It also exports its source partition for the Pages writer and verifier. Each
independently checks the Actions archive digests, source revision, admitted
editions and checkout inputs, then reassembles the full catalog with its
shared text and source packs.
Locally, `make check-native-print-compile` prepares and compiles the entire
set. The gate requires a PDF and settled references within each edition's
pass limit, exact admission membership, and closure over the bundle and the
browser runtime's `texFiles`. Only `texmf.cnf`, `ls-R` and the engine format
are exempt. XeTeX sees only the runtime's font faces.
Before deployment, a read-only verification job checks all eight sets of
successful receipts against the exact site that passed artifact verification.
It matches every edition ID, mounted file and invocation identity, and source
revision. Shared text can be packaged differently in a partition. The site
check verifies raw assets and the contents of its gzip source packs.
The native engine checks establish source and runtime closure. The browser
produces its own PDF with WebAssembly. Each runner discards its temporary
PDFs and retains the per-edition receipts and shard summary as a workflow
artifact.

Source and evidence review, print-template review, and inspection of one
rendering are separate facts. A successful build is not a new visual review
or publication approval. When issuing a reviewed print edition, follow the
owning profile and [repository print-review contract](../guidance/repository.md#build-and-review-contract),
including exact page/duplex requirements and a receipt for the actual output
and pages inspected. Keep generated files and review rasters outside Git.

Exact binary source evidence is optional local data, resolved through
`src/sources/artifact-delivery.json`. To inspect it offline, obtain the
relevant verified archive and explicitly hydrate it as described in
[the source-library contract](../guidance/sources.md#exact-binary-delivery-and-offline-access).
A normal site build does not fetch that archive. Access and redistribution
remain governed by each source's rights, even when a print recipe exists.

Old PDF links may now open an identified reader or a page explaining the
print options. A historical binary download is offered only when its exact
archive delivery is verified; the current print recipe need not reproduce
its old bytes. Source removal does not erase PDF objects from Git history or
shrink a full-history clone.
