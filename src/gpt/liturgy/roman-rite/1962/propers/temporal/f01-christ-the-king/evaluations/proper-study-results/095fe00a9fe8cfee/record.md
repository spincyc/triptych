# Actual engine results

Workflow `proper-study`, version 13, digest `7568a7728ef8a16e5a7c65475e9a3ae0d24c695caab6faa5d0c0c7ec52621d16`.
Run `095fe00a9fe8cfee`; seed commit `5b48292320cc04c0f174b6bb96ce1342c554d8a1`. Terminal disposition **ACCEPTED**.

The JSON files are exact engine-retained result bytes, copied after the run reached its terminal disposition. A stage's PASS records only its own completed work; publication acceptance is the terminal gate's. The engine supplies any `review_inputs` seal; workers do not author it. The interventions are the driver's records of host facts the packets do not carry, and the driver's account of every cycle is in `workflows/reviews/gpt-1962-f01-production-2026-10-19/CYCLES.md`.

| Stage | Iteration | Disposition | Packet SHA-256 | Accepted result SHA-256 |
| --- | ---: | --- | --- | --- |
| scope-gate | 0 | PASS | `da1f92438e682126d078390b4722d2dbd2359911742d970aef60adfe0532b18a` | `c2c5dc73384dcaa82e6a0b0b6d655a49fd9f0d8345607513add762f6826c4e2d` |
| resolve-context | 0 | PASS | `68f059dc25ef629694a5ae88578a460a7f33f0bc9b693b3a976eb203cc9093be` | `3efee1d28661cc13806aed2cdc2c9aa1e2ac6e4070810cfd51fd547572e4676f` |
| research | 0 | PASS | `f057979a433ab1de6294056de774b7cbd46bd41d67dcdafe607698c52f155db6` | `49f584c7fb6d28d951d41f8b0b339c8e4f3f4bf23eea792f53f30a2ae7ade49b` |
| research-preflight | 0 | PASS | `651d4e267d3881a5f503f6cb1206beb2cc1e342391a7eaa5a4755a810319df4b` | `d9c4c5d71ce61eb0186e720a8b7c42807d1ab40d1053516f4841a9f45c9468f1` |
| research-review | 0 | CHANGES_REQUIRED | `9d5a85ead21f8d557a0b2dd5cf741fd34f44b6e58b7d8ca3e124917b785cd10f` | `bd890fabed93240d44493859898d9638e2bc052ea91c4d61ef2362fc626d161c` |
| research | 1 | PASS | `dd3a93802d02021ac2094a19cd60f59601452e6d0c6c3285d312191afc459812` | `e614b73dfe829f53dbe7135007b739d12ef4c81f40c93a6efbb9e9afe04de8a9` |
| research-preflight | 1 | PASS | `0cf4bfa6f79827f825a752868ea5ca4887d0b513ff47fb442c41d951cc65560e` | `3d41e3743c4cd6ecf837fcb791516f7a053ba74c59eeb7aa7a2100847f40b2c9` |
| research-review | 1 | PASS | `a54b0412fb348b2f8b45d775644b370a9d2c08893e6369dac09d834d9c514c3b` | `934e17bf23151a16731422e634b00af86dfbd90b8221bb27aa0b4ff4c85762e9` |
| author-study | 0 | PASS | `dd52e172d2f7fa2d7d015014f5f63604dc118733dbb014141d2ffa35182c184f` | `e1cd66df2b16bf9d95bbddd43b18c8e1738663ba457db6fa536f63e1664923fe` |
| study-preflight | 0 | PASS | `b026687ee337ab57701c946f9a21616995e590db04943851d148521e2904cf8e` | `db4f430efb6baf21bb53a26e3ace3bc17674c5b6c4e65d8af259ee8366a0f0ae` |
| study-review | 0 | PASS | `79f3e189be26f3bb677770e6a3348715fd5cd0942812508967df1a1f07b8d07d` | `850af8d808d1e41c391dbc82367f8ca94751f336ea190a83cc8e79d2a8929209` |
| derive-synthesis | 0 | PASS | `e230572c44935ef3f6b67e838f6fca88841613fb28f8bb99cb51d7bfe5366271` | `1a8f7793038585f604384d39d0a65a91daafbabef01827229aedaa324b337c77` |
| synthesis-preflight | 0 | PASS | `dab24a060eff44569ba9ebe952a2e68effddcacbd0d4eb8b080a850f545da267` | `67b87db41056e0690c03027475a5706f18334b8a627effc6e088c72dc2725ad3` |
| synthesis-review | 0 | PASS | `c153cbafc718fb4d934f8614644d9b625fb40898d742dae2984405ca3a660a48` | `a2ee7900fed153ad1b9f1cc669d52034130c440f6eccff0eee45f2b087fe3bca` |
| derive-homily | 0 | PASS | `76ca0f551634750114408f916817c0c8ce9bd215e7efd9d2c86253857a72762b` | `e998d1914b955f6337d78185466f302ea3db4f0027e2343c3d1ae6922debe2b2` |
| homily-preflight | 0 | PASS | `381fd9396e5abdbac6c1efd8e0c14a176acb969281e82f76e61f33a07af955ec` | `38c3abc374b62eb01fe47799b263dc88821ecda5d4aac8a36d1adbda83d9b628` |
| homily-review | 0 | CHANGES_REQUIRED | `7ffdd44fe044108d02d185d6cda334240a51b5ac09b39ee387941d4615c0ea31` | `8b7640cb8fc95490595ce5c9063ebce48e90b4866106039c361bc958392c2405` |
| research | 2 | PASS | `550534fe5e6c3e2941d59cfd7bae99942a3f731220065e5c794c878b163d989e` | `13e699aabc852c40ecbe33984f337b8308c75eafbbe11bc625f2a4a73d97b313` |
| research-preflight | 2 | PASS | `d4b314ecd56bb637e8e6dc4e4f5bf434eae0749f080f063a6a6296488f0193bb` | `4826841d9cf1db8e180ed8cb4eba89546e06958edef59f53b3bd0b25143da4b9` |
| research-review | 2 | PASS | `9454d05f5aaa876b1d6502a77da58aac8b8592280edaef92d8b200182be1d7cd` | `1b1242e69cd218cfdcc5aa558589c55f6a65a6eb9d95232d32af8925fe4ae5cc` |
| author-study | 1 | PASS | `c628f4429236e82a0d51a3afa470897c861285999be66b096b466b889e1f62d6` | `e27449ce15e4d40131519190edf0b1c38d7131579a1899b6e3a01346ffc923f0` |
| study-preflight | 1 | PASS | `922abc4e56797bcae55a5872196bacf22819b136ae7b81075f8a8823c40ca49a` | `64cc916498497445157cff08a5427e9162b4d673fa3d872e7e211df5c9e04202` |
| study-review | 1 | PASS | `b5c2f76225cebea61da4550b7476a82359f975bef71426e782dee73d9033e9e7` | `5a4dda1496fb92c2edc27aa05e39df05ef427a618dee4cd6805f117931471bc8` |
| derive-synthesis | 1 | PASS | `637fdf86b9af438a3326ff24e34c96889a457eba78eb889e5a1ef75813df6bbb` | `3cedb81b5a87c6ffd81a6bf160a21142dcd8ffe7f53a6148b3c526bc8e2438fc` |
| synthesis-preflight | 1 | PASS | `3c80c9f2d68b39b2038f6860927cc0220ea38db7e4a32658dffba1df41211321` | `6e1973b0386d22a673b2f14206bbd01007c3c41624ed78abd9fac4f7055f4055` |
| synthesis-review | 1 | PASS | `ce115006746221c86ab11159860545e1762346b80a08836dad016f0104020569` | `217c5b70ae8efb9491f25de8c558d33dcf135a2982616fde263eb7bae481d726` |
| derive-homily | 1 | PASS | `077f7e03a42d37e3f6d918d0d21e60f03c59eaf8bcb8b2d0aae54ebe55ddbaf2` | `2ec78e49f653f071b3353ebdb9e9e4b900dcef564ce0c3738b54ac7dad59939c` |
| homily-preflight | 1 | PASS | `2fb4e6d9e5991d3400006875422df95ddabd217abcedbbe95ee59a9cb723ce48` | `dd64e18d636bf105c5b251444195d128462ca7f80ffb809f123598fc42bea5de` |
| homily-review | 1 | PASS | `cc118d2f2c047dd13da47396ff846ea21700d619f41f2d9735ddebd89dcceba9` | `e4ee910a20401f1bcd14465cc96b2c51017beb6fc41278389b5a103a82892956` |
| build-artifacts | 0 | PASS | `512b0a7e0a085dc42a26ad73dbebe59b867aa034095dc3ce37530c279411cfb8` | `2d433d903225e06dfdb5097a371f995359f6ba2144622b58c9a2187898a73e86` |
| artifact-gates | 0 | PASS | `18b329e2700f9cc50438debfee8892354d9600017bca523415d86cf21d314e33` | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review | 0 | PASS | `4052f8c29e7e0d0e19306903e1935e7d058fc7d5c4af0dc7212eddb8de9f6723` | `54f29d812915c1b8446a266e97f6e58949b03a7badc50829d64699845bec7473` |
| generate-web | 0 | PASS | `c3d6b906be0636d50e58c971abf03fd7b63f878fe20d46526eb913aa9312eca4` | `ceb474d71a4a463c5602c1207e070492502f6fbc96c2bdca6f7c49375387d212` |
| web-review | 0 | CHANGES_REQUIRED | `ffa4623ceaa1f414a79c17cb0750a7919be5c3c7b4358d30e212cbc62e03906d` | `b49c99d5bf9c0fa44d12ea4c99e31fae816ab03bcae7be8de24c4bf519785747` |
| author-study | 2 | PASS | `f0b5121ee3dfb36e43fecc2f314c4d9c23b6162a68949ae79b00b601b0c49494` | `b76f4fe303b0e9d14bc7376555ed62399effa247a3d00f54696ae956e89cb196` |
| study-preflight | 2 | PASS | `b1efe2ee09dd84deee6e9cffdce69f5dad674d393367c501be716b83b75a6b25` | `fa1f37edf322caf9a8086d37c76932f39c21fd61b9e8cb561d319d286391c9bd` |
| study-review | 2 | PASS | `e752d81deef02f208c77c26ffad9d9198b28c6b8c2ebf12e12020192460ee33e` | `cae28847ead12fc4adb58550c0320290df10873b7f035614b5f62bff60a02308` |
| derive-synthesis | 2 | PASS | `a0bf6fba91757928e2433e939b030caf1f3aeb79974188d7a8494a86331eb794` | `f14af2e3de3a7e91760f33e8325454b68ced25c919b340a42cc96ff7f7599529` |
| synthesis-preflight | 2 | PASS | `cb0606f4b57316c331a2ce2c036f01c3e576a6a373ca9c3c60ccc0bf673234f3` | `42a2ff6eb1fbf1e3588bd868fb35cdfcf87527144fff18ceffdfdb4cefa15e04` |
| synthesis-review | 2 | PASS | `abd218db7345cb9c7f350433542b1dd97efe073915943bc799a32c608a75ff8a` | `24a0da000173e576d87fb22391f8f59146178d2c28f3a05dc843f3b513e0c27b` |
| derive-homily | 2 | PASS | `4774832927af6019853569127251aad53b8a7d5f7bcf7484845cdb24e4dfdd66` | `805d4223954b976dfcaafb25d4573dcbb7ec87dbaba9bfc30dbbb489742cabdd` |
| homily-preflight | 2 | PASS | `d1d847a1d157e22989d155900af93495cddf34acbfc7243d072305b3d498ba01` | `23f1c17e63456e714c79689645f3e2206f31fb96e970e1fd50342e8360141942` |
| homily-review | 2 | PASS | `7a6f6bbd3351c2cb03aef720e2153e747b5f331e517ad9c8d87cc628e5a872e4` | `cd55a3d1689ede35fd48d16cbf1606bf2e5ccf47c1629a929907bb1d7cf298a3` |
| build-artifacts | 1 | PASS | `3811dd3aa4b805767c7c1ae24343669600623363ebbcbf71037232228cb8cf88` | `1256484e3b72499c3850656ecd2c00a80973f77c64597d5593b70c1bfabed506` |
| artifact-gates | 1 | PASS | `6e7b920cf7f7f34a641335fcf4e0a55b8d863372e7d0685bd7fdf01b7a381920` | `8d6a7c139b783c8489d67a5012f7cc8e3099b15e615f90603c523961611646cd` |
| visual-review | 1 | PASS | `ccd4a5587a662de34621e320ebb215bb6ddc6de9138b1034ba690620e3969592` | `76e742519829d296bcff6929085ad64ecdf6bcc3319e232743f94091258c7673` |
| generate-web | 1 | PASS | `071d923267cadb6293192acffa3670e168884a2599773dd835deb471ed6c8760` | `3db5f01613b87fb3ab642f93be944434be3b81388c347c0432c830ca99bd0377` |
| web-review | 1 | PASS | `3d439097d5d6151ee3e2220d103445d94dbb5f07b5414aa88ec80be7fb9db22b` | `48b349deb377c0c16b11f13980f9928d2db1a5c90ed9be7a50ce34274b9e8654` |
| install-publication | 0 | PASS | `8674e22459a3965f985e7ab083fa06c72f69511acd23d549c083674fa9512c7a` | `fb836024848455728932a6976924ec1f2b48eb57078c076c20c6692e8d8734c5` |
| publication-gates | 0 | PASS | `27984c38b812832e29bc2b927fe33fb0548c9582b8fff5f42032ffa6b840372a` | `87e27f47187bceefeff0205ab007611fe381e50491f82a337afa2b2f1cdd7d2a` |

The run recorded 50 results over 50 packets, all of which are preserved verbatim under `packets/`.

`interventions/` holds the 3 manual interventions this run recorded. They are unencoded workflow debt, not acceptances.

`terminal-status.json` and `terminal-replay.json` are the engine's own terminal records. A terminal replay reports `deterministic: null` by design and checks the saved packet's integrity, which it confirms.
