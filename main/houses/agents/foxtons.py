from datetime import datetime
import re
import urllib2
import xml.etree.ElementTree as xml
import sys

from main.houses.model import Property, Address, Price

class Foxtons:
    def __init__(self):
        self._titlePattern = re.compile(r'.(\d+)\s+per\s+(week|month)\s+(.*),\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)\. Contact Foxtons')

    def _feedURI(self):
        return 'http://www.foxtons.co.uk/feeds/foxtons_feed.rss?bedrooms_from=2&bedrooms_to=2&result_view=rss&search_type=LL&submit_type=search'
    
    def properties(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self._feedURI())).read()
        tree = xml.fromstring(unicode(xmlString, errors='replace'))

        return [self._buildProperty(item) for item in tree.findall('channel/item')]

    def _buildProperty(self, item):
        try:
            titleMatches = self._titlePattern.findall(item.find('title').text)[0]
            idMatch = self._idPattern.findall(item.find('guid').text)[0]
            descMatches = self._descPattern.findall(item.find('description').text)[0]

            return Property('Foxtons',
                            Price(titleMatches[0], titleMatches[1]),
                            Address(titleMatches[2], titleMatches[3]),
                            item.findall('link')[0].text,
                            idMatch,
                            datetime.strptime(item.findall('pubDate')[0].text, '%a, %d %b %Y %H:%M:%S -0000'),
                            descMatches[1] + '.',
                            descMatches[0])
        except Exception, e:
            print 'Failed extraction: %s' % e
