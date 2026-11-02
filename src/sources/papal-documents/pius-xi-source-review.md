# Pius XI historical source review

Reviewed on 26 October 2026 (UTC).

This review accounts for every one of the 100 Pius XI records in the captured catalog that offered Latin and carried an act date no later than 31 December 1930. The captured catalog SHA-256 is `241dc8d08b8b402fc81b422c4be774ba291fcd21b1a6dea650628b2a8fec83e9`. Later discoveries are outside this fixed review boundary.

All 100 received an identified contemporary AAS publication witness. Ninety-four new item-specific approvals supplement six Pius XI approvals already present. No item was cleared from its act date alone. Full raw-delivery and approved-text hashes, exact apparatus exclusions, publication locators, and jurisdictional grounds belong to [publication-approvals.json](publication-approvals.json); the governing rights position is [papal-documents-rights-v1.toml](../inventories/papal-documents-rights-v1.toml).

The complete HTML responses and journal PDFs were retrieved mechanically and hashed before extraction. Opening and closing passage fragments were matched within each stated journal extent, with the extracted headings, dating/signature material and terminal apparatus inspected. Source notes and appendices were assessed within those historical extents. These are normalized Vatican web transcriptions; this review is not full image collation, correction of every OCR/transcription error, a diplomatic edition, or an examination of every passage for a downstream doctrinal or legal claim.

The approval transformations remove only exact modern bibliographic blocks or suffixes and their associated title markers. Historical numbered references and appended material remain. A separate exact correction joins the split word in Quas primas on the evidence of the printed page break; it supplies no new letters.

## Controlling historical deliveries

