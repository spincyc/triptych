Independent integrated chronology review — 2026-10-05

Verdict: PASS for the bounded chronology integration. No blocking finding and no additional chronology correction required before the coordinator proceeds to the research seal. This is not approval of a rendered publication or a claim that unresolved Psalm occasions have been dated.

Snapshot and scope

Reviewed HEAD 50b1ff05f232ab128c2d32ce3770c2d8f0458ac9 against current-main base b373dd5db, plus the uncommitted seven-line correction to tools/tests/test_proper_chronology_reads.py. The fifteen reviewed file hashes in integrated-sha256.txt match the new immutable handoff at build/agent-handoffs/20261005T131112Z-integrated-psalm-gospel-chronology and were checked again after the focused verification. Other live worktree changes were excluded. No tracked file was edited by this reviewer.

This is a fresh integration recheck, not reuse of the earlier PASS. I inspected the focused diff against current main, changes to the governing chronology/source guidance since the original review base, the reconciled projection and tests, the current trace implementation, both freshness functions, and live Proper 60 output. The original direct source inspection remains applicable: all four added source passage records are byte-identical to the previously reviewed records, independently verified against the earlier hashes. No broad source re-research was necessary.

Findings

1. Source and locus boundaries survive the rebase. The added bindings remain traditional-attribution only for Psalms 107, 118, and 144. Psalm 118's alternative occasions are preserved without selecting one. The Psalm 136 scene remains a derived one-sided historical-setting bound across the represented lament; the destruction's absolute dates remain restricted to the separate retrospective-event at verse 7. The Cana event still covers only John 4:46–53, with a 26–27 A.D. interval derived from the single source-internal A.U.C. calibration. It retains the exact source label and does not assert a precise healing day or consensus chronology. Upstream Psalm 32/137/140 bindings, chronology profiles, and composition data are not removed or rewritten by this delta.

2. Upstream presentation behavior is preserved. The production-code delta against current main is confined to visible temporal-subject names and explicit missing/nonuniform Psalm-occasion groups. It leaves the upstream year-specific hedge parser, source casing, quoted duration labels, '(derived)' suffix, display deduplication, sealed duplicate assertions, profile reader names, and computation-read trace implementation intact. The new subject naming continues through concise_display_label(initial=False), preserving source case after the subject. Live Proper 60 output matches the handoff byte for byte. In particular, the Cana display is 'A.D. 26-27 (derived)' without 'c.': the source's 'about' qualifies Pentecost, not the year. The Offertory separately displays the Babylonian scene's bound and the quoted seventy-year duration, without importing A.M. 3416 into its opening verses.

3. The trace-test change is appropriate and does not weaken freshness. ComputationReadsTests.test_cited_sources_are_exactly_what_the_record_cites now compares the current trace's library-source set with the current in-memory generated record. It retains exact-set equality, including the comparison claims, and retains its positive Catholic Encyclopedia assertion. It is a completeness check on what this computation cites, so a previously reviewed historical snapshot was the wrong expected side after a corpus change.

   Freshness remains separately enforced. tools/check-content-preflight still regenerates and compares the carried chronology TOML and annotation TeX byte for byte in check_chronology_record_current and check_chronology_annotations_current; these functions and the research-seal implementation have no delta against current main. I also ran the real PC-S51 'proper-chronology record --check' command: it still exited 1 and identified the historical chronology.toml as not matching the current corpus. Thus the corrected test passes without making that historical snapshot current or allowing omissions from the source trace. Consumer rereview obligations remain in force.

Independent verification performed

- PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.scratch/chronology-review-2026-10-05" python3 -m unittest tools.tests.test_proper_chronology_reads.ComputationReadsTests.test_cited_sources_are_exactly_what_the_record_cites -v
  Exit 0; 1 test passed in 2.836s. Log: integrated-trace-test.log.
- tools/tpt proper-chronology record --provider claude --document liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a --check
  Exit 1 as expected: historical record is not what the corpus now answers. This is evidence that the separate freshness gate still refuses it, not a new integration defect.
- Live Proper 60 annotation generation: exit 0. Output saved as integrated-proper60.txt; cmp against the new handoff's upcoming-annotations.txt exited 0.
- sha256sum checks: all fifteen current handoff files match, and all four added source records match the original independent source review. Final check log: integrated-hash-check.log.
- git diff --check against current main over the focused chronology paths: exit 0.

The new handoff's checks.txt reports 334 chronology/display/lineage/postconciliar/hedge tests and 14 computation-read tests passing, with twenty CLI examples replaying cleanly. I inspected that evidence and the relevant test changes; I did not repeat those full suites because the assigned integration recheck required no broad rerun absent a concern. The earlier pre-rebase Ephesians exception failure is superseded by current main's fix and is not a finding against this integrated state.

Limits

This PASS covers the integrated chronology semantics, preserved source bounds, reader-label behavior, and the narrow source-trace test correction. It does not accept a research seal itself, certify publication layout, regenerate historical leaf snapshots, or eliminate their recorded rereview obligations. The earlier review's source limits remain: attribution is not an occasion; the Babylonian scene is not the date of writing; the Cana itinerary interval is a derivation within the named traditional scheme; and no exhaustive claim about all Psalms or all traditional witnesses is made.
