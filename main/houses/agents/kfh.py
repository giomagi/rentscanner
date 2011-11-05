import locale
import re
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.loader import Filter

class KFH(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+.(\d?,?\d+)\.\d+\s+-\s+\S+\s+(\S+)')

    def agentURIs(self):
        return ['http://www.kfh.co.uk/search/rss.aspx?Section=Home&searchType=1&searchTerm=' + postcode + '&lat=&lng=&zoom=6&tenure=Per%20Month&order_by=price_desc&minprice=1300&maxprice=2200&minbeds=102&type=r&t=Thumbnail' for postcode in Filter.interestingZones()]

    def agent(self):
        return 'KFH'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][2])

    def pricePeriod(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][3]

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][0]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def link(self, item):
        return item.findall('link')[0].text

    def propertyId(self, item):
        link = self.link(item)
        link = link[0:len(link)-1]
        return link[link.rfind('/')+1:]

    def publicationTime(self, item):
        return None

    def description(self, item):
        return item.find('description').text

    def imageLink(self, item):
        return 'resources/sorry_no_image.jpeg'
