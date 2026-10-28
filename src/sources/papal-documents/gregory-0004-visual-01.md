# Gregory XVI visual review gregory-0004 lane 01

PASS: 34 assigned PDFs, 57 pages individually opened at full size; zero blocking findings. All are new inspections, with zero reused pages. This report covers only lane 01 of Gregory batch `gregory-0004`, all from volume 2 of the Acta Gregorii PP. XVI (acts dated 1837-01-04 to 1838-02-08).

## Scope and method

Each assigned page PNG was opened as its own full-size image (1700 x 2200 raster) with the Read tool, one image per page. No contact sheet, thumbnail, new raster pass, source acquisition, word-level collation, text correction or date reconstruction was performed. The rasters are those produced by the repository `pdf-review` tool and pinned in the assignment.

On every page the displayed title, responsible issuer, act date and language label were compared with the frozen metadata. Headings, two-column flow, gutter, margins and visible glyphs were inspected, together with the natural source closing (dating clause, subscriptions, historical notes) and the terminal source/rights apparatus. No clipping, overlap, missing-glyph or tofu blocks, collapsed table, stranded heading, modern digitizer signature (for example "Digitized by Google" or a damaged variant), journal running head or page-furniture line interrupting a body sentence, marginal summary fused into a body sentence, or raw placeholder such as `None` was found.

No document in this lane is an identified historical fragment: every assigned record has `extent_kind` `printed-act` and a complete-papal-body source note, so no fragment title or missing-content notice was expected or displayed. No assigned document carried a `prior_finding`.

This report does not claim installation, publication, deployment, historical authentication or word-level fidelity.

## Evidence verification

All assigned PDF, page-PNG, render receipt, frozen manifest and raster-run digests were computed before and after inspection and matched their assignment pins both times (94 files each pass; the before and after verification records are byte-identical).

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt (`.scratch/typeset_pipeline/claude/gregory-0004/receipt.json`) | `4dccf3338c9c4a77fb4b36f5661a89f0e1eb13561fd927c06e02524ae3e28512` | Before and after |
| Frozen manifest (`.scratch/typeset_pipeline/claude/gregory-0004/frozen-manifest.json`) | `be696029777647c8c7e703017638fef85e2ed9a11cb97d4764486d03c926af9c` | Before and after |
| Raster run (`.scratch/claude-review/rasters-gregory-0004/review-run.json`) | `ff6bf42a5454221d05d0f1a148b04b03f6da70a3005e6d6d35413f76f551d83b` | Before and after |
| Lane assignment | `29730dcea172230d3a7b79f184f983ae5711b7d58dd3b89a8aa636329b049940` | Exact scope binding |
| Individual inspection ledger (`observations.jsonl`) | `651c9720de9c66d6523b4473850778d91a4292b04d962c983c1d11cef46d94d2` | 57 unique observations |
| Before verification record | `89f34f985c94cd355bd1a6fe99582721d89ed9f78c0790e23f9ee5cb55fa01d6` | PASS |
| After verification record | `89f34f985c94cd355bd1a6fe99582721d89ed9f78c0790e23f9ee5cb55fa01d6` | PASS; identical input hashes |

## PDF outcomes

