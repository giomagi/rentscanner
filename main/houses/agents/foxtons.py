from datetime import datetime
import re
from main.houses.agents.base_extractors import RssBasedExtractor

class Foxtons(RssBasedExtractor):
    def __init__(self):
        self._titlePattern = re.compile(r'.(\d+)\s+per\s+(week|month)\s+(.*),\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)\. Contact Foxtons')

    def _feedURI(self):
        return 'http://www.foxtons.co.uk/feeds/foxtons_feed.rss?bedrooms_from=2&bedrooms_to=2&result_view=rss&search_type=LL&submit_type=search'
    
    def agent(self):
        return 'Foxtons'

    def priceAmount(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][0]

    def pricePeriod(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][2]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][3]

    def link(self, item):
        return item.findall('link')[0].text

    def propertyId(self, item):
        return self._idPattern.findall(item.find('guid').text)[0]

    def publicationTime(self, item):
        return datetime.strptime(item.findall('pubDate')[0].text, '%a, %d %b %Y %H:%M:%S -0000')

    def description(self, item):
        return self._descPattern.findall(item.find('description').text)[0][1] + '.'

    def imageLink(self, item):
        return self._descPattern.findall(item.find('description').text)[0][0]
