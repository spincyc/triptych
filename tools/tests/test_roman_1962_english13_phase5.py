"""English13: bounded historical words, separate literal recipient-byte guards.

No protected1962 transcript, raster, scratch path or normalized donor lookup.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
import copy, csv, hashlib, io, json, re, sys, tomllib, unicodedata, unittest
from tools.tests import _source_batch_guards as source_batch
ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
def sha(v):
    return hashlib.sha256(v.encode() if isinstance(v, str) else v).hexdigest()
def digest(v):
    return sha(json.dumps(v, sort_keys=True, ensure_ascii=False))
def words(v):
    v = v.casefold().replace("æ", "ae").replace("œ", "oe")
    return re.findall("[a-z]+|[0-9]+", "".join(c for c in unicodedata.normalize("NFKD", v) if not unicodedata.combining(c)))
def wordsha(v):
    return sha(json.dumps(v, ensure_ascii=False))
def listed_word_projection(tokens, differences):
    """Test-only historical collation, NEVER a recipient or donor lookup."""
    projected = list(tokens)
    for d in differences:
        at = d["historical_word_number_1_based"] - 1
        if at != d["actual_1962_word_number_1_based"] - 1 or projected[at] != d["historical_token"]:
            raise ValueError("listed historical word not at its exact inspected position")
        target = d["actual_1962_token"]
        if projected[at].replace("j", "i") != target.replace("j", "i"):
            raise ValueError("not the authorized consonantal i/j transformation")
        projected[at] = target
    return projected
ORACLES = {('apparitione-beatae-mariae-virginis-immaculatae', 'main', 'Collect', 'all', 1): {'canonical_bytes': 223,
                                                                                   'canonical_sha256': '6ee41d8065bf62d6bdb9cb9ecbc1847b2fd44904f6e3372d08b627df7e7eec7e',
                                                                                   'english': 'O God, Who by '
                                                                                              'the immaculate '
                                                                                              'conception of '
                                                                                              'the Virgin '
                                                                                              'didst prepare a '
                                                                                              'worthy '
                                                                                              'habitation for '
                                                                                              'Thy Son, we '
                                                                                              'humbly beseech '
                                                                                              'Thee that, '
                                                                                              'worthily '
                                                                                              'celebrating the '
                                                                                              'apparition of '
                                                                                              'the same '
                                                                                              'Virgin, we may '
                                                                                              'obtain health '
                                                                                              'of soul and '
                                                                                              'body. Through '
                                                                                              'the same.',
                                                                                   'line': 2,
                                                                                   'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-lourdes-collect',
                                                                                   'receipt': {'actual_historical_ending': 'Per '
                                                                                                                           'eundem '
                                                                                                                           'Dominum.',
                                                                                               'actual_seed_ending': 'Per '
                                                                                                                     'eundem '
                                                                                                                     'Dominum.',
                                                                                               'actual_seed_transcription_sha256': 'ba4ca4ee6694f3994e3e69dd9703f8694f75da5caae694e7d520b3cf687ec7b4',
                                                                                               'actual_seed_word_count': 28,
                                                                                               'actual_seed_words_sha256': 'f2ca8e9908172097bec859b6605dc3dcaeb9c8cdda715149a9b619b9ded882aa',
                                                                                               'candidate_id': 'lasance-next-lourdes-collect',
                                                                                               'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                                               'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                                               'differences': [{'actual_1962_token': 'eiusdem',
                                                                                                                'actual_1962_word_number_1_based': 17,
                                                                                                                'classification': 'transformation, '
                                                                                                                                  'not '
                                                                                                                                  'changed '
                                                                                                                                  'word/ending, '
                                                                                                                                  'not '
                                                                                                                                  'OCR '
                                                                                                                                  'correction',
                                                                                                                'historical_token': 'ejusdem',
                                                                                                                'historical_word_number_1_based': 17,
                                                                                                                'kind': 'declared-consonantal-i-j-orthographic-transformation'}],
                                                                                               'english_served_sha256': '3d0a11ce6fb797b7ab611bd1b6c64edc5d59aef6dce06a646f86b3faca1c968d',
                                                                                               'english_with_lf_sha256': '6c4eb256e0d06ce1aedae311e61e094dbb45c33504992683fd40ec7ccb924c2d',
                                                                                               'historical_after_listed_transformations_words_sha256': 'f2ca8e9908172097bec859b6605dc3dcaeb9c8cdda715149a9b619b9ded882aa',
                                                                                               'historical_latin_transcription_sha256': '2c774c49cce77f06eba4289ed3ea799f16106d8f17f4c4c14d6eeaad577c7307',
                                                                                               'historical_word_count': 28,
                                                                                               'historical_words_sha256': '0b9c6745e22f6b7af3f79346e04e69912cf750a56975ec92474d7041249d6ad3',
                                                                                               'not_a_normalized_recipient_join': True,
                                                                                               'not_raw_glyph_or_1962_byte_identity': True,
                                                                                               'unlisted_word_or_ending_differences': []},
                                                                                   'references': {'roman-1962': [{'form': '',
                                                                                                                  'kind': 'marian',
                                                                                                                  'mass': 'apparitione-beatae-mariae-virginis-immaculatae',
                                                                                                                  'proper': 'Collect'}],
                                                                                                  'roman-pre-1955': [{'form': '',
                                                                                                                      'kind': 'marian',
                                                                                                                      'mass': 'apparitione-beatae-mariae-virginis-immaculatae',
                                                                                                                      'proper': 'Collect'}]},
                                                                                   'seed_context': 'Complete '
                                                                                                   'own '
                                                                                                   'actual1962 '
                                                                                                   'prayer and '
                                                                                                   'ending '
                                                                                                   'separately '
                                                                                                   'inspected '
                                                                                                   'for this '
                                                                                                   'English '
                                                                                                   'binding.',
                                                                                   'seed_locus': 'printed p. '
                                                                                                 '473, no. '
                                                                                                 '2165; '
                                                                                                 'artifact PDF '
                                                                                                 'p. 554; '
                                                                                                 'right',
                                                                                   'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-lourdes-collect-seed',
                                                                                   'seed_pdf_page': 554,
                                                                                   'seed_unit': 2165,
                                                                                   'source_context': 'February '
                                                                                                     '11 '
                                                                                                     'Apparition '
                                                                                                     'of the '
                                                                                                     'Blessed '
                                                                                                     'Virgin '
                                                                                                     'Mary '
                                                                                                     'Immaculate, '
                                                                                                     'Prayer',
                                                                                   'source_key': 'lourdes-collect',
                                                                                   'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-lourdes-collect',
                                                                                   'source_pdf_pages': [915],
                                                                                   'source_printed_pages': ['916']},
 ('apparitione-beatae-mariae-virginis-immaculatae', 'main', 'Secret', 'all', 1): {'canonical_bytes': 190,
                                                                                  'canonical_sha256': '962082fc0df7d2e5655ce79f737d221d1c2fd7b72f03d99e10959686041b02d5',
                                                                                  'english': 'May the '
                                                                                             'sacrifice of '
                                                                                             'praise which we '
                                                                                             'offer Thee, O '
                                                                                             'Lord, by the '
                                                                                             'merits of the '
                                                                                             'glorious and '
                                                                                             'immaculate '
                                                                                             'Virgin, be as an '
                                                                                             'odor of '
                                                                                             'fragrance unto '
                                                                                             'Thee and bring '
                                                                                             'down upon us '
                                                                                             'health of body '
                                                                                             'and soul. '
                                                                                             'Through our '
                                                                                             'Lord.',
                                                                                  'line': 3,
                                                                                  'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-lourdes-secret',
                                                                                  'receipt': {'actual_historical_ending': 'Per '
                                                                                                                          'Dominum.',
                                                                                              'actual_seed_ending': 'Per '
                                                                                                                    'Dominum.',
                                                                                              'actual_seed_transcription_sha256': 'd54d74f6551f140e6323112e69b074328c8c4baabb952ec48a8a7a2f7c66f38b',
                                                                                              'actual_seed_word_count': 27,
                                                                                              'actual_seed_words_sha256': 'cd9d7f50b9b6899b903ffb395e62d774f03693a1037abbbbc08032ac63be901f',
                                                                                              'candidate_id': 'lasance-next-lourdes-secret',
                                                                                              'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                                              'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                                              'differences': [],
                                                                                              'english_served_sha256': '4a3da97f27666fce4feadc72167ec384d2e5b86b51e9675e269a5d8a103c4009',
                                                                                              'english_with_lf_sha256': '9ed066e2cbaf3e419584d3772fb5f74e027b343d59dc1382d38445c29ae7c35f',
                                                                                              'historical_after_listed_transformations_words_sha256': 'cd9d7f50b9b6899b903ffb395e62d774f03693a1037abbbbc08032ac63be901f',
                                                                                              'historical_latin_transcription_sha256': 'd54d74f6551f140e6323112e69b074328c8c4baabb952ec48a8a7a2f7c66f38b',
                                                                                              'historical_word_count': 27,
                                                                                              'historical_words_sha256': 'cd9d7f50b9b6899b903ffb395e62d774f03693a1037abbbbc08032ac63be901f',
                                                                                              'not_a_normalized_recipient_join': True,
                                                                                              'not_raw_glyph_or_1962_byte_identity': True,
                                                                                              'unlisted_word_or_ending_differences': []},
                                                                                  'references': {'roman-1962': [{'form': '',
                                                                                                                 'kind': 'marian',
                                                                                                                 'mass': 'apparitione-beatae-mariae-virginis-immaculatae',
                                                                                                                 'proper': 'Secret'}],
                                                                                                 'roman-pre-1955': [{'form': '',
                                                                                                                     'kind': 'marian',
                                                                                                                     'mass': 'apparitione-beatae-mariae-virginis-immaculatae',
                                                                                                                     'proper': 'Secret'}]},
                                                                                  'seed_context': 'Complete '
                                                                                                  'own '
                                                                                                  'actual1962 '
                                                                                                  'prayer and '
                                                                                                  'ending '
                                                                                                  'separately '
                                                                                                  'inspected '
                                                                                                  'for this '
                                                                                                  'English '
                                                                                                  'binding.',
                                                                                  'seed_locus': 'printed p. '
                                                                                                '474, no. '
                                                                                                '2173; '
                                                                                                'artifact PDF '
                                                                                                'p. 555; right',
                                                                                  'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-lourdes-secret-seed',
                                                                                  'seed_pdf_page': 555,
                                                                                  'seed_unit': 2173,
                                                                                  'source_context': 'February '
                                                                                                    '11 '
                                                                                                    'Apparition, '
                                                                                                    'Secret',
                                                                                  'source_key': 'lourdes-secret',
                                                                                  'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-lourdes-secret',
                                                                                  'source_pdf_pages': [917],
                                                                                  'source_printed_pages': ['918']},
 ('comm-ss-sergii-bacchi-marcelli-apuleii', 'main', 'Postcommunion', 'all', 1): {'canonical_bytes': 197,
                                                                                 'canonical_sha256': 'e21b7428f2efd8030cbe61e0d12e4fde5c58d42185e8721c6f046dfd127c73ed',
                                                                                 'english': 'May we be '
                                                                                            'fortified, O '
                                                                                            'Lord, by the '
                                                                                            'reception of Thy '
                                                                                            'sacraments, and '
                                                                                            'protected, '
                                                                                            'through the '
                                                                                            'intercession of '
                                                                                            'Thy holy martyrs, '
                                                                                            'Sergius, Bacchus, '
                                                                                            'Marcellus, and '
                                                                                            'Apuleius, by '
                                                                                            'heavenly armor '
                                                                                            'against all the '
                                                                                            'malice that '
                                                                                            'assaileth us. '
                                                                                            'Through our Lord.',
                                                                                 'line': 4,
                                                                                 'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-oct7-martyrs-postcommunion',
                                                                                 'receipt': {'actual_historical_ending': 'Per '
                                                                                                                         'Dominum.',
                                                                                             'actual_seed_ending': 'Per '
                                                                                                                   'Dominum.',
                                                                                             'actual_seed_transcription_sha256': '2128f7fecbd89a936b57ebb9e8b88271d772170cb7a2a213f6caa5d09252e5f0',
                                                                                             'actual_seed_word_count': 23,
                                                                                             'actual_seed_words_sha256': '9d6ed8aa174afc191b45aa87471345ec4241802732dd2768a6b68d8853f88b95',
                                                                                             'candidate_id': 'lasance-next-oct7-martyrs-postcommunion',
                                                                                             'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                                             'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                                             'differences': [],
                                                                                             'english_served_sha256': '2648c61357ab80b34d33c9e7f9b0d5330a6e5bc4db9be67b58c144f94c5e58bc',
                                                                                             'english_with_lf_sha256': 'e4c51ce926eae6c9092efc026f98171639b56f16c20bade74a3206799b1cf733',
                                                                                             'historical_after_listed_transformations_words_sha256': '9d6ed8aa174afc191b45aa87471345ec4241802732dd2768a6b68d8853f88b95',
                                                                                             'historical_latin_transcription_sha256': '2128f7fecbd89a936b57ebb9e8b88271d772170cb7a2a213f6caa5d09252e5f0',
                                                                                             'historical_word_count': 23,
                                                                                             'historical_words_sha256': '9d6ed8aa174afc191b45aa87471345ec4241802732dd2768a6b68d8853f88b95',
                                                                                             'not_a_normalized_recipient_join': True,
                                                                                             'not_raw_glyph_or_1962_byte_identity': True,
                                                                                             'unlisted_word_or_ending_differences': []},
                                                                                 'references': {'roman-1962': [{'form': '',
                                                                                                                'kind': 'sanctoral',
                                                                                                                'mass': 'comm-ss-sergii-bacchi-marcelli-apuleii',
                                                                                                                'proper': 'Postcommunion'}],
                                                                                                'roman-pre-1955': [{'form': '',
                                                                                                                    'kind': 'sanctoral',
                                                                                                                    'mass': 'comm-ss-sergii-bacchi-marcelli-apuleii',
                                                                                                                    'proper': 'Postcommunion'}]},
                                                                                 'seed_context': ' Separate '
                                                                                                 'no. 3817 '
                                                                                                 'under '
                                                                                                 'October 8, '
                                                                                                 'marked P; '
                                                                                                 'not no. 3814 '
                                                                                                 'despite same '
                                                                                                 'words on the '
                                                                                                 'same page. ',
                                                                                 'seed_locus': 'printed p. '
                                                                                               '681, no. 3817; '
                                                                                               'artifact PDF '
                                                                                               'p. 762; left',
                                                                                 'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-oct7-martyrs-postcommunion-seed',
                                                                                 'seed_pdf_page': 762,
                                                                                 'seed_unit': 3817,
                                                                                 'source_context': 'October 7 '
                                                                                                   'Commemoration '
                                                                                                   'Holy '
                                                                                                   'Martyrs '
                                                                                                   'Sergius '
                                                                                                   'Bacchus '
                                                                                                   'Marcellus '
                                                                                                   'and '
                                                                                                   'Apuleius, '
                                                                                                   'Postcommunion',
                                                                                 'source_key': 'oct7-martyrs-postcommunion',
                                                                                 'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-oct7-martyrs-postcommunion',
                                                                                 'source_pdf_pages': [1224],
                                                                                 'source_printed_pages': ['1229']},
 ('comm-ss-sergii-bacchi-marcelli-apuleii', 'main', 'Secret', 'all', 1): {'canonical_bytes': 131,
                                                                          'canonical_sha256': '3b312da3ef6bbaabae27f02bf13d00143847fe89ce45bb1917cd3f5b160e479a',
                                                                          'english': 'May this sacrifice that '
                                                                                     'is about to be offered '
                                                                                     'cause Thy majesty to be '
                                                                                     'appeased toward us, O '
                                                                                     'Lord, by the worthy '
                                                                                     'prayer of Thy saints. '
                                                                                     'Through our Lord.',
                                                                          'line': 5,
                                                                          'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-oct7-martyrs-secret',
                                                                          'receipt': {'actual_historical_ending': 'Per '
                                                                                                                  'Dominum.',
                                                                                      'actual_seed_ending': 'Per '
                                                                                                            'Dominum.',
                                                                                      'actual_seed_transcription_sha256': '318a680830070fec4dc0798395e44f498fc82176794c1c765c8dd0bc8d519899',
                                                                                      'actual_seed_word_count': 16,
                                                                                      'actual_seed_words_sha256': 'fa722f3da1a71d7fd36e26c85d5cd163d2cd514b9e6fadd06d7ba350988b4143',
                                                                                      'candidate_id': 'lasance-next-oct7-martyrs-secret',
                                                                                      'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                                      'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                                      'differences': [{'actual_1962_token': 'maiestatem',
                                                                                                       'actual_1962_word_number_1_based': 1,
                                                                                                       'classification': 'transformation, '
                                                                                                                         'not '
                                                                                                                         'changed '
                                                                                                                         'word/ending, '
                                                                                                                         'not '
                                                                                                                         'OCR '
                                                                                                                         'correction',
                                                                                                       'historical_token': 'majestatem',
                                                                                                       'historical_word_number_1_based': 1,
                                                                                                       'kind': 'declared-consonantal-i-j-orthographic-transformation'}],
                                                                                      'english_served_sha256': '5cd688081823093bc162b0b247e83f3f0d9005f9ee4522933d39e03682fd8511',
                                                                                      'english_with_lf_sha256': '575bf2e63c1178d88ec5e50e475112c1cdc97f5e267a86e728b3355981220802',
                                                                                      'historical_after_listed_transformations_words_sha256': 'fa722f3da1a71d7fd36e26c85d5cd163d2cd514b9e6fadd06d7ba350988b4143',
                                                                                      'historical_latin_transcription_sha256': '5d93cd44e80f39f5de4b702007568ba446ce1054ad64571961c35b662074c0dc',
                                                                                      'historical_word_count': 16,
                                                                                      'historical_words_sha256': '55f55d7aee6ed4722500e215e0689f7868b65c2d95aa74b1d13b0726559cdadb',
                                                                                      'not_a_normalized_recipient_join': True,
                                                                                      'not_raw_glyph_or_1962_byte_identity': True,
                                                                                      'unlisted_word_or_ending_differences': []},
                                                                          'references': {'roman-1962': [{'form': '',
                                                                                                         'kind': 'sanctoral',
                                                                                                         'mass': 'comm-ss-sergii-bacchi-marcelli-apuleii',
                                                                                                         'proper': 'Secret'}],
                                                                                         'roman-pre-1955': [{'form': '',
                                                                                                             'kind': 'sanctoral',
                                                                                                             'mass': 'comm-ss-sergii-bacchi-marcelli-apuleii',
                                                                                                             'proper': 'Secret'}]},
                                                                          'seed_context': ' 1962 October 8 '
                                                                                          'commemoration '
                                                                                          'versus Lasance '
                                                                                          'October 7 '
                                                                                          'commemoration; '
                                                                                          'prayer text and '
                                                                                          'actual names, not '
                                                                                          'calendar date, are '
                                                                                          'the join. ',
                                                                          'seed_locus': 'printed p. 681, no. '
                                                                                        '3816; artifact PDF p. '
                                                                                        '762; left',
                                                                          'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-oct7-martyrs-secret-seed',
                                                                          'seed_pdf_page': 762,
                                                                          'seed_unit': 3816,
                                                                          'source_context': 'October 7 '
                                                                                            'Commemoration '
                                                                                            'Holy Martyrs '
                                                                                            'Sergius Bacchus '
                                                                                            'Marcellus and '
                                                                                            'Apuleius, Secret '
                                                                                            'across page break',
                                                                          'source_key': 'oct7-martyrs-secret',
                                                                          'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-oct7-martyrs-secret',
                                                                          'source_pdf_pages': [1223, 1224],
                                                                          'source_printed_pages': ['1228',
                                                                                                   '1229']},
 ('commune-plurimorum-martyrum-3', 'main', 'Collect', 'all', 1): {'canonical_bytes': 161,
                                                                  'canonical_sha256': '59b0bdb4319ca305233c629223f74e5504399f9d5a9895b4e5e664b0f6e19e7c',
                                                                  'english': 'O God, Who dost gladden us by '
                                                                             'the annual solemnity of Thy '
                                                                             'martyrs, N. and N., mercifully '
                                                                             'grant that we be kindled by the '
                                                                             'example of those in whose merits '
                                                                             'we rejoice. Through our Lord.',
                                                                  'line': 6,
                                                                  'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-paschal-plural-martyrs-extra-collect',
                                                                  'receipt': {'actual_historical_ending': 'Per '
                                                                                                          'Dominum.',
                                                                              'actual_seed_ending': 'Per '
                                                                                                    'Dominum.',
                                                                              'actual_seed_transcription_sha256': 'd8f7d9b34ca7af0e4325156cf0c441a6160c76c826d8e935eaf9a9f49ee49150',
                                                                              'actual_seed_word_count': 22,
                                                                              'actual_seed_words_sha256': 'f93a02db3ed22fcff8d1e2b392b5760434f6365aeb6986d1c4487b297e4ca925',
                                                                              'candidate_id': 'lasance-next-paschal-plural-martyrs-extra-collect',
                                                                              'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                              'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                              'differences': [],
                                                                              'english_served_sha256': '17bba96cc2c8e9446b7eeab26c86f268f294167df530a6c391b4316be083a85e',
                                                                              'english_with_lf_sha256': 'f8a02d6ec9993b0978a39fb1dbb53893f36967744ae0e7cda8e9b74c49535415',
                                                                              'historical_after_listed_transformations_words_sha256': 'f93a02db3ed22fcff8d1e2b392b5760434f6365aeb6986d1c4487b297e4ca925',
                                                                              'historical_latin_transcription_sha256': '2ab0476b0faacd641da99f35c3fb41b3be761fd5fc3a8221061c74d0af5a5671',
                                                                              'historical_word_count': 22,
                                                                              'historical_words_sha256': 'f93a02db3ed22fcff8d1e2b392b5760434f6365aeb6986d1c4487b297e4ca925',
                                                                              'not_a_normalized_recipient_join': True,
                                                                              'not_raw_glyph_or_1962_byte_identity': True,
                                                                              'unlisted_word_or_ending_differences': []},
                                                                  'references': {'roman-1962': [{'form': '',
                                                                                                 'kind': 'common',
                                                                                                 'mass': 'commune-plurimorum-martyrum-3',
                                                                                                 'proper': 'Collect'},
                                                                                                {'form': '',
                                                                                                 'kind': 'common',
                                                                                                 'mass': 'commune-martyrum-tempore-paschali-2',
                                                                                                 'proper': 'Collect '
                                                                                                           '(Item '
                                                                                                           'altera '
                                                                                                           'oratio)'},
                                                                                                {'form': '',
                                                                                                 'kind': 'sanctoral',
                                                                                                 'mass': 'comm-ss-faustini-iovitae-martyrum',
                                                                                                 'proper': 'Collect'}],
                                                                                 'roman-pre-1955': [{'form': '',
                                                                                                     'kind': 'common',
                                                                                                     'mass': 'commune-plurimorum-martyrum-3',
                                                                                                     'proper': 'Collect'},
                                                                                                    {'form': '',
                                                                                                     'kind': 'common',
                                                                                                     'mass': 'commune-martyrum-tempore-paschali-2',
                                                                                                     'proper': 'Collect '
                                                                                                               '(Item '
                                                                                                               'altera '
                                                                                                               'oratio)'},
                                                                                                    {'form': '',
                                                                                                     'kind': 'sanctoral',
                                                                                                     'mass': 'comm-ss-faustini-iovitae-martyrum',
                                                                                                     'proper': 'Collect'}]},
                                                                  'seed_context': ' 1962 III Pro pluribus '
                                                                                  'Martyribus Tertia Missa; '
                                                                                  'Lasance Paschal-Time '
                                                                                  'alternative Prayer supplies '
                                                                                  'the same full Latin without '
                                                                                  "importing that source's "
                                                                                  'rubrics. ',
                                                                  'seed_locus': 'printed p. [12], no. 4261; '
                                                                                'artifact PDF p. 820; right',
                                                                  'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-paschal-plural-martyrs-extra-collect-seed',
                                                                  'seed_pdf_page': 820,
                                                                  'seed_unit': 4261,
                                                                  'source_context': 'Common Martyrs in '
                                                                                    'Paschal-Time, Another '
                                                                                    'Prayer for Martyrs Only',
                                                                  'source_key': 'paschal-plural-martyrs-extra-collect',
                                                                  'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-paschal-plural-martyrs-extra-collect',
                                                                  'source_pdf_pages': [1353],
                                                                  'source_printed_pages': ['1334']},
 ('commune-virginum-4', 'main', 'Collect', 'all', 1): {'canonical_bytes': 146,
                                                       'canonical_sha256': '41f67809f1aa5bcab0a7534f161a38b69eca31944dc4686f75d63df7fe6b1b7b',
                                                       'english': 'Graciously hear us, O God, our Saviour, '
                                                                  'that, as we rejoice in the festival of '
                                                                  'blessed N., Thy virgin, so we may be taught '
                                                                  'by the spirit of pious devotion. Through '
                                                                  'our Lord.',
                                                       'line': 7,
                                                       'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-virgin-not-martyr-collect',
                                                       'receipt': {'actual_historical_ending': 'Per Dominum.',
                                                                   'actual_seed_ending': 'Per Dominum.',
                                                                   'actual_seed_transcription_sha256': '607e441fd09721d9b1f26ccb4cce1b5672c622f9b19987de707bcb216ccfcda9',
                                                                   'actual_seed_word_count': 21,
                                                                   'actual_seed_words_sha256': '0b4655e325ad1bb766bcf5cedb3b9762d07b2b0f6f5c682f9a61ca55731cc470',
                                                                   'candidate_id': 'lasance-next-virgin-not-martyr-collect',
                                                                   'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                   'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                   'differences': [],
                                                                   'english_served_sha256': '5df0e8ce88c2b1cca458a7e33e963aeefaec50b08cab27298145e6090cbc6889',
                                                                   'english_with_lf_sha256': 'b3df70c3f21895c822ae3ad2a7ce7176176431068b9de134e9e4c4337c7120f4',
                                                                   'historical_after_listed_transformations_words_sha256': '0b4655e325ad1bb766bcf5cedb3b9762d07b2b0f6f5c682f9a61ca55731cc470',
                                                                   'historical_latin_transcription_sha256': 'd36548651ebc5bb96d155260bc3a142f01f5c4c69f332d970877932bba9d7790',
                                                                   'historical_word_count': 21,
                                                                   'historical_words_sha256': '0b4655e325ad1bb766bcf5cedb3b9762d07b2b0f6f5c682f9a61ca55731cc470',
                                                                   'not_a_normalized_recipient_join': True,
                                                                   'not_raw_glyph_or_1962_byte_identity': True,
                                                                   'unlisted_word_or_ending_differences': []},
                                                       'references': {'roman-1962': [{'form': '',
                                                                                      'kind': 'common',
                                                                                      'mass': 'commune-virginum-4',
                                                                                      'proper': 'Collect'},
                                                                                     {'form': '',
                                                                                      'kind': 'sanctoral',
                                                                                      'mass': 'comm-s-petronillae-virginis',
                                                                                      'proper': 'Collect'}],
                                                                      'roman-pre-1955': [{'form': '',
                                                                                          'kind': 'common',
                                                                                          'mass': 'commune-virginum-4',
                                                                                          'proper': 'Collect'},
                                                                                         {'form': '',
                                                                                          'kind': 'sanctoral',
                                                                                          'mass': 'comm-s-petronillae-virginis',
                                                                                          'proper': 'Collect'}]},
                                                       'seed_context': 'Complete own actual1962 prayer and '
                                                                       'ending separately inspected for this '
                                                                       'English binding.',
                                                       'seed_locus': 'printed p. [33], no. 4422; artifact PDF '
                                                                     'p. 841; right',
                                                       'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-virgin-not-martyr-collect-seed',
                                                       'seed_pdf_page': 841,
                                                       'seed_unit': 4422,
                                                       'source_context': 'Common of a Virgin not a Martyr, '
                                                                         'Prayer',
                                                       'source_key': 'virgin-not-martyr-collect',
                                                       'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-virgin-not-martyr-collect',
                                                       'source_pdf_pages': [1393],
                                                       'source_printed_pages': ['1374']},
 ('epiphany-3', 'main', 'Postcommunion', 'all', 1): {'canonical_bytes': 120,
                                                     'canonical_sha256': '6c014880165486b3ae670c87c14f3a2e1fc7c6d2d13aa19c70617763c15acc3d',
                                                     'english': 'We beseech Thee, O Lord, that Thou wouldst '
                                                                'vouchsafe to fit us to receive the benefits '
                                                                'of these august mysteries as Thou dost of Thy '
                                                                'bounty grant us to perform them. Through our '
                                                                'Lord.',
                                                     'line': 8,
                                                     'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-supplementary4-postcommunion',
                                                     'receipt': {'actual_historical_ending': 'Per Dominum.',
                                                                 'actual_seed_ending': 'Per Dominum.',
                                                                 'actual_seed_transcription_sha256': '37c560e9b5170fae468e3b28043adffb2a917a7164c667e6740ffacc0419a6f3',
                                                                 'actual_seed_word_count': 16,
                                                                 'actual_seed_words_sha256': '5f08b5c8b7125b7da69239f3dc37b15a00f7a1253e65a38a402939ae57dc48aa',
                                                                 'candidate_id': 'lasance-next-supplementary4-postcommunion',
                                                                 'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                 'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                 'differences': [],
                                                                 'english_served_sha256': '2389481987655b73fd82818953582aca8517298bee30a81c3da821f45c454c8f',
                                                                 'english_with_lf_sha256': 'd1fdde36f4e873219209df6af16d8f940e39068a77960cc9522e838f82cc3428',
                                                                 'historical_after_listed_transformations_words_sha256': '5f08b5c8b7125b7da69239f3dc37b15a00f7a1253e65a38a402939ae57dc48aa',
                                                                 'historical_latin_transcription_sha256': '37c560e9b5170fae468e3b28043adffb2a917a7164c667e6740ffacc0419a6f3',
                                                                 'historical_word_count': 16,
                                                                 'historical_words_sha256': '5f08b5c8b7125b7da69239f3dc37b15a00f7a1253e65a38a402939ae57dc48aa',
                                                                 'not_a_normalized_recipient_join': True,
                                                                 'not_raw_glyph_or_1962_byte_identity': True,
                                                                 'unlisted_word_or_ending_differences': []},
                                                     'references': {'roman-1962': [{'form': '',
                                                                                    'kind': 'seasonal',
                                                                                    'mass': 'epiphany-3',
                                                                                    'proper': 'Postcommunion'},
                                                                                   {'form': '',
                                                                                    'kind': 'seasonal',
                                                                                    'mass': 'resumed-epiphany-3',
                                                                                    'proper': 'Postcommunion'}],
                                                                    'roman-pre-1955': [{'form': '',
                                                                                        'kind': 'seasonal',
                                                                                        'mass': 'epiphany-3',
                                                                                        'proper': 'Postcommunion'},
                                                                                       {'form': '',
                                                                                        'kind': 'seasonal',
                                                                                        'mass': 'resumed-epiphany-3',
                                                                                        'proper': 'Postcommunion'}]},
                                                     'seed_context': 'Complete own actual1962 prayer and '
                                                                     'ending separately inspected for this '
                                                                     'English binding.',
                                                     'seed_locus': 'printed p. 46, no. 315; artifact PDF p. '
                                                                   '127; right',
                                                     'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-supplementary4-postcommunion-seed',
                                                     'seed_pdf_page': 127,
                                                     'seed_unit': 315,
                                                     'source_context': 'Supplementary Mass No. 4, '
                                                                       'Postcommunion',
                                                     'source_key': 'supplementary4-postcommunion',
                                                     'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-supplementary4-postcommunion',
                                                     'source_pdf_pages': [750],
                                                     'source_printed_pages': ['752']},
 ('epiphany-4', 'main', 'Collect', 'all', 1): {'canonical_bytes': 213,
                                               'canonical_sha256': '192aad7dac3fd13e281089d9882798d00ef22d28cbe1fa7879d76d87dda1fab5',
                                               'english': 'O God, Who knowest that we are surrounded by perils '
                                                          'so great as to be unendurable because of our human '
                                                          'frailty, grant us health of mind and body, so that '
                                                          'by Thine assistance we may conquer the things with '
                                                          'which we are afflicted because of our sins. Through '
                                                          'our Lord.',
                                               'line': 9,
                                               'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-supplementary3-collect',
                                               'receipt': {'actual_historical_ending': 'Per Dominum.',
                                                           'actual_seed_ending': 'Per Dominum.',
                                                           'actual_seed_transcription_sha256': 'd11999369c8f8568241fc60f1714f0921d47f5ea739a1ff48586becefa6abfbd',
                                                           'actual_seed_word_count': 32,
                                                           'actual_seed_words_sha256': '55b391c162dc5837616b64a783173a798d68dc2c2d9b795eb6c08c6ee414fec2',
                                                           'candidate_id': 'lasance-next-supplementary3-collect',
                                                           'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                           'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                           'differences': [{'actual_1962_token': 'adiuvante',
                                                                            'actual_1962_word_number_1_based': 29,
                                                                            'classification': 'transformation, '
                                                                                              'not changed '
                                                                                              'word/ending, '
                                                                                              'not OCR '
                                                                                              'correction',
                                                                            'historical_token': 'adjuvante',
                                                                            'historical_word_number_1_based': 29,
                                                                            'kind': 'declared-consonantal-i-j-orthographic-transformation'}],
                                                           'english_served_sha256': '38137c23095a80bb6acc0bbcc33dfada21aa73f326410076f8ea736ff3f3cb74',
                                                           'english_with_lf_sha256': 'f431e02e40de459a0932b0c90b93c5238454eca835c3824922e779aa386feb00',
                                                           'historical_after_listed_transformations_words_sha256': '55b391c162dc5837616b64a783173a798d68dc2c2d9b795eb6c08c6ee414fec2',
                                                           'historical_latin_transcription_sha256': 'f711dbc1c12e607ec2c8c357231d6bfba31acfbe0467e876315131a30375beeb',
                                                           'historical_word_count': 32,
                                                           'historical_words_sha256': '7c4ad6d343731d98589e7944e687d32b90192bc91e7520e15783db0cea32c53a',
                                                           'not_a_normalized_recipient_join': True,
                                                           'not_raw_glyph_or_1962_byte_identity': True,
                                                           'unlisted_word_or_ending_differences': []},
                                               'references': {'roman-1962': [{'form': '',
                                                                              'kind': 'seasonal',
                                                                              'mass': 'epiphany-4',
                                                                              'proper': 'Collect'},
                                                                             {'form': '',
                                                                              'kind': 'seasonal',
                                                                              'mass': 'resumed-epiphany-4',
                                                                              'proper': 'Collect'}],
                                                              'roman-pre-1955': [{'form': '',
                                                                                  'kind': 'seasonal',
                                                                                  'mass': 'epiphany-4',
                                                                                  'proper': 'Collect'},
                                                                                 {'form': '',
                                                                                  'kind': 'seasonal',
                                                                                  'mass': 'resumed-epiphany-4',
                                                                                  'proper': 'Collect'}]},
                                               'seed_context': 'Complete own actual1962 prayer and ending '
                                                               'separately inspected for this English binding.',
                                               'seed_locus': 'printed p. 46, no. 317; artifact PDF p. 127; '
                                                             'right',
                                               'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-supplementary3-collect-seed',
                                               'seed_pdf_page': 127,
                                               'seed_unit': 317,
                                               'source_context': 'Supplementary Mass No. 3, Prayer',
                                               'source_key': 'supplementary3-collect',
                                               'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-supplementary3-collect',
                                               'source_pdf_pages': [745],
                                               'source_printed_pages': ['747']},
 ('epiphany-6', 'main', 'Secret', 'all', 1): {'canonical_bytes': 90,
                                              'canonical_sha256': 'f6e8086cae1c5f2acfe640f301efcc121aba6fb17856a864b91e136807bd812b',
                                              'english': 'May this oblation, O God, cleanse, renew, govern, '
                                                         'and protect us, we beseech Thee. Through our Lord.',
                                              'line': 10,
                                              'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-supplementary1-secret',
                                              'receipt': {'actual_historical_ending': 'Per Dominum.',
                                                          'actual_seed_ending': 'Per Dominum.',
                                                          'actual_seed_transcription_sha256': '8f3b59a55de3767eb7968e2771bc1cbddd985f0993388353a7db0580c6a1522d',
                                                          'actual_seed_word_count': 13,
                                                          'actual_seed_words_sha256': '6345f0297379dc8b6e58ecf85c24bb7bd95ddf305d9b3a526927ecca9fd6239d',
                                                          'candidate_id': 'lasance-next-supplementary1-secret',
                                                          'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                          'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                          'differences': [],
                                                          'english_served_sha256': '7607e21656589872ae35e404536189ae86d64da665ada3f06e7179e353e4c06b',
                                                          'english_with_lf_sha256': '9d1737f6dacea5bf135a27ac99313d7a09dff59a520227f3836ee55285782b95',
                                                          'historical_after_listed_transformations_words_sha256': '6345f0297379dc8b6e58ecf85c24bb7bd95ddf305d9b3a526927ecca9fd6239d',
                                                          'historical_latin_transcription_sha256': 'ccf9f453b0cc7010d1726612104a75033332f32a98cecd384f92b0bf819480c7',
                                                          'historical_word_count': 13,
                                                          'historical_words_sha256': '6345f0297379dc8b6e58ecf85c24bb7bd95ddf305d9b3a526927ecca9fd6239d',
                                                          'not_a_normalized_recipient_join': True,
                                                          'not_raw_glyph_or_1962_byte_identity': True,
                                                          'unlisted_word_or_ending_differences': []},
                                              'references': {'roman-1962': [{'form': '',
                                                                             'kind': 'seasonal',
                                                                             'mass': 'epiphany-6',
                                                                             'proper': 'Secret'},
                                                                            {'form': '',
                                                                             'kind': 'seasonal',
                                                                             'mass': 'resumed-epiphany-6',
                                                                             'proper': 'Secret'}],
                                                             'roman-pre-1955': [{'form': '',
                                                                                 'kind': 'seasonal',
                                                                                 'mass': 'epiphany-6',
                                                                                 'proper': 'Secret'},
                                                                                {'form': '',
                                                                                 'kind': 'seasonal',
                                                                                 'mass': 'resumed-epiphany-6',
                                                                                 'proper': 'Secret'}]},
                                              'seed_context': 'Complete own actual1962 prayer and ending '
                                                              'separately inspected for this English binding.',
                                              'seed_locus': 'printed p. 49, no. 343; artifact PDF p. 130; '
                                                            'right',
                                              'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-supplementary1-secret-seed',
                                              'seed_pdf_page': 130,
                                              'seed_unit': 343,
                                              'source_context': 'Supplementary Mass No. 1, Secret',
                                              'source_key': 'supplementary1-secret',
                                              'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-supplementary1-secret',
                                              'source_pdf_pages': [741],
                                              'source_printed_pages': ['743']},
 ('lent-1-ember-saturday', 'longer', 'Collect', 'all', 1): {'canonical_bytes': 120,
                                                            'canonical_sha256': '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533',
                                                            'english': 'Look favorably upon Thy people, we '
                                                                       'beseech Thee, O Lord, and of Thy mercy '
                                                                       'turn aside from it the scourges of Thy '
                                                                       'wrath. Through our Lord.',
                                                            'line': 11,
                                                            'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-lent1-ember-collect-longer',
                                                            'receipt': {'actual_historical_ending': 'Per '
                                                                                                    'Dominum.',
                                                                        'actual_seed_ending': 'Per Dominum.',
                                                                        'actual_seed_transcription_sha256': '335fb0456212fc3c80f8a47cf01d79f94f964b6a7f919b872ea0730003d73e96',
                                                                        'actual_seed_word_count': 16,
                                                                        'actual_seed_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                        'candidate_id': 'lasance-next-lent1-ember-collect',
                                                                        'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                        'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                        'differences': [],
                                                                        'english_served_sha256': '9686f0790d405485f43ca3260c6d767a0f2f9dec9ce08f0c1c2490bba232104c',
                                                                        'english_with_lf_sha256': '98437c06b8cd85945e64c5b716fe16ad1887a068a3bb96007e9eea098f634177',
                                                                        'historical_after_listed_transformations_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                        'historical_latin_transcription_sha256': '335fb0456212fc3c80f8a47cf01d79f94f964b6a7f919b872ea0730003d73e96',
                                                                        'historical_word_count': 16,
                                                                        'historical_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                        'not_a_normalized_recipient_join': True,
                                                                        'not_raw_glyph_or_1962_byte_identity': True,
                                                                        'unlisted_word_or_ending_differences': []},
                                                            'references': {'roman-1962': [{'form': 'Longer '
                                                                                                   'form '
                                                                                                   '(forma '
                                                                                                   'missae '
                                                                                                   'longior)',
                                                                                           'kind': 'seasonal',
                                                                                           'mass': 'lent-1-ember-saturday',
                                                                                           'proper': 'Collect'}],
                                                                           'roman-pre-1955': [{'form': 'Longer '
                                                                                                       'form '
                                                                                                       '(forma '
                                                                                                       'missae '
                                                                                                       'longior)',
                                                                                               'kind': 'seasonal',
                                                                                               'mass': 'lent-1-ember-saturday',
                                                                                               'proper': 'Collect'}]},
                                                            'seed_context': 'Actual FORMA MISSAE LONGIOR '
                                                                            'heading on this page; not '
                                                                            'inferred from shorter form.  ',
                                                            'seed_locus': 'printed p. 73, no. 494; artifact '
                                                                          'PDF p. 154; right',
                                                            'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-lent1-ember-collect-longer-seed',
                                                            'seed_pdf_page': 154,
                                                            'seed_unit': 494,
                                                            'source_context': 'Ember Saturday in Lent, first '
                                                                              'Prayer after Kyrie and '
                                                                              'Flectamus genua',
                                                            'source_key': 'lent1-ember-collect',
                                                            'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-lent1-ember-collect',
                                                            'source_pdf_pages': [258],
                                                            'source_printed_pages': ['258']},
 ('lent-1-ember-saturday', 'shorter', 'Collect', 'all', 1): {'canonical_bytes': 120,
                                                             'canonical_sha256': '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533',
                                                             'english': 'Look favorably upon Thy people, we '
                                                                        'beseech Thee, O Lord, and of Thy '
                                                                        'mercy turn aside from it the scourges '
                                                                        'of Thy wrath. Through our Lord.',
                                                             'line': 12,
                                                             'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-lent1-ember-collect-shorter',
                                                             'receipt': {'actual_historical_ending': 'Per '
                                                                                                     'Dominum.',
                                                                         'actual_seed_ending': 'Per Dominum.',
                                                                         'actual_seed_transcription_sha256': '335fb0456212fc3c80f8a47cf01d79f94f964b6a7f919b872ea0730003d73e96',
                                                                         'actual_seed_word_count': 16,
                                                                         'actual_seed_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                         'candidate_id': 'lasance-next-lent1-ember-collect',
                                                                         'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                         'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                         'differences': [],
                                                                         'english_served_sha256': '9686f0790d405485f43ca3260c6d767a0f2f9dec9ce08f0c1c2490bba232104c',
                                                                         'english_with_lf_sha256': '98437c06b8cd85945e64c5b716fe16ad1887a068a3bb96007e9eea098f634177',
                                                                         'historical_after_listed_transformations_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                         'historical_latin_transcription_sha256': '335fb0456212fc3c80f8a47cf01d79f94f964b6a7f919b872ea0730003d73e96',
                                                                         'historical_word_count': 16,
                                                                         'historical_words_sha256': '84d6e17ee9bbff655a3eaef9d749fab2aae130c6af0219389c2dc453cf32d0d0',
                                                                         'not_a_normalized_recipient_join': True,
                                                                         'not_raw_glyph_or_1962_byte_identity': True,
                                                                         'unlisted_word_or_ending_differences': []},
                                                             'references': {'roman-1962': [{'form': 'Shorter '
                                                                                                    'form',
                                                                                            'kind': 'seasonal',
                                                                                            'mass': 'lent-1-ember-saturday',
                                                                                            'proper': 'Collect'}],
                                                                            'roman-pre-1955': [{'form': 'Shorter '
                                                                                                        'form',
                                                                                                'kind': 'seasonal',
                                                                                                'mass': 'lent-1-ember-saturday',
                                                                                                'proper': 'Collect'}]},
                                                             'seed_context': 'Actual FORMA MISSAE BREVIOR '
                                                                             'heading on this page; separately '
                                                                             'read.  ',
                                                             'seed_locus': 'printed p. 77, no. 519; artifact '
                                                                           'PDF p. 158; right',
                                                             'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-lent1-ember-collect-shorter-seed',
                                                             'seed_pdf_page': 158,
                                                             'seed_unit': 519,
                                                             'source_context': 'Ember Saturday in Lent, first '
                                                                               'Prayer after Kyrie and '
                                                                               'Flectamus genua',
                                                             'source_key': 'lent1-ember-collect',
                                                             'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-lent1-ember-collect',
                                                             'source_pdf_pages': [258],
                                                             'source_printed_pages': ['258']},
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Secret', 'all', 1): {'canonical_bytes': 172,
                                                                 'canonical_sha256': '4fcb9b4f5f436b5bae4d0bc6d9419f1f8b290b323ff1e0c0758c0607f0cb2104',
                                                                 'english': 'By Thy clemency, O Lord, and the '
                                                                            'intercession of blessed Mary, '
                                                                            'ever a virgin, may this oblation '
                                                                            'profit us unto eternal and also '
                                                                            'present well being and peace. '
                                                                            'Through our Lord.',
                                                                 'line': 13,
                                                                 'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-marian-secret',
                                                                 'receipt': {'actual_historical_ending': 'Per '
                                                                                                         'Dominum.',
                                                                             'actual_seed_ending': 'Per '
                                                                                                   'Dominum.',
                                                                             'actual_seed_transcription_sha256': 'bf8ef01828c48f1b57a6bd6885642baf788600374f457f37a78534808a9c3f5a',
                                                                             'actual_seed_word_count': 22,
                                                                             'actual_seed_words_sha256': '05620a9fbf3166e0555f6200b22daf861936fd573bd62bf031454dc4a6173e84',
                                                                             'candidate_id': 'lasance-next-marian-secret',
                                                                             'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                             'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                             'differences': [],
                                                                             'english_served_sha256': '4247caf5d0d4365b4edb98d3b4802349fd6b1c54bc92a7a22d8e880954436e31',
                                                                             'english_with_lf_sha256': 'ddb3b3c8f08001fb55f31c0a9ccd518791c042b128f440ec3a2e4d9f1c1e5273',
                                                                             'historical_after_listed_transformations_words_sha256': '05620a9fbf3166e0555f6200b22daf861936fd573bd62bf031454dc4a6173e84',
                                                                             'historical_latin_transcription_sha256': 'bf8ef01828c48f1b57a6bd6885642baf788600374f457f37a78534808a9c3f5a',
                                                                             'historical_word_count': 22,
                                                                             'historical_words_sha256': '05620a9fbf3166e0555f6200b22daf861936fd573bd62bf031454dc4a6173e84',
                                                                             'not_a_normalized_recipient_join': True,
                                                                             'not_raw_glyph_or_1962_byte_identity': True,
                                                                             'unlisted_word_or_ending_differences': []},
                                                                 'references': {'roman-1962': [{'form': '',
                                                                                                'kind': 'common',
                                                                                                'mass': 'missa-de-s-maria-in-sabbato-2',
                                                                                                'proper': 'Secret'},
                                                                                               {'form': '',
                                                                                                'kind': 'common',
                                                                                                'mass': 'missa-de-s-maria-in-sabbato-3',
                                                                                                'proper': 'Secret'},
                                                                                               {'form': '',
                                                                                                'kind': 'common',
                                                                                                'mass': 'missa-de-s-maria-in-sabbato-4',
                                                                                                'proper': 'Secret'}],
                                                                                'roman-pre-1955': [{'form': '',
                                                                                                    'kind': 'common',
                                                                                                    'mass': 'missa-de-s-maria-in-sabbato-2',
                                                                                                    'proper': 'Secret'},
                                                                                                   {'form': '',
                                                                                                    'kind': 'common',
                                                                                                    'mass': 'missa-de-s-maria-in-sabbato-3',
                                                                                                    'proper': 'Secret'},
                                                                                                   {'form': '',
                                                                                                    'kind': 'common',
                                                                                                    'mass': 'missa-de-s-maria-in-sabbato-4',
                                                                                                    'proper': 'Secret'}]},
                                                                 'seed_context': '  Actually followed '
                                                                                 'left-column start to '
                                                                                 'right-column top; no '
                                                                                 'truncation at praesentem.',
                                                                 'seed_locus': 'printed p. [45], no. 4507; '
                                                                               'artifact PDF p. 853; left '
                                                                               'start, right top conclusion',
                                                                 'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-marian-secret-seed',
                                                                 'seed_pdf_page': 853,
                                                                 'seed_unit': 4507,
                                                                 'source_context': 'Common of the Blessed '
                                                                                   'Virgin Mary, Secret',
                                                                 'source_key': 'marian-secret',
                                                                 'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-marian-secret',
                                                                 'source_pdf_pages': [1416],
                                                                 'source_printed_pages': ['1397']},
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Postcommunion', 'all', 1): {'canonical_bytes': 186,
                                                                        'canonical_sha256': '6107c5bac2ff048431036d057b4302efb086b93f077602883144bb97b43f2025',
                                                                        'english': 'Having received the aids '
                                                                                   'of our everlasting '
                                                                                   'salvation, O Lord, we '
                                                                                   'beseech Thee, grant us to '
                                                                                   'be everywhere protected by '
                                                                                   'the patronage of blessed '
                                                                                   'Mary, ever a virgin, in '
                                                                                   'veneration of whom we have '
                                                                                   'made these offerings to '
                                                                                   'Thy majesty. Through our '
                                                                                   'Lord',
                                                                        'line': 14,
                                                                        'publication_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase5-en14-marian-postcommunion',
                                                                        'receipt': {'actual_historical_ending': 'Per '
                                                                                                                'Dominum.',
                                                                                    'actual_seed_ending': 'Per '
                                                                                                          'Dominum.',
                                                                                    'actual_seed_transcription_sha256': '0ef2be9ecc110435fb938c2467bbbade21ed8870caab9454d810a7cd9de55103',
                                                                                    'actual_seed_word_count': 24,
                                                                                    'actual_seed_words_sha256': 'cf9fbc3a6aabe5b9a297ae302bc5b6320729322b972a76779777aca110cd76b4',
                                                                                    'candidate_id': 'lasance-next-marian-postcommunion',
                                                                                    'corrected_primary_oracle_sha256': 'ec5a547350d81029cd7eaecb34143089bffb9da9140183dced7dd3fc2015bbce',
                                                                                    'corrected_primary_receipt_sha256': '56ba03ef197935f1b553c17cca2edabef27b895bd3b4bd0ce69ad3c0d588ff25',
                                                                                    'differences': [{'actual_1962_token': 'cuius',
                                                                                                     'actual_1962_word_number_1_based': 17,
                                                                                                     'classification': 'transformation, '
                                                                                                                       'not '
                                                                                                                       'changed '
                                                                                                                       'word/ending, '
                                                                                                                       'not '
                                                                                                                       'OCR '
                                                                                                                       'correction',
                                                                                                     'historical_token': 'cujus',
                                                                                                     'historical_word_number_1_based': 17,
                                                                                                     'kind': 'declared-consonantal-i-j-orthographic-transformation'},
                                                                                                    {'actual_1962_token': 'maiestati',
                                                                                                     'actual_1962_word_number_1_based': 22,
                                                                                                     'classification': 'transformation, '
                                                                                                                       'not '
                                                                                                                       'changed '
                                                                                                                       'word/ending, '
                                                                                                                       'not '
                                                                                                                       'OCR '
                                                                                                                       'correction',
                                                                                                     'historical_token': 'majestati',
                                                                                                     'historical_word_number_1_based': 22,
                                                                                                     'kind': 'declared-consonantal-i-j-orthographic-transformation'}],
                                                                                    'english_served_sha256': 'bc571510821d70eea7b6d660aaf44fe603bbe8d6d8e9caf77d981d37ff562b56',
                                                                                    'english_with_lf_sha256': '6eebbac1a0fc821e142e2b2f817c2f7de47f92379fa869acbfb7a469f7ef2b28',
                                                                                    'historical_after_listed_transformations_words_sha256': 'cf9fbc3a6aabe5b9a297ae302bc5b6320729322b972a76779777aca110cd76b4',
                                                                                    'historical_latin_transcription_sha256': '4a3e7a1b0504373a378984192af4e1b3f39920591b21b942a5408c7e10643548',
                                                                                    'historical_word_count': 24,
                                                                                    'historical_words_sha256': 'fbd40f99028469764e3dab3ac6e3c85b494ba097db7e79bb4db67a4a1d29267a',
                                                                                    'not_a_normalized_recipient_join': True,
                                                                                    'not_raw_glyph_or_1962_byte_identity': True,
                                                                                    'unlisted_word_or_ending_differences': []},
                                                                        'references': {'roman-1962': [{'form': '',
                                                                                                       'kind': 'common',
                                                                                                       'mass': 'missa-de-s-maria-in-sabbato-3',
                                                                                                       'proper': 'Postcommunion'}],
                                                                                       'roman-pre-1955': [{'form': '',
                                                                                                           'kind': 'common',
                                                                                                           'mass': 'missa-de-s-maria-in-sabbato-3',
                                                                                                           'proper': 'Postcommunion'}]},
                                                                        'seed_context': 'Complete own '
                                                                                        'actual1962 prayer and '
                                                                                        'ending separately '
                                                                                        'inspected for this '
                                                                                        'English binding.',
                                                                        'seed_locus': 'printed p. [46], no. '
                                                                                      '4520; artifact PDF p. '
                                                                                      '854; right',
                                                                        'seed_passage_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.phase5-en14-marian-postcommunion-seed',
                                                                        'seed_pdf_page': 854,
                                                                        'seed_unit': 4520,
                                                                        'source_context': 'Common of the '
                                                                                          'Blessed Virgin '
                                                                                          'Mary, Postcommunion',
                                                                        'source_key': 'marian-postcommunion',
                                                                        'source_passage_id': 'passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.verify-phase5-en14-marian-postcommunion',
                                                                        'source_pdf_pages': [1416],
                                                                        'source_printed_pages': ['1397']}}

ARTIFACT = {'byte_size': 3219,
 'id': 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.phase5-twelve-prayers-thirteen-owners-en-cfd58bf4',
 'path': 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase5-twelve-prayers-thirteen-owners-en-cfd58bf4/phase5-twelve-prayers-thirteen-owners-en.tsv',
 'sha256': 'cfd58bf4120c2c506074e0ed17e8e1108ca32dd42806c313dc2b701d1870e979'}

PRIOR206_KEYS = [('advent-1', 'main', 'Collect', 'all', 1),
 ('advent-1', 'main', 'Postcommunion', 'all', 1),
 ('advent-1', 'main', 'Secret', 'all', 1),
 ('advent-2', 'main', 'Postcommunion', 'all', 1),
 ('advent-2', 'main', 'Secret', 'all', 1),
 ('advent-3', 'main', 'Collect', 'all', 1),
 ('advent-3', 'main', 'Postcommunion', 'all', 1),
 ('advent-3', 'main', 'Secret', 'all', 1),
 ('advent-4', 'main', 'Collect', 'all', 1),
 ('advent-4', 'main', 'Postcommunion', 'all', 1),
 ('advent-4', 'main', 'Secret', 'all', 1),
 ('advent-ember-friday', 'main', 'Secret', 'all', 1),
 ('comm-beatae-mariae-virginis-a-mercede', 'main', 'Collect', 'all', 1),
 ('comm-impressionis-sacrorum-stigmatum-s-francisci', 'main', 'Secret', 'all', 1),
 ('comm-s-alexii-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-bonifatii-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Collect', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-canuti-regis-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-gorgonii-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-gorgonii-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-hermetis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-hermetis-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Collect', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-pauli-apostoli', 'main', 'Secret', 'all', 1),
 ('comm-s-petri-apostoli', 'main', 'Collect', 'all', 1),
 ('comm-s-petri-apostoli', 'main', 'Secret', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Collect', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-petri-apostoli-2', 'main', 'Secret', 'all', 1),
 ('comm-s-praxedis-virginis', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-praxedis-virginis', 'main', 'Secret', 'all', 1),
 ('comm-s-romani-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-romani-martyris', 'main', 'Secret', 'all', 1),
 ('comm-s-saturnini-martyris', 'main', 'Postcommunion', 'all', 1),
 ('comm-s-saturnini-martyris', 'main', 'Secret', 'all', 1),
 ('comm-septem-dolorum-beatae-mariae-virginis', 'main', 'Sequence', 'all', 1),
 ('comm-ss-alexandri-eventii-theoduli-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-alexandri-eventii-theoduli-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-cypriani-iustinae-virginis-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-hippolyti-cassiani-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-hippolyti-cassiani-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-placidi-sociorum-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-proti-hyacinthi-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('comm-ss-proti-hyacinthi-martyrum', 'main', 'Secret', 'all', 1),
 ('comm-ss-quatuor-coronatorum-martyrum', 'main', 'Collect', 'all', 1),
 ('comm-ss-symphorosae-septem-eius-filiorum', 'main', 'Secret', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Collect', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Postcommunion', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Secret', 'all', 1),
 ('commemoratione-omnium-fidelium-defunctorum', 'first', 'Sequence', 'all', 1),
 ('commune-abbatum', 'main', 'Postcommunion', 'all', 1),
 ('commune-confessoris-non-pontificis-1', 'main', 'Postcommunion', 'all', 1),
 ('commune-confessoris-non-pontificis-1', 'main', 'Secret', 'all', 1),
 ('commune-confessoris-pontificis-1', 'main', 'Postcommunion', 'all', 1),
 ('commune-confessoris-pontificis-1', 'main', 'Secret', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Collect', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Collect (In ipso die Dedicationis)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Postcommunion (In ipso die Dedicationis)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Secret (Extra ecclesiam ipsam dedicatam)', 'all', 1),
 ('commune-dedicationis-ecclesiae', 'main', 'Secret (In ipso die Dedicationis)', 'all', 1),
 ('commune-doctorum-non-pontificis', 'main', 'Secret', 'all', 1),
 ('commune-doctorum-pontificis', 'main', 'Postcommunion', 'all', 1),
 ('commune-doctorum-pontificis', 'main', 'Secret', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Alleluia', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Gradual', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Postcommunion', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Secret', 'all', 1),
 ('commune-festorum-bmv', 'main', 'Tract', 'all', 1),
 ('commune-martyrum-tempore-paschali-1', 'main', 'Postcommunion (Pro Martyre tantum)', 'all', 1),
 ('commune-plurimorum-martyrum-1', 'main', 'Postcommunion', 'all', 1),
 ('commune-plurimorum-martyrum-2', 'main', 'Secret', 'all', 1),
 ('commune-summorum-pontificum', 'main', 'Collect', 'all', 1),
 ('commune-unius-martyris-2', 'main', 'Postcommunion', 'all', 1),
 ('commune-unius-martyris-2', 'main', 'Secret', 'all', 1),
 ('commune-unius-martyris-3', 'main', 'Secret', 'all', 1),
 ('commune-virginum-2', 'main', 'Collect', 'all', 1),
 ('commune-virginum-2', 'main', 'Postcommunion', 'all', 1),
 ('commune-virginum-2', 'main', 'Secret', 'all', 1),
 ('commune-virginum-3', 'main', 'Postcommunion', 'all', 1),
 ('commune-virginum-3', 'main', 'Secret', 'all', 1),
 ('commune-virginum-4', 'main', 'Alleluia', 'all', 1),
 ('corpus-christi', 'main', 'Sequence', 'all', 1),
 ('easter-5', 'main', 'Postcommunion', 'all', 1),
 ('easter-monday', 'main', 'Secret', 'all', 1),
 ('easter-sunday', 'main', 'Secret', 'all', 1),
 ('easter-sunday', 'main', 'Sequence', 'all', 1),
 ('easter-vigil', 'main', 'Blessing of the Baptismal Water', 'all', 1),
 ('easter-vigil', 'main', 'Blessing of the New Fire', 'all', 1),
 ('easter-vigil', 'main', 'Lumen Christi', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the First Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Fourth Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Second Prophecy', 'all', 1),
 ('easter-vigil', 'main', 'Oration after the Third Prophecy', 'all', 1),
 ('epiphany-5', 'main', 'Secret', 'all', 1),
 ('good-friday', 'main', 'Showing of the Cross', 'all', 1),
 ('holy-family', 'main', 'Collect', 'all', 1),
 ('holy-family', 'main', 'Postcommunion', 'all', 1),
 ('holy-family', 'main', 'Secret', 'all', 1),
 ('holy-monday', 'main', 'Postcommunion', 'all', 1),
 ('lent-1-ember-wednesday', 'main', 'Secret', 'all', 1),
 ('lent-3-friday', 'main', 'Postcommunion', 'all', 1),
 ('lent-4-monday', 'main', 'Postcommunion', 'all', 1),
 ('lent-4-monday', 'main', 'Secret', 'all', 1),
 ('lent-4-saturday', 'main', 'Secret', 'all', 1),
 ('lent-4-tuesday', 'main', 'Postcommunion', 'all', 1),
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Communion', 'all', 1),
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Offertory', 'all', 1),
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Alleluia', 'all', 1),
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Introit', 'all', 1),
 ('missa-de-s-maria-in-sabbato-4', 'main', 'Offertory', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Collect', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Postcommunion', 'all', 1),
 ('most-holy-name-of-jesus', 'main', 'Secret', 'all', 1),
 ('nativitate-beatae-mariae-virginis', 'main', 'Communion', 'all', 1),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 1),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 2),
 ('palm-sunday', 'main', 'Procession Antiphon', 'all', 3),
 ('palm-sunday', 'main', 'Responsory at the Entrance into the Church', 'all', 1),
 ('palm-sunday', 'main', 'Versicle at the Beginning of the Procession', 'all', 1),
 ('pentecost', 'main', 'Alleluia', 'all', 1),
 ('pentecost', 'main', 'Collect', 'all', 1),
 ('pentecost', 'main', 'Communion', 'all', 1),
 ('pentecost', 'main', 'Gospel', 'all', 1),
 ('pentecost', 'main', 'Introit', 'all', 1),
 ('pentecost', 'main', 'Offertory', 'all', 1),
 ('pentecost', 'main', 'Postcommunion', 'all', 1),
 ('pentecost', 'main', 'Secret', 'all', 1),
 ('pentecost', 'main', 'Sequence', 'all', 1),
 ('pentecost-13', 'main', 'Collect', 'all', 1),
 ('pentecost-13', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-13', 'main', 'Secret', 'all', 1),
 ('pentecost-14', 'main', 'Collect', 'all', 1),
 ('pentecost-14', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-14', 'main', 'Secret', 'all', 1),
 ('pentecost-15', 'main', 'Collect', 'all', 1),
 ('pentecost-15', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-15', 'main', 'Secret', 'all', 1),
 ('pentecost-19', 'main', 'Collect', 'all', 1),
 ('pentecost-19', 'main', 'Introit', 'all', 1),
 ('pentecost-19', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-19', 'main', 'Secret', 'all', 1),
 ('pentecost-4', 'main', 'Postcommunion', 'all', 1),
 ('pentecost-4', 'main', 'Secret', 'all', 1),
 ('pentecost-ember-saturday', 'longer', 'Postcommunion', 'all', 1),
 ('pentecost-ember-saturday', 'longer', 'Secret', 'all', 1),
 ('pentecost-ember-saturday', 'shorter', 'Postcommunion', 'all', 1),
 ('pentecost-ember-saturday', 'shorter', 'Secret', 'all', 1),
 ('pentecost-thursday', 'main', 'Secret', 'all', 1),
 ('praesentatione-beatae-mariae-virginis', 'main', 'Postcommunion', 'all', 1),
 ('praesentatione-beatae-mariae-virginis', 'main', 'Secret', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-alberti-magni-episcopi-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-angelae-mericiae-virginis', 'main', 'Collect', 'all', 1),
 ('s-antonini-episcopi-confessoris', 'main', 'Secret', 'all', 1),
 ('s-augustini-episcopi-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-bedae-venerabilis-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-bernardini-senensis-confessoris', 'main', 'Secret', 'all', 1),
 ('s-bibianae-virginis-martyris', 'main', 'Collect', 'all', 1),
 ('s-birgittae-viduae', 'main', 'Secret', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-cyrilli-episcopi-alexandrini-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-damasi-i-papae-confessoris', 'main', 'Collect', 'all', 1),
 ('s-ephraem-syri-diaconi-confessoris-ecclesiae', 'main', 'Collect', 'all', 1),
 ('s-francisci-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-francisci-confessoris', 'main', 'Secret', 'all', 1),
 ('s-gregorii-i-papae-confessoris-ecclesiae', 'main', 'Postcommunion', 'all', 1),
 ('s-gregorii-i-papae-confessoris-ecclesiae', 'main', 'Secret', 'all', 1),
 ('s-gregorii-thaumaturgi-episcopi-confessoris', 'main', 'Secret', 'all', 1),
 ('s-gregorii-vii-papae-confessoris', 'main', 'Collect', 'all', 1),
 ('s-hermenegildi-martyris', 'main', 'Postcommunion', 'all', 1),
 ('s-hermenegildi-martyris', 'main', 'Secret', 'all', 1),
 ('s-ioannis-a-deo-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-ioannis-baptistae-la-salle-confessoris', 'main', 'Secret', 'all', 1),
 ('s-ioannis-eudes-confessoris', 'main', 'Collect', 'all', 1),
 ('s-ioannis-matha-confessoris', 'main', 'Collect', 'all', 1),
 ('s-iosephi-cupertino-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-iosephi-cupertino-confessoris', 'main', 'Secret', 'all', 1),
 ('s-luciae-virginis-martyris', 'main', 'Postcommunion', 'all', 1),
 ('s-luciae-virginis-martyris', 'main', 'Secret', 'all', 1),
 ('s-marthae-virginis', 'main', 'Secret', 'all', 1),
 ('s-monicae-viduae', 'main', 'Postcommunion', 'all', 1),
 ('s-monicae-viduae', 'main', 'Secret', 'all', 1),
 ('s-pauli-primi-eremitae-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-pauli-primi-eremitae-confessoris', 'main', 'Secret', 'all', 1),
 ('s-petri-canisii-confessoris-ecclesiae-doctoris', 'main', 'Collect', 'all', 1),
 ('s-petri-nolasci-confessoris', 'main', 'Postcommunion', 'all', 1),
 ('s-petri-nolasci-confessoris', 'main', 'Secret', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Collect', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Postcommunion', 'all', 1),
 ('s-silvestri-abbatis', 'main', 'Secret', 'all', 1),
 ('sanctissimi-nominis-beatae-mariae-virginis', 'main', 'Postcommunion', 'all', 1),
 ('sanctissimi-nominis-beatae-mariae-virginis', 'main', 'Secret', 'all', 1),
 ('septem-dolorum-beatae-mariae-virginis', 'main', 'Sequence', 'all', 1),
 ('september-ember-saturday', 'longer', 'Collect', 'all', 1),
 ('september-ember-saturday', 'shorter', 'Collect', 'all', 1),
 ('sexagesima', 'main', 'Secret', 'all', 1),
 ('ss-perpetuae-felicitatis-martyrum', 'main', 'Postcommunion', 'all', 1),
 ('ss-philippi-iacobi-apostolorum', 'main', 'Postcommunion', 'all', 1),
 ('ss-quadraginta-martyrum', 'main', 'Collect', 'all', 1),
 ('ss-septem-fratrum-martyrum-ac-ss', 'main', 'Collect', 'all', 1),
 ('ss-vincentii-anastasii-martyrum', 'main', 'Secret', 'all', 1),
 ('vigil-of-the-ascension', 'main', 'Postcommunion', 'all', 1)]

PRIOR206_SHA = 'f340855f55b4e6416c6836d97aa31311b69e10185e74fd1d290a92940b0ab551'

OLD_SOURCE_FILES_SHA = '5552d21ae9143d119df9cd395e5cde740850ac1b7a1c315e976697682d4b1c31'

OWNED_SOURCE_PATHS = ['src/sources/inventories/roman-1962-proper-translations-v1.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-lent1-ember-collect-longer-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-lent1-ember-collect-shorter-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-lourdes-collect-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-lourdes-secret-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-marian-postcommunion-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-marian-secret-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-oct7-martyrs-postcommunion-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-oct7-martyrs-secret-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-paschal-plural-martyrs-extra-collect-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-supplementary1-secret-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-supplementary3-collect-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-supplementary4-postcommunion-seed.toml',
 'src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-virgin-not-martyr-collect-seed.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase5-twelve-prayers-thirteen-owners-en-cfd58bf4/artifact.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase5-twelve-prayers-thirteen-owners-en-cfd58bf4/phase5-twelve-prayers-thirteen-owners-en.tsv',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-lent1-ember-collect-longer.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-lent1-ember-collect-shorter.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-lourdes-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-lourdes-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-marian-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-marian-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-oct7-martyrs-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-oct7-martyrs-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-paschal-plural-martyrs-extra-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-supplementary1-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-supplementary3-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-supplementary4-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-virgin-not-martyr-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-lent1-ember-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-lourdes-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-lourdes-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-marian-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-marian-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-oct7-martyrs-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-oct7-martyrs-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-paschal-plural-martyrs-extra-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-supplementary1-secret.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-supplementary3-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-supplementary4-postcommunion.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-virgin-not-martyr-collect.toml']

COVERAGE = {'roman-1962': (1427, 219, 1208), 'roman-pre-1955': (1378, 206, 1172)}

BASELINE14_SHA = {('apparitione-beatae-mariae-virginis-immaculatae', 'main', 'Collect', 'all', 1): '6ee41d8065bf62d6bdb9cb9ecbc1847b2fd44904f6e3372d08b627df7e7eec7e',
 ('apparitione-beatae-mariae-virginis-immaculatae', 'main', 'Secret', 'all', 1): '962082fc0df7d2e5655ce79f737d221d1c2fd7b72f03d99e10959686041b02d5',
 ('beatae-mariae-virginis-a-rosario', 'main', 'Collect', 'all', 1): 'e1181b3b428cc4d74b431ba38cbbbe9c0d59ca11cce04cf579fbd67ab0a0de52',
 ('comm-ss-sergii-bacchi-marcelli-apuleii', 'main', 'Postcommunion', 'all', 1): 'e21b7428f2efd8030cbe61e0d12e4fde5c58d42185e8721c6f046dfd127c73ed',
 ('comm-ss-sergii-bacchi-marcelli-apuleii', 'main', 'Secret', 'all', 1): '3b312da3ef6bbaabae27f02bf13d00143847fe89ce45bb1917cd3f5b160e479a',
 ('commune-plurimorum-martyrum-3', 'main', 'Collect', 'all', 1): '59b0bdb4319ca305233c629223f74e5504399f9d5a9895b4e5e664b0f6e19e7c',
 ('commune-virginum-4', 'main', 'Collect', 'all', 1): '41f67809f1aa5bcab0a7534f161a38b69eca31944dc4686f75d63df7fe6b1b7b',
 ('epiphany-3', 'main', 'Postcommunion', 'all', 1): '6c014880165486b3ae670c87c14f3a2e1fc7c6d2d13aa19c70617763c15acc3d',
 ('epiphany-4', 'main', 'Collect', 'all', 1): '192aad7dac3fd13e281089d9882798d00ef22d28cbe1fa7879d76d87dda1fab5',
 ('epiphany-6', 'main', 'Secret', 'all', 1): 'f6e8086cae1c5f2acfe640f301efcc121aba6fb17856a864b91e136807bd812b',
 ('lent-1-ember-saturday', 'longer', 'Collect', 'all', 1): '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533',
 ('lent-1-ember-saturday', 'shorter', 'Collect', 'all', 1): '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533',
 ('missa-de-s-maria-in-sabbato-2', 'main', 'Secret', 'all', 1): '4fcb9b4f5f436b5bae4d0bc6d9419f1f8b290b323ff1e0c0758c0607f0cb2104',
 ('missa-de-s-maria-in-sabbato-3', 'main', 'Postcommunion', 'all', 1): '6107c5bac2ff048431036d057b4302efb086b93f077602883144bb97b43f2025'}

ROSARY_ABSENCE_SHA = '68c9593fdeceb23c3717ef25c19c6d85e26efe3ed874de8d9a12375b1f1ff9be'

RETIRED_PATHS = ['src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/phase5-en14-rosary-collect-seed.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase5-thirteen-prayers-fourteen-owners-en-73fe3a88/artifact.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/phase5-thirteen-prayers-fourteen-owners-en-73fe3a88/phase5-thirteen-prayers-fourteen-owners-en.tsv',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/publish-phase5-en14-rosary-collect.toml',
 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/passages/verify-phase5-en14-rosary-collect.toml',
 'tools/tests/test_roman_1962_english14_phase5.py']

class English13SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("english13_test_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        cls.p = module_from_spec(spec); sys.modules[spec.name] = cls.p; loader.exec_module(cls.p)
        cls.doc = cls.p.load_calendar(CAL, "roman-1962")
        cls.records, problems = cls.p._source_library_records(CAL)
        if problems:
            raise AssertionError(problems)
        cls.overlay, cls.absent, cls.stale, cls.witnesses = cls.p.translation_overlay("roman-1962", CAL)
        cls.entries = {cls.p.translation_record_identity(r, cls.doc): r
                       for r in tomllib.loads(LEDGER.read_text())["entries"]}
        cls.bodies = {}
        for _, mass in cls.p.masses_of(cls.doc):
            for form, proper, taken in cls.p.appointed_propers(cls.doc, mass):
                owner = cls.p.source_slot_identity(cls.doc, mass, form, proper, taken)
                for key, body in cls.p.coverage_slot_units(proper, owner):
                    cls.bodies[key] = body

    def test_exact_thirteen_owners_twelve_historical_prayers_eleven_pages(self):
        selected = {k for k, r in self.entries.items() if r.get("publication_artifact_id") == ARTIFACT["id"]}
        self.assertEqual(selected, set(ORACLES))
        self.assertEqual(len(selected), 13)
        self.assertEqual(len({o["source_passage_id"] for o in ORACLES.values()}), 12)
        self.assertEqual(len({o["seed_passage_id"] for o in ORACLES.values()}), 13)
        self.assertEqual(len({p for o in ORACLES.values() for p in o["source_pdf_pages"]}), 11)
        self.assertEqual(len(source_batch.historical_english_entries(self.entries)), 219)

    def test_fresh_english_hashes_placeholders_same_ending_and_no_added_period(self):
        for key, o in ORACLES.items():
            actual = self.entries[key]["translations"][0]["text"]
            self.assertEqual(actual, o["english"])
            self.assertEqual(sha(actual), o["receipt"]["english_served_sha256"])
            self.assertEqual(sha(actual + "\n"), o["receipt"]["english_with_lf_sha256"])
            self.assertFalse(actual.endswith("\n"))
            if o["source_key"] == "lourdes-collect":
                self.assertTrue(actual.endswith("Through the same."))
            elif o["source_key"] == "marian-postcommunion":
                self.assertTrue(actual.endswith("Through our Lord"))
                self.assertFalse(actual.endswith("."))
            else:
                self.assertTrue(actual.endswith("Through our Lord."))
        self.assertIn("N. and N.", ORACLES[("commune-plurimorum-martyrum-3", "main", "Collect", "all", 1)]["english"])
        self.assertIn("blessed N.", ORACLES[("commune-virginum-4", "main", "Collect", "all", 1)]["english"])

    def test_whole_historical_to_own_seed_words_and_actual_endings(self):
        strict, qualified = 0, 0
        for key, o in ORACLES.items():
            receipt = o["receipt"]
            record = self.records[o["source_passage_id"]]
            self.assertEqual(json.loads(record["notes"].split("collation_receipt: ", 1)[1]), receipt)
            self.assertEqual(record["artifact_page_ranges"], [[o["source_pdf_pages"][0], o["source_pdf_pages"][-1]]])
            self.assertIn("printed p. " + ",".join(o["source_printed_pages"]), record["context"])
            historical = words(self.bodies[key]["text"])
            self.assertEqual(wordsha(historical), receipt["historical_words_sha256"])
            projected = listed_word_projection(historical, receipt["differences"])
            self.assertEqual(wordsha(projected), receipt["actual_seed_words_sha256"])
            self.assertEqual(wordsha(projected), receipt["historical_after_listed_transformations_words_sha256"])
            self.assertEqual(len(projected), receipt["actual_seed_word_count"])
            self.assertEqual(receipt["actual_historical_ending"], receipt["actual_seed_ending"])
            self.assertEqual(receipt["unlisted_word_or_ending_differences"], [])
            self.assertTrue(receipt["not_raw_glyph_or_1962_byte_identity"])
            self.assertTrue(receipt["not_a_normalized_recipient_join"])
            if receipt["differences"]:
                qualified += 1
            else:
                strict += 1
        self.assertEqual((strict, qualified), (9, 4))

    def test_only_four_declared_i_j_cases_and_five_positioned_differences(self):
        artifact = self.records[ARTIFACT["id"]]
        declared = json.loads(artifact["notes"].split("differences: ", 1)[1])
        expected = {o["source_key"]: o["receipt"]["differences"] for o in ORACLES.values() if o["receipt"]["differences"]}
        self.assertEqual(declared, expected)
        self.assertEqual(len(declared), 4)
        self.assertEqual(sum(map(len, declared.values())), 5)
        for key, o in ORACLES.items():
            self.assertEqual(json.loads(self.records[o["seed_passage_id"]]["notes"].split("differences: ", 1)[1]), o["receipt"]["differences"])
            self.assertEqual(json.loads(self.records[o["publication_passage_id"]]["notes"].split("differences: ", 1)[1]), o["receipt"]["differences"])
            if not o["receipt"]["differences"]:
                continue
            historical = words(self.bodies[key]["text"])
            actual = listed_word_projection(historical, o["receipt"]["differences"])
            self.assertNotEqual(historical, actual)
            self.assertIn("i/j", artifact["transformation"])
            self.assertIn("not OCR", artifact["transformation"])
            for damaged in (historical + ["nostrum"], ["aliud"] + historical[1:], historical[:-1]):
                try:
                    projected = listed_word_projection(damaged, o["receipt"]["differences"])
                except (ValueError, IndexError):
                    continue
                self.assertNotEqual(projected, actual)
        # Broad orthographic normalization is intentionally NOT authorized.
        self.assertNotEqual(words("coelestibus"), words("caelestibus"))
        self.assertNotEqual(words("beatum"), words("sanctum"))
        self.assertNotEqual(words("Per Dominum."), words("Per Dominum nostrum."))

    def test_frozen_pre_parallel_canonical_entire_utf8_not_all_roman_yaml(self):
        self.assertEqual(len(BASELINE14_SHA), 14)
        for key, expected in BASELINE14_SHA.items():
            self.assertEqual(sha(self.bodies[key]["text"]), expected)
        for key, o in ORACLES.items():
            body = self.bodies[key]["text"]
            self.assertEqual((sha(body), len(body.encode())), (o["canonical_sha256"], o["canonical_bytes"]))
            self.assertTrue(body.endswith("\n"))
            seed = self.records[o["seed_passage_id"]]
            self.assertEqual(seed["locus"], o["seed_locus"])
            self.assertIn(o["canonical_sha256"], seed["notes"])
            self.assertIn(o["canonical_sha256"], self.entries[key]["witness_note"])

    def test_recipient_whitespace_word_ending_pointing_wrap_and_hash_mismatches(self):
        for key, o in ORACLES.items():
            body = self.bodies[key]["text"]
            variants = [body.rstrip("\n"), " " + body, body + "\n", body.replace("\n", " "),
                        body.replace(" ", "  ", 1), body.replace(".", "", 1), "aliud " + body,
                        re.sub(r"Per\s+(?:eundem\s+)?Dominum\.\s*$", "Per Dominum nostrum.\n", body)]
            for altered in variants:
                self.assertNotEqual(altered, body)
                self.assertNotEqual(sha(altered), o["canonical_sha256"])
            self.assertNotEqual(o["canonical_sha256"], "0" * 64)
        # Even a legal word-collation transformation is NOT a literal recipient join.
        self.assertEqual(listed_word_projection(["adjuvante"], [{
            "historical_word_number_1_based": 1, "actual_1962_word_number_1_based": 1,
            "historical_token": "adjuvante", "actual_1962_token": "adiuvante"}]), ["adiuvante"])
        self.assertNotEqual(sha("adjuvante\n"), sha("adiuvante\n"))

    def test_distinct_lent_controls_marian_column_and_october_page_continuations(self):
        longer = ORACLES[("lent-1-ember-saturday", "longer", "Collect", "all", 1)]
        shorter = ORACLES[("lent-1-ember-saturday", "shorter", "Collect", "all", 1)]
        self.assertEqual((longer["seed_pdf_page"], longer["seed_unit"]), (154, 494))
        self.assertEqual((shorter["seed_pdf_page"], shorter["seed_unit"]), (158, 519))
        self.assertNotEqual(longer["seed_passage_id"], shorter["seed_passage_id"])
        self.assertEqual(longer["source_passage_id"], shorter["source_passage_id"])
        marian = ORACLES[("missa-de-s-maria-in-sabbato-2", "main", "Secret", "all", 1)]
        self.assertIn("right top conclusion", marian["seed_locus"])
        october = ORACLES[("comm-ss-sergii-bacchi-marcelli-apuleii", "main", "Secret", "all", 1)]
        self.assertEqual(october["source_pdf_pages"], [1223, 1224])
        self.assertEqual(ORACLES[("comm-ss-sergii-bacchi-marcelli-apuleii", "main", "Postcommunion", "all", 1)]["seed_unit"], 3817)
        self.assertEqual(ORACLES[("epiphany-4", "main", "Collect", "all", 1)]["source_key"], "supplementary3-collect")

    def test_twenty_one_actual_references_each_effective_calendar(self):
        for calendar in COVERAGE:
            document = self.p.load_calendar(CAL, calendar)
            refs = {k: [] for k in ORACLES}
            for kind, mass in self.p.masses_of(document):
                for form, proper, taken in self.p.appointed_propers(document, mass):
                    owner = self.p.source_slot_identity(document, mass, form, proper, taken)
                    for key, body in self.p.coverage_slot_units(proper, owner):
                        if key in refs:
                            self.assertEqual(sha(body["text"]), ORACLES[key]["canonical_sha256"])
                            refs[key].append({"kind": kind, "mass": mass["key"], "form": form, "proper": proper["name"]})
            self.assertEqual(sum(map(len, refs.values())), 21)
            for key, references in refs.items():
                self.assertEqual(sorted(references, key=digest), sorted(ORACLES[key]["references"][calendar], key=digest))

    def test_payload_source_graph_exact_rows_and_binding_negative_controls(self):
        raw = (ROOT / ARTIFACT["path"]).read_bytes()
        self.assertEqual((sha(raw), len(raw)), (ARTIFACT["sha256"], ARTIFACT["byte_size"]))
        rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
        self.assertEqual(len(rows), 13)
        for line, row in enumerate(rows, 2):
            key = (row["mass"], row["form_id"], row["proper"], row["cycle"], int(row["occurrence"]))
            o = ORACLES[key]; entry = self.entries[key]
            self.assertEqual(json.loads(row["english_json"]), o["english"])
            pub = self.records[entry["publication_passage_id"]]
            self.assertEqual(pub["physical_line_ranges"], [[line, line]])
            self.assertEqual(pub["locus"], self.records[entry["passage_id"]]["locus"])
            self.p.validate_translation_publication_binding(entry, CAL, LEDGER, self.witnesses)
            for field, value in (("mass", "wrong-owner"), ("form_id", "wrong-form"), ("cycle", "A"),
                                 ("occurrence", 2), ("publication_artifact_sha256", "0" * 64)):
                changed = copy.deepcopy(entry); changed[field] = value
                with self.assertRaises(ValueError):
                    self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)
            for altered in (o["english"] + " Amen.", " " + o["english"], o["english"].replace("God", "Lord", 1) + " "):
                changed = copy.deepcopy(entry); changed["translations"][0]["text"] = altered
                with self.assertRaises(ValueError):
                    self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)

    def test_all206_prior_entry_dictionaries_and773_old_english_source_files(self):
        self.assertEqual(len(PRIOR206_KEYS), 206)
        self.assertEqual(digest([self.entries[k] for k in sorted(PRIOR206_KEYS)]), PRIOR206_SHA)
        actual = source_batch.historical_english_source_files()
        self.assertEqual(len(actual), 773)
        self.assertEqual(digest(sorted(actual.items())), OLD_SOURCE_FILES_SHA)

    def test_bounded_us_english_rights_not_whole_mixed_scan_or_latin(self):
        artifact = self.records[ARTIFACT["id"]]
        self.assertEqual((artifact["rights_status"], artifact["rights_jurisdiction"]), ("public-domain", "United States"))
        for phrase in ("A110108", "A192159", "1298a-1298n", "1302a-1302d"):
            self.assertIn(phrase, artifact["rights_basis"])
        self.assertIn("No whole mixed-scan", artifact["rights_basis"])
        self.assertIn("No Latin permission", artifact["notes"])
        self.assertEqual(artifact["derived_from"], self.records[next(iter(ORACLES.values()))["source_passage_id"]]["artifact_id"])

    def test_current_coverage_and_original_held_scope(self):
        historical_entries = source_batch.historical_english_entries(self.entries)
        for calendar, expected in COVERAGE.items():
            historical = source_batch.historical_english_coverage(calendar)
            self.assertEqual((historical["slots"], historical["with_english"], historical["ledgered_untranslated"]), expected)
            row = self.p.english_coverage(CAL, calendar)
            source_batch.assert_current_english_coverage(row, calendar)
            for field in ("unaccounted", "outside_the_ledger", "unmatched_records", "stale_translation_records", "rights_restricted"):
                self.assertEqual(row[field], 0, (calendar, field))
        self.assertEqual(source_batch.historical_english_coverage("roman-pre-1955")["inherited_inapplicable_records"], 49)
        for mass in ("s-ioannis-a-cruce-confessoris-ecclesiae", "s-ioannis-mariae-vianney-confessoris", "advent-2"):
            key = (mass, "main", "Collect", "all", 1)
            self.assertNotIn(key, historical_entries)
            if key in self.entries:
                self.assertEqual(self.overlay[key], self.entries[key])
            else:
                self.assertNotIn(key, self.overlay)
        self.assertFalse(any("john-cross" in o["source_key"] or "vianney" in o["source_key"] for o in ORACLES.values()))


    def test_primary_rosary_changed_word_withdrawn_and_virgin_source_period(self):
        key = ("beatae-mariae-virginis-a-rosario", "main", "Collect", "all", 1)
        historical = tomllib.loads(source_batch.historical_text(LEDGER.relative_to(ROOT).as_posix()))
        self.assertFalse(any(self.p.translation_record_identity(r, self.doc) == key
                             for r in historical["entries"]))
        absence = [r for r in historical["untranslated"]
                   if self.p.translation_record_identity(r, self.doc) == key]
        self.assertEqual(len(absence), 1)
        self.assertEqual(digest(absence[0]), ROSARY_ABSENCE_SHA)
        # The rejected Lasance word substitution stays rejected. The later
        # original study English has its own accepted source and review.
        source_batch.assert_current_english_entries(self.entries)
        current = self.entries[key]
        self.assertEqual(self.overlay[key], current)
        self.assertEqual(current["source_latin_sha256"], BASELINE14_SHA[key])
        self.assertEqual(current["translation_review"],
                         "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/translation-review.json")
        self.assertEqual(current["translations"][0]["rights"], "project-created")
        self.assertEqual(sha(current["translations"][0]["text"]),
                         "198f1387d8cea84eccdf910df0c0f8b87560d6c94dd12508afb3d91272327b11")
        context = self.p.study_translation_source_context("roman-1962", CAL)
        self.p.validate_study_translation_binding(current, "roman-1962", CAL, LEDGER, context=context)
        changed_source = copy.deepcopy(current)
        changed_source["source_latin_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.p.validate_study_translation_binding(changed_source, "roman-1962", CAL, LEDGER, context=context)
        for path in RETIRED_PATHS:
            self.assertFalse((ROOT / path).exists(), path)
        for record in self.records.values():
            if record.get("record_type") == "passage":
                self.assertFalse(record.get("id", "").endswith((
                    ".verify-phase5-en14-rosary-collect", ".publish-phase5-en14-rosary-collect",
                    ".phase5-en14-rosary-collect-seed")))
        artifact = self.records[ARTIFACT["id"]]
        self.assertIn("sanctissimo", artifact["notes"])
        self.assertIn("sacratissimo", artifact["notes"])
        declared = json.loads(artifact["notes"].split("differences: ", 1)[1])
        self.assertNotIn("rosary-collect", declared)
        # Synthetic positioned regression: no protected complete control transcript.
        historical = ["verbum"] * 36; target = historical.copy()
        historical[1] = "cujus"; target[1] = "cuius"
        historical[19] = "sanctissimo"; target[19] = "sacratissimo"
        ij = {"historical_word_number_1_based": 2, "actual_1962_word_number_1_based": 2,
              "historical_token": "cujus", "actual_1962_token": "cuius"}
        self.assertNotEqual(listed_word_projection(historical, [ij]), target)
        with self.assertRaises(ValueError):
            listed_word_projection(historical, [{
                "historical_word_number_1_based": 20, "actual_1962_word_number_1_based": 20,
                "historical_token": "sanctissimo", "actual_1962_token": "sacratissimo"}])
        virgin = self.entries[("commune-virginum-4", "main", "Collect", "all", 1)]
        english = virgin["translations"][0]["text"]
        self.assertIn("pious devotion. Through our Lord.", english)
        self.assertNotIn("pious devotion: Through", english)
        self.assertEqual(sha(english + "\n"), "b3df70c3f21895c822ae3ad2a7ce7176176431068b9de134e9e4c4337c7120f4")
        changed = copy.deepcopy(virgin)
        changed["translations"][0]["text"] = english.replace("devotion. Through", "devotion: Through")
        with self.assertRaises(ValueError):
            self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)

if __name__ == "__main__":
    unittest.main()
