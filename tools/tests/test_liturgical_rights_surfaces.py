#!/usr/bin/env python3
"""One rights boundary for source payloads, CLI, browser data, and downloads.

The ICEL web permission is surface-specific.  It does not clear the same words
for a public Git corpus, a command-line export, a PDF, or another downloadable
file.  These checks deliberately cross those seams: a green browser test is not
enough if the tracked TSV or the JSON behind the browser still distributes the
text.

This file contains no protected liturgical wording.  The synthetic CLI marker
is project-created test prose, and registered protected artifacts are compared
by digest rather than copied or quoted.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
import tomllib
import unicodedata
import unittest
import zipfile
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TPT = ROOT / "tools" / "tpt"
STRUCTURE_ROOT = ROOT / "src" / "web" / "data" / "structure"
WORKS_ROOT = ROOT / "src" / "sources" / "works"
ICEL_MARKER = "international-commission-on-english-in-the-liturgy"
FDLC_WORK_ROOT = (
    WORKS_ROOT
    / "federation-of-diocesan-liturgical-commissions"
    / "mystagogical-reflections"
)
FDLC_PUBLIC_EDITIONS = (
    STRUCTURE_ROOT
    / "sources"
    / "editions"
    / "federation-of-diocesan-liturgical-commissions"
    / "mystagogical-reflections"
)
FDLC_INVENTORY = (
    ROOT
    / "src"
    / "sources"
    / "inventories"
    / "postconciliar-proper-translations-v1.toml"
)
ELLC_EDITION_ID = (
    "edition.english-language-liturgical-consultation.praying-together.1998"
)
# SHA-256 of NFC/whitespace-normalized ELLC sense lines.  The protected words
# are deliberately not retained in this test or reconstructed at runtime.
ELLC_LINE_SHA256 = frozenset(
    """
01c8576bb1453c9c5ef21d54838b79034f5c22c80f46ac173ee352133fb7243a
03f030bf047ffedecbf58558653a2e1b0b6fb811c1117f6de0aebd5e323bcac9
083652146dae34ca5b195aa1913048da2fe1ac687847babf8de3f6d4b59d1a97
0c07a263fc1d2446098667f41c6021a339f8d48820fbb19eb85753b85f89d15b
0da882ca1f892b826fea3215e51613cf9c99ba58545abb9714a22b693142a9a0
0ee2ad90439a0b3ffc415134884f1dbe85cb4b7d14794f7895e9c0e536fd0c8a
15609d5202d47035d2df8d3ebd4ab8354292a7a055f21e4e8ba0d6c96639d70b
169cd3b056cfd01c4475b2ba117e76701d6fbc35674c78d4ab183738e9b28619
16c9633d625b473e00f577fe01b4881e4e751c26fdd1e17056342cc1f4e295b5
19d533ceae2f85af5616497fd930f3eef65957c5fd2d3eeb250616e9c29a8e43
1bb2bf20cce60df202a8299a17bc1017cebfbdb38d852739d2003fdd4bb06fb1
1cbdcd75155878c48761069b1f4905316a86784bc6cda4f2260fe0cb5f1a3176
1fab3540cce5dbf0fe80678f5d3b04cab06c51eb356e3b6570b2513fccfffa2e
210bf867664809a81ebce2eb54b7f17878e2369a39d4721dd6be9672c7b9c3db
230dfca90dcc2a3e7f390d375b31c2d706219bb350e79424504e52112f4466fb
268f1b109bc80246d53af72b2d7337867b6789650d3d851f9f47f5a5940a1973
292e6b4b89e8ae4f998a474830fa8f40ac99a8731354d1b17517ce1a809633a5
2b8cb9e49938296dafe6fef2416d3e34b98fea35bff590173a2737e7bf2895b7
2c104cb993e62222d7ad33b2fe049a83565e182a3e461d019615ad013c56d8cf
321f1ec52d6d2de96b80ba3b2a0b82f0d353e99920bc092fe07531a1daab8cd0
35e2f8d0a78602f8fad11d3ff34f5e2736cd1367220bef536a498d2fd6e389a8
391914b3dd0d53ee190409dad4dbe3d513d088abaa9b64a28050ea1f21d465c4
3978e47f9c0df68481ec2fa8ebfb88119ee0c722bc80d043d84e0ea4c80bb348
3a0121302ba9091d50c7820ce170d0d50f8ce1f39ca3657ceaae2b98856a7a83
3cbc1625acd32b5bbd9789e496d09f638ef702bd05fab9f58635b9ffe7cc1c5c
3e89a95036799784626761699322a694ac292f4df35ef4af0158660fef079670
422b89d21f191fd3bf4eeab3709c20fa1339269d1b13cfbae5f5002c2933bb68
43b925fa0e8bea56d14cebf00dfc7e6a90f9f5519e2a83653a014cfdc6d44786
4a6b912157b7540cecd9f1233ee15a59403a7c1d0a41765756e5db1ae98ed95e
4c2eefa78d6e8b0eeb4c9ec8d8579ffb79102ee4c5f6206198d5860f14501f71
4d4bdf854bf565bf2f8abedfe4f719221a3a059606cfb4991df894d453803b13
50d6c8175648255e90537274615fcd8759d6060b9ac8cca9ab9b896baef1aeb8
598a3f2a060b3677764de4989685e9fa2a4e530f328b861031faecbf93f62f36
5ef37b6f490465a08d8b56001ed72ea1e07fc0efb953c7b4e461718b32879401
681933bf1150848e72696f5dec7c22477736cad27d93dba0db6e61294dcb1579
6fb6a0ec05abd6f679d50a7912d43e4b36cf3db4ceae9f1440d94ce9a8c56bee
714e05555610ab1741212da737544fbc15dba8cc0780f987a0daeb44c3aa46f2
7451e95233124f8b34667f8a102102d75b72fff0606e1c51fb16da6fce55ca5a
762e148c503f269b71571b77b06cbd2a63f248f3f05c3b580b51c925d579d61f
77872da6c1ddc11c4ab2ed92466a5c599eb6b7867f7460969e299812c07b20aa
7d0c578f2b0363c30c6a0c315052500fb9e4c84f1703f6eb0f5f4bec91c623b8
7dcd528ec68046977e4c41973a5d3b09089e05a7159c0b6d2a2309648235b199
7e314dee770c129782c2261cb79907e02634bd3b7b30e5b12107b77c8410a57d
816119db8bc9e597013dbda43388214d087461c858570a3b01a6ea7262531fa3
8486c21ef8b4987f699479a18f5eca71df85946a09541da8be14cd2f143329c9
870badea56e53193b38c8d3436d80578d8a042b61bbcf072579478ee2385d8dc
871d49844353a78cf911d8ba1040b0b11919985295d5075d2180cea24ca1b234
89254a08cc3c6cd21462218155ed50be616b950c56ef98f735429c8d38a5ed3b
8a1df83877acc69b97b2309cb7e75ee4415a726c8f811d800c90c7150dcede0d
8a66173d2620db274e838e86d57df789f455ffd481f2938746509f6d7feef62e
8d2a01d94b4659e43e134a2b0a691eb0a5522a915a880fbdb0dcd9fe053d4113
8f75047ae8acbd4adbe8a8da380483580e13d3adf99fec2b975b5ecd00cdb082
8fbf71a1a29b2428d801455dc5481f3fcf65fbe7609f38a81c5e6c10dca97a93
90ebd2dea09943d16be912edc9a813a9844ca699d2580491f29dc48954c9c060
90ec20563f0516d20c414c95f9b69a4f2f3fe1bc6a7ac35525ba43e8cb03a41d
944b41406aa367ed8b46a23443e305280a41fc236c10dcbc88da3ff738bb8b15
9510c55f1d5ea3abf05fa04eb5718a436ebdb4930d980bf8038af63a161affb1
959a4087b9a193f46edf9d2926322ab514cfb5ac346469470ff2c69925f5e343
96ad0fb25487a0fe55fc59335e5e2d6c22d56c3671f23327a4d6fc6a6a6636f9
9b3b983d2020dabfee2531a9ef4b4b099b9fc9251b524fbc3a31c66b4d8b71d9
9b847c0eb54f39a47d80867e5cb5ea3a7df1f409ff31cabd52fed3b8d224847d
9c8674277cc17e584d5ec3acfaaf6d4e9afcacda1270d6383663a7e40a4ff3c0
a028c445a731f9164b5dd54e272a44de265abca1c9c4cd092eb34043aabc8f75
a521602157286154e4ac32d36d8b29fa73df3e7a9ef08754512f8dc41ed8c2f3
a5e7db1c649d8b28404113d69b2169b5144bfa3d6f1746b8b62df8ce742951f8
a8f1f246867bc41ac3b36fdbf1befb07a4f86deafb605e6146d1be912bf2fb9a
ac95171c155a4ad58e7306fbafe0bc06497fca2c2f0815322d46a969b1fb0e08
afa5fca21964c9ece808bc3e9ef63a3a1271e7941de132387dbb42e7287c4d47
b050cbe4e0e7a3d7a869c62ff613405f76b49b28da488c469c5ca6e2ed4f187d
b44ec458105366ac38d319396644345510a7cb5269e6de9316d8938e4e1d1353
b4768c8f4ea5aa1fcffabf70e258829547d7f6290d11c375f9efae325a8ceaac
b7b168eead2cde59afffc286d3c61594b37cdc59721bdae30297bd4f6ac6f43c
b95c2e0ca8879fab7a35cdc6714735198e035e8a039cf1cbba22d2ca75ec2ac1
bab0fae6026fb49d07306f6a156a4c6dd3ad2a6776d3aa5113816c91909ceec1
bcdc1808c484acce9c9cd15b221fb3f8f66ffc51b9bec068e50369f719f2ee46
bd224aa28ddfcd496903f984cec724aa74149438ddb65282f6183f20603b2590
c09b5330541b566f7888757dd24c648e76ebe3db7f912edb6ce3a200bc99e179
c4c65632ddd24d76b48ff5b177f4ac2f875ec4123abb0f90b2d5d6de29af61d3
c9b242c5ae3c916ae18b6f837fb643d9bc77df14d80ca5ef902463142676ee1b
cac709eea49356e01117c20503472559a072277bde3255ce743c5cd30ee95fc0
cbe3153c0f2dc60423a7121c533c6fb8fb5e78fe2c6e4fb5e2b14e6032e1cd0e
cc20bbe1f2d08b19aaf57c6ccffdc195be79d3856f711832a59ce27f22157d5f
cce331567035959a480dcc36160d778b0640a27c683d1dcfd52f0fe5181b9264
cf2d6b448119f9c4455e0310b5140a84bc5db3b81d28cff7217955a3e1696436
d0dabd563b8199e1859a3380994d7c06c4602be0828fdeb1e0e99984d35ca7f2
d291c2f8c7d1f4c4d0ebb17a2fa8ff75c6fdc0f06d763d6df9dbc777f9475143
d36c35f9f394b771bbf277c401a1a97e52981932bfdb46b1c5563717e1cb2ce9
d3b28d01b4ca215e0eb270ac3f64088c9d35ce6f3a747c6bee3d0f492d539731
d552cb084629f304f10e8ee41190dc5287e772fdd43f854f8f6a45664e25f898
d6a3f0b0c54a124ecea4910e886951c0e42f1e10adbb38ed169be55f3cc42cca
da0a4456943c711eea4010c00988670c1938b883a4f8bf019813d81b746951a7
da5ca96b71e9e01dd7d320449d7aaf41278a5f734192fc224a946cd5749b9089
db06cd6bd5318cc99750e19d9024f9d3100092993cd4d9a3349d95963da0fb75
dbcb715e16978b183fd24abcd086609e2e68b56f22ae34ccaa21e594370e29d1
dc21de297935cddb8a68c66064d262d4311da38788cb80f8102b83b62624f107
dc79d5279c604001f0c8610db901d549046e026b847149b77424b9728c88ba69
dee132feb1a819d45ead3750097aceb8f5d690917f7b6eaeaa8d21a5637b4223
deb5f56d63598a39581ca754369d076ceef6136bc182095d408212418e8acef0
e2133e2efd5ded2e31b7cf8c6890a52e8e69c80d91fb98806cc873a8343f9692
e39034cdc6c08df427bdef86c19bca5e78daa10e39dc74c0cc84396ccd166691
e582b88aa2550cdd0290b2a1118cfd68eb02126d702ea1c68e3bfc47a1737e1b
e7a8ddec2acfadd31a3b160b3ac0e4bc7640b424616a96c9bfdff2e3204bed0f
e88327f8d488296686cd2a8e564ec55823ab3df874d675c85c26006ae7e50d13
e9c5f9ef82d0caaf8df6122527f59a58674f8eb78681532beb64d224a7e48d86
ebd018bcbad71bf1edf5784123a1bf72170059a4c2e3ee20d4777abdca571348
ec4ab90762a4c52ccddd881c44e94a9965118d22d8291f9514d7c424abe554fb
ec710cf99c90fe1f1c3c7feab570c9483dfd31558179dc66d3b23d5dab2c786a
f70183184c1534a12a8ff32301a3764db206ee8482032024c87f928506ebc4b4
f9cc23f5a35b6e44ede2afbe24ff5e4e4dcab226d3d1262696e83f0c3a1500b3
fdd531594be4cb0422eceb8b5ac6e4269423a51e6eda8e21e78d6e2b2d4a6e0c
""".split()
)
ELLC_BODY_SHA256 = frozenset(
    """
