# Aquinas nature, knowledge, grace, and fall: source audit

> Retained research record, consolidated 2026-09-29. Scratch filenames identify the original acquisition history, not required runtime dependencies. Current durable identities and fingerprints are in [source-bindings.toml](../source-bindings.toml); the [source-audit index](../source-audit.md) records controlling corrections and reading scopes.


Access date: 2026-09-29. Authoring lane: aquinas_nature. These notes describe the evidence actually inspected, not every work mentioned by an authority in the Summa. All exposition is independently composed; no earlier Claude angelology prose supplied it.

## Complete Summa reading

Primary witness: Thomas Aquinas, *Summa theologiae*, Prima Pars, English Dominican Province translation, Benziger Brothers, New York, Project Gutenberg ebook 17611. The electronic title identifies the translators and publisher but does not establish a printing year. Gutenberg credits Sandra K. Perry and David McClamrock; release 2006-01-26, updated 2021-01-03. Catalog: https://www.gutenberg.org/ebooks/17611 . Exact downloaded text: https://www.gutenberg.org/cache/epub/17611/pg17611.txt . Gutenberg marks this text public domain in the USA. This is a transcription, not an inspected facsimile of a Benziger printing.

Retained raw bytes: `summa-prima.txt`, 2,911,941 bytes, SHA256 `c9443221a31768991db4bbe37e6ed035b278143a6728af64dc8ba0cf8e79154d`. The local `q50.txt` through `q64.txt` are working extracts from those bytes. Complete questions I.50–64 were read, including every objection, sed contra, determination, and reply. Truncated display portions were reopened to complete the reading. Census: 72 articles, respectively 5, 3, 3, 3, 5, 3, 3, 5, 7, 4, 5, 4, 9, 9, 4. The JSON inventory preserves each article separately rather than treating a question's doctrinal grade as uniform.

Known witness problems: I.50.2 has `individual substance` where the Latin reads `substantia intellectualis`; I.60's Third Article carries an erroneous bracketed article number 4; I.62's Ninth Article carries erroneous bracketed article number 3. Numbering follows ordinal article headings and the question's contents, checked against Latin. I.57.3 reply 3 repeats a phrase in this witness. I.61.1's Augustine reference `XI, 50` is not adopted as a verified original locus.

Existing work ID: `work.thomas-aquinas.summa-theologiae`.

## Direct Latin controls and parallel loci

The following exact Corpus Thomisticum HTML files were fetched and their relevant Latin read through local text projections. Complete downloaded files do not imply complete reading. These are modern electronic witnesses to medieval texts, with edition-specific transcription/editing; no manuscript or printed facsimile collation is claimed.

| Work and URL | Edition stated by witness | Actual locus read | Retained raw file and SHA256 |
|---|---|---|---|
| Summa I.50–64, https://www.corpusthomisticum.org/sth1050.html | Leonine, Rome 1889; Busa electronic text, Alarcón revision | I.50.2 corpus [30565], I.60.3 corpus [30911], I.62.9 corpus [31037] | `sth1050.html`; `e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7` |
| De veritate q.8, https://www.corpusthomisticum.org/qdv08.html | Text adjusted to Leonine 1972 from corrected proofs; Busa/Alarcón | Complete corpora of q.8 aa.9, 12, 14, 15, not their entire disputed articles | `qdv08.html`; `9b15fb2b63b70db664ba953a6a9a1ea349d3895482cd6a6cdb872dab817a1ec3` |
| De malo q.16, https://www.corpusthomisticum.org/qdm16.html | Turin 1953; Busa/Alarcón | Complete corpora of q.16 aa.2–6, not their entire disputed articles | `qdm16.html`; `125185866e21f915d9d469dd101e266842cd4ab6bee62ed7d57c7ad6515dcc62` |
| De ente et essentia, https://www.corpusthomisticum.org/oee.html | Baur 1933 with Koch corrections; Busa/Alarcón | Complete cap.3 [69874], beginning *Nunc restat videre*, and cap.4 [69875], beginning *His igitur visis* | `oee.html`; `4fbd17e8136d920cd929f7b67fca45693f15eccdf4db7495bd16f9bcca119bb7` |

