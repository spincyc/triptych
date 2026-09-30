# Actual engine results

Workflow `proper-study`, version 7, digest `9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
Run `a27462e34ec9c09a`; seed commit `56d8c30f24bd0e42234c88c7d71c801981a9f2f9`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-1962-59-production-2026-09-30/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `29ecaecd73e6c9045353dc3ddde86111de4721f7b9473cc20fe399cafe4e2904` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `abdf83bcb1b987533499d9a28b667f232b981dc9f142951d6a3d350b7fa62700` | `b24729481d17c96a93f0477f6810f45b88ea4c46d5b7ec2a22beeb98d63e3495` |
| research | 0 | PASS | `4a327b1df4b2fa3b8c66a633e8fcb470ae3ad7d01fba16fdd5ed4aaba93010c1` | `49d27652d710d2b69c3a7a2334a0365c1bf758c03c92f8c4c1b6c6cdbd374a7c` |
| research-preflight | 0 | PASS | `91b5a3a7e84197c35c10756d655c79905d37dc94a503c786c48621f7d5cb95af` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `97a85d7932ec55e1eb1942ab86aff5ee8e50565694d3ceab9d11850a6b7a3fd5` | `530d7337173681acd7644b04e2fa36bf048100325a54d93cc722787f6f87fa70` |
| research | 1 | PASS | `71c9f6c793c7b163ee608c415acf8dfb49c8302086950075591b06f7aa76aff0` | `23d1817978fd621e9587f16d369319f1337cfd4cdfeb559ca4c896fa07c78084` |
| research-preflight | 1 | PASS | `b604bf6e6604215acf3721e336e2210bdcc0b6f2bda7438efb584cdf73f227b3` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | CHANGES_REQUIRED | `6f07e0cfaee39dfea4959e6bd34394398749efe97668323b7936f37accf48a0e` | `505e484be54eee4ac62c06a362bce638022fbb4d2b86c5f0b2545e6399b3583b` |
| research | 2 | PASS | `77f9b3e25e04f6aeba92971072f12376c36baea86916a9d8b13a5377ef1ee426` | `b3a85cb244b515958bf03fe2c92da04bedcd2ca65f696167b0da53a28cf3a4cb` |
| research-preflight | 2 | PASS | `894b7860bc5e4acc1df5004c8fdc6f1c5d09562bd34e7a9e9a055590044608bb` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `cb3556c1e8c3db991abcca6ce5006f265e2d3bbc290af04386164d2b2443eb98` | `0b8a2cf6599ffb90bc64d1af705d9d5c9b3564d4a9d7a88e10383cd962df716d` |
| author-study | 0 | PASS | `db110e7753025a9de23e0875fbee2ae431ab9153597e5da06de38b08a9712e0e` | `cf34c1c4929c7b25b4c8279a3e5b90e1f74ffc8f1cf8f1766b8a53efea26f721` |
| study-preflight | 0 | PASS | `96b0b8d8010d5ef2774430e924a1bddda4d7cf5a91d17467cbe24361080763ec` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `d57819eb72b5282f3f6ff2b7297dbab6abbcc62b0fe9b3b308501dcd402c6cf6` | `d43b5540f56d3ddb51006bb017ea75d809dbbfef5035bc89dcf073c764754bfa` |
| author-study | 1 | PASS | `df7a7e72c5924af4cd8ae180b1293ee31a0e7307c6a59d1674fe7cc84d9c8b03` | `59aa1936d5042ea97310779ce96d3585a18258830134b9ae004b2fccb3bbed1b` |
| study-preflight | 1 | PASS | `f83fe8cc24bbd79be9c92a2c2a26dc3d4a2d88edbe98ff409c98febd4c728dea` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `c70ddedd1c2b551eac784de18f1fb4bcfb425fe9b6de96b53735c39c243820fa` | `86c641bb440a946faf545b9f4c2020ef811ee1c3df16148c1e2b1dcf7887878d` |
| derive-synthesis | 0 | PASS | `796b5eb773a74287dcc27f09b7f5bee585259a4919515773f7b4bce19d130810` | `c3f626e07abe0400130f890e2b1b67e0815e9304076948a4c6ec488a1cd3be2c` |
| synthesis-preflight | 0 | PASS | `f6cee7fcab716905d094dd54a8af54e7d0406d9fa2e9c06f5d4bed5cf9aa17ab` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `3ddcb2150969e7806c3cf24f9cb08745e5de9a6a049b9db1eeb51ef107deaa0e` | `6f3d6358ef9ab958e3ad5199357a485fb43dd9a8d2b7c26d73cb8950af47e173` |
| derive-homily | 0 | PASS | `49dea9aeb5e45bd8aca9b32e86fa5449fee979e71a0a5698363ba7707c7ce8c4` | `8577b1c4635bb4dd26ce9533162ae1070c2f86e9d4de9a1c34a0a905bb9b06e2` |
| homily-preflight | 0 | PASS | `51eb62f8589e14c7622b634514a4cc312fdeecfde9e52d48a4722cd411326e24` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `182964a4d1fcd01b5d23f8b022620f2f1a8b72764fe6eb2ea0d7f4557e6daa99` | `73a466212a349c6eea41fbb5026234eeeab8bf6397d09d3da46e2be1d4854efe` |
| build-artifacts | 0 | PASS | `ac84a1484c837048f28866eee661a55a3b68cd2dd5cb35c68f1b40e8d5e4258d` | `77702d40610c2a6506a50b1f3e272edfee499a12efba1ee09ac51ba7734989a6` |
| artifact-gates | 0 | PASS | `4c74b17c6bda653dfd7336a41cb65a3457165ee9196667016bdbd509b81fd5cb` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `a441936f2696e2f27f340bce0ab4b20fd9b87e6937572d3a743c95ade85a0409` | `2a50ceafe601b1213ec339cfcf345c57c625761ab5621a3b82994994adf85ab5` |
| generate-web | 0 | PASS | `a7684a4e1b9941d7b0253d0e37b924d12846efae54cbe9cc5e4075bb95f2466f` | `4d9b2bc045672aca9203a8f2c380bf7c2589684c0a14232fa9e290b612f34f16` |
| web-review | 0 | PASS | `334dd9ad320623d066f11004675c6900ef099f626d9e1434048fc355d86a0e9d` | `861205d0d0dce2b343e527634737e3dd768338c47daef0acc01b72b5813032c7` |
| install-publication | 0 | PASS | `6f5e177b4f9c41491bdc07d02052c646e48228e0fcf8c2177b7e8e75dc7e5a18` | `5a2a9573bb3804ca5efb3703294924fd15d73dfb98a09053efebe1dfbba68a45` |
| publication-gates | 0 | PASS | `bd0a68621a6304dad4b25f57e7a78a8e0db4bfe6e42808259502cfebf2b7fda9` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 30 results over 30 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 2 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
