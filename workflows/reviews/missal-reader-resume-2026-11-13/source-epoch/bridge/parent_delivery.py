"""Proposed finite d85 and five-payload delivery successor of the parent proof.

This is candidate adapter support, not a canonical resolver or permission rule.
The adapter must separately bind its exact accepted parent, full manifest and
missing-path domain before calling this function.
"""
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import tomllib

INDEX = 'src/sources/artifact-delivery.json'
D85_OWNER = ('src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/'
             'benziger-revised-1945/artifacts/'
             'english-completion-20261029-postconciliar-opening2-lasance-conclusion217-d85c36fb/'
             'artifact.toml')
D85_BEFORE_SHA = '617e48d287ca3a1b6409d74e9adf1cc8faad0e97bc52fe02706ed4f257b45252'
D85_AFTER_SHA = 'dc71449fba4dd7ffceacc3ad09e57ac8307343811bbfba92f807eacfc2663525'
D85_REVIEW = ('workflows/reviews/missal-reader-resume-2026-11-13/'
              'd85-digitizer-notice/root-adoption.json')
D85_REVIEW_SHA = '0b823b676c8fce1cc4572a9c76b298de7af2854baac39e7ba283e929e3ab3289'
PARENT_INDEX_SHA = '24f2dbb3b4aa20097d3a7719f1d3e9ea5494c738aba5b7174d10ed836090bffc'
TEN_INDEX_SHA = '3c1a023e9777b575f343f3257cac57a711acfcf508a1044ba2cfd0f7abe64bde'
TEN_REVIEW = ('workflows/reviews/missal-reader-resume-2026-11-12/'
              'postconciliar-ten/source-contract-adoption.json')
TEN_REVIEW_SHA = '55b8f5bfdaab2ceaf6c6768470922f04565e51bd919bf28d642fc90762293299'
TEN_ARCHIVE_SHA = '04d04fc3a80723e240c5ba78d01e49bb031704ef5cbcf2a55342c4c6d8a6e0aa'
TEN_ARCHIVE = {
    'id': TEN_ARCHIVE_SHA, 'name': 'triptych-binaries-0012-04d04fc3a80723e2.tar',
    'sha256': TEN_ARCHIVE_SHA, 'bytes': 1484800, 'urls': [], 'delivery': 'offline-only',
}
# Exact paths, complete payload identities and full owner-record digests are
# code-owned. Neither a sidecar nor a source record can extend this finite set.
TEN_PAYLOADS = (
    ('liber-mozarabicus-sacramentorum', 'ferotin-1912',
     'a2c3faecd154022fe00d1c09ed043c3441b78c7e4ae6430164ef287a81f1988e', 167718,
     'ccece4208590fc19a446c82cac88e5ed3fbfa8fbfc132d23fc6df5bb387df007'),
    ('manuale-ambrosianum', 'magistretti-pars-altera-1904',
     'b86a5a1adc0ec7f92e9585b1fafefddc47d0a8c2fd4887589bbbf0063616d759', 445268,
     '08f7c2a4d71f9c402f808bb0a0072aa4e784a41d2d9b075ab2e5e95e0fa655b8'),
    ('missale-romanum', 'pustet-ratisbon-1862',
     '21722c83217e64738042331b1f8185fbd0c497ea9db43b5cb7498c5b3c762997', 623510,
     '2c80f620a6ff9d7dd18fa1247815343ee6c975791bff1aa5f4a22bb8f6b2f2ba'),
    ('sacramentarium-gelasianum-vetus', 'wilson-1894',
     'adab3b804ccdae4e930f71543d5ac24c28b5e54906d76a708e104cc738cfcb69', 131148,
     'dad3ae6a989d99d5b30ac7cea0ea5b20d783b343da927d1fc951acc9f0b964ae'),
    ('sacramentarium-veronense', 'feltoe-1896',
     '1891b45b9a8554097eacd35bce0b3fc3b4c871d70820bfc48e17d0945d2a1cf4', 101806,
     '08c3b82419e4bbd3c6be1034eaf82e78bab64b8d7972b02054ddfece024dd884'),
)


def added_records():
    records = {}
    for work, edition, body_sha, size, owner_sha in TEN_PAYLOADS:
        prefix = ('src/sources/works/catholic-church/' + work + '/editions/' + edition
                  + '/artifacts/ordinary-collects-old-pages-20261112/')
        path = prefix + 'pages.pdf'
        records[path] = ({'path': path, 'sha256': body_sha, 'bytes': size,
                          'kind': 'source-evidence', 'media_type': 'application/pdf',
                          'archive': TEN_ARCHIVE_SHA, 'member': path},
                         prefix + 'artifact.toml', owner_sha)
    return records


