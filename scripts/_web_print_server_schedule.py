"""Source-only server occurrence schedule and final-assembly conservation gate.

The schedule is constructed from canonical calls before the first conversion.
It has no rendering callback and never uses a fragment audit or rendered unit
as an expectation. Final HTML is checked before the owner seals its bodies.
"""
from __future__ import annotations
import copy
from collections import Counter
from html.parser import HTMLParser
import json
import re


SOURCE_MARKS = frozenset('℣℟✠□☐')


def _api():
    import _web_print_server as s
    return s


def _compact(events):
    result = []
    for event in events:
        event = list(event)
        if event[0] == 'text':
            if not event[1]:
                continue
            if result and result[-1][0] == 'text':
                result[-1][1] += ' ' + event[1]
                continue
        result.append(event)
    # The bounded source ledger has no visible atom for an empty table
    # cell. Such cells remain the table/fragment structural auditor's remit;
    # every nonempty cell retains its own final-assembly boundary.
    visible = []
    for event in result:
        if event == ['close', 'cell', ''] and visible and visible[-1] == ['open', 'cell', '']:
            visible.pop()
        else:
            visible.append(event)
    return visible


# These finite source templates are projected into browser structures rather
# than executed as arbitrary TeX. A changed definition requires its adapter
# projection to be reviewed; source identity alone cannot approve old labels.
# Only definition digests live here. All occurrence text remains canonical.
SUPPORTED_TEMPLATES = {
    'BroadIPA': frozenset(('fbb5b1092de8581db2dc0f1f9eef0c886655b38deb3ab954fc4eaadf266753df',)),
    'CanonLatin': frozenset(('5efd6e24659dde492e60ad44d6d9a9275372ca95ec60b13d58558b89fbaaa127',)),
    'CardCompanionTerminalApparatus': frozenset(('420b58d6810cb7c2d69511879110b86c564cc6887acf99e964d4ac1e2a9a5bcd',)),
    'GuideVoiceChoice': frozenset(('0b71f83892c34743f0465e344ef68b039abe15cac35d013928303eab1ce885b6', '6b9fbd87204599afb2e2778261877d41f130a3faeddfa1ce50504f320cc0d0b8', 'f8249c51b880ecd7a5b73df4c095f228c98af21150090b286c02596408bff2f1',)),
    'LMAction': frozenset(('467394760a9613ee8bc5dab36a24fed6a198b11b14ecebc70a15ed22bfdb19bf',)),
    'LMBeatBadge': frozenset(('25c08230baaada5ea5475488ccd9b522aafa37ce19afa0566f94712416963819',)),
    'LMBranch': frozenset(('63e8500f6ee6c418a1e4e3ddb6ed326343a66f99c50fac2cd3af8a7c895c4751',)),
    'LMCompactTrainerAction': frozenset(('462d5e8d293272dbb2484190ee3de69995587f96c3f8292e918c5c548983aead',)),
    'LMDiagramNote': frozenset(('62bd8d0baf77f88eed456fe2de87c9ec447d378c41d3b15e0efb0701bd59d068',)),
    'LMDialogueFirst': frozenset(('33691c8c1a8046d609d23c643e5e60a80f96eb477c2c5874c3bf8cadf0bb2bd0',)),
    'LMDialogueLiteral': frozenset(('ad850ef479d72a5a35a5fa9f614c6d425fabb0c01657d2a54cec97f8062d54a7',)),
    'LMDialogueRepeat': frozenset(('3758e8eb3a32a925749e0f0a00280644f1a6cdbb4a60f3f391728893ded22471',)),
    'LMLaneHeadings': frozenset(('2fc2c18b14396a43375a1659711f2a967175f38bbdc84511094c8dc67de4feea',)),
    'LMLaneLabel': frozenset(('89786e08b3ba3dcff2822c4ee76bbda151a8bfddb3deb8b110e87d6beee07178',)),
    'LMModelChoice': frozenset(('f9edf6508d67888b14cd667f69ffeee47440922a3d8c8b638d78dbfbad090231',)),
    'LMPageIntro': frozenset(('32594c199a613d4dd1566013186e04f84779bea6495341a2d564ce258cbc51ab',)),
    'LMPhraseBlock': frozenset(('b05671cc96d168930691727a61ee5dbae8c4277b777883e19607b5da4d4279ee',)),
    'LMRenderGenerationMetadata': frozenset(('54a931707027d72dfb516f0f52bb77198bd44d729e48de54255bc1139047a37d', 'de163f7d83458d9bf8663550b9c63ffe0c1e28db9338c91f14a8a5096a3855f2',)),
    'LMRepeatTag': frozenset(('2080955ea5988a547f92267ad8139494b727d261f7b83097745c9842e6be907e',)),
    'LMTrainerNote': frozenset(('a64b0bc718fb8e0db9083294fc45870552f4c7975896836c156a2b371226aeb5',)),
    'LearnLatin': frozenset(('dd28b2bf4781b2957f873ff5cda7a5acf02491b4d5bc5092a304b4909435ec18',)),
    'LocalChoice': frozenset(('67db340c340778521aa11dc0f61ee3eb305cc8f4bec5692a3105505ab8e36c8d',)),
    'LowMassBackCard': frozenset(('2ff463f8bc98466ed5398cb93e296d659e872c5e0ccf1d249b0a259b763ac30c',)),
    'LowMassFinalNotice': frozenset(('87dbf30b5de071e609e9883d89e317ec0e6c6609e5081e3f8561f2fe1412f4aa',)),
    'LowMassFlashFrame': frozenset(('3e8d7463d9f6140bd80ebd8b3fa289e70f792f3eb7e7c30f060c74c00349b28b',)),
    'LowMassFlashHeader': frozenset(('72c07c9ad0acd5d6431b24ad759082a131a8abf6bbdb51cec05b314342aa5cf4',)),
    'LowMassFrontCard': frozenset(('1b5dd0c3329e58dc0675856c2305bfc21cfa613e54a6bfda05bf4267124fa2a3',)),
    'LowMassQualifiedCue': frozenset(('a4adff1b97a06d4cd772dd4a6b039fe58dee29728cf09efd0c88c8b4d5edf690',)),
    'LowMassSheetFooter': frozenset(('72b2491388ae79d78e969f3a9e20dbda68c528971636eaecd2282ce28a6d735d',)),
    'MCGuideCheck': frozenset(('ab5599d1575d2d4ca39c0c3c237513bed2d513e5ac3081a75f996b8fd1706db7',)),
    'MCRoleHeading': frozenset(('015af4cf142d0cb20d2cbb5aa5e9e3e4dcf1655f32537edc8e47695a2371dfd0',)),
    'MCSceneTile': frozenset(('1f46eaf8dc34cc9193b02887ab208609cc9176a69da5a64006c9225e6c31bcfe', 'a1feac5fc196211e0f149480ce2ea507e74d402e93bf538ac6f18e03225382bb',)),
    'MissalDisplay': frozenset(('7ed1a5f4cd3cc350dcab73e7c154e63e5245c349d164a4c5f5ad6f5d3d500223',)),
    'MissalRule': frozenset(('9614b98e5da350ba1faad5dcb0487bac3cb8d31d4faa44e15dd3c9827dedac30',)),
    'MissalSeparator': frozenset(('70e34bff4bcd59825a9e867bf8c70cfb53c91bdd2d45a798cc1cb9558f43b955',)),
    'ModelRule': frozenset(('1fa5f7d61e459247c5fa0adb0b7628db28c2f036ba4a7cbd6851ceebb28e2380',)),
    'PrintServerAnswer': frozenset(('3ca12d913ef6384a20f84bdb585a4ba0f3d332ba9024fb9ee6cdcdf4ff00d940', '4f85ad65476ab0fe7c473bd56eb40f76a77b32c49dd899d69af01fa66b3d28c9',)),
    'ResponseCardID': frozenset(('5ae5e26b0f127f8f2c247fa5ec651bee5fcf3eed9f92f766936c3b8b180ec830',)),
    'ResponseFormMark': frozenset(('90e94575da49a64e5ab257588e7d45238fbbb1afc217cf4a60ee892930631fe9',)),
    'ResponseLessonData': frozenset(('36391fd4d71720d964188cf12acc21a26e93e95e1da46dd6bef4a8a01a78ac90',)),
    'ResponseMark': frozenset(('0976bf7e9d6832922b329fce621ac4d74ec3d2e9d79a5182ecc1df08e7a55d4b',)),
    'ServerAnswerRef': frozenset(('dd28b2bf4781b2957f873ff5cda7a5acf02491b4d5bc5092a304b4909435ec18',)),
    'ServerCueData': frozenset(('f47a9d4438db417ca83ad8a9a8b5c5698521425c18b7576beaab275963ec182e',)),
    'ServerIPAData': frozenset(('34da5eb57c7554271342e11fbe8eda5f239681a728c19c16d025a4295c74f959',)),
    'ServerJobData': frozenset(('20d5f7609a251d7a0ea1745b401be9d706c2a43c7af6e7871f25d424699f11d8', '424e28f6af3995fdf9952f75b5f8dac8e8d84263bb6e51873ae9c94b90113f02', 'fece6599409679a92ab88d5d1d75cb4ee967ceee55fc11a62063fbaae3195abd',)),
    'ServerLatinData': frozenset(('2dc38f2c37367066b33f7a4c6b2f0468108152a69ff00761569aa1fa9d87c5f5',)),
    'ServerLearnerData': frozenset(('47f557ab447e357219c79a4391753b22b1f5575af5567abba092eef41dd965fa',)),
    'ServerLearnerLine': frozenset(('3e69877e08236a82eed5fc58792169b537df0b39fb93ca351b1a0ccb649f08f6',)),
    'ServerMeaningData': frozenset(('c50ff8b23ec35532d5c2935eba5bbfa636957980c9ae8c3da524411078d826d1',)),
    'ServerSoundData': frozenset(('b9f1f1c99e8d2d0eb8365b2ecd901c14993d7c80025b12d63f7dd520b7ee3fdd',)),
    'ServerStress': frozenset(('da9c158223d0197d6a3fd68b89498ed9d4185456ed85f5b0cefbd2ca93f9392b',)),
    'ServerTitleData': frozenset(('53a43fe5f9b7ad4ccb5c30642d591802be6bfa1035e979757926cfae7fd2a70c',)),
    'ServerVoiceData': frozenset(('1bf4babf68500d5360daf713df71dd1a2e0a12adf6ab8d656523f489137d725f', 'a6e359c91bf76ff0b6ac3dfee6987b85c4ed48dd340e7014ac54b08969072db4', 'e9c1741af83544cc49814d7087502ee388dc5016e459e3a67b44082563926e92',)),
    'SolemnEveryRoleTrack': frozenset(('5c596fa5a0ec8b52814f34642c06ff35d5538cf2e14c7968e79638816fe56d40', 'dce67c4fd9563d6ac7cdc2bf94850e9895fb1001e93a18facf0503b882e8ff12',)),
    'SolemnMapStop': frozenset(('bcc2377168141f4359b4d81441e86c257fc07e306784d26e12facee3333e28ba', 'cf92d9630bd77f86717aeca6a1115789087328d05968ceec1c066ccc1ac13c79',)),
    'SoundLine': frozenset(('3e69877e08236a82eed5fc58792169b537df0b39fb93ca351b1a0ccb649f08f6',)),
    'SpokenCue': frozenset(('d500012795fa52f484a4deb8ced3a4b3c95ce499a28d364b12260cf19af57ac9',)),
    'SpokenResponse': frozenset(('db6009f73cbf20b163e547565929156c0bf2dd1448f71bfa64a2f30d76b5b3d9',)),
    'TerminalNote': frozenset(('6e0eacec690c049943354768b53eccadae15034178cbca48538d30066f7d854f',)),
    'VersicleMark': frozenset(('9a5e81acfc906cb81fdb594e4426b75c5c5d5b459a6a3933ecc23273ff56a60f',)),
    'actionflashback': frozenset(('c3e1cacf573dee75f90fa362b2c045b736ccf63614971d0798f29f1c82af292d',)),
    'actionrowid': frozenset(('6e455ca3a0a1fa950116834419800fb7132d5f9be6f9d4e066aad304fb1bc233', '9a272622592fb179776d75652f96f2fefdf897e777dbfbae5c75d8337c6f6d4d', 'e90e46f106541cc25e7f3243fb7679134f6dce18c6d6af4bea74c04d5bd6771f',)),
    'actionsection': frozenset(('06cc355a11725bb07627a7dfdfe5bbf63f88827b43b5a356ab2a12137fb5244f', '424c3b16d1b9817ca4504a083c29cfbe7fdeca383db90c5787ffb3ccdd319c09', 'fb8b4b562af58e488c0f0db94a13462762c4bd3de29ba5438730bb83e5c61be5',)),
    'denseintegratedresponseback': frozenset(('be5f62e41fff37573090aaac7c990469e02fd8b2d4f2666a3380676c82f6ffc7',)),
    'flashfront': frozenset(('726cb6dc3331492db924fd8224094f368ab3307923ae4cc6c043deac51c25757',)),
    'flashheader': frozenset(('ea0948d2b1788cbb2fdbb91fdeffaf2f279b7f159e88adb0377a464abe93bfcb',)),
    'integratedresponseback': frozenset(('3220393384910209027d8fe8f69fd8a9451feaff20b69787d34f686eca42591e',)),
    'integratedresponsefront': frozenset(('c70f36af8de1477a9c0ad1b2e4ea12b6fd8c8bffde179af5a76dbe8ded53a1a7',)),
    'masterybox': frozenset(('4338a183b20a4acf6ec92ad5a3edba4c92663a746968c4310797c8229c45523a',)),
    'mcroleheading': frozenset(('21e6bd0d793f3fc43ab76c1248c32031fe01da694726b6edf3568771f6f7f39e', 'ec618c5c07f5e6b8b879f26a80a5c5a165ee745ace52e47bb790998eac57452a',)),
    'mcrolerow': frozenset(('673e715a858915a6bac2eb7d5e1c1084f4ac8f0abd63a84782c068812774f479',)),
    'rolecard': frozenset(('7db351f9f5cca0f7b16ac1096e7b094b18466703c21587a6bff12f456fce2807', '93c3fe4bd2d4671f070fe8871f972dc8c23107e7b3a51f13fe812c1b50fa5c74', 'f4be363e03f8e10c75b4b52e25e9ce8344c2469f97edc33308ddd1f70d3c5ad5',)),
    'serverguidetitle': frozenset(('9a7f3759ca54bf3bdb8d63e800b5a57e5ea2f98ae78fb49736433eeb63570026',)),
    'servervoicerow': frozenset(('7d3783fc6528d82a8be5295880c4af21680466bfaab52d560f37157c1e438326',)),
    'storedresponseback': frozenset(('6b90f291c081e0c558f2697fea47254e4e2abe023357dd390e0c69c20826c54d',)),
}


