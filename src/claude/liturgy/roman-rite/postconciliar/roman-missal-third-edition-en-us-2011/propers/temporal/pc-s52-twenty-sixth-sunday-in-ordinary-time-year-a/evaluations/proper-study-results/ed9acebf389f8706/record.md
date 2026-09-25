# Actual engine results

Workflow `proper-study`, version 7, digest `9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`.
Run `ed9acebf389f8706`; seed commit `8f5a1fa0fec4b255f89e124503b541bba816ecf5`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-pc-s52-production-2026-09-25/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `0feea89cfd5edbd4f10c0e328127c412af6f957db9ae12629c5796f252039af7` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `10c0f623ab32cf7e39f5d97c92c850d97c9ee2e7ad31d5f812dfe1b1431d5ea5` | `1f55d821211bb898458dcea5ee24804eed3832c75bfa3a5309b28cd7a62432af` |
| research | 0 | PASS | `8da6d901ceb34f55883c15fcc5426a5bdb06a86818e13faa4959946af2ab8220` | `65e05442637798a1249716b7341bb1606a99d21108b215740ea622b52eee8325` |
| research-preflight | 0 | PASS | `1ae2d1a0cd06fb59072a135a63e0647199697ed960b6b59c5a55f0ab457169a3` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `acebcb9a224f0146a713d64c8046e6cf02aa555b84ce76f98669c8d02d9ce343` | `dc6599b0d758aab537a2f9438a17832a805c840f36c47f38c53e2fdeed9dd1fb` |
| research | 1 | PASS | `544d4a639171f0cfc041dc3be8bb5d8706e369e66dfbe61e128dbaf2d90d9c34` | `b293b2f74cafe42311bafc8d7057da47ea2e831b28b82a71f1869a13f22e0ce1` |
| research-preflight | 1 | PASS | `43ad1c91fcdd9dc59ea99ec6e9161c981907b048cc981f6f0fecb203abc7d7ed` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `5a52f20a0a14694154f009bf9a200ab0654ac9d3ce478f78fce93e094aac8664` | `d1d87b7101f53a4348866838a3777823e64de6ff1ff63767b8fc0e09c73aab3d` |
| author-study | 0 | PASS | `66ca90d1863b67b2dc4262403e2684dc7fc6eca2ae12f1050daf88043d99ea7a` | `515e53073bdde5159384ad2680aed4159f65aa367967dd5a826c604acffd1312` |
| study-preflight | 0 | PASS | `634b54db713dc83915f45fab0468b53f6ab461d5c781c6bd17ef319e823cde03` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | PASS | `12a760e0c5a2f9f500f527e3317861f3d879048c7056bd919f23482bc58d2350` | `03d0e04b9ff79aba42238c1ca8a648e6f5fcd47f807d03b285531c89ae225703` |
| derive-synthesis | 0 | PASS | `ae7398c24352d564b0df8570325e1b3fabc71771ffdfbaf44eb2d98a1f7dc165` | `c9bef062ab1f13df8e070cade1cba5bf8f4acfc4428b9c0f2da96f5f02013662` |
| synthesis-preflight | 0 | PASS | `ff2de276f99f8c112f2773e50ed31205edef4c89970dec02251edfd23aef4e80` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `413cc7c22e0c99adb59b1aa628628f19ea2f56d81fd2301cc73dfd726701bfc9` | `efb08a7c25700d2e6fac7b20ad7ebc771f6ca3fe48f1fa8c480902549fefa890` |
| derive-homily | 0 | PASS | `e8a6f23d2777c8a7f9d3132761454b3a79e72aa0266034be8bc73ed45dcf37c3` | `47b47988b88633594ce8f24a6d7b1e6f728c59e6374218f20279dac877144f29` |
| homily-preflight | 0 | PASS | `cf157b821cf3544411ea25a494f127ac919b14827b3818d3bba499837d847e41` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `342d27bf3899929489f14054bab4f6974766ff9cb68d5d0e3a11f5fcb1c1c19c` | `136e3fea4f7b52efba3cece9c37c8bffc1645875f90609cc86b9dfdcce456db0` |
| build-artifacts | 0 | PASS | `28f14d5f4f54b2f1da85ceb87e4c780687f4c728aaafcef16bdde33d103b5d65` | `1801b2f943eccff423a92a1a20f81707c64341a32abcf286ded4aa66cb8eb105` |
| artifact-gates | 0 | PASS | `4575a522bf8deb96e653311205727910ee07ddc4cd7b66535066784c22c07196` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `9e1179399580f0bc5ac236cb48640114ff3a854fbadb63570cb1db233010ee36` | `7ca132570cf6c67149c7eda3ced53e3f164afd5e932f183ad0b1e28ed9e14e32` |
| generate-web | 0 | PASS | `093aa569516ab146d18b62672ce5d4e10cf17b3df2f638e0dfbb9f460cb93281` | `5516eeb23bfd11d12cc6ce1fdb311321d48feba083c9ad05e1f7eeed9b41a92d` |
| web-review | 0 | PASS | `712589c43a44345ce6d98553b43c393cd835de0f31015af44130c87dd426252f` | `eead1dc8257fe9178e775353e17a4276719ebf9cf018083de0647e1eb7b80351` |
| install-publication | 0 | PASS | `4ca0e7e0941d68c5483b38b53a6dbc344e4163f0f171a819d29dbbf79a1b5f1a` | `1450c469052bd48f693c0510cdfcbcd92c2f05a39ff676a68a4aa429485d0fcb` |
| publication-gates | 0 | PASS | `8a272a372c51d79279b606d26ff1cfee466ebac1fc9fd24250ec24a1d1d6811d` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 24 results over 24 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 2 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
