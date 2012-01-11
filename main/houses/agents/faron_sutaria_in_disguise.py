import locale
import re
import urllib2
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Address, Price, Property

class FaronSutaria(PropertyExtractor):
    def __init__(self):
        super(FaronSutaria, self).__init__()
        self._pricePattern = re.compile(r'(\d?,?\d+).*(week|month)')
        self._addressPattern = re.compile(r'(.*)\.\s+(\w*)$')

    def agentURIs(self):
        baseAddress = 'http://www.faronsutaria.co.uk/property/london/property-for-rent-in-london.html'
        content = self.urlopen(urllib2.Request(baseAddress)).read()

        lastPage = re.compile(r'initpagingex\(\d+,\s*(\d+),\s*\d+,\s*\d+\)', re.MULTILINE).findall(content)[0]

        return ['http://www.faronsutaria.co.uk/p.dtx?t=page\\results&f=results.tem&page=' + str(page) for page in
                range(1, locale.atoi(lastPage) + 1)]

    def propertyFrom(self, item):
        addressTag = item.find('div', 'paddress').a

        addressMatches = self._addressPattern.findall(addressTag.string)[0]

        priceText = item.find('td', 'plistimg_price').string.strip()
        priceMatches = ('0', 'month') if priceText.startswith('Price on application') else self._pricePattern.findall(priceText)[0]

        imageTag = item.find('img', 'imagelist')
        imageLink = 'resources/sorry_no_image.jpeg&' if imageTag is None else imageTag['src']

        return Property('FaronSutaria',
            Price(priceMatches[0], priceMatches[1]),
            Address(addressMatches[0], addressMatches[1]),
            addressTag['href'],
            addressTag['name'],
            None,
            item.find('div', id=re.compile(r'pdescription_\d+')).string,
            imageLink[:imageLink.index('&')])

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('div', 'plist')
