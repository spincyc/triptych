"""Exactly two separately authorized, fresh-verbatim CommonVirginII English owners."""
from pathlib import Path
import copy,csv,hashlib,io,json,tomllib,unittest
from tools.tests import test_roman_1962_english31_phase4 as prior
from tools.tests import _source_batch_guards as source_batch
ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/"src/sources/calendars"
LEDGER=ROOT/"src/sources/inventories/roman-1962-proper-translations-v1.toml"
LATIN=ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
def sha(v):return hashlib.sha256(v.encode() if isinstance(v,str) else v).hexdigest()
def digest(rows):return sha(json.dumps(rows,sort_keys=True,ensure_ascii=False))
ORACLES = {('commune-virginum-2', 'main', 'Collect', 'all', 1): {'english': 'May blessed N., virgin and martyr, who '
                                                                  'was ever pleasing to Thee by her merit of '
                                                                  'chastity and by her extolling of Thy '
                                                                  'power, implore Thy forgiveness for us, we '
                                                                  'beseech Thee, O Lord. Through our Lord.',
                                                       'english_with_lf_sha256': '206a2d6c3598c7e9cacd22506cc19e6833cd2def47eb721dee329b59ad354c51',
                                                       'historical_latin': 'Indulgentiam nobis quaesumus, '
                                                                           'Domine, beata N. Virgo et Martyr '
                                                                           'imploret: quae tibi grata semper '
                                                                           'exstitit, et merito castitatis, '
                                                                           'et tuae professione virtutis. '
                                                                           'Per Dominum.',
                                                       'latin': 'Indulgentiam nobis, quaesumus, Domine, '
                                                                'beata N. Virgo et Martyr imploret: quae\n'
                                                                'tibi grata semper exstitit, et merito '
                                                                'castitatis, et tuae professione\n'
                                                                'virtutis. Per Dominum.\n',
                                                       'latin_sha256': '7a2eaf7ab5fb11fe9b6eec0d428e6ac13d128aca84c5b2b7c612d19046541331',
                                                       'pages': [1382, 1383],
                                                       'printed': ['1363', '1364'],
                                                       'seed_locus': '1962 printed p. [30], no. 4394, left '
                                                                     'column; PDF838 / IA n837.'},
 ('commune-virginum-2', 'main', 'Secret', 'all', 1): {'english': 'Graciously accept, O Lord, the sacrifices '
                                                                 'dedicated to the merits of blessed N., Thy '
                                                                 'virgin and martyr, and grant them as a '
                                                                 'perpetual aid in our behalf. Through our '
                                                                 'Lord.',
                                                      'english_with_lf_sha256': 'e04ddff0670a36855c9051004bbbcdea1ac8226849bdd87e7c6af9a7fda176a3',
                                                      'historical_latin': 'Hostias tibi, Domine, beatae N. '
                                                                          'Virginis et Martyris tuae dicatas '
                                                                          'meritis, benignus assume: et ad '
                                                                          'perpetuum nobis tribue provenire '
                                                                          'subsidium. Per Dominum.',
                                                      'latin': 'Hostias tibi, Domine, beatae N. Virginis et '
                                                               'Martyris tuae dicatas meritis,\n'
                                                               'benignus assume: et ad perpetuum nobis '
                                                               'tribue provenire subsidium. Per\n'
                                                               'Dominum.\n',
                                                      'latin_sha256': 'b060f8757b58981dc9f3033ba4ef87fea00dfd0dcedc82515f613899e652b2b2',
                                                      'pages': [1385],
                                                      'printed': ['1366'],
                                                      'seed_locus': '1962 printed p. [31], no. 4402, left '
                                                                    'column; PDF839 / IA n838.'}}

ARTIFACT = {'byte_size': 508,
 'id': 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.phase4-common-virgin-ii-two-prayers-en-11658a3a',
 'path': 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase4-common-virgin-ii-two-prayers-en-11658a3a/phase4-common-virgin-ii-two-prayers-en.tsv',
 'sha256': '11658a3a8b1e605ae3c589ecba978ee0f556ea1f198ccfc44be96dc8d9ccafdd'}

OLD204_SHA = '2c68817c78cce4277c826cbab530ebd158f449a4081f6bc9bfc0f535d061a3f3'

