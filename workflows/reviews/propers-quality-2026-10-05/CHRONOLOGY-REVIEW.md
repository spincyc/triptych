> Historical snapshot: this report concerns the initial local base. Read
> [the disposition](RECORD.md) and [current-main comparison](CURRENT-MAIN-REVIEW.md)
> before treating a finding as current.

Independent chronology review — 2026-10-05

Verdict: no blocking finding in the reviewed Psalm dating / annotation delta or the subsequently added Cana event. The change meaningfully adds traditional historical context while retaining explicit limits. It does not establish an occasion date for Psalms 107, 118, or 144, and must not be described as doing so. Acceptance here concerns chronology semantics and evidence, not publication layout or approval of an installed guide.

Reviewed snapshot

Initial review base: a53e262d00d2658ac079801b07b26deeffb05a6d. The unrelated controls checkpoint f66b0fabf3ed69656df74a422096515582606f6d became HEAD during the review; the chronology delta remained uncommitted and unchanged. The author declared the chronology files frozen before the final independent suite. frozen-sha256.txt is the authoritative reviewed snapshot, independent of that controls checkpoint: it identifies all 14 focused reviewed files, including the four new passage records. Their hashes still matched after the suite. reviewed.patch records the tracked chronology diff; it does not include the untracked passage contents. No tracked file was changed by this reviewer. All reviewer outputs are confined to this scratch directory.

Read: resolved personal guidance, workspace/repository AGENTS.md, complete guidance/scripture-chronology.md, guidance/sources.md, and guidance/external-review-handoffs.md. Review included the code, data, new passage manifests, affected regression tests, regenerated coverage/manifest, and live Proper 60 annotation output. The unrelated production-quality changes were excluded.

Evidence and disposition

1. Ps 107 and Ps 144 attribution — supported. The tracked Douay headings explicitly name David. bindings.yaml:73 binds the existing David reference era only as traditional-attribution. The same output separately says that the occasion date is unresolved; it does not date either poem or episode to his reign. The retained Corbett article's opening paragraph states the conventional 1055–1015 B.C. regnal span and contrasts a later reckoning. The subject and disputed disposition preserve that qualification. No current scholarly consensus date is implied.

2. Ps 118 attribution — supported and appropriately limited. Direct image inspection of Haydock artifact page 817, printed p. 781, confirms general attribution to David and several proposed occasions: Solomon's instruction, David's persecution by Saul, and consolation of the captives. The tracked Douay heading is anonymous. bindings.yaml:87 correctly relies on the commentary witness and promotes none of these alternatives into a chosen historical setting. The passage record preserves the competing proposals. An attribution era remains context about the received author, not an answer to when these verses' particular occasion happened.

3. Ps 136 — the two temporal questions remain distinct. Haydock artifact page 830, printed p. 794, has the Babylonian captivity argument, a verse-1 note preserving expression at Babylon or at the return and possible earlier prophetic composition, and a verse-7 note identifying Edomite incitement of Babylonian destruction. The tracked Psalm text also supports the represented exile scene. The whole-psalm historical-setting boundary in bindings.yaml:4328 and the new event dates that represented scene after Jerusalem's destruction; it does not date composition, first performance, a selected deportation, or the end of exile. Extending this scene-setting assertion across the poem is semantically sound because it identifies the poem's represented context, not every event mentioned inside it.

   The separate retrospective-event binding at bindings.yaml:4344 is confined to verse 7. Therefore the destruction's absolute dates do not reach the Proper 60 Offertory's opening verses. Independent inspection of Haydock artifact page 776, printed p. 740, also confirms the reused preferred A.M. 3416 figure with its Usher attribution. That existing figure is reported under the existing named profile exception, not converted into B.C. or asserted as a date for the lament. The existing alternate destruction dates were not independently re-researched in this review.

