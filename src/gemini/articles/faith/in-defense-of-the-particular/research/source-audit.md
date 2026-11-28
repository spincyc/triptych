# Source Audit: In Defense of the Particular

- **Publication:** `gemini/articles/faith/in-defense-of-the-particular`
- **Audit date:** 2026-11-28 (updated after independent cold-review remediation)
- **Verification standard:** Every verbatim English quotation in the body, endnotes, and appendices was read directly from a locally tracked, public-domain text artifact under `src/sources/works/` and pinned in `research/source-bindings.toml` with its exact SHA-256 fingerprint. Latin citations from Aquinas's *De ente et essentia* were collated directly in the tracked Baur–Koch Latin artifact and rendered closely inline without English quotation marks.

## 1. Verified Public-Domain Primary Witnesses (Direct Collation)

### Sacred Scripture (Challoner Douay-Rheims, Project Gutenberg eBook 1581)
Collated directly against the single reading-text witness `artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.gutenberg-text-7d10da78` (`pg1581.txt`, matching sibling essays in *The Creature Before God*), replacing the earlier control-text `american-1899-ebible` TSVs that carried OCR errors at Deut 10:17 and Ps 8:5. All 43 cited loci verified directly:
- `Gen.12.1-3` (confirming `IN THEE shall all the kindreds of the earth be blessed.`), `Deut.7.6-8`, `Deut.10.14-19`, `Ps.8.4-6`, `Wis.11.21`, `Wis.11.25`, `Wis.11.27`, `Isa.2.2-3`, `Isa.49.6`, `Amos.9.7`, `Matt.1.1`, `Matt.1.16-17`, `Matt.13.55-57`, `Matt.16.15`, `Matt.25.35-36`, `Matt.25.40`, `Mark.6.3-5`, `Luke.2.1-2`, `Luke.3.1-2`, `Luke.3.23`, `Luke.3.38`, `John.1.14`, `John.1.45-46`, `John.4.24`, `John.14.6`, `John.20.27-28`, `John.21.9`, `John.21.12-13`, `John.21.15-17`, `Acts.4.12`, `Acts.17.27-28`, `Rom.9.4-5`, `Rom.11.17-18`, `Rom.11.28-29`, `Rom.11.33`, `1Cor.1.23`, `Gal.4.4-5`, `1Tim.2.4-5`, `Heb.1.1-2`, `Heb.2.16`, `1John.4.19-21`, `Apoc.2.17` (`a white counter`), `Apoc.5.9`.

