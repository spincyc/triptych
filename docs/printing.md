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

The reviewed web readers keep their reading presentation. Their Print action
opens the corresponding complete edition. Select **Generate PDF** on that page
to start generation; opening or reloading the page does not start it. The
selected edition includes its own notes, appendices, references, revision and
rights notices. Companions, such as a proper's concise study or homily, select
their own TeX entrypoint.

Native PDF generation replaces browser reflow as the complete-edition print
format. A browser's Print or Save as PDF command applied to an HTML reader uses
different typography and pagination. Use the generated PDF for the designed
layout; follow its paper, scale and duplex instructions when printing cards or
paired pages. Generation alone is not a new physical-printer inspection.

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
the engine sees. Illustrated HTML readers may defer offscreen images, while
PDF generation still includes every image selected by the edition.

A generated file can be saved by the reader. A disposable browser cache may
reuse an exact result only while its source, style and typesetter identities
still match. That cache is optional and supplies no publication authority;
neither a saved file nor an earlier printing substitutes for current inputs.
Native TeX remains responsible for the authored layout; printing the HTML
reader does not reproduce that layout.

Where an edition offers **Earlier printed edition**, that link preserves a verified
historical fixed layout in the external archive. It is distinct from browser
reflow and from a newly generated current print edition. The exact public snapshot,
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
`print-compile` job (locally `make check-native-print-compile`) prepares the
exact source bundle the site serves for each admitted edition and typesets it
in the pinned TeX Live toolchain with the engine the bundle names and the
browser's pass policy. It fails when an edition does not compile, produces no
PDF or does not settle within the bundle's maximum passes; when the admitted and
prepared sets differ; or when any edition opens a file that is neither in its
bundle nor in the browser runtime's `texFiles` (only `texmf.cnf`, `ls-R` and
the engine's format are exempt). XeTeX sees only the runtime's font faces.
The deploy job waits for it. The native engines are not the WebAssembly ones,
so a pass proves the bundle and runtime closure, not byte identity with a
browser-made PDF. Its PDFs are discarded; per-edition receipts and a summary
are kept as a workflow artifact.

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
