import unittest

from houses.model import Address, Price

class TestModel(unittest.TestCase):
    def testPricesAreAlwaysDecodedAsMonthly(self):
        self.assertEqual(300 * 52 / 12, Price(300, "week").monthlyPrice())
        self.assertEqual(300, Price(300, "month").monthlyPrice())

    def testFailsOnInvalidPostcodes(self):
        self.assertRaises(Exception, Address._validate, "KE1")
