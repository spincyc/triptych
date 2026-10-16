"""Original-language witness snapshots for the Eucharistic-book history.

Adapters read canonical text owners and their publication decisions. A snapshot
records evidence held, not prayers introduced by an act; missing collected text
never implies historical deletion. No adapter infers ancestry or earlier text.
"""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys

import _calendars
import _proper_latin

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-eucharistic-texts/v1"
PROPER_TARGET_EDITION = "edition.catholic-church.missale-romanum.vatican-typica-1962"
TOOL_INPUT_PATHS = (
    "scripts/_eucharistic_texts.py", "scripts/_proper_latin.py", "scripts/_calendars.py",
    "scripts/_tooling.py", "tools/source-library", "guidance/liturgical-text-publication-policy.md",
)
ORDINARY_EDITION = "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
WILSON_EDITION = "edition.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915"
WILSON_MEMENTO_PASSAGE = "passage.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-memento-domine"
WILSON_MEMENTO_ARTIFACT = "artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-memento-checked-latin-784ee4c8"
WILSON_MEMENTO_TEXT_SHA256 = "4fc270656e69b4c24537399483253c6d0311f1b56d734744753fc701dd3ccf87"
# Trusted selections identify reviewed source bodies; they contain no copied
# liturgical text. New witnesses use this same loader rather than a new parser.
CHECKED_PASSAGE_SETS: dict[str, dict] = {'brightman-1896-greek-basil': {'edition_id': 'edition.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1',
                                'scope': {'omitted_book_divisions': ['The rest of the anaphora and liturgy',
                                                                     'Rubrics, speaker cues, '
                                                                     'diaconal/congregational responses and '
                                                                     'apparatus',
                                                                     'Other constituent liturgies in the '
                                                                     'volume'],
                                          'represented_witness': 'Modern Greek Basil prayers as printed in '
                                                                 'Brightman 1896, from the Venice 1869 '
                                                                 'Euchologion according to the printed p. '
                                                                 '308 source note. Not the separate '
                                                                 'Barberini/Grottaferrata section.',
                                          'status': 'bounded-checked-greek-prayer-selection',
                                          'text_identity': 'Original Greek wording of two bounded prayer '
                                                           'units in the identified 1896 edition; explicit '
                                                           'typography and speech-block normalization, not a '
                                                           'reconstruction of earlier use.'},
                                'title': 'Brightman 1896: Greek Basil remembrance, offering and invocation',
                                'units': [{'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-anamnesis-oblation-checked-greek-e123ebb5',
                                           'division': 'anaphora',
                                           'element_key': 'anamnesis-oblation',
                                           'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-anamnesis-oblation-facsimile',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.byzantine-modern-text-sources'],
                                           'facsimile_pdf_page': '511',
                                           'language': 'grc',
                                           'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-anamnesis-oblation',
                                           'printed_page': '405',
                                           'source_order': 1,
                                           'text_sha256': '17f334010b240830b279e79d4ffe66b9bd7f21ec498986763b910a5aa7893759',
                                           'unit_id': 'unit.brightman-1896.greek-basil.anaphora.anamnesis-oblation'},
                                          {'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-invocation-gifts-checked-greek-e4935cb8',
                                           'division': 'anaphora',
                                           'element_key': 'invocation-gifts',
                                           'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-invocation-gifts-facsimile',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-metabalon-apparatus-note',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.byzantine-modern-text-sources'],
                                           'facsimile_pdf_page': '511,512',
                                           'language': 'grc',
                                           'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.basil-invocation-gifts',
                                           'printed_page': '405–406',
                                           'source_order': 2,
                                           'text_sha256': 'f78e45e409869baffc1350ebda80d88dcaa56ccfb072908096c9bdb420234b43',
                                           'unit_id': 'unit.brightman-1896.greek-basil.anaphora.invocation-gifts'}],
                                'witness_date': '1896 printed edition; modern text attributed by Brightman '
                                                'to Venice 1869'},
 'brightman-1896-greek-chrysostom': {'edition_id': 'edition.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1',
                                     'scope': {'omitted_book_divisions': ['The rest of the anaphora and '
                                                                          'liturgy',
                                                                          'Rubrics, speaker cues, '
                                                                          'diaconal/congregational responses '
                                                                          'and apparatus',
                                                                          'Other constituent liturgies in '
                                                                          'the volume'],
                                               'represented_witness': 'Modern Greek Chrysostom text as '
                                                                      'printed in Brightman 1896, attributed '
                                                                      'on printed p. 308 to the Venice 1869 '
                                                                      'Euchologion with Athens 1890 reader '
                                                                      'material. Not the separate Barberini '
                                                                      'manuscript section.',
                                               'status': 'bounded-checked-greek-prayer-selection',
                                               'text_identity': 'Original Greek wording of two bounded '
                                                                'prayer units in the identified 1896 '
                                                                'edition; explicit typography and '
                                                                'speech-block normalization, not a '
                                                                'reconstruction of earlier use.'},
                                     'title': 'Brightman 1896: Greek Chrysostom remembrance, offering and '
                                              'invocation',
                                     'units': [{'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-anamnesis-oblation-checked-greek-3c396481',
                                                'division': 'anaphora',
                                                'element_key': 'anamnesis-oblation',
                                                'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-anamnesis-oblation-facsimile',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.byzantine-modern-text-sources'],
                                                'facsimile_pdf_page': '492',
                                                'language': 'grc',
                                                'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-anamnesis-oblation',
                                                'printed_page': '386',
                                                'source_order': 1,
                                                'text_sha256': 'd423124934d7134070c446092e42ed7cb4a9a22b34371a40effe2ca791c02885',
                                                'unit_id': 'unit.brightman-1896.greek-chrysostom.anaphora.anamnesis-oblation'},
                                               {'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-invocation-gifts-checked-greek-68a9876c',
                                                'division': 'anaphora',
                                                'element_key': 'invocation-gifts',
                                                'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-invocation-gifts-facsimile',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                        'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.byzantine-modern-text-sources'],
                                                'facsimile_pdf_page': '492,493',
                                                'language': 'grc',
                                                'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.chrysostom-invocation-gifts',
                                                'printed_page': '386–387',
                                                'source_order': 2,
                                                'text_sha256': '5479fe984a2db7f9da1ba3a74356e286ad47ba777f811c3169fdf76a1617a98a',
                                                'unit_id': 'unit.brightman-1896.greek-chrysostom.anaphora.invocation-gifts'}],
                                     'witness_date': '1896 printed edition; modern text attributed by '
                                                     'Brightman to Venice 1869'},
 'brightman-1896-greek-james': {'edition_id': 'edition.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1',
                                'scope': {'omitted_book_divisions': ['The rest of the anaphora and liturgy',
                                                                     'Rubrics, speaker cues, '
                                                                     'diaconal/congregational responses and '
                                                                     'apparatus',
                                                                     'Other constituent liturgies in the '
                                                                     'volume'],
                                          'represented_witness': 'Greek James as printed in Brightman 1896 '
                                                                 'from Paris Bibliothèque nationale MS '
                                                                 'graec. 2509, ff. 194–210, according to '
                                                                 'printed p. 2. Its manuscript date is '
                                                                 'source-stated fifteenth century after the '
                                                                 'printed p. cii correction; the manuscript '
                                                                 'itself was not inspected. This is not the '
                                                                 'separately printed Syriac James text.',
                                          'status': 'bounded-checked-greek-prayer-selection',
                                          'text_identity': 'Original Greek wording of two bounded prayer '
                                                           'units in the identified 1896 edition; explicit '
                                                           'typography and speech-block normalization, not a '
                                                           'reconstruction of earlier use.'},
                                'title': 'Brightman 1896: Greek James remembrance, offering and invocation',
                                'units': [{'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-anamnesis-oblation-checked-greek-9e6745c8',
                                           'division': 'anaphora',
                                           'element_key': 'anamnesis-oblation',
                                           'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-anamnesis-oblation-facsimile',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.greek-james-source-and-corrigendum'],
                                           'facsimile_pdf_page': '158,159',
                                           'language': 'grc',
                                           'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-anamnesis-oblation',
                                           'printed_page': '52–53',
                                           'source_order': 1,
                                           'text_sha256': '99360800128e40b9fe59723cebc4cd0513db05a7aec892c98f5adaef67d7f37a',
                                           'unit_id': 'unit.brightman-1896.greek-james.anaphora.anamnesis-oblation'},
                                          {'artifact_id': 'artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-invocation-gifts-checked-greek-0844d792',
                                           'division': 'anaphora',
                                           'element_key': 'invocation-gifts',
                                           'evidence_source_ids': ['artifact.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.ia-pdf-254f7d21',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-invocation-gifts-facsimile',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.editorial-typography',
                                                                   'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.greek-james-source-and-corrigendum'],
                                           'facsimile_pdf_page': '159,160',
                                           'language': 'grc',
                                           'passage_id': 'passage.frank-edward-brightman.liturgies-eastern-and-western.1896-oxford-clarendon-volume-1.james-invocation-gifts',
                                           'printed_page': '53–54',
                                           'source_order': 2,
                                           'text_sha256': 'eff48580f671663ab9e2c9fc71f0ddef0a8d622e7698ed3bfaaf346d92bbab52',
                                           'unit_id': 'unit.brightman-1896.greek-james.anaphora.invocation-gifts'}],
                                'witness_date': '1896 printed edition; source-stated fifteenth-century Paris '
                                                'gr. 2509, after Brightman’s corrigendum'},
 'warner-1915-stowe-mass-prayers': {'edition_id': 'edition.catholic-church.stowe-missal.warner-1915-vol-2',
                                    'scope': {'date_roles': 'target_date identifies the historical printed '
                                                            'edition; this adapter assigns no exact '
                                                            'manuscript date',
                                              'omitted_book_divisions': ['all prayers outside the explicitly '
                                                                         'selected units',
                                                                         'critical apparatus and editorial '
                                                                         'introduction',
                                                                         'all other ritual, rubrical and '
                                                                         'supplemental material'],
                                              'represented_witness': 'Royal Irish Academy MS D. II. 3 as '
                                                                     "mediated by Warner's 1915 printed "
                                                                     'text; layers, expansions and apparatus '
                                                                     'are those of the critical edition',
                                              'status': 'selected-complete-prayers',
                                              'text_identity': 'Bounded normalized native-language text from '
                                                               'the identified critical edition; apparatus '
                                                               'and uncollected units excluded'},
                                    'title': 'Warner 1915 Stowe Missal: Sanctus and two Canon prayers',
                                    'units': [{'artifact_id': 'artifact.catholic-church.stowe-missal.warner-1915-vol-2.sanctus-checked-latin-27b79875',
                                               'division': 'praefatio',
                                               'element_key': 'sanctus',
                                               'evidence_source_ids': ['artifact.catholic-church.stowe-missal.warner-1915-vol-2.ia-scan-27c6070e'],
                                               'facsimile_pdf_page': 96,
                                               'language': 'la',
                                               'passage_id': 'passage.catholic-church.stowe-missal.warner-1915-vol-2.sanctus',
                                               'printed_page': '10',
                                               'source_order': 1,
                                               'text_sha256': '3796eb71df0487f317f1039e1bea4a32126c189068d5d11b83e05524fa10b798',
                                               'unit_id': 'unit.warner-1915.stowe.praefatio.sanctus'},
                                              {'artifact_id': 'artifact.catholic-church.stowe-missal.warner-1915-vol-2.canon-hanc-igitur-checked-latin-7465da67',
                                               'division': 'canon-missae',
                                               'element_key': 'hanc-igitur',
                                               'evidence_source_ids': ['artifact.catholic-church.stowe-missal.warner-1915-vol-2.ia-scan-27c6070e'],
                                               'facsimile_pdf_page': 98,
                                               'language': 'la',
                                               'passage_id': 'passage.catholic-church.stowe-missal.warner-1915-vol-2.canon-hanc-igitur',
                                               'printed_page': '12',
                                               'source_order': 2,
                                               'text_sha256': '30ad19b30cef8ad7a6df62c56a7ff2cdea94fe88eb1626d0254ef979ef4e1252',
                                               'unit_id': 'unit.warner-1915.stowe.canon-missae.hanc-igitur'},
                                              {'artifact_id': 'artifact.catholic-church.stowe-missal.warner-1915-vol-2.canon-quam-oblationem-checked-latin-e404c122',
                                               'division': 'canon-missae',
                                               'element_key': 'quam-oblationem',
                                               'evidence_source_ids': ['artifact.catholic-church.stowe-missal.warner-1915-vol-2.ia-scan-27c6070e'],
                                               'facsimile_pdf_page': 98,
                                               'language': 'la',
                                               'passage_id': 'passage.catholic-church.stowe-missal.warner-1915-vol-2.canon-quam-oblationem',
                                               'printed_page': '12',
                                               'source_order': 3,
                                               'text_sha256': '18096be7fc73c46fb41307756342c0e85a2f9c2b24454d6d7a2f703d8a424378',
                                               'unit_id': 'unit.warner-1915.stowe.canon-missae.quam-oblationem'}],
                                    'witness_date': None},
 'wilson-1894-gelasian-canon-prayers': {'edition_id': 'edition.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894',
                                        'scope': {'date_roles': 'target_date identifies the historical '
                                                                'printed edition; this adapter assigns no '
                                                                'exact manuscript date',
                                                  'omitted_book_divisions': ['all prayers outside the '
                                                                             'explicitly selected units',
                                                                             'critical apparatus and '
                                                                             'editorial introduction',
                                                                             'all other ritual, rubrical and '
                                                                             'supplemental material'],
                                                  'represented_witness': 'Vatican Reg. lat. 316 as mediated '
                                                                         "by Wilson's 1894 critical edition; "
                                                                         'no new manuscript collation',
                                                  'status': 'selected-complete-prayers',
                                                  'text_identity': 'Bounded normalized native-language text '
                                                                   'from the identified critical edition; '
                                                                   'apparatus and uncollected units '
                                                                   'excluded'},
                                        'title': 'Wilson 1894 Gelasian Canon: Hanc igitur and Quam '
                                                 'oblationem',
                                        'units': [{'artifact_id': 'artifact.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894.canon-hanc-igitur-checked-latin-75df4acf',
                                                   'division': 'canon-missae',
                                                   'element_key': 'hanc-igitur',
                                                   'evidence_source_ids': ['artifact.anonymous.gelasian-sacramentary.wilson-clarendon-1894.printed-p235-image-d98c2326'],
                                                   'facsimile_pdf_page': 328,
                                                   'language': 'la',
                                                   'passage_id': 'passage.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894.canon-hanc-igitur',
                                                   'printed_page': '235',
                                                   'source_order': 1,
                                                   'text_sha256': '91d5e24ad22d131ba8086f2d394c6e1d0ddbaa2795087c89fed5a2260a483bfb',
                                                   'unit_id': 'unit.wilson-1894.gelasian.canon-missae.hanc-igitur'},
                                                  {'artifact_id': 'artifact.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894.canon-quam-oblationem-checked-latin-e01e1083',
                                                   'division': 'canon-missae',
                                                   'element_key': 'quam-oblationem',
                                                   'evidence_source_ids': ['artifact.anonymous.gelasian-sacramentary.wilson-clarendon-1894.printed-p235-image-d98c2326'],
                                                   'facsimile_pdf_page': 328,
                                                   'language': 'la',
                                                   'passage_id': 'passage.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894.canon-quam-oblationem',
                                                   'printed_page': '235',
                                                   'source_order': 2,
                                                   'text_sha256': 'ebe2f0b6c0222d064ce2da46220e62306228bc3f7f83fd5ffbe08284eee36683',
                                                   'unit_id': 'unit.wilson-1894.gelasian.canon-missae.quam-oblationem'}],
                                        'witness_date': None},
 'wilson-1915-gregorian-canon-prayers': {'edition_id': 'edition.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915',
                                         'scope': {'date_roles': 'target_date identifies the historical '
                                                                 'printed edition; this adapter assigns no '
                                                                 'exact manuscript date',
                                                   'omitted_book_divisions': ['all prayers outside the '
                                                                              'explicitly selected units',
                                                                              'critical apparatus and '
                                                                              'editorial introduction',
                                                                              'all other ritual, rubrical '
                                                                              'and supplemental material'],
                                                   'represented_witness': 'R, Vatican Reginae 337, as '
                                                                          "mediated by Wilson's 1915 "
                                                                          'critical edition; no new '
                                                                          'manuscript collation',
                                                   'status': 'selected-complete-prayers',
                                                   'text_identity': 'Bounded normalized native-language text '
                                                                    'from the identified critical edition; '
                                                                    'apparatus and uncollected units '
                                                                    'excluded'},
                                         'title': 'Wilson 1915 Gregorian Canon: Hanc igitur and Quam '
                                                  'oblationem',
                                         'units': [{'artifact_id': 'artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-hanc-igitur-checked-latin-b46e0e89',
                                                    'division': 'canon-missae',
                                                    'element_key': 'hanc-igitur',
                                                    'evidence_source_ids': ['artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7'],
                                                    'facsimile_pdf_page': 60,
                                                    'language': 'la',
                                                    'passage_id': 'passage.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-hanc-igitur',
                                                    'printed_page': '2',
                                                    'source_order': 1,
                                                    'text_sha256': 'fd9e64a913ca9147428be52dc932c3fac0a48723bd9afb04182963632a8b732b',
                                                    'unit_id': 'unit.wilson-1915.gregorian.canon-missae.hanc-igitur'},
                                                   {'artifact_id': 'artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-quam-oblationem-checked-latin-94b63de8',
                                                    'division': 'canon-missae',
                                                    'element_key': 'quam-oblationem',
                                                    'evidence_source_ids': ['artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7'],
                                                    'facsimile_pdf_page': [60, 61],
                                                    'language': 'la',
                                                    'passage_id': 'passage.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.canon-quam-oblationem',
                                                    'printed_page': '2-3',
                                                    'source_order': 2,
                                                    'text_sha256': '19287cda6b3f4d8a027e0cbcc63d4c2399a22827ab75668e1294e596f796d734',
                                                    'unit_id': 'unit.wilson-1915.gregorian.canon-missae.quam-oblationem'}],
                                         'witness_date': None}}