| Source ID | Date metadata | Language | Page count | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `gregory-xvi-acta.volume-02.line-00027209` | 1837-01-04 | `la` | 2 | 1, 2 | `19c030a0839ec0a9ff4bb3a7dc8bbcbf8bd0b06c4b945165c7b67178c6f85bbb` | PASS |
| `gregory-xvi-acta.volume-02.line-00027394` | 1837-01-08 | `la` | 1 | 1 | `e5513bd2ad5b1df359f1603bfde5cbb72b8c3f875a43c686a38294fffb25cd37` | PASS |
| `gregory-xvi-acta.volume-02.line-00027512.part-01` | 1837-01-10 | `la` | 1 | 1 | `dce45781b2a106f97fa8e5480280b5388b0d6cf935dac41b94657a8dcd8e99bb` | PASS |
| `gregory-xvi-acta.volume-02.line-00027512.part-02` | 1837-01-14 | `la` | 1 | 1 | `abb173f54b1f7e41471df8ff31ad92196b332d081834922242ac0b035a54a0f2` | PASS |
| `gregory-xvi-acta.volume-02.line-00027716.part-01` | 1837-01-19 | `la` | 1 | 1 | `1df9fee5c823bc98e52f7a01e81d47d079ce65568f3d80e0aab5debe18807155` | PASS |
| `gregory-xvi-acta.volume-02.line-00027716.part-02` | 1837-01-24 | `la` | 2 | 1, 2 | `5ac6c08bf7f83f0f801449eb385924e40923951421ca45f95916044706118671` | PASS |
| `gregory-xvi-acta.volume-02.line-00027994` | 1837-01-29 | `la` | 4 | 1, 2, 3, 4 | `33f2faa68aa44ef802e0628c966077af5d32b047e1da053974128ff14da3a55c` | PASS |
| `gregory-xvi-acta.volume-02.line-00028557` | 1837-02-21 | `la` | 1 | 1 | `deba51328abc8fde8bc9d17ee4873ad2d245713d055bb361aabe5a3bccd4182a` | PASS |
| `gregory-xvi-acta.volume-02.line-00028834` | 1837-03-10 | `la` | 2 | 1, 2 | `830733eb7fb20f89e4a06a27abaeada1fc2c985b800d7c81a0c389ebd5000894` | PASS |
| `gregory-xvi-acta.volume-02.line-00029012` | 1837-03-13 | `la` | 1 | 1 | `d9246d6f0b4ad8b8a4c199be2021daa6c96471988f66c570b980a05da8c05c98` | PASS |
| `gregory-xvi-acta.volume-02.line-00029485.part-01` | 1837-04-12 | `la` | 1 | 1 | `2e14f7386cd7c52747fad23362e8d738ecb40636bf8368d689975e895bc31a86` | PASS |
| `gregory-xvi-acta.volume-02.line-00029095.part-02` | 1837-04-14 | `la` | 3 | 1, 2, 3 | `de4e729fd58dc784e57395870f232c618c009396042b22549e3c4aefedfeec78` | PASS |
| `gregory-xvi-acta.volume-02.line-00029485.part-02` | 1837-04-22 | `la` | 1 | 1 | `c365c3e23f5cd154749ca416ff7d7890974a8f15bfa5f94e31a789be017b7f66` | PASS |
| `gregory-xvi-acta.volume-02.line-00029666` | 1837-04-25 | `la` | 2 | 1, 2 | `a9c931e2c0f8422324210deb90657f305c9fbac63eb69d28a76d6735805ed78c` | PASS |
| `gregory-xvi-acta.volume-02.line-00029942` | 1837-05-01 | `la` | 2 | 1, 2 | `6fcc0c9d53d00c06bb7e1747a12b35c1f3fc57ad0035a26969c755f4c1a653c2` | PASS |
| `gregory-xvi-acta.volume-02.line-00030727` | 1837-05-22 | `la` | 2 | 1, 2 | `4d968680e553e80c27ec966a490db9192e08b71f3deb53be8087729882ca1b3a` | PASS |
| `gregory-xvi-acta.volume-02.line-00030892` | 1837-05-30 | `la` | 1 | 1 | `a13f647d2d140ddf8f4d96caf0221220f0844662d3cd26882d3a3fbd84a4f8b7` | PASS |
| `gregory-xvi-acta.volume-02.line-00030966.part-01` | 1837-06-06 | `la` | 1 | 1 | `f5da78ee8c05bc16189e1701ec73ab8f5cb6b03e15486d61fc54e2ab2e150874` | PASS |
| `gregory-xvi-acta.volume-02.line-00030966.part-02` | 1837-06-06 | `la` | 1 | 1 | `ce2e65e52fd3c74d36d7b191b2eadf44e6466118a43e9e28a6e264d0294d5baf` | PASS |
| `gregory-xvi-acta.volume-02.line-00031091.part-01` | 1837-06-13 | `la` | 1 | 1 | `bd87a8a27af025d2606861fe42b81fc933ef3a69a7d9ee18f20b2b118f9f4907` | PASS |
| `gregory-xvi-acta.volume-02.line-00031404` | 1837-07-28 | `la` | 1 | 1 | `54a6acd0866fee6450710b6e7c185ed8516f9978ef3e4eba41fc7d2fcdba6442` | PASS |
| `gregory-xvi-acta.volume-02.line-00031488.part-01` | 1837-07-28 | `la` | 1 | 1 | `ee12eef69212a488c7ae87e9a6bb7428c646b379d45244a69672533959b198cf` | PASS |
| `gregory-xvi-acta.volume-02.line-00031488.part-02` | 1837-07-28 | `la` | 1 | 1 | `1c2ac696008298e8631b2389bf47471c45e206bde349c1c1ce739de127c57328` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-04` | 1837-08-08 | `la` | 3 | 1, 2, 3 | `4bd67ca8946f779f35674d0da1ed40517e49c469943482642f0a9a06cfa1687a` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-05` | 1837-08-08 | `la` | 3 | 1, 2, 3 | `a257c69133a7becdd3ec572b5b563e7a2490ec8d2f23a491c9a593d20599fa81` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-06` | 1837-08-10 | `la` | 1 | 1 | `e9fb3e2aff8b29402000cf727c6da3b781e2ab3689648411e411c94e0294e3b5` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-01` | 1837-12-10 | `la` | 2 | 1, 2 | `d31548104da247a2969388764f966265b0b3ff3f8217af61dd74451e6213b39e` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-02` | 1837-12-12 | `mul` | 4 | 1, 2, 3, 4 | `9837a91a0bef953ecd1d686b5f9fbfadda34e9ef8612e532295485efe3c3c715` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-03` | 1837-12-19 | `la` | 2 | 1, 2 | `03a77f58d5c4bd32f138ea157655ed17614099baccca375fd81b6b0af26450bd` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-04` | 1837-12-22 | `la` | 2 | 1, 2 | `21f86c0086c040fd136618992640791de624dce7fc814f55a0d3e0ca7897fb1e` | PASS |
| `gregory-xvi-acta.volume-02.line-00036157` | 1837-12-26 | `la` | 1 | 1 | `70ef7c997f14ed7f749d3cd9c50e579d62dbeea399f2e18fc3226a76cf7e52fc` | PASS |
| `gregory-xvi-acta.volume-02.line-00036237` | 1838-01-18 | `la` | 1 | 1 | `0401d94d8a482eea1e27a5db9eff9d05af251717bece6e975e009ea92a5d5b87` | PASS |
| `gregory-xvi-acta.volume-02.line-00036323` | 1838-01-23 | `la` | 2 | 1, 2 | `55d760c9371df8994d3ea5ab295029eb408cd553abdd9d30ad3931a811ad0d8f` | PASS |
| `gregory-xvi-acta.volume-02.line-00036579` | 1838-02-08 | `la` | 2 | 1, 2 | `4c57aa390ef3d09bf459842c1b1c68527c7e849398392d7269609f1abbe14795` | PASS |

## Page raster digests

| Source ID | Page | PNG SHA-256 | Outcome |
| --- | --- | --- | --- |
| `gregory-xvi-acta.volume-02.line-00027209` | 1 | `8559f7ad703ad96a79acd40dff0e2c220dc8483d8eb7ebc16478e20b42d1a277` | PASS |
| `gregory-xvi-acta.volume-02.line-00027209` | 2 | `8023e570a9ff5842823c819f34f9d412fc80580c3626ee81237d30c6aeeb0b44` | PASS |
| `gregory-xvi-acta.volume-02.line-00027394` | 1 | `2c53189f32592bbc72763375f7f3b2d5e0a1e17fe6c662671a655ee95b9d5bb7` | PASS |
| `gregory-xvi-acta.volume-02.line-00027512.part-01` | 1 | `ea01373b0b0450649a3b0930d5e3a3a3915898ad8a98840d9bc1c8e765a4f67c` | PASS |
| `gregory-xvi-acta.volume-02.line-00027512.part-02` | 1 | `31ea450061294fff0d756bf6b06257e7d4d75633bc326ddaccfb82f5f5fdfcab` | PASS |
| `gregory-xvi-acta.volume-02.line-00027716.part-01` | 1 | `ac2461391ef7c363f2e72dc958aa44aa506d51961162add42c6d55f725b1e971` | PASS |
| `gregory-xvi-acta.volume-02.line-00027716.part-02` | 1 | `0eba89a9ab9ac6c136081ae4616f60c5ccc879f29b655b18d67e2d4c5465121a` | PASS |
| `gregory-xvi-acta.volume-02.line-00027716.part-02` | 2 | `0d6d605c99692c053bfe4116f0a221baa15ee5c9bb74bf05fec590e89a58f3bc` | PASS |
| `gregory-xvi-acta.volume-02.line-00027994` | 1 | `561579e5d4334fa8b6009113ac602a631a916431473c21de7a165dee6f52715b` | PASS |
| `gregory-xvi-acta.volume-02.line-00027994` | 2 | `791bb0df88f5e3c4033af757cc1a12c2782e643ea154b613dc9d501d740dd5b2` | PASS |
| `gregory-xvi-acta.volume-02.line-00027994` | 3 | `dff5cecd497888734a9846a4df3b0c6a843db53dbb626cbd4b9aa6a277f5e907` | PASS |
| `gregory-xvi-acta.volume-02.line-00027994` | 4 | `85b1cdfed9f0d044816b3d30f57e98caca8940c7b77d49b37247cb12313bd929` | PASS |
| `gregory-xvi-acta.volume-02.line-00028557` | 1 | `681d2f3c50daf50f46eedc67e3436072750c506a7359203d8560bdb2483972bb` | PASS |
| `gregory-xvi-acta.volume-02.line-00028834` | 1 | `1f026a792a74f6d54f9c233c07c8fa1833dfc4b80e63b31b67da362bfd401873` | PASS |
| `gregory-xvi-acta.volume-02.line-00028834` | 2 | `8da1340e260a946bd39a0eb8543754be9023781714d3b8d40f9aa2e92cee3d12` | PASS |
| `gregory-xvi-acta.volume-02.line-00029012` | 1 | `9cfce7adda662e16d187485cd83291bfb448ee8d547a4c601a07058d39ebacf3` | PASS |
| `gregory-xvi-acta.volume-02.line-00029485.part-01` | 1 | `fddfdb26f4b4f8a8d2214d5713209aa3c2955ab3cd4f77d85f24c811dcae87a1` | PASS |
| `gregory-xvi-acta.volume-02.line-00029095.part-02` | 1 | `7a9aea2aec88058aeca02c8cda18b10a8dbb82ea1fcf809c069572b8bc98d86f` | PASS |
| `gregory-xvi-acta.volume-02.line-00029095.part-02` | 2 | `56c77af78a2e908eadd093d7a56f5b4bfb08e4fbc4090565226ad692a59ac2c5` | PASS |
| `gregory-xvi-acta.volume-02.line-00029095.part-02` | 3 | `a7aa33d630860ee5c8be210faf8fccc20b7a2d676a8e100897ef960df9fd251d` | PASS |
| `gregory-xvi-acta.volume-02.line-00029485.part-02` | 1 | `580f31b56d1322f196b3d4d507ee5e0019792250bff9e13d0dc4dee3b2ac44ab` | PASS |
| `gregory-xvi-acta.volume-02.line-00029666` | 1 | `542f1965dae501acd512b0810d61a0e47f271830e26d5a631ba09f69321b2e6b` | PASS |
| `gregory-xvi-acta.volume-02.line-00029666` | 2 | `9d83d160736ee189bc4bbda02fc6351117c0f08a28ebd2a5739276def56fed57` | PASS |
| `gregory-xvi-acta.volume-02.line-00029942` | 1 | `ec3bdca9be294f088ce74a33b16e110c0957c659158b2c6feebb18ac915d9640` | PASS |
| `gregory-xvi-acta.volume-02.line-00029942` | 2 | `b1deb75b279be1bc955b8807c28cc47393369af7d89375cc2c449cf5935cd038` | PASS |
| `gregory-xvi-acta.volume-02.line-00030727` | 1 | `351e00bc01321dd88da49b34a93a65d5bee6ad9c5a48388d43ddb0057661de8c` | PASS |
| `gregory-xvi-acta.volume-02.line-00030727` | 2 | `574beff92e99ff93622490a7607b1bea9c0bab8ed2447c6b143d8b6aa6fa5f8b` | PASS |
| `gregory-xvi-acta.volume-02.line-00030892` | 1 | `955bea93d412e89551ae8fae1e8e69f7d1cd2054016f59b35ba8084d792404b5` | PASS |
| `gregory-xvi-acta.volume-02.line-00030966.part-01` | 1 | `e36365cd303111ab7519631983bc03628486b7d0da13fabd6489f856c980f5c8` | PASS |
| `gregory-xvi-acta.volume-02.line-00030966.part-02` | 1 | `7ae2d2fd6a97b75cc575f5edbb7eecd7714873e279790880c9560b3bddd0901c` | PASS |
| `gregory-xvi-acta.volume-02.line-00031091.part-01` | 1 | `35e9d81995b72cde097e41956e23c5a0df38aee90e21d35f351ef9d96d5617b2` | PASS |
| `gregory-xvi-acta.volume-02.line-00031404` | 1 | `b32500cb2bd647901a770205258664b7efad2ce3af998fe0510ad9523a500d04` | PASS |
| `gregory-xvi-acta.volume-02.line-00031488.part-01` | 1 | `8afff598a58f81c33a0f8661f8ba5025aa2849b30df3a0fde7832d1943f1f8fb` | PASS |
| `gregory-xvi-acta.volume-02.line-00031488.part-02` | 1 | `7444a7e25b41b2a4c49d817fbf3330247ca55ea5451eec2cc51d6b21df4c841b` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-04` | 1 | `6031f35b081e8773aaa5d6ea476ae4139a4ccd958710cae5916463f2ba23f204` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-04` | 2 | `610b3995b743ce46cd63811dec425668a1f80acb9dcab9b50b270b2cb51879b9` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-04` | 3 | `2a87decf6bdf593435bbac9ae5912df622cd09887a8b8790599fc3ab82a999a7` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-05` | 1 | `10c22e0bc0b76e3b300f328d303349f5b609f3bade008618446650b0991cea86` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-05` | 2 | `da9709c6b86ace0a8a9d4ea087f7d9d9e6d60b572d1c24ab3f59c05018943861` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-05` | 3 | `3ea220688ac636b6c36eb74d63792209bee3f694832f8d684cb0655aa1d87d71` | PASS |
| `gregory-xvi-acta.volume-02.line-00031836.part-06` | 1 | `c407fe7eef211586e4f9ab2cd6a022742a9d65a96c4bc57f0b19bd6897b559d3` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-01` | 1 | `48da44a1b4acea5317b5f9789bda89febfb65087965524c21b6874bd1e327f2b` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-01` | 2 | `e10e00d9f34dcc636a3d4aaf3bf2cde2b6f4fe4572573451bcab57d389696e49` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-02` | 1 | `36b8de66c914676e365b740b04c68e78c345f1f3656dc1c47a842b7ecd576631` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-02` | 2 | `3203a8742e0ba06efac2ba0da8d018eb5d4b0f42094dedbd41d99421864abe7c` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-02` | 3 | `953ba288871e442a62af155a3d07517e9385e81151342962d1260b40a05b2442` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-02` | 4 | `b6bb6550166f32014daffe67908131d6d2a9263b77fc01a2016a89d8aea9c786` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-03` | 1 | `eef5ddfbe8f2520e57cc6ae2641e2fe106c9402e1d278d4aa8656e49d828c1bf` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-03` | 2 | `1a439229699b50e92fad849f96b1be8e18a44a64017910caaa9b79d7d97382e6` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-04` | 1 | `908eee3dfb0d5604ddd9ca51758c6112d95be270a2331bef0bbf2641beeedaf9` | PASS |
| `gregory-xvi-acta.volume-02.line-00034934.part-04` | 2 | `c97720cb51083d06650eb59355be0f4a6a3ba6aa04e2dc14c772c0d6268fcc01` | PASS |
| `gregory-xvi-acta.volume-02.line-00036157` | 1 | `0036f85da6be9aceaaa2775c173b0b457cc09bf1cb53dc5dbf8eb92975ed9701` | PASS |
| `gregory-xvi-acta.volume-02.line-00036237` | 1 | `60c9c6f70fce9be8b60fed40c28da2cdec7625c798b8fd2f3110b584d6d8e03c` | PASS |
| `gregory-xvi-acta.volume-02.line-00036323` | 1 | `5f2bc7f6c134ea69c69c8ceb9ed4636d8f01978154e40eee7ec5bfe1ccf0ab86` | PASS |
| `gregory-xvi-acta.volume-02.line-00036323` | 2 | `1a267fad79a18a8ccd348c3035b32a4f5359161f286eaf5b5c167274546e8ec4` | PASS |
| `gregory-xvi-acta.volume-02.line-00036579` | 1 | `f05f51de4c6eb5f0773362d652bb6038103127290f289709e877e8db45a6ed8d` | PASS |
| `gregory-xvi-acta.volume-02.line-00036579` | 2 | `3ebfe1efbace38e0163be9f971e15017b6d1cdd4ef7f92ea441926d4963f6992` | PASS |

