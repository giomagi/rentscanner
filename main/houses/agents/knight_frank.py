import locale
import re
from datetime import datetime
from main.houses.agents.base_extractors import RssBasedExtractor

class KnightFrank(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'GBP\s+.([\d,]+)\s+(.*),\s+.*,\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)')

    def agentURI(self):
        return 'http://search.knightfrank.com/feeds/feedhandler.ashx?buyrent=rent&locale=en&locids=1978&minbed=2&maxbed=255&minprice=1300&maxprice=2200&curr=gbp&format=rss'

    def agent(self):
        return 'KnightFrank'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][0])

    def pricePeriod(self, item):
        # ugly as hell, but knight frank doesn't publish the price period
        return 'month' if self.priceAmount(item) > 1000 else 'week'

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][2]

    def link(self, item):
        return item.findall('link')[0].text

    def propertyId(self, item):
        return self._idPattern.findall(item.find('guid').text)[0]

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:pubDateAsString.rfind(' ') - 1], '%a, %d %b %Y %H:%M:%S')

    def description(self, item):
        return self._descPattern.findall(self.descriptionText(item))[0][1]

    def imageLink(self, item):
        return self._descPattern.findall(self.descriptionText(item))[0][0]

    def descriptionText(self, item):
        return re.sub(r'\s+', ' ', item.find('description').text)
