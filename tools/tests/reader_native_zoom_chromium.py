#!/usr/bin/env python3
"""Opt-in native Chrome tab-zoom regression over an identity-bound built artifact."""
from __future__ import annotations

import argparse
import base64
import functools
import hashlib
import http.server
import json
import math
import os
import re
from pathlib import Path
import shutil
import signal
import socket
import struct
import subprocess
import tempfile
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / '.scratch/reader-native-zoom'
FIXTURES = ROOT / 'tools/tests/fixtures/liturgy-reader-native-zoom/v1'
EXTENSION = FIXTURES / 'extension'
STATE = (FIXTURES / 'reader-state.js').read_text(encoding='utf-8')
WINDOW_SIZE = (1280, 1000)
ELEMENT = 'element-6066-11e4-a52e-4f735466cecf'


def save(file: Path, value):
    file.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def verify_artifact(root: Path, expected: str):
    root = root.resolve(strict=True)
    manifest = (root / 'SHA256SUMS').read_bytes()
    assert hashlib.sha256(manifest).hexdigest() == expected, 'artifact manifest identity differs'
    total = 0
    for line in manifest.decode().splitlines():
        digest, relative = line.split('  ', 1)
        path = root / relative
        assert not path.is_symlink() and path.resolve().is_relative_to(root), relative
        assert path.is_file(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, relative
        total += 1
    return {'sha256sums_sha256': expected, 'verified_files': total,
            'publication_manifest_sha256': hashlib.sha256((root / 'PUBLICATION-MANIFEST.json').read_bytes()).hexdigest()}


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def group_members(group):
    found = []
    if not Path('/proc/self/stat').exists():
        # POSIX hosts without Linux procfs still expose process groups via ps.
        rows = subprocess.check_output([require_executable('ps'), '-A', '-o', 'pid=,pgid=,stat='], text=True)
        for row in rows.splitlines():
            pid, pgid, state = row.split()
            if int(pgid) == group and not state.startswith(('Z', 'X')):
                found.append(int(pid))
        return found
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields = path.read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == group and fields[0] not in ('Z', 'X'):
                found.append(int(path.parent.name))
        except (OSError, ValueError, IndexError):
            pass
    return found


def clean_group(group):
    for signum in (signal.SIGTERM, signal.SIGKILL):
        if not group_members(group):
            return []
        try:
            os.killpg(group, signum)
        except ProcessLookupError:
            return []
        until = time.monotonic() + 3
        while time.monotonic() < until and group_members(group):
            time.sleep(.05)
    return group_members(group)


class Browser:
    def __init__(self, out, chrome, driver):
        self.out = out
        self.port = free_port()
        self.session = None
        self.trace = []
        self.api_results = []
        self.chrome_binary = chrome
        self.driver_binary = driver
        self.profile = None
        self.log = None
        self.driver = None

    def request(self, method, path, value=None, timeout=35):
        self.trace.append({'method': method, 'endpoint': path,
                           **({'cdp_command': value['cmd']} if value and 'cmd' in value else {})})
        request = urllib.request.Request(f'http://127.0.0.1:{self.port}' + path,
            method=method, headers={'Content-Type': 'application/json'},
            data=json.dumps(value).encode() if value is not None else None)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.load(response)['value']
        except urllib.error.HTTPError as error:
            raise RuntimeError(error.read().decode()) from error
        if isinstance(data, dict) and 'error' in data:
            raise RuntimeError(json.dumps(data))
        return data

    def wd(self, method, path, value=None):
        return self.request(method, '/session/' + self.session + path, value)

    def start(self):
        self.profile = Path(tempfile.mkdtemp(prefix='profile-', dir=self.out))
        self.log = (self.out / 'chromedriver.log').open('wb')
        self.driver = subprocess.Popen([self.driver_binary, f'--port={self.port}',
                                        '--log-level=WARNING'], stdout=self.log,
                                       stderr=self.log, start_new_session=True)
        save(self.out / 'handles.json', {'driver_pid': self.driver.pid,
             'process_group': self.driver.pid, 'driver_port': self.port,
             'profile': str(self.profile)})
        self.wait(lambda: self.request('GET', '/status'), 'ChromeDriver startup', retry=True)
        arguments = ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
                     '--window-size=%d,%d' % WINDOW_SIZE,
                     '--user-data-dir=' + str(self.profile),
                     '--load-extension=' + str(EXTENSION),
                     '--disable-extensions-except=' + str(EXTENSION)]
        capabilities = {'browserName': 'chrome', 'pageLoadStrategy': 'none',
            'goog:loggingPrefs': {'browser': 'ALL', 'performance': 'ALL'},
            'goog:chromeOptions': {'binary': self.chrome_binary, 'args': arguments,
                'excludeSwitches': ['disable-extensions'], 'enableExtensionTargets': True}}
        value = self.request('POST', '/session', {'capabilities': {'alwaysMatch': capabilities}})
        self.session = value['sessionId']
        save(self.out / 'capabilities.json', {'requested': capabilities, 'returned': value['capabilities']})
        self.wd('POST', '/timeouts', {'script': 20000, 'pageLoad': 30000, 'implicit': 0})
        self.wait(self.find_control, 'MV3 control page', retry=True)
        window = self.wd('GET', '/window/rect')
        assert (window['width'], window['height']) == WINDOW_SIZE, 'requested desktop window bounds not established'
        command_line = self.wd('POST', '/goog/cdp/execute', {'cmd': 'Browser.getBrowserCommandLine', 'params': {}})
        save(self.out / 'browser-command-line.json', command_line)
        forbidden = ('--force-device-scale-factor', '--high-dpi-support', '--enable-device-emulation')
        assert not any(arg.startswith(forbidden) for arg in command_line['arguments'])

    def js(self, script, *arguments):
        return self.wd('POST', '/execute/sync', {'script': script, 'args': list(arguments)})

    def extension(self, operation, *arguments):
        self.wd('POST', '/window', {'handle': self.control})
        result = self.wd('POST', '/execute/async', {
            'script': 'const done=arguments[arguments.length-1]; '
                      'window.ReaderNativeZoom[arguments[0]](...arguments[1]).then('
                      'value=>done({ok:true,value}),error=>done({ok:false,error:String(error)}));',
            'args': [operation, list(arguments)]})
        self.api_results.append({'operation': operation, 'arguments': arguments, 'response': result})
        save(self.out / 'extension-api-results.json', self.api_results)
        assert result['ok'], result
        return result.get('value')

    def find_control(self):
        for handle in self.wd('GET', '/window/handles'):
            self.wd('POST', '/window', {'handle': handle})
            url = self.wd('GET', '/url')
            if url.startswith('chrome-extension://') and url.endswith('/control.html'):
                if self.js('return !!window.ReaderNativeZoom'):
                    self.control = handle
                    return True
        return False

    def wait(self, predicate, message, retry=False):
        until = time.monotonic() + 25
        while time.monotonic() < until:
            try:
                value = predicate()
                if value:
                    return value
            except Exception:
                if not retry:
                    raise
            time.sleep(.05)
        raise AssertionError('timeout: ' + message)

    def settle(self):
        self.wd('POST', '/execute/async', {'script':
            'const done=arguments[arguments.length-1]; requestAnimationFrame(()=>'
            'requestAnimationFrame(()=>requestAnimationFrame(()=>done(true))));', 'args': []})

    def scroll_settled(self):
        return self.wd('POST', '/execute/async', {'script': '''
            const done=arguments[arguments.length-1], start=performance.now();
            let previous={x:scrollX,y:scrollY}, stable=0, frames=0;
            const samples=[];
            function sample(now) {
              const position={x:scrollX,y:scrollY};
              stable=Math.abs(position.x-previous.x)<.1 && Math.abs(position.y-previous.y)<.1
                ? stable+1 : 0;
              previous=position; frames++;
              samples.push({elapsed:now-start,x:position.x,y:position.y});
              if(samples.length>12) samples.shift();
              const settled=now-start>=150 && stable>=6;
              if(settled || now-start>=3000) {
                done({settled,elapsed:now-start,frames,stableFrames:stable,lastSamples:samples});
              } else requestAnimationFrame(sample);
            }
            requestAnimationFrame(sample);
        ''', 'args': []})

    def click(self, selector):
        element = self.wd('POST', '/element', {'using': 'css selector', 'value': selector})
        self.wd('POST', '/element/' + element[ELEMENT] + '/click', {})

    def key(self, value):
        self.wd('POST', '/actions', {'actions': [{'type': 'key', 'id': 'keyboard', 'actions': [
            {'type': 'keyDown', 'value': value}, {'type': 'keyUp', 'value': value}]}]})

    def picture(self, filename):
        png = base64.b64decode(self.wd('GET', '/screenshot'))
        (self.out / filename).write_bytes(png)
        return list(struct.unpack('>II', png[16:24]))

    def snapshot(self):
        return self.js(STATE)

    def diagnostics(self):
        browser = self.wd('POST', '/se/log', {'type': 'browser'})
        performance = self.wd('POST', '/se/log', {'type': 'performance'})
        bad = []
        for item in performance:
            message = json.loads(item['message'])['message']
            if message['method'] == 'Network.responseReceived':
                response = message['params']['response']
                if response['status'] >= 400:
                    bad.append({'status': response['status'], 'url': response['url']})
            if message['method'] == 'Network.loadingFailed' and not message['params'].get('canceled'):
                bad.append({'network_error': message['params'].get('errorText')})
        return {'browser': [row for row in browser if row['level'] in ('SEVERE', 'WARNING')], 'network': bad}

    def close(self):
        if self.session:
            try:
                self.request('DELETE', '/session/' + self.session, timeout=3)
            except Exception:
                pass
        remaining = clean_group(self.driver.pid) if self.driver else []
        if self.driver:
            try:
                self.driver.wait(timeout=5)
            except subprocess.TimeoutExpired:
                remaining = sorted(set(remaining + [self.driver.pid]))
        if self.log:
            self.log.close()
        save(self.out / 'command-trace.json', self.trace)
        if not remaining and self.profile:
            shutil.rmtree(self.profile, ignore_errors=True)
        return remaining