4. Ps 78 — the new bounded source note is honest. Haydock artifact page 786, printed p. 750, preserves Babylonian and Antiochene/Machabean possibilities. No unique event date has been invented from them. This is retained evidence, not a proof that all traditional sources are silent, and not newly populated event coverage.

5. Cana addition — supported as a derivation within one identified traditional itinerary. The retained Maas article, SHA-256 88b1d692d90f6a5bc1855e93d624844b3925437134f7349da0a0db415e3d58d7, lines 92–97, puts the Cana incident inside the Second Journey from A.U.C. 779 to about Pentecost 780. Line 25 supplies the source's A.U.C. 782 = A.D. 29 calibration. The new interval 26–27 A.D. follows arithmetically from that single named calibration, retains the raw A.U.C. label, and is visibly marked Derived. This is an enclosing itinerary interval, not a precise healing date or a consensus chronology. The damaged normalized phrase is disclosed in the passage record; the tracked John 4:46–53 controls the identity of the ruler and his son. Jesus is at Cana and the sick son at Capharnaum. The binding is deliberately limited to the inspected appointment through verse 53; this review does not claim that verse 54's summary is intrinsically unrelated or undatable.

6. Annotation behavior — responsible and useful. scripts/_proper_chronology.py:939 shows the subject and derived status of nontextual assertions. At :1090 it exposes a missing or nonuniform Psalm occasion rather than allowing attribution, textual history, or prophetic fulfillment to imply one. Live Proper 60 output (proper60.txt) keeps the mixed Daniel/Psalm Introit nonuniform; the Gradual, Alleluia, and Communion have Davidic attribution plus an unresolved occasion; the Offertory has the identified Babylonian scene and servitude duration, without the destruction's absolute dates. The corpus's existing critical composition bound stays explicitly Composition. These distinctions answer the user's complaint without pretending every psalm narrates a datable episode.

Verification

- PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.scratch/chronology-review-2026-10-05" python3 -m unittest tools.tests.test_chronology tools.tests.test_chronology_derivation_lineage tools.tests.test_proper_chronology_annotations tools.tests.test_proper_chronology_postconciliar
  Exit 1: 311 tests in 102.007s; exactly one failure, QuotedBasisTests.test_a_span_that_cannot_be_reopened_is_declared_and_not_discarded. It is the known unchanged critical.ephesians-later-disciple missing remote-quotation exception. HEAD already contains that unit and lacks the exception; composition.yaml has no delta. No new failure remains. Log: frozen-tests.log.
- ./tools/tpt source-library validate
  Exit 0; valid, including 5,203 passage records. Log: source-library.log.
- The final suite's corpus validation reports 289 events, 78 textual units, 387 bindings, and current coverage at 1,887 rows. Its manifest freshness, source-label exception, numerical calibration, locus-scope, and annotation tests pass.
- git diff --check over the focused tracked paths: exit 0.
- sha256sum -c frozen-sha256.txt: exit 0 after the suite. Log: snapshot-check.log.
- The complete Haydock PDF's independently computed digest matches the registered 9d2dd602cc4a574a8300936c37b7e2f1b3be938803acc6a607cbf5622a2fcab2.

An earlier exploratory suite overlapped the author's Gospel addition and returned seven failures, including stale generated outputs and the then-undeclared label exception. It is superseded by the frozen run; those transient failures are not findings against the reviewed snapshot. The earlier annotation/postconciliar run also passed 45 tests before the Gospel addition; the final combined run covers the finished state.

Limits / required reporting

No new blocker requires a code or data correction. Do not report the full suite as green, nor describe unresolved psalm occasions as newly dated. This review does not certify all Psalms, alternate unenumerated numbering systems, all traditional commentators, the existing critical composition model, every pre-existing destruction-date alternative, generated source-browser catalogs, or any rendered publication. Existing guides were not edited or visually reviewed; their freshness and any future regeneration remain the coordinator's publication work. The full make check-sources/catalog baseline was not independently rerun here; the source-library graph itself was validated.
