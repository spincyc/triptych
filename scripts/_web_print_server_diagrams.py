#!/usr/bin/env python3
"""Render exact active altar-server diagram macros to self-contained SVG via DVI.

Inventory is source-only. Native tools run only through an explicit render
call, into a required disposable output directory. Canonical macro definitions,
edition branches, artwork and overlays remain the authoring authority.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import shutil
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

REL_OWNER = Path('src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides')
TEX_OWNER = 'liturgy/roman-rite/1962/reference/altar-server-guides'
SVG_NS = 'http://www.w3.org/2000/svg'
XLINK_NS = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG_NS)
ET.register_namespace('xlink', XLINK_NS)
DIAGRAM_FILES = ['low-mass-diagrams.tex', 'sung-mass-diagrams.tex']
CONSUMER_FILES = ['low-mass-ceremony.tex', 'missa-cantata-role-sheets.tex',
                  'missa-cantata-ceremony.tex', 'solemn-role-sheets.tex', 'solemn-ceremony.tex']
MAIN_FILES = ['01-low-mass', '01-low-mass-trainer-manual', '02-missa-cantata', '03-solemn-mass']
VARIANTS = {'child': ('low', r'\LowMassGuidetrue\ChildBookletGuidetrue\ResponseDataOnlyGuidetrue', r'\textwidth'),
            'trainer': ('low', r'\LowMassGuidetrue\TrainerManualGuidetrue\ResponseDataOnlyGuidetrue', r'0.745\textwidth'),
            'sung': ('sung', r'\MissaCantataGuidetrue', r'\textwidth')}



class ServerDiagramError(ValueError):
    """The selected source, output boundary or authoring runtime is unsuitable."""


def canonical_root(root: Path) -> Path:
    """Require the caller's explicit checkout; never infer a neighboring root."""
    root = Path(root).resolve()
    if not (root / 'src/common/preamble.tex').is_file() or not (root / REL_OWNER).is_dir():
        raise ServerDiagramError('explicit root lacks canonical server-guide sources')
    return root