## Per-document findings

### `gregory-xvi-acta.volume-02.line-00027209`

*Epistola vestra — Augustinianis Calcuttae de vicario apostolico Bengalensi et schismate Meliaporensi* — GREGORIUS PP. XVI. — 1837-01-04 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-01-04, Latin match metadata; address, salutation, two balanced columns, clean gutter/margins; no clipping, tofu, digitizer footer or running head.
- Page 2 (PASS): Single-column continuation to natural close: final blessing and Datum Romae dating clause (die quarta ianuarii 1837, anno sexto), then source note and rights colophon. Source-bearing sparse final page.

### `gregory-xvi-acta.volume-02.line-00027394`

*Pietatem tuam — Vicario capitulari Goano de schismate Meliaporensi* — GREGORIUS PP. XVI. — 1837-01-08 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-01-08, Latin match; address line has OCR noise 'Dilecto filio ch Regan' (literal OCR, limitation); two columns clean; Datum Romae closing then source/rights apparatus. Stray OCR '$' and '|' are literal OCR.

### `gregory-xvi-acta.volume-02.line-00027512.part-01`

*Ex munere pastoralis ministerii — Vicariatus apostolicus insulae Iamaicae cum Bahamis et Honduras erigitur* — GREGORIUS PP. XVI. . ’ — 1837-01-10 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, issuer with stray marks (matches metadata), 1837-01-10, Latin; ad perpetuam rei memoriam protocol; two columns clean; Datum Romae closing then source/rights. Qualification: Non-blocking qualification: issuer line 'GREGORIUS PP. XVI. . ’' carries stray OCR marks and matches frozen metadata.

