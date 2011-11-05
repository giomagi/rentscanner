import locale
import urllib2
import xml.etree.ElementTree as xml
from main.houses.model import Property, Price, Address

class RssBasedExtractor:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')

    def properties(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self.agentURI())).read()
        tree = xml.fromstring(xmlString)

        return [prop for prop in [self.propertyFrom(item) for item in tree.findall('channel/item')] if prop is not None]

    def charThatILikeFor(self, ch):
        try:
            return ch.decode('ascii', 'replace')
        except:
            return '?'

    def propertyFrom(self, item):
        try:
            return Property(self.agent(),
                            Price(self.priceAmount(item), self.pricePeriod(item)),
                            Address(self.fullAddress(item), self.postcode(item)),
                            self.link(item),
                            self.propertyId(item),
                            self.publicationTime(item),
                            self.description(item),
                            self.imageLink(item))
        except Exception, e:
            print 'Failed extraction: %s' % e

    def agentURI(self):
        raise NotImplementedError("Must be specified by the subclass")

    def agent(self):
        raise NotImplementedError("Must be specified by the subclass")

    def priceAmount(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def pricePeriod(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def fullAddress(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def postcode(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def link(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def propertyId(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def publicationTime(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def description(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def imageLink(self, item):
        raise NotImplementedError("Must be specified by the subclass")