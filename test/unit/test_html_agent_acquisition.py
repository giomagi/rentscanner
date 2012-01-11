import unittest
from main.houses.agents.douglas_and_gordon import DouglasAndGordon
from main.houses.agents.faron_sutaria import FaronSutaria
from main.houses.agents.marsh_and_parsons import MarshAndParsons
from main.houses.agents.webdadi import LawsonRutter, Chard, Dexters

class TestAgentAcquisition(unittest.TestCase):
    def testDecodesALawsonRutterItem(self):
        properties = LawsonRutter().properties(['File:sample_lawson_rutter.html'])

        self.assertEqual(2, len(properties))

        property = properties[0]
        self.assertEqual('Delorme Street, London', property.address.address)
        self.assertEqual('W6', property.address.postcode)
        self.assertEqual(1235, property.price.monthlyPrice())
        self.assertEqual('LawsonRutter', property.agent)
        self.assertEqual('http://lettings.lawsonrutter.com/Delorme-Street/homes/beds-2/details.dtx?propertyid=0E8B7552-5381-401A-B202-C7101B8F2E75' , property.link)
        self.assertEqual('0E8B7552-5381-401A-B202-C7101B8F2E75', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('Boasting of a large open plan kitchen/reception room is this well presented first floor two double bedroom Victorian conversion.' , property.description)
        self.assertEqual('http://lettings.lawsonrutter.com/public/webresize.dll?filename={76C83E9E-9636-4B62-8EFF-73133ED1DA06}.jpg&amp;height=150&amp;width=200' , property.image)

    def testDecodesAChardItem(self):
        properties = Chard().properties(['File:sample_chard.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual('Harbour Reach, Imperial Wharf', property.address.address)
        self.assertEqual('SW6', property.address.postcode)
        self.assertEqual(600 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('Chard', property.agent)
        self.assertEqual('http://www.chard.co.uk/Flattolet/Harbour Reach, Imperial Wharf/SW6/beds-2/property.vtx?propertyid=D3132A04-7BA4-4869-AA7F-1F5E17EB80FC' , property.link)
        self.assertEqual('D3132A04-7BA4-4869-AA7F-1F5E17EB80FC', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('This two bedroom apartment to let is arranged on the fifth floor (with lift access) of this modern purpose built riverside.' , property.description)
        self.assertEqual('http://www.chard.co.uk/public/webresize.dll?filename={689159A5-D8DF-4EE2-8DC0-ACC05732996A}.jpg&amp;height=150&amp;width=200' , property.image)

    def testDecodesADextersItem(self):
        properties = Dexters().properties(['File:sample_dexters.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual('Myrna Close, Colliers Wood, London', property.address.address)
        self.assertEqual('SW19', property.address.postcode)
        self.assertEqual(1200, property.price.monthlyPrice())
        self.assertEqual('Dexters', property.agent)
        self.assertEqual('http://lettings.dexters.co.uk/details.dtx?propertyid=8DF3E2D7-A75F-4CB0-A9A0-069D8B688773', property.link)
        self.assertEqual('8DF3E2D7-A75F-4CB0-A9A0-069D8B688773', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('A beautiful two double bedroom end of terrace house within a private cul-de-sac which is less than 1/2 a mile to Colliers.' , property.description)
        self.assertEqual('http://lettings.dexters.co.uk/public/webresize.dll?filename={80CDBCB8-CC43-48A3-AA17-3DBD6C227770}.jpg&amp;height=150&amp;width=200' , property.image)

    def testDecodesADouglasAndGordonItem(self):
        properties = DouglasAndGordon().properties(['File:sample_douglas_and_gordon.html'])

        self.assertEqual(20, len(properties))

        property = properties[0]
        self.assertEqual('Ringford Road', property.address.address)
        self.assertEqual('SW18', property.address.postcode)
        self.assertEqual(300 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('DouglasAndGordon', property.agent)
        self.assertEqual('http://www.douglasandgordon.com/property/overview/?a=letting&b=2&min=300&max=550&id=31038', property.link)
        self.assertEqual('31038', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('A delightful split level flat situated on this quiet residential street less than ten minutes walk from East Putney underground.' , property.description)
        self.assertEqual('http://images.douglasandgordon.com/property/31038/photos/219/146/photo_31038_4.jpg', property.image)

    def testDecodesAMarshAndParsonsItem(self):
        properties = MarshAndParsons().properties(['File:sample_marsh_and_parsons.html'])

        self.assertEqual(15, len(properties))

        property = properties[0]
        self.assertEqual('Devonport, 23 Southwick Street', property.address.address)
        self.assertEqual('W2', property.address.postcode)
        self.assertEqual(550 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('MarshAndParsons', property.agent)
        self.assertEqual('http://www.marshandparsons.co.uk/property-to-rent-in-london/devonport-23-southwick-street-w2/property-details/22453/' , property.link)
        self.assertEqual('22453', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('A large two bedroom flat in a secure block.', property.description)
        self.assertEqual('http://www.marshandparsons.co.uk/dxModules/dxPictures/dxThumbsRent/ecimage1/P022453.jpg', property.image)

    def testDecodesAFaronSutariaItem(self):
        properties = FaronSutaria().properties(['File:sample_faron_sutaria.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual('Elsham Road, West Kensington', property.address.address)
        self.assertEqual('W14', property.address.postcode)
        self.assertEqual(195 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('FaronSutaria', property.agent)
        self.assertEqual('http://www.faronsutaria.co.uk/W14/West-Kensington/Elsham-Road/1-bed/property.vtx?p=C2FA2BB2-BBA1-4DB2-BF4C-78809C3C08C8' , property.link)
        self.assertEqual('C2FA2BB2-BBA1-4DB2-BF4C-78809C3C08C8', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('resources/sorry_no_image.jpeg', property.image)
