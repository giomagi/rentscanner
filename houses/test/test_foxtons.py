from datetime import datetime
import unittest
import xml.etree.ElementTree as xml

from houses.foxtons import Foxtons

class TestFoxtons(unittest.TestCase):
    def testDecodesAFoxtonsItem(self):
        sample = open("sample_foxtons.xml", "r")
        property = Foxtons()._buildProperty(xml.fromstring(sample.read()).find("channel/item"))

        self.assertEqual("Lexham Gardens, Kensington", property.address.address)
        self.assertEqual("W8", property.address.postcode)
        self.assertEqual(450 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual("Foxtons", property.agent)
        self.assertEqual("http://www.foxtons.co.uk/rental-property-in-kensington/chpk0260124", property.link)
        self.assertEqual("chpk0260124", property.agentId)
        self.assertEqual(datetime(2011, 9, 16, 14, 17, 51), property.publicationDateTime)
