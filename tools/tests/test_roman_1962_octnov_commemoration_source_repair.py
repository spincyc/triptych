"""Eighteen complete own prayers, with distinct target control and old-word rights.

The fixed body oracles below were compared with target page images and the
retained 1862 pages; they are not learned from the calendar or its ledger.
Independent cold source review remains a separate acceptance gate.
"""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import yaml
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from tools.tests import _source_batch_guards as BATCH_GUARDS
import _calendars as C
from _proper_latin import LatinKey, SURFACES, body_owners, decision_for, read_sidecar

HIST = "catholic-church.missale-romanum.pustet-ratisbon-1862"
CONTROL = "catholic-church.missale-romanum.vatican-typica-1962"
PROJECT = "triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22"
HIST_ARTIFACT = "artifact." + HIST + ".phase2-octnov-commemoration-pages-20261022"
PROJECT_ARTIFACT = "artifact." + PROJECT + ".phase2-octnov-commemorations-20261022"
TARGET_ARTIFACT = "artifact." + CONTROL + ".cmaa-facsimile-pdf"
HIST_HASH = "e9c01846945e38c79bd43b9d9a7da4df7a0fc7c520875f3cf97c24b501bedc78"
PROJECT_HASH = "cfb24c25cfb2496837f71eda4551e785e12f682075416d244aabffbf6aa44bd5"
ORACLES = json.loads(r'''[
  {
    "mass": "comm-ss-sergii-bacchi-marcelli-apuleii",
    "proper": "Secret",
    "body": "Majestatem tuam nobis, Domine, quaesumus, haec hostia reddat immolanda\nplacatam, tuorum digna postulatione Sanctorum. Per Dominum.\n",
    "body_sha256": "3b312da3ef6bbaabae27f02bf13d00143847fe89ce45bb1917cd3f5b160e479a",
    "physical_line_ranges": [
      [
        1,
        2
      ]
    ],
    "target": {
      "pdf": 762,
      "printed": "681",
      "unit": "3816",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        642
      ],
      "printed": [
        "556"
      ],
      "column": "L",
      "heading": "Secreta"
    }
  },
  {
    "mass": "comm-ss-sergii-bacchi-marcelli-apuleii",
    "proper": "Postcommunion",
    "body": "Sacramentis, Domine, muniamur acceptis: et sanctorum Martyrum tuorum\nSergii, Bacchi, Marcelli et Apuleii intercessione, contra omnes\nnequitias irruentes, armis caelestibus protegamur. Per Dominum.\n",
    "body_sha256": "e21b7428f2efd8030cbe61e0d12e4fde5c58d42185e8721c6f046dfd127c73ed",
    "physical_line_ranges": [
      [
        4,
        6
      ]
    ],
    "target": {
      "pdf": 762,
      "printed": "681",
      "unit": "3817",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        642
      ],
      "printed": [
        "556"
      ],
      "column": "R",
      "heading": "Pro sanctis Martyribus. Postcommunio"
    }
  },
  {
    "mass": "comm-ss-ursulae-ac-sociarum-virginum",
    "proper": "Secret",
    "body": "Intende, quaesumus, Domine, munera altaribus tuis pro sanctarum\nVirginum et Martyrum tuarum Ursulae et Sociarum ejus festivitate\nproposita; ut, sicut per haec beata mysteria illis gloriam contulisti;\nita nobis indulgentiam largiaris. Per Dominum.\n",
    "body_sha256": "e5f7bdf9955b0c3ff263081dc4e3b3b6b3dd44536443d2a7c58bcb9e5382e012",
    "physical_line_ranges": [
      [
        8,
        11
      ]
    ],
    "target": {
      "pdf": 775,
      "printed": "694",
      "unit": "3921",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        649
      ],
      "printed": [
        "563"
      ],
      "column": "R",
      "heading": "Secreta"
    }
  },
  {
    "mass": "comm-ss-vitalis-agricolae-martyrum",
    "proper": "Collect",
    "body": "Praesta, quaesumus, omnipotens Deus: ut, qui sanctorum Martyrum tuorum\nVitalis et Agricolae solemnia colimus, eorum apud te intercessionibus\nadjuvemur. Per Dominum.\n",
    "body_sha256": "a9f91f01c49bec151e7f0d1dc3b3966ad5efb37c9c194711723368c0cc909217",
    "physical_line_ranges": [
      [
        13,
        15
      ]
    ],
    "target": {
      "pdf": 792,
      "printed": "711",
      "unit": "4035",
      "column": "L"
    },
    "historical": {
      "pdf": [
        657
      ],
      "printed": [
        "571"
      ],
      "column": "R",
      "heading": "Pro SS. Vitale et Agricola Martyribus. Oratio"
    }
  },
  {
    "mass": "comm-ss-vitalis-agricolae-martyrum",
    "proper": "Secret",
    "body": "Oblatis, quaesumus, Domine, placare muneribus: et, intercedentibus\nsanctis Martyribus tuis Vitale et Agricola, a cunctis nos defende\npericulis. Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum\nvivit et regnat in unitate.\n",
    "body_sha256": "745a0803357ee930c43cbbe8504507d0bf1b23e41c1b22dabd1001157e7afb97",
    "physical_line_ranges": [
      [
        17,
        20
      ]
    ],
    "target": {
      "pdf": 792,
      "printed": "711",
      "unit": "4041",
      "column": "R"
    },
    "historical": {
      "pdf": [
        658
      ],
      "printed": [
        "572"
      ],
      "column": "L",
      "heading": "Pro sanctis Martyribus. Secreta"
    }
  },
  {
    "mass": "comm-ss-vitalis-agricolae-martyrum",
    "proper": "Postcommunion",
    "body": "Haec nos communio, Domine, purget a crimine: et, intercedentibus\nsanctis Martyribus tuis Vitale et Agricola, caelestis remedii faciat\nesse consortes. Per Dominum nostrum Jesum Christum, Filium tuum: Qui\ntecum vivit et regnat in unitate.\n",
    "body_sha256": "274e6f70f149253c31c85896bbf9ce4c80a6e64c2946684b146d564bc8c583dd",
    "physical_line_ranges": [
      [
        22,
        25
      ]
    ],
    "target": {
      "pdf": 792,
      "printed": "711",
      "unit": "4043",
      "column": "R"
    },
    "historical": {
      "pdf": [
        658
      ],
      "printed": [
        "572"
      ],
      "column": "L bottom to R top",
      "heading": "Pro sanctis Martyribus. Postcommunio"
    }
  },
  {
    "mass": "comm-ss-tryphonis-respicii-nymphae-virginis",
    "proper": "Collect",
    "body": "Fac nos, quaesumus, Domine, sanctorum Martyrum tuorum Tryphonis,\nRespicii et Nymphae semper festa sectari: quorum suffragiis,\nprotectionis tuae dona sentiamus. Per Dominum.\n",
    "body_sha256": "deb57a9cfa239206bf764cdd2af1ecf027ad45cee56a7eaba8c7887e37fbea65",
    "physical_line_ranges": [
      [
        27,
        29
      ]
    ],
    "target": {
      "pdf": 795,
      "printed": "714",
      "unit": "4064",
      "column": "R"
    },
    "historical": {
      "pdf": [
        660
      ],
      "printed": [
        "574"
      ],
      "column": "R",
      "heading": "Oratio"
    }
  },
  {
    "mass": "comm-ss-tryphonis-respicii-nymphae-virginis",
    "proper": "Secret",
    "body": "Munera tibi, Domine, nostrae devotionis offerimus: quae et pro tuorum\ntibi grata sint honore justorum, et nobis salutaria, te miserante,\nreddantur. Per Dominum.\n",
    "body_sha256": "27eb1021a8ae63e7ba3d0fc482b4cce5981dc4ce889215748e24ab680b4e4fff",
    "physical_line_ranges": [
      [
        31,
        33
      ]
    ],
    "target": {
      "pdf": 796,
      "printed": "715",
      "unit": "4070",
      "column": "L"
    },
    "historical": {
      "pdf": [
        661
      ],
      "printed": [
        "575"
      ],
      "column": "L",
      "heading": "Secreta"
    }
  },
  {
    "mass": "comm-ss-tryphonis-respicii-nymphae-virginis",
    "proper": "Postcommunion",
    "body": "Praesta nobis, quaesumus, Domine: intercedentibus sanctis Martyribus\ntuis Tryphone, Respicio et Nympha; ut, quod ore contingimus, pura\nmente capiamus. Per Dominum nostrum Jesum Christum, Filium tuum: Qui\ntecum vivit et regnat in unitate.\n",
    "body_sha256": "07a740e583d7ee0b12022fdf9ec48b5df76ee8a1f4e9aad3345b9a2af68be281",
    "physical_line_ranges": [
      [
        35,
        38
      ]
    ],
    "target": {
      "pdf": 796,
      "printed": "715",
      "unit": "4072",
      "column": "R"
    },
    "historical": {
      "pdf": [
        661
      ],
      "printed": [
        "575"
      ],
      "column": "L",
      "heading": "Postcommunio"
    }
  },
  {
    "mass": "comm-s-mennae-martyris",
    "proper": "Secret",
    "body": "Muneribus nostris, quaesumus, Domine, precibusque susceptis: et\ncaelestibus nos munda mysteriis, et clementer exaudi. Per Dominum.\n",
    "body_sha256": "358b3c80aa6754c588523873263e1a3345eaff44ecb50d9714f1e1257c845f47",
    "physical_line_ranges": [
      [
        40,
        41
      ]
    ],
    "target": {
      "pdf": 798,
      "printed": "717",
      "unit": "4088",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        662
      ],
      "printed": [
        "576"
      ],
      "column": "L",
      "heading": "Secreta"
    }
  },
  {
    "mass": "comm-s-mennae-martyris",
    "proper": "Postcommunion",
    "body": "Da, quaesumus, Domine Deus noster: ut, sicut tuorum commemoratione\nSanctorum, temporali gratulamur officio; ita perpetuo laetemur\naspectu. Per Dominum.\n",
    "body_sha256": "e20901eac87b8ebf187effd60b30e33fcebf6dd2846867cad74247ba6ef21603",
    "physical_line_ranges": [
      [
        43,
        45
      ]
    ],
    "target": {
      "pdf": 798,
      "printed": "717",
      "unit": "4089",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        662
      ],
      "printed": [
        "576"
      ],
      "column": "L-to-R",
      "heading": "Postcommunio"
    }
  },
  {
    "mass": "comm-s-felicitatis-martyris",
    "proper": "Secret",
    "body": "Vota populi tui, Domine, propitiatus intende: et, cujus nos tribuis\nsolemnia celebrare, fac gaudere suffragiis. Per Dominum.\n",
    "body_sha256": "e6e1a1e31175529247f57f551f79c5c2421b44e9f37071a8131259b4793ad3cf",
    "physical_line_ranges": [
      [
        47,
        48
      ]
    ],
    "target": {
      "pdf": 806,
      "printed": "725",
      "unit": "4158",
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        668
      ],
      "printed": [
        "582"
      ],
      "column": "R",
      "heading": "Pro S. Felicitate Mart. Secreta"
    }
  },
  {
    "mass": "comm-s-felicitatis-martyris",
    "proper": "Postcommunion",
    "body": "Supplices te rogamus, omnipotens Deus: ut, intercedentibus Sanctis\ntuis, et tua in nobis dona multiplices, et tempora nostra disponas.\nPer Dominum nostrum.\n",
    "body_sha256": "73c245cfdb76716117797efa254e74ac132b37fc0c0b204834640751557f2be4",
    "physical_line_ranges": [
      [
        50,
        52
      ]
    ],
    "target": {
      "pdf": 806,
      "printed": "725",
      "unit": "4159",
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        669
      ],
      "printed": [
        "583"
      ],
      "column": "L",
      "heading": "Pro S. Felicitate Mart. Postcommunio"
    }
  },
  {
    "mass": "comm-s-chrysogoni-martyris",
    "proper": "Secret",
    "body": "Oblatis, quaesumus, Domine, placare muneribus: et, intercedente beato\nChrysogono Martyre tuo, a cunctis nos defende periculis. Per Dominum\nnostrum.\n",
    "body_sha256": "a65df37219ba0b98805405af6a34d306669402cb6a1a52b4973ed37bbd8c5ba9",
    "physical_line_ranges": [
      [
        54,
        56
      ]
    ],
    "target": {
      "pdf": 807,
      "printed": "726",
      "unit": "4163",
      "column": "L"
    },
    "historical": {
      "pdf": [
        670
      ],
      "printed": [
        "584"
      ],
      "column": "R",
      "heading": "Secreta in S. Chrysogoni Mart."
    }
  },
  {
    "mass": "comm-s-chrysogoni-martyris",
    "proper": "Postcommunion",
    "body": "Tui, Domine, perceptione sacramenti, et a nostris mundemur occultis,\net ab hostium liberemur insidiis. Per Dominum.\n",
    "body_sha256": "a61cd82cc930a26f0cfde418e0d9d0fbf4a6db87a7ffca3ce0501a32e1f3ec3e",
    "physical_line_ranges": [
      [
        58,
        59
      ]
    ],
    "target": {
      "pdf": 807,
      "printed": "726",
      "unit": "4165",
      "column": "L"
    },
    "historical": {
      "pdf": [
        670
      ],
      "printed": [
        "584"
      ],
      "column": "R",
      "heading": "Postcommunio in S. Chrysogoni Mart."
    }
  },
  {
    "mass": "comm-s-saturnini-martyris",
    "proper": "Collect",
    "body": "Deus, qui nos beati Saturnini Martyris tui concedis natalicio perfrui:\nejus nos tribue meritis adjuvari. Per Dominum.\n",
    "body_sha256": "22bc39335d9f5fa1a811589a5f34b8de1044ea2086b0bae1fa8c912bd582cbba",
    "physical_line_ranges": [
      [
        61,
        62
      ]
    ],
    "target": {
      "pdf": 509,
      "printed": "Proprium Sanctorum opening, unnumbered",
      "unit": "1809",
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        448
      ],
      "printed": [
        "362 (opening leaf, number suppressed)"
      ],
      "column": "R",
      "heading": "Pro commemor. S. Saturnini Martyris. Oratio in Vigilia S. Andreae"
    }
  },
  {
    "mass": "comm-s-saturnini-martyris",
    "proper": "Secret",
    "body": "Munera, Domine, tibi dicata sanctifica: et, intercedente beato\nSaturnino Martyre tuo, per haec eadem nos placatus intende. Per\nDominum.\n",
    "body_sha256": "4bb23534461afb16e55498de1841c0212b423e44c36c788b46f5781e4429a79b",
    "physical_line_ranges": [
      [
        64,
        66
      ]
    ],
    "target": {
      "pdf": 509,
      "printed": "Proprium Sanctorum opening, unnumbered",
      "unit": "1810",
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        450
      ],
      "printed": [
        "364"
      ],
      "column": "R",
      "heading": "Pro S. Saturnino. Secreta in Vigilia S. Andreae"
    }
  },
  {
    "mass": "comm-s-saturnini-martyris",
    "proper": "Postcommunion",
    "body": "Sanctificet nos, quaesumus, Domine, tui perceptio sacramenti: et\nintercessione Sanctorum tuorum tibi reddat acceptos. Per Dominum\nnostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat in\nunitate.\n",
    "body_sha256": "ad9e7c1a738581515156c43f62c5bb98290117f10b98a3bb73431fa603a7e6ab",
    "physical_line_ranges": [
      [
        68,
        71
      ]
    ],
    "target": {
      "pdf": 509,
      "printed": "Proprium Sanctorum opening, unnumbered",
      "unit": "1811",
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        450,
        451
      ],
      "printed": [
        "364",
        "365"
      ],
      "column": "R bottom to L top",
      "heading": "Pro sancto Saturnino. Postcommunio in Vigilia S. Andreae"
    }
  }
]''')
KEYS = {(r["mass"], r["proper"]) for r in ORACLES}
MASSES = list(dict.fromkeys(r["mass"] for r in ORACLES))


