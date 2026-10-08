# `PC-S54-A` — Target Composition Audit (Claude edition)

**Formula:** `PC-S54-A`, Twenty-eighth Sunday in Ordinary Time, Year A
**Canonical Missal owner:** [Ordinary Time Week XXVIII](../../shared/ordinary-time/weeks/28/propers/verified.md)
**Identity record:** [`instance/manifest.md`](../instance/manifest.md)
**Collated:** 2026-10-08
**Provider:** Anthropic Claude

This record verifies the composition of the target: which units make up this
Mass, in what order, with what boundaries, branches and rights dispositions.
The Missal formulary's witnesses, locators, incipits and variation check belong
to the owner and are not restated. The Lectionary witnesses, with their hashes
and page locators, were collated at context resolution and are recorded in
[`research/context.md`](../research/context.md); this record states what the
research stage itself re-checked.

## What this stage checked, and what it relied on

| Matter | Basis |
| --- | --- |
| Sunday, cycle, occurrence, Lectionary no. 142 and every reading boundary | Re-collated at the research stage from bytes fetched whole over verified TLS on 2026-10-08 and matched to their registered hashes before reading: the USCCB 2026 calendar at printed pp. 5 and 40 (artifact pp. 7 and 42) and its Spanish title list at artifact p. 59; the dated readings page for 11 October 2026, byte-identical to the context stage's copy; and the *Ordo lectionum Missae* 1981 no. 142 on a page image of printed p. 77 (artifact p. 131). Every figure agrees with `research/context.md`. All are bound in `research/source-bindings.toml` |
| Missal elements, order, *Vel:* structure, absent units, conclusions | The Week XXVIII owner. Re-read at the research stage in the 2002 Latin at physical PDF p. 291 (text layer and page image) and in the ICEL excerpt at printed p. 80 (artifact p. 88); nothing differs from the owner's table. The owner's additions of this date record the oration antecedents and the antiphons' comparison with the *Nova Vulgata* |
| Precedence and the omitted memorial | `research/context.md`, whose loci in the 2002 artifact (*Normae universales* nos. 59–60, pp. 70–71; the *Calendarium Romanum generale*, p. 79) are bound to it; at this stage the calendar's text layer was searched again for John XXIII and Juan XXIII and names him only in the Spanish title list at artifact p. 59 |
| Chant and branch rubrics | The governing United States English GIRM, read at the research re-entry of 2026-10-08 in pages fetched whole over verified HTTPS: chapter II (109,916 bytes), byte-identical to the registered state `…english-us-2011-emended-2021.girm2-html-d8ae3c14`, at nos. 48, 51, 53, 61–64, 68, 74 and 87; chapter VII (58,213 bytes), whose bytes matched no registered state and were registered as `…english-us-2011-emended-2021.usccb-chapter-vii-html-2026-10-08-a6786170`, at nos. 363–365. Both are bound in `research/source-bindings.toml`. The chant branches of `research/context.md` were corrected to this text: four options each for the Entrance and Communion chants, the third and fourth approved by the Conference of Bishops or the Diocesan Bishop and the third including psalms in responsorial or metrical form (48, 87); the Offertory chant under the same norms (74); for the psalm, the *Graduale* forms or an antiphon and psalm from another collection approved by the Conference or the Diocesan Bishop, including metrical psalms, and no song or hymn in place of the Responsorial Psalm (61). The Latin *Institutio generalis* in the 2002 artifact, read earlier at the same numbers, agrees except at these United States adaptations. The earlier passes of this stage had met HTTP 403 on both pages |
| Study-text boundaries | Re-read at this stage in the tracked Douay–Rheims (Challoner) and Clementine Vulgate at Isaiah 24:23–25:12; Psalm 22 whole; Psalm 33:9–12; Psalm 129 whole; Philippians 4:10–23; Ephesians 1:15–19; Matthew 21:43–22:15; 1 John 3:1–3; 2 Peter 1:3–4; and 1 Corinthians 15:53–55 |
| Lectionary Latin | The *Nova Vulgata* as published on the Holy See's site, read at Isaiah 25, Psalms 23 (22), 34 (33) and 130 (129), Matthew 22, Ephesians 1, Philippians 4 and 1 John 3 in web states fetched whole on 2026-10-08, not registered and not retained (sizes and SHA-256 values in `research/scope.md` section 5) |
| Greek of the Gospel | The SBL Greek New Testament text and apparatus of Matthew, fetched whole and matched to their registered hashes, read at Matthew 22:1–14 |
| Citation encoding | Every citation below was passed through `tools/tpt proper-chronology`, which parses it with `tools/citations` and returned its book, chapter and verse ranges with partial-verse letters intact |

