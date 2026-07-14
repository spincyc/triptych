---
name: audit
description: Audit an existing Triptych document, corpus, shared-source system, or publication path. Use for evidence-backed source, doctrine, law, history, metadata, build, layout, PDF, or catalog checks; remain report-only unless remediation is explicit.
---

# Audit

Perform an evidence-backed audit of a document, corpus, shared-source system, or publication path. The default mode reports findings without editing; use `fix` or equivalent explicit language to authorize remediation.

## What to provide

Treat the user's complete request and thread context as controlling input, whether it follows the suggestions below or is entirely free-form.

- The target title, path, collection, document set, or claimed property to audit.
- Audit dimensions such as doctrine, canon law, liturgical text, history, quotations, citations, private revelation, completeness, source records, AI metadata, shared ownership, build, layout, installed PDFs, or catalog links.
- Whether the desired mode is `report` or `fix`, the as-of date or external standard, and the desired severity threshold.
- Suspected defects, known sources, exclusions, deliverable format, and all free-form context, guides, limits, staging, or commit instructions.

## Preflight

1. Read `../../references/conventions.md` completely, apply it, route the target to every controlling profile, and inspect its source, records, consumers, build artifacts, installed PDF, and catalog entry.
2. Treat a request without clear remediation authority as report-only. Diagnostic builds and read-only checks are allowed; source, PDF, catalog, guidance, and Git changes are not.
3. Define the audit population, sampling policy if any, authority hierarchy, currentness boundary, and pass/fail criteria before drawing conclusions.
4. If auditing PDFs or layout, establish whether the installed file matches the current build before attributing a defect to the source.

## Plan

List the audit dimensions, governing standards, files and artifacts examined, reproducible checks, claim samples or full population, severity model, and—only in fix mode—the remediation and verification boundary.

## Actions

1. Inspect before editing. Trace each material claim or defect to the authoritative source, research record, canonical fragment, build rule, or publication artifact responsible for it.
2. Classify findings by consequence and confidence. Give exact file and line or page locations, evidence, controlling rule, and the smallest coherent remedy.
3. Distinguish factual error, unsupported assertion, incomplete evidence, stale mutable fact, doctrinal or legal category error, editorial judgment, metadata defect, rendering defect, and optional enhancement.
4. In report mode, make no tracked changes and do not silently repair findings. In fix mode, remediate only the authorized population and update all required records, metadata, consumers, guidance, catalogs, and PDFs.
5. Re-run the same tests after remediation and add profile-specific gates; do not close a finding merely because the text changed.
6. Commit only when the user explicitly authorizes it, grouping fixes into coherent reviewable stages with substantive `AI summary:` bodies.

## Verification

Confirm the audit covered the declared population, every finding is reproducible and evidence-linked, severity and confidence are justified, report-only boundaries were respected, and any remediated source, consumer, PDF, and catalog passes its governing completion gates.

## Summary

Lead with the audit verdict and finding counts by severity; then give the most consequential findings, scope and checks, fixes and commits if authorized, artifacts verified, false positives rejected, and limitations.

## Next Steps

Name the single highest-priority unresolved finding, missing source, or independent review.
