# Agent Instructions — Commit and Preserve Mass Pictographic Structural Corpus

## Objective
Take the contents of this handoff package and create a clean repository checkpoint that preserves the approved structural corpus for the **spoken 1962 Low Mass with two servers**.

## Inputs
This package contains:
- `artifacts/mass-pictographic-core-v0.21/`
- `HANDOFF-SUMMARY.md`
- `PLAN-OUTLINE.md`
- this instruction file

## Tasks

1. **Inspect the current repository state**
   - determine the correct location in the repo for this corpus,
   - avoid overwriting unrelated in-flight work without review.

2. **Import the structural corpus**
   - add the `mass-pictographic-core-v0.21` materials to an appropriate project path,
   - preserve filenames and versions,
   - do not silently discard YAML, SVG, or PNG artifacts.

3. **Add handoff documentation**
   - incorporate the handoff summary and plan outline into a durable documentation location,
   - preserve the approved corrections and invariants.

4. **Document current status**
   - note that the 1962 Low Mass structural pass is complete through v0.21,
   - note that artistic rendering has not yet begun,
   - note that High Mass / Pontifical / postconciliar are still pending.

5. **Create a clean commit**
   - commit message should make clear this is a structural-corpus checkpoint,
   - suggested message:
     - `Add approved structural corpus for 1962 Low Mass mass pictographic dictionary (v0.21)`

6. **Report back**
   - branch name,
   - commit hash,
   - files added / changed,
   - any uncertainties about placement.

## Constraints
- Do not reinterpret the approved rubrical corrections unless there is an obvious transcription error.
- Preserve the distinctions about:
  - two-server Low Mass,
  - missal transfer roles,
  - AC1-only ablutions,
  - bell profiles,
  - coordinated post-ablution crossings,
  - 1962 dismissal branching.
- This checkpoint is a preservation step, not a redesign step.

## After the commit
The next human-guided web review lane should begin the **publication-quality artistic render pass**, using this structural corpus as the deterministic base.
