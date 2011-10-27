import unittest
import datetime
from main.houses.loader import Loader
from main.houses.model import Property, Price, Address

class TestLoader(unittest.TestCase):
    def testInterestingValidationReturnsTrueForAGoodProperty(self):
        self.assertEqual(Loader().isInteresting(self.property(1800, 'SW6')), True)

    def testInterestingValidationReturnsFalseForAPropertyWithALowPrice(self):
        self.assertEqual(Loader().isInteresting(self.property(1300, 'SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyWithAHighPrice(self):
        self.assertEqual(Loader().isInteresting(self.property(2200, 'SW6')), False)

    def testInterestingValidationReturnsFalseForAPropertyInANonInterestingArea(self):
        self.assertEqual(Loader().isInteresting(self.property(1800, 'SE6')), False)

    def testFiltersOutBadProperties(self):
        good = self.property(1800, 'SW6')
        bad = self.property(1800, 'SE6')

        filtered = Loader().filter([good, bad])

        self.assertTrue(good in filtered)
        self.assertFalse(bad in filtered)
        
    def property(self, monthlyPrice, postcode):
        return Property("AGENT", Price(monthlyPrice, 'month'), Address('address', postcode), 'link', '123', datetime.datetime.now(), 'description')
