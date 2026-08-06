# Independent public-cutover-plan review request

Please give explicit PASS/FAIL dispositions—not a general “looks good”—for:

1. Is same-path source promotion behind unchanged `day.html` and `index.html`
   the smallest safe mechanism?
2. Does the plan preserve the existing Day and Propers URL/state contracts?
3. Is the proposed diff limited to cutover rather than redesign or refactor?
4. Are relative paths, indexing, caching, GitHub Pages, and mixed-cache risks
   handled?
5. Is ordinary-revert rollback immediate, complete, and testable?
6. Are local, canonical-route, visual-oracle, accessibility, publication,
   deployment, and post-cache-window gates sufficient?
7. Is the Day first-visit test genuinely deterministic without weakening the
   empty-URL/default-date contract?
8. Is the plan exact enough for a later clean agent to execute without a new
   architectural decision?

Please also disposition each proposed public-contract decision:

- accept Roman 1962 as the repository-declared empty-Day default, or require
  legacy manifest-order postconciliar behavior;
- require existing production reasoning/territorial outcomes inside the
  Instrument shell, or accept the narrower explicit fail-closed treatment;
- accept public `cycle`, `alternative`, and `translation-witness` keys;
- require source-static noindex/noarchive and route-neutral metadata on
  retained candidates;
- approve removal of internal/candidate diagnostics on canonical routes;
- approve a quiet direct Day↔Propers counterpart link with contextual links in
  Details, or specify another exact accepted location;
- require regeneration of `PROPOSED-CUTOVER.patch` after those dispositions
  before execution authorization (Codex recommends yes).

Possible result: request planning changes, or accept the plan and separately
authorize a later execution phase. Public navigation and public cutover remain
unauthorized until explicitly stated.
