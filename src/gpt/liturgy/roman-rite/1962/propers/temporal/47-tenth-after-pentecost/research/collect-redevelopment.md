# Collect redevelopment record

## Scope

This record supports only the Collect commentary for the Tenth Sunday after
Pentecost. It distinguishes textual control, transmission, Thomistic
reception, and later Roman reception. It does not establish authorship,
original date, or the intention behind the prayer's 1962 assignment.

## Verified text and transmission

- The controlling 1962 facsimile, printed page 389 (PDF page 470), reads
  `misericordiam`. The prayer moves from a relative confession through an
  imperative petition to an `ut` purpose clause.
- H. A. Wilson, *The Gelasian Sacramentary* (1894), Book III, section VI,
  “Item alia missa,” pages 227–228, no. 1198, transmits the Collect with
  `gratiam`, followed by the corresponding Secret and Postcommunion.
- Deshusses, *Le sacramentaire grégorien*, SupG 1159–1161, transmits the
  three-prayer set under `Dominica XI post octabas Pentecosten`. SupG is a
  supplement and must not be represented as the core Hadrianum or as proof of
  Gregory the Great's authorship.

The Gelasian and Gregorian witnesses establish transmission and variant
wording. They do not prove personal authorship, an exact compositional stratum,
the reason for the 1962 assignment, or a common origin for all ten elements of
the later formulary.

## Direct Thomistic reception

- *Summa theologiae* II–II, q. 30, a. 4, ad 3 is the direct Summa locus.
  Thomas says that mercy is especially attributed to God, belongs to supreme
  power, and reaches the effect of participation in the divine good.
- *Super Sententias* IV, d. 46, q. 2, a. 1, qc. 3, arg. 1 and ad 1 quotes the
  Collect and supplies the precise authority argument. God remits penalties
  and gives beyond debt by his own power, because he is subject to none.
  Thomas immediately distinguishes this from the substance of pardoning, in
  which divine goodness is manifested above all.

The older scope's use of *ST* I, q. 25, a. 3 and I–II, q. 113, a. 9 as though
they directly received this Collect should be removed. They are broader
analogues, not the controlling direct loci.

## Later Roman reception

- The 1970 and 2002 Roman Missals assign the prayer, with `gratiam`, to the
  Twenty-sixth Sunday in Ordinary Time.
- *Catechism of the Catholic Church* 270 and 277 receives the axiom through
  forgiveness, conversion from sin, and restoration to friendship by grace.
- Francis, *Misericordiae vultus* 6 cites *ST* II–II, q. 30, a. 4 and calls
  the prayer ancient. Its parenthetical `1198` identifies the Gelasian prayer
  number; it is not the year 1198.

These later uses are reception evidence. They do not demonstrate the original
reason for the prayer's position in the 1962 formulary.

## Binding additions for serialized integration

Add the following loci to the document's shared bindings after the relevant
repository source records have been confirmed:

| Source | Locus | Role | Claim controlled |
| --- | --- | --- | --- |
| `edition.anonymous.gelasian-sacramentary.wilson-clarendon-1894` and its registered artifact | Book III, section VI, pp. 227–228, no. 1198 | transmission | `gratiam` witness and three-prayer set |
| Thomas Aquinas, *Summa theologiae* | II–II, q. 30, a. 4, ad 3 | reception | mercy, supreme power, participation in divine good |
| Thomas Aquinas, *Super Sententias* | IV, d. 46, q. 2, a. 1, qc. 3, arg. 1 and ad 1 | reception | remission by supreme authority; goodness qualification |
| *Catechism of the Catholic Church* | 270, 277 | magisterial reception | forgiveness, conversion, restoration by grace |
| Francis, *Misericordiae vultus* | 6, notes 5–6 | magisterial reception | Thomistic and Gelasian reception of the axiom |
| *Missale Romanum* (2002) | Twenty-sixth Sunday per annum, artifact p. 289 | liturgical reception | postconciliar `gratiam` form |

The Gregorian heading should be cited to Deshusses, SupG 1159–1161. A
searchable manuscript-inventory corroboration is available at
<https://publicacions.iec.cat/repository/pdf/00000188/00000055.pdf>, but it is
secondary and does not replace the edition.

## Replacement point

In `main.tex`, replace the three Collect paragraphs beginning
“The Collect's grammar moves from confession to petition and end” and ending
“not the purpose of its placement here” with:

```tex
\input{sections/31-collect-redevelopment.tex}
```

Because this record was produced in a component-exclusive lane, that shared
integration is intentionally left to the serialized document owner.
