import locale
import urllib2
import xml.etree.ElementTree as xml
from main.houses.model import Property, Price, Address

class PropertyExtractor:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')

    def properties(self, uris):
        allprops = []
        for uri in uris:
            content = urllib2.build_opener().open(urllib2.Request(uri)).read()

            for singleItemRepresentation in self.breakDownIntoItems(content):
                try:
                    allprops.append(self.propertyFrom(singleItemRepresentation))
                except Exception, e:
                    print 'Failed extraction: %s' % e
                    print '\tfor ' + str(singleItemRepresentation)

        return allprops

    def agentURIs(self):
        raise NotImplementedError("Must be specified by the subclass")

    def propertyFrom(self, item):
        raise NotImplementedError("Must be specified by the subclass")

    def breakDownIntoItems(self, resourceContent):
        raise NotImplementedError("Must be specified by the subclass")

class RssBasedExtractor(PropertyExtractor):
    def __init__(self):
        PropertyExtractor.__init__(self)

    def breakDownIntoItems(self, resourceContent):
        return xml.fromstring(resourceContent).findall('channel/item')

class HtmlBasedExtractor(PropertyExtractor):
    def __init__(self):
        PropertyExtractor.__init__(self)

    def breakDownIntoItems(self, resourceContent):
        # do something with beautiful soup
        pass
