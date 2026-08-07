# Cache-window verification

The accepted observed static freshness window is 600 seconds. The immediate
pass completed at `2026-08-07T12:16:10.158Z`. The post-window verifier refuses
to start before 601 elapsed seconds and uses a fresh Chrome profile, ordinary
cache behavior, plain canonical URLs, and no cache-busting request headers.

The post-window pass began after 613 elapsed seconds and completed at
`2026-08-07T12:26:32.943Z`. It used no cache-busting query or request headers.

Result: PASS, 216/216 assertions over six required canonical states: empty Day,
governing Day deep link, Day Missal, governing Propers deep link, mobile Details,
and territorial Why. There were zero console, failed-request, HTTP, accessibility-
name, duplicate-ID, or overflow problems. All 15 canonical/candidate/oracle and
shared reader assets remained HTTP 200, unredirected, and byte-identical to the
locked build. Responses retained `max-age=600`, the deployed `Last-Modified`
timestamp, and the expected ETags; observed Age values were fresh single digits.
No mixed-generation behavior appeared and no rollback trigger fired.

Machine result: `evidence/live/post-window/browser-results.json`.
