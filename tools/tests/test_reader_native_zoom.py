"""Artifact binding and opt-in native 400% zoom over both built readers."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / 'tools/tests/reader_native_zoom_chromium.py'
FIXTURES = ROOT / 'tools/tests/fixtures/liturgy-reader-native-zoom/v1'
SPEC = importlib.util.spec_from_file_location('reader_native_zoom_probe', PROBE)
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


class ReaderNativeZoomTest(unittest.TestCase):
    def test_fixture_javascript_parses(self):
        node = probe.require_executable('node')
        for path in (FIXTURES / 'extension/background.js', FIXTURES / 'extension/control.js'):
            with self.subTest(path=path.name):
                subprocess.run([node, '--check', str(path)], check=True,
                               capture_output=True, text=True, timeout=15)
        # WebDriver scripts have a top-level return, so parse as a function body.
        subprocess.run([node, '-e',
                        'new Function(require("node:fs").readFileSync(process.argv[1],"utf8"));',
                        str(FIXTURES / 'reader-state.js')], check=True,
                       capture_output=True, text=True, timeout=15)

    def test_artifact_binding_rejects_changed_bytes_and_escaped_paths(self):
        scratch = ROOT / '.scratch/reader-native-zoom-offline'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='artifact-', dir=scratch) as temporary:
            base = Path(temporary)
            artifact = base / 'built'
            artifact.mkdir()
            publication = artifact / 'PUBLICATION-MANIFEST.json'
            publication.write_text('{"fixture":true}\n', encoding='utf-8')
            asset = artifact / 'asset.js'
            asset.write_text('/* identity fixture */\n', encoding='utf-8')
            def manifest(entries):
                raw = ''.join(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + name + '\n'
                              for name, path in entries).encode()
                (artifact / 'SHA256SUMS').write_bytes(raw)
                return hashlib.sha256(raw).hexdigest()
            expected = manifest([('PUBLICATION-MANIFEST.json', publication), ('asset.js', asset)])
            receipt = probe.verify_artifact(artifact, expected)
            self.assertEqual(receipt['verified_files'], 2)
            self.assertEqual(receipt['publication_manifest_sha256'],
                             hashlib.sha256(publication.read_bytes()).hexdigest())
            with self.subTest(defect='wrong-manifest-identity'), self.assertRaises(AssertionError):
                probe.verify_artifact(artifact, '0' * 64)
            asset.write_text('/* changed bytes */\n', encoding='utf-8')
            with self.subTest(defect='changed-listed-asset'), self.assertRaises(AssertionError):
                probe.verify_artifact(artifact, expected)
            outside = base / 'outside.txt'
            outside.write_text('outside artifact\n', encoding='utf-8')
            expected = manifest([('../outside.txt', outside)])
            with self.subTest(defect='escaped-path'), self.assertRaises(AssertionError):
                probe.verify_artifact(artifact, expected)
            link = artifact / 'linked.txt'
            link.symlink_to(outside)
            expected = manifest([('linked.txt', outside)])
            with self.subTest(defect='symlink'), self.assertRaises(AssertionError):
                probe.verify_artifact(artifact, expected)

    @unittest.skipUnless(os.environ.get('TRIPTYCH_NATIVE_ZOOM_CHROMIUM') == '1',
                         'set TRIPTYCH_NATIVE_ZOOM_CHROMIUM=1 and TRIPTYCH_NATIVE_ZOOM_CONFIG '
                         'for the expensive, explicitly released built-artifact native zoom check')
    def test_eight_built_reader_cases_at_native_400_percent_zoom(self):
        config = os.environ.get('TRIPTYCH_NATIVE_ZOOM_CONFIG')
        self.assertTrue(config, 'TRIPTYCH_NATIVE_ZOOM_CONFIG must name the released artifact/source record')
        process = subprocess.Popen([sys.executable, str(PROBE), '--config', config, '--released'],
                                   cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
        stdout = stderr = ''
        try:
            stdout, stderr = process.communicate(timeout=900)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    stdout, stderr = process.communicate(timeout=120)
                except subprocess.TimeoutExpired:
                    # Last-resort cleanup uses only the helper's scratch-owned handles.
                    # Preserve its evidence and report failure rather than accepting a leak.
                    os.killpg(process.pid, signal.SIGKILL)
                    stdout, stderr = process.communicate(timeout=10)
                    for line in stdout.splitlines():
                        try:
                            announced = json.loads(line)
                            out = Path(announced['result']).parent.resolve()
                        except (ValueError, KeyError, TypeError):
                            continue
                        if out.is_relative_to((ROOT / '.scratch').resolve()) and (out / 'handles.json').is_file():
                            handles = json.loads((out / 'handles.json').read_text())
                            remaining = probe.clean_group(int(handles['process_group']))
                            profile = Path(handles['profile']).resolve()
                            if not remaining and profile.is_relative_to(out):
                                shutil.rmtree(profile, ignore_errors=True)
                            (out / 'wrapper-cleanup.json').write_text(json.dumps({
                                'forced_helper_stop': True, 'remaining_group_pids': remaining,
                                'profile_exists': profile.exists()}, indent=2) + '\n')
        self.assertEqual(process.returncode, 0, stdout + stderr)
        summary = json.loads(stdout.strip().splitlines()[-1])
        self.assertEqual(summary['status'], 'pass', stdout + stderr)
        self.assertEqual(summary['cases'], 8)
        self.assertEqual(summary['remaining_group_pids'], [])
        report = json.loads(Path(summary['result']).read_text(encoding='utf-8'))
        self.assertEqual({row['case']['name'] for row in report['cases']}, {
            entrance + '-' + mode for entrance in ('day', 'propers')
            for mode in ('read', 'missal', 'study', 'compare')})
        self.assertTrue(all(row['status'] == 'pass' for row in report['cases']))
        self.assertEqual(report['diagnostics'], {'browser': [], 'network': []})
        self.assertFalse(report['profile_exists'])
        self.assertFalse(report['server_thread_alive'])
        self.assertEqual(report['artifact'], report['artifact_after'])


if __name__ == '__main__':
    unittest.main()
