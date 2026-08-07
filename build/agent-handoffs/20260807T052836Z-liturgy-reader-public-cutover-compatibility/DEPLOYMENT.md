# Deployment observations

- Compatibility implementation: `3f3949617a04ffa68a1070058d0f7bc5ac74dc93`.
- Successful Pages run: `31148986910`.
- Evidence-only checkpoint: `998648c341691c0807b0c209f93fbae16d641d48`.
- Successful Pages run: `31150296458`.

Direct post-run checks returned HTTP 200 for retained Day and Propers pages,
their changed controllers/styles, shared state, and both legacy canonical
routes. Changed CSS/JS matched source; built candidate HTML matched deployed
HTML. Retained candidates were statically noindex and canonical pages remained
indexable.

Run `31128301816` for older planning commit `5e1b82b51` was cancelled after it
remained queued/waiting since the prior day and blocked the current run. It is
not a successful deployment and does not qualify any product byte.

The proposed canonical patch is not deployed because it is not applied or
authorized. A later execution must obtain a new successful Pages result for
its exact SHA and repeat direct and post-600-second cache checks.
