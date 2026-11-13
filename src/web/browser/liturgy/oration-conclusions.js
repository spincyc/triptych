/* Source-controlled conclusion groups. Formula bodies stay in generated data;
 * this mechanically checked map contains only finite descriptor fingerprints. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TriptychOrationConclusions = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const METHOD_ID = 'roman-1962-rg115-conclusion-execution-20261112';
  const V2_METHOD_ID = 'missal-finite-oration-conclusion-execution-20261112-v2';
  const GROUP_RULE = 'RGMR 436-437; 442-443; 480; 505';
  // This exact authority is activated by its adjacent root-adoption record.
  const ACTIVE_AUTHORITY_SHA256 = 'b26fe7863979e300ea47ad925e22d77d783dd76a418672b516eba73cac166744';
  // BEGIN GENERATED CONCLUSION PINS — derived from the single finite authority.
  const GENERATED_AUTHORITY_SHA256 = "b26fe7863979e300ea47ad925e22d77d783dd76a418672b516eba73cac166744";
  const PUBLIC_PINS = Object.freeze({
  "[\"advent-1\",\"main\",\"Postcommunion\",\"all\",1]": "9d8c3de90fe2ba0f9f24b5009e1754535dd0db659e711964ef462341c4110171",
  "[\"advent-2\",\"main\",\"Postcommunion\",\"all\",1]": "df5f2fab381f6162b102734c5a7a9d846bd7137c6c1cc21bc3539b9eb043fe60",
  "[\"advent-2\",\"main\",\"Secret\",\"all\",1]": "abb1983c934f4d24505ae7213c05795c697b6dd112e410f19c0b1bcf00da85d7",
  "[\"advent-3\",\"main\",\"Collect\",\"all\",1]": "b88f3b9b6b876eb35b2826e76f2bc418e1cd97e1537f64321d75e57778ddd04d",
  "[\"advent-3\",\"main\",\"Postcommunion\",\"all\",1]": "aa9d9487e5c5e8ef02aff43e26717d11e0bf38549a3ec3e3889bed62b10ef9ec",
  "[\"advent-3\",\"main\",\"Secret\",\"all\",1]": "849727beface9ca84495f547c07b9f8ecc225a61d02cbaead5dd5a00234e5c29",
  "[\"advent-4\",\"main\",\"Collect\",\"all\",1]": "ee87922a29df93c8365bf229523c225bd196ce7832402231aca9bb6883fd72f1",
  "[\"advent-4\",\"main\",\"Postcommunion\",\"all\",1]": "3116163a0b1e5ec7c58a50fb4fd7ff03f6069a20d176da9278c3df2b9f05696b",
  "[\"advent-4\",\"main\",\"Secret\",\"all\",1]": "d4bebe3b02e6c39c61fcf3f2986abb1f1c57c737fa2d507b6c0d4ef59151c60e",
  "[\"advent-ember-friday\",\"main\",\"Collect\",\"all\",1]": "ff4d03dd1677f52ce06e8b9e1d310d9ea044f30b3bed6de5fb6ee57b799d6a65",
  "[\"advent-ember-friday\",\"main\",\"Postcommunion\",\"all\",1]": "525d435b9674fdfb3a37808bc3732ef3b32a7ba726def42a99f5155fc65db4f0",
  "[\"advent-ember-wednesday\",\"main\",\"Collect\",\"all\",1]": "4689174ef9ef01967128553417ac5f910d79a390003ad1518bec4b0385a9887b",
  "[\"advent-ember-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "247c371a88e52c4534a387b923249289978b2d51d9030437459ff0259f6faec7",
  "[\"advent-ember-wednesday\",\"main\",\"Secret\",\"all\",1]": "d075405b8c4eba58a7f18b2a92a5291b99c8c6a208d3d41d5eec384e8bd7a6bb",
  "[\"apparitione-beatae-mariae-virginis-immaculatae\",\"main\",\"Collect\",\"all\",1]": "5e4670f4fdf9dcd4cfce17133785748581a76627883d8e249ba0d3d2e9c5b55b",
  "[\"apparitione-beatae-mariae-virginis-immaculatae\",\"main\",\"Postcommunion\",\"all\",1]": "480608463dc51d75019044d83908d395b557d787d4c1c663c4f1221840c39ffd",
  "[\"apparitione-beatae-mariae-virginis-immaculatae\",\"main\",\"Secret\",\"all\",1]": "7890a88d95b2594d3e151a10f1336b26a96f2dd309aaba61f786262447ae04f6",
  "[\"ascension\",\"main\",\"Collect\",\"all\",1]": "316f7e9ef4ce24d691865e610582221d307695e225280131fe3606355b564a76",
  "[\"ascension\",\"main\",\"Postcommunion\",\"all\",1]": "9dab2d9fa1884cc2b9734bd07bfdc5af0ec07f6ae4debd1f393077f59ecd656e",
  "[\"ascension\",\"main\",\"Secret\",\"all\",1]": "6817a7ec78d096d1a323571545f6c112fa2409e621e54133e5ed98bd2c925035",
  "[\"ash-wednesday\",\"main\",\"Collect\",\"all\",1]": "9f2076cf7af4e7017d75e1a45c718df8d20b0e660c4b87b34b46610eca3545f4",
  "[\"ash-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "f9ee271351bfac7e2c5305c5dfddc7fe7a773cdb85527bd3fec066f95911da9a",
  "[\"ash-wednesday\",\"main\",\"Secret\",\"all\",1]": "18ff94d3398723fd07a799dd664f0d130d8236ece0e3759d5d2c341fe696b349",
  "[\"beatae-mariae-virginis-a-rosario\",\"main\",\"Postcommunion\",\"all\",1]": "885e10ad3edc5b1e93605c97447380fdeebb5155fad09a14e659103f45506441",
  "[\"beatae-mariae-virginis-a-rosario\",\"main\",\"Secret\",\"all\",1]": "f9d8e6e683d8ecbb5d67abe87dd955178ba4978b85bf59395667462b4f2fc2f0",
  "[\"comm-beatae-mariae-virginis-monte-carmelo\",\"main\",\"Collect\",\"all\",1]": "d396fdba0824533205fa9d5bc067af85a6f6241793c09489f61d45ed8ad106f9",
  "[\"comm-beatae-mariae-virginis-monte-carmelo\",\"main\",\"Postcommunion\",\"all\",1]": "d38fbcac0c76d3d4ddeb0d82496b5c0188ae3d9f3fde0f210c8d18d8aa93f5a0",
  "[\"comm-beatae-mariae-virginis-monte-carmelo\",\"main\",\"Secret\",\"all\",1]": "3d7f01114d0d47a9686623942d357a96f3e99bbb94b3ffcb65e95cb68de77af2",
  "[\"comm-impressionis-sacrorum-stigmatum-s-francisci\",\"main\",\"Collect\",\"all\",1]": "c1924473183079abd111d36bed07a5698ce12d5066baa45b1e0106cfb5e76588",
  "[\"comm-impressionis-sacrorum-stigmatum-s-francisci\",\"main\",\"Postcommunion\",\"all\",1]": "7dc414d8790a9a5e34086d56873c7c7ef1bd8a5030ade0ef0fca8977a9f602c9",
  "[\"comm-impressionis-sacrorum-stigmatum-s-francisci\",\"main\",\"Secret\",\"all\",1]": "88f6b8b3b68cb7385e14eb2dd8c49b6a27a6d1307edb8e959bc4adbe7de23c04",
  "[\"comm-s-agapiti-martyris\",\"main\",\"Collect\",\"all\",1]": "dfa368394a455ffe675cef3b1ea00302fc89b0d6fa173f47226b6d83d4ab56b5",
  "[\"comm-s-agapiti-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "ecf8df23dd7dfbc7066ab4b8f68c76892e2aace4ec2cd1860ec70dc2b770b154",
  "[\"comm-s-agapiti-martyris\",\"main\",\"Secret\",\"all\",1]": "81a60731fcf2bcf8b1e85613f77b21a9da99d21263a107fea260cc2d02de41cf",
  "[\"comm-s-agnetis-virginis-martyris-secundo\",\"main\",\"Collect\",\"all\",1]": "8b4a14fa21075d1848b26b7b8d75dc17182b6371423b6f6e1215fd151c4f5bc8",
  "[\"comm-s-agnetis-virginis-martyris-secundo\",\"main\",\"Postcommunion\",\"all\",1]": "15e33b7c57491e61c4e507fdb405787559fc2e590aa9891f3b9d2fe5fb2c80b2",
  "[\"comm-s-agnetis-virginis-martyris-secundo\",\"main\",\"Secret\",\"all\",1]": "3be6864753d8a724f54c0edab8111737a2f94fecb1c86a05e531e281748865cf",
  "[\"comm-s-alexii-confessoris\",\"main\",\"Secret\",\"all\",1]": "acabc5d32829fc31223691b6052d1aabc8253e44b1b00507d6131e24df4caf41",
  "[\"comm-s-bonifatii-martyris\",\"main\",\"Collect\",\"all\",1]": "861f11866b9cedba6f44627e0f0880defe1c97ccb0137796ca5335c38747f13c",
  "[\"comm-s-chrysogoni-martyris\",\"main\",\"Collect\",\"all\",1]": "ca7ca4b2d2582d9a64c5622546c08541adb6f60640cd3ed06eded70ae03bee5c",
  "[\"comm-s-chrysogoni-martyris\",\"main\",\"Secret\",\"all\",1]": "a3f8709fe0478831434730d6bbccb554893b2bdba0c51bf4900d35bb935e2362",
  "[\"comm-s-donati-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "b9e269e3da9aa118a74f44cd71caa99375d32cd4ea3acec58f2f1b26c912cbed",
  "[\"comm-s-donati-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "434a5db81901ec7dd2b8f54464c2490dfe47e9ce4930f73bd10e40398ff62410",
  "[\"comm-s-donati-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "1704cd3c030a67c040df209b2fd01d3264c088e07e778bd9fbc2b89fdf5b8f60",
  "[\"comm-s-felicis-presbyteri-martyris\",\"main\",\"Collect\",\"all\",1]": "ba71c682ae9d2d234aa69fe0406a6236a17d0e647320b1425c276fcf6bcdbc8e",
  "[\"comm-s-felicis-presbyteri-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "c744ceeb0332cca23f858c13c05853602609734179a241203028c76813529ef8",
  "[\"comm-s-felicis-presbyteri-martyris\",\"main\",\"Secret\",\"all\",1]": "0f747e87d06de675a4355f62f96e9e853a565374ae6861f0b67d1a366fa7a5a8",
  "[\"comm-s-felicitatis-martyris\",\"main\",\"Collect\",\"all\",1]": "a4874a4cf9c2d29297b3a04decec588b0b38b278aeb06497ef70e79a6ede06b1",
  "[\"comm-s-felicitatis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "bd43bc02ebe68db61d6b781d5f95fbebff456c6ba9fb453a8578234a74852695",
  "[\"comm-s-felicitatis-martyris\",\"main\",\"Secret\",\"all\",1]": "3c17df4e20c1d21828a0e080aabb9848a9ce6bc34e39d9107188096199f1caf1",
  "[\"comm-s-georgii-martyris\",\"main\",\"Collect\",\"all\",1]": "5669cb8347339f1d63027ae0cc1a7e60cabaf5395eb1b17dee7b58bdf51b4213",
  "[\"comm-s-georgii-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "f058864005c1c8bb787f7ccfb98f909bf899c8c8128e9de63e64e2811ee46e64",
  "[\"comm-s-georgii-martyris\",\"main\",\"Secret\",\"all\",1]": "3ef73589d3d46e8cd65f29242ec63ce01afde038937f0c04d3540ff647a8e355",
  "[\"comm-s-gorgonii-martyris\",\"main\",\"Collect\",\"all\",1]": "ba87760a1a4cc3a1fba027c0c71522029d237c0f433ab58eb74bd7e2fd56da41",
  "[\"comm-s-hermetis-martyris\",\"main\",\"Collect\",\"all\",1]": "4b646d95939f5635702c2bb569894c812e8b62536665e86d72327200306fe90c",
  "[\"comm-s-mennae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "693c0630d8803e542bdbdcc0172f0edeafda43a16001486a9bbe456380a6f24c",
  "[\"comm-s-mennae-martyris\",\"main\",\"Secret\",\"all\",1]": "62d263cbdcaba9675f68e3d774a9ac29bb438eb7b9c2ad3505c4c8e725f0039b",
  "[\"comm-s-nicomedis-martyris\",\"main\",\"Collect\",\"all\",1]": "0858f3eb4aad2db193e02cd7a47dd9b2022f50d4b4392cdab530af0997d713d1",
  "[\"comm-s-nicomedis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "a43bc8e1028d377c04436d7de8f527084b29db2dfb173fa2a5552d81ed24e92c",
  "[\"comm-s-nicomedis-martyris\",\"main\",\"Secret\",\"all\",1]": "8fbdb67ecac7d25aefd4165f44cbf92252c348a8b36faf48d74c1d82fb0b7e31",
  "[\"comm-s-petri-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "bf4e60992c07ce7ecb1d64ab9df95092acf58442c478df216d0208f7fb9125a9",
  "[\"comm-s-praxedis-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "9214b508693526955e740fad0f6108ea285eac47823f27b2221c6226ecc356bf",
  "[\"comm-s-praxedis-virginis\",\"main\",\"Secret\",\"all\",1]": "761eff1ecf1189d8977e1954e3c686ad0cbbdbe672ee755b03d3424244ef7d50",
  "[\"comm-s-priscae-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "7a79bb26698e6be775d9300ab1117abc7559a0b1edf89d57cddc9ba141f236e9",
  "[\"comm-s-priscae-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "38e32e2e6931e6962410976c8bbf83193ac26a9b689802be6730bcc3926073ab",
  "[\"comm-s-theodori-martyris\",\"main\",\"Collect\",\"all\",1]": "5f92a078371ba30ca21e23208667c2c4fb99f3ec7592210958b06d39aa05ddb0",
  "[\"comm-s-theodori-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "57f8f7200a650c5a8f7f20e98c583561c00a63e9ac255bba45482e60846416e9",
  "[\"comm-s-theodori-martyris\",\"main\",\"Secret\",\"all\",1]": "c141fb3a1e3fab9b460b31d66058d00fbe30c9a0e12da393049e3846ebf25f95",
  "[\"comm-s-thomae-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "e8cea91535b103557d1cae7fc1e00f3248b37bbd44a7f11464f6a39c627bb865",
  "[\"comm-s-thomae-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "a1042bb61cd8f759001b418d1d54e378deead1ae24a90abac68941ebf9e46689",
  "[\"comm-s-thomae-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "64cc5a77ceb6749dcd186d9e32418bb83d7ac1eb0153d9d1f9b94c67c3c07aa0",
  "[\"comm-s-valentini-presbyteri-martyris\",\"main\",\"Collect\",\"all\",1]": "c08d09c77dc5d770dde1d32ce90edbc0da4e3587722d4375de6fa030988c7759",
  "[\"comm-s-valentini-presbyteri-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "42c550d13d563b0011dca65f1c6e4771453923b3d8e3e5de802cae7ce47be88e",
  "[\"comm-s-valentini-presbyteri-martyris\",\"main\",\"Secret\",\"all\",1]": "7362b5b90b5349db948bccb583c0f18a88ca211bfa1b14791269f3cde55af51c",
  "[\"comm-septem-dolorum-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "9bb3654fef1798fd0b79763c8acd961d927245cd749357cd844dff82909050e7",
  "[\"comm-septem-dolorum-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "9280600d322a4d0db519c514c0ffd78eb30a954e00fccf6b79f5cb882549aad4",
  "[\"comm-ss-abdon-sennen-martyrum\",\"main\",\"Collect\",\"all\",1]": "fa62f6e32c12a9467b61680d166f65074efae92ae03f87c1be9257087f9d0907",
  "[\"comm-ss-abdon-sennen-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "1f06d349ef9d711c85e53d552d4710668d5f189b4c9b4156a2791fd8cdd3b69d",
  "[\"comm-ss-abdon-sennen-martyrum\",\"main\",\"Secret\",\"all\",1]": "20386556209e3f35130ddb40be254bc95567ef3bc14c95b6f4d46a705e963833",
  "[\"comm-ss-alexandri-eventii-theoduli-martyrum\",\"main\",\"Collect\",\"all\",1]": "5091930678f10eba39d30caf696ae6400d2bf05a6c9a9866c1c2f82ad8bf1503",
  "[\"comm-ss-basilidis-cyrini-naboris-nazarii\",\"main\",\"Collect\",\"all\",1]": "cdb4eca6a282a4a1f6d1ffdae20726f6074adb8b90cddca5324c274359608861",
  "[\"comm-ss-basilidis-cyrini-naboris-nazarii\",\"main\",\"Postcommunion\",\"all\",1]": "eed6c3488a02ff9d9f65ef668c334b4838987553b32875e0a5e030894f66f97f",
  "[\"comm-ss-basilidis-cyrini-naboris-nazarii\",\"main\",\"Secret\",\"all\",1]": "5817578d229c2a5812cf1c85984ec35eb2e170226ba77df766c4b46348243c06",
  "[\"comm-ss-chrysanthi-dariae-martyrum\",\"main\",\"Collect\",\"all\",1]": "8ce70efc4f55fa78fd81b1f27854418ced1b908e55b721735da96b3c3938ebc2",
  "[\"comm-ss-chrysanthi-dariae-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "51591aa2e984bb64bd09669d6173a00d0015c5357e1141df53aa590d180a6c4e",
  "[\"comm-ss-cypriani-iustinae-virginis-martyrum\",\"main\",\"Collect\",\"all\",1]": "1406883af4b21e47ce14bbaf8a74795ca92d3d0571e5c0192474b527b95c5438",
  "[\"comm-ss-cyriaci-largi-smaragdi-martyrum\",\"main\",\"Collect\",\"all\",1]": "08c0bf129fe0a0fd418d772becd62f19d31abfafc39b5e62aee785b1c2747009",
  "[\"comm-ss-cyriaci-largi-smaragdi-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "01bf7038ab681d3e04bcfe80d744bb85b436ee855bc42cc03bd2315f8ecd03d3",
  "[\"comm-ss-cyriaci-largi-smaragdi-martyrum\",\"main\",\"Secret\",\"all\",1]": "b6b1eaa866d5f2bf38578fdac93f53f829922d85c3e2c1dd7223acc57a9fc9f5",
  "[\"comm-ss-dionysii-episcopi-rustici-eleutherii\",\"main\",\"Collect\",\"all\",1]": "8eebf7cba5168335c0be50712f9fed76c5403459554746567b65bc8c5a2175eb",
  "[\"comm-ss-dionysii-episcopi-rustici-eleutherii\",\"main\",\"Postcommunion\",\"all\",1]": "cf292b5f3fbaca6acf285729a2c9f54289983e4733e5c64bea1db613e881f1a5",
  "[\"comm-ss-dionysii-episcopi-rustici-eleutherii\",\"main\",\"Secret\",\"all\",1]": "f28abeae665bea90874743950c97bbdb29693266291f97dd842e26a83392cb90",
  "[\"comm-ss-duodecim-fratrum-martyrum\",\"main\",\"Collect\",\"all\",1]": "d515e9941beee8c58b9070a0a83c3e663462af7e8bbbe3e3e652f303a208b30e",
  "[\"comm-ss-duodecim-fratrum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "afa5fc57e523071e79a4006ec99f16385811b2e5efb00cafd4c31fed26f53e29",
  "[\"comm-ss-duodecim-fratrum-martyrum\",\"main\",\"Secret\",\"all\",1]": "76b7dac2632e907539bb67245c375fbfda02285782119fe0e16a9647118cfda9",
  "[\"comm-ss-euphemiae-virginis-luciae-geminiani\",\"main\",\"Postcommunion\",\"all\",1]": "8032899e0119bcf1deee67ec48043e8d827786da00df5af07e8bddce56beb0df",
  "[\"comm-ss-euphemiae-virginis-luciae-geminiani\",\"main\",\"Secret\",\"all\",1]": "9a28924e463b9ba7799b7a8c56938857c7684f3e9cbcb322534782c41d620e84",
  "[\"comm-ss-faustini-iovitae-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "c48dc265cf14fde75bd06a3701901a7473547ea78f0020abd1155fd2b23a4f79",
  "[\"comm-ss-faustini-iovitae-martyrum\",\"main\",\"Secret\",\"all\",1]": "521b01e6548eb4d4356eb98955edbeacba2e5b844d306e3722fb752444617345",
  "[\"comm-ss-felicis-adaucti-martyrum\",\"main\",\"Collect\",\"all\",1]": "2065c76ecdf3fab4d6830cfbebc176180271cdc6f72761482b61dc19a26a7e8c",
  "[\"comm-ss-felicis-adaucti-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "428d042984853a8959880ea9c0233418a07a6e75edfdddb74c1f5a118a78b37d",
  "[\"comm-ss-felicis-adaucti-martyrum\",\"main\",\"Secret\",\"all\",1]": "50c63abaf0e49c89816207fffd1400a79ac975bf4fba83611a0b9f0fdf2e8001",
  "[\"comm-ss-felicis-simplicii-faustini-beatricis\",\"main\",\"Collect\",\"all\",1]": "7f834d09b3b2997c7e252fb5df84a458d26cb688ad519857fb2f738d45c7a222",
  "[\"comm-ss-felicis-simplicii-faustini-beatricis\",\"main\",\"Postcommunion\",\"all\",1]": "5a882e2b094cb4b649d11aa87e48aba51a855d8a5907bd257cb3cd133ffc3ec2",
  "[\"comm-ss-felicis-simplicii-faustini-beatricis\",\"main\",\"Secret\",\"all\",1]": "9833fd479d76a69325a20553f10a04522ebe8f5f859eb44b61d9e254ab654a34",
  "[\"comm-ss-gordiani-epimachi-martyrum\",\"main\",\"Collect\",\"all\",1]": "47d691f0dbaa6b0861f48b61b5c03bbc7557c9128ce005a45ed62e713b83b41e",
  "[\"comm-ss-gordiani-epimachi-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "6e2a0a6c826f69495a92fa48748bf00cfb8b4741dd26857472c9b20281d14d88",
  "[\"comm-ss-gordiani-epimachi-martyrum\",\"main\",\"Secret\",\"all\",1]": "d2b0115b0135683bb6cc7cd9391d91ad5d74998f0fbbad1f08b55c4cc11dc6c7",
  "[\"comm-ss-hippolyti-cassiani-martyrum\",\"main\",\"Collect\",\"all\",1]": "abcabdf0669bc31a1363065b09a70afa215bbb7f446cc6c951b81a2c59d25701",
  "[\"comm-ss-machabaeorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "3c1239339d80ab5002ab114699e71ca79acf27eeea90a98cce53571836c33dd9",
  "[\"comm-ss-machabaeorum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "f30ad9562b2c8fde6e02a1160e80ae8e9141ff7ff91457397abf16f340a4a081",
  "[\"comm-ss-machabaeorum-martyrum\",\"main\",\"Secret\",\"all\",1]": "484412e70f87a7d9cbf8a2197fc6a9a1837cdf016af3f8603df4f87e75f9ef37",
  "[\"comm-ss-marcellini-petri-atque-erasmi\",\"main\",\"Collect\",\"all\",1]": "4506ab784920007d5722a9e5371e7ae90b6a1009c53c9b5569c0dfe6bf0da7d6",
  "[\"comm-ss-marcellini-petri-atque-erasmi\",\"main\",\"Postcommunion\",\"all\",1]": "703a5aa45ec1b01f7f9c7a419468f085778424e3954c1db2786140d2811a3c77",
  "[\"comm-ss-marcellini-petri-atque-erasmi\",\"main\",\"Secret\",\"all\",1]": "540d5702b3742b8a2e0f44d6c6c3f3a10efd5cb016e01efa0b9e012a75e53376",
  "[\"comm-ss-marci-marcelliani-martyrum\",\"main\",\"Collect\",\"all\",1]": "3b9c514029f563a97da230c5faa79d0be9e2357998e4ce6491ae867430fad0f8",
  "[\"comm-ss-marci-marcelliani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "c946ac27aaed46ad75315e6d3a11b499386e1b2abbb4566dde1f19a09b05d915",
  "[\"comm-ss-marci-marcelliani-martyrum\",\"main\",\"Secret\",\"all\",1]": "adabf3dffc836ce5647602c24845e0f91c31c65f2b87af4800507e0ad99e7d55",
  "[\"comm-ss-marii-marthae-audifacis-abachum\",\"main\",\"Collect\",\"all\",1]": "8222d02f6b063fb2c67876976f2fa48c44f47042bc0c58e2f1656c4c6911ef2b",
  "[\"comm-ss-marii-marthae-audifacis-abachum\",\"main\",\"Postcommunion\",\"all\",1]": "0e7f8cbe5e8c69842fce828f7d1882b432b8f79f32f5842ef6794e6cb1b34a40",
  "[\"comm-ss-marii-marthae-audifacis-abachum\",\"main\",\"Secret\",\"all\",1]": "f88a3570070879f77cdf2a5d193f8da5e82ac4d8ff80ee58e11b5fe38d6d8047",
  "[\"comm-ss-mauritii-sociorum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "a3aca07f7ff26992e8b9d7d3aa44c7164843286e402b34c125ad8e90dfbd5c2e",
  "[\"comm-ss-mauritii-sociorum-martyrum\",\"main\",\"Secret\",\"all\",1]": "e5516786152b2f95027d5192e6caf34aa972c8e88a0672ee65b1472d0fd16170",
  "[\"comm-ss-naboris-felicis-martyrum\",\"main\",\"Collect\",\"all\",1]": "cbc825f731e5f0e8bed480a07232bf93803bb2134d76f66d4710b2837172f1a8",
  "[\"comm-ss-primi-feliciani-martyrum\",\"main\",\"Collect\",\"all\",1]": "0a114b373ce72bfe875fde80f4e6be95d45495acf43543c855085196c09a88ab",
  "[\"comm-ss-primi-feliciani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "7b4822c6f31a62f95811405fa49ae2b933e9bf3f3efc59958c716ea083d58be7",
  "[\"comm-ss-primi-feliciani-martyrum\",\"main\",\"Secret\",\"all\",1]": "f02050954b3724d27eac30a11d3b5b3e23fd609a8454e93192524221d3be9825",
  "[\"comm-ss-processi-martiniani-martyrum\",\"main\",\"Collect\",\"all\",1]": "288b21aac04e965103035421a5875dbd41ff2035a5603fd58c7a54f528a80885",
  "[\"comm-ss-processi-martiniani-martyrum\",\"main\",\"Secret\",\"all\",1]": "bfbbd54aae71c9c5526d8a544946501e11f4f15931da1eebacbe60bca0779f8b",
  "[\"comm-ss-proti-hyacinthi-martyrum\",\"main\",\"Collect\",\"all\",1]": "7bbd73bdf788e4d88fceacd11dee55bbfe14156417aee2cde3950fb59048741f",
  "[\"comm-ss-quatuor-coronatorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "f9920962165f053b22f8ea0f6a1ebb1857f2d762f4c02cc596b64a27d556cbb6",
  "[\"comm-ss-quatuor-coronatorum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "25e67e3fa567a3bb758de0942d63b312cfca2f0168efe1fcba43d623a99a6cd1",
  "[\"comm-ss-quatuor-coronatorum-martyrum\",\"main\",\"Secret\",\"all\",1]": "05333f31fb89596a4ba585db04398384f02f72102e25b669b288931f26d17c43",
  "[\"comm-ss-sergii-bacchi-marcelli-apuleii\",\"main\",\"Collect\",\"all\",1]": "2518ac0bdb1de28b042f212760847d5afeba69ee1ad0a7e595cc0ca8d8a553c8",
  "[\"comm-ss-sergii-bacchi-marcelli-apuleii\",\"main\",\"Postcommunion\",\"all\",1]": "f2a1e6334f4765f2845977c03d6eac852d264fd994500da0a5c52334d630618f",
  "[\"comm-ss-sergii-bacchi-marcelli-apuleii\",\"main\",\"Secret\",\"all\",1]": "e9258e2d1230c94595f02b2a9e8d89ab3371365c5014407fa668c23494e8ccd8",
  "[\"comm-ss-tiburtii-susannae-virginis-martyrum\",\"main\",\"Collect\",\"all\",1]": "3cfcb7cab45f18de04df0568e1c16c8cdd75c0a0e64f28d712b0b81cc7866f1a",
  "[\"comm-ss-tiburtii-susannae-virginis-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "a3a1528d552bfa6d8771f87558756ab6dda9192075ded361ecd29f8f01c1de9e",
  "[\"comm-ss-tiburtii-susannae-virginis-martyrum\",\"main\",\"Secret\",\"all\",1]": "272c57e2a0e37fcd8fade97839a301e07a072647add439091c84490f8aa231e3",
  "[\"comm-ss-tiburtii-valeriani-maximi-martyrum\",\"main\",\"Collect\",\"all\",1]": "89f80716ebbd1b10594d33e850a7cb4353bd5f40e4bdc4aa1c1962d275df85c2",
  "[\"comm-ss-tiburtii-valeriani-maximi-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "df90b29c8025fa454f65015987d6cc2d6aebef5ffb240d2c8e939615c87a363f",
  "[\"comm-ss-tiburtii-valeriani-maximi-martyrum\",\"main\",\"Secret\",\"all\",1]": "5f04e0aa79cf7a262b92d0137b118e2d1f9ccb9aded3e0528c7309ab4e1cd7a8",
  "[\"comm-ss-timothei-sociorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "96aa722e011cdc0fecce73c4c41768b7d75fc0824206cbb0416915624e40058d",
  "[\"comm-ss-tryphonis-respicii-nymphae-virginis\",\"main\",\"Collect\",\"all\",1]": "bddc61aca9cd9073274f0a7498b905f84bd3719ef6cb690f7455b29a8b237d07",
  "[\"comm-ss-tryphonis-respicii-nymphae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "83edb7ef219c673a7b8ca52d0701f4b87dcde13b7cfcd3422b923b1ab9989ddb",
  "[\"comm-ss-tryphonis-respicii-nymphae-virginis\",\"main\",\"Secret\",\"all\",1]": "99f0c80f7c5edef15be707e7e4a2a2d74a2f3ba247f6c98bc612cf2569bb06df",
  "[\"comm-ss-vitalis-agricolae-martyrum\",\"main\",\"Collect\",\"all\",1]": "317c297f2d46d7d1dbd566ebc78cdae59f75657904e80522ed8c8a07fe2f0773",
  "[\"comm-ss-vitalis-agricolae-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "32dc4b0d1b9636c7517ea12506c4e89b5d1487406878fe4479a30e3078f35b63",
  "[\"comm-ss-vitalis-agricolae-martyrum\",\"main\",\"Secret\",\"all\",1]": "19b235ce4742afcfc4f3563d2a1a288dcb207686f1af2e62a808a4f61bbc447e",
  "[\"comm-ss-viti-modesti-atque-crescentiae\",\"main\",\"Collect\",\"all\",1]": "809ada941e891fcd0d7098adcb5bf2412ba0825f84cf9479c7514916dc69b52c",
  "[\"comm-ss-viti-modesti-atque-crescentiae\",\"main\",\"Postcommunion\",\"all\",1]": "3c2015967e9728093e65ff8d818339a66a9df0bafbe9850d0b7ed17238ef6d27",
  "[\"comm-ss-viti-modesti-atque-crescentiae\",\"main\",\"Secret\",\"all\",1]": "0a89665934acd0feef5cbd214e47e79306f5e2535cbc9e7a1a665f593de9e749",
  "[\"commemoratione-baptismatis-domini-nostri-iesu-christi\",\"main\",\"Collect\",\"all\",1]": "3766c679b4f91d2653b53a25c6f44cee9b21b8de0f02b9ef0ea4c3fd09facfa5",
  "[\"commemoratione-baptismatis-domini-nostri-iesu-christi\",\"main\",\"Postcommunion\",\"all\",1]": "4cacfa96357f29e9cdcfb8dd0e6da988a5bede041d08f3d5094a80d2f19694cc",
  "[\"commemoratione-baptismatis-domini-nostri-iesu-christi\",\"main\",\"Secret\",\"all\",1]": "7f1222d81dbef93aadf299601163c6d46cd9a3c86c593c88fab817cfe200d30d",
  "[\"commune-confessoris-non-pontificis-2\",\"main\",\"Secret\",\"all\",1]": "26c64ad0480eb2f2135393c6d606f5a351062e57e9cb9d35300d592722e676b5",
  "[\"commune-confessoris-pontificis-1\",\"main\",\"Secret\",\"all\",1]": "c1df961145bab6f3c0328a6cadecd4a478b0cf3a61a2702ebe8f19793104a282",
  "[\"commune-dedicationis-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "cb368165af1207213beb2563e528e62ea5b12df7ed40412f187d28431c56c500",
  "[\"commune-dedicationis-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "dc47cd3c9c23befe21cfea72a3a0d4045216f7919fda4b69e78550d59aea250a",
  "[\"commune-festorum-bmv\",\"main\",\"Collect\",\"all\",1]": "f40bbc0965d9c8d8935be3e9a38203a4e88ddb9b0e701795e97e1ea0b5c1df4a",
  "[\"commune-martyrum-tempore-paschali-2\",\"main\",\"Secret\",\"all\",1]": "4ce91a27f52fb3d10d3e3ca6de13a60fabe3899d07701839f5362aaad1f36e4f",
  "[\"commune-plurimorum-martyrum-1\",\"main\",\"Postcommunion\",\"all\",1]": "9d5d2dd3f0d8e251747577c30bb1cebd75b71996c48430b825a1508f064dab51",
  "[\"commune-plurimorum-martyrum-1\",\"main\",\"Secret\",\"all\",1]": "9ab11fffb06840dfb36edd1551d20d9eae5a8971fe29ad7bb295d60ba96445db",
  "[\"commune-summorum-pontificum\",\"main\",\"Postcommunion\",\"all\",1]": "cba19851865b199c36997b3e0a791070ce3644b96856e5008e53a5023e28d24e",
  "[\"commune-summorum-pontificum\",\"main\",\"Secret\",\"all\",1]": "a9cfe1fd1af25202aaca83c7921a56aef241eb9012643b83133d9619e179094b",
  "[\"commune-unius-martyris-3\",\"main\",\"Postcommunion\",\"all\",1]": "2f512e275a5a9bad1a72358ef20f1e3f49f30fd4a15ce2b176934644d05c92dd",
  "[\"commune-unius-martyris-4\",\"main\",\"Secret\",\"all\",1]": "7c3ca642b57150e09738ef13862d098d2a65dc7913371654d88969a515f157c4",
  "[\"commune-virginum-3\",\"main\",\"Postcommunion\",\"all\",1]": "92b46a9c849c53d0ca5f74eee59db3bb2d58418da54a7f01d38a8ce0b6dbf85b",
  "[\"commune-virginum-3\",\"main\",\"Secret\",\"all\",1]": "e473acec1db25a1b91c5c9d1aaafbe608a48997bd0a9bbd5e15f90737951c70a",
  "[\"conceptione-immaculata-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "d4c9f20abdff4cd9e69df0f436bbc4a4071e61f1e06b8659f12710a120008d24",
  "[\"conceptione-immaculata-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "7c2a2c036cb060d2f4a271839ca31f6cd15f1bdc0bffdafea5d58dc06e648202",
  "[\"conceptione-immaculata-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "07009958e3a89166b7ef423f6ecc3be7b720e2f2d7f8a3cb75552f1027be3f83",
  "[\"corpus-christi\",\"main\",\"Collect\",\"all\",1]": "947268c46aee06f709f81f328bcbecae64759518425f35d4570f55dba9215d56",
  "[\"corpus-christi\",\"main\",\"Secret\",\"all\",1]": "3c32ba9c04ebc8fcf7853ab81f50e17c079bfa1af09a4c49f4b50b66b76b6740",
  "[\"decollatione-s-ioannis-baptistae\",\"main\",\"Collect\",\"all\",1]": "a43016434ae603227775c816b238bba320f6a4a88a4bcfcb449a3e4616f47b4a",
  "[\"decollatione-s-ioannis-baptistae\",\"main\",\"Postcommunion\",\"all\",1]": "0e8667cb58439b86a094b93a5d8de8b258a3a1d2b93ec2222220a8a1d4dad6b0",
  "[\"decollatione-s-ioannis-baptistae\",\"main\",\"Secret\",\"all\",1]": "8fe3514608f18476e914885130001178aa972c0acec2519e3e97ae9f066c0c97",
  "[\"dedicatione-s-michaelis-archangeli\",\"main\",\"Collect\",\"all\",1]": "605cffc9f00223c06aec14c63adaf395f6fb72048ffdeaec4626b1eb6e4dc92c",
  "[\"dedicatione-s-michaelis-archangeli\",\"main\",\"Postcommunion\",\"all\",1]": "98889fab951fef191e3e6b5db688d1c792739620da7431e712a0b09cf0f99a32",
  "[\"dedicatione-s-michaelis-archangeli\",\"main\",\"Secret\",\"all\",1]": "a86945f3d3f0096c985975c9df2f4c4f1450416029f61b0d8c4cbcc44caa90d6",
  "[\"easter-2\",\"main\",\"Collect\",\"all\",1]": "95cddf0d15e5f4e37ed44c5f87472b24bcc7be1580a5a763519475299f3daeff",
  "[\"easter-2\",\"main\",\"Postcommunion\",\"all\",1]": "4339c57a1b7d62f5090b55d01197dd8a720e98301274bc2d7c84a02fdfa3b366",
  "[\"easter-2\",\"main\",\"Secret\",\"all\",1]": "2a4c04171e1092beaf5bcc88822b745186bd4480f05b06cfa3dfaa98b56d9cb7",
  "[\"easter-3\",\"main\",\"Collect\",\"all\",1]": "47b193632d1fa5d3ec72ee355ed16e3344fcce275033c90e13e5ccdea469a02c",
  "[\"easter-3\",\"main\",\"Postcommunion\",\"all\",1]": "e8fd039a5bf70a2e8d552616ad8f673eb2383f7c6467f3345a36433785778bcd",
  "[\"easter-3\",\"main\",\"Secret\",\"all\",1]": "3171d873149335ed4e07fd2372e86b569814ffdae97e5bb73261d1f23303a528",
  "[\"easter-4\",\"main\",\"Collect\",\"all\",1]": "d564dcd9fc8d49ebdd2d95d03afa59f7c2388b46f711a882cfef176c6726a8ab",
  "[\"easter-4\",\"main\",\"Postcommunion\",\"all\",1]": "0bd60c9ddb0a1382c6190a3e4fac2cb7cd0e93c64b0e0a1d3f43858dde70fd85",
  "[\"easter-4\",\"main\",\"Secret\",\"all\",1]": "5d0a6f3fd6a23a8ff0920a88cbd988fef1febbbadcb6f16ad155c979578a6a44",
  "[\"easter-5\",\"main\",\"Collect\",\"all\",1]": "1d80b5d01b262078f9fd6fd0e96a32004c5fba967381897ef179766500de89ba",
  "[\"easter-5\",\"main\",\"Postcommunion\",\"all\",1]": "89f40f23d9fe7cb8f6ee8fd732c8ba6c62d31560d0665b6a8e267c4c75c54d88",
  "[\"easter-5\",\"main\",\"Secret\",\"all\",1]": "3a1a40f491e4b4a5010b6dac05319b303a6045931b2c64eeb42b4b83fb90c038",
  "[\"easter-friday\",\"main\",\"Secret\",\"all\",1]": "7bb6732a6e03189171e88e3ca15262d57bccfbcbf8954ebd46bc74f50fe9e9f2",
  "[\"easter-monday\",\"main\",\"Collect\",\"all\",1]": "4d254673f39b49b374036957e382e6f55a6cacb0d32f60896b4ae4b30682afa9",
  "[\"easter-monday\",\"main\",\"Secret\",\"all\",1]": "5cc1a50247eee6925082f156c4a69c13adbb00932f3b29eb77e3fcb65a2e26e1",
  "[\"easter-saturday\",\"main\",\"Collect\",\"all\",1]": "03402b709c0489196bd31edbb796960a34b1c26d2ec7e9d68d6716d5284f27d6",
  "[\"easter-saturday\",\"main\",\"Postcommunion\",\"all\",1]": "5b5f9fde69ae3a148c8ec2d4c48f9f9932e016b05b6464ddf221d663df3788f2",
  "[\"easter-saturday\",\"main\",\"Secret\",\"all\",1]": "1e9b2e2587ce9747cbf96adeaca35eafe111baa4aca0d96d1875bda36e11e2d6",
  "[\"easter-sunday\",\"main\",\"Secret\",\"all\",1]": "f95a6c2d261612b9a6891712275001637d06d95f188076e0eaa802026894f731",
  "[\"easter-thursday\",\"main\",\"Collect\",\"all\",1]": "92f90dc2309020610997798fa337f32b20a5c7403ac2ab97425e50966a057999",
  "[\"easter-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "aa04e1d693d2ec994ffe367a8952719aef76290b5715389c207c5ce41dc1230b",
  "[\"easter-thursday\",\"main\",\"Secret\",\"all\",1]": "754f2dcfda184a3619fab7c1ae67b67f8ce308419d29218e677c760c19059552",
  "[\"easter-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "d5068964de7cdc0c83af900f4b18051ff1a85a3997ab164e4e882246d6efd201",
  "[\"easter-tuesday\",\"main\",\"Secret\",\"all\",1]": "1ee0417ffcfa38df88d0338fa7323576844304fb03f4e6f56431514d42deff39",
  "[\"easter-vigil\",\"main\",\"Secret\",\"all\",1]": "06fceb0b1ff5cf45a43e923c09bf128ea4e2dcae55e276de53da4bb6f9317aff",
  "[\"easter-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "b2be515d1c87420b9d27042afd378765f05f75c809fc69a2e1c25e15f327c8af",
  "[\"easter-wednesday\",\"main\",\"Secret\",\"all\",1]": "450dc6ec9885cfb34484dbc5701c9400c4fd876cf5d5cc0ca6192682f476f3e4",
  "[\"epiphania-domini\",\"main\",\"Collect\",\"all\",1]": "267de69b314c7861166d24bb9578e1d32f928d09b63c8fbab0d21d0a1bf7a413",
  "[\"epiphania-domini\",\"main\",\"Secret\",\"all\",1]": "aa3a3702f0cb617697ec7f3e6daf44866e345c413cd6df834d0d43c0cba21661",
  "[\"epiphany-2\",\"main\",\"Collect\",\"all\",1]": "e9ef35c1c19f2fc3343ce86f4f90c13ec4709d42e8e12540c240708c97dfbb20",
  "[\"epiphany-2\",\"main\",\"Postcommunion\",\"all\",1]": "d9c28fc1fd718dfdc95a2a4c729b1254f790599080fe59c41e9fa4c5775b3665",
  "[\"epiphany-2\",\"main\",\"Secret\",\"all\",1]": "5757d10138c6dbb941c86512388dbbfe1e89f4fc126369f1a39ff3e74c927ba7",
  "[\"epiphany-3\",\"main\",\"Collect\",\"all\",1]": "623d2c76ec22e53dd94e5c7fcd6819dd4679f7c3b3c5fc31cd092e6fe63fc02e",
  "[\"epiphany-3\",\"main\",\"Postcommunion\",\"all\",1]": "0e8af7257b8f62749a9962b0ff86534d831819f8056f1836b2ed66751115f4d7",
  "[\"epiphany-3\",\"main\",\"Secret\",\"all\",1]": "12542ad003ee5ee19b510aa2dad16fd372f551366405556bd5059e35b0b62920",
  "[\"epiphany-4\",\"main\",\"Collect\",\"all\",1]": "c36ba4f4756daf1b3b16de6ee3d12963acfd6f35523db0c29b3ee169c22af9f9",
  "[\"epiphany-4\",\"main\",\"Postcommunion\",\"all\",1]": "c69a36924a17289f7979d5af906149a3a0fc2a081d3704e1d3b7a735ecbb5363",
  "[\"epiphany-4\",\"main\",\"Secret\",\"all\",1]": "5a525124be9c4506d427abd3d2c44c25552a396eef3326fb9fbb31b4d7f72de0",
  "[\"epiphany-5\",\"main\",\"Collect\",\"all\",1]": "904ebad174650fae167bb19383abcb6934ee757b1e6e60fe9e6d038ec837471e",
  "[\"epiphany-5\",\"main\",\"Postcommunion\",\"all\",1]": "9d58c6d67a6399d2be2d236e9049bfd78af8aae4391d5514deccdae591a6af45",
  "[\"epiphany-5\",\"main\",\"Secret\",\"all\",1]": "0ec2c57467aa6b8c64e2249fcf4e019c5f35239f56a95f3a507fe23634fa50ef",
  "[\"epiphany-6\",\"main\",\"Collect\",\"all\",1]": "0ea0c8a95a02e9de7b4e3b6a76475ac964cd8ec467a4b1eae43a8737614f69e7",
  "[\"epiphany-6\",\"main\",\"Postcommunion\",\"all\",1]": "49b98224415f0320a031314ae50d3ed6f37928197f5f91520166c02710cfb951",
  "[\"epiphany-6\",\"main\",\"Secret\",\"all\",1]": "31521a0ead9ca9500c86b6e00a290ab86c9e05a916185833e25b01d4f65f797b",
  "[\"exaltatione-s-crucis\",\"main\",\"Collect\",\"all\",1]": "d01736e64e15b7413ca7bb46ff246c69ae5781679478de8efac287ae7f644c37",
  "[\"exaltatione-s-crucis\",\"main\",\"Postcommunion\",\"all\",1]": "666500d56c5d0232fff07bbcefdf1ac8bf9700f6b0bff5dba73e0a64928030e5",
  "[\"exaltatione-s-crucis\",\"main\",\"Secret\",\"all\",1]": "de43491509741c9fa12cd433d2d5119e53e77e4dfeaa5ada0917925960a6b4f6",
  "[\"fourth-day-within-octave-ss-innocentium\",\"main\",\"Collect\",\"all\",1]": "75d58be9de2fae81896acc9fae7f25e49224d9145a7df709285b6232046abdcb",
  "[\"fourth-day-within-octave-ss-innocentium\",\"main\",\"Postcommunion\",\"all\",1]": "4a0a66a9d0d15290b4c6a7b77dbabd7042e444654ee50c8783ff353782353f8f",
  "[\"fourth-day-within-octave-ss-innocentium\",\"main\",\"Secret\",\"all\",1]": "05f51ab4c3b704aea8209980b449b6a336bf614cbc75c69b18eb4bfb0b1e01da",
  "[\"friday-after-ash-wednesday\",\"main\",\"Collect\",\"all\",1]": "0a0cee06036b3f544155257c8a4b1f22664d4bfd3ecd105872407418fa176b14",
  "[\"friday-after-ash-wednesday\",\"main\",\"Secret\",\"all\",1]": "89d2d515bd48caf9aa3bda7f697b446889ee016c1b075c2e99a353e77f34cf76",
  "[\"good-friday\",\"main\",\"Collect\",\"all\",1]": "eabe72c5c1e62db803b96fe351b2b4fda82e8768811fd9f4619ef534c6344c23",
  "[\"holy-monday\",\"main\",\"Postcommunion\",\"all\",1]": "de9de285bc1374fd653c6066466cfe0fb77ea706d262bdd41bf2f995959403a4",
  "[\"holy-monday\",\"main\",\"Secret\",\"all\",1]": "ecded0bb50de9198ec29382530afeb3a9a20d81abf20183236bf12c99f57b18b",
  "[\"holy-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "8247bab6349cf9fd8c64aed6535d5e664efdac5f4456f8df219e1ca2c4fc8054",
  "[\"holy-tuesday\",\"main\",\"Secret\",\"all\",1]": "a7467369658f9085bab700990bb701636bce568348b43034d0a9c5ce90395952",
  "[\"holy-wednesday\",\"main\",\"Collect\",\"all\",1]": "4d13b89614d98ffd146f40733c025601e611c7672a54a0d61c07ecd9bbc4d932",
  "[\"last-sunday-after-pentecost\",\"main\",\"Collect\",\"all\",1]": "66dba26cad8f2fc5b8f008ec257c347edb5a63b53afdc3931a5762e61451679c",
  "[\"last-sunday-after-pentecost\",\"main\",\"Postcommunion\",\"all\",1]": "4549ec3045b92ce278ca45df763d2a2796d79fa8335b88396570837823330e6e",
  "[\"last-sunday-after-pentecost\",\"main\",\"Secret\",\"all\",1]": "5d31e8c394ae2c04fa56d72cf922cd2ce41842520a0c5ee0ccd24c4cfbaba385",
  "[\"lent-1\",\"main\",\"Postcommunion\",\"all\",1]": "d20fe22bfab771bded8d892a5d9634480abd76f91b71115b5932c2bc8e96b6e4",
  "[\"lent-1\",\"main\",\"Secret\",\"all\",1]": "8b7fb182a03acd23c27493fb1e7929c82eec203d7232fba8f2e3819e82a47b78",
  "[\"lent-1-ember-friday\",\"main\",\"Collect\",\"all\",1]": "e9aa5f4522a4270ab46e25e1f7efbc4914d2c6f8e1349920a68919436b21bd1e",
  "[\"lent-1-ember-friday\",\"main\",\"Postcommunion\",\"all\",1]": "0e0b43ec13444f439dee263df00af904980f1d07769181e79e7711785f769946",
  "[\"lent-1-ember-friday\",\"main\",\"Secret\",\"all\",1]": "a2c22bae6551bd98947b5fe8ce08e826bd19fdd35ea2075f1b7a69506983251a",
  "[\"lent-1-ember-wednesday\",\"main\",\"Collect\",\"all\",1]": "f3c7712d815f514e12347ab24234ddd1a9cd048de11f31b484793041a0de9a4e",
  "[\"lent-1-ember-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "83d84b87968735f030e59032bc9bf682c32f0c97da5d6e99eac90b6c0fb7977c",
  "[\"lent-1-ember-wednesday\",\"main\",\"Secret\",\"all\",1]": "0be56a1e739bd77d6a92cb7bcc49771c7d9a9a91d58635a1620cd1813bf39484",
  "[\"lent-1-monday\",\"main\",\"Collect\",\"all\",1]": "6674cf1be85db0ad885a30ebddf197246a9be659dac9e2dd167ff26f5b98166d",
  "[\"lent-1-monday\",\"main\",\"Postcommunion\",\"all\",1]": "4e4ca3117b0814389e487a05d8c28ccfb2bffe750c504cd97a449e00f5e89f59",
  "[\"lent-1-monday\",\"main\",\"Secret\",\"all\",1]": "c23e1c52b3a5b45be97dc69897eecf3a80661599be463c680bde8ad4408f25b8",
  "[\"lent-1-thursday\",\"main\",\"Collect\",\"all\",1]": "46b3c94ff5b9141621f4a825c18266e733de2dbc463dc90eb8b85a8164ea3e51",
  "[\"lent-1-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "156c924df9ff2ca271752cbc5a084ea5512653cd4d799ea5083754cfffae0454",
  "[\"lent-1-thursday\",\"main\",\"Secret\",\"all\",1]": "3ee986ae770b100732c84eccb6005a48845329e644fa35bd1b90527cb43b0903",
  "[\"lent-1-tuesday\",\"main\",\"Collect\",\"all\",1]": "c70dd0e4e1eabcba0dff957320fb1bb640f267c2ad04830211bfa5313042f10a",
  "[\"lent-1-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "9217b1785ffbf568b320fd3f9e67d6507839e736075a48b0273e8583274a6b91",
  "[\"lent-1-tuesday\",\"main\",\"Secret\",\"all\",1]": "ade569f95426dde4f00f29608f3d1ee360d15f10157c02e76b191cfd8bd29eb5",
  "[\"lent-2\",\"main\",\"Collect\",\"all\",1]": "fe7dcad5159d75b7c1728acb9b48d59841348b0000f8edd5aaef1741a925e4bb",
  "[\"lent-2\",\"main\",\"Postcommunion\",\"all\",1]": "164c1b24ea4a583ad6526f13b24ec295579343f567ba56bcb3498b92048f7545",
  "[\"lent-2\",\"main\",\"Secret\",\"all\",1]": "e722ea748428f63103f58ea1955bf5404023a1a52623a9e5de4d58678759a8d1",
  "[\"lent-2-friday\",\"main\",\"Collect\",\"all\",1]": "7ce389d98c96afc0fc8cb1c8853686c3c9fdabd06dc8f4b80a2fe480a05e3622",
  "[\"lent-2-friday\",\"main\",\"Postcommunion\",\"all\",1]": "9bed20fddc5e11edfb718314150fc030e01a27ecf98f7061b38aea5a81ad7f6a",
  "[\"lent-2-friday\",\"main\",\"Secret\",\"all\",1]": "a1a8ffe16b340fac4b21b0e80e17fda6774171f19db331ff04efa9f68c4339f7",
  "[\"lent-2-monday\",\"main\",\"Collect\",\"all\",1]": "83fb21e6692ff7b1e25ae39ed8e612278675fc062937f5e3696ace3a48a19884",
  "[\"lent-2-monday\",\"main\",\"Postcommunion\",\"all\",1]": "f9505acc089369d5fa305955bd1c1a773a32a2b557b7b9cc822011f676c8a2bb",
  "[\"lent-2-monday\",\"main\",\"Secret\",\"all\",1]": "ed10c52a70288da3952b2311020c73acfbfa95ef2724664ccd79b741c979634a",
  "[\"lent-2-saturday\",\"main\",\"Collect\",\"all\",1]": "32397f97f3cac1f7a7c64d39f8e68df95257e08e9afce1fde88b7b830dbaa6d1",
  "[\"lent-2-saturday\",\"main\",\"Postcommunion\",\"all\",1]": "3dc669c60e41419e87329caed13997145d76e5c18a9e6030939faaf5d8b89af5",
  "[\"lent-2-saturday\",\"main\",\"Secret\",\"all\",1]": "71358b3956ffd974313945b81c7b2e1970427f18db700a6c1b90db5888d62bd8",
  "[\"lent-2-thursday\",\"main\",\"Collect\",\"all\",1]": "ef7ef86ed63be54825d6fc0d9dff33ca4728b4403202d7845ae83f2f49d7d7d7",
  "[\"lent-2-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "26d725ecdd4277e79dc16b71ad3a64ad4c0c0f5157298eb2925a15685a4073c4",
  "[\"lent-2-thursday\",\"main\",\"Secret\",\"all\",1]": "b3891646002dd4f38320b8cbb603f09094bef57db8ff201c0564f8d608a8b9cd",
  "[\"lent-2-tuesday\",\"main\",\"Collect\",\"all\",1]": "28c900ca3f29674cd5795b57536e6cf86272047235d90a2fb683a2a77837cc5e",
  "[\"lent-2-tuesday\",\"main\",\"Secret\",\"all\",1]": "a59b453a338219bf2849c1b4502929b617594351fbfec9562b95522817ba7b00",
  "[\"lent-2-wednesday\",\"main\",\"Collect\",\"all\",1]": "79abc5343e7a60905b33965ecdfa936fae051e09dde9e364423bf65b056ead3a",
  "[\"lent-2-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "28bfe04d8af56f324e413e8afc7ad450e121bf0dce696b122c99ce2446d7b346",
  "[\"lent-2-wednesday\",\"main\",\"Secret\",\"all\",1]": "5120a681a7da273707801f0d4ef78b2850a5b811b1b3cfd692dc06a9f27183cd",
  "[\"lent-3\",\"main\",\"Collect\",\"all\",1]": "4396441681913fe0a5315677f34795fff07ba15887baae8a717fd42e84accb04",
  "[\"lent-3\",\"main\",\"Postcommunion\",\"all\",1]": "2d51022f1e3c9c8797ca03c92ca9927afe0caea420b581c041b5e04a7b59a2ab",
  "[\"lent-3\",\"main\",\"Secret\",\"all\",1]": "e7829d6156902c6c8e49229599b97e835c7571dc509ea57002e44d192c90c0f4",
  "[\"lent-3-friday\",\"main\",\"Collect\",\"all\",1]": "4b25ba22305a251f92ffb7fa2359e176214e8abac445f9141007d28b17143c7b",
  "[\"lent-3-friday\",\"main\",\"Postcommunion\",\"all\",1]": "76d9545fc065a206fb176322cc9722c4e66fa83e29d90983dc41c322eee96e92",
  "[\"lent-3-friday\",\"main\",\"Secret\",\"all\",1]": "bc3f3645c14fc00f50072420db106bb57ec0fe3fcb2d7c7cf78b63e87899dc74",
  "[\"lent-3-monday\",\"main\",\"Collect\",\"all\",1]": "aa6b194d7b99bf9e42efc84576a7a43b1aa86518fc590141af80118824833c50",
  "[\"lent-3-monday\",\"main\",\"Postcommunion\",\"all\",1]": "b9035ff2d485b7ee64f61f33249f352b17daf41f11f890d5bfddac46dec3736d",
  "[\"lent-3-monday\",\"main\",\"Secret\",\"all\",1]": "ae4a188a33a02233843aed9c00eb94298f7fa284f59d058d9b62b8bca4890838",
  "[\"lent-3-saturday\",\"main\",\"Collect\",\"all\",1]": "fdca02695c76cf29153bfee6f3ffc34396dc01d7fab151fd08b5fc340c44e636",
  "[\"lent-3-saturday\",\"main\",\"Secret\",\"all\",1]": "976752e3525c045b3a9018d56b1f6b2fb792b3d792a80261a230d502e8d15407",
  "[\"lent-3-thursday\",\"main\",\"Collect\",\"all\",1]": "bc5e3626f1f4bcfa13307e11a407637d7513b59d64f418f1f540381c55d200f8",
  "[\"lent-3-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "c44cc61710b8cbc20f24c7439326d343702412e0196265888a43f5706d67f37d",
  "[\"lent-3-thursday\",\"main\",\"Secret\",\"all\",1]": "2a05165f9a0e2a4154a961450f2d39766a1fdf32290e7fd3a15a17ddb01a85d9",
  "[\"lent-3-tuesday\",\"main\",\"Collect\",\"all\",1]": "d2443bbb0af3ebab85234759bd8c3ca08728dfef37fe436ea4c1c86ee2378fe7",
  "[\"lent-3-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "eb4032925b2cecc38ceee2700eaec6538aa74570cd616189099d7c7662305390",
  "[\"lent-3-tuesday\",\"main\",\"Secret\",\"all\",1]": "6f4942d8069e7b73edf8379d6bdfb7f9ee57183cbe4358e5f9705b0bbece4ac5",
  "[\"lent-3-wednesday\",\"main\",\"Collect\",\"all\",1]": "1a7d8ce7246569e459bb90980e6ed40597cb1479a43548c93533a31e23ad352c",
  "[\"lent-3-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "c7f09fc0365183f6d423227e872becea739320deeb33d09a6a12bf7327c7e23b",
  "[\"lent-3-wednesday\",\"main\",\"Secret\",\"all\",1]": "13fa457b816a3938bdcd22081c3dc21fbdf678ed7b125accc061e0471a5f3dcd",
  "[\"lent-4\",\"main\",\"Collect\",\"all\",1]": "f7addf87dbf5091a10f321c46a6bc73e36875265f751e6be01cf8599c8b76fe3",
  "[\"lent-4\",\"main\",\"Postcommunion\",\"all\",1]": "3c376d181bda625727f7d59dd20a9b24b5f5c1f8f8d4e72ef61b12e811a98a2e",
  "[\"lent-4\",\"main\",\"Secret\",\"all\",1]": "e2f64d511acfcfd28a01a4495be0498ccc9d25fef682a8b832e847342423aadf",
  "[\"lent-4-friday\",\"main\",\"Collect\",\"all\",1]": "41ea10f616bdb86e220373030ba22fcc9ba084b5ae69a46167d0c6a4cdf1bd17",
  "[\"lent-4-friday\",\"main\",\"Postcommunion\",\"all\",1]": "58896bfb53abb1632e4c6ecbf85f01bec64de7b64f0e0db80afd8697369d16f1",
  "[\"lent-4-friday\",\"main\",\"Secret\",\"all\",1]": "305c6cdd7c594bbdd9cc42797c01683198a9a1c7193c17b9bd70ef0bb6e63643",
  "[\"lent-4-monday\",\"main\",\"Collect\",\"all\",1]": "ba0fa3a3b07d56a50d935ca8e336e2b0ea9c8d1f075975aa976cf64c638966f0",
  "[\"lent-4-monday\",\"main\",\"Postcommunion\",\"all\",1]": "db74bec33eb7fdc5d5c6055728afd762ed2ed61b4299e5a6b5c148d98e6e4d89",
  "[\"lent-4-monday\",\"main\",\"Secret\",\"all\",1]": "0174583c05d29d9d9e8bae50b56359d4236c5ba6b8246ab8caf0300a37b7718f",
  "[\"lent-4-saturday\",\"main\",\"Collect\",\"all\",1]": "082ffea5fce539d290f12f85179f953320a6411e7782cd163299c41e0cdbde0b",
  "[\"lent-4-saturday\",\"main\",\"Postcommunion\",\"all\",1]": "a1718c7d544bb3041f8891a1f9d36dddcf0843237c8f4fd9b1f2a4bb7485029d",
  "[\"lent-4-saturday\",\"main\",\"Secret\",\"all\",1]": "912e6a77ccdfb09bd753b3211aa7a60b6c30f2690e50bb05e196846a32439c35",
  "[\"lent-4-thursday\",\"main\",\"Collect\",\"all\",1]": "2c26b9ab9d3d16548c35317281f4c026eae86f2f55dc169ea1180d3d8062f29b",
  "[\"lent-4-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "7ffacc19bc8b3272b39474a3aaed1b4e01efc5883907c901f84b09bda605da96",
  "[\"lent-4-thursday\",\"main\",\"Secret\",\"all\",1]": "a0b764ae64256664d9c461d70494b7efb49fa0ac2ad6d23168bbf45251941c84",
  "[\"lent-4-tuesday\",\"main\",\"Collect\",\"all\",1]": "1b874c2c8fe9261e113a58a05948c0924755c3858cfbeedd2dca45468537be7b",
  "[\"lent-4-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "c2865521a9231b4c48f4236c7909a4e39e53e5138982c24d62ca6722deb39c4c",
  "[\"lent-4-tuesday\",\"main\",\"Secret\",\"all\",1]": "774af9822eea99668a9c237247d3d1d5a6c62c1f60a3fdce0cd7fd52121a17cf",
  "[\"lent-4-wednesday\",\"main\",\"Collect\",\"all\",1]": "9766f93b1cc8aa337e0876f353993ea84be1111c15a6261d587a809d0acce1bf",
  "[\"lent-4-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "7abf93160cf7b638a8ce1d32a6804975d7b41fec703bf8279920a125dcef7054",
  "[\"lent-4-wednesday\",\"main\",\"Secret\",\"all\",1]": "9a178f279ff277f7b92b129a93dd0c4f7cfa9f5c4281698cfd8a6c5cb261c30d",
  "[\"litania-maior\",\"main\",\"Collect\",\"all\",1]": "137e120aef88527798e90897066cda9ae003ee68c4fa245755f82ef8c7fe2de9",
  "[\"litania-maior\",\"main\",\"Postcommunion\",\"all\",1]": "0b63cc72ce60194c397af7d72cc18bb611a1951e84ff6d9b7139f372b22123ee",
  "[\"litania-maior\",\"main\",\"Secret\",\"all\",1]": "686c6eb83e2087912bad899f697e570c65a3e53c5ed7b3598629e0a6a49fe379",
  "[\"low-sunday\",\"main\",\"Collect\",\"all\",1]": "f0d4ac95efd27c98a13eafa16a395939ad3dbd555059f1277d18101113070079",
  "[\"low-sunday\",\"main\",\"Postcommunion\",\"all\",1]": "9fa0555678c416038d7d7456c3e6cc0c1b108dc3ef95b1984080451ae9799159",
  "[\"low-sunday\",\"main\",\"Secret\",\"all\",1]": "118d54c9544903252ce4092e30fabdc6c505dcf9721420b444d9d5d44625d2aa",
  "[\"mass-of-the-first-sunday-after-epiphany\",\"main\",\"Collect\",\"all\",1]": "647e35846aae6184bbeb61c817838f4cb63a28a043a19be60290f5e97e57ece7",
  "[\"mass-of-the-first-sunday-after-epiphany\",\"main\",\"Postcommunion\",\"all\",1]": "59ce3acf73f07377ae3509cec9dca7567b062c127abe06361e8ce6d48a0c50c0",
  "[\"mass-of-the-first-sunday-after-epiphany\",\"main\",\"Secret\",\"all\",1]": "fa71e5d56c22c447e419f9cfdd3ba9d8fd1c0d47fc8982788b4a133596a638c0",
  "[\"mass-of-the-first-sunday-after-pentecost\",\"main\",\"Collect\",\"all\",1]": "feeeb3c68391a0af794a0be8e8a850ed65b48aa07710c65b85cd78672763c58d",
  "[\"mass-of-the-first-sunday-after-pentecost\",\"main\",\"Postcommunion\",\"all\",1]": "ee2304556499926fae85a5ad0acfdf6707c4d480065bc537701a660b1ca7c88e",
  "[\"mass-of-the-first-sunday-after-pentecost\",\"main\",\"Secret\",\"all\",1]": "b6cefb2266ae183836cddd5dc165c84393f5e9a24d7252639334efc4bf767c1e",
  "[\"mass-of-the-lords-supper\",\"main\",\"Postcommunion\",\"all\",1]": "54871c39799c96e60a443662f4252225b0d1d25e17796442ff5ea968189798e1",
  "[\"mass-of-the-lords-supper\",\"main\",\"Secret\",\"all\",1]": "b88835ef2d569744b7d12d091b4c3e96fa4c971f8ea594061fadc7af301b838b",
  "[\"maternitatis-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "de1bdc8e9d9951efa382f95f14ae6254998c012eebf41569af6fbacbf4b2ba38",
  "[\"maternitatis-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "195d044cb6cff5664d7e0d75f5a886f1bfe53b4ec6edf5dc422b6cd0a035074e",
  "[\"maternitatis-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "5795818dc5cfe3db9f975e02096dfa14e8ece5fce21ced13e02ff5aae874679d",
  "[\"missa-de-s-maria-in-sabbato-1\",\"main\",\"Collect\",\"all\",1]": "2d60314d40b4e583fe268e034db48cb09fb0bee5f5c65414058ffde18dccd74e",
  "[\"missa-de-s-maria-in-sabbato-1\",\"main\",\"Postcommunion\",\"all\",1]": "ce4ea9f68d5d2a8786ad80362cb24d610bd47eb69a3b4a579e832e783be5d044",
  "[\"missa-de-s-maria-in-sabbato-1\",\"main\",\"Secret\",\"all\",1]": "626987be2b3c8bc85491104fc475211eebf90c040aabebe0990d1261c8423499",
  "[\"missa-de-s-maria-in-sabbato-2\",\"main\",\"Collect\",\"all\",1]": "f2947058c291645ae6dd1e3c22afddc4bd7e70bda389f84557fb78f7b39283af",
  "[\"missa-de-s-maria-in-sabbato-2\",\"main\",\"Postcommunion\",\"all\",1]": "0e50f670f2fe3ae3d9719af0eb29d33a7f332f945bc96b1c77721b477c8c2c78",
  "[\"missa-de-s-maria-in-sabbato-2\",\"main\",\"Secret\",\"all\",1]": "df29a572a9b86ab2e5c88edd1ce299d4c40cd24be0932714d39a256bb2b5a7ab",
  "[\"missa-de-s-maria-in-sabbato-4\",\"main\",\"Collect\",\"all\",1]": "a5c63a41b320669f797caa334284b83dabdce143bce43f2fe7c36821310c1819",
  "[\"missa-de-s-maria-in-sabbato-4\",\"main\",\"Postcommunion\",\"all\",1]": "f9b3ead1cdc069579bf7e494838f7b9c01ad061e0f62a5c900ad1987a9bbfae3",
  "[\"nativitate-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "8339f347972ad89373a096b89aa79a2c85ce9a61aa888cc33294f9c8de7a67fe",
  "[\"nativitate-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "fb79d3ca544842ebd13250fb60d44511500910ff326a62d2176f61d8b1b5052a",
  "[\"nativitate-s-ioannis-baptistae\",\"main\",\"Collect\",\"all\",1]": "db1aa6cc35ac8ae4654b12de888dabc7f28a87ff1c58eea7cafa52fa65038969",
  "[\"nativitate-s-ioannis-baptistae\",\"main\",\"Postcommunion\",\"all\",1]": "eba9fbbfcff89d6f6efcf1020bcc5ef57908eb2e5c1428604afe6d937e974c26",
  "[\"nativitate-s-ioannis-baptistae\",\"main\",\"Secret\",\"all\",1]": "3e4a975e3cd71dfab2895504765a11f9affb5435d6930e8de82a31c55d1ee028",
  "[\"octava-nativitatis-domini\",\"main\",\"Collect\",\"all\",1]": "615b148251309bb842793aed7065b0d4fe5b7cd7adefaa05450c01ede11d44f8",
  "[\"octava-nativitatis-domini\",\"main\",\"Postcommunion\",\"all\",1]": "6a2bdf0c4daf17909dc6e4fc3ec96a0e67465ad2826a62b62ac285d6234e9fc2",
  "[\"octava-nativitatis-domini\",\"main\",\"Secret\",\"all\",1]": "38191003225b476b2365eb30aadef20eef64d7454474caeda942e77dcbecafd8",
  "[\"omnium-sanctorum\",\"main\",\"Collect\",\"all\",1]": "9b3571cf26ae350323ee8237abc1213db26f046ceb94b0339f0f714689f990c5",
  "[\"omnium-sanctorum\",\"main\",\"Postcommunion\",\"all\",1]": "541de9d8c97a6d24509d2be79b90ac20240feaf0369484f2aa0f36ebfeb06afe",
  "[\"omnium-sanctorum\",\"main\",\"Secret\",\"all\",1]": "d9276ca6bfd1ed7a2df48d5bf19d45ee41cefb20757d34f3425b8a3c9d9eac62",
  "[\"palm-sunday\",\"main\",\"Postcommunion\",\"all\",1]": "4e0a1e15ac35a55ecff5b896dc7190f9abb28d263b9ee98a6bff126c26246791",
  "[\"palm-sunday\",\"main\",\"Secret\",\"all\",1]": "3f3666a8326f17ff1d9f0171ff36b2daf8dd3c74658d3eec64f63eb50697c9f2",
  "[\"passion-friday\",\"main\",\"Collect\",\"all\",1]": "939063b0b842d54e14114bb6bdddf62fa05682a0a10d566541d7726deb4543f1",
  "[\"passion-friday\",\"main\",\"Postcommunion\",\"all\",1]": "fcd9e4c4b61feaa205885c6b4d93f091927087c1411d43f7e310a36d960e3cb7",
  "[\"passion-friday\",\"main\",\"Secret\",\"all\",1]": "9033c4a1f8bd58f57418e2811395ca91da1c9473cf72c0e0e51dc6435a176e37",
  "[\"passion-monday\",\"main\",\"Collect\",\"all\",1]": "5d3e26489bd47635aab5995f3f4bdad104129c1fbd72b905e9568dfcaf744494",
  "[\"passion-monday\",\"main\",\"Postcommunion\",\"all\",1]": "4b7d2d66f5cd9b17059d3b8dd14bfbaabc09255b4df3d27f5f7361d6b603468b",
  "[\"passion-monday\",\"main\",\"Secret\",\"all\",1]": "8fdf6d339a5b1ae6e1102151ae362c7ab58ec8d88c38790808e538e0b455d825",
  "[\"passion-saturday\",\"main\",\"Collect\",\"all\",1]": "c67ec6b524af5a2ad3200e4f42730a23e7761e87a46a20ce15a6607912280906",
  "[\"passion-saturday\",\"main\",\"Postcommunion\",\"all\",1]": "d8b59eecc3d0ee8d6e04cc3a5417ea7210e6bc42a6dbbf64fa1b57cda7fce479",
  "[\"passion-saturday\",\"main\",\"Secret\",\"all\",1]": "d7585b5c2a80125112065efeb36b105eeccbeb9f812ead7cc8537b45f7ce89d5",
  "[\"passion-sunday\",\"main\",\"Collect\",\"all\",1]": "796d40baa3566be1841e8f1630a4ac9335070dfc7e4edb9ad99763546eb37338",
  "[\"passion-sunday\",\"main\",\"Postcommunion\",\"all\",1]": "ec2ea0b4c3020c7e6669d63cc6d5a001433ffb5e9d4c68e69477d826139757f7",
  "[\"passion-sunday\",\"main\",\"Secret\",\"all\",1]": "c6e4efc91ba32f21eba52b0f9caf9ef9c14d0c992575b42721f092bac9b96fff",
  "[\"passion-thursday\",\"main\",\"Postcommunion\",\"all\",1]": "83c898585ee6233707abf99ca51a2b748796d5135acad2563912a481d5e0d8b5",
  "[\"passion-thursday\",\"main\",\"Secret\",\"all\",1]": "399a1912a415b3272a45974da2cb097e43d7a4ec7b38142804d3030fd334d025",
  "[\"passion-tuesday\",\"main\",\"Collect\",\"all\",1]": "188a77fce3783ef37a6c670d2b5eb80b4df8b525b8a8a0112f7883cd4c2ae1bf",
  "[\"passion-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "3d495327b1a62248a515c05c1d2b68221fe4ad91883d6e8061656a3e4e6e2b29",
  "[\"passion-tuesday\",\"main\",\"Secret\",\"all\",1]": "59059d2993677e2eb8067545926b81c093a9cb3a7a7e1045530ee94e987d5275",
  "[\"passion-wednesday\",\"main\",\"Collect\",\"all\",1]": "ebb1e3dd71b1db1bd171982702f3b7a2ec2356dc58573afac4d06c8ef6671a6d",
  "[\"passion-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "2014578e5c57626ddaac9bbc048c92011f4699df6078309ef1efac7db1bd666e",
  "[\"passion-wednesday\",\"main\",\"Secret\",\"all\",1]": "0940139167de5cfe42ce1fab4df54b590a5a57f13798dc5f705c98b8514ff315",
  "[\"pentecost-10\",\"main\",\"Collect\",\"all\",1]": "e44f96d4fa5405c56f2d4c116271407e985fa758d696883adc10c01d2c8ea5de",
  "[\"pentecost-10\",\"main\",\"Postcommunion\",\"all\",1]": "2bd4c0b65ae863b92925896b74acda13ea94e01b47ade95a39cc44548814f767",
  "[\"pentecost-10\",\"main\",\"Secret\",\"all\",1]": "0677348b4dcb4ff9749c25026c1cd44e755bb9677ed8e607214c1656f19e869d",
  "[\"pentecost-11\",\"main\",\"Collect\",\"all\",1]": "f123f303ac4e56539bd5cb042377d4ef8f4a3766815a3152ba4da749b6a06c09",
  "[\"pentecost-11\",\"main\",\"Postcommunion\",\"all\",1]": "c378e0393dc11b48e0e2ce840c9060c3cb3b41d092b689f8e28c7c1eca36d53e",
  "[\"pentecost-11\",\"main\",\"Secret\",\"all\",1]": "e41e6c6d691dd4a91fa03a220467d79f26c40e25f08d3744767b735361967429",
  "[\"pentecost-12\",\"main\",\"Collect\",\"all\",1]": "b07da3f65a4af73178a9b271711fdae84f12cad56fa37791d86ce7ec41b1606f",
  "[\"pentecost-12\",\"main\",\"Postcommunion\",\"all\",1]": "a31e30017bd16d47222d46524537fd7b0a6706883a2dcf81488085d85c93cadc",
  "[\"pentecost-12\",\"main\",\"Secret\",\"all\",1]": "d4e22c979bc042053892dd2c79f10fa7a264ef4fc1a13d645a29be1de7282e11",
  "[\"pentecost-16\",\"main\",\"Collect\",\"all\",1]": "f7f967cf61289820de62cb71d12b85a79349c20fe2c83e693de01aa8e5ee20f5",
  "[\"pentecost-16\",\"main\",\"Postcommunion\",\"all\",1]": "ea22bffa9fb98a9094890e5cec56e866cfd320559a0f72de28ec6946efe122ad",
  "[\"pentecost-16\",\"main\",\"Secret\",\"all\",1]": "cd1773f80244224d786eef53c19c1f4898075e59123d9f1dd12578fd0a625e1a",
  "[\"pentecost-17\",\"main\",\"Collect\",\"all\",1]": "5dd81a0bebc824ff920397016b29905d786c3f1c3e00ef17bc1ea16184906ddd",
  "[\"pentecost-17\",\"main\",\"Postcommunion\",\"all\",1]": "72cfe0fd6c48de47d267bcbae2d52f733ddf41f341b150ad03978555fa2147ef",
  "[\"pentecost-17\",\"main\",\"Secret\",\"all\",1]": "d8b78b99eeb4e928345d803465f534098100abf1dbe7666cb5974be79eea49c5",
  "[\"pentecost-18\",\"main\",\"Collect\",\"all\",1]": "bd1cc7797b25abb5b0bd043418d8ad632ead98a576e201dbd981f3684820f9e2",
  "[\"pentecost-18\",\"main\",\"Postcommunion\",\"all\",1]": "69c2de7b6a03835291ec03e210cddd9eb7144e7cc9b097cc5c5a6b5317a3605d",
  "[\"pentecost-18\",\"main\",\"Secret\",\"all\",1]": "a871f3dec5769a36bd2d657ea547563f578d04bc1e53064c11358e0ba22a62c4",
  "[\"pentecost-2\",\"main\",\"Postcommunion\",\"all\",1]": "d5f43daaab05088eff63fa75dfd07c1b1ef0cb78824401dee09c48382eea7f72",
  "[\"pentecost-2\",\"main\",\"Secret\",\"all\",1]": "d6727e173eb9725777b9567aef6cfb6992366a018acfeb758fc4afd78678b3d3",
  "[\"pentecost-20\",\"main\",\"Collect\",\"all\",1]": "e44185e73e9f8abcb5466710fe654dab5c2d9705312c3586f6e937c164db1459",
  "[\"pentecost-20\",\"main\",\"Postcommunion\",\"all\",1]": "ced3d0df472121ef19ad5bf04875bb357c26ac9c0e3596c4cfd0459326635ce9",
  "[\"pentecost-20\",\"main\",\"Secret\",\"all\",1]": "bac6a3f2db0165a3ec43f42eb6f07aff6c4f37c53751919613c6583863123b24",
  "[\"pentecost-21\",\"main\",\"Postcommunion\",\"all\",1]": "2b5e2a9e0f6131166d7194e7f47d0368ae583a18c7d670928c16fd7afd895a4a",
  "[\"pentecost-21\",\"main\",\"Secret\",\"all\",1]": "fdd1661e4cb7e4dc3994f20e87e3c58a09c6b731bebd273e2d2009966e0eb12c",
  "[\"pentecost-22\",\"main\",\"Collect\",\"all\",1]": "a79d93fa47bf96e63a15f8bed56cb8d669314325eff45094a20051b7569d00bd",
  "[\"pentecost-22\",\"main\",\"Postcommunion\",\"all\",1]": "ba6d1f92b52ce56e2d78ec97c641eff4484de1409d2456ccd7adcec6e4e6491c",
  "[\"pentecost-22\",\"main\",\"Secret\",\"all\",1]": "1873d87741d24e87c7b748ec18a3ad465a841794adaae2cef003d58600a960ce",
  "[\"pentecost-23\",\"main\",\"Collect\",\"all\",1]": "85aae00b95c3d79e93be659f239338485e48abfdaee4f05e8965b45235ec084e",
  "[\"pentecost-23\",\"main\",\"Postcommunion\",\"all\",1]": "2ff83e7dac7abfde143aad34b484fbc4c38a21536eaf89f3109709e363b940be",
  "[\"pentecost-23\",\"main\",\"Secret\",\"all\",1]": "a96b0dee3395abc44748b468d4eacfd70185b6a73e011b41d4d8708949702658",
  "[\"pentecost-3\",\"main\",\"Collect\",\"all\",1]": "0f5e9d67578fb5cae5337e0a99ee11932ff8d014e09636cb7a292373b13896c5",
  "[\"pentecost-3\",\"main\",\"Postcommunion\",\"all\",1]": "6ffd515e0109b8ac2aca77dee6f6fbb76dc89d36a1ba6a20aa43d55983dd27dc",
  "[\"pentecost-3\",\"main\",\"Secret\",\"all\",1]": "8bfcc8b20f84c644da448c10d42c1f372fe272ef4c9595a60695ca337c3a9dd4",
  "[\"pentecost-4\",\"main\",\"Collect\",\"all\",1]": "5586e37743a642d2bb1bce3674dd657c21831e0f3cc832af47804844e1be84ee",
  "[\"pentecost-4\",\"main\",\"Postcommunion\",\"all\",1]": "78151e4c9671b6624b753b366e5e9eaaa013d89cc43e8afde4c49a9689cc396c",
  "[\"pentecost-4\",\"main\",\"Secret\",\"all\",1]": "3632f25c81285b043f8ac112ad9e5810592219e4e8e0da7ff594bfe3b7c0cf2a",
  "[\"pentecost-5\",\"main\",\"Collect\",\"all\",1]": "824e9a36b12b9fa68e093b572d14fa9dfafb6a18037f74f25cfc30a465606660",
  "[\"pentecost-5\",\"main\",\"Postcommunion\",\"all\",1]": "6e2248249b67d348293405c58f052176d6b368446e228361c158285f7098d928",
  "[\"pentecost-5\",\"main\",\"Secret\",\"all\",1]": "a339edf56d11931a50193c71285a203753eed7af84144fafd603952dddd26259",
  "[\"pentecost-6\",\"main\",\"Collect\",\"all\",1]": "f491fd4c7eebb875424c8c2d33a48673d0527891eb01befac8d44e286b759063",
  "[\"pentecost-6\",\"main\",\"Postcommunion\",\"all\",1]": "b0b9aec19fbace1e5ffcf3710755c9b3385a2b0d206ec7081402dbee854e5a62",
  "[\"pentecost-6\",\"main\",\"Secret\",\"all\",1]": "4e405a99a613075b8787aa95ea1fe7f26025acf3ff4f640413a71df7b7d49eb2",
  "[\"pentecost-7\",\"main\",\"Collect\",\"all\",1]": "62d35ab17d4b7f145f150795d269a88d882e8c8356d5df97ab1d6253d5dd5572",
  "[\"pentecost-7\",\"main\",\"Postcommunion\",\"all\",1]": "e74bcf5582c73ee689174da3a776ac5d39ddd37dc26144c923021f564f1b7af2",
  "[\"pentecost-7\",\"main\",\"Secret\",\"all\",1]": "bc6e1aa16655ab3845939fc0e374fa8a9eefc844199cebd645cd81927b593d11",
  "[\"pentecost-8\",\"main\",\"Postcommunion\",\"all\",1]": "5a36785b18386bb371bf721a91fad92b18d9ce16358725c3c3d10198a979f1eb",
  "[\"pentecost-8\",\"main\",\"Secret\",\"all\",1]": "c1e614b209181ba58558c121944bbe4842a50a5f06fd39e7682bc2b1a7c2d18a",
  "[\"pentecost-9\",\"main\",\"Postcommunion\",\"all\",1]": "fc628f3ec762f30b52601a2ce74ed79e2d16b205225dae34eb6a551259880d70",
  "[\"pentecost-9\",\"main\",\"Secret\",\"all\",1]": "1b7222c570d45aa3e3561b05530d95b19ac972818197afe2cb623973ec2a9801",
  "[\"pentecost-ember-friday\",\"main\",\"Postcommunion\",\"all\",1]": "7127cfea67520a7f46ebce659aae70eefd0f48a8611cb9486bcb6763b8382284",
  "[\"pentecost-ember-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "39d36c0ec4883ded94042377a632c0d988d1f09e8ea4e281a8e950c9e62c23f2",
  "[\"pentecost-ember-wednesday\",\"main\",\"Secret\",\"all\",1]": "f019b8cd49d9bf768a1dad3e168a66ca5ca341a2c1ac31a47b7154be8032de4e",
  "[\"postconciliar\",\"ascension\",\"day\",\"Collect\",\"all\",2]": "02f45b23158e883ecece70ce15a51e82eec798184feb4c2a26386caf78acb083",
  "[\"postconciliar\",\"epiphany\",\"day\",\"Collect\",\"all\",1]": "8f93fa9ec05bc66c58654a7d678ee80834b6abe55d5bfcf42602165e13615823",
  "[\"postconciliar\",\"nativity\",\"dawn\",\"Collect\",\"all\",1]": "fb0f722746e209e52e18767c383fee5be4b4220bf3e7a53d347d822fb0b40541",
  "[\"postconciliar\",\"nativity\",\"day\",\"Collect\",\"all\",1]": "effe0c5a658a0695fb484cacab2a858d5f635133cb2ab66c58f331187da70217",
  "[\"postconciliar\",\"ot-10\",\"main\",\"Collect\",\"all\",1]": "b9dd05fef36167105627d39fc2946d21fe9b5cca60fe066377ff096c4ff9048a",
  "[\"postconciliar\",\"ot-12\",\"main\",\"Collect\",\"all\",1]": "a2f0dcf64e828d52310d1ea87151314b36b27f3bd26c37fb02d0f3c30968b50a",
  "[\"postconciliar\",\"ot-15\",\"main\",\"Collect\",\"all\",1]": "3ec42cafbb28896435d4a3077e951bffab8acb0817847ff53f013c7857b2cd01",
  "[\"postconciliar\",\"ot-2\",\"main\",\"Collect\",\"all\",1]": "465651ebc9d4d328e3b40052d829db1a53858db5c0a43149a82269fc029aa757",
  "[\"postconciliar\",\"ot-20\",\"main\",\"Collect\",\"all\",1]": "1015374e37b9a99e199d22467d83cfa236f34a052a157d4562c2590d09275abc",
  "[\"postconciliar\",\"ot-21\",\"main\",\"Collect\",\"all\",1]": "f26204579a58ca34ef9ab9f0fd60c50778bec21cc11c7170b09d0b0de3985a96",
  "[\"postconciliar\",\"ot-22\",\"main\",\"Collect\",\"all\",1]": "69dc03857b308a4b077e978dc7c6ec4674e003873f9f973ca66f843c81bd1978",
  "[\"postconciliar\",\"ot-24\",\"main\",\"Collect\",\"all\",1]": "5ee6990f694a8b920f1bddaab6c8f53a641c8aeb1df13a9beeea9df7bc128c7a",
  "[\"postconciliar\",\"ot-26\",\"main\",\"Collect\",\"all\",1]": "fa58a6092d027fcf1a8b0d37054f6a9fa314d38eea0034b7cfce6c4eef6b9f39",
  "[\"postconciliar\",\"ot-27\",\"main\",\"Collect\",\"all\",1]": "5f898829d922faafc306223ca773e96c3e4c743b255e10aeb03ad7496bf84348",
  "[\"postconciliar\",\"ot-28\",\"main\",\"Collect\",\"all\",1]": "49b72c94b51826ce4f7d5346fe2467e38d01ef327351e72f503309e982a6f297",
  "[\"postconciliar\",\"ot-29\",\"main\",\"Collect\",\"all\",1]": "a73a206d5ad24c63d1b48d1e09fe3a8d6751572477934f083dedf7fa04908760",
  "[\"postconciliar\",\"ot-3\",\"main\",\"Collect\",\"all\",1]": "479a8b00b6d4fe78f8d9756cdfb3319dc71196ae1508ed49e8c046af8dcf2a86",
  "[\"postconciliar\",\"ot-30\",\"main\",\"Collect\",\"all\",1]": "5ffbaeef41d5450b82babb3034ff7f49124aa2915f5852e7cef713e3dcb30d0a",
  "[\"postconciliar\",\"ot-31\",\"main\",\"Collect\",\"all\",1]": "d719277f8387c2c9571bebffe4f4a5bf6a36234f22ac0f3005306db8e8449fbb",
  "[\"postconciliar\",\"ot-32\",\"main\",\"Collect\",\"all\",1]": "4742496645547b948c369d594401e7613b08788f4724cb82a0503271db8685b4",
  "[\"postconciliar\",\"ot-33\",\"main\",\"Collect\",\"all\",1]": "1cf1912c64ee257a949c65944b433946ccc41613ad38de193cc0b6c47e8ba13a",
  "[\"postconciliar\",\"ot-4\",\"main\",\"Collect\",\"all\",1]": "a2351de0505bf0a5e71970eb2f4ccd4c697efe3a9f77158b5d0c2a82240cba77",
  "[\"postconciliar\",\"ot-7\",\"main\",\"Collect\",\"all\",1]": "4083b2ae41114f896994d0449d5a2b20f58b4859fc6c22895cf2f5e937843eed",
  "[\"postconciliar\",\"ot-8\",\"main\",\"Collect\",\"all\",1]": "a641f826bfcce863c20b0bd1a6250f1c04d6b21df76f4e08dca08051b0bd4184",
  "[\"postconciliar\",\"ot-9\",\"main\",\"Collect\",\"all\",1]": "7d08f945f3ce27e969227e77667caba7cb5381d77accbc1b1552499cbb9156db",
  "[\"postconciliar\",\"pentecost\",\"day\",\"Collect\",\"all\",1]": "af5b5549c57482073f816c557bcb91e92494862f2ec7d85033228dc3f7a6491f",
  "[\"pretiosissimi-sanguinis-domini-nostri-iesu-christi\",\"main\",\"Postcommunion\",\"all\",1]": "1ec65b2ee4a77fdf934dd686c12e37f7071a477eaef3087c0c499b8d9f6aec24",
  "[\"pretiosissimi-sanguinis-domini-nostri-iesu-christi\",\"main\",\"Secret\",\"all\",1]": "17f6a12901a2cd9b2deb914466dd6e790a7075d85de3de7fd9ab8e1df79da12f",
  "[\"purificatione-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "961e9683328e5788bc780f5d8484fe8735e23f5cf744121a78315c9de69fc6fe",
  "[\"purificatione-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "5de044c24851038dcd2270b521372c724978c0f86f6a067c82c85afea3330094",
  "[\"purificatione-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "e08da4bbcaccc4b1dea1a6b3d9b7f1230ba1929bce091aeb542ca9e85b14f9a2",
  "[\"quinquagesima\",\"main\",\"Collect\",\"all\",1]": "4aa81c5641ad156f885e5c183a03abea2f0a650e5427fa22b4be16c5ad40c95b",
  "[\"quinquagesima\",\"main\",\"Postcommunion\",\"all\",1]": "160a980e71af1ed8210612305999187c5ca58fceb91fd2feee646c3d3cb98214",
  "[\"quinquagesima\",\"main\",\"Secret\",\"all\",1]": "b2767a628e675ae2e7156c13a5cf1a36ee17d125a0024c4b60faea36d9429ff3",
  "[\"rogation-mass\",\"main\",\"Collect\",\"all\",1]": "505e748f93262b14925e4a0b32d4ca8266b48e511438c4dbc8d01e55224a4a6e",
  "[\"rogation-mass\",\"main\",\"Postcommunion\",\"all\",1]": "6886a0d087af6432d7ebeeea77459496930d06cf202bb6e435b66bdb1594cca3",
  "[\"rogation-mass\",\"main\",\"Secret\",\"all\",1]": "14323354627c672370242b578fa14dda2b51fd8341745bee7a35e99ac8a89944",
  "[\"roman-1962\",\"advent-2\",\"main\",\"Collect\",\"all\",1]": "754105a16de4ef1418b3b4a58234bcf99c3a80a51eab57dd28a0da71d92ed316",
  "[\"roman-1962\",\"advent-ember-friday\",\"main\",\"Secret\",\"all\",1]": "448fda960f1de0d1471e57c16d941fe29e3f16680d62bc848df4614bd6b91957",
  "[\"roman-1962\",\"annuntiatio-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "ae27622fe16f8943d34c569575e8ebc2b3352e3ca6bf012feb8de051256be33a",
  "[\"roman-1962\",\"annuntiatio-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "20452c3b863e9903416843b7bcf30a4f8a649776b5fb3dde96019effcdf4ad23",
  "[\"roman-1962\",\"annuntiatio-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "c86017bfad26e4dfbf6b358c22b6e583b0fb2906bb323766f3cb363f1e05a237",
  "[\"roman-1962\",\"ash-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "1aeae8c8adbd2e0261791dd37ef4cd040c99560158a0e896ff109528e7dd3e84",
  "[\"roman-1962\",\"beatae-mariae-virginis-a-rosario\",\"main\",\"Collect\",\"all\",1]": "b8e8d7a76f16b2860bb5b572ec5ac5784005c0a0efd73360b92407871e403e3c",
  "[\"roman-1962\",\"beatae-mariae-virginis-reginae\",\"main\",\"Postcommunion\",\"all\",1]": "7672b2b446061af983362cc508e0191cc0bb34f829e214f13927ba29116e06b0",
  "[\"roman-1962\",\"beatae-mariae-virginis-reginae\",\"main\",\"Secret\",\"all\",1]": "22877ca4475631b064e7558dc716674f98db8e2a0790a687cc30f7bf26f262e0",
  "[\"roman-1962\",\"chrism-mass\",\"main\",\"Collect\",\"all\",1]": "4f6d51457d3d56723046004741acd887767f36bf0831471ecee2aeec4d51ad78",
  "[\"roman-1962\",\"chrism-mass\",\"main\",\"Postcommunion\",\"all\",1]": "24c751ce9ee4adc26f84a9c26bfcf528f6442c847577eb2a9ed5334959ba4822",
  "[\"roman-1962\",\"chrism-mass\",\"main\",\"Secret\",\"all\",1]": "40f038337b2f4bc5696d8caa230218e53077050fcea60ba51cf6109f9ee9cfc7",
  "[\"roman-1962\",\"christ-the-king\",\"main\",\"Collect\",\"all\",1]": "b4e5d5232d3f804046a6daa65e152cc31b9f73608b48977d5bbcadd1a3cdad21",
  "[\"roman-1962\",\"christ-the-king\",\"main\",\"Postcommunion\",\"all\",1]": "c6d8ce7eb4703a22583af6177602022a2c23cf8e83f3d8e16d73e0f517132472",
  "[\"roman-1962\",\"christ-the-king\",\"main\",\"Secret\",\"all\",1]": "b910595b435a5a6c2c783169e267f30ad19f200d1c175b8457345182715d8e0a",
  "[\"roman-1962\",\"comm-beatae-mariae-virginis-a-mercede\",\"main\",\"Collect\",\"all\",1]": "dbe06789567d4135cb0d323f82b8b978d0e5e2d080485623e92d076ae5eaf969",
  "[\"roman-1962\",\"comm-s-alexii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "a70a1644c09c252a3ac6cf8386c2e0e8eecebefe9c2f0daf2fb411f10a68a95c",
  "[\"roman-1962\",\"comm-s-bonifatii-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "86f2a5f174751cf759a94fbea8cc11a52744ebe7db8bfb57404a9b06b14818e8",
  "[\"roman-1962\",\"comm-s-bonifatii-martyris\",\"main\",\"Secret\",\"all\",1]": "f9f77f9fef00e93fa9930593563674f61911bdf147b455d35ba614888b310f4b",
  "[\"roman-1962\",\"comm-s-canuti-regis-martyris\",\"main\",\"Collect\",\"all\",1]": "2b154027baaad6e5fac52cb9505b29f6d5f19e99e29bb6f84325199c7e312a68",
  "[\"roman-1962\",\"comm-s-canuti-regis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "1fcfe8d65ef4a205ab89639ecf99e0036f96160ea8677d70dad275858fa83b4b",
  "[\"roman-1962\",\"comm-s-canuti-regis-martyris\",\"main\",\"Secret\",\"all\",1]": "59862c8a11612439d7158498f139c43135fce240cb5dbc85ea54a7d22dbbf215",
  "[\"roman-1962\",\"comm-s-chrysogoni-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "f409fd24cfea901a91d88bd739d652fcf98959f6a359795303aec90a333ac270",
  "[\"roman-1962\",\"comm-s-eusebii-confessoris\",\"main\",\"Collect\",\"all\",1]": "244e9a940ce20dd052b9759f3072769cd1f137c3d453744ec3c5e7f709e985af",
  "[\"roman-1962\",\"comm-s-gorgonii-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "b54d2c4679f36cdd8bd880422ec264a1a02f026a779087c7c82f589bee3a0224",
  "[\"roman-1962\",\"comm-s-gorgonii-martyris\",\"main\",\"Secret\",\"all\",1]": "66e34fa246d58f688ce662f425d66f7b7ea265f543c5c0e6e4a50ea03d324e1b",
  "[\"roman-1962\",\"comm-s-hermetis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "a953023f18bf567c0dc7fa50b7a4747709ef1808b9a99045524b00dfc1e736de",
  "[\"roman-1962\",\"comm-s-hermetis-martyris\",\"main\",\"Secret\",\"all\",1]": "b397c348f38782148d3e4a9b84609dc35c6b4be600e61f4aa1f98e7d689123cd",
  "[\"roman-1962\",\"comm-s-mennae-martyris\",\"main\",\"Collect\",\"all\",1]": "e62198db1a63c014b6fd133eb1fe08113670325404f2c93681c2efa6514ffc9e",
  "[\"roman-1962\",\"comm-s-pauli-apostoli\",\"main\",\"Collect\",\"all\",1]": "430d9e661403471462297a8642651c3e24fcc044fc03b20189b76d22b1e3eca6",
  "[\"roman-1962\",\"comm-s-pauli-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "5db1cb0bff15361d8a06cbd1875eacedde17aabe47333be98f2b7d24c0611d15",
  "[\"roman-1962\",\"comm-s-pauli-apostoli\",\"main\",\"Secret\",\"all\",1]": "d00d6e1391ba094983ecbf51131620377d10c68fa1019702850eec24a527e0bc",
  "[\"roman-1962\",\"comm-s-petri-apostoli\",\"main\",\"Collect\",\"all\",1]": "29806437242d6e1f3a01b18e941d1245fc18f7b98e23beb3305302496c162114",
  "[\"roman-1962\",\"comm-s-petri-apostoli\",\"main\",\"Secret\",\"all\",1]": "cf7367c25facc6f9c8255df5a0bc7ee211e99c2c7e6a6f938ad71034f4265644",
  "[\"roman-1962\",\"comm-s-petri-apostoli-2\",\"main\",\"Collect\",\"all\",1]": "d70cbad6813528b470e9259003ef753b62e73d012aedf44799c1184e27618709",
  "[\"roman-1962\",\"comm-s-petri-apostoli-2\",\"main\",\"Postcommunion\",\"all\",1]": "c849dbf600bfc639c3771c6f04bfbe5f811a754516d5112313a9e71841f7a8ec",
  "[\"roman-1962\",\"comm-s-petri-apostoli-2\",\"main\",\"Secret\",\"all\",1]": "2cbe0c59154e1567ad7b9ff13097732b8f639d5c7d7a67c19e4bcb2c7be212b3",
  "[\"roman-1962\",\"comm-s-praxedis-virginis\",\"main\",\"Collect\",\"all\",1]": "6ddf6a0888d997df149a1ebbff5ecc26815f52f4d25d5b207cf676f96ed2c298",
  "[\"roman-1962\",\"comm-s-priscae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "d1562dda19930edf4916f23bb3b45d7246308b98b43d3950096c7a799eba83df",
  "[\"roman-1962\",\"comm-s-romani-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "3ca2fec9849bd51eda2cdb87ee91515b7f510e888a724ec206f4cd28df782f0e",
  "[\"roman-1962\",\"comm-s-romani-martyris\",\"main\",\"Secret\",\"all\",1]": "034a2257bcf925f2da23792ea7c78e3cd8e1b11e9c554ef5b076cb7b46cca6a8",
  "[\"roman-1962\",\"comm-s-sabbae-abbatis\",\"main\",\"Collect\",\"all\",1]": "daf3bd540b02e3a2e74a5d79b86ad9ee5e1808357eca57d7d9d21131720aecff",
  "[\"roman-1962\",\"comm-s-sabbae-abbatis\",\"main\",\"Postcommunion\",\"all\",1]": "a0c536c74255c8ef7eb575793e100f99575b439fac1c81d3734a69e7a8713b26",
  "[\"roman-1962\",\"comm-s-sabbae-abbatis\",\"main\",\"Secret\",\"all\",1]": "d5bfa6f48ae6eb12774727d91a3484a52645902b080533df1f9dba69b539fd9e",
  "[\"roman-1962\",\"comm-s-sabinae-martyris\",\"main\",\"Collect\",\"all\",1]": "e47c79eabffb29566534594baec918eb0ddad9fa5d899152deaa8931261ad2d9",
  "[\"roman-1962\",\"comm-s-sabinae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "75e1c69c73caba679012b453c6ce535a79fa7d434d91c735db233db1e1691a7c",
  "[\"roman-1962\",\"comm-s-sabinae-martyris\",\"main\",\"Secret\",\"all\",1]": "b842aeacb01ff00bffc72ea8f9398272d271a9f492ebc86db8e4338d26248c5b",
  "[\"roman-1962\",\"comm-s-saturnini-martyris\",\"main\",\"Collect\",\"all\",1]": "4e568eed33adec8e35b080f36c8ff3528768967ab55a6f64617d3965cd1345d0",
  "[\"roman-1962\",\"comm-s-saturnini-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "3803fac6a169c751d042dde7f3b5e610b4ae719e920e802c2e43f418d0a1c0f9",
  "[\"roman-1962\",\"comm-s-saturnini-martyris\",\"main\",\"Secret\",\"all\",1]": "7da2fdbea247284236242ce644cc08a459631d0be9027205f47cdc588e41404d",
  "[\"roman-1962\",\"comm-s-silvestri-i-papae-confessoris\",\"main\",\"Collect\",\"all\",1]": "0220fa00745ef5f2f33dbb05a32fd6aa6cc237e7cf0fb1a63a4c15bb7bc6f6f3",
  "[\"roman-1962\",\"comm-s-theclae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "67f897f2b2bdff024630f993a0da72fe21b950a3e61b8105f41cacdd973c1e97",
  "[\"roman-1962\",\"comm-s-urbani-i-papae-martyris\",\"main\",\"Collect\",\"all\",1]": "422c296a2cc6f66a26249e22367996b1a7480c10d51454662c33b400127c7307",
  "[\"roman-1962\",\"comm-s-zephyrini-papae-martyris\",\"main\",\"Collect\",\"all\",1]": "091c0b21ba9d8656bde773a8e0eeb7a1e08dec73d3a6feffea5a017f4394119d",
  "[\"roman-1962\",\"comm-septem-dolorum-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "c1ec46f7734277368c7a7ea1b8790fd374e5df309d58d6513a72cc0bf264f3ae",
  "[\"roman-1962\",\"comm-ss-alexandri-eventii-theoduli-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "45c154f58cd2697f5b450f506f8339a89426a25932548d5f89870ef524abc711",
  "[\"roman-1962\",\"comm-ss-alexandri-eventii-theoduli-martyrum\",\"main\",\"Secret\",\"all\",1]": "2c1040a418d307f8a32002198e46fe1d2c8d5443320126a9311b0767e19f96d5",
  "[\"roman-1962\",\"comm-ss-chrysanthi-dariae-martyrum\",\"main\",\"Secret\",\"all\",1]": "32989bb18d5c83260414a95d07d6cd80959455a71f82740ca02d677fcb15203b",
  "[\"roman-1962\",\"comm-ss-cypriani-iustinae-virginis-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "1049ebf3afba5596250c4d3f8782fc64d2cf7a26c263dbc09a9cc39e95c095cb",
  "[\"roman-1962\",\"comm-ss-cypriani-iustinae-virginis-martyrum\",\"main\",\"Secret\",\"all\",1]": "a2a8867dcc32da9753e47ddea7ee138f3408fed91c103827afc0bc58dec75311",
  "[\"roman-1962\",\"comm-ss-euphemiae-virginis-luciae-geminiani\",\"main\",\"Collect\",\"all\",1]": "a60f6a216ccc0dbd3169977a4fc6a1ce99102112bee5098f39a37d8089db3620",
  "[\"roman-1962\",\"comm-ss-gervasii-protasii-martyrum\",\"main\",\"Collect\",\"all\",1]": "cb5331effc74f47d3a0e92016c10c6fb2fae55b1e91c0e7f2094ec03e7c2b96c",
  "[\"roman-1962\",\"comm-ss-gervasii-protasii-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "dbcd713867d0d2d1731a686e6a27c1b087dd0e4fee6c5a73dfc736c7c55e1b26",
  "[\"roman-1962\",\"comm-ss-gervasii-protasii-martyrum\",\"main\",\"Secret\",\"all\",1]": "8edc4dd717b3e1c1ab616d6ea7072804e22b0b169bb9a25dee9b2d51d4fcb327",
  "[\"roman-1962\",\"comm-ss-hippolyti-cassiani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "8c5a1043848083c47825b787274ebebe4a9e7b3cf7b1a48a244cc22ab4356df4",
  "[\"roman-1962\",\"comm-ss-hippolyti-cassiani-martyrum\",\"main\",\"Secret\",\"all\",1]": "e60c97660cbeeec012dedd76af11fbdd2f68e30ba357c790246b86e8f689fa90",
  "[\"roman-1962\",\"comm-ss-mauritii-sociorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "36fc4721e9d272a0d58002a9999bd76a1663d8af328a069f2399d2bbbb3eda3b",
  "[\"roman-1962\",\"comm-ss-placidi-sociorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "8a8149c5febed6106aa1fdf156e044fc9f274ad6c52e912a3cfe784bafaea3e1",
  "[\"roman-1962\",\"comm-ss-placidi-sociorum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "bed1fbf4d4eebeecc2694042dd98c758aff602e00c0cb90cc39dfd3d51902322",
  "[\"roman-1962\",\"comm-ss-placidi-sociorum-martyrum\",\"main\",\"Secret\",\"all\",1]": "5843dac38d464efdaf1009aa5bebcef63730cdee27aad650c37cf0724383b1aa",
  "[\"roman-1962\",\"comm-ss-processi-martiniani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "6c93dfb9c2537199839d1b9b27adb4d10be6aee4ad500e0fa3ebf4e9724bf38b",
  "[\"roman-1962\",\"comm-ss-proti-hyacinthi-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "df6cc0c8c34829591dab3ab7a4f5767e350df1f0e53baf42569f3f0dfb05b43c",
  "[\"roman-1962\",\"comm-ss-proti-hyacinthi-martyrum\",\"main\",\"Secret\",\"all\",1]": "bd8087da3f7c5294cef559c13273f15ed0f22b584eb803be18fceafea3719a80",
  "[\"roman-1962\",\"comm-ss-symphorosae-septem-eius-filiorum\",\"main\",\"Collect\",\"all\",1]": "9c8d804b3a7ac74bb49c2577f9a9d932c50a44f71391713df36850ee15ef8cad",
  "[\"roman-1962\",\"comm-ss-symphorosae-septem-eius-filiorum\",\"main\",\"Postcommunion\",\"all\",1]": "f763e426e3ed7e1771b7256826adfb4b649a15425099018ed580365d0f07ef61",
  "[\"roman-1962\",\"comm-ss-symphorosae-septem-eius-filiorum\",\"main\",\"Secret\",\"all\",1]": "9f56ed095b997b34035cff0a96cdc22ebad14da6917d94062338f59ee172dd8c",
  "[\"roman-1962\",\"comm-ss-ursulae-ac-sociarum-virginum\",\"main\",\"Collect\",\"all\",1]": "d87f9d87200728bd2737d967bd7898b74c621989c43f06b69328ce2d593fbab6",
  "[\"roman-1962\",\"comm-ss-ursulae-ac-sociarum-virginum\",\"main\",\"Postcommunion\",\"all\",1]": "c14a73ec42a7d5beb20d8234bf050eaa6a73c83a98ada71b71c823fb067750ba",
  "[\"roman-1962\",\"comm-ss-ursulae-ac-sociarum-virginum\",\"main\",\"Secret\",\"all\",1]": "702a5a6b827ba68cc41f6b3fba566911563ce7d24953d6c4379fac0ece213559",
  "[\"roman-1962\",\"comm-ss-xysti-ii-papae-felicissimi\",\"main\",\"Collect\",\"all\",1]": "cece1e55222a338520f115cd71a93e000d5ade0b349b9efc4d39432e0ce790a4",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"first\",\"Collect\",\"all\",1]": "ce158be1912a1f01bdf56ad1f7ac774ec6c75a6f68cc30528acd6926ef78b1b1",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"first\",\"Postcommunion\",\"all\",1]": "812e6a89855c0bc92a90836c6a6c1a362fa154f4d3a4f8923537b69eec55ce22",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"first\",\"Secret\",\"all\",1]": "7de2be01eff548d52c609b699fb0fbb19095cc4809d1a5132f8db83ab4b9093b",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"second\",\"Secret\",\"all\",1]": "b0d73c593f914112edd5190c7b771c43dad58c676471498f371b72d57509fd3f",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"third\",\"Postcommunion\",\"all\",1]": "cedcfe0fa600fdaea45f4f90e2038c5fcca13b079034caf12ed0f28863d16738",
  "[\"roman-1962\",\"commemoratione-omnium-fidelium-defunctorum\",\"third\",\"Secret\",\"all\",1]": "c19a0ecf304b3e5b511040056362908149dcd8fe1c58b1c601939862f994d9ee",
  "[\"roman-1962\",\"commune-confessoris-non-pontificis-1\",\"main\",\"Postcommunion\",\"all\",1]": "3d41e5c125c867cc2f64fb895be9ab7515535a4f11455bf98c50e58f32bed5bf",
  "[\"roman-1962\",\"commune-confessoris-non-pontificis-1\",\"main\",\"Secret\",\"all\",1]": "9f8c933718fde8e7171d24a3355426b1bf6651b1e84675b383f7dcaa3cc3bcd8",
  "[\"roman-1962\",\"commune-festorum-bmv\",\"main\",\"Postcommunion\",\"all\",1]": "5abafd874804fb48cc015d9d784698a52151ea686f6b5a12160b47b701a21005",
  "[\"roman-1962\",\"commune-festorum-bmv\",\"main\",\"Secret\",\"all\",1]": "8cc71ff2e39dd68073c123fc43d028cade3fc6750ec00422215c9d648518c81a",
  "[\"roman-1962\",\"commune-plurimorum-martyrum-2\",\"main\",\"Secret\",\"all\",1]": "f8a88d7384b7b23e38a11e8bcd1fa0ced64614a3cdf238d0674434251a709083",
  "[\"roman-1962\",\"commune-unius-martyris-3\",\"main\",\"Secret\",\"all\",1]": "8c4d7d1671cefb72b6536642ee6a1f2c3464573eccfce7e78274c3fc44b00ef5",
  "[\"roman-1962\",\"corpus-christi\",\"main\",\"Postcommunion\",\"all\",1]": "c5dce5c5e6f50dd4b377a01bd9766066c1961b7bde222bb208cc86009c126eaf",
  "[\"roman-1962\",\"easter-friday\",\"main\",\"Collect\",\"all\",1]": "ff4b56ef2dc575088404d03e9efa1d82c2ceed7f5a3aee2c43a97bb9875b1736",
  "[\"roman-1962\",\"easter-friday\",\"main\",\"Postcommunion\",\"all\",1]": "55086916a1e014e638a0ceafb9758d0da490370591097c1baf25887465719474",
  "[\"roman-1962\",\"easter-sunday\",\"main\",\"Collect\",\"all\",1]": "78e63155729764cb9687ff0ba979abcff038ce94d6bdda81905d42554dc920b5",
  "[\"roman-1962\",\"easter-tuesday\",\"main\",\"Collect\",\"all\",1]": "d39ffc227709a0043c5155a9fedc1a7737ecd59b73fc0a4e662eced343db13fa",
  "[\"roman-1962\",\"easter-vigil\",\"main\",\"Collect\",\"all\",1]": "27528ef133e2f963881482a573de57a21e1afadc59a68fabb7189b14cd77b5dd",
  "[\"roman-1962\",\"easter-wednesday\",\"main\",\"Collect\",\"all\",1]": "70bd60b5180066c4336b5ddf39442dc11b2c7f687ea80e8e78fcdb6c68a19f4b",
  "[\"roman-1962\",\"epiphania-domini\",\"main\",\"Postcommunion\",\"all\",1]": "3fb831fb9ea74d90ebff69efcf8b13aa3e7877a58944bc5cc95e7fb560f0f840",
  "[\"roman-1962\",\"friday-after-ash-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "89f5235d172161f426fffc82621ceb60a5456e7ee509c0d5e978d4a6e8d1d6a8",
  "[\"roman-1962\",\"holy-family\",\"main\",\"Collect\",\"all\",1]": "868a551e48c2efad0a9317e7eddf0656b8ded31408a1fcc0faa6edc8b2da99dc",
  "[\"roman-1962\",\"holy-family\",\"main\",\"Postcommunion\",\"all\",1]": "f1842e67c73ac6e8b91968be3723ced927e23aa1a3989b729b141ce9c502e6bd",
  "[\"roman-1962\",\"holy-family\",\"main\",\"Secret\",\"all\",1]": "f4c9dbc175f7d9dac19fe064e6e23bf94ef89baef9af6e531a65cd18e9444ebe",
  "[\"roman-1962\",\"holy-monday\",\"main\",\"Collect\",\"all\",1]": "f992f3c23abc540c49e87f763a74e77f655d9dbc186d12fb6f1060b4a485a5f7",
  "[\"roman-1962\",\"holy-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "30221c1356db9a1bad670aa67a1d77462a7b4f58102bda3a6a0402e2a0a1e034",
  "[\"roman-1962\",\"holy-tuesday\",\"main\",\"Collect\",\"all\",1]": "4273208516048bb068893225b9bee8951fe2dd606ac50a8903339cdbe645dc70",
  "[\"roman-1962\",\"holy-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "ec63f50d9d561b96a3e9be88049403801d7c837757da7b774bc0530c83476810",
  "[\"roman-1962\",\"holy-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "826fb23d431f9b3efdceb82836abc131793b69a95df384e3c2145829823cb4cd",
  "[\"roman-1962\",\"holy-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "9610679dea3d368bf611986eae386d1cc957b140fce031235ab151bcdf7a16fe",
  "[\"roman-1962\",\"holy-wednesday\",\"main\",\"Secret\",\"all\",1]": "49fcd855cd3ca7256a81c746ed7a7e0b71800daa2b6765b141d288d3761629b8",
  "[\"roman-1962\",\"immaculati-cordis-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "f113967f850352b468cbf5df6ad67c40413e2c416c39ae2e5483b7f4edeb44d9",
  "[\"roman-1962\",\"lent-1\",\"main\",\"Collect\",\"all\",1]": "19e0be39e908580682ba0cd9eb5a1deb5d12ccda1737ba7b53564deadd4549df",
  "[\"roman-1962\",\"lent-1-ember-friday\",\"main\",\"Oratio super populum\",\"all\",1]": "17ec2a977b3f3f0936f85cf83c2497f27ddb1bf7e576dc1f905421594bcb4103",
  "[\"roman-1962\",\"lent-1-ember-saturday\",\"longer\",\"Oratio\",\"all\",6]": "818560ce7ca3152221eeba2ba6e746ef484a51978c8abb66ebb27cce8c094a11",
  "[\"roman-1962\",\"lent-1-ember-saturday\",\"shorter\",\"Oratio\",\"all\",2]": "4932374497d5e4a6a5ae83faad1cd4f21aabfe7eeb41e0166bcae8af42fdc213",
  "[\"roman-1962\",\"lent-1-ember-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "f1773ef57832e55b05ddca395530b04e9fd5c58e355cfab8729c3ed32b4c33dc",
  "[\"roman-1962\",\"lent-1-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "16898535a65bac54b36e76a3fdf307d31e4a7b6f66421d4ee1d3df1b1af22d16",
  "[\"roman-1962\",\"lent-1-thursday\",\"main\",\"Oratio super populum\",\"all\",1]": "d9d9ba1b315faa01c18fa44fab1a1141a3ac2a1da8d93bfa4331cd62d75bdba8",
  "[\"roman-1962\",\"lent-1-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "c5ce46b3ef0dd9fa8b3d5ef0e5d02024ef81bd38b964bf4ebc198b3eede6eac6",
  "[\"roman-1962\",\"lent-2-friday\",\"main\",\"Oratio super populum\",\"all\",1]": "7d178334da728da5640ed773d46984a97e762f127a035d3c87561df6c40a306a",
  "[\"roman-1962\",\"lent-2-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "2bf68e84d241bc3d5842a821eeacd43adc0b8094f9c27a3c62db7d8d617a7b80",
  "[\"roman-1962\",\"lent-2-saturday\",\"main\",\"Oratio super populum\",\"all\",1]": "aea7b36a4e96ecd7f84cabba4dc03c4f83e7fa4ba1c4fb6ed798b3a98bf120cf",
  "[\"roman-1962\",\"lent-2-thursday\",\"main\",\"Oratio super populum\",\"all\",1]": "68ee4a8fcf1b3fb1ad7eb4704f6f573843f25f1ecd01b20b2195253fee7989a3",
  "[\"roman-1962\",\"lent-2-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "d85c7718ff30b8ebb1490792bc1d13c8d3136ad06d1463a15ef9adfce42a5d0e",
  "[\"roman-1962\",\"lent-2-tuesday\",\"main\",\"Postcommunion\",\"all\",1]": "4da0f756643489901ed6b06f3740ccb9796bd252753ee2cdc99cff8dc05b3288",
  "[\"roman-1962\",\"lent-2-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "b4aff2e49914bc5c278c9ae5abf2cc1283d4ca508ae76e99293fd005ca9a39d6",
  "[\"roman-1962\",\"lent-3-friday\",\"main\",\"Oratio super populum\",\"all\",1]": "84ce04c228880c5accb3ccbade1128ca528628661d8ebc038a08eeb9e122ae88",
  "[\"roman-1962\",\"lent-3-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "ebf485ac8708da06f82fbaca902f695cde292079cb719a8ace148cef8d1b5016",
  "[\"roman-1962\",\"lent-3-saturday\",\"main\",\"Oratio super populum\",\"all\",1]": "481e286ed434ba47ae30f6ca84adf0b55773e749b397a628b6f9e25a03098df6",
  "[\"roman-1962\",\"lent-3-saturday\",\"main\",\"Postcommunion\",\"all\",1]": "a179b1efb8e637c1ff001e0a82df14d59e998590f89531d95fec6ac42bf15790",
  "[\"roman-1962\",\"lent-3-thursday\",\"main\",\"Oratio super populum\",\"all\",1]": "835c4bd19ee1166bb4b9822753a32b3016c6a2db4f61b1da5ab9c9fe269a497d",
  "[\"roman-1962\",\"lent-3-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "45750093f4755c6efd1fe819eb4820bc15d1a82338203d7cf29db2e768d1d71b",
  "[\"roman-1962\",\"lent-3-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "101b2ee1ca827ed1116e5c4b64fa52ab674289e661ec638b45722e0a823428a3",
  "[\"roman-1962\",\"lent-4-friday\",\"main\",\"Oratio super populum\",\"all\",1]": "1260ee846f962e40e60813f9202fd59a458a50b261f38f96e83b6d9a2f8d4023",
  "[\"roman-1962\",\"lent-4-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "020576fe32aecb96552cb5da51466be5d4985d95e01a1199fcaad2e8de2545c2",
  "[\"roman-1962\",\"lent-4-saturday\",\"main\",\"Oratio super populum\",\"all\",1]": "8863932c9e8bf9bb023e2ba8e6a42623ad365d730f0b6382161ca0420471b15c",
  "[\"roman-1962\",\"lent-4-thursday\",\"main\",\"Oratio super populum\",\"all\",1]": "3d4b47031b525b12672c8bd169d51e0401ab383565c921ac7adc23257a68048d",
  "[\"roman-1962\",\"lent-4-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "f53455bf25faa9e8d6d4bee64b152a660159541c796d47f6f52cd7d49628fc09",
  "[\"roman-1962\",\"lent-4-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "e1d79e4b435542003d45d89714bec1f6f32c122680bf3edd113d4c2e9516dbca",
  "[\"roman-1962\",\"mass-of-the-lords-supper\",\"main\",\"Collect\",\"all\",1]": "626f15e00cb7fe114235e6711d242661dd217d79ae4e1da01ac1861bac2f78ab",
  "[\"roman-1962\",\"missa-de-s-maria-in-sabbato-3\",\"main\",\"Postcommunion\",\"all\",1]": "d2bbcd60da727fc8dd7218cf5a4e465f1c8ea113e613e1580c0f910c405735a9",
  "[\"roman-1962\",\"most-holy-name-of-jesus\",\"main\",\"Collect\",\"all\",1]": "38c6b30899dfef4f613dd942fcb9c330c3cfd57c33737750f50cd020ddfa465d",
  "[\"roman-1962\",\"most-holy-name-of-jesus\",\"main\",\"Postcommunion\",\"all\",1]": "1950c03ffa7a759a50b3d9987332c452643a0ee656815360c750a4019ef2d8d4",
  "[\"roman-1962\",\"most-holy-name-of-jesus\",\"main\",\"Secret\",\"all\",1]": "f65bcbe5305f61727c4e3e6221fb2d8fcb56b11d674d441c5ceba0d2b8613196",
  "[\"roman-1962\",\"nativitate-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "9469248f817b2153a9e3016ad92a30a8d1b86a6e627f369eeeaae648e5c803f6",
  "[\"roman-1962\",\"nativitate-domini-octave\",\"day\",\"Collect\",\"all\",1]": "256042e76685d5efbd50d3f61b08e35ab25cee4cb01cba44c30ffc620c8894b5",
  "[\"roman-1962\",\"nativitate-domini-octave\",\"day\",\"Postcommunion\",\"all\",1]": "45f572d9c24286d7d9b9427790db8ebdfba01c8c2f5f6f6409a13942dcf69730",
  "[\"roman-1962\",\"nativitate-domini-octave\",\"day\",\"Secret\",\"all\",1]": "de959babb461645a6650b38e3f2ff90005d66fe0875b8a4da98a1d25dd31e427",
  "[\"roman-1962\",\"palm-sunday\",\"main\",\"Collect\",\"all\",1]": "8889aa85237fea5ea392b282a0f4c7c8f623a3d9efd9fa95a71da05183e11a57",
  "[\"roman-1962\",\"passion-friday\",\"main\",\"Oratio super populum\",\"all\",1]": "d039309069e04219f356071901782f05b40f607c9127c69763b1f3f773215116",
  "[\"roman-1962\",\"passion-monday\",\"main\",\"Oratio super populum\",\"all\",1]": "432c96a0bbe021c2988eb21a3826ffe2b8f53b35cda0165acf55b97c5ffd2667",
  "[\"roman-1962\",\"passion-saturday\",\"main\",\"Oratio super populum\",\"all\",1]": "5695a9b67e6a8105c6e15ae094688545688fdd6688c07d529a404c633d9059ed",
  "[\"roman-1962\",\"passion-thursday\",\"main\",\"Collect\",\"all\",1]": "896481745b5177bc1ad0d2b866a66216b0ed506de150e731f3bf31f57224305f",
  "[\"roman-1962\",\"passion-thursday\",\"main\",\"Oratio super populum\",\"all\",1]": "7a59e398ac3cc7e8fc6ad75e0b8e129d2bca072daa60dca48f1d4e1e1de3ea7e",
  "[\"roman-1962\",\"passion-tuesday\",\"main\",\"Oratio super populum\",\"all\",1]": "80623fd92e59c2cf20bb2a89fe3e9e5ecd94f270c614da697933586a9ac60801",
  "[\"roman-1962\",\"passion-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "7cc13667a54f2e9c2f83a47cabadeffa086c7f8c2f1d019077d201528c8113fc",
  "[\"roman-1962\",\"pentecost-13\",\"main\",\"Collect\",\"all\",1]": "d82121166c8e44d1af20154eb892d23abcc72971f2893327777e04be5654eccc",
  "[\"roman-1962\",\"pentecost-13\",\"main\",\"Postcommunion\",\"all\",1]": "612ce41c39729b8274e746ae70553a308a0a73811488ba3afe09afb1061b28c8",
  "[\"roman-1962\",\"pentecost-13\",\"main\",\"Secret\",\"all\",1]": "bc82de457e17d6582c320719dd115b26e697a623769b9c5c0c9812f19b4cbbff",
  "[\"roman-1962\",\"pentecost-14\",\"main\",\"Collect\",\"all\",1]": "743e8e94ce96013c407699771b81dfe2f61a9284342fe1953a2a6a890f0e167d",
  "[\"roman-1962\",\"pentecost-14\",\"main\",\"Postcommunion\",\"all\",1]": "883be5d0f085068cf1a1ef586fade2bde2b475e7e3fb34c2672adaca52ec6a4b",
  "[\"roman-1962\",\"pentecost-14\",\"main\",\"Secret\",\"all\",1]": "c4cce1a2fa571e2e4bb69f3852cfec40edc5bc038ee69faee064d8c45aabcedb",
  "[\"roman-1962\",\"pentecost-15\",\"main\",\"Collect\",\"all\",1]": "d307984f176105b068c1841d1cffb53083e99bd9d11bf54c7e53da0d02be9896",
  "[\"roman-1962\",\"pentecost-15\",\"main\",\"Postcommunion\",\"all\",1]": "bc728cda88f315680b9ad089d6ebdf9904343ed70a87acea81dd8314245c4614",
  "[\"roman-1962\",\"pentecost-15\",\"main\",\"Secret\",\"all\",1]": "1f9fac8bcc8cf3f7635f95355dcedc3d786e494c680791ab3a14f49cc6f7f288",
  "[\"roman-1962\",\"pentecost-19\",\"main\",\"Collect\",\"all\",1]": "b6eb3c3458a563cd383384db4e79d608b983480de86af8c902a14180efcdb212",
  "[\"roman-1962\",\"pentecost-19\",\"main\",\"Postcommunion\",\"all\",1]": "251a0bbdf52279d16bab8be0c21878ac0e1382b368e2cd23bbf2d12171e47177",
  "[\"roman-1962\",\"pentecost-19\",\"main\",\"Secret\",\"all\",1]": "87e30afceb563e83eedc42026db88896b58390686506ca66d912b1c1c594e181",
  "[\"roman-1962\",\"pentecost-2\",\"main\",\"Collect\",\"all\",1]": "e9d1e025164919b319a334b42127dc0dca8f4e08c19b581fbe601714b1e6c86f",
  "[\"roman-1962\",\"pentecost-8\",\"main\",\"Collect\",\"all\",1]": "1d4ed4651c92c52e87c018f035fc9b92b709347384647f7aef13d48505d62eb2",
  "[\"roman-1962\",\"pentecost-9\",\"main\",\"Collect\",\"all\",1]": "01fc3b8f8051dc4bbbe944a0a6544e623576f7f39100bd283538770e297e3b85",
  "[\"roman-1962\",\"pentecost-monday\",\"main\",\"Postcommunion\",\"all\",1]": "e921f740de5085a3720c4674f84325cd0ae5b7ae7deb43680f08e11b8caeaac9",
  "[\"roman-1962\",\"pentecost-monday\",\"main\",\"Secret\",\"all\",1]": "1c18f8554c4db89f44edd64ba0e306d852b55a708c822929cf70f64baf2c4913",
  "[\"roman-1962\",\"pentecost-tuesday\",\"main\",\"Secret\",\"all\",1]": "0aa084261dc9a56a11a0f21f520e109e39f6e1cc8a096b509098b81d4461a559",
  "[\"roman-1962\",\"praesentatione-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "3669ad99883d5539f5800f50671e949c7fc7c3edeb81ed28210b871db23b23b9",
  "[\"roman-1962\",\"praesentatione-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "f91fc3789943cee9e7be82ba6e1ecfa1e809dbda1fc4abe41047899bcf3d49d8",
  "[\"roman-1962\",\"s-alfonsi-mariae-ligorio-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "e604bcc1bbe2222970baa5d9c09422403c734ca1d7b63d067c6ef7c83121b89b",
  "[\"roman-1962\",\"s-alfonsi-mariae-ligorio-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "1d91a49a80dae0680917a53f9d05bb281fd133b0555df2e6c89339cf1bbd3cc3",
  "[\"roman-1962\",\"s-alfonsi-mariae-ligorio-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "a553c153e03eaffdeacc5f9bbd4f4181d8f5a2cc35ac7d4749d752753c48ac38",
  "[\"roman-1962\",\"s-aloisii-gonzagae-confessoris\",\"main\",\"Collect\",\"all\",1]": "8c15afdc5847bde643eeb86c2a8d26b8f12db7d216908d0c4f9779af4107d069",
  "[\"roman-1962\",\"s-andreae-avellini-confessoris\",\"main\",\"Collect\",\"all\",1]": "8e28b8654cf4cf502d1c0e310a5660ba61b98e1f241da0d888cbc2793a6cfd16",
  "[\"roman-1962\",\"s-angelae-mericiae-virginis\",\"main\",\"Collect\",\"all\",1]": "379a55ee88b1614433d964cd6c482d07b6af82178702d3251e0fceab38d4242c",
  "[\"roman-1962\",\"s-antonii-abbatis\",\"main\",\"Collect\",\"all\",1]": "77d70d298cc227b203415ce01f4c4ed4a345a8f98919ae3d6a650c318fd044bf",
  "[\"roman-1962\",\"s-antonii-abbatis\",\"main\",\"Postcommunion\",\"all\",1]": "7f172978a5a14552be031850334ff9278b11fe90aee574fee8b2f82861b1da6b",
  "[\"roman-1962\",\"s-antonii-abbatis\",\"main\",\"Secret\",\"all\",1]": "f501eb55435b3674e2c4ee6a6cc5c3cde51095958056f74e1a2ddf5366ce1cff",
  "[\"roman-1962\",\"s-antonii-mariae-zaccaria-confessoris\",\"main\",\"Collect\",\"all\",1]": "578b599943eab5dc35e92a89a7475723da65e53e0f7f7516d98c8864ef6617c0",
  "[\"roman-1962\",\"s-antonii-padua-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "7be30283710f17ff60e050c0da8c5f10996327f96e2d2b6a1e79e6994e257d03",
  "[\"roman-1962\",\"s-antonii-padua-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "c4634c768b9d522e035c28318cc011152bcf823d884a93978ec307864bdc6c7a",
  "[\"roman-1962\",\"s-antonini-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "682f12db68c1b0383176c0d1ab81f51b9ee25742c4558c0657b006256717442a",
  "[\"roman-1962\",\"s-augustini-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "8b20d3a750669bda4a2184db8ea3f9a9a400e133e19f5f9454658e642ef0c42b",
  "[\"roman-1962\",\"s-augustini-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "67dd552bbd3475097dac61e33232b445358080e6c21a8090893d3fa1ded6a3aa",
  "[\"roman-1962\",\"s-augustini-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "de2af8369bc110c6878ee56c8d78879708622f467de7c01401d8939d0c580576",
  "[\"roman-1962\",\"s-basilii-magni-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "d75eaaf491deeeb3df1ce2bd5521ac679bc7c2200394fa910e64546413ee66ae",
  "[\"roman-1962\",\"s-basilii-magni-episcopi-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "303c862797bdd79cbf6187a727ddb23c97ca5e5eda7d9759a5622a51a5c17d04",
  "[\"roman-1962\",\"s-basilii-magni-episcopi-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "97c42b54cdf1f16a176f161ac84cf3ee6e60d4f8decd02bdff0d6de5a4956c34",
  "[\"roman-1962\",\"s-bedae-venerabilis-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "be82a084082594de1c9fb3f8fe27ec500a45471a7f9f8f17de9755ae23e726af",
  "[\"roman-1962\",\"s-bernardi-abbatis-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "c0835f3ab5e30709fbd0a990abccb49c232197762f9da832a08c583b2d62d7d2",
  "[\"roman-1962\",\"s-bernardi-abbatis-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "af300034cc24ceb76c8f71cd749cf71e94b1bf081a87dd4eafde911c74d15398",
  "[\"roman-1962\",\"s-bernardi-abbatis-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "253444cb3aefe4d6ac652ed7f7c369eec008b376f1309aa97a8a7b757fb65b1d",
  "[\"roman-1962\",\"s-bernardini-senensis-confessoris\",\"main\",\"Secret\",\"all\",1]": "bc9ac84a2e64b38703ecbbd12f319ddb6dab4ae2615a5a83c3de171586e77214",
  "[\"roman-1962\",\"s-bibianae-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "fda07a1454cfab1cc8a5987b77d9ea0a85e333b973d9cf7474a61c41a695867f",
  "[\"roman-1962\",\"s-bibianae-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "4c8f211960cd0ec6516917e6485352ca38ac4dd3d4d03402562b0a2a2239a1db",
  "[\"roman-1962\",\"s-birgittae-viduae\",\"main\",\"Collect\",\"all\",1]": "75877df4da926a64d50f736f6c7985b0e3540a8720375ddd85e80e279982d848",
  "[\"roman-1962\",\"s-bonaventurae-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "a7c7826d12eecea9396b84473318d6d24629ca7ae9d772de617527398c0d6504",
  "[\"roman-1962\",\"s-bonaventurae-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "8fa46b9f3d2ce3caced0ca2edb20a7ae2251e93a6e838e97aa0a22ff9a252fa9",
  "[\"roman-1962\",\"s-bonaventurae-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "fc53b58bd637c2a8b66c8ecc1970fa4a2cff7822818264b084f4fa19a75ee018",
  "[\"roman-1962\",\"s-brunonis-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "13ec5cb90e6f7537cd0d27be9332fa6778c364406d77902679ea950250938524",
  "[\"roman-1962\",\"s-camilli-lellis-confessoris\",\"main\",\"Secret\",\"all\",1]": "b2e1df209039a8f760782b2b750531a544e60659e79625a5d117f45c0b4e63ac",
  "[\"roman-1962\",\"s-catharinae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "744ac43094944565df834c45c8c8c0022de8e598c1cd3d2eed7828f807fd9beb",
  "[\"roman-1962\",\"s-clementis-i-papae-martyris\",\"main\",\"Collect\",\"all\",1]": "a0784958bdb3facdb85ba50be97513a9b19a26ec0570fb9fa56673fbac6dddc9",
  "[\"roman-1962\",\"s-clementis-i-papae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "45357a13aca9e327c278dd04a2c39cd6e574c84cdffae8d5618520c778139916",
  "[\"roman-1962\",\"s-clementis-i-papae-martyris\",\"main\",\"Secret\",\"all\",1]": "fcc83c9e48ccb890d63396812ff8c395d6b8778bc2e20eb254567eff247e0af8",
  "[\"roman-1962\",\"s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "7eef65db4a02f359ac5363aa4eda7921c249d73b5c012dd87a4d11d2e9f44ba7",
  "[\"roman-1962\",\"s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "3dda64dbfb33f1264795aa49fa68a90185fd40bb117ca74dba991e4384181a7e",
  "[\"roman-1962\",\"s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "adf5ef6cd5f1f3c843af36f4e5b7bf4d2809ca96600d8b2812d156c73684f171",
  "[\"roman-1962\",\"s-damasi-i-papae-confessoris\",\"main\",\"Collect\",\"all\",1]": "d2ea5b4aac0408a8d965f0dee9ed2133b3731e48512809ee5288a8d3baecced7",
  "[\"roman-1962\",\"s-ephraem-syri-diaconi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "af0b50f69f1293bf7b8fdbb8e2553df662f8d54b1fef550862875cb099cb4f82",
  "[\"roman-1962\",\"s-fidelis-sigmaringa-martyris\",\"main\",\"Collect\",\"all\",1]": "cc9c48265ff7bb68c06f61b56a14b73cd8a31cfe968722c248bb98c155df6fbe",
  "[\"roman-1962\",\"s-francisci-borgiae-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "fa02e962e54a8da83c7c9d850f092e584f4a4dde64b56b6a6f82531eabc0a4f4",
  "[\"roman-1962\",\"s-francisci-borgiae-confessoris\",\"main\",\"Secret\",\"all\",1]": "91e4eed89234fcacb81db7ffa4921ff180cdf054825fed6d9de726894c41d464",
  "[\"roman-1962\",\"s-gregorii-i-papae-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "ce06b42fc2840a456c8671793a4291d6fd4ce69b796705e305f4dcda45604bb1",
  "[\"roman-1962\",\"s-gregorii-nazianzeni-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "ab9ccbfa003ac4e017ed3767e2aea605963cd48480d110940de5c72dae585d42",
  "[\"roman-1962\",\"s-gregorii-nazianzeni-episcopi-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "a9dea6fa85ea2f9ae96eaf5ee6441256a3822935d321b3f3de43d1e7ffc5ec70",
  "[\"roman-1962\",\"s-gregorii-nazianzeni-episcopi-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "f164fa1a00e741d7d3cb5d5ce808c04d3ef0e19c81a9564c9322ed61075a9e8e",
  "[\"roman-1962\",\"s-gregorii-thaumaturgi-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "378b70eaf56c4c71fd142f967b8327b8499bd87a0b186aa80060ec38d6c0d6f6",
  "[\"roman-1962\",\"s-gregorii-thaumaturgi-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "0b8af39c500086c9625793f282cd5778d54dcb7a664935a1d0665dee212a27e2",
  "[\"roman-1962\",\"s-gregorii-vii-papae-confessoris\",\"main\",\"Collect\",\"all\",1]": "8cd3459219a60acb104878a12760c2803dd4ba880dd424dee875e44884c0d780",
  "[\"roman-1962\",\"s-hermenegildi-martyris\",\"main\",\"Secret\",\"all\",1]": "4f8e258826c61ec6fc8554cc5bb11107a3866965ce97fe1fa04c0dc58441a081",
  "[\"roman-1962\",\"s-hilarii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "1bd59a8f77ec2eb3956dbd5912e1fd42ac16f299d805137c68dbd688d2b32ce3",
  "[\"roman-1962\",\"s-hilarii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "03cbe51bb7f06cc15d9b49fb3744b09e74f1d88fa6cc96b4d3d060599cd14f62",
  "[\"roman-1962\",\"s-hilarii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "9ee00bec303fe6b6198d493044c6317762e8f917f11a3a6b1680ebe9ad0f6dc6",
  "[\"roman-1962\",\"s-ioachim-patris-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "2f9f36f98158a3ebdff67fb165f4eaf19728489cbee1e4880601e0f719002c55",
  "[\"roman-1962\",\"s-ioannae-franciscae-fremiot-chantal-viduae\",\"main\",\"Collect\",\"all\",1]": "de20d5fe64da07047d9b1db3e2cea0bd93bc640845bf981c1b00073b2d2ebabb",
  "[\"roman-1962\",\"s-ioannis-a-deo-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "6b0623ca46234b137e38d819bd4db0d1a3f49c514a4db53b54c3424e58e37fe3",
  "[\"roman-1962\",\"s-ioannis-baptistae-la-salle-confessoris\",\"main\",\"Secret\",\"all\",1]": "eadf7a9fd885d0cb8b7ef978e8273d7d2215d0a8f207166f29c6bc8dede4e3bf",
  "[\"roman-1962\",\"s-ioannis-bosco-confessoris\",\"main\",\"Collect\",\"all\",1]": "02cee35139e035765f9f21f6e67f82ae69ec52ac1cefaadf07be9cc090ac03ab",
  "[\"roman-1962\",\"s-ioannis-bosco-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "a4157f82b577381df76ef7e74c1cb86fbd84110bfe16e95a43832cd0aa147207",
  "[\"roman-1962\",\"s-ioannis-bosco-confessoris\",\"main\",\"Secret\",\"all\",1]": "d24408f23cdbc79cdb378136fae94c20e062592ca6a8f413701347e631ed4bb2",
  "[\"roman-1962\",\"s-ioannis-capistrano-confessoris\",\"main\",\"Collect\",\"all\",1]": "70f359af9e9d2255c48c7f6238fbf0e91e463a1e40322c0f1866b657327f9fdb",
  "[\"roman-1962\",\"s-ioannis-chrysostomi-episcopi-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "9598d493329665cfe60606a5e6179c986ca6bbd4830fff30e024eafabe671165",
  "[\"roman-1962\",\"s-ioannis-chrysostomi-episcopi-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "3d7c12288732f5923d29a1be0f6f82ab22864bcd11418721bfc46f582c39e3c6",
  "[\"roman-1962\",\"s-ioannis-damasceni-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "08088f4f816d0be6ace0a70fca389bf429ebec06c3a82b7eeb88d7e0856c13f1",
  "[\"roman-1962\",\"s-ioannis-eudes-confessoris\",\"main\",\"Collect\",\"all\",1]": "546562f12b9475fd23f087c4add0bc507133098a6d780406ca166a97175590ab",
  "[\"roman-1962\",\"s-ioannis-gualberti-abbatis\",\"main\",\"Collect\",\"all\",1]": "4e50d57d442690d5042a5dfef6fa75c3edf1d4f0cffab6d2e6b0fa9bf2a5d7eb",
  "[\"roman-1962\",\"s-ioannis-gualberti-abbatis\",\"main\",\"Postcommunion\",\"all\",1]": "bf030e1968cce76e6f75326eac1fb4e11b22c99a36e2e15ec68d53740772c794",
  "[\"roman-1962\",\"s-ioannis-gualberti-abbatis\",\"main\",\"Secret\",\"all\",1]": "6decb2d6cfaf44005b86c505e561d1960ca75cb9fe2858cfc8ed9c363a1a8ead",
  "[\"roman-1962\",\"s-ioannis-mariae-vianney-confessoris\",\"main\",\"Collect\",\"all\",1]": "916aefad97deaf465b08a56e97c54ebd88f065ce540d0a849d3020bacfdf66b3",
  "[\"roman-1962\",\"s-ioannis-matha-confessoris\",\"main\",\"Collect\",\"all\",1]": "eb2a3c242e4e5fb3ce68fcac07a9f2281bc46a5d4ba1e6448b2090488c07f819",
  "[\"roman-1962\",\"s-iosephi-cupertino-confessoris\",\"main\",\"Collect\",\"all\",1]": "917e39c0086d31656a9188f658a193a5dabe3620d750af7e814c6c12dcbcb6e9",
  "[\"roman-1962\",\"s-iosephi-cupertino-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "da4095b51c021b57bca5e23ae62880746114f2297a2930a72dcaa6b87d5362c1",
  "[\"roman-1962\",\"s-iosephi-cupertino-confessoris\",\"main\",\"Secret\",\"all\",1]": "4f260a0eebb232be46787cba090a4548f8d3be593003e8415448c5001d740cfe",
  "[\"roman-1962\",\"s-irenaei-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "1f079357336e14ad7feecb3b5ef4c39bf92526d4c85db8c36e2c389dc2ba5925",
  "[\"roman-1962\",\"s-iustini-martyris\",\"main\",\"Secret\",\"all\",1]": "f35c916d2506dfaaed7c0bb5fc0b8c420a93789933fc7eb26878ade9091b3618",
  "[\"roman-1962\",\"s-ludovici-regis-confessoris\",\"main\",\"Secret\",\"all\",1]": "575e9bb58f416d58d3b78d665139a8124c6fda1ceb7c64095c23064fe4da7566",
  "[\"roman-1962\",\"s-marcelli-i-papae-martyris\",\"main\",\"Collect\",\"all\",1]": "ca5882326e40ab5031e2f154b6dacf687f7a102d214a5d4e94bd62ac10eabeee",
  "[\"roman-1962\",\"s-margaritae-mariae-alacoque-virginis\",\"main\",\"Collect\",\"all\",1]": "d543fa2c77320e1c660f1666de47515bd875640fb54d979e18a05ddd4fd3a576",
  "[\"roman-1962\",\"s-margaritae-mariae-alacoque-virginis\",\"main\",\"Secret\",\"all\",1]": "293c8a76690edc59b248093cef80c4187af2fa64df448adeeae5d54a87000af3",
  "[\"roman-1962\",\"s-marthae-virginis\",\"main\",\"Collect\",\"all\",1]": "8a97a876bb9fb0586204184bfc679fe6449736789237206d728e25852b7135c7",
  "[\"roman-1962\",\"s-paschalis-baylon-confessoris\",\"main\",\"Collect\",\"all\",1]": "77216edddb20789dd00f7cfaa3479cc1e3dba47e3ed37ac103dfe423cfdd8ecd",
  "[\"roman-1962\",\"s-pauli-primi-eremitae-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "00d2e134095e0e4a8ef64c2270661e2d6070efe06393ee210353f2e88630494b",
  "[\"roman-1962\",\"s-pauli-primi-eremitae-confessoris\",\"main\",\"Secret\",\"all\",1]": "4c322ff06734c5dc4f2d76c29bf4f701228b3d8c1ef286732c06ca051acbe0a4",
  "[\"roman-1962\",\"s-petri-alcantara-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "3c930407632435d05da488c2745acc56f2249fef30c25323bf024a0a8248b6fb",
  "[\"roman-1962\",\"s-petri-caelestini-papae-confessoris\",\"main\",\"Collect\",\"all\",1]": "468113a642b4c8891cb3f0ce02833dab17cdef5f11fcc9988d93c77e83901281",
  "[\"roman-1962\",\"s-petri-canisii-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "8a4bd66022a0838c6617e05be5abe9afd0a66827ad8cb1f23dcecb8a525a1f88",
  "[\"roman-1962\",\"s-petri-chrysologi-episcopi-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "43b5e2a0bcd2d30cb64cb07a062420c9d57cf81910e30882ee99b51874ee9f2f",
  "[\"roman-1962\",\"s-petri-chrysologi-episcopi-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "19b33e3ff63b62337e834bc577715fd7c0bc86845cc39bc0e10c02b74dfac009",
  "[\"roman-1962\",\"s-petri-nolasci-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "55b017d754c2dfef14c6391a2147895797b103c9ed42d5fca2a505393e80791a",
  "[\"roman-1962\",\"s-petri-nolasci-confessoris\",\"main\",\"Secret\",\"all\",1]": "9b34fef126494e57727c174ab8cb13a80cb204798da61baca35927a520a2287f",
  "[\"roman-1962\",\"s-pii-x-papae-confessoris\",\"main\",\"Secret\",\"all\",1]": "71bcfb47904aede7538d0ec6bdbc76438524af9bd9d7f97ba0df3898d7cf44fc",
  "[\"roman-1962\",\"s-polycarpi-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "633fc8cadb7b11ea61577932773cd5e32ab18f5de8d28178ffab65128cf93867",
  "[\"roman-1962\",\"s-polycarpi-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "a5b5580ac51fd6efe1ef3161ad54cfb56f8c0db867755c8663d08256d07302a3",
  "[\"roman-1962\",\"s-polycarpi-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "257d9d76bee59c017bcfd4ec0ef6bceb691205138a6ce58b9eb2c96f69168d96",
  "[\"roman-1962\",\"s-raphaelis-archangeli\",\"main\",\"Collect\",\"all\",1]": "0bf3fb08b4ed53ab40822ab15b33f2ceaae8877b882f028faca0662f87d89e06",
  "[\"roman-1962\",\"s-rosae-limanae-virginis\",\"main\",\"Collect\",\"all\",1]": "dfe53f854c57f13d9a7fb6fef4f0c8a10b4b24a3355600a02eafdf54abf2a0cc",
  "[\"roman-1962\",\"s-silvestri-abbatis\",\"main\",\"Collect\",\"all\",1]": "3477553f21aea2da5c0e6d0ebcc180926bf53be2e0f8654355dcdd60d876c18f",
  "[\"roman-1962\",\"s-silvestri-abbatis\",\"main\",\"Postcommunion\",\"all\",1]": "2b860471a6c32eee68f454e784a7a28360fcca964caf93e20c69072b66d0f788",
  "[\"roman-1962\",\"s-silvestri-abbatis\",\"main\",\"Secret\",\"all\",1]": "ed352d3a21b0b9ffab511ed62ef21b1c3d5ea459cf5484e83a978ce25c2555b5",
  "[\"roman-1962\",\"s-stephani-regis-confessoris\",\"main\",\"Secret\",\"all\",1]": "ed58e9f6181bc6f11a6f0b4229dcea5228d2930e65f179df049a2f3a5ffebeeb",
  "[\"roman-1962\",\"s-teresiae-a-iesu-infante-virginis\",\"main\",\"Collect\",\"all\",1]": "acf555a468e3a189894180a41f05ed8814b0c74558368d2768d8ec819b32c903",
  "[\"roman-1962\",\"s-teresiae-a-iesu-infante-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "7818811b62fe5bdf44918bfa09924ed2b55b1d0063f0f40c6aab6558c57a649d",
  "[\"roman-1962\",\"s-teresiae-a-iesu-infante-virginis\",\"main\",\"Secret\",\"all\",1]": "16a1bc1c98d4869f1475efb2bf1082b60c0c295a873526d9d5eb292582fc2dd8",
  "[\"roman-1962\",\"s-teresiae-virginis\",\"main\",\"Collect\",\"all\",1]": "72e8b6489f295ce8d7e48ad9f6c668b4f5106db28635b6abb461f0899718ad05",
  "[\"roman-1962\",\"s-thomae-aquino-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "4d480c14c81a1dd7519e8572d497ae7be78f82af2d4ddda7b23362f696ba0d3c",
  "[\"roman-1962\",\"s-thomae-aquino-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "b08051e6c397bc8edb7355208c31f468348c09181fa40e91228a4ec7ce0d1b67",
  "[\"roman-1962\",\"s-timothei-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "526424fd4e6cbde624289f7e2863e5430131f79e31fdfa03dbfebe690e2b1597",
  "[\"roman-1962\",\"s-timothei-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "d34b90d7ebb6747d6445cf1f898ef485740bed9e3fad1427b3b1967034886cd4",
  "[\"roman-1962\",\"s-timothei-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "f468852584129c6136f5041b4f15687bf8dab296bc03d0414454d04f61f697d3",
  "[\"roman-1962\",\"s-titi-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "075609df468245e981abd3f67948ca7bec2172a85d2605a23a1e862089fda358",
  "[\"roman-1962\",\"s-vincentii-a-paulo-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "4f72381f6bd94e4f40f0a5c46b5ba4bc278345bdbf5242b7a6dcb3a95624c5df",
  "[\"roman-1962\",\"sanctissimi-nominis-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "cb173f1e51ea2e2aa9c7583998fd230a45c7037561adbd224a68940b13df8185",
  "[\"roman-1962\",\"sanctissimi-nominis-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "11cc79c6c789e7db39271c15a44fc72c37111aaf2963a5cd06b3065aa4e4a0c3",
  "[\"roman-1962\",\"saturday-after-ash-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "ac5199d5fdff8d1a84b286b972d0300df03aa523032ac3744751fb3331aa725d",
  "[\"roman-1962\",\"second-day-within-octave-s-stephani\",\"main\",\"Collect\",\"all\",1]": "3feb8fef99376003dda4cb6e1b2df30831696bbdea9a853086ba04cf5a6ce99f",
  "[\"roman-1962\",\"septem-dolorum-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "6991f0541243d95dbe50eb76fa28f6828390666801f2ae61b91da86acc093759",
  "[\"roman-1962\",\"september-ember-wednesday\",\"main\",\"Collect\",\"all\",1]": "c949481fce2d9af7e052cd6ab2a5dc8f6338b0e1713638a0ebda157e5d272f8d",
  "[\"roman-1962\",\"ss-cornelii-papae-cypriani-episcopi-martyrum\",\"main\",\"Collect\",\"all\",1]": "1141a05176d1ce6686a8698023778bebe67179bd0da12686598f82c7a1abacd3",
  "[\"roman-1962\",\"ss-cosmae-damiani-martyrum\",\"main\",\"Collect\",\"all\",1]": "7f59bfc0ee3b589b81d1ef2f5b1e54e9118276614da91ad07b99ec1127a0e163",
  "[\"roman-1962\",\"ss-fabiani-papae-sebastiani-martyrum\",\"main\",\"Secret\",\"all\",1]": "3c67ca9ebd8f43cf5a3eb6fd4dd4f12ed37c04cc5648deeae38a24fafca8c085",
  "[\"roman-1962\",\"ss-ianuarii-episcopi-sociorum-martyrum\",\"main\",\"Collect\",\"all\",1]": "518a0affb68af038ea30b2d165fcdb0af150a9f30977427684142f2effcddf03",
  "[\"roman-1962\",\"ss-ianuarii-episcopi-sociorum-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "8cecebb238e7a4e981bc733f4c0fa48884516ef13280cff51991c9d5bb0523e6",
  "[\"roman-1962\",\"ss-ianuarii-episcopi-sociorum-martyrum\",\"main\",\"Secret\",\"all\",1]": "853c09e0c84c60ee01e5e41a2a738742bc4236af933793273996cd1ad8e930fa",
  "[\"roman-1962\",\"ss-perpetuae-felicitatis-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "f4687f40aab680cb1db8b63798364f6e47db695896b697c6d13eeee2a078985d",
  "[\"roman-1962\",\"ss-philippi-iacobi-apostolorum\",\"main\",\"Collect\",\"all\",1]": "f0270395a5d5bb78eee5d98e80e3e4ee9d4b19e002f173b11f515fa9bde7582b",
  "[\"roman-1962\",\"ss-septem-fundatorum-ordinis-servorum-beatae\",\"main\",\"Collect\",\"all\",1]": "fb0bf67eab5de79fadab01a7a1bc8cca9e8b98041fbd023e6ed8785ce907505a",
  "[\"roman-1962\",\"ss-vincentii-anastasii-martyrum\",\"main\",\"Secret\",\"all\",1]": "ef31f5f8c257e9c5f8919fd9d7567090b394067f24726536f3e8a6c6ef414052",
  "[\"roman-1962\",\"thursday-after-ash-wednesday\",\"main\",\"Collect\",\"all\",1]": "48395b4660943ebcbcf72df5fe4ffa0fd36d63ac875748e805fc2fdc96f2b511",
  "[\"roman-1962\",\"thursday-after-ash-wednesday\",\"main\",\"Oratio super populum\",\"all\",1]": "b4ecfe9377907e05bf5691046cf48d88bc1b1748427ef9c90af352b7876c4460",
  "[\"roman-1962\",\"transfiguratione-domini-nostri-iesu-christi\",\"main\",\"Postcommunion\",\"all\",1]": "33156eb9eb7b3f569e7030bcf8fd592ef7e199d3d22e27a6d43b10a7bc3cd0a9",
  "[\"roman-1962\",\"vigil-nativity-lord\",\"main\",\"Collect\",\"all\",1]": "9388ec34144d8fb0bd785473b0c3850881a74aaeedac6a1b16ccd920c1eb41fa",
  "[\"roman-1962\",\"vigil-saints-peter-paul\",\"main\",\"Collect\",\"all\",1]": "919984baae4dd4d9432dbf21f24a6d2e51c748760d44a9bfe527348e886a1c0e",
  "[\"roman-1962\",\"vigil-saints-peter-paul\",\"main\",\"Secret\",\"all\",1]": "1675ff4fd154bf68d85d357ad6a560440f9688e2de22c57e4ddcc4bcf642645d",
  "[\"roman-1962\",\"visitatione-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "929b09a488b2ef07e17e254539ffbab4a654f466971acc03da293506708cb361",
  "[\"s-agathae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "2060ea4965722b4cd479455cbbc4a2abc2b7bd05abcbbcf5295980e196c40c9a",
  "[\"s-agathae-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "3dac6e467c61422827e8f4546f07272981b2a700c317407e76def5fab9bc6d14",
  "[\"s-agathae-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "4a2b95a3fd6fd9e27297901c11cbfaa980c9856ac346da469c9f9711ba912c45",
  "[\"s-agnetis-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "7b332b5fd6f5dc06c04347de30336d5bb9b79623ab64e818ad56974e680bb1f3",
  "[\"s-agnetis-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "f19e66f13ec0fecb57323c0b01e89d0d4fb587c71979f4c1626ce3a0ac1c205c",
  "[\"s-agnetis-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "6913405b606a6aede56e3222a853d7283ce0e79dc4ce692be74a8e1f86fbaf6f",
  "[\"s-aloisii-gonzagae-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "7c57792cdd8e220e114401c393326a8d43f61f25be3b7b3fcdc3e76d36ddfe97",
  "[\"s-aloisii-gonzagae-confessoris\",\"main\",\"Secret\",\"all\",1]": "dc9a5dec3550553e3cc2b777fd35433389d39ca9d7a72f4e3985a28b6265eaf2",
  "[\"s-ambrosii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "9207b0de0753c37c17a846ad7cfdaf8e971aadde2f6612d0a05885738ab170a5",
  "[\"s-ambrosii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "1f8cd0dd2965e38eeeef9d63aeac8046232831da866946d8fbef526943654bd6",
  "[\"s-ambrosii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "6cbe7522e6ee56c0b264dbae2d0d23197194159baf802dab1ac432a02ceb1ef3",
  "[\"s-andreae-apostoli\",\"main\",\"Collect\",\"all\",1]": "605784bb54018fad1354359b3855cbeb02f933428afa395eab957f8f5ea90c35",
  "[\"s-andreae-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "18b2c941cd703675c34c4210ee63c1528aaf412de89a6a1907c4cfd09e35d176",
  "[\"s-andreae-apostoli\",\"main\",\"Secret\",\"all\",1]": "19396aa7faa9b3b2ffae5f7bcb2d339ac9ef892879a491921d4fa2bfbfe193d1",
  "[\"s-andreae-avellini-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "247e67c3930463e3f340676ac005e0bfd6e9ca98e9e8ebac5023d5509ca11815",
  "[\"s-andreae-avellini-confessoris\",\"main\",\"Secret\",\"all\",1]": "3a780ad9f2393fa000a13741e199461d3faf992799ca133bf0aae13df9637f76",
  "[\"s-andreae-corsini-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "8f1b87577871428c6fda56576cc41167aae717da30d9d8d567255bf46c56322c",
  "[\"s-angelae-mericiae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "3a10648ce46004df22c94053fd0a4ac289ee3d1cce8292a6b5b66f087ceccd78",
  "[\"s-angelae-mericiae-virginis\",\"main\",\"Secret\",\"all\",1]": "351cc9100c8930e45347cdda0acab5f47cb34669a644b9c697a18d05af316f5f",
  "[\"s-annae-matris-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "f37e44e1b11061f3df1e74a3e2b893fd1adeceab0d2577aa78ed3bdda771fb30",
  "[\"s-annae-matris-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "9bb8bba57c0ce5d29907b3da175c71ae238605be9bd213f97d6f0ab93da80fa9",
  "[\"s-annae-matris-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "ae8febb216c9f4d531aeac4842256e3ad7924819248d270af7964bce5745d2bc",
  "[\"s-antonii-mariae-zaccaria-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "510635dc271dce5361e0c718285598d2115e5da17b1a39960e3d951d080d569c",
  "[\"s-antonii-mariae-zaccaria-confessoris\",\"main\",\"Secret\",\"all\",1]": "3611dbda5843b6f3b3a85e67c7b276a7f4dfef9be17218e92599f6ca4a29d044",
  "[\"s-antonini-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "9a3c91bc8d66f0fe987f13fb6835719d00056301a9fa98589a592a7f7efdcdcc",
  "[\"s-antonini-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "a72ad7591ba65e055b9dbaf3f3c6c823a26b096b79368f68effc0c5d9b27466a",
  "[\"s-apollinaris-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "bbe3805a1a89e092c3ab8d253b518c3efa48ffb81cf5d5a6e884924df80155e6",
  "[\"s-apollinaris-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "819449a678695d5fd23bcbec9171f376cea0594fb4ba9c1af9029bbe049ef3b3",
  "[\"s-apollinaris-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "6bdc59df3376cfae15295a9e1bb850317e661d79562bd85f16543698484946db",
  "[\"s-athanasii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "a16944bc505b72e6663d9a100e3b424316ac7fbb4ea798d766b2a5c3f875195d",
  "[\"s-athanasii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "acd46d2aa19ab2cfc5379707ed5d563a6fc619ec6e9152c663017954ceedbc41",
  "[\"s-athanasii-episcopi-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "4895ded0a8f4a4907135804880f9ddd7476f2b3ac2ec3616363610f9d9237224",
  "[\"s-augustini-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "dddbd1e0293a954647e9204a47565f08242c7a807d818940914009f568b7d01b",
  "[\"s-augustini-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "f7bcfbb6862310839fbcb6edfa76c35ed2943fb472b223df73b3ef8915eda1a3",
  "[\"s-augustini-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "4efaaf8de824203191d59ed3f6aa085623de92ec9266f5ef417c9d9a0f804b1d",
  "[\"s-barnabae-apostoli\",\"main\",\"Collect\",\"all\",1]": "dac823d03602079c20913074fba436c71c105c83a5809bc84a5bbe78f8343985",
  "[\"s-barnabae-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "b070416d10379fccc87b73e384b2648d5f0dd3cf2941907d69c916d930a61f86",
  "[\"s-barnabae-apostoli\",\"main\",\"Secret\",\"all\",1]": "72ce7c8566cc66c1879a0039ef94181e54010c721e63dfda4a6a1755c51ef252",
  "[\"s-bartholomaei-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "3c0430283f634fabece7aa6a53ce8fb8d86fa35da159e026a9069baef4610659",
  "[\"s-bernardini-senensis-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "0278c99c900c87299ff5740c1693bbf8179e5478cfee45c7e127ae662efab734",
  "[\"s-bibianae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "d2f64fdc32b1b5800fed96001ddd714edd4e631922a8704be7e9bc2962c75d10",
  "[\"s-birgittae-viduae\",\"main\",\"Postcommunion\",\"all\",1]": "f7f83f1c9748c04682336a9ab31d58eed7f21397a90f703a544c019d62e412ba",
  "[\"s-birgittae-viduae\",\"main\",\"Secret\",\"all\",1]": "cec9f051e3873c2d39638cf33b60ce0aa10848301b1521906788b1cb0c2bff89",
  "[\"s-bonifatii-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "bc9674636ca0d89a167789ccf65f9c56cceff2c1895bea124f6b5bb82c9e4d3e",
  "[\"s-bonifatii-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "c1569a0b89e7369d83d343c8fe424cfaa05ade7a62aae0a2d3b8d68e5d02b9fb",
  "[\"s-bonifatii-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "c5a73a5c688b250818418f8831d2df45927cda5ae5505eb08739e3ace4e50b61",
  "[\"s-brunonis-confessoris\",\"main\",\"Collect\",\"all\",1]": "34109a3f727a6038c7265aed5ce011593ec07d7a19b51ad924f83d3da3109a23",
  "[\"s-caeciliae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "38dd281b7b132b801d2f30e0305b820ce0d220409732e0a83b7b50af0dbe7fc3",
  "[\"s-caeciliae-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "0615d6592df34369681acef5cbe3b39d0571a203462819e1191631f67a54b37a",
  "[\"s-caeciliae-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "9a633aac71fd356798d21da6fcf14b28af2e99bcd86a03a92cd429e983d24e57",
  "[\"s-caietani-confessoris\",\"main\",\"Collect\",\"all\",1]": "edac0991fe98eeeb7eae0914d280e5e4397ee112f98c88f518b7ea9dcf5a5207",
  "[\"s-caietani-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "feea2d6652a44ab055c587a44a805ceabc45fc63532b688bbd03fa272dae4989",
  "[\"s-caietani-confessoris\",\"main\",\"Secret\",\"all\",1]": "8e2b556ebd447cafe01a6c6ee522fd42322a238f5d283e221cbdd1c841c0142a",
  "[\"s-callisti-i-papae-martyris\",\"main\",\"Collect\",\"all\",1]": "5dff413b233a9aa5c4227a7744936f9394abc7a4fca9210764790508f9a64b0b",
  "[\"s-callisti-i-papae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "23f61994fed5d8f9fb6991c63baa12354fcb36ceec576677918b6b1f85faa8df",
  "[\"s-callisti-i-papae-martyris\",\"main\",\"Secret\",\"all\",1]": "22b46f0be7fdc10d3e3b9abb4253df40deb760c4a6d9f2c956897108b757e179",
  "[\"s-camilli-lellis-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "e410d8e5740d6fa5f11a693a67794c8c3121cc407a194d94b2e3323bdf932510",
  "[\"s-caroli-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "4e72a5c86f46a52faa176305ae77df0f7a607a90519ec42bbcaae2a515b24c56",
  "[\"s-casimiri-confessoris\",\"main\",\"Collect\",\"all\",1]": "1386a6d8f4ff88e16c681b921b39c07b40de86a6d8c7f71d4444534ddc188df9",
  "[\"s-catharinae-senensis-virginis\",\"main\",\"Collect\",\"all\",1]": "2777647c5499efa4f5b8dc03b9ba91fb753cc72c8a2247f4854249e87dae61e0",
  "[\"s-catharinae-senensis-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "b6d4276f105511ddf152e49511946bea4ae6c7e1429017c93e011b08d66eae8c",
  "[\"s-catharinae-senensis-virginis\",\"main\",\"Secret\",\"all\",1]": "be4b68bcfa26e2df22b18f56fb0efcefd7c4cd5ed2fe091e7a976aecd24be28f",
  "[\"s-cyrilli-episcopi-hierosolymitani-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "a6236f6c8f81329e2d65eb5a5c3b441da84f61be1999d53e383f88ae69ec8658",
  "[\"s-cyrilli-episcopi-hierosolymitani-confessoris-ecclesiae\",\"main\",\"Postcommunion\",\"all\",1]": "c0bf46068fa64cb1f1cf8b7f39c26788771f27c5d0d0f5f339be90d9fae51e94",
  "[\"s-cyrilli-episcopi-hierosolymitani-confessoris-ecclesiae\",\"main\",\"Secret\",\"all\",1]": "9fb1c0f3d9da805cf0a4f9b064480aad4e60f276aa5c60934b9ef030fb17eff1",
  "[\"s-didaci-confessoris\",\"main\",\"Collect\",\"all\",1]": "89217b93e7333330e1a6b4514aaa2879d5008a29174f5070076ac75314abaaec",
  "[\"s-dominici-confessoris\",\"main\",\"Collect\",\"all\",1]": "deb659df1d18856d0cece9f4c5dc0a4b16c1a917ef1e0bf0bb9d952f15db87ed",
  "[\"s-dominici-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "384797084e72bda320a9b5a0c029c773e6f684a85e05ab115abe1f769d9dbf58",
  "[\"s-dominici-confessoris\",\"main\",\"Secret\",\"all\",1]": "ebdfc6f236426331d46ba07a813f33ccf7cf5a16c5d2b4f05212e13517b9ee41",
  "[\"s-eduardi-regis-confessoris\",\"main\",\"Collect\",\"all\",1]": "34aef74ed1f084a29c70859ab53c33648d0ac8b443e11957aa9c318ad56c5a3a",
  "[\"s-elisabeth-reginae-viduae\",\"main\",\"Collect\",\"all\",1]": "87dd0338bea9accecad423f48be19c199a361adfcba6486a6276b9b35bcd4ee9",
  "[\"s-elisabeth-viduae\",\"main\",\"Collect\",\"all\",1]": "67e9806eb94d05f5d56a02f24bc3024e1e723741a9878780494ea591d90ab464",
  "[\"s-felicis-valois-confessoris\",\"main\",\"Collect\",\"all\",1]": "7d30cc9f9d0363170f2629506de684eaba9a537016190c4876419c12f00105ad",
  "[\"s-franciscae-romanae-viduae\",\"main\",\"Collect\",\"all\",1]": "aaf1ec3eb36c4751c701131f425bc87a5fe1e66bdc6294a26de68fa6d66f2578",
  "[\"s-francisci-borgiae-confessoris\",\"main\",\"Collect\",\"all\",1]": "f9528324726451dc5aba4ea5aa421c38458e493be7d8a6c8ee5a69eb949fdc04",
  "[\"s-francisci-caracciolo-confessoris\",\"main\",\"Collect\",\"all\",1]": "ef5678fb61e86702ecc5d1a317755597a9817482f05c569f35d343dac1453a1a",
  "[\"s-francisci-caracciolo-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "0c4e19af3b7d15fc2676cfd0a0fbd73bd3362b500ca4e5c2af2318db5f5a79f9",
  "[\"s-francisci-caracciolo-confessoris\",\"main\",\"Secret\",\"all\",1]": "bd24375b0d48fd43ab823246efc41d3413260b9d2ea7800845e1d3ad7cb3e1a3",
  "[\"s-francisci-confessoris\",\"main\",\"Collect\",\"all\",1]": "32487dce471f35972afcfe42651eecd4b50c08525088656e2735d2fe7bfa13be",
  "[\"s-francisci-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "8754cd3cb5b6ebdde5bff446eb608419c4e1b233b508623c0418d0d3e08a0e7d",
  "[\"s-francisci-confessoris\",\"main\",\"Secret\",\"all\",1]": "c50bed657342fd5c1f71250a14d9cd88548d95ef7a97ed7c2c7a2636794bd15c",
  "[\"s-francisci-paula-confessoris\",\"main\",\"Collect\",\"all\",1]": "fac45e6de1603185f68b3c6b499804c0fdce440e62c426122bc4c3876ea5c41c",
  "[\"s-francisci-paula-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "ae2cb0ec4ba4aa4fc51f26b0f5807bcea2a3a8a997acb1ec5a0caaeb839d856e",
  "[\"s-francisci-paula-confessoris\",\"main\",\"Secret\",\"all\",1]": "46ef033655e6e470d2b94a3f98ea44f9d33471e36dbbbdb03e64315653d5183b",
  "[\"s-francisci-salesii-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "ab774a229075da0711ffe2142be19872204ff63f91bcaf5337c7f7f22562d4ac",
  "[\"s-francisci-xaverii-confessoris\",\"main\",\"Collect\",\"all\",1]": "88fbed378109a461818a1fb17eec4f02b97fa2bfea711755814e74612de39f56",
  "[\"s-francisci-xaverii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "91401df9c5168d33a5ed8ba0b3e77810642dcef948223c611dbaea4ba5f83efa",
  "[\"s-francisci-xaverii-confessoris\",\"main\",\"Secret\",\"all\",1]": "45484469789c89e0d691d2e0317323dd6af6e0d777b6d358bed4abaeb6f22592",
  "[\"s-gabrielis-a-virgine-perdolente-confessoris\",\"main\",\"Collect\",\"all\",1]": "03c7c03f22ba857f5814a802e26cc3e5b6434445705ee4a4b8c57286f6c36290",
  "[\"s-gabrielis-a-virgine-perdolente-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "09a6a49a4475d0b74d563a6514ea7e82e0833e2c81a2fd80b07ce395a48a41ca",
  "[\"s-gabrielis-a-virgine-perdolente-confessoris\",\"main\",\"Secret\",\"all\",1]": "266b328dca36b434e7120b412f372f2fc2d41787c8bace3faccb17c499840466",
  "[\"s-gabrielis-archangeli\",\"main\",\"Postcommunion\",\"all\",1]": "13532c133958f2cb6878b15d334e3741232a58702fbcb2edf4fef850eafdcdb0",
  "[\"s-gabrielis-archangeli\",\"main\",\"Secret\",\"all\",1]": "1171ba94867b2544baad9d9e572aa32513b2453c9bf25000a11eac1c74c006be",
  "[\"s-gertrudis-virginis\",\"main\",\"Collect\",\"all\",1]": "6bf52d5eac7c4e048a0a399270e97c573b334a43444d90aec88bf687035838ad",
  "[\"s-gregorii-i-papae-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "67b60586c82ac7a15696a0708cab0811822631186ba8447e684097a9f8013073",
  "[\"s-gregorii-thaumaturgi-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "b44abc36acf2d78c1829dbeed635aefc193d915635943438f044c63807f5bf59",
  "[\"s-gulielmi-abbatis\",\"main\",\"Collect\",\"all\",1]": "a2d6c38d57232c6c7988b7a53bef0dd87d80e572eb1942bed9a74ef689640e16",
  "[\"s-hedwigis-viduae\",\"main\",\"Collect\",\"all\",1]": "fb35a410ff14969a69093161180f14c2269c3f5a36499043084588a389ad9bb1",
  "[\"s-henrici-imperatoris-confessoris\",\"main\",\"Collect\",\"all\",1]": "ad4f9a349b2b496dd9dd569c08f42a716b722c5691e4bd19d47d2be18e4301b0",
  "[\"s-hermenegildi-martyris\",\"main\",\"Collect\",\"all\",1]": "fc5d7142a540d47d5f8e051fbcff5a7756690a5a42f1a60afbb3e0e724f16ad0",
  "[\"s-hermenegildi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "a2de85c426de07872050c73eee955504504e9d630da719278105cee902053eef",
  "[\"s-hieronymi-aemiliani-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "d89424fb7a6e29dfa6ecd5b421c53a80a71fdbd4d2a0cfa2e9a5aca44c381a87",
  "[\"s-hieronymi-aemiliani-confessoris\",\"main\",\"Secret\",\"all\",1]": "ec6e208e6068298a14b96b2419f1459ff58074ee31b05d1d834e7577df1fb891",
  "[\"s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "20e6650aa5d3b7c38aad2511efe9988d48331ad87eb6febeb78acf324ee0f582",
  "[\"s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "a15317ffa7609ebfb760f30217f4260163f513406a896dc7f6220f721f1d2d98",
  "[\"s-hieronymi-presbyteri-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "a13aa588c32b5fec3d4a2d1c5c08dcb12df821e6cc8f56c3373886b979dbb336",
  "[\"s-iacobi-apostoli\",\"main\",\"Collect\",\"all\",1]": "e93c7cf0d213561701cf3786675f02af044b60f8c1033cc415e9ab7382130a27",
  "[\"s-iacobi-apostoli\",\"main\",\"Secret\",\"all\",1]": "8f158bd7c5d7588f47d25636dadddda16af07c7ef865f454166da6fe0da1b42a",
  "[\"s-ignatii-confessoris\",\"main\",\"Collect\",\"all\",1]": "beea2077f9829b9792b310a193e37fefc8d244706ce808930ea2b513466d6464",
  "[\"s-ignatii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "1bf033b23b7058c6fd67f39f191cf1f4c0db132a47f23fd6a8b76028652c494b",
  "[\"s-ignatii-confessoris\",\"main\",\"Secret\",\"all\",1]": "85fbc5fe80ce5f9ae21af717e367d2bd4ac3a18bd0b265689eadddec1c106560",
  "[\"s-ignatii-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "d884538c68c6616ce3ab71854f93db2f366de9f10d2078ebe42503880ccd798c",
  "[\"s-ignatii-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "9925657a435234c0386b684a28082de6e0e4771742deec95f27887810f7e0472",
  "[\"s-ioachim-patris-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "672bd707ee5cefd90bf6504bb083cd74788d791be4119bf35e3c593349ae8ed0",
  "[\"s-ioannae-franciscae-fremiot-chantal-viduae\",\"main\",\"Secret\",\"all\",1]": "5648f8e963b34f31c196cefc9f8acd253b850dd977a3193d44bbbb41d50a1b21",
  "[\"s-ioannis-a-cruce-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "e8564efe733c47abeb20399abac4c71a7b7f7c302e1975ae7abdf0a1821ffaa7",
  "[\"s-ioannis-a-deo-confessoris\",\"main\",\"Collect\",\"all\",1]": "8ba7ba381ee08293a69687cf66c944926f8512cc61b58cf4bbedeedd688e3303",
  "[\"s-ioannis-a-deo-confessoris\",\"main\",\"Secret\",\"all\",1]": "b79b09251e3138bc6620964648b9f17290450cbc3b463c12c381b9572222e91b",
  "[\"s-ioannis-baptistae-la-salle-confessoris\",\"main\",\"Collect\",\"all\",1]": "d23b739e0d2128c30247644a179185fcab165569128bbe4ed73fbbc50828e564",
  "[\"s-ioannis-baptistae-la-salle-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "1e1d967f5345603d000da75c7f933f7591afac0b639e636795b3daad00e7b89a",
  "[\"s-ioannis-cantii-confessoris\",\"main\",\"Collect\",\"all\",1]": "7143980ddf234b5acc0ec4f7d67ac13303df4ebed5d20105b9befd117e134577",
  "[\"s-ioannis-cantii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "ffa54c2be7528cc742e98322abed21c33927754bc1d8ac9cd671322a9a4a13ca",
  "[\"s-ioannis-cantii-confessoris\",\"main\",\"Secret\",\"all\",1]": "47338361cacfa89a78ab9d2ab43d5887786c326c0fe950f60ea8eb470a4b1543",
  "[\"s-ioannis-capistrano-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "005c503ba912a8129935635e97277e4844532eb9f41071c7206cb65c1187b56a",
  "[\"s-ioannis-capistrano-confessoris\",\"main\",\"Secret\",\"all\",1]": "d21b7a033affd2ef673cf617f7a7b7045d921022630f802f04f0578efb9ffb3b",
  "[\"s-ioannis-chrysostomi-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "d1023bac2c09dc1965b80af84d61451038c3623f80bc45b7eb0bfe64bdc72604",
  "[\"s-ioannis-damasceni-confessoris-ecclesiae-doctoris\",\"main\",\"Postcommunion\",\"all\",1]": "4290fdeab0fbd03ba07140216b39345688de7b7fe67d943fb0d311a2c5d2d024",
  "[\"s-ioannis-damasceni-confessoris-ecclesiae-doctoris\",\"main\",\"Secret\",\"all\",1]": "61fb1502d0366693fb083a477ca2b9f8edf59349dbc7463157bdaf96b4f26366",
  "[\"s-ioannis-leonardi-confessoris\",\"main\",\"Collect\",\"all\",1]": "decb2d5dd48a6e82787c6ccf32b8c7cfde16baa9f8aa8a9b049adbe5183588db",
  "[\"s-ioannis-leonardi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "2e58ab00a7950f18bac436af71ccd61607a8eca1d4064ace2e9639dddbce19d6",
  "[\"s-ioannis-leonardi-confessoris\",\"main\",\"Secret\",\"all\",1]": "228f4cadece94ccadff358c273dba8f7c7d089acd97fb824111f358d171d5763",
  "[\"s-ioannis-s-facundo-confessoris\",\"main\",\"Collect\",\"all\",1]": "3b3944242bb229989fdd1d11c3f4366c53cbaa892aba4cb38c524e3c09bb61a6",
  "[\"s-iosaphat-episcopi-martyris\",\"main\",\"Secret\",\"all\",1]": "51caa17c30b339dbab3b59ac176d9b99449773c53a682529c4cdbfb89dddf924",
  "[\"s-ioseph-sponsi-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "56a7711fe14923fdf4b1af618bf8b1aa65f6ebd750dd92ac28deee711a02754b",
  "[\"s-ioseph-sponsi-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "465824cf4e87402fa67a412f086f03b26ca6d61926040e081cd310fdce355098",
  "[\"s-ioseph-sponsi-beatae-mariae-virginis\",\"main\",\"Secret\",\"all\",1]": "40d98f76662ce188f4548b874b2fa0385743174db7e8f1aadaf0ff74a4e01b33",
  "[\"s-iosephi-calasanctii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "24519454d3162b2740720d32c51da8193de1242d46592bf02d79ece4c7578567",
  "[\"s-iosephi-calasanctii-confessoris\",\"main\",\"Secret\",\"all\",1]": "98ea8b1443176c311df4201829b80617e7becd2c49956e75c541e2dfb8e15031",
  "[\"s-irenaei-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "6b5649f17a48a14743245fdb6a6a99fc96db954a57eaf589327057ad3905f071",
  "[\"s-irenaei-episcopi-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "d0ccd745adbe66dfaed5654fc936a4f13d6a95cd4e153b3bdc85429abf5e03b1",
  "[\"s-iulianae-falconeriis-virginis\",\"main\",\"Collect\",\"all\",1]": "949f555d112fd07fca25567fb6b9cc62cda3ca743aec940f8c904ab223b91f79",
  "[\"s-iustini-martyris\",\"main\",\"Collect\",\"all\",1]": "947f431bd35e3d0ac51a1a692e72b98d4a680c2a330fd30033b33b35c2329932",
  "[\"s-iustini-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "1e658ae867b18c12e475d87b2a3b85c615f3b9df06f1080680e389a2361f9c20",
  "[\"s-laurentii-martyris\",\"main\",\"Collect\",\"all\",1]": "497146ffd88c8ee2a33cc4ad401582cd892f1864a7fd2356216e97140bcaf4fd",
  "[\"s-laurentii-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "d2b1342926a5034359de4ad340f5e120a2c1c9207c6b5ac2d4a86e5f9a0defc6",
  "[\"s-laurentii-martyris\",\"main\",\"Secret\",\"all\",1]": "018cfc3461d1b4fb172303107ce061f078b11eb3f934eb077f99ac62a70ba16d",
  "[\"s-lucae-evangelistae\",\"main\",\"Collect\",\"all\",1]": "3a0a20ee5dab8101e5c50d0f0a57b283cbf6cb665426262c5fec64f7f6e67b59",
  "[\"s-lucae-evangelistae\",\"main\",\"Postcommunion\",\"all\",1]": "a545e19295cbc574604dc2c6b16227b6fda9bb0598b6cf30e561f291d369465f",
  "[\"s-lucae-evangelistae\",\"main\",\"Secret\",\"all\",1]": "2551873b5afdc7b1070417dd375bf37d466a0de09f939189826b028d08d513ff",
  "[\"s-luciae-virginis-martyris\",\"main\",\"Collect\",\"all\",1]": "5ba584cc5783a335eaafcc1cc399d1c2de84a83d43207a0b81ee033e125f58d1",
  "[\"s-luciae-virginis-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "baa42c2e67ddb164e968082d95302faec3341cffb56f805449f6dd8f76e8d184",
  "[\"s-luciae-virginis-martyris\",\"main\",\"Secret\",\"all\",1]": "e085e46f35a41b0b8567043d659f6dc42b6c408e269e7c8d5f4767eb34532250",
  "[\"s-ludovici-regis-confessoris\",\"main\",\"Collect\",\"all\",1]": "88f9a18059e216d91689905e28b97fb091fadbc3886314cd7ceb69db22381131",
  "[\"s-ludovici-regis-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "3207bec61dc6fb4aa0a3a1a1baf92577a2c85d08324797273c671c1c3725ce05",
  "[\"s-margaritae-mariae-alacoque-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "a89820cc639bd23641490541394b2ed1636dce4654cf80f4e6a1835612712998",
  "[\"s-margaritae-reginae-viduae\",\"main\",\"Collect\",\"all\",1]": "8ef4ef8d6d3d5042eca2ca92c4c0b5c6be847509e45edb8b27bdf623202b6fe8",
  "[\"s-mariae-magdalenae-paenitentis\",\"main\",\"Collect\",\"all\",1]": "a22f634031909948de13c6fd3a84f3c7e1dbe7b168649f8de45a1b8f321140a6",
  "[\"s-mariae-magdalenae-paenitentis\",\"main\",\"Postcommunion\",\"all\",1]": "f2cbc67652c504b34258f49f2748055c736f26f02cf630af471b2a361cbe89aa",
  "[\"s-mariae-magdalenae-paenitentis\",\"main\",\"Secret\",\"all\",1]": "fa668629792ee9eca8e786d01456dbb4efc1352a52f313934fdd84f6038f75ce",
  "[\"s-mariae-magdalenae-pazzis-virginis\",\"main\",\"Collect\",\"all\",1]": "475fec6b911e9ac920b3a3da7213b1808895ce553e2b891e98f77016407b2e16",
  "[\"s-marthae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "d1ff7f68f00b5ae41d5ae95636ac9a92523d03cebdd54c7995475195bf8868ea",
  "[\"s-marthae-virginis\",\"main\",\"Secret\",\"all\",1]": "217bc559f06fd038f563143ed9b323fb11c16ddaeb650e8a36dc9d144edad4fa",
  "[\"s-martini-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "7b32de6bded0cfce57a03819d68cd4dbdda85c71302e07f3a9c51a2f4a293a70",
  "[\"s-martini-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "1adfb9f66c6846e54b697de2fb33b0e54ef31b8067bd092476a7d0cdd5ba1fff",
  "[\"s-martini-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "681129505b959e19b7685f3e8832bfd5252b0776654f03de55d1fdad64e02e06",
  "[\"s-matthaei-apostoli-evangelistae\",\"main\",\"Collect\",\"all\",1]": "445ec6bf36eb7fd04e13a9e590f60ce1c9baa8bda7077f8c287247023cd80187",
  "[\"s-matthaei-apostoli-evangelistae\",\"main\",\"Postcommunion\",\"all\",1]": "e250bd8e7dd912e6826a1ce30d502e7bcc2882711002232c984b0aad6c69d1d2",
  "[\"s-matthaei-apostoli-evangelistae\",\"main\",\"Secret\",\"all\",1]": "70fe2438322e2197787fd106e7f334a4029dab1d64f654edfb9580d58490bf37",
  "[\"s-matthiae-apostoli\",\"main\",\"Collect\",\"all\",1]": "58447470f9866e3829d59a50006e96eb0ac901a3ae11d8070389870615b3fb38",
  "[\"s-matthiae-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "5fbad4320c8b905ffe5f425f425b89daa7497ef90c01ffb42206aee390b426a8",
  "[\"s-matthiae-apostoli\",\"main\",\"Secret\",\"all\",1]": "70397af8d95e8c97825d1d07200bc50ed14b5334c4ecb8d1f2c7153e6d362fe7",
  "[\"s-monicae-viduae\",\"main\",\"Collect\",\"all\",1]": "c535ec3388c43684b7836b30b81c8620e75a28e9f41cb69a4b0ec39f03ed1651",
  "[\"s-monicae-viduae\",\"main\",\"Postcommunion\",\"all\",1]": "bc8ff2241672e2111430166503c7cce64c0b076c0e4234fe1239362f1b736968",
  "[\"s-monicae-viduae\",\"main\",\"Secret\",\"all\",1]": "b970d5f0ac7f6379c0ce3d29074fdcab8e101d19f29bba261974d673f2704dd3",
  "[\"s-nicolai-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "2e9c89605bf8639d6e1abee9cd6011ac6b4dfd80e647bbfe4cbbfedf9d7990f1",
  "[\"s-nicolai-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "40cf5171be91137d8de78e26e868644b2530e6bea121795b2caa4000acd8ea88",
  "[\"s-nicolai-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "6c175a9716215be020b0d4e8eb4b5a9c6349141034ef74586bbc46f117c15e77",
  "[\"s-norberti-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "8a603a07b6d995cfe3b40e3021ceda89743340035b992ff84a48d4b9a944eece",
  "[\"s-patricii-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "7081dae67fdb902d52788d87131be413cd046ee16cd40880e4ef87247226395d",
  "[\"s-pauli-a-cruce-confessoris\",\"main\",\"Collect\",\"all\",1]": "f3e1d49bf944b9dde78dcd845d860331e4bb8960e71bee9b7be01c960ba9c337",
  "[\"s-pauli-a-cruce-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "bf7b4b159cf597a215f0fc67f7382d2840b136f5e37c5acac6d9673cc2104510",
  "[\"s-pauli-a-cruce-confessoris\",\"main\",\"Secret\",\"all\",1]": "0e9a8a94ee22cbe526dd16550b0070e1641972d04dd04b814e41cb140e9f6c48",
  "[\"s-pauli-primi-eremitae-confessoris\",\"main\",\"Collect\",\"all\",1]": "974c7ef574b33c1d1ad3ea132225c5497a7682c7eb7e3e8ee4e3e4622e7d6678",
  "[\"s-paulini-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "f2e6106535f599d74f90a36a818f35d451c318d30ac0484ff8947d5f0c2a742d",
  "[\"s-paulini-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "9ee55aa8d28d24983d09f3f4affdb176bdcc3a9c66f26436e9491258c243677a",
  "[\"s-paulini-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "df5a1b65ad12c9b4ed1d850ae7fb83e07666196c94053e6642160a1ab93fd8cf",
  "[\"s-petri-alcantara-confessoris\",\"main\",\"Collect\",\"all\",1]": "a3641ed7a670e269c62d288ca1a2ab83b4e385e89d58fd334c92354a3fada99d",
  "[\"s-petri-alcantara-confessoris\",\"main\",\"Secret\",\"all\",1]": "531415bd816bb7fe986f06526fe42f74139c8c1201e8e6c18d02b6c384f21bda",
  "[\"s-petri-chrysologi-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "0b7f55f0468e00e2da6c76a1e25123171583d4aeb96dba0d0d884bb07dda52ca",
  "[\"s-petri-damiani-episcopi-confessoris-ecclesiae\",\"main\",\"Collect\",\"all\",1]": "b306835772442cdf3919487b7a58d55ce82fc9563891984007796bc0c7d2cb14",
  "[\"s-petri-martyris\",\"main\",\"Collect\",\"all\",1]": "0bacd2c9f4c89e57e5a9b3442459b993fc2260d70eebb3faf2517cf5eba7a9f0",
  "[\"s-petri-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "18541755c640c1d5c9f915d49a07a219dcac5ed6872478b3d3da03e3b6e477e2",
  "[\"s-petri-martyris\",\"main\",\"Secret\",\"all\",1]": "a2a6d06b07c8fc7824e7d1bd89cffbec87d855bd13985718a4ca9552f51fb953",
  "[\"s-petri-nolasci-confessoris\",\"main\",\"Collect\",\"all\",1]": "7e1d078835dd5a9c9d8325a4e70b8322d77934eccc7c02d9bd8221a4db33509d",
  "[\"s-philippi-benitii-confessoris\",\"main\",\"Collect\",\"all\",1]": "17c344c5e9fe85586bf5fb7f1ec8f519a9a2a4f655f36d48b6f0f6beb2b08ef7",
  "[\"s-philippi-nerii-confessoris\",\"main\",\"Collect\",\"all\",1]": "391dbe67ee81b1f250a769b30101edd00b5ca5674dfbb5bce7d75cd8fb818333",
  "[\"s-philippi-nerii-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "1a6e3dd9b53efd6771b42754642c3964868d4154805d6c73441736cf6b17eb25",
  "[\"s-pii-v-papae-confessoris\",\"main\",\"Collect\",\"all\",1]": "a16e7a6e24d220800d0608bb24db64da6044ec5eca5ad680cf75ce221f1e0876",
  "[\"s-raphaelis-archangeli\",\"main\",\"Postcommunion\",\"all\",1]": "8362a03d04462f04f4100022277022bea4ba9bb4a03f2666a86b2480b004bd89",
  "[\"s-raphaelis-archangeli\",\"main\",\"Secret\",\"all\",1]": "796c6c133de9bde0d223f560f46603ed3ce3a99aa8692ef7badd682e8b07b9cd",
  "[\"s-raymundi-nonnati-confessoris\",\"main\",\"Collect\",\"all\",1]": "0090229cc64e7c45e1ad679d70a3084679ffc2da2c0b1594ec5e86ede96d91ae",
  "[\"s-raymundi-penafort-confessoris\",\"main\",\"Collect\",\"all\",1]": "47936436e74ff1b16cf00eff11c9cb409bf30d7e24d854336d7413d6e5158dca",
  "[\"s-scholasticae-virginis\",\"main\",\"Collect\",\"all\",1]": "ab570864e3cff9762b525b2c3b608d5d3139cf01f7b3663bbd475034a173092e",
  "[\"s-stanislai-episcopi-martyris\",\"main\",\"Collect\",\"all\",1]": "4129f8233b787682df211d3e625a892e3bcc450107ea412a9688429be5ac8773",
  "[\"s-stephani-regis-confessoris\",\"main\",\"Collect\",\"all\",1]": "15d586086841ce0d20c8b7598a43757f5f7a82a8ecc333c551fa60979b8e0f00",
  "[\"s-stephani-regis-confessoris\",\"main\",\"Postcommunion\",\"all\",1]": "e9332a6044afe188b91da5c1ad07bb40b057155c2623cbb678abf694bdc0e48e",
  "[\"s-thomae-apostoli\",\"main\",\"Collect\",\"all\",1]": "9b92433cf0434c60b14926c82d156713d3603139f5b10ef0a7550870c51585ed",
  "[\"s-thomae-apostoli\",\"main\",\"Postcommunion\",\"all\",1]": "63bd2e7d9b90771810429f3a427eecff91765781823d4f649f9facfcbca738ca",
  "[\"s-thomae-apostoli\",\"main\",\"Secret\",\"all\",1]": "13c7dbbfe51b85add7b532a66f8e80b15baba6db4ae653a783c6ff7ccd231bda",
  "[\"s-thomae-aquino-confessoris-ecclesiae-doctoris\",\"main\",\"Collect\",\"all\",1]": "e0500028833854bf077465595d2d23d0fc073e3c589a95bfa721e63526beb924",
  "[\"s-thomae-villanova-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "fc07c2db03312afdd04cdbeee558481dbba844a349aea7d8a8907b9776159534",
  "[\"s-titi-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "757b1ae85a673f60559e29edad026c5e02b8860fdd3e6851f02098c1c36c8992",
  "[\"s-titi-episcopi-confessoris\",\"main\",\"Secret\",\"all\",1]": "2feadb4f82085a586da7be357e65fb0a83843b328f0f0e05b4fa9b2e9647f39b",
  "[\"s-ubaldi-episcopi-confessoris\",\"main\",\"Collect\",\"all\",1]": "99d8f70472ac343e51b38344a3a8d365aadd429eda19c5f77396cc8f6f24239a",
  "[\"s-venantii-martyris\",\"main\",\"Collect\",\"all\",1]": "d70b41802fac7afacb7a408838b5651e6ce00858c9715d4e20b0f16cc82f463c",
  "[\"s-venantii-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "2eeaffa060da9a7fa2254925cd64fa3f087d1b0e3352659b0698e7217323f262",
  "[\"s-venantii-martyris\",\"main\",\"Secret\",\"all\",1]": "bb77354e9bcb8735c7372ea0ae47378f370497d06240d3830ede7e688e7dc300",
  "[\"s-vincentii-a-paulo-confessoris\",\"main\",\"Collect\",\"all\",1]": "0a614cf8986baa66fb4cdd3d4712a0e32211fdfee6c6c2ae02a430d87a772ca2",
  "[\"s-vincentii-a-paulo-confessoris\",\"main\",\"Secret\",\"all\",1]": "675603be12520f561d17da790f779e0e61ae4eb6b525f10d4a3d3a26cac08119",
  "[\"s-vincentii-ferrerii-confessoris\",\"main\",\"Collect\",\"all\",1]": "4028d2b68af4ae06c4fa7805dd0a4e32ffd52201fe2f90a4ee53a9ed97b7021a",
  "[\"s-wenceslai-ducis-martyris\",\"main\",\"Collect\",\"all\",1]": "60969ebfe837b8630836ad2e43fb30e21b97210112eaae8726313df52fda49c7",
  "[\"sacred-heart\",\"main\",\"Collect\",\"all\",1]": "6105bcd0f835cb03a73c89d2a757fc003830493a01ab76c63624fd86eb93e459",
  "[\"sacred-heart\",\"main\",\"Postcommunion\",\"all\",1]": "2742f0ba50648c5339bcb0e0b58f8da68075e37077491140d8f87afce82a6cf6",
  "[\"sacred-heart\",\"main\",\"Secret\",\"all\",1]": "da5bce77faeab7e78ece793176e91dd9d994eb6b0fd630171539cb37e4c0456c",
  "[\"sanctissimi-nominis-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "84ca590ba4de827ae53592e1b1fac2a9aef22f1d36a3257220a2883d63f2d22c",
  "[\"saturday-after-ash-wednesday\",\"main\",\"Collect\",\"all\",1]": "8059e3eeac79020e36318f4075b450f47d011e7fc20fba362299799597108f47",
  "[\"saturday-after-ash-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "e1bacb0d8d4a958a99da65b256a822542206021bf6866d795e8b6637c7e0319c",
  "[\"saturday-after-ash-wednesday\",\"main\",\"Secret\",\"all\",1]": "6999d59774f282a355a73f23048331a7e792ea07f073ac13c480e41af82f1b92",
  "[\"second-day-within-octave-s-stephani\",\"main\",\"Postcommunion\",\"all\",1]": "c400a904d988d15109e3d26c086276b66662ec5d45bb59b79cb714c4a31b01d1",
  "[\"second-day-within-octave-s-stephani\",\"main\",\"Secret\",\"all\",1]": "f3bc8196908efd0e776077a2645c4b5f420e1d4b6bb06b7727452a344c9662c9",
  "[\"septem-dolorum-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "e419ea8cdd42ced5ec33a9d923458f417b57486a95a38e0d4501af6968859f0a",
  "[\"septem-dolorum-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "f64126f2ad512c7c15463c9818b9a8cddf74c9eecf3d8e89722a514cad9d48cd",
  "[\"september-ember-friday\",\"main\",\"Collect\",\"all\",1]": "bfe2093d898fb91e38281ecbcfa66c5b0bda73bc7d6e0a592ad991652f1fd0a2",
  "[\"september-ember-friday\",\"main\",\"Postcommunion\",\"all\",1]": "8eee059008a018746ccb74fa46fa6e020ee0d1fe535cc03582a0b35d08cae1f9",
  "[\"september-ember-friday\",\"main\",\"Secret\",\"all\",1]": "5b1ce0d2b02c7f4dd09f3c68c633ebf7e2325e7b0f31bbc527c4c59664a73d31",
  "[\"september-ember-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "17bee48a578f6a6871e917c1c011b0d494168d806967da978fa4780183031dae",
  "[\"september-ember-wednesday\",\"main\",\"Secret\",\"all\",1]": "b6f6432ff3f565eaa36dbdccc7761eb2638dc2befd2a762850df2ce1229896fa",
  "[\"septuagesima\",\"main\",\"Collect\",\"all\",1]": "37c285566674fadcc443941694f0726ffc3226cafa7df4d1366536018b1ab4e7",
  "[\"septuagesima\",\"main\",\"Postcommunion\",\"all\",1]": "b657f3c0aa9d45fbe1252a8c346d1e3de6124e78d13d31572a7a91fdd6e73f92",
  "[\"septuagesima\",\"main\",\"Secret\",\"all\",1]": "8ddf824f451c6484f89ab52996a89bd59db0ab4f6907f58f8c63fafb08d5ac8a",
  "[\"sexagesima\",\"main\",\"Collect\",\"all\",1]": "34f139847ebf8178c1d5b79ef0d1ea343b5c76fb78bea44d76f0fd3fdd6d8545",
  "[\"sexagesima\",\"main\",\"Postcommunion\",\"all\",1]": "057205e4498dc3ce93e5094feac2ac888d5c3103699507bb98aea2c0c61041e5",
  "[\"sexagesima\",\"main\",\"Secret\",\"all\",1]": "160d41d72cb87ead780b6bc41ee4407c7091a64df7c3601f3069a3e1906c4ab1",
  "[\"ss-angelorum-custodum\",\"main\",\"Collect\",\"all\",1]": "65d324858d0a2cc60f7a995fbb06b99e6a2c110f18908698a7f1cb70c1870dc5",
  "[\"ss-angelorum-custodum\",\"main\",\"Postcommunion\",\"all\",1]": "54c4c38f8f05a86ed53a57bc375b03714a2a6bcd7028f3f8def17c1ddf44e4fc",
  "[\"ss-angelorum-custodum\",\"main\",\"Secret\",\"all\",1]": "d1e0c3f806236dee1539cb92a503db66e1f7dd4240441fcbe3cc947793b5b71b",
  "[\"ss-cosmae-damiani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "e892d080bff0407cabfce0a1959a1d9b3327df3784193b1df3a9ca2983f2d571",
  "[\"ss-cosmae-damiani-martyrum\",\"main\",\"Secret\",\"all\",1]": "5dddb62b6b837792f127325643cce0b16a4935404dbfc1d26e372605fd5d8baa",
  "[\"ss-cyrilli-methodii-episcoporum-confessorum\",\"main\",\"Collect\",\"all\",1]": "fed29a385c5394872a3cbf1bc33869733cc9c987bd92309ca0dce2e129245a9e",
  "[\"ss-cyrilli-methodii-episcoporum-confessorum\",\"main\",\"Postcommunion\",\"all\",1]": "1f7fc9ee3a256291a12f3e7a82dd8c13ddd8033245a6c928e566a7f138016db9",
  "[\"ss-cyrilli-methodii-episcoporum-confessorum\",\"main\",\"Secret\",\"all\",1]": "da8d592b7c725404fe5e9283913c1cf3c4864e48df5cd5ac83d7dddd3584c2b3",
  "[\"ss-fabiani-papae-sebastiani-martyrum\",\"main\",\"Collect\",\"all\",1]": "b7bba4c296128cd1a3f76e96f31a63ccbebd0006ed8dbb52bfbe62afd0ee63a7",
  "[\"ss-fabiani-papae-sebastiani-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "00d23b9fd3b8e6e51cb2d548ef817e6e6a5d2dd5ad091f5cadd7533cfc70ae44",
  "[\"ss-ioannis-pauli-martyrum\",\"main\",\"Collect\",\"all\",1]": "bcf80efbcb7ef5441efc5b5f18c0d3e157b9d9dfaef455cab9242fb02dd7f2ac",
  "[\"ss-ioannis-pauli-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "6b51a0d3b5774966b11cb8ff0c41ff869a9be4271c160c8b47ec59f516060cf6",
  "[\"ss-ioannis-pauli-martyrum\",\"main\",\"Secret\",\"all\",1]": "964a1d1da3f1901d22e4b661723b67a84c3835a08d1c2363fb78d90e1d68691d",
  "[\"ss-nazarii-celsi-martyrum-victoris-i\",\"main\",\"Collect\",\"all\",1]": "fdc6ebc397c4682283f7c1083781353213c4c446b2bacb273a0714fb2bb9d4d7",
  "[\"ss-nazarii-celsi-martyrum-victoris-i\",\"main\",\"Postcommunion\",\"all\",1]": "2549f26163193d95a43174a5920fb028ceb1d1285949746cae4b6669f20c2cd9",
  "[\"ss-nazarii-celsi-martyrum-victoris-i\",\"main\",\"Secret\",\"all\",1]": "e3c3399c4cd1e8bb718c4b8cde7e69e6be39ab6d06d560efafc64566063dd4be",
  "[\"ss-nerei-achillei-domitillae-virginis-atque\",\"main\",\"Collect\",\"all\",1]": "f4f3d0e86943e81ad09c15d6ef5fb29df6596fe100b38bc268ab19d2725331bc",
  "[\"ss-nerei-achillei-domitillae-virginis-atque\",\"main\",\"Postcommunion\",\"all\",1]": "973b45e500fe9191288c4afeb349b3afe58e49c4a65be0f0e31dc8cef9504281",
  "[\"ss-nerei-achillei-domitillae-virginis-atque\",\"main\",\"Secret\",\"all\",1]": "4f85777bb2e49a818f511a3240a6505f67bad2c5283a9f8d2ea17673e7bc3913",
  "[\"ss-petri-pauli-apostolorum\",\"main\",\"Collect\",\"all\",1]": "e836d96e98a946beae764d13c826c69ae2aa14cf952299f5e77cdbd6b1aad8f9",
  "[\"ss-petri-pauli-apostolorum\",\"main\",\"Postcommunion\",\"all\",1]": "6bf8651a855f174a1e68302567b5c15c8e3beccd11448177bd700617090b3fdc",
  "[\"ss-petri-pauli-apostolorum\",\"main\",\"Secret\",\"all\",1]": "fcaace8c4843081ad479621b2db26d56f3d476c9eabe63af22a0dca5ed4723ca",
  "[\"ss-philippi-iacobi-apostolorum\",\"main\",\"Postcommunion\",\"all\",1]": "f27aeb3ade536e6e1791b9b01af043a01d036ec5fa76a98d2c43372eee07a7b5",
  "[\"ss-philippi-iacobi-apostolorum\",\"main\",\"Secret\",\"all\",1]": "026e95d01ba029a52e6fdbbd3a0406f6f077efc0487fbd87fb306be87f90277d",
  "[\"ss-quadraginta-martyrum\",\"main\",\"Collect\",\"all\",1]": "c605d0b2dea0e5eb696c0dcbbd93f9b7d0c436d4953a1dd8f3ca1a62f7b6a6e6",
  "[\"ss-quadraginta-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "922a0c35c2d7d532cbb234ae049dc68eedacc4a0fe54fb68bfc479a7fbfdbc98",
  "[\"ss-quadraginta-martyrum\",\"main\",\"Secret\",\"all\",1]": "bf008a0c190e3ffe2bc8639e3343352876ecedcc739e119583b7c7973dc3f64f",
  "[\"ss-septem-fratrum-martyrum-ac-ss\",\"main\",\"Collect\",\"all\",1]": "0d3bd8fa3947376280b69b598b575bfb8afbfeb450806b3ff54d86034cb252f1",
  "[\"ss-septem-fratrum-martyrum-ac-ss\",\"main\",\"Postcommunion\",\"all\",1]": "4b6068d6b037f6f583f3cf1d590139a11fb2ea1f8f78213b0cdb1e7c66acc341",
  "[\"ss-septem-fratrum-martyrum-ac-ss\",\"main\",\"Secret\",\"all\",1]": "d65c711f59e4234e9fcee436593d717b8f29890c5fd1783ffc75beb7801db71e",
  "[\"ss-septem-fundatorum-ordinis-servorum-beatae\",\"main\",\"Postcommunion\",\"all\",1]": "ac79f9741c4eea47bd81d79af868e3ab373bbad0212ac9aedc8094650cd04719",
  "[\"ss-septem-fundatorum-ordinis-servorum-beatae\",\"main\",\"Secret\",\"all\",1]": "96bb445a3b8bf8eb069deaa6b71830ee00fd370a5c39e2e487fb1048e4125dcb",
  "[\"ss-simonis-iudae-apostolorum\",\"main\",\"Collect\",\"all\",1]": "d3deac020cc015b5df1b863a0e18ad7b7765cbe5472143851462ba61f9645225",
  "[\"ss-simonis-iudae-apostolorum\",\"main\",\"Postcommunion\",\"all\",1]": "82f598418da99d32fb37738573f7bfa33a3ad943722b92990ed6277d3c6b1127",
  "[\"ss-simonis-iudae-apostolorum\",\"main\",\"Secret\",\"all\",1]": "d05bdf38564819f1b7ac91b8f6db44a3124e752a64e118c7d207c177e76ad0f6",
  "[\"ss-vincentii-anastasii-martyrum\",\"main\",\"Collect\",\"all\",1]": "427a0c8ded0924fab387f035c2e81aab449f09d17868d774b17aa089fa93fd88",
  "[\"ss-vincentii-anastasii-martyrum\",\"main\",\"Postcommunion\",\"all\",1]": "bc0adc652f2fa4c6622f77f9b2dfa08613dfcf7eb437896897306159b8c656a5",
  "[\"sunday-after-ascension\",\"main\",\"Collect\",\"all\",1]": "1dc8daf6fca8625b90330a93d4c209ce66974af4bec9566bb5ca344d1b1f82c0",
  "[\"sunday-after-ascension\",\"main\",\"Postcommunion\",\"all\",1]": "d08586c280c7eeaea63df623cf4096b778bb960d7621506c7613a0755e4bddc9",
  "[\"sunday-after-ascension\",\"main\",\"Secret\",\"all\",1]": "faabac55d6614f0f4f60add76402f8fef86e66ef4b0a646ec8f669e14163e1fc",
  "[\"sunday-within-octave-of-nativity\",\"main\",\"Collect\",\"all\",1]": "690ad2098a9ca33f6bc1123db1b48a9659e7c1e78711a50abdb82226e30cb8a4",
  "[\"sunday-within-octave-of-nativity\",\"main\",\"Postcommunion\",\"all\",1]": "c05d9ab58ce6aba71dbd62dcc98059172753ea0b5012f262a0f569dba76c4d2d",
  "[\"sunday-within-octave-of-nativity\",\"main\",\"Secret\",\"all\",1]": "90d27d118f70256f5b5d0ecaed1b76a8156e05baf87261242ccf4feac99474fc",
  "[\"third-day-within-octave-s-ioannis\",\"main\",\"Collect\",\"all\",1]": "70bcae767d4c83db3f6059caf1c181311aded6c496b2fccad1b83d6e654e9432",
  "[\"third-day-within-octave-s-ioannis\",\"main\",\"Postcommunion\",\"all\",1]": "d5eef95795feb97c2d101ba7a49a816444660175b31ddb3e5062b307e5ac6990",
  "[\"third-day-within-octave-s-ioannis\",\"main\",\"Secret\",\"all\",1]": "35e6a7f331b2c92ddc922d23a3c82b202423c9e9e3c9a92ba318d336749ac58f",
  "[\"thursday-after-ash-wednesday\",\"main\",\"Postcommunion\",\"all\",1]": "2e0f81038189610ee3c51250864c8569985d67a7b28559a15333c728090b9073",
  "[\"thursday-after-ash-wednesday\",\"main\",\"Secret\",\"all\",1]": "959f0897961a90249f6730376b5e26f17ca6594b23d8159948520d1ea93f1704",
  "[\"transfiguratione-domini-nostri-iesu-christi\",\"main\",\"Collect\",\"all\",1]": "daf7ab95c7e39f9ebcda289aa573733e48358298440f461f8fe0b3c6fac9bcf5",
  "[\"transfiguratione-domini-nostri-iesu-christi\",\"main\",\"Secret\",\"all\",1]": "8fff17e27b581ebf61a7d919b894c6ba2a1ebb917d564716e90068e226515ec4",
  "[\"trinity\",\"main\",\"Collect\",\"all\",1]": "8eef3bf900925afee7b40019cf078538809c481380f1d7342856811374a5b27f",
  "[\"trinity\",\"main\",\"Postcommunion\",\"all\",1]": "333c80cceaa099fbd6f155d21e6059825fad8bd509b43fc2c08887f89adedecb",
  "[\"trinity\",\"main\",\"Secret\",\"all\",1]": "4f4e4930adc9fbfbbaa236de5f851cdcdd3944862cbd670f580c66fb117cddfc",
  "[\"vigil-assumption\",\"main\",\"Collect\",\"all\",1]": "cfb0247750be245b57cced6b6f2060be1d14490711d10fb00d04678054281c56",
  "[\"vigil-assumption\",\"main\",\"Postcommunion\",\"all\",1]": "b3dfeb7ceb1668fa6dcb2b38b8dc5712a9a35c6077607f935f26174b36e9707f",
  "[\"vigil-assumption\",\"main\",\"Secret\",\"all\",1]": "bd48a3125323c5112f32278e4bf8a3e4d295a16454b1634b52fc0d30959b53e2",
  "[\"vigil-nativity-lord\",\"main\",\"Postcommunion\",\"all\",1]": "1a591d98ff0501c553828cf8956a0c80c53393c9292ab2561abf86f223c25662",
  "[\"vigil-nativity-lord\",\"main\",\"Secret\",\"all\",1]": "b4754924afb8b17964a3fc0df3af19dcc3dee0b33c4a65de054d001562b5d092",
  "[\"vigil-nativity-saint-john-baptist\",\"main\",\"Collect\",\"all\",1]": "4c892046005cd2bd69296e65683cb2c7b8a331cd889ed7166a2c3a6183791bb2",
  "[\"vigil-nativity-saint-john-baptist\",\"main\",\"Postcommunion\",\"all\",1]": "e7672aa84e4952fef609d15140b15af54ae193af6fc73603a332b830bb989c0a",
  "[\"vigil-nativity-saint-john-baptist\",\"main\",\"Secret\",\"all\",1]": "e0ea9891fa2729fc704b28a396531c5aacaae843c77395aa2a78f77d1839a898",
  "[\"vigil-of-the-ascension\",\"main\",\"Collect\",\"all\",1]": "f7b7b4cd55658e0212e489f6e058f7fca53dd7b272a78bfc2c40eddb87557742",
  "[\"vigil-of-the-ascension\",\"main\",\"Postcommunion\",\"all\",1]": "a8f8569cc02880fe10a23167d62d290d5cb650deb74eccd277ad520545b6c53d",
  "[\"vigil-of-the-ascension\",\"main\",\"Secret\",\"all\",1]": "b816703767f73f45880796a78632c3826f2ddd42267814cc6ff5671c778c4d17",
  "[\"vigil-saint-lawrence\",\"main\",\"Collect\",\"all\",1]": "d553d6a0deb7584fb4bcc034dae3c0400ab43fb27895275bb8c01c84b6f3ce21",
  "[\"vigil-saint-lawrence\",\"main\",\"Postcommunion\",\"all\",1]": "17ece52e7f95c5a771cc9c3873029931bbe22b2708d5573b304447d66d1c5b6c",
  "[\"vigil-saint-lawrence\",\"main\",\"Secret\",\"all\",1]": "1272ad28396da333038b7c8e5542ae10f403b3efcc727f5d1e8898d1b7d72de8",
  "[\"vigil-saints-peter-paul\",\"main\",\"Postcommunion\",\"all\",1]": "65b721a1c4519656d99e0e559fd0bb2cb8243b37586bb04a8f81932ce39fed80",
  "[\"visitatione-beatae-mariae-virginis\",\"main\",\"Collect\",\"all\",1]": "aaff55eec3011cf3dd066d53729251841b0f2b07ece93a6b075589f1eeaa3152",
  "[\"visitatione-beatae-mariae-virginis\",\"main\",\"Postcommunion\",\"all\",1]": "438d80aee105eb4e18c408d824616fe017ce0b3efaf9c0fa0b861092af2f6510"
});
  // END GENERATED CONCLUSION PINS
  // Separate finite editorial authority. Activation requires exact Root adoption;
  // an ending-authority successor requires a newly reviewed editorial authority.
  const ACTIVE_DISPLAY_AUTHORITY_SHA256 = '231c2cfa81cc193060d5d00ab85882b0b1ae2c4b3b22a9380df524931c1de1d3';
  const GENERATED_DISPLAY_AUTHORITY_SHA256 = "231c2cfa81cc193060d5d00ab85882b0b1ae2c4b3b22a9380df524931c1de1d3";
  const DISPLAY_ENDING_AUTHORITY_SHA256 = "b26fe7863979e300ea47ad925e22d77d783dd76a418672b516eba73cac166744";
  const DISPLAY_METHOD_ID = "roman-1962-finite-english-editorial-readings-20261112";
  const DISPLAY_SOURCE_REVIEW_SHA256 = "5afefdfd76d2a96c61448f4d7c733a3205a06eba457325acbe5419438f2bfa40";
  const DISPLAY_PINS = Object.freeze({
  "[\"commune-unius-martyris-3\",\"main\",\"Postcommunion\",\"all\",1]": "29363b5e3c9c9caccf691e5dd5ac0e60eeffb06eef7ffe8a64b545c21d10e42c",
  "[\"comm-s-mennae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": "8aa321f6cd29ba0f286b12027e1d46071fc3ef2b6359c67f42cc0437b355266d",
  "[\"s-matthiae-apostoli\",\"main\",\"Secret\",\"all\",1]": "0823e3e6cf2e0ade3a882e919b08f15ecf7e0cabad8bfbdc1298a633ea3541b1"
});
  const DISPLAY_RECORDS = {
  "[\"commune-unius-martyris-3\",\"main\",\"Postcommunion\",\"all\",1]": {
    "target": [
      "commune-unius-martyris-3",
      "main",
      "Postcommunion",
      "all",
      1
    ],
    "language": "en",
    "source_id": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
    "source_body_sha256": "7a8afa935a57f8be1fdd945a1dc9da9ebb1c79a8825f1cd1ade2766b05f9fd97",
    "translation_binding_sha256": "ac4e28fcb678f5dcada51f1246bd7949e198ff7ab1cd58ad2af3d5c50d293843",
    "public_descriptor_sha256": "2f512e275a5a9bad1a72358ef20f1e3f49f30fd4a15ce2b176934644d05c92dd",
    "native_admission_sha256": "2bca8bb122622bdb9a0c37cf5a91382f0377969727c9a20d50a625cb875f7e4f",
    "cue_start": 177,
    "operation": {
      "end": 16,
      "new": "beseech",
      "offset_unit": "utf16",
      "old": "bseech",
      "source_prefix_sha256": "5aa51681af03cbd57a1738cbccd5dd8933d475a1ad1c754302ad38e94c0e142c",
      "start": 10,
      "strictly_before_original_cue": true
    },
    "annotation": "The printed source reads “bseech”; the reading text supplies the missing e.",
    "source_review_sha256": "bdec3898ee7b7a01f636c3c1c845aeee986ac1093789e30f475bed10aba39a25",
    "variants": {
      "conclusion-provider": {
        "priest_text_sha256": "017100e4801f09143839ed49bc01c62d0b59fc1bcb3964950518b0d8a8e85bba",
        "display_text_sha256": "a2ee47e2cf9cf92d4c6710913a30c3e60942615b3bdcc7b4a2a8fa63c0f045c3"
      },
      "petition": {
        "priest_text_sha256": "5aa51681af03cbd57a1738cbccd5dd8933d475a1ad1c754302ad38e94c0e142c",
        "display_text_sha256": "3e35538b574f0c11a0322039bd2c3fe8ae3ae362154ebeb4d4b3c7fc49b10b80"
      }
    }
  },
  "[\"comm-s-mennae-martyris\",\"main\",\"Postcommunion\",\"all\",1]": {
    "target": [
      "comm-s-mennae-martyris",
      "main",
      "Postcommunion",
      "all",
      1
    ],
    "language": "en",
    "source_id": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
    "source_body_sha256": "7a8afa935a57f8be1fdd945a1dc9da9ebb1c79a8825f1cd1ade2766b05f9fd97",
    "translation_binding_sha256": "266f9af85e4840b695909b3eb9e2201d6f4d3f723d89ae4a2ba0d5c20c20a89e",
    "public_descriptor_sha256": "693c0630d8803e542bdbdcc0172f0edeafda43a16001486a9bbe456380a6f24c",
    "native_admission_sha256": "d414986ec4a8e693302e41189bd27d9f59267f6c90b07b284d7d69b392d1969c",
    "cue_start": 177,
    "operation": {
      "end": 16,
      "new": "beseech",
      "offset_unit": "utf16",
      "old": "bseech",
      "source_prefix_sha256": "5aa51681af03cbd57a1738cbccd5dd8933d475a1ad1c754302ad38e94c0e142c",
      "start": 10,
      "strictly_before_original_cue": true
    },
    "annotation": "The printed source reads “bseech”; the reading text supplies the missing e.",
    "source_review_sha256": "bdec3898ee7b7a01f636c3c1c845aeee986ac1093789e30f475bed10aba39a25",
    "variants": {
      "conclusion-provider": {
        "priest_text_sha256": "017100e4801f09143839ed49bc01c62d0b59fc1bcb3964950518b0d8a8e85bba",
        "display_text_sha256": "a2ee47e2cf9cf92d4c6710913a30c3e60942615b3bdcc7b4a2a8fa63c0f045c3"
      },
      "petition": {
        "priest_text_sha256": "5aa51681af03cbd57a1738cbccd5dd8933d475a1ad1c754302ad38e94c0e142c",
        "display_text_sha256": "3e35538b574f0c11a0322039bd2c3fe8ae3ae362154ebeb4d4b3c7fc49b10b80"
      }
    }
  },
  "[\"s-matthiae-apostoli\",\"main\",\"Secret\",\"all\",1]": {
    "target": [
      "s-matthiae-apostoli",
      "main",
      "Secret",
      "all",
      1
    ],
    "language": "en",
    "source_id": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
    "source_body_sha256": "dd101c35df430d5785beb3c60cb6012bd2c1af12c9b5a8492b6cf2c615ddc262",
    "translation_binding_sha256": "f0e79dec458b1625cd685b6c014f249c1ad33d32b7bf5430b5eb60a7d99c5f5b",
    "public_descriptor_sha256": "70397af8d95e8c97825d1d07200bc50ed14b5334c4ecb8d1f2c7153e6d362fe7",
    "native_admission_sha256": "4b93d41347866e36fab590bb24b83968b92e55daf898dff368dc8ddb3c46e47c",
    "cue_start": 182,
    "operation": {
      "end": 181,
      "new": ".",
      "offset_unit": "utf16",
      "old": "",
      "source_prefix_sha256": "14b5394d03b99b1030aa00adaf7ba1f59f5bfc11e42f3f7041099e684d837ed7",
      "start": 181,
      "strictly_before_original_cue": true
    },
    "annotation": "The printed source has no punctuation between “defended” and “Through”; the reading text supplies a period after “defended”.",
    "source_review_sha256": "bdec3898ee7b7a01f636c3c1c845aeee986ac1093789e30f475bed10aba39a25",
    "variants": {
      "conclusion-provider": {
        "priest_text_sha256": "d2fe94319daf77d2648eae87dfb11fe592a90fc8cb571d6deae34c255173e5ff",
        "display_text_sha256": "c1143f97208ed2d14a3f256c273d589aa1f68db17a5ea0655b97f21cc0efcedd"
      },
      "petition": {
        "priest_text_sha256": "14b5394d03b99b1030aa00adaf7ba1f59f5bfc11e42f3f7041099e684d837ed7",
        "display_text_sha256": "5cdf44df727948cead2e34728b3cfb9cce6367dba5a18c17653560fef281d927"
      }
    }
  }
};

  function canonical(value) {
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
    return JSON.stringify(value);
  }
  function sha(text) {
    const bytes = unescape(encodeURIComponent(text)), words = [], constants = [], initial = [];
    let prime = 2;
    while (constants.length < 64) {
      let isPrime = true;
      for (let factor = 2; factor * factor <= prime; factor++) if (prime % factor === 0) { isPrime = false; break; }
      if (isPrime) {
        if (initial.length < 8) initial.push((Math.sqrt(prime) % 1 * 4294967296) | 0);
        constants.push((Math.cbrt(prime) % 1 * 4294967296) | 0);
      }
      prime++;
    }
    for (let index = 0; index < bytes.length; index++) words[index >> 2] = (words[index >> 2] || 0) | bytes.charCodeAt(index) << (24 - index % 4 * 8);
    words[bytes.length >> 2] = (words[bytes.length >> 2] || 0) | 128 << (24 - bytes.length % 4 * 8);
    words[(((bytes.length + 8) >> 6) + 1) * 16 - 1] = bytes.length * 8;
    const rotate = (value, count) => value >>> count | value << (32 - count);
    let hash = initial.slice();
    for (let start = 0; start < words.length; start += 16) {
      const schedule = [], work = hash.slice();
      for (let index = 0; index < 64; index++) {
        if (index < 16) schedule[index] = words[start + index] | 0;
        else {
          const a = schedule[index - 15], b = schedule[index - 2];
          schedule[index] = (schedule[index - 16] + (rotate(a, 7) ^ rotate(a, 18) ^ a >>> 3) + schedule[index - 7] + (rotate(b, 17) ^ rotate(b, 19) ^ b >>> 10)) | 0;
        }
        const [a, b, c, d, e, f, g, h] = work;
        const t1 = (h + (rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25)) + (e & f ^ ~e & g) + constants[index] + schedule[index]) | 0;
        const t2 = ((rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22)) + (a & b ^ a & c ^ b & c)) | 0;
        work.splice(0, 8, (t1 + t2) | 0, a, b, c, (d + t1) | 0, e, f, g);
      }
      hash = hash.map((value, index) => (value + work[index]) | 0);
    }
    return hash.map(value => (value >>> 0).toString(16).padStart(8, '0')).join('');
  }
  function requireValue(condition, reason) { if (!condition) throw new Error(reason); }
  function isV2(source) { return source && source.schema === 'triptych-oration-conclusion-source/v2'; }
  function equal(left, right) { return canonical(left) === canonical(right); }
  function validate(source) {
    requireValue(ACTIVE_AUTHORITY_SHA256 && ACTIVE_AUTHORITY_SHA256 === GENERATED_AUTHORITY_SHA256, 'conclusion authority inactive');
    const v2 = isV2(source);
    requireValue(source && (v2 ? source.method_id === V2_METHOD_ID : source.schema === 'triptych-oration-conclusion-source/v1' && source.method_id === METHOD_ID), 'unknown conclusion descriptor');
    requireValue(Array.isArray(source.target) && source.target.length === 5, 'missing conclusion target');
    const key = JSON.stringify(v2 ? [source.calendar, ...source.target] : source.target);
    requireValue(sha(canonical(source)) === PUBLIC_PINS[key], 'changed or unlisted conclusion descriptor');
    return source;
  }
  function wordingProjection(member, source, part, context, petition) {
    const choice = source.context.constraints && source.context.constraints.wording_choice;
    if (!choice) {
      requireValue((context.massCategory === undefined ? 'mass-of-office' : context.massCategory) === source.context.mass_category, 'different execution context');
      return petition;
    }
    const use = context.prayerUse, groups = context.groups;
    requireValue(use && equal(use.sourceTarget, source.target) && use.choiceId === choice.id, 'unbound prayer use');
    requireValue(Array.isArray(groups) && groups.length === 1 && groups[0].conclusion_group === 1 && groups[0].kind === 'principal' && Array.isArray(groups[0].members) && groups[0].members.length === 1 && groups[0].members[0].id === member.id, 'wording requires one principal prayer');
    const branches = choice.branches.filter(branch => branch.id === use.branch && branch.required_use === use.kind);
    requireValue(branches.length === 1, 'unreviewed prayer-use branch');
    const branch = branches[0], selected = branch.languages[member.language];
    requireValue(['principal-office-mass', 'principal-votive-mass'].includes(branch.required_use), 'unsupported prayer use');
    const category = branch.required_use === 'principal-votive-mass' ? 'votive' : 'mass-of-office';
    requireValue((context.massCategory === undefined ? 'mass-of-office' : context.massCategory) === category, 'prayer use and Mass category differ');
    requireValue(selected && selected.offset_units === 'utf16' && selected.body_sha256 === part.body_sha256, 'wording source owner differs');
    requireValue(Number.isInteger(selected.start) && Number.isInteger(selected.end) && 0 <= selected.start && selected.start < selected.end && selected.end <= part.cue_start, 'wording leaves petition');
    requireValue(member.text.slice(selected.start, selected.end) === selected.source && typeof selected.selected_literal === 'string' && selected.selected_literal, 'wording source partition differs');
    return petition.slice(0, selected.start) + selected.selected_literal + petition.slice(selected.end);
  }
  function memberProjection(member, context, slot, executionKind = 'grouped-mass-orations') {
    const source = validate(member.source), language = member.language;
    requireValue(JSON.stringify(member.target) === JSON.stringify(source.target) && member.target[2] === slot, 'different source owner');
    requireValue(source.calendar === context.calendar, 'different execution calendar');
    const v2 = isV2(source);
    if (v2) requireValue(source.context.execution_kind === executionKind && source.context.required_slot === slot, 'different execution context');
    else requireValue(executionKind === 'grouped-mass-orations' && (context.massCategory === undefined ? 'mass-of-office' : context.massCategory) === source.context.mass_category, 'different execution context');
    requireValue(language === 'la' || language === 'en', 'unknown language');
    requireValue(language !== 'en' || member.witness === source.source_id || v2 && source.source_id === '' && member.witness === null, 'different selected witness');
    const part = source.languages[language], text = member.text;
    requireValue(part && typeof text === 'string' && sha(text) === part.body_sha256, 'different source text');
    requireValue(part.offset_units === 'utf16' && Number.isInteger(part.cue_start) && Number.isInteger(part.cue_end) && part.cue_start > 0 && part.cue_start < part.cue_end && part.cue_end === text.length && text.slice(part.cue_start) === part.cue, 'source partition differs');
    requireValue(typeof member.id === 'string' && member.id, 'unbound member');
    let petition = text.slice(0, part.cue_start);
    if (v2) {
      requireValue(typeof part.full_conclusion === 'string' && part.full_conclusion && Array.isArray(part.source_hooks) && part.source_hooks.length > 0, 'unbound conclusion source');
      requireValue(part.response && typeof part.response.speaker === 'string' && typeof part.response.text === 'string' && part.response.text, 'unbound conclusion response');
      if (part.conclusion_mode === 'source-complete') requireValue(text.slice(part.cue_start, part.cue_start + part.full_conclusion.length) === part.full_conclusion, 'complete source conclusion differs');
      if (executionKind === 'grouped-mass-orations') petition = wordingProjection(member, source, part, context, petition);
      else requireValue((context.massCategory === undefined ? 'mass-of-office' : context.massCategory) === source.context.mass_category, 'different execution context');
    }
    const result = {id: member.id, language, source_text: text, petition, conclusion: part.full_conclusion,
      source_hooks: v2 ? part.source_hooks : [source.rule_passage_id, source.formula_passage_id, source.source_publication_passage_id],
      response: v2 ? part.response : source.response, source_method: source.method_id, v2};
    if (v2) {
      requireValue(source.qualification && typeof source.qualification[language] === 'string' && source.body_fidelity && source.body_fidelity[language] && typeof source.body_fidelity[language] === 'object', 'missing execution qualification');
      result.qualification = source.qualification[language];
      result.body_fidelity = source.body_fidelity[language];
    }
    return result;
  }
  function projectedMember(member, final, method) {
    const result = {id: member.id, source_text: member.source_text,
      priest_text: member.petition + (final ? member.conclusion : ''),
      role: final ? 'conclusion-provider' : 'petition', source_hooks: member.source_hooks};
    if (method === V2_METHOD_ID) result.source_method = member.source_method;
    if (member.v2) {
      result.qualification = member.qualification;
      result.body_fidelity = member.body_fidelity;
    }
    return result;
  }
  function unresolved(method, reason) {
    return {schema: 'triptych-oration-conclusion-group/v1', state: 'unresolved',
      execution_extent: {state: 'unresolved', method_id: method}, reasons: [reason], members: []};
  }
  function groupMethod(context) {
    return context && Array.isArray(context.groups) && context.groups.some(group => group && Array.isArray(group.members) && group.members.some(member => member && isV2(member.source))) ? V2_METHOD_ID : METHOD_ID;
  }
  function executeGroup(context) {
    const method = groupMethod(context);
    try {
      requireValue(context && context.calendar === 'roman-1962' && context.rule === GROUP_RULE, 'unproved grouping rule');
      const groups = context.groups;
      requireValue(Array.isArray(groups) && groups.length > 0 && groups.length <= 2, 'missing conclusion group');
      const number = groups[0].conclusion_group, slot = groups[0].slot;
      requireValue(number === 1 || number === 2, 'unknown conclusion group');
      requireValue(number !== 1 || groups.length === 1, 'principal conclusion split');
      const members = [];
      groups.forEach((group, index) => {
        requireValue(group.conclusion_group === number && group.slot === slot && group.position === (number === 1 ? 1 : index + 2), 'mixed or unordered groups');
        requireValue(group.conclusion_final === (index === groups.length - 1), 'wrong conclusion provider unit');
        requireValue((number === 1 ? ['principal', 'inseparable'] : ['commemoration', 'inseparable']).includes(group.kind), 'wrong group kind');
        requireValue(Array.isArray(group.members) && group.members.length === (group.kind === 'inseparable' ? 2 : 1), 'unbound member order');
        group.members.forEach(member => members.push(memberProjection(member, context, slot)));
      });
      requireValue(new Set(members.map(member => member.id)).size === members.length && new Set(members.map(member => member.language)).size === 1, 'duplicate or mixed-language members');
      return {schema: 'triptych-oration-conclusion-group/v1', state: 'source-derived-complete',
        execution_extent: {state: 'source-derived-complete', method_id: method}, conclusion_group: number, slot,
        members: members.map((member, index) => projectedMember(member, index === members.length - 1, method)),
        response: {...members[members.length - 1].response, provider_id: members[members.length - 1].id}};
    } catch (error) {
      return unresolved(method, 'conclusion-group-source-or-context-unbound');
    }
  }
  function executeStudy(context) {
    try {
      requireValue(context && context.calendar === 'postconciliar' && context.executionScope === 'source-local-study', 'unproved study scope');
      const member = context.member, source = validate(member.source), selected = context.selection;
      requireValue(isV2(source) && source.context.execution_kind === 'source-local-study' && member.language === 'en' && source.target[2] === 'Collect', 'unreviewed study recipient');
      const constraints = source.context.constraints && source.context.constraints.source_local_study;
      requireValue(constraints && constraints.requires_explicit_selection === true && constraints.only_one_collect === true && constraints.current_2008_admitted === false && constraints.latin_body_available === false, 'unbound study constraints');
      requireValue(constraints.source_selection && typeof constraints.source_selection === 'object' && !Array.isArray(constraints.source_selection), 'unbound bibliographic study selection');
      requireValue(equal(context.sourceRule, source.context.source_rule), 'different study source rule');
      requireValue(selected && equal(selected.target, constraints.target) && equal(selected.target, source.target) && equal(selected.source_selection, constraints.source_selection) && selected.rule_id === constraints.rule_id && selected.only_one_collect === true && equal(selected.alternative, constraints.alternative), 'different study selection');
      const projected = memberProjection(member, context, source.target[2], 'source-local-study');
      return {schema: 'triptych-oration-conclusion-group/v1', state: 'source-derived-complete',
        execution_extent: {state: 'source-derived-complete', method_id: V2_METHOD_ID},
        execution_scope: 'source-local-study', source_rule: source.context.source_rule,
        current_2008_admitted: false, latin_body_available: false,
        conclusion_group: 1, slot: source.target[2], members: [projectedMember(projected, true, V2_METHOD_ID)],
        response: {...projected.response, provider_id: projected.id}};
    } catch (error) {
      return unresolved(V2_METHOD_ID, 'conclusion-study-source-or-context-unbound');
    }
  }
  function executeProperRite(context) {
    try {
      requireValue(context && context.calendar === 'roman-1962', 'unreviewed proper rite calendar');
      const rite = context.rite, member = context.member, source = validate(member.source);
      requireValue(isV2(source) && source.context.execution_kind === 'proper-rite', 'missing proper rite conclusion source');
      const expected = source.context, target = source.target;
      requireValue(rite && equal(Object.keys(rite).sort(), ['appointment', 'appointmentLocus', 'id', 'locus', 'ownConclusion', 'semanticRole', 'sourceIndex']), 'unknown proper rite fields');
      requireValue(rite && rite.id === 'oratio-super-populum' && rite.id === expected.rite_id && rite.semanticRole === 'prayer-over-people' && rite.semanticRole === expected.semantic_role && rite.ownConclusion === true && rite.locus === expected.rite_locus, 'different proper rite');
      requireValue(rite.appointment && equal(rite.appointment, {mass: target[0], form_id: target[1], proper: target[2], occurrence: target[4]}), 'different rite appointment');
      requireValue(Number.isInteger(rite.sourceIndex) && rite.sourceIndex >= 0 && rite.sourceIndex === expected.source_index && typeof rite.appointmentLocus === 'string' && rite.appointmentLocus && rite.appointmentLocus === expected.appointment_locus, 'unbound rite source row');
      requireValue(member.id === 'proper/' + context.calendar + '/' + target[0] + '/' + String(rite.sourceIndex + 1).padStart(3, '0'), 'different rite event owner');
      const projected = memberProjection(member, context, target[2], 'proper-rite');
      return {schema: 'triptych-oration-conclusion-group/v1', state: 'source-derived-complete',
        execution_extent: {state: 'source-derived-complete', method_id: V2_METHOD_ID},
        execution_kind: 'proper-rite', rite, conclusion_group: 1, slot: target[2],
        members: [projectedMember(projected, true, V2_METHOD_ID)], response: {...projected.response, provider_id: projected.id}};
    } catch (error) {
      return unresolved(V2_METHOD_ID, 'conclusion-rite-source-or-context-unbound');
    }
  }
  function applyDisplayCorrections(context, projected) {
    // executeGroup owns all source admission and actual member roles. This
    // additive presentation stage neither repairs its inputs nor changes its result.
    if (!ACTIVE_DISPLAY_AUTHORITY_SHA256 || projected.state !== 'source-derived-complete') return projected;
    const inputs = context.groups.flatMap(group => group.members);
    const members = projected.members.map(function (member) {
      const input = inputs.find(one => one.id === member.id);
      const key = input && JSON.stringify(input.target), row = key && DISPLAY_RECORDS[key];
      if (!row || input.language !== 'en') return member;
      try {
        requireValue(ACTIVE_DISPLAY_AUTHORITY_SHA256 === GENERATED_DISPLAY_AUTHORITY_SHA256 &&
          ACTIVE_AUTHORITY_SHA256 === DISPLAY_ENDING_AUTHORITY_SHA256 &&
          GENERATED_AUTHORITY_SHA256 === DISPLAY_ENDING_AUTHORITY_SHA256, 'editorial authority differs');
        requireValue(sha(canonical(row)) === DISPLAY_PINS[key], 'editorial record differs');
        const source = validate(input.source), part = source.languages.en, operation = row.operation;
        requireValue(input.witness === row.source_id && source.source_id === row.source_id &&
          sha(canonical(source)) === row.public_descriptor_sha256 &&
          source.translation_binding_sha256 === row.translation_binding_sha256 &&
          part.body_sha256 === row.source_body_sha256 && part.cue_start === row.cue_start &&
          input.text === member.source_text && sha(member.source_text) === row.source_body_sha256,
          'editorial source binding differs');
        const method = groupMethod(context);
        requireValue(source.schema === 'triptych-oration-conclusion-source/v1' && source.method_id === METHOD_ID &&
          projected.execution_extent.state === 'source-derived-complete' &&
          projected.execution_extent.method_id === method && projected.slot === input.target[2] &&
          (method === METHOD_ID ? !Object.prototype.hasOwnProperty.call(member, 'source_method') :
            method === V2_METHOD_ID && member.source_method === METHOD_ID),
          'editorial execution differs');
        const final = projected.members[projected.members.length - 1];
        requireValue(projected.response.speaker === 'response' && projected.response.text === 'Amen.' &&
          projected.response.provider_id === final.id &&
          member.role === (member.id === final.id ? 'conclusion-provider' : 'petition'),
          'editorial role or response differs');
        const variant = row.variants[member.role], prefix = member.source_text.slice(0, row.cue_start);
        const suffix = member.role === 'conclusion-provider' ? part.full_conclusion : '';
        requireValue(variant && sha(member.priest_text) === variant.priest_text_sha256 &&
          member.priest_text === prefix + suffix, 'editorial execution preimage differs');
        requireValue(operation.offset_unit === 'utf16' && operation.strictly_before_original_cue === true &&
          Number.isInteger(operation.start) && Number.isInteger(operation.end) &&
          operation.start >= 0 && operation.start <= operation.end && operation.end < row.cue_start &&
          sha(prefix) === operation.source_prefix_sha256 &&
          prefix.slice(operation.start, operation.end) === operation.old,
          'editorial operation differs');
        const display = member.priest_text.slice(0, operation.start) + operation.new + member.priest_text.slice(operation.end);
        const shift = operation.new.length - (operation.end - operation.start);
        requireValue(sha(display) === variant.display_text_sha256 &&
          display.slice(row.cue_start + shift) === suffix, 'editorial result differs');
        return Object.assign({}, member, {display_text: display, display_correction: {
          state: 'applied', method_id: DISPLAY_METHOD_ID, authority_sha256: ACTIVE_DISPLAY_AUTHORITY_SHA256,
          source_review_sha256: DISPLAY_SOURCE_REVIEW_SHA256, target: row.target.slice(), annotation: row.annotation
        }});
      } catch (error) {
        return Object.assign({}, member, {display_correction: {state: 'unavailable',
          reasons: ['finite-editorial-reading-unbound']}});
      }
    });
    return Object.assign({}, projected, {members});
  }
  function executeDisplayGroup(context) {
    return applyDisplayCorrections(context, executeGroup(context));
  }

  return Object.freeze({ACTIVE_DISPLAY_AUTHORITY_SHA256, GENERATED_DISPLAY_AUTHORITY_SHA256, executeDisplayGroup, METHOD_ID, V2_METHOD_ID, GROUP_RULE, ACTIVE_AUTHORITY_SHA256, GENERATED_AUTHORITY_SHA256, PUBLIC_PINS, canonical, sha, validate, executeGroup, executeStudy, executeProperRite});
});
