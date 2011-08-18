import urllib2
import xml.etree.ElementTree as xml
from re_helper import *

class Foxtons:
    def __init__(self):
        pass

    def feedAddress(self):
        return "http://www.foxtons.co.uk/feeds?price_from=350&price_to=500&location_ids=296&search_type=LL&result_view=rss"
    
    def content(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self.feedAddress())).read()
        tree = xml.fromstring(xmlString)
        
        firstNode = tree.findall("channel/item")[0]
        
        print self.address(firstNode)

    def price(self, item):
        title = item.find("title").text
        price = unique(PriceFinder, title, int)
        period = unique(WeekMonthSelector, title)
        
        if (period == "week"):  return price * 52/12
        else:                   return price
    
    def address(self, item):
        title = item.find("title").text
        print unique(FoxtonsAddressFinder, title)
        print unique(PostalCodeFinder, title)


def main():
    Foxtons().content()

if __name__ == "__main__":
    main()
