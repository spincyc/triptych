# Chronology evidence review

The postconciliar adapter used only this edition's checked appointments and
canonical Week 32 owner. Its ordered twelve-key input retains both second-reading
forms, both Communion choices, the psalm response and adaptations. The query
for Wisdom uses Vulgate 6:13–17, corresponding to the appointed modern 6:12–16;
the input's descriptive element name and source audit state that conversion.
The generated visible passage cell reads “First reading (appointed Wisdom
6:12–16); Vulgate equivalent: Wis. 6:13–17.” Its citation and query remain
Vulgate 6:13–17. Thessalonians uses Clementine 4:13–18
and 4:13–14, with the study Bible's different printed ranges recorded separately.
No subverse date is claimed for the refrain or acclamation.

`proper-chronology record --write` and `annotations --presentation
orientation-v3 --write` generated the record, sealed annotation macros and
complete table. The actual output was inspected: each passage has its own
group; long and short second readings retain their separately identified uses;
the three composed prayers have no invented biblical date. There is no short
Gospel. Composition alternatives are not dates of Jesus' telling a parable,
the future advent or this liturgical occurrence.

## Controlling dated subjects and source checks

- **Wisdom:** read Gigot's *Catholic Encyclopedia*, “Book of Wisdom,” authorship,
  place and date paragraphs in the retained article artifact. He rejects
  Solomonic composition while explaining the literary voice, places the work
  at Alexandria, and offers the persecution eras of Ptolemy IV (221–204 B.C.) or
  VII (145–117 B.C.), allowing publication after those rulers. The output rightly
  preserves both disputed “in or after” alternatives. These are Gigot's
  historical arguments, not a date spoken by Solomon or modern consensus.
- **Psalms 22 and 62:** independently read the actual Challoner titles and
  Corbett's “King David” opening in the retained 1908 article. Both titles
  explicitly name David; the shared qualified 1055–1015 B.C. reign is an era
  of traditional attribution, not the date either psalm was composed or the
  date of a remembered crisis. A narrow source binding was added for these
  two psalms because the earlier composition-only output omitted attribution.
  Both generated attribution rows identify the usual chronology beside the
  regnal subject and state that Corbett also reports writers dating the reign
  30–50 years later. The shared source-owned orientation qualification retains
  this relative alternative; no new endpoints were calculated. Read 2 Kings 5:5
  for Hebron/Jerusalem geography. Psalm 22 identifies no occasion: unresolved
  occasion remains unresolved alongside the attribution.
- **Psalm 62's occasion:** read Drum's “Psalms,” historical-title paragraph,
  which associates Hebrew 63/Vulgate 62 with flight from Absalom. Read Psalm 3:1
  for the shared event's relative description. This is a traditional historical
  setting distinct from the actual Psalm 62 title, whose held Challoner says
  desert of Edom; Augustine says Idumaea. It does not prove a specific year
  or permit silently replacing this title with Judea. The generated output
  keeps the relative flight wording. No dates from other episodes in David's
  reign were borrowed.
- **Psalter composition limit:** independently reacquired and read the complete
  official USCCB Psalms introduction. Its inability to date individual psalms
  and pre-Maccabean horizon justify the output's broad critical-profile
  boundary before c. 165 B.C.; this is not an individual composition estimate
  or a substitute for attribution/occasion. The acquired HTML differs in hash
  from the registered older response; acquisition handoff preserves both facts.
- **Psalm 87:** its title names sons of Core and Eman, not David. Read Drum's
  Sons of Korah discussion, which allows guild composition/collection and
  proposes the period between Isaias and return from exile from style and
  allusions. The output is that source's group-composition horizon. Neither
  title nor inspected reception identifies a dated individual lament occasion;
  the unresolved historical setting is retained. Augustine's Passion reading
  is theological reception, not a date of the psalm's literal event.
- **Matthew:** read Jacquier's date discussion and Durand's “New Testament”
  origin paragraphs in the exact retained articles. The generated alternatives
  c. A.D. 38–45, 40–42, 40–45, 60–68, 64–67 and 50 report their incompatible traditional
  proposals. The Semitic-original/Palestine qualification cannot be dropped
  or converted into a secure date and writing site for the extant Greek text.
  Read Matthew 24–25 directly: 24:3 locates the continuing discourse on Mount
  Olivet. A scoped source-owned description was added for 25:1–13, explicitly
  identifying narrative-continuity inference and Jesus' telling, not a dated
  wedding. Its event date remains unresolved.
- **Luke:** read Durand's approximate A.D. 70 proposal and the 1912 PBC response
  I–IX in AAS 4 pp. 463–465, with controlling VI–VII visually checked on p. 464
  of the exact reacquired PDF. The generated record preserves both the
  approximate proposal and before-Acts/Roman-captivity bound; no absolute
  Emmaus date is derived from either. Read Luke 24 whole: the recognition is
  recalled at 35 after the travelers' return to Jerusalem. The existing corpus
  deliberately bounds its resurrection event separately from the later
  appearances; this leaf does not relabel a composition date as that event.
  The Communion basis is not a separately appointed narrative pericope; the
  generated composition-only result is stated as a corpus limit, not proof
  that the episode has no relative narrative setting.
