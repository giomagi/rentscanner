import locale
import urllib2
from libs.BeautifulSoup import BeautifulSoup

# TODO: i don't like the inconsistent way the uris and the properties are handled
class RssBasedExtractor:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')

    def properties(self, uris):
        allprops = []
        for uri in uris:
            content = urllib2.build_opener().open(urllib2.Request(uri)).read()
            soup = BeautifulSoup(content)

            for item in soup.findAll('item'):
                try:
                    allprops.append(self.propertyFrom(item))
                except Exception, e:
                    print 'Failed extraction: %s' % e

        return allprops

    def propertyFrom(self, item):
        raise NotImplementedError("Must be specified by the subclass")