def digest(value):
    if isinstance(value, str):
        value = value.encode()
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def record(identifier):
    kind, owner, work, edition, name = identifier.split(".")
    if edition.startswith("editorial-projection-"):
        edition = edition.removeprefix("editorial-projection-") + "-editorial-projection"
    base = ROOT / "src/sources/works" / owner / work / "editions" / edition
    path = base / "artifacts" / name / "artifact.toml" if kind == "artifact" else base / "passages" / (name + ".toml")
    row = tomllib.loads(path.read_text())
    if row["id"] != identifier:
        raise AssertionError(identifier)
    return row


def latin_key(r):
    return LatinKey(r["mass"], "", r["proper"], "", "", 1)


def prayer(index, r):
    return next(p for p in index[r["mass"]]["propers"] if p["name"] == r["proper"])



# Fixed authority: independently accepted corrected Latin22 source ZIP
# 49d60c3be6e6d5106eb7fbf68401cb8c61778cce382f2720f66f10a7c893769e.
# accepted22-authority.json SHA256 ad19f18c83be912ea90bae78f6f71377e8429c3f788962e3a05d8f70815f7e2f;
# source receipt SHA256 3d15ddac0abafbecaeffa77ad54bc0b3b872a40a965c638dd0749227a7bd39e8.
# These literals are NOT imported from the new Phase5 test or runtime scratch.
PHASE5_PREDECESSOR_YAML = "56a045e25b0f533d7b6466b4017c57c87f2066e11e5bc7e1e08e52e80ab6ab48"
PHASE5_PREDECESSOR_LEDGER = "7275c5fe135c3a147321ce9be3ac0db7b2a2c87b29a0265ac05353663a11c09c"
PHASE5_PREDECESSOR_DOCUMENT = "532b5dd86ede4ea2b7f98b9e80d19b3f0070515c3254ece4ece66cc6373f1a34"
PHASE5_PREDECESSOR_CHRISTMAS = "061553be1ebf77b4d41758e061e730b0d69c92969b7e8ae91a6d2dbdac05957f"
PHASE5_CURRENT_DOCUMENT = "269d6137edc331494c404360a8d1ee874f142187aca519e7d349f838282b7c64"
PHASE5_CURRENT_YAML = "018642eee26d09e3bb014fa60baa0f820ab3637c9d6e349378c696a7b79d6877"
PHASE5_CURRENT_LEDGER = "560e82057dc0480a5b1fe835304ba57ed476b346a38cab6fac550298582016ea"
PHASE5_CURRENT_CHRISTMAS = "604cb78229672f570c13c9bee3f66e36049fba2dd50ebe16dde8c96c50ce63b3"
PHASE5_LEDGER_PATH = "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
PHASE5_LATIN22 = json.loads(r'''[
  {
    "key": {
      "mass": "commune-plurimorum-martyrum-3",
      "form": "",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "common",
      "masses",
      7,
      "propers",
      5
    ],
    "body": "Alleluia, alleluia. V. Te Martyrum candidatus laudat exercitus,\nDomine. Alleluia.\n",
    "body_sha256": "0c087cf38c152a856f483a806d14c4a63056ca5e38cf040e08ffcacc885bfaf0",
    "node_sha256": "4c30cba7a579a2313e2d53bae481041642f58308abb54cbf4d99ad70f225ace4",
    "yaml_slice_sha256": "8bd69432e8755c625454547cfcb47ca4cabb5ceb66fcb7a65ed25248f528c6a6",
    "predecessor_yaml_slice": "      - name: Alleluia\n        incipit: Te Martyrum candidatus\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: 1962 CMAA facsimile, artifact p. 821, printed [13]; raw text page line 27; Printed text unit\n          4264; uncited chant. Its exact body remains unavailable; no Bible passage substitutes for it.\n        ordinary_disposition:\n          kind: alternative\n          group: plurimorum-martyrum-3-post-epistle\n          option: regular\n          basis: 1962 Common opening, artifact p.809/[1], plus 1962 CMAA facsimile, artifact p. 820, printed\n            [12]; raw text page line 67 and the numbered local chant cues\n          anchor:\n            mass: commune-plurimorum-martyrum-3\n            form_id: main\n            proper: Alleluia\n            occurrence: 1\n          when:\n            fact: roman-1962-common-chant-regime\n            in:\n            - advent\n            - regular\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "1962 CMAA facsimile, artifact p. 821, printed [13]; raw text page line 27; Printed text unit 4264; uncited chant. Its exact body remains unavailable; no Bible passage substitutes for it."
    },
    "row_sha256": "ac8ac39a52d5aca48a40f3c65417a07a786b5d5e1f57fb5c03101e60975ac94c",
    "ledger_slice_sha256": "0256a7b9f74426ccce5fe67627087f0214e86766b8185041b7310ffe30faec92",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-commune-plurimorum-martyrum-3-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "nativitate-domini-octave",
      "form": "Ad tertiam Missam in die",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "christological",
      "masses",
      7,
      "forms",
      2,
      "propers",
      4
    ],
    "body": "Alleluia, alleluia. V. Dies sanctificatus illuxit nobis: venite,\ngentes, et adorate Dominum: quia hodie descendit lux magna super\nterram. Alleluia.\n",
    "body_sha256": "355b92fdc4351a3ee69c6da72b8b4833e5e965af8a2cb98877e58b23bde69176",
    "node_sha256": "e17a470e1ecb48c21e83c79145606659f1380b28a63389358e008919226e9dc3",
    "yaml_slice_sha256": "4e1bacef099a1b5fe0edc4e5c15347f74acaa251bfcb6e9b8b71eda0a93475bc",
    "predecessor_yaml_slice": "        - name: Alleluia\n          source: composed\n          text_status:\n            state: unavailable\n            scope: proper-body\n            reasons:\n            - kind: no-exemplar\n          notes: Missale Romanum 1962, artifact p. 102, printed p. 21, unit 135; source-appointed body; no exact publishable\n            exemplar is bound.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "no-exemplar"
          }
        ]
      },
      "notes": "Missale Romanum 1962, artifact p. 102, printed p. 21, unit 135; source-appointed body; no exact publishable exemplar is bound."
    },
    "row_sha256": "3ec0155be960e186ef2067fb2448bf333f4be016614005149951349ee2df7dec",
    "ledger_slice_sha256": "9fe3bce46b3255a029073fc9df0eb00fbb7129a9705602883261e57f40e5a770",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-nativitate-domini-octave-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-nativitate-domini-octave-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-nativitate-domini-octave-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "commune-unius-martyris-2",
      "form": "",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "common",
      "masses",
      2,
      "propers",
      5
    ],
    "body": "Alleluia, alleluia. V. Hic est sacerdos, quem coronavit Dominus.\nAlleluia.\n",
    "body_sha256": "5b8d34963dd1739949a0933d110cbefd33977b552741d89a66b3c5ec97cc70b2",
    "node_sha256": "01be4c9da0d5ab415e401c7373b43de8c0903b0f2638e7256cb91986691ad9bc",
    "yaml_slice_sha256": "1271e0e3d797913d9d1a29ec4d836c60850ed45e6282041b14c1d03a6253ab6b",
    "predecessor_yaml_slice": "      - name: Alleluia\n        incipit: Hic est sacerdos\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: 1962 CMAA facsimile, artifact p. 814, printed [6]; raw text page line 8; Printed text unit 4208;\n          uncited chant. Its exact body remains unavailable; no Bible passage substitutes for it.\n        ordinary_disposition:\n          kind: alternative\n          group: unius-martyris-2-post-epistle\n          option: regular\n          basis: 1962 Common opening, artifact p.809/[1], plus 1962 CMAA facsimile, artifact p. 813, printed\n            [5]; raw text page line 42 and the numbered local chant cues\n          anchor:\n            mass: commune-unius-martyris-2\n            form_id: main\n            proper: Alleluia\n            occurrence: 1\n          when:\n            fact: roman-1962-common-chant-regime\n            in:\n            - advent\n            - regular\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "1962 CMAA facsimile, artifact p. 814, printed [6]; raw text page line 8; Printed text unit 4208; uncited chant. Its exact body remains unavailable; no Bible passage substitutes for it."
    },
    "row_sha256": "68cde980a23740b034dce4fe7e74470c4b219e9246c0aba096df993b149af483",
    "ledger_slice_sha256": "17008bd627c740d618dad348a67fdfe6c9cfd80bb135c506101b601284611fbe",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-commune-unius-martyris-2-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-commune-unius-martyris-2-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-commune-unius-martyris-2-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "advent-3",
      "form": "",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      2,
      "propers",
      4
    ],
    "body": "Alleluia, alleluia. V. Excita, Domine, potentiam tuam, et veni, ut\nsalvos facias nos. Alleluia.\n",
    "body_sha256": "0188d53c71815633e8cf11e8d8a245f74e98481cafb978ebe38348733b0b3ccc",
    "node_sha256": "a617e70334803f6a0cf77cf16fd346a51552189ab94b0af729ffaf6023b87b43",
    "yaml_slice_sha256": "a5371a8f780f5ea9faba1182aeda279290d7a94133ca286aa16f2a667f0214aa",
    "predecessor_yaml_slice": "      - name: Alleluia\n        ordinary_disposition:\n          kind: conditional\n          group: advent-3-alleluia-use\n          basis: >-\n            Missale Romanum 1962 CMAA facsimile, artifact p. 86, printed p.\n            5, L column, between Gradual24 and Alleluia25:\n            on Advent ferias using this Sunday Mass only the Gradual remains;\n            omit the Alleluia and its following verse. No other Proper is changed.\n          when: {fact: roman-1962-advent-sunday-alleluia-use, in: [chant-present]}\n        incipit: Excita, Domine, potentiam tuam\n        source: composed\n        notes: 'Missale Romanum 1962, artifact p. 86, printed p. 5, unit 25: this Alleluia is printed without a Scripture\n          citation. Its literal body is not supplied by an inferred psalm reference.'\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: no-exemplar\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "no-exemplar"
          }
        ]
      },
      "notes": "Missale Romanum 1962, artifact p. 86, printed p. 5, unit 25: this Alleluia is printed without a Scripture citation. Its literal body is not supplied by an inferred psalm reference."
    },
    "row_sha256": "00a353d710ad476d372fdb80fe19a5695d735eca48d2cb315ba523384e61f059",
    "ledger_slice_sha256": "3627dc8cd7a6b601579bf150a82e437713caa75d3641d64796304c80d67d8e27",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-advent-3-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-advent-3-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-advent-3-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "easter-tuesday",
      "form": "",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      71,
      "propers",
      4
    ],
    "body": "Alleluia, alleluia. V. Surrexit Dominus de sepulcro, qui pro nobis\npependit in ligno.\n",
    "body_sha256": "a2964bcbc4d25603e63aaef01081a6db08505a9ea7cd841b206d3259e085c641",
    "node_sha256": "f7e6393a2ea14a2de322c02f2107512e96c701dd407e2980a33f34fb98cb5096",
    "yaml_slice_sha256": "f3664f5961df572fe4e3933eb534bbe73d19ad32fa678f6a45cbf7645a34dbea",
    "predecessor_yaml_slice": "      - name: Alleluia\n        incipit: Surrexit Dominus de sepulcro\n        source: composed\n        notes: Missale Romanum 1962, artifact p. 414, printed p. 333, numbered unit 1166; source-established normal appointment.\n          The printed acclamation has no biblical citation and follows Graduale1165. Exact wording remains unavailable\n          in this record.\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: no-exemplar\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "no-exemplar"
          }
        ]
      },
      "notes": "Missale Romanum 1962, artifact p. 414, printed p. 333, numbered unit 1166; source-established normal appointment. The printed acclamation has no biblical citation and follows Graduale1165. Exact wording remains unavailable in this record."
    },
    "row_sha256": "279c07e653c473ec6d50fc1b18c18b8a14769e875489fc1ca6d912d0da0e4704",
    "ledger_slice_sha256": "e51308efc2756d0bee91fe9675b16cd1055f898e3f38247ba2bac768423aeef9",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-easter-tuesday-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-easter-tuesday-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-easter-tuesday-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "easter-thursday",
      "form": "",
      "proper": "Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      73,
      "propers",
      4
    ],
    "body": "Alleluia, alleluia. V. Surrexit Christus, qui creavit omnia: et\nmisertus est humano generi.\n",
    "body_sha256": "2c0b6384f0112c7cbfdb68e5a8feeb2430673ef063f44374328df073942fd635",
    "node_sha256": "d9cbb4a81a5650a5ece51b9fbce5a2764d980585db28e698eaafee8e4444c804",
    "yaml_slice_sha256": "e7afc7e4b0659fde626c44d177848e957f446fb73345dcf7ef26e3cd212a474e",
    "predecessor_yaml_slice": "      - name: Alleluia\n        incipit: Surrexit Christus, qui creavit\n        source: composed\n        notes: Missale Romanum 1962, artifact p. 418, printed p. 337, numbered unit 1188; source-established normal appointment.\n          The printed acclamation has no biblical citation and follows Graduale1187. Exact wording remains unavailable\n          in this record.\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: no-exemplar\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "no-exemplar"
          }
        ]
      },
      "notes": "Missale Romanum 1962, artifact p. 418, printed p. 337, numbered unit 1188; source-established normal appointment. The printed acclamation has no biblical citation and follows Graduale1187. Exact wording remains unavailable in this record."
    },
    "row_sha256": "348e527222d3564a33a999fa1a45985ce353652a2e10d1e18f3517231b1a61e5",
    "ledger_slice_sha256": "99793b0bcde86d387d59914b0fcf1f070633a1aaf2f810bdc396f8fb08e7224e",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-easter-thursday-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-easter-thursday-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-easter-thursday-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "pentecost-ember-wednesday",
      "form": "",
      "proper": "Second Alleluia",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      89,
      "propers",
      6
    ],
    "body": "Alleluia, alleluia. V. Veni, Sancte Spiritus, reple tuorum corda\nfidelium: et tui amoris in eis ignem accende.\n",
    "body_sha256": "ffb81b41664b394f896ca1e4a08258361e4e605285923035f1d2f65a154ba51c",
    "node_sha256": "1c2d20b35730c89df02a499e0fb7cb3aa20e9b67bfc897e57baf529fd2501b9f",
    "yaml_slice_sha256": "10511c3bc680431fdb142bfdeadc8b8097bfd7fffee492106d7c237b5a74a363",
    "predecessor_yaml_slice": "      - name: Second Alleluia\n        incipit: Veni, Sancte Spiritus\n        source: composed\n        notes: Missale Romanum 1962, artifact p. 443, printed p. 362, numbered unit 1346; source-established normal appointment.\n          The printed invocation has no biblical citation and follows the second Lesson1345. Exact wording remains unavailable\n          in this record.\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: no-exemplar\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "no-exemplar"
          }
        ]
      },
      "notes": "Missale Romanum 1962, artifact p. 443, printed p. 362, numbered unit 1346; source-established normal appointment. The printed invocation has no biblical citation and follows the second Lesson1345. Exact wording remains unavailable in this record."
    },
    "row_sha256": "b7133d9d0540e36b7c20697fbee92fd76494efe0e7071ed3114b57316c4023ab",
    "ledger_slice_sha256": "c8aa7a2f9c532f8e5f9e8f3d69739d978efa352312ad5b5ed9542c14c726b029",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-pentecost-ember-wednesday-second-alleluia",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "ash-wednesday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      22,
      "propers",
      15
    ],
    "body": "Inclinantes se, Domine, majestati tuae, propitiatus intende: ut, qui\ndivino munere sunt refecti, caelestibus semper nutriantur auxiliis.\nPer Dominum.\n",
    "body_sha256": "15ced62446f8ebd36bbb422f30e61593d6cbb73377f425949bb846028299a577",
    "node_sha256": "5d11e7c738ec0e89e5bfc94748009d93354565c417525f091a64cc507fc88e94",
    "yaml_slice_sha256": "17bd2cdfe392b8916c674037c5602819b73463caf0f7168ee26025a24a42515e",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Inclinantes se Domine\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 58, artifact PDF p. 139, numbered unit 396, R column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 58, artifact PDF p. 139, numbered unit 396, R column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "dd3048e399e2cb65244bc269eef7488550f12dbc301000413663029c6e927e8b",
    "ledger_slice_sha256": "db4e5ab25cb26617fa7924383859584fab519ffd112fdccfceec9a72eb2673ba",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-ash-wednesday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-ash-wednesday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-ash-wednesday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "saturday-after-ash-wednesday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      25,
      "propers",
      9
    ],
    "body": "Fideles tui, Deus, per tua dona firmentur: ut eadem et percipiendo\nrequirant, et quaerendo sine fine percipiant. Per Dominum.\n",
    "body_sha256": "8cf8402809c00ebb85b5900f9d3b16ec2af5f1628ee9edee60df71e4172d82d0",
    "node_sha256": "72e4fbb97a69f589cdbf6d8e76737715a4d686da0000c88b62e1cfc3fff0e508",
    "yaml_slice_sha256": "052cb5815844373608e8102341876e4bc9926c7a36b49baabb6c104468b1650a",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Fideles tui Deus\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 63, artifact PDF p. 144, numbered unit 427, R column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 63, artifact PDF p. 144, numbered unit 427, R column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "b099173cc2999ae5b1e4796f781c10a36bbcd41fc199fc204b7fe86438d2feda",
    "ledger_slice_sha256": "87863b2a2e317b71f82f517c8e754a8baf68798bc893dfc37ba582f000bf96ac",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "sacred-heart",
      "form": "",
      "proper": "Collect",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      97,
      "propers",
      1
    ],
    "body": "Deus, qui nobis, in Corde Filii tui, nostris vulnerato peccatis,\ninfinitos dilectionis thesauros misericorditer largiri dignaris:\nconcede, quaesumus; ut, illi devotum pietatis nostrae praestantes\nobsequium, dignae quoque satisfactionis exhibeamus officium. Per\neundem Dominum.\n",
    "body_sha256": "c7d00a4a72b472208ac1bc38e4479eb3c80e286b498734de8c024f8f3e4ce59d",
    "node_sha256": "c18d043c92921bfe3baa1d6f24f4130cae8a0d4429ad8d3aa3a7abe3e21ee580",
    "yaml_slice_sha256": "96726fcdcb6e3f05b24998ac2df09f273fd14662167a63a0a2a55cb2474d2d7c",
    "predecessor_yaml_slice": "      - name: Collect\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n            - kind: witness-gap\n              source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      }
    },
    "row_sha256": "d6f1a43a3ebdaca9969f05afbd8ec7f3c45b4ef9276a61e1fea57f2461b64ac5",
    "ledger_slice_sha256": "d79ff54e5a8dea6832f315762269f185cdc11ce7bd2bb58e941eeea4c0bf48b7",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-sacred-heart-collect",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-sacred-heart-collect",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-sacred-heart-collect",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  },
  {
    "key": {
      "mass": "s-teresiae-a-iesu-infante-virginis",
      "form": "",
      "proper": "Postcommunion",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      9
    ],
    "body": "Illo nos, Domine, amoris igne caeleste mysterium inflammet: quo sancta\nTeresia Virgo tua se tibi pro hominibus caritatis victimam devovit.\nPer Dominum nostrum.\n",
    "body_sha256": "bd156cf03db2181218acba1a033684509dd2867ea60aeedcd169291c1f9e7e15",
    "node_sha256": "f4a7f48a61ac644c41d83da4dab3b0574378c2f4870bedef8b87fd62342bf590",
    "yaml_slice_sha256": "94affaf0d78bebbf368c6b872732a679b42031abd6ddf6dbe91f252acd9b5198",
    "predecessor_yaml_slice": "      - name: Postcommunion\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n            - kind: witness-gap\n              source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      }
    },
    "row_sha256": "975b1711bd2474f1431bedef17c559bdecfaad5eafcfd6f61e4c64f7b3124beb",
    "ledger_slice_sha256": "1cc35b64e40fb696878248fdf2f1648a7d511143f1f9ddf6220bc98f87b67314",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  },
  {
    "key": {
      "mass": "s-teresiae-a-iesu-infante-virginis",
      "form": "",
      "proper": "Secret",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      7
    ],
    "body": "Sacrificium nostrum tibi, Domine, quaesumus, sanctae Teresiae Virginis\ntuae precatio sancta conciliet: ut, in cujus honore solemniter\nexhibetur, ejus meritis efficiatur acceptum. Per Dominum nostrum.\n",
    "body_sha256": "44ae620a19de8395079129c2c441a1d94df62b63057d618cf37682b000ee32f1",
    "node_sha256": "7ab509243a91297effeb587718d951410bb02d70b24a3e92d97cb8bfebd7a3ce",
    "yaml_slice_sha256": "9bff7331f353b3caa582b44204e1ee129a5fac94ec6648eb052e5136a18b9eb8",
    "predecessor_yaml_slice": "      - name: Secret\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n            - kind: witness-gap\n              source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      }
    },
    "row_sha256": "42945d65ee596ce4020c00a5ee2225febfaecfbe64ee6d6ea62a2e9bd57f991f",
    "ledger_slice_sha256": "50f790e4a17669d799139f64cb5b8524542730c7d94b50ab1532ea672c66a301",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  },
  {
    "key": {
      "mass": "lent-1-thursday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      30,
      "propers",
      9
    ],
    "body": "Da, quaesumus, Domine, populis christianis: et, quae profitentur,\nagnoscere, et caeleste munus diligere, quod frequentant. Per Dominum.\n",
    "body_sha256": "804b104f1f85757f51eddf555e651d41ab772bc9faf2ec636f436e400174548a",
    "node_sha256": "0d408afd82f30408789747586e67ad1f3e5bbf034a5fee132cb02e15e844bb4a",
    "yaml_slice_sha256": "a936e64aaa77552035e4630e74e52943e37a8ad1d5d02b61067618265c016cba",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Da quaesumus Domine\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 71, artifact PDF p. 152, numbered unit 481, R column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 71, artifact PDF p. 152, numbered unit 481, R column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "3355b18d454c2a5d33e2926560d5f1b62844f3fa6e5c7dfcb65463ac92ddebcb",
    "ledger_slice_sha256": "803f21e65d63787cb964ecdcad6ba5716590a99513094bb106562bfa9d2f321d",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-thursday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022"
    ]
  },
  {
    "key": {
      "mass": "sacred-heart",
      "form": "",
      "proper": "Secret",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      97,
      "propers",
      7
    ],
    "body": "Respice, quaesumus, Domine, ad ineffabilem Cordis dilecti Filii tui\ncaritatem: ut quod offerimus sit tibi munus acceptum et nostrorum\nexpiatio delictorum. Per eundem Dominum.\n",
    "body_sha256": "44ed87c1a9536993d8371d13e421744097960aa62da90162f1f78d3da287dc98",
    "node_sha256": "1d991da8a5aa60a4f7d6bab5ec9967f028f42575da3d7c088e6bc816f5a3aa3a",
    "yaml_slice_sha256": "a67663f54a00d3553f14d6b0d9f708066b365284301caa300901472bc9608cfe",
    "predecessor_yaml_slice": "      - name: Secret\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n            - kind: witness-gap\n              source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      }
    },
    "row_sha256": "4b41ae8ae6c93dceb5b06f213832af1ffb22092d10e100fb4e771502820cb0c4",
    "ledger_slice_sha256": "dc062f68b5cc51068f301ac5ec05ba6e5b72e356df39da51a7672a241f9757fd",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-sacred-heart-secret",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-sacred-heart-secret",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-sacred-heart-secret",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  },
  {
    "key": {
      "mass": "thursday-after-ash-wednesday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      23,
      "propers",
      9
    ],
    "body": "Parce, Domine, parce populo tuo: ut, dignis flagellationibus\ncastigatus, in tua miseratione respiret. Per Dominum nostrum.\n",
    "body_sha256": "96fa3323adf06aa40efee765bada25fdee952b141f7964a0b946be17d042d74b",
    "node_sha256": "30f05648817a74171608ee7ccf664d32aa67b6b3d71049d9fe42539cc110c8d2",
    "yaml_slice_sha256": "33be77340e7aeb19591c839e83e85e4195dce552a6405a80fe462d94002ff582",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Parce Domine parce\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 60, artifact PDF p. 141, numbered unit 406, L column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 60, artifact PDF p. 141, numbered unit 406, L column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "debe76042685bba454badcc8d02ab09bcfe55a9a65e6eee905899e0aa76b3e51",
    "ledger_slice_sha256": "6889a6b6c6b50aaf65d3bc88f8452783f2572166fe0e86aa84decbb12b4ce45e",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "friday-after-ash-wednesday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      24,
      "propers",
      10
    ],
    "body": "Tuere, Domine, populum tuum, et ab omnibus peccatis clementer emunda:\nquia nulla ei nocebit adversitas, si nulla ei dominetur iniquitas. Per\nDominum nostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat\nin unitate.\n",
    "body_sha256": "fde9e9ecb8760757adafae9aaece1cb2809a1b845f64df6c6376b21bf576a074",
    "node_sha256": "1c927bc2cceef606b2d4104436bf6f023f94162cedbd5aacfe3e31969e1e6739",
    "yaml_slice_sha256": "6fb695c90d24f17945de55b56c99667b8b71cb930803b17a04c388ac333c2030",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Tuere Domine\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 62, artifact PDF p. 143, numbered unit 417, L column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 62, artifact PDF p. 143, numbered unit 417, L column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "4407db416dcf903026c965bd0d419b461d68f4b5492c69b32a5df5b0f311b3c1",
    "ledger_slice_sha256": "abf0a785a925c6d5a4f499c2089cbf90013a4a9daadfb70248b53354364b1203",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-friday-after-ash-wednesday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "lent-1-monday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      27,
      "propers",
      10
    ],
    "body": "Absolve, quaesumus, Domine, nostrorum vincula peccatorum: et, quidquid\npro eis meremur, propitiatus averte. Per Dominum nostrum Jesum\nChristum, Filium tuum: Qui tecum vivit et regnat in unitate.\n",
    "body_sha256": "d3ccb3ddbe69bf7e9c146fb21f63fc621019632045966faa0715e694116bb1a0",
    "node_sha256": "34e3ebcc2d118bd44094e9dd988d4f03f7264b659afac6f6a4a81fd6436293df",
    "yaml_slice_sha256": "6fdd0c5036df0d60e8475ad903335bc1c3c7020b94bfc0dc77c3806dfe9cd093",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Absolve quaesumus\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 66, artifact PDF p. 147, numbered unit 448, R column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 66, artifact PDF p. 147, numbered unit 448, R column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "f07d8dabe0c29d88b077a0db93a93f500f3425f15ccdd31c15a19f659411875a",
    "ledger_slice_sha256": "9e60e099a3662d0279ada4dfcd216506bcf9de4230cc72f808556976a51149cb",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-monday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-monday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-monday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "lent-1-ember-wednesday",
      "form": "",
      "proper": "Oratio",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      29,
      "propers",
      4
    ],
    "body": "Devotionem populi tui, quaesumus, Domine, benignus intende: ut, qui\nper abstinentiam macerantur in corpore, per fructum boni operis\nreficiantur in mente. Per Dominum nostrum Jesum Christum, Filium tuum:\nQui tecum vivit et regnat in unitate.\n",
    "body_sha256": "49ca63839813f8f0be869fe588411b9e7801d2b869b5cd3ff41b4232003f817c",
    "node_sha256": "9025ae2797305452c9f2ff84a6f4637f17dddacadf63dfd747c2039fbcd4b8c9",
    "yaml_slice_sha256": "300c5b4b32a6180bb243d0e89f58625328b1d8366e43884b17fbf9984d66b8b2",
    "predecessor_yaml_slice": "      - name: Oratio\n        incipit: Devotionem populi\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 68, artifact PDF p. 149, numbered unit 463, R column.\n          The Missal places this prayer after the First Gradual and before the Second Lesson.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 68, artifact PDF p. 149, numbered unit 463, R column. The Missal places this prayer after the First Gradual and before the Second Lesson."
    },
    "row_sha256": "a3f03a34485b3f9b0bf2afc3ae595137e64f21925e4a06c31963977a789449b1",
    "ledger_slice_sha256": "44d681ee151e996dc9e2069ec28cb3ed7252b4e40aa6425e7a21ff1defdb9ffb",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-ember-wednesday-oratio",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-ember-wednesday-oratio",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-ember-wednesday-oratio",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "lent-1-ember-wednesday",
      "form": "",
      "proper": "Oratio super populum",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "seasonal",
      "masses",
      29,
      "propers",
      12
    ],
    "body": "Mentes nostras, quaesumus, Domine, lumine tuae claritatis illustra: ut\nvidere possimus, quae agenda sunt; et, quae recta sunt, agere\nvaleamus. Per Dominum nostrum.\n",
    "body_sha256": "6607863842ea49d0be968e7d46bdfb007173bdd1d545e7547a61e99504cc1670",
    "node_sha256": "6a88b56f1301ffa73f46a15d6196325a6be1e6115cb36414878c39c0ce0d9686",
    "yaml_slice_sha256": "ddfcdaed186b64229a80930a2bc9310322f900ec4cf1d4bbb48fd891c30d5a05",
    "predecessor_yaml_slice": "      - name: Oratio super populum\n        incipit: Mentes nostras\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: witness-gap\n            source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n        notes: Missale Romanum 1962, Proprium de tempore, printed p. 70, artifact PDF p. 151, numbered unit 471, L column.\n          The Missal places this prayer after the Postcommunion, under the direction Super populum.\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      },
      "notes": "Missale Romanum 1962, Proprium de tempore, printed p. 70, artifact PDF p. 151, numbered unit 471, L column. The Missal places this prayer after the Postcommunion, under the direction Super populum."
    },
    "row_sha256": "0a80a753cb299d90c04a82d8570a38675c94f7ae6ab4f1c05447a54845c16bd0",
    "ledger_slice_sha256": "7e55cc1606ea92c8f24effb51795551d2668b67e8ec2a7014b60df6732d0515c",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-lent-1-ember-wednesday-oratio-super-populum",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "s-teresiae-a-iesu-infante-virginis",
      "form": "",
      "proper": "Collect",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "sanctoral",
      "masses",
      234,
      "propers",
      1
    ],
    "body": "Domine, qui dixisti: Nisi efficiamini sicut parvuli, non intrabitis in\nregnum caelorum: da nobis, quaesumus; ita sanctae Teresiae Virginis in\nhumilitate et simplicitate cordis vestigia sectari, ut praemia\nconsequamur aeterna: Qui vivis et regnas cum Deo Patre in unitate.\n",
    "body_sha256": "af5711fcc13cd77c33978d3406ffa1cb0295a737023cbb6ca95c31531e62c66f",
    "node_sha256": "451a96faf5ddb86f6c99db7d8b17e5800b2bc482d52b073d8b50276e823d9e7f",
    "yaml_slice_sha256": "7c3024bf2c1ad2aedd08ec283d11c86dfe40a6f2232240f7bab7d9e5fbe04511",
    "predecessor_yaml_slice": "      - name: Collect\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n            - kind: witness-gap\n              source_id: artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "witness-gap",
            "source_id": "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
          }
        ]
      }
    },
    "row_sha256": "f810c4f82d8497504c3d0395c8b83db438f222526d54ca2e95a6289913b415d6",
    "ledger_slice_sha256": "02d24c5b94ee79366add2a896ebd4976651969b08f0f176a653157419f251639",
    "predecessor_ledger_slice": "",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022",
      "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022"
    ]
  },
  {
    "key": {
      "mass": "s-ioannis-a-cruce-confessoris-ecclesiae",
      "form": "",
      "proper": "Collect",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "sanctoral",
      "masses",
      283,
      "propers",
      0
    ],
    "body": "Deus, qui sanctum Joannem Confessorem tuum atque Doctorem perfectae\nsui abnegationis et Crucis amatorem eximium effecisti: concede; ut,\nejus imitationi jugiter inhaerentes, gloriam assequamur aeternam. Per\nDominum nostrum.\n",
    "body_sha256": "6434b8c24e32369497ab4c99386ebb42cc16322972a2af680a2d735f315779bb",
    "node_sha256": "d8249db6555398b4cc17884c5b37fcc5f771544f8569562a3fcd9d6a289cc5a1",
    "yaml_slice_sha256": "5b505c22cd58e6a93ab00990b4fc03637ee3cd055cbb457dcbd2cebc3600ad5a",
    "predecessor_yaml_slice": "      - name: Collect\n        source: composed\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: rights-withheld\n            source_id: edition.catholic-church.missale-romanum.vatican-typica-1962\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "rights-withheld",
            "source_id": "edition.catholic-church.missale-romanum.vatican-typica-1962"
          }
        ]
      }
    },
    "row_sha256": "282d8fe5428a8bfe436df0bba4dc8a58e22c54bd9816eef11b94c5e2be85e778",
    "ledger_slice_sha256": "3f16ff93fe46a6be2671d69651a3856b29a36d42a85849488ca7c530afa20821",
    "predecessor_ledger_slice": "[[entries]]\nmass = \"s-ioannis-a-cruce-confessoris-ecclesiae\"\nform = \"\"\nproper = \"Collect\"\ncourse = \"\"\ncycle = \"\"\noccurrence = 1\ntext_sha256 = \"966103039dbcb44a41cca1c03603c1e67bc201b6a8b3cd4051f729770ddd677e\"\nbody_status = \"removed\"\n\n",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  },
  {
    "key": {
      "mass": "s-ioannis-mariae-vianney-confessoris",
      "form": "",
      "proper": "Collect",
      "course": "",
      "cycle": "",
      "occurrence": 1
    },
    "yaml_path": [
      "sections",
      "sanctoral",
      "masses",
      178,
      "propers",
      0
    ],
    "body": "Omnipotens et misericors Deus, qui sanctum Joannem Mariam pastorali\nstudio et jugi orationis ac paenitentiae ardore mirabilem effecisti:\nda, quaesumus; ut, ejus exemplo et intercessione, animas fratrum\nlucrari Christo, et cum eis aeternam gloriam consequi valeamus. Per\neundem Dominum.\n",
    "body_sha256": "12105ba3649c6e5b37c48e65fd93475d55706432eb8485f495625e32b20ddcb4",
    "node_sha256": "2861b35393fa8b4334b8e7957b83c8fe2fff3265e2c3dca499dc21acff05748f",
    "yaml_slice_sha256": "629afd66f7469a82411004e17fa698791821e1e7ad4b0a58ddbf3eaf8ba46c3e",
    "predecessor_yaml_slice": "      - name: Collect\n        incipit: Omnipotens et misericors Deus\n        source: composed\n        notes: Printed p. 618, no. 3305, marked P.\n        text_status:\n          state: unavailable\n          scope: proper-body\n          reasons:\n          - kind: rights-withheld\n            source_id: edition.catholic-church.missale-romanum.vatican-typica-1962\n",
    "predecessor_fields": {
      "text_status": {
        "state": "unavailable",
        "scope": "proper-body",
        "reasons": [
          {
            "kind": "rights-withheld",
            "source_id": "edition.catholic-church.missale-romanum.vatican-typica-1962"
          }
        ]
      },
      "notes": "Printed p. 618, no. 3305, marked P."
    },
    "row_sha256": "4e96418e0099a80fb5742e98440bb51c5f5cf26a528f7213db8b146a586eb918",
    "ledger_slice_sha256": "e10b48fa580002a110be3986d915352057048aff5432bce827696c594089d6e1",
    "predecessor_ledger_slice": "[[entries]]\nmass = \"s-ioannis-mariae-vianney-confessoris\"\nform = \"\"\nproper = \"Collect\"\ncourse = \"\"\ncycle = \"\"\noccurrence = 1\ntext_sha256 = \"e42c126f04943ce03e2b50e8f6ccd832e36985beb23041a1e5830c3b889120db\"\nbody_status = \"removed\"\nprovenance_status = \"collated\"\nsource_id = \"artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf\"\nsource_date = \"1962\"\nlocator = \"1962 printed p. 618, collect no. 3305; artifact PDF p. 699\"\nrelationship = \"collated-non-exact\"\nverification_source_id = \"passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.john-mary-vianney-collect\"\nverification_locator = \"Lasance printed p. 1149; Internet Archive leaf n1141; facsimile artifact PDF p. 1142\"\ntransformations = [\"join-line-breaks\"]\nprovenance_evidence = \"Exact Vatican 1962 and Lasance page images inspected; the registered Lasance passage records the variant.\"\nprovenance_authority = \"Human page-image collation\"\nprovenance_confidence = \"high\"\npublication_status = \"withheld\"\npublication_basis = \"non-exact-historical-witness\"\nsurfaces = []\nnote = \"HOLD: Lasance reads `beatum Joannem Mariam` where the target reads `sanctum Ioannem Mariam`; its `poenitentiae` versus target `paenitentiae` is separately orthographic. The historical witness does not establish the target wording.\"\n\n",
    "source_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "verification_source_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "historical_passage_id": "passage.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect",
    "publication_source_ids": [
      "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022",
      "artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022"
    ]
  }
]''')
PHASE5_SOURCE_POSTIMAGES = json.loads(r'''{
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-commune-plurimorum-martyrum-3-alleluia.toml": "00b44686e8f989337785cd6cec81cc090f62d67cd8ff3ccaefadddfc57ea50cb",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-commune-plurimorum-martyrum-3-alleluia.toml": "96994cf5792758abe15be4800154e79a3e18f40be20e72e6a0c782a86fbd9015",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-commune-plurimorum-martyrum-3-alleluia.toml": "b0774a5f5520a7ffdd1ed09589234ecd5ec12e6395a5903317dc10a891f464bb",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-nativitate-domini-octave-alleluia.toml": "5fc7c47de63cfa27ea1f57c9480483c4c8dd845bbb8c9d36544fb9ed703da31b",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-nativitate-domini-octave-alleluia.toml": "ebe707b83387981cafa039b5466b4213cada67a517a5ff1421c31094d6b27cb7",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-nativitate-domini-octave-alleluia.toml": "e9811a314ac3c3872307f92cd6e6463b872fe22371b50307a34f7e9ebe831607",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-commune-unius-martyris-2-alleluia.toml": "4768e961f8359b902084a0987daf0088de1be02d2dbc9f7ddb4e62d0ec7b868b",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-commune-unius-martyris-2-alleluia.toml": "50f61a7d0e34f528ab5b79fbff6f6e5328a5db0a11481b4f66f097d7fbc34c0e",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-commune-unius-martyris-2-alleluia.toml": "ef484349960f11158012b71a51be9b9f7422acdadc5b09c3d292ff074585967a",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-advent-3-alleluia.toml": "c9718e76a0696c529a9b0ce21c79d2b7b1aebe5a3532464dbc3ede2a3e4dbb59",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-advent-3-alleluia.toml": "a50a239c801a862b9a5473661076e831b7fc6544ca342944a7fe1d23541e1168",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-advent-3-alleluia.toml": "f3b08797bb7d14c9107fdfb72276c6baf5bc9a7ac574829da996568128ce13aa",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-easter-tuesday-alleluia.toml": "1cd74a2cbbd133071319fb5f6df84249feeca32dcc87e132524c5b20b0296231",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-easter-tuesday-alleluia.toml": "72fdb4bca8e3d8438b0952edd240681cfb907d688aef232831437ab80b29de50",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-easter-tuesday-alleluia.toml": "6b3d9e417d29f507c8b48850f412a014d2391d75b89cd973670e825686184727",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-easter-thursday-alleluia.toml": "b3f6e968ac15307a7a602b8a2270115f2452157891a431376c53fdb694f5df9c",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-easter-thursday-alleluia.toml": "e0020c3622b8ba19392551bbf39cf1557247b7f633c18461a6f64745c3751983",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-easter-thursday-alleluia.toml": "fbbf5f48bddaf922d82ea7b6fd23b25f99460391097e958124a52aeef2984f70",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-pentecost-ember-wednesday-second-alleluia.toml": "c3d71b6fe083c589a4185dbb0ca293e91965bbd0203d7de00c6c971be14abca4",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-pentecost-ember-wednesday-second-alleluia.toml": "b5794e5860a78bcc0ba803ba1d68111cbeab2ccd60fd93fd44ca8bd19fafb1d1",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-pentecost-ember-wednesday-second-alleluia.toml": "8a139d49fcda228cc7b1e54737eb42ca996f26b5605f1f773ada23cf76702367",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-ash-wednesday-oratio-super-populum.toml": "70ada56149288d9144e325515cbcf749a9e3f01b90540ae4177b3221e480ca74",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-ash-wednesday-oratio-super-populum.toml": "bf876ddff14da29558708f455f742763287ae1c127d8f05c3cc32b4ac5fdc8dd",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-ash-wednesday-oratio-super-populum.toml": "4dccbb0595a7ffaada1d0a7bb885b0810c2f493358022b0a558162c65a8c2783",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum.toml": "8f54a39185ae1c8f8cfbb4aa66b7e89d8fe87493aaeef3c8af20c3002db56b14",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum.toml": "00b84be4e1e88c3ba0f2c2a9c0d964bf7415ebcf05d9076954fd00bb93c1897a",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-saturday-after-ash-wednesday-oratio-super-populum.toml": "a4ca3f5c05afc7aafc7942eafdccfb01f545e4990cb54c43d57207f37f894da8",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-sacred-heart-collect.toml": "2291d0cf04f9ba59f0ea9e152ab8d7c5df53d122fd07376a8624b7611a68a792",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-sacred-heart-collect.toml": "7b7a640b2df3b9f7a9b9ad6203dad59d8f5b9c1f789c2a3840c008209b930980",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-sacred-heart-collect.toml": "4e7c100c718dd67a8be4cf99eed8caa2ed44c7d494573a73c0d25438b4e5dc1c",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion.toml": "a6953d0a26249465a2c3df510b79aca88eda491cd69b2002a936748ad7680ffd",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion.toml": "977ed459ebb207e4cdeecaac3d60bac4763e51f3c3610cffb76b83af7563b658",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-postcommunion.toml": "439fe68ee9cf65f180c5aa8c10f6770249daaeb3c1b7e26d634d1e2e693eb926",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret.toml": "d3ae5d9f5d1296a06e5001781efe4de1653cb9e8a26a0ca9117c66e51a79d5bc",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret.toml": "7423603f70b6488f4e50198b8042e9ca23590901f8d87bc03d4d8a1cdfc8a138",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-secret.toml": "e30c6407098606d9f9c2043afa9bc3cb48031503912887c1e87c84268ec2b6d0",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-lent-1-thursday-oratio-super-populum.toml": "29d626d5e248b723ba22d304bdf8f4c3bbbde3de4aae71b4a5fb8950d0748086",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-lent-1-thursday-oratio-super-populum.toml": "da12ae553397246a00f76e87dcb94ae5d38a4601d628a431f30cd425062fd97f",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-lent-1-thursday-oratio-super-populum.toml": "12a9f31356211e49e452f2da57100eb9d46c3e5d77234ab80717cd9f336149a3",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-sacred-heart-secret.toml": "04dc88995a448a93e9f76af34b68b46bbaf8e1fdb68fcf66fed9867b0ecf0836",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-sacred-heart-secret.toml": "b90d4bb75ff3d3d7a9efb87a9da700510f2ff6d3738b67a25e3bad9f47b960a5",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-sacred-heart-secret.toml": "c2e51ac5f7a7061dcf780944b28b6a6215b50b301e4f77d640f39677f5c9c115",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum.toml": "86e833af127405a9190ef036a35ece7d29b77e1221d5dafe6b45f502988dc7f1",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum.toml": "a73433d7b26654f111f1db5da9a2bd47f9b7ff72f5f7cdc07af4f87aa1ea5f5a",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-thursday-after-ash-wednesday-oratio-super-populum.toml": "f318711a42497ade9f00c1b324b0e28cd39ee4a83c2bbbff93fd29d30286ddd3",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-friday-after-ash-wednesday-oratio-super-populum.toml": "a680dbf919f3763dd0f6b311162d9553995caa99a76a3fc35f9fc4b20f1841c9",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-friday-after-ash-wednesday-oratio-super-populum.toml": "02bd79a906797baa2141d2eb267e0e2ca0e4e847b7df55b87fced6fa19ac9b36",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-friday-after-ash-wednesday-oratio-super-populum.toml": "d9073cfa85efeca6a163eb4c1ad24dd098cdfd58f9434bea7384ec0ecd13f61e",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-lent-1-monday-oratio-super-populum.toml": "07659342e40347ff0fd4438c25a45f3a9b3359bac615e3879dae473ab9feba3b",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-lent-1-monday-oratio-super-populum.toml": "2c0d1ff00d5cc6f3e5abcc7fefdc0801b56a051482adc1f670404fcbfa2d19ab",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-lent-1-monday-oratio-super-populum.toml": "c7c6f1b266580339242b8947d3a5bd8ad2086c438e72b133fb17638c353cd8cd",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-lent-1-ember-wednesday-oratio.toml": "8af42cdd524259bab19fd2be187ffc72b3bfe9bf692178e349795f012e9874a5",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-lent-1-ember-wednesday-oratio.toml": "9b2fc4c75402659f9ddcb111804555a62bfeed7dcce4453975e502a585271179",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-lent-1-ember-wednesday-oratio.toml": "4493d89ca2a874e3f8c65ada1ae98b084bd3aa6aab60c9cfe7aee6bcb7ebb947",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-lent-1-ember-wednesday-oratio-super-populum.toml": "c98d5700377897c11ac25351b87a41787622202933daa2248dcd2d82248e6d99",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-lent-1-ember-wednesday-oratio-super-populum.toml": "497c1c736248ab135db64949890a18af21bf7b3f6977c7359eb75ea8d194f358",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-lent-1-ember-wednesday-oratio-super-populum.toml": "e4338902a879d6e5ad4b865de80327652ae1b2f5204974ff4554debb653c791a",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect.toml": "9eac8521a42a331bf6d2f834ba33292b638f48a76c1ee929907ec2492f5452bb",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect.toml": "a7659cf481f25a02691ed4234282d77ac0a097019f09d015271ab837e7a781e3",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-s-teresiae-a-iesu-infante-virginis-collect.toml": "42d4f24892e44db2a57039d0aa22da4ad47f17f8b3c9e1029c8d8a2809602a74",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect.toml": "bc96b48c32db3ba499f3a3f7a9e977d1222a6cc64f41570c73aaf229779fbcd0",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect.toml": "d9c9fc23854068008c7a8810065ad9a015cdc6ca18dcf4111b6838a4a042cf16",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-s-ioannis-a-cruce-confessoris-ecclesiae-collect.toml": "7dcbb0003038b88f5f6f3c8846c8a425509a176a43519980e8efcd6fc12fa1bf",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/passages/phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect.toml": "8c60e97e55812c26fb3cab8f3ecced804b9221c06dc39a844504f20e363b2c4f",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect.toml": "706e27d9c00ba544c33b198fe5730465ec9aecfacec2adf5509f00035927e160",
  "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-latin22-s-ioannis-mariae-vianney-confessoris-collect.toml": "7cf4aff8ae24d51051baf9527cf098412d14992df14f098289bfcd919edb8e0e",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase5-latin22-petitions-and-formulas-20261022/source.pdf": "5d088d757984a53622d0b3cd763390204986df08e867241ad546bbee891283e1",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase5-latin22-petitions-and-formulas-20261022/artifact.toml": "c1c852372738ede0ef22b54b1f68eebee847068d4289590c98a1f630d3919c6b",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/artifacts/phase5-latin22-seven-historical-prayers-20261022/latin-only.txt": "ba9e819046bfea45167b7ba99f4fbd9b0fc8d0e69cc70adc9a6113dd59febc34",
  "src/sources/works/anselm-schott/das-vollstandige-romische-messbuch/editions/herder-second-revised-1929/artifacts/phase5-latin22-seven-historical-prayers-20261022/artifact.toml": "2dac4bf0afbb5ef02dc96cf61f176c558b2c6853d5194a5bb6ac6e873ad8a925",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase5-latin22-conclusion-authority-20261022/latin-only.txt": "45634a9b0825436ff735d14d49b10634cb6ffde35196bba28bf5795a56079ad8",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase5-latin22-conclusion-authority-20261022/artifact.toml": "a01e28a406a96f333288b6a2a2c41ac53c333847fdf6b7c4568a1e12f8ec8b85",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-pustet-projection-20261022/latin.txt": "f6993617fed59176e4e527f4c47c853b3e80b01f3e4fd61dfc41e68c8ef7661d",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-pustet-projection-20261022/artifact.toml": "3a2f7db77c27327023cff64302cdb2434d245e58c5ba9d768321d88bf58f65e9",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-schott-projection-20261022/latin.txt": "dab1c4edc0d73c87a91406deb5c6e2178f8bd6ace6b505932ff7b615f47431d4",
  "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase5-latin22-schott-projection-20261022/artifact.toml": "ffd5b44b78a809b5951b25aadfeae1c69a3cb8b13cbc9102d9bbce41448ad6e6",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-rubricae-generales-17.toml": "28a1a6022a99f92f49f87efc66c0a6a681ff9dbdc28dce780e7416684c666125",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-ritus-celebrandi-v-1.toml": "527eba6e148895eae0edd1ba489ae5c8dd530aa653ac47f92aa282d3746fccb0",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-father-through-son.toml": "a8d8f8a89238272c612bbc871edaca4262c86f378b956a75937d6b4c14076bfe",
  "src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase5-latin22-son-addressed.toml": "525673d47e3177e65f6c11569c1d9bf35f6d95e2c90301c9f90744b3ea144023"
}''')