def require(value, label):
    if not value:
        raise AssertionError('immutable parent delivery: ' + label)


def digest(raw):
    return sha256(raw).hexdigest()


def ordinary(root, relative):
    path = PurePosixPath(relative)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == relative,
            'canonical repository-relative path')
    result = root
    for part in path.parts:
        result /= part
        require(not result.is_symlink(), 'no symlink ancestry ' + relative)
    return result


def current_owner(root, owner_path, parent_raw, current_pins):
    """Keep ordinary exact equality; permit only the adopted d85 note bytes."""
    import json

    current_raw = ordinary(root, owner_path).read_bytes()
    if current_raw == parent_raw:
        return
    require(owner_path == D85_OWNER and digest(parent_raw) == D85_BEFORE_SHA
            and digest(current_raw) == D85_AFTER_SHA,
            'local artifact owner differs outside the exact admitted d85 metadata successor')
    require(isinstance(current_pins, dict)
            and current_pins.get(D85_OWNER) == D85_AFTER_SHA
            and current_pins.get(D85_REVIEW) == D85_REVIEW_SHA,
            'd85 current owner and actual Root review belong to selected current epoch')
    review_raw = ordinary(root, D85_REVIEW).read_bytes()
    require(digest(review_raw) == D85_REVIEW_SHA, 'complete actual d85 Root review bytes')
    review = json.loads(review_raw)
    before, after = tomllib.loads(parent_raw.decode()), tomllib.loads(current_raw.decode())
    require(review['decision'] == 'accept-exact-rights-basis-absence-correction'
            and review['artifact_manifest_path'] == owner_path
            and review['before_manifest_sha256'] == D85_BEFORE_SHA
            and review['field'] == 'rights_basis'
            and before['rights_basis'] == review['before']
            and after['rights_basis'] == review['after'], 'exact adopted metadata correction')
    restored = dict(after)
    restored['rights_basis'] = before['rights_basis']
    require(restored == before, 'all other parent artifact fields remain unchanged')


def ten_review(root, current_pins):
    require(isinstance(current_pins, dict)
            and current_pins.get(INDEX) == TEN_INDEX_SHA
            and current_pins.get(TEN_REVIEW) == TEN_REVIEW_SHA,
            'local delivery declaration and actual ten review belong to current epoch')
    raw = ordinary(root, TEN_REVIEW).read_bytes()
    require(digest(raw) == TEN_REVIEW_SHA, 'complete actual ten source adoption bytes')
    return json.loads(raw)


def current_declaration(root, parent_raw, current_pins):
    """Retain exact equality, or accept only this independently adopted addition."""
    raw = ordinary(root, INDEX).read_bytes()
    if raw == parent_raw:
        return
    require(digest(parent_raw) == PARENT_INDEX_SHA and digest(raw) == TEN_INDEX_SHA,
            'local delivery declaration differs outside exact five-payload successor')
    ten_review(root, current_pins)
    before, after = json.loads(parent_raw), json.loads(raw)
    records = added_records()
    prior_paths = {row['path'] for row in before['artifacts']}
    require(not prior_paths.intersection(records), 'five new paths were absent from parent')
    additions = [row for row in after['artifacts'] if row['path'] not in prior_paths]
    require(additions == [row[0] for row in records.values()], 'exact five new delivery dictionaries')
    require([row for row in after['artifacts'] if row['path'] in prior_paths] == before['artifacts'],
            'all prior delivery dictionaries and relative ordering remain exact')
    require([row for row in after['archives'] if row['id'] == TEN_ARCHIVE_SHA] == [TEN_ARCHIVE],
            'one exact new offline archive')
    restored = dict(after)
    restored['artifacts'] = before['artifacts']
    restored['archives'] = [row for row in after['archives'] if row['id'] != TEN_ARCHIVE_SHA]
    require(restored == before, 'all other parent declaration fields remain exact')


