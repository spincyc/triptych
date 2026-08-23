# Postcommunion redevelopment audit

This focused record supports the replacement Postcommunion commentary in
`sections/28-postcommunion.tex`. It does not supersede the formulary-wide
`scope.md` or the canonical `source-bindings.toml`.

## Controlling text and grammar

The visually collated 1962 form is:

> Quǽsumus, Dómine Deus noster: ut, quos divínis reparáre non désinis
> sacraméntis, tuis non destítuas benígnus auxíliis. Per Dóminum.

The substantive petition is stable in the checked 1570, 1920, and 1962 Roman
Missals. Typography, accenting, punctuation, orthography, and abbreviated
conclusions vary. The current appointed-text TeX expands the 1962 facsimile's
printed `Per Dóminum.` to `Per Dóminum nostrum.`; the serialized integration
must either reproduce the controlling abbreviation or document an edition
that governs the expansion.

- `reparare` means renew or restore here, not make reparation.
- `non desinis` makes the sacramental renewal continuing divine action.
- `tuis auxiliis` is an ablative of deprivation with `destituas`.
- `benignus` characterizes God as gracious or kind.

The prayer therefore asks that God, in his kindness, not leave without his aid
those whom he does not cease to renew by the divine sacraments. It does not by
itself specify bodily healing, a body-and-soul pair of effects, complete
restoration, emotional cure, or a technical category of actual grace.

## Direct commentary

The earlier claim that the bounded search located no direct commentary is
false. Four direct treatments were checked:

| Witness | Locus | Responsible use |
| --- | --- | --- |
| Prosper Guéranger, *The Liturgical Year*, vol. XI | p. 271 | Says the sacrament repairs losses caused by human misery, then identifies the requested aids as further graces needed to preserve and increase the soul's received treasure. |
| Ildefonso Schuster, *Liber Sacramentorum*, vol. III | p. 123 | Compares bodily food's restoration of spent forces with spiritual nourishment's repair of the soul's losses, and treats continuing help as necessary for eternal life and preservation of Eucharistic fruit. |
| Miguel Nicolau, SJ, “La comunión y la vida de la gracia,” *Revista Española de Teología* 18 (1958) | p. 42 | Cites the prayer while explaining Eucharistic restoration of spiritual strength diminished by daily faults. |
| Leo La Fontaine, thesis on the Sunday Mass formularies (1967) | p. 59 | Traces the prayer through Gelasian, Gregorian, early printed Roman, and modern Roman assignments. |

Guéranger, Schuster, and Nicolau are theological reception. Their fuller
claims must remain attributed and may not be presented as the lexical content
of `reparare`. La Fontaine is a transmission witness, not evidence of
authorship or original compositional intent.

## Transmission

- Mohlberg's critical Old Gelasian prints the prayer at Book III.V, no. 1197,
  p. 178 (manuscript fol. 175v), and again at III.VI, no. 1200, p. 179.
  Mohlberg's diplomatic text has `diuinis … distituas` in both occurrences. Wilson
  normalizes `divinis … destituas` and regards no. 1197 as probably a
  scribal duplication. Neither Gelasian occurrence is assigned to Pentecost X.
- The exact prayer is *Corpus Orationum* 4829.
- *Sacramentarium II de Gellone* no. 1111 transmits it as *Ad complendum* for
  *Dominica XI post octavas Pentecosten*, keyed to SupG 1161. Its preceding
  Collect and Secret are SupG 1159–1160, so this witness transmits the
  three-oration set together.
- Santa Maria de Vilabertran, Paris BnF lat. 1102, no. 478, preserves the same
  Sunday/formulary with `ut quos tuis reparare non…`.
- Gerbert's Alemannic collection and a modern Ambrosian formulary use the
  exact prayer on the First Sunday after Epiphany; the Ambrosian companion
  orations differ.

The evidence establishes durable transmission, movement of the three-oration
set, and later portability of this prayer by itself. It does not establish a
named author, original composition date or calendar location, or the reason
for its eventual Roman placement on Pentecost X.

