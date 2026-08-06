# Prototype to production

The accepted prototype supplies presentation only. Production keeps ownership
of URL/state, Day and Propers resolution, Proper and Ordinary renderers,
Ordinary seating, semantic event order, absence reasons, focus, surfaces, and
render races.

| Accepted hook | Production owner |
| --- | --- |
| masthead and Instrument tokens | new scoped `reader-instrument.css` and stable HTML hooks |
| Read axis and measure | existing `.reader-document`/Proper DOM, scoped CSS |
| Missal cue grid | existing renderer nodes and semantic locations, scoped CSS |
| rail/dock and open surfaces | existing `reader-shell.js` behavior, scoped CSS |
| mode styling | authoritative Day commit exposed as `data-reader-mode` |
| compact uncompiled warning | existing source-owned node moved into `coverage-notice` before commit |
| grouped inline absences | direct existing Ordinary notice nodes wrapped without changed text or IDs |
| Propers Browse | existing production form; prototype search remains deferred |

The visual harness navigates the accepted and production pages with identical
state, viewport, scroll, zoom/media, and open-surface inputs and records both
screenshots and geometry.

