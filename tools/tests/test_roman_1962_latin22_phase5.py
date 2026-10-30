"""Twenty-two bounded whole-Latin adoptions from pre-frozen primary-image proof.

Fixed oracles originate before canonical edits. This source gate is not annual
or independent acceptance. Older source oracles and their body bytes stay pinned.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys
import tomllib
import unicodedata
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/"scripts")]
from tools.tests import _source_batch_guards as BATCH_GUARDS
import _calendars as C
from _proper_latin import LatinKey, SURFACES, body_owners, decision_for, publication_records, read_sidecar
from tools.tests.test_roman_1962_octnov_commemoration_source_repair import record

def digest(x):
    return hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":"))
def key(x):
    return LatinKey.from_mapping(x)
def tokens(s):
    s=unicodedata.normalize("NFD",s.lower().replace("æ","ae").replace("œ","oe"))
    s="".join(c for c in s if not unicodedata.combining(c)).replace("j","i")
    return re.findall(r"[a-z]+",s)
def received(s):
    return [dict(sepulchro="sepulcro",coelestibus="caelestibus",coeleste="caeleste",
                 poenitentiae="paenitentiae").get(x,x) for x in tokens(s)]
def node_at(n,path):
    for k in path:n=n[k]
    return n
def yaml_unowned(s):
    tree=yaml.compose(s,Loader=yaml.CLoader)
    def at(n,path):
        for k in path:n=n.value[k] if isinstance(k,int) else {a.value:b for a,b in n.value}[k]
        return n
    spans=sorted((at(tree,x["path"]).start_mark.line,at(tree,x["path"]).end_mark.line) for x in ORACLES)
    lines=s.splitlines(keepends=True);out="";cursor=0
    for a,b in spans:out+="".join(lines[cursor:a]);cursor=b
    return out+"".join(lines[cursor:])
def ledger_unowned(s):
    parts=re.split(r"(?m)^\[\[entries\]\]\n",s);out=parts[0]
    for p in parts[1:]:
        x=tomllib.loads("[[entries]]\n"+p)["entries"][0]
        if key(x) not in KEYS:out+="[[entries]]\n"+p
    return out

ORACLES = json.loads(r'''[
  {
    "mass": "commune-plurimorum-martyrum-3",
    "form": "",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "common",
      "masses",
      7,
      "propers",
      5
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Te Martyrum candidatus laudat exercitus,\nDomine. Alleluia.\n",
    "body_sha256": "0c087cf38c152a856f483a806d14c4a63056ca5e38cf040e08ffcacc885bfaf0",
    "historical_body": "Alleluja, alleluja. V. Te Martyrum candidatus laudat exercitus, Domine. Alleluja.",
    "historical_ending": "Domine. Alleluja.",
    "target_ending": "Domine. Alleluia.",
    "target_locus": "PDF 821 / printed [13]; left; unit 4264; Commune plurimorum Martyrum extra tempus paschale; III Salus autem iustorum continuation",
    "historical_locus": "PDF 685 / printed [15]; right bottom; Commune plurimorum Martyrum; De eodem Communi Alia Missa, Salus autem iustorum",
    "target": {
      "pdf": [
        821
      ],
      "printed": "[13]",
      "unit": 4264,
      "column": "left",
      "heading": "Commune plurimorum Martyrum extra tempus paschale; III Salus autem iustorum continuation"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        685
      ],
      "printed": "[15]",
      "column": "right bottom",
      "heading": "Commune plurimorum Martyrum; De eodem Communi Alia Missa, Salus autem iustorum"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "physical_line_ranges": [
      [
        1,
        2
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i."
    ],
    "restored": false
  },
  {
    "mass": "nativitate-domini-octave",
    "form": "Ad tertiam Missam in die",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "christological",
      "masses",
      7,
      "forms",
      2,
      "propers",
      4
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Dies sanctificatus illuxit nobis: venite,\ngentes, et adorate Dominum: quia hodie descendit lux magna super\nterram. Alleluia.\n",
    "body_sha256": "355b92fdc4351a3ee69c6da72b8b4833e5e965af8a2cb98877e58b23bde69176",
    "historical_body": "Alleluja, alleluja. V. Dies sanctificatus illuxit nobis: venite gentes, et adorate Dominum: quia hodie descendit lux magna super terram. Alleluja.",
    "historical_ending": "terram. Alleluja.",
    "target_ending": "terram. Alleluia.",
    "target_locus": "PDF 102 / printed 21; right top; unit 135; In Nativitate Domini; third Mass in die",
    "historical_locus": "PDF 106 / printed 20; left top; Christmas third Mass continuation, before St.Stephen heading",
    "target": {
      "pdf": [
        102
      ],
      "printed": "21",
      "unit": 135,
      "column": "right top",
      "heading": "In Nativitate Domini; third Mass in die"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        106
      ],
      "printed": "20",
      "column": "left top",
      "heading": "Christmas third Mass continuation, before St.Stephen heading"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-nativitate-domini-octave-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-nativitate-domini-octave-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-nativitate-domini-octave-alleluia",
    "physical_line_ranges": [
      [
        4,
        6
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i; target comma after venite declared."
    ],
    "restored": false
  },
  {
    "mass": "commune-unius-martyris-2",
    "form": "",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "common",
      "masses",
      2,
      "propers",
      5
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Hic est sacerdos, quem coronavit Dominus.\nAlleluia.\n",
    "body_sha256": "5b8d34963dd1739949a0933d110cbefd33977b552741d89a66b3c5ec97cc70b2",
    "historical_body": "Alleluja, alleluja. V. Hic est Sacerdos, quem coronavit Dominus. Alleluja.",
    "historical_ending": "Dominus. Alleluja.",
    "target_ending": "Dominus. Alleluia.",
    "target_locus": "PDF 814 / printed [6]; left; unit 4208; Commune unius Martyris extra tempus paschale; II Pro Martyre Pontifice continuation",
    "historical_locus": "PDF 674 / printed [4]; right; Commune unius Martyris Pontificis; De eodem Communi, Alia Missa",
    "target": {
      "pdf": [
        814
      ],
      "printed": "[6]",
      "unit": 4208,
      "column": "left",
      "heading": "Commune unius Martyris extra tempus paschale; II Pro Martyre Pontifice continuation"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        674
      ],
      "printed": "[4]",
      "column": "right",
      "heading": "Commune unius Martyris Pontificis; De eodem Communi, Alia Missa"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-commune-unius-martyris-2-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-commune-unius-martyris-2-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-commune-unius-martyris-2-alleluia",
    "physical_line_ranges": [
      [
        8,
        9
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i; historical Sacerdos / target sacerdos capitalization."
    ],
    "restored": false
  },
  {
    "mass": "advent-3",
    "form": "",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      2,
      "propers",
      4
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Excita, Domine, potentiam tuam, et veni, ut\nsalvos facias nos. Alleluia.\n",
    "body_sha256": "0188d53c71815633e8cf11e8d8a245f74e98481cafb978ebe38348733b0b3ccc",
    "historical_body": "Alleluja, alleluja. V. Excita Domine potentiam tuam, et veni, ut salvos facias nos. Alleluja.",
    "historical_ending": "nos. Alleluja.",
    "target_ending": "nos. Alleluia.",
    "target_locus": "PDF 86 / printed 5; left top; unit 25; Third Advent Sunday continuation, before FeriaIV heading",
    "historical_locus": "PDF 92 / printed 6; left top; Third Advent Sunday continuation, before FeriaIV heading",
    "target": {
      "pdf": [
        86
      ],
      "printed": "5",
      "unit": 25,
      "column": "left top",
      "heading": "Third Advent Sunday continuation, before FeriaIV heading"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        92
      ],
      "printed": "6",
      "column": "left top",
      "heading": "Third Advent Sunday continuation, before FeriaIV heading"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-advent-3-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-advent-3-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-advent-3-alleluia",
    "physical_line_ranges": [
      [
        11,
        12
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i; target commas around Domine explicitly retained."
    ],
    "restored": false
  },
  {
    "mass": "easter-tuesday",
    "form": "",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      71,
      "propers",
      4
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Surrexit Dominus de sepulcro, qui pro nobis\npependit in ligno.\n",
    "body_sha256": "a2964bcbc4d25603e63aaef01081a6db08505a9ea7cd841b206d3259e085c641",
    "historical_body": "Alleluja, alleluja. V. Surrexit Dominus de sepulchro, qui pro nobis pependit in ligno.",
    "historical_ending": "in ligno.",
    "target_ending": "in ligno.",
    "target_locus": "PDF 414 / printed 333; right; unit 1166; FeriaIII infra octavam Paschae; after Graduale1165 and before Sequentia1167",
    "historical_locus": "PDF 358 / printed 272; right; FeriaIIIpostPascha; after Graduale and before Sequentia",
    "target": {
      "pdf": [
        414
      ],
      "printed": "333",
      "unit": 1166,
      "column": "right",
      "heading": "FeriaIII infra octavam Paschae; after Graduale1165 and before Sequentia1167"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        358
      ],
      "printed": "272",
      "column": "right",
      "heading": "FeriaIIIpostPascha; after Graduale and before Sequentia"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-easter-tuesday-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-easter-tuesday-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-easter-tuesday-alleluia",
    "physical_line_ranges": [
      [
        14,
        15
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i.",
      "Historical sepulchro / target sepulcro is a real received spelling; not an OCR correction."
    ],
    "restored": false
  },
  {
    "mass": "easter-thursday",
    "form": "",
    "proper": "Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      73,
      "propers",
      4
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Surrexit Christus, qui creavit omnia: et\nmisertus est humano generi.\n",
    "body_sha256": "2c0b6384f0112c7cbfdb68e5a8feeb2430673ef063f44374328df073942fd635",
    "historical_body": "Alleluja, alleluja. V. Surrexit Christus, qui creavit omnia, et misertus est humano generi.",
    "historical_ending": "humano generi.",
    "target_ending": "humano generi.",
    "target_locus": "PDF 418 / printed 337; left bottom; unit 1188; FeriaV infra octavam Paschae; after Graduale1187",
    "historical_locus": "PDF 362 / printed 276; right; FeriaVpostPascha; after Graduale before Sequentia",
    "target": {
      "pdf": [
        418
      ],
      "printed": "337",
      "unit": 1188,
      "column": "left bottom",
      "heading": "FeriaV infra octavam Paschae; after Graduale1187"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        362
      ],
      "printed": "276",
      "column": "right",
      "heading": "FeriaVpostPascha; after Graduale before Sequentia"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-easter-thursday-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-easter-thursday-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-easter-thursday-alleluia",
    "physical_line_ranges": [
      [
        17,
        18
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i; historical comma after omnia / target colon."
    ],
    "restored": false
  },
  {
    "mass": "pentecost-ember-wednesday",
    "form": "",
    "proper": "Second Alleluia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      89,
      "propers",
      6
    ],
    "lane": "pustet",
    "body": "Alleluia, alleluia. V. Veni, Sancte Spiritus, reple tuorum corda\nfidelium: et tui amoris in eis ignem accende.\n",
    "body_sha256": "ffb81b41664b394f896ca1e4a08258361e4e605285923035f1d2f65a154ba51c",
    "historical_body": "Alleluja, alleluja. V. Veni sancte Spiritus, reple tuorum corda fidelium: et tui amoris in eis ignem accende.",
    "historical_ending": "ignem accende.",
    "target_ending": "ignem accende.",
    "target_locus": "PDF 443 / printed 362; right; unit 1346; FeriaIV Quatuor Temporum Pentecostes; follows second Lesson1345, before Sequence1347",
    "historical_locus": "PDF 391 / printed 305; left; FeriaIV Quatuor Temporum Pentecostes; after second Lesson and before Sequence",
    "target": {
      "pdf": [
        443
      ],
      "printed": "362",
      "unit": 1346,
      "column": "right",
      "heading": "FeriaIV Quatuor Temporum Pentecostes; follows second Lesson1345, before Sequence1347"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        391
      ],
      "printed": "305",
      "column": "left",
      "heading": "FeriaIV Quatuor Temporum Pentecostes; after second Lesson and before Sequence"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "physical_line_ranges": [
      [
        20,
        21
      ]
    ],
    "formula": null,
    "differences": [
      "Alleluja/Alleluia j/i; comma after Veni and capital Sancte are actual target pointing/case.",
      "Both books mark genuflection before verse; this is recorded as a rubric fact, excluded from candidate spoken Latin body."
    ],
    "restored": false
  },
  {
    "mass": "ash-wednesday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      22,
      "propers",
      15
    ],
    "lane": "pustet",
    "body": "Inclinantes se, Domine, majestati tuae, propitiatus intende: ut, qui\ndivino munere sunt refecti, caelestibus semper nutriantur auxiliis.\nPer Dominum.\n",
    "body_sha256": "15ced62446f8ebd36bbb422f30e61593d6cbb73377f425949bb846028299a577",
    "historical_body": "Inclinantes se, Domine, Majestati tuae, propitiatus intende: ut, qui divino munere sunt refecti, coelestibus semper nutriantur auxiliis. Per Dominum.",
    "historical_ending": "Per Dominum.",
    "target_ending": "Per Dominum.",
    "target_locus": "PDF 139 / printed 58; right bottom; unit 396; Oratio after Ash Wednesday Postcommunio395 and Humiliate capita cue",
    "historical_locus": "PDF 142 / printed 56; left; Oratio after Ash Wednesday Postcommunion complex and Humiliate capita cue, before FeriaQuinta",
    "target": {
      "pdf": [
        139
      ],
      "printed": "58",
      "unit": 396,
      "column": "right bottom",
      "heading": "Oratio after Ash Wednesday Postcommunio395 and Humiliate capita cue"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        142
      ],
      "printed": "56",
      "column": "left",
      "heading": "Oratio after Ash Wednesday Postcommunion complex and Humiliate capita cue, before FeriaQuinta"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-ash-wednesday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-ash-wednesday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-ash-wednesday-oratio-super-populum",
    "physical_line_ranges": [
      [
        23,
        25
      ]
    ],
    "formula": null,
    "differences": [
      "Majestati/maiestati capitalization and j/i; historical coelestibus / target caelestibus real received spelling."
    ],
    "restored": false
  },
  {
    "mass": "saturday-after-ash-wednesday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      25,
      "propers",
      9
    ],
    "lane": "pustet",
    "body": "Fideles tui, Deus, per tua dona firmentur: ut eadem et percipiendo\nrequirant, et quaerendo sine fine percipiant. Per Dominum.\n",
    "body_sha256": "8cf8402809c00ebb85b5900f9d3b16ec2af5f1628ee9edee60df71e4172d82d0",
    "historical_body": "Fideles tui, Deus, per tua dona firmentur: ut eadem et percipiendo requirant, et quaerendo sine fine percipiant. Per Dominum.",
    "historical_ending": "Per Dominum.",
    "target_ending": "Per Dominum.",
    "target_locus": "PDF 144 / printed 63; right; unit 427; Super populum Oratio before DominicaIinQuadragesima",
    "historical_locus": "PDF 146 / printed 60; right bottom; Super populum Oratio; final prayer of Saturday",
    "target": {
      "pdf": [
        144
      ],
      "printed": "63",
      "unit": 427,
      "column": "right",
      "heading": "Super populum Oratio before DominicaIinQuadragesima"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        146
      ],
      "printed": "60",
      "column": "right bottom",
      "heading": "Super populum Oratio; final prayer of Saturday"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "physical_line_ranges": [
      [
        27,
        28
      ]
    ],
    "formula": null,
    "differences": [],
    "restored": false
  },
  {
    "mass": "sacred-heart",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      97,
      "propers",
      1
    ],
    "lane": "schott",
    "body": "Deus, qui nobis, in Corde Filii tui, nostris vulnerato peccatis,\ninfinitos dilectionis thesauros misericorditer largiri dignaris:\nconcede, quaesumus; ut, illi devotum pietatis nostrae praestantes\nobsequium, dignae quoque satisfactionis exhibeamus officium. Per\neundem Dominum.\n",
    "body_sha256": "c7d00a4a72b472208ac1bc38e4479eb3c80e286b498734de8c024f8f3e4ce59d",
    "historical_body": "Deus, qui nobis, in Corde Filii tui, nostris vulnerato peccatis, infinitos dilectionis thesauros misericorditer largiri dignaris; concede, quaesumus, ut illi devotum pietatis nostrae praestantes obsequium, dignae quoque satisfactionis exhibeamus officium. Per eundem Dominum.",
    "historical_ending": "Per eundem Dominum.",
    "target_ending": "Per eundem Dominum.",
    "target_locus": "PDF 460 / printed 379 (opening folio suppressed); left; unit 1453; Oratio; In festo Sacratissimi Cordis Iesu; Friday after second Sunday after Pentecost",
    "historical_locus": "PDF 1483 / printed [269]; left; Oratio; Fest des allerheiligsten Herzens Jesu",
    "target": {
      "pdf": [
        460
      ],
      "printed": "379 (opening folio suppressed)",
      "unit": 1453,
      "column": "left",
      "heading": "Oratio; In festo Sacratissimi Cordis Iesu; Friday after second Sunday after Pentecost"
    },
    "historical": {
      "witness": "schott",
      "pdf": [
        1483
      ],
      "printed": "[269]",
      "column": "left",
      "heading": "Oratio; Fest des allerheiligsten Herzens Jesu"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-sacred-heart-collect",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-sacred-heart-collect",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-sacred-heart-collect",
    "physical_line_ranges": [
      [
        1,
        5
      ]
    ],
    "formula": null,
    "differences": [
      "Pointing: historical dignaris; concede, quaesumus, ut illi / target dignaris: concede, quaesumus; ut, illi."
    ],
    "restored": false,
    "historical_line_ranges": [
      [
        1,
        1
      ]
    ]
  },
  {
    "mass": "s-teresiae-a-iesu-infante-virginis",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      9
    ],
    "lane": "schott",
    "body": "Illo nos, Domine, amoris igne caeleste mysterium inflammet: quo sancta\nTeresia Virgo tua se tibi pro hominibus caritatis victimam devovit.\nPer Dominum nostrum.\n",
    "body_sha256": "bd156cf03db2181218acba1a033684509dd2867ea60aeedcd169291c1f9e7e15",
    "historical_body": "Illo nos, Domine, amoris igne caeleste mysterium inflammet: quo sancta Teresia Virgo tua se tibi pro hominibus caritatis victimam devovit. Per Dominum nostrum.",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum nostrum.",
    "target_locus": "PDF 756 / printed 675; right top; unit 3768; Postcommunio; before October4 heading",
    "historical_locus": "PDF 1482 / printed [268]; left; Postcommunio",
    "target": {
      "pdf": [
        756
      ],
      "printed": "675",
      "unit": 3768,
      "column": "right top",
      "heading": "Postcommunio; before October4 heading"
    },
    "historical": {
      "witness": "schott",
      "pdf": [
        1482
      ],
      "printed": "[268]",
      "column": "left",
      "heading": "Postcommunio"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "physical_line_ranges": [
      [
        7,
        9
      ]
    ],
    "formula": null,
    "differences": [],
    "restored": false,
    "historical_line_ranges": [
      [
        3,
        3
      ]
    ]
  },
  {
    "mass": "s-teresiae-a-iesu-infante-virginis",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      7
    ],
    "lane": "schott",
    "body": "Sacrificium nostrum tibi, Domine, quaesumus, sanctae Teresiae Virginis\ntuae precatio sancta conciliet: ut, in cujus honore solemniter\nexhibetur, ejus meritis efficiatur acceptum. Per Dominum nostrum.\n",
    "body_sha256": "44ae620a19de8395079129c2c441a1d94df62b63057d618cf37682b000ee32f1",
    "historical_body": "Sacrificium nostrum tibi, Domine, quaesumus, sanctae Teresiae Virginis tuae precatio sancta conciliet: ut in cujus honore solemniter exhibetur ejus meritis efficiatur acceptum. Per Dominum nostrum.",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum nostrum.",
    "target_locus": "PDF 756 / printed 675; left bottom; unit 3766; Secreta; Therese formulary continues",
    "historical_locus": "PDF 1482 / printed [268]; left; Secreta",
    "target": {
      "pdf": [
        756
      ],
      "printed": "675",
      "unit": 3766,
      "column": "left bottom",
      "heading": "Secreta; Therese formulary continues"
    },
    "historical": {
      "witness": "schott",
      "pdf": [
        1482
      ],
      "printed": "[268]",
      "column": "left",
      "heading": "Secreta"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "physical_line_ranges": [
      [
        11,
        13
      ]
    ],
    "formula": null,
    "differences": [
      "cujus/cuius and ejus/eius declared j/i orthography.",
      "Historical Schott PDF1482/[268] and target1962 PDF756/p675/unit3766 both print solemniter (one l); retained without spelling normalization.",
      "Target commas after ut and exhibetur are explicitly projected."
    ],
    "restored": false,
    "historical_line_ranges": [
      [
        5,
        5
      ]
    ]
  },
  {
    "mass": "lent-1-thursday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      30,
      "propers",
      9
    ],
    "lane": "pustet",
    "body": "Da, quaesumus, Domine, populis christianis: et, quae profitentur,\nagnoscere, et caeleste munus diligere, quod frequentant. Per Dominum.\n",
    "body_sha256": "804b104f1f85757f51eddf555e651d41ab772bc9faf2ec636f436e400174548a",
    "historical_body": "Da, quaesumus Domine, populis christianis, et quae profitentur, agnoscere: et coeleste munus diligere, quod frequentant. Per Dominum nostrum.",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum.",
    "target_locus": "PDF 152 / printed 71; right top; unit 481; Super populum Oratio before FeriaSexta Quatuor Temporum",
    "historical_locus": "PDF 155 / printed 69; left bottom; Super populum Oratio before FeriaSexta in right column",
    "target": {
      "pdf": [
        152
      ],
      "printed": "71",
      "unit": 481,
      "column": "right top",
      "heading": "Super populum Oratio before FeriaSexta Quatuor Temporum"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        155
      ],
      "printed": "69",
      "column": "left bottom",
      "heading": "Super populum Oratio before FeriaSexta in right column"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "physical_line_ranges": [
      [
        30,
        31
      ]
    ],
    "formula": null,
    "differences": [
      "Historical coeleste / target caeleste is a real received spelling.",
      "Target pointing around Domine, christianis, et quae and agnoscere is explicitly projected.",
      "Target omits terminal nostrum from the historical conclusion; deletion only, no new words or assembled conclusion."
    ],
    "restored": false
  },
  {
    "mass": "sacred-heart",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      97,
      "propers",
      7
    ],
    "lane": "schott",
    "body": "Respice, quaesumus, Domine, ad ineffabilem Cordis dilecti Filii tui\ncaritatem: ut quod offerimus sit tibi munus acceptum et nostrorum\nexpiatio delictorum. Per eundem Dominum.\n",
    "body_sha256": "44ed87c1a9536993d8371d13e421744097960aa62da90162f1f78d3da287dc98",
    "historical_body": "Respice, quaesumus, Domine, ad ineffabilem Cordis dilecti Filii tui caritatem: ut quod offerimus sit tibi munus acceptum et nostrorum expiatio delictorum. Per eundem Dominum nostrum.",
    "historical_ending": "Per eundem Dominum nostrum.",
    "target_ending": "Per eundem Dominum.",
    "target_locus": "PDF 461 / printed 380; right; unit 1459; Secreta; same Sacred Heart formulary continues above following Sunday",
    "historical_locus": "PDF 1486 / printed [272]; left; Secreta",
    "target": {
      "pdf": [
        461
      ],
      "printed": "380",
      "unit": 1459,
      "column": "right",
      "heading": "Secreta; same Sacred Heart formulary continues above following Sunday"
    },
    "historical": {
      "witness": "schott",
      "pdf": [
        1486
      ],
      "printed": "[272]",
      "column": "left",
      "heading": "Secreta"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-sacred-heart-secret",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-sacred-heart-secret",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-sacred-heart-secret",
    "physical_line_ranges": [
      [
        15,
        17
      ]
    ],
    "formula": null,
    "differences": [
      "Exact whole petition is unchanged. Target shortens the historical conclusion by omitting terminal nostrum; explicit deletion, no addition or assembled conclusion."
    ],
    "restored": false,
    "historical_line_ranges": [
      [
        7,
        7
      ]
    ]
  },
  {
    "mass": "thursday-after-ash-wednesday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      23,
      "propers",
      9
    ],
    "lane": "pustet",
    "body": "Parce, Domine, parce populo tuo: ut, dignis flagellationibus\ncastigatus, in tua miseratione respiret. Per Dominum nostrum.\n",
    "body_sha256": "96fa3323adf06aa40efee765bada25fdee952b141f7964a0b946be17d042d74b",
    "historical_body": "Parce, Domine, parce populo tuo, ut dignis flagellationibus castigatus, in tua miseratione respiret. Per Dominum.",
    "historical_ending": "Per Dominum.",
    "target_ending": "Per Dominum nostrum.",
    "target_locus": "PDF 141 / printed 60; left bottom before FeriaSexta; unit 406",
    "historical_locus": "PDF 143 / printed 57; right; Super populum Oratio before FeriaSexta",
    "target": {
      "pdf": 141,
      "printed": "60",
      "unit": 406,
      "column": "left bottom before FeriaSexta"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        143
      ],
      "printed": "57",
      "column": "right",
      "heading": "Super populum Oratio before FeriaSexta"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "physical_line_ranges": [
      [
        33,
        34
      ]
    ],
    "formula": "father-through-son",
    "differences": [
      "Only standard conclusion length changes: historical Per Dominum. to actual target Per Dominum nostrum.; nostrum is witnessed in one complete old standard formula, not borrowed from another petition.",
      "Target colon after tuo and comma after ut are pointing, not a petition variant."
    ],
    "restored": false,
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "mass": "friday-after-ash-wednesday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      24,
      "propers",
      10
    ],
    "lane": "pustet",
    "body": "Tuere, Domine, populum tuum, et ab omnibus peccatis clementer emunda:\nquia nulla ei nocebit adversitas, si nulla ei dominetur iniquitas. Per\nDominum nostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat\nin unitate.\n",
    "body_sha256": "fde9e9ecb8760757adafae9aaece1cb2809a1b845f64df6c6376b21bf576a074",
    "historical_body": "Tuere, Domine, populum tuum, et ab omnibus peccatis clementer emunda: quia nulla ei nocebit adversitas, si nulla ei dominetur iniquitas. Per Dominum nostrum.",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "target_locus": "PDF 143 / printed 62; left top before Sabbato; unit 417",
    "historical_locus": "PDF 145 / printed 59; left bottom; Super populum Oratio before Saturday block in right column",
    "target": {
      "pdf": 143,
      "printed": "62",
      "unit": 417,
      "column": "left top before Sabbato"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        145
      ],
      "printed": "59",
      "column": "left bottom",
      "heading": "Super populum Oratio before Saturday block in right column"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "physical_line_ranges": [
      [
        36,
        39
      ]
    ],
    "formula": "father-through-son",
    "differences": [
      "Standard Father-through-Son conclusion expands only to the target's actually printed in unitate.; it stops there.",
      "Historical formula Jesum to target Iesum is declared j/i spelling; target comma after Christum is pointing.",
      "Exemplar words ejusdem Spiritus sancti Deus are beyond the printed target stop and are NOT copied or supplied."
    ],
    "restored": false,
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "mass": "lent-1-monday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      27,
      "propers",
      10
    ],
    "lane": "pustet",
    "body": "Absolve, quaesumus, Domine, nostrorum vincula peccatorum: et, quidquid\npro eis meremur, propitiatus averte. Per Dominum nostrum Jesum\nChristum, Filium tuum: Qui tecum vivit et regnat in unitate.\n",
    "body_sha256": "d3ccb3ddbe69bf7e9c146fb21f63fc621019632045966faa0715e694116bb1a0",
    "historical_body": "Absolve, quaesumus Domine, nostrorum vincula peccatorum: et quidquid pro eis meremur, propitiatus averte. Per Dominum.",
    "historical_ending": "Per Dominum.",
    "target_ending": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "target_locus": "PDF 147 / printed 66; right bottom, complete final prayer on same page; unit 448",
    "historical_locus": "PDF 150 / printed 64; left bottom continues at right top of SAME page; Super populum Oratio before FeriaTertia heading",
    "target": {
      "pdf": 147,
      "printed": "66",
      "unit": 448,
      "column": "right bottom, complete final prayer on same page"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        150
      ],
      "printed": "64",
      "column": "left bottom continues at right top of SAME page",
      "heading": "Super populum Oratio before FeriaTertia heading"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-monday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-monday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-monday-oratio-super-populum",
    "physical_line_ranges": [
      [
        41,
        43
      ]
    ],
    "formula": "father-through-son",
    "differences": [
      "Only the same-class standard conclusion expands; actual target stop is in unitate.",
      "Historical prayer pointing around quaesumus Domine and et quidquid is normalized to the freshly read target; no petition words change.",
      "Formula Jesum/Iesum is j/i; comma after Christum is pointing. No ejusdem Spiritus sancti Deus, per omnia or Amen supplied."
    ],
    "restored": false,
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "mass": "lent-1-ember-wednesday",
    "form": "",
    "proper": "Oratio",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      29,
      "propers",
      4
    ],
    "lane": "pustet",
    "body": "Devotionem populi tui, quaesumus, Domine, benignus intende: ut, qui\nper abstinentiam macerantur in corpore, per fructum boni operis\nreficiantur in mente. Per Dominum nostrum Jesum Christum, Filium tuum:\nQui tecum vivit et regnat in unitate.\n",
    "body_sha256": "49ca63839813f8f0be869fe588411b9e7801d2b869b5cd3ff41b4232003f817c",
    "historical_body": "Devotionem populi tui, quaesumus Domine, benignus intende: ut, qui per abstinentiam macerantur in corpore, per fructum boni operis reficiantur in mente. Per Dominum nostrum.",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "target_locus": "PDF 149 / printed 68; right bottom, after first Gradual462; unit 463",
    "historical_locus": "PDF 152 / printed 66; right; Oremus Oratio after first Gradual, before second Lesson; Hic non dicitur Flectamus cue",
    "target": {
      "pdf": 149,
      "printed": "68",
      "unit": 463,
      "column": "right bottom, after first Gradual462"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        152
      ],
      "printed": "66",
      "column": "right",
      "heading": "Oremus Oratio after first Gradual, before second Lesson; Hic non dicitur Flectamus cue"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-ember-wednesday-oratio",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-ember-wednesday-oratio",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-ember-wednesday-oratio",
    "physical_line_ranges": [
      [
        45,
        48
      ]
    ],
    "formula": "father-through-son",
    "differences": [
      "Role is the local unformed Oratio, raw occurrence1, the second physical oration after first Gradual462; NOT opening Collect Preces nostras460 and NOT Oratio super populum Mentes nostras471.",
      "Only the same-class standard conclusion expands; actual stop in unitate is preserved.",
      "Commas around quaesumus Domine follow target pointing; formula Jesum/Iesum is j/i. No further conclusion suffix added."
    ],
    "restored": false,
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "mass": "lent-1-ember-wednesday",
    "form": "",
    "proper": "Oratio super populum",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "seasonal",
      "masses",
      29,
      "propers",
      12
    ],
    "lane": "pustet",
    "body": "Mentes nostras, quaesumus, Domine, lumine tuae claritatis illustra: ut\nvidere possimus, quae agenda sunt; et, quae recta sunt, agere\nvaleamus. Per Dominum nostrum.\n",
    "body_sha256": "6607863842ea49d0be968e7d46bdfb007173bdd1d545e7547a61e99504cc1670",
    "historical_body": "Mentes nostras, quaesumus Domine, lumine tuae claritatis illustra: ut videre possimus, quae agenda sunt: et quae recta sunt, agere valeamus. Per Dominum.",
    "historical_ending": "Per Dominum.",
    "target_ending": "Per Dominum nostrum.",
    "target_locus": "PDF 151 / printed 70; left before Feriaquinta; unit 471",
    "historical_locus": "PDF 154 / printed 68; left top; Final Wednesday Oratio, before FeriaQuinta heading",
    "target": {
      "pdf": 151,
      "printed": "70",
      "unit": 471,
      "column": "left before Feriaquinta"
    },
    "historical": {
      "witness": "pustet",
      "pdf": [
        154
      ],
      "printed": "68",
      "column": "left top",
      "heading": "Final Wednesday Oratio, before FeriaQuinta heading"
    },
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "physical_line_ranges": [
      [
        50,
        52
      ]
    ],
    "formula": "father-through-son",
    "differences": [
      "Only same-class standard conclusion adds nostrum, witnessed contiguously in the old formula.",
      "Target commas around quaesumus Domine, semicolon after sunt and comma after et are pointing; petition/address unchanged."
    ],
    "restored": false,
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "mass": "s-teresiae-a-iesu-infante-virginis",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      1
    ],
    "lane": "schott",
    "body": "Domine, qui dixisti: Nisi efficiamini sicut parvuli, non intrabitis in\nregnum caelorum: da nobis, quaesumus; ita sanctae Teresiae Virginis in\nhumilitate et simplicitate cordis vestigia sectari, ut praemia\nconsequamur aeterna: Qui vivis et regnas cum Deo Patre in unitate.\n",
    "body_sha256": "af5711fcc13cd77c33978d3406ffa1cb0295a737023cbb6ca95c31531e62c66f",
    "historical_body": "Domine, qui dixisti: Nisi efficiamini sicut parvuli, non intrabitis in regnum caelorum: da nobis, quaesumus; ita sanctae Teresiae Virginis in humilitate et simplicitate cordis vestigia sectari, ut praemia consequamur aeterna: Qui vivis.",
    "historical_ending": "Qui vivis.",
    "target_ending": "Qui vivis et regnas cum Deo Patre in unitate.",
    "target_locus": "PDF 755 / printed 674; left bottom under Die3octobris; unit 3758",
    "historical_locus": "PDF 1480 / printed [266]; left; Oratio; Die hl.Theresia vom Kinde Jesu, Jungfrau; 3.Okt.",
    "target": {
      "pdf": 755,
      "printed": "674",
      "unit": 3758,
      "column": "left bottom under Die3octobris"
    },
    "historical": {
      "witness": "schott",
      "pdf": [
        1480
      ],
      "printed": "[266]",
      "column": "left",
      "heading": "Oratio; Die hl.Theresia vom Kinde Jesu, Jungfrau; 3.Okt."
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "physical_line_ranges": [
      [
        19,
        22
      ]
    ],
    "formula": "son-addressed",
    "differences": [
      "The Son-directed Qui vivis family stays Son-directed; no Per Dominum to Qui vivis addressee substitution.",
      "Actual target prints only through in unitate.; it does NOT print Spiritus Sancti, Deus, per omnia or Amen.",
      "Formula exemplar comma after Patre is absent in target: pointing only. Whole petition word identity is retained; accents, ligatures and physical wraps normalized.",
      "Fresh actual unit number is3758, not the prior research receipt's3761.3761 is the right-column Alleluia. Prior files remain unchanged."
    ],
    "restored": false,
    "historical_line_ranges": [
      [
        9,
        9
      ]
    ],
    "formula_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-son-addressed"
  },
  {
    "mass": "s-ioannis-a-cruce-confessoris-ecclesiae",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "sanctoral",
      "masses",
      283,
      "propers",
      0
    ],
    "lane": "schott",
    "body": "Deus, qui sanctum Joannem Confessorem tuum atque Doctorem perfectae\nsui abnegationis et Crucis amatorem eximium effecisti: concede; ut,\nejus imitationi jugiter inhaerentes, gloriam assequamur aeternam. Per\nDominum nostrum.\n",
    "body_sha256": "6434b8c24e32369497ab4c99386ebb42cc16322972a2af680a2d735f315779bb",
    "historical_body": "Deus qui sanctum Joannem Confessorem tuum atque Doctorem perfectae sui abnegationis et Crucis amatorem eximium effecisti concede ut ejus imitationi jugiter inhaerentes gloriam assequamur aeternam Per Dominum nostrum",
    "historical_ending": "Per Dominum nostrum.",
    "target_ending": "Per Dominum nostrum.",
    "target_locus": "PDF 806 / printed 725; right bottom; unit 4160 P",
    "historical_locus": "PDF 1208 / printed 1138; left; 24.Nov. Der hl.Johannes vom Kreuz, Bekenner und Kirchenlehrer; Oratio",
    "target": {
      "pdf": 806,
      "printed": "725",
      "unit": "4160 P",
      "column": "right bottom",
      "date": "11-24"
    },
    "historical": {
      "pdf": 1208,
      "printed": "1138",
      "column": "left",
      "heading": "24.Nov. Der hl.Johannes vom Kreuz, Bekenner und Kirchenlehrer; Oratio"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "physical_line_ranges": [
      [
        24,
        27
      ]
    ],
    "formula": null,
    "differences": [
      "line-end hyphenation, stress, ligatures, case and pointing",
      "Joannem/Ioannem, ejus/eius, jugiter/iugiter are declared j/i orthography"
    ],
    "restored": true,
    "historical_line_ranges": [
      [
        11,
        11
      ]
    ]
  },
  {
    "mass": "s-ioannis-mariae-vianney-confessoris",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "path": [
      "sections",
      "sanctoral",
      "masses",
      178,
      "propers",
      0
    ],
    "lane": "schott",
    "body": "Omnipotens et misericors Deus, qui sanctum Joannem Mariam pastorali\nstudio et jugi orationis ac paenitentiae ardore mirabilem effecisti:\nda, quaesumus; ut, ejus exemplo et intercessione, animas fratrum\nlucrari Christo, et cum eis aeternam gloriam consequi valeamus. Per\neundem Dominum.\n",
    "body_sha256": "12105ba3649c6e5b37c48e65fd93475d55706432eb8485f495625e32b20ddcb4",
    "historical_body": "Omnipotens et misericors Deus qui sanctum Joannem Mariam pastorali studio et jugi orationis ac poenitentiae ardore mirabilem effecisti da quaesumus ut ejus exemplo et intercessione animas fratrum lucrari Christo et cum eis aeternam gloriam consequi valeamus Per eundem Dominum",
    "historical_ending": "Per eundem Dominum.",
    "target_ending": "Per eundem Dominum.",
    "target_locus": "PDF 699 / printed 618; left; unit 3305 P",
    "historical_locus": "PDF 1479 / printed [265] (opening numeral suppressed; integral contents confirms); left; Neueste vorgeschriebene Feste; 9.Aug. Der hl.Johannes Maria Vianney; Oratio",
    "target": {
      "pdf": 699,
      "printed": "618",
      "unit": "3305 P",
      "column": "left",
      "date": "08-08"
    },
    "historical": {
      "pdf": 1479,
      "printed": "[265] (opening numeral suppressed; integral contents confirms)",
      "column": "left",
      "heading": "Neueste vorgeschriebene Feste; 9.Aug. Der hl.Johannes Maria Vianney; Oratio"
    },
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "physical_line_ranges": [
      [
        29,
        33
      ]
    ],
    "formula": null,
    "differences": [
      "line-end hyphenation, stress, ligatures, case and pointing",
      "Joannem/Ioannem, jugi/iugi, ejus/eius",
      "historical poenitentiae / target paenitentiae is a real received spelling, not a changed saint title or OCR noise"
    ],
    "restored": true,
    "historical_line_ranges": [
      [
        13,
        13
      ]
    ]
  }
]''')

LANES = json.loads(r'''{
  "pustet": {
    "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
    "path": "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-pustet-projection-20261022/latin.txt",
    "sha256": "f6993617fed59176e4e527f4c47c853b3e80b01f3e4fd61dfc41e68c8ef7661d",
    "historical_artifact_id": "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
    "historical_sha256": "5d088d757984a53622d0b3cd763390204986df08e867241ad546bbee891283e1"
  },
  "schott": {
    "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
    "path": "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-schott-projection-20261022/latin.txt",
    "sha256": "dab1c4edc0d73c87a91406deb5c6e2178f8bd6ace6b505932ff7b615f47431d4",
    "historical_artifact_id": "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022",
    "historical_sha256": "ba9e819046bfea45167b7ba99f4fbd9b0fc8d0e69cc70adc9a6113dd59febc34"
  }
}''')

AUTHORITY = json.loads(r'''[
  {
    "slug": "rubricae-generales-17",
    "pdf": 44,
    "printed": "38",
    "column": "right, paragraph17",
    "heading": "Rubricae generales Missalis; conclusions of orations",
    "body": "In conclusione Orationum hic modus servatur. Si Oratio dirigatur ad Patrem, concluditur Per Dominum nostrum etc. Si ad Filium, Qui vivis et regnas cum Deo Patre etc. Si in principio Orationis fiat mentio Filii, concluditur Per eumdem Dominum nostrum etc. Si in fine Orationis ejus fiat mentio, Qui tecum vivit etc. Si facta sit mentio Spiritus sancti, in conclusione dicitur: In unitate ejusdem Spiritus sancti etc. Alia quoque in dicendis Orationibus serventur, quae superius in Rubrica de Commemorationibus dicta sunt.\n",
    "physical_line_ranges": [
      [
        1,
        1
      ]
    ],
    "passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-rubricae-generales-17"
  },
  {
    "slug": "ritus-celebrandi-v-1",
    "pdf": 55,
    "printed": "49",
    "column": "right, continuation of V.De Oratione1",
    "heading": "Ritus celebrandi Missam, V.De Oratione1",
    "body": "Cum dicit: Per Dominum nostrum, jungit manus, easque junctas tenet usque ad finem. Si aliter concluditur Oratio, Qui tecum, vel Qui vivis, cum dicit: in unitate, jungit manus.\n",
    "physical_line_ranges": [
      [
        3,
        3
      ]
    ],
    "passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-ritus-celebrandi-v-1"
  },
  {
    "slug": "father-through-son",
    "pdf": 390,
    "printed": "304",
    "column": "right top, second Oratio after Gloria cue",
    "heading": "Feria IV.Quatuor Temporum Pentecostes; Praesta",
    "body": "Praesta, quaesumus omnipotens et misericors Deus: ut Spiritus sanctus adveniens, templum nos gloriae suae dignanter inhabitando perficiat. Per Dominum nostrum Jesum Christum Filium tuum: Qui tecum vivit et regnat in unitate ejusdem Spiritus sancti Deus.\n",
    "physical_line_ranges": [
      [
        5,
        5
      ]
    ],
    "passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-father-through-son"
  },
  {
    "slug": "son-addressed",
    "pdf": 532,
    "printed": "446",
    "column": "left, May17 Collect",
    "heading": "S.Paschalis Baylon, Confessoris; Deus qui beatum Paschalem",
    "body": "Deus, qui beatum Paschalem Confessorem tuum, mirifica erga Corporis et Sanguinis tui sacra mysteria dilectione decorasti: concede propitius; ut, quam ille ex hoc divino convivio spiritus percepit pinguedinem; eamdem et nos percipere mereamur. Qui vivis et regnas cum Deo Patre, in unitate Spiritus sancti Deus etc.\n",
    "physical_line_ranges": [
      [
        7,
        7
      ]
    ],
    "passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-son-addressed"
  }
]''')

AUTHORITY_ARTIFACT = json.loads(r'''"artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"''')

TARGET = json.loads(r'''"artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"''')

TARGET_HASH = json.loads(r'''"648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"''')

PUSTET_PAGES = json.loads(r'''[
  44,
  55,
  92,
  106,
  142,
  143,
  145,
  146,
  150,
  152,
  154,
  155,
  358,
  362,
  390,
  391,
  532,
  674,
  685
]''')

UNOWNED_YAML_SHA256 = json.loads(r'''"78303c7aff9a8d17a6f7474bb46130d0933386a16a4af0f2bde900240aa2d272"''')

UNOWNED_LEDGER_SHA256 = json.loads(r'''"1b56e6ba354782f008de8d30f6bd684eaeb6ca14424c97ea12d34ead24db2439"''')

PRIOR_PRESENT_SHA256 = json.loads(r'''"c75742cc1e33d59178b2b9de24c53ad7e53bed25f8a78dd6a4eb13482e32d0c0"''')

WRAPPERS = json.loads(r'''[
  {
    "name": "Alleluia",
    "incipit": "Te Martyrum candidatus",
    "source": "composed",
    "ordinary_disposition": {
      "kind": "alternative",
      "group": "plurimorum-martyrum-3-post-epistle",
      "option": "regular",
      "basis": "1962 Common opening, artifact p.809/[1], plus 1962 CMAA facsimile, artifact p. 820, printed [12]; raw text page line 67 and the numbered local chant cues",
      "anchor": {
        "mass": "commune-plurimorum-martyrum-3",
        "form_id": "main",
        "proper": "Alleluia",
        "occurrence": 1
      },
      "when": {
        "fact": "roman-1962-common-chant-regime",
        "in": [
          "advent",
          "regular"
        ]
      }
    }
  },
  {
    "name": "Alleluia",
    "source": "composed"
  },
  {
    "name": "Alleluia",
    "incipit": "Hic est sacerdos",
    "source": "composed",
    "ordinary_disposition": {
      "kind": "alternative",
      "group": "unius-martyris-2-post-epistle",
      "option": "regular",
      "basis": "1962 Common opening, artifact p.809/[1], plus 1962 CMAA facsimile, artifact p. 813, printed [5]; raw text page line 42 and the numbered local chant cues",
      "anchor": {
        "mass": "commune-unius-martyris-2",
        "form_id": "main",
        "proper": "Alleluia",
        "occurrence": 1
      },
      "when": {
        "fact": "roman-1962-common-chant-regime",
        "in": [
          "advent",
          "regular"
        ]
      }
    }
  },
  {
    "name": "Alleluia",
    "ordinary_disposition": {
      "kind": "conditional",
      "group": "advent-3-alleluia-use",
      "basis": "Missale Romanum 1962 CMAA facsimile, artifact p. 86, printed p. 5, L column, between Gradual24 and Alleluia25: on Advent ferias using this Sunday Mass only the Gradual remains; omit the Alleluia and its following verse. No other Proper is changed.",
      "when": {
        "fact": "roman-1962-advent-sunday-alleluia-use",
        "in": [
          "chant-present"
        ]
      }
    },
    "incipit": "Excita, Domine, potentiam tuam",
    "source": "composed"
  },
  {
    "name": "Alleluia",
    "incipit": "Surrexit Dominus de sepulcro",
    "source": "composed"
  },
  {
    "name": "Alleluia",
    "incipit": "Surrexit Christus, qui creavit",
    "source": "composed"
  },
  {
    "name": "Second Alleluia",
    "incipit": "Veni, Sancte Spiritus",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Inclinantes se Domine",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Fideles tui Deus",
    "source": "composed"
  },
  {
    "name": "Collect",
    "source": "composed"
  },
  {
    "name": "Postcommunion",
    "source": "composed"
  },
  {
    "name": "Secret",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Da quaesumus Domine",
    "source": "composed"
  },
  {
    "name": "Secret",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Parce Domine parce",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Tuere Domine",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Absolve quaesumus",
    "source": "composed"
  },
  {
    "name": "Oratio",
    "incipit": "Devotionem populi",
    "source": "composed"
  },
  {
    "name": "Oratio super populum",
    "incipit": "Mentes nostras",
    "source": "composed"
  },
  {
    "name": "Collect",
    "source": "composed"
  },
  {
    "name": "Collect",
    "source": "composed"
  },
  {
    "name": "Collect",
    "incipit": "Omnipotens et misericors Deus",
    "source": "composed"
  }
]''')

REMAINING_REMOVED = json.loads(r'''[
  {
    "mass": "comm-s-silvestri-i-papae-confessoris",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "3b272cbc2235d117f16ba9a76b02d0e1a36f9f26e450bf3cbf90fcb0c61dae88",
    "body_status": "removed"
  },
  {
    "mass": "easter-vigil",
    "form": "",
    "proper": "Blessing of the Lighted Candle",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "60b503ba9006dcb3f74b49fa7cf3cdebaaacbea23d68e829ef59b4e99f7209c4",
    "body_status": "removed"
  },
  {
    "mass": "easter-vigil",
    "form": "",
    "proper": "Blessing of the Paschal Candle",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "186eadda4a345e8fdb790b8030f75bac32509c8be472dc43541d33f1c135e9ba",
    "body_status": "removed"
  },
  {
    "mass": "easter-vigil",
    "form": "",
    "proper": "Renewal of Baptismal Promises",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "54cef0a77744ee788fb0d13989d114ae0fd94558f35c412b5ccf95cd682be2fc",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Antiphons at the Translation of the Blessed Sacrament",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "cf6998f6e26d8ed9b51fc9226fd6d7d880c3cb2cfba14b17c8e8c760264c9fba",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "First Prayer after Communion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "667bd7ff547b9d972a1e4af9b0b897a18d3e47f467ff20f78f1bbefa9aed9e89",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Improperia",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "dc76fa149743742f7d0ce72e5ee61e94ce3a7c322f470d8436cef0b9862ea08e",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Prayer after the Prostration",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "0ff9b8c02fcb280f7d1a6ed99e8dfd234bcda4a7d7cadc7cdd35b21ba70cdf14",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Second Prayer after Communion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "7ab95f45879ac285f085f5fa2ceddd3a6e1965ecff0484b02afdd1e152af3f35",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Solemn Intercessions",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "fed2c1a100ca75e899e1adde61a110e07f7ae8c2e64b7a49199308ca1d2c84fa",
    "body_status": "removed"
  },
  {
    "mass": "good-friday",
    "form": "",
    "proper": "Third Prayer after Communion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "cdac027526824556b6499a48e39f8134d95f53808e8515be314f0ffa6f077139",
    "body_status": "removed"
  },
  {
    "mass": "palm-sunday",
    "form": "",
    "proper": "Blessing of the Palms",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "682fe28904c60a97cf5ff20ccb54745aa05e98d3b7fdd3ccf8aa40e5e3863eac",
    "body_status": "removed"
  },
  {
    "mass": "palm-sunday",
    "form": "",
    "proper": "Oration to Conclude the Procession",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "0559fa07fc696853dbe02769d4202de6293451c6f82b0d64513834f79e1be709",
    "body_status": "removed"
  },
  {
    "mass": "palm-sunday",
    "form": "",
    "proper": "Procession Antiphon",
    "course": "",
    "cycle": "",
    "occurrence": 4,
    "text_sha256": "9bcc969b821433d7056fc209fdef0b9e102b6630faf703742a73dfca92411294",
    "body_status": "removed"
  },
  {
    "mass": "palm-sunday",
    "form": "",
    "proper": "Procession Antiphon",
    "course": "",
    "cycle": "",
    "occurrence": 5,
    "text_sha256": "3f45a777373ace21cbeceee20f8bf20a2a6254830ed583dd71449b46959529d2",
    "body_status": "removed"
  },
  {
    "mass": "palm-sunday",
    "form": "",
    "proper": "Procession Antiphon",
    "course": "",
    "cycle": "",
    "occurrence": 6,
    "text_sha256": "a688650a13dc6845e131d135eca3a536ea9b34b6eee1077a39999331225bf49d",
    "body_status": "removed"
  },
  {
    "mass": "s-alberti-magni-episcopi-confessoris-ecclesiae",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "3a194e4c84c13ba8d47374e8001ad4f0b761b7e19582178f08cb97310020f03f",
    "body_status": "removed",
    "provenance_status": "collated",
    "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf",
    "source_date": "1962",
    "locator": "printed p. 719; digital p. 800; appointment and current-slot control",
    "relationship": "collated-exact",
    "verification_source_id": "passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.albert-the-great-collect",
    "verification_locator": "artifact p. 1290; printed p. 1289; IA leaf n1289",
    "transformations": [
      "join printed line wraps",
      "strip printed stress accents",
      "expand printed ae/oe ligatures to ae/oe",
      "normalize incidental spacing",
      "retain witness j orthography",
      "select the witness's abbreviated conclusion rather than the longer controlling-edition conclusion"
    ],
    "provenance_evidence": "src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/albert-the-great-collect.toml; visually collated 2026-08-26",
    "provenance_authority": "1962 typica for appointment; registered Lasance page-image passage for the exact bounded wording",
    "provenance_confidence": "high",
    "publication_status": "withheld",
    "publication_basis": "unresolved",
    "surfaces": [],
    "note": "HOLD on corpus-data, public-git, web, download, print, and cli: exactness needs orthographic and spacing transformations beyond the approved line-wrap-only publication gate; no 1962-only expansion is published."
  },
  {
    "mass": "s-alberti-magni-episcopi-confessoris-ecclesiae",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "bce37e2d47a948576c33735055ce0ce47199729c379795a2c056c289cf7a9601",
    "body_status": "removed",
    "provenance_status": "collated",
    "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf",
    "source_date": "1962",
    "locator": "printed p. 719; digital p. 800; appointment and current-slot control",
    "relationship": "collated-exact",
    "verification_source_id": "passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.albert-the-great-postcommunion",
    "verification_locator": "artifact p. 1291; printed p. 1290; IA leaf n1290",
    "transformations": [
      "join printed line wraps",
      "strip printed stress accents",
      "expand printed ae/oe ligatures to ae/oe",
      "normalize incidental spacing",
      "retain witness j orthography"
    ],
    "provenance_evidence": "src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/albert-the-great-postcommunion.toml; visually collated 2026-08-26",
    "provenance_authority": "1962 typica for appointment; registered Lasance page-image passage for the exact bounded wording",
    "provenance_confidence": "high",
    "publication_status": "withheld",
    "publication_basis": "unresolved",
    "surfaces": [],
    "note": "HOLD on corpus-data, public-git, web, download, print, and cli: exactness needs orthographic and spacing transformations beyond the approved line-wrap-only publication gate."
  },
  {
    "mass": "s-alberti-magni-episcopi-confessoris-ecclesiae",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "8337420edbcf5267c78e618ab26c6d06a966e352f9b488ba3a7085533ab1538a",
    "body_status": "removed",
    "provenance_status": "collated",
    "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf",
    "source_date": "1962",
    "locator": "printed p. 719; digital p. 800; appointment and current-slot control",
    "relationship": "collated-exact",
    "verification_source_id": "passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.albert-the-great-secret",
    "verification_locator": "artifact p. 1291; printed p. 1290; IA leaf n1290",
    "transformations": [
      "join printed line wraps",
      "strip printed stress accents",
      "expand printed ae/oe ligatures to ae/oe",
      "normalize incidental spacing",
      "retain witness j orthography"
    ],
    "provenance_evidence": "src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/albert-the-great-secret.toml; visually collated 2026-08-26",
    "provenance_authority": "1962 typica for appointment; registered Lasance page-image passage for the exact bounded wording",
    "provenance_confidence": "high",
    "publication_status": "withheld",
    "publication_basis": "unresolved",
    "surfaces": [],
    "note": "HOLD on corpus-data, public-git, web, download, print, and cli: exactness needs orthographic and spacing transformations beyond the approved line-wrap-only publication gate."
  },
  {
    "mass": "s-antonii-padua-confessoris-ecclesiae-doctoris",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "text_sha256": "4750a85cade3e62f43bc0e1525aea460e04d09f94788450e2f1d911e5baab0dc",
    "body_status": "removed"
  }
]''')

# Re-pinned after later accepted reader integrations: pre-1955 Bonn three
# (8d7e3b301), _proper_latin/_calendars/_missal_coverage (8d7e3b301, da270a039)
# and the Anthony-Collect oracle update in the Alexander/Hilary test.
PRESERVED_FILES = json.loads(r'''{
  "src/sources/calendars/roman-pre-1955/propers.yaml": "b28446e40b74769e7d16de193ad075dab362a9692b005a5e8ff8f97b1928291f",
  "src/sources/inventories/roman-pre-1955-proper-latin-provenance-v1.toml": "da959d9ba61843d2cb8f08155241b5b69058b6705f3d76aac67e6c70803546d9",
  "src/sources/inventories/christ-the-king-early-witnesses-rights-v1.toml": "709520743fe520e94386a6e514426ef27acc305d27d80d03ded7886e4831c7cd",
  "scripts/_proper_latin.py": "4a76b969d373bd23a06ea8905450c9b8ee10764e6cb68cc4b5d6621b2eb72aae",
  "scripts/_calendars.py": "54f37042b07ae107a9bea59fe6080d5699f70290335ae7ddee453752f35eb7d4",
  "scripts/_missal_coverage.py": "635cc202ce2bc40d8c6195733bd365cf9b63405bf8d60c2d2b9ee5782587589d",
  "tools/tests/test_roman_1962_winter_ursula_source_repair.py": "e7354e1d015919cc47f235fca3aa1f5134afc8fe250765eb24b6d2eafbc71f05",
  "tools/tests/test_roman_1962_octnov_commemoration_source_repair.py": "c13d838baf217cf25be163e465a4f90322d8ecf04e89322f237eec105764686e",
  "tools/tests/test_roman_1962_boniface_annual_source_repair.py": "b1cab01b3a01d831143e075cdc83345ef73d03145caf674624b1c27bf6c11775",
  "tools/tests/test_roman_1962_mayoct_source_repair.py": "8acb539c4388f6665f1b61b252879e2a73d6844052c21ae1d67d481e8d116599",
  "tools/tests/test_roman_1962_alexander_hilary_restoration.py": "04f9cc3568716f34b786d6cdc167977a11335fd2432b96313f2071e035524ce5",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/edition.toml": "010c0563003399bf9af8708cdede8ae59377cdf44793f299ff9130640b33f800",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-mennae-martyris-postcommunion.toml": "cd1e36b37e43bff1d02fb34a8f71098b17b81b40cea1dd54de323a9d4ac46d6f",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-callisti-i-papae-martyris-postcommunion.toml": "4fd8da4e92c3ba6e529effd00e3c90f072db7d569a88c23f4afc8488f62b9a9e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-fourth-day-within-octave-ss-innocentium-secret.toml": "20ac3eb8c17c74266669c56eed5b41f1a733b987f02a14f0b86d08ddfb2a13ef",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-venantii-martyris-secret.toml": "46247bb01c8347baef041bf908dcdc499eabf6c65854d3a311c6b7de1004fd80",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-second-day-within-octave-s-stephani-collect.toml": "61f563e4ef59942e41707d0a139ee3b87f07e3159ecac8e108a75d01bd90b32c",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-mennae-martyris-secret.toml": "99b2d3efcd446158b299f50507acd070214da746b083880b90e1cdc30129b86a",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-annae-matris-beatae-mariae-virginis-collect.toml": "f796c95eb421faed471c2bc6ba4ef1e7903cfccc401a41f3882a959b34dc8000",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-secret.toml": "d07979f0be69fd88fca4fc16caae51db438341a459100337175f85f1f8a5d4d9",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-thomae-episcopi-martyris-postcommunion.toml": "722c04406f6c548cbf58674d5d9e7de945e1b09b2c6000502acb94b8c74724d2",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-s-sabinae-martyris-secret.toml": "eea90957a34be5d1df60369c10d6237da384dfa3e84190ff004f7a64a2a6597f",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-commune-virginum-2-collect-word-repair.toml": "c45f489a1bef41e1d76235acf87a4213af61dfb1702d5475ce218cc5b2a56f7b",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-tryphonis-respicii-nymphae-virginis-secret.toml": "f2b21795553aea9f12823206bb77c29de96c617ff2fcbca8d632fb7fe48b6a7e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-third-day-within-octave-s-ioannis-collect.toml": "f89d3f6066b9763545a84f65432f755581cb289f933f1f319c4f2bcaaf15b5e5",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-saturnini-martyris-postcommunion.toml": "16f949a1d77edb436f79f39a8b2409806dc25e9f740aba74d01f1462a2d0be9e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/boniface-secret.toml": "98dcf46f755d4b71f2c13e234fbb137e09e3929020632670943bae7ad1e0f991",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-s-bibianae-virginis-martyris-postcommunion.toml": "837c169f4a69fe2b0b36554c9b230e79f09136227e2300d0c53196fa05e74703",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-saturnini-martyris-secret.toml": "8acbef22a5e18732ddb5002647e9ae0dfe6cbcdead5cec2120b0dc9919bc7547",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-thomae-episcopi-martyris-secret.toml": "ef3643cb77bbc48980ba3f28387eb8261a0fdfde78b0135b1bc45d9aa78ad836",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-euphemiae-virginis-luciae-geminiani-postcommunion.toml": "84b1f71799e133f2917b8ee64cfafb4c65cf391d81d8ddd231b67917225d6e16",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-thomae-episcopi-martyris-collect.toml": "5114923d0a5545c6d1aca2ee5150126073290d8144a90291bbbc3a303886823b",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-callisti-i-papae-martyris-secret.toml": "f1604284035d00043746ff586a0a4c237716b9322acfe44187cd1bdf910ea17e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-annae-matris-beatae-mariae-virginis-secret.toml": "6ab2113967b51c285e34bbee4b7491680ba24b4cd7f1570179e551d12dd30882",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-commune-virginum-2-secret-word-repair.toml": "acb85acef18d5d59091384294139e0db7053df00d8d5e470f9d276965a51c722",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-vitalis-agricolae-martyrum-postcommunion.toml": "5b0b91e93abcb88d14c1b61655aad188c25de21ecf81a44cfbe9f9df9d9db1dd",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-sergii-bacchi-marcelli-apuleii-postcommunion.toml": "ced30a69c64d6cfba6705bf9a1a8d3fdbeebb04e71845880d6c5a20ec399b598",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-ursulae-ac-sociarum-virginum-secret.toml": "3283cb779eec59fc9af4a26e83057f4d6d70357cfc135ab5ca507e5df6843f79",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-brunonis-confessoris-postcommunion.toml": "22eed0158358875c68591a10ef463e33f5b7ce4845496a36df38bdcab1dfc141",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-annae-matris-beatae-mariae-virginis-postcommunion.toml": "dfdbdff2783a28fd7ccb91b343fdf8b8d1b8d4dce0246dbba89d91bb75ff45ad",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-third-day-within-octave-s-ioannis-secret.toml": "d1da56d2cbdb49f1cf6afbf5ce0df23ac144622819e0ae1c548aa6d410ef1d97",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-felicis-simplicii-faustini-beatricis-secret.toml": "df85a66d050454559726a29c6743e742e93e6a49d322fff8dd717acbc305dd47",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-second-day-within-octave-s-stephani-postcommunion.toml": "1b6e9f97f6f27bf15e673e9c8c70999cb6d3d1e236e1503f9283b8e93ead0cfc",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-euphemiae-virginis-luciae-geminiani-collect.toml": "14b88740dcbbeedcad182ffa1d6d3a613832f6572365e66e1b64a33031fdc522",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-chrysogoni-martyris-secret.toml": "21e5df315a65ad3b4723900873e57228e95dbf48320d2434cd4eb1bf89bd3f98",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-tryphonis-respicii-nymphae-virginis-postcommunion.toml": "6b7323c22a577a47a3e7b6b56e23a90f51367cc826317542fa8237297b0d1a8d",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-venantii-martyris-postcommunion.toml": "11537572254c952fd2b9d4f328c6a3458c3c3b3ca6e706793dc84f94dde9d7f0",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-s-sabinae-martyris-postcommunion.toml": "3f5dde0adf1b2f4908da56e34565bb79be48c3792b38fc9c8a2c38886c92e64e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-s-nicomedis-martyris-secret.toml": "13db7720e81c0abce13f1d57cc75b7330722a569dbc506f54b8c4dc45ac51616",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-vitalis-agricolae-martyrum-secret.toml": "13042a3ca1d3d94befc8be9cf64a3f2e6d1210c501455280b913677eef550279",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-felicis-simplicii-faustini-beatricis-postcommunion.toml": "64c272d18cd0b3002d3b2d1ea521624e1068ee8d0154de41411ad3467ba42d7d",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-ss-ursulae-ac-sociarum-virginum-postcommunion.toml": "cbc3b80ddd26ab462ac4b397f85ed174fdeaa92c94312eebbb7d8aa6b59e2d55",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-sergii-bacchi-marcelli-apuleii-secret.toml": "fdfff1d0058f0db87fd2867588dc4c717b7d247bdeb185f22b28ea43763c558e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/boniface-collect.toml": "91eaa099bf08ce07eeecdf077f978b375302f8942385f3c67b6e7ffb3ca505f9",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/boniface-postcommunion.toml": "ce76bccf2eae835ab9b55611d8f39e17a34246fde960fb1e3d7fb7a0d05af4d0",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-francisci-borgiae-confessoris-secret.toml": "84eed07f296bf0734ecb895ec2de3b6b06505e30c0d042ef000c48a73da45ab8",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-alexandri-eventii-theoduli-martyrum-postcommunion.toml": "c12da4cdf1881f882d7e91de39fb2db84aff9d89da483b788655d9eab6d2839e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-fourth-day-within-octave-ss-innocentium-collect.toml": "c542fdc67e137e3920c30001c2bd44290fc593cd07e7f9b54d8b917f0e650138",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-hilarii-episcopi-confessoris-ecclesiae-doctoris-postcommunion.toml": "573b4ace5344c7ba5a58bb2b2ed09ae8e9751a4c5d9e6102522669e32de39baf",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-francisci-borgiae-confessoris-postcommunion.toml": "5f63a8f87c007f4d20a9da6389f0755fb7f272a4bc23cba65f5714145266a423",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-vitalis-agricolae-martyrum-collect.toml": "cd389bf1ed16a92c866d9a3e12fc840442d8a6711fa2c8309f196da6c2c76c10",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-saturnini-martyris-collect.toml": "4a48355c9c60bdbb32e83b9078d94aac59434f484f0606f59b4cd53dcc2c6c07",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-s-bibianae-virginis-martyris-collect.toml": "bf54562bc6ca2325e6b7e3d63fbde419a796a10dbf05a3f13d7e293dc6405772",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-s-bibianae-virginis-martyris-secret.toml": "01287127808713dc7de4aae9e0d3d994f3eb5788744041f93a7bf038879cf645",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-chrysogoni-martyris-postcommunion.toml": "e2809f2546345dc2d336ba3ef6abd7156df4280d51cac0ef2e7481baca5de09e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-postcommunion.toml": "312108f492dc32ccace60667bbd6d2e23ff2db63a2f80c404db77855d5414536",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-fourth-day-within-octave-ss-innocentium-postcommunion.toml": "a1c9c2b0a4203a5d338fd6faca38b48ed6b6d9219403de2b0223e6175a4093a7",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-felicitatis-martyris-postcommunion.toml": "98ef55fcabf3eb1fab3bb395ff2729e33c2c31b3b1f00d1a76a80a7afa32ce95",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-s-nicomedis-martyris-postcommunion.toml": "cfeb3d7d0f9251549ac5d6674e07e7125d16e67a39e79a46b37ab36bc4a0beca",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-sabbae-abbatis-postcommunion.toml": "d8c6b29616afb4d25de634f90d97952b91ad7846f76148c6531b1bc151176419",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-sabbae-abbatis-secret.toml": "ee97b5b783753b73b53d92f168ac65ee81df0db2a3de054389516e93c153b064",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-comm-ss-euphemiae-virginis-luciae-geminiani-secret.toml": "175095a9b36333d75e3faed9480564fd4dedc97b0e762520f9ef407350450666",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-ss-tryphonis-respicii-nymphae-virginis-collect.toml": "e52022171bc2bdfa46cce4cf0e379538cb070d733abf20c640b1986a83228be2",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-second-day-within-octave-s-stephani-secret.toml": "7cd126ff05473fa6636b2da33768df75cefe344372a2f27f7ee29a8feb4ab84e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase2-comm-s-felicitatis-martyris-secret.toml": "6b0d877e7d48fc8263b763a198628de3ab71dab0a207aaf0f4f2d0fd237148ea",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-comm-s-sabbae-abbatis-collect.toml": "558bcd92c11c0f6c575cdefc145764096ef78645f3bc8910690451ab67d32036",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase3-third-day-within-octave-s-ioannis-postcommunion.toml": "cf20b94db4f1ae235d713517bdc8e61d6913226c02fe90a40cb2b669ca1375ce",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/boniface-three-orations-ae811235/artifact.toml": "b5d28b4ddad8919f3740b29d1e13011db001546f28963dd07bb4377027d49e7d",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/boniface-three-orations-ae811235/boniface-three-orations.txt": "ae81123525827b67576e175b54004653cce51016d900716364650afe56b5e74f",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase3-ursula-postcommunion-20261022/phase3-ursula-postcommunion.txt": "5a5b9ed5c33e154ea2ca35320f7447da49d6100622ca563537e849b60d0137d2",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase3-ursula-postcommunion-20261022/artifact.toml": "4f2240e5980faf12b5368a7bc1353cfda944d40c741cd3a1448d2378a258586e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-mayoct-alexander-twentytwo-orations-20261022/artifact.toml": "5a7fa5351815148bae82439129b78707f01f72c6f1362615be9acc9fec3c3531",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-mayoct-alexander-twentytwo-orations-20261022/phase4-mayoct-alexander-twentytwo-orations.txt": "dd94f56f258e665930043284c747c41852bb47371aa2fda01337a58bb459dc11",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-common-virgin-ii-two-word-repair-ce623d9f/artifact.toml": "becfea4f799e4cf8a39283d2eaedda167f5e95ae4aaba846b7194a951ef5e327",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-common-virgin-ii-two-word-repair-ce623d9f/common-virgin-ii-collect-secret.txt": "ce623d9f71e6021c3e7121f910ef5f7adce6122d6e007eb5905ec50834a6841e",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-hilary-postcommunion-20261022/artifact.toml": "74dce5caae2dda6e4b4d6093d700673438fd63a9acb3ada76391dd5d484300d0",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-hilary-postcommunion-20261022/phase4-hilary-postcommunion.txt": "7037ccdbaacb3debd53b93d275f320b12899fb9c5f7fbf98b2526dd8c497fab0",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase3-winter-eighteen-orations-20261022/artifact.toml": "9976ac91badd8afa05862407427fc0f2db74a68968f1fc9c5e6c2a98ebca4a54",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase3-winter-eighteen-orations-20261022/phase3-winter-eighteen-orations.txt": "3f31c1eef89a6baa0dbbb26b6616f89dc2edf003b6a080680d9517f843a81146",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase2-octnov-commemorations-20261022/artifact.toml": "49501ae110491258124582be3e8364e6233f87209f3a7a6f54e70a58e0533f90",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase2-octnov-commemorations-20261022/phase2-octnov-commemorations.txt": "cfb24c25cfb2496837f71eda4551e785e12f682075416d244aabffbf6aa44bd5"
}''')

KEYS = {key(x) for x in ORACLES}


class Latin22Phase5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/"src/sources/calendars/roman-1962/propers.yaml").read_text()
        cls.doc=yaml.safe_load(cls.source)
        cls.ledger=(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text()
        cls.records,errors=read_sidecar(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:raise AssertionError(errors)

    def test_22_fixed_whole_bodies_and_fail_closed_six_surface_hashes(self):
        self.assertEqual((22,20,2),(len(KEYS),sum(not x["restored"] for x in ORACLES),sum(x["restored"] for x in ORACLES)))
        for x in ORACLES:
            with self.subTest(mass=x["mass"],proper=x["proper"]):
                p=node_at(self.doc,x["path"]);r=self.records[key(x)]
                self.assertEqual(x["proper"],p["name"])
                self.assertEqual(x["body"],p["text"])
                self.assertEqual(x["body_sha256"],digest(p["text"]))
                self.assertNotIn("text_status",p)
                self.assertNotIn("body_status",r)
                self.assertEqual(("collated","permitted","public-domain"),tuple(r[k] for k in ["provenance_status","publication_status","publication_basis"]))
                self.assertTrue(decision_for(key(x),p["text"],self.records).permits(SURFACES))
                self.assertFalse(decision_for(key(x),p["text"]+"Amen.\n",self.records).permits(SURFACES))

        # The correction adopts the actual one-l reading in both witnesses.
        # Strict source-validated publication records must reject the superseded
        # two-l body, even though it is a permissible received spelling generally.
        therese=next(x for x in ORACLES if x["mass"]=="s-teresiae-a-iesu-infante-virginis" and x["proper"]=="Secret")
        old=therese["body"].replace("solemniter","sollemniter")
        self.assertEqual("d7798392abc24558fcb314f9de2bfe3490199d87a03351d4de63bd215f938521",digest(old))
        validated,errors=publication_records(ROOT/"src/sources/calendars","roman-1962")
        self.assertEqual([],errors)
        self.assertTrue(decision_for(key(therese),therese["body"],validated).permits(SURFACES))
        rejected=decision_for(key(therese),old,validated)
        self.assertFalse(rejected.permits(SURFACES))
        self.assertIn("stale text hash",rejected.reason)
        self.assertEqual(["solemniter"],[t for t in tokens(therese["body"]) if t in {"solemniter","sollemniter"}])
        for passage_id in [therese["historical_passage_id"],therese["projection_passage_id"],therese["target_passage_id"]]:
            self.assertIn("both print solemniter (one l)",record(passage_id)["notes"])
            self.assertNotIn("target sollemniter",record(passage_id)["notes"])

    def test_whole_petition_word_identity_and_declared_received_spellings(self):
        for x in ORACLES:
            h=received(x["historical_body"]);t=received(x["body"])
            he=received(x["historical_ending"]);te=received(x["target_ending"])
            self.assertEqual(he,h[-len(he):],x["mass"])
            self.assertEqual(te,t[-len(te):],x["mass"])
            self.assertEqual(h[:-len(he)],t[:-len(te)],(x["mass"],x["proper"]))
            self.assertNotIn("N.",x["body"])
            evidence=" ".join(self.records[key(x)]["transformations"])
            for difference in x["differences"]:self.assertIn(difference,evidence)

    def test_six_formula_prefix_expansions_and_two_explicit_shortenings(self):
        expanded=[x for x in ORACLES if x["formula"]]
        self.assertEqual(6,len(expanded))
        formulas={
            "father-through-son":"Per Dominum nostrum Jesum Christum Filium tuum: Qui tecum vivit et regnat in unitate ejusdem Spiritus sancti Deus.",
            "son-addressed":"Qui vivis et regnas cum Deo Patre, in unitate Spiritus sancti Deus etc."}
        for x in expanded:
            prefix=tokens(x["target_ending"]);formula=tokens(formulas[x["formula"]])
            self.assertEqual(prefix,formula[:len(prefix)])
            self.assertGreater(len(prefix),len(tokens(x["historical_ending"])))
            self.assertNotIn("Spiritus",x["target_ending"])
            self.assertNotIn("Amen",x["body"])
            self.assertIn(x["formula_passage_id"],self.records[key(x)]["provenance_evidence"])
            self.assertIn(AUTHORITY_ARTIFACT,self.records[key(x)]["publication_source_ids"])
        shorter=[x for x in ORACLES if len(tokens(x["target_ending"]))<len(tokens(x["historical_ending"]))]
        self.assertEqual({("lent-1-thursday","Oratio super populum"),("sacred-heart","Secret")},{(x["mass"],x["proper"]) for x in shorter})
        for x in shorter:self.assertEqual(tokens(x["target_ending"])+["nostrum"],tokens(x["historical_ending"]))
        for x in AUTHORITY:
            p=record(x["passage_id"]);a=record(p["artifact_id"]);lines=(ROOT/a["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(x["body"],"".join(lines[x["physical_line_ranges"][0][0]-1:x["physical_line_ranges"][0][1]]))
        son=next(x for x in AUTHORITY if x["slug"]=="son-addressed")
        self.assertTrue(son["body"].endswith("Deus etc.\n"))

    def test_per_owner_source_target_projection_and_rights_bindings(self):
        for x in ORACLES:
            r=self.records[key(x)];lane=LANES[x["lane"]]
            self.assertEqual((x["projection_passage_id"],x["target_passage_id"]),(r["source_id"],r["verification_source_id"]))
            p=record(r["source_id"]);a=record(p["artifact_id"]);data=(ROOT/a["path"]).read_bytes()
            self.assertEqual((lane["artifact_id"],lane["sha256"]),(p["artifact_id"],p["artifact_sha256"]))
            self.assertEqual(a["sha256"],digest(data))
            self.assertEqual(a["byte_size"],len(data))
            lines=data.decode().splitlines(keepends=True)
            self.assertEqual(x["body"],"".join("".join(lines[i-1:j]) for i,j in p["physical_line_ranges"]))
            self.assertEqual("editorial-projection",a["artifact_type"])
            self.assertIn(TARGET,a["projected_from"])
            historical=record(x["historical_passage_id"]);h=record(historical["artifact_id"])
            self.assertEqual((lane["historical_artifact_id"],lane["historical_sha256"]),(historical["artifact_id"],historical["artifact_sha256"]))
            self.assertEqual("public-domain",h["rights_status"])
            self.assertEqual(h["sha256"],digest((ROOT/h["path"]).read_bytes()))
            self.assertIn(x["historical_passage_id"],r["provenance_evidence"])
            target=record(x["target_passage_id"])
            self.assertEqual((TARGET,TARGET_HASH,x["target_locus"]),(target["artifact_id"],target["artifact_sha256"],target["locus"]))
            self.assertEqual(1,target["schema"]) # Existing restricted controller has no registered page_count.
            self.assertNotIn(TARGET,r["publication_source_ids"])
            self.assertIn(lane["historical_artifact_id"],r["publication_source_ids"])

    def test_schott_latin_only_extent_and_restricted_parent_do_not_expand(self):
        lane=LANES["schott"];a=record(lane["historical_artifact_id"])
        self.assertEqual("restricted",record(a["derived_from"])["rights_status"])
        selected=[x for x in ORACLES if x["lane"]=="schott"]
        self.assertEqual(7,len(selected))
        self.assertEqual("\n\n".join(x["historical_body"] for x in selected)+"\n",(ROOT/a["path"]).read_text())
        for x in selected:
            p=record(x["historical_passage_id"]);lines=(ROOT/a["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(x["historical_body"]+"\n","".join("".join(lines[i-1:j]) for i,j in p["physical_line_ranges"]))
        self.assertIn("corroborated inference",a["rights_basis"])
        self.assertIn("end2024",a["rights_basis"])
        self.assertIn("missing scan pages remain unfilled",a["notes"])
        self.assertIn("No German",a["notes"])
        self.assertIn("1929",a["rights_basis"])

    def test_1247_prior_body_bytes_and_all_unowned_yaml_ledger_bytes(self):
        BATCH_GUARDS.assert_live_baseline_bodies(self.doc)
        prior_document = BATCH_GUARDS.historical_document(self.doc)
        present=[dict(key=k.as_dict(),body=b,state=s) for k,b,s in body_owners(prior_document) if s=="present" and k not in KEYS]
        self.assertEqual(1247,len(present))
        self.assertEqual(PRIOR_PRESENT_SHA256,digest(canonical(present)))
        self.assertEqual(UNOWNED_YAML_SHA256,digest(yaml_unowned(BATCH_GUARDS.historical_text(BATCH_GUARDS.YAML_PATH, self.source))))
        self.assertEqual(UNOWNED_LEDGER_SHA256,digest(ledger_unowned(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH, self.ledger))))
        for x,wrapper in zip(ORACLES,WRAPPERS):
            p=node_at(self.doc,x["path"])
            self.assertEqual(wrapper,{k:v for k,v in p.items() if k not in {"text_status","text","notes"}})
        for path,h in PRESERVED_FILES.items():
            if path == "scripts/_proper_latin.py":
                # This code input is not one of the seventeen source inverses.
                # Its original literal is archived from the accepted 6aeb96a392
                # checkpoint, separately from the later finite-authority code.
                archived = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/checkpoint-v1/historical-code/proper-latin-prior.py"
                self.assertEqual(h, digest(archived.read_bytes()), path + " at 6aeb96a392")
                self.assertEqual("d94a4301e865dc7d7f9fc8d657761201675e0123041e3ef00973b36565199376",
                                 digest((ROOT / path).read_bytes()), path + " current")
                authority = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v1.json"
                self.assertEqual("920299972ab84575183de8c84adcd3f7418bdc46304fbe1d6a4435fad1103ee3",
                                 digest(authority.read_bytes()))
                self.assertEqual("adopted", json.loads(authority.read_text())["state"])
            elif path == "scripts/_missal_coverage.py":
                archived = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/checkpoint-v1/historical-code/missal-coverage-prior.py"
                self.assertEqual(h, digest(archived.read_bytes()), path + " at 6aeb96a392")
                self.assertEqual("10dbc61463d145cb642d52829be8e026e4fee46720b2f3e9221fe3f6ff397f70",
                                 digest((ROOT / path).read_bytes()), path + " current")
                # Typed evidence behavior has its own coverage/report tests;
                # these code pins do not grant source or wording authority.
            else:
                self.assertEqual(h,digest(BATCH_GUARDS.historical_bytes(path)),path)

    def test_remaining_twenty_removed_holds_and_exact_accounting(self):
        BATCH_GUARDS.assert_current_latin(self.records)
        BATCH_GUARDS.assert_live_baseline_bodies(self.doc)
        raw=tomllib.loads(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH, self.ledger))["entries"]
        removed=[x for x in raw if x.get("body_status")=="removed"]
        self.assertEqual(REMAINING_REMOVED,removed)
        self.assertEqual((1289,1269,20),(len(raw),sum(x.get("publication_status")=="permitted" for x in raw),len(removed)))
        owners=list(body_owners(BATCH_GUARDS.historical_document(self.doc)))
        self.assertEqual((1269,20),(sum(s=="present" for _,_,s in owners),sum(s=="removed" for _,_,s in owners)))

    def test_raw_and_production_resolver_roles_and_boundaries(self):
        index=C.mass_index(self.doc)
        for x in ORACLES:
            resolved,errors=C.resolve_propers(self.doc,index[x["mass"]],appointments=True)
            self.assertEqual([],errors)
            found=[p for f,p,_ in resolved if f==x["form"] and p["name"]==x["proper"]]
            self.assertEqual([x["body"]],[p.get("text") for p in found])
        ember=index["lent-1-ember-wednesday"]["propers"]
        self.assertEqual(("First Gradual","Oratio","Second Lesson"),tuple(ember[i]["name"] for i in [3,4,5]))
        pent=index["pentecost-ember-wednesday"]["propers"]
        self.assertEqual(("Second Lesson","Second Alleluia","Sequence"),tuple(pent[i]["name"] for i in [5,6,7]))
        th=next(x for x in ORACLES if x["mass"]=="s-teresiae-a-iesu-infante-virginis" and x["proper"]=="Collect")
        self.assertEqual(3758,th["target"]["unit"])
        secret=next(x for x in ORACLES if x["mass"]=="sacred-heart" and x["proper"]=="Secret")
        self.assertEqual([461],secret["target"]["pdf"])
        vianney=next(x for x in ORACLES if x["mass"]=="s-ioannis-mariae-vianney-confessoris")
        self.assertIn("qui sanctum Joannem Mariam"," ".join(vianney["body"].split()))
        self.assertTrue(" ".join(vianney["body"].split()).endswith("Per eundem Dominum."))
        john=next(x for x in ORACLES if x["mass"]=="s-ioannis-a-cruce-confessoris-ecclesiae")
        self.assertIn("Confessorem tuum atque Doctorem"," ".join(john["body"].split()))

    def test_p55_inheritance_is_not_a_new_publication_or_target_attestation(self):
        records,errors=publication_records(ROOT/"src/sources/calendars","roman-pre-1955")
        self.assertEqual([],errors)
        for x in ORACLES:
            self.assertFalse(decision_for(key(x),x["body"],records).permits(SURFACES))
            self.assertIn("target-recension",records[key(x)]["note"])
            self.assertEqual([],records[key(x)]["surfaces"])

    def test_real_cli_exact_1962_bodies_and_p55_refusal(self):
        for mass in sorted({x["mass"] for x in ORACLES}):
            for calendar in ["roman-1962","roman-pre-1955"]:
                p=subprocess.run([sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show","--calendar",calendar,"--mass",mass,"--format","json"],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(0,p.returncode,p.stderr)
                m=json.loads(p.stdout)["mass"]
                for x in [x for x in ORACLES if x["mass"]==mass]:
                    group=next(f["propers"] for f in m["forms"] if f["name"]==x["form"]) if x["form"] else m["propers"]
                    proper=next(v for v in group if v["name"]==x["proper"])
                    if calendar=="roman-1962":
                        self.assertEqual(x["body"],proper["text"])
                        if x["mass"]=="s-teresiae-a-iesu-infante-virginis" and x["proper"]=="Secret":
                            self.assertIn("both print solemniter (one l)",json.dumps(proper,ensure_ascii=False))
                            self.assertNotIn("target sollemniter",json.dumps(proper,ensure_ascii=False))
                    else:
                        self.assertIsNone(proper.get("text"))
                        self.assertTrue(proper["latin"]["withheld"])

if __name__=="__main__":
    unittest.main()
