# Saint Peter — research scope

Provider: Anthropic Claude.

## Publication identity

- **Publication:** *Saint Peter: The Fisherman and the Keys*
- **Provider / collection / leaf:** `claude / biographies / saint-peter`
- **Genre:** source-first historical and hagiographic biography
- **Subject:** Simon Peter (Simon; Cephas; Petros), Galilean fisherman,
  apostle, and martyr
- **Primary geography:** Bethsaida, Capernaum and the Sea of Galilee,
  Jerusalem, Samaria, Lydda, Joppa, Caesarea, Antioch, Rome
- **Primary life period:** first century AD; birth unrecorded; death at Rome
  under Nero between 64 and 68
- **Reception period:** first century through the research cutoff
- **Language:** English; ancient names and Latin/Greek tags only where they
  clarify evidence
- **Research and mutable-fact cutoff:** 2026-07-25
- **Governing guidance:** `guidance/editorial.md`, `guidance/repository.md`,
  `guidance/biographies.md`, `guidance/sources.md`

This Claude edition was researched and written independently of the sibling
GPT edition; per the independence rule, the only file consulted under
`src/gpt/biographies/saint-peter/` was `research/scope.md`, for topic parity
only. No GPT sections, chronology, tradition audit, or prose were read.

## Staleness review — 2026-07-27

Changed inputs: newly registered exact-OCR passage records for Irenaeus,
*Against Heresies* 1.10.1–3, 3.3.1–4, 3.22.4, and 5.2.2–3; and a new
Penelope web edition and exact passage record for Josephus, *Antiquities*
8.2.5. Both required candidates are preserved under
`build/staleness/claude/biographies/saint-peter/`.

| Consequential claim | Old publication | Minimal candidate | Research-first rewrite | Effect |
|---|---|---|---|---|
| Irenaeus's Roman witness and succession in *AH* 3.3.2–3 | Uses it as second-century reception for Roman apostolic ordering and the Linus succession, not as eyewitness proof or a continuous episcopate from the 40s | Retains the prose; notes that the exact OCR now controls the existing bounded substance | Reaches the same judgment from the records: public apostolic tradition, Rome and Smyrna, and succession, with the same second-century ceiling | **Strengthens source control only**; adds, removes, weakens, and contradicts no claim |
| Irenaeus's newly recorded 1.10.1–3, 3.22.4, and 5.2.2–3 | Makes no claim from these loci | Excludes them as unrelated | Excludes them as rule-of-faith, Marian-recapitulation, and Eucharistic-resurrection material rather than Petrine biography | **No effect** |
| Agrippa I and the conventional A.D. 44 anchor | Uses Josephus, *Antiquities* 19.8.2, with the conversion and source limit stated | Retains the claim unchanged | Reconstructs the same bounded chronology | **No effect**; new 8.2.5 concerns Solomon, Eleazar, and demons |
| Overall life, Roman martyrdom, and tradition judgments | Distinguishes canonical portrait, early reception, later legend, and project synthesis | Preserves all judgments | Independently reproduces the same architecture and conclusions from the research records | **No substantive disagreement** |

**Verdict: no material change.** The changed research improves the provenance
available for one already bounded Irenaeus claim but requires no publication
wording, chronology, tradition, or conclusion change. A future maintenance
revision may upgrade the Irenaeus binding from catalog-level live-web use to
the inspected OCR record while preserving its OCR and non-critical-edition
limits. The Josephus 8.2.5 material must not be imported into this biography.

## Controlling question

What does the earliest controlled evidence establish about Simon of
Bethsaida; what can responsibly be said about his death at Rome and its
evidence chain; and what have legend, archaeology, liturgy, and doctrine
each claimed about him, at what actual evidential ceiling?

The publication is a study aid for serious general readers, students,
clergy, and researchers. It is not an archaeological authentication, a
critical edition, an ecumenical adjudication of Matthew 16, or a substitute
for magisterial teaching.

