import boto.sdb
from main.domain.configuration import Configuration
from main.houses.model import Rating, Property

class Librarian(object):
    def __init__(self, config):
        connection = boto.sdb.connect_to_region(config.awsRegion())
        self.properties = connection.get_domain(config.propertiesDomain())
        self.ratings = connection.get_domain(config.ratingsDomain())

    def archiveProperties(self, properties):
        self.properties.batch_put_attributes(dict((p.key(), p.marshal()) for p in properties))

    def retrieveNewProperties(self):
        return [Property.unmarshal(p) for p in self.properties.select('select * from ' + self.properties.name) if not self.ratings.get_item(Property._key_from(p))]

    def retrievePropertiesWithRating(self, desiredRating):
        return [Property.unmarshal(p) for p in self.properties.select('select * from ' + self.properties.name) if self.ratings.get_item(Property._key_from(p)) and self.ratings.get_item(Property._key_from(p))['rating'] == desiredRating]

    def retrieveSavedProperties(self):
        return self.retrievePropertiesWithRating(Rating.INTERESTING())

    def retrieveDiscardedProperties(self):
        return self.retrievePropertiesWithRating(Rating.NOT_INTERESTING())

    def markAs(self, propertyId, rating):
        self.ratings.put_attributes(propertyId, {'rating' : rating})

    def markAsNotInteresting(self, propertyId):
        self.markAs(propertyId, Rating.NOT_INTERESTING())

    def markAsInteresting(self, propertyId):
        self.markAs(propertyId, Rating.INTERESTING())