def _check_templates(definitions, required=()):
    s = _api()
    for name in required:
        if name not in definitions:
            raise s.Refusal('missing server source template: '+name)
    for name, definition in definitions.items():
        if name in SUPPORTED_TEMPLATES:
            digest = s.sha(json.dumps(definition, sort_keys=True))
            if digest not in SUPPORTED_TEMPLATES[name]:
                raise s.Refusal('unsupported server source template: '+name)

class Planner:
    def __init__(self, adapter):
        self.s = _api()
        self.model = copy.copy(adapter)
        self.model.definitions = dict(adapter.definitions)
        _check_templates(self.model.definitions)
        self.model.inputs = dict(adapter.inputs)
        self.inputs = dict(adapter.inputs)
        self.model.read = self.read
        self._checked_templates = {}
        # Check the source definitions themselves, including transitive helper
        # templates in the common preamble, before an adapter can override or
        # lower them. The revision timestamp is a canonical data parameter;
        # its value is selected separately from generation-metadata.tex.
        for source in tuple(self.inputs):
            if source.endswith('.tex'):
                self.read(self.model.root / source)
        self.context = None
        self.occurrences = []
        self.tokens = {}
        self.assets = {}
        self.diagrams = Counter()

    def read(self, path):
        text = self.s._source_bytes(self.model.root, path, self.inputs).decode()
        if path.suffix == '.tex':
            digest = self.s.sha(text)
            if self._checked_templates.get(path) != digest:
                definitions, _ = self.s.web.command_definitions(text)
                _check_templates(definitions)
                self._checked_templates[path] = digest
        return text

    def origin(self, path, macro, start=0):
        if macro in SUPPORTED_TEMPLATES:
            _check_templates(self.model.definitions, (macro,))
        path = path.resolve()
        self.read(path)
        key = path.relative_to(self.model.root).as_posix()
        self.context = dict(path=key, sha256=self.inputs[key], macro=macro, selected_offset=start)

    def literal(self, text):
        marks = dict(Counter(c for c in text if c in SOURCE_MARKS))
        return [('text', self.s.semantics.normalized(text)), ('marks', marks)]

    def wrap(self, role, events, key=''):
        return [('open', role, key), *events, ('close', role, key)]

    def text(self, source):
        required = set(re.findall(r'\\([A-Za-z@]+)', source)) & SUPPORTED_TEMPLATES.keys()
        _check_templates(self.model.definitions, required)
        text = self.model.fragment_source(source)
        occurrence = len(self.occurrences) + 1
        context = self.context or dict(path=(self.model.leaf / 'main.tex').relative_to(self.model.root).as_posix())
        projection = dict(source=context, expanded_sha256=self.s.sha(text),
                          macro_state_sha256=self.s.sha(json.dumps(self.model.definitions, sort_keys=True)))
        selected = dict(body=text, head='', sources={},
                        chunks=[dict(path=context['path'], occurrence=occurrence, selected_line=1, text=text,
                                     projection=projection)],
                        selection=dict(entrypoint=context['path'], role='canonical-fragment',
                                       selection_digest=self.s.sha(json.dumps(projection, sort_keys=True))))
        try:
            ledger = self.s.semantics.expected_fragment_units(selected, self.s.web)
        except ValueError as error:
            raise self.s.Refusal('canonical assembly schedule cannot account for source: ' + str(error)) from error
        self.occurrences.append(dict(id=f'source-occurrence-{occurrence:06d}', context=projection,
                                     ledger_digest=ledger['ledger_digest'], units=ledger['units'],
                                     containers=ledger['containers']))
        events = []
        # Pandoc emits a fragment's notes after its body, with the source note
        # order preserved. All source units, including one-word notes, remain.
        for lane in ('body', 'notes'):
            for unit in ledger['units']:
                if unit['lane'] != lane:
                    continue
                if unit['kind'] in {'math', 'diagram'}:
                    raise self.s.Refusal('unimplemented assembly source atom: ' + unit['kind'])
                value = unit['expected']
                pieces = re.split(r'(serverscheduleblock\d+end)', value)
                unit_events = []
                for piece in pieces:
                    if piece in self.tokens:
                        unit_events.extend(self.tokens[piece])
                    elif piece:
                        unit_events += self.literal(piece)
                role = {'heading':'heading', 'table-cell':'cell', 'term':'term'}.get(unit['kind'])
                events += self.wrap(role, unit_events) if role else unit_events
        events.append(('marks', dict(Counter(c for c in text if c in SOURCE_MARKS))))
        return events

    def stash(self, events):
        token = 'SERVERSCHEDULEBLOCK' + str(len(self.tokens)).zfill(6) + 'END'
        self.tokens[token.casefold()] = events
        return '\n\n' + token + '\n\n'

    def diagram(self, name):
        m = self.model
        if m.asset_resolver is None:
            from _web_print_assets import server_asset
            resolver = server_asset
        else:
            resolver = m.asset_resolver
        variant = 'sung' if m.form != 'low' else 'trainer' if m.trainer else 'child'
        record = dict(resolver(m.root, variant, name))
        key = variant + ':' + name
        if record.get('id') != key or not record.get('src') or not record.get('sha256'):
            raise self.s.Refusal('assembly schedule lacks its canonical diagram asset')
        for path, digest in record['source_inputs'].items():
            if self.s.sha(self.s._source_bytes(m.root, m.root / path, self.inputs)) != digest:
                raise self.s.Refusal('assembly schedule diagram is stale: ' + path)
        pinned = {field: record[field] for field in ('id', 'src', 'sha256', 'bytes', 'source_inputs', 'includes_caption')}
        if key in self.assets and self.assets[key] != pinned:
            raise self.s.Refusal('assembly schedule asset changed during selection')
        self.assets[key] = pinned
        self.diagrams[name] += 1
        return [('asset', key, 'diagram-' + name + '-' + str(self.diagrams[name]), record['src'])]

    def block(self, name, a):
        if name in SUPPORTED_TEMPLATES:
            _check_templates(self.model.definitions, (name,))
        m = self.model
        t, lit, wrap = self.text, self.literal, self.wrap
        heading = lambda events: wrap('heading', events)
        if name == 'actionrowid':
            body = heading(lit(a[0]))
            for label, value in zip(('Cue', 'Actor', 'Action', 'Finish / next'), a[1:]):
                body += wrap('term', lit(label)) + t(value)
            return wrap('action', body, a[0])
        if name in {'LMAction', 'LMCompactTrainerAction'}:
            return wrap('action', heading(t(a[0] + ' · ' + a[1])) + t(r'\textbf{DO:} ' + a[2] + r'\par\textbf{HOW / FINISH:} ' + a[3]), a[0])
        if name in {'LMDialogueFirst', 'LMDialogueRepeat', 'LMDialogueLiteral'}:
            if name == 'LMDialogueLiteral':
                number, actor, cue, response = a
                sound = ''
            else:
                number, cue, identity = a
                actor, response = 'Priest', m.bank[identity]['latin']
                sound = m.bank[identity]['sound'] if name == 'LMDialogueFirst' else ''
            lanes = lit('℣ · ' + actor) + t(cue) + lit('℟ · Both') + t(r'\textbf{' + response + '}')
            if sound:
                lanes += lit('SAY IT') + t(sound)
            return wrap('response', heading(lit(number)) + wrap('paired-lanes', lanes), number)
        if name == 'LMPhraseBlock':
            return wrap('response', heading(t(a[0] + ' · ' + a[1])) + t(r'\textbf{' + a[2] + '}') + lit('SAY IT') + t(a[3]))
        if name in {'LMBranch', 'LMTrainerNote', 'TerminalNote'}:
            return wrap('branch', t(a[0]) + t(a[1]))
        if name in {'LMPageIntro', 'LMDiagramNote', 'LMModelChoice', 'masterybox'}:
            return t(a[0])
        if name == 'serverguidetitle':
            return heading(t(a[0])) + t(a[1]) + t(a[2])
        if name == 'PrintServerAnswer':
            identity = a[0]
            item = m.bank[identity]
            body = heading(t(item['title']))
            for label, value in (('YOUR JOB', m.lookup['job', identity]), ('HEAR', m.lookup['cue', identity]),
                                 ('RESPONSE', item['latin']), ('LATIN CHUNKS', item['learner']),
                                 ('SAY IT LIKE', item['sound']), ('MEANING', item['meaning'])):
                body += lit(label) + t(value)
            return wrap('response', body, 'response-' + identity)
        if name in {'PrintAightAnswer', 'PrintMassOrderVoiceMap', 'SolemnEveryRoleTrack', 'LMTitlePage', 'LMReadingKey', 'LMModelKeyLine', 'coachreference'}:
            value = m.definitions[name][2]
            value = re.sub(r'\\ifdefined\\LMTitleApparatus.*?\\fi', '', value, flags=re.S)
            if name == 'SolemnEveryRoleTrack':
                boxes = self.s.calls(value, 'parbox', 2)
                if len(boxes) != 1:
                    raise self.s.Refusal('canonical role reminder changed its source container')
                value = boxes[0][0][1]
            return self.tex(value)
        if name in {'rolecard', 'mcrolerow', 'MCSceneTile', 'SolemnMapStop'}:
            body = heading(t(a[0]))
            for value in a[1:]:
                body += self.tex(value)
            return wrap('role', body)
        if name in {'mcroleheading', 'actionsection'}:
            return heading(t(a[0]))
        if name == 'servervoicerow':
            voice = a[2 + (0 if m.form == 'low' else 1 if m.form == 'cantata' else 2)]
            return wrap('response', t(a[0]) + t(a[1]) + lit('Who answers') + t(voice))
        if name == 'LMRenderGenerationMetadata':
            return lit('Last revised (UTC): ' + m.revised)
        if name == 'TriptychRightsNotice':
            return self.tex(m.rights)
        if name == 'LMLaneHeadings':
            return wrap('paired-lanes', lit('℣ · Priest’s cue') + lit('℟ · Both answer'))
        if name in m.diagram_names:
            return self.diagram(name)
        raise self.s.Refusal('unimplemented assembly schedule macro: ' + name)

    def tex(self, source):
        m, s = self.model, self.s
        source = m.select(source)
        def hook(a):
            if a[0] != 'shipout/foreground':
                raise s.Refusal('unsupported source shipout hook')
            match = re.search(r'at\s*\([^)]*\)\s*\{', a[1])
            if match is None or r'\includegraphics' in a[1]:
                raise s.Refusal('shipout source text needs a selected asset')
            return s.web.brace_group(a[1], match.end()-1)[0]
        source = s.replace(source, 'AddToHookNext', 2, hook)
        definitions, source = s.web.command_definitions(source)
        _check_templates(definitions)
        m.definitions.update(definitions)
        source = s.without_environment_definitions(source)
        source = s.replace(source, 'TrainerIPARow', 1,
                           lambda a: r'\textbf{' + a[0] + '} & ' + s.tipa_unicode('/' + m.bank[a[0]]['ipa'] + '/') + r'\\' + '\n')
        for name, count in (('serveranswer', 6), ('RegisterServerData', 6), ('DefineResponseVoice', 4),
                            ('DefineResponseJob', 4), ('DefineResponseCue', 2), ('DefineResponseLesson', 2)):
            source = s.replace(source, name, count, lambda a: '')
        source = re.sub(r'\\(?:LowMass|MissaCantata|SolemnMass|CardsOnly|ResponseDataOnly|ChildBooklet|TrainerManual|LMSuppressTrainerMeaning)Guide(?:true|false)', '', source)
        source = re.sub(r'\\LMSuppressTrainerMeaning(?:true|false)', '', source)
        source = source.replace(r'\TriptychRightsNoticeRenderedtrue', '').replace(r'\AIDisplayDocumentRevisionTimestamp', '')
        commands = {'actionrowid':5, 'actionsection':1, 'rolecard':2, 'mcroleheading':1, 'mcrolerow':2,
                    'MCSceneTile':3, 'SolemnMapStop':4, 'servervoicerow':5, 'LMAction':4, 'LMCompactTrainerAction':4,
                    'LMBranch':2, 'LMTrainerNote':2, 'TerminalNote':2, 'LMPageIntro':1, 'LMDiagramNote':1,
                    'LMModelChoice':1, 'LMDialogueFirst':3, 'LMDialogueRepeat':3, 'LMDialogueLiteral':4,
                    'LMPhraseBlock':5, 'PrintServerAnswer':1, 'masterybox':1, 'serverguidetitle':3}
        events = [(start,end,name,a) for name,count in commands.items() for a,start,end in s.calls(source,name,count)]
        zero = {'PrintAightAnswer','PrintMassOrderVoiceMap','SolemnEveryRoleTrack','LMTitlePage','LMReadingKey','LMModelKeyLine',
                'LMRenderGenerationMetadata','TriptychRightsNotice','LMLaneHeadings','coachreference'} | m.diagram_names
        for name in zero:
            events += [(x.start(),x.end(),name,[]) for x in re.finditer(re.escape('\\'+name)+r'(?![A-Za-z@])',source)]
        output, offset = [], 0
        outer_context = self.context
        for start,end,name,a in sorted(events):
            if start < offset:
                continue
            output.append(source[offset:start])
            self.context = {**(outer_context or {}), 'macro':name, 'selected_offset':start}
            output.append(self.stash(self.block(name,a)))
            offset=end
        self.context=outer_context
        output.append(source[offset:])
        text=''.join(output)
        for name in ('actiontable','servervoicetable'):
            text=text.replace(r'\begin{'+name+'}','').replace(r'\end{'+name+'}','')
        text=s.replace(text,'label',1,lambda a: self.stash([]))
        text=re.sub(r'\\begin\{mcroleroute\}\{([^}]+)\}',lambda x:self.stash(self.wrap('heading', self.literal(x[1]+' · Every scene'))+self.text(m.definitions['MCRoleAlways'][2])),text)
        text=text.replace(r'\end{mcroleroute}','')
        box=re.compile(r'\\begin\{(learnerbox|coachbox|watchbox|familybox)\}\s*\{')
        while match:=box.search(text):
            title,end=s.web.brace_group(text,match.end()-1)
            stop=text.find(r'\end{'+match[1]+'}',end)
            if stop<0:
                raise s.Refusal('unclosed source teaching box')
            value=self.wrap('heading',self.text(title))+self.tex(text[end:stop])
            text=text[:match.start()]+self.stash(value)+text[stop+len(r'\end{'+match[1]+'}'):]
        for name,count in (('addcontentsline',3),('addtocontents',2),('microtypesetup',1),('titleformat',5),
                           ('titlespacing',4),('setcounter',2),('setlength',2),('addtolength',2),('enlargethispage',1)):
            text=s.replace(text,name,count,lambda a:'')
        text=text.replace(r'\global','')
        text=s.web.REGISTER_ASSIGNMENT_RE.sub('',text)
        text=re.sub(r'\\hrule(?:\s+height\s*[0-9.]+(?:pt|in|em|cm))?','',text)
        text=re.sub(r'\\(?:EndLMPage|rolecardstart|columnbreak|guidecontents|carddeckoddpage)(?![A-Za-z@])','',text)
        for opening,closing in ((r'\begin{deepstudy}',r'\end{deepstudy}'),(r'\begin{multicols}{2}',r'\end{multicols}')):
            text=text.replace(opening,'').replace(closing,'')
        text=s.web.drop_continuation_heads(s.web.terminate_swallowers(s.web.fix_column_specs(text)))
        return self.text(text)

    def guides(self):
        m,s=self.model,self.s
        parts=[]
        if m.form=='low':
            path=m.owner/'shared/low-mass-ceremony.tex'
            raw=self.read(path)
            begin=sorted((start,end,a,name) for name in ('BeginLMPage','BeginLMSingleScenePage','ContinueLMPairedScene') for a,start,end in s.calls(raw,name,3))
            self.origin(path,'document-prefix')
            parts.append(dict(id='title',kind='guide-title',events=self.tex(raw[:begin[0][0]])))
            for index,(start,end,a,name) in enumerate(begin):
                stop=begin[index+1][0] if index+1<len(begin) else len(raw)
                self.origin(path,name,end)
                body=self.tex(raw[end:stop])
                rail=self.tex(a[2]) if m.trainer else []
                heading=self.wrap('heading',self.text(a[0]+' · '+a[1]))
                if m.trainer:
                    body=self.wrap('trainer-layout',self.wrap('trainer-rail',rail)+body)
                parts.append(dict(id=f'scene-{index+1:02d}',kind='paired-scene',events=heading+body))
        else:
            path=m.leaf/'main.tex'
            _,body=s.web.split_document(self.read(path))
            def include(a):
                name=a[0]
                if name.endswith('sung-mass-diagrams'):
                    return ''
                target=m.root/'src'/m.provider/(name+('' if name.endswith('.tex') else '.tex'))
                if 'generation-metadata' in name:
                    return '\nLast revised (UTC): '+m.revised+'\n'
                return self.read(target)
            body=s.replace(body,'input',1,include)
            self.origin(path,'document-body')
            events=self.tex(body)
            self.origin(m.root/'src/common/preamble.tex','TriptychRightsNotice')
            events+=self.tex(m.rights)
            parts.append(dict(id='complete-guide',kind='guide',events=events))
        return parts


