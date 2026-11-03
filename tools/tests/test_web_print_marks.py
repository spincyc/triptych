"""Five-mark source/provenance boundaries and explicit offline delivery."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import struct
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import _artifact_store as transport
import _web_print_marks as marks


class MarksTests(unittest.TestCase):
    def setUp(self):
        scratch=ROOT/'.scratch/web-print-marks/tests';scratch.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.pack=self.root/'.scratch/pack'
        self.data=json.loads((ROOT/marks.INDEX_PATH).read_text())
        for row in (self.data['license'],self.data['recipe_reference']):
            p=self.root/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/row['path']).read_bytes())
        raw=bytearray(64);raw[:8]=b'wOF2\x00\x01\x00\x00';struct.pack_into('>I',raw,8,len(raw))
        self.payload=bytes(raw);font=self.data['font'];font.update(sha256=marks.sha(raw),bytes=len(raw),path=marks.PREFIX+marks.sha(raw)+'.woff2')
        self.data['derivation'].update(output_woff2_sha256=font['sha256'],output_woff2_bytes=font['bytes'])
        input=self.root/'.scratch/input.woff2';input.parent.mkdir(parents=True);input.write_bytes(raw)
        entry={k:font[k] for k in ('path','sha256','bytes','media_type')};entry['kind']='font-software'
        archives,entries=transport.pack_delivery_archives(self.root,self.pack,[entry],resolver=lambda r,p:input,release='test',archive_prefix='marks')
        self.data['delivery']={'schema':marks.DELIVERY_SCHEMA,'archives':archives,'artifacts':entries};self.save()

    def save(self):
        self.data['manifest_digest']=marks.sha(marks.canonical({k:v for k,v in self.data.items() if k!='manifest_digest'}))
        transport._json(self.root/marks.INDEX_PATH,self.data)

    def hydrate(self):return marks.hydrate(self.root,archive_dir=self.pack)

    def test_metadata_only_and_missing_payload_never_fetch_or_run_native(self):
        with patch.object(transport,'urlopen',side_effect=AssertionError('network')),patch('subprocess.run',side_effect=AssertionError('native')),patch('subprocess.Popen',side_effect=AssertionError('native')):
            self.assertEqual(marks.check(self.root)['unicode_range'],marks.UNICODE_RANGE)
            with self.assertRaises(FileNotFoundError):marks.font_asset(self.root)
            with self.assertRaises(FileNotFoundError):marks.hydrate(self.root)

    def test_offline_roundtrip_exact_font_and_existing_canonical_license(self):
        with patch.object(transport,'urlopen',side_effect=AssertionError('network')),patch('subprocess.run',side_effect=AssertionError('native')):
            self.assertEqual(self.hydrate()['hydrated'],1)
            row=marks.font_asset(self.root)
            self.assertEqual(row['body'],self.payload);self.assertEqual(row['family'],'Triptych Source Marks')
            self.assertEqual(row['unicode_range'],'U+211F,U+2123,U+21A9,U+2610,U+2720')
            self.assertEqual(row['license']['src'],'shared/fonts/OFL-Junicode.txt')
            self.assertEqual(marks.sha(row['license']['body']),marks.LICENSE_SHA)
            self.assertNotIn('body',marks.font_asset(self.root,include_body=False))

    def test_fetch_requires_explicit_true(self):
        archive=self.data['delivery']['archives'][0]
        with patch.object(transport,'urlopen',return_value=io.BytesIO((self.pack/archive['name']).read_bytes())) as fetch:
            self.assertEqual(marks.hydrate(self.root,fetch=True)['hydrated'],1);fetch.assert_called_once()

    def test_exact_five_range_cannot_be_broadened_or_alias_source_unicode(self):
        self.data['font']['unicode_range']+=',U+0041';self.save()
        with self.assertRaisesRegex(marks.MarksError,'identity/range'):marks.check(self.root)

    def test_checkbox_is_not_falsely_claimed_upstream(self):
        self.data['derivation']['source_glyphs']['U+2610']=copy.deepcopy(self.data['derivation']['output_glyphs']['U+2610']);self.save()
        with self.assertRaisesRegex(marks.MarksError,'cmap scope'):marks.check(self.root)

    def test_inherited_outline_or_metrics_tamper_rejected(self):
        self.data['derivation']['output_glyphs']['U+211F']['advance']+=1;self.save()
        with self.assertRaisesRegex(marks.MarksError,'shape or metrics'):marks.check(self.root)

    def test_checkbox_geometry_and_hole_are_deterministic(self):
        a=marks.ballot_box_geometry(1000,663);self.assertEqual(a,marks.ballot_box_geometry(1000,663))
        self.assertEqual((a['stroke'],a['sidebearing'],a['advance']),(46,60,783))
        def winding(points,x,y):
            result=0
            for i,(a,b) in enumerate(points):
                c,d=points[(i+1)%len(points)]
                cross=(c-a)*(y-b)-(x-a)*(d-b)
                if b<=y<d and cross>0:result+=1
                elif d<=y<b and cross<0:result-=1
            return result
        outer,inner=a['outer_clockwise'],a['inner_counterclockwise']
        self.assertEqual(winding(outer,391,331)+winding(inner,391,331),0)
        self.assertNotEqual(winding(outer,70,331)+winding(inner,70,331),0)
        self.assertEqual(winding(outer,0,331)+winding(inner,0,331),0)
        self.data['derivation']['added_ballot_box']['inner_counterclockwise'].reverse();self.save()
        with self.assertRaisesRegex(marks.MarksError,'construction'):marks.check(self.root)

    def test_upstream_and_canonical_license_pins_are_strict(self):
        self.data['upstream']['commit']='0'*40;self.save()
        with self.assertRaisesRegex(marks.MarksError,'upstream provenance'):marks.check(self.root)

    def test_existing_notice_changed_or_new_license_owner_rejected(self):
        self.data['license']['path']='src/common/new-OFL.txt';self.save()
        with self.assertRaisesRegex(marks.MarksError,'canonical license'):marks.check(self.root)

    def test_protected_copyright_and_license_name_changes_rejected(self):
        self.data['derivation']['output_protected_names']['0']='f'*64;self.save()
        with self.assertRaisesRegex(marks.MarksError,'origin/license'):marks.check(self.root)

    def test_roundtrip_proof_cannot_hide_changed_shape(self):
        self.data['derivation']['roundtrip_glyphs']['U+2610']['outline_sha256']='0'*64;self.save()
        with self.assertRaisesRegex(marks.MarksError,'roundtrip outline'):marks.check(self.root)

    def test_cached_bytes_tampered_rejected(self):
        self.hydrate();entry=self.data['delivery']['artifacts'][0];path=transport.cache_path(self.root,entry)
        path.chmod(0o600);path.write_bytes(self.payload+b'x')
        with self.assertRaises(ValueError):marks.font_asset(self.root)

    def test_symlink_cache_rejected(self):
        self.hydrate();entry=self.data['delivery']['artifacts'][0];path=transport.cache_path(self.root,entry)
        moved=path.with_name('moved.woff2');path.rename(moved);path.symlink_to(moved)
        with self.assertRaises(ValueError):marks.font_asset(self.root)

    def test_traversal_or_link_archive_members_rejected(self):
        for link in (False,True):
            with self.subTest(link=link):
                archive=self.data['delivery']['archives'][0];path=self.pack/archive['name']
                with tarfile.open(path,'w') as stream:
                    info=tarfile.TarInfo('../escape')
                    if link:info.type=tarfile.SYMTYPE;info.linkname='../escape'
                    else:info.size=len(self.payload)
                    stream.addfile(info,None if link else io.BytesIO(self.payload))
                archive.update(id=transport._digest(path),sha256=transport._digest(path),bytes=path.stat().st_size)
                self.data['delivery']['artifacts'][0]['archive']=archive['id'];self.save()
                with self.assertRaises(ValueError):self.hydrate()
                self.assertFalse((self.root/'escape').exists())

    def test_duplicate_manifest_keys_and_wrong_font_type_rejected(self):
        (self.root/marks.INDEX_PATH).write_text('{"schema":"a","schema":"b"}')
        with self.assertRaises(marks.MarksError):marks.load_index(self.root)
        for body in (b'not a font',b'wOF2'+bytes(60)):
            with self.assertRaises(marks.MarksError):marks._typed(body)

    def test_sfnt_checksum_and_name_rename_preserve_origin_records(self):
        head=bytearray(54);struct.pack_into('>H',head,18,1000)
        rows=[];strings=bytearray()
        for n,text in [(0,'Copyright upstream'),(1,'Junicode'),(2,'Regular'),(3,'Original'),(4,'Junicode Regular'),(5,'Version 2.003'),(6,'Junicode-Regular'),(13,'OFL-1.1'),(14,'https://example.org/OFL')]:
            b=text.encode('utf-16-be');rows.append(struct.pack('>HHHHHH',3,1,0x409,n,len(b),len(strings)));strings.extend(b)
        name=struct.pack('>HHH',0,len(rows),6+12*len(rows))+b''.join(rows)+strings
        body=marks._build_sfnt({b'head':bytes(head),b'name':name})
        renamed=marks.rename_sfnt(body);before=marks.sfnt_tables(body);after=marks.sfnt_tables(renamed)
        self.assertEqual(marks._protected(before),marks._protected(after))
        names={n:b.decode('utf-16-be') for _,_,_,n,b in marks.name_records(after)}
        self.assertEqual(names[1],marks.FAMILY);self.assertIn('project-authored U+2610',names[10])
        with self.assertRaises(marks.MarksError):marks.sfnt_tables(body[:-1]+b'x')


if __name__=='__main__':unittest.main()
