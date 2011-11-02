import locale
from datetime import datetime
import re
from string import rindex
import urllib2
import xml.etree.ElementTree as xml
import sys

from main.houses.model import Property, Address, Price

class Winkworth:
    def __init__(self):
        locale.setlocale( locale.LC_ALL, '' )

        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+GBP\s+(\S+)\s+(\S+)')
        self._descPattern = re.compile(r'<img\s+.*\s+src="(.*)"/>.*\[REF:(\w+)\]')

    def _feedURI(self):
        return 'http://www.winkworth.co.uk/rss/searchproperty?choose_type_letting=1&locality=London&radius=&ptype=&beds=2&price_min=&price=&under_offer=1'
    
    def properties(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self._feedURI())).read()
        tree = xml.fromstring(xmlString)

        return [self._buildProperty(item) for item in tree.findall('channel/item')]

    def _buildProperty(self, item):
        try:
            titleMatches = self._titlePattern.findall(item.find('title').text)[0]
            text = item.find('description').text
            print unicode(text)
            descMatches = self._descPattern.findall(text)[0]

            link = item.find('link').text
            return Property('Winkworth',
                            Price(locale.atoi(titleMatches[2]), titleMatches[3]),
                            Address(titleMatches[0], titleMatches[1]),
                            link,
                            descMatches[1],
                            datetime.strptime(item.findall('pubDate')[0].text, '%a, %d %b %Y %H:%M:%S +0000'),
                            'WINKWORTH DEL CAZZO',
                            descMatches[0])
        except Exception, e:
            print 'Failed extraction: %s' % e


#        self.assertEqual("Norfolk Road, St John's Wood", property.address.address)
#        self.assertEqual("NW8", property.address.postcode)
#        self.assertEqual(8000 * 52 / 12, property.price.monthlyPrice())
#        self.assertEqual("Winkworth", property.agent)
#        self.assertEqual("http://www.winkworth.co.uk/rent/property/WNKSJW063995", property.link)
#        self.assertEqual("WNKSJW063995", property.agentId)
#        self.assertEqual(datetime(2011, 11, 2, 22, 28, 54), property.publicationDateTime)
#        self.assertEqual("6 Bedroom House\n\nA well maintained low built detached house, located on the favoured East side of St John's Wood and within close proximity of all the local shopping and transport amenities of St John's Wood.", property.description)
#        self.assertEqual("http://media2.winkworth.com/properties/f2a40c61-78f9-44f2-9078-e1ee0dd91f68/Listing/8v495J47X6.jpg", property.image)
#rrr = re.compile(r'<img/s+.*/s+src="([^"]*)"')
#ttt = '<a href="http://www.winkworth.co.uk/estate-agents/st-johns-wood?utm_source=RSS&amp;utm_medium=RSS&amp;utm_campaign=WNKSJW063995">St Johns Wood - 020 7586 7001</a><br/><table><tr><td valign="top"><a href="#"><img width="200" border="0" src="http://media2.winkworth.com/properties/f2a40c61-78f9-44f2-9078-e1ee0dd91f68/Listing/8v495J47X6.jpg"/></a></td><td valign="top" ><p><b>6 Bedroom House</b></p><p>&#65;&#32;&#119;&#101;&#108;&#108;&#32;&#109;&#97;&#105;&#110;&#116;&#97;&#105;&#110;&#101;&#100;&#32;&#108;&#111;&#119;&#32;&#98;&#117;&#105;&#108;&#116;&#32;&#100;&#101;&#116;&#97;&#99;&#104;&#101;&#100;&#32;&#104;&#111;&#117;&#115;&#101;&#44;&#32;&#108;&#111;&#99;&#97;&#116;&#101;&#100;&#32;&#111;&#110;&#32;&#116;&#104;&#101;&#32;&#102;&#97;&#118;&#111;&#117;&#114;&#101;&#100;&#32;&#69;&#97;&#115;&#116;&#32;&#115;&#105;&#100;&#101;&#32;&#111;&#102;&#32;&#83;&#116;&#32;&#74;&#111;&#104;&#110;&#39;&#115;&#32;&#87;&#111;&#111;&#100;&#32;&#97;&#110;&#100;&#32;&#119;&#105;&#116;&#104;&#105;&#110;&#32;&#99;&#108;&#111;&#115;&#101;&#32;&#112;&#114;&#111;&#120;&#105;&#109;&#105;&#116;&#121;&#32;&#111;&#102;&#32;&#97;&#108;&#108;&#32;&#116;&#104;&#101;&#32;&#108;&#111;&#99;&#97;&#108;&#32;&#115;&#104;&#111;&#112;&#112;&#105;&#110;&#103;&#32;&#97;&#110;&#100;&#32;&#116;&#114;&#97;&#110;&#115;&#112;&#111;&#114;&#116;&#32;&#97;&#109;&#101;&#110;&#105;&#116;&#105;&#101;&#115;&#32;&#111;&#102;&#32;&#83;&#116;&#32;&#74;&#111;&#104;&#110;&#39;&#115;&#32;&#87;&#111;&#111;&#100;&#46;<br/><br/>[REF:WNKSJW063995]</p></td></tr></table>'
#
#print rrr.findall(ttt)