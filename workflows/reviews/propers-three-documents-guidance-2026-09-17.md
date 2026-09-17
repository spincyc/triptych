# Cold review: three-document propers guidance

Verdict: **pass for this guidance snapshot**. No blocking defects or required revisions found. This verdict does not accept the implementation, research, authored publications, rendered artifacts, or workflow run.

Reviewed the new `guidance/liturgy/propers-three-documents.md` and changes to both proper profiles, `guidance/repository.md`, `guidance/web-editions.md`, and `guidance/liturgy/propers-production-plan.md`, against the supplied user-intent brief. Read the applicable workspace, personal, repository, editorial, web-edition, and proper-profile guidance. The review was independent of the authoring conversation; subject files were not edited. The final snapshot includes the added Homiletic Directory paragraph and schema-2 web-edition clarification.

## Findings

**Blockers: none. Advisories: none requiring an amendment.**

The following are review conclusions, not evidence that a future artifact meets these requirements:

- **User intent and breadth:** `propers-three-documents.md:90–116` requires two to five substantial whole-formulary interpretations, every appointed element, actual exegetical reasoning, and each interpretation's own four senses. The extent is a planning range with an explicit rejection of thin outlines, rather than a length ceiling. The older passage-by-passage reception sweep remains mandatory at lines 48–62.
- **Grouping and attribution:** lines 59–80 distinguish an editor's whole-Mass synthesis from an author's passage-level exegesis; require compatible controlling arguments; preserve narrower disagreement; and distinguish complementary emphases from contradictory identifications. These provisions do not make historical agreement or disagreement a numerical quota.
- **Concise comparison:** lines 126–143 require genuine interleaving, preservation of every interpretation's controlling claim and truth-changing qualifications, reader independence from the long document, and upstream research/review for any new source-dependent claim. They do not permit a sequence of abbreviated lane summaries to stand in for comparison.
- **Homily feasibility:** lines 147–176 permit selection of a coherent reviewed argument, require a verbatim spoken body and pertinent pedagogy, place the source apparatus outside the speech, and distinguish an estimated duration from a human delivery event. The requirement to connect Gospel, other Scripture, and prayer is proportionate to the homily's purpose; it does not impose the study's exhaustive minor-proper inventory on oral delivery.
- **Supersession and ownership:** lines 12–25, both profiles' opening schema-2 notices, and `repository.md:182–190` explicitly supersede the old fixed presentation and prose-free companion architecture while retaining source, rights, identity, edition, and branch controls. Each output may have its own authored prose within one canonical leaf. No second research owner or phantom web companion is required.
- **Homiletic source:** lines 178–184 accurately summarize the cited liturgical orientation. Independently checked the official [Homiletic Directory](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20140629_direttorio-omiletico_en.html), nos. 6–15 and 25: exegesis serves the proclamation, the prayers and readings are interpreted through the Paschal mystery, and preaching leads toward Eucharistic participation and daily life. The profile uses this as an editorial orientation and does not attribute prayer, pastoral acquaintance, or ordained ministry to an AI.
- **Web scope:** `web-editions.md:122–129` explicitly avoids claiming that the canonical HTML reproduces the companions' separately authored prose. This is consistent with the declared sole web owner and three linked PDFs.
- **Acceptance and regeneration:** lines 198–221 require fresh cold review at substantive stages, direct findings to their owning stage, invalidate downstream judgments after upstream changes, invalidate visual acceptance after render changes, and require a new run after a pinned workflow digest changes. Reused research cannot carry an unearned verdict.
- **Production boundary:** the two new authorizations in `propers-production-plan.md:69–89` do not reopen the entire closed collections or migrate earlier publications automatically. Their dated liturgical occurrence must still be proved by the research stage; this review did not independently collate the calendars.

## Verification and scope

`git diff --check -- guidance/liturgy/roman-1962-propers.md guidance/liturgy/postconciliar-propers.md guidance/repository.md guidance/web-editions.md guidance/liturgy/propers-production-plan.md` returned exit status 0. The new profile was read directly because it was untracked. Apart from the Homiletic Directory citation, no publication-source verification was part of this lane. No implementation tests, artifact builds, or page inspections were performed.

