import locale
import re
import urllib2
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Price, Address, Property

class Sandersons(PropertyExtractor):
    def __init__(self):
        super(Sandersons, self).__init__()
        self.rootAddress = 'http://www.sandersonslondon.co.uk'
        self._pricePattern = re.compile(r'(\d?,?\d+) P\.W')
        self._addressPattern = re.compile(r'(.*),\s+(\w*)$', re.MULTILINE)

    def agentURIs(self):
        baseAddress = self.rootAddress + '/search/%d.html?instruction_type=Letting&address_keyword=&minpricew=350&maxpricew=550&bedrooms=2&image.x=52&image.y=12&part_postcode[]=W10%%2CW11%%2CW2%%2CW8%%2CSW1X%%2CSW3%%2CW14%%2CSW5%%2CSW6%%2CW1%%2CW9&orderby=price+desc'

        content = urllib2.build_opener().open(urllib2.Request(baseAddress % 1)).read()
        lastPage = BeautifulSoup(content).find('div', {'id':'page'}).p.findAll('a', text=re.compile(r'^\d+$'))[-1]
        return [baseAddress % page for page in range(1, locale.atoi(lastPage) + 1)]


    def propertyFrom(self, item):
        priceMatches = self._pricePattern.findall(item.find('div', 'price').string.strip())[0]
        propContent = item.find('div', 'prop_content')

        addressString = ' '.join([piece.strip() for piece in propContent.h2.a.contents if isinstance(piece, unicode)])
        addressMatches = self._addressPattern.findall(addressString)[0]

        link = self.rootAddress + propContent.h2.a['href']
        propIdPlusParams = link.split('/')[-1]

        return Property('Sandersons',
            Price(priceMatches, 'week'),
            Address(addressMatches[0], addressMatches[1]),
            link,
            propIdPlusParams[:propIdPlusParams.find('?')],
            None,
            propContent.p.contents[0],
            self.rootAddress + item.find('div', 'prop_image').a.img['src'])
    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('div', {'id' : 'prop_details'})
