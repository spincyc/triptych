"""Source-selected curriculum rendering with independent semantic coverage.

Canonical TeX remains authoritative. Unsupported executed controls refuse rather
than passing incomplete prose to Pandoc. The package never installs publications.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata

from _web_print_publication import split_parts


class CurriculumError(ValueError):
    pass


COURSE = "curriculums/ecclesiastical-latin"
COMMAND = re.compile(r"\\([A-Za-z@]+|.)", re.S)
RESPONSE = "TRIPTYCHCURRICULUMRESPONSESPACE"
ITEM_MARKER = re.compile(r'TRIPTYCHCURRICULUM(?:PROMPT|ANSWER)(?:START|END)[0-9]+')
REGISTRY_MARKER = re.compile(r'TRIPTYCHCURRICULUMREGISTRY(?:START|END)[0-9]+')
OFFICIAL_PANDOC_SHA256 = '870b811354a230a1864dd2b50dec3b850a981926ff4659ae460aea96ab6b8d28'
# The adapter replaces these owners' runtime machinery with named semantic
# adapters. Refuse a changed owner until that adapter has been reconciled; do
# not silently preserve an obsolete interpretation when source prose changes.
ADAPTER_CONTRACTS = {
    "course-format.sty": "94c1564726b6c2533522e1d748bbcd9e216be3a573e1d38a59651147f5f4b6e4",
    "memory/renderers.tex": "904661f5bcc947a03af8bdc210403aa9c29c6d87226d50bb58328a85a0231d15",
    "readers/renderers.tex": "dec65b9903e585390872f4658bb9689fcf5510196ef09b771c5736de0a0f1135",
}


def load_converter(root: Path):
    # Deferred to avoid the publication dispatcher importing its own loader.
    from _web_print_publication import load_library
    return load_library(root)


class Packet:
    def __init__(self, root: Path, recipe: dict, *, allow_companion: bool = False):
        self.root = root.resolve()
        self.web = load_converter(self.root)
        if recipe.get("provider") != "gpt" or recipe.get("edition", "main") != "main":
            raise CurriculumError("adapter supports canonical GPT curriculum packets only")
        self.recipe = recipe
        self.entry = self.root / recipe["entrypoint"]
        if not self.entry.resolve().is_relative_to(self.root / "src/gpt" / COURSE):
            raise CurriculumError("entrypoint is outside the course owner")
        if not allow_companion and not (self.entry.parent / "module-data.tex").is_file():
            raise CurriculumError("adapter requires a substantial packet's module-data.tex")
        self.macros = {}
        self.sources: dict[str, str] = {}
        self.units, self.variants = "all", "all"
        self.solutions = False
        self.memorysolutions = False
        self.stack = []
        self.active_inputs = []
        self.worksheets = []
        self.items = []
        self.selected_units = []
        self.worksheet_id = "UNSET"
        self.exercise_number = self.passage_number = 0
        self.response_spaces = 0
        self.response_geometry = []
        self.part = "Cover"
        self.expected_units = []
        self.expected_items = []
        self.expected_registry_units = []
        self.registry_occurrences = []
        self.lexemes, self.grammar, self.sets, self.prompts = {}, {}, {}, {}
        self.review_sources = "none"
        self.input_aliases = {}
        self.load_library()

    def custom_command(self, name, text, pos, depth):
        """Extension point: return (rendered, newpos), or None."""
        return None

    def custom_environment(self, name, text, pos, depth):
        """Extension point after the begin{name}: (rendered,newpos), or None."""
        return None

    def postprocess_html(self, rendered):
        number=0
        def arrow(match):
            nonlocal number
            if re.search(r'<mo>→</mo>',match.group()) and re.search(r'\\rightarrow\s*</annotation>',match.group()):
                number+=1
                return '<math xmlns="http://www.w3.org/1998/Math/MathML" data-semantic-unit="curriculum-inline-arrow-'+str(number)+'"><mo>→</mo></math>'
            return match.group()
        rendered=re.sub(r'<math\b[^>]*>.*?</math>',arrow,rendered,flags=re.S)
        if number!=len(getattr(self,'inline_arrow_units',{})):
            raise CurriculumError('canonical inline arrow occurrence count differs')
        return rendered

    def canonical_semantic_projection(self, body):
        units={}
        def arrow(match):
            ident='curriculum-inline-arrow-'+str(len(units)+1)
            signature=[['start','mo'],['text','→'],['end','mo']]
            units[ident]={'kind':'math','id':ident,'source_ref':{'path':self.recipe['entrypoint'],'occurrence':ident,'selected_line':1},
                'source_sha256':hashlib.sha256(match.group().encode()).hexdigest(),
                'ast_digest':hashlib.sha256(json.dumps(signature).encode()).hexdigest(),'expected_mathml_signature':signature}
            return r'\SemanticMathUnit{'+ident+'}'
        body=re.sub(r'\$\s*\\rightarrow\s*\$',arrow,body)
        self.inline_arrow_units=units
        return body, units

    def independent_semantic_ledger(self):
        from . import independent_projection
        selection=independent_projection.project_curriculum(self.root,self.recipe,self.web,self.canonical_semantic_projection)
        for path,raw in selection['sources'].items():
            relative=path.relative_to(self.root).as_posix()
            if relative in self.sources and self.sources[relative]!=hashlib.sha256(raw.encode()).hexdigest():
                raise CurriculumError('canonical source changed between renderer and independent planner: '+relative)
        import _web_print_semantics as semantic
        return selection,semantic.expected_units(selection,self.web),semantic

    def annotate_minipages(self, rendered):
        number=0
        def identify(match):
            nonlocal number
            number+=1
            tag=re.sub(r'\s+data-semantic-minipage="[^"]*"','',match.group())
            return tag[:-1]+' data-semantic-minipage="minipage-'+str(number)+'">'
        return re.sub(r'<div\b[^>]*\bclass="[^"]*\bminipage\b[^"]*"[^>]*>',identify,rendered)

    def make_parts(self, rendered):
        return split_parts(rendered)

    def pandoc_html(self, body, shim):
        folder=self.root/'.scratch/web-print-curriculum'
        folder.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile('w',suffix='.lua',dir=folder,encoding='utf-8') as stream:
            stream.write(self.web.TABLE_FILTER);stream.flush()
            return subprocess.run([self.pandoc_executable(),'-f','latex','-t','html5','--wrap=none','--shift-heading-level-by=1',
                '--lua-filter='+stream.name],input=shim+'\n\\begin{document}\n'+body+'\n\\end{document}\n',text=True,capture_output=True)

    def pandoc_executable(self):
        from _web_print_publication import Refused,require_print_toolchain
        try:
            attestation=require_print_toolchain(self.root)
        except Refused as error:
            raise CurriculumError(str(error)) from error
        path=Path(shutil.which('pandoc')).resolve()
        version=subprocess.run([str(path),'--version'],text=True,capture_output=True,check=True).stdout.splitlines()[0]
        self.pandoc_info={'id':'official-pandoc-3.11','sha256':attestation['pandoc_binary_sha256'],'version':version,
                          'lock_path':attestation['lock_path'],'lock_sha256':attestation['lock_sha256']}
        return str(path)

    def table_span_receipt(self, run):
        # The shared table filter emits exactly one typed receipt, including
        # an empty inventory. All other diagnostics still fail closed.
        lines=run.stderr.splitlines()
        receipt=self.web.TABLE_SPANS_RE.fullmatch(lines[0]) if len(lines)==1 else None
        if run.returncode or receipt is None:
            raise CurriculumError('Pandoc table-span receipt refused: '+run.stderr)
        spans=Counter(int(value) for value in receipt[1].split())
        if any(value<2 for value in spans):
            raise CurriculumError('invalid Pandoc table-span receipt')
        return spans

    def validate_table_spans(self, expected, rendered):
        if self.web.html_table_spans(rendered)!=expected:
            raise CurriculumError('source multicolumn spans changed in curriculum HTML')

    def normalize_profile(self, rendered):
        import _web_print_common as common
        normalized=common.normalize_html(rendered,profile='curriculum')
        self.html_profile_info={'module_sha256':hashlib.sha256(Path(common.__file__).read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256(rendered.encode()).hexdigest(),
            'output_sha256':hashlib.sha256(normalized.encode()).hexdigest(),
            'input_styles':re.findall(r'\sstyle\s*=\s*["\']([^"\']*)["\']',rendered)}
        return normalized

    def bind_units(self, ledger, rendered, coverage):
        from _web_print_publication import bind_print_units
        bound, identifiers=bind_print_units(ledger, rendered, coverage)
        self.print_binding_info={
            'input_sha256':hashlib.sha256(rendered.encode()).hexdigest(),
            'output_sha256':hashlib.sha256(bound.encode()).hexdigest(),
            'unit_count':len(identifiers)}
        self.expected_print_units=identifiers
        return bound

    def independent_plan(self):
        """Read selections and source occurrences before conversion.

        This parser never calls eval or consults output HTML. Its raw-source
        hashes and occurrence identities can be checked by an outer fidelity
        auditor independently of the presentation adapter.
        """
        data = self.read(self.entry.parent / 'module-data.tex')
        values = {definition.name:definition.macro[2]
                  for kind,definition in self.web.walk_definitions(data)
                  if kind=='definition' and definition.name and definition.macro
                  and definition.macro[0]==0}
        def field(name):
            value=values.get(name,'').strip().replace(r'\CourseRoot',COURSE)
            if not value or '\\' in value:
                raise CurriculumError('independent plan cannot resolve '+name)
            return value
        units=field('ModuleUnit').split(',')
        variants=field('ModuleWorksheetVariants').split(',')
        readers=field('ModuleReaderSet').split(',')
        supplement_map={'M18':['MR62-FORM-ADV1','MR62-FORM-PENT','MR62-FORM-XII-PENT','MR62-FORM-XXIII-PENT'],
                        'M21':['MR62-FORM-XII-PENT'],'M22':['MR62-FORM-XXIII-PENT']}
        supplements=[source for key in readers for source in supplement_map.get(key,[])]
        practice=values.get('ModulePractice','')
        match=re.fullmatch(r'\s*\\begingroup\s*\\SelectCourseUnits\{([^}]+)\}\s*\\input\{([^}]+)\}\s*\\endgroup\s*',practice)
        if not match:
            raise CurriculumError('independent packet-practice selection contract unsupported')
        practice_units=match[1].split(',')
        practice_source=match[2].replace(r'\CourseRoot',COURSE)
        def resolve(name):
            value=self.root/'src/gpt'/name
            return value if value.suffix else value.with_suffix('.tex')
        def scan(name, selected, solutions, part, review_selected=()):
            path=resolve(name); source=self.read(path)
            event=re.compile(r'\\input\s*\{|\\begin\{(courseunit|reviewsourceunit)\}')
            pos=0
            while (found:=event.search(source,pos)):
                if found[1] is None:
                    child,pos=self.group(source,found.end()-1)
                    scan(child.replace(r'\CourseRoot',COURSE),selected,solutions,part,review_selected)
                    continue
                env=found[1]
                args,pos=self.args(source,found.end(),1)
                raw,pos=self.environment(source,pos,env)
                if args[0] not in (selected if env=='courseunit' else review_selected):
                    continue
                source_path=path.relative_to(self.root).as_posix()
                record={'id':args[0],'source':source_path,'locator':env+':'+args[0],
                        'part':part,'solutions':solutions,
                        'source_tex':raw,
                        'selected_line':(self.root/source_path).read_text().split('\\begin{'+env+'}{'+args[0]+'}',1)[0].count('\n')+1,
                        'source_body_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                        'occurrence_id':part+':'+source_path+':'+env+':'+args[0]+('::solutions' if solutions else '::learner')}
                self.expected_units.append(record)
                # Exercise records have stable worksheet IDs and two separately
                # selected render occurrences. Parse every form independently.
                for form in re.finditer(r'\\begin\{worksheet\}',raw):
                    args,end=self.args(raw,form.end(),6)
                    content,_=self.environment(raw,end,'worksheet')
                    if args[1] not in variants: continue
                    exercise=passage=0
                    for item in re.finditer(r'\\(Exercise|ShortExercise|LongExercise|PassageExercise)\b',content):
                        end=item.end()
                        if item[1]=='Exercise' and content[end:].lstrip().startswith('['): end=content.index(']',end)+1
                        payload,_=self.args(content,end,3 if item[1]=='PassageExercise' else 2)
                        if item[1]=='PassageExercise':
                            passage+=1;stable=args[0]+'.P'+str(passage)
                        else:
                            exercise+=1;stable=args[0]+'.E'+str(exercise)
                        self.expected_items.append({'id':stable,'source':source_path,
                            'locator':'worksheet:'+args[0]+':'+stable,'part':part,'solutions':solutions,
                            'payloads':payload,'occurrence_id':part+':'+stable+('::solutions' if solutions else '::learner')})
        scan(field('ModuleLessonSource'),units,False,'Teaching')
        scan(COURSE+'/shared/content/readers/all',readers,False,'Reading and Composition')
        if supplements:scan(COURSE+'/shared/content/readers/all',(),False,'Reading and Composition',supplements)
        scan(practice_source,practice_units,False,'Reading and Composition')
        scan(field('ModuleExerciseSource'),units,False,'Cumulative Practice')
        scan(COURSE+'/shared/content/readers/all',readers,True,'Answers and Models')
        if supplements:scan(COURSE+'/shared/content/readers/all',(),True,'Answers and Models',supplements)
        scan(practice_source,practice_units,True,'Answers and Models')
        scan(field('ModuleExerciseSource'),units,True,'Answers and Models')
        self.selection_contract={'units':units,'variants':variants,'reader_sets':readers,
                                 'supplemental_review_sources':supplements,
                                 'memory_set':field('ModuleMemorySet'),'practice_units':practice_units,
                                 'render_states':{'Teaching':{'solutions':False,'BeforeContinuing':'suppressed-by-canonical-module-shell'},
                                     'Memory Work':{'memorysolutions':False},'Reading and Composition':{'solutions':False},
                                     'Cumulative Practice':{'solutions':False},'Answers and Models':{'solutions':True,'memorysolutions':True}}}
        key=field('ModuleMemorySet')
        if key not in self.sets or key not in self.prompts:
            raise CurriculumError('independent memory-set selection missing')
        def expect(file, locator, value, mode, view):
            self.expected_registry_units.append({'source':'src/gpt/'+COURSE+'/shared/memory/'+file,
                'locator':locator,'tex':value,'part':'Answers and Models' if mode else 'Memory Work',
                'solutions':mode,'view':view,'occurrence_id':view+':'+locator+('::solutions' if mode else '::learner')})
        def lexemes(sequence):
            return [v for v in self.sets[key][sequence].split(',') if v]
        for ident in lexemes(1):
            for index,name in enumerate(('citation','sense','morphology','usage')):
                expect('lexemes.tex',ident+':'+name,self.lexemes[ident][index],False,'new-lexemes')
        for mode in (False,True):
            for sequence in range(1,6):
                for ident in lexemes(sequence):
                    for index,name in enumerate(('citation','sense') if mode else ('citation',)):
                        expect('lexemes.tex',ident+':'+name,self.lexemes[ident][index],mode,'retrieval-'+str(sequence))
            for ident in lexemes(6):
                for index,name in enumerate(('title','family','prompt','answer') if mode else ('title','family','prompt')):
                    expect('grammar-facts.tex',ident+':'+name,self.grammar[ident][index],mode,'grammar')
            for index,name in enumerate(('reconstruction','reconstructionmodel','composition','compositionmodel')):
                if mode or index in (0,2):
                    expect('sets.tex',key+':'+name,self.prompts[key][index],mode,'reconstruction-composition')

    def read(self, path: Path) -> str:
        path = path.resolve()
        if not path.is_relative_to(self.root / "src") or not path.is_file():
            raise CurriculumError("missing or escaping canonical source: " + str(path))
        text = path.read_text()
        self.sources[path.relative_to(self.root).as_posix()] = hashlib.sha256(text.encode()).hexdigest()
        return self.web.strip_tex_comments(text)

    def group(self, text, pos):
        pos = self.web.skip_gap(text, pos)
        if text[pos:pos + 1] != "{":
            raise CurriculumError("expected brace argument near " + repr(text[pos:pos + 100]))
        return self.web.brace_group(text, pos)

    def args(self, text, pos, count):
        values = []
        for _ in range(count):
            value, pos = self.group(text, pos)
            values.append(value)
        return values, pos

    def calls(self, text, name, count):
        for found in re.finditer(r"\\" + re.escape(name) + r"(?=\s*\{)", text):
            yield self.args(text, found.end(), count)[0]

    def definitions(self, text):
        for kind, definition in self.web.walk_definitions(self.web.mask_tex_comments(text)):
            if kind == "definition" and definition.name and definition.macro:
                if definition.command == "providecommand" and definition.name in self.macros:
                    continue
                self.macros[definition.name] = definition.macro

    def load_library(self):
        owner = self.root / "src/gpt" / COURSE / "shared"
        for name in ("course-format.sty", "module-components.tex", "memory/renderers.tex", "readers/renderers.tex"):
            text = self.read(owner / name)
            if name in ADAPTER_CONTRACTS and hashlib.sha256((owner / name).read_bytes()).hexdigest() != ADAPTER_CONTRACTS[name]:
                raise CurriculumError("semantic adapter contract needs reconciliation: " + name)
            self.definitions(text)
        # Parse only declarative registry calls, never their TeX implementation.
        for file, command, count, table in (
            ("memory/lexemes.tex", "DeclareMemoryLexeme", 7, self.lexemes),
            ("memory/grammar-facts.tex", "DeclareMemoryGrammarFact", 5, self.grammar),
            ("memory/sets.tex", "DeclareMemorySet", 8, self.sets),
            ("memory/sets.tex", "DeclareMemoryPrompts", 5, self.prompts),
        ):
            for row in self.calls(self.read(owner / file), command, count):
                if row[0] in table:
                    raise CurriculumError("duplicate canonical registry ID: " + row[0])
                table[row[0]] = row[1:]
        # Their content-bearing instructions are expanded from the owner file.
        # These five helpers contain layout or runtime assignment machinery only.
        self.macros.update({name: (0, None, "") for name in ("CourseUnitOpeningGuard", "LearnerWorksheetBreak", "SolutionWorksheetBreak")})

    def scalar(self, text):
        for _ in range(30):
            changed = False
            def replace(match):
                nonlocal changed
                value = self.macros.get(match.group(1))
                if value and value[0] == 0:
                    changed = True
                    return value[2]
                return match.group(0)
            text = re.sub(r"\\([A-Za-z@]+)", replace, text)
            if not changed:
                return text.strip()
        raise CurriculumError("recursive scalar macro")

    def include(self, name):
        name = self.scalar(name)
        path = self.root / "src/gpt" / name
        if not path.suffix:
            path = path.with_suffix(".tex")
        if path.resolve() in self.active_inputs:
            raise CurriculumError("recursive canonical input: " + name)
        # The course format's complex rendering machinery has explicit adapters.
        if name == "common/preamble":
            self.read(self.root / "src/common/preamble.tex")
            return ""
        if name.endswith(("course-format.sty", "memory/renderers.tex", "readers/renderers.tex")):
            self.read(path)
            return ""
        self.active_inputs.append(path.resolve())
        try:
            return self.eval(self.read(path))
        finally:
            self.active_inputs.pop()

    def membership(self, key, selection):
        return selection == "all" or key in self.scalar(selection).split(",")

    def environment(self, text, pos, name):
        pattern = re.compile(r"\\(begin|end)\{" + re.escape(name) + r"\}")
        depth = 1
        for match in pattern.finditer(text, pos):
            depth += 1 if match[1] == "begin" else -1
            if depth == 0:
                return text[pos:match.start()], match.end()
        raise CurriculumError("unclosed environment: " + name)

    def conditional(self, text, pos, truth):
        # Nested primitive conditionals are parsed rather than matched with a
        # non-recursive expression. Only executed branches reach further input.
        pattern = re.compile(r"\\(if[A-Za-z@]+|else|fi)\b")
        depth, split = 1, None
        for match in pattern.finditer(text, pos):
            if match[1].startswith("if"):
                depth += 1
            elif match[1] == "fi":
                depth -= 1
                if depth == 0:
                    a = text[pos:split.start() if split else match.start()]
                    b = text[split.end():match.start()] if split else ""
                    return self.eval(a if truth else b), match.end()
            elif depth == 1:
                split = match
        raise CurriculumError("unclosed conditional")

    def response(self, origin, height=None):
        from .response_geometry import signature
        self.response_spaces += 1
        self.response_geometry.append(signature(origin,height))
        return " " + RESPONSE + str(len(self.response_geometry)) + "END "

    def render_responses(self, rendered):
        from .response_geometry import render
        for number,event in enumerate(self.response_geometry,1):
            marker=RESPONSE+str(number)+'END'
            if rendered.count(marker)!=1:raise CurriculumError('response geometry occurrence lost or repeated: '+str(number))
            rendered=rendered.replace(marker,render(event,number))
        if RESPONSE in rendered:raise CurriculumError('unplanned response geometry marker')
        return rendered

    def strip_response_markers(self, text):
        return re.sub(re.escape(RESPONSE)+r'[1-9][0-9]*END','',text)

    def eval(self, text, depth=0):
        if depth > 80:
            raise CurriculumError("macro expansion depth exceeded")
        out, pos = [], 0
        while pos < len(text):
            match = COMMAND.search(text, pos)
            if not match:
                out.append(text[pos:]); break
            out.append(text[pos:match.start()])
            name, pos = match[1], match.end()
            custom = self.custom_command(name, text, pos, depth)
            if custom is not None:
                rendered, pos = custom
                out.append(rendered)
                continue
            if name in {"newcommand", "renewcommand", "providecommand"}:
                definition = self.web.read_latex_definition(text, match)
                if definition is None or definition.macro is None:
                    raise CurriculumError("unreadable active definition")
                if name != "providecommand" or definition.name not in self.macros:
                    self.macros[definition.name] = definition.macro
                pos = definition.end
            elif name in {"input", "include"}:
                values, pos = self.args(text, pos, 1)
                out.append(self.include(values[0]))
            elif name == "InputIfFileExists":
                values, pos = self.args(text, pos, 3)
                candidate = self.scalar(values[0])
                if (self.root / "src/gpt" / candidate).is_file():
                    out.append(self.include(candidate)); out.append(self.eval(values[1], depth + 1))
                else:
                    out.append(self.eval(values[2], depth + 1))
            elif name in {"begingroup", "bgroup"}:
                self.stack.append((dict(self.macros), self.units, self.variants, self.solutions, self.memorysolutions, self.review_sources))
            elif name in {"endgroup", "egroup"}:
                if not self.stack: raise CurriculumError("unbalanced TeX scope")
                self.macros, self.units, self.variants, self.solutions, self.memorysolutions, self.review_sources = self.stack.pop()
            elif name in {"solutionsfalse", "solutionstrue", "memorysolutionsfalse", "memorysolutionstrue"}:
                if name.startswith("memory"): self.memorysolutions = name.endswith("true")
                else: self.solutions = name.endswith("true")
            elif name in {"ifsolutions", "ifmemorysolutions"}:
                piece, pos = self.conditional(text, pos, self.solutions if name == "ifsolutions" else self.memorysolutions)
                out.append(piece)
            elif name.startswith("if") or name in {"else", "fi"}:
                raise CurriculumError("unsupported active conditional: " + name)
            elif name in {"IfStrEq", "IfSubStr"}:
                values, pos = self.args(text, pos, 4)
                a, b = self.scalar(values[0]), self.scalar(values[1])
                out.append(self.eval(values[2] if (a == b if name == "IfStrEq" else b in a) else values[3], depth + 1))
            elif name in {"SelectCourseUnits", "SelectWorksheetVariants", "SelectReviewSources"}:
                values, pos = self.args(text, pos, 1)
                value = self.scalar(values[0])
                if name == "SelectCourseUnits": self.units = value
                elif name == "SelectWorksheetVariants": self.variants = value
                else: self.review_sources = value
            elif name == "forcsvlist":
                values, pos = self.args(text, pos, 2)
                for value in self.scalar(values[1]).split(','):
                    if value:
                        out.append(self.eval(values[0]+'{'+value+'}', depth + 1))
            elif name in {"BeginWorkedPassageBank", "BeginExerciseBank"}:
                values, pos = self.args(text, pos, 1)
                if not re.fullmatch(r"[A-Za-z0-9_]+", self.scalar(values[0])):
                    raise CurriculumError("invalid course bank ID")
            elif name == "end":
                values, pos = self.args(text, pos, 1)
                out.append('\\end{'+values[0]+'}')
            elif name == "begin":
                values, pos = self.args(text, pos, 1)
                env = values[0]
                custom = self.custom_environment(env, text, pos, depth)
                if custom is not None:
                    rendered, pos = custom
                    out.append(rendered)
                    continue
                if env in {"courseunit", "reviewsourceunit", "worksheet", "workedexample", "grammarbox", "learningobjectives", "titlepage", "xltabular", "tabularx", "tabular", "longtable"}:
                    count = {"courseunit":1,"reviewsourceunit":1,"worksheet":6,"workedexample":2,"grammarbox":1,"xltabular":2,"tabularx":2,"tabular":1,"longtable":1}.get(env,0)
                    values, pos = self.args(text, pos, count)
                    body, pos = self.environment(text, pos, env)
                    if env in {"courseunit", "reviewsourceunit"}:
                        selection = self.units if env == "courseunit" else self.review_sources
                        if self.membership(values[0], selection):
                            self.selected_units.append({"id":values[0],"solutions":self.solutions,'part':self.part,
                                'source':self.active_inputs[-1].relative_to(self.root).as_posix(),
                                'source_body_sha256':hashlib.sha256(body.encode()).hexdigest()})
                            out.append(self.eval(body, depth + 1))
                    elif env == "worksheet":
                        if self.membership(values[1], self.variants):
                            self.worksheet_id = values[0]
                            self.exercise_number = self.passage_number = 0
                            self.worksheets.append({"id":values[0],"variant":values[1],"solutions":self.solutions})
                            label = "Solution" if self.solutions else "Worksheet"
                            out.append("\\subsubsection{"+label+" "+values[0]+" — "+values[3]+"}\n\\textbf{Worksheet ID:} "+values[0]+"\\par\n\\textbf{Focus:} "+values[4]+"\\par\n\\textbf{Use:} "+values[5]+"\n\\begin{enumerate}\n"+self.eval(body, depth+1)+"\n\\end{enumerate}\n")
                    elif env == "workedexample":
                        out.append("\\paragraph{Worked example: "+values[0]+"}\n\\textit{Worked passage ID: "+values[1]+"; exact source and collation state are recorded in the passage inventory.}\n\\begin{quote}"+self.eval(body,depth+1)+"\\end{quote}\n")
                    elif env == "grammarbox": out.append("\\begin{minipage}{\\linewidth}\\textbf{"+values[0]+"}\\par "+self.eval(body,depth+1)+"\\end{minipage}\n")
                    elif env == "learningobjectives": out.append("\\begin{quote}\\textbf{This lesson develops the ability to:}\\begin{itemize}"+self.eval(body,depth+1)+"\\end{itemize}\\end{quote}\n")
                    elif env == "titlepage": out.append(self.eval(body, depth+1))
                    elif env in {"xltabular", "tabularx", "tabular", "longtable"}:
                        columns = re.sub(r'[PpCm]\{[^{}]+\}', 'l', values[-1])
                        columns = columns.replace('Y','l').replace('X','l')
                        out.append("\\begin{longtable}{"+columns+"}"+self.eval(body,depth+1)+"\\end{longtable}")
                else:
                    out.append("\\begin{"+env+"}")
            elif name in {"Exercise", "ShortExercise", "LongExercise", "PassageExercise"}:
                height={'Exercise':'0.38in','ShortExercise':'0.22in','LongExercise':'0.9in','PassageExercise':'1.15in'}[name]
                if name == "Exercise" and text[pos:].lstrip().startswith("["):
                    start=self.web.skip_gap(text,pos);end=text.index(']',start)
                    height=text[start+1:end].strip();pos=end+1
                values, pos = self.args(text, pos, 3 if name == "PassageExercise" else 2)
                if name == "PassageExercise":
                    self.passage_number += 1
                    stable = self.worksheet_id+".P"+str(self.passage_number)
                    prompt = "\\textbf{Text:} \\Latin{"+values[0]+"}\\par \\textit{Passage ID: "+self.worksheet_id+"."+str(self.passage_number)+"; exact source and collation state are recorded in the passage inventory.}\\par "+values[1]
                    answer = values[2]
                else:
                    self.exercise_number += 1
                    stable = self.worksheet_id+".E"+str(self.exercise_number)
                    prompt, answer = values
                self.items.append({"id":stable,"solutions":self.solutions,'part':self.part,
                    'source':self.active_inputs[-1].relative_to(self.root).as_posix(),
                    'payloads':values,"prompt":prompt,"answer":answer})
                ordinal=str(len(self.items))
                marked_prompt=(' TRIPTYCHCURRICULUMPROMPTSTART'+ordinal+' '+self.eval(prompt,depth+1)
                               +' TRIPTYCHCURRICULUMPROMPTEND'+ordinal+' ')
                answer_label='Answer / notes:' if name=='PassageExercise' else 'Answer / model:'
                marked_answer=('\\par\\textbf{'+answer_label+'} TRIPTYCHCURRICULUMANSWERSTART'+ordinal+' '
                               +self.eval(answer,depth+1)+' TRIPTYCHCURRICULUMANSWEREND'+ordinal+' ' if self.solutions else '\\par '+self.response(name,height)+'\\par ')
                out.append("\\item \\begin{minipage}{\\linewidth}"+marked_prompt+marked_answer+"\\end{minipage}\n")
            elif name in {"MemoryLexemeField", "MemoryGrammarField", "MemorySetField"}:
                values, pos = self.args(text,pos,2)
                key, field = map(self.scalar,values)
                if name == "MemoryLexemeField": table, fields = self.lexemes,"citation sense morphology usage strand expectation".split()
                elif name == "MemoryGrammarField": table, fields = self.grammar,"title family prompt answer".split()
                elif field in {"reconstruction","reconstructionmodel","composition","compositionmodel"}: table, fields = self.prompts,"reconstruction reconstructionmodel composition compositionmodel".split()
                else: table,fields=self.sets,"title new rone rtwo rfive stage grammar".split()
                if key not in table or field not in fields: raise CurriculumError("unknown registry lookup: "+key+"/"+field)
                value=table[key][fields.index(field)]
                file=('lexemes.tex' if name=='MemoryLexemeField' else 'grammar-facts.tex' if name=='MemoryGrammarField' else 'sets.tex')
                self.registry_occurrences.append({'source':'src/gpt/'+COURSE+'/shared/memory/'+file,
                    'locator':key+':'+field,'solutions':self.memorysolutions,'tex':value})
                ordinal=str(len(self.registry_occurrences))
                out.append(' TRIPTYCHCURRICULUMREGISTRYSTART'+ordinal+' '+self.eval(value,depth+1)
                           +' TRIPTYCHCURRICULUMREGISTRYEND'+ordinal+' ')
            elif name == "memory@usesequence":
                values,pos=self.args(text,pos,3)
                key,field,callback=map(self.scalar,values)
                fields="title new rone rtwo rfive stage grammar".split()
                if key not in self.sets or field not in fields: raise CurriculumError("unknown memory sequence")
                for value in self.sets[key][fields.index(field)].split(','):
                    if value: out.append(self.eval(callback+"{"+value+"}",depth+1))
            elif name in {"memory@eventrows","memory@reverseeventrows"}:
                values,pos=self.args(text,pos,3)
                self.macros['memory@event']=(0,None,values[1])
                source=self.macros[name][2]
                found=re.search(r'\\memory@usesequence\{#1\}\{#3\}\{\\([^}]+)\}',source)
                if not found: raise CurriculumError('memory event callback contract changed')
                out.append(self.eval('\\memory@usesequence{'+values[0]+'}{'+values[2]+'}{\\'+found[1]+'}',depth+1))
            elif name in {"memory@blankcell","memory@twolines","memory@fourlines","Blank","LongBlank","hrulefill"}:
                out.append(self.response(name))
            elif name == 'vspace':
                star=text[pos:pos+1]=='*'
                if star:pos+=1
                values,end=self.args(text,pos,1);height=re.sub(r'\s+','',values[0])
                nextpos=self.web.skip_gap(text,end);following=COMMAND.match(text,nextpos)
                if following and following[1]=='hrulefill':
                    out.append(self.response('vspace',height));pos=following.end()
                else:
                    out.append('\\vspace'+('*' if star else '')+'{'+values[0]+'}');pos=end
            elif name == 'rule':
                values,end=self.args(text,pos,2)
                if values[0].strip()=='0pt':out.append(self.response('rule',values[1].strip()))
                else:out.append('\\rule{'+values[0]+'}{'+values[1]+'}')
                pos=end
            elif name == "fcolorbox":
                values,pos=self.args(text,pos,3);out.append(self.eval(values[2],depth+1))
            elif name in {"Needspace","hypersetup","setcounter","setlength","addtolength","addcontentsline","CourseUnnumberedSectionContents","markboth","pagenumbering","thispagestyle"}:
                count={"setcounter":2,"setlength":2,"addtolength":2,"addcontentsline":3,"markboth":2}.get(name,1)
                _,pos=self.args(text,pos,count)
            elif name in {"part","chapter"}:
                star = text[pos:pos+1]=='*'
                if star:pos+=1
                values,pos=self.args(text,pos,1)
                if name=='part': self.part=self.scalar(values[0])
                out.append(('\\section' if name=='part' else '\\subsection')+'{'+self.eval(values[0],depth+1)+'}\n')
            elif name in {"section", "subsection", "subsubsection"}:
                star = text[pos:pos+1]=='*'
                if star:pos+=1
                values,pos=self.args(text,pos,1)
                next_level={'section':'subsubsection','subsection':'paragraph','subsubsection':'subparagraph'}[name]
                out.append('\\'+next_level+('*' if star else '')+'{'+self.eval(values[0],depth+1)+'}\n')
            elif name == "space":
                out.append(' ')
            elif name == "let":
                target,pos,_=self.web.control_sequence(text,self.web.skip_gap(text,pos))
                source,pos,_=self.web.control_sequence(text,self.web.skip_gap(text,pos))
                if source not in self.macros: raise CurriculumError('unsupported let source: '+str(source))
                self.macros[target]=self.macros[source]
            elif name in self.macros:
                macro=self.macros[name]
                call=self.web.macro_call(text,pos,macro)
                if call is None: raise CurriculumError('unreadable macro call: '+name)
                expanded,pos=call
                out.append(self.eval(expanded,depth+1))
            else:
                # Macro substitution preserves TeX token boundaries. A textual
                # serialization must not join a terminal control word to the
                # first letter of the following expanded source token.
                out.append('\\'+name+(' ' if name[0].isalpha() else ''))
        return ''.join(out)

    def flatten(self):
        self.independent_plan()
        source=self.eval(self.read(self.entry))
        if self.stack: raise CurriculumError('unclosed TeX scopes')
        head,body=self.web.split_document(source)
        if r'\TriptychRightsNotice' not in body:
            body += '\n\\TriptychRightsNotice\n'
        body=self.web.strip_layout_macros(body)
        # Safe primitive hints cannot consume the number opening the next cell.
        body=self.web.drop_continuation_heads(self.web.terminate_swallowers(self.web.fix_column_specs(body)))
        body=self.web.STARRED_ROW_END_RE.sub(r'\\\\',body)
        body=self.web.PARTIAL_RULE_RE.sub('',body)
        body=self.web.LIST_OPTION_RE.sub(r'\1',body)
        shim=self.web.SHIM.read_text()
        defined=self.web.defined_names(shim)
        problems=self.web.undefined_uses({self.entry:body},defined)
        if problems: raise CurriculumError('\n'.join(problems))
        self.validate_selection()
        return body,shim

    def validate_selection(self):
        if self.units=='all': raise CurriculumError('packet never established exact unit selection')
        for actual,expected in ((self.selected_units,self.expected_units),(self.items,self.expected_items)):
            keys=('id','solutions','part','source','source_body_sha256') if actual is self.selected_units else ('id','solutions','part','source','payloads')
            if [{key:row[key] for key in keys} for row in actual] != [{key:row[key] for key in keys} for row in expected]:
                raise CurriculumError('independent canonical occurrence order/payload coverage failed')
        keys=('source','locator','solutions','tex')
        if [{key:row[key] for key in keys} for row in self.registry_occurrences] != [{key:row[key] for key in keys} for row in self.expected_registry_units]:
            raise CurriculumError('independent canonical registry occurrence order/payload coverage failed')

    def render(self):
        body,shim=self.flatten()
        source_selection,semantic_ledger,semantic_engine=self.independent_semantic_ledger()
        title=self.scalar(r'\ModuleID: \ModuleTitle')
        run=self.pandoc_html(body,shim)
        expected_spans=self.table_span_receipt(run)
        rendered=self.render_responses(run.stdout)
        rendered=self.annotate_minipages(self.postprocess_html(rendered))
        if re.search(r'\\[A-Za-z]+',rendered): raise CurriculumError('unconverted control sequence in output')
        tables = self.web.table_count(body, shim)
        if tables != len(re.findall(r'<table(?:\s|>)', rendered)):
            raise CurriculumError('source/output semantic table count differs')
        lost = self.web.lost_cell_openings(self.strip_response_markers(body), rendered, shim)
        if lost:
            raise CurriculumError('source table cell payload lost: '+repr(lost))
        if 'Reuse and rights.' not in rendered or 'Last revised (UTC):' not in rendered:
            raise CurriculumError('source revision or rights notice missing')
        if any(name in rendered for name in ('AIModelContribution','AIGenerationProvenance','AIDocumentRevisionTimestamp')):
            raise CurriculumError('internal metadata escaped into the reader')
        def normalized(value):
            value=html.unescape(re.sub(r'<[^>]*>',' ',value))
            return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',value).casefold()))
        def count_phrase(value,text):
            return len(re.findall(r'(?<!\w)'+re.escape(value)+r'(?!\w)',text))
        def literal(value):
            # Registry values are data, not programs. Refuse an unknown text
            # command before deriving the independent expected verbal payload.
            value=value.replace(r'\Missal',r'\textit{Missale Romanum} (1962)')
            value=self.web.LIST_OPTION_RE.sub(r'\1',value)
            value=re.sub(r'\\(?:begin|end)\{(?:enumerate|itemize|description|quote|quotation|verse)\}',' ',value)
            value=re.sub(r'\\item\b',' ',value)
            value=re.sub(r'\\(?:Blank|LongBlank|ldots|dots)\b',' ',value)
            value=value.replace(r'\rightarrow','→').replace('$','')
            known={'Latin','English','Term','textit','textbf','texttt','emph','textsc','textrm','textnormal','footnote','endnote','space','par','ae','oe','\\'}
            for name in COMMAND.findall(value):
                if name not in known and name not in '%&#_$':
                    raise CurriculumError('unsupported registry payload command: '+name)
            value=re.sub(r'\\(?:Latin|English|Term|textit|textbf|texttt|emph|textsc|textrm|textnormal|footnote|endnote)\b','',value)
            value=value.replace(r'\ae','æ').replace(r'\oe','œ')
            value=re.sub(r'\\(?:space|par)\b',' ',value)
            return normalized(value.replace('{','').replace('}','').replace('\\',''))
        # These payloads are independently parsed from canonical worksheet
        # occurrences. Short prompts and answers have exactly the same guard
        # as long text; no minimum-length threshold permits their deletion.
        visible=html.unescape(re.sub(r'<[^>]*>',' ',rendered))
        registry_failures=[]
        for ordinal,row in enumerate(self.expected_registry_units,1):
            match=re.search('TRIPTYCHCURRICULUMREGISTRYSTART'+str(ordinal)+r'\b(.*?)TRIPTYCHCURRICULUMREGISTRYEND'+str(ordinal)+r'\b',visible,re.S)
            expected=literal(row['tex'])
            actual=normalized(match[1]) if match else None
            if actual != expected:
                registry_failures.append({'occurrence':row['occurrence_id'],'expected':expected,'actual':actual})
        if registry_failures:
            raise CurriculumError('independent canonical registry payload shortfall: '+repr(registry_failures))
        item_failures=[]
        for ordinal,row in enumerate(self.expected_items,1):
            # The ordinal itself is checked against an independently parsed
            # canonical occurrence sequence. Match verbal payloads inside that
            # occurrence, so another "Amen" elsewhere cannot hide a deletion.
            for kind,payloads in (('PROMPT',row['payloads'][:-1]),('ANSWER',row['payloads'][-1:] if row['solutions'] else [])):
                if not payloads:continue
                match=re.search('TRIPTYCHCURRICULUM'+kind+'START'+str(ordinal)+r'\b(.*?)TRIPTYCHCURRICULUM'+kind+'END'+str(ordinal)+r'\b',visible,re.S)
                if match is None:
                    item_failures.append({'occurrence':row['occurrence_id'],'field':kind,'failure':'missing payload boundary'})
                    continue
                actual=normalized(match[1])
                for value,count in Counter(literal(value) for value in payloads).items():
                    found=count_phrase(value,actual)
                    if value and found<count:
                        item_failures.append({'occurrence':row['occurrence_id'],'field':kind,'payload':value,'expected':count,'found':found})
        if item_failures:
            raise CurriculumError('independent canonical prompt/answer payload shortfall: '+repr(item_failures))
        rendered=REGISTRY_MARKER.sub('',ITEM_MARKER.sub('',rendered))
        rendered=self.normalize_profile(rendered)
        self.validate_table_spans(expected_spans,rendered)
        from . import prose_coverage
        literal_units,literal_coverage=prose_coverage.derive_and_check(self.expected_units,rendered,self.web)
        complete_coverage=semantic_engine.check_units(semantic_ledger,rendered,self.web)
        if not complete_coverage.get('complete'):
            error=CurriculumError('complete curriculum semantic source coverage failed')
            error.coverage=complete_coverage
            raise error
        rendered=self.bind_units(semantic_ledger,rendered,complete_coverage)
        complete_coverage=semantic_engine.check_units(semantic_ledger,rendered,self.web)
        if not complete_coverage.get('complete'):
            error=CurriculumError('bound curriculum semantic source coverage failed')
            error.coverage=complete_coverage
            raise error
        from .response_geometry import check as check_geometry
        geometry_coverage=check_geometry(source_selection['response_geometry'],rendered)
        answer_ids=[item['id'] for item in self.items if item['solutions']]
        learner_ids=[item['id'] for item in self.items if not item['solutions']]
        if answer_ids!=learner_ids: raise CurriculumError('selected exercise and answer identity/order mismatch')
        html_document='<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape(title)+'</title><body>'+rendered+'</body></html>\n'
        source_digest=hashlib.sha256(json.dumps(self.sources,sort_keys=True).encode()).hexdigest()
        selection_digest=hashlib.sha256(json.dumps(self.selection_contract,sort_keys=True).encode()).hexdigest()
        return {'html':html_document,'tex':REGISTRY_MARKER.sub('',ITEM_MARKER.sub('',body)),'source_paths':self.sources,'source_digest':source_digest,
                'output_id':self.recipe['id'].removeprefix('publication:'),'print_type':'curriculum-packet','title':title,
                'render_toolchain':self.pandoc_info,'html_profile':self.html_profile_info,
                'print_binding':self.print_binding_info,'expected_print_units':self.expected_print_units,
                'response_geometry_coverage':geometry_coverage,'expected_response_geometry':source_selection['response_geometry'],
                'parts':self.make_parts(rendered),
                'selection_digest':selection_digest,'expected_units':self.expected_units,'expected_items':self.expected_items,
                'expected_registry_units':self.expected_registry_units,
                'expected_literal_units':literal_units,'literal_coverage':literal_coverage,
                'coverage_result':complete_coverage,'semantic_ledger':semantic_ledger,
                'semantic_selection':source_selection['selection'],
                'assets':[], 'selections':{'contract':self.selection_contract,'units':self.selected_units,'worksheets':self.worksheets,'items':self.items},
                'checks':{'exercise_answer_ids_match':True,'canonical_occurrence_order_payloads_match':True,'canonical_registry_payload_units':len(self.expected_registry_units),'registry_payload_shortfalls':registry_failures,'prompt_answer_payload_shortfalls':item_failures,'learner_items':len(learner_ids),'answer_items':len(answer_ids),'response_spaces':self.response_spaces,'source_html_table_count':tables,'lost_table_cell_openings':lost},'status':'generated-unreviewed'}


def render_packet(root: Path, recipe: dict):
    return Packet(Path(root),recipe).render()
