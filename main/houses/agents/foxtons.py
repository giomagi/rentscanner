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
        titleMatches = self._titlePattern.findall(item.find('title').text)[0]
        descMatches = self._descPattern.findall(item.find('description').text)[0]

        return Property('Foxtons',
                        Price(locale.atoi(titleMatches[0]), titleMatches[1]),
                        Address(titleMatches[2], titleMatches[3]),
                        item.findall('link')[0].text,
                        self._idPattern.findall(item.find('guid').text)[0],
                        self.publicationTime(item),
                        descMatches[1] + '.',
                        descMatches[0])

    def agentURIs(self):
        return ['http://www.foxtons.co.uk/feeds/foxtons_feed.rss?bedrooms_from=2&bedrooms_to=2&location_ids=290&price_from=300&price_to=550&result_view=rss&search_type=LL&submit_type=search']

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S')