CHECKED_PASSAGE_SETS.update({'cistercian-1606-latin-ordinary': {'title': 'Cistercian missal 1606: three selected Ordinary prayers',
                                    'edition_id': 'edition.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606',
                                    'witness_date': '1606 printed edition; dates earlier cited acts '
                                                    'separately',
                                    'scope': {'status': 'bounded-checked-latin-ordinary-selection',
                                              'represented_witness': 'The identified Paris 1606 Cistercian '
                                                                     'missal, original Latin printed '
                                                                     'wording.',
                                              'text_identity': 'Confiteor, Suscipe Trinitas and Orate '
                                                               'dialogue; normalized spelling presentation '
                                                               'and recoverable spoken blocks, independently '
                                                               'checked against retained page images.',
                                              'omitted_book_divisions': ['All other Ordinary prayers',
                                                                         'Propers, calendar and rites '
                                                                         'elsewhere in the volume',
                                                                         'Red rubrics and response cue '
                                                                         'glyphs from the spoken comparison '
                                                                         'body; their selected context '
                                                                         'remains in provenance']},
                                    'units': [{'unit_id': 'unit.cistercian-1606.ordinary.confiteor',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.confiteor',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.confiteor-checked-latin-60e1426e',
                                               'text_sha256': 'ae1ed27ae22ae246c788fc249b3908304672177145da2d8b12702108912030f5',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'preparatory-prayers',
                                               'kind': 'prayer',
                                               'element_key': 'confiteor',
                                               'source_order': 1,
                                               'printed_page': '180',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.bsb-canvas-00234-7c8474ea',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.confiteor-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.title-and-imprint']},
                                              {'unit_id': 'unit.cistercian-1606.ordinary.suscipe-trinitas',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.suscipe-trinitas',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.suscipe-trinitas-checked-latin-0c61e53d',
                                               'text_sha256': 'f4ef4201b6fd2a2d3b81da889d8706d698d73f6c14e36d2e7f73b291820b76ac',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'offertory',
                                               'kind': 'prayer',
                                               'element_key': 'suscipe-trinitas',
                                               'source_order': 2,
                                               'printed_page': '181',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.bsb-canvas-00235-2646b0f5',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.suscipe-trinitas-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.title-and-imprint']},
                                              {'unit_id': 'unit.cistercian-1606.ordinary.orate-response',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.orate-response',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.orate-response-checked-latin-2bab0892',
                                               'text_sha256': '4a26e65f009e5e81bd72c1e051311bda55ab919198e23ead1c53f21c3fb5f516',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'offertory',
                                               'kind': 'dialogue',
                                               'element_key': 'orate-response',
                                               'source_order': 3,
                                               'printed_page': '181',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.bsb-canvas-00235-2646b0f5',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.orate-response-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-marnef-cavellat-1606.title-and-imprint']}]},
 'cistercian-1657-latin-ordinary': {'title': 'Cistercian missal 1657: three selected Ordinary prayers',
                                    'edition_id': 'edition.cistercian-order.missale-cisterciense.paris-cramoisy-1657',
                                    'witness_date': '1657 printed edition; dates earlier cited acts '
                                                    'separately',
                                    'scope': {'status': 'bounded-checked-latin-ordinary-selection',
                                              'represented_witness': 'The identified Paris 1657 Cistercian '
                                                                     'missal, original Latin printed '
                                                                     'wording.',
                                              'text_identity': 'Confiteor, Suscipe Trinitas and Orate '
                                                               'dialogue; normalized spelling presentation '
                                                               'and recoverable spoken blocks, independently '
                                                               'checked against retained page images.',
                                              'omitted_book_divisions': ['All other Ordinary prayers',
                                                                         'Propers, calendar and rites '
                                                                         'elsewhere in the volume',
                                                                         'Red rubrics and response cue '
                                                                         'glyphs from the spoken comparison '
                                                                         'body; their selected context '
                                                                         'remains in provenance']},
                                    'units': [{'unit_id': 'unit.cistercian-1657.ordinary.confiteor',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.confiteor',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.confiteor-checked-latin-b2321dac',
                                               'text_sha256': '29f922326cfa06d28bf797bbb0a2f0e37bf648ef9e2b96192e38242ded70fe5d',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'preparatory-prayers',
                                               'kind': 'prayer',
                                               'element_key': 'confiteor',
                                               'source_order': 1,
                                               'printed_page': '169',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.fides-page-0231-jpeg-ef6deece',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.confiteor-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.title-and-imprint']},
                                              {'unit_id': 'unit.cistercian-1657.ordinary.suscipe-trinitas',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.suscipe-trinitas',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.suscipe-trinitas-checked-latin-6da6f1b5',
                                               'text_sha256': '3088e7f4905afabe0f2e384ed69a33c58342b21de8a79c7e431c655a174a07de',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'offertory',
                                               'kind': 'prayer',
                                               'element_key': 'suscipe-trinitas',
                                               'source_order': 2,
                                               'printed_page': '174',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.fides-page-0236-jpeg-f461bff9',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.suscipe-trinitas-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.title-and-imprint',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.offertory-placement-host',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.offertory-placement-chalice']},
                                              {'unit_id': 'unit.cistercian-1657.ordinary.orate-response',
                                               'passage_id': 'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.orate-response',
                                               'artifact_id': 'artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.orate-response-checked-latin-a362cf3f',
                                               'text_sha256': '27c6a6fe46613aef99abc25c7ef2602fa8b9ac52a57e9af2f54cad3c30b62e4f',
                                               'language': 'la',
                                               'division': 'ordinary',
                                               'part': 'offertory',
                                               'kind': 'dialogue',
                                               'element_key': 'orate-response',
                                               'source_order': 3,
                                               'printed_page': '174',
                                               'evidence_source_ids': ['artifact.cistercian-order.missale-cisterciense.paris-cramoisy-1657.fides-page-0236-jpeg-f461bff9',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.orate-response-facsimile',
                                                                       'passage.cistercian-order.missale-cisterciense.paris-cramoisy-1657.title-and-imprint']}]}})
