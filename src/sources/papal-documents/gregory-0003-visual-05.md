# Gregory XVI Acta visual review — gregory-0003 lane 05

PASS: 51 assigned PDFs, 65 pages individually opened at full size; 51 PASS, 0 CHANGES_REQUIRED; zero blocking findings. All are new inspections, with zero reused pages. Prior findings: none assigned to any document in this lane.

## Scope and method

Lane 05 of batch `gregory-0003` covers 51 newly admitted Gregory XVI Acta readers (50 from volume 3, one audience rescript from volume 4), act dates 1842-01-19 to 1842-10-03, all Latin. Each page PNG listed in `assignment.json` was opened individually with the Read tool at full raster size (1700x2200, displayed 1545x2000); no contact sheet or thumbnail was used, and no new rasterization was performed. A supplementary `pdftotext` scan of every assigned PDF (kept inside the lane directory) found no `Google`/`Digitized`/`None` strings and no `ACTA, vol.` running-head furniture.

Checked on every page: title line, responsible issuer, date and Latin label against frozen metadata; headings, two-column flow, gutters, margins and glyphs (clipping, overlap, tofu, collapsed tables, stranded headings); natural source closing (dating clause, subscriptions, the edition's own notes); modern digitizer signatures; journal/volume running heads; marginal summaries fused into body sentences; raw placeholders.

This report does not authorize installation or claim that installation, deployment, historical authentication or publication has occurred.

## Evidence verification

Before/after verification: **PASS**. All 119 hashed files (receipt, frozen manifest, raster run, 51 PDFs, 65 page PNGs) matched their assignment pins before and after inspection, and the after hashes are identical to the before hashes.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/gregory-0003/receipt.json` | `577919974e1a28297556b1831218679f679e3d9ca177dfdb0e06dd61d494cdd0` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/gregory-0003/frozen-manifest.json` | `a6a2848a84eff686f984d05e2707ab592b0119dd621858fdd034a0b38dca65d0` | Before and after |
| Raster run | `.scratch/claude-review/rasters-gregory-0003/review-run.json` | `d604d73b069c67a6adfc51aa429515f56b8d1f225b32cfda61a4b4adefc4f6ec` | Before and after |
| Lane assignment | `.scratch/claude-review/gregory-0003/lane-05/assignment.json` | `93e2060f2d865fbcfbb77ee1e7fbeebbfa6bc118ccdc0a3bd8f2fa5bec24bdb2` | Scope binding |
| Observation ledger | `.scratch/claude-review/gregory-0003/lane-05/observations.jsonl` | `27cbab287855d05557efec7b454286cd090c063133316b9048c13725f341a3e3` | 65 unique page observations |
| Before verification | `.scratch/claude-review/gregory-0003/lane-05/verification-before.json` | `9b91df2d0ae23290a88a966259d9ee25dfaaa28401cae52c47dd2513a7634325` | PASS |
| After verification | `.scratch/claude-review/gregory-0003/lane-05/verification-after.json` | `9b91df2d0ae23290a88a966259d9ee25dfaaa28401cae52c47dd2513a7634325` | PASS; identical |

## PDF outcomes

| # | Source ID | Date | Issuer (metadata) | Lang | Pages | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `gregory-xvi-acta.volume-03.line-00027141` | 1842-01-19 | GREGORIUS PP. XVI. | `la` | 1 | `e2ddbe68e54cdc0868b4c95a48e24d9f0e3ef6eb28a022f43042d0a916cdd78d` | PASS |
| 1 | `gregory-xvi-acta.volume-03.line-00027232` | 1842-01-24 | ACTA GREGORII PP. XVI. | `la` | 1 | `ea624362fff96ef7eed585ed0a688b235c2b40c1cb9b2a0c324c1469f033943d` | PASS |
| 2 | `gregory-xvi-acta.volume-03.line-00027383` | 1842-01-24 | ACTA GREGORII PP. XVI. | `la` | 1 | `e1776684a23b50e75d840464fb161b4e577e6d37200b4d309bbe747c03a8e487` | PASS |
| 3 | `gregory-xvi-acta.volume-03.line-00027785.part-02` | 1842-01-27 | ACTA GREGORII PP. XVI. | `la` | 1 | `67d142be70092f5288138dc55efba17b49cb78ed8ae267d0cdf06f9326f8c024` | PASS |
| 4 | `gregory-xvi-acta.volume-03.line-00027490` | 1842-01-28 | GREGORIUS EPISCOPUS | `la` | 3 | `da4e75984770bda2654b8e2a1a114fac59a16c230ee70cd4f47ba55dba04f44e` | PASS |
| 5 | `gregory-xvi-acta.volume-03.line-00027785.part-01` | 1842-01-28 | GREGORIUS EPISCOPUS | `la` | 2 | `944bab340ed2321c8d3250b4660dbfc58668047d21547ab4191b9cfaa943e27c` | PASS |
| 6 | `gregory-xvi-acta.volume-04.line-00092886.part-02` | 1842-01-29 | Ccard. Vicarius. | `la` | 1 | `6484f45f14260381de828e09a84b599b46359d4a7733c739f3d9de8735a303f4` | PASS |
| 7 | `gregory-xvi-acta.volume-03.line-00028049` | 1842-02-06 | . GREGORIUS PP. XVI. | `la` | 1 | `5b90ec5cdfa2f95df63e1ab1caf30e9b5f3ac2dcb1e684a86f4798cd4604e122` | PASS |
| 8 | `gregory-xvi-acta.volume-03.line-00028140` | 1842-02-15 | GREGORIUS PP. XVI. | `la` | 1 | `89dcc12b05b8fba4ed1cd8516dc31850312a0ed2234110685f3b0a2857a43855` | PASS |
| 9 | `gregory-xvi-acta.volume-03.line-00028229` | 1842-02-15 | GREGORIUS PP. XVI. | `la` | 2 | `d23b2694f1628a0afe087d144dc9bdf5d371878d14a3216f6121151307300e37` | PASS |
| 10 | `gregory-xvi-acta.volume-03.line-00028370` | 1842-02-16 | GREGORIUS PP. XVI. | `la` | 2 | `798b794a7278ffcfc4ee371d6e3b8734710af468e83b1dbdc41e65d27dfa557b` | PASS |
| 11 | `gregory-xvi-acta.volume-03.line-00028540` | 1842-02-18 | GREGORIUS PP. XVI. | `la` | 1 | `6bb170dbae595be4461eecdcf0b68b22efabdbc3f4dafc15886db41aa2632098` | PASS |
| 12 | `gregory-xvi-acta.volume-03.line-00028645` | 1842-02-22 | GREGORIUS PP. XVI. | `la` | 2 | `414428727b58ff3d452b50c5f8ba6cb464d6f5399d8e965c02a6e9c19753ef2a` | PASS |
| 13 | `gregory-xvi-acta.volume-03.line-00028913` | 1842-03-01 | GREGORIUS PP. XVI. | `la` | 1 | `9b5432a9966132654521c493730cfabcacc2406bc0afcdd736a879212bfa48b8` | PASS |
| 14 | `gregory-xvi-acta.volume-03.line-00029103.part-01` | 1842-03-12 | GREGORIUS PP. XVI. | `la` | 1 | `073d8fd380daca2f13e5a9f17348f5721a610cd8031ab7d9fd2ff8374cdbfc64` | PASS |
| 15 | `gregory-xvi-acta.volume-03.line-00029103.part-02` | 1842-03-12 | GREGORIUS PP. XVI. | `la` | 1 | `74ccf40d0ae2efc3d8ba0e80917b260324f72da647d61f92a56981879f8c90f8` | PASS |
| 16 | `gregory-xvi-acta.volume-03.line-00029263` | 1842-03-18 | GREGORIUS PP. XVI. | `la` | 2 | `081e7aed825e63ef903c6124daa5abeddeda20b616a63611e70d1cf852fbe36e` | PASS |
| 17 | `gregory-xvi-acta.volume-03.line-00029416.part-01` | 1842-03-28 | GREGORIUS PP. XVI. | `la` | 1 | `3ae59abde023b315727daefbada846edd2fc8a861ce5b8ca6d136e955945fd16` | PASS |
| 18 | `gregory-xvi-acta.volume-03.line-00029416.part-02` | 1842-03-28 | GREGORIUS PP. XVI. | `la` | 1 | `ed247863d71028ae77a2dbfd5a0d557750f92254d1909f6832d5c0dc2f4af678` | PASS |
| 19 | `gregory-xvi-acta.volume-03.line-00029558.part-01` | 1842-03-28 | GREGORIUS PP. XVI. | `la` | 1 | `ab7a8a1a2c260f19b072d47292a1f11608242903f3c223592a659682ff2c6be3` | PASS |
| 20 | `gregory-xvi-acta.volume-03.line-00029558.part-02` | 1842-04-01 | GREGORIUS PP. XVI. | `la` | 2 | `6af482a17fdca2efac062104a7c4eda2d0242df1dc4043603fa66991a15a421a` | PASS |
| 21 | `gregory-xvi-acta.volume-03.line-00029777` | 1842-04-05 | GREGORIUS PP. XVI. | `la` | 2 | `279880d749d941bd9dfb10e854d963cc054c92c812403f5f650322e7415f7182` | PASS |
| 22 | `gregory-xvi-acta.volume-03.line-00029915` | 1842-04-05 | GREGORIUS PP. XVI. | `la` | 2 | `77b7d709f4f2ba5466bc18b59d6c4c822b8a3c1bdfc5812d5a9361d856ead809` | PASS |
| 23 | `gregory-xvi-acta.volume-03.line-00030087` | 1842-04-07 | GREGORIUS PP. XVI. | `la` | 1 | `7cc8d7a4d2cd83b8a3c95328f9b58bc3750ec2e82754ba0f3a4950f66291dd3c` | PASS |
| 24 | `gregory-xvi-acta.volume-03.line-00030158` | 1842-04-07 | GREGORIUS PP. XVI. | `la` | 1 | `3ca149929e643976625bfbf143127f1d98ddf8a71a2f451c4c7ab5c85ad6f8e1` | PASS |
| 25 | `gregory-xvi-acta.volume-03.line-00030246` | 1842-04-18 | GREGORIUS PP. XVI. | `la` | 1 | `93de90e5634f545c4f5455c14a5485709d1553876211b492e7d22516500ca9f2` | PASS |
| 26 | `gregory-xvi-acta.volume-03.line-00030308` | 1842-04-22 | GREGORIUS PP. XVI. | `la` | 1 | `eac6efa31ffb710a29f5701cc38870184d98d1fe26407a3821d917a54dad25ff` | PASS |
| 27 | `gregory-xvi-acta.volume-03.line-00030377` | 1842-04-23 | GREGORIUS PP. XVI. | `la` | 1 | `1b004f16444ce7c41b20bbfb478798909f184c8e3e5cdce6a891d03ac41cbe18` | PASS |
| 28 | `gregory-xvi-acta.volume-03.line-00030469.part-01` | 1842-04-23 | GREGORIUS PP. XVI. | `la` | 1 | `4ce90b6ad282dfa7b081be01e3a1cf53084a1e53a3d99ddefbc59c4b3f3aa2cd` | PASS |
| 29 | `gregory-xvi-acta.volume-03.line-00030469.part-02` | 1842-05-30 | GREGORIUS PP. XVI. | `la` | 1 | `abab2e455bffb2fef0a7aa79a5810e0f14d1b70ea7b5b4669a32776bed5187ca` | PASS |
| 30 | `gregory-xvi-acta.volume-03.line-00030613` | 1842-06-14 | GREGORIUS PP. XVI. | `la` | 1 | `652122c680f53ce847024a5b0bd5e609b8de4939b9d65335cfe533cef5e48ca4` | PASS |
| 31 | `gregory-xvi-acta.volume-03.line-00030704` | 1842-06-17 | GREGORIUS PP. XVI. | `la` | 1 | `6ec11e2b607a072480eb48c7e4d06da7d1603a1e49d6c83ffdbdb8c0ccdeb5dc` | PASS |
| 32 | `gregory-xvi-acta.volume-03.line-00030801` | 1842-06-21 | GREGORIUS PP. XVI. | `la` | 1 | `3010a9983517ccc91fb2a711e22117e73ff68862f40e3b857d9f2887315a147e` | PASS |
| 33 | `gregory-xvi-acta.volume-03.line-00030908` | 1842-06-22 | GREGORIUS PP. XVI. | `la` | 1 | `96a80de11d086948b7ba59ffe7b1b77c320a6c4aa2875e3f35fae4d266e7ae96` | PASS |
| 34 | `gregory-xvi-acta.volume-03.line-00031405` | 1842-06-28 | GREGORIUS PP. XVI. | `la` | 2 | `75339afe85c1ff0530e72ee28812a8138208d3a5fe9a2bf87829a16a067f2457` | PASS |
| 35 | `gregory-xvi-acta.volume-03.line-00031545` | 1842-06-30 | GREGORIUS PP. XVI. | `la` | 1 | `bc6851084a2a84d9a7391426e6f7d464293c89a85f6fd698b9678e30aedbeb3f` | PASS |
| 36 | `gregory-xvi-acta.volume-03.line-00031615` | 1842-07-09 | GREGORIUS PP. XVI. | `la` | 1 | `f834471aebf92aefc476ad131c0a69bc5f17c8a8b0aab337a00bbaaa2a6b5f84` | PASS |
| 37 | `gregory-xvi-acta.volume-03.line-00031752` | 1842-07-15 | GREGORIUS PP. XVI. | `la` | 1 | `a0d966e6e931ce56c700bea8b3decd524c901f917453b6234728432e0250dad7` | PASS |
| 38 | `gregory-xvi-acta.volume-03.line-00031858` | 1842-07-22 | ACTA GREGORII PP. XVI. | `la` | 1 | `4ef0f292e6b65c5c63b03dccb1fc5b74c534c3c2883ad695c9f2fd184dd14576` | PASS |
| 39 | `gregory-xvi-acta.volume-03.line-00031950` | 1842-08-06 | GREGORIUS PP. XVI. | `la` | 1 | `f94689204625c57fbc56f042d96bfb1c7f46742ebeeeb5adb021e421c0b86973` | PASS |
| 40 | `gregory-xvi-acta.volume-03.line-00032044` | 1842-08-23 | GREGORIUS PP. XVI. | `la` | 1 | `afb6967b5714182a076a1cff0c5e69ad690912e7b3870ed36b4806232a6b713a` | PASS |
| 41 | `gregory-xvi-acta.volume-03.line-00032172` | 1842-08-23 | GREGORIUS PP. XVI. | `la` | 1 | `6e13db17cf63de2065149bc404b2b1d7b8f2b8fcafbbd97123f897c6d43217f0` | PASS |
| 42 | `gregory-xvi-acta.volume-03.line-00032247` | 1842-08-23 | GREGORIUS PP. XVI. | `la` | 1 | `28882a3f895b6473a9d21888dd93e0059b3da63d81db3a6900d5993a2b68987a` | PASS |
| 43 | `gregory-xvi-acta.volume-03.line-00032341` | 1842-08-23 | GREGORIUS PP. XVI. | `la` | 1 | `99b5f211e7e113d657bafe473f0477c2e812c69b529a46c44e78b88d86e97dd1` | PASS |
| 44 | `gregory-xvi-acta.volume-03.line-00032425` | 1842-08-25 | GREGORIUS PP, XVI. | `la` | 1 | `e75b24477fcbd1b0334ba1bbf8f6c8aae466e1f13d8d834c522de7e2f1a0e047` | PASS |
| 45 | `gregory-xvi-acta.volume-03.line-00032524.part-01` | 1842-08-30 | GREGORIUS PP. XVI | `la` | 1 | `5ea0c9230f5703cca64a94fe181bacef14400b9122be08bc5f6f630746d2f733` | PASS |
| 46 | `gregory-xvi-acta.volume-03.line-00032524.part-02` | 1842-09-20 | GREGORIUS PP. XVI. | `la` | 1 | `9ae864a807641786dbbea12041fea09502054350e5311b6689f1e84ea456074f` | PASS |
| 47 | `gregory-xvi-acta.volume-03.line-00032713` | 1842-09-20 | GREGORIUS PP. XVI. | `la` | 1 | `9a1ca9ba806dbaff90a7219c8d9c1eee8f32c14fd9983b77403081a50b696739` | PASS |
| 48 | `gregory-xvi-acta.volume-03.line-00032826` | 1842-09-28 | GREGORIUS EPISCOPUS | `la` | 4 | `42f3841d4ad5ac2e8342e7ac33b4c1d9e246ed07e350ae4ac504d613508e34e5` | PASS |
| 49 | `gregory-xvi-acta.volume-03.line-00033233` | 1842-09-30 | GREGORIUS PP. XVI. | `la` | 1 | `92de33e8cc77126e398633acf2226781bb905390b08e54300490f73b748d154f` | PASS |
| 50 | `gregory-xvi-acta.volume-03.line-00033328` | 1842-10-03 | GREGORIUS PP. XVI. | `la` | 1 | `4c65fe869b90da57a00654b4ca06fa1fe9bcf57c44cd999a678e76dc56887b22` | PASS |

## Page rasters

| Source ID | Page | PNG SHA-256 | Status |
| --- | --- | --- | --- |
| `gregory-xvi-acta.volume-03.line-00027141` | 1 | `d45db1bb2e982b47042c9d493d9279fa91bfd1a2e4f743e1a2bb930975ffb592` | PASS |
| `gregory-xvi-acta.volume-03.line-00027232` | 1 | `7255768d978cea52ac0193f56a5bfa6cea3dac0b3bd9efef1925f2cd86d15870` | PASS |
| `gregory-xvi-acta.volume-03.line-00027383` | 1 | `152fe2de2f249700f11e84979b95c68f4437731f48ac66172bf95f1df456b265` | PASS |
| `gregory-xvi-acta.volume-03.line-00027785.part-02` | 1 | `feb7202f1fd6d93daf61b371b52e86a83548e7aacb80589e091e599a40236c80` | PASS |
| `gregory-xvi-acta.volume-03.line-00027490` | 1 | `e607bda23a3c672ed4f7fa25d55f4bf29053b48ac899f6c3f1809081c942e6ab` | PASS |
| `gregory-xvi-acta.volume-03.line-00027490` | 2 | `aeec10b9dfd0ad594f9c8146b5e144a88cf347e0741abd63c3a35d4f78930550` | PASS |
| `gregory-xvi-acta.volume-03.line-00027490` | 3 | `4fb885511518e81415443f05cdad303c74de0149c805ffbc941801484617dd75` | PASS |
| `gregory-xvi-acta.volume-03.line-00027785.part-01` | 1 | `0823c44b536e1db0ce31f3c6afe1f9635044e1116ba27fda068c17b7dbbc272a` | PASS |
| `gregory-xvi-acta.volume-03.line-00027785.part-01` | 2 | `65fdb2eb8ce8f496c488c738cec2044f7af340b7396c179497547204fba526d5` | PASS |
| `gregory-xvi-acta.volume-04.line-00092886.part-02` | 1 | `ef024edd1437b7daf130b7f62f8062691ef2937366e9c2d1a6c60d482d8d24d2` | PASS |
| `gregory-xvi-acta.volume-03.line-00028049` | 1 | `b42ec8aea2563022f7c17acf2f27af8626af82ba57799ec8cd3863b21ffb7d19` | PASS |
| `gregory-xvi-acta.volume-03.line-00028140` | 1 | `c6261e6b1a653917682a950cffbae43dae3eccfd129e970f8836b2d3f1f07644` | PASS |
| `gregory-xvi-acta.volume-03.line-00028229` | 1 | `23ab6ed54b44512bd830ab9b23170e18a8fa61b03b6d828a20e6e3d50dc75dcd` | PASS |
| `gregory-xvi-acta.volume-03.line-00028229` | 2 | `7812b3c4a82444c78bfb34247d65dcf56b9c928f838bdcdf99b259b05c6cbc30` | PASS |
| `gregory-xvi-acta.volume-03.line-00028370` | 1 | `f9bfbe6cc4df6b5153884f7fde77a88d678c10d57295ef44783d76e748b9055e` | PASS |
| `gregory-xvi-acta.volume-03.line-00028370` | 2 | `d8c25bc62fed58dcd57ba42bbeecfbb3c04e3e4ba110dc4e88732b4a1963371d` | PASS |
| `gregory-xvi-acta.volume-03.line-00028540` | 1 | `cfb332454b8be245124b2d3f77402f1f1a780539c53f2974d699547ed74d1768` | PASS |
| `gregory-xvi-acta.volume-03.line-00028645` | 1 | `ec7a3c97c3c9486d26e454ff3e6345ee2abef37e1cc9a510f5b99c11aabe514c` | PASS |
| `gregory-xvi-acta.volume-03.line-00028645` | 2 | `3d444ef3f65d5fe8b1a9e5c5aa3fbe95940b9df9cfeaa0b3df44c4b5c4f20a0a` | PASS |
| `gregory-xvi-acta.volume-03.line-00028913` | 1 | `c626556e576a173504a760b077a6c0a780a64066e8ff892a7a83592e292a15e2` | PASS |
| `gregory-xvi-acta.volume-03.line-00029103.part-01` | 1 | `dc38e26956fd92d8ad579431d700ce4d3720b6511bc98c3f2f11fcc1c20e3a2a` | PASS |
| `gregory-xvi-acta.volume-03.line-00029103.part-02` | 1 | `1a0be60a549a0a2553f06c9ad9c8aaa0f36caf9ebbe3fd4d04ec4d916ab13a29` | PASS |
| `gregory-xvi-acta.volume-03.line-00029263` | 1 | `789ac0be4e4ec4d863b8a706415489000034130846f1744b537936d3853338b9` | PASS |
| `gregory-xvi-acta.volume-03.line-00029263` | 2 | `8c0de32326279252284157e0f5a6becf15547263721648e60f092d90a61eb73e` | PASS |
| `gregory-xvi-acta.volume-03.line-00029416.part-01` | 1 | `e2d8a394cd1e38111ed8c5bc30c8f458cdd2048f28e876d64b38d276d0bd91f1` | PASS |
| `gregory-xvi-acta.volume-03.line-00029416.part-02` | 1 | `8135371569d8fd17795de08bea4c80bafd95390752775cf769f26020dbb0eec8` | PASS |
| `gregory-xvi-acta.volume-03.line-00029558.part-01` | 1 | `c571ac1836387cbf02e03239b8c284e566de70714e367b7235c8da0c25517b70` | PASS |
| `gregory-xvi-acta.volume-03.line-00029558.part-02` | 1 | `b1f2dd88b7af20168e6c3a70df9d399e313405d47206e124a59f22253b701b3d` | PASS |
| `gregory-xvi-acta.volume-03.line-00029558.part-02` | 2 | `40589c6655f57aba92f1570507664eb5116cbcb96e9973572a142222ded0e460` | PASS |
| `gregory-xvi-acta.volume-03.line-00029777` | 1 | `3ad3c998db4473bfee13b5726985c9a842b13c1d5ec3948cd9ae66ab73b8ab79` | PASS |
| `gregory-xvi-acta.volume-03.line-00029777` | 2 | `b7bc9f171049045c4dddedb01696da67b477f916af6eff9e9576d1301ae728d8` | PASS |
| `gregory-xvi-acta.volume-03.line-00029915` | 1 | `6c5340152665b548655065135e9edc70447017eb311cde2579b3d99fbf11df3d` | PASS |
| `gregory-xvi-acta.volume-03.line-00029915` | 2 | `13dd706d038e0d8b28448f51d238e71d003af562165e4dd2c1f8e9550bad5650` | PASS |
| `gregory-xvi-acta.volume-03.line-00030087` | 1 | `ab7c3f3bbbdb903e28fe4d5d86f98c6083f6ced3197bdd45b51e9c36c397c61a` | PASS |
| `gregory-xvi-acta.volume-03.line-00030158` | 1 | `d6a2049a236f57d89d3d169e9bdfa6b136c3ca71fba5a14488d8323c149aa0dc` | PASS |
| `gregory-xvi-acta.volume-03.line-00030246` | 1 | `89a07ea4e34e6aee56777ac6f6b94a6128ebbfd5b8ff8d748d8394d5eca37f64` | PASS |
| `gregory-xvi-acta.volume-03.line-00030308` | 1 | `0b8a915b0fdf4b2f6c3ab5bcbc5a5176b1c854ab972c1d20c4da82c7e0543806` | PASS |
| `gregory-xvi-acta.volume-03.line-00030377` | 1 | `65fa3434e79610859fa300230d67581b6dbd8b7dabcb262adf76a992892e5fbd` | PASS |
| `gregory-xvi-acta.volume-03.line-00030469.part-01` | 1 | `e050909c8e2248690a890e1bc25f4a2cc6316c67d2396aecb8eab1869c7f30b6` | PASS |
| `gregory-xvi-acta.volume-03.line-00030469.part-02` | 1 | `0b7eeff00a9a294dbedbe1db13fa15103a2e1fa77e4a43a150d09ec7f68c674b` | PASS |
| `gregory-xvi-acta.volume-03.line-00030613` | 1 | `8d76b266334532d7aca3d133499c4d24c4c58abd6ffdd2f39af41fff67bccee2` | PASS |
| `gregory-xvi-acta.volume-03.line-00030704` | 1 | `c9412c0a0b03a24b860b3620881e412c543a6d1c89eb41f2373ef385f4b238b0` | PASS |
| `gregory-xvi-acta.volume-03.line-00030801` | 1 | `21f51ad838c1bb5b78a72e0a367c33aeecf02bf579c223189712a3c9d8831863` | PASS |
| `gregory-xvi-acta.volume-03.line-00030908` | 1 | `2d5e48e0a24abc6ccd39959c02d18ca2c4db4911d1b726146594799cca10faa1` | PASS |
| `gregory-xvi-acta.volume-03.line-00031405` | 1 | `7844444ca2c3a51a5438390616c778f00fadc3f29f42a6149b18c28a152cc0b8` | PASS |
| `gregory-xvi-acta.volume-03.line-00031405` | 2 | `d6109afe4842e6f103b2ad4fdf73b1818357c62836fa6365cd1df7c694541b31` | PASS |
| `gregory-xvi-acta.volume-03.line-00031545` | 1 | `c9ad8247de9c84e3ae35cc2466acb1744fbbecda07ed3d83f751024d53cc19b2` | PASS |
| `gregory-xvi-acta.volume-03.line-00031615` | 1 | `7d625bf82b73937d91d926e22b7c360d39c271b7bded4796878f241a65e3e19e` | PASS |
| `gregory-xvi-acta.volume-03.line-00031752` | 1 | `e1a1114c10cde92b9c3ccbd8bbf0359dc5b8a29f9c0a9dcfa57e6b5c4ffebed9` | PASS |
| `gregory-xvi-acta.volume-03.line-00031858` | 1 | `87365d0d8fc2af8153bf4eaba6ccf843f279013463f1322ba452c1bb5f6132c2` | PASS |
| `gregory-xvi-acta.volume-03.line-00031950` | 1 | `7298c67b4b93cb51a85593fffeb57f66895355041d9155705af154840c84bac4` | PASS |
| `gregory-xvi-acta.volume-03.line-00032044` | 1 | `651a17a7ef18072cc968e9dca5d4d1b878cf7738dc318d1d3bdd0414ef4db6f8` | PASS |
| `gregory-xvi-acta.volume-03.line-00032172` | 1 | `d152de094ef9d7a22da13c4eead319a06ad92b3899fdfff90660b8b41d45dc91` | PASS |
| `gregory-xvi-acta.volume-03.line-00032247` | 1 | `86064b44d8acc6b916ccbc6c133211a70b621d6feef2b5364e786915d69dd99a` | PASS |
| `gregory-xvi-acta.volume-03.line-00032341` | 1 | `f445b44675c07f0d4c03519198adbf90625cd932d4e7ed4ae8540b97c586293d` | PASS |
| `gregory-xvi-acta.volume-03.line-00032425` | 1 | `2d7ecce06f104e4828107ea15a166e7f520a642c9ca624bd5302a8a24d8a7e6b` | PASS |
| `gregory-xvi-acta.volume-03.line-00032524.part-01` | 1 | `97c545d306ec27e6e0057e8cf2608f1467a6a9f4b9e8b47b70f329510f6f89b2` | PASS |
| `gregory-xvi-acta.volume-03.line-00032524.part-02` | 1 | `2d0a53b8c32c126a356cebf5ed77d586824e2a17b63266b8ce9d92c50ac87657` | PASS |
| `gregory-xvi-acta.volume-03.line-00032713` | 1 | `3a1d2b254e98df49c0ed3f1955c3b4f1892c3b918a253c23e84efe80fc8a1c30` | PASS |
| `gregory-xvi-acta.volume-03.line-00032826` | 1 | `bb5059c9c27926666109466ac30b9628b2b9f62fb21dbcd6fbbd66ca2e0a9fa8` | PASS |
| `gregory-xvi-acta.volume-03.line-00032826` | 2 | `d4e44b72467a152f995c17892b113c840f5ee644ee5206aba7500d4216e29fa6` | PASS |
| `gregory-xvi-acta.volume-03.line-00032826` | 3 | `59534921103565aafadaf8a209b1942efe0fb73b6504a38fa828a1c049577bcf` | PASS |
| `gregory-xvi-acta.volume-03.line-00032826` | 4 | `d7b1d308f7b56bfefa39279d990f9f2ffefff338b695abee811581216fb0b587` | PASS |
| `gregory-xvi-acta.volume-03.line-00033233` | 1 | `a583df86f6075b1c6991b51c39108ec63426c8088da1298b2e8d59c450e3d134` | PASS |
| `gregory-xvi-acta.volume-03.line-00033328` | 1 | `763c8e4e3d0d4fe258e9f17149a75a87758832bc8fa1b54ccf701ab9555b9a6f` | PASS |

## Per-document findings

No document has a blocking finding. Standing coordinator rulings were applied: the three consistorial allocutions (`line-00027232`, `line-00027383`, `line-00027785.part-02`) and `line-00031858` display the issuer `ACTA GREGORII PP. XVI.` from the volume running title, matching frozen metadata (non-blocking qualification); OCR-damaged issuer spellings (`. GREGORIUS PP. XVI.`, `GREGORIUS PP, XVI.`, `GREGORIUS PP. XVI`) and the audience-rescript recording official `Ccard. Vicarius.` match metadata and are qualifications. Sparse final pages all carry genuine source closing (dating clause, sanction clause) before the project notes; no final page holds only project notices. No digitizer signature, running head, fused marginal summary, raw placeholder, clipping, overlap or missing glyph was seen.

### `gregory-xvi-acta.volume-03.line-00027141` — PASS

Literas tuas datas — Paulo Marusci archiepiscopo primati Armeno Constantinopolitano de coadiutore · GREGORIUS PP. XVI. · 1842-01-19 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-01-19, Latin match; address, issuer line, salutation, body, Datum Romae dating clause in right column; terminal source/rights notes follow; clean two-column layout, no clipping or furniture.

### `gregory-xvi-acta.volume-03.line-00027232` — PASS

Communis Nobiscum — Allocutio in consistorio secreto de cardinalibus declarandis et creandis · ACTA GREGORII PP. XVI. · 1842-01-24 · 1 page(s).

- p1: Allocution body, cardinal lists, Quid vobis videtur, declarations and closing invocation (literal OCR crosses disclosed) on one page; no dating clause, disclosed; clean layout. Findings: NON-BLOCKING qualification: issuer line ACTA GREGORII PP. XVI. taken from volume running title (standing ruling), matches metadata

### `gregory-xvi-acta.volume-03.line-00027383` — PASS

Quod tandiu ad faciliorem Sabinensis ecclesiae procurationem — Allocutio de novo ecclesiae Sabinensis statu · ACTA GREGORII PP. XVI. · 1842-01-24 · 1 page(s).

- p1: Allocution complete on one page ending 'succedant.,'; no dating clause, disclosed in note; OCR stray underscores are literal; clean layout. Findings: NON-BLOCKING qualification: issuer line ACTA GREGORII PP. XVI. taken from volume running title (standing ruling), matches metadata

### `gregory-xvi-acta.volume-03.line-00027785.part-02` — PASS

Benedicti XIV gloriosissimae memoriae — Allocutio de patriarchatu Ciliciae Armenorum et electione Iacobi Holas · ACTA GREGORII PP. XVI. · 1842-01-27 · 1 page(s).

- p1: Allocution complete on one page with Quid vobis videtur, confirmation and closing invocation (literal OCR crosses disclosed); no dating clause, disclosed; clean layout. Findings: NON-BLOCKING qualification: issuer line ACTA GREGORII PP. XVI. taken from volume running title (standing ruling), matches metadata

### `gregory-xvi-acta.volume-03.line-00027490` — PASS

Romani Pontificis, quem pastor ille coelestis — Iacobus Holas in patriarcham Ciliciae Armenorum confirmatur et transfertur · GREGORIUS EPISCOPUS · 1842-01-28 · 3 page(s).

- p1: Title, GREGORIUS EPISCOPUS, 1842-01-28, Latin match; address, issuer, salutation, body flow cleanly across two columns; no furniture or clipping.
- p2: Body continues with oath formula in guillemets ending 'evangelia >.'; columns balanced, no running heads or digitizer lines.
- p3: Final page holds the source's own dating clause then project notes; acceptable sparse close. Findings: NON-BLOCKING qualification: sparse final page carries genuine Datum Romae dating clause before terminal source/rights notes

### `gregory-xvi-acta.volume-03.line-00027785.part-01` — PASS

Cum Nos hodie patriarchali ecclesiae — Iacobo Holas patriarchae Ciliciae Armenorum pallium conceditur · GREGORIUS EPISCOPUS · 1842-01-28 · 2 page(s).

- p1: Title, GREGORIUS EPISCOPUS, 1842-01-28, Latin match; address, salutation, body with pallium and oath formulas in two columns; clean layout.
- p2: Final page holds the source dating clause then project notes; acceptable sparse close. Findings: NON-BLOCKING qualification: sparse final page carries genuine Datum Romae dating clause before terminal source/rights notes

### `gregory-xvi-acta.volume-04.line-00092886.part-02` — PASS

Rescriptum ex audientia quo Gregorius XVI regulas processus criminalis tribunalis vicariatus adprobat, 29 ianuarii 1842 · Ccard. Vicarius. · 1842-01-29 · 1 page(s).

- p1: Short rescript: Ex audientia date line, third-person grant, subscription Ccard. Vicarius., then source note (1904 volume) and rights; single-column use of left column only, no defect. Findings: NON-BLOCKING qualification: issuer line 'Ccard. Vicarius.' (OCR'd subscription of the recording cardinal vicar) matches frozen metadata; audience-rescript genre and papal context disclosed in source note

### `gregory-xvi-acta.volume-03.line-00028049` — PASS

Binas nuper a te accepimus literas — Maximo patriarchae Antiocheno Graeco-Melchitarum de auxilio pro fidelibus Libani · . GREGORIUS PP. XVI. · 1842-02-06 · 1 page(s).

- p1: Title, 1842-02-06, Latin match; address, salutation, body, Datum Romae dating clause; source note flows from left column foot into right column; no furniture or clipping. Findings: NON-BLOCKING qualification: issuer reads '. GREGORIUS PP. XVI.' with stray OCR mark, matches frozen metadata

### `gregory-xvi-acta.volume-03.line-00028140` — PASS

Ex munere pastoralis ministerii — Insula Novae Scotiae in episcopatum Halifaxiensem erigitur · GREGORIUS PP. XVI. · 1842-02-15 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-02-15, Latin match; body, non obstantibus clause and Datum Romae dating clause; clean two-column layout.

### `gregory-xvi-acta.volume-03.line-00028229` — PASS

Apostolatus officium — Guilelmo Fraser ecclesiae Halifaxiensi praeficitur · GREGORIUS PP. XVI. · 1842-02-15 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-02-15, Latin match; address, salutation, body flow cleanly; right column ends mid-sentence 'auctoritate Nostra' continuing on page 2.
- p2: Body continues 'impendere licite valeat', non obstantibus clause, Datum Romae dating clause, then source/rights notes; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00028370` — PASS

Officium perlibenter accepimus — Petro episcopo Augustano de funere reginae acatholicae · GREGORIUS PP. XVI. · 1842-02-16 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-02-16, Latin match; address with (Augustam Vindelicorum), salutation, body; notes retained per source note; no running heads or digitizer lines. Findings: NON-BLOCKING qualification: the edition's historical notes 2-6 are set as separate paragraphs in source order at a paragraph boundary in the right column (between '...in destructionem.' and 'Plane autem'), not fused into a body sentence; note markers OCR'd as '?', '3', '*', '5', '©'; no separately numbered note 1 is visible (limitation, not collated)
- p2: Body close 'peramanter impertimur', Datum Romae dating clause, source note stating substantive notes retained literally in source order; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00028540` — PASS

Romani Pontifices honorum insignia — Canonicis cathedralis Sabinensis cappa magna conceditur · GREGORIUS PP. XVI. · 1842-02-18 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-02-18, Latin match; body, non obstantibus clause, Datum Romae dating clause; clean layout (an OCR line break 'est optime meritus' / 'annuendum' renders as short indented paragraphs, literal).

### `gregory-xvi-acta.volume-03.line-00028645` — PASS

Catholicae religionis causa — Publicae preces et indulgentia in forma iubilaei pro Hispania · GREGORIUS PP. XVI. · 1842-02-22 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-02-22, Latin match; body flows across both columns; stray OCR vertical mark 'per- |' left column is literal and disclosed in source note.
- p2: Body continues through indulgence grant, publication clause and Datum Romae dating clause; source note discloses stray vertical mark; no furniture or clipping.

### `gregory-xvi-acta.volume-03.line-00028913` — PASS

Romanorum indulgentia Pontificum — Clero collegiatae Spinazzola rocchetum et almutia conceduntur · GREGORIUS PP. XVI. · 1842-03-01 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-03-01, Latin match; body, non obstantibus clause, Datum Romae dating clause; clean layout.

### `gregory-xvi-acta.volume-03.line-00029103.part-01` — PASS

Has fidelissimae tuae maiestati literas — Mariae Portugalliae reginae rosa aurea mittitur · GREGORIUS PP. XVI. · 1842-03-12 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-03-12, Latin match; address, salutation, body with in-paragraph Datum Romae dating clause; source note flows from left column foot into right column; clean.

### `gregory-xvi-acta.volume-03.line-00029103.part-02` — PASS

Redditae Nobis sunt humanissimae litterae — Mariae Portugalliae reginae de baptismo prolis nasciturae · GREGORIUS PP. XVI. · 1842-03-12 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-03-12, Latin match; address, salutation, body, Datum Romae dating clause continuing to right column top, then source/rights notes; clean.

### `gregory-xvi-acta.volume-03.line-00029263` — PASS

Romanum certe decet Pontificem — De abbatia Sanctae Mariae del Tiglietto in dioecesi Aquensi · GREGORIUS PP. XVI. · 1842-03-18 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-03-18, Latin match; body and derogation clause flow across both columns; no running heads. Findings: NON-BLOCKING qualification: OCR block breaks render as short separate paragraphs ('spe-' alone at top of right column before 'ctabit'; 'effectus sortiri ... ad quos-' before 'spectat'); words are complete and in order, no clipping
- p2: Body close 'contrarium facientibus quibuscumque', Datum Romae dating clause, then source/rights notes; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00029416.part-01` — PASS

Quod propositum Nobis fuit — Leopoldo Belgarum regi de Raphaele Fornari nuntio · GREGORIUS PP. XVI. · 1842-03-28 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-03-28, Latin match; address, salutation, body, Datum Romae dating clause; source note continues into right column; clean. Findings: NON-BLOCKING qualification: OCR block break renders 'modis provisum esset, unaque vincula officio-' as a short separate paragraph; text complete and in order

### `gregory-xvi-acta.volume-03.line-00029416.part-02` — PASS

Opportunum in Domino iudicavimus — Engelberto cardinali Sterckx et episcopis Belgii de Raphaele Fornari nuntio · GREGORIUS PP. XVI. · 1842-03-28 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-03-28, Latin match; address to Cardinal Sterckx and Belgian bishops, salutation, body, Datum Romae dating clause, source/rights notes; left column only, clean.

### `gregory-xvi-acta.volume-03.line-00029558.part-01` — PASS

Nostrum et Apostolicae Sedis nuntium — Aloysiae Belgarum reginae de Raphaele Fornari nuntio · GREGORIUS PP. XVI. · 1842-03-28 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-03-28, Latin match; address to Queen Aloysia, salutation, body, Datum Romae dating clause, source/rights notes; left column only, clean.

### `gregory-xvi-acta.volume-03.line-00029558.part-02` — PASS

Inter ea, quae supremi apostolatus munere urgente — Epistola encyclica ad episcopos Helvetiae de coenobiis · GREGORIUS PP. XVI. · 1842-04-01 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-01, Latin match (encyclical to Swiss bishops); address, salutation, body across both columns ending 'unicuique ve-' continued on page 2; clean.
- p2: Body close 'peramanter impertimur', dating clause, project notes; source-bearing final page. Findings: NON-BLOCKING qualification: sparse final page carries the body close and genuine Datum Romae dating clause before source/rights notes

### `gregory-xvi-acta.volume-03.line-00029777` — PASS

Ex debito pastoralis officii — Vicariatus Novae Hollandiae in episcopatus Sydneyensem, Hobartoniensem et Adelaidensem partitur · GREGORIUS PP. XVI. · 1842-04-05 · 2 page(s).

- p1: Title (three lines), GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-04-05, Latin match; body and decree clause across both columns; clean.
- p2: Non obstantibus clause, Datum Romae dating clause, then source/rights notes; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00029915` — PASS

Ecclesiarum omnium ex demandato Nobis — Cardinali Lambruschini episcopo Sabinensi de literis apostolicis pro beneficiis · GREGORIUS PP. XVI. · 1842-04-05 · 2 page(s).

- p1: Title (three lines), GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-04-05, Latin match; body across both columns ending 'firmas, va-' continued on page 2; clean.
- p2: Body continues 'lidas et efficaces', non obstantibus clause, Datum Romae dating clause, source/rights notes; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00030087` — PASS

Qui pro singulari — Ferdinando Austriae imperatori de morte archiducis Herminiae · GREGORIUS PP. XVI. · 1842-04-07 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-07, Latin match; address to Emperor Ferdinand, salutation, body, Datum Romae dating clause, notes; left column only, clean.

### `gregory-xvi-acta.volume-03.line-00030158` — PASS

Qui sensus animi Nostri sint — Ferdinando Austriae imperatori de matrimonio Adelaidis et Victoris Emmanuelis · GREGORIUS PP. XVI. · 1842-04-07 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-07, Latin match; address, salutation, body, Datum Romae dating clause; source/rights notes in right column; clean.

### `gregory-xvi-acta.volume-03.line-00030246` — PASS

Cognitum Nobis exploratumque — Ludovico Bavariae regi de nuptiis Adelgundae · GREGORIUS PP. XVI. · 1842-04-18 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-18, Latin match; address to King Ludwig, salutation, body, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00030308` — PASS

Ad supremum totius Ecclesiae regimen — Sedes Sydneyensis in metropolitanam erigitur · GREGORIUS PP. XVI. · 1842-04-22 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-04-22, Latin match; body, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: witness abbreviates conventional formulae with 'etc.' ('de venn. fratrum etc.', 'non obstantibus etc.'), disclosed in source note and kept literal

### `gregory-xvi-acta.volume-03.line-00030377` — PASS

Compertum habenti tibi — Carolo Alberto Sardiniae regi de matrimonio Victoris Emmanuelis · GREGORIUS PP. XVI. · 1842-04-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-23, Latin match; address to Carlo Alberto, salutation, body, Datum Romae dating clause; source note continues into right column; clean. Findings: NON-BLOCKING qualification: OCR block breaks render several short separate paragraphs ('Compertum habenti tibi quomodo erga re-' / 'giam ...'; 'Nostrum tamen ... tibi,' / ''carissime ... confir-'; 'cultores, ad ... ipsius-'); text complete and in order

### `gregory-xvi-acta.volume-03.line-00030469.part-01` — PASS

Ad tam multa quae habemus — Francisco Estensi duci Mutinae de nuptiis filii · GREGORIUS PP. XVI. · 1842-04-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-04-23, Latin match; two-line address, salutation, body, Datum Romae dating clause, source note, rights line at top of right column; clean.

### `gregory-xvi-acta.volume-03.line-00030469.part-02` — PASS

Omnis iucunda Nobis accidit occasio — Leopoldo archiduci Austriae, magno duci Etruriae, de nova prole · GREGORIUS PP. XVI. · 1842-05-30 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-05-30, Latin match; address in three short lines (literal OCR), salutation, body, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00030613` — PASS

Romani Pontifices provido sane consilio — Beneficiariis cathedralis Alatrinae cappa conceditur · GREGORIUS PP. XVI. · 1842-06-14 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-06-14, Latin match; body, non obstantibus, Datum Romae dating clause; clean. Findings: NON-BLOCKING qualification: stray '4' at end of derogation clause ('cumque. 4') is literal OCR, disclosed in source note

### `gregory-xvi-acta.volume-03.line-00030704` — PASS

Romani Pontifices honorifica insignia — Canonicis Massae Fiscagliae floccus violaceus conceditur · GREGORIUS PP. XVI. · 1842-06-17 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-06-17, Latin match; body, non obstantibus, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00030801` — PASS

Cum christianae et civili reipublicae — Titulus Cappellae Gregorianae confirmatur · GREGORIUS PP. XVI. · 1842-06-21 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-06-21, Latin match; body, non obstantibus, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: OCR block breaks render short separate paragraphs ('Cum christianae ... teneris annis' / 'ad omnem ...'; 'Non obstantibus ... constitu-' / 'tionibus ...'); stray leading '_' before Datum is literal OCR

### `gregory-xvi-acta.volume-03.line-00030908` — PASS

Cum nobiles familiae religione — Praedium Valle Pietra in marchionatum erigitur · GREGORIUS PP. XVI. · 1842-06-22 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-06-22, Latin match; body across both columns, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: OCR block breaks render short separate paragraphs ('esse soleant, tum R. Pontifices splendidos no-,'; 'presse derogamus ...'); text complete and in order

### `gregory-xvi-acta.volume-03.line-00031405` — PASS

Cum viri nobilitate, religione — Fundus Pietralata in marchionatum erigitur · GREGORIUS PP. XVI. · 1842-06-28 · 2 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-06-28, Latin match; body across both columns ending 'et san-' continued on page 2; clean.
- p2: Body continues 'ctionibus apostolicis', derogation clause, Datum Romae dating clause, source/rights notes; source-bearing final page.

### `gregory-xvi-acta.volume-03.line-00031545` — PASS

Gaudii nuntium — Ferdinando Austriae imperatori de nato filio archiducis Francisci Caroli · GREGORIUS PP. XVI. · 1842-06-30 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-06-30, Latin match; address to Emperor Ferdinand, salutation, body, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00031615` — PASS

Literas accepimus, quibus, dilecte fili — Ruperto Leiss praesidi monachorum Schyrensium de funere reginae acatholicae · GREGORIUS PP. XVI. · 1842-07-09 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-07-09, Latin match; address to Rupert Leiss, salutation, body across both columns, Datum Romae apud sanctam Mariam Maiorem dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00031752` — PASS

Cum Nobis nihil certe potius — Sodalitas Sanctissimi Cordis Mariae Varsaviae in archisodalitatem erigitur · GREGORIUS PP. XVI. · 1842-07-15 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-07-15, Latin match; body, non obstantibus, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00031858` — PASS

Haerentem diu animo Nostro dolorem — Allocutio de calamitatibus Ecclesiae catholicae in imperio Russiaco · ACTA GREGORII PP. XVI. · 1842-07-22 · 1 page(s).

- p1: Allocution 'Venerabiles fratres' complete, closes 'quantocius largiatur.' at top of right column; clean. Findings: NON-BLOCKING qualification: issuer line ACTA GREGORII PP. XVI. taken from volume running title (standing ruling), matches metadata; NON-BLOCKING qualification: allocution has no dating clause, date taken from excluded edition caption, disclosed in source note

### `gregory-xvi-acta.volume-03.line-00031950` — PASS

Studium pio prudentique antistite — Thomae Gousset archiepiscopo Rhemensi de libris liturgicis · GREGORIUS PP. XVI. · 1842-08-06 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-08-06, Latin match; address to Thomas Gousset, issuer and salutation, body, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00032044` — PASS

Pastoris aeterni vicariam operam — Vicariatus apostolicus Oceaniae Centralis erigitur · GREGORIUS PP. XVI. · 1842-08-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-08-23, Latin match; body, decree and non obstantibus clauses, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00032172` — PASS

Cum novus ac distinctus alter vicariatus — Guillelmo Dusarre coadiutor vicarii apostolici Oceaniae Centralis (CLXX) · GREGORIUS PP. XVI. · 1842-08-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-08-23, Latin match; address to Guillelmus Dusarre, salutation, body, Datum Romae dating clause; source note continues into right column; clean. Findings: NON-BLOCKING qualification: witness abbreviates 'Non obstantibus etc.', disclosed in source note and kept literal; title carries disambiguating '(CLXX)' matching frozen metadata

### `gregory-xvi-acta.volume-03.line-00032247` — PASS

Cum gravissimis ex causis — Petro Bataillon vicariatus Oceaniae Centralis committitur · GREGORIUS PP. XVI. · 1842-08-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-08-23, Latin match; address to Petrus Bataillon, issuer with salutation, body, non obstantibus, Datum Romae dating clause continuing to right column, notes; clean. Findings: NON-BLOCKING qualification: OCR block breaks render short separate paragraphs ('tate erigendum censuerimus iis circumscriptum'; 'limitibus ... alacri'); text complete and in order

### `gregory-xvi-acta.volume-03.line-00032341` — PASS

Cum novus ac distinctus alter vicariatus — Guillelmo Dusarre coadiutor vicarii apostolici Oceaniae Centralis (CLXXII) · GREGORIUS PP. XVI. · 1842-08-23 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI., 1842-08-23, Latin match; address, salutation, body, non obstantibus, Datum Romae dating clause; notes in right column; clean. Findings: NON-BLOCKING qualification: title carries disambiguating '(CLXXII)' matching frozen metadata (recurrent incipit with CLXX on same date)

### `gregory-xvi-acta.volume-03.line-00032425` — PASS

De universi dominici gregis salute — Raphaeli Barissich visitator apostolicus archidioecesis Antibarensis · GREGORIUS PP, XVI. · 1842-08-25 · 1 page(s).

- p1: Title, 1842-08-25, Latin match; address to Raphael Barissich, salutation, body, non obstantibus, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: issuer reads 'GREGORIUS PP, XVI.' (OCR comma), matches frozen metadata and identifies the pope; stray '»' after derogation clause is literal OCR

### `gregory-xvi-acta.volume-03.line-00032524.part-01` — PASS

Cum ex recta religiosarum familiarum disciplina — Franciscus Villardel visitator apostolicus trium congregationum Basilianarum Melchitarum · GREGORIUS PP. XVI · 1842-08-30 · 1 page(s).

- p1: Title (three lines), 1842-08-30, Latin match; address to Franciscus Villardel, salutation, body, mandamus, non obstantibus, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: issuer reads 'GREGORIUS PP. XVI' (no final period), matches frozen metadata

### `gregory-xvi-acta.volume-03.line-00032524.part-02` — PASS

Apostolici ministerii munus — Missio Hollandica de Curaçao in vicariatum apostolicum erigitur · GREGORIUS PP. XVI. · 1842-09-20 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-09-20, Latin match; body, non obstantibus, Datum Romae dating clause continuing to right column, notes; clean. Findings: NON-BLOCKING qualification: isolated OCR marks ':' , '_' and ';' kept literal in body/dating clause, disclosed in source note

### `gregory-xvi-acta.volume-03.line-00032713` — PASS

Cum per similes Nostras apostolicas literas — Sedes episcopalis dioecesis Canadae superioris occidentalis in civitate Torontina constituitur · GREGORIUS PP. XVI. · 1842-09-20 · 1 page(s).

- p1: ' after 'civitate' kept literal, disclosed in source note|Title (three lines), GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-09-20, Latin match; body, decree and non obstantibus clauses, Datum Romae dating clause, notes; clean. Findings: NON-BLOCKING qualification: isolated OCR mark '

### `gregory-xvi-acta.volume-03.line-00032826` — PASS

Universalis Ecclesiae procuratio — Erectio cathedralis ecclesiae Sancti Salvatoris in America centrali · GREGORIUS EPISCOPUS · 1842-09-28 · 4 page(s).

- p1: Title, GREGORIUS EPISCOPUS servus servorum Dei ad perpetuam rei memoriam, 1842-09-28, Latin match; dense consistorial bull body flows across both columns; no running heads or clipping.
- p2: Body continues (erection, territory, dotation, decimae) across both full columns; clean. Findings: NON-BLOCKING qualification: OCR block break renders 'dum- modo ex peculiari indulto seu privilegio non' / 'Sint eis attributa' as separate paragraphs; text complete and in order
- p3: Body continues (administration, metropolitan subjection, executor, praesentes, non obstantibus, transumpta clauses); clean. Findings: NON-BLOCKING qualification: OCR block breaks render 'decreto executoriali describendi fines novae dioe-.' as a short paragraph at left-column foot, continuing 'cesis' at right-column top; text complete and in order
- p4: Source-bearing final page; no furniture. Findings: NON-BLOCKING qualification: sparse final page carries the genuine Nulli ergo sanction clause and Datum Romae apud sanctam Mariam Maiorem dating clause before source/rights notes; stray '_protenduntur' literal, disclosed

### `gregory-xvi-acta.volume-03.line-00033233` — PASS

Dominici gregis cura — Nova Brunopolis (New Brunswick) in dioecesim erigitur · GREGORIUS PP. XVI. · 1842-09-30 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-09-30, Latin match; body, decree, non obstantibus, Datum Romae dating clause, notes; clean.

### `gregory-xvi-acta.volume-03.line-00033328` — PASS

De universi dominici gregis salute — Vicariatus apostolicus Guineae et Sierra Leone instituitur · GREGORIUS PP. XVI. · 1842-10-03 · 1 page(s).

- p1: Title, GREGORIUS PP. XVI. ad perpetuam rei memoriam, 1842-10-03, Latin match; body, decree, non obstantibus, Datum Romae dating clause; source note flows from left column foot into right column; clean. Findings: NON-BLOCKING qualification: isolated OCR mark ':' after 'attentari.' kept literal, disclosed in source note

## Limitations

- Literal, uncorrected, uncollated historical OCR (Acta Gregorii Papae XVI, Rome: Ex Typographia Polyglotta S. C. de Propaganda Fide, 1902/1904); OCR spellings, stray marks and line-block breaks are kept literal and were not judged or corrected.
- Layout-only visual review of the supplied rasters; no word-level collation, source-fidelity recheck, historical authentication, date reconstruction, publication, installation or deployment claim.
- Historical notes in `line-00028370` were checked only for separate setting and source order; note-marker OCR (`?`, `*`, `©`) is literal and no note-numbering was collated.
- Several readers display OCR line-block breaks as short separate paragraphs (recorded per page above); words remain in reading order and these are not layout defects.