def source_schedule(adapter):
    p=Planner(adapter)
    if adapter.cards:
        from _web_print_server_card_schedule import plan_cards
        parts=plan_cards(p)
    else:
        parts=p.guides()
    for part in parts:
        marks = Counter()
        for event in part['events']:
            if event[0] == 'marks': marks.update(event[1])
        part['source_marks'] = dict(marks)
        part['events']=_compact(e for e in part['events'] if e[0] != 'marks')
    schedule=dict(schema=1,output_id=adapter.provider+'/'+adapter.output_id,parts=parts,
                  occurrences=p.occurrences,source_inputs=p.inputs,assets=p.assets)
    schedule['digest']=p.s.sha(json.dumps(schedule,sort_keys=True,separators=(',',':')))
    return schedule


class Actual(HTMLParser):
    blocks=set('address article aside blockquote br dd div dl dt figcaption figure footer h1 h2 h3 h4 h5 h6 header hr li main ol p section table tbody td th thead tr ul'.split())
    voids=set('area base br col embed hr img input link meta param source track wbr'.split())
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events=[]
        self.buffer=[]
        self.stack=[]
        self.hidden=0
        self.source_marks=Counter()

    def flush(self):
        text=_api().semantics.normalized(''.join(self.buffer))
        self.buffer=[]
        if text:self.events.append(('text',text))

    def handle_starttag(self,tag,attrs):
        a=dict(attrs);classes=set(a.get('class','').split())
        if ('hidden' in a or a.get('aria-hidden')=='true' and 'blank' not in classes or
                re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden)',a.get('style',''),re.I)):
            raise _api().Refusal('final assembly hides canonical source content')
        skip=self.hidden or a.get('id','').startswith('fnref') or bool(classes & {'footnote-ref','footnote-backref'})
        if tag in self.blocks:self.buffer.append(' ')
        role=key=None
        if not skip:
            if tag in {'h1','h2','h3','h4','h5','h6'}:role,key='heading',''
            elif tag in {'td','th'}:role,key='cell',''
            elif tag=='dt':role,key='term',''
            elif 'sheet' in classes:role,key='sheet',('low' if 'low' in classes else 'sung')+'/'+a.get('data-side','')+'/'+a.get('data-sheet','')
            elif 'grid' in classes:
                rows=re.fullmatch(r'--rows:\s*([34])\s*;?',a.get('style',''))
                role,key='grid',rows[1] if rows else ''
            elif 'face' in classes and 'blank' not in classes:role,key='face',a.get('data-unit-id','')
            elif 'face-header' in classes:role,key='face-header',''
            elif 'field' in classes:role,key='field',next((x for x in ('response','learner','sound','meaning') if x in classes),'')
            elif 'action' in classes:role,key='action',a.get('data-unit-id',a.get('data-source-action',''))
            elif tag=='article' and 'response' in classes:role,key='response',a.get('data-unit-id',a.get('data-dialogue',''))
            else:
                for name in ('answer','face-footer','action-body','sheet-duplex','sheet-notice','apparatus','branch','paired-lanes','role','trainer-layout','trainer-rail'):
                    if name in classes:
                        role,key=name,a.get('data-unit-id','') if name in {'sheet-duplex','sheet-notice','apparatus'} else ''
                        break
            if role:
                self.flush();self.events.append(('open',role,key))
            if tag=='img':
                self.flush()
                figure=next((frame[3] for frame in reversed(self.stack) if frame[0]=='figure'),{})
                self.events.append(('asset',figure.get('data-diagram-id',''),figure.get('data-unit-id',''),a.get('src','')))
        if tag not in self.voids:
            self.stack.append((tag,role,key,a,bool(skip)))
            self.hidden+=bool(skip)

    def handle_endtag(self,tag):
        if tag in self.voids:return
        if not self.stack or self.stack[-1][0]!=tag:
            raise _api().Refusal('final assembly has malformed HTML structure: '+tag)
        _,role,key,a,skip=self.stack.pop()
        self.hidden-=skip
        if role:
            self.flush();self.events.append(('close',role,key))
        if tag in self.blocks or tag=='span' and self.stack and self.stack[-1][1]=='face-header':self.buffer.append(' ')

    def handle_data(self,data):
        if not self.hidden:
            self.buffer.append(data)
            self.source_marks.update(c for c in data if c in SOURCE_MARKS)

    def finish(self):
        self.close();self.flush()
        if self.stack:raise _api().Refusal('final assembly has unclosed HTML')
        return _compact(self.events)