def _phase5_require(condition, label):
    if not condition:
        raise AssertionError("Phase5 Latin22 authority mismatch: " + label)


def _phase5_at(value, path):
    for part in path:
        value = value[part]
    return value


def _phase5_key(row):
    return LatinKey(*(row[field] for field in
                      ("mass", "form", "proper", "course", "cycle", "occurrence")))


def _phase5_source_postimages():
    # Frozen from the independently accepted corrected source, not a live oracle.
    for path, expected in PHASE5_SOURCE_POSTIMAGES.items():
        _phase5_require(digest((ROOT / path).read_bytes()) == expected, path)


def _phase5_validate_node(node, spec):
    _phase5_require(digest(canonical(node)) == spec["node_sha256"],
                    str(spec["key"]) + " full node/wrapper/notes")
    _phase5_require(node.get("text") == spec["body"] and
                    digest(node["text"]) == spec["body_sha256"],
                    str(spec["key"]) + " full body")


def _phase5_validate_row(row, spec):
    _phase5_require(_phase5_key(row) == _phase5_key(spec["key"]),
                    "six-field ledger owner")
    _phase5_require(digest(canonical(row)) == spec["row_sha256"],
                    str(spec["key"]) + " full provenance/publication row")


def phase5_owner(document, key, records):
    """Positive whole-body/source/publication oracle for one exact accepted owner."""
    specs = [s for s in PHASE5_LATIN22 if _phase5_key(s["key"]) == key]
    _phase5_require(len(specs) == 1, "unaccepted owner")
    spec = specs[0]
    _phase5_validate_node(_phase5_at(document, spec["yaml_path"]), spec)
    matches = [(body, state) for owner, body, state in body_owners(document)
               if owner == key]
    _phase5_require(matches == [(spec["body"], "present")],
                    "six-field calendar owner " + str(key))
    _phase5_validate_row(records[key], spec)
    _phase5_source_postimages()
    _phase5_require(decision_for(key, spec["body"], records).permits(SURFACES),
                    "accepted body must be publishable")
    _phase5_require(not decision_for(key, "Mutatum " + spec["body"],
                                    records).permits(SURFACES),
                    "damaged body must be refused")
    return spec


