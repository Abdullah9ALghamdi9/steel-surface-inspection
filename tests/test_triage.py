import unittest
from triage import assess_inspection_priority

class TriageTests(unittest.TestCase):
    def test_unknown_requires_review(self):
        r = assess_inspection_priority('unknown', 'unknown', 'unknown')
        self.assertEqual(r['priority'], 'review')
        self.assertEqual(r['actual_severity'], 'غير محددة')

    def test_deep_is_high_priority(self):
        self.assertEqual(assess_inspection_priority('deep', 'localized', 'no')['priority'], 'high')

    def test_routine_requires_all_three(self):
        self.assertEqual(assess_inspection_priority('surface', 'localized', 'no')['priority'], 'routine')
        self.assertEqual(assess_inspection_priority('surface', 'localized', 'unknown')['priority'], 'review')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            assess_inspection_priority('fake', 'localized', 'no')

if __name__ == '__main__':
    unittest.main()
