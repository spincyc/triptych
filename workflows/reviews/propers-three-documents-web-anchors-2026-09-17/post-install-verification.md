# Post-installation verification

After the independently reviewed postconciliar canonical web edition was
installed and staged, the coordinator reran the exact case previously blocked
by its absence:

```text
python3 -m unittest tools.tests.test_public_alpha.PublicAlphaTest.test_no_site_page_renders_a_fence_as_running_prose
```

Exit status: **0**. One test passed. The unmodified concise output is
[post-install-fence-regression.txt](post-install-fence-regression.txt).

This resolves that case against the legitimately installed publication. It
does not rewrite the historical combined command: that earlier 199-test run
returned 198 passes and one missing-file error, also reproduced using the
baseline tool and test. The whole 199-test command was not rerun.

Current renderer SHA-256:
`ac4d7145e7b9886042db03c1a4a38923386bf002956602f06186f0674d860251`.
Installed postconciliar canonical Markdown SHA-256:
`ac4cdbecab8f07b38803ca3168c174d49cc1b6d22c584697bb1ca4252f5e19b7`.
The exact web conversion had already passed independent web review iteration 1.
This check does not assert terminal workflow or full deployment acceptance.

The coordinator also ran the actual `tmt check` after the two-label renderer
correction; exit status 0, output `ok`. Scoped release bindings were refreshed
only for the reviewed renderer and later the installed postconciliar web, its
own catalog, and the regenerated document projection. The final integration
review separately verifies the resulting shared state.