### `gregory-xvi-acta.volume-02.line-00027512.part-02`

*Literae quas inde — Patriarchae Antiocheno Syrorum de reditu schismaticorum et calendario Gregoriano* — GREGORIUS PP. XVI. — 1837-01-14 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-01-14, Latin match; address/salutation; body in left column continuing to Datum Romae dating clause ending 'anno sexto.' at top of right column, then source/rights apparatus. No clipping or furniture.

### `gregory-xvi-acta.volume-02.line-00027716.part-01`

*Gravissimas inter apostolicae sollicitudinis curas — Monasterium s. Theresiae in Quirinali iurisdictioni cardinalis vicarii subiicitur* — GREGORIUS PP. XVI. — 1837-01-19 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (three lines), GREGORIUS PP. XVI., 1837-01-19, Latin match; ad perpetuam rei memoriam; two columns clean; Datum Romae closing (reads 'anno septimo', literal source/OCR, not inferred) then apparatus. Stray OCR marks (e.g. a copyright sign) are literal OCR.

### `gregory-xvi-acta.volume-02.line-00027716.part-02`

*Cum christianae civilisque reipublicae salus — Coenobium s. Nicolai in Carbonara Ianuae fratribus Scholarum Christianarum attribuitur* — GREGORIUS PP. XVI. — 1837-01-24 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (three lines), GREGORIUS PP. XVI., 1837-01-24, Latin match; protocol; two balanced columns, clean gutter; literal OCR marks ('has*praesentes', 'suffragari®') are OCR limitations.
- Page 2 (PASS): Single-column continuation: non obstantibus clause, Datum Romae dating clause (1837, anno sexto), then source note and rights colophon. Source-bearing sparse final page.