254d4276eb9e8714713822afb9bd4ab4b3578ba8d231e99c5ca6266e39549226
2b6a21e4cd3a16dfc15e26e40dccfea0c5fa1da238e64d8fa959808d3b71af1f
3433a5ed7b29965061f901e0ea7d56f3eae90207ff9f48831630f4e6253b601e
35976eab28f72c97a4aa53953cfb1190b135e9c1782e2845548714f364285218
429d30637371eb4a7c2d24d81dae769dd69c2b2661e6c403f594f4bb41d048fc
4ea684bfdfdc8efe0d35eb417067459c31b63955a0aafc075674c5a84267f313
6018f010a53d224d76a7363f77baaf5c6d2ba8c3e19c519810283553cc1e05fc
60d028d062702e77c6b4f7ee1b4a80f7cd10a86fd8376889f03881af1c764790
a532e104797f6cc1736216db8e17fecef76514eaeb006ed8066aa17d9b9911ba
c865b4de0ffbd0d479520306d8dfdba19e7b59754e833b0159f7759a90e803f6
e31bf7d126222f5932425565dbbef16a8577550db53dad9f63895943f13c60af
""".split()
)
ELLC_TEXT_SHA256 = ELLC_LINE_SHA256 | ELLC_BODY_SHA256
# Word-count plus SHA-256 of case-folded alphanumeric tokens for the two
# protected Collect fragments formerly embedded in source-study notes.
PROTECTED_SNIPPET_FINGERPRINTS = {
    4: {"341a696549ed4123c802379f9cbc18e6209a59e5de1264016e80988aefedea2c"},
    5: {"400474acfe4f785a89407bf6650d46e68261377d0f6d696df5a91b5b885ea692"},
    6: {"e76bbc0b0b6fa98e023bd35384a241cb59f3b1023968218eb80ab05739d532ac"},
    12: {"c17a74c6a3e86d43592c9cfabd2bf3f32f36d0c86fb9b9b57db08ade28fed67c"},
    13: {"9b61b40caf1ecc6c6729e836aa984c9cfa85a1155f9eecfec8ee3f70a93607cb"},
}
# The liturgy generators intentionally have the narrower allow-list documented
# by the publication policy.  The general Sources reader may publish a genuine
# redistribution licence (for example CC BY-SA), but never an unresolved or
# surface-limited permission record.
UNSAFE_LITURGY_RIGHTS = {"licensed", "permission", "unresolved"}
PUBLIC_LITURGY_RIGHTS = {"project-created", "public-domain"}
SOURCE_DISTRIBUTABLE_RIGHTS = {"licensed", "project-created", "public-domain"}
IDENTITY_FIELDS = {
    "artifact",
    "artifact_id",
    "edition_id",
    "source",
    "source_id",
    "witness",
    "witness_artifact_id",
}
RESTRICTED_TRANSLATION_METADATA = IDENTITY_FIELDS | {
    "acknowledgement",
    "byte_size",
    "hash",
    "indexable",
    "license",
    "notice",
    "page",
    "page_count",
    "path",
    "permission",
    "quarantined_text_sha256",
    "rejected_detectors",
    "retrieved",
    "rights",
    "rights_basis",
    "rights_status",
    "sha256",
    "source_url",
    "surfaces",
    "verified_artifact_page",
    "verified_heading",
    "verified_on_page",
    "verified_printed_page",
    "verified_url",
}
SAFE_RESTRICTED_PROJECTION_FIELDS = {"target", "lang", "state"}
SAFE_PROPER_TARGET_FIELDS = {
    "mass",
    "form_id",
    "proper",
    "cycle",
    "occurrence",
    "extent",
}
SAFE_ORDINARY_ABSENCE_FIELDS = {"key", "count", "state", "kind"}
SAFE_COMMON_FROM_FIELDS = {"scope", "options"}
SAFE_COMMON_OPTION_FIELDS = {"mass", "form_id", "selection"}
LATIN_CAPABILITY_BODY_FIELDS = {
    "body",
    "content",
    "lines",
    "text",
    "texts",
    "translation",
    "translations",
}
LATIN_CAPABILITY_AUDIT_FIELD_PARTS = {
    "artifact",
    "evidence",
    "hash",
    "locus",
    "locator",
    "page",
    "passage",
    "permission",
    "provenance",
    "rights",
    "sha",
    "source",
    "verification",
    "verified",
    "witness",
}
ORDINARY_ABSENCE_KINDS = {
    "model-gap",
    "no-exemplar",
    "not-applicable",
    "outside-layer",
    "rights-withheld",
    "witness-gap",
}
NON_NEUTRAL_ABSENCE_KEY_PARTS = (
    "artifact",
    "copyright",
    "ellc",
    "icel",
    "permission",
    "source",
)
SOURCE_INVENTORIES = ROOT / "src" / "sources" / "inventories"
PUBLIC_SOURCE_TEXT = STRUCTURE_ROOT / "sources" / "text"
PUBLIC_LITURGY_ROOTS = (
    STRUCTURE_ROOT / "ordinary",
    STRUCTURE_ROOT / "propers",
)
RUBRICS_SOURCE_ROOT = ROOT / "src" / "sources" / "calendars"
RUBRICS_PUBLIC_ROOT = STRUCTURE_ROOT / "rubrics"
PROPER_LATIN_INVENTORY = (
    ROOT
    / "src"
    / "sources"
    / "inventories"
    / "roman-1962-proper-latin-provenance-v1.toml"
)
RUBRICS_ALLOWED_LATIN_PATHS = {
    "postconciliar": frozenset(),
    "roman-1962": frozenset(),
    "roman-pre-1955": frozenset(
        {"$.precedence.latin", "$.saturday_office.latin"}
    ),
}
RUBRICS_PRIVATE_PUBLIC_FIELDS = {
    "artifact",
    "artifact_id",
    "derived_from",
    "edition_id",
    "source_id",
    "witness",
    "witness_artifact_id",
    "witnesses",
}
DOWNLOAD_ROOTS = (
    ROOT / "pdf",
    ROOT / "downloads",
    *PUBLIC_LITURGY_ROOTS,
)
def files_under(*roots: Path) -> list[Path]:
    """Every current payload, including an untracked file a build might copy."""
    return sorted(
        path
        for root in roots
        if root.is_dir()
        for path in root.rglob("*")
        if path.is_file()
    )


def tracked_files(*pathspecs: str) -> list[Path]:
    """Existing files selected from Git's index, never incidental build output."""
    run = subprocess.run(
        ["git", "ls-files", "-z", "--", *pathspecs],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return sorted(
        ROOT / item.decode("utf-8")
        for item in run.stdout.split(b"\0")
        if item and (ROOT / item.decode("utf-8")).is_file()
    )


def decoded_text(path: Path) -> str | None:
    """UTF-8 text only; archives, images and other binary evidence stay separate."""
    content = path.read_bytes()
    if b"\0" in content:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None


def artifact_manifests(works_root: Path = WORKS_ROOT) -> list[tuple[Path, dict]]:
    """Read the source library instead of maintaining a second protected list."""
    return [
        (path, tomllib.loads(path.read_text(encoding="utf-8")))
        for path in sorted(works_root.glob("**/artifact.toml"))
    ]


def protected_artifact_manifests(
    works_root: Path = WORKS_ROOT,
) -> list[tuple[Path, dict]]:
    """Artifacts whose manifest records no repository redistribution basis."""
    return [
        (path, record)
        for path, record in artifact_manifests(works_root)
        if record.get("rights_status") not in SOURCE_DISTRIBUTABLE_RIGHTS
    ]


def protected_artifact_identities(
    protected: list[tuple[Path, dict]],
    all_records: list[tuple[Path, dict]] | None = None,
) -> set[str]:
    """Artifact ids plus editions for which every artifact is protected.

    A distributable normalized text may sit beside an unresolved capture of its
    permissions page, so one protected sibling must not poison that edition.
    Conversely, a new FDLC-style edition made entirely of unresolved remote
    PDFs is protected even when a projection records only its edition id.
    """
    artifact_ids = {
        str(record.get("id") or "")
        for _, record in protected
        if str(record.get("id") or "")
    }
    all_by_edition: dict[str, list[dict]] = defaultdict(list)
    for _, record in all_records or artifact_manifests():
        edition_id = str(record.get("edition_id") or "")
        if edition_id:
            all_by_edition[edition_id].append(record)
    fully_protected_editions = {
        edition_id
        for edition_id, artifacts in all_by_edition.items()
        if artifacts
        and all(
            artifact.get("rights_status") not in SOURCE_DISTRIBUTABLE_RIGHTS
            for artifact in artifacts
        )
    }
    editions_by_work: dict[str, set[str]] = defaultdict(set)
    for path, record in all_records or artifact_manifests():
        edition_id = str(record.get("edition_id") or "")
        edition_path = path.parents[2] / "edition.toml"
        if not edition_id or not edition_path.is_file():
            continue
        edition = tomllib.loads(edition_path.read_text(encoding="utf-8"))
        work_id = str(edition.get("work_id") or "")
        if work_id:
            editions_by_work[work_id].add(edition_id)
    fully_protected_works = {
        work_id
        for work_id, editions in editions_by_work.items()
        if editions and editions <= fully_protected_editions
    }
    return artifact_ids | fully_protected_editions | fully_protected_works


def ellc_manifests(
    works_root: Path = WORKS_ROOT,
) -> list[tuple[Path, dict]]:
    return [
        (path, record)
        for path, record in artifact_manifests(works_root)
        if record.get("edition_id") == ELLC_EDITION_ID
    ]


def ellc_identities(records: list[tuple[Path, dict]] | None = None) -> set[str]:
    records = ellc_manifests() if records is None else records
    identities = {ELLC_EDITION_ID}
    identities.update(
        str(record.get("id") or "")
        for _, record in records
        if str(record.get("id") or "")
    )
    for path, _ in records:
        edition_path = path.parents[2] / "edition.toml"
        if edition_path.is_file():
            edition = tomllib.loads(edition_path.read_text(encoding="utf-8"))
            work_id = str(edition.get("work_id") or "")
            if work_id:
                identities.add(work_id)
    return identities


def walk_json(value: object, path: str = "$"):
    """Yield every JSON object with a stable address for useful failures."""
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from walk_json(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_json(child, f"{path}[{index}]")


def walk_strings(value: object, path: str = "$"):
    """Yield every string leaf without confusing metadata with object keys."""
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def string_valued_key_paths(value: object, wanted: str) -> set[str]:
    """Addresses where an exact object key carries a string payload."""
    return {
        f"{address}.{wanted}"
        for address, row in walk_json(value)
        if isinstance(row.get(wanted), str)
    }


def rubric_latin_findings(document: object, calendar: str, label: str) -> list[str]:
    """Permit only the two frozen pre-1955 historical Latin statements."""
    allowed = RUBRICS_ALLOWED_LATIN_PATHS[calendar]
    actual = string_valued_key_paths(document, "latin")
    findings = [
        f"{label} {path}: string-valued latin is not authorized"
        for path in sorted(actual - allowed)
    ]
    findings.extend(
        f"{label} {path}: authorized historical latin statement is absent"
        for path in sorted(allowed - actual)
    )
    return findings


def public_rubric_findings(
    document: object,
    calendar: str | None,
    protected_identities: set[str],
    label: str,
) -> list[str]:
    """Public rubrics carry structural rules, not protected witness internals."""
    findings = (
        rubric_latin_findings(document, calendar, label)
        if calendar is not None
        else []
    )
    for identity in identities_in(document, protected_identities):
        findings.append(f"{label}: protected witness identity {identity}")
    for address, row in walk_json(document):
        for key, child in row.items():
            normalized = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", str(key))
            normalized = normalized.casefold().replace("-", "_")
            if normalized in RUBRICS_PRIVATE_PUBLIC_FIELDS:
                findings.append(
                    f"{label} {address}.{key}: protected rubric provenance field"
                )
            elif normalized == "edition" and isinstance(child, (dict, list)):
                findings.append(
                    f"{label} {address}.{key}: structured edition internals are public"
                )
    return findings


def normalized_words(value: str) -> str:
    return unicodedata.normalize("NFC", " ".join(value.split()))


def text_units(value: str, path: Path | None = None) -> list[str]:
    """Physical lines plus decoded JSON string leaves for exact fingerprints."""
    units = list(value.splitlines())
    if path is not None and path.suffix.casefold() == ".json":
        try:
            document = json.loads(value)
        except json.JSONDecodeError:
            return units
        for _, string in walk_strings(document):
            units.append(string)
            units.extend(string.splitlines())
    return units


def unresolved_latin_body_hashes(
    inventory: Path = PROPER_LATIN_INVENTORY,
) -> frozenset[str]:
    """Exact hashes of bodies whose current publication decision is fail-closed."""
    document = tomllib.loads(inventory.read_text(encoding="utf-8"))
    defaults = document.get("defaults") or {}
    hashes = set()
    for row in document.get("entries") or []:
        if not isinstance(row, dict):
            continue
        publication_status = row.get(
            "publication_status", defaults.get("publication_status")
        )
        if row.get("body_status") != "removed" and publication_status not in {
            "unresolved",
            "withheld",
        }:
            continue
        digest = str(row.get("text_sha256") or "")
        if re.fullmatch(r"[0-9a-f]{64}", digest):
            hashes.add(digest)
    return frozenset(hashes)


def protected_text_findings(
    value: str,
    identities: set[str],
    label: str,
    *,
    path: Path | None = None,
    text_fingerprints: frozenset[str] = ELLC_TEXT_SHA256,
    exact_text_fingerprints: frozenset[str] = frozenset(),
) -> list[str]:
    """Find protected identities and exact ELLC lines without retaining words."""
    findings = [
        f"{label}: protected witness identity {identity}"
        for identity in sorted(identities)
        if identity in value
    ]
    seen = set()
    for unit in text_units(value, path):
        exact_digest = hashlib.sha256(unit.encode("utf-8")).hexdigest()
        if exact_digest in exact_text_fingerprints and exact_digest not in seen:
            seen.add(exact_digest)
            findings.append(
                f"{label}: protected unresolved body sha256 {exact_digest}"
            )
        normalized = normalized_words(unit)
        if not normalized:
            continue
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if digest in text_fingerprints and digest not in seen:
            seen.add(digest)
            kind = (
                "sense-line"
                if digest in ELLC_LINE_SHA256
                else "body" if digest in ELLC_BODY_SHA256 else "text"
            )
            findings.append(f"{label}: protected ELLC {kind} sha256 {digest}")
    return findings


def archive_protected_findings(
    path: Path,
    identities: set[str],
    *,
    pdftotext: str | None,
    exact_text_fingerprints: frozenset[str] = frozenset(),
) -> list[str]:
    """Stream nested archive members through the same textual/PDF boundary."""
    findings = []
    maximum_member_size = 100 * 1024 * 1024

    def visit(data: bytes, label: str, member_name: str, depth: int) -> None:
        if depth > 4:
            findings.append(f"{label}: nested archive depth exceeds four")
            return
        stream = io.BytesIO(data)
        if zipfile.is_zipfile(stream):
            stream.seek(0)
            try:
                with zipfile.ZipFile(stream) as archive:
                    for info in archive.infolist():
                        if info.is_dir():
                            continue
                        child_label = f"{label}!{info.filename}"
                        if info.file_size > maximum_member_size:
                            findings.append(
                                f"{child_label}: archive member exceeds scan limit"
                            )
                            continue
                        with archive.open(info) as member:
                            visit(
                                member.read(),
                                child_label,
                                info.filename,
                                depth + 1,
                            )
            except (OSError, RuntimeError, zipfile.BadZipFile) as error:
                findings.append(f"{label}: unreadable archive: {error}")
            return

        binary_identities = [
            identity for identity in sorted(identities) if identity.encode() in data
        ]
        for identity in binary_identities:
            findings.append(f"{label}: protected witness identity {identity}")

        if Path(member_name).suffix.casefold() == ".pdf" and pdftotext:
            run = subprocess.run(
                [pdftotext, "-", "-"],
                input=data,
                capture_output=True,
                check=False,
            )
            if run.returncode:
                findings.append(f"{label}: pdftotext failed for archive member")
                return
            extracted = run.stdout.decode("utf-8", errors="replace")
            findings.extend(
                protected_text_findings(
                    extracted,
                    identities,
                    label,
                    exact_text_fingerprints=exact_text_fingerprints,
                )
            )
            return

        if b"\0" in data:
            return
        try:
            value = data.decode("utf-8")
        except UnicodeDecodeError:
            return
        findings.extend(
            protected_text_findings(
                value,
                identities,
                label,
                path=Path(member_name),
                exact_text_fingerprints=exact_text_fingerprints,
            )
        )
        if Path(member_name).suffix.casefold() == ".json":
            try:
                document = json.loads(value)
            except json.JSONDecodeError as error:
                if "/candidate/browse/structure/" in member_name.replace("\\", "/"):
                    findings.append(f"{label}: invalid candidate JSON: {error}")
            else:
                findings.extend(
                    candidate_browse_structure_findings(
                        document,
                        member_name,
                        identities,
                        label,
                    )
                )

    visit(path.read_bytes(), str(path.relative_to(ROOT)), path.name, 0)
    return findings


def protected_snippet_findings(value: str, label: str) -> list[str]:
    """Sliding token fingerprints for short protected source-note fragments."""
    tokens = re.findall(r"[^\W_]+", unicodedata.normalize("NFC", value).casefold())
    findings = []
    for width, fingerprints in PROTECTED_SNIPPET_FINGERPRINTS.items():
        for offset in range(0, len(tokens) - width + 1):
            digest = hashlib.sha256(
                " ".join(tokens[offset : offset + width]).encode("utf-8")
            ).hexdigest()
            if digest in fingerprints:
                findings.append(
                    f"{label}: protected source-note fragment sha256 {digest}"
                )
    return findings


def identities_in(value: object, identities: set[str]) -> list[str]:
    strings = [text for _, text in walk_strings(value)]
    return sorted(
        identity
        for identity in identities
        if any(identity in text for text in strings)
    )


def assert_no_findings(
    case: unittest.TestCase, findings: list[str], message: str
) -> None:
    """Report a bounded sample; a corpus-scale leak must not flood test logs."""
    if not findings:
        return
    sample = "\n".join(f"  {one}" for one in findings[:20])
    more = len(findings) - min(20, len(findings))
    if more:
        sample += f"\n  ... and {more} more"
    case.fail(f"{message}: {len(findings)} finding(s)\n{sample}")


def restricted_liturgy_row(row: dict) -> bool:
    """Whether a public row describes a witness withheld on rights grounds."""
    reason = row.get("reason")
    kind = reason.get("kind") if isinstance(reason, dict) else reason
    return (
        row.get("rights") in UNSAFE_LITURGY_RIGHTS
        or row.get("rights_status") in UNSAFE_LITURGY_RIGHTS
        or ICEL_MARKER in str(row.get("source_id") or "")
        or row.get("state") == "rights-restricted"
        or kind == "rights-restricted"
    )


def source_artifact_findings(path: Path, record: dict) -> list[str]:
    """Policy findings for one manifest-declared protected source artifact."""
    if record.get("rights_status") in SOURCE_DISTRIBUTABLE_RIGHTS:
        return []
    label = str(path)
    findings = []
    if record.get("storage") not in {"remote", "restricted"}:
        findings.append(
            f"{label}: protected artifact storage is not remote or restricted"
        )
    if str(record.get("path") or "").strip():
        findings.append(f"{label}: protected artifact declares a payload path")
    for sibling in sorted(path.parent.rglob("*") if path.parent.is_dir() else []):
        if sibling.is_file() and sibling != path and sibling.suffix != ".toml":
            findings.append(
                f"{label}: protected artifact retains {sibling.relative_to(path.parent)}"
            )
    return findings


def source_inventory_findings(
    document: object, protected_identities: set[str], label: str
) -> list[str]:
    """Reject protected provenance only when its public source row has words."""
    findings = []
    for address, row in walk_json(document):
        payload = [
            row.get(key)
            for key in ("body", "content", "english", "lines", "text", "translation")
            if row.get(key) not in (None, "", [], {})
        ]
        if not payload:
            continue
        # Rights-policy prose and exact acknowledgements are text-free in the
        # relevant sense: they describe a basis but do not offer a liturgical
        # or source passage.  Actual corpus rows identify their language or a
        # liturgical target.
        if not (
            row.get("lang")
            or row.get("language")
            or set(row) & {"element", "element_key", "mass", "proper"}
        ):
            continue
        if (
            row.get("rights") not in (None, *SOURCE_DISTRIBUTABLE_RIGHTS)
            or row.get("rights_status")
            not in (None, *SOURCE_DISTRIBUTABLE_RIGHTS)
            or identities_in(row, protected_identities)
        ):
            findings.append(f"{label} {address}: protected text is embedded")
    return findings


def restricted_projection_findings(row: dict, label: str) -> list[str]:
    """The public absence is a target and state, never a provenance record."""
    findings = []
    if ".absences[" in label:
        unexpected = sorted(set(row) ^ SAFE_ORDINARY_ABSENCE_FIELDS)
        if unexpected:
            findings.append(
                f"{label}: Ordinary absence does not have exact safe fields; "
                f"difference {', '.join(unexpected)}"
            )
            return findings
        kind = str(row.get("kind") or "")
        expected_state = (
            "rights-restricted" if kind == "rights-withheld" else "unavailable"
        )
        if row.get("state") != expected_state:
            findings.append(
                f"{label}: Ordinary absence state must be {expected_state} for {kind}"
            )
        key = str(row.get("key") or "").casefold()
        if (
            not re.fullmatch(r"[a-z][a-z0-9-]*", key)
            or any(part in key for part in NON_NEUTRAL_ABSENCE_KEY_PARTS)
        ):
            findings.append(f"{label}: Ordinary absence key is not neutral")
        if (
            not isinstance(row.get("count"), int)
            or isinstance(row.get("count"), bool)
            or int(row["count"]) < 0
        ):
            findings.append(f"{label}: Ordinary absence count is not nonnegative")
        if kind not in ORDINARY_ABSENCE_KINDS:
            findings.append(f"{label}: Ordinary absence kind is outside safe taxonomy")
        return findings
    if row.get("state") == "rights-restricted":
        unexpected = sorted(set(row) ^ SAFE_RESTRICTED_PROJECTION_FIELDS)
        if unexpected:
            findings.append(
                f"{label}: restricted state differs from exact safe fields by "
                f"{', '.join(unexpected)}"
            )
        target = row.get("target")
        if isinstance(target, dict):
            difference = sorted(set(target) ^ SAFE_PROPER_TARGET_FIELDS)
            if difference:
                findings.append(
                    f"{label}: restricted target differs from exact safe fields by "
                    f"{', '.join(difference)}"
                )
            if not all(
                isinstance(target.get(key), str) and bool(target[key].strip())
                for key in ("mass", "form_id", "proper", "cycle", "extent")
            ):
                findings.append(f"{label}: restricted target has an empty identity")
            if (
                not isinstance(target.get("occurrence"), int)
                or isinstance(target.get("occurrence"), bool)
                or target["occurrence"] < 1
            ):
                findings.append(f"{label}: restricted target has invalid occurrence")
        elif not isinstance(target, str) or not target.strip():
            findings.append(f"{label}: restricted target is not a safe identity")
        if not isinstance(row.get("lang"), str) or not row["lang"].strip():
            findings.append(f"{label}: restricted language is not a nonempty string")
    if row.get("kind") == "rights-withheld":
        unexpected = sorted(set(row) - {"kind"})
        if unexpected:
            findings.append(
                f"{label}: rights-withheld reason leaks {', '.join(unexpected)}"
            )
    return findings


def common_from_findings(value: object, label: str) -> list[str]:
    """A public Common direction is not its source-study locator."""
    if not isinstance(value, dict):
        return [f"{label}: public common_from is not an object"]
    findings = []
    unexpected = sorted(set(value) ^ SAFE_COMMON_FROM_FIELDS)
    if unexpected:
        findings.append(
            f"{label}: public common_from fields differ by {', '.join(unexpected)}"
        )
    if not isinstance(value.get("scope"), str) or not value["scope"]:
        findings.append(f"{label}: public common_from has no scope")
    options = value.get("options")
    if not isinstance(options, list) or not options:
        findings.append(f"{label}: public common_from has no options")
        return findings
    for index, option in enumerate(options):
        option_label = f"{label}.options[{index}]"
        if not isinstance(option, dict):
            findings.append(f"{option_label}: Common option is not an object")
            continue
        private = sorted(set(option) - SAFE_COMMON_OPTION_FIELDS)
        if private:
            findings.append(
                f"{option_label}: Common option leaks {', '.join(private)}"
            )
        if not isinstance(option.get("mass"), str) or not option["mass"]:
            findings.append(f"{option_label}: Common option has no mass")
    return findings


def latin_capability_findings(value: object, label: str) -> list[str]:
    """A withheld Latin capability is semantic state, never source evidence."""
    if not isinstance(value, dict):
        return [f"{label}: withheld Latin capability is not an object"]
    findings = []
    if value.get("held") is not False:
        findings.append(f"{label}: withheld Latin capability must have held=false")
    for address, row in walk_json(value):
        for key, child in row.items():
            tokens = set(re.split(r"[^a-z0-9]+", str(key).casefold()))
            is_typed_incipit = address == "$.incipit" and key == "text"
            if (
                key in LATIN_CAPABILITY_BODY_FIELDS
                and not is_typed_incipit
                and child not in (
                None,
                "",
                [],
                {},
                )
            ):
                findings.append(f"{label} {address}.{key}: Latin body is exposed")
            if tokens & LATIN_CAPABILITY_AUDIT_FIELD_PARTS:
                findings.append(
                    f"{label} {address}.{key}: Latin audit metadata is exposed"
                )
    return findings


def public_liturgy_findings(
    document: object,
    protected_identities: set[str],
    ellc_ids: set[str],
    label: str,
    source_study_bodies: dict[str, str] | None = None,
    *,
    strict_absences: bool = True,
) -> list[str]:
    """One machine-readable boundary shared by browser, CLI and downloads."""
    findings = []
    for identity in identities_in(document, protected_identities | ellc_ids):
        findings.append(f"{label}: protected witness identity {identity}")
    for address, row in walk_json(document):
        if row.get("common_from") is not None:
            findings.extend(
                common_from_findings(row["common_from"], f"{label} {address}.common_from")
            )
        rights = row.get("rights")
        rights_status = row.get("rights_status")
        if rights is not None and rights not in PUBLIC_LITURGY_RIGHTS:
            findings.append(f"{label} {address}: rights={rights}")
        if rights_status is not None and rights_status not in PUBLIC_LITURGY_RIGHTS:
            findings.append(f"{label} {address}: rights_status={rights_status}")
        if (
            rights is not None
            and rights_status is not None
            and rights != rights_status
        ):
            findings.append(
                f"{label} {address}: rights and rights_status disagree"
            )
        if restricted_liturgy_row(row):
            leaked = sorted(set(row) & RESTRICTED_TRANSLATION_METADATA)
            if leaked:
                findings.append(
                    f"{label} {address}: restricted metadata {', '.join(leaked)}"
                )
        if (
            strict_absences
            or ".absences[" not in address
            or restricted_liturgy_row(row)
        ):
            findings.extend(restricted_projection_findings(row, f"{label} {address}"))
    if source_study_bodies:
        rendered = [normalized_words(text) for _, text in walk_strings(document)]
        for element, body in source_study_bodies.items():
            normalized = normalized_words(body)
            if len(normalized) >= 80 and any(normalized in text for text in rendered):
                findings.append(
                    f"{label}: ELLC source-study body {element} is assembled"
                )
    return findings


def candidate_browse_structure_findings(
    document: object,
    member_name: str,
    protected_identities: set[str],
    label: str,
) -> list[str]:
    """Apply today's public schemas to old, downloadable browser candidates."""
    normalized = member_name.replace("\\", "/")
    match = re.search(
        r"(?:^|/)candidate/browse/structure/(ordinary|propers|rubrics)/([^/]+)\.json$",
        normalized,
    )
    if match is None:
        return []
    layer, filename = match.groups()
    if layer in {"ordinary", "propers"}:
        return public_liturgy_findings(
            document,
            protected_identities,
            set(),
            label,
            strict_absences=layer != "ordinary",
        )

    calendar = filename.removesuffix(".json")
    if calendar == "index":
        calendar_name = None
    elif calendar in RUBRICS_ALLOWED_LATIN_PATHS:
        calendar_name = calendar
    else:
        calendar_name = None
    findings = public_rubric_findings(
        document,
        calendar_name,
        protected_identities,
        label,
    )
    if calendar_name is None and calendar != "index":
        findings.extend(
            f"{label} {path}: unknown-calendar rubric exposes string-valued latin"
            for path in sorted(string_valued_key_paths(document, "latin"))
        )
    return findings


def protected_digests(records: list[tuple[Path, dict]]) -> dict[str, str]:
    return {
        str(record["sha256"]): str(path)
        for path, record in records
        if re.fullmatch(r"[0-9a-f]{64}", str(record.get("sha256") or ""))
    }


def download_findings(
    paths: list[Path], digests: dict[str, str], identities: set[str]
) -> list[str]:
    findings = []
    text_suffixes = {".csv", ".html", ".json", ".tsv", ".txt", ".yaml", ".yml"}
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest in digests:
            findings.append(f"{path}: duplicates protected artifact {digests[digest]}")
        if path.suffix.lower() in text_suffixes:
            decoded = content.decode("utf-8", errors="replace")
            for identity in sorted(identities):
                if identity in decoded:
                    findings.append(f"{path}: exposes protected identity {identity}")
    return findings


def ellc_source_rows(
    records: list[tuple[Path, dict]] | None = None,
) -> tuple[Path, dict, list[dict]] | None:
    """The optional, tracked ELLC source-study transcription and its lines."""
    records = ellc_manifests() if records is None else records
    for manifest, record in records:
        if record.get("artifact_type") != "normalized-text":
            continue
        relative = str(record.get("path") or "")
        if not relative:
            continue
        payload = ROOT / relative
        if not payload.is_file():
            continue
        with payload.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        return manifest, record, rows
    return None


def ellc_source_study_findings(record: dict, rows: list[dict]) -> list[str]:
    """Keep the ELLC exception visibly scholarly, exact and line-aware."""
    findings = []
    notice = str(record.get("acknowledgement") or record.get("rights_basis") or "")
    if not (
        "English Language Liturgical Consultation (ELLC)" in notice
        and "used by permission" in notice
        and "www.englishtexts.org" in notice
    ):
        findings.append("ELLC source-study notice is missing or inexact")
    caution = str(record.get("caution") or record.get("notes") or "").casefold()
    if not (
        "not a liturgical book" in caution
        and ("not approved" in caution or "nothing here may be used for recitation" in caution)
    ):
        findings.append("ELLC source-study payload lacks a non-recitation label")
    by_element: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_element[str(row.get("element_key") or "")].append(row)
    if not by_element or any(not key for key in by_element):
        findings.append("ELLC source-study payload has no typed elements")
    if not any(len(element_rows) > 1 for element_rows in by_element.values()):
        findings.append("ELLC source-study payload flattened every sense line")
    for element, element_rows in by_element.items():
        numbers = [str(row.get("line") or "") for row in element_rows]
        if any(not number.isdigit() for number in numbers):
            findings.append(f"ELLC source-study element {element} has an untyped line")
        if any(not str(row.get("text") or "").strip() for row in element_rows):
            findings.append(f"ELLC source-study element {element} has an empty line")
        numeric = [int(number) for number in numbers if number.isdigit()]
        if numeric != sorted(numeric) or len(numeric) != len(set(numeric)):
            findings.append(f"ELLC source-study element {element} reorders sense lines")
    return findings


def ellc_bodies(rows: list[dict]) -> dict[str, str]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("element_key") or "")].append(str(row.get("text") or ""))
    return {key: "\n".join(lines) for key, lines in grouped.items() if key}