- **1 Thessalonians:** read Prat's Pauline chronology list and Drum's time/place
  and occasion sections. The output preserves A.D. 52 and 53–54 under the
  traditional profile. Drum's competing Harnack chronology is not silently
  adopted. His Corinth argument cites Timothy's return; Acts 18:5 was read.
  The setting distinguishes the writing at Corinth from recipients at
  Thessalonica. Neither date predicts the Lord's future coming.

The exact retained encyclopedia article artifacts, Scripture books and AAS
PDF are bound. Source records and the corpus events, bindings and orientation
metadata were inspected in addition to actual witness text. A reported
traditional date is not a dogmatic definition or a claim to current historical
consensus. No prose author may edit the generated page or choose one of its
date alternatives for convenience.

## Shared-source change and integration boundary

The retained research changed two shared chronology files: `bindings.yaml` adds the
Psalms 22/62 attribution and `orientation.yaml` adds the scoped Matthew 25
context. No shared date was changed. Scanning all 49 existing chronology
records identifies only the Claude and GPT PC-S54 Year A studies, in addition
to this target, as existing consumers of the changed passage scopes. Their
Psalm 22 responsorial appointments require regeneration. Before the integration refresh, actual record and
annotation currency checks failed for both PC-S54 leaves and passed for the
current PC-S58 leaf. The driver subsequently regenerated the affected consumers.

The driver additionally identified four GPT consumers with metadata-only
registry dependency-hash changes: PC-R07, PC-S51, PC-S53 and PC-S55. These
are separate from the two substantive Psalm 22 consumers above. The driver
assigned their generated bookkeeping refresh to the integration lane; no
new scholarship or prose change is implied.

Before the first cold review, the version-19 research worker independently ran both `record --check` and
`annotations --check` for all six named consumers and this target after that
refresh: all fourteen checks passed. The target's explicit `record --write`
and `annotations --presentation orientation-v3 --write` also reported already
current, and the complete table and annotations were inspected against the
source distinctions above. No chronology date, source owner, generated byte
or other leaf was changed in that initial research pass. These checks establish
currency for the identified consumers; they do not substitute for downstream
content review or a repository-wide release verdict.

## Research repair after the first cold review

The first reading's generated passage cell now identifies the appointed Wisdom
6:12–16 and the Vulgate equivalent 6:13–17. This corrects the earlier review's
acceptance of an unqualified Vulgate address. The underlying citation and all
five query loci remain unchanged. The source check reread OLM no. 154 on
printed p. 85 (PDF p. 139), the dated USCCB first reading, and the retained
Challoner Wisdom 6 in full. The OLM heading gives 6:12–16; its opening agrees
with the content at held Challoner 6:13. The final appointed encounter with
Wisdom is held Challoner 6:17, whereas 6:12 precedes the appointment.

The retained Corbett article's complete opening paragraph and its registered
printed-page passage record were reread. The shared subject
`israel.monarchy.david-traditional-era` now uses the orientation title
“David's reign in the usual chronology” and the source-owned claim
qualification “Corbett also reports writers dating the reign 30–50 years
later.” His fuller explanation involving Assyrian inscriptions remains in the
claim's basis and is recoverable through the exact source references. This
qualifies the existing disputed regnal reference era without adding another
answerable date or calculating absolute endpoints. Both the Communion Psalm
and responsorial Psalm rows print it. Their composition bounds and the
distinct unresolved Psalm 22 occasion and relative Psalm 62 setting remain.

The target record and orientation-v3 annotations/table were regenerated through
their owning commands and their currency checks passed. The generated visible
cells were inspected, including their sealed query reaches and source labels.
The shared chronology corpus validated. Its first coverage check exposed the
stale generated rows for the earlier Psalm 22/62 attribution bindings; the
owning build command regenerated exactly those two coverage rows, and the
coverage currency check then passed. The 44 existing proper-chronology
annotation tests and source-library validation also passed. No new source was
acquired or registered, no source payload
or source-library fingerprint was changed, and no generated file was edited
by hand.

The shared subject occurs in 31 existing chronology records: this target and
30 other leaves. The 1962 consumers are GPT 47, 48, 52, 54–57, 59–61, F01 and
F02, and Claude 48, 52, 54–57, 59–61, F01 and F02. Postconciliar consumers are
GPT PC-S51, PC-S54, PC-S55 and this PC-S58, and Claude PC-S51, PC-S52, PC-S54
and PC-S55, all Year A. Their numerical chronology is unchanged; the shared
orientation qualification requires generated-output currency validation. The
driver owns the other leaves' generated-only integration. This research repair
does not revise their authored prose or renew their independent review.

The driver's integration checks subsequently established generated currency
for all 30 other leaves (226 generated artifacts) and successful isolated
conversion and fidelity checks for their 74 admitted reader outputs. Two
held or withdrawn Claude Fourteenth Sunday outputs were excluded from that
reader count. Its comparison found 2,578 protected files unchanged and exactly
90 generated files changed in the expected qualifications and row identifiers;
the other leaves' chronology TOML bytes were unchanged. These are mechanical
integration results, not a renewed content verdict for those studies.
