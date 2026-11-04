"""A small Chromium DevTools driver for focused page-level browser tests.

It reuses the existing CDP harness from `test_browser_truthfulness` without
importing that module's real-corpus fixtures, so callers need no generated
browser-product cache. A plan names inline `responses` (and optional
repository `files`) and a list of `acts`; the harness serves them and
returns what each named act observed.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/cdp-drive"
_test_ast = ast.parse((ROOT / "tools/tests/test_browser_truthfulness.py").read_text())
HARNESS = next(ast.literal_eval(node.value) for node in _test_ast.body if isinstance(node, ast.Assign)
               and any(isinstance(name, ast.Name) and name.id == "HARNESS" for name in node.targets))


def browser():
    found = os.environ.get("TRIPTYCH_CHROME") or shutil.which("chromium") or shutil.which("google-chrome")
    if not found:
        raise unittest.SkipTest("Chromium is unavailable")
    return found


def act(expression, name=None):
    return {"do": "eval", "expression": expression, **({"name": name} if name else {})}


def wait(expression):
    return {"do": "wait", "until": expression}


def idle_arrivals(route, loaded, snapshot):
    """Observe direct and retained print links without invoking their action."""
    return [
        {"do": "navigate", "url": route}, loaded, act(snapshot, "normal"),
        {"do": "navigate", "url": route + "?print=1"}, loaded, act(snapshot, "query"),
        {"do": "reload"}, loaded, act(snapshot, "reload"),
        {"do": "background"},
        {"do": "navigate", "url": route + "?print=1&background=1"}, loaded,
        act(snapshot, "background"), act("document.hidden", "hidden"),
        {"do": "foreground"}]


_ACTIONS = """} else if (act.do === 'click') {
      const point=await evaluate(cdp,`(()=>{const rect=document.querySelector(${JSON.stringify(act.selector)}).getBoundingClientRect();return {x:rect.left+rect.width/2,y:rect.top+rect.height/2};})()`);
      await cdp.send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...point});
      await cdp.send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...point});
    } else if (act.do === 'reload') {
      await evaluate(cdp, 'window.printTestReloadPending=true');
      await cdp.send('Page.reload');
      await waitFor(cdp, "!window.printTestReloadPending && document.readyState === 'complete'", 'reloaded document');
    } else if (act.do === 'background') {
      const other=await cdp.send('Target.createTarget',{url:'about:blank'});
      await cdp.send('Target.activateTarget',{targetId:other.targetId});
      await waitFor(cdp, 'document.hidden', 'background document');
    } else if (act.do === 'foreground') {
      await cdp.send('Page.bringToFront');
      await waitFor(cdp, '!document.hidden', 'foreground document');
    } else if (act.do === 'key') {
      await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:act.key,code:act.code,modifiers:act.modifiers||0});
      await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:act.key,code:act.code,modifiers:act.modifiers||0});
    } else if (act.do === 'media') {
      await cdp.send('Emulation.setEmulatedMedia', {media: act.media});
    } else if (act.do === 'network') {
      await cdp.send('Network.enable');
      await cdp.send('Network.setBlockedURLs', {urls:act.urls});
    } else if (act.do === 'eval') {"""


def drive(plan):
    harness = HARNESS.replace("JSON.parse(process.argv[3])", "JSON.parse(await readFile(process.argv[3], 'utf8'))")
    harness = harness.replace("mkdtemp, readFile, rm", "mkdtemp, readFile, rm, writeFile")
    harness = harness.replace("? PLAN.responses[relative] : await readFile(file)", "? PLAN.responses[relative] : await readFile(Object.hasOwn(PLAN.files || {}, relative) ? resolve(ROOT, PLAN.files[relative]) : file)")
    harness = harness.replace("? PLAN.responses[relative] : await readFile(repositoryPath(ROOT, file))", "? PLAN.responses[relative] : await readFile(repositoryPath(ROOT, Object.hasOwn(PLAN.files || {}, relative) ? resolve(ROOT, PLAN.files[relative]) : file))")
    harness = harness.replace("join(tmpdir(), 'triptych-truthfulness-')", "join(ROOT, '.scratch/cdp-drive/chrome-')")
    harness = harness.replace("} else if (act.do === 'eval') {", _ACTIONS)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=SCRATCH) as folder:
        folder = Path(folder)
        (folder / "harness.mjs").write_text(harness)
        (folder / "plan.json").write_text(json.dumps(plan))
        result = subprocess.run(["node", str(folder / "harness.mjs"), str(ROOT), str(folder / "plan.json"), browser()],
                                text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)
