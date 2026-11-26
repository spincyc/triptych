# Scope and plan: Advent, a handbook for the season (Claude, postconciliar)

Status: plan of 2026-11-26, settled after the five research lanes reported.
The body plan below is the one the writer received; later phases record their
results in `source-audit.md`, `source-bindings.toml` and `cold-review.md`
beside this file.

## Work identity

| Field | Value |
| --- | --- |
| Leaf | `src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/seasons/advent` |
| Kind and type | `seasonal-handbook-postconciliar`, document type `liturgy-reference-v1` |
| Profile | `guidance/liturgy/postconciliar-seasonal-handbooks.md`, which imports the standard of `guidance/liturgy/roman-1962-seasonal-handbooks.md` |
| Provider | Claude. A ChatGPT edition of the same season stands beside it at `src/gpt/…/seasons/advent`; neither draws on the other. |
| Rite and books | Roman Rite: *Missale Romanum*, third typical edition (2002, emended 2008) and the Roman Missal in its U.S. English edition (2011); the *Lectionary for Mass* for the dioceses of the United States; the *Liturgy of the Hours*; the General Roman Calendar with the proper calendar of the United States |
| Catalog | `library/novus-ordo-liturgy.md`, Seasonal Handbooks, Advent row, Claude column |
| As-of | Advent 2026: First Sunday 29 November 2026, Sunday cycle B; statements of law and calendar current on 26 November 2026 |
| Length | About 16,500–18,000 words of body text, with four appendices |

## Reader and purpose

A Catholic in a parish in the United States who wants to understand Advent and
to keep it at Mass, in the Liturgy of the Hours and at home, and who may be new
to the Hours. The handbook prepares that reader before the season and goes
with them through it: what the Church means by the Lord's coming, how she came
to keep the season, how to watch, pray, do penance and works of mercy and go
to confession, what each week and each of the last eight days give, and the
Fathers on Bethlehem and the manger at the threshold of Christmas.

