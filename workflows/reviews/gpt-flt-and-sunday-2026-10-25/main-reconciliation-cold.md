# All Saints current-context integration review

Reviewed 26 October 2026 UTC, after ordinary integration of accepted candidate
`844cdc6d62908cfc92cf655a3cd9b9478896b5bf` with incoming main
`f3f59d483358128e1b78d7a12aaeb4f3feab4a8a`. This review examines their combined
source state while the merge is being prepared. It owns no subject edits,
native-engine operation, Git index, commit, push or deployment.

**Scoped integration disposition: ACCEPT.** Incoming main requires no change to the
accepted GPT All Saints appointed texts, commentary, chronology, three PDFs or
canonical web edition. After the coordinator completed the combined release
reconciliation, the fresh scoped public-alpha check also exited 0. This verdict
covers the target-specific content, sources and publication contract examined
here; final whole-site checks and disclosure review remain the coordinator's
separate gates.

## Historical native acceptance and current global inputs

The version-15 native run `fb0417d471635250`, seeded at
`24c1b7ce1781f79937f57b66c221b0ed82e219d9`, remains an authentic historical
ACCEPTED run. All 55 archived files are byte-identical to the accepted candidate;
the archive retains its 25 results, 25 packets and zero interventions. Its
publication-gate result still hashes to
`87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a`.

The current merged tree does **not** reproduce every historical research seal.
Four of the research review's 1,779 file pins differ; the other 1,775 match.
Recursive inspection of the research computation pins finds no additional
changed path. The four differences are:

| Global path | Archived SHA-256 | Current SHA-256 |
| --- | --- | --- |
| `src/sources/calendars/roman-1962/propers.yaml` | `4cd520fce806347e4b2c8b2865765d929e2d48de71273f73150264abfb3059f4` | `3536021b46c88b5fc883e53319edd8c5e4ac90e906c50d630ffe35c3b192b545` |
| `src/sources/calendars/roman-1962/rubrics.yaml` | `d2cfedf30d811b2339612d21dd1980639ce3421559fa209914b0795d4a431dcd` | `f12674aa5e1541ef1f55f761ef6ce5b48d46ac94c8c165f5c4e2fd443509a4d6` |
| `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` | `c0191ad579809d8abac8f80d878cafca0e4d8222fb4c6e9a25dc72d81ec66687` | `aafe43ebf3c4a7c5a7a7ab974c19472fe331b936c6d671b110be94f1bad81eb2` |
| `src/sources/inventories/roman-1962-proper-translations-v1.toml` | `c37b6ea3ebfff40fdd4e25f7cdaa927f18fee16e5ee83a7bcd380b0401b074e9` | `a8140456e71ed2a1a94589740de62ca2dc2619abe7f7adfbcf5a1a5c3f4d88ea` |

The final accepted study iteration's 18 pins, concise study's 14, homily's nine,
visual review's 30 and canonical web pin still match. The initial study review
is intentionally superseded by its accepted revision; its changed
`40-purification-and-rest.tex` pin is the recorded STU-001 repair, not an incoming
main regression. No archive, review result, provenance declaration or proof was
restamped to conceal either kind of historical difference. This new review and
the current checks below supply the bounded integration judgment.

## Target facts and actual source loci

Exhaustive parsed comparison against `844cdc6d6` finds both complete Mass
dictionaries, `omnium-sanctorum` and `pentecost-23`, unchanged. The only changed
Mass dictionaries concern September Dolors, Anthony of Padua, the June 30 Paul
commemoration, John Damascene and Jane Frances de Chantal. All seven relevant
Latin-provenance dictionaries and all seven relevant translation dictionaries
for the feast and Sunday are unchanged. Source availability and rights additions
elsewhere in those large inventories do not change a target permission or text.

All 72 publication binding fingerprints match the current source library. Every
bound record and all 136 distinct records in their ancestor closure are unchanged
from the accepted candidate; the loaded source graph reports no errors. This
comparison reaches actual edition, artifact and passage owners rather than
accepting an unchanged bibliography as sufficient. In particular, the exact
Mame 1922, Pustet 1862, Lasance/Walsh 1945 and Cummiskey 1861 owners, the registered
Bede and other commentary sources, the dated Ordo metadata and the qualified
chronology witnesses retain their existing pins and loci.

Independent primary-page inspection in this review reopened the CMAA 1962
Missal after recomputing its whole-file SHA-256:
`648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`.
The actual inspected one-based artifact pages were 15–17, 32, 333–334, 497–498
and 783–784. These establish:

- The ten feast texts at printed pp. 702–703, marginal nos. 3974–3983, remain
  the appointed texts. The composed Introit antiphon is distinct from Ps. 32:1;
  the Gradual takes only the latter clause of Ps. 33:11; the Gospel ends at
  Matthew 5:12a before the prophets clause; the Wisdom 3 Offertory is selected
  and adapted; the Communion takes Matthew 5:8–10. The full Lesson's twelve
  tribes and its ending remain present.
- The Sunday Collect, Secret and Postcommunion are the three actual prayers
  at printed pp. 416–417, nos. 1720, 1726 and 1728. Their printed conclusions
  remain distinct from the feast prayers. The source records retain exact
  abbreviated cues; this integration composes or expands no prayer.
