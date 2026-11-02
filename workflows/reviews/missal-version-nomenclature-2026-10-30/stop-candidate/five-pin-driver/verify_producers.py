#!/usr/bin/env python3
"""Read-only Names53 producer checks, separate from fixture bookkeeping."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys

import names_metadata as m

RAW = Path(__file__).read_bytes()
PAIRS = [('roman-1962', 'roman-1962'), ('roman-pre-1955', 'roman-bonn-2004-study'),
         ('postconciliar', 'roman-2008-study')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--parent', required=True)
    parser.add_argument('--test-root-binding', required=True)
    parser.add_argument('--test-root-binding-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    m.require(out.is_relative_to(root / m.OWN) and not out.exists(), 'fresh own behavior output')
    _, updates, runtime = m.names_context(root)
    m.test_root_binding(root, args.test_root_binding, args.test_root_binding_sha256, args.parent)
    m.pinned(root, m.SNAPSHOT, m.SNAPSHOT_SHA)
    m.pinned(root, m.SUPPORT, m.SUPPORT_SHA)
    support = runpy.run_path(str(root / m.SUPPORT))
    store, _, rows, _ = m.parent_state(root, args.parent, support)
    expected = {r['path']: updates[r['path']]['after_sha256'] if r['path'] in updates else r['post_sha256'] for r in rows}
    def scope_exact():
        for name, digest in expected.items():
            m.pinned(root, name, digest)
    scope_exact()
    guard = m.Runtime(root, store, args.parent, runtime)
    for name in runtime:
        guard.check(root / name)
    sys.addaudithook(guard.audit)
    sys.path.insert(0, str(root / 'scripts'))
    import _missal_versions as versions
    import _recensions
    producers = {name: runpy.run_path(str(root / 'tools' / name)) for name in
                 ('mass-propers', 'mass-ordinary', 'calendar-days', 'calendar-rubrics')}
    sources, calendars = root / 'src/sources', root / 'src/sources/calendars'
    m.require(not _recensions.catalog_problems(calendars, repository=root, required=True), 'actual source-root catalog validation')
    props, ordinary = producers['mass-propers'], producers['mass-ordinary']
    artifacts = ordinary['artifact_records'](sources)
    contributions = []
    for internal, public in PAIRS:
        actual_p = props['calendar_structure'](calendars, internal, props['book_tokens']())
        inventory = sources / 'inventories' / (internal + ordinary['INVENTORY_SUFFIX'])
        actual_o = ordinary['calendar_structure'](sources, inventory, artifacts)
        prior_p = json.loads(store.blob(args.parent, 'src/web/data/structure/propers/' + internal + '.json'))
        prior_o = json.loads(store.blob(args.parent, 'src/web/data/structure/ordinary/' + internal + '.json'))
        for label, old, new in [('propers', prior_p, actual_p), ('ordinary', prior_o, actual_o)]:
            m.require(m.canonical(m.producer_semantics(old)) == m.canonical(m.producer_semantics(new)), 'actual producer body/source/grade/choice/event preservation ' + internal + '/' + label)
        before = versions.contribution_from_published(propers=prior_p, ordinary=prior_o)
        after = versions.reader_metadata(calendars, internal, propers=actual_p, ordinary=actual_o)
        m.require(m.canonical(after['reader_contribution']) == m.canonical(before) and before['eligible'], 'actual lawful-body contribution ' + internal)
        m.require(not versions.public_metadata_problems(after, calendars, internal), 'source-owned public metadata ' + internal)
        m.require(versions.normalize_calendar_key(calendars, public) == internal, 'exact public alias ' + public)
        contributions.append({'calendar': internal, 'public': public, 'contribution': before,
                              'propers_semantic_sha256': m.sha(m.canonical(m.producer_semantics(actual_p)).encode()),
                              'ordinary_semantic_sha256': m.sha(m.canonical(m.producer_semantics(actual_o)).encode())})
    def cli(name, key):
        common = ['--root', str(sources if name == 'mass-ordinary' else calendars), '--calendar', key, '--json']
        command = {'mass-propers': ['list'], 'mass-ordinary': ['coverage'],
                   'calendar-days': ['day', '--date', '2026-04-05'],
                   'calendar-rubrics': ['day', '--date', '2026-04-05']}[name] + common
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = producers[name]['main'](command)
        return rc, stdout.getvalue()
    aliases = []
    for name in producers:
        for internal, public in PAIRS[1:]:
            old, new = cli(name, internal), cli(name, public)
            m.require(old[0] == new[0] == 0 and old[1] == new[1], 'actual CLI aliases exact ' + name + '/' + public)
            aliases.append({'tool': name, 'internal': internal, 'public': public, 'output_sha256': m.sha(old[1].encode())})
        for refused in ['unknown-reader', *(b['id'] for b in versions.catalog(calendars)['books'])]:
            m.require(cli(name, refused)[0] != 0, 'book/unknown key cannot select a reader ' + name)
    for name, digest in guard.observed.items():
        m.pinned(root, name, digest)
    scope_exact()
    m.test_root_binding(root, args.test_root_binding, args.test_root_binding_sha256, args.parent)
    m.pinned(root, m.SNAPSHOT, m.SNAPSHOT_SHA)
    m.require(Path(__file__).read_bytes() == RAW and Path(m.__file__).read_bytes() == m.RAW, 'behavior and metadata driver bytes stable')
    proof = {'schema': 'triptych-Names53-actual-source-producer-review-input/v1',
             'status': 'checks-PASS-independent-root-review-pending', 'parent_git_revision': args.parent,
             'source_input_manifest_sha256': m.sha(m.encoded([{'path': p, 'post_sha256': expected[p]} for p in sorted(expected)])),
             'contributions': contributions, 'actual_four_cli_alias_pairs': aliases,
             'actual_unknown_and_nine_book_keys_refused_by_each_tool': True,
             'runtime_code_sha256': guard.observed, 'metadata_driver_sha256': m.sha(m.RAW),
             'behavior_driver_sha256': m.sha(RAW), 'canonical_writes': 0,
             'publication_permission_created': False, 'generated_output_currentness_or_browser_acceptance_claimed': False}
    out.mkdir(parents=True)
    (out / 'behavior-proof.json').write_bytes(m.encoded(proof))
    print(json.dumps({'status': proof['status'], 'actual_readers': len(contributions), 'alias_pairs': len(aliases)}, sort_keys=True))


if __name__ == '__main__':
    main()
