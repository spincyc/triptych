# Actual engine results

Workflow `proper-study`, version 12, digest `e6d49782e4c62eb282fbb9ce1e18a27f1e74c81170f26533f5efea288ebf4ff5`.
Run `7397c12187517ff2`; seed commit `9b87d598b34870344f3df756982af1ff5990d993`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/claude-1962-f01-production-2026-10-19/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `a21c9f05d722d52d01e50770fca3cc252978f3a055a930d13c8b2c6cddd03d6e` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `e469d5e68aab2f54b3fb6f8b13fd96e8d3acae6613aabdd1fd81b727442ca652` | `8924f9541cbc546ac78453450bce6d18cad760951c1c18ea1364f3903ae32d99` |
| research | 0 | PASS | `d4da02a23bb838af41923bd8af29450e938f7f002d84e84696a09bce380c4815` | `7f7031f383bbca013df1f5223dfa0e1a83df30f607b4149a18b7b7838e0977e7` |
| research-preflight | 0 | PASS | `7d8c7ba785e2e792f0934316db3fc9703ca08e9ed6a681ae202146db1b2f9f0c` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `32f3ff747d105bcc907577ceac88fd5a2ae0e8e7cea7e939871c08ef4402523a` | `3515a9a6fe290d2e5839d56fdc7f3d7baf91b536d64c7374882daf5c3c1ecdc6` |
| research | 1 | PASS | `0be98c5e9479c1b70aa71317089f52d12d801183956a4c3f41c4a30bf1457492` | `e9cba2ce866614ae6f196ee4bf3dc26d8c10a9f778182132eaea94abad5883ea` |
| research-preflight | 1 | PASS | `badbde7c649be9654bb7154211a31691f24c3043ccbd1f635adb820541903082` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | CHANGES_REQUIRED | `87f52fc0110361048f4d12718628153d5e3f47dcbddb675d37060684ad1d9464` | `7ea01cd782b5384b5c3115034b46ceed43e728a742701ec50b933e3eef76076b` |
| research | 2 | PASS | `2187fef01cd7d53a09ce4c5d0909eefcd140aae1f0ea5e0503174c48e62bc5f8` | `0385bbd9372ff1918458bd8420e1b374c5f1ec381ee6b7d9559db13619c1c955` |
| research-preflight | 2 | PASS | `5690bc514699c2ac813a9fb9580ddc353c7055c1ccfbb30cdc656c67f8734957` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `32f32718c42fd3b5cb6f3e49f80495f3c419aa764ff2200b94c71fa43515cb68` | `e83c6bad128f2538b0d46f35b02c1e6068e852adaf37692139bff302d05836bb` |
| author-study | 0 | PASS | `8c2c5dde11f73d1b76e6856fa5fd5228d5895f10687868c14dbced7c25d0f868` | `01eda5df23fba927a02109691af37f606e6d2cc3ecfd57ce04b7b536fc90441e` |
| study-preflight | 0 | PASS | `2228fdd2a974427357512076ac26fbacdb478734035c788cb39a5fb399bcdc86` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | CHANGES_REQUIRED | `d82135dfda9ae221fed090bb52f3031cc07a0d77a45b605d3e2b83e4492c6c4a` | `fcafc0014797e1f3f90974410d8274e4fb1f9e0a424e1b6d1ffdc7a86f006bcb` |
| author-study | 1 | PASS | `77ea8265a4b428d861b14b7bdd6ea00f3a3b9865b9446970dd3c29e5dc6ea81c` | `a1d52e9b7ff01b07579bd60025b8059aa8f98d60109fb0f33070a83246b1f2f0` |
| study-preflight | 1 | PASS | `b218dcad524c80c9cee055635fe2bd9ca6a2a920cdbae11ef7aa4861406d6082` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `f5662321cbe9cd90ba0b186a8da4351f9b9b7bdd69a35b83a495643b58927444` | `38749986d483a0e9a118dec1316a6d32f2764a2435dc50ba42ee494c11f47f8b` |
| derive-synthesis | 0 | PASS | `d43f7cc20455a14d1f38c2fc687ce4e237436f7d725e3cf8f72468b7ac5b7c1c` | `e683ea9a2a436640140bdff10b9c56090d6919023da36ba53a19dd46ee198525` |
| synthesis-preflight | 0 | PASS | `c984a8a820884d39725fe43ba8b3756d60cbc0369a7a733cc7aa8e6cd5971d8a` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | CHANGES_REQUIRED | `88e76127ff35019b33616af8019ad6d2a7f36ebf7ae9ae0a3892709331c3162c` | `971b41120e9fd74dbd3d6899a1fe5944a2a79b2b868cc61f229668b78929a94b` |
| derive-synthesis | 1 | PASS | `e793b3890eb92f8d8dd72c9f8bff8888e00d650623150bfcb897be109a70725b` | `95197e58d253ce15c65cd1b885a8ebc461fc748265f3fd303cefebb3d153f030` |
| synthesis-preflight | 1 | PASS | `4363c833797eaf7628465b9ee7f9a57773d81f64ba249ea35c2ffebf81952c7a` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `02477796eee3aad43af7ff92e1a53bd02ff5c249deb54fe1d1337cfc70dad375` | `713cc5507ac59393f087608109a041c216e1b658ed2fdf310d47c16b855bbc03` |
| derive-homily | 0 | PASS | `7f6104d12fb1b48293826a78bfd662ad5d64539875f50f4b525b75801946e814` | `c2ee093f1e6369f4e7522ac2f0cbae015c1fbd02885aa1da0435c2427ead544e` |
| homily-preflight | 0 | PASS | `d28adca9cd49d77e84a974323f11ecc7236cdb3ec4f262392d8bbc3793f63b4e` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | PASS | `cb7ddafa1d877259d0dab68df94b183f342f1d7679b44decdc53afda7f982e76` | `5376ed1e20f58a3c0b52723e413f10ec14c82e211a0450aa5ffc0db4836407a2` |
| build-artifacts | 0 | PASS | `f272cb682b41829cf7946835e7473b426b4565a98174c1f78c67f41cbaff49cd` | `b683449883d6c539b386fdea8206217c6772fc838a0a03f789371351add11381` |
| artifact-gates | 0 | PASS | `a8d5d14564bafa578b058bec71617bc808a12351d4bc0f718a5a900a6b3cdaf7` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `6774804f54bf2cf330304ebfff59645b2fafa1d299a9db0feb59a2fdfc0bbae5` | `8581c6c79a5e7fef124aafc249163e1ac6d0b607f8248e7beefc3edbcba90a08` |
| generate-web | 0 | PASS | `d09d82076d850bae1b54a78ec744c6263269f151c5d303fdb6da4f2ff4b7a252` | `534801969f2a6ad789e6786b33b3ade25f04706a7503201d2d59f9b4f9b39899` |
| web-review | 0 | PASS | `aa36dcce876dcc263797bd3ffb83cb172fd85d0344cc06b3eb67aed11b21cd9c` | `7de96e7c398ce31779e4669b2627791afe854184db42f878f5db19f02ebbc6bf` |
| install-publication | 0 | PASS | `12d8cc94316b6388c14184c8a0a1e8d88a72c7cdb596edd7f16c6f2732626aad` | `f8a5bde3ab3a4dab212c846815cb8ea6d726597f38a764a180abb7166881f8b4` |
| publication-gates | 0 | PASS | `e304c2e0877966ada7108e1ac9bd25841e1a202449f66553d1016e5141940a44` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 33 results over 33 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 4 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
