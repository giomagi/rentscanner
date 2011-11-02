from datetime import datetime
import unittest
import xml.etree.ElementTree as xml
from main.houses.agents.foxtons import Foxtons
from main.houses.agents.winkworth import Winkworth

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
        self.assertEqual("This stunning third floor one bedroomed flat offers a spacious interior with a high standard of decor throughout, modern fittings and fixtures, bright rooms and a superb location for shops, services and transport links.", property.description)
        self.assertEqual("http://r.yhd.net/1316192650/chpk0260124_small-1.jpg", property.image)

class TestWinkworth(unittest.TestCase):
    def testDecodesAWinkworthItem(self):
        sample = open("sample_winkworth.xml", "r")
        property = Winkworth()._buildProperty(xml.fromstring(sample.read()).find("channel/item"))

        self.assertEqual("Norfolk Road, St John's Wood", property.address.address)
        self.assertEqual("NW8", property.address.postcode)
        self.assertEqual(8000 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual("Winkworth", property.agent)
        self.assertEqual("http://www.winkworth.co.uk/rent/property/WNKSJW063995", property.link)
        self.assertEqual("WNKSJW063995", property.agentId)
        self.assertEqual(datetime(2011, 11, 2, 22, 28, 54), property.publicationDateTime)
#        self.assertTrue("6 Bedroom House" in property.description)
#        self.assertTrue("A well maintained low built detached house, located on the favoured East side of St John's Wood and within close proximity of all the local shopping and transport amenities of St John's Wood." in property.description)
        self.assertEqual("http://media2.winkworth.com/properties/f2a40c61-78f9-44f2-9078-e1ee0dd91f68/Listing/8v495J47X6.jpg", property.image)
