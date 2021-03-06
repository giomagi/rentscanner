import unittest
from main.houses.agents.douglas_and_gordon import DouglasAndGordon
from main.houses.agents.faron_sutaria import FaronSutaria
from main.houses.agents.marsh_and_parsons import MarshAndParsons
from main.houses.agents.sandersons import Sandersons
from main.houses.agents.shaws import Shaws
from main.houses.agents.webdadi import LawsonRutter, Chard, Dexters

class TestAgentAcquisition(unittest.TestCase):
    def testDecodesALawsonRutterItem(self):
        properties, errors = LawsonRutter().properties(['File:sample_lawson_rutter.html'])

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
        properties, errors = Chard().properties(['File:sample_chard.html'])

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
        properties, errors = Dexters().properties(['File:sample_dexters.html'])

        self.assertEqual(6, len(properties))

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
        properties, errors = DouglasAndGordon().properties(['File:sample_douglas_and_gordon.html'])

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
        properties, errors = MarshAndParsons().properties(['File:sample_marsh_and_parsons.html'])

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
        properties, errors = FaronSutaria().properties(['File:sample_faron_sutaria.html'])

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

    def testDecodesAShawsItem(self):
        properties, errors = Shaws().properties(['File:sample_shaws.html'])

        self.assertEqual(6, len(properties))

        property = properties[0]
        self.assertEqual('Tasso Road, London', property.address.address)
        self.assertEqual('W6', property.address.postcode)
        self.assertEqual(530 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('Shaws', property.agent)
        self.assertEqual('http://www.shawsestateagents.com/property/22826157' , property.link)
        self.assertEqual('22826157', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('http://www.shawsestateagents.com/resize/22826157/0/286?show_badge=1', property.image)

    def testDecodesASandersonsItem(self):
        properties, errors = Sandersons().properties(['File:sample_sandersons.html'])

        self.assertEqual(5, len(properties))

        property = properties[0]
        self.assertEqual('Leamington Road Villas, Notting Hill', property.address.address)
        self.assertEqual('W11', property.address.postcode)
        self.assertEqual(550 * 52 / 12, property.price.monthlyPrice())
        self.assertEqual('Sandersons', property.agent)
        self.assertEqual('http://www.sandersonslondon.co.uk/property/2432715?instruction_type=Letting&address_keyword=&minpricew=350&maxpricew=550&bedrooms=2&image_x=52&image_y=12&part_postcode%5B0%5D=W10%2CW11%2CW2%2CW8%2CSW1X%2CSW3%2CW14%2CSW5%2CSW6%2CW1%2CW9&orderby=price+desc' , property.link)
        self.assertEqual('2432715', property.agentId)
        self.assertEqual(None, property.publicationDateTime)
        self.assertEqual('A Superb 2 bedroom top floor split level apartment set within this delightful period conversion just off Westbourne Park Road. The property comprises a large reception room, separate...', property.description)
        self.assertEqual('http://www.sandersonslondon.co.uk/resize/2432715/0/296?show_badge=1', property.image)