def _phase5_restore_fields(node, spec):
    # No source, role, form, disposition, incipit, or other field is masked.
    for field in ("text", "text_status", "notes"):
        node.pop(field, None)
    node.update(copy.deepcopy(spec["predecessor_fields"]))


def phase5_predecessor_document(document):
    """Validate the entire current batch before the historical Phase5 replay."""
    return _phase5_predecessor_document_legacy(BATCH_GUARDS.historical_document(document))


def _phase5_predecessor_document_legacy(document):
    """Restore Phase5 only after the public current-input check has passed."""
    owners = collections.Counter((k, body, state)
                                 for k, body, state in body_owners(document))
    for spec in PHASE5_LATIN22:
        key = _phase5_key(spec["key"])
        _phase5_validate_node(_phase5_at(document, spec["yaml_path"]), spec)
        _phase5_require(owners[(key, spec["body"], "present")] == 1,
                        "six-field calendar owner " + str(key))
    _phase5_require(digest(canonical(document)) == PHASE5_CURRENT_DOCUMENT,
                    "complete current calendar wrappers before masking")
    ledger = (ROOT / PHASE5_LEDGER_PATH).read_text()
    phase5_predecessor_ledger(ledger)
    _phase5_source_postimages()
    result = copy.deepcopy(document)
    for spec in PHASE5_LATIN22:
        _phase5_restore_fields(_phase5_at(result, spec["yaml_path"]), spec)
    _phase5_require(digest(canonical(result)) == PHASE5_PREDECESSOR_DOCUMENT,
                    "unrelated calendar node, owner, form, order or wrapper")
    return result


