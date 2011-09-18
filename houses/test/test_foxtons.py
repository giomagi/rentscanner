import unittest
import xml.etree.ElementTree as xml

from houses.foxtons import Foxtons

class TestFoxtons(unittest.TestCase):
    def testDecodesAFoxtonsItem(self):
        sample = open("sample_foxtons.xml", "r")
        property = Foxtons()._buildProperty(xml.fromstring(sample.read()).find("channel/item"))

        self.assertEqual(property.address.address, "Lexham Gardens, Kensington")
        self.assertEqual(property.address.postcode, "W8")
        self.assertEqual(property.monthlyPrice, 450 * 52 / 12)