- RG 91, 106, 108, 109(a), 111(a), 113 and 120(d) support the first-class feast,
  privileged Sunday commemoration and white color. Fresh `calendar-rubrics day`
  for 1 November 2026 returns All Saints as winner and `pentecost-23` as the
  privileged commemoration in both Low Mass and sung non-conventual forms,
  with a second conclusion. Its Easter, Pentecost and next-Advent anchors
  remain 5 April, 24 May and 29 November 2026.
- RGMR 482–483, 494(b) and 498 continue to select the Common Preface. The
  commemorated Sunday's printed Trinity Preface does not introduce a proper
  Preface into this feast. The actual Common Preface body and its transition
  to the Sanctus were reopened at printed pp. 252–253, no. 1057. The fourteen
  stable appointed keys remain ten feast texts, three Sunday prayers and this
  selected Preface.

The dated FSSPX Ordo remains a precisely identified, restricted historical
acquisition, `a7d8fbbf…`, with its original scope and institutional limit.
This review neither claims a new Ordo retrieval nor elevates that institute's
witness into a diocesan calendar or present permission to use the book.

The chronology corpus and target chronology inputs are unchanged. Current
generation checks reproduce both the full record and its annotations. Direct
reinspection of the retained Gigot article, lines 27–29, again confirms that
either proposed Ptolemaic persecution horizon permits later publication; both
visible dates retain “in or after.” Jacquier's Matthew composition alternatives,
Durand's distinction between the Aramaic original and its undated Greek
rendering, and the Apocalypse alternatives remain qualified in their actual
retained texts and in the study. The Davidic reference era, pre-accession flight,
collection-wide Psalm composition bound and unresolved Gospel event remain
separate. No new precision or date was supplied by this merge.

## Incoming publication guard and superseded Ordinary repair

The fourteen changed lines in `guidance/propers-for-agents.md` update census
counts for newly recovered texts. They introduce no target-specific appointment,
source or publication requirement.

The fifty-line `tools/public-alpha` delta admits and validates
`oration_relation` only when bound to the source-owned applied RG 110 rule.
It requires the exact execution object and exact, nonrepeated pair membership;
missing, extra or altered relations fail. The current tool hashes to
`b05a93a62a0f6d6d1392d12de4bf051ac422d3fdd14885635708e56aa3b69577`.
The three pairs are Conversion of Paul/Peter, Chair of Peter/Paul and June 30
Paul/Peter. Neither `omnium-sanctorum` nor `pentecost-23` is a member. Reading
RG 110 itself at artifact p. 16 confirms that its inseparable single conclusion
and count-of-one treatment concerns Peter and Paul. It does not combine this
feast's prayer and its privileged Sunday commemoration into one.

Incoming main's canonical John Damascene source correction also supersedes the
earlier temporary Ordinary role-label repair. The coordinator restored the two
unsealed Ordinary tables to incoming main rather than preserving obsolete alias
assertions. The older repair's cold-review hashes therefore remain historical
evidence of that repair, not current-table claims. Neither table belongs to the
accepted F02 render inputs. This review does not claim acceptance of every
unrelated incoming feature; its target-impact conclusion follows the exact
membership and source comparisons above.

## Actual current checks and artifact boundary

The following checks ran against the combined source state, independently of
the historical native stage results. Each exited 0:

| Command | Outcome |
| --- | --- |
| `.scratch/publication-prep/venv/bin/python scripts/_proper_study.py check --provider gpt --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --date 2026-11-01 --phase publication --require-presentation --require-format --require-authority --require-orientation --require-orientation-v2` | Current scoped publication contract passes |
| `.scratch/publication-prep/venv/bin/python tools/tpt proper-chronology record --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --provider gpt --check` | Record current with the corpus |
| `.scratch/publication-prep/venv/bin/python tools/tpt proper-chronology annotations --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --provider gpt --check` | Annotations current with the corpus |
| `python tools/tpt calendar-rubrics day --calendar roman-1962 --date 2026-11-01 --json` | Dated finding aid agrees with the bounded appointment above |
| `.scratch/publication-prep/venv/bin/python tools/tpt public-alpha check --provider gpt --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints` | Current scoped public-alpha check passes after combined release reconciliation |

The last command reports global source, release and authorization records valid
for 274 publications, while limiting installed-PDF inspection to the three F02
outputs. Its actual log SHA-256 is
`6d67d02adf7d3942fe78e813e14a95acac2c0ea11094acbe839ee2afab92bee0`.
That scoped pass establishes neither unrelated PDF installation nor deployment.

Independent byte checks find all 25 accepted F02 render inputs unchanged, all
55 archive files unchanged, and all twelve entries in `installed-artifacts.json`
unchanged in both hash and size: seven PDFs and five canonical Markdown files.
The GPT Four Last Things source and web trees are unchanged from the accepted
candidate. The coordinator owns a fresh built-site comparison of their four
accepted HTML hashes under the changed generator; that comparison is separate
from the installed Markdown equality established here.

No full global aggregate, site rebuild, deployment or engine rerun was performed
by this lane. The open 528-row global chronology audit and pending source-family
screening remain open. The nonblocking `WEB-REGISTER-001` next-revision advisory
remains recorded. Current-context acceptance cannot be used to rewrite those
boundaries or represent historical global seals as current.
