"""Explicit-scope browser checks; qualitative reader review remains separate."""
from __future__ import annotations
import argparse
import base64
import functools
import hashlib
import http.server
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'triptych-history-browser-plan/v1'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inside(root, value):
    path = Path(value)
    path = path if path.is_absolute() else root / path
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes selected repository root')
    return path

def owned_output(root, value):
    path = inside(root,value)
    scratch = root / '.scratch'
    if not path.resolve().is_relative_to(scratch.resolve()) or path.resolve()==scratch.resolve():
        raise ValueError('output must be a dedicated directory below repository .scratch')
    parent = path
    while parent != root:
        if parent.is_symlink():
            raise ValueError('output path must not contain symlinks')
        parent = parent.parent
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise ValueError('output must be new or empty; prior evidence is never overwritten')
    return path

def local_url(value):
    parsed = urllib.parse.urlsplit(value)
    try:
        local = ipaddress.ip_address(parsed.hostname or '').is_loopback
    except ValueError:
        local = parsed.hostname=='localhost'
    if parsed.scheme!='http' or not local or parsed.username or parsed.password or parsed.fragment or not parsed.path.endswith('/history/'):
        raise ValueError('URL must be unauthenticated loopback HTTP ending /history/')
    return parsed

def descriptors(stage):
    return stage.get('text_projections') or ([stage] if stage.get('text_binding') else [])

def siblings_preserved(before, after, selected):
    def others(rows):
        return {row['binding']:(row['open'],row['units']) for row in rows if row['binding']!=selected}
    return others(before)==others(after)

def validate_plan(plan, catalogue, raw):
    if plan.get('schema')!=SCHEMA or plan.get('catalogue_sha256')!=digest(raw):
        raise ValueError('plan schema or frozen catalogue digest does not match')
    tables = {key:catalogue[table] for key,table in [('entries','entries'),('groups','presentation_groups'),('native_bindings','native_texts'),('comparisons','comparisons')]}
    tables.update({key:catalogue['stage_history'][key] for key in ['stages','transitions']})
    selected = 0
    for key,rows in tables.items():
        values = plan.get(key,[])
        available = {r['adapter_id'] if key=='native_bindings' else r['id'] for r in rows}
        if not isinstance(values,list) or any(not isinstance(v,str) for v in values) or len(values)!=len(set(values)) or not set(values)<=available:
            raise ValueError('unknown or duplicate identities in '+key)
        selected += len(values)
    if not selected:
        raise ValueError('plan must select actual records or payloads')
    return plan

