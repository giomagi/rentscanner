from datetime import datetime
import locale
import re
import urllib2
from libs.BeautifulSoup import BeautifulSoup, NavigableString
from main.houses.agents.base_extractors import PropertyExtractor
from main.houses.model import Address, Price, Property

class Webdadi(PropertyExtractor):
    def __init__(self):
        PropertyExtractor.__init__(self)
        self._priceAmountPattern = re.compile(r'&pound;[^\d]*(\d?,?\d+)', re.MULTILINE)
        self._pricePeriodPattern = re.compile(r'(month|week|p/w)', re.MULTILINE)
        self._addressPattern = re.compile(r'(.*),\s+(\S+)')
        self._idPattern = re.compile(r'propertyid=([^"]*)$')

    def breakDownIntoItems(self, resourceContent):
        return BeautifulSoup(resourceContent).findAll('table', 'lresultsrow')

    def addressTagName(self):
        return 'lresultsaddress'

    def propertyFrom(self, item):
        priceText = item.find('td', 'lresultspricelets').contents[0]

        addressTag = (item.find('td', self.addressTagName())).a
        addressMatches = self._addressPattern.findall(addressTag.string)[0]

        link = addressTag['href'].rstrip()
        propertyId = self._idPattern.findall(link)[0]

        return Property(self.agentName(),
                        Price(locale.atoi(self._priceAmountPattern.findall(priceText)[0]),
                              self._pricePeriodPattern.findall(priceText)[0]),
                        Address(addressMatches[0], addressMatches[1]),
                        link,
                        propertyId,
                        None,
                        self.descriptionFrom(item).rstrip(' .') + '.',
                        self.imageLink(item))

    def agentName(self):
        raise NotImplementedError("Must be specified by the subclass")

    def descriptionFrom(self, item):
        for child in item.find('td', 'lresultsDescription').contents:
            if isinstance(child, NavigableString):
                return child
        return 'No description found'

    def imageLink(self, item):
        for imgTag in item.findAll('img'):
            if 'propertyid' in imgTag['src'] or 'filename' in imgTag['src']:
                imgFullLink = imgTag['src']
                return imgFullLink[:imgFullLink.index('&')] + '&amp;height=150&amp;width=200'

        return 'resources/sorry_no_image.jpeg'

class LawsonRutter(Webdadi):
    def agentName(self):
        return 'LawsonRutter'

    def agentURIs(self):
        return ['http://lettings.lawsonrutter.com/results.dtx?source=&GetData=false&Search=bycriteria&Page=1&_DSPropertyType={00000000-0000-0000-0000-000000000000}&_DSMinPrice=1200&_DSMaxPrice=2500&_DSMinBedrooms=2&_DSCustomChecks=&_DSareas=2482%2C2838%2C2483%2C1319%2C1318%2C2556%2C2484%2C2554%2C2485&rpp=1000&rppselect=10&select1=1']

class Chard(Webdadi):
    def agentName(self):
        return 'Chard'

    def agentURIs(self):
        return ['http://www.chard.co.uk/results.dtx?from=&getdata=true&search=bycriteria&page=' + str(page) + '&branch=&_DSpropertytype={00000000-0000-0000-0000-000000000000}&_DSminprice=300&_DSmaxprice=600&_DSminbedrooms=2&areas=0&_DSareas=&x=35&y=1' for page in range(1, 21)]

class Dexters(Webdadi):
    def agentName(self):
        return 'Dexters'

    def agentURIs(self):
        return ['http://lettings.dexters.co.uk/results.dtx?getdata=true&search=bycriteria&page=' + str(page) + '&_DSminbedrooms=2&_DSminprice=1200&_DSmaxprice=2500&_DSpropertytype={00000000-0000-0000-0000-000000000000}&lat=-0.3&long=51.4361123&zoom=6' for page in range(1, 76)]

    def addressTagName(self):
        return 'lresultsaddress1'
