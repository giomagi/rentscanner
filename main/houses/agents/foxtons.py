from datetime import datetime
import locale
import re
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.model import Address, Price, Property

class Foxtons(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'(\d?,?\d+)\.?.*\s+per\s+(week|month)\s+(.*),\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)\. Contact Foxtons')

    def propertyFrom(self, item):
            return Property(self.agent(),
                            Price(self.priceAmount(item), self.pricePeriod(item)),
                            Address(self.fullAddress(item), self.postcode(item)),
                            self.link(item),
                            self.propertyId(item),
                            self.publicationTime(item),
                            self.description(item),
                            self.imageLink(item))

    def agentURIs(self):
        return ['http://www.foxtons.co.uk/feeds/foxtons_feed.rss?bedrooms_from=2&bedrooms_to=2&location_ids=290&price_from=300&price_to=550&result_view=rss&search_type=LL&submit_type=search']
    
    def agent(self):
        return 'Foxtons'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][0])

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
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S')

    def description(self, item):
        return self._descPattern.findall(item.find('description').text)[0][1] + '.'

    def imageLink(self, item):
        return self._descPattern.findall(item.find('description').text)[0][0]
