import unittest
from main.houses.agents.webdadi import LawsonRutter, Chard, Dexters
from libs.BeautifulSoup import BeautifulSoup

class TestAgentAcquisition(unittest.TestCase):
    def testDecodesALawsonRutterItem(self):
        properties = LawsonRutter().properties(['File:sample_lawson_rutter.html'])

        self.assertEqual(2, len(properties))

        property = properties[0]
        self.assertEqual("Delorme Street, London", property.address.address)
        self.assertEqual("W6", property.address.postcode)
        self.assertEqual(1235, property.price.monthlyPrice())
        self.assertEqual("LawsonRutter", property.agent)
        self.assertEqual("http://lettings.lawsonrutter.com/Delorme-Street/homes/beds-2/details.dtx?propertyid=0E8B7552-5381-401A-B202-C7101B8F2E75", property.link)
        self.assertEqual("0E8B7552-5381-401A-B202-C7101B8F2E75", property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual("Boasting of a large open plan kitchen/reception room is this well presented first floor two double bedroom Victorian conversion.", property.description)
        self.assertEqual("http://lettings.lawsonrutter.com/public/webresize.dll?filename={76C83E9E-9636-4B62-8EFF-73133ED1DA06}.jpg&amp;height=150&amp;width=200", property.image)

    def testDecodesAChardItem(self):
        properties = Chard().properties(['File:sample_chard.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual("Harbour Reach, Imperial Wharf", property.address.address)
        self.assertEqual("SW6", property.address.postcode)
        self.assertEqual(600 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual("Chard", property.agent)
        self.assertEqual("http://www.chard.co.uk/Flattolet/Harbour Reach, Imperial Wharf/SW6/beds-2/property.vtx?propertyid=D3132A04-7BA4-4869-AA7F-1F5E17EB80FC", property.link)
        self.assertEqual("D3132A04-7BA4-4869-AA7F-1F5E17EB80FC", property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual("This two bedroom apartment to let is arranged on the fifth floor (with lift access) of this modern purpose built riverside.", property.description)
        self.assertEqual("http://www.chard.co.uk/public/webresize.dll?filename={689159A5-D8DF-4EE2-8DC0-ACC05732996A}.jpg&amp;height=150&amp;width=200", property.image)

    def testDecodesADextersItem(self):
        properties = Dexters().properties(['File:sample_dexters.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual("Myrna Close, Colliers Wood, London", property.address.address)
        self.assertEqual("SW19", property.address.postcode)
        self.assertEqual(1200, property.price.monthlyPrice())
        self.assertEqual("Dexters", property.agent)
        self.assertEqual("http://lettings.dexters.co.uk/details.dtx?propertyid=8DF3E2D7-A75F-4CB0-A9A0-069D8B688773", property.link)
        self.assertEqual("8DF3E2D7-A75F-4CB0-A9A0-069D8B688773", property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual("A beautiful two double bedroom end of terrace house within a private cul-de-sac which is less than 1/2 a mile to Colliers.", property.description)
        self.assertEqual("http://lettings.dexters.co.uk/public/webresize.dll?filename={80CDBCB8-CC43-48A3-AA17-3DBD6C227770}.jpg&amp;height=150&amp;width=200", property.image)

