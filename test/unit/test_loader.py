import unittest
from main.domain.configuration import Configuration
from main.houses.loader import Loader
from test.support.test_utils import PropertyMaker

class TestLoader(unittest.TestCase, PropertyMaker):

    def setUp(self):
        super(TestLoader, self).setUp()
        self.loader = Loader(Configuration.test())

    def testInterestingValidationReturnsTrueForAGoodProperty(self):
        self.assertEqual(self.loader.isInteresting(self.aProperty(price=1800, postcode='SW6')), True)

    def testInterestingValidationReturnsFalseForAPropertyWithALowPrice(self):
        self.assertEqual(self.loader.isInteresting(self.aProperty(price=1300, postcode='SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyWithAHighPrice(self):
        self.assertEqual(self.loader.isInteresting(self.aProperty(price=2200, postcode='SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyInANonInterestingArea(self):
        self.assertEqual(self.loader.isInteresting(self.aProperty(price=1800, postcode='SE6')), False)

    def testFiltersOutBadProperties(self):
        good = self.aProperty(price=1800, postcode='SW6')
        bad = self.aProperty(price=1800, postcode='SE6')

        filtered = self.loader.filter([good, bad])

        self.assertTrue(good in filtered)
        self.assertFalse(bad in filtered)
