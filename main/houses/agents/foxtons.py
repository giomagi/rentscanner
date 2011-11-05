from datetime import datetime
import locale
import re
from main.houses.agents.base_extractors import RssBasedExtractor

class Foxtons(RssBasedExtractor):
    def __init__(self):
        RssBasedExtractor.__init__(self)
        self._titlePattern = re.compile(r'(\d?,?\d+)\.?.*\s+per\s+(week|month)\s+(.*),\s+(\S+)')
        self._idPattern = re.compile(r'(\w+)$')
        self._descPattern = re.compile(r'img src="([^"]*)".*>(.*)\. Contact Foxtons')

    def agentURI(self):
        return 'http://www.foxtons.co.uk/search?search_type=LL&managed=&openhouse=&oh_date_from=&oh_date_to=&stoppress=&sp_max_days=&submit_type=search&search_form=map&prop_type=&bedrooms=2&bedrooms_max=2&price_from=300&price_to=550&location_ids=290&new_homes_id=&dev_op=&result_view=&per_page=10&order_by=price_desc'
    
    def agent(self):
        return 'Foxtons'

    def priceAmount(self, item):
        return locale.atoi(self._titlePattern.findall(item.find('title').text)[0][0])

    def pricePeriod(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][1]

    def fullAddress(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][2]

    def postcode(self, item):
        return self._titlePattern.findall(item.find('title').text)[0][3]

    def link(self, item):
        return item.findall('link')[0].text

    def propertyId(self, item):
        return self._idPattern.findall(item.find('guid').text)[0]

    def publicationTime(self, item):
        pubDateAsString = item.findall('pubDate')[0].text
        return datetime.strptime(pubDateAsString[:len(pubDateAsString)-6], '%a, %d %b %Y %H:%M:%S')

    def description(self, item):
        return self._descPattern.findall(item.find('description').text)[0][1] + '.'

    def imageLink(self, item):
        return self._descPattern.findall(item.find('description').text)[0][0]
