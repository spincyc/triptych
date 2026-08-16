#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import https from 'node:https';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const WIDTH = 3800;
const HEIGHT = 2436;
const ZOOM = 9;
const TILE_SIZE = 256;
const TILE_X_MIN = 300;
const TILE_X_MAX = 307;
const TILE_Y_MIN = 205;
const TILE_Y_MAX = 215;
const TILE_BASE_URL =
  'https://s3.amazonaws.com/elevation-tiles-prod/terrarium';
const ACQUIRED_ON = '2026-08-16';
const EXPECTED_OUTPUT_SHA256 =
  'ceb958487d6e0173f8bb74327a46fc88aface5206dd223c1473bc6194a05a2b2';
const NATURAL_EARTH_SOURCE_PAGE =
  'https://www.naturalearthdata.com/downloads/10m-physical-vectors/';
const TERRAIN_SHADE_SEAM_REPAIR = {
  firstReplacedRow: 1998,
  lastReplacedRow: 2008,
  upperControlRow: 1997,
  lowerControlRow: 2009,
};
const EXCLUDED_NAMED_CANALS = new Set(['Suez Canal', 'Ismailiya Canal']);
const EXPECTED_TOOLCHAIN = {
  node: 'v26.7.0',
  imagemagick: [
    'Version: ImageMagick 7.1.2-29 Q16-HDRI x86_64 b919b37fd:20260727 https://imagemagick.org',
    'Copyright: (C) 1999 ImageMagick Studio LLC',
    'License: https://imagemagick.org/license/',
    'Features: Cipher DPC HDRI Modules OpenCL OpenMP',
    'Delegates (built-in): bzlib cairo djvu fftw fontconfig freetype heic jbig jng jp2 jpeg jxl lcms lqr ltdl lzma openexr pangocairo png raqm raw rsvg tiff uhdr webp wmf x xml zip zlib zstd',
    'Compiler: gcc (16.1)',
  ].join('\n'),
  rsvg_convert: [
    'rsvg-convert version 2.62.3',
    '',
    'libraries used:',
    '  cairo 1.18.4',
    '  pango 1.58.2',
    '  harfbuzz 14.3.1',
    '  fontconfig 2.18.3',
  ].join('\n'),
};

const NATURAL_EARTH = [
  ['land', 'ne_10m_land.geojson',
    '1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416'],
  ['coastline', 'ne_10m_coastline.geojson',
    '6f75ae0e0de157b14946e2255eb1f5486d9a13819032e26d4610852d296788f6'],
  ['lakes', 'ne_10m_lakes.geojson',
    '2d036f53dedec578001c5c30c2959ee7d4eebc1306900fa4367c49929ec8f2d9'],
  ['rivers', 'ne_10m_rivers_lake_centerlines.geojson',
    'bb854a900ecbd3b408df46d5e16e3e0f974ba55993f9d8b5c26e855273c0905a'],
];

