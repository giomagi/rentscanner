import locale
from datetime import datetime
import re
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.model import Address, Price, Property

class Winkworth(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+GBP\s+(\S+)\s+(\S+)')
        self._descPattern = re.compile(r'<img\s+.*\s+src="(.*)"/>.*\[REF:(\w+)\]')

    def propertyFrom(self, item):
        titleMatches = self._titlePattern.findall(item.find('title').text)[0]
        descMatches = self._descPattern.findall(item.find('description').text)[0]

        return Property('Winkworth',
                        Price(locale.atoi(titleMatches[2]), titleMatches[3]),
                        Address(titleMatches[0], titleMatches[1]),
                        item.find('link').text,
                        descMatches[1],
                        self.publicationTime(item),
                        'WINKWORTH DEL CAZZO',
                        descMatches[0])

    def agentURIs(self):
        return ['http://www.winkworth.co.uk/rss/searchproperty?choose_type_letting=1&locality=London&radius=&ptype=&beds=2&price_min=300&price=550&under_offer=1']

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S')
