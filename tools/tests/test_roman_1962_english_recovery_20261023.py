"""Full-prayer source and publication joins for the 23 October English recovery."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
import copy
import hashlib
import json
import re
import sys
import tomllib
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
LATIN_LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
ARTIFACT = 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-2026-10-23-913430ca'
ARTIFACT_SHA = '913430ca8abf6959e6d3c18e9c79ef28d69f9e79343de48e038a3b06f403d1df'
ORACLES = {('comm-s-agnetis-virginis-martyris-secundo', 'main', 'Collect', 'all', 1): ('e4ed2371ac9229f90fd2fdcdd34d23b2525eac13aec03d479230e04aad35ede3',
                                                                             '597e91e678124386ab68c3013b5f55665a401c2ad010b27dfdc02519318c44c3',
                                                                             '313ac4c618a740aa2a53cf97dc8e00bf1ab50f121ad815b958b6d046e1b7b9a7',
                                                                             [891],
                                                                             ['892']),
 ('comm-s-agnetis-virginis-martyris-secundo', 'main', 'Postcommunion', 'all', 1): ('681adfe42c21db528531e97d7b3caed76ec711d26732eac9a052f61ae2d8a67a',
                                                                                   'b7e4296770576cca60964922397e20095d59953563a414d85d619e5d3d2b2d0b',
                                                                                   'e1aa29a2a9483511d83628a9c322b229459fc2fe9f7cb99b643bad811025b233',
                                                                                   [891],
                                                                                   ['892']),
 ('comm-s-felicis-presbyteri-martyris', 'main', 'Postcommunion', 'all', 1): ('aea56afd4ba65a9041f053db6a311d691c4acc0d567824cdd5f30a796d62e37e',
                                                                             '244b717b0f945af67bf25c112a479da3c62f48e89e24b2842e57f9a5d0b7b960',
                                                                             '551e23594dccbb09b77991d37fa951a9f72e349e2c2d03cacbccb54a84030bdf',
                                                                             [861, 862],
                                                                             ['862', '863']),
 ('comm-s-felicis-presbyteri-martyris', 'main', 'Secret', 'all', 1): ('0d83d6a2a255898962309d294cfa6fdade0f3482c15f159a71001b3c2c8dd495',
                                                                      '5011e93d3687c7cca3c5c8090d35595009e6ed4f969c3c925c295b2afc224e11',
                                                                      'aaebb18c35a7432b03f85f81d3142085b6d6bc9a816dbe5ff8887dad60a52881',
                                                                      [861, 862],
                                                                      ['862', '863']),
 ('comm-s-valentini-presbyteri-martyris', 'main', 'Secret', 'all', 1): ('db9e0987d46cb7a86489374015bc7ff0ad472cea3f572ce31c21d587098a41d5',
                                                                        'b4cbab638fafb34615c315ea068141ad391da0268b11bc6c257acc6ae70d843d',
                                                                        '26b279f0bf862e0946e308c761554ccc67492d09dd954204297bf1e37e47f5a0',
                                                                        [922],
                                                                        ['923']),
 ('comm-ss-marii-marthae-audifacis-abachum', 'main', 'Collect', 'all', 1): ('2ef11b9b712b47cd8a05d6fda0ca578ad8e41547b9f28c6dab1cc8897f142d14',
                                                                            'a93bd9a25a0534556a7f5e2aa9ad23bc9ee6c720dd683c26f3883a6491e8e73c',
                                                                            '51c5857748b6697df98610bbca7f9c2ca6da76507b08b7f060fb6a20567b8207',
                                                                            [873],
                                                                            ['874']),
 ('comm-ss-marii-marthae-audifacis-abachum', 'main', 'Postcommunion', 'all', 1): ('f7709aeff3e6254eb0ce96983b045c82586cadd442a98cba471c10bceb05f4a5',
                                                                                  'a5ff85aaa1254e279095a2fb04b46834111313975b348621c2280c0e25f318b5',
                                                                                  '003d2b3c75183d9c66ca2fa4178f2b6d803211ecfdf53152cc75849ec1e2c64b',
                                                                                  [876],
                                                                                  ['877']),
 ('commune-martyrum-tempore-paschali-1', 'main', 'Postcommunion (Pro Martyre tantum, item altera postcommunio)', 'all', 1): ('accb3a69fa98109ba685b0d7d33e53319a76d95d855d5a0a764c73aaf5e3e56a',
                                                                                                                             'b127729c6c18f6bcc643a4b76a8d6bf5e1df1ed904ea5103834393eb8915351a',
                                                                                                                             '0f33eab8caf8072619e6e93b0490c0c41c9448130f3c4b13c3f7c0f6de272e1c',
                                                                                                                             [1351,
                                                                                                                              1352],
                                                                                                                             ['1332',
                                                                                                                              '1333']),
 ('commune-martyrum-tempore-paschali-1', 'main', 'Secret (Pro Martyre tantum, item altera secreta)', 'all', 1): ('0d7e1255da8cf29a71c5f6a31a0acd5b5b2bf7dabbea662177d0ab36988949cb',
                                                                                                                 'a8ac08e1fb9e030a0cb1cc46c0b389c753d5a91e228c92ae3d4fd3a52ffabfc3',
                                                                                                                 'de1113e161f5b2f9cf5e48e681af6472787a5261267a3eb4ba9007012741e279',
                                                                                                                 [1351],
                                                                                                                 ['1332']),
 ('commune-non-virginum-1', 'main', 'Secret', 'all', 1): ('f3a71b2ece360dfe5a7e5fd16490c9c2776317f43218c28b7ecf0c32040457c5',
                                                          'db61a1f2c51a376a5e3e285c6f49a85f37ceb10ed3888d40d2cc87209f74fe7d',
                                                          '9a5f725eda829889ea9bdb18f0444cf636d19b10067cb1c2c207a7c4f196a6f3',
                                                          [1401],
                                                          ['1382']),
 ('commune-unius-martyris-1', 'main', 'Collect', 'all', 1): ('8ea87dff0e938627fd30710a37dc20eab6a80b7a1d830adef7898e5488eac9d1',
                                                             'b83a6e36b19d464701b3e1ae955dfb1c358c13b1979a1eb1184a61d7a5fb4234',
                                                             '76dca1e2baec26afd9652a7a53e5929f342f7ab07658bbca69953775729aaa2f',
                                                             [1348],
                                                             ['1329']),
 ('commune-virginum-2', 'main', 'Postcommunion (Pro pluribus Virginibus Martyribus)', 'all', 1): ('fdcb7b9e193daac45e7f62579f4f30f7d1ea810d04de343c608e1ca2651e24ca',
                                                                                                  '08eb411bac4a27731d81b8abedc4481fba96098d326d79090fd31798e4e08da5',
                                                                                                  'd42362fb583ac3ab62dbc58eaa6484f47fc4151074a4ddc22cc06458d5cbb83c',
                                                                                                  [1388,
                                                                                                   1389],
                                                                                                  ['1369',
                                                                                                   '1370']),
 ('easter-2', 'main', 'Postcommunion', 'all', 1): ('282b835b459d186798e93b17b519c676f77878db656e748541d5d28afd6aee9b',
                                                   '782d7e1ea7d5ed6e4bc62622b9de6b72bf027cc83483a182acff841e43987367',
                                                   'fca2c75eecc1f7bdd9d93f6d7a74b22209976c9cc3325c5dbac7c1c2b5951495',
                                                   [567],
                                                   ['569']),
 ('easter-2', 'main', 'Secret', 'all', 1): ('63f5a49c360a7a70856e4c94725515f4b60f64812cf08310b48b7084d6be610e',
                                            '7c639867fb299d2fbd1bb1cf5b19c7f6fed6431c039bd181d9ff99649551f8b5',
                                            '73761d9f8e18abc140df0f58c54e28819cdc22be4f41bee499f7b9498034320c',
                                            [566, 567],
                                            ['568', '569']),
 ('easter-3', 'main', 'Postcommunion', 'all', 1): ('61040a2d77551606b34fdbb61f21e57833c8c47dbb89a0ef5c45896303670347',
                                                   '6445c5e5129e1d957261939390a8a24ca1efe3ed3a14901ecf2ca60f6ac2ed47',
                                                   '7236a0f6b76e54fcd5daad5b686e6008db1f419280e9a29240555b84cdeb7873',
                                                   [570],
                                                   ['572']),
 ('easter-3', 'main', 'Secret', 'all', 1): ('c3ae5908b2ed82e73e4fd1ff5c9e0e4aab078a75f173217240ab0a99696da359',
                                            '83b4d0df0d8ce4f065b46ab6eeeed144700c4bb21b9b0f5f78553ed29f8e918c',
                                            'f34967db2d9aa56181892f4ae2b5c5953a3259da5cccb78e7d9e4d530d92abe8',
                                            [570],
                                            ['572']),
 ('easter-4', 'main', 'Collect', 'all', 1): ('bda6482fdb6808169e0afb185b113dd5f19e58d2d7df499d7dcef13c7ec76b1b',
                                             '9c364cadf651360e4ea2258e54a31a539848946eae5ea055caf1841d9ddbd422',
                                             '66c9f4719e1765a86ceb28ff58a298eac20e55d2d211d58ae80895690bba0f6c',
                                             [571],
                                             ['573']),
 ('easter-4', 'main', 'Secret', 'all', 1): ('c26cb426aa2903dc7ab1caae9a1197b639833e63853eef4eb227863b976f5dd9',
                                            '5a6e8af98eb12f8da33cb757ea88840c4a82ea02e74463d3fb6665205b6dc63d',
                                            '55bd2a957d08d53d516e7449841d81d5eb24dffbe6bb50aed51848a5af32094c',
                                            [573],
                                            ['575']),
 ('missa-de-s-maria-in-sabbato-4', 'main', 'Collect', 'all', 1): ('ae2e3d4ba13f641b171cc893a79f28f69a4c83700fd2aac9c3fe3c691b9769d6',
                                                                  '05953f0cfd52e2502b114616c346e11d3a9318e1a976c63d617ba0ae92cac58c',
                                                                  'f33675d6460b78ca9776a47ce4951d9a1349b82d4a05a3ae228a75a0c6f52475',
                                                                  [1414],
                                                                  ['1395']),
 ('pentecost-10', 'main', 'Collect', 'all', 1): ('afaf2f6f4cd524abcc48ee5c8b1b97ee2f05a97efb1b7e775acdf9ac48518af3',
                                                 '2606c39705cbd81681f8381ea015d267c682d0453ae1f931e1655d7ac4736bfb',
                                                 'edc5dbd313ea91057e45134c173486c02c178369f0a7ce3482e167503252139d',
                                                 [670],
                                                 ['672']),
 ('pentecost-10', 'main', 'Postcommunion', 'all', 1): ('f1830209032a40650d6e48ff93ffd7988e823ae2b1873037f68b8503dd3a8f54',
                                                       '8b4ac6154e2f8e3228841f626b6551d8f8a64b457c1145f6d646f68ec7bc69ef',
                                                       '36edac3709beaebbf9bec64a71b565a0e5090bc123b041dbd8e7adca387123ac',
                                                       [673],
                                                       ['675']),
 ('pentecost-11', 'main', 'Postcommunion', 'all', 1): ('da51c4ccb4263098cf60f25fadf53ed822ea5d102579ee9dac632dd4473ef33a',
                                                       '47d33ed7d65d95cd6bca8db8ec9eecee8e5b287e55977256b02fd4f920f61ec4',
                                                       'e9372b296f2d8126bb56f683dcac4ae51bb8f8bb2607b578ee58ed9843fd4ef5',
                                                       [676],
                                                       ['678']),
 ('pentecost-11', 'main', 'Secret', 'all', 1): ('40ba71ae2f54009c2b6256330a43069b5c8c9c49743da7a8f5d0a2f85d2ceb7f',
                                                '9f11b6e4c480a28f8fe2c53c228b385e6846756a69350cb9950009aa4a64b4bb',
                                                'bf84f718f03ded7025241c0d18cb594c5a63e775904995206fcd78357637359d',
                                                [676],
                                                ['678']),
 ('pentecost-12', 'main', 'Collect', 'all', 1): ('d33e23d1a728f4c09bbdb4fc253207291282cd0f6328c07eff9f782bec187fe5',
                                                 'e8b9246f30a78ae00a1a32e83edb43c05e3f0f4ff4cb70b5337e306a06358ebc',
                                                 'c399363b16e33522f25274de001d4845709b5b39503c893cd47499ae89ae90b2',
                                                 [677],
                                                 ['679']),
 ('pentecost-12', 'main', 'Postcommunion', 'all', 1): ('b912ed5a51974a59f09f13c871172d1cf66b418b7bee0d255937555befb35085',
                                                       'a6b64e74fb7fe3c70633b77fec9419fc4c658fe3c10c3da15fa55d3bc0447e5e',
                                                       '60e2f473d9ffe2662476ef0d6c1319fc436b3b4a72a831c181d4a0ce2d7c4865',
                                                       [680],
                                                       ['682']),
 ('pentecost-16', 'main', 'Collect', 'all', 1): ('8766f18eeafbbfa789e8973258ac31c9723620cad06795820bd02883b1c7c0e4',
                                                 '1bcaf42c23c959b1d90b35f66d593da2337a22089f51a9af5fa8a54de5a2fa6b',
                                                 '63fe0b96a4a4e941dbd4efe049f554bf171a511ec5d5230e568156429c7e7a03',
                                                 [691],
                                                 ['693']),
 ('pentecost-16', 'main', 'Postcommunion', 'all', 1): ('37b31b897df44a69ce44c503fb2db0e908cd8d2c70f2cd908ec5412640cf1329',
                                                       '539d86e0b8886c98c9fbb09c8794c7c45b66258674fe0fc6c650774ff885a303',
                                                       'd85b4eaf2198a2144635190ed12db68ef145e70fa8c528b44930a539665feddb',
                                                       [694],
                                                       ['696']),
 ('pentecost-16', 'main', 'Secret', 'all', 1): ('8e7f9d28652bbd6eed2bc6cfcb885869c97b28115972412c757a50960a960121',
                                                '1fccd23fd2f05a6ae0e805fa5be5abc26d5b8496f7f0e70602d91dbb7e474832',
                                                '723d50d26e5796b42fa8df5b6a91996f771d98ad287ea01e314935256588e595',
                                                [693],
                                                ['695']),
 ('pentecost-18', 'main', 'Collect', 'all', 1): ('0beb868eef7502c505d90fcdd19507e7745fd64adb766c3e1028169a0a59f8c7',
                                                 '920bcf20c9a4cc5d66a7bed24234f9f725d5d736ed7a7aea6161acca755939ca',
                                                 '258f8ad4f6abda162f5a6932a6d1722c54e68841e8c88c59a1b3ad36c321fcf7',
                                                 [715, 716],
                                                 ['717', '718']),
 ('pentecost-18', 'main', 'Postcommunion', 'all', 1): ('6cfc433858a64e3e6ebb7e423960e086531d81979db24afb5a8ec853959ddc5c',
                                                       'dfc294ef66d70fea0252b291e496f35c9d71c94fbb4d68e976581dd832ada0e2',
                                                       'd4fc475ce32f018daf84fb81d0ece49c83e5848780e2dc9cb39d69dea8063531',
                                                       [718],
                                                       ['720']),
 ('pentecost-18', 'main', 'Secret', 'all', 1): ('7da7d48d5f3c1617670c8dd2770f56bd63faa6c3641df228b4d7e7ff29076038',
                                                'f8d0c737e88fb55c0a281ba7900d6f9c819f228b26630b3ad1c07f8d477ec96e',
                                                'f3476be57223ef373d317a3fcdc22892288de737bf7c2e2f806897b61cc2d316',
                                                [717],
                                                ['719']),
 ('pentecost-2', 'main', 'Postcommunion', 'all', 1): ('f8e3a44b3ccd8425a190150374a23887f82f6f77994213b1caaa570eadcf0822',
                                                      '508f35eb35bb2e589e61816f262a7325a353472851c3c4d7934b7f52fc725e75',
                                                      'de9d53187ebbc5ba6c0ca2116958328ad94751b9c4a27c28bffe7ddbbfe473a8',
                                                      [641],
                                                      ['643']),
 ('pentecost-2', 'main', 'Secret', 'all', 1): ('4f90c74b9d0bee425158e066f37e176cb92cb53db453f59b7b4a5b5ed0da1219',
                                               'b937a0f20ba9b0a556042737a9f0f020a10a65d42247f33a234f3e02e3034066',
                                               '6ceab47e017955980f92ca7d7d1d47277c54bc23e6c20eb51c899d91ecd5411f',
                                               [641],
                                               ['643']),
 ('pentecost-20', 'main', 'Collect', 'all', 1): ('4febdef07b08549f84d5ac9604a1bb333d1bc10e2583654b02a4530c61314262',
                                                 '864597d5f08a54721142862d66eaffea420d7fd063e479ec8dc394317b2700bc',
                                                 '3098b3352a492622ae77fb21635cb9bb704af4b9bd2d063f0a097b3bb9c965e0',
                                                 [722],
                                                 ['724']),
 ('pentecost-20', 'main', 'Secret', 'all', 1): ('a65cc0670230ed46e963ca0c4aa5283217244e8009d51e518e16eed0b4d1d41d',
                                                '19d0eb5bd97f061714cee28eeb944b39a523227615b2bb78b4f0db96ce90fcc6',
                                                '348ad3ea9a53551074c6f3c3ffa7b4ec0dc45388425697252400e71b499e30ee',
                                                [723, 724],
                                                ['725', '726']),
 ('pentecost-3', 'main', 'Collect', 'all', 1): ('d980b2bd8ac2698e378442d130f7f28ebb6d18a6e894d8ccd6d29f4e2f93602c',
                                                'dffdc4314d3d2282ec075ce63826a73c9af30206afc86dbfc3b3f93052470a7e',
                                                '78470ca6dc3d3d805c646b611eeaaa3157801be2c2423510fd9d5af93762d8dc',
                                                [647, 648],
                                                ['649', '650']),
 ('pentecost-3', 'main', 'Postcommunion', 'all', 1): ('7d8dbb6cd3808bded8a4745efd24f7afcb347770582a2af989dbc9cd6dbbdd33',
                                                      '70abcca44c897ece1124bad2367c3e88e4fdac1ace0896cb76a31cc73eecfb74',
                                                      '458e62ad713271505a01c3e4503e40832c2132be87866376ea5b04e8bf10e6a7',
                                                      [650],
                                                      ['652']),
 ('pentecost-5', 'main', 'Secret', 'all', 1): ('84e13f797cba43e78382c389796d25b106112935f6f276b8be24dcf1708f88f2',
                                               '33370e5b27f839b525d2da86db3062e4f47a069e99bc0f5b55cc57bb214a22e9',
                                               '28ee11bd7ad5684039de1bf75d571ab213e2f39af7877d63e9aaff226020a981',
                                               [656],
                                               ['658']),
 ('pentecost-6', 'main', 'Secret', 'all', 1): ('77caa0aa55b1394d5d2a293419bc747006656d963d23ca54d7512fddfdbdf3f8',
                                               '0071e090b944864d3b350857b81508a6ff6bd670c8e6b88f481365211d441ff5',
                                               '11176a94f30ad1bb3c8b13191ea7ba5171e06a99fdd4fff041d2463acdd34a84',
                                               [660],
                                               ['662']),
 ('pentecost-7', 'main', 'Collect', 'all', 1): ('8bbae064db8252a8f4ff7e94bfacd913dd697bb3c606e831a4e8a9375cbdef4c',
                                                'dbfd5a5e9c8f29573e7c46cdf5ffda35b60976595f8c3aa0dc6c49ba955d5ab1',
                                                'd29b25fb7c94b2aea925c20f30371ae3b56ae5c30d661ef43eab72dcdd9dc27f',
                                                [661],
                                                ['663']),
 ('pentecost-7', 'main', 'Postcommunion', 'all', 1): ('1411dde30d935a15c60b6330a24fcc39da5651adff98b0799b6546619e551841',
                                                      '12a7019ad3ffeb0241d1b49021e30a289b57e5bf44846c51248405d72a05e5ec',
                                                      'cee85babbaa3427d7a03ad74554959e4288bdc5432d4cf4e3fb4cf76cd2d9be1',
                                                      [663],
                                                      ['665']),
 ('pentecost-7', 'main', 'Secret', 'all', 1): ('fb640357e91d538dafb4b90bfaf85536689d9c64de9ae9eb373934437694f4fb',
                                               '1a6cc6d92bb7dd5ce02b6f55b21e75e0f78ba206c2c4607bf24fd6f5a5ef9976',
                                               'ac5e8c78f253b3567b506de5d6cd51b183097bd1c3ed3c50e906a3573856b07a',
                                               [663],
                                               ['665']),
 ('pentecost-8', 'main', 'Collect', 'all', 1): ('fba4e19d07b09b72b1242918ae674dad2f04226680e1128d9cc494a583b04412',
                                                '421ff60a6aa91423885cb5600436d59ebe2b53248283ec1d579efccebe6c18f8',
                                                'b319bd5852d2f912bbf18159792a9d0a96141d978fb878ca7a602640b08e9443',
                                                [664],
                                                ['666']),
 ('pentecost-8', 'main', 'Postcommunion', 'all', 1): ('8f038343c882201a1e0ca174cda11283e11d96e5e1d0f9e89e62b39ba5919bbe',
                                                      'a2e17f6d09c3b7e7ab22ece3cb5e55e081c8784a09d32afee5801bc934f7f88e',
                                                      'c26dcd78cdb6006b27a60ce30e3875f71504579029f88345d4cdfa265f3c02a6',
                                                      [667],
                                                      ['669']),
 ('pentecost-8', 'main', 'Secret', 'all', 1): ('2b5a4a4cf9ae5eb7dfeaf0dfae864c0e31e89be0a8bb5d4fdaeb470553026e1f',
                                               '61be66415b591b744c62b44eca3cc0b384e8d807ae836b019d81305a074c6ed9',
                                               '9bd96425fecbbd74ddfcbc83b2215c42e1cf618d90b47d609f928f606573bc00',
                                               [666],
                                               ['668']),
 ('rogation-mass', 'main', 'Postcommunion', 'all', 1): ('2559780029bd0d8055f910eabbbed4e3953719d2c89718fe2dd94e94dfda8589',
                                                        '9f1755ab46be8f13eae66857599ffac1b83e99c502fe9dc7bf81cb32fa0cf293',
                                                        '1102bf072dc77eb02e921654187194cc0e96e668eed2238c6ecccba66ac573a9',
                                                        [579],
                                                        ['581']),
 ('s-agnetis-virginis-martyris', 'main', 'Collect', 'all', 1): ('cb1cb58df56141638598ec06195f8470e74b22ab2c7e8a37aafebf5bd4370426',
                                                                '1bf6a0664d365e70f759794da11960c5008fe6d13a96ef3d0440e143554522f9',
                                                                '2e3bfa1200549af09e2304b7a3f8f50721c64a758bf75a8f38cfbd7765b68f0e',
                                                                [879],
                                                                ['880']),
 ('s-agnetis-virginis-martyris', 'main', 'Secret', 'all', 1): ('d7c15150b9b7d6b5c44fc8e8b881c2393826f4775cdd91e02e72fd64fb58a4c9',
                                                               'bf3757f2176c584c4b0e4fb23ef143e9c07d3ce1592cc8bdd3fc248a107ce004',
                                                               '416234780a49ffeca6af9c4eac97174411c3099e7a00a5028b1e5240c24158ce',
                                                               [881],
                                                               ['882']),
 ('s-andreae-corsini-episcopi-confessoris', 'main', 'Collect', 'all', 1): ('ba671555cd58ce1235520d650196f02765c4303552c48f03f10eef31c4599c00',
                                                                           'e3fefb12a05709c2f3ddf0ac9b30cceeb92b92bbfbbfda5a41e3c53407d42b09',
                                                                           'b2e77195bf268fe81fe6e9a5a7a76cff6a991d12c27503531d0713a1b8d0653f',
                                                                           [908],
                                                                           ['909']),
 ('s-francisci-salesii-episcopi-confessoris-ecclesiae', 'main', 'Collect', 'all', 1): ('77677be2a71eea3e6996324aae8eb22ff6c90d003f6ebac0f9bfd00c9741131e',
                                                                                       '89b40e6ed7f9e126914d1e3daa1ccfbce72d77dfffeeda8c75de5b61e48c90b1',
                                                                                       'ccf196ab5c5bd34d520fc498df550211bf372e6f984a47dca9eb7e0d04f9ae8c',
                                                                                       [892],
                                                                                       ['893']),
 ('s-ignatii-episcopi-martyris', 'main', 'Collect', 'all', 1): ('ad83876a6bbb6cc0019f4350312005f38049aafbc85f9a14c92879de3df3f654',
                                                                '36c482a66db184a1462255e3b3e17ca21871764b3ea192f6f245d94499c6973c',
                                                                'ec1777100995cacfe8fa7950e79b50e7a42e89fd6b0023c06968e1f30ee56e84',
                                                                [896],
                                                                ['897']),
 ('ss-fabiani-papae-sebastiani-martyrum', 'main', 'Postcommunion', 'all', 1): ('8c77ed4df357e933dc1334afbade9077187775dd2b6e9657b727a825a18cf52c',
                                                                               '569b9f6866f5a2cec05d52b6d6b4f1455e4b3b85685509d46a552e538bc7c410',
                                                                               'aa5c6c3232569487023b934ea32f54c275bb375166301f76e5ab3d5aa47802e6',
                                                                               [879],
                                                                               ['880']),
 ('sunday-after-ascension', 'main', 'Collect', 'all', 1): ('1dfa3086c6e44ee47e263ac9a6e72470839cff2dc33d4768b07d0bfff64761c7',
                                                           'ba6988c643ab3cd6fda6933e2efa0223ff80d97842683ae241fd430eeb741383',
                                                           '36dc6e335aa60dce39b826ef74d2ec06e9a55351663bfa665a3ca28882d68e5b',
                                                           [586],
                                                           ['588']),
 ('trinity', 'main', 'Collect', 'all', 1): ('cab28fc984dfbeb39c8c9e8baac38e7d6bb066083793af52bef2aa392ec640aa',
                                            '57a84aba1f0f5b207467ab9a1d7aef637ac544ef70ac7e677cc5888077628803',
                                            '52cb33f09fc16a047e07a680b09b0286972ed8be981c9a4dcb152e1e08b4f05c',
                                            [624],
                                            ['626']),
 ('trinity', 'main', 'Postcommunion', 'all', 1): ('1c345cf1c96579df15ae406d19f7822ca697313a8529eba32fded30cd15200ef',
                                                  '12d9740fca1292f0a3664570d9487afdf17cb54bff0667381ad6e6ca4b0380e4',
                                                  '8eca048c25385d089020da96ed0b123b4b4c13cfb85619fb4f0c160b803bbef4',
                                                  [626, 627],
                                                  ['628', '629']),
 ('trinity', 'main', 'Secret', 'all', 1): ('1a19178cba24b3599544506f480034b11b2b7edd0424dc83183a9373ef2c248b',
                                           '97be42c811fd3df3c304a77bf04609e7a58c234d9772d378599a21aca97127a1',
                                           'db2a9ff56afee5e4dfc88a1207957c0ea94ed6a661b10a739ea0fb74f351ff2e',
                                           [626],
                                           ['628'])}


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def words(value):
    value = value.casefold().replace("æ", "ae").replace("œ", "oe")
    value = "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c))
    return re.findall("[a-z]+|[0-9]+", value)


class EnglishRecovery20261023Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("english_recovery_20261023_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        cls.p = module_from_spec(spec)
        sys.modules[spec.name] = cls.p
        loader.exec_module(cls.p)
        cls.doc = cls.p.load_calendar(CAL, "roman-1962")
        cls.overlay, cls.absent, cls.stale, cls.witnesses = cls.p.translation_overlay("roman-1962", CAL)
        cls.records, cls.trouble = cls.p._source_library_records(CAL)
        cls.entries = {k: r for k, r in cls.overlay.items() if r.get("publication_artifact_id") == ARTIFACT}
        cls.slots = {}
        for _, mass in cls.p.masses_of(cls.doc):
            for form, proper, taken in cls.p.appointed_propers(cls.doc, mass):
                owner = cls.p.source_slot_identity(cls.doc, mass, form, proper, taken)
                for identity, body in cls.p.coverage_slot_units(proper, owner):
                    cls.slots[identity] = body
        cls.latin = tomllib.loads(LATIN_LEDGER.read_text())["entries"]

    def test_exact_owner_set_replaces_only_genuine_absences(self):
        self.assertFalse(self.stale)
        self.assertFalse(self.trouble)
        self.assertEqual(set(self.entries), set(ORACLES))
        missing = {self.p.translation_record_identity(r, self.doc)
                   for r in tomllib.loads(LEDGER.read_text())["untranslated"]}
        self.assertFalse(set(ORACLES) & missing)
        for key, entry in self.entries.items():
            with self.subTest(target=key):
                self.assertEqual(sha(self.slots[key]["text"]), ORACLES[key][0])
                self.assertEqual(sha(entry["translations"][0]["text"]), ORACLES[key][1])

    def test_complete_source_words_and_actual_endings_match_each_target(self):
        marker = "Historical Latin transcription, layout and stress accents normalized for comparison: "
        for key, entry in self.entries.items():
            with self.subTest(target=key):
                passage = self.records[entry["passage_id"]]
                historical = passage["notes"].split(marker, 1)[1].split(" Complete checked English SHA256 ", 1)[0]
                self.assertEqual(sha(historical), ORACLES[key][2])
                self.assertEqual(words(historical), words(self.slots[key]["text"]))
                self.assertEqual(words(historical)[-2:], ["per", "dominum"])
                self.assertNotEqual(words(historical), words(historical + " nostrum"))
                self.assertNotEqual(words(historical), words(historical.replace(" ", " est ", 1)))
                self.assertEqual(passage["verified_on"], "2026-10-23")
                pages = ORACLES[key][3]
                self.assertEqual(passage["artifact_page_ranges"], [[min(pages), max(pages)]])
                self.assertEqual(entry["ia_leaf_range"], [min(pages) - 1, max(pages) - 1])
                self.assertIn("no fresh target-edition image inspection claimed", passage["notes"])

    def test_every_latin_body_retains_its_independent_publication_proof(self):
        for key in ORACLES:
            with self.subTest(target=key):
                mass = next(m for _, m in self.p.masses_of(self.doc) if m["key"] == key[0])
                rows = [r for r in self.latin if r["mass"] == key[0] and r["proper"] == key[2]
                        and r["occurrence"] == key[4] and (r["cycle"] or "all") == key[3]
                        and self.p.form_id_for_label(mass, r["form"]) == key[1]]
                self.assertEqual(len(rows), 1)
                row = rows[0]
                self.assertEqual((row["provenance_status"], row["publication_status"], row["publication_basis"]),
                                 ("collated", "permitted", "public-domain"))
                self.assertEqual(row["text_sha256"], ORACLES[key][0])
                self.assertIn(row["verification_source_id"], self.records)
                self.assertIn(row["verification_source_id"], self.entries[key]["witness_note"])

    def test_text_free_audit_replays_preservation_and_current_gap_denominator(self):
        audit_path = ROOT / "src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml"
        audit = tomllib.loads(audit_path.read_text())
        self.assertEqual(audit["record_type"], "roman-1962-english-recovery-audit")
        self.assertEqual({tuple(r["target"]) for r in audit["accepted"] if r.get("batch", "phase1") == "phase1"}, set(ORACLES))
        self.assertEqual(sum(r.get("comparison_batch", "phase1") == "phase1" for r in audit["rejected_comparisons"]), 44)
        for record in audit["input_snapshots"]:
            self.assertEqual(sha((ROOT / record["path"]).read_bytes()), record["after_sha256"])
        for record in audit["source_postimages"]:
            # THIRD_PARTY.md is the shared disclosure every stream appends to
            # (the papal sources added a section in 1277f02baf, removing no
            # line); test_lasance_artifact_rights pins this recovery's text.
            if record["path"] == "THIRD_PARTY.md":
                self.assertTrue((ROOT / record["path"]).is_file())
                continue
            self.assertEqual(sha((ROOT / record["path"]).read_bytes()), record["sha256"])
        missing = {k: b for k, b in self.slots.items() if k not in self.overlay
                   and self.p.slot_family(b.get("name")) in ("Collect", "Secret", "Postcommunion")}
        recorded = {}
        for group in audit["remaining_groups"]:
            for target in group["targets"]:
                key = tuple(target)
                self.assertNotIn(key, recorded)
                recorded[key] = group["target_latin_sha256"]
        self.assertEqual(set(recorded), set(missing))
        for key, body in missing.items():
            self.assertEqual(recorded[key], sha(body["text"]) if body.get("text") else "not-held")
        outcome = audit["outcome"]
        coverage = self.p.english_coverage(CAL, "roman-1962")
        self.assertEqual((outcome["represented_english_slots"], outcome["positive_english"], outcome["untranslated_english"]),
                         (coverage["slots"], coverage["with_english"], coverage["ledgered_untranslated"]))
        self.assertEqual(outcome["untranslated_prayer_owners"], len(missing))
        self.assertEqual(outcome["untranslated_prayer_owners_with_latin"], sum(bool(b.get("text")) for b in missing.values()))
        self.assertEqual(outcome["untranslated_prayers_without_latin"], sum(not bool(b.get("text")) for b in missing.values()))

    def test_exact_bounded_publication_bindings_and_english_negative_control(self):
        artifact = self.records[ARTIFACT]
        self.assertEqual(artifact["sha256"], ARTIFACT_SHA)
        self.assertEqual(sha((ROOT / artifact["path"]).read_bytes()), ARTIFACT_SHA)
        self.assertEqual(artifact["rights_status"], "public-domain")
        self.assertEqual(artifact["rights_jurisdiction"], "United States")
        for key, entry in self.entries.items():
            with self.subTest(target=key):
                self.p.validate_translation_publication_binding(entry, CAL, LEDGER, self.witnesses)
                changed = copy.deepcopy(entry)
                changed["translations"][0]["text"] += " Amen."
                with self.assertRaisesRegex(ValueError, "translation body differs from its exact publication passage"):
                    self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)


if __name__ == "__main__":
    unittest.main()
