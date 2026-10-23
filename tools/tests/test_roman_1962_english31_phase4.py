"""Independent full-body source/seed oracles for the authorized English31."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader,module_from_spec
import copy,csv,hashlib,io,json,re,sys,tomllib,unicodedata,unittest
from tools.tests import _source_batch_guards as source_batch
ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/"src/sources/calendars"
LEDGER=ROOT/"src/sources/inventories/roman-1962-proper-translations-v1.toml"
LP="francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945"
CP="eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
def sha(v):return hashlib.sha256(v.encode() if isinstance(v,str) else v).hexdigest()
def identity(r):return (r["mass"],r["form_id"],r["proper"],r["cycle"],r["occurrence"])
def words(v):
 v=v.casefold().replace("æ","ae").replace("œ","oe")
 return re.findall("[a-z]+|[0-9]+","".join(c for c in unicodedata.normalize("NFKD",v) if not unicodedata.combining(c)))
def slug(k):return "--".join(re.sub("[^a-z0-9]+","-",str(v).lower()).strip("-") for v in k)
SOURCE_ORACLES = {'lasance-common-abbot-postcommunion': {'english': 'Together with the reception of Thy sacrament, '
                                                   'O Lord, may the blessed abbot N., protect us '
                                                   'by interceding for us, that we may put into '
                                                   'practice the virtues of his life and partake '
                                                   'of the power of his intercession. Through our '
                                                   'Lord.',
                                        'english_sha256': '54a5415f872792083e60382cd60c58461cf44accc6082b2c3529fa10aa8c170a',
                                        'historical_latin': 'Protegat nos, Domine, cum tui '
                                                            'perceptione sacramenti beatus N. '
                                                            'Abbas, pro nobis intercedendo: ut, et '
                                                            'conversationis ejus experiamur '
                                                            'insignia, et intercessionis '
                                                            'percipiamus suffragia. Per Dominum.',
                                        'pdf_pages': [1378],
                                        'printed_pages': ['1359']},
 'lasance-common-confessor-bishop-1-postcommunion': {'english': 'Grant, we beseech Thee, O '
                                                                'almighty God, that, giving thanks '
                                                                'for the favors we have received, '
                                                                'we may, by the intercession of '
                                                                'blessed N., Thy confessor and '
                                                                'bishop, obtain blessings still '
                                                                'greater. Through our Lord.',
                                                     'english_sha256': 'ffed65c43057c928cff48acebf8ec4c43efd3d467f8d44a3d300445b893fdc47',
                                                     'historical_latin': 'Praesta, quaesumus, '
                                                                         'omnipotens Deus: ut, de '
                                                                         'perceptis muneribus '
                                                                         'gratias exhibentes, '
                                                                         'intercedente beato N. '
                                                                         'Confessore tuo atque '
                                                                         'Pontifice, beneficia '
                                                                         'potiora sumamus. Per '
                                                                         'Dominum.',
                                                     'pdf_pages': [1359],
                                                     'printed_pages': ['1340']},
 'lasance-common-virgin-2-postcommunion': {'english': 'Filled with the bounty of Thy divine gift, '
                                                      'we beseech Thee, O Lord, that, by the '
                                                      'intercession of the blessed N., Thy virgin '
                                                      'and martyr, we may ever live in the '
                                                      'partaking thereof. Through our Lord.',
                                           'english_sha256': '3a11a64879f35aeb333c8c4a0ce57072e175e86b23845525d9524d2479390465',
                                           'historical_latin': 'Divini muneris largitate satiati, '
                                                               'quaesumus, Domine Deus noster: ut, '
                                                               'intercedente beata N. Virgine et '
                                                               'Martyre tua, in ejus semper '
                                                               'participatione vivamus. Per '
                                                               'Dominum.',
                                           'pdf_pages': [1385, 1386],
                                           'printed_pages': ['1366', '1367']},
 'lasance-dedication-anniversary-collect': {'english': 'O God, Who year by year dost renew the day '
                                                       'of the consecration of this Thy holy '
                                                       'temple, and dost ever bring us again in '
                                                       'safety to the holy mysteries, hear the '
                                                       'prayers of Thy people, and grant that '
                                                       'whosoever entereth this temple to seek '
                                                       'blessings may rejoice to obtain all that '
                                                       'he seeketh. Through our Lord.',
                                            'english_sha256': 'aa9242c2be1ad34bf16b540a92e3f7dc70af16eb0a84d9a27e3f7e35ce0a9285',
                                            'historical_latin': 'Deus, qui nobis per singulos '
                                                                'annos hujus sancti templi tui '
                                                                'consecrationis reparas diem, et '
                                                                'sacris semper mysteriis '
                                                                'repraesentas incolumes: exaudi '
                                                                'preces populi tui, et praesta; '
                                                                'ut, quisquis hoc templum '
                                                                'beneficia petiturus ingreditur, '
                                                                'cuncta se impetrasse laetetur. '
                                                                'Per Dominum.',
                                            'pdf_pages': [1408],
                                            'printed_pages': ['1389']},
 'lasance-four-crowned-martyrs-collect': {'english': 'Grant, we beseech Thee, O almighty God, that '
                                                     'we, who have known the fortitude of the '
                                                     'glorious martyrs in bearing witness to Thee, '
                                                     'may experience the fruit of their '
                                                     'intercession with Thee. Through our Lord.',
                                          'english_sha256': '3e4bcd7d513b1df18f541202c3c081b3a5c0695591c6db86af9a21418f5d7423',
                                          'historical_latin': 'Praesta, quaesumus, omnipotens '
                                                              'Deus: ut, qui gloriosos Martyres '
                                                              'fortes in sua confessione '
                                                              'cognovimus, pios apud te in nostra '
                                                              'intercessione sentiamus. Per '
                                                              'Dominum.',
                                          'pdf_pages': [1282],
                                          'printed_pages': ['1281']},
 'lasance-lent-3-friday-postcommunion': {'english': 'May the receiving of this sacrament, O Lord, '
                                                    'purify us from sin and bring us to the '
                                                    'heavenly realms. Through our Lord.',
                                         'english_sha256': 'bb348d1ddceb95b39e7947f3fd2ac3cdb6f2586be942a88a856ed0b87bd3fed3',
                                         'historical_latin': 'Hujus nos, Domine, perceptio '
                                                             'sacramenti mundet a crimine: et ad '
                                                             'caelestia regna perducat. Per '
                                                             'Dominum.',
                                         'pdf_pages': [319],
                                         'printed_pages': ['319']},
 'lasance-lent-4-monday-postcommunion': {'english': 'Having received the sacrament of salvation, O '
                                                    'Lord, may we be profited unto the increase of '
                                                    'our everlasting redemption. Through our Lord.',
                                         'english_sha256': '9b2a56cbb68808d3aaea2fccd5fdc00cf8ce41afaabda30c58507e3a87ed7673',
                                         'historical_latin': 'Sumptis, Domine, salutaribus '
                                                             'sacramentis: ad redemptionis '
                                                             'aeternae, quaesumus, proficiamus '
                                                             'augmentum. Per Dominum.',
                                         'pdf_pages': [334],
                                         'printed_pages': ['334']},
 'lasance-lent-4-monday-secret': {'english': 'May the sacrifice offered to Thee, O Lord, ever '
                                             'vivify and fortify us. Through our Lord.',
                                  'english_sha256': 'e216765f17f50eb1b24216d10261e72e34f6e288f54af9409ed5187decdbf324',
                                  'historical_latin': 'Oblatum tibi, Domine sacrificium vivificet '
                                                      'nos semper, et muniat. Per Dominum.',
                                  'pdf_pages': [334],
                                  'printed_pages': ['334']},
 'lasance-paschal-martyr-bishop-postcommunion-haec': {'english': 'May this communion, O Lord, '
                                                                 'cleanse us from guilt, and by '
                                                                 'the intercession of blessed N., '
                                                                 'Thy martyr and bishop, unite us '
                                                                 'in Him who is the heavenly '
                                                                 'medicine of our souls. Through '
                                                                 'our Lord.',
                                                      'english_sha256': '89356d579beb01476efca8eec107685799c9ec6ea15de16fc287a7480c82298a',
                                                      'historical_latin': 'Haec nos communio '
                                                                          'Domine purget a '
                                                                          'crimine: et '
                                                                          'intercedente beato N. '
                                                                          'Martyre tuo atque '
                                                                          'Pontifice, caelestis '
                                                                          'remedii faciat esse '
                                                                          'consortes. Per Dominum.',
                                                      'pdf_pages': [1351],
                                                      'printed_pages': ['1332']},
 'lasance-paschal-martyr-bishop-secret-munera': {'english': 'Sanctify O Lord the gifts we offer to '
                                                            'Thee, and, blessed N., Thy martyr and '
                                                            'bishop, interceding for us, appeased '
                                                            'thereby, graciously look down on us. '
                                                            'Through our Lord.',
                                                 'english_sha256': 'b8b23837e85e459525629b859f72ebf95c5312fd3913be5f0c524d6fca35107a',
                                                 'historical_latin': 'Munera tibi Domine dicata '
                                                                     'sanctifica: et, intercedente '
                                                                     'beato N. Martyre tuo atque '
                                                                     'Pontifice, per eadem nos '
                                                                     'placatus intende. Per '
                                                                     'Dominum.',
                                                 'pdf_pages': [1350],
                                                 'printed_pages': ['1331']},
 'lasance-pentecost-4-postcommunion': {'english': 'May the mysteries we have received purify us, '
                                                  'we beseech Thee, O Lord, and by their virtue '
                                                  'protect us. Through our Lord.',
                                       'english_sha256': '670de5e23d63442a7f56336ed09c787a931979b6d468c1042fb41dfc3f31da16',
                                       'historical_latin': 'Mysteria nos, Domine, quaesumus, '
                                                           'sumpta purificent: et suo munere '
                                                           'tueantur. Per Dominum.',
                                       'pdf_pages': [653],
                                       'printed_pages': ['655']},
 'lasance-pentecost-4-secret': {'english': 'Receiving our oblations, be appeased, we pray Thee, O '
                                           'Lord, and in Thy kindness constrain our wills toward '
                                           'Thee, even when resisting. Through our Lord.',
                                'english_sha256': '4bc9d0bd1edbd4ef35227d7f31f6c94e787f9aee88a3610e04a9853a31213b32',
                                'historical_latin': 'Oblationibus nostris, quaesumus, Domine, '
                                                    'placare susceptis: et ad te nostras etiam '
                                                    'rebelles compelle propitius voluntates. Per '
                                                    'Dominum.',
                                'pdf_pages': [653],
                                'printed_pages': ['655']},
 'lasance-pentecost-ember-saturday-postcommunion': {'english': 'May Thy holy things, O Lord, fill '
                                                               'us with divine fervor, so that we '
                                                               'may have pleasure alike in their '
                                                               'performance and in their effect. '
                                                               'Through our Lord.',
                                                    'english_sha256': '305d759e1c663f5ba789e99790f6f02b7cb6473f57ee001d8e91a87d6b67d37d',
                                                    'historical_latin': 'Praebeant nobis, Domine, '
                                                                        'divinum tua sancta '
                                                                        'fervorem: quo eorum '
                                                                        'pariter et actu '
                                                                        'delectemur, et fructu. '
                                                                        'Per Dominum.',
                                                    'pdf_pages': [623],
                                                    'printed_pages': ['625']},
 'lasance-pentecost-ember-saturday-secret': {'english': 'That our fasts may be accepted by Thee, O '
                                                        'Lord, grant us, we beseech Thee, by the '
                                                        'grace of this sacrament, to offer Thee a '
                                                        'clean heart. Through our Lord.',
                                             'english_sha256': 'e5c9413f029f2b9671559e8ff4c3148f97ec96a39b7b2a7cde43acf089cf0048',
                                             'historical_latin': 'Ut accepta tibi sint, Domine, '
                                                                 'nostra jejunia: praesta nobis '
                                                                 'quaesumus, hujus munere '
                                                                 'sacramenti purificatum tibi '
                                                                 'pectus offerre. Per Dominum.',
                                             'pdf_pages': [622, 623],
                                             'printed_pages': ['624', '625']},
 'lasance-september-ember-saturday-collect': {'english': 'Almighty, eternal God, Who dost heal '
                                                         'bodies and souls through wholesome '
                                                         'continence, we supplicate Thy majesty '
                                                         'that, being appeased by the devout '
                                                         'prayer of those who fast, Thou wouldst '
                                                         'grant us help both for the present and '
                                                         'for the future. Through our Lord.',
                                              'english_sha256': '40ff59774f754a2885148a0809124edbdc94129007b698839bfacd22f1a1b36c',
                                              'historical_latin': 'Omnipotens sempiterne Deus, qui '
                                                                  'per continentiam salutarem '
                                                                  'corporibus mederis et mentibus: '
                                                                  'majestatem tuam supplices '
                                                                  'exoramus; ut pia jejunantium '
                                                                  'deprecatione placatus, et '
                                                                  'praesentia nobis subsidia '
                                                                  'tribuas, et futura. Per '
                                                                  'Dominum.',
                                              'pdf_pages': [707],
                                              'printed_pages': ['709']},
 'lasance-st-bibiana-collect': {'english': 'O God, the giver of all good gifts, Who in Thy '
                                           'handmaid Bibiana didst join the palm of martyrdom to '
                                           'the flower of virginity, by her intercession, unite '
                                           'our hearts in charity to Thee, that our perils may be '
                                           'removed, and we may obtain the rewards of eternity. '
                                           'Through our Lord.',
                                'english_sha256': '28bb5a8686d0f4177e9b4798a355c317efc823b3ff53fd67d311b0c487f6f930',
                                'historical_latin': 'Deus, omnium largitor bonorum, qui in famula '
                                                    'tua Bibiana cum virginitatis flore martyrii '
                                                    'palmam conjunxisti: mentes nostras ejus '
                                                    'intercessione tibi caritate conjunge; ut, '
                                                    'amotis periculis, praemia consequamur '
                                                    'aeterna. Per Dominum.',
                                'pdf_pages': [837],
                                'printed_pages': ['838']},
 'lasance-st-francis-postcommunion': {'english': 'May heavenly grace, we beseech Thee, O Lord, '
                                                 'enlarge Thy Church which Thou wast pleased to '
                                                 'enlighten by the glorious merits and examples of '
                                                 'blessed Francis, Thy confessor. Through our '
                                                 'Lord.',
                                      'english_sha256': '9a264123c62cfa8aeb8cff938ee8b04377deda80acf74a7b12bafaa7f558803a',
                                      'historical_latin': 'Ecclesiam tuam, quaesumus, Domine, '
                                                          'gratia caelestis amplificet: quam beati '
                                                          'Francisci Confessoris tui illuminare '
                                                          'voluisti gloriosis meritis, et '
                                                          'exemplis. Per Dominum.',
                                      'pdf_pages': [1219],
                                      'printed_pages': ['1224']},
 'lasance-st-francis-secret': {'english': 'Sanctify, O Lord, the gifts dedicated to Thee, and, by '
                                          'the intercession of blessed Francis, cleanse us from '
                                          'all stain of sin. Through our Lord.',
                               'english_sha256': '11407d2f65144547c65ed756f04c8eb8224839925d6fe5b876f0fe48bab18e11',
                               'historical_latin': 'Munera tibi Domine dicata sanctifica: et, '
                                                   'intercedente beato Francisco, ab omni nos '
                                                   'culparum labe purifica. Per Dominum.',
                               'pdf_pages': [1219],
                               'printed_pages': ['1224']},
 'lasance-supplementary-mass-3-secret': {'english': 'We offer Thee, O Lord, the sacrifice of '
                                                    'reconciliation, that Thou mayest mercifully '
                                                    'forgive our sins and direct our wavering '
                                                    'hearts. Through our Lord.',
                                         'english_sha256': '58a54e6f4a19eb464e42bcfc1469782bf9437dd1483583d2b5e2922e99835f38',
                                         'historical_latin': 'Hostias tibi Domine placationis '
                                                             'offerimus: ut et delicta nostra '
                                                             'miseratus absolvas, et nutantia '
                                                             'corda tu dirigas. Per Dominum.',
                                         'pdf_pages': [744],
                                         'printed_pages': ['746']}}

SEED_ORACLES = {('comm-impressionis-sacrorum-stigmatum-s-francisci', 'main', 'Secret', 'all', 1): {'latin': 'Munera '
                                                                                             'tibi, '
                                                                                             'Domine, '
                                                                                             'dicata '
                                                                                             'sanctifica: '
                                                                                             'et, '
                                                                                             'intercedente '
                                                                                             'beato '
                                                                                             'Francisco, '
                                                                                             'ab\n'
                                                                                             'omni '
                                                                                             'nos '
                                                                                             'culparum '
                                                                                             'labe '
                                                                                             'purifica. '
                                                                                             'Per '
                                                                                             'Dominum.\n',
                                                                                    'locus': 'printed '
                                                                                             'p. '
                                                                                             '661, '
                                                                                             'no. '
                                                                                             '3652; '
                                                                                             'artifact '
                                                                                             'PDF '
                                                                                             'p. '
                                                                                             '742',
                                                                                    'page': 742,
                                                                                    'sha256': 'cbe6cca40c3d4b2aeac8d4996792381bbae3db33a2a73a31e55cf51882d3b553'},
 ('commune-abbatum', 'main', 'Postcommunion', 'all', 1): {'latin': 'Protegat nos, Domine, cum tui '
                                                                   'perceptione sacramenti beatus '
                                                                   'N. Abbas, pro\n'
                                                                   'nobis intercedendo: ut et '
                                                                   'conversationis ejus experiamur '
                                                                   'insignia, et\n'
                                                                   'intercessionis percipiamus '
                                                                   'suffragia. Per Dominum.\n',
                                                          'locus': 'printed p. [28], no. 4380; '
                                                                   'artifact PDF p. 836',
                                                          'page': 836,
                                                          'sha256': '533a5981694534bf71428bda70c589c7a6f82e33c16283a8180108ea493a6832'},
 ('commune-confessoris-pontificis-1', 'main', 'Postcommunion', 'all', 1): {'latin': 'Praesta, '
                                                                                    'quaesumus, '
                                                                                    'omnipotens '
                                                                                    'Deus: ut, de '
                                                                                    'perceptis '
                                                                                    'muneribus '
                                                                                    'gratias\n'
                                                                                    'exhibentes, '
                                                                                    'intercedente '
                                                                                    'beato N. '
                                                                                    'Confessore '
                                                                                    'tuo atque '
                                                                                    'Pontifice, '
                                                                                    'beneficia\n'
                                                                                    'potiora '
                                                                                    'sumamus. Per '
                                                                                    'Dominum.\n',
                                                                           'locus': 'printed p. '
                                                                                    '[20], no. '
                                                                                    '4317; '
                                                                                    'artifact PDF '
                                                                                    'p. 828',
                                                                           'page': 828,
                                                                           'sha256': '98c77901b712e4eebedc4a21f6ba8ef40596928452a69165eb49e5cea1a67376'},
 ('commune-dedicationis-ecclesiae', 'main', 'Collect', 'all', 1): {'latin': 'Deus, qui nobis per '
                                                                            'singulos annos hujus '
                                                                            'sancti templi tui '
                                                                            'consecrationis\n'
                                                                            'reparas diem, et '
                                                                            'sacris semper '
                                                                            'mysteriis '
                                                                            'repraesentas '
                                                                            'incolumes: exaudi\n'
                                                                            'preces populi tui, et '
                                                                            'praesta; ut, quisquis '
                                                                            'hoc templum beneficia '
                                                                            'petiturus\n'
                                                                            'ingreditur, cuncta se '
                                                                            'impetrasse laetetur. '
                                                                            'Per Dominum.\n',
                                                                   'locus': 'printed p. [39], no. '
                                                                            '4461; artifact PDF p. '
                                                                            '847',
                                                                   'page': 847,
                                                                   'sha256': 'db0081ffeb2c7c4b5d33c7263cbb5e1c95388cf9cc188c353724494e36ec9edd'},
 ('commune-unius-martyris-2', 'main', 'Postcommunion', 'all', 1): {'latin': 'Haec nos communio, '
                                                                            'Domine, purget a '
                                                                            'crimine: et, '
                                                                            'intercedente beato '
                                                                            'N.\n'
                                                                            'Martyre tuo atque '
                                                                            'Pontifice, caelestis '
                                                                            'remedii faciat esse '
                                                                            'consortes. Per\n'
                                                                            'Dominum.\n',
                                                                   'locus': 'printed p. [6], no. '
                                                                            '4214; artifact PDF p. '
                                                                            '814',
                                                                   'page': 814,
                                                                   'sha256': '0b346f95768addcc33e840c07cfb106afea5adaf93ee63e83513aa1178d2ca81'},
 ('commune-unius-martyris-2', 'main', 'Secret', 'all', 1): {'latin': 'Munera tibi, Domine, dicata '
                                                                     'sanctifica: et, intercedente '
                                                                     'beato N. Martyre\n'
                                                                     'tuo atque Pontifice, per '
                                                                     'eadem nos placatus intende. '
                                                                     'Per Dominum.\n',
                                                            'locus': 'printed p. [6], no. 4212; '
                                                                     'artifact PDF p. 814',
                                                            'page': 814,
                                                            'sha256': '09b6d4a8b81a1c2462c959340788c1d976b6f2fa95b9ab4004322beadce49d7d'},
 ('commune-virginum-2', 'main', 'Postcommunion', 'all', 1): {'latin': 'Divini muneris largitate '
                                                                      'satiati, quaesumus, Domine '
                                                                      'Deus noster: ut,\n'
                                                                      'intercedente beata N. '
                                                                      'Virgine et Martyre tua, in '
                                                                      'ejus semper participatione\n'
                                                                      'vivamus. Per Dominum.\n',
                                                             'locus': 'printed p. [31], no. 4404; '
                                                                      'artifact PDF p. 839',
                                                             'page': 839,
                                                             'sha256': 'eec222bea24a088576931d21a301828d2607a20deb51b370a5b224200846dd49'},
 ('epiphany-5', 'main', 'Secret', 'all', 1): {'latin': 'Hostias tibi, Domine, placationis '
                                                       'offerimus: ut et delicta nostra miseratus\n'
                                                       'absolvas, et nutantia corda tu dirigas. '
                                                       'Per Dominum.\n',
                                              'locus': 'printed p. 48, no. 333; artifact PDF p. '
                                                       '129',
                                              'page': 129,
                                              'sha256': 'be852e2fdd2f135ab124972e0dbfa0f27ec6006111e3e8580080cf6ebb893139'},
 ('holy-monday', 'main', 'Postcommunion', 'all', 1): {'latin': 'Praebeant nobis, Domine, divinum '
                                                               'tua sancta fervorem: quo eorum '
                                                               'pariter et\n'
                                                               'actu delectemur et fructu. Per '
                                                               'Dominum.\n',
                                                      'locus': 'printed p. 142, no. 866; artifact '
                                                               'PDF p. 223',
                                                      'page': 223,
                                                      'sha256': 'b0adda8b9a0bee22b3f4d7138be7e34f205fb5c8e42cd95ff7e11620c0a78994'},
 ('lent-3-friday', 'main', 'Postcommunion', 'all', 1): {'latin': 'Hujus nos, Domine, perceptio '
                                                                 'sacramenti mundet a crimine: et '
                                                                 'ad caelestia\n'
                                                                 'regna perducat. Per Dominum.\n',
                                                        'locus': 'printed p. 101, no. 665; '
                                                                 'artifact PDF p. 182',
                                                        'page': 182,
                                                        'sha256': 'b88dcae8fdad1144a59b33b06287fab3744233b0be96d1d0b2b6f36fea2aa7d0'},
 ('lent-4-monday', 'main', 'Postcommunion', 'all', 1): {'latin': 'Sumptis, Domine, salutaribus '
                                                                 'sacramentis: ad redemptionis '
                                                                 'aeternae,\n'
                                                                 'quaesumus, proficiamus '
                                                                 'augmentum. Per Dominum.\n',
                                                        'locus': 'printed p. 107, no. 696; '
                                                                 'artifact PDF p. 188',
                                                        'page': 188,
                                                        'sha256': '979d3c0687f83f6435365060f0d26bff2e98d236ce0edea20600ccd86a331b3f'},
 ('lent-4-saturday', 'main', 'Secret', 'all', 1): {'latin': 'Oblationibus nostris, quaesumus, '
                                                            'Domine, placare susceptis: et ad te '
                                                            'nostras\n'
                                                            'etiam rebelles compelle propitius '
                                                            'voluntates. Per Dominum.\n',
                                                   'locus': 'printed p. 117, no. 749; artifact PDF '
                                                            'p. 198',
                                                   'page': 198,
                                                   'sha256': '583d847585b7cb8db4508c6f41faac5b67b4ad6e8682f7287757711f2336e744'},
 ('pentecost-4', 'main', 'Postcommunion', 'all', 1): {'latin': 'Mysteria nos, Domine, quaesumus, '
                                                               'sumpta purificent: et suo munere '
                                                               'tueantur.\n'
                                                               'Per Dominum.\n',
                                                      'locus': 'printed p. 383, no. 1481; artifact '
                                                               'PDF p. 464',
                                                      'page': 464,
                                                      'sha256': 'a6509cc09e7ab180bb6129d8fff280599984974443f6f7cd47fed9ac0ba72db2'},
 ('pentecost-ember-saturday', 'longer', 'Postcommunion', 'all', 1): {'latin': 'Praebeant nobis, '
                                                                              'Domine; divinum tua '
                                                                              'sancta fervorem: '
                                                                              'quo eorum pariter '
                                                                              'et actu\n'
                                                                              'delectemur et '
                                                                              'fructu. Per '
                                                                              'Dominum.\n',
                                                                     'locus': '1962 control '
                                                                              'printed p.370, '
                                                                              'no.1397; artifact '
                                                                              'PDF p.451.',
                                                                     'page': 451,
                                                                     'sha256': 'e42adb4760f296b180b6d8c35fc62a03bed1f362007ab995b1bfa21fda35f6c6'},
 ('pentecost-ember-saturday', 'longer', 'Secret', 'all', 1): {'latin': 'Ut accepta tibi sint, '
                                                                       'Domine, nostra jejunia: '
                                                                       'praesta nobis, quaesumus; '
                                                                       'hujus\n'
                                                                       'munere sacramenti '
                                                                       'purificatum tibi pectus '
                                                                       'offerre. Per Dominum.\n',
                                                              'locus': '1962 control printed '
                                                                       'p.370, no.1395; artifact '
                                                                       'PDF p.451.',
                                                              'page': 451,
                                                              'sha256': '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b'},
 ('pentecost-ember-saturday', 'shorter', 'Postcommunion', 'all', 1): {'latin': 'Praebeant nobis, '
                                                                               'Domine, divinum '
                                                                               'tua sancta '
                                                                               'fervorem: quo '
                                                                               'eorum pariter et '
                                                                               'actu\n'
                                                                               'delectemur et '
                                                                               'fructu. Per '
                                                                               'Dominum.\n',
                                                                      'locus': '1962 control '
                                                                               'printed p.371, '
                                                                               'no.1410; artifact '
                                                                               'PDF p.452.',
                                                                      'page': 452,
                                                                      'sha256': '9d66ea9b051dea3c388b3569261c7fef87992f7ccb2f212e608204f3a708d0eb'},
 ('s-bibianae-virginis-martyris', 'main', 'Collect', 'all', 1): {'latin': 'Deus, omnium largitor '
                                                                          'bonorum, qui in famula '
                                                                          'tua Bibiana cum\n'
                                                                          'virginitatis flore '
                                                                          'martyrii palmam '
                                                                          'conjunxisti: mentes '
                                                                          'nostras ejus\n'
                                                                          'intercessione tibi '
                                                                          'caritate conjunge; ut, '
                                                                          'amotis periculis, '
                                                                          'praemia\n'
                                                                          'consequamur aeterna. '
                                                                          'Per Dominum.\n',
                                                                 'locus': '1962 printed p. 430, '
                                                                          'no. 1823, column R, '
                                                                          'marked P; artifact PDF '
                                                                          'p. 511',
                                                                 'page': 511,
                                                                 'sha256': '8c4d3b74e94461a000887dc8640554092cda67bdaa8a4c273eb9c3bd155c2fcb'},
 ('s-francisci-confessoris', 'main', 'Postcommunion', 'all', 1): {'latin': 'Ecclesiam tuam, '
                                                                           'quaesumus, Domine, '
                                                                           'gratia caelestis '
                                                                           'amplificet: quam '
                                                                           'beati\n'
                                                                           'Francisci Confessoris '
                                                                           'tui illuminare '
                                                                           'voluisti gloriosis '
                                                                           'meritis et exemplis.\n'
                                                                           'Per Dominum.\n',
                                                                  'locus': 'printed p. 676, no. '
                                                                           '3779; artifact PDF p. '
                                                                           '757',
                                                                  'page': 757,
                                                                  'sha256': '2f7bdfdfd597e51a2cdb7dc3ea3ff360fb9686d9549a99124bf388cc776ac3f2'},
 ('september-ember-saturday', 'longer', 'Collect', 'all', 1): {'latin': 'Omnipotens sempiterne '
                                                                        'Deus, qui per '
                                                                        'continentiam salutarem '
                                                                        'corporibus mederis et\n'
                                                                        'mentibus: majestatem tuam '
                                                                        'supplices exoramus; ut, '
                                                                        'pia jejunantium '
                                                                        'deprecatione\n'
                                                                        'placatus, et praesentia '
                                                                        'nobis subsidia tribuas, '
                                                                        'et futura. Per Dominum.\n',
                                                               'locus': '1962 control printed '
                                                                        'p.404, no.1634; artifact '
                                                                        'PDF p.485.',
                                                               'page': 485,
                                                               'sha256': '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018'},
 ('sexagesima', 'main', 'Secret', 'all', 1): {'latin': 'Oblatum tibi, Domine, sacrificium '
                                                       'vivificet nos semper et muniat. Per\n'
                                                       'Dominum.\n',
                                              'locus': 'printed p. 53, no. 363; artifact PDF p. '
                                                       '134',
                                              'page': 134,
                                              'sha256': 'f2cfab0a02e6ce66d7db73079ca0e6c87b653d60c1bc5e7eed17aa1d11169b8d'},
 ('ss-quadraginta-martyrum', 'main', 'Collect', 'all', 1): {'latin': 'Praesta quaesumus, '
                                                                     'omnipotens Deus: ut, qui '
                                                                     'gloriosos Martyres fortes in '
                                                                     'sua\n'
                                                                     'confessione cognovimus, pios '
                                                                     'apud te in nostra '
                                                                     'intercessione sentiamus. '
                                                                     'Per\n'
                                                                     'Dominum.\n',
                                                            'locus': 'printed p. 487, no. 2271; '
                                                                     'artifact PDF p. 568',
                                                            'page': 568,
                                                            'sha256': '7e769e83e0a50801b9d284606d16c120ab2f8145ab80021288e978ece133037a'},
 ('ss-septem-fratrum-martyrum-ac-ss', 'main', 'Collect', 'all', 1): {'latin': 'Praesta, quaesumus, '
                                                                              'omnipotens Deus: '
                                                                              'ut, qui gloriosos '
                                                                              'Martyres fortes in\n'
                                                                              'sua confessione '
                                                                              'cognovimus, pios '
                                                                              'apud te in nostra '
                                                                              'intercessione '
                                                                              'sentiamus.\n'
                                                                              'Per Dominum.\n',
                                                                     'locus': 'printed p. 582, no. '
                                                                              '3012; artifact PDF '
                                                                              'p. 663',
                                                                     'page': 663,
                                                                     'sha256': '1944cc089a542dd99119c5346d10c3fd57963061446c9d9e50667b57ea03c849'}}

TARGET_ORACLES = {('comm-impressionis-sacrorum-stigmatum-s-francisci', 'main', 'Secret', 'all', 1): ('lasance-st-francis-secret',
                                                                                    ('comm-impressionis-sacrorum-stigmatum-s-francisci',
                                                                                     'main',
                                                                                     'Secret',
                                                                                     'all',
                                                                                     1),
                                                                                    'cbe6cca40c3d4b2aeac8d4996792381bbae3db33a2a73a31e55cf51882d3b553'),
 ('comm-ss-quatuor-coronatorum-martyrum', 'main', 'Collect', 'all', 1): ('lasance-four-crowned-martyrs-collect',
                                                                         ('ss-septem-fratrum-martyrum-ac-ss',
                                                                          'main',
                                                                          'Collect',
                                                                          'all',
                                                                          1),
                                                                         '1944cc089a542dd99119c5346d10c3fd57963061446c9d9e50667b57ea03c849'),
 ('commune-abbatum', 'main', 'Postcommunion', 'all', 1): ('lasance-common-abbot-postcommunion',
                                                          ('commune-abbatum',
                                                           'main',
                                                           'Postcommunion',
                                                           'all',
                                                           1),
                                                          '533a5981694534bf71428bda70c589c7a6f82e33c16283a8180108ea493a6832'),
 ('commune-confessoris-pontificis-1', 'main', 'Postcommunion', 'all', 1): ('lasance-common-confessor-bishop-1-postcommunion',
                                                                           ('commune-confessoris-pontificis-1',
                                                                            'main',
                                                                            'Postcommunion',
                                                                            'all',
                                                                            1),
                                                                           '98c77901b712e4eebedc4a21f6ba8ef40596928452a69165eb49e5cea1a67376'),
 ('commune-dedicationis-ecclesiae', 'main', 'Collect', 'all', 1): ('lasance-dedication-anniversary-collect',
                                                                   ('commune-dedicationis-ecclesiae',
                                                                    'main',
                                                                    'Collect',
                                                                    'all',
                                                                    1),
                                                                   'db0081ffeb2c7c4b5d33c7263cbb5e1c95388cf9cc188c353724494e36ec9edd'),
 ('commune-unius-martyris-2', 'main', 'Postcommunion', 'all', 1): ('lasance-paschal-martyr-bishop-postcommunion-haec',
                                                                   ('commune-unius-martyris-2',
                                                                    'main',
                                                                    'Postcommunion',
                                                                    'all',
                                                                    1),
                                                                   '0b346f95768addcc33e840c07cfb106afea5adaf93ee63e83513aa1178d2ca81'),
 ('commune-unius-martyris-2', 'main', 'Secret', 'all', 1): ('lasance-paschal-martyr-bishop-secret-munera',
                                                            ('commune-unius-martyris-2',
                                                             'main',
                                                             'Secret',
                                                             'all',
                                                             1),
                                                            '09b6d4a8b81a1c2462c959340788c1d976b6f2fa95b9ab4004322beadce49d7d'),
 ('commune-virginum-2', 'main', 'Postcommunion', 'all', 1): ('lasance-common-virgin-2-postcommunion',
                                                             ('commune-virginum-2',
                                                              'main',
                                                              'Postcommunion',
                                                              'all',
                                                              1),
                                                             'eec222bea24a088576931d21a301828d2607a20deb51b370a5b224200846dd49'),
 ('epiphany-5', 'main', 'Secret', 'all', 1): ('lasance-supplementary-mass-3-secret',
                                              ('epiphany-5', 'main', 'Secret', 'all', 1),
                                              'be852e2fdd2f135ab124972e0dbfa0f27ec6006111e3e8580080cf6ebb893139'),
 ('holy-monday', 'main', 'Postcommunion', 'all', 1): ('lasance-pentecost-ember-saturday-postcommunion',
                                                      ('holy-monday',
                                                       'main',
                                                       'Postcommunion',
                                                       'all',
                                                       1),
                                                      'b0adda8b9a0bee22b3f4d7138be7e34f205fb5c8e42cd95ff7e11620c0a78994'),
 ('lent-1-ember-wednesday', 'main', 'Secret', 'all', 1): ('lasance-supplementary-mass-3-secret',
                                                          ('epiphany-5',
                                                           'main',
                                                           'Secret',
                                                           'all',
                                                           1),
                                                          'be852e2fdd2f135ab124972e0dbfa0f27ec6006111e3e8580080cf6ebb893139'),
 ('lent-3-friday', 'main', 'Postcommunion', 'all', 1): ('lasance-lent-3-friday-postcommunion',
                                                        ('lent-3-friday',
                                                         'main',
                                                         'Postcommunion',
                                                         'all',
                                                         1),
                                                        'b88dcae8fdad1144a59b33b06287fab3744233b0be96d1d0b2b6f36fea2aa7d0'),
 ('lent-4-monday', 'main', 'Postcommunion', 'all', 1): ('lasance-lent-4-monday-postcommunion',
                                                        ('lent-4-monday',
                                                         'main',
                                                         'Postcommunion',
                                                         'all',
                                                         1),
                                                        '979d3c0687f83f6435365060f0d26bff2e98d236ce0edea20600ccd86a331b3f'),
 ('lent-4-monday', 'main', 'Secret', 'all', 1): ('lasance-lent-4-monday-secret',
                                                 ('sexagesima', 'main', 'Secret', 'all', 1),
                                                 'f2cfab0a02e6ce66d7db73079ca0e6c87b653d60c1bc5e7eed17aa1d11169b8d'),
 ('lent-4-saturday', 'main', 'Secret', 'all', 1): ('lasance-pentecost-4-secret',
                                                   ('lent-4-saturday', 'main', 'Secret', 'all', 1),
                                                   '583d847585b7cb8db4508c6f41faac5b67b4ad6e8682f7287757711f2336e744'),
 ('lent-4-tuesday', 'main', 'Postcommunion', 'all', 1): ('lasance-lent-3-friday-postcommunion',
                                                         ('lent-3-friday',
                                                          'main',
                                                          'Postcommunion',
                                                          'all',
                                                          1),
                                                         'b88dcae8fdad1144a59b33b06287fab3744233b0be96d1d0b2b6f36fea2aa7d0'),
 ('pentecost-4', 'main', 'Postcommunion', 'all', 1): ('lasance-pentecost-4-postcommunion',
                                                      ('pentecost-4',
                                                       'main',
                                                       'Postcommunion',
                                                       'all',
                                                       1),
                                                      'a6509cc09e7ab180bb6129d8fff280599984974443f6f7cd47fed9ac0ba72db2'),
 ('pentecost-4', 'main', 'Secret', 'all', 1): ('lasance-pentecost-4-secret',
                                               ('lent-4-saturday', 'main', 'Secret', 'all', 1),
                                               '583d847585b7cb8db4508c6f41faac5b67b4ad6e8682f7287757711f2336e744'),
 ('pentecost-ember-saturday', 'longer', 'Postcommunion', 'all', 1): ('lasance-pentecost-ember-saturday-postcommunion',
                                                                     ('pentecost-ember-saturday',
                                                                      'longer',
                                                                      'Postcommunion',
                                                                      'all',
                                                                      1),
                                                                     'e42adb4760f296b180b6d8c35fc62a03bed1f362007ab995b1bfa21fda35f6c6'),
 ('pentecost-ember-saturday', 'longer', 'Secret', 'all', 1): ('lasance-pentecost-ember-saturday-secret',
                                                              ('pentecost-ember-saturday',
                                                               'longer',
                                                               'Secret',
                                                               'all',
                                                               1),
                                                              '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b'),
 ('pentecost-ember-saturday', 'shorter', 'Postcommunion', 'all', 1): ('lasance-pentecost-ember-saturday-postcommunion',
                                                                      ('pentecost-ember-saturday',
                                                                       'shorter',
                                                                       'Postcommunion',
                                                                       'all',
                                                                       1),
                                                                      '9d66ea9b051dea3c388b3569261c7fef87992f7ccb2f212e608204f3a708d0eb'),
 ('pentecost-ember-saturday', 'shorter', 'Secret', 'all', 1): ('lasance-pentecost-ember-saturday-secret',
                                                               ('pentecost-ember-saturday',
                                                                'longer',
                                                                'Secret',
                                                                'all',
                                                                1),
                                                               '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b'),
 ('s-bibianae-virginis-martyris', 'main', 'Collect', 'all', 1): ('lasance-st-bibiana-collect',
                                                                 ('s-bibianae-virginis-martyris',
                                                                  'main',
                                                                  'Collect',
                                                                  'all',
                                                                  1),
                                                                 '8c4d3b74e94461a000887dc8640554092cda67bdaa8a4c273eb9c3bd155c2fcb'),
 ('s-francisci-confessoris', 'main', 'Postcommunion', 'all', 1): ('lasance-st-francis-postcommunion',
                                                                  ('s-francisci-confessoris',
                                                                   'main',
                                                                   'Postcommunion',
                                                                   'all',
                                                                   1),
                                                                  '2f7bdfdfd597e51a2cdb7dc3ea3ff360fb9686d9549a99124bf388cc776ac3f2'),
 ('s-francisci-confessoris', 'main', 'Secret', 'all', 1): ('lasance-st-francis-secret',
                                                           ('comm-impressionis-sacrorum-stigmatum-s-francisci',
                                                            'main',
                                                            'Secret',
                                                            'all',
                                                            1),
                                                           'cbe6cca40c3d4b2aeac8d4996792381bbae3db33a2a73a31e55cf51882d3b553'),
 ('september-ember-saturday', 'longer', 'Collect', 'all', 1): ('lasance-september-ember-saturday-collect',
                                                               ('september-ember-saturday',
                                                                'longer',
                                                                'Collect',
                                                                'all',
                                                                1),
                                                               '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018'),
 ('september-ember-saturday', 'shorter', 'Collect', 'all', 1): ('lasance-september-ember-saturday-collect',
                                                                ('september-ember-saturday',
                                                                 'longer',
                                                                 'Collect',
                                                                 'all',
                                                                 1),
                                                                '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018'),
 ('sexagesima', 'main', 'Secret', 'all', 1): ('lasance-lent-4-monday-secret',
                                              ('sexagesima', 'main', 'Secret', 'all', 1),
                                              'f2cfab0a02e6ce66d7db73079ca0e6c87b653d60c1bc5e7eed17aa1d11169b8d'),
 ('ss-quadraginta-martyrum', 'main', 'Collect', 'all', 1): ('lasance-four-crowned-martyrs-collect',
                                                            ('ss-quadraginta-martyrum',
                                                             'main',
                                                             'Collect',
                                                             'all',
                                                             1),
                                                            '7e769e83e0a50801b9d284606d16c120ab2f8145ab80021288e978ece133037a'),
 ('ss-septem-fratrum-martyrum-ac-ss', 'main', 'Collect', 'all', 1): ('lasance-four-crowned-martyrs-collect',
                                                                     ('ss-septem-fratrum-martyrum-ac-ss',
                                                                      'main',
                                                                      'Collect',
                                                                      'all',
                                                                      1),
                                                                     '1944cc089a542dd99119c5346d10c3fd57963061446c9d9e50667b57ea03c849')}

OLD_KEYS = [('advent-1', 'main', 'Collect', 'all', 1),
 ('advent-1', 'main', 'Postcommunion', 'all', 1),
 ('advent-1', 'main', 'Secret', 'all', 1),
 ('advent-2', 'main', 'Postcommunion', 'all', 1),
 ('advent-2', 'main', 'Secret', 'all', 1),
 ('advent-3', 'main', 'Collect', 'all', 1),
 ('advent-3', 'main', 'Postcommunion', 'all', 1),
 ('advent-3', 'main', 'Secret', 'all', 1),
 ('advent-4', 'main', 'Collect', 'all', 1),
 ('advent-4', 'main', 'Postcommunion', 'all', 1),
 ('advent-4', 'main', 'Secret', 'all', 1),
 ('advent-ember-friday', 'main', 'Secret', 'all', 1),
 ('comm-beatae-mariae-virginis-a-mercede', 'main', 'Collect', 'all', 1),
 ('comm-s-alexii-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-bonifatii-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Collect', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-gorgonii-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-gorgonii-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-hermetis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-hermetis-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Collect', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Secret', 'all', 1),
 ('comm-s-petri-apostoli', 'main', 'Collect', 'all', 1),
 ('comm-s-petri-apostoli', 'main', 'Secret', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Collect', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Secret', 'all', 1),
 ('comm-s-praxedis-virginis', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-praxedis-virginis', 'main', 'Secret', 'all', 1),
 ('comm-s-romani-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-romani-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-saturnini-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-saturnini-martyris', 'main', 'Secret', 'all', 1),
 ('comm-septem-dolorum-beatae-mariae-virginis', 'main', 'Sequence', 'all', 1),
 ('comm-ss-alexandri-eventii-theoduli-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-alexandri-eventii-theoduli-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-cypriani-iustinae-virginis-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-hippolyti-cassiani-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-hippolyti-cassiani-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-placidi-sociorum-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-proti-hyacinthi-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-proti-hyacinthi-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-symphorosae-septem-eius-filiorum', 'main', 'Secret', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Collect', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Postcommunion', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Secret', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Sequence', 'all', 1),
 ('commune-confessoris-non-pontificis-1', 'main', 'Postcommunion', 'all', 1),
 ('commune-confessoris-non-pontificis-1', 'main', 'Secret', 'all', 1),
 ('commune-confessoris-pontificis-1', 'main', 'Secret', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Collect (In ipso die Dedicationis)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Postcommunion (In ipso die Dedicationis)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Secret (Extra ecclesiam ipsam dedicatam)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Secret (In ipso die Dedicationis)', 'all', 1),
 ('commune-doctorum-non-pontificis', 'main', 'Secret', 'all', 1),
 ('commune-doctorum-pontificis', 'main', 'Postcommunion', 'all', 1),
 ('commune-doctorum-pontificis', 'main', 'Secret', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Alleluia', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Gradual', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Postcommunion', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Secret', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Tract', 'all', 1),
 ('commune-martyrum-tempore-paschali-1', 'main', 'Postcommunion (Pro Martyre tantum)', 'all', 1),
 ('commune-plurimorum-martyrum-1', 'main', 'Postcommunion', 'all', 1),
 ('commune-plurimorum-martyrum-2', 'main', 'Secret', 'all', 1),
 ('commune-summorum-pontificum', 'main', 'Collect', 'all', 1),
 ('commune-unius-martyris-3', 'main', 'Secret', 'all', 1),
 ('commune-virginum-3', 'main', 'Postcommunion', 'all', 1),
 ('commune-virginum-3', 'main', 'Secret', 'all', 1),
 ('commune-virginum-4', 'main', 'Alleluia', 'all', 1),
 ('corpus-christi', 'main', 'Sequence', 'all', 1),
 ('easter-5', 'main', 'Postcommunion', 'all', 1),
 ('easter-monday', 'main', 'Secret', 'all', 1),
 ('easter-sunday', 'main', 'Secret', 'all', 1),
 ('easter-sunday', 'main', 'Sequence', 'all', 1),
 ('easter-vigil', 'main', 'Blessing of the Baptismal Water', 'all', 1),
 ('easter-vigil', 'main', 'Blessing of the New Fire', 'all', 1),
 ('easter-vigil', 'main', 'Lumen Christi', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the First Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Fourth Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Second Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Third Prophecy', 'all', 1),
 ('good-friday', 'main', 'Showing of the Cross', 'all', 1),
 ('holy-family', 'main', 'Collect', 'all', 1),
 ('holy-family', 'main', 'Postcommunion', 'all', 1),
 ('holy-family', 'main', 'Secret', 'all', 1),
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Communion', 'all', 1),
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Offertory', 'all', 1),
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Alleluia', 'all', 1),
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Introit', 'all', 1),
 ('missa-de-s-maria-in-sabbato-4', 'main', 'Offertory', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Collect', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Postcommunion', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Secret', 'all', 1),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 1),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 2),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 3),
 ('palm-sunday', 'main', 'Responsory at the Entrance into the Church', 'all', 1),
 ('palm-sunday', 'main', 'Versicle at the Beginning of the Procession', 'all', 1),
 ('pentecost', 'main', 'Alleluia', 'all', 1),
 ('pentecost', 'main', 'Collect', 'all', 1),
 ('pentecost', 'main', 'Communion', 'all', 1),
 ('pentecost', 'main', 'Gospel', 'all', 1),
 ('pentecost', 'main', 'Introit', 'all', 1),
 ('pentecost', 'main', 'Offertory', 'all', 1),
 ('pentecost', 'main', 'Postcommunion', 'all', 1),
 ('pentecost', 'main', 'Secret', 'all', 1),
 ('pentecost', 'main', 'Sequence', 'all', 1),
 ('pentecost-13', 'main', 'Collect', 'all', 1),
 ('pentecost-13', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-13', 'main', 'Secret', 'all', 1),
 ('pentecost-14', 'main', 'Collect', 'all', 1),
 ('pentecost-14', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-14', 'main', 'Secret', 'all', 1),
 ('pentecost-15', 'main', 'Collect', 'all', 1),
 ('pentecost-15', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-15', 'main', 'Secret', 'all', 1),
 ('pentecost-19', 'main', 'Collect', 'all', 1),
 ('pentecost-19', 'main', 'Introit', 'all', 1),
 ('pentecost-19', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-19', 'main', 'Secret', 'all', 1),
 ('pentecost-thursday', 'main', 'Secret', 'all', 1),
 ('praesentatione-beatae-mariae-virginis', 'main', 'Postcommunion', 'all', 1),
 ('praesentatione-beatae-mariae-virginis', 'main', 'Secret', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-angelae-mericiae-virginis', 'main', 'Collect', 'all', 1),
 ('s-antonini-episcopi-confessoris', 'main', 'Secret', 'all', 1),
 ('s-augustini-episcopi-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-bedae-venerabilis-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-bernardini-senensis-confessoris', 'main', 'Secret', 'all', 1),
 ('s-birgittae-viduae', 'main', 'Secret', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-damasi-i-papae-confessoris', 'main', 'Collect', 'all', 1),
 ('s-ephraem-syri-diaconi-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-gregorii-i-papae-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-gregorii-i-papae-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-gregorii-thaumaturgi-episcopi-confessoris', 'main', 'Secret', 'all', 1),
 ('s-gregorii-vii-papae-confessoris', 'main', 'Collect', 'all', 1),
 ('s-hermenegildi-martyris', 'main', 'Postcommunion', 'all', 1),
 ('s-hermenegildi-martyris', 'main', 'Secret', 'all', 1),
 ('s-ioannis-a-deo-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-ioannis-baptistae-la-salle-confessoris', 'main', 'Secret', 'all', 1),
 ('s-ioannis-eudes-confessoris', 'main', 'Collect', 'all', 1),
 ('s-ioannis-matha-confessoris', 'main', 'Collect', 'all', 1),
 ('s-iosephi-cupertino-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-iosephi-cupertino-confessoris', 'main', 'Secret', 'all', 1),
 ('s-luciae-virginis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('s-luciae-virginis-martyris', 'main', 'Secret', 'all', 1),
 ('s-marthae-virginis', 'main', 'Secret', 'all', 1),
 ('s-monicae-viduae', 'main', 'Postcommunion', 'all', 1),
 ('s-monicae-viduae', 'main', 'Secret', 'all', 1),
 ('s-pauli-primi-eremitae-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-pauli-primi-eremitae-confessoris', 'main', 'Secret', 'all', 1),
 ('s-petri-canisii-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-petri-nolasci-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-petri-nolasci-confessoris', 'main', 'Secret', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Collect', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Postcommunion', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Secret', 'all', 1),
 ('sanctissimi-nominis-beatae-mariae-virginis', 'main', 'Postcommunion', 'all', 1),
 ('sanctissimi-nominis-beatae-mariae-virginis', 'main', 'Secret', 'all', 1),
 ('septem-dolorum-beatae-mariae-virginis', 'main', 'Sequence', 'all', 1),
 ('ss-perpetuae-felicitatis-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('ss-philippi-iacobi-apostolorum', 'main', 'Postcommunion', 'all', 1),
 ('ss-vincentii-anastasii-martyrum', 'main', 'Secret', 'all', 1),
 ('vigil-of-the-ascension', 'main', 'Postcommunion', 'all', 1)]

OLD_ENTRY_SHA = '02256f54b09c73c5a5901b4f3a45509639b7d1b4eda1cc2b9b08c317a0f4770b'

COVERAGE = {'roman-1962': (1427, 219, 1208), 'roman-pre-1955': (1378, 206, 1172)}

ARTIFACT_ORACLES = {'artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.phase4-nativity-marian-reuse-en-ed897177': ('ed89717779d0b40259dee17372a269085854d3747c9aab34252df73c0a148f88',
                                                                                                                     193,
                                                                                                                     'src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/artifacts/phase4-nativity-marian-reuse-en-ed897177/phase4-nativity-marian-reuse-en.tsv'),
 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.phase4-nineteen-prayers-en-0779811a': ('0779811a3d96a3ac4ba4427d6d11e3cfca6cb18a6c4071ccbcc70b0d1a6e6999',
                                                                                                                    6786,
                                                                                                                    'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase4-nineteen-prayers-en-0779811a/phase4-nineteen-prayers-en.tsv')}

DONOR = ('missa-de-s-maria-in-sabbato-2', 'main', 'Communion', 'all', 1)

REUSE_TARGET = ('nativitate-beatae-mariae-virginis', 'main', 'Communion', 'all', 1)

DONOR_ENTRY = {'artifact_id': 'artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.ia-scan-pdf',
 'collated': 'page-image and tracked transcription, 2026-08-26',
 'collation_result': 'confirmed',
 'cycle': 'all',
 'form_id': 'main',
 'ia_leaf': 517,
 'ia_leaf_range': [517, 517],
 'incipit': 'Beata viscera Mariae Virginis',
 'mass': 'missa-de-s-maria-in-sabbato-2',
 'occurrence': 1,
 'passage_id': 'passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.verify-missa-de-s-maria-in-sabbato-2-communion',
 'printed_page': '509',
 'proper': 'Communion',
 'publication_artifact_id': 'artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.common-marian-verified-en',
 'publication_artifact_sha256': '1c414c2fb24abd25f211841302a0b4ac95ff89d47a998afbefd2b9a323896851',
 'publication_passage_id': 'passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.publish-missa-de-s-maria-in-sabbato-2-communion',
 'translations': [{'lang': 'en',
                   'rights': 'public-domain',
                   'source_id': 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861',
                   'text': 'Blessed is the womb of Mary, the Virgin which bore the Son of the '
                           'eternal Father.'}],
 'witness': 'cummiskey-1861',
 'witness_note': 'The dated page-image verification passage and the separate tracked public-domain '
                 'passage bind this complete English body to the target formulary identity '
                 'established by the recorded Latin comparison above. The Cummiskey witness '
                 'remains a pre-1955 lay hand missal; this row makes no broader recension claim.'}


class English31SourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  loader=SourceFileLoader("english31_test_propers",str(ROOT/"tools/mass-propers"))
  spec=spec_from_loader(loader.name,loader);cls.p=module_from_spec(spec);sys.modules[spec.name]=cls.p;loader.exec_module(cls.p)
  cls.doc=cls.p.load_calendar(CAL,"roman-1962")
  cls.records,problems=cls.p._source_library_records(CAL)
  if problems:raise AssertionError(problems)
  cls.overlay,cls.absent,cls.stale,cls.witnesses=cls.p.translation_overlay("roman-1962",CAL)
  cls.entries={cls.p.translation_record_identity(r,cls.doc):r for r in tomllib.loads(LEDGER.read_text())["entries"]}
  cls.bodies={}
  for _,m in cls.p.masses_of(cls.doc):
   for form,proper,taken in cls.p.appointed_propers(cls.doc,m):
    owner=cls.p.source_slot_identity(cls.doc,m,form,proper,taken)
    for k,body in cls.p.coverage_slot_units(proper,owner):cls.bodies[k]=body

 def test_full_historical_english_and_nineteen_source_inspection_owners(self):
  self.assertEqual(len(SOURCE_ORACLES),19)
  for key,(source,seed,digest) in TARGET_ORACLES.items():
   row=self.entries[key];oracle=SOURCE_ORACLES[source]
   with self.subTest(key=key):
    self.assertEqual(row["translations"][0]["text"],oracle["english"])
    self.assertEqual(sha(row["translations"][0]["text"]),oracle["english_sha256"])
    self.assertEqual(row["passage_id"],"passage."+LP+".verify-phase4-en31-"+source)
    v=self.records[row["passage_id"]]
    self.assertIn("printed p. "+oracle["printed_pages"][0],v["context"])
    self.assertEqual(v["artifact_page_ranges"],[[oracle["pdf_pages"][0],oracle["pdf_pages"][-1]]])
    historical=v["notes"].split("Historical Latin transcription (layout reflowed): ",1)[1].split(" Source Latin ending: ",1)[0]
    self.assertEqual(historical,oracle["historical_latin"])
    self.assertEqual(words(historical),words(self.bodies[seed]["text"]))
    self.assertTrue(oracle["english"].endswith("Through our Lord."))
    self.assertEqual("N." in historical,"N." in oracle["english"])

 def test_all_twenty_two_seeds_are_independently_body_and_locus_checked(self):
  self.assertEqual(len(SEED_ORACLES),22)
  for seed,s in SEED_ORACLES.items():
   with self.subTest(seed=seed):
    self.assertEqual(self.bodies[seed]["text"],s["latin"])
    self.assertEqual(sha(s["latin"]),s["sha256"])
    record=self.records["passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-en31-seed-"+slug(seed)]
    self.assertEqual(record["locus"],s["locus"])
    self.assertIn(s["sha256"],record["notes"])
    self.assertEqual(record["artifact_sha256"],"648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a")

 def test_every_recipient_entire_literal_latin_and_actual_ending(self):
  latin=tomllib.loads((ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())["entries"]
  masses={m["key"]:m for _,m in self.p.masses_of(self.doc)}
  comparisons=dict(TARGET_ORACLES)
  comparisons[REUSE_TARGET]=("existing-cummiskey",DONOR,"7083e0d7d8b0fcfa0708cfb40cfab85450b47d45cd1eb029bc930197e49ec979")
  self.assertEqual(len(comparisons),31)
  for key,(source,seed,digest) in comparisons.items():
   with self.subTest(key=key):
    self.assertEqual(self.bodies[key]["text"],self.bodies[seed]["text"])
    self.assertEqual(sha(self.bodies[key]["text"]),digest)
    if key != REUSE_TARGET:
     self.assertTrue(self.bodies[key]["text"].endswith(("Per Dominum.\n","Per\nDominum.\n")))
    lp=[r for r in latin if r["mass"]==key[0] and r["proper"]==key[2] and r["occurrence"]==key[4]
        and self.p.form_id_for_label(masses[key[0]],r["form"])==key[1]]
    self.assertEqual(len(lp),1)
    self.assertEqual((lp[0]["text_sha256"],lp[0]["publication_status"],lp[0]["publication_basis"]),
                     (digest,"permitted","public-domain"))
    self.assertIn(digest,self.entries[key]["witness_note"])

 def test_artifact_exact_bytes_and_each_recipient_column(self):
  expected=set(TARGET_ORACLES)|{REUSE_TARGET};carried=set()
  for art,(digest,size,path) in ARTIFACT_ORACLES.items():
   payload=(ROOT/path).read_bytes();record=self.records[art]
   self.assertEqual((sha(payload),len(payload)),(digest,size))
   self.assertEqual((record["sha256"],record["byte_size"]),(digest,size))
   self.assertEqual((record["storage"],record["rights_status"],record["rights_jurisdiction"]),
                    ("tracked","public-domain","United States"))
   for line,r in enumerate(csv.DictReader(io.StringIO(payload.decode()),delimiter="\t"),2):
    key=(r["mass"],r["form_id"],r["proper"],r["cycle"],int(r["occurrence"]))
    self.assertNotIn(key,carried);carried.add(key)
    row=self.entries[key]
    self.assertEqual(json.loads(r["english_json"]),row["translations"][0]["text"])
    publication=self.records[row["publication_passage_id"]]
    self.assertEqual(publication["physical_line_ranges"],[[line,line]])
    self.assertEqual(publication["locus"],self.records[row["passage_id"]]["locus"])
    self.p.validate_translation_publication_binding(row,CAL,LEDGER,self.witnesses)
  self.assertEqual(carried,expected)

 def test_existing_cummiskey_donor_is_unchanged_not_reinspected(self):
  self.assertEqual(self.entries[DONOR],DONOR_ENTRY)
  target=self.entries[REUSE_TARGET]
  self.assertEqual(self.bodies[REUSE_TARGET]["text"],self.bodies[DONOR]["text"])
  for key in ("artifact_id","passage_id","collated","collation_result","ia_leaf","printed_page"):
   self.assertEqual(target[key],DONOR_ENTRY[key])
  self.assertEqual(target["translations"],DONOR_ENTRY["translations"])
  self.assertEqual(target.get("incipit",""),self.bodies[REUSE_TARGET].get("incipit",""))
  self.assertIn("This chant has no oration conclusion; none is added.",target["witness_note"])
  self.assertIn("zero new historical",target["witness_note"])

 def test_all_173_prior_rows_and_their_bindings_are_unchanged(self):
  old=[self.entries[k] for k in OLD_KEYS]
  self.assertEqual(len(old),173)
  self.assertEqual(sha(json.dumps(old,sort_keys=True,ensure_ascii=False)),OLD_ENTRY_SHA)

 def test_authorized_common_two_and_original_advent_hold(self):
  historical=source_batch.historical_english_entries(self.entries)
  for proper in ("Collect","Secret"):
   key=("commune-virginum-2","main",proper,"all",1)
   self.assertIn(key,self.overlay)
   self.assertEqual(self.entries[key]["publication_artifact_id"],'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.phase4-common-virgin-ii-two-prayers-en-11658a3a')
  key=("advent-2","main","Collect","all",1)
  self.assertNotIn(key,historical)
  if key in self.entries:
   self.assertEqual(self.overlay[key],self.entries[key])
  else:
   self.assertNotIn(key,self.overlay)

 def test_existing_rights_boundary_does_not_become_latin_authority(self):
  lasance=next(r for k,r in self.records.items() if k in ARTIFACT_ORACLES and r["edition_id"]=="edition."+LP)
  for phrase in ("A110108","A192159","1298a-1298n","1302a-1302d","No whole mixed-scan"):
   self.assertIn(phrase,lasance["rights_basis"])
  pdf=self.records["artifact."+LP+".internet-archive-facsimile-pdf-6cf3c3d0"]
  self.assertEqual((pdf["storage"],pdf["rights_status"]),("remote","unresolved"))
  self.assertIn("Existing Latin permission remains independent.",self.entries[next(iter(TARGET_ORACLES))]["witness_note"])

 def test_modified_english_and_artifact_hash_are_refused(self):
  row=copy.deepcopy(self.entries[next(iter(TARGET_ORACLES))])
  row["translations"][0]["text"]+=" Amen."
  with self.assertRaises(ValueError):
   self.p.validate_translation_publication_binding(row,CAL,LEDGER,self.witnesses)
  row=copy.deepcopy(self.entries[next(iter(TARGET_ORACLES))])
  row["publication_artifact_sha256"]="0"*64
  with self.assertRaises(ValueError):
   self.p.validate_translation_publication_binding(row,CAL,LEDGER,self.witnesses)

 def test_current_coverage_has_zero_accounting_errors(self):
  self.assertEqual(self.stale,[])
  for cal,expected in COVERAGE.items():
   historical=source_batch.historical_english_coverage(cal)
   self.assertEqual((historical["slots"],historical["with_english"],historical["ledgered_untranslated"]),expected)
   row=self.p.english_coverage(CAL,cal)
   source_batch.assert_current_english_coverage(row,cal)
   for field in ("unaccounted","outside_the_ledger","unmatched_records","stale_translation_records","rights_restricted"):
    self.assertEqual(row[field],0,(cal,field))

if __name__=="__main__":unittest.main()
