import shelve
from main.houses.model import Rating

class Librarian:
    propertiesArchive = "/var/gio/rentscanner/properties.data"
    ratingsArchive = "/var/gio/rentscanner/ratings.data"

    def archiveProperties(self, properties):
        propertiesRegister = shelve.open(self.propertiesArchive)
        for property in properties:
            propertiesRegister[property.key()] = property

        propertiesRegister.close()

    def retrieveNewProperties(self):
        propertiesRegister = shelve.open(self.propertiesArchive)
        ratingsRegister = shelve.open(self.ratingsArchive)

        res = [p for p in propertiesRegister.values() if p.key() not in ratingsRegister.keys()]

        propertiesRegister.close()
        ratingsRegister.close()

        return res

    def retrieveSavedProperties(self):
        propertiesRegister = shelve.open(self.propertiesArchive)
        ratingsRegister = shelve.open(self.ratingsArchive)

        interestingIds = [id for id, rating in ratingsRegister.iteritems() if rating == Rating.INTERESTING()]
        res = [p for p in propertiesRegister.values() if p.key() in interestingIds]

        propertiesRegister.close()
        ratingsRegister.close()

        return res

    def markAsNotInteresting(self, propertyId):
        self.markAs(propertyId, Rating.NOT_INTERESTING())

    def markAsInteresting(self, propertyId):
        self.markAs(propertyId, Rating.INTERESTING())

    def markAs(self, propertyId, rating):
        ratingsRegister = shelve.open(self.ratingsArchive)
        ratingsRegister[propertyId] = rating
        ratingsRegister.close()
