import locale
import re
import urllib2
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Price, Address, Property

class Shaws(PropertyExtractor):
    def __init__(self):
        super(Shaws, self).__init__()
        self.rootAddress = 'http://www.shawsestateagents.com'
        self._pricePattern = re.compile(r'&pound;(\d?,?\d+)')
        self._addressPattern = re.compile(r'(.*)\s+(\w*)$')

    def agentURIs(self):
        baseAddress = self.rootAddress + '/search/?orderby=price+desc&showstc=on&instruction_type=Letting&minprice=300&maxprice=550&bedrooms=2&image.x=35&image.y=14'
        content = urllib2.build_opener().open(urllib2.Request(baseAddress)).read()
        lastPage = locale.atoi(BeautifulSoup(content).find('div', 'pagecontrols').p.contents[0]) / 6 + 1
        return [baseAddress + 'page-' + str(page) + '/' for page in range(1, lastPage + 1)]

    def propertyFrom(self, item):
        priceMatches = self._pricePattern.findall(item.find('div', 'price').string.strip())[0]
        addressMatches = self._addressPattern.findall(item.find('p').string)[0]

        link = item.find('div', 'link').a['href']

        return Property('Shaws',
            Price(priceMatches, 'week'),
            Address(addressMatches[0], addressMatches[1]),
            self.rootAddress + link,
            link.split('/')[-1],
            None,
            'No description available for Shaws properties',
            self.rootAddress + item.find('a').img['src'])

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('div', {'id' : 'property-list'})
