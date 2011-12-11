import re
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Price, Address, Property

class MarshAndParsons(PropertyExtractor):
    def __init__(self):
        super(MarshAndParsons, self).__init__()
        self._pricePattern = re.compile(r'&pound;(\d?,?\d+).*(week|month)')
        self._addressPattern = re.compile(r'(.*),\s+(\w*)$')

    def agentURIs(self):
        # append page-X/
        return ['http://www.marshandparsons.co.uk/properties-to-rent/property-in-london-300pw-min-550pw-max-2-beds/15-properties-per-page/order-by-price-desc/']

    def propertyFrom(self, item):
        priceMatches = self._pricePattern.findall(item.find('div', 'PropertyBriefPrice').string.strip())[0]
        addressMatches = self._addressPattern.findall(item.find('a', 'PropertyBriefAddress').string)[0]

        link = item.find('a', 'PropertyBriefAddress')['href']

        return Property('MarshAndParsons',
                        Price(priceMatches[0], priceMatches[1]),
                        Address(addressMatches[0], addressMatches[1]),
                        link,
                        link.split('/')[-2],
                        None,
                        item.find('div', 'PropertyBriefDetails').contents[0].strip().replace('...', '.'),
                        item.find('div', 'PropertyBriefThumb').a.img['src'])

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('div', 'PropertyBrief')
