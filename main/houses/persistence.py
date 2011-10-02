import shelve
from main.houses.model import Rating

class Librarian:
    LIBRARY_LOCATION = "/var/gio/rentscanner/properties.data"

    def __init__(self):
        self.propertiesRegister = shelve.open(self.LIBRARY_LOCATION)

    def archiveProperties(self, properties):
        for property in properties:
            key = property.key()
            if property in self.propertiesRegister.values():
                property.rating = self.propertiesRegister[key].rating

            self.propertiesRegister[key] = property

    def retrieveProperties(self):
        return [p for p in self.propertiesRegister.values() if p.rating != Rating.NOT_INTERESTING()]

    def markAsNotInteresting(self, agent, agentId):
        key = agent + "_" + agentId
        property = self.propertiesRegister[key]
        property.rating = Rating.NOT_INTERESTING()
        self.propertiesRegister[key] = property