The De ente chapter numbering differs from some familiar editions; the incipits in the essay footnote identify the actual passages. De malo 16.4 develops the first-instant argument through the order of natural knowledge and supernatural orientation; ST I.63.5 argues from initial divine causality. The essay preserves that difference. De malo 16.3 concentrates on refusing dependence on grace; ST I.63.3 gives two linked accounts of the desired likeness to God.

Existing work IDs: `work.thomas-aquinas.de-veritate`, `work.thomas-aquinas.de-malo`, `work.thomas-aquinas.de-ente-et-essentia`.

## Patristic and catechetical direct reading

These were first inspected as browser-returned New Advent/Vatican primary texts. The source-library lane subsequently retained New Advent raw HTML and mechanical text projections. This lane then independently read the full relevant passages in `.scratch/source-library/gregory-or38.txt` (IX–X), `augustine-cdg12.txt` (7–9), and `augustine-cdg14.txt` (3–4), confirming the relevant content and binding this added inspection to the retained artifacts. Damascene and Catechism here remain browser inspections; other lanes handle their retained-artifact review.

- John Damascene, *Exposition of the Orthodox Faith* II.3–4, complete: https://www.newadvent.org/fathers/33042.htm . S. D. F. Salmond translation, controlled by the CCEL NPNF second series vol.9 Edinburgh 1898 title and volume header; New Advent is an additional hosted transcription whose 1899 volume-level footer does not control constituent authorship or the selected printing. Used for the spiritual/circumscribed nature, uncertainty of essential equality, earlier creation, earthly ruler, and irreversibility of fall. Existing work ID: `work.john-of-damascus.de-fide-orthodoxa`.
- Gregory Nazianzen, Oration 38.9–10, complete (surrounding §§7–11 were also displayed): https://www.newadvent.org/fathers/310238.htm . Browne/Swallow translation, NPNF second series vol.7 (1894), hosted transcription. Used for intellectual creation followed by material creation. No independent Greek collation.
- Augustine, *City of God* XII.7–9, complete: https://www.newadvent.org/fathers/120112.htm ; XIV.3–4, complete: https://www.newadvent.org/fathers/120114.htm . Marcus Dods translation, NPNF first series vol.2 (1887), hosted transcription. Used for the deficient origin of evil will, creation of nature and holy love, and incorporeal pride/envy. Existing work ID: `work.augustine.de-civitate-dei`. Other Augustine loci in the dossiers are expressly Aquinas's received authorities, not independently collated original passages in this lane.
- Catechism of the Catholic Church §§327–330, https://www.vatican.va/archive/ENG0015/__P1A.HTM ; §§391–395, https://www.vatican.va/archive/ENG0015/__P1C.HTM . Official English web text, directly inspected. Used for spiritual intelligent willing personal beings, immortality, created goodness, voluntary evil, irreversibility, and the bounded power of Satan. This lane used the Catechism's quotation and reference for Lateran IV; the opening audit records root's subsequent direct inspection of DS800–801 Latin and an English control. The integrated publication therefore has council-level evidence, without retroactively attributing that reading to this lane.

## Verification ceiling and integration

The essay distinguishes independent patristic reading from Aquinas's use of named authorities. References to Aristotle, Avicebron, the Book of Causes, Gregory the Great, Peter Lombard, and Augustine's Literal Meaning of Genesis report what Aquinas invokes in the fully read articles. Dionysian translation differences in I.56.1 are likewise a report of Aquinas's explicit comparison, not a new Greek manuscript judgment. Scripture loci are exact citations used in these questions; no new textual-critical claims are made.

The governing profile uses `Thomist position` for Aquinas's systematic determination as such. The label does not by itself claim dissent. `Disputed` requires actual open division in the identified witnesses; lack of a consensus survey is insufficient. The durable question inventory, rather than the original scratch JSON, controls integrated proposition grades.

This lane performed source and structural checks, not a full publication build. Integrated validation and rendered review are recorded separately by root. The source library has registered the retained witnesses; source-bindings.toml supplies current exact identities and fingerprints.
