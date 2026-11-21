# Actual engine results

Workflow `proper-study`, version 19, digest `73706a2ab569c88974452c4aec8fe2b7540a23ad1192efa39d574ddfbd334645`.
Run `df0ccb9ecfdea6c9`; seed commit `cdae1562964b77f5ce00c022420bfcbbe75967cd`. Terminal disposition **ACCEPTED**.

The result JSON files are explicitly declared public derivatives of the verified engine-retained bytes. The only permitted changes are removal of current-repository-root prefixes in top-level `notes` strings; removal of current-repository-root prefixes in canonical top-level `artifact_path` strings. The native run is unchanged; original and archived hashes and every changed JSON pointer/count are in `redaction-receipt.json`. All other input files remain exact. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-68-production-2026-11-16/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 | Archived result SHA-256 |
| --- | ---: | --- | --- | --- | --- |
| scope-gate | 0 | PASS | `168119066754e829730f095698953f214cd9588aa2a8f83f49945ac95629692d` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `61060ecc98c28b246fbf9faefe94d8c954de94c4136c88707f9522d62444efe6` | `63fe472db64609bc21ba9c3c68a205a8298a3845f14fe959c76a02ef4690b3f6` | `63fe472db64609bc21ba9c3c68a205a8298a3845f14fe959c76a02ef4690b3f6` |
| research | 0 | PASS | `c226811864a4add3f392a7591c723e981a4b17fb830d8b046f59b8a393f2d0c1` | `d03f66970b21488a2172ec4c25a4bdffe6fca663342633fe4b3fb5d2332c0714` | `2ee6ae703532f8ae7c5599f2e56e989deb53c99333d182d414fb173448db5d0d` |
| source-registration | 0 | PASS | `c01fb7087058818e9cb67063a3f891df69ed2ab32e5b91a59945d9fe68abfc4d` | `7fdeb53eaa64f7ec82bd930813bdb279c14033d8d9b9d954324fc401f3aec030` | `7fdeb53eaa64f7ec82bd930813bdb279c14033d8d9b9d954324fc401f3aec030` |
| research-preflight | 0 | PASS | `092087a0946c2644c0032a8c7821d2ac573242e0436bb474904f395b8a067651` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `89a7f6d16be895ad58971c61855f8c16d9d52b1e2c8be5ef3e7d0a303ccbcd67` | `8b75c9022995cbe53d08287278f92f6ac0a1e9a31e4dd607500ee4b477c7e681` | `8b75c9022995cbe53d08287278f92f6ac0a1e9a31e4dd607500ee4b477c7e681` |
| research | 1 | PASS | `acbe6b5bcea1d5577011bc369116c7a29be238e30ee61f5d76c1bf9ee69b698d` | `f1b8a14804656c60bc192b22b5cad48f3190b7a59422c61f4353d77cd98f76fe` | `f1b8a14804656c60bc192b22b5cad48f3190b7a59422c61f4353d77cd98f76fe` |
| source-registration | 1 | PASS | `9a1f880532419aab71241ce8bb9dc01527ae3f6f4ecf393f772324d702e911d8` | `b966cc8091126796c12131cd3353078f833fb8a07d18f5c1b61c3c91dbc7bd6d` | `b966cc8091126796c12131cd3353078f833fb8a07d18f5c1b61c3c91dbc7bd6d` |
| research-preflight | 1 | PASS | `df44f1da938c1c50a37f2f760d6e7429d57c04706e3eabc83f4e60cf472e8e9b` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | CHANGES_REQUIRED | `091e379d5bc2df3e8e4ea74ab1c9eb0cb6e2b4b1d00773e51e52188d8be85ed6` | `86a85177011881527f3cc3e58432776c4249d4fae24b6fe5a89c71edd4181a55` | `86a85177011881527f3cc3e58432776c4249d4fae24b6fe5a89c71edd4181a55` |
| research | 2 | PASS | `845822f6c6d2320daa5e05179c359b5209f80ae2d07b2000609c90a8f3920f68` | `5e1e204edf358a19d606f1ed91e14bd3dfe877a4aa0eab6cca387f74da86b88d` | `5e1e204edf358a19d606f1ed91e14bd3dfe877a4aa0eab6cca387f74da86b88d` |
| source-registration | 2 | PASS | `5d82e46d46caa54235c40a081f8f8f6e2fb0c6990bd2ff7d259946913974c84f` | `743526f31daa8349b0fc52d04f7ca82c51db986d63e6c201ddc7381a794a61ec` | `743526f31daa8349b0fc52d04f7ca82c51db986d63e6c201ddc7381a794a61ec` |
| research-preflight | 2 | PASS | `9d5827c5845b4250c27bbcf3520371c7a8e7e954f9d9e8e6b720adcc7d6de406` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `d49513ce8cda181eb34d3963646cf33fa27716445a0a66ff206e85907da0e7bb` | `7f09f162efd7beb4d2bcbccb3faeb3800fefcb1325db2071188b98f0d24a1816` | `7f09f162efd7beb4d2bcbccb3faeb3800fefcb1325db2071188b98f0d24a1816` |
| author-study | 0 | PASS | `8a60dc0398f504435f9198c3590a783808687aaa5da57fe7e8bb45c2d67eef28` | `7d2484b8e6c13cb1249db538e86c6a03e920c9e08b06b194de49bdc278315b40` | `7d2484b8e6c13cb1249db538e86c6a03e920c9e08b06b194de49bdc278315b40` |
| study-preflight | 0 | PASS | `ea241d53f0ca63155afb2c1e82945019003b203ed82779ac346a4e857ce61511` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `ad61cb18533f2442a2b5213e78bbbcd8204b8398ff640eb018e0ddf7a90a52a5` | `30fb28fbe18e9b71e4aac611dd3a70c3b8b6ce9af232a001d63ab50c15e67862` | `30fb28fbe18e9b71e4aac611dd3a70c3b8b6ce9af232a001d63ab50c15e67862` |
| author-study | 1 | PASS | `e7d759f7d521a7d26570066b6ad3d67990620f127866e4ed75556b1d032f6ccd` | `42c25990b32d3fbca391e16d6988f952b68502d357f161966649863d369cb776` | `42c25990b32d3fbca391e16d6988f952b68502d357f161966649863d369cb776` |
| study-preflight | 1 | PASS | `9a342476fbbbdda524845cc247eada887b7a1b1e4c1b12927e9b6bfc4ef320d5` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `a440fa23bde2c558c10dbc9abc8ba6e4ebc4dd86c779fc7569289d720cc80757` | `52c09e184a1e7da83b278339287f2b1050b1fd81a789f8927bc6f31b4bc4bdd5` | `52c09e184a1e7da83b278339287f2b1050b1fd81a789f8927bc6f31b4bc4bdd5` |
| derive-synthesis | 0 | PASS | `7c4ea9840f30d6bb7c3d633e3f9fca82f1e3cb8c6d8d6d681c39dc61d0263a3a` | `e289add481447b2e8bccc44b3d38f4ca819b50b136fe5c38a82ca4f090844c85` | `e289add481447b2e8bccc44b3d38f4ca819b50b136fe5c38a82ca4f090844c85` |
| synthesis-preflight | 0 | PASS | `4968537a468b73b4b86a133593cbf6072f06d4588951d04a335d01cb36011792` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `8ac5329a08677e16f9d157bfc8a3edd252a88eb051c6610cbe63443f0da091d7` | `b97d91dc2f68330e5e819eaea6c6cf02899b4ab1ef20a8318e80ab710f46c85a` | `b97d91dc2f68330e5e819eaea6c6cf02899b4ab1ef20a8318e80ab710f46c85a` |
| derive-homily | 0 | PASS | `af7bf0c5df6ab7669339ffde2a939fb01f1f6e507f2d36949ef48ef2f51e8486` | `bc4188a129c90575b224e474244bc6386b69b287f28c028a454a62bcbf431638` | `bc4188a129c90575b224e474244bc6386b69b287f28c028a454a62bcbf431638` |
| homily-preflight | 0 | PASS | `6df6b061b5ff5b662bfcff7b0ba880cfab17d094e5fa6b8897265eba6ea6318c` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `1c01917f357eb7fb88adb013dc2e3764bb0ed13e6807b10d82bfe3644d470012` | `d7c4cbafc7f182a51db8c2e740123e8b51662e1dcfb772532ea6261be1b02215` | `d7c4cbafc7f182a51db8c2e740123e8b51662e1dcfb772532ea6261be1b02215` |
| build-artifacts | 0 | PASS | `a99c68642d65b848ce210294444941db478b4f8951421e3ac3a06794d9ad3cfc` | `08452ed2b2f5317339cea1c4a48d4ea21a5ba6795800b60997e311c591dc0146` | `08452ed2b2f5317339cea1c4a48d4ea21a5ba6795800b60997e311c591dc0146` |
| artifact-gates | 0 | PASS | `55a9e64e5f5ee98eb2c9a7a8a7866c2383e45396ec692bffac21409922530cf2` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| generate-web | 0 | PASS | `3fd1383db316e3a8daac225e1d7201ddf0c0391056565f2139d900f8b8cad271` | `6f033b93f6c554a91877e2f56746b58edac543d10b315698d619a83d38b952f0` | `6f033b93f6c554a91877e2f56746b58edac543d10b315698d619a83d38b952f0` |
| web-review | 0 | PASS | `07bc3016904fa6749b69208788b07de4f22c9b1220cb7f74cfacbe74a6411fdf` | `48dd53955c48add30064b6505312fca377a7449dd16d34f1e464889fdb0e89d2` | `48dd53955c48add30064b6505312fca377a7449dd16d34f1e464889fdb0e89d2` |
| install-publication | 0 | PASS | `913d1d7857908ef5d204a9d61ece848653e387d0b13801743ae74fa6c74271a0` | `1d66f5ee558a202350ac9a37b36b80f5305436b3162742c962a033f16bde960f` | `1d66f5ee558a202350ac9a37b36b80f5305436b3162742c962a033f16bde960f` |
| publication-gates | 0 | PASS | `5d554057e5f49c21aa47e680cbb7e13640e9a87beaf8ac78ed5390e098acbec9` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 32 results over 32 packets, all of which are preserved verbatim under `packets/`.

The run recorded no manual intervention, so there is no `interventions/` directory.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