### `gregory-xvi-acta.volume-02.line-00027994`

*In supremo beati Petri — Erectio dioecesis Guayaquilensis in America Meridionali* — GREGORIUS EPISCOPUS — 1837-01-29 — bull — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS EPISCOPUS, 1837-01-29, Latin match; 'servus servorum Dei / ad perpetuam rei memoriam' protocol; two balanced columns, clean gutter and margins; no furniture or digitizer marks.
- Page 2 (PASS): Two-column continuation (parish list, erection clauses); flow continuous, no clipping, overlap or tofu; literal OCR marks ('J[spisapa', stray underscores) are OCR limitations.
- Page 3 (PASS): Two-column continuation (chapter, prebends, seminary); continuous flow; no running heads or fused marginalia; stray '|' is literal OCR.
- Page 4 (PASS): Two columns to executory clauses, Nulli ergo sanction, Datum Romae dating clause (quarto kalendas februarii 1837, anno sexto), then source/rights apparatus in right column.

### `gregory-xvi-acta.volume-02.line-00028557`

*Universi dominici gregis — Iosephus Angelus Fazio visitator et administrator apostolicus Aegypti et Arabiae* — GREGORIUS PP. XVI. — 1837-02-21 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-02-21, Latin match; address/salutation; two columns clean; Datum Romae closing then source note including disclosed literal 'etc.' formula abbreviation, and rights colophon.

### `gregory-xvi-acta.volume-02.line-00028834`

*Religionis propagandae et amplificandae studium — Vicario capitulari Goano de novis vicariatibus apostolicis in Indiis* — ACTA GREGORIL PP, XVI. — 1837-03-10 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, 1837-03-10, Latin match; issuer qualification recorded; two balanced columns, clean gutter; no digitizer footer, running head or fused marginalia in body. Qualification: Non-blocking qualification: displayed issuer 'ACTA GREGORIL PP, XVI.' is an OCR-damaged volume running-title attribution that matches the frozen metadata exactly and still identifies Gregory XVI (applied under the standing Acta-issuer and damaged-spelling rulings; note this act is a papal letter, not an allocution). Body protocol line reads OCR-damaged 'GREGORIUS Pre wv.' (literal OCR).
- Page 2 (PASS): Single-column continuation: decernentes clause, Datum Romae dating clause (decima martii 1837, anno septimo), then source note and rights colophon. Source-bearing sparse final page.

### `gregory-xvi-acta.volume-02.line-00029012`

*Iucundae Nobis fuerunt — Episcopo Marianopolitano de coadiutore et seminario s. Sulpitii* — GREGORIUS PP. XVI. — 1837-03-13 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-03-13, Latin match; address/salutation; left column body; Datum Romae clause continues to top of right column (anno septimo), then apparatus.

### `gregory-xvi-acta.volume-02.line-00029485.part-01`

*Ex pastoralis ministerii munere — Vicariatus apostolicus Guianae Britannicae erigitur* — GREGORIUS PP. XVI. — 1837-04-12 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-04-12, Latin match; protocol; body in left column to Datum Romae dating clause (anno septimo); source note (with disclosed literal 'etc.' abbreviation) flows from left foot to top of right column, then rights colophon. No clipping.