Reviewed working-tree snapshot above HEAD `b27036f9b856bd8f662f51b6e6128bd90a5ed633`:

| File | SHA-256 |
| --- | --- |
| `guidance/liturgy/propers-three-documents.md` | `a8109ac234676b722d17fc96a5a772d88aaa507ebad36079306fb47c4934752e` |
| `guidance/liturgy/roman-1962-propers.md` | `688df7fff816e29c44a0bb4953e73d2601a844463cb0dbf163366b77ff98aaba` |
| `guidance/liturgy/postconciliar-propers.md` | `3f0fe1d499f0f343756d90c6bbe2bf59c0a412834677f0d7c386694f49f29e28` |
| `guidance/repository.md` | `867feb0d3551235eda17a7b8940120f37666303634a5295ad90cc8d46f41dd80` |
| `guidance/web-editions.md` | `2f8a02f673cffcaf02a46aebd42840fce9b5310a11bd58af6fcdddcdb651ebe8` |
| `guidance/liturgy/propers-production-plan.md` | `76b95ff386c7ba9d08cecee467650087b8776f358fa3731ff3d383a1bbd3c66f` |

Only `.scratch/guidance-cold-review/review.md` was created. No commits or nested delegation.

## Supplement: independent liturgical paths

Verdict: **pass for the revised guidance snapshot below**. No blocking defects or required revisions found. The original review and its hashes above remain a record of the earlier snapshot. This supplement addresses the subsequent user clarification that the 1962 and postconciliar calendar, source, research, interpretation, document, and workflow paths must remain separate.

Read the current three-document profile completely and compared it with the previously reviewed text. Its new separation section and calendar declaration are consistent with the existing three-document contract:

- `propers-three-documents.md:29–34` gives each run exactly one calendar family and proper identity. The exclusive scope expressly covers context, appointed texts, options, research judgments, interpretation lanes, all three documents, review evidence, and publication records. A shared civil date cannot become an inferred correspondence or a combined interpretation.
- Lines 36–39 select the family from the canonical identity before date resolution, retain that family's governing books and source owner, and reject liturgical owners or authored proper components imported from the other family. This prevents the date-first approach from quietly treating the two calendars as one source of appointments.
- Lines 40–43 permit shared machinery and independent primary-source citation, while expressly prohibiting transfer of appointments, cycles, rubrical choices, or another proper guide's interpretation. In conjunction with the retained source standards and separate leaf research records, this permits reuse of an external primary witness with an independently established publication use; it does not permit one family's source judgment or review acceptance to stand in for the other's.
- Lines 243–244 bind the declared calendar to the canonical document path and require rejection of cross-family imports. This is a stated mechanical requirement, not a finding here that the checker implements it.
- The existing expansive-study, concise-comparison, homily, and downstream-review invalidation requirements are unchanged. The separation applies throughout their production, rather than only to final filenames.

`propers-production-plan.md` was byte-identical to the original review's snapshot. No separate user-clarification amendment was present in that file. It already routes the three-document contract to its owning profile and authorizes two distinct identities, so the separation rule does not need a duplicate there. This observation was reported to the coordinator before completing the supplement.

No implementation, calendar computation, source collation, authored publication, run-state isolation, or rendered artifact was verified by this supplement. Those remain separate acceptance subjects. No subject files were edited.

Verification: `git diff --check -- guidance/liturgy/roman-1962-propers.md guidance/liturgy/postconciliar-propers.md guidance/repository.md guidance/web-editions.md guidance/liturgy/propers-production-plan.md` returned exit status 0. The new untracked profile was read directly. HEAD remained `b27036f9b856bd8f662f51b6e6128bd90a5ed633`.

