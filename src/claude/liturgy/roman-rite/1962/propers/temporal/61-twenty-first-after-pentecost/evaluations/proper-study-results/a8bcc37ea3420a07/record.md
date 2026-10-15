# Actual engine results

Workflow `proper-study`, version 11, digest `17f12ad495885888db9045416b60df5bc828dccdf9f1eab5a1edb648cc280964`.
Run `a8bcc37ea3420a07`; seed commit `cc2e968320e2416ef9049f1c6910ac281df8feb9`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-1962-61-production-2026-10-15/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `b942ad558010af1429d9ba2037f7a75e58e958adda53ed6862b156dafc3e89fe` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `b6e86391e68398cc219748ad3790bb61e0ccfb7783e4d9d6f5e9a6bff14a8eb5` | `c2107f0cc5ec153e386dc02a4a7d9cf143b935549c0c9cbe3b6793eecf4e541e` |
| research | 0 | PASS | `0eadf80a223659cf0d9cca3dfb0f553b3265a3c2325986463f785b5efb377645` | `03e1228de7836971dd361653faad9832b9d0545101bb1b34985ecfed4305be80` |
| research-preflight | 0 | PASS | `9ade0b441ef229fb0b740eee0a8f2e5a49e4cf841061edf54bf9de93bc6bfb81` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `311796cf330be08697c89b11761e20a72a605a6a4ae8e83513f9714cb312db39` | `68b8f76ac7e302f315403d1389fe872cf89176139434a06eaf0e9854384a4735` |
| research | 1 | PASS | `8029db7ccc2139e6857e8d12fc159926a726bbdc67994a26f364bc9b59dbc921` | `f2a72069ad506b17a77353b84136ddf44316918082da4c2a542e2ab53f93e42b` |
| research-preflight | 1 | PASS | `dde4e8ff5aff7855a97173f12bff7851079bd7daffd35c3d590404762dbe808b` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | CHANGES_REQUIRED | `f09ce89b88976244b0032e39f26d1e40853dec5b8948eb24efacff2ed5962fde` | `2ee319b403a171e8754253e88b09d7f46c8ae9dcfc65ad24ade07abc22ea48c7` |
| research | 2 | PASS | `35210ae97006098333acf6c70fe22861079eaf789f75d6e1a42f83f09b1d91af` | `c449398cccf7ef49801a01bb3277d43dee10cae25de5309026705be1d6a5cff1` |
| research-preflight | 2 | PASS | `b3f2caccd9761644dd23a4957b72174d440f7686fa14c2fb12378372826e7fd3` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `c56807f74c869efd483f529a06d92889e41d5d3da788d02e1cd45719c888fbdc` | `24f242eba0b439911ff4885668ff4bfdaa64d8e480c5a7c7a0dcc3f25c04bc69` |
| author-study | 0 | PASS | `cc4f52a3e2a11a738a1d85401494041c050c6384fc4fb62a59a5c4c38ad8266f` | `91362943be7e996fc7d7341ad5199e88ee5ebb608eccccc47611b537a11aaac5` |
| study-preflight | 0 | PASS | `d3fb9f86710a967b67b875cdc72734c77f49d3d09c9a8517be44e81374a4b20a` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `a7b78864961f3b4661b76a8ddbbdf148f0ad55fc701d01fbf0c6b97ae79be28e` | `0fd7d95480499ae85d468361508e15b2fab3e833ac3499ce929f59c82ebfc0fc` |
| author-study | 1 | PASS | `b7eec26711960d1581d969b0d146309607cbb7a28c6ac31ab3f15074cd7532d8` | `88cd295df087c196a51126d8cab136ea4a2f0475437e293ae4747fbcc4ebcdce` |
| study-preflight | 1 | PASS | `64d7c11f4ede34c785c65838e76282f5feb2a6ee682e50903d789435a61fb068` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | CHANGES_REQUIRED | `6adae23a9b9400553fc93f414456b224b88fb33dedcfff54d37317597bcc66da` | `6f47214013ca210b9198b686c8387a055d02b68ad8ff133b31d49cb0e57b96e9` |
| author-study | 2 | PASS | `b6e7125057449cf8da81ad780da7b017da5af5564bf6820f0d2e5f92c35e8fe2` | `28d586d2bda1a41f059b3bc1895a2be6ebaa6b384b0beddc6c03b8cb3dd9f4bd` |
| study-preflight | 2 | PASS | `0aa0873d018528458af8b1bfad354e5aaaf62dfd7c0091e5154758a5aab98245` | `fa1f37edf322caf9a8086d37c76932f39c21fd61b9e8cb561d319d286391c9bd` |
| study-review | 2 | PASS | `3f74b042a541fba558365a1a06daf252a2d9d7e48f70563b375003613ea1b47f` | `83a68f80e7d30b92bf8781727f0bad04b1628d5645c092b682bbd1b82616ef55` |
| derive-synthesis | 0 | PASS | `740b26ad5ee5f7e2e6c85a2d1c63cde2f5b38f4ffb9c68d4c527259e73f46e11` | `73ab55e227d91dffa58b4fda66315bdfd6f748f37e0104264a044d4f21546880` |
| synthesis-preflight | 0 | PASS | `013c3b6ca64694192f67caa8cddabd0aea4c1c3d8a9dd8a67eb44163e56d29d5` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `32eb9f634ec8c05d497ff8b485c4aaa99eecd9f2831b267fd283ead92902a76d` | `9cef1aed11c70ba150999999b83c509257341ef9dafa0b55bd9fb454e2e55690` |
| derive-homily | 0 | PASS | `ebd53d05b106e4e89b9148617c2e7ae309a0cc9d9009f0c950b70dbaad343fb7` | `f8230904726e7083f30513f50784799431c71ab0b29528f2145290d43bc8885d` |
| homily-preflight | 0 | PASS | `78a18917138f367aa5b511c06163e531af7fea035e17441c65070c52abf3fa3a` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | CHANGES_REQUIRED | `8b1540fb01b71f8c53b36892c4ad2a57f64f7e6e5bd401e4e15eaeb632ae8904` | `5af77a02475f4adab38d840d9499ec41c8961b4130d6ee56940ee7f6e1db86cd` |
| derive-homily | 1 | PASS | `792d1a9194643a1f1ab0f503992da356aa85885c108356b8e33527cda987da21` | `622e3c6685f612a2507168eef656823de29c3cb67f299e38b8855b1d13d03c76` |
| homily-preflight | 1 | PASS | `17ac757d88f4036c6414794342500aa38f6002f630606cb865fc1d7d88fcd4bc` | `dd64e18d636bf105c5b251444195d128462ca7f80ffb809f123598fc42bea5de` |
| homily-review | 1 | PASS | `8a3501e763d376f74637ce494d9df1ae9d8214c441cb4f4e7c10b9b5b0f9b583` | `744c2e8ea70823006b50251b3e0d8f10e34c06cbaa1969f9d71c2118f83b08f4` |
| build-artifacts | 0 | PASS | `be220513c83c1d022d63dfbc87f529e19f29c8f5917a5c11a2cfd7f0958d3d3b` | `e96456c65f788417564c6bbb2bbfe47093f2455a864037f1c7518d8f87273204` |
| artifact-gates | 0 | FAIL | `167f77fc9c3883e66857d74903c285d8bfdb5e2b427b731facc0277a2768ec4f` | `7938e62ce435340b532ec78f8ecec92817dd420196c33150e2562e794d425283` |
| research | 3 | PASS | `1781c38308f0cfcd84a06dcfb2ce97f806d5d0fe565c4b9a1e2b4a82b53fb3d6` | `cff505f05f6810399a78645c06dc9d1be1c6e14c6fd42babb3a860fecda95d0d` |
| research-preflight | 3 | PASS | `812b8d92a34b0d4da26d524406d923364e90eafae04a07f2d8e3c8cf5c745650` | `393e6dd007262b9fe6ed5110a41f98e20f390d80902c760e27d7615b35658411` |
| research-review | 3 | PASS | `037a120c40ad3fdf8e6bafebfa276a14122b94750d78d71565ea4b458707f2d4` | `afecbfb02c6dd65ad79f57f6c6a008c96ce18750da437d7d0b0088c35dde8f8f` |
| author-study | 3 | PASS | `5b94466b83edc78ae543661351d7d1dc7ef9c63c68501effd76889b47c087bdd` | `98c9bd44c83da6466a363bb138c83ede2b05bb426937a416f7ba29a2936c53fc` |
| study-preflight | 3 | PASS | `d3a20ba806d0b27a52fad0d71f2de984ce92c98def1617bb3a3ecbc77cb8197c` | `d2e347b6068fe56c569ec03f02e85d8a024348a190dcc3b30b097603c418c8b8` |
| study-review | 3 | PASS | `b107be1d099a07ef3045c200b60e48b3dd1e1d2030653f477cf67e3b615d2d65` | `b2cfcf0a512c3d37a4b51df12f12b584401e050f117337df9278dd43e07dbb12` |
| derive-synthesis | 1 | PASS | `3434b310a86c06c16ea159671c05ec065a43699f58dfb004f7dde4eaacbe5a51` | `9dd88a7cf1152e7a8592d96ddcc34c476513955e598e2b58305993ac71101a61` |
| synthesis-preflight | 1 | PASS | `b7f02f8744bb79d911cfcdf037430b4f6e1abb236f41ec155f2eeeb7a2429d52` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `39f0a5ca19334397efc3714905624dbb6c55c4afadca442e70f48e5e866e62f5` | `b11d8dab67343909a689cf5b38f472ebb00528978f42acaec535aa29b1636db0` |
| derive-homily | 2 | PASS | `c0197b53fc2f56ed0760364499ccf5100bc24ea599d8553c6a53ababf5df72f4` | `24345b65587c7da158083ab62af573546aebbfeabb53c78019892271e7f9bdad` |
| homily-preflight | 2 | PASS | `f2374bad4b310039b31c694c5a78479e130263b07fa280e93154b204c2338aeb` | `23f1c17e63456e714c79689645f3e2206f31fb96e970e1fd50342e8360141942` |
| homily-review | 2 | PASS | `f66c22227aecf84fa27312cb32d5169c3b59ed7f8330eadc47af54955ab98857` | `9857b8fb6cf8ae6991ae09e420838d7197f9f166734fdea6a69925db5a686432` |
| build-artifacts | 1 | PASS | `28fb63f66bd89dc50a5f3f1973fef00e5b158dfc8b3ebf2e166f79b146d09478` | `7d856aaf56ba2d62ace8f715ce3d050a6c4f81cca23cc94016fc67703bdf3f07` |
| artifact-gates | 1 | PASS | `65186e4f84d7c410efcd6055ddbfdadee35c1a59d63db66583e0fec190980592` | `8d6a7c139b783c8489d67a5012f7cc8e3099b15e615f90603c523961611646cd` |
| visual-review | 0 | CHANGES_REQUIRED | `b8bddbcab9861389a8da6e86f2bed14177c7f10ff14df3560699bc80a0271d41` | `c699feb2867db24fc632439a7b93fc407750c40f40e6740a62786212ee257fbf` |
| derive-synthesis | 2 | PASS | `3955459e79247e5aba433ce3bd51a8b42cfaaff3d5dc57e3a6d1ad3a40125655` | `80840230a491a5e373e4c9b9dd7a2846859b6180675d498bfae7f43d588842d4` |
| synthesis-preflight | 2 | PASS | `64e8cbe9bb43ff0b5642fb3bc139d6be149a5c283045c5c600db62b93f608b5b` | `42a2ff6eb1fbf1e3588bd868fb35cdfcf87527144fff18ceffdfdb4cefa15e04` |
| synthesis-review | 2 | PASS | `7ac8d01eca77c8ac3bf70ef640129a5116873a8b1bab38c60c4fd4eb9827de59` | `7a5405d0788263eb032d80fb7a287a62c034a54fa0f4ce272b02b3b3f2599204` |
| derive-homily | 3 | PASS | `14e7882086b74fb41946e341e9d8e24e5125c5d6c3ad412cb96fc058190e11be` | `70df39cad03fe67c74378afb12b372d56c36a3cd50233728849b77ddb219fec7` |
| homily-preflight | 3 | PASS | `fe943e6ade6f0f20230324b73533b7ab23bbd98da2bf33a525f25ebbfceaecab` | `dc2361ae4eb46c773241ec094095528c61ac1ac30c6c9dacff0e6231a3c3e576` |
| homily-review | 3 | PASS | `546fa1782aac27653cc715735c87ee87cb9adb9bd45ceedbf1f76529eca930da` | `ff117ab120e91145693efa536803570bd7d3822eb89cdb09ce259ed5842462e4` |
| build-artifacts | 2 | PASS | `bbe60cb7707caba2e5e8af55d7201fa2c63fae719dbe9efa75aeda6538ec866d` | `e985a2b51c61bbbf3720ffc9f75840662152a2a2e9af580a88d1698a962f6970` |
| artifact-gates | 2 | PASS | `e15f90ee7db8283933356508436c34b4c4af717e528f4ce392392f964fcac1e3` | `7981c4f2602b3b78a96c2e69320a92b1c660b9f5343e34f6f357f208e80283b5` |
| visual-review | 1 | PASS | `485c5075e2fc51124f0cf21a9e6f9a70d6d1ed9107a6d90c3d5ee6384ec24a17` | `e743adc8c7dd3c3bf02712378d56706ce202c9ad41865ece3e994c09de6d5590` |
| generate-web | 0 | PASS | `b2880ea0189417541340bf77ae6684909255663b60d6a92bc2f2fd6e5dfd5a7b` | `8026cdf87f3f5443361f5220219d8f1cc9e8feaf30b8f7800964db68043dc1cf` |
| web-review | 0 | PASS | `1e7a45c08eeb997e47302a7b0cd398717fa7206210b9e969e7a4f9968a485cad` | `ea5b344927dfe5432db84c2867911c92d066441fe85ed0a039623b93f1ddd78c` |
| install-publication | 0 | PASS | `438986a6473a5c0431bcfd261e5a1085e598a85c16a640d61bb081e40b9de8c5` | `1cdc5d4356653f249386f404e603e9bacfa164426a9b1654d7e06ea48426a468` |
| publication-gates | 0 | PASS | `1c5d6d2e3cf4037d930a3156b9c9c4dabb4718540ba91206d3502e411527ed44` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 59 results over 59 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 2 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