### Patristic and Scholastic Witnesses
- **St. Irenaeus, *Against Heresies***: Collated directly in `artifact.ante-nicene-fathers.volume-1.ccel-web-2026-10-13.ccel-text-ee9c7f0a` (dated CCEL electronic text, exact reprint date not asserted: III.18.1, 7; III.22.1–2, 4; IV.22.2) and checked Buffalo 1887 witness `artifact.ante-nicene-fathers.volume-1.buffalo-1887.irenaeus-adversus-haereses-5.praef-checked-text-f4b5cc69` (V, preface).
- **St. Athanasius, *On the Incarnation of the Word***: Collated directly in checked 1892 texts (`athanasius-de-incarnatione-8.1-checked-text-9bb74c9a`, `54.2-3-checked-text-99993354`) and tracked NPNF2-4 volume `ia-djvu-text-ae54c8ba` (New York: The Christian Literature Company; Oxford and London: Parker & Company, 1892: §§ 9.3, 41.5, 42.7, 43.1, 3–4, 44.2, 5–8). Unused loci (`8.2-3`, `45`) removed from audit and references.
- **St. Gregory of Nazianzus, *Oration 38***: Collated directly in unrevised CCEL NPNF2-7 electronic text `artifact.nicene-and-post-nicene-fathers.series-2-volume-7.ccel-web-2026-10-06.ccel-text-56d84cfa` (file header cites New York: Christian Literature Publishing Co., 1893; not collated as a facsimile: §§ 11, 13–14), avoiding New Advent's modernized web revision (`complete-oration-text-635aae9d`).
- **St. John Chrysostom, *Homilies on Matthew***: Collated directly in CCEL NPNF1-10 electronic text `artifact.nicene-and-post-nicene-fathers.series-1-volume-10.ccel-web-2026-09-17.ccel-text-adb8f1c9` (file header cites New York: Christian Literature Publishing Co., 1886; identity with a specific historical printing not asserted: Homily 50, §§ 4–5). De-duplicated against Part II (*The Due Return*) by quoting the non-overlapping sentences on golden cups vs. cold water and the distressed brother as living temple.
- **St. Augustine, *The City of God***: Collated directly in `artifact.augustine.de-civitate-dei.dods-1871.pg45304-body-lf` (Edinburgh: T. & T. Clark, 1871; Project Gutenberg eBook 45304; Book X translated by Marcus Dods: 10.5, 10.6, 10.28, 10.29, 10.32).
- **St. Augustine, *Tractates on the Gospel of John***: Collated directly in CCEL NPNF1-7 electronic text `artifact.nicene-and-post-nicene-fathers.series-1-volume-7.ccel-web-2026-09-17.ccel-text-266502c9` (file header cites New York: Christian Literature Publishing Co., 1886; identity with a specific historical printing not asserted: Tractate 80, § 3; Tractate 123, §§ 2, 5).
- **St. Leo the Great, *Letters* and *Sermons***: Collated directly in CCEL NPNF2-12 electronic text `artifact.nicene-and-post-nicene-fathers.series-2-volume-12.ccel-web-2026-09-28.ccel-text-7bb1db6e` (exact print impression not asserted: *Letter 28* / Tome §§ 3–4; *Sermon 74* § 2, verifying Feltoe's translation `"was changed into a sacramental presence"` and his apparatus citation of the Latin phrase *in sacramenta transivit*) and checked New York 1895 excerpts (`leo-sermo-21.1-checked-text-5097e399`, `leo-sermo-21.2-checked-text-d9bfbd1d`, `leo-sermo-54.4-wondrous-exchange-checked-text-7f1cfed1`).
- **St. Thomas Aquinas, *Summa Theologiae* (Prima Pars & Tertia Pars)**: Collated directly in tracked Project Gutenberg English Dominican electronic texts `pg17611-body-9c99a67a` (eBook 17611; exact print year not inferred: I, q. 3, a. 5; q. 8, a. 1; q. 14, a. 11; q. 22, aa. 2–4; q. 29, aa. 1, 3; q. 44, a. 1; q. 85, a. 1; q. 86, a. 1; q. 104, a. 1) and `pg19950-body-4597132e` (eBook 19950; exact print year not inferred: III, q. 1, a. 1 [including Volusianus *Ep.* 135 and Augustine *Ep.* 137]; q. 2, aa. 1–2 [including Chalcedon]; q. 4, aa. 4–5 [including Damascene]; q. 60, a. 4; q. 61, a. 1; q. 64, a. 7; q. 75, a. 1 [including obj. 3]; q. 76, a. 3 [including obj. 3]).
- **St. Thomas Aquinas, *De ente et essentia***: Collated directly in tracked Latin text `oee-historical-latin-aa6b1de0` (Baur–Koch, Münster: Aschendorff, 1933: cc. 2, 3, 5); rendered closely inline without English quotation marks.

## 2. Rights-Restricted / Catalog-Only Magisterial Sources (Independent Paraphrase Only)

The following official Catholic magisterial texts are bound as `role = "bibliographic"`, `states = ["cataloged"]` and presented strictly in independent analytical doctrinal paraphrase with zero verbatim reproduction:
- *Catechism of the Catholic Church* (1997 Latin typical edition): §§ 1084–1085, 1145–1152.
- Second Vatican Council, *Lumen gentium* (1964): § 16.
- Second Vatican Council, *Nostra aetate* (1965): §§ 2, 4.
- Second Vatican Council, *Dei Verbum* (1965): §§ 2–4, 14–16.
- Second Vatican Council, *Gaudium et spes* (1965): § 22 (preserving the exact *quodammodo* reserve).
- Pope St. John Paul II, *Redemptoris missio* (1990): §§ 5–6, 28.
- Pope St. John Paul II, *Fides et ratio* (1998): §§ 7, 11–12.
- Congregation for the Doctrine of the Faith, *Dominus Iesus* (2000): §§ 6, 13–15.

## 3. Untracked Interlocutors (Conceptual Engagement Boundary)

No local public-domain full-text artifacts exist in the repository for Celsus (preserved in Origen's *Contra Celsum*, whose cataloged ANF-4 HTML artifacts are remote/restricted), Baruch Spinoza, Gotthold Ephraim Lessing, Immanuel Kant, Søren Kierkegaard, Thomas Paine, Thomas Chalmers, John Hick, or Francisco Suárez. Boethius's definition of person is cited via Aquinas (*ST* I, q. 29, a. 1), and Bl. John Duns Scotus is mentioned historically for the school contrast on individuation (*haecceitas*). Zero verbatim quotations are attributed to any of these figures; this boundary is disclosed in `sections/90-scope-method-qualifications.tex` and `sections/99-references.tex`.