CHECKED_PASSAGE_SETS.update({'dominican-1550-suscepimus': {'edition_id': 'edition.order-of-preachers.missale.1550-venice',
                               'title': 'Dominican 1550: Suscepimus Deus collect',
                               'witness_date': '1550 printed edition',
                               'scope': {'status': 'bounded-checked-latin-collect-selection',
                                         'represented_witness': 'Missale ad usum fratrum Praedicatorum '
                                                                'Sancti Dominici; Venice, 1550',
                                         'text_identity': 'One collect of the Suscepimus Deus formulary. The '
                                                          'pairing is anchored by that named formulary: 1550 '
                                                          'Dominica octava after Trinity versus 1604 '
                                                          'Dominica sexta after the octave of Trinity. The '
                                                          'selected collect is complete as printed but the '
                                                          'full spoken conclusion is abbreviated by the '
                                                          'source. Other formulary items, rubrics, the '
                                                          'ordinary, sanctoral and remaining book are '
                                                          'excluded. No immediate ancestry or local '
                                                          'reception is inferred.',
                                         'omitted_book_divisions': ['Other Suscepimus formulary elements and '
                                                                    'rubrics',
                                                                    'Ordinary, remaining temporale, '
                                                                    'sanctoral and other book divisions']},
                               'units': [{'unit_id': 'unit.dominican-1550-suscepimus.suscepimus-collect',
                                          'passage_id': 'passage.order-of-preachers.missale.1550-venice.suscepimus-collect',
                                          'artifact_id': 'artifact.order-of-preachers.missale.1550-venice.suscepimus-collect-checked-latin-d5fb591c',
                                          'text_sha256': '70806af820909d2ed1493cf677a2f40c4aec8f99c421d4d9143aa34ce4a8fd5e',
                                          'language': 'la',
                                          'division': 'temporale',
                                          'element_key': 'suscepimus-collect',
                                          'source_order': 1,
                                          'printed_page': '125r',
                                          'facsimile_pdf_page': '289',
                                          'evidence_source_ids': ['artifact.order-of-preachers.missale.1550-venice.pdf-page-289-image-1a0d3a7a',
                                                                  'passage.order-of-preachers.missale.1550-venice.suscepimus-folio-125r',
                                                                  'passage.order-of-preachers.missale.1550-venice.title'],
                                          'kind': 'prayer',
                                          'part': 'collect'}]},
 'dominican-1604-suscepimus': {'edition_id': 'edition.order-of-preachers.missale.1604-rome-xavierre',
                               'title': 'Dominican 1604: Suscepimus Deus collect',
                               'witness_date': '1604 printed edition',
                               'scope': {'status': 'bounded-checked-latin-collect-selection',
                                         'represented_witness': 'Missale juxta ritum sacri ordinis '
                                                                'Praedicatorum S. P. N. Dominici; Rome: ex '
                                                                'typographia Alfonsi Ciacconi, apud Carolum '
                                                                'Vulliettum, 1604',
                                         'text_identity': 'One collect of the Suscepimus Deus formulary. The '
                                                          'pairing is anchored by that named formulary: 1550 '
                                                          'Dominica octava after Trinity versus 1604 '
                                                          'Dominica sexta after the octave of Trinity. The '
                                                          'selected collect is complete as printed but the '
                                                          'full spoken conclusion is abbreviated by the '
                                                          'source. Other formulary items, rubrics, the '
                                                          'ordinary, sanctoral and remaining book are '
                                                          'excluded. No immediate ancestry or local '
                                                          'reception is inferred.',
                                         'omitted_book_divisions': ['Other Suscepimus formulary elements and '
                                                                    'rubrics',
                                                                    'Ordinary, remaining temporale, '
                                                                    'sanctoral and other book divisions']},
                               'units': [{'unit_id': 'unit.dominican-1604-suscepimus.suscepimus-collect',
                                          'passage_id': 'passage.order-of-preachers.missale.1604-rome-xavierre.suscepimus-collect',
                                          'artifact_id': 'artifact.order-of-preachers.missale.1604-rome-xavierre.suscepimus-collect-checked-latin-72fc670a',
                                          'text_sha256': '8861302457a0775f9710d82ad21c88492d80915de577db7419a796bd4d660c57',
                                          'language': 'la',
                                          'division': 'temporale',
                                          'element_key': 'suscepimus-collect',
                                          'source_order': 1,
                                          'printed_page': '238',
                                          'facsimile_pdf_page': '314',
                                          'evidence_source_ids': ['artifact.order-of-preachers.missale.1604-rome-xavierre.pdf-page-314-image-b5893d5a',
                                                                  'passage.order-of-preachers.missale.1604-rome-xavierre.suscepimus-page-238',
                                                                  'passage.order-of-preachers.missale.1604-rome-xavierre.title'],
                                          'kind': 'prayer',
                                          'part': 'collect'}]},
 'carmelite-1574-october-calendar': {'edition_id': 'edition.carmelite-order.missale.1574-venice-giunta',
                                     'title': 'Carmelite 1574: October 5 calendar entry',
                                     'witness_date': '1574 printed edition',
                                     'scope': {'status': 'bounded-checked-latin-calendar-row',
                                               'represented_witness': 'Missale antique professionis '
                                                                      'Regularium beatissime Dei genitricis '
                                                                      'semperque virginis Marie de Monte '
                                                                      'Carmelo; Venice: apud Iuntas, 1574',
                                               'text_identity': 'Bounded October 5 calendar row, not a Mass '
                                                                'prayer. An empty feast cell in 1574 is not '
                                                                'a claim that Teresa or a devotion is absent '
                                                                'throughout the book. The 1621 printed date '
                                                                'is October 5; no date correction to October '
                                                                '15 is made. No introduction date or '
                                                                'immediate ancestry is established.',
                                               'omitted_book_divisions': ['Other calendar rows and '
                                                                          'computistical columns',
                                                                          'Ordinary, propers, readings and '
                                                                          'rubrics']},
                                     'units': [{'unit_id': 'unit.carmelite-1574-october-calendar.october-05-calendar-entry',
                                                'passage_id': 'passage.carmelite-order.missale.1574-venice-giunta.october-05-calendar-entry',
                                                'artifact_id': 'artifact.carmelite-order.missale.1574-venice-giunta.october-05-calendar-entry-checked-latin-f0b5c2c2',
                                                'text_sha256': 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
                                                'language': 'la',
                                                'division': 'calendar',
                                                'element_key': 'calendar-october-05',
                                                'source_order': 1,
                                                'printed_page': 'unnumbered October calendar',
                                                'facsimile_pdf_page': '20',
                                                'evidence_source_ids': ['artifact.carmelite-order.missale.1574-venice-giunta.pdf-page-20-image-e1380012',
                                                                        'passage.carmelite-order.missale.1574-venice-giunta.october-calendar',
                                                                        'passage.carmelite-order.missale.1574-venice-giunta.title'],
                                                'kind': 'calendar-entry',
                                                'part': 'calendar'}]},
 'carmelite-1621-october-calendar': {'edition_id': 'edition.carmelite-order.missale.1621-venice-giunta',
                                     'title': 'Carmelite 1621: October 5 calendar entry',
                                     'witness_date': '1621 printed edition',
                                     'scope': {'status': 'bounded-checked-latin-calendar-row',
                                               'represented_witness': 'Missale fratrum Carmelitarum Ordinis '
                                                                      'Beatae Dei Genitricis Mariae; Venice: '
                                                                      'apud Iuntas, 1621',
                                               'text_identity': 'Bounded October 5 calendar row, not a Mass '
                                                                'prayer. An empty feast cell in 1574 is not '
                                                                'a claim that Teresa or a devotion is absent '
                                                                'throughout the book. The 1621 printed date '
                                                                'is October 5; no date correction to October '
                                                                '15 is made. No introduction date or '
                                                                'immediate ancestry is established.',
                                               'omitted_book_divisions': ['Other calendar rows and '
                                                                          'computistical columns',
                                                                          'Ordinary, propers, readings and '
                                                                          'rubrics']},
                                     'units': [{'unit_id': 'unit.carmelite-1621-october-calendar.october-05-calendar-entry',
                                                'passage_id': 'passage.carmelite-order.missale.1621-venice-giunta.october-05-calendar-entry',
                                                'artifact_id': 'artifact.carmelite-order.missale.1621-venice-giunta.october-05-calendar-entry-checked-latin-3033d681',
                                                'text_sha256': 'c33b45602d801fdd84527fbba77701b560c80bd425b983e259d0a5b4b7a26515',
                                                'language': 'la',
                                                'division': 'calendar',
                                                'element_key': 'calendar-october-05',
                                                'source_order': 1,
                                                'printed_page': 'unnumbered October calendar',
                                                'facsimile_pdf_page': '22',
                                                'evidence_source_ids': ['artifact.carmelite-order.missale.1621-venice-giunta.pdf-page-22-image-87dc3360',
                                                                        'passage.carmelite-order.missale.1621-venice-giunta.october-calendar',
                                                                        'passage.carmelite-order.missale.1621-venice-giunta.title'],
                                                'kind': 'calendar-entry',
                                                'part': 'calendar'}]}})
