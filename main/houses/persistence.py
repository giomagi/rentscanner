import shelve
from main.houses.model import Rating

class Librarian:
    PROPERTIES_LOCATION = "/var/gio/rentscanner/properties.data"
    RATINGS_LOCATION = "/var/gio/rentscanner/ratings.data"

    def archiveProperties(self, properties):
        propertiesRegister = shelve.open(self.PROPERTIES_LOCATION)
        for property in properties:
            propertiesRegister[property.key()] = property

        propertiesRegister.close()

    def retrieveInterestingProperties(self):
        propertiesRegister = shelve.open(self.PROPERTIES_LOCATION)
        ratingsRegister = shelve.open(self.RATINGS_LOCATION)

        res = [p for p in propertiesRegister.values() if p.key() not in ratingsRegister.keys()]

        propertiesRegister.close()
        ratingsRegister.close()

        return res

    def markAsNotInteresting(self, propertyId):
        ratingsRegister = shelve.open(self.RATINGS_LOCATION)
        ratingsRegister[propertyId] = Rating.NOT_INTERESTING()
        ratingsRegister.close()
