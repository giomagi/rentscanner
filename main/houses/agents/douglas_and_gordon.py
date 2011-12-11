import locale
import re
import urllib2
from libs.BeautifulSoup import BeautifulSoup
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Property, Price, Address

class DouglasAndGordon(PropertyExtractor):
    def __init__(self):
        super(DouglasAndGordon, self).__init__()
        self._pricePattern = re.compile(r'&#163;(\d?,?\d+)([a-zA-Z]*)')
        self._addressPattern = re.compile(r'(.*),\s+(\w*)$')

    def agentURIs(self):
        baseAddress = 'http://www.douglasandgordon.com/search/list/?a=letting&b=2&min=300&max=550&order=pricelowestfirst'

        content = urllib2.build_opener().open(urllib2.Request(baseAddress)).read()

        lastPage = BeautifulSoup(content).find('div', 'pagination').findAll('a', text=re.compile(r'^\d+$'))[-1]

        return [baseAddress + '&page=' + str(page) for page in range(1, locale.atoi(lastPage + 1))]

    def propertyFrom(self, item):
        priceMatches = self._pricePattern.findall(item.find('span', 'highlightTurqoise').text)[0]
        addressMatches = self._addressPattern.findall(item.find('div', 'propertyDetail').h2.a.contents[2].strip())[0]

        link = item.find('p', 'propertyDesc').a['href']

        return Property('DouglasAndGordon',
                        Price(locale.atoi(priceMatches[0]), priceMatches[1]),
                        Address(addressMatches[0], addressMatches[1]),
                        link,
                        link[link.rindex('=') + 1:],
                        None,
                        item.find('p', 'propertyDesc').contents[0].strip(),
                        item.find('div', 'propertyThumb').img['src'])

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('li', 'contain')