def phase5_predecessor_yaml(source):
    """Validate whole current raw input before replaying two historical layers."""
    return _phase5_predecessor_yaml_legacy(BATCH_GUARDS.historical_text(BATCH_GUARDS.YAML_PATH, source))


def _phase5_predecessor_yaml_legacy(source):
    """Private legacy step; public callers must supply the current input."""
    _phase5_require(digest(source) == PHASE5_CURRENT_YAML,
                    "complete current raw calendar before masking")
    _phase5_predecessor_document_legacy(yaml.load(source, Loader=yaml.CSafeLoader))
    tree = yaml.compose(source, Loader=yaml.CLoader)
    lines = source.splitlines(keepends=True)
    replacements = []
    for spec in PHASE5_LATIN22:
        node = tree
        for part in spec["yaml_path"]:
            node = (node.value[part] if isinstance(part, int) else
                    next(v for k, v in node.value if k.value == part))
        start, end = node.start_mark.line, node.end_mark.line
        _phase5_require(digest("".join(lines[start:end])) ==
                        spec["yaml_slice_sha256"], "raw YAML slice")
        replacements.append((start, end, spec["predecessor_yaml_slice"]))
    # All slices have been checked before the first replacement.
    for start, end, predecessor in sorted(replacements, reverse=True):
        lines[start:end] = [predecessor]
    result = "".join(lines)
    _phase5_require((digest(result), len(result.encode())) ==
                    (PHASE5_PREDECESSOR_YAML, 2576894), "whole predecessor YAML")
    return result


