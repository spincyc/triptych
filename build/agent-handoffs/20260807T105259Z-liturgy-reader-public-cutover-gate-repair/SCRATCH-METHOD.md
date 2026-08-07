# Scratch method

The first temporary clone under `/tmp` exceeded that tmpfs quota and was
discarded. Validation used a separate shared-object clone at
`build/gate-repair-scratch.u1lspq/repo`, checked out directly at
`e20b2f542ab51a2b4f0807e6394ca5ecb313699c`. This is not a Git worktree.

The rejected patch was applied there as a draft. Only the authorized 19 paths
were allowed to differ. The four named test/harness boundaries and one further
stale selector in the already-authorized Day harness were repaired. The clone
was never pushed and no workflow/deployment command was invoked.

The corrected patch was generated as a normal-context full-index diff from the
scratch tree back to the unchanged baseline, then apply-checked in the real
checkout.
