"""Focused real Chromium checks for complete browser Print editions."""
from __future__ import annotations
import base64
import ast
import copy
import hashlib
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT/"src/web/browser/shared"
SCRATCH = ROOT/".scratch/web-print-controller-tests"
SCRATCH.mkdir(parents=True,exist_ok=True)
sys.path.insert(0, str(ROOT))
sys.path.insert(0,str(ROOT/"scripts"))
from _web_print_common import structure_sha256
# Reuse the existing CDP harness without importing its real-corpus fixtures:
# These tests do not require a generated browser-product cache.
_test_ast = ast.parse((ROOT/'tools/tests/test_browser_truthfulness.py').read_text())
HARNESS = next(ast.literal_eval(node.value) for node in _test_ast.body if isinstance(node, ast.Assign)
               and any(isinstance(name, ast.Name) and name.id == 'HARNESS' for name in node.targets))


def browser():
    found = os.environ.get('TRIPTYCH_CHROME') or shutil.which('chromium') or shutil.which('google-chrome')
    if not found: raise unittest.SkipTest('Chromium is unavailable')
    return found


def math_font_path():
    from _web_print_assets import font_assets
    try:
        faces=font_assets(ROOT,include_body=True)
    except FileNotFoundError as error:
        raise unittest.SkipTest('Pinned Math font is not hydrated; run the explicit browser-print asset bootstrap before native-font acceptance.') from error
    face=next(face for face in faces if face['family']=='Libertinus Math')
    body=face['body']
    if hashlib.sha256(body).hexdigest()!=face['sha256']:
        raise AssertionError('Math font does not match its source-bound asset record')
    folder=SCRATCH/'fonts';folder.mkdir(exist_ok=True)
    path=folder/(face['sha256']+'.woff2')
    if not path.exists():
        with tempfile.NamedTemporaryFile(dir=folder,delete=False) as handle:
            handle.write(body);temporary=Path(handle.name)
        temporary.replace(path)
    return path.relative_to(ROOT).as_posix()


def source_marks_font_path():
    from _web_print_marks import font_asset
    try:
        face=font_asset(ROOT,include_body=True)
    except FileNotFoundError as error:
        raise unittest.SkipTest('The pinned source-marks font is not hydrated; bootstrap the browser-print assets before native-font acceptance.') from error
    body=face['body']
    if hashlib.sha256(body).hexdigest()!=face['sha256']:
        raise AssertionError('Source-marks font differs from its pinned asset record')
    folder=SCRATCH/'fonts';folder.mkdir(exist_ok=True)
    path=folder/(face['sha256']+'.woff2');path.write_bytes(body)
    return path.relative_to(ROOT).as_posix()