class Browser:
    def __init__(self, root, out, url, site):
        self.root,self.out,self.url,self.site = root,out,url,site
        self.server=self.driver=self.session=self.fd=self.log=None
        self.checks,self.requests,self.resources=[],[],{}
    def save(self,name,value):
        (self.out/(name+'.json')).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    def check(self,name,value,detail=None):
        self.checks.append({'name':name,'pass':bool(value),'detail':detail})
        self.save('checks',self.checks)
    def fetch(self,path):
        address=urllib.parse.urljoin(self.url,path)
        with urllib.request.urlopen(address,timeout=45) as response:
            data=response.read()
        self.resources[urllib.parse.urlsplit(address).path]={'sha256':digest(data),'byte_size':len(data)}
        return data
    def request(self,method,path,data=None):
        request=urllib.request.Request(self.driver_url+path,method=method,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=45) as response:
            value=json.load(response)['value']
        if isinstance(value,dict) and 'error' in value:
            raise RuntimeError(value.get('message',value['error']))
        return value
    def call(self,method,path,data=None):
        return self.request(method,'/session/'+self.session+path,data)
    def js(self,script,*args):
        return self.call('POST','/execute/sync',{'script':script,'args':list(args)})
    def cdp(self,method,params):
        return self.call('POST','/goog/cdp/execute',{'cmd':method,'params':params})
    def key(self,value):
        self.call('POST','/actions',{'actions':[{'type':'key','id':'acceptance','actions':[{'type':'keyDown','value':value},{'type':'keyUp','value':value}]}]})
    def wait(self,script,*args):
        for _ in range(240):
            if self.js(script,*args): return
            time.sleep(.025)
        raise RuntimeError('browser state did not settle')
    def navigate(self,view='timeline',fragment='',width=1440):
        self.cdp('Emulation.setDeviceMetricsOverride',{'width':width,'height':900,'deviceScaleFactor':1,'mobile':False})
        self.call('POST','/url',{'url':self.url.split('?')[0]+'?view='+view+fragment})
        self.wait('return document.querySelector(arguments[0])?.getAttribute("aria-busy")==="false"','#catalogue-results' if view=='catalogue' else '#timeline-chart')
        self.js('document.documentElement.style.fontSize="";document.documentElement.style.scrollBehavior="auto"')
    def capture(self,name,selector,index=0):
        self.js('document.querySelectorAll(arguments[0])[arguments[1]].scrollIntoView({block:"start",behavior:"instant"})',selector,index)
        time.sleep(.1)
        geometry=self.js('const e=document.querySelectorAll(arguments[0])[arguments[1]],r=e.getBoundingClientRect();return {clip:{x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:Math.min(r.height,1200),scale:1},text:e.textContent,viewport:{width:innerWidth,height:innerHeight}}',selector,index)
        self.save(name+'-geometry',geometry)
        data=self.cdp('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,'clip':geometry['clip']})
        (self.out/(name+'.png')).write_bytes(base64.b64decode(data['data']))
    def start(self):
        parsed=local_url(self.url)
        if parsed.port==0:
            if not self.site: raise ValueError('port zero requires --site')
            owner=self
            class Quiet(http.server.SimpleHTTPRequestHandler):
                def log_request(self,code='-',size='-'): owner.requests.append({'path':self.path,'status':code})
                def log_message(self,*_): pass
            self.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(self.site)))
            threading.Thread(target=self.server.serve_forever,daemon=True).start()
            self.url=urllib.parse.urlunsplit(('http','127.0.0.1:'+str(self.server.server_port),parsed.path,parsed.query,''))
        temporary=self.out/'tmp'
        temporary.mkdir()
        # The descriptor alias shortens Unix socket names; files stay in owned scratch.
        self.fd=os.open(temporary,os.O_RDONLY|os.O_DIRECTORY)
        environment=dict(os.environ,TMPDIR=f'/proc/{os.getpid()}/fd/{self.fd}')
        self.log=(self.out/'chromedriver.log').open('w')
        self.driver=subprocess.Popen(['/usr/bin/chromedriver','--port=0'],stdout=self.log,stderr=subprocess.STDOUT,env=environment)
        for _ in range(100):
            match=re.search(r'started successfully on port (\d+)',(self.out/'chromedriver.log').read_text())
            if match:
                self.driver_url='http://127.0.0.1:'+match[1]
                break
            if self.driver.poll() is not None: raise RuntimeError('ChromeDriver startup failed; inspect owned log')
            time.sleep(.05)
        else: raise RuntimeError('ChromeDriver did not report its port')
        session=self.request('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'chrome','goog:chromeOptions':{'binary':'/usr/bin/chromium','args':['--headless=new','--no-sandbox','--disable-dev-shm-usage','--window-size=1440,900','--user-data-dir='+str(self.out/'profile')]},'goog:loggingPrefs':{'browser':'ALL'}}}})
        self.session=session['sessionId']
        self.save('environment',{'browser':session['capabilities']['browserVersion'],'driver':session['capabilities']['chrome']['chromedriverVersion']})
    def close(self):
        if self.session:
            try: self.call('DELETE','')
            except Exception: pass
        if self.driver:
            self.driver.terminate()
            try: self.driver.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.driver.kill()
                self.driver.wait()
        if self.log: self.log.close()
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.fd is not None: os.close(self.fd)

def exercise(b,catalogue,raw,plan,source):
    history=catalogue['stage_history']
    b.check('fresh-served-catalogue',b.fetch('../browse/structure/act-history/catalogue.json')==raw)
    pins=[]
    for item in catalogue['inputs']:
        data=inside(b.root,item['path']).read_bytes()
        pins.append({'path':item['path'],'sha256':digest(data),'byte_size':len(data)})
    b.check('fresh-source-owners',all(p['sha256']==r['sha256'] and p['byte_size']==r['byte_size'] for p,r in zip(pins,catalogue['inputs'])))
    runtime=[]
    for route,path in [('history.js','src/web/browser/history/history.js'),('history.css','src/web/browser/history/history.css'),('../shared/browser-core.js','src/web/browser/shared/browser-core.js'),('../shared/browser-core.css','src/web/browser/shared/browser-core.css'),('../assets/site.css','release/public-alpha/assets/site.css')]:
        data=inside(b.root,path).read_bytes()
        served=b.fetch(route)
        runtime.append({'path':path,'source_sha256':digest(data),'served_sha256':digest(served)})
    html=b.fetch('./')
    b.check('fresh-runtime',all(r['source_sha256']==r['served_sha256'] for r in runtime))
    if b.site: b.check('fresh-built-html',html==(b.site/'history/index.html').read_bytes())
    b.save('identity',{'catalogue_sha256':digest(raw),'helper_sha256':digest(Path(__file__).read_bytes()),'plan_sha256':digest(json.dumps(plan,sort_keys=True).encode()),'runtime':runtime,'html_sha256':digest(html),'source_owners':pins})
    if any(not r['pass'] for r in b.checks): raise ValueError('fresh identity guard failed; tasks not run')
    entries={r['id']:r for r in catalogue['entries']}
    if plan.get('entries'): b.navigate('catalogue')
    for index,identifier in enumerate(plan.get('entries',[])):
        row=entries[identifier]
        target='catalogue-entry-'+identifier
        b.js('document.getElementById(arguments[0]).focus()',target)
        b.key('\ue007')
        b.wait('return document.activeElement.id==="catalogue-detail"')
        result=b.js('const d=document.querySelector("#catalogue-detail"),a=[...d.querySelectorAll(".catalogue-facts dt")],v=[...d.querySelectorAll(".catalogue-facts dd")];return {title:d.querySelector(".panel-title").textContent,facts:Object.fromEntries(a.map((e,i)=>[e.textContent,v[i].textContent])),original:JSON.parse(d.querySelector("pre").textContent)}')
        expected={'Record group':row['presentation_group']['label'],'Date as recorded':row['date_label'],'Evidence status':row['evidence_status'],'Source acquisition':row['acquisition_status'],'Text status':row['text_status'],'Substantive-version status':row['substantive_status']}
        expected={k:('Not recorded' if v is None or v=='' else str(v)) for k,v in expected.items()}
        if row.get('chronology'): expected['Date interpretation']=' · '.join(row['chronology'].get(k,'') for k in ['kind','certainty'] if row['chronology'].get(k))
        b.check('record:'+identifier,result['title']==row['title'] and result['original']==row['source_record'] and all(result['facts'].get(k)==v for k,v in expected.items()),result['facts'])
        if index in (0,len(plan['entries'])-1): b.capture('record-'+str(index+1),'#catalogue-detail')
        b.js('document.querySelector("#catalogue-detail > button").focus()')
        b.key('\ue007')
        b.check('record-keyboard-return:'+identifier,b.js('return document.activeElement.id')==target)
    groups={r['id']:r for r in catalogue['presentation_groups']}
    if plan.get('groups'): b.navigate('catalogue',width=320)
    for identifier in plan.get('groups',[]):
        row=groups[identifier]
        b.js('const e=document.querySelector("#catalogue-family");e.value=arguments[0];e.dispatchEvent(new Event("change",{bubbles:true}))','group:'+identifier)
        b.wait('return document.querySelector("#catalogue-status").textContent.startsWith(arguments[0])',str(row['count'])+' of ')
        result=b.js('return {label:document.querySelector("#catalogue-family").selectedOptions[0].textContent,count:document.querySelectorAll("#catalogue-results .catalogue-title").length}')
        b.check('group:'+identifier,result=={'label':row['label'],'count':row['count']},result)
    for kind,table in [('stage','stages'),('transition','transitions')]:
        rows={r['id']:r for r in history[table]}
        for identifier in plan.get(table,[]):
            row=rows[identifier]
            for mode in ['chart','list']:
                b.navigate(fragment='#'+urllib.parse.urlencode({kind:identifier,'presentation':mode,'leads':'1'}))
                expected='Selected state: '+row['label']+'; '+row['date_label'] if kind=='stage' else 'Selected transition: '+row['summary']
                b.wait('return document.querySelector("#timeline-detail").getAttribute("aria-label")===arguments[0]',expected)
                text=b.js('return document.querySelector("#timeline-detail").textContent')
                b.check(kind+':'+identifier+':'+mode,all(e.get('locus','') in text for e in row.get('evidence',[])))
                b.js('document.querySelector("#timeline-detail > button").focus()')
                b.key('\ue007')
                returned=b.js('return {stage:document.activeElement.dataset.stage,transition:document.activeElement.dataset.transition,id:document.activeElement.id}')
                b.check(kind+'-keyboard-return:'+identifier+':'+mode,returned.get(kind)==identifier or returned['id']=='timeline-'+mode+'-'+kind+'-'+identifier,returned)
                b.key('\ue007')
                b.wait('return document.activeElement.id==="timeline-detail"')
                b.check(kind+'-keyboard-open:'+identifier+':'+mode,b.js('return document.querySelector("#timeline-detail").getAttribute("aria-label")')==expected)
            b.capture(kind+'-'+re.sub('[^a-zA-Z0-9_-]','-',identifier),'#timeline-detail')
    native={r['adapter_id']:r for r in catalogue['native_texts']}
    for binding in plan.get('native_bindings',[]):
        declaration=native[binding]
        stage=next(r for r in history['stages'] if any(d['text_binding']==binding for d in descriptors(r)))
        b.navigate(fragment='#'+urllib.parse.urlencode({'stage':stage['id'],'presentation':'list','leads':'1'}))
        selector='.native-text-fold[data-text-binding="'+binding+'"]'
        b.wait('return !!document.querySelector(arguments[0])',selector)
        order=b.js('return [...document.querySelectorAll("#timeline-detail .native-text-fold")].map(e=>e.dataset.textBinding)')
        b.check('native-order:'+binding,order==[d['text_binding'] for d in descriptors(stage)],order)
        data=b.fetch('../browse/structure/act-history/'+declaration['projection_path'])
        payload=json.loads(data)
        b.check('native-source-served:'+binding,data==(b.root/'src/web/data/structure/act-history'/declaration['projection_path']).read_bytes())
        b.check('native-lazy:'+binding,b.js('return !document.querySelector(arguments[0]).open&&!document.querySelector(arguments[0]).querySelector(".native-text-body")',selector))
        b.check('native-not-prefetched:'+binding,b.js('return !performance.getEntriesByType("resource").some(e=>e.name.endsWith(arguments[0]))','/structure/act-history/'+declaration['projection_path']))
        sibling_script='return [...document.querySelectorAll("#timeline-detail .native-text-fold")].map(e=>({binding:e.dataset.textBinding,open:e.open,units:e.querySelectorAll(".native-text-body").length}))'
        siblings_before=b.js(sibling_script)
        b.js('document.querySelector(arguments[0]).querySelector("summary").focus()',selector)
        b.key('\ue007')
        b.wait('return document.querySelector(arguments[0]).querySelectorAll(".native-text-body").length===arguments[1]',selector,len(payload['units']))
        siblings_after=b.js(sibling_script)
        b.check('native-siblings-preserved:'+binding,siblings_preserved(siblings_before,siblings_after,binding),{'before':siblings_before,'after':siblings_after})
        rendered=b.js('const e=document.querySelector(arguments[0]);return {extent:e.querySelector(".native-text-extent").textContent,scope:e.querySelector(".native-text-scope").textContent,units:[...e.querySelectorAll(".native-text-unit")].map(n=>{const t=n.querySelector(".native-text-body");return {id:t.dataset.unitId,text:t.textContent,language:t.lang,direction:t.dir,locus:n.querySelector(".native-text-source").textContent}})}',selector)
        b.check('native-text:'+binding,len(rendered['units'])==len(payload['units']) and all(all(a[k]==u[v] for k,v in [('id','unit_id'),('text','text'),('language','language'),('direction','direction')]) for a,u in zip(rendered['units'],payload['units'])))
        b.check('native-loci:'+binding,all(u['source_locator'] in a['locus'] for a,u in zip(rendered['units'],payload['units'])))
        coverage='complete' if payload['scope']['whole_book_complete'] else 'partial'
        b.check('native-coverage:'+binding,rendered['scope']==payload['scope']['description'] and ('Whole-book text coverage: '+coverage+'.') in rendered['extent'] and stage['text_coverage']==coverage,{'binding_whole_book_complete':payload['scope']['whole_book_complete'],'stage_text_coverage':stage['text_coverage'],'expected':coverage})
        safe=binding.removeprefix('native-book:')
        b.capture('native-'+safe+'-scope',selector)
        for index in sorted({0,len(payload['units'])//2,len(payload['units'])-1}): b.capture('native-'+safe+'-unit-'+str(index+1),selector+' .native-text-unit',index)
        b.cdp('Emulation.setDeviceMetricsOverride',{'width':320,'height':900,'deviceScaleFactor':1,'mobile':False})
        b.js('document.documentElement.style.fontSize="200%"')
        b.check('native-narrow:'+binding,b.js('return document.documentElement.clientWidth===document.documentElement.scrollWidth'))
        b.capture('native-'+safe+'-narrow',selector)
    comparisons={r['id']:r for r in catalogue['comparisons']}
    for identifier in plan.get('comparisons',[]):
        row=comparisons[identifier]
        transition=next((r for r in history['transitions'] if identifier in r.get('comparison_ids',[])),None)
        if transition:
            b.navigate(fragment='#'+urllib.parse.urlencode({'transition':transition['id'],'presentation':'list','leads':'1'}))
            index=transition['comparison_ids'].index(identifier)
            selector='#timeline-detail .comparison-fold'
        else:
            b.navigate('catalogue')
            index=catalogue['comparisons'].index(row)
            selector='#catalogue-comparison-list .comparison-fold'
        b.js('document.querySelectorAll(arguments[0])[arguments[1]].querySelector("summary").focus()',selector,index)
        b.key('\ue007')
        b.wait('return document.querySelectorAll(arguments[0])[arguments[1]].querySelectorAll(".held-text").length===2',selector,index)
        data=b.fetch('../browse/structure/act-history/'+row['projection_path'])
        payload=json.loads(data)
        result=b.js('const e=document.querySelectorAll(arguments[0])[arguments[1]];return {words:[...e.querySelectorAll(".held-text")].map(n=>n.textContent),text:e.textContent,caveat:e.querySelector(".comparison-caveat").textContent}',selector,index)
        b.check('comparison:'+identifier,result['words']==[payload['left']['joined_source_text'],payload['right']['joined_source_text']] and result['caveat']==payload['apparatus_caveat'] and payload['unified_diff'] in result['text'])
        b.check('comparison-source-served:'+identifier,data==(b.root/'src/web/data/structure/act-history'/row['projection_path']).read_bytes())
        b.capture('comparison-'+identifier,selector,index)
    b.check('final-catalogue-stable',b.fetch('../browse/structure/act-history/catalogue.json')==raw and source.read_bytes()==raw)
    b.check('final-owners-stable',all(digest(inside(b.root,p['path']).read_bytes())==p['sha256'] for p in pins))
    log=b.call('POST','/log',{'type':'browser'})
    b.save('browser-log',log)
    b.check('no-console-errors',not [r for r in log if r['level']=='SEVERE' and 'favicon.ico' not in r['message']])
    b.check('no-local-http-errors',not [r for r in b.requests if isinstance(r['status'],int) and r['status']>=400 and urllib.parse.urlsplit(r['path']).path!='/favicon.ico'])
    b.save('served-resources',b.resources)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',required=True,help='loopback URL ending /history/; port0 starts an owned --site server')
    parser.add_argument('--catalogue',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path,help='new or empty repository .scratch directory')
    parser.add_argument('--plan',required=True,type=Path,help='explicit identities and frozen catalogue SHA256')
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--site',type=Path)
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args(argv)
    browser=None
    try:
        root=args.root.resolve()
        local_url(args.url)
        source=inside(root,args.catalogue)
        raw=source.read_bytes()
        catalogue=json.loads(raw)
        plan=validate_plan(json.loads(inside(root,args.plan).read_text()),catalogue,raw)
        out=owned_output(root,args.out)
        site=inside(root,args.site).resolve() if args.site else None
        if site and not (site/'history/index.html').is_file(): raise ValueError('preview history route is missing')
        out.mkdir(parents=True,exist_ok=True)
        browser=Browser(root,out,args.url,site)
        browser.start()
        exercise(browser,catalogue,raw,plan,source)
        status=int(any(not r['pass'] for r in browser.checks))
        result={'v':1,'status':'pass' if status==0 else 'fail','checks':len(browser.checks),'failures':sum(not r['pass'] for r in browser.checks),'exit_status':status,'catalogue_sha256':digest(raw),'qualitative_reader_judgment':'separate review required'}
        browser.save('summary',result)
        print(json.dumps(result,sort_keys=True,separators=(',',':')))
        return status
    except (ValueError,OSError,json.JSONDecodeError) as error:
        result={'v':1,'status':'error','code':'invalid-input','error':str(error),'exit_status':2}
        if browser: browser.save('failure',result)
        print(json.dumps(result,sort_keys=True),file=sys.stderr)
        return 2
    except Exception as error:
        result={'v':1,'status':'error','code':'browser-or-harness','error':str(error),'exit_status':70}
        if browser: browser.save('failure',result)
        print(json.dumps(result,sort_keys=True),file=sys.stderr)
        return 70
    finally:
        if browser: browser.close()