OLD31_FILES = {'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-comm-impressionis-sacrorum-stigmatum-s-francisci--main--secret--all--1.toml': '0a1b0ca2f0c3b0048e13213cedf22dff67223bb951a61b7e4ed6f97eaa5f2629',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-abbatum--main--postcommunion--all--1.toml': '0f2f45d40573b1a7318a4c98e7ff06409e54ba21d0d54034c7a5d89b44ff558e',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-confessoris-pontificis-1--main--postcommunion--all--1.toml': '7d73bec86177496876f341844898071b7113656168b8e2ba1927fb3a009d4e25',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-dedicationis-ecclesiae--main--collect--all--1.toml': '42c1b0bcd728217b8f4219d7d55536288a94f44f3cb18d3d6878111bda2679aa',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-unius-martyris-2--main--postcommunion--all--1.toml': 'c3c8dad82671185828a399ce049cbde947b9c7e6add129977ab6371bd55dd12b',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-unius-martyris-2--main--secret--all--1.toml': '78ff16d43322771f700bda772e00c217dbf7c04ccec5196a98b0b829fa908a6e',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-commune-virginum-2--main--postcommunion--all--1.toml': '2ecf4125c203839da85b475e8881297a08322527795f5326a3c3bbe961e1f476',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-epiphany-5--main--secret--all--1.toml': 'bd0a6bfacc70169b4c27c6b3be2cf23a06d88141172fdb48db90c20e4ed17198',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-holy-monday--main--postcommunion--all--1.toml': 'e72e54b5a24cb11ea59a4e6963cdaac288f93d3cd8ea508d9795d47ba03046f7',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-lent-3-friday--main--postcommunion--all--1.toml': '463cd7fe35ee6d0c546c28d5eb91c1baf5cab833a3bf84924381a595a0bc6324',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-lent-4-monday--main--postcommunion--all--1.toml': 'd61c91f00cf8d27d0da56e999050f3a7c9daf4b6da93d993f8b9e0b0c4387cba',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-lent-4-saturday--main--secret--all--1.toml': '9691113c37b17019c66f8ac26251bd7dd8737877d93ca6f4538b7d043dc83c46',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-pentecost-4--main--postcommunion--all--1.toml': '63d97f1b7683a4467d7abd127b42837279783a00c181624a0562e9ce7c865947',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-pentecost-ember-saturday--longer--postcommunion--all--1.toml': '5d3be10fc352c176ddd916f2845ddfac60a493882fe45ff38f96adb2e5332f00',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-pentecost-ember-saturday--longer--secret--all--1.toml': 'e26d5db2417f30e3df6e69a887482fd6775d6b5096d3eb2e741c2a590d94f5fb',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-pentecost-ember-saturday--shorter--postcommunion--all--1.toml': 'c688dd2cc545928a00f7b0f333b410cb405ad696fcbe1f14db0accd02708363b',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-s-bibianae-virginis-martyris--main--collect--all--1.toml': '135f6181ecd04ffb73a88fec23476fdff86d612696243e115b7816b20a55b512',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-s-francisci-confessoris--main--postcommunion--all--1.toml': '0c598997dc32fec2dd803c1dbee5090ce679024c11c94a561291cfb2c6e8e5d0',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-september-ember-saturday--longer--collect--all--1.toml': '9b5be0eb465f1c6d3c96a159fe7d5d44a19d780e6ba0bcb26a499b3b113174a2',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-sexagesima--main--secret--all--1.toml': '79b41630405979cd7c00b89432b74ee4d412accc1cc9e799b2c5a08639d5bbcd',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-ss-quadraginta-martyrum--main--collect--all--1.toml': '2de49e67ac7561c1db3a19f1d42785b635110772202d7c9949d0cab531c9d178',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-en31-seed-ss-septem-fratrum-martyrum-ac-ss--main--collect--all--1.toml': 'e2be2028b2cbc30622cb8845251a9da0232c51f2505f5be76c59189ce96a8db3',
 'src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/artifacts/phase4-nativity-marian-reuse-en-ed897177/artifact.toml': '292f8877b185a0950d430dcb9cbdcf1f58b3d7ecb3a021b0dd7e52874de8d107',
 'src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/artifacts/phase4-nativity-marian-reuse-en-ed897177/phase4-nativity-marian-reuse-en.tsv': 'ed89717779d0b40259dee17372a269085854d3747c9aab34252df73c0a148f88',
 'src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/passages/publish-phase4-en31-nativitate-beatae-mariae-virginis--main--communion--all--1.toml': '9a07115231a348676ec49c93ae9f65730615fef27c5d0fe58686cc0a55f7f5cd',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase4-nineteen-prayers-en-0779811a/artifact.toml': 'd3a737f151ee456b35fcf402b209f088587d628330d47585d470115a69606148',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase4-nineteen-prayers-en-0779811a/phase4-nineteen-prayers-en.tsv': '0779811a3d96a3ac4ba4427d6d11e3cfca6cb18a6c4071ccbcc70b0d1a6e6999',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-comm-impressionis-sacrorum-stigmatum-s-francisci--main--secret--all--1.toml': 'bc02813d4139d329d8add9e04df63946f485d443b2302ed6574130d4c1119bf0',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-comm-ss-quatuor-coronatorum-martyrum--main--collect--all--1.toml': '803f5226389f297e20d2d0fa6fc2bb75279f57b0a93ea0b2a0eec359bf2e73ce',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-abbatum--main--postcommunion--all--1.toml': 'b31ec1f0a90260f230299bed6fda362185eb37d1c3ebbd90e976f4f21dc6ceec',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-confessoris-pontificis-1--main--postcommunion--all--1.toml': '6fb7415507bdd6ba0a7f1c37f2477228da0c5aeae609aa9252f2e74436d3633f',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-dedicationis-ecclesiae--main--collect--all--1.toml': '439ffe6b195a1e12720a96f1513847790ae7d7d2b1c84dacaea8ecfefad2b465',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-unius-martyris-2--main--postcommunion--all--1.toml': '58ec4639a3380946c45acef837c725b604a8c2e609bacea6176112f1db23bc2a',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-unius-martyris-2--main--secret--all--1.toml': 'eb4040129a08d07e19b2c9bfa22b2a22611ca64cc513fe01447db47117743370',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-commune-virginum-2--main--postcommunion--all--1.toml': 'c9f59b14b2b378c245c3b1ceb5150a82db2c6deb571ba2179de7d16a273d6bf4',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-epiphany-5--main--secret--all--1.toml': '581ae50ffb5b2060cf6cdab67ce7d2c9a843e7685c4f4768cf49a7a34173d5c9',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-holy-monday--main--postcommunion--all--1.toml': '8b686ed697b7b64697ad7b1d78a7909c22fcf962ad6c7f3aaff28d0f4a1ac759',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-1-ember-wednesday--main--secret--all--1.toml': 'fdc20e559eb9c4d580ab2433460ac4375f44ae6059c4d257d5188c6bb74a2ada',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-3-friday--main--postcommunion--all--1.toml': '71903c178c75f909c599e7bd2fa82069ea0f64f8976eb645d6d48ca549bf1493',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-4-monday--main--postcommunion--all--1.toml': 'ae6d400ec14d5c9210b3d92829085965bcadad83f8deced7aa5f6360a440f447',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-4-monday--main--secret--all--1.toml': 'f205adee753dbb86f58ff0429dc9f2d30bd861cbe633a10968217759a6ab1a19',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-4-saturday--main--secret--all--1.toml': 'ee0f4939b26d2a5ff552f348dd3441713d0548e477368dffab268fd27ad7f981',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-lent-4-tuesday--main--postcommunion--all--1.toml': '9578a4da345938ecbd0f966f151c056a63ccb17c9479a9ee8effe91194958d64',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-4--main--postcommunion--all--1.toml': 'a28ae1010c69957fa0a1b277c8b2c0b8df5ea3e27554705fe3f0bd7a1401762b',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-4--main--secret--all--1.toml': 'b5b96fe35f8e31ef16ae06062ff46bfe2218d5f995baa28b32a238a577a96009',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-ember-saturday--longer--postcommunion--all--1.toml': '3fc3e6c9791774c21df9b5e65370d5958fa566a9a23d42baa130d3181aafbd6f',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-ember-saturday--longer--secret--all--1.toml': '8ea8d51eca1fc6b39e72607cab4c563af18c24321d3246397055f285237aeaa2',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-ember-saturday--shorter--postcommunion--all--1.toml': '0edb0eeab914afb73336f44a09ee19c4f2f3d352c7ee48f24bd3dadb860aec2b',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-pentecost-ember-saturday--shorter--secret--all--1.toml': '38b808ed88e938ba802b7693d5bac905707fcf88a690f7583a95cd922aabe521',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-s-bibianae-virginis-martyris--main--collect--all--1.toml': 'a9cd15ade597c31d4ac5b79a783bb6d4d995b36b18fdcad1e7c9e3b89f4460fd',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-s-francisci-confessoris--main--postcommunion--all--1.toml': '6a932344580d203205f18a2b3b047ec3c3f96656843969a3a8e4f3aeb73286f4',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-s-francisci-confessoris--main--secret--all--1.toml': '7d83512e7acbdce07cbaeec5dc8cc26a75acda9e63f9f3e7879a4b48b4556a11',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-september-ember-saturday--longer--collect--all--1.toml': '86f037c978b56942c6ed716c63d8f8267454fc637127a13485d5084c3805c2bb',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-september-ember-saturday--shorter--collect--all--1.toml': '0bd6918442637347b3f7832519342ed2b40d3accfbf6f47d44fe49a93f757221',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-sexagesima--main--secret--all--1.toml': 'a163f965acacb4625a7e0ae29e65bd5184506f96914638000b1e7388ccb25316',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-ss-quadraginta-martyrum--main--collect--all--1.toml': '658367c578c189f7f9bf98265dddeb5482b7a6027334b4fe224f786886b7acda',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase4-en31-ss-septem-fratrum-martyrum-ac-ss--main--collect--all--1.toml': '91b0f255fd25d5bc8bb7d870f260400f22ddf07a44c098382da0aeae2729b44d',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-common-abbot-postcommunion.toml': '50c82a9615b4fd03d1078a8e53db493f63d218aa73357ff26a1ae842e553d55a',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-common-confessor-bishop-1-postcommunion.toml': '80438aaa2ac2d49db771a40ad2b69fd729dc63c32d1575462995d3ae99868d41',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-common-virgin-2-postcommunion.toml': 'b0c3b349be7c7b36509d1e178a9fd5e445d50535e7514a736e27b9900d55924c',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-dedication-anniversary-collect.toml': 'e63bd740a5ecf3362714ba6ef794eb8e3ab87c597dfdc5fe8b2c2dadc9784590',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-four-crowned-martyrs-collect.toml': '619172bea2fc65195ae60f0698d306e09b0a7d1bb2ceba86168b0e9fbeafbcc7',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-lent-3-friday-postcommunion.toml': '85d0acf01c1fc1e5ea510dfdf61b8d6053ce7d47f51aca191080aea20f42ebe8',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-lent-4-monday-postcommunion.toml': '37b4d483102c0899f656dd5baea8db359a969b8d92adc8e0c039d454d55df5f8',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-lent-4-monday-secret.toml': '2667a7475dbc4c4e293facf4607a21c38f5e36c76174f57a2ae4402cd7a4fa7c',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-paschal-martyr-bishop-postcommunion-haec.toml': 'f3c23e929b227dbb1530134c5247769638d66b0942d08a3ae1151dd66e1d699b',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-paschal-martyr-bishop-secret-munera.toml': 'f2c9c4ed7ee62643c15fa9babaf7596993b8520f5648569cca0e5722bf720ed9',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-pentecost-4-postcommunion.toml': 'f13745dd0ccd4c6aadb1a7b3f030557b9fadeb0c5b78f079b632079e1adc4f95',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-pentecost-4-secret.toml': '04cb7b6798683ca56d221f6c46ce520092c1088d0e6ce8211cba72e9ad639951',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-pentecost-ember-saturday-postcommunion.toml': '534a9d0891e4ccb2fbecca6c93b45156e78ec404074bb7831ad9ed02cf553865',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-pentecost-ember-saturday-secret.toml': '39fec68e2fd705406cf5a20e3e4cd81f81c57ca3ab35327afb76d9b55dab2553',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-september-ember-saturday-collect.toml': '5f9975befcc5e0c340ee53e1e44de038d1e5f33e54759233530108630ca0d0f5',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-st-bibiana-collect.toml': '3094215e8687398ba7f57e5ccd27613dbf1fafbd26970e332db3edec05a012c4',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-st-francis-postcommunion.toml': '8c466bcec735f60a5f7808a204adff8988fd2cc5e021196e57aa6ec22cf562ed',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-st-francis-secret.toml': '201416ad4a4122a88f264e97433cdbc487f0b50cfaa74c35ed3d423251d15feb',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase4-en31-lasance-supplementary-mass-3-secret.toml': '3b47887f81314a2766821c6eb03b87f4ae66da59888f67ed8c66c0da03a7f261'}

FROZEN_COMMON_FILES = {'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/ia-facsimile-pdf-363d6fc3/artifact.toml': '50af0360ef7cee43b0be7a77f211e8c63dc57f7db868a0a4f103f2e3b6056fc8',
 'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/missale-romanum-1862-text-f34bc7cf/artifact.toml': 'f11f0261f3faa3eead52eac8cc04962cdf54f2b4955ff94bcdf8780d959d487c',
 'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/missale-romanum-1862-text-f34bc7cf/missale-romanum-1862-text.txt': 'f34bc7cf9293ffb353159e94118f4316bb4cc0a60230b315904dc77ba2502162',
 'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase4-common-virgin-ii-orations-pages-698-699-20261022/artifact.toml': 'a711df90bda4c44ab68d27da45ec0ec5e2c873f440a0a99a83f2c19c826f9c1f',
 'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/artifacts/phase4-common-virgin-ii-orations-pages-698-699-20261022/source.pdf': 'd78a82cf27b7fc5aa1e8aa92714304ede819fef4848cbd4f0eebaf2075c55369',
 'src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862/passages/phase4-commune-virginum-2-collect-secret-page-images-2026-10-22.toml': 'd508a0a3f8b597d7ef5a302286abd52631aae78211178dca117d9a68d5c122cc',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/artifacts/cmaa-facsimile-pdf/artifact.toml': '9e2440cfcf8fd3a0bc86dfc57bd9871992b9bca4fd5baced4ce07c7c06c48fbf',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-commune-virginum-2-collect-word-repair-recheck-2026-10-22.toml': 'abddfa1923513f536f58a3afcb394cad99d72d09ce19b3217d7dfdef1e592ff4',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase4-commune-virginum-2-secret-word-repair-recheck-2026-10-22.toml': 'ac7b3b585468053e8ae3782b86ef75f37926b61839bfdfd209c508bc700c99b3',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/artifacts/commons-2-orations-8f0f1a33/artifact.toml': '75c407c140acabe5e15a9328ecc8b7c29fbf86c449307cf2fd014f38232f05c5',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/artifacts/commons-2-orations-8f0f1a33/commons-2-orations-8f0f1a33.txt': '8f0f1a33bcd92be8742d2d69e89ddd5c455c180f33c64f1f584f40638e087995',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-collect.toml': '7252a4a2e2f055b2ab8dd194b96778d458a74b1e0576c43398bdb0724aea18f4',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-postcommunion.toml': '21ea32617470b8748b3fcdc63a2eb9dc60e659ad00735502529d67aa68ea7bca',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-abbatum-secret.toml': '31488b03b8823baf47edb94c91355437bcd600d4680c25ea3567545dbe8bcd09',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-collect.toml': 'a4eb206c3cd7bef5c783bbf59e5702127a35a07ad56c01395027374212144481',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-postcommunion.toml': '750393a112746fd9a7b61c5dc05059fe8c67edd322e5ec259320ce7250253d76',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-confessoris-non-pontificis-2-secret.toml': 'dd2d2a42fee2a7c2605f684d688f7ca1e8e5bad68b5fbbf78ca6fc87c551ae51',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-collect-in-ipso-die-dedicationis.toml': '641478b09b534155b181de1ed6b10c51f8120293bc3ee939ae7bfc958c901491',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-collect.toml': 'f0aa7a9273ed9735b79138cea3651b6d00a9a2be9e8af54c029a29d53fc942a6',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-postcommunion-in-ipso-die-dedicationis.toml': '0aeaf00caf4a6b49ef6316d8bef1632f4360a24f59df7fda3f606bc33d66dfa5',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-postcommunion.toml': '2b4c8ff178bb0a94f5a31b001bef9cb00de999aa18fe94ef4ea491349c84d015',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-secret-extra-ecclesiam-ipsam-dedicatam.toml': '84f414c23345f2c7d7700f21b240df105dbd0b06ec85faf55dbd3152d721a360',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-dedicationis-ecclesiae-secret-in-ipso-die-dedicationis.toml': 'ad9cc763cc6233b844202f387b4afbeb4869fc2538e41fedb88897cbd2ca8676',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-collect.toml': 'da558610b6a9852462312137b3925250f86d234ecab96eef738b80d45897d296',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-postcommunion.toml': '83f0215a1e9f8f9ea0c11be3c5f6d60ec95bb33428f32958c4de5646f971a871',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-festorum-bmv-secret.toml': '661fa79d3160eda9fbb0dae4a69477689f46f1bd107f6c11baa637d4151805f5',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-collect-pro-pluribus-martyribus-quae-non-sint-virgines.toml': '417b5c09bc41eb2e43ea97de9f56215752c25d5e63c5355448e105ec4567d6b6',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-collect.toml': '9b811bd6bcbeb621b00c0ac58d7819fad77ae033b5ad75751e7149673d0e8f9a',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-postcommunion.toml': '57794ddaeaf2b0e4fbe8f3c3070c04d9cf77efefc994f2365947cc1cc8af8ae4',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-secret-pro-pluribus-martyribus-quae-non-sint-virgines.toml': '2c505965b9d3c37b86f85dd543038e8b2819c17966a3ddc2731c89f38a159890',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-1-secret.toml': 'cd7f861800c9f3194ff871532576d2ea2946e98ecf6dc0dffea498c1b0305ad1',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-non-virginum-2-collect.toml': 'b18a9d6822a38059d7901fce1d6ec00607635ce7721870bf98de78d228839100',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-collect.toml': 'd469c7124b22915b8473da03060f7e44a548a493695122abbc5e407f483c07b5',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-postcommunion.toml': '5374407b323342ac39bd2b4333f07c838bad4273c6389f48f2f37ffea344f063',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-1-secret.toml': 'e000171fb26bdf467c281d3e169092fcdf97ede5a362e95f44b8624e78c48bd6',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-collect-pro-pluribus-virginibus-martyribus.toml': '8f6e8f21255ecb84d48b18ebd637d6cd4c579ee8ba857cee72b8abaa26ba5457',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-collect.toml': '2216f2b1cda0074f6995b9960118c7ef91afadad4c5f6a113a2b59efadf8c25a',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-postcommunion-pro-pluribus-virginibus-martyribus.toml': '4359b1a34b45c4eab70d8c572c0ae82eeeee16e0c8b1eeb474207ff8d69eab25',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-postcommunion.toml': '45d96bcc7d8622ae9f0ea0e8cfd2274ceb9c898575dff7f154814646b23aefff',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-secret-pro-pluribus-virginibus-martyribus.toml': 'f67c2b24b2d5222b23c25341972929eadc9cf20572b8deb73bad83834b7ea2b9',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-2-secret.toml': '90fab9ea36f94010efff1e16a8f7a6eff2cbaf8224bb664180b83ab9d81a7862',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-collect.toml': 'db9b43044b38148ac620fb41859c64a9dcc3edb197e92f36d460a22e70dbd7d0',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-postcommunion.toml': '3033c5a9a25bafd807bb4fabe1cdbf0334ffd7f1d2949082aa6025bf12b5f664',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-3-secret.toml': 'b70655eed2dec984dc49b1c19535ca7648649f343b068f360e6c99283b6a6d5b',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/commune-virginum-4-collect.toml': '5f9b8505eb97c221fee202acdfbb2aeb8752c25e5c27c097fccb539d6d20f692',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-collect.toml': '49cbd6e444bfd8158017c10d0858bfeedab4cd4ad917425f7313863b29dfe756',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-postcommunion.toml': '8fa0478e6b1c1da3ee11c099b9cf8a6a928d6d54791294742eb29b0816dd8f13',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-1-secret.toml': '7e84319c635e8af03752b1707a2a17607619e7f94749370bdb2dab2cbd28f6d6',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-collect.toml': '38984de29887653b011b15237c6a3539b25347fd6770495730b998f1a0646fdd',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-postcommunion.toml': '5fd60100fe3f3d2733925eed38a16d6ec7f0af10d29dd050bc2f8a67612a3dd9',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-2-secret.toml': '392fe22bed075848cb789f4614f621f985902ac6af8d2d6842d3ec7e704d75a0',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-3-postcommunion.toml': '7419043b9d38717fdcc66de8f7e5d76f300a09f51f9374f7f0d88f222f9f6380',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-4-collect.toml': '49b0a1528eb7cf2f030efb841adf746bf7004f2939d07d34edea908383d49675',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection/passages/missa-de-s-maria-in-sabbato-4-postcommunion.toml': 'abdd025d3a41c72b7fb5dea54d08467758cba9e4e6adc5e0bfbae1e0561e79a1',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-common-virgin-ii-two-word-repair-ce623d9f/artifact.toml': 'becfea4f799e4cf8a39283d2eaedda167f5e95ae4aaba846b7194a951ef5e327',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/artifacts/phase4-common-virgin-ii-two-word-repair-ce623d9f/common-virgin-ii-collect-secret.txt': 'ce623d9f71e6021c3e7121f910ef5f7adce6122d6e007eb5905ec50834a6841e',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-commune-virginum-2-collect-word-repair.toml': 'c45f489a1bef41e1d76235acf87a4213af61dfb1702d5475ce218cc5b2a56f7b',
 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-22-editorial-projection/passages/phase4-commune-virginum-2-secret-word-repair.toml': 'acb85acef18d5d59091384294139e0db7053df00d8d5e470f9d276965a51c722'}

COMMON_ROWS_SHA = 'de2894782e4de987679556937182ec5ec4c213d40ccf99070b6f3ceab5184415'

SHARED41_SHA = 'e0b7682ad67b1aa372c3bc6c550235595e1bdebd20191e4890debd1366beff3d'

COVERAGE = {'roman-1962': (1427, 219, 1208), 'roman-pre-1955': (1378, 206, 1172)}

CONSUMERS = {'comm-s-christinae-virginis-martyris',
 'comm-s-dorotheae-virginis-martyris',
 'comm-s-emerentianae-virginis-martyris',
 'comm-s-margaritae-virginis-martyris',
 'commune-virginum-2'}


class CommonVirginIIEnglishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prior.English31SourceTests.setUpClass()
        ctx=prior.English31SourceTests
        cls.p,cls.doc,cls.records,cls.entries=ctx.p,ctx.doc,ctx.records,ctx.entries
        cls.bodies,cls.witnesses=ctx.bodies,ctx.witnesses
        cls.latin=tomllib.loads(LATIN.read_text())["entries"]

    def test_fresh_whole_historical_english_and_latin_seed_pairs(self):
        self.assertEqual(len(ORACLES),2)
        for key,o in ORACLES.items():
            row=self.entries[key];verification=self.records[row["passage_id"]]
            self.assertEqual(row["translations"][0]["text"],o["english"])
            self.assertEqual(sha(o["english"]+"\n"),o["english_with_lf_sha256"])
            self.assertEqual(prior.words(o["historical_latin"]),prior.words(o["latin"]))
            self.assertTrue(o["english"].endswith("Through our Lord."))
            self.assertIn("N.",o["english"])
            self.assertEqual(verification["artifact_page_ranges"],[[o["pages"][0],o["pages"][-1]]])
            self.assertIn("printed p. "+o["printed"][0],verification["context"])
            self.assertIn(o["historical_latin"],verification["notes"])
        collect=self.entries[("commune-virginum-2","main","Collect","all",1)]["translations"][0]["text"]
        self.assertEqual(sha(collect+"\n"),"206a2d6c3598c7e9cacd22506cc19e6833cd2def47eb721dee329b59ad354c51")
        self.assertNotEqual(collect,"May blessed N., virgin and martyr, who was ever pleasing to Thee by her merit of chastity and her profession of Thy power, implore for us Thy indulgence. Through our Lord.")

    def test_accepted_entire_canonical_bytes_seed_locus_and_short_endings(self):
        for key,o in ORACLES.items():
            self.assertEqual(self.bodies[key]["text"],o["latin"])
            self.assertEqual(sha(self.bodies[key]["text"]),o["latin_sha256"])
            self.assertTrue(o["latin"].endswith(("Per Dominum.\n","Per\nDominum.\n")))
            row=next(r for r in self.latin if r["mass"]==key[0] and r["proper"]==key[2])
            self.assertEqual((row["text_sha256"],row["publication_status"],row["publication_basis"]),(o["latin_sha256"],"permitted","public-domain"))
            seedid="passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-en33-common-virgin-ii-"+key[2].lower()+"-seed"
            seed=self.records[seedid]
            self.assertEqual(seed["locus"],o["seed_locus"])
            self.assertIn(o["latin_sha256"],seed["notes"])

    def test_exact_two_owners_ten_actual_recipient_references_not_ten_entries(self):
        selected={k for k,r in self.entries.items() if r.get("publication_artifact_id")==ARTIFACT["id"]}
        self.assertEqual(selected,set(ORACLES))
        self.assertEqual(len(source_batch.historical_english_entries(self.entries)),219)
        for calendar in COVERAGE:
            document=self.p.load_calendar(CAL,calendar);refs={k:set() for k in ORACLES}
            for _,mass in self.p.masses_of(document):
                for form,proper,taken in self.p.appointed_propers(document,mass):
                    owner=self.p.source_slot_identity(document,mass,form,proper,taken)
                    for key,body in self.p.coverage_slot_units(proper,owner):
                        if key in refs:
                            self.assertEqual(body["text"],ORACLES[key]["latin"])
                            refs[key].add(mass["key"])
            self.assertEqual(sum(map(len,refs.values())),10)
            for key,names in refs.items():self.assertEqual(names,CONSUMERS)
        for mass in CONSUMERS-{"commune-virginum-2"}:
            for proper in ("Collect","Secret"):
                self.assertNotIn((mass,"main",proper,"all",1),self.entries)

    def test_exact_new_payload_binding_and_altered_word_or_identity_refusals(self):
        payload=(ROOT/ARTIFACT["path"]).read_bytes()
        self.assertEqual((len(payload),sha(payload)),(508,ARTIFACT["sha256"]))
        rows=list(csv.DictReader(io.StringIO(payload.decode()),delimiter="\t"))
        self.assertEqual(len(rows),2)
        self.assertEqual({(r["mass"],r["form_id"],r["proper"],r["cycle"],int(r["occurrence"])) for r in rows},set(ORACLES))
        for key,o in ORACLES.items():
            row=self.entries[key]
            self.p.validate_translation_publication_binding(row,CAL,LEDGER,self.witnesses)
            for field,value in (("mass","comm-s-emerentianae-virginis-martyris"),("form_id","wrong"),("cycle","A"),("occurrence",2)):
                changed=copy.deepcopy(row);changed[field]=value
                with self.assertRaises(ValueError):self.p.validate_translation_publication_binding(changed,CAL,LEDGER,self.witnesses)
            changed=copy.deepcopy(row);changed["translations"][0]["text"]+=" Amen."
            with self.assertRaises(ValueError):self.p.validate_translation_publication_binding(changed,CAL,LEDGER,self.witnesses)

    def test_all173_and_all31_previous_entry_and_binding_dictionaries_preserved(self):
        keys=sorted(set(prior.OLD_KEYS)|set(prior.TARGET_ORACLES)|{prior.REUSE_TARGET})
        self.assertEqual(len(keys),204)
        self.assertEqual(digest([self.entries[k] for k in keys]),OLD204_SHA)

    def test_all76_sealed31_source_files_are_byte_immutable(self):
        self.assertEqual(len(OLD31_FILES),76)
        for path,expected in OLD31_FILES.items():
            with self.subTest(path=path):self.assertEqual(sha((ROOT/path).read_bytes()),expected)

    def test_accepted_common_latin_proof_old43_old9778_and41_bindings_frozen(self):
        for path,expected in FROZEN_COMMON_FILES.items():
            with self.subTest(path=path):self.assertEqual(sha((ROOT/path).read_bytes()),expected)
        common=[r for r in self.latin if r["mass"]=="commune-virginum-2" and r["proper"] in ("Collect","Secret")]
        self.assertEqual(digest(common),COMMON_ROWS_SHA)
        old="artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.commons-2-orations-8f0f1a33"
        historical_latin=tomllib.loads(source_batch.historical_text(source_batch.LATIN_PATH))["entries"]
        shared=[r for r in historical_latin if old in r.get("publication_source_ids",[])]
        self.assertEqual(len(shared),41);self.assertEqual(digest(shared),SHARED41_SHA)
        collect=self.entries[("commune-virginum-2","main","Collect","all",1)]
        for ident in (collect["passage_id"],collect["publication_passage_id"]):
            notes=self.records[ident]["notes"]
            self.assertIn("extitit",notes);self.assertIn("exstitit",notes);self.assertIn("NOT OCR damage",notes)
        artifact=self.records[ARTIFACT["id"]]
        self.assertEqual((artifact["rights_status"],artifact["rights_jurisdiction"]),("public-domain","United States"))
        for phrase in ("A110108","A192159","1298a-1298n","1302a-1302d"):self.assertIn(phrase,artifact["rights_basis"])

    def test_current_both_calendar_coverage_and_original_advent_hold(self):
        historical_entries=source_batch.historical_english_entries(self.entries)
        for calendar,expected in COVERAGE.items():
            historical=source_batch.historical_english_coverage(calendar)
            self.assertEqual((historical["slots"],historical["with_english"],historical["ledgered_untranslated"]),expected)
            row=self.p.english_coverage(CAL,calendar)
            source_batch.assert_current_english_coverage(row,calendar)
            for field in ("unaccounted","outside_the_ledger","unmatched_records","stale_translation_records","rights_restricted"):self.assertEqual(row[field],0,(calendar,field))
        self.assertEqual(source_batch.historical_english_coverage("roman-pre-1955")["inherited_inapplicable_records"],49)
        key=("advent-2","main","Collect","all",1)
        self.assertNotIn(key,historical_entries)
        overlay=self.p.translation_overlay("roman-1962",CAL)[0]
        if key in self.entries:
            self.assertEqual(overlay[key],self.entries[key])
        else:
            self.assertNotIn(key,overlay)

if __name__=="__main__":unittest.main()
