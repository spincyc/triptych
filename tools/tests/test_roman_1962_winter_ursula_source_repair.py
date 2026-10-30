"""Nineteen fixed complete-petition oracles; independent cold review is separate."""
from pathlib import Path
import collections
import hashlib
import json
import re
import subprocess
import sys
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from tools.tests import _source_batch_guards as BATCH_GUARDS
import _calendars as C
from tools.tests.test_roman_1962_octnov_commemoration_source_repair import (
    phase5_predecessor_yaml, phase5_predecessor_ledger,
)
from _proper_latin import LatinKey, SURFACES, body_owners, decision_for, read_sidecar

ORACLES = json.loads(r'''[
  {
    "mass": "s-bibianae-virginis-martyris",
    "proper": "Collect",
    "body": "Deus, omnium largitor bonorum, qui in famula tua Bibiana cum\nvirginitatis flore martyrii palmam conjunxisti: mentes nostras ejus\nintercessione tibi caritate conjunge; ut, amotis periculis, praemia\nconsequamur aeterna. Per Dominum.\n",
    "body_sha256": "8c4d3b74e94461a000887dc8640554092cda67bdaa8a4c273eb9c3bd155c2fcb",
    "physical_line_ranges": [
      [
        1,
        4
      ]
    ],
    "target": {
      "pdf": 511,
      "printed": "430",
      "unit": 1823,
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        452
      ],
      "printed": [
        "366"
      ],
      "column": "R"
    },
    "target_text": "Deus, omnium largitor bonorum, qui in famula tua Bibiana cum virginitatis flore martyrii palmam coniunxisti: mentes nostras eius intercessione tibi caritate coniunge; ut, amotis periculis, praemia consequamur aeterna. Per Dominum.",
    "historical_text": "Deus, omnium largitor bonorum, qui in famula tua Bibiana cum virginitatis flore martyrii palmam conjunxisti: mentes nostras ejus intercessione tibi caritate conjunge, ut amotis periculis, praemia consequamur aeterna. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-s-bibianae-virginis-martyris-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-s-bibianae-virginis-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-s-bibianae-virginis-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "s-bibianae-virginis-martyris",
    "proper": "Secret",
    "body": "Hostias tibi, Domine, beatae Bibianae Virginis et Martyris tuae\ndicatas meritis, benignus assume: et ad perpetuum nobis tribue\nprovenire subsidium. Per Dominum.\n",
    "body_sha256": "25ab0bc6af50bda4876ef38d7e9b9d85887f39d6554d1ee20eecf63a3c0b302b",
    "physical_line_ranges": [
      [
        6,
        8
      ]
    ],
    "target": {
      "pdf": 511,
      "printed": "430",
      "unit": 1824,
      "column": "R",
      "mark": "C"
    },
    "historical": {
      "pdf": [
        699
      ],
      "printed": [
        "[29]"
      ],
      "column": "L"
    },
    "target_text": "Hostias tibi, Domine, beatae Bibianae Virginis et Martyris tuae dicatas meritis, benignus assume: et ad perpetuum nobis tribue provenire subsidium. Per Dominum.",
    "historical_text": "Hostias tibi, Domine, beatae N. Virginis et Martyris tuae dicatas meritis, benignus assume: et ad perpetuum nobis tribue provenire subsidium. Per Dominum.",
    "substitution": {
      "printed_blank": "N.",
      "target": "Bibianae",
      "rule": "guidance/propers-for-agents.md: filling a rubric-directed saint-name blank is permitted; full surrounding prayer must match."
    },
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-s-bibianae-virginis-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-s-bibianae-virginis-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-s-bibianae-virginis-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "s-bibianae-virginis-martyris",
    "proper": "Postcommunion",
    "body": "Divini muneris largitate satiati, quaesumus, Domine Deus noster: ut,\nintercedente beata Bibiana Virgine et Martyre tua, in ejus semper\nparticipatione vivamus. Per Dominum.\n",
    "body_sha256": "8b3e5ff4a7563bbbd49521b0161a00c7a15bf94803fba18d9a103669b3f07495",
    "physical_line_ranges": [
      [
        10,
        12
      ]
    ],
    "target": {
      "pdf": 511,
      "printed": "430",
      "unit": 1825,
      "column": "R",
      "mark": "C"
    },
    "historical": {
      "pdf": [
        699
      ],
      "printed": [
        "[29]"
      ],
      "column": "L"
    },
    "target_text": "Divini muneris largitate satiati, quaesumus, Domine Deus noster: ut, intercedente beata Bibiana Virgine et Martyre tua, in eius semper participatione vivamus. Per Dominum.",
    "historical_text": "Divini muneris largitate satiati, quaesumus Domine Deus noster: ut, intercedente beata N. Virgine et Martyre tua, in ejus semper participatione vivamus. Per Dominum.",
    "substitution": {
      "printed_blank": "N.",
      "target": "Bibiana",
      "rule": "guidance/propers-for-agents.md: explicit Common saint-name blank."
    },
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-s-bibianae-virginis-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-s-bibianae-virginis-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-s-bibianae-virginis-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-sabbae-abbatis",
    "proper": "Collect",
    "body": "Intercessio nos, quaesumus, Domine, beati Sabbae Abbatis commendet:\nut, quod nostris meritis non valemus, ejus patrocinio assequamur. Per\nDominum nostrum.\n",
    "body_sha256": "74502b8c7c784423dc10e8c2bd4fae0dfe865c7301ade470b17a3c53210fc3fb",
    "physical_line_ranges": [
      [
        14,
        16
      ]
    ],
    "target": {
      "pdf": 514,
      "printed": "433",
      "unit": 1849,
      "column": "R",
      "mark": "C"
    },
    "historical": {
      "pdf": [
        454
      ],
      "printed": [
        "368"
      ],
      "column": "R"
    },
    "target_text": "Intercessio nos, quaesumus, Domine, beati Sabbae Abbatis commendet: ut, quod nostris meritis non valemus, eius patrocinio assequamur. Per Dominum nostrum.",
    "historical_text": "Intercessio nos, quaesumus Domine, beati Sabbae Abbatis commendet: ut quod nostris meritis non valemus, ejus patrocinio assequamur. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-sabbae-abbatis-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-sabbae-abbatis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-sabbae-abbatis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-sabbae-abbatis",
    "proper": "Secret",
    "body": "Sacris altaribus, Domine, hostias superpositas sanctus Sabbas,\nquaesumus, in salutem nobis provenire deposcat. Per Dominum nostrum\nJesum Christum, Filium tuum: Qui tecum.\n",
    "body_sha256": "148a642ee692c936b0b4c839149f324bb749a27d790646ed791cc3f31fd8a5da",
    "physical_line_ranges": [
      [
        18,
        20
      ]
    ],
    "target": {
      "pdf": 514,
      "printed": "433",
      "unit": 1850,
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        454
      ],
      "printed": [
        "368"
      ],
      "column": "R"
    },
    "target_text": "Sacris altaribus, Domine, hostias superpositas sanctus Sabbas, quaesumus, in salutem nobis provenire deposcat. Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum.",
    "historical_text": "Sacris altaribus, Domine, hostias superpositas sanctus Sabbas, quaesumus, in salutem nobis provenire deposcat. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "expanded-stopping-Qui-tecum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-sabbae-abbatis-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-sabbae-abbatis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-sabbae-abbatis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-sabbae-abbatis",
    "proper": "Postcommunion",
    "body": "Protegat nos, Domine, cum tui perceptione sacramenti beatus Sabbas,\npro nobis intercedendo: ut et conversationis ejus experiamur insignia,\net intercessionis percipiamus suffragia. Per Dominum.\n",
    "body_sha256": "aa4f312160889b7632924f4cb6b1060a87cd9462dd158898f7ecbc6d829e56ca",
    "physical_line_ranges": [
      [
        22,
        24
      ]
    ],
    "target": {
      "pdf": 515,
      "printed": "434",
      "unit": 1851,
      "column": "L",
      "mark": "P"
    },
    "historical": {
      "pdf": [
        454
      ],
      "printed": [
        "368"
      ],
      "column": "R"
    },
    "target_text": "Protegat nos, Domine, cum tui perceptione sacramenti beatus Sabbas, pro nobis intercedendo: ut et conversationis eius experiamur insignia, et intercessionis percipiamus suffragia. Per Dominum.",
    "historical_text": "Protegat nos, Domine, cum tui perceptione sacramenti beatus Sabbas pro nobis intercedendo: ut et conversationis ejus experiamur insignia, et intercessionis percipiamus suffragia. Per Dominum nostrum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-sabbae-abbatis-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-sabbae-abbatis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-sabbae-abbatis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "second-day-within-octave-s-stephani",
    "proper": "Collect",
    "body": "Da nobis, quaesumus, Domine, imitari quod colimus: ut discamus et\ninimicos diligere; quia ejus natalicia celebramus, qui novit etiam pro\npersecutoribus exorare Dominum nostrum Jesum Christum, Filium tuum:\nQui tecum vivit et regnat in unitate.\n",
    "body_sha256": "f916b45b83ae1c4ddc57fcf86fbed35d580f7c1b1fd3d74403e28370cc0d52d7",
    "physical_line_ranges": [
      [
        26,
        29
      ]
    ],
    "target": {
      "pdf": 104,
      "printed": "23",
      "unit": 152,
      "column": "R"
    },
    "historical": {
      "pdf": [
        106
      ],
      "printed": [
        "20"
      ],
      "column": "R bottom"
    },
    "target_text": "Da nobis, quaesumus, Domine, imitari quod colimus: ut discamus et inimicos diligere; quia eius natalicia celebramus, qui novit etiam pro persecutoribus exorare Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "historical_text": "Da nobis, quaesumus Domine, imitari quod colimus: ut discamus et inimicos diligere: quia ejus natalitia celebramus, qui novit etiam pro persecutoribus exorare Dominum nostrum Jesum Christum Filium tuum. Qui tecum vivit.",
    "substitution": null,
    "target_conclusion_class": "expanded-through-in-unitate",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-second-day-within-octave-s-stephani-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-second-day-within-octave-s-stephani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-second-day-within-octave-s-stephani-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-ss-ursulae-ac-sociarum-virginum",
    "proper": "Postcommunion",
    "body": "Praesta nobis, quaesumus, Domine: intercedentibus sanctis Virginibus\net Martyribus tuis Ursula et Sociabus ejus; ut, quod ore contingimus,\npura mente capiamus. Per Dominum nostrum Jesum Christum.\n",
    "body_sha256": "5a5b9ed5c33e154ea2ca35320f7447da49d6100622ca563537e849b60d0137d2",
    "physical_line_ranges": [
      [
        1,
        3
      ]
    ],
    "target": {
      "pdf": 775,
      "printed": "694",
      "unit": 3922,
      "column": "R",
      "mark": "P"
    },
    "historical": {
      "edition": "Mame Tours 1922",
      "pdf": [
        855
      ],
      "printed": [
        "741"
      ],
      "column": "R top"
    },
    "target_text": "Praesta nobis, quaesumus, Domine: intercedentibus sanctis Virginibus et Martyribus tuis Ursula et Sociabus eius; ut, quod ore contingimus, pura mente capiamus. Per Dominum nostrum Iesum Christum.",
    "historical_text": "Praesta nobis, quaesumus, Domine: intercedentibus sanctis Virginibus et Martyribus tuis Ursula et Sociabus ejus; ut, quod ore contingimus, pura mente capiamus. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum-Iesum-Christum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-ss-ursulae-ac-sociarum-virginum-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase3-comm-ss-ursulae-ac-sociarum-virginum-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-ss-ursulae-ac-sociarum-virginum-orations-recheck-2026-10-22",
    "lane": "ursula"
  },
  {
    "mass": "second-day-within-octave-s-stephani",
    "proper": "Secret",
    "body": "Suscipe, Domine, munera pro tuorum commemoratione Sanctorum: ut, sicut\nillos passio gloriosos effecit; ita nos devotio reddat innocuos. Per\nDominum nostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat\nin unitate.\n",
    "body_sha256": "5d61b1e210363df2115f0b313cb7291bfc49c4f67b61b4cfeca4d1d2c29c86b2",
    "physical_line_ranges": [
      [
        31,
        34
      ]
    ],
    "target": {
      "pdf": 106,
      "printed": "25",
      "unit": 161,
      "column": "L"
    },
    "historical": {
      "pdf": [
        107,
        108
      ],
      "printed": [
        "21",
        "22"
      ],
      "column": "R bottom to L top"
    },
    "target_text": "Suscipe, Domine, munera pro tuorum commemoratione Sanctorum: ut, sicut illos passio gloriosos effecit; ita nos devotio reddat innocuos. Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "historical_text": "Suscipe, Domine, munera, pro tuorum commemoratione Sanctorum: ut sicut illos passio gloriosos effecit, ita nos devotio reddat innocuos. Per Dominum nostrum Jesum Christum.",
    "substitution": null,
    "target_conclusion_class": "expanded-through-in-unitate",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-second-day-within-octave-s-stephani-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-second-day-within-octave-s-stephani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-second-day-within-octave-s-stephani-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "second-day-within-octave-s-stephani",
    "proper": "Postcommunion",
    "body": "Auxilientur nobis, Domine, sumpta mysteria: et, intercedente beato\nStephano Martyre tuo, sempiterna protectione confirment. Per Dominum\nnostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat in\nunitate.\n",
    "body_sha256": "a407bb53039a6fd23fd74cce73cede5a858040d2f28dbd97fa0a609ac3f8eedc",
    "physical_line_ranges": [
      [
        36,
        39
      ]
    ],
    "target": {
      "pdf": 106,
      "printed": "25",
      "unit": 164,
      "column": "L"
    },
    "historical": {
      "pdf": [
        108
      ],
      "printed": [
        "22"
      ],
      "column": "L"
    },
    "target_text": "Auxilientur nobis, Domine, sumpta mysteria: et, intercedente beato Stephano Martyre tuo, sempiterna protectione confirment. Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "historical_text": "Auxilientur nobis, Domine, sumpta mysteria: et intercedente beato Stephano Martyre tuo, sempiterna protectione confirment. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "expanded-through-in-unitate",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-second-day-within-octave-s-stephani-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-second-day-within-octave-s-stephani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-second-day-within-octave-s-stephani-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "third-day-within-octave-s-ioannis",
    "proper": "Collect",
    "body": "Ecclesiam tuam, Domine, benignus illustra: ut, beati Joannis Apostoli\ntui et Evangelistae illuminata doctrinis, ad dona perveniat\nsempiterna. Per Dominum nostrum.\n",
    "body_sha256": "c54e7b763d548996f776d7f05275456bcb9b04b1153a7591fbbfc22f7e376563",
    "physical_line_ranges": [
      [
        41,
        43
      ]
    ],
    "target": {
      "pdf": 106,
      "printed": "25",
      "unit": 167,
      "column": "R"
    },
    "historical": {
      "pdf": [
        108
      ],
      "printed": [
        "22"
      ],
      "column": "L"
    },
    "target_text": "Ecclesiam tuam, Domine, benignus illustra: ut, beati Ioannis Apostoli tui et Evangelistae illuminata doctrinis, ad dona perveniat sempiterna. Per Dominum nostrum.",
    "historical_text": "Ecclesiam tuam, Domine, benignus illustra: ut beati Joannis Apostoli tui et Evangelistae illuminata doctrinis, ad dona perveniat sempiterna. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-third-day-within-octave-s-ioannis-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-third-day-within-octave-s-ioannis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-third-day-within-octave-s-ioannis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "third-day-within-octave-s-ioannis",
    "proper": "Secret",
    "body": "Suscipe, Domine, munera, quae in ejus tibi solemnitate deferimus,\ncujus nos confidimus patrocinio liberari. Per Dominum.\n",
    "body_sha256": "d311cdae0f9693975b979070c6d0833a14e461001c8e3a413184879aefbea35a",
    "physical_line_ranges": [
      [
        45,
        46
      ]
    ],
    "target": {
      "pdf": 107,
      "printed": "26",
      "unit": 176,
      "column": "R"
    },
    "historical": {
      "pdf": [
        109
      ],
      "printed": [
        "23"
      ],
      "column": "L"
    },
    "target_text": "Suscipe, Domine, munera, quae in eius tibi solemnitate deferimus, cuius nos confidimus patrocinio liberari. Per Dominum.",
    "historical_text": "Suscipe, Domine, munera, quae in ejus tibi solemnitate deferimus, cujus nos confidimus patrocinio liberari. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-third-day-within-octave-s-ioannis-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-third-day-within-octave-s-ioannis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-third-day-within-octave-s-ioannis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "third-day-within-octave-s-ioannis",
    "proper": "Postcommunion",
    "body": "Refecti cibo potuque caelesti, Deus noster, te supplices deprecamur:\nut, in cujus haec commemoratione percepimus, ejus muniamur et\nprecibus. Per Dominum.\n",
    "body_sha256": "f6bf920edcf45badbd82ff92ed014e83daf0c7fe218b0de9079a9085ce6ec472",
    "physical_line_ranges": [
      [
        48,
        50
      ]
    ],
    "target": {
      "pdf": 107,
      "printed": "26",
      "unit": 179,
      "column": "R"
    },
    "historical": {
      "pdf": [
        109
      ],
      "printed": [
        "23"
      ],
      "column": "L"
    },
    "target_text": "Refecti cibo potuque caelesti, Deus noster, te supplices deprecamur: ut, in cuius haec commemoratione percepimus, eius muniamur et precibus. Per Dominum.",
    "historical_text": "Refecti cibo potuque coelesti, Deus noster, te supplices deprecamur: ut, in cujus haec commemoratione percepimus, ejus muniamur et precibus. Per Dominum nostrum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-third-day-within-octave-s-ioannis-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-third-day-within-octave-s-ioannis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-third-day-within-octave-s-ioannis-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "fourth-day-within-octave-ss-innocentium",
    "proper": "Collect",
    "body": "Deus, cujus hodierna die praeconium Innocentes Martyres non loquendo,\nsed moriendo confessi sunt: omnia in nobis vitiorum mala mortifica; ut\nfidem tuam, quam lingua nostra loquitur, etiam moribus vita fateatur.\nPer Dominum nostrum.\n",
    "body_sha256": "782402e5d4b95e2b323bc68e1455eea6cebe73139b9b24691e7b93f700654c5c",
    "physical_line_ranges": [
      [
        52,
        55
      ]
    ],
    "target": {
      "pdf": 108,
      "printed": "27",
      "unit": 182,
      "column": "L"
    },
    "historical": {
      "pdf": [
        109
      ],
      "printed": [
        "23"
      ],
      "column": "R"
    },
    "target_text": "Deus, cuius hodierna die praeconium Innocentes Martyres non loquendo, sed moriendo confessi sunt: omnia in nobis vitiorum mala mortifica; ut fidem tuam, quam lingua nostra loquitur, etiam moribus vita fateatur. Per Dominum nostrum.",
    "historical_text": "Deus, cujus hodierna die praeconium Innocentes martyres non loquendo, sed moriendo confessi sunt: omnia in nobis vitiorum mala mortifica: ut fidem tuam, quam lingua nostra loquitur, etiam moribus vita fateatur. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-fourth-day-within-octave-ss-innocentium-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-fourth-day-within-octave-ss-innocentium-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-fourth-day-within-octave-ss-innocentium-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "fourth-day-within-octave-ss-innocentium",
    "proper": "Secret",
    "body": "Sanctorum tuorum, Domine, nobis pia non desit oratio: quae et munera\nnostra conciliet, et tuam nobis indulgentiam semper obtineat. Per\nDominum nostrum.\n",
    "body_sha256": "23477b7bf7796b39e641e5383c50ca5a6319a127192f23523211c1ecb5f2ac12",
    "physical_line_ranges": [
      [
        57,
        59
      ]
    ],
    "target": {
      "pdf": 109,
      "printed": "28",
      "unit": 191,
      "column": "L"
    },
    "historical": {
      "pdf": [
        110
      ],
      "printed": [
        "24"
      ],
      "column": "R"
    },
    "target_text": "Sanctorum tuorum, Domine, nobis pia non desit oratio: quae et munera nostra conciliet, et tuam nobis indulgentiam semper obtineat. Per Dominum nostrum.",
    "historical_text": "Sanctorum tuorum, Domine, nobis pia non desit oratio, quae et munera nostra conciliet, et tuam nobis indulgentiam semper obtineat. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-fourth-day-within-octave-ss-innocentium-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-fourth-day-within-octave-ss-innocentium-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-fourth-day-within-octave-ss-innocentium-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "fourth-day-within-octave-ss-innocentium",
    "proper": "Postcommunion",
    "body": "Votiva, Domine, dona percepimus: quae Sanctorum nobis precibus, et\npraesentis, quaesumus, vitae pariter et aeternae tribue conferre\nsubsidium. Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum\nvivit et regnat in unitate.\n",
    "body_sha256": "9ff8b7d5e06be74a5a08703fae62942a8eec81cb446c55bc03817a406f5882f3",
    "physical_line_ranges": [
      [
        61,
        64
      ]
    ],
    "target": {
      "pdf": 109,
      "printed": "28",
      "unit": 194,
      "column": "R"
    },
    "historical": {
      "pdf": [
        110,
        111
      ],
      "printed": [
        "24",
        "25"
      ],
      "column": "R bottom to L top"
    },
    "target_text": "Votiva, Domine, dona percepimus: quae Sanctorum nobis precibus, et praesentis, quaesumus, vitae pariter et aeternae tribue conferre subsidium. Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "historical_text": "Votiva, Domine, dona percepimus: quae Sanctorum nobis precibus, et praesentis quaesumus vitae, pariter et aeternae tribue conferre subsidium. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "expanded-through-in-unitate",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-fourth-day-within-octave-ss-innocentium-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-fourth-day-within-octave-ss-innocentium-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-fourth-day-within-octave-ss-innocentium-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-thomae-episcopi-martyris",
    "proper": "Collect",
    "body": "Deus, pro cujus Ecclesia gloriosus Pontifex Thomas gladiis impiorum\noccubuit: praesta, quaesumus; ut omnes, qui ejus implorant auxilium,\npetitionis suae salutarem consequantur effectum. Per Dominum nostrum\nJesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.\n",
    "body_sha256": "d8609bba66e8e990ca7f7b4d3d4588448319f5ee3e234386dc7f4a4b326616f4",
    "physical_line_ranges": [
      [
        66,
        69
      ]
    ],
    "target": {
      "pdf": 111,
      "printed": "30",
      "unit": 207,
      "column": "L"
    },
    "historical": {
      "pdf": [
        111
      ],
      "printed": [
        "25"
      ],
      "column": "L"
    },
    "target_text": "Deus, pro cuius Ecclesia gloriosus Pontifex Thomas gladiis impiorum occubuit: praesta, quaesumus; ut omnes, qui eius implorant auxilium, petitionis suae salutarem consequantur effectum. Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "historical_text": "Deus, pro cujus Ecclesia gloriosus Pontifex Thomas gladiis impiorum occubuit: praesta, quaesumus: ut omnes, qui ejus implorant auxilium, petitionis suae salutarem consequantur effectum. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "expanded-through-in-unitate",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-thomae-episcopi-martyris-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-thomae-episcopi-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-thomae-episcopi-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-thomae-episcopi-martyris",
    "proper": "Secret",
    "body": "Munera tibi, Domine, dicata sanctifica: et, intercedente beato Thoma\nMartyre tuo atque Pontifice, per eadem nos placatus intende. Per\nDominum nostrum.\n",
    "body_sha256": "1febcd48b7aa8a056ee777a615ff7911c5929a30c2c149409bc5a5e7907f4533",
    "physical_line_ranges": [
      [
        71,
        73
      ]
    ],
    "target": {
      "pdf": 112,
      "printed": "31",
      "unit": 214,
      "column": "L"
    },
    "historical": {
      "pdf": [
        112
      ],
      "printed": [
        "26"
      ],
      "column": "L bottom"
    },
    "target_text": "Munera tibi, Domine, dicata sanctifica: et, intercedente beato Thoma Martyre tuo atque Pontifice, per eadem nos placatus intende. Per Dominum nostrum.",
    "historical_text": "Munera tibi, Domine, dicata sanctifica: et intercedente beato Thoma Martyre tuo atque Pontifice, per eadem nos placatus intende. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum-nostrum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-thomae-episcopi-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-thomae-episcopi-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-thomae-episcopi-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  },
  {
    "mass": "comm-s-thomae-episcopi-martyris",
    "proper": "Postcommunion",
    "body": "Haec nos communio, Domine, purget a crimine: et, intercedente beato\nThoma Martyre tuo atque Pontifice, caelestis remedii faciat esse\nconsortes. Per Dominum.\n",
    "body_sha256": "2887ac1784e0e51909819486a7533d7642e55c23caccb79187ebeb29dc116f80",
    "physical_line_ranges": [
      [
        75,
        77
      ]
    ],
    "target": {
      "pdf": 112,
      "printed": "31",
      "unit": 217,
      "column": "L"
    },
    "historical": {
      "pdf": [
        112
      ],
      "printed": [
        "26"
      ],
      "column": "R"
    },
    "target_text": "Haec nos communio, Domine, purget a crimine: et, intercedente beato Thoma Martyre tuo atque Pontifice, caelestis remedii faciat esse consortes. Per Dominum.",
    "historical_text": "Haec nos communio, Domine, purget a crimine: et intercedente beato Thoma Martyre tuo atque Pontifice, coelestis remedii faciat esse consortes. Per Dominum.",
    "substitution": null,
    "target_conclusion_class": "Per-Dominum",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-comm-s-thomae-episcopi-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-comm-s-thomae-episcopi-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase3-comm-s-thomae-episcopi-martyris-orations-recheck-2026-10-22",
    "lane": "winter"
  }
]''')
LANES = json.loads(r'''{
  "winter": {
    "project_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-winter-eighteen-orations-20261022",
    "historical_id": "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-winter-oration-pages-20261022",
    "parent_hash": "363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474",
    "pdf_hash": "f435966244f979f41a4b55b7299f1c2a7e274982909ffa38ac4ce3ffb533619a",
    "pages": [
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      452,
      454,
      699
    ],
    "pdf_byte_size": 1823911,
    "project_sha256": "3f31c1eef89a6baa0dbbb26b6616f89dc2edf003b6a080680d9517f843a81146",
    "project_byte_size": 3410
  },
  "ursula": {
    "project_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-ursula-postcommunion-20261022",
    "historical_id": "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase3-ursula-postcommunion-page-20261022",
    "parent_hash": "9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005",
    "pdf_hash": "493cf7402b6dfbd6a4059422fb55d7cf49717356f1a31314e9095be02063759d",
    "pages": [
      855
    ],
    "pdf_byte_size": 47970,
    "project_sha256": "5a5b9ed5c33e154ea2ca35320f7447da49d6100622ca563537e849b60d0137d2",
    "project_byte_size": 196
  }
}''')
UNCHANGED_YAML_SPAN_HASHES = ['6baf900dfbeee677b64663c59ae550c8ee7d773c8385cdc67e8976cdae8ff01f', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd3c78303d59274336fe566dee3e86fac414449511da26d8681b457ce6160c08a', 'c542ff0402de9629cb7a896db3ad2d9a9f00c19dadd34fd9dda9b5bb82cbbf88', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '63929e4daa1fdf3c170cffbc95530b5e97a944baa2e5cd7ecf63f93fe9f90e32', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '7aed7c8ce0f494fb9874fd2edc50a3cdf0a0a621d8218245195c08f69c287b74', '61152c31e05965feddb77b6e063515a4738b1ff61d86612a7d17573fa2e518b4', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '85861abcf9fb6a4dba98e1e445a797297a7b80af127562a40d0b3b34d55fc47c', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'cdef9eaba355b1e1b8b53e2737866774f1472b81ba7797ab9c4a7cc145fbe099', 'ec1ce16efd54e1233257e3820c9142a353269b0c9f2f2c6ea5ba0025ffe6365a', '3a9cf19746f327b7a7475f0e75f3bba45f7e0de34049c32b918f0c651d717221', 'a96af4a1ec2e39b94024e0e4fd108eaa2105a40001842fb01bc00bc7fb0c0481', '8f2adce51e3d56c24af5db95063b3daffb48ee6f43dc173cebc3ec6386c2d0ee', '5cbb86c0fc12914affd74cbdb6e5a9d776a039e3a9fbf00716aeda663b86c6cb', '32704202b0eed539b1c6737b5b1ea1c207795ed4e433395e6ed173cdb8847bb8', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'eba31fb245294fe825d1d1848c11fcae159c0b9eae140866b47c71dc8d152e12', 'd383e07f5662e531efc1a2618175730deeadcca608441ebfbb37bbb95cce87da', '0017a63d1fa39df54115549af77bed32e4ced5aacf65204409427ff4cf773953', 'ba32d647f5cfe57870728f65be2ab89deeae1f7cf8c4de351ce7044724d2053a', 'c2f50a2f15c6d12409d114ca6483a06570bb02fae9d420ac130b6ac76c908b62', '06f2e76e925b178aa41d71aa3061ff2c131b6fdd90e606221fb89fef6473d8db', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'f0778d2fc13e5f8c60f9ac8570b42dc96bbd8bff5d55be7877555ca8f50443a0']
UNOWNED_LEDGER_BYTES_HASH = '9b69bbc84a3f678b85a0a5dc1b6dbcc8fcc7a3bf5b1979a9a63ff9ce50bd7493'
UNOWNED_CALENDAR_HASH = 'b87234f1f0dfa33be8a76b894a41e344f1e825bbc0af30f012596851a07497ca'
CHANGED_NOTES = ['comm-s-sabbae-abbatis', 'comm-s-thomae-episcopi-martyris', 'commune-dedicationis-ecclesiae', 'dedicatione-archibasilicae-mi-salvatoris', 'dedicatione-basilicarum-ss-petri-pauli-apostolorum', 's-bibianae-virginis-martyris', 'third-day-within-octave-s-ioannis']
NOTE_HASHES = {'comm-s-sabbae-abbatis': 'c69b2b78329115c25c7ec2e2012e5102664fb914ab8343d3c891df8bb45b34de', 'comm-s-thomae-episcopi-martyris': '79659e3b5cdc79c8e0e3e512844d7a7d479cffadb387022745d9b00cf1f66843', 'commune-dedicationis-ecclesiae': '9f84716e232237d737d1bd2a84f46e319676469e0172bb9d32bc66e11e502d25', 'dedicatione-archibasilicae-mi-salvatoris': '4d8e8b0fda2529cdb052114bd6ff22a2362fda7f8da54cc1a38eb9ff6a5db1c7', 'dedicatione-basilicarum-ss-petri-pauli-apostolorum': 'd66ac6920fa846ca8285bbce68373dd5808c38c7bc487034888f5fa4a2c5c2f3', 's-bibianae-virginis-martyris': 'e2b096fce48f31a40daeee77bc131beb03f38b1eb3576757aefe819ba3dd0c88', 'third-day-within-octave-s-ioannis': '044dae07fbc7c48fea675bced4fc8ac211f01b30b0c557253cbf956f4a485737'}

KEYS = {(r["mass"], r["proper"]) for r in ORACLES}
TARGET = "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
TARGET_HASH = "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"
COMMON = "commune-dedicationis-ecclesiae"
DEDICATIONS = {"dedicatione-archibasilicae-mi-salvatoris", "dedicatione-basilicarum-ss-petri-pauli-apostolorum"}
digest = lambda v: hashlib.sha256(v if isinstance(v, bytes) else v.encode()).hexdigest()
canonical = lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

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

def tokens(s):
    s = s.lower().replace("æ", "ae").replace("œ", "oe").replace("j", "i")
    return re.findall("[a-z]+", s.replace("oe", "ae").replace("natalitia", "natalicia"))

def key(r):
    return LatinKey(r["mass"], "", r["proper"], "", "", 1)

def spans(source):
    fields = lambda node: {k.value: v for k,v in node.value}
    tree = yaml.compose(source, Loader=yaml.CLoader)
    nodes = {fields(m)["key"].value: m for section in fields(fields(tree)["sections"]).values()
             for m in fields(section)["masses"].value}
    out = []
    for mass, node in nodes.items():
        for p in fields(node).get("propers", yaml.SequenceNode("tag:yaml.org,2002:seq", [])).value:
            if (mass, fields(p)["name"].value) in KEYS:
                out.append((p.start_mark.line, p.end_mark.line))
        for k,v in node.value:
            if ((mass in CHANGED_NOTES and k.value == "notes") or
                (mass == COMMON and k.value == "common_sets") or
                (mass in DEDICATIONS and k.value == "takes_from")):
                end = v.end_mark.line + int(isinstance(v,yaml.ScalarNode) and v.end_mark.column > 0)
                out.append((k.start_mark.line,end))
    return sorted(out)

class WinterUrsulaSourceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT / "src/sources/calendars", "roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records, errors = read_sidecar(ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)

    def test_nineteen_full_bodies_have_exact_hash_bound_six_surface_rights(self):
        self.assertEqual((19,7),(len(KEYS),len({r["mass"] for r in ORACLES})))
        for r in ORACLES:
            with self.subTest(mass=r["mass"],proper=r["proper"]):
                p = next(p for p in self.index[r["mass"]]["propers"] if p["name"] == r["proper"])
                self.assertEqual(r["body"],p["text"])
                self.assertEqual(r["body_sha256"],digest(p["text"]))
                self.assertEqual("composed",p["source"])
                self.assertNotIn("text_status",p)
                self.assertNotIn("takes_from",p)
                row = self.records[key(r)]
                self.assertEqual(r["body_sha256"],row["text_sha256"])
                self.assertEqual(("collated","editorial-projection-exact-to-target","permitted","public-domain"),
                                 tuple(row[k] for k in ["provenance_status","relationship","publication_status","publication_basis"]))
                self.assertNotIn("body_status",row)
                lane = LANES[r["lane"]]
                self.assertEqual([lane["project_id"],lane["historical_id"]],row["publication_source_ids"])
                self.assertEqual(set(SURFACES),set(row["surfaces"]))
                self.assertTrue(decision_for(key(r),p["text"],self.records).permits(SURFACES))
                self.assertFalse(decision_for(key(r),"Mutatum "+p["text"],self.records).permits(SURFACES))

    def test_whole_historical_petitions_match_with_only_two_explicit_blanks(self):
        blanks = []
        for r in ORACLES:
            historical = r["historical_text"]
            if r["substitution"]:
                self.assertEqual(1,historical.count("N."))
                blanks.append((r["mass"],r["proper"],r["substitution"]["target"]))
                historical = historical.replace("N.",r["substitution"]["target"])
            marker = "Qui tecum" if (r["mass"],r["proper"]) == ("second-day-within-octave-s-stephani","Collect") else "Per Dominum"
            self.assertEqual(tokens(r["target_text"].split(marker)[0]),tokens(historical.split(marker)[0]))
            self.assertEqual(tokens(r["target_text"]),tokens(r["body"]))
        self.assertEqual([("s-bibianae-virginis-martyris","Secret","Bibianae"),
                          ("s-bibianae-virginis-martyris","Postcommunion","Bibiana")],blanks)

    def test_actual_conclusions_are_neither_expanded_nor_inferred(self):
        counts = collections.Counter()
        bodies = {}
        for r in ORACLES:
            body = " ".join(r["body"].split())
            bodies[r["mass"],r["proper"]] = body
            if body.endswith("Qui tecum vivit et regnat in unitate."):
                kind = "expanded-through-in-unitate"
            elif body.endswith("Qui tecum."):
                kind = "expanded-stopping-Qui-tecum"
            elif body.endswith("Per Dominum nostrum Jesum Christum."):
                kind = "Per-Dominum-nostrum-Iesum-Christum"
            elif body.endswith("Per Dominum nostrum."):
                kind = "Per-Dominum-nostrum"
            elif body.endswith("Per Dominum."):
                kind = "Per-Dominum"
            else:
                self.fail(body)
            self.assertEqual(r["target_conclusion_class"],kind)
            counts[kind] += 1
            self.assertNotIn("Spiritus Sancti",body)
        self.assertEqual({"Per-Dominum":7,"Per-Dominum-nostrum":5,"expanded-through-in-unitate":5,
                          "expanded-stopping-Qui-tecum":1,"Per-Dominum-nostrum-Iesum-Christum":1},dict(counts))
        sabbas = bodies["comm-s-sabbae-abbatis","Secret"]
        self.assertTrue(sabbas.endswith("Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum."))
        self.assertNotIn("vivit",sabbas)
        stephen = bodies["second-day-within-octave-s-stephani","Collect"]
        self.assertIn("exorare Dominum nostrum Jesum Christum",stephen)
        self.assertNotIn("Per Dominum",stephen)

    def test_bounded_artifacts_and_all_nineteen_physical_passages(self):
        for lane in LANES.values():
            art = record(lane["project_id"])
            payload = (ROOT/art["path"]).read_bytes()
            self.assertEqual((lane["project_sha256"],lane["project_byte_size"]),(digest(payload),len(payload)))
            self.assertEqual(lane["project_sha256"],art["sha256"])
            self.assertEqual("project-created",art["rights_status"])
            self.assertEqual([lane["historical_id"],TARGET],art["projected_from"])
            self.assertIn("conclusion",art["transformation"])
        for r in ORACLES:
            lane = LANES[r["lane"]]
            art = record(lane["project_id"])
            passage = record(r["projection_passage_id"])
            self.assertEqual((lane["project_id"],lane["project_sha256"],r["physical_line_ranges"]),
                             (passage["artifact_id"],passage["artifact_sha256"],passage["physical_line_ranges"]))
            lines = (ROOT/art["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(r["body"],"".join("".join(lines[a-1:b]) for a,b in passage["physical_line_ranges"]))
            self.assertEqual(r["projection_passage_id"],self.records[key(r)]["source_id"])

    def test_historical_extract_rights_parent_hashes_and_exact_page_maps(self):
        for name,lane in LANES.items():
            art = record(lane["historical_id"])
            payload = (ROOT/art["path"]).read_bytes()
            self.assertEqual((lane["pdf_hash"],lane["pdf_byte_size"]),(digest(payload),len(payload)))
            self.assertEqual(("public-domain","tracked",len(lane["pages"])),
                             (art["rights_status"],art["storage"],art["page_count"]))
            parent = record(art["derived_from"])
            self.assertEqual(lane["parent_hash"],parent["sha256"])
            self.assertEqual("public-domain",parent["rights_status"])
            self.assertEqual("United States",art["rights_jurisdiction"])
            self.assertIn(", ".join(map(str,lane["pages"])),art["transformation"])
            self.assertIn("no crop, OCR",art["transformation"])
        self.assertEqual([106,107,108,109,110,111,112,452,454,699],LANES["winter"]["pages"])
        self.assertEqual([855],LANES["ursula"]["pages"])

    def test_exact_loci_are_separate_from_publication_authority(self):
        for r in ORACLES:
            row = self.records[key(r)]
            h,t = record(r["historical_passage_id"]),record(r["target_passage_id"])
            lane = LANES[r["lane"]]
            self.assertEqual((lane["historical_id"],lane["pdf_hash"]),(h["artifact_id"],h["artifact_sha256"]))
            expected = {lane["pages"].index(p)+1 for p in r["historical"]["pdf"]}
            actual = {p for a,b in h["artifact_page_ranges"] for p in range(a,b+1)}
            self.assertTrue(expected <= actual)
            self.assertEqual((TARGET,TARGET_HASH),(t["artifact_id"],t["artifact_sha256"]))
            self.assertEqual(r["target_passage_id"],row["verification_source_id"])
            self.assertIn("no. "+str(r["target"]["unit"]),row["verification_locator"])
            self.assertIn("PDF p. "+str(r["target"]["pdf"]),row["verification_locator"])
            self.assertIn("200 and 400 dpi",t["notes"])
            self.assertNotIn(TARGET,row["publication_source_ids"])
            self.assertIn(r["historical_passage_id"],row["provenance_evidence"])

    def test_ursula_1922_full_named_petition_does_not_clear_1862_mismatch(self):
        r = next(r for r in ORACLES if r["lane"] == "ursula")
        self.assertIsNone(r["substitution"])
        self.assertIn("Ursula et Sociabus ejus",r["historical_text"])
        self.assertNotIn("N.",r["historical_text"])
        self.assertTrue(r["historical_text"].endswith("Per Dominum."))
        old = record("passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase2-comm-ss-ursulae-ac-sociarum-virginum-orations-page-image-2026-10-22")
        self.assertIn("lexical mismatch",old["notes"])
        self.assertIn("no explicit blank",old["notes"])

    def test_raw_and_appointed_bodies_match_once_without_common_substitution(self):
        for mass in sorted({r["mass"] for r in ORACLES}):
            entries,errors = C.resolve_propers(self.document,self.index[mass])
            self.assertEqual([],errors)
            for r in [r for r in ORACLES if r["mass"] == mass]:
                matches = [(p,o) for _,p,o in entries if C.proper_family(p["name"]) == r["proper"]]
                self.assertEqual(1,len(matches))
                self.assertEqual((r["body"],None),(matches[0][0]["text"],matches[0][1]))

    def test_nontarget_yaml_bytes_notes_and_provenance_bytes_stay_pinned(self):
        source = (ROOT/"src/sources/calendars/roman-1962/propers.yaml").read_text()
        source = phase5_predecessor_yaml(source)
        lines = source.splitlines(keepends=True)
        cursor = 0
        hashes = []
        for a,b in spans(source):
            hashes.append(digest("".join(lines[cursor:a])))
            cursor = b
        hashes.append(digest("".join(lines[cursor:])))
        self.assertEqual(UNCHANGED_YAML_SPAN_HASHES,hashes)
        for mass,h in NOTE_HASHES.items():
            self.assertEqual(h,digest(self.index[mass]["notes"]))
        ledger = (ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text()
        ledger = phase5_predecessor_ledger(ledger)
        parts = re.split(r"(?m)^\[\[entries\]\]\n",ledger)
        unowned = parts[0]
        for part in parts[1:]:
            row = tomllib.loads("[[entries]]\n"+part)["entries"][0]
            if (row["mass"],row["proper"]) not in KEYS:
                unowned += "[[entries]]\n"+part
        self.assertEqual(UNOWNED_LEDGER_BYTES_HASH,digest(unowned))

    def test_exact_current_owner_counts_keep_other_unknowns(self):
        BATCH_GUARDS.assert_live_baseline_bodies(self.document)
        prior_records = BATCH_GUARDS.historical_latin_records(self.records)
        owners = list(body_owners(BATCH_GUARDS.historical_document(self.document)))
        self.assertEqual((1289,1269,20),(len(prior_records),sum(s=="present" for _,_,s in owners),
                                      sum(s=="removed" for _,_,s in owners)))
        # historical_latin_records selects original owner IDs but keeps their
        # CURRENT rows. Replay raw statuses separately, applying only the
        # original declared defaults rather than current admission validation.
        original = tomllib.loads(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH))
        raw_records = {LatinKey.from_mapping(row): {**original["defaults"], **row}
                       for row in original["entries"]}
        self.assertEqual(set(raw_records), set(prior_records))
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
        restored = {k for k in removed if prior_records[k]["publication_status"] == "permitted"}
        self.assertEqual(restored, {anthony} | later)
        legacy = dict(raw_records)
        legacy[anthony] = prior_records[anthony]
        self.assertEqual((1270,16,3), counts(legacy))
        self.assertEqual(removed - {anthony}, {k for k, r in legacy.items() if r.get("body_status") == "removed"})
        self.assertEqual(removed - restored, {k for k, r in prior_records.items() if r.get("body_status") == "removed"})
        # The finite-sixteen authority restores Silvester; installation-a7619040
        # and its two source reviews map Palm English ordinals 6/7 to Latin 5/6.
        status = lambda row: (row["publication_status"], row["provenance_status"])
        self.assertEqual(later, {k for k in prior_records if status(prior_records[k]) != status(legacy[k])})
        bodies = {k: body for k, body, state in body_owners(self.document) if state == "present"}
        for k in restored:
            self.assertEqual(("permitted", "collated"), status(prior_records[k]))
            self.assertTrue(decision_for(k, bodies[k], self.records).permits(SURFACES))
        for k in removed - restored:
            self.assertEqual(status(raw_records[k]), status(prior_records[k]))
            self.assertFalse(decision_for(k, "Invented body.", self.records).permits(SURFACES))
        self.assertEqual((1273,13,3), counts(prior_records))
        boniface = self.index["comm-s-bonifatii-martyris"]["takes_from"]["common_sets"]["orations"]
        self.assertEqual("unresolved",boniface["state"])
        self.assertEqual({"c3","c4"},set(boniface["candidates"]))

    def test_cli_outputs_the_same_nineteen_permission_bound_bytes(self):
        for mass in sorted({r["mass"] for r in ORACLES}):
            proc = subprocess.run([sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show",
                                   "--calendar","roman-1962","--mass",mass,"--format","json"],
                                  cwd=ROOT,capture_output=True,text=True,check=True)
            data = json.loads(proc.stdout)
            for r in [r for r in ORACLES if r["mass"]==mass]:
                raw = next(p for p in data["mass"]["propers"] if p["name"]==r["proper"])
                appointed = [p for p in data["appointed"] if p["name"]==r["proper"]]
                self.assertEqual(1,len(appointed))
                self.assertIsNone(appointed[0]["taken_from"])
                for p in [raw,appointed[0]["proper"]]:
                    self.assertEqual(r["body"],p["text"])
                    self.assertFalse(p.get("latin",{}).get("withheld",False))

if __name__ == "__main__":
    unittest.main()
