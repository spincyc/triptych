# Actual engine results

Workflow `proper-study`, version 9, digest `ef8058d0bd73437c67569a8d24ce67dac4c273fef7688aef8a54dec9e7986b13`.
Run `9c1136f1f8d1241c`; seed commit `1fa591a03c11d064c9f1afda6c44ccdbe7903bf2`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-1962-60-production-2026-10-07/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `3a2e03066e283330ecbec91c86724167d5d9850dba726fc94f5ae1201252cdfe` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `b86be658848660df6b35f7f13ade5b06830364504f742918651d850a0e65db20` | `5383d99a90be12d717771db069e410486d8175b0a0b06ce3454c17d9d2250b68` |
| research | 0 | PASS | `3bf568d2954c542d78fb8dfab4952f78fbdf48f355ad229333e05c5727aa7644` | `942bc40aa4422fd325d8e4fffdae7e9d62d0aaa400b74c1c0d05c098b87cdac4` |
| research-preflight | 0 | PASS | `c10ab8ae051b33ed8aa02d8cfeb6b3f4c6c38eb901f5c7c25e8290e9faccff72` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `83a9009a660a3d2bded0d04fff41eb6cc131cb7f1576f5e0ce0359d3d2f59d71` | `5119b846bc24df2b6c71cf972a716b4f6a69a30324a7d2b0ff7684eb1addce91` |
| research | 1 | PASS | `8df14e9dd02aca48a7a42b35199ecb8a471270a6081b988b90a0847c00c7d950` | `97bbedefe28e71caf37b098a7fea77e99ae3768e5c63f772cb732bbd78a497a3` |
| research-preflight | 1 | PASS | `ddcce55e12fc7b3ae167d6dce1a5cdd45e2dbc3b475dccb8b74e1fa6ff30dd51` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `369f24161ed03d32ebc7e2f93f36efd7044db50d8b55067d7707b1f578337b6b` | `8e79120144c7f0186357568cac62698a5fbbe427ad484c9f9dc14040a8a36b84` |
| author-study | 0 | PASS | `3be6b29e9cfe019030f765a9f161bca0b1be093bbf0a2f954dd74a16313386be` | `f6c5f8e1e232b05b8db45c3f08a75386b1ecd548278a24ffaad1e47b6e0e9f6e` |
| study-preflight | 0 | PASS | `ce410e3522e886d51a467073aab63be278e27d02d3ea634e3681019fcfe3bccd` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `479c6e54dccd9fb6b557a2b854c24edd1b69f7a5868040500d8bee7af0aa8a4a` | `6bb124a064b34c7faad13d7ab4aec9563325b1d70167a314b5ddd29a7adabb19` |
| author-study | 1 | PASS | `0ad0a126605b6eb82c33c3a2828a8418a4a062d5b73186c62ddde0c6706f875c` | `86e9ae99ff1ff4a9cf25e0cab7e5ad1498b4638599678f4a3522b87dfe2de134` |
| study-preflight | 1 | PASS | `6652e6d0dd5203a6b263c17784636a01be07c200b0d6d7e843fa30becc2d243e` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `f4876316f8ab3dc9253ac449779a5fbdbf69cc479d19bf06a10d347bf82bf440` | `24c2896ce189432fc99a58da06fdc2b1e6fc738d8aa2508cfd58784f1986b187` |
| derive-synthesis | 0 | PASS | `bffe2767a59d1232c958ccf70f82c1c0d2271e3fad402d1ff9a4ad2873671435` | `1d519d8bc19ffcdaa0221ebc5bf8322876ed56ebdcf1010145de8c58ae8cdee0` |
| synthesis-preflight | 0 | PASS | `6f9555606566344842281a7aa57755accaaee856441defb2225acdb299394be6` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | CHANGES_REQUIRED | `d317d8c2e6b36130d48b0165ecb24eddd759bcd131e8cccc7e4a3be4dd787815` | `c22173750b38ae7fa879606c42cd75c0d2576670414a967c428acb025c51b123` |
| derive-synthesis | 1 | PASS | `79db0a59d56ccda4ff2c4488b7f2c9a95de2054a64a12a65ce93d5c676e275d2` | `964abf03af1b6b122ad6ec84bc2522b73c6bbb4cbf6b04de1e39d7f0cdfab506` |
| synthesis-preflight | 1 | PASS | `d6e1f1bfb7987cf07bf139e7f913e2f47b09870ef7461140e02b439fe5dfbe22` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `54e1b38bf00750c670177c0fb69df059fbd4f0e2147ceced82272cf249b9e425` | `1e83b78de979f60999551743742c58b5eb3584c2ca5f7b17277b1499a6d70873` |
| derive-homily | 0 | PASS | `b9c319af8e1f8b1655ad2dd16a6f1a378ab11681909b5148031ce36a06c1d7d2` | `3834b6554934facf2dc55855ea36f20d5431136b8006437cd0fd4256f238e071` |
| homily-preflight | 0 | PASS | `9605727a96b67d6e3a63038aa2a4e45e8adc745a6049c2bad2636c8acf4d1ded` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `be9eedc52c35d79a728dac0a41f4e87375014422dd18328a2db53afbcf9e7900` | `5274320b7dc07994feda1f976223cc450859844f69e98c6ee1bdb71078592254` |
| build-artifacts | 0 | PASS | `89334c794a059845af95b967f1e60fbfda9ded8883b9fa8f1af9a6d8568553af` | `49e90dd654e06a26790a6eebcbce9d785ac98e03a94c83fb36ca6d1f792a3110` |
| artifact-gates | 0 | PASS | `f333bda02409c9a719251dc5db1b776e45c76f34262851a53befbf0057cdd996` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `c4c74e807fd6ab0ba36952a5a53223ed9eb98c5ab511b20fe974724f8a75bfc5` | `c8719f1c46c40896ff644366520791e5d5a0b3626de8f30aaffc413cb7b89c52` |
| generate-web | 0 | PASS | `5877e77c1d704c997e05fb13782499af0564d1b319875e8aeb6024b36df0d6b7` | `9cae2815c3fa6b2e9999a35a69b2e1e2a1e85678163eb3df456c630170505ec5` |
| web-review | 0 | PASS | `03997d9bfd27be80b3e96671dcab835fa1f8c652756ab49f3505f685e2766121` | `43fd4357cc003e128fa0713c451f1c151dd1a0d2707d1c468e49b5d823278c42` |
| install-publication | 0 | PASS | `75889ce6d7d60a00b64aba16e578439afd27313e8a6c36dbc499380a789eaea4` | `2778801edd6f80f7641c73326f94661a48d7854fd5706a798f6b85003ade91e1` |
| publication-gates | 0 | PASS | `0e418a115533f07dbbeb6042eadccf6ef35abe1260dd5ed698d9fa120e8351fc` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 30 results over 30 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 1 manual intervention this run recorded. It is unencoded workflow debt, not an acceptance.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