ORDINARY_DIVISIONS = (
    "ordinarium-praeparatio", "ordinarium-oblatio", "praefationes", "canon-missae",
    "ordinarium-communio", "ordinarium-conclusio",
)
SOURCE_FIELDS = frozenset({
    "id", "record_type", "title", "publication", "date", "authority", "language", "jurisdiction",
    "work_id", "edition_id", "artifact_id", "segment_id", "artifact_sha256", "physical_line_ranges",
    "artifact_page_ranges", "locus", "states", "verified_on", "source_url", "provenance", "retrieved",
    "artifact_type", "media_type", "storage", "rights_status", "rights_basis", "rights_jurisdiction",
    "sha256", "byte_size", "path", "derived_from", "projected_from", "transformation", "support_artifacts", "page_count",
})


class AdapterError(ValueError):
    """A source, identity, or publication prerequisite is not satisfied."""


def adapter_ids() -> tuple[str, ...]:
    return ("roman-1962-propers", "cummiskey-1861-latin-ordinary", "wilson-1915-gregorian-canon-memento",
            *sorted(CHECKED_PASSAGE_SETS))


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _tool_inputs() -> list[dict]:
    """Pin required implementation/policy files from the executing checkout.

    These paths are relative to ROOT, independently of an alternate data root.
    Missing trusted inputs are errors, never silently incomplete provenance.
    """
    result = []
    for relative in sorted(TOOL_INPUT_PATHS):
        payload = (ROOT / relative).read_bytes()
        result.append({"path": relative, "sha256": _sha(payload), "byte_size": len(payload)})
    return result