class Text(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.feed(value)
    def handle_data(self, data):
        self.text.append(data)
    def normalized(self):
        return ' '.join(''.join(self.text).split())


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def inventory(values):
    return {'count':len(values),'sha256':sha(json.dumps(values,ensure_ascii=False,separators=(',',':')))}


def compact_descriptor(descriptor):
    descriptor=copy.deepcopy(descriptor)
    descriptor['unit_inventory']=inventory([unit['id'] for unit in descriptor.pop('expected_units')])
    descriptor['coverage_result'].pop('expected_units')
    descriptor['coverage_result']['unit_inventory']=copy.deepcopy(descriptor['unit_inventory'])
    for part in descriptor['parts']:
        part['expected_ids']=inventory(part['expected_ids'])
        part['units']=inventory(part['units'])
    for key in ['sources','source_selection','source_paths','print_unit_expectations']:
        descriptor.pop(key,None)
    return descriptor


def act(expression, name=None):
    return {'do': 'eval', 'expression': expression, **({'name': name} if name else {})}


def wait(expression):
    return {'do': 'wait', 'until': expression}


def drive(plan):
    harness = HARNESS.replace("JSON.parse(process.argv[3])", "JSON.parse(await readFile(process.argv[3], 'utf8'))")
    harness = harness.replace('mkdtemp, readFile, rm', 'mkdtemp, readFile, rm, writeFile')
    harness = harness.replace("? PLAN.responses[relative] : await readFile(file)", "? PLAN.responses[relative] : await readFile(Object.hasOwn(PLAN.files || {}, relative) ? resolve(ROOT, PLAN.files[relative]) : file)")
    harness = harness.replace("? PLAN.responses[relative] : await readFile(repositoryPath(ROOT, file))", "? PLAN.responses[relative] : await readFile(repositoryPath(ROOT, Object.hasOwn(PLAN.files || {}, relative) ? resolve(ROOT, PLAN.files[relative]) : file))")
    harness = harness.replace("join(tmpdir(), 'triptych-truthfulness-')", "join(ROOT, '.scratch/web-print-controller-tests/chrome-')")
    harness = harness.replace("} else if (act.do === 'eval') {", """} else if (act.do === 'click') {
      const point=await evaluate(cdp,`(()=>{const rect=document.querySelector(${JSON.stringify(act.selector)}).getBoundingClientRect();return {x:rect.left+rect.width/2,y:rect.top+rect.height/2};})()`);
      await cdp.send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...point});
      await cdp.send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...point});
    } else if (act.do === 'media') {
      await cdp.send('Emulation.setEmulatedMedia', {media: act.media});
    } else if (act.do === 'network') {
      await cdp.send('Network.enable');
      await cdp.send('Network.setBlockedURLs', {urls:act.urls});
    } else if (act.do === 'platform-fonts') {
      await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
      await cdp.send('DOM.getDocument');
      const expression=(act.frame?"document.querySelector('[data-web-print-frame]').contentDocument":"document")+'.querySelector('+JSON.stringify(act.selector)+')';
      const value=await cdp.send('Runtime.evaluate',{expression,returnByValue:false});
      const node=await cdp.send('DOM.requestNode',{objectId:value.result.objectId});
      seen[act.name]=(await cdp.send('CSS.getPlatformFontsForNode',{nodeId:node.nodeId})).fonts;
      await cdp.send('Runtime.releaseObject',{objectId:value.result.objectId});
    } else if (act.do === 'frame-proof') {
      const available=await evaluate(cdp,"!!document.querySelector('[data-web-print-frame]')");
      if(!available)throw new Error('Cannot capture unprepared edition: '+await evaluate(cdp,"document.querySelector('[data-web-print-status]').textContent"));
      let html = await evaluate(cdp,`(()=>{
        const root=document.querySelector('[data-web-print-document]');
        const assets=JSON.parse(root.querySelector('[data-web-print-manifest]').textContent).assets||[];
        const copy=document.querySelector('[data-web-print-frame]').contentDocument.documentElement.cloneNode(true);
        for(const picture of copy.querySelectorAll('img')){
          const asset=assets.find(asset=>asset.id===picture.dataset.printAsset);
          if(!asset)throw new Error('Capture has an undeclared illustration');
          picture.src=new URL(asset.href,location.href).href;
        }
        return copy.outerHTML;
      })()`);
      let captureFonts=[];
      if(act.captureFonts){
        captureFonts=await evaluate(cdp,"(()=>{const root=document.querySelector('[data-web-print-document]');return JSON.parse(root.querySelector('[data-web-print-manifest]').textContent).fonts.map(font=>({...font,href:new URL(font.href,location.href).href}));})()");
        const css=captureFonts.map(font=>'@font-face{font-family:'+JSON.stringify(font.family)+';src:url('+JSON.stringify(font.href)+');font-weight:'+(font.weight||'400')+';font-style:'+(font.style||'normal')+';'+(font.unicode_range?'unicode-range:'+font.unicode_range+';':'')+'}').join('');
        html=html.replace('</head>','<style data-capture-fonts>'+css+'</style></head>');
      }
      PLAN.responses['validated-print.html']=html;
      await cdp.send('Page.navigate',{url:base+'/validated-print.html'});
      await waitFor(cdp,"document.readyState === 'complete'",'validated print frame');
      await waitFor(cdp,"[...document.images].every(picture=>picture.complete&&picture.naturalWidth>0)",'validated source illustrations');
      if(captureFonts.length){
        const loaded=await evaluate(cdp,`(async()=>{const fonts=${JSON.stringify(captureFonts)};await Promise.all(fonts.map(font=>document.fonts.load((font.style||'normal')+' '+(font.weight||'400')+' 12px '+JSON.stringify(font.family),font.unicode_range==='U+2E4E'?'⹎':font.family==='Triptych Source Marks'?'℟℣↩☐✠':'Test')));await document.fonts.ready;return [...document.fonts].filter(font=>font.status==='loaded').length;})()`);
        if(loaded!==captureFonts.length)throw new Error('Pinned capture fonts did not all load');
      }
      const pdf=await cdp.send('Page.printToPDF',{printBackground:true,displayHeaderFooter:false,preferCSSPageSize:true});
      await writeFile(join(ROOT,'.scratch/web-print-controller-tests',act.name+'.pdf'),Buffer.from(pdf.data,'base64'));
      await writeFile(join(ROOT,'.scratch/web-print-controller-tests',act.name+'.html'),html);
    } else if (act.do === 'eval') {""")
    plan['responses'] = {'shared/web-print.js': (ASSETS/'web-print.js').read_text(),
                         'shared/web-print.css': (ASSETS/'web-print.css').read_text(),
                         **plan.get('responses', {})}
    with tempfile.TemporaryDirectory(dir=SCRATCH) as folder:
        folder = Path(folder)
        (folder/'harness.mjs').write_text(harness)
        (folder/'plan.json').write_text(json.dumps(plan))
        result = subprocess.run(['node', str(folder/'harness.mjs'), str(ROOT), str(folder/'plan.json'), browser()],
                                text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


READY_HOOK = """window.printCalls=0; window.nativeEvents=0;
document.querySelector('[data-web-print-document]').addEventListener('webprintready', event => {
 const frame = event.detail.frame;
 const snapshot = () => {
  const doc=frame.contentDocument;
  window.printSnapshot={units:[...doc.querySelectorAll('[data-print-unit]')].map(n=>n.dataset.printUnit),
   words:doc.body.textContent, images:[...doc.images].map(n=>n.complete&&n.naturalWidth>0),
   fonts:doc.fonts.status, blocked:doc.body.classList.contains('web-print-frame-blocked'),
   details:[...doc.querySelectorAll('details')].map(n=>n.open)};
  window.printSnapshot.tables=doc.querySelectorAll('table').length;
  window.printSnapshot.columns=doc.querySelector('.print-columns')?getComputedStyle(doc.querySelector('.print-columns')).columnCount:null;
  window.printSnapshot.cardFaces=doc.querySelectorAll('.print-card-face').length;
  window.printSnapshot.paperWidth=doc.querySelector('[data-web-print-paper]').getBoundingClientRect().width;
  window.printSnapshot.gridFaces=[...doc.querySelectorAll('.print-card-grid')].map(g=>[...g.children].map(n=>n.dataset.printUnit));
 };
 frame.contentWindow.addEventListener('beforeprint', ()=>{window.nativeEvents++;snapshot();});
 const original=frame.contentWindow.print.bind(frame.contentWindow);
 frame.contentWindow.print=()=>{
  window.printCalls++;
  if(window.useNativePrint) original();
  else {frame.contentWindow.dispatchEvent(new Event('beforeprint'));snapshot();frame.contentWindow.dispatchEvent(new Event('afterprint'));}
 };
});"""


def fixture(inline=False, image=False, font=False, native=False):
    source = sha('Canonical synthetic source')
    selection = sha('Three canonical source units')
    units = [{'id': f'u-{n}', 'source': f'fixture:source#{n}', 'occurrence': '1'} for n in range(1,4)]
    descriptor = {'schema':'triptych-web-print-document/v1','id':'publication:fixture/example','title':'Complete fixture',
                  'edition':'Synthetic edition','revision':'2026-11-02','language':'en','print_type':'flow',
                  'source_digest':source,'selection_digest':selection,'style_sha256':sha((ASSETS/'web-print.css').read_text()),'expected_units':units,
                  'coverage_result':{'status':'pass','output_id':'publication:fixture/example','source_digest':source,
                                     'selection_digest':selection,'expected_units':copy.deepcopy(units)},
                  'parts':[],'assets':[],'fonts':[]}
    responses={}
    bodies=[]
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"><rect x="1" y="1" width="98" height="48" fill="white" stroke="black"/><text x="4" y="26">source figure</text></svg>'
    for n in range(1,4):
        body=(f'<section data-print-part="part-{n}" data-print-document="{descriptor["id"]}" data-print-source="{source}">'
              f'<h2 id="heading-{n}">Unit {n}</h2><section id="u-{n}" data-print-unit="u-{n}">'
              f'<p class="print-callout">Complete canonical body {n}; τέλος. Source qualification retained.</p></section>')
        if n==3 and image:
            body+='<figure><img data-print-asset="diagram" src="/images/diagram.svg" alt="A source-controlled figure"><figcaption>Complete diagram caption.</figcaption></figure>'
        if n==3:
            body+='<footer class="source-apparatus"><p>Exact source rights and revision'+(' ⹎' if font else '')+'.</p></footer>'
        body+='</section>'
        part={'id':f'part-{n}','text_sha256':sha(Text(body).normalized()),'structure_sha256':structure_sha256(body),'expected_ids':[f'heading-{n}',f'u-{n}'],
              'units':[f'u-{n}'],'counts':{'section':1,'p':2 if n==3 else 1,'img':1 if n==3 and image else 0}}
        part.update({'selector':f'[data-print-part="part-{n}"]'} if inline else {'href':f'example/part-{n}.html'})
        descriptor['parts'].append(part)
        responses[f'print/example/part-{n}.html']='<!doctype html><html><body>'+body+'</body></html>'
        bodies.append(body)
    if image:
        descriptor['assets']=[{'id':'diagram','href':'../images/diagram.svg','sha256':sha(svg),'mime':'image/svg+xml'}]
        responses['images/diagram.svg']=svg
    if font:
        path='src/web/browser/shared/fonts/triptych-punctus-elevatus.woff2'
        descriptor['fonts']=[{'family':'Triptych Punctus Elevatus','href':'/'+path,'sha256':sha((ROOT/path).read_bytes()),'unicode_range':'U+2E4E'}]
    root=(f'<div data-web-print-document="{descriptor["id"]}" data-web-print-style="../shared/web-print.css">'
          '<button data-web-print-start>Print</button><button data-web-print-cancel hidden>Cancel</button>'
          '<p data-web-print-status role="status"></p><p data-web-print-notice>Use Print for a complete edition.</p>'
          '<div data-web-print-content>'+(''.join(bodies) if inline else '<p>Edition introduction and period links.</p>')+'</div>'
          '<script type="application/json" data-web-print-manifest>'+json.dumps(descriptor).replace('</','<\\/')+'</script></div>')
    root+=' <script>'+READY_HOOK+('window.useNativePrint=true;' if native else '')+'</script><script src="../shared/web-print.js"></script>'
    # The actual repository page shell proves the print frame stays independent
    # of production reader/navigation styles, without invoking a site build.
    shell=(ROOT/'release/public-alpha/layout.html').read_text()
    fields={'DOCUMENT_TITLE':'Complete fixture','ASSET_PATH':'/release/public-alpha/assets/site.css',
            'HEAD_EXTRA':'<link rel="stylesheet" href="../shared/web-print.css">','CONTENT_ELEMENT':'main',
            'PAGE_CLASS':'page-shell','CONTENT':root,'HOME_PATH':'/','ABOUT_PATH':'/about','CONTRIBUTING_PATH':'/contributing'}
    responses['print/example.html']=re.sub(r'\{\{([A-Z_]+)\}\}',lambda m:fields.get(m[1],''),shell)
    return descriptor,responses


def plan(responses, auto=False):
    return {'responses':responses,'acts':[
        {'do':'navigate','url':'/print/example.html'+('?print=1' if auto else '')},
        wait("window.TriptychWebPrint && document.querySelector('[data-web-print-document]').dataset.webPrintState"),
        *([] if auto else [act("document.querySelector('[data-web-print-start]').click()")]),
        wait("!document.querySelector('[data-web-print-start]').disabled"),
        act("({calls:printCalls,nativeEvents, snapshot:window.printSnapshot,state:document.querySelector('[data-web-print-document]').dataset.webPrintState,status:document.querySelector('[data-web-print-status]').textContent,frames:document.querySelectorAll('[data-web-print-frame]').length})",'result')
    ]}


class ControllerTests(unittest.TestCase):
    def test_verified_cross_part_notes_become_internal_without_stealing_other_citations(self):
        descriptor,responses=fixture();changed=copy.deepcopy(descriptor);path='print/example/part-1.html'
        links=[('part-2.html#heading-%CE%93','Cross-part note'),('/print/example.html#heading-%CE%93','Whole-edition note'),
               ('https://example.org/source.html#heading-%CE%93','External collision'),('../elsewhere.html#heading-%CE%93','Other document collision'),
               ('part-2.html?view=full#heading-%CE%93','Qualified resource'),('part-2.html#missing','Missing destination'),('#heading-1','Same-part note')]
        body='<p>'+''.join('<a href="'+href+'">'+title+'</a> ' for href,title in links)+'</p>'
        responses[path]=responses[path].replace('</section></section>',body+'</section></section>')
        second='print/example/part-2.html';responses[second]=responses[second].replace('id="heading-2"','id="heading-Γ"');changed['parts'][1]['expected_ids'][0]='heading-Γ'
        for index,key in enumerate([path,second]):
            changed['parts'][index].update(text_sha256=sha(Text(responses[key]).normalized()),structure_sha256=structure_sha256(responses[key],'part-'+str(index+1)),counts={})
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact_descriptor(changed)))
        p=plan(responses,auto=True);p['acts'].append(act("[...document.querySelector('[data-web-print-frame]').contentDocument.querySelectorAll('a')].map(n=>({text:n.textContent,href:n.getAttribute('href')}))",'links'))
        observed=drive(p);self.assertEqual(observed['result']['calls'],1,observed)
        values={link['text']:link['href'] for link in observed['links']}
        self.assertEqual(values['Cross-part note'],'#heading-%CE%93')
        self.assertEqual(values['Whole-edition note'],'#heading-%CE%93')
        self.assertEqual(values['Same-part note'],'#heading-1')
        self.assertEqual(values['External collision'],'https://example.org/source.html#heading-%CE%93')
        self.assertTrue(values['Other document collision'].endswith('/print/elsewhere.html#heading-%CE%93'))
        self.assertTrue(values['Qualified resource'].endswith('/print/example/part-2.html?view=full#heading-%CE%93'))
        self.assertTrue(values['Missing destination'].endswith('/print/example/part-2.html#missing'))

    def test_full_width_dictionary_qualification_stays_inside_the_printable_page(self):
        descriptor,responses=fixture();changed=copy.deepcopy(descriptor);changed['print_type']='plates';path='print/example/part-1.html'
        old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
        qualification='This witness establishes no required sanctuary layout. '
        body='<section class="opening-composition"><div class="source-minipage">'+qualification*12+'</div></section>'
        responses[path]=responses[path].replace(old,body)
        changed['parts'][0].update(text_sha256=sha(Text(responses[path]).normalized()),structure_sha256=structure_sha256(responses[path],'part-1'),counts={})
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact_descriptor(changed)))
        p=plan(responses);p['acts'].append(act("const doc=document.querySelector('[data-web-print-frame]').contentDocument;({paper:doc.querySelector('[data-web-print-paper]').getBoundingClientRect().toJSON(),qualification:doc.querySelector('.opening-composition>.source-minipage').getBoundingClientRect().toJSON()})",'bounds'))
        seen=drive(p)
        self.assertEqual(seen['result']['calls'],1,seen)
        self.assertEqual(seen['result']['snapshot']['words'].count(qualification.strip()),12)
        self.assertLessEqual(seen['bounds']['qualification']['right'],seen['bounds']['paper']['right'])
        self.assertGreaterEqual(seen['bounds']['qualification']['left'],seen['bounds']['paper']['left'])

    def test_all_source_marks_require_the_exact_pinned_supplement(self):
        for mutation in ['missing','wrong-range','valid']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture();changed=copy.deepcopy(descriptor);path='print/example/part-1.html'
                responses[path]=responses[path].replace('Complete canonical body 1','Complete source marks ℟ ℣ ↩ ☐ ✠')
                changed['parts'][0].update(text_sha256=sha(Text(responses[path]).normalized()),structure_sha256=structure_sha256(responses[path],'part-1'))
                if mutation!='missing':
                    font_path=source_marks_font_path()
                    changed['fonts']=[{'family':'Triptych Source Marks','href':'/'+font_path,'sha256':sha((ROOT/font_path).read_bytes()),'weight':'400','style':'normal',
                                       'unicode_range':'U+211F,U+2123,U+21A9,U+2610,U+2720' if mutation=='valid' else 'U+211F,U+2123,U+21A9,U+2720'}]
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact_descriptor(changed)))
                p=plan(responses)
                if mutation=='valid':
                    p['acts'].append({'do':'platform-fonts','frame':True,'selector':'.print-callout','name':'actualFonts'})
                    p['acts'].append(act("""(()=>{const doc=document.querySelector('[data-web-print-frame]').contentDocument;
const canvas=doc.createElement('canvas');canvas.width=120;canvas.height=120;const ctx=canvas.getContext('2d');
ctx.fillStyle='#fff';ctx.fillRect(0,0,120,120);ctx.fillStyle='#000';ctx.font="100px 'Triptych Source Marks'";ctx.fillText('☐',10,95);
const pixels=ctx.getImageData(0,0,120,120).data;const dark=(x,y)=>pixels[(y*120+x)*4]<180;const xs=[],ys=[];
for(let y=0;y<120;y++)for(let x=0;x<120;x++)if(dark(x,y)){xs.push(x);ys.push(y);}
if(!xs.length)return {empty:true};const box={left:Math.min(...xs),right:Math.max(...xs),top:Math.min(...ys),bottom:Math.max(...ys)};
const x=Math.floor((box.left+box.right)/2),y=Math.floor((box.top+box.bottom)/2);
const runs=values=>values.reduce((n,v,i)=>n+(v&&(i===0||!values[i-1])?1:0),0);
return {box,centre:[...pixels.slice((y*120+x)*4,(y*120+x)*4+4)],horizontalRuns:runs(Array.from({length:120},(_,a)=>dark(a,y))),verticalRuns:runs(Array.from({length:120},(_,a)=>dark(x,a)))};})()""",'checkbox'))
                observed=drive(p);seen=observed['result']
                self.assertEqual(seen['calls'],1 if mutation=='valid' else 0,seen)
                if mutation=='valid':
                    self.assertIn('℟ ℣ ↩ ☐ ✠',seen['snapshot']['words'])
                    self.assertEqual(seen['snapshot']['fonts'],'loaded')
                    marks=[font for font in observed['actualFonts'] if font['familyName']=='Triptych Source Marks']
                    self.assertTrue(marks,observed['actualFonts'])
                    self.assertTrue(all(font['isCustomFont'] for font in marks))
                    self.assertEqual(sum(font['glyphCount'] for font in marks),5,observed['actualFonts'])
                    self.assertEqual(observed['checkbox']['centre'],[255,255,255,255])
                    self.assertEqual(observed['checkbox']['horizontalRuns'],2)
                    self.assertEqual(observed['checkbox']['verticalRuns'],2)
                    self.assertGreater(observed['checkbox']['box']['right']-observed['checkbox']['box']['left'],60)
                    (SCRATCH/'source-marks-native-proof.json').write_text(json.dumps({
                        'status':'pass','source_marks_sha256':changed['fonts'][0]['sha256'],
                        'unicode_range':changed['fonts'][0]['unicode_range'],'unicode_text':'℟ ℣ ↩ ☐ ✠',
                        'platform_fonts':observed['actualFonts'],'checkbox_canvas':observed['checkbox'],
                        'method':'Actual prepared production-controller frame; native Chromium platform-font attribution and black-on-white canvas. Four Junicode source outlines plus one separately documented project-authored hollow checkbox.'},ensure_ascii=False,indent=2)+'\n')

    def test_source_writing_geometry_has_exact_rules_dimensions_and_complete_inventory(self):
        from collections import Counter
        from _web_print_curriculum.response_geometry import signature, variant, render
        events=[signature(origin) for origin in ['Blank','LongBlank','memory@blankcell','memory@twolines','memory@fourlines','hrulefill']]
        events += [signature('Exercise',height) for height in ['0.22in','0.38in','0.65in','0.7in','0.8in','0.9in','1.0in','1.1in','1.15in','1.2in','1.3in','1.4in']]
        events += [signature('vspace',r'1.1\baselineskip')]
        events += [signature('rule',height) for height in ['0.5in','0.52in','0.55in','0.62in','0.65in','0.72in','0.76in','0.78in','0.82in']]
        proof={'status':'pass','complete':True,'unit_count':len(events),'kinds':dict(Counter(event['kind'] for event in events)),
               'variants':dict(Counter(variant(event) for event in events)),'expected_digest':sha('Independent synthetic geometry plan')}
        for mutation in ['valid','missing-proof','wrong-count','missing-rule','wrong-width','wrong-gap','invisible-rule','orphan']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture();changed=copy.deepcopy(descriptor);changed['print_type']='curriculum'
                path='print/example/part-1.html'
                old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
                body=''.join('<p>Source field: '+render(event,i+1)+'</p>' for i,event in enumerate(events))
                # Two fill fields share the same canonical paragraph and retain
                # positive remaining width without displacing the source labels.
                extra=render(signature('hrulefill'),len(events)+1)+ ' Target worksheet: '+render(signature('hrulefill'),len(events)+2)
                body+='<p>Repeated family: '+extra+'</p>'
                bound=copy.deepcopy(proof);bound['unit_count']+=2;bound['variants']['response-rule']+=2;bound['kinds']['inline-rule']+=2
                changed['response_geometry_coverage']=bound
                if mutation=='missing-proof':changed.pop('response_geometry_coverage')
                if mutation=='wrong-count':bound['variants']['response-rule']-=1
                if mutation=='missing-rule':body=body.replace('<span class="response-ruled-line"></span>','',1)
                if mutation=='orphan':body+='<span class="response-block-022"></span>'
                responses[path]=responses[path].replace(old,body)
                changed['parts'][0].update(text_sha256=sha(Text(responses[path]).normalized()),structure_sha256=structure_sha256(responses[path],'part-1'),counts={})
                if mutation in ['wrong-width','wrong-gap','invisible-rule']:
                    extra_css={'wrong-width':'[data-print-type="curriculum"] .response-blank-short{width:1in}',
                               'wrong-gap':'[data-print-type="curriculum"] .response-lines-2{row-gap:0}',
                               'invisible-rule':'[data-print-type="curriculum"] .response-cell{border-bottom-color:white}'}[mutation]
                    responses['shared/web-print.css']=(ASSETS/'web-print.css').read_text()+extra_css
                    changed['style_sha256']=sha(responses['shared/web-print.css'])
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact_descriptor(changed)))
                p=plan(responses)
                if mutation=='valid':
                    p['acts'].append(act("const doc=document.querySelector('[data-web-print-frame]').contentDocument;const row=[...doc.querySelectorAll('p')].find(n=>n.textContent.startsWith('Repeated family:'));({fills:[...row.querySelectorAll('.response-rule')].map(n=>({x:n.getBoundingClientRect().x,y:n.getBoundingClientRect().y,w:n.getBoundingClientRect().width})),width:row.getBoundingClientRect().width})",'geometry'))
                seen=drive(p)
                self.assertEqual(seen['result']['calls'],1 if mutation=='valid' else 0,seen)
                if mutation=='valid':
                    first,second=seen['geometry']['fills']
                    self.assertGreater(first['w'],1);self.assertGreater(second['w'],1)
                    self.assertAlmostEqual(first['y'],second['y'],delta=1)
                    self.assertGreater(second['x'],first['x']+first['w'])

    def test_reviewed_reader_guard_preserves_screen_body_and_qualifies_native_print(self):
        content=('<div data-web-print-reader><p data-web-print-reader-notice>Use Print to prepare the complete edition.</p>'
                 '<div data-web-print-reader-content><h1>Reviewed reader</h1><p>Existing body and terminal appendix remain visible.</p></div>'
                 '</div><a href="/print/source.html?print=1">Print complete edition</a>')
        shell=(ROOT/'release/public-alpha/layout.html').read_text()
        fields={'DOCUMENT_TITLE':'Reviewed reader','ASSET_PATH':'/release/public-alpha/assets/site.css',
                'HEAD_EXTRA':'<link rel="stylesheet" href="/shared/web-print.css">','CONTENT_ELEMENT':'main',
                'PAGE_CLASS':'page-shell','CONTENT':content,'HOME_PATH':'/','ABOUT_PATH':'/about','CONTRIBUTING_PATH':'/contributing'}
        page=re.sub(r'\{\{([A-Z_]+)\}\}',lambda m:fields.get(m[1],''),shell)
        expression="({body:getComputedStyle(document.querySelector('[data-web-print-reader-content]')).display,notice:getComputedStyle(document.querySelector('[data-web-print-reader-notice]')).display,controller:!!window.TriptychWebPrint,frames:document.querySelectorAll('[data-web-print-frame]').length})"
        p={'responses':{'reader.html':page},'acts':[{'do':'navigate','url':'/reader.html'},wait("document.readyState==='complete'"),act(expression,'screen'),{'do':'media','media':'print'},act(expression,'print')]}
        seen=drive(p)
        self.assertNotEqual(seen['screen']['body'],'none')
        self.assertEqual(seen['screen']['notice'],'none')
        self.assertEqual(seen['print']['body'],'none')
        self.assertNotEqual(seen['print']['notice'],'none')
        self.assertFalse(seen['screen']['controller'])
        self.assertEqual(seen['print']['frames'],0)

    def test_canonical_inline_form_lines_keep_source_widths_and_hfill_geometry(self):
        descriptor,responses=fixture();changed=copy.deepcopy(descriptor);path='print/example/part-1.html'
        old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
        new=('<p class="print-form-field-row">Checker: <span class="print-fill-line print-fill-line-28" data-print-type="write-in-line" '
             'data-semantic-form-line="line-1" data-source-width="0.28\\linewidth" data-source-thickness="0.4pt"></span>'
             '<span class="print-fill-gap" data-print-type="fill-gap" data-semantic-form-line="gap-1"></span>Date: '
             '<span class="print-fill-line print-fill-line-20" data-print-type="write-in-line" '
             'data-semantic-form-line="line-2" data-source-width="0.20\\linewidth" data-source-thickness="0.4pt"></span></p>')
        responses[path]=responses[path].replace(old,new)
        changed['parts'][0].update(text_sha256=sha(Text(responses[path]).normalized()),structure_sha256=structure_sha256(responses[path],'part-1'),counts={'p':1,'span':3})
        compact=compact_descriptor(changed)
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
        p=plan(responses)
        p['acts'].append(act("const doc=document.querySelector('[data-web-print-frame]').contentDocument;const row=doc.querySelector('.print-form-field-row');({row:row.getBoundingClientRect().width,widths:[...row.querySelectorAll('.print-fill-line')].map(n=>n.getBoundingClientRect().width),gap:row.querySelector('.print-fill-gap').getBoundingClientRect().width,thickness:doc.defaultView.getComputedStyle(row.querySelector('.print-fill-line')).borderBottomWidth})",'form'))
        seen=drive(p)
        self.assertEqual(seen['result']['calls'],1,seen)
        self.assertAlmostEqual(seen['form']['widths'][0]/seen['form']['row'],.28,delta=.001)
        self.assertAlmostEqual(seen['form']['widths'][1]/seen['form']['row'],.20,delta=.001)
        self.assertGreater(seen['form']['gap'],0)
        self.assertGreater(float(seen['form']['thickness'].removesuffix('px')),.5)

    def test_source_structure_seals_attributes_math_grouping_and_native_repairs(self):
        for mutation in ['valid','list-start','class','href','math-group','native-repair']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture();changed=copy.deepcopy(descriptor);path='print/example/part-1.html'
                old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
                body='<ol start="2"><li>Complete source item.</li></ol><p class="print-callout">Complete source paragraph.</p><a href="https://example.org/first">Source citation</a>'
                counts={'ol':1,'li':1,'p':1,'a':1}
                if mutation=='math-group':
                    changed['print_type']='curriculum'
                    math='<mrow><munder><mtext>ā</mtext><mo>⏟</mo></munder><mtext>arma</mtext></mrow>'
                    body='<p class="poetry-scansion"><math xmlns="http://www.w3.org/1998/Math/MathML" data-semantic-unit="math-1">'+math+'</math></p>'
                    counts={'p':1,'math':1,'mrow':1,'munder':1,'mtext':2,'mo':1}
                if mutation=='native-repair':
                    body='<p>Complete source table.</p><table><tr><td>Complete source cell.</td></tr></table>'
                    counts={'p':1,'table':1,'tr':1,'td':1}
                canonical=responses[path].replace(old,body)
                changed['parts'][0].update(text_sha256=sha(Text(canonical).normalized()),structure_sha256=structure_sha256(canonical,'part-1'),counts=counts)
                actual=canonical
                if mutation=='list-start':actual=actual.replace('start="2"','start="3"')
                elif mutation=='class':actual=actual.replace('class="print-callout"','class="print-reference"')
                elif mutation=='href':actual=actual.replace('https://example.org/first','https://example.org/second')
                elif mutation=='math-group':actual=actual.replace(math,'<mrow><mtext>ā</mtext><munder><mo>⏟</mo><mtext>arma</mtext></munder></mrow>')
                responses[path]=actual
                compact=compact_descriptor(changed)
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],int(mutation=='valid'),seen)
                if mutation!='valid':self.assertIn('source-structure',seen['status'])

    def test_reader_details_fold_state_is_normalized_only_on_the_print_clone(self):
        for opened in [False,True]:
            with self.subTest(opened=opened):
                descriptor,responses=fixture(inline=True);changed=copy.deepcopy(descriptor);path='print/example/part-1.html'
                old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
                new='<details><summary>Canonical qualification</summary><p>Complete canonical body 1; τέλος. Source qualification retained.</p></details>'
                responses[path]=responses[path].replace(old,new)
                changed['parts'][0].update(text_sha256=sha(Text(responses[path]).normalized()),structure_sha256=structure_sha256(responses[path],'part-1'),counts={'p':1,'details':1,'summary':1})
                compact=compact_descriptor(changed)
                responses['print/example.html']=responses['print/example.html'].replace(old,new).replace(json.dumps(descriptor),json.dumps(compact))
                p=plan(responses)
                p['acts'].insert(2,act('document.querySelector("[data-web-print-content] details").open='+str(opened).lower()))
                p['acts'].append(act('document.querySelector("[data-web-print-content] details").open','readerOpen'))
                seen=drive(p)
                self.assertEqual(seen['result']['calls'],1,seen)
                self.assertEqual(seen['result']['snapshot']['details'],[True])
                self.assertEqual(seen['readerOpen'],opened)

    def test_required_source_glyph_font_is_not_optional(self):
        descriptor,responses=fixture(font=True);changed=copy.deepcopy(descriptor);changed['fonts']=[]
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
        seen=drive(plan(responses))['result']
        self.assertEqual(seen['calls'],0,seen)
        self.assertIn('required source character',seen['status'])

    def test_curriculum_math_poetry_response_space_and_unicode_inventory(self):
        descriptor,responses=fixture();changed=copy.deepcopy(descriptor);changed['print_type']='curriculum'
        font_path=math_font_path()
        changed['fonts']=[{'family':'Libertinus Math','href':'/'+font_path,'sha256':sha((ROOT/font_path).read_bytes()),'weight':'400','style':'normal'}]
        changed['expected_units'][0]['id']='verse-Γ-⛪'
        changed['coverage_result']['expected_units']=copy.deepcopy(changed['expected_units'])
        changed['parts'][0]['units']=['verse-Γ-⛪']
        path='print/example/part-1.html'
        old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
        new='<div class="poetry-source-window" data-poetry-window="1" data-poetry-window-name="PoetryVirgilAeneidOpening"><p class="poetry-verse-line" data-poetry-line="1">Arma virumque cano.</p><math class="poetry-scansion" xmlns="http://www.w3.org/1998/Math/MathML" display="block" data-semantic-unit="scansion-1"><mrow><munder><mtext>ā</mtext><mo>⏟</mo></munder><mtext>arma</mtext></mrow></math></div><span class="response-space response-block-065" data-response-id="response-1" data-response-origin="Exercise" aria-label="Response space"></span>'
        changed['response_geometry_coverage']={'status':'pass','complete':True,'unit_count':1,'kinds':{'response-block':1},'variants':{'response-block-065':1},'expected_digest':sha('Synthetic source Exercise gap')}
        responses[path]=responses[path].replace(old,new).replace('data-print-unit="u-1"','data-print-unit="verse-Γ-⛪"')
        changed['parts'][0]['text_sha256']=sha(Text(responses[path]).normalized())
        changed['parts'][0]['structure_sha256']=structure_sha256(responses[path],'part-1')
        changed['parts'][0]['counts']={'section':1,'p':1,'div':1,'span':1,'math':1,'munder':1,'mrow':1,'mtext':2,'mo':1}
        compact=compact_descriptor(changed)
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
        p=plan(responses)
        p['acts'] += [act("const doc=document.querySelector('[data-web-print-frame]').contentDocument;({height:doc.querySelector('.response-space').getBoundingClientRect().height,mathNamespace:doc.querySelector('math').namespaceURI,poetryMargin:doc.defaultView.getComputedStyle(doc.querySelector('.poetry-verse-line')).marginTop})",'curriculum')]
        seen=drive(p)
        self.assertEqual(seen['result']['calls'],1,seen)
        self.assertEqual(seen['result']['snapshot']['units'],['verse-Γ-⛪','u-2','u-3'])
        self.assertGreaterEqual(seen['curriculum']['height'],62)
        self.assertEqual(seen['curriculum']['mathNamespace'],'http://www.w3.org/1998/Math/MathML')
        self.assertEqual(seen['curriculum']['poetryMargin'],'0px')

    def test_compact_inventory_prepares_every_complete_selected_part(self):
        descriptor,responses=fixture(image=True,font=True)
        compact=compact_descriptor(descriptor)
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
        seen=drive(plan(responses))['result']
        self.assertEqual(seen['calls'],1,seen)
        self.assertEqual(seen['snapshot']['units'],['u-1','u-2','u-3'])
        self.assertEqual(seen['snapshot']['images'],[True])
        self.assertFalse(seen['snapshot']['blocked'])

    def test_compact_inventory_rejects_missing_wrong_order_source_and_coverage(self):
        for mutation in ['part-ids','part-units','root-units','order','source','coverage','missing']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture();compact=compact_descriptor(descriptor)
                if mutation=='part-ids':compact['parts'][0]['expected_ids']['sha256']='0'*64
                elif mutation=='part-units':compact['parts'][0]['units']['sha256']='0'*64
                elif mutation=='root-units':
                    compact['unit_inventory']['sha256']='0'*64
                    compact['coverage_result']['unit_inventory']=copy.deepcopy(compact['unit_inventory'])
                elif mutation=='order':compact['parts'][0],compact['parts'][1]=compact['parts'][1],compact['parts'][0]
                elif mutation=='source':responses['print/example/part-2.html']=responses['print/example/part-2.html'].replace(descriptor['source_digest'],'0'*64)
                elif mutation=='coverage':compact['coverage_result'].pop('unit_inventory')
                else:del responses['print/example/part-2.html']
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['state'],'error')

    def test_compact_inventory_also_refuses_duplicate_units_independent_of_ids(self):
        descriptor,responses=fixture();compact=compact_descriptor(descriptor)
        responses['print/example/part-2.html']=responses['print/example/part-2.html'].replace('data-print-unit="u-2"','data-print-unit="u-1"')
        compact['parts'][1]['structure_sha256']=structure_sha256(responses['print/example/part-2.html'],'part-2')
        compact['parts'][1]['units']=inventory(['u-1'])
        compact['unit_inventory']=inventory(['u-1','u-1','u-3'])
        compact['coverage_result']['unit_inventory']=copy.deepcopy(compact['unit_inventory'])
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(compact))
        seen=drive(plan(responses))['result']
        self.assertEqual(seen['calls'],0,seen)
        self.assertEqual(seen['state'],'error')

    def test_complete_lazy_edition_and_assets_fonts_precede_print(self):
        _,responses=fixture(image=True,font=True)
        p=plan(responses);p['delays']=[{'match':'diagram.svg','ms':150}]
        seen=drive(p)['result']
        self.assertEqual(seen['calls'],1,seen)
        self.assertEqual(seen['snapshot']['units'],['u-1','u-2','u-3'])
        self.assertEqual(seen['snapshot']['images'],[True])
        self.assertEqual(seen['snapshot']['fonts'],'loaded')
        self.assertFalse(seen['snapshot']['blocked'])
        self.assertIn('Exact source rights',seen['snapshot']['words'])

    def test_complete_inline_edition_print_query_and_actual_native_print_events(self):
        _,responses=fixture(inline=True,native=True)
        seen=drive(plan(responses,auto=True))['result']
        self.assertEqual(seen['calls'],1,seen)
        self.assertGreaterEqual(seen['nativeEvents'],1,seen)
        self.assertEqual(seen['snapshot']['units'],['u-1','u-2','u-3'])
        self.assertFalse(seen['snapshot']['blocked'])

    def test_user_mouse_click_opens_native_print_and_own_cycle_stays_ready(self):
        _,responses=fixture(inline=True,native=True)
        p=plan(responses)
        p['acts'][2]={'do':'click','selector':'[data-web-print-start]'}
        p['acts'] += [act("const frame=document.querySelector('[data-web-print-frame]');const root=document.querySelector('[data-web-print-document]');({nativeEvents,ready:TriptychWebPrint.install(root,JSON.parse(root.querySelector('script').textContent)).ready(),blocked:frame.contentDocument.body.classList.contains('web-print-frame-blocked')})",'cycle')]
        seen=drive(p)
        self.assertEqual(seen['result']['calls'],1,seen)
        self.assertGreaterEqual(seen['cycle']['nativeEvents'],1)
        self.assertTrue(seen['cycle']['ready'],seen)
        self.assertFalse(seen['cycle']['blocked'])

    def test_missing_tampered_duplicate_hidden_and_clipped_content_never_prints(self):
        for mutation in ['missing','truncated','duplicate','hidden','visibility-class','clipped','css-hidden','css-white-ink']:
            with self.subTest(mutation=mutation):
                _,responses=fixture()
                path='print/example/part-2.html'
                if mutation=='missing':del responses[path]
                elif mutation=='truncated':responses[path]=responses[path].replace('Complete canonical body 2','Truncated body')
                elif mutation=='duplicate':responses[path]+=responses[path]
                elif mutation=='hidden':responses[path]=responses[path].replace('<section data-print-part','<section hidden data-print-part',1)
                elif mutation=='visibility-class':responses[path]=responses[path].replace('print-callout','visually-hidden')
                else:
                    descriptor=json.loads(responses['print/example.html'].split('data-web-print-manifest>')[1].split('</script>')[0])
                    changed=copy.deepcopy(descriptor)
                    extra={'clipped':'.print-callout{height:1px;overflow:hidden}','css-hidden':'.print-callout{visibility:hidden}','css-white-ink':'.print-callout{color:white}'}[mutation]
                    responses['shared/web-print.css']=(ASSETS/'web-print.css').read_text()+extra
                    changed['style_sha256']=sha(responses['shared/web-print.css'])
                    responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['state'],'error',seen)
                self.assertEqual(seen['frames'],0)

    def test_canonical_coverage_and_exact_selected_output_are_required(self):
        for mutation in ['coverage','selection','units']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture()
                changed=copy.deepcopy(descriptor)
                if mutation=='coverage':changed['coverage_result']['status']='fail'
                elif mutation=='selection':changed['coverage_result']['selection_digest']='0'*64
                else:changed['parts'][-1]['units']=[]
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['state'],'error')

    def test_print_type_profiles_and_stylesheet_pin_are_required(self):
        for mutation in ['wrong-profile','missing-style','changed-style','unsupported']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture();changed=copy.deepcopy(descriptor)
                if mutation=='wrong-profile':changed['print_type']='bible'
                elif mutation=='missing-style':changed.pop('style_sha256')
                elif mutation=='changed-style':changed['style_sha256']='0'*64
                else:changed['availability']='unsupported'
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['state'],'error')

    def test_required_asset_and_font_failures_never_print(self):
        for mutation in ['image-missing','image-hash','font-hash']:
            with self.subTest(mutation=mutation):
                descriptor,responses=fixture(image=True,font=True)
                if mutation=='image-missing':del responses['images/diagram.svg']
                else:
                    changed=copy.deepcopy(descriptor)
                    changed['assets' if mutation=='image-hash' else 'fonts'][0]['sha256']='0'*64
                    responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
                seen=drive(plan(responses))['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['frames'],0)

    def test_cancel_url_change_and_retry_leave_no_partial_edition(self):
        for interrupt in ['cancel','hash','pushstate']:
            with self.subTest(interrupt=interrupt):
                _,responses=fixture()
                p=plan(responses);p['delays']=[{'match':'part-2.html','ms':250}]
                p['acts'].insert(3,wait("document.querySelector('[data-web-print-status]').textContent.includes('part 2')"))
                expression={'cancel':"document.querySelector('[data-web-print-cancel]').click()",'hash':"location.hash='#changed'",'pushstate':"history.pushState({},'', '?changed=1')"}[interrupt]
                p['acts'].insert(4,act(expression))
                seen=drive(p)['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['frames'],0)
                self.assertIn(seen['state'],['cancelled','error'])
        _,responses=fixture();p=plan(responses);p['blocked']=['*part-2.html']
        p['acts'] += [{'do':'network','urls':[]},act("document.querySelector('[data-web-print-start]').click()"),wait("!document.querySelector('[data-web-print-start]').disabled"),act('printCalls','retriedCalls')]
        self.assertEqual(drive(p)['retriedCalls'],1)

    def test_mid_load_root_identity_source_or_metadata_changes_refuse_print(self):
        for mutation in ['identity','source','metadata']:
            with self.subTest(mutation=mutation):
                _,responses=fixture()
                script='<script src="../shared/web-print.js"></script>'
                manual="<script>window.liveDescriptor=JSON.parse(document.querySelector('[data-web-print-manifest]').textContent);TriptychWebPrint.install(document.querySelector('[data-web-print-document]'),liveDescriptor);</script>"
                responses['print/example.html']=responses['print/example.html'].replace(script,script+manual)
                p=plan(responses);p['delays']=[{'match':'part-2.html','ms':200}]
                p['acts'].insert(3,wait("document.querySelector('[data-web-print-status]').textContent.includes('part 2')"))
                expression={'identity':"document.querySelector('[data-web-print-document]').dataset.webPrintDocument='publication:changed'",'source':"liveDescriptor.source_digest='0'.repeat(64)",'metadata':"liveDescriptor.title='Changed selection title'"}[mutation]
                p['acts'].insert(4,act(expression))
                seen=drive(p)['result']
                self.assertEqual(seen['calls'],0,seen)
                self.assertEqual(seen['frames'],0)
                self.assertEqual(seen['state'],'error')

    def test_parent_native_print_never_presents_unprepared_content_as_complete(self):
        _,responses=fixture()
        p=plan(responses);p['acts']=p['acts'][:2]+[
            {'do':'media','media':'print'},act("window.dispatchEvent(new Event('beforeprint'));({content:getComputedStyle(document.querySelector('[data-web-print-content]')).display,notice:getComputedStyle(document.querySelector('[data-web-print-notice]')).display,calls:printCalls})",'guard')]
        seen=drive(p)['guard']
        self.assertEqual(seen['content'],'none')
        self.assertNotEqual(seen['notice'],'none')
        self.assertEqual(seen['calls'],0)

    def test_beforeprint_revalidates_prepared_markup(self):
        _,responses=fixture();p=plan(responses)
        p['acts'] += [act("const frame=document.querySelector('[data-web-print-frame]');frame.contentDocument.querySelector('[data-print-unit]').hidden=true;frame.contentWindow.dispatchEvent(new Event('beforeprint'));frame.contentDocument.body.classList.contains('web-print-frame-blocked')",'blocked')]
        self.assertTrue(drive(p)['blocked'])

    def test_beforeprint_revalidates_loaded_font_metrics(self):
        _,responses=fixture(font=True);p=plan(responses)
        p['acts'] += [act("const frame=document.querySelector('[data-web-print-frame]');const doc=frame.contentDocument;[...doc.fonts][0].sizeAdjust='0%';frame.contentWindow.dispatchEvent(new Event('beforeprint'));doc.body.classList.contains('web-print-frame-blocked')",'blocked')]
        self.assertTrue(drive(p)['blocked'])

    def test_frame_styles_wrappers_transforms_and_overlays_are_frozen_before_print(self):
        for mutation in ['white-ink','stylesheet','scale','overlay','cssom','adopted','animation','fontset']:
            with self.subTest(mutation=mutation):
                _,responses=fixture();p=plan(responses)
                change={'white-ink':"doc.body.style.color='white'",'stylesheet':"doc.head.querySelector('style').textContent+='p{color:white}'",'scale':"doc.querySelector('[data-web-print-paper]').style.transform='scale(0)'",'overlay':"const cover=doc.createElement('div');cover.style.cssText='position:fixed;inset:0;background:white;z-index:99';doc.body.appendChild(cover)", 'cssom':"doc.styleSheets[0].insertRule('p{color:white!important}',0)", 'adopted':"const sheet=new frame.contentWindow.CSSStyleSheet();sheet.replaceSync('p{color:white!important}');doc.adoptedStyleSheets=[sheet]", 'animation':"doc.querySelector('[data-web-print-paper]').animate([{opacity:0},{opacity:0}],{duration:100000})", 'fontset':"doc.fonts.add(new frame.contentWindow.FontFace('Unexpected', 'local(Georgia)'))"}[mutation]
                p['acts'] += [act("const frame=document.querySelector('[data-web-print-frame]');const doc=frame.contentDocument;"+change+";frame.contentWindow.dispatchEvent(new Event('beforeprint'));doc.body.classList.contains('web-print-frame-blocked')",'blocked')]
                self.assertTrue(drive(p)['blocked'])

    def test_landscape_table_and_multicolumn_styles_preserve_all_content(self):
        descriptor,responses=fixture();changed=copy.deepcopy(descriptor);changed['page_format']='letter-landscape'
        path='print/example/part-1.html'
        old='<p class="print-callout">Complete canonical body 1; τέλος. Source qualification retained.</p>'
        new='<table><caption>Source matrix</caption><thead><tr><th scope="col">First source</th><th scope="col">Second source</th></tr></thead><tbody><tr><td>Complete first testimony</td><td>Complete second testimony</td></tr></tbody></table><div class="print-columns"><p>Left column source text.</p><p>Right column source text.</p></div>'
        responses[path]=responses[path].replace(old,new)
        changed['parts'][0]['text_sha256']=sha(Text(responses[path]).normalized())
        changed['parts'][0]['structure_sha256']=structure_sha256(responses[path],'part-1')
        changed['parts'][0]['counts']={'section':1,'p':2,'table':1,'tr':2,'th':2,'td':2}
        responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
        p=plan(responses)
        if os.environ.get('TRIPTYCH_PRINT_CAPTURES')=='1':p['acts'].append({'do':'frame-proof','name':'landscape-table'})
        seen=drive(p)['result']
        self.assertEqual(seen['calls'],1,seen)
        self.assertEqual(seen['snapshot']['tables'],1)
        self.assertEqual(seen['snapshot']['columns'],'2')
        self.assertAlmostEqual(seen['snapshot']['paperWidth'],960,delta=1)
        self.assertIn('Complete second testimony',seen['snapshot']['words'])

    def test_card_fronts_and_mirrored_backs_print_all_faces_or_refuse_overflow(self):
        for overflow in [False,True]:
            with self.subTest(overflow=overflow):
                descriptor,responses=fixture();changed=copy.deepcopy(descriptor);changed['print_type']='cards'
                faces=[(str(n),'front') for n in range(1,7)]+[(str(n),'back') for n in [2,1,4,3,6,5]]
                units=[{'id':f'card-{n}-{side}','source':f'fixture:response-{n}','occurrence':side} for n,side in faces]
                body=f'<section class="print-sheet" data-print-part="deck" data-print-document="{descriptor["id"]}" data-print-source="{descriptor["source_digest"]}">'
                for side in ['front','back']:
                    body+='<div class="print-card-grid" data-print-grid="six">'
                    for n,face in faces:
                        if face!=side:continue
                        key=f'card-{n}-{face}'
                        words=('Excessive source words '*300 if overflow and key=='card-1-front' else f'Complete source {n} {face}.')
                        body+=f'<div id="{key}" data-print-unit="{key}" class="print-card-face print-card-{face}"><h3>{n} {face}</h3><p>{words}</p></div>'
                    body+='</div>'
                body+='</section>'
                changed['expected_units']=units;changed['coverage_result']['expected_units']=copy.deepcopy(units)
                changed['parts']=[{'id':'deck','href':'example/deck.html','text_sha256':sha(Text(body).normalized()),'expected_ids':[u['id'] for u in units],'units':[u['id'] for u in units],'counts':{'.print-card-face':12,'.print-card-front':6,'.print-card-back':6}}]
                responses['print/example/deck.html']='<!doctype html><html><body>'+body+'</body></html>'
                responses['print/example.html']=responses['print/example.html'].replace(json.dumps(descriptor),json.dumps(changed))
                p=plan(responses)
                if not overflow and os.environ.get('TRIPTYCH_PRINT_CAPTURES')=='1':p['acts'].append({'do':'frame-proof','name':'duplex-cards'})
                seen=drive(p)['result']
                if overflow:self.assertEqual(seen['calls'],0,seen)
                else:
                    self.assertEqual(seen['calls'],1,seen)
                    self.assertEqual(seen['snapshot']['cardFaces'],12)
                    self.assertEqual(seen['snapshot']['gridFaces'][1],[f'card-{n}-back' for n in [2,1,4,3,6,5]])


if __name__=='__main__':unittest.main()