def read_added_external(root, relative, current_pins):
    """Prove each of the five new actual payloads without widening parent115."""
    from _artifact_store import delivery_entries, resolve
    from _source_delivery_policy import external_source_identity

    root = Path(root).resolve()
    records = added_records()
    require(relative in records, 'exact five newly adopted paths only')
    ordinary(root, relative)
    require(digest(ordinary(root, INDEX).read_bytes()) == TEN_INDEX_SHA,
            'complete adopted current delivery declaration')
    review = ten_review(root, current_pins)
    entry, owner_path, owner_sha = records[relative]
    require(current_pins.get(relative) == entry['sha256']
            and current_pins.get(owner_path) == owner_sha,
            'new payload and complete owner belong to current epoch')
    require([row for row in delivery_entries(root) if row['path'] == relative] == [entry],
            'exact new delivery entry')
    raw_owner = ordinary(root, owner_path).read_bytes()
    require(digest(raw_owner) == owner_sha, 'complete exact newly adopted owner bytes')
    require([row for row in review['source_files'] if row['path'] == owner_path]
            == [{'path': owner_path, 'sha256': owner_sha, 'bytes': len(raw_owner)}],
            'whole owner explicitly bound by actual source adoption')
    owner = tomllib.loads(raw_owner.decode())
    require(external_source_identity(root, relative, metadata=owner)
            == {'path': relative, 'sha256': entry['sha256'], 'byte_size': entry['bytes']},
            'new owner, affirmative distribution rights and delivery identity agree')
    raw = resolve(root, relative, fetch=False).read_bytes()
    require(len(raw) == entry['bytes'] == owner['byte_size']
            and digest(raw) == entry['sha256'] == owner['sha256'],
            'entire actual new local payload bytes and size')
    return raw


def read_parent_external(root, store, parent, pins, relative, *, current_pins=None):
    """Return actual bytes only after committed declaration and owner proof."""
    from _artifact_store import delivery_entries, resolve
    from _source_delivery_policy import external_source_identity

    root = Path(root).resolve()
    require(relative in pins and INDEX in pins, 'payload and declaration belong to parent manifest')
    ordinary(root, relative)
    parent_index = store.blob(parent, INDEX)
    require(digest(parent_index) == pins[INDEX], 'entire committed parent delivery declaration')
    current_declaration(root, parent_index, current_pins)
    rows = [row for row in delivery_entries(root) if row['path'] == relative]
    require(len(rows) == 1, 'one exact declared delivery entry')
    entry = rows[0]
    require(entry['kind'] == 'source-evidence' and entry['sha256'] == pins[relative],
            'exact parent source-evidence payload declaration')
    parts = PurePosixPath(relative).parts
    require(len(parts) >= 10 and parts[:3] == ('src', 'sources', 'works')
            and parts[5] == 'editions' and parts[7] == 'artifacts', 'canonical source artifact owner')
    owner_path = str(PurePosixPath(*parts[:9], 'artifact.toml'))
    require(owner_path in pins, 'owner record belongs to exact accepted parent manifest')
    owner_raw = store.blob(parent, owner_path)
    require(digest(owner_raw) == pins[owner_path], 'entire committed parent artifact owner record')
    current_owner(root, owner_path, owner_raw, current_pins)
    owner = tomllib.loads(owner_raw.decode())
    # Edition IDs may differ from directory labels; the complete accepted
    # parent owner record, including its actual IDs, is pinned above.
    identity = external_source_identity(root, relative, metadata=owner)
    require(identity == {'path': relative, 'sha256': pins[relative], 'byte_size': entry['bytes']},
            'parent owner, publication rights, size, media and declaration agree')
    payload = resolve(root, relative, fetch=False)
    raw = payload.read_bytes()
    require(len(raw) == owner['byte_size'] == entry['bytes']
            and digest(raw) == owner['sha256'] == entry['sha256'] == pins[relative],
            'entire actual local payload bytes and size')
    return raw


def verify_parent_rows(root, store, parent, rows, *, current_pins=None):
    """Verify exactly the accepted v2 logical input epoch at its future commit."""
    import json

    encoded = lambda value: (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                                       allow_nan=False) + '\n').encode()
    require(digest(encoded(rows)) == 'f427c98032220558654aef37d8ccc483ed8dcccb22e4678bbfcf8cdeed4c4658',
            'exact accepted v2 complete input manifest')
    pins = {row['path']: row['post_sha256'] for row in rows}
    require(len(pins) == len(rows) == 7449, 'exact distinct parent input domain')
    tree = store.tree(parent)
    physical = [row for row in rows if row['path'] in tree]
    external = [row for row in rows if row['path'] not in tree]
    require(len(external) == 115 and digest(encoded(external)) ==
            'cc87af4a3995bd5233e3f882bf184a71a0511c9434e0203eb3d7219cfe582acd',
            'exact115 declared absent-Git parent paths and hashes')
    store.verify_rows(parent, physical)
    for row in external:
        raw = read_parent_external(root, store, parent, pins, row['path'], current_pins=current_pins)
        require(digest(raw) == row['post_sha256'], 'actual parent payload ' + row['path'])
    return {'git_blob_inputs': len(physical), 'actual_local_payloads': len(external),
            'input_manifest_sha256': digest(encoded(rows)), 'metadata_only_success': False}