def _load_library(root: Path):
    # Executable code comes only from this checkout, never from a data root.
    name = "_eucharistic_texts_source_library"
    if name not in sys.modules:
        loader = importlib.machinery.SourceFileLoader(name, str(ROOT / "tools/source-library"))
        spec = importlib.util.spec_from_loader(name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        loader.exec_module(module)
    library = sys.modules[name].load_library(root, check_binding_fingerprints=False)
    if library.errors:
        raise AdapterError("Source library prevents text export: " + "; ".join(library.errors))
    return library


class _Sources:
    def __init__(self, root: Path, library):
        self.root = root
        self.library = library
        self.records = {key: {**record.data, "record_type": record.record_type, "id": key}
                        for key, record in library.records.items()}
        self.used: set[str] = set()
        self.inputs: dict[str, dict] = {}

    def pin(self, path: Path) -> bytes:
        path = path.resolve()
        if not path.is_relative_to(self.root):
            raise AdapterError("Source input is outside its repository root")
        payload = path.read_bytes()
        rel = path.relative_to(self.root).as_posix()
        self.inputs[rel] = {"path": rel, "sha256": _sha(payload), "byte_size": len(payload)}
        return payload

    def use(self, source_id: str) -> dict:
        if source_id not in self.records:
            raise AdapterError(f"Unregistered source: {source_id}")
        data = self.records[source_id]
        if source_id in self.used:
            return data
        self.used.add(source_id)
        self.pin(self.library.records[source_id].path)
        for field in ("work_id", "edition_id", "artifact_id", "segment_id", "derived_from"):
            parent = data.get(field)
            if isinstance(parent, str):
                self.use(parent)
        for parent in data.get("projected_from", []):
            self.use(parent)
        for support in data.get("support_artifacts", []):
            self.use(support["artifact_id"])
        if data.get("storage") == "tracked" and data.get("path"):
            self.payload(data)
        return data

    def payload(self, artifact: dict) -> bytes:
        if artifact.get("storage") != "tracked" or not artifact.get("path"):
            raise AdapterError(f"No tracked payload: {artifact['id']}")
        blob = self.pin(self.root / artifact["path"])
        if _sha(blob) != artifact.get("sha256"):
            raise AdapterError(f"Artifact hash mismatch: {artifact['id']}")
        return blob

    def verify_projection(self, passage: dict, text: str) -> None:
        """Compare with the owning projection, allowing its printed line wraps."""
        artifact = self.use(passage.get("artifact_id", ""))
        if passage.get("artifact_sha256") != artifact.get("sha256"):
            raise AdapterError(f"Passage artifact hash mismatch: {passage['id']}")
        ranges = passage.get("physical_line_ranges")
        if not ranges:
            raise AdapterError(f"Projection has no bounded text: {passage['id']}")
        lines = self.payload(artifact).decode("utf-8").splitlines()
        selected = []
        for start, end in ranges:
            if not 1 <= start <= end <= len(lines):
                raise AdapterError(f"Projection range outside artifact: {passage['id']}")
            selected.extend(lines[start - 1:end])
        if " ".join("\n".join(selected).split()) != " ".join(text.split()):
            raise AdapterError(f"Calendar text differs from owning projection: {passage['id']}")

    def metadata(self) -> list[dict]:
        return [{"manifest_path": self.library.records[key].path.relative_to(self.root).as_posix(),
                 "manifest_sha256": self.inputs[self.library.records[key].path.relative_to(self.root).as_posix()]["sha256"],
                 **{field: value for field, value in self.records[key].items() if field in SOURCE_FIELDS}}
                for key in sorted(self.used)]


def _proper_units(sources: _Sources) -> dict:
    calendar_root = sources.root / "src/sources/calendars"
    path = calendar_root / "roman-1962/propers.yaml"
    ledger = sources.root / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
    sources.pin(path)
    sources.pin(ledger)
    document = _calendars.load_document(calendar_root, "roman-1962", effective=False)
    records, problems = _proper_latin.publication_records(calendar_root, "roman-1962", registered_sources=sources.records)
    problems.extend(_proper_latin.sidecar_problems(
        [path], inventory_root=ledger.parent, required=True, registered_source_ids=set(sources.records)))
    if problems:
        raise AdapterError("Latin publication gate: " + "; ".join(problems))
    masses = {}
    for section_key, section in document["sections"].items():
        for order, mass in enumerate(section.get("masses", []), 1):
            masses[mass["key"]] = {
                "section": section_key, "section_kind": section["kind"], "source_mass_order": order,
                **{field: mass[field] for field in ("key", "name", "registry", "date", "season", "rank") if field in mass},
            }
    units, omitted = [], []
    for order, (key, text, state) in enumerate(_proper_latin.body_owners(document), 1):
        if state != "present":
            omitted.append({"identity": key.as_dict(), "body_status": state, "reason": "Quarantined body; wording not exported"})
            continue
        decision = _proper_latin.decision_for(key, text, records)
        permission = decision.projection({"public-git", "corpus-data"})
        if not decision.permits({"public-git", "corpus-data"}):
            raise AdapterError(f"Present body lacks export permission: {key.label()}: {permission['reason']}")
        if decision.provenance_status != "collated" or decision.relationship != "editorial-projection-exact-to-target":
            raise AdapterError(f"Unsupported provenance relationship: {key.label()}")
        source = sources.use(decision.source_id)
        target = sources.use(decision.verification_source_id)
        if target.get("edition_id") != PROPER_TARGET_EDITION:
            raise AdapterError(f"Verification target edition mismatch: {key.label()}: "
                               f"expected {PROPER_TARGET_EDITION}, got {target.get('edition_id')!r}")
        sources.verify_projection(source, text)
        for source_id in decision.publication_source_ids:
            sources.use(source_id)
        identity = {"calendar": "roman-1962", **key.as_dict()}
        identity_hash = _sha(json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8"))
        units.append({
            "unit_id": "unit.roman-1962.proper." + identity_hash[:24],
            "content_id": "sha256:" + decision.text_sha256,
            "language": "la", "text": text, "text_sha256": decision.text_sha256,
            "identity": identity, "source_order": order, "mass": masses[key.mass],
            "formulary": {"mass": key.mass, "form": key.form}, "slot": key.proper,
            "text_edition_id": source["edition_id"], "target_edition_id": target["edition_id"],
            "transcription_kind": "editorial-projection", "diplomatic": False,
            "source_id": decision.source_id, **permission,
        })
    return {
        "title": "Roman 1962 Latin Proper editorial projections", "units": units,
        "target_date": sources.use(PROPER_TARGET_EDITION)["date"],
        "witness_date": None, "reviewed_on": None,
        "scope": {
            "status": "partial", "whole_book_complete": False, "reference_expansion_performed": False,
            "no_historical_backprojection": True,
            "omitted_book_divisions": ["front matter", "calendar and computus", "general rubrics and Ritus servandus",
                "Ordinary and Canon", "complete Preface series", "unrepresented ritual/votive/dead/local formularies",
                "literal Scripture readings and chants represented only by citations", "unavailable and quarantined Proper bodies"],
            "text_identity": "Project editorial projection with 1962 target verification; not a diplomatic historical antecedent",
        },
        "omitted_body_owners": omitted,
        "counts": {"units": len(units), "unique_text_hashes": len({u["text_sha256"] for u in units}),
                   "mass_identities_with_text": len({u["identity"]["mass"] for u in units}),
                   "by_section": dict(Counter(u["mass"]["section_kind"] for u in units)),
                   "by_text_edition": dict(Counter(u["text_edition_id"] for u in units))},
    }


def _tsv(sources: _Sources, artifact: dict) -> list[dict]:
    return list(csv.DictReader(sources.payload(artifact).decode("utf-8").splitlines(), delimiter="\t"))


def _ordinary_units(sources: _Sources) -> dict:
    sources.use(ORDINARY_EDITION)
    units, divisions = [], []
    for division_order, division in enumerate(ORDINARY_DIVISIONS, 1):
        latin_id = "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861." + division + "-la"
        latin = sources.use(latin_id)
        english_id = latin_id[:-3] + "-en"
        english = sources.use(english_id)
        if latin.get("rights_status") != "public-domain" or not latin.get("rights_basis"):
            raise AdapterError(f"Facing-language payload lacks publication basis: {latin_id}")
        if latin.get("edition_id") != ORDINARY_EDITION or english.get("edition_id") != ORDINARY_EDITION:
            raise AdapterError(f"Ordinary artifact has wrong edition: {latin_id}")
        rows, english_rows = _tsv(sources, latin), _tsv(sources, english)
        en_by_key = {row["element_key"]: row for row in english_rows}
        if len(en_by_key) != len(english_rows):
            raise AdapterError(f"Duplicate Ordinary skeleton key: {english_id}")
        present, unit_ids = set(), []
        last_seq = 0
        for line, row in enumerate(rows, 2):
            key = row["element_key"]
            companion = en_by_key.get(key)
            seq = int(row["seq"])
            if key in present or seq <= last_seq or companion is None or row["seq"] != companion["seq"]:
                raise AdapterError(f"Ordinary row identity/order mismatch: {latin_id}/{key}")
            present.add(key)
            last_seq = seq
            unit_id = "unit.cummiskey-1861." + division + "." + key
            unit_ids.append(unit_id)
            text = row["latin"]
            if not text:
                raise AdapterError(f"Empty original-language body: {unit_id}")
            text_hash = _sha(text.encode("utf-8"))
            units.append({
                "unit_id": unit_id, "content_id": "sha256:" + text_hash,
                "language": "grc-Latn" if key in {"kyrie-eleison", "christe-eleison", "kyrie-eleison-repetitio"} else "la",
                "source_column": "latin", "text": text, "text_sha256": text_hash,
                "text_edition_id": ORDINARY_EDITION, "target_edition_id": ORDINARY_EDITION,
                "transcription_kind": "witness-normalized-transcription", "diplomatic": False,
                "division": division, "division_order": division_order, "source_order": seq,
                "element_key": key, "part": row["part"], "kind": companion["kind"], "speaker": companion["speaker"],
                "source_id": latin_id, "source_artifact_sha256": latin["sha256"], "source_physical_line": line,
                "printed_page": row["printed_page"], "ia_leaf": row["ia_leaf"], "source_notes": row["notes"],
                "structural_metadata_source_id": english_id,
                "provenance": {"status": "recorded-page-image-transcription", "new_collation_performed": False,
                    "relation": "same-identified-witness", "artifact_provenance_source_id": latin_id},
                "publication": {"status": "permitted", "basis": "public-domain", "jurisdiction": "United States",
                    "basis_source_id": latin_id, "surfaces": ["public-git", "corpus-data"]},
            })
        omitted = [{"element_key": row["element_key"], "source_order": int(row["seq"]), "kind": row["kind"],
                    "printed_page": row["printed_page"], "reason": "Witness prints no facing Latin; English payload omitted"}
                   for row in english_rows if row["element_key"] not in present]
        divisions.append({"division": division, "unit_ids": unit_ids, "latin_column_rows": len(rows),
                          "source_skeleton_rows": len(english_rows), "omitted_non_latin_blocks": omitted,
                          "coverage_basis": latin.get("notes", ""),
                          "completeness": "complete-held-facing-language-column; not the whole bilingual division or book"})
    return {
        "title": "Cummiskey 1861 original-language Ordinary", "edition_id": ORDINARY_EDITION,
        "target_date": sources.use(ORDINARY_EDITION)["date"],
        "witness_date": sources.use(ORDINARY_EDITION)["date"], "reviewed_on": None,
        "units": units, "divisions": divisions,
        "scope": {
            "status": "partial-book; complete-held-facing-language-columns", "whole_book_complete": False,
            "self_contained_division": {"division": "canon-missae", "scope": "Printed Latin prayer/form/dialogue blocks from Te igitur through the concluding Per omnia saecula saeculorum",
                "printed_pages": "xxxiii-xxxix", "ia_leaves": "n43-n49",
                "excluded_variants": "Proper Communicantes/Hanc igitur forms are outside this bounded Canon division"},
            "omitted_book_divisions": ["English wording and English-only rubrics/headings", "temporale", "sanctorale", "Commons",
                "votive and other formularies", "front matter and calendar", "all other book text outside the six retained Ordinary columns"],
            "normalization": "Exact TSV wording; source records describe closed French spacing, small capitals rendered as capitals, omitted cross glyphs noted, and abbreviations retained",
            "not_an_altar_book": True, "not_1920_or_1962_text": True,
        },
        "counts": {"units": len(units), "languages": dict(Counter(u["language"] for u in units)),
                   "by_division": dict(Counter(u["division"] for u in units))},
    }


def _wilson_memento(sources: _Sources) -> dict:
    passage = sources.use(WILSON_MEMENTO_PASSAGE)
    artifact = sources.use(WILSON_MEMENTO_ARTIFACT)
    if (passage.get("edition_id") != WILSON_EDITION or artifact.get("edition_id") != WILSON_EDITION
            or passage.get("artifact_id") != WILSON_MEMENTO_ARTIFACT):
        raise AdapterError("Wilson Memento source edition/artifact identity mismatch")
    if "verified" not in passage.get("states", []) or not passage.get("verified_on"):
        raise AdapterError("Wilson Memento lacks a verified bounded transcription")
    if (artifact.get("rights_status") != "public-domain" or not artifact.get("rights_basis")
            or artifact.get("rights_jurisdiction") != "United States"):
        raise AdapterError("Wilson Memento lacks its public-domain publication basis")
    if (artifact.get("artifact_type") != "normalized-text"
            or passage.get("artifact_sha256") != artifact.get("sha256")
            or passage.get("physical_line_ranges") != [[1, 1]]):
        raise AdapterError("Wilson Memento checked-text extent/hash mismatch")
    blob = sources.payload(artifact)
    if not blob.endswith(b"\n") or blob.count(b"\n") != 1:
        raise AdapterError("Wilson Memento must contain exactly one complete text line")
    text = blob[:-1].decode("utf-8")
    if _sha(text.encode("utf-8")) != WILSON_MEMENTO_TEXT_SHA256:
        raise AdapterError("Wilson Memento differs from its reviewed wording")
    unit = {
        "unit_id": "unit.wilson-1915.gregorian.canon-missae.memento-vivorum",
        "content_id": "sha256:" + WILSON_MEMENTO_TEXT_SHA256, "language": "la",
        "text": text, "text_sha256": WILSON_MEMENTO_TEXT_SHA256,
        "text_edition_id": WILSON_EDITION, "target_edition_id": WILSON_EDITION,
        "transcription_kind": "witness-normalized-transcription", "diplomatic": False,
        "division": "canon-missae", "division_order": 1, "source_order": 1,
        "element_key": "memento-vivorum", "part": "canon", "kind": "prayer",
        "source_id": WILSON_MEMENTO_PASSAGE, "source_artifact_id": WILSON_MEMENTO_ARTIFACT,
        "source_artifact_sha256": artifact["sha256"], "source_physical_line": 1,
        "printed_page": "2", "facsimile_pdf_page": 60,
        "provenance": {"status": "verified-bounded-printed-edition-transcription",
                       "reviewed_on": passage["verified_on"], "source_locator": passage["locus"],
                       "represented_witness": "Wilson's R-based main text (Vatican Reginae 337); not the apparatus or a newly inspected manuscript",
                       "normalization": artifact["transformation"],
                       "apparatus_limit": "Note 6 assigns pro quibus tibi offerimus vel to O (Vatican Ottobonianus 313); this pair does not date its introduction"},
        "publication": {"status": "permitted", "basis": "public-domain", "jurisdiction": "United States",
                        "basis_source_id": WILSON_MEMENTO_ARTIFACT, "surfaces": ["public-git", "corpus-data"]},
    }
    return {
        "title": "Wilson 1915 Gregorian Canon: Memento for the living", "edition_id": WILSON_EDITION,
        "target_date": sources.use(WILSON_EDITION)["date"],
        "witness_date": "ninth century (R, as represented by Wilson 1915; no exact date asserted)",
        "reviewed_on": passage["verified_on"], "units": [unit],
        "scope": {"status": "one-complete-prayer", "whole_book_complete": False,
                  "text_identity": "A bounded normalized transcription of Wilson's 1915 critical-edition main text",
                  "omitted_book_divisions": ["all other Canon prayers", "all other sacramentary text",
                                             "critical apparatus, including the O variant", "front matter and supplements"],
                  "not_direct_manuscript_transcription": True, "no_historical_backprojection": True},
        "counts": {"units": 1, "words": len(text.split()), "languages": {"la": 1}},
    }


def _checked_passages(sources: _Sources, selection: dict) -> dict:
    """Load bounded, verified native-language units from their canonical owners."""
    edition_id = selection["edition_id"]
    edition = sources.use(edition_id)
    units = []
    for chosen in selection["units"]:
        passage = sources.use(chosen["passage_id"])
        artifact = sources.use(chosen["artifact_id"])
        if (passage.get("edition_id") != edition_id or artifact.get("edition_id") != edition_id
                or passage.get("artifact_id") != chosen["artifact_id"]):
            raise AdapterError(f"Checked passage identity mismatch: {chosen['passage_id']}")
        if "verified" not in passage.get("states", []) or not passage.get("verified_on"):
            raise AdapterError(f"Checked passage is not verified: {chosen['passage_id']}")
        if (artifact.get("rights_status") != "public-domain" or not artifact.get("rights_basis")
                or artifact.get("rights_jurisdiction") != "United States"):
            raise AdapterError(f"Checked passage lacks public-domain publication basis: {chosen['artifact_id']}")
        if (artifact.get("artifact_type") != "normalized-text" or passage.get("physical_line_ranges") != [[1, 1]]
                or passage.get("artifact_sha256") != artifact.get("sha256")):
            raise AdapterError(f"Checked passage extent/hash mismatch: {chosen['passage_id']}")
        blob = sources.payload(artifact)
        if not blob.endswith(b"\n") or blob.count(b"\n") != 1 or b"\r" in blob:
            raise AdapterError(f"Checked passage must have one complete text line: {chosen['passage_id']}")
        text = blob[:-1].decode("utf-8")
        if not text or _sha(text.encode("utf-8")) != chosen["text_sha256"]:
            raise AdapterError(f"Checked passage differs from reviewed wording: {chosen['passage_id']}")
        for source_id in chosen.get("evidence_source_ids", []):
            sources.use(source_id)
        units.append({
            **{key: chosen[key] for key in ("unit_id", "language", "division", "element_key", "source_order")},
            **{key: chosen[key] for key in ("printed_page", "facsimile_pdf_page", "kind", "part") if key in chosen},
            "content_id": "sha256:" + chosen["text_sha256"], "text": text, "text_sha256": chosen["text_sha256"],
            "text_edition_id": edition_id, "target_edition_id": edition_id,
            "transcription_kind": "witness-normalized-transcription", "diplomatic": False,
            "source_id": chosen["passage_id"], "source_artifact_id": chosen["artifact_id"],
            "source_artifact_sha256": artifact["sha256"], "source_physical_line": 1,
            "provenance": {"status": "verified-bounded-printed-edition-transcription",
                "reviewed_on": passage["verified_on"], "source_locator": passage["locus"],
                "normalization": artifact["transformation"], "scope": passage.get("context", ""),
                "review_limits": passage.get("notes", ""),
                "evidence_source_ids": chosen.get("evidence_source_ids", [])},
            "publication": {"status": "permitted", "basis": "public-domain", "jurisdiction": "United States",
                "basis_source_id": chosen["artifact_id"], "surfaces": ["public-git", "corpus-data"]},
        })
    reviewed = {unit["provenance"]["reviewed_on"] for unit in units}
    return {"title": selection["title"], "edition_id": edition_id,
            "target_date": edition["date"], "witness_date": selection.get("witness_date"),
            "reviewed_on": next(iter(reviewed)) if len(reviewed) == 1 else None,
            "units": units, "scope": {**selection["scope"], "whole_book_complete": False,
                                      "no_historical_backprojection": True, "not_direct_manuscript_transcription": True},
            "counts": {"units": len(units), "whitespace_tokens": sum(len(u["text"].split()) for u in units),
                       "languages": dict(Counter(u["language"] for u in units))}}


def load_adapter(adapter_id: str, root: Path = ROOT) -> dict:
    """Return a deterministic JSON-compatible snapshot; write no export files.

    Validation errors and present bodies without export permission raise
    AdapterError. Quarantined text-free Proper nodes remain explicit omissions.
    Source-library binding freshness is outside this text-owner adapter's scope.
    """
    if adapter_id not in adapter_ids():
        raise AdapterError(f"Unknown Eucharistic text adapter: {adapter_id}")
    root = Path(root).resolve()
    sources = _Sources(root, _load_library(root))
    try:
        loaders = {"roman-1962-propers": _proper_units, "cummiskey-1861-latin-ordinary": _ordinary_units,
                   "wilson-1915-gregorian-canon-memento": _wilson_memento}
        result = (_checked_passages(sources, CHECKED_PASSAGE_SETS[adapter_id])
                  if adapter_id in CHECKED_PASSAGE_SETS else loaders[adapter_id](sources))
        unit_ids = [unit["unit_id"] for unit in result["units"]]
        if len(set(unit_ids)) != len(unit_ids):
            raise AdapterError("Export repeats a stable unit identity")
        return {"schema": SCHEMA, "adapter_id": adapter_id, **result,
                "sources": sources.metadata(), "inputs": sorted(sources.inputs.values(), key=lambda row: row["path"]),
                "tool_inputs": _tool_inputs(), "tool_input_base": "executing-tool-checkout",
                "historical_comparisons": [],
                "history_semantics": "Evidence snapshot, not an act's additions/deletions. No inferred ancestry or backprojection; uncollected wording is unknown.",
                "verification": {"source_library_valid": True, "source_binding_fingerprints_checked": False,
                                 "new_page_collation_performed": False}}
    except (OSError, KeyError, TypeError, UnicodeError) as error:
        raise AdapterError(f"Cannot export {adapter_id}: {error}") from error