### `gregory-xvi-acta.volume-02.line-00029095.part-02`

*Romani Pontifices sacrarum familiarum — Confirmatio congregationis Oratorii s. Philippi Nerii Catanae* — GREGORIUS PP. XVI. — 1837-04-14 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-04-14, Latin match; ad perpetuam rei memoriam; two dense balanced columns, clean gutter; stray OCR marks ('urb2', '|', 'subia+') are literal OCR.
- Page 2 (PASS): Two-column continuation (indulgences, decernentes, non obstantibus, transumpt clause); continuous flow; no running head, digitizer mark or fused marginal summary.
- Page 3 (PASS): Final page: genuine Datum Romae dating clause (decima quarta aprilis 1837, anno septimo) followed by source note and rights colophon. Sparse source-bearing final page; not apparatus-only.

### `gregory-xvi-acta.volume-02.line-00029485.part-02`

*Singulari, ut nosti — Davidi principi Dyce Sombre de obitu aviae et de rebus Sirdhanae* — GREGORIUS PP. XVI. — 1837-04-22 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-04-22, Latin match; address/salutation; two columns clean; Datum Romae closing (anno septimo) then source/rights apparatus in right column.

### `gregory-xvi-acta.volume-02.line-00029666`

*Dominico gregi — Ecclesia Chiapensis archiepiscopo Mexicano suffraganea restituitur* — GREGORIUS EPISCOPUS — 1837-04-25 — bull — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS EPISCOPUS, 1837-04-25, Latin match; servus servorum Dei / ad perpetuam rei memoriam protocol; two balanced columns; stray '|' and '_' marks are literal OCR; no running head or digitizer mark.
- Page 2 (PASS): Two columns to Nulli ergo sanction and Datum Romae dating clause (septimo kalendas maias 1837, anno septimo), then source/rights apparatus in right column.

### `gregory-xvi-acta.volume-02.line-00029942`

*Ad supremi apostolatus fastigium — Clementi Masson de electione in coadiutorem vicarii apostolici Tunquini Occidentalis* — GREGORIUS PP. XVI. — 1837-05-01 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-05-01, Latin match; address/salutation; two columns; body through the apostolic blessing; clean gutter and margins. Qualification: Non-blocking layout note: right column ends about four-fifths down the page and the dating clause begins page 2 (kept with its notes); no clipping, overlap or loss.
- Page 2 (PASS): Final page: genuine Datum Romae dating clause (die prima maii 1837, anno septimo) and the letter's own two historical citation notes (De civit. Dei; Epist. 32), then source note disclosing retained notes and rights colophon. Source-bearing final page.

### `gregory-xvi-acta.volume-02.line-00030727`

*Cum Romani Pontifices — Mandela vulgo Poggio Mirteto civitatis titulo decoratur* — GREGORIUS PP. XVI. — 1837-05-22 — motu-proprio — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-05-22, Latin match (motu proprio form); protocol; two dense balanced columns; clean gutter and margins; no running head, digitizer mark or fused marginalia.
- Page 2 (PASS): Single-column continuation: derogation clause, Datum Romae dating clause (vigesima secunda maii 1837, anno septimo), then source note and rights colophon. Source-bearing sparse final page.

### `gregory-xvi-acta.volume-02.line-00030892`

*Romanorum indulgentia Pontificum — Cappa violacea dignitatibus et canonicis cathedralis Zacynthiensis* — GREGORIUS PP. XVI. — 1837-05-30 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-05-30, Latin match; protocol; left column body to Datum Romae clause (anno septimo); source note continues to top of right column, then rights colophon. No clipping.

### `gregory-xvi-acta.volume-02.line-00030966.part-01`

*Ex munere pastoralis ministerii — Vicariatus apostolicus Promontorii Bonae Spei erigitur* — GREGORIUS PP. XVI. — 1837-06-06 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-06-06, Latin match; protocol; left column body; Datum Romae clause continues into right column (sexta iunii 1837, anno septimo); source note discloses literal 'etc.' formula; rights colophon.

### `gregory-xvi-acta.volume-02.line-00030966.part-02`

*Pastorale officium — Raymundus Griffith vicarius apostolicus Promontorii Bonae Spei eligitur* — GREGORIUS PP. XVI. — 1837-06-06 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-06-06, Latin match; uppercase address and salutation as transcribed; two columns; Datum Romae clause (die vi iunii MDCCCXxxvn, 'anno v.' literal, not inferred) then source note disclosing the brief is transcribed from the edition's footnote with editor's note number/introduction omitted; rights colophon.

### `gregory-xvi-acta.volume-02.line-00031091.part-01`

*Cum Nobis nihil gratius — Episcopo Papiensi facultas brachium b. Bernardini Tomitani Feltrinis tradendi* — GREGORIUS PP. XVI. — 1837-06-13 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-06-13, Latin match; address/salutation; two columns; Datum Romae closing (decima tertia iunii 1837, anno septimo), then source/rights apparatus. No clipping or furniture.

### `gregory-xvi-acta.volume-02.line-00031404`

*Universi dominici gregis salus — Erectio dioecesis Natchetensis* — GREGORIUS PP. XVI. — 1837-07-28 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (single line), GREGORIUS PP. XVI., 1837-07-28, Latin match; protocol; left column body to Datum Romae apud sanctam Mariam Maiorem clause (anno septimo); source note (disclosed literal 'etc.') continues into right column; rights colophon.

### `gregory-xvi-acta.volume-02.line-00031488.part-01`

