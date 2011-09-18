import re
import urllib2
import xml.etree.ElementTree as xml

from houses.model import Property, Address

class Foxtons:
    def __init__(self):
        self.pattern = re.compile(r".(\d+)\s+per\s+(week|month)\s+(.*),\s+(\S+)")

    def _feedURI(self):
        return "http://www.foxtons.co.uk/feeds?price_from=350&price_to=500&location_ids=296&search_type=LL&result_view=rss"
    
    def properties(self):
        xmlString = urllib2.build_opener().open(urllib2.Request(self._feedURI())).read()
        tree = xml.fromstring(xmlString)

        return [self._buildProperty(item) for item in tree.findall("channel/item")]

    def _buildProperty(self, item):
        title = item.find("title").text
        matches = self.pattern.findall(title)[0]

        return Property((matches[0], matches[1]),
                        Address(matches[2], matches[3]))

def main():
    for p in Foxtons().properties():
        print p

if __name__ == "__main__":
    main()
