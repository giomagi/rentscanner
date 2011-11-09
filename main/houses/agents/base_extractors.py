import locale
import urllib2
import xml.etree.ElementTree as xml
from main.houses.model import Property, Price, Address

class RssBasedExtractor:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')

    # TODO: this shouldn't be a superclass for the agents (the way the uris and the properties are handled is inconsistent)
    def properties(self, uris):
        allprops = []
        for uri in uris:
            xmlString = urllib2.build_opener().open(urllib2.Request(uri)).read()
            tree = xml.fromstring(xmlString)

            for item in tree.findall('channel/item'):
                try:
                    allprops.append(self.propertyFrom(item))
                except Exception, e:
                    print 'Failed extraction: %s' % e

        return allprops

    def propertyFrom(self, item):
        raise NotImplementedError("Must be specified by the subclass")
