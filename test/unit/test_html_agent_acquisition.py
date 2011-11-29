import unittest
from main.houses.agents.webdadi import LawsonRutter
from libs.BeautifulSoup import BeautifulSoup

class TestAgentAcquisition(unittest.TestCase):
    # TODO: move to integration and check the URIs against a real page
    def testDecodesNextPageLinkForLawsonRutter(self):
        pass

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
