import locale
import re
from datetime import datetime
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.model import Address, Price, Property

class KnightFrank(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'GBP\s+.([\d,]+)\s+(.*),\s+.*,\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)')

    def propertyFrom(self, item):
        titleMatches = self._titlePattern.findall(item.find('title').text)[0]
        descMatches = self._descPattern.findall(self.descriptionText(item))[0]

        priceAmount = locale.atoi(titleMatches[0])

        return Property('KnightFrank',
                        Price(priceAmount, self.pricePeriodFrom(priceAmount)),
                        Address(titleMatches[1], titleMatches[2]),
                        item.findall('link')[0].text,
                        self._idPattern.findall(item.find('guid').text)[0],
                        self.publicationTime(item),
                        descMatches[1],
                        descMatches[0])

    def agentURIs(self):
        return ['http://search.knightfrank.com/feeds/feedhandler.ashx?buyrent=rent&locale=en&locids=1978&minbed=2&maxbed=255&minprice=1300&maxprice=2200&curr=gbp&format=rss']

    def pricePeriodFrom(self, priceAmount):
        # ugly as hell, but knight frank doesn't publish the price period
        return 'month' if priceAmount > 1000 else 'week'

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:pubDateAsString.rfind(' ') - 1], '%a, %d %b %Y %H:%M:%S')

    def descriptionText(self, item):
        return re.sub(r'\s+', ' ', item.find('description').text)