def cases():
    rows = []
    for entrance in ('day', 'propers'):
        for mode in ('read', 'missal', 'study', 'compare'):
            values = {'missal': 'roman-1962', 'bible': 'douay-rheims', 'orations': 'la', 'mode': mode}
            if entrance == 'day':
                # Let the canonical Day resolve its source-owned formulary.
                values['date'] = '2026-11-22'
                if mode == 'compare':
                    values.update(compare='recension', **{'peer-missal': 'postconciliar', 'territory': 'universal', 'ordinary': '0'})
            else:
                values.update(type='seasonal', mass='pentecost-10')
                if mode == 'compare':
                    values.update(compare='oration-language', **{'peer-orations': 'en'})
            if mode == 'missal':
                values['ordinary-lang'] = 'la'
            rows.append({'name': entrance + '-' + mode, 'entrance': entrance, 'mode': mode,
                         'path': '/liturgy/' + ('day.html' if entrance == 'day' else 'index.html') +
                                 '#' + urllib.parse.urlencode(values)})
    return rows


def run_case(browser, origin, case):
    partial = {'case': case, 'status': 'running', 'phase': 'create-reader'}
    def progress(**values):
        partial.update(values)
        save(browser.out / (case['name'] + '-partial.json'), partial)
    progress()
    handles = set(browser.wd('GET', '/window/handles'))
    tab = browser.extension('create', origin + case['path'])
    progress(tab=tab)
    browser.wait(lambda: len(set(browser.wd('GET', '/window/handles')) - handles) == 1, 'reader tab')
    handle = (set(browser.wd('GET', '/window/handles')) - handles).pop()
    browser.wd('POST', '/window', {'handle': handle})
    browser.wait(lambda: browser.js('const d=window[arguments[0]]; return !!d?.ready && '
        'd.state?.requestedMode===arguments[1] && ["ready","unresolved"].includes(d.outcome) && '
        'document.getElementById("reader-document")?.getAttribute("aria-busy")==="false";',
        case['entrance'] + 'ReaderDebug', case['mode']), case['name'] + ' reader')
    baseline_zoom = browser.extension('set', tab['tabId'], 1)
    browser.wd('POST', '/window', {'handle': handle})
    browser.settle()
    baseline = browser.snapshot()
    baseline_window = browser.wd('GET', '/window/rect')
    baseline_pixels = browser.picture(case['name'] + '-100.png')
    progress(phase='baseline-recorded', baseline_api=baseline_zoom, baseline=baseline,
             baseline_window=baseline_window, baseline_pixels=baseline_pixels)
    zoom = browser.extension('set', tab['tabId'], 4)
    browser.wd('POST', '/window', {'handle': handle})
    browser.settle()
    enlarged = browser.snapshot()
    enlarged_pixels = browser.picture(case['name'] + '-400.png')
    geometry = {'baseline_api': baseline_zoom, 'zoom_api': zoom,
                'baseline': baseline, 'zoomed': enlarged,
                'baseline_window': baseline_window,
                'zoom_window': browser.wd('GET', '/window/rect'),
                'baseline_pixels': baseline_pixels, 'zoom_pixels': enlarged_pixels}
    save(browser.out / (case['name'] + '-zoom-geometry.json'), geometry)
    progress(phase='zoom-recorded-before-assertions', **geometry)
    # Chromium stores a logarithmic level and converts it back to a factor.
    # Preserve the unrounded API result and tolerate only conversion noise.
    equivalent = lambda value, expected: math.isclose(value, expected, rel_tol=0, abs_tol=1e-9)
    assert equivalent(baseline_zoom['reportedZoomFactor'], 1) and equivalent(zoom['reportedZoomFactor'], 4), \
        repr({'baseline_factor': baseline_zoom['reportedZoomFactor'], 'zoom_factor': zoom['reportedZoomFactor']})
    assert zoom['settings']['mode'] == 'automatic'
    assert zoom['settings']['scope'] == 'per-tab'
    assert any(equivalent(event['newZoomFactor'], 4) for event in zoom['events']), repr(zoom['events'])
    assert browser.wd('GET', '/window/rect') == baseline_window, 'physical browser bounds changed'
    assert baseline_zoom['window'] == zoom['window'], 'extension-reported window bounds changed'
    assert baseline_pixels == enlarged_pixels, 'output pixel viewport changed'
    assert abs(enlarged['devicePixelRatio'] / baseline['devicePixelRatio'] - 4) < .01
    assert abs(enlarged['cssViewport']['width'] * 4 - baseline['cssViewport']['width']) <= 4
    assert enlarged['visualViewport']['scale'] == baseline['visualViewport']['scale'] == 1
    assert enlarged['root']['zoom'] == baseline['root']['zoom']
    assert enlarged['root']['bodyZoom'] == baseline['root']['bodyZoom']
    assert enlarged['root']['fontSize'] == baseline['root']['fontSize']
    assert enlarged['cssViewport']['scrollWidth'] <= enlarged['cssViewport']['width'] + 1
    if case['mode'] == 'compare':
        assert enlarged['comparePairColumns'] and all(len(columns.split()) == 1
            for columns in enlarged['comparePairColumns']), 'Compare did not stack at native zoom'
    browser.click('[data-reader-action="contents"]')
    browser.settle()
    destination = browser.js('const rows=[...document.querySelectorAll("[data-reader-location]")]; '
        'return rows[Math.floor(rows.length*.6)]?.dataset.readerLocation;')
    assert destination, 'Contents has no semantic target'
    browser.picture(case['name'] + '-400-contents.png')
    browser.click('[data-reader-location=' + json.dumps(destination) + ']')
    scroll_readiness = browser.scroll_settled()
    landed = browser.snapshot()
    browser.picture(case['name'] + '-400-landed.png')
    progress(phase='contents-landed', contents_destination=destination,
             scroll_readiness=scroll_readiness, landed=landed)
    assert scroll_readiness['settled'], repr(scroll_readiness)
    assert landed['focus']['semanticLocation'] == destination
    assert landed['scroll']['y'] > 0
    assert landed['cssViewport']['scrollWidth'] <= landed['cssViewport']['width'] + 1
    heading = landed['focus']['heading']
    exposed = min(heading['bottom'], landed['actions']['top']) - max(heading['top'], landed['masthead']['bottom'])
    assert exposed >= 12, 'Contents heading is hidden under fixed reader chrome'
    before = browser.snapshot()
    browser.click('[data-reader-action="mode"]')
    browser.settle()
    mode = browser.snapshot()
    browser.picture(case['name'] + '-400-mode.png')
    progress(phase='mode-open', mode_open=mode)
    assert mode['focus']['close'], 'Mode did not focus its Close action'
    assert all(row['scrollWidth'] <= row['clientWidth'] + 1 for row in mode['openSurfaces'])
    browser.key('\ue00c')  # Native WebDriver Escape key.
    browser.settle()
    closed = browser.snapshot()
    browser.picture(case['name'] + '-400-restored.png')
    progress(phase='mode-closed', mode_closed=closed)
    assert closed['focus']['action'] == 'mode'
    assert closed['currentUnit'] == before['currentUnit']
    assert abs(closed['scroll']['y'] - before['scroll']['y']) <= 2
    focus = closed['focus']['rect']
    assert 0 <= focus['left'] and focus['right'] <= closed['cssViewport']['width'] + 1
    assert 0 <= focus['top'] and focus['bottom'] <= closed['cssViewport']['height'] + 1
    assert closed['focus']['outline'] != 'none', 'restored Mode focus is not visible'
    final_zoom = browser.extension('describe', tab['tabId'])
    progress(phase='final-zoom-recorded', final_zoom_api=final_zoom)
    assert equivalent(final_zoom['reportedZoomFactor'], 4), repr(final_zoom['reportedZoomFactor'])
    browser.extension('remove', tab['tabId'])
    progress(status='pass', phase='case-complete')
    return {'case': case, 'status': 'pass', 'baseline_api': baseline_zoom, 'zoom_api': zoom,
            'baseline_window': baseline_window, 'baseline_pixels': baseline_pixels,
            'zoom_pixels': enlarged_pixels, 'baseline': baseline, 'zoomed': enlarged,
            'contents_destination': destination, 'landed': landed,
            'mode_open': mode, 'mode_closed': closed, 'final_zoom_api': final_zoom,
            'scroll_readiness': scroll_readiness}


