"""Bounded whole-prayer source oracles; independent acceptance is a separate gate."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys
import tomllib
import unittest
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import _calendars as C
from _proper_latin import LatinKey, SURFACES, body_owners, decision_for, publication_records, read_sidecar
from tools.tests.test_roman_1962_octnov_commemoration_source_repair import record, digest, canonical
def key(r):
    return LatinKey(r["mass"], "", r["proper"], "", "", 1)
def prayer(index,r):
    return next(p for p in index[r["mass"]]["propers"] if p["name"] == r["proper"])
TARGET = "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
TARGET_HASH = "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"
def project(s):
    changes = {'Iesum': 'Jesum', 'Iesu': 'Jesu', 'Iuvenale': 'Juvenale', 'eius': 'ejus', 'cuius': 'cujus', 'adiuti': 'adjuti', 'adiuvemur': 'adjuvemur', 'maiestati': 'majestati'}
    return re.sub(r"\b("+"|".join(changes)+r")\b",lambda m:changes[m[0]],s)
LANES = {'main': {'edition': 'pustet-ratisbon-1862', 'name': 'Pustet Ratisbon 1862', 'year': 1862, 'parent': 'ia-facsimile-pdf-363d6fc3', 'held': '.scratch/roman-annual-source-repair-1/pustet-1862-complete.pdf', 'parent_hash': '363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474', 'pages': [525, 532, 586, 588, 589, 617, 618, 626, 627, 628, 637, 641, 645, 646], 'historical_slug': 'phase4-mayoct-alexander-oration-pages-20261022', 'project_slug': 'phase4-mayoct-alexander-twentytwo-orations-20261022', 'payload_name': 'phase4-mayoct-alexander-twentytwo-orations.txt', 'url': 'https://archive.org/download/bub_gb_E7sPAAAAIAAJ/bub_gb_E7sPAAAAIAAJ.pdf', 'hist': 'catholic-church.missale-romanum.pustet-ratisbon-1862', 'historical_id': 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-mayoct-alexander-oration-pages-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-mayoct-alexander-twentytwo-orations-20261022', 'pdf_hash': 'd87ea7debe9992fb92b4d838e2e93893c9e2a3d1a7ccece01e9160f8926a5a3e', 'pdf_byte_size': 2963971, 'project_sha256': 'dd94f56f258e665930043284c747c41852bb47371aa2fda01337a58bb459dc11', 'project_byte_size': 4242}, 'hilary': {'edition': '1922-tours-mame-editio-quarta-iuxta-typicam', 'name': 'Mame Tours 1922, editio quarta iuxta typicam', 'year': 1922, 'parent': 'ia-scan-pdf-9873693a', 'held': '.scratch/c1-pre1955/download/mame1922.pdf', 'parent_hash': '9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005', 'pages': [904, 905], 'historical_slug': 'phase4-hilary-doctor-pontiff-pages-20261022', 'project_slug': 'phase4-hilary-postcommunion-20261022', 'payload_name': 'phase4-hilary-postcommunion.txt', 'url': 'https://archive.org/download/missaleromanum0000unse/missaleromanum0000unse.pdf', 'hist': 'catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam', 'historical_id': 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase4-hilary-doctor-pontiff-pages-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-hilary-postcommunion-20261022', 'pdf_hash': '54f346b6e359a864a8596823ebf815d2fd8a1a0c377450c9b81edd648463e1ba', 'pdf_byte_size': 389906, 'project_sha256': '7037ccdbaacb3debd53b93d275f320b12899fb9c5f7fbf98b2526dd8c497fab0', 'project_byte_size': 147}, 'common': {'edition': 'pustet-ratisbon-1862', 'name': 'Pustet Ratisbon 1862', 'year': 1862, 'parent': 'ia-facsimile-pdf-363d6fc3', 'held': '.scratch/roman-annual-source-repair-1/pustet-1862-complete.pdf', 'parent_hash': '363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474', 'pages': [698, 699], 'historical_slug': 'phase4-common-virgin-ii-orations-pages-698-699-20261022', 'project_slug': 'phase4-common-virgin-ii-two-word-repair-ce623d9f', 'payload_name': 'common-virgin-ii-collect-secret.txt', 'url': 'https://archive.org/download/bub_gb_E7sPAAAAIAAJ/bub_gb_E7sPAAAAIAAJ.pdf', 'hist': 'catholic-church.missale-romanum.pustet-ratisbon-1862', 'historical_id': 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-common-virgin-ii-orations-pages-698-699-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-common-virgin-ii-two-word-repair-ce623d9f', 'pdf_hash': 'd78a82cf27b7fc5aa1e8aa92714304ede819fef4848cbd4f0eebaf2075c55369', 'pdf_byte_size': 466366, 'project_sha256': 'ce623d9f71e6021c3e7121f910ef5f7adce6122d6e007eb5905ec50834a6841e', 'project_byte_size': 328}}
ORACLES = json.loads(r'''[
  {
    "mass": "s-venantii-martyris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Hanc oblationem, omnipotens Deus, beati Venantii merita tibi reddant\nacceptam: ut, ipsius subsidiis adjuti, gloriae ejus consortes\nefficiamur. Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum\nvivit et regnat in unitate.\n",
    "body_sha256": "a246958003c01f4cac2f2259239f45e55fc40db43b84175e83d0123096b12e51",
    "lane": "main",
    "physical_line_ranges": [
      [
        1,
        4
      ]
    ],
    "historical": "Pustet PDF 532 / printed 446, right middle",
    "historical_pages": [
      532
    ],
    "target": "PDF 613 / printed 532, unit 2619 P, right middle",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-venantii-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-venantii-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-venantii-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length; preserve unsupported outside-Paschal whole-form obligation, no new branch"
  },
  {
    "mass": "s-venantii-martyris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Sumpsimus, Domine, aeternae vitae sacramenta, te humiliter\ndeprecantes: ut, beato Venantio Martyre tuo pro nobis deprecante,\nveniam nobis concilient et gratiam. Per Dominum nostrum.\n",
    "body_sha256": "851f668abedb63468d2266ee2f32ba363b9be81a78ce0743e91ffa09940adc5e",
    "lane": "main",
    "physical_line_ranges": [
      [
        6,
        8
      ]
    ],
    "historical": "Pustet PDF 532 / printed 446, right middle-lower",
    "historical_pages": [
      532
    ],
    "target": "PDF 613 / printed 532, unit 2620 P, right lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-venantii-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-venantii-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-venantii-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length; preserve existing referral and unresolved form obligation"
  },
  {
    "mass": "s-annae-matris-beatae-mariae-virginis",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Deus, qui beatae Annae gratiam conferre dignatus es, ut Genetricis\nunigeniti Filii tui mater effici mereretur: concede propitius; ut,\ncujus solemnia celebramus, ejus apud te patrociniis adjuvemur. Per\neundem Dominum nostrum.\n",
    "body_sha256": "63350515ef181152ed0a9b7ea5f52a46bd6e2c43cea24dd0b6eafc3ed49b15c2",
    "lane": "main",
    "physical_line_ranges": [
      [
        10,
        13
      ]
    ],
    "historical": "Pustet PDF 586 / printed 500, left middle-lower",
    "historical_pages": [
      586
    ],
    "target": "PDF 683 / printed 602, unit 3175, left lower",
    "historical_conclusion": "Per eundem Dominum.",
    "target_conclusion": "Per eundem Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-annae-matris-beatae-mariae-virginis-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-annae-matris-beatae-mariae-virginis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-annae-matris-beatae-mariae-virginis-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; historical genitricis/target Genetricis received spelling, not a lexical addition; target conclusion"
  },
  {
    "mass": "s-annae-matris-beatae-mariae-virginis",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Sacrificiis praesentibus, quaesumus, Domine, placatus intende: ut per\nintercessionem beatae Annae, quae Genetricis Filii tui Domini nostri\nJesu Christi mater exstitit, et devotioni nostrae proficiant, et\nsaluti. Per eundem Dominum nostrum Jesum Christum, Filium tuum: Qui\ntecum vivit et regnat in unitate.\n",
    "body_sha256": "e67e8b433dd1b1cd08acc54bc3135120e92bb2b27a0398935340d383f6402ff7",
    "lane": "main",
    "physical_line_ranges": [
      [
        15,
        19
      ]
    ],
    "historical": "Pustet PDF 586 / printed 500, right upper",
    "historical_pages": [
      586
    ],
    "target": "PDF 684 / printed 603, unit 3181, left bottom",
    "historical_conclusion": "Per eundem Dominum.",
    "target_conclusion": "Per eundem Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-annae-matris-beatae-mariae-virginis-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-annae-matris-beatae-mariae-virginis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-annae-matris-beatae-mariae-virginis-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; historical genitricis/target Genetricis and Anne Secret historical mater extitit -> target mater exstitit are real received-spelling differences, not OCR damage; canonical exstitit retained; actual target conclusion",
    "historical_petition_normalized": "Sacrificiis praesentibus, quaesumus, Domine, placatus intende: ut per intercessionem beatae Annae, quae genitricis Filii tui Domini nostri Iesu Christi mater extitit, et devotioni nostrae proficiant, et saluti."
  },
  {
    "mass": "s-annae-matris-beatae-mariae-virginis",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Caelestibus sacramentis vegetati, quaesumus, Domine Deus noster: ut,\nintercessione beatae Annae, quam Genetricis Filii tui matrem esse\nvoluisti, ad aeternam salutem pervenire mereamur. Per eundem Dominum.\n",
    "body_sha256": "318338d87f9133de9b5495330926862ea901aa7bb0d6791c479a39ce60f8d08f",
    "lane": "main",
    "physical_line_ranges": [
      [
        21,
        23
      ]
    ],
    "historical": "Pustet PDF 586 / printed 500, right middle",
    "historical_pages": [
      586
    ],
    "target": "PDF 684 / printed 603, unit 3183, right upper",
    "historical_conclusion": "Per eundem Dominum.",
    "target_conclusion": "Per eundem Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-annae-matris-beatae-mariae-virginis-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-annae-matris-beatae-mariae-virginis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-annae-matris-beatae-mariae-virginis-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; historical Coelestibus/genitricis versus target Caelestibus/Genetricis received spellings"
  },
  {
    "mass": "comm-ss-felicis-simplicii-faustini-beatricis",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Hostias tibi, Domine, pro sanctorum Martyrum tuorum Felicis,\nSimplicii, Faustini et Beatricis commemoratione deferimus: suppliciter\ndeprecantes; ut indulgentiam nobis pariter conferant, et salutem. Per\nDominum nostrum.\n",
    "body_sha256": "5a34d62cf22d5c7aaa0fde8b9f1d2db665171f26ce63bfa9c8cf29cc4f200d38",
    "lane": "main",
    "physical_line_ranges": [
      [
        25,
        28
      ]
    ],
    "historical": "Pustet PDF 588 / printed 502, right bottom; actual full names inside petition",
    "historical_pages": [
      588
    ],
    "target": "PDF 687 / printed 606, unit 3212 P, right lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-felicis-simplicii-faustini-beatricis-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-felicis-simplicii-faustini-beatricis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-felicis-simplicii-faustini-beatricis-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length; no saint blanks"
  },
  {
    "mass": "comm-ss-felicis-simplicii-faustini-beatricis",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Praesta, quaesumus, omnipotens Deus: ut sanctorum Martyrum tuorum\nFelicis, Simplicii, Faustini et Beatricis caelestibus mysteriis\ncelebrata solemnitas, indulgentiam nobis tuae propitiationis acquirat.\nPer Dominum.\n",
    "body_sha256": "bd56e230baea691402ed12bf8996b0cbb1184e5da6d9ef34527210079b8f93ed",
    "lane": "main",
    "physical_line_ranges": [
      [
        30,
        33
      ]
    ],
    "historical": "Pustet PDF 589 / printed 503, left middle; actual full names inside petition, heading Felix et Socii",
    "historical_pages": [
      589
    ],
    "target": "PDF 687 / printed 606, unit 3213 P, right bottom",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-felicis-simplicii-faustini-beatricis-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-felicis-simplicii-faustini-beatricis-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-felicis-simplicii-faustini-beatricis-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; historical coelestibus versus target caelestibus spelling; no blanks"
  },
  {
    "mass": "comm-s-sabinae-martyris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Hostias tibi, Domine, beatae Sabinae Martyris tuae dicatas meritis,\nbenignus assume: et ad perpetuum nobis tribue provenire subsidium. Per\nDominum nostrum.\n",
    "body_sha256": "a60e2bd520dd60298049a143d35deb74edf4a471c24fc6fd7032eb3b24bcbce4",
    "lane": "main",
    "physical_line_ranges": [
      [
        35,
        37
      ]
    ],
    "historical": "Pustet PDF 617 / printed 531, right bottom, continues PDF 618 / printed 532 left top",
    "historical_pages": [
      617,
      618
    ],
    "target": "PDF 724 / printed 643, unit 3508 P, left lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-s-sabinae-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-s-sabinae-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-s-sabinae-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length"
  },
  {
    "mass": "comm-s-sabinae-martyris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Divini muneris largitate satiati, quaesumus, Domine Deus noster: ut,\nintercedente beata Sabina Martyre tua, in ejus semper participatione\nvivamus. Per Dominum.\n",
    "body_sha256": "5186ec98c729793f9904339c75a4344f6177c2de00759848608b53376f0faaa1",
    "lane": "main",
    "physical_line_ranges": [
      [
        39,
        41
      ]
    ],
    "historical": "Pustet PDF 618 / printed 532, left middle",
    "historical_pages": [
      618
    ],
    "target": "PDF 724 / printed 643, unit 3509 P, left bottom (not the prior repeated PC unit 3506)",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-s-sabinae-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-s-sabinae-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-s-sabinae-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match"
  },
  {
    "mass": "comm-s-nicomedis-martyris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Suscipe, Domine, munera propitius oblata: quae majestati tuae beati\nNicomedis Martyris commendet oratio. Per Dominum.\n",
    "body_sha256": "95e4a58fb8950f504e4212bf38075f8f833c083d02055d26ff668999bc06661f",
    "lane": "main",
    "physical_line_ranges": [
      [
        43,
        44
      ]
    ],
    "historical": "Pustet PDF 626 / printed 540, right bottom; below Pro S. Nicomede Collect",
    "historical_pages": [
      626
    ],
    "target": "PDF 739 / printed 658, unit 3633 P, right middle, not repeated 3628",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-s-nicomedis-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-s-nicomedis-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-s-nicomedis-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; no blank"
  },
  {
    "mass": "comm-s-nicomedis-martyris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Purificent nos, Domine, sacramenta quae sumpsimus: et, intercedente\nbeato Nicomede Martyre tuo, a cunctis efficiant vitiis absolutos. Per\nDominum nostrum.\n",
    "body_sha256": "3ba94c8df6ad47b0003956d0f5f071f7c5e0aa21f505da0c83832715021b166f",
    "lane": "main",
    "physical_line_ranges": [
      [
        46,
        48
      ]
    ],
    "historical": "Pustet PDF 626 / printed 540, right bottom, continues PDF 627 / printed 541 left top, directly above Nicomedes heading referring to orations above",
    "historical_pages": [
      626,
      627
    ],
    "target": "PDF 739 / printed 658, unit 3634 P, right middle-lower, not repeated 3631",
    "historical_conclusion": "Per Dominum nostrum.",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-s-nicomedis-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-s-nicomedis-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-s-nicomedis-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; no blank"
  },
  {
    "mass": "comm-ss-euphemiae-virginis-luciae-geminiani",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Praesta, Domine, precibus nostris cum exsultatione proventum: ut\nsanctorum Martyrum Euphemiae, Luciae et Geminiani, quorum diem\npassionis annua devotione recolimus, etiam fidei constantiam\nsubsequamur. Per Dominum nostrum.\n",
    "body_sha256": "4750ebd705a8c68fa3de1abfbca257520baf79c2827ba09f79c08948c2517edb",
    "lane": "main",
    "physical_line_ranges": [
      [
        50,
        53
      ]
    ],
    "historical": "Pustet PDF 627 / printed 541, right lower, complete petition; no printed conclusion before Tertia Oratio rubric. PDF 628 / printed 542 left middle explicitly refers orations supra positae under the saints' heading.",
    "historical_pages": [
      627,
      628
    ],
    "target": "PDF 740 / printed 659, unit 3641 P, right middle",
    "historical_conclusion": "",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-collect",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; historical exultatione versus target exsultatione received spelling; target conclusion independently witnessed"
  },
  {
    "mass": "comm-ss-euphemiae-virginis-luciae-geminiani",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Vota populi tui, quaesumus, Domine, propitius intende: et, quorum nos\ntribuis solemnia celebrare, fac gaudere suffragiis. Per Dominum.\n",
    "body_sha256": "874f46d32e074ea2c732cb040295c856fef4159b021aae7d54c24307a9a4218c",
    "lane": "main",
    "physical_line_ranges": [
      [
        55,
        56
      ]
    ],
    "historical": "Pustet PDF 627 / printed 541, right bottom through intende, continues PDF 628 / printed 542 left top through suffragiis, followed by Tertia Secreta rubric",
    "historical_pages": [
      627,
      628
    ],
    "target": "PDF 741 / printed 660, unit 3643 P, left top",
    "historical_conclusion": "",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion independently witnessed; no named saint or blank"
  },
  {
    "mass": "comm-ss-euphemiae-virginis-luciae-geminiani",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Exaudi, Domine, preces nostras: et sanctorum Martyrum tuorum\nEuphemiae, Luciae et Geminiani, quorum festa solemniter celebramus,\ncontinuis foveamur auxiliis. Per Dominum.\n",
    "body_sha256": "c18a43e4ce4f6b2211b2cf8634005cbaeda3ff1318c7a915d8dfced8fbe80817",
    "lane": "main",
    "physical_line_ranges": [
      [
        58,
        60
      ]
    ],
    "historical": "Pustet PDF 628 / printed 542, left upper-middle, complete petition; no printed conclusion before Tertia Postcomm. rubric",
    "historical_pages": [
      628
    ],
    "target": "PDF 741 / printed 660, unit 3644 P, left upper",
    "historical_conclusion": "",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-euphemiae-virginis-luciae-geminiani-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion independently witnessed; whole named historical body"
  },
  {
    "mass": "s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Donis caelestibus da nobis, quaesumus, Domine, libera tibi mente\nservire: ut munera quae deferimus, interveniente beato Hieronymo\nConfessore tuo, et medelam nobis operentur, et gloriam. Per Dominum.\n",
    "body_sha256": "647fb4e0ff93de48d2d6a8e3d825f452da25bdce975d5701d95f6e223ea511e9",
    "lane": "main",
    "physical_line_ranges": [
      [
        62,
        64
      ]
    ],
    "historical": "Pustet PDF 637 / printed 551, right middle",
    "historical_pages": [
      637
    ],
    "target": "PDF 753 / printed 672, unit 3740 P, left lower-middle",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; no saint blank"
  },
  {
    "mass": "s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Repleti alimonia caelesti, quaesumus, Domine: ut, interveniente beato\nHieronymo Confessore tuo, misericordiae tuae gratiam consequi\nmereamur. Per Dominum.\n",
    "body_sha256": "725c3b941e115566b848c73d971b8272d521b82f263474836decae14d435054f",
    "lane": "main",
    "physical_line_ranges": [
      [
        66,
        68
      ]
    ],
    "historical": "Pustet PDF 637 / printed 551, right middle-lower",
    "historical_pages": [
      637
    ],
    "target": "PDF 753 / printed 672, unit 3741 P, left bottom",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; both Pustet1862 PDF637/printed551 and 1962 PDF753/printed672 no.3741 P end only Per Dominum.; no expanded conclusion and no saint blank"
  },
  {
    "mass": "s-brunonis-confessoris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Quaesumus, omnipotens Deus: ut, qui caelestia alimenta percepimus,\nintercedente beato Brunone Confessore tuo, per haec contra omnia\nadversa muniamur. Per Dominum nostrum Jesum Christum, Filium tuum: Qui\ntecum vivit et regnat in unitate.\n",
    "body_sha256": "fb74a2c272ed52c93d30ff0b79aa0b4c9640f936955798d723b97830b98ca387",
    "lane": "main",
    "physical_line_ranges": [
      [
        70,
        73
      ]
    ],
    "historical": "Pustet PDF 641 / printed 555, right bottom",
    "historical_pages": [
      641
    ],
    "target": "PDF 758 / printed 677, unit 3785 P, left bottom",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-brunonis-confessoris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-brunonis-confessoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-brunonis-confessoris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length; no saint blank"
  },
  {
    "mass": "s-francisci-borgiae-confessoris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Sacris altaribus, Domine, hostias superpositas sanctus Franciscus,\nquaesumus, in salutem nobis provenire deposcat. Per Dominum nostrum\nJesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.\n",
    "body_sha256": "f64aafc8a077836085f6dd5c33464883b5d17116d39ca3242f920eda4017b71b",
    "lane": "main",
    "physical_line_ranges": [
      [
        75,
        77
      ]
    ],
    "historical": "Pustet PDF 645 / printed 559, left middle",
    "historical_pages": [
      645
    ],
    "target": "PDF 766 / printed 685, unit 3844 P, left lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-francisci-borgiae-confessoris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-francisci-borgiae-confessoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-francisci-borgiae-confessoris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length"
  },
  {
    "mass": "s-francisci-borgiae-confessoris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Protegat nos, Domine, cum tui perceptione sacramenti beatus\nFranciscus, pro nobis intercedendo: ut et conversationis ejus\nexperiamur insignia, et intercessionis percipiamus suffragia. Per\nDominum.\n",
    "body_sha256": "a38026d2ecc085e3af8696e19a7979d14ca4ac63525c9c3f552df7b004a953df",
    "lane": "main",
    "physical_line_ranges": [
      [
        79,
        82
      ]
    ],
    "historical": "Pustet PDF 645 / printed 559, left lower",
    "historical_pages": [
      645
    ],
    "target": "PDF 766 / printed 685, unit 3845 P, left bottom",
    "historical_conclusion": "Per Dominum nostrum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-francisci-borgiae-confessoris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-francisci-borgiae-confessoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-francisci-borgiae-confessoris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion shorter"
  },
  {
    "mass": "s-callisti-i-papae-martyris",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Mystica nobis, Domine, prosit oblatio: quae nos et a reatibus nostris\nexpediat, et perpetua salvatione confirmet. Per Dominum.\n",
    "body_sha256": "28b499a2c89d6bbd0b43b3608f86d84a4cbbff54245e114285700001628fb7ce",
    "lane": "main",
    "physical_line_ranges": [
      [
        84,
        85
      ]
    ],
    "historical": "Pustet PDF 646 / printed 560, left middle",
    "historical_pages": [
      646
    ],
    "target": "PDF 768 / printed 687, unit 3862 P, left middle",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-callisti-i-papae-martyris-secret",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-callisti-i-papae-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-callisti-i-papae-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; no saint blank"
  },
  {
    "mass": "s-callisti-i-papae-martyris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Quaesumus, omnipotens Deus: ut reatus nostros munera sacrata\npurificent, et recte vivendi nobis operentur effectum. Per Dominum\nnostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat in\nunitate.\n",
    "body_sha256": "82722b4ed627758f0f91f5e5cb5af81abe6dd1408144f65f37d377bb3d9c612c",
    "lane": "main",
    "physical_line_ranges": [
      [
        87,
        90
      ]
    ],
    "historical": "Pustet PDF 646 / printed 560, left middle-lower",
    "historical_pages": [
      646
    ],
    "target": "PDF 768 / printed 687, unit 3863 P, left middle-lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-callisti-i-papae-martyris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-s-callisti-i-papae-martyris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-callisti-i-papae-martyris-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "whole-petition match; target conclusion length; no saint blank"
  }
]''')

class SourceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT/"src/sources/calendars","roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records,errors = read_sidecar(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)
    def test_exact_whole_bodies_and_six_surface_hash_joins(self):
        for r in ORACLES:
            with self.subTest(mass=r["mass"],proper=r["proper"]):
                p = prayer(self.index,r)
                self.assertEqual(r["body"],p["text"])
                self.assertEqual(r["body_sha256"],digest(p["text"]))
                self.assertEqual("composed",p["source"])
                self.assertNotIn("text_status",p)
                row = self.records[key(r)]
                self.assertNotIn("body_status",row)
                self.assertEqual((r["body_sha256"],"collated","permitted","public-domain"),
                                 tuple(row[k] for k in ["text_sha256","provenance_status","publication_status","publication_basis"]))
                self.assertEqual(set(SURFACES),set(row["surfaces"]))
                self.assertTrue(decision_for(key(r),r["body"],self.records).permits(SURFACES))
                self.assertFalse(decision_for(key(r),"Mutatum "+r["body"],self.records).permits(SURFACES))
                self.assertEqual(r["projection_passage_id"],row["source_id"])
                self.assertEqual(r["target_passage_id"],row["verification_source_id"])
                self.assertIn(r["historical_passage_id"],row["provenance_evidence"])
                self.assertNotIn(TARGET,row["publication_source_ids"])
                self.assertTrue(" ".join(p["text"].split()).endswith(project(r["target_conclusion"])))

        # Source-derived regression:1962 PDF753/672 no3741 P and Pustet637/551
        # both print only Per Dominum.; the previous author's expansion was wrong.
        jerome = prayer(self.index,dict(mass='s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris',proper="Postcommunion"))["text"]
        self.assertEqual('Repleti alimonia caelesti, quaesumus, Domine: ut, interveniente beato\nHieronymo Confessore tuo, misericordiae tuae gratiam consequi\nmereamur. Per Dominum.\n',jerome)
        self.assertEqual('725c3b941e115566b848c73d971b8272d521b82f263474836decae14d435054f',digest(jerome))
        self.assertEqual("Per Dominum."," ".join(jerome.split()).split("mereamur. ",1)[1])
        rejected = 'Repleti alimonia caelesti, quaesumus, Domine: ut, interveniente beato\nHieronymo Confessore tuo, misericordiae tuae gratiam consequi\nmereamur. Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum\nvivit et regnat in unitate.\n'
        self.assertFalse(decision_for(LatinKey('s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris',"","Postcommunion","","",1),rejected,self.records).permits(SURFACES))
        anne = next(r for r in ORACLES if r["mass"] == 's-annae-matris-beatae-mariae-virginis' and r["proper"] == "Secret")
        self.assertEqual('e67e8b433dd1b1cd08acc54bc3135120e92bb2b27a0398935340d383f6402ff7',digest(prayer(self.index,anne)["text"]))
        source_petition = anne["historical_petition_normalized"]
        self.assertIn("mater extitit",source_petition)
        normalized = source_petition.replace("genitricis","Genetricis").replace("mater extitit","mater exstitit")
        target_petition = " ".join(prayer(self.index,anne)["text"].split()).split(" Per eundem Dominum",1)[0]
        self.assertEqual(project(normalized),target_petition)
        for identifier in [anne["historical_passage_id"],anne["target_passage_id"],anne["projection_passage_id"],LANES["main"]["project_id"]]:
            account = record(identifier)
            self.assertIn("Anne Secret",account.get("notes","")+account.get("transformation",""))
            self.assertIn("mater extitit",account.get("notes","")+account.get("transformation",""))
            self.assertIn("mater exstitit",account.get("notes","")+account.get("transformation",""))
        row = self.records[key(anne)]
        self.assertIn("mater extitit",row["provenance_evidence"])
        self.assertIn("not OCR damage",row["provenance_evidence"])
        self.assertTrue(any("mater extitit" in s and "mater exstitit" in s for s in row["transformations"]))

    def test_bounded_projection_slices_and_lawful_historical_pages(self):
        for r in ORACLES:
            lane = LANES[r["lane"]]
            row = self.records[key(r)]
            self.assertEqual([lane["project_id"],lane["historical_id"]],row["publication_source_ids"])
            passage = record(r["projection_passage_id"])
            art = record(passage["artifact_id"])
            payload = (ROOT/art["path"]).read_bytes()
            self.assertEqual((lane["project_sha256"],lane["project_byte_size"]),(digest(payload),len(payload)))
            self.assertEqual((lane["project_id"],lane["project_sha256"],r["physical_line_ranges"]),
                             (passage["artifact_id"],passage["artifact_sha256"],passage["physical_line_ranges"]))
            lines = payload.decode().splitlines(keepends=True)
            self.assertEqual(r["body"],"".join("".join(lines[a-1:b]) for a,b in passage["physical_line_ranges"]))
            historical = record(r["historical_passage_id"])
            extract = record(historical["artifact_id"])
            pdf = (ROOT/extract["path"]).read_bytes()
            self.assertEqual((lane["pdf_hash"],lane["pdf_byte_size"]),(digest(pdf),len(pdf)))
            self.assertEqual("public-domain",extract["rights_status"])
            self.assertEqual(lane["parent_hash"],record(extract["derived_from"])["sha256"])
            self.assertIn(", ".join(map(str,lane["pages"])),extract["transformation"])
            selected = {p for a,b in historical["artifact_page_ranges"] for p in range(a,b+1)}
            self.assertTrue({lane["pages"].index(p)+1 for p in r["historical_pages"]} <= selected)
            target = record(r["target_passage_id"])
            self.assertEqual((TARGET,TARGET_HASH),(target["artifact_id"],target["artifact_sha256"]))
            self.assertIn(r["target"],target["locus"])
    def test_raw_and_appointed_whole_bodies_override_once(self):
        for mass in sorted({r["mass"] for r in ORACLES}):
            rows,errors = C.resolve_propers(self.document,self.index[mass])
            self.assertEqual([],errors)
            for r in [r for r in ORACLES if r["mass"] == mass]:
                found = [(p,o) for _,p,o in rows if C.proper_family(p["name"]) == r["proper"]]
                self.assertEqual([(r["body"],None)],[(p["text"],o) for p,o in found])
    def test_real_cli_same_1962_bytes_no_pre1955_published_body_or_attestation(self):
        pre,errors = publication_records(ROOT/"src/sources/calendars","roman-pre-1955")
        self.assertEqual([],errors)
        for mass in sorted({r["mass"] for r in ORACLES}):
            for calendar in ["roman-1962","roman-pre-1955"]:
                proc = subprocess.run([sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show","--calendar",calendar,
                                       "--mass",mass,"--format","json"],cwd=ROOT,capture_output=True,text=True,check=True)
                payload = json.loads(proc.stdout)
                for r in [r for r in ORACLES if r["mass"] == mass]:
                    p = next(p for p in payload["mass"]["propers"] if p["name"] == r["proper"])
                    if calendar == "roman-1962":
                        self.assertEqual(r["body"],p["text"])
                    else:
                        self.assertIsNone(p.get("text"))
                        self.assertTrue(p["latin"]["withheld"])
                        self.assertFalse(decision_for(key(r),r["body"],pre).permits(SURFACES))
                        self.assertIn("target-recension",pre[key(r)]["note"])

if __name__ == "__main__":
    unittest.main()
