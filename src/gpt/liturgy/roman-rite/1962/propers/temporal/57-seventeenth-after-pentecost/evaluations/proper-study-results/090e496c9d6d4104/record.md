# Actual engine results

| Identity | Value |
| --- | --- |
| Workflow | `proper-study` v6 |
| Workflow digest | `a965af881c1e4110b6e4698001b4f06b9a688a93a1f1652c292d15002afe1768` |
| Run | `090e496c9d6d4104` |
| Seed commit | `30c7baebd99056e4faac09a0f13cb085f9de1ea7` |
| Proper | `liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost` |
| Provider | `gpt` |
| Date / audience | `2026-09-20` / `adult parish assembly` |

The manifest and bootstrap retain their exact seed bytes and identity. The state is the exact terminal engine state. Result JSON files at this directory's root and packet text under `packets/` are exact engine-retained bytes. This run recorded no interventions.

| Engine record | SHA-256 |
| --- | --- |
| `seed-manifest.json` | `2a66e72db3d627e72044067b6996bfefa512fa417e4dc3e4f88bbf9c3b76e1c3` |
| `seed-bootstrap.json` | `f6cfcbc4966c66b8eb6b3fec250162e1dace548c5f373c21c13ff6b67afdf6cd` |
| `terminal-state.json` | `c3e7853ba091004eb4ce1489eaa770f2555045678f85dfa78b1579f7c3a39c6d` |
| `terminal-status.json` | `c91f0c25df670c3c0b5ea524fe0f338844c87326c969a215fd76b0657defa3a9` |
| `terminal-replay.json` | `5a79b216b886456c0668198788ed9d965ea2d9eabef8fe63d49aefbae6e03358` |

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `a7ad584540f2c9cb86e42f2788b8066b0fe3f9283d55cb9ef454e89a731c90c9` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `e7ad9f7e71614532ba2cff5dedbaebef85533fef6b071e3361772bdb0d15aef5` | `6c68360ff12a66b9d075adedf9a9ca1b990a81b0e03b99bbcd7b12b90176045c` |
| research | 0 | PASS | `edc294a953e6a9e04d185aa83496755e752174ed331cb944a2445ed78623d5a2` | `1bfc4278bf39868c3f59e96498218fbbd882dae6a5df39498a72094cb0b476e2` |
| research-preflight | 0 | PASS | `071a02d06c4a13f3c106191d5bcbe4d29c5b36f97eff7037068fe2a909d18194` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | PASS | `8266716fca4110bd3d4152e4860871123bd88a78ef270574819286f5fc7126a8` | `29da6c6707e41c5fdcd020e2f806486f63da26bcacd7ed4c1216b7ed825e728d` |
| author-study | 0 | PASS | `bf2d9ccd784e481575029417fc57ae361f138e717e40f45f6b48eec2936827d7` | `2d3e31064ccb6864b577d43a3ef2750882a55776b3369cef8fc6467c92cfefbb` |
| study-preflight | 0 | PASS | `16fe47dd139f82146306b8a1c54b07f81657b1f4d1183c1672517eb77aea8d1d` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | PASS | `f703f7e87825990ca40dec4bc0b179da4c3fe1250019250dd6f4346c2b9e6805` | `30db1c919673791fce82e8eff790639c5c1a3991b716d1ddec1015f51bf27eef` |
| derive-synthesis | 0 | PASS | `12e566979ade1951321a39414ef193f1cfbb6b767c13bfe5b6bc97ab60805a1c` | `90c343104e8ad6a93456817ca04f0e7d38f572794dc8599d753c7bd34b662df0` |
| synthesis-preflight | 0 | PASS | `f49a4d6550c9cee9ad12e2780eada2056c25bdc897a204f9068177de7a2fb2c5` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `00214d1901c6f60ab05a5fd001b80e79f5353a4436a79cc97f990727bfcb05ae` | `6deeb131e4b7a2d938afb3cf831d611c7fe54291f453a88ba0f6ec8c59cc5416` |
| derive-homily | 0 | PASS | `7ee1ea8de625c03a21bb39bb927313a8291a32793b29418338b0f2aab117fbd5` | `bded170065bb6589b3a94c01d3a418f0434b579acfbee50bd3e02047666fb638` |
| homily-preflight | 0 | PASS | `0a155c2ec81d98cfc16141b8d2ef6a917d56221a0fb9090cfd45de04a6680acb` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `1936aa85634750f34a18dcf6d883016a06b8e65b23f2babf36c040765bd27d35` | `3a63ca19f5d65e11884d1a672c15fc89422e7f110fe338de60ae65fa95c9873a` |
| build-artifacts | 0 | PASS | `63a54c462048957560f86f036fc29095c51bcbadb2df3dc9a85cd5f831d574d0` | `99479b283fced7b05a495ec81840b5016aa0c111ddb61c1c5965ae6c50f7ae7d` |
| artifact-gates | 0 | PASS | `883db9fb47e5d1d22c1c0bb9ebc0f31cd1bc4641a2855f8619c00a07636394aa` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `bb5e346f1a9fc0e3b00f7c4e56a44663607a7952552a087d2c85e0965680c456` | `6d485938a13ea0d1b5f5d0b7ff347811c7570042c37eb9ab422c547616cfc1f2` |
| generate-web | 0 | PASS | `e7a949e4591983646e67c2a45b70c6ecb6f36e85260e67281f6e55af4b7074ce` | `15b810c52ea02f744ccd5b45749d3171414aaca7354bc7a9a2966035f9a8ac03` |
| web-review | 0 | PASS | `ac4ef86566a52941d189417ec2ed463d288f5ab8fcb9e8d6dbad79aaa65a449b` | `cfe62c40e7d6d21ec3427350f259e1a67e1e783bde0ce37cbc4fee62d80d5631` |
| install-publication | 0 | PASS | `c6bccf55fb5e5e4bf6d6ee391e60a99b9317c52cd4b612f144da8562b7e3c875` | `742bb30a950a09b16d0a9818d5dbc3b2bca1c5a63a37a7402b7425c9530bffda` |
| publication-gates | 0 | FAIL | `58862c4bc242b5aa5c89db4b8f69705371a65a2d36ab200b1978631f8bfc2795` | `48e3198be5224ac7fce6168da5bf24007c570ed35decb90880b5650bcbb6c8ea` |
| install-publication | 1 | PASS | `f4a0c154e3e8942a1e8c638fe95834561b0cf7cfcbe7e7b2e9739577bd92fd5d` | `025a897527da2339ce8a3eab2fb19d6782e390a8c1b6ad8eb26cfb9c8c8000e2` |
| publication-gates | 1 | PASS | `c365468183e1a093f8b1f8081585760a5de6091f2236a8fda9121e285017cc42` | `ce997de4ddf26681d85bd5133ef4aaeabdfe30dc81dac9bde2a3d404c28d9717` |

The run recorded 23 accepted submissions and 23 packets. `terminal-status.json` and `terminal-replay.json` are exact outputs from `tools/tpt proper-study … status/replay`: status is `ACCEPTED`; replay reports `recorded_file_intact: true` and `deterministic: null` for the terminal packet-integrity check.
