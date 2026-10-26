# Actual engine results

Workflow `proper-study`, version 15, digest `4218c6138a9943b56536f7736897e8aece682852d8a205a5454ab0d09ee52d83`.
Run `fb0417d471635250`; seed commit `24c1b7ce1781f79937f57b66c221b0ed82e219d9`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-all-saints-production-2026-10-25/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `11afeb0eb793fb98e4de8c90bc6335e3d0bbd9ea250ab4975b54b0fb66b2825e` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `97725821b05cbe012077e2206bd9aa32b03fc51acf9be8111044c955b1d01963` | `9cef828b7d5cb14fe911f79f6691a2af3815aebbac0f3a4f60ed2ca9b44d13db` |
| research | 0 | PASS | `e4e42e23c9a9cdd2bdae94398cc2e7644f3a528108ed0ba64d9e98aea59f7d64` | `3b6b7e0e68b8ee13b0caf1b6042737ecdf3a5c9ae0b5e8a0562f5b92a14fb586` |
| source-registration | 0 | PASS | `7e609bfa775db80c9f155fc6325cc9cee11ce80840ed32f13e7aeb5c1d048e29` | `78c661f113fbfa0aeea7e8e114279888588e3e18c23a93a78bfaeaf656df7a8b` |
| research-preflight | 0 | PASS | `21d4fdbf6937529e73d4182eeb6edb08eea87adc051fb810b3c47b99078ef2be` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | PASS | `053663e7fd72d8ed5ed66ab4c51c527f9c3b05363dab976563897925e96d8404` | `81781b5341455b26679c3031cbc64f6c8f7533e333a1e17c61cc0db3dd944447` |
| author-study | 0 | PASS | `1aca5d8f90591bc1b7cf29ea5d9089e40b4836970af4a9f48a60adb869849c69` | `44761c9f1c6b215a98b147056626464cdb83528067c515135170a4b9092866f6` |
| study-preflight | 0 | PASS | `99adf4db8d1495e6fa9f286188a805dbfb46b1465afed54f8d0279324d68a898` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `060689d832f9357b1d7ef9b3af72b8e778f0e1bc6e8a8ffe5c2a7277bb26626d` | `6e4a32920210182c5d50807a8f0242ab1e537f26e084ad40f443816faa159da3` |
| author-study | 1 | PASS | `dae34cebc0f4e53c823ad2f7bf4f167f13b08a25bf662ecea76135521ec8dbb0` | `7ad5ea8f8755a3e75c039cccfcb6a15a040d05c266a21a4a321793b740dbe45b` |
| study-preflight | 1 | PASS | `9232219cac24bae4ffb97b0fddcb2bcf8094779ce3def6f67cbd226d116e5b4a` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `c69bf76a078969e1502ef66b52026da5fc11a26b1797516816b7e38250d99993` | `69f2ebb0270247830cbae4d0f0a8816cd3597a44f7fb70b6f99587fc15c60b17` |
| derive-synthesis | 0 | PASS | `2a30cba9f2244cef4c3cd0c9d9b0b2f20181bb170ada96bac25bf259bb13402f` | `316b64fe4cecd5fe4b83b23690a7f42b9c707d7ea1022188b6ab5b637fb94d63` |
| synthesis-preflight | 0 | PASS | `f91b9707d41a6f29fef8d2e1dfa3921ba3d6ded23ee1b5a16d90c64e791a0901` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `3b0328010a68cf6cd73952d4352b23904e8e42f22dd49a8b588dbfe6e023a52f` | `74d8f71027e48bd12aa8501cecade9ec70210ea92a84036afa7712a956fa2d24` |
| derive-homily | 0 | PASS | `0fbbade2899eb8eb0dda019be2a895069c7f9646dae2c871368a280fde31d70d` | `243bcde467d1a1f5461bcdd249cd6387599bf95c40e505784e7ddbba6a6eb67e` |
| homily-preflight | 0 | PASS | `7c3ec487ce84064b78208d6a7cbc56785da8b513da7f4bee1c1544444d4d897c` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `e6f13b1969bd97ef575e02a9d461db2886c4d2b3a70f98548fff0b29e57a2a27` | `0e6fae0b142c68526e9a902ef9bfdd20d0857b61f60cefc5dc444691374a0f22` |
| build-artifacts | 0 | PASS | `13c18eacc9a501aea127cd3256e37c5ee3cd752ed245cc0a466377dff93d7bdd` | `dab5c015c627d37aa31d4f606a6db5187c5882720b405d0a9620b2446d056de4` |
| artifact-gates | 0 | PASS | `f6c85fc49ad72fe3942dfafd243f3875b31ec269cf572585c5b85824af824d87` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `c92f928a41f101af44b00544ebfae5be6f5dfcad9751cd4f42a0083189fe7fde` | `1a79bb707de52aa5798fe3b0a544fbe474559b6ae8556a2b5d447cc543899df7` |
| generate-web | 0 | PASS | `d42db767012445b5ddae029bba939860ef8db5ab4ee7a2daa864e020490d0e65` | `fa5d9e51b489ec7f57b0f4874d182e4c1d79f0415bef5267fcef741ed7a7c29f` |
| web-review | 0 | PASS | `5e9025609378e231e3d9fbc5d1305480fc242bb545afc84a08f5be0a94da2437` | `5890f4cc3ab9ffb58034ef67fa40ab43b35546ff3fec9dabc2c404ead93f8302` |
| install-publication | 0 | PASS | `36a9eae593c3f0a4bb25979d771b731fd6063150663eb68d53604e97b9624184` | `525603c95aa134ad8ae1971d9b145035135229e11f9cd6579206703948355394` |
| publication-gates | 0 | PASS | `14c585d8c7b0cd7140eb37b3449ce8c1eb9d82b967b697d0fbfd918b479827ac` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 25 results over 25 packets, all of which are preserved verbatim under `packets/`.

The run recorded no manual intervention, so there is no `interventions/` directory.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
