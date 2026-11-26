# Canonical Object Inventory

> Derived mechanically from `shared/objects/**/*.toml` by `shared/generate_editions.py`.
> Do not hand-edit this table; update the canonical TOML records and re-run `--write`.

- **Declared edition-locale:** `2008-latin-2011-us-english` (*Missale Romanum* 2002/2008 + US Roman Missal 2011)
- **As-of date:** 2026-11-25
- **Total canonical records:** 43 (40 current postconciliar sanctuary objects + 3 historically superseded postconciliar forms)

## Current Postconciliar Sanctuary Objects

| ID | English | Latin | Category | Disposition | Server Boundary | 1962 Counterpart | Plate | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pc-obj-altar` | Altar | *Altare* | `sanctuary-furnishings` | `required` | `recognizes-only` | `materially changed` | Plate II | N01 |
| `pc-obj-ambo` | Ambo | *Ambo* | `sanctuary-furnishings` | `required` | `recognizes-only` | `newly provided` | Plate II | N02 |
| `pc-obj-presidential-chair` | Presidential Chair | *Sedes sacerdotis celebrantis* | `sanctuary-furnishings` | `required` | `clergy-reserved` | `materially changed` | Plate II | N03 |
| `pc-obj-credence-table` | Credence Table | *Abacus* | `sanctuary-furnishings` | `required` | `prepares` | `continued` | Plate I | N04 |
| `pc-obj-tabernacle` | Tabernacle | *Tabernaculum* | `sanctuary-furnishings` | `required` | `clergy-reserved` | `materially changed` | Plate II | N05 |
| `pc-obj-sanctuary-lamp` | Sanctuary Lamp | *Lampas peculiaris* | `sanctuary-furnishings` | `required` | `recognizes-only` | `continued` | Plate II | N06 |
| `pc-obj-baptismal-font` | Baptismal Font | *Fons baptismalis* | `sanctuary-furnishings` | `required` | `recognizes-only` | `materially changed` | Plate X | N07 |
| `pc-obj-chalice` | Chalice | *Calix* | `sacred-vessels` | `required` | `prepares` | `materially changed` | Plate III | N08 |
| `pc-obj-paten` | Paten | *Patena* | `sacred-vessels` | `required` | `prepares` | `materially changed` | Plate III | N09 |
| `pc-obj-ciborium` | Ciborium | *Pyxis* | `sacred-vessels` | `provided` | `prepares` | `continued` | Plate III | N10 |
| `pc-obj-pyx` | Pyx | *Pyxis parva* | `sacred-vessels` | `provided` | `recognizes-only` | `continued` | Plate III | N11 |
| `pc-obj-communion-cup` | Communion Cup | *Calix* | `sacred-vessels` | `territorial adaptation` | `prepares` | `newly provided` | Plate III | N12 |
| `pc-obj-cruets` | Cruets | *Urceoli* | `sacred-vessels` | `required` | `presents` | `continued` | Plate VI | N13 |
| `pc-obj-flagon` | Flagon | *Lagoena* | `sacred-vessels` | `permitted` | `handles` | `no established counterpart` | Plate III | N14 |
| `pc-obj-altar-cloth` | Altar Cloth | *Mappa* | `linens` | `required` | `prepares` | `materially changed` | Plate IV | N15 |
| `pc-obj-corporal` | Corporal | *Corporale* | `linens` | `required` | `prepares` | `continued` | Plate IV | N16 |
| `pc-obj-purificator` | Purificator | *Purificatorium* | `linens` | `required` | `prepares` | `continued` | Plate IV | N17 |
| `pc-obj-pall` | Pall | *Palla* | `linens` | `optional` | `prepares` | `optional` | Plate IV | N18 |
| `pc-obj-lavabo-towel` | Lavabo Towel | *Manutergium* | `linens` | `required` | `presents` | `continued` | Plate IV | N19 |
| `pc-obj-roman-missal` | Roman Missal | *Missale Romanum* | `liturgical-books` | `required` | `presents` | `materially changed` | Plate V | N20 |
| `pc-obj-lectionary` | Lectionary for Mass | *Lectionarium* | `liturgical-books` | `required` | `prepares` | `materially changed` | Plate V | N21 |
| `pc-obj-book-of-the-gospels` | Book of the Gospels | *Evangeliarium* | `liturgical-books` | `provided` | `recognizes-only` | `changed use` | Plate V | N22 |
| `pc-obj-book-of-the-chair` | Book of the Chair | *Excerpts from the Roman Missal (no Latin typical edition)* | `liturgical-books` | `territorial adaptation` | `presents` | `no established counterpart` | Plate V | N23 |
| `pc-obj-missal-stand` | Missal Stand | *Pulpitum* | `liturgical-books` | `customary` | `handles` | `continued` | Plate V | N24 |
| `pc-obj-processional-cross` | Processional Cross | *Crux processionalis* | `service-and-incense` | `required` | `carries` | `changed use` | Plate VI | N25 |
| `pc-obj-altar-candles` | Altar Candles | *Candelabra cum cereis* | `service-and-incense` | `required` | `handles` | `materially changed` | Plate I | N26 |
| `pc-obj-sanctuary-bells` | Sanctuary Bells | *Campanula* | `service-and-incense` | `optional` | `handles` | `optional` | Plate VI | N27 |
| `pc-obj-aspergillum-aspersorium` | Aspergillum and Aspersorium | *Aspergillum et aspersorium* | `service-and-incense` | `optional` | `presents` | `changed use` | Plate VI | N28 |
| `pc-obj-thurible` | Thurible | *Turibulum* | `service-and-incense` | `optional` | `handles` | `changed use` | Plate VII | N29 |
| `pc-obj-incense-boat` | Incense Boat | *Navicula* | `service-and-incense` | `optional` | `presents` | `continued` | Plate VII | N30 |
| `pc-obj-alb` | Alb | *Alba* | `vesture-and-ministry` | `required` | `handles` | `changed use` | Plate VIII | N31 |
| `pc-obj-cincture` | Cincture | *Cingulum* | `vesture-and-ministry` | `required` | `handles` | `optional` | Plate VIII | N32 |
| `pc-obj-amice` | Amice | *Amictus* | `vesture-and-ministry` | `required` | `handles` | `optional` | Plate VIII | N33 |
| `pc-obj-stole` | Stole | *Stola* | `vesture-and-ministry` | `required` | `clergy-reserved` | `changed use` | Plate VIII | N34 |
| `pc-obj-chasuble` | Chasuble | *Casula* | `vesture-and-ministry` | `required` | `clergy-reserved` | `continued` | Plate VIII | N35 |
| `pc-obj-dalmatic` | Dalmatic | *Dalmatica* | `vesture-and-ministry` | `provided` | `clergy-reserved` | `continued` | Plate VIII | N36 |
| `pc-obj-cassock-surplice` | Cassock and Surplice | *Vestis talaris et superpelliceum* | `vesture-and-ministry` | `permitted` | `handles` | `changed use` | Plate IX | N37 |
| `pc-obj-cope` | Cope | *Pluviale* | `vesture-and-ministry` | `provided` | `clergy-reserved` | `continued` | Plate IX | N38 |
| `pc-obj-humeral-veil` | Humeral Veil | *Velum humerale* | `vesture-and-ministry` | `provided` | `presents` | `changed use` | Plate IX | N39 |
| `pc-obj-holy-oils-stocks` | Holy Oils and Oil Stocks | *Olea sancta et vasa oleorum* | `sacramental-adjacent` | `required` | `moves-only-by-direction` | `materially changed` | Plate X | N40 |

## Historically Superseded Postconciliar Forms (Chronological Separation)

| ID | Form | Latin | Period | Controlling Act | Disposition | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `pc-obj-hist-subdeacon-tunicle-maniple` | Subdeacon's Tunicle and Maniple | *Tunicella et manipulus* | 1967–1972 | Tres abhinc annos (1967) no. 25; Ministeria quaedam (1972); 1975 Missale Romanum; CE (1984) no. 56 | `superseded` | N41 |
| `pc-obj-hist-fragile-vessels-pouring` | Fragile Vessels, Flagon Pouring, and EMHC Purification | *Vasa fragilia et infusio* | 1970–2006/2011 | GIRM (2002/2008) nos. 279, 328–330; Redemptionis Sacramentum (2004) nos. 106, 117, 119; CDWDS letter (Oct 2006); USCCB Norms (2011) no. 53 | `superseded` | N42 |
| `pc-obj-hist-1970-sanctuary-clarifications` | Sanctuary, Cross, Tabernacle, Altar Card, and Veil Clarifications (1970/1975) | *Crux, tabernaculum, tabellae et velum* | 1970–2002/2008 | CDWDS Response (25 Sept 2000, Prot. N. 2036/00/L); GIRM (2002/2008) nos. 118c, 299, 306, 308, 314–315 | `superseded` | N43 |