def ellc_output_findings(
    output: str, identities: set[str], bodies: dict[str, str], label: str
) -> list[str]:
    findings = [
        f"{label}: ELLC witness identity {identity}"
        for identity in sorted(identities)
        if identity in output
    ]
    if (
        "English Language Liturgical Consultation" in output
        or "(ELLC)" in output
    ):
        findings.append(f"{label}: ELLC witness metadata is rendered")
    normalized_output = normalized_words(output)
    for element, body in bodies.items():
        normalized = normalized_words(body)
        if len(normalized) >= 80 and normalized in normalized_output:
            findings.append(f"{label}: ELLC source-study body {element} is rendered")
        for line_index, line in enumerate(body.splitlines(), 1):
            normalized_line = normalized_words(line)
            if len(normalized_line) >= 20 and normalized_line in normalized_output:
                findings.append(
                    f"{label}: ELLC source-study sense line "
                    f"{element}/{line_index} is rendered"
                )
    return findings


class TrackedSourceBoundary(unittest.TestCase):
    def test_manifest_protected_sources_track_metadata_not_payloads(self) -> None:
        """Every non-distributable manifest is remote/text-free, including FDLC."""
        protected = protected_artifact_manifests()
        self.assertTrue(protected, "the source library declares no protected artifacts")
        failures = [
            finding
            for path, record in protected
            for finding in source_artifact_findings(path, record)
        ]
        assert_no_findings(
            self,
            failures,
            "a manifest-protected source artifact retains distributable bytes",
        )

    def test_source_inventories_do_not_embed_permission_scoped_text(self) -> None:
        """Text-free provenance may remain; its protected wording may not."""
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected)
        failures: list[str] = []
        for path in sorted(SOURCE_INVENTORIES.glob("*.toml")):
            document = tomllib.loads(path.read_text(encoding="utf-8"))
            failures.extend(
                source_inventory_findings(
                    document, identities, str(path.relative_to(ROOT))
                )
            )
        assert_no_findings(
            self,
            failures,
            "a source overlay cannot retain words barred from public Git",
        )

    def test_fdlc_container_metadata_is_fail_closed_and_text_free(self) -> None:
        """FDLC container records neither clear the PDFs nor quote the orations."""
        source_paths = [FDLC_WORK_ROOT / "work.toml"]
        source_paths.extend(sorted(FDLC_WORK_ROOT.glob("editions/*/edition.toml")))
        source_paths.extend(
            sorted(FDLC_WORK_ROOT.glob("editions/*/artifacts/*/artifact.toml"))
        )
        projection_paths = sorted(FDLC_PUBLIC_EDITIONS.glob("*.json"))
        self.assertEqual(len(source_paths), 11, "FDLC source graph is incomplete")
        self.assertEqual(
            len(projection_paths), 2, "FDLC public edition projection is incomplete"
        )

        failures: list[str] = []
        for path in source_paths + projection_paths:
            value = decoded_text(path)
            self.assertIsNotNone(value, f"{path}: FDLC metadata is not UTF-8 text")
            assert value is not None
            label = str(path.relative_to(ROOT))
            failures.extend(protected_snippet_findings(value, label))
            if re.search(r"\(c\)\s*2010\b", value, re.IGNORECASE):
                failures.append(f"{label}: substitutes (c) for the copyright symbol")
            if re.search(r"\b(?:standing|permission)\b", value, re.IGNORECASE):
                failures.append(
                    f"{label}: FDLC container metadata reasons from a permission claim"
                )
            if "passed through a model" in value.casefold():
                failures.append(f"{label}: asserts an unprovable model-handling fact")

        for path in sorted(FDLC_WORK_ROOT.glob("editions/*/edition.toml")):
            edition = tomllib.loads(path.read_text(encoding="utf-8"))
            label = str(path.relative_to(ROOT))
            if edition.get("translators"):
                failures.append(
                    f"{label}: attributes the composite reflection edition to a translator"
                )
            authority = str(edition.get("authority") or "")
            if not all(
                marker in authority
                for marker in (
                    "Federation of Diocesan Liturgical Commissions",
                    "embedded excerpts",
                    "translation rightsholder",
                )
            ):
                failures.append(f"{label}: does not distinguish container and text layers")

        assert_no_findings(
            self,
            failures,
            "FDLC source metadata is not a fail-closed, text-free container record",
        )

    def test_fdlc_artifact_types_layers_and_projection_match(self) -> None:
        """Rehosted 2012 and publisher-issued 2016 PDFs remain distinct."""
        manifests = [
            (path, tomllib.loads(path.read_text(encoding="utf-8")))
            for path in sorted(
                FDLC_WORK_ROOT.glob("editions/*/artifacts/*/artifact.toml")
            )
        ]
        self.assertEqual(len(manifests), 8, "expected all eight FDLC artifacts")
        by_edition: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
        failures: list[str] = []
        for path, record in manifests:
            label = str(path.relative_to(ROOT))
            edition_id = str(record.get("edition_id") or "")
            by_edition[edition_id].append((path, record))
            for key, expected in (
                ("storage", "remote"),
                ("rights_status", "unresolved"),
                ("media_type", "application/pdf"),
                ("indexable", False),
            ):
                if record.get(key) != expected:
                    failures.append(f"{label}: {key} is not {expected!r}")
            if record.get("path"):
                failures.append(f"{label}: unresolved FDLC PDF declares a payload path")
            provenance = str(record.get("provenance") or "")
            if not all(
                marker in provenance
                for marker in ("rendered page images", "text layer", "only as a locator")
            ):
                failures.append(f"{label}: visual-check provenance is incomplete")

            rights_basis = re.sub(
                r"\s+", " ", str(record.get("rights_basis") or "")
            ).strip()
            if "2012-2013-collects" in edition_id:
                if record.get("artifact_type") != "rehosted-pdf":
                    failures.append(f"{label}: Evansville mirror is not rehosted-pdf")
                if "www.evdio.org" not in str(record.get("source_url") or ""):
                    failures.append(f"{label}: 2012 artifact is not tied to its mirror")
                required_layers = (
                    "FDLC compilation",
                    "contributor-authored",
                    "artwork or images",
                    "ICEL",
                    "composite PDF",
                    "rehosted-byte provenance",
                )
            else:
                if record.get("artifact_type") != "publisher-issued-pdf":
                    failures.append(f"{label}: official FDLC artifact type drifted")
                if "fdlc.org" not in str(record.get("source_url") or ""):
                    failures.append(f"{label}: 2016 artifact is not tied to FDLC")
                required_layers = (
                    "FDLC compilation",
                    "contributor-authored",
                    "Archdiocese of Chicago",
                    "ICEL",
                    "composite PDF",
                )
                if any(token in str(record.get("id") or "") for token in ("78c", "78d")):
                    required_layers += ("Paul Turner", "World Library Publications")
            for marker in required_layers:
                if marker not in rights_basis:
                    failures.append(f"{label}: rights basis omits {marker!r}")

        self.assertEqual(
            sorted(len(records) for records in by_edition.values()),
            [4, 4],
            "FDLC artifact grouping is not four per edition",
        )
        projected_by_edition = {}
        for path in sorted(FDLC_PUBLIC_EDITIONS.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            projected_by_edition[document["edition"]["id"]] = (path, document)
        for edition_id, records in by_edition.items():
            if edition_id not in projected_by_edition:
                failures.append(f"{edition_id}: public source projection is absent")
                continue
            projection_path, document = projected_by_edition[edition_id]
            projected = {
                row.get("id"): row for row in document.get("artifacts") or []
            }
            expected_ids = {record.get("id") for _, record in records}
            if set(projected) != expected_ids:
                failures.append(
                    f"{projection_path.relative_to(ROOT)}: projected artifact ids drift"
                )
                continue
            for _, record in records:
                row = projected[record["id"]]
                for source_key, public_key in (
                    ("artifact_type", "artifact_type"),
                    ("media_type", "media_type"),
                    ("storage", "storage"),
                    ("rights_status", "rights"),
                    ("rights_jurisdiction", "rights_jurisdiction"),
                    ("source_url", "source_url"),
                    ("retrieved", "retrieved"),
                    ("byte_size", "byte_size"),
                    ("page_count", "page_count"),
                ):
                    if row.get(public_key) != record.get(source_key):
                        failures.append(
                            f"{projection_path.relative_to(ROOT)}: {record['id']} "
                            f"{public_key} does not match its manifest"
                        )

        assert_no_findings(
            self,
            failures,
            "FDLC artifact provenance or public projection drifted",
        )

    def test_fdlc_inventory_uses_date_inference_and_hash_only_rows(self) -> None:
        """The inventory preserves provenance without overstating the witness."""
        document = tomllib.loads(FDLC_INVENTORY.read_text(encoding="utf-8"))
        sources = {
            row.get("id"): row
            for row in document.get("sources") or []
            if str(row.get("id") or "").startswith("fdlc-mystagogy-")
        }
        self.assertEqual(set(sources), {"fdlc-mystagogy-2012", "fdlc-mystagogy-2016"})
        failures: list[str] = []
        for source_id, row in sources.items():
            basis = str(row.get("attests_basis") or "")
            if row.get("attests_kind") != "date-bound":
                failures.append(f"{source_id}: attestation is not date-bound")
            for marker in ("repeated page acknowledgment", "© 2010", "date inference"):
                if marker not in basis:
                    failures.append(f"{source_id}: attestation omits {marker!r}")
            if "(c) 2010" in basis:
                failures.append(f"{source_id}: historical notice uses ASCII (c)")

        held = [
            row
            for row in document.get("untranslated") or []
            if str(row.get("witness") or "").startswith("fdlc-mystagogy-")
        ]
        self.assertEqual(len(held), 40, "FDLC hash-only quarantine count drifted")
        for index, row in enumerate(held):
            if row.get("availability") != "unavailable":
                failures.append(f"FDLC held row {index}: availability is not unavailable")
            reason = row.get("reason") or {}
            if reason.get("kind") != "rights-withheld":
                failures.append(f"FDLC held row {index}: reason is not rights-withheld")
            if row.get("text"):
                failures.append(f"FDLC held row {index}: retains liturgical wording")
            digests = row.get("quarantined_text_sha256") or []
            if not (
                isinstance(digests, list)
                and len(digests) == 1
                and re.fullmatch(r"[0-9a-f]{64}", str(digests[0]))
            ):
                failures.append(f"FDLC held row {index}: quarantine hash is invalid")

        assert_no_findings(
            self,
            failures,
            "FDLC inventory provenance or text quarantine drifted",
        )

    def test_current_sources_have_no_protected_collect_fragments_or_stale_claims(
        self,
    ) -> None:
        """Removed ICEL snippets and former publication claims stay removed."""
        contradiction = re.compile(
            r"\b(?:publishable|may be published)\b.{0,500}?"
            r"\b(?:not|nothing)\s+(?:is\s+)?landed\b",
            re.IGNORECASE | re.DOTALL,
        )
        failures = []
        for path in tracked_files(
            "src/sources/calendars/postconciliar/propers.yaml"
        ):
            value = decoded_text(path)
            if value is None:
                continue
            label = str(path.relative_to(ROOT))
            failures.extend(protected_snippet_findings(value, label))
            for match in contradiction.finditer(value):
                line = value.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{label}:{line}: obsolete publishable-but-not-landed claim"
                )
        assert_no_findings(
            self,
            failures,
            "current source retains protected wording or obsolete publication prose",
        )

    def test_calendar_rubric_sources_keep_only_authorized_historical_latin(
        self,
    ) -> None:
        """Modern/1962 bodies are quarantined; two pre-1955 statements remain."""
        failures = []
        for calendar in RUBRICS_ALLOWED_LATIN_PATHS:
            path = RUBRICS_SOURCE_ROOT / calendar / "rubrics.yaml"
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            failures.extend(
                rubric_latin_findings(
                    document, calendar, str(path.relative_to(ROOT))
                )
            )
        assert_no_findings(
            self,
            failures,
            "a calendar-rubrics source retains unauthorized Latin wording",
        )