| File | Revised snapshot SHA-256 |
| --- | --- |
| `guidance/liturgy/propers-three-documents.md` | `035c2c66d368fd74b7b2e2ccbf4bf46801c0dc98cca4d27baf55409193234d9d` |
| `guidance/liturgy/roman-1962-propers.md` | `688df7fff816e29c44a0bb4953e73d2601a844463cb0dbf163366b77ff98aaba` |
| `guidance/liturgy/postconciliar-propers.md` | `3f0fe1d499f0f343756d90c6bbe2bf59c0a412834677f0d7c386694f49f29e28` |
| `guidance/repository.md` | `867feb0d3551235eda17a7b8940120f37666303634a5295ad90cc8d46f41dd80` |
| `guidance/web-editions.md` | `2f8a02f673cffcaf02a46aebd42840fce9b5310a11bd58af6fcdddcdb651ebe8` |
| `guidance/liturgy/propers-production-plan.md` | `76b95ff386c7ba9d08cecee467650087b8776f358fa3731ff3d383a1bbd3c66f` |

Only this scratch review was updated. No commits or nested delegation.

## Supplement: physical trees for all propers

Verdict: **pass for this guidance delta**. No blockers or required amendments found. The new paragraph at `guidance/liturgy/propers-three-documents.md:45–55` implements the latest user clarification in the written contract:

- It names the separate 1962 and edition-specific postconciliar source roots and keeps context, evidence judgments, the three authored documents, and durable publication reviews under their owning leaf.
- It locates the postconciliar shared Missal owner inside the same edition tree. That exception preserves the existing shared-owner architecture without providing a route into the 1962 tree.
- It requires mirrored build, installed PDF, and web paths, and expressly rules out a common Sunday leaf above the two source roots.
- It requires examination of indirect dependencies as well as direct imports and extends the boundary to every oration, chant, reading, and optional branch. The rule therefore governs the complete formulary, rather than only Gospel selection or publication labels.

The preceding paragraph's permission to share generic machinery and independently cite provider-neutral primary witnesses remains intact. Read together, the paragraphs separate publication ownership and liturgical judgments without requiring duplicate copies of the reusable primary-source library. Existing per-family run and review separation also remains in force.

Verified the delta boundary with `sed '45,56d' guidance/liturgy/propers-three-documents.md | sha256sum`: removing only the added paragraph and its following blank line reproduces the previous reviewed hash `035c2c66d368fd74b7b2e2ccbf4bf46801c0dc98cca4d27baf55409193234d9d`. The other five guidance files retain the hashes in the preceding supplement. The tracked-diff whitespace check again returned exit status 0; the profile remains untracked and was inspected directly.

Current profile SHA-256: `eb476970ef1bbc87bbbabc877663ef093e2fbc9f0e4902201da93ae34dc034bc`.

HEAD remains `b27036f9b856bd8f662f51b6e6128bd90a5ed633`. This verdict concerns guidance only; it verifies neither the implementation's dependency traversal and path enforcement nor any actual publication tree or workflow run. Only this scratch report was updated. The coordinator's copy at `workflows/reviews/propers-three-documents-guidance-2026-09-17.md` was not edited. No commits or nested delegation.

## Supplement: substantive contributions from two authors

Verdict: **pass for this guidance delta**. No blockers or required amendments found. At `guidance/liturgy/propers-three-documents.md:96–98`, replacing the discretionary multi-author expectation with at least two distinct patristic or saintly authors per interpretation is coherent with the user's request to collate authors into interpretive groups. The explicit requirement for a developed contribution prevents a second name from satisfying the rule through decorative citation alone.

The surrounding requirements still control how the minimum is met: compatible arguments, checked passages and exact supporting loci, truthful attribution, agreement on controlling claims, and preservation of material disagreement. The minimum therefore does not authorize invented agreement, an unsupported witness, or attribution of the editor's entire Mass synthesis to either author. These are compatible semantic requirements, not a finding that any prepared lane meets them.

Current profile SHA-256: `886871a098f66329e7f2b4e6d81558a50f971d7923efe8b760646595e08f75fb`. HEAD remains `b27036f9b856bd8f662f51b6e6128bd90a5ed633`. Scope was only this textual delta and its immediate governing context. No implementation test, manifest, prepared study, or author contribution was verified. Only this scratch report was updated; the coordinator's tracked review copy remains untouched. No commits or nested delegation.