def verify_assembly(schedule, parts, assets, *, root):
    s=_api()
    if not isinstance(schedule,dict) or schedule.get('schema')!=1:
        raise s.Refusal('independent canonical assembly schedule is required')
    unsealed={key:value for key,value in schedule.items() if key!='digest'}
    digest=s.sha(json.dumps(unsealed,sort_keys=True,separators=(',',':')))
    if digest!=schedule.get('digest'):
        raise s.Refusal('canonical assembly schedule changed after source selection')
    for path, expected_hash in schedule['source_inputs'].items():
        if s.sha(s._source_bytes(root, root / path, {})) != expected_hash:
            raise s.Refusal('canonical assembly source changed during rendering: '+path)
    if [(p['id'],p['kind']) for p in parts]!=[(p['id'],p['kind']) for p in schedule['parts']]:
        raise s.Refusal('final assembly parts differ from the canonical source schedule')
    for expected,part in zip(schedule['parts'],parts):
        parser=Actual();parser.feed(part['html']);actual=parser.finish()
        if dict(parser.source_marks) != expected['source_marks']:
            raise s.Refusal('final assembly changed canonical response/cross/choice symbols in '+part['id']+': expected='+str(expected['source_marks'])+' actual='+str(dict(parser.source_marks)))
        if actual!=expected['events']:
            index=next((i for i,(left,right) in enumerate(zip(expected['events'],actual)) if left!=right),min(len(expected['events']),len(actual)))
            raise s.Refusal('final assembly lost canonical source text, role or asset in '+part['id']+' at event '+str(index)+': expected='+repr(expected['events'][index:index+1])[:1600]+' actual='+repr(actual[index:index+1])[:1600])
    actual_assets={item['id']:{field:item[field] for field in ('id','src','sha256','bytes','source_inputs','includes_caption')} for item in assets}
    if len(actual_assets)!=len(assets) or actual_assets!=schedule['assets']:
        raise s.Refusal('final assembly asset records differ from canonical source projections')
    return dict(status='pass',scope='canonical-source-occurrence-schedule-to-final-html',schedule_digest=digest,
                source_occurrences=len(schedule['occurrences']),source_units=sum(len(o['units']) for o in schedule['occurrences']),
                parts=len(parts),asset_instances=sum(e[0]=='asset' for p in schedule['parts'] for e in p['events']))
