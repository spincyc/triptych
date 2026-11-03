"""Independent literal ledger for selected raw curriculum courseunit bodies.

Only named source APIs are projected here. This is deliberately separate from
the semantic renderer and does not expand general TeX macros or claim to prove
their meaning. All literal units, including one-word paragraphs and notes, use
the outer source ledger's occurrence-counted checks without a length cutoff.
"""
import re


class ProjectionError(ValueError):
    pass


def selected_conditionals(source, solutions):
    pattern = re.compile(r'\\(if[A-Za-z@]+|else|fi)\b')
    found = pattern.search(source)
    if found is None:
        return source
    if found[1] != 'ifsolutions':
        raise ProjectionError('unsupported independent source conditional: '+found[1])
    depth, split = 1, None
    for token in pattern.finditer(source,found.end()):
        if token[1].startswith('if'):
            depth += 1
        elif token[1]=='fi':
            depth -= 1
            if depth==0:
                first=source[found.end():split.start() if split else token.start()]
                second=source[split.end():token.start()] if split else ''
                return (source[:found.start()]+selected_conditionals(first if solutions else second,solutions)
                        +selected_conditionals(source[token.end():],solutions))
        elif depth==1:
            split=token
    raise ProjectionError('unclosed independent source conditional')


def replace_calls(source, names, counts, replacement, library):
    pattern=re.compile(r'\\('+'|'.join(map(re.escape,names))+r')\b')
    pieces=[];pos=0
    while (found:=pattern.search(source,pos)):
        pieces.append(source[pos:found.start()])
        end=library.skip_gap(source,found.end())
        if source[end:end+1]=='[':
            end=library.skip_gap(source,source.index(']',end)+1)
        args=[]
        for _ in range(counts[found[1]]):
            value,end=library.brace_group(source,library.skip_gap(source,end))
            args.append(value)
        pieces.append(replacement(found[1],args));pos=end
    pieces.append(source[pos:]);return ''.join(pieces)


def project_unit(raw, mode, part, library):
    source=selected_conditionals(library.strip_tex_comments(raw),mode)
    if part=='Teaching':
        # The canonical module shell locally renews BeforeContinuing to a
        # no-op in Teaching; its integrated readiness chapter appears later.
        source=library.replace_grouped_macro(source,'BeforeContinuing',1,lambda _: '')
    source=library.replace_grouped_macro(source,'SubmoduleExtension',5,
        lambda a:'\n\n'+'\n\n'.join('{'+v+'}' for v in ([a[0],a[4]] if mode else a[:4]))+'\n\n')
    # Worksheet field 3 is an unused formatter argument. The canonical public
    # formatter displays ID, variant title, focus and use; preserve those all.
    pattern=re.compile(r'\\begin\{worksheet\}')
    pieces=[];pos=0
    while (found:=pattern.search(source,pos)):
        pieces.append(source[pos:found.start()]);end=found.end();args=[]
        for _ in range(6):
            value,end=library.brace_group(source,library.skip_gap(source,end));args.append(value)
        closing=source.find(r'\end{worksheet}',end)
        if closing<0:raise ProjectionError('unclosed independent worksheet')
        pieces.append('\n\n'+'\n\n'.join('{'+args[n]+'}' for n in (0,3,4,5))+'\n\n'+source[end:closing])
        pos=closing+len(r'\end{worksheet}')
    pieces.append(source[pos:]);source=''.join(pieces)
    names=('Exercise','ShortExercise','LongExercise','PassageExercise')
    source=replace_calls(source,names,{name:3 if name=='PassageExercise' else 2 for name in names},
        lambda _,a:'\n\n'+'\n\n'.join('{'+value+'}' for value in (a if mode else a[:-1]))+'\n\n',library)
    # A row's optional length is a physical spacing argument, never text.
    source=re.sub(r'\\\\\*?\s*(?:\[[^\]]*\])?','\n',source)
    source=source.replace(r'\begin{xltabular}',r'\begin{tabularx}').replace(r'\end{xltabular}',r'\end{tabularx}')
    return source


def derive_and_check(expected_units, rendered, library):
    from . import _literal_coverage as ledger
    chunks=[]
    for occurrence,row in enumerate(expected_units,1):
        chunks.append({'path':row['source'],'occurrence':occurrence,'selected_line':row['selected_line'],
            'text':project_unit(row['source_tex'],row['solutions'],row['part'],library)})
    units=ledger.expected_units({'chunks':chunks},library)
    return units,ledger.check_units(units,rendered,library)
