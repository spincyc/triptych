# Actual engine results

| Identity | Value |
| --- | --- |
| Workflow | `proper-study` v6 |
| Workflow digest | `a965af881c1e4110b6e4698001b4f06b9a688a93a1f1652c292d15002afe1768` |
| Run | `bbe114e132356b38` |
| Seed commit | `30c7baebd99056e4faac09a0f13cb085f9de1ea7` |
| Proper | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a` |
| Provider | `gpt` |
| Date / audience | `2026-09-20` / `adult parish assembly` |

The manifest and bootstrap retain their exact seed bytes and identity. The state is the exact terminal engine state. Result JSON files at this directory's root and packet text under `packets/` are exact engine-retained bytes. This run recorded no interventions.

| Engine record | SHA-256 |
| --- | --- |
| `seed-manifest.json` | `1fad0e4593035d83753ef72478de6c0bffc3772864e960c5a1cb11eb2ff867e3` |
| `seed-bootstrap.json` | `8875025913ee441ea6917908dc9516a424bfca00c24da1303ae7054bfc2bc101` |
| `terminal-state.json` | `4a5952b49f2e1c760c6fa63a6f6633b7599b91c210f2214459ec05babeebd4be` |
| `terminal-status.json` | `3a728332e8465c1be1181cc5164d82adce075ff924ad2228af590c36c1cb7c04` |
| `terminal-replay.json` | `e88c841423484dc4a16b93efbf4b5ee871e58df3cf9002d2ac813b5bae17629f` |

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `860e4e74438ee3d96ab8563f3a7a428f7189be3991f8228d70dc0a361d42201a` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `54838aab3cf835af09793db09e1b0498444eb8902e25e90886a88c3a7438e16e` | `ee54ba35529b719ff05ec2d7bc11ce9121c760e956a04ef8349c9bd7ee837237` |
| research | 0 | PASS | `73be4d3a7a9c0c834e5d2a777d7e693c8125629df0f22b064630af81950fa608` | `714341e236d237901470f114b6203fe94801413119a98b198d5126a6d058e760` |
| research-preflight | 0 | PASS | `f4a59d83149e2360b7eac1d93319394963055f8e94ea4e1c1c7a717725b7a444` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `57659367c97560ab8590557f7d9244e833353e15160c28f82d17bedfa7e1df6c` | `2d5da9b34010851b25fc8947b30c6064545882428261b3b429857bb279ada5a8` |
| research | 1 | PASS | `d4203801522f31a825f95f6284182160549490facbce86be79bf1f1fb2667433` | `4b7e8886bcf3b63cc1aba481aad25ace506c745bb22b25174b98ffb2ef0930f2` |
| research-preflight | 1 | PASS | `8857d5ddcdd67f94511d8b531685c538ca81cc5ab6113275d726d4527c2ca450` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `47dd0bf7fbe85d52abb7e2147dc04c94591ffa926bd6b2620c3fd5544b09f260` | `b8460072ce6857f3e402ba99e99896afab1e04a7b54b0f15d668c9eda8be441b` |
| author-study | 0 | PASS | `c986ed15c245ac18fae235c181621a83646b68ccca1f65f01ddbbe38d6054924` | `06567787d6a84940171e0848ef1523a5b07f74fb3a68a657d439213c16d0ea0b` |
| study-preflight | 0 | PASS | `4b3a55e9ac6bfa56dc30e0538fddbee3137f784a3af6e642f3773845d0a74158` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `3a90bc2480fb09b9b0645c43189851a2c071aeca3ef34d65e571bd692944c2d1` | `933532d3a7208ab3a79d6091b20fd629d4adbce68e61036ee609241403dce911` |
| author-study | 1 | PASS | `d3cf8d44473309c619e34f8017ba06f8ffec66b4d1e5dce7608d21b8c806945a` | `52f71f9179b06634130533a5f597eb343337d847f3f8fa12f4f7addb7f37cd34` |
| study-preflight | 1 | PASS | `f594e1a5bfe75867d97bac0a243e35fbabfedae57373d05efa0177eb653dead5` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `a4c0ae433773265120512f777f1a119849f6e83149ea751c6ad56efe877b634d` | `b7a828584e0aac6c2f3de8c828360135fad95980d450648fb31e4f0f32d8df5a` |
| derive-synthesis | 0 | PASS | `d804349d786e60adb5afcc35a570bd84dd173cc025a73fb116a304fe1abff779` | `113ba8bb29d07e04e070d4712d02fece5322bf4f6db0ffd4d511ac41797dea1a` |
| synthesis-preflight | 0 | PASS | `41df927a9162a94303c04834377973d59cc648bdba922943cb1d6703b9286228` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | CHANGES_REQUIRED | `2891050ed9873ba25cae23450e7e2a0618ff685148dc05e8ed83dfb86b088c32` | `c95ffef7905b3bcb935a7f39b8b63d1b8e47b8814115b9cd65f11c1286240d38` |
| derive-synthesis | 1 | PASS | `558c95c02cc017afb8e8b482fa628c9b661ebb881bdf9aeac1faf4df3853a642` | `ac4481790ce994832f6a902659ecf9c1f7c9c0114cc824a540a19aa92cb993be` |
| synthesis-preflight | 1 | PASS | `8633daaff4e00cd2ede13d4d1c749c5d1ffe9b77f87ea07c580bfc69e6aa57fe` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `e4f5e427e610b50c37f7517fe7c96c6806e7f614104de36a2f550bd3e5fb62ee` | `b223f454a20c52b9bd7d844a3d51e56779de38d54c1cc0b42adfc1533d169282` |
| derive-homily | 0 | PASS | `ce384366aaa36941ed0bf7d5257ff4480ee8b74b174eb6efae0b7e65d34bf069` | `f82dca52725e0805c5ae5360d4d41afc933571e1fea4c5744c0ee08679492ee5` |
| homily-preflight | 0 | PASS | `eebe09cb8c3728699f88c1ef6e5cb992da6fb490a20da68b901997d93d6756e7` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `b47d0f0be3e7b6f8f561ba61c69ca56c31a1bbd0f6ed5720f057bd50a2a25042` | `af96da17cecbb2bbd3aa24be0e2e7e65f8377265864f0642e8b0c751571163d0` |
| build-artifacts | 0 | PASS | `a7726414141d156e7fa164809cb020f8f68df707422efee98bbac565177f7a64` | `825e517a4855c7317d607e1fca47d63dc773b789ba0135367e7a142b677cdb6f` |
| artifact-gates | 0 | PASS | `014edd870defda6c5c0ecef0d826a36de7b8e00b5bb9c625d116578c8082f412` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `bd4a623224ec605831ce8cff4722ef8abe82039f13f123e5b73465d0335fcc30` | `83ab2c030d0a202fbb2fa80ba9fc6782ba86abbd1a80d87c8f6a42cfc05be28a` |
| generate-web | 0 | PASS | `e5f2ea26ed01673af9aca2b2f68253ec10b99c31199573a032b2be39b0afff27` | `ec4ef3b4b8c023cb409807f3582b5f7bc284d58e2fff5f24336ead982725eebb` |
| web-review | 0 | PASS | `d191a4395a8aee4ea8d913b6d76f972bf2ecbb4b0c8b3dcc01f080cd77d727d6` | `c0c70b5d2030d3e476375e57a3fe816188f9856d34a31cbc04384210cd020199` |
| install-publication | 0 | PASS | `fcfd1a852f6a85eb0bfdd8ad89b26ac691cd78f8b2ea12f82d82eb6295e88e96` | `154bcf102a1062b3501ab8144445717a96b7751aeda397fa8da26e0c7e3084ac` |
| publication-gates | 0 | PASS | `9d43df4e9f7c567dc8121f4f7cd79775af87e99c84eb8b1cd2214022614585ab` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 30 accepted submissions and 30 packets. `terminal-status.json` and `terminal-replay.json` are exact outputs from `tools/tpt proper-study … status/replay`: status is `ACCEPTED`; replay reports `recorded_file_intact: true` and `deterministic: null` for the terminal packet-integrity check.