## Evidence classes

The biography profile's codes are used exactly as defined in the terminal
appendix: A (none uncontested; 1–2 Peter graded, not presumed), N (Paul's
undisputed letters; the Gospels and Acts as distinct first-century
witnesses; Tacitus for context), E (1 Clement; Ignatius; Papias, Dionysius
of Corinth, Gaius, Origen via Eusebius; Irenaeus; Tertullian), L (Acts of
Peter and the legend cycle; constructed episcopal chronology; relic and
site legends; iconography), M (Pastor aeternus; calendar; the 1950 and 1968
papal announcements, each limited to its object), K (excavation report and
review literature as reported in Smothers 1966; named critical positions on
the letters), S (project synthesis, never attributed to a source).

## Source corpus in scope

- Scripture in the Challoner Douay–Rheims translation (drbo.org), with all
  quoted chapters retrieved and read on 2026-07-25; Mt 16:16–19 and Jn 21
  quoted exactly from this identified witness.
- 1 Clement 5–6; Ignatius, Romans 4 (middle recension); Irenaeus, AH 3.1.1,
  3.3.2–3; Tertullian, Prescription 36 and Scorpiace 15; Eusebius, HE 2.15,
  2.25, 3.1, 3.3, 3.39 (preserving Papias, Dionysius, Gaius, Origen);
  Jerome, De viris illustribus 1; Tacitus, Annals 15.44 — all in identified
  public-domain translations (ANF/NPNF; Church–Brodribb).
- Acts of Peter 35–40 in M. R. James's 1924 translation, labeled apocryphal
  and dated by the translator's headnote ("not later than A.D. 200").
- The Vatican scavi: Smothers, "The Bones of St. Peter," Theological
  Studies 27 (1966) 79–88, read in full; Paul VI's audience of 26 June
  1968 (vatican.va, Italian); L'Osservatore Romano English article of June
  2024; the basilica's official necropolis page. The 1951 Esplorazioni
  report and Guarducci's volumes were NOT inspected directly; every claim
  from them is ceilinged as reported.
- Pastor aeternus, official Latin, bound to the repository source-library
  passage record and re-verified byte-identical (SHA-256 032a5f65…) on
  2026-07-25.
- Catholic Encyclopedia (1908–1912) articles "St. Peter, Prince of the
  Apostles," "Chair of Peter," "Pope St. Clement I" for reception history,
  and "St. Cyprian of Carthage" (vol. 4, Chapman) for the two recensions of
  De unitate 4, which that article prints in full.

Added in the 2026-07-25 deepening revision:

- The Greek New Testament read directly at the loci where a claim turns on
  the Greek: the Robinson–Pierpont Byzantine Textform (RP2018) in the
  byztxt Unicode CSV form of Robinson's CCAT files, with its inline
  NA/Byz divergence apparatus. Eight book files (Mt, Lk, Jn, Acts, Gal,
  1–2 Pt, Jude) were downloaded at a pinned repository state, hashed, and
  registered as tracked artifacts under
  `src/sources/works/robinson-pierpont/`; bindings record acquisition and
  inspection with pinned fingerprints. This is one textual tradition with a
  divergence apparatus, not a critical edition; no manuscript or collation
  work was done.
- The Clementine Vulgate of John 21 as presented at drbo.org, for the
  diligis/amas and pasce renderings.
- Origen, Commentary on Matthew 12.10–14 (ANF 9, Patrick) — the fullest
  ancient statement of the "every confessor is a Peter" reading.
- Cyprian, On the Unity of the Catholic Church 4–5 (ANF 5, Wallis).
- Augustine, Tractates on John 124.5 (NPNF1-7) — the petra/Peter etymology.
- The Jerome–Augustine correspondence on Gal 2:11–14, read in full:
  Augustine, Letters 28, 40, 82; Jerome's reply (Aug. Letter 75 = Jerome
  Letter 112), NPNF1-1 (Cunningham), with Jerome's own numbering checked at
  NPNF2-6.