def phase5_predecessor_ledger(source):
    """Validate whole current ledger before the historical Phase5 replay."""
    return _phase5_predecessor_ledger_legacy(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH, source))


def _phase5_predecessor_ledger_legacy(source):
    """Private legacy step retaining every non-Phase5 byte."""
    parts = re.split(r"(?m)^\[\[entries\]\]\n", source)
    specs = {_phase5_key(s["key"]): s for s in PHASE5_LATIN22}
    seen = collections.Counter()
    replacements = {}
    for index, part in enumerate(parts[1:], 1):
        raw = "[[entries]]\n" + part
        row = tomllib.loads(raw)["entries"][0]
        key = _phase5_key(row)
        if key in specs:
            spec = specs[key]
            _phase5_validate_row(row, spec)
            _phase5_require(digest(raw) == spec["ledger_slice_sha256"],
                            "raw ledger row/separator")
            seen[key] += 1
            replacements[index] = spec["predecessor_ledger_slice"]
    _phase5_require(seen == collections.Counter({k: 1 for k in specs}),
                    "missing, duplicate, wrong-form or wrong-occurrence ledger owner")
    _phase5_require(digest(source) == PHASE5_CURRENT_LEDGER,
                    "complete current raw ledger before masking")
    _phase5_source_postimages()
    # Keep header, row order, separators and every unselected row verbatim.
    result = parts[0] + "".join(
        replacements.get(index, "[[entries]]\n" + part)
        for index, part in enumerate(parts[1:], 1))
    _phase5_require((digest(result), len(result.encode())) ==
                    (PHASE5_PREDECESSOR_LEDGER, 4850755),
                    "whole predecessor ledger including unrelated rows")
    return result


