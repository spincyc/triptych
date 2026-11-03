"""Independent selected-source lexical unit ledger, before Pandoc rendering.

This supplemental gate verifies complete long literal source runs, all
headings and locators, and the existing independent table-cell audit. A source
run that cannot be accounted for refuses export. It does not manufacture a
coverage pass from the output's own hash or infer visual approval.
"""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
import hashlib,re

class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.words=[];self.hrefs=[]
    def handle_data(self,data):self.words.append(data)
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.hrefs.extend(value for key,value in attrs if key=='href')

def phrase(text, library):
    return library.word_phrase(unescape(text).replace('’',"'").replace('‘',"'").replace('`',"'"))


# These arguments control typography or hidden PDF metadata. No content-bearing
# command is added merely because an audit reports a missing word.
STRUCTURAL_ARGUMENTS={'setlength':2,'addtolength':2,'setcounter':2,'addtocounter':2,
 'fontsize':2,'vspace':1,'hspace':1,'Needspace':1,'needspace':1,'rule':2,
 'enlargethispage':1,'thispagestyle':1,'pagestyle':1,'pagenumbering':1,
 'label':1,'zlabel':1,'addcontentsline':3,'addtocontents':2,'geometry':1}

def strip_structural(source,library):
    source=library.drop_continuation_heads(source)
    source=library.REGISTER_ASSIGNMENT_RE.sub('',source)
    source=library.PARTIAL_RULE_RE.sub('',source)
    for name,count in STRUCTURAL_ARGUMENTS.items():
        source=library.replace_grouped_macro(source,name,count,lambda _: '{}')
    source=library.replace_grouped_macro(source,'multicolumn',3,lambda a:'{'+a[2]+'}')
    source=library.replace_grouped_macro(source,'texorpdfstring',2,lambda a:'{'+a[0]+'}')
    for environment,count in {'longtable':1,'tabular':1,'tabularx':2,'tabular*':2,'multicols':1}.items():
        pattern=re.compile(r'\\begin\s*\{'+re.escape(environment)+r'\}')
        pieces=[];cursor=0
        for match in pattern.finditer(source):
            index=match.end()
            for _ in range(count):_,index=library.brace_group(source,index)
            pieces.extend((source[cursor:match.start()],'\n'));cursor=index
        pieces.append(source[cursor:]);source=''.join(pieces)
    return source

def expected_units(selection,library):
    units=[];occurrences=Counter()
    def add(kind,payload,reference):
        normalized=phrase(re.sub(r'\\[A-Za-z@]+',' ',payload),library)
        if not normalized:return
        key=(kind,reference['path'],reference['occurrence']);occurrences[key]+=1
        units.append({'id':f"{reference['path']}:{reference['occurrence']}:{kind}:{occurrences[key]}",'kind':kind,'source_ref':{k:reference[k] for k in ('path','occurrence','selected_line')},'expected':normalized,'text_digest':hashlib.sha256(normalized.encode()).hexdigest()})
    for chunk in selection['chunks']:
        source=library.strip_tex_comments(chunk['text'])
        source=library.LIST_OPTION_RE.sub(r'\1',source)
        # Definition bodies are not occurrences. The owning audit separately
        # validates expansion, scoped assignments and every content macro.
        _,source=library.command_definitions(source)
        source=library.replace_grouped_macro(source,'AIModelContribution',3,lambda _: '')
        source=library.replace_grouped_macro(source,'AIGenerationProvenance',6,lambda _: '')
        source=library.replace_grouped_macro(source,'hypersetup',1,lambda _: '')
        for name in ('footnote','endnote'):
            def note(arguments):
                for run in library.source_word_runs(arguments[0]):
                    if run:add('note-run',' '.join(run),chunk)
                return ''
            source=library.replace_grouped_macro(source,name,1,note)
        for name in ('url','href','sourceurl'):
            def locator(arguments):
                add('locator',arguments[0],chunk)
                return '{'+arguments[1]+'}' if len(arguments)>1 else '{}'
            source=library.replace_grouped_macro(source,name,2 if name=='href' else 1,locator)
        # Explicit source headings, including short ones, retain all words.
        for heading in re.finditer(r'\\(?:section|subsection|subsubsection|paragraph|subparagraph)\*?\s*\{',source):
            payload,_=library.brace_group(source,heading.end()-1)
            add('heading',payload,chunk)
        source=strip_structural(source,library)
        source=re.sub(r'\\(?:begin|end)\s*\{[^{}]+\}',' ',source)
        for run in library.source_word_runs(source):
            if run:add('source-run' if len(run)>=6 else 'short-literal-unit',' '.join(run),chunk)
    return units

def check_units(units,rendered,library):
    parser=Text();parser.feed(rendered)
    visible=phrase(' '.join(parser.words),library)
    locators=phrase(' '.join(parser.hrefs),library)
    expected=Counter((unit['kind'],unit['expected']) for unit in units)
    missing=[]
    for (kind,text),count in expected.items():
        actual=len(re.findall(r'(?<!\w)'+re.escape(text)+r'(?!\w)',locators if kind=='locator' else visible))
        if actual<count:missing.append({'kind':kind,'expected':text,'wanted':count,'found':actual})
    # Literal source runs are independently occurrence-counted, including
    # repeated prose. Note movement and table reflow do not impose a false
    # global order; ordered include/occurrence identity lives in selection.
    return {'status':'refused' if missing else 'pass','unit_count':len(units),'kinds':dict(Counter(unit['kind'] for unit in units)),'missing_units':missing,'ordered_selection_digest_required':True,'scope':'Independent selected-source long literal runs, explicit headings and locators; owning full table-cell, title, macro, note and paragraph audits retained. This supplemental ledger is conservative and is not a general TeX semantic interpreter.'}