- Eusebius, HE 1.12 (Clement of Alexandria's namesake theory) and 6.20
  (the Gaius–Proclus dialogue under Zephyrinus).
- Ignatius, Smyrnaeans 3 (ANF 1).
- The Muratorian Fragment in Metzger's translation, for the deliberate
  omission of Peter's martyrdom from Acts and for the absence of the
  Petrine epistles from the earliest canon list.
- Josephus, Antiquities 19.8.2 (Whiston) for Agrippa I's death.
- Calvin, Institutes 4.6.3–7 (Beveridge, CCEL), read in full as the
  strongest Reformation statement of the case against.
- Lumen gentium 22 and Ut unum sint 88–97 (official English, vatican.va).
- Smothers 1966 re-read in full for the von Gerkan/Kirschbaum/Prandi/Magi
  stratigraphic dispute, the three bone groups, and the coin objection.

## Required coverage delivered

Names and Galilean world; three call portraits kept distinct; discipleship
and confession at Caesarea Philippi with Mt 16:16–19 quoted exactly;
denials; restoration in Jn 21; Acts leadership through the council; the
Antioch incident of Gal 2 handled squarely; the epistles' authorship
questions bounded; the Mark tradition; the extra-scriptural Rome/martyrdom
chain (1 Clement 5–6, Ignatius Rom 4, Dionysius, Gaius's tropaia and
HE 2.25, Irenaeus, Tertullian, Origen via HE 3.1); Quo vadis and inverted
crucifixion from the Acts of Peter, labeled late; the scavi and the
Guarducci controversy reported with ceilings; Petrine doctrine bounded to
Pastor aeternus as reception; feasts and iconography; chronology with
per-event bases; tradition audit; terminal apparatus.

Added in the 2026-07-25 deepening revision (16 pp. to 38 pp.):

- A dedicated section on Mt 16:18–19 reading the Greek and the Aramaic
  substrate, setting out the four historic readings of "this rock," quoting
  Origen and Calvin at their strongest, giving the two recensions of
  Cyprian's De unitate 4 with the textual controversy named, giving
  Augustine's petra/Peter etymology, and closing with a labelled Project
  synthesis on what the wording carries.
- Luke 22:31–32 treated as the second primacy text, with the Greek
  plural/singular pivot, the fact that Luke places it immediately before the
  denial, and Pastor aeternus ch. 4's use of it together with the council's
  own limiting clause on new doctrine.
- John 21:15–17 treated with the agapao/phileo and boske/poimaine
  variations, the Johannine interchange of the two love-verbs elsewhere, the
  Vulgate and Douay renderings, and 1 Pt 5:1–2 as the text that universalizes
  the charge in Peter's own name.
- Antioch expanded into the three ancient escape routes (Clement's namesake
  theory, refuted from Gal 2:7–9; Origen–Jerome's staged rebuke; Augustine's
  plain reading) and the Jerome–Augustine exchange read at the letters, with
  a Project synthesis whose stated counterargument is Jerome's tu quoque.
- Rome argued by first stating the four silences at full strength (Rom 16,
  the captivity letters, Acts, the first century as a whole), conceding what
  they refute (the 25-year episcopate), then weighing 1 Clement in its
  context of chs. 4–6 against Tacitus, Ignatius, Dionysius, Irenaeus, and
  Gaius, with a Project synthesis whose counterargument is single-tradition
  propagation.
- The letters graded with the 2 Peter/Jude shared clause read in Greek, the
  Muratorian silence, the Symeon datum, and a Project synthesis.
- The tomb section rebuilt around the actual stratigraphic dispute and the
  three bone groups, with a stated inability to date the grave itself to the
  first century.
- Reception extended to Lumen gentium 22 and Ut unum sint.
- A rendered tradition-and-status table in the terminal appendix.

## Controlling conclusions

- The first-century core (fisherman, call, primacy among the Twelve,
  confession, denials, restoration, Jerusalem leadership, Cornelius,
  council, Antioch rebuke) is established by N-class texts read severally.
- Martyrdom at Rome under Nero is historically well attested and morally
  certain in Catholic tradition on the cumulative E-chain beginning with
  1 Clement, while remaining distinct from strict documentary certainty;
  year (64–68) and manner (crucifixion, first explicit in Tertullian c. 200)
  are not fixed; head-down crucifixion is L/E from c. 200/230 onward.
- The archaeology establishes a c. 160 memorial continuously enclosed up to
  the present altar; it cannot identify human remains. The 1968 relic
  identification is reported as contested, with the chain-of-custody and
  Ferrua–Guarducci dispute stated.
- Doctrine (Pastor aeternus) is reported accurately as M-class reception,
  not converted into first-century data, and is set beside Lumen gentium 22
  and Ut unum sint.
- Four labelled Project synthesis judgments are reached, each with reasons,
  the strongest counterargument in its holders' own terms, and a named
  defeater: (i) on the wording of Mt 16:18–19; (ii) on what Antioch shows
  and does not show; (iii) on the letters' usability as historical evidence;
  (iv) on the Roman death and the rejected long episcopate.

## Exclusions and restraint

- No invented scenes, dialogue, psychology, or continuous itinerary; no
  harmony of the Gospels; no use of Acts speeches as transcripts.
- No claim that the 25-year episcopate or Claudian arrival is chronology.
- No forensic authentication (or debunking) of the Vatican bones.
- No adjudication of confessional exegesis of Mt 16:18–19.
- No treatment of 1–2 Peter as uncontested autobiography.
- No images.

## Live uncertainties requiring review

- Year of the crucifixion of Jesus (30/33) and thus of all dependent dates.
- Relation of Gal 2 to Acts 15; date and outcome of the Antioch incident.
- Authorship, date, and setting of 1 Peter; authorship and date of 2 Peter.
- Whether "Babylon" (1 Pt 5:13) can independently establish Rome.
- Year and manner of the martyrdom within 64–68.
- Identity of the Wall-g bones; custody 1942–1953; the standing of
  Guarducci's readings beyond *Petros eni*.
- Whether the earth grave beneath the aedicula is first-century at all
  (von Gerkan's objection against Kirschbaum's reply; Prandi's judgment that
  no Campo P burial is first-century, from which he declined to draw the
  conclusion).
- Direction of dependence between 2 Peter and Jude.
- Whether the alternative recension of Cyprian, De unitate 4 is the author's
  own revision (the 1912 CE account's conclusion, not confirmed here).

## Rights and publication maturity

Project prose is original; quotations follow identified public-domain
translations (Douay–Rheims Challoner and the Clementine Vulgate; ANF/NPNF;
Beveridge's Calvin 1845; Church–Brodribb; Whiston's Josephus; M. R.
James 1924) and the Robinson–Pierpont Greek text, which its distributors
place in the public domain; brief Latin from the Holy See's web text, brief
English from Lumen gentium and Ut unum sint, brief scholarly quotations from
Smothers 1966, and one clause of Metzger's translation of the Muratorian
Fragment are attributed; NABRE and other modern Scripture translations are
not used. Internal editorial and production checking
only; no independent specialist, theological, archaeological, rights, or
ecclesiastical review is claimed.

## Production verification

## Staleness review — 2026-07-26

Both candidates found new source-family records improve auditability without
changing canonical, patristic, archaeological, or reception conclusions. **No
material change.** See
`src/sources/inventories/peter-paul-staleness-review-2026-07-26.md`.

See the production notes in `source-audit.md`; the build, validation, and
page-review record for this revision is kept there and must be updated
with any rebuild.
