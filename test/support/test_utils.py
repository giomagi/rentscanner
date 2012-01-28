import datetime
from main.houses.model import Address, Price, Property

class PropertyMaker(object):
    def aProperty(self, agent='AGENT', price=1000, fulladdress='some place', postcode='SW6', link='link', propId='123',
                  pubTime=datetime.datetime(2012, 1, 28, 10, 46, 33), desc='description', img='image'):
        return Property(agent, Price(price, 'month'), Address(fulladdress, postcode), link, propId, pubTime, desc, img)