## Binding additions for serialized integration

The canonical `research/source-bindings.toml` should receive bindings only
after the relevant reusable source records and fingerprints have been checked.
Required loci are:

- Mohlberg, Old Gelasian, nos. 1197 and 1200, pp. 178–179, manuscript
  fol. 175v;
- Wilson, *The Gelasian Sacramentary*, corresponding Book III.V–VI text and
  duplication note;
- *Corpus Orationum* 4829;
- *Sacramentarium II de Gellone* nos. 1109–1111 / SupG 1159–1161;
- Vilabertran no. 478;
- Gerbert's Alemannic formulary, First Sunday after Theophany;
- modern Ambrosian formulary, First Sunday after Epiphany;
- Guéranger, vol. XI, p. 271;
- Schuster, vol. III, p. 123;
- Nicolau (1958), p. 42; and
- La Fontaine (1967), p. 59.

No source identifier or verification fingerprint is invented in this record.

## Exact bibliography and access

- Prosper Guéranger, *The Liturgical Year*, Time after Pentecost, vol. II
  (overall vol. XI), trans. Dom Laurence Shepherd, 2nd ed. (Dublin: James
  Duffy, 1900), p. 271,
  <https://archive.org/details/V11TheLiturgicalYear/page/n303/mode/2up>.
- Ildefonso Schuster, *The Sacramentary (Liber Sacramentorum): Historical and
  Liturgical Notes on the Roman Missal*, trans. Arthur Levelis-Marke, vol. III
  (London: Burns Oates & Washbourne, 1927), p. 123,
  <https://archive.org/details/LiberSacramentorum>.
- Miguel Nicolau, SJ, “La comunión y la vida de la gracia,” *Revista Española
  de Teología* 18 (1958): 35–59, at 42,
  <https://repositorio.sandamaso.es/bitstream/123456789/10164/1/RET-58-1%20%282%29.pdf>.
- Leo La Fontaine, *The Historical Deveopment [sic] of the Postcommunion
  Collects for the Sundays and Some Feast Days of the Church Year* (S.T.M.
  thesis, Concordia Seminary, St. Louis, 1967), p. 59,
  <https://scholar.csl.edu/stm/370/>.
- Leo Cunibert Mohlberg, Leo Eizenhöfer, and Petrus Siffrin, eds., *Liber
  sacramentorum Romanae aeclesiae ordinis anni circuli (Sacramentarium
  Gelasianum)*, Rerum Ecclesiasticarum Documenta, Series Maior, Fontes IV
  (Rome: Herder, 1960), nos. 1197 and 1200, pp. 178–179,
  <https://archive.org/details/mohlberg1960libersacramentorum>.
- H. A. Wilson, ed., *The Gelasian Sacramentary: Liber Sacramentorum Romanae
  Ecclesiae* (Oxford: Clarendon Press, 1894), p. 227,
  <https://archive.org/details/TheGelasianSacramentary/page/n319/mode/2up>.
- *Corpus Orationum* 4829, vol. VII, p. 254,
  <https://usuarium.elte.hu/corpusorationum/4829>.
- *Sacramentarium II de Gellone*, nos. 1109–1111,
  <https://publicacions.iec.cat/repository/pdf/00000188/00000055.pdf>.
- Santa Maria de Vilabertran sacramentary, Paris BnF lat. 1102, no. 478,
  <https://publicacions.iec.cat/repository/pdf/00000174/00000058.pdf>.
- Gerbert, *Monumenta veteris liturgiae Alemannicae* (St. Blasien, 1777–79),
  First Sunday after Theophany,
  <https://www.e-rara.ch/download/pdf/14805899.pdf>.
- Modern Ambrosian First Sunday after Epiphany formulary,
  <https://www.ambrosianeum.net/wp-content/uploads/2021/07/C10-Dominica-I-post-Epiphaniam-A5.pdf>.