## Ordered textual units

| Order | Key | Unit and boundary | Status | Rights disposition |
| --- | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | *Si iniquitates observaveris, Domine*. Psalm 129 (Hebrew 130):3 and the first colon of v. 4, with a closing vocative *Deus Israel* that neither the Clementine nor the *Nova Vulgata* carries; printed without `Cf.` | required | Latin incipit and original description only. Douay–Rheims Psalm 129:3–4 may stand beside it as its identified scriptural source, labelled as such and with the Missal's departures stated; no English is composed for the antiphon or its vocative |
| 2 | `collect` | *Tua nos, quaesumus, Domine, gratia*; long conclusion | required | Latin incipit and original description only |
| 3 | `first-reading` | Isaiah 25:6–10a; v. 10 shown as partial, its Moab clause marked as context | required | Douay–Rheims (Challoner), public domain, labelled as study text |
| 4 | `responsorial-psalm` | Psalm 23 (22):1–3a, 3b–4, 5, 6; response from v. 6cd | required | Douay–Rheims at Psalm 22. The strophe break within v. 3 shown; the response shown as the second half of v. 6 only; finding 2 governs how the United States response stands to that verse |
| 5 | `second-reading` | Philippians 4:12–14, 19–20; vv. 15–18 omitted between the segments | required | Douay–Rheims; the omission marked, never closed up |
| 6 | `gospel-acclamation` | Alleluia verse, `Cf.` Ephesians 1:17–18, recast in the first person plural | required | Ephesians 1:17–18 in Douay–Rheims as its identified text, with the recasting described and not translated; no English is composed for it |
| 7a | `gospel-long` | Matthew 22:1–14 | appointed alternative | Douay–Rheims; shown as its own form |
| 7b | `gospel-short` | Matthew 22:1–10 | appointed alternative | Douay–Rheims; shown as its own form, never merged with 7a |
| 8 | `prayer-over-offerings` | *Suscipe, Domine, fidelium preces*; short conclusion | required | Latin incipit and original description only |
| 9a | `communion-antiphon-a` | `Cf.` Psalm 34 (33):11 | appointed alternative | Douay–Rheims at Psalm 33:11 beside a description of the Missal's departures (owner finding 2); no English is composed for the antiphon |
| 9b | `communion-antiphon-b` | 1 John 3:2, its second half, with a supplied subject *Dominus*; printed without `Cf.` | appointed alternative | Douay–Rheims at 1 John 3:2 as its identified source, with the departures described (owner finding 3); no English is composed for the antiphon |
| 10 | `prayer-after-communion` | *Maiestatem tuam, Domine, suppliciter deprecamur*; short conclusion | required | Latin incipit and original description only |

No Offertory antiphon, Sequence, proper Preface, proper Eucharistic Prayer
insert, prayer over the people or solemn blessing is appointed. The approved
United States English of the Missal and of the Lectionary is reproduced nowhere
in this leaf.

## Findings of this stage

