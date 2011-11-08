import locale
from datetime import datetime
import re
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.model import Address, Price, Property

class Winkworth(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+GBP\s+(\S+)\s+(\S+)')
        self._descPattern = re.compile(r'<img\s+.*\s+src="(.*)"\s*/>.*\[REF:(\w+)\]')

    def propertyFrom(self, itemSoup):
        titleMatches = self._titlePattern.findall(itemSoup.find('title').text)[0]
        descMatches = self._descPattern.findall(itemSoup.find('description').text)[0]
        pubDateAsString = itemSoup.find('pubdate').text

        return Property('Winkworth',
                        Price(locale.atoi(titleMatches[2]), titleMatches[3]),
                        Address(titleMatches[0], titleMatches[1]),
                        itemSoup.findAll(text=re.compile(r'http\://'))[0],
                        descMatches[1],
                        datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S'),
                        'WINKWORTH DEL CAZZO',
                        descMatches[0])

    def agentURIs(self):
        return ['http://www.winkworth.co.uk/rss/searchproperty?choose_type_letting=1&locality=London&radius=&ptype=&beds=2&price_min=300&price=550&under_offer=1']
