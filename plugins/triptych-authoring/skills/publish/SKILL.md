---
name: publish
description: Build, inspect, install, catalog, and optionally commit completed Triptych documents. Use when substantive source work is complete and one or more affected publications must pass their repository and profile gates.
---

# Publish

Take completed source work through the repository’s publication gates without treating publication as permission for unrelated substantive expansion or external release.

## What to provide

Treat the user's complete request and thread context as controlling input, whether it follows the suggestions below or is entirely free-form.

- The source leaf, document title, collection, build target, or set of mutually dependent documents to publish.
- The desired stopping point: validate only, build, visually review, install, catalog, commit, or the complete in-repository sequence.
- Whether installed PDF changes and a Git commit are authorized, how coherent stages should be grouped, and any required commit subject.
- Release constraints, expected versions, known warnings, deadlines, exclusions, and all free-form context, guides, limits, or special verification requests.

## Preflight

1. Read `../../references/conventions.md` completely, apply it, read every controlling profile, and inspect the target source, research records, generation metadata, dependencies, current build and installed artifacts, README row, and worktree.
2. Determine every consumer affected by shared source changes and expand the build set only to those necessary consumers.
3. Check that substantive content and profile-required research records are complete. Fix only defects that block the authorized publication stage; report broader editorial opportunities separately.
4. Treat in-repository installation and Git commits as separate permissions. This skill never authorizes external hosting, release creation, pushing, or history rewriting.

## Plan

State the exact targets and consumers, validation gates, build pass count, log checks, visual-inspection method, installation and byte-identity checks, catalog changes, and authorized commit grouping.

## Actions

1. Validate structured generation metadata, source-record completeness, links, imports, canonical shared ownership, and profile-specific completion prerequisites.
2. Build every target for enough passes to settle contents, references, indexes, and cross-document dependencies. Keep intermediates under `build/`.
3. Inspect logs for fatal errors, undefined references, overflow, suspicious font substitution, and layout warnings. Resolve or explicitly justify every material warning.
4. Visually inspect every page of every affected PDF for clipping, collision, orphaned headings, broken tables, blank pages, hyperlink problems, and inconsistent metadata or running matter.
5. Install only reviewed PDFs under the mirrored `doc/` path, confirm byte identity with the reviewed build, and update the README so each named document artifact occupies its own column.
6. Review the complete staged diff and commit only when authorized. Use a concise subject plus a substantive `AI summary:` body covering changes, verification, and limitations.
7. Leave unrelated worktree changes untouched and report any requested publication step that was not performed.

## Verification

Re-run universal and profile gates; check settled builds, clean material logs, every-page review, PDF structure and fonts where applicable, installed/build byte identity, catalog and local links, staged-file coherence, and the final worktree state.

## Summary

Lead with the publication state reached; then list targets and consumers, PDFs installed, catalog changes, verification evidence, commit if authorized, warnings accepted, and any withheld or external step.

## Next Steps

Name only the one remaining in-repository review or separately authorized external action, if any.
