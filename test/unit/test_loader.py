import unittest
import datetime
from main.houses.loader import Loader
from main.houses.model import Property, Price, Address
from test.support.test_utils import PropertyMaker

class TestLoader(PropertyMaker):
    def testInterestingValidationReturnsTrueForAGoodProperty(self):
        self.assertEqual(Loader().isInteresting(self.aProperty(price=1800, postcode='SW6')), True)

    def testInterestingValidationReturnsFalseForAPropertyWithALowPrice(self):
        self.assertEqual(Loader().isInteresting(self.aProperty(price=1300, postcode='SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyWithAHighPrice(self):
        self.assertEqual(Loader().isInteresting(self.aProperty(price=2200, postcode='SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyInANonInterestingArea(self):
        self.assertEqual(Loader().isInteresting(self.aProperty(price=1800, postcode='SE6')), False)

    def testFiltersOutBadProperties(self):
        good = self.aProperty(price=1800, postcode='SW6')
        bad = self.aProperty(price=1800, postcode='SE6')

        filtered = Loader().filter([good, bad])

        self.assertTrue(good in filtered)
        self.assertFalse(bad in filtered)
