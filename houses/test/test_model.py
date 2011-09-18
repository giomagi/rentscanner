import unittest

from houses.model import Address, Property

class TestModel(unittest.TestCase):
    def testPricesAreAlwaysDecodedAsMonthly(self):
        self.assertEqual(Property((300, "week"), "some place").monthlyPrice, 300 * 52 / 12)
        self.assertEqual(Property((300, "month"), "some place").monthlyPrice, 300)

    def testFailsOnInvalidPostcodes(self):
        self.assertRaises(Exception, Address._validate, "KE1")
