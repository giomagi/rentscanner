import unittest
import datetime
from main.houses.model import Address, Price, Property

class PropertyMaker(unittest.TestCase):
    def aProperty(self, agent='AGENT', price=1000, fulladdress='some place', postcode='SW6', link='link', propId=123, pubTime=datetime.datetime.now(), desc='description', img='image'):
        return Property(agent, Price(price, 'month'), Address(fulladdress, postcode), link, propId, pubTime, desc, img)
