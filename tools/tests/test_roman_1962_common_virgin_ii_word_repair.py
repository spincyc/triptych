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
from tools.tests.test_roman_1962_octnov_commemoration_source_repair import (
    record, digest, canonical, phase5_predecessor_document, phase5_predecessor_ledger,
)
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
    "mass": "commune-virginum-2",
    "form": "",
    "proper": "Collect",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Indulgentiam nobis, quaesumus, Domine, beata N. Virgo et Martyr imploret: quae\ntibi grata semper exstitit, et merito castitatis, et tuae professione\nvirtutis. Per Dominum.\n",
    "body_sha256": "7a2eaf7ab5fb11fe9b6eec0d428e6ac13d128aca84c5b2b7c612d19046541331",
    "lane": "common",
    "physical_line_ranges": [
      [
        1,
        3
      ]
    ],
    "historical": "Pustet PDF 698 / printed [28], left middle; Oratio under Item pro Virgine et Martyre, Alia Missa, Me exspectaverunt",
    "historical_pages": [
      698
    ],
    "target": "PDF 838 / printed [30], unit 4394, left middle",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-commune-virginum-2-collect-word-repair",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-commune-virginum-2-collect-secret-page-images-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-commune-virginum-2-collect-word-repair-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "Exactly mine -> Domine; historical extitit -> target exstitit is a real received-spelling normalization, not OCR damage. Pustet has quaesumus Domine without the target comma.",
    "old_body": "Indulgentiam nobis, quaesumus, mine, beata N. Virgo et Martyr imploret: quae\ntibi grata semper exstitit, et merito castitatis, et tuae professione\nvirtutis. Per Dominum.\n",
    "old_sha256": "ebcbc78ed20c6dbca24a387defbbb3b28a943e99e145e65ec8235854b03b6499"
  },
  {
    "mass": "commune-virginum-2",
    "form": "",
    "proper": "Secret",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Hostias tibi, Domine, beatae N. Virginis et Martyris tuae dicatas meritis,\nbenignus assume: et ad perpetuum nobis tribue provenire subsidium. Per\nDominum.\n",
    "body_sha256": "b060f8757b58981dc9f3033ba4ef87fea00dfd0dcedc82515f613899e652b2b2",
    "lane": "common",
    "physical_line_ranges": [
      [
        5,
        7
      ]
    ],
    "historical": "Pustet PDF 699 / printed [29], left middle; Secreta after Diffusa est, before Feci judicium",
    "historical_pages": [
      699
    ],
    "target": "PDF 839 / printed [31], unit 4402, left middle",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-commune-virginum-2-secret-word-repair",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-commune-virginum-2-collect-secret-page-images-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-commune-virginum-2-secret-word-repair-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "Exactly mentis -> meritis; both independent complete page images print meritis, not mentis. No other lexical difference.",
    "old_body": "Hostias tibi, Domine, beatae N. Virginis et Martyris tuae dicatas mentis,\nbenignus assume: et ad perpetuum nobis tribue provenire subsidium. Per\nDominum.\n",
    "old_sha256": "1f30c96155951a38b1c6eb2816eb684a45bc41d9dc4025c6a2c2db1363b60871"
  }
]''')
ALL_KEYS = {('s-venantii-martyris', 'Secret'), ('comm-s-nicomedis-martyris', 'Secret'), ('commune-virginum-2', 'Secret'), ('s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris', 'Postcommunion'), ('comm-s-sabinae-martyris', 'Secret'), ('s-brunonis-confessoris', 'Postcommunion'), ('comm-ss-euphemiae-virginis-luciae-geminiani', 'Postcommunion'), ('s-annae-matris-beatae-mariae-virginis', 'Secret'), ('s-annae-matris-beatae-mariae-virginis', 'Collect'), ('s-callisti-i-papae-martyris', 'Postcommunion'), ('comm-ss-felicis-simplicii-faustini-beatricis', 'Secret'), ('s-francisci-borgiae-confessoris', 'Postcommunion'), ('s-venantii-martyris', 'Postcommunion'), ('comm-s-nicomedis-martyris', 'Postcommunion'), ('comm-s-sabinae-martyris', 'Postcommunion'), ('s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris', 'Secret'), ('s-hilarii-episcopi-confessoris-ecclesiae-doctoris', 'Postcommunion'), ('s-annae-matris-beatae-mariae-virginis', 'Postcommunion'), ('comm-ss-euphemiae-virginis-luciae-geminiani', 'Secret'), ('comm-ss-euphemiae-virginis-luciae-geminiani', 'Collect'), ('comm-ss-felicis-simplicii-faustini-beatricis', 'Postcommunion'), ('s-callisti-i-papae-martyris', 'Secret'), ('s-francisci-borgiae-confessoris', 'Secret'), ('comm-ss-alexandri-eventii-theoduli-martyrum', 'Postcommunion'), ('commune-virginum-2', 'Collect')}
IMMUTABLE_GUARDS = {'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/artifacts/commons-2-orations-8f0f1a33/commons-2-orations-8f0f1a33.txt': '8f0f1a33bcd92be8742d2d69e89ddd5c455c180f33c64f1f584f40638e087995', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-collect.toml': '7252a4a2e2f055b2ab8dd194b96778d458a74b1e0576c43398bdb0724aea18f4', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-postcommunion.toml': '21ea32617470b8748b3fcdc63a2eb9dc60e659ad00735502529d67aa68ea7bca', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-secret.toml': '31488b03b8823baf47edb94c91355437bcd600d4680c25ea3567545dbe8bcd09', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-collect.toml': 'a4eb206c3cd7bef5c783bbf59e5702127a35a07ad56c01395027374212144481', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-postcommunion.toml': '750393a112746fd9a7b61c5dc05059fe8c67edd322e5ec259320ce7250253d76', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-secret.toml': 'dd2d2a42fee2a7c2605f684d688f7ca1e8e5bad68b5fbbf78ca6fc87c551ae51', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-collect-in-ipso-die-dedicationis.toml': '641478b09b534155b181de1ed6b10c51f8120293bc3ee939ae7bfc958c901491', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-collect.toml': 'f0aa7a9273ed9735b79138cea3651b6d00a9a2be9e8af54c029a29d53fc942a6', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-postcommunion-in-ipso-die-dedicationis.toml': '0aeaf00caf4a6b49ef6316d8bef1632f4360a24f59df7fda3f606bc33d66dfa5', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-postcommunion.toml': '2b4c8ff178bb0a94f5a31b001bef9cb00de999aa18fe94ef4ea491349c84d015', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-secret-extra-ecclesiam-ipsam-dedicatam.toml': '84f414c23345f2c7d7700f21b240df105dbd0b06ec85faf55dbd3152d721a360', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-secret-in-ipso-die-dedicationis.toml': 'ad9cc763cc6233b844202f387b4afbeb4869fc2538e41fedb88897cbd2ca8676', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-collect.toml': 'da558610b6a9852462312137b3925250f86d234ecab96eef738b80d45897d296', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-postcommunion.toml': '83f0215a1e9f8f9ea0c11be3c5f6d60ec95bb33428f32958c4de5646f971a871', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-secret.toml': '661fa79d3160eda9fbb0dae4a69477689f46f1bd107f6c11baa637d4151805f5', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-collect-pro-pluribus-martyribus-quae-non-sint-virgines.toml': '417b5c09bc41eb2e43ea97de9f56215752c25d5e63c5355448e105ec4567d6b6', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-collect.toml': '9b811bd6bcbeb621b00c0ac58d7819fad77ae033b5ad75751e7149673d0e8f9a', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-postcommunion.toml': '57794ddaeaf2b0e4fbe8f3c3070c04d9cf77efefc994f2365947cc1cc8af8ae4', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-secret-pro-pluribus-martyribus-quae-non-sint-virgines.toml': '2c505965b9d3c37b86f85dd543038e8b2819c17966a3ddc2731c89f38a159890', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-secret.toml': 'cd7f861800c9f3194ff871532576d2ea2946e98ecf6dc0dffea498c1b0305ad1', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-2-collect.toml': 'b18a9d6822a38059d7901fce1d6ec00607635ce7721870bf98de78d228839100', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-collect.toml': 'd469c7124b22915b8473da03060f7e44a548a493695122abbc5e407f483c07b5', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-postcommunion.toml': '5374407b323342ac39bd2b4333f07c838bad4273c6389f48f2f37ffea344f063', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-secret.toml': 'e000171fb26bdf467c281d3e169092fcdf97ede5a362e95f44b8624e78c48bd6', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-collect-pro-pluribus-virginibus-martyribus.toml': '8f6e8f21255ecb84d48b18ebd637d6cd4c579ee8ba857cee72b8abaa26ba5457', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-collect.toml': '2216f2b1cda0074f6995b9960118c7ef91afadad4c5f6a113a2b59efadf8c25a', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-postcommunion-pro-pluribus-virginibus-martyribus.toml': '4359b1a34b45c4eab70d8c572c0ae82eeeee16e0c8b1eeb474207ff8d69eab25', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-postcommunion.toml': '45d96bcc7d8622ae9f0ea0e8cfd2274ceb9c898575dff7f154814646b23aefff', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-secret-pro-pluribus-virginibus-martyribus.toml': 'f67c2b24b2d5222b23c25341972929eadc9cf20572b8deb73bad83834b7ea2b9', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-secret.toml': '90fab9ea36f94010efff1e16a8f7a6eff2cbaf8224bb664180b83ab9d81a7862', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-collect.toml': 'db9b43044b38148ac620fb41859c64a9dcc3edb197e92f36d460a22e70dbd7d0', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-postcommunion.toml': '3033c5a9a25bafd807bb4fabe1cdbf0334ffd7f1d2949082aa6025bf12b5f664', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-secret.toml': 'b70655eed2dec984dc49b1c19535ca7648649f343b068f360e6c99283b6a6d5b', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-4-collect.toml': '5f9b8505eb97c221fee202acdfbb2aeb8752c25e5c27c097fccb539d6d20f692', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-collect.toml': '49cbd6e444bfd8158017c10d0858bfeedab4cd4ad917425f7313863b29dfe756', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-postcommunion.toml': '8fa0478e6b1c1da3ee11c099b9cf8a6a928d6d54791294742eb29b0816dd8f13', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-secret.toml': '7e84319c635e8af03752b1707a2a17607619e7f94749370bdb2dab2cbd28f6d6', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-collect.toml': '38984de29887653b011b15237c6a3539b25347fd6770495730b998f1a0646fdd', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-postcommunion.toml': '5fd60100fe3f3d2733925eed38a16d6ec7f0af10d29dd050bc2f8a67612a3dd9', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-secret.toml': '392fe22bed075848cb789f4614f621f985902ac6af8d2d6842d3ec7e704d75a0', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-3-postcommunion.toml': '7419043b9d38717fdcc66de8f7e5d76f300a09f51f9374f7f0d88f222f9f6380', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-4-collect.toml': '49b0a1528eb7cf2f030efb841adf746bf7004f2939d07d34edea908383d49675', 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-4-postcommunion.toml': 'abdd025d3a41c72b7fb5dea54d08467758cba9e4e6adc5e0bfbae1e0561e79a1', 'src/sources/calendars/roman-pre-1955/propers.yaml': '037c74fa2dc8ecab13e2bd3bebc2e0ee194255c149b35d2c546d8c36cd9af65d', 'src/sources/inventories/roman-pre-1955-proper-latin-provenance-v1.toml': 'da959d9ba61843d2cb8f08155241b5b69058b6705f3d76aac67e6c70803546d9'}
UNOWNED_YAML = "21a82d2c4fdc9152fa4aa9df6a83df3476ab5a5872d50ffa92cccf7c35818b9a"
UNOWNED_LEDGER_BYTES = "654728b0769082f1046384746d7c654054d9ff9e83a59821d3f696ff20c6728c"

NOTE_HASHES = {'comm-s-nicomedis-martyris': '75987dd97ce97f95ab9ed31be055a9f82e6137b82a3fc780ed53af4a29689556', 'comm-s-sabinae-martyris': 'dddbb5f273b1a6b2fe71ea38b9fd70ded14651d996c35b7ff787c490ec602709', 'comm-ss-felicis-simplicii-faustini-beatricis': '0ebb181cd2a2a5db9c5ae346fa36f032d9386279b4f275a3ec1b51ba2bcdbc1d', 's-annae-matris-beatae-mariae-virginis': 'a1f24574d5326fbb84e423731e94fd86c1fa24cfb90fb5affcf3269d3ddb9949', 'comm-ss-euphemiae-virginis-luciae-geminiani': '4bbb527fabcf595b80e6ab3b545de17ef9c97053816925267f6f19145a0329d0', 's-brunonis-confessoris': 'ae203f26e6ada51158ed29b2b72a48498bd3bc417837f5b3538c1f1a3cd292c1', 's-callisti-i-papae-martyris': 'ae203f26e6ada51158ed29b2b72a48498bd3bc417837f5b3538c1f1a3cd292c1', 's-francisci-borgiae-confessoris': 'ae203f26e6ada51158ed29b2b72a48498bd3bc417837f5b3538c1f1a3cd292c1', 's-hieronymi-presbyteri-confessoris-ecclesiae-doctoris': 'ae203f26e6ada51158ed29b2b72a48498bd3bc417837f5b3538c1f1a3cd292c1', 's-hilarii-episcopi-confessoris-ecclesiae-doctoris': '07b24be9340e6e367c60b4b766c9a0a54dd4719eaee1bfd59b37d6b942fd5e03', 's-venantii-martyris': 'da14ce8930befa3c78f4ef9d29ccc9909b2886fd1ed974e34df1d68b7c2b6c43'}

class CommonVirginIIWordRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT/"src/sources/calendars","roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records,errors = read_sidecar(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)
    def test_exact_two_tokens_keep_all_other_bytes_and_reject_old_body_hashes(self):
        replacements = [("mine","Domine"),("mentis","meritis")]
        for r,(old,new) in zip(ORACLES,replacements):
            p = prayer(self.index,r)
            self.assertEqual(r["old_body"].replace(old,new,1),p["text"])
            self.assertEqual(r["body"],p["text"])
            self.assertEqual(r["body_sha256"],digest(p["text"]))
            self.assertEqual(r["old_sha256"],digest(r["old_body"]))
            self.assertIn("N.",p["text"])
            self.assertTrue(p["text"].endswith("Dominum.\n"))
            self.assertTrue(decision_for(key(r),p["text"],self.records).permits(SURFACES))
            self.assertFalse(decision_for(key(r),r["old_body"],self.records).permits(SURFACES))
            self.assertFalse(decision_for(key(r),p["text"].replace("N.","Bibiana"),self.records).permits(SURFACES))
    def test_new_bounded_binding_and_real_spelling_difference_not_false_ocr_or_long_ending(self):
        lane = LANES["common"]
        art = record(lane["project_id"])
        payload = (ROOT/art["path"]).read_bytes()
        self.assertEqual((328,"ce623d9f71e6021c3e7121f910ef5f7adce6122d6e007eb5905ec50834a6841e"),(len(payload),digest(payload)))
        self.assertEqual([lane["historical_id"],TARGET],art["projected_from"])
        lines = payload.decode().splitlines(keepends=True)
        for r,bounds in zip(ORACLES,[[[1,3]],[[5,7]]]):
            row = self.records[key(r)]
            passage = record(row["source_id"])
            self.assertEqual((r["projection_passage_id"],r["target_passage_id"]),(row["source_id"],row["verification_source_id"]))
            self.assertEqual((lane["project_id"],lane["project_sha256"],bounds),(passage["artifact_id"],passage["artifact_sha256"],passage["physical_line_ranges"]))
            self.assertEqual(r["body"],"".join(lines[bounds[0][0]-1:bounds[0][1]]))
            self.assertEqual([lane["project_id"],"artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf",lane["historical_id"]],row["publication_source_ids"])
            self.assertNotIn(TARGET,row["publication_source_ids"])
            self.assertEqual(set(SURFACES),set(row["surfaces"]))
            self.assertIn("Per Dominum.",row["provenance_evidence"])
            target = record(row["verification_source_id"])
            self.assertEqual((TARGET,TARGET_HASH),(target["artifact_id"],target["artifact_sha256"]))
        collect = self.records[key(ORACLES[0])]
        self.assertIn("extitit -> target exstitit",collect["provenance_evidence"])
        self.assertIn("not OCR damage",collect["provenance_evidence"])
        historical = record(ORACLES[0]["historical_passage_id"])
        self.assertEqual([[1,2]],historical["artifact_page_ranges"])
        extract = record(lane["historical_id"])
        pdf = (ROOT/extract["path"]).read_bytes()
        self.assertEqual((lane["pdf_hash"],lane["pdf_byte_size"]),(digest(pdf),len(pdf)))
        self.assertEqual("public-domain",extract["rights_status"])
        self.assertIn("698, 699",extract["transformation"])
    def test_old9778_byte_artifact_and_all43_passage_bindings_are_immutable(self):
        self.assertEqual(46,len(IMMUTABLE_GUARDS))
        for p,h in IMMUTABLE_GUARDS.items():
            self.assertEqual(h,digest((ROOT/p).read_bytes()),p)
        old = record("artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.commons-2-orations-8f0f1a33")
        self.assertEqual(9778,(ROOT/old["path"]).stat().st_size)
    def test_all_other_calendar_nodes_appointments_and_exact_ledger_bytes_unchanged(self):
        d = phase5_predecessor_document(self.document)
        for sec in d["sections"].values():
            for m in sec["masses"]:
                if m["key"] in NOTE_HASHES:
                    self.assertEqual(NOTE_HASHES[m["key"]],digest(m["notes"]))
                    m.pop("notes")
                m["propers"] = [p for p in m.get("propers",[]) if (m["key"],p["name"]) not in ALL_KEYS]
        self.assertEqual(UNOWNED_YAML,digest(canonical(d)))
        ledger = (ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text()
        ledger = phase5_predecessor_ledger(ledger)
        parts = re.split(r"(?m)^\[\[entries\]\]\n",ledger)
        unowned = parts[0]
        for part in parts[1:]:
            row = tomllib.loads("[[entries]]\n"+part)["entries"][0]
            if (row["mass"],row["proper"]) not in ALL_KEYS:
                unowned += "[[entries]]\n"+part
        self.assertEqual(UNOWNED_LEDGER_BYTES,digest(unowned))
        owners = list(body_owners(self.document))
        self.assertEqual((1289,1269,20),(len(self.records),sum(s=="present" for _,_,s in owners),sum(s=="removed" for _,_,s in owners)))
        self.assertEqual(1244,sum(s=="present" and (k.mass,k.proper) not in ALL_KEYS for k,p,s in owners))
        self.assertEqual((1269,17,3),(sum(r["publication_status"]=="permitted" for r in self.records.values()),sum(r["provenance_status"]=="unresolved" for r in self.records.values()),sum(r["publication_status"]=="withheld" for r in self.records.values())))
    def test_inherited_two_word_corrections_are_not_pre1955_target_attestation(self):
        pre = C.load_document(ROOT/"src/sources/calendars","roman-pre-1955")
        index = C.mass_index(pre)
        records,errors = publication_records(ROOT/"src/sources/calendars","roman-pre-1955")
        self.assertEqual([],errors)
        for r in ORACLES:
            self.assertEqual(r["body"],prayer(index,r)["text"])
            self.assertEqual("unresolved",records[key(r)]["publication_status"])
            self.assertIn("not established",records[key(r)]["note"])
            self.assertFalse(decision_for(key(r),r["body"],records).permits(SURFACES))

if __name__ == "__main__":
    unittest.main()
