# Actual engine results

Workflow `proper-study`, version 11, digest `17f12ad495885888db9045416b60df5bc828dccdf9f1eab5a1edb648cc280964`.
Run `4d16b5e19d25dad9`; seed commit `fd99f7289aeb120b0a598e053dd292593a2f6576`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-pc-s55-production-2026-10-16/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `68c4f78b1baf943f9666aaee027f4553f630210ccbf93f3b8f03fb178c002aa2` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `439f8a657e1d67cf15b2bca9c01ede150fd447977bf3d8c99f54cdae5d8072b1` | `13a0fba6c36dbf94e42e87e8a28616c4d4d285b73b70a1d515d074c34cc95ef8` |
| research | 0 | PASS | `3a7381d6fc3516dbf61386ea75956d14961816695f5cf0d8d2ea6da2d5ad725d` | `fe210f000ea537fdd4a4f7338f26dccf5d227e6a5eee74b557c28ea0b5e4e915` |
| research-preflight | 0 | PASS | `bf5dd3be6a598bca6887843191d33ce240fc2a05e954c03cf783cd40a334c6d8` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `07a1bdd976cd55a4b217cb5c26d67ec526a411a1f5c6c7607dd6731cad180a3e` | `e4f8e2c01ac8ebd62e8841a7cf7132bd39e84497db2f8e91e4fe441abf4d8a04` |
| research | 1 | PASS | `0d3b6ecf296dfe26bdd78fb7d2c0f1a648b0e8da5ce719fe380e5f61be23f37d` | `9bafa7fce790d460bc6183d20180a79ca37924314fd67945ff028113ac96a6eb` |
| research-preflight | 1 | PASS | `62705bc63ecbcafc11d2b983dd3f9d2e6c881287519963ace74ddc6ddb2647a1` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | CHANGES_REQUIRED | `6f508e866e0494a6c358a39d0280809b5bdc15d13726b8cc9abf334bef93c543` | `eaffe5544eb998dbd2100c624d643ce11630cf2f8cf01fe379817a46e942762e` |
| research | 2 | PASS | `b683a78ddd19e9fdec2bf8591f25e1d6ee68f5c0a6e4512292ada54ca191dc90` | `60eca829ec9c7b7a64f8f19bc948350759d02634ba52702902e02f5bb6e535c3` |
| research-preflight | 2 | PASS | `7e88ab67746d771b73f70fcfdb3ef16c0cf9427c63d375d6e0fff703eafe95be` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `28b6bfc90a852c6643edc7b2809f01574b207fe12a713889ada7dcef5ae2c255` | `6fd0720f1c23dbcf7526c098cc342ae68ebc6d9c80a770cdc13dfe9e7294b76c` |
| author-study | 0 | PASS | `4d1f4e91c7bf6692a81e09e57444556ddde6d7b74bfbd9e8d8fcfa737d6b3211` | `8d4499863224ed2ab516e585f11d07e50244365b88b6a6cf468e2e7bc0cc6b64` |
| study-preflight | 0 | PASS | `17aeb43d568d3b447f0b857b38f0f7bc4cb53ef07de7c9becda05162c9739d6a` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `45890e41ba631ae84d61c9b83a5df66350140f622f6269d2df808061295fc0fb` | `8ce94b1420b3679937efe7560549c9f7287f22ed4be7835dbbb7b67adc6fddc0` |
| author-study | 1 | PASS | `33c8e597d9c9c5e8dde9575d4c60c37fef1becc9e7676e1ccb7a683cc46f9d65` | `cc54f65754e62c132723b96207a5a224f5b9df305fa4d30373adac1d1f3836c8` |
| study-preflight | 1 | PASS | `3c41490b891ffae77dedf4a915f7939ca5f3d3a1e0d9c433af2110a042c80b07` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `4d4e2361acae8b60b3e842f47aa1199413652c6d5a555c996df60fc08d839ccc` | `70a36d08421a624c1b00a837f72e18a10f04869f079dd36a45ef84dec881fe96` |
| derive-synthesis | 0 | PASS | `6adf8235348410cdf2e204c9175b518cfa84594b1c9cc7441cf4622d34987aa2` | `4dbbd720c1e64f253f47278c6a2d19a6d45979cc5e470caadf93bf59f3221ba1` |
| synthesis-preflight | 0 | PASS | `1ebba42fb202ec2a064696ba9065fad072f07f1bf4301f51e07e752fbd535c6d` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | CHANGES_REQUIRED | `65b505f399e33b6ac7c085f04c522b0427da70e84f77014eadf4d42e2f259165` | `21318a5d25e36493e9b945de1f62743b2fab3500ab20ca8d4dacd61d26126dc4` |
| derive-synthesis | 1 | PASS | `65a270dc147a99199ea5251841eb0a79ec1bc307d4aa7a86691da1b38533e79f` | `a0fccb976607b37f2cbe29e85f33d6599f0237b2ccfdf3e339d8022a30c7c64c` |
| synthesis-preflight | 1 | PASS | `d456b5ebef8664280035ac83f0ca3a5255a38913339187cef3b94912ba0be66b` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `2cdaeef8c5228c47a5655c88ba23e74d83a510e83857967da013633ece5e8920` | `38d4811c9b8f7285036589bfb92bd77d7bc868d2aad2a0ba4d29a31846452241` |
| derive-homily | 0 | PASS | `c0b6e159c9a161014ac1c395bf7960e2ccad7eca96f56db63976ab62dade2978` | `97ec3a6112f560281eac2e5cd169756d894310832d85fe6b3bd6dc3ebf8a154c` |
| homily-preflight | 0 | PASS | `d7303a888c2f19d3df25d17f07d45ac745e6491352a534d05c473132c8ce9ab5` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `51667ad26d29deb0799f144c7039eefcfe84e87b31433cb49dfbe574b8f5d243` | `c0c843296b6b79aeff9f4aac138508fa2c485a0eb0559354ec28431952c501ce` |
| build-artifacts | 0 | PASS | `e58b67ab4bb3ed942edcaba6bf6125819334efeb50efb37bebcc32299831e432` | `5ca12f2f66d69514453cd9169d67668f0986bea15ec69be5f21ea3eef5288f93` |
| artifact-gates | 0 | PASS | `6970cbfa0e3c96c2bf879d1e24dafd62835bb5ceedc2cbe2d28a18935fd850c3` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `66e99f8c49b63b09c2dca2089c868c38dd3ac3868dbd2d2dedece615ac0b6c71` | `67aca0b0c5c594ff18288cbd26d3e537476c4e50302fed04ac6ee3aec16f00a2` |
| generate-web | 0 | PASS | `88dddecc7f32ff471ad7ca034c05c3e5a4bb1abe2f94ddeff42551aaa7fdb7cb` | `016d6f6bde1fb0bd00d25ec9d0f2cd1688f97e45a83a930af53363a6b48d8181` |
| web-review | 0 | PASS | `b543e826c072cfe52ceaf23a78088ced7c8911287c0ad17779ca0ad9cefebdd4` | `6bd376cd3700541af7a0f42e5814d56d75d2e70a7fe211188c6bed737f89fc11` |
| install-publication | 0 | PASS | `08682c2cc86e6cf6b57567db10b432aa022440156a5da56a772e81366da99f04` | `d529ad08659848a5473a70fb75b7d6206028359fc0e8606155e66c15bf02821f` |
| publication-gates | 0 | PASS | `bb0cb25eddbb7dbfe8f83fafe2c0e9b9051f6163608dda858a2924f5821fe700` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 33 results over 33 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 1 manual intervention this run recorded. It is unencoded workflow debt, not an acceptance.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
