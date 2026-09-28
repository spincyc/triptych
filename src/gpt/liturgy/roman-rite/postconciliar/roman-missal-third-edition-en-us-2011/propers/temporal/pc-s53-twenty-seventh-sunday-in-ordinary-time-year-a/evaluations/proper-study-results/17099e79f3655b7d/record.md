# Actual engine results

Workflow `proper-study` v7; run `17099e79f3655b7d`; final disposition **ACCEPTED**.
Workflow digest `9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38`; original seed commit `264879369f1710eb0600a74836cedc62abd1ff28`.
Provider `gpt`; requested date `2026-10-04`; audience `adult parish assembly`.

[The production archive](../../../../../../../../../../../../workflows/reviews/gpt-pc-s53-production-2026-09-28/README.md) retains every exact recorded packet/result, intervention and checkpoint, including the two failed cold reviews and their repairs. Its terminal checkpoint preserves exact seed manifest/bootstrap, final state and event stream with a hash manifest. These files do not certify an external approval or deployment.

| Terminal command output | SHA-256 |
| --- | --- |
| `terminal-status.json` | `5ab16734cddcf68f5ad0eedd76fe3a989c0bd2fa1bc1e7d1acca36981c824f23` |
| `terminal-replay.json` | `a93fbf294c26f92d285a066ae4907624fb14d44b98b26b416ae61c53f79ada63` |

| Stage | Iteration | Disposition | Packet SHA-256 | Result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `3bfbc3dd013b07a4648714a3f672635d6af43af4a136f93f1e08ec843fb35eb3` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `729dae49b6badb26a8923a729d0e184333d7cde063385aea6d419c8a23cadb80` | `48fe325962cd3855b8dda01aecbc7ca2569f57108257981ef97f5b185d1b0163` |
| research | 0 | PASS | `5c635b54723e8ce129c0a0cae1489bff92666340e04bb6eb6596af5fa9ec3ef5` | `c2413ccdf70db57317342bfe5eedaaefd37ebe4f4bcb648d11a59fae41b03362` |
| research-preflight | 0 | PASS | `a8619a2091e644002fd527e8c27989958114f94f1ad56e7367f13a7a34baeccd` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `ea9dff5ad208639b2bb11c6c44ce81a9c4537cf97d825ffd908039af25b2e1c9` | `7626a2b1c0c6201e03fa0a560d0f14ca751ac2daf18db171347a30596f2ade6c` |
| research | 1 | PASS | `8ed566b165d2f5cdd3c99df0b9b7b2e06524fe7b89d6881c86c9c98cd08f118e` | `3666e15c3b86b0c1544ee8e2850ed9ce60f6673b7799eaa7e0409121821457a4` |
| research-preflight | 1 | PASS | `a5b2d9ad4ea3a8259ba70063fea6380b5838e13d0e42133842972febfd02058b` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `0a2f3c2e95152c635affe76d8bfca6818e97204b0edd2e28f5cf387488bd228f` | `e6581f94fce856375b782255e7d8fe8ebff2157f3a1f80700e4531ccba258b9e` |
| author-study | 0 | PASS | `75db4102956180ff3c19a9d6cdab126c9840b1bd2fb98b8b9ef265e5845cf6f4` | `1e156f34ec6dd239ec66335b3d24e9b5fae2e187d3249baa6c2c50627fb0c3b9` |
| study-preflight | 0 | PASS | `5900ad4d5c4bd138f30af7f02128bfe2aebff79fa5ea3cfa6a2e4eeeeba91bf3` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | PASS | `fb22299a560b0c888aca51b7e1e47dd61f003007a7d32cbdb140f3d2f45a36c0` | `401537c1d76e3cd8f47d9f14f003fe489b33b362d2ce2bcba9899ff01e6dffc9` |
| derive-synthesis | 0 | PASS | `6a0ad17bdc89ca23cf82abc87ceb7f152375c0aaac586800db0f831c3d121d34` | `8ac417a35ebb679cd3dfd48fadc1574353a63f7efff4e04d4d472defb90cfdad` |
| synthesis-preflight | 0 | PASS | `073239bcfe350fb96a5c6fcea60587f28f4b2bc19e85726d88f58bd6e06a61aa` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `adebb47d4de7d039b8f2963b03845dd2bb3eb4250841858a9737fd24d21dc7ae` | `c3aaf099614c01e50f722895e3791cfe210b6fb6bbbd09af463b3a00054ddd5d` |
| derive-homily | 0 | PASS | `29ca920be4862d43c52fe7b60f01728e17f0fb8fde0d1bcc2bfd0630b7427396` | `ef70333377d4b2ea2ea40e841da3efc6cd2b77288d1ed27ecb4aa0b4c55c00b6` |
| homily-preflight | 0 | PASS | `d5c1c4074e3526d107f3b22665d68cbb07d2431eb4a3ceb82415f9b1f61bf092` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `f97c3daeca7d9f01f776c59d524d0ffa7f3eeb997a447049dd84625e31a897d8` | `220a87d8f7681687808ee5d3118356e1e7a346598e38cad6a1b7c4cd91cc5e5f` |
| build-artifacts | 0 | PASS | `8c29890c12a21584dd7cf5a6f5d06adfb8be847dd9542342e11144e87984c562` | `b132a9ff63b9feacc19e1710fd5e49ff9acc7a2b47369cd00bbd7469344e31ac` |
| artifact-gates | 0 | PASS | `48de6b6038d4e30e5b6961274b6f3dd32da274cb178c763e15c46a079d1f936d` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `cd00fc64b729832e5615cbf9b011210d6fcae0685b11a4bcce18325278662f06` | `c5c012bc87911de937591a22366e7c69e7aeec0bf83b8061fa2c15d5ae6d8a2d` |
| generate-web | 0 | PASS | `d82d1382d28f4f59591bce90d34e1c2434f4e48a906639f9167ff26d525cfb57` | `8fcc71ee1ad1a66294c3f83864acabe84c0e681b38885255143e048326a936a6` |
| web-review | 0 | CHANGES_REQUIRED | `75c0053e103f4b9a86504f95dc97769bc063cb7dd71a63391eb12408533303e6` | `ff27adea5f74d071182ea5612b3f5a935d9c015cb00b04bf853bffb64cca7f46` |
| generate-web | 1 | PASS | `6b45caa056571258d6a26ea087224d2281441225516e2ae3df91e7368106fc3c` | `5162f8eba931a3404c21762e8ef369ddda82175ad57f111ce26c8a2a18d0b499` |
| web-review | 1 | PASS | `c1311536df08c297d7ed7a2df9fb91f1f18c6f1aa4e9929714a8215ceda8f239` | `998b81558e86d3e36970a9c95b7ac4c7160e4dd5ba86d95c33ef1693e0aa551d` |
| install-publication | 0 | PASS | `e4615ad06152056a9f6945c55d29efcc3941f1b9f29c0d3923b50ed563e4d7c4` | `7e7d49daf4641200040661b3948ce9d623a6ffc2991163c7d21783f6dc2a5e9e` |
| publication-gates | 0 | PASS | `50bb1ccd111de9c7874e926286bde8a96dcf5f5c0940ae7e82fa6cdf74e6819f` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

