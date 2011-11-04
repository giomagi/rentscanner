import locale
from datetime import datetime
import re
from main.houses.agents.base_extractors import RssBasedExtractor

class Winkworth(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+GBP\s+(\S+)\s+(\S+)')
        self._descPattern = re.compile(r'<img\s+.*\s+src="(.*)"/>.*\[REF:(\w+)\]')

    def _feedURI(self):
        return 'http://www.winkworth.co.uk/rss/searchproperty?choose_type_letting=1&locality=London&radius=&ptype=&beds=2&price_min=&price=&under_offer=1'

    def agent(self):
        return 'Winkworth'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][2])

    def pricePeriod(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][3]

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][0]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def link(self, item):
        return item.find('link').text

    def propertyId(self, item):
        return self._descPattern.findall(item.find('description').text)[0][1]

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S')

    def description(self, item):
        return 'WINKWORTH DEL CAZZO'

    def imageLink(self, item):
        return self._descPattern.findall(item.find('description').text)[0][0]