| Printing | Exact delivery SHA-256 | Bytes |
| --- | --- | ---: |
| [AAS 14 (1922)](https://www.vatican.va/archive/aas/documents/AAS-14-1922-ocr.pdf) | `fd00c5d9ad190b3d0da50e15fc26c9250b02858aa48276dc88bb138df99b3ea5` | 3,232,866 |
| [AAS 15 (1923)](https://www.vatican.va/archive/aas/documents/AAS-15-1923-ocr.pdf) | `acab305a3df26a4fe1dfe3c37c9287d8a180b40ba4690a2a2a4239fbb779d33e` | 2,992,828 |
| [AAS 16 (1924)](https://www.vatican.va/archive/aas/documents/AAS-16-1924-ocr.pdf) | `ff70624da45b0b1bbd8700308147bcfdd3082420433b19d8144d26dc220b659d` | 2,486,767 |
| [AAS 17 (1925)](https://www.vatican.va/archive/aas/documents/AAS-17-1925-ocr.pdf) | `c101831ef1fc721d22a890da35ab53b28eb669d553de951a1adcca6f74ef329e` | 3,443,092 |
| [AAS 18 (1926)](https://www.vatican.va/archive/aas/documents/AAS-18-1926-ocr.pdf) | `6d501f9ad97d4dc9a7581e83c6f057fe4e74ec7b0fc55e4530a4da4c66a77c7a` | 2,671,749 |
| [AAS 19 (1927)](https://www.vatican.va/archive/aas/documents/AAS-19-1927-ocr.pdf) | `c28d6baeeca4217355425d884392e68193b08f52e81b7b37c4940cb2a9b784c8` | 2,163,910 |
| [AAS 20 (1928)](https://www.vatican.va/archive/aas/documents/AAS-20-1928-ocr.pdf) | `91fb66fb21c61d26009a58157d47ad6c6956651de1259455f43608c518c053d6` | 2,160,117 |
| [AAS 21 (1929)](https://www.vatican.va/archive/aas/documents/AAS-21-1929-ocr.pdf) | `98b6d3710f1934d977ed141c1e1271958ede5607b579b5e35ccba9897f60625b` | 4,209,603 |
| [AAS 22 (1930)](https://www.vatican.va/archive/aas/documents/AAS-22-1930-ocr.pdf) | `89d2a2036d36c98dd1e217ed1d50d05b68bb0300f08695ddcaca735d0414b20e` | 3,080,361 |

The 1931 volume was also acquired as a boundary check; no approval in this review relies on publication after 1930. AAS 22 (1930), pp. 539–592, supplies the historical publication for Casti connubii despite its last-day-of-year act date.

## Item dispositions

“Existing” means one of the six already admitted Pius XI candidates; “Approved” means a new exact-text approval from this sweep. The displayed text digest is shortened to twelve hexadecimal characters for navigation; the approval record supplies the complete SHA-256. Titles and act dates below retain the captured catalog form, with material conflicts explained afterward.

| Catalog identity | Captured title | Historical publication | Disposition | Approved text SHA-256 prefix |
| --- | --- | --- | --- | --- |
| `papal.pius-xi.hf-p-xi-motu-proprio-19220312-romani-pontificis` | Motu Proprio Romani Pontificis | Acta Apostolicae Sedis 14 (1922), pp. 177-182 | Approved | `1acbacf04839` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19220503-romanorum-pontificum` | Motu Proprio Romanorum Pontificum | Acta Apostolicae Sedis 14 (1922), pp. 321-330 | Approved | `d36a219a4c10` |
| `papal.pius-xi.hf-p-xi-apc-19220725-summorum-pontificum` | Summorum Pontificum | Acta Apostolicae Sedis 14 (1922), pp. 420-422 | Approved | `f002de8fe898` |
| `papal.pius-xi.hf-p-xi-apl-19220801-officiorum-omnium` | Officiorum omnium to Cardinal Gaetano Bisleti concerning seminaries and universities | Acta Apostolicae Sedis 14 (1922), pp. 449-458 | Approved | `3d46d49a4fe8` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19221122-ad-musicae-sacrae` | Motu Proprio Ad Musicae Sacrae | Acta Apostolicae Sedis 14 (1922), pp. 623-626 | Approved | `8337dfb35c35` |
| `papal.pius-xi.hf-p-xi-apc-19221124-de-tulancingo` | De Tulancingo | Acta Apostolicae Sedis 15 (1923), pp. 332-335 | Approved | `db4aaba27af1` |
| `papal.pius-xi.hf-p-xi-apc-19221124-verae-crucis` | Verae crucis | Acta Apostolicae Sedis 15 (1923), pp. 329-332 | Approved | `ccb3c34ebbeb` |
| `papal.pius-xi.hf-p-xi-apl-19221203-meditantibus-nobis` | Meditantibus Nobis on the third centenary of the Canonization of St Ignatius of Loyola and Francis Xavier | Acta Apostolicae Sedis 14 (1922), pp. 627-634 | Approved | `831d0b62b866` |
| `papal.pius-xi.hf-p-xi-enc-19221223-ubi-arcano-dei-consilio` | Ubi Arcano Dei Consilio | Acta Apostolicae Sedis 14 (1922), pp. 673-700 | Existing | `d747db27cce6` |
| `papal.pius-xi.hf-p-xi-enc-26011923-rerum-omnium-perturbationem` | Rerum Omnium Perturbationem | Acta Apostolicae Sedis 15 (1923), pp. 49-63 | Approved | `7dee0b6d089d` |
| `papal.pius-xi.hf-p-xi-apl-19230315-ex-hac-excelsa` | Ex hac excelsa | Acta Apostolicae Sedis 15 (1923), pp. 194-195 | Approved | `38aa58a933bf` |
| `papal.pius-xi.hf-p-xi-apl-19230315-quae-catholico` | Quae catholico | Acta Apostolicae Sedis 15 (1923), pp. 195-196 | Approved | `555cf6c8b945` |
| `papal.pius-xi.hf-p-xi-apl-19230317-romani-pontifices` | Romani Pontifices | Acta Apostolicae Sedis 15 (1923), pp. 196-197 | Approved | `0984ce46c69e` |
| `papal.pius-xi.hf-p-xi-apl-19230324-monasterium-speinshartense` | Monasterium Speinshartense | Acta Apostolicae Sedis 15 (1923), pp. 197-199 | Approved | `c053692d98df` |
| `papal.pius-xi.hf-p-xi-apl-19230413-romanorum-pontificum` | Romanorum Pontificum | Acta Apostolicae Sedis 15 (1923), pp. 200-201 | Approved | `bc961220b051` |
| `papal.pius-xi.hf-p-xi-apl-19230419-quae-catholico` | Quae catholico | Acta Apostolicae Sedis 15 (1923), pp. 201-202 | Approved | `09536ae7636f` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19230420-post-datam` | Motu Proprio Post datam | Acta Apostolicae Sedis 15 (1923), pp. 193-194 | Approved | `edf01e8a7174` |
| `papal.pius-xi.hf-p-xi-apl-19230429-quod-ioannes` | Quod Ioannes | Acta Apostolicae Sedis 15 (1923), pp. 202-207 | Approved | `6ad80bccdb4e` |
| `papal.pius-xi.hf-p-xi-apl-19230504-cum-ex-apostolico` | Cum ex apostolico | Acta Apostolicae Sedis 15 (1923), pp. 335-336 | Approved | `cc5bf3ea6d76` |
| `papal.pius-xi.hf-p-xi-apl-19230504-ex-hac-sublimi` | Ex hac sublimi | Acta Apostolicae Sedis 15 (1923), pp. 336-337 | Approved | `338631acd158` |
| `papal.pius-xi.hf-p-xi-apl-19230611-iam-inde` | Iam inde | Acta Apostolicae Sedis 15 (1923), pp. 337-338 | Approved | `ddc09978c1cd` |
| `papal.pius-xi.hf-p-xi-apl-19230611-venerabilis-frater` | Venerabilis frater | Acta Apostolicae Sedis 15 (1923), pp. 338-339 | Approved | `10c4890a22e3` |
| `papal.pius-xi.hf-p-xi-enc-19230629-studiorum-ducem` | Studiorum Ducem | Acta Apostolicae Sedis 15 (1923), pp. 309-326 | Approved | `951c5ea1844d` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19230629-orbem-catholicum` | Motu Proprio Orbem catholicum | Acta Apostolicae Sedis 15 (1923), pp. 327-329 | Approved | `e323c2281a3b` |
| `papal.pius-xi.hf-p-xi-enc-19231112-ecclesiam-dei` | Ecclesiam Dei | Acta Apostolicae Sedis 15 (1923), pp. 573-582 | Approved | `1ba1818d7fd3` |
| `papal.pius-xi.hf-p-xi-enc-18011924-maximam-gravissimamque` | Maximam Gravissimamque | Acta Apostolicae Sedis 16 (1924), pp. 5-11 | Approved | `54a5bd0a1c9b` |
| `papal.pius-xi.hf-p-xi-apl-19240319-unigenitus-dei` | Unigenitus Dei on the criteria for the formation of clergy | Acta Apostolicae Sedis 16 (1924), pp. 133-148 | Approved | `be06c28bbc29` |
| `papal.pius-xi.hf-p-xi-apc-19240708-umbratilem` | Umbratilem | Acta Apostolicae Sedis 16 (1924), pp. 385-391 | Approved | `4808a8b820df` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19241020-litterarum-latinarum` | Motu Proprio Latinarum litterarum | Acta Apostolicae Sedis 16 (1924), pp. 417-420 | Approved | `65bfff1647f5` |
| `papal.pius-xi.hf-p-xi-apl-19250531-beatus-vianney` | Christi nomen, Decretal Letter | Acta Apostolicae Sedis 17 (1925), pp. 465-481 | Approved | `d0b7eda149e3` |
| `papal.pius-xi.hf-p-xi-enc-11121925-quas-primas` | Quas Primas | Acta Apostolicae Sedis 17 (1925), pp. 593-610 | Existing | `549b7a6e70f9` |
| `papal.pius-xi.hf-p-xi-apl-19260202-paterna-sane-sollicitudo` | Paterna Sane to Bishops, clergy and people of Mexico on the conditions of Mexico | Acta Apostolicae Sedis 18 (1926), pp. 175-179 | Approved | `430e730155db` |
| `papal.pius-xi.hf-p-xi-enc-19260228-rerum-ecclesiae` | Rerum Ecclesiae | Acta Apostolicae Sedis 18 (1926), pp. 65-83 | Existing | `482bb54a7c78` |
| `papal.pius-xi.hf-p-xi-enc-19260430-rite-expiatis` | Rite Expiatis | Acta Apostolicae Sedis 18 (1926), pp. 153-175 | Approved | `bf0c065ced51` |
| `papal.pius-xi.hf-p-xi-apl-19260613-singulare-illud` | Singulare Illud on Saint Aloysius Gonzaga, Patron of Catholic Youth | Acta Apostolicae Sedis 18 (1926), pp. 258-267 | Approved | `ec5f6ab84058` |
| `papal.pius-xi.hf-p-xi-enc-18111926-iniquis-afflictisque` | Iniquis Afflictisque | Acta Apostolicae Sedis 18 (1926), pp. 465-477 | Approved | `ff8e940d1ac5` |
| `papal.pius-xi.hf-p-xi-enc-19280106-mortalium-animos` | Mortalium Animos | Acta Apostolicae Sedis 20 (1928), pp. 5-16 | Existing | `74ed5b789c36` |
| `papal.pius-xi.hf-p-xi-apc-19280119-apostolici-officii` | Apostolici officii | Acta Apostolicae Sedis 21 (1929), pp. 97-98 | Approved | `9e7df9eb470e` |
| `papal.pius-xi.hf-p-xi-enc-19280508-miserentissimus-redemptor` | Miserentissimus Redemptor | Acta Apostolicae Sedis 20 (1928), pp. 165-179 | Existing | `dc6d503e2be7` |
| `papal.pius-xi.hf-p-xi-apl-19280711-decessor-noster` | Decessor Noster | Acta Apostolicae Sedis 21 (1929), pp. 99-100 | Approved | `035972fd2acf` |
| `papal.pius-xi.hf-p-xi-apl-19280711-dilectus-filius` | Dilectus filius | Acta Apostolicae Sedis 21 (1929), pp. 101-103 | Approved | `08271c9172d9` |
| `papal.pius-xi.hf-p-xi-apl-19280711-friburgensis-archidioecesis` | Friburgensis archidioecesis | Acta Apostolicae Sedis 21 (1929), pp. 100-101 | Approved | `bdb8a2e1dec6` |
| `papal.pius-xi.hf-p-xi-apl-19280712-cum-tu` | Cum tu | Acta Apostolicae Sedis 21 (1929), pp. 177-178 | Approved | `74aba1d37b0b` |
| `papal.pius-xi.hf-p-xi-apl-19280718-per-similes` | Per similes | Acta Apostolicae Sedis 21 (1929), pp. 178-179 | Approved | `3ad865aba0d8` |
| `papal.pius-xi.hf-p-xi-apl-19280718-quum-ex` | Quum ex Apostolico | Acta Apostolicae Sedis 21 (1929), p. 180 | Approved | `cb29a9acb34b` |
| `papal.pius-xi.hf-p-xi-apl-19280719-ex-hac` | Ex hac | Acta Apostolicae Sedis 21 (1929), pp. 181-182 | Approved | `fb29263e826c` |
| `papal.pius-xi.hf-p-xi-apl-19280802-inter-praestantiores` | Inter praestantiores | Acta Apostolicae Sedis 21 (1929), pp. 182-183 | Approved | `37ee85bbb230` |
| `papal.pius-xi.hf-p-xi-apl-19280815-providentia-opportuna` | Providentia opportuna | Acta Apostolicae Sedis 21 (1929), pp. 12-21 | Approved | `79e65c60069c` |
| `papal.pius-xi.hf-p-xi-apl-19280824-leodiensis-dioecesis` | Leodiensis dioecesis | Acta Apostolicae Sedis 21 (1929), pp. 183-185 | Approved | `ce8aceddb00d` |
| `papal.pius-xi.hf-p-xi-apl-19280829-sagiensis-dioecesis` | Sagiensis dioecesis | Acta Apostolicae Sedis 21 (1929), pp. 545-546 | Approved | `e3ddf9f96899` |
| `papal.pius-xi.hf-p-xi-enc-19280908-rerum-orientalium` | Rerum Orientalium | Acta Apostolicae Sedis 20 (1928), pp. 277-288 | Approved | `59210881c709` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19280914-motuproprio-quod-maxime` | Motu Proprio Quod Maxime | Acta Apostolicae Sedis 20 (1928), pp. 309-315 | Approved | `b4ca79bfd229` |
| `papal.pius-xi.hf-p-xi-apl-19281015-commissum-nobis` | Commissum nobis | Acta Apostolicae Sedis 21 (1929), pp. 548-549 | Approved | `e932204d0913` |
| `papal.pius-xi.hf-p-xi-apl-19281015-praedecessor-noster` | Praedecessor noster | Acta Apostolicae Sedis 21 (1929), pp. 549-550 | Approved | `e881d7a4a5c4` |
| `papal.pius-xi.hf-p-xi-apc-19281220-divini-cultus-sanctitatem` | Divini cultus sanctitatem | Acta Apostolicae Sedis 21 (1929), pp. 33-41 | Approved | `fa41170a8efd` |
| `papal.pius-xi.hf-p-xi-apc-19290106-auspicantibus-nobis` | Auspicantibus Nobis on the occasion of the Extraordinary Jubilee of the Year 1929 | Acta Apostolicae Sedis 21 (1929), pp. 5-11 | Approved | `20aeaf64d28b` |
| `papal.pius-xi.hf-p-xi-apl-19290125-litteris-apostolicis` | Litteris Apostolicis | Acta Apostolicae Sedis 21 (1929), pp. 581-582 | Approved | `d9e0e136851d` |
| `papal.pius-xi.hf-p-xi-apl-19290206-missionariorum-filiorum` | Missionariorum filiorum | Acta Apostolicae Sedis 21 (1929), pp. 551-552 | Approved | `ffa22a7e944f` |
| `papal.pius-xi.hf-p-xi-apl-19290208-ex-apostolico-munere` | Ex Apostolico munere | Acta Apostolicae Sedis 21 (1929), pp. 552-553 | Approved | `b985b8766584` |
| `papal.pius-xi.hf-p-xi-apl-19290211-peruvianis-in-finibus` | Peruvianis in finibus | Acta Apostolicae Sedis 21 (1929), pp. 582-583 | Approved | `dc07ed6222d9` |
| `papal.pius-xi.hf-p-xi-apl-19290215-in-longinquis` | In longinquis latisque | Acta Apostolicae Sedis 21 (1929), pp. 584-585 | Approved | `43a09d1e1ae6` |
| `papal.pius-xi.hf-p-xi-apl-19290220-faesulanae-dioecesis` | Faesulanae dioecesis | Acta Apostolicae Sedis 21 (1929), pp. 587-588 | Approved | `7f9e6c2d7eb0` |
| `papal.pius-xi.hf-p-xi-apl-19290220-pastorale-officium` | Pastorale officium | Acta Apostolicae Sedis 21 (1929), pp. 553-554 | Approved | `433022346a34` |
| `papal.pius-xi.hf-p-xi-apl-19290220-ut-evangelium` | Ut evangelium | Acta Apostolicae Sedis 21 (1929), pp. 585-586 | Approved | `86083d88a2fe` |
| `papal.pius-xi.hf-p-xi-apl-19290221-ea-quae` | Ea, quae catholicae | Acta Apostolicae Sedis 21 (1929), p. 590 | Approved | `5e56a84ed6f5` |
| `papal.pius-xi.hf-p-xi-apl-19290221-ut-aucto` | Ut, aucto | Acta Apostolicae Sedis 21 (1929), pp. 589-590 | Approved | `20587376f75b` |
| `papal.pius-xi.hf-p-xi-apl-19280918-monasterii-sanctae` | Monasterii Sancti Benedicti | Acta Apostolicae Sedis 21 (1929), pp. 547-548 | Approved | `f714dd398512` |
| `papal.pius-xi.hf-p-xi-apl-19290304-caritatem-docet` | Caritatem docet | Acta Apostolicae Sedis 21 (1929), pp. 129-137 | Approved | `5986b0432a93` |
| `papal.pius-xi.hf-p-xi-apl-19290310-archiepiscopali-in-urbe` | Archiepiscopali in urbe | Acta Apostolicae Sedis 21 (1929), pp. 592-593 | Approved | `ac00898115d7` |
| `papal.pius-xi.hf-p-xi-apl-19290317-litteris-apostolicis` | Litteris apostolicis nostris | Acta Apostolicae Sedis 21 (1929), pp. 593-594 | Approved | `2bbb3c36232d` |
| `papal.pius-xi.hf-p-xi-apl-19290318-cum-vicarius` | Cum vicarius apostolicus | Acta Apostolicae Sedis 21 (1929), pp. 594-595 | Approved | `59fac7a357b2` |
| `papal.pius-xi.hf-p-xi-apl-19290330-ad-animorum` | Ad animorum bonum | Acta Apostolicae Sedis 21 (1929), pp. 595-596 | Approved | `04a8ab9cca9c` |
| `papal.pius-xi.hf-p-xi-apl-19290408-ad-fidem` | Ad fidem catholicam | Acta Apostolicae Sedis 21 (1929), pp. 622-623 | Approved | `5247e6363786` |
| `papal.pius-xi.hf-p-xi-apl-19290410-litteris-apostolicis` | Litteris Apostolicis Nostris | Acta Apostolicae Sedis 21 (1929), pp. 623-624 | Approved | `902a59e3c0e8` |
| `papal.pius-xi.hf-p-xi-apl-19290415-quod-christiani` | Quod christiani | Acta Apostolicae Sedis 21 (1929), pp. 652-653 | Approved | `e37073a3a190` |
| `papal.pius-xi.hf-p-xi-apl-19290416-ut-aucto` | Ut, aucto pastorum | Acta Apostolicae Sedis 21 (1929), pp. 653-654 | Approved | `a06d967c2a98` |
| `papal.pius-xi.hf-p-xi-apl-19290423-anno-iubilari` | Anno Iubilari | Acta Apostolicae Sedis 21 (1929), pp. 312-313 | Approved | `d9b76f397513` |
| `papal.pius-xi.hf-p-xi-apl-19290430-litteris-apostolicis` | Litteris Apostolicis | Acta Apostolicae Sedis 21 (1929), pp. 554-557 | Approved | `96366cb459a2` |
| `papal.pius-xi.hf-p-xi-apl-19290508-quantopere-nobis` | Quantopere nobis | Acta Apostolicae Sedis 21 (1929), pp. 654-655 | Approved | `af58572b5c9d` |
| `papal.pius-xi.hf-p-xi-apl-19290524-quae-catholicae` | Quae catholicae | Acta Apostolicae Sedis 21 (1929), pp. 656-657 | Approved | `0d8de04a43b8` |
| `papal.pius-xi.hf-p-xi-apl-19290524-quod-nobis` | Quod nobis | Acta Apostolicae Sedis 21 (1929), pp. 655-656 | Approved | `625c49f7cba1` |
| `papal.pius-xi.hf-p-xi-apl-19290525-cum-venerabilis` | Cum venerabili frater | Acta Apostolicae Sedis 21 (1929), pp. 658-659 | Approved | `60afe38be3d0` |
| `papal.pius-xi.hf-p-xi-apl-19290525-nobis-ex` | Nobis ex alto | Acta Apostolicae Sedis 21 (1929), pp. 657-658 | Approved | `a7b5074f8174` |
| `papal.pius-xi.hf-p-xi-apl-19290602-mirabilis-deus` | Mirabilis Deus | Acta Apostolicae Sedis 21 (1929), pp. 313-318 | Approved | `ba692c5493d6` |
| `papal.pius-xi.hf-p-xi-apl-19290606-cum-ex` | Cum ex apostolico | Acta Apostolicae Sedis 21 (1929), pp. 659-660 | Approved | `337c443bb569` |
| `papal.pius-xi.hf-p-xi-apl-19290608-edocet-nos` | Edocet Nos | Acta Apostolicae Sedis 21 (1929), pp. 660-661 | Approved | `5a284bcc4bf3` |
| `papal.pius-xi.hf-p-xi-apl-19290609-decor-carmeli` | Decor Carmeli | Acta Apostolicae Sedis 21 (1929), pp. 473-477 | Approved | `842ce3924eb5` |
| `papal.pius-xi.hf-p-xi-apl-19290614-edocet-nos` | Edocet Nos | Acta Apostolicae Sedis 21 (1929), pp. 661-662 | Approved | `5d321d3281fa` |
| `papal.pius-xi.hf-p-xi-apl-19290616-ardenti-amore` | Ardenti amore | Acta Apostolicae Sedis 21 (1929), pp. 477-481 | Approved | `cb9ba1f87471` |
| `papal.pius-xi.hf-p-xi-apl-19290619-buscoducensi` | Buscoducensi | Acta Apostolicae Sedis 21 (1929), pp. 662-663 | Approved | `57ed37fee029` |
| `papal.pius-xi.hf-p-xi-apl-19290623-martyrum-corona` | Martyrum corona | Acta Apostolicae Sedis 21 (1929), pp. 482-485 | Approved | `dce4ee46b863` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19290624-decessor-noster` | Motu Proprio Decessor Noster | Acta Apostolicae Sedis 21 (1929), pp. 342-345 | Approved | `47c4dfe60932` |
| `papal.pius-xi.hf-p-xi-motu-proprio-19290624-vix-ad-summi` | Motu Proprio Vix ad summi Pontificatus | Acta Apostolicae Sedis 21 (1929), pp. 345-349 | Approved | `dc6fcd7f6e33` |
| `papal.pius-xi.hf-p-xi-apl-19290623-mites-corde` | Mites corde | Acta Apostolicae Sedis 21 (1929), pp. 485-488 | Approved | `48ec625e3f09` |
| `papal.pius-xi.hf-p-xi-apc-19290815-quam-curam` | Quam curam | Acta Apostolicae Sedis 21 (1929), pp. 577-581 | Approved | `1171950069eb` |
| `papal.pius-xi.hf-p-xi-enc-19291220-mens-nostra` | Mens Nostra | Acta Apostolicae Sedis 21 (1929), pp. 689-706 | Approved | `fa36236e4499` |
| `papal.pius-xi.hf-p-xi-enc-19291223-quinquagesimo-ante-anno` | Quinquagesimo Ante Anno | Acta Apostolicae Sedis 21 (1929), pp. 707-722 | Approved | `8ae7fe6b7d55` |
| `papal.pius-xi.hf-p-xi-enc-31121929-divini-illius-magistri` | Divini Illius Magistri | Acta Apostolicae Sedis 22 (1930), pp. 49-86 | Existing | `ee8eba55a119` |
| `papal.pius-xi.hf-p-xi-enc-19300420-ad-salutem-humani` | Ad Salutem Humani | Acta Apostolicae Sedis 22 (1930), pp. 201-234 | Approved | `3b09c259119e` |
| `papal.pius-xi.hf-p-xi-enc-19301231-casti-connubii` | Casti Connubii | Acta Apostolicae Sedis 22 (1930), pp. 539-592 | Approved | `2f2ca21a525d` |

## Identified source discrepancies and extent

- `papal.pius-xi.hf-p-xi-motu-proprio-19220312-romani-pontificis`: The historical Index clericorum conclavistarum following the signature is retained; the publication extent includes that list through p. 182.
- `papal.pius-xi.hf-p-xi-motu-proprio-19220503-romanorum-pontificum`: For the motu proprio of 3 May 1922, the historical statutes following the signature are retained within its printed pp. 321-330 extent.
- `papal.pius-xi.hf-p-xi-apc-19221124-de-tulancingo`: The modern web note begins its range at p. 322; the act actually begins at p. 332 in AAS 15 (1923) and ends p. 335. The excluded web citation is a finding aid, not the controlling pagination.
- `papal.pius-xi.hf-p-xi-apc-19221124-verae-crucis`: The web transcription contains embedded printed running-head material inside its body paragraph; it is retained as supplied, not silently corrected.
- `papal.pius-xi.hf-p-xi-apl-19230324-monasterium-speinshartense`: The web transcription contains embedded printed running-head material around pages 198-199 and a stray asterisk inside its long body paragraph; these are retained as supplied, not silently corrected.
- `papal.pius-xi.hf-p-xi-enc-19231112-ecclesiam-dei`: The web dating clause reads MDCCCCXVIII although the contemporary AAS 15 (1923) act and index identify 12 November 1923. The web transcription error is preserved and not treated as a new date for the act.
- `papal.pius-xi.hf-p-xi-apc-19240708-umbratilem`: The referenced Carthusian Statuta appear only as a short prologue/excerpt followed by an omission formula in AAS 16 p. 390 and this web delivery. This reading edition does not provide the complete Statuta.
- `papal.pius-xi.hf-p-xi-enc-11121925-quas-primas`: The exact adjacent web blocks C / hristo are joined without a separator on the evidence of AAS 17 pp. 608-609; the correction has a separate exact approval.
- `papal.pius-xi.hf-p-xi-apl-19260202-paterna-sane-sollicitudo`: The Latin act includes an Italian letter of Cardinal Gasparri dated 5 September 1924, printed with the act on AAS 18 p. 179. The separate Spanish reply beginning p. 180 is absent from the web delivery. Historical asterisk cross-references to that annex are retained.
- `papal.pius-xi.hf-p-xi-apl-19280829-sagiensis-dioecesis`: The modern web note gives pp. 546-547; the act begins p. 545 and ends p. 546 in AAS 21 (1929).
- `papal.pius-xi.hf-p-xi-apc-19290106-auspicantibus-nobis`: The modern web note gives volume XXII for 1929 and pp. 6-11; the contemporary witness is AAS 21 (1929), pp. 5-11. The source act text and signature identify the work.
- `papal.pius-xi.hf-p-xi-apl-19290206-missionariorum-filiorum`: The modern web note gives pp. 550-551; the act begins p. 551 and ends p. 552 in AAS 21 (1929).
- `papal.pius-xi.hf-p-xi-apl-19290220-pastorale-officium`: The source index and filename suggest 20 February 1929, but both the Latin body and AAS 21 (1929), p. 554 print 8 February 1929. The act concerns Brazzaville and Ubanghi Chari.
- `papal.pius-xi.hf-p-xi-apl-19280918-monasterii-sanctae`: The English/Italian index association supplies another act title and 23 February 1929; this Latin delivery is Monasterii Sanctae Mariae, dated 18 September 1928 in its signature and AAS 21 (1929), p. 548.
- `papal.pius-xi.hf-p-xi-apl-19290304-caritatem-docet`: The modern web source citation incorrectly identifies AAS 14 (1922), pp. 627-634; direct incipit, body and signature matching identifies AAS 21 (1929), pp. 129-137. The modern citation is excluded; source transcription errors including 2*e are preserved.

Several 1923 web bibliographic notes print volume XIV while naming the year 1923. The actual historical deliveries are AAS 15 (1923). Other notes divide page numbers across HTML blocks or truncate them; the historical folios in the table come from the identified journal bounds, rather than an unchecked transcription of those notes.

For Rerum Ecclesiae, the long paragraph beginning “At si curandum” occurs once in both the retained source artifact and AAS 18 (1926), pp. 76–77. Its continuation across a column or page is not grounds to delete text.

The distinction between original historical wording, later web presentation, source transcription defects, and the project’s own apparatus remains explicit. No worldwide public-domain claim, blanket Vatican permission, or complete historical papal corpus claim follows from this review.

## Supplemental Latin-only discovery

After the fixed 100-item snapshot, the Latin index supplied `papal.pius-xi.hf-p-xi-apl-19290223-monasterii-sancti`. Its original Latin opening, Ilbenstadt subject, and signature match AAS 21 (1929), pp. 591–592; the act is dated 23 February 1929. It is distinct from the Colwich act Monasterii Sanctae Mariae dated 18 September 1928. A separate exact approval admits this additional historical text (approved text SHA-256 `f6789b3ae4cbf5cacb574d922e520b0ac0a495b2894a5c3947463b3ae6a9dc16`). This supplement brings the review to 101 identified works: 95 new approvals and six previously approved Pius XI works.

## Superseding publication review: Casti connubii

**26 October 2026: the Casti connubii distribution approval above is reopened.** Its AAS 22 (1930) volume citation and 31 December 1930 act date do not establish actual publication before 1931. The earlier eligible-publication assumption, its approval row, and the resulting totals are superseded for this item. Within the fixed 100-item sweep, 99 retain an affirmative assessment and one is reopened; including the supplemental Ilbenstadt act, 100 retain an affirmative assessment and one is reopened.

The [complete Vatican AAS 22 delivery](https://www.vatican.va/archive/aas/documents/AAS-22-1930-ocr.pdf), SHA-256 `89d2a2036d36c98dd1e217ed1d50d05b68bb0300f08695ddcaca735d0414b20e`, distinguishes three facts: issue 13 has its nominal 31 December 1930 masthead at p. 529 and contains Casti at pp. 539–592; issue 14 also carries that nominal date at p. 593; the annual-volume colophon at p. 652 states completion on 20 January 1931. The colophon does not establish that every earlier separately issued fascicle first appeared in 1931.

An [actual microfilm-image copy of issue 13](https://archive.org/details/sim_acta-apostolicae-sedis_1930-12-31_22_13) was acquired in full: 69 PDF pages, 14,960,211 bytes, SHA-256 `8be40cc41ab2fee3853c4a0fd5669d83a276e284b9248863c87d8c67ae2ce25b`. Its cover, issue index and masthead identify the nominal issue; no independent release or dispatch date was established from this delivery. A nominal issue date is not being promoted into proof of actual first publication.

Contemporary reporting points to January 1931. [The Spectator, 17 January 1931, p. 3, “The Encyclical on Marriage”](https://archive.spectator.co.uk/article/17th-january-1931/3/the-encyclical-on-marriage-the-papal-encyclical-up) expressly reports publication on Thursday, 8 January, and identifies the document by its incipit. An [AP report carried on the Manchester Evening Herald front page of 8 January 1931](https://cdn.manchesterhistory.org/News/Manchester%20Evening%20Hearld_1931-01-08.pdf), under its Vatican City dateline that day, likewise presents the marriage encyclical as newly issued. These reports support a January public release; they do not prove that no earlier Latin printing existed. The Spectator article was read through the web research tool, but direct HTML acquisition returned an empty response and its image endpoint returned 403; direct acquisition of the Manchester PDF also returned 403. No acquired-byte hashes are asserted for those press deliveries.

The contrary [Open Library Paulist Press catalog row](https://openlibrary.org/books/OL21501095M) assigns 1930 to an English edition, on University of Toronto catalog provenance. Its physical title/imprint and distribution were not verified. That catalog date supplies a lead, not a resolution of the Latin publication conflict. The examined source families were the complete Vatican annual delivery, actual issue microfilm and wrapper, contemporary press, institutional-derived edition metadata, and a bounded Internet Archive edition search. No verified pre-1931 publication witness was found within that scope.

The current disposition is therefore **publication basis unresolved: retain metadata, withhold the full source body and its PDF/TeX derivatives from Git and public output** until a pre-1931 printing/distribution witness or another affirmative distribution basis is established. The act date remains 31 December 1930. This is a correction to one artifact’s clearance, not a claim that the volume colophon dates all earlier 1930 issue bodies.
