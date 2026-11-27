# Plate Manifest

- **Owner:** `src/gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary`
- **Declared edition-locale:** *Missale Romanum*, *editio typica tertia* (2002; *reimpressio emendata* 2008) and *The Roman Missal, Third Edition* (United States, 2011) with USCCB GIRM adaptations
- **As-of date:** 2026-11-25
- **Page format:** US Letter portrait, monochrome graphite artwork seamlessly integrated on white ground; all labels, position keys, scale notices, monochrome liturgical-color pattern keys, and note keys typeset by TeX.

## Master Plate Schedule (10 Monochrome Graphite Plates)

| Plate ID | Plate Title | Artwork Asset | Scale Treatment | Primary Depicted Objects | Editions Consuming |
| --- | --- | --- | --- | --- | --- |
| `pc-plt-01-sanctuary` | Plate I — The Postconciliar Roman Sanctuary | `pc-art-01-sanctuary-composition.png` | Not to common scale (architectural perspective) | Altar, Ambo, Presidential Chair, Credence Table, Tabernacle, Sanctuary Lamp, Altar Cloth, Altar Candles, Altar/Processional Cross, Cruets | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-02-furnishings` | Plate II — Principal Sanctuary Furnishings | `pc-art-02-altar-ambo-chair.png` | Not to common scale | Altar, Ambo, Presidential Chair, Tabernacle, Sanctuary Lamp | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-03-vessels` | Plate III — Sacred Vessels and Vessels for Communion | `pc-art-03-sacred-vessels.png` | Not to common scale | Chalice, Paten, Ciborium, Flagon, Communion Cup, Pyx | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-04-linens` | Plate IV — Altar and Vessel Linens | `pc-art-04-white-linens.png` | Not to common scale | Corporal (unfolded 3x3 & folded), Purificator, Pall, Lavabo Towel, Altar Cloth | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-05-books` | Plate V — Liturgical Books and Stands | `pc-art-05-liturgical-books.png` | Relative proportions shown | Roman Missal, Missal Stand, Lectionary for Mass, Book of the Gospels, Book of the Chair | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-06-service` | Plate VI — Processional and Service Equipment | `pc-art-06-service-cruets-bells.png` | Not to common scale | Cruets (with tray), Lavabo Pitcher & Basin, Processional Cross, Sanctuary Bells, Aspergillum & Aspersorium | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-07-incense` | Plate VII — Incense Equipment | `pc-art-07-incense-set.png` | Not to common scale | Thurible (closed & open fire-pan inset), Incense Boat and Spoon | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-08-vesture-ordained` | Plate VIII — Ordained Vesture at Mass | `pc-art-08-priest-deacon-vesture.png` | Common scale (standing figures; detail insets not to scale) | Alb, Cincture, Amice, Stole (priestly straight & diaconal diagonal), Chasuble, Dalmatic | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-09-vesture-choir-solemn` | Plate IX — Choir Dress and Solemn Ceremonial Vesture | `pc-art-09-black-cassock-surplice-cope.png` | Common scale (standing figures) | Cassock and Surplice, Cope, Humeral Veil | Comprehensive, Altar Server, Sacristan, General Reader |
| `pc-plt-10-communion-sacramental` | Plate X — Communion Under Both Kinds and Sacramental Vessels | `pc-art-10-communion-triduum-vessels.png` | Not to common scale | Communion Cup, Ciborium (veiled), Chalice, Paten, Corporal, Purificator, Holy Oils Stocks, Baptismal Font | Comprehensive, Altar Server, Sacristan, General Reader |

## Web-Edition Accessible Equivalents

Every plate block is enclosed in `\ifdefined\TriptychPrintEdition ... \else ... \fi` in the deterministically generated TeX sections. Native print renders the 8-bit grayscale PNG plate with its typeset header, scale notice, and position key; web conversion renders an object-level visual summary and spatial reading order from `shared/schema/plates-and-editions.toml` without duplicating authoritative descriptions.
