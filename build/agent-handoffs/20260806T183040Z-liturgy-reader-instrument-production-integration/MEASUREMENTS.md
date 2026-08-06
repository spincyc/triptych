# Prototype-to-production measurements

| Governing state | Accepted prototype | Production candidate | Delta / disposition |
| --- | --- | --- | --- |
| Day Read 768×1024 | width 636px; ~75 characters; first text y 267.39 | width 636px; ~75 characters; first text y 268.03 | exact measure; +0.64px text position |
| Day Missal 393×852 | 351px plane; first text y 324.09 | 351px plane; first text y 320.66 | exact plane; production 3.43px earlier |
| 200% at 393×852 | four 178.91×104px targets; one-line labels | same geometry and one-line labels | exact shell reflow; no clip or overflow |
| 1024 dock | opaque, square, shadowless, edge-bound | same computed shell properties and reserved end space | pass |

The 19/19 governed assertions span 100 captures, including 23 exact
prototype/production pairs. The capture metadata records URL/hash, viewport,
scroll, semantic state, geometry, target names/sizes, overflow, focus, console,
requests, and HTTP status. Browser results record zero console, failed-request,
HTTP, unnamed-control, duplicate-ID, and required-overflow failures.

Asset hashes are recorded in `evidence/browser-results.json` and the canonical
continuity file. No measurement is manufactured.

