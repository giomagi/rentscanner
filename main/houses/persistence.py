import shelve
from main.houses.model import Rating

class Librarian:
    PROPERTIES_LOCATION = "/var/gio/rentscanner/properties.data"
    RATINGS_LOCATION = "/var/gio/rentscanner/ratings.data"

    def __init__(self):
        self.propertiesRegister = shelve.open(self.PROPERTIES_LOCATION)
        self.ratingsRegister = shelve.open(self.RATINGS_LOCATION)

    def archiveProperties(self, properties):
        for property in properties:
            self.propertiesRegister[property.key()] = property

    def retrieveInterestingProperties(self):
        return [p for p in self.propertiesRegister.values() if p.key() not in self.ratingsRegister.keys()]

    def markAsNotInteresting(self, agent, agentId):
        key = agent + "_" + agentId
        self.ratingsRegister[key] = Rating.NOT_INTERESTING()