1. **Isaiah 25:6–10a: the Latin and Greek forms.** The *Ordo*'s titulus,
   *Faciet Dominus convivium, et absterget lacrimam ab omni facie*, condenses
   v. 6 and v. 8 in the wording of the *Nova Vulgata* (web state of
   2026-10-08), which has *absterget* in v. 8 where the Clementine has
   *auferet*. The two Latin texts differ also in v. 6, where the *Nova
   Vulgata* speaks of a feast of pure and of refined wine (*vini meri … vini
   deliquati*) and the Clementine of the vintage (*vindemiae … vindemiae
   defaecatae*), and in v. 9, *dicetur* against *dicet*. Both read *Praecipitabit
   mortem in sempiternum* in v. 8; the Douay–Rheims follows the Clementine
   ("He shall cast death down headlong for ever"), and its "wipe away tears"
   renders *auferet*. Paul quotes v. 8 in another form, *Absorpta est mors in
   victoria* (1 Corinthians 15:54, Clementine). Jerome gives the Septuagint
   beside the Vulgate (*devoravit mors praevalens*) and notes that the
   Septuagint's *Trade omnia haec gentibus* is the translators' sense, not
   the words of Scripture; the Septuagint form of v. 6 quoted in the third
   Mystagogical Catechesis transmitted under Cyril of Jerusalem's name (NPNF
   English) speaks of drinking wine and gladness and of being anointed with
   ointment. These are recorded so that no study attributes a
   Father's lemma to the Lectionary. The appointment ends with the first
   clause of v. 10 (*in monte isto*), as `research/context.md` established;
   no Greek or Hebrew text of Isaiah was examined.
2. **Psalm 23 (22): the response.** The *Ordo* cites *(6cd)* and prints
   *Inhabitabo in domo Domini, in longitudinem dierum*, which is the second
   half of v. 6 as the *Nova Vulgata* reads it. The dated USCCB page gives the
   same locator, but its response, read and described and not transcribed,
   speaks both of living in the house of the Lord and of all the days of one's
   life; in the Clementine, the Douay–Rheims and the *Nova Vulgata* the whole
   span of life belongs to the first half of v. 6 (*omnibus diebus vitae
   meae*), and the page's own fourth strophe has it there too. The United
   States response therefore joins words of 6c with words of 6b under the
   locator 6cd: an adaptation of the verse, not a quotation of 6cd. Whether
   the printed United States Lectionary has the same response was not
   established; no edition-identified witness of the printed volume was
   available. The study text shows v. 6 whole with the appointed response
   marked as its second half, and no claim may rest on the response's wording.
