# Round 1 shell measurements

| State | Reviewed | Corrected | Delta / disposition |
| --- | --- | --- | --- |
| 1024×768 Read dock | x 232.5, width 544, y 686; radius 12.8px; 97% panel; 12×40px shadow | x 0, width 1009 layout px, y 698; radius 0; opaque `rgb(250, 248, 242)`; no shadow; 2px rule | Direct edge ownership; four named 239.05–239.06×68px targets; final content clears dock at maximum scroll |
| 1024×768 Read text | first principal text y 299.23, width 636 | y 299.23, width 636 | No accepted geometry change |
| 768×1024 Read | first text y 267.39, width 636/about 75 characters | y 267.39, width 636/about 75 characters | Accepted measure unchanged; residual dock shadow removed |
| 393×852 at 200% | 393×144.39 four-column dock; three labels split inside words | 393×245.19 two-column/two-row dock; four 178.91×104 targets | Every label remains one line; no clip, text shrink, or horizontal overflow |
| 200% first text | y 1027.28, width 311 | y 1027.28, width 311 | Accepted high-zoom reading geometry unchanged |

`evidence/capture-metadata.json` contains per-capture URL/hash, viewport,
scroll, shell/button/label geometry, focus/semantic state, overflow, console,
request, and HTTP results. `evidence/browser-results.json` records the 15/15
authoritative assertion disposition. The ephemeral loopback origin was
normalized to `https://preview.invalid`; every path, query, hash, and measured
value remains exact.
