# Actual engine results

| Identity | Value |
| --- | --- |
| Workflow | `proper-study` v7 |
| Workflow digest | `9c0b654d981692c0a1d4592beae5a00764180378d63ba80185d3ce7a23f5be38` |
| Run | `b686b7a44f0e35e7` |
| Seed commit | `a1320fb62298ed6b1cf10d82d252212a03a484d0` |
| Proper | `liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost` |
| Provider | `gpt` |
| Date / audience | `2026-10-04` / `adult parish assembly` |

The manifest, bootstrap, terminal state, packets and accepted submissions
retain the exact engine bytes. Status and replay are exact terminal command
outputs. No state or result was rewritten for this archive.

| Engine record | SHA-256 |
| --- | --- |
| `seed-manifest.json` | `b18ea9bdb172c757c02cf068ed6eff41c71480ab735f356b8566ee32fe16ab9d` |
| `seed-bootstrap.json` | `a24e1b6a484d38f2837fe96481f09cfb576403f21848aacf52add2afeb8afe64` |
| `terminal-state.json` | `16912d10f06f8baf76c2e515701982bb19132b380832b2629b60ae8bec5becf4` |
| `terminal-status.json` | `f07d4f97643187c20ea3e0977b37e08a7218f95a292033194a31b259251cd6b8` |
| `terminal-replay.json` | `c6493930a2f67c2f1ec0050077b801989f43a56854c4b999e58f1bcdb6a9a0d2` |

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `5a9a98b4f9d10764ea267edda6735d065fb17e0aa0778e1d794f91cba3ab88c4` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `b2291eca92b9bb75ed1c0d9d03160f147c3625ce67e7ec1154ebefbc72f1fbc2` | `8886842bbabd8b65e71107e0559e20ba3ad812f5078c1f2c9b6c158f8e8dbc77` |
| research | 0 | PASS | `0414063a2699580554e8a9ac9ba988c6c7cc75db38438a9048f0e02ccbb301d6` | `c679554afe197a5fe5e9cfa3b7b5ea5e03ad748f2025f3b48b2b134371f339e9` |
| research-preflight | 0 | PASS | `709e39bee92a5096290ef28a2193f0077aec40db8bb7ed85fa4a0b2cc49110ba` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `6a8e70771a98d99f02727ac30b9cbbe6bbf964328733371d3547f2dc51ba994e` | `a30895399a9b27f4d73fd54da1d90984371c21115c5326c8025c9b0c1053471c` |
| research | 1 | PASS | `d1aa6ed43a84786a67b76e636316681fc0955c2cff2e0cb907e107fcc1579015` | `22ca754fd32211a8edeca81781d86ee0c2b5245d02af7fcb371713f17f01fae8` |
| research-preflight | 1 | PASS | `efa697a04e1f1cc8d19b956802da89285ed24c5f9a69285b90bba47fa5e73aa7` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `c3072daf8e5eea6e5edb7c4a788fd408f29287bb03f72eec80403cbda3945224` | `e18c4fd337073fd5044c37d83b052f5f5268f8bf83a079b0c12db7541e34cf42` |
| author-study | 0 | PASS | `98b1bb2c256d990fce68ec4ca7719d34a9863944a7542aea07caf51bf0d75291` | `c280e5c18981d24bb2f73e021a44776dddf21ef03b00435cf7c3c9aa07bc4a36` |
| study-preflight | 0 | PASS | `75ec6ad854f942e73fc2a79b69ae648d8c49d2af6fb0238c5b47dd963c79a4f2` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `33be22f0d3fcb22605869c838d496493a845791fc4f9245b0b51f38957f6ec15` | `49f02a3b08d53a2264efbd275cfd905be77d03c0254bb9adaa420597269c4b9c` |
| research | 2 | PASS | `a50497fa34ba139f9729d0cdb1b1cb1a97b6d832e1eb0a7e93b2611e83e2d454` | `e251635a3a5e55c4e08315154bcb2323d69eeeb64673282ab318f72e88a69662` |
| research-preflight | 2 | PASS | `1776930fa5aa00221652358d773170cf304118104542f4b9fd03693805e7b384` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `3adf4d47e53046a40d67fd9c82cb710e544ddd812503e42d091ac4c111094d73` | `9b29713e7b0b1f0388bf65df3e720061be07524651ce868547b5085ecd5fbded` |
| author-study | 1 | PASS | `5705bb636fd0191e7b85d008fce5d703eeef88a2ded290e56b9716c394af5f24` | `9f2326667cdee37043fe79ef99dd6f6fed5d77aa7d6ef0cc4d54915c390f92e3` |
| study-preflight | 1 | PASS | `a8d2a15d576e2a2c1adc1b0c9d06759f9b989b313816e12eea5527f81b0b6214` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `a8c78e2ed48c5276c703300e292bc887abe34474784ab8a43b471d6af24f64ce` | `39f8782cd62c4d5aeed4f5dd4329ab1fda52c37b2148e922ef11e2bd36dc323d` |
| derive-synthesis | 0 | PASS | `aef7556b75665fd28bab3d958cf7a3a6ea9c37bad5e26c3752ca8d3e0a020551` | `df7e6868c945eb4e754b465a5a004468ad95225f5d3f514d4426c0f4e58a9e5a` |
| synthesis-preflight | 0 | PASS | `f9cac8da2c873c37b2fa5574a3da1a942c83147af3ff3fbf19111ede958b6dba` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `d6bc7da9df0f55a66d9364412efbd5f80712276cec2e68309a72f3d73bfe250e` | `5afa1e7e937b6a247f579a1747ab8959a5a431a9f85bcdf957e1b120e62b5716` |
| derive-homily | 0 | PASS | `b4db7dc1b4ef477e141323c45f12c6dc55e98f6bd3f6c6b8a3cc61f87ba1440e` | `7451db3dbb9fda96c16c4d4be05a7691c3ca34b7620bebd5af63afc147e2d9eb` |
| homily-preflight | 0 | PASS | `76829bae0d49d7c8ac854fa771e5bcaf2176fb1ce1393afa7b55f483f288b220` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `5da8025c482a26b3cac8c9342e8917f0473558f5a1810d92bd1c0dd6cca7bfee` | `694f210e24dd4092fb2a7dd9442c026f8779a12f741d41cb6f6d31598075126d` |
| build-artifacts | 0 | PASS | `9744d288546077fc66c2ae9357abdf8dd0a95d8772a60ac005da038c4770db77` | `700161b48e4b82589a665ae8aac2031e55981928633cdbe34f75434aaf83c9f4` |
| artifact-gates | 0 | PASS | `976aaa4e73132e918763d4b93f28126667b9508b554200f61a602081bfaa17c7` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `e23cae423a6c23bc0b312ca0662610efae5251f7e3e21618aeac497e168103e4` | `5994486404e1fce474f51f4bf7cab5df0a0d227c22c979ed59235bd5a19f0c14` |
| generate-web | 0 | PASS | `e9f6031409d819dc9f8e0575e0d1533ac92af296f6e2f5e7e9b88b150e61830b` | `073c051eada6ea50b87f2160f8cef1278b984f11f4a1a980da4dc343280d19c3` |
| web-review | 0 | PASS | `7a244ee32a566d56110e6efacd9fd56efffe945bf3abc9bd52312a999601f595` | `5bda1c866fddd87d65f1b8591bfaa989d9850a33b227e4afa1ab59b38addf2cb` |
| install-publication | 0 | PASS | `1320e02ef7eade9c9ce227e21948f1d14c8a6244ca5c4081e6011ef3aae6b57e` | `4bcdcdaffcbf603594c046fac2aeac5e46fa968fc7652b16298a118855ecaafb` |
| publication-gates | 0 | PASS | `4d9e19d49beaad6643b0bdd7881608ec854504afacc58c9695c459af16e658e3` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run retained 30 packets and 30 accepted submissions.
The terminal disposition is `ACCEPTED`. Installed artifacts and remaining
validation limits are recorded in the owning production review and
`workflows/reviews/gpt-1962-59-production-2026-09-28/CYCLES.md`.