3. **Philippians 4:19: prayer or promise.** The Clementine reads *impleat
   omne desiderium vestrum*, a wish, and the Douay–Rheims follows it ("may my
   God supply all your want"); the *Nova Vulgata* reads *implebit*, a promise,
   and the dated USCCB page, described, renders the verse as a promise of what
   God will supply. Chrysostom's text, in the NPNF translation, is a blessing
   invoked on the givers and reports variant readings of the object (every
   need, every grace, every joy); Aquinas expounds the Vulgate's *impleat …
   desiderium*. No Greek text of Philippians was examined. The studies may
   not make an argument turn on the mood of the verb or on *desiderium*
   against "need" without stating which text they follow. The *Ordo* opens
   the reading with the liturgical incipit *Fratres*; the omitted vv. 15–18
   carry the Philippians' earlier gifts and the gift brought by Epaphroditus.
4. **Acclamation.** The *Ordo*'s verse, read on the page image of printed
   p. 77, is *Pater Domini nostri Iesu Christi illuminet oculos cordis
   nostri, ut sciamus quae sit spes vocationis nostrae*: it names the Father
   as subject, omits the spirit of wisdom and revelation, and changes Paul's
   *vestri … sciatis … vocationis eius* to the first person plural, closing on
   the hope of *our* calling. The dated page's English verse, described, has
   the same structure. The `Cf.` is printed in both.
5. **Matthew 22:1–14: the text.** The SBL apparatus (registered artifact,
   fetched whole and hash-matched) records only small differences among the
   editions it reports at vv. 1, 4, 5, 7, 9, 10 and 13: at v. 7 the
   Robinson–Pierpont Byzantine text has the king *hearing* before he is angry,
   as the Clementine (*Rex autem cum audisset*) and the Douay–Rheims do, where
   NA28, Westcott–Hort, Tregelles, the SBL text and the *Nova Vulgata* (*Rex
   autem iratus est*) do not; at v. 10 Westcott–Hort print the bridal hall
   (νυμφών) for the wedding; at v. 13 Robinson–Pierpont add "take him away".
   None changes who is invited, who refuses, who is gathered or why the guest
   is cast out. No manuscript was examined. The *Ordo*'s incipit names the
   chief priests and the elders of the people as those addressed, the words
   of 21:23; at 21:45 the narrative names the chief priests and Pharisees.
   The study text follows the Douay–Rheims and does not print the incipit as
   Scripture.
6. **Entrance antiphon.** The owner's finding 1 and its addition 5 govern: an
   adaptation of Psalm 129:3–4a printed without `Cf.`, ending with a vocative
   whose Latin source is not established. The chronology input records the
   Missal's printed locator as an `adaptation` in Vulgate numbering.
7. **Communion antiphon A.** The owner's finding 2 and addition 6 govern:
   Vulgate Psalm 33:11 with `Cf.`, Hebrew 34:11 or, in English Bibles that do
   not number the title, 34:10; the Hebrew-based King James Version has young
   lions where the Latin and the Douay–Rheims have the rich. The study text is
   the Douay–Rheims at Psalm 33:11, and no claim may rest on the Hebrew
   subject. The chronology input enters the Missal's printed Vulgate locator
   with `Cf.` as an `adaptation`.
8. **Communion antiphon B.** The owner's finding 3 and addition 6 govern: the
   second half of 1 John 3:2 with the subject *Dominus* supplied, printed
   without `Cf.`; recorded as an `adaptation`. Verse 3, which follows
   immediately, is context and not part of the antiphon.

## Relationship classes

| Relation | Class | Authority |
| --- | --- | --- |
| First reading ↔ Gospel | `officially correlated` | *Praenotanda* 1981, nos. 105–107; no. 106 says the relation between the readings of one Mass is shown by the careful choice of the tituli set over them. At no. 142 the *Ordo* heads the first reading with Isaiah 25:6 and 8, the feast the Lord makes and the tear wiped from every face, and the Gospel with Matthew 22:9, *Quoscumque inveneritis, vocate ad nuptias*, a verse in both forms |
| Second reading, the *Ordo*'s emphasis | `semi-continuous` | Headed *Omnia possum in eo, qui me confortat* (Philippians 4:13). The three tituli are edition-controlled evidence of what the Lectionary singles out in each reading and of the one official correlation; they are not evidence of a whole-formulary design |
| Psalm → first reading | `responsorial` | GIRM 61 |
| Alleluia verse → Gospel | `acclamatory` | GIRM 62 |
| Second reading; Gospel | each `semi-continuous`; this is the last Sunday of the four-Sunday Philippians course of Year A (*Tabella II*), and the Gospel's course runs from Matthew 21:33–43 on 4 October to 22:15–21 on 18 October | *Praenotanda* 1981, no. 107 and *Tabella II*; national calendar |
| Missal antiphons and orations ↔ Year A readings | `source-grounded synthesis`, `documented reception` or `editorial or AI proposal`, labelled case by case in `research/interpretations.md` | The week's Missal texts serve all three cycles |
| Recurrence of the vocabulary of calling, feasting and hunger, riches and glory, and seeing across units | `textual observation` | The texts themselves (Douay–Rheims and Clementine); `research/scope.md` section 2 lists them. No source consulted states a design |

## Branches

The twelve branch IDs of `instance/manifest.md` apply unchanged. Statuses,
authorities and resolutions are those tabulated in `research/context.md`; no
selection was supplied and none is inferred. For `gospel-short-form`, every
claim in the research records that rests on Matthew 22:11–14 is marked as not
holding for a celebration that uses the shorter form. For the Communion pair,
every claim resting on one antiphon only is marked with that antiphon.

## Outstanding

Whether the printed United States Lectionary prints the psalm response as the
dated page does (finding 2); the Greek of Isaiah 25 and of Philippians 4:19;
manuscript evidence for Matthew 22:1–14 beyond the editions' apparatus;
whether the United States Lectionary admits another acclamation verse from a
common set on Sundays in Ordinary Time (GIRM 62 a, in the Latin and in the
United States English alike, says only that the verse is taken from the
Lectionary or the *Graduale*); the printed United States Lectionary volume,
which was not inspected; independent review of this audit.
