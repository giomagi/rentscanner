from datetime import datetime
import unittest
from main.houses.agents.foxtons import Foxtons
from main.houses.agents.kfh import KFH
from main.houses.agents.knight_frank import KnightFrank
from main.houses.agents.winkworth import Winkworth

class TestAgentAcquisition(unittest.TestCase):
    def testDecodesAFoxtonsItem(self):
        properties = Foxtons().properties(['File:sample_foxtons.xml'])

        self.assertEqual(2, len(properties))

        property = properties[0]
        self.assertEqual("Lexham Gardens, Kensington", property.address.address)
        self.assertEqual("W8", property.address.postcode)
        self.assertEqual(1450 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual("Foxtons", property.agent)
        self.assertEqual("http://www.foxtons.co.uk/rental-property-in-kensington/chpk0260124", property.link)
        self.assertEqual("chpk0260124", property.agentId)
        self.assertEqual(datetime(2011, 9, 16, 14, 17, 51), property.publicationDateTime)
        self.assertEqual("This stunning third floor one bedroomed flat offers a spacious interior with a high standard of decor throughout, modern fittings and fixtures, bright rooms and a superb location for shops, services and transport links.", property.description)
        self.assertEqual("http://r.yhd.net/1316192650/chpk0260124_small-1.jpg", property.image)

    def testDecodesAWinkworthItem(self):
        properties = Winkworth().properties(['File:sample_winkworth.xml'])

        self.assertEqual(2, len(properties))

        property = properties[0]
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

    def testDecodesAKnightFrankItem(self):
        properties = KnightFrank().properties(['File:sample_knight_frank.xml'])

        self.assertEqual(2, len(properties))

        property = properties[0]
        self.assertEqual("Albemarle, Wimbledon Park Side, Wimbledon", property.address.address)
        self.assertEqual("SW19", property.address.postcode)
        self.assertEqual(2200, property.price.monthlyPrice())
        self.assertEqual("KnightFrank", property.agent)
        self.assertEqual("http://search.knightfrank.com/asp147225", property.link)
        self.assertEqual("asp147225", property.agentId)
        self.assertEqual(datetime(2011, 5, 25, 11, 02, 00), property.publicationDateTime)
        self.assertEqual("Situated within this portered block adjacent to Wimbledon Common, this three bedroom 3rd floor flat, available to rent, offers spacious and light accomodation including three bedrooms, two reception rooms, fitted kitchen with breakfast area, two bathrooms, communal garden and parking space for one car. The closest tube station is Southfields station but Wimbledon Station is easy to get to either by foot or using the frequent no 93 bus which takes you directly to the station. Available to let unfurnished. ", property.description)
        self.assertEqual("http://resources.knightfrank.com/GetRes.ashx?ref=ASP147225&type=20&order=1", property.image)

    def testDecodesAKFHItem(self):
        properties = KFH().properties(['File:sample_kfh.xml'])

        self.assertEqual(2, len(properties))

        property = properties[0]
        self.assertEqual("Fellows Road, Swiss Cottage", property.address.address)
        self.assertEqual("NW3", property.address.postcode)
        self.assertEqual(2145, property.price.monthlyPrice())
        self.assertEqual("KFH", property.agent)
        self.assertEqual("http://www.kfh.co.uk/residential/flats-to-rent/london-fulham-sw6-ranelagh-garden-mansions/34538/", property.link)
        self.assertEqual("34538", property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual("A well presented mansion block flat to rent located in an excellent location next to Putney Bridge underground station and the river.", property.description)
        self.assertEqual("resources/sorry_no_image.jpeg", property.image)