const TERRARIUM_TILES = [
  [300, 205, '177ba3c39783f1c24df008ac52ae31485a78db95877330312b50e0a9900d050d', 'pCc9.F9Stud.FAIL2IwGZRYZ3f0GOgLh', 'etopo1/ETOPO1_Bed_g.tif'],
  [300, 206, '9527632114a0d35b2d23a969cf836b5537736cca01a53d538fabd06f183e34df', 'mWm_eQGEGwvjgq0tTYrCjfKfvd0gJnS_', 'etopo1/ETOPO1_Bed_g.tif'],
  [300, 207, '950e7fc7cba8fd010d3f9bc1a19236fa7974b20168ea3bd69b97ce0b9ba449e2', '4hH9mk6cXL0EzdmP5SmsJrT3DG657ESO', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [300, 208, '26260e43e664a7209a0c530e24e72ed4523dfb18100fa8a169b5ef74ebc35c7b', 'XEJlqnDmYDGshP.QSAYvOvnZMvJOKI1s', 'srtm/N31E031.tif, srtm/N31E030.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [300, 209, '0c7f203fec8f8c2733251a70ba58cd854facfd1b613c42a39b0f01426e5e2da4', 'bB.zYwRlZ_8yApobB_qUcg6gTh3jKNej', 'srtm/N31E031.tif, srtm/N30E031.tif, srtm/N31E030.tif, srtm/N30E030.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [300, 210, '4bc94151fdb353be1cd571dcfe7d72eca9deed11d079eccf7c78c06c50134479', 'B4N1CaAVN2N65OPzCLqEKQu7ZHa3PKo5', 'srtm/N30E031.tif, srtm/N30E030.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [300, 211, 'ecad1c505f4d45d5bc4379647906e6bf1d75620d906c4bbe918186386a356e2a', 'wxueU01FK9FGDIxymgA8knrJ4rbEBDDC', 'srtm/N29E031.tif, srtm/N30E031.tif, srtm/N29E030.tif, srtm/N30E030.tif, gmted/10N030E_20101117_gmted_mea075.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [300, 212, '550e4269e79b0ca91ef9684c3390880b1a230a57c620062fff11e48833ab7a5d', 'UaTiPoVb9sdGwTPbOJJPdsqPli9EFQlW', 'srtm/N29E031.tif, srtm/N28E031.tif, srtm/N29E030.tif, srtm/N28E030.tif, gmted/10N030E_20101117_gmted_mea075.tif'],
  [300, 213, '1f28c0fd72e905ddfe49b61431b65ef987cde61e20cb9c40f585c6b39b733c0b', 'JBzJjh91xvsaPGjJUO5upUtuNBoej7MM', 'srtm/N28E031.tif, srtm/N28E030.tif, gmted/10N030E_20101117_gmted_mea075.tif'],
  [300, 214, 'b1fdbb19363f3efa626ea6ea1e2b474648ceb0c91886c15d1f3b1722de437d1f', 'V7ITAdKOh3Mo0dG4.M2iYrs9gyHDEDee', 'srtm/N27E031.tif, srtm/N28E031.tif, srtm/N27E030.tif, srtm/N28E030.tif'],
  [300, 215, '54100a01f09721f48637469a00ed8a0c4b5f846d7ae54153590cfaf10f870970', 'b_CZp9Mzkj7mvrn_U6PGX8FJI_gK4DDE', 'srtm/N27E031.tif, srtm/N27E030.tif, gmted/10N030E_20101117_gmted_mea075.tif'],
  [301, 205, 'e7e935d9769a4daf05e7ffc2561e2de20d7c93e573fbee6c398b8d1a99f8f27b', 'WExR5yPwyKBFjf4TKdqo2HmR_EVnDweQ', 'etopo1/ETOPO1_Bed_g.tif'],
  [301, 206, '4b22e6e1bddda6e9fae034e601b8be2595a3d29457e03a1ece918b4f80fafcf2', 'LetMhuZdmgXRugHzoj6WkBv1I.Q.44VJ', 'etopo1/ETOPO1_Bed_g.tif'],
  [301, 207, 'efadb2784768f51770a26e87167deb815f1eaa3bbd9737f5f9ed706060fb7062', 'u.fjaPHqzlZwMKdcZWQ_wAO6feDi.Xd6', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [301, 208, 'cae1d09660b87e245eb4bb2751e14d754727faf2334201313f863a9b0edeb2df', 'fdFwATHUTzybN3Pf_JWqqqjcg3s_4P.4', 'srtm/N31E031.tif, srtm/N31E032.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [301, 209, '1076fff8795a9674773bcf7d11e15d4403696c11e2f8f58274bbc91109703154', 'BSYdRPsQl8rB9kmA.T9F6QIXugmkJA2V', 'srtm/N31E032.tif, srtm/N31E031.tif, srtm/N30E031.tif, srtm/N30E032.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [301, 210, '67b5cc77e6cef13d4fac37a55803dc0d8650c3dd763d38a827b62eaab47187aa', 'mfy67KM38vRl1Z5A2t8cUEMIyPQL.rxx', 'srtm/N30E031.tif, srtm/N30E032.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [301, 211, 'cec767ab942e3f0f474ddea9e142454bff60b8d1033704951e3a335f4595a781', 'pxAxrTM0gqcEmwoK4X7rCU8kMy1KIo0c', 'srtm/N29E032.tif, srtm/N29E031.tif, srtm/N30E031.tif, srtm/N30E032.tif'],
  [301, 212, 'f38418f0e71e9f56c7b0729aad0f3c3b8a15a5ac78ff60a4b6c14a63592f848d', 'WPHMepDy2QPy5mKX2czoEb9H.cYvnqOG', 'srtm/N29E032.tif, srtm/N29E031.tif, srtm/N28E031.tif, srtm/N28E032.tif'],
  [301, 213, '7894e7fff2bd5b2ac512e7783a1598a15569da00da56271c8fadb0704093b3ed', 'L06zeAQ2h2Ja_PO40f0OWlomo2_DlGEX', 'srtm/N28E032.tif, srtm/N28E031.tif'],
  [301, 214, '606122e9d3ff6ae5e5b32d78007fffadb683e14ab42ebcf1b4646b80c49cc068', 'mqHa7mWP4suP8Zd_zN0aTk6_tUWlKPM8', 'srtm/N28E032.tif, srtm/N27E031.tif, srtm/N28E031.tif, srtm/N27E032.tif'],
  [301, 215, '1752b11f9c18d02d36fcaecc3041ee58416c88b17d9cbab462946c20216e2512', 'uej6Ngjwalf_C_ld823yPetYBld2mkid', 'srtm/N27E031.tif, srtm/N27E032.tif'],
  [302, 205, '51e7955c0788b0c773239c6dab8a9f598bd745cf0ea8dc75ac549e2cd017c2b9', 'F1rBVTHihuWTxbnps7.T3VJQuTXvgRtj', 'etopo1/ETOPO1_Bed_g.tif'],
  [302, 206, '45de7f72300334d11b56fd7dc1cac1fb510adcedabfa3d96d1b8002dde602ff6', 'zRSYN5SEZkw1H0Rqugj.cXghsUJgfr7U', 'etopo1/ETOPO1_Bed_g.tif'],
  [302, 207, '3c739cace178b92c057cd76129230e51071fc427db5db682e43ce37ada1c8886', 'VGWOd_9yT_NZKRKMxsqRaNBM1t3WYp71', 'etopo1/ETOPO1_Bed_g.tif'],
  [302, 208, '93a13044113f51917f7289c85a02b7d497b354b0b21cc25967e0cf647d2f2038', 'ivyMyt0vUkQmWq.nqDNKl8e2Q3T_S3Hu', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 209, 'a93a9b8cc36b2b8cfad7c4fc4797edaad869ad90d5b14e3a6c2e77ecd5b15ade', 'kR2DL4mip41Oslkx6g5agSsQ4cT4UJxl', 'srtm/N31E032.tif, srtm/N30E032.tif, srtm/N31E033.tif, srtm/N30E033.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 210, '9701d8733924343b6d85090912614c00718ee3c4886ba45acbabaa8a6f8d71c9', 'dYr95mcTsa3jsOF5_sKY59cDV348QZqS', 'srtm/N30E032.tif, srtm/N30E033.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 211, 'd3072ae3d41791c2c85fbb96250636d98e069ad5ff6e4973a99001439a342cad', '.0qwGJsAowjNAZdwpYXWn_E06kzWnnoh', 'srtm/N29E032.tif, srtm/N30E032.tif, srtm/N29E033.tif, srtm/N30E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 212, 'b21d77c060341b4dee36e5da16c49573ddd67383f19a28f20eb64f6f58f0fad2', 'i82hTl8xanj7HfsXAfT2TuB4nO4rHeY3', 'srtm/N29E032.tif, srtm/N28E032.tif, srtm/N29E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 213, 'e00b1efbaca4d700aad2954d68340657fc2400279140fac36617dc07d0bd56a9', 'pJsvDlSj4wWOBamiho9D_lWrLxMx2CBC', 'srtm/N28E032.tif, srtm/N28E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [302, 214, 'b4038a54b86ac01ce1ae9d1ce97d8face146046fa7d1c658bac48b5d340fc001', '89ClMNK70nW1pCAZM6OLeQkTc_DMMfXi', 'srtm/N28E032.tif, srtm/N27E032.tif, srtm/N27E033.tif, srtm/N28E033.tif'],
  [302, 215, 'e3e27421cdc55695d8f8244317ac61e6cc003a007aa8ab0ac8fae2e9a61406b5', 'MrJ9eU1BQsS_aMtUh9_gbmiLvym6vSEu', 'srtm/N27E032.tif, srtm/N27E033.tif'],
  [303, 205, '6ad955fc0221cddd22afbe269af05eb341dc4933bc66ccf9b2b11e3a4b1a4f56', 'kuPzyw06q3f88aPN3CjJePOdmDgwDmn3', 'etopo1/ETOPO1_Bed_g.tif'],
  [303, 206, '896db96e37157511ecea2c328987e921043cca61349aa716e40755d4137c2a0b', 'RxEsYwEE38zeMclZQLzRyrr.Ndo4YbyO', 'etopo1/ETOPO1_Bed_g.tif'],
  [303, 207, '413e1617ac1f21c0d6b8f35ff2d8778788c50070dc43f2895298419e54ab0c04', 'XlHufBFXPqmtSvY6VfrGNhsbzbeT_qYH', 'etopo1/ETOPO1_Bed_g.tif'],
  [303, 208, '19d0fe3626effba7904105df0ffebb300360019a584d293ee3b3012785288ca5', 'q8n7WSFxEt1rTrt4tUpKIKtXiGfqZcwD', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [303, 209, 'b43e53d85c4d60c2d0a0df0f5c7d1385a1462c2915795a14ae555f931be70efa', 'Y04pwTz6AUM3Jr2KL3ZUGBvFlfkg96iH', 'srtm/N31E033.tif, srtm/N30E033.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [303, 210, '4ebc6f9ba01f9d56868ea339742ead4a7ff74c3eda9c09c2ec69d531b6e13b49', 'cjqPY4GBPcvgSu7IMkWHUOuH10kjQYN5', 'srtm/N30E033.tif'],
  [303, 211, 'ea3efa35ac505909c9bb49e4501cc2245f46a3de9c656897128de5a25bc21869', 'KKDvp6BqfqffjvnXcwexvhAB3SkVFvMw', 'srtm/N29E033.tif, srtm/N30E033.tif'],
  [303, 212, 'e14fad1a1a0ad49af8f465c1b717c200a46e8439b530b8ba1d33c3f1f46894b9', '9xus318mcpw.iSRVFZDbK1wXkLNxNVxc', 'srtm/N29E033.tif, srtm/N28E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [303, 213, 'e4ea7fbf1654cf7f36728bff3a5ecfeba215cce20d65508e0088266c53bad969', 'akmPK9Amt1CTRgqYGDG9njWmSSgf0YEO', 'srtm/N28E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [303, 214, 'ba147c5dc1984edae956beadc1b63e03c12c7fc420547363e74473838041db55', 'ssfFCJE3oAQBh27nxXy.AcIBmfA8ez4F', 'srtm/N27E033.tif, srtm/N28E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [303, 215, '3f1312eacd3cddf17dab34cb2525225e8676afc8aeeb292c16a006e0f650f317', '1NM50M3TOYNhGLZa5KrPp5poqCCrVVdU', 'srtm/N27E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 205, 'afae232997a84bbb8a1fa805f381c6e4807bc8174386727af7c95c1f922ca1ad', 'zmfnCQQuyQXUAyH4w4bg8ivsKr75Fxlb', 'etopo1/ETOPO1_Bed_g.tif'],
  [304, 206, 'ace13ffd8e7bbb6f98e586b4c37a76dd1d31f31f46d620c3c8380db1984c7868', 'A_ozs4yKV0GzMhrknqVtnlw1hpOZR4.i', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 207, '9cd370ff06f10f1b26f232a4b9cac681cc747c24be784f43ca88a0a3a5027137', 'nKEPloUZg5scknHRQ.0pH76KwgGDOUQv', 'gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 208, 'e5eb8dad67c714a244741013ba32ba8ae88f759e045f247a42bbc145d64c0080', 'OYw64zQOttz2ybV9fNuHACnYZQc2NwXL', 'srtm/N31E034.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 209, 'daf5bfcfd2f1a4812154994b0fe1fb30dd1cee112f1cfdad240208d63ddab91e', 'd9i7f_t1nm9xnI.eWCyN94Hh1_.tn.tR', 'srtm/N31E034.tif, srtm/N31E033.tif, srtm/N30E034.tif, srtm/N30E033.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 210, 'de433c449405b2e2426ff9307d2b98fdc17e7f9dd2e19633c5d44e59c03476ed', 'xAwOFMC50845t6lMtQXK1d_Bp39L0VWE', 'srtm/N30E034.tif, srtm/N30E033.tif'],
  [304, 211, 'fbd099d37b2569bef5cba794e0da17232368e2db54bf1590c8b1974769bcc6e2', '3bArUl2gaVaRrdqdBCPm2ohRXH2q8pbH', 'srtm/N29E034.tif, srtm/N29E033.tif, srtm/N30E034.tif, srtm/N30E033.tif'],
  [304, 212, '91ec8c4d90b3e51f8bf5a1f84167e9588b6777266ca95d2f5d0ad710f35b5328', '17CTnLJT9F1rdlPSnQ710OFYU2dR2lnZ', 'srtm/N29E034.tif, srtm/N29E033.tif, srtm/N28E034.tif, srtm/N28E033.tif'],
  [304, 213, '4e853974623be60897b1e9704843c7445adf663489a784a3045384d2d7dd31bf', 'JjjK17Eh1q.8oiD5HpIfXbSO501iVDfP', 'srtm/N28E034.tif, srtm/N28E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 214, 'ab658a8f72e7c13628bc16cbc484d69b4c744fac44db2b3a17bbe41ba4bebc34', 'Kcvwp1VhVgrQWLMiVyQEZ8LHLtOtVhn2', 'srtm/N27E034.tif, srtm/N28E034.tif, srtm/N28E033.tif, srtm/N27E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [304, 215, '3c0cc8977b7c53a8cd21e364d6364ce6e3568871cfb109a5c35528c3978ed26b', '0SIWif7TTY.9jswXz7nxDKVJeQadn7hy', 'srtm/N27E034.tif, srtm/N27E033.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 205, '0ba1217e5cf6386caecff45c8e5823c936f8986d8d13295e2544aefa30114b55', 'yF8afhvWd5mPtpEyODpnE1vtPuFTqA3y', 'srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 206, 'edb1837a78ec2dd7b86dc4faec32d49ec63451210a58b800a1364a17e27c4648', '5Cy43EfzJu1tK_4Os8wn.qREZzTqO81e', 'srtm/N32E034.tif, srtm/N32E035.tif, srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 207, 'fae2d1220318376e8fa5e2c7243b792030aba7d487a50a2f9cf3b0760c402acc', 'mUwcHy5KbXnLo7HNIZiigPkI7FjGinkY', 'srtm/N32E034.tif, srtm/N32E035.tif, srtm/N31E034.tif, srtm/N31E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 208, 'ff863328728a240f13c1e8d0331d84332179292c1c559a308d09637a28c7123b', 'GTx2mkvvYqzp57r4nDDB1fXWUlLLQKEV', 'srtm/N31E034.tif, srtm/N31E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 209, 'f7e274ad9786a930e8ef909268d5051604251da194a3cc2720af15d3adfab07b', 'v5t_Ift_SKWfcxhc7tr77wAySeUoGrrt', 'srtm/N31E034.tif, srtm/N30E034.tif, srtm/N31E035.tif, srtm/N30E035.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [305, 210, '9c705465705649bcd586abb2e24a64985560690cd9c7cc4c8c3599753f399e7e', 'TUwo8d865HPr0QJI7GDXt_6Wwk.WzUb4', 'srtm/N30E034.tif, srtm/N30E035.tif'],
  [305, 211, '32e23504661e676ae575a4fa6b2e86827fb760b5fc337ea872e89882e0f81c65', '3lgv6cn8WioBZnF8lY5r1DMkw2vz3odi', 'srtm/N29E034.tif, srtm/N30E034.tif, srtm/N29E035.tif, srtm/N30E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 212, '100ad3f9513c9860ecb9f47e7a477d02fe85995daf7e3ecffd26995bb31588ba', '0WRj9Q75s0Z3r9nVo8dNewnJD71m5Vog', 'srtm/N29E034.tif, srtm/N29E035.tif, srtm/N28E034.tif, srtm/N28E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 213, 'e246c873983dd72d6ce7f2e0a0075fe93125aeb8dc97cce6214f0c0d5424e366', 'me2prCrVWV6q1Q1k4vyvNC5jh8kqdNzZ', 'srtm/N28E034.tif, srtm/N28E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 214, '80796a9a1705390fd59df2308c778ebe69738c9590dcd322766b92503c16aad2', '0N0sA5LWJ2XuugzVxIlBBV0QYAK.hDgP', 'srtm/N27E034.tif, srtm/N28E034.tif, srtm/N28E035.tif, srtm/N27E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [305, 215, '839f4580840d15324d049d08913dd69688f8b756c1474990ec7c126f1c1d1869', 'L41gX0jeqmXn2vmX_UNM7M2iR9x9sWfX', 'gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 205, '6859363803827d39e239328fa8f7256bac9bad9617589ba8511461ed793f9c37', 'BiYjHwl8KktK59qhh3n.YAgYjiDe.RMC', 'srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 206, 'f241984bc914661a3cd81bb715e5dd37bf570b73fb6668194a34f4242a1ba894', 'qZ0hOwamJT2_1ZHaMZntp8lZPgwfLCRP', 'srtm/N32E035.tif, srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 207, 'f4196157da4625bf19580e179784bdc4742c2977acbe827eabb844c8f17f3861', 'uKBUCKgiZXOwmyYNtsvSM83unmIMAD62', 'srtm/N32E035.tif, srtm/N31E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 208, '76392d0d184bd09404b1429df33212d1c4975e3eb24f6e284b94f42bf56656f2', 'fbyI.YNKocEyqv.rLbRfCqgWAhmHxpQ5', 'srtm/N31E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 209, '25c12d65a9246367ae6bf39c46e035cba9dba975634ae13aa3b2692a0ccbeaeb', 'oRuC_b9HXGgdlhYvt3zHSMcZPT1EfVim', 'srtm/N31E035.tif, srtm/N30E035.tif, gmted/30N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 210, 'e8bb79caff47b6785d37a58f7e59687ecaa1edb0d159709a8be30d6d9c3892d4', 'ND.7G5EqyWflXBW._3_HgAfK7Mvezqr2', 'srtm/N30E035.tif'],
  [306, 211, '74a9f9399fff170cefb1111fa99d9542203ee834a0e6433f3fc7170eb86450ef', 'U5kagnlKwReYl_OPJYG6qV0AUnFfK5pH', 'srtm/N29E035.tif, srtm/N30E035.tif'],
  [306, 212, '663362f7e0bb950b8ea2861f437f06a9bfe166a27f519be8cbec2b5786860b07', 'q7T7EVfuP_PwFbnCw.TMGY0oP9fzuZr4', 'srtm/N29E035.tif, srtm/N28E035.tif'],
  [306, 213, 'da3727986b9bba96e77a7a0cdd18e7cd7b4a48f73b583b93ff9a2a57d1997076', 'RoBR1nx2JxFNnAPC51d6.MSJ1WGSZVhL', 'srtm/N28E035.tif'],
  [306, 214, '1c4f181fba6f6abe913c47168201ff9a2d2378fa9dd6ac8c9abbc1d77eecba31', '5QeYnsxpP1m2ZKTiQGQ98v9VDILdBXcT', 'srtm/N27E035.tif, srtm/N28E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [306, 215, 'd4a18b52617e8b4c282e48f8ccf86261a90d98e0b906e700a0d960c3c571ae66', 'oRHSMXdYYGYZkbMXP75SBOdIP..gXk3Z', 'srtm/N27E035.tif, gmted/10N030E_20101117_gmted_mea075.tif, etopo1/ETOPO1_Bed_g.tif'],
  [307, 205, 'c83399b34a144025d546fabb29add4777351fce08559503cf39aceaaa38c371c', 'Frwv.B9vElNR9dksv4XPpuH4ppXOkp7P', 'srtm/N33E036.tif, srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [307, 206, '9ebf2baf5e349b60f8f5779807a7bfd8c5b014ee5d4fc16db673aae21cdc500e', 'HO4Formhy8tygH1X4vuI_s6zXvEXWH87', 'srtm/N32E036.tif, srtm/N33E036.tif, srtm/N32E035.tif, srtm/N33E035.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [307, 207, '6822e9235a2b4685d9576f391a31c787f0138b54cad81b19e7161e32cb5d7e59', 'kE_RwfA4f4IELo2aqNtZaEN97r2p8wyC', 'srtm/N32E036.tif, srtm/N32E035.tif, srtm/N31E036.tif, srtm/N31E035.tif, gmted/30N030E_20101117_gmted_mea075.tif'],
  [307, 208, '72853c19efdaa1717e7d3030a24d87946a19ac3b8bec1ed7ac8ee8302c11a1bf', '8IjwOFuR_mFQ11hERS5msO.Ul0XfYADQ', 'srtm/N31E036.tif, srtm/N31E035.tif'],
  [307, 209, 'c9c887175ac4a40f4fec58cf9bf07c1f686f0a63cca256a142d534b205c3b5c9', 'kCalmg60bsYtzUUKI42ZEo5HpJsxqFej', 'srtm/N31E036.tif, srtm/N30E036.tif, srtm/N31E035.tif, srtm/N30E035.tif'],
  [307, 210, '0e098a389d5b545e008fb001d6c58b0a544471e0e14872c55a0b131663f0d15d', 'xEmYj75QzUsP60WBuC9VxzRTYjxAenG.', 'srtm/N30E036.tif, srtm/N30E035.tif'],
  [307, 211, '8bcbd9b09cb99b1be3ef688495b3929b8cb9f66df8be52a2b4bb6372d1eaf21a', 'K7Qz_bSsnQ.d4sf6thu9a9l9xuyxeEY1', 'srtm/N29E036.tif, srtm/N30E036.tif, srtm/N29E035.tif, srtm/N30E035.tif, gmted/10N030E_20101117_gmted_mea075.tif'],
  [307, 212, '7ba36fdc1c43291da6d0123e188fd9bb41cd11d111c667057b5fb10b6f9250ce', 'jvnA9m3KtQuPzDgrPzL4WmdT6Dl1_gL9', 'srtm/N29E036.tif, srtm/N29E035.tif, srtm/N28E036.tif, srtm/N28E035.tif'],
  [307, 213, 'df3d46a574b916493d5141cb59bde8ba1edf4e938cfacf4a07b11e638b1f5771', 'a3Rpu6cjEIx49IaHrKfzNyL2agSdPr6U', 'srtm/N28E036.tif, srtm/N28E035.tif, gmted/10N030E_20101117_gmted_mea075.tif'],
  [307, 214, 'bef01197a029507fb0202ea57936595632cc4e1e7696e49638f6e0422c69076b', 'iaK8ocojWrOKyKUY2ItSfw7XlXpYECaK', 'srtm/N27E036.tif, srtm/N28E036.tif, srtm/N27E035.tif, srtm/N28E035.tif'],
  [307, 215, '6db14b29d6e2b1b4a2432193a5d515544428d679b7f5159e66a9ee1f88cc38f2', 'ev8pp14MuxY1uFerwIDLKhKAmp1qSMVS', 'srtm/N27E036.tif, srtm/N27E035.tif'],
];

const PANELS = [
  {
    id: 'regional',
    bbox: [31.0, 27.4, 36.5, 33.5],
    x: 84,
    y: 98,
    height: 2240,
  },
  {
    id: 'levant',
    bbox: [33.1, 31.2, 36.2, 33.5],
    x: 1916,
    width: 1800,
  },
];

function usage() {
  return `usage: build-ark-journey-cartographic-base.mjs \\
  --data-dir NATURAL_EARTH_GEOJSON_DIR --build-dir IGNORED_BUILD_DIR \\
  [--out-svg FILE] [--out-png FILE] [--out-receipt FILE] \\
  [--magick COMMAND] \\
  [--rsvg-convert COMMAND]\n`;
}

function parseArgs(argv) {
  const values = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (key === '--help' || key === '-h') {
      process.stdout.write(usage());
      process.exit(0);
    }
    if (!key.startsWith('--') || i + 1 >= argv.length) {
      throw new Error(`invalid argument: ${key}\n${usage()}`);
    }
    values.set(key.slice(2), argv[i + 1]);
    i += 1;
  }
  for (const required of ['data-dir', 'build-dir']) {
    if (!values.has(required)) {
      throw new Error(`missing --${required}\n${usage()}`);
    }
  }
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  return {
    dataDir: path.resolve(values.get('data-dir')),
    buildDir: path.resolve(values.get('build-dir')),
    outSvg: path.resolve(values.get('out-svg') ??
      path.join(values.get('build-dir'), 'ark-journey-cartographic-graphite-v3.svg')),
    outPng: path.resolve(values.get('out-png') ??
      path.join(scriptDir, 'ark-journey-cartographic-graphite-v3.png')),
    outReceipt: path.resolve(values.get('out-receipt') ??
      path.join(scriptDir, '..', 'research', 'cartographic-base-v3-receipt.json')),
    magick: values.get('magick') ?? 'magick',
    rsvgConvert: values.get('rsvg-convert') ?? 'rsvg-convert',
  };
}

function sha256(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function checkedRead(file, expectedSha256) {
  const bytes = fs.readFileSync(file);
  const actual = sha256(bytes);
  if (actual !== expectedSha256) {
    throw new Error(`SHA-256 mismatch for ${path.basename(file)}: ${actual}`);
  }
  return bytes;
}

function run(command, args) {
  const result = spawnSync(command, args, { encoding: 'utf8' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(
      `${command} failed (${result.status}):\n${result.stderr || result.stdout}`,
    );
  }
}

function commandOutput(command, args) {
  const result = spawnSync(command, args, { encoding: 'utf8' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(
      `${command} failed (${result.status}):\n${result.stderr || result.stdout}`,
    );
  }
  return result.stdout.trimEnd().split(/\r?\n/).map((line) => line.trimEnd()).join('\n');
}

function verifyToolchain(options) {
  const actual = {
    node: process.version,
    imagemagick: commandOutput(options.magick, ['--version']),
    rsvg_convert: commandOutput(options.rsvgConvert, ['--version']),
  };
  for (const [tool, expected] of Object.entries(EXPECTED_TOOLCHAIN)) {
    if (actual[tool] !== expected) {
      throw new Error(`${tool} version differs from the pinned cartographic toolchain`);
    }
  }
  return actual;
}

function download(url, redirects = 4) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Triptych cartographic source audit' } },
      (response) => {
        if ([301, 302, 307, 308].includes(response.statusCode) &&
            response.headers.location && redirects > 0) {
          response.resume();
          resolve(download(response.headers.location, redirects - 1));
          return;
        }
        if (response.statusCode !== 200) {
          response.resume();
          reject(new Error(`${url}: HTTP ${response.statusCode}`));
          return;
        }
        const chunks = [];
        response.on('data', (chunk) => chunks.push(chunk));
        response.on('end', () => resolve({
          bytes: Buffer.concat(chunks),
          headers: response.headers,
        }));
      }).on('error', reject);
  });
}

async function acquireTiles(buildDir) {
  const tilesDir = path.join(buildDir, 'tiles', String(ZOOM));
  const records = new Array(TERRARIUM_TILES.length);
  let next = 0;
  async function worker() {
    while (next < TERRARIUM_TILES.length) {
      const index = next;
      next += 1;
      const [x, y, expected, versionId, imagerySources] = TERRARIUM_TILES[index];
      const dir = path.join(tilesDir, String(x));
      const file = path.join(dir, `${y}.png`);
      const unversionedUrl = `${TILE_BASE_URL}/${ZOOM}/${x}/${y}.png`;
      const url = `${unversionedUrl}?versionId=${encodeURIComponent(versionId)}`;
      fs.mkdirSync(dir, { recursive: true });
      let bytes;
      if (fs.existsSync(file)) {
        bytes = fs.readFileSync(file);
      } else {
        const downloaded = await download(url);
        bytes = downloaded.bytes;
        if (downloaded.headers['x-amz-version-id'] !== versionId ||
            downloaded.headers['x-amz-meta-x-imagery-sources'] !== imagerySources) {
          throw new Error(`version or imagery-source header mismatch: ${url}`);
        }
        if (sha256(bytes) !== expected) {
          throw new Error(`versioned tile bytes differ from the pin: ${url}`);
        }
        const temporary = `${file}.download`;
        fs.writeFileSync(temporary, bytes);
        fs.renameSync(temporary, file);
      }
      const actual = sha256(bytes);
      if (actual !== expected) {
        throw new Error(`cached tile SHA-256 mismatch: ${file}`);
      }
      records[index] = {
        z: ZOOM,
        x,
        y,
        url,
        version_id: versionId,
        imagery_sources: imagerySources,
        sha256: actual,
        bytes: bytes.length,
      };
    }
  }
  await Promise.all(Array.from({ length: 8 }, worker));
  return { tilesDir, records };
}

function globalPixelX(lon) {
  return ((lon + 180) / 360) * (2 ** ZOOM) * TILE_SIZE;
}

function globalPixelY(lat) {
  const radians = lat * Math.PI / 180;
  const mercator = Math.log(Math.tan(radians) + 1 / Math.cos(radians));
  return ((1 - mercator / Math.PI) / 2) * (2 ** ZOOM) * TILE_SIZE;
}

function preparePanels() {
  const result = PANELS.map((panel) => {
    const [west, south, east, north] = panel.bbox;
    const projectedWidth = globalPixelX(east) - globalPixelX(west);
    const projectedHeight = globalPixelY(south) - globalPixelY(north);
    const width = panel.width ?? panel.height * projectedWidth / projectedHeight;
    const height = panel.height ?? panel.width * projectedHeight / projectedWidth;
    return { ...panel, width, height };
  });
  result[1].y = (HEIGHT - result[1].height) / 2;
  return result;
}

function featureLines(geometry) {
  if (!geometry) return [];
  if (geometry.type === 'LineString') return [geometry.coordinates];
  if (geometry.type === 'MultiLineString') return geometry.coordinates;
  return [];
}

function featurePolygons(geometry) {
  if (!geometry) return [];
  if (geometry.type === 'Polygon') return [geometry.coordinates];
  if (geometry.type === 'MultiPolygon') return geometry.coordinates;
  return [];
}

function clipSegment(a, b, bbox) {
  const [west, south, east, north] = bbox;
  let [x0, y0] = a;
  let [x1, y1] = b;
  const outcode = (x, y) =>
    (x < west ? 1 : 0) | (x > east ? 2 : 0) |
    (y < south ? 4 : 0) | (y > north ? 8 : 0);
  let code0 = outcode(x0, y0);
  let code1 = outcode(x1, y1);
  while (true) {
    if (!(code0 | code1)) return [[x0, y0], [x1, y1]];
    if (code0 & code1) return null;
    const code = code0 || code1;
    let x;
    let y;
    if (code & 8) {
      x = x0 + (x1 - x0) * (north - y0) / (y1 - y0);
      y = north;
    } else if (code & 4) {
      x = x0 + (x1 - x0) * (south - y0) / (y1 - y0);
      y = south;
    } else if (code & 2) {
      y = y0 + (y1 - y0) * (east - x0) / (x1 - x0);
      x = east;
    } else {
      y = y0 + (y1 - y0) * (west - x0) / (x1 - x0);
      x = west;
    }
    if (code === code0) {
      x0 = x;
      y0 = y;
      code0 = outcode(x0, y0);
    } else {
      x1 = x;
      y1 = y;
      code1 = outcode(x1, y1);
    }
  }
}

function samePoint(a, b) {
  return Math.abs(a[0] - b[0]) < 1e-10 && Math.abs(a[1] - b[1]) < 1e-10;
}

function clipLine(points, bbox) {
  const parts = [];
  let current = [];
  for (let i = 1; i < points.length; i += 1) {
    const segment = clipSegment(points[i - 1], points[i], bbox);
    if (!segment) {
      if (current.length > 1) parts.push(current);
      current = [];
      continue;
    }
    if (!current.length || !samePoint(current[current.length - 1], segment[0])) {
      if (current.length > 1) parts.push(current);
      current = [segment[0], segment[1]];
    } else {
      current.push(segment[1]);
    }
  }
  if (current.length > 1) parts.push(current);
  return parts;
}

function clipRing(ring, bbox) {
  let points = ring.slice();
  if (points.length > 1 && samePoint(points[0], points[points.length - 1])) {
    points.pop();
  }
  const [west, south, east, north] = bbox;
  const boundaries = [
    {
      inside: ([x]) => x >= west,
      intersect: (a, b) => [west, a[1] + (b[1] - a[1]) * (west - a[0]) / (b[0] - a[0])],
    },
    {
      inside: ([x]) => x <= east,
      intersect: (a, b) => [east, a[1] + (b[1] - a[1]) * (east - a[0]) / (b[0] - a[0])],
    },
    {
      inside: ([, y]) => y >= south,
      intersect: (a, b) => [a[0] + (b[0] - a[0]) * (south - a[1]) / (b[1] - a[1]), south],
    },
    {
      inside: ([, y]) => y <= north,
      intersect: (a, b) => [a[0] + (b[0] - a[0]) * (north - a[1]) / (b[1] - a[1]), north],
    },
  ];
  for (const boundary of boundaries) {
    if (!points.length) break;
    const input = points;
    points = [];
    let previous = input[input.length - 1];
    let previousInside = boundary.inside(previous);
    for (const point of input) {
      const pointInside = boundary.inside(point);
      if (pointInside) {
        if (!previousInside) points.push(boundary.intersect(previous, point));
        points.push(point);
      } else if (previousInside) {
        points.push(boundary.intersect(previous, point));
      }
      previous = point;
      previousInside = pointInside;
    }
  }
  return points.length >= 3 ? points : [];
}

function projector(panel) {
  const [west, south, east, north] = panel.bbox;
  const x0 = globalPixelX(west);
  const y0 = globalPixelY(north);
  const dx = globalPixelX(east) - x0;
  const dy = globalPixelY(south) - y0;
  return ([lon, lat]) => [
    panel.x + (globalPixelX(lon) - x0) * panel.width / dx,
    panel.y + (globalPixelY(lat) - y0) * panel.height / dy,
  ];
}

function number(value) {
  return Number(value.toFixed(2)).toString();
}

function pathForLines(collection, panel, includeFeature = () => true) {
  const project = projector(panel);
  const commands = [];
  for (const feature of collection.features) {
    if (!includeFeature(feature)) continue;
    for (const line of featureLines(feature.geometry)) {
      for (const part of clipLine(line, panel.bbox)) {
        const projected = part.map(project);
        commands.push(`M${number(projected[0][0])},${number(projected[0][1])}`);
        for (let i = 1; i < projected.length; i += 1) {
          commands.push(`L${number(projected[i][0])},${number(projected[i][1])}`);
        }
      }
    }
  }
  return commands.join('');
}

function pathForPolygons(collection, panel) {
  const project = projector(panel);
  const commands = [];
  for (const feature of collection.features) {
    for (const polygon of featurePolygons(feature.geometry)) {
      for (const ring of polygon) {
        const clipped = clipRing(ring, panel.bbox);
        if (!clipped.length) continue;
        const projected = clipped.map(project);
        commands.push(`M${number(projected[0][0])},${number(projected[0][1])}`);
        for (let i = 1; i < projected.length; i += 1) {
          commands.push(`L${number(projected[i][0])},${number(projected[i][1])}`);
        }
        commands.push('Z');
      }
    }
  }
  return commands.join('');
}

function buildMosaic(options, tilesDir) {
  const rows = [];
  for (let y = TILE_Y_MIN; y <= TILE_Y_MAX; y += 1) {
    const row = path.join(options.buildDir, `terrarium-row-${y}.png`);
    const inputs = [];
    for (let x = TILE_X_MIN; x <= TILE_X_MAX; x += 1) {
      inputs.push(path.join(tilesDir, String(x), `${y}.png`));
    }
    run(options.magick, [
      ...inputs, '+append', '-strip', '-define', 'png:exclude-chunks=date,time', row,
    ]);
    rows.push(row);
  }
  const mosaic = path.join(options.buildDir, 'terrarium-mosaic.png');
  run(options.magick, [
    ...rows, '-append', '-strip', '-define', 'png:exclude-chunks=date,time', mosaic,
  ]);
  const dem = path.join(options.buildDir, 'terrarium-dem.miff');
  run(options.magick, [
    mosaic,
    '-alpha', 'off',
    '-colorspace', 'sRGB',
    '-fx', '(u.r*65280+u.g*255+u.b*0.99609375)/65535',
    '-depth', '16',
    dem,
  ]);
  const hillshade = path.join(options.buildDir, 'terrarium-hillshade.png');
  run(options.magick, [
    dem,
    '-level', '49%,52%',
    '-shade', '315x38',
    '-colorspace', 'Gray',
    '-auto-level',
    '-fill', 'white',
    '-colorize', '35%',
    '-depth', '8',
    '-strip',
    '-define', 'png:color-type=0',
    '-define', 'png:compression-level=9',
    '-define', 'png:exclude-chunks=date,time',
    hillshade,
  ]);
  const upper = path.join(options.buildDir, 'terrain-seam-upper-control.png');
  const lower = path.join(options.buildDir, 'terrain-seam-lower-control.png');
  const ramp = path.join(options.buildDir, 'terrain-seam-ramp.png');
  const replacement = path.join(options.buildDir, 'terrain-seam-replacement.png');
  const repaired = path.join(options.buildDir, 'terrarium-hillshade-repaired.png');
  const mosaicWidth = (TILE_X_MAX - TILE_X_MIN + 1) * TILE_SIZE;
  const replacementHeight = TERRAIN_SHADE_SEAM_REPAIR.lastReplacedRow -
    TERRAIN_SHADE_SEAM_REPAIR.firstReplacedRow + 1;
  run(options.magick, [
    hillshade,
    '-crop', `${mosaicWidth}x1+0+${TERRAIN_SHADE_SEAM_REPAIR.upperControlRow}`,
    '+repage', upper,
  ]);
  run(options.magick, [
    hillshade,
    '-crop', `${mosaicWidth}x1+0+${TERRAIN_SHADE_SEAM_REPAIR.lowerControlRow}`,
    '+repage', lower,
  ]);
  run(options.magick, [
    upper, lower, '-append', '-filter', 'Triangle',
    '-resize', `${mosaicWidth}x${replacementHeight + 2}!`, ramp,
  ]);
  run(options.magick, [
    ramp,
    '-crop', `${mosaicWidth}x${replacementHeight}+0+1`,
    '+repage', replacement,
  ]);
  run(options.magick, [
    hillshade,
    replacement,
    '-geometry', `+0+${TERRAIN_SHADE_SEAM_REPAIR.firstReplacedRow}`,
    '-composite',
    '-depth', '8',
    '-strip',
    '-define', 'png:color-type=0',
    '-define', 'png:compression-level=9',
    '-define', 'png:exclude-chunks=date,time',
    repaired,
  ]);
  return repaired;
}

function xmlEscape(text) {
  return text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function renderSvg(hillshadeBytes, layers, panels, receipt) {
  const mosaicWidth = (TILE_X_MAX - TILE_X_MIN + 1) * TILE_SIZE;
  const mosaicHeight = (TILE_Y_MAX - TILE_Y_MIN + 1) * TILE_SIZE;
  const terrain = hillshadeBytes.toString('base64');
  const panelData = panels.map((panel) => ({
    panel,
    land: pathForPolygons(layers.land, panel),
    coastline: pathForLines(layers.coastline, panel),
    lakes: pathForPolygons(layers.lakes, panel),
    rivers: pathForLines(
      layers.rivers,
      panel,
      (feature) => !EXCLUDED_NAMED_CANALS.has(feature.properties?.name),
    ),
  }));
  const definitions = panelData.map(({ panel, land }) =>
    `    <clipPath id="panel-${panel.id}"><rect x="${number(panel.x)}" y="${number(panel.y)}" width="${number(panel.width)}" height="${number(panel.height)}"/></clipPath>\n` +
    `    <clipPath id="land-${panel.id}" clip-rule="evenodd"><path d="${land}"/></clipPath>`,
  ).join('\n');
  const drawings = panelData.map(({ panel, coastline, lakes, rivers }) => {
    const [west, , east, north] = panel.bbox;
    const cropX = globalPixelX(west) - TILE_X_MIN * TILE_SIZE;
    const cropY = globalPixelY(north) - TILE_Y_MIN * TILE_SIZE;
    const cropWidth = globalPixelX(east) - globalPixelX(west);
    const scale = panel.width / cropWidth;
    const tx = panel.x - cropX * scale;
    const ty = panel.y - cropY * scale;
    return `  <g clip-path="url(#panel-${panel.id})">\n` +
      `    <rect x="${number(panel.x)}" y="${number(panel.y)}" width="${number(panel.width)}" height="${number(panel.height)}" fill="#f8f8f8"/>\n` +
      `    <rect x="${number(panel.x)}" y="${number(panel.y)}" width="${number(panel.width)}" height="${number(panel.height)}" fill="#dedede" clip-path="url(#land-${panel.id})"/>\n` +
      `    <g clip-path="url(#land-${panel.id})"><use href="#terrain" transform="matrix(${scale.toFixed(12)} 0 0 ${scale.toFixed(12)} ${tx.toFixed(6)} ${ty.toFixed(6)})" opacity="0.94"/></g>\n` +
      `    <path d="${coastline}" fill="none" stroke="#f8f8f8" stroke-width="4.8" stroke-linecap="round" stroke-linejoin="round"/>\n` +
      `    <path d="${coastline}" fill="none" stroke="#313131" stroke-width="1.56" stroke-linecap="round" stroke-linejoin="round"/>\n` +
      `    <path d="${lakes}" fill="#eeeeee" fill-rule="evenodd" stroke="#5a5a5a" stroke-width="1.16" stroke-linejoin="round"/>\n` +
      `    <path d="${rivers}" fill="none" stroke="#747474" stroke-width="0.96" stroke-linecap="round" stroke-linejoin="round"/>\n` +
      '  </g>';
  }).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}">\n` +
    `  <metadata>${xmlEscape(JSON.stringify(receipt))}</metadata>\n` +
    '  <defs>\n' +
    `    <image id="terrain" width="${mosaicWidth}" height="${mosaicHeight}" href="data:image/png;base64,${terrain}"/>\n` +
    `${definitions}\n` +
    '  </defs>\n' +
    `  <rect width="${WIDTH}" height="${HEIGHT}" fill="#f8f8f8"/>\n` +
    `${drawings}\n` +
    '</svg>\n';
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const toolchain = verifyToolchain(options);
  const recipeSha256 = sha256(fs.readFileSync(fileURLToPath(import.meta.url)));
  fs.mkdirSync(options.buildDir, { recursive: true });
  fs.mkdirSync(path.dirname(options.outSvg), { recursive: true });
  fs.mkdirSync(path.dirname(options.outPng), { recursive: true });
  fs.mkdirSync(path.dirname(options.outReceipt), { recursive: true });

  const layers = {};
  const naturalEarthRecords = [];
  for (const [id, filename, expected] of NATURAL_EARTH) {
    const bytes = checkedRead(path.join(options.dataDir, filename), expected);
    layers[id] = JSON.parse(bytes.toString('utf8'));
    naturalEarthRecords.push({
      id,
      version: '5.1.2',
      source_page: NATURAL_EARTH_SOURCE_PAGE,
      filename,
      sha256: expected,
      bytes: bytes.length,
    });
  }

  const { tilesDir, records: tileRecords } = await acquireTiles(options.buildDir);
  const panels = preparePanels();
  const receipt = {
    schema: 'triptych-cartographic-input-receipt/v1',
    acquired_on: ACQUIRED_ON,
    projection: 'EPSG:3857 Web Mercator, north-up',
    toolchain,
    output: {
      width: WIDTH,
      height: HEIGHT,
      mode: 'grayscale',
      sha256: EXPECTED_OUTPUT_SHA256,
      svg_embeds_receipt: true,
      png_embeds_receipt: false,
    },
    recipe: { sha256: recipeSha256 },
    panels: panels.map((panel) => ({
      id: panel.id,
      bbox_wgs84: panel.bbox,
      panel_rect: {
        x: Number(panel.x.toFixed(6)),
        y: Number(panel.y.toFixed(6)),
        width: Number(panel.width.toFixed(6)),
        height: Number(panel.height.toFixed(6)),
      },
    })),
    natural_earth: naturalEarthRecords,
    terrarium: {
      encoding: 'Mapzen Terrarium',
      zoom: ZOOM,
      tile_extent_xyz: [TILE_X_MIN, TILE_Y_MIN, TILE_X_MAX, TILE_Y_MAX],
      hillshade: {
        azimuth_degrees: 315,
        elevation_degrees: 38,
        dem_level_percent: [49, 52],
        auto_level: true,
        white_blend_percent: 35,
        source_seam_repair: {
          method: 'linear image-space interpolation between adjacent uncontaminated shaded rows',
          ...TERRAIN_SHADE_SEAM_REPAIR,
        },
      },
      tiles: tileRecords,
    },
    vector_treatment: {
      natural_earth_layers: ['land', 'coastline', 'lakes', 'rivers'],
      excluded_named_canals: [...EXCLUDED_NAMED_CANALS],
      political_boundaries: 'not loaded',
      labels_markers_routes: 'not drawn',
    },
  };
  const receiptBytes = `${JSON.stringify(receipt, null, 2)}\n`;
  fs.writeFileSync(
    path.join(options.buildDir, 'cartographic-input-receipt.json'),
    receiptBytes,
  );
  fs.writeFileSync(options.outReceipt, receiptBytes);

  const hillshade = buildMosaic(options, tilesDir);
  const svg = renderSvg(fs.readFileSync(hillshade), layers, panels, receipt);
  const temporarySvg = `${options.outSvg}.tmp`;
  fs.writeFileSync(temporarySvg, svg);
  fs.renameSync(temporarySvg, options.outSvg);

  const rendered = path.join(options.buildDir, 'cartographic-render-rsvg.png');
  run(options.rsvgConvert, [
    '--format', 'png', '--width', String(WIDTH), '--height', String(HEIGHT),
    '--output', rendered, options.outSvg,
  ]);
  const temporaryPng = `${options.outPng}.tmp`;
  run(options.magick, [
    rendered,
    '-colorspace', 'Gray',
    '-alpha', 'off',
    '-depth', '8',
    '-strip',
    '-define', 'png:color-type=0',
    '-define', 'png:compression-level=9',
    '-define', 'png:exclude-chunks=date,time',
    temporaryPng,
  ]);
  fs.renameSync(temporaryPng, options.outPng);
  const outputSha256 = sha256(fs.readFileSync(options.outPng));
  if (outputSha256 !== receipt.output.sha256) {
    throw new Error(`PNG SHA-256 differs from the pinned output: ${outputSha256}`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
});