def load_release(config_path: Path):
    """Bind one explicitly released run to reviewed source and artifact identities."""
    config = json.loads(config_path.read_text(encoding='utf-8'))
    if config.get('released_by_coordinator') is not True:
        raise ValueError('native zoom is on HOLD: release config must explicitly enable this run')
    if config.get('smoke_only') is True:
        raise ValueError('the registered check always runs all eight cases; a smoke release is insufficient')
    for field, digits in (('source_commit', 40), ('runtime_source_commit', 40),
                          ('sha256sums_sha256', 64), ('publication_manifest_sha256', 64)):
        if not re.fullmatch('[0-9a-f]{%d}' % digits, str(config.get(field, ''))):
            raise ValueError(f'{field} must be a full lowercase hexadecimal identity')
    if not isinstance(config.get('source_qualification'), str) or not config['source_qualification'].strip():
        raise ValueError('source_qualification must describe reviewed HEAD/runtime provenance')
    relative = Path(config['artifact_root'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('artifact_root must be a repository-relative path')
    artifact = (ROOT / relative).resolve(strict=True)
    if not artifact.is_relative_to(ROOT):
        raise ValueError('artifact_root must resolve inside the repository')
    return config, artifact


def scratch_root():
    path = Path(os.environ.get('TRIPTYCH_BROWSER_SCRATCH', SCRATCH)).resolve()
    owned = (ROOT / '.scratch').resolve()
    if path == owned or not path.is_relative_to(owned):
        raise ValueError('TRIPTYCH_BROWSER_SCRATCH must be a child of repository .scratch')
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_executable(name):
    found = shutil.which(name)
    if found:
        candidate = Path(found).resolve()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    # Personal guidance treats a local-bin executable as available after a PATH
    # miss. Explicit paths keep their meaning; only bare command names fall back.
    if Path(name).name == name:
        candidate = (Path.home() / '.local/bin' / name).resolve()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def require_executable(name):
    if found := find_executable(name):
        return found
    raise ValueError(f'{name!r} is not executable on PATH or under ~/.local/bin')


def binary(environment, choices):
    configured = os.environ.get(environment)
    if configured:
        found = find_executable(configured)
        if found:
            return found
        raise ValueError(f'{environment} does not name an executable')
    for name in choices:
        if found := find_executable(name):
            return found
    raise ValueError(f'{environment} is required; no executable found among {choices!r}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True,
                        help='explicit artifact/source release JSON; see fixture README')
    parser.add_argument('--released', action='store_true',
                        help='coordinator has released this expensive run after quiet timing')
    args = parser.parse_args()
    if not args.released:
        parser.error('native zoom is on HOLD; no server or browser was started')
    if not __debug__:
        parser.error('Python assertions must be enabled for this regression test')
    try:
        if os.name != 'posix':
            raise ValueError('this runner requires POSIX process groups for owned browser cleanup')
        config, artifact = load_release(args.config)
        chrome = binary('TRIPTYCH_CHROME', ('chromium', 'chromium-browser', 'google-chrome'))
        driver = binary('TRIPTYCH_CHROMEDRIVER', ('chromedriver',))
        git = require_executable('git')
        source_commit = subprocess.check_output([git, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        if source_commit != config['source_commit']:
            raise ValueError('actual reviewed HEAD differs from release config source_commit')
        subprocess.run([git, 'cat-file', '-e', config['runtime_source_commit'] + '^{commit}'],
                       cwd=ROOT, check=True, capture_output=True)
        identity = verify_artifact(artifact, config['sha256sums_sha256'])
        if identity['publication_manifest_sha256'] != config['publication_manifest_sha256']:
            raise ValueError('publication manifest identity differs from release config')
        out = Path(tempfile.mkdtemp(prefix=time.strftime('%Y%m%dT%H%M%SZ-', time.gmtime()),
                                    dir=scratch_root()))
    except (OSError, ValueError, KeyError, AssertionError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    save(out / 'release-config.json', config)
    source_status = subprocess.check_output([git, 'status', '--porcelain=v1'], cwd=ROOT, text=True)
    requests = []
    class Server(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if urllib.parse.urlsplit(self.path).path == '/favicon.ico':
                self.send_response(204); self.end_headers(); return
            super().do_GET()
        def log_request(self, code='-', size='-'):
            requests.append({'path': self.path, 'status': str(code)})
        def log_message(self, *_args):
            pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Server, directory=str(artifact)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    browser = None
    rows = []
    result = {'source_commit': source_commit, 'source_worktree_status': source_status,
              'runtime_source_commit': config['runtime_source_commit'],
              'source_qualification': config['source_qualification'],
              'artifact_root': config['artifact_root'], 'artifact': identity,
              'emulation_configured': False, 'window_size_requested': WINDOW_SIZE,
              'headless': 'unified Chromium headless; genuine automatic tabs API zoom',
              'requested_zoom_factor': 4, 'native_api_absolute_tolerance': 1e-9,
              'visual_review_required': True, 'status': 'fail', 'cases': rows}
    print(json.dumps({'status': 'running', 'result': str(out / 'result.json'),
                      'helper_pid': os.getpid()}), flush=True)
    def interrupted(signum, _frame):
        raise InterruptedError(f'run interrupted by signal {signum}')
    old_handlers = {signum: signal.signal(signum, interrupted)
                    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGALRM)}
    started = False
    try:
        signal.alarm(780)
        thread.start()
        started = True
        browser = Browser(out, chrome, driver)
        browser.start()
        for case in cases():
            row = run_case(browser, f'http://127.0.0.1:{server.server_port}', case)
            rows.append(row)
            save(out / 'result.json', result)
        result['diagnostics'] = browser.diagnostics()
        assert not result['diagnostics']['browser'] and not result['diagnostics']['network']
        assert not any(row.get('cdp_command', '').startswith('Emulation.') for row in browser.trace)
        result['artifact_after'] = verify_artifact(artifact, config['sha256sums_sha256'])
        assert result['artifact_after'] == identity
        result['status'] = 'pass'
    except Exception as error:
        result['error'] = str(error)
        result['traceback'] = traceback.format_exc()
        partials = sorted(out.glob('*-partial.json'), key=lambda file: file.stat().st_mtime_ns)
        if partials:
            result['partial_case'] = json.loads(partials[-1].read_text())
    finally:
        signal.alarm(0)
        # Give the owned cleanup its bounded grace period after interruption.
        for signum in old_handlers:
            signal.signal(signum, signal.SIG_IGN)
        if browser and browser.session and 'diagnostics' not in result:
            try:
                result['diagnostics'] = browser.diagnostics()
            except Exception as error:
                result['diagnostics_collection_error'] = str(error)
        try:
            result['remaining_group_pids'] = browser.close() if browser else []
            result['profile_exists'] = bool(browser and browser.profile and browser.profile.exists())
        except Exception as error:
            result['cleanup_error'] = str(error)
            result['remaining_group_pids'] = group_members(browser.driver.pid) if browser and browser.driver else []
            result['profile_exists'] = bool(browser and browser.profile and browser.profile.exists())
        finally:
            if started:
                server.shutdown()
            server.server_close()
            if started:
                thread.join(timeout=5)
            result['server_thread_alive'] = thread.is_alive()
            for signum, handler in old_handlers.items():
                signal.signal(signum, handler)
        result['requests'] = requests
        result['screenshots'] = [path.name for path in sorted(out.glob('*.png'))]
        if result['remaining_group_pids'] or result['profile_exists'] or result['server_thread_alive'] or result.get('cleanup_error'):
            result['status'] = 'fail'
        save(out / 'result.json', result)
    print(json.dumps({'status': result['status'], 'cases': len(rows), 'result': str(out / 'result.json'),
                      'remaining_group_pids': result['remaining_group_pids']}))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
