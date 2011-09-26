from datetime import datetime
import re
import urllib2
import xml.etree.ElementTree as xml

from main.houses.model import Property, Address, Price

class Foxtons:
    def __init__(self):
        self._titlePattern = re.compile(r".(\d+)\s+per\s+(week|month)\s+(.*),\s+(\S+)")
        self._idPattern = re.compile(r"(\w+)$")

    def _feedURI(self):
        return "http://www.foxtons.co.uk/feeds?price_from=350&price_to=500&location_ids=296&search_type=LL&result_view=rss"
    
    def properties(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self._feedURI())).read()
        tree = xml.fromstring(xmlString)

        return [self._buildProperty(item) for item in tree.findall("channel/item")]

    def _buildProperty(self, item):
        titleMatches = self._titlePattern.findall(item.find("title").text)[0]
        idMatch = self._idPattern.findall(item.find("guid").text)[0]

        return Property("Foxtons",
                        Price(titleMatches[0], titleMatches[1]),
                        Address(titleMatches[2], titleMatches[3]),
                        item.findall("link")[0].text,
                        idMatch,
                        datetime.strptime(item.findall("pubDate")[0].text, "%a, %d %b %Y %H:%M:%S -0000"))
