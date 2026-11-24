import unittest
from opening_review import review
class ReviewTest(unittest.TestCase):
    def test_review(self):
        r={"date":"2026-11-24","eligible":True,"original_ref":"original","actual_ref":"official","actual":110,"previous_close":100,"models":{"V0":{"center":100},"V2":{"center":112}}}
        x=review([r])
        self.assertEqual(x["paired_metrics"]["5"]["models"]["V2"]["mae"],2)
        self.assertEqual(x["paired_metrics"]["5"]["n"],1)
        self.assertEqual(review([{**r,"eligible":False}])["rows"],[])
        with self.assertRaises(ValueError):
            review([r,r])
