# Bounded visual decisions

1. Preserve the accepted external ruled rail at `min-width: 72rem`.
2. At `max-width: 71.999rem`, transition Instrument directly to an opaque,
   square, shadowless, edge-bound dock with a two-pixel top rule.
3. Use the existing block-end reserve so no final content is hidden beneath the
   permanent dock; assert the clearance at maximum scroll.
4. Make the reader shell a named inline-size container. At at most `18rem` in
   the current root-font measure, reflow only Instrument's actions to a labeled
   2×2 grid.
5. Preserve visible whole labels, accessible names, at least 44×44 CSS-pixel
   targets, focus indication, forced-color support, and zero horizontal
   overflow. Do not counter-scale text.

No accepted composition decision was reopened.