| Installed PDF | SHA-256 |
| --- | --- |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a-homily.pdf` | `b7fd7a87d99b7e7dd7c2b329b61d315854649c4860f14cfc66fd39cf6eafca97` |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a-synthesis.pdf` | `f394f3f2081808e8470d416631638c64ef2e18a7fa3d2284c28ba3f6184a1729` |
| `pdf/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a.pdf` | `57ce918f211983e2aef40cc572863f40f79fc4c0400f8bcdaa66bf2ea8a060cf` |

Canonical web `web/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a.md` has SHA-256 `7d4109999858aab4efb433b0e95df5652edee458450e75c94eb9316a6196dac9` and equals its reviewed conversion.

The final studies contain 21 and 11 physical pages; the homily has 3 pages and 1,366 spoken words, estimated at 10.9–11.9 minutes before pauses. No audible or human timing event was claimed.

The record retains advisory STU-001/SYN-CIT-001 (Durand bibliography title), accepted VIS-001 (sparse substantive terminal bibliography page), the schema-2 quota clarification, the homily coverage tool/profile tension, the stylesheet seal limitation and bounded source-access/collation limits. None is concealed by terminal acceptance. See the linked archive and research production audit for exact dispositions.

All authors and reviewers were fresh no-history Codex workers at the workflow-declared high or xhigh effort, respectively. Program gates and engine advancement were performed by the coordinator. Shared responsive-rendering remediation was handled by the coordinating root’s separate tooling lane. Exact model variant and runtime versions were not exposed beyond the recorded metadata; no additional contributor identity is inferred.
