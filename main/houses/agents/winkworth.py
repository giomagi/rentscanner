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
        tree = xml.fromstring(xmlString.decode('utf-8'))

        return [self._buildProperty(item) for item in tree.findall('channel/item')]

    def _buildProperty(self, item):
        try:
            titleMatches = self._titlePattern.findall(item.find('title').text)[0]
            descMatches = self._descPattern.findall(item.find('description').text)[0]

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