The voice speaks from within the tradition (`guidance/editorial.md`, "Speaking
from within the tradition"): the Fathers, the saints, the popes and the
liturgy itself carry the teaching, quoted at identified places from held
witnesses, with the writer's own inferences stated once and plainly as such.
The book does not use the labels "Novus Ordo", "Ordinary Form",
"Traditional Latin Mass" or "Extraordinary Form", and does not grade one form
of the Roman Rite against another. The sister volume for the 1962 books
(`src/claude/liturgy/roman-rite/1962/seasons/advent`) was read for register
only.

## Boundary

The handbook owns the season. It names each Sunday's and weekday's readings by
citation and gives the Office of Readings' second reading by author and work;
it does not reproduce or expound a whole formulary. Proper guides for single
Sundays, where they exist, own their formularies.

## Rights that shape the text

- The ICEL English of the 2011 Missal, the New American Bible text of the
  Lectionary, the U.S. psalm responses and the modern English of the Liturgy
  of the Hours are never printed; they are described and cited by place.
- Postconciliar Latin with no public-domain witness is not printed. Where an
  older Roman prayer stands behind a present one, the older prayer is quoted
  as itself and called its antecedent.
- Prayers printed for saying reproduce one identified received witness each,
  unaltered: the Angelus and its prayer (the Raccolta, 1910), whose body
  is the Collect of the Fourth Sunday of Advent; the Entrance Antiphon of
  the Fourth Sunday (Missal of 1922; Lasance, 1945); the
  great O antiphons (Breviary of 1888; Bute, 1908); and the others listed in
  `source-audit.md`.
- Holy See texts of 1969–1975 (the Universal Norms on the Liturgical Year and
  the Calendar, the commentary on the calendar, *Mysterii Paschalis*, the
  Missal constitution, *Marialis cultus*) are paraphrased with their numbers.
  Later papal and curial texts are paraphrased sparingly.
- Scripture is quoted from the Douay-Rheims (Challoner) and the Clementine
  Vulgate in the library's tracked verse texts, each with its own reference;
  Lectionary citations use the U.S. Lectionary's verse division and the Hebrew
  numbering of the psalms.

## Law

Present law is stated with its body, territory and date where first given (the
1983 Code; the U.S. bishops' Pastoral Statement on Penance and Abstinence of
1966; the U.S. holy days of obligation and their Sunday rule), and kept apart
from history. Personal disciplines are given as counsel.

## Body plan and the passage that makes each chapter worth reading

| File | Chapter | The passage it is built on |
| --- | --- | --- |
| `05-to-the-reader` | To the Reader | The three books, the Sunday cycle (2026 is Year B) and a first way to begin. |
| Part One | The Coming | Part heading: what the Church awaits, and how she came to keep the season. |
| `10-go-out-to-meet-him` | Go Out to Meet Him | The year's first Collect asks to go out to meet Christ with just works; its old home is a Gelasian prayer after Communion, and the First Sunday's Office still sings *Aspiciens a longe … Ite obviam ei* after Cyril. |
| `12-two-comings` | Two Comings, and the One Between | Cyril, Catechesis 15.1, read that Sunday; Bernard's middle coming (Sermon 5 on Advent); Advent Preface I keeps the frame of a Veronense Ascension preface. |
| `14-history` | How the Church Came to Keep Advent | Saragossa and 17 December; Perpetuus and Mâcon; the Gelasian and Gregorian books; the Council and the reform of 1969–1970, the new Missal taking force on the First Sunday of Advent 1969. |
| Part Two | Keeping Advent | Part heading: watching, prayer, penance and mercy, a rule, confession. |
| `20-watch` | Watch | The doorkeeper of Mark 13 (Year B); Chrysostom and Gregory on the hidden hour. |
| `22-prayer` | The Day's Prayer | The Hours for all the faithful; the Angelus, whose prayer is the Fourth Sunday's Collect. |
| `24-penance-and-mercy` | Penance and Mercy | Present law beside the old Advent fast; Matthew 25 with Chrysostom. |
| `26-rule-of-life` | A Rule for the Season | Counsel for a short and a fuller rule, for the sick, the bereaved and households. |
| `28-confession` | Confession before Christmas | John's preaching; Trent, Session 14. |
| Part Three | Through the Weeks | Part heading: each week, the last eight days, the Fourth Sunday and the Vigil. |
| `30-first-week` | The First Week | "O that thou wouldst rend the heavens" (Year B); the centurion's words and the words before Communion. |
| `31-second-week` | The Second Week | The Baptist; the Immaculate Conception, patroness of the United States, and *Ineffabilis Deus*; Our Lady of Guadalupe. |
| `32-third-week` | The Third Week | *Gaudete*; Augustine's "John the voice, Christ the Word", read that Sunday. |
| `33-last-days` | The Last Days: 17 to 24 December | The O antiphons at Evening Prayer and, in another order, at Mass; each day's Gospel with its Father, from Leo's Wisdom on the evening of *O Sapientia* to Augustine's Wisdom shown as an infant on the 24th. |
| `34-fourth-sunday` | The Fourth Sunday | *Rorate caeli*; the Angelus prayer as the Collect, whose oldest Roman place is the Annunciation. |
| `36-vigil-and-night` | The Vigil and the Holy Night | The Benedictus at the morning Mass of 24 December; the Gloria returning with the angels' song. |
| Part Four | Toward Bethlehem | Part heading: the Fathers on Bethlehem, the manger and the exchange. |
| `40-house-of-bread` | The House of Bread | Gregory, Homily 8: Bethlehem, the house of bread, and the manger; Greccio, with Bonaventure and Pope Francis (*Admirabile signum*, signed there on the First Sunday of Advent 2019). |
| `42-swaddling-bands` | The Swaddling Bands | Luke 2:7 and 23:53; Gregory's leaps of the Lord. |
| `44-wonderful-exchange` | The Wonderful Exchange | *O admirabile commercium*; the Letter to Diognetus; Irenaeus; Athanasius. |
| `48-the-holy-night` | The Holy Night | St Thérèse of Lisieux on the grace of Christmas night 1886; Leo, Sermon 21, read on Christmas Day: "Christian, acknowledge thy dignity." |

Appendices: `90-daily-readings` (Sundays A/B/C, the weekdays to 16 December,
17–24 December with the O antiphons, the feasts, the Christmas Masses, and how
to find the day, with Advent 2026 worked); `92-prayers` (received texts only);
`95-scope` (About This Book, scope-appendix role); `99-references`
(references role).

## Process

Five research lanes (law and history; the Mass; the Office; the Fathers on the
Gospels; saints and papal teaching) verified or refuted the plan and
registered missing witnesses; one evidence pack was collated; one cold writer
wrote the body from it, and two others wrote the appendices; a blind reader
and an accuracy reviewer then read the whole (`cold-review.md`).

## Changes after the cold review

The two cold reviews (`cold-review.md`) added two voices the plan lacked: St
Thérèse of Lisieux at the holy night, and Pope Francis at Greccio. The Angelus
is printed from one witness, the Raccolta of 1910, in both places it appears;
"Finding the Day" now opens the daily readings; and the body states its rules
for any year, keeping 2026 as an example.