class PublicDataBoundary(unittest.TestCase):
    def test_tracked_agent_handoffs_have_no_protected_text_payload(self) -> None:
        """Review bundles are tracked downloads, not a bypass around source policy."""
        paths = tracked_files("build/agent-handoffs")
        self.assertTrue(paths, "no tracked agent-handoff evidence was found")
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected) | ellc_identities()
        unresolved_body_hashes = unresolved_latin_body_hashes()
        self.assertTrue(
            unresolved_body_hashes,
            "the Roman publication inventory yielded no fail-closed body hashes",
        )
        failures = []
        textual = 0
        archives = 0
        pdftotext = shutil.which("pdftotext")
        for path in paths:
            if path.suffix.casefold() == ".zip":
                archives += 1
                failures.extend(
                    archive_protected_findings(
                        path,
                        identities,
                        pdftotext=pdftotext,
                        exact_text_fingerprints=unresolved_body_hashes,
                    )
                )
                continue
            value = decoded_text(path)
            if value is None:
                continue
            textual += 1
            failures.extend(
                protected_text_findings(
                    value,
                    identities,
                    str(path.relative_to(ROOT)),
                    path=path,
                    exact_text_fingerprints=unresolved_body_hashes,
                )
            )
            relative = str(path.relative_to(ROOT))
            if path.suffix.casefold() == ".json":
                try:
                    document = json.loads(value)
                except json.JSONDecodeError as error:
                    if "/candidate/browse/structure/" in f"/{relative}":
                        failures.append(f"{relative}: invalid candidate JSON: {error}")
                else:
                    failures.extend(
                        candidate_browse_structure_findings(
                            document,
                            relative,
                            identities,
                            relative,
                        )
                    )
        self.assertGreater(textual, 0, "the tracked handoff corpus had no UTF-8 text")
        self.assertGreater(archives, 0, "the tracked handoff corpus had no archives")
        assert_no_findings(
            self,
            failures,
            "a tracked agent handoff retains a protected textual payload",
        )

    def test_source_browser_has_no_protected_text_projection(self) -> None:
        """The Sources reader is another browser/download surface."""
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected)
        failures: list[str] = []
        for path in sorted(PUBLIC_SOURCE_TEXT.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            failures.extend(
                source_inventory_findings(
                    document, identities, str(path.relative_to(ROOT))
                )
            )
        assert_no_findings(
            self,
            failures,
            "the Sources browser projects protected text",
        )

    def test_calendar_rubrics_fresh_and_tracked_are_rights_sanitized(self) -> None:
        """The browser/download rubric corpus is text- and provenance-free."""
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected)
        failures: list[str] = []
        with tempfile.TemporaryDirectory(
            prefix="rubrics-rights-", dir=scratch
        ) as temporary:
            fresh_root = Path(temporary)
            run = subprocess.run(
                [
                    str(TPT),
                    "calendar-rubrics",
                    "structure",
                    "--out",
                    str(fresh_root),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                run.returncode,
                0,
                f"fresh calendar-rubrics structure refused:\n{run.stdout}{run.stderr}",
            )
            fresh_public = fresh_root / "structure" / "rubrics"
            for surface, root in (
                ("fresh", fresh_public),
                ("tracked", RUBRICS_PUBLIC_ROOT),
            ):
                for calendar in RUBRICS_ALLOWED_LATIN_PATHS:
                    path = root / f"{calendar}.json"
                    document = json.loads(path.read_text(encoding="utf-8"))
                    failures.extend(
                        public_rubric_findings(
                            document,
                            calendar,
                            identities,
                            f"{surface} {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path.name}",
                        )
                    )
                index = root / "index.json"
                document = json.loads(index.read_text(encoding="utf-8"))
                failures.extend(
                    public_rubric_findings(
                        document,
                        None,
                        identities,
                        f"{surface} rubrics/index.json",
                    )
                )
        assert_no_findings(
            self,
            failures,
            "public calendar rubrics retain protected wording or provenance",
        )

    def test_browser_and_download_json_carry_no_permission_or_icel_witness(self) -> None:
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected)
        ellc = ellc_identities()
        source = ellc_source_rows()
        bodies = ellc_bodies(source[2]) if source else {}
        failures: list[str] = []
        files = sorted(
            path
            for root in PUBLIC_LITURGY_ROOTS
            for path in root.glob("*.json")
            if path.is_file()
        )
        self.assertTrue(files, "no generated Ordinary/Propers data was found")
        for path in files:
            document = json.loads(path.read_text(encoding="utf-8"))
            failures.extend(
                public_liturgy_findings(
                    document,
                    identities,
                    ellc,
                    str(path.relative_to(ROOT)),
                    bodies,
                )
            )
        assert_no_findings(
            self,
            failures,
            "browser data is itself a public, downloadable corpus",
        )

    def test_ellc_source_study_exception_keeps_notice_and_sense_lines(self) -> None:
        """ELLC may remain as labeled study material, never as a Missal offer."""
        source = ellc_source_rows()
        if source is None:
            leaked = []
            identities = ellc_identities()
            for path in sorted(PUBLIC_SOURCE_TEXT.glob("*.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                if identities_in(document, identities):
                    leaked.append(str(path.relative_to(ROOT)))
            self.assertEqual(
                leaked,
                [],
                "a source-study text projection survives without its ELLC payload",
            )
            return
        _, record, rows = source
        assert_no_findings(
            self,
            ellc_source_study_findings(record, rows),
            "the ELLC source-study exception lost a licence condition",
        )
        projections = []
        for path in (STRUCTURE_ROOT / "sources" / "editions").glob("**/*.json"):
            document = json.loads(path.read_text(encoding="utf-8"))
            edition = document.get("edition") or {}
            if edition.get("id") == ELLC_EDITION_ID:
                projections.append((path, document))
        self.assertEqual(len(projections), 1, "ELLC source-study edition projection drifted")
        path, document = projections[0]
        artifacts = {
            artifact.get("id"): artifact
            for artifact in document.get("artifacts") or []
            if isinstance(artifact, dict)
        }
        projected = artifacts.get(record.get("id"))
        self.assertIsNotNone(projected, f"{path}: ELLC source-study artifact is absent")
        assert isinstance(projected, dict)
        self.assertEqual(
            projected.get("rights_basis"),
            record.get("rights_basis"),
            "the source-study view altered the required notice",
        )
        self.assertEqual(
            projected.get("notes"),
            record.get("notes"),
            "the source-study view lost its non-recitation label",
        )

    def test_registered_protected_artifacts_are_not_public_downloads(self) -> None:
        """No exact protected artifact or private identity reaches a download."""
        protected = protected_artifact_manifests()
        ellc = ellc_manifests()
        identities = protected_artifact_identities(protected) | ellc_identities(ellc)
        paths = files_under(*DOWNLOAD_ROOTS)
        assert_no_findings(
            self,
            download_findings(
                paths, protected_digests([*protected, *ellc]), identities
            ),
            "a protected artifact reached a download",
        )


class CliBoundary(unittest.TestCase):
    MARKER = "PROJECT-CREATED-RESTRICTED-CLI-PROBE"
    UNRESOLVED_MARKER = "PROJECT-CREATED-UNRESOLVED-CLI-PROBE"
    SOURCE_ID = f"edition.{ICEL_MARKER}.synthetic-rights-probe"
    UNRESOLVED_SOURCE_ID = "edition.synthetic.unresolved-rights-probe"
    ARTIFACT_ID = "artifact.synthetic.private-cli-probe"
    QUARANTINE_HASH = "f" * 64

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(TPT), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_withheld_latin_capabilities(
        self,
        payload: object,
        targets: set[str],
        label: str,
        *,
        require_language_selection: bool,
    ) -> None:
        matches: dict[str, list[tuple[str, dict, object]]] = defaultdict(list)
        for address, row in walk_json(payload):
            latin = row.get("latin")
            if not isinstance(latin, dict) or latin.get("held") is not False:
                continue
            target = str(latin.get("target") or row.get("name") or "")
            if target in targets:
                matches[target].append(
                    (address, latin, row.get("language_selection"))
                )
        self.assertEqual(
            targets,
            set(matches),
            f"{label}: expected withheld Latin targets were not projected",
        )
        findings = []
        for target, rows in matches.items():
            for address, latin, selection in rows:
                findings.extend(
                    latin_capability_findings(
                        latin, f"{label} {address}.latin ({target})"
                    )
                )
                if require_language_selection:
                    findings.extend(
                        latin_capability_findings(
                            selection,
                            f"{label} {address}.language_selection ({target})",
                        )
                    )
        assert_no_findings(
            self,
            findings,
            f"{label} exposes withheld Latin wording or audit evidence",
        )

    def test_mass_propers_cli_redacts_restricted_words_in_every_format(self) -> None:
        """The maintenance CLI is an export surface, not a rights bypass."""
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="triptych-rights-", dir=scratch
        ) as temporary:
            workspace = Path(temporary)
            calendar_root = workspace / "calendars"
            calendar = calendar_root / "demo"
            calendar.mkdir(parents=True)
            (calendar / "propers.yaml").write_text(
                textwrap.dedent(
                    f"""\
                    schema: triptych-calendar-masses/v1
                    calendar: demo
                    edition: Synthetic rights fixture
                    psalm_numbering: vulgate
                    sections:
                      '01':
                        kind: seasonal
                        masses:
                        - key: rights-probe
                          name: Rights probe
                          propers:
                          - name: Collect
                            source: composed
                            text: Excita testum.
                            translations:
                            - lang: en
                              rights: permission
                              source_id: {self.SOURCE_ID}
                              text: {self.MARKER}
                            - lang: en
                              rights: unresolved
                              source_id: {self.UNRESOLVED_SOURCE_ID}
                              text: {self.UNRESOLVED_MARKER}
                    """
                ),
                encoding="utf-8",
            )
            inventories = workspace / "inventories"
            inventories.mkdir()
            (inventories / "demo-proper-translations-v1.toml").write_text(
                textwrap.dedent(
                    f"""\
                    schema = "triptych-proper-translations/v1"
                    calendar = "demo"

                    [[untranslated]]
                    mass = "rights-probe"
                    form_id = "main"
                    proper = "Collect"
                    cycle = "all"
                    occurrence = 1
                    lang = "en"
                    extent = "body"
                    availability = "unavailable"
                    reason = {{ kind = "rights-withheld" }}
                    note = "Synthetic rights-withheld regression fixture."
                    source_id = "{self.SOURCE_ID}"
                    artifact_id = "{self.ARTIFACT_ID}"
                    verified_printed_page = 7
                    quarantined_text_sha256 = ["{self.QUARANTINE_HASH}"]
                    """
                ),
                encoding="utf-8",
            )

            outputs = {}
            for output_format in ("text", "yaml", "json"):
                run = self.run_tool(
                    "mass-propers",
                    "show",
                    "--root",
                    str(calendar_root),
                    "--calendar",
                    "demo",
                    "--mass",
                    "rights-probe",
                    "--lang",
                    "en",
                    "--format",
                    output_format,
                )
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                self.assertNotIn(self.MARKER, run.stdout, output_format)
                self.assertNotIn(self.UNRESOLVED_MARKER, run.stdout, output_format)
                self.assertNotIn(self.SOURCE_ID, run.stdout, output_format)
                self.assertNotIn(self.UNRESOLVED_SOURCE_ID, run.stdout, output_format)
                self.assertNotIn(self.ARTIFACT_ID, run.stdout, output_format)
                self.assertNotIn(self.QUARANTINE_HASH, run.stdout, output_format)
                self.assertNotIn("rights: permission", run.stdout, output_format)
                self.assertNotIn("rights: unresolved", run.stdout, output_format)
                outputs[output_format] = run.stdout

        self.assertIn("rights restricted", outputs["text"].lower())
        for output_format in ("yaml", "json"):
            self.assertIn("rights-restricted", outputs[output_format])
        machine = json.loads(outputs["json"])
        restricted = [
            row
            for _, row in walk_json(machine)
            if row.get("state") == "rights-restricted"
        ]
        self.assertTrue(restricted, "the CLI lost the typed restricted state")
        failures = [
            finding
            for index, row in enumerate(restricted)
            for finding in restricted_projection_findings(
                row, f"mass-propers JSON restricted row {index}"
            )
        ]
        assert_no_findings(
            self,
            failures,
            "mass-propers exposes source audit internals through its CLI",
        )

    def test_mass_today_machine_surface_contains_no_protected_witness(self) -> None:
        """The composed day payload must preserve the same fail-closed boundary."""
        run = self.run_tool(
            "mass-today",
            "show",
            "--date",
            "2027-03-21",
            "--calendar",
            "postconciliar",
            "--ordinary",
            "--format",
            "json",
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        payload = json.loads(run.stdout)
        protected = protected_artifact_manifests()
        source = ellc_source_rows()
        findings = public_liturgy_findings(
            payload,
            protected_artifact_identities(protected),
            ellc_identities(),
            "mass-today JSON",
            ellc_bodies(source[2]) if source else {},
        )
        assert_no_findings(
            self,
            findings,
            "mass-today reintroduced a protected witness",
        )

    def test_latin_unresolved_witnesses_are_text_free_public_capabilities(self) -> None:
        """Known Latin gaps remain typed absences on both composed JSON surfaces."""
        cases = (
            (
                "mass-propers St Albert",
                (
                    "mass-propers",
                    "show",
                    "--calendar",
                    "roman-1962",
                    "--mass",
                    "s-alberti-magni-episcopi-confessoris-ecclesiae",
                    "--lang",
                    "la",
                    "--format",
                    "json",
                ),
                {"Collect", "Secret", "Postcommunion"},
                False,
            ),
            (
                "mass-today St Albert",
                (
                    "mass-today",
                    "show",
                    "--date",
                    "2027-11-15",
                    "--calendar",
                    "roman-1962",
                    "--lang",
                    "la",
                    "--format",
                    "json",
                ),
                {"Collect", "Secret", "Postcommunion"},
                True,
            ),
            (
                "mass-propers Pustet Common",
                (
                    "mass-propers",
                    "show",
                    "--calendar",
                    "roman-1962",
                    "--mass",
                    "commune-dedicationis-ecclesiae",
                    "--lang",
                    "la",
                    "--format",
                    "json",
                ),
                {"Gradual", "Alleluia (Tempore paschali)"},
                False,
            ),
            (
                "mass-today Pustet Common",
                (
                    "mass-today",
                    "show",
                    "--date",
                    "2027-11-18",
                    "--calendar",
                    "roman-1962",
                    "--lang",
                    "la",
                    "--format",
                    "json",
                ),
                {"Gradual", "Alleluia (Tempore paschali)"},
                True,
            ),
        )
        for label, arguments, targets, requires_selection in cases:
            with self.subTest(surface=label):
                run = self.run_tool(*arguments)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                self.assert_withheld_latin_capabilities(
                    json.loads(run.stdout),
                    targets,
                    label,
                    require_language_selection=requires_selection,
                )

    def test_mass_ordinary_machine_surface_contains_only_public_states(self) -> None:
        run = self.run_tool(
            "mass-ordinary",
            "show",
            "--calendar",
            "postconciliar",
            "--format",
            "json",
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        protected = protected_artifact_manifests()
        findings = public_liturgy_findings(
            json.loads(run.stdout),
            protected_artifact_identities(protected),
            ellc_identities(),
            "mass-ordinary JSON",
        )
        assert_no_findings(
            self,
            findings,
            "mass-ordinary exposes a private witness or rich absence",
        )

    def test_common_direction_cli_exposes_no_source_locator(self) -> None:
        """Fatima keeps its Common choice without exporting its audit trail."""
        invocations = (
            (
                "mass-propers",
                "show",
                "--calendar",
                "postconciliar",
                "--mass",
                "our-lady-fatima",
            ),
            (
                "mass-today",
                "show",
                "--date",
                "2027-05-13",
                "--calendar",
                "postconciliar",
                "--mass",
                "our-lady-fatima",
            ),
        )
        for invocation in invocations:
            with self.subTest(tool=invocation[0]):
                run = self.run_tool(*invocation, "--format", "json")
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                payload = json.loads(run.stdout)
                commons = [
                    row["common_from"]
                    for _, row in walk_json(payload)
                    if row.get("common_from") is not None
                ]
                self.assertTrue(commons, f"{invocation[0]} lost Fatima's Common")
                failures = [
                    finding
                    for index, common in enumerate(commons)
                    for finding in common_from_findings(
                        common, f"{invocation[0]} common_from {index}"
                    )
                ]
                assert_no_findings(
                    self,
                    failures,
                    f"{invocation[0]} exported Common source provenance",
                )


class EllcAssemblyBoundary(unittest.TestCase):
    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(TPT), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def source_material(self) -> tuple[set[str], dict[str, str]]:
        source = ellc_source_rows()
        return ellc_identities(), ellc_bodies(source[2]) if source else {}

    def test_ordinary_and_day_cli_withhold_ellc_in_text_and_json(self) -> None:
        """A licensed study witness is not a Roman Missal participation offer."""
        identities, bodies = self.source_material()
        invocations = (
            (
                "mass-ordinary",
                "show",
                "--calendar",
                "postconciliar",
            ),
            (
                "mass-today",
                "show",
                "--date",
                "2027-03-21",
                "--calendar",
                "postconciliar",
                "--ordinary",
            ),
        )
        failures: list[str] = []
        for invocation in invocations:
            label = " ".join(invocation[:2])
            for output_format in ("text", "json"):
                run = self.run_tool(*invocation, "--format", output_format)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                failures.extend(
                    ellc_output_findings(
                        run.stdout, identities, bodies, f"{label} {output_format}"
                    )
                )
        assert_no_findings(
            self,
            failures,
            "ELLC source-study material reached an assembled CLI surface",
        )

    def test_tracked_participation_pdfs_withhold_protected_text(self) -> None:
        """Tracked print evidence and liturgy PDFs obey the same text boundary."""
        pdfs = []
        for path in tracked_files("build/agent-handoffs", "pdf"):
            relative = path.relative_to(ROOT)
            parts = set(relative.parts)
            is_handoff_print = (
                relative.parts[0] == "build"
                and relative.suffix.casefold() == ".pdf"
            )
            is_postconciliar_participation = (
                relative.parts[0] == "pdf"
                and "postconciliar" in parts
                and bool(parts & {"ordinary", "propers"})
                and relative.suffix.casefold() == ".pdf"
            )
            if is_handoff_print or is_postconciliar_participation:
                pdfs.append(path)
        if not pdfs:
            return
        executable = shutil.which("pdftotext")
        self.assertIsNotNone(executable, "pdftotext is required for the PDF rights gate")
        protected = protected_artifact_manifests()
        identities = protected_artifact_identities(protected) | ellc_identities()
        failures: list[str] = []
        for path in pdfs:
            run = subprocess.run(
                [str(executable), str(path), "-"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            failures.extend(
                protected_text_findings(
                    run.stdout,
                    identities,
                    str(path.relative_to(ROOT)),
                )
            )
        assert_no_findings(
            self,
            failures,
            "protected source material reached a tracked participation PDF",
        )


class RightsMutationBoundary(unittest.TestCase):
    """Synthetic leaks prove the gates fail, not merely that today's tree passes."""

    def scratch_directory(self):
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        return tempfile.TemporaryDirectory(prefix="rights-mutation-", dir=scratch)

    def test_extracted_text_mutation_detects_identity_and_line_fingerprint(
        self,
    ) -> None:
        identity = "artifact.synthetic.protected-extracted-text"
        identity_failures = protected_text_findings(
            f"metadata names {identity}", {identity}, "synthetic extracted PDF"
        )
        self.assertTrue(
            any("protected witness identity" in one for one in identity_failures),
            identity_failures,
        )
        marker = "PROJECT-CREATED PROTECTED LINE FINGERPRINT MUTATION"
        digest = hashlib.sha256(normalized_words(marker).encode("utf-8")).hexdigest()
        fingerprint_failures = protected_text_findings(
            marker,
            set(),
            "synthetic extracted PDF",
            text_fingerprints=frozenset({digest}),
        )
        self.assertTrue(
            any("protected ELLC text sha256" in one for one in fingerprint_failures),
            fingerprint_failures,
        )
        exact_marker = "PROJECT-CREATED  exact unresolved-body mutation\nline two"
        exact_digest = hashlib.sha256(exact_marker.encode("utf-8")).hexdigest()
        exact_failures = protected_text_findings(
            json.dumps({"latin": exact_marker}),
            set(),
            "synthetic unresolved body JSON",
            path=Path("candidate/browse/structure/propers/roman-1962.json"),
            exact_text_fingerprints=frozenset({exact_digest}),
        )
        self.assertTrue(
            any("protected unresolved body sha256" in one for one in exact_failures),
            exact_failures,
        )

    def test_latin_capability_mutation_rejects_body_and_audit_evidence(self) -> None:
        safe = {
            "requested": "la",
            "status": "withheld",
            "held": False,
            "available": False,
            "complete": False,
            "reason": {"lang": "la", "state": "latin-withheld"},
        }
        self.assertEqual(latin_capability_findings(safe, "synthetic Latin state"), [])
        for field, value in (
            ("text", "PROJECT-CREATED-LATIN-BODY-MUTATION"),
            ("source_id", "edition.synthetic.private-latin"),
            ("artifact_id", "artifact.synthetic.private-latin"),
            ("page", 7),
            ("evidence_sha256", "b" * 64),
        ):
            mutated = dict(safe)
            mutated[field] = value
            findings = latin_capability_findings(
                mutated, f"synthetic Latin {field} mutation"
            )
            self.assertTrue(findings, f"{field} crossed the Latin capability boundary")

    def test_calendar_rubric_mutations_reject_latin_and_provenance(self) -> None:
        identity = "artifact.synthetic.protected-rubric-witness"
        safe = {
            "calendar": "roman-pre-1955",
            "edition": "Synthetic historical rubric fixture",
            "precedence": {
                "latin": "PROJECT-CREATED AUTHORIZED PATH FIXTURE",
                "locus": "Synthetic neutral locus",
                "gloss": "Synthetic neutral gloss",
            },
            "saturday_office": {
                "latin": "PROJECT-CREATED AUTHORIZED PATH FIXTURE",
                "rule": "Synthetic neutral structural rule",
            },
        }
        baselines = {
            "postconciliar": {
                "calendar": "postconciliar",
                "edition": "Synthetic modern rubric fixture",
            },
            "roman-1962": {
                "calendar": "roman-1962",
                "edition": "Synthetic 1962 rubric fixture",
            },
            "roman-pre-1955": safe,
        }
        for calendar, baseline in baselines.items():
            with self.subTest(calendar=calendar, mutation="baseline"):
                self.assertEqual(
                    public_rubric_findings(
                        baseline,
                        calendar,
                        {identity},
                        f"synthetic safe {calendar} rubrics",
                    ),
                    [],
                )
            with self.subTest(calendar=calendar, mutation="latin"):
                extra_latin = json.loads(json.dumps(baseline))
                extra_latin["synthetic_exception"] = {
                    "latin": "PROJECT-CREATED UNAUTHORIZED LATIN PATH MUTATION"
                }
                latin_failures = public_rubric_findings(
                    extra_latin,
                    calendar,
                    {identity},
                    f"synthetic {calendar} Latin rubric mutation",
                )
                self.assertTrue(
                    any(
                        "string-valued latin is not authorized" in one
                        for one in latin_failures
                    ),
                    latin_failures,
                )

        for field, value in (
            ("derived_from", {"publication": "synthetic"}),
            ("artifact_id", identity),
            ("edition_id", "edition.synthetic.protected-rubric-witness"),
            ("source_id", "source.synthetic.protected-rubric-witness"),
            ("witnesses", [{"id": identity}]),
            ("edition", {"id": "edition.synthetic.protected-rubric-witness"}),
        ):
            mutated = json.loads(json.dumps(safe))
            mutated[field] = value
            findings = public_rubric_findings(
                mutated,
                "roman-pre-1955",
                {identity},
                f"synthetic rubric {field} mutation",
            )
            self.assertTrue(
                any(
                    "protected rubric provenance field" in one
                    or "structured edition internals" in one
                    for one in findings
                ),
                f"{field}: {findings}",
            )

        identity_only = json.loads(json.dumps(safe))
        identity_only["precedence"]["gloss"] = identity
        identity_failures = public_rubric_findings(
            identity_only,
            "roman-pre-1955",
            {identity},
            "synthetic protected rubric identity mutation",
        )
        self.assertTrue(
            any("protected witness identity" in one for one in identity_failures),
            identity_failures,
        )

    def test_manifest_discovery_catches_new_source_and_download_payloads(self) -> None:
        with self.scratch_directory() as temporary:
            base = Path(temporary)
            artifact = (
                base
                / "works"
                / "new-rightsholder"
                / "new-work"
                / "editions"
                / "new-edition"
                / "artifacts"
                / "new-artifact"
            )
            artifact.mkdir(parents=True)
            payload = b"PROJECT-CREATED-PROTECTED-DOWNLOAD-MUTATION"
            digest = hashlib.sha256(payload).hexdigest()
            payload_path = artifact / "payload.pdf"
            payload_path.write_bytes(payload)
            (artifact.parents[1] / "edition.toml").write_text(
                textwrap.dedent(
                    """\
                    schema = 1
                    record_type = "edition"
                    id = "edition.synthetic.new-protected-work"
                    work_id = "work.synthetic.new-protected-work"
                    """
                ),
                encoding="utf-8",
            )
            manifest_path = artifact / "artifact.toml"
            manifest_path.write_text(
                textwrap.dedent(
                    f"""\
                    schema = 2
                    record_type = "artifact"
                    id = "artifact.synthetic.new-protected-work"
                    edition_id = "edition.synthetic.new-protected-work"
                    artifact_type = "publisher-issued-pdf"
                    media_type = "application/pdf"
                    storage = "tracked"
                    rights_status = "unresolved"
                    sha256 = "{digest}"
                    byte_size = {len(payload)}
                    path = "payload.pdf"
                    """
                ),
                encoding="utf-8",
            )
            records = artifact_manifests(base / "works")
            protected = protected_artifact_manifests(base / "works")
            self.assertEqual(len(protected), 1, "the new protected work was not discovered")
            identities = protected_artifact_identities(protected, records)
            self.assertIn("edition.synthetic.new-protected-work", identities)
            self.assertIn("work.synthetic.new-protected-work", identities)
            source_failures = source_artifact_findings(*protected[0])
            self.assertTrue(
                any("storage is not remote" in finding for finding in source_failures),
                source_failures,
            )
            self.assertTrue(
                any("payload path" in finding for finding in source_failures),
                source_failures,
            )
            isolated_storage_failure = source_artifact_findings(
                base / "isolated" / "artifact.toml",
                {"rights_status": "unresolved", "storage": "tracked"},
            )
            self.assertEqual(
                len(isolated_storage_failure),
                1,
                "the storage mutation must fail without help from a path or payload",
            )
            self.assertIn("storage is not remote", isolated_storage_failure[0])

            download = base / "downloads" / "public.pdf"
            download.parent.mkdir()
            download.write_bytes(payload)
            metadata = base / "downloads" / "public.json"
            metadata.write_text(
                json.dumps({"artifact_id": "artifact.synthetic.new-protected-work"}),
                encoding="utf-8",
            )
            download_failures = download_findings(
                [download, metadata], protected_digests(protected), identities
            )
            self.assertTrue(
                any("duplicates protected artifact" in finding for finding in download_failures),
                download_failures,
            )
            self.assertTrue(
                any("exposes protected identity" in finding for finding in download_failures),
                download_failures,
            )

    def test_public_projection_mutation_rejects_payload_and_private_metadata(self) -> None:
        identity = "artifact.synthetic.mutated-protected-work"
        leaky = {
            "unavailable_translations": [
                {
                    "target": "Collect",
                    "lang": "en",
                    "state": "rights-restricted",
                    "source_id": identity,
                    "artifact_id": identity,
                    "sha256": "e" * 64,
                    "page": 7,
                    "rights": "permission",
                    "text": "PROJECT-CREATED-PROTECTED-PUBLIC-MUTATION",
                }
            ]
        }
        failures = public_liturgy_findings(
            leaky, {identity}, set(), "synthetic public mutation"
        )
        self.assertTrue(any("protected witness identity" in one for one in failures))
        self.assertTrue(any("exact safe fields" in one for one in failures))
        self.assertTrue(any("rights=permission" in one for one in failures))

        status_only = {"translations": [{"rights_status": "permission"}]}
        status_failures = public_liturgy_findings(
            status_only, set(), set(), "synthetic rights_status mutation"
        )
        self.assertTrue(
            any("rights_status=permission" in one for one in status_failures),
            status_failures,
        )

        mismatch_only = {
            "translations": [
                {"rights": "public-domain", "rights_status": "project-created"}
            ]
        }
        mismatch_failures = public_liturgy_findings(
            mismatch_only, set(), set(), "synthetic rights mismatch mutation"
        )
        self.assertTrue(
            any("rights and rights_status disagree" in one for one in mismatch_failures),
            mismatch_failures,
        )

        safe = {
            "unavailable_translations": [
                {"target": "Collect", "lang": "en", "state": "rights-restricted"}
            ]
        }
        self.assertEqual(
            public_liturgy_findings(safe, {identity}, set(), "synthetic safe state"),
            [],
        )
        for field, value in (
            ("text", "PROJECT-CREATED-PROTECTED-PAYLOAD-ONLY-MUTATION"),
            ("source_id", identity),
            ("artifact_id", identity),
            ("page", 7),
            ("sha256", "a" * 64),
        ):
            mutated = json.loads(json.dumps(safe))
            mutated["unavailable_translations"][0][field] = value
            one_fault = public_liturgy_findings(
                mutated, {identity}, set(), f"synthetic one-fault {field} mutation"
            )
            self.assertTrue(
                any("exact safe fields" in finding for finding in one_fault),
                f"{field}: {one_fault}",
            )

        safe_target = {
            "mass": "synthetic-mass",
            "form_id": "main",
            "proper": "Collect",
            "cycle": "all",
            "occurrence": 1,
            "extent": "body",
        }
        structured = {
            "unavailable_translations": [
                {
                    "target": safe_target,
                    "lang": "en",
                    "state": "rights-restricted",
                }
            ]
        }
        self.assertEqual(
            public_liturgy_findings(
                structured, set(), set(), "synthetic structured safe state"
            ),
            [],
        )
        smuggled = json.loads(json.dumps(structured))
        smuggled["unavailable_translations"][0]["target"]["source_id"] = identity
        smuggled_failures = public_liturgy_findings(
            smuggled, {identity}, set(), "synthetic target smuggling mutation"
        )
        self.assertTrue(
            any("restricted target differs" in one for one in smuggled_failures),
            smuggled_failures,
        )
        bool_occurrence = json.loads(json.dumps(structured))
        bool_occurrence["unavailable_translations"][0]["target"]["occurrence"] = True
        bool_failures = public_liturgy_findings(
            bool_occurrence, set(), set(), "synthetic bool occurrence mutation"
        )
        self.assertTrue(
            any("invalid occurrence" in one for one in bool_failures),
            bool_failures,
        )

    def test_common_projection_mutation_rejects_source_artifact_and_locus(self) -> None:
        leaky = {
            "masses": [
                {
                    "key": "synthetic-common",
                    "common_from": {
                        "scope": "missal-propers-except-collect",
                        "source_id": "edition.synthetic.protected-common",
                        "artifact_id": "artifact.synthetic.protected-common",
                        "locus": "PROJECT-CREATED-PRIVATE-LOCATOR",
                        "options": [{"mass": "commune-demo"}],
                    },
                }
            ]
        }
        failures = public_liturgy_findings(
            leaky,
            {
                "edition.synthetic.protected-common",
                "artifact.synthetic.protected-common",
            },
            set(),
            "synthetic Common mutation",
        )
        self.assertTrue(any("protected witness identity" in one for one in failures))
        self.assertTrue(any("public common_from fields" in one for one in failures))

        safe = {
            "masses": [
                {
                    "key": "synthetic-common",
                    "common_from": {
                        "scope": "missal-propers-except-collect",
                        "options": [
                            {
                                "mass": "commune-demo",
                                "form_id": "form-a",
                                "selection": "Form A",
                            }
                        ],
                    },
                }
            ]
        }
        self.assertEqual(
            public_liturgy_findings(
                safe,
                {"artifact.synthetic.protected-common"},
                set(),
                "synthetic safe Common",
            ),
            [],
        )

    def test_ordinary_absence_mutation_enforces_neutral_exact_state(self) -> None:
        safe = {
            "absences": [
                {
                    "key": "protected-text",
                    "count": 3,
                    "state": "rights-restricted",
                    "kind": "rights-withheld",
                },
                {
                    "key": "no-exemplar",
                    "count": 2,
                    "state": "unavailable",
                    "kind": "no-exemplar",
                },
            ]
        }
        self.assertEqual(
            public_liturgy_findings(safe, set(), set(), "synthetic Ordinary"),
            [],
        )
        leaky = {
            "absences": [
                {
                    "key": "icel-permission",
                    "count": 3,
                    "state": "rights-restricted",
                    "kind": "rights-withheld",
                    "what": "PROJECT-CREATED-PRIVATE-PROVENANCE-MUTATION",
                },
                {
                    "key": "icel-permission",
                    "count": 3,
                    "state": "rights-restricted",
                    "kind": "rights-withheld",
                },
            ]
        }
        failures = public_liturgy_findings(
            leaky, set(), set(), "synthetic leaky Ordinary"
        )
        self.assertTrue(any("exact safe fields" in one for one in failures), failures)
        self.assertTrue(any("key is not neutral" in one for one in failures), failures)

    def test_source_inventory_mutation_rejects_protected_text_not_metadata(self) -> None:
        identity = "artifact.synthetic.protected-source-mutation"
        metadata_only = {
            "artifact_id": identity,
            "rights": "unresolved",
            "sha256": "d" * 64,
            "lang": "en",
        }
        self.assertEqual(
            source_inventory_findings(metadata_only, {identity}, "metadata-only"),
            [],
        )
        leaky = metadata_only | {"text": "PROJECT-CREATED-PROTECTED-SOURCE-MUTATION"}
        self.assertTrue(
            source_inventory_findings(leaky, {identity}, "leaky source row")
        )

    def test_ellc_source_study_mutation_rejects_flattening_and_lost_notice(self) -> None:
        record = {
            "rights_basis": (
                "English Language Liturgical Consultation (ELLC), "
                "used by permission. www.englishtexts.org"
            ),
            "notes": (
                "Not a liturgical book; this study is not approved and "
                "nothing here may be used for recitation."
            ),
        }
        rows = [
            {
                "element_key": "synthetic",
                "line": "1",
                "text": "PROJECT-CREATED ELLC source-study mutation line one.",
            },
            {
                "element_key": "synthetic",
                "line": "2",
                "text": "PROJECT-CREATED ELLC source-study mutation line two.",
            },
        ]
        self.assertEqual(ellc_source_study_findings(record, rows), [])
        flattened = [
            {
                "element_key": "synthetic",
                "line": "1",
                "text": " ".join(str(row.get("text") or "") for row in rows),
            }
        ]
        failures = ellc_source_study_findings(
            {**record, "rights_basis": "", "acknowledgement": ""}, flattened
        )
        self.assertTrue(any("notice" in one for one in failures), failures)
        self.assertTrue(any("flattened" in one for one in failures), failures)
        bodies = ellc_bodies(rows)
        line_failure = ellc_output_findings(
            rows[0]["text"], set(), bodies, "synthetic ELLC line mutation"
        )
        self.assertTrue(any("sense line" in one for one in line_failure), line_failure)


if __name__ == "__main__":
    unittest.main()