def output_directory(root: Path, out: Path) -> Path:
    """Allow only an explicit checkout-local disposable directory."""
    root = canonical_root(root)
    out = Path(out)
    if not out.is_absolute():
        out = root / out
    out = out.resolve()
    if not out.is_relative_to(root) or out == root:
        raise ServerDiagramError('output must be inside the explicit root')
    relative = out.relative_to(root)
    if '.git' in relative.parts:
        raise ServerDiagramError('output cannot enter repository metadata')
    if not out.is_relative_to(root / '.scratch'):
        try:
            result = subprocess.run(
                ['git', '-C', str(root), 'check-ignore', '--quiet', '--', relative.as_posix()],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
        except OSError as exc:
            raise ServerDiagramError('cannot verify an ignored output directory') from exc
        if result.returncode != 0:
            raise ServerDiagramError('output must be under .scratch or Git-ignored')
    try:
        tracked = subprocess.run(
            ['git', '-C', str(root), 'ls-files', '--', relative.as_posix()],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise ServerDiagramError('cannot verify output against tracked files') from exc
    if tracked.returncode != 0 or tracked.stdout.strip():
        raise ServerDiagramError('output overlaps tracked files')
    return out


def _output_child(out: Path, relative: str) -> Path:
    path = (out / relative).resolve()
    if not path.is_relative_to(out):
        raise ServerDiagramError('output child escapes through a symlink')
    return path


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def group(text: str, start: int) -> tuple[str, int]:
    assert text[start] == '{'
    depth, pos = 1, start + 1
    while depth:
        if pos >= len(text):
            raise ServerDiagramError('unterminated canonical TeX definition')
        if text[pos] == '%' and (pos == 0 or text[pos-1] != '\\'):
            pos = text.find('\n', pos)
            if pos < 0:
                raise ValueError('Unterminated TeX comment')
            continue
        if text[pos] in '{}':
            escapes, p = 0, pos - 1
            while p >= 0 and text[p] == '\\':
                escapes += 1; p -= 1
            if escapes % 2 == 0:
                depth += 1 if text[pos] == '{' else -1
        pos += 1
    return text[start+1:pos-1], pos


def definitions(root: Path, variant: str = 'child') -> dict:
    root = canonical_root(root)
    shared = root / REL_OWNER / 'shared'
    result = {}
    alternatives = {}
    pattern = re.compile(r'\\(?:re)?newcommand\s*\{\\([A-Za-z]+)\}\s*(?:\[\d+\])?\s*(?:\[[^\]]*\])?\s*\{')
    for name in DIAGRAM_FILES:
        source = shared / name
        text = source.read_text()
        for match in pattern.finditer(text):
            body, end = group(text, match.end()-1)
            definition = {'source': rel(root, source), 'line': text.count('\n',0,match.start())+1,
                               'definition_tex': text[match.start():end], 'body': body,
                               'definition_sha256': sha(text[match.start():end].encode())}
            alternatives.setdefault(match[1], []).append(definition)
            result[match[1]] = definition
    # Only these five top-level dimensions have duplicate definitions in the
    # canonical file: the first branch is trainer and the second is child.
    for name, options in alternatives.items():
        if len(options) > 1:
            if name not in {'LMSceneXUnit','LMSceneYUnit','LMPencilSceneHeight','LMPencilPairHeight','LMLavaboHeight'} or len(options) != 2:
                raise ValueError(f'Unhandled conditional/duplicate definition: {name}')
            result[name] = dict(options[0 if variant == 'trainer' else 1])
            result[name]['selected_branch'] = 'trainer' if variant == 'trainer' else 'child'
            result[name]['alternative_definitions'] = [{k:v for k,v in d.items() if k != 'body'} for d in options]
    return result


def inventory(root: Path) -> dict:
    """Discover active canonical diagrams without invoking native tools."""
    root = canonical_root(root)
    owner = root / REL_OWNER
    shared = owner / 'shared'
    defs = definitions(root)
    candidates = {n for n in defs if re.fullmatch(r'LMScene[A-Za-z]+|[A-Za-z]+Diagram', n) and n not in {'LMSceneXUnit','LMSceneYUnit'}}
    uses = {name: [] for name in candidates}
    for fname in CONSUMER_FILES:
        source = shared / fname
        text = source.read_text()
        for match in re.finditer(r'\\([A-Za-z]+)\b', text):
            # Ignore comment-only occurrences; current consumer calls are direct.
            line_begin = text.rfind('\n', 0, match.start()) + 1
            if '%' in text[line_begin:match.start()]:
                continue
            if match[1] in uses:
                uses[match[1]].append({'source': rel(root, source), 'line': text.count('\n', 0, match.start())+1})
    entries = {}
    for macro, usage in sorted(uses.items()):
        if not usage:
            continue
        family = 'low' if macro.startswith('LMScene') else 'sung'
        for variant, (var_family, _, _) in VARIANTS.items():
            if family != var_family:
                continue
            variant_defs = definitions(root, variant)
            direct = dict(variant_defs[macro]); direct.pop('body')
            closure, queue = {}, [macro]
            while queue:
                item = queue.pop()
                if item in closure:
                    continue
                current = variant_defs[item]
                closure[item] = {k: v for k,v in current.items() if k != 'body'}
                queue.extend(n for n in re.findall(r'\\([A-Za-z]+)',current['body']) if n in defs and n not in closure)
            key = f'{variant}:{macro}'
            entries[key] = {'key': key, 'macro': macro, 'variant': variant,
                            'asset': f'assets/{variant}/{macro}.svg', 'usage': usage,
                            'definition': direct, 'definition_closure': closure,
                            'includes_caption': family == 'sung' and macro != 'CommunionPatenSafetyDiagram'}
    source_evidence = [root/'src/common/preamble.tex', shared/'server-guide-format.tex', shared/'low-mass-book-format.tex']
    source_evidence += [shared/f for f in DIAGRAM_FILES + CONSUMER_FILES]
    source_evidence += [owner/f/'main.tex' for f in MAIN_FILES]
    pngs = list((shared/'artwork/pencil').glob('*.png'))
    existing_svg = list(owner.rglob('*.svg'))
    return {'schema_version': 1, 'purpose': 'selected altar-server diagram SVG authoring',
            'pipeline': 'canonical TeX → latex DVI (PGF dvisvgm driver) → dvisvgm path SVG → original PNG byte embedding',
            'source_root': str(REL_OWNER), 'active_macro_count': len({e['macro'] for e in entries.values()}),
            'asset_count': len(entries), 'entries': entries,
            'source_evidence': {rel(root, p):sha(p.read_bytes()) for p in source_evidence},
            'plaintext_svg_search': {'root': str(REL_OWNER), 'existing_svg': [rel(root, p) for p in existing_svg],
                                     'pencil_png_count': len(pngs)},
            'inactive_diagram_macros': sorted(n for n, u in uses.items() if not u and not any(n in e['definition_closure'] for e in entries.values())),
            'indirect_diagram_helpers': sorted(n for n, u in uses.items() if not u and any(n in e['definition_closure'] for e in entries.values())),
            'limitations': [
                'Scope is existing active diagram macros, not full-book page matching, duplex cards, or publication approval.',
                'All figure macros are imported unchanged. Sung macro captions are included inside the SVG.',
                'Glyphs become vector paths. Exact source TeX is retained in definition metadata; SVG text is not selectable.',
                'SVGs retain transparency. Display and print on white, as in the original paper design.',
                'Low-Mass last-Gospel artwork remains the existing schematic TikZ scene; no pencil replacement is invented.',
                'PGF emits an unsupported-fading capability warning while loading the full preamble; active scenes use no fading.',
                'Selected generation needs latex, its canonical packages/fonts, extractbb, and dvisvgm. Serving SVG needs none of them.',
                'Existing historical whole-page print reviews do not validate this renderer or the browser print layout.',
            ]}


def _wrapper(variant: str, macro: str) -> str:
    family, switches, width = VARIANTS[variant]
    setup = '\\input{common/preamble}\n' + f'\\input{{{TEX_OWNER}/shared/server-guide-format}}\n' + switches + '\n'
    if family == 'low':
        setup += f'\\input{{{TEX_OWNER}/shared/low-mass-book-format}}\n'
    setup += f'\\input{{{TEX_OWNER}/shared/{"low" if family=="low" else "sung"}-mass-diagrams}}\n'
    return (r'\PassOptionsToPackage{dvisvgm}{graphicx}'+'\n'+
            r'\PassOptionsToPackage{dvisvgm}{xcolor}'+'\n'+
            r'\def\pgfsysdriver{pgfsys-dvisvgm.def}'+'\n'+setup+
            '\\usepackage[active,tightpage]{preview}\n\\PreviewBorder=0pt\n\\begin{document}\n\\begin{preview}\n'+
            f'\\begin{{minipage}}{{{width}}}\n'+
            ('\\begin{deepstudy}\n' if family == 'sung' else '')+
            '\\typeout{DIAGRAM-LINEWIDTH=\\the\\linewidth}\n'+f'\\{macro}\n'+
            ('\\end{deepstudy}\n' if family == 'sung' else '')+
            '\\end{minipage}\n\\end{preview}\n\\end{document}\n')



def selected_wrapper(root: Path, variant: str, macro: str) -> str:
    """Return the unchanged selected TeX wrapper; never invoke native tools."""
    if f'{variant}:{macro}' not in inventory(root)['entries']:
        raise ServerDiagramError(f'not an active diagram variant: {variant}:{macro}')
    return _wrapper(variant, macro)


def _native_tools() -> dict[str, str]:
    tools = {}
    for name in ('latex', 'dvisvgm', 'extractbb', 'dvitype', 'kpsewhich'):
        path = shutil.which(name)
        if not path:
            raise ServerDiagramError(f'missing selected-render dependency: {name}')
        tools[name] = path
    return tools


def _run(args: list[str], cwd: Path, env: dict, log: str) -> str:
    try:
        proc = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, check=False)
    except OSError as exc:
        raise ServerDiagramError(f'cannot execute {args[0]}') from exc
    _output_child(cwd, log).write_text(proc.stdout)
    if proc.returncode:
        raise ServerDiagramError(f'{args[0]} failed ({proc.returncode}); see {cwd / log}')
    return proc.stdout


def _tool_versions(tools: dict[str, str], env: dict) -> dict:
    result = {}
    for name in ('latex', 'dvisvgm', 'extractbb', 'dvitype'):
        proc = subprocess.run([tools[name], '--version'], stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, env=env, check=True)
        result[name] = proc.stdout.splitlines()[0]
    return result


def _kpse_file(name: str, tools: dict[str, str], env: dict) -> Path | None:
    proc = subprocess.run([tools['kpsewhich'], name], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, env=env, check=False)
    return Path(proc.stdout.strip()).resolve() if proc.returncode == 0 else None


def _vector_font_dependencies(dvi: Path, tools: dict[str, str], env: dict) -> dict:
    proc = subprocess.run([tools['dvitype'], '-output-level=0', str(dvi)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, env=env, check=True)
    names = sorted(set(re.findall(r'Font \d+: ([^ ]+)', proc.stdout)))
    paths = {Path(value).resolve() for value in tools.values()}
    font_map = next((p for n in ('dvisvgm.map', 'ps2pk.map', 'pdftex.map',
                                 'dvipdfm.map', 'psfonts.map')
                     if (p := _kpse_file(n, tools, env))), None)
    if font_map:
        paths.add(font_map)
        lines = font_map.read_text().splitlines()
        for name in names:
            for ext in ('.tfm', '.vf'):
                path = _kpse_file(name + ext, tools, env)
                if path:
                    paths.add(path)
            for line in lines:
                if line.split(' ', 1)[0] not in (name, name + '--base'):
                    continue
                for token in re.findall(r'<+\[?([^\s<>]+)', line):
                    path = _kpse_file(token, tools, env)
                    if path:
                        paths.add(path)
    return {str(p): sha(p.read_bytes()) for p in sorted(paths)}


def _render_warnings(log: str) -> list[str]:
    warnings = re.findall(
        r'(?:(?:Package [^\n]*|LaTeX(?: Font)?) Warning:[\s\S]*?(?=\n\n|\n\())'
        r'|(?:Overfull[^\n]*)|(?:Underfull[^\n]*)', log)
    # Loading the complete canonical preamble declares fadings even though
    # these scenes use none. All other final-pass diagnostics require review.
    unsupported = [warning for warning in warnings if not re.search(
        r'graphic driver pgfsys-dvisvgm\.def does not support fa\s*dings\.', warning)]
    if unsupported or 'Missing character:' in log:
        raise ServerDiagramError('unresolved selected-render diagnostics; see selected.log')
    return [warning.strip() for warning in warnings]


def render(root: Path, variant: str, macro: str, out: Path) -> dict:
    """Explicitly render one canonical active variant into disposable output.

    No native work occurs through inventory, wrapper selection, or import.
    Normal browser builds use the separately verified immutable asset delivery.
    """
    root = canonical_root(root)
    catalog = inventory(root)
    key = f'{variant}:{macro}'
    if key not in catalog['entries']:
        raise ServerDiagramError(f'not an active diagram variant: {key}')
    entry = catalog['entries'][key]
    out = output_directory(root, out)
    job = _output_child(out, f'jobs/{variant}--{macro}')
    target = _output_child(out, entry['asset'])
    # Verify every file this routine writes before launching the authoring tools.
    for name in ('selected.tex', 'selected.aux', 'selected.log', 'selected.out',
                 'selected.fls', 'selected.dvi', 'raw.svg', 'receipt.json',
                 'latex-pass-1.stdout', 'latex-pass-2.stdout', 'dvisvgm.stdout'):
        _output_child(job, name)
    tools = _native_tools()
    repository_dependencies = dict(catalog['source_evidence'])
    artwork_pattern = re.compile(re.escape(TEX_OWNER) + r'/shared/artwork/pencil/[A-Za-z0-9._-]+\.png')
    for definition in entry['definition_closure'].values():
        for name in artwork_pattern.findall(definition['definition_tex']):
            artwork = (root / 'src/gpt' / name).resolve()
            artwork.relative_to(root / REL_OWNER / 'shared/artwork/pencil')
            repository_dependencies[rel(root, artwork)] = sha(artwork.read_bytes())
    job.mkdir(parents=True, exist_ok=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    # A failed explicit refresh must not leave an earlier receipt claiming it.
    (job / 'receipt.json').unlink(missing_ok=True)
    (job / 'selected.tex').write_text(_wrapper(variant, macro))
    env = dict(os.environ)
    env.update({'TEXINPUTS': f'{root}/src/gpt/:{root}/src/:',
                'SOURCE_DATE_EPOCH': '0', 'FORCE_SOURCE_DATE': '1', 'TZ': 'UTC',
                'TEXMFOUTPUT': str(job), 'TMPDIR': str(job)})
    latex_cmd = [tools['latex'], '-interaction=nonstopmode', '-halt-on-error',
                 '-shell-restricted', '-recorder', 'selected.tex']
    _run(latex_cmd, job, env, 'latex-pass-1.stdout')
    _run(latex_cmd, job, env, 'latex-pass-2.stdout')
    svg_cmd = [tools['dvisvgm'], '--no-fonts', '--embed-bitmaps', '--precision=6',
               '--cache=none', '--no-mktexmf', '--output=raw.svg', 'selected.dvi']
    svg_output = _run(svg_cmd, job, env, 'dvisvgm.stdout')
    if '1 of 1 page converted' not in svg_output:
        raise ServerDiagramError('selected macro did not yield exactly one DVI page')
    if re.search(r'warning|error|not found|unsupported', svg_output, re.IGNORECASE):
        raise ServerDiagramError('SVG backend reported an unresolved warning; see dvisvgm.stdout')
    tree = ET.parse(job / 'raw.svg')
    svg = tree.getroot()
    embedded = []
    for elem in svg.iter(f'{{{SVG_NS}}}image'):
        href = elem.get(f'{{{XLINK_NS}}}href') or elem.get('href')
        if not href or href.startswith('data:'):
            raise ServerDiagramError(f'unexpected bitmap href {href!r}')
        path = (root / 'src/gpt' / href).resolve()
        path.relative_to(root / REL_OWNER / 'shared/artwork/pencil')
        data = path.read_bytes()
        elem.set(f'{{{XLINK_NS}}}href', 'data:image/png;base64,' + base64.b64encode(data).decode())
        embedded.append({'source': rel(root, path), 'sha256': sha(data), 'bytes': len(data)})
    title = ET.Element(f'{{{SVG_NS}}}title')
    title.text = f'\\{macro} ({variant})'
    svg.insert(0, title)
    svg.set('role', 'img')
    tree.write(target, encoding='utf-8', xml_declaration=True)
    for elem in svg.iter():
        href = elem.get(f'{{{XLINK_NS}}}href') or elem.get('href')
        if href and not (href.startswith('#') or href.startswith('data:image/png;base64,')):
            raise ServerDiagramError('selected SVG still references an external resource')
    latex_log = (job / 'selected.log').read_text()
    warnings = _render_warnings(latex_log)
    tool_dependencies = {}
    for line in (job / 'selected.fls').read_text().splitlines():
        if not line.startswith('INPUT '):
            continue
        path = Path(line[6:])
        if not path.is_absolute():
            path = job / path
        path = path.resolve()
        if not path.is_file() or path.is_relative_to(out):
            continue
        if path.is_relative_to(root):
            repository_dependencies.setdefault(rel(root, path), sha(path.read_bytes()))
        else:
            tool_dependencies[str(path)] = sha(path.read_bytes())
    for item in embedded:
        expected = repository_dependencies.setdefault(item['source'], item['sha256'])
        if item['sha256'] != expected:
            raise ServerDiagramError('canonical artwork changed during selected render')
    for name, expected in repository_dependencies.items():
        if sha((root / name).read_bytes()) != expected:
            raise ServerDiagramError(f'canonical dependency changed during selected render: {name}')
    tool_dependencies.update(_vector_font_dependencies(job / 'selected.dvi', tools, env))
    receipt = {
        **entry,
        'schema': 'triptych-server-diagram-render/v1',
        'renderer_sha256': sha(Path(__file__).read_bytes()),
        'source_evidence': catalog['source_evidence'],
        'repository_dependencies': dict(sorted(repository_dependencies.items())),
        'toolchain_dependencies': dict(sorted(tool_dependencies.items())),
        'tool_versions': _tool_versions(tools, env),
        'commands': [latex_cmd, latex_cmd, svg_cmd],
        'svg_sha256': sha(target.read_bytes()), 'svg_bytes': target.stat().st_size,
        'embedded_artwork': embedded, 'embedded_artwork_byte_identity': True,
        'viewBox': svg.get('viewBox'), 'width': svg.get('width'), 'height': svg.get('height'),
        'linewidth': re.search(r'DIAGRAM-LINEWIDTH=([^\n]+)', latex_log)[1],
        'warnings': [w.strip() for w in warnings],
        'dvi_pages': 1, 'pdf_files_generated': [],
        'job': job.relative_to(out).as_posix(),
    }
    (job / 'receipt.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='explicit canonical checkout root')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list', help='list active variant:macro keys from source; no native tools')
    commands.add_parser('inventory', help='emit source inventory JSON; no native tools or writes')
    render_parser = commands.add_parser('render', help='explicitly render one selected diagram via DVI')
    render_parser.add_argument('--variant', choices=VARIANTS, required=True)
    render_parser.add_argument('--macro', required=True)
    render_parser.add_argument('--out', type=Path, required=True,
                               help='required output directory under .scratch or Git-ignored')
    args = parser.parse_args(argv)
    try:
        if args.command == 'render':
            result = render(args.root, args.variant, args.macro, args.out)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            result = inventory(args.root)
            if args.command == 'list':
                print('\n'.join(result['entries']))
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(2, f'server-diagram authoring refused: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
