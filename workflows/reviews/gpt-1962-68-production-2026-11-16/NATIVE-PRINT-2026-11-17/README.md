# Selected native print compilation

The summary and three receipts preserve the native compiler's exact JSON
for the renewed study, concise study and homily at source checkpoint
`c5e60649b7b67596e6e3c0e73912fe76a083b732`. The historical 16 November
records are unchanged.

`tools/native-print-compile prepare` selected only these three admitted
publication identities. `tools/native-print-compile compile --jobs 3`
settled each after two passes, with no reported problems:

| Edition | Pages | PDF bytes |
| --- | ---: | ---: |
| Expansive study | 26 | 558,586 |
| Concise study | 10 | 419,721 |
| Homily | 3 | 301,722 |

The existing `check-proper-components` artifact-phase validator passes
against disposable byte-identical copies of the PDFs and their settled
aux/log files. This checks the page limits, the concise edition's absolute
opening-page markers and embedded Latin Modern fonts. The existing
`check-generation-metadata --pdf` validator also passes for all three.
The study and concise metadata checks pass on their 300-second reruns
after initial 100-second timeouts.

The homily exceeds the 75 KiB-per-page investigation threshold at about
98.2 KiB per page. Inspection finds twelve embedded, subset Latin Modern
font records and no raster images. Its absolute size remains 301,722
bytes. The standard shared typography and lossless compression policy
are retained; no local font, geometry, counter, padding or compression
override is introduced.

The isolated Arch TeX Live 2026 host validates the pinned native runtime
file closure. Its `pdftex.map` has different bytes, as the exact receipts
report. This does not establish pinned-container or browser-WebAssembly
byte identity.

The PDFs are disposable verification outputs, not tracked or installed
print editions. There is no full-page visual inspection or print-layout
acceptance. This selected run is not the complete admitted-edition Pages
compilation gate.
