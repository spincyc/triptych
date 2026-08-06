# Context

Independent review selected Liturgical Instrument from a three-direction reset
package. The reviewed end commit was
`0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113`; the current implementation is
`62e712a1962080d1dc3c6e106651c41afbf7531b`.

This pass is a visual correction and evidence task. It does not replace public
Day or Propers, alter liturgical data, add deferred modes, or execute production
integration. The prototype remains unlinked and noindex. The accepted shared
state contract, Day/Propers adapters, Proper and Ordinary renderers, single
Ordinary seating path, semantic restoration, focus lifecycle, render-race
ownership, invalid-state refusal, and production routes remain byte-isolated.

The seven governing findings were: detached widget-like shell; late Missal
opening; empty Read gutter; over-broad 768 portrait measure; overpowering
partial warnings; provisional circular T/progress dash; and unfinished mobile
spacing/title wrapping. `PLAN-AND-CONTINUITY.md` records the exact reviewer
language and Codex response.
