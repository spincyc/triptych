# Actual engine results

Workflow `proper-study`, version 9, digest `ef8058d0bd73437c67569a8d24ce67dac4c273fef7688aef8a54dec9e7986b13`.
Run `0b0f756d95e3ee20`; seed commit `643a137fb493003f1d9928036b870ce96d0240e3`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-pc-s54-production-2026-10-08/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `516d3753d886256b694e189ba06da51472b0b33509d48a47d12c225e3381220d` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `f8f2925ea59d5c18c0b6594a2f1fb7dbc71067d4ceb64cb1d9b89f42bb366d92` | `79b8ece365adc3244f3bf36d78f96c48da676358e9b26883f0d81ef9e3b9cabb` |
| research | 0 | PASS | `a4046dc762b7731d18ae99f237be00a78cf980627dd0f4108602c3c919cbea33` | `86ed87ff305084d42bc4ad9271382d31ea46b1f8544cab6c01d008d9efeb0dd7` |
| research-preflight | 0 | PASS | `11b04862dbb8cc1eba2b7e4164ffbaba10f14fd9d9be6aeeb4a4937a62213526` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `a024254e51ac25eaaea83821cd59373fb278e539aa43702d3f488a08f2be67c7` | `f2e3369f15968dc8093d138b25b35d01e959fde0561b21abbad57c236364040d` |
| research | 1 | PASS | `a636963636f62855c84e2d8216396c8645e61715ddafb860e2cbff70b2753d34` | `17635adc614d2b611831afda8e049fa4a1f033fac9f9c442ab9d39cab013b242` |
| research-preflight | 1 | PASS | `ab12c4f691324e27253cacf87168a0f2d9dfe809f6d68f47ab4d8db0da1a5206` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `e3c24426d53c6a6b584935ce8fecbf3fbb9da14b24d2a00243c8aa687b55bd14` | `35e6801c2578fa02ada4fef8b55e72f8c778c2754f5e1a87638dfd3a808717e8` |
| author-study | 0 | PASS | `dd37eafbef450a09786d1341a359beae1d491a8358394ff3c0788db0e505ce30` | `8c69ad3f6c4ec8940462742ff0bdbf2d6ee32ec90709d0ee258aac7532f2617d` |
| study-preflight | 0 | PASS | `e321381cc184dab50163859e833971a3e56950fdc309127128d066e72acb206c` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `60bff78f428e1e35298a9feb08e83bce5036c1d763f98642fa2245fce4a0863a` | `5552002c9cdcc3a6dd123e15cfaba17bbc99a99e634ad6952fe8cbc312e83a76` |
| author-study | 1 | PASS | `bfbaadfc1fc97b045d5f2e9a26e5516b86598270fc5b99fb4168a50c3871c8f8` | `8657e16a77a1d025b1b19c5c3712ecc4dd7e59fde041735d3759619fc9d57bc6` |
| study-preflight | 1 | PASS | `2c7161a82fd105dd05822c72a7aaaab433d87974769d1e53fad9a08f697688a0` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | CHANGES_REQUIRED | `f15646ea1b68c242dad0466b2b522aeb7b358da86dfd3d194eafeca79cedeb6d` | `f91df3e4325df74ab96f94183c58c85c09d2de2de39c0aa028924bb13ba7d7cd` |
| author-study | 2 | PASS | `41cbd1e4372f7b5f6054da8eda21be3ef7b74ef3ee17edd6cbdec708231e6d8b` | `6c0a808c856219dcbfb723cd03430a9b19b1587fdd2fef98349f54426503e5fa` |
| study-preflight | 2 | PASS | `7701111be8b68fc5989f24819dc1d45a469ed4c0aa68f523b403d8b7bf364416` | `fa1f37edf322caf9a8086d37c76932f39c21fd61b9e8cb561d319d286391c9bd` |
| study-review | 2 | PASS | `8667d542e68949c690b1cda912c7ee3c73bff8c55cde07dba60987de18f99d64` | `cfdc4e74159fe0e1d134646cff8ac711df7c3be085687371bfc37afb3db3325d` |
| derive-synthesis | 0 | PASS | `7fcff8b0195c9eafc6989c50b55963ee018a6d6b5b3ad890c7de45c62943e7e3` | `8ff9d2f149b2e6b94f75986a223f802a900b87cde7bed8b5f6e711e1af422465` |
| synthesis-preflight | 0 | PASS | `e152bba49230d7319bc01e5a6b8d151c5d07df172a3ee0bd5761b9c2f6a88646` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | CHANGES_REQUIRED | `7e706952ee72dac72908b99c7962130b57a20cf6852a9bfdf18755c936a4e38c` | `100c73d793d081490c1479b025bdaf1f7a8c7b9d83c9b6ba1dd803ae19c80f26` |
| derive-synthesis | 1 | PASS | `36e6189e559acfd46b99afebb20039f1d85111c153a089b5a60451f97171b20e` | `15a84bff03ef4ec654110bd7e4d5d079e12eb2b39480cbd6353ac4e376d4fa90` |
| synthesis-preflight | 1 | PASS | `b7babc5ac76e6df4a8f62dc895911682452148953055532980aec7f79c87347d` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | CHANGES_REQUIRED | `e3f6d73f7e6da3811cedb3176fd480d3275835fd0e305e2d09c00cd1bc42d32f` | `9ef4ba4ae06bb49de6b0b0ec20b4829509c47bbcc396c3e5dc422c96d0ae40b9` |
| derive-synthesis | 2 | PASS | `2079e49ece6eac5eec8c0056f8dca8b3935be32d2d9e5d6ecb8191c623ea4f60` | `53f9059fe9a41e65b6a8256c2eb8ad209a60d271de67ddc62f048bc6dce209ef` |
| synthesis-preflight | 2 | PASS | `d4865b4bbce5e467627ba71afd9df7204a2809c94b17ac29f2022960026714c0` | `42a2ff6eb1fbf1e3588bd868fb35cdfcf87527144fff18ceffdfdb4cefa15e04` |
| synthesis-review | 2 | PASS | `45d57cb60565009a5580e609d33566ba9293e1fb455b1b917f9a1ce628a4c521` | `3e1402d386ded7d5322b30f20c1a84f2fbadee88cef6c9149a5c189071f8dee7` |
| derive-homily | 0 | PASS | `12aadfb54cc9af6d670b0a5b201289157ede7037c3707fb34c0e3e9a5c4a0f7d` | `24bc0c01d180cac2ff0a3f7e436c976903cf207e0af2c574b22faffe730d234c` |
| homily-preflight | 0 | PASS | `bbda72938eb049cf0626afbdf325e4516338301661796272be0fcc8e366f4bae` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | CHANGES_REQUIRED | `50bcca1758c3f11f9458c8055f27521cd7f0f5e51c9bb6c48dd20ae07a8e95a3` | `6f6db038df81f9799f9a19c93872d32a18e4454d36514e283e618d21232d5afd` |
| derive-homily | 1 | PASS | `90ca6e9ea25966af14aa05259dd695cc2fa5f6d43b98d9d857dca6354a7ec602` | `ed06631e1e0a69aeae4a09d682d5d94b06b5e8a65ac60054c1b2f8057c651421` |
| homily-preflight | 1 | PASS | `82aa69198ed504727035fe031a6289e9b1efca10bbe161e28b870fc09a2e55c9` | `dd64e18d636bf105c5b251444195d128462ca7f80ffb809f123598fc42bea5de` |
| homily-review | 1 | PASS | `b708f0b27823200ce074db3729d63092e466d697574ff7994e17f3143b085890` | `1f6da0bfe5a5fd08b62529223dcf7b710235377f0b27dde9412a8869714b99fd` |
| build-artifacts | 0 | PASS | `884c1e103bb0aab190e7444fe5a185db34be959a90f3722ad2c0b945cd9f2845` | `50d169f3c785413b6a7fad1f44ace368e27ea6966c08101e7802dc9a47b8c3d5` |
| artifact-gates | 0 | PASS | `5efacd12cf8e2c3994900e95b850cf31c3ee9eeabe56903aab3fef9029f8e291` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | CHANGES_REQUIRED | `30563523a6566fc7d10eb1066faf119f2d0dc8c80153d447d4709d2ca91d1a9c` | `bd83406b6a14a487396e663f3dfbd3c4042aa5da0008ec5f0366036175b822ca` |
| derive-synthesis | 3 | PASS | `3d6c5ba0eaf60cfe7aca327f08150d881b3d5e8fcde7731d7616d93b510138fd` | `bbc2e769d830416a57156f6ffc2c3ec0463eb4df3d144cb05251d0989dff862f` |
| synthesis-preflight | 3 | PASS | `f941cf91ce2cffa5b9153764881c0c274041e61eeee8b5712a15e5ded64eb584` | `66d3490d62161845be2c67fe2e00298669ead41ac54a2372ab5a71dce0627b02` |
| synthesis-review | 3 | PASS | `90b687b8eb0bd43281578cec297bbe056ce9010ecdf0be62a9a606454a3d83ad` | `b4f5c394b4d9668f146acf47d426aca84b59bc1ae078f357211e626e84fbf57c` |
| derive-homily | 2 | PASS | `803d518646aff79859645aa1d1412c8efec70b1b53f9534ad4386ce99da1f34b` | `7c8ed3d562dcbacf0977279b2c4073d2ab79e3b7a7aa1ce3487efdbcf35dd40f` |
| homily-preflight | 2 | PASS | `777d555ca9ee4c0dc58e5bf2d12af49f3044a64a9f2666101ae55fccbce844d4` | `23f1c17e63456e714c79689645f3e2206f31fb96e970e1fd50342e8360141942` |
| homily-review | 2 | PASS | `1bff4ae588571a15d892eb271c4317017e4d43b7ca070215014bd03748474508` | `55bbbeef3740e80c524090f4cb884148bde3bf296f6654b9416af8da749a591c` |
| build-artifacts | 1 | PASS | `62f961a2dffa3684e85c8c572aa9fcca80132fe36fc899ce5e0cc14b3cf486cf` | `b2cd6c6e2fe26d2a9e242f0848b736aedbe69b6dd6b69be214609d3fd9312917` |
| artifact-gates | 1 | PASS | `1d9b464fd51632c7b4b0a34a1d86e7c7e43a3ec6a83098ded90ce0f452ca15aa` | `8d6a7c139b783c8489d67a5012f7cc8e3099b15e615f90603c523961611646cd` |
| visual-review | 1 | PASS | `680746b7e733ac1cc9472343e77c1dcd22b710018a9d201c03833f1ff1705b24` | `f6430ae3b6dbc69b34eaa5a162e1c85e90ce367fa590535710fa337796663a98` |
| generate-web | 0 | PASS | `d716c8f868fd7e672f71e8a349e698b2524e9b2fccbe63ab175b3dc8fcf11feb` | `33b25cb082d84a049b835cdb713446551d4782945080db5a84694d9d0b7124e3` |
| web-review | 0 | PASS | `3b176abecca7e85f3e595cac5d0eea385629971d5e1c9821ab905a1f1eac3470` | `28cca685aa74b3c9b836452843c8abd6e52b58bd1781899d36356fc43082e634` |
| install-publication | 0 | PASS | `2d614321a342b57d0ea7e76fc709f4a606ba25534b69a8095badbe785845b7f0` | `b9854be78838e0500d290e69a4d565b946eded5fad6eb046582afc0f5fd59b1e` |
| publication-gates | 0 | PASS | `6da1a9f0f9b49c5fcc6ee53d8fcb6041a66910853e4fecd4b536822230021164` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 48 results over 48 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 4 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
