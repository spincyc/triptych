"""Withdrawal metadata requires confirmed loci and actual unchanged PDF bytes."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import _bullarium_corrections as corrections
import test_bullarium_corrections as fixtures


class WithdrawalTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.CorrectionTests()
        self.fixture.setUp()
        self.root=self.fixture.root
        self.out=self.root/'withdrawals.json'
        d=self.fixture.doc
        self.evidence={'unit_id':d['id'],'current_document_id':d['id'],'original_document_id':d['id'],
            'known_correction_ids':[],'classification':'confirmed-fusion','artifact_id':d['artifact_id'],
            'artifact_sha256':d['sha256'],'segment_id':d['segment_id'],'physical_line_ranges':d['physical_line_ranges'],
            'affected_physical_line_ranges':[[5,5]],'native_word_evidence':[{'source_word_global_1':1,'value':'Synthetic fixture evidence.'}],
            'cache_path':'.scratch/not-a-durable-citation.xml'}
        self.plan={'schema':corrections.PLAN_SCHEMA,'initial_manifests':['initial.json'],
            'prior_receipts':[str(self.fixture.receipt.relative_to(self.root))],
            'withdrawals':[{'unit_id':d['id'],'prior_id':d['id'],'reason':'Confirmed synthetic source-order fixture.',
                            'evidence':self.evidence}]}

    def tearDown(self):
        self.fixture.tearDown()

    def build(self):
        self.fixture.write_json(self.fixture.plan_path,self.plan)
        return corrections.build_withdrawals(self.root,self.fixture.plan_path,self.out,fixtures.REVISION)

    def test_exact_pdf_source_and_all_old_bytes_are_preserved(self):
        before=self.fixture.frozen_files()
        result=self.build()
        self.assertEqual(result['documents'],[])
        self.assertIsNone(result['supersessions'][0]['replacement'])
        self.assertEqual(result['supersessions'][0]['prior']['artifact_id'],self.fixture.doc['artifact_id'])
        self.assertNotIn('cache_path',result['affected_units'][0]['source_order_evidence'])
        self.assertEqual(before,{p:v for p,v in self.fixture.frozen_files().items() if p!=self.out})

    def test_uncertain_finding_cannot_be_withdrawn_as_confirmed(self):
        self.evidence['classification']='ambiguous'
        with self.assertRaisesRegex(ValueError,'confirmed current'):
            self.build()
        self.assertFalse(self.out.exists())

    def test_locus_must_belong_to_the_actual_selected_source(self):
        self.evidence['affected_physical_line_ranges']=[[11,11]]
        with self.assertRaisesRegex(ValueError,'outside the prior selected'):
            self.build()

    def test_wrong_controller_evidence_is_refused(self):
        self.evidence['artifact_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'disagrees with current source'):
            self.build()

    def test_pdf_tampering_is_refused(self):
        (self.fixture.receipt.parent/'edition/prior.pdf').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'PDF SHA-256 mismatch'):
            self.build()

    def test_cumulative_variants_are_revalidated_and_replay_is_identical(self):
        self.build()
        second=self.fixture.add_receipt('prior-two',b'%PDF-1.4\nDifferent synthetic fixture output.\n')
        self.plan['prior_receipts'].append(str(second.relative_to(self.root)))
        result=self.build()
        self.assertEqual(len(result['supersessions']),2)
        self.assertEqual(len(result['affected_units']),1)
        before=self.out.read_bytes()
        self.build()
        self.assertEqual(self.out.read_bytes(),before)

    def test_effective_row_revision_binds_the_older_frozen_receipt(self):
        self.fixture.cumulative_initial()
        self.build()
        receipt=json.loads(self.fixture.receipt.read_text())
        receipt['documents'][0]['render_revision']=fixtures.REVISION
        self.fixture.write_json(self.fixture.receipt,receipt)
        with self.assertRaisesRegex(ValueError,'render revision disagree'):
            self.build()

    def test_retired_alias_is_not_an_active_withdrawal_predecessor(self):
        replacement=copy.deepcopy(self.fixture.doc)
        replacement['id']+='.metadata-v2'
        self.fixture.write_json(self.fixture.initial,{'schema':corrections.SCHEMA,'revision':fixtures.PRIOR_REVISION,
            'documents':[self.fixture.doc,replacement]})
        self.evidence['current_document_id']=replacement['id']
        self.evidence['known_correction_ids']=[replacement['id']]
        with self.assertRaisesRegex(ValueError,'current corrected identity'):
            self.build()


if __name__=='__main__':
    unittest.main()