*Universi dominici gregis salus — Erectio dioecesis Dubuquensis* — GREGORIUS PP. XVI. — 1837-07-28 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (single line), GREGORIUS PP. XVI., 1837-07-28, Latin match; protocol; left column body to Datum Romae clause (anno septimo); source note continues into right column with disclosed 'etc.'; rights colophon. OCR noise ('rere volumus', 'por anebatut') is literal.

### `gregory-xvi-acta.volume-02.line-00031488.part-02`

*Universi dominici gregis salus — Erectio dioecesis Nashvillensis* — GREGORIUS PP. XVI. — 1837-07-28 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (single line), GREGORIUS PP. XVI., 1837-07-28, Latin match; protocol; left column body to Datum Romae clause (anno septimo); source note continues into right column; rights colophon. No clipping or furniture.

### `gregory-xvi-acta.volume-02.line-00031836.part-04`

*Cum semper in catholica Ecclesia — Martinus de Porres Beati honore decoratur* — GREGORIUS PP. XVI. — 1837-08-08 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-08-08, Latin match; protocol; two dense balanced columns, clean gutter and margins; no running head, digitizer mark or fused marginalia.
- Page 2 (PASS): Two-column continuation (life, virtues, beatification grant, non obstantibus, transumpt clause); continuous flow, clean gutter; no running head, digitizer mark or fused marginalia.
- Page 3 (PASS): Final page: end of transumpt clause, Datum Romae apud sanctam Mariam Maiorem dating clause (octava augusti 1837, anno septimo), then genuine subscriptions 'Loco > signi / Pro dom. card. De Grecorio / A. Picchioni substitutus.' (literal OCR), then source/rights apparatus. Source-bearing final page.

### `gregory-xvi-acta.volume-02.line-00031836.part-05`

*Amantissimus ille humanae dignitatis reparator — Ioannes Massias Beati honore decoratur* — GREGORIUS PP. XVI. — 1837-08-08 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-08-08, Latin match; protocol; two dense balanced columns, clean gutter and margins; literal OCR marks (cent sign, backslash) are OCR limitations.
- Page 2 (PASS): Two-column continuation (virtues, death, causa, beatification grant); continuous flow; no running head, digitizer mark or fused marginalia.
- Page 3 (PASS): Final page: grant clauses, non obstantibus, transumpt clause, Datum Romae dating clause (octava augusti 1837, anno septimo), genuine subscription 'Loco >¥ signi Pro dom. card. Dz GreGortIo A. Picchioni substitutus.' (literal OCR), then source/rights apparatus. Source-bearing final page.

### `gregory-xvi-acta.volume-02.line-00031836.part-06`

*Expositum Nobis nuper fuit — Indulgentiae Filiabus Charitatis s. Vincentii a Paulo in toto Galliarum regno extenduntur* — GREGORIUS PP. XVI. — 1837-08-10 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-08-10, Latin match; protocol; short act set entirely in left column (body, Datum Romae clause decima augusti 1837 anno septimo, source/rights apparatus); right column empty. Natural balance for a short act; no clipping.

### `gregory-xvi-acta.volume-02.line-00034934.part-01`

*Dum intima conficeremur amaritudine — Allocutio de iniuria archiepiscopo Coloniensi illata* — ACTA GREGORII PP. XVI. — 1837-12-10 — consistorial-allocution — Latin. Prior finding: none.

- Page 1 (PASS): Title, 1837-12-10, Latin match; issuer qualification recorded; 'Venerabiles fratres' address; two dense balanced columns, clean gutter; no running head, digitizer mark or fused marginalia. Qualification: Non-blocking qualification: allocution issuer 'ACTA GREGORII PP. XVI.' is the volume running-title attribution and matches the frozen metadata (standing coordinator ruling).
- Page 2 (PASS): Single-column continuation to the allocution's natural close (exhortation to prayer ending 'clementissime propulset.'); an allocution carries no Datum clause; source note discloses that the omitted edition caption supplies the date; rights colophon. Source-bearing final page.

### `gregory-xvi-acta.volume-02.line-00034934.part-02`

