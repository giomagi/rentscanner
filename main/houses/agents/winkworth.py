﻿import locale
from datetime import datetime
import re
from main.houses.agents.base_extractors import RssBasedExtractor

class Winkworth(RssBasedExtractor):
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')

        self._titlePattern = re.compile(r'([^,]*,[^,]*).*\s+(\S+)\s+-\s+GBP\s+(\S+)\s+(\S+)')
        self._descPattern = re.compile(r'<img\s+.*\s+src="(.*)"/>.*\[REF:(\w+)\]')

    def agent(self):
        return 'Winkworth'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][2])

    def pricePeriod(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][3]

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][0]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def link(self, item):
        return item.find('link').text

    def propertyId(self, item):
        return self._descPattern.findall(item.find('description').text)[0][1]

    def publicationTime(self, item):
        return datetime.strptime(item.findall('pubDate')[0].text, '%a, %d %b %Y %H:%M:%S +0000')

    def description(self, item):
        return 'WINKWORTH DEL CAZZO'

    def imageLink(self, item):
        return self._descPattern.findall(item.find('description').text)[0][0]
