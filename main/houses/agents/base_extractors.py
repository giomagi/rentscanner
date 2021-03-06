import cookielib
import locale
import os
import urllib2
import xml.etree.ElementTree as xml

class PropertyExtractor(object):
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'en_GB.utf8' if os.name == 'posix' else 'eng_gbr')
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())))
        self.urlopen = urllib2.urlopen

    def properties(self, uris):
        allprops = []
        errors = []

        for uri in uris:
            content = self.urlopen(urllib2.Request(uri)).read()

            for singleItemRepresentation in self.breakDownIntoItems(content):
                try:
                    allprops.append(self.propertyFrom(singleItemRepresentation))
                except Exception, e:
                    errors.append(str(singleItemRepresentation))

        return allprops, errors

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
