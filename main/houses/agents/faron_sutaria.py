import re
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Address, Price, Property

class FaronSutaria(PropertyExtractor):

    def __init__(self):
        super(FaronSutaria, self).__init__()
        self._pricePattern = re.compile(r'(\d?,?\d+).*(week|month)')
        self._addressPattern = re.compile(r'(.*)\.\s+(\w*)$')

    def agentURIs(self):
        return ['http://www.faronsutaria.co.uk/results.dtx?getdata=true&page=1&_DSkeyindex=&branch=&display=&s=keyword&rppselect=&incsold=yes&view=list&street=&_DSMinPrice=300&_DSMaxPrice=550&_DSMinBedRooms=2&view=list&x=34&y=20']

    def propertyFrom(self, item):
        addressTag = item.find('div', 'paddress').a

        addressMatches = self._addressPattern.findall(addressTag.string)[0]
        priceMatches = self._pricePattern.findall(item.find('td', 'plistimg_price').string.strip())[0]

        imageLink = item.find('img', 'imagelist')['src']

        return Property('FaronSutaria',
                        Price(priceMatches[0], priceMatches[1]),
                        Address(addressMatches[0], addressMatches[1]),
                        addressTag['href'],
                        addressTag['name'],
                        None,
                        item.find('div', id = re.compile(r'pdescription_\d+')).string,
                        imageLink[:imageLink.index('&')])

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('div', 'plist')