*La comunità e popolo di Marino — Chirografo al cardinale Mario Mattei sull’istruzione pubblica di Marino* — GREGORIUS PP. XVI. — 1837-12-12 — chirograph — Multilingual (Italian chirograph with Latin address, protocol and salutation). Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-12-12; language label 'Italian chirograph with Latin address, protocol and salutation' matches 'mul' and source order (Latin address/protocol/salutation then Italian body); two balanced columns; numbered items I./II. preserved; OCR marks ('|'', euro sign for 'e') are literal OCR.
- Page 2 (PASS): Two-column continuation (items III-V, narrative of the reform); continuous flow; no running head, digitizer mark or fused marginalia; OCR noise ('III]', 'VY.', 'pit') is literal.
- Page 3 (PASS): Two-column continuation (rents, legacies, staffing provisions); some short indented fragment lines reflect source line breaks; no clipping, overlap or tofu.
- Page 4 (PASS): Two columns to the derogation clause and the Italian dating clause 'Dato dal Nostro palazzo apostolico Vaticano li 12 decembre 1837.', then source note (discloses Latin protocol preceding Italian text) and rights colophon.

### `gregory-xvi-acta.volume-02.line-00034934.part-03`

*Cum religiosae familiae — Congregatio Camaldulensis Neapolitana iterum constituitur* — GREGORIUS PP. XVI. — 1837-12-19 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-12-19, Latin match; protocol; two dense balanced columns, clean gutter and margins; no running head, digitizer mark or fused marginalia.
- Page 2 (PASS): Single-column continuation: decernentes and non obstantibus clauses, Datum Romae dating clause (decima nona decembris 1837, anno septimo), then source note and rights colophon. Source-bearing final page.

### `gregory-xvi-acta.volume-02.line-00034934.part-04`

*Cum ex pastorali munere — Paroeciae Casumaro pars a dioecesi Mutinensi seiungitur et Bononiensi adiungitur* — GREGORIUS PP. XVI — 1837-12-22 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, issuer 'GREGORIUS PP. XVI' (no final period, matches metadata), 1837-12-22, Latin; protocol; two balanced columns; numbered conditions I.-VIII. preserved as source prints them (OCR 'II.' for III. is literal); clean gutter, no furniture.
- Page 2 (PASS): Two columns to decernentes, non obstantibus and Datum Romae dating clause (vigesima secunda decembris 1837, anno septimo), then source/rights apparatus in right column.

### `gregory-xvi-acta.volume-02.line-00036157`

*Ad acerbissimum quem nuper suscepimus dolorem — Capitulo Coloniensi de archiepiscopo accusato* — GREGORIUS PP. XVI. — 1837-12-26 — papal-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1837-12-26, Latin match; address/salutation; left column body to Datum Romae dating clause (vigesima sexta decembris 1837, anno septimo); source note continues into right column; rights colophon.

### `gregory-xvi-acta.volume-02.line-00036237`

*Singulare ac debitum devotionis Nostrae studium — Capitulo Vaticano binae cruces cum particulis ligni Crucis donantur* — GREGORIUS PP. XVI. — 1838-01-18 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1838-01-18, Latin match; two columns; Datum Romae clause (decima octava ianuarii 1838, anno septimo) at top of right column, then source/rights apparatus. No clipping or furniture.

### `gregory-xvi-acta.volume-02.line-00036323`

*Cum virgines Deo sacrae — Institutum sanctimonialium perpetuae adorationis in monasterio s. Annae Urbis iterum approbatur* — GREGORIUS PP. XVI. — 1838-01-23 — apostolic-letter — Latin. Prior finding: none.

- Page 1 (PASS): Title (three lines), GREGORIUS PP. XVI., 1838-01-23, Latin match; protocol; two dense balanced columns, clean gutter; stray '|' and '_' are literal OCR; no furniture or digitizer marks.
- Page 2 (PASS): Two columns to decernentes, non obstantibus, transumpt clause and Datum Romae dating clause (vigesima tertia ianuarii 1838, anno septimo), then source/rights apparatus in right column.

### `gregory-xvi-acta.volume-02.line-00036579`

*Neminem certe latet — Collegium protonotariorum apostolicorum participantium ad septem restituitur* — GREGORIUS PP. XVI. — 1838-02-08 — apostolic-constitution — Latin. Prior finding: none.

- Page 1 (PASS): Title, GREGORIUS PP. XVI., 1838-02-08, Latin match; protocol; two columns, right column ends ~two-thirds down (non obstantibus and dating clause flow to page 2); clean gutter; euro-sign OCR marks are literal OCR.
- Page 2 (PASS): Single-column continuation: non obstantibus, transumpt clause, Datum Romae dating clause (sexto idus februarii 1838, 'anno octavo' literal, not inferred), then source note and rights colophon. Source-bearing sparse final page.

## Qualifications (non-blocking)

- `gregory-xvi-acta.volume-02.line-00034934.part-01` (allocution, 1837-12-10): issuer line "ACTA GREGORII PP. XVI." is the volume running-title attribution recorded in the frozen metadata; non-blocking under the standing coordinator ruling.
- `gregory-xvi-acta.volume-02.line-00028834` (papal letter, 1837-03-10): displayed issuer "ACTA GREGORIL PP, XVI." is an OCR-damaged running-title attribution that matches the frozen metadata exactly and still identifies Gregory XVI. This act is a letter rather than an allocution, so it is recorded as a qualification under the damaged-spelling ruling; the coordinator may wish to confirm that a running-title attribution is intended for a letter whose body protocol reads "GREGORIUS Pre wv." (literal OCR).
- `gregory-xvi-acta.volume-02.line-00027512.part-01`: issuer line "GREGORIUS PP. XVI. . ’" carries stray OCR marks and matches the frozen metadata.
- `gregory-xvi-acta.volume-02.line-00034934.part-04`: issuer "GREGORIUS PP. XVI" without final period matches the metadata.
- `gregory-xvi-acta.volume-02.line-00034934.part-02`: multilingual label "Italian chirograph with Latin address, protocol and salutation" matches `mul` and the visible source order.
- Sparse final pages in this lane all carry genuine source closing (dating clause, and where printed subscriptions or the letter's own citation notes) before the project apparatus; none is apparatus-only.
- Several readers (for example `line-00030966.part-01`, `line-00031404`, `line-00031488.part-01`, `line-00031488.part-02`) disclose in the source note that the witness abbreviates conventional formulae with literal "etc."; these remain unexpanded as disclosed.
- Regnal-year statements that look internally inconsistent (for example "anno v." on 1837-06-06 and "anno octavo" on 1838-02-08) are literal source/OCR wording; no date was inferred or repaired.

## Limitations

- Text is literal, uncorrected, uncollated historical OCR; odd spellings, stray OCR marks (`|`, `_`, `€`, `¢`, `¥`) and damaged words are recorded as limitations, not defects.
- Layout review only: no word-level collation against the printed witness, no source-fidelity check beyond what is visible, and no historical authentication.
- Dates are compared with the frozen metadata only; no conflicting date was reconciled or inferred.
- No claim of installation, publication or deployment is made.
