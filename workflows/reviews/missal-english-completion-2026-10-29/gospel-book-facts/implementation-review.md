# Bounded Gospel book-facts review

Accept the corrected code at these exact SHA-256 values:

| Subject | SHA-256 |
| --- | --- |
| `src/web/browser/liturgy/ordinary-seating.js` | `90467f26022701a79cfee246c131de8776a6226f208cde0c5bc30010aaa3b5ba` |
| `src/web/browser/liturgy/reader-state-adapters.js` | `8dfa04ac0d4dd56a80aef3cefdbdd3d3d18a61cb6de444af50888ee8a307723f` |
| `tools/mass-today` | `5786300fa910d5011e85a4dffd985da8dab8a3f8ab2d58d1254e833d3182fa45` |
| `tools/tests/test_gospel_book_facts.py` | `05064c9ffed968ae95cb945ec7bacd18d9eb1782a215feb7f4546cadd3535c8b` |
| `tools/tests/gospel_book_facts.mjs` | `effa4917976c02baf9020836211b195ef5a0aa884af90b0dc44172520f44fa13` |

The initial implementation inspected only selected cycle citations, while the
existing material selector emits the parent-plus-selected union. Four independent
counterexamples demonstrated incorrect certainty for conflicting/unresolved/
non-Gospel parent citations and a missed known parent-only citation. The owner
corrected this with shared `properCitations`, retained exact original CLI source
rows before cycle flattening, and kept those rows in private attributes outside
the public JSON dictionary.

The final derivation consumes applicable prepared Gospel owners and exact source
indices, honors source-path material selection and explicit alternatives, requires
all applicable citations to agree on one of four canonical books, and retains
unknowns for missing/invalid/unresolved/contradictory evidence. Query fields and
role labels do not appoint a book. Duplicate source indices return unknown.

Verification at the listed hashes:

- All six independent Gospel controls pass, including all four initial failures.
- Four independent applicability and held-offer controls pass: one applicable
  witness, unknown/inapplicable withholding, two-witness choice, and separate
  source-offer versus held-element coverage counts.
- The owner's three focused Python groups pass, including its eleven Node cases,
  browser adapter reference projection and both CLI-cycle/raw-parent groups.
- Evidence: `initial-independent.log`, `final-independent.log`,
  `applicability-preservation.log`, and `owner-focused-tests.log`.

This is implementation acceptance. Actual four-heading source installation and
the broader source-sensitive integration gates remain the coordinator's owning
work; their unavailable or unsettled results are not claimed passed here.

Reviewer writes are confined to owned scratch; no subject edit, commit or push.