def phase5_predecessor_christmas(mass):
    """Only the unique named day-form Alleluia may be normalized here."""
    _phase5_require(digest(canonical(mass)) == PHASE5_CURRENT_CHRISTMAS,
                    "complete current Christmas wrapper before masking")
    spec, = [s for s in PHASE5_LATIN22
             if s["key"]["mass"] == "nativitate-domini-octave"]
    _phase5_require(mass["key"] == spec["key"]["mass"], "Christmas mass")
    day, = [f for f in mass["forms"] if f["id"] == "day" and
            f["name"] == spec["key"]["form"]]
    node, = [p for p in day["propers"] if p["name"] == "Alleluia"]
    _phase5_validate_node(node, spec)
    records, errors = read_sidecar(ROOT / PHASE5_LEDGER_PATH)
    _phase5_require(not errors, "Christmas sidecar")
    _phase5_validate_row(records[_phase5_key(spec["key"])], spec)
    _phase5_source_postimages()
    result = copy.deepcopy(mass)
    day, = [f for f in result["forms"] if f["id"] == "day"]
    node, = [p for p in day["propers"] if p["name"] == "Alleluia"]
    _phase5_restore_fields(node, spec)
    _phase5_require(digest(canonical(result)) == PHASE5_PREDECESSOR_CHRISTMAS,
                    "Christmas night/dawn/day wrappers or other roles")
    return result


class Phase5PredecessorGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.yaml_source = (ROOT / "src/sources/calendars/roman-1962/propers.yaml").read_text()
        cls.ledger_source = (ROOT / PHASE5_LEDGER_PATH).read_text()
        cls.document = yaml.load(cls.yaml_source, Loader=yaml.CSafeLoader)

    def test_exact_whole_predecessors_not_new_historical_digests(self):
        self.assertEqual(PHASE5_PREDECESSOR_YAML,
                         digest(phase5_predecessor_yaml(self.yaml_source)))
        self.assertEqual(PHASE5_PREDECESSOR_LEDGER,
                         digest(phase5_predecessor_ledger(self.ledger_source)))
        self.assertEqual((22, 20, 2), (len(PHASE5_LATIN22),
                         sum(not s["predecessor_ledger_slice"] for s in PHASE5_LATIN22),
                         sum(bool(s["predecessor_ledger_slice"]) for s in PHASE5_LATIN22)))

    def test_no_accepted_body_or_notes_can_be_damaged_before_masking(self):
        for spec in PHASE5_LATIN22:
            for field in ("text", "notes", "source"):
                with self.subTest(owner=spec["key"], field=field):
                    damaged = copy.deepcopy(self.document)
                    node = _phase5_at(damaged, spec["yaml_path"])
                    node[field] = "Mutatum " + node[field]
                    with self.assertRaises(AssertionError):
                        phase5_predecessor_document(damaged)

    def test_extra_owner_wrong_form_occurrence_and_wrapper_are_not_masked(self):
        spec = PHASE5_LATIN22[0]
        for kind in ("extra-owner", "incipit", "form-name", "form-id", "occurrence"):
            with self.subTest(kind=kind):
                damaged = copy.deepcopy(self.document)
                if kind in ("form-name", "form-id"):
                    mass = C.mass_index(damaged)["nativitate-domini-octave"]
                    day = next(f for f in mass["forms"] if f["id"] == "day")
                    day["name" if kind == "form-name" else "id"] += " mutatum"
                elif kind == "incipit":
                    _phase5_at(damaged, spec["yaml_path"])["incipit"] += " mutatum"
                else:
                    propers = _phase5_at(damaged, spec["yaml_path"][:-1])
                    node = copy.deepcopy(propers[spec["yaml_path"][-1]])
                    propers.insert(0 if kind == "occurrence" else len(propers), node)
                with self.assertRaises(AssertionError):
                    phase5_predecessor_document(damaged)

    def test_raw_yaml_order_whitespace_and_unrelated_fields_are_not_masked(self):
        for damaged in (self.yaml_source.replace("schema:", "# extra\nschema:", 1),
                        self.yaml_source.replace("Te Martyrum", "Mutatum Te Martyrum", 1)):
            with self.assertRaises(AssertionError):
                phase5_predecessor_yaml(damaged)

    def test_ledger_wrong_supplement_occurrence_extra_owner_and_unrelated_row_refused(self):
        spec = next(s for s in PHASE5_LATIN22 if len(s["publication_source_ids"]) == 3)
        parts = re.split(r"(?m)^\[\[entries\]\]\n", self.ledger_source)
        selected = next("[[entries]]\n" + p for p in parts[1:]
                        if _phase5_key(tomllib.loads("[[entries]]\n" + p)["entries"][0])
                        == _phase5_key(spec["key"]))
        mutations = {
            "supplement": self.ledger_source.replace(selected, selected.replace(
                spec["publication_source_ids"][2], spec["publication_source_ids"][1])),
            "occurrence": self.ledger_source.replace(selected, selected.replace(
                "occurrence = 1", "occurrence = 2")),
            "extra-owner": self.ledger_source + selected,
            "unrelated-row": self.ledger_source.replace("text_sha256 = \"",
                                                       "text_sha256 = \"0", 1),
            "header": "# extra\n" + self.ledger_source,
        }
        for label, damaged in mutations.items():
            with self.subTest(kind=label):
                self.assertNotEqual(damaged, self.ledger_source)
                with self.assertRaises(AssertionError):
                    phase5_predecessor_ledger(damaged)


class OctNovCommemorationSourceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT / "src/sources/calendars", "roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records, errors = read_sidecar(ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)

    def test_eighteen_exact_own_bodies_and_hash_bound_permissions(self):
        self.assertEqual((18, 8), (len(KEYS), len(MASSES)))
        counts = collections.Counter()
        for r in ORACLES:
            with self.subTest(mass=r["mass"], proper=r["proper"]):
                p = prayer(self.index, r)
                self.assertEqual(r["body"], p["text"])
                self.assertEqual(r["body_sha256"], digest(p["text"]))
                self.assertEqual("composed", p["source"])
                self.assertNotIn("text_status", p)
                self.assertNotIn("takes_from", p)
                row = self.records[latin_key(r)]
                self.assertEqual(r["body_sha256"], row["text_sha256"])
                self.assertNotIn("body_status", row)
                self.assertEqual("collated", row["provenance_status"])
                self.assertEqual("editorial-projection-exact-to-target", row["relationship"])
                self.assertEqual("public-domain", row["publication_basis"])
                self.assertEqual([PROJECT_ARTIFACT, HIST_ARTIFACT], row["publication_source_ids"])
                self.assertEqual(set(SURFACES), set(row["surfaces"]))
                self.assertTrue(decision_for(latin_key(r), p["text"], self.records).permits(SURFACES))
                changed = "Mutatum " + p["text"].split(" ", 1)[1]
                self.assertFalse(decision_for(latin_key(r), changed, self.records).permits(SURFACES))
                counts["long" if "Qui tecum vivit" in " ".join(p["text"].split()) else
                       "nostrum" if " ".join(p["text"].split()).endswith("Per Dominum nostrum.") else "short"] += 1
        self.assertEqual({"short": 12, "long": 4, "nostrum": 2}, dict(counts))

    def test_projection_artifact_and_all_eighteen_bounded_passages(self):
        artifact = record(PROJECT_ARTIFACT)
        payload = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual((PROJECT_HASH, 3084), (digest(payload), len(payload)))
        self.assertEqual(PROJECT_HASH, artifact["sha256"])
        self.assertEqual("project-created", artifact["rights_status"])
        self.assertEqual([HIST_ARTIFACT, TARGET_ARTIFACT], artifact["projected_from"])
        lines = payload.decode().splitlines(keepends=True)
        for r in ORACLES:
            row = self.records[latin_key(r)]
            expected_id = "passage." + PROJECT + ".phase2-" + r["mass"] + "-" + r["proper"].lower()
            self.assertEqual(expected_id, row["source_id"])
            p = record(expected_id)
            self.assertEqual(PROJECT_ARTIFACT, p["artifact_id"])
            self.assertEqual(PROJECT_HASH, p["artifact_sha256"])
            self.assertEqual(r["physical_line_ranges"], p["physical_line_ranges"])
            begin, end = p["physical_line_ranges"][0]
            self.assertEqual(r["body"], "".join(lines[begin - 1:end]))
            self.assertEqual("2026-10-22", p["verified_on"])

    def test_historical_payload_is_exact_fourteen_page_parented_extract(self):
        artifact = record(HIST_ARTIFACT)
        payload = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual((HIST_HASH, 2981377), (digest(payload), len(payload)))
        self.assertEqual((14, "public-domain", "tracked"),
                         (artifact["page_count"], artifact["rights_status"], artifact["storage"]))
        parent = record(artifact["derived_from"])
        self.assertEqual("363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474", parent["sha256"])
        self.assertEqual(102880787, parent["byte_size"])
        pages = [448, 450, 451, 642, 649, 650, 657, 658, 660, 661, 662, 668, 669, 670]
        self.assertIn(", ".join(map(str, pages)), artifact["transformation"])
        self.assertIn("no crop, OCR", artifact["transformation"])
        self.assertIn("Ursula", artifact["notes"])

    def test_grouped_historical_bounds_and_target_control_stay_separate(self):
        bounds = {
            "comm-ss-sergii-bacchi-marcelli-apuleii": [[4, 4]],
            "comm-ss-ursulae-ac-sociarum-virginum": [[5, 6]],
            "comm-ss-vitalis-agricolae-martyrum": [[7, 8]],
            "comm-ss-tryphonis-respicii-nymphae-virginis": [[9, 10]],
            "comm-s-mennae-martyris": [[11, 11]],
            "comm-s-felicitatis-martyris": [[12, 13]],
            "comm-s-chrysogoni-martyris": [[14, 14]],
            "comm-s-saturnini-martyris": [[1, 3]],
        }
        self.assertEqual(set(MASSES), set(bounds))
        for mass in MASSES:
            h = record("passage." + HIST + ".phase2-" + mass + "-orations-page-image-2026-10-22")
            t = record("passage." + CONTROL + ".phase2-" + mass + "-orations-recheck-2026-10-22")
            self.assertEqual((HIST_ARTIFACT, HIST_HASH, bounds[mass]),
                             (h["artifact_id"], h["artifact_sha256"], h["artifact_page_ranges"]))
            self.assertEqual(TARGET_ARTIFACT, t["artifact_id"])
            self.assertEqual("648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a", t["artifact_sha256"])
            self.assertIn("200 and 400 dpi", t["notes"])
            for r in (r for r in ORACLES if r["mass"] == mass):
                row = self.records[latin_key(r)]
                self.assertEqual(t["id"], row["verification_source_id"])
                self.assertNotIn(TARGET_ARTIFACT, row["publication_source_ids"])
                self.assertIn("no. " + r["target"]["unit"], row["verification_locator"])
                self.assertIn("PDF p. " + str(r["target"]["pdf"]), row["verification_locator"])

    def test_local_own_orations_override_common_prayers_exactly_once(self):
        for mass in MASSES:
            rows, errors = C.resolve_propers(self.document, self.index[mass])
            self.assertEqual([], errors)
            for r in (r for r in ORACLES if r["mass"] == mass):
                matches = [(p, origin) for _, p, origin in rows if p["name"] == r["proper"]]
                self.assertEqual(1, len(matches))
                self.assertIsNone(matches[0][1])
                self.assertEqual(r["body"], matches[0][0]["text"])
                self.assertFalse(any(p["name"].startswith(r["proper"] + " (") for _, p, _ in rows))

    def test_ursula_new_mame_witness_does_not_clear_old_1862_mismatch(self):
        mass = "comm-ss-ursulae-ac-sociarum-virginum"
        p = next(p for p in self.index[mass]["propers"] if p["name"] == "Postcommunion")
        # Phase3 separately supplies the complete named 1922 petition;
        # Phase2's old 1862 source failure remains a source-specific failure.
        self.assertEqual("5a5b9ed5c33e154ea2ca35320f7447da49d6100622ca563537e849b60d0137d2", digest(p["text"]))
        self.assertNotIn("text_status", p)
        row = self.records[LatinKey(mass, "", "Postcommunion", "", "", 1)]
        self.assertEqual(
            "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase3-ursula-postcommunion-page-20261022",
            row["publication_source_ids"][1])
        rows, errors = C.resolve_propers(self.document, self.index[mass])
        self.assertEqual([], errors)
        self.assertEqual([(p, None)], [(q, o) for _, q, o in rows if q["name"] == "Postcommunion"])
        historical = record("passage." + HIST + ".phase2-" + mass + "-orations-page-image-2026-10-22")
        self.assertIn("no explicit blank", historical["notes"])
        self.assertIn("lexical mismatch", historical["notes"])

    def test_no_other_calendar_words_appointments_or_contexts_change(self):
        d = phase5_predecessor_document(self.document)
        for section in d["sections"].values():
            for mass in section["masses"]:
                mass["propers"] = [p for p in mass.get("propers", [])
                                   if (mass["key"], p["name"]) not in KEYS]
                if mass["key"] == "comm-s-saturnini-martyris":
                    mass.pop("notes", None)
        self.assertEqual("a469d7f3b1c9c3d875eb61042af59f22f3527bb952deb0dce87a820c3c0dee1c", digest(canonical(d)))

    def test_other_provenance_rows_remain_exact_and_delta_is_eighteen(self):
        rows = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())["entries"]
        predecessor_rows = tomllib.loads(phase5_predecessor_ledger(
            (ROOT / PHASE5_LEDGER_PATH).read_text()))["entries"]
        self.assertEqual(1269, len(predecessor_rows))
        unowned = [r for r in predecessor_rows if (r["mass"], r["proper"]) not in KEYS]
        self.assertEqual("555c3d0866875122302b5d48219887c21f82438bdcd569ef139a6579d54f6a9c", digest(canonical(unowned)))
        BATCH_GUARDS.assert_live_baseline_bodies(self.document)
        current_prior_records = BATCH_GUARDS.historical_latin_records(self.records)
        historical_rows = tomllib.loads(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH))["entries"]
        self.assertEqual(1289, len(historical_rows))
        owners = list(body_owners(BATCH_GUARDS.historical_document(self.document)))
        # historical_latin_records selects original owner IDs but keeps their
        # CURRENT rows. Replay raw statuses separately, applying only the
        # original declared defaults rather than current admission validation.
        original = tomllib.loads(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH))
        raw_records = {LatinKey.from_mapping(row): {**original["defaults"], **row}
                       for row in original["entries"]}
        self.assertEqual(set(raw_records), set(current_prior_records))
        counts = lambda rows: (sum(r["publication_status"] == "permitted" for r in rows.values()),
                               sum(r["provenance_status"] == "unresolved" for r in rows.values()),
                               sum(r["publication_status"] == "withheld" for r in rows.values()))
        self.assertEqual((1269,17,3), counts(raw_records))
        removed = {k for k, _, state in owners if state == "removed"}
        self.assertEqual(removed, {k for k, r in raw_records.items() if r.get("body_status") == "removed"})
        self.assertTrue(all(raw_records[k]["publication_status"] != "permitted" for k in removed))
        # The accepted 26 October latin-seven-rights-adoption restores only
        # Anthony's Collect. Preserve that intermediate status-count contract.
        anthony = LatinKey("s-antonii-padua-confessoris-ecclesiae-doctoris", "", "Collect", "", "", 1)
        later = {LatinKey("comm-s-silvestri-i-papae-confessoris", "", "Collect", "", "", 1),
                 LatinKey("palm-sunday", "", "Procession Antiphon", "", "", 5),
                 LatinKey("palm-sunday", "", "Procession Antiphon", "", "", 6)}
        restored = {k for k in removed if current_prior_records[k]["publication_status"] == "permitted"}
        self.assertEqual(restored, {anthony} | later)
        legacy = dict(raw_records)
        legacy[anthony] = current_prior_records[anthony]
        self.assertEqual((1270,16,3), counts(legacy))
        self.assertEqual(removed - {anthony}, {k for k, r in legacy.items() if r.get("body_status") == "removed"})
        self.assertEqual(removed - restored, {k for k, r in current_prior_records.items() if r.get("body_status") == "removed"})
        # The finite-sixteen authority restores Silvester; installation-a7619040
        # and its two source reviews map Palm English ordinals 6/7 to Latin 5/6.
        status = lambda row: (row["publication_status"], row["provenance_status"])
        self.assertEqual(later, {k for k in current_prior_records if status(current_prior_records[k]) != status(legacy[k])})
        bodies = {k: body for k, body, state in body_owners(self.document) if state == "present"}
        for k in restored:
            self.assertEqual(("permitted", "collated"), status(current_prior_records[k]))
            self.assertTrue(decision_for(k, bodies[k], self.records).permits(SURFACES))
        for k in removed - restored:
            self.assertEqual(status(raw_records[k]), status(current_prior_records[k]))
            self.assertFalse(decision_for(k, "Invented body.", self.records).permits(SURFACES))
        self.assertEqual((1273,13,3), counts(current_prior_records))

    def test_real_cli_raw_and_appointed_bodies_have_the_same_bytes(self):
        for mass in MASSES:
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools/mass-propers"), "show",
                 "--calendar", "roman-1962", "--mass", mass, "--format", "json"],
                cwd=ROOT, capture_output=True, text=True, check=True)
            payload = json.loads(result.stdout)
            for r in (r for r in ORACLES if r["mass"] == mass):
                raw = [p for p in payload["mass"]["propers"] if p["name"] == r["proper"]]
                appointed = [p for p in payload["appointed"] if p["name"] == r["proper"]]
                self.assertEqual((1, 1), (len(raw), len(appointed)))
                self.assertIsNone(appointed[0]["taken_from"])
                for p in (raw[0], appointed[0]["proper"]):
                    self.assertEqual(r["body"], p["text"])
                    self.assertFalse(p.get("latin", {}).get("withheld", False))

    def test_specific_continuations_and_conclusion_lengths_are_not_inferred(self):
        bodies = {(r["mass"], r["proper"]): " ".join(prayer(self.index, r)["text"].split()) for r in ORACLES}
        self.assertTrue(bodies["comm-s-felicitatis-martyris", "Postcommunion"].endswith("Per Dominum nostrum."))
        self.assertTrue(bodies["comm-s-chrysogoni-martyris", "Secret"].endswith("Per Dominum nostrum."))
        self.assertIn("ejus nos tribue meritis adjuvari.", bodies["comm-s-saturnini-martyris", "Collect"])
        sat = bodies["comm-s-saturnini-martyris", "Postcommunion"]
        self.assertIn("tibi reddat acceptos.", sat)
        self.assertTrue(sat.endswith("Qui tecum vivit et regnat in unitate."))
        self.assertNotIn("Spiritus Sancti", sat)
        self.assertIn("contra omnes nequitias irruentes", bodies["comm-ss-sergii-bacchi-marcelli-apuleii", "Postcommunion"])
        self.assertIn("ita nobis indulgentiam largiaris.", bodies["comm-ss-ursulae-ac-sociarum-virginum", "Secret"])


if __name__ == "__main__":
    unittest.main()
