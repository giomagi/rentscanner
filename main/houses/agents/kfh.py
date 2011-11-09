import locale
import re
from main.houses.agents.base_extractors import RssBasedExtractor
from main.houses.model import Address, Price, Property

class KFH(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+.(\d?,?\d+)\.\d+\s+-\s+\S+\s+(\S+)')

    def propertyFrom(self, item):
        descMatches = self._titlePattern.findall(self.replaceHtmlEntitiesInTitle(item))[0]

        link = item.findall('link')[0].text
        return Property('KFH',
                        Price(locale.atoi(descMatches[2]), descMatches[3]),
                        Address(descMatches[0], descMatches[1]),
                        link,
                        self.propertyIdFrom(link),
                        None,
                        item.find('description').text,
                        'resources/sorry_no_image.jpeg')

    def agentURIs(self):
        return ['http://www.kfh.co.uk/search/rss.aspx?Section=Home&searchType=1&searchTerm=' + postcode + '&lat=&lng=&zoom=6&tenure=Per%20Month&order_by=price_desc&minprice=1000&maxprice=2500&minbeds=102&type=r&t=Thumbnail' for postcode in self.interestingZones()]

    def interestingZones(self):
        return "NW1", "NW3", "NW8", "SW1", "SW3", "SW5", "SW6", "SW7", "SW10", "SW11", "W1", "W2", "W8", "W11", "W14", "WC1", "WC2"

    def propertyIdFrom(self, link):
        link = link[0:len(link)-1]
        return link[link.rfind('/')+1:]

    def replaceHtmlEntitiesInTitle(self, item):
        return item.find('title').text.replace(u"\u00A0", ' ')

